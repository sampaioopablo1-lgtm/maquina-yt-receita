# Máquina de cold mail

Várias contas Gmail em rotação: importa a lista, envia a sequência intercalando as caixas, lê as
respostas, classifica com IA, responde e marca a reunião na agenda do closer no CRM.

```
leads.csv ──importar──▶ Supabase (cold_leads)
                            │  a cada 30 min, seg-sex 8h-18h (coldmail-relogio.yml)
                            ▼
                    enviar: aquecimento + rotação ──▶ conta A, conta B, conta C, A, B, C…
                            │                          (follow-up sai sempre da mesma conta, na mesma conversa)
                            ▼
                    ler (IMAP, todas as caixas, a qualquer hora)
                            ├─ bounce ............ bloqueio, nunca mais envia
                            ├─ ausência .......... sequência continua
                            └─ resposta real ──── sequência PARA ──▶ Claude classifica e escreve a réplica
                                   ├─ aceitou horário livre ─▶ reunião na agenda "Reunião com closer" + confirmação
                                   ├─ interessado ──────────▶ réplica com 2-3 horários livres reais
                                   ├─ pediu info / objeção ─▶ rascunho no Gmail + tarefa da SDR no CRM
                                   └─ descadastro ──────────▶ bloqueio
```

A reunião cai na mesma agenda que o `wesales/tools/calendly_para_crm.py` usa, então tudo o que vem
depois já funciona: convite com Meet, pós-agendamento, `reunioes_robo.py` (confirmação, resultado e
no-show).

## Modos

| `COLDMAIL_MODO` | O que acontece com a resposta do lead |
|---|---|
| `rascunho` (padrão) | A IA escreve a réplica e ela fica nos **Rascunhos da própria conta, dentro da conversa do lead**. Quem respondeu com interesse vira contato no CRM e a SDR ganha a tarefa `[COLD] Responder e-mail`. Nada sai sem uma pessoa clicar em Enviar. |
| `auto` | "Aceitou um horário livre" → marca a reunião e confirma por e-mail. "Interessado" → responde oferecendo horários livres. As duas coisas só acontecem com confiança ≥ `COLDMAIL_CONFIANCA_MIN` (0.8). O resto continua em rascunho. |

Descadastro e bounce são sempre automáticos. Comece em `rascunho`, leia umas 30 respostas e só depois
passe para `auto`.

## Configuração (uma vez)

### 1. Contas de envio

> **Use Google Workspace em domínios secundários, não @gmail.com.** O código funciona com os dois, mas
> uma conta @gmail.com pessoal mandando prospecção é derrubada rápido pelo Google, e nela você não
> controla SPF, DKIM e DMARC. Compre 2-5 domínios parecidos com o principal (ex.: `usewesales.com.br`)
> e crie 2-3 caixas por domínio. Nunca envie pelo domínio principal.

Em cada domínio: SPF, DKIM (Admin do Google > Gmail > Autenticar e-mail) e DMARC (`p=none` para
começar), e redirecione o site do domínio para o site principal.

Em cada caixa:
1. Ative a verificação em duas etapas.
2. Gere uma **senha de app** (Conta Google > Segurança > Senhas de app). No Workspace, o administrador
   precisa permitir isso.
3. Coloque a caixa no `COLDMAIL_CONTAS` (formato em `contas.exemplo.json`). `inicio` é o primeiro dia de
   envio: a máquina começa com 5 e-mails por dia e sobe 3 por dia até o `limite_dia` (recomendado: 30).

O aumento gradual de volume não substitui o aquecimento de reputação. Deixe cada caixa nova 2-3 semanas
numa ferramenta de aquecimento (lemwarm, Warmup Inbox ou o aquecimento avulso do Instantly) antes de
colocá-la aqui, e mantenha o aquecimento ligado depois.

### 2. Banco (Supabase)

Rode `coldmail/schema.sql` no SQL Editor do Supabase. Os segredos `SUPABASE_URL` e
`SUPABASE_SERVICE_ROLE_KEY` já existem no repositório.

### 3. Segredos e variáveis do repositório

Configure em Settings > Secrets and variables > Actions.

| Tipo | Nome | Valor |
|---|---|---|
| Segredo | `COLDMAIL_CONTAS` | o JSON das contas (com as senhas de app) |
| Segredo | `COLDMAIL_SEQUENCIA` | o JSON da sequência (formato de `sequencia.exemplo.json`) |
| Segredo | `ANTHROPIC_API_KEY` | chave da API do Claude |
| Segredo | `GHL_PIT` | já existe (o mesmo dos robôs do wesales) |
| Variável | `COLDMAIL_MODO` | `rascunho` ou `auto` |
| Variável | `COLDMAIL_EMPRESA` / `COLDMAIL_OFERTA` | nome e uma frase sobre a oferta (contexto para a IA responder) |
| Variável | `COLDMAIL_LINK_AGENDA` | link do Calendly, oferecido como alternativa aos horários |
| Variável | `COLDMAIL_POR_RODADA` | envios por conta a cada 30 min (padrão 3) |
| Variável | `COLDMAIL_JANELA` | horário de envio, padrão `8-18` |

O repositório é público, por isso a sequência e as contas ficam em segredo, não em arquivo.

Opcionais (variáveis de ambiente): `COLDMAIL_AGENDA_ID`, `COLDMAIL_CLOSER_ID`, `COLDMAIL_SDR_ID` e
`COLDMAIL_DURACAO_MIN` (padrão: a agenda "Reunião com closer" do `calendly_para_crm.py`, 30 min),
além de `COLDMAIL_MODELO` (padrão `claude-opus-5-5`).

### 4. Ligar

Depois de criar o segredo `COLDMAIL_CONTAS`, rode o workflow **Cold mail - relogio** com
`testar-contas` (faz login em cada caixa), depois `simular-envio` e, por fim, `relogio`. A partir daí
ele se mantém sozinho. Para desligar, apague o segredo `COLDMAIL_CONTAS`.

## Leads

Importe no seu PC, com `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` no ambiente. A lista nunca entra
no repositório.

```bash
python coldmail/tools/cold.py importar leads.csv            # confere: válidos, bloqueados, repetidos
python coldmail/tools/cold.py importar leads.csv --aplicar
python coldmail/tools/cold.py personalizar --limite 100 --aplicar   # 1ª linha por IA lendo o site
python coldmail/tools/cold.py enviar --forcar --mostrar       # vê o texto exato que sairia
python coldmail/tools/cold.py status
```

O CSV aceita `,` ou `;` (veja `leads.exemplo.csv`). A única coluna obrigatória é `email`. As colunas
conhecidas são `primeiro_nome` (ou `nome`), `empresa`, `cargo`, `site` e `abertura`. Qualquer outra
coluna vira variável da sequência: uma coluna `segmento` pode ser usada como `{segmento}`.

**Verifique os e-mails antes de importar** (MillionVerifier, NeverBounce). Bounce acima de 2% queima o
domínio. Onde encontrar leads: Apollo (B2B em geral), Casa dos Dados (CNPJ), Apify ou Outscraper
(Google Maps), LinkedIn Sales Navigator.

## Sequência

```json
{"passos": [
  {"espera_dias": 0, "assunto": "{{primeiro_nome}, pergunta rápida|pergunta sobre a {empresa}}", "corpo": "..."},
  {"espera_dias": 3, "corpo": "..."}
]}
```

- `{Oi|Olá}` sorteia uma variação a cada e-mail. Isso evita que todos os e-mails saiam iguais.
- As variáveis disponíveis são `{primeiro_nome}`, `{empresa}`, `{cargo}`, `{site}`, `{abertura}`,
  `{remetente}`, `{assinatura}` e as colunas extras do CSV. Variável vazia some do texto.
- Os passos depois do primeiro saem como resposta na mesma conversa ("Re: assunto"), da mesma conta.
- Escreva em texto puro, curto, sem link e sem imagem no primeiro e-mail, com uma linha de saída
  ("responda 'sair'"). A conta também envia o cabeçalho `List-Unsubscribe`.

## LGPD

Prospecção B2B por e-mail corporativo se apoia em legítimo interesse: mande só para quem tem relação com
a oferta, identifique quem está enviando e ofereça a saída em todo e-mail. A lista de bloqueio
(`cold_bloqueio`) é permanente e a importação a respeita.
