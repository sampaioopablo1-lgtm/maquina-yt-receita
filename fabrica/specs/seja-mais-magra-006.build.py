#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-006.

ALAVANCA ATACADA: **A — conversao short -> inscrito**. Numero de partida:
**0,00%**. Cinco shorts, 55 views somadas, zero inscritos. Dez videos no canal,
zero inscritos.

E aqui o numero e mais duro que em qualquer outro canal da frota: os CINCO
LONGOS somam **ZERO view**. Nao "poucas": zero, os cinco. Veredito `canal frio`.

O QUE DEU CERTO, e e pouco mas e legivel. Short a short:

    32 views  3,99 v/d  "Ozempic e Mounjaro: O Que Voce REGANHA Nao E o
                         Que Voce PERDEU"
    19 views  2,64 v/d  "Produtos com Proteina: A Conta por Grama"
     2 views  0,43 v/d  "Semaglutida Generica Aprovada"
     1 view   0,19 v/d  "Shake e Termogenico: 189 Alegacoes Permitidas"
     1 view   0,07 v/d  "Ozempic natural? A Anvisa acabou de proibir 3"

Os dois primeiros falam do CORPO ou do BOLSO de quem assiste, na segunda
pessoa, e contradizem a intuicao. Os tres ultimos noticiam uma decisao de
orgao. E a mesma separacao do aprendizado 487, num terceiro canal e num
terceiro idioma.

O QUE VOU MUDAR: eixo novo (o veredito de `canal frio` manda), mantendo a forma
que mediu melhor — conta na segunda pessoa sobre algo que a pessoa tem na mao.

--------------------------------------------------------------------- A PAUTA

Eixo: **como ler a tabela nutricional**. Nunca usado. Os publicados cobrem
ozempic natural, reganho pos-Ozempic, proteina por grama, shake e termogenico,
e semaglutida generica.

E ele resolve um problema que este canal tem e que nao e de audiencia: e um
canal de saude e emagrecimento, onde ensinar "faca a conta em voce mesmo" pode
virar conselho medico. Aritmetica de ROTULO nao tem esse risco — e leitura de
embalagem, nao prescricao. O video ensina a comparar dois produtos, e nao diz
a ninguem o que comer.

FONTES INSTITUCIONAIS, duas rotas independentes que se confirmam:

  1. ANVISA (gov.br/anvisa, pagina de rotulagem nutricional e os comunicados
     de 2020 e 2022):
       RDC 429/2020 e IN 75/2020 ..... em vigor desde 9 de outubro de 2022.
       passou a ser obrigatorio ...... declarar acucares TOTAIS e ADICIONADOS.
       passou a ser obrigatorio ...... declarar valor energetico e nutrientes
                                       por 100 g ou 100 ml, e a propria Anvisa
                                       diz para que serve: "para ajudar na
                                       comparacao de produtos".
       passou a ser obrigatorio ...... o numero de PORCOES POR EMBALAGEM.
       tabela ........................ so letra preta em fundo branco.
       rotulagem frontal ............. lupa com "ALTO EM" para acucares
                                       adicionados, gorduras saturadas e
                                       sodio, na parte SUPERIOR da face
                                       frontal. Tres nutrientes porque lista
                                       exaustiva diluiria a atencao.

  2. O TEXTO DAS NORMAS, hospedado fora do portal: a RDC 429/2020 no
     bvsms.saude.gov.br e no antigo.anvisa.gov.br, e a IN 75/2020 espelhada
     por vigilancias sanitarias estaduais e municipais.

O QUE FOI DESCARTADO, e vai dito no AVISO: os LIMITES NUMERICOS da lupa
(quantos gramas de acucar adicionado por 100 g disparam o "ALTO EM") moram no
Anexo XV da IN 75/2020, e eu NAO consegui confirma-los em duas fontes oficiais
— a busca devolveu o numero de acucar para solido e bebida mas nao fechou o de
sodio nem o de gordura saturada, e uma das passagens dizia "por porcao" onde a
outra dizia "por 100 g". Entao os limites nao entram no video. O roteiro foi
construido para NAO precisar deles: a conta que ele ensina usa so os numeros
que estao no proprio rotulo.

A CONTA, na segunda pessoa e sem nada alem da embalagem na mao:
  1. nao compare dois produtos pela coluna da PORCAO — as porcoes sao
     escolhidas por cada fabricante e quase nunca sao iguais;
  2. compare pela coluna por 100 g ou 100 ml, que existe por obrigacao e
     justamente para isso;
  3. depois olhe "porcoes por embalagem" e multiplique pelo que voce come de
     verdade, que raramente e uma porcao.

O QUE O VIDEO NAO FAZ: nao recomenda nem desaconselha alimento nenhum, nao
fala de dose, nao cita os limites da lupa, e nao substitui nutricionista nem
medico.
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


# ============================ OS PRIMEIROS 200 SEGUNDOS ======================
# As duas colunas que resolvem a comparação saem nos capítulos 1 a 3.

# ------------------------------------------------------------------- cap 1
T("Dois produtos na mão", "e uma comparação errada",
  "Você está no mercado com dois produtos parecidos na mão, vira os dois e "
  "compara a tabela nutricional. Essa comparação quase sempre sai errada, e "
  "não é culpa sua.",
  cap="Por que a comparação sai errada")
I("O motivo", "a porção não é padronizada",
  "O motivo é simples: a coluna da porção usa a porção que cada fabricante "
  "escolheu. Duas embalagens parecidas costumam declarar porções de tamanhos "
  "bem diferentes.")
I("O efeito", "o menor parece melhor",
  "Quando as porções são diferentes, o produto que declarou a porção menor "
  "aparece com números menores. Ele não é melhor: ele foi medido num pedaço "
  "menor.")
I("E ninguém está mentindo", "os dois estão corretos",
  "Repare que ninguém mentiu na embalagem. Os dois rótulos estão corretos "
  "dentro da regra, e mesmo assim a comparação entre eles não vale.")
I("A boa notícia", "existe coluna para isso",
  "A boa notícia é que existe uma coluna obrigatória que resolve exatamente "
  "isso, e muita gente passa a vida sem reparar nela.")
I("Desde quando", "nove de outubro",
  "As regras novas de rotulagem entraram em vigor em nove de outubro de dois "
  "mil e vinte e dois, por uma resolução e uma instrução normativa da "
  "Anvisa.")
I("O que vem agora", "duas colunas e um número",
  "Nos próximos minutos você vai saber onde olhar: duas colunas da tabela e "
  "um número que quase ninguém lê.")

# ------------------------------------------------------------------- cap 2
T("A coluna que compara", "por cem gramas",
  "Primeira coisa, e é a que resolve o problema lá do mercado.",
  cap="A coluna por cem gramas")
I("O que ficou obrigatório", "por cem gramas ou cem mililitros",
  "A tabela passou a ser obrigada a declarar o valor energético e os "
  "nutrientes por cem gramas, ou por cem mililitros quando o produto for "
  "líquido.")
I("Para que ela existe", "a própria Anvisa diz",
  "E a Anvisa diz para que essa coluna serve, com essas palavras: para "
  "ajudar na comparação de produtos.")
I("Ou seja", "é a única coluna comparável",
  "Ou seja, ela existe justamente porque a coluna da porção não serve para "
  "comparar. Ela põe os dois produtos na mesma base de medida.")
I("Como usar", "mesma linha, mesma base",
  "Na prática: escolha o nutriente que te interessa, ache a linha dele nos "
  "dois produtos, e leia só a coluna por cem gramas.")
I("Um cuidado", "sólido e líquido não se misturam",
  "Um cuidado só: sólido se compara por cem gramas e bebida por cem "
  "mililitros. Comparar um com o outro não faz sentido, porque as bases são "
  "diferentes.")
I("Se o produto não tiver", "é sinal de rótulo antigo",
  "Se você achar um produto sem essa coluna, provavelmente é embalagem antiga "
  "ainda em circulação. A regra vale para o que foi rotulado depois dela.")
I("Onde ela costuma estar", "ao lado da porção",
  "Na maioria dos rótulos ela fica ao lado da coluna da porção, e é fácil "
  "confundir as duas se você estiver com pressa.")

# ------------------------------------------------------------------- cap 3
T("O número esquecido", "porções por embalagem",
  "Segunda coisa, e é a que muda o tamanho do que você realmente come.",
  cap="Porções por embalagem")
I("Também virou obrigatório", "quantas porções tem ali",
  "A mesma regra tornou obrigatório declarar quantas porções tem a "
  "embalagem.")
I("Por que isso importa", "você raramente come uma porção",
  "Isso importa porque quase ninguém come exatamente uma porção. As pessoas "
  "comem o pacote, ou metade dele, e a tabela continua falando de uma porção "
  "só.")
I("A conta", "porções vezes o que você come",
  "Então a conta é direta: veja quantas porções tem na embalagem e "
  "multiplique os números da coluna da porção pelo tanto que você realmente "
  "come.")
I("Exemplo do mecanismo", "o pacote inteiro",
  "Se a embalagem declara quatro porções e você come o pacote inteiro, todos "
  "os números daquela coluna valem quatro vezes.")
I("Não é pegadinha", "é escala",
  "Isso não é pegadinha do fabricante. É só escala: a tabela informa uma "
  "unidade, e quem decide quantas unidades vai comer é você.")
I("E vale para o contrário também", "quem come menos que uma porção",
  "Vale para o outro lado também. Se você come menos do que a porção "
  "declarada, os números da coluna valem menos, e a conta é a mesma "
  "multiplicação, só que para baixo.")
I("Isso já é o método", "duas colunas e um número",
  "E isso já é o método inteiro: compare por cem gramas, depois dimensione "
  "pelo número de porções. O resto do vídeo é o que está em volta disso.")

# ============ até aqui, ~200 segundos. O que segue aprofunda. ===============

# ------------------------------------------------------------------- cap 4
T("Comparando de verdade", "o mesmo erro, desfeito",
  "Vamos refazer a cena do mercado, agora na ordem certa.",
  cap="Refazendo a comparação")
I("O erro típico", "comparar porção com porção",
  "O erro típico é olhar a coluna da porção dos dois produtos e concluir que "
  "o de números menores é o mais leve.")
I("O que fazer no lugar", "ignore a porção primeiro",
  "O certo é ignorar a coluna da porção no primeiro momento. Ela responde "
  "outra pergunta, e não a de comparar dois produtos.")
I("Passo a passo", "linha, coluna, leitura",
  "Ache a linha do nutriente, vá até a coluna por cem gramas, e leia os dois "
  "números lado a lado. Nada além disso.")
I("Só depois", "volte para a porção",
  "Só depois de decidir qual produto você prefere, volte para a coluna da "
  "porção e para o número de porções, para saber quanto você vai consumir de "
  "fato.")
I("A ordem importa", "comparar, depois dimensionar",
  "A ordem é essa e ela importa: primeiro comparar na mesma base, depois "
  "dimensionar para o seu consumo. Invertida, a tabela engana sem mentir.")
I("Duas embalagens do mesmo produto", "o truque aparece",
  "O caso em que isso fica mais visível é o de dois tamanhos do mesmo "
  "produto. Se as porções declaradas forem diferentes, até o mesmo alimento "
  "parece dois alimentos distintos na tabela.")
I("Funciona no mercado mesmo", "leva dez segundos",
  "E isso não é trabalho de casa. Com o produto na mão leva uns dez segundos, "
  "depois que você sabe qual coluna está procurando.")

# ------------------------------------------------------------------- cap 5
T("A lupa da frente", "o que ela diz",
  "Agora a parte da frente da embalagem, que mudou junto com a tabela.",
  cap="A lupa e o que ela diz")
I("O símbolo", "uma lupa com ALTO EM",
  "A rotulagem frontal é uma lupa acompanhada da expressão alto em, impressa "
  "na parte superior da face da frente.")
I("Por que ali em cima", "é onde o olho bate",
  "A posição não é por acaso: é a área que o olho alcança primeiro quando a "
  "pessoa pega o produto na prateleira.")
I("Três nutrientes", "e só três",
  "Ela cobre três nutrientes: açúcares adicionados, gorduras saturadas e "
  "sódio.")
I("Por que só três", "para não diluir a atenção",
  "A própria Anvisa explica a escolha: uma lista exaustiva diluiria a "
  "atenção, então ficaram os de evidência mais robusta de dano por excesso.")
I("O que a lupa não é", "não é proibição",
  "A lupa não proíbe nada e não diz que o produto é ruim. Ela avisa que a "
  "quantidade daquele nutriente ficou acima de um limite definido em norma.")
I("Por que não cito o limite", "não fechou em duas fontes",
  "E eu não vou dizer aqui qual é esse limite. Ele existe num anexo da "
  "instrução normativa, mas eu não consegui confirmar todos os valores em "
  "duas fontes oficiais.")
I("A regra da casa", "número conferido ou nada",
  "Número que não bate em duas fontes oficiais não entra em vídeo, mesmo "
  "quando eu tenho quase certeza. Principalmente aqui, que é assunto de "
  "saúde.")

# ------------------------------------------------------------------- cap 6
T("Açúcar total e adicionado", "duas linhas diferentes",
  "Uma mudança discreta da regra nova, e talvez a mais útil de todas.",
  cap="Açúcar total e açúcar adicionado")
I("O que mudou", "duas linhas onde havia uma",
  "A tabela passou a declarar açúcares totais e também açúcares adicionados, "
  "em linhas separadas.")
I("Por que separar", "nem todo açúcar foi posto ali",
  "A separação importa porque parte do açúcar de um alimento pode ser dele "
  "mesmo, como a fruta do suco, e parte pode ter sido acrescentada durante o "
  "processo.")
I("Onde isso aparece", "produtos parecidos, linhas diferentes",
  "Dois produtos podem ter açúcar total parecido e açúcar adicionado bem "
  "diferente. Sem a segunda linha, essa diferença ficava invisível.")
I("O que fazer com isso", "leia as duas",
  "Então leia as duas linhas, e não só a de cima. E compare pela coluna por "
  "cem gramas, como a gente viu.")
I("Vale para bebida também", "principalmente para bebida",
  "Isso vale muito para bebidas, onde a diferença entre o açúcar próprio da "
  "fruta e o que foi acrescentado costuma ser grande.")
I("Cuidado com a leitura", "adicionado está dentro do total",
  "E cuidado com uma leitura comum: o açúcar adicionado já está contado "
  "dentro do total. As duas linhas não se somam, uma é parte da outra.")
I("O que a segunda linha responde", "quanto foi posto no processo",
  "A pergunta que a segunda linha responde é essa: do açúcar que está aqui, "
  "quanto foi colocado durante a fabricação.")

# ------------------------------------------------------------------- cap 7
T("De onde vem", "e o que eu descartei",
  "De onde saiu tudo isso, e o que eu deixei de fora de propósito.",
  cap="De onde vem e o que descartei")
I("A fonte", "Anvisa",
  "Tudo o que eu afirmei aqui vem da Anvisa: a página de rotulagem "
  "nutricional e os comunicados sobre a entrada em vigor da regra.")
I("As normas", "resolução e instrução normativa",
  "As normas são uma resolução de diretoria colegiada e uma instrução "
  "normativa, as duas de dois mil e vinte, com o texto disponível em "
  "repositórios públicos.")
I("O que eu descartei", "os limites da lupa",
  "O que eu descartei foram os limites numéricos que disparam a lupa. "
  "Ficaram de fora por não fecharem em duas fontes oficiais.")
I("Como eu percebi", "as fontes discordavam",
  "E não foi escrúpulo abstrato: uma das passagens dizia por porção onde "
  "outra dizia por cem gramas. Quando as fontes discordam assim, o número "
  "ainda não está pronto.")
I("Tem revisão em andamento", "consulta pública",
  "Vale saber também que existe uma proposta de revisão dessa regulamentação "
  "em consulta pública. Proposta não é regra, e eu só volto ao assunto "
  "quando virar norma.")
I("Por que insisto nisso", "é assunto de saúde",
  "Insisto porque aqui é assunto de saúde, e número errado em saúde não é "
  "curiosidade. Prefiro dizer menos e ter conferido o pouco que eu disse.")

# ------------------------------------------------------------------- cap 8
T("Na próxima compra", "três gestos",
  "Três gestos para a próxima vez que você estiver com a embalagem na mão.",
  cap="Na próxima compra")
I("Primeiro", "ache a coluna por cem gramas",
  "Ache a coluna por cem gramas, ou por cem mililitros se for bebida. Ela "
  "está lá, por obrigação, em todo produto embalado.")
I("Segundo", "compare só por ela",
  "Compare os dois produtos só por essa coluna, na linha do nutriente que te "
  "interessa. Ignore a porção nessa hora.")
L("Terceiro", ["Quantas porções tem a embalagem",
               "Quanto eu como de verdade",
               "Então quanto isso vale para mim"],
  "Depois olhe quantas porções tem a embalagem, pense em quanto você come de "
  "verdade, e multiplique.")
I("O gesto que sobra", "olhar a frente",
  "E de passagem, olhe a parte de cima da frente. Se tiver lupa, você já sabe "
  "o que ela está dizendo e o que ela não está.")
I("Uma vez basta", "depois vira automático",
  "Faça isso uma vez com calma. Depois que você localiza a coluna certa uma "
  "vez, o olho passa a achar sozinho.")
I("Resumindo", "comparar, depois dimensionar",
  "Resumindo: compare por cem gramas, dimensione pelo número de porções, e "
  "leia as duas linhas de açúcar.")
C("Seja Mais Magra e Saudável", "faça no próximo rótulo",
  "Faça isso uma vez, no próximo produto que você pegar. Aqui a gente pega um "
  "número que já está na sua mão e transforma numa conta que você mesma faz. "
  "Se é isso que você procura, se inscreve.")


# -------------------------------------------------------------------- short
#
# A conta inteira, na segunda pessoa, sobre a embalagem que a pessoa TEM.
# Nenhum limite nao confirmado, nenhuma recomendacao alimentar.
SHORT = [
    {"layout": "titulo", "kicker": "Dois produtos", "sub": "a comparação sai errada",
     "nar": "Quando você compara a tabela de dois produtos, quase sempre sai "
            "errado. E não é culpa sua.", "sem_cap": True},
    {"layout": "item", "kicker": "O motivo", "preco": "as porções são diferentes",
     "nar": "Cada fabricante escolhe o tamanho da porção. Quem declara a "
            "porção menor aparece com números menores.", "sem_cap": True},
    {"layout": "item", "kicker": "Use a outra coluna", "preco": "por cem gramas",
     "nar": "Compare pela coluna por cem gramas. Ela é obrigatória desde dois "
            "mil e vinte e dois, e existe exatamente para comparar.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Depois", "preco": "porções por embalagem",
     "nar": "Só então olhe quantas porções tem o pacote, e multiplique pelo "
            "que você come de verdade.", "sem_cap": True},
    {"layout": "cta", "kicker": "Seja Mais Magra", "sub": "no próximo rótulo",
     "nar": "Faça isso no próximo produto que você pegar na mão.",
     "sem_cap": True},
]

COPY = """# Tabela nutricional: a coluna que compara e o numero que dimensiona

## TITULO
Tabela Nutricional: a Coluna Certa para Comparar Dois Produtos (e o Número que Todo Mundo Pula)

## DESCRICAO
Você está no mercado com dois produtos parecidos na mão, vira os dois e compara a tabela nutricional. Essa comparação quase sempre sai errada — e não é culpa sua. A coluna da porção usa a porção que cada fabricante escolheu, e duas embalagens parecidas costumam declarar porções de tamanhos diferentes. Quando as porções são diferentes, o produto que declarou a porção menor aparece com números menores: ele não é melhor, ele foi medido em pedaço menor. Este vídeo mostra as duas colunas e o número que resolvem isso, usando só o que já está impresso na embalagem que você tem na mão.

O QUE MUDOU EM 2022 (fonte: Anvisa)

A RDC 429/2020 e a IN 75/2020 entraram em vigor em 9 de outubro de 2022. Com elas passou a ser obrigatório: declarar o valor energético e os nutrientes por 100 g (ou por 100 ml, em líquidos); declarar o número de porções por embalagem; e declarar açúcares totais E açúcares adicionados em linhas separadas. A tabela também passou a admitir apenas letras pretas em fundo branco.

A COLUNA POR 100 g EXISTE PARA COMPARAR — e a própria Anvisa diz isso com essas palavras: a declaração por 100 g ou 100 ml serve "para ajudar na comparação de produtos". É a única coluna que põe dois produtos na mesma base. Cuidado apenas para não misturar: sólido se compara por 100 g, bebida por 100 ml.

O NÚMERO QUE QUASE NINGUÉM LÊ: porções por embalagem. Quase ninguém come exatamente uma porção — as pessoas comem o pacote, ou metade dele. Se a embalagem declara 4 porções e você come o pacote inteiro, todos os números da coluna da porção valem 4 vezes.

A ORDEM IMPORTA: primeiro comparar na mesma base (por 100 g), depois dimensionar para o seu consumo (porções × o quanto você come). Invertida, a tabela engana sem mentir.

A LUPA DA FRENTE: a rotulagem frontal é uma lupa com a expressão "ALTO EM", impressa na parte superior da face frontal, e cobre três nutrientes — açúcares adicionados, gorduras saturadas e sódio. A Anvisa explica a escolha de apenas três: uma lista exaustiva diluiria a atenção, então ficaram os de evidência mais robusta de dano por excesso. A lupa não proíbe nada e não diz que o produto é ruim; ela avisa que a quantidade daquele nutriente ficou acima de um limite definido em norma.

AÇÚCAR TOTAL E AÇÚCAR ADICIONADO são linhas diferentes, e essa é talvez a mudança mais útil: parte do açúcar pode ser do próprio alimento e parte pode ter sido acrescentada no processo. Dois produtos podem ter açúcar total parecido e adicionado bem diferente — sem a segunda linha, isso ficava invisível.

Este vídeo não recomenda nem desaconselha alimento nenhum, não fala de dose de medicamento, e não substitui nutricionista nem médico.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Pega o produto embalado mais próximo de você agora e responde uma coisa só: quantas porções diz que tem a embalagem? Não precisa dizer a marca. Quero ver quantas de vocês descobrem que o pacote que costumam comer inteiro declara três ou quatro porções — porque é aí que a conta muda de tamanho.

## HASHTAGS
#RotulagemNutricional #LerRotulo #SejaMaisMagra

## TAGS
tabela nutricional, rotulo de alimentos, rotulagem nutricional, por 100g, porcoes por embalagem, acucar adicionado, acucares totais, lupa alto em, rotulagem frontal, anvisa, rdc 429, in 75, comparar produtos, leitura de rotulo, alimentacao baseada em evidencia

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
As afirmacoes vem da ANVISA por duas rotas independentes que se confirmam: (1) o portal gov.br/anvisa, na pagina de rotulagem nutricional e nos comunicados sobre a entrada em vigor; e (2) o TEXTO das normas hospedado fora do portal — a RDC 429/2020 no bvsms.saude.gov.br e no repositorio antigo da Anvisa, e a IN 75/2020 espelhada por vigilancias sanitarias estaduais e municipais. O que esta confirmado nas duas rotas: a entrada em vigor em 9 de outubro de 2022; a obrigatoriedade de declarar valor energetico e nutrientes por 100 g ou 100 ml, com a finalidade declarada pela propria Anvisa de "ajudar na comparacao de produtos"; a obrigatoriedade do numero de porcoes por embalagem; a declaracao separada de acucares totais e adicionados; a tabela em letra preta sobre fundo branco; e a rotulagem frontal em lupa com "ALTO EM" para acucares adicionados, gorduras saturadas e sodio, na parte superior da face frontal, com a justificativa de tres nutrientes para nao diluir a atencao. O QUE FOI DESCARTADO, e o video diz isso em voz alta: os LIMITES NUMERICOS que disparam a lupa. Eles moram no Anexo XV da IN 75/2020, e nao consegui confirmar todos em duas fontes oficiais — a busca devolveu o valor de acucar para solido e para bebida, mas nao fechou o de sodio nem o de gordura saturada, e uma passagem dizia "por porcao" onde outra dizia "por 100 g". Numero que nao bate em duas fontes oficiais nao entra, ainda mais em assunto de saude. Por isso o roteiro foi construido para NAO depender desses limites: a conta que ele ensina usa apenas os numeros impressos no proprio rotulo. Ha ainda uma proposta de revisao dessa regulamentacao em consulta publica; proposta nao e regra, e o video diz isso e nao trata a revisao como certa.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seja-mais-magra-006.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-006",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#22303C", "c1": "#2E8B7A", "c2": "#D98324",
               "bg": "#F6F3EE"},
    "thumb": {"l1": "Por 100 g", "l2": "nao por porcao"},
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/seja-mais-magra-006.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
