# Biblioteca de mensagens versionada — R-04

Fonte da verdade dos textos das 3 mensagens automáticas da Cadência 12x30
(`build-wesales.md`, seção 2.6). Em Reev/Meetime o template é objeto de
primeira classe, com desempenho próprio — aqui virava texto solto dentro do
nó do workflow, sem código e sem histórico. Este documento é o que fecha essa
diferença: cada texto tem um código, cada edição gera uma versão nova, e o
campo `Template usado` (C-23, `campos-e-tags.md`) grava qual saiu para cada
contato.

## Regra de versionamento

**Nunca edite um texto em vigor.** Editar o texto de `M1-v1` sem trocar o
código quebra a régua: toda resposta anterior à edição fica atribuída a um
texto que não existe mais, e a comparação de desempenho perde o chão. O
fluxo correto:

1. Escreva a nova versão numa linha nova, com código seguinte (`M1-v1` →
   `M1-v2`; variante de teste A/B do R-05 usa sufixo de letra, `M1-a`/`M1-b`,
   não número — os dois formatos convivem porque significam coisas
   diferentes: `-v2` substitui, `-a`/`-b` compete).
2. Marque a linha antiga como `Substituído em <data>` na coluna Status.
   Nunca apague a linha: é o histórico que permite comparar depois.
3. Troque o texto no nó de envio do workflow (`build-wesales.md`, seção 2.6)
   para o novo código.
4. Campo `Template usado` é `TEXT` (não `SINGLE_OPTIONS`) exatamente para
   este passo não exigir editar a lista de opções do campo na tela — o
   workflow escreve o código novo direto.

## Templates ativos

| Código | Canal | Nó de envio | Desde | Status |
|---|---|---|---|---|
| `M1-v1` | WhatsApp | Cadência 12x30 — T1, D1 08:45 | 18/09/2026 | Substituído em 18/09/2026 (R-05) |
| `M1-a` | WhatsApp | Cadência 12x30 — T1, D1 08:45, Caminho A do Split (50%) | 18/09/2026 | Ativo — teste A/B (R-05) |
| `M1-b` | WhatsApp | Cadência 12x30 — T1, D1 08:45, Caminho B do Split (50%) | 18/09/2026 | Ativo — teste A/B (R-05) |
| `M2-v1` | WhatsApp | Cadência 12x30 — após T8, D10 13:30 | 18/09/2026 | Ativo |
| `M3-v1` | WhatsApp | Cadência 12x30 — após T12, D30 17:45 | 18/09/2026 | Ativo |
| `MI-0` | WhatsApp | Cadência Inbound — imediata, antes da TI1 (R-07) | 18/09/2026 | Ativo |
| `MI-F` | WhatsApp | Cadência Inbound — handoff ao fim da TI5 (R-07) | 18/09/2026 | Ativo |
| `RE-1` | WhatsApp | Reengajamento 90 dias — imediata, antes da TR1 (R-08) | 18/09/2026 | Ativo |
| `RE-2` | WhatsApp | Reengajamento 90 dias — handoff ao fim da TR4 (R-08) | 18/09/2026 | Ativo |
| `NS-1` | WhatsApp | Recuperação de No-show — imediata, antes da NS1 (R-12) | 18/09/2026 | Ativo |
| `NS-2` | WhatsApp | Recuperação de No-show — handoff ao fim da NS3 (R-12) | 18/09/2026 | Ativo |
| `PA-CONF` | WhatsApp | Pós-agendamento — confirmação imediata, nó 7 (R-12/seção 5) | 22/09/2026 | Ativo |
| `PA-R24` | WhatsApp | Pós-agendamento — lembrete 24h antes, nó 8 | 22/09/2026 | Ativo |
| `PA-R3H` | WhatsApp | Pós-agendamento — lembrete 3h antes, nó 9 | 22/09/2026 | Ativo |
| `PA-R30` | WhatsApp | Pós-agendamento — lembrete curto 30min antes, nó 10 | 22/09/2026 | Ativo |

## M1-v1 — abertura, pede permissão de ligar (substituído)

**Substituído em 18/09/2026** pelo teste A/B do R-05: o texto seguiu
idêntico em `M1-a` (só trocou de código, para caber no par que o Split
compara), e ganhou um concorrente novo em `M1-b`. Linha e texto ficam aqui
por regra de versionamento — nunca apagar, é o que permite comparar depois.

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}.
> Vi que vocês trabalham com {{contact.segmento}} e queria te fazer 2 perguntas
> rápidas sobre captação de clientes. Posso te ligar hoje ou prefere por aqui?

## M1-a — abertura, pergunta de diagnóstico (teste A/B — R-05)

Caminho A do Split especificado em `build-wesales.md`, seção 2.6.1. Mesmo
texto de `M1-v1`: é o "braço de controle" do teste, o gancho já em produção
contra o qual `M1-b` compete.

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}.
> Vi que vocês trabalham com {{contact.segmento}} e queria te fazer 2 perguntas
> rápidas sobre captação de clientes. Posso te ligar hoje ou prefere por aqui?

Sem `[Agendar com o closer]` de propósito: é a mensagem que pergunta permissão
de ligar, e um link ali compete com a pergunta em vez de reforçá-la.

## M1-b — abertura, gancho de dor do segmento (teste A/B — R-05)

Caminho B do Split especificado em `build-wesales.md`, seção 2.6.1. Único
elemento que muda em relação a `M1-a`: a primeira frase depois da
apresentação troca a pergunta de diagnóstico genérica por uma dor específica
do segmento, para testar se nomear o problema antes de perguntar gera mais
resposta do que perguntar direto. Saudação, `{{contact.segmento}}`, ausência
de link e a pergunta de fechamento são as mesmas de `M1-a`, de propósito —
variar só o gancho é o que deixa a comparação limpa.

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}.
> A maioria das empresas de {{contact.segmento}} que eu falo perde cliente
> novo não por falta de anúncio, mas por demora pra responder o lead. É o seu
> caso também, ou vocês já resolveram isso? Posso te ligar hoje ou prefere
> por aqui?

Sem `[Agendar com o closer]`, pelo mesmo motivo de `M1-a`.

## M2-v1 — reforço

> {{contact.first_name}}, tentei falar com você algumas vezes e não quero ser
> chato. Uma linha só: hoje vocês trazem cliente novo mais por indicação ou por
> anúncio? Se for indicação, tenho um caso que talvez te interesse. Se preferir
> já reservar 30 min direto, sem esperar minha ligação: [Agendar com o closer]

## M3-v1 — encerramento

> {{contact.first_name}}, vou parar de te procurar por aqui. Se um dia quiser
> falar sobre captação, me responde esta mensagem que eu retomo de onde paramos.
> Ou, se quiser adiantar, o link continua de pé: [Agendar com o closer]
> Sucesso!

`[Agendar com o closer]` é o Trigger Link da seção 2.9 do `build-wesales.md`,
não texto literal — insira pelo ícone `{}` da caixa de mensagem, em Custom
Values → Trigger Links.

## MI-0 — confirmação imediata (Cadência Inbound — R-07)

Especificada em `build-wesales.md`, seção 2.10. Dispara no instante em que
o lead entra em `Em cadência` pela origem inbound, antes de qualquer
tentativa de ligação. Objetivo: o lead saber que foi ouvido antes mesmo do
telefone tocar — o equivalente, do lado do lead, ao que o Meetime documenta
como notificar o SDR "independente de onde ele esteja".

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}.
> Recebi seu contato agora e já vou te ligar em poucos minutos. Se preferir
> me responder por aqui enquanto isso, também tá valendo.

Sem `[Agendar com o closer]` de propósito: é a mesma lógica de `M1-a`/`M1-b`
— a mensagem que promete uma ligação não deve competir com um link.

## MI-F — handoff para a régua normal (Cadência Inbound — R-07)

Especificada em `build-wesales.md`, seção 2.10, nó 1 do handoff. Dispara se
as 5 tentativas rápidas (5 min a 3 dias) terminam sem conexão — o lead não
sai da máquina, entra na Cadência 12x30 pela ação `Add to Workflow`.

> {{contact.first_name}}, tentei falar com você algumas vezes nos últimos
> dias sem sucesso. Vou continuar te procurando por mais tempo — se quiser
> adiantar, o link continua de pé: [Agendar com o closer]

`[Agendar com o closer]` é o Trigger Link da seção 2.9 do `build-wesales.md`,
mesmo uso de `M2-v1`/`M3-v1`.

## RE-1 — reabertura (Reengajamento 90 dias — R-08)

Especificada em `build-wesales.md`, seção 2.12. Dispara no instante em que
o lead reativado entra em `Em cadência` pela régua de reengajamento, 90
dias depois de cair em `Nutrição`. Tom deliberadamente diferente de
`M1-a`/`M1-b`: não é a primeira abordagem, é uma retomada — a mensagem
reconhece o tempo passado em vez de fingir que é um primeiro contato, e
pergunta se vale a pena retomar em vez de pedir permissão de ligar (essa
pergunta já foi feita e respondida com silêncio da primeira vez).

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da
> {{location.name}} de novo. Já faz um tempo que a gente não troca uma
> ideia — como estão as coisas aí em captação de clientes? Vale a pena
> retomar a conversa, ou ainda não é o momento?

Sem `[Agendar com o closer]`, mesmo motivo de `M1-a`/`M1-b`/`MI-0`: é a
mensagem que reabre o diálogo, um link ali compete com a pergunta.

## RE-2 — handoff de volta para a nutrição (Reengajamento 90 dias — R-08)

Especificada em `build-wesales.md`, seção 2.12, no fim da régua TR1-TR4.
Dispara se as 4 tentativas de reengajamento terminam sem conexão — o lead
não sai da máquina, volta para `Nutrição` e o próprio workflow de
reengajamento dispara de novo dali a mais 90 dias, sozinho.

> {{contact.first_name}}, não consegui falar com você dessa vez também.
> Vou deixar quieto por mais um tempo e volto a tentar depois — se antes
> disso quiser conversar, é só responder aqui ou usar o link:
> [Agendar com o closer]

`[Agendar com o closer]` é o Trigger Link da seção 2.9 do
`build-wesales.md`, mesmo uso de `M2-v1`/`M3-v1`/`MI-F`.

## NS-1 — sentimos sua falta (Recuperação de No-show — R-12)

Especificada em `build-wesales.md`, seção 5.3, ramo Recuperação. Dispara no
instante em que o closer marca a reunião como `No Show`, antes da tarefa
`NS1` nascer para o SDR. Com link de propósito, diferente de `M1-a`/`M1-b`/
`RE-1`/`MI-0`: aqui a mensagem inteira existe para gerar um reagendamento, e
o link é o caminho mais rápido para isso — não compete com pergunta nenhuma,
porque não há pergunta de diagnóstico aqui.

> Oi {{contact.first_name}}, vi que não conseguimos nos falar no horário
> combinado — imagino que bateu algum imprevisto! Sem problema nenhum, é só
> escolher um novo horário aqui: [Agendar com o closer]. Se preferir, me
> chama por aqui mesmo que eu te ajudo a remarcar.

## NS-2 — handoff de volta para a nutrição (Recuperação de No-show — R-12)

Especificada em `build-wesales.md`, seção 5.3, fim do ramo Recuperação.
Dispara se as 3 tentativas de recuperação (NS1-NS3) terminam sem
reagendamento — o lead não sai da máquina, volta para `Nutrição` e o
Reengajamento 90 dias (seção 2.12, R-08) reativa sozinho dali a 90 dias.
Mesmo padrão de `RE-2`/`MI-F`: reconhece a tentativa, deixa a porta aberta,
inclui o link.

> {{contact.first_name}}, tentei falar com você algumas vezes depois do
> nosso horário perdido e não consegui. Vou parar de te procurar por agora,
> mas se quiser remarcar quando for melhor, o link continua de pé:
> [Agendar com o closer]

`[Agendar com o closer]` é o Trigger Link da seção 2.9 do `build-wesales.md`,
mesmo uso de `M2-v1`/`M3-v1`/`MI-F`/`RE-2`.

## PA-CONF — confirmação imediata (Pós-agendamento — R-12/seção 5)

Especificada em `build-wesales.md`, seção 5, nó 7. Dispara no instante em
que o SDR confirma o horário na tela, junto com a nota de qualificação —
texto que já existia solto no modelo do nó 7 desde a migração de
19/09/2026, sem código nem versão própria; ganhou os dois nesta rodada
(G-05, peça 2) para poder entrar na guarda de janela como as outras
mensagens automáticas.

> {{contact.first_name}}, reunião confirmada para
> {{appointment.start_time}}. Vou te mandar o link aqui mesmo 30 min antes. Se
> precisar remarcar, responde esta mensagem.

**Limite conhecido, herdado do texto original, não desta versão:** a
promessa "vou te mandar o link aqui mesmo 30 min antes" não tem, hoje,
nenhum mecanismo de workflow que a cumpra — detalhe em `build-wesales.md`,
seção 5, depois da tabela de nós.

## PA-R24 — lembrete 24h antes (Pós-agendamento — R-12/seção 5)

Especificada em `build-wesales.md`, seção 5, nó 8. Primeiro dos três
lembretes — nenhum tinha texto versionado antes desta rodada (G-05, peça
2), achado ao contar os nós do Pós-agendamento com atenção. Tom de
confirmação, não de alerta: 24h de antecedência é cedo demais para soar
como cobrança.

> {{contact.first_name}}, passando para confirmar: nossa reunião com
> {{user.first_name}} é amanhã, {{appointment.start_time}}. Segue valendo? Se
> precisar remarcar, responde por aqui.

## PA-R3H — lembrete 3h antes (Pós-agendamento — R-12/seção 5)

Especificada em `build-wesales.md`, seção 5, nó 9. Mesmo motivo do
`PA-R24`: sem texto antes desta rodada. Mais curto que o de 24h — a essa
distância o lead já decidiu comparecer ou não, o lembrete é só para não
deixar a agenda esfriar.

> {{contact.first_name}}, nossa reunião com {{user.first_name}} é hoje às
> {{appointment.start_time}}, daqui a poucas horas. Te espero!

## PA-R30 — lembrete curto (Pós-agendamento — R-12/seção 5)

Especificada em `build-wesales.md`, seção 5, nó 10. O mais curto dos
quatro, de propósito — a tabela de nós já pedia "lembrete curto" desde a
versão original. Não afirma anexar o link da reunião (ver o limite
registrado em `PA-CONF` acima): confirma só o horário.

> {{contact.first_name}}, é agora — nossa reunião com {{user.first_name}}
> começa em 30 min.

## Template Meta para envio fora da janela de 24h — G-05

Descoberto em 21/09/2026 (roadmap, G-05): o WhatsApp Business API só aceita
o texto livre desta biblioteca quando o contato está dentro da janela de
atendimento de 24h (abre só quando o **cliente** escreve primeiro). Como
nenhum lead desta base jamais escreveu no WhatsApp antes de receber uma
mensagem automática, praticamente todo envio cai fora da janela — cada
código abaixo precisa de um **Template** equivalente, pré-aprovado pela
Meta no Business Manager (decisão e ação do dono, fora do alcance deste
conector; aprovação leva até 48h), para o portão de `build-wesales.md`
seção 2.6.2 ter o que enviar no ramo "fora da janela".

| Código | Template Meta | Status |
|---|---|---|
| `M1-a` | — | A submeter (peça 1 do G-05, feita) |
| `M1-b` | — | A submeter (peça 1 do G-05, feita) |
| `M2-v1` | — | A submeter (peça 1 do G-05, feita) |
| `M3-v1` | — | A submeter (peça 1 do G-05, feita) |
| `MI-0` | — | A submeter (peça 2 do G-05, feita) |
| `MI-F` | — | A submeter (peça 2 do G-05, feita) |
| `RE-1` | — | A submeter (peça 2 do G-05, feita) |
| `RE-2` | — | A submeter (peça 2 do G-05, feita) |
| `NS-1` | — | A submeter (peça 2 do G-05, feita) |
| `NS-2` | — | A submeter (peça 2 do G-05, feita) |
| `PA-CONF` | — | A submeter (peça 2 do G-05, feita) |
| `PA-R24` | — | A submeter (peça 2 do G-05, feita) |
| `PA-R3H` | — | A submeter (peça 2 do G-05, feita) |
| `PA-R30` | — | A submeter (peça 2 do G-05, feita) |

"A submeter" cobre só a guarda de janela em si (`build-wesales.md`, seções
2.6.2, 2.10, 2.12, 5 e 5.3, e os nós correspondentes de
`IMPLEMENTACAO-WORKFLOWS.md`) — a submissão de verdade no Meta Business
Manager, com o texto convertido para o formato de Template (variáveis
posicionadas no lugar dos merge fields, possível botão CTA no lugar do
Trigger Link) continua ação do dono, não executada nesta rodada. Com esta
rodada, todo código ativo da tabela "Templates ativos" acima (o `M1-v1`
substituído não conta) tem guarda de janela especificada — a lista de
pendências que o G-05 registrou em 21/09/2026 (`ROADMAP-SALES-ENGAGEMENT.md`)
está zerada.

## Como isso responde o "Pronto quando" do R-04

"Dá para dizer qual abertura teve mais resposta" sem abrir mensagem por
mensagem: a interceptação de sinal do F-01 (`build-wesales.md`, seção 2.9.3)
já grava `Sinal recebido` = `Resposta de mensagem` toda vez que o lead
responde fora do fluxo normal, via gatilho nativo `Customer Replied`. A lista
inteligente `Resposta por Template` (`build-wesales.md`, seção 8.13) cruza
esse sinal com `Template usado` — contar linhas agrupadas por código responde
a pergunta, sem campo de contagem novo e sem planilha.

**Limite conhecido:** `Sinal recebido` é um campo único, não um log — se o
mesmo contato responder a M1 e mais tarde clicar num link (sinal de M2/M3), o
valor mais recente sobrescreve o mais antigo e a resposta a M1 some do filtro
`Resposta por Template`. É o mesmo limite já registrado no F-01
(`build-wesales.md`, seção 2.9.4) para `Sinal recebido` em geral; não é
específico deste item e não compensa criar um campo por sinal só para cobrir
o caso raro de dois sinais do mesmo contato antes de qualquer classificação.

## Quando a próxima versão nascer

Edite só a tabela "Templates ativos" e adicione a seção do texto novo abaixo
das existentes — nunca troque o texto de uma seção já publicada. Atualize o
nó de envio correspondente em `build-wesales.md`, seção 2.6, para o novo
código.
