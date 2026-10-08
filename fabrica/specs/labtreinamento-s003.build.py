"""labtreinamento-s003 — o que separa 1.133 de 4 neste canal, com numero.

ALAVANCA: A (alcance por short). Decimo quinto short solto, terceiro do labtreinamento.

O QUE DEU CERTO: a regra nova do 650 ja pagou. Comparando a ULTIMA leitura com a
MEDIANA das tres ultimas, a divergencia e sistematica nas pecas jovens:
  epomeno-s005   ultima 291  mediana 254
  epomeno-s004   ultima 195  mediana 162
  kolejny-s003   ultima  57  mediana  33
  kolejny-s004   ultima  16  mediana   0
Nas pecas maduras elas coincidem (1.155 e 1.155, 884 e 884). Ou seja a oscilacao
morde justo onde eu mais quero ler resultado.
E ISSO QUALIFICA O 650, em vez de derruba-lo: para peca em PLATO a mediana e o
numero certo; para peca AINDA SUBINDO a mediana e um PISO, nao o valor. Com peca
jovem diga FAIXA (mediana a ultima), nunca um numero so.

O QUE NAO DEU, e e uma correcao minha de uma hora atras: as 08:23 eu escrevi que
o pacote completo no labtreinamento "resolve a restricao estrutural" porque so
pacote cria origem nova. Esta ERRADO. Quem esta sem origem e o epomeno e o
kolejny, e os dois estao bloqueados por calendario ate 09/10. O labtreinamento
tem ONZE origens livres — pacote ali acrescenta origem onde ela ja sobra. O
pacote no labtreinamento vale por si, nao por desbloquear nada, e nao e urgente.

O ACHADO DA RODADA, e esse eu POSSO usar na proxima spec: dentro do
labtreinamento a diferenca entre os shorts e de uma ordem de grandeza e ela NAO e
aleatoria. Views do short de cada pacote:
  006 INSS do autonomo, 11% ou 20%     1.111
  007 por hora ou por projeto          1.133
  008 desconto para pagar a vista        214
  009 FGTS, confira o deposito            82
  012 custo por pessoa do treinamento     70
  013 vale-transporte, 6% de qual          40
  010 CAT em doenca ocupacional           39
  011 treinamento vencendo                 35
  003 ISO 9001                            28
  002 NR-1 planilha                       26
  004 NR-10                               21
  005 FAP 2027                            22
  001 NR-1 planilha                         4
Os dois de cima sao DINHEIRO DA PROPRIA PESSOA, com papel que ela ja tem na mao —
a guia, um orcamento. Os de baixo sao CONFORMIDADE CORPORATIVA, onde o numero e
do empregador e nao do espectador. Fator ~30. Isso refina a leitura que a rotina
ja tinha ("papel que o espectador ja tem na mao") com numero, e NAO e "assunto":
e de quem e o numero.

O QUE VOU MUDAR, e e uma coisa so: este short sai do OUTRO longo de mais de mil
(`4OYBkCHFTV8`, o INSS do autonomo), em vez de voltar ao 007 de novo.
NUMERO DE PARTIDA: 1.111 do short daquele pacote, e 196 do unico solto maduro
do canal.

DE ONDE SAI: capitulo "Quando nao vale consertar" do longo, que o short original
so cita como gancho final. O recorte e ARITMETICO e NAO repete percentual
nenhum: complementar vem com juros, e juros crescem com a IDADE do mes, logo
"complementar tudo" e a entrada errada — ordene do mes mais novo para o mais
velho, e confira antes quanto tempo ainda falta.

IDENTIDADE: a faixa do canal e `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}` com trilha `Inspired` — OITO pacotes seguidos (007 a 013, s001,
s002). O 006 usa paleta antiga `{#1F3A5F, #C1462E, #E9B44C}` e eu NAO a copiei,
mesmo sendo dele que vem a pauta: o 601 manda comparar com a faixa historica, nao
com o pacote de origem.

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar. Do
PL/26 lido as 06:22 ficou a FORMA: pergunta ou imperativo em segunda pessoa, onze
de quinze. Cena 1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. NAO cita percentual de contribuicao, NAO cita
# aliquota de complementacao, NAO cita taxa de juro, NAO cita valor, NAO cita
# tempo minimo de contribuicao e NAO nomeia orgao. Nao ha numero dito na
# narracao.
#
# O QUE O VIDEO AFIRMA: que a complementacao de meses passados vem com juros e
# que a conta cresce com a idade do mes, logo convem ordenar os meses do mais
# novo para o mais velho e conferir primeiro quanto tempo ainda falta. Isso esta
# no longo labtreinamento-006 (`4OYBkCHFTV8`), no capitulo "Quando nao vale
# consertar", com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) os percentuais da guia e da diferenca, e qualquer taxa de juro — estao no
#       longo com fonte; o short nao precisa deles para dizer que mes antigo
#       custa mais;
#   (2) quanto tempo de contribuicao e exigido, e em que regra — e afirmacao
#       juridica com numero e NAO foi reconferida hoje em duas fontes; o short
#       MANDA conferir, nao afirma;
#   (3) se vale ou nao complementar, que depende de idade e de historico e esta
#       no longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Vai complementar?", "sub": "não comece por tudo",
     "nar": "Decidiu complementar a guia para contar tempo de contribuição? Não "
            "comece querendo tudo.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Mês antigo", "sub": "custa mais juro",
     "nar": "Cada mês que você complementa vem com juro, e quanto mais antigo o "
            "mês, maior fica a conta.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ordene os meses", "sub": "do mais novo ao mais velho",
     "nar": "Ordene então os meses do mais novo para o mais velho, e some só até "
            "onde o dinheiro alcança.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Pode já bastar", "sub": "veja o que falta",
     "nar": "Antes disso, confira quanto tempo ainda falta. Talvez você não "
            "precise complementar todos.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Monte a ordem", "sub": "antes de pagar",
     "nar": "Monte essa ordem antes de pagar a primeira guia. A conta completa "
            "está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Não complemente", "l2": "tudo"}

COPY = """# labtreinamento-s003

## TITULO
Complementar a Guia do Autônomo: Comece pelos Meses Mais Novos, Não por Todos

## TITULO SHORT
Não complemente tudo. Ordene os meses

## DESCRICAO
Quem descobre que a guia que paga todo mês não conta para tempo de contribuição costuma ter a mesma reação: complementar o passado inteiro. É a decisão certa pelo motivo errado, e ela sai mais cara do que precisa.

A complementação de um mês passado não custa só a diferença: custa a diferença mais juro, e esse juro depende de quanto tempo aquele mês já ficou para trás. Dois meses com exatamente a mesma diferença custam valores diferentes se um é do ano passado e o outro é de muitos anos atrás. Então "complementar tudo" não é uma decisão única: é uma fila de decisões com preços diferentes, e tratá-la como bloco faz você pagar primeiro justamente o que é mais caro por mês recuperado.

A ordem honesta é a inversa da intuição: liste os meses do mais recente para o mais antigo, veja o custo de cada um, e vá somando até onde o dinheiro que você tem de verdade alcança. Assim cada real comprado compra o máximo de tempo possível. Se depois sobrar fôlego, você desce mais na lista — mas já com o barato garantido.

E há um passo que vem antes de todos e que quase ninguém dá: conferir quanto tempo ainda falta. Dependendo da sua idade e do que já está registrado, pode ser que você não precise de todos aqueles meses, ou que o caminho que faz sentido não seja o de tempo de contribuição. Complementar sem saber quanto falta é comprar sem saber o preço do que se quer.

Não há aqui nenhum percentual, nenhuma taxa de juro e nenhum valor: os números que decidem estão na sua guia e no seu extrato. A conta completa, onde encontrar cada número, quando NÃO vale consertar e o que fazer ainda nesta semana — estão no vídeo.

## COMENTARIO FIXADO
A ordem importa e é contraintuitiva. Complementar um mês passado custa a diferença MAIS juro, e o juro cresce com a idade do mês — então dois meses de diferença igual têm preços diferentes. Liste os meses do mais NOVO para o mais VELHO, veja o custo de cada um e vá somando até onde o seu dinheiro alcança: assim cada real compra o máximo de tempo. E antes de qualquer pagamento, confira quanto tempo ainda falta — dependendo da idade e do que já está registrado, talvez você não precise de todos, ou talvez o caminho não seja esse. Se você fizer a lista, comente só se a diferença entre o mês mais novo e o mais velho foi grande — sem valores.

## HASHTAGS
#Autonomo #INSS #LabTreinamento

## TAGS
autonomo, complementacao, guia de contribuicao, tempo de contribuicao, juro, meses passados, aposentadoria, financas pessoais, brasil, calculo, carne, extrato, lab treinamento, ordem de pagamento, mes mais novo

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita percentual de contribuicao, nao cita
aliquota de complementacao, nao cita taxa de juro, nao cita valor, nao cita tempo
minimo de contribuicao e nao nomeia orgao. Nao ha numero dito na narracao.

O QUE O VIDEO AFIRMA: que a complementacao de meses passados vem com juros e que
a conta cresce com a idade do mes, logo convem ordenar os meses do mais novo para
o mais velho e conferir primeiro quanto tempo ainda falta. Esta no longo
labtreinamento-006 (4OYBkCHFTV8), no capitulo "Quando nao vale consertar", com as
fontes.

DESCARTADO, e vai escrito:
  (1) os percentuais da guia e da diferenca, e qualquer taxa de juro — estao no
      longo com fonte; o short nao precisa deles para dizer que mes antigo custa
      mais;
  (2) quanto tempo de contribuicao e exigido, e em que regra — afirmacao juridica
      com numero, NAO reconferida hoje em duas fontes; o short MANDA conferir;
  (3) se vale ou nao complementar, que depende de idade e historico e esta no
      longo.

## FONTES
O longo de onde este short foi extraido (labtreinamento-006, 4OYBkCHFTV8) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s003",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "4OYBkCHFTV8",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s003.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
