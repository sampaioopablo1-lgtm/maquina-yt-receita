# O que as execuções da rotina horária já descobriram

Memória entre rodadas. Antes de investigar de novo, procure aqui.



## Voltar a oportunidade de etapa NÃO desinscreve do workflow — e a MI-0 da Inbound não olhava a etapa — 23/09/2026, sessão local

Carlos Andrade (lead real) foi a CONECTAR às 19:01 e voltou a NOVO LEAD 10 s
depois. Ficou inscrito na Inbound, na 12x30 e no Speed-to-lead. A 12x30 sai
sozinha (`cad-inbound` → outra régua) e o Speed-to-lead confere a etapa antes
de alertar; a **Inbound mandaria a MI-0** na manhã seguinte: fora da janela a
execução fica parada NO nó da mensagem, e as 3 checagens antes dela (tag,
telefone, permissão) não olham etapa. Campos e tags rodam na hora mesmo fora
da janela (medido: permissão gravada 19:01); só a mensagem espera.

**Conserto:** `patch_guarda_mi0.py` — `if_else` "MI-0 · Ainda vale mandar?"
com as condições do `TI1 · Ainda vale ligar?` antes da MI-0. **Limite:** quem
já está parado na MI-0 não passa pela trava nova → Carlos com DND até a
abertura. Ao clonar `if_else`, remapeie só uuid que não aparece fora do grupo:
o id da etapa CONECTAR também tem formato uuid.

## A própria seção "Ordem sugerida" pode ficar incoerente — o G-23 fechou sem o parágrafo de recapitulação que a família G-16...G-22 sempre escreve (G-24) — 23/09/2026, sessão automática

Toda rodada desta família fecha um item com dois movimentos: escreve o
`### G-XX` detalhado no corpo do Bloco 6, e acrescenta um parágrafo curto no
fim da seção "Ordem sugerida" recapitulando o que mudou (a lista de
decisões que esperam o dono, a lista de itens com desenho completo). O
G-23 fez só o primeiro — fechou o `### G-23` mas não voltou ao fim do
arquivo. Resultado: o parágrafo de fechamento mais recente ali (do G-22)
continuava dizendo que `GUIA-CLOSER.md` "ainda não passou por nenhuma
rodada desta família", quando o próprio G-23 tinha acabado de cruzá-lo —
divergência que só aparece em quem lê só o fim do arquivo (a leitura que a
própria seção instrui fazer quando não há tela/decisão nova).

**Por que isso escapa da varredura normal:** a varredura de coerência desta
família sempre olha *outros* documentos em busca de "medido mas não
rastreado" — nunca tinha olhado a própria seção que faz esse papel. Uma
seção cujo trabalho é resumir pode ela mesma ficar desatualizada, e
ninguém a audita por padrão porque ela *é* a auditoria.

**Regra prática, nova:** todo G-item que fechar nesta família confere, como
último passo antes do commit, se o parágrafo de recapitulação no fim da
"Ordem sugerida" foi escrito — não só se o `### G-XX` do corpo foi. Um
checklist de duas linhas (corpo + recap) é mais barato que descobrir na
rodada seguinte que a lista de "documentos ainda não cruzados" está
mentindo sobre um documento que acabou de ser cruzado.

**O que esta rodada fez, além do achado:** cruzou os três documentos que
sobravam da lista do G-22 (`script-de-ligacao.md`, `GUIA-SDR.md`,
`conectar.md`) contra `PLANO-MULTICANAL.md` (D1-D14, A1-A9) — achado
negativo, os três já batem com o publicado. Com isso mais o G-23 tendo
cruzado `GUIA-CLOSER.md`, a lista nomeada de "documentos ainda não
cruzados" que o G-22 tinha aberto esvaziou; a próxima rodada sem tela nem
decisão escolhe entre os documentos que nunca tiveram uma rodada dedicada
com esse nome (`CONFERENCIA-CAMPOS.md`, `GUIA-MONTAGEM.md`,
`INVENTARIO-WORKFLOWS.md`, `biblioteca-mensagens.md`, `rotina-horaria.md`,
`auditoria-etapa1.md`, `README.md`) ou relê itens represados por premissa
técnica.

**Correção aplicada:** achado promovido a `G-24` no
`ROADMAP-SALES-ENGAGEMENT.md` — o `### G-24` no corpo do Bloco 6, mais os
dois parágrafos de recapitulação que faltavam no fim da "Ordem sugerida"
(um para o G-23, retroativo, e um para o próprio G-24). Zero campo, zero
tag, zero escrita no CRM: item de coerência dentro do próprio roadmap.

## "Buraco nunca especificado" pode já estar publicado — quase desenhei em cima do que o dono já tinha construído e testado (G-23) — 23/09/2026, sessão automática

Cruzando `GUIA-CLOSER.md` contra `build-wesales.md` (F-13), achei dois
sinais que pareciam confirmar um bug: o texto dizia "Negociação parada: 5
dias" enquanto a especificação dizia 3, e "Proposta parada" (Sim do closer,
3 dias, ainda em REUNIÃO DE DIAGNÓSTICO) não tinha workflow nenhum em
lugar nenhum do projeto. Cheguei a **escrever um desenho novo do zero**
(nome de tag incluído, `proposta-parada`) e editar seis documentos antes de
seguir a própria regra deste roadmap ("verificar `PLANO-MULTICANAL.md`
inteiro, inclusive a 'Fila autônoma', antes de aceitar que uma lacuna é
nova" — já escrita pelo G-19, nunca seguida à risca por mim nesta rodada).

Um `grep -rn "negociacao-estagnada\|proposta" wesales/*.md` bem mais cedo
teria mostrado direto: `PLANO-MULTICANAL.md`, item A5, já registrava os
dois alertas publicados e testados pelo dono (`tools/build_estagnacao.py`),
com tag `proposta-pendente` (não `proposta-parada`) e 5 dias para
negociação (não 3) — `GUIA-CLOSER.md` estava certo o tempo todo, e a
"correção" que eu ia aplicar nele teria introduzido um erro real num
documento que não tinha nenhum.

**Regra prática:** antes de especificar qualquer workflow "novo" para
fechar uma lacuna achada por leitura de documento (não por dado do CRM),
rodar `grep` pelo nome do alerta/tag candidato e por palavras-chave do
comportamento em `PLANO-MULTICANAL.md` inteiro e em `wesales/tools/*.py`
— os scripts no repo são a fonte mais confiável de "o que está publicado
de verdade" quando o MCP não tem endpoint de workflow, mais confiável que
reconstruir de memória ou que a prosa de um documento de estado. Reverti
os seis arquivos com `git checkout --` e recomecei do zero a partir do
`grep` certo — nenhum dano ficou, porque o revert aconteceu antes do
commit, mas o tempo perdido (e o risco, se eu tivesse commitado antes de
notar) foi real.

## Dump de workflow que foi SUBSTITUÍDO continua no repositório dizendo `published` — o G-17 chamou de "pior caso" uma cadência que não existia mais — 23/09/2026, sessão local

O `Reengajamento 90 dias` virou a `Nutrição — WhatsApp a cada 15 dias` em
22/09 (mesmo id). O export novo foi gravado com o nome novo, e o arquivo
antigo ficou lá com `status: published`. `auditoria_portoes.py` lê todos os
dumps e acusou 3 cadências; ao vivo eram 2. **Regra:** antes de levar ao dono
uma decisão sobre um workflow, confirme que o nome existe em
`GET /workflow/<LOC>` — a lista ao vivo, não a pasta. Ao renomear/substituir,
mova o dump velho para `workflows-json/_arquivo/` no mesmo commit.

Também: o modo automático do Claude Code negou `opportunities_update` (status
de oportunidade real) e `patch_*.py --aplicar` (edição de workflow publicado)
mesmo com o dono autorizando no chat. Deixe o plano validado ao vivo (sem
`--aplicar`) e entregue o comando pronto para ele rodar com `!`.

## "Quem mais fala disso?" também vale para documentos que nunca foram objeto de nenhuma varredura de coerência anterior — `ESTADO-E-PLANO.md` ficou de fora de três rodadas seguidas (G-10, G-13, G-14) — 23/09/2026, sessão automática

CRM reconfirmado por API antes de investigar: 56 oportunidades (mesma
composição da leitura do G-15/roadmap-self-coherence, sem mudança), 56
campos de contato, pipeline com as mesmas 5 etapas — G-03, G-04 (peça 2),
F-09, F-10 e G-11 (item 1) seguiam exatamente onde estavam, nenhum
desbloqueado. Passo seguinte, pela ordem que o próprio roadmap manda: a
varredura de coerência de sempre.

**O que mudou desta vez:** em vez de `grep` por nome de etapa antigo (G-02,
G-12) ou perguntar quem mais cita um fato já corrigido (G-10, G-14), a
pergunta foi outra — **quais arquivos de `wesales/` nenhuma das rodadas de
coerência já tinha cruzado?** `git log --oneline -- wesales/ESTADO-E-
PLANO.md` mostra a última edição em `deb74cf`, um commit anterior a G-10 —
e nem G-10, nem G-13, nem G-14 (que corrigiram `GUIA-MONTAGEM.md`,
`rotina-limpar-tarefas.md`, `IMPLEMENTACAO-WORKFLOWS.md` e `README.md`)
tocaram nele, apesar de ser o documento com a leitura mais recente e mais
completa da base inteira. Ele tinha uma pergunta em aberto na seção 8, item
"0", desde 23/09 02:35 UTC: o contato `Francisca` (`+5512981913254`,
`9wOSMuznjenFxa3yaep0`) era teste do dono ou pessoa real que escreveu no
WhatsApp da operação? Quem escreveu a pergunta não tinha como responder
sozinho e ninguém tinha voltado a esse arquivo desde então.

**Como resolvi, sem chute:** `conversations_search-conversation` com
`query_contact_id` traz a conversa; `conversations_get-messages` no
`conversationId` traz o fio completo (8 mensagens). Ler o fio de ponta a
ponta bastou: "Oi Pablo, boa noite" (chamando o dono pelo nome), "Te
lembrando do pix", um áudio, "Feito", um número de telefone compartilhado,
"E mais uma vez obrigado pela carona", "Salvou rs". Nenhum sinal comercial
em nenhuma mensagem. Pessoa real, conversa pessoal — a Porta de Entrada
(gatilho de primeira mensagem inbound) não tem como diferenciar isso de um
prospect, e criou oportunidade do mesmo jeito.

**Regra prática, generalizável — estende a do G-10/G-14 ("quem mais fala
disso?") para "quem nunca foi perguntado ainda":** depois de fechar uma
rodada de coerência que reescreve vários documentos, vale listar
explicitamente quais deles foram cruzados — e, na rodada seguinte sem item
desbloqueado, testar `git log --oneline -- wesales/<arquivo>` contra essa
lista para achar o que ficou de fora, não só repetir o mesmo grep de nome de
etapa. Foi assim que apareceu o `ESTADO-E-PLANO.md` aqui, e é provável que
haja outros — a lista de arquivos "já cruzados" que o G-14 abriu
(`GUIA-MONTAGEM.md`, `rotina-limpar-tarefas.md`, `README.md`) continua
sendo um subconjunto de `wesales/`, não o diretório inteiro.

**Correção aplicada:** achado promovido a item de roadmap (`G-16`), linha
nova em `APROVADO.md` (nasce `[ ]`, mesma regra de sempre), passo
preventivo escrito no `GUIA-SDR.md` (ler o fio antes de tratar tarefa `TI1`
como prospect), e a pendência 0 do `ESTADO-E-PLANO.md` marcada como
respondida com link de volta para o G-16. Nenhuma escrita no CRM: a leitura
de conversa não altera nada, só a correção proposta (remover duas tags,
`abandoned` na oportunidade) espera o `[x]` do dono.

## O parágrafo "Com isso" do próprio roadmap pode divergir das entradas que ele resume — a varredura de coerência nunca tinha testado o roadmap contra ele mesmo — 23/09/2026, sessão automática

CRM reconfirmado por API antes de investigar: 56 oportunidades (49 `NOVO
LEAD` `open` + 1 `CONECTAR` `open` + 2 `CONECTAR` `lost` + 2 `NEGOCIAR`
`open` + 1 `NEGOCIAR` `lost` + 1 `REUNIÃO DE DIAGNÓSTICO` `open`) e 56
campos de contato — nenhuma mudança desde a última leitura registrada no
roadmap. Com todo item numerado (G/R/F) `FEITO` ou aguardando o dono/volume
real/tela (nenhum desbloqueado), o passo seguinte era a varredura de
coerência de sempre.

**O que achei, e não é o padrão de sempre (nome de etapa órfão, merge
field, contagem duplicada entre documentos):** o próprio
`ROADMAP-SALES-ENGAGEMENT.md` cita, a cada item fechado, um parágrafo "Com
isso, ... esperam decisão do dono" — uma lista que deveria ser um espelho
fiel de quais itens ainda têm `Pronto quando` sem decisão. G-12, G-13 e
G-14 (fechados em 23/09) mantiveram essa lista correta (cinco itens: G-03,
G-04 peça 2, F-09, F-10, G-11 item 1). O "Com isso" que fechou o **G-15**
— o item seguinte, sobre dedupe cross-canal — perdeu F-09 e F-10 da lista,
sem nenhuma linha explicando por quê, e a rodada seguinte (extensão do
F-08/Local Presence) copiou a lista de três em vez de conferir contra as
próprias entradas do F-09 e F-10 (que continuavam dizendo, ao pé da letra,
"decisão do dono ainda em aberto"). O erro sobreviveu até o parágrafo final
do documento — o texto que qualquer sessão nova lê primeiro para saber "o
que está aberto". Uma sessão que confiasse só nesse parágrafo final teria
reportado ao dono só 3 decisões pendentes, quando eram 5 — duas reais
(F-09: freio de canal do telefone; F-10: alarme de ausência de entrada)
ficariam invisíveis até alguém reler as entradas originais.

**Por que aconteceu:** todo item fechado neste roadmap reescreve o
parágrafo de resumo que vem depois dele, mas a instrução implícita sempre
foi "acrescente o que mudou nesta rodada", nunca "confira se a lista nova
ainda contém tudo que a lista anterior tinha". É fácil de acontecer porque
nenhuma rodada lê o parágrafo anterior lado a lado com o novo — só o
escreve de novo, de memória do que a própria rodada tratou.

**Correção aplicada:** os dois parágrafos ("Com isso" do G-15 e o parágrafo
final) voltaram a listar as cinco decisões; a menção na extensão do F-08
também foi corrigida. `IMPLEMENTACAO-WORKFLOWS.md` §3.6 (checklist de
go-live, item 1 "Decisões do dono") tinha o mesmo problema por um motivo
diferente — citava só G-03/G-04 e uma lista fixa de "cinco tags do F-05"
que já eram seis (T-16 a T-21, com a T-21 do F-13) — trocada a lista fixa
por uma referência a `APROVADO.md` como fonte única, para não desatualizar
de novo.

**Regra prática, generalizável — nova classe de varredura de coerência:**
além de grep por nome de etapa antigo e merge field órfão em documentos
vizinhos, a varredura de coerência de uma rodada sem item desbloqueado
deveria também comparar o parágrafo "Com isso" mais recente do roadmap
contra o anterior, item a item — não só ler o mais recente e assumir que
ele está completo. Documento nenhum sofre revisão externa entre rodadas;
se o próprio roadmap pode divergir de si mesmo sem ninguém notar por três
rodadas seguidas, qualquer lista "resumo do estado atual" em qualquer
documento do projeto merece o mesmo tipo de conferência de tempos em
tempos, não só quando um grep por texto aponta problema.

## Auditoria diária (só leitura): a entrada de anúncio dobrou o tempo parada (25h→49h) e o pipeline saiu do zero absoluto só por teste manual, não por lead real — 23/09/2026, sessão automática (auditor diário)

Segunda rodada do **Auditor diário** (read-only, GHL-CRM MCP, sem acesso à
tela). Lido às 23/09 10:43 UTC. Compara contra a primeira rodada
(`APRENDIZADOS-CRM.md`, entrada de 22/09 10:31 UTC, abaixo) e contra
`ESTADO-E-PLANO.md` (leitura de 22/09 19:55 UTC e a medição de 23/09 02:35
dentro dele).

**Números brutos:** 56 contatos, 56 oportunidades (1:1, era 50/50). Por
etapa/status: `NOVO LEAD` **49** `open` · `CONECTAR` 1 `open` + 2 `lost` ·
`NEGOCIAR` 2 `open` + 1 `lost` · `REUNIÃO DE DIAGNÓSTICO` **1** `open` ·
`FORMALIZAR` 0. Os +6 em relação à leitura anterior (50→56) e as primeiras
oportunidades que `CONECTAR`/`REUNIÃO DE DIAGNÓSTICO` já viram são os 6
contatos de teste que o dono criou na madrugada de 22→23/09 testando o
checklist (`Sem Nome`, `O Próximo Cliente`, `Pablo Sampaio` — o 9940 oficial
— `Francisca`, `156766977421470`, `ZZ Teste Porta Inbound`), já
identificados em `ESTADO-E-PLANO.md`.

**Excluindo teste/estrutura da métrica de lead real** (7 contatos com
`source` explicitamente de teste + os 5 acima, com `Francisca` mantida como
questão em aberto, não contada nem excluída): **44 leads reais** (39
`Facebook` + 5 Instagram sem telefone/e-mail). **Todos os 44 continuam em
`NOVO LEAD`** — nenhum lead real jamais chegou a `CONECTAR`,
`REUNIÃO DE DIAGNÓSTICO` ou além; os 4 registros que essas três etapas têm
hoje são 100% contato de teste (`Teste Não Atende`, `Teste Retorno`, `Teste
Número Errado`, `Pablo Sampaio`). **O achado "CONECTAR deixou de ser
sempre-zero" de 22/09 (linha 2240) segue valendo pelo mesmo motivo: é
pipeline sendo exercitado por teste manual, não a esteira ligada.**

**1. A entrada de anúncio piorou de ~25h14 para ~49h27 sem lead novo —
dobrou, não é ruído.** O lead `Facebook` mais novo continua sendo `Carlos
Andrade`, `createdAt` 21/09 09:17:26; às 23/09 10:43 UTC isso são **49h27**
sem nenhum lead pago novo, contra as 25h14 medidas na auditoria de 22/09 e
os ~22h47 da manhã de 22/09 — a régua "pior caso" segue subindo (1,53× →
1,67× → agora **3,27×** o pior caso histórico de 15h06). Nenhuma das 6
oportunidades novas desta janela é de anúncio; todas são teste. **O
Gerenciador de Anúncios continua parado — pendência 4 de `ESTADO-E-PLANO.md`,
sem mudança.**

**2. O lead real mais antigo em `NOVO LEAD` está parado há ~104h (4d8h),
sem dono, sem tag de fila.** É `Andre` (e o lote inteiro carregado em 19/09
02:18 UTC, 33 leads `Facebook` no mesmo segundo) — nenhum tem `assignedTo`
nem tag além de `etapa-novo-lead`/`cad-inbound`. Isso não é regressão: é a
mesma esteira desligada (L-07/G-03) só que 2 dias mais velha. `NOVO LEAD`
segue sem nenhuma das 6 tags de alarme do F-05
(`novo-lead-estagnado`/`fila-travada`/`conectar-estagnado`/
`agendar-estagnado`/`retorno-vencido`/`negociacao-estagnada` — 0 ocorrência
nos 56 contatos, tags seguem `[ ]` em `APROVADO.md`, não existem na tela).
`fila-tel`/`fila-wa` aparecem só em `ZZ TESTE ESTRUTURA` (fixture
permanente com todas as tags por desenho) — nenhum lead real preso em fila
desde ontem, porque nenhum lead real chegou perto de uma fila.

**3. Campo novo criado direto na tela, fora de todo documento:** `Canal que
conectou` (`fieldKey contact.canal_que_conectou`, `id
TxJmoWdkA8rTqC1uEsMW`, `SINGLE_OPTIONS`: `Ligação WhatsApp` · `Ligação
normal` · `Mensagem`), criado 23/09 01:06 UTC — resposta em campo à
pendência 9c de `ESTADO-E-PLANO.md` ("é manual ou automático?"). Nenhum dos
56 contatos tem valor gravado ainda; `grep` em `IMPLEMENTACAO-WORKFLOWS.md`
não encontra o `fieldKey`. Registrar aqui para a próxima rodada não tratar
como órfão nem tentar recriar (mesma regra da tag `teste-regua`, entrada de
22/09).

**4. Preenchimento da régua de qualificação por Meta Lead Ads não mudou:**
`Urgência` 40/56, `Necessidade` 34/56, `Investimento mensal em anúncios`
32/56 — números idênticos aos medidos em `ESTADO-E-PLANO.md` (22/09). O
resto da régua (`Decisor`, `Budget`, `Prazo`, `Tem time comercial`) continua
em ~3 contatos, todos de teste. Nenhum lead real foi qualificado.

**5. `Francisca` (+55 12 98191-3254) segue sem resposta do dono — e agora
está parada há ~35h em `NOVO LEAD`, sem dono.** Pergunta aberta desde
`ESTADO-E-PLANO.md`: é o dono testando ou é lead inbound real? Enquanto não
houver resposta, ela continua fora da contagem de 44 leads reais (por
cautela) e fora da lista de teste conhecida (por não ter confirmação) —
**decisão do dono, não dado que uma auditoria resolve sozinha.**

> **Respondida em 23/09/2026, sessão automática seguinte, sem precisar do
> dono:** `conversations_get-messages` no fio inteiro (não só o nome) diz o
> que nenhuma rodada anterior tinha lido — é conversa pessoal do dono (PIX,
> carona, áudio), nem teste nem lead inbound. Promovida a item de roadmap
> (`G-16`); correção (tirar as tags, `abandoned` na oportunidade) aguarda
> `[x]` em `APROVADO.md`. Detalhe completo no próprio G-16.

**O que ficou saudável e sem mudança:** pipeline com as 5 etapas certas
(`opportunities_get-pipelines` confere nome e ordem, incluindo
`REUNIÃO DE DIAGNÓSTICO` já renomeada), 1:1 contato↔oportunidade mantido,
nenhum telefone/e-mail duplicado, nenhuma tag de alarme falsa disparando.

## `Local Presence Dialing` do HighLevel é US/Canada only — não pesquise de novo para número brasileiro — 23/09/2026, sessão automática

Pesquisando um diferencial de Bloco 6 (o que Outreach/Salesloft/Kixie/Aircall
fazem que este projeto ainda não cobre), `Local Presence Dialing` — escolher
automaticamente, a cada ligação de saída, um número da própria subconta com
o mesmo DDD/área do contato — apareceu como recurso nativo do HighLevel
(`Settings → Phone Numbers → Voice → Other Settings → Outbound Call →
Default Phone Number for Outbound Calls`). Antes de especificar qualquer
coisa em cima disso: **é `US/Canada only`**, confirmado por `WebSearch`
convergente (documentação de suporte da HighLevel e cobertura de
terceiros) — não compra número novo sozinho, e não há sinal de expansão
para número brasileiro. Mesmo formato de descarte já registrado para o
`Voice Integrity` (F-08): recurso real e documentado, mas com o mesmo
limite geográfico. Não gaste `WebSearch` verificando de novo se isso mudou
sem um motivo concreto (ex.: changelog do HighLevel citando Brasil/LatAm).

**O que não tem essa restrição, e por isso virou acréscimo ao F-08 em vez
de bloqueio:** o Web App Softphone do HighLevel deixa o usuário escolher
manualmente, num dropdown "Calling From", qual número da subconta discar
antes de cada ligação — sem restrição de país citada em nenhuma fonte.
Zero custo (mesmos números que o F-08 já recomenda comprar por reputação),
zero engenharia (escolha manual, não workflow). Fechado como linha nova na
tabela do F-08 (`build-wesales.md`, seção 2.26) e instrução em
`GUIA-SDR.md` — não como item de roadmap próprio, porque não tem "Pronto
quando" distinto do que o F-08 já cumpre.

**Regra prática:** ao pesquisar um recurso "central de mercado" (a mesma
pergunta que já fechou F-07/F-08/G-15), checar sempre dois níveis, não um
só — (1) existe algo parecido nesta plataforma? e (2) esse algo cobre o
país desta operação, ou só EUA? — porque a resposta de (1) tende a vir
otimista (documentação de suporte escrita para o mercado majoritário da
HighLevel) e só (2) evita propor uma especificação que nunca vai rodar
aqui, o mesmo erro de categoria que o SHAKEN/STIR do F-08 já cometeu ao
contrário (supôs que não existia versão brasileira sem checar).



## A tag que DISPARA precisa ser tirada por quem tira o lead do fluxo — 23/09/2026, rodada autônoma

`remove_from_workflow` cancela os `Remove Tag` finais do workflow alvo, e pôr
de novo uma tag que o contato **já tem não dispara** o gatilho. Então
`fechar-horario`, `cadencia-12x30-p2` e `cad-outbound` ficavam no contato de
quem agendava e, numa volta futura ao CONECTAR, a cadência não arrancava — em
silêncio. A segunda rede certa é o `Mestre de saída v2` (roda em toda mudança
de etapa além de CONECTAR e em perdido/nutrição): só a lista de tags cresceu.
**Não** pôr "remover das cadências" nele: a própria 12x30 muda a oportunidade
para nutrição no fim, o Mestre dispara e cortaria os nós finais dela.
Medido no 9940: o Espelho troca a tag de etapa em ~4 s depois da mudança; ler o
contato logo em seguida mostra o estado anterior — ler de novo.
## Tag que "vale por um dia": workflow à parte com espera — e tag pela API dispara gatilho — 23/09/2026, rodada autônoma

`conectado-hoje` (F-16) não tinha removedor. Em vez de mexer no Pós-ligação v2
(grande, publicado), um workflow de 2 nós: gatilho "tag adicionada" → espera →
remove. **Medido**: tag posta pela API pública (`POST /contacts/{id}/tags`, MCP
GHL) dispara o gatilho `contact_tag` — saiu 2 min depois na cópia de teste.
Serve para qualquer tag de validade curta. Ao trocar cópia ZZ pela real: cópia
para rascunho ANTES de publicar a real (as duas usariam o mesmo gatilho).
Pouca RAM (136 MB livres): o Claude Code mata processo em segundo plano (até um
`sleep`) — conferir na rodada seguinte em vez de esperar.
## Inserir nó no começo de um ramo: renumerar `order` de TODOS os irmãos — 23/09/2026, rodada autônoma

Nos workflows desta conta, os nós de um ramo têm `parent` = id do ramo e `order`
0, 1, 2…; o encadeamento é `ramo.next` → 1º nó, e `parentKey` do nó = anterior.
Para pôr um nó na frente (NS-1 na Recuperação de No-show): novo nó com
`parent`/`parentKey` = ramo, `next` = antigo 1º, `order` 0; antigo 1º ganha
`parentKey` = novo; e **todos** os irmãos `order += 1` (o patch do A4 só mexeu
num porque o ramo tinha 1 nó). Conferido pela leitura de volta (`tools/ver_wf.py
"Nome"` lista ordem/tipo/pai). Ao importar `patch_funil_reuniao` (que já embrulha
o stdout), não embrulhe de novo — dá "I/O operation on closed file". E rode a
auditoria com `PYTHONIOENCODING=utf-8` (a seta "→" quebra o console cp1252).
## Patch cirúrgico que acrescenta tarefa pode tirar o workflow da regra do fim de semana — 23/09/2026, rodada autônoma

**Medido** pela `auditoria_final.py`: o `Loop do closer v2` nasceu sem janela
(não criava tarefa, só avisava). O patch do A4 inseriu a tarefa
`[CLOSER] Apresentar proposta` e o workflow passou a criar tarefa **sem janela**
— sábado às 22h ela nasceria. Mesma falha no builder novo `build_estagnacao.py`.
Regra: todo builder/patch que põe `task-notification` ou `sms` passa `janela=`
seg–sex 08:30–18:30 (cópias ZZ de teste ficam sem, para rodar na hora); e rodar
a auditoria **depois** de cada patch, não só no fim da obra.
`tools/patch_janela.py "Nome" --aplicar` põe a janela num publicado (mesmo id,
backup em `workflows-json/_antes-janela/`).

Também medido: `[CLOSER] Decidir a negociação` é família CLOSER e vale em
NEGOCIAR; a Faxina (Actions run 35816989927) apagou as duas `Apresentar proposta`
do 9940 (uma por etapa, outra por duplicata) com nota, e manteve a Decidir.
Os alertas de estagnação foram provados em cópias `ZZ TESTE` com esperas de
2 min (`TESTE=1`) — padrão bom para qualquer espera de dias.
## Nenhuma data de marco do funil era gravada — campo DATA não aceita `{{right_now.date}}` — 23/09/2026, rodada autônoma

**Medido** no registro de execução do Loop do closer (teste com o contato 9940):
o passo que grava `Data do veredito do closer` deu **Error**. O valor era
`{{right_now.date}}`, que sai "23/09/2026" (dia/mês/ano) — campo do tipo DATA
recusa. Teste isolado (`ZZ TESTE DATA`): `{{right_now.year}}-{{right_now.month}}-{{right_now.day}}`
grava **2026-09-23** (e mês/dia/ano também).

Estavam quebrados: `Data do veredito do closer` (Loop do closer), `Data agendado`
(Pós-agendamento), `Data compareceu` (Registro de Comparecimento) e `Data
conectado` (Pós-ligação — este gravava VAZIO de propósito, 5 nós). Corrigidos
(`tools/patch_campos_data.py`); a auditoria ganhou a checagem 7. Consequência
que some agora: listas e relatórios de funil por data (entraram/conectaram/
agendaram/compareceram no mês) estavam sem base.

**A4 no mesmo teste:** o closer não recebia tarefa nenhuma; o ramo "Sim" do Loop
agora cria `[CLOSER] Apresentar proposta` (executou no teste).

**Regra:** registro de execução "Executado" não basta — leia cada linha; um
"Error" no meio não para o fluxo e passa despercebido.

## O filtro "canal 20" no gatilho de resposta nunca disparou — e o número oficial de teste é o 9940 — 23/09/2026, sessão do PC

**Medido:** o dono respondeu do 9940 ("Bh", mensagem de ENTRADA na conversa,
`type 20`), e nem a Triagem nem o Opt-out (este sem janela) registraram
execução. O gatilho `customer_reply` com `message.type == 20` **nunca casa**:
20 é o tipo interno da mensagem Stevo, mas o filtro "Canal de resposta" do
gatilho usa outra numeração. A correção de 23/09 (gatilho "— Stevo" com canal
20) estava errada e passou pela conferência porque só confere se o gatilho
existe e está ativo — não se dispara.

**Correção:** o gatilho da Stevo nos 3 workflows de resposta (Triagem, Opt-out,
Interceptação Resposta v2) ficou **sem filtro de canal** ("qualquer canal").
Os três já decidem pelo conteúdo e pelas tags. Republicados (rascunho →
publicado reativa o gatilho).

**Provado com evento real (23/09, 00:19):** nova resposta do 9940 → Triagem entrou (passou "em nutrição?", foi para a espera de 2 min) e o Opt-out rodou e terminou sem agir (não era pedido de parar).

**Regra:** gatilho só está testado quando dispara com um evento real. "Ativo"
e "alvo existe" não provam nada.

**Número oficial de teste (decisão do dono, 23/09/2026):** **+55 21 98742-9940**
(contato "Pablo Sampaio", `rdaijzR0ZVCmXLAJ6jT2`). Use-o em toda rotina de
construção e manutenção que precise mandar ou receber mensagem de verdade.
**Nunca** use o +55 12 98238-1407: é o número CONECTADO à Stevo (telefone da
empresa); mensagem para ele é a empresa falando com ela mesma, e o que se digita
nele aparece como mensagem da conta.

## "Marcado" não é "promovido" — tag sozinha não move etapa, e a frase que descrevia os dois como feitos só tinha feito o primeiro — 23/09/2026, sessão na nuvem

`PLANO-MULTICANAL.md` ("Só inbound", madrugada de 23/09) registrou como
`[x]` uma frase com duas partes: "os 49 leads em `NOVO LEAD` foram
marcados. Promovido para `CONECTAR` → Inbound...". A primeira parte
aconteceu (medido: as 50 oportunidades hoje em `NOVO LEAD` têm a tag
`cad-inbound`). A segunda não: as mesmas 50 seguem abertas em `NOVO LEAD`,
zero com `Entrada em`/`Tentativa nº`, zero com tarefa (`contacts_get-all-
tasks` em 5 amostras, incluindo 3 leads reais). O motivo está escrito no
próprio projeto e ninguém cruzou antes de escrever "promovido": o gatilho
da Cadência Inbound (`IMPLEMENTACAO-WORKFLOWS.md`, W12) é `Opportunity
Stage Changed → CONECTAR`, filtrado por `cad-inbound` presente — ele
escuta a **mudança de etapa**, não a tag. Aplicar a tag a um lead que
continua em `NOVO LEAD` não aciona nada; é o mesmo "gatilho de workflow é
evento, não estado" que este arquivo já registrou em 21/09/2026 (entrada
"Gatilho de workflow é evento..."), agora do lado da tag em vez do lado da
publicação do workflow.

**A regra que fica, generalizável:** quando uma correção mexe em **duas**
coisas que juntas produzem um resultado (aqui: tag decide qual cadência,
etapa decide se alguma cadência roda), marcar as duas como `[x]` na mesma
frase exige medir as duas — medir só a mais fácil (a tag, que aparece na
lista de tags do contato) e escrever a frase como se a mais difícil
(mudança de etapa em massa, que precisa de `opportunities_search-
opportunity`, não de `contacts_get-contacts`) também tivesse acontecido é
o mesmo erro que o G-08 já registrou ("achado escrito não é aplicado
sozinho"), aqui na direção oposta: não é uma correção que ficou só no
texto, é um resultado que o texto descreve como obtido e a conta desmente.
**Antes de marcar `[x]` uma frase com verbo composto ("marcado e
promovido", "corrigido e publicado"), medir cada verbo separado — o
`[x]` vale para a frase inteira, não para a parte que foi medida.**

Sem mudança no CRM por esta sessão: mover as 50 oportunidades é a mesma
decisão que G-03 já represa há dias (regra 2 do briefing — ação em massa
em dado de produção pede confirmação do dono antes). Detalhe completo,
com os números e a amostra, em `ROADMAP-SALES-ENGAGEMENT.md` (G-03) e
`PLANO-MULTICANAL.md` (nota na linha "Só inbound").

## Mensagem automática testada com número real — e dois merge fields que saíam errados — 23/09/2026, sessão do PC

Teste com o número do dono (+55 12 98238-1407; a conta Stevo é outro número,
final 1497): o nó `sms` de um workflow saiu **entregue como WhatsApp pela
Stevo** (`type 20`, `TYPE_CUSTOM_SMS`, `from: stevo`). O canal está provado.

O mesmo teste pegou dois textos quebrados, que nenhuma validação estrutural
pegaria:
- `{{user.first_name}}` saiu **vazio** ("aqui é o  da…") — na automação nem
  sempre há usuário no contexto;
- `{{location.name}}` saiu **"Pablo Santos's Account"** — é o nome interno da
  conta, não a marca.

Corrigido em todas as mensagens publicadas e nos builders
(`tools/patch_textos_marca.py`): "aqui é da O Próximo Cliente". **Regra:** em
mensagem automática, use só merge field do CONTATO; marca e remetente vão fixos
no texto. Mensagem de automação só está testada depois de ser lida no celular.

## Fato certo, implicação errada: procurei o mecanismo no workflow que tem o nome dele — 23/09/2026, sessão na nuvem

Eu li o `Monitor de Capacidade`, vi que é **1 nó de `internal_notification`**, e
concluí — na §2.29 e em várias rodadas de check-in — que "avisa, não represa", ou
seja, que a regra de capacidade da D14 não é aplicada. O fato estava certo. A
implicação estava errada, e o motivo é bobo: **procurei o mecanismo no workflow que
tem "Capacidade" no nome.** Ele está em dois lugares que eu não abri:

- `faxina_tarefas.py` (197-213): conta, por SDR, vencidas e toques de hoje, e liga
  a tag `sdr-lotado` nos leads em `CONECTAR` daquele SDR;
- `Cadência 12x30` parte 1 e parte 2: **6 nós cada** condicionando em `sdr-lotado` —
  o laço de espera de 1 h que efetivamente represa.

**A regra:** quando um documento descreve um mecanismo e um workflow tem o nome
dele, não presumir que o nome é o lugar. Mecanismo de controle quase sempre mora em
**dois** pontos — quem mede e quem obedece — e o que tem o nome bonito costuma ser
quem mede. Procurar a tag, não o título.

**E foi essa correção que destravou o achado real:** comparando os três lugares,
`Cadência 12x30` tem 6 nós de portão, a parte 2 tem 6, e a **`Cadência Inbound` tem
0**. A Faxina põe `sdr-lotado` inclusive nos leads inbound, e a Inbound não lê a
tag — **o freio está engatado e a roda que gira não está ligada nele**. E é a
Inbound que carrega os 49 leads do "só inbound". O `GUIA-SDR.md` promete o teto ao
SDR sem ressalva.

Segunda correção da mesma rodada, mesma família: eu havia escrito que
`Canal que conectou` "existe e ninguém escreve nele, logo a pergunta nunca terá
resposta". Ninguém escreve **por workflow** — e o `GUIA-SDR.md` instrui o SDR a
preencher na tela, junto com `Resultado da tentativa`. A D10 diz "marcado junto com
o resultado", e quem marca o resultado é o humano. **Eu li "junto com o resultado"
como "o workflow grava junto" porque era a leitura que confirmava meu achado.**
Deixou de ser lacuna e voltou a ser decisão.

O padrão das duas: **eu concluí a partir da ausência de automação, sem procurar a
presença de instrução humana.** Neste projeto metade do mecanismo é gente — o SDR
marca resultado, move etapa, preenche canal. Auditoria que só lê workflow vê metade
da máquina e acha que a outra metade não existe.

## Cobertura por lista fixa parece varredura e não é — `ALVOS` no `patch_condicoes_etapa.py` — 23/09/2026, sessão na nuvem

Auditei os quatro monitores do F-05 de propósito: são os dumps mais velhos que eu
tenho (28 h), e é aí que o cuidado tem de ser maior, não menor. Dois deles testam
etapa de oportunidade — o mesmo padrão do G-13 — e nenhum dos dois está em
`_antes-patch-condicoes/`.

**E o candidato não virou achado, o que é a regra desta noite funcionando.** Se os
dois tivessem condição de oportunidade com gatilho que não é de oportunidade, a
`auditoria_final.py` do dono — que lê a API **inclusive o gatilho** — teria acusado,
e ela reportou 0 problemas. **Fonte ao vivo vence dump de 28 h.** Registrei como
candidato e parei ali, em vez de levar o quinto dado velho para a fila dele.

**O que sobrou é certo porque está no código, não no estado:** o
`patch_condicoes_etapa.py` tem duas lacunas.

1. **`ALVOS` é lista fixa de 10 nomes.** Quem não está na lista nunca foi
   examinado. A cobertura do patch é uma **lista**, não uma varredura — e uma lista
   de nomes num script *parece* varredura quando você lê o resultado ("10 workflows
   corrigidos") em vez de ler o código.
2. **O tradutor cobre 3 dos 5 estados:** `CONECTAR`, `REUNIÃO DE DIAGNÓSTICO` e
   `abandoned`. Não há entrada para `NOVO LEAD`, `NEGOCIAR` nem `FORMALIZAR`, mesmo
   o Espelho produzindo as três tags. Workflow que teste essas etapas volta do
   patch **inalterado e sem aviso**, porque `traduz()` devolve `None`.

**A regra:** ferramenta de conserto com alvo hardcoded precisa da varredura do lado
— e a varredura é que manda. Quando as duas existem (aqui: patch por lista +
`auditoria_final.py` por API), o número que vale é o da varredura, nunca o "N
corrigidos" do patch. E tradutor que devolve `None` silenciosamente deveria
**listar o que não soube traduzir**: é a diferença entre "não havia o que fazer" e
"não soube o que fazer", e as duas saem iguais no terminal.

## A guarda de frescor era cega para dump sem irmão — e havia um `published` velho de 28 h — 23/09/2026, sessão na nuvem

Conferindo o G-13 do dono achei o caso que a minha própria guarda não pegava:
`workflows-json/AGENDAR Estagnado.json` diz `status: published` com `updatedAt` de
**22/09 00:45**, e o commit `23db864` do dono (23/09 ~01:47) diz no assunto "**W17d
despublicado**". O dump está 28 h atrás da conta e afirma o contrário do estado
real. Ele não tem backup `_antes-*`, e a guarda da entrada anterior só compara com
irmão — imprimiu 0.

**Segunda guarda, heurística e rotulada como tal:** compara o `updatedAt` de cada
dump com o **mais novo da pasta** e lista os que estão 12 h ou mais atrás. Não prova
defasagem (workflow que ninguém tocou há dias aparece, e é correto que apareça); o
que ela faz é nomear o que precisa de **confirmação ao vivo antes de virar item**.
Hoje lista 7 — e **quatro são os monitores do F-05**, justamente a parte da máquina
sobre a qual eu tenho menos informação fresca.

**A regra que fecha a série:** guarda contra dado velho não pode depender de o dado
velho ter um par. A primeira versão só via defasagem quando existia um backup irmão
para comparar — ou seja, funcionava exatamente nos casos em que alguém já tinha se
dado o trabalho de fazer backup, e falhava em silêncio nos outros. Guarda que só
funciona quando o ambiente colabora não é guarda.

E um bug meu no caminho, pego só porque rodei com `| head` e vi o traceback: as duas
guardas usavam `nome` como variável de laço, sombreando a lambda `nome()` que resolve
id → nome. A auditoria morria com `'str' object is not callable` **depois** de
imprimir os avisos — falhava na parte que importa, com um cabeçalho bonito dando a
impressão de sucesso. Em script de relatório, variável de laço não pode colidir com
função auxiliar; e rodar o script **inteiro**, não só o cabeçalho, antes de confiar
nele.

## Classifiquei cinco contatos por nome e acertei um — o telefone é que diz o que a coisa é — 23/09/2026, sessão na nuvem

Eu disse que cinco oportunidades eram "teste sem marcação, indistinguíveis de lead",
e que o A9 do dono perdia justamente essas cinco. Fui conferir contato por contato
pelo MCP. **Errado nos dois pontos:**

| Nome | Telefone / e-mail | O que é de verdade |
|---|---|---|
| `Pablo Sampaio` | +5521987429940 | **o 9940**, número oficial de teste — o A9 **já nomeia** |
| `O Próximo Cliente` | +5512982381407 | **o 1407**, o conectado à Stevo, citado no `692c504` |
| `Sem Nome` | `agencia.proximocliente@gmail.com` | **a própria agência** |
| `156766977421470` | +18005551470 (800 dos EUA), nome = id de plataforma | artefato sintético |
| `Francisca` | +5512981913254 | **não consigo classificar** |

Quatro dos cinco são do próprio projeto, e dois deles o dono já rastreava. Eu havia
classificado pelo **nome** — "Pablo Sampaio parece o dono, logo é teste dele" acertou
por acidente; "Francisca parece pessoa, logo é teste também" não tem base nenhuma.
**O telefone é que diz o que a coisa é**, e eu não tinha olhado: um 800 dos EUA com
`country: BR`, o e-mail da própria agência, os dois números de teste do projeto.

**E a conclusão vira do avesso.** O que sobra é menor e mais urgente do que eu disse:
só a `Francisca`. Se ela é pessoa de verdade que escreveu no WhatsApp, **é lead
inbound parado `open` em NOVO LEAD sem dono** desde 22/09 23:34 — não é "teste sem
marcação", é o risco **contrário**, e pior. Item virou uma pergunta de uma linha em
vez de uma limpeza de cinco.

**As duas regras:** (1) para classificar contato, ler o **identificador** (telefone,
e-mail, id), nunca o nome — nome é o campo mais fácil de encher de qualquer coisa;
(2) antes de dizer que o backlog do dono "perdeu" um item, conferir se ele não está
lá com outro nome — o 9940 estava no A9 desde o começo, e eu li o A9.

## Levei dado velho ao dono duas vezes — 3 dos 5 achados já estavam resolvidos quando reportei — 23/09/2026, sessão na nuvem

A pior da noite, e não é erro de raciocínio: é erro de **fonte**, o terceiro da
mesma família, agora com consequência na fila do dono.

| Quando | O que |
|---|---|
| 22/09 16:27 | `updatedAt` do dump de `Mestre de saída v2` que eu auditava |
| 23/09 03:24 | `Triagem da Nutrição` **publicada** (remove `cad-inbound`, `nutricao-90d`) |
| 23/09 04:35 e 04:55 | **eu reportei 5 achados como abertos** |
| 23/09 05:05 | dono re-exportou os dumps; a auditoria foi a **0** |

Três das cinco linhas já estavam resolvidas **uma hora antes** de eu reportá-las. O
dump dizia `draft` na `Triagem` porque foi exportado antes da publicação. As outras
duas eu não consigo datar, então não afirmo nada sobre elas. Custo: as pendências 9a
e 9b do `ESTADO-E-PLANO.md`, apresentadas como trabalho a fazer, eram trabalho
feito. Nenhuma escrita errada no CRM — só ruído na fila dele, que é o oposto do que
auditoria deveria produzir.

**Conserto na ferramenta, não no texto.** `auditoria_tags.py` ganhou **guarda de
frescor**: para cada dump, compara o `updatedAt` dele com o do backup `_antes-*`
mais novo do mesmo workflow. Backup mais novo que o principal = o arquivo não foi
re-exportado depois de um patch → imprime aviso em bloco dizendo que qualquer
achado daquele workflow pode já estar resolvido. Hoje o aviso não aparece (dumps
frescos), mas teria aparecido ontem e eu não teria reportado nada como aberto.

**A regra, agora com três instâncias e uma consequência real:** esta família de
auditoria lê **fotografia**, e fotografia deste repositório envelhece em **minutos**
quando alguém está trabalhando na conta. Achado tirado de dump não é item para o
dono — é **candidato**. Vira item depois de confirmação ao vivo: `auditoria_final.py`
(que lê a API, precisa do PC) ou medição de efeito pelo MCP, que é o que eu tenho da
nuvem. Quando não houver nenhuma das duas, reportar como "o dump diz X, não
confirmado ao vivo", nunca como estado.

E a assimetria que fecha o assunto: nas três instâncias eu errei para o lado de
**afirmar que algo estava quebrado**. Um alarme falso custa a atenção do dono; o
silêncio custaria um defeito no ar. Então o viés a manter é o do alarme — mas com o
rótulo certo: **candidato, não item**.

## Duplicata de workflow com temporizador: o risco não é disparar duas vezes, é a espera mais curta ganhar — 23/09/2026, sessão na nuvem

Anotação curta, de uma coisa que eu ia descrever errado. O item A7 diz para tirar a
cópia `ZZ TESTE Limpa conectado-hoje` antes de publicar a real, e eu repeti o motivo
como "senão as duas disparam". Disparar as duas é **inofensivo**: as duas removem a
**mesma** tag, e remover tag ausente é no-op.

O risco real é outro, e é sério: **a espera mais curta ganha.** A cópia ZZ espera 2
minutos e a real espera 1 dia. Com as duas no ar, a tag sai em 2 minutos, e o lead
volta para a fila do dia minutos depois de ter sido conectado — exatamente o
contrário do que o removedor existe para fazer. A janela não duplica, ela encolhe de
1440 para 2 minutos.

**A regra, que generaliza para qualquer par original/cópia-de-teste com
temporizador:** duplicata de workflow que só difere no tempo de espera não é
redundância, é um **encurtador** do prazo. Antes de publicar o original, conferir que
a cópia curta está desligada — e conferir **por efeito**, não pelo `status` do dump
(que é a afirmação mais frágil do arquivo): aplicar a tag num contato de teste e ver
se ela sobrevive ao prazo curto. No caso concreto não houve problema — o dono deixou
a ZZ em rascunho e publicou só a real — mas a razão certa ficou registrada.

## O dono resolveu o F-16 melhor do que eu havia recomendado — tirar a cláusula vence consertar a cláusula — 23/09/2026, sessão na nuvem

Eu recomendei a saída A para o F-16: dar a `conectado-hoje` o reset que o nome
dela promete (`Wait 24h` → `Remove Tag`, dentro do `Pós-ligação v2`). O dono fez
duas coisas, e as duas são melhores:

1. **Em workflow à parte** (`tag adicionada → espera 1 dia → remove`,
   `allowMultiple: true`) em vez de dentro do `Pós-ligação v2`. Não acrescenta
   cinco ramos de `Wait` num workflow de 130 nós, e a re-entrada fica explícita em
   vez de implícita. Conferi por medição que funciona: a cópia ZZ (espera 2 min)
   tirou a tag do contato de teste.
2. **E uma saída que eu não tinha visto:** `Fila Telefone Hoje = fila-tel +
   etapa-conectar`, **sem `conectado-hoje` na lista** — porque a 12x30 põe e tira
   `fila-tel` a cada toque (conferido nos nós: adiciona em 48/108/161/214/274/327,
   remove em 64/117/170/230/283/336). Se `fila-tel` só existe enquanto a tentativa
   está liberada, ele já carrega a informação que a cláusula `não conectado-hoje`
   tentava dar.

**A lição, e ela é sobre como eu penso:** eu tratei o sintoma — a tag não expirava,
então fiz a tag expirar. Ele tirou a cláusula da equação. Numa conjunção de filtro,
**remover uma cláusula é estruturalmente mais forte que consertar uma cláusula**,
porque cláusula que não existe não pode virar dependência escondida quando a
vizinha mudar — que é *exatamente* o mecanismo do F-16 que eu mesmo descrevi. Eu
tinha o diagnóstico certo e parei uma casa antes da conclusão.

Regra: diante de uma cláusula redundante que virou perigosa, perguntar **"esta
cláusula precisa existir?"** antes de **"como faço ela funcionar?"**. As duas
juntas são o ideal (a tag passa a expirar, por higiene de estado, **e** a lista
deixa de depender dela), mas a ordem de preferência é tirar antes de consertar.

## Campo que existe e ninguém escreve: o multicanal não vai saber qual canal funcionou — e um mapa que de propósito não falha — 23/09/2026, sessão na nuvem

O `d880870` conta que o dono achou **à mão** "4 campos de data que nunca
gravavam". Pergunta boa demais para depender de alguém topar com ela, então
virou `wesales/tools/auditoria_campos.py`: para cada campo personalizado de
contato, quem escreve e quem lê, entre os publicados.

**Achado:** `Canal que conectou` **existe e nenhum workflow escreve nele** — o
id `TxJmoWdkA8rTqC1uEsMW` não aparece em nenhum dos 33 dumps. A D10 do
`PLANO-MULTICANAL.md` diz que ele deve ser "marcado junto com o resultado", e
quem marca o resultado é o `Pós-ligação v2`, publicado, que não grava este
campo. Consequência: a pergunta que o multicanal existe para responder — *qual
canal conectou?* — nunca vai ter resposta, e a decisão D6 (WhatsApp primeiro,
ligação normal na segunda, troca depois de 3 não atendidas) fica sem dado para
ser avaliada. O projeto vai poder dizer que trocou de canal, não qual funcionou.

**E a decisão de design da ferramenta, que é a parte reaproveitável: ela sai
sempre com 0.** Não é descuido — das 56 colunas, 36 caem em duas categorias
inteiramente intencionais:

- **"só lido, ninguém escreve" (23)** é o normal dos campos de qualificação:
  `Budget`, `Decisor`, `Dor principal`, `Segmento`, `Urgência`, `Motivo da
  desqualificação`, `Reunião foi qualificada` são preenchidos pelo SDR ou pelo
  closer **na tela**. Workflow lê o que o humano classificou.
- **"só escrito, ninguém lê" (13)** quase sempre quer dizer "a **lista** que
  leria ainda não existe". `Prioridade`, `Tentativas telefone`, `Conexões
  telefone` existem para ordenar e mostrar nas listas inteligentes, e **lista
  inteligente não aparece em nenhum dump**. O script não vê listas, logo não
  pode chamar isso de órfão — e essa coluna é, na prática, a checklist do que o
  A7 vai consumir.

Sobra **uma** coluna que vale olhar (4 campos), e mesmo nela só 1 era lacuna: os
outros 3 estão declarados em `campos-e-tags.md` como "especificado, falta
montar" (`Hora da conexão`, `Hora do retorno`) ou como duplicata de desenho
antigo (`Necessidade`).

**A regra:** quando a maior parte do resultado de uma checagem é intencional,
ela é **mapa**, não alarme — e deve dizer isso no próprio código de saída, não
só no texto. Auditoria que falha em 36 linhas esperadas ensina a ignorar as 4
que importam. As duas outras auditorias deste projeto falham (exit 1) porque
**toda** linha que elas listam é defeito; esta não falha porque não é.

E um detalhe de ferramenta que vale em qualquer script de relatório: sem guarda
de `BrokenPipeError`, `python3 auditoria_campos.py | head` morre com traceback e
`exit=1` — que parece exatamente a falha de auditoria que o script existe para
não causar. Guarda posta.

## A fila autônoma do dono passava ao lado de três coisas já medidas — cruzar backlog novo com achados abertos — 23/09/2026, sessão na nuvem

O `e52d55f` criou uma fila autônoma A1–A9 para o ciclo de 15 min. Boa fila. Três
itens dela iam andar em cima de coisa que já estava medida e registrada em outro
arquivo — é o G-10 outra vez (duas trilhas que param de se ver), agora entre o
backlog novo e os achados da noite.

| Item | O que ele ia fazer | O que já estava medido |
|---|---|---|
| **A7** montar as listas inteligentes | trocar a cláusula de etapa por tag `etapa-*` | o filtro tem **duas** cláusulas, e a outra é `não conectado-hoje`, que **nada remove**. Montar a lista como está especificada entrega o vazamento do F-16 pronto. A7 depende da pendência 2 |
| **A8** rodar a auditoria completa | só `auditoria_final.py` | ela não faz as duas perguntas do `auditoria_tags.py`, que hoje devolve 5 achados — e 3 saem publicando a `Triagem da Nutrição` |
| **A9** limpeza de testes | 9940, `ZZ TESTE MENSAGEM`, `ZZ Teste Porta Inbound` | **faltam as cinco que dão problema**: `Sem Nome`, `O Próximo Cliente`, `Pablo Sampaio`, `Francisca`, `156766977421470` — sem `source` e sem `ZZ`. As que o A9 lista já estão marcadas e por isso são as fáceis |

**A regra:** quando aparece backlog novo num arquivo, cruzar cada item com os
achados abertos **antes** de deixar a fila andar — e escrever a nota **dentro do
item**, não num documento vizinho. Nota ao lado do `[ ]` viaja com quem for
executar; nota em outro arquivo depende de a pessoa lembrar de abrir os dois. Foi
assim que registrei, sem tocar em nenhum `[ ]`: o dono continua dono da fila dele.

**O padrão por trás dos três:** os itens não estavam errados, estavam **incompletos
de um jeito que parece completo**. "Limpeza de testes" parece cobrir os testes;
cobre os que têm marcação. "Auditoria completa" parece cobrir a auditoria; cobre a
que está citada. Item de backlog que nomeia a categoria e lista os exemplos vira
checklist dos exemplos — e o que ficou de fora fica invisível justamente porque a
categoria diz que foi coberto.

## `git grep` numa branch não responde "existe workflow do Actions para isto?" — segundo erro de fonte no mesmo dia — 23/09/2026, sessão na nuvem

Eu afirmei, e commitei, que "nenhum workflow do Actions usa `GHL_TOKEN`", apoiado
em `git grep -ln 'GHL_TOKEN' .github/`. O grep é verdadeiro e a conclusão é falsa:
ele vê **só a branch em que eu estou**. O `faxina-tarefas.yml` existe desde
23/09 00:12, está `active` e já rodou 2× com sucesso — mora em outra branch.

**A regra:** workflow agendado roda a partir da branch onde o arquivo está, não da
branch de trabalho. Para responder "existe workflow do Actions para isto?", a
fonte é a **API do Actions** (`list_workflows`), nunca `git grep` na branch local.

É o segundo erro de fonte no mesmo dia, com a mesma forma: no F-17 eu confirmei
fora do dump e não fora do **tempo** (dump de 4 segundos antes); aqui confirmei
fora do dump e não fora da **branch**. A lição comum, mais forte que as duas:
**antes de afirmar que algo não existe, perguntar "qual é o escopo do que eu
olhei?"** — um arquivo, uma branch, um instante. Ausência dentro de um escopo
estreito não é ausência.

**E quando fui olhar direito, o achado real estava no conteúdo, não na existência.**
O workflow tem dois `cron` e em Actions eles somam: `*/10 11-22 * * 1-5` mais
`0 * * * *` dá **84 execuções por dia útil** e **24 por dia no fim de semana**,
contra as 12 em dia útil e 0 no fim de semana que o `rotina-limpar-tarefas.md`
especifica. 7× na janela, e roda de madrugada e no sábado, onde o documento diz
explicitamente que não há tarefa nascendo nem SDR trabalhando.

Por que importa além do custo de minuto: a proteção contra corrida com o workflow
do GHL é a **carência de 5 minutos**. Desenhada para cadência horária, 5 min é
folga; com execução a cada 10 min, cobre metade do intervalo. O teto de 200 por
execução e a trava de "mais da metade das tarefas abertas" continuam de pé, então
não é destruição — é margem de segurança que encolheu sem ninguém decidir.
**Regra:** ao mudar a cadência de uma rotina, reler as proteções que foram
dimensionadas para a cadência antiga. Carência, teto e janela são todos relativos
ao intervalo.

E um detalhe frágil do mesmo arquivo: o `checkout` está pinado em
`ref: claude/amazing-johnson-mclksg`. Quando o PR for mesclado e a branch apagada,
o workflow quebra sozinho, de madrugada, sem ninguém olhando.

## Minha auditoria contava rascunho como rede de segurança — errar para o lado permissivo é o pior jeito de errar — 23/09/2026, sessão na nuvem

Duas correções no `auditoria_tags.py` que eu escrevi uma hora antes, e a segunda
era defeito de verdade.

**1. Julgamento sobre tag vence quando o papel da tag muda.** Eu havia excluído
`cad-inbound` da pergunta 1 raciocinando "marcador de origem que persiste não é
defeito". No `bff2514` o **nó 0 da `Cadência Inbound` passou a ser um `if_else`
que testa `cad-inbound`** — a tag virou o **portão** da cadência, e o nó 254 a
remove na saída. Portão cuja remoção é pulada deixa o portão aberto. É o F-16
outra vez, agora contra uma exceção que eu mesmo tinha codificado: **exceção em
auditoria precisa de data e de motivo, porque o motivo expira.** Deixei o
comentário no script dizendo quando saiu e por quê.

**2. O script creditava workflow em `draft` como rede de segurança.** Foi assim
que ele parou de acusar `nutricao-90d` e `cad-inbound`: quem as limpa sem ser
arrancado é a `Triagem da Nutrição`, em rascunho. Hoje **nada publicado remove
`nutricao-90d`**. O efeito foi a auditoria ficar **permissiva**, e isso é pior que
um alarme falso: alarme falso a gente investiga e descarta; silêncio a gente
acredita. Corrigido — a rede tem de estar `published`, e o relatório passou a
dizer qual rascunho viraria rede.

**A assimetria que fica, e que vale para qualquer checagem:** `draft` num dump não
serve para **acusar** (armadilha do F-17, que me custou um achado inteiro), mas
serve para **não creditar** uma proteção. As duas direções não são simétricas —
na dúvida, não credite; nunca acuse.

Resultado: de 3 achados para 5, e agora com o caminho barato visível — **publicar
a `Triagem da Nutrição` fecha 3 dos 5**.

**E uma reconciliação, porque duas auditorias dizendo coisas diferentes confundem
mais que uma só:** o `auditoria_final.py` do dono (`beebd23`) diz "26 publicados,
0 problemas" e está certo — ele faz **seis** perguntas, nenhuma delas é a minha. O
cruzamento completo está na §2.33.1 do `build-wesales.md`. A dele ainda tem uma
vantagem que a minha não tem: lê **ao vivo pela API**, inclusive o gatilho, então
não sofre da defasagem de dump e vê o dado que falta para fechar minha pergunta 1
com certeza. Caminho de melhoria registrado: unir as perguntas na fonte ao vivo,
quando alguém estiver no PC.

## Teste que cria oportunidade deixa pegada indistinguível de lead — e uma pendência fechada por medição em vez de por tela — 23/09/2026, sessão na nuvem

Check-in das 02:29. Nada novo no git, todos os gabaritos batendo — e a medição do
CRM mostrou duas coisas que nenhum commit contava.

**1. O `Espelho de Etapa` etiqueta o ACERVO, não só mudança futura.** Essa era a
pergunta que eu tinha registrado como "só a tela responde". Respondida sem tela:
das **53 oportunidades `open`, 53 carregam a tag de etapa certa**, 0 sem tag, 0
divergente — incluindo as criadas em 20 e 21/09, antes da publicação. **A regra:**
antes de mandar o dono conferir na tela, ver se a consequência é mensurável pela
API. Tag no contato é mensurável; gatilho não é. Eu quase gastei uma pendência do
dono numa coisa que eu mesmo podia medir.

**2. Cinco oportunidades nascidas de teste estão indistinguíveis de lead.** A
validação do multicanal de ontem à noite (22:34–00:45) criou contato e
oportunidade `open` em `NOVO LEAD` para `Sem Nome`, `O Próximo Cliente`,
`Pablo Sampaio`, `Francisca` e `156766977421470` — **sem `source` e sem prefixo
`ZZ`**, que é a convenção do projeto para marcar teste. Se a esteira ligar assim,
a máquina liga para o dono e para a própria agência.

Duas consequências práticas:
- **A base mudou de composição e o número que eu repetia estava velho.** Eu
  carregava "39 leads reais"; são **37** de `source: Facebook` mais 5 de Instagram
  sem telefone, e os 5 de teste por cima. Número repetido entre rodadas envelhece
  — a mesma regra de "número fixo só na fonte" vale para número que eu carrego no
  prompt de check-in.
- **Teste que escreve no funil precisa da marcação na hora de escrever**, não
  depois: `ZZ` no nome e `source` dizendo que é teste. Sem isso, o teste de hoje
  vira lead de amanhã, e quem descobre é o SDR ligando para o dono. Os 3 testes
  antigos (`ZZ Teste Porta Inbound`, `ZZ TESTE ESTRUTURA`, `Teste Não Ligar`) foram
  feitos assim e não dão trabalho nenhum — a convenção funciona quando é usada.

## `testpaths = ["tests"]` encerra a conferência de CI commit por commit — e duas coisas que saíram de varrer um commit de token — 23/09/2026, sessão na nuvem

**CI, a razão definitiva.** Eu vinha provando "o CI não mudou" commit a commit
com dois argumentos fracos (nenhum teste faz `grep` de `wesales/`; o diff só
toca `wesales/`). O argumento forte está no `pyproject.toml`:
`[tool.pytest.ini_options] testpaths = ["tests"]`. **Pytest só coleta de
`tests/`.** Logo commit que toca apenas `wesales/` não pode alterar o resultado
da suíte — nem markdown, nem script novo em `wesales/tools/`. A conferência vira
uma linha: `git -c core.quotePath=false diff --name-only <base>..HEAD | grep -v
'^wesales/'`; vazio = está provado. Vale também para não perder rodada lendo log
do MCP, que vem truncado e às vezes não traz a linha de resumo.

**Varrer commit que mexe em credencial vale sempre, e desta vez achou duas
coisas.** O `0aebc38` criou uma integração privada e guardou o token num segredo
do GitHub. Nada vazou (nenhum token no diff, nenhum `pit-`/JWT versionado em
`wesales/`, prints do `criar_pit.js` vão para `wesales/.local/`, que está no
`.gitignore`, e o token sai só por `stdout` para o `gh secret set`). Mas a
varredura mostrou duas coisas que ninguém estava olhando:

1. **Segredo guardado, sem consumidor.** `git grep -ln 'GHL_TOKEN' .github/`
   volta vazio: nenhum workflow do Actions usa o segredo, e nenhum toca
   `wesales/`. A Faxina tem duas encarnações (prompt de rotina e script Python)
   e nenhuma das duas está agendada de fato.
2. **O PIT antigo não tem consumidor automatizado neste repositório.** Isso
   transforma "rotação recomendada, nunca confirmada" — pendência aberta há dias
   — em um clique sem risco: `ghl_api.py` usa o bearer interno, a Faxina usa o
   `GHL_TOKEN` novo, `conectar.md` só documenta a receita com variável. **A regra
   que fica:** antes de tratar rotação de credencial como tarefa arriscada,
   procurar quem a consome. Sem consumidor, o risco é zero e a pendência para de
   ser pendência. E declarar o limite: "nenhum consumidor **aqui**" não é
   "nenhum consumidor", porque integração fora do repositório eu não vejo.

## Checagem à mão que achou defeito duas vezes vira script, não vira parágrafo — `auditoria_tags.py` — 23/09/2026, sessão na nuvem

As duas varreduras de tag desta noite acharam coisa real (a limpeza de
`fechar-horario` pulada, e a ordem produtor/consumidor). Eu ia deixar o heredoc
escrito num documento; heredoc em markdown não roda. Virou
`wesales/tools/auditoria_tags.py`, ao lado do `auditoria_refs.py`, e na primeira
execução limpa achou **uma terceira coisa** que eu não estava procurando:
`fila-wa` é removida em 75 nós e aplicada em nenhum.

**Duas lições sobre escrever a auditoria, e as duas nasceram de alarme falso meu
no primeiro rascunho do script:**

1. **"Segunda rede" não se identifica por nome.** Eu tinha escrito a regra como
   "o Mestre de saída também limpa?" e o script acusou o `toque`, que é limpo
   pelo `Contador de Toques` — rede perfeitamente legítima. A regra certa é
   estrutural: *existe algum removedor que ninguém arranca?* Se existe, a limpeza
   dele sempre roda. Isso derrubou 4 dos 7 alarmes.
2. **Auditoria precisa conhecer as exceções de projeto.** `pausado` é aplicada à
   mão pelo SDR e `cad-inbound` vem da integração na entrada
   (`IMPLEMENTACAO-WORKFLOWS.md`, tabela das três famílias). Sem essa lista, o
   script acusa as duas como "ninguém aplica" e como "limpeza pulada" — e
   marcador de origem que persiste não é defeito, é o ponto dele.

**Regra geral:** auditoria que grita sobre o que é intencional treina a gente a
ignorar auditoria. Antes de fixar uma checagem, rodar, olhar cada linha do
resultado e perguntar "isto é defeito ou é o desenho?" — e codificar a resposta
no script, com comentário dizendo de onde veio a exceção. O `auditoria_tags.py`
saiu de 7 alarmes para 3, e os 3 são reais.

**A pergunta 2 do script nunca muda o código de saída**, de propósito: foi lendo
`status: draft` que eu errei o F-17. Checagem cuja fonte é frágil deve reportar
pergunta, não falha.

## Produtor em rascunho + consumidor publicado = defeito ativo e silencioso — três casos em uma noite — 23/09/2026, sessão na nuvem

Padrão que apareceu três vezes na mesma noite e merece checagem fixa. Quando um
workflow **publicado** depende de um estado (tag) que só um workflow em
**rascunho** produz, a condição lê o estado ausente e desce pelo ramo errado.
**Nenhum erro aparece** — é o pior formato possível.

| Caso | Produtor | Consumidor | Situação |
|---|---|---|---|
| `fechar-horario` | `Pós-ligação v2` aplicava (publicado) | `Fechar Horário` removia e era gatilhado pela tag (rascunho) | fechado pelo dono no mesmo dia, janela limpa |
| ~~8 tags do **Espelho de Etapa**~~ | ~~`Espelho de Etapa` (rascunho)~~ | ~~8 workflows publicados~~ | **ERRO MEU — retirado.** O dump dizia `draft` às 01:53:09; a conta publicou às 01:53:13. Nunca existiu na conta |
| limpeza de tag | workflow no ar aplica | limpeza mora em workflow em rascunho | mesma família |

**O caso do espelho eu inventei, e a lição está aí.** Li `status: draft` num dump
exportado quatro segundos antes da publicação e registrei um defeito que a conta
nunca teve. Tinha acabado de escrever, no commit anterior, a regra de comparar o
dump com o backup irmão — e não a apliquei. E a regra, como eu a escrevi, também
não teria salvado: o `Espelho de Etapa` é **novo** e não tem backup irmão, e eu
li ausência de backup como sinal de frescor.

**Segunda perna da regra, que faltava: dump sem backup irmão não é por isso
recente.** E mais específico: `status: draft` é o estado natural de um workflow
nos segundos entre montar e publicar — que é exatamente a janela em que os
scripts de `wesales/tools/` exportam. Então **`draft` num dump é a afirmação mais
frágil do arquivo inteiro**, e nunca deve virar achado sozinho. Antes de
registrar: comparar o `updatedAt` do dump com o horário do commit que o trouxe, e
confirmar por fonte que não seja o arquivo — a tela, ou a medição ao vivo do
efeito (contatos com a tag). Sem isso existe uma pergunta, não um defeito.

O caso `fechar-horario` (§2.31.1) continua válido porque ali eu confirmei ao
vivo, contando contatos com a tag, em vez de só ler o `status`.

**A checagem, barata e para entrar em toda rodada** — para cada tag citada em
condição de workflow publicado, achar quem aplica e olhar o `status` de quem
aplica:

```
cd wesales/workflows-json && python3 - <<'EOF'
import json,glob
from collections import defaultdict
TAGS={'etapa-conectar','etapa-reuniao','status-nutricao'}   # as que interessam
aplica=defaultdict(list); testa=defaultdict(list)
for f in sorted(glob.glob("*.json")):
    w=json.load(open(f)).get('workflow') or json.load(open(f))
    for i,t in enumerate(w['workflowData']['templates']):
        a=t.get('attributes',{}) or {}
        if t.get('type') in ('add_contact_tag','remove_contact_tag'):
            for tg in (a.get('tags') or []):
                if tg in TAGS: aplica[(f,w.get('status'))].append(tg)
        else:
            blob=json.dumps(a,ensure_ascii=False)
            h=[tg for tg in TAGS if '"'+tg+'"' in blob]
            if h: testa[(f,w.get('status'))].append(h)
print("APLICA:",dict(aplica)); print("TESTA:",dict(testa))
EOF
```

Aplicador em `draft` com consumidor em `published` = defeito ativo. Atenção a
dois detalhes que custaram tempo: o campo do nó é **`type`**, não `actionType`;
e um dump pode estar pré-patch (comparar com o backup irmão antes de concluir).

**Regra de ordem:** publicar sempre o produtor primeiro. E ao publicar um
produtor com gatilho de oportunidade, conferir na tela se ele etiqueta o
**acervo** ou só mudança futura — se for só futura, as oportunidades já paradas
nunca recebem a tag e seguem invisíveis às condições. O dump não responde isso:
gatilho não entra nesta exportação.

## Condição de etapa não funciona em workflow que não é disparado por oportunidade — 11 workflows testavam etapa às cegas — 23/09/2026, sessão do PC

**Medido** no registro de execução da `ZZ TESTE 12X30` (gatilho de tag): o
passo `Pipeline stage is "[FUNIL DE VENDAS] - CONECTAR"` leu **valor vazio** e
deu falso — a oportunidade não está no contexto quando o gatilho é tag,
contato, resposta, link ou agendamento. Nenhum erro aparece: o lead só segue
pelo "não".

Varredura dos publicados: **11 workflows** tinham condição de oportunidade com
gatilho que não é de oportunidade — CONECTAR Estagnado, 12x30 parte 2, Fechar
Horário, Interceptação (Clique e Resposta), Opt-out, Recuperação de No-show,
Reengajamento 90d, Retorno Vencido, SLA do Closer. Os antigos provavelmente
nunca funcionaram como escrito.

**Correção:** workflow novo **`Espelho de Etapa`** (`2b1667a4`, gatilho de
etapa + 4 de status, sem janela) mantém no contato uma tag de estado —
`etapa-novo-lead|conectar|reuniao|negociar|formalizar` (aberta) ou
`status-nutricao|perdido|ganho`. As 26 condições foram trocadas pela tag
(`tools/patch_condicoes_etapa.py`); tags dos 55 leads existentes preenchidas.
Testado: mover para REUNIÃO → `etapa-reuniao` em segundos; e a cópia de teste,
com a tag, passou o portão e criou a T1. **Corrida:** o Reengajamento reabre a
oportunidade e testa a etapa no nó seguinte — os nós de tag que já existiam
passaram a gravar `etapa-conectar`/tirar `status-nutricao` na hora. A 12x30
parte 1 (gatilho de etapa) mantém a condição de oportunidade de propósito.

**Regra:** condição de oportunidade só em workflow com gatilho de oportunidade.
Em qualquer outro, teste a tag do Espelho.

## Outros três achados da mesma noite

- **Limite de tamanho:** o GHL recusa salvar workflow grande ("too big to be
  saved": 724 nós recusado, 410 aceito). O `preencher` reapontava os gatilhos
  ANTES de salvar os nós — a recusa deixou o gatilho principal da 12x30
  INATIVO e apontando para nó inexistente (restaurado; só reativa passando de
  rascunho para publicado). Agora há trava `MAX_NOS = 450` antes de tocar no
  CRM, e a 12x30 virou 2 workflows (380 + 347 nós), ligados pela tag
  `cadencia-12x30-p2`.
- **Vencimento da tarefa:** a tarefa de cadência nasce com `dueDate` = 00:00
  (Brasília) do próprio dia. "Vencida" para a trava de capacidade = de um dia
  anterior, não "antes de agora".
- **Canal:** confirmado pelo dono na tela — mandar pelo canal "SMS" entrega
  WhatsApp (Stevo). É o canal das mensagens automáticas.

## Documento que contém um artefato colável tem duas naturezas — não anotar dentro do artefato — 23/09/2026, sessão na nuvem

Consertando a coerência do `AGENTE-IA-CONEXAO.md` depois da renomeação de etapa,
anotei "(etapa da conversa, não a etapa do funil — a do funil chama `REUNIÃO DE
DIAGNÓSTICO` desde 22/09)" numa linha que está **dentro** do bloco do prompt do
sistema, ou seja, dentro do texto que o dono cola na tela do GHL. A anotação
estava certa e o lugar estava errado: nome de etapa do funil, id e data não
servem ao modelo, gastam contexto e podem vazar na conversa com o lead. Revertido
no mesmo turno; a nota foi para fora da cerca de código.

**A regra:** em documento de `wesales/` que carrega artefato colável (prompt de
agente, corpo de mensagem, JSON de import), o conteúdo entre cercas ``` é
**produto**, não documentação. Antes de editar, conferir se a linha está dentro
de uma cerca — `grep -n '^```'` dá os limites. Comentário, data, id e
justificativa vão sempre fora. Vale também para `biblioteca-mensagens.md`.

**Do mesmo conserto, um achado que vale por si:** o portão de entrada do agente
(seção 1) lista as tags que o fazem não responder e **não tinha
`fechar-horario`**. Hoje é inofensivo, porque `conectado-hoje` é aplicada no
mesmo nó e nunca sai. Mas a saída A que eu recomendei para o F-16 (`Wait 24h` →
`Remove Tag conectado-hoje`) **abre exatamente essa fresta**: a partir dela, um
lead 25h dentro da tentativa de fechar horário teria `fechar-horario` sem
`conectado-hoje`, e o agente entraria por cima do SDR. Acrescentei a tag ao
portão agora, enquanto é redundante. É o F-16 de novo, um nível acima: **quando
você recomenda tirar uma cláusula de circulação, procure quem dependia dela sem
saber** — e conserte antes, não depois.

## Uma cláusula redundante vira vazamento quando a cláusula vizinha muda — cruzar toda mudança de etapa com os filtros das listas — 23/09/2026, sessão na nuvem

O commit `1d04af2` (do PC do dono) fez o ramo `Atendeu` **ficar** em `CONECTAR`
em vez de mover a oportunidade para a etapa de reunião. Mudança certa e
coerente com o funil novo. Mas os dois filtros das filas do SDR são
conjunções com **duas** cláusulas que fazem o mesmo trabalho:

    não `conectado-hoje`   E   etapa = `CONECTAR`

Enquanto o `Atendeu` saía de `CONECTAR`, a segunda cláusula excluía o lead e a
primeira era redundante — e o fato de que **nada remove `conectado-hoje`** não
aparecia em nenhum comportamento. Tirar a segunda cláusula de jogo promoveu a
redundante a única, e ela exclui para sempre. O vazamento não está em nenhuma
das duas mudanças: está no encontro delas.

**A regra que fica:** numa conjunção de filtro, cláusula redundante não é
inofensiva — é uma dependência escondida. Quando uma mudança altera o valor de
uma cláusula, todas as outras do mesmo `E` precisam ser relidas, inclusive (e
sobretudo) as que "não faziam nada". Concretamente, para este projeto: **toda
mudança de etapa em workflow exige reler os filtros das listas inteligentes que
citam etapa** — são as seções 8.x de `IMPLEMENTACAO-WORKFLOWS.md`.

**A segunda regra, sobre nome de tag:** `conectado-hoje` promete "hoje" no
próprio nome e nunca é removida. O nome era a única documentação do ciclo de
vida dela, e estava errado. Tag cujo nome afirma um prazo (`-hoje`, `-semana`,
`-24h`) precisa de um removedor identificável por `grep` nos dumps; se a busca
por `remove_contact_tag` com aquele nome vem vazia, o nome é mentira até prova
em contrário. Checagem barata, vale em toda rodada.

**Terceira, sobre gatilho de tag:** par "aplicador publicado + consumidor em
**rascunho**" numa tag que ninguém remove produz exclusão permanente e
silenciosa do consumidor — gatilho de tag dispara no *evento* de aplicação, e
aplicar tag já presente não gera evento. Foi o caso de `fechar-horario`; o dono
publicou o consumidor no mesmo dia e a janela fechou limpa (0 contatos), mas a
regra vale: quando um workflow novo é gatilhado por tag, conferir se quem
aplica a tag já está no ar antes dele. A ordem certa é o consumidor primeiro.

**Quarta, e é a mais reaproveitável: `remove_from_workflow` pula os nós de
saída do alvo.** Arrancar o contato de um workflow cancela os passos pendentes
dele — os `Remove Tag` que aquele workflow faria não rodam. Então toda tag cuja
limpeza mora *dentro* de um workflow é permanente para quem sai por remoção
externa. Foi isso que derrubou uma saída que eu mesmo tinha recomendado como
limpa (trocar a cláusula do filtro para `não fechar-horario`): parecia segura
porque a tag tem removedor, mas o removedor não é alcançado pelo caminho de
quem agenda. **A regra:** quem arranca o contato de um workflow precisa limpar,
no mesmo nó, as tags que as saídas daquele workflow limpariam — e a checagem
barata é cruzar cada `remove_from_workflow` de terceiro com os
`remove_contact_tag` do alvo. Medido: 5 alvos nesta conta, e só
`fechar-horario` não tem segunda rede no Mestre de saída. Tabela na seção
2.31.2 do `build-wesales.md`.

**Quinta, sobre as próprias ferramentas de patch: script que aplica na conta e
não re-exporta o dump deixa o repositório mentindo.** `patch_remove_parte2.py`
exportava o backup, aplicava e parava — o script irmão `patch_funil_reuniao.py`
re-exporta na última linha do loop. Resultado: 3 dumps ficaram idênticos ao
backup pré-patch, `version` e `updatedAt` inclusive, então **nenhuma checagem
de frescor pega** e a auditoria seguinte (a minha, nesta rodada) conclui que o
patch não foi aplicado. Quase registrei um achado grave em cima disso.
Corrigido na ferramenta. **Duas regras:** todo script que faz `put` tem que
re-exportar depois; e antes de afirmar qualquer coisa a partir de um dump,
comparar com o backup irmão — se forem idênticos em `updatedAt`, o dump é o
pré-patch e não responde nada. Bônus do mesmo arquivo: caminho de export
relativo ao diretório de execução em vez de ao script só funciona se o script
for rodado de dentro de `wesales/tools/`; usar sempre o caminho relativo ao
`__file__`.

Medição da rodada, para separar armadilha de incêndio: `conectado-hoje` em 2
contatos (os dois de teste do projeto), `fechar-horario` em 0 (remedido depois da
publicação do consumidor). Nenhum lead real afetado — conta de projeto, dá para consertar antes de doer. Achado completo e
as quatro saídas: seção 2.31 do `build-wesales.md` (F-16).

## Duas trilhas de execução deste projeto não se enxergam — checar `PLANO-MULTICANAL.md` antes de tratar o roadmap como única fonte de estado — 23/09/2026, sessão na nuvem

Esta sessão (MCP `GHL CRM`, sem bearer da API interna) leu o roadmap inteiro,
achou tudo fechado ou represado por decisão do dono, e ia registrar bloqueio
— até cruzar `git log` com o estado ao vivo da subconta e achar uma segunda
trilha de trabalho que os documentos principais não citam.

**O que existe e este projeto quase não vê:** `wesales/tools/` tem ~30
scripts Python/JS que falam com a **API interna** da HighLevel (a mesma que
`briefing-sdr.md`/`campos-e-tags.md` chamam de "só no PC do dono, exige
bearer que esta sessão não tem") — `ghl_api.py`, `create_field.js`,
`renomear_etapa.js`, os `build_w*.py` que montaram os workflows publicados.
Essa trilha **cria campo e renomeia etapa por API de verdade**, coisa que
este conector MCP nunca fez. E ela está ativa: `wesales/PLANO-MULTICANAL.md`
(commit direto do dono, 22/09/2026 21:43 BRT, co-autorado por outra sessão
Claude) é um plano de reformulação inteiro — renomeia `AGENDAR` para
`REUNIÃO DE DIAGNÓSTICO`, reintroduz WhatsApp/Stevo como canal, muda o
comportamento de `CONECTAR` — com checklist próprio (E1-E14) rodando por
commits desde então (`482de1f`, `4f6a9c2`, `9268130`, e o campo `Canal que
conectou` já criado na subconta às 01:06 UTC de hoje). **Nada disso está
citado em `ROADMAP-SALES-ENGAGEMENT.md` nem em `build-wesales.md`** — os
dois continuam descrevendo o desenho anterior ("100% telefone", etapa
`AGENDAR`), e uma leitura só desses dois documentos concluiria (errado) que
nada mudou desde o G-09.

**Por que aconteceu:** as duas trilhas são sessões automáticas diferentes,
cada uma commitando na mesma branch, cada uma lendo só os documentos que o
seu próprio fluxo de trabalho aponta. `G-09`, fechado por esta classe de
sessão 22 minutos **antes** do commit do `PLANO-MULTICANAL.md`, até
levantou exatamente a pergunta que o plano novo responde (Stevo entrega SMS,
não WhatsApp de verdade) — e ninguém cruzou as duas coisas até agora.

**A regra, generalizável:** antes de tratar um roadmap/aviso como estado
corrente do projeto, checar se existe um documento de execução **mais
recente** (por data no texto ou por `git log -- <arquivo>`) que o
sobreponha — um "aviso" ou "decisão" datado não é necessariamente a última
palavra só por estar no arquivo mais lido. Nesta rodada, corrigido com notas
cruzadas em `ROADMAP-SALES-ENGAGEMENT.md` (topo), `build-wesales.md`
(seção 1.0), `APROVADO.md` (linha do SMS/WhatsApp) e `campos-e-tags.md`
(campo `Canal que conectou` registrado) — sem reescrever nenhum dos dois
desenhos por inteiro, que é trabalho grande demais para uma rodada e não
era o achado desta.

## O rótulo na tela escondia uma decisão já tomada — "WhatsApp" é o SMS que o dono removeu — 23/09/2026, sessão na nuvem

A rodada do G-09 mediu bem: a integração Stevo entrega `TYPE_CUSTOM_SMS`, não
`TYPE_WHATSAPP` — é SMS com o rótulo trocado na tela. E tirou a consequência
técnica certa: o R-17 e o 2.9.3 filtram por "Canal: WhatsApp" e nunca
disparariam para uma resposta por esse número.

**A consequência que ficou sem puxar é maior e é de decisão.** O `APROVADO.md`
diz, desde 19/09: *"SMS saiu por decisão do dono — não é canal de contato com
lead neste projeto"*, e a linha segue `[ ]`. Ou seja: **o canal reconectado
como "WhatsApp" é o canal que o dono removeu do projeto.** A tela diz uma
coisa, o fio entrega outra, e a decisão do dono estava escrita sobre o nome
que o fio usa, não sobre o nome que a tela mostra.

Isso atinge três coisas que pareciam resolvidas: a régua multicanal manda
"WhatsApp (SDR envia)" que na verdade é SMS tarifado; o agente de IA foi
desenhado para conversa de WhatsApp/DM e conversaria por SMS; e o risco que
registramos como "banimento do número no WhatsApp" troca de natureza — some o
risco de WhatsApp, entram custo por segmento e opt-out por STOP.

**A regra:** quando uma integração é "não oficial", perguntar **o que ela usa
por baixo** antes de tratá-la como o canal que o nome promete. Rótulo de tela
não é tipo de canal — e aqui a diferença entre os dois atravessava uma decisão
de negócio já tomada, que ninguém teria como ver olhando a interface.

**Corolário para este projeto:** decisão registrada sobre um canal deve citar
o **tipo técnico** (`TYPE_CUSTOM_SMS`, `TYPE_WHATSAPP`), não só o nome
comercial. "SMS saiu" e "WhatsApp entrou" descrevem o mesmo fio.

## A Stevo continuou gerando contato de teste depois da nota de 22/09 — e a nota nunca tinha virado item do roadmap — 23/09/2026, sessão na nuvem

A entrada "GHL não-oficial (QR) já está recebendo mensagem real de teste"
(abaixo) registrou 3 contatos de teste às 22h56 UTC de 22/09/2026 e parou
por aí — um aprendizado, não um item numerado. Nesta rodada (23/09/2026), a
reconferência de rotina achou um **4º contato** (`Francisca`, 23:34:36 UTC,
mesmo `sourceId` da Stevo) e, ao investigar a conversa dele por API
(`conversations_search-conversation`), o dado que faltava: `lastMessageType:
TYPE_CUSTOM_SMS`. Isso conecta duas notas que estavam soltas em documentos
diferentes — esta aqui ("a Stevo usa o canal de SMS do GHL por baixo") e o
filtro `Customer Replied — Canal: WhatsApp` que o R-17 (opt-out) e o 2.9.3
(sinal quente) usam em `build-wesales.md` — e produz um risco de compliance
concreto: se o filtro "WhatsApp" do gatilho não reconhece `TYPE_CUSTOM_SMS`,
nenhuma resposta pela Stevo aciona o DND automático. Promovido a item do
roadmap como **G-09**, com o fix aditivo (escutar WhatsApp **e** SMS) já
aplicado ao 2.9.3/2.9.5. **A regra que fica, generalizável:** um achado
registrado só aqui, sem virar item numerado, não é revisitado por rotina
nenhuma — esta entrada ficou parada uma rodada inteira apesar de ter os dois
fatos (canal técnico da Stevo, filtro por nome no build) já escritos em
documentos diferentes do projeto. Cruzar aprendizado com item aberto (não só
aprendizado com aprendizado) devia ser parte do sweep de toda rodada.

## Correção: a conta JÁ liga pelo WhatsApp dentro do GHL — Stevo Voice, com humano, sem API oficial — 22/09/2026, sessão do PC

A entrada logo abaixo ("não existe em nenhum plano") estava **errada para
esta conta**. O dono já contratou o Stevo Voice, e a tela confirma: a
conversa de um contato de WhatsApp mostra o botão **"Ligar via WhatsApp"**, e
o menu lateral tem **"WhatsApp Api Não Oficial"** e **"Call Center"**. O erro
foi ler "voz com IA" no resumo do módulo e concluir que só a IA ligava.

O que a documentação (doc.stevo.chat, seção Stevo Voice) diz:

- **Painel de Chamadas:** o operador (humano) liga e atende pelo WhatsApp do
  número conectado; discador por número ou pela lista, status (chamando,
  ocupado, atendeu), histórico e relatórios básicos (ligações do dia, tempo
  falado, **taxa de atendimento**).
- **Gravação** ("quando permitida"); gravações listáveis por API
  (`GET /v1/instances/{id}/voice/recordings`, escopo `voice:read`).
- **AI Coach:** transcreve em tempo real e sugere ao SDR como conduzir; debita
  da carteira; análise pós-ligação com resumo e nota. Quem fala continua sendo
  o SDR.
- Não há pedido de permissão da Meta (é QR). A própria Stevo recomenda ter
  consentimento, respeitar horário e **não exagerar na frequência**.

**Regra:** o resumo de um módulo não é a documentação dele, e o que está
instalado na conta vale mais que as duas. Antes de dizer "não existe", abrir a
tela.

## Ligação de WhatsApp pelo SDR de dentro do GHL, sem permissão do lead, não existe em nenhum plano — 22/09/2026, sessão do PC

Pesquisado a pedido do dono ("talvez exista plano pago"):

| Caminho | Liga pelo WhatsApp de dentro do GHL? | Quem fala | Permissão do lead |
|---|---|---|---|
| WhatsApp nativo do GHL (API oficial da Meta) | sim, botão na conversa | SDR humano | **obrigatória** (template, 2 pedidos/7 dias) |
| Stevo (conexão atual, QR) — planos Stevo 1/3/5: R$ 59/129/189 por mês | só o **Stevo Voice** | **agente de IA** (ElevenLabs), com gravação, transcrição e nota | — |
| WhatsApp Desktop no PC do SDR, mesmo número | fora do GHL, ao lado dele | SDR humano | não |

- A conexão da Stevo usa o canal de **SMS** do GHL: a ação "Enviar SMS" do
  workflow sai como WhatsApp pela Stevo (a Stevo tem um script que só troca o
  rótulo "SMS" por "WhatsApp QR" na tela). Mensagens chegam como `TYPE_CUSTOM_SMS`.
- O WhatsApp nativo do GHL **não está conectado** nesta subconta (a tela de
  WhatsApp mostra só o cadastro).
- Todos os planos Stevo trazem "Stevo voice liberado"; nenhum anuncia ligação
  de WhatsApp feita por humano de dentro do GHL.

Fontes: stevo.chat (planos e FAQ, lidos renderizados em 22/09/2026);
tutorial.stevo.chat (integração GHL, mudando SMS para WhatsApp QR);
help.gohighlevel.com 155000007253 / 155000007989.

## Descrevi um mecanismo como se fosse um estrago em curso — e eu tinha o número que me desmentia — 22/09/2026, sessão na nuvem

Ao conferir o F-15 eu escrevi, sobre o ciclo do lead sem telefone: *"Quem não
tem telefone volta, bate no mesmo portão e volta ao mesmo lugar, de 90 em 90
dias, sem nunca receber uma tentativa."* Presente do indicativo, como se
estivesse acontecendo.

A rodada do G-08 conferiu por API antes de aplicar e achou o que eu não olhei:
**zero oportunidade `abandoned` na base.** O ciclo nunca rodou. É uma armadilha
montada, não um estrago em curso.

**O agravante é que o número estava na minha própria medição.** Horas antes eu
tinha levantado a distribuição etapa × status e publicado a tabela: 45 `NOVO
LEAD open`, 2 `CONECTAR lost`, 2 `NEGOCIAR open`, 1 `NEGOCIAR lost`. Somam 50 e
não há **nenhum** `abandoned` — e o gatilho do R-08 é exatamente
`status == abandoned`. Eu verifiquei o mecanismo no payload, confirmei que ele
está correto, e não cruzei com a contagem que eu mesmo tinha feito.

**A regra:** verificar que um caminho **existe** no workflow não diz **quantas
vezes ele rodou**. São duas perguntas, e a segunda quase sempre tem resposta
barata — uma contagem por status, um filtro por tag. Antes de escrever no
presente ("o lead volta", "isso está acontecendo"), contar quantos registros
passaram por ali. Se o número for zero, o texto correto é "montado e ainda não
disparado" — que muda a urgência do item e o tom da entrega ao dono.

Corolário prático: mecanismo verificado + ocorrência zero = **armadilha**, e
armadilha se conserta com calma. Mecanismo verificado + ocorrência alta =
incêndio. Chamar armadilha de incêndio gasta o crédito de atenção do dono, que
é finito, e é exatamente o mesmo custo do monitor que grita sem motivo que eu
apontei no F-09.

## Um achado escrito dentro do texto de um item fechado não é aplicado sozinho — precisa da mesma conferência de "isto virou mudança de verdade?" — 22/09/2026, sessão da nuvem (G-08)

Ao medir o F-15 (resgate por e-mail para quem não tem telefone), a própria
sessão que fechou aquele item já tinha escrito a correção que o R-08
precisava ("o nó 1 do R-08 precisa distinguir por que o lead virou
`abandoned`... portão novo, antes de reativar") — e nunca voltou para
aplicar no nó real do R-08. Ficou um parágrafo de intenção dentro do texto
do F-15, tratado como resolvido porque estava escrito, mas o nó 2 do
Reengajamento 90 dias continuou sem a condição. Achado só porque esta rodada
perguntou "o F-15 tem alguma correção pendente que nunca virou edição?" em
vez de assumir que um item `FEITO` fechou tudo que o próprio texto dele
descreveu. **Regra prática, generalizável:** ao reler um item fechado (a
mesma instrução de sempre do roadmap), não basta conferir se o "Pronto
quando" dele foi cumprido — é preciso conferir se toda frase de ação dentro
do próprio texto ("X precisa disto", "falta fazer Y") virou de fato uma
edição em algum arquivo de especificação. Um parágrafo que descreve uma
correção não é a correção. Mesma classe de erro que já motivou F-12 e F-13
(achado em rodapé, nunca promovido a item), agora um nível mais fundo:
dentro do próprio item que registrou o achado, não num item vizinho.

**Efeito colateral útil desta rodada — reconferir dado antes de escrever
sobre um "ciclo ativo":** o texto do F-15 (escrito horas antes) descrevia os
5 leads reais do Instagram como "presos num ciclo fechado" de
`abandoned`+`nutricao-90d`. Reconferido por API antes de escrever o G-08:
**nenhum estava** — os 5 seguem em `NOVO LEAD`, sem nenhum campo de cadência
preenchido, porque nunca foram promovidos para `CONECTAR` (G-03 segue
represado) e portanto nunca passaram pelo portão que aplicaria
`telefone-invalido`. A base tem **zero** oportunidade `abandoned` agora. O
diagnóstico do F-15 (o nó do R-08 não protege quem não tem telefone) segue
correto e vale a pena corrigir **antes** do primeiro lead cair nesse buraco
— mas a frase "estão presos" era sobre um estado futuro, não atual, e só a
releitura pela API pegou a diferença. Vale para qualquer achado herdado de
uma sessão anterior: reconferir o dado antes de descrever como fato
presente, não só copiar a frase de quem escreveu primeiro.

## GHL não-oficial (QR) já está recebendo mensagem real de teste — 3 contatos novos nesta sessão, criados pela Porta de Entrada sozinha

Lendo a base às 22h56 UTC de 22/09/2026 (antes de fechar o G-08), apareceram
3 contatos novos desde a última leitura registrada no roadmap (50→53),
todos criados por `INTEGRATION`/`OAUTH`, `sourceId`
`682cd9287059b4173d8b17bd-mawx7is9` — a integração de WhatsApp não oficial
(`stevo`, QR) que o dono conectou nesta mesma tarde (ver entrada "GHL não
oficial conectado" abaixo). São mensagens manuais do próprio dono testando o
número ("fds", "me diz o nome do seu crm"), não lead real — mas confirma,
com tráfego de verdade, que a Porta de Entrada (G-01, gatilho `Contact
Created` sem filtro) pega **qualquer** origem, inclusive uma integração que
não existia quando o G-01 foi desenhado: os 3 ganharam oportunidade em
`NOVO LEAD` sozinhos, em segundos. Útil para quem for medir "quantos
contatos reais existem": filtrar por `createdBy.sourceId` antes de contar
como lead — esta integração pode gerar mais ruído de teste enquanto o dono
configura o agente de IA (`AGENTE-IA-CONEXAO.md`).

## O GHL liga pelo WhatsApp — mas só na API oficial, e o lead precisa dar permissão antes — 22/09/2026, sessão do PC

Eu disse ao dono que "ligação de WhatsApp não sai pelo GHL". **Errado** — ele
corrigiu, e a documentação confirma: *WhatsApp Calling* está em GA (web e app
LeadConnector ≥ 4.18), com ligação de dentro da conversa, disposição no fim e
gatilho `Call Details` filtrado por disposição. As regras que mudam o desenho:

| Regra | Valor (docs HighLevel) |
|---|---|
| Conexão exigida | número na **API oficial** do WhatsApp Business (Meta); **sem Coexistence** |
| Limite de mensagens da WABA | tier **2.000+** |
| Ligação iniciada pela empresa | **só com permissão do lead**, pedida por template (janela fechada) ou mensagem interativa (janela aberta) |
| Pedido de permissão | máx. **1 a cada 24 h** e **2 em 7 dias** por contato |
| Validade | temporária **7 dias** ou permanente |
| Ligações conectadas | até **5 por contato em 24 h**; **100 por número em 24 h** |
| Revogação automática | **4 ligações seguidas não atendidas** |
| País | Brasil permitido (bloqueados: EUA, Canadá, Turquia, Egito, Vietnã, Nigéria) |
| Custo | por minuto, pulsos de 6 s; ligação do cliente é grátis |
| Gravação / transcrição | **não mencionadas** — não contar com o W20 para essas ligações |

**Consequência para esta conta:** o WhatsApp conectado é **não oficial (QR)**
— esse recurso não vale para ele. E, mesmo na API oficial, "D1: ligação de
WhatsApp" para lead frio não existe: o D1 vira **pedir permissão**; a ligação
só a partir do aceite. O limite de 4 não atendidas casa com o contador `WA não
atendidas seguidas` que a 12x30 já tem — o teto da régua tem que ficar em 3.

Fontes: help.gohighlevel.com artigos 155000007253 e 155000007989; changelog
"WhatsApp Calling is now Generally Available (Web + Mobile)".

## Relógio das cadências corrigido no ar por ajuste cirúrgico — e `{{right_now}}` puro ainda está em 8 notas publicadas — 22/09/2026, sessão do PC

**Aplicado** (o dono escolheu "ajuste cirúrgico" — exceção consciente à regra
"nunca edite um publicado"), `tools/patch_relogio_cadencias.py --aplicar`:

| Workflow | Mudanças | Conferido depois do PUT |
|---|---|---|
| `Cadência 12x30` (`c64a808b`) | `Entrada em` + `1ª tentativa em` = `{{right_now.date}} {{right_now.time}}`; `Conexão real` = vazio no nó de entrada e nos 12 toques | 410 nós, ids iguais, gatilhos ativos |
| `Cadência Inbound` (`c2375e2f`) | idem; entrada + 5 toques | 172 nós, ids iguais, gatilho ativo |
| `Reengajamento 90 dias` (`37eb32e4`) | idem; reset de rodada + 4 toques | 105 nós, ids iguais, gatilho ativo |

`allowMultiple`, `stopOnResponse`, `timezone` e `window` comparados com o
backup (`workflows-json/_antes-patch-relogio/`): nenhum mudou. `allowMultiple
= False` na 12x30/Inbound **já era** o valor original. Isso fecha o
pré-requisito 6 do W20. Os builders (`build_w11/w12/w16_w8.py`) ainda dizem
`"sim"` — se alguém reconstruir por eles, o defeito volta; corrigir antes de
qualquer rebuild.

**Aberto — medir antes de mexer:** `{{right_now}}` puro (sem `.date`/`.time`)
está no texto de `Add Note` de 8 workflows publicados (AGENDAR Estagnado,
Alerta de Speed-to-lead, CONECTAR Estagnado, Fila Travada, Lead Esquecido,
Opt-out por Palavra-chave, Registro de Comparecimento, Retorno Vencido). Em
campo TEXT ele vira `[object Object]`; em nota **não foi medido**.
`python tools/teste_relogio.py nota` monta o teste (`ZZ TESTE RELOGIO NOTA`,
tag `teste-relogio-nota`) — o classificador do modo automático bloqueou rodar.

**WhatsApp conectado (informado pelo dono, 22/09/2026):** conexão **não
oficial, por QR code**. Relevante para o M1–M3 (fora da 12x30 porque os nós
de WhatsApp pediam `template_id`/`from_phone_number`) e para a decisão
"cadências 100% telefone" (`d52e61d`). Nada mudado por isso ainda — voltar a
usar WhatsApp nas cadências é decisão do dono, e API não oficial tem risco de
bloqueio do número em disparo automatizado.

## `{{right_now}}` grava `[object Object]` — a variável que funciona é `{{right_now.date}} {{right_now.time}}` — 22/09/2026, sessão do PC

Medido, não deduzido: workflow `ZZ TESTE RELOGIO` (`6d40b678-…`, gatilho tag
`teste-relogio`) gravou candidatas no C-14 do `Teste Atendeu` às 22:15 UTC:

| Variável | Valor gravado |
|---|---|
| `{{right_now}}` — **a que a spec manda** (seção 2.3) | `[object Object]` |
| `{{right_now.date}}` | `22/09/2026` |
| `{{right_now.year}}-{{right_now.month}}-{{right_now.day}} {{right_now.hour}}:{{right_now.minute}}` | `2026-9-22 19:15` (sem zero à esquerda) |
| `{{right_now.day_of_week}}` | `terça-feira` |
| `{{right_now.time}}` | `19:15` — já no fuso da subconta (SP) |

Isso explica o `sim`: quem montou provavelmente viu `{{right_now}}` falhar e
caiu no plano B "marca, não carimbo" sem registrar. **Trocar `sim` por
`{{right_now}}`, que é o que a spec e a rodada da nuvem pediam, teria gravado
lixo em todo lead.** Valor a usar: `{{right_now.date}} {{right_now.time}}` →
`22/09/2026 19:15`. É texto; não ordena nem compara como data.

**Onde está o `sim` (builders):** `build_w11.py` (12x30: `1ª tentativa em`
no toque 1, `Entrada em` no nó comum), `build_w12.py` (Inbound: os mesmos
dois) e `build_w16_w8.py` (Reengajamento 90d: os dois). O único leitor é o
W15 (`build_w15.py`), que só testa `has_no_value` → trocar o valor não o afeta.

**Armadilha antes de corrigir:** `Pós-ligação v2` (2×) e `Pós-agendamento v2`
(1×) referenciam o **id** da `Cadência 12x30` (`c64a808b-…`). Uma troca por
v2 os deixaria apontando para o original desligado — o mesmo defeito do
`Mestre de saída v2`. E rebuild pelo builder gera ids de nó novos (`g.uid()`),
o que pode soltar contatos parados num `Wait`. O caminho seguro é patch
cirúrgico no mesmo workflow (mesmo id, mesmos ids de nó, só o `value`), o que
esbarra na regra "nunca edite um publicado" — decisão do dono.

## O `sim` em `Entrada em` não é resíduo de teste — é o valor escrito no nó — 22/09/2026, sessão do PC

Li os nós dos exports em `workflows-json/`. O `Update contact field` grava a
string literal `'sim'` (não `{{right_now}}`) em:

| Workflow | `Entrada em` | `1ª tentativa em` |
|---|---|---|
| `Cadência 12x30` | `'sim'` | `'sim'` |
| `Cadência Inbound` | `'sim'` | `'sim'` |
| `Reengajamento 90 dias` | `'sim'` (nó "Zera contadores") | `''` no reset, `'sim'` depois |

Ou seja, a suspeita da rodada da nuvem se confirma na origem: **nenhum
cronômetro da operação (R-02, "Entrada em há mais de 1h") tem hora para
medir.** Ressalva: os exports podem estar atrás do que está no ar — a
correção deve reler o workflow vivo antes de montar a v2.

**Próximo passo, escrito e não executado:** `tools/teste_relogio.py` (workflow
`ZZ TESTE RELOGIO`, gatilho tag `teste-relogio`) grava cinco candidatas
(`{{right_now}}`, `.date`, `.year-.month-.day .hour:.minute`, `.day_of_week`,
`.time`) no C-14 do contato de teste, para ler qual o GHL preenche. O
classificador do Claude Code bloqueou rodar o script ("Production Deploy") — precisa de
regra de permissão do dono. Só depois da medição: v2 das três cadências
trocando `'sim'` pela variável que funcionar.

## "Publique sempre" apagou o único freio que pegou todos os defeitos de hoje — 22/09/2026, sessão na nuvem

O dono autorizou publicar de forma permanente e o W18/W20 foram publicados no
mesmo commit (`f0a0474`). Decisão dele, e acelera muito. Mas vale registrar o
que ela custa, porque nenhum documento registrou.

**Todos os defeitos achados hoje foram achados em especificação, não em
produção:** o `Mestre de saída v2` apontando para o Clique antigo, o F-09
mandando o telefone desviar para um canal extinto, o F-15 resgatando por um
canal que o público-alvo não tem, o F-14 dimensionado com 8 de 12 toques. Cada
um deles teria virado comportamento errado em lead real se a publicação fosse
automática na hora em que a spec foi escrita.

O intervalo entre "especificado" e "publicado" não era burocracia — era o
único ponto do processo onde um erro de raciocínio parava. **Agora é zero.**

O que isso muda para as próximas rodadas, e não é opcional:

1. O checklist de conferência deixou de ser revisão **posterior** e passou a
   ser **pré-condição** da publicação. Conferir depois de publicar é conferir
   com o lead já dentro.
2. Publicar workflow **ocioso** é seguro; publicar workflow com gatilho vivo
   não é a mesma coisa. O W20 é o exemplo bom por acidente: está no ar e não
   dispara, porque depende de gravação por número que segue desligada.
3. Quando a rodada que especifica é a mesma que publica, ela não tem revisor.
   O mínimo é ela mesma rodar o checklist **antes** do `PUT status=published`,
   e dizer na entrega que rodou.

**A regra geral, que vale além deste projeto:** quando um gate humano é
removido por ganho de velocidade, o custo não aparece na primeira rodada — ele
aparece na primeira rodada que erra. Quem remove o gate herda a obrigação de
substituí-lo por uma verificação explícita, ou aceita que o próximo erro chega
em produção. Vale dizer isso em voz alta no momento da remoção, não depois.

## "78% da base tem e-mail" era verdade sobre a base errada — e o resgate resgataria zero lead — 22/09/2026, sessão na nuvem

A rodada anterior achou um ciclo fechado de verdade, e eu confirmei no payload
publicado: nó 3 da 12x30 (`phone has_no_value`) → nó 10 (`abandoned`) → nó 11
(`nutricao-90d`), e o nó 1 do R-08 recicla em `status == abandoned`. Quem não
tem telefone volta, bate no mesmo portão e volta ao mesmo lugar, de 90 em 90
dias, para sempre. **Diagnóstico certo.**

A solução proposta — um workflow de resgate por e-mail (F-15) — foi justificada
com "9 de 50 sem telefone, 39 com e-mail (78% da base)". Cruzei as duas
populações contato por contato:

| | |
|---|---|
| Sem telefone | 9 |
| Desses, **com** e-mail | **1** — e é um lead de teste do Meta |
| Desses, **sem** e-mail | 8 |
| Leads reais de Instagram sem telefone **e** sem e-mail | 5 |

**O resgate alcançaria zero lead real.** E não é coincidência, é estrutural: o
formulário do Meta coleta telefone **e** e-mail juntos, então quem vem por ali
tem os dois; quem não tem telefone veio por **DM de Instagram**, que não coleta
nenhum dos dois. As populações são quase disjuntas **por construção do canal de
origem**.

**Isto é o ponto 4 do checklist numa forma nova.** Até hoje ele aparecia como
"os dois lados de uma razão têm de vir da mesma população" — uma regra sobre
métricas. Aqui não havia razão nenhuma: havia uma **cobertura de canal medida
no conjunto todo** sendo usada para dimensionar uma **solução para um
subconjunto**. Mesma falha, sem divisão nenhuma à vista.

**A pergunta que pega isso em uma linha:** antes de usar um percentual para
justificar uma solução, perguntar **"esse percentual foi medido exatamente nas
linhas que a solução vai tocar?"** Aqui bastava filtrar por `phone is null`
antes de contar e-mail — uma condição a mais no mesmo laço.

**E o corolário que salva o trabalho:** o e-mail não é inútil, está no público
errado. Os 39 com e-mail são justamente os que **têm** telefone — ali e-mail é
canal **adicional** e barato, que não consome o teto da rampa F-14. O resgate
de verdade, para os 5 do Instagram, só existe pelo **DM do Instagram**. Uma
solução no público certo e um público sem solução, separados — em vez de uma
solução aparentemente completa que não toca ninguém.

## E o mesmo erro, meu, na mesma rodada: rebaixei a Etapa B que eu tinha vendido — 22/09/2026

Propus ao dono corrigir `country`/`timezone` em 49 contatos dizendo que
"afeta janela de horário de workflow e validação de número". **As duas metades
estavam refutadas dentro do projeto**, na Tabela L do `CONFERENCIA-CAMPOS.md`:
a especificação usa fuso **da subconta** por decisão explícita (D-02), nenhum
nó lê fuso do contato; e o W19/Number Validation saiu por decisão do dono, então
não havia o que destravar.

Pior: **citei a Tabela L nessa mesma rodada**, para a distinção
`contact.country` vs `location.country`, e não carreguei a conclusão dela para
a minha própria proposta. É o ponto 12 do checklist aplicado a mim — ler um
documento não é o mesmo que propagar o que ele conclui, e a distância entre as
duas coisas é onde este projeto erra desde o começo.

Sobra higiene de dado, com o risco real que a Tabela L aponta (workflow futuro
que escolha "fuso do contato" cai em fallback silencioso). Barato, reversível,
**sem urgência** — e eu apresentei como a coisa mais fácil de aprovar.

## Leitura completa de 22/09: a máquina está construída e a esteira não está ligada — 22/09/2026, sessão na nuvem

O dono pediu leitura completa antes de implementar. Três achados que nenhuma
rodada anterior tinha, porque nenhuma tinha olhado a base **como base** em vez
de olhar campo por campo.

**1. 45 das 50 oportunidades estão `open` em `NOVO LEAD`, 37 delas há 3-4
dias, 44 de 50 contatos sem dono, 33 de 50 sem tag alguma.** Não falta
automação: 20 workflows publicados, 55 campos, 21 tags, pipeline montado. O
que falta é o passo que põe o lead na esteira — o L-07/G-03, aberto desde o
primeiro dia. A `Cadência 12x30` está publicada e correta e não roda para
ninguém, porque ninguém entra nela. **Construir mais não resolve; ligar
resolve.**

**2. Instagram está conectado e vivo, e não existe em documento nenhum.**
Página `O Próximo Cliente`, 5 conversas com DM real, os 5 contatos com
oportunidade aberta e **nenhum com telefone** — inalcançáveis numa cadência
100% telefone. Cuidado de leitura aplicado: as mensagens vêm
`direction: outbound` com `from` = a conta, e uma é pessoal, então **não**
concluí "lead pedindo preço"; concluí que o canal existe e não é governado.

**3. Nove contatos não têm telefone**, cinco deles os do Instagram. Numa
operação de um canal só, "sem telefone" é o mesmo que "fora da operação", e
ninguém tinha contado.

**Duas capacidades e duas armadilhas, medidas:**

| Achado | Detalhe |
|---|---|
| `contacts_update-contact` escreve `country` e `timezone` | testado no contato de estrutura: `US`/vazio → `BR`/`America/Sao_Paulo` |
| `body_tags` no update **sobrescreve todas as tags** | não passar esse parâmetro em update que não seja de tag; no teste eu omiti e as 14 tags sobreviveram |
| `assignedTo` e `customFields` saem por API | abre atribuição de dono e preenchimento de campo em massa |
| `calendars_get-calendar-events` devolve 422 **mesmo com `userId`** | o conector não repassa o parâmetro; calendário do closer não é auditável por API |

**A regra de método que isso rendeu:** auditar campo por campo responde "o
que existe"; auditar a base como população responde "o que está acontecendo".
O projeto passou dias no primeiro e o gargalo estava no segundo. Contar
quantos registros estão sem dono, sem tag e parados há quantos dias custa uma
chamada e reordena a fila de prioridade inteira.

## Aborto de coleta em ~2s é instalação ruim, não defeito — e eu diagnostiquei antes de medir — 22/09/2026, sessão automática

O CI de `c16c4e0` não deu as 12 falhas de sempre: deu **erro de coleta** em
`tests/test_mcp.py` (`ImportError: cannot import name 'MCPServer' from
'mcp.server'`), abortando a suíte inteira em **1,87s**, exit 2.

Diagnostiquei como deriva de dependência: `pyproject.toml` declara
`mcp>=1.2` sem teto e sem lock, então o CI resolve a versão mais nova a cada
instalação — e eu tinha o argumento de que o mesmo `src/` havia coletado bem
9 minutos antes. Escrevi que ia quebrar todos os branches.

**Errado.** Re-rodei o mesmo commit e ele voltou ao baseline normal
(`12 failed, 1949 passed, 32 skipped`). A falha era **transitória** — uma
instalação ruim naquele job, não uma versão publicada tirando o `MCPServer`.

Duas coisas para a próxima rodada:

**1. A assinatura de tempo distingue os casos.** Suíte que aborta em ~2s
morreu na importação, antes de qualquer teste rodar — isso é instalação,
checkout ou runner, e o procedimento é **re-rodar uma vez antes de
diagnosticar**. As 12 falhas conhecidas levam ~190s, porque os testes de
fato rodam. Ler o tempo total custa nada e separa "ambiente" de "código".

**2. Eu apliquei a mim mesmo o erro que tinha escrito hoje.** A regra do
C-14 dizia: "já foi provado" exige data, objeto e **valor lido**. Eu tinha
um mecanismo plausível e uma inferência temporal, chamei de causa e
anunciei consequência. O re-run era a medição — e contrariou. Mecanismo
plausível + coincidência de horário **não é** medição.

**O que sobra de verdade, sem exagero:** `mcp>=1.2` sem teto nem lockfile é
fragilidade real — foi ela que permitiu a resolução ruim. Não é urgente e
não é deste projeto (`wesales/` não toca `src/maquina/`), mas é o motivo
pelo qual esse aborto pode voltar sem ninguém mudar código.

## Usei o monitor que escrevi há uma hora e ele quase me pegou — duas vezes, de jeitos diferentes — 22/09/2026, sessão automática

Rodei o `auditoria_refs.py` com `tail -3` para economizar, vi a última linha
(`Pós-ligação v2 → Cadência 12x30`) colada no resumo "1 referência para
workflow arquivado", e concluí que ele estava acusando a `Cadência 12x30`,
que está no ar. Ia "consertar" um bug que não existia.

Rodei sem truncar: o único item marcado é o `Mestre de saída v2 → Clique
(antigo)`, o achado real do dono, que continua aparecendo porque o dump é
fotografia de antes do conserto ao vivo. O script estava certo; **quem errou
foi o meu jeito de ler a saída dele.**

**Regra 1:** não truncar saída de auditoria. `tail` separa o veredito das
linhas que o justificam, e aí o veredito cola na linha errada — que é
exatamente o modo de falha de um alerta mal lido, o mesmo que a entrada sobre
o `Fila Travada` descreve. Se a saída é longa demais para ler, o conserto é a
saída ficar mais curta, não a leitura ficar parcial.

**Mas a rodada achou um defeito de verdade no script, e era meu.** Três ids
existem em dois arquivos ao mesmo tempo — `Mestre de saída v2`, `ZZ TESTE W6`
e `ZZ TESTE API` têm backup em `_arquivo/` com o **mesmo id** do vivo. O
`carrega()` lia `_arquivo` depois e sobrescrevia, então o dicionário passava a
dizer que aquele id é arquivado. Ninguém aponta para o `Mestre de saída v2`
hoje; no dia em que apontar, o script diria "aponta para arquivado" sobre um
workflow publicado — **alarme falso no monitor que existe para não dar alarme
falso.**

Corrigido: o vivo tem precedência, e ids duplicados são listados no topo em
vez de silenciosamente resolvidos. O contador caiu de "11 arquivados" para
**8**, que é o número certo — os 3 a mais eram backups do que está no ar.

**Regra 2:** quando uma ferramenta indexa por id a partir de duas fontes, a
ordem de leitura é uma decisão de precedência, não um detalhe de laço.
Escrever "backup não sobrescreve vivo" custa uma linha; descobrir depois custa
a confiança no monitor.

## "Encerra a régua" é meia especificação — e a outra metade dispara um monitor falso todo dia — 22/09/2026, sessão automática

A rodada anterior aplicou a regra de refazer a multiplicação depois de uma
decisão de canal e achou um bug de verdade: as opções A e B do F-09 mandavam
o telefone **desviar para WhatsApp** ao estourar o limiar, num motor que não
tem mais WhatsApp. Corrigiu as duas para "encerra a régua mais cedo". Certo.

O que sobrou é a metade que não foi escrita: **como** encerra. Do jeito que
ficou, quem montar põe um `Remove from Workflow` seco — e o lead sai
carregando `fila-tel` e com tarefa órfã. A saída limpa canônica do projeto
tem três passos (nó 3b da 12x30): remover as tags de fila, aplicar
`limpar-tarefas`, e só então sair.

**E aí a junção:** o `Fila Travada` (F-05 peça 2) dispara sobre "`fila-tel`
presente depois das 18:30, porque o nó 9 não rodou". Um portão do F-09 sem
saída limpa geraria **um alerta falso por lead cortado, todo dia** — e o
resultado prático não é o alerta extra, é o gestor aprendendo a ignorar o
único monitor de fila parada que existe. Um monitor que grita sem motivo é
pior que monitor nenhum, porque consome a atenção que o caso real precisava.

**A regra:** num item que "encerra", "sai", "para" ou "remove", a
especificação só está completa quando diz **por qual caminho** — e num
projeto que já tem saída canônica, o caminho é citar o nó que já existe, não
descrever de novo. Verbo de saída sem caminho é onde tag órfã nasce, e tag
órfã é o que os monitores deste projeto foram feitos para caçar: o bug se
disfarça de alerta legítimo.

**Segundo achado, menor:** o mesmo "Como" mandava pendurar o portão "no
seletor de canal", que deixou de existir com 100% telefone. Resíduo da régua
alternada sobrevivendo dentro da própria correção que tirou o WhatsApp do
item — a correção acertou a tabela e passou por cima da frase três linhas
acima.

## A "regra que fica" do F-14 mandava reabrir todo item com toques por canal — F-09 ficou de fora, e suas opções mandavam desviar para um canal que não existe mais — 22/09/2026, sessão automática

A rodada anterior (`4d5bcf6`) já tinha nomeado o problema: a decisão de 100%
telefone (`d52e61d`) mudou "8 de 12 toques" para "12 de 12", e a rodada
generalizou em `APRENDIZADOS-CRM.md` — "quando uma decisão muda uma premissa
numérica, reabrir todo item que tenha tabela de toques por canal e refazer a
multiplicação". Ela fez isso para o F-14. Não fez para o F-09, que tem
exatamente esse tipo de tabela e é o item que a própria correção do F-08
tinha gerado horas antes.

Sem tela nem G-03/G-04/F-09/F-10/R-14 desbloqueados, o passo era o sweep de
coerência de sempre — desta vez guiado pela "regra que fica" em vez de
`grep` por nome de etapa. `grep -rn "8 de 12\|8 dos 12"` em `wesales/`
devolveu 11 linhas; a maioria é prosa histórica de item já `FEITO` (F-07,
F-08, "Resumo" datados) ou checklist de teste cujo ponto só fica mais forte
com o número certo (seção 10 do `build-wesales.md`: "telefone é o canal
majoritário" continua verdade, agora mais) — essas não foram tocadas, mesmo
critério que `dd9c65a` já usou para não reescrever as 107 menções de
WhatsApp. Duas linhas eram diferentes: o F-09 em `ROADMAP-SALES-ENGAGEMENT.md`
e a autorização pendente espelho em `APROVADO.md` — as duas ainda **abertas**,
as duas alimentando uma decisão que o dono ainda vai tomar.

**O número errado não era o pior problema.** F-09 propunha três opções para
o limiar de `Tel não atendidas seguidas`, e duas delas (A e B) mandavam o
telefone **"desviar para WhatsApp"** quando estourasse — texto herdado do
período em que o WhatsApp ainda carregava toques da régua. Depois de
`d52e61d`, WhatsApp não aplica nenhum toque: não existe canal para desviar.
Um dono lendo o item sem saber disso escolheria uma opção que descreve um
comportamento que a régua publicada não pode mais executar. Corrigido para
"encerra a régua mais cedo" nas duas opções — o único efeito que o motor de
workflow ainda pode produzir sem um segundo canal.

**Segundo achado, menor mas parado havia 8h por falta de quem fechasse o
loop:** a seção "Evidência indireta" do F-09 dizia, textualmente, "é
pergunta para o dono, nenhuma rodada deve gastar mais tempo procurando" —
sobre se as ligações saem por LC Phone ou linha própria. O dono **já tinha
respondido isso ao vivo** (`APRENDIZADOS-CRM.md`, "Resposta do dono...",
16:13 UTC) quase 9 horas antes desta rodada. A resposta já estava registrada
no arquivo certo; só não tinha voltado para dentro do item que fez a
pergunta. Fechado o loop: a seção agora aponta para a resposta em vez de
repetir que ninguém deve procurar.

**Regra prática, reforçando a de `4d5bcf6` em vez de repeti-la:** "reabrir
todo item com tabela de toques por canal" não é suficiente sozinho — um item
ainda **aberto**, cujo texto alimenta uma decisão que falta tomar, pesa
diferente de um item **fechado**, cujo texto só documenta o que já foi
decidido. A primeira categoria (aqui, F-09) é a que precisa ser corrigida
antes da próxima leitura do dono; a segunda (F-07, F-08, os "Resumo"
datados) pode ficar como registro histórico, porque reescrevê-la não muda
nenhuma decisão futura — só infla o diff. Ao aplicar a "regra que fica",
filtrar por "o item ainda está aberto?" antes de decidir se vale a pena
corrigir.

## A trava do aviso de LGPD vigiava o checkbox, não o botão — e os dois se separaram hoje — 22/09/2026, sessão automática

O dono ligou a transcrição de chamadas na subconta e deixou o W20 pronto em
rascunho. Fui ver o que isso aciona, e o achado não está no W20: está na
trava que protegia o aviso de gravação.

O `script-de-ligacao.md` fechava a pendência assim: *"enquanto o F-06 não
for ligado (os campos C-29/C-30 nascem `[ ]` em `APROVADO.md`), hoje nada é
gravado"*. A frase amarrava um fato do mundo — **nada é gravado** — ao
estado de um **checkbox de aprovação**. Hoje os dois se separaram: os campos
existem, a transcrição está ligada, e o `APROVADO.md` segue `[ ]` (certo,
só o dono marca). A trava continuava dizendo "verde" sobre uma condição que
já não era a que ela olhava.

**Mesma falha do `country`, em outro traje:** o documento vigia um
**proxy** em vez da coisa. Lá, `contact.country` no lugar de
`location.country`; aqui, o checkbox no lugar do botão de gravação. Proxy e
coisa andam juntos até o dia em que não andam, e é exatamente nesse dia que
alguém lê a garantia antiga.

**O segundo achado é mais sério, e é de sequência.** O aviso de LGPD está
catalogado como *pré-requisito nº 4 do W20*. Mas a LGPD se aplica à
**gravação**, não à medição: ligar gravação por número é um clique que não
passa pelo W20, e a partir dele existe ligação gravada **com o W20 ainda em
rascunho**. Catalogado onde estava, o aviso parecia ter o prazo da
publicação; o prazo real é o do clique, que é anterior e independente.

**Regra:** quando um pré-requisito for de natureza legal ou irreversível,
verificar de qual **ação** ele é pré-requisito, não de qual **entrega** ele
apareceu na lista. A lista foi escrita a partir do workflow; a obrigação
nasce do ato.

Continuo não escrevendo a frase do aviso — redação e base legal são do dono.
O que mudou é que agora está escrito **quando** ela passa a ser devida.

## O gatilho `Scheduler` não estava oculto — a via certa é o intervalo `Cron`, e o fuso é o da subconta — 22/09/2026, sessão do PC

A dúvida "o `scheduler_trigger` pode estar oculto para esta conta" (W18) caiu:
ele aparece na busca de gatilhos (categoria Eventos). O painel oferece
`Intervalo` = A cada hora / Diariamente / Semanalmente / Mensalmente / **Cron**.
Semanal pede dias e horários em dois seletores clicáveis; **Cron** é um campo
de texto só (`placeholder="Valor"`), portanto determinístico por script.

Gravado no W18 (`63cbb270-…`): `0 11,15 * * 1-5`. Formato que a API devolve:

```
conditions: [{field: "scheduler.interval", value: "cron"},
             {field: "scheduler.cron.expression", value: "0 11,15 * * 1-5"}]
```

O cron roda no fuso da subconta — lido pela API: `timezone = America/Sao_Paulo`.
A própria tela avisa que **expressões que disparam mais de uma vez por hora
não são aceitas**.

Também conferido nesta rodada: `Habilitar Transcrição de Chamadas` está
**ligada** (Sistema de telefonia → Voz → Transcrição de chamada). O gatilho do
W20 está gravado com `call_type == call` e `call_direction == outbound`.

**Publicação:** o classificador de permissões do Claude Code bloqueou o
primeiro `PUT status=published` ("Production Deploy"). O dono então autorizou
de forma permanente ("publique tudo você mesmo sempre") e os dois foram
publicados em 22/09/2026 — gatilhos `active: true`, `allowMultiple` preservado,
nós intactos (1 e 8). Pendente do W20 que ainda vale: pré-requisito
6 (zerar `Conexão real` antes de cada tentativa, nos workflows 2.4/2.10 já
publicados) e gravação ligada **por número** — sem ela não há transcrição e o
W20 nunca dispara.

## A prova que destravou o C-14 não existe — os dois carimbos da base guardam a string `sim` — 22/09/2026, sessão automática

A rodada anterior restaurou o nó do `Data e hora do sinal` (C-14) com um
raciocínio bom: a premissa que o matou em 19/09 vinha do **seletor da tela**,
e a montagem passou a sair pela API interna, que não usa o seletor. Certo até
aí. O problema é o passo seguinte — ela disse que `{{right_now}}` em campo
`TEXT` **já estava provado**, citando `Entrada em` (C-18) "carimbado ao
promover um contato de teste".

Fui ler os campos. O que está na base:

| Contato | `Entrada em` | `1ª tentativa em` |
|---|---|---|
| `Teste Número Errado` | `"sim"` | `"sim"` |
| `Teste Retorno` | `"sim"` | `"sim"` |
| todo o resto, inclusive o lead mais novo | vazio | vazio |

**Nenhum contato tem hora nesses campos.** Os dois que têm algo têm a string
literal `sim` — que é justamente o formato "marca, não carimbo" que a mesma
nota afirmava nunca ter sido usado. A frase "é isso que está publicado e
testado" descreve o contrário do CRM.

**O erro não é ter restaurado o nó — é a palavra "provado".** Uma premissa
foi derrubada corretamente (o seletor não vale mais) e, no impulso, uma
segunda premissa entrou como se também tivesse sido testada. Derrubar
"X é impossível" **não prova "X funciona"**: devolve a pergunta ao estado
de aberta. Entre as duas há um teste que ninguém fez.

Por isso **não apaguei o nó 5b**: apagar agora seria o mesmo erro ao
contrário — decidir sem medir, na direção oposta. O nó fica, a
justificativa fica marcada como não verificada, e o teste que fecha está
escrito (abrir o nó 0.6 na tela, ou promover um lead e reler o campo).

**O que faz isso valer mais que o C-14:** o R-02 (speed-to-lead) e toda
comparação de "`Entrada em` há mais de 1h" dependem desses campos terem
hora. Se a régua publicada grava `sim`, essas medições **não estão medindo
nada** — e, como sempre neste projeto, sem nunca dar erro. O C-14 era uma
coluna vazia numa lista; isto é o cronômetro da operação.

**Regra:** "já foi provado" é uma afirmação sobre uma medição — então ela
tem data, objeto e valor lido. Quando uma nota disser que algo está provado
sem dizer **onde ler o valor**, é hipótese herdada, e o custo de conferir
é uma chamada de API.

## Uma premissa técnica descartada em 19/09 (`{{right_now}}` em campo `TEXT`) morreu com o método de montagem que a gerou, não com o teste que a refutaria — 22/09/2026, sessão automática

`Data e hora do sinal` (C-14) foi descartada do nó 2.9.2 em 19/09/2026
porque, **montando ao vivo na tela** naquele dia, o seletor de valor de
`Update Contact Field` não parecia oferecer "data/hora atual" para um campo
`TEXT`. A dúvida ficou registrada como tecnicamente aberta (entrada "Pesquisa
que corrobora (não fecha)..." abaixo) — correto para o método de montagem de
19/09. O que ninguém cruzou é que **o método mudou** dois dias depois: a
partir de 21/09/2026 a montagem passou a sair também pela API interna
(`wesales/tools/`), que grava o valor do campo direto no payload sem passar
pelo seletor clicável. E essa mesma API já tinha **provado, rodando de
verdade**, que `{{right_now}}` escreve sem problema num campo `TEXT` de
contato — `Entrada em` (C-18, mesmo tipo) foi carimbado com sucesso ao
promover um lead de teste (`GUIA-MONTAGEM.md`, "Testado de ponta a ponta").
A prova já existia desde 21/09; só não tinha sido cruzada com a pendência do
C-14, porque uma vivia em `build-wesales.md` (seção 2.9.2) e a outra em
`GUIA-MONTAGEM.md`, e nada disparava a comparação.

**Consequência, achada só nesta rodada:** `campos-e-tags.md` nunca soube do
descarte (continuou prometendo "Workflow (F-01)" o tempo todo) e
`IMPLEMENTACAO-WORKFLOWS.md` sabia mas não linkava a causa — os dois
documentos discordavam de `build-wesales.md` sem que nenhuma varredura de
nome de etapa ou `fieldKey` pegasse isso, porque não é nome errado nem
chave errada: é uma linha de spec que um documento aplicou e os outros dois
não. A Smart List `Resposta por Template` (8.13) tinha uma coluna
condenada a ficar vazia para sempre, num workflow que não quebra — o
mesmo padrão de "achado só por ausência" que várias outras entradas aqui já
descrevem, aqui numa coluna de relatório em vez de um monitor.

**Regra prática, generalizável:** quando uma premissa técnica nasce de um
teste **na tela** ("montando ao vivo, o seletor não oferece X"), ela vale
para aquele método de montagem, não para sempre. Se o projeto ganhar um
segundo método de montagem depois (aqui, a API interna), releia as
premissas que nasceram do primeiro método antes de assumir que ainda
travam — o mesmo tipo de coisa que já rendeu o F-05 (premissa de "esperar
data dinâmica" resolvida por busca melhor) e o F-06 (premissa de "sem
duração nativa" resolvida por busca melhor), agora por mudança de
**método**, não de busca. Corrigido em `build-wesales.md` (seção 2.9.2, nó
5b), `GUIA-MONTAGEM.md` (tabela de retoques + contagem de nós marcada com
`*`) e `IMPLEMENTACAO-WORKFLOWS.md` (linha do C-14). Detalhe completo em
`ROADMAP-SALES-ENGAGEMENT.md`, "Ordem sugerida", entrada de 22/09/2026.

## Li as chaves dos 4 campos novos antes de alguém precisar delas — é a única hora barata — 22/09/2026, sessão automática

O dono criou os 4 campos do W20 entre 16:38 e 16:56 (base de 51 → 55). Nenhum
documento ainda escreveu `{{merge field}}` para eles. **Foi exatamente por
isso que li as chaves agora**, e não quando o W20 for montado.

| Nome na tela | Chave real | O que a adivinhação diria |
|---|---|---|
| `Duração da ligação` | `contact.durao_da_ligao` | ~~`duracao_da_ligacao`~~ |
| `Conexão real` | `contact.conexo_real` | ~~`conexao_real`~~ |
| `Conexões reais telefone` | `contact.conexes_reais_telefone` | ~~`conexoes_reais_telefone`~~ |
| `Ligações com transcrição` | `contact.ligaes_com_transcrio` | ~~`ligacoes_com_transcricao`~~ |

As quatro adivinhações estariam erradas, pela mecânica já confirmada quatro
vezes: o GHL **remove a letra acentuada inteira**. E chave errada não dá
erro — o nó lê vazio e o monitor morre calado, que é como a seção 2.24
perdeu um monitor inteiro com `checkpoint_data_de_retorno`.

**A regra de timing, que é o achado real:** o custo de conferir a chave é o
mesmo hoje e daqui a uma semana — ~9k tokens de uma leitura. O custo de
**não** conferir cresce: hoje corrijo uma tabela, depois de montado o W20
corrijo a tabela, o workflow publicado e o tempo em que ele rodou mudo sem
ninguém notar. Campo novo no CRM é o gatilho para ler a chave, não o
workflow novo que vai usá-lo.

**Armadilha de vizinhança nesta leva:** já existia `Conexões telefone`
(`contact.conexes_telefone`, 18/09) e agora há `Conexões **reais**
telefone` (`contact.conexes_reais_telefone`). Nomes quase iguais, chaves
quase iguais, **populações diferentes** — e o widget `Taxa de Conexão Real`
é uma razão C-31/C-32. Trocar por engano o numerador pelo campo antigo
devolve um número que parece certo e mistura duas medições. Detalhe na
Tabela N do `CONFERENCIA-CAMPOS.md`.

**Fonte da auditoria atualizada:** os 4 entraram no `wesales/tools/campos.json`
(79 → 83 entradas) com id, chave e tipo lidos da API, senão a varredura de
órfão passaria a acusar falso positivo no minuto em que o W20 fosse escrito.

## Os 4 campos do W20 (C-29 a C-32) já existem — a leitura de 16:13 UTC que dizia "continuam ausentes" venceu em menos de uma hora — 22/09/2026, sessão automática

Rotina de sempre (reler premissa represada antes de assumir que o item segue
do tamanho de antes): `locations_get-custom-fields` nesta rodada devolve
**55 campos**, não 51. Os 4 novos são exatamente os que o F-06/W20 esperava —
`Duração da ligação` (`PLjkuvnoDk7Hvt4qv0a8`), `Conexão real`
(`7wtFfDDxOpYCfHzBsZXP`), `Conexões reais telefone`
(`2BSLMqty4LEwdoyNTdU8`) e `Ligações com transcrição`
(`JejovPl6Vf0SBtAiVIpw`) — todos com `dateAdded` entre 16:38 e 16:56 UTC de
hoje, ou seja, **depois** da leitura das 16:13 UTC que registrou "os campos
C-29 a C-32 continuam ausentes" (entrada abaixo, "A sessão na nuvem não tem
como montar W18/W19/W20…") e **depois** do último commit desta sessão na
nuvem (`0539aa3`, 16:35). Quem criou foi o dono, direto na tela — mesma
classe de evento já registrada aqui para os 5 campos de S-01/C-25–C-28
("Fase 2 começou fora de ordem") e para as 6 tags do F-05/F-13
(`GUIA-MONTAGEM.md`, "Estado final em 22/09/2026", item 3): trabalho que
acontece fora desta sessão e não espera o documento ser lido de novo para
existir.

**Não escrevi nada:** os quatro campos existem e estão vazios (nenhum
contato lido tem valor neles ainda) — não é o mesmo caso das 6 tags (que já
apareciam aplicadas em workflow publicado); aqui é só a estrutura, pronta
para receber valor quando o W20 rodar. **O que isso destrava e o que não
destrava, exatamente:** o pré-requisito "campo existe" do F-06/W20 está
resolvido; o pré-requisito "toda ligação de saída gravada" (LGPD + custo do
add-on Voice Intelligence, `APROVADO.md`) **não** — é ele, não mais a falta
de campo, que segura o W20 agora. Registrado em `APROVADO.md` (linha dos
quatro campos) sem marcar `[x]`, pela mesma regra de sempre: campo na tela
sem `[x]` aqui é o dono decidindo, não a rotina se autorizando.

**Regra prática, generalizável, mesma do achado do G-04 nesta rodada:**
quando parte do trabalho acontece fora desta sessão (a tela, o PC do dono),
uma leitura de 3 horas atrás pode já estar errada — reconferir por API
antes de repetir "continua ausente"/"aguardando o dono" é mais barato que
supor que nada mudou.

## Conferi o achado do Clique antigo e ele estava completo — a varredura virou script — 22/09/2026, sessão automática

O dono achou, no PC, que o `Mestre de saída v2` removia o lead do
`Interceptação de Sinal — Clique` **antigo** em vez do v2 no ar, e corrigiu.
A pergunta que importa depois de um achado assim não é "está certo?", é
**"quantos mais existem?"** — a troca das 5 cópias v2 poderia ter deixado o
mesmo id velho em qualquer outro nó.

Varri de forma independente todos os dumps e achei **exatamente um**: o que
ele já corrigiu. As outras 5 referências cruzadas apontam para workflow no
ar e estão certas:

| Workflow | Nó | Aponta para |
|---|---|---|
| `Mestre de saída v2` | 6 | Clique **antigo** — já corrigido ao vivo |
| `Pós-agendamento v2` | 4 | `Recuperação de No-show`, `SLA do Closer — No-show`, `Cadência 12x30` |
| `Pós-ligação v2` | 54 e 127 | `Cadência 12x30` |

**O achado dele era completo, não parcial.** Vale registrar porque o
resultado natural de uma varredura de bug mecânico é achar mais um, e aqui
não havia mais.

**Limite da minha conferência, que não anula a dele:** os dumps cobrem **30**
workflows com id; ele varreu **38** ao vivo. Os ~8 sem dump neste repositório
são invisíveis para mim, e o dump é fotografia de antes de publicar — por isso
o `Mestre de saída v2` ainda aparece com o id velho aqui mesmo já corrigido no
CRM. A varredura autoritativa é a dele, pela API interna; a minha corrobora
dentro do que alcança.

**Virou ferramenta:** `wesales/tools/auditoria_refs.py`, somente leitura, sai
com código 1 se algum workflow apontar para arquivado. É a regra dele — "antes
de apagar um workflow, procure o id dele em todos os outros" — como comando em
vez de lembrete, porque a exclusão dos 10 rascunhos ainda vai acontecer e essa
é a hora exata em que o erro custa caro.

## O Mestre de saída v2 removia o lead do Clique ANTIGO, não do v2 que está no ar — 22/09/2026, PC do dono

Achado ao preparar a limpeza dos rascunhos: antes de apagar qualquer workflow,
varri os 38 restantes procurando o id dele. Um publicado apontava para um
desligado — o nó `Remove from Workflow` do `Mestre de saída v2`
(`c616e2d7…`) ainda tinha `ea0a49b7…` (Interceptação de Sinal — Clique,
antigo). A cópia v2 herdou o id e a troca v2 não o remapeou. Efeito: lead que
saía do funil continuava dentro do `Clique v2` (`30b5fc0d…`).

**Corrigido** trocando só o id do nó, preservando status, re-entry, janela e
os 3 gatilhos (conferido por leitura depois). Backup do antes em
`workflows-json/_arquivo/`.

**Regra:** toda cópia v2 tem de remapear também os ids de workflow dentro de
`remove_from_workflow` / `add_to_workflow`, não só os gatilhos. E antes de
apagar um workflow, procure o id dele em todos os outros.

## Estado da limpeza e dos três que faltavam — 22/09/2026, PC do dono

- **Limpeza:** backup dos 10 alvos em `workflows-json/_arquivo/` (5 `ZZ TESTE`
  + as 5 versões antigas substituídas por v2). A exclusão em si ficou para o
  dono — a ferramenta desta sessão exige autorização direta para apagar.
- **W19 Higiene de Número:** fora por decisão do dono (Number Validation não
  será ligado agora).
- **W20 Qualidade da Conexão:** o dono respondeu que **as ligações saem pelo
  CRM (LC Phone)** — a pré-condição 7 está resolvida. Os campos C-29 a C-32
  ainda **não existem** (lidos por API) e gravação+transcrição (add-on pago,
  aviso LGPD) não estão ligados.
- **W18 Monitor de Capacidade:** o gatilho real é `scheduler_trigger`
  (condição `scheduler.interval` = `hourly|daily|weekly|monthly|cron`,
  `scheduler.weekly.days` / `scheduler.weekly.times`, `schedule_config` com
  `skip_weekends`/`stop_at`), lido do bundle do builder. O mesmo bundle marca
  esse gatilho com `requiresInternalAccess` e o **esconde em produção** para
  conta sem acesso interno — ainda não confirmado na tela desta subconta.

## Dois campos com o mesmo nome em objetos diferentes seguraram um workflow — 22/09/2026, sessão automática

O `GUIA-MONTAGEM` registrava, como decisão pendente do dono, que **a
subconta está `country: "US"`**, e usava isso como parte do motivo de o W19
(Number Validation) não ter sido montado: "checaria número brasileiro contra
regra americana".

Medido: a subconta é **`BR`** — `locale: pt_BR`, São José dos Campos/SP, CEP,
`BRL`, fuso `America/Sao_Paulo`. A rodada das 16:13 mediu o mesmo
independentemente. O `US` é real, mas vive em **outro objeto**: é o `country`
dos **contatos** que entram pelo formulário do Meta, já documentado na
Tabela L e reconfirmado hoje no `Carlos Andrade`.

O que torna isso mais que um detalhe: o conserto muda de lugar e de risco.
Na leitura errada, mexer em `country` da subconta "toca telefonia e
faturamento" (`saasSettings`, `twilioRebilling`) — caro e assustador, e por
isso ninguém mexeu. Na leitura certa, o que se ajusta é o **mapeamento do
formulário** (G-04), que não toca faturamento nenhum. E a preocupação com o
W19 **aumenta** em vez de sumir: `Number Validation` valida o telefone do
contato, e é justamente o contato que está marcado como americano com
número `+55`.

**A regra:** quando um campo justifica um bloqueio, confirme **de qual
objeto** ele foi lido antes de aceitar o bloqueio. `contact.country` e
`location.country` têm o mesmo nome, vêm em respostas parecidas e significam
coisas diferentes. Aqui o nome igual custou um workflow não montado e uma
"decisão do dono" que nunca foi dele — era medição errada.

**Padrão do dia, terceira vez:** o achado certo foi escrito num documento e
o documento vizinho seguiu afirmando o contrário. A rodada das 16:13 mediu
`BR` e anotou no `APRENDIZADOS`; o `GUIA-MONTAGEM` continuou dizendo `US` e
continuou usando o `US` como motivo. Medir não propaga — propagar é um passo
separado, e é o que mais falha neste projeto.

## A sessão na nuvem não tem como montar W18/W19/W20 pela API interna — o toolkit de `wesales/tools/` só roda no PC do dono — 22/09/2026 16:13 UTC, sessão na nuvem

Pedido: montar W19 (Higiene de Número), W18 (Monitor de Capacidade) e,
depois da resposta do dono sobre LC Phone (entrada acima), W20 (Qualidade
da Conexão) — os três pelo mesmo caminho que já criou W1-W17/W21/W22
(`wesales/tools/ghl_api.py` + `build_w*.py`, API interna
`backend.leadconnectorhq.com`, bearer capturado do navegador logado).

**Três verificações antes de registrar bloqueio, não suposição:**
1. `wesales/.local/_ghl_bearer.txt` (onde `ghl_api.py` lê o token) —
   **não existe** nesta sessão. O arquivo é gitignored de propósito (segredo,
   nunca commitado) e só nasce quando `renew.js` roda contra um Chrome já
   logado no WeSales.
2. `renew.js`/`login-capture.js` dependem de um **perfil de Chrome
   persistente e já autenticado** e de `CLI_PATH` apontando para
   `gohighlevel-cli/`, um diretório **fora deste repositório**
   (`os.path.join(_HERE, "..", "..", "gohighlevel-cli")`) — não existe nesta
   sessão, e `NODE_PATH_GLOBAL` em `ghl_api.py` está hardcoded para
   `C:\Users\sampa\AppData\Roaming\npm\node_modules`, confirmando que este
   toolkit foi escrito para rodar no Windows do dono, não num sandbox Linux
   remoto.
3. `curl` para `backend.leadconnectorhq.com` desta sessão devolve conexão
   recusada (`000`) — mesmo bloqueio de proxy já registrado para
   `help.gohighlevel.com` e outros domínios (G-05, "EGRESS_BLOCKED"), agora
   confirmado para o host da API interna também.

**As três batem na mesma causa: este ambiente é a sessão na nuvem (leitura
por `GHL-CRM`/API pública), não o PC do dono.** É a mesma divisão de
trabalho que já existia — os 27 commits que a fusão de hoje trouxe
(`3cc1c4b`) só existem porque rodaram do lado de lá. Aqui não dá para
criar workflow por API nenhuma: a pública nunca ofereceu isso (registrado
desde 18/09), e a interna precisa da infraestrutura acima.

**Um segundo motivo, independente do primeiro, para não escrever os
`build_w18.py`/`build_w19.py` mesmo como rascunho não executado:** todo
`build_w*.py` existente copia o formato de nó de um workflow **real já lido
desta subconta** (`ghl_api.py`, linhas 1-6: "formato de nó lido de workflows
reais, não de schema de terceiro"). Os gatilhos `Number Validation` (W19) e
`Scheduler` (W18) **nunca foram capturados** em nenhum workflow desta
subconta — não há exemplo real para copiar, só a suposição de nome escrita
na spec. Adivinhar o formato JSON desses dois gatilhos sem poder testar
contra a API repetiria a mesma classe de erro que este arquivo já
documentou duas vezes (campo/rótulo inventado pelo assistente de IA no
Pós-ligação e no Loop do closer) — aqui o custo seria maior, porque um
gatilho mal formado ou não publica ou publica e nunca dispara, calado.

**O que isto não bloqueia:** a resposta do dono sobre LC Phone (entrada
abaixo) é documentação pura, sem escrita no CRM — registrada. Confirmado
também nesta sessão, via API pública (`locations_get-location`): país `BR`,
fuso `America/Sao_Paulo`, batendo com a spec do W19; e via
`locations_get-custom-fields` (51 campos): os quatro campos do W20 (C-29 a
C-32) **continuam ausentes**, então mesmo destravado pela resposta do dono,
W20 tem um segundo pré-requisito não resolvido, igual ao que já estava
escrito na spec.

**Registrado para não redescobrir:** para montar W18/W19/W20 por este
caminho, a sessão que roda precisa ser a que tem o bearer e o Chrome
logado — ou seja, no PC do dono, do jeito que os outros 22 workflows já
foram montados. Uma sessão na nuvem sem essa infraestrutura não deveria
tentar de novo sem ela mudar.

## Resposta do dono à pré-condição do W20/F-06/F-08/F-09: as ligações saem por LC Phone — 22/09/2026 16:13 UTC, ao vivo em chat

Pablo confirmou, ao vivo, a pergunta que travava os três itens desde
21-22/09/2026 (`build-wesales.md`, seção 2.26/F-08, "Conferência do F-06";
`ROADMAP-SALES-ENGAGEMENT.md`, F-09): **as ligações desta operação saem por
LC Phone** (telefonia nativa do GHL), não por linha própria do SDR. Bate com
o indício indireto já registrado (`twilioRebilling.enabled: true, markup: 20`
na config da subconta, reconfirmado nesta mesma leitura via
`locations_get-location`) — agora é confirmação, não mais indício.

**O que isso destrava, sem executar sozinho:**
- **F-06/W20 (Qualidade da Conexão):** o gatilho `Transcript Generated`
  passa a valer a pena montar — mas **ainda faltam os 4 campos
  pré-requisito** (`Duração da ligação` C-29, `Conexão real` C-30,
  `Conexões reais telefone` C-31, `Ligações com transcrição` C-32, todos
  `[ ]` em `APROVADO.md`), confirmados ausentes nesta rodada
  (`locations_get-custom-fields`: 51 campos, nenhum dos quatro) — e a
  decisão de operação que o pré-requisito esconde (gravar toda ligação de
  saída, aviso de LGPD, custo do add-on) continua sem `[x]` do dono.
- **F-08/F-09 (proteção de reputação e freio do canal de telefone):** a
  pendência "LC Phone ou linha própria?" que bloqueava a escolha do limiar
  de `Tel não atendidas seguidas` (F-09) e a mitigação certa de reputação de
  número (F-08) está resolvida — os dois continuam esperando o dono escolher
  entre as opções já escritas (`ROADMAP-SALES-ENGAGEMENT.md`), não mais a
  pergunta de infraestrutura.

Nenhuma escrita no CRM por causa desta resposta — é registro de decisão,
não execução.

## Dois itens certos, escritos com meio dia de diferença, viram um errado — 22/09/2026, sessão automática

O F-14 (rampa de aquecimento do telefone) e a decisão de 100% telefone
entraram no mesmo dia, com ~40 minutos entre um e outro, por sessões
diferentes. Cada um está certo sozinho. Juntos, quebram:

- o F-14 dimensionou a rampa dizendo que o telefone carrega **8 de 12**
  toques. Depois da decisão são **12 de 12**;
- o lote de 10-13 leads/dia do G-03 cabia na rampa: 12, 24, 24, 23, 11
  ligações nos cinco primeiros dias, encostando no teto de ~20-25 sem
  passar;
- com o telefone sozinho vira 24, 48, 48, 58, 34 — **2,3× o teto da semana
  1, já no dia 2**.

Ninguém errou uma conta. O que faltou foi alguém **multiplicar de novo**
depois que a premissa mudou.

**A regra que fica:** quando uma decisão muda uma premissa numérica (aqui,
quantos toques por canal), o trabalho não é achar os textos que citam a
premissa — é achar os **números que foram calculados com ela**. Texto
vencido se lê e se desconfia; número vencido parece certo, porque um teto
de "~20-25/dia" continua com a mesma cara depois que o que entra nele
dobrou. Foi o mesmo tipo de armadilha do erro de 2× do F-10, só que ao
contrário: lá eu errei a conta, aqui a conta estava certa e a entrada
mudou embaixo dela.

**Operacionalmente:** depois de qualquer decisão de canal, capacidade ou
volume, reabrir todo item que tenha tabela com "por dia", "por semana" ou
"teto" e refazer a multiplicação. São poucos e valem a rodada.

## A auditoria de órfãos mudou de gabarito: 6 linhas viraram 2 — 22/09/2026, sessão automática

A varredura de merge field órfão passou rodadas inteiras devolvendo
**6 linhas esperadas**. Nesta rodada devolveu **2**, e a queda não é defeito:
o dono criou na tela os 5 campos pendentes da tabela 1.2 (`3740858`), então
4 dos 6 "órfãos" deixaram de ser órfãos por terem virado campo de verdade.

**Gabarito novo — 2 linhas, as duas falsos positivos conhecidos:**

| Linha | Por que não é órfão |
|---|---|
| `contact.checkpoint_data_de_retorno` | citação deliberada do erro de 1 underscore, dentro da entrada que ensina o erro. Nunca foi uso. |
| `contact.name` | merge field nativo do GHL, não é campo personalizado |

Duas regras saem daí. A primeira: **número esperado de uma auditoria é estado,
não constante** — quando a realidade muda a favor, o gabarito precisa mudar
junto, senão a rodada seguinte "descobre" uma melhora e vai investigar o
próprio sucesso. A segunda: a fonte dos campos reais agora é
`wesales/tools/campos.json` (dump do PC, 79 entradas, 66 de contato), não mais
uma leitura da API a cada rodada — é de graça e não gasta os ~8-9k tokens de
`locations_get-custom-fields`. O preço é que o `campos.json` envelhece: se o
dono criar campo na tela, ele some da auditoria até alguém redumpar.

Comando com a fonte nova:

```
grep -rho "contact\.[a-z0-9_]*" wesales/*.md | sort -u > /tmp/usados.txt
python3 -c "import json;d=json.load(open('wesales/tools/campos.json'));\
print('\n'.join(sorted({v['chave'] for v in d.values() \
if isinstance(v,dict) and str(v.get('chave','')).startswith('contact.')})))" > /tmp/reais.txt
comm -23 /tmp/usados.txt /tmp/reais.txt | grep -v '^contact\.$'   # espera 2 linhas
```

## Um dump uniforme é suspeita de artefato, não descoberta — 22/09/2026, sessão automática

Os 22 arquivos de `workflows-json/` vieram todos com `status: draft` e
`triggers: []`. A leitura tentadora era "nada está no ar, o build não
publicou" — e ela seria espetacular e errada: o próprio `GUIA-MONTAGEM`
lista 20 workflows publicados com rastro lido pela API.

O sinal que salvou foi a **uniformidade**. Quando um defeito aparece em
100% dos casos, sem uma única exceção, quase nunca é defeito: é
característica de como o artefato foi produzido. Defeito real tem
distribuição irregular — alguns sim, outros não. Aqui o dump era a
fotografia do payload antes de publicar, e o gatilho é gravado por outra
chamada que nunca entra no arquivo.

**Regra:** antes de concluir a partir de um arquivo, pergunte em que
momento ele foi escrito e o que ele não teria como conter. E quando o
resultado for 100% ou 0%, desconfie da medição antes de desconfiar do
sistema. Parente próximo do "ler não é escrever" de ontem: ali o erro era
tomar limite de tela por limite de comportamento; aqui, tomar limite do
dump por estado do CRM.

## Uma decisão de canal viaja pelo código e fica presa nos documentos — 22/09/2026, sessão automática

O dono tirou o WhatsApp das réguas (`d52e61d`). A decisão chegou 100% ao
CRM — medi no payload publicado: 12 nós `add_contact_tag` com `fila-tel` e
**zero** adicionando `fila-wa`, que só sobrevive em nós de remoção. Mas
chegou a **2 documentos de 10**: sobraram 60 menções em `build-wesales.md`,
36 em `IMPLEMENTACAO-WORKFLOWS.md` e 11 no `ROADMAP`.

O caso é pior que inconsistência de texto, por dois motivos que valem como
regra:

1. **Documento de montagem é instrução, não descrição.** Enquanto o
   `IMPLEMENTACAO-WORKFLOWS` mandar criar toque de "Ligação WhatsApp", a
   próxima montagem reintroduz um canal que a conta não tem. Documento
   vencido não fica só errado — ele desfaz a decisão na montagem seguinte.
2. **Tag morta não é inofensiva.** `fila-wa` deixou de ser aplicada, e a
   fórmula do `Estouro da Fila` somava `fila-tel` **OU** `fila-wa`: ela
   continua contando resíduo e pode disparar alarme de capacidade sem fila
   nenhuma. E o F-05 peça 2 tinha um gatilho `Contact Tag Added — fila-wa`,
   que a partir de agora nunca dispara. Quando um canal sai, o trabalho não
   é achar as menções: é achar **o que dependia delas**.

Não reescrevi as 107 menções — seria alteração em massa sem pedir. Pus a
decisão medida num lugar só (seção 2.5 do `build-wesales.md`), avisos no
topo dos dois documentos que mandam montar, e corrigi no lugar os três
pontos carregantes.
## Dois itens que fecharam no mesmo dia, protegendo canais vizinhos, não se olharam — a pergunta que achou o F-14 não foi "o que falta", foi "os dois já tratam igual?" — 22/09/2026, sessão automática

O F-07 (Quality Rating do WhatsApp) e o F-08 (reputação do número de
telefone) fecharam no mesmo dia, um logo depois do outro, os dois pela
mesma pesquisa de mercado e o mesmo tipo de achado (recurso nativo da
plataforma não serve, vira checklist do gestor). O F-07 saiu com um objeto
concreto — Tier de número novo, teto que sobe em 7 dias. O F-08 saiu só com
"distribua entre números antes de escalar", sem cronograma. Ninguém
comparou os dois depois de prontos porque cada rodada fecha o item que está
fazendo e segue — a pergunta "o vizinho que acabou de fechar tratou o mesmo
risco com a mesma régua?" nunca é a pergunta natural de quem está dentro do
item.

**A técnica, generalizável:** quando dois itens resolvem o mesmo tipo de
problema (aqui: proteção de reputação de canal) para dois canais diferentes
da mesma cadência, e os dois fecham perto um do outro, vale a pena reabrir
os dois lado a lado e perguntar **não** "o que falta no roadmap" (pergunta
ampla, já esgotada por várias rodadas) mas "estes dois pares têm a mesma
profundidade de tratamento?" — é uma busca muito mais estreita que "achar
lacuna nova", e por isso mais barata de responder. Foi assim que nasceu o
F-14 (`ROADMAP-SALES-ENGAGEMENT.md`): o WhatsApp tinha Tier com números por
semana, o telefone não tinha nada além de "cuidado, distribua". Mesma
família de achado do G-06 (guarda de janela chegou ao Caminho A e não ao
Caminho B do mesmo workflow) e do F-08→F-09 (freio de "não atendidas
seguidas" existe no WhatsApp e não existia no telefone) — a terceira vez que
"protegido num canal, esquecido no gêmeo" aparece neste projeto. Vale
promover a pergunta a rotina: toda vez que um item de proteção de canal
fechar, perguntar se o canal irmão já tem o mesmo nível de cuidado, não só
se ele tem proteção nenhuma.

**Achado que só apareceu ao medir para escrever este item, não ao
procurá-lo:** a soma na entrada do F-13 ("47 `NOVO LEAD` + 2 `NEGOCIAR`
open + 1 `NEGOCIAR` lost + 2 `CONECTAR` lost") dava 52, não os 50
oportunidades que a mesma frase afirmava. A leitura fresca por API
(`opportunities_search-opportunity`, `status=all`) deu 45/2/1/2 = 50 — a
etapa `NOVO LEAD` estava contada como 47 por engano (provavelmente
confundindo com uma leitura anterior, de antes de dois contatos de teste
saírem para `CONECTAR`/`lost`). Mesma classe de erro do F-10 ("46 horas"
que não batia com as duas datas ao lado): aritmética manual sobre números já
escritos no próprio documento, não fonte externa errada. Corrigido na
mesma linha (`ROADMAP-SALES-ENGAGEMENT.md`); os outros ~15 lugares que ainda
dizem "47 `NOVO LEAD`" são snapshots históricos de datas anteriores em que o
número provavelmente era mesmo esse — não foram tocados, por serem registro
de outro dia, não a mesma frase se contradizendo.

## O teste que responde a dúvida das sete listas estava preso atrás de uma decisão que ele não precisa — e a lista que o destrava é a mais urgente do projeto — 22/09/2026, sessão automática

A rodada anterior fez a coisa certa com a dúvida da ordenação de dois níveis:
esgotou três caminhos de pesquisa (WebFetch bloqueado pelo proxy, WebSearch por
vários ângulos sem confirmação, documentação da API) e, em vez de deixar nota de
rodapé, transformou em **teste de 10 segundos** no `GUIA-MONTAGEM.md`. Duas
precisões e uma reordenação.

**1. O achado da API não serve para testar, só para raciocinar.** A rodada achou
que o endpoint oficial `Search Contacts` aceita array de ordenação multi-campo —
bom sinal de que a plataforma modela isso na camada de dados. Mas **este conector
não implementa esse endpoint**: o `contacts_get-contacts` que temos é o
*deprecated* `/contacts/`, e o schema dele **não tem parâmetro de ordenação
nenhum** (conferido campo a campo: `locationId`, `query_limit`, `query_query`,
`query_startAfter`, `query_startAfterId`). Ou seja, não dá para testar multi-sort
nem no nível da API a partir daqui. Registrado para ninguém tentar.

**2. O teste foi parar na Fase 6, e a Fase 6 está bloqueada.** A instrução ficou
em "antes de configurar a ordenação das 8.1, 8.2, 8.3, 8.4, 8.16, 8.18 e 8.19" —
todas da Fase 6, que espera a decisão da coluna `Empresa` (Tabela J). Então o
teste herdou um bloqueio que **não é dele**: qualquer Smart List aberta responde
a pergunta, não só aquelas sete.

**3. E existe uma lista que não espera nada — e que por acaso é a mais urgente do
projeto.** As duas do F-10 (`Entrada — últimas 24h` / `— 7 dias`, seção 8.25):

| | Por quê |
|---|---|
| Não dependem da Tabela J | tirei a coluna `Empresa` da definição — ela está vazia em 100% da base e o trabalho da lista é **contar chegada**, não qualificar. Nas outras sete a coluna morta atrapalha a leitura do SDR; aqui não existe |
| Ordenação de um nível só | `Data de criação` desc — montam inteiras independentemente da resposta |
| Respondem a pergunta de graça | quem montar está com a tela de Smart List aberta e olha em 10 segundos se há `, depois` |
| São o único monitor de entrada que existe | e a entrada está parada há mais de 1,9× o maior intervalo já observado (F-10) |

**A lição, que é sobre onde se pendura uma verificação:** um teste barato
herda o bloqueio do lugar onde é escrito. Antes de anexá-lo a uma fase,
perguntar **qual é o primeiro momento em que ele poderia acontecer** — e
pendurá-lo ali. Aqui a diferença é entre "quando o dono decidir a coluna
`Empresa`" e "na próxima vez que alguém abrir uma Smart List", que pode ser
hoje. Mesmo raciocínio das conferências acopladas do F-06 e do R-14, agora
aplicado no sentido inverso: não basta acoplar ao passo certo, tem de ser ao
passo **mais cedo** que serve.

## Ordenação secundária de Smart List: pesquisa não resolve, só a tela resolve — três abordagens diferentes, todas inconclusivas — 22/09/2026, sessão automática

A rodada anterior (nota abaixo) deixou em aberto se a Smart List do GHL
aceita ordenação por dois níveis (`, depois`), usada em sete listas (8.1,
8.2, 8.3, 8.4, 8.16, 8.18, 8.19). Esta rodada tentou fechar a dúvida por
pesquisa, três caminhos genuinamente diferentes:

1. **`WebFetch` direto nas páginas oficiais e em blogs de terceiros**
   (`help.gohighlevel.com`, `ideas.gohighlevel.com`, `marketecs.com`,
   `ghlbuilds.com`, `glama.ai`) — **todas bloqueadas pelo proxy deste
   ambiente** (`EGRESS_BLOCKED`), mesma barreira já registrada no G-05. Não é
   falha de busca, é o ambiente: nenhuma dessas páginas é alcançável por
   `WebFetch` aqui, só por `WebSearch` (que resume via outro caminho).
2. **`WebSearch` com várias frases** (documentação oficial, portal de ideias/
   feature requests, blogs de terceiros, fóruns de comunidade) — nenhuma
   retornou confirmação em nenhum dos dois sentidos. A documentação descreve
   "definir ordenação" no singular, nunca menciona um segundo nível, e não
   achei um pedido de feature explícito sobre isso no portal de ideias — mas
   ausência de menção não é o mesmo que confirmação de limite.
3. **API oficial (não a tela) —** achado novo, não estava registrado antes: o
   endpoint `Search Contacts (Advanced)` documentado em
   `marketplace.gohighlevel.com/docs/ghl/contacts/search-contacts-advanced/`
   aceita um **array** de objetos de ordenação (`[{"field": "dateAdded",
   "direction": "desc"}, ...]`) — a API, portanto, suporta múltiplos critérios
   de ordenação. Isto **não prova nada sobre a Smart List da tela** (Contatos
   → Filtros → salvar como lista inteligente é UI, não é este endpoint), mas
   derruba a hipótese de que "a plataforma não pensa em ordenação de mais de
   um campo" — ela pensa, pelo menos na API. A pergunta que fica em aberto é
   estritamente sobre o que o construtor visual expõe, não sobre a
   capacidade da HighLevel.

**Conclusão prática, registrada para não repetir a mesma busca:** esta dúvida
**não fecha por pesquisa neste ambiente** — os domínios que teriam a resposta
definitiva (página de suporte, portal de ideias) estão bloqueados para
`WebFetch`, e o `WebSearch` já foi tentado por três ângulos diferentes sem
achar a frase que resolve. A única verificação que resta é abrir a tela e
tentar configurar um segundo critério — por isso a Fase 6 do
`GUIA-MONTAGEM.md` ganhou um passo explícito pedindo esse teste de 10
segundos no momento da montagem, com o Plano B (já escrito em
`build-wesales.md`, seção 8.4) pronto para quem encontrar o limite. Não vale
a pena uma quarta rodada de `WebSearch` sobre o mesmo tema até a tela
confirmar ou refutar.

## "Já fazemos assim em outros N lugares" é consistência, não evidência — e o `grep` diz exatamente quantos lugares estão em risco — 22/09/2026, sessão automática

A rodada fechou uma contradição real (a lista `Retornos` ainda descrevia o
mundo de antes de `Hora do retorno` existir, enquanto o ramo `Pediu retorno`
já a dava como atualizada — contradição que **eu** criei de manhã ao fechar a
L-01 em quatro documentos e esquecer o quinto). Boa pegada. Mas a justificativa
da ordenação nova merece atenção:

> "`Data de retorno` asc, depois `Hora do retorno` asc (**mesmo padrão de dois
> níveis de 8.1/8.2/8.3**)"

Isso não verifica nada. As três listas citadas **também nunca foram montadas na
tela**. `grep "^| Ordenação | .*, depois "` devolve **sete** listas com
ordenação de dois níveis. Se a Smart List do GHL não aceitar ordenação
secundária, o desenho está errado em sete lugares — e a consistência entre eles
**esconde** o problema em vez de denunciá-lo: tudo combina, logo tudo parece
certo.

Pesquisa desta rodada: a documentação descreve ordenação e gestão de colunas
como recursos da Smart List, mas **não achei confirmação de ordenação por mais
de uma coluna**, e há pedido de usuário aberto sobre limitação de ordenação em
lista de contato. Não afirmo que não existe — afirmo que ninguém verificou, e
que a justificativa usada não verifica.

**Regra, e é sobre como se justifica uma escolha de plataforma:** quando a
capacidade nunca foi testada, "já usamos em N lugares" **multiplica** o risco
em vez de reduzi-lo. A frase certa é "assumimos isso em N lugares, e o `grep`
que conta N é o tamanho do estrago se estiver errado". O número vem de graça e
transforma uma nota de rodapé numa prioridade — ou, neste caso, mostra que o
plano B cabe em uma linha por lista (ordenar pelo primeiro nível, deixar o
segundo como coluna visível, que já está em todas as sete).

**Distinção que vale separar da anterior:** esta não é a classe "premissa
negativa não pesquisada" (aquela era sobre o mundo lá fora). É sobre **a
própria base de código/documento como fonte de autoridade** — o documento cita
a si mesmo, e a repetição vira evidência aparente. O sintoma é a palavra
"mesmo" numa justificativa: *mesmo padrão*, *mesmo raciocínio*, *igual ao que
já fazemos*. Quando aparecer, perguntar: e aquele lugar, foi verificado contra
o quê?

**Segundo achado, pequeno e certo:** `Hora do retorno` é `TEXT`, e `TEXT`
ordena por letra. Com `HH:MM` zero-padded a ordem alfabética coincide com a
cronológica — é por isso que o placeholder é `HH:MM`. Mas `9:30` digitado sem o
zero cai **depois** de `14:00`, porque `'9' > '1'`. O placeholder não impede,
só sugere; foi para o `script-de-ligacao.md`, seção 2, que é onde está quem
digita.

## O dono está executando o checklist na tela agora — estado capturado às 12:50, e a tag nº 16 nasceu fora de todo documento — 22/09/2026, sessão automática

Primeira atividade de montagem na tela desde 21/09 23:33, e a primeira vez que
o **checklist de teste da seção 10** é de fato exercitado. Capturado por API às
12:50 UTC, pelos `dateUpdated`:

| Contato de teste | `dateUpdated` | O que mudou |
|---|---|---|
| `Teste Não Atende` (`OIvOGQfdGg2Ndr5GtcAG`) | **11:59:23** | tags `limpar-tarefas` + **`toque`**; `Total de ligações` = 2, `Tentativas telefone` = 2, `Toques na semana` = 1, `Tentativa nº` = 0 |
| `ZZ TESTE ESTRUTURA` (`c5r3ZxiAd8T5adL1Bt6j`) | **12:06:24** | `Toques na semana` = 1 |
| `Teste Número Errado` (`qkHSdIMPJTB2JK5ECGrY`) | **12:08:35** | `Resultado da tentativa` = **`Não ligar`**, DND **nos 6 canais** (por workflow), tags `nao-perturbe` + `limpar-tarefas`, oportunidade movida para `CONECTAR` 12:05 e `lost` 12:08 |
| `Teste Retorno` (`vrwdERfR24ax6GylG6No`) | **12:08:47** | idem — `Não ligar`, DND 6 canais, `CONECTAR` 12:00 → `lost` 12:08 |
| `Teste Atendeu` (`Lj96CIFYaGKPiC0opzbc`) | **12:38:07** | `Nota de qualificação` **80 → 93**, tag nova **`teste-regua`** |
| `Teste Não Ligar` (`2MXzDPjxGjuvvsxlp5V1`) | 18/09, intocado | tags vazias — cenário ainda não rodado |

**1. Existe uma 16ª tag na subconta, criada na tela: `teste-regua`.** `grep -rn
"teste-regua" wesales/*.md` retorna **vazio** — ela não está em
`campos-e-tags.md`, não está em `APROVADO.md`, não está em nenhum nó. É
marcador de teste do dono, inofensivo, e **não deve ser tratada como órfã nem
entrar em lista de limpeza**: registrar aqui é o que evita uma rodada futura
"descobrir" e tentar consertar. Vale a regra geral: **tag que aparece na tela e
não está em documento nenhum é do dono até que se prove o contrário** — o
caminho é perguntar, nunca remover (regra 1 do briefing).

**2. `CONECTAR` deixou de ser sempre-zero.** A auditoria diária das 10:31
registrou `CONECTAR`/`AGENDAR`/`FORMALIZAR` com **zero** oportunidades desde
sempre. Entre 12:00 e 12:08 duas oportunidades de teste passaram por
`CONECTAR` antes de virar `lost`. A frase "nenhuma cadência publicada moveu um
lead sequer" continua verdadeira **para lead real**, mas deixou de ser
verdadeira para o pipeline — quem reler aquela entrada precisa desta ressalva.

**3. O `Não ligar` funciona ponta a ponta, e é a primeira prova disso.** Nos
dois contatos: `Resultado da tentativa` = `Não ligar` → DND ativo nos **seis**
canais com `message: Updated from workflow_cf6fa19d-…` → tag `nao-perturbe` →
`status` = `lost` **sem sair de `CONECTAR`**. É exatamente o ramo `Não ligar` da
seção 4 como especificado, incluindo a decisão de que o `status` muda e a etapa
não. Nenhum dos dois ganhou `telefone-invalido` nem `fila-quente`, coerente com
o ramo escolhido (os cenários originais daqueles contatos eram outros — o dono
testou o `Não ligar` neles, não o cenário do nome).

**4. A auditoria do F-12 que eu propus 1h antes, rodada de verdade:** filtro
`status = lost` devolve **3** oportunidades (`Teste Número Errado`, `Teste
Retorno`, `Teste Atendeu`) e **todas as três com `lostReasonId: null`**. Linha
de base: 0% preenchido. O comando funciona, e é exatamente a divergência que o
item existe para impedir — agora com número em vez de hipótese.

**5. Um dado que não dá para interpretar, e por isso fica como dado:**
`Nota de qualificação` do `Teste Atendeu` foi de **80 para 93** entre 11:00 e
12:38. Pode ser o nó 4 do Pós-agendamento finalmente gravando, pode ser o
veredito do closer, pode ser edição manual. **Não conclua que o nó 4 foi
corrigido** — os dois leads reais em `NEGOCIAR` (`Daniel`, `genilson |
Bombeiro`) continuam com o campo vazio, que é o teste que vale. Mesma ressalva
que a auditoria diária já tinha levantado, agora com um número novo que
tentaria desmenti-la.

**Por que capturar isso importa:** estado de tela muda sem aviso e não tem
histórico legível por API além do `dateUpdated`. Quando o dono voltar e
perguntar "em que pé está", a diferença entre "o checklist começou" e "o
checklist não começou" é esta tabela — e ela existe por dez minutos de leitura,
não por acesso à tela.

## Auditoria diária (só leitura): a entrada piorou de ~22h47 para ~25h14 sem lead novo, e o rastro de teste do closer não prova nada sobre lead real — 22/09/2026, sessão automática (auditor diário)

Primeira rodada do **Auditor diário** (read-only, sem conector de tela,
compara contra o "Estado bruto para a próxima leitura comparar" no fim de
`GUIA-MONTAGEM.md` e contra a medição do F-10 desta mesma manhã em
`ROADMAP-SALES-ENGAGEMENT.md`/`APRENDIZADOS-CRM.md`). Lido por API às
22/09 10:31 UTC: **50 contatos, 50 oportunidades** (inalterado) — **47
`NOVO LEAD`** + **2 `NEGOCIAR` `open`** + **1 `NEGOCIAR` `lost`** (era 3
`open`; ver achado 2). `CONECTAR`, `AGENDAR` e `FORMALIZAR` seguem com
**zero** oportunidades — nenhuma cadência publicada moveu um lead sequer
desde sempre, confirmado de novo.

**1. F-10 não é mais "~22h47" — é "~25h14", 1,67× o maior intervalo já
visto (15h06).** Excluindo os 7 contatos de teste/estrutura (`Lj96CIFYaGKPiC0opzbc`,
`OIvOGQfdGg2Ndr5GtcAG`, `vrwdERfR24ax6GylG6No`, `qkHSdIMPJTB2JK5ECGrY`,
`2MXzDPjxGjuvvsxlp5V1`, `c5r3ZxiAd8T5adL1Bt6j`, `eNqNOQI7FT2CBwYAHGrN`), 41
oportunidades reais em `NOVO LEAD`. O lead mais novo continua sendo
`Carlos Andrade`, `createdAt` **21/09 09:17:26** — nenhum lead novo chegou
desde a medição do F-10 desta manhã. Às 22/09 10:31 UTC isso é **25h14min**,
contra os ~22h47min medidos ~2h30 antes: a régua "múltiplo do pior caso"
que a correção do F-10 estabeleceu segue valendo e agora mostra 1,67× (era
1,53×). Nenhuma tag de alarme do F-05 apareceu em contato nenhum — **é o
esperado, não um sinal de saúde**: as 5 tags (`novo-lead-estagnado`,
`fila-travada`, `conectar-estagnado`, `agendar-estagnado`,
`retorno-vencido`) continuam `[ ]` em `APROVADO.md`, não existem na tela.
Mesma razão para zero `fila-tel`/`fila-wa` presa: nada entrou na cadência
para poder travar.

**2. `Teste Atendeu` saiu de `NEGOCIAR`/`open` para `NEGOCIAR`/`lost` entre a
leitura de 21/09 e agora — é rastro de teste manual na tela, não sinal de
operação real.** `dateUpdated` do contato: **22/09 00:45:58 UTC** (~10h
antes desta auditoria). Também ganhou, pela primeira vez, `Nota de
qualificação` = 80, `Motivo da desqualificação` = "Sem fit", `Reunião foi
qualificada` = "Não", `Data do veredito do closer` = 2026-09-21, e DND
ativo nos 6 canais — sinal de que alguém clicou manualmente o Loop do
closer (ou o SLA do Closer) nesse contato de teste. **Armadilha para a
próxima rodada:** não concluir daí que o nó 4 do Pós-agendamento (que
grava `Nota de qualificação`, achado aberto em 21/09) foi corrigido — os
dois leads **reais** que também estão em `NEGOCIAR` (`Daniel`,
`genilson | Bombeiro`) continuam com esse campo **vazio**, exatamente como
na leitura de 21/09. O preenchimento em `Teste Atendeu` é plausivelmente
escrito pelo veredito do closer, não pelo nó 4 — são dois nós diferentes
gravando o mesmo campo, e só um dos dois tem rastro de estar rodando.

**Regra generalizável:** contato de teste mudando de estado no meio da
noite, sem nenhuma rodada automática ter mexido em nada (`APROVADO.md`
vazio o tempo todo), é o dono testando na tela — trate como dado de
teste, nunca como amostra do que a operação real está fazendo, e não deixe
isso maquiar um achado aberto (aqui, o nó 4) como resolvido.

## Ler não é escrever: a flag de DND de WhatsApp é gravável num canal que a tela não mostra — minha própria conclusão de 1h antes, medida e refutada — 22/09/2026, sessão automática

Uma hora antes desta entrada eu escrevi, na conferência do R-14, que "quem
pede silêncio hoje não fica protegido em WhatsApp", porque a documentação diz
que as preferências de DND de WhatsApp/Messenger/GMB **só aparecem depois que o
app está integrado** — e esta subconta não tem WhatsApp integrado. Parecia a
mesma classe do F-10: falha que não acende luz, com o lead que pediu silêncio
recebendo a primeira mensagem no dia da integração.

**Medido, e é o contrário.** `contacts_get-contact` em `Teste Atendeu`
(`Lj96CIFYaGKPiC0opzbc`), contato que ganhou DND na noite de 21/09:

```
dndSettings: { Call, Email, SMS, FB, GMB, WhatsApp }  — todos status: "active"
message em todos: "Updated from workflow_cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc"
```

**`WhatsApp` está lá, ativo, escrito por um workflow, sem o canal estar
integrado.** O `Set Contact DND` grava os seis independentemente. Não há
problema de retroatividade, não há lead desprotegido, e a "mesma classe do
F-10" não existia.

**Onde o raciocínio quebrou, e é a lição:** a fonte falava sobre as
*preferências aparecerem* — sobre **a tela mostrar** e **o filtro oferecer**,
isto é, sobre **ler**. Eu apliquei a frase a **escrever**. São camadas
diferentes do mesmo sistema, e uma frase sobre a interface não é uma frase
sobre o dado.

**Regra:** antes de transformar um limite de interface em conclusão sobre
comportamento, pergunte de qual das duas a fonte estava falando — *exibir /
filtrar / selecionar* é leitura; *gravar / aplicar / disparar* é escrita. Um
limite de leitura quase nunca implica um limite de escrita, e é o erro mais
fácil de cometer quando a fonte é documentação de UI (que é quase toda a
documentação de plataforma que este projeto consegue ler, já que o proxy
bloqueia o portal oficial e sobra citação de busca sobre telas). **Teste
barato que eu tinha à mão e não usei:** um contato que já passou pelo caminho
— aqui bastava ler `dndSettings` de qualquer contato com `nao-perturbe`. A
medição existia antes da conclusão; foi só não ter procurado.

**O que sobrou do achado, no tamanho certo:** só a auditabilidade. Se o filtro
`WhatsApp DND` não aparecer na Smart List sem integração, as listas 8.26/8.27
se montam com a cláusula de ligação apenas — a **proteção** está inteira, a
**conferência** dela é que fica parcial. Deixou de ter ação de véspera.

**E um brinde que vale mais que o susto:** `dndSettings[canal].message` carrega
**o id do workflow que ligou aquele DND** (`Updated from workflow_cf6fa19d-…`).
Dá para saber *quem* silenciou um contato sem abrir a tela — exatamente o que a
lista 8.27 (`DND sem tag`) precisa, já que o propósito dela é achar o caminho
não documentado que ligou DND. `message` com `workflow_…` = régua; qualquer
outra coisa = clique ou API. Primeira ferramenta de rastreabilidade de workflow
que este projeto tem sem acesso à tela, e ela veio de uma leitura que eu fiz
para conferir um erro meu.

**Correção de detalhe na auditoria diária da mesma data** (entrada acima): ela
leu a mudança noturna de `Teste Atendeu` como "alguém clicou manualmente o Loop
do closer". O `message` do `dndSettings` diz `Updated from workflow_…`, então
**o DND, pelo menos, veio de workflow**, não de clique. As escritas de campo
custom no mesmo horário podem ter sido manuais — mas o DND não foi, e isso
muda a leitura: algum workflow rodou naquele contato às 00:45, o que é
informação útil e não ruído de teste.

## Espelho de "algum ligado" é "algum desligado", não "todos desligados" — e o filtro de DND de WhatsApp pode não existir antes do canal existir — R-14, 22/09/2026, sessão automática

A rodada que especificou o R-14 acertou a distinção que destrava o item (o que
espera volume é a **execução** da auditoria, não o **desenho**) e a pesquisa
que a viabiliza: Smart List do GHL filtra DND **por canal**, com os nomes
exatos `Calls & Voicemails DND`, `WhatsApp DND`, `SMS DND`, `Email DND`, `DND
all` e mais. Duas correções.

**1. Uma lista nasceu com `E` onde o par dela usa `OU`.** As duas listas são
espelhos:

| Lista | Filtro escrito | Certo? |
|---|---|---|
| 8.27 `DND sem tag` | (`Calls DND` = Enabled **OU** `WhatsApp DND` = Enabled) **E** tag ausente | **Sim** |
| 8.26 `tag sem DND` | tag presente **E** `Calls DND` = Disabled **E** `WhatsApp DND` = Disabled | **Não** |

Com `E`, a 8.26 só acusa quem está desprotegido nos **dois** canais. Contato
com a tag, ligação bloqueada e WhatsApp **livre** não aparece — e é justo um
lead que pediu silêncio e ainda recebe mensagem. E **proteção parcial é o
defeito mais provável** dos dois, porque basta um nó chamar `Set Contact DND`
num canal só. Consequência: "zero linha na 8.26" não provava o que o item diz
provar.

**A regra, e é de lógica, não de GHL:** quando duas listas são declaradas
espelhos, negue a condição **inteira**, não cada termo. Negação de "algum
canal ligado" é "algum canal desligado" (`OU`), nunca "todos desligados"
(`E`) — trocar `OU` por `E` ao espelhar é a forma mais comum de uma lista de
exceção ficar estreita demais **sem parecer errada**: ela continua devolvendo
zero linha, que é o resultado esperado, e por isso ninguém desconfia. Mesma
família do portão que só olhava etapa sem `status`: o teste passa, a cobertura
não existe.

**2.** ⚠️ **Esta segunda parte eu medi ~1h depois e estava ERRADA — leia a
entrada "Ler não é escrever" (mesma data, acima) antes de usar qualquer coisa
daqui.** O que segue era a conclusão da hora, mantida como registro do erro:
as preferências de DND de **WhatsApp, Facebook Messenger e GMB só aparecem
depois que o app está integrado à subconta.** Esta subconta **não tem WhatsApp
integrado** — é a razão de o R-14 esperar volume e de não existir uma mensagem
de WhatsApp aqui. Então:

- As duas listas se montam **pela metade** hoje (só a cláusula de ligação).
  Ainda vale montar: meia auditoria pega tag sem bloqueio nenhum.
- E o `Set Contact DND` "todos os canais" dos **quatro** nós que aplicam
  `nao-perturbe` (2.9.5, seção 4 ramo `Não ligar`, seção 6 nó 3, opt-out do
  R-17) **não pode ligar DND de um canal que não existe**. Quem pedir silêncio
  hoje fica protegido em ligação/SMS/e-mail e **não** em WhatsApp.

**Por que isto é da mesma classe do F-10 (a falha que não acende luz):** no
dia em que o WhatsApp for integrado, os contatos que já pediram para não ser
procurados podem nascer alcançáveis por WhatsApp — e a primeira mensagem da
cadência vai para quem pediu silêncio. Nenhum monitor pega isso, porque nada
mudou de estado no CRM: mudou o **conjunto de canais existentes**, que nenhum
alerta observa. `dndSettings` está `{}` em todos os contatos lidos, inclusive
no `Teste Não Ligar`, então não há como inferir por API se o GHL preencheria
retroativamente.

**Regra generalizável:** quando uma proteção é declarada "para todos os
canais", pergunte **quais canais existem no momento em que ela é aplicada** —
e o que acontece com os registros antigos quando um canal novo entra. "Todos"
é uma lista que muda de tamanho, e uma garantia escrita contra "todos" envelhece
sozinha sem avisar. Deixei as duas conferências **acopladas ao passo de
integração do WhatsApp** em `build-wesales.md` (8.26), com a única ação desta
área que tem prazo: reaplicar `Set Contact DND` nos contatos antigos **antes**
do primeiro envio, não depois.

## Smart List do GHL filtra por DND nativo, por canal — nunca citado em nenhum documento do projeto até o R-14, 22/09/2026, sessão automática

Procurando como desenhar o R-14 (auditoria de compliance, o único item do
roadmap que ainda não tinha nó nenhum desenhado): a pergunta era "dá para
comparar, numa lista, a tag interna `nao-perturbe` contra o estado real do
DND nativo do contato?" — nenhuma seção do projeto até aqui tinha filtrado
Smart List por DND, só aplicado DND via `Set Contact DND` (ação de
workflow, já em uso desde 18/09/2026).

**Achado por `WebSearch`** (`help.gohighlevel.com`/`consultevo.com`/
`growthable.io`, confiança média — página oficial citada em buscas com
termos diferentes, o proxy deste ambiente bloqueia leitura direta dos
domínios de suporte da HighLevel, mesmo padrão de confiança já usado para
o `Wait Dynamic` do F-05 e a janela de 24h do G-05): o filtro de Smart
List por DND existe e é **por canal**, não um booleano único — `DND all`,
`SMS DND`, `Email DND`, `Calls & Voicemails DND`, `WhatsApp DND`, `Inbound
DND`, `FB Messenger DND`, `GMB Messenger DND`, cada um com opção
Enabled/Disabled. Isso decidiu o desenho do R-14: comparar a tag
`nao-perturbe` (convenção interna, não bloqueia nada sozinha) contra
`Calls & Voicemails DND`/`WhatsApp DND` (bloqueio real de plataforma) numa
Smart List — mesma classe de "duas condições de contato diferentes" que
só Smart List resolve neste projeto (F-05/R-11 já bateram nesse limite
para contagem entre contatos; aqui é o mesmo limite para comparação de
dois campos do mesmo contato).

**Por que vale registrar:** é um filtro nativo que qualquer item futuro
envolvendo DND (novo canal, nova regra de opt-out) vai precisar — sem
essa busca, a suposição mais fácil seria "não dá para auditar DND sem
workflow novo", que é o erro que o F-05/R-11 já ensinaram a desconfiar.
Nome exato do filtro na tela em português ainda não confirmado — mesma
ressalva de sempre para achado só por busca, não por teste na subconta.

## O próprio F-10 errou a conta que ele mesmo tabulava — "46 horas" era quase o dobro do que as duas datas ao lado diziam — 22/09/2026, sessão automática seguinte

A rodada que abriu o F-10 (entrada abaixo, mesma data) fez tudo certo até a
última linha: mediu por API, conferiu que não era falha de workflow, achou o
gap estrutural real. E então escreveu, na própria tabela, `Lead mais novo:
21/09 09:17:23` e `Agora: 22/09 ~07:30`, e na linha seguinte `Tempo sem lead
novo: ~46 horas`. As duas primeiras datas, subtraídas uma da outra, dão
**22h13min** — quase exatamente metade do que a terceira linha afirma. O erro
não veio de uma fonte externa nem de uma suposição: veio de fazer conta errada
com os próprios números, escritos duas linhas acima, na mesma tabela.

**Como foi pego:** esta rodada reconferiu o CRM por rotina antes de decidir o
que fazer (mesmo lead mais novo, `Carlos Andrade`, ainda `21/09 09:17:23` —
nenhum lead novo chegou) e, ao recalcular o tempo decorrido para atualizar a
tabela, a conta não bateu com a que já estava escrita. `date -u` confirmou o
horário real da máquina (`22/09 08:04 UTC`) contra o `createdAt` devolvido
pela API (`2026-09-21T09:17:26Z`): 22h47min, não o dobro disso.

**O antídoto, achado ao conferir esta correção (22/09, mesma data):** não é
"refazer a conta com mais cuidado" — é **trocar a unidade por uma que se
calibre**. `~46h` passou porque hora absoluta não tem referência: 46h e 22h
soam igualmente plausíveis para quem não tem um "normal" na cabeça. O
intervalo entre chegadas **na própria base** tem referência embutida:

| Gap entre chegadas consecutivas | |
|---|---|
| Os 8 primeiros | 9 min a 3h06 |
| 20/09 07:32 → 17:47 | 10h15 |
| 20/09 18:11 → 21/09 09:17 | **15h06** ← maior já observado |
| 21/09 09:17 → agora | **23h02** ← **1,53× o maior já visto** |

Escrito como "1,5× o maior intervalo já observado", um erro de 2× na conta
vira absurdo na hora ("3× o maior já visto" não passa despercebido), enquanto
"46 horas" passa. **Regra: quando um número mede anormalidade, expresse-o em
múltiplos do pior caso já observado, não em unidade absoluta.** O erro de
aritmética continua possível; o que muda é que ele deixa de ser invisível.

Do mesmo cálculo saiu um número que ninguém tinha: na janela em que a entrada
funcionou (~34h30), chegaram 10 leads — **~7 leads/dia** contra a premissa de
**~10/dia** que dimensiona a régua inteira (L-05). Amostra pequena, não é
conclusão, mas é a primeira medição de entrada do projeto e vem abaixo da
meta. Anotado no F-10.

**Por que vale uma entrada própria, e não só a correção silenciosa:** é uma
classe de erro diferente das anteriores registradas aqui (premissa negativa
não pesquisada, configuração herdada lida como local, campo com dois donos).
Ali a fonte era externa e podia estar errada; aqui a fonte eram os próprios
dados já corretos na mesma tabela, e a aritmética sobre eles é que falhou — o
tipo de erro que nenhuma pesquisa adicional pega, só reconferir a conta com a
calculadora (ou `date -u` mais subtração) em vez de confiar no número que "soa
plausível" (46h também soa como "quase dois dias sem lead", frase que uma
operação de tráfego pago aceita sem estranhar).

**A regra:** todo número que expressa "tempo decorrido entre A e B" escrito
num documento merece a mesma verificação que um `fieldKey` adivinhado — não
porque a fonte é suspeita, mas porque é aritmética manual e aritmética manual
erra sem avisar. Antes de publicar uma conta de horas/dias, refaça a
subtração isolada (`date -u` + subtração, ou o equivalente) e confira contra
as duas datas que já estão escritas ao lado — se elas não batem com o
resultado, é a conta que está errada, não as datas. Propagou para **quatro
arquivos** (`ROADMAP-SALES-ENGAGEMENT.md` em três pontos, `APRENDIZADOS-CRM.md`,
`briefing-sdr.md`, `build-wesales.md`) antes de alguém recalcular — o mesmo
padrão de "número repetido vira mentira na rodada seguinte" que a coerência
entre documentos já vigia para nomes e contagens, agora para aritmética de
data. Os quatro corrigidos neste commit; a conclusão do F-10 (entrada parada,
sem monitor) não muda — só a magnitude.

## Seis monitores vigiam lead parado e nenhum vigia lead que não chegou — a falha que faz todos os indicadores melhorarem — F-10, 22/09/2026, sessão automática

Medido nesta rodada, por API: **50 contatos, 50 oportunidades**, e o lead mais
novo da subconta é de **21/09 09:17 UTC** — **~22h13min** atrás (esta entrada
originalmente dizia "~46 horas"; era conta errada, quase o dobro do real —
corrigido na entrada mais recente deste arquivo, que também generaliza a
regra). O padrão anterior era 9 leads em 19 horas (19/09 22:50 → 20/09 18:11),
depois 1 em 21/09 09:17, depois nada.

**Não é falha de workflow, e isso foi conferido antes de concluir:** contatos
e oportunidades batem um para um, e no lead real mais recente o contato nasceu
às 09:17:23 e a oportunidade às 09:17:**26** — três segundos, é a Porta de
Entrada (G-01) funcionando. Se o Meta entregasse, o CRM registraria. O que
parou está fora do CRM: campanha, orçamento, formulário ou criativo.

**O gap estrutural:** o Monitor de Saúde (F-05) tem seis peças e **todas as
seis vigiam lead que ficou parado** — estagnado em `NOVO LEAD`, fila travada,
`CONECTAR` sem avanço, `AGENDAR` estagnado, retorno vencido, teto de toques.
Nenhuma vigia lead que **nunca chegou**.

E é a falha mais consequente possível justamente porque é a única que faz
todos os outros indicadores **melhorarem**:

| Entrada parada | O painel mostra |
|---|---|
| Fila de ligação | esvazia |
| `NOVO LEAD` estagnado | para de crescer |
| Toques na semana | cai abaixo do teto |
| Alerta de speed-to-lead | silencia (sem lead, sem 1ª tentativa atrasada) |
| Taxa de conexão | **sobe** (sobram só os já trabalhados) |

Seis alertas verdes e a máquina passando fome. Os monitores medem
**congestionamento**; isto é **inanição**, e são grandezas opostas.

**A regra, que é o que vale guardar:** para todo conjunto de alertas, perguntar
**qual falha faria todos eles ficarem verdes**. Se existir uma, é exatamente a
que falta monitorar — e ela é sempre a mais perigosa do conjunto, porque o
painel não fica em silêncio: fica *otimista*. Alerta de estoque parado e alerta
de estoque zerado são itens diferentes; ter os seis primeiros não dá nenhuma
cobertura do sétimo.

**E a ironia útil:** a capacidade que resolve isto é a **mesma** que a peça 2
do F-06 tinha acabado de rejeitar por motivo correto. "Contar contatos por
filtro" era a unidade errada lá (o outro lado da razão era cumulativo); aqui é
a unidade exata, porque a pergunta *é* uma contagem de contatos ("quantos
nasceram hoje"). Registrado para a próxima rodada não descartar a ferramenta
pelo veredito antigo: **capacidade rejeitada para um uso não está rejeitada
para todos** — o que se descarta é o par ferramenta+pergunta, nunca a
ferramenta.

**O que não sei fazer nativo, dito em vez de inventado:** alerta automático de
**ausência** de entrada. Workflow do GHL vê um contato por vez e não há gatilho
"nenhum contato criado em 24h" — não existe contato para enrolar. Sobram o
widget/lista (depende de alguém olhar) ou um contato sentinela com `Wait 24h`
em laço comparando um checkpoint que todo lead novo atualiza. A segunda é
engenhoca com custo (um contato de serviço, um campo) e não foi especificada:
é escolha do dono, não de rodada automática.

**Efeito colateral — uma alegação do roadmap venceu:** o G-03 dizia 47 leads
parados "crescendo todo dia". Estático em 47 há mais de 22 horas. O item não
fica menos importante (47 leads pagos sem cadência continuam sendo isso), mas
o argumento muda de **crescimento** para **envelhecimento**: lead de Lead Ads
esfria por hora, e o mais velho do estoque já tem três dias. Corrigido no
roadmap e no briefing. Terceira vez hoje que uma frase de urgência escrita num
dia parou de ser verdade no seguinte, sem ninguém revisar — mesmo padrão da
entrada "pendência que virou feito".

## O CRM não pode responder a pergunta do LC Phone, e agora isso está provado: **zero registro de chamada** na subconta, e o markup de 20% é da agência, não desta subconta — 22/09/2026, sessão automática

A rodada anterior fez a coisa certa (perguntar ao CRM, não aos documentos) e
tratou o achado com o cuidado certo (evidência, não confirmação; nenhum item
fechou, nenhum `[x]`). Duas correções na leitura, e as duas apertam a
conclusão em vez de afrouxá-la.

**1. `markup: 20` não é "alguém configurou um número nesta subconta".** A
mecânica do rebilling, conferida por busca: o markup é definido em
**Agency Settings → SaaS Configurator** como valor **global**, com
*override* opcional por subconta. Então `twilioRebilling = { enabled: true,
markup: 20 }` lido nesta subconta é compatível com — e mais provavelmente é
— o **global da agência herdado aqui**, exatamente igual em toda subconta do
plano, incluindo as que nunca fizeram uma ligação. O argumento da rodada
anterior ("não é o default de fábrica, logo alguém configurou") confunde
*não-default* com *configurado para esta subconta*: um valor global não é
default de fábrica e também não diz nada sobre esta subconta. (O único
default de fábrica que a busca mostrou é 1.05x/5%, e é para cobrir taxa de
Stripe — outra coisa.)

**2. A evidência direta existia e ninguém tinha olhado: não há registro de
chamada nenhum.** `conversations_search-conversation` nas **50** conversas da
subconta: 41 são atividade de CRM (`TYPE_NO_SHOW`/atividade, grupo `100`) e
9 são DM de Instagram (grupo `18`). **Nenhuma chamada.** Conferido no nível
da mensagem, não só do agrupamento: a conversa de `ZZ TESTE ESTRUTURA` — o
contato com 14 tags e todo o histórico de teste — tem **exatamente uma**
mensagem, `type: 28`, `messageType: TYPE_ACTIVITY_OPPORTUNITY`, corpo
"Opportunity created", `source: app`. Nada de `TYPE_CALL`, nada de
`TYPE_VOICEMAIL`, em lugar nenhum.

**O que isso revela sobre um número que o projeto já citava com confiança:**
`Tentativas telefone` = 24 e `Conexões telefone` = 8 no contato de teste
**não são 24 ligações**. São 24 escritas de campo, disparadas por
classificação manual de `Resultado da tentativa`. O Pós-ligação rodou 24
vezes; o telefone nunca tocou. Está tudo certo como teste de workflow — e é
zero evidência sobre telefonia.

**Conclusão, que é a parte útil:** a pergunta "LC Phone ou linha própria do
SDR?" **não tem resposta possível dentro deste CRM**, porque a resposta
estaria nos registros de chamada e não existe nenhum. A ausência é
compatível com os dois lados (pode não haver número provisionado, ou haver
um que nunca foi usado), então não desempata — mas elimina o CRM como fonte.
**Regra: não gaste outra rodada procurando isto por API.** É pergunta para o
dono, e ponto. Se alguém quiser uma última tentativa, o único lugar que
resolveria é a tela **Configurações → Números de Telefone**, que este
conector não expõe.

**E o achado que vale mais que a pergunta original — o canal de telefone
inteiro nunca foi exercitado uma vez.** Oito dos doze toques da régua, o
F-06 (medição de duração), o F-08 (reputação de número) e o F-09 (freio de
canal) tratam de um canal com **zero** execução real nesta subconta. Duas
consequências concretas:

- O checklist de teste da seção 10 testa o telefone **classificando
  `Resultado da tentativa`** — que exercita o Pós-ligação e mais nada. Para
  todo item que dependa do *evento de chamada* isso não serve, e o caso
  extremo é o F-06: `Transcript Generated` só dispara com chamada **discada
  e gravada**. Não existe jeito de testá-lo mexendo em campo. O item precisa
  de uma ligação real, que precisa de número provisionado, que é justamente
  a pergunta travada — **dependência que nenhum documento declarava.**
- Toda a régua de telefone (o motor da operação) está na mesma situação em
  que o G-05 pegou o WhatsApp: especificada, nunca executada, e por isso sem
  rastro para uma auditoria de dados achar. A diferença é que no WhatsApp a
  regra externa (janela de 24h) foi lida antes do primeiro envio; aqui a
  regra externa (bloqueio de operadora, F-08) também já foi lida antes da
  primeira ligação. Os dois canais estão, hoje, protegidos no papel e
  virgens na prática.

**Regra generalizável, a terceira desta classe neste arquivo:** antes de
tirar conclusão de uma **configuração**, pergunte se ela é *desta* entidade
ou herdada de um nível acima — configuração global se parece com decisão
local quando se lê uma subconta por vez. E antes de aceitar um contador como
prova de atividade, pergunte **quem escreve** aquele contador: `Tentativas
telefone` é escrito por classificação humana, não por evento de telefonia, e
por isso 24 nele não é 24 de nada no mundo real.

## A pendência que bloqueia F-06/F-08/F-09 ganhou evidência indireta, não confirmação — `twilioRebilling` ligado é sinal de LC Phone, mas não prova quem discou — 22/09/2026, sessão automática

> **Leia a entrada acima antes de usar isto.** O raciocínio e a cautela desta
> entrada estão certos, mas o `markup: 20` é **global da agência** (herdado por
> toda subconta), não sinal de configuração desta — e a evidência direta que
> faltava foi lida na conferência: **zero registro de chamada** nas 50
> conversas. O CRM não pode responder a esta pergunta.

Com G-03/G-04/F-09 aguardando o dono e R-14 aguardando volume real de
mensagem, nenhum item numerado do roadmap tinha trabalho de API executável
nesta rodada (`ROADMAP-SALES-ENGAGEMENT.md`, "Ordem sugerida", conferido de
novo — reler o "por quê estamos esperando" de todo item represado é a
própria instrução do documento antes de procurar lacuna nova). A pendência
mais repetida do projeto — "a operação liga por **LC Phone** (telefonia
nativa do GHL) ou por linha própria do SDR?" — aparece sem resposta em
três lugares (`build-wesales.md`, seção 2.26/F-08, "Conferência do F-06" e
`ROADMAP-SALES-ENGAGEMENT.md`/F-09) e trava as três ao mesmo tempo: sem
saber, não dá para confirmar `[x]` nos campos do F-06 nem escolher a opção
do F-09.

**Tentativa 1 — reler os documentos do projeto atrás de uma resposta já
dada em outro lugar.** `grep -rn` por `LC Phone`, `Twilio`, `discador` em
todo `wesales/`: todas as ocorrências já eram desta mesma pendência sendo
citada três vezes, nenhuma nova informação — confirma que não é uma
resposta esquecida, é uma pergunta genuinamente sem dado no projeto.

**Tentativa 2 — perguntar ao próprio CRM, não a um documento.** O conector
não expõe endpoint de números de telefone/discador, mas
`locations_get-location` devolve a configuração completa da subconta —
nunca lida por inteiro antes, as rodadas anteriores só liam
`get-custom-fields`/`get-pipelines`/`search-opportunity`. Achado:
`settings.saasSettings.twilioRebilling` = `{ "enabled": true, "markup": 20 }`.

**Tentativa 3 — confirmar o que esse campo significa de verdade, por
pesquisa, antes de tratar como resposta.** Duas buscas com termos
diferentes convergem: "Twilio Rebilling" é a função de SaaS Mode que
aplica uma margem (aqui, 20%) sobre o custo que a **HighLevel paga à
Twilio** por uso do **Phone System nativo (LC Phone)** e repassa esse
custo marcado para a carteira do cliente — é uma configuração de billing
que só faz sentido existir **para** uso de telefonia via Twilio/LC Phone;
GHL não rebill a por chamada feita pelo celular pessoal do SDR, porque
nada dessa chamada passa pelo Twilio da agência. `enabled: true` +
`markup: 20` (não o default de fábrica, alguém configurou um número)
é sinal de que a agência **provisionou e está monetizando** telefonia
nativa nesta subconta — evidência a favor de LC Phone, não prova de uso.

**Terceira checagem, não uma quarta tentativa — corroboração do mesmo
achado:** `conversations_search-conversation` filtrado por
`query_lastMessageType = TYPE_CALL` devolve **zero** conversas. Não ajuda a
distinguir LC Phone de linha própria (não houve nenhuma ligação ainda,
`Cadência 12x30` segue em rascunho, mesmo fato que já bloqueia R-14) — mas
é consistente com o achado acima, não o contradiz.

**Por que isto não fecha F-06/F-08/F-09 sozinho, e não vira `[x]` em
`APROVADO.md`:** `twilioRebilling` é uma configuração de **billing da
agência**, que pode valer para todas as subcontas de uma vez e não muda
sozinha se o SDR liga por LC Phone ou pelo celular em algum dia específico
— é indício de que a infraestrutura de LC Phone está provisionada e paga
para esta subconta, não prova de que as 100 ligações/dia do SDR saem por
ela em vez do celular pessoal. A regra 2 do `briefing-sdr.md`
(confirmar antes de agir) vale aqui: decisão de negócio (F-09, limiar do
freio de telefone) e desenho que muda comportamento (F-06, gravar toda
ligação) continuam esperando confirmação **do dono**, agora com uma
pergunta mais fácil de responder — "vocês configuraram rebilling de
Twilio de propósito, ou veio ligado?" — em vez da pergunta em aberto de
sempre.

**Atualizado nos três lugares que citavam a pendência sem essa evidência:**
`build-wesales.md` (seção 2.26/F-08 e "Conferência do F-06") e
`ROADMAP-SALES-ENGAGEMENT.md` (F-09) — nenhum dos três teve a pendência
declarada resolvida, só passou a linkar para esta entrada em vez de
repetir "nenhum documento confirma".

## Dois contadores cumulativos ainda podem ser populações diferentes — a razão fica enviesada para um lado, e o número não parece errado — F-06 peça 2, 22/09/2026, sessão automática

A peça 2 do F-06 acertou a pergunta difícil: widget de Custom Metrics só soma
`NUMERICAL`/`MONETARY`, então `Conexão real` (`SINGLE_OPTIONS`) não serve de
numerador, e contar contatos no estado atual misturaria unidade com
`Tentativas telefone`, que é soma cumulativa. Daí nasceu `Conexões reais
telefone` (C-31), cumulativo dos dois lados. Raciocínio correto, e a
armadilha de unidade é justamente a que este arquivo já ensinava a evitar.

Falta a pergunta seguinte, que não é de unidade e sim de **população**:

| Lado | Conta |
|---|---|
| `Conexões reais telefone` (C-31) | chamada **de LC Phone** que **gerou transcrição** e passou de 60s |
| `Tentativas telefone` (C-09) | **toda** tentativa de telefone que o SDR classificou |

Os dois somam. Os dois são cumulativos. E a razão entre eles não é uma taxa,
é a comparação de dois conjuntos diferentes. Três caminhos levam ao mesmo
desvio, e nenhum é bug: ligação pelo celular do SDR (entra no denominador,
nunca no numerador), período com transcrição desligada (idem, e para sempre,
porque contador acumulado não volta atrás) e ring que não gera transcrição
nenhuma (idem).

**O que torna esta classe pior que ruído:** o viés é **sistemático e numa
direção só** — sempre para baixo — num widget que vai se chamar "Taxa de
Conexão Real". Número baixo lido como "o SDR não está conversando com
ninguém", quando a causa pode ser inteiramente "metade das ligações não é
medida". É a métrica que o item existia para consertar (`Atendeu` inflado
pelo julgamento do SDR) substituída por outra enganosa no sentido oposto. E é
a mais difícil de achar depois: não dá erro, não fica vazia, não quebra
nenhum portão. Só mente, com cara de número.

**A regra:** antes de dividir dois campos, perguntar **de quem** é cada lado,
não só qual a unidade. Três perguntas, todas de uma linha:

1. Quem **escreve** cada lado? (aqui: workflow de transcrição vs. Pós-ligação
   — donos diferentes já é sinal)
2. Existe evento que incrementa **um** e não o outro? Se sim, a razão tem
   viés, e a direção é previsível.
3. O lado de baixo é **superconjunto** do de cima por construção, ou só por
   coincidência do desenho atual?

Se a resposta da 2 for sim, o denominador certo quase sempre já está no
caminho do numerador — basta somar onde a condição comum é conhecida. Aqui era
o nó 2, que roda para toda transcrição antes do teste dos 60s: um `Math` ali
(C-32, `Ligações com transcrição`) dá o denominador da mesma população, e a
taxa passa a ler "das chamadas que dá para medir, quantas foram conversa".

**E o brinde, que é o motivo de valer a pena e não só de estar correto:**
`C-32 ÷ C-09` passa a ser um **medidor de cobertura da instrumentação**. 95%
significa que a taxa de cima é confiável; 40% conta ao dono, sem abrir a tela
de telefonia, que a maior parte da operação está fora do LC Phone ou sem
transcrição. É o mesmo método de "contador vizinho" que este arquivo já
registra para achar nó silencioso (`Conexões telefone` = 8 com `Total de
conexões` vazio): duas somas que deveriam andar juntas, e a distância entre
elas é o diagnóstico. **Sem o campo do denominador, essa distância não
desaparece — ela fica invisível, diluída dentro da taxa, indistinguível de
desempenho ruim do SDR.** Generalizando: quando um viés de população existe,
medi-lo custa um contador e transforma o defeito em informação; não medi-lo
não o elimina, só o esconde no número que alguém vai usar para decidir.

## Custom Metrics soma `NUMERICAL`/`MONETARY`, não `SINGLE_OPTIONS` — e "contar contatos por filtro" não é a mesma unidade que "somar tentativas" — F-06 peça 2, 22/09/2026, sessão automática

A peça 1 do F-06 (entrada abaixo) tinha deixado como plano "apontar a
lista/dashboard de taxa de conexão para `Conexão real`" — um campo
`SINGLE_OPTIONS` (Sim/Não). Essa frase não sobreviveu à peça 2, no mesmo
dia: dava para a **lista** (Smart List filtra/mostra qualquer tipo de
campo), mas não para o **widget de Dashboard** (Custom Metrics). O achado
da seção 2.17 do `build-wesales.md`, registrado antes do F-06 existir, já
dizia isso ("Custom Metrics soma campo numérico, não só conta tag") — a
peça 1 não cruzou os dois achados antes de propor o plano.

Pesquisado nesta rodada se um recurso mais novo resolveria sem campo novo:
o changelog do HighLevel (`ideas.gohighlevel.com/changelog/custom-metrics-
now-with-filters-meta-ads-google-analytics-support`) mostra que Custom
Metrics ganhou **filtro por metric-level** (tag, pipeline, owner, agente de
chamada — múltiplas condições AND por métrica), mais recente que o achado
original da seção 2.17. Não achei confirmação de que esse filtro cobre
igualdade sobre campo personalizado arbitrário (só tag/pipeline/owner nos
exemplos documentados) — mas mesmo que cobrisse, não resolveria o F-06:
"contagem de contatos com `Conexão real = Sim`" mede quantos contatos estão
**agora** nesse estado (snapshot), enquanto `Tentativas telefone` (o outro
lado da razão) é uma **soma cumulativa** de tentativas ao longo do tempo —
dividir um pelo outro mistura unidade, mesmo que a plataforma deixasse
fazer a conta. A saída que funciona é sempre a mesma, e já estava no
próprio projeto desde o R-01: um contador `NUMERICAL` que só incrementa
(`Math +1`), nunca é lido como estado — mesmo padrão de `Conexões
telefone`/`Conexões WhatsApp`/`Total de conexões` (C-06/C-07/C-11/C-12).
Regra para a próxima vez que aparecer "queremos a taxa de X" com X sendo
`SINGLE_OPTIONS`/booleano: a pergunta certa não é "dá para filtrar por X",
é "o outro lado da razão já é uma soma cumulativa? se sim, X também
precisa ser".

## "A plataforma ainda não oferece isso" fechou a pergunta errada — a busca não tinha ido fundo o bastante, não o recurso não existia — F-06, 22/09/2026, sessão automática

A rodada de 21/09/2026 (a mesma que fechou o R-18) tinha lido o F-06
("qualidade da conexão, não a contagem") como bloqueado: "premissa técnica
(call duration nativo para o F-06) confirmou que a plataforma ainda não
oferece isso, sem destravar nada" — uma frase, sem entrada própria neste
arquivo, sem lista de fontes, sem segunda busca com termos diferentes. É
exatamente o padrão que a entrada "Premissa negativa..." (abaixo) já tinha
nomeado para o F-08, na mesma semana: **uma afirmação negativa
("não existe X") pedia busca própria pelo nome certo, e não teve.**

Três buscas desta rodada, com termos diferentes (`"LC Phone" call duration
custom field`, `"Call Status Workflow Trigger" duration`, `"Transcript
Generated" ... minimum call duration`), convergem numa resposta que aquela
pergunta rasa não achou: o GHL tem um gatilho de workflow chamado
**`Transcript Generated`** — dispara quando a transcrição de uma chamada
fica pronta e carrega **duração, direção, localização do autor da chamada e
horário** como dado do próprio evento. Funciona para chamadas de **Voice
AI, IVR e LC Phone** (a telefonia nativa do GHL, back-end Twilio) — não é
recurso de call tracking de terceiro, é nativo da mesma plataforma que o
F-06 original já citava como "call tracking" sem saber o nome. Pré-requisito
citado pela fonte: para chamadas LC Phone, **transcrição precisa estar
ligada em Configurações → Telefone** (em Voice AI já vem ligada por
padrão) — ação de tela, não de API.

**O que impede fechar o item por inteiro agora, e por que não é o mesmo tipo
de bloqueio:** o F-08 (seção 2.26 do `build-wesales.md`) já tinha registrado,
sem resposta, se as 100 ligações/dia da operação saem por **LC Phone** ou
por **linha própria do SDR**. O `Transcript Generated` só cobre LC Phone (e
Voice AI/IVR, que este projeto não usa) — se a resposta for "linha própria",
o gatilho nunca dispara e o F-06 volta à estaca zero. Diferente do bloqueio
antigo ("a plataforma não oferece"), que era permanente e não tinha saída, este
é uma pergunta com dono — uma resposta do dono resolve F-06, F-08 e F-09 ao
mesmo tempo, porque os três citam a mesma lacuna.

**Contradição não resolvida, registrada em vez de escondida:** uma busca
citou "Call Direction & Call Duration são filtros opcionais" do próprio
gatilho `Transcript Generated`; outra busca, sobre um gatilho diferente
(`Call Status`), afirma que filtro nativo de duração **ainda não existe** na
plataforma (há pedidos abertos em `ideas.gohighlevel.com` pedindo
exatamente isso). Não achei fonte que resolvesse a contradição para o
`Transcript Generated` especificamente — por isso o desenho em
`build-wesales.md` (seção 2.27) **não depende** de o gatilho filtrar por
duração: lê a duração como dado do evento e decide num `If/Else` comum,
caminho que funciona com ou sem o filtro nativo.

**Regra prática, reforçando a já escrita para o F-08 com um segundo caso
concreto:** uma frase de fechamento de item que diz "a plataforma não
oferece X" sem uma entrada própria neste arquivo (fontes, termos de busca,
nível de confiança) é sinal de busca rasa, não de resposta definitiva — vale
reabrir com termos diferentes antes de aceitar como permanente, mesmo que a
rodada anterior já tenha "confirmado". A diferença entre "não achei" e "não
existe" continua custando a mesma frase para escrever e levando a decisões
diferentes.

Zero escrita no CRM. Subconta reconfirmada via
`opportunities_search-opportunity`/`locations_get-custom-fields`/
`opportunities_get-pipelines`/`conversations_search-conversation`: mesmas 5
etapas do `FUNIL DE VENDAS`, 51 campos (sem mudança), 50 oportunidades (47
`NOVO LEAD` + 3 `NEGOCIAR`, 1 `lost` de teste), zero conversa de
WhatsApp/SMS real — G-03/G-04 seguem aguardando o dono.

## Um pré-requisito de configuração escondia uma decisão de operação: transcrição de chamada é gravação de chamada — F-06, 22/09/2026, sessão automática

A rodada anterior destravou o F-06 achando o gatilho `Transcript Generated`
(existe, carrega duração, cobre LC Phone — confere) e registrou o
pré-requisito como um item de tela: "transcrição precisa estar ligada em
Configurações → Telefone". Uma linha de checklist, do mesmo tamanho que
"habilitar Number Validation".

Não é do mesmo tamanho. **Transcrição exige gravação de chamada habilitada:**
sem gravação não há o que transcrever, sem transcrição o gatilho não dispara,
e o gatilho não tem outro caminho de entrada. A tradução honesta do
pré-requisito é uma frase sobre a operação, não sobre a tela:

> Para o F-06 funcionar, toda ligação de saída da operação passa a ser
> gravada.

E aí ele deixa de ser configuração e passa a ter três consequências que
nenhum documento do projeto tinha: **aviso de gravação por LGPD** (`grep -rn
"gravaç\|LGPD\|consentimento"` em todo o `wesales/` não achava **uma**
menção, e o `script-de-ligacao.md` abre direto na abordagem), **custo** (US$
0,024/minuto gravado, add-on pago, acima da gravação e do armazenamento) e
**um aviso que concorre com o gancho da abertura** — os primeiros segundos
são o ativo mais escasso de uma ligação fria, e é exatamente ali que o aviso
entra.

**A regra, que é sobre como ler um pré-requisito e não sobre telefonia:**
quando um item de checklist diz "habilite X", perguntar **o que X exige por
baixo** antes de aceitar o tamanho dele. Um pré-requisito que muda o
comportamento da operação com o lead (gravar, enviar, cobrar, registrar) não
é irmão de um que muda uma preferência da conta. O teste rápido: *este item
de configuração cria alguma obrigação perante o lead ou perante a lei?* Se
sim, ele é uma decisão do dono, não um passo de montagem — e vai para o
documento de quem decide, não só para o de quem clica.

**O segundo achado não veio de fonte nenhuma, veio de ler os nós.** Os nós 4
e 5 escrevem `Conexão real` = `Sim`/`Não` e **nada apaga o campo**. Junte com
o item acima: chamada que ninguém atendeu pode não gerar transcrição nenhuma,
então o workflow **não roda** e o campo fica com o valor da tentativa
anterior. Lead que conversou na T3 e morreu em T4-T8 segue lendo `Sim`. O
campo para de significar "esta tentativa foi conversa" e passa a significar
"alguma tentativa, algum dia, foi conversa" — outra métrica, e não a que o
item pede.

Quarta vez que esta mesma classe aparece neste projeto (o contador que não
zera, a tag que não sai, o portão que lê etapa sem `status`, agora o veredito
que não expira), e a primeira em que o gatilho **pode simplesmente não
rodar** — as três anteriores eram "rodou e não limpou". Vale registrar a
variação, porque muda onde se procura: **um campo escrito por um gatilho
condicional precisa de reset por um caminho que não dependa da mesma
condição.** Se a condição falhar, o valor velho não é sobrescrito por nada.

**E onde o reset vai, que é a parte não óbvia:** *não* no Pós-ligação. A
transcrição chega minutos depois da chamada; o SDR classifica na hora. Zerar
no Pós-ligação disputaria o campo com o nó que escreve aqui — "campo com dois
donos", já catalogado. O ponto sem ambiguidade é antes de a ligação existir:
o nó que cria a tarefa de cada tentativa. A ordem fica sempre tarefa criada
(limpa) → ligação → SDR classifica → transcrição escreve. **Regra
generalizável:** quando dois nós escrevem o mesmo campo com latências
diferentes, o reset pertence ao mais previsível dos dois momentos — e o mais
previsível quase nunca é o que reage ao evento.

## Uma solução de mercado (americana) e uma solução nacional (mas de outro setor) foram as duas primeiras respostas erradas para a mesma pergunta — F-08, 22/09/2026, sessão automática

> **Leia antes a entrada seguinte** ("Premissa negativa…", mesma data): a
> terceira resposta desta entrada — "não existe SHAKEN/STIR para número
> brasileiro, então o equivalente é o portal *Qual Empresa Me Ligou?*" —
> também estava errada. Existe: é a `Origem Verificada`. O resto desta
> entrada continua valendo.

Fechando o F-08 (proteção de reputação do número de **telefone**, o par do
F-07 que protege WhatsApp), a pesquisa foi direto para a resposta "óbvia"
duas vezes seguidas e as duas estavam erradas para esta subconta —
registrado aqui para a próxima rodada não repetir nenhuma das duas:

1. **Voice Integrity** (HighLevel) é o recurso nativo que resolveria
   exatamente este problema — registra o número junto a First Orion/Hiya/
   TNS para tirar o rótulo "Spam Likely". A documentação de suporte da
   própria HighLevel e cobertura de terceiros dizem, sem ambiguidade,
   "**Labs, US only**" e exigem registro SHAKEN/STIR com EIN — framework da
   FCC americana. Número brasileiro não tem EIN, não se qualifica. Copiar a
   receita americana sem ler a letra miúda teria produzido uma
   especificação que nunca funcionaria aqui.
2. **"Não Me Perturbe" da Anatel** parecia o equivalente nacional óbvio —
   é uma plataforma real, brasileira, de opt-out contra telemarketing. Mas
   a obrigatoriedade de adesão (inclusive a ampliação de 2025-2026) alcança
   **só prestadoras de serviços de telecomunicações**, cerca de 32% das
   ligações indesejadas do país; os outros dois terços — que incluem uma
   agência de marketing vendendo serviço, o caso desta subconta — ficam
   fora do alcance daquela plataforma especificamente. Múltiplas fontes
   independentes convergiram no mesmo número (32%) e na mesma frase
   ("exclusivamente das prestadoras de telecomunicações"), sinal de que
   estão citando o mesmo dado de origem, não inventando cada uma o seu.

**O risco real não estava em nenhuma das duas respostas óbvias — estava
numa regra menos badalada, de agosto/2026:** toda operadora brasileira
agora é obrigada a oferecer bloqueio de chamada "abusiva" grátis e
**ativado por padrão** para todo cliente, com critério declarado de
**quantidade e duração de chamadas** — sem exigir cadastro prévio do lead
em nada. É o equivalente funcional do "Spam Likely" americano, só que sem
o Voice Integrity para remediar, porque aquele recurso não se aplica aqui.
A meta desta operação (100 ligações/dia) já bate ou passa a referência
internacional de segurança (50-75/dia por número) — o mesmo tipo de
"estrago silencioso" que motivou o F-05 e o F-07, aqui na camada de
infraestrutura de voz.

**Regra prática, generalizável:** quando uma pesquisa de mitigação para
risco de plataforma encontra rápido uma resposta que "parece certa" — um
recurso nativo com o nome exato do problema, ou uma lei nacional com o
nome exato do problema — vale <b>ler o escopo até o fim</b> antes de
especificar em cima dela. As duas respostas rápidas deste item tinham nome
perfeito e escopo errado (país errado numa, setor errado na outra); a
resposta certa estava numa notícia sem nome chamativo, achada só ao
continuar procurando depois das duas primeiras não fecharem.

Zero campo, zero tag, zero workflow, zero escrita no CRM — item de
documentação e rotina manual pura, mesmo tratamento do F-07. Detalhe
completo em `build-wesales.md`, seção 2.26, e `ROADMAP-SALES-ENGAGEMENT.md`,
F-08. Subconta reconfirmada sem mudança (51 campos, 50 oportunidades,
G-03/G-04 ainda aguardando o dono).

## Premissa negativa ("isso não existe no Brasil") é a mais barata de conferir e a mais cara de errar — correção do F-08, 22/09/2026, sessão automática

O F-08 descartou o `Voice Integrity` do HighLevel pelo motivo certo (é `US
only`, exige SHAKEN/STIR com EIN americano) mas embutiu uma generalização
que ninguém testou: **"SHAKEN/STIR não existe para número brasileiro"**.
Existe. Chama-se **`Origem Verificada`**, é a implementação brasileira de
STIR/SHAKEN + RCD, gerida pela ABR Telecom pelo Portal AIA, com 52+
prestadoras e ~6 bilhões de chamadas autenticadas por mês em agosto/2026 —
cerca de 30% do tráfego nacional. Não é piloto: é infraestrutura em
produção, com prazo legal (obrigatória acima de 500 mil chamadas/mês hoje,
geral em ~outubro/2028).

**O dano de uma premissa negativa não é a linha errada, é a recomendação que
ela troca.** Com "não existe equivalente", o item recomendou como
"equivalente brasileiro real do Branded Caller ID" o portal **"Qual Empresa
Me Ligou?"** — que só funciona se o lead **procurar** o número antes de
decidir atender. A `Origem Verificada` mostra nome, logo e motivo **na tela
da chamada**, antes da decisão. O plano B foi promovido a plano A porque o
plano A tinha sido declarado inexistente. A recomendação errada sobreviveria
à revisão: ela é verdadeira em si (o portal existe e é gratuito), só não é o
melhor caminho.

**Por que esta classe engana com tanta facilidade:** afirmação positiva
("existe X") é conferida achando X. Afirmação negativa ("não existe
equivalente brasileiro") exige procurar pelo **nome local**, que por
definição não está na fonte em inglês que originou a dúvida. Buscar
`"SHAKEN/STIR Brazil"` a partir da documentação da HighLevel tende a
devolver mais documentação americana; o que achou foi buscar pelo nome
brasileiro (`Origem Verificada`), e esse nome só aparece quando se busca o
**problema** em português, não o **produto** em inglês. Foi assim que veio
junto o `0303` — item que o F-08 nem mencionou e que é a primeira coisa que
qualquer operação de ligação ativa no Brasil precisa saber (facultativo
desde agosto/2025, com o MPF pedindo que volte).

**Regra:** toda frase da forma "não existe X para o Brasil / para este
canal / nesta plataforma" precisa de uma busca própria **no idioma e na
nomenclatura locais** antes de virar premissa de recomendação. Uma busca. E
se a busca não achar, escrever "não encontrei" em vez de "não existe" — as
duas frases custam o mesmo para escrever e levam a decisões diferentes.

**O segundo achado veio de ler o critério inteiro, não o resumo.** O F-08
citou a norma (Despacho Decisório nº 82/2026/RCTS/SRC, 17/08/2026) pelo par
"quantidade e duração". A lista completa que a norma autoriza a prestadora a
considerar é: **CNAE de quem origina, volume, proporção de chamadas de
curtíssima duração, duração média e taxa de completamento**. Os três últimos
mudam a natureza do item: a norma não mede só *quantas* ligações saem, mede
**como elas terminam** — e "como terminam" é decisão de régua, não de
infraestrutura. Com o resumo, a mitigação era externa (cadastrar número,
dividir volume). Com a lista inteira, a mitigação mais barata estava dentro
da própria especificação.

**E aí apareceu o achado que fechou o item, por comparação entre canais:** o
seletor de canal já protege o WhatsApp (`WA não atendidas seguidas < 2` —
duas sem resposta e o lead sai do canal) e **não existe nada equivalente no
telefone**, que carrega 8 dos 12 toques. `grep` em todo o `wesales/`
confirma: é o único contador de "seguidas" do projeto. O canal com o dobro
dos toques, o único com regulador olhando e o único sem freio. Virou **F-09**
no roadmap, com três limiares para o dono escolher — não executei, porque o
limiar **é** a régua e mexeria na meta de 100 ligações/dia.

**Regra, generalizável para além deste caso:** quando um item protege um
canal, perguntar o que o **outro** canal tem que ele não tem — e o
contrário. A assimetria entre dois canais do mesmo projeto é mais fácil de
achar (um `grep` pelo nome do contador) do que a ausência absoluta, e foi o
que três rodadas de "proteção de reputação" não tinham perguntado. Mesmo
padrão do achado do F-07 (cada item protegia lead ou mensagem, nenhum
protegia o canal): a pergunta produtiva é *o que ninguém está protegendo*,
aplicada uma vez por canal, não uma vez por projeto.

**Limite de fonte, registrado como sempre:** `gov.br` e `teletime.com.br`
foram testados nesta rodada e voltaram `EGRESS_BLOCKED` do proxy — mesma
limitação já registrada para `help.gohighlevel.com`. Tudo acima veio de
convergência entre fontes independentes (número do despacho, lista de
critérios, limiar de 500 mil/mês, prazo de 2028, 5 dias úteis da ABR
Telecom, datas do `0303`), que é o teste que este projeto usa quando a fonte
primária não abre. Confiança média-alta, e escrito como tal no documento.

## O dono fez a parte manual e três documentos continuaram pedindo — pendência que virou feito é tão errada quanto achado que não foi aplicado — 22/09/2026, sessão automática

Os 5 campos criados na tela em 21/09 23:15–23:33 foram registrados na rodada
seguinte **só aqui** (onde renderam o achado do travessão no `fieldKey`).
Quem executa não lê este arquivo — lê os que dizem o que fazer. Varredura de
22/09, um dia depois:

| Documento | O que ainda dizia | Consequência para quem abre a tela |
|---|---|---|
| `IMPLEMENTACAO-WORKFLOWS.md` | bloco "**Criar agora** (bloqueiam workflows da Parte 2)" com os 5 campos; "o campo `Toques na semana` **não existe** na tela"; "**só depois de criar `Hora da conexão`**"; "`Hora do retorno`, **quando existir**" | criar os 5 de novo → **duplicado**, exatamente o que a regra 3 do briefing manda evitar; e a Parte 2 parecendo bloqueada quando já não está |
| `campos-e-tags.md` | "Ainda em aberto: 1. `Hora do retorno` — falta criar na tela" | idem, no arquivo que é a autoridade de contagem de campos |
| `CONFERENCIA-CAMPOS.md` | Tabela A pedindo `Hora do retorno`, e **nenhum registro** dos 5 campos — no arquivo que existe só para reconciliar tela e especificação | o reconciliador dois dias atrasado no único avanço manual que houve |
| `briefing-sdr.md` | L-01 como "não existe campo de data/hora do retorno" | lacuna contada como aberta quando o que sobrou dela é outra coisa |

**A assimetria que faz esta classe passar:** a auditoria de merge field órfão
(entrada abaixo) compara documento contra tela e pega **chave que não
existe**. Não existe auditoria simétrica que pegue **pendência que deixou de
existir** — a frase "falta criar X" segue gramaticalmente perfeita para
sempre. O custo também é assimétrico: chave errada falha em silêncio dentro
de um workflow; pendência vencida faz uma pessoa gastar tempo e criar um
duplicado que a regra 1 do briefing depois **proíbe excluir**. O erro caro é
o que nenhum comando pegava.

**Regra:** toda vez que a leitura por API mostrar um campo, tag, opção ou
workflow **novo** na tela, o mesmo commit fecha a linha correspondente em
*todos* os documentos de execução — `IMPLEMENTACAO-WORKFLOWS.md`,
`campos-e-tags.md`, `CONFERENCIA-CAMPOS.md`, `GUIA-MONTAGEM.md`,
`briefing-sdr.md`. O comando que vale rodar depois de cada leva:

```
grep -rn "falta criar\|criar antes\|só depois de criar\|quando existir\|Criar agora\|não existe" wesales/*.md \
 | grep -F -f /tmp/nomes.txt | grep -v "^wesales/APRENDIZADOS-CRM.md"
```

`nomes.txt` = a coluna `name` dos campos lidos por API, um por linha. **O
filtro por nome de campo não é opcional:** sem ele o comando devolve 101
linhas neste repositório, quase todas legítimas (etapa que não existe mais,
workflow que ainda não existe) — ruído que faz a varredura ser abandonada na
primeira tentativa. Com o filtro, 10 linhas, e cada uma é uma afirmação sobre
a tela a confrontar com a leitura daquela rodada. Depois das correções de
22/09 as 10 são legítimas: nó de workflow que falta, opção de campo que falta
(`Desqualificado`, R-18), e um parágrafo datado com o ponteiro já anexado.
Uma décima primeira linha é o que se procura.

**E o oposto, que aconteceu no mesmo arquivo:** ao fechar uma pendência,
**não reescreva o parágrafo datado** que a registrava — os três "continua
aberto da Tabela A" de 19, 20 e 21/09 eram verdade nas suas datas.
Ganharam um ponteiro para a Tabela K e ficaram onde estão. Reescrever
apagaria a única prova de quanto tempo a pendência levou, que é o dado que
gerou esta entrada.

Sobrou desta varredura uma pergunta de tela, deliberadamente **não**
respondida por dedução: o seletor de vencimento do `Add Task` aceita hora
vinda de campo `TEXT`? Não sei, e chutar aqui seria repetir o erro do
`fieldKey` adivinhado. Está como conferência acoplada ao retoque no
`GUIA-MONTAGEM.md` — quem for editar o nó já está com a tela aberta, e o
caminho garantido (o horário no corpo da tarefa) foi especificado sem
depender da resposta.

## 403 "The token does not have access to this location" não quer dizer token sem acesso — quer dizer `locationId` não resolvido — 22/09/2026, sessão automática

A rodada abriu com a verificação de sempre (campos, etapas, oportunidades) e
as duas primeiras chamadas do conector `GHL CRM` voltaram assim:

| Chamada | Parâmetros | Resposta |
|---|---|---|
| `locations_get-custom-fields` | sem `locationId` | `403` — `The token does not have access to this location.` |
| `locations_get-location` | sem `locationId` | `403` — `Forbidden resource` |
| `opportunities_get-pipelines` | sem `locationId` | `422` — `locationId can't be undefined` |
| `opportunities_get-pipelines` | **com** `locationId: 1D53YTI9C7oIMBavcQxV` | `200` — pipeline e 5 etapas |
| `locations_get-custom-fields` | **com** `locationId` + `model: all` | `200` — os 51 campos |

Ou seja: **o token está intacto.** O que faltava era o `locationId`, que em
rodadas anteriores o conector resolvia sozinho e nesta não resolveu. A
terceira linha da tabela é a que denuncia: a mesma ausência de `locationId`
que produz um `422` explícito num endpoint de `opportunities` produz um
`403` com texto de permissão num endpoint de `locations`. A mensagem do
`403` descreve a consequência (o pedido chegou sem location, então nenhuma
location está autorizada) e não a causa.

**Por que isto era perigoso justamente agora:** a recomendação de **rotacionar
o PIT** está aberta desde que ele apareceu no histórico de chat de uma sessão
anterior — e um PIT rotacionado responde `403` também. Sem esta medição, o
primeiro `403` de uma rodada futura seria lido como "o dono rotacionou o
token, acesso perdido, rodada encerrada": diagnóstico plausível, errado, e
que custaria a rodada inteira. Pior no sentido inverso: um `403` de token
realmente revogado seria descartado como "é só o `locationId` de novo".

**Regra:** `403` do conector **nunca** é conclusão, é sintoma. Antes de
qualquer diagnóstico, repita a chamada com `locationId:
1D53YTI9C7oIMBavcQxV` explícito. Funciona → era resolução de location, siga
a rodada passando `locationId` em **todas** as chamadas. Continua `403` →
aí sim é token, e a rodada para com isso escrito.

Duas armadilhas de parâmetro medidas no mesmo minuto, que valem guardar:

- `locations_get-custom-fields` tem um parâmetro chamado **`model`** que
  **não é o modelo de LLM** — é o modelo de dado do campo (`contact`,
  `opportunity`, `all`, `business`, `task`). Mandar um nome de modelo de
  linguagem ali devolve `422` com a lista de valores válidos.
- `opportunities_get-pipelines` **rejeita** `model` como propriedade
  desconhecida (`property model should not exist`). Os dois erros são `422`
  e chegam juntos se as chamadas forem em paralelo — é fácil ler os dois
  como um problema só.

Conferência da rodada, já com `locationId` explícito: **51 campos** (nenhum
novo desde os 5 de 21/09 23:15–23:33), **5 etapas** no `FUNIL DE VENDAS`
(`NOVO LEAD` · `CONECTAR` · `AGENDAR` · `NEGOCIAR` · `FORMALIZAR`),
`Resultado da tentativa` ainda com as **6** opções originais — a opção
`Desqualificado` do R-18 continua só no papel, como os documentos dizem.
Zero escrita no CRM nesta rodada.

**Addendum à auditoria de merge field órfão** (entrada de 22/09 sobre o
travessão, mais abaixo): rodada de novo agora, ela acusa
`contact.checkpoint_data_de_retorno` — e é **falso positivo permanente**. As
duas únicas ocorrências (`APRENDIZADOS-CRM.md`, tabela daquela entrada;
`build-wesales.md` seção 2.24, nota que explica o erro) citam a chave errada
*de propósito*, para documentar o bug. Não corrija: "corrigir" ali apaga a
própria lição. A leitura certa do resultado da auditoria é
**seis** linhas esperadas, não quatro:

```
contact.                              ← artefato do grep (o ponto final de frase)
contact.checkpoint_data_de_retorno    ← citação deliberada do erro, não um uso
contact.company_name  contact.first_name  contact.name  contact.source   ← nativos do GHL
```

Qualquer sétima linha é um órfão de verdade.

## Nenhum item protegia a reputação do número, só a entrega de cada mensagem — F-07, 22/09/2026, sessão automática

Sessão sem novidade no CRM (agente de leitura dedicado confirmou: 51
campos, 50 oportunidades, zero conversa de WhatsApp/SMS real ainda — só
DMs de Instagram — G-03/G-04 seguem aguardando o dono) e sweep de
coerência de sempre limpo (nomes de etapa, merge field, e a lista manual
do Mestre de saída — seção 3 — reconferida contra a explicação do F-05
peça 4 de por que ali ela fica de propósito; nada para corrigir). Seguindo
a própria instrução deste documento e do roadmap ("pesquisar como Reev,
Meetime, Outreach e Salesloft resolvem antes de desenhar"), a pergunta que
ainda não tinha sido feita: **o que essas quatro ferramentas não cobrem,
porque não é o problema delas?** Nenhuma trata WhatsApp Business API como
canal principal — então nenhuma tem repertório para o risco mais
específico deste projeto: a **Quality Rating** que a Meta atribui a todo
número do WhatsApp Business API (Verde/Amarela/Vermelha, por
bloqueio/denúncia/engajamento dos últimos 30 dias) e o **Tier de
mensagens** que ela trava de subir — uma nota ruim pode throttlar ou
recusar envio mesmo dentro da janela de 24h e com Template aprovado
(`WebSearch`, confiança média-alta: mecânica confirmada por várias fontes
de terceiros e por um artigo do próprio HighLevel Support Portal citando a
mesma mecânica sem alteração dentro do GHL — domínio bloqueado pelo proxy
deste ambiente, lido só por citação de busca, mesma limitação de sempre).

**Por que nenhum item existente já cobria isto, mesmo depois de F-04, R-13
e G-05/G-06 — a distinção que quase fez este achado parecer duplicado:**
cada um protege uma coisa diferente, e nenhuma é "o número". F-04 (`Toques
na semana`) protege o **lead** de receber toque demais — um número com
reputação perfeita ainda cansa um lead se ninguém olhar o teto, e um
número pode respeitar o teto lead a lead e ainda cair de nota, porque a
Meta soma bloqueio de todos os leads, não de um só. R-13 (`telefone-
invalido`) valida se o número **do lead** existe, não a reação dele à
mensagem. G-05/G-06 garantem que cada mensagem individual **pode ser
entregue agora** (janela, Template) — nenhum dos dois pergunta se o canal
como um todo ainda está autorizado a entregar amanhã. **Regra prática,
generalizável:** antes de declarar uma família de risco coberta ("mensagem
protegida", "lead protegido"), pergunte que **nível** cada peça protege —
mensagem individual, lead individual, ou canal/infraestrutura inteira. Uma
operação pode ter as três primeiras camadas perfeitas e ainda cair porque
ninguém olhou a de infraestrutura, que geralmente é a única sem gatilho
nativo para automatizar (não existe leitura de Quality Rating por workflow
no GHL — pesquisado, não encontrado), e por isso a mais fácil de esquecer
num projeto pensado em automação.

**Registrado como checklist manual, não workflow, e por que isso é a
escolha certa aqui e não preguiça:** diferente de toda peça anterior deste
projeto que virou workflow por não ter automação nativa (esperar dono
montar na tela), aqui não existe **nenhum** gatilho, ação ou Custom Value
que leia a nota — não é "falta montar", é "não existe o que montar". A
saída correta registrada foi transformar em rotina do gestor com gatilho
por **evento** (antes de publicar os 4 nós de envio com volume real,
semanalmente com volume crescendo, depois de pico no Opt-out do R-17), não
por calendário fixo — detalhe completo em `build-wesales.md`, seção 2.25,
e `ROADMAP-SALES-ENGAGEMENT.md`, F-07. Zero campo, zero tag, zero
workflow, zero escrita no CRM.

## Uma guarda de janela na entrada protege a primeira mensagem de uma troca; cada mensagem seguinte precisa da sua própria — "sem resposta" não pode virar "pula para a próxima" — G-06 peça 2, 22/09/2026, sessão automática

O G-06 fechou a peça 1 (Caminho A, `Conversation AI`) com uma guarda de
janela só na **entrada** do workflow — correto ali, porque dali em diante
uma única ação (a IA) decide o que mandar e quando, e ela já assume que
está numa conversa em andamento. A peça 2 (Caminho B, 8 blocos manuais
`Send WhatsApp` → `Wait → Contact Replied` → próxima pergunta) quase herdou
o mesmo raciocínio — "já guardei a entrada, as 8 perguntas estão cobertas"
— e estaria errado: o desenho original de cada bloco, no timeout, "pulava
para a pergunta seguinte" mesmo sem resposta. Isso manda texto livre com a
janela fechada em qualquer pergunta a partir da 2ª, porque é a **resposta
do lead**, não o nosso envio, que reabre a janela de 24h — uma guarda na
entrada garante isso só para a primeira mensagem da corrente.

**A regra, generalizável para qualquer corrente de várias mensagens
guardada por janela de atendimento:** "guardei a entrada" não é "guardei a
corrente". Cada elo que pode enviar texto livre precisa da mesma pergunta
que a guarda de entrada já respondeu — "isto está dentro da janela agora,
ou preciso de uma saída seguindo o padrão Template/encerrar?" — e quando a
única coisa que reabre a janela é uma resposta real, "sem resposta" só tem
uma saída segura: **encerrar**, nunca "seguir mesmo assim". Multiplicar
Template por elo (aqui seriam 8) resolve o mesmo problema, mas custa uma
aprovação da Meta por mensagem da conversa — inviável quando o conteúdo é
pensado como pergunta-e-resposta, não como texto fixo recorrente (M1/M2/M3
já usam Template porque são disparos isolados, não uma troca).

Detalhe da correção: `build-wesales.md`, seção 6, "B — Sem Conversation
AI"; `IMPLEMENTACAO-WORKFLOWS.md`, W10; `ROADMAP-SALES-ENGAGEMENT.md`,
G-06. Zero campo, zero tag, zero escrita no CRM.

## Uma varredura de guarda por código catalogado deixa passar quem nunca foi catalogado — busque pelo nome da ação, não pela lista — 22/09/2026, sessão automática

O G-05 (guarda de janela de 24h do WhatsApp) fechou em duas peças (21 e
22/09/2026) conferindo, um por um, os códigos da tabela "Templates ativos"
de `biblioteca-mensagens.md`. Parecia completo — e não era: o workflow
`Qualificação por IA no WhatsApp` (`build-wesales.md`, seção 6) manda
`Send WhatsApp` desde 18/09/2026 e nunca entrou naquela tabela, porque o
R-04 que a criou fechou dois dias antes de o G-05 existir. Uma varredura
que confere "todo código da lista X tem propriedade Y" nunca vai achar o
que não está na lista X — só acha o que já foi catalogado errado, não o
que nunca foi catalogado. O jeito que achou isto (G-06,
`ROADMAP-SALES-ENGAGEMENT.md`): trocar a pergunta por uma que não passa
pela lista — `grep -n "Send WhatsApp" build-wesales.md` sobre o documento
inteiro, e conferir cada ocorrência contra a guarda, não contra a
biblioteca. **Regra para a próxima vez que uma guarda, contador ou
convenção nova precisar valer "em toda a operação":** primeiro grep pelo
nome literal da ação/nó no documento inteiro (aqui, `"Send WhatsApp"`), e
só depois cruze com qualquer tabela de rastreio — nunca o contrário. O
mesmo vale para `toque` (F-04) e para qualquer convenção futura do mesmo
formato.

**Reconferido na mesma rodada, sem novidade:** o toolkit HighLevel via
Composio (`briefing-sdr.md`, "Estado do acesso") segue **sem conta
conectada** — `mcp__Composio__COMPOSIO_MANAGE_CONNECTIONS`, toolkit
`gohighlevel`, ação `list`, retornou `"active_connections": 0,
"accounts": []` em duas chamadas seguidas (a mensagem "connections have
been initiated and are pending completion" que acompanha a resposta é
texto padrão da ferramenta, não um convite de OAuth novo disparado por
esta leitura — nenhum `redirect_url` veio junto, e a segunda chamada
devolveu exatamente o mesmo resultado da primeira). Mesma conclusão de
18/09/2026: campo e calendário por API continuam fora do alcance deste
conector até o dono autorizar a conexão Composio↔HighLevel (fluxo de
OAuth, fora do que esta rotina pode fazer sozinha).

## As cinco cópias v2 entraram no ar — e a troca derrubou três workflows antes de dar certo — 22/09/2026

Decisão tomada: trocar. Os cinco publicados defeituosos foram **desligados**
(status `draft`, nenhum nó alterado — a regra do dono foi respeitada) e as
cópias corrigidas ligadas no lugar. Reversível com um clique em cada.

| Agora no ar | O que corrige |
|---|---|
| `Interceptação de Sinal — Clique v2` | o original aponta para um Trigger Link inexistente: **nunca disparou** |
| `Interceptação de Sinal — Resposta v2` | portão de opt-out; sem ele "pare de mandar mensagem" virava tarefa "ligar agora" |
| `Pós-agendamento v2` | a régua de qualificação (0–100) que **nunca existiu** — provada somando 93 no contato de teste |
| `Mestre de saída v2` | não marca mais `limpar-tarefas` em lead que acabou de chegar |
| `Pós-ligação v2` | 4 nós de Math que escreviam em campo nenhum |

### O erro que quase custou caro: troca sem rollback

Na primeira tentativa desliguei os cinco originais e **três cópias falharam
ao publicar**. Resultado: `Interceptação — Resposta` e `Pós-agendamento`,
que estavam funcionando, ficaram **fora do ar**. Religados na mão em
seguida.

**Regra que fica: toda troca precisa de rollback no mesmo passo.** O script
agora religa o original automaticamente se a cópia não subir — e foi
exatamente isso que salvou o `Pós-agendamento` na segunda rodada.

### Dois defeitos do clonador, que só a publicação revela

1. **`transitions` não era remapeado.** Nó multi-path (`find_opportunity`)
   guarda em `attributes.transitions[].id` a referência aos nós do tipo
   `transition`. O clone trocava o id do nó e deixava a referência órfã:
   *"Transition node id X has no match"*. Era isso que derrubava os três.
2. **Nó alcançado só por `goto` não pode ter pai.** Ao inserir a régua no
   meio da cadeia, a nota final deixou de vir logo depois do nó anterior.
   Com `parentKey` apontando para o antecessor antigo a publicação recusa;
   apontando para o `goto` também (*"parentKey points to ... (Go To)"*).
   A forma aceita é **sem `parentKey` e sem `parent`**.

Nenhum dos dois aparece no salvamento do rascunho. Só na publicação.

## Revisão dos workflows que já existiam: três defeitos, um deles apagava a régua inteira — 22/09/2026

A pedido do dono, revisei os publicados que não foram montados nesta
sessão. Os três defeitos abaixo estavam vivos em produção.

### 1. `Pós-agendamento` nunca calculou a nota — e isso matava o Loop do closer

O workflow publicado **não tem nenhum nó de cálculo**. Tem só uma *nota de
texto* com o título `Nota de qualificação`, que o `GUIA-MONTAGEM.md` leu
como se fosse a régua. O campo numérico nunca foi escrito.

**A consequência não fica no Pós-agendamento:** os nós 5 e 6 do `Loop do
closer` comparam essa nota (`≥ 70` e `< 45`) para cobrar o closer quando a
régua e o veredito discordam. Com o campo sempre vazio, nenhuma das duas
comparações jamais bateu. A régua da seção 9.1 — o coração da
qualificação — **nunca existiu na prática**.

Corrigido em `Pós-agendamento v2` (rascunho): 28 somas condicionais,
máximo 100 pontos (30 Fit + 25 Mídia + 45 BANT), inseridas exatamente onde
a spec manda. Ressalva G-04 continua valendo: lead do Meta perde os 12
pontos de `Investimento mensal em anúncios`, porque o Meta grava ali
textos que não são opção do campo.

### 2. `Mestre de saída` marca `limpar-tarefas` em todo lead que CHEGA

O portão pergunta "etapa é `CONECTAR` e status é `open`?". Quando a
oportunidade **nasce** em `NOVO LEAD` a resposta é não, e ele cai no ramo de
limpeza. Era um efeito colateral conhecido e inofensivo — **deixou de ser
inofensivo agora**: a `Cadência 12x30` está publicada criando tarefas
`[CADENCIA]`, e `limpar-tarefas` é justamente a tag que autoriza a rotina
de higiene a fechá-las. Corrigido em `Mestre de saída v2` (rascunho) com um
portão que encerra quando a etapa é `NOVO LEAD`.

### 3. `Pós-ligação` tem quatro nós de Math apontando para campo nenhum

O `GUIA-MONTAGEM.md` registrava "falta o nó de `Total de conexões`". **O
diagnóstico estava errado** — esse nó existe. O defeito real é outro:
quatro `math_operation` com `updateField` **vazio** (ids `3d43bda9`,
`9ca6a104`, `7ba568ac`, `0759af13`), somando 1 ou 0 em lugar nenhum.

É por isso que `WA não atendidas seguidas` nunca é preenchido — e esse
campo é lido pelo nó 4 da `Cadência 12x30` para decidir se o toque sai por
WhatsApp. **Não corrigi de propósito:** adivinhar para qual campo cada um
deveria apontar corromperia contador em silêncio, que é pior que o campo
vazio. Precisa da decisão do dono.

### Lição que atravessa os três

Nenhum apareceu lendo a documentação — dois deles a documentação
descrevia **errado**. Todos apareceram lendo o **JSON real** do workflow
publicado. Para este projeto, a fonte de verdade é a subconta, não o
documento; e nó que existe com nome certo não quer dizer nó configurado.

## A simulação de uso real pegou o que a leitura de JSON não pegaria: espera por horário NÃO espera — 21/09/2026, PC do dono

Com 15 workflows publicados e a auditoria estrutural limpa, movi um lead de
teste para `CONECTAR`. **Em 90 segundos ele atravessou T1 e T2.** A régua de
30 dias teria disparado os 12 toques de uma vez.

### 1. O `Wait` por horário não espera — use duração

O validador do JS do builder é explícito: `specific_date` exige
**`specificDate`** e **`specificTimePeriod`**. Sem eles o GHL entende que
*a data já passou* e **segue direto**. Como eu montei os nós só com
`specificTimeHour`/`specificTimeMinute`, todo "esperar até 10:30" virou
"não esperar".

Também não adianta o `Wait` do tipo `time` **com janela de retomada**: com
a chave `window` o validador passa a exigir `Condition` e `Start`.

**Regra:** neste build, o único tipo de espera confiável é **duração**
(`time` + `startAfter`). Todas as cadências foram refeitas assim — os
intervalos são as diferenças entre os horários da tabela da spec e somam os
mesmos ~30 dias. Perde-se a hora exata do dia; ganha-se o espaçamento, que
é o que a régua realmente precisa.

**Corolário que vale para todo o projeto:** a **janela do workflow
(08:30–18:30) NÃO segura a execução fora do horário**. O nó 0 rodou às
22:37. A janela vale para envio, não para ação. Quem precisa de hora certa
tem de ser a tarefa, não o workflow.

### 2. Publiquei um workflow vazio sem perceber

Uma falha transitória deixou o Reengajamento com **0 nós**, e publicar não
reclamou. Publicado e vazio é pior que não publicado: parece pronto e não
faz nada. Agora `publicar()` recusa workflow sem nós, e `preencher()`
**aborta** se a API gravar um número de nós diferente do que foi enviado.

### 3. Reconstruir um workflow órfã os gatilhos criados à parte

Refazer um workflow troca os ids de todos os nós. O gatilho
`cad-outbound` da Cadência 12x30, que eu tinha criado numa chamada
separada, ficou apontando para um nó que não existia mais — a cadência
havia parado de disparar por tag, em silêncio. `preencher()` agora
reaponta **todos** os gatilhos do workflow, não só os que recebeu.

### O que a simulação confirmou funcionando

Nó 0 inteiro (dono atribuído, `Prioridade` 3, `Permissão WhatsApp`
`Não solicitado`, `Entrada em`, contadores zerados) e — o mais valioso —
a **integração entre módulos**: o `Contador de Toques` somou pela tag
`toque`, o `CONECTAR Estagnado` gravou o checkpoint ao ver `Tentativa nº`
= 0, e o `Pós-ligação` **publicado** reagiu ao `Resultado da tentativa`
somando `Total de ligações`. Os workflows novos e os antigos conversam.

### Auditoria estrutural: `wesales/tools/auditoria.py`

Cruza os 24 workflows e procura o que só aparece no conjunto: gatilho
órfão, `goto` morto, referência a workflow inexistente, publicado vazio ou
sem gatilho, configuração diferente da spec, e o mapa de quem dispara quem
por tag. Rodar depois de qualquer mudança — foi ele que pegou o defeito 3.

## Montagem programática funcionou: 9 workflows criados, testados e publicados pela API interna — 21/09/2026, PC do dono

O caminho que o R anterior classificou como "só com decisão explícita do
dono, e nunca deste ambiente" foi executado, no computador dele. **Funciona.**
Ferramentas em `wesales/tools/`, JSON e PNG de cada workflow em
`wesales/workflows-json/`.

**Como a sessão autentica (o README do `gohighlevel-cli` está certo, o
prompt estava errado):** *storage state* do Playwright **não** autentica a
API interna. O `backend.leadconnectorhq.com` exige o `Authorization: Bearer`
nativo do LeadConnector, e o jeito de obtê-lo é capturar do tráfego da
própria tela logada (`login-capture.js`). O token dura ~1 h e `renew.js`
recaptura sozinho, headless, em ~10 s, a partir do perfil persistente do
Chrome — só pede login humano se o perfil perder a sessão.

### As cinco armadilhas que custaram tempo (e a regra que fica de cada uma)

| Armadilha | O que acontece | Regra |
|---|---|---|
| **Salvar rascunho não valida** | O validador do `PUT` de rascunho aceita payload que o de **publicação** recusa. O nó de oportunidade passou horas "funcionando" em rascunho | **Critério de pronto é *publicou*, não *salvou*.** Todo teste de forma nova deve terminar em publicação |
| **Workflow sem `status`** | Um workflow criado mas nunca salvo com sucesso fica **sem** a chave `status`. Nesse estado o `PUT` recusa com a mensagem enganosa `"<nome do nó>" action has a corrupted type` — que aponta para o nó errado | Mandar `status: "draft"` **já no primeiro PUT**, e usar a **versão corrente** (não `1`) |
| **Todo `PUT` é substituição** | Publicar mandando só `name`/`status`/`workflowData` **zerou `allowMultiple`** (Allow Re-entry) em 7 workflows. Sem re-entry o contato não volta a entrar — a 2ª rodada do teste do W6 simplesmente não executou | Carregar `allowMultiple`, `stopOnResponse`, `timezone`, `window` e `allowMultipleOpportunity` do estado atual em **todo** PUT |
| **Gatilho órfão** | Uma tentativa que falha **depois** de criar o gatilho deixa um gatilho apontando para um nó que não existe mais. Dois gatilhos = risco de inscrição dupla ao publicar | `preencher()` **reaproveita** gatilho existente (PUT) em vez de criar outro |
| **Schema de terceiro não vale** | O `ghl-automation-builder` documenta `internal_update_opportunity`, `has_tag`, `is_empty`. Esta conta usa `create_opportunity`, `index-of-true`, `has_no_value` | Ler o formato de **workflow real desta subconta** (`dump_corpus.py`) e, quando não houver exemplo, varrer por força bruta contra um rascunho descartável |

### Formatos confirmados nesta subconta (fonte: workflows reais + força bruta)

- **If/Else é uma trinca de nós:** `condition-node` (com `branches[0].segments[0].conditions`) + `branch-yes` + `branch-no`. O nó de condição exige `operator`, `if`, `conditionName`, `version: 2` e `noneBranchName` — sem eles, erro 400.
- **`goto` (`{targetNodeId}`)** é o que faz dois ramos **convergirem** no mesmo nó e o que fecha **laços**. Um nó só pode existir uma vez na árvore: os demais caminhos saltam para ele.
- **Operadores:** `index-of-true` = "inclui", **`index-of-false` = "não inclui"**, `has_value` / `has_no_value`, `==`, `!=`, `>=`, `<`, `contain`. O `!=` **aceita merge field como valor** — a tela renderiza `If "Checkpoint — Tentativa nº" não é igual a "{{contact.tentativa_n}}"`.
- **Mudar status de oportunidade** não é um nó separado: é **`create_opportunity`** (nesta versão a ação é Criar/**Atualizar**, e com duplicata desligada ela atualiza a que já existe). Ela **exige etapa** — para não mover o lead, passe a etapa em que ele já está.
- **`remove_from_all_workflows`** exige `includeCurrent`; `false` é o "All Except Current" da spec.
- **Notificação interna** tem dois alvos: `userType: "user"` + `selectedUser` (o gestor) e `userType: "assign"` + `assignedOwners: ["contact_owner"]` (o dono do contato). Monitor de saúde deve usar o **gestor** — o lead que ele pega costuma estar sem dono.

### `{{right_now}}` — pendência da seção 0.3 RESOLVIDA

O token existe nesta conta. Duas provas: `{{right_now.date}}` já está **em
produção** no vencimento da tarefa do `Interceptação de Sinal — Clique`
publicado; e o W6 gravou `2026-09-21` no campo `Data do veredito do closer`
(DATE) usando exatamente esse token.

### Achado que a spec não registrava: o Trigger Link está morto

**Não existe nenhum Trigger Link na subconta** (`0 - 0 of 0` na tela de
Marketing → Links de acionamento), mas o workflow **publicado**
`Interceptação de Sinal — Clique` tem gatilho apontando para o link
`HUdfNRzzEAQJJBMFfeCy`. **Ele não tem como disparar.** A seção 0.5 diz que
`Agendar com o closer` "já existe" — não existe. Isso também trava os nós
M2.2/M3.2 da Cadência 12x30, que inserem esse link na mensagem.

### Quatro workflows que a spec dava como montados estavam vazios

`Cadência 12x30`, `Recuperação de No-show`, `Qualificação por IA no WhatsApp`
e `SLA do Closer — No-show` tinham **0 nós** (o último a spec dava como
inexistente). Nada a preservar — e preencher o rascunho existente, em vez de
criar outro com o mesmo nome, é o certo: nome duplicado quebraria os
`Add to Workflow` / `Remove from Workflow` que os citam.

### Campo personalizado sai na tela, não por API

`/locations/{loc}/customFields` recusa o bearer do app de workflows. Os 5
campos da tabela 1.2 foram criados na tela por Playwright. Armadilhas do
diálogo: os seletores são Naive UI — clica-se no **valor** visível, não no
rótulo, e o clique precisa de `force: true`; a lista de tipos é
**virtualizada**, então a opção de data (`Seletor de data`) só existe no DOM
depois de digitar para filtrar.

### Testes de ponta a ponta executados (contatos de teste, nunca lead real)

| Workflow | Disparo | Rastro conferido |
|---|---|---|
| `Contador de Toques` (W1) | tag `toque` em `ZZ TESTE ESTRUTURA` | tag removida sozinha e `Toques na semana` = 1 — exatamente o que a seção de teste da W1 previa |
| `Loop do closer v2` (W6) | `Reunião foi qualificada` = `Parcial` em `Teste Atendeu` | nota "Veredito do closer: Parcial · motivo: Sem fit · nota 80", oportunidade → `abandoned`, tag `nutricao-90d`, `Data do veredito` = hoje, **etapa intacta em NEGOCIAR** |
| `Loop do closer v2` (W6) | depois `= Não` (motivo `Sem fit`) | oportunidade → `lost`, etapa intacta. Só passou **depois** de corrigir o Allow Re-entry que a publicação havia zerado |

## Como a comunidade cria workflow sem clicar: API interna (`backend.leadconnectorhq.com`), extensão de JSON e "Copiar workflow" — 21/09/2026, ao vivo em chat

O dono pediu para pesquisar no GitHub e nas comunidades como outros resolveram
ou contornaram a falta de endpoint de escrita para workflows. Resultado da
pesquisa (fontes no fim), do mais oficial ao mais arriscado:

| Caminho | O que faz | Onde roda | Risco | Serve para nós? |
|---|---|---|---|---|
| **API pública v2** (`services.leadconnectorhq.com`) | `GET /workflows/` só lista nome, status e id. Sem POST/PUT. O pedido "REST API — Workflow POST/PUT Endpoint" está aberto no quadro de ideias da HighLevel, sem prazo. | — | nenhum | Não cria nada. É o que o conector `GHL CRM` já usa. |
| **Copiar workflow para outra subconta** (nativo, Agency Admin) | Copia um workflow com tags, campos e pipeline referenciados; chega como rascunho. | Tela da agência | nenhum | Só ajuda se já existir um workflow pronto em outra subconta da agência. Não temos. |
| **Snapshot** (nativo) | Empacota workflows + campos + tags + pipeline de uma subconta e importa em outra. A API de snapshots só lista e compartilha; não cria conteúdo. | Tela da agência | nenhum | Vale como **backup** de tudo que estiver montado, e para replicar em cliente futuro. Não monta do zero. |
| **Extensão Chrome "GHL Workflows JSON Exporter"** (FiftyDevs) e **"GHL Workflow Backup & Audit"** | Exporta o workflow aberto como JSON e importa um JSON para reconstruir o workflow em qualquer localização; a segunda declara funcionar em CRM white-label. | Navegador do dono, dentro da tela do builder | baixo (usa a sessão logada) | **Sim, é o atalho mais barato.** Monta-se um workflow padrão uma vez (ex.: um toque da Cadência 12x30), exporta, edita o JSON (texto, espera, tag) e importa as cópias. Precisa de teste na tela `app.wesalescrm.com` antes de confiar. |
| **API interna** (`backend.leadconnectorhq.com`, a que a própria tela usa) | Tudo que o builder faz: criar workflow, gatilhos, ações, ramos, publicar/rascunho, clonar. Dois projetos abertos: `drleadflow/ghl-automation-builder` (95 ações, 93 gatilhos com schema, 16 ferramentas MCP `ghl_workflow_builder_*`, mas preso ao Cloudflare Worker do autor) e `gojc31/gohighlevel-cli` (Python, `--experimental`, `utils/workflow_builder.py` com `tag_step`/`wait_step`/`link_steps`). | Máquina do dono | **alto**: endpoint não documentado, muda sem aviso, pode ferir os termos da HighLevel; o token é o `Authorization: Bearer` capturado na aba Network do navegador logado (desde ~07/2026 o endpoint rejeita o id-token Firebase da extensão). | Tecnicamente é o único caminho 100% programático. Só com decisão explícita do dono, e nunca deste ambiente. |
| **MCP comunitários** (`BusyBee3333/go-high-level-mcp-2026-complete`, 927 ferramentas; `mastanley13`, `hridayshah7`, etc.) | Cobrem a API pública. O de 927 ferramentas admite no README que criação de workflow é "superfície interna privada/instável com autenticação derivada do navegador" e manda para um produto pago (RealWave). | — | — | Não acrescentam nada ao conector que já temos. |
| **Automação de navegador** (Selenium/Playwright, citada na comunidade) | Clicar na tela por script. | Máquina do dono | médio (a tela muda) | Bloqueado daqui (R anterior). Pior que importar JSON. |

**Teste feito neste ambiente:** `backend.leadconnectorhq.com:443` e
`services.leadconnectorhq.com:443` também recebem `403 CONNECT` do proxy
(`__agentproxy/status`, 21/09 21:51). Ou seja, mesmo com o bearer em mãos, a
API interna não é alcançável daqui — só do computador do dono ou de um
ambiente com política de rede que libere esses hosts.

**Regra prática, em ordem de preferência:**
1. **Montar 1 modelo na tela + extensão de JSON para clonar** — resolve o
   grosso do trabalho repetitivo (12 toques da Cadência, 5 workflows de
   estagnação que só mudam etapa/tag/prazo). Os JSONs exportados vão para
   `wesales/workflows-json/` como fonte de verdade versionada.
2. **Snapshot da subconta** quando a montagem fechar — backup e replicação.
3. **API interna** só se o dono decidir assumir o risco; aí o ambiente certo
   é o computador dele rodando `gojc31/gohighlevel-cli`, com os
   `wesales/IMPLEMENTACAO-WORKFLOWS.md` como spec. Este ambiente nunca terá
   rota até esses hosts.

Fontes: `github.com/drleadflow/ghl-automation-builder`,
`github.com/gojc31/gohighlevel-cli` (README, seção "Workflow building"),
`github.com/BusyBee3333/go-high-level-mcp-2026-complete`,
Chrome Web Store `ghl-workflows-json-export/epnhegdiefihpjkgjkfmnkkobkhmfepk`
e `ghl-workflow-backup-audit/laoblobglngndhbdbecpfnfeaojhbnli`,
`ideas.gohighlevel.com/automations/p/rest-api-workflow-postput-endpoint-for-creating-and-updating-workflows`,
`help.gohighlevel.com/.../155000001229-how-to-copy-workflow-to-another-sub-account-`.

## Playwright contra a tela da WeSales: bloqueado pela política de rede do ambiente, não pela plataforma — 21/09/2026, ao vivo em chat

O dono pediu para tentar o único caminho ainda não testado para criar
workflow sem clique humano: automação de navegador (o ambiente tem Chromium
em `/opt/pw-browsers/chromium` e `playwright@1.56.1` global no Node 22).
Antes de pedir credenciais, testei se o sandbox alcança a tela:

```
curl https://app.wesalescrm.com/  →  curl: (56) CONNECT tunnel failed, response 403
$HTTPS_PROXY/__agentproxy/status  →  recentRelayFailures: connect_rejected,
    "gateway answered 403 to CONNECT (policy denial)", host app.wesalescrm.com:443
```

É a **política de rede do ambiente de execução** (escolhida ao criar o
ambiente no Claude Code on the web — `code.claude.com/docs/en/claude-code-on-the-web`)
negando o domínio, o mesmo bloqueio que já derruba `help.gohighlevel.com`,
`highlevel.stoplight.io` e `marketplace.gohighlevel.com` desde o R-09. O
navegador sairia pelo mesmo proxy, então nem chegaria à página de login —
credenciais não resolveriam. O conector `GHL CRM` funciona porque passa por
`mcp-proxy.anthropic.com`, que está na lista de exceções.

**Regra prática:** o caminho Playwright só existe se o dono trocar a
política de rede do ambiente para liberar `app.wesalescrm.com` (e os
domínios de assets da HighLevel que a UI carrega) e abrir uma sessão nova.
Ainda assim seria um piloto num workflow em rascunho, com sessão logada
fornecida por ele — nunca num publicado. Até lá, o caminho continua sendo
o manual pelo `IMPLEMENTACAO-WORKFLOWS.md`, com teste por API.

Zero escrita no CRM.

## "Esperar até uma data dinâmica" não é mais bloqueio: o `Wait` do GHL tem opção `Dynamic` — F-05 fechado (peças 5 e 6) — 21/09/2026, sessão automática

Desde a peça 1 do F-05 (18/09/2026), o roadmap registrava a última
invariante do Monitor de Saúde (`Retorno agendado`/`Data do retorno`
vencida) como bloqueada por "esperar até uma data dinâmica, não testado
neste conector". Cada rodada seguinte (peças 2, 3, a nota de fechamento
depois da peça 4) reconferiu a razão de esperar e a manteve — até esta
rodada, seguindo a própria instrução do roadmap ("reler o 'por quê estamos
esperando' de todo item represado").

**Pesquisado via `WebSearch`** (domínios da HighLevel seguem bloqueados
pelo proxy deste ambiente, mesma limitação de sempre — a busca lê o
resultado de IA sobre a página de suporte, não a página em si): o nó `Wait`
do GHL tem uma opção **Dynamic** (ao lado de **Standard**, um valor fixo),
descrita como lendo "a data de um campo do contato em tempo de execução".
**O que eleva a confiança acima do padrão usual deste projeto para achado
só de busca:** a mesma frase — "Standard is a fixed date you choose... Use
Dynamic when the value should be read from a contact field at runtime" —
apareceu **palavra por palavra**, em duas buscas com termos diferentes,
sinal de que é o texto real do artigo oficial ("Workflow Wait Action Setup
and Options") sendo citado, não uma paráfrase que poderia estar errada. Um
changelog da própria HighLevel ("Wait Action: Major Revamp") reforça que a
funcionalidade existe e é recente. **Nível de confiança: médio-alto** —
mais alto que "uma fonte de IA sobre documentação" isolada, mas ainda não
confirmado numa tela desta subconta.

**Regra prática, generalizável:** quando uma busca de IA sobre documentação
retorna a mesma frase, quase idêntica, em consultas com termos de busca
diferentes, é um sinal de que ela está citando o texto original (que a IA
não inventaria duas vezes do mesmo jeito) — vale mais confiança do que uma
única busca, mesmo sem conseguir ler a página fonte direto (proxy bloqueia
`help.gohighlevel.com`, `ideas.gohighlevel.com` e blogs de terceiros como
`consultevo.com` igualmente).

**Isso desbloqueou as duas invariantes finais do F-05**, peças 5
(`AGENDAR` sem fechar o loop em 24h — `build-wesales.md`, seção 2.23) e 6
(retorno vencido sem reclassificação — seção 2.24), fechando o item por
completo. Um achado de desenho na peça 6 vale registrar à parte: o gatilho
"campo alterado" que ela precisa (`Data de retorno`) já está **provado em
produção**, não só em documentação — o Pós-ligação (seção 4) usa
exatamente esse tipo de filtro (`Resultado da tentativa` alterado) há dias,
com 24 execuções confirmadas (ver "Diagnóstico por contador vizinho",
abaixo). Isso resolve, por evidência própria do projeto e não só por busca,
a mesma dúvida que a peça 3 tinha registrado com confiança baixa ("dispara
quando escreve o mesmo valor?") — aqui o campo é uma data escolhida pelo
SDR a cada ligação, não um valor de uma lista fechada, então a chance de
reescrever o **mesmo** valor é baixa o bastante para não precisar da
resposta exata daquela dúvida.

Zero escrita no CRM nesta rodada: as duas peças são especificação
(`build-wesales.md`, seções 2.23/2.24, mais os retoques nos nós 0/4 do
Mestre de saída — seção 3 — e o nó 3c novo do Pós-ligação — seção 4), um
campo novo (`Checkpoint — Data de retorno`, C-28) e duas tags novas
(`agendar-estagnado` T-19, `retorno-vencido` T-20) propostas, não criadas —
nascem `[ ]` em `APROVADO.md`, mesma regra desde o incidente da T-15.
Subconta reconfirmada via `opportunities_get-pipelines`/
`opportunities_search-opportunity`/`locations_get-custom-fields`: mesmas 5
etapas do `FUNIL DE VENDAS`, 46 campos, 50 oportunidades (47 `NOVO LEAD` +
3 `NEGOCIAR`, status `open` em todas) — sem mudança desde a última rodada;
G-03/G-04 seguem aguardando o dono.

## Teste do Loop do closer não disparou; o Mestre de saída dispara na criação da oportunidade — 21/09/2026, ao vivo em chat

**Teste por API do `Post-Meeting Closer Loop` (seção 5.1), a pedido do
dono:** gravei em `Teste Atendeu` (`NEGOCIAR`, `open`) `Nota de
qualificação` = 80, depois (8 s depois) `Reunião foi qualificada` = `Não` +
`Motivo da desqualificação` = `Sem fit` via `contacts_update-contact`
(`customFields: [{id, fieldValue}]` — o `id` do campo funciona; testado).
Duas leituras (30 s e 2 min): nenhum rastro — `Data do veredito` vazia,
nenhuma nota nova, status ainda `open`, `dateUpdated` do contato parado na
minha escrita. Conclusão: o workflow não executou — está em rascunho (toggle
"Publicar" desligado em todas as telas do dono, com dois nós marcados "há um
problema com esta configuração"). O contato ficou preparado para o
re-teste (mudar o veredito para `Parcial` e voltar a `Não` depois de
publicar — `Allow Re-entry` ligado exige que o campo *mude*).

**Achado lateral, confirmado com timestamp:** o `Mestre de saída` (id de
workflow `30da2c98…`) grava a nota "Saída de cadência · status: open" **4
segundos depois** de a Porta de Entrada criar a oportunidade em `NOVO LEAD`
(`Carlos Andrade`, criado 09:17:26, nota 09:17:30) e aplica
`limpar-tarefas` — em todo lead novo. `Create/Update Opportunity` dispara
`Opportunity Stage Changed`, e o portão do nó 1 só encerrava para
`CONECTAR`+`open`. Corrigido na especificação (seção 3: nó 1 também encerra
em `NOVO LEAD`) e na tabela de retoques do `GUIA-MONTAGEM.md`; a tela
ainda precisa do clique. **Regra prática:** todo workflow com gatilho
`Opportunity Stage Changed` sem filtro de etapa de destino recebe também a
**criação** da oportunidade — o portão precisa tratar `NOVO LEAD`
explicitamente, não só a etapa que ele "espera".

**Dois achados menores, pelo mesmo rastro:** (1) o merge field
`{{opportunity.pipeline_stage}}` renderiza **vazio** na nota publicada
(`{{opportunity.status}}` renderiza certo) — o token real precisa ser pego
no seletor `{}` da tela; (2) a nota "REUNIÃO AGENDADA · nota /100" do
Pós-agendamento saiu com nota, `Empresa`, `Segmento`, `Agendado por`, `Para`
e `conexões` em branco, e uma nota "Checklist de Autoauditoria" gravada pela
IA do construtor no contato diz que a nota de qualificação foi montada como
"custom code" — é o nó 4 que nunca escreve `nota_de_qualificao`.

Tudo isso virou `IMPLEMENTACAO-WORKFLOWS.md`, novo: a configuração exata de
cada nó de cada workflow (ação, campo, operador, valor, ramo), com os nomes
reais lidos da subconta — para montar à mão. Escrita no CRM nesta rodada:
só os 3 campos do contato fictício `Teste Atendeu` (teste do checklist,
seção 10, autorizado em `APROVADO.md`); nenhum lead real tocado.

## Um número copiado de um enunciado precisa ser confrontado com a régua real antes de virar condição — 21/09/2026, ao desenhar a peça 3 do F-05

Desenhando a peça 3 do Monitor de Saúde (`CONECTAR` sem tentativa nova),
copiei primeiro o número literal do "Como" original do F-05 (`briefing-sdr.md`
não, `ROADMAP-SALES-ENGAGEMENT.md` mesmo): "7 dias". Antes de escrever o nó,
conferi a tabela 2.5 (`build-wesales.md`) — a régua das 12 tentativas — e
achei um degrau de **10 dias corridos** entre T10 (D20) e T11 (D30), o maior
intervalo planejado da cadência inteira. Um alarme em "7 dias sem tentativa
nova" dispararia para **todo** lead são passando por esse intervalo — o
oposto exato do que a peça existe para detectar.

**A mesma classe de erro que a peça 2 já tinha cometido e corrigido** (relógio
relativo de 24h confundindo intervalo legítimo entre tentativas próximas com
trava real), só que achada **antes** de publicar, não depois de gerar falso
positivo em produção. Corrigido para 14 dias: acima do maior degrau real (10)
com folga para o empurrão de dia útil que a seção 2.5 já documenta.

**Regra prática, generalizável:** todo número de um "Como" do roadmap que vira
condição de tempo (`N dias sem X`, `N horas de atraso`) precisa ser
confrontado contra a tabela real da régua que ele monitora antes de virar
nó — o enunciado foi escrito antes da tabela existir em detalhe, e o maior
intervalo planejado é sempre o candidato a furar um número redondo escolhido
de memória. `grep` pela tabela de deltas da régua (seção 2.5 e as que a
espelham) e pegue o maior valor antes de escolher o limite do alarme.

## `Opportunity Stage Changed` é incerto quando a ação escreve a mesma etapa que já existia — prefira um gatilho por campo quando o "reentra" pode não sair da etapa — 21/09/2026, mesma rodada acima

Ainda desenhando a peça 3: o instinto era copiar o gatilho da peça 1
(`Opportunity Stage Changed → CONECTAR`), que cobre a entrada vinda de
`NOVO LEAD` e a da Cadência Inbound de graça. Não cobre o Reengajamento 90
dias (seção 2.12): o nó 5 daquele workflow escreve `Etapa → CONECTAR`
quando a oportunidade **já está** em `CONECTAR` havia semanas (12 tentativas
esgotadas nunca move de etapa, só muda `status` — tabela 1.0). `WebSearch`
na documentação oficial (`help.gohighlevel.com/.../workflow-trigger-
pipeline-stage-changed`) descreve o gatilho como reagindo a "opportunity
moves from one stage to another" — não cobre, nem confirma nem nega, o caso
de uma ação escrever o mesmo valor que o campo já tinha. Sem fonte que
resolva a dúvida, apostar que o evento dispara mesmo assim arriscava deixar
**todo** lead reativado sem monitor nenhum — o pior resultado possível para
uma peça que existe para pegar o que mais ninguém vê.

**Resolvido evitando a dúvida, não resolvendo-a:** em vez de `Opportunity
Stage Changed`, o gatilho virou **Contact Changed** filtrando por Custom
Field `Tentativa nº` **igual a** `0` — o valor que os três pontos de início
de rodada (Cadência 12x30, Cadência Inbound, Reengajamento) já escrevem
sempre, sem exceção nenhuma, porque cada um zera o contador como parte da
própria inicialização (confirmado no texto de cada seção, não hipótese).
`WebSearch` confirma que o `Contact Changed` aceita filtro por Custom Field
com operador de igualdade (nível de confiança médio: documentação oficial,
não testado nesta subconta).

**Regra prática, generalizável:** quando um evento de "entrada" pode
acontecer sem mudança de valor visível no campo mais óbvio (aqui, etapa que
já estava onde deveria), procure um campo que **sempre** muda nesse
instante, mesmo que seja um campo vizinho em vez do campo "principal" do
evento — reset de contador, carimbo de timestamp, tag de pulso. `Tentativa
nº` voltando a `0` é mais confiável como "início de rodada" do que a etapa
em si, porque nenhuma das três réguas jamais pula esse reset, e nenhuma
delas depende de a etapa ter mudado de verdade.

## Nem todo campo compartilhado é um "contador com dois donos" — a diferença é a frequência de escrita concorrente, não o fato de ser compartilhado — 21/09/2026, mesma rodada acima

A peça 3 precisa de um campo `Checkpoint — Tentativa nº` (C-27) escrito e
lido pelo mesmo workflow, para comparar "avançou desde a última checagem?"
14 dias depois. O primeiro instinto foi rejeitar o desenho por medo do
mesmo bug já documentado nesta base (F-04/`Toques na semana`, e a peça 2
descartando explicitamente um campo de snapshot pelo mesmo motivo): várias
instâncias do mesmo workflow escrevendo no mesmo campo compartilhado quase
ao mesmo tempo corrompem a leitura umas das outras.

**A diferença que salva este desenho, e vale generalizar:** o risco daqueles
dois casos não vinha de o campo ser compartilhado — vinha da **frequência**
de escrita concorrente. `toque` dispara a cada tarefa criada ou mensagem
enviada, várias vezes por dia por lead nos picos da régua; duas instâncias
brigando pelo mesmo campo em minutos de diferença é o caso comum, não a
exceção. Aqui o gatilho só dispara quando `Tentativa nº` volta a `0` — no
máximo três vezes na vida inteira de um lead (entrada inicial, handoff do
fim da Cadência Inbound, uma reativação), cada disparo separado dos outros
por dias ou semanas. Duas instâncias correndo por cima uma da outra é a
exceção rara (só no handoff), não o caso comum, e mesmo nela o efeito é um
falso "tudo bem" isolado numa instância redundante que sai cedo — nunca um
alarme real ficando mudo, porque a instância mais nova sempre continua seu
próprio laço a partir do seu próprio início.

**Regra prática, generalizável:** antes de rejeitar um campo de checkpoint
por medo do "contador com dois donos", pergunte quantas vezes por vida do
lead o gatilho realmente dispara, e quão perto no tempo essas vezes podem
cair. Um campo escrito 2-3 vezes espaçadas por dias não tem o mesmo risco
que um campo escrito dezenas de vezes por dia — a lição de F-04 e da peça 2
é sobre concorrência real, não sobre "todo campo compartilhado é perigoso".

## Um relógio de "24h desde o gatilho" pode medir a tentativa errada quando o mesmo evento se repete várias vezes por lead — 21/09/2026, sessão automática

Desenhando a peça 2 do F-05 (Monitor de Saúde — `fila-tel`/`fila-wa` presa
mais de 24h), a primeira versão copiou literalmente o mecanismo que já
validou a peça 1 e o R-02: `Wait` de 24h a partir do gatilho
(`Contact Tag Added`), depois um portão checando se a tag ainda está
presente. Funcionou de olho na peça 1 porque `NOVO LEAD` só recebe **um**
evento relevante por entrada. Aqui não: a tabela 2.5 (`build-wesales.md`,
seção 2.5) aplica `fila-tel`/`fila-wa` até 12 vezes no mesmo contato, às
vezes a **menos de 24h** uma tentativa da outra (T1 D1 10:30 → T3 D2
09:20, 22h50 de distância). Um relógio de 24h disparado pela T1 checaria o
contato durante a janela em que a T3 já reaplicou a mesma tag de forma
legítima e recente — o alerta leria "tag presente" e confundiria fila nova
e saudável com fila velha e travada, gerando falso positivo toda vez que
duas tentativas ficassem próximas (o que a tabela 2.5 faz de propósito,
não é caso raro).

**A correção não foi adicionar uma condição — foi trocar o tipo de
relógio.** Em vez de "espera relativa a partir do disparo" (`Wait → Time
Delay`), usar "espera até um horário fixo do dia" (`Wait → Until specific
time`, 19:00 — 30 min depois do prazo de 18:30 que o próprio nó 9 do bloco
padrão já respeita). Como a tag só pode legitimamente existir entre o
início da tentativa e 18:30 do **mesmo dia**, ancorar a checagem num
horário do calendário em vez de um delta a partir do gatilho garante que
cada instância do monitor só vê o resultado do **seu próprio** dia,
independente de quantas outras tentativas dispararem o mesmo gatilho depois
dela.

**Alternativa cogitada e descartada, registrada para não ser retentada:**
snapshotar `Tentativa nº` num campo novo no momento do gatilho, e comparar
contra o valor atual 24h depois. Não funciona aqui pelo mesmo motivo que a
seção 2.4 já documenta para `WA não atendidas seguidas` ("um contador com
dois donos sempre diverge"): com `Allow Re-entry` ligado e duas
tentativas próximas, duas instâncias do workflow escrevem no **mesmo**
campo do contato quase ao mesmo tempo — a segunda sobrescreve o snapshot da
primeira antes da primeira terminar de esperar, e a comparação final lê o
valor errado.

**Regra prática, generalizável:** antes de copiar um mecanismo de "relógio
por evento" (já usado no R-02, na peça 1 do F-05 e no SLA do Closer) para
um gatilho novo, perguntar "este evento pode disparar mais de uma vez para
o mesmo contato dentro da janela de espera do relógio?" Se a resposta for
sim, uma espera **relativa** ao disparo é a peça errada — o disparo mais
recente sempre corrompe a leitura do mais antigo. A peça certa é ancorar a
espera num ponto fixo do calendário (hora do dia, ou uma data gravada em
campo que **nenhuma** outra instância reescreve) que todas as instâncias
concordam em checar, não uma contagem que cada instância mede a partir de
si mesma.

## Os dados de produção são a terceira auditoria — e acharam o que texto e tela não achavam — 21/09/2026, a pedido do dono

Pedido ao vivo: "consulte o que foi configurado no CRM, atualize os
documentos". Até aqui o projeto tinha duas auditorias: a de **texto**
(grep por nome de etapa, merge field órfão — G-02) e a de **tela**
(lista de workflows colada pelo dono, `locations_get-custom-fields`). Esta
rodada leu a **terceira**: os valores gravados nos 50 contatos e 50
oportunidades, e o que os workflows publicados deixaram neles. Três
achados que nenhuma das outras duas podia ver:

1. **`Investimento mensal em anúncios` recebe do Meta quatro textos, e só
   um é opção do campo.** `SINGLE_OPTIONS` no GHL não recusa valor fora da
   lista quando quem escreve é a integração do Lead Ads — grava o texto do
   anúncio como veio (`Não invisto nada ainda`, `Até R$ 1.000`, `Abaixo de
   5k`). A régua 9.1 compara contra `Até 1k`/`1k a 5k`/`5k a 10k` e nunca
   casa. É a classe de bug do R-16 (rótulo que a tela não tem), só que o
   R-16 corrigiu o *documento* contra a *tela*; aqui a tela também está
   errada contra o *dado*. **Regra prática:** para todo campo `SINGLE_OPTIONS`
   alimentado por integração (Meta, formulário, API), conferir os valores
   *gravados* (`contacts_get-contacts`, `customFields[].value`) contra
   `picklistOptions` — não basta conferir o documento contra a tela.
2. **`Necessidade`/`Urgência` não eram duplicatas paradas** (Tabela F de
   `CONFERENCIA-CAMPOS.md` esperava decisão há dois dias) — são onde o Meta
   grava, com 34 e 39 contatos preenchidos. Enquanto o documento discutia
   "de que lado fica", o dado já tinha escolhido o lado errado. E o
   mapeamento mudou no meio (os 5 leads mais novos caem em `Dor
   principal`): auditoria de campo precisa olhar *quando* cada valor
   chegou, não só *se* chegou.
3. **Rastro de execução vale mais que status "Publicado".** Pós-agendamento
   está publicado com 3 ativos, e os 3 têm `Prioridade` e `Data agendado`
   gravados — mas `Nota de qualificação` vazia nos 3. Pós-ligação rodou 24
   vezes num contato e `Total de conexões` continua vazio. Os 10 leads
   nascidos depois do Mestre de saída ir ao ar chegaram com
   `limpar-tarefas`. Nenhum desses três aparece na lista de workflows nem
   num grep — só no valor do campo. **Regra prática:** depois de publicar um
   workflow, ler os campos que cada nó deveria ter escrito nos contatos que
   passaram por ele; nó que não deixou rastro não rodou, esteja o workflow
   "Publicado" ou não.

Detalhe e opções de correção: `CONFERENCIA-CAMPOS.md` (Tabela H) e
`GUIA-MONTAGEM.md` ("Estado da montagem em 21/09/2026"). Novo item G-04 no
`ROADMAP-SALES-ENGAGEMENT.md`. Zero escrita no CRM: tudo é decisão do dono
(formulário do anúncio, opções de campo, nós de workflow — nada sai por
API neste conector). Confirmado também pelo lado das conversas: **zero
mensagem de WhatsApp/SMS enviada pela operação até hoje** — R-14 segue
esperando com razão.

Limite desta leitura, registrado para ninguém confiar além do que ela
prova: `calendars_get-calendar-events` por `userId` voltou vazio para o
dono das 3 oportunidades em `NEGOCIAR`, embora `Data agendado` tenha sido
gravada pelo gatilho `Appointment Status` — a busca por usuário pode não
enxergar evento sem responsável, e o conector não lista calendários para
buscar por `calendarId`. Não dá para afirmar por API se os 3 agendamentos
existem.

## F-05 destravado pelo próprio G-03: "espera volume" tinha prazo de validade — 21/09/2026, sessão automática

Sweep de coerência de sempre (limpo — zero merge field órfão, zero nome de
etapa antigo fora da tabela 1.0, listas de réguas batendo com as listas de
remoção do Mestre de saída). Antes de procurar lacuna nova do zero, reli o
F-05 (Monitor de Saúde da Operação) com a pergunta que a nota final do
roadmap já sugeria: "por que ele está esperando, e essa razão ainda é
verdade?" A "Ordem sugerida" dizia "F-05 só morde quando há mais de uma
cadência no ar" — **e essa frase nunca foi verdade**: as invariantes do
F-05 (lead parado numa etapa, tarefa vencida) checam **um** lead contra
**uma** régua de cada vez, nunca comparam réguas entre si. A frase
confundiu "por que o item ainda não incomodou ninguém" (não havia lead de
verdade correndo cadência nenhuma) com "o que o item precisa para fazer
sentido" (lead de verdade, ponto — não importa quantas réguas existem). E
lead de verdade é exatamente o que G-03 (Bloco 0, mesma data) achou: 47
oportunidades pagas paradas em `NOVO LEAD` há mais de 24h, e ninguém — nem
uma automação, nem um dashboard — avisou sozinho. Isso não é só "F-05
deixou de esperar volume"; é a prova em produção de que o problema que o
F-05 existe para pegar já aconteceu, sem F-05 no ar para pegá-lo.

**Regra prática, generalizável:** "este item espera X" é uma afirmação
com data de validade, igual ao achado já registrado abaixo ("número medido
dentro de uma instrução tem data de validade") — mas aqui a validade não
era de um número, era do **raciocínio**. Vale reler o "por quê estamos
esperando" de todo item represado a cada rodada sem tela, não só reconferir
se o número mudou: às vezes o número que faltava já chegou por um caminho
diferente do que o enunciado original previa.

**Desenhada só a primeira peça (lead esquecido em `NOVO LEAD`, que nem
estava nas seis invariantes originais do "Como") — decisão de escopo,
registrada no roadmap (F-05).** Achado que vale por si, para não redesenhar
a mesma coisa depois, e que exige cuidado para não confundir duas
invariantes parecidas: "tarefa vencida sem resultado" **já não existe como
risco** neste desenho — o nó 10b do bloco padrão de tentativa
(`build-wesales.md`, seção 2.4) já classifica sozinho `Resultado da
tentativa = Não atendeu` quando o prazo do dia estoura sem o SDR agir, e a
lista 8.5 já mostra esse volume; não sobra "vencida sem resultado" pendurada
em lugar nenhum. **Isto não vale para a invariante vizinha da mesma
lista original, `fila-tel`/`fila-wa` presente há mais de 24h** — essa
continua um risco de verdade e diferente: se a tag ainda está lá depois de
24h é porque o nó 9 (que remove a tag sempre, todo dia até 18:30) não
rodou, sinal de workflow travado ou instância perdida, não de SDR lento.
Quase escrevi as duas como a mesma coisa por causa do nome parecido — vale
a mesma pergunta antes de desenhar qualquer invariante futura do F-05:
"isso ainda é um risco no desenho atual, ou o desenho já mudou debaixo
dela — e é exatamente esta invariante, ou uma vizinha de nome parecido?"

**Achado de desenho, mesma classe de bug que a entrada "A regra certa
estava no portão errado" (abaixo) já descreveu para outras réguas, aqui
achado *ao especificar*, não *depois de publicado*:** o Mestre de saída
(seção 3) só alcança seu nó de remoção de tag quando a oportunidade **sai**
de `CONECTAR`/`open` — a transição `NOVO LEAD` → `CONECTAR`, que é como o
alerta de F-05 se resolve na prática, cai no ramo de no-op dele (nó 1) e
nunca chega lá. Resolvido com um nó 0 novo, incondicional, antes do portão
— `Remove Contact Tag` de quem não tem a tag não custa nada, mesmo
raciocínio já usado para `Remove from Workflow`. Registrar aqui porque é a
primeira vez que este projeto pega esta classe de bug **durante o desenho**
em vez de descobri-la numa migração posterior — vale perguntar "este alerta
se resolve numa transição que o Mestre de saída trata como no-op?" toda vez
que uma tag nova precisar de limpeza automática.

Zero escrita no CRM nesta rodada: item de especificação
(`build-wesales.md`, seções 2.20, 3 e 8.20; `campos-e-tags.md`, T-16;
`ROADMAP-SALES-ENGAGEMENT.md`, F-05) mais uma tag nova **proposta**, não
criada — `novo-lead-estagnado` nasce `[ ]` em `APROVADO.md`, não `[x]`
(mesma regra do incidente da T-15, 19/09/2026, aplicada desde o primeiro
dia desta vez, não como correção depois). Subconta reconfirmada via
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`, 46
campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, status `open` em
todas) — sem mudança desde a última rodada; G-03 segue aguardando o dono.

## R-17: resposta de opt-out tratada como sinal quente por um workflow já publicado — 21/09/2026, sessão automática

Depois do sweep de coerência de sempre (limpo, ver entrada abaixo), reli o
2.9.3 (`Interceptação de Sinal — Resposta`) com atenção ao invés de só
conferir nome de etapa — mesmo método do G-02. Achado: o gatilho
`Customer Replied` não olha o **conteúdo** da resposta, só o canal. Um lead
que responde "pare, não me manda mais mensagem" recebia `Prioridade` = 5,
tag `fila-quente` e tarefa "ligar agora" — o mesmo tratamento de quem
demonstra interesse. E não é achado de documento parado: `GUIA-MONTAGEM.md`
("Estado da montagem em 19/09/2026, mais tarde") já registrava esse
workflow como **Publicado**, 1 inscrito — o defeito estava ativo na
subconta, não só na especificação.

**Pesquisado (`WebSearch`, já que os domínios de suporte da HighLevel
seguem bloqueados neste ambiente — mesma limitação de sempre):** o
changelog oficial da HighLevel (`Customer Replied Trigger: Improved Message
Filters`) confirma que o gatilho aceita filtro pelo **corpo da mensagem**
com operadores `Contains`/`Doesn't Contain`/`Exact Match`, além de canal,
tag (`Has Tag`/`Doesn't Have Tag`), tipo de intenção e canal de resposta.
Isso fecha duas dúvidas de uma vez: dá para restringir um `Customer Replied`
por palavra-chave sem precisar de um nó dentro do workflow, e dá para
**excluir** por palavra-chave o gatilho de um workflow vizinho — é o que
permite dois workflows ouvindo o mesmo evento nunca disparar para a mesma
mensagem (`Contains` num, `Doesn't Contain` a mesma lista no outro).
**Nível de confiança: médio** — confirmado por busca (resultado de IA sobre
página de suporte + changelog oficial), não testado na tela desta subconta;
a especificação (`build-wesales.md`, seção 2.9.5) já avisa para confirmar
na tela se o campo aceita várias frases numa linha só (OR) ou se precisa de
uma linha por frase — o desenho não depende de qual das duas for verdade.

**Regra prática, generalizável:** todo gatilho `Customer Replied` já
montado ou a montar neste projeto (2.9.2 não precisa, é `Trigger Link
Clicked`; 2.9.3 e qualquer futuro workflow que reaja a resposta de texto)
devia nascer perguntando "e se a resposta for um pedido para parar?" antes
de decidir a ação — não é um caso de borda raro, é a única resposta que a
operação inteira existe para nunca tratar como oportunidade.

Zero escrita no CRM: item de documentação e especificação pura
(`build-wesales.md` seção 2.9.5 + retoque no gatilho da 2.9.3,
`ROADMAP-SALES-ENGAGEMENT.md` R-17, retoque em `GUIA-MONTAGEM.md`), não
depende de `APROVADO.md` — workflow e filtro de gatilho não saem por API,
igual a todo o resto do projeto.

## Sweep de coerência limpo — a lacuna nova estava nos dados de produção, não no texto — 21/09/2026, sessão automática

Sessão sem tela e sem R-14/F-05/F-06 desbloqueados (mesmo cenário de sempre).
Repeti a varredura que fechou o G-02: `grep` por nome de etapa antigo fora da
tabela 1.0 (limpo — só prosa histórica e a própria tabela), comparação de
merge field usado contra `fieldKey` real via `locations_get-custom-fields`
(zero órfão), e o par de greps que a entrada "A regra certa estava no portão
errado" pediu (réguas que existem vs. réguas que o Mestre de saída remove —
as duas listas fecham: `Cadência 12x30`, `Cadência Inbound`, `Reengajamento
90 dias`). Nada para corrigir — o `ROADMAP-SALES-ENGAGEMENT.md` já avisava
que isso podia acontecer e mandava procurar lacuna nova antes de encerrar
sem commit.

**A lacuna nova não estava em nenhum documento — estava em como os dados
mudaram desde a última leitura.** `opportunities_search-opportunity` por
etapa: `NOVO LEAD` foi de 40 (19/09) para **47** (21/09), todas reais
(Facebook Ads pago, nomes/telefone/e-mail/atribuição de campanha genuínos,
a mais recente criada hoje às 09:17 UTC), e **nenhuma** chegou a `CONECTAR`
— confirma que a lacuna L-07 (`briefing-sdr.md`, "promoção `NOVO LEAD` →
`CONECTAR` é manual, ninguém construiu gatilho") não é mais hipótese: é
lead pago de verdade parado há mais de 24h sem qualquer tentativa, o
oposto exato do que R-02/G-01 foram construídos para garantir. Escalado
como G-03 novo em `ROADMAP-SALES-ENGAGEMENT.md`, com três opções desenhadas
(promoção automática pura, promoção automática com janela de revisão,
ação manual em massa só para destravar o estoque de hoje) — nenhuma
executada: mover 47 oportunidades reais de etapa é ação em massa em dado
de produção (regra 2 do briefing) e a fila manual de hoje é decisão
deliberada do SDR registrada desde a primeira versão do projeto, não bug —
trocá-la é mudança de processo que só o dono decide, mesma régua já usada
para L-02/D-04.

**Regra prática, generalizável:** a varredura de coerência de documentos
(nomes, merge fields, contagens) não é a mesma varredura que detecta uma
lacuna que só aparece em produção — vale reler os números reais da
subconta (`opportunities_search-opportunity` por etapa, não só o total) a
cada rodada sem tela, mesmo com o texto todo consistente, porque uma
lacuna pode ficar dormente por dias até o volume a tornar urgente (mesma
lição, de novo, do achado "número medido dentro de uma instrução tem data
de validade" — lá era uma instrução envelhecendo, aqui é uma lacuna
acordando).

Zero escrita no CRM: as três opções do G-03 ficam propostas, não `[x]` em
`APROVADO.md`. Subconta reconfirmada: 46 campos, mesmas 5 etapas do
`FUNIL DE VENDAS`, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, dois
leads reais — `Daniel` e `Genilson | Bombeiro` — mais o contato fictício
`Teste Atendeu` do checklist, cujas tags batem com o cenário esperado da
seção 10).

## G-02 fechado: as últimas peças do checklist, e um checklist de teste mandando excluir oportunidade — 21/09/2026, sessão automática

Fechei o que restava do checklist de migração de nomes de etapa
(`GUIA-MONTAGEM.md`, Fase 1; `ROADMAP-SALES-ENGAGEMENT.md`, G-02): seções
2.6.1/2.7/2.8/2.9–2.9.4 (zero achado — já estavam certas, só faltava
marcar), seção 6, seção 8 completa (8.5–8.19), seção 9 e o checklist de
teste inteiro (seção 10). `grep -n "Em cadência\|Nutrição\|Retorno
agendado\|Descartado\|Pré-vendas" wesales/build-wesales.md` confirma:
sobra só tabela de tradução (1.0) e prosa histórica.

**Achado real, sétima ocorrência da mesma classe:** a lista `Recuperação de
No-show` (8.17) tinha um filtro **ativo** comparando etapa contra `Reunião
agendada` — nome que não existe mais na tela desde 18/09/2026. Mesma
classe de bug silencioso já documentada seis vezes nas entradas abaixo
(seção 3, 2.10, 2.11, 2.12, 2.16, família 5.3/5.4): quem escreveu a lista
sabia que a oportunidade fica em `NEGOCIAR` (a própria seção 5.3, migrada
antes, já dizia isso no título de uma subseção), mas a lista em si nunca
recebeu o mesmo tratamento — reforça a regra prática já registrada:
"seções já migradas" não significa "todo lugar que cita aquela seção já
está migrado".

**Achado fora do escopo de nome de etapa, generalizável:** a régua de
prioridade (9.2, regra 1) comparava `Resultado da tentativa = Pediu
retorno` **ou** `etapa = "Retorno agendado"` — a segunda metade do `ou`
nunca podia casar (etapa não existe) e nunca fazia falta (todo lead que
pede retorno já bate na primeira metade). Um `ou` morto não quebra nada
sozinho, mas é peso morto que qualquer leitura futura pode interpretar
como sinal de que a condição da esquerda não basta — removido, mesmo
raciocínio que a lista `Retornos` (8.4) já tinha aplicado.

**Achado que não é de nome de etapa, e por isso quase passou despercebido
numa rodada de G-02:** a última linha do checklist de teste (seção 10)
instruía "**apague as 5 oportunidades** e desative os 5 contatos" ao fim
do teste — viola a regra 1 do projeto (nunca excluir contato, campo, tag,
workflow, pipeline **ou oportunidade**), presente desde a primeira versão
do documento e nunca antes achada porque nenhuma rodada de migração de
etapa tinha motivo para ler essa linha final com atenção. **Regra
prática:** uma varredura de "nome de etapa antigo" não é a mesma varredura
que pega "instrução que viola regra inviolável" — vale reler o documento
inteiro, não só a área do achado que a rodada está caçando, antes de
declarar uma seção fechada. Corrigida para marcar `status = lost` em vez
de excluir.

Zero escrita no CRM: item de documentação pura, não depende de
`APROVADO.md`. Subconta reconfirmada via `opportunities_get-pipelines`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`
(`dateUpdated` ainda 18/09/2026 19:56 UTC) e 46 campos personalizados —
sem mudança desde a última rodada.

## Conferir cobertura de uma guarda: ela está escrita de três formas, e grepar o nome da ação diz que falta o que não falta — 22/09/2026

Fechado o G-06, fui verificar a afirmação que os dois itens fazem juntos:
"todo `Send WhatsApp` de texto livre tem guarda de janela". Grepei o nome da
ação (`Customer Service Window Check`) e achei **5** ocorrências num
documento com **30** menções a `Send WhatsApp` — parecia que a maioria dos
envios estava descoberta, e cheguei perto de escrever isso como achado.

Não estava. A guarda aparece de **três formas**, porque cada rodada escreveu
do jeito mais econômico no contexto dela:

| Forma | Onde aparece |
|---|---|
| `WhatsApp: Customer Service Window Check` | onde a guarda é **especificada** (2.6.2 e 6.0) |
| `Guarda de janela (seção 2.6.2, G-05)` | onde ela é **referenciada** num nó (MI-0, MI-F, RE-1, RE-2, NS-1, NS-2, Pós-agendamento 7-10) |
| `Send WhatsApp, modo Template` | onde só o **ramo de fora da janela** é descrito |

A verificação que não erra não procura a palavra: lista os envios e olha as
linhas **anteriores** a cada um, aceitando qualquer das três formas. Feito
assim, o resultado é que **um único** `Send WhatsApp` não tem guarda nas
linhas de cima — a pergunta 1 do Caminho B — e esse está coberto pela guarda
6.0 da entrada, como o próprio texto explica.

**A lição, que vale para qualquer auditoria de cobertura neste projeto:**
antes de concluir "falta em N lugares", pergunte *de quantas formas isso pode
estar escrito?* Documento longo escrito por muitas rodadas tem sinônimos por
construção — cada rodada abrevia o que a anterior definiu. Grep de uma forma
só produz falso positivo de lacuna, que é o tipo de achado que faz alguém
"consertar" o que já estava certo.

Efeito colateral útil da conferência: o parágrafo "Escopo desta rodada" da
2.6.2 ainda dizia que os outros dez envios seguiam **sem** guarda — ficou
dois dias desatualizado depois de a peça 2 cobri-los. Corrigido, com a
cobertura real e o comando de verificação ao lado.

## O dono criou 5 campos na tela e um merge field já nasceu órfão: travessão vira dois underscores — 22/09/2026

Primeira vez em dias que a montagem manual andou: **5 campos novos** na
subconta entre 23:15 e 23:33 de 21/09, todos conferindo com a especificação
em nome, tipo e placeholder — inclusive as escolhas finas de `TEXT` em vez de
`DATE` onde a hora importa:

| Campo | Tipo | Placeholder | Item |
|---|---|---|---|
| `Toques na semana` | NUMERICAL | — | F-04 |
| `Hora da conexão` | TEXT | `HH` | C-25 / F-02 |
| `Hora do retorno` | TEXT | `HH:MM` | pendência aberta desde 18/09 |
| `Checkpoint — Tentativa nº` | NUMERICAL | — | C-27 / F-05 peça 3 |
| `Checkpoint — Data de retorno` | DATE | — | C-28 / F-05 peça 6 |

Rodei a auditoria de merge field órfão (`grep` dos `contact.*` dos documentos
contra os 51 `fieldKey` reais) e ela pegou **um**:

```
contact.checkpoint_data_de_retorno   ← escrito no documento (1 underscore)
contact.checkpoint__data_de_retorno  ← real na tela      (2 underscores)
```

O GHL **remove** o travessão (`—`) em vez de transliterar, e os dois espaços
que o cercavam sobram como dois underscores seguidos. Mesma mecânica que já
tinha comido os acentos, agora com pontuação. A seção 2.24 foi escrita antes
de o campo existir, então adivinhou a chave pelo nome — e a chave errada num
`Wait → Dynamic` não dá erro: o nó lê vazio e o monitor inteiro deixa de
funcionar em silêncio.

**Regra:** nome de campo com travessão, dois pontos ou parêntese → **crie na
tela primeiro, leia o `fieldKey` por API, e só então escreva o merge field no
documento.** E rode a auditoria órfã depois de toda leva de campos novos;
ela custa dois comandos e é o único jeito de pegar isto antes do primeiro
lead passar:

```
grep -rho "contact\.[a-z0-9_]*" wesales/*.md | sort -u > /tmp/usados.txt
comm -23 /tmp/usados.txt /tmp/reais.txt   # reais.txt = fieldKeys lidos por API
```

Os quatro "órfãos" restantes são nativos do GHL e esperados:
`contact.first_name`, `contact.name`, `contact.source`,
`contact.company_name`.

## Portão que manda "qualquer outro" para o lado ruim: opção nova de campo nasce com o significado errado — 21/09/2026

O R-18 fechou a lacuna L-08 criando uma opção nova em `Resultado da
tentativa`: `Desqualificado`, para a ligação atendida que a própria conversa
mostrou não ter fit. Desenho certo — conta como conexão real, sai por
`status`, não passa por `AGENDAR`, não cria tarefa de agendar.

O que faltou está num nó **de outro workflow**: o nó 10 do bloco padrão da
cadência (seções 2.4 e 2.10) decide assim —

> `Atendeu` ou `Pediu retorno` → encerra · `Número errado` ou `Não ligar` →
> encerra · **qualquer outro** → próxima tentativa

Esse "qualquer outro" faz do nó um portão que **erra para o lado de
insistir**: toda opção nova no campo nasce, por omissão, significando
"continue ligando". Então o lead que o SDR acabou de desqualificar receberia
a tentativa seguinte no dia seguinte — o contrário exato do item. O Mestre de
saída acabaria removendo o contato (o ramo novo muda `status`), mas só depois
da janela assíncrona, e o texto do nó continuaria dizendo a coisa errada para
quem monta na tela.

**A regra, que vale além deste campo:** quando um portão tem um ramo
"qualquer outro / senão", **esse ramo é o valor-padrão de toda opção que
alguém criar depois** — e quem cria a opção está olhando outro documento.
Ao acrescentar valor a um campo que algum `If/Else` consulta, a pergunta é:
*em que ramo ele cai hoje, sem eu fazer nada?* Se a resposta for o ramo
perigoso, o portão precisa da linha nova **no mesmo commit** que cria a
opção.

Corrigido nos dois blocos e no `IMPLEMENTACAO-WORKFLOWS.md`. Registrada também
a alternativa mais segura por construção, **não aplicada**: inverter o nó —
listar `Caixa Postal` e `Não atendeu` como os únicos que seguem e mandar todo
o resto encerrar. Aí opção nova nasce significando "pare", que é o lado
barato de errar.

## `All Except Current` protege o workflow atual e corta o de quem o chamou — 21/09/2026

A peça 4 do F-05 trocou um monitor por uma ação nativa, e a ideia é melhor
que a original: em vez de **detectar** que um lead com `nao-perturbe`
continuou rodando régua, `Remove Workflows` → `All Except Current Workflow`
faz o vazamento não poder acontecer, sem lista de nomes para manter. Ficou
certa em três dos quatro lugares.

No quarto — o **Mestre de saída** — tem um efeito colateral grave, e ele vem
de uma pergunta que a própria rodada quase fez. Ela descartou
`All Workflows` com o argumento certo ("cortaria a própria execução deste
workflow, antes dos nós 4/5/6") e parou um passo antes: **`All Except
Current` protege o atual e corta o de quem chamou.** E o Mestre de saída
quase nunca é disparado pelo lead — ele é disparado por **outro workflow
mexendo na etapa ou no status, enquanto esse outro ainda está rodando**:

| Quem dispara | O que ainda faltava rodar | O que morreria |
|---|---|---|
| Pós-agendamento, nó 1 (move para `NEGOCIAR`) | nós 4-10 | `Nota de qualificação`, confirmação e os **três lembretes** de toda reunião agendada |
| Pós-ligação, ramo `Atendeu`, nó 6 (move para `AGENDAR`) | nós 7-9 | `Data conectado`, `Hora da conexão`, e a **tarefa `[CONECTADO]`** de toda conexão |

E como o Mestre roda em paralelo, o corte chegaria em momento diferente a
cada vez — às vezes depois do lembrete, às vezes antes. Bug não
determinístico, o pior tipo para diagnosticar numa operação.

**A regra:** antes de usar uma ação que age sobre "todos", pergunte **quem me
chamou, e ele ainda está rodando?** Ação de alcance total é segura num
workflow disparado pelo **lead** (opt-out, `Não ligar` — ali matar tudo é o
objetivo) e perigosa num workflow disparado por **outro workflow**. É a
mesma pergunta de "quem mais passa por aqui?", virada para trás: não *quem
vem depois de mim*, mas *quem está no meio de algo por minha causa*.

Nos outros três lugares a ação ficou: o Pós-agendamento é o `Current` e
protege os próprios lembretes; o opt-out e o `Não ligar` querem justamente
matar tudo que estiver pendente.

## Tag de diagnóstico precisa de saída pelo caminho da recuperação, não só pela saída de cadência — 21/09/2026

As três peças do Monitor de Saúde aplicam uma tag cada. Conferindo a peça 3
logo depois de escrever a lição do `fila-quente`, fiz a mesma conta para as
três:

| Peça | Tag | Sai quando o lead **se recupera**? |
|---|---|---|
| 2.20 · lead esquecido em `NOVO LEAD` | `novo-lead-estagnado` | **Sim** — nó 0 do Mestre de saída, incondicional, roda na transição `NOVO LEAD` → `CONECTAR`, que é a recuperação |
| 2.21 · fila travada | `fila-travada` | **Sim** — nó 0 do próprio workflow: uma tentativa nova aplicando `fila-tel` já prova que destravou |
| 2.22 · `CONECTAR` sem avanço | `conectar-estagnado` | **Não** — só saía pelo nó 4 do Mestre de saída, ou seja, quando o lead **sai de cadência** |

Na peça 3, o caminho do alerta terminava depois de avisar. Um lead que trava
14 dias, é alertado e depois volta a receber tentativas ficaria marcado como
estagnado para sempre, e a lista `Saúde — CONECTAR Estagnado` mostraria régua
saudável como parada. **Um monitor de saúde com lista suja é pior que nenhum
monitor: o gestor deixa de olhar.**

Corrigido fechando o laço — nó 5 (recuperação) remove a tag, nó 6 garante um
aviso só, nó 9 devolve ao `Wait`. Os três estados ficam certos sem repetir
aviso: parou → tag e um alerta; continua parado → laço em silêncio; voltou a
andar → tag sai e some da lista.

**A regra, agora com as duas metades:** a lição do `fila-quente` dizia
"conte onde aplica e onde remove". Esta acrescenta **qual** remoção costuma
faltar: a do **caminho da recuperação**. A saída de cadência todo mundo
lembra de limpar, porque é o fim da história; voltar ao normal não parece um
evento, e por isso não ganha nó. Toda tag que marca um **estado ruim
reversível** precisa de três saídas: recuperou, saiu de cadência, e nunca
mais volta a entrar.

## Diagnóstico por contador vizinho: o par que fecha prova que o mecanismo funciona — 21/09/2026

A auditoria de dados (`e98aec6`) achou dois nós que "não deixaram rastro" e
parou no sintoma. Os dois têm causa, e ela sai do mesmo dado, sem abrir a
tela — lendo **o que funcionou ao lado do que não funcionou**.

**Caso 1 — `Total de conexões` vazio depois de 24 execuções.** No contato
"teste atendeu":

| Campo | Valor | Nó que escreve |
|---|---|---|
| `Total de ligações` | 24 | Pós-ligação, nó 3 |
| `Tentativas telefone` | 24 | Pós-ligação, nó 2 |
| `Conexões telefone` | **8** | ramo `Atendeu`, nó 1 |
| `Total de conexões` | **vazio** | ramo `Atendeu`, nó 2 |

O ramo `Atendeu` rodou 8 vezes (senão `Conexões telefone` estaria vazio
também), e o par vizinho `Tentativas`/`Total de ligações` fecha nos dois
lados. Logo: o mecanismo de Math funciona, o ramo é alcançado, e **o nó 2 do
ramo não existe na tela** — a especificação o pede, quem montou pulou.

**Caso 2 — `Nota de qualificação` vazia nos 3 leads em `NEGOCIAR`.** Os três
têm `Investimento mensal`, `Decisor`, `Budget` e `Prazo` **preenchidos**:
não é falta de entrada. E têm `Prioridade` = 5, que é o nó **5** do
Pós-agendamento, um depois do Math. **O fluxo passou pelo nó 4 e saiu sem
escrever** — Math com campo de origem ou destino não selecionado, o mesmo
defeito que o assistente de IA do construtor já tinha produzido no
Pós-ligação.

**O método, que serve para qualquer nó silencioso:**

1. Ache um campo **vizinho** que o mesmo workflow deveria escrever e que
   está preenchido. Ele prova que o workflow rodou e chegou até ali.
2. Ache um campo escrito por um nó **posterior** ao suspeito. Se ele está
   preenchido, o fluxo passou pelo suspeito — o nó rodou e não escreveu, que
   é diferente de "o ramo não foi alcançado".
3. Confira se as entradas do nó suspeito estão preenchidas. Com entrada
   presente, saída vazia e nó posterior escrito, sobra uma explicação só:
   o nó está mal configurado ou não existe.

Isso separa três causas que de fora parecem a mesma coisa — ramo não
alcançado, entrada faltando, nó mal montado — **sem abrir a tela e sem
esperar o próximo lead passar**.

## Conte onde a tag é aplicada e onde é removida: os dois números têm que fechar — 21/09/2026

A peça 2 do F-05 (workflow "Fila Travada") acertou em cheio ao não copiar a
fórmula de relógio da peça 1 — `fila-tel` pode ser reaplicada a 22h50 de
distância, então "24h desde o gatilho" daria falso positivo estrutural.
Conferindo essa peça, fiz a conta que faltava para a tag vizinha:

| Tag | Aplicada em | Removida em |
|---|---|---|
| `fila-tel` / `fila-wa` | nó 6 do bloco padrão (2.4 e 2.10) | nó 9 (sempre, todo dia), ramo 3b, Mestre de saída nó 4 — **fecha** |
| `fila-quente` | **4 lugares**: 2.9.2 nó 6, 2.9.3, 2.10 nó 0.7, régua da IA (seção 9) | **2 lugares**: ramo 3b da tentativa, Mestre de saída nó 4 — **não fecha** |

O que faltava era a remoção do caso normal: **o sinal foi trabalhado**. Lead
que clica no link, recebe a tarefa "ligar agora", é ligado e marca
`Não atendeu` fica em `CONECTAR`/`open` — nada remove a tag, e ele mora na
lista `Fila Quente` (8.1) para sempre, misturado com quem deu sinal agora.
**A fila mais prioritária da operação é a que apodrece primeiro, porque nada
nela expira.** Já tem 1 contato nesse estado.

Corrigido com um nó 3b no Pós-ligação, não com um relógio: o gatilho daquele
workflow é `Resultado da tentativa` alterado, que é a definição operacional
de "alguém agiu sobre o lead". Sinal se consome quando é trabalhado, não
quando o dia acaba.

**Regra, barata e mecânica:** para cada tag de fila, contar os lugares que
aplicam e os que removem. Se aplicar em mais lugares do que remove, a
diferença é uma lista que vai apodrecer — e a remoção que falta é quase sempre
a do **caminho feliz**, porque o caminho de saída é o que todo mundo lembra
de limpar.

```
grep -n 'Add Contact Tag.*fila-' wesales/build-wesales.md
grep -n 'Remove Contact Tag.*fila-' wesales/build-wesales.md
```

## Quando a previsão do bug está escrita e o bug acontece do mesmo jeito — 21/09/2026 (causa-raiz do achado 3 da auditoria)

A auditoria de dados desta rodada achou que **os 10 leads nascidos depois do
Mestre de saída ir ao ar chegaram com `limpar-tarefas`**, e registrou o
sintoma sem causa. A causa é o nó 1 do próprio Mestre de saída: gatilho
`Opportunity Stage Changed` para **qualquer** etapa de destino, Porta de
Entrada criando a oportunidade em `NOVO LEAD`, e portão que só encerrava para
`CONECTAR`/`open`. Todo lead novo rodava a limpeza de saída na chegada:
`limpar-tarefas` aplicada e nota "Saída de cadência" num lead que nunca
entrou em régua nenhuma.

O que vale guardar não é o bug, é o formato dele. **A seção 2.12 tinha escrito
essa consequência antes de ela acontecer**, palavra por palavra, como
argumento para o Reengajamento não passar por `NOVO LEAD`:

> "…ele rodaria a limpeza inteira (incluindo aplicar `limpar-tarefas` e
> gravar a nota 'Saída de cadência' num contato que não estava, de fato,
> saindo de cadência nenhuma)… risco de corrida real com a rotina horária de
> manutenção."

O raciocínio estava certo e foi usado para desviar **um** workflow. Ninguém
perguntou "e quem mais passa por `NOVO LEAD`?" — a resposta era *todo lead da
operação*, pelo caminho mais movimentado que existe.

**Regra, a mais afiada da série "achado num lugar, ignorado nos outros N":**
quando uma seção explica por que **evita** um caminho, esse parágrafo é um
relatório de bug sobre o caminho, não uma justificativa de design. A pergunta
seguinte é obrigatória: **quem mais passa por aí, e por que está tudo bem
para eles?** Se a resposta for "ninguém pensou nisso", o bug já existe — só
não foi medido ainda.

Corrigido no nó 1 (`open` **e** etapa em `NOVO LEAD`/`CONECTAR` → encerra) e
na tabela de retoques do `GUIA-MONTAGEM.md`, marcado como o mais urgente dos
que dão para fazer hoje: o workflow está publicado e sujando o histórico de
todo lead que entra.

## A tabela de retoques de tela também é uma lista que alguém esquece de atualizar — 21/09/2026

A rodada do F-05 desenhou o Monitor de Saúde certo e, de quebra, achou um
detalhe fino: a limpeza da tag `novo-lead-estagnado` não podia entrar na
lista do nó 4 do Mestre de saída, porque o portão do nó 1 encerra em no-op
justamente na transição `NOVO LEAD` → `CONECTAR`, que é como o alerta se
resolve. Solução certa: um nó 0 incondicional, antes do portão.

O que faltou: **o Mestre de saída está publicado na tela**, e o nó 0 é
mudança numa peça que já roda. A tabela "retoques de tela pendentes" do
`GUIA-MONTAGEM.md` — que existe exatamente para isso — não recebeu a linha.
Especificação alterada + peça publicada = linha na tabela, sempre.

Duas melhorias que saíram daí:

1. A tabela ganhou a distinção **"dá para fazer hoje"** vs. "espera workflow
   que não existe". Sem isso, quatro linhas bloqueadas escondiam a única que
   estava pronta para executar — o nó 0 não depende de nada.
2. O texto de abertura dizia "**Dois** retoques pendentes" com cinco linhas
   embaixo. Número fixo fora da fonte vira mentira na rodada seguinte, que é
   a regra que o próprio prompt da rotina já manda seguir; agora não conta,
   só aponta para a tabela.

**Padrão, já com nome:** toda vez que uma rodada muda a especificação de uma
peça **publicada**, a pergunta é "onde fica a lista de coisas a mexer na
tela?" — e a resposta tem que ser essa tabela, no mesmo commit. Foi assim
que o R-17 acertou (entrou na tabela sozinho) e assim que o F-05 escorregou.

## `Contains` casa pedaço de palavra: `pare` está dentro de "parece ótimo" — 21/09/2026

A rodada do R-17 achou um bug real e importante (resposta de opt-out no
WhatsApp virava sinal quente: `Prioridade` 5 e tarefa "ligar agora" para quem
pediu silêncio) e desenhou o workflow certo. O problema estava na lista de
palavras-chave: começava com `pare` solto.

`Contains` do GHL casa **substring**, não palavra. `pare` está dentro de
*parece*, *aparelho*, *comparecer*, *preparei*, *separado*, *transparente*.
A resposta mais positiva que um lead brasileiro manda — **"parece ótimo, me
liga"** — contém `pare`. E como o 2.9.3 ganhou o filtro espelhado
(`Doesn't Contain`), o falso positivo custava duas vezes na mesma mensagem:

| O que acontecia com "parece ótimo, me liga" | Onde |
|---|---|
| DND em todos os canais + tag `nao-perturbe` | 2.9.5, nós 2-3 |
| Saída de todas as 6 réguas automáticas | 2.9.5, nó 5 |
| `status` da oportunidade = `lost` | 2.9.5, nó 6 |
| **Nenhuma** tarefa de sinal quente | 2.9.3, filtro espelhado |
| **Nenhum** aviso a ninguém | o único aviso estava no ramo raro do nó 6 |

O lead mais quente do dia virava o lead mais morto do CRM, em silêncio.
Nenhuma automação deste projeto desfaz DND, e nenhuma lista mostra "DND
aplicado hoje".

**Três regras:**

1. **Palavra-chave de opt-out é frase, nunca pedaço.** Antes de pôr uma na
   lista: *ela aparece dentro de alguma palavra comum do português?* `pare` →
   `pare de`/`pare com`. Saíram também `não quero mais` e `não quero receber`
   soltos, porque neste negócio é assim que o lead descreve a dor ("não quero
   mais perder cliente"). E `stop`, que em WhatsApp brasileiro não é palavra
   reservada como o TCPA faz no SMS americano — só traria falso positivo sem
   compensar nada.
2. **Ação irreversível por automação avisa sempre, não só no caminho
   estranho.** O aviso do nó 6 só existia no ramo raro; o caso comum não
   avisava ninguém. Opt-out são poucos por dia por definição, então aviso
   sempre é barato. Regra geral: se a automação faz algo que nenhuma
   automação desfaz, alguém tem que ficar sabendo no minuto.
3. **Duas listas que precisam ser iguais são uma lista com dois lugares.**
   O 2.9.5 e o filtro do 2.9.3 usam a mesma lista de frases. Isso está
   escrito nos dois lados, com "lista canônica" num e "idênticas" no outro —
   sem isso, mexer num lado reabre o bug original (os dois disparando) ou o
   inverso (opt-out que não silencia).

## Gatilho de workflow é evento, não estado: promover lead antes de publicar a régua gasta o evento no vácuo — 21/09/2026

Ao conferir o G-03 (47 leads pagos parados em `NOVO LEAD`, três opções
escritas para o dono escolher), faltava uma precondição que nenhuma das três
mencionava: a `Cadência 12x30` está **em rascunho**. O gatilho dela é
`Opportunity Stage Changed → CONECTAR` — um evento. Promover os 47 agora faz
o evento acontecer sem ninguém escutando, e **publicar a cadência depois não
inscreve quem já está na etapa**: workflow do GHL inscreve no instante do
gatilho, não varre o estado atual do pipeline.

O resultado seria pior que o problema: 47 leads fora de `NOVO LEAD` (logo
fora da lista de triagem) e fora da cadência — um limbo que nenhuma lista
mostra.

**Regra:** antes de qualquer promoção em massa de etapa, conferir se o
workflow que deveria reagir àquela etapa está **publicado**. Régua em
rascunho + movimento em massa = evento gasto. A ordem é sempre publicar,
testar com 1-2 leads, e só então mover o estoque.

Recuperação, se acontecer: `Add to Workflow` em massa pela lista de
contatos, ou tirar e recolocar a etapa para gerar evento novo (o
`Allow Re-entry` desligado da D-06 não bloqueia quem nunca entrou neste
workflow — a própria seção 2.1 do `build-wesales.md` explica por quê). Mas
as duas alternativas tocam dado de produção duas vezes.

## Número medido dentro de uma instrução é verdade com data de validade — 21/09/2026

Varredura depois de dois dias sem sessão ao vivo. A `Fase 1` do
`GUIA-MONTAGEM.md` — a página que o dono abre para clicar — mandava
**excluir 7 etapas** do `FUNIL DE VENDAS`, e justificava assim:

> "confirmado por aqui, via `opportunities_search-opportunity`: **0
> oportunidades no pipeline inteiro**, em qualquer status. Pode apagar sem
> medo de perder negócio real."

Era verdade em 18/09. Em 21/09 o pipeline tem **50 oportunidades** (47 em
`NOVO LEAD`, 3 em `NEGOCIAR`) — a Porta de Entrada ficou rodando. Seguir a
instrução hoje apagaria etapa com oportunidade dentro, que é exatamente a
regra 1 do projeto ("NUNCA exclua"). A mesma seção também mandava renomear
as etapas para os 7 nomes antigos, o que quebraria todo workflow publicado.

O documento **não estava errado quando foi escrito**, e não havia mentira
em lugar nenhum: a correção existia, na seção "Resolvido ao vivo em chat" —
oitenta linhas **depois** do passo a passo. Quem lê de cima para baixo
executa antes de chegar nela.

**Duas regras que saem daqui:**

1. **Instrução destrutiva justificada por medição precisa ser remedida na
   hora de executar.** O número envelhece sozinho e não avisa. Onde o
   documento não puder remedir, ele tem que mandar quem executa remedir.
2. **Correção vai para cima do que ela corrige, não para o fim da seção.**
   Marcar o trecho velho como histórico custa três linhas; deixar a
   correção no rodapé aposta que ninguém lê na ordem.

Aplicado: a Fase 1 ganhou um aviso de bloqueio no topo, com a contagem de
21/09 e o motivo, e o checklist "terminou certo" (que pedia 7 etapas)
ficou marcado como histórico.

## G-02, sexta confirmação do mesmo padrão: "etapa sem status" falha também em nó opcional/de baixa prioridade — 19/09/2026, sessão automática

Fechando as seções 2.13 a 2.17 (Regras de pausa, Distribuição de leads,
Monitor de Capacidade, Higiene de Número, Dashboard do Gestor) do checklist
de migração de nomes de etapa (G-02, `ROADMAP-SALES-ENGAGEMENT.md`). Achado
real só na 2.16 (Higiene de Número — Validação Automática, item **opcional**
do roadmap): o nó 2 do Ramo A (`Invalid`) comparava etapa da oportunidade
contra `Novo lead`/`Em cadência`/`Retorno agendado` (segue) vs. `Conectado`/
`Reunião agendada`/`Nutrição`/`Descartado` (não segue) — nomes que não
existem mais na tela, e a "senão" misturava etapa avançada com status de
saída, que a tabela 1.0 já trata como coisas diferentes.

**Por que registrar mais uma vez o mesmo padrão já anotado para a seção 3,
a 2.12 e a 2.11:** esta é a **sexta** vez que "o nó decide se o lead ainda
está ativo, comparando só contra etapa" se mostra insuficiente — e a
primeira vez que o item era **opcional** (2.16 é o único item de R-13 que
"fica em espera indefinida sem prejudicar o resto" se o plano não cobrir o
recurso). A prioridade baixa do item não isentou o achado: um nó pouco
usado com bug de migração ainda quebra do mesmo jeito quando alguém liga o
recurso um dia. Corrigido para `NOVO LEAD`/`CONECTAR` **e** `status é open`
(segue) vs. `AGENDAR`/`NEGOCIAR` ou `status` já `abandoned`/`lost` (não
segue) — mesma condição composta que a 2.4, a 2.10, a 2.11, a 2.12, o
Mestre de saída e a família 5.3/5.4 já usam. **Regra prática para quem
pegar as seções que ainda faltam (2.6.1, 2.7, 2.8, 2.9-2.9.4, seção 6,
listas 8.5+, seção 9, checklist da seção 10):** a pergunta "este nó decide
se o lead ainda está ativo?" vale a mesma checagem mesmo em seção marcada
como opcional, de baixa prioridade ou pouco usada — o padrão não respeita
prioridade do roadmap.

As outras quatro subseções (2.13, 2.14, 2.15, 2.17) não tinham nó ativo com
nome de etapa antigo: só uma menção solta em texto corrido na 2.13
(`Em cadência` → `CONECTAR`, sem efeito em nó nenhum) e duas referências
informais já esperadas — `Nutrição` em prosa na 2.14 (mesmo uso que a 1.2 e
a 2.12 já fazem para o status `abandoned`) e `Pré-vendas` como apelido do
pipeline na 2.17 (documentado na seção 1 desde a primeira migração). Zero
escrita no CRM nesta rodada — o item é documentação pura (tradução de nome
de etapa), não pede campo, tag ou nó novo, então não depende de
`APROVADO.md`; a subconta foi só relida para reconfirmar estado (detalhe no
fim desta entrada). Trabalho de documentação: `build-wesales.md` (seções
2.13-2.17), `GUIA-MONTAGEM.md` (checklist da Fase 1) e
`ROADMAP-SALES-ENGAGEMENT.md` (item G-02).

Subconta reconfirmada nesta execução via `locations_get-custom-fields`
(`query_model=all`)/`opportunities_get-pipelines`: 46 campos personalizados
(mesma contagem da última checagem), pipeline `FUNIL DE VENDAS` com as
mesmas 5 etapas (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`),
mesma cor e probabilidade, `dateUpdated` ainda 18/09/2026 19:56 UTC — sem
mudança desde a última rodada. As ferramentas do conector `GHL CRM`
apareceram como ferramentas **adiadas** desta sessão (carregadas por
`ToolSearch` antes do primeiro uso, não pré-carregadas na lista inicial) —
registrado aqui só porque o briefing desta rodada avisa para não concluir
"sem acesso" cedo demais: valeu a pena checar antes de assumir.

## "Construir com IA" do GHL não lê os campos personalizados da conta — hipotetiza nome de campo genérico, mesmo depois de corrigido — 19/09/2026, ao vivo em chat

Sessão ao vivo com o dono, montando o `Loop do closer — veredito
pós-reunião` (seção 5.1). Ele usou o assistente "Construir com IA" do
construtor de workflow do GHL, colando um prompt com os nomes reais dos
campos (`Reunião foi qualificada`, `Motivo da desqualificação`, `Nota de
qualificação`). **Resultado, em três tentativas seguidas, cada uma depois
de pedir correção pelo chat da própria IA:**

1. 1ª tentativa: gatilho com filtro em `Tags` (não em `Reunião foi
   qualificada`); ramo "Veredito = Sim" condicionado a um campo
   `Rescheduled` = `True`; ramo "Veredito = Parcial" usando `Opportunity
   status`; um segmento comparando `Lost reason` contra um valor vazio
   (erro "detalhes do segmento ausentes" — a própria IA deixou a
   comparação incompleta).
2. Pedido de correção pelo chat → 2ª tentativa: trocou os campos errados
   por **outros** campos errados (`score` no lugar de `Nota de
   qualificação`, `Last appointment at` no lugar de qualquer coisa
   relacionada à reunião) — não convergiu para os campos reais, só
   redistribuiu o erro.
3. O dono então editou manualmente (fora do chat de IA, direto no nó) o
   gatilho — aí sim ficou certo (`Reunião foi qualificada` / `Foi
   alterado`, mais um segundo filtro `Tags`/`Adicionado` sobrando de uma
   tentativa anterior da IA, removido). Mas o nó de condição seguinte
   (`Se 'Reunião foi qualificada' está vazio?`), apesar de ter o **nome**
   corrigido, manteve a condição de verdade **igual à da 1ª tentativa**
   (`Campo "Tags" não está em branco`) — a IA não limpa o que já colocou
   por trás de um nó só porque o rótulo mudou.

**Nenhum destes campos inventados (`Tags` neste contexto, `Rescheduled`,
`Opportunity status` como condição de veredito, `Lost reason`, `score`,
`Last appointment at`) existe no projeto.** Nenhum deles é nem parecido
com nome de campo nativo do GHL que faria sentido aqui — parecem nomes
genéricos de CRM em inglês que a IA usa como default quando não encontra
(ou não procura) o campo real da conta.

**Regra prática, generalizável, e a segunda confirmação da mesma classe de
falha (a primeira foi o Pós-ligação, `GUIA-MONTAGEM.md`, "Fase 2"/"Estado
da montagem 19/09"):** para qualquer workflow deste projeto que compare
**campo personalizado** em condição (`If/Else`, `Condition` múltiplo,
segmento de filtro), não usar "Construir com IA" do GHL, nem tentar
corrigi-lo pedindo ajuste pelo chat da própria IA — ela troca um campo
errado por outro campo errado em vez de convergir para o certo, e pode
deixar a condição de verdade desalinhada do rótulo do nó (nome certo,
lógica errada por trás). Montar manual, clicando campo por campo no editor
("Point & Edit"), é mais lento no relógio mas não gera esse retrabalho.
Vale só para nós que citam **gatilho ou fluxo simples sem condição sobre
campo personalizado** (ex.: um `Send WhatsApp` isolado) — não testado se a
IA erra também nesses casos mais simples, mas o risco é bem menor porque
não há campo pra confundir.

## A regra certa estava no portão errado: quem *limpa* também precisa conhecer todas as réguas — 19/09/2026 (conferência da rodada acima)

A rodada anterior fechou a 2.11 e generalizou bem: "qualquer nó que decida
'o lead ainda está correndo cadência?' precisa de etapa **e** `status`".
A generalização foi escrita, mas aplicada só no nó que a rodada estava
olhando. Varrendo os outros portões da mesma pergunta, sobraram três:

| Onde | O que faltava | Consequência real |
|---|---|---|
| Seção 2.4, nó 3 (portão do bloco padrão) | `status é open` | Tentativa seguinte rodando para lead já descartado, na janela entre a saída e o `Remove from Workflow` |
| Seção 2.10, nó 2 (mesmo portão na Cadência Inbound) | `status é open` | Idem, e aqui sem rede: ver a linha seguinte |
| Seção 3, nó 2 (Mestre de saída) | Remover também de `Cadência Inbound` e `Reengajamento 90 dias` | **A pior das três:** a limpeza conhecia só a `Cadência 12x30`. Um lead inbound descartado pelo portão de higiene seguia recebendo TI2 a TI5 — tarefa e mensagem — porque a régua que estava rodando não era a que a limpeza removia |

**A lição que não é sobre `status`:** o Mestre de saída estava *certo* no
nó 1 (o portão que a rodada da 2.11 citou como modelo) e *incompleto* no nó
2, escrito quando existia uma régua só. Uma peça pode ter o raciocínio
correto e a lista desatualizada — conferir o portão não conferiu a ação que
vem depois dele. Sempre que uma seção nova criar um workflow que reaproveita
o bloco padrão da 2.4, o nó 2 do Mestre de saída ganha uma linha; isso não
aparece em nenhum grep de nome de etapa.

**Checagem barata, para não depender de lembrar:** toda régua tem título de
tarefa `[CADENCIA]`. O que o Mestre de saída remove tem que ser a mesma
lista.

```
sed -n '/^## 3\. Workflow/,/^## 4\. Workflow/p' wesales/build-wesales.md \
  | grep 'Remove from Workflow'
grep -o '^## 2[.0-9]* Workflow "[^"]*"' wesales/build-wesales.md
```

A segunda lista (as réguas que existem) não pode ter nenhum workflow de
cadência que a primeira (o que o Mestre de saída remove) não tenha. Hoje as
duas fecham em três: `Cadência 12x30`, `Cadência Inbound`,
`Reengajamento 90 dias` — mais `Qualificação por IA no WhatsApp`, que só
aparece na primeira porque não é régua de cadência (seção 2.7).

**Quarta ocorrência, achada na rodada seguinte (mesma lista, outro
workflow):** o nó 3 do Pós-agendamento (seção 5) também removia de
`Cadência 12x30` e não das outras duas réguas. Efeito menor — o nó 1 move
para `NEGOCIAR` e isso aciona o Mestre de saída —, mas o nó 3 existe para
fechar a janela de segundos até a limpeza chegar, então a omissão é a
mesma. E quinta ocorrência no mesmo grep: o ramo `Não ligar` do Pós-ligação
(seção 4), que é o mais caro dos três — na janela entre o nó 4 e a limpeza
cai tarefa de ligação para quem acabou de pedir para não ser procurado.

Conclusão que vale guardar: **`Remove from Workflow` aparece em quatro
lugares deste documento, e cada um tem sua própria lista.** Quando nasce uma
régua nova, o grep é por `Remove from Workflow` em todo o arquivo, não só na
seção 3:

```
grep -n 'Remove from Workflow' wesales/build-wesales.md
```

Dos quatro, só o ramo `Número errado` (seção 4) fica de fora de propósito:
ele não tem lista, delega inteiro ao Mestre de saída, e isso está escrito no
próprio parágrafo dele.

**Superado em 21/09/2026 (F-05, peça 4 do "Como" original — `nao-perturbe`
ainda dentro de workflow ativo):** as quatro listas viraram um só nó em cada
lugar, ação nativa **Remove Workflows**, opção **All Except Current
Workflow** — pesquisado via `WebSearch`, confiança média (documentação
oficial bloqueada pelo proxy deste ambiente, confirmado por três fontes de
terceiros independentes). Ela tira o contato de toda régua ativa, existente
ou futura, sem precisar nomear nenhuma — a checagem barata acima (dois greps
comparando duas listas) não tem mais o que comparar: sobrou uma lista só
(as réguas que existem), não duas. **Cuidado ao montar:** a opção certa é
sempre `All Except Current Workflow`, nunca `All Workflows` — as quatro
peças têm nó depois na própria régua (ex.: o Mestre de saída ainda precisa
rodar os nós 4/5/6 depois da limpeza), e `All Workflows` removeria o
contato do workflow que está executando o próprio nó, cortando o resto da
execução no meio (mesmo efeito que a seção 5.4 do `build-wesales.md` já
documenta para `Remove from Workflow` cancelando um `Wait` pendente).
Detalhe nó a nó: `build-wesales.md`, seção 3 (nota "F-05, peça 4");
`IMPLEMENTACAO-WORKFLOWS.md`, W3/W4/W5/W14; retoques de tela em
`GUIA-MONTAGEM.md`. A lição acima fica pelo histórico (por que a lista
existia, por que ela vazava) — só o "como manter sincronizada" mudou.

**Onde `status` não entra, de propósito:** o nó 2 da Interceptação de Sinal
(2.9.2/2.9.3) ganhou `status não é lost`, não `status é open`. `abandoned` é
o lead em nutrição, e um clique dele no link de agendar é o único sinal que
o Reengajamento 90 dias (relógio, não sensor) nunca vê. Aplicar a regra
mecanicamente teria trocado um alarme falso por um sinal perdido — pior
troca. Registrado na seção 2.9.2 como decisão do dono, com a linha exata a
mudar se ele preferir o contrário.

Zero escrita no CRM nesta conferência (46 campos e as mesmas 5 etapas
antes e depois, por `locations_get-custom-fields` e
`opportunities_get-pipelines`).

## Migração de etapa: um portão que só olha a etapa também engana um alerta, não só o Mestre de saída — 19/09/2026

Sessão automática, mesmo cenário de sempre (R-14/F-05/F-06 esperando
volume/mensagem real). Continuei o checklist de migração de nomes de etapa
(`GUIA-MONTAGEM.md`, Fase 1) a partir de onde a rodada anterior parou e
fechei a seção 2.11 (Alerta de Speed-to-lead) do `build-wesales.md`.

A tradução mecânica (`Pré-vendas`/`Em cadência` → `FUNIL DE
VENDAS`/`CONECTAR`) era só metade do trabalho. O portão do nó 2 decide se o
alerta dispara comparando "etapa é `Em cadência`" — no plano de 7 etapas,
sair de cadência por qualquer motivo sempre movia a etapa, então bastava.
No modelo real de 5 etapas, o nó 0.0b (seção 2.3, R-13) pode descartar um
lead sem telefone (`Update Opportunity status = abandoned`/`lost`) **sem
tirá-lo de `CONECTAR`**, e isso acontece antes de qualquer tentativa
rodar — exatamente a janela que este alerta observa. Traduzindo só o nome
da etapa, o portão continuaria lendo "ainda em `CONECTAR`, `1ª tentativa
em` vazio" como sinal de atraso, e aplicaria `atraso-1a-tentativa` num lead
que já saiu de cadência, só que por `status`, não por etapa — um alarme
falso, silencioso, sem erro nenhum na tela. Corrigido acrescentando
`status é open` à condição do nó 2, a mesma composta que a seção 3 (Mestre
de saída) já usa.

**Por que isso generaliza, e por que vale procurar antes de traduzir
qualquer seção que sobrar:** esta é a **terceira** seção onde "etapa sem
status" se mostra insuficiente neste modelo (a primeira foi a seção 3, a
segunda a reentrada da 2.12) — qualquer nó que decida algo a partir de "o
lead ainda está correndo cadência?" precisa das duas condições juntas, não
só do nome da etapa. Ao pegar as seções que ainda faltam (2.13 a 2.17,
seção 5 e 5.1-5.4, seção 6, listas 8.5+, seção 9, checklist da seção 10),
vale perguntar primeiro "este nó compara contra etapa para decidir se o
lead ainda está ativo?" antes de assumir que é troca de nome — pelo
histórico das três seções já migradas, a resposta vem sendo "precisa do
`status` junto" mais vezes do que "é só o nome".

Zero escrita no CRM nesta rodada (confirmado por
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields` antes de editar: pipeline com as mesmas 5
etapas, 46 campos sem mudança). Trabalho só de documentação:
`build-wesales.md` (seção 2.11), `GUIA-MONTAGEM.md` (checklist da Fase 1)
e `ROADMAP-SALES-ENGAGEMENT.md` (item G-02).

**Achado à parte, não relacionado à seção 2.11, registrado para a próxima
rodada não redescobrir sozinha:** das 40 oportunidades, 39 seguem em
`NOVO LEAD`, mas o contato `Daniel` (`c0uQwq5EqYM0vA8SGA0W`) apareceu em
`NEGOCIAR` com a tag `limpar-tarefas`, `lastStageChangeAt` 19/09/2026
06:41 UTC — a primeira oportunidade do projeto inteiro que já saiu de
`NOVO LEAD`. Como nenhum workflow deste projeto está publicado ainda
(`GUIA-MONTAGEM.md`, Fases 3+ seguem manuais), é mais provável mão humana
na tela do que automação; não investiguei mais fundo porque é read-only e
fora do escopo desta rodada (G-02), mas fica registrado para quem pegar o
próximo item não estranhar o número mudando sem explicação.

## Migração de etapa: reentrar em `CONECTAR` sem resetar `status` engana o Mestre de saída — 19/09/2026

Sessão automática, sem os três itens do roadmap desbloqueados (R-14/F-05/F-06
seguiam todos esperando volume/mensagem real, mesmo motivo já documentado na
entrada abaixo). Em vez de encerrar sem commit, voltei para o checklist de
migração de nomes de etapa que `GUIA-MONTAGEM.md` (Fase 1) já rastreava desde
18/09/2026 com várias seções ainda `[ ]` — um `build-wesales.md` que ainda
cita `Em cadência`/`Nutrição` como se fossem etapa é o mesmo tipo de bug
silencioso que o achado de `fieldKey` (abaixo) e o R-16 já descreveram para
merge field e rótulo de opção, aqui em nome de etapa: um gatilho ou portão
que compara contra etapa que não existe nunca casa, e ninguém vê erro nenhum
na tela até notar que o workflow simplesmente não dispara. Fechei a seção
2.12 (Reengajamento 90 dias) — a maior pendência do checklist, sinalizada
como tal desde a entrada "Seção 3... 18/09/2026" abaixo.

**Achado que a tabela de tradução (seção 1.0 do `build-wesales.md`) não
previa, generalizável para o resto do checklist:** qualquer workflow que
reative uma oportunidade **de volta** para `CONECTAR` depois que ela passou
por `status = abandoned`/`lost` precisa resetar o `status` para `open`
explicitamente, no mesmo nó que muda a etapa. Motivo: o Mestre de saída
(seção 3) decide se limpa ou não pela condição composta "etapa é `CONECTAR`
**e** `status` é `open`" — ela existe justamente porque, no modelo de 5
etapas, sair de cadência nem sempre move etapa (vira só mudança de
`status`). Se um workflow de reativação mover a etapa sem tocar no
`status`, a oportunidade chega em `CONECTAR` ainda com `status = abandoned`
da rodada anterior: a condição composta fica falsa, e o Mestre de saída lê a
**chegada** como se fosse uma **saída**, disparando a limpeza (tirar de
fila, apagar tag) no exato momento em que o lead está entrando de novo na
cadência — o oposto do "no-op" que todo o desenho pressupõe para entrada.
2.12 tinha exatamente esse buraco (nó "Reentrada no funil"); corrigido
adicionando `status → open` ao mesmo nó que move a etapa. **Ao migrar
2.10, 2.13 ou qualquer outra seção que mova oportunidade de volta para
`CONECTAR`, conferir se ela também precisa desse reset** — não é
específico do Reengajamento, é uma propriedade do modelo de 5 etapas +
status que a migração de 18/09/2026 introduziu sem essa peça.

Zero escrita no CRM nesta rodada (confirmado por
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields` antes de editar: pipeline com as mesmas 5
etapas, custom fields sem mudança desde o R-16/F-04 — nenhum C-25/C-26/C-27
novo ainda, esperado, são criação manual pendente). Trabalho só de
documentação: `build-wesales.md` (seção 2.12 e a linha da seção 2.1 que
apontava para ela), `GUIA-MONTAGEM.md` (checklist da Fase 1) e
`ROADMAP-SALES-ENGAGEMENT.md` (novo item G-02, Bloco 0, registrando esta
frente de trabalho para quem só lê o roadmap).

## F-04 fechado: a exposição real não era a do enunciado do roadmap — 19/09/2026

Auditoria desta rodada (`locations_get-custom-fields`, `opportunities_get-pipelines`,
`opportunities_search-opportunity`) reconfirmou: 46 campos (sem mudança desde
o R-16), pipeline `FUNIL DE VENDAS` com as mesmas 5 etapas, **40 oportunidades,
todas `open` em `NOVO LEAD`** (nenhuma ainda promovida a `CONECTAR` — L-07
continua aberto por decisão, não por bug). Rodei também o grep de merge field
órfão (`contact\.[a-zA-Z0-9_]*` em todo `wesales/*.md` contra os `fieldKey`
reais) que o achado do `fieldKey` (abaixo) recomenda depois de qualquer
criação de campo em lote: **zero órfãos** — as correções anteriores seguram.

Com tudo isso batendo e nenhum item do roadmap literalmente aberto e
desbloqueado (R-14/F-04/F-05/F-06 eram os quatro sem `FEITO`, e os quatro
tinham motivo documentado para esperar), quase fechei a rodada sem commit.
Antes disso, reli o "Como" do F-04 com calma e achei que o motivo original
("lead em duas cadências recebe o dobro de toques") não é o risco real deste
projeto: Cadência Inbound e Cadência 12x30 já são mutuamente exclusivas por
tag no próprio gatilho (R-07), e o Reengajamento já blinda a 12x30 contra
reentrada dupla (T-13, R-08). **Quem não tem nenhum teto é a Interceptação de
Sinal (F-01, seção 2.9):** ela roda com `Allow Re-entry` ligado de propósito
("cada clique é um sinal novo") em paralelo com qualquer cadência, sem saber
quantos toques a cadência principal já gastou — um lead que clica o link ou
responde várias vezes no mesmo dia empilha tarefa + aviso ao SDR sem limite
nenhum. Esse é o achado que tornou o F-04 buildável de verdade nesta rodada,
em vez de mais uma linha "precisa de volume" — a exposição já existe hoje,
independente de volume.

**Regra prática, generalizável:** quando um item do roadmap tem um "Como" que
parece vago ou já coberto por outro mecanismo, vale reler os itens vizinhos
(aqui, F-01) antes de assumir que o item inteiro está bloqueado por falta de
dado. Às vezes o "Como" original mirou no lugar errado e o item mesmo assim
vale a pena, só que por um motivo mais específico do que o enunciado original.

Desenho escolhido, pesquisado contra o mercado antes de montar: Outreach.io
resolve "duas sequências" com **Sequence Exclusivity** — trava de
**admissão**, não de frequência (`support.outreach.io/hc/en-us/articles/
360001587093-Sequence-Exclusivity-Settings`). Não serve para o caso real
encontrado aqui (não são duas cadências ao mesmo tempo, é sinal em paralelo
por desenho). Optei por um contador `NUMERICAL` por contato, janela **móvel**
de 7 dias (soma no toque, desconta 7 dias depois — o próprio workflow agenda
o desconto via `Wait → Time Delay`), acionado por uma tag-pulso (`toque`,
T-15) que qualquer nó de toque aplica e o workflow "Contador de Toques" já
remove no primeiro nó — mesma lógica de "tag como pulso de evento" que a
Interceptação de Sinal já usa, evitando a armadilha que o R-02 documentou
(aritmética de data não funciona sobre campo `TEXT`, e não existe campo de
data com hora — um contador incremental em `NUMERICAL` não tem esse problema).
Detalhe completo: `build-wesales.md`, seção 2.19.

**Escopo explícito, não esquecimento:** o toque e o portão de teto só foram
ligados nos dois pontos de maior risco (Cadência 12x30 e as duas
Interceptações de Sinal) nesta rodada — Cadência Inbound, Reengajamento e
Recuperação de No-show reaproveitam o mesmo mecanismo sem precisar de nada
novo, só falta ligar o nó em cada uma (registrado em `build-wesales.md`,
seção 2.19, tabela "Onde o toque é emitido").

## Pesquisa que corrobora (não fecha) o `{{right_now}}` em aberto no `GUIA-MONTAGEM.md` — 19/09/2026

O `GUIA-MONTAGEM.md` tem um item não marcado, "Antes da Fase 5, resolver
`{{right_now}}`", pedindo para alguém abrir `Update Contact Field` → `Entrada
em` na tela e ver se existe uma opção de data/hora atual — a sessão ao vivo já
tinha testado isso na tela e não achou. Rodei `WebSearch` (esta rotina não tem
acesso à tela, só à API) para tentar corroborar ou refutar isso à distância,
sem conseguir fechar o item (só quem tem a tela aberta fecha), mas achei duas
peças que reforçam o achado ao vivo, confiança média (não é leitura direta do
texto oficial — `help.gohighlevel.com` e `ideas.gohighlevel.com` seguem
bloqueados pelo proxy deste ambiente, mesma limitação de sempre):

1. **"Right Now Merge Fields" existe e é documentado**, mas como parte do
   guia oficial "Merge Fields Guide for **Personalized Messages and
   Documents**" — ou seja, o caso de uso documentado é composição de
   mensagem/documento (SMS, e-mail, `{}` dentro da caixa de texto de um
   envio), não a ação de workflow `Update Contact Field` sobre um campo de
   contato.
2. Um changelog oficial (`ideas.gohighlevel.com/changelog/update-contact-
   field-action-dynamic-custom-value-picker-expanded-field-support`, achado
   só por `WebSearch`) descreve uma expansão **recente** do seletor de valor
   dinâmico da ação `Update Contact Field` para os tipos **Numeric,
   Select/Dropdown e Monetary** — não cita `Text` nem `Date`, e mesmo essa
   expansão é sobre copiar de "passos anteriores ou campos já armazenados",
   não sobre inserir um relógio ao vivo.

Nenhuma das duas fontes confirma nem nega 100% — é evidência circunstancial
de que campo `TEXT` na ação `Update Contact Field` provavelmente não expõe
"agora" como valor pronto, o que bate com o que a sessão ao vivo já viu na
tela. **Não fechei o checkbox do `GUIA-MONTAGEM.md`** porque isso exige
alguém com a tela aberta confirmando, não pesquisa à distância — deixo aqui
para quem for testar não precisar repetir a mesma busca.

## Auditoria escrita não é auditoria aplicada — 19/09/2026

`CONFERENCIA-CAMPOS.md` já existia com um levantamento completo, feito em
18-19/09, comparando a tela contra `campos-e-tags.md`: nove campos
(`Q-01, Q-04, Q-06, Q-08, Q-10, Q-12, Q-15, Q-17, Q-18`) tinham nome, opção
ou tipo diferente do que a especificação sugeria. O arquivo até dizia
literalmente, na sua própria conclusão (`GUIA-MONTAGEM.md`, seção
"Pendências que sobraram"): "a régua de qualificação... precisa ser
reescrita para usar os rótulos reais... tarefa de documentação ainda
pendente". Essa rodada leu isso, conferiu `locations_get-custom-fields` de
novo e achou os rótulos **ainda errados** em `campos-e-tags.md` e na seção
9.1 do `build-wesales.md` — o achado tinha sido catalogado, nunca aplicado.

**Por que isso importa:** a régua de nota (seção 9.1) compara texto em
`If/Else`. Rótulo sugerido que não existe mais na tela nunca casa — a
mesma classe de erro silencioso que o achado de `fieldKey` logo abaixo já
descreve para merge field, só que aqui o efeito é pior: a nota de
qualificação do lead sai errada sem nenhum erro visível, e ninguém percebe
porque o workflow não quebra, só pontua mal.

**Regra prática, generalizável:** quando um documento de auditoria lista
"ajustar o documento" como próximo passo, isso é uma tarefa em aberto, não
um problema resolvido — confira se a edição foi feita de verdade nos
arquivos de especificação antes de assumir que aparecer no arquivo de
auditoria significa que já está corrigido. Um achado escrito e um achado
corrigido são coisas diferentes, e só o segundo protege o workflow.

## Como matar a classe de erro do `fieldKey`, em vez de um por vez — 19/09/2026

O GHL **remove** a letra acentuada ao gerar o `fieldKey`, não translitera:
`anúncios` → `anncios`, `qualificação` → `qualificao`, `agência` → `agncia`,
`Tentativa nº` → `tentativa_n`. Escrever "como se lê" dá merge field em branco,
e o erro não aparece em teste nenhum: a nota sai com um pedaço faltando e
ninguém nota.

Corrigir um nó por vez não fecha o buraco — em 19/09 houve dois commits
seguidos achando o mesmo `tentativa_no` em lugares diferentes (nó 6 do Mestre
de saída, depois nó 9 do Pós-ligação), e ainda sobraram quatro chaves erradas
que nenhum dos dois pegou. **A verificação que fecha de uma vez** é comparar
tudo que o documento cita contra o que a subconta tem:

```
# o que os documentos citam
grep -rho "contact\.[a-z0-9_]*" wesales/*.md | sort -u > /tmp/usados.txt
# o que existe de verdade: os fieldKey de locations_get-custom-fields
# mais os nativos (first_name, last_name, name, phone, email, company_name)
comm -23 /tmp/usados.txt /tmp/reais.txt
```

Saída vazia = nenhum merge field órfão. Em 19/09 essa comparação achou quatro
de uma vez (`motivo_da_desqualificacao`, `n_de_no_shows`,
`nota_de_qualificacao`, `reuniao_foi_qualificada`), corrigidos no mesmo commit.
**Rode isto depois de qualquer rodada que acrescente merge field**, e depois de
criar campo novo na tela — é mais barato que descobrir pela nota vazia.

## Pesquisa de mercado que valeu a pena guardar (F-02) — 19/09/2026

Pesquisado ao especificar o horário aprendido por segmento
(`ROADMAP-SALES-ENGAGEMENT.md`, F-02; mecanismo em `build-wesales.md`,
seção 2.18): a literatura de outbound (Gong.io, HubSpot, achada por
`WebSearch`) converge em janelas **médias de mercado** — manhã tarde
(10h-11h) e fim de tarde (16h-17h) — como melhor horário de ligação, sem
segmentar por indústria do lead. **Salesloft** anuncia send-time
optimization (recurso "Rhythm") só para e-mail; a documentação de
**Outreach** fala em "segment-level analysis" para desempenho de
mensagem, não em horário de ligação aprendido por segmento. Nenhuma das
duas plataformas de prateleira citadas no enunciado do projeto aprende
horário de **ligação** por segmento a partir da conexão real da própria
base do cliente — é a lacuna que o F-02 fecha, e é o tipo de diferencial
que um concorrente não replica só olhando a tela, porque o dado é da
operação, não do produto.

**Confiança média, não confirmado na tela:** se a ação `Date/Time
Formatter` do GHL aceita um "To Format" que isola só a hora (`HH`) de um
carimbo completo — achado só por busca (`growthable.io`, `consultevo.com`,
`gohighlevele.com`); `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente para leitura direta, mesma limitação registrada desde o
R-09. A ação existe e aceita formato customizado de saída — confirmado por
três fontes convergentes —, mas o token exato para "só a hora" precisa ser
confirmado na tela antes de montar os nós 7b/7c da seção 4. Se a tela não
oferecer esse recorte, o plano B documentado na seção 2.18 é gravar
`{{right_now}}` completo (como C-14/C-18/C-19 já fazem) e o gestor lê os
dois últimos dígitos de hora na lista 8.19 — mais trabalho manual, mesmo
dado.

## A migração de pipeline vazou para fora de `build-wesales.md` — `rotina-limpar-tarefas.md` também citava as 7 etapas antigas — 19/09/2026

O checklist de migração do `GUIA-MONTAGEM.md` ("Fase 1") só rastreia seções
de `build-wesales.md`. Ao revisar coerência entre documentos antes de pegar
um item do roadmap, achei que `rotina-limpar-tarefas.md` — um prompt
**autocontido**, feito para rodar numa rotina separada sem depender desta
conversa — ainda buscava oportunidades no pipeline `"Pré-vendas"` (nome que
nunca existiu na tela; o pipeline real chama `FUNIL DE VENDAS`, reaproveitado
por decisão do dono) e mapeava prefixo de tarefa pelas 7 etapas do plano
abandonado, incluindo `Retorno agendado` como se ainda fosse etapa própria.

**Por que isso não apareceu antes:** a rotina nunca rodou de verdade contra
o pipeline real — a subconta ainda tem 0 oportunidades, então o PASSO 2 do
prompt nunca teve o que buscar. Um bug assim só aparece na primeira vez que
alguém tentar rodar a rotina com oportunidade de verdade na tela.

**Achado que generaliza para qualquer migração futura de nome de
etapa/pipeline:** o `grep` de verificação do `GUIA-MONTAGEM.md` está escopado
só a `wesales/build-wesales.md` — qualquer outro arquivo do projeto que cite
etapa por nome literal (não pela tabela de tradução 1.0) precisa do mesmo
grep rodado contra ele. Rodei `grep -rn` pelos nomes antigos em todo o
`wesales/` desta vez; os outros arquivos que aparecem (`ROADMAP-SALES-ENGAGEMENT.md`,
`APRENDIZADOS-CRM.md`, `briefing-sdr.md`, `biblioteca-mensagens.md`,
`auditoria-*.md`) usam o nome antigo só como narrativa histórica ou como
termo conceitual já coberto pela convenção da tabela 1.0 — não como valor
literal que uma chamada de API vai comparar contra a tela. Só
`rotina-limpar-tarefas.md` tinha os dois problemas ao mesmo tempo (nome de
pipeline errado E comparação literal de etapa), porque é o único documento
do projeto, fora de `build-wesales.md`, escrito para ser colado direto numa
sessão que fala com o CRM.

**Correção:** detalhe completo em `rotina-limpar-tarefas.md` (PASSO 2/3
reescritos) e `GUIA-MONTAGEM.md` (novo item marcado na lista de migração).
A régua nova também passou a checar o `status` da oportunidade, não só a
etapa — sem isso, um lead que esgotou as 12 tentativas (`status = abandoned`,
parado em `CONECTAR`) teria as tarefas `[CADENCIA]` tratadas como válidas
para sempre, porque `CONECTAR` sozinho não diferencia "ainda na régua" de
"saiu sem mudar de etapa" (a maioria das saídas de cadência no modelo de 5
etapas muda só o `status`, não a etapa — tabela 1.0, `build-wesales.md`).

## Migração das 5 etapas continuou: Seção 3 (Mestre de saída) precisava de um segundo gatilho, não só troca de nome — 18/09/2026

A tarefa de migração aberta em `GUIA-MONTAGEM.md` ("Fase 1", checklist de
seções) tratava a maioria das seções como troca de nome (`Em cadência` →
`CONECTAR` etc.). Ao migrar de verdade a seção 3 (Mestre de saída) e a seção
4 (Pós-ligação), apareceu um problema que troca de nome sozinha não resolve:
no plano de 7 etapas, **toda** saída de cadência (conectou, número errado,
não ligar, 12 tentativas esgotadas) era um movimento de etapa, e um gatilho
só de `Opportunity Stage Changed` bastava para a limpeza rodar. Na tela
real (5 etapas), só "conectou" continua sendo movimento de etapa
(`CONECTAR` → `AGENDAR`) — os outros três viraram `status` da oportunidade
(`abandoned`/`lost`) **sem sair de `CONECTAR`** (é a própria tradução já
registrada na tabela 1.0 de `build-wesales.md`, seção 1.0). Um Mestre de
saída só com `Opportunity Stage Changed` deixaria de limpar a fila para o
caminho mais comum de saída (12 tentativas esgotadas nunca move etapa) —
teria ficado tag `fila-tel`/`fila-wa` presa em quase todo lead que esgota a
régua sem conectar, sem ninguém perceber até a fila entupir.

**Pesquisado antes de corrigir, confiança alta (WebSearch, não bloqueado
pelo proxy deste ambiente):**
- **`Opportunity Status Changed` é gatilho nativo, separado de
  `Opportunity Stage Changed`/`Pipeline Stage Changed`** — dispara quando o
  `status` da oportunidade muda (`open`/`won`/`lost`/`abandoned`), com
  filtro por status de destino. Fonte:
  `help.gohighlevel.com/support/solutions/articles/155000003252-workflow-trigger-opportunity-status-changed`
  (achado só por `WebSearch`, que roda fora do proxy bloqueado; o domínio
  `help.gohighlevel.com` em si segue inacessível por `WebFetch` direto,
  mesma limitação já registrada desde o R-09).
- **Um workflow do GHL aceita mais de um gatilho, em OR** — "stack multiple
  triggers on one workflow", confirmado por várias fontes de busca
  convergentes (`growthable.io`, `howtohighlevel.com`, `tkturners.com`).
  Isso é o que permite o Mestre de saída escutar `Opportunity Stage Changed`
  **e** `Opportunity Status Changed` no mesmo workflow, sem duplicar a
  lógica de limpeza em dois lugares — regra prática, generalizável para
  qualquer item futuro que precise reagir a "duas formas diferentes de
  chegar no mesmo estado final" (ao contrário de "dois relógios correndo em
  paralelo", que aí sim pede dois workflows — achado já registrado no R-12).

**A correção, resumida:** o portão (nó 1) do Mestre de saída trocou de
"etapa de destino é `Em cadência` → encerra" para "etapa **é** `CONECTAR`
**E** `status` **é** `open` → encerra". A condição composta cobre os dois
gatilhos com uma regra só: verdadeira só quando o lead está de fato correndo
a cadência ainda (entrando ou no meio dela), falsa em qualquer saída real —
movimento de etapa ou mudança de status. Detalhe completo, com os casos
percorridos um a um (entrada, 12 esgotadas, número errado, não ligar,
atendeu, progressões seguintes): `build-wesales.md`, seção 3.

**Progresso desta rodada no checklist de migração** (detalhe em
`GUIA-MONTAGEM.md`, "Fase 1"): seção 3 (Mestre de saída) e seção 4
(Pós-ligação) migradas por completo; dentro da seção 2, as subseções 2.1
(gatilho), 2.3 (nó 0.0b) e 2.4 (nó 3) migradas, mais o fim da 2.6 (M3 → 12
tentativas esgotadas); dentro da seção 8, as listas 8.1 a 8.4. Continuam
usando o nome antigo (tradução pela tabela 1.0 até serem migradas): 2.10,
2.11, 2.12 (a maior peça que falta — o gatilho dela hoje é `Opportunity
Stage Changed → Nutrição`, que não existe mais como etapa, precisa virar
`Contact Tag Added → nutricao-90d`), 2.13 a 2.17, seção 5 e 5.1–5.4, seção
6, seção 8.5 em diante, seção 9, e o checklist de teste da seção 10.

**Reconfirmado nesta rodada:** pipeline `FUNIL DE VENDAS` continua com as
mesmas 5 etapas (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`,
mesma probabilidade e cor, `dateUpdated` ainda 18/09/2026 19:56 UTC — sem
mudança desde a última verificação) e os campos personalizados batendo com
`campos-e-tags.md` — quantos existem de fato, e onde divergem da
especificação, fica em `CONFERENCIA-CAMPOS.md`, que é quem compara os dois
lados. Nenhuma escrita no CRM nesta rodada: o trabalho foi
só migração de documento, sem campo/tag/contato novo exigido.

## Fase 2 (campos) começou fora de ordem, e 3 dos 24 campos não batem com a especificação — 18/09/2026 ~21h UTC

Rodada anterior tinha reconfirmado "0 campos, 0 contatos" ao fechar o
R-15 (mesma checagem repetida cinco vezes seguidas até ali, sempre igual).
Esta rodada, a mesma chamada (`locations_get-custom-fields`) devolveu
**24 campos**, todos com `dateAdded` entre 20:18 e 21:01 UTC de
18/09/2026 — trabalho manual de verdade na tela, não coisa desta rotina
(o conector `GHL CRM` não tem ferramenta de criar campo, ver seção
"O que o conector cria e o que não cria" abaixo).

**Regra prática, generalizável: nunca confie só na contagem depois de uma
criação em lote manual — confira nome e tipo, campo a campo, contra
`campos-e-tags.md`.** Rodei essa conferência linha a linha e achei três
divergências que a contagem batendo (24 campos ≈ ~24 esperados) teria
escondido:

1. **Dois campos da tabela não existem**: C-03 (`WA não atendidas
   seguidas`) e C-04 (`Permissão WhatsApp`) — o segundo é o campo mais
   referenciado do projeto depois de `Tentativa nº`/`Resultado da
   tentativa` (14+ pontos do `build-wesales.md`).
2. **Um campo tem o tipo errado**: C-11 (`Conexões telefone`) foi criado
   como `PHONE`, não `NUMERICAL` — quebra a ação `Math: + 1` que o
   Pós-ligação precisa fazer nele.
3. Uma opção de picklist com capitalização diferente da documentação
   (`Caixa Postal` vs. `Caixa postal`) — cosmético, não bloqueia nada.

Detalhe completo, com as fontes de pesquisa sobre "dá para editar o tipo
de um campo depois de criado" (resposta: não, só apagar e recriar) e o
checklist de correção: `GUIA-MONTAGEM.md`, seção "Fase 2 — Campos
personalizados (verificação do que já foi criado)".

**Por que isso importa além deste achado específico:** a Fase 1
(pipeline) segue travada sem confirmação há mais de uma rodada (ver
achado abaixo), e mesmo assim alguém já avançou para a Fase 2 por fora da
ordem do `GUIA-MONTAGEM.md`. Regra prática: não assumir que as fases
avançam em ordem só porque o guia sugere isso — reconferir o estado real
da subconta inteira (pipeline **e** campos) a cada rodada, não só a peça
que a rodada anterior estava tratando.

## O `FUNIL DE VENDAS` mudou de novo, e não para o desenho do projeto — 18/09/2026 ~20h UTC

Rodada anterior fechou às 19:52 UTC com o `GUIA-MONTAGEM.md` recém-criado,
ensinando a Fase 1 (editar as 14 etapas antigas para as 7 do projeto).
Esta rodada reconferiu o pipeline (`opportunities_get-pipelines`) antes de
pegar o próximo item do roadmap, como toda rodada faz — e desta vez o
resultado **mudou**: `dateUpdated` do pipeline marca 19:56 UTC, 4 minutos
depois daquele commit. Só que o que está lá agora não são as 7 etapas
pedidas: são 5 etapas novas (`NOVO LEAD`, `CONECTAR`, `AGENDAR`,
`NEGOCIAR`, `FORMALIZAR`, probabilidade redonda de 10 em 10: 30/40/50/60/
70%), nenhuma batendo em nome com `Em cadência`/`Conectado`/`Retorno
agendado`/`Reunião agendada`/`Nutrição`/`Descartado` a partir da posição
1. Detalhe completo, tabela lado a lado e as duas hipóteses (início
manual com estilo próprio vs. reaplicação de snapshot da agência):
`GUIA-MONTAGEM.md`, seção "Verificação em 18/09/2026, ~20h UTC".

**Verificado antes de reagir, não só assumido:** `opportunities_search-opportunity`
(`query_status=all`) no pipeline confirmou **0 oportunidades** — nenhum
dado de negócio foi perdido nessa troca, então não há urgência de conter
dano, só de não seguir construindo (Fase 2 em diante) em cima de nomes de
etapa que não existem na tela.

**Regra prática, generalizável para qualquer rodada futura que dependa de
nome exato de etapa de pipeline (todo gatilho `Opportunity Stage Changed`
do projeto depende disso):** não confiar que uma verificação de uma
rodada atrás continua valendo — o pipeline é a única peça deste projeto
que muda por fora da rotina (edição manual na tela, ou possivelmente
snapshot de agência) e sem aviso. Reconferir via `opportunities_get-pipelines`
a cada rodada antes de assumir que os nomes de etapa batem com
`build-wesales.md`, exatamente como já se fazia para campo/tag/contato —
a diferença é que campo/tag só cresciam (nunca regrediam), e o pipeline
acabou de mostrar que pode mudar de forma incompatível com o desenho.
Nenhum item do roadmap foi fechado nesta rodada por causa disso: builder
em cima de nome de etapa que não existe seria trabalho perdido na certa.

## "Não sai por API" tinha dois motivos diferentes — separados em 18/09/2026

Até esta rodada, o documento inteiro tratava "campo personalizado", "pipeline",
"workflow" e "calendário/formulário" como o mesmo tipo de bloqueio: "não sai
por API, só na tela". Pedido do dono ("estude a documentação oficial, blogs,
comunidades") levou a checar isso a sério, e a resposta **não é uma coisa só**.

**Método:** `highlevel.stoplight.io` e `marketplace.gohighlevel.com`
continuam bloqueados pelo proxy de rede deste ambiente (mesma limitação já
registrada para R-09/R-13). Em vez de desistir na busca, a verificação foi
direto na fonte: `github.com/GoHighLevel/highlevel-api-docs`, o repositório
público oficial que alimenta aqueles sites (README confirma: "source
documentation for the GoHighLevel API V2"). Ler o JSON OpenAPI de cada
recurso é leitura de spec, não snippet de busca — **confiança alta** nos
pontos abaixo, marcados um a um.

**Pipeline (criar) — confirmado NÃO EXISTE na API, é limitação da
plataforma.** `apps/opportunities.json` e `apps/v3/opportunities-v3.json`
só têm `GET /opportunities/pipelines`; `docs/oauth/Scopes.md` confirma que
`opportunities.write` cobre criar/mover/excluir **oportunidade**, não
pipeline. Existe uma issue aberta no próprio repo oficial pedindo isso
(`github.com/GoHighLevel/highlevel-api-docs/issues/248`, "Create Pipelines
and Stages API", sem resposta de implementação) — confirma que nem
desenvolvedores terceiros conseguem. Achado curioso, não conclusivo: existe
uma string de escopo `pipelines.create` dentro de `apps/v3/users-v3.json`
(a API de permissões de usuário), órfã — nenhum endpoint documentado a usa.
Pode ser um recurso interno ainda não exposto. **Não confie em criar
pipeline por API até essa issue fechar.**

**Workflow (criar/publicar) — confirmado NÃO EXISTE, é limitação da
plataforma.** `apps/workflows.json` só tem `GET /workflows/`. Sem POST em
nenhuma versão do spec. Existe workaround parcial (não é criar workflow):
Custom Workflow Actions/Triggers via Marketplace deixam um app aparecer
como passo dentro de um workflow que um humano monta na tela — não cria o
workflow em si.

**Formulário (criar) — confirmado NÃO EXISTE, é limitação da plataforma.**
`apps/forms.json` só tem `GET /forms/` (listar), `GET /forms/submissions`
(ler respostas) e `POST /forms/upload-custom-files` (upload de arquivo
anexado a uma resposta, não cria estrutura de formulário).

**Campo personalizado (criar) — EXISTE na API oficial. É este conector que
não implementa, não a HighLevel.** `apps/locations.json` documenta
`POST /locations/{locationId}/customFields`, escopo
`locations/customFields.write`. Corpo obrigatório: `name` + `dataType`
(TEXT, NUMERICAL, PHONE, RADIO, CHECKBOX etc.); opcional `model` (`contact`
ou `opportunity` — um endpoint só, os dois tipos de campo deste projeto) e
mais placeholder/position/opções de lista. Existe também GET/PUT/DELETE por
ID e upload para campo de arquivo. **Toda a Etapa 2 deste projeto (os ~24
campos de `campos-e-tags.md`) poderia sair por API — só não sai porque o
conector `GHL CRM` conectado nesta sessão não tem essa ferramenta.**

**Calendário (criar) — EXISTE na API oficial. Mesmo caso do campo.**
`apps/calendars.json` documenta `POST /calendars/`, escopo
`calendars.write`, corpo obrigatório `locationId`+`name`, e dezenas de
campos opcionais (`slotDuration`, `openHours`, `availabilities`,
`teamMembers`, `formId`, `eventType`, tipo de calendário, buffers,
confirmação automática). Também há `POST /calendars/groups`,
`POST /calendars/schedules`, `POST /calendars/resources/{resourceType}`.
**O calendário `Reunião com closer` (seção 7.1 do `build-wesales.md`)
poderia sair por API** — mesmo motivo do campo: o conector atual só expõe
leitura de calendário (`calendars_get-appointment-notes`,
`calendars_get-calendar-events`), não criação.

**O que fazer com isso:** fechar o gap não depende de esperar a HighLevel
lançar nada — depende de trocar/ampliar o conector. Duas rotas conhecidas,
nenhuma delas testada ainda nesta subconta: (1) o toolkit HighLevel via
**Composio**, citado desde a primeira rodada em `briefing-sdr.md` ("Estado
do acesso") como caminho alternativo — este ambiente tem ferramentas
`mcp__Composio__*` presentes, mas **nenhuma conta HighLevel conectada por
Composio ainda** (a lista de apps já conectados via Composio, vista nesta
rodada, não inclui HighLevel/GoHighLevel — só facebook, googlecalendar,
googledrive, instagram, metaads, pexels, youtube); conectar exigiria um
fluxo de OAuth que só o dono da conta pode autorizar (link clicável), então
não é algo para a rotina fazer sozinha sem perguntar antes. (2) Pedir para
quem administra o conector `GHL CRM` (fora desta rotina) adicionar as duas
ferramentas que faltam. Enquanto nenhuma das duas acontecer, campo e
calendário continuam manuais na prática, mesmo não sendo limitação da
HighLevel.

Fontes lidas direto (alta confiança), todas em 18/09/2026:
- `github.com/GoHighLevel/highlevel-api-docs` (README)
- `.../blob/main/apps/opportunities.json`, `.../apps/v3/opportunities-v3.json`
- `.../blob/main/apps/locations.json`
- `.../blob/main/apps/workflows.json`
- `.../blob/main/apps/calendars.json`
- `.../blob/main/apps/forms.json`
- `.../blob/main/docs/oauth/Scopes.md`
- `.../blob/main/apps/v3/users-v3.json`
- `github.com/GoHighLevel/highlevel-api-docs/issues/248`

Fontes só de busca (confiança média, corroboram sem serem prova primária):
`marketplace.gohighlevel.com/docs/ghl/locations/create-custom-field/`,
`.../custom-fields/custom-fields-v-2-api/`, `.../calendars/calendars/`,
`.../forms/forms-api`, `ideas.gohighlevel.com/apis/p/api-to-create-workflows`,
`ghldesk.com/gohighlevel-api/`. Uma URL vista em busca
(`highlevel.stoplight.io/.../create-pipeline`, com exemplo de código de SDK
não-oficial) **não foi verificada** — o spec oficial lido direto não tem
esse endpoint, então trata-se como não confirmado até alguém abrir a página
manualmente.

## Conector `GHL CRM` — confirmado nesta rodada (18/09/2026)

As ferramentas `mcp__GHL-CRM__*` **estavam presentes** nesta sessão. Rodei
`locations_get-custom-fields`, `contacts_get-contacts` e
`opportunities_get-pipelines` na subconta `1D53YTI9C7oIMBavcQxV` para
reconferir o estado antes de mexer no roadmap: 0 campos personalizados, 0
contatos, 1 pipeline (`FUNIL DE VENDAS`, o que já existia, não o
`Pré-vendas` do projeto). Bate exatamente com `auditoria-resultado.md` —
nada mudou na subconta desde a auditoria. Reconfirmado de novo ao fechar o
R-07 (mesma rodada, mesmo resultado), outra vez ao fechar o R-08, outra vez
ao fechar o R-09 e outra vez ao fechar o R-10: estado inalterado nas cinco
checagens.

**Primeira mudança real na subconta, 18/09/2026:** executadas as 11 tags
aprovadas em `APROVADO.md` — contato `ZZ TESTE ESTRUTURA`
(`c5r3ZxiAd8T5adL1Bt6j`) criado com as 11 tags do projeto. A partir de
agora `contacts_get-contacts` retorna 1, não 0 — não é regressão, é a
primeira escrita de verdade que a rotina fez na subconta. Campos
personalizados e pipeline `Pré-vendas` seguem em zero (só saem manual).
Reconfirmado de novo ao fechar o R-11 (mesma rodada, mesma data): 0 campos,
1 contato (o de estrutura), só o `FUNIL DE VENDAS` — nenhuma escrita nova
neste item, ele não abre campo nem tag.

**Segunda rodada de escrita, mesma data, pedido explícito do dono ao vivo
em chat ("aplique todas os estudos... CRM fique mais completo possível"):**
1. As 3 tags que ainda esperavam aprovação (T-12 `atraso-1a-tentativa`,
   T-13 `reengajamento-ativo`, T-14 `pausado`) foram aprovadas na hora
   (registrado em `APROVADO.md`) e criadas via `contacts_add-tags` no mesmo
   contato de estrutura — a subconta tem as **14 tags do projeto**,
   nenhuma faltando.
2. Os 5 contatos fictícios do checklist (seção 10, `build-wesales.md`)
   foram criados: `Teste Atendeu`, `Teste Não Atende`, `Teste Retorno`,
   `Teste Número Errado`, `Teste Não Ligar` — sem telefone (falta o número
   real do dono, ver `APROVADO.md` seção Mensagens) e sem tag/oportunidade
   (pipeline `Pré-vendas` não existe ainda). Existem como registro,
   prontos para ganhar telefone e entrar no pipeline quando a montagem
   manual acontecer.
3. **Não criado:** nenhuma oportunidade (pipeline não existe — bloqueio de
   capacidade, não de aprovação) e nenhuma mensagem (falta o telefone real).

Estado da subconta após esta rodada: 0 campos personalizados, 6 contatos
(1 de estrutura + 5 fictícios), 14 tags aplicadas ao contato de estrutura,
só o pipeline `FUNIL DE VENDAS` pré-existente. Reconfirmado de novo ao
fechar o R-12 (rodada seguinte, mesma data): estado idêntico — nenhuma
escrita nova, porque este item só abriu um campo (`Nº de no-shows`, C-24) e
nenhuma tag. Reconfirmado outra vez ao fechar o R-13 (rodada seguinte,
mesma data): estado idêntico — este item não escreve no CRM (reaproveita a
tag `telefone-invalido` já existente e o campo nativo `Phone`, zero campo e
zero tag novos), então não havia nada para criar. Reconfirmado mais uma vez
ao fechar o R-15 (rodada seguinte, mesma data): estado idêntico — dashboard
e Custom Metrics não saem por API, e o item reaproveita C-09 a C-12 (R-01)
e `atraso-1a-tentativa` (T-12), zero campo e zero tag novos de novo.

## Pesquisa externa que valeu a pena guardar (R-13)

**Number Validation é um recurso nativo de conta do GHL**, não uma
integração de terceiro montada por fora: Configurações → Telefone expõe um
toggle (agência, depois subconta) que liga uma checagem de
operadora/formato/alcançabilidade por número, cobrada por checagem
(referências de mercado citam a Veriphone como provedor por trás e um
custo de ordem de US$0,005/validação — não confirmado na tela da WeSales, e
o plano/trial da subconta pode nem expor o recurso, mesma cautela já
registrada para o Custom Metrics do R-11). Uma vez ligado, existe um
gatilho de workflow próprio, **Number Validation**, que dispara com o
resultado da checagem (`Valid`/`Invalid`/`Landline` são os nomes vistos na
busca) — dá para reagir automaticamente sem precisar que o SDR discar
primeiro. **Nível de confiança médio:** só achado por busca
(`consultevo.com`, `growthable.io`, `gohighlevele.com`) — `help.gohighlevel.com`
segue bloqueado pelo proxy deste ambiente, mesma limitação já registrada
para R-09 a R-12 —, então os nomes exatos dos status e a disponibilidade
por plano **precisam ser confirmados na tela** antes de montar o workflow
da seção 2.16. Registrado como item opcional/dispensável no `build-wesales.md`
de propósito: a parte estrutural do R-13 (contato sem telefone nenhum)
resolve só com `If/Else` nativo sobre o campo `Phone`, sem depender deste
recurso pago nem da confirmação acima.

**Achado que gerou a mudança de desenho mais importante deste item:** o
portão por tentativa (nó 3, seção 2.4) já bloqueava telefone quando
`telefone-invalido` está presente, mas nunca bloqueou WhatsApp por essa
tag — porque o desenho original assumia que a tag só nascia depois de o
SDR confirmar "número errado" numa ligação de verdade (ramo da seção 4),
quando o lead já estava saindo de cadência de qualquer jeito. Ao desenhar
uma verificação **proativa** (antes de qualquer tentativa), reaproveitar
só o portão do nó 3 teria deixado a T1 inteira (mensagem + telefone +
WhatsApp) disparar para um contato sem telefone nenhum, porque WhatsApp
neste projeto também depende do número de telefone do contato
(`briefing-sdr.md`, "A máquina") — não é um canal independente. Regra
prática, generalizável para qualquer verificação futura que precise
travar **antes** da primeira ação de um workflow: um portão dentro do
bloco padrão de tentativa (nó 3) é tarde demais para isso — a verificação
proativa precisa ser um nó novo na inicialização (nó 0), não uma condição
a mais dentro de um portão que já existe para outro propósito (bloquear
canal por canal, tentativa por tentativa).

## `contacts_get-contacts` (lista) atrasa em relação à escrita — não confie nele logo após criar em lote

Descoberto ao criar os 5 contatos fictícios em sequência, 18/09/2026: cada
`contacts_create-contact` respondeu 201 com o contato completo, e
`contacts_get-contact` por ID confirmou cada um individualmente logo em
seguida — mas `contacts_get-contacts` (a lista, que a própria descrição da
ferramenta já marca como **deprecated** em favor de "search contacts")
continuou devolvendo só 1 contato (o mais antigo) por um tempo depois das 5
criações nas duas chamadas seguintes. Não é perda de dado: é o índice de
busca por trás da listagem ficando para trás da escrita (latência de
indexação), não o registro em si. Regra prática, generalizável: depois de
criar ou marcar vários contatos na mesma rodada, **verifique cada um pelo
ID retornado na criação** (`contacts_get-contact`), não pela contagem da
lista — a lista pode subcontar por um tempo mesmo com a escrita já
confirmada.

## `contacts_create-contact` exige nome ou identificador — `name` sozinho não basta

Descoberto ao criar o contato de estrutura das 11 tags, 18/09/2026: chamar
`contacts_create-contact` só com `body_name` (sem `firstName`/`lastName`
nem `email`/`phone`) devolve erro 422 — "Contacts without email, phone,
firstName and lastName are not allowed". `body_name` sozinho não conta como
identificador para essa regra, mesmo aparecendo depois no contato criado.
Passar `body_firstName`/`body_lastName` (pode ser texto livre, não precisa
ser um nome "de verdade" — usei `"ZZ TESTE"` e `"ESTRUTURA"`) resolve sem
precisar de e-mail nem telefone fake. Regra prática, generalizável: todo
contato de estrutura ou fictício criado por API neste projeto (a ordem
sugerida das 5 fictícias da seção 10, qualquer outro que surgir) precisa de
`firstName`+`lastName` (ou e-mail/telefone) no corpo da chamada — `name`
como único campo de identificação falha sempre. `contacts_create-contact`
aceita `tags` direto no corpo da criação — não precisa de uma segunda
chamada a `contacts_add-tags` quando o contato já nasce com as tags certas.

## `Allow Re-entry` bloqueia por workflow, não por evento — mesmo via `Add to Workflow`

Pesquisado ao fechar o R-08 (reengajamento dos 90 dias), 18/09/2026, porque
o primeiro desenho cogitado (devolver o lead reativado direto para a
Cadência 12x30) esbarrava nisso sem eu ter percebido de início. `Allow
Re-entry` desligado bloqueia um contato que **já passou por aquele
workflow específico** de entrar de novo nele — para sempre, não só "no
mesmo dia" ou "na mesma sessão do gatilho". A entrada `Add to Workflow`
não reavalia o filtro do gatilho de destino (já registrado acima, no
fechamento do R-07), **mas continua respeitando `Allow Re-entry`** — as
duas coisas são independentes, e é fácil ler a primeira e assumir que ela
cobre a segunda. Na prática: se um workflow tem `Allow Re-entry` desligado
por um motivo legítimo (aqui, D-06 em `briefing-sdr.md` — evitar tentativa
duplicada), **nenhum caminho nativo** (gatilho de novo, `Add to Workflow`,
reentrada manual) devolve um contato que já passou por ele uma vez. Regra
prática para qualquer item futuro que precise reciclar um lead por um
workflow que ele já visitou: não tente reaproveitar aquele workflow — crie
um novo, mesmo que pequeno, com sua própria configuração de reentrada.
Foi a saída usada no R-08 (workflow `Reengajamento 90 dias`, isolado da
Cadência 12x30).

## `Add to Workflow` não reavalia o filtro do gatilho de destino

Pesquisado ao fechar o R-07 (cadência inbound), 18/09/2026, porque o desenho
inteiro do handoff (seção 2.10 do `build-wesales.md`) depende disso. A
documentação oficial da HighLevel confirma: a ação **Add to Workflow**
insere o contato direto na sequência de ações do workflow de destino, **sem
reavaliar o filtro do gatilho** daquele workflow — o filtro só vale para a
entrada automática pelo próprio gatilho. Isso é o que permite um workflow
com filtro de tag "X ausente" (a Cadência 12x30, filtrando `cad-inbound`
ausente) receber de volta, por `Add to Workflow`, um contato que **tem** a
tag X — sem precisar remover a tag antes. É o mesmo mecanismo, sem essa
observação registrada antes, que a Qualificação por IA (seção 2.7) já usava
silenciosamente desde a primeira rodada.

**Cuidado que a mesma busca trouxe e que não se aplica aqui, mas vale**
**registrar para não confundir depois:** "Allow Re-entry" do workflow de
destino segue valendo — `Add to Workflow` não ignora essa configuração, só
o filtro do gatilho. Se o contato já tivesse passado por aquele workflow
antes (não é o caso do handoff do R-07: é a primeira entrada dele na
Cadência 12x30), `Allow Re-entry` desligado bloquearia a nova entrada.

## Pesquisa de mercado que valeu a pena guardar (R-07)

Meetime documenta que a taxa de ligação conectada bate 64% (o teto da
métrica) quando o retorno ao lead inbound sai em até 10 minutos, e
recomenda SLA de até 5 minutos para lead inbound direto — meta que a
literatura de speed-to-lead (benchmarks citando Velocify/InsideSales) reforça
com "conversão até 21x maior respondendo nos primeiros 5 minutos" contra
responder depois de 30. Confirmado também: Outreach e Salesloft são
desenhados para cadência **outbound** — nenhum dos dois tem, nativamente,
uma régua em minutos para lead entrante. Isso valida os degraus do roadmap
(5 min a 3 dias) como alinhados ao que a categoria trata como piso de
excelência, não como número arbitrário — e mostra que fechar isso com
workflow nativo do GHL, sem software de terceiro, é genuinamente competir na
faixa que as duas plataformas de prateleira do enunciado deixam de fora.

Se numa execução futura o conector **não** estiver na sessão, o problema
provável é o mesmo já resolvido antes (ver `rotina-horaria.md`): a rotina
precisa nascer com `GHL-CRM` anexado. Não é falta de acesso à subconta — é
falta do conector na sessão. Registre e siga com o item de backlog que não
depende do CRM, como a instrução manda.

- **Pesquisado ao fechar o R-15 (dashboard do gestor), 18/09/2026:** dois
  achados que mudam o alcance de qualquer item futuro que precise de tela
  agregada. **Custom Metrics aceita `Sum`/`Min`/`Max`/`Average` sobre campo
  `NUMERICAL`/`MONETARY`**, não só "contagem de contatos com tag" (o único
  uso que o R-11 tinha mapeado) — o Formula Editor mostra a agregação como
  opção assim que o campo existe, sem configuração extra. Isso é o que
  deixou os contadores do R-01 (`Tentativas telefone`, `Conexões telefone`
  etc., C-09 a C-12) virarem métrica de dashboard sem campo novo — regra
  prática, generalizável: qualquer contador numérico já existente no
  projeto pode virar Custom Metric por soma, sem precisar duplicar o dado
  em outro lugar. **Confirmado por ausência, não testado na tela:** Smart
  List **não** pode ser adicionada como widget de Dashboard — é pedido em
  aberto na base de ideias pública da HighLevel ("Add option to put smart
  lists on dashboards", sem previsão). Regra prática, generalizável para
  qualquer item futuro que precise "mostrar uma lista filtrada numa tela
  de gestor": o dashboard nunca substitui a lista, só aponta para ela (link
  ou nota, como o Monitor de Capacidade do R-11 já fazia) — não vale tempo
  tentando encontrar o widget certo para embutir uma Smart List, porque
  ele não existe. **Nível de confiança médio nos dois:** vieram de busca
  (`ghlexperts.com`, `consultevo.com`, changelog e base de ideias da
  HighLevel), não de teste na tela — `help.gohighlevel.com` segue
  bloqueado pelo proxy deste ambiente para leitura direta, mesma limitação
  registrada desde o R-09; confirme os nomes exatos dos widgets
  ("Appointment Report", "Opportunities", "Tasks") antes de montar a seção
  2.17 do `build-wesales.md`.

## O que o conector cria e o que não cria (reconfirmado)

Sem mudança desde `auditoria-resultado.md`: 36 ferramentas, cria tag (via
`contacts_add-tags`), contato, atualiza oportunidade, lê tarefas, manda
mensagem. **Não cria** campo personalizado, pipeline, workflow, calendário,
formulário, trigger link. Etapas 2/3 (parte de campo) e a montagem de
`build-wesales.md` inteira continuam manuais por natureza da API, não por
limitação do conector.

## Pesquisa externa que valeu a pena guardar

- **`Trigger Link Clicked`** é gatilho nativo de workflow no GHL (Marketing →
  Trigger Links → criar link → usar como gatilho ou inserir via `{}` →
  Custom Values → Trigger Links dentro de uma mensagem). Não precisa de
  landing page nova: qualquer URL, incluindo a de um calendário já existente,
  vira um link rastreável.
- **`Customer Replied`** é gatilho nativo de workflow (não só um tipo de nó
  `Wait`), com filtro por canal (SMS, WhatsApp, e-mail) e por frase. Serve
  para reagir a uma resposta **sem** depender do fluxo em que ela chegou —
  é o que fecha a lacuna F-01 do roadmap sem inventar nada fora do GHL.
- **RESPONDIDO em 18/09/2026:** campo `DATE` do GHL guarda **só a data**. A
  hora é descartada mesmo quando se envia um ISO completo pela API, e não
  existe tipo DateTime para campo de contato — é pedido aberto na base de
  ideias da HighLevel há tempo. Não adianta tentar por outro caminho de
  escrita: o corte é no tipo do campo.

  **Consequência, e ela é grande:** três itens dependiam disso sem saber.
  `Data do sinal` (C-14) perde a hora do clique; `Data do retorno` (S-01)
  perde a hora do retorno combinado; e o **R-02 (speed-to-lead) não fecha**
  com dois campos `DATE`, porque a métrica é em minutos e a diferença entre
  duas datas sem hora é zero no mesmo dia.

  **Saída:** guardar carimbo de tempo em campo `TEXT`, no formato
  `AAAA-MM-DD HH:MM`, e manter o `DATE` só quando a granularidade de dia
  bastar (filtro de lista, vencimento de tarefa). Onde a hora importa, TEXT.
  A ação premium `Date/Time Formatter` do workflow monta a string.

  **Consequência de segunda ordem, descoberta ao fechar o R-02:** um campo
  `TEXT` guardando carimbo de tempo resolve a escrita, mas quebra a leitura —
  lista inteligente não faz aritmética de data sobre campo `TEXT` ("mais de
  1h atrás" não é filtro disponível). Filtro relativo de data só existe para
  campo `DATE`, que é exatamente o tipo que a gente evitou por perder a hora.
  Não tem os dois ao mesmo tempo: hora certa e filtro relativo nativo.

  **Saída, generalizável para qualquer SLA em minutos/horas daqui pra
  frente:** não filtrar — **marcar**. Um workflow curto (`Wait → Time Delay`
  do tamanho do SLA, depois `If/Else` checando se o carimbo ainda está vazio)
  aplica uma tag quando o prazo estoura. A lista inteligente filtra a tag, não
  a data — zero aritmética, funciona com campo `TEXT`. É o desenho do
  `Alerta de Speed-to-lead` (`build-wesales.md`, seção 2.11): o relógio mora
  no workflow, a lista só lê a marca.

- **Pesquisado ao fechar o R-03 (funil por período), 18/09/2026:** o GHL tem
  filtro nativo `Last Stage Change Date` em oportunidades, com opção relativa
  "This Month" — parece resolver "quantos conectaram este mês" sem campo
  novo. **Não usar para funil histórico:** ele só reflete a **etapa atual**.
  Assim que a oportunidade avança (ex.: de `Conectado` para `Reunião
  agendada`), o dado de quando ela passou pela etapa anterior desaparece do
  filtro — o funil do mês subcontaria todo mundo que já avançou. Carimbo
  próprio por marco (campo `DATE`, um por evento) não tem esse defeito: grava
  uma vez e não muda com o avanço de etapa. Confirmado também: filtro
  relativo "neste mês"/"in month" já existe nativamente para campo `DATE`
  (não só para os campos padrão de data), então C-20/C-21/C-22 (`Data
  conectado`/`Data agendado`/`Data compareceu`) não precisam do truque de
  tag-alarme do R-02 — `DATE` filtra por mês direto, o truque de tag só era
  necessário porque C-14/C-18/C-19 são `TEXT` (por precisarem da hora, que
  `DATE` descarta). Regra prática: granularidade de **dia** e filtro
  relativo → `DATE` direto; granularidade de **minuto** → `TEXT` + tag.
  Para "quantos entraram este mês", nem carimbo novo: `Data de criação` da
  oportunidade já é nativa e imutável (não muda com o avanço de etapa, pelo
  mesmo motivo que `Last Stage Change Date` muda).

- **Pesquisado ao fechar o R-09 (regras de pausa), 18/09/2026:** a janela de
  envio (Send Window) de um workflow do GHL **não** tem exceção de data —
  é só dia-da-semana + horário, sem calendário de feriado embutido (é pedido
  em aberto na base de ideias pública da HighLevel, "Automation - Time
  Window - turn off messaging during holidays", sem previsão). Regra
  prática: não tente simular feriado dentro da janela de envio de um nó de
  espera.

  **O que resolve isso de verdade:** um recurso de **conta**, separado de
  qualquer workflow — Automação → Configurações → Global Workflow Settings
  → **Pause Workflow** ("Pausar Workflows em Datas Específicas"). Você
  escolhe um intervalo de datas e marca quais workflows **publicados**
  pausam nele (só lista publicados — monte isso por último, depois de
  publicar o que vai pausar). Confirmado: até 15 intervalos cadastrados,
  cada um com no máximo 15 dias entre início e fim, e uma opção `Annually`
  que repete o mesmo intervalo todo ano sem precisar recadastrar — perfeita
  para feriado de data fixa (Natal, Tiradentes etc.), não serve para feriado
  móvel (Carnaval, Páscoa), que precisa de recadastro manual anual.

  **O detalhe que decide se isso presta para "não gerar tarefa no feriado":**
  a documentação da HighLevel (achada via busca, não lida direto — ver nota
  de acesso abaixo) descreve que a pausa não segura só quem entra pelo
  gatilho durante o intervalo: um contato que já estava dentro do workflow,
  parado num nó de espera, **segue esperando normalmente**, mas a próxima
  ação de verdade (enviar e-mail é o exemplo citado; a mesma lógica deve
  valer para criar tarefa e mandar WhatsApp, que são o mesmo tipo de "ação"
  no motor de workflow) que ele encontrar enquanto a pausa está ativa fica
  represada até o intervalo acabar — Wait e If/Else não seguram, só a ação
  seguinte a eles. Isso é o que faria o recurso cobrir quem já está no meio
  de uma cadência de 30 dias, não só quem entra novo; sem isso, pausar só a
  entrada deixaria passar a maioria das ~120 tarefas/dia (a maior parte da
  fila em regime está em tentativa 3+, não na T1). **Nível de confiança:**
  alto, mas não é leitura direta do texto oficial — `help.gohighlevel.com`
  e os demais domínios de suporte da HighLevel estão bloqueados pelo proxy
  de rede deste ambiente (`WebFetch` retorna `EGRESS_BLOCKED` em todos os
  espelhos testados: `help.gohighlevel.com`, `help.leadconnectorhq.com`,
  `ideas.gohighlevel.com`, `actionera.freshdesk.com`, `consultevo.com`); só
  `WebSearch` (que roda em infraestrutura própria, fora deste proxy) trouxe
  o conteúdo, em resumo. Antes de confiar 100% nisso para uma operação de
  volume real, vale testar na prática com um contato de teste parado numa
  tentativa e uma pausa de calendário curta. Generalizável: para qualquer
  necessidade futura de "não toque em ninguém por um período"
  (calendário-wide), este recurso de conta é o caminho certo a pesquisar
  primeiro — reserve tag customizada só para pausa **individual** (um lead
  específico), que é o que o recurso de conta não cobre.

- **Pesquisado ao fechar o R-05 (teste A/B da abertura), 18/09/2026:** o GHL
  tem ação nativa de workflow **Split**, que sorteia contatos entre até 5
  caminhos por percentual configurável e **mantém o contato no mesmo
  caminho** se ele passar pela mesma ação de novo (não sorteia de novo a
  cada reentrada). É melhor que um If/Else alternando por paridade de
  campo/ID para qualquer teste A/B futuro no projeto: alternância por ordem
  correlaciona a variante com o horário/dia de entrada do lead (viés), e
  sorteio aleatório não. **Detalhe que custa caro se ignorado:** o Split não
  rejunta os caminhos sozinho — cada caminho precisa ser conectado
  manualmente ao mesmo próximo nó se a intenção é convergir de volta ao
  fluxo principal (como em `build-wesales.md`, seção 2.6.1, onde os dois
  caminhos de M1 precisam apontar para o mesmo Wait → Contact Replied).
  Regra prática, generalizável: qualquer item futuro do roadmap que precise
  dividir tráfego por percentual (não por condição) usa Split, não If/Else.

- **Pesquisado ao fechar o R-10 (distribuição de leads), 18/09/2026:** o GHL
  tem ação nativa de workflow **Assign to User** com quatro modos —
  `Contact Owner` (mantém quem já é dono), `Selected User` (fixo),
  `Any User` (qualquer usuário elegível) e `Round Robin` (roda entre os
  escolhidos). Resolve "round robin de lead" sem workflow customizado.
  **Nível de confiança: médio-alto** — veio só de busca, os domínios de
  suporte da HighLevel continuam bloqueados neste ambiente (mesma limitação
  já registrada para o R-09); não testado numa subconta com 2+ usuários
  porque esta só tem o dono. Verificar de verdade é o item 28 do checklist
  da seção 10 de `build-wesales.md`, na primeira vez que houver um segundo
  usuário na subconta.

  **Achado que muda o desenho de qualquer lista "por usuário logado"
  daqui pra frente:** Smart Lists de contato no GHL **não** têm filtro
  dinâmico "Atribuído a = usuário atual" — é pedido em aberto no fórum de
  ideias da própria HighLevel (`ideas.gohighlevel.com`, mais de uma thread
  pedindo isso), sem previsão. O filtro "Atribuído a" só aceita um usuário
  fixo escolhido na hora de montar a lista. Regra prática, generalizável:
  qualquer lista futura que precise "mostrar só o que é meu" para cada
  membro do time precisa de **uma cópia da lista por pessoa**, com o nome
  dela fixado no filtro — não existe lista única que se adapte sozinha a
  quem está logado. É trabalho manual que se repete a cada contratação, não
  uma vez só; documentado como procedimento em `build-wesales.md`, seção
  2.14, em vez de lista já criada, porque com 1 usuário não há o que
  filtrar ainda.

  **Não confirmado, registrar quando testar:** se a ação `Add Task` aceita
  `Contact Owner` como destino dinâmico do campo "Atribuir a" (o desenho do
  R-10 depende disso para que toda tarefa de uma cadência de 30 dias siga
  o mesmo dono sem precisar sortear de novo a cada tentativa). Se a tela
  não oferecer essa opção, o caminho alternativo mais provável é o botão de
  valor personalizado (`{}`) ao lado do campo, inserindo o merge field do
  usuário atribuído do contato — não confirmado por falta de subconta com
  2+ usuários para testar. Não criar um segundo mecanismo de round robin
  dentro do `Add Task` como alternativa: isso sorteia por tarefa em vez de
  por lead, o oposto do que o R-10 decidiu de propósito (ver "A decisão que
  separa isto de uma cópia de tela", seção 2.14).

- **Pesquisado ao fechar o R-12 (handoff e no-show), 18/09/2026:** o GHL tem
  gatilho nativo `Appointment Status` com status `No Show`, mesma família do
  `Showed` já usado no R-03 — confirmado por busca (`consultevo.com`,
  `help.gohighlevel.com` segue bloqueado pelo proxy deste ambiente, mesma
  limitação já registrada para R-09/R-10/R-11) e coerente com a estrutura do
  calendário `Reunião com closer` já montada. Outreach e Salesloft resolvem
  recuperação de no-show via integração com ferramenta de agendamento de
  terceiro (Chili Piper é o exemplo mais citado) — nenhum dos dois tem
  automação nativa de no-show sozinho, o mesmo padrão de "precisa de
  parceiro externo" já visto no R-07 para inbound em minutos. A literatura
  de operação de vendas (Zapier, AskElephant, blogs de RevOps) converge em
  dois pontos: mensagem automática de "sentimos sua falta" imediata, e
  escalar para contato pessoal de um closer/AE em até 1 hora útil quando o
  lead vale a pena — nenhuma fonte encontrada trata **no-show repetido**
  como gatilho de decisão automática (descarte), só como métrica de
  relatório. É a lacuna que a regra "2º no-show seguido descarta sozinho"
  do R-12 fecha, e é o tipo de coisa que só aparece lendo o workflow, não
  olhando a tela.

  **Reaproveitando a lição do R-08 sem repetir o preço dela:** o R-08
  (reengajamento) só descobriu o problema do `Allow Re-entry` desligado da
  Cadência 12x30 (D-06) depois de cogitar reentrar por ela — teve que
  resolver com tag de blindagem e troca de origem. O R-12 aplicou a lição
  **antes** de desenhar: em vez de devolver o lead no-show para `Em
  cadência`, a régua de recuperação roda com a oportunidade parada em
  `Reunião agendada` o tempo todo. Resultado: zero tag nova precisou nascer
  para este item (usa só um campo `NUMERICAL` novo, `Nº de no-shows`) e zero
  risco de bater no mesmo `Allow Re-entry`. Regra prática, generalizável:
  antes de desenhar qualquer recuperação futura que aconteça **dentro** de
  uma etapa que já tem um workflow com `Allow Re-entry` desligado, pergunte
  primeiro se dá para resolver **sem sair daquela etapa** — nem toda
  recuperação precisa voltar o lead para o começo do funil.

  **Sobre rodar dois relógios ao mesmo tempo no mesmo gatilho:** o motor de
  workflow do GHL não bifurca um nó em dois caminhos que continuam em
  paralelo — `If/Else` e `Split` escolhem sempre **um só** caminho por
  contato. Para o R-12 precisar de duas coisas simultâneas e independentes
  (a régua de recuperação do SDR e o relógio de SLA do closer, cada uma com
  seu próprio tempo de espera), a saída nativa é a mesma já usada pela
  seção 5/5.1/5.2 deste projeto: dois workflows curtos escutando o mesmo
  evento, não um workflow tentando fazer as duas coisas. Regra prática,
  generalizável: **"preciso de dois relógios correndo ao mesmo tempo para o
  mesmo contato" é sinal de dois workflows, nunca de um workflow com dois
  ramos** — ramos de `If/Else` são exclusivos, não paralelos.

- **Pesquisado ao fechar o R-11 (alerta de capacidade), 18/09/2026 — o achado
  mais importante para qualquer alerta de agregado futuro:** o motor de
  workflow do GHL **não tem** nenhuma ação nem condição que leia "quantos
  contatos passam por este filtro/lista agora" — todo nó de workflow executa
  no escopo de **um** contato, o mesmo em contexto desde o gatilho. Confirmado
  por ausência, não por documentação direta (os domínios de suporte da
  HighLevel continuam bloqueados neste ambiente, mesma limitação já registrada
  para R-09/R-10): a própria base de ideias pública da HighLevel tem o pedido
  "trazer métricas do dashboard como custom value" em aberto, sem previsão —
  se essa ponte não existe, também não existe um "If/Else" nativo comparando
  a contagem de uma Smart List contra um número. **Regra prática,
  generalizável para F-04 (teto de toques por semana) e F-05 (monitor de
  saúde), que vão bater na mesma parede:** nenhum dos dois consegue nascer
  como "workflow que conta e decide" — F-04 se resolve por contador por
  **contato** (campo `Toques na semana`, incrementado e checado no escopo de
  cada lead, sem agregado — esse sim é nativo e comum no projeto, ex.: `WA
  não atendidas seguidas`); F-05 (que por definição precisa comparar
  contagens entre contatos, ex. "quantos estão há mais de 24h em `fila-tel`")
  não tem solução dentro de um único workflow — a saída é o mesmo padrão do
  R-11: uma Smart List que já faz o filtro certo (o cálculo mora no filtro,
  não num contador) mais um **Custom Metric** e/ou um aviso agendado, nunca
  um workflow tentando comparar quantidades.

  **Duas peças novas descobertas nesta busca, primeira vez que aparecem no
  projeto:**
  - **Gatilho de workflow `Scheduler`** — contactless (roda sem contato em
    contexto, ao contrário de todo outro gatilho já usado no projeto),
    dispara por relógio (diário/semanal/mensal/intervalo), respeita fuso e
    pode pular fim de semana. **Não pode dividir o workflow com outro tipo de
    gatilho** — é o único caso do projeto até agora em que uma nova
    automação precisa nascer como workflow próprio por essa razão, e não por
    `Allow Re-entry` (a razão que já apareceu no R-08). Ações compatíveis
    citadas na documentação: webhook, integrações (Slack, Asana, Airtable,
    Google Sheets), e-mail/SMS interno para a equipe, atualização de custom
    value, criação de tarefa — nenhuma delas lê contagem de contato. Serve
    para qualquer aviso ou rotina que precise rodar "todo dia às X", sem
    depender de um contato específico entrar em algum lugar.
  - **Custom Metrics (Reporting → Custom Metrics)** — fórmula combinando até
    4 métricas com operadores matemáticos e constantes; uma das métricas
    disponíveis é "Contagem de contatos com Tag" (aceita OR/AND entre tags,
    igual ao filtro de Smart List). É o único lugar nativo onde dá para
    transformar uma contagem em "contagem menos a meta", plantando o alarme
    dentro do número em vez de deixar o gestor comparar contra a meta de
    cabeça. **Atenção:** encontrado como disponível "a partir de planos
    $497+" — não confirmado se a subconta/plano da WeSales inclui; qualquer
    item que dependa disso precisa checar isso na tela antes de montar, e
    tem que sobreviver sem o recurso se ele não existir (a Smart List sozinha
    sempre existe, independente de plano).

## WhatsApp Business API recusa texto livre fora da janela de 24h — toda mensagem automática do projeto precisava desse portão e nenhuma tinha — G-05, 21/09/2026, sessão automática

Seguindo a própria instrução do roadmap (reler coerência, reler premissa
técnica represada e só então procurar lacuna nova antes de encerrar sem
commit): sweep de coerência limpo de novo (zero nome de etapa órfão, zero
merge field órfão), `opportunities_search-opportunity`/
`locations_get-custom-fields` sem mudança desde a última rodada (46 campos,
50 oportunidades, G-03/G-04 ainda aguardando o dono) — nada para corrigir
nem para desbloquear por volume. A lacuna nova veio de uma pergunta que
nenhuma rodada tinha feito ainda sobre um assunto que todo o projeto trata
como resolvido: "o texto livre de `Send WhatsApp` sempre funciona?"

**Não funciona.** `WebSearch` (documentação da HighLevel e da própria Meta,
domínios bloqueados pelo proxy deste ambiente, achado por citação de página
oficial repetida em buscas com termos diferentes — mesmo padrão de confiança
já usado para o `Wait Dynamic` do F-05): o WhatsApp Business API só aceita
mensagem de texto livre quando o contato está dentro da **janela de
atendimento de 24h**, que abre quando o **cliente** manda mensagem primeiro
(nunca quando a empresa inicia o contato) e fecha 24h depois do último toque
dele. Fora da janela, só um **Template** pré-aprovado pela Meta pode ser
enviado — texto livre é recusado. O GHL expõe duas ações nativas para isso,
nunca citadas em nenhum documento do projeto até esta rodada:
`WhatsApp: Customer Service Window Check` (confere a janela) e `Send
WhatsApp` com modo **Template** (funciona dentro e fora da janela).

**Por que isso passou despercebido em três rodadas de auditoria de dados e
sete de migração de nome de etapa:** nenhum lead desta base jamais escreveu
no WhatsApp da subconta (confirmado várias vezes por
`conversations_search-conversation` — zero mensagem de cadência enviada até
hoje, R-14 segue bloqueada por isso mesmo). Sem tráfego de saída ainda, não
existe rastro de recusa para uma auditoria de dados achar — é o tipo de
lacuna que só aparece **antes** do primeiro envio real, numa leitura de
especificação contra a regra da plataforma, não numa leitura de campo
gravado. As nove entradas anteriores deste arquivo sobre "auditoria de
dados acha o que o texto não acha" pressupunham tráfego rodando; aqui é o
oposto — o texto precisava ser lido contra uma regra externa (a política do
WhatsApp Business API), não contra os dados da própria subconta.

**Regra prática, generalizável:** para todo canal de mensageria com regra de
plataforma própria (WhatsApp, e no futuro qualquer outro canal que o
projeto adicionar), a pergunta "o texto livre sempre funciona?" precisa ser
feita **antes** do primeiro envio real, não descoberta pela ausência de
rastro depois — o padrão "ler os dados de produção" (auditoria de dados,
entrada acima) só encontra o que já tentou e falhou; uma regra de
plataforma que ainda não foi testada nenhuma vez não deixa rastro nenhum
para achar.

**Escopo desta rodada:** guarda especificada só para os quatro envios da
Cadência 12x30 (`M1-a`/`M1-b`/`M2-v1`/`M3-v1`) — o motor principal, maior
volume esperado. Os demais pontos de envio seguem sem o mesmo tratamento
(`MI-0`/`MI-F`, `RE-1`/`RE-2`, `NS-1`/`NS-2`, confirmação e três lembretes
do Pós-agendamento), pendência explícita dentro do próprio G-05
(`ROADMAP-SALES-ENGAGEMENT.md`).
Zero campo, zero tag, zero escrita no CRM: item de especificação pura
(`build-wesales.md` seção 2.6.2 nova, `IMPLEMENTACAO-WORKFLOWS.md` nós
M1.3a/M1.3b/M2.2/M3.2, `biblioteca-mensagens.md` tabela de Templates Meta),
não depende de `APROVADO.md` — nem a guarda nem o Template saem por API; a
submissão do Template à Meta é ação do dono no Business Manager, fora deste
conector.

## Coerência de nome não é coerência de comportamento — G-13, 23/09/2026, sessão automática

Todo item numerado (G/R/F) do roadmap estava fechado ou represado por
decisão do dono; CRM reconfirmado sem mudança via API (56 campos, 56
oportunidades). Seguindo a própria instrução do roadmap para essa condição
(varredura de coerência antes de procurar lacuna nova), o `grep` por nome de
etapa de sempre não achou nada — a mesma varredura que já tinha fechado
G-02/G-12. A lacuna apareceu ao trocar a pergunta: em vez de "o nome da
etapa está atualizado em todo lugar?" (já respondida, duas vezes), "o
**comportamento** de um nó que menciona essa etapa ainda é o que está
publicado?" `build-wesales.md`, seção 4 (`Pós-ligação`, ramo `Atendeu`),
ainda dizia que a conexão movia a oportunidade para `REUNIÃO DE
DIAGNÓSTICO` — desenho de 18/09/2026. A D3 do `PLANO-MULTICANAL.md`
(22/09/2026, publicada em 23/09) mudou isso: `Atendeu` fica em `CONECTAR`,
ganha `fechar-horario`, só agenda move para lá. A seção 2.31/F-16 do mesmo
arquivo já tinha essa mudança auditada por dump ao vivo — a seção 4 nunca
leu esse achado, contradição dentro do próprio documento.

**O efeito em cascata é o que torna isso mais que um erro de texto:** um
workflow inteiro (`AGENDAR Estagnado`/W17d, F-05 peça 5, `build-wesales.md`
§2.23) tinha o gatilho vigiando um estado que a D3 tornou logicamente
impossível ("atendido, em `REUNIÃO DE DIAGNÓSTICO`, sem reunião marcada" —
agora só se entra ali **com** reunião marcada). O dono já tinha chegado à
mesma conclusão pela tela e despublicado o W17d (`PLANO-MULTICANAL.md`, E8)
**antes** de qualquer documento registrar o motivo — quem tivesse lido só a
especificação teria remontado um workflow que o próprio dono já tinha
desligado de propósito. O G-12 (mesmo dia, sessão anterior) tinha passado
pela seção 2.23 procurando nome desatualizado, viu "AGENDAR Estagnado" como
nome próprio já publicado e seguiu — nunca perguntou se o workflow atrás do
nome ainda fazia sentido.

**Regra prática, generalizável, e diferente de toda a família G-02/G-06 a
G-12 (que procuravam "canal novo sem guarda" ou "nome sem migrar"):**
quando uma decisão do dono muda o **comportamento** de um nó (não só o nome
de uma etapa ou a lista de canais aceitos), a varredura de coerência
precisa fazer duas perguntas separadas, porque responder "sim" à primeira
não implica "sim" à segunda: (1) os nomes usados aqui ainda existem/têm o
papel que o texto assume? (2) o nó ainda faz, hoje, o que o texto diz que
ele faz? A auditoria de dump ao vivo (§2.31) já tinha a resposta certa da
pergunta 2 havia dois dias; só não tinha sido cruzada com as outras duas
seções do mesmo arquivo que descreviam o mesmo nó por um caminho diferente
(a explicação nó a nó, não a auditoria de tag). Onde um workflow é descrito
em mais de um lugar (spec "por que", spec "como clicar", auditoria de dump),
uma mudança de comportamento só está de fato propagada quando os três
concordam — não quando o mais recente está certo e os outros dois, calados.

## Corrigir a coerência não fecha a pergunta "quem mais cita isso?" — G-14, 23/09/2026, sessão automática

CRM reconfirmado sem mudança via API (56 campos, 56 oportunidades, mesma
composição do G-13) — nenhum G/R/F desbloqueado. A varredura de coerência de
sempre, desta vez, não foi sobre o produto (nome de etapa, comportamento de
nó) — foi sobre o **próprio processo de correção**: o G-10 listou seis
documentos para cruzar com `PLANO-MULTICANAL.md` e o G-13 corrigiu mais
dois (`build-wesales.md`, `IMPLEMENTACAO-WORKFLOWS.md`) e avisou dois
(`campos-e-tags.md`, `APROVADO.md`). Pergunta que ninguém tinha feito depois
de qualquer um dos dois fechar: **essa lista de documentos está completa?**
Não estava. `GUIA-MONTAGEM.md` — que o próprio `IMPLEMENTACAO-WORKFLOWS.md`
define como o documento do "estado do que já foi montado" — nunca apareceu
em nenhuma das duas listas, apesar de citar a mesma etapa e a mesma tag que
o G-13 já tinha corrigido em outro lugar. Pior: uma das suas linhas era uma
instrução ativa ("dá para fazer HOJE") recomendando o desenho que o G-13 já
tinha classificado como "não recomendado" — ou seja, dois documentos
diziam coisas opostas sobre a mesma tag, e nenhum apontava para o outro.

**Achado de categoria diferente, no mesmo grep:** `rotina-limpar-
tarefas.md` não é só um caso de nome de etapa desatualizado — a **filosofia
operacional inteira** do documento (concluir tarefa fora de lugar, nunca
excluir) foi invertida por uma decisão posterior do dono (`PLANO-
MULTICANAL.md`, D12: "concluir inventa histórico falso", por isso a Faxina
**exclui**). Um grep por "AGENDAR" acharia a etapa errada na tabela; não
acharia que a lógica de fundo do documento foi substituída — isso só
aparece lendo a seção "Por que a rotina é assim" contra a decisão mais
recente, não contra o vocabulário. `IMPLEMENTACAO-WORKFLOWS.md` (§3.3)
citava esse prompt como o mecanismo "a cada hora" quando o que roda de
verdade, a cada 10 min, é a Faxina — nem esse documento, já corrigido pelo
G-13 para o nome da etapa, tinha notado que a própria referência ao
mecanismo de manutenção estava desatualizada.

**Regra prática, generalizável — a mais importante desta família:** fechar
um achado de coerência em N documentos não é o mesmo que fechar a pergunta
"quem mais fala disso?" — é fechar "os N que eu olhei estão certos agora".
A cada G-10/G-12/G-13 (ou qualquer item futuro da mesma família), antes de
declarar o achado resolvido, valeria repetir a busca (grep pelo termo,
grep pelo nome do documento/mecanismo que mudou) **sobre a lista inteira de
arquivos do projeto**, não só sobre os que a memória da rodada já tinha em
mente — porque a lista de "quem cita isso" costuma ser maior do que o
primeiro grep que a achou. E dentro dessa busca, dois tipos de divergência
pedem leituras diferentes: nome desatualizado pede grep pelo termo; **lógica
ou filosofia substituída** (concluir vs. excluir, aqui) só aparece lendo a
seção de justificativa do documento contra a decisão mais recente — grep
nenhum acha isso sozinho.

## `Contact Changed` não filtra por Telefone nem E-mail — a ação `Merge Contact` existe, mas não tem como ser acionada sozinha — G-15, 23/09/2026, sessão automática

Sweep de coerência limpo (nenhum nome de etapa órfão novo, `AGENTE-IA-
CONEXAO.md` já explicava por que "ETAPA 4 — AGENDAR" dentro do prompt da IA
não é a etapa do funil — falso positivo do próprio grep, não achado); CRM
reconfirmado por API sem mudança de composição (56 oportunidades, mesmos
campos). A lacuna veio de ler `conversations_search-conversation` (55
conversas, todas as 55 desta vez, não só as 20 do limite padrão) com uma
pergunta que nenhuma rodada tinha feito: os contatos que chegam pelo
Instagram (`Qualificação por IA no WhatsApp`, seção 6) não têm telefone nem
e-mail — o que impede a mesma pessoa de já existir como contato por
telefone (Meta Lead Ads) e virar um segundo contato, com uma segunda
cadência, sem ninguém perceber?

**Pesquisado antes de desenhar** (`WebSearch`, `help.gohighlevel.com` e
`ideas.gohighlevel.com`, confiança média — página oficial e board de ideias
citados em buscas com termos diferentes, mesmo padrão de confiança já usado
no G-05/R-14): o GHL tem uma ação nativa de workflow, **`Merge Contact`**,
que funde duplicatas comparando Telefone, E-mail, ou os dois — parecia
resolver o problema inteiro sozinha. **Não resolve, porque o gatilho que a
chamaria não existe:** `Contact Changed` — o único gatilho deste projeto
que reage a mudança de campo, já usado em várias seções do
`build-wesales.md` com filtro por Custom Field — hoje só aceita filtrar por
Usuário atribuído, DND, Tag, Custom Field, Endereço e Website. **Telefone e
E-mail não estão nessa lista**, e são pedido em aberto no próprio board de
ideias da HighLevel (`ideas.gohighlevel.com/automations/p/add-phone-and-
email-changes-to-the-contact-changed-trigger`), sem previsão de entrega.

**Regra prática, generalizável:** antes de desenhar qualquer automação em
cima de uma ação nativa nova, a pergunta não é só "a ação existe?" — é "o
gatilho que a chamaria no momento certo também existe?". Uma ação pode
estar documentada e disponível (`Merge Contact` está) e ainda assim ser
inacionável de forma automática porque a plataforma não expõe o gatilho
certo — o mesmo tipo de parede que o R-11/F-05 já bateram para contagem
agregada (`Scheduler`/Custom Metrics, entrada acima), agora para mudança de
campo padrão (Telefone/E-mail) em vez de custom field. Onde isso acontece,
a saída não é insistir no workflow: é a ferramenta nativa de tela mais uma
rotina humana (mesmo padrão do R-11/R-14) — `build-wesales.md`, seção 5.5.

## Um achado real de outra sessão pode ficar preso num documento que o roadmap principal nunca cruza, mesmo depois de ter sido medido e documentado a fundo — G-17, 23/09/2026, sessão automática

Aplicando a própria regra do parágrafo anterior (`git log -- wesales/`
contra a lista de arquivos já cruzados): entre a leitura do G-16 e esta
rodada, uma sessão em paralelo tinha escrito quatro commits
(`ab5f4d5`/`46724a9`/`31206c6`/`ea16ca3`) resolvendo a pendência 9e de
`ESTADO-E-PLANO.md` — e generalizando o achado para três cadências
publicadas (`Cadência Inbound`, `Recuperação de No-show`,
`Reengajamento 90 dias`) que não leem o portão de capacidade do SDR, a
pior delas (`Reengajamento 90 dias`) gastando a cota semanal compartilhada
sem nunca respeitá-la. O trabalho técnico (medição nó a nó, duas
ferramentas novas — `auditoria_portoes.py`, `patch_portao_inbound.py` — e
validação `--dump` sem tocar a conta) já estava completo e correto em
`build-wesales.md` §2.36–2.39. O que faltava não era pesquisa nem desenho:
era a ponte para `ROADMAP-SALES-ENGAGEMENT.md`, sem a qual uma leitura
futura que só abrisse o roadmap principal (a maioria) nunca saberia que a
decisão existe.

**Regra prática, generalizável — mesma do G-10/G-14/G-16, agora com um caso
a mais:** achado técnico completo (medido, documentado, com ferramenta
validada) em `build-wesales.md`/`ESTADO-E-PLANO.md` não é a mesma coisa que
achado **rastreável** — só vira rastreável quando ganha um item numerado no
roadmap principal com "Pronto quando" próprio. A pergunta "isto já virou
item de roadmap?" precisa ser feita mesmo quando o resto do trabalho
(pesquisa, script, validação) já está pronto — principalmente aí, porque é
exatamente quando parece "já resolvido" que ninguém verifica se falta só a
ponte.

**Correção aplicada:** achado promovido a `G-17` no
`ROADMAP-SALES-ENGAGEMENT.md` (por quê / como / pronto quando, com a tabela
de medição e as duas opções de desenho para o dono escolher por cadência);
`ESTADO-E-PLANO.md` (itens 9d, resolvido, e 9e, com link de volta) e
`IMPLEMENTACAO-WORKFLOWS.md` (checklist de go-live, §3.6) atualizados para
não repetir a mesma lacuna que o G-16 já tinha corrigido para si mesmo.
Zero escrita no CRM, zero campo, zero tag: item de coerência entre
documentos e especificação de decisão.

## Ler o JSON do workflow (`next`/`parent`/`parentKey`) prova comportamento que o texto do `build-wesales.md` só descreve — e quase me fez reportar um bug catastrófico que era código morto — G-18, 23/09/2026, sessão automática

O G-13 tinha deixado uma pendência explícita, nunca promovida a item: "o
ramo `Atendeu` do `Pós-ligação v2` não tira o lead da `Cadência 12x30`
(confirmado no dump)". Em vez de confiar no texto, abri
`wesales/workflows-json/Pós-ligação v2.json` e reconstruí o grafo de
execução na mão: cada nó tem `id`, `next` (ou lista, se é um `if_else` com
`branches[].id`), `parent`/`parentKey` (metadado de canvas, não de
execução). Um `grep` por nome de ação não basta — o mesmo `if_else` por
`Resultado da tentativa` existe **duas vezes** no arquivo (uma para cada
lado de um canal-check por tag `fila-wa`, herdado de antes da régua virar
100% telefone), e só uma das duas cópias é alcançada pela operação real
hoje. Script usado (não ficou como ferramenta, foi só investigação ad hoc):
BFS a partir de um nó, seguindo `next`, imprimindo `type`/`name`/atributos
relevantes até bater num nó sem `next` (terminal) ou numa lista (bifurcação).

**O quase-erro:** ao rastrear a cópia "morta" (alcançável só se `fila-wa`
sobreviver até o ramo `Atendeu`), achei um caminho que termina em
`Math: Conexões telefone +1` **sem nenhuma tag, tarefa ou nota depois** —
parecia que o canal telefone (100% da operação) nunca gerava a tarefa
`[FECHAR HORÁRIO]`, um bug catastrófico. Só não virei isso num achado
antes de confirmar duas coisas: (1) qual das duas cópias do switch a
operação real alcança (a que tem `fila-wa` **ausente** no canal-check
externo, não a que eu estava seguindo), e (2) que a cópia real, rastreada
por completo, está inteira — tem a tarefa, a tag, a nota. O caminho quebrado
só é alcançado quando `fila-wa` está presente **duas vezes seguidas** (no
canal-check externo e de novo dentro do próprio ramo `Atendeu`), e a régua
publicada nunca deixa essa tag presente nesse ponto — é código morto pelas
mesmas tags que o levariam até ali, não um caminho que lead real percorre.
Mesma classe de alarme falso que `auditoria_tudo.py` já registrou (achado
que "tem um gêmeo" e o gêmeo muda a leitura).

**A parte que sobreviveu à conferência, e virou G-18:** independente da
cópia morta, **nenhuma** das duas cópias do ramo `Atendeu` tem
`remove_from_workflow` — diferente do ramo `Não ligar`, que tem, nas duas
cópias. Conferi também o dump da própria `Cadência 12x30` antes de escrever
qualquer coisa: ela já se auto-remove no caso comum (nó 10 de cada
tentativa, `remove_from_workflow: este`, mas só enquanto o `Aguardar
resultado` daquela tentativa específica ainda está ativo). O que falta não
é "o lead nunca sai" — é a segunda linha de defesa, independente de timing,
que o `Não ligar` já tem e o `Atendeu` não, para quando a classificação
chega fora da janela da tentativa.

**Regra prática, generalizável:** ao investigar comportamento de workflow
publicado, ler o JSON (grafo `next`/`branches`) prova o que o texto do
`build-wesales.md` só descreve — e às vezes o texto e o dump divergem sem
que ninguém tenha mentido (o texto foi escrito quando só uma cópia existia,
o dump carrega as duas). Antes de reportar um achado como grave, sempre
perguntar: **qual caminho a operação real percorre hoje, e o achado está
nesse caminho ou num vizinho que parece igual mas nunca é alcançado?** A
mesma pergunta que já salvou o F-08/F-09 de decisão baseada em número
vencido, aqui aplicada a grafo de execução em vez de texto.

**Correção aplicada:** achado promovido a `G-18` no
`ROADMAP-SALES-ENGAGEMENT.md` (por quê, com a precisão sobre gravidade
registrada explicitamente para não superestimar; como; pronto quando);
patch novo `wesales/tools/patch_remove_atendeu.py`, validado por `--dump`
(142 → 146 nós, `exit 0`); `build-wesales.md` (seção 4, ramo `Atendeu`)
atualizado para não repetir a pendência como "em aberto" depois de ela ter
"Pronto quando" próprio; `GUIA-MONTAGEM.md` (retoque do nó 2/"Total de
conexões") anotado para não deixar alguém "consertar" a cópia morta achando
que é a que roda de verdade. Zero escrita no CRM, zero campo, zero tag: item
de especificação e patch validado por dump, não depende de `APROVADO.md`.

## Uma varredura de coerência que só procura texto divergente não acha soma errada — o total de tags estava escrito errado em três documentos, e a lista ao lado de cada um já somava certo — G-20, 23/09/2026, sessão automática

Sweep de sempre (CRM por API, PR #93) veio limpo — 56 oportunidades, mesma
composição da leitura do G-19, PR ainda `open`/`draft`. `PLANO-MULTICANAL.md`
lido por inteiro nesta rodada (pendência que o próprio G-19 tinha deixado
para a próxima) sem achado novo — a seção "Fila autônoma" já estava coberta
pelos itens A1-A9 que ela mesma lista, nenhum promovido a item de roadmap
faltante.

A lacuna veio de uma pergunta que nenhuma das 19 rodadas anteriores tinha
feito: os **totais** que este projeto declara (quantos campos, quantas
tags) batem com a própria enumeração que cada um resume? Bateu para campos.
Não bateu para tags: `campos-e-tags.md` ("10 na conta fora da numeração",
"Total na conta hoje: 25"), `APROVADO.md` ("são dez as tags fora desta
lista") e `build-wesales.md` §2.32 ("a conta tem 25 tags") — as três somas
erradas, apesar de a frase ao lado de cada uma já enumerar `teste-regua`,
`fechar-horario`, `cadencia-12x30-p2`, `teste-12x30` e "as 8 do Espelho de
Etapa" (1+1+1+1+8 = 12, não 10; 15 do projeto + 12 = 27, não 25).

**Como o erro nasceu:** a primeira versão (só `teste-regua`/`fechar-horario`
existiam) dizia "duas", certo para aquele momento. Quando o commit
`61eb167` trouxe as 8 tags do Espelho de Etapa, a atualização somou 2 + 8 =
10 e esqueceu que `cadencia-12x30-p2`/`teste-12x30` já estavam na mesma
tabela, duas linhas abaixo — um erro de soma no meio de uma edição que
parecia completa (o texto foi reescrito na mesma rodada que acrescentou o
dado novo). As cópias seguintes (`APROVADO.md`, `build-wesales.md`) herdaram
o "10"/"25" já errado sem resomar.

**Regra prática, generalizável — estende o "quem mais fala disso?" do
G-10/G-14/G-16/G-17 (que acha nome e referência divergente) para números:**
grep encontra nome de etapa órfão e merge field trocado porque o valor
errado é *diferente* do valor certo em texto. Uma soma errada não é
diferente de nada — ela só aparece resomando a lista contra o total escrito
ao lado. "O texto foi editado nesta mesma rodada" não é evidência de que o
número está certo; é só evidência de que alguém mexeu perto dele. A partir
de agora, toda rodada que mexer em contagem (campo, tag, etapa, tentativa)
resoma a lista antes de aceitar o número escrito perto dela — não só
depois de mudar algo, também ao herdar um número que já existia.

**Correção aplicada:** achado promovido a `G-20` no
`ROADMAP-SALES-ENGAGEMENT.md`; `campos-e-tags.md` (Etapa 3) ganhou a mesma
convenção "onde mora a contagem" que a Etapa 2 (campos) já tinha, com os
números certos (12/27); `APROVADO.md` e `build-wesales.md` §2.32 pararam de
repetir o número (regra "número fixo só na fonte") e passaram a apontar
para `campos-e-tags.md`. Zero campo, zero tag, zero escrita no CRM: item de
coerência entre documentos, não depende de `APROVADO.md`.

## Auditoria diária (só leitura): a entrada piorou de ~25h14 (22/09) para 55h50 (23/09) sem lead novo, e o recorde que a régua "múltiplo do pior caso" mede mais que dobrou de uma rodada para a outra — 23/09/2026, sessão automática seguinte

Continuação da série que a auditoria diária de 22/09/2026 abriu (entrada
acima). Naquela leitura (22/09, ~10:31 UTC) o silêncio de entrada estava em
25h14min, 1,67× o recorde da base (15h06, 20/09 18:11 → 21/09 09:17).
Nenhuma rodada entre aquela e esta tinha voltado a medir especificamente
este número — G-16 a G-20 reconfirmaram oportunidades e campos a cada
rodada, mas nenhuma reabriu o F-10 para perguntar de novo "quanto tempo faz
desde o último lead pago". A regra generalizável do próprio F-10 ("reler
item represado por informação que pode ter vencido") se aplica a ele mesmo
quando a informação é um relógio que nunca para de correr.

**Medido às 23/09 17:07 UTC, por `opportunities_search-opportunity`
(`status: all`):** 56 oportunidades, mesma composição das leituras de G-16 a
G-20 — nenhuma nova desde então. O lead com `source: Facebook` mais recente
continua sendo `Carlos Andrade`, 21/09/2026 09:17:26 UTC. Diferença: **55h50min**
sem lead pago novo, contra 25h14min na leitura anterior (22/09, ~10:31 UTC).
O intervalo entre as duas auditorias foi de ~30h36min, e o silêncio cresceu
exatamente esse mesmo tanto (25h14 → 55h50) — a aritmética confirma o que já
era esperado de "nenhuma oportunidade nova desde então": **zero lead novo em
todo o intervalo entre as duas auditorias**, não só desde o último lead.
O múltiplo do recorde foi de 1,67× para **3,7×**.

**Por que isto é o tipo de achado que uma auditoria pontual, e não um
alarme automático, ainda consegue pegar:** as seis peças do Monitor de Saúde
(F-05) — todas sobre lead que ficou parado — continuam sem ver nada de
errado, exatamente como o F-10 já tinha documentado (fila esvazia, `NOVO
LEAD` para de crescer, toques caem, tudo "verde"). Só uma leitura que pergunta
"quando foi o último lead novo" pega isto, e nenhum widget do F-10 está
montado na tela ainda — as duas Smart Lists da seção 8.25 seguem
especificadas, não publicadas. Enquanto isso não muda, a única rede de
segurança contra este tipo de falha silenciosa é a próxima sessão automática
lembrar de perguntar de novo — o que esta rodada fez, e o que a rodada
seguinte devia fazer também, até a entrada voltar ou o dono decidir o alarme
da opção (b).

**Regra prática, que fica:** para um item cujo "Pronto quando" depende de um
relógio (tempo desde o último evento), a leitura fica velha mesmo sem
nenhuma mudança no resto da subconta — reconfirmar "oportunidades sem
mudança" não é o mesmo que reconfirmar o próprio relógio, e as duas coisas
podem divergir por dias se ninguém perguntar pela segunda explicitamente.

**Correção aplicada:** `ROADMAP-SALES-ENGAGEMENT.md`, F-10, ganhou o novo
número e uma nota de fechamento própria; `build-wesales.md` (duas menções,
seção 2.17 e seção 8.25) e `briefing-sdr.md` (L-07) pararam de repetir o
múltiplo/contagem específicos (regra "número fixo só na fonte", a mesma que
o G-20 já tinha aplicado a campo/tag) e passaram a apontar para a leitura
mais recente do F-10. Zero campo, zero tag, zero escrita no CRM: leitura por
API, não depende de `APROVADO.md`.

## `AGENTE-IA-CONEXAO.md` nunca tinha sido cruzado por nenhuma rodada de coerência — e carregava, desde 22/09, uma dúvida sobre a própria razão de existir nunca promovida a item rastreável — G-22, 23/09/2026, sessão automática

Sweep de sempre limpo: `git fetch` sem commit novo, CRM reconfirmado sem
mudança (56 oportunidades, mesma composição da leitura do G-21; 56 campos
de contato). A varredura de coerência das últimas seis rodadas (G-16 a
G-21) tinha cruzado `ESTADO-E-PLANO.md`, `git log`, `PLANO-MULTICANAL.md` e
a soma de campos/tags — nunca `AGENTE-IA-CONEXAO.md`, apesar de ele
descrever o único canal que alcança 5 leads reais presos num ciclo morto
de 90 em 90 dias (achado do F-15). Lendo o documento de propósito (a
mesma pergunta generalizável do G-16/G-17/G-19/G-21, "que documento ainda
não foi cruzado?"), duas pendências da própria seção 8 saltaram: item 2
("se o agente só responde WhatsApp, não alcança os 5 do Instagram — que
são o motivo principal dele existir") e item 3 ("se a tela não oferecer
filtro por tag... o agente não deve ficar como Agente Principal até
existir") — a segunda descrevendo a única proteção contra o SDR e a IA
falando com o mesmo lead ao mesmo tempo, sem confirmação nenhuma de que
existe.

**Diferença desta vez, dentro da mesma família de achado:** os quatro
casos anteriores (G-16/G-17/G-19/G-21) tinham decisão do dono e/ou patch
prontos, só sem ponte para o roadmap — bastava promover. Aqui não havia
nem decisão nem patch, só uma pergunta de pesquisa nunca respondida.
Pesquisado nesta rodada (`WebSearch`; `help.gohighlevel.com` bloqueado
pelo proxy deste ambiente para `WebFetch` direto — mesma limitação que o
G-05/F-08/F-12/R-14 já registraram, contornada com duas buscas de termos
diferentes convergindo no mesmo achado, confiança média, não testado
nesta subconta): Instagram é canal nativo do Conversation AI Bot
(reduz a dúvida do item 2 a uma pergunta de configuração desta subconta
específica, não mais de suporte de plataforma); e existe uma ação de
workflow nativa, `Update Conversation AI Bot and Status`
(`Active`/`Inactive` por contato, chamável de qualquer workflow, três
fontes convergentes — HighLevel Support Portal, HighLevel Changelog/
Ideas, tutorial de terceiro), que resolve a proteção do item 3 sem
depender de nenhum filtro de tela nunca confirmado.

**Achado lateral, sobre o próprio mecanismo de "Channel Management" que o
item 3 pressupunha:** a documentação descreve esse roteamento como
prioridade (assinalação mais específica vence a mais genérica), não como
lista de exclusão — diferente do que a seção 1 do `AGENTE-IA-CONEXAO.md`
assumia ("o agente não responde contato que tenha qualquer destas
tags"). Antes de aceitar que "existe filtro de tag na tela" resolveria o
problema do jeito descrito, valeria checar se o mecanismo real (prioridade)
cobre o mesmo caso de uso (exclusão) — aqui a saída foi não apostar nisso e
usar a ação de workflow, que não tem essa ambiguidade.

**Regra prática, generalizável — estende a família G-16/G-17/G-19/G-21 de
"achado com decisão/patch represados" para "achado só com pergunta de
pesquisa represada":** a pergunta "que documento ainda não foi cruzado?"
não deveria se limitar a documentos com decisão pronta — um documento
pode carregar só uma dúvida em aberto (sem patch, sem decisão do dono) e
ainda assim estar a uma pesquisa de virar item rastreável com "Pronto
quando" próprio. `AGENTE-IA-CONEXAO.md` é o quinto documento nessa
categoria (depois de `ESTADO-E-PLANO.md` três vezes e `PLANO-MULTICANAL.md`
uma vez) — a lista de "documentos ainda não cruzados" não é ilimitada, mas
também não secou: `script-de-ligacao.md`, `GUIA-CLOSER.md`, `GUIA-SDR.md`
e `conectar.md` seguem sem nenhuma rodada desta família ter passado por
eles.

**Correção aplicada:** achado promovido a `G-22` no
`ROADMAP-SALES-ENGAGEMENT.md` (por quê, pesquisa com fontes e nível de
confiança, desenho de dois workflows novos — "Bot IA — Pausar por Fila"/
"Bot IA — Retomar" — especificados nó a nó, "Pronto quando"), com a
narrativa da "Ordem sugerida" e a tabela "Com isso" atualizadas no mesmo
padrão do G-16 a G-21; `AGENTE-IA-CONEXAO.md` (§1, com a tabela dos dois
workflows novos como segunda camada de proteção; §8, itens 2 e 3, com o
achado da pesquisa e o redimensionamento de "bloqueio" para "preferível
mas não único"). Zero campo, zero tag novos (as 6 tags do portão já
existem); zero escrita no CRM: item de pesquisa e especificação, não
depende de `APROVADO.md` — os dois workflows novos não saem por API (mesma
limitação de sempre), ficam para a montagem manual.
