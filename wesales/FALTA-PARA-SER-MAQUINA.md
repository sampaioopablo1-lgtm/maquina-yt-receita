# O que falta para o CRM ser uma máquina de vendas

Medido em 27/09/2026 na subconta `1D53YTI9C7oIMBavcQxV`, não copiado de documento
anterior. Onde o número apareceu de leitura ao vivo, ele está aqui com o que foi lido.

**Nome sem data de propósito:** este arquivo é para ser atualizado no lugar. Um
`FALTA-27-09.md` viraria arqueologia em três dias.

## A frase de contexto

A máquina está **construída e publicada** — 33 dos 36 workflows em `published`, 56
campos, 28 tags, 5 etapas, as duas cadências inscritas e paradas esperando a janela
abrir. O que falta não é construção: é **quem é o dono do lead, de onde vem o lead
novo, e três decisões suas.** É a diferença entre "workflow publicado" e "operação
funcionando".

## 0. Fora do CRM, e manda em tudo: a conta de anúncio está `UNSETTLED`

Conta **"O Próximo Cliente"**, `ad_account_id` `1695865631502778`. A API devolve
`account_status: UNSETTLED`, `is_queryable: false`, `has_payment_method: true`.
`UNSETTLED` na Meta é saldo em aberto que não foi cobrado, e conta nesse estado **não
entrega anúncio**.

Sem entrada de lead, tudo o que está abaixo é enfeite: a máquina fica perfeita e vazia.
O plano de 10 leads/dia — que sustenta a conta das 100 tarefas — não começa.

**Não é investigável daqui** (`is_queryable: false` fecha a API). É conferência de
cobrança no Gerenciador de Anúncios, do seu lado. **Este é o item mais caro da lista, e
é o único que não tem nada a ver com CRM.**

## 1. Ninguém é dono de 36 dos 39 leads em `CONECTAR` — inclusive os 5 de terça

Medido agora, em `opportunities_search-opportunity`:

| etapa | oportunidades abertas | com dono |
|---|---|---|
| `CONECTAR` | 39 | **3** |
| `NOVO LEAD` | 2 | 2 |
| `NEGOCIAR` | 2 | 2 |

E nos contatos: **48 de 64 sem `assignedTo`**; os 16 restantes todos no mesmo usuário
(`JdvhvOTEBTvUyRi0BXU8`).

Conferi um por um os cinco leads que a máquina vai tocar na terça — o lote 1 que passa
no portão MI-0. **Os cinco estão sem dono:**

    Gerson De Souza Pia    dono=NENHUM
    Ana Ruth               dono=NENHUM
    Ricardo                dono=NENHUM
    Andreia                dono=NENHUM
    Andre                  dono=NENHUM

**Por que isso é o item número 1 dentro do CRM:** a máquina cria tarefa, e tarefa sem
destinatário não aparece na fila de ninguém. O SDR abre o CRM na terça, olha "minhas
tarefas" e vê vazio — enquanto as tarefas existem, órfãs. É o R-10 do roadmap, que
estava registrado como "lead novo nasce com `assignedTo: null`" e agora tem número.

**Decisão sua, curta:** quem é o SDR? Com o nome, a distribuição vira escrita em lote
(a API pública escreve `assignedTo`) e o lead novo passa a nascer com dono.

## 2. `Reunião Cancelada` está pronto e em `draft`

Workflow completo, **10 nós**, gatilho `appointment.status == cancelled` no calendário
`3uNQFjCEDe7b4gKZJuOZ`. Ele tira o lead dos lembretes e do pós-agendamento, manda
WhatsApp oferecendo outro horário, cria tarefa de remarcar e escreve nota. Respeita
`nao-perturbe` no ramo `NÃO`.

**Hoje, se o lead cancelar:** os lembretes continuam chegando para uma reunião que não
existe, e ninguém é avisado de remarcar. É o buraco mais barato de fechar da lista — o
trabalho já está feito, falta publicar.

Os outros dois `draft` (`Lembretes da Reunião` e `v2`) **não são lacuna**: foram
substituídos pelo `v3`, que está publicado. Corretamente parados.

## 3. Pastas de campo — o botão está pronto, sobram 27 arrastos

Action `wesales-pastas.yml`, `Run workflow` com `criar: true`. Ela renomeia a pasta
grande para `5 · NÃO MEXER — a máquina escreve` (29 dos 30 campos da máquina já estão
lá, então não se arrastam) e cria as outras quatro. Depois são **27 arrastos** na tela,
na ordem que o próprio job imprime.

A pasta 1 tem **3 campos** e já limpa o dia da SDR. Se parar nela, valeu.

Detalhe em §4 do `USABILIDADE.md`, com a medição que refez o mapa.

## 4. G-04 — a nota de qualificação nasce zerada no Bloco B para todo lead do Meta

24 de 27 valores gravados em `Investimento mensal em anúncios` não existem na picklist
do campo, porque o formulário do Meta escreve texto livre. O Bloco B da §9.1 vale 25
pontos e não pontua nenhum deles.

Duas opções, **recomendo a B**:

- **A** — arrumar a picklist e o mapeamento nos formulários. São **oito** formulários de
  Lead Ads: trabalho de tela oito vezes, e todo formulário novo nasce errado de novo.
- **B** — a §9.1 passa a ler `Urgência`/`Necessidade` por `Contains`. Um conserto, e
  formulário novo já nasce certo.

**A medição de hoje reforça a B sem eu ter ido buscar isso:** contando preenchimento
para refazer as pastas, os três únicos campos que chegam com o lead são `Urgência`
(40/64), `Necessidade` (34/64) e `Investimento mensal` (32/64). A B lê os dois
primeiros — são os campos mais preenchidos da conta depois dos que a máquina
inicializa. A B não aposta em campo frágil.

Sob a B, o `patch_picklist_investimento.py` deixa de existir.

## 4-BIS. O mapeamento dos formulários do Meta está incompleto — e é dado pago sendo descartado

**Levantado pelo dono**, e medido depois: *"tem campos, pelo formulário nativo da Meta
associado ao CRM, que podem correlacionar com o CRM."*

Cruzei o `mediumId` da atribuição de cada contato (que **é** o id do formulário de Lead
Ads) com os campos que cada um encheu. `wesales/dados/formularios-meta-27-09.json`:

| formulário | leads | campos de anúncio que ele enche |
|---|---|---|
| `2412763482587375` | 21 | `Urgência`, `Necessidade`, `Investimento mensal` |
| `1026163897118958` | 8 | `Urgência`, `Necessidade` — **falta `Investimento mensal`** |
| `28266780626312413` | 7 | os três |
| `1625438192440294` | 3 | os três |
| outros **cinco** | 1 cada | **nenhum** |

- **São 9 formulários, não 8.** O roadmap dimensionava a opção A do G-04 por 8.
- **O mapeamento é por formulário e inconsistente** — um dos quatro deixa de fora um
  campo que os outros três trazem.
- **Cinco formulários não mapeiam nada.** Cinco leads pagos entraram só com nome e
  telefone.
- **A resposta não mapeada não vai para outro lugar: desaparece.** Conferido — nenhum
  `customField` fora dos 56 aparece nos contatos, e `companyName`, `website`, `city`,
  `state`, `postalCode` estão todos em **0/64**.

**Isto é um defeito separado do G-04**, e nem a opção A nem a B o resolvem: o G-04 é sobre
a picklist de **um** campo; este é sobre campos que nem chegam. Entra na lista como item
próprio.

**O que não deu para medir daqui, e é honesto dizer:** quais perguntas cada formulário
faz. Exige `ads_get_ad_entities`, e a conta está `UNSETTLED` com `is_queryable: false`
(reconferido em leitura fresca hoje). **Então eu sei que o mapeamento está incompleto; não
sei ainda quanto dado está sendo descartado.** Quando a conta voltar a `ACTIVE`, isso é a
primeira coisa a ler — e aí o mapa de pastas da §4 do `USABILIDADE.md` pode mudar, porque
campo que passar a chegar com o lead troca de pasta.

**Onde se conserta:** na tela do GHL, no mapeamento da integração de Lead Ads, formulário
por formulário. Não sai por API pública.

### E um achado de conferência que precisa da sua checagem

`ads_get_ad_account_pages` devolveu, para a página **"O Próximo Cliente"**
(`1117439194786453`): **`leadgen_tos_accepted: false`**.

Os Termos de Lead Generation da página não estão aceitos. Isso **impede criar novo
conjunto de anúncios de Lead Ads**. Não afirmo que explica o passado — leads de Lead Ads
entraram, então ou o termo foi aceito e caiu, ou a flag não cobre o histórico. Mas para a
reativação a 10 leads/dia isso é um bloqueio a conferir, junto com o `UNSETTLED`. Aceita-se
em https://www.facebook.com/legal/leadgen/tos

## 5. O texto da tarefa T1 manda clicar num botão que não existe

A tarefa diz para clicar em "Ligar via WhatsApp". **Esta conta não tem esse botão** — o
WhatsApp aqui não é a Cloud API oficial (três evidências convergentes em `CANAIS.md`:
`TYPE_CUSTOM_SMS`, `sourceId` de app de marketplace, JID de grupo entrando como
contato), e a WhatsApp Business Calling API exige a oficial.

Telefone tem de ser o passo 1 do texto. Conserto de texto, sem risco — mas mexe em
workflow publicado, então precisa da API interna ou da tela.

## 6. Dois portões leem tag que ninguém escreve

| tag | quem lê | quem escreve |
|---|---|---|
| `fila-wa` | 3 workflows, num portão | **ninguém** |
| `sdr-lotado` | 4 workflows, num portão | **ninguém** |

O `sdr-lotado` é o **freio de capacidade**: quatro portões consultam se o SDR está
lotado, e a resposta é sempre "não", porque nada nunca aplica a tag. O freio não existe.

**Não afeta a terça** — o portão sempre passa hoje, com 5 leads. O custo aparece no
cenário de 10 leads/dia, quando a fila estourar e o freio não fechar.

**Tem alternativa que não depende de liberar host nenhum:** o workflow só precisa **ler**
a tag, e nada diz que quem escreve tem de ser um workflow. Um atuador externo (Action
contando tarefa vencida) aplica e remove a tag por fora, e o freio passa a existir.
Limites honestos e o desenho em `TRAVAS-E-ALTERNATIVAS.md`.

## 7. R-14, auditoria de compliance — espera volume, não trabalho

Rotina que prova que ninguém com DND recebeu mensagem e que nada saiu fora da janela.
Está especificado e não construído **por decisão**: com zero mensagem enviada, a
auditoria não tem o que auditar. Entra quando a máquina começar a mandar.

## 8. E os dois que valem mais que qualquer configuração

`Daniel` (`+5521968390582`) e `genilson | Bombeiro` (`+5521972023213`), em `NEGOCIAR`,
R$ 5.000 cada. Nota **93**, faixa A: `Budget` = `Tem`, `Prazo` = `Pra ontem`,
`Investimento mensal` = `Acima de 10k`, `Decisor` = `Sim`.

Criados em **19/09**. `updatedAt` e `lastStatusChangeAt`: **19/09**. Oito dias, nenhum
toque. Conferido ao vivo hoje.

Nenhum item desta lista rende o que ligar para esses dois rende.

## Resumindo quem faz o quê

| falta | de quem é | tem prazo? |
|---|---|---|
| conta de anúncio `UNSETTLED` | **você**, no Gerenciador | manda em tudo |
| ligar para Daniel e Genilson | **você** ou o closer | 8 dias parados |
| dizer quem é o SDR | **você** (uma frase) | antes de terça |
| G-04 A ou B | **você** (recomendo B) | não |
| mapeamento dos 9 formulários do Meta | **você** na tela do GHL, ou eu com o passo a passo | não, mas cada lead novo entra cego |
| `leadgen_tos_accepted: false` na página | **você**, conferir | trava campanha nova |
| apertar o botão das pastas + 27 arrastos | **você** | não |
| distribuir dono nos 36 leads | minha, depois da sua frase | antes de terça |
| publicar `Reunião Cancelada` | minha, com API interna ou tela | não |
| texto da T1 | minha, com API interna ou tela | não |
| atuador de `sdr-lotado` e `fila-wa` | minha | quando o volume vier |
| R-14 | minha | quando houver mensagem |

**Nada nesta lista tem prazo antes de segunda.** A janela `days: [2]`, que era o único
item com data, foi cancelada por medição — ver item 1 do `ESTADO-27-09.md`.
