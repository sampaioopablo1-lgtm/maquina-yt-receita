#!/usr/bin/env python3
"""Monta a spec labtreinamento-006.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA, e ele e o pior da frota:

    labtreinamento-002  short   21 views  0 insc  ret 26,6%
    labtreinamento-003  short   20 views  0 insc  ret 43,7%
    labtreinamento-004  short    5 views  0 insc  ret 49,8%
    labtreinamento-001  short    1 view   0 insc

    canal inteiro: 8 videos, 75 views, ZERO inscritos

O QUE DEU CERTO: nada que de para medir. Setenta e cinco views em oito videos
nao sustentam conclusao nenhuma, e dizer o contrario seria inventar.

O QUE NAO DEU, e isso da para ver sem estatistica: QUATRO DOS CINCO TITULOS
comecam com "[EXCEL] Planilha de...". O canal esta oferecendo uma FERRAMENTA,
e as tres condicoes do aprendizado 504 nao valem em nenhum deles:

  - "[EXCEL] Planilha de Riscos Psicossociais NR-1"  -> ferramenta, nao a
    conta do dinheiro de quem assiste
  - "NR-10 Atualizada: o Prazo Termina em Junho de 2027" -> tem prazo, mas e
    obrigacao imposta ao EMPREGADOR, nao escolha de quem assiste
  - "[EXCEL] ISO 9001:2026 — Planilha de Transicao"  -> ferramenta de novo

VEREDITO `canal frio`, e a rotina manda EIXO NOVO. Este e o eixo novo.

O QUE MUDEI: saio da obrigacao da empresa e entro na escolha do profissional.
O publico deste canal e tecnico — SST, qualidade, processos — e muitos deles
emitem nota como autonomo. A escolha de aliquota do INSS e a decisao de
dinheiro mais cara que essa pessoa toma, ela decide sozinha, e quase ninguem
faz a conta antes.

As TRES condicoes, agora todas presentes:
  1. o dinheiro E DELE: e a guia que ele paga todo mes
  2. e uma ESCOLHA dele: onze por cento ou vinte, ninguem escolhe por ele
  3. o video entrega a CONTA: quanto custa consertar depois, e quando

OS NUMEROS, e as rotas institucionais

  - Contribuinte individual sem vinculo com empresa contribui a 20% sobre o
    salario de contribuicao, OU a aliquota reduzida de 11%, e nesse caso
    somente sobre o salario minimo.
  - Quem opta pela reduzida NAO tem direito a aposentadoria por tempo de
    contribuicao — so por idade.
  - Para contar aquele tempo, e preciso COMPLEMENTAR com 9% sobre o salario
    minimo usado de base, MAIS juros de mora. O acerto se faz pelo Meu INSS.

    rota 1  INSS (gov.br/inss) — paginas "Contribuicao dos segurados
            facultativo e contribuinte individual", "Plano simplificado" e
            "Regularizacao de Contribuicao Previdenciaria"
    rota 2  Receita Federal (gov.br/receitafederal) — "Contribuicoes
            previdenciarias (pessoas fisicas)"; e o acerto do art. 29 da
            Emenda Constitucional 103/2019, no acervo do Planalto

O QUE FICOU DE FORA, e o video diz em voz alta

  - O VALOR do salario minimo. As aliquotas incidem sobre ele, mas eu nao
    confirmei o valor de 2026 em duas rotas, e o espectador nao precisa dele:
    ele tem o valor da PROPRIA guia na mao, que e melhor que qualquer media.
  - A TAXA de juros de mora da complementacao. Muda conforme o periodo, e
    citar um numero fixo daria uma conta errada para quase todo mundo. O video
    manda simular no Meu INSS, que e onde o calculo e feito de verdade.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ------------------------------------------- 1. A escolha que voce ja fez
T("Você já escolheu", "mesmo sem perceber",
  "Se você emite nota como autônomo, já fez uma escolha que decide como você "
  "vai se aposentar. E é bem provável que ninguém tenha te explicado ela.",
  cap="A escolha que você já fez")
T("Ela está na sua guia", "no código dela",
  "A escolha está na guia que você paga todo mês. No código dela, mais "
  "precisamente, e é uma diferença de dois dígitos.")
L("As duas opções", ["Vinte por cento sobre o que você declarar",
                     "Onze por cento, só sobre o salário mínimo"],
  "São duas. Vinte por cento sobre o valor que você declarar, ou onze por "
  "cento, e nesse caso só sobre o salário mínimo.")
T("A de onze parece melhor", "e é mais barata mesmo",
  "A de onze por cento parece melhor, e é mesmo mais barata todo mês. É por "
  "isso que ela é escolhida com tanta frequência.")
T("Mas ela cobra o preço", "em outro lugar",
  "Só que ela cobra o preço em outro lugar, e num lugar que você só vai "
  "visitar daqui a muitos anos.")
I("O que você vai aprender", "quanto custa consertar",
  "Neste vídeo você vai saber calcular quanto custa consertar essa escolha, "
  "se ela foi a errada para o seu caso. Com o valor da sua guia.")
T("E não é opinião minha", "é regra publicada",
  "E nada disso é opinião. É regra publicada pelo próprio Instituto Nacional "
  "do Seguro Social, e eu digo no fim onde conferir.")
T("Vale uma ressalva", "eu não sei o seu caso",
  "Uma ressalva honesta antes: eu não sei a sua idade nem quanto tempo você "
  "já contribuiu. A conta é sua, e o vídeo te dá o método.")

# ------------------------------------------- 2. O que a reduzida tira
T("O que a reduzida tira", "e é grande",
  "Vamos ao que a alíquota reduzida tira de você. É uma coisa só, mas é "
  "grande, e ela não aparece em lugar nenhum na hora de pagar.",
  cap="O que a reduzida tira")
I("Quem paga onze por cento", "não tem tempo de contribuição",
  "Quem contribui pela alíquota reduzida não tem direito à aposentadoria por "
  "tempo de contribuição. Só por idade.")
T("Leia de novo", "só por idade",
  "Vale ler de novo devagar: só por idade. O tempo que você pagou continua "
  "existindo, mas não conta para aquela porta.")
T("E a diferença entre as duas", "são anos da sua vida",
  "A diferença entre as duas portas costuma ser de anos. Anos em que você "
  "poderia já estar recebendo e vai estar trabalhando.")
T("Ninguém te avisa", "porque a guia não avisa",
  "E ninguém te avisa disso, porque a guia não avisa. Ela só cobra o valor "
  "menor, todo mês, e o valor menor parece uma boa notícia.")
I("A boa notícia real", "dá para consertar",
  "A boa notícia de verdade é outra: dá para consertar. Existe um caminho "
  "oficial, e ele tem nome, prazo e preço.")
T("E repare no detalhe", "o dinheiro não some",
  "Repare num detalhe que confunde muita gente: o dinheiro que você pagou não "
  "some, e o benefício por idade continua garantido. O que some é a outra porta.")
T("Por isso não é golpe", "é uma troca mal explicada",
  "Por isso não chame de golpe. É uma troca legítima, oferecida por lei, e "
  "mal explicada no momento em que a pessoa escolhe.")
T("O nome dele", "complementação",
  "O nome dele é complementação. É disso que trata o resto deste vídeo, e é "
  "por aí que a sua conta começa.")

# ------------------------------------------- 3. Como se conserta
T("Como se conserta", "e quanto custa",
  "O conserto é simples de descrever e não é barato: você paga a diferença "
  "entre o que pagou e o que deveria ter pago.",
  cap="Como se conserta")
I("A diferença", "nove por cento",
  "Como a reduzida é onze e a cheia é vinte, a diferença é de nove por cento "
  "sobre o salário mínimo que serviu de base naquele mês.")
I("E mais", "juros de mora",
  "E sobre esse valor incidem juros de mora, porque é pagamento atrasado. "
  "Quanto mais antigo o mês, mais o juro pesa.")
T("Essa é a parte", "que muda tudo",
  "E essa é a parte que muda a conta inteira. Nove por cento de um mês do ano "
  "passado é uma coisa. De um mês de dez anos atrás é outra bem diferente.")
T("Por isso o tempo", "trabalha contra você",
  "Por isso o tempo aqui trabalha contra você. Cada mês que passa encarece o "
  "conserto dos meses que já passaram.")
I("Onde se faz", "no Meu INSS",
  "O acerto se faz pelo Meu INSS, e é lá que o cálculo com juros aparece "
  "certo, mês a mês, para o seu caso específico.")
T("Você pode consertar em partes", "não precisa ser tudo",
  "E não precisa ser tudo de uma vez. Dá para complementar alguns meses, os "
  "que fizerem diferença para o seu caso, e deixar os outros como estão.")
T("Isso muda a conta", "de impossível para escolhível",
  "Isso costuma mudar a conversa de impossível para escolhível, porque você "
  "passa a comprar exatamente o tempo de que precisa.")
T("Não vou dar taxa de juro", "e vou dizer por quê",
  "Eu não vou dar aqui a taxa de juros. Ela muda conforme o período, e um "
  "número fixo daria uma conta errada para quase todo mundo que assiste.")

# ------------------------------------------- 4. A conta, com a sua guia
T("Agora a sua conta", "com a sua guia na mão",
  "Agora a conta, e você faz com a sua guia na mão. Não precisa de planilha "
  "nem de contador para o primeiro número.",
  cap="A conta com a sua guia")
L("Três coisas da guia", ["O valor que você paga por mês",
                          "O código de pagamento",
                          "Desde quando você paga assim"],
  "Pegue três coisas: o valor que você paga por mês, o código de pagamento, e "
  "desde quando você paga assim.")
T("O código diz qual você é", "e é o mais importante",
  "O código é o mais importante dos três, porque é ele que diz se você está "
  "na alíquota cheia ou na reduzida. Confira antes de tudo.")
I("Primeiro passo", "seu valor dividido por onze",
  "Se você está na reduzida, divida o valor que paga por onze. Isso te dá "
  "quanto vale um ponto percentual na sua base.")
I("Segundo passo", "multiplique por nove",
  "Multiplique esse resultado por nove. Esse é o valor que falta em CADA mês, "
  "antes dos juros.")
I("Terceiro passo", "multiplique pelos meses",
  "Multiplique pelo número de meses que você já pagou assim. Agora você tem a "
  "ordem de grandeza do conserto, sem os juros.")
T("Os juros vêm por cima", "e só o Meu INSS calcula",
  "Os juros vêm por cima disso, e só o sistema calcula certo. Mas você já "
  "sabe se está falando de centenas ou de dezenas de milhares.")
T("Guarde esse número", "ele é o seu ponto de partida",
  "Guarde esse número em algum lugar. Ele é o seu ponto de partida, e é ele "
  "que você vai comparar com o que o sistema devolver.")
T("E é isso que decide", "se vale a pena",
  "E é exatamente esse número que decide se vale a pena consertar, adiar, ou "
  "simplesmente mudar de alíquota daqui para frente.")

# ------------------------------------------- 5. Quando NAO vale consertar
T("Quando não vale", "e isso quase não se fala",
  "Agora a parte que quase nenhum vídeo faz: quando NÃO vale a pena "
  "consertar. Porque existem casos assim, e vários.",
  cap="Quando não vale consertar")
T("Se você já está perto da idade", "a outra porta chega antes",
  "Se você já está perto da idade da aposentadoria por idade, a porta que "
  "você já tem pode chegar antes da que você compraria.")
T("Se o conserto custa demais", "compare com o que ele compra",
  "Se o conserto sai muito caro, compare esse valor com o que ele compra: "
  "quantos meses de antecipação, e de que valor de benefício.")
I("A pergunta certa", "quantos meses eu antecipo",
  "A pergunta certa não é quanto custa. É quantos meses eu antecipo, e quanto "
  "eu recebo a mais por mês depois disso.")
T("Sem esses dois números", "não dá para decidir",
  "Sem esses dois números, ninguém consegue decidir, e quem te disser que "
  "sempre vale a pena não fez a conta.")
T("E tem o meio-termo", "que muita gente ignora",
  "E existe um meio-termo que muita gente ignora: não consertar o passado, "
  "mas mudar de alíquota daqui para frente.")
T("Esse caminho serve bem", "para quem tem tempo pela frente",
  "Esse meio-termo costuma servir bem para quem ainda tem muitos anos de "
  "trabalho pela frente, porque o tempo novo vale igual e não tem juro.")
T("E serve mal", "para quem está no fim",
  "E serve mal para quem está perto do fim da carreira, porque não sobra "
  "tempo suficiente para o novo contar.")
I("Assim", "o passado fica como está",
  "Nesse caminho o passado fica como está, e o tempo novo já entra contando "
  "para as duas portas. Custa mais por mês e nada de uma vez.")

# ------------------------------------------- 6. O que fazer esta semana
T("Esta semana", "três passos curtos",
  "Três passos para esta semana, todos com os seus números e nenhum com os "
  "meus.",
  cap="Três passos esta semana")
L("Primeiro e segundo", ["Abra a sua guia e ache o código",
                         "Some quantos meses você pagou assim"],
  "Primeiro: abra a guia e ache o código de pagamento. Segundo: some quantos "
  "meses você já pagou dessa forma.")
L("Terceiro", ["Entre no Meu INSS",
               "Peça a simulação da complementação"],
  "Terceiro: entre no Meu INSS e peça a simulação da complementação. É lá que "
  "o número com juros aparece certo.")
T("Anote o resultado", "com a data",
  "Anote o resultado com a data do dia. Daqui a seis meses esse número vai "
  "estar maior, e você vai querer saber quanto maior.")
T("Se der um valor alto", "não decida no susto",
  "E se o número vier alto, não decida no susto. Leve as duas perguntas do "
  "capítulo anterior antes de assinar qualquer coisa.")
T("Antes disso, um cuidado", "com quem te procura",
  "Um cuidado antes: assunto de aposentadoria atrai quem vende solução "
  "pronta. Desconfie de quem te dá um número sem olhar a sua guia.")
T("Ninguém calcula isso", "sem os seus dados",
  "Ninguém consegue calcular isso sem os seus dados, e quem afirmar que "
  "consegue está vendendo, não calculando.")
T("O Meu INSS é de graça", "e é a fonte",
  "A simulação no Meu INSS é gratuita e vem da fonte. Comece por ela, e só "
  "depois procure ajuda se o número pedir.")
I("Uma conversa vale", "com quem calcula isso",
  "Vale conversar com quem calcula isso profissionalmente. O que este vídeo "
  "te dá é a pergunta certa para levar, e a ordem de grandeza.")

# ------------------------------------------- 7. Fechamento
T("Uma frase para levar", "se esquecer o resto",
  "Se você esquecer todos os números deste vídeo, leve uma frase só.",
  cap="Uma frase para levar")
T("A alíquota menor", "não é desconto",
  "A alíquota menor não é um desconto. É uma troca: você paga menos agora e "
  "abre mão de uma porta depois.")
T("Trocas não são erradas", "erradas são as não escolhidas",
  "Trocas não são erradas por si. Erradas são as que a gente faz sem saber "
  "que está fazendo, e essa é feita assim todo mês, no Brasil inteiro.")
T("E vale para quem começa agora", "principalmente",
  "Se você está começando a emitir nota agora, isso vale ainda mais para "
  "você. A escolha do primeiro código é a mais barata de acertar.")
T("Acertar no começo", "custa zero",
  "Acertar no começo custa zero. Consertar dez anos depois custa nove por "
  "cento de cada mês, com juros de cada mês.")
T("É a mesma decisão", "com preços muito diferentes",
  "É literalmente a mesma decisão, tomada em dois momentos, com preços "
  "completamente diferentes.")
I("Então confira o código", "hoje",
  "Então confira o código da sua guia hoje. Dois minutos, e você sai sabendo "
  "em qual das duas portas você está.")
T("Dois minutos hoje", "contra anos depois",
  "Dois minutos hoje decidem uma coisa que você só vai sentir daqui a muitos "
  "anos. Poucas decisões têm essa proporção, e essa está na sua gaveta.")
C("Faça a conta e me diga", "em qual você estava",
  "Faça a conta e escreve nos comentários em qual das duas você descobriu que "
  "estava. Se esse tipo de conta te serve, se inscreve — aqui cada regra vira "
  "uma conta que você faz sozinho.")


# ---------------------------------------------------------------------------
# O SHORT: escolha, dinheiro dele, a conta — e aponta para o longo (493).
SHORT = [
    {"layout": "titulo", "kicker": "Se você emite nota", "sub": "como autônomo",
     "nar": "Se você emite nota como autônomo, já fez uma escolha que decide "
            "como vai se aposentar.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Está na sua guia", "sub": "no código dela",
     "nar": "Ela está no código da guia que você paga todo mês. Onze por "
            "cento, ou vinte.", "sem_cap": True},
    {"layout": "titulo", "kicker": "A de onze é mais barata",
     "sub": "e tira uma porta",
     "nar": "A de onze é mais barata. E quem paga ela não tem aposentadoria "
            "por tempo de contribuição. Só por idade.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dá para consertar", "sub": "pagando a diferença",
     "nar": "Dá para consertar pagando nove por cento de diferença em cada "
            "mês, mais juros.", "sem_cap": True},
    {"layout": "cta", "kicker": "Quanto isso dá no seu caso",
     "sub": "e quando não vale",
     "nar": "Quanto isso dá com a sua guia, e quando NÃO vale a pena "
            "consertar, está no vídeo completo aqui embaixo.",
     "sem_cap": True},
]

THUMB = {"l1": "11% ou 20%", "l2": "confira sua guia"}

COPY = """# A alíquota menor não é desconto: é uma troca, e ela é feita sem escolha

## TITULO
INSS do Autônomo: 11% ou 20%? A Escolha na Sua Guia Que Decide a Aposentadoria

## DESCRICAO
Se você emite nota como autônomo, já fez uma escolha que decide como vai se aposentar — e é provável que ninguém tenha explicado ela. A escolha está no código da guia que você paga todo mês, e são duas opções: 20% sobre o valor que você declarar, ou 11%, e nesse caso somente sobre o salário mínimo.

A alíquota de 11% é mais barata todo mês, e é por isso que ela é escolhida com tanta frequência. Mas ela cobra o preço em outro lugar: quem contribui pela alíquota reduzida não tem direito à aposentadoria por tempo de contribuição — apenas por idade. O tempo pago continua existindo, mas não conta para aquela porta, e a diferença entre as duas costuma ser de anos.

Dá para consertar, e o caminho é oficial: chama-se complementação. Como a reduzida é 11% e a cheia é 20%, a diferença é de 9% sobre o salário mínimo que serviu de base naquele mês, acrescida de juros de mora — porque é pagamento atrasado. O acerto é feito pelo Meu INSS, e é lá que o cálculo mês a mês aparece correto para o seu caso.

O vídeo monta a conta com a guia do espectador, sem planilha e sem contador para o primeiro número: pegue o valor que você paga por mês, divida por 11 para saber quanto vale um ponto percentual na sua base, multiplique por 9 para achar o que falta em cada mês, e multiplique pelo número de meses que você já paga assim. Isso dá a ordem de grandeza do conserto antes dos juros — o suficiente para saber se a conversa é de centenas ou de dezenas de milhares.

Há um capítulo inteiro para o que quase não se fala: quando NÃO vale a pena consertar. Se você já está perto da idade, a porta que você já tem pode chegar antes da que compraria. E a pergunta certa nunca é quanto custa, e sim quantos meses eu antecipo e quanto recebo a mais por mês depois disso. Existe ainda o meio-termo que muita gente ignora: não consertar o passado e mudar de alíquota daqui para frente.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Confere o código da sua guia e escreve aqui em qual das duas você descobriu que estava — e, se fizer a simulação no Meu INSS, quanto deu a ordem de grandeza. Tenho curiosidade em ver quanta gente está na reduzida sem saber que está, porque nas conversas que tive esse número parece alto demais para ser acidente individual.

## HASHTAGS
#INSS #Autonomo #LabTreinamento

## TAGS
inss autonomo, contribuinte individual, aliquota 11 ou 20, complementacao inss, aposentadoria por tempo de contribuicao, meu inss, guia da previdencia, carne leao, pro labore, contribuicao previdenciaria, aposentadoria por idade, planejamento previdenciario, profissional tecnico, carreira tecnica, lab treinamento

## CONFIGURACAO DE STUDIO
- Idioma: Português (pt-BR) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Brasil | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 26 de agosto de 2026. As regras deste vídeo foram conferidas em rotas institucionais independentes: (1) INSS, em gov.br/inss — páginas "Contribuição dos segurados facultativo e contribuinte individual", "Plano simplificado" e "Regularização de Contribuição Previdenciária"; (2) Receita Federal, em gov.br/receitafederal — "Contribuições previdenciárias (pessoas físicas)"; e o acerto previsto no art. 29 da Emenda Constitucional nº 103, de 12 de novembro de 2019, no acervo do Planalto. As três afirmações centrais são: o contribuinte individual sem vínculo com empresa contribui a 20% sobre o salário de contribuição ou a 11% incidentes somente sobre o salário mínimo; quem opta pela alíquota reduzida não tem direito à aposentadoria por tempo de contribuição, apenas por idade; e para contar aquele tempo é necessário complementar a contribuição com 9% sobre o salário mínimo usado de base, acrescidos de juros de mora, pelo Meu INSS.

AVISO SOBRE OS NÚMEROS — o que foi descartado e por quê. (a) O VALOR do salário mínimo não é citado: as alíquotas incidem sobre ele, mas o valor de 2026 não foi confirmado em duas rotas oficiais, e o espectador não precisa dele — tem o valor da própria guia, que descreve o caso dele melhor que qualquer média. (b) A TAXA de juros de mora da complementação não é citada: ela varia conforme o período do débito, e um número fixo produziria uma conta errada para quase todos. O vídeo direciona à simulação no Meu INSS, que é onde o cálculo é feito com a taxa correta mês a mês. (c) Não há projeção de valor de benefício futuro: isso depende de todo o histórico contributivo da pessoa. Este vídeo não é consultoria previdenciária nem recomendação individual; ele descreve regras publicadas e ensina a ordem de grandeza, e recomenda expressamente conversar com quem calcula isso profissionalmente antes de decidir.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-006",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1F3A5F", "c1": "#C1462E", "c2": "#E9B44C", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "labtreinamento-006.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
