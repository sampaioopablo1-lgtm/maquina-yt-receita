"""seja-mais-magra-010 — tres categorias, e a caixa diz qual e a sua.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal, deduplicado e com a ULTIMA leitura de
`metricas` (a trava do 549 acusou 170 quedas em 4.046 linhas lifetime nesta
rodada — `max(views)` esta proibido, aprendizados 592 e 594):

    pacote  short -> longo  dur   titulo
    005         2 ->  15    534s  Semaglutida Generica Aprovada: o Que a Anvisa Registrou...
    003        19 ->   2    710s  Produtos com Proteina: A Conta por Grama...
    006        45 ->   1    559s  Tabela Nutricional: a Coluna Certa...
    008         4 ->   1    592s  Semana ou Fim de Semana?
    004         1 ->   1    872s  Shake e Termogenico: 189 Alegacoes Permitidas
    007        40 ->   0    501s  Atividade Fisica: as Duas Faixas Oficiais
    002        32 ->   0    782s  Ozempic e Mounjaro
    001         1 ->   0    764s  "Ozempic Natural" Existe?
    009         0 ->   0    592s  publicado ontem, sem leitura

O QUE DEU CERTO: o 005, com QUINZE views de longo a partir de DUAS de short.
E o unico pacote do canal em que o longo foi achado quase inteiramente FORA do
short, e e o segundo mais curto (534 s). A forma dele: nomeia o ORGAO (Anvisa),
nomeia a substancia, e promete uma distincao factual — o que foi registrado e o
que ainda nao tem.

O QUE NAO DEU, e e a mesma coisa que aparece em todo canal hoje: os dois
MAIORES shorts do canal (45 e 40 views) entregaram UMA e ZERO views de longo. E
o unico titulo com ponto de interrogacao pura (001) deu zero.

O QUE VOU MUDAR: repetir a forma do 005 — orgao nomeado, distincao factual,
sem interrogacao — num eixo que o canal nunca usou, e ficar no piso de oito
minutos. Saiu em 8,7 min.

VEREDITO DO CANAL: `canal frio` (v_maquina_licoes, 8 shorts e 8 longos
medidos, 164 views). Eixo novo e piso de 8 minutos por analogia com
`suspenso`.

EIXO, e por que ele e novo. Os nove pacotes falam de semaglutida generica,
proteina por grama, coluna da tabela nutricional, dia da semana, alegacoes de
shake, faixas de atividade fisica, reganho com Ozempic, produtos proibidos e
variacao da balanca. NENHUM fala do que esta ESCRITO NA CAIXA de qualquer
remedio — e e ali que a lei poe a diferenca entre as tres categorias.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO CITA PRECO, DOSE, MARCA NEM PERCENTUAL DE ECONOMIA. O que
# entra sao DEFINICOES DE LEI, que nao mudam por trimestre, fechadas em DUAS
# instituicoes:
#
#   * planalto.gov.br — texto da Lei 9.787/1999, que altera a Lei 6.360/1976.
#     Os incisos lidos no proprio texto:
#       XX  Medicamento Similar: mesmos principios ativos, mesma concentracao,
#           forma farmaceutica, via, posologia e indicacao do de referencia,
#           podendo diferir so em tamanho e forma, prazo de validade,
#           embalagem, rotulagem, excipientes e veiculos — "devendo sempre ser
#           identificado por nome comercial ou marca";
#       XXI Medicamento Generico: similar a um produto de referencia, "que se
#           pretende ser com este intercambiavel", produzido em geral apos a
#           expiracao da patente, e "designado pela DCB ou, na sua ausencia,
#           pela DCI";
#       XXII Medicamento de Referencia: produto inovador registrado e
#           comercializado no Pais, com eficacia, seguranca e qualidade
#           comprovadas;
#       XXIV Bioequivalencia: equivalencia farmaceutica mais biodisponibilidade
#           comparavel, estudadas sob o mesmo desenho experimental;
#       XVIII e XIX: DCB e DCI sao as denominacoes comuns do principio ativo.
#   * gov.br/anvisa — a pagina de Medicamentos Genericos, que ensina a
#     consultar o registro publico e diz que a busca tem o campo "Categoria
#     Regulatoria", onde "Generico" e uma das opcoes. Isso confirma, pela
#     agencia, que as tres categorias sao categorias REGULATORIAS consultaveis,
#     e da ao espectador o lugar de conferir a propria caixa.
#
# DESCARTADO, e por que: NAO digo que generico e "igual", nem que similar e
# "pior", nem quanto um custa em relacao ao outro. A lei define equivalencia e
# intercambialidade em termos tecnicos, e transformar isso em juizo de valor
# seria dizer mais do que as duas fontes dizem.
#
# TAMBEM FORA: nao oriento ninguem a trocar de medicamento. Trocar e decisao de
# quem prescreve e de quem dispensa, e o video diz isso com todas as letras.
# E nao e orientacao medica.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: a propria caixa dele. A lei diz que o
# similar SEMPRE tem nome comercial e que o generico e designado pela
# denominacao comum. Entao a caixa se classifica sozinha, sem consultar nada —
# e a confirmacao esta no registro publico da agencia.
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


# Link gravado na spec pela busca via `pg_net` dentro do banco, que e onde a
# chave do Pexels mora. Com o link gravado o pacote fica reproduzivel.
BROLL = {
    # Farmacia em funcionamento, sob a cena que diz que TODO medicamento
    # vendido no pais esta numa das tres categorias. 20 s para uma cena de
    # 9,5 s.
    8667456: ("https://videos.pexels.com/video-files/8667456/8667456-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-man-and-a-woman-working-at-a-pharmacy-8667456/"),
    # Pessoa organizando os PROPRIOS medicamentos em casa, sob o capitulo da
    # resposta, que manda pegar uma caixa que esteja em casa agora. 31 s / 7,6 s.
    8581288: ("https://videos.pexels.com/video-files/8581288/8581288-hd_1920_1080_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/a-person-organizing-her-medicine-8581288/"),
    # Observacao em experimento, sob o capitulo da bioequivalencia, que fala de
    # produtos ESTUDADOS sob o mesmo desenho experimental. 27 s / 9,1 s.
    3214096: ("https://videos.pexels.com/video-files/3214096/3214096-hd_1920_1080_25fps.mp4",
              "Pressmaster",
              "https://www.pexels.com/video/a-man-in-deep-focus-of-his-observation-in-an-experiment-3214096/"),
    # Farmaceutico atendendo no balcao, sob o capitulo que explica por que as
    # categorias se confundem — e o primeiro motivo citado e justamente o que
    # acontece no balcao. 55 s / 9,7 s.
    8657656: ("https://videos.pexels.com/video-files/8657656/8657656-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-pharmacist-assisting-an-elderly-woman-in-choosing-the-8657656/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor,
                           "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — a pessoa classifica a propria caixa — fecha no capitulo 3.

# -------------------------------------------------------------------- cap 1
B("São três categorias", "e a sua caixa pertence a uma delas",
  "Todo medicamento vendido no Brasil pertence a uma de três categorias "
  "oficiais. E a caixa que está na sua gaveta já diz qual é a dela.",
  "pharmacy counter with staff working", 8667456,
  cap="São três categorias")
T("Por que isso importa", "porque as três não garantem a mesma coisa",
  "Isso importa porque as três categorias não garantem exatamente a mesma "
  "coisa. O que muda não é a qualidade pela qualidade: é o que foi comprovado.")
T("A primeira", "o de referência",
  "A primeira categoria é o medicamento de referência. É o produto inovador, "
  "registrado e vendido no país, com eficácia, segurança e qualidade comprovadas.")
T("A segunda", "o genérico",
  "A segunda é o genérico. A lei o define como similar a um produto de "
  "referência que se pretende ser com este intercambiável.")
T("A terceira", "o similar",
  "A terceira é o similar. Tem os mesmos princípios ativos, a mesma "
  "concentração, a mesma forma, a mesma via e a mesma indicação do de referência.")
T("Então qual é a diferença", "está no nome impresso",
  "Se similar e genérico têm tanto em comum, onde está a diferença visível? "
  "Ela está no nome impresso na caixa, e a lei determina os dois casos.")
T("E esse é o seu número", "a sua própria caixa",
  "Esse é o dado que só você tem: a caixa que está na sua casa. Daqui a pouco "
  "você vai classificá-la sem consultar nada.")

# -------------------------------------------------------------------- cap 2
T("O que a lei determina", "e está escrito nos incisos",
  "Agora o que a lei determina, e vou ler o sentido de cada inciso em vez de "
  "resumir por fora. São três definições curtas.",
  cap="O que a lei determina")
T("Sobre o similar", "sempre tem marca",
  "Sobre o similar, a lei diz que ele deve sempre ser identificado por nome "
  "comercial ou marca. A palavra que a lei usa ali é sempre.")
T("Sobre o genérico", "designado pela denominação comum",
  "Sobre o genérico, a lei diz que ele é designado pela denominação comum "
  "brasileira, ou, na ausência dela, pela denominação comum internacional.")
T("O que é denominação comum", "o nome da substância",
  "Denominação comum é o nome da substância em si, aquele que não pertence a "
  "nenhum fabricante. É o nome do princípio ativo, e não um nome de produto.")
T("Junte as duas regras", "e a caixa se classifica sozinha",
  "Junte as duas regras e aparece o atalho: se a caixa traz um nome de marca, "
  "ela não é um genérico. Se traz o nome da substância, ela não é um similar.")
T("No que o similar pode diferir", "e a lista é fechada",
  "A lei também lista no que o similar pode diferir do de referência: tamanho "
  "e forma do produto, prazo de validade, embalagem, rotulagem, excipientes e veículos.")
T("E no que não pode", "princípio ativo, dose, forma, via, indicação",
  "E, por consequência, no que ele não pode diferir: princípio ativo, "
  "concentração, forma farmacêutica, via de administração, posologia e indicação.")

# -------------------------------------------------------------------- cap 3
B("Classifique a sua caixa", "três perguntas, nenhuma consulta",
  "Agora é com você. Pegue uma caixa de remédio que esteja em casa e responda "
  "três perguntas, nessa ordem.",
  "person sorting their own medicines at home", 8581288,
  cap="Classifique a sua caixa")
T("Pergunta um", "o nome maior é de marca ou de substância",
  "Pergunta um: o nome em destaque na frente é um nome inventado, de marca, ou "
  "é o nome da substância? Essa única pergunta já separa dois dos três casos.")
T("Pergunta dois", "aparece a palavra genérico",
  "Pergunta dois: a caixa traz a palavra genérico escrita nela? Nos genéricos "
  "essa identificação aparece na embalagem, junto do nome da substância.")
T("Pergunta três", "a substância aparece em algum lugar",
  "Pergunta três: se o nome da frente é de marca, procure o nome da substância "
  "em letra menor. Ele está lá, e é por ele que você compara com qualquer outra caixa.")
T("Agora você já sabe", "e sem abrir nenhum site",
  "Com essas três respostas você já sabe em qual das três categorias a sua "
  "caixa está. Esse é o resultado, e ele não precisou de internet.")
T("Depois, confirme", "no registro público da agência",
  "Depois, se quiser confirmar, a agência mantém uma consulta pública de "
  "medicamentos com um campo chamado categoria regulatória.")
T("É lá que fecha", "o que a caixa diz e o que o registro diz",
  "É ali que a sua leitura fecha: o que você leu na caixa e o que o registro "
  "público mostra devem dizer a mesma coisa. O resto do vídeo é para não ler errado.")

# -------------------------------------------------------------------- cap 4
B("O que é bioequivalência", "e por que ela é o centro de tudo",
  "Primeiro detalhe, e é o centro de tudo: a palavra bioequivalência. Ela "
  "aparece na lei com uma definição técnica e bem estreita.",
  "researcher observing an experiment", 3214096,
  cap="O que é bioequivalência")
T("Duas partes", "equivalência e biodisponibilidade",
  "A definição tem duas partes. A primeira é equivalência farmacêutica: mesma "
  "forma, mesma composição qualitativa e quantitativa do princípio ativo.")
T("A segunda parte", "biodisponibilidade comparável",
  "A segunda é biodisponibilidade comparável. Biodisponibilidade, na própria "
  "lei, é a velocidade e a extensão com que o princípio ativo é absorvido.")
T("E sob o mesmo desenho", "comparados do mesmo jeito",
  "E a lei acrescenta uma condição: os produtos têm que ser estudados sob um "
  "mesmo desenho experimental. Comparação feita de jeitos diferentes não serve.")
T("Por que isso é exigente", "mesma substância pode absorver diferente",
  "Isso é exigente porque dois produtos com a mesma substância podem ser "
  "absorvidos em velocidades diferentes, dependendo de como foram feitos.")
T("É aí que entram os excipientes", "o que não é princípio ativo",
  "E é aí que os excipientes importam. Eles são a parte que não é princípio "
  "ativo, e a lei permite que o similar os tenha diferentes.")
T("Então a palavra chave", "é comprovado, não parecido",
  "Por isso a palavra que decide não é parecido. É comprovado, com estudo, sob "
  "o mesmo desenho — e é isso que separa uma afirmação de uma suposição.")

# -------------------------------------------------------------------- cap 5
B("Onde as pessoas erram", "e quase nunca é má-fé",
  "Agora a parte mais mal lida. Há vários motivos legítimos para alguém se "
  "confundir entre as três categorias, e nenhum deles é desatenção.",
  "pharmacist assisting a customer at the counter", 8657656,
  cap="Onde as pessoas erram")
T("Primeiro motivo", "as caixas se parecem",
  "Primeiro motivo: as embalagens se parecem muito. A lei permite que o "
  "similar tenha rotulagem e embalagem próprias, então o visual não é pista.")
T("Segundo motivo", "a farmácia fala em marca",
  "Segundo motivo: no balcão quase todo mundo chama o remédio pelo nome mais "
  "conhecido, que costuma ser o de marca, mesmo quando entrega outra coisa.")
T("Terceiro motivo", "a receita pode vir dos dois jeitos",
  "Terceiro motivo: a receita pode vir com o nome da substância ou com um nome "
  "comercial, e isso muda o que a pessoa espera ver na caixa.")
T("Quarto motivo", "o mesmo fabricante faz mais de um",
  "Quarto motivo: um mesmo fabricante pode ter produtos nas três categorias. "
  "Reconhecer a empresa não diz em qual categoria aquele produto está.")
T("Quinto motivo", "a palavra genérico virou gíria",
  "Quinto motivo: no dia a dia a palavra genérico virou sinônimo de mais "
  "barato. Na lei ela não significa preço, significa uma categoria de registro.")
T("Então, antes de concluir", "leia a caixa, não a memória",
  "Por isso, antes de concluir qualquer coisa, vale ler a caixa em vez da "
  "memória. A informação está impressa, e ler leva poucos segundos.")

# -------------------------------------------------------------------- cap 6
T("O que isso não quer dizer", "e aqui eu vou ser exata",
  "Agora os limites, e vou ser exata, porque é aqui que um vídeo como este "
  "costuma dizer mais do que as fontes dizem.",
  cap="O que isso não quer dizer")
T("Não digo que um é melhor", "a lei define, não classifica",
  "Primeiro: não estou dizendo que uma categoria é melhor que a outra. A lei "
  "define o que cada uma é e o que cada uma precisa comprovar.")
T("Não falo de preço", "preço não está na definição",
  "Segundo: não falei de preço em nenhum momento, e não vou falar. Preço não "
  "faz parte de nenhuma das definições que eu li, e ele varia por produto, por "
  "farmácia e por mês.")
T("Não mando trocar nada", "isso é de quem prescreve",
  "Terceiro: não estou dizendo para você trocar o seu medicamento. Essa "
  "decisão é de quem prescreve e de quem dispensa, e não de um vídeo.")
T("Não avalio a sua caixa", "eu não a vi",
  "Quarto: não estou avaliando a sua caixa específica. Eu não a vi, e o "
  "registro público existe exatamente para quem precisa confirmar.")
T("E não é orientação médica", "é leitura de rótulo",
  "E quinto: isto não é orientação médica. É leitura de rótulo, com as "
  "definições que estão na lei e na página da agência.")
T("O que você leva", "uma classificação que você mesma fez",
  "O que você leva daqui é uma classificação que você mesma fez, com a caixa "
  "na mão. Isso continua valendo para a próxima caixa, e para a seguinte.")

# -------------------------------------------------------------------- cap 7
T("O que ficou de fora", "e esta parte costuma ser pulada",
  "Agora a parte que quase todo mundo pula. Tem coisa que ficou de fora de "
  "propósito, e eu vou dizer cada uma e por quê.",
  cap="O que ficou de fora")
T("Nenhuma marca", "nem para elogiar nem para criticar",
  "Primeiro: não citei nenhuma marca, nem para elogiar nem para criticar. "
  "O vídeo é sobre categorias de registro, não sobre fabricantes.")
T("Nenhum preço", "nem percentual de economia",
  "Segundo: nenhum preço e nenhum percentual de economia. Esses números mudam "
  "por produto, por farmácia e por mês.")
T("Nenhuma dose", "dose é de quem prescreve",
  "Terceiro: nenhuma dose e nenhuma posologia. Isso está na bula e na receita "
  "de quem acompanha você, e não é o assunto deste vídeo em nenhum momento.")
T("Nada sobre intercambialidade caso a caso", "e esse é um limite real",
  "Quarto, e este é um limite de verdade: eu li a definição de intercambiável "
  "que está na lei, e não digo se um produto específico é intercambiável com outro.")
T("Por que esse limite", "porque depende do registro de cada um",
  "Não digo porque isso depende do registro daquele produto específico, e "
  "quem tem essa informação é o registro público e quem dispensa.")
T("A regra que eu uso", "duas fontes ou não entra",
  "A regra que eu uso aqui é simples: o que não bate em duas fontes oficiais "
  "não entra no vídeo. Preferi ficar com as definições do que arriscar o resto.")

# -------------------------------------------------------------------- cap 8
T("Quatro passos", "do começo ao fim",
  "Agora a verificação inteira em quatro passos, para você fazer depois que "
  "este vídeo terminar.",
  cap="Quatro passos")
T("Passo um", "pegue uma caixa",
  "Passo um: pegue uma caixa de remédio que esteja em casa agora. Qualquer "
  "uma serve, e é melhor começar por uma que você usa com frequência.")
T("Passo dois", "leia o nome maior",
  "Passo dois: leia o nome em destaque na frente e decida se é um nome de "
  "marca ou o nome de uma substância. Essa decisão é quase sempre imediata.")
T("Passo três", "procure a substância em letra menor",
  "Passo três: se o nome da frente for de marca, ache o nome da substância em "
  "letra menor. Anote esse nome, porque é por ele que tudo se compara.")
T("Passo quatro", "confirme no registro público",
  "Passo quatro: abra a consulta pública de medicamentos da agência e procure "
  "pelo nome da substância, olhando o campo de categoria regulatória.")
T("Anote em uma linha", "substância, categoria, data",
  "Anote numa linha o nome da substância, a categoria que você encontrou e a "
  "data de hoje. Uma linha por caixa, na mesma folha.")
T("E repita quando trocar", "a categoria pode mudar de caixa para caixa",
  "Repita isso sempre que comprar de novo, porque a caixa seguinte pode ser de "
  "outra categoria mesmo sendo a mesma substância.")
T("Essa é a parte que fica", "o hábito, não o vídeo",
  "E é esse hábito que fica depois, não este vídeo. Ler a caixa leva menos "
  "tempo do que procurar a resposta pronta na internet.")

C("Escreva só a categoria", "não escreva o remédio",
  "Nos comentários escreva só em qual das três categorias a sua caixa estava. "
  "Não escreva o nome do remédio nem para que você usa.")

THUMB = {"l1": "Três", "l2": "categorias"}


SHORT = [
    {"layout": "titulo", "kicker": "Três categorias oficiais",
     "sub": "e a caixa diz qual é a sua",
     "nar": "Todo remédio no Brasil está em uma de três categorias oficiais. "
            "A sua caixa já diz qual é.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Um", "sub": "o similar sempre tem marca",
     "nar": "Um: a lei diz que o similar deve sempre ser identificado por nome "
            "comercial ou marca.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dois", "sub": "o genérico leva o nome da substância",
     "nar": "Dois: o genérico é designado pela denominação comum, que é o nome "
            "da própria substância.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Três", "sub": "o de referência é o inovador",
     "nar": "Três: o de referência é o produto inovador registrado e vendido "
            "no país.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Agora olhe", "sub": "marca ou substância",
     "nar": "Olhe o nome maior da sua caixa. Se é marca, não é genérico. Se é "
            "a substância, não é similar.", "sem_cap": True},
]


COPY = """# seja-mais-magra-010

## TITULO
Genérico, Similar ou Referência: as 3 Categorias e o Que Está Escrito na Caixa

## TITULO SHORT
Genérico ou similar: olhe o nome na caixa

## DESCRICAO
Todo medicamento vendido no Brasil pertence a uma de três categorias oficiais —
referência, genérico e similar — e a caixa que está na sua gaveta já diz qual é
a dela. Este vídeo não cita preço, dose nem marca. O que ele mostra são as
definições que estão na lei, e como usá-las para classificar a sua própria
caixa em poucos segundos, sem abrir nenhum site.

A Lei 9.787 de 1999, que alterou a Lei 6.360 de 1976, define as três. O
medicamento de referência é o produto inovador, registrado e comercializado no
país, com eficácia, segurança e qualidade comprovadas. O genérico é definido
como similar a um produto de referência que se pretende ser com este
intercambiável, e — este é o ponto — é designado pela Denominação Comum
Brasileira ou, na ausência dela, pela Denominação Comum Internacional, ou seja,
pelo nome da própria substância. O similar tem os mesmos princípios ativos, a
mesma concentração, forma farmacêutica, via de administração, posologia e
indicação do de referência, podendo diferir apenas em tamanho e forma do
produto, prazo de validade, embalagem, rotulagem, excipientes e veículos — e,
nas palavras da lei, deve sempre ser identificado por nome comercial ou marca.

Junte as duas regras e aparece o atalho que este vídeo ensina: se a caixa traz
um nome de marca em destaque, ela não é um genérico; se traz o nome da
substância, ela não é um similar.

A lei também define bioequivalência, e a definição é estreita: equivalência
farmacêutica entre produtos na mesma forma farmacêutica, com idêntica
composição qualitativa e quantitativa de princípio ativo, e biodisponibilidade
comparável quando estudados sob um mesmo desenho experimental. Biodisponibilidade,
ainda na lei, é a velocidade e a extensão de absorção do princípio ativo. Por
isso a palavra que decide não é parecido: é comprovado.

Antes de concluir qualquer coisa, o vídeo lista cinco motivos legítimos para
alguém confundir as categorias: as embalagens se parecem; no balcão o remédio é
chamado pelo nome mais conhecido; a receita pode vir com o nome da substância ou
com um nome comercial; o mesmo fabricante pode ter produtos nas três
categorias; e no dia a dia a palavra genérico virou sinônimo de mais barato,
embora na lei ela signifique uma categoria de registro.

Para confirmar, a Anvisa mantém uma consulta pública de medicamentos em que a
busca tem o campo Categoria Regulatória, com Genérico entre as opções.

Este vídeo não diz que uma categoria é melhor que outra, não fala de preço, não
orienta ninguém a trocar de medicamento — essa decisão é de quem prescreve e de
quem dispensa — e não é orientação médica.

Capítulos:
00:00 São três categorias
01:05 O que a lei determina
02:10 Classifique a sua caixa
03:15 O que é bioequivalência
04:20 Onde as pessoas erram
05:25 O que isso não quer dizer
06:30 O que ficou de fora
07:35 Quatro passos

Nos comentários escreva só em qual das três categorias a sua caixa estava — não
escreva o nome do remédio nem para que você usa.

## DISCLOSURE
A narração e os visuais deste vídeo foram produzidos com inteligência
artificial. As definições citadas vêm do texto da lei e da página da agência
reguladora, mencionados na descrição.

## HASHTAGS
#Medicamentos #Genericos #LeituRaDeRotulo

## TAGS
medicamento generico, medicamento similar, medicamento de referencia, diferenca generico e similar, lei 9787, bioequivalencia, denominacao comum brasileira, como ler caixa de remedio, categoria regulatoria anvisa, consulta publica medicamentos, intercambiavel, principio ativo, excipientes, rotulagem de medicamento, registro de medicamento

## COMENTARIO FIXADO
Quatro passos: pegue uma caixa → leia o nome em destaque e decida se é marca ou
substância → se for marca, ache a substância em letra menor e anote → confirme
na consulta pública de medicamentos da agência, no campo categoria regulatória.
Atalho da lei: se tem nome de marca, não é genérico; se tem o nome da
substância, não é similar. Escreva aqui só a categoria, não o remédio.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seja-mais-magra-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-010",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#22303C", "c1": "#B04A2F", "c2": "#2E7D6B", "bg": "#FAF6F0"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena, GAP_CENA_S
    grava(SPEC, "fabrica/specs/seja-mais-magra-010.json")
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
        t += duracao_cena(c.get("nar", ""), SPEC["voz"]) + GAP_CENA_S
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s  (ultimo)")
