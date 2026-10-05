"""nivel-do-jogo-010 — quanto você já gastou em moeda e passe este ano.

ALAVANCA ATACADA: A (travessia short -> longo). E este canal e a TERCEIRA
confirmacao independente do aprendizado 577, no mesmo dia que a segunda.

O NUMERO DE PARTIDA, lado a lado:

    pacote  short  longo   o que o longo responde
    004      100     21    EA FC 27: Standard, Ultimate ou Plus? a conta em
                           reais ANTES de comprar  <- MELHOR LONGO
    005       11      8    Steam mudou como seu jogo e precificado
    007        4      8    loja em reais, cartao em dolar ou gift card?
    003      250      4    preco dos jogos: quantas horas de trabalho custa
                           <- MAIOR SHORT DO CANAL
    009        6      3    reembolso: sao dois prazos, nao um
    008       15      2    se tivesse comprado em vez de assinar
    006        6      0    demissoes nos games: a Square Enix vendeu 8% menos

O MAIOR short do canal, 250 views, entregou QUATRO views de longo. O MELHOR
longo, 21 views, veio de um short de 100 — dois quintos do alcance, cinco vezes
o resultado. E o unico pacote com ZERO views de longo e o unico que entrega
FATO sobre a industria: demissoes na Square Enix.

Tres canais, tres idiomas, quarenta e tres pacotes, mesmo sinal: epomeno
(1.614 -> 110 contra 540 -> 431), kolejny (287 -> 21 contra 27 -> 103) e agora
nivel-do-jogo (250 -> 4 contra 100 -> 21). Alcance de short nao compra
travessia. Aprendizados 577 e 578.

O QUE DEU CERTO: "a conta em reais ANTES de comprar" — decisao do espectador,
com numero dele, antes de gastar.
O QUE NAO DEU: constatacao sobre a industria (zero views de longo) e o short de
maior alcance, que falava de horas de trabalho em abstrato.
O QUE VOU MUDAR: a conta vem do HISTORICO DE COMPRAS do proprio espectador, que
e uma pagina que ele abre em dez segundos, e responde uma decisao com prazo: o
proximo passe, que expira.

EIXO, e por que ele e novo. Os sete anteriores falam de edicao de jogo (004),
precificacao regional da Steam (005), moeda de pagamento e gift card (007),
preco em horas de trabalho (003), prazo de reembolso (009), assinar contra
comprar (008) e demissoes (006). Nenhum fala do que ele JA GASTOU em moeda do
jogo e passe. O game-money-lab tocou moeda interna no 006 dele, mas e outro
canal, outro idioma e outra pergunta: la era quanto vale a moeda, aqui e quanto
voce ja pagou.

VEREDITO: `canal frio` (v_maquina_licoes, 04/10/2026) — eixo novo e piso de oito
minutos por analogia com `suspenso`. Com oito capitulos e o MARGEM_CAP o minimo
aritmetico ja e 514 s, entao o alvo fica logo acima.

ALAVANCA B com a licao 575 aplicada de saida: a `pt-BR-AntonioNeural` tem
residuo de mais dois virgula oito por cento no ensaio.py. Residuo POSITIVO, o
mesmo tipo que custou dois virgula dois segundos no seja-mais-magra-009, entao a
resposta foi posicionada pela estimativa CORRIGIDA e com folga deliberada.

TITULO PROPRIO DO SHORT: tem. Similaridade maxima contra o corpus de cento e
quarenta e seis titulos: zero virgula quatrocentos e catorze.

NOTA DE RODADA: esta spec foi escrita numa rodada em que o render estava
indisponivel — jobs do GitHub aceitos, nenhum runner atribuido, cancelados aos
quinze minutos (aprendizado 580). Escrever spec nao precisa de runner, entao a
rodada entregou o que podia entregar: dois pacotes prontos para render em vez de
um, para quando a capacidade voltar.
"""

import json

CENAS = []

# Resolvidos por `pg_net` dentro do Postgres (aprendizado 574).
BROLL = {
    4267433: ("https://videos.pexels.com/video-files/4267433/4267433-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/man-pressing-gaming-controller-4267433/"),
    7534262: ("https://videos.pexels.com/video-files/7534262/7534262-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/person-holding-credit-card-7534262/"),
    6257825: ("https://videos.pexels.com/video-files/6257825/6257825-hd_1366_720_24fps.mp4",
              "ArtHouse Studio",
              "https://www.pexels.com/video/man-touch-typing-on-phone-6257825/"),
    6672502: ("https://videos.pexels.com/video-files/6672502/6672502-hd_1280_720_24fps.mp4",
              "Andy Barbour",
              "https://www.pexels.com/video/a-person-writing-6672502/"),
    5717468: ("https://videos.pexels.com/video-files/5717468/5717468-hd_1280_720_25fps.mp4",
              "Polina",
              "https://www.pexels.com/video/writting-in-a-notebook-5717468/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ===================== OS PRIMEIROS DUZENTOS SEGUNDOS =======================

# -------------------------------------------------------------------- cap 1
T("Existe um número", "que você nunca somou",
  "Existe um número seu que você nunca somou: quanto saiu da sua conta este "
  "ano em moeda de jogo, passe e pacote. Ele está escrito.",
  cap="O número que existe e que ninguém soma")
T("Não é estimativa", "é recibo",
  "E não é estimativa. São recibos, com data e valor, numa página que você "
  "abre em dez segundos.")
T("Por que ninguém soma", "porque sai em pedaços",
  "Ninguém soma porque não sai de uma vez: sai em pedaços de cinco, de dez, "
  "de trinta reais, e cada um parece pequeno.")
B("E a memória", "conta sempre menos",
  "A memória também não ajuda: ela lembra da compra grande e esquece as "
  "pequenas, que são justamente as que se repetem.",
  "person pressing a gaming controller", 4267433)
T("O que isso custa", "decisão, não dinheiro",
  "Isso custa decisão: você decide o próximo passe comparando com um número "
  "que não existe.")
T("Não é falta de controle", "é falta de total",
  "Não é falta de controle e não é vergonha nenhuma. É um total que ninguém "
  "calculou, e total se calcula.")
T("Nenhum número meu", "em todo o vídeo",
  "Não tem número meu aqui. Nenhuma média, nenhum limite recomendado, nenhum "
  "nome de loja. Os dois números saem do seu histórico.")
T("O prazo é seu", "o passe que está acabando",
  "O prazo também é seu: a temporada que está terminando, com o passe que você "
  "vai decidir comprar ou não dentro de dias.")

# -------------------------------------------------------------------- cap 2
T("Por que não parece dinheiro", "três motivos de desenho",
  "Três coisas no desenho da compra fazem o gasto não parecer gasto. Vale "
  "conhecer as três, porque é por elas que o total surpreende.",
  cap="Por que a moeda do jogo não parece dinheiro")
T("A primeira", "você compra duas vezes",
  "A primeira: você compra duas vezes. Dinheiro por moeda, moeda por item. Só "
  "a primeira é gasto, e é a que se esquece.")
T("A segunda", "os pacotes não fecham",
  "A segunda: os pacotes de moeda não fecham com o preço do item. Sobra um "
  "resto guardado, e o resto puxa a próxima compra.")
B("A terceira", "o cartão já está salvo",
  "A terceira: o cartão já está salvo, e compra sem digitar nada não tem o "
  "instante em que você olha o valor.",
  "person holding a credit card", 7534262)
T("Juntas", "elas transformam gasto em rotina",
  "Juntas, as três transformam gasto em rotina. E rotina só aparece no total, "
  "nunca na compra.")
T("E o total existe", "a loja guarda tudo",
  "E o total existe mesmo assim, porque a loja guarda cada recibo. Ela precisa "
  "guardar, e isso trabalha a seu favor agora.")
T("Não é armadilha", "é desenho comum",
  "Nada disso é armadilha. É desenho comum de loja digital, igual ao da "
  "cafeteria que vende cartão pré-pago.")
T("O que vem agora", "a conta, em dois passos",
  "O que vem agora é a conta. Dois passos, e nada além do histórico que já é "
  "seu.")

# -------------------------------------------------------------------- cap 3
T("Passo um", "abra o histórico de compras",
  "Passo um: abra o histórico de compras da loja onde você joga. Console, "
  "Steam ou celular, todos têm.",
  cap="A conta: o histórico do ano e uma divisão")
T("Filtre o ano", "e só o que é moeda ou passe",
  "Filtre do primeiro dia do ano até hoje e marque só moeda, passe, pacote ou "
  "item. Jogo inteiro fica de fora.")
T("Some tudo", "inclusive os de cinco reais",
  "Some todos, inclusive os de cinco reais. São eles que mudam o total, porque "
  "são muitos.")
T("Esse é o primeiro número", "o total do ano",
  "Esse total é o seu primeiro número: quanto você já colocou em moeda e "
  "passe neste ano.")
T("Passo dois", "divida pelos meses",
  "Passo dois: divida pelo número de meses que já passaram. Não por doze.")
T("O resultado", "é o seu valor por mês",
  "O resultado é o seu gasto por mês nessa categoria. E é esse número que você "
  "compara com o preço do próximo passe, não o preço dele sozinho.")
T("Por que jogo fica fora", "porque não repete",
  "Voltando ao filtro: jogo inteiro fica de fora porque não repete. O que "
  "estamos medindo é o gasto que volta, e é ele que decide a próxima compra.")
T("E um detalhe do filtro", "assinatura entra, jogo não",
  "Um detalhe do filtro que muda o total: assinatura mensal de serviço entra "
  "na conta, porque repete igual ao passe. O que fica de fora é só jogo "
  "comprado de uma vez, que você joga e não volta a pagar.")
T("Guarde os dois", "o total e o por mês",
  "Guarde os dois: o total do ano e o valor por mês. Sem o total você não "
  "saberá depois se o mês mudou ou se o ano inteiro mudou.")

# ========================== DEPOIS DA RESPOSTA ===============================

# -------------------------------------------------------------------- cap 4
T("Por que o recibo", "e não a lembrança",
  "O motivo de usar recibo e não lembrança é medido, não é desconfiança: a "
  "lembrança soma as compras grandes e some com as pequenas.",
  cap="Por que o recibo vence a lembrança")
T("As pequenas repetem", "e repetição é o total",
  "E são as pequenas que repetem. Uma compra de trinta reais por mês é "
  "trezentos e sessenta por ano, e nenhuma delas pareceu grande.")
T("A lembrança também", "escolhe o mês bom",
  "A lembrança ainda faz outra coisa: escolhe o mês em que você gastou pouco "
  "como se fosse o mês típico. O histórico não escolhe.")
B("E o histórico tem data", "o que a memória não tem",
  "O histórico tem data em cada linha, e data é o que permite dividir por mês. "
  "Lembrança não tem data, só tem impressão.",
  "man typing on a phone", 6257825)
T("Isso não é culpa", "é como memória funciona",
  "Isso não é defeito seu. É como a memória funciona com valores repetidos e "
  "pequenos, e é por isso que existe a conta.")
T("O que você ganha", "um número comparável",
  "O que você ganha é um número comparável. Agora o preço do passe tem com o "
  "que ser comparado, e antes não tinha.")
T("E vale ao contrário", "pode sair menor",
  "E pode sair menor do que você temia. Isso também é informação, e também "
  "muda a decisão, no sentido oposto.")
T("A próxima parte", "como ler o próximo passe",
  "Falta usar o número. Como olhar o próximo passe com ele na mão.")

# -------------------------------------------------------------------- cap 5
T("Duas condições", "as duas juntas",
  "Duas condições, e as duas precisam valer para a compra ser decidida e não "
  "automática.",
  cap="Como decidir sobre o próximo passe")
T("A primeira", "cabe no seu valor por mês",
  "A primeira: o preço do passe, dividido pelos meses que ele dura, cabe no "
  "seu valor por mês sem empurrar nada. Quem decide se cabe é você.")
T("A segunda", "você jogou o anterior até o fim",
  "A segunda: você terminou o passe anterior. Passe não terminado é dinheiro "
  "que saiu e valor que ficou na loja.")
B("As duas, não uma", "esse é o filtro",
  "As duas, não uma. A primeira sem a segunda é como a conta cresce: cabe no "
  "mês, mas não é usado, e isso repete por temporadas.",
  "a person writing on paper", 6672502)
T("Se o passe anterior", "parou na metade",
  "Se o passe anterior parou na metade, o número a comparar não é o preço "
  "dele: é a metade que você aproveitou, pelo preço inteiro que pagou.")
T("Quando sobra folga", "aí é decisão e não impulso",
  "Quando as duas condições passam, comprar é decisão com número atrás. É "
  "exatamente o que faltava antes.")
T("O que não fazer", "comparar com o amigo",
  "O que não fazer: comparar o seu valor por mês com o de um amigo. Ele tem "
  "outros jogos, outra rotina e outro tempo livre.")
T("E não arredondar", "para baixo",
  "E não arredondar para baixo porque o número incomodou. Ele é recibo, não "
  "opinião, e arredondar desfaz a conta inteira.")

# -------------------------------------------------------------------- cap 6
T("Três erros", "que o total deixa visível",
  "Com o total escrito, três erros comuns ficam óbvios. Os três são a mesma "
  "confusão: olhar a compra e não a série.",
  cap="Três erros que o total torna visíveis")
T("Erro um", "somar só as compras grandes",
  "Erro um: somar só as compras que você lembra. O histórico tem linhas que "
  "você vai ler e não reconhecer, e elas contam igual.")
T("Erro dois", "contar a moeda que sobrou como dinheiro",
  "Erro dois: tratar a moeda que sobrou na conta como dinheiro guardado. Ela "
  "só vale dentro daquela loja, e só para aquele catálogo.")
T("Erro três", "medir um mês só",
  "Erro três: medir um mês e achar que é o seu padrão. Tem mês de lançamento e "
  "mês parado, e a série precisa do ano.")
T("Nenhum dos três", "é descontrole",
  "Nenhum dos três é descontrole. São erros de medição, e é por isso que têm "
  "conserto sem precisar de força de vontade.")
T("O caso mais caro", "renovar sem terminar",
  "O caso mais caro é renovar passe três temporadas seguidas sem terminar "
  "nenhuma, porque o preço parece pequeno e o aproveitado nunca é medido.")
T("E o inverso", "cortar o que você usava",
  "O inverso custa também: cortar o passe que você jogava até o fim, por causa "
  "de um susto com o total, quando era a parte bem gasta do ano.")
T("O mesmo número", "resolve os dois",
  "O mesmo total resolve os dois casos, e é por isso que vale os dez minutos "
  "que leva.")

# -------------------------------------------------------------------- cap 7
T("O que anotar", "e em que formato",
  "O formato do registro decide se a conta ainda serve na próxima temporada, "
  "que é quando a pergunta volta.",
  cap="O que anotar, e por que dois números")
T("Dois números", "e o ano",
  "Anote dois números e o ano: o total do ano e o valor por mês. Uma linha por "
  "ano já resolve.")
T("Não anote o percentual", "anote reais",
  "Não anote percentual da sua renda. Anote reais, porque reais você compara "
  "com o preço do passe e percentual não.")
T("Se quiser uma coluna", "quantos passes terminou",
  "Se quiser uma coluna a mais, anote quantos passes você terminou naquele "
  "ano. É a coluna que separa gasto de desperdício.")
B("Papel serve", "e bloco do celular também",
  "Papel serve, bloco de notas serve. O que importa é ver os números e o ano, "
  "não um gráfico que suaviza justamente o que interessa.",
  "writing in a notebook", 5717468)
T("Em dois anos", "você tem uma série",
  "Em dois anos você tem dois totais e dois valores por mês, e aí a pergunta "
  "deixa de ser sobre o passe e passa a ser sobre a tendência.")
T("Se o total subir muito", "isso também é informação",
  "E se o total subir muito de um ano para o outro, isso é informação: mudou o "
  "jogo, mudou a rotina ou mudou o preço, e dá para descobrir qual.")
T("Nada disso exige", "comprar nada",
  "Nada disso exige aplicativo, planilha paga ou assinatura. Exige uma página "
  "de histórico e uma divisão.")

# -------------------------------------------------------------------- cap 8
T("Uma ressalva", "e ela importa mais",
  "Antes de terminar, uma ressalva, e ela importa mais que a conta.",
  cap="O que esta conta NÃO diz")
T("Não diz", "se você gasta demais",
  "Esta conta não diz se você gasta demais. Diz quanto você gasta. Se é demais "
  "ou não, só você sabe, olhando o resto do seu mês.")
T("E não julga", "o hobby",
  "E não julga o hobby. Jogo é lazer e lazer custa dinheiro, como cinema, "
  "viagem ou qualquer outra coisa que você escolhe.")
T("Não é aconselhamento", "financeiro",
  "Não é aconselhamento financeiro. É uma soma e uma divisão em cima de "
  "recibos que já são seus.")
T("E se o número assustar", "ele continua sendo só um número",
  "E se o total assustar, ele continua sendo apenas um número. Ele serve para "
  "decidir a próxima compra, não para brigar com as anteriores.")
T("O que sobra", "reais por mês, seus",
  "O que sobra para você são reais por mês, calculados no seu histórico, para "
  "o seu ano — e uma data em que a pergunta volta.")
T("Comece agora", "antes do passe acabar",
  "Comece pela página de histórico, hoje, antes de a temporada virar e a "
  "pergunta chegar sem o número.")
C("Escreva o valor por mês", "só esse número",
  "Nos comentários, escreva só o valor por mês. Não o total, não o seu salário, "
  "não o jogo. Quero ver o quanto esse número varia entre pessoas que jogam "
  "parecido.")

# ================================== SHORT ====================================

# O short fecha UMA pergunta — quanto saiu este ano, com a conta inteira — e o
# longo abre OUTRA: as duas condicoes do proximo passe (aprendizado 563).

SHORT = [
    {"layout": "titulo", "kicker": "Um número seu", "sub": "que ninguém soma",
     "nar": "Quanto saiu da sua conta este ano em moeda de jogo e passe? O "
            "número existe e está escrito em recibos.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Primeiro", "sub": "o histórico do ano",
     "nar": "Abra o histórico de compras, filtre do começo do ano e marque só "
            "moeda, passe e pacote.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Some tudo", "sub": "até os de cinco reais",
     "nar": "Some todas, inclusive as de cinco reais. São elas que mudam o "
            "total.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Divida", "sub": "pelos meses que passaram",
     "nar": "Divida pelo número de meses que já passaram. Esse é o seu valor "
            "por mês, e é com ele que se compara o próximo passe.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "As duas condições", "sub": "no vídeo",
     "nar": "Quando comprar o próximo passe são duas condições, e as duas "
            "estão no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Quanto já", "l2": "saiu"}

COPY = """# O total do ano em moeda de jogo e passe, somado no próprio histórico

## TITULO
Passe de Temporada: Quanto Você Já Gastou Este Ano — A Conta Está no Seu Histórico

## TITULO SHORT
Quanto saiu em moeda de jogo este ano?

## DESCRICAO
Existe um número seu que você provavelmente nunca somou: quanto saiu da sua conta este ano em moeda de jogo, passe e pacote. Ele não é estimativa. São recibos, com data e valor, numa página que você abre em dez segundos — e ninguém soma porque o gasto não sai de uma vez, sai em pedaços de cinco, de dez, de trinta reais, e cada pedaço parece pequeno sozinho.

Três coisas no desenho da compra fazem o gasto não parecer gasto. Você compra duas vezes: primeiro troca dinheiro por moeda, depois troca moeda por item, e só a primeira troca é gasto — justamente a que se esquece. Os pacotes de moeda quase nunca fecham com o preço do item, então sobra um resto guardado que puxa a próxima compra. E o cartão já está salvo, então a compra não tem o instante em que você olha o valor e pensa. Nada disso é armadilha: é desenho comum de loja digital.

A conta tem dois passos e nenhum número meu. Passo um: abra o histórico de compras da loja onde você joga — console, Steam ou celular, todos têm essa página — filtre do primeiro dia do ano até hoje e marque só o que é moeda, passe, pacote ou item. Jogo inteiro comprado uma vez fica de fora, porque não repete, e o que estamos medindo é o gasto que volta. Some tudo, inclusive os de cinco reais, que são os que mudam o total. Passo dois: divida esse total pelo número de meses que já passaram — não por doze, pelos meses que realmente aconteceram. O resultado é o seu valor por mês nessa categoria, e é com ele que se compara o preço do próximo passe, não com o preço dele sozinho.

O vídeo fecha essa conta nos primeiros três minutos e depois mostra o que fazer com o número: por que o recibo vence a lembrança, as duas condições que a compra do próximo passe precisa cumprir (caber no seu valor por mês E você ter terminado o passe anterior), três erros de medição que o total torna visíveis, e o que anotar para que a conta ainda sirva na próxima temporada.

Uma ressalva que importa mais que a conta: isso não diz se você gasta demais — diz quanto você gasta. Se é demais ou não, só você sabe, olhando o resto do seu mês. E não julga o hobby: jogo é lazer e lazer custa dinheiro, como cinema ou viagem. Não é aconselhamento financeiro, é uma soma e uma divisão em cima de recibos que já são seus.

CAPITULOS
{CAPITULOS}

Nos comentários, escreva só o valor por mês. Não o total, não o seu salário, não o jogo. Quero ver o quanto esse número varia entre pessoas que jogam parecido.

## DISCLOSURE
A narração e as imagens deste vídeo são geradas por computador. O roteiro é original e o conteúdo é informativo, não é aconselhamento financeiro.

## HASHTAGS
#passedetemporada #moedadojogo #gastos

## TAGS
passe de temporada, moeda do jogo, historico de compras, quanto gastei em jogos, gasto por mes, battle pass, microtransacoes, loja digital, recibos de compra, controle de gastos em jogos, steam historico, compras no console, valor por mes, passe nao terminado, lazer e orcamento

## COMENTARIO FIXADO
A conta em duas linhas: abra o histórico de compras, filtre do começo do ano e some só moeda, passe e pacote (jogo inteiro fica fora). Divida pelos meses que já passaram. Esse é o seu valor por mês — e é com ele que se compara o próximo passe. Escreve aqui só esse número, não o total.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita gasto medio em microtransacao, nao cita percentual recomendado de orcamento para lazer, nao cita preco de passe de nenhum jogo, nao cita nome de loja nem de editora e nao cita quanto a industria fatura com moeda virtual. Os dois numeros da conta sao do proprio espectador: a soma dos recibos dele no ano e o numero de meses que ja passaram. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer valor de referencia do tipo "o normal e gastar X por mes em jogo", porque nao existe fonte oficial para isso e o video nao faz essa comparacao — a conta e sobre o historico dele, nao sobre uma media; (2) qualquer numero de faturamento da industria, porque seria FATO sobre o mundo, e neste canal o unico pacote com ZERO views de longo e justamente o que entregou fato sobre a industria (demissoes na Square Enix); (3) qualquer juizo sobre gastar em jogo — o video diz explicitamente que lazer custa dinheiro e que se o total e demais ou nao, so o espectador sabe. ESTE EIXO SUBSTITUI O NUMERO INSTITUCIONAL DE PROPOSITO, e a decisao vem do dado deste canal: o MAIOR short daqui (250 views) entregou QUATRO views de longo, falando de preco em horas de trabalho em abstrato, enquanto o MELHOR longo (vinte e uma views) veio de um short de cem e prometia "a conta em reais ANTES de comprar".
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/nivel-do-jogo-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-010",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1B4332", "c1": "#D64570", "c2": "#7FB069",
               "bg": "#EFF6F1"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/nivel-do-jogo-010.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
    RESIDUO = 1.028   # pt-BR-AntonioNeural, +2,8% no ensaio.py
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "é o seu gasto por mês nessa categoria" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
