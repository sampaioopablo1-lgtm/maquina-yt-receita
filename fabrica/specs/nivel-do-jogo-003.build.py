#!/usr/bin/env python3
"""nivel-do-jogo-003 — quantas horas de trabalho custa um jogo AAA em 2026.

PAUTA (PASSO 0 feito HOJE, do zero: o `pautas_banco` deste canal estava VAZIO).
Coletei 49 videos de 90 dias em cinco angulos de busca, calculei views/dia e
gravei todos — 21 outliers e 10 mortos. Mediana dos LONGOS do nicho: 17,35
views/dia, corte de outlier em 52,1. Registrada em `canais.nicho_mediana_vd`.

O eixo PRECO domina os outliers em portugues:
  * osn4DtAc5fY "O Panico Comecou: Jogos de PS3 Disparam de Preco" — 407,2 v/d,
    o MAIOR outlier longo em portugues da amostra.
  * ybkRasGXwgI "Jogos e controles de PS5 nos EUA estao mais caros que no
    Brasil?" — 246,3 v/d.
  * Geclls-M0qg, CZkAyA-7iII, xCYC6ctPAFg, FVnVts39Lm4 — todos acima de 90 v/d.

A ESTRUTURA copiada e a do osn4DtAc5fY: substantivo concreto + verbo de
movimento de preco. O ASSUNTO nao — ele fala de mercado secundario de PS3.

EIXO INEDITO. O canal publicou dois videos: iSby7u2ltf8 sobre inflacao DENTRO
dos jogos (economia virtual) e o pacote 002 sobre a Lei Felca e caixinhas. Este
fala do preco de VAREJO, que nenhum dos dois toca.

NUMEROS — cada um confirmado em duas fontes ou mais:
  * GTA 6 padrao: R$ 449,90 no Brasil e US$ 79,99 nos EUA. Ultimate: R$ 549,90
    e US$ 99,99. Lancamento em 19/11/2026. Tecnoblog, O Tempo, Omelete, Pichau
    Arena, Gamers&Games e GameVicio.
  * Salario minimo 2026: R$ 1.621,00, reajuste de 6,79%. Decreto 12.797
    (planalto.gov.br), Agencia Brasil e a tabela historica da Contabeis.
  * IPCA de 2025: 4,26%. Acumulado de doze meses ate julho de 2026: 4,44%.

O QUE NAO ENTROU, e por que: eu queria comparar com a inflacao acumulada de
trinta anos, mas o IPCA longo nao fechou em duas fontes independentes — as
sinteses publicas so trazem doze meses e ano corrente. Preferi cortar o trecho
a narrar um numero que nao consegui confirmar. Todo numero deste roteiro sai de
tres valores verificados e de aritmetica que roda no rodape deste arquivo.

DIMENSIONAMENTO. pt-BR-AntonioNeural com R = 16,11 chars/s e P = 0,939 s/frase,
n = 132 cenas de PRODUCAO. Medido em producao vale mais que ensaio: hoje o
Ardi (producao, n=282) errou 1,6% e o Marek (ensaio, n=8) errou 10,4%.
"""
import json
import os

SLUG = "nivel-do-jogo"
PACOTE = "nivel-do-jogo-003"

PALETA = {"bg": "#0F1020", "c1": "#FF4D6D", "c2": "#4CC9F0", "ink": "#F2F2F7"}

PRECO_BR = 449.90
PRECO_US = 79.99
MINIMO = 1621.00
JORNADA = 220.0          # horas/mes, a base da CLT


def t(kicker, sub, nar, cap=None, sem_cap=False):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def i(kicker, preco, nar, cap=None, sem_cap=False):
    c = {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


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


def cta(kicker, sub, nar):
    return {"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar,
            "sem_cap": True}


LONGO = [
    # ---------- 1. o numero na tela ----------
    t("QUATROCENTOS E CINQUENTA", "e a pergunta que ninguém faz",
      "Quatrocentos e quarenta e nove reais e noventa centavos. Esse é o preço "
      "do jogo mais esperado de dois mil e vinte e seis. E quase ninguém fez a "
      "pergunta que importa.",
      cap="O número na tela"),
    i("A pergunta certa", "quantas horas",
      "A pergunta não é se está caro. Caro é opinião. A pergunta é quantas "
      "horas do seu trabalho esse número representa."),
    i("Por que essa pergunta", "preço não muda, salário sim",
      "Ela é melhor porque o preço na loja é igual para todo mundo, e o tempo "
      "que cada um leva para juntar esse valor não é."),
    li("O que este vídeo faz",
       ["converte preço em horas", "compara Brasil e Estados Unidos",
        "mostra o que mudou"],
       "Neste vídeo eu converto o preço em horas de trabalho, comparo o mesmo "
       "jogo no Brasil e nos Estados Unidos, e mostro o que realmente mudou na "
       "conta dos últimos anos."),
    i("Por que agora", "o preço saiu",
      "O gatilho deste vídeo é simples: o preço saiu, com data de lançamento "
      "marcada, e virou assunto em todo canal de games do Brasil."),
    i("O que quase todos fizeram", "compararam com o passado",
      "E quase todos fizeram a mesma comparação: com o preço do jogo anterior. "
      "É uma comparação fraca, porque compara dois números que não são da mesma "
      "moeda no tempo."),
    t("REGRA DA CASA", "todo número tem fonte",
      "Regra da casa: todo número que aparecer aqui tem fonte, e a fonte está "
      "na descrição. O que eu não consegui confirmar em duas fontes, eu não "
      "falo.",
      sem_cap=True),

    # ---------- 2. os tres numeros ----------
    t("TRÊS NÚMEROS", "e o resto é conta",
      "A conta inteira sai de três números. Guarde os três, porque o resto é "
      "aritmética.",
      cap="Os três números"),
    i("Número um", "quatrocentos e quarenta e nove reais",
      "O primeiro: a edição padrão custa quatrocentos e quarenta e nove reais e "
      "noventa centavos no Brasil, na loja digital do console."),
    i("Número dois", "setenta e nove dólares",
      "O segundo: a mesma edição padrão custa setenta e nove dólares e noventa "
      "e nove centavos nos Estados Unidos."),
    i("Número três", "mil seiscentos e vinte e um reais",
      "O terceiro: o salário mínimo brasileiro em dois mil e vinte e seis é de "
      "mil seiscentos e vinte e um reais, com reajuste de seis vírgula setenta "
      "e nove por cento."),
    i("De onde vem o terceiro", "decreto",
      "Esse último não é estimativa de mercado. Está em decreto publicado, e o "
      "número é o mesmo em toda fonte que você consultar."),
    i("O que eu deixei de fora", "a inflação de trinta anos",
      "E tem um número que eu queria trazer e não trouxe. Eu queria comparar "
      "com a inflação acumulada de trinta anos, mas não consegui confirmar o "
      "índice longo em duas fontes independentes."),
    i("Por que isso importa", "melhor faltar que errar",
      "Então esse trecho ficou de fora. Prefiro um vídeo com menos números do "
      "que um vídeo com um número que eu não checei."),
    t("AGORA A CONTA", "só divisão",
      "Com esses três, tudo o que vem a seguir é divisão. Nenhuma projeção, "
      "nenhum palpite sobre o futuro.",
      sem_cap=True),

    # ---------- 3. o preco em fracao de salario ----------
    t("PRIMEIRA CONTA", "que fatia do salário",
      "Primeira conta, a mais simples. Que fatia do salário mínimo mensal esse "
      "jogo representa.",
      cap="Que fatia do salário"),
    b("Um jogo dentro do salário mínimo",
      ["preço do jogo", "o que sobra do mínimo"],
      [45, 117],
      "Quatrocentos e quarenta e nove e noventa dividido por mil seiscentos e "
      "vinte e um dá vinte e sete vírgula setenta e cinco por cento. Mais de um "
      "quarto de um salário mínimo inteiro, num único produto."),
    i("Traduzindo", "mais de uma semana",
      "Traduzindo para o calendário: mais de uma semana de trabalho de quem "
      "ganha o mínimo, para levar um jogo."),
    i("E a edição maior", "trinta e três por cento",
      "A edição Ultimate custa quinhentos e quarenta e nove reais e noventa "
      "centavos. Isso é trinta e três vírgula noventa e um por cento do salário "
      "mínimo — um terço do mês."),
    i("Para dimensionar", "quatro dias de comida",
      "Para dimensionar: mais de um quarto do salário é a fatia que muita "
      "família reserva para o mês inteiro de mercado, ou para o aluguel de uma "
      "quitinete em cidade pequena."),
    i("A comparação que não fiz", "não é sobre prioridade",
      "E não estou dizendo que jogo não vale isso. Estou dizendo qual é o "
      "tamanho da decisão, que é diferente de dizer se ela é certa."),
    t("E ISSO É SÓ O JOGO", "o console é outra conta",
      "E repare que estamos falando só do jogo. O aparelho que roda o jogo é "
      "uma conta separada, e bem maior.",
      sem_cap=True),

    # ---------- 4. o preco em horas ----------
    t("SEGUNDA CONTA", "em horas de trabalho",
      "Segunda conta, e é ela que dá a dimensão real. Vamos converter o preço "
      "em horas.",
      cap="O preço em horas"),
    i("A jornada padrão", "duzentas e vinte horas",
      "A base de cálculo da carteira assinada no Brasil é de duzentas e vinte "
      "horas por mês. É o divisor que aparece no seu contracheque."),
    i("O valor da hora", "sete reais e trinta e sete",
      "Divida o mínimo pela jornada. O resultado é sete reais e trinta e sete "
      "centavos por hora, antes de qualquer desconto."),
    b("Horas de trabalho por edição",
      ["edição padrão", "edição Ultimate"],
      [61, 75],
      "Agora divida. A edição padrão custa sessenta e uma horas de trabalho. A "
      "Ultimate custa setenta e cinco horas."),
    i("O que são sessenta e uma horas", "uma semana e meia",
      "Sessenta e uma horas são mais de sete dias de expediente completo. Uma "
      "semana e meia de trabalho, sem contar desconto nenhum."),
    i("Se você ganha o dobro", "trinta horas",
      "Se você ganha o dobro do mínimo, a conta cai pela metade: cerca de trinta "
      "horas. Ainda são quase quatro dias de trabalho."),
    i("Se você ganha cinco mínimos", "doze horas",
      "Com cinco salários mínimos, caem para cerca de doze horas. É por isso "
      "que o mesmo preço não é o mesmo preço para duas pessoas."),
    b("O mesmo jogo, três salários",
      ["um mínimo", "dois mínimos", "cinco mínimos"],
      [61, 30, 12],
      "Olhe as três barras. O preço na loja não mudou nenhuma vez. O que mudou "
      "foi quem está pagando."),
    i("Antes ou depois dos descontos", "isso é antes",
      "E esse número é otimista de propósito. Ele usa o salário bruto. Com os "
      "descontos, as horas necessárias aumentam."),

    # ---------- 5. a comparacao internacional ----------
    i("O console entra na conta", "e é maior",
      "E vale abrir esse parênteses. O aparelho custa vários jogos, e ele vem "
      "antes do primeiro. Quem está entrando na geração agora soma as duas "
      "contas."),
    i("O jogo é o gasto recorrente", "o console é uma vez",
      "A diferença é que o console você compra uma vez por geração, e o jogo "
      "você compra várias vezes por ano. É o gasto que se repete que decide o "
      "orçamento."),
    t("TERCEIRA CONTA", "o mesmo jogo lá fora",
      "Terceira conta, e aqui aparece o número que mais incomoda. O mesmo "
      "arquivo, o mesmo download, nos Estados Unidos.",
      cap="O mesmo jogo lá fora"),
    i("O preço lá", "setenta e nove dólares",
      "Lá a edição padrão sai por setenta e nove dólares e noventa e nove "
      "centavos. É o mesmo produto, entregue pela mesma loja digital."),
    i("O piso salarial de lá", "sete dólares e vinte e cinco",
      "O piso salarial federal americano é de sete dólares e vinte e cinco "
      "centavos por hora, e está parado nesse valor há muitos anos."),
    b("Horas de trabalho no piso salarial",
      ["Estados Unidos", "Brasil"],
      [11, 61],
      "Onze horas de trabalho no piso americano. Sessenta e uma no piso "
      "brasileiro. O mesmo arquivo digital."),
    i("A razão entre as duas", "cinco vezes e meia",
      "A diferença é de cinco vezes e meia. Não em reais, não em dólares: em "
      "horas da própria vida de quem compra."),
    i("Uma ressalva honesta", "o piso não é o salário médio",
      "Uma ressalva antes de seguir: o piso salarial não é o salário médio, nem "
      "lá nem aqui. Ele é o chão, e serve para comparar chão com chão."),
    i("Por que uso o piso", "é o número comparável",
      "Uso o piso porque ele é definido por lei nos dois países, e por isso é "
      "comparável. Salário médio muda de metodologia de um país para outro."),
    i("Se usar o salário médio", "a distância diminui",
      "Se você refizer a conta com o salário médio dos dois países, a distância "
      "diminui — mas não desaparece."),
    t("O PONTO DO VÍDEO", "o preço é global, o salário não",
      "E esse é o ponto do vídeo inteiro. O preço de um produto digital é "
      "praticamente global. O salário que paga por ele não é.",
      sem_cap=True),
    i("Onde entra o imposto", "parte da diferença",
      "Parte da diferença é tributo. Software e serviço digital são tributados "
      "de forma diferente em cada país, e o Brasil está no lado mais pesado "
      "dessa comparação."),
    i("Mas não é tudo imposto", "há decisão de preço",
      "Só que tributo não fecha os cinco vezes e meia sozinho. O resto é "
      "decisão de quanto o mercado local aguenta pagar."),
    i("Como saber qual é qual", "olhe outros países",
      "Dá para separar os dois olhando países com tributação parecida e salário "
      "diferente. Quando o preço acompanha o salário, é decisão comercial."),
    i("Por que isso importa agora", "digital não tem frete",
      "Isso ficou mais visível com o digital. Não há frete, não há estoque, não "
      "há caixa para fabricar. O que resta na diferença de preço é decisão "
      "comercial e imposto."),

    # ---------- 6. o que mudou de verdade ----------
    t("O QUE MUDOU", "e o que não mudou",
      "Agora a parte que costuma ser contada errado: o que de fato mudou nessa "
      "conta.",
      cap="O que mudou de verdade"),
    i("O que subiu", "o preço nominal",
      "O preço nominal dos jogos subiu, e subiu bastante. Isso é fato e ninguém "
      "discute."),
    i("O que também subiu", "o custo de produzir",
      "O custo de produzir também subiu. Equipes maiores, ciclos mais longos, "
      "marketing mais caro. Isso explica parte da alta."),
    i("Um dado do lado da indústria", "a receita migrou",
      "Do lado da indústria há um fato que ajuda a entender: a receita dos "
      "grandes estúdios deixou de vir principalmente da venda de cópias."),
    i("De onde ela vem hoje", "do que vem depois",
      "Ela vem cada vez mais do que acontece depois da compra — passes, itens, "
      "temporadas. O preço de entrada virou uma parte do modelo, não o modelo "
      "inteiro."),
    li("O que a alta NÃO explica sozinha",
       ["a diferença entre países", "o preço da edição maior",
        "o que veio junto"],
       "Mas o custo de produção não explica três coisas. Não explica a "
       "diferença entre países, porque o custo é o mesmo. Não explica o salto "
       "da edição maior. E não explica o que passou a vir junto do jogo."),
    i("O que passou a vir junto", "compras dentro do jogo",
      "Porque o preço de entrada subiu ao mesmo tempo em que as compras dentro "
      "do jogo se tornaram comuns. Antes, o preço cheio comprava o jogo "
      "inteiro."),
    t("A CONTA COMPLETA", "entrada mais o resto",
      "Então a conta honesta de hoje não é o preço de entrada. É o preço de "
      "entrada mais o que vem depois — e essa segunda parte não aparece em "
      "nenhuma etiqueta.",
      sem_cap=True),

    # ---------- 7. o que fazer com esse numero ----------
    i("Um efeito colateral", "a pirataria e o mercado cinza",
      "Essa distância tem um efeito colateral conhecido: quanto maior ela é, "
      "mais gente procura chave de região, conta estrangeira e caminho "
      "irregular."),
    i("Não é recomendação", "é descrição",
      "Não estou recomendando nada disso, e boa parte fere os termos de uso. "
      "Estou descrevendo o que acontece quando o preço se descola do salário."),
    t("O QUE FAZER", "com essa conta",
      "Tudo isso serve para alguma coisa prática. Três usos.",
      cap="O que fazer com a conta"),
    i("Uso um", "converta antes de comprar",
      "Primeiro: antes de comprar qualquer jogo, divida o preço pelo valor da "
      "sua hora. Não pelo salário do mínimo — pelo seu."),
    i("Como achar sua hora", "salário dividido por jornada",
      "Sua hora é o seu salário mensal dividido pela sua jornada mensal. Se "
      "você trabalha as duzentas e vinte horas padrão, é só dividir por "
      "duzentos e vinte."),
    i("Uma regra prática", "compare com o seu mês",
      "Uma regra prática que eu uso: se o preço passar de dez por cento do meu "
      "salário mensal, eu espero. Não porque seja errado, mas porque a espera "
      "quase sempre derruba esse número."),
    i("Uso dois", "espere o preço cair",
      "Segundo: o preço de lançamento é o preço mais alto que aquele jogo vai "
      "ter. Ele cai, e cai bastante, e a espera não custa nada além de "
      "paciência."),
    i("Quanto costuma cair", "muito, e rápido",
      "Jogos grandes costumam ter a primeira queda relevante de preço em poucos "
      "meses, e promoções fortes no primeiro ano. Ninguém precisa te avisar: "
      "basta esperar."),
    i("O custo de esperar", "spoiler e conversa",
      "O custo de esperar não é dinheiro, é social. Você perde a conversa do "
      "lançamento. Isso tem valor real, e cada um mede o seu."),
    i("Uso três", "conte o que vem depois",
      "Terceiro: some o que você costuma gastar dentro do jogo ao longo de um "
      "ano. Esse número costuma surpreender mais que o preço de entrada."),
    li("Três perguntas antes de comprar",
       ["quantas horas isso custa", "quanto cai em seis meses",
        "quanto gasto dentro dele"],
       "Três perguntas, então. Quantas horas do meu trabalho isso custa. Quanto "
       "esse preço cai em seis meses. E quanto eu costumo gastar dentro do jogo "
       "depois de comprar."),

    # ---------- 8. fecho ----------
    li("Onde achar o preço real",
       ["a loja do console", "os comparadores de preço",
        "o histórico de promoções"],
       "E para fazer a conta com dado atual: o preço oficial está na loja do "
       "console, os comparadores mostram o varejo, e o histórico de promoções "
       "mostra quanto aquele jogo já caiu antes."),
    i("O histórico é o mais útil", "ele mostra o padrão",
      "O histórico é o mais útil dos três, porque revela o padrão daquela "
      "publicadora. Algumas derrubam o preço rápido, outras seguram por anos."),
    t("O NÚMERO PARA GUARDAR", "sessenta e uma horas",
      "Se você guardar um número deste vídeo, guarde este: sessenta e uma "
      "horas.",
      cap="O número para guardar"),
    i("Por que esse", "é o preço em vida",
      "Porque ele não está em reais, e por isso não muda com a inflação nem com "
      "o câmbio. Ele está na única moeda que não dá para imprimir."),
    i("O que ele não é", "não é julgamento",
      "E ele não é um julgamento. Sessenta e uma horas pode valer muito a pena "
      "para você, e não valer nada para outra pessoa. Quem decide é quem "
      "trabalhou as horas."),
    i("Uma alternativa que existe", "assinatura",
      "Existe ainda um caminho do meio que a conta favorece: as assinaturas "
      "mensais de catálogo. Elas trocam um pagamento grande por um pequeno e "
      "recorrente."),
    i("Como medir a assinatura", "em horas por mês",
      "E a conta é a mesma: divida a mensalidade pelo valor da sua hora. Se der "
      "menos de uma hora por mês, a decisão é bem diferente. Compare com o "
      "pagamento único lá do começo."),
    i("O que a assinatura não dá", "posse",
      "O que ela não dá é posse. O jogo sai do catálogo e você fica sem ele. É "
      "aluguel, e aluguel tem vantagem e tem desvantagem."),
    t("O QUE MUDA", "saber antes, não depois",
      "O que muda é saber o número antes de clicar em comprar, e não depois de "
      "olhar a fatura.",
      sem_cap=True),
    cta("NÍVEL DO JOGO", "faça a conta com o seu salário",
        "Faça essa conta com o seu próprio salário e escreve nos comentários "
        "quantas horas deu. Se esse tipo de conta te interessa, se inscreve no "
        "canal."),
]

SHORT = [
    {"layout": "titulo", "kicker": "SESSENTA E UMA HORAS",
     "sub": "é o preço real do jogo",
     "nar": "Sessenta e uma horas de trabalho. Esse é o preço do jogo mais "
            "esperado de dois mil e vinte e seis."},
    {"layout": "item", "kicker": "O preço na loja", "preco": "quatrocentos e quarenta e nove",
     "nar": "Quatrocentos e quarenta e nove reais e noventa centavos no Brasil."},
    {"layout": "item", "kicker": "O salário mínimo", "preco": "mil seiscentos e vinte e um",
     "nar": "O mínimo de dois mil e vinte e seis é mil seiscentos e vinte e um "
            "reais. A hora sai por sete e trinta e sete."},
    {"layout": "barras", "kicker": "Horas no piso salarial",
     "itens": ["Estados Unidos", "Brasil"], "alturas": [11, 61],
     "nar": "Nos Estados Unidos, onze horas. No Brasil, sessenta e uma. O mesmo "
            "arquivo digital."},
    {"layout": "item", "kicker": "A diferença", "preco": "cinco vezes e meia",
     "nar": "Cinco vezes e meia, medida em horas da própria vida."},
    {"layout": "cta", "kicker": "A CONTA INTEIRA", "sub": "está no vídeo longo",
     "nar": "A conta inteira, com as fontes, está no vídeo longo aqui do canal."},
]

COPY = """# O preço dos jogos medido em horas de trabalho

## TÍTULO
Preço dos Jogos em 2026: Quantas Horas de Trabalho Custa GTA 6

## DESCRIÇÃO
Quatrocentos e quarenta e nove reais e noventa centavos. Esse é o preço da
edição padrão do jogo mais esperado de 2026 no Brasil. A pergunta que quase
ninguém faz não é se está caro — caro é opinião. É quantas horas do seu trabalho
esse número representa.

Os números usados neste vídeo, todos confirmados em mais de uma fonte:

• GTA 6 edição padrão: R$ 449,90 no Brasil e US$ 79,99 nos Estados Unidos. A
edição Ultimate sai por R$ 549,90 e US$ 99,99. Lançamento em 19 de novembro de
2026.

• Salário mínimo brasileiro em 2026: R$ 1.621,00, com reajuste de 6,79%,
definido por decreto.

• Jornada mensal de referência da CLT: 220 horas. Isso põe a hora do salário
mínimo em R$ 7,37 antes de qualquer desconto.

As contas que saem daí:

• O jogo custa 27,75% de um salário mínimo mensal. A edição Ultimate custa
33,92% — um terço do mês.

• Em horas: 61 horas de trabalho para a edição padrão, 75 para a Ultimate. São
mais de sete dias de expediente completo, usando o salário bruto.

• Nos Estados Unidos, com o piso federal de US$ 7,25 por hora, o mesmo jogo
custa cerca de 11 horas. A diferença é de cinco vezes e meia — não em moeda, mas
em horas da vida de quem compra.

O ponto do vídeo é esse: o preço de um produto digital é praticamente global, e
o salário que paga por ele não é. Sem frete, sem estoque e sem caixa para
fabricar, o que resta na diferença entre países é decisão comercial e imposto.

O vídeo também separa o que a alta de custo de produção explica do que ela não
explica: ela não explica a diferença entre países, porque o custo é o mesmo; não
explica o salto da edição maior; e não explica o preço de entrada ter subido ao
mesmo tempo em que as compras dentro do jogo se tornaram comuns.

No fim ficam três perguntas para antes de comprar: quantas horas do meu trabalho
isso custa, quanto esse preço cai em seis meses, e quanto eu costumo gastar
dentro do jogo depois de comprar.

Isto não é recomendação de compra nem crítica a quem compra. É a conta, com as
fontes na mesa.

Se esse tipo de conta te interessa, se inscreve no canal.

## CAPÍTULOS
{CAPITULOS}

## COMENTÁRIO FIXADO
Faça a conta com o SEU salário: pegue seu salário mensal, divida pela sua jornada
mensal (220h se for a padrão da CLT) e divida o preço do jogo pelo resultado.
Escreve nos comentários quantas horas deu. No mínimo de 2026 dá 61 horas.

## HASHTAGS
#games #economia #gta6

## TAGS
preco dos jogos, GTA 6, GTA 6 preco Brasil, salario minimo 2026, economia dos games, quantas horas de trabalho, poder de compra, jogos caros, industria dos games, preco digital, Brasil x Estados Unidos, custo de vida, PS5, Xbox, financas pessoais

## CONFIGURAÇÕES DO STUDIO
Categoria 27 (Educação). Idioma português do Brasil, faixa de áudio pt-BR. Não é
para crianças. Contém conteúdo sintético — declarado na publicação. Legendas a
partir do arquivo SRT.

## MÚSICA / LICENÇA
Inspired — YouTube Audio Library, sem obrigação de atribuição. Nível de menos
vinte e oito decibéis em relação à narração.

## FONTES
Preço do GTA 6 no Brasil e nos EUA: Tecnoblog, O Tempo, Omelete, Pichau Arena,
Gamers&Games e GameVicio. Salário mínimo 2026: Decreto 12.797 (planalto.gov.br),
Agência Brasil e tabela histórica da Contabeis. Piso federal americano: US
Department of Labor.
"""

TAGS = [
    "preco dos jogos", "GTA 6", "GTA 6 preco Brasil", "salario minimo 2026",
    "economia dos games", "quantas horas de trabalho", "poder de compra",
    "jogos caros", "industria dos games", "preco digital",
    "Brasil x Estados Unidos", "custo de vida", "PS5", "Xbox",
    "financas pessoais",
]

SPEC = {
    "slug": SLUG,
    "pacote": PACOTE,
    "voz": "pt-BR-AntonioNeural",
    "idioma": "pt-BR",
    "trilha": "Inspired",
    "paleta": PALETA,
    "thumb": {"l1": "61 HORAS", "l2": "DE TRABALHO"},
    "longo": LONGO,
    "short": SHORT,
    "copy": COPY,
    "tags": TAGS,
    "fonte_pauta": "osn4DtAc5fY",
}


if __name__ == "__main__":
    hora = MINIMO / JORNADA
    print(f"  hora do minimo      R$ {hora:6.2f}")
    for nome, p in (("padrao", PRECO_BR), ("ultimate", 549.90)):
        print(f"  {nome:9s} {p:7.2f}  = {p/MINIMO*100:5.2f}% do minimo"
              f"  = {p/hora:5.1f} horas")
    print(f"  EUA padrao US$ {PRECO_US} / US$ 7,25 = {PRECO_US/7.25:.1f} horas")
    print(f"  razao BR/EUA = {(PRECO_BR/hora)/(PRECO_US/7.25):.2f}x")

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           f"{PACOTE}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{destino}: {len(LONGO)} cenas, short {len(SHORT)}")
