# Decisões do projeto

Registro das decisões tomadas, para não serem re-discutidas a cada sessão.

## Canal

| Item | Decisão |
|---|---|
| Nome | Setiap Level |
| Handle | [@SetiapLevelID](https://www.youtube.com/@SetiapLevelID) — já criado, dar continuidade |
| Idioma | Indonésio (`id`) |
| Tema | Dinheiro, trabalho, status e decisões |
| Público | Geral/adulto — **não** infantil (`madeForKids: false`) |
| Tipo | Subnichado, sem rosto (narração própria clonada) |
| Assets prontos | `setiap-level-avatar.png`, `setiap-level-banner.png` |

## Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Linguagem | Python 3.11 | Ecossistema de mídia e APIs |
| Motor de execução | GitHub Actions | Cron nativo, secrets, ffmpeg pré-instalado |
| Estado | Supabase (Postgres) | Persistência + painel + leitura via conector |
| Render | ffmpeg | Único caminho sério para composição de vídeo |
| Laboratório | Google Colab | Só experimentação e GPU pontual |

Comparativo completo e justificativa: `01-arquitetura.md`.

## Formato

Ambos, com papéis distintos:
- **Longo 16:9 (1920x1080)** — ativo principal, caminho realista para as 4.000h do YPP.
- **Shorts 9:16 (1080x1920)** — aquisição e teste de gancho.

## Idioma: indonésio (decisão estratégica confirmada)

Mantido por decisão do operador. Como o operador não lê indonésio, duas lacunas reais
precisam de compensação — e ambas estão implementadas:

| Lacuna | Compensação |
|---|---|
| Não dá para julgar se o roteiro soa natural | `maquina revisar <slug>` traduz e avalia naturalidade |
| Não dá para ler os comentários | `maquina comentarios <slug>` traduz e extrai sinais técnicos |

A leitura de comentários não é conveniência: segundo o próprio material estudado, é onde
o diagnóstico aparece antes do gráfico de retenção ("música alta"). Num canal em idioma
estrangeiro, sem tradução esse canal de feedback simplesmente não existe.

## Voz — a validar antes de escalar

A intenção é usar a **voz clonada do operador** (`Gravando-aprimorado-v2.wav`), porque voz
de catálogo é um dos marcadores mais óbvios de conteúdo produzido em massa, e a voz
própria é um ativo que o concorrente não replica.

⚠️ **Risco em aberto:** o clone é de um falante de português gerando indonésio. O
`eleven_multilingual_v2` carrega características de pronúncia do falante original, e uma
audiência nativa percebe sotaque em segundos — batendo direto no pilar 3 (retenção).

**Decisão: testar antes de escalar.** Rode `maquina voice-test`, envie a amostra para um
falante nativo e pergunte se a pronúncia soa nativa. Se soar estrangeira, troque para voz
nativa de catálogo e fixe uma só como identidade do canal.

> O `.wav` **não** é versionado (áudio pessoal fora do git). Coloque em `assets/voice/` e
> rode `maquina voice-clone`.

## Aprovação / revisão

- Revisão humana antes de publicar: **obrigatória por padrão**.
- Aprovação por WhatsApp: **removida**. O fluxo de aprovação acontece no CLI
  (`maquina review`) e na tabela `videos` do Supabase — sem canal externo, sem número de
  telefone, sem dependência de API não oficial.

## Ritmo: diário

Escolha do operador. Publicar diariamente **não viola política por si só** — a regra do
YouTube mira "produção em massa com variação mínima", não frequência.

O risco que o volume cria é convergência: 30 vídeos/mês no mesmo subnicho tendem a ficar
parecidos sozinhos. Por isso o ritmo diário veio acompanhado de três ajustes, e não só de
um teto maior:

| Parâmetro | Antes | Diário | Motivo |
|---|---|---|---|
| Teto/dia | 2 | 3 | Cota da API permite ~6 uploads/dia |
| Similaridade máx. | 0.75 | **0.65** | Mais rigoroso: volume converge sozinho |
| Janela de comparação | 20 | **30** | Cobre ~1 mês de publicação |
| Eixos temáticos | — | **7 rotacionados** | Força variação estrutural na origem |

A rotação de eixos é determinística de propósito: sorteio aleatório repete eixo por acaso
com frequência alta em ritmo diário. Com 7 eixos, 7 vídeos seguidos percorrem 7 estruturas
distintas antes de reiniciar.

**Custo estimado:** ~US$ 2,70/vídeo (TTS domina) → **~US$ 80/mês** em ritmo diário.
Acompanhe com `maquina custo` e compare com o RPM observado.

## Fora de escopo (decidido não fazer)

- Publicação automática sem revisão como padrão.
- Volume acima do teto diário configurado — ver `03-compliance-monetizacao.md`.
- Cópia de thumbnail/roteiro de canais específicos.
- Uso de ferramentas pagas de terceiros do material de origem (Dark Planner etc.); toda a
  automação equivalente está neste repositório.
