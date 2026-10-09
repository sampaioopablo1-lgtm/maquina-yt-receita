# Máquina de prospecção e agendamento

Projeto independente da máquina de vídeo (raiz deste repo) — mesma filosofia
de "roda sem credencial nenhuma" (todo provider cai num stub offline se
faltar chave), mesma estrutura de CLI + providers + Supabase como estado.

Busca leads que batem num ICP, dispara uma cadência multicanal (LinkedIn +
e-mail), detecta resposta e manda automaticamente o link para o lead escolher
um horário — um agendamento próprio, sem depender do Calendly.

## Por que "melhor" que uma ferramenta de automação de LinkedIn pura

Produtos como o Catacliente automatizam só o LinkedIn. Duas decisões
diferentes aqui:

1. **Multicanal desde o início** — LinkedIn sozinho tem teto baixo (convites/
   semana) e depende de aceite de conexão. E-mail escala mais e entra em
   paralelo na mesma cadência.
2. **O risco do LinkedIn é tratado como risco, não escondido.** Automatizar
   ações no LinkedIn viola os Termos de Uso da plataforma — não tem como
   eliminar esse risco, só mitigar (sessão por cookie em vez de senha, teto
   diário conservador, delays humanos). Por isso o provider de LinkedIn só
   liga com uma env var explícita (`PROS_LINKEDIN_RISCO_ACEITO=true`) — ver
   o aviso completo em `src/prospeccao/providers/linkedin_playwright.py`.

## Começando

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[prospeccao]"
.venv/bin/playwright install chromium   # só necessário se for usar LinkedIn de verdade
cp .env.example .env                    # preencha as chaves na secao "Maquina de prospeccao"
.venv/bin/prospectar doctor             # mostra ICP, limites e providers ativos
```

**Roda sem nenhuma credencial** (modo demo/stub): gera leads sintéticos,
"envia" mensagens só no log, e cria horários fake — dá para testar o funil
inteiro, incluindo a página de agendamento:

```bash
.venv/bin/prospectar rodar              # um ciclo: busca leads -> avança cadência -> detecta resposta
.venv/bin/prospectar status             # funil por estágio
.venv/bin/prospectar agenda-web         # sobe a pagina publica em http://localhost:8000
```

## Ligando os providers reais

| Provider | Credencial | O que faz |
|---|---|---|
| Leads | `APOLLO_API_KEY` | Busca pessoas no Apollo.io pelo ICP (cargo, setor, tamanho, localização) |
| E-mail | `RESEND_API_KEY` ou `SMTP_HOST`/`SMTP_USER`/`SMTP_PASSWORD` | Envia a sequência por e-mail |
| LinkedIn | `PROS_LINKEDIN_RISCO_ACEITO=true` + `prospectar linkedin-login` | Convites e mensagens automatizados — **leia o aviso de risco antes** |
| Agenda | `prospectar auth-google` (Google Calendar) | Lê disponibilidade real e cria o evento (com Meet) quando o lead confirma |

Sem a credencial, cada um cai automaticamente no stub — nada quebra.

## Editar o ICP e a cadência

- `config/prospeccao.yaml` — ICP (cargos, setores, tamanho de empresa,
  localização) e os tetos diários de envio.
- `config/prospeccao_templates.yaml` — texto de cada etapa da cadência
  (convite, intro, follow-ups, breakup).
- A ordem/timing das etapas (`dia_offset`, canal, qual template) fica em
  `Config.sequencia`, `src/prospeccao/config.py` — mude ali se quiser uma
  cadência diferente da padrão (convite dia 0 → e-mail dia 0 → follow-up
  LinkedIn dia 3 → follow-up e-mail dia 7 → breakup dia 12).

## Estrutura

```
src/prospeccao/
├── cli.py                       # comandos: doctor, buscar-leads, rodar, status, agenda-web, ...
├── pipeline.py                  # orquestrador (ciclo(): busca -> cadência -> resposta -> agenda)
├── agenda.py                    # slots livres + confirmação de reunião
├── web.py                       # página pública de agendamento (FastAPI)
├── sequencias.py                # renderização dos templates da cadência
├── models.py                    # Lead, Mensagem, Reuniao, ICP, EtapaSequencia
├── config.py                    # YAML + env
├── storage.py                   # SQLite local (espelha o schema do Supabase)
└── providers/
    ├── base.py                  # Protocols (BuscadorLeads, EnviadorEmail, AutomacaoLinkedIn, Calendario)
    ├── stubs.py                 # deterministicos, offline, sem credencial
    ├── reais.py                 # Apollo, SMTP/Resend, Google Calendar
    ├── linkedin_playwright.py   # automação LinkedIn (gated por risco)
    └── fabrica.py                # escolhe real vs. stub

config/prospeccao.yaml            # ICP + limites diários
config/prospeccao_templates.yaml  # texto de cada etapa
supabase/migrations/20260907_prospeccao_schema.sql
```

## O que falta para produção (não implementado ainda)

- **Sincronização com Supabase.** A migration existe (schema pronto), mas o
  `storage.py` hoje só grava em SQLite local — ainda não há um
  `sincronizacao.py` como o da máquina de vídeo. Sem isso, o estado não
  sobrevive a um runner efêmero (ex.: GitHub Actions).
- **Detecção automática de resposta.** E-mail: precisa de IMAP (ou webhook de
  inbound email, ex. Resend/SES) casando pelo thread; hoje só existe o
  caminho manual `prospectar marcar-resposta <lead_id>`. LinkedIn: o
  `checar_respostas` é best-effort e depende de seletores de UI que mudam sem
  aviso.
- **Deploy da página de agendamento.** `prospectar agenda-web` sobe local
  via uvicorn; falta hospedar (Fly/Railway/Netlify) e apontar
  `PROS_BOOKING_BASE_URL` para lá.
- **Agendamento de execução.** Não há workflow do GitHub Actions chamando
  `prospectar rodar` 1x/dia (a máquina de vídeo tem um em `.github/workflows/`
  — o mesmo padrão serve aqui).
