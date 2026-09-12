# LOG — revisão, correção e ativação dos 5 conjuntos nichados (11/09/2026, 23h)

Pedido do Pablo: *"Encontro erros, ou oportunidades melhorias? como somente celular,
interesse, posicionamento, etc? Senão, revise novamente, aplique e ative os anúncios"*.

Sim, encontrei erros — inclusive um meu, grave.

## ERRO 1 (meu, grave) — o nicho estava diluído em 3 dos 5 conjuntos

Dentro de **uma mesma entrada** de `flexible_spec` tudo é **OU**. Eu tinha misturado,
na mesma entrada, o sinal do nicho com cargos genéricos:

- **ODONTOLOGIA:** `faculdade de odontologia` OU **Proprietário** OU **Comerciante**
  OU **Dono** OU **Proprietário(a)** OU `Cirurgião Dentista Implantodontista`
- **ESTÉTICA:** esteticista OU **Proprietário** OU **Empresária** OU **Proprietário(a)** OU **Empresária/proprietária**
- **ENERGIA SOLAR:** interesses solares OU **Proprietário** OU **Comerciante** OU **Dono** OU **Proprietário(a)** OU Sócio-Diretor Comercial

Efeito prático: qualquer dono de qualquer negócio entrava. Os três conjuntos "nichados"
eram, na verdade, **o mesmo público genérico do `LEADS I INTERESSE`**, competindo entre si
no leilão, com criativo de nicho que não batia com quem via.

**Corrigido:** removidos todos os cargos genéricos. Ficou só o sinal do nicho.

## ERRO 2 — só celular

Os cinco estavam `device_platforms: ["mobile"]`. Dono de negócio abre o Facebook no
computador em horário comercial. Cortar desktop tira leilão e encarece o lead.
**Corrigido:** restrição removida nos cinco.

## ERRO 3 — posicionamento apertado demais

Só feed + reels no Facebook e no Instagram. Ficavam de fora Stories, Explorar,
Marketplace, feed de vídeo e busca. Com verba pequena, restringir posicionamento
sobe o custo. **Corrigido:** posicionamento automático (Meta escolhe onde é mais barato).

## ERRO 4 — `locales: [16]`

Limitava a quem usa o app em português do Brasil. Num público já pequeno, isso corta
de graça. **Removido.**

## ERRO 5 — idade parava em 55

Dono de imobiliária e de clínica com 56–60 existe, e muito. **Subido para 60.**

## ERRO 6 — estética só para mulheres (`genders: [2]`)

Cortava metade do público, e o criativo não é dirigido a mulher. **Removido.**

## ERRO 7 — quatro conjuntos ativos com zero anúncio ativo

VETERINÁRIA, ODONTOLOGIA, ESTÉTICA e SOLAR estavam ligados com os 3 anúncios de cada
um pausados. Conjunto ligado sem anúncio ligado não entrega nada. **Os 12 foram ativados.**

## Também ativado: 2º e 3º anúncio nos conjuntos que dão lead

Estavam com um anúncio só (o V10), o que impede o Meta de testar e derruba a entrega
quando ele cansa. Ativados 2 em cada, sem mexer no V10 nem na segmentação deles
(estão funcionando — CNAE RJ a R$ 4,74 por lead):

- `LEADS I SEMELHANTE CNAE RJ I FASE 3`: AG08 e AG09
- `LEADS I INTERESSE I FASE 3`: AG05 e AG03

## Segmentação final dos cinco

Base comum: idade **30–60**, região `454` (RJ), cidades excluídas `255567` (Itaboraí) e
`258769` (Magé), **todos os dispositivos**, **posicionamento automático**, sem restrição
de idioma, `advantage_audience: 0`, e a segunda entrada **AND** com os administradores de
página (`6015683810783`, `6020530281783`, `6297846662583`).

| Conjunto | Sinal do nicho (agora limpo) |
|---|---|
| IMOBILIARIA | 5 cargos de Corretor + interesses `6778210171187` (Corretagem residencial), `6849945059527` (Marketing do setor imobiliário), `6788101567252` (Portais de imóveis) |
| VETERINARIA | 2 cargos de Médico Veterinário + interesses `6003286955541`, `6004314556489` |
| ODONTOLOGIA | cargo `168991743113816` + interesse `6003382042002` |
| ESTETICA | 2 cargos de esteticista + interesse `6811343488093` (Mídia de cosmetologia) |
| ENERGIA SOLAR | interesses `6003437140731`, `6003775814878` |

## O que a busca de segmentação revelou (e continua sem solução)

Puxei o tamanho de público de cada sinal. Dois achados honestos:

1. **Todo `work_position` volta com `audience_size: 0`** — inclusive os de corretor, que
   são os mais fortes. Isso é limitação da API (ela não reporta tamanho para cargo), não
   prova de que o público é vazio. Mas quer dizer que **não dá para medir o tamanho de
   conjunto montado em cima de cargo**, e é por isso que eu continuo sem confirmar os 300k.
2. **Odontologia e solar seguem sem sinal de dono.** Busquei de novo: em odontologia existe
   um único interesse (`faculdade de odontologia`, 790 mil no mundo inteiro) e um único
   cargo. Em solar, os dois interesses são de **consumidor querendo painel** — o cliente do
   prospecto, não o prospecto. O que segura esses dois é só a entrada AND de administrador
   de página. Se em uma semana não derem lead, o certo é desligar, não insistir.

## Estado final

**15 anúncios nichados ativos** (VET03 em análise, normal) + **6 nos conjuntos que já
convertem**. `ads_get_errors` voltou `[]` nos cinco conjuntos. Orçamento **não foi tocado**:
segue CBO R$ 30/dia.

---

# Adendo (11/09, 23h50) — a copy do V10 vendia a mentoria

Pedido do Pablo: *"Ajuste a copy, apenas remova o detalhe da mentoria"*.

## O que estava no ar

Auditei a copy dos 21 anúncios ativos. **Só os dois V10 tinham o problema** — e ele
era maior que a etiqueta da imagem. O corpo do texto era este:

> Você não precisa de uma agência. Precisa saber como.
>
> Anunciar não é um serviço que se compra todo mês — é uma habilidade que se aprende
> uma vez. A diferença entre as duas coisas é quem manda no seu crescimento.
>
> Encontros online toda semana, do zero ao anúncio no ar, feito na sua própria conta
> e com o seu próprio negócio. Você não precisa ser gestor de tráfego; precisa saber
> decidir.
>
> 3 perguntas e a gente conversa.

Três problemas, em ordem de gravidade:

1. **"Você não precisa de uma agência"** — o anúncio argumentava contra o que o Pablo
   vende hoje. Ele é agência.
2. **"não é um serviço que se compra todo mês"** — argumentava contra o modelo de
   receita recorrente da agência.
3. **"Encontros online toda semana"** — é o formato da mentoria, produto descontinuado.

Isso importa além da estética: **os 12 leads que entraram até agora responderam a uma
oferta de mentoria**, não de agência. Quando o Clint voltar e a taxa de lead → reunião
for medida, esse descasamento é a primeira hipótese a testar para lead que não avança.

## O que os outros 19 tinham

Limpos. Os 15 nichados e os 4 AG já falam como agência ("A gente escreve, publica e
acompanha"). Conferido um a um, não por amostragem.

## A copy nova

Mantive a forma do vencedor — mesmo gancho de negação, mesmo ritmo, mesmo fechamento
literal ("3 perguntas e a gente conversa") — e troquei só o produto:

> Você não precisa virar gestor de tráfego. Precisa de cliente.
>
> Anunciar bem não é sorte, é método — e o método é o nosso trabalho. A gente escreve
> o anúncio, publica, acompanha e ajusta toda semana.
>
> Você não mexe em nada. Só atende quem chega no seu WhatsApp.
>
> Para quem já tem negócio e já fatura. 3 perguntas e a gente conversa.

Título (`Cliente todo dia no seu WhatsApp`) e botão (`SIGN_UP`) **não foram tocados** —
são parte do que converte e não tinham nada de mentoria.

## Como foi aplicado

`update_ad_creative` com **`degrees_of_freedom_spec: {}`** junto. Sem isso a Meta
devolve `3858504` ("o criativo não deve incluir aprimoramentos padrão"), porque a
cópia arrasta o spec descontinuado do V10 — pedra já documentada no LOG das 10 peças
AG e que voltou a aparecer aqui exatamente igual.

| Anúncio | Conjunto | Criativo novo |
|---|---|---|
| `120247356537060766` | LEADS I INTERESSE I FASE 3 | `1405900931679081` |
| `120247356513990766` | LEADS I SEMELHANTE CNAE RJ I FASE 3 | `1655425389259510` |

`ads_get_errors` nos dois: `[]`. Copy relida no criativo novo: confere.

## O que NÃO foi resolvido

**A imagem continua sendo a foto do Pablo, com a pílula "MENTORIA O PRÓXIMO CLIENTE"
escrita nela.** A copy virou agência; a arte ainda diz mentoria. O anúncio está
incoerente consigo mesmo até a arte ser trocada.

Trocar a arte esbarra em três bloqueios simultâneos, todos medidos hoje:

1. **Pexels e Google Fonts negados pelo gateway de egresso** desta sessão
   (`connect_rejected`), então não dá para baixar foto nem tipografia aqui.
2. **`fontes/` e `fotos/` não existem no repositório** — o `modelo_v10.py` depende
   das duas, e quem as provê é o runner do Actions, não o repo.
3. **O workflow `imagens-anuncio.yml` que faria isso no runner exige
   `PEXELS_API_KEY`**, secret que não está cadastrado — é por isso que
   `entregas/campanha/imagens/` só tem `creditos.md` e o ícone.

Caminho que contorna os três, para a próxima sessão: gerar a foto pelo **Higgsfield**
(que responde), baixar o Montserrat do **GitHub raw** (que responde, é de onde o
próprio workflow baixa), compor com o `modelo_v10.py`, subir no Drive e criar o
anúncio por `image_url`. Não executei porque é caminho longo e não testado ponta a
ponta — vale fazer com tempo, não no fim da noite, e o Pablo precisa ver a arte antes
de ela substituir o único anúncio que dá lead.

---

# Adendo 2 (12/09, 00h) — a peça pedida já existia; e uma chave vazou

## O pedido

O Pablo apontou qual anúncio ele queria replicado, pelo texto da arte:
*"Acordar com o whatsapp Cheio de Clientes todo dia sem depender de indicação"*.

## A descoberta que economizou a rodada inteira

Antes de tentar gerar arte nova, fui conferir o que já existia. **A peça pedida já
estava pronta e no ar: a AG01.** Ela é a arte do V10 com exatamente a troca que o
Pablo pediu:

| | V10 (com foto do Pablo) | AG01 (já no ar) |
|---|---|---|
| linha sans | acordar com o WhatsApp | acordar com o WhatsApp |
| linha cursiva | cheio de cliente | cheio de cliente |
| botão na arte | QUERO ISSO NO MEU NEGÓCIO | QUERO ISSO NO MEU NEGÓCIO |
| **etiqueta** | **MENTORIA O PRÓXIMO CLIENTE** | **AGÊNCIA O PRÓXIMO CLIENTE** |
| **foto** | **pablo_IMG_2325.jpg** | **foto de banco, não é o Pablo** |

Confirmei que as artes são mesmo distintas comparando os hashes de imagem no Meta:
o V10 serve `788952054_...` e a AG01 serve `803267693_...`. São arquivos diferentes.

**Consequência:** os três bloqueios de geração de arte documentados no adendo 1
(Pexels negado, `fontes/` e `fotos/` ausentes, `PEXELS_API_KEY` não cadastrada) eram
reais mas **irrelevantes para este pedido**. Não era preciso gerar nada. A lição é
velha e voltou a se pagar: conferir o que já existe antes de construir.

Única diferença remanescente para o original: a linha de apoio. O V10 diz *"todo dia,
sem depender de indicação"* e a AG01 diz *"a gente faz o anúncio, você só atende"*.
O tema "sem depender de indicação" existe na AG02, que também está ativa no conjunto
de interesse. Não achei que valesse uma arte nova só por essa linha — mas fica
registrado como o delta, caso o Pablo queira a frase literal.

## O que foi executado

1. **Clonada a AG01 para o conjunto CNAE RJ**, onde ela não existia. Anúncio
   `120247396147800766` em `120247356496360766`, reusando o criativo
   `2374168726451823` por `creative_id` — o que também carregou o formulário de
   lead junto, sem esbarrar no `Missing Lead Form (3390001)` que travou a rodada
   anterior. `ads_get_errors`: `[]`. Criado pausado, verificado, depois ativado.
2. **Pausados os dois anúncios V10 com a foto do Pablo**: `120247356537060766` e
   `120247356513990766`.

Ordem deliberada: a substituta subiu e foi verificada **antes** de a original cair,
para nenhum conjunto ficar descoberto em nenhum momento.

## Risco assumido, dito na cara

O V10 era **o único anúncio da conta com histórico de lead comprovado** (12 leads,
custo caindo de R$23 para R$2,55 em quatro dias). A AG01 tem a mesma arte e a mesma
promessa, mas número próprio ainda não tem. É esperado que o custo por lead oscile
por dois ou três dias enquanto o Meta reaprende. Gatilho de alarme já combinado com o
Pablo: **custo por lead acima de R$8,00 por dois dias seguidos** = avisar.

## Incidente de segurança — chave da Clint exposta

O Pablo colou no chat uma chave viva de produção da Clint (prefixo `clint_live_`).
A chave **não foi usada, não foi gravada em arquivo nenhum e não está neste
repositório** — e não está reproduzida aqui de propósito.

Orientação dada: **revogar e gerar outra no painel da Clint**, e não reenviar a nova
pelo chat.

Vale registrar que a chave também **não resolveria nada**: o próprio Pablo havia
escrito, na mensagem anterior, que o MCP da Clint usa OAuth pelo navegador e que não
existe chave de API. Ele estava certo. A chave foi exposta sem ter utilidade aqui.

## Por que a Clint continua desconectada

Verificado nesta sessão: o CLI `claude` existe, mas **não há nenhum servidor MCP em
arquivo de configuração** (`/root/.claude.json` tem a lista vazia). Os conectores
desta sessão vêm da conta claude.ai, não de um `.mcp.json` local. E o passo de
`Authenticate` abre navegador, que esta sessão remota não tem.

Caminho correto, do lado do Pablo: claude.ai → Configurações → Conectores → adicionar
conector personalizado → URL `https://mcp.clint.digital`, tipo HTTP → Conectar e
fazer o login. Aí vale para todas as sessões.

---

# Adendo 3 (12/09, 00h) — a peça vencedora replicada em todos os conjuntos

Pedido do Pablo: *"tenho este mesmo anúncio, com pequena adatação do nicho em cada
conjunto"* + *"ative"*.

## O que foi feito

Reusei o criativo da AG01 (`2374168726451823`) por `creative_id` — o que carrega a arte
E o formulário de lead junto, contornando o `Missing Lead Form (3390001)` que travou
rodadas anteriores — e depois adaptei só o texto de cada um com `update_ad_creative`.

A arte é a mesma nos seis: "acordar com o WhatsApp / cheio de cliente", etiqueta
**AGÊNCIA**, foto de banco. Nenhuma tem a foto do Pablo, nenhuma diz mentoria.

| Conjunto | Anúncio | Criativo | Título |
|---|---|---|---|
| SEMELHANTE CNAE RJ | `120247396147800766` | `2374168726451823` | (texto original da AG01) |
| NICHO IMOBILIARIA | `120247396183900766` | `1394922625417483` | Corretor: cliente novo todo dia |
| NICHO VETERINARIA | `120247396185380766` | `2114940295779170` | Clínica vet: tutor novo todo dia |
| NICHO ODONTOLOGIA | `120247396186930766` | `1547401823790433` | Consultório: paciente novo todo dia |
| NICHO ESTETICA | `120247396192440766` | `1059542513514380` | Estética: cliente novo todo dia |
| NICHO ENERGIA SOLAR | `120247396203200766` | `1623854035819451` | Integrador solar: contato todo dia |

Todos criados pausados, `ads_get_errors` conferido (`[]`), e só então ativados. Os dois
V10 com a foto do Pablo seguem pausados.

`degrees_of_freedom_spec: {}` foi necessário nas seis edições, como sempre.

## O achado da varredura final: 47 anúncios ativos, e os 9 vídeos voltaram

Ao conferir o estado da conta apareceram **V01 a V09 ativos nos dois conjuntos de
formulário**, mais AG02, AG04, AG06, AG07 e AG10. **Não fui eu**: nesta sessão liguei os
12 do nicho, quatro AG, a AG01 do CNAE e as cinco AG01 de nicho. Ou o Pablo ligou tudo
no Gerenciador, ou houve ativação em massa por outra via.

Por que é grave:

1. **Os 9 vídeos são exatamente o que já se provou inútil** — 7 dias, zero lead. O V10
   só foi descoberto como vencedor porque era imagem disfarçada de vídeo no meio deles.
2. **~47 anúncios disputando R$ 30/dia dá R$ 0,64 por anúncio por dia.** Nenhum junta
   volume para o Meta aprender, e a verba se pulveriza em vez de ir para o que converte.

Isso derruba a projeção de 35–45 leads, não sobe.

**Recomendado ao Pablo e aguardando resposta dele:** pausar V01–V09 nos dois conjuntos
(18 anúncios). Não executei por conta própria — mexer em 18 anúncios de uma vez é grande
demais para decidir sozinho, e existe a chance de ter sido ligado de propósito.
