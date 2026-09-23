# Etapas 2 e 3 — campos e tags para confirmar antes de criar

**Nada aqui foi criado.** Esta é a lista que eu executo depois da auditoria e
da sua confirmação, item por item. A auditoria pode cortar linhas desta lista
(campo que já existe é reaproveitado, nunca duplicado).

## Etapa 2 — Campos personalizados (50 + 1 sugerido)

> **Onde mora a contagem.** Só este título conta campos, e só ele. Os títulos
> de seção perderam o número de propósito: eram quatro lugares para errar cada
> vez que um campo nasce, e já erraram. Quem quiser saber quantos tem numa
> seção, conta as linhas da tabela — que é a verdade, não um resumo dela.

Todos no objeto **contato**. Tipo é o `dataType` da API do GHL.

### Controle da cadência

| # | Nome | Tipo | Opções | Quem escreve |
|---|---|---|---|---|
| C-01 | Tentativa nº | NUMERICAL | — | Workflow |
| C-02 | Resultado da tentativa | SINGLE_OPTIONS | Atendeu, Caixa Postal, Não atendeu, Número errado, Pediu retorno, Não ligar, **Desqualificado** (opção nova, L-08/R-18 — falta criar na tela) | SDR |
| C-03 | WA não atendidas seguidas | NUMERICAL | — | Workflow |
| C-04 | Permissão WhatsApp | SINGLE_OPTIONS | Sim, Não, Não solicitado | IA / SDR |
| C-05 | Prioridade | NUMERICAL | 1 a 5 | Workflow |
| C-06 | Total de ligações | NUMERICAL | — | Workflow |
| C-07 | Total de conexões | NUMERICAL | — | Workflow |
| C-08 | Nota de qualificação | NUMERICAL | 0 a 100 | Workflow |
| C-09 | Tentativas telefone | NUMERICAL | — | Workflow (R-01) |
| C-10 | Tentativas WhatsApp | NUMERICAL | — | Workflow (R-01) |
| C-11 | Conexões telefone | NUMERICAL | — | Workflow (R-01) |
| C-12 | Conexões WhatsApp | NUMERICAL | — | Workflow (R-01) |
| C-13 | Sinal recebido | SINGLE_OPTIONS | Clique em link, Resposta de mensagem | Workflow (F-01) |
| C-14 | Data e hora do sinal | TEXT | `AAAA-MM-DD HH:MM` | Workflow (F-01) |
| C-15 | Reunião foi qualificada | SINGLE_OPTIONS | Sim, Não, Parcial | Closer (F-03) |
| C-16 | Motivo da desqualificação | SINGLE_OPTIONS | Sem fit, Sem budget, Timing errado, Não é decisor, Concorrente, Duplicado ou já cliente | Closer (F-03) — **e SDR (R-18)**, reaproveitado pré-reunião quando `Resultado da tentativa = Desqualificado` |
| C-17 | Data do veredito do closer | DATE | — | Workflow (F-03) |
| C-18 | Entrada em | TEXT | `AAAA-MM-DD HH:MM` | Workflow (R-02) |
| C-19 | 1ª tentativa em | TEXT | `AAAA-MM-DD HH:MM` | Workflow (R-02) |
| C-20 | Data conectado | DATE | — | Workflow (R-03) |
| C-21 | Data agendado | DATE | — | Workflow (R-03) |
| C-22 | Data compareceu | DATE | — | Workflow (R-03) |
| C-23 | Template usado | TEXT | código do template, ex. `M1-a` | Workflow (R-04) |
| C-24 | Nº de no-shows | NUMERICAL | — | Workflow (R-12) |
| C-25 | Hora da conexão | TEXT | `HH`, 00 a 23 | Workflow (F-02) |
| C-26 | Toques na semana | NUMERICAL | — | Workflow (F-04) |
| C-27 | Checkpoint — Tentativa nº | NUMERICAL | — | Workflow (F-05) |
| C-28 | Checkpoint — Data de retorno | DATE | — | Workflow (F-05) |
| C-29 | Duração da ligação | NUMERICAL | segundos | Workflow (F-06) |
| C-30 | Conexão real | SINGLE_OPTIONS | Sim, Não | Workflow (F-06) |
| C-31 | Conexões reais telefone | NUMERICAL | — | Workflow (F-06) |
| C-32 | Ligações com transcrição | NUMERICAL | — | Workflow (F-06) |

C-09 a C-12 abrem `Total de ligações`/`Total de conexões` (C-06/C-07) por
canal — sem eles não dá para responder "a T7 do telefone conecta mais que a
do WhatsApp?", que é a pergunta do R-01 do roadmap. Escritos pelo Pós-ligação
(`build-wesales.md`, seção 4, nós 2 e o ramo `Atendeu`); a lista inteligente
que os lê é a 8.6.

C-13 e C-14 alimentam a interceptação de sinal (`build-wesales.md`, seção 2.9,
F-01 do roadmap): registram que tipo de sinal furou a fila e quando, para o
SDR ver na nota do contato e para uma futura auditoria (bloco F-05) conseguir
provar que o sinal foi atendido a tempo. **Atenção de tipo:** como o campo
**Medido em 18/09/2026:** campo `DATE` do GHL guarda **só a data** — a hora é
descartada até quando se envia ISO completo pela API, e não existe tipo
DateTime para campo de contato. Por isso `Data e hora do sinal` (C-14) é
`TEXT` no formato `AAAA-MM-DD HH:MM`, e `Data de retorno` (S-01, nome real
da tela) virou par: `DATE` para filtrar e vencer tarefa, `TEXT` para a hora
combinada.

C-15 e C-16 fecham o loop do closer (`build-wesales.md`, seção 5.1, F-03 do
roadmap): o closer registra se a reunião que o SDR agendou tinha fit de
verdade, e por quê quando não teve. É o único par deste documento preenchido
por um papel que a coluna "Quem escreve" ainda não tinha: nem SDR, nem
workflow, nem IA.

C-16 ganhou um espelho fora deste documento em 22/09/2026 (F-12): quando o
valor leva a `status = lost`, o mesmo motivo passa a ser gravado também no
`Lost Reason` nativo da oportunidade — campo reservado da plataforma, por
isso não aparece nesta lista de campos personalizados. Não substitui C-16
(continua sendo o SDR/closer quem preenche, um campo só); só abre relatório
e gatilho nativos que um `SINGLE_OPTIONS` de contato nunca teria. Desenho
completo em `build-wesales.md`, seção 4.1 — **e leia a "Conferência do F-12"
no fim daquela seção antes de criar os valores na tela**: (1) `Lost Reason`
criado **nunca pode ser apagado**, então os cinco valores têm de nascer com o
texto exato de C-16 na primeira vez (`Sem fit`, `Sem budget`, `Não é decisor`,
`Concorrente`, `Duplicado ou já cliente`); (2) não está confirmado que a ação
`Update Opportunity` permita gravá-lo por workflow — há pedido aberto de
usuários dizendo que automação não referencia `Lost Reason` —, e o plano B é
escolha manual na tela de quem marca `lost`; (3) `lostReasonId` é **legível**
por API (`opportunities_search-opportunity`) e **não gravável** por este
conector, o que torna a conferência automática: oportunidade `lost` com
`lostReasonId` vazio é a divergência que o item existe para impedir.

C-17 é `DATE`, não `TEXT`: nada aqui mede minutos (diferente de C-14), só
"em que dia o closer deu o veredito", então a granularidade de dia do `DATE`
basta e evita outro par de campos como o de C-14/S-01.

C-18 e C-19 medem speed-to-lead (`build-wesales.md`, seção 2.11, R-02 do
roadmap): `Entrada em` grava quando o lead entra em `Em cadência` (nó 0.6 da
Cadência 12x30), `1ª tentativa em` grava quando a T1 dispara de verdade (nó
5c, só na primeira tentativa). Mesmo motivo de C-14: `TEXT` porque a métrica
é em minutos e `DATE` descarta a hora.

C-20 a C-22 fecham o funil por marco (`build-wesales.md`, seções 4, 5 e 5.2,
R-03 do roadmap): cada campo grava a data em que a oportunidade cruzou aquele
marco pela primeira vez — `Data conectado` no Pós-ligação, `Data agendado` no
Pós-agendamento, `Data compareceu` no comparecimento confirmado pelo
calendário. Pesquisado antes de desenhar: o GHL tem filtro nativo `Last Stage
Change Date`, mas ele só reflete a **etapa atual** — assim que o lead avança
para a etapa seguinte, o dado de quando ele passou pela etapa anterior se
perde, e o funil do mês subconta quem já avançou. Um carimbo próprio por
marco sobrevive ao avanço. `DATE` basta aqui (diferente de C-14/C-18/C-19):
a métrica é contagem por mês, não velocidade em minutos, e o filtro relativo
"neste mês" já existe nativamente para campo `DATE`. O quarto marco do
funil, "entraram", não ganha campo novo: usa o filtro nativo `Data de
criação` da oportunidade, que não muda quando o lead avança — o mesmo
problema do `Last Stage Change Date` não existe aqui porque criação é
imutável.

C-23 fecha a biblioteca de mensagens versionada (`build-wesales.md`, seção
2.6, R-04 do roadmap): grava o código do template que acabou de sair (ex.:
`M1-a`) toda vez que M1, M2 ou M3 dispara. **`TEXT`, não `SINGLE_OPTIONS`,
de propósito:** uma lista de opções fixa exige reabrir o campo na tela toda
vez que nasce uma versão nova — e o R-05 (teste A/B da M1, seção 2.6.1 do
`build-wesales.md`) já criou `M1-a`/`M1-b`, escritos pelos dois caminhos do
Split sem tocar no campo. `TEXT` deixa o workflow escrever qualquer código
novo sem depender de edição manual do campo; o custo é não ter validação de
valor digitado, que aqui é baixo porque só o workflow escreve neste campo,
nunca o SDR. Textos e códigos completos, versionados, ficam em
`biblioteca-mensagens.md`.

C-24 fecha o handoff de no-show (`build-wesales.md`, seções 5.3/5.4, R-12 do
roadmap): conta quantos no-shows seguidos o lead acumulou desde o último
comparecimento de verdade — a seção 5.2 zera este campo ao confirmar
`Showed`, e a seção 5.3 o incrementa a cada `No Show`, descartando a
oportunidade automaticamente a partir do 2º seguido (proteção de agenda do
closer). **`NUMERICAL`, não uma tag:** a lista 8.17 (`build-wesales.md`)
filtra direto pelo valor do campo, mesmo raciocínio já usado em C-06/C-07 —
uma tag só valeria a pena se algum portão precisasse checar "presente/
ausente" sem importar a contagem, o que não é o caso aqui.

C-26 fecha o teto de toques por semana (`build-wesales.md`, seção 2.19, F-04
do roadmap): conta, numa janela móvel de 7 dias corridos, quantos toques
(tarefa de ligação criada ou mensagem automática enviada) o lead recebeu —
somado por um nó `Math +1` a cada toque e descontado por um `Math -1` 7 dias
depois pelo workflow "Contador de Toques". `NUMERICAL`, mesmo raciocínio já
usado em C-06/C-07/C-09 a C-12: é contado por `Math`, não lido por SDR nem
por IA, então uma tag "presente/ausente" não bastaria — o portão de
frequência (seção 2.4, nó 2.5c) compara contra um número, não contra
presença.

C-27 fecha a peça 3 do Monitor de Saúde (`build-wesales.md`, seção 2.22,
F-05 do roadmap): guarda o valor de `Tentativa nº` (C-01) no instante em que
uma rodada nova começa, para o próprio workflow comparar 14 dias depois se a
régua avançou. **`NUMERICAL`, campo de uso exclusivo deste workflow:**
diferente de C-26 (vários toques por semana, escritas frequentes e
concorrentes), este campo é escrito no máximo três vezes na vida de um lead
(entrada inicial em `CONECTAR`, handoff do fim da Cadência Inbound,
reativação do Reengajamento), sempre bem espaçadas — não herda o risco de
"contador com dois donos" que C-26 e outros campos deste documento já
evitaram com cuidado, porque nenhum outro nó do projeto lê ou escreve nele.

C-28 fecha a peça 6 do Monitor de Saúde (`build-wesales.md`, seção 2.24,
F-05 do roadmap): guarda o valor de `Data de retorno` no instante em que o
workflow "Retorno Vencido" dispara, para comparar contra o valor ao vivo no
dia do vencimento e saber se a promessa foi renovada enquanto o relógio
esperava. Mesmo raciocínio de C-27: `DATE` (não `TEXT` — aqui não se mede
minutos, só qual dia foi prometido, granularidade que o par C-14/S-01 já
usa para o mesmo tipo de campo), campo de uso exclusivo deste workflow,
escrito no máximo poucas vezes na vida de um lead e sempre espaçado por
dias — não herda o risco de "contador com dois donos".

C-29 e C-30 fecham a peça 1 do F-06 (`build-wesales.md`, seção 2.27):
`Duração da ligação` (`NUMERICAL`, segundos) grava o dado que o gatilho
nativo `Transcript Generated` carrega para toda chamada de LC Phone;
`Conexão real` (`SINGLE_OPTIONS`: Sim, Não) é o veredito automático — mais
de 60s conta, menos não conta, mesmo que o SDR tenha marcado `Atendeu`. Os
dois convivem com `Conexões telefone`/`Conexões WhatsApp`/`Total de
conexões` (C-06/C-07/C-11/C-12) em vez de substituí-los: aqueles vêm do
julgamento do SDR no Pós-ligação e continuam alimentando o relatório atual.

C-31 fecha a peça 2 do F-06 (`build-wesales.md`, seção 2.27, nó 6): conta,
cumulativamente, quantas chamadas de telefone bateram o limiar dos 60s —
`NUMERICAL`, incrementado por `Math +1` a cada `Conexão real = Sim`, nunca
sobrescrito. **Por que não basta apontar a lista/o dashboard direto para
`Conexão real` (o que a peça 1 tinha deixado como plano):** `Conexão real`
é um veredito por tentativa, sobrescrito a cada chamada (e sujeito ao
próprio estado vencido que a peça 1 já registrou — um `Sim` da T3 sobrevive
a T4-T8 sem transcrição) — serve para o portão do "Pronto quando" que olha
uma tentativa por vez, não para uma taxa acumulada. Widget de Custom
Metrics (seção 2.17) só soma campo `NUMERICAL`/`MONETARY` (achado já
registrado ali) — somar um `SINGLE_OPTIONS` não é operação que a fórmula
aceite, e contar contatos com `Conexão real = Sim` (recurso mais novo de
filtro por metric-level, checado nesta rodada) contaria pessoas no estado
atual, não chamadas ao longo do tempo, misturando unidade diferente da do
`Tentativas telefone` (C-09) que forma o outro lado da razão. C-31 escreve
uma vez por chamada e nunca é sobrescrito — mesmo padrão de C-06/C-07/C-11/
C-12, e a mesma razão por que eles existem: contador cumulativo, não
estado. Escrito só pelo workflow do F-06 — não herda risco de "contador com
dois donos".

C-32 foi acrescentado na conferência da mesma peça (`build-wesales.md`, seção
2.27, "Conferência da peça 2", nó 2b) porque C-31 e C-09 são cumulativos mas
**não são da mesma população**: C-31 só conta chamada de LC Phone que gerou
transcrição; C-09 conta toda tentativa que o SDR classificou. Ligação pelo
celular do SDR, período com transcrição desligada e ring sem transcrição a
gerar entram no denominador e nunca no numerador — a razão fica enviesada
para baixo de forma sistemática, num widget chamado "Taxa de Conexão Real".
C-32 é incrementado no nó 2b, que roda para **toda** transcrição, antes do
teste dos 60s: passa a ser o denominador da mesma população ("das chamadas
que dá para medir, quantas foram conversa"). De brinde, `C-32 ÷ C-09` mede a
**cobertura da instrumentação** — a distância entre dois contadores que
deveriam andar juntos, o mesmo método de contador vizinho que este projeto já
usou para achar nó silencioso. Escrito só pelo workflow do F-06.

**Corrigido em 22/09/2026, dois pontos** (`build-wesales.md`, "Conferência do
F-06"): (1) os dois campos só se preenchem se **a gravação de chamada estiver
habilitada** — transcrição exige gravação, e sem transcrição o workflow nunca
dispara; ligar isto implica aviso de gravação por LGPD no início da ligação
(`script-de-ligacao.md`, seção 2) e custo de add-on por minuto gravado. (2)
`Conexão real` **precisa de um reset**: chamada não atendida pode não gerar
transcrição nenhuma, e sem reset um `Sim` da T3 sobrevive a T4-T8, fazendo o
campo significar "alguma tentativa foi conversa" em vez de "esta foi". O
reset (`= vazio`) vai no nó que cria a tarefa de cada tentativa (seções 2.4 e
2.10), **antes** da ligação — não no Pós-ligação, que disputaria o campo com o
workflow novo, já que a transcrição chega minutos depois e o SDR classifica na
hora. Com o reset nesse ponto não há "dois donos"; sem ele, há estado
vencido.

C-25 fecha o horário aprendido por segmento (`build-wesales.md`, seção 2.18,
F-02 do roadmap): grava só a **hora** (não o carimbo completo) em que o lead
`Atendeu`, para cruzar com `Segmento` (Q-01) numa lista e enxergar se um
segmento conecta mais de manhã e outro à tarde. **`TEXT` de duas casas
(`HH`), não `NUMERICAL` nem o carimbo `AAAA-MM-DD HH:MM` que C-14/C-18/C-19
usam:** aqui ninguém mede minutos entre dois eventos (o que pediria
`TEXT` completo, R-02) nem soma o valor (o que pediria `NUMERICAL`, como
C-06 a C-12) — o campo só precisa ser lido e comparado por um humano numa
lista, por segmento, e uma string de duas casas evita o risco que o próprio
projeto já registrou com `Conexões telefone` (C-11): um `NUMERICAL` criado
errado na tela quebra a ação `Math` sem avisar; um `TEXT` não tem esse jeito
de quebrar porque nenhum nó soma nele.

**R-10 (distribuição de leads) não abre campo novo.** O roadmap sugeria um
campo `SDR responsável`; a especificação (`build-wesales.md`, seção 2.14)
reaproveita o campo nativo `Assigned User` (dono do contato), que o GHL já
expõe em filtro de Smart List e em ação de workflow (`Assign to User`) — um
campo personalizado espelhando a mesma informação divergiria na primeira
reatribuição feita direto na tela, o mesmo problema de "campo com dois
donos" que este documento já evita desde C-01 a C-23.

**R-13 (higiene de base) não abre campo nem tag nova.** O portão 0.0/0.0b
das seções 2.3 e 2.10 e o workflow opcional da seção 2.16 (`build-wesales.md`)
reaproveitam `telefone-invalido` (T-09, já existente) e o campo nativo
`Phone` — o mesmo raciocínio de "não duplicar o que o GHL já expõe" do
parágrafo do R-10 acima, agora aplicado a tag em vez de campo: a tag já
significava "não dá para ligar nesse número", e cobrir "não tem número
nenhum" com a mesma tag é extensão de significado, não invenção de um
segundo estado.

### Qualificação — BANT + diagnóstico

| # | Nome | Tipo | Opções |
|---|---|---|---|
| Q-01 | Segmento | TEXT | livre — **resolve a L-02**: a tela criou como texto livre em vez de esperar a lista fechada de segmentos |
| Q-02 | Site | TEXT (URL) | — |
| Q-03 | Instagram | TEXT | — |
| Q-04 | Clientes novos por mês | SINGLE_OPTIONS | 10, 11-30, 31-100, +101 |
| Q-05 | Investe em anúncios | SINGLE_OPTIONS | Sim, Já investiu e parou, Nunca |
| Q-06 | Investimento mensal em anúncios | SINGLE_OPTIONS | Até 1k, 1k a 5k, 5k a 10k, Acima de 10k |
| Q-07 | Plataformas de anúncio | SINGLE_OPTIONS **— deveria ser MULTIPLE_OPTIONS** | Meta, Google, Tiktok, Outros — tipo errado ainda não corrigido na tela, ver `CONFERENCIA-CAMPOS.md` Tabela A |
| Q-08 | Já teve agência? | SINGLE_OPTIONS | Tem hoje, Já teve, Nunca teve |
| Q-09 | Experiência com agência | TEXT | — |
| Q-10 | Tem time comercial | SINGLE_OPTIONS | Só dono, 1-5, 6-10, +10 |
| Q-11 | Quem atende os leads | SINGLE_OPTIONS | Dono, Vendedor, SDR, Ninguém fixo |
| Q-12 | Usa CRM | SINGLE_OPTIONS | Sim, Não |
| Q-13 | Canal principal de venda | SINGLE_OPTIONS | WhatsApp, Telefone, Loja, Online |
| Q-14 | Budget | SINGLE_OPTIONS | Tem, Precisa aprovar, Não tem |
| Q-15 | Decisor | SINGLE_OPTIONS | Sim, Influencia, Não decide |
| Q-16 | Dor principal | TEXT | — |
| Q-17 | Prazo | SINGLE_OPTIONS | Pra ontem, Espera 30 dias, Este ano, Sem prazo |
| Q-18 | Qualificação | SINGLE_OPTIONS | SDR, IA Whatsapp, Vendedor |

Observações de tipo:
- **Q-02 Site**: o GHL não tem `dataType` URL. Vai como TEXT com placeholder
  `https://`. Se preferir validação, o campo do formulário pode ser marcado
  como website na tela.
- **Q-09 e Q-16**: resolvido — quem montou na tela criou os dois como
  `TEXT` (não `LARGE_TEXT`, que eu tinha sugerido). Funciona, só corta em
  uma linha; a coluna acima já reflete o tipo real.

**Reconciliado com a tela em 19/09/2026** (`CONFERENCIA-CAMPOS.md`, Tabelas
B/C/D): as duas tabelas acima (Controle da cadência e Qualificação) já
mostram nome, tipo e opção **como `locations_get-custom-fields` devolve
hoje**, não como foram sugeridos na primeira rodada. A régua de nota
(`build-wesales.md`, seção 9.1) foi corrigida junto — é quem realmente
sofre quando o rótulo muda, porque um `If/Else` que compara contra um
rótulo que não existe mais não casa nunca, e a nota erra em silêncio.
Nove campos tiveram nome, opção ou tipo diferente do sugerido (Q-01, Q-04,
Q-06, Q-08, Q-10, Q-12, Q-15, Q-17, Q-18); só `Q-07 Plataformas de anúncio`
continua **errado de verdade** (linha do campo, acima): nasceu
`SINGLE_OPTIONS` em vez de `MULTIPLE_OPTIONS`, o único caso desta lista com
perda de função (lead que anuncia em duas plataformas só registra uma) —
pendente de correção manual na tela, detalhe em `CONFERENCIA-CAMPOS.md`
Tabela A.

### Sugerido por mim — não crio sem seu ok

| # | Nome | Tipo | Por que |
|---|---|---|---|
| S-01 | Data do retorno | DATE + `Hora do retorno` (TEXT) — **os dois já existem na tela desde 21/09/2026 23:18** | São dois campos porque `DATE` no GHL descarta a hora. Nomes reais da tela: `Data de retorno` (sem o "o", `DATE`, `contact.data_de_retorno`) e `Hora do retorno` (`TEXT`, placeholder `HH:MM`, `contact.hora_do_retorno`). **L-01 fechada por inteiro em 22/09/2026:** a fiação que faltava (tarefa `[RETORNO]` citando `{{contact.hora_do_retorno}}` no corpo, `build-wesales.md` seção 4 nó 4b, e a lista `Retornos` ordenando por `Data de retorno`/`Hora do retorno`, seção 8.4) está especificada — falta só a montagem manual na tela, mesma fila dos demais nós ainda não publicados |

**Três campos fora desta lista, criados sozinhos pela tela ao montar o
formulário** (`Urgência`, `Necessidade`, ambos `TEXT`, e `Empresa`, `TEXT`)
— `Empresa` já foi absorvido pela especificação (`build-wesales.md`, seções
5 e 7.2, e a seção 8 abre avisando qual coluna é a personalizada), mas
`Urgência` e `Necessidade` seguem duplicando `Prazo` (Q-17) e `Dor
principal` (Q-16) sem que ninguém tenha decidido qual dos dois pares fica.
Detalhe completo, e por que não contam no título acima (regra da contagem
única no topo deste arquivo), em `CONFERENCIA-CAMPOS.md`, Tabela F.

**Um quarto campo fora desta lista, criado pela API interna em 23/09/2026:**
`Canal que conectou` (`SINGLE_OPTIONS`: Ligação WhatsApp, Ligação normal,
Mensagem — `contact.canal_que_conectou`, id `TxJmoWdkA8rTqC1uEsMW`,
confirmado por `locations_get-custom-fields` nesta rodada, `dateAdded`
2026-09-23T01:06Z). ⚠️ **Medido em 23/09 03:50: nenhum workflow escreve nele.**
O id não aparece em nenhum dos 33 dumps, e a D10 do `PLANO-MULTICANAL.md` diz
que ele deve ser "marcado junto com o resultado" — quem marca o resultado é o
`Pós-ligação v2`, publicado, e ele não grava este campo. Logo a pergunta que o
multicanal existe para responder (*qual canal conectou?*) não vai ter resposta.
Correção e onde encaixá-la: seção 2.34 do `build-wesales.md`. Não nasceu deste documento nem de `build-wesales.md`:
é o D10/E3 de `wesales/PLANO-MULTICANAL.md`, o plano do dono de 22/09/2026
que reformula a cadência (ver nota no topo de `ROADMAP-SALES-ENGAGEMENT.md`).
Registro, não aprovação — o campo já existe na tela, criado por fora deste
conector; nenhum nó de `build-wesales.md` o lê ou escreve ainda, porque
`build-wesales.md` segue descrevendo o desenho anterior ao `PLANO-
MULTICANAL.md`.

## Etapa 3 — Tags (21 numeradas, seis pendentes de aprovação — e 10 na conta fora da numeração)

As 21 são as tags **deste projeto**: T-01 a T-15 criadas, T-16 a T-21 esperando
`[x]` no `APROVADO.md`. A conta tem outras **10**, criadas por ação do dono e
registradas abaixo nas linhas `—` (`teste-regua`, `fechar-horario`,
`cadencia-12x30-p2`, `teste-12x30` e as 8 do Espelho de Etapa) — ficam fora da
numeração de propósito, para o `T-nn` continuar significando "tag que a rotina
só cria com aprovação". **Total na conta hoje: 25.** Dois números diferentes
porque contam coisas diferentes; quem for conferir na tela vê 25.

| # | Tag | Função na máquina |
|---|---|---|
| T-01 | `fila-quente` | Lista inteligente Fila Quente (Prioridade ≥ 4) |
| T-02 | `fila-tel` | Tentativa de telefone liberada hoje |
| T-03 | `fila-wa` | Tentativa de ligação por WhatsApp liberada hoje |
| T-04 | `fila-linkedin` | Reserva — hoje sem canal na cadência (lacuna L-03) |
| T-05 | `conectado-hoje` | Tira o lead das filas do dia após conexão — **e hoje isso é falso: nada remove esta tag.** Nenhum dos 26 dumps tem `remove_contact_tag` com ela e nenhum documento especifica reset. Ela está na família **Estado** ("sobrevive à saída de cadência") em `IMPLEMENTACAO-WORKFLOWS.md`, o que contradiz o "do dia" desta linha. Até 22/09 a contradição era inofensiva porque o ramo `Atendeu` tirava a oportunidade de `CONECTAR` e as filas 8.2/8.3 também exigem `etapa = CONECTAR`; com `1d04af2` o `Atendeu` **fica** em `CONECTAR` e esta tag passa a ser a única cláusula que exclui o lead — para sempre. Achado e saídas na seção 2.31 do `build-wesales.md` (F-16). Medido em 23/09: 2 contatos, os dois de teste do projeto |
| T-06 | `nao-perturbe` | Portão de segurança em toda tentativa |
| T-07 | `limpar-tarefas` | Fila da rotina horária de manutenção |
| T-08 | `nutricao-90d` | Saída branda, volta depois |
| T-09 | `telefone-invalido` | Portão das tentativas de telefone |
| T-10 | `cad-inbound` | Origem: inbound |
| T-11 | `cad-outbound` | Origem: outbound |
| T-12 | `atraso-1a-tentativa` | Alerta de speed-to-lead (R-02/R-07): aplicada pelo workflow da seção 2.11 do `build-wesales.md` quando o lead passa o tempo daquele relógio (varia por origem, seção 2.11 tem o valor certo) em `Em cadência` sem a T1 disparar; filtra a lista 8.8 |
| T-13 | `reengajamento-ativo` | Reengajamento 90 dias (R-08): aplicada pelo workflow da seção 2.12 do `build-wesales.md` enquanto o lead reativado roda a régua TR1-TR4; blinda o gatilho da Cadência 12x30 (seção 2.1) contra entrada dupla e filtra a lista 8.14 |
| T-14 | `pausado` | Regras de pausa (R-09): aplicada manualmente pelo SDR para represar as tentativas de **um** lead sem ser opt-out; checada no nó 2.5 (seção 2.4) e 1.5 (seção 2.10) do `build-wesales.md`, limpa pelo Mestre de saída (seção 3) e filtra a lista 8.15 |
| T-15 | `toque` | Teto de toques por semana (F-04): pulso, não estado — todo nó que cria tarefa de ligação ou manda mensagem automática aplica esta tag, o workflow "Contador de Toques" (seção 2.19 do `build-wesales.md`) reage a ela, soma em `Toques na semana` (C-26) e a remove no mesmo instante; nunca fica presente por mais que alguns segundos |
| — | `teste-regua` | **Tag nº 16, criada pelo dono na tela em 22/09/2026 ~12:38**, fora deste documento e de `APROVADO.md`. Marcador de teste dele, aplicada no `Teste Atendeu`. **Não é órfã e não entra em lista de limpeza nenhuma** — registrada aqui só para nenhuma rodada futura "descobrir" e tentar consertar. Regra: tag na tela que não está em documento é do dono até prova em contrário; o caminho é perguntar, nunca remover | Dono (teste) |
| — | `fechar-horario` | **Tag nº 17, criada por ação do dono no commit `1d04af2` (23/09/2026)**, fora de `APROVADO.md` — não é criação minha e não estou desfazendo. Estado novo "conectou, está fechando o horário da reunião de diagnóstico": **aplicada** pelo `Pós-ligação v2` (publicado, nós 13/26/77/86/97, junto com `conectado-hoje`) e **removida só** pelo `Fechar Horário` (publicado no `23db864` — nasceu em rascunho e a janela fechou limpa, 0 contatos com a tag; seção 2.31.1). **O que continua aberto:** a remoção mora nos 4 nós de saída do `Fechar Horário` (36/38/39/40) e o caminho de quem **agenda** não passa por eles — o `Pós-agendamento v2` arranca o contato do workflow no nó 4, e `remove_from_workflow` não executa as saídas do alvo. Logo todo lead que agenda fica com esta tag para sempre, e ela é a única da conta **sem** segunda rede (o Mestre de saída não a limpa). Correção: um `Remove Tag fechar-horario` no nó 4 do `Pós-agendamento v2`. Detalhe na seção 2.31.2 do `build-wesales.md` | Dono (`1d04af2`) |
| — | `etapa-novo-lead`, `etapa-conectar`, `etapa-reuniao`, `etapa-negociar`, `etapa-formalizar`, `status-nutricao`, `status-perdido`, `status-ganho` | **Tags 18 a 25, criadas por ação do dono no commit `61eb167` (23/09/2026)**, fora de `APROVADO.md` — não são criação minha. São o **Espelho de Etapa**: a etapa/status da oportunidade virando tag no contato, porque condição `Pipeline stage is …` lê vazio em workflow cujo gatilho não é oportunidade (achado do dono, medido no registro de execução da `ZZ TESTE 12X30`). Exatamente uma delas por contato. O `Espelho de Etapa` está **publicado** (v4, 36 nós) e os 11 consumidores também — a ordem está certa. (Cheguei a registrar que ele estava em rascunho; era leitura de dump exportado 4 segundos antes da publicação, e retirei o achado — seção 2.32 do `build-wesales.md`.) Continua em aberto, e nenhum dump responde: **o gatilho de oportunidade etiqueta o acervo ou só mudança futura?** Se for só futura, as 45 oportunidades paradas em `NOVO LEAD` não recebem `etapa-novo-lead` | Dono (`61eb167`) |
| — | `cadencia-12x30-p2`, `teste-12x30` | Tags de controle e de teste da divisão da 12x30 em duas partes, criadas por ação do dono em 23/09. `cadencia-12x30-p2` marca quem está na segunda metade da régua; `teste-12x30` é marcador de teste dele. Registradas aqui para nenhuma rodada futura "descobrir" e tentar consertar | Dono |
| T-16 | `novo-lead-estagnado` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.20 do `build-wesales.md`): aplicada pelo workflow "Lead Esquecido em NOVO LEAD" quando a oportunidade passa 24h em `NOVO LEAD` sem ser promovida nem descartada; limpa incondicionalmente pelo nó 0 novo do Mestre de saída (seção 3) e filtra a lista 8.20 |
| T-17 | `fila-travada` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.21 do `build-wesales.md`): aplicada pelo workflow "Fila Travada" quando `fila-tel`/`fila-wa` segue presente depois do fim do dia em que foi aplicada (sinal de que o nó 9 do bloco padrão, seção 2.4, não rodou); limpa pelo próprio workflow (nó 0, na tentativa seguinte) e pelo nó 4 do Mestre de saída (seção 3, quando o lead sai de cadência de verdade) e filtra a lista 8.21 |
| T-18 | `conectar-estagnado` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.22 do `build-wesales.md`): aplicada pelo workflow "Cadência Sem Avanço" quando a oportunidade segue em `CONECTAR`/`open` sem nenhuma tentativa nova em 14 dias corridos (sinal de cadência realmente parada, não só uma tentativa travada — diferença explicada na seção 2.22); limpa pelo nó 4 do Mestre de saída (seção 3, quando o lead sai de cadência de verdade) e filtra a lista 8.22 |
| T-19 | `agendar-estagnado` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.23 do `build-wesales.md`): aplicada pelo workflow "AGENDAR Estagnado" quando a oportunidade passa 24h em `AGENDAR` sem virar reunião marcada nem sair por outro caminho (o SDR atendeu e não fechou o loop); limpa pelo nó 0 do Mestre de saída (seção 3, incondicional — mesmo tratamento de `novo-lead-estagnado`, por causa da lacuna L-08) e filtra a lista 8.23 |
| T-20 | `retorno-vencido` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.24 do `build-wesales.md`): aplicada pelo workflow "Retorno Vencido" quando `Data de retorno` (S-01) passa sem o SDR reclassificar `Resultado da tentativa`; limpa pelo nó 3c novo do Pós-ligação (seção 4, incondicional, a cada resultado novo) e, como rede de segurança, pelo nó 4 do Mestre de saída (seção 3); filtra a lista 8.24 |
| T-21 | `negociacao-estagnada` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação, extensão à negociação (F-13, seção 2.28 do `build-wesales.md`): aplicada pelo workflow "Negociação Estagnada" quando o closer marca `Reunião foi qualificada` = `Sim` e a oportunidade passa 3 dias corridos em `NEGOCIAR`/`open` sem virar `won` nem `lost`; limpa pelo nó 4 do Mestre de saída (seção 3, quando o lead sai de `NEGOCIAR` de verdade) |

Todas em minúsculas com hífen. O GHL normaliza tags para minúsculas, então
`Fila-Quente` e `fila-quente` são a mesma tag — o que ajuda a não duplicar.

**Executado em 18/09/2026 (as 14 primeiras) e 19/09/2026 (T-15).** Todas
saíram por `contacts_add-tags` sobre o mesmo contato de estrutura (`ZZ
TESTE ESTRUTURA`, `c5r3ZxiAd8T5adL1Bt6j`): as 11 originais numa chamada, as
T-12/13/14 numa segunda chamada no mesmo dia, e T-15 (`toque`, nascida do
F-04) numa terceira chamada no dia seguinte — cada uma com sua própria
linha de aprovação em `APROVADO.md`, porque cada uma nasceu numa rodada de
roadmap posterior às 11 originais. **T-16 (`novo-lead-estagnado`, nascida
do F-05 em 21/09/2026) ainda não saiu por API** — nasce `[ ]` em
`APROVADO.md`, não `[x]`: a lição do incidente de 19/09/2026 com a T-15
(a própria rotina escrevendo o próprio `[x]` não é aprovação, é a rotina se
autorizando) é para ficar, e vale para toda tag nova a partir de agora, não
só para aquela. **T-17 (`fila-travada`, nascida do F-05 peça 2 nesta
rodada) segue a mesma regra desde o nascimento** — nasce `[ ]`, não `[x]`.
**T-18 (`conectar-estagnado`, nascida do F-05 peça 3), T-19
(`agendar-estagnado`, nascida do F-05 peça 5) e T-20 (`retorno-vencido`,
nascida do F-05 peça 6) idem — nenhuma das três saiu por API ainda.**

## O que eu preciso de você para executar

**L-02, S-01 (metade) e Q-09/Q-16 já se resolveram sozinhos** — quem montou
os campos na tela decidiu por você: `Segmento` virou `TEXT` livre em vez de
esperar a lista fechada (fecha a L-02), `Q-09`/`Q-16` viraram `TEXT`, e a
metade `DATE` de `S-01` (`Data de retorno`) já existe. Não são mais
perguntas em aberto.

**S-01 fechou por inteiro em 21/09/2026 23:18**, junto com mais quatro campos
que a tela criou na mesma leva (C-25, C-26, C-27, C-28 — total de 51 campos na
subconta, detalhe e `fieldKey` reais em `CONFERENCIA-CAMPOS.md`, Tabela K).
**Não recrie `Hora do retorno`:** ele existe, com o placeholder `HH:MM` da
especificação.

Ainda em aberto:

1. **`Plataformas de anúncio`** — nasceu `SINGLE_OPTIONS`, precisa virar
   `MULTIPLE_OPTIONS` (campo novo, o antigo fica parado — regra 1 do
   briefing proíbe excluir).
2. **`Urgência` e `Necessidade`** — a tela criou os dois sozinha, duplicando
   `Prazo` e `Dor principal`. **A metade `Urgência`/`Prazo` já não bloqueia
   nada** (G-04, `ROADMAP-SALES-ENGAGEMENT.md`): o Pós-agendamento v2, no ar
   desde 22/09/2026, lê `Urgência` como reserva quando `Prazo` vem vazio, com
   a mesma pontuação — nenhuma decisão de formulário foi necessária para
   isso. `Necessidade`/`Dor principal` seguem duplicados sem decisão (nenhum
   dos dois entra na régua de nota, então não é urgente); decidir se o
   formulário aponta para os campos que já existem (recomendo) ou se os dois
   novos ganham função própria continua em aberto só por organização, não
   por pontuação errada.

Já respondido: a subconta é `1D53YTI9C7oIMBavcQxV` e a permissão de criar
veio em 18/09/2026 ("tem todas as permissões") — é o que liberou a Etapa 3,
já entregue. A Etapa 2 não depende mais de resposta, e sim de ferramenta:
campo personalizado **tem** endpoint de criação na API oficial da
HighLevel (`POST /locations/{locationId}/customFields` — confirmado lendo
o spec oficial em 18/09/2026, `APRENDIZADOS-CRM.md`), só o conector `GHL
CRM` conectado nesta sessão não a implementa. Até isso mudar (outro
conector, ou este ganhar a ferramenta), a tabela acima é para copiar em
Configurações → Campos personalizados, na tela.
