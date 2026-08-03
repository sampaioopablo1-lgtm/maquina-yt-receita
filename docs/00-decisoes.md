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

## Voz

Narração com **clonagem da voz original do operador** (arquivo
`Gravando-aprimorado-v2.wav`), não voz sintética genérica de catálogo.

Isso é uma decisão de qualidade, não estética: voz de catálogo é um dos marcadores mais
óbvios de conteúdo produzido em massa. A voz própria também é um ativo de marca que o
concorrente não replica.

> O `.wav` de referência **não** está versionado (áudio pessoal fora do git). Coloque-o em
> `assets/voice/` localmente e rode `maquina voice-clone` para registrar o `voice_id`.

## Aprovação / revisão

- Revisão humana antes de publicar: **obrigatória por padrão**.
- Aprovação por WhatsApp: **removida**. O fluxo de aprovação acontece no CLI
  (`maquina review`) e na tabela `videos` do Supabase — sem canal externo, sem número de
  telefone, sem dependência de API não oficial.

## Fora de escopo (decidido não fazer)

- Publicação automática sem revisão como padrão.
- Volume alto (>2 vídeos/dia) — ver `03-compliance-monetizacao.md`.
- Cópia de thumbnail/roteiro de canais específicos.
- Uso de ferramentas pagas de terceiros do material de origem (Dark Planner etc.); toda a
  automação equivalente está neste repositório.
