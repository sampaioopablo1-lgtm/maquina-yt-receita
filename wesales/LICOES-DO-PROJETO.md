# Lições do projeto WeSales — a camada destilada

**Leia este arquivo primeiro, em qualquer sessão.** Ele não conta o histórico: ele
diz o que é invariante, quais erros este projeto já cometeu mais de uma vez, e qual
verificação impede cada um. O objetivo é que ninguém pague duas vezes pelo mesmo
aprendizado.

## O que este arquivo é, e o que ele não é

| arquivo | natureza | quando usar |
|---|---|---|
| **este** | destilado, não cronológico: invariantes + padrões de erro + mapa de acesso | sempre, antes de agir |
| `APRENDIZADOS-CRM.md` (branch `claude/amazing-johnson-mclksg`, ~6.700 linhas) | **registro de casos, datado**, um achado por entrada | quando precisar do caso específico e da evidência dele |
| `ESTADO-27-09.md` | estado da conta e trilha de auditoria das escritas | antes de escrever no CRM |
| `USABILIDADE.md` | medições de usabilidade e os defeitos de fila | trabalho de experiência das funções |
| `TRAVAS-E-ALTERNATIVAS.md` | o que é possível por qual caminho | quando algo parecer impossível |

**Não duplicar conteúdo entre eles.** Este projeto já perdeu tempo com duplicata:
um `ABERTURA.md` foi escrito numa sessão enquanto outro, melhor, já existia noutro
branch — e o novo trazia premissas que a conta desmentia. Achado, removido, e a
lição virou esta linha.

---

# PARTE 1 — INVARIANTES

Coisas que não mudam com autorização nova, com pressa, nem com plano melhor.

## 1.1 Nunca excluir. Nada.

Contato, lead, oportunidade, campo, tag, workflow, pipeline: **nunca**. Descartar é
`status = lost` (ou `abandoned` para nutrição). A etapa fica onde estava.

O dono reforçou em 27/09, com o motivo: **todos os leads vieram de campanha paga
pelo formulário do Meta Ads.** Cada contato é dinheiro já gasto em anúncio. Apagar
um não é limpar base — é jogar fora a compra e o histórico que prova o que o
anúncio trouxe.

Consequência para código: um script que atua sobre contato **não deve conter o verbo
de exclusão**, nem para um caminho que "nunca vai ser chamado". Não é questão de
disciplina na hora de chamar; é de não existir o caminho.

## 1.2 São DOIS formulários, e confundi-los estraga a leitura da conta

Esta distinção foi esclarecida pelo dono em 27/09 e é estrutural:

| | formulário do **Meta Ads** (Lead Ads) | formulário de **qualificação do SDR** |
|---|---|---|
| quem preenche | o próprio interessado, no anúncio | o **SDR**, durante a ligação |
| quando | na entrada do lead | ao marcar a reunião com o closer |
| o que traz | contato, `Urgência`, `Necessidade`, `Dor principal`, `Investimento mensal`, atribuição (`campaignId`, `adSetId`, `adId`) | o BANT e o fit: `Budget`, `Decisor`, `Prazo`, `Clientes novos por mês`, `Tem time comercial`, `Quem atende os leads` |

E o modelo de preenchimento é **progressivo**: os campos personalizados vão sendo
acrescentados ao mesmo lead/oportunidade **ao longo do processo, até o fechamento da
venda**. O registro não nasce completo e não deveria parecer completo.

**O erro que isso previne, e que eu quase cometi em 27/09:** olhei `Budget`,
`Decisor` e `Clientes novos por mês` vazios em 60 de 64 contatos e tratei como
defeito de captação. **Não é defeito. É o processo em andamento.** Eu ia calcular a
`Nota de qualificação` da §9.1 para todos — e como a §9.1 dá consequência automática
à faixa (25–44 vai para nutrição com `abandoned`, 0–24 é descarte com `lost`), eu
teria **descartado lead real pago** por causa de campo que ainda não chegou a ser
preenchido.

Daí a regra: **campo vazio pode ser "ainda não", não "faltou".** Antes de tratar
vazio como defeito, perguntar quem preenche aquele campo e em que momento.

## 1.3 A nota e a prioridade pertencem ao fluxo, no momento certo

`Nota de qualificação` é montada no **Pós-agendamento (nó 4)**, depois do formulário
do SDR — não na entrada, não por rotina, não em lote. Rotina que calcula nota
antecipada está sempre errada, porque pontua ausência de dado como ausência de fit.

## 1.4 Autorização é por escopo, e escopo não se estica

O `APROVADO.md` é o freio de mão: `[ ]` significa não autorizado, e **um `[x]` que a
própria rotina escreveu não é autorização**. Autorização do dono ao vivo em chat
vale, e vale **para o que ele disse**, não para o que seria conveniente inferir.

Quando o dono autorizou "aplique as melhorias e correções no CRM, módulo por
módulo", isso não derrubou 1.1 nem 1.2. Autorização amplia o que posso fazer; não
apaga o que não se deve fazer.

## 1.5 Toda escrita no CRM entra na trilha de auditoria

`ESTADO-27-09.md` §1: o quê, quantos, por quê. **Sem trilha, a escrita não
aconteceu** — porque ninguém vai conseguir desfazer nem entender depois.

---

# PARTE 2 — OS PADRÕES DE ERRO QUE SE REPETEM

Cada um com a forma do erro, um caso real, e a verificação que o mata.

## 2.1 Contar string não é contar coisa

**Forma:** procurar um nome no dump/arquivo e reportar a contagem como se fosse uso.

**Casos:** a string `ai_agent` aparece nos 36 dumps de produção — sempre dentro de
`nestedDropdownTypes`, que é o **catálogo** de tipos que o construtor oferece, não nó
montado. Contar string daria "36 workflows usam IA"; o censo do campo `type` deu
**zero**. Antes disso, `fila-wa` apareceu 90+ vezes e eu quase chamei de "tag em uso"
— todas as ocorrências eram `remove_contact_tag` ou condição, nenhuma era `add`.

**Verificação:** contar pelo **papel estrutural** (o campo `type` do nó, o verbo da
ação), nunca pela presença do texto.

## 2.2 Portão que lê o que ninguém escreve é peça morta

**Forma:** a máquina consulta um estado que nenhum produtor produz. Não dá erro
nenhum: o portão simplesmente sempre passa (ou sempre barra).

**Casos:** `sdr-lotado` é lido em portão por 4 workflows de produção e **escrito por
nenhum** — o freio do teto de 100 tarefas/dia não tem atuador, e a notificação do
`Monitor de Capacidade` diz ao gestor que *"o sistema segura sozinho"*. `fila-wa` é
lida por 3 e adicionada por 0 — a fila de WhatsApp do SDR não pode encher.
`reengajamento-ativo` é apagada por 3 e criada por nenhum, porque o workflow que a
criaria não tem dump ativo.

**Verificação, que rende sempre:** para cada tag e cada campo, cruzar **quem LÊ**
(`if_else`) contra **quem ESCREVE** (`add_contact_tag` / `update_contact_field`).
Assimetria é defeito ou é manual — e aí tem de estar escrito que é manual.

## 2.3 Manual por desenho ≠ defeito

**Forma:** a varredura de 2.2 acusa "ninguém escreve" e você chama de defeito,
quando o desenho previa uma pessoa aplicando à mão.

**Caso:** `pausado` é lida por 5 workflows e escrita por nenhum — e a §3.1 manda o
SDR aplicar à mão quando o lead pede "me liga mês que vem". Correto. A diferença com
o `sdr-lotado` é uma frase: lá a notificação **afirma** que o sistema faz sozinho.

**Verificação:** antes de chamar de defeito, procurar no documento de operação se
alguém foi instruído a fazer aquilo. Se foi, é desenho. Se o sistema **promete** que
faz e não faz, é defeito — e do pior tipo, porque induz confiança.

## 2.4 Tag que só entra e nunca sai

**Forma:** aplicar sem remover. A base acumula e o filtro que depende da ausência
para de funcionar.

**Casos:** `limpar-tarefas` é aplicada por 7 workflows e removida por nenhum — é a
causa de a lista 8.5 do gestor devolver 18 linhas, 11 delas de leads já descartados.
`telefone-invalido` é aplicada por 4 e removida por nenhum: número corrigido fica
rebaixado para sempre (e a regra 8 da §9.2 no `recalcula_prioridade.py` o mantém em
`Prioridade` 1).

**Verificação:** toda tag nova nasce com a pergunta "quem a tira, e quando?" — sem
resposta, não nasce.

## 2.5 Proteção em camada errada

**Forma:** proteger no lugar que parece certo, e não no lugar que o sistema consulta.

**Caso, e foi meu:** liguei `dnd = true` em 30 contatos para travar a rampa, sem
aplicar a tag `nao-perturbe`. Mas os portões da cadência testam
`tags index-of-false ['nao-perturbe']` — **é a tag que a lógica lê**; o DND bloqueia
só o canal de envio. Resultado: o canal calado e a régua andando, queimando tentativa
em silêncio, que é o pior dos dois mundos. Corrigido em 27/09, 31 tags aplicadas.

**Verificação:** achar o portão real (no dump) e proteger exatamente a condição que
ele lê. "Deve funcionar" não é verificação.

## 2.6 Ler ausência de artefato como ausência de execução

**Forma:** os artefatos que você esperava não estão lá, então você conclui que nada
rodou — sem checar se eles vêm **antes ou depois** do ponto onde a execução parou.

**Caso, o mais grave que cometi:** não havia tag de fila nem tarefa nos 38 leads de
`CONECTAR`, e eu concluí que as cadências nunca os inscreveram. Estavam inscritos e
**parados no primeiro `Wait`**, esperando a janela de execução. A prova estava nos
mesmos contatos que eu li: `Tentativa nº` = 0 e `Permissão WhatsApp` = `Não
solicitado` são **escritas de inicialização do nó 0**. Tag e tarefa vêm depois do nó
de mensagem, que é o que espera a janela. Eu havia recomendado `Add to Workflow` em
lote — que teria **duplicado execução**.

**Verificação:** antes de concluir "não rodou", localizar no dump a **ordem** dos nós
e perguntar quais escritas já deviam existir se tivesse rodado até o ponto X. Campo
inicializado com zero **é** rastro de execução, não de ausência.

## 2.7 Escopo estreito que parece varredura

**Forma:** medir num subconjunto e relatar como se fosse a conta inteira.

**Casos:** declarei "45 de 56 campos mortos" varrendo só a etapa `CONECTAR` e com
fixture montado apenas com os contatos que eu havia lido — **18 foram desmentidos**
por leitura direta. Antes disso, `ALVOS` numa lista fixa no
`patch_condicoes_etapa.py` parecia cobertura e não era.

**Verificação:** dizer sempre o denominador ("de 64 contatos", "dos 36 dumps de
produção"). Se o denominador é um subconjunto, a conclusão também é.

## 2.8 Confiar no comentário em vez do estado

**Forma:** o código afirma uma coisa e a realidade é outra; você cita o comentário.

**Caso:** `renew.js` e `login-capture.js` dizem gravar em "`.local/` (gitignored)".
**`.local` não estava no `.gitignore`**, e este repositório é **público** — um
`git add -A` depois de renovar o bearer publicaria a sessão logada do CRM. Corrigido
em 27/09; histórico conferido, nada havia sido comitado.

**Verificação:** `git check-ignore -v <caminho>` em vez de ler o comentário. Vale para
qualquer afirmação de estado que um comentário faça.

## 2.9 Parser errado vira "a conta mudou"

**Forma:** um bug de leitura seu parece movimento no sistema observado.

**Caso:** contei tarefas em `relations[0].tasks` e achei zero, quando elas vêm na
chave de **topo** `tasks` da oportunidade. Quase reportei "a faxina apagou as duas
tarefas vencidas". Elas estavam lá.

**Verificação:** mudança inesperada no número é primeiro suspeita **do leitor**.
Confirmar na fonte (um objeto inteiro, cru) antes de reportar movimento.

## 2.10 Dois nomes parecidos, dois objetos

**Forma:** tratar campos homônimos como o mesmo.

**Casos:** o **nome da oportunidade** e o **nome do contato** são campos diferentes —
a oportunidade da `Carla Sampaio` estava em branco enquanto o contato tinha nome, e eu
relatei "lead sem nome". O seletor de coluna mostra **dois** `Empresa` (um nativo,
vazio; um personalizado). E `AGENDAR` foi renomeada para `REUNIÃO DE DIAGNÓSTICO`
mantendo o mesmo id.

**Verificação:** ler o objeto certo pelo id, não pelo rótulo.

## 2.11 Levar dado velho ao dono

**Forma:** reportar achado que já foi resolvido, ou repetir como novo o que está
catalogado.

**Casos:** 3 de 5 achados de uma rodada já estavam resolvidos quando reportei.
Apresentei a picklist de `Investimento mensal` como defeito novo — estava catalogada
como **G-04** desde 21/09, com decisão do dono pendente. E o `IMPLEMENTACAO-WORKFLOWS.md`
ainda diz "W11 rascunho, 0 inscritos" quando o dump diz `published` v35.

**Verificação:** antes de reportar, procurar o achado no roadmap e nos catálogos
(G-xx, F-xx, R-xx). E desconfiar de cabeçalho de documento: o estado está na conta e
no dump, não na prosa.

## 2.12 Anunciar destravado antes de ler o corpo da requisição

**Forma:** ver o endpoint existir e concluir que o caso de uso está resolvido.

**Caso, de hoje:** achei `POST /custom-fields/folder` e `PUT /custom-fields/{id}` no
spec oficial e anunciei que reagrupar os 53 campos saía por API. Fui escrever o
script e li o corpo: **o `PUT` não aceita `parentId`**. Criar pasta, sim; **mover
campo existente, não** — só campo novo nasce em pasta. Voltou a ser trabalho de tela.

**Verificação:** endpoint existir não é capacidade. Ler `requestBody.properties` e
confirmar que o campo que você precisa mexer está lá.

## 2.13 Agrupar campo por nome do campo, em vez de por quem o preenche

**Forma:** montar a tela em cima do que o campo *parece ser*, sem medir quem escreve
nele. O erro não aparece como erro: aparece como uma pasta com nome plausível.

**Caso, de hoje:** a §4 do `USABILIDADE.md` tinha uma pasta `VEIO DO ANÚNCIO` com 20
campos, porque `Budget`, `Decisor`, `Prazo` e `Urgência` *soam* como coisa que o
formulário do Meta Ads coleta. O dono corrigiu (§1.2: são dois formulários), e a medição
fechou o caso — preenchimento nos 64 contatos: `Urgência` 40, `Necessidade` 34,
`Investimento mensal` 32; e então um degrau seco para `Dor principal` 6, `Budget` 3,
`Segmento` 0. **Três** campos vêm do anúncio; os outros 17 a SDR preenche depois.

**Por que custava caro:** o dano não era a pasta feia. Um campo vazio dentro de
`VEIO DO ANÚNCIO` lê como "o anúncio não mandou" — quando é "a SDR ainda não perguntou".
A pasta teria escondido o trabalho dela da própria tela dela. É a §1.2 outra vez, agora
no lugar onde ela dói.

**Verificação:** antes de agrupar campo por função, contar em quantos registros ele está
preenchido. Snapshot versionado em `wesales/dados/campos-27-09.json`, conferido pelo
próprio script (`--plano` falha se sobrar ou faltar campo).

### CORREÇÃO, no mesmo dia, e ela é o miolo da lição

Eu havia escrito aqui: *"campo que chega com o lead aparece em quase todos; campo de
etapa posterior aparece em poucos. O degrau na contagem é onde fica a fronteira, e é
observável."* **Isso está errado, e o dono apontou o porquê:** *"tem campos, pelo
formulário nativo da Meta associado ao CRM, que podem correlacionar com o CRM."*

O degrau na contagem marca a fronteira do **mapeamento**, não a do processo. Uma
pergunta que o formulário do Meta faz mas que ninguém mapeou para o campo do CRM lê
como `0/64` — **idêntico** a um campo que ninguém nunca preenche. Os dois casos têm a
mesma aparência no dado e significados opostos:

- "a SDR ainda precisa perguntar isso" → trabalho legítimo dela
- "o lead **já respondeu** e a resposta foi descartada na porta" → dado pago no lixo

Medi a diferença e ela existe nesta conta (`wesales/dados/formularios-meta-27-09.json`):
**9 formulários** de Lead Ads distintos, e o mapeamento é por formulário e inconsistente
— 4 mapeiam 2 ou 3 campos, um deles não mapeia `Investimento mensal em anúncios` que os
outros mapeiam, e **5 formulários não mapeiam nada**. Cinco leads pagos entraram só com
nome e telefone.

**O que fica como verificação, então:** contagem de preenchimento separa "campo que a
conta usa" de "campo que a conta não usa" — e **nada mais**. Para saber se um `0/64` é
"ninguém pergunta" ou "a resposta é descartada", tem de olhar a definição do formulário
de origem, não o CRM. Enquanto essa leitura não existir, todo agrupamento por origem é
**provisório**, e tem de estar escrito que é.

## 2.14 Ler uma lista da resposta e supor que é a resposta inteira

**Forma:** a rota devolve várias coleções; o código lê uma e conclui pela ausência.

**Caso, de hoje:** para não recriar pasta que já existe, o script leu `fields` da
resposta do `GET /custom-fields/object-key/{objectKey}` e procurou pasta ali. O spec tem
**duas** listas: `fields` e `folders`. A checagem nunca acharia nada, e o script criaria
as cinco pastas de novo a cada execução — idempotência que parecia existir. Achado ao
ler o schema da resposta, antes de rodar.

**O que escondeu:** o conector MCP `locations_get-custom-fields` também devolve só
`fields`, nas duas variantes (`model=contact` e `model=all`). Duas leituras concordando
não são confirmação quando as duas são a mesma leitura. E a conta já tinha **três**
pastas em uso, que nenhuma das duas mostrou.

**Verificação:** ao consultar existência antes de criar, ler o schema da resposta e
conferir em qual coleção a coisa mora. Idempotência não testada é idempotência suposta.

## 2.15 Confiar na lista quando a pergunta é sobre o registro

**Forma:** verificar uma escrita relendo o endpoint de **lista**, que serve um índice de
busca, e não o registro.

**Caso, de hoje:** depois de escrever `assignedTo` em 48 contatos — todas as 48 respostas
`200` com o `assignedTo` novo no corpo — o `contacts_get-contacts` ainda devolvia **2 sem
dono**. Lidos um a um com `contacts_get-contact`, os dois **tinham** o campo. O índice da
lista atrasa.

**O que eu quase fiz:** reescrever os dois, e relatar "62 de 64" ao dono. Duas escritas à
toa e um número errado, os dois por ler a fonte errada.

**Verificação:** a lista serve para achar; o registro serve para confirmar. Quando a
lista discorda do que a escrita respondeu, ler o registro antes de concluir qualquer
coisa — inclusive antes de repetir a escrita.

## 2.16 Parar na metade da mecânica por não ter lido a configuração

**Forma:** aplicar a correção na entidade errada, ou só em parte dela, porque não se leu
onde o mecanismo de fato pendura o comportamento.

**Caso, de hoje:** atribuí dono nas 43 oportunidades e ia parar ali, dizendo ao dono que
não sabia se os 48 contatos precisavam do mesmo. Fui ler o dump da `Cadência 12x30`:
**todo nó de tarefa traz `"assignedTo": "contact.assigned_user"`**. A fila do SDR se monta
pelo dono do **contato**. As 43 oportunidades, sozinhas, não colocariam uma única tarefa na
fila de ninguém — a correção teria parecido feita e não teria efeito.

**Verificação:** antes de declarar uma correção completa, achar no artefato que executa
(o dump do workflow, não o documento) de qual campo ele lê. Uma busca por `assignedTo`
nos 36 dumps custa menos que uma abertura de operação com a fila vazia.

## 2.17 A própria plataforma deixa a resposta na conta, e eu ia pedir acesso

**Forma:** concluir que um dado só existe do outro lado de uma API fechada, sem procurar
o que essa API já escreveu na base.

**Caso, de hoje:** eu precisava saber **quais perguntas** o formulário do Meta faz, e
escrevi que não dava — `ads_get_ad_entities` exige a conta `is_queryable`, e ela está
`UNSETTLED`. A resposta estava na própria subconta: a Meta injeta um contato de teste
cujos valores são literalmente `<test lead: dummy data for quando_você_pretende_
resolver_isso?>`. **O nome da pergunta, dentro do valor do campo.** Três campos, três
perguntas, mapeamento completo — sem nenhum acesso novo.

**Verificação:** antes de declarar que um dado exige acesso que não se tem, procurar o que
a integração já gravou. Registro de teste, log de webhook e campo de atribuição costumam
carregar metadado que a API só entregaria autenticada. Foi a atribuição (`mediumId`) que
deu os ids dos 9 formulários, e foi o contato de teste que deu as perguntas.

## 2.18 Regra de derivação com o lado "senão" aberto

**Forma:** escrever a regra pelo caso interessante e deixar o resto cair num `else`, que
então aceita qualquer lixo.

**Caso, de hoje:** para derivar `Investe em anúncios` de `Investimento mensal`, escrevi
*"`Não invisto nada ainda` → `Nunca`; qualquer outro → `Sim`"*. Rodei em seco antes de
aplicar e o contato `<test lead>` da Meta apareceu na lista recebendo
`Investe em anúncios = Sim` — derivado de uma **string de teste**. O `else` não distingue
"investe 10k" de "isto não é uma resposta".

**Verificação:** derivação usa **vocabulário fechado** nos dois lados. Valor fora da lista
conhecida não deriva nada e vira exceção reportada, não um `Sim` silencioso. O relatório
de ignorados é parte do resultado, não ruído.

## 2.19 Rota existir não é capacidade: o servidor tem de aceitar o `objectKey`

**Forma:** confirmar no spec que a rota existe, confirmar que o `requestBody` tem o campo
que interessa — e ainda assim errar, porque o servidor recusa o **valor** que importa.

**Caso, de hoje, e é a terceira correção minha no mesmo assunto:** eu escrevi, na §4 do
`USABILIDADE.md` e no docstring do `pastas_de_campo.py`, que criar pasta de campo saía por
API pública. Rodei na Action, com PIT válido:

```
GET  /custom-fields/object-key/contact        -> HTTP 400
POST /custom-fields/folder objectKey=contact  -> HTTP 400
{"message":"Api does not support objectKey of type contact or opportunity"}
```

O grupo `/custom-fields/` da v2 é para **objeto personalizado**. Os campos do contato não
estão nele. E o truque de renomear a pasta grande para poupar 29 arrastos morreu junto,
porque o `PUT` de renome é do mesmo grupo.

**A escada de enganos, porque ela é instrutiva:**

| o que eu conferi | o que faltava |
|---|---|
| a rota existe no spec | ler o `requestBody` (lição 2.12) |
| o corpo tem o campo | ler qual **coleção** a resposta traz (lição 2.14) |
| a rota e o corpo servem | o servidor aceitar o **`objectKey`** — esta |

**Verificação:** spec descreve a forma, não a permissão nem o domínio. Antes de escrever
documento afirmando que algo sai por API, **fazer uma chamada de sonda** — uma, com nome
reconhecível, e ler a resposta bruta. Custa um dispatch. Documento errado custa uma
decisão errada do dono.

**E o corolário que dói:** eu prometi ao dono "27 arrastos em vez de 56" com base nessa
suposição. O número certo é 56, mais criar as 5 pastas. Prometer economia que não existe é
pior que não achar a economia.

## 2.20 Duas trilhas de execução que não se enxergam

**Forma:** sessão na nuvem e sessão no PC produzindo estado e documento que o outro
lado não lê.

**Casos:** o `APRENDIZADOS-CRM.md` mora num branch e a operação de hoje em outro —
inclusive **este arquivo** nasce nesse problema. O `ESTADO-E-PLANO.md` ficou fora de
três varreduras seguidas. Um `ABERTURA.md` duplicado foi escrito porque o bom estava
noutro branch.

**Verificação:** antes de criar documento, `git ls-tree` nos branches ativos
procurando assunto parecido. Antes de tratar um roadmap como fonte única, checar se
existe outro plano.

---

# PARTE 3 — MAPA DE ACESSO (o que dá para fazer de onde)

Medido em 27/09/2026. Economiza horas de tentativa.

| quero | funciona por | não funciona por |
|---|---|---|
| ler/escrever contato e oportunidade | **conector MCP `GHL CRM`** (roda fora do contêiner) | `curl` do contêiner: proxy nega |
| criar pasta de campo | API pública (`POST /custom-fields/folder`) via Action com `GHL_PIT` | — |
| **mover** campo para pasta | **nada** — `PUT` não aceita `parentId`. É tela | API pública |
| editar workflow | **API interna** (`backend.leadconnectorhq.com`), cliente em `ghl_interno.py` | API pública: só `GET /workflows/`. Snapshot: só `GET` + `share/link` |
| rodar a API interna | GitHub Actions com segredo de sessão; ou host liberado na política de rede | contêiner: **403 na CONNECT** |
| ler spec oficial do GHL | `git clone GoHighLevel/highlevel-api-docs` | `WebFetch` nos domínios do GHL: egresso bloqueado |
| pesquisar documentação | `WebSearch` (roda fora do contêiner) | `WebFetch` em `help.gohighlevel.com` |
| ler condições exatas de portão | os **36 dumps de produção** em `wesales/workflows-json/` | percorrer o grafo pelo `next` dos `if_else` (a continuação mora fora) |

**A regra que isso ensina:** quando um host é negado, a pergunta não é como furar o
proxy — é **onde mais esse dado vive**. Duas vezes em 27/09 a resposta foi "no
GitHub": o spec oficial da API e os dumps de workflow.

---

# PARTE 4 — O QUE FICOU PARA TRÁS POR ENTENDIMENTO ANTIGO

O dono pediu em 27/09 que isto fosse explícito: coisas paradas por uma leitura que
já mudou, e que merecem ser reabertas em vez de ficarem herdadas como "decidido".

| item | por que parou | o que mudou / o que reabrir |
|---|---|---|
| **Reagrupar os 53 campos em 4 pastas** | tratado como tela, e tela nunca aconteceu | segue tela (ver 2.12), mas é a **origem da queixa do dono** ("meio completo e confuso"). Merece ser feito, não herdado como pendência |
| **`Add to Workflow` em lote** | eu recomendei sob hipótese errada | **retirado**: os leads já estão inscritos (2.6). Não reabrir |
| **Nota de qualificação em lote** | eu tinha posto na fila | **retirado** por 1.2/1.3. Não reabrir |
| **G-04, picklist de `Investimento mensal`** | espera decisão do dono desde 21/09 | 3 de 4 leads do Meta somam 0 nessa linha da régua. A recomendação medida é a **Opção B** (ler `Urgência`/`Necessidade` por `Contains`), porque são 8 formulários e a A é trabalho de tela 8 vezes |
| **Janela das cadências em `days: [2]`** | exige API interna | segue sendo a única alavanca que para o motor (a tag só cala o canal). Vira desnecessária depois de terça |
| **`fila-wa` e `sdr-lotado`** | tratados como "conserto de workflow", logo bloqueados | há **alternativa sem editar workflow**: atuador externo aplicando a tag pelo conector, porque o workflow só precisa **ler** (ver `TRAVAS-E-ALTERNATIVAS.md`) |
| **Laço de atribuição (criativo → cliente)** | bloqueado pela conta de anúncio `UNSETTLED` | o lado do CRM (agrupar por `adSetId`/`adId`) dá para adiantar sem gastar |
| **IA do GHL** (Conversation, Voice, Reviews, Content, Ask, AI Studio) | **decisão ativa do dono**: parar por custo | não é "esquecido", é escolha. Sem plano, a conta cai em pay-per-use no cartão da agência. Ver `IA-E-CUSTO-GHL.md` |

---

# PARTE 5 — COMO TRABALHAR AQUI

1. **Medir antes de escrever.** Ler o estado, decidir pelo dado, escrever, **reler
   para confirmar**. Escrita sem leitura antes é chute.
2. **Um módulo por rodada**, com trilha de auditoria. Lote grande sem conferência
   entre lotes é como se erra em 40 registros de uma vez.
3. **Declarar o denominador** em toda medição.
4. **Corrigir em voz alta.** Metade do valor deste arquivo vem de erros meus escritos
   por inteiro. Achado que se descobre errado vale mais corrigido do que apagado.
5. **Verificação que achou defeito duas vezes vira script**, não vira parágrafo.
6. **Não acordar o dono por nada que não seja novo** — e quando for novo, dizer o
   número, não a impressão.
7. **Ação premium de workflow** (webhook, Google Sheets, Slack) custa ~US$ 0,01 por
   execução na carteira da agência. Hoje nenhum dos 36 workflows usa. Não estragar
   isso sem decisão.

## 2.21 "A API não faz" só vale depois de ler o spec inteiro — e a rota antiga

Em 27/09 escrevi que campo de contato não podia ser criado por API, porque
`POST /custom-fields/` recusa `objectKey=contact` (2.19). Faltou olhar o **outro**
grupo: `POST /locations/{id}/customFields` aceita `model: contact` — está no
`locations.json` do repositório oficial. A conclusão certa era "a rota nova recusa;
a antiga aceita". Generalizei de uma rota para a plataforma.

O que fiz de diferente na mesma tarde: clonei `GoHighLevel/highlevel-api-docs` e
listei **todas** as rotas dos grupos relevantes antes de responder "dá ou não dá".
Formulário: não dá (três rotas, todas de leitura). Tudo o que o dono queria do
formulário: dá, por sete rotas — e por isso a resposta foi construir a página, não
retratar de novo.

Regra: antes de dizer que uma plataforma não faz X, listar as rotas do spec e
procurar X pelo **substantivo** (customFields, appointments, free-slots), não pelo
grupo onde eu esperava encontrá-lo.

## 2.22 Dois serviços, duas regras opostas para o mesmo cabeçalho

O GHL exige `User-Agent` de navegador (senão Cloudflare 1010). O Supabase **recusa a
chave secreta** quando o `User-Agent` parece navegador ("Forbidden use of secret API
key in browser", run 36333353072). O mesmo cabeçalho, copiado de um cliente para o
outro, virou um 401 que não dizia nada sobre a chave. Um cliente HTTP por serviço,
cada um com o cabeçalho que aquele serviço espera — não "o que funcionou no anterior".

## 2.23 Um projeto em restrição contamina tudo que se pendura nele

O painel foi publicado primeiro no `maquina-yt-dark`, que está em restrição de cota
de storage: o gateway devolve 402 em PostgREST — o mesmo episódio de 25/08. A função
publica, mas não lê a própria tabela. Antes de pendurar algo novo num projeto, uma
chamada de saúde ao gateway; se 402, outro projeto. Mudei para o
`cscczluzpblzhvojxanp` e a tabela `config` foi criada lá.
