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

## Voz — Fish Audio (decisão herdada do processo anterior)

A voz do operador **já está clonada no Fish Audio** — modelo "Pablo (eu)",
id `0f8b54a7ec2f4d328a146db341ab63ad` (público, é a URL do modelo). O provider `fish`
está implementado e é o padrão da config.

A referência master também já existe: `Gravando-aprimorado-v2.wav` tratado — 71,5s, mono
48 kHz, pico -1 dB, ruído ~50 dB abaixo da voz. Se precisar reclonar em outro serviço, é
esse arquivo que se usa (fica em `assets/voice/`, fora do git).

🔴 **Segurança:** a chave de API do Fish foi colada em texto aberto no chat do ChatGPT e
está no export dessa conversa. **Revogar a chave "chatgpt" e gerar outra** antes de usar
o provider. A nova chave só existe como env `FISH_AUDIO_API_KEY`.

**Caminho gratuito** (registrado no processo anterior, para quando não houver assinatura):
1. **Gravar a própria narração** — automatiza-se tudo menos a voz. Zero custo, zero
   risco de licença.
2. **Chatterbox Indonesian no Colab** (modelo aberto, exige GPU CUDA) — é exatamente o
   papel de laboratório que `01-arquitetura.md` reserva ao Colab. Validar licença
   comercial antes de usar no canal.

⚠️ **Risco em aberto (continua):** clone de falante de português gerando indonésio tem
sotaque. Rode `maquina voice-test` e valide com um nativo antes de escalar — vale para o
Fish tanto quanto valia para o ElevenLabs.

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

## Decisões herdadas do processo no ChatGPT (export estudado em 04/08/2026)

| Decisão | Detalhe |
|---|---|
| Nome do canal | "Level Hidup" estava ocupado → **Setiap Level** |
| Primeira pauta | **"7 níveis de salário na Indonésia"** — já estruturada, é o episódio 1 |
| Trilha sonora | **YouTube Audio Library** (grátis, sem risco de direitos) — não gerar música por IA |
| Conta Google | Tem **vários canais antigos** — todo OAuth deve confirmar que é o Setiap Level |
| Cadência | "15/dia" é o limite de seleção do Studio, não permissão; limite real varia por canal |
| Expectativa | "Monetizar em 48h" não existe: YPP exige 1.000 inscritos + 4.000h + revisão |
| **Identidade visual** | Doodle: fundo branco, linhas pretas irregulares, poucas cores, 1 imagem/cena, 16:9 — codificada no prompt de roteiro |
| País BR no canal | **Deliberado**: residência jurídica/pagamentos do dono; conteúdo segue indonésio |
| Trilha (nível) | -28 a -24 LUFS sob a voz; ganho padrão do mixer ajustado para -24 dB |
| Teste A/B | YouTube permite testar até 3 títulos/thumbnails em vídeos longos — usar quando houver impressões |
| Render (backlog) | Remotion avaliado como alternativa programática ao ffmpeg — não necessário agora |

Sobre a última linha: a meta operacional do projeto é constância e qualidade dos 3
pilares. Receita é consequência do acervo, não meta de curto prazo — qualquer promessa
diferente disso já foi identificada como marketing de mentoria no material de origem.

## Fora de escopo (decidido não fazer)

- Publicação automática sem revisão como padrão.
- Volume acima do teto diário configurado — ver `03-compliance-monetizacao.md`.
- Cópia de thumbnail/roteiro de canais específicos.
- Uso de ferramentas pagas de terceiros do material de origem (Dark Planner etc.); toda a
  automação equivalente está neste repositório.
