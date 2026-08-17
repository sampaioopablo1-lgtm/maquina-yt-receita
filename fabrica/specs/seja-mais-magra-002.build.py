#!/usr/bin/env python3
"""seja-mais-magra-002 — o que se reganha depois da caneta nao e o que se perdeu.

PAUTA (PASSO 0, medido em 17/08/2026 sobre 109 videos de 90 dias, pt-BR):
mediana do nicho 197,1 views/dia, outlier a partir de 591,3. O eixo campeao e
"canetas emagrecedoras" — 1-FJxXz2GWk (BBC) 40.113 v/d, 77stnrUGd28 13.857 v/d,
jVWCkaXZ83c ("o efeito que quase ninguem mostra no espelho") 8.130 v/d.

O canal ja publicou o molde "X natural existe / a Anvisa proibiu"
(ezwObtEpxps, fonte x6NixO45JEA). Repetir seria similaridade alta, entao o eixo
aqui e OUTRO: nao os produtos falsos, e o que acontece com a composicao corporal
de quem usa a caneta de verdade e depois para.

ESTRUTURA modelada no outlier (revelacao: "o que acontece com seu corpo que
ninguem te conta"), nunca o assunto dele.

NUMEROS — duas fontes que batem, ambas com DXA:
  * STEP-1 (semaglutida, subgrupo DXA, n=95): cerca de 40% do peso perdido saiu
    como massa magra; gordura total caiu ~19% e massa magra ~10%.
  * SURMOUNT-1 (tirzepatida, subgrupo DXA, n=124): cerca de 25% do peso perdido
    saiu como massa magra; na semana setenta e dois, peso -21,3%, gordura -33,9%
    e massa magra -10,9%.
  * SURMOUNT-4: apos perder 20,9% em trinta e seis semanas, quem passou para
    placebo reganhou catorze pontos percentuais em cinquenta e duas semanas.
  * Revisao sistemática de interrupcao: cerca de dois tercos do peso perdido
    volta em torno de um ano, mais rapido nos tres primeiros meses.

O video NAO diz para parar nem para comecar tratamento — diz o que medir e o que
perguntar ao medico. Conteudo de saude sem indicacao de conduta.

Duracao dimensionada com o MODELO MEDIDO da voz (17/08/2026): Francisca
R=16,92 chars/s e P=1,036 s/frase. Com o modelo antigo (P=0,310) este mesmo
roteiro seria estimado em quase dois minutos a menos.
"""
import json
import os

SLUG = "seja-mais-magra"
PACOTE = "seja-mais-magra-002"

PALETA = {"bg": "#FDF3F4", "c1": "#C9184A", "c2": "#7FB069", "ink": "#2B1B1F"}


def t(kicker, sub, nar, cap=None, sem_cap=False):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def i(kicker, preco, nar):
    return {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}


def li(kicker, itens, nar, cap=None, sem_cap=False):
    c = {"layout": "lista", "kicker": kicker, "itens": itens, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def b(kicker, itens, alturas, nar, cap=None, sem_cap=False):
    c = {"layout": "barras", "kicker": kicker, "itens": itens,
         "alturas": alturas, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


LONGO = [
    # ---------- capitulo 1: o espelho ----------
    t("MENOS DEZ QUILOS", "e o espelho discordando da balança",
      "A balança marcou dez quilos a menos. Você olhou no espelho e alguma coisa "
      "não fechou. O número desceu, mas o corpo não ficou do jeito que você "
      "imaginou que ficaria.",
      cap="Intro: o espelho e a balança"),
    i("O que a balança mede", "peso total",
      "A explicação não é frescura, nem impressão sua. É que a balança mede uma "
      "coisa só: o peso total do corpo. Ela não pergunta de onde veio o que "
      "saiu."),
    i("O que ela não separa", "gordura de músculo",
      "E o que saiu não é uma coisa só. Todo emagrecimento tira gordura e tira "
      "também massa magra, que é músculo, água e outros tecidos. A balança soma "
      "os dois e mostra um número só."),
    t("A PERGUNTA DO VÍDEO", "quanto do que você perdeu era músculo",
      "Então a pergunta que interessa não é quanto você perdeu. É quanto do que "
      "você perdeu era músculo. E essa conta muda tudo o que vem depois.",
      sem_cap=True),
    i("Por que agora", "as canetas",
      "Essa pergunta virou urgente por um motivo simples. As canetas "
      "emagrecedoras colocaram milhões de pessoas perdendo peso rápido, e "
      "perdendo muito peso."),
    i("Os nomes", "semaglutida e tirzepatida",
      "Você conhece pelos nomes comerciais. Por trás deles estão duas "
      "substâncias diferentes: a semaglutida e a tirzepatida. Guarde essa "
      "diferença, porque ela vai importar."),
    li("O que este vídeo responde",
       ["quanto da perda é músculo",
        "o que acontece quando para",
        "o que muda essa conta"],
       "Este vídeo responde três coisas. Quanto do peso perdido é músculo. O que "
       "acontece com o corpo quando o tratamento para. E o que, segundo os "
       "estudos, muda essa conta a seu favor."),
    t("O AVISO", "isto não é indicação de tratamento",
      "Um aviso antes de continuar, e ele é sério. Este vídeo não diz para você "
      "começar nem para parar nada. Quem decide isso é o seu médico, com os seus "
      "exames na frente.",
      sem_cap=True),
    i("O que ele é", "informação para perguntar melhor",
      "O que este vídeo faz é outra coisa. Ele mostra o que os estudos mediram, "
      "para você chegar na consulta sabendo o que perguntar e o que pedir para "
      "acompanhar."),
    i("A diferença", "medir, não adivinhar",
      "Porque a diferença entre um bom resultado e um resultado frustrante, "
      "aqui, quase sempre está no que foi medido e no que ninguém mediu."),
    t("O NÚMERO QUE FALTA", "a balança sozinha não conta a história",
      "E a coisa mais importante que quase ninguém mede é justamente a que a "
      "balança não sabe mostrar sozinha.",
      sem_cap=True),

    # ---------- capitulo 2: o que o exame mede ----------
    t("COMO SE MEDE", "o exame que separa o que saiu",
      "Existe um exame que separa. Ele se chama densitometria de corpo inteiro, "
      "conhecida pela sigla em inglês, dexa. Ele diz quanto do seu peso é "
      "gordura e quanto é massa magra.",
      cap="Como se mede o que saiu"),
    i("O que ele faz", "divide o peso",
      "Em vez de um número só, o exame devolve a divisão. Tantos quilos de "
      "gordura. Tantos quilos de massa magra. E aí dá para acompanhar cada um "
      "separado ao longo do tratamento."),
    i("Por que isso importa", "dois cenários, mesmo peso",
      "Imagine duas pessoas que perderam os mesmos dez quilos. Na primeira, oito "
      "eram gordura e dois eram músculo. Na segunda, seis eram gordura e quatro "
      "eram músculo. A balança conta a mesma história para as duas."),
    b("Mesma perda, composição diferente",
      ["oito de gordura", "seis de gordura"], [80, 60],
      "Mas o corpo das duas não é o mesmo no fim. E o que vai acontecer com cada "
      "uma nos meses seguintes também não vai ser o mesmo.",
      sem_cap=True),
    i("O que o músculo faz", "sustenta o gasto",
      "Massa magra não é estética. É o tecido que sustenta boa parte do que você "
      "gasta em repouso, que segura a força para as tarefas do dia e que protege "
      "articulação e osso."),
    i("O que ele faz com a glicose", "guarda o açúcar",
      "O músculo também é o maior destino do açúcar que entra pela comida. Menos "
      "músculo significa menos lugar para guardar essa glicose."),
    t("A CONTA MUDA", "perder músculo cobra depois",
      "Por isso a mesma perda de peso pode cobrar preços diferentes. E o preço "
      "de perder músculo não aparece na hora. Ele aparece meses depois.",
      sem_cap=True),
    i("Onde os estudos mediram", "subgrupos com o exame",
      "A boa notícia é que os grandes estudos das canetas fizeram esse exame. "
      "Não em todo mundo, mas em subgrupos. E os números foram publicados."),
    i("O que vem agora", "os dois estudos",
      "São dois estudos, um para cada substância. E eles não deram o mesmo "
      "resultado. Vamos aos dois."),

    # ---------- capitulo 3: os numeros ----------
    t("ESTUDO UM", "semaglutida, subgrupo com exame",
      "O primeiro é o estudo da semaglutida, chamado step um. No subgrupo que "
      "fez a densitometria, foram noventa e cinco participantes acompanhados.",
      cap="Semaglutida: o que o exame mostrou"),
    i("O que aconteceu com a gordura", "queda de cerca de dezenove por cento",
      "A gordura total caiu cerca de dezenove por cento. É uma queda "
      "expressiva, e é exatamente o que se espera de um tratamento que funciona "
      "para reduzir peso."),
    i("O que aconteceu com o músculo", "queda de cerca de dez por cento",
      "A massa magra também caiu. Cerca de dez por cento. E é aqui que a conta "
      "começa a ficar interessante."),
    b("Da perda total, o que era músculo",
      ["gordura", "massa magra"], [60, 40],
      "Quando se olha o peso perdido como um todo, cerca de quarenta por cento "
      "dele saiu como massa magra. Quatro de cada dez quilos que sumiram da "
      "balança não eram gordura.",
      sem_cap=True),
    t("QUARENTA POR CENTO", "quatro em cada dez quilos",
      "Vale repetir o número devagar, porque ele é o centro deste vídeo. Quatro "
      "em cada dez quilos perdidos, no subgrupo medido da semaglutida, não eram "
      "gordura.",
      sem_cap=True),
    t("ESTUDO DOIS", "tirzepatida, subgrupo com exame",
      "O segundo estudo é o da tirzepatida, chamado surmount um. O subgrupo com "
      "densitometria teve cento e vinte e quatro participantes.",
      sem_cap=True),
    i("O peso na semana setenta e dois", "menos vinte e um vírgula três por cento",
      "Na semana setenta e dois, o peso corporal tinha caído vinte e um vírgula "
      "três por cento. Uma perda grande, de gente que perdeu de verdade."),
    i("A gordura", "menos trinta e três vírgula nove por cento",
      "A gordura caiu bem mais que o peso, em termos proporcionais. Trinta e "
      "três vírgula nove por cento a menos. É esse descompasso que interessa."),
    i("A massa magra", "menos dez vírgula nove por cento",
      "E a massa magra caiu dez vírgula nove por cento. Um número parecido com o "
      "da semaglutida em queda absoluta, mas com um peso total bem maior "
      "embaixo."),
    b("Da perda total, o que era músculo",
      ["gordura", "massa magra"], [75, 25],
      "Resultado: cerca de vinte e cinco por cento do peso perdido era massa "
      "magra. Um quarto, e não quatro décimos.",
      sem_cap=True),
    t("A DIFERENÇA", "vinte e cinco contra quarenta",
      "Então as duas substâncias não se comportam igual nesse ponto. Vinte e "
      "cinco por cento contra cerca de quarenta por cento da perda saindo como "
      "massa magra.",
      sem_cap=True),
    i("O cuidado com a comparação", "estudos diferentes",
      "Um cuidado honesto aqui. São estudos diferentes, com desenhos e "
      "populações diferentes. Comparar lado a lado não é o mesmo que ter feito "
      "um estudo que compare as duas de frente."),
    i("O que dá para dizer", "as duas tiram músculo",
      "O que dá para afirmar com segurança é o mais simples. As duas tiram "
      "músculo junto com a gordura. Nenhuma das duas tira só gordura."),
    t("E ISSO É NORMAL", "toda perda de peso faz isso",
      "E aqui vem uma coisa que quase nunca é dita. Isso não é defeito da "
      "caneta. Emagrecimento por dieta também tira massa magra. A questão nunca "
      "foi se tira, foi quanto tira.",
      sem_cap=True),
    i("O que muda", "a velocidade e o tamanho",
      "O que a caneta muda é a escala. Perde-se mais peso, e mais rápido. Então "
      "a fatia de músculo que sai junto também fica maior em quilos, mesmo que a "
      "porcentagem fosse a mesma."),

    # ---------- capitulo 4: quando para ----------
    t("A SEGUNDA METADE", "o que acontece quando o tratamento para",
      "Agora a segunda metade da história, que é a que quase ninguém conta. O "
      "que acontece quando o tratamento para.",
      cap="O que acontece quando para"),
    i("O estudo", "surmount quatro",
      "Existe um estudo desenhado exatamente para isso, chamado surmount quatro. "
      "Todo mundo usou o tratamento por trinta e seis semanas primeiro."),
    i("O que aconteceu nas trinta e seis semanas", "menos vinte por cento",
      "Nessas trinta e seis semanas, o grupo perdeu em média vinte vírgula nove "
      "por cento do peso. Um resultado forte, do tipo que muda a vida de quem "
      "conseguiu."),
    i("A divisão do grupo", "continuar ou parar",
      "Aí o grupo foi dividido. Metade continuou com o tratamento. A outra "
      "metade passou a receber placebo, ou seja, na prática parou."),
    b("Cinquenta e duas semanas depois",
      ["quem continuou", "quem parou"], [82, 30],
      "Cinquenta e duas semanas depois, quem parou tinha reganhado catorze "
      "pontos percentuais de peso. Sobrou cerca de dez por cento de perda em "
      "relação ao ponto de partida.",
      sem_cap=True),
    t("DOIS TERÇOS", "a maior parte do peso volta",
      "Juntando os estudos de interrupção, o padrão se repete. Em torno de um "
      "ano depois de parar, cerca de dois terços do peso perdido voltaram.",
      sem_cap=True),
    i("A velocidade", "os três primeiros meses",
      "E não volta devagar e por igual. Volta rápido no começo. Os três "
      "primeiros meses depois da parada são os mais intensos, e depois o ritmo "
      "desacelera."),
    i("O que isso diz", "é tratamento, não é curso",
      "O que esse desenho de estudo mostra é uma característica do tratamento, "
      "não uma falha de quem usou. A obesidade é tratada como doença crônica, e "
      "o efeito acompanha o uso."),
    t("MAS FALTA UMA COISA", "o peso voltou. e o músculo?",
      "Só que tem uma pergunta que esses números de peso não respondem. O peso "
      "voltou, sim. Mas voltou como o quê?",
      sem_cap=True),
    i("A assimetria", "a volta não é simétrica",
      "E é aqui que a conta fica desconfortável. Porque não há razão para o peso "
      "voltar na mesma proporção em que saiu."),
    i("O que reganha sozinho", "gordura",
      "Ganhar gordura de volta é o que acontece por padrão quando o apetite "
      "volta e o consumo sobe. Não exige nada de você além de comer mais."),
    i("O que não reganha sozinho", "músculo",
      "Recuperar massa magra é outra história. Músculo não volta só porque você "
      "voltou a comer. Ele responde a estímulo de força e a proteína suficiente."),

    # ---------- capitulo 5: a troca ----------
    t("A TROCA SILENCIOSA", "sai músculo, volta gordura",
      "Junte as duas metades e aparece a troca silenciosa. Você perdeu uma parte "
      "em músculo. E o que voltou tende a ser, em maior proporção, gordura.",
      cap="A troca silenciosa"),
    i("O resultado no ciclo", "mesmo peso, corpo diferente",
      "O resultado é que a pessoa pode voltar ao mesmo peso de antes com uma "
      "composição pior que a de antes. Mesma balança, corpo diferente."),
    i("Por que o espelho estranha", "menos músculo por baixo",
      "É por isso que o espelho às vezes discorda da balança. Com menos massa "
      "magra por baixo, o mesmo peso ocupa o corpo de outro jeito."),
    t("O EFEITO SANFONA", "por que ele fica mais difícil a cada volta",
      "E isso ajuda a explicar por que cada rodada do efeito sanfona costuma "
      "parecer mais difícil que a anterior.",
      sem_cap=True),
    i("O que sobra no fim", "menos músculo sustentando",
      "Se a cada ciclo sai músculo e volta gordura, a base que sustenta o gasto "
      "diário vai ficando menor. E o corpo que precisa emagrecer de novo tem "
      "menos estrutura para isso."),
    i("O que isso não significa", "não é culpa de quem usou",
      "Isso não é um argumento contra o tratamento, e não é culpa de quem "
      "tratou. É um argumento contra tratar sem medir e contra parar sem plano."),
    t("A PERGUNTA CERTA", "não é se emagrece. é o que fica",
      "Então a pergunta certa nunca foi se a caneta emagrece. Ela emagrece, e os "
      "números disso são grandes. A pergunta é o que fica no corpo depois.",
      sem_cap=True),
    i("O que a resposta depende", "do que foi feito junto",
      "E essa resposta não depende só da substância. Depende bastante do que foi "
      "feito junto com ela."),

    # ---------- capitulo 6: o que muda a conta ----------
    t("O QUE MUDA A CONTA", "duas alavancas conhecidas",
      "Os estudos de composição corporal apontam para duas alavancas. Nenhuma "
      "delas é novidade, e é justamente por isso que são subestimadas.",
      cap="O que muda essa conta"),
    i("Alavanca um", "treino de força",
      "A primeira é treino de força. É o estímulo que sinaliza para o corpo que "
      "aquele músculo está em uso e precisa ser mantido enquanto o peso desce."),
    i("O que isso não é", "não é cardio",
      "E não é a mesma coisa que caminhar ou pedalar. Caminhada é excelente para "
      "muita coisa, e vale a pena. Mas o sinal que preserva músculo em déficit "
      "vem principalmente da carga."),
    i("Alavanca dois", "proteína suficiente",
      "A segunda é proteína suficiente ao longo do dia. Com o apetite reduzido "
      "pela medicação, comer menos no total é fácil. Comer pouca proteína "
      "também."),
    li("O problema do apetite baixo",
       ["come-se menos no total",
        "a proteína cai junto",
        "o músculo perde matéria-prima"],
       "E aí se forma o pior arranjo possível. Menos comida no total, menos "
       "proteína dentro dela, e o corpo sem a matéria-prima para segurar a massa "
       "magra enquanto perde peso.",
       sem_cap=True),
    i("O que perguntar", "quanta proteína no meu caso",
      "Uma pergunta concreta para a consulta: quanta proteína por dia faz "
      "sentido no meu caso, com o meu peso e a minha função renal? Esse número "
      "não é igual para todo mundo."),
    i("O que pedir", "acompanhar a composição",
      "E outra: dá para acompanhar a composição corporal, e não só o peso, ao "
      "longo do tratamento? Nem sempre haverá o exame disponível, mas a pergunta "
      "muda a conversa."),
    t("POR QUE PERGUNTAR MUDA", "o que se mede é o que se cuida",
      "Porque o que não é medido não é cuidado. Se a única coisa acompanhada for "
      "o número da balança, é ele que vai guiar as decisões — e ele não separa o "
      "que saiu.",
      sem_cap=True),
    i("O terceiro ponto", "o plano de saída",
      "E existe um terceiro ponto, que aparece pouco. Qual é o plano para "
      "depois? Porque os estudos de interrupção mostram que parar sem plano tem "
      "um resultado bem previsível."),
    i("O que já se sabe", "o reganho é esperado",
      "Se dois terços do peso costumam voltar em cerca de um ano, isso deixa de "
      "ser surpresa e passa a ser algo a planejar desde o começo."),
    t("O QUE PROTEGE", "força e proteína continuam depois",
      "E as duas alavancas do tratamento são as mesmas do depois. Manter treino "
      "de força e proteína adequada é o que continua trabalhando quando a "
      "medicação sai de cena.",
      sem_cap=True),

    # ---------- capitulo 7: fecho ----------
    t("RECAPITULANDO", "os quatro números",
      "Vamos fechar com os quatro números que importam deste vídeo.",
      cap="Os quatro números"),
    li("O que ficou medido",
       ["quarenta por cento na semaglutida",
        "vinte e cinco por cento na tirzepatida",
        "catorze pontos reganhos ao parar"],
       "No subgrupo medido da semaglutida, cerca de quarenta por cento da perda "
       "era massa magra. No da tirzepatida, cerca de vinte e cinco. E quem parou "
       "reganhou catorze pontos percentuais em um ano."),
    i("O quarto número", "dois terços voltam",
      "E o quarto: em torno de dois terços do peso perdido volta cerca de um ano "
      "depois da parada, mais rápido nos três primeiros meses."),
    t("O QUE FAZER COM ISSO", "não é parar. é medir",
      "O que fazer com esses números não é largar tratamento nenhum por causa de "
      "um vídeo. É levar as perguntas certas para quem acompanha você.",
      sem_cap=True),
    li("As três perguntas",
       ["quanta proteína no meu caso",
        "dá para acompanhar a composição",
        "qual é o plano depois"],
       "São três. Quanta proteína por dia no meu caso. Dá para acompanhar a "
       "composição corporal e não só o peso. E qual é o plano para quando o "
       "tratamento terminar."),
    t("A PONTE", "o peso é o placar, não o jogo",
      "E fica a ideia que atravessa tudo isso. O peso é o placar. Ele é fácil de "
      "ler e por isso vira o centro de tudo. Mas o jogo que está sendo disputado "
      "por baixo é outro.",
      sem_cap=True),
    i("O que está em disputa", "o que sai e o que volta",
      "O que está em disputa é a composição do que sai agora e a composição do "
      "que volta depois. Duas contas que a balança soma numa só e entrega "
      "resolvida."),
    {"layout": "cta", "kicker": "Sua vez",
     "sub": "você já mediu composição, ou só peso?",
     "cap": "A sua vez",
     "nar": "Agora me conta nos comentários: no seu acompanhamento, alguém já "
            "mediu sua composição corporal, ou foi sempre só a balança? Sua "
            "resposta ajuda a escolher o próximo vídeo."},
    t("ATÉ O PRÓXIMO", "se inscreva para os próximos números",
      "Se você quer os próximos assuntos de saúde tratados assim, com o número e "
      "a fonte na mesa, se inscreva no canal. Até o próximo vídeo.",
      sem_cap=True),
]

SHORT = [
    {"layout": "titulo", "kicker": "QUARENTA POR CENTO",
     "sub": "do que você perdeu pode não ser gordura",
     "nar": "Quarenta por cento do peso que você perdeu pode não ser gordura."},
    {"layout": "item", "kicker": "O que o exame separou", "preco": "massa magra",
     "nar": "No exame do estudo da semaglutida, quatro em cada dez quilos "
            "perdidos eram massa magra."},
    {"layout": "item", "kicker": "Quando o tratamento para", "preco": "dois terços",
     "nar": "E quando o tratamento para, cerca de dois terços do peso voltam em "
            "um ano. Só que o que volta é, em maior proporção, gordura."},
    {"layout": "titulo", "kicker": "A TROCA", "sub": "mesmo peso, corpo diferente",
     "nar": "Sai músculo, volta gordura. Dá para terminar no mesmo peso com uma "
            "composição pior."},
    {"layout": "cta", "kicker": "No vídeo completo",
     "sub": "os quatro números e as três perguntas",
     "nar": "No vídeo do canal estão as três perguntas para levar ao seu médico. "
            "Não é indicação de tratamento."},
]

COPY = """# O que se reganha depois da caneta nao e o que se perdeu

## TÍTULO
Ozempic e Mounjaro: O Que Você Reganha Não É o Que Você Perdeu

## DESCRIÇÃO
A balança mede uma coisa só: o peso total. Ela não separa gordura de massa magra — e é essa diferença que decide o que acontece com o seu corpo depois.

Neste vídeo eu mostro o que os exames de composição corporal dos grandes estudos das canetas emagrecedoras encontraram, e por que o peso que volta depois não é o mesmo peso que saiu.

Os números que aparecem aqui:

• No subgrupo com densitometria (DXA) do estudo STEP-1, com semaglutida e 95 participantes, cerca de 40% do peso perdido saiu como massa magra. A gordura total caiu cerca de 19% e a massa magra cerca de 10%.

• No subgrupo com densitometria do estudo SURMOUNT-1, com tirzepatida e 124 participantes, cerca de 25% do peso perdido saiu como massa magra. Na semana 72: peso −21,3%, gordura −33,9% e massa magra −10,9%.

• No estudo SURMOUNT-4, o grupo perdeu 20,9% do peso em 36 semanas. Quem passou para placebo reganhou 14 pontos percentuais em 52 semanas, sobrando cerca de 10% de perda em relação ao início.

• Nos estudos de interrupção, cerca de dois terços do peso perdido volta em torno de um ano, mais rápido nos três primeiros meses.

A assimetria é o ponto central do vídeo: gordura volta sozinha quando o apetite retorna, mas músculo não volta só porque a pessoa voltou a comer. Ele responde a treino de força e a proteína suficiente. Por isso um ciclo de perder e reganhar pode terminar no mesmo peso da balança com uma composição corporal pior do que a de antes — e é isso que ajuda a explicar por que cada rodada do efeito sanfona costuma parecer mais difícil que a anterior.

Isso não é um argumento contra o tratamento, e não é culpa de quem tratou. É um argumento contra tratar sem medir e contra parar sem plano.

As três perguntas para levar à consulta estão no fim do vídeo: quanta proteína por dia no seu caso, se dá para acompanhar composição corporal e não apenas o peso, e qual é o plano para quando o tratamento terminar.

AVISO: este vídeo é informativo e NÃO é indicação de tratamento. Ele não recomenda começar, ajustar ou interromper qualquer medicamento. Quem decide isso é o seu médico, com os seus exames na frente.

Se você quer assuntos de saúde tratados assim, com o número e a fonte na mesa, se inscreva no canal.

## CAPÍTULOS
{CAPITULOS}

## COMENTÁRIO
No seu acompanhamento, alguém já mediu sua composição corporal, ou foi sempre só a balança? Conta aqui — a resposta ajuda a escolher o próximo vídeo. E lembrando: nada aqui substitui a conversa com o seu médico.

## HASHTAGS
#emagrecimento #massamagra #saude

## TAGS
ozempic, mounjaro, semaglutida, tirzepatida, canetas emagrecedoras, massa magra, composicao corporal, efeito sanfona, reganho de peso, emagrecimento saudavel, perder gordura, musculo, proteina, treino de forca, saude baseada em evidencia

## CONFIGURAÇÕES DO STUDIO
Categoria: Educação. Idioma do vídeo e do áudio: português (Brasil). Não é conteúdo para crianças. Conteúdo sintético declarado: sim (narração e ilustração geradas por IA). Legendas: arquivo .srt em português enviado junto. Visibilidade: público.

## MÚSICA / LICENÇA
{TRILHA}

## FONTES
STEP-1 (semaglutida), subgrupo com DXA, n=95. SURMOUNT-1 (tirzepatida), subgrupo com DXA, n=124, semana 72. SURMOUNT-4 (interrupção após 36 semanas). Revisões de reganho após interrupção de agonistas de GLP-1.

Conteúdo produzido com narração e ilustração sintéticas (geradas por inteligência artificial). Os dados citados vêm dos estudos nomeados acima.
"""


TAGS = [
    "ozempic", "mounjaro", "semaglutida", "tirzepatida",
    "canetas emagrecedoras", "massa magra", "composicao corporal",
    "efeito sanfona", "reganho de peso", "emagrecimento saudavel",
    "perder gordura", "musculo", "proteina", "treino de forca",
    "saude baseada em evidencia",
]

SPEC = {
    "slug": SLUG,
    "pacote": PACOTE,
    "voz": "pt-BR-FranciscaNeural",
    "idioma": "pt-BR",
    "trilha": "Wholesome",
    "paleta": PALETA,
    "thumb": {"l1": "40% NÃO", "l2": "ERA GORDURA"},
    "longo": LONGO,
    "short": SHORT,
    "copy": COPY,
    "tags": TAGS,
    "fonte_pauta": "jVWCkaXZ83c",
}

if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           f"{PACOTE}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{destino}: {len(LONGO)} cenas, short {len(SHORT)}")
