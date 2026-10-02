# Máquina de cold mail

Várias contas Gmail em rotação: importa a lista, envia a sequência intercalando as caixas, lê as
respostas, classifica com IA, responde e marca a reunião na agenda do closer no CRM.

```
leads.csv ──importar──▶ coldmail.db (repositório privado opc-crm-dados)
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
                                   ├─ mandou WhatsApp ──────▶ telefone no CRM + tarefa da SDR (chamar e marcar)
                                   ├─ interessado ──────────▶ pede o WhatsApp (e oferece 2 horários livres)
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

## Primeiro teste (uma caixa, você mesmo como lead)

1. **Senha de app** da caixa de envio: <https://myaccount.google.com/apppasswords> (precisa da verificação
   em duas etapas ligada). Não cole a senha em conversa nenhuma: ela vai direto no segredo.
2. **Segredo `COLDMAIL_CONTAS`** (Settings > Secrets and variables > Actions > New repository secret):
   ```json
   [{"email": "sampaioopablo@gmail.com", "senha_app": "xxxx xxxx xxxx xxxx", "nome": "Pablo Sampaio",
     "assinatura": "Pablo\nWeSales", "limite_dia": 20}]
   ```
3. **Variáveis** (aba Variables): `COLDMAIL_MODO` = `auto` (agenda sozinho), `COLDMAIL_EMPRESA` = `WeSales`,
   `COLDMAIL_OFERTA` = uma frase sobre o que vocês vendem.
4. **`leads.csv`** em `opc-crm-dados/coldmail/` só com e-mails SEUS para o teste (outra conta sua, de um sócio):
   ```csv
   email,primeiro_nome,empresa
   seu.outro.email@gmail.com,Pablo,Empresa Teste
   ```
5. No Actions, rode **Cold mail - relogio** com `testar-contas` (login), depois `simular-envio` (mostra o
   e-mail sem enviar) e por fim `relogio` (liga). Para testar fora do horário comercial, crie a variável
   `COLDMAIL_JANELA` = `0-24` durante o teste.
6. Da outra conta, responda o e-mail com um horário ("pode ser quinta às 15h?"). Em até 30 min a máquina lê,
   cria o contato e a oportunidade em FUNIL DE VENDAS > NOVO LEAD e, se o horário estiver livre na agenda
   "Reunião com closer", marca a reunião e confirma por e-mail. Se não estiver livre, responde com 2-3
   horários livres; responda escolhendo um.

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

### 2. Dados (repositório privado)

Tudo o que tem lead fica no repositório **privado** `sampaioopablo1-lgtm/opc-crm-dados`, pasta `coldmail/`,
o mesmo que o monitor do wesales já usa (segredo `DADOS_DEPLOY_KEY`, que já existe). Este repositório é
público: lead nenhum entra aqui.

| Arquivo em `opc-crm-dados/coldmail/` | Quem mexe |
|---|---|
| `leads.csv` | você: sobe e atualiza pelo site do GitHub (Add file > Upload files) |
| `coldmail.db` | a máquina: estado de cada lead, envios, respostas, bloqueios (gravado a cada ciclo) |
| `STATUS.md` | a máquina: resumo atualizado a cada ciclo |

A cada ciclo a máquina importa os e-mails novos do `leads.csv` (os repetidos e os bloqueados são ignorados).
Para mandar mais gente, é só acrescentar linhas no arquivo.

### 3. Segredos e variáveis do repositório

Configure em Settings > Secrets and variables > Actions.

| Tipo | Nome | Valor |
|---|---|---|
| Segredo | `COLDMAIL_CONTAS` | o JSON das contas (com as senhas de app) |
| Segredo | `COLDMAIL_SEQUENCIA` | opcional: substitui o `coldmail/sequencia.json` sem commit |
| Segredo | `ANTHROPIC_API_KEY` | chave da API do Claude |
| Segredo | `GHL_PIT` | já existe (o mesmo dos robôs do wesales) |
| Variável | `COLDMAIL_MODO` | `rascunho` ou `auto` |
| Variável | `COLDMAIL_EMPRESA` / `COLDMAIL_OFERTA` | nome e uma frase sobre a oferta (contexto para a IA responder) |
| Variável | `COLDMAIL_LINK_AGENDA` | link do Calendly, oferecido como alternativa aos horários |
| Variável | `COLDMAIL_POR_RODADA` | envios por conta a cada 30 min (padrão 3) |
| Variável | `COLDMAIL_JANELA` | horário de envio, padrão `8-18` |

O repositório é público, por isso as contas (com as senhas de app) ficam em segredo, não em arquivo. A
sequência está em `coldmail/sequencia.json`: é o texto que vai para os leads, não tem nada de sigiloso.

Opcionais (variáveis de ambiente): `COLDMAIL_AGENDA_ID`, `COLDMAIL_CLOSER_ID`, `COLDMAIL_SDR_ID`,
`COLDMAIL_FUNIL_ID`, `COLDMAIL_ETAPA_ID` (padrão: FUNIL DE VENDAS > NOVO LEAD) e `COLDMAIL_DURACAO_MIN` (padrão: a agenda "Reunião com closer" do `calendly_para_crm.py`, 30 min),
além de `COLDMAIL_MODELO` (padrão `claude-opus-5-5`).

### 4. Ligar

Depois de criar o segredo `COLDMAIL_CONTAS`, rode o workflow **Cold mail - relogio** com
`testar-contas` (faz login em cada caixa), depois `simular-envio` e, por fim, `relogio`. A partir daí
ele se mantém sozinho. Para desligar, apague o segredo `COLDMAIL_CONTAS`.

## Leads

Suba o `leads.csv` em `opc-crm-dados/coldmail/` pelo site do GitHub. Para conferir no PC antes:

```bash
python coldmail/tools/cold.py importar leads.csv            # confere: válidos, bloqueados, repetidos
python coldmail/tools/cold.py enviar --forcar --mostrar       # vê o texto exato que sairia
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
- `[[trecho com {variavel}]]` é opcional: some inteiro quando o lead não tem aquele dado (pode aninhar).
- As variáveis disponíveis são `{primeiro_nome}`, `{empresa}`, `{cargo}`, `{site}`, `{abertura}`,
  `{remetente}`, `{assinatura}` e as colunas extras do CSV. Variável vazia some do texto.
- Os passos depois do primeiro saem como resposta na mesma conversa ("Re: assunto"), da mesma conta.
- Escreva em texto puro, curto, sem link e sem imagem no primeiro e-mail, com uma linha de saída
  ("responda 'sair'"). A conta também envia o cabeçalho `List-Unsubscribe`.

## LGPD

Prospecção B2B por e-mail corporativo se apoia em legítimo interesse: mande só para quem tem relação com
a oferta, identifique quem está enviando e ofereça a saída em todo e-mail. A lista de bloqueio
(tabela `cold_bloqueio` do `coldmail.db`) é permanente e a importação a respeita.
