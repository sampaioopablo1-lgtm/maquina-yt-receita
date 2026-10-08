"""labtreinamento-s006 — o orcamento nao e o custo: falta a hora fora do posto.

ALAVANCA: A (alcance por short). Sexto short solto do labtreinamento.

O QUE DEU CERTO, e por pouco nao virou erro: o `kolejny-s008` saltou de 4 para
**92 views as 2,9 h**, a melhor curva inicial do canal hoje. A tentacao era
creditar isso a correcao de tags do 662 — e seria FALSO: a correcao foi aplicada
ao s009 e ao epomeno-s009, NAO ao s008, que subiu com as oito tags de sempre.
Conferi antes de escrever. Decimo quarto caso em que o instrumento (aqui, a
coincidencia temporal com a minha propria correcao) tentou fabricar a conclusao.

O QUE NAO DEU, e segue ABERTO pelo 661: o `epomeno-s007` esta com ZERO as 8,9 h e
o `s008` com ZERO as 6,9 h. Enquanto isso o kolejny — que o 634 colocava ABAIXO
do epomeno em alcance — tem uma peca com 92 as 2,9 h. Isso pode estar invertendo
a ordem do 634, mas e UMA peca e UMA leitura: anotado, nao afirmado. O s007
chega as 12 h por volta das 22:20 e e la que a pergunta vale.

O QUE VOU MUDAR, e e uma coisa so, de PAUTA: o labtreinamento esta em 5 contra os
7 pedidos, e as oito origens que sobraram sao todas de conformidade corporativa —
o perfil que o 651 mede como ~30x pior. Em vez de abandonar o canal ou fingir que
o numero vai ser bom, escolhi a origem MENOS distante do perfil que funciona:
`Sr6VhvD_aPE`, custo por pessoa de treinamento. Para quem paga a conta de um
negocio pequeno, esse numero E o dinheiro dele, com papel na mao (o orcamento).
Expectativa honesta: faixa de 4 a 70, nao de mil.
NUMERO DE PARTIDA: 80 do short daquele pacote; 62 do melhor solto maduro do canal
hoje.

DE ONDE SAI: longo `Sr6VhvD_aPE` (labtreinamento-012), capitulos "O que entra na
comparacao" e "O que a conta nao decide", que o short original daquele pacote NAO
toca — ele gasta as cinco cenas na divisao pelo numero real em vez do limite da
turma. A entrada errada atacada aqui e outra e tambem aritmetica: comparar
orcamentos pelo PRECO IMPRESSO. Falta somar o que escala com PESSOAS e nao com a
turma — as horas fora do posto — antes de dividir. Com essa parcela dentro, a
ordem das cotacoes muda outra vez.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}` com trilha `Inspired`, decimo primeiro pacote seguido.

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar. Do
PL/26 das 06:22 ficou a FORMA: pergunta ou imperativo em segunda pessoa. Cena 1
pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita preco, nao
# cita tamanho de turma, nao cita carga horaria, nao cita salario e nao nomeia
# norma nem orgao. Conferido A MAO campo por campo, porque o portao `narracao`
# conta QUANTIDADES por frase e NAO pega digito cru (640).
#
# O QUE O VIDEO AFIRMA: que o preco do orcamento e da TURMA, que as horas fora do
# posto escalam com PESSOAS, e que somar essa parcela antes de dividir muda a
# ordem das cotacoes. E aritmetica sobre os papeis do proprio espectador, nao
# afirmacao sobre o mundo. Esta no longo labtreinamento-012 (`Sr6VhvD_aPE`),
# capitulos "O que entra na comparacao" e "O que a conta nao decide".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qualquer preco, qualquer tamanho de turma e qualquer carga horaria —
#       estao no longo, e aqui sao os numeros DO ESPECTADOR;
#   (2) se a hora fora do posto deve ou nao ser contada como custo contabil — e
#       discussao de metodo que depende do regime de cada empresa e esta no longo;
#   (3) a divisao pelo numero real em vez do limite da turma, que e do short
#       original daquele pacote e nao se repete aqui.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Comparou os preços?", "sub": "falta uma parcela",
     "nar": "Você comparou os orçamentos de treinamento pelo preço impresso e "
            "escolheu o mais barato por pessoa?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "O preço é da turma", "sub": "a hora é por pessoa",
     "nar": "O preço do orçamento é da turma. Mas a hora fora do posto você paga "
            "por pessoa, não por turma.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Some antes", "sub": "depois divida",
     "nar": "Então some as horas de todos ao preço da turma, e só depois divida "
            "pelo seu número de pessoas.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A ordem muda", "sub": "outra vez",
     "nar": "Com essa parcela dentro, a cotação mais barata do papel pode virar a "
            "mais cara da sua lista.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Refaça a conta", "sub": "com as horas dentro",
     "nar": "Refaça a comparação com as horas dentro antes de assinar. O exemplo "
            "inteiro está no vídeo aqui embaixo.",
     "sem_cap": True},
]

THUMB = {"l1": "Some as horas", "l2": "primeiro"}

COPY = """# labtreinamento-s006

## TITULO
Comparar Orçamentos de Treinamento: Some as Horas Fora do Posto Antes de Dividir

## DESCRICAO
Quem recebe três orçamentos de treinamento compara três preços, e isso parece suficiente. O problema é que o preço impresso responde uma pergunta menor do que a que você precisa responder: ele diz quanto custa contratar a turma, não quanto custa treinar as suas pessoas.

A diferença está em como cada parcela escala. O preço do curso é da TURMA: ele é o mesmo se você manda o grupo cheio ou metade dele. Já as horas em que cada pessoa fica fora do posto escalam com PESSOAS: dobram se você manda o dobro de gente, e mudam se um fornecedor pede mais horas de aula do que outro. São dois comportamentos diferentes dentro da mesma decisão, e somá-los na ordem errada — ou não somar um deles — é o que faz a comparação apontar para o lado errado.

A conta que resolve tem dois passos e usa só números que você já tem. Primeiro, para cada cotação, some ao preço da turma o total de horas fora do posto de todas as pessoas que você vai mandar. Segundo, divida esse total pelo seu número real de pessoas — o mesmo número nas duas cotações, sempre. Só depois desse segundo passo as duas propostas ficam comparáveis entre si.

E o resultado costuma surpreender em uma direção específica: a cotação com o preço de tabela mais baixo é muitas vezes a que pede mais horas de aula, porque é assim que ela consegue cobrar menos pela turma. Quando as horas entram, a ordem inverte — e inverte justamente no caso em que você tem pouca gente para mandar, porque aí o preço da turma se dilui pouco e as horas pesam proporcionalmente mais.

Não há aqui nenhum preço, nenhum tamanho de turma e nenhuma carga horária: os números que decidem estão nos seus orçamentos e na sua escala. O exemplo completo com números redondos, os quatro campos que você precisa ler em cada proposta e o que esta conta NÃO decide — estão no vídeo.

## TITULO SHORT
Some as horas antes de comparar preço

## COMENTARIO FIXADO
A chave é que as duas parcelas escalam de formas diferentes: o preço é da TURMA (igual com grupo cheio ou metade) e a hora fora do posto é por PESSOA (dobra se você manda o dobro de gente). Por isso: some as horas de todos ao preço da turma e só então divida pelo seu número real — o mesmo número nas duas cotações. Quem fizer isso vai notar que a proposta mais barata no papel costuma ser a que pede mais horas de aula. Se você refizer a conta, comente só se a ordem das cotações mudou — sem valores.

## HASHTAGS
#Treinamento #GestaoDePessoas #LabTreinamento

## TAGS
treinamento, custo por pessoa, orcamento de treinamento, horas fora do posto, comparacao de cotacoes, gestao de pessoas, pequeno negocio, custo real, turma fechada, carga horaria, decisao de compra, brasil, calculo, rh, lab treinamento

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pt-BR
defaultAudioLanguage: pt-BR
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita preco, nao
cita tamanho de turma, nao cita carga horaria, nao cita salario e nao nomeia
norma nem orgao. Conferido a mao campo por campo, porque o portao `narracao`
conta quantidades por frase e nao pega digito cru (640).

O QUE O VIDEO AFIRMA: que o preco do orcamento e da TURMA, que as horas fora do
posto escalam com PESSOAS, e que somar essa parcela antes de dividir muda a ordem
das cotacoes. E aritmetica sobre os papeis do proprio espectador. Esta no longo
labtreinamento-012 (Sr6VhvD_aPE), capitulos "O que entra na comparacao" e "O que
a conta nao decide".

DESCARTADO, e vai escrito:
  (1) qualquer preco, tamanho de turma e carga horaria — sao os numeros DO
      ESPECTADOR;
  (2) se a hora fora do posto deve ser contada como custo contabil — depende do
      regime de cada empresa e esta no longo;
  (3) a divisao pelo numero real em vez do limite da turma, que e do short
      original daquele pacote.

## FONTES
O longo de onde este short foi extraido (labtreinamento-012, Sr6VhvD_aPE) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s006",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "Sr6VhvD_aPE",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s006.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 35-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
