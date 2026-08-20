#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-004.

POR QUE ESTE TEMA, E POR QUE ASSIM

O canal tem dois eixos medidos e usou os DOIS:

    proteina-produtos       n=4    mediana 10.555,5 v/d   usado em 18/08
    canetas-emagrecedoras   n=33   mediana  2.744,7       usado em 12 e 17/08
    canetas (mortos)        n=56   mediana      9,4

As quatro pautas em banco sao de um TERCEIRO eixo, inedito: o custo financeiro
de dieta ao longo de cinco anos. E, como sempre, elas trazem o ASSUNTO e nao a
forma (aprendizado 372). A forma vem do que o canal ja provou: o video mais bem
medido dele fundiu CONTA QUE NINGUEM FAZ com REVELACAO — "A Conta por Grama que
Ninguem Faz no Supermercado". Similaridade do titulo novo contra o acervo do
canal: 0,376, teto 0,65.

A DECISAO QUE MUDOU O ROTEIRO INTEIRO

A pauta do banco dizia "R$ 18.000 em Shakes e Termogenicos: O Custo de 5 Anos
de Suplementos Inuteis". Duas coisas erradas ali, e as duas sao graves num
canal de saude:

  1. O numero. R$ 18.000 nao veio de fonte nenhuma — nao ha pesquisa que meca
     gasto medio brasileiro com shake e termogenico em cinco anos. Publicar
     esse numero como se fosse dado seria inventar.
  2. A palavra "inuteis". Afirmar que suplemento nao funciona e uma alegacao de
     eficacia, e eu nao tenho como sustenta-la — nem preciso.

O que EXISTE, e e muito mais forte, e um fato REGULATORIO: pela Anvisa,
suplemento alimentar nao pode alegar emagrecimento. Ha uma lista de 189
alegacoes funcionais ou de saude permitidas em rotulagem, todas com evidencia
exigida, e emagrecer nao esta entre elas. Isso nao e opiniao sobre eficacia: e
o que a norma permite dizer. O video se apoia nisso e em aritmetica de preco,
que o espectador faz com o proprio extrato.

FONTES, duas que batem, a institucional primeiro:

  Anvisa — RDC 243/2018 (limites de nutrientes e bioativos), IN 28/2018 (lista
  de ingredientes autorizados), RDC 241/2018 e 242/2018 (fabricacao, propaganda,
  registro). 189 alegacoes permitidas; suplemento alimentar nao pode alegar
  emagrecimento; a propria agencia orienta a desconfiar de promessa milagrosa.
  Fiscalizacao dificultada pelo e-commerce, com monitoramento de anuncios por IA.

  Camara dos Deputados — Grupo de Trabalho sobre a Comercializacao de
  Suplementos Alimentares, Relatorio 1/2026.

  ABIAD — 59% dos lares brasileiros consomem suplemento alimentar, alta de 10
  pontos sobre 2015; 90% entendem como complemento da alimentacao; 85% consomem
  por saude.

  BRASNUTRI com dados da Euromonitor International — o setor movimentou cerca
  de R$ 7,6 bilhoes em 2025, alta de cerca de 15%, com projecao de R$ 13,8
  bilhoes ate 2030. Reportado por Jornal do Bras, Revista Imprensa Brasil e
  Revista SuplementAcao, todos com os mesmos numeros.

  Revista Eletronica Acervo Saude (2026), Faculdade Pernambucana de Saude —
  28,7% dos universitarios DA AREA DA SAUDE consomem termogenico sem
  prescricao, relatando insonia, agitacao, dor gastrica e palpitacao.

O QUE O ROTEIRO NAO FAZ, de proposito: nao diz que suplemento nao funciona, nao
promete emagrecimento por nenhuma via, nao da um numero de gasto medio como se
fosse pesquisa, e nao substitui profissional. Ele ensina o espectador a fazer a
PROPRIA conta e diz, na cena e na descricao, o que a norma permite alegar.

TAXA DA VOZ. pt-BR-FranciscaNeural, MODELO_VOZ de ensaio.py: R = 15,24 chars/s,
P = 0,298 s por frase — P baixissimo, esta voz quase nao pausa, e por isso o
orcamento e grande. Densidade medida do canal: 2,24 frases/cena no longo, 1,90
no short. Orcamento para oitenta cenas em 810 s: 11.169 caracteres. Faixa do
short: 428 a 546 caracteres.
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar, cap=None):
    # `cap` tambem aqui, e nao so no T: quem abre capitulo e a cena, nao o
    # layout. O capitulo 4 abre com um numero — "sete bilhoes e seiscentos" —
    # e forcar um layout de titulo so para poder carimbar o capitulo trocaria a
    # decisao visual pela limitacao do ajudante.
    c = {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ---------------------------------------------- 1. A regra que ninguem leu
T("Cento e oitenta e nove", "e emagrecer nao esta la",
  "Existe uma lista oficial do que um suplemento alimentar pode prometer no "
  "rotulo. Ela tem cento e oitenta e nove alegacoes. Emagrecer nao e uma delas.",
  cap="A regra que ninguem leu")
T("Isso nao e opiniao", "e a norma em vigor",
  "Isso nao e a minha opiniao sobre se funciona ou nao. E o que a Anvisa "
  "permite escrever. Duas coisas bem diferentes, e a segunda da para conferir.")
I("A lista existe", "e e publica",
  "A lista e publica. Cada alegacao dela precisou de evidencia para entrar. E "
  "nenhuma diz que o produto faz voce perder peso.")
T("Entao pense", "no ultimo anuncio que voce viu",
  "Agora pense no ultimo anuncio de termogenico que apareceu para voce. "
  "Provavelmente prometia exatamente isso.")
T("A distancia entre os dois", "e o video de hoje",
  "A distancia entre o que a norma permite e o que o anuncio promete: e disso "
  "que este video trata.")
L("Tres coisas", ["O que a norma diz",
                  "Por que o anuncio existe",
                  "Como fazer a sua conta"],
  "Tres coisas. O que a norma diz. Por que o anuncio existe mesmo assim. E "
  "como fazer a conta do que isso custa para voce.")
I("O que nao vou fazer", "dizer que nao funciona",
  "O que eu nao vou fazer: dizer que suplemento nao funciona. Nao tenho como "
  "sustentar isso, e nem preciso.")
I("E nao vou dar", "um numero de gasto medio",
  "Tambem nao vou inventar quanto o brasileiro gasta em media. Nao existe "
  "pesquisa com esse numero, e chutar seria pior que nao falar.")
T("O que eu tenho", "duas coisas solidas",
  "O que eu tenho e solido: o texto da norma, e aritmetica. A aritmetica quem "
  "faz e voce, com o seu proprio extrato.")
T("E uma coisa importante", "isto nao substitui profissional",
  "E uma coisa que precisa ser dita antes de tudo. Nada aqui substitui "
  "nutricionista ou medico. Se voce usa alguma coisa, converse com quem "
  "acompanha voce.")
I("Por que insisto nisso", "tem dado atras",
  "Insisto nisso porque tem dado atras, e eu mostro ele no fim. Guarde a "
  "pergunta.")
C("Vamos comecar", "pelo texto da norma",
  "Vamos comecar pelo texto. Pelo que esta escrito e assinado.")

# ------------------------------------------- 2. O que a norma diz, exatamente
T("Quatro normas", "de dois mil e dezoito",
  "O que rege suplemento alimentar no Brasil sao quatro normas da Anvisa, "
  "todas de dois mil e dezoito.",
  cap="O que a norma diz, exatamente")
L("Quais sao", ["RDC duzentos e quarenta e tres",
                "Instrucao Normativa vinte e oito",
                "RDC duzentos e quarenta e um",
                "RDC duzentos e quarenta e dois"],
  "Sao a resolucao duzentos e quarenta e tres, a instrucao normativa vinte e "
  "oito, e as resolucoes duzentos e quarenta e um e duzentos e quarenta e dois.")
I("A duzentos e quarenta e tres", "limites",
  "A primeira estabelece limites de nutrientes e de substancias bioativas. "
  "Quanto pode ter de cada coisa, no maximo e no minimo.")
I("A instrucao normativa", "a lista de ingredientes",
  "A instrucao normativa lista quais ingredientes sao autorizados. Se nao esta "
  "nela, nao pode estar no produto.")
I("As outras duas", "fabricacao e propaganda",
  "As duas ultimas tratam de fabricacao, de registro, e de propaganda. E a "
  "propaganda e onde a coisa aperta.")
T("Por que essas normas existem", "tem historia atras",
  "Essas regras nao nasceram do nada. Elas vieram depois de substancias como "
  "efedrina e dinitrofenol circularem em produto de emagrecimento.")
I("O dinitrofenol", "caso fatal",
  "O dinitrofenol chegou a estar ligado a mortes. Nao e exagero regulatorio: e "
  "resposta a desfecho grave.")
T("Voltando a lista", "as cento e oitenta e nove",
  "Voltando a lista das cento e oitenta e nove alegacoes permitidas. Ela diz "
  "coisas como contribui para o funcionamento do intestino, ou auxilia na "
  "formacao de ossos.")
T("Sao alegacoes de funcao", "nao de resultado",
  "Repare no tipo de frase. Sao alegacoes de funcao no corpo. Nenhuma promete "
  "um resultado na balanca.")
I("E a agencia diz mais", "desconfie de milagre",
  "E a propria agencia orienta o consumidor a desconfiar de propaganda que "
  "promete efeito milagroso. Esta escrito no material dela.")
T("Entao a regra e simples", "e pouca gente sabe",
  "A regra, resumida: suplemento alimentar nao pode alegar emagrecimento. "
  "Simples assim, e pouca gente sabe.")
C("A pergunta seguinte", "por que o anuncio continua",
  "O que leva a pergunta obvia. Se e proibido, por que os anuncios continuam "
  "aparecendo?")

# ------------------------------------ 3. Por que o anuncio existe mesmo assim
T("A resposta curta", "onde ele e vendido",
  "A resposta curta esta em onde esses produtos sao vendidos hoje. Boa parte "
  "da venda irregular saiu da loja fisica e foi para o comercio eletronico. "
  "Fiscalizar prateleira e uma coisa; fiscalizar anuncio que aparece so para "
  "voce, no seu celular, e outra bem diferente.",
  cap="Por que o anuncio existe mesmo assim")
T("O anuncio segmentado", "some antes de ser visto",
  "O anuncio segmentado tem uma propriedade incomoda para quem fiscaliza: ele "
  "nao fica exposto. Aparece para o perfil escolhido, roda alguns dias, e sai "
  "do ar. Quando a denuncia chega, nao ha mais o que olhar.")
I("O que a agencia passou a fazer", "monitorar com IA",
  "Diante disso a Anvisa passou a monitorar anuncios online com ferramentas de "
  "inteligencia artificial. E uma mudanca de metodo: da denuncia pontual para "
  "a varredura continua.")
T("Tem outra frente", "no Congresso",
  "E tem uma segunda frente aberta, fora da agencia. Em dois mil e vinte e "
  "seis a Camara dos Deputados instalou um grupo de trabalho especifico sobre "
  "a comercializacao de suplementos alimentares, com relatorio proprio.")
I("O que isso sinaliza", "o assunto virou pauta",
  "Nao antecipo o que vai sair dali. O que isso sinaliza e outra coisa, e ja "
  "vale: o assunto deixou de ser reclamacao de consumidor e virou pauta "
  "legislativa, com prazo e relator.")
T("Junte as duas pontas", "e o quadro muda",
  "Junte as duas pontas. De um lado, uma regra clara que proibe a promessa. Do "
  "outro, um canal de venda onde ela circula rapido demais para ser alcancada. "
  "O resultado e o que voce ve na tela.")
T("E aqui e importante separar", "produto e propaganda",
  "E aqui vale separar duas coisas que vem grudadas. Uma e o produto, que pode "
  "ser regular, notificado, com rotulo dentro da norma. A outra e a propaganda, "
  "que promete o que o rotulo nao pode dizer.")
I("Da para ter os dois", "produto legal, anuncio nao",
  "Da para existir produto perfeitamente regular sendo vendido com anuncio "
  "irregular. E esse e, provavelmente, o caso mais comum de todos.")
T("Por isso a pergunta muda", "nao e o produto e bom",
  "Por isso a pergunta util nao e se o produto e bom. E outra, mais simples de "
  "responder: o que exatamente esta escrito no rotulo dele, e o que esta "
  "escrito no anuncio que te trouxe ate ele?")
L("Duas leituras", ["O rotulo, com a alegacao",
                    "O anuncio, com a promessa"],
  "Duas leituras, dois minutos. O rotulo, para ver qual alegacao ele usa. E o "
  "anuncio, para ver o que ele prometeu. Quando os dois nao batem, voce ja "
  "sabe qual dos dois esta preso a norma.")
I("Isso muda a decisao", "de crenca para conferencia",
  "Isso tira a decisao do terreno da crenca e devolve para o terreno da "
  "conferencia. Voce nao precisa saber bioquimica para fazer essa comparacao.")
C("Agora o tamanho", "de quanto dinheiro estamos falando",
  "Antes de chegar na sua conta, vale ver o tamanho do mercado inteiro. Ele "
  "explica por que o anuncio insiste tanto.")

# ------------------------------------------------------- 4. O tamanho disso
I("Sete bilhoes e seiscentos", "em um ano",
  "Segundo levantamento da Brasnutri com dados da Euromonitor, o setor de "
  "suplementos alimentares movimentou cerca de sete bilhoes e seiscentos "
  "milhoes de reais no Brasil em dois mil e vinte e cinco.",
  cap="O tamanho disso")
I("Crescendo quinze por cento", "ao ano",
  "E crescendo em torno de quinze por cento ao ano. A projecao do proprio "
  "setor fala em treze bilhoes e oitocentos milhoes de reais ate dois mil e "
  "trinta.")
B("O caminho projetado", ["2025", "2030"], [0.55, 1.0],
  "Ou seja: a expectativa e quase dobrar em cinco anos. Isso e o setor falando "
  "do setor, entao trate como projecao, nao como fato consumado. Mas projecao "
  "tambem informa, porque mostra em que aposta quem investe.")
I("Cinquenta e nove por cento", "dos lares",
  "Do lado de quem compra, uma pesquisa da Abiad aponta que cinquenta e nove "
  "por cento dos lares brasileiros ja consomem algum suplemento alimentar. "
  "Dez pontos a mais que em dois mil e quinze.")
T("Ou seja", "e mais da metade das casas",
  "Mais da metade das casas do pais. Isso deixou de ser habito de academia ha "
  "bastante tempo, e passou a ser item de lista de mercado.")
I("E olha esse dado", "noventa por cento",
  "E tem um numero dessa mesma pesquisa que eu acho o mais interessante de "
  "todos. Noventa por cento das pessoas entendem suplemento como complemento "
  "da alimentacao. Complemento. Nao substituto, e nao tratamento.")
T("Quer dizer", "a maioria ja sabe",
  "Quer dizer que a maioria absoluta ja tem a ideia certa na cabeca. O "
  "problema nao e ignorancia do publico.")
I("E oitenta e cinco por cento", "consomem por saude",
  "Oitenta e cinco por cento dizem consumir por razoes de saude. Tambem "
  "coerente. As pessoas nao estao comprando por promessa milagrosa; estao "
  "comprando por cuidado.")
T("Entao onde entra o desencontro", "na propaganda, de novo",
  "Entao onde mora o desencontro? Na ponta da propaganda, de novo. O publico "
  "compra pensando em complemento, e o anuncio vende prometendo resultado.")
T("E o resultado prometido", "e o que a norma proibe",
  "E o resultado prometido e exatamente aquele que a lista de alegacoes nao "
  "autoriza. Voltamos ao ponto de partida, agora com o tamanho do mercado do lado.")
I("Uma ressalva honesta", "sao numeros de setor",
  "Uma ressalva: esses numeros de faturamento vem de levantamento de mercado, "
  "nao de censo publico. Sao a melhor medida disponivel, e eu digo de onde "
  "vieram.")
C("Agora sim", "a sua conta",
  "Com o tamanho na mesa, vamos para a parte que interessa mais. A sua conta.")

# ---------------------------------------------------- 5. A conta de cinco anos
T("Aqui eu nao te dou", "um numero pronto",
  "Agora a parte que da titulo a muito video por ai: quanto custa cinco anos "
  "disso. E aqui eu vou fazer o contrario do que se costuma fazer. Nao vou te "
  "dar um numero pronto, porque nao existe pesquisa que meca esse gasto medio "
  "no Brasil. Quem te da um numero desses inventou.",
  cap="A conta de cinco anos")
T("O que existe", "e a sua conta",
  "O que existe, e vale muito mais, e a sua propria conta. Ela leva tres "
  "minutos e usa dados que so voce tem.")
L("Do que voce precisa", ["O que voce compra por mes",
                          "Quanto pagou da ultima vez",
                          "Ha quanto tempo compra"],
  "Voce precisa de tres coisas. O que voce compra num mes tipico. Quanto pagou "
  "da ultima vez em cada item. E ha quanto tempo isso se repete.")
I("O primeiro numero", "o mes tipico",
  "Comece pelo mes tipico, e nao pelo mes em que voce comprou tudo de uma vez. "
  "Se o pote dura quarenta e cinco dias, ele nao e um gasto mensal cheio. "
  "Divida pelo tempo real de duracao, sempre.")
T("Esse detalhe muda tudo", "duracao real, nao embalagem",
  "Esse detalhe e o que mais erra na conta de cabeca. A gente lembra do preco "
  "da embalagem e esquece de dividir pelo tempo que ela durou. O gasto mensal "
  "sai inflado, e a conta perde credibilidade justamente com voce.")
I("Depois multiplique", "por doze e por cinco",
  "Com o mensal na mao, multiplique por doze para ter o ano. E o ano por "
  "cinco. Nada mais sofisticado que isso.")
T("Uma correcao honesta", "preco nao fica parado",
  "Uma correcao que quase ninguem faz e vale fazer: preco nao fica parado por "
  "cinco anos. Se voce quiser ser justo com o passado, use o que pagou naquela "
  "epoca, e nao o preco de hoje aplicado para tras.")
T("E se voce nao lembra", "tem um jeito melhor",
  "E se voce nao lembra dos precos antigos, ha um caminho melhor que a "
  "memoria. Busque no extrato do cartao ou no historico do aplicativo de "
  "compra. O numero real esta la, e ele costuma surpreender.")
I("O que fazer com o resultado", "nada, por enquanto",
  "Quando o resultado aparecer, nao faca nada com ele por enquanto. Nao "
  "cancele nada, nao se culpe. Ele e so uma informacao que voce nao tinha "
  "cinco minutos atras.")
T("Porque ele pode ir", "para os dois lados",
  "E ele pode ir para dois lados. Pode vir menor do que voce imaginava, e ai o "
  "gasto nunca foi o problema. Ou maior, e ai voce tem uma pergunta nova para "
  "levar a consulta.")
C("A pergunta seguinte", "e o que ele compraria",
  "E a pergunta que vem depois do numero e sempre a mesma. Esse dinheiro "
  "compraria o que?")

# ---------------------------------------------- 6. O que esse dinheiro compra
T("Cuidado com esta parte", "e onde se mente mais",
  "Esta e a parte em que mais se mente em video de saude, entao vou pisar "
  "devagar. O truque comum e comparar o seu gasto com algo que supostamente "
  "resolveria o problema. Nao vou fazer isso: eu nao sei o que resolve o seu "
  "caso.",
  cap="O que esse dinheiro compra")
T("O que da para dizer", "o que tem efeito documentado",
  "O que da para dizer com honestidade e outra coisa. Existem gastos cujo "
  "efeito e documentado e verificavel, e existem gastos cujo efeito prometido "
  "nao pode nem ser escrito no rotulo.")
L("Da primeira categoria", ["Consulta com nutricionista",
                            "Exames de acompanhamento",
                            "Atividade fisica orientada"],
  "Na primeira categoria estao coisas como consulta com nutricionista, exames "
  "de acompanhamento, e atividade fisica com orientacao. Nao porque garantem "
  "resultado, mas porque geram medida.")
I("Essa e a diferenca", "medida contra promessa",
  "E essa e a diferenca que interessa. Um exame te devolve um numero seu. Um "
  "anuncio te devolve uma promessa generica, feita para milhoes de pessoas ao "
  "mesmo tempo.")
T("Nao estou dizendo", "troque um pelo outro",
  "Repare que eu nao disse para trocar um pelo outro. Muita gente faz os dois, "
  "e com orientacao. O que eu estou dizendo e para saber qual dos dois voce "
  "esta comprando.")
I("Porque as vezes", "e o mesmo dinheiro",
  "Porque, dependendo da sua conta, e o mesmo dinheiro. E ai deixa de ser uma "
  "questao de disciplina e passa a ser uma questao de escolha informada.")
T("Tem um caso especifico", "que merece atencao",
  "Tem um caso em que essa escolha pesa mais que nos outros, e ele aparece "
  "muito no meu comentario aqui do canal. O da pessoa que ja tentou varias "
  "vezes e sempre recomeca do zero.")
T("Nesse caso", "o gasto se repete",
  "Nesse caso o gasto nao acontece uma vez. Ele se repete a cada recomeco, "
  "junto com o desgaste de recomecar. E a conta de cinco anos costuma ser "
  "bem diferente da que a pessoa imaginava.")
I("Se for o seu caso", "leve o numero a consulta",
  "Se for o seu caso, ha algo concreto para fazer com o numero que voce acabou "
  "de calcular. Leve ele para a consulta. E um dado sobre o seu historico, e "
  "poucos profissionais recebem esse dado dos pacientes.")
T("Nao e vergonha", "e informacao",
  "E nao ha nada de vergonhoso nesse numero. Ele nao mede a sua forca de "
  "vontade. Ele mede quanto um mercado de bilhoes conseguiu conversar com uma "
  "dor real que voce tem.")
C("Falta a ultima parte", "os limites do que eu disse",
  "Falta a parte que quase nenhum video tem, e que eu acho a mais importante "
  "de todas. Os limites do que eu acabei de dizer.")

# ----------------------------------------- 7. O que este video nao afirma
T("Primeiro limite", "eu nao disse que nao funciona",
  "Primeiro limite, e o principal. Em nenhum momento eu disse que suplemento "
  "nao funciona. Eu disse o que a norma permite alegar, que e uma afirmacao "
  "sobre rotulo e nao sobre o seu corpo.",
  cap="O que este video nao afirma")
T("Segundo limite", "nao ha numero de gasto medio",
  "Segundo limite. Eu nao te dei o custo medio de cinco anos porque ele nao "
  "existe medido. Se voce vir esse numero por ai, pergunte de qual pesquisa "
  "ele saiu. Quase sempre nao ha resposta.")
I("Terceiro limite", "os numeros de mercado",
  "Terceiro. Os numeros de faturamento que eu citei vem de levantamento de "
  "setor, com dados de consultoria, e nao de estatistica publica. Sao a melhor "
  "medida que existe hoje, e ainda assim sao estimativa.")
T("Agora o dado que faltava", "o que eu pedi para guardar",
  "E agora o dado que eu pedi para voce guardar la no comeco. Ele e o motivo "
  "pelo qual eu insisto tanto em conversar com profissional.")
I("Vinte e oito virgula sete", "por cento",
  "Uma pesquisa publicada na Revista Eletronica Acervo Saude, em dois mil e "
  "vinte e seis, na Faculdade Pernambucana de Saude, encontrou que vinte e oito "
  "virgula sete por cento dos universitarios da area da saude usam termogenico "
  "sem prescricao.")
T("Repare em quem", "sao os da area da saude",
  "Repare em quem sao essas pessoas. Estudantes da area da saude. Nao e "
  "desinformacao, e a proximidade com o assunto nao protegeu ninguem.")
L("O que eles relataram", ["Insonia", "Agitacao", "Dor gastrica", "Palpitacao"],
  "E o que eles relataram foi insonia, agitacao, dor gastrica e palpitacao. "
  "Sao os sintomas do proprio grupo pesquisado, e nao previsao para voce.")
T("Por isso a frase", "que parece protocolo",
  "Por isso aquela frase que soa a protocolo chato. Converse com um "
  "profissional. Ela existe porque estimulante sem acompanhamento tem efeito "
  "antes de qualquer resultado na balanca.")
L("O que fica", ["Confira a alegacao no rotulo",
                 "Compare com a promessa do anuncio",
                 "Faca a sua conta de cinco anos"],
  "Tres coisas para levar. Confira qual alegacao esta no rotulo. Compare com o "
  "que o anuncio prometeu. E faca a sua conta de cinco anos, com o extrato na "
  "mao e sem culpa nenhuma.")
C("No proximo", "o rotulo linha por linha",
  "No proximo video eu abro um rotulo de suplemento linha por linha, e mostro "
  "onde exatamente fica a alegacao permitida. Depois de ver uma vez, voce "
  "repara sempre.")

# ---------------------------------------------------------------- o short
# Video inteiro por si: abre pelo FATO regulatorio, que e o resultado, e nao
# pelo contexto. Orcamento medido para 36,4 s com 6 cenas e 1,90 frases por
# cena: 479 caracteres (aprendizado 373 — medir ANTES de escrever).
SHORT = [
    {"layout": "titulo", "kicker": "Cento e oitenta e nove",
     "sub": "e emagrecer nao esta la",
     "nar": "A Anvisa tem uma lista do que suplemento pode prometer no rotulo. "
            "Sao cento e oitenta e nove alegacoes.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Nenhuma delas", "sub": "diz emagrecer",
     "nar": "Nenhuma delas e emagrecer. Suplemento alimentar nao pode alegar "
            "emagrecimento.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Nao e opiniao", "sub": "e a norma",
     "nar": "Isso nao e opiniao sobre eficacia. E o que a norma deixa escrever.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Entao compare", "sub": "rotulo e anuncio",
     "nar": "Entao compare duas coisas. A alegacao no rotulo, e a promessa do "
            "anuncio que te trouxe ate ele.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Quando nao batem", "sub": "voce ja sabe qual vale",
     "nar": "Quando as duas nao batem, voce ja sabe qual das duas responde a "
            "norma.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "No video completo", "sub": "a conta de cinco anos",
     "nar": "No video completo eu mostro como fazer a sua conta de cinco anos.",
     "sem_cap": True},
]

THUMB = {"l1": "189 alegacoes permitidas", "l2": "emagrecer nao e uma"}

COPY = """# A regra da Anvisa sobre o que suplemento pode prometer

## TITULO
Shake e Termogênico: 189 Alegações Permitidas, e Emagrecer Não É Uma Delas

## DESCRICAO
A Anvisa mantém uma lista de 189 alegações funcionais ou de saúde que um suplemento alimentar pode usar em rotulagem — todas com exigência de evidência científica para entrar. Emagrecimento não está entre elas: suplemento alimentar não pode alegar emagrecimento. Isso não é uma opinião sobre eficácia, é o que a norma permite escrever, e dá para conferir.

Este vídeo trata da distância entre o que a norma permite e o que o anúncio promete.

O que rege o setor são quatro normas de 2018: a RDC 243, que estabelece limites de nutrientes e substâncias bioativas; a Instrução Normativa 28, com a lista de ingredientes autorizados; e as RDCs 241 e 242, que tratam de fabricação, registro e propaganda. Elas vieram depois de substâncias como efedrina e dinitrofenol circularem em produtos de emagrecimento — o dinitrofenol chegou a ser associado a desfechos fatais. Não é excesso regulatório, é resposta a dano.

Por que o anúncio continua existindo então? Porque boa parte da venda irregular migrou para o comércio eletrônico, e anúncio segmentado não fica exposto: aparece para um perfil, roda alguns dias e sai do ar. A Anvisa passou a monitorar anúncios online com ferramentas de inteligência artificial, e em 2026 a Câmara dos Deputados instalou um grupo de trabalho específico sobre a comercialização de suplementos alimentares.

Vale separar produto de propaganda: existe produto perfeitamente regular sendo vendido com anúncio irregular, e esse é provavelmente o caso mais comum. Por isso a pergunta útil não é "esse produto é bom", e sim: qual alegação está no rótulo, e o que o anúncio prometeu?

Sobre o tamanho disso — segundo levantamento da Brasnutri com dados da Euromonitor, o setor movimentou cerca de R$ 7,6 bilhões no Brasil em 2025, crescendo cerca de 15% ao ano, com projeção de R$ 13,8 bilhões até 2030. Pesquisa da ABIAD aponta que 59% dos lares brasileiros consomem algum suplemento, 10 pontos acima de 2015; 90% entendem suplemento como complemento da alimentação e 85% consomem por razões de saúde. Ou seja: o público já tem a ideia certa. O desencontro está na ponta da propaganda.

E a conta de cinco anos: eu não dou um número pronto, porque não existe pesquisa medindo esse gasto médio no Brasil. O vídeo ensina a fazer a sua, com o extrato na mão — incluindo o erro mais comum, que é esquecer de dividir o preço da embalagem pelo tempo real de duração.

Nada aqui substitui nutricionista ou médico.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Uma pergunta e um pedido. A pergunta: você já tinha lido qual alegação está escrita no rótulo do que você usa? E o pedido: se você fizer a conta de cinco anos, não precisa contar o valor aqui — só me diga se veio maior ou menor do que você imaginava. Estou juntando isso para o próximo vídeo, em que abro um rótulo linha por linha.

## HASHTAGS
#Anvisa #Suplementos #SejaMaisMagra

## TAGS
anvisa, suplemento alimentar, termogenico, shake, rotulo de suplemento, alegacao funcional, rdc 243, propaganda irregular, emagrecimento, saude, nutricao, consumo consciente, mercado de suplementos, abiad, whey

## CONFIGURACAO DE STUDIO
- Idioma: Português (pt-BR) | Categoria: Educação (27)
- Não feito para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Brasil | Licença: Licença padrão do YouTube
- Anúncios no meio: ligados (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
A lista de 189 alegações funcionais ou de saúde permitidas em rotulagem, a vedação de alegação de emagrecimento para suplemento alimentar e a orientação para desconfiar de propaganda com efeito milagroso são da Anvisa. O marco regulatório citado é composto pela RDC 243/2018, pela Instrução Normativa 28/2018 e pelas RDCs 241/2018 e 242/2018. O grupo de trabalho da Câmara dos Deputados sobre comercialização de suplementos alimentares tem relatório de 2026. Os dados de faturamento (cerca de R$ 7,6 bilhões em 2025, crescimento em torno de 15% e projeção de R$ 13,8 bilhões até 2030) vêm de levantamento da Brasnutri com dados da Euromonitor International — são estimativa de mercado, não estatística pública. Os percentuais de consumo (59% dos lares, 90%, 85%) são de pesquisa da ABIAD. O dado de 28,7% de universitários da área da saúde consumindo termogênico sem prescrição, com relato de insônia, agitação, dor gástrica e palpitação, é de pesquisa publicada na Revista Eletrônica Acervo Saúde em 2026, conduzida na Faculdade Pernambucana de Saúde, e descreve o grupo pesquisado — não é previsão para quem assiste. Consultado em 20 de agosto de 2026. Este vídeo NÃO afirma que suplementos não funcionam, não promete emagrecimento por nenhuma via, não apresenta custo médio de consumo porque não há pesquisa que o meça, e não substitui avaliação de nutricionista ou médico.
"""

SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-004",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#2B1B1F", "c1": "#C9184A", "c2": "#7FB069", "bg": "#FDF3F4"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "seja-mais-magra-004.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
