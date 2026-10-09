"""labtreinamento-s008 — antecedencia se MEDE no seu historico, nao se arredonda.

ALAVANCA: **primeiro teste da mira nova** (experimento 38, aprendizado 669). Os
dezenove shorts de 08/10 sairam com 34,8 s reais de media contra teto de 45 s, e
a culpa era minha: a mira "35 a 37" era habito, nao limite. O portao sempre
permitiu 43,14 estimados. Esta peca mira `ALVO_SHORT = (41.5, 43.0)`.

POR QUE EM pt-BR E NAO EM pl: a `pt-BR-ThalitaMultilingualNeural` tem o residuo
mais NEGATIVO e mais consistente das tres (−3,5% a −6,8%, n=4), entao 43 est cai
em 40,1 a 41,5 reais — a maior folga contra os 45 s. Testar o teto primeiro na
`pl-PL-Marek`, cujo residuo chega a +4,4%, seria escolher a voz errada para a
primeira medicao.

O QUE DEU CERTO na rodada anterior: o `epomeno-epipedo-s011` saiu em 37,47 s
reais contra 37,8 estimados (−0,9%), dentro da faixa do grego, e subiu com as
QUINZE tags direto do pipeline — segunda publicacao seguida desde que o `[:8]`
saiu do `publicar.py`, o que confirma o conserto ponta a ponta.

O QUE NAO DEU, e vai dito: o estoque livre deste canal sao SEIS origens e as
seis sao conformidade corporativa, o perfil que o 651 mediu como ~30x pior (4 a
70 views contra 1.111 e 1.133), porque ali o numero e do empregador. Escolhi
`lau1nnOUm1U` porque e a UNICA das seis em que o mecanismo do 651 ainda vale: o
numero e do PROPRIO espectador — ele e o responsavel, e a lista e dele, com papel
na mao. Nao e desculpa; e a melhor jogada dentro de um estoque ruim. A saida
estrutural continua sendo pacote completo, que pede janela do dono.

O QUE VOU MUDAR: uma coisa so, a DURACAO ALVO. O CTA continua pedindo inscricao
(experimento 37, aberto no s011) para nao misturar duas mudancas numa peca — mas
isso significa que esta peca carrega DOIS experimentos abertos, e eu NAO vou
poder separa-los olhando so para ela. Declarado aqui para nao me enganar depois:
o 37 se mede por inscrito/mil views do CANAL ao longo de dias, o 38 por tempo de
exibicao; sao metricas diferentes, e e isso que torna a sobreposicao tolerave].

NUMERO DE PARTIDA: 46 views do short do pacote de origem. Media real das pecas
de 08/10 neste canal: 42 views. Duracao real media da frota ontem: 34,8 s.

DE ONDE SAI: longo `lau1nnOUm1U` (labtreinamento-011), capitulos "De quanto
tempo | depende de duas coisas", "Meca, nao estime | olhe a ultima vez" e "Some
uma folga | porque algo sempre atrasa". O short ORIGINAL do pacote nao usa
nenhum dos tres: ele faz as duas contas (realizacao + periodicidade, e vencimento
− hoje) e termina no erro da data de emissao. A antecedencia fica inteira livre.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}`, trilha `Inspired` (601).

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita prazo de
# norma, nao cita periodicidade de treinamento, nao cita quantos dias de
# antecedencia, nao cita custo e nao nomeia norma nem orgao. Conferido A MAO
# campo por campo, porque o portao `narracao` conta QUANTIDADES por frase e NAO
# pega digito cru.
#
# E ESTE E O PONTO DA PECA: a antecedencia certa NAO E um numero que eu possa
# dar. Dar um numero redondo aqui seria cometer exatamente o erro que o video
# ataca. O longo tambem nao da prazo — o capitulo final dele se chama "Por que
# nao dei prazos | e isto e importante".
#
# O QUE O VIDEO AFIRMA: que a antecedencia do aviso deve sair do tempo que a
# propria organizacao levou para realizar a ultima turma, mais uma folga, e nao
# de um numero redondo escolhido de cabeca. Esta no longo labtreinamento-011
# (`lau1nnOUm1U`), capitulos "De quanto tempo", "Meca, nao estime" e "Some uma
# folga".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qualquer prazo em dias — e o numero do historico DELE, nao meu, e darei
#       um numero seria o erro que a peca denuncia;
#   (2) periodicidade de qualquer treinamento especifico, que muda por norma e
#       NAO foi reconferida nesta rodada em duas fontes;
#   (3) o custo de descobrir tarde, que esta no longo e depende da operacao.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "A lista esta pronta", "sub": "e agora?",
     "nar": "Você montou a lista de vencimentos, ela está ordenada pelo que "
            "vence primeiro, e agora precisa decidir com quanta antecedência "
            "avisar.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Número redondo", "sub": "é palpite",
     "nar": "Quase todo mundo escolhe aqui um número redondo de dias. Número "
            "redondo parece regra, mas é palpite com cara de organização.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Olhe a última vez", "sub": "não o palpite",
     "nar": "Olhe a última turma que você realizou. Quantos dias "
            "passaram entre alguém pedir e ela finalmente acontecer?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Esse é o seu número", "sub": "mais uma folga",
     "nar": "Esse intervalo é o tempo que a sua operação leva. Some uma folga, "
            "porque alguma coisa sempre atrasa.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Se inscreva", "sub": "para as próximas",
     "nar": "Meça no seu histórico, não no meu palpite. Se inscreva para as "
            "próximas, e a lista inteira está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Meça o seu", "l2": "histórico"}

COPY = """# labtreinamento-s008

## TITULO
Antecedência do Aviso de Vencimento: Por Que Ela Se Mede no Seu Histórico e Não se Arredonda

## TITULO SHORT
Antecedência não se arredonda: se mede

## DESCRICAO
Depois que a lista de vencimentos existe e está ordenada, aparece a pergunta que ninguém respondeu ainda: com quanta antecedência avisar? E aqui quase todo mundo faz a mesma coisa — escolhe um número redondo de dias, porque número redondo parece organizado. Ele não é organizado. Ele é um palpite com cara de regra.

A antecedência certa não é uma convenção, é uma medida, e a medida já está na sua operação. Pense na última turma que você realizou: entre o momento em que alguém pediu e o momento em que ela aconteceu de verdade, quantos dias passaram? Aquele intervalo é a sua antecedência mínima, porque é o tempo que a sua organização realmente leva — com o seu fornecedor, a sua aprovação de compra, a sua escala de turno, a sua sala.

Sobre esse intervalo você soma uma folga. Não por pessimismo: porque alguma coisa sempre atrasa, e a folga é o que impede que um atraso normal transforme um vencimento previsto em um vencimento perdido. O resultado dessas duas parcelas é a antecedência que você vai usar, e ela é diferente da do vizinho exatamente por isso.

Repare no que esta conta NÃO tem: nenhum número vindo de fora. Nenhum prazo que eu pudesse te dar aqui serviria, e dar um seria cometer o erro que este vídeo ataca — trocar a medida por um arredondamento. Pela mesma razão o vídeo completo também não dá prazos, e isso é deliberado.

Vale um ajuste fino quando fizer sentido: um número por tipo de treinamento, porque nem todos levam o mesmo tempo para ser agendados. Quem mudou de função, quem voltou de afastamento, quem está de licença e quem é terceirizado tem tratamento próprio na lista — e isso, mais as cinco colunas, a ordenação por vencimento e os campos que você precisa procurar no certificado, está no vídeo.

## COMENTARIO FIXADO
A conta da antecedência, em duas parcelas, para quem quiser fazer agora: primeira, quantos dias levou entre pedir a última turma e ela acontecer DE VERDADE — isso é medida, está no seu histórico. Segunda, uma folga, porque algo sempre atrasa. A soma é a sua antecedência. Se você escolheu um número redondo de cabeça, você estimou e não mediu, e é assim que um atraso normal vira vencimento perdido. Um número por tipo de treinamento, se os prazos de agendamento forem diferentes. Quem fizer a conta, comente só se o resultado ficou maior ou menor do que o palpite que usava antes — sem prazos.

## HASHTAGS
#Treinamentos #SegurancaDoTrabalho #LabTreinamento

## TAGS
antecedencia de aviso, vencimento de treinamento, controle de treinamentos, planilha de vencimentos, gestao de treinamentos, seguranca do trabalho, prazo de agendamento, folga de prazo, lista de vencimentos, responsavel de treinamento, como medir, historico da operacao, labtreinamento, treinamento vencendo, planejamento de turma

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita prazo de
norma, nao cita periodicidade, nao cita quantos dias de antecedencia, nao cita
custo e nao nomeia norma nem orgao. Conferido a mao campo por campo.

E ESTE E O PONTO DA PECA: a antecedencia certa NAO E um numero que eu possa dar.
Dar um numero redondo seria cometer exatamente o erro que o video ataca. O longo
tambem nao da prazo — o capitulo final dele se chama "Por que nao dei prazos".

O QUE O VIDEO AFIRMA: que a antecedencia do aviso deve sair do tempo que a
propria organizacao levou para realizar a ultima turma, mais uma folga, e nao de
um numero redondo escolhido de cabeca. Esta no longo labtreinamento-011
(lau1nnOUm1U), capitulos "De quanto tempo", "Meca, nao estime" e "Some uma folga".

DESCARTADO, e vai escrito:
  (1) qualquer prazo em dias — e o numero do historico DELE, nao meu;
  (2) periodicidade de treinamento especifico, que muda por norma e NAO foi
      reconferida nesta rodada em duas fontes;
  (3) o custo de descobrir tarde, que esta no longo e depende da operacao.

## FONTES
O longo de onde este short foi extraido (labtreinamento-011, lau1nnOUm1U) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s008",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "lau1nnOUm1U",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/labtreinamento-s008.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | teto 43.14 | piso 30")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO — ajuste a narracao'}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
