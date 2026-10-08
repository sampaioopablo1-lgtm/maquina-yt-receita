"""labtreinamento-s005 — conferir UM mes nao prova nada: erro de base se repete.

ALAVANCA: A (alcance por short). Quinto short solto do labtreinamento.

O QUE DEU CERTO, e e o achado desta rodada: MEDIR ANTES DE CONCLUIR salvou a
rodada. A consulta "peca do dia por hora de vida" leu, as 15:10,
`labtreinamento-s002 = 0 views as 6,9 h` — passado o piso de 6 h do 657, o que
seria a prova de que o canal nao recebeu distribuicao hoje. Coletando NA HORA
(req 628): s002 com SESSENTA e s003 com QUARENTA E NOVE. A consulta nao mede o
agora, mede a ultima coleta GRAVADA, que estava horas atrasada. Virou o
aprendizado 660, e ele e o decimo terceiro da familia "o instrumento fabricou o
achado" — este fabricaria exatamente o erro do 657 outra vez, agora com o piso
de 6 h me dando falsa confianca.

O QUE NAO DEU: nao ha par legivel nesta rodada. No kolejny o espalhamento entre
as pecas de hoje e de ~5x em idades parecidas (s003 73 as 11,9 h; s006 24 as
8,8 h; s004 18 as 10,9 h; s005 14 as 9,8 h), mas as quatro tem a MESMA forma —
cinco cenas de cartao de texto, mesma paleta, mesma estrutura de narracao. A
unica diferenca e a pauta, e o 2-B.3 manda recusar "assunto" como resposta.
Entao digo o que e: SEM DIFERENCA DE FORMA QUE EU POSSA MUDAR.

O QUE VOU MUDAR, e e uma coisa so: a regra do 660 — coletar ANTES de ler idade
contra views, sempre, sem excecao. E o residuo de duracao: o s004 saiu 6,5%
ABAIXO da estimativa, o maior desvio negativo ja medido em pt-BR, entao esta
spec mira ~36 s estimados em vez de ~34 para nao raspar o piso de 30.
NUMERO DE PARTIDA: 82 do short do pacote de origem; 60 e 49 dos dois soltos de
hoje no canal, as 6,9 h e 5,9 h.

DE ONDE SAI: capitulo "Faca a conta do ano" do longo labtreinamento-009
(`dsoEo103l1o`), que o short original daquele pacote nao toca — ele entrega os
quatro passos da conferencia de UM mes e para ali. Perfil 651: dinheiro da
PROPRIA pessoa, com papel que ela ja tem na mao (a folha e o extrato). O recorte
e ARITMETICO: conferir um mes so e amostra de tamanho um. Erro de BASE nao
acontece uma vez, ele se repete todo mes, logo a diferenca de um mes multiplica
pelos meses trabalhados. E a entrada errada e escolher um mes CALMO para
conferir: e no mes de hora extra que a base erra mais.

IDENTIDADE: faixa atual do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}` com trilha `Inspired` — decimo pacote seguido.

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar. Do
PL/26 lido as 06:22 ficou a FORMA: pergunta ou imperativo em segunda pessoa.
Cena 1 pergunta, cena 5 imperativo. E o s004, publicado as 14:28, usou a forma
"mesmo numero, contexto diferente"; esta usa "amostra de tamanho um", que e
outra entrada errada — nao repeti a forma no mesmo dia.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o
# percentual do deposito, nao cita data, nao cita prazo legal, nao cita valor e
# nao nomeia orgao, lei nem aplicativo. Conferido A MAO campo por campo, porque o
# portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru (640).
#
# O QUE O VIDEO AFIRMA: que um erro na BASE do deposito se repete mes a mes, logo
# a diferenca de um mes se multiplica pelos meses trabalhados, e que o mes com
# hora extra e o que melhor revela erro de base. Esta no longo
# labtreinamento-009 (`dsoEo103l1o`), capitulos "A base nao e o que cai na
# conta", "Quando a diferenca e normal" e "Faca a conta do ano", com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o percentual do deposito e a data do mes — estao no longo com fonte; o
#       short nao precisa deles para dizer que erro de base se repete;
#   (2) qualquer prazo para reclamar diferenca — e afirmacao juridica com numero
#       e NAO foi reconferida hoje em duas fontes; o short nao fala de prazo;
#   (3) o que fazer quando a diferenca e real, que depende do caso e esta no
#       longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Conferiu um mês?", "sub": "isso não prova nada",
     "nar": "Você conferiu o depósito de um mês, bateu, e ficou tranquilo? Esse é "
            "um teste de tamanho um.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Erro de base", "sub": "não erra uma vez só",
     "nar": "Se a base do cálculo está errada, ela está errada todos os meses, "
            "porque é a mesma regra aplicada sempre.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Multiplique", "sub": "pelos meses trabalhados",
     "nar": "Então pegue a diferença de um mês e multiplique pelos meses que você "
            "já trabalhou nessa empresa.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Escolha o mês certo", "sub": "o de hora extra",
     "nar": "E não confira um mês calmo. Confira o mês em que você fez hora "
            "extra: é ali que a base erra mais.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Confira dois meses", "sub": "um calmo, um cheio",
     "nar": "Confira então um mês calmo e também um mês cheio, e compare. A conta "
            "do ano inteiro está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Um mês", "l2": "não prova"}

COPY = """# labtreinamento-s005

## TITULO
Conferir Um Mês de Depósito Não Prova Nada: Erro de Base se Repete Todo Mês

## TITULO SHORT
Conferiu um mês? Isso é amostra de um

## DESCRICAO
Quem aprende a conferir o depósito do fundo costuma fazer a conta uma vez, ver que fecha, e encerrar o assunto. O problema é que uma conferência isolada responde uma pergunta muito menor do que a pessoa pensa: ela diz que aquele mês específico está certo. Não diz nada sobre os outros.

E a distinção importa porque os dois tipos de erro possíveis se comportam de maneiras opostas. Um erro de lançamento é pontual: acontece num mês, por descuido, e não diz nada sobre o mês seguinte. Um erro de base é estrutural: alguém decidiu, em algum momento, o que entra e o que não entra no cálculo, e essa decisão é aplicada todos os meses, igual, sem ninguém revisitar. Se ela está errada, ela está errada desde que passou a valer — e a diferença que você vê num mês é só uma fatia do total.

Daí a conta que o vídeo faz: pegue a diferença de um mês e multiplique pelos meses que você já trabalhou ali. Esse é o tamanho real do assunto, e normalmente é ele que decide se vale levar a conversa adiante ou não. Uma diferença que parece pequena no mês quase nunca parece pequena no ano.

Tem ainda a escolha de qual mês conferir, e aqui a intuição também atrapalha. A tendência é conferir um mês comum, "limpo", porque a conta fica mais fácil. Mas é justamente no mês atípico — aquele com hora extra, adicional, algum pagamento habitual fora do básico — que uma base mal definida aparece, porque é ali que a diferença entre o básico e o que realmente deveria compor o cálculo fica grande. Um mês calmo pode fechar perfeitamente com uma base errada e você não ver nada.

A recomendação prática é conferir dois meses: um calmo e um cheio. Se os dois fecham, a base provavelmente está certa. Se o calmo fecha e o cheio não, você achou um erro de base, e ele tem a idade do seu contrato.

Não há aqui nenhum percentual, nenhuma data e nenhum prazo: os números que decidem estão na sua folha e no seu extrato. A conta do ano, onde encontrar cada número, quando a diferença é normal e o que este vídeo não diz — estão no vídeo.

## COMENTARIO FIXADO
O ponto é a diferença entre erro de lançamento e erro de base. Lançamento é pontual; base é uma regra aplicada todo mês, então ela erra desde que passou a valer. Por isso conferir um mês só é amostra de tamanho um — e por isso o mês a conferir é o CHEIO, com hora extra e adicionais, não o calmo: um mês calmo fecha bonito mesmo com a base errada. Confira dois, um de cada tipo. Se o calmo fecha e o cheio não, multiplique a diferença pelos meses de casa. Quem fizer os dois, comente só se os dois fecharam ou não — sem valores.

## HASHTAGS
#FGTS #DireitosDoTrabalhador #LabTreinamento

## TAGS
fgts, deposito mensal, base de calculo, hora extra, adicional habitual, folha de pagamento, extrato, conferencia, erro de base, direitos do trabalhador, financas pessoais, brasil, calculo, carteira assinada, lab treinamento

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o percentual
do deposito, nao cita data, nao cita prazo legal, nao cita valor e nao nomeia
orgao, lei nem aplicativo. Conferido a mao campo por campo, porque o portao
`narracao` conta quantidades por frase e nao pega digito cru (640).

O QUE O VIDEO AFIRMA: que um erro na BASE do deposito se repete mes a mes, logo a
diferenca de um mes se multiplica pelos meses trabalhados, e que o mes com hora
extra e o que melhor revela erro de base. Esta no longo labtreinamento-009
(dsoEo103l1o), capitulos "A base nao e o que cai na conta", "Quando a diferenca e
normal" e "Faca a conta do ano", com as fontes.

DESCARTADO, e vai escrito:
  (1) o percentual do deposito e a data do mes — estao no longo com fonte;
  (2) qualquer prazo para reclamar diferenca — afirmacao juridica com numero, NAO
      reconferida hoje em duas fontes; o short nao fala de prazo;
  (3) o que fazer quando a diferenca e real, que depende do caso e esta no longo.

## FONTES
O longo de onde este short foi extraido (labtreinamento-009, dsoEo103l1o) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s005",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "dsoEo103l1o",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s005.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 35-38)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
