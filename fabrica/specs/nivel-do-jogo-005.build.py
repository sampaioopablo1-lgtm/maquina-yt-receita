#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-005.

POR QUE ESTE CANAL, E O QUE O VEREDITO MUDOU AQUI

Primeiro da fila que produz (ultimo pacote 18/08 18:17). Veredito da
v_maquina_licoes: `suspenso` — short com mediana de 0,73 views/dia e o longo em
0,15, ou seja o longo nao paga o proprio render.

Mas a variancia e enorme: o TOPO do short e 92,5 v/d. O canal ja acertou. Entao
a pergunta util nao era "qual formato", era "o que o acerto teve".

O ACERVO RESPONDE, e responde limpo:

    Preco dos Jogos em 2026: Quantas Horas de Trabalho Custa GTA 6   92,5 v/d
    EA FC 27: Standard, Ultimate ou Plus? A Conta em Reais           39,5
    Lei Felca nos Games: R$ 333 Milhoes e o Fim da Caixinha           1,7
    Por Que a Inflacao nos Games E Mais Perigosa Que na Vida Real?    0,1

Os dois que funcionaram tem PRECO CONCRETO EM REAIS mais UMA DECISAO DE COMPRA
do espectador, presos a um produto especifico. Os dois que morreram sao
regulacao e economia abstrata.

Isso contraria a leitura preguicosa da regra do "eixo nao usado": os eixos que
o canal ainda nao repetiu sao justamente os dois MORTOS. Onde o nicho e o
acervo discordam, vale o acervo — entao fica-se no eixo de preco e muda-se o
ANGULO. Similaridade contra o acervo: 0,299, teto 0,65.

O ANGULO INEDITO. Os dois videos que funcionaram falaram do preco de UM jogo.
Este fala do MECANISMO que decide o preco de todos eles — e ele mudou.

A DOR DATADA, duas fontes que batem:

  Valve, 28 de marco de 2026: atualizou as tabelas de conversao das 35 moedas
  da Steam e lancou ferramentas de precificacao regional. O desenvolvedor
  passa a escolher entre TRES modelos: cambio simples, poder de compra, e
  multivariavel (cambio mais poder de compra mais o preco de outras formas de
  entretenimento na regiao — o mais proximo do que a Valve usava antes).

  O efeito em reais, para um jogo de dez dolares:
      antes            R$ 33
      cambio simples   R$ 55
      multivariavel    R$ 38
      poder de compra  R$ 25

  Reportado com os mesmos numeros por Mix Vale, GameVicio, Adrenaline,
  GameCentral, VZone, Guia do ED e Blast.

  A Valve deixou claro que NENHUM preco muda automaticamente: so muda se o
  desenvolvedor mexer.

O GIRO. O preco de um jogo no Brasil nunca foi "o dolar convertido". Agora e
explicitamente uma ESCOLHA de quem publica, entre tres contas diferentes, e o
mesmo produto pode variar mais que o dobro dependendo de qual escolheram.

O QUE O ROTEIRO NAO FAZ: nao diz que os precos vao subir, porque a propria
Valve diz que nada muda sozinho; nao acusa estudio nenhum de escolher o modelo
caro; e nao trata o exemplo de dez dolares como se fosse o preco de um AAA.

DURACAO: o veredito `suspenso` manda escrever o longo no PISO da faixa. O piso
duro da rotina e 8 min; o alvo aqui e ~9 min com 60 cenas, deixando margem
acima do piso. O melhor material vai para o SHORT, que e o que este canal ja
provou que entrega.

TAXA DA VOZ. pt-BR-AntonioNeural: R = 16,68 chars/s, P = 1,040 s/frase.
Densidade do canal: 2,03 frases/cena no longo, 1,67 no short. Orcamento: 60
cenas em 540 s = 6.602 caracteres, 110 por cena. Short: 400 caracteres.

CAPITULOS abrem sempre em layout `titulo` (aprendizado 388). Seis capitulos de
dez cenas — o minimo da faixa da rotina, coerente com o longo no piso.
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


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ------------------------------------------------ 1. O preço nunca foi o dólar
T("Vinte e cinco", "ou cinquenta e cinco",
  "Um jogo de dez dólares na Steam pode custar vinte e cinco reais para você. "
  "Ou cinquenta e cinco. O mesmo jogo, no mesmo dia, na mesma loja.",
  cap="O preço nunca foi o dólar")
T("E a diferença", "não é promoção",
  "E a diferença entre os dois não é promoção, não é imposto e não é o dólar "
  "ter mexido. É uma escolha.")
I("Quem escolhe", "quem publica o jogo",
  "Quem escolhe é o estúdio que publica o jogo. Desde vinte e oito de março "
  "deste ano, ele decide isso entre três contas diferentes.")
T("A gente sempre achou", "que era conversão",
  "A gente sempre tratou preço de jogo no Brasil como conversão de dólar. Pega "
  "o valor lá fora, multiplica pelo câmbio, pronto.")
T("Nunca foi só isso", "e agora está escrito",
  "Nunca foi só isso. A diferença é que agora está escrito, com nome e com "
  "tabela, e dá para saber qual conta usaram no jogo que você quer.")
L("O que tem aqui", ["As três contas, uma por uma",
                     "Por que o mesmo jogo varia o dobro",
                     "Como descobrir qual usaram"],
  "Três coisas. As três contas, uma por uma. Por que elas afastam tanto o preço "
  "final. E como descobrir qual delas usaram.")
I("Antes de começar", "nada muda sozinho",
  "Uma coisa importante antes de começar, porque muita gente entendeu errado. "
  "Nenhum preço muda automaticamente. Só muda se o estúdio mexer.")
T("Então isto não é", "um vídeo de pânico",
  "Então isto não é um vídeo dizendo que tudo vai encarecer amanhã. É um vídeo "
  "sobre como o número que você paga é montado.")
T("E vale para tudo", "que você comprar",
  "E vale para qualquer jogo que você for comprar daqui para a frente, não só "
  "para o lançamento da semana.")
C("Vamos às contas", "começando pela mais simples",
  "Vamos às contas. Começando pela mais simples, que também é a mais cara.")

# ---------------------------------------------------- 2. Conta um: só o câmbio
T("Câmbio simples", "a conta óbvia",
  "A primeira conta é a que todo mundo imagina. Pega o preço em dólar e "
  "converte pela cotação do dia. Nada mais entra.",
  cap="Conta um: só o câmbio")
I("Dez dólares viram", "cinquenta e cinco reais",
  "Num jogo de dez dólares, essa conta chega a cinquenta e cinco reais.")
T("E é a mais cara", "das três",
  "É a mais cara das três, e por um motivo que não tem nada de conspiração.")
I("O dólar não sabe", "quanto você ganha",
  "O câmbio mede quanto vale a moeda. Ele não mede quanto custa viver aqui, nem "
  "quanto o brasileiro médio consegue gastar com lazer.")
T("Para o estúdio", "é a conta mais fácil",
  "Para quem publica, é a conta mais simples de manter. Um preço em dólar, uma "
  "tabela, e o mundo inteiro resolvido.")
T("Para você", "é a conta menos favorável",
  "Para quem compra num país de moeda fraca, é a menos favorável das três. "
  "Sempre.")
I("E repare", "isso não é novo",
  "E repare numa coisa. Essa conta sempre existiu. O que mudou foi ela virar "
  "uma opção declarada, ao lado de outras duas.")
T("O que ficou visível", "é a escolha",
  "O que ficou visível não foi o preço. Foi a escolha por trás dele.")
T("Guarde o cinquenta e cinco", "é o teto",
  "Guarde esse cinquenta e cinco. Ele é o teto do nosso exemplo, e as outras "
  "duas contas descem a partir dele.")
C("Agora a oposta", "a conta mais barata",
  "Agora a conta oposta, que é a que mais favorece quem compra daqui.")

# ------------------------------------------- 3. Conta dois: poder de compra
T("Poder de compra", "quanto pesa no seu bolso",
  "A segunda conta não pergunta quanto vale o real. Pergunta quanto o comprador "
  "daquele país consegue gastar.",
  cap="Conta dois: poder de compra")
I("O mesmo jogo", "vinte e cinco reais",
  "No exemplo de dez dólares, essa conta chega a vinte e cinco reais. Menos da "
  "metade da anterior.")
T("A ideia", "é preço proporcional",
  "A ideia por trás dela é que o jogo custe uma fatia parecida da renda em cada "
  "lugar, e não o mesmo número absoluto.")
T("Não é caridade", "é estratégia",
  "E não é caridade. É estratégia de volume: um preço que cabe vende mais "
  "cópias, e pirateia menos.")
I("A troca", "menos por cópia",
  "A troca é clara. O estúdio ganha menos por cópia vendida aqui, apostando que "
  "vende bem mais cópias.")
T("Por isso", "nem todo jogo usa",
  "Por isso nem todo jogo usa essa conta. Ela funciona melhor em jogo com "
  "público grande, e pior em jogo de nicho.")
T("Se o seu jogo", "custa vinte e cinco",
  "Então se um jogo internacional está custando por volta de vinte e cinco "
  "reais aqui, provavelmente foi essa a conta escolhida.")
I("E isso é informação", "sobre o estúdio",
  "E isso diz algo sobre quem publicou. Diz que ele olhou o mercado brasileiro "
  "e decidiu disputar preço.")
T("Falta uma conta", "e é a do meio",
  "Falta a terceira, que é a do meio, e é também a que mais se parece com o que "
  "a Steam já fazia antes.")
C("A terceira", "mistura tudo",
  "A terceira mistura as duas anteriores com uma coisa a mais.")

# -------------------------------------------- 4. Conta três: a multivariável
T("Multivariável", "três coisas juntas",
  "A terceira conta junta câmbio, poder de compra, e uma terceira informação "
  "que ninguém esperava numa tabela de preço de jogo.",
  cap="Conta três: a multivariável")
I("A terceira informação", "quanto custa se divertir",
  "Quanto custa entretenimento na sua região. Cinema, streaming, esses preços "
  "entram na conta.")
T("A lógica", "o jogo compete com o resto",
  "A lógica é que o jogo não compete só com outros jogos. Ele compete com tudo "
  "aquilo em que você gastaria a mesma noite.")
I("No exemplo", "trinta e oito reais",
  "No jogo de dez dólares, essa conta dá trinta e oito reais. Fica entre as "
  "outras duas, como era de esperar.")
T("E ela é a mais próxima", "do que já existia",
  "Essa é a conta mais próxima do que a Steam vinha usando antes da mudança. "
  "Então é o cenário de menor ruptura.")
I("O preço anterior", "trinta e três reais",
  "Para comparação: antes da mudança, esse mesmo jogo saía por trinta e três "
  "reais. A multivariável fica cinco reais acima disso.")
T("Ou seja", "quase o mesmo lugar",
  "Ou seja, quem escolher a multivariável entrega um preço quase igual ao que "
  "você já pagava. Sem susto.")
T("Agora junte as três", "e olhe o intervalo",
  "Agora junte as três num só lugar, porque é o intervalo que conta a história, "
  "não cada número sozinho.")
B("O mesmo jogo de US$10", ["Poder", "Antes", "Multi", "Câmbio"],
  [0.45, 0.60, 0.69, 1.0],
  "Vinte e cinco. Trinta e três. Trinta e oito. Cinquenta e cinco. Quatro "
  "preços, um produto.")
C("Do menor ao maior", "é mais que o dobro",
  "Do menor ao maior é mais que o dobro. E é isso que muda como você compra.")

# ------------------------------------------ 5. Como descobrir qual usaram
T("Não tem etiqueta", "dizendo qual conta é",
  "A Steam não põe uma etiqueta na página dizendo qual conta o estúdio "
  "escolheu. Mas dá para deduzir, e leva um minuto.",
  cap="Como descobrir qual usaram")
L("Você precisa de", ["O preço em dólar",
                      "O preço em reais",
                      "A cotação do dia"],
  "Você precisa de três coisas. O preço em dólar, o preço em reais, e a cotação "
  "do dólar de hoje.")
I("Divida", "reais pelo preço em dólar",
  "Divida o preço em reais pelo preço em dólar. O resultado é a taxa que aquele "
  "estúdio está usando na prática.")
T("Compare com a cotação", "e a resposta aparece",
  "Compare esse número com a cotação real do dia. Se bater quase igual, é "
  "câmbio simples.")
T("Se for bem menor", "é poder de compra",
  "Se for bem menor que a cotação, é poder de compra. E se ficar no meio do "
  "caminho, é a multivariável.")
I("Por que isso serve", "para esperar ou não",
  "E para que serve saber? Para decidir se vale esperar promoção. Jogo com "
  "preço por poder de compra já está perto do piso dele.")
T("Jogo em câmbio simples", "tem mais gordura",
  "Jogo em câmbio simples tem muito mais gordura para cair numa promoção. A "
  "distância até o preço mínimo é maior.")
T("É a mesma lógica", "de comparar preço em qualquer loja",
  "É a mesma lógica de qualquer compra: saber de onde veio o número diz se ele "
  "ainda tem para onde descer.")
I("E funciona", "em qualquer jogo",
  "E isso funciona para qualquer jogo da loja, não só para lançamento. A conta "
  "é sempre a mesma.")
C("Antes de encerrar", "o que isso não significa",
  "Antes de encerrar, o que este vídeo não está dizendo.")

# ---------------------------------------- 6. O que este vídeo não está dizendo
T("Primeiro", "nada subiu automaticamente",
  "Primeiro, e é o mais importante: nada subiu automaticamente. A Valve foi "
  "explícita nisso. Preço só muda se o estúdio mexer.",
  cap="O que este vídeo não está dizendo")
T("Segundo", "não é vilão escolher o câmbio",
  "Segundo, escolher a conta do câmbio não faz de ninguém vilão. Para estúdio "
  "pequeno, manter uma tabela por país custa trabalho que ele não tem.")
I("Terceiro", "dez dólares não é AAA",
  "Terceiro, o exemplo de dez dólares é um exemplo. Não é o preço de um jogo "
  "grande, e não dá para multiplicar direto.")
T("A proporção viaja", "o valor não",
  "O que viaja entre faixas de preço é a proporção entre as contas, não o valor "
  "em reais.")
I("Quarto", "isso é só a Steam",
  "Quarto, isso vale para a Steam. Loja de console tem regra própria, e o preço "
  "lá pode não seguir nada disso.")
T("E quinto", "eu não sei o futuro",
  "E quinto: eu não sei quantos estúdios vão trocar de conta, nem em que "
  "direção. Ninguém sabe, e quem afirmar está chutando.")
L("O que fica", ["Preço é escolha, não câmbio",
                 "Divida reais por dólar",
                 "Poder de compra já está no piso"],
  "Três coisas para levar. Preço é escolha, não conversão. Divida reais por "
  "dólar para descobrir qual conta usaram. E preço por poder de compra já está "
  "perto do piso.")
T("Uma pergunta", "para os comentários",
  "Uma pergunta que eu quero mesmo: faça essa conta no jogo que está na sua "
  "lista de desejos e escreve o resultado aqui embaixo.")
T("No próximo", "as lojas de console",
  "No próximo vídeo eu faço a mesma conta nas lojas de console, onde a regra é "
  "outra e o preço costuma ser mais teimoso.")
C("Até lá", "divide e confere",
  "Até lá: divide, compara com a cotação, e você já sabe mais que a página do "
  "jogo te contou.")

# ---------------------------------------------------------------- o short
# Aqui vai o MELHOR material, por instrucao do veredito `suspenso`: e o short
# que este canal ja provou que entrega (topo de 92,5 v/d contra 0,15 do longo).
# Abre pelo intervalo, que e o resultado. Orcamento medido: 400 caracteres em
# 6 cenas a 1,67 frases/cena para 35,9 s.
SHORT = [
    {"layout": "titulo", "kicker": "Vinte e cinco", "sub": "ou cinquenta e cinco",
     "nar": "O mesmo jogo de dez dólares pode custar vinte e cinco reais ou "
            "cinquenta e cinco.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Não é promoção", "sub": "nem imposto",
     "nar": "Não é promoção, não é imposto, e não é o dólar ter mexido.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "É escolha", "sub": "de quem publica",
     "nar": "Desde março o estúdio escolhe entre três contas: câmbio, poder de "
            "compra, ou as duas misturadas.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Para descobrir", "sub": "divide",
     "nar": "Para saber qual usaram, divida o preço em reais pelo preço em "
            "dólar.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Deu perto do dólar", "sub": "tem promoção pela frente",
     "nar": "Se der perto da cotação, é câmbio simples — e esse tem muita "
            "gordura para cair em promoção.", "sem_cap": True},
    {"layout": "titulo", "kicker": "As três contas", "sub": "no vídeo",
     "nar": "As três contas, com os números, estão no vídeo do canal.",
     "sem_cap": True},
]

THUMB = {"l1": "R$25 ou R$55", "l2": "pelo mesmo jogo"}

COPY = """# As três contas que decidem o preço de um jogo no Brasil

## TITULO
Steam Mudou Como Seu Jogo é Precificado: R$25 ou R$55 pelo Mesmo US$10

## DESCRICAO
Em 28 de março de 2026 a Valve atualizou as tabelas de conversão das 35 moedas da Steam e lançou um conjunto de ferramentas de precificação regional. A mudança é menos visível que um aumento de preço e mexe em algo mais profundo: quem decide quanto um jogo custa no Brasil, e com base em quê.

A partir dela, quem publica escolhe entre três modelos de conversão.

Câmbio simples — pega o preço em dólar e converte pela cotação. Nada mais entra. É o modelo mais simples de manter e o menos favorável para quem compra em moeda fraca, porque o câmbio mede quanto vale o real, não quanto custa viver aqui. Num jogo de US$10, chega a R$55.

Poder de compra — pergunta quanto o comprador daquele país consegue gastar, e busca um preço que represente uma fatia parecida da renda em cada lugar. No mesmo jogo, R$25. Não é caridade: é aposta em volume, ganhando menos por cópia para vender mais cópias.

Multivariável — mistura câmbio, poder de compra e o preço de outras formas de entretenimento na região, porque um jogo compete com o cinema e com o streaming pela mesma noite. Dá R$38, e é o modelo mais próximo do que a Steam já usava antes.

Para comparação, o mesmo jogo saía por R$33 antes da mudança. Do menor ao maior modelo, o intervalo é de mais que o dobro para um produto idêntico.

E o vídeo mostra como descobrir qual conta usaram em qualquer jogo, sem etiqueta nenhuma na página: divida o preço em reais pelo preço em dólar e compare com a cotação do dia. Se bater quase igual, é câmbio simples. Se ficar bem abaixo, é poder de compra. No meio, multivariável. Isso serve para uma decisão prática — jogo precificado por poder de compra já está perto do piso, e jogo em câmbio simples tem bem mais gordura para cair em promoção.

O que este vídeo NÃO diz: que os preços subiram. A Valve foi explícita — nenhum preço muda automaticamente, só muda se o desenvolvedor mexer. Também não trata o exemplo de US$10 como preço de jogo grande (o que viaja entre faixas é a proporção entre os modelos, não o valor), não julga quem escolhe o câmbio simples, e vale para a Steam — loja de console tem regra própria.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz a conta no jogo que está na sua lista de desejos e escreve aqui: preço em reais dividido pelo preço em dólar, e como isso ficou em relação à cotação de hoje. Quero montar uma lista de quais jogos estão em qual modelo — é o tipo de coisa que nenhuma página da loja mostra e que só dá para saber juntando muita gente.

## HASHTAGS
#Steam #PreçoDeJogos #NívelDoJogo

## TAGS
steam, preço de jogos, precificação regional, valve, jogos no brasil, dólar, poder de compra, promoção steam, games, economia dos games, comprar jogos, preço em reais, mercado de games, jogos baratos, steam brasil

## CONFIGURACAO DE STUDIO
- Idioma: Português (pt-BR) | Categoria: Educação (27)
- Não feito para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Brasil | Licença: Licença padrão do YouTube
- Anúncios no meio: ligados (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
A atualização das tabelas de conversão das 35 moedas da Steam e o lançamento das ferramentas de precificação regional foram anunciados pela Valve em 28 de março de 2026. Os três modelos de conversão (câmbio simples, poder de compra e multivariável) e os valores usados como exemplo para um jogo de US$10 — R$33 antes da mudança, R$55 no câmbio simples, R$38 no multivariável e R$25 no poder de compra — foram reportados com os mesmos números por Mix Vale, GameVicio, Adrenaline, GameCentral, VZone, Guia do ED e Blast. Consultado em 20 de agosto de 2026. A Valve declarou que nenhum preço é alterado automaticamente: a mudança só ocorre se o desenvolvedor atualizar os valores do próprio jogo. Este vídeo não afirma que os preços aumentaram, não estima quantos estúdios vão trocar de modelo nem em que direção, não trata o exemplo de US$10 como preço de um título AAA, e trata apenas da Steam — lojas de console operam com regras próprias.
"""

SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-005",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#F2F2F7", "c1": "#FF4D6D", "c2": "#4CC9F0", "bg": "#0F1020"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "nivel-do-jogo-005.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
