# Arquitetura: onde a máquina roda

## A pergunta: "Colab é o caminho mais eficiente e gratuito?"

Resposta curta: **não para produção.** O Colab é ótimo para *experimentar*, e péssimo
para *operar um canal*. O erro de arquitetura mais comum aqui é tentar usar uma
ferramenta só. Este projeto separa três responsabilidades que têm requisitos
tecnicamente incompatíveis:

| Responsabilidade | O que exige | Onde roda |
|---|---|---|
| **Processamento pesado** (render de vídeo, ffmpeg, TTS, imagens) | CPU/RAM, minutos de execução, disco temporário | GitHub Actions |
| **Estado e controle** (ideias, roteiros, calendário, métricas, jobs) | Banco persistente, consulta, dashboard | Supabase |
| **Experimentação** (testar voz, testar prompt, GPU pontual) | Interatividade, GPU grátis | Colab |

## Comparativo honesto

### Google Colab
- **A favor:** grátis, GPU disponível, zero setup, bom para testar clonagem de voz e Whisper.
- **Contra — e isto é eliminatório:**
  - A sessão **morre**: desconecta por inatividade (~90 min) e tem teto de ~12h mesmo ativa.
  - **Não tem agendador.** Não existe cron. Publicar "toda terça 18h" exige o navegador aberto.
  - Segredos ficam expostos no notebook ou dependem de montar o Drive.
  - Sem versionamento real do código — notebook não é histórico de mudanças.
  - O Termos de Uso do Colab desencoraja uso não interativo prolongado; automação 24/7 é
    exatamente o caso que pode ser limitado no tier gratuito.
- **Veredito:** ferramenta de laboratório, não de linha de produção. Mantemos para o que
  ele é bom (ver `notebooks/`).

### GitHub Actions ← **motor escolhido**
- **A favor:**
  - **Cron nativo** (`schedule:`) — o canal publica sozinho, sem ninguém logado.
  - **Secrets criptografados** de primeira classe (`ANTHROPIC_API_KEY`, token do YouTube).
  - Runner `ubuntu-latest` **já vem com ffmpeg instalado**.
  - Código versionado, cada execução tem log auditável, artefatos baixáveis.
  - Cota gratuita: repositório **público = ilimitado**; privado = 2.000 min/mês no plano Free.
- **Contra:** teto de 6h por job (irrelevante — nosso render fica em minutos); não tem GPU
  no tier grátis; disco do runner é efêmero (por isso o estado vai para o Supabase).
- **Custo real estimado:** um vídeo longo renderiza em ~4-8 min de runner. 30 vídeos/mês
  ≈ 240 min → cabe folgado nos 2.000 min gratuitos mesmo com repositório privado.

### Supabase ← **estado escolhido**
- **A favor:** Postgres gerenciado, Storage para os assets, Auth, e um painel pronto para
  você olhar o que a máquina está fazendo. Tier gratuito generoso para este volume.
- **Contra — importante não errar aqui:** Edge Functions rodam em **Deno com timeout
  curto (~150s)** e **não têm ffmpeg**. Não tente renderizar vídeo no Supabase. Ele é o
  cérebro/memória, não o músculo.
- **Papel neste projeto:** tabelas de `ideias`, `roteiros`, `videos`, `publicacoes`,
  `metricas` — e é o que permite a máquina aprender com o que já publicou
  (ex.: "não repetir tema", "priorizar padrão de título com melhor CTR").

### VPS / Cloud Run (alternativa futura)
Só vale quando o volume passar da cota do Actions ou quando você precisar de render com
GPU. Custo a partir de ~US$ 5/mês. **Não é necessário agora** — anotado como plano de
escala, não como passo atual.

## Arquitetura escolhida

```
                    ┌──────────────────────────────┐
   cron / manual ──▶│      GitHub Actions          │
                    │  (motor: roda a pipeline)    │
                    └───────────┬──────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
  ┌───────────┐          ┌────────────┐          ┌─────────────┐
  │  LLM      │          │   TTS      │          │  Imagens    │
  │ (roteiro) │          │ (narração) │          │  (b-roll)   │
  └─────┬─────┘          └──────┬─────┘          └──────┬──────┘
        └───────────────────────┼───────────────────────┘
                                ▼
                       ┌─────────────────┐
                       │ ffmpeg (render) │  9:16 Shorts | 16:9 longo
                       └────────┬────────┘
                                ▼
                       ┌─────────────────┐
                       │ YouTube Data API│  upload resumable + agendamento
                       └────────┬────────┘
                                ▼
                    ┌──────────────────────────────┐
                    │        Supabase              │
                    │ estado, métricas, calendário │
                    └──────────────────────────────┘
                                ▲
                    ┌───────────┴──────────────────┐
                    │   Colab (só laboratório):    │
                    │ testar voz, Whisper, prompts │
                    └──────────────────────────────┘
```

## Por que GitHub e não "plugin nativo do ChatGPT/Codex"

Integração nativa com o chat é excelente para *você conversar com o projeto*. Ela não
resolve o problema central de um canal: **executar sozinho, no horário certo, sem você.**
Um plugin só age quando alguém está do outro lado pedindo. Um cron do Actions age às 3h
da manhã de domingo. O canal precisa da segunda coisa.

O uso natural das integrações nativas continua valendo, e este repositório está montado
para isso: o código está no GitHub (o Codex/Claude lê e edita direto), e o estado no
Supabase (o conector lê as métricas e te responde "qual vídeo rendeu mais"). As duas
integrações viram *interface*, e o Actions continua sendo o *motor*.
