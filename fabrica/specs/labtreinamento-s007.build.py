"""labtreinamento-s007 — dia util nao e dia: conte no calendario, nao na cabeca.

ALAVANCA: A (alcance por short). Setimo short solto do labtreinamento, fechando
os 7/dia pedidos nos TRES canais.

O QUE DEU CERTO, e derruba de vez uma leitura minha: o `epomeno-s009` — SETIMA
peca do dia no canal, publicada DEPOIS do s007 e do s008 — fez **216 views em
2,9 h**. Os dois anteriores seguem em ZERO as 9,9 h e 7,9 h. Isso elimina
qualquer versao de "peca tardia do dia nao recebe distribuicao": a diferenca e
DA PECA, nao da posicao. Aprendizado 663.

O QUE NAO DEU, e a hipotese que eu quase comprei: atribuir o zero as TAGS. O
kolejny-s009 tem as QUINZE tags repostas a mao e **1 view as 1,9 h**; o
kolejny-s008 tem as OITO de sempre e **88 as 3,9 h**. As tags nao explicam. O que
sobra como candidato e FORMA: o epomeno-s007 e o s008 sairam a duas horas de
distancia com a MESMA entrada errada ("compare o ano, nao o mes" / "falta uma
coluna"), que a propria rotina manda nao repetir no mesmo dia. Hipotese
registrada como `candidato`: repetir a forma no mesmo canal no mesmo dia suprime
AS DUAS pecas, nao so divide atencao.

O QUE VOU MUDAR, e e consequencia direta disso: escolhi a origem desta rodada
pela FORMA e nao pelo alcance. O `lau1nnOUm1U` (46) seria a melhor por numero,
mas a entrada errada dele — "somar/subtrair uma parcela que falta antes de
ordenar" — e da mesma familia do s006 que acabei de publicar neste canal.
Troquei por `6BeNHqT2okA` (41), cuja entrada errada e de OUTRA familia: "qual das
datas vale, e como se conta a partir dela".
NUMERO DE PARTIDA: 41 do short daquele pacote; 68 do melhor solto maduro do canal
hoje. Expectativa honesta: faixa de conformidade, 4 a 70, pelo 651.

DE ONDE SAI: longo `6BeNHqT2okA` (labtreinamento-010), o capitulo do dia util. O
short original daquele pacote resolve QUAL das tres datas vale e para ali; este
ataca o passo seguinte, que e onde a conta erra na pratica: contar o prazo em
dias corridos, ou comecar a contagem na propria data. Dia util e contagem de
CALENDARIO, nao de cabeca, e cair numa sexta ou em vespera muda a resposta.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}` com trilha `Inspired`.

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. NAO diz quantos dias
# e o prazo, NAO nomeia a lei, NAO nomeia orgao, NAO cita valor e NAO cita multa.
# Conferido A MAO campo por campo, porque o portao `narracao` conta QUANTIDADES
# por frase e NAO pega digito cru (640).
#
# O QUE O VIDEO AFIRMA: que o prazo e contado em dias UTEIS e nao corridos, e que
# a contagem nao comeca na propria data — logo cair numa sexta ou em vespera de
# feriado muda a data final. E NORMA, nao estatistica, e esta no longo
# labtreinamento-010 (`6BeNHqT2okA`), capitulos "Um dia util, contado a partir de
# qual data" e "Hoje: tres datas e um dia util", com as fontes. Declarado aqui
# conforme a regra de fonte unica que e norma.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a duracao do prazo em dias e a excecao de morte imediata — estao no longo
#       com fonte, e dizer prazo errado num short e pior que nao dizer;
#   (2) qual das tres datas vale, que e o short original daquele pacote e nao se
#       repete aqui;
#   (3) qualquer consequencia de perder o prazo, que e afirmacao juridica com
#       numero e NAO foi reconferida nesta rodada em duas fontes.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Já sabe a data?", "sub": "a contagem é o outro erro",
     "nar": "Você já descobriu qual data começa o prazo. Agora falta a parte em "
            "que quase todo mundo erra.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Dia útil", "sub": "não é dia",
     "nar": "O prazo é contado em dias úteis, não corridos. E a contagem não "
            "começa na própria data do fato.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Abra o calendário", "sub": "não conte de cabeça",
     "nar": "Então abra o calendário de verdade e marque, porque sábado, domingo "
            "e feriado não entram na conta.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Sexta ou véspera", "sub": "muda a resposta",
     "nar": "Se a data cair numa sexta ou numa véspera de feriado, o prazo não "
            "termina amanhã como parece.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Marque agora", "sub": "no calendário",
     "nar": "Marque essa data no calendário antes de fechar o caso. O prazo "
            "inteiro está no vídeo aqui embaixo.",
     "sem_cap": True},
]

THUMB = {"l1": "Dia útil", "l2": "não é dia"}

COPY = """# labtreinamento-s007

## TITULO
Prazo em Dias Úteis: Por Que Contar de Cabeça Erra a Data Final

## TITULO SHORT
Dia útil não é dia. Abra o calendário

## DESCRICAO
Quem já resolveu a parte difícil — descobrir qual data faz o prazo começar a correr — costuma tratar o resto como detalhe. É aí que a conta erra, e erra de um jeito que não aparece até ser tarde: o prazo é contado em dias úteis, e dia útil não é a mesma coisa que dia.

São duas armadilhas distintas na mesma contagem. A primeira é contar dias corridos: sábado, domingo e feriado não entram, então um prazo que parece curto pode atravessar um fim de semana inteiro e, no sentido inverso, um prazo que parece ter folga pode não ter. A segunda é começar a contagem na própria data do fato, em vez de começar no dia seguinte — e esse deslocamento de um dia é exatamente o que separa estar dentro do prazo de estar fora dele.

O procedimento que não erra não tem nada de sofisticado e é justamente por isso que funciona: abra o calendário, encontre a data que inicia a contagem, e marque a data final riscando os dias que não contam. Não faça isso de cabeça. Fazer de cabeça é como a maioria dos atrasos acontece, porque a intuição conta dias corridos sem avisar que está contando errado.

Há um caso que merece atenção especial, e é o mais comum de todos: quando a data cai numa sexta-feira ou numa véspera de feriado. Nessas situações a resposta "é amanhã" está quase sempre errada, e o erro vai na direção perigosa — você acha que tem menos tempo do que tem, corre, ou acha que tem mais, e perde. O calendário resolve em dez segundos o que a cabeça erra com confiança.

Não há aqui nenhum número de dias, nenhuma lei citada e nenhuma consequência afirmada: esses estão no vídeo, com as fontes. O que este short entrega é a mecânica da contagem, que é a parte que ninguém revisa.

## COMENTARIO FIXADO
As duas armadilhas são independentes, e dá para errar nas duas ao mesmo tempo: (1) contar dias corridos em vez de úteis — sábado, domingo e feriado não entram; (2) começar a contagem na própria data do fato em vez do dia seguinte. O caso que mais derruba é a data cair numa sexta ou véspera de feriado, porque aí a resposta intuitiva "é amanhã" está errada. Abra o calendário e marque riscando os dias que não contam, em vez de contar de cabeça. Se você for conferir um caso seu, comente só se a data final mudou — sem detalhes do caso.

## HASHTAGS
#SegurancaDoTrabalho #Prazos #LabTreinamento

## TAGS
prazo em dias uteis, contagem de prazo, dia util, feriado, calendario, comunicacao de acidente, seguranca do trabalho, gestao de prazos, erro de contagem, data inicial, dia seguinte, brasil, procedimento, rh, lab treinamento

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao diz quantos dias e
o prazo, nao nomeia a lei, nao nomeia orgao, nao cita valor e nao cita multa.
Conferido a mao campo por campo, porque o portao `narracao` conta quantidades por
frase e nao pega digito cru (640).

O QUE O VIDEO AFIRMA: que o prazo e contado em dias UTEIS e nao corridos, e que a
contagem nao comeca na propria data — logo cair numa sexta ou em vespera de
feriado muda a data final. E NORMA, nao estatistica, e esta no longo
labtreinamento-010 (6BeNHqT2okA), capitulos "Um dia util, contado a partir de qual
data" e "Hoje: tres datas e um dia util", com as fontes. Declarado conforme a
regra de fonte unica que e norma.

DESCARTADO, e vai escrito:
  (1) a duracao do prazo em dias e a excecao de morte imediata — estao no longo
      com fonte, e dizer prazo errado num short e pior que nao dizer;
  (2) qual das tres datas vale, que e o short original daquele pacote;
  (3) qualquer consequencia de perder o prazo — afirmacao juridica com numero,
      NAO reconferida nesta rodada em duas fontes.

## FONTES
O longo de onde este short foi extraido (labtreinamento-010, 6BeNHqT2okA) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s007",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "6BeNHqT2okA",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s007.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 35-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
