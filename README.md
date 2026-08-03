# Máquina de vídeo — YouTube

Pipeline automatizada de criação, edição e publicação de vídeos para o canal
[@SetiapLevelID](https://www.youtube.com/@SetiapLevelID) (Setiap Level).

Da pauta ao vídeo publicado: roteiro → narração → visuais → legendas → render →
thumbnail → checagens de compliance → upload agendado → diagnóstico de métricas.

## Começando

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
cp .env.example .env          # preencha as chaves
.venv/bin/maquina doctor      # confere ambiente e providers ativos
```

**Roda sem nenhuma credencial.** Todo provider sem chave cai num stub offline que
produz assets reais (áudio com duração correta, PNG de verdade), então a pipeline
inteira — inclusive o render do ffmpeg — executa e pode ser validada sem gastar
crédito:

```bash
MAQ_LLM_PROVIDER=stub MAQ_TTS_PROVIDER=stub MAQ_IMAGE_PROVIDER=stub \
  .venv/bin/maquina produzir "Titulo de teste" --formato shorts
```

## Comandos

| Comando | O que faz |
|---|---|
| `maquina doctor` | Ambiente, credenciais e providers ativos |
| `maquina pesquisar "<termo>"` | Descobre o que performa no subnicho (pilar 1) |
| `maquina ideias --formato longo` | Gera pautas candidatas |
| `maquina produzir "Título"` | Ideia → MP4 renderizado (não publica) |
| `maquina auto --formato longo` | Escolhe pauta, produz e passa nas checagens |
| `maquina listar` | Estado de cada vídeo |
| `maquina retomar <slug>` | Continua um vídeo interrompido, sem refazer |
| `maquina publicar <slug>` | Publica com agendamento (após revisão) |
| `maquina diagnosticar` | Aponta qual dos 3 pilares é o gargalo |
| `maquina revisar <slug>` | Traduz o roteiro e avalia se soa natural |
| `maquina comentarios <slug>` | Traduz comentários e extrai sinais técnicos |
| `maquina custo` | Custo de produção por vídeo |
| `maquina auth-youtube` | Autoriza a conta (uma vez, local) |
| `maquina voice-clone <audios>` | Registra sua voz e devolve o `voice_id` |
| `maquina voice-test` | Amostra no idioma do canal para avaliação nativa |

## Arquitetura

Três responsabilidades com requisitos incompatíveis, em três lugares:

- **GitHub Actions** — o motor. Cron nativo, secrets, ffmpeg já instalado no runner.
- **Supabase** — o estado. Roteiros, métricas, calendário, painel.
- **Colab** — só laboratório. Testar voz, Whisper, prompts.

Comparativo completo e por que Colab não serve como motor: [`docs/01-arquitetura.md`](docs/01-arquitetura.md).

## Os 3 pilares

A máquina otimiza três métricas, nesta ordem — acertar duas e errar uma derruba o vídeo:

| Pilar | Métrica | Meta |
|---|---|---|
| Título | Impressões | crescendo |
| Thumbnail | CTR | ≥ 5% (bom a partir de 7-8%) |
| Roteiro | Retenção média | ≥ 30% |

`maquina diagnosticar` converte a combinação em um gargalo nomeado: CTR alto com
retenção baixa significa problema de **roteiro**, não de thumbnail — e evita
refazer a coisa errada. Detalhes em [`docs/02-playbook-youtube.md`](docs/02-playbook-youtube.md).

## Canal em idioma estrangeiro

O canal é em indonésio e o operador não lê o idioma. Duas ferramentas fecham essa
lacuna — sem elas a revisão humana vira carimbo:

- `maquina revisar <slug>` — traduz o roteiro e classifica a naturalidade
- `maquina comentarios <slug>` — traduz os comentários e destaca sinais técnicos
  (volume de música, qualidade da voz, ritmo), que aparecem ali antes de aparecerem
  na curva de retenção

## Barreiras antes de publicar

O modo de falha mais caro aqui não é um vídeo ruim — é o canal perder monetização
por conteúdo repetitivo ou spam de automação. Publicar diariamente não viola
política; produzir em massa com variação mínima, sim. Por isso o ritmo diário vem
com pressão ativa por variação:

- Teto de **3 publicações/dia** (a cota da API permite ~6)
- Roteiro **>65% similar** aos últimos 30 → bloqueia
- **7 eixos temáticos rotacionados** — força variação estrutural na origem
- Título quase idêntico a outro do canal → bloqueia
- Divulgação de conteúdo sintético automática no upload
- **Revisão humana obrigatória por padrão**

Fundamentação e links das políticas oficiais: [`docs/03-compliance-monetizacao.md`](docs/03-compliance-monetizacao.md).

## Estrutura

```
src/maquina/
├── cli.py              # comandos
├── pipeline.py         # orquestrador com retomada
├── models.py           # domínio (Video, Roteiro, Cena, Métricas)
├── config.py           # YAML + env
├── media.py            # ffmpeg: Ken Burns, concat, trilha, legendas
├── storage.py          # SQLite (espelha o schema do Supabase)
├── providers/          # Anthropic, OpenAI, ElevenLabs + stubs offline
└── stages/
    ├── roteiro.py      # ideação e roteirização
    ├── producao.py     # narração, visuais, legendas SRT
    ├── render.py       # montagem do MP4 e da thumbnail
    ├── compliance.py   # barreiras pré-upload
    ├── youtube.py      # upload resumable + Analytics
    └── diagnostico.py  # gargalo dos 3 pilares

.github/workflows/      # producao (cron), publicacao (manual), diagnostico, ci
supabase/schema.sql     # tabelas, views painel_pilares e progresso_ypp
docs/                   # decisões, arquitetura, playbook, compliance
```

## Testes

```bash
MAQ_LLM_PROVIDER=stub MAQ_TTS_PROVIDER=stub MAQ_IMAGE_PROVIDER=stub .venv/bin/pytest -q
```

13 testes, sem rede e sem custo — incluindo um render real de ponta a ponta que
valida o MP4 gerado.

## Próximos passos

Ver [`docs/04-roadmap.md`](docs/04-roadmap.md).
