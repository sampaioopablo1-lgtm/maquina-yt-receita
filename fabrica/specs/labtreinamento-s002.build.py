"""labtreinamento-s002 — o canal que estava em ZERO hoje, e a correcao do contador.

ALAVANCA: A (alcance por short). Decimo quarto short solto, segundo do labtreinamento.

O QUE DEU CERTO: nada de novo na entrega — a ponte, catorze vezes.
O QUE NAO DEU, e e grande: o `viewCount` publico NAO E MONOTONO. Ele OSCILA.
Serie horaria do `u-vIsXaKjcM`:
  133 -> 396 -> 455 -> 455 -> 481 -> 491 -> 498 -> 491 -> 525 -> 491
Ele volta a 491 QUATRO vezes. Os 525 que eu reportei as 07:12 como o achado da
janela de 21,6 h eram um PICO TRANSITORIO; o plato e 491. Varrendo trinta horas
de `metricas`, DEZESSEIS pecas da frota cairam, de -1 a -34: rM5TYxhMHFQ 10 -> 0,
NNgAQLlpEzg 5 -> 1, m5Kiqy-k2nM 187 -> 169, QiaGg03WSR0 70 -> 52, SguKk8lMR0s
356 -> 330. A amplitude cresce com o tamanho do contador. Aprendizado 650.

O QUE ISSO DERRUBA: a parte do 605 que dizia "UMA view abaixo e retratacao de
spam, dezenas NAO sao" — o limiar esta errado. E derruba o meu proprio relato de
uma hora atras: o delta honesto do u-vIsXaKjcM e +358 para 491, nao +392 para 525.

O QUE VOU MUDAR, e e a SEXTA correcao de instrumento: `views_agora` deixa de ser
a ultima leitura. Passa a ser a MEDIANA das tres ultimas coletas da peca, e delta
menor que a faixa de oscilacao daquela peca e RUIDO, nao delta. Nunca mais anuncio
recorde ou retomada com uma leitura so.
E respondendo a pergunta do 2-B.8 contra mim mesmo: sim, o instrumento podia
produzir o achado. Ler o maximo de uma serie que oscila fabrica "recorde", igual
janela curta fabrica "morte" e amostra de doze quadros fabrica "aviso isolado".
Nono defeito com essa assinatura.

POR QUE O LABTREINAMENTO: ele estava em ZERO videos hoje contra quatro do epomeno
e quatro do kolejny, e e o UNICO dos tres com estoque de origem — doze longos
livres. O epomeno e o kolejny estao em zero livres e o pacote completo do epomeno
so libera em 09/10 07:12. Nao e o melhor canal em alcance (196 contra 1.046 e
1.155 na mesma faixa de idade) e eu digo isso: e o canal que podia produzir.
NUMERO DE PARTIDA: 201 do `m5Kiqy-k2nM`, o unico solto que o canal ja teve.

DE ONDE SAI: do `ntrMxq89I4o` (labtreinamento-007), o longo que gerou o MELHOR
short do canal (`DDaZqbcZCTM`, 1.133). O short original ensina a divisao — liquido
do projeto sobre as horas do projeto. Este ataca o capitulo "O que a conta nao
pega": as horas das propostas que voce montou e NAO ganhou tambem foram suas, e
quem divide por um projeto so nao as conta. Entrada errada e a CONTAGEM DE HORAS,
e a saida e dividir pelo MES.
E DE PROPOSITO o titulo deste e CURTO e PROPRIO: o 633 mediu que os dois maiores
shorts deste canal tem titulo COPIADO do longo, e esta rebaixado de medido para
observado — nao vou copiar titulo com base nele.

IDENTIDADE: faixa do canal — paleta `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}`, trilha `Inspired`, voz `pt-BR-ThalitaMultilingualNeural`.

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar. O
PL/26 lido as 06:22 deu FORMA: onze de quinze titulam em pergunta ou imperativo
em segunda pessoa. A cena 1 daqui e pergunta e a 5 e imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita preco, nao cita hora, nao cita
# imposto, nao cita aliquota, nao cita taxa e nao nomeia orgao. Nao ha numero
# dito na narracao.
#
# O QUE O VIDEO AFIRMA: que as horas gastas em propostas nao ganhas sao horas
# trabalhadas, e que por isso dividir o liquido de UM projeto pelas horas DAQUELE
# projeto superestima o valor da hora. Isso e aritmetica e esta no longo
# `ntrMxq89I4o` (labtreinamento-007), no capitulo sobre o que a conta nao pega.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qualquer valor, preco por hora ou percentual de imposto;
#   (2) quanto a hora costuma cair ao dividir pelo mes — varia por pessoa e e
#       exatamente o que o espectador vai MEDIR;
#   (3) o que a conta NAO decide — se vale cobrar por hora ou por projeto. Esta
#       no longo, e o short manda para la.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Somou as horas?", "sub": "faltou uma parte",
     "nar": "Você somou as horas daquele projeto? Então faltou no denominador "
            "a parte que não aparece.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A proposta perdida", "sub": "também foi sua hora",
     "nar": "As propostas que você montou e não ganhou também gastaram as suas "
            "horas, e ninguém pagou por nenhuma delas.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Divida pelo mês", "sub": "não pelo projeto",
     "nar": "Divida então pelo mês inteiro, e não por um projeto só. Entra "
            "tudo que o mês consumiu.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A hora cai", "sub": "e é essa a real",
     "nar": "O valor da sua hora cai. E é esse número menor que decide o seu "
            "próximo preço.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Refaça hoje", "sub": "pelo mês todo",
     "nar": "Refaça a conta pelo mês todo, hoje mesmo. A conta completa está "
            "no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Refaça pelo", "l2": "mês todo"}

COPY = """# labtreinamento-s002

## TITULO
As Horas da Proposta Que Você Não Ganhou Também Contam: Refaça a Conta pelo Mês

## TITULO SHORT
Refaça pelo mês, não pelo projeto

## DESCRICAO
A conta do valor real da sua hora é simples e cabe em uma divisão: o líquido que sobrou de um trabalho dividido pelas horas que aquele trabalho consumiu. Ela funciona, e é por onde se começa. Mas ela tem um buraco no denominador, e o buraco não é pequeno.

As horas que você soma são as horas do projeto que você ENTREGOU. Ficam de fora as horas que você gastou montando propostas que não viraram projeto: a conversa inicial, o escopo que você escreveu, o orçamento que você detalhou, o retorno que nunca veio. Essas horas foram trabalhadas do mesmo jeito, saíram do mesmo mês e não foram pagas por ninguém. Se o denominador só tem as horas do trabalho que deu certo, o valor da sua hora sai mais alto do que ele é — e é com esse número inflado que você vai precificar o próximo.

A versão honesta troca o recorte: em vez de um projeto, o MÊS. Pegue o líquido que entrou no mês e divida por todas as horas que o mês consumiu, incluindo as propostas perdidas, as reuniões que não fecharam nada e o tempo de administração. O número cai. Esse número menor é o que descreve a sua operação, e é ele que decide se o próximo preço paga a sua semana ou só a sua entrega.

Vale manter as duas contas, porque elas respondem perguntas diferentes: a do projeto diz quanto aquele trabalho rendeu; a do mês diz quanto você ganha por hora trabalhada. A distância entre as duas é o custo de conseguir trabalho, e ela aparece em quase todo mundo que vende serviço.

Não há aqui nenhum preço, nenhuma hora e nenhum percentual: os números que decidem estão no seu extrato e na sua agenda. A conta completa, onde achar as horas que você não anotou, quando ela engana e como passar de um mês para o ano — estão no vídeo.

## COMENTARIO FIXADO
A conta do projeto é líquido do projeto sobre horas do projeto. O buraco está no denominador: ela não conta as horas das propostas que você montou e não ganhou, e essas saíram do mesmo mês. Refaça pelo MÊS — líquido que entrou no mês sobre todas as horas do mês, propostas perdidas e administração incluídas. O número cai, e é o menor que descreve a sua operação e precifica o próximo trabalho. Guarde as duas: a do projeto diz quanto aquele trabalho rendeu, a do mês diz quanto você ganha por hora trabalhada, e a distância entre elas é o custo de conseguir trabalho. Se refizer, comente só se a hora caiu pouco ou muito — sem valores e sem cliente.

## HASHTAGS
#Freelancer #PrecoPorHora #LabTreinamento

## TAGS
valor da hora, preco por hora, por projeto, freelancer, prestador de servico, proposta, orcamento, horas trabalhadas, precificacao, financas pessoais, brasil, calculo, autonomo, lab treinamento, conta do mes

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita preco, nao cita hora, nao cita imposto,
nao cita aliquota, nao cita taxa e nao nomeia orgao. Nao ha numero dito na
narracao.

O QUE O VIDEO AFIRMA: que as horas gastas em propostas nao ganhas sao horas
trabalhadas, e que por isso dividir o liquido de UM projeto pelas horas DAQUELE
projeto superestima o valor da hora. E aritmetica e esta no longo
labtreinamento-007 (ntrMxq89I4o), no capitulo sobre o que a conta nao pega.

DESCARTADO, e vai escrito:
  (1) qualquer valor, preco por hora ou percentual de imposto;
  (2) quanto a hora costuma cair ao dividir pelo mes — varia por pessoa e e
      exatamente o que o espectador vai MEDIR;
  (3) o que a conta NAO decide — se vale cobrar por hora ou por projeto. Esta no
      longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (labtreinamento-007, ntrMxq89I4o) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s002",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "ntrMxq89I4o",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s002.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
