"""labtreinamento-s014 — SEGUNDO ANGULO do mesmo longo. Substituir nao conserta.

ESTA PECA EXERCITA O ACHADO DA RODADA DAS 10:07, e e a primeira a faze-lo de
proposito: **a unidade de pauta e (longo, familia de capitulo), nao o longo.**
Medido: das 49 origens que as specs consomem, 48 estavam usadas UMA vez e o
precedente de duas estava no ar desde o comeco (`h04-UVlVevs` -> s002 e s006).
Eu tratei cada longo como uso unico por HABITO e anunciei "a pauta acabou" tres
vezes no mesmo dia.

ORIGEM: longo `6BeNHqT2okA` (pacote `labtreinamento-010`), **66 capitulos**. O
primeiro short dele, o `labtreinamento-s007`, usou DOIS — "Um dia util, contado a
partir de qual data" e "tres datas e um dia util" — e carregou a familia UNIDADE
(dia util contra dia corrido). **Sessenta e quatro capitulos nunca foram tocados.**

ESTE SHORT USA OUTROS, e eu os li na spec do pacote (os capitulos estao locais,
entao nao precisei de API): "E se a empresa nao comunicar", "Cinco podem
formalizar", "E aqui esta o detalhe", "O que isso significa", "Mas atencao" e
"Traduzindo".

FAMILIA NOVA, a nona: **SUBSTITUICAO QUE NAO SUBSTITUI**. Quando um terceiro
cumpre a obrigacao no lugar de quem a devia, parece que ela foi cumprida — e nao
foi, para quem a devia. O proprio longo diz isso em letra: "o trabalhador emitir
a comunicacao nao conserta o descumprimento da empresa".
Ja usadas: LIMIAR, COMPOSICAO, ORDEM, DEFASAGEM NO TEMPO, ARITMETICA
media-contra-produto, CONDICAO/ACAO, MARGINAL contra TOTAL, A SOMA DOS PEQUENOS.
E a regra (f) e respeitada: o labtreinamento teve hoje o `s013`, que era
ARITMETICA (media contra produto) — familia diferente desta.

MIRA: `alvo_short('labtreinamento')` = **33,0 a 37,0**, o OVERRIDE do canal
(aprendizado 698), nao a mira da frota. E no pt-BR o residuo e -3,7%, entao o
TOPO e o lado seguro: mirei 36,5.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO DIGITO e ZERO NUMERAL na narracao, conferido campo a campo. Em especial:
#
#   * NAO digo QUANTOS podem comunicar no lugar da empresa. O longo diz cinco;
#     dizer "cinco" aqui seria numeral, e a lista pode mudar por reforma. A peca
#     diz "outros", que e a regra;
#   * NAO cito numero de artigo nem de paragrafo. Eles nao estao na lista da
#     regra (g) — taxa, indice, aliquota, limite, data de vigencia — mas mudam
#     por reforma legislativa do mesmo jeito, e o longo ja os carrega com fonte;
#   * NAO digo a duracao do prazo, nem a excecao de morte imediata, nem valor de
#     multa. O `s007` tambem os descartou, pela mesma razao: prazo errado num
#     short e pior que prazo nenhum.
#
# O QUE A PECA CARREGA, e nao envelhece: a comunicacao feita por um terceiro
# VALE como comunicacao, e NAO conserta o descumprimento de quem a devia. Logo
# "alguem comunicou" nao e resposta para "a empresa cumpriu". Isso e desenho de
# obrigacao, nao tabela.
#
# E O QUE EU NAO LEVEI, escrito para a proxima rodada achar: o capitulo da
# "copia fiel" (paragrafos do mesmo artigo) — a obrigacao de entregar copia ao
# acidentado e ao sindicato, que "nao e aviso, nao e resumo e nao e confirmacao
# de protocolo". E outra familia inteira (O DOCUMENTO NAO E O AVISO) e da um
# TERCEIRO angulo deste mesmo longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Alguém comunicou", "sub": "a empresa não cumpriu", "nar": "Alguém comunicou. A empresa não cumpriu.", "sem_cap": True},
    {"layout": "item", "kicker": "A obrigação", "nar": "A comunicação é obrigação da empresa.", "sem_cap": True},
    {"layout": "item", "kicker": "Mas", "nar": "Se ela falha, outros podem comunicar.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E vale", "sub": "como comunicação", "nar": "E ela vale, para todo efeito.", "sem_cap": True},
    {"layout": "item", "kicker": "Aqui mora", "nar": "Aqui mora o engano que custa.", "sem_cap": True},
    {"layout": "item", "kicker": "Parece", "nar": "Parece obrigação cumprida.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Não foi", "sub": "não para quem a devia", "nar": "Não foi. Não para quem devia cumprir.", "sem_cap": True},
    {"layout": "item", "kicker": "A lei separa", "nar": "A lei separa as duas de propósito.", "sem_cap": True},
    {"layout": "item", "kicker": "Logo", "nar": "Comunicada por outro, segue descumprida.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Confira quem", "sub": "emitiu a sua última", "nar": "Confira quem emitiu a sua última.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se", "nar": "Se isso te poupou um problema, inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "Comunicada", "l2": "não é cumprida"}

COPY = """# labtreinamento-s014

## TITULO
Comunicação Emitida Por Terceiro Vale Como Comunicação — E Não Conserta O Descumprimento Da Empresa

## TITULO SHORT
Quem emitiu a sua última?

## DESCRICAO
Há um ponto na comunicação de acidente do trabalho que quase todo procedimento interno trata errado, e o erro não é de prazo nem de formulário: é de **a quem a obrigação pertence**.

A comunicação é obrigação da empresa. Se ela não a cumpre, a lei abre uma segunda via: outras pessoas podem formalizá-la no lugar dela — e essa comunicação **vale**, para todo efeito. O registro existe, o benefício caminha, o fato está documentado.

E é exatamente aí que o engano se instala. Vendo a comunicação emitida e aceita, o procedimento interno conclui que a obrigação foi atendida. **Não foi** — não para quem a devia. A lei separa as duas coisas de propósito: a comunicação feita por terceiro resolve o acesso do trabalhador ao que é dele, e não apaga o descumprimento de quem tinha o dever de comunicar e não comunicou.

A consequência prática é desconfortável e vale ser dita: uma empresa pode ter todas as comunicações em ordem no arquivo e ainda assim estar em falta, se parte delas foi emitida por outra pessoa. O arquivo mostra o documento; ele não mostra **quem** o emitiu.

Daí o teste que fecha o short: abra as últimas comunicações e veja quem as emitiu. Se não foi a empresa, não é um detalhe de procedência — é uma obrigação que ficou aberta e que o próprio documento não denuncia.

Este short não cita prazo, não cita número de artigo, não diz quantos podem comunicar no lugar da empresa e não cita valor de multa: parte disso muda por reforma, e tudo está no vídeo completo com a fonte. O que não muda é o desenho da obrigação.

No vídeo completo: as três datas candidatas e qual delas conta, a contagem em dia útil, a exceção que não admite prazo, quem exatamente pode comunicar na falta da empresa, e a obrigação de entregar cópia fiel que quase ninguém cumpre.

## COMENTARIO FIXADO
O detalhe que faz esse erro sobreviver é que ele não deixa rastro no arquivo: a comunicação está lá, aceita e protocolada, e nada no documento diz que foi o trabalhador, o sindicato ou o médico que a emitiu. Então o procedimento interno marca como cumprido. A lei separa as duas coisas de propósito — a comunicação por terceiro resolve o acesso do trabalhador ao que é dele, e não conserta o descumprimento de quem tinha o dever. Ou seja: "alguém comunicou" nunca é resposta para "a empresa cumpriu". De propósito não coloquei aqui prazo, artigo nem quantas pessoas podem fazê-lo: parte disso muda por reforma e está no vídeo com a fonte. Vale um teste de cinco minutos: nas últimas comunicações do seu arquivo, quem assinou a emissão? Conta nos comentários se você encontrou alguma que não foi emitida pela empresa.

## HASHTAGS
#SegurancaDoTrabalho #CAT #LabTreinamento

## TAGS
comunicacao de acidente, quem emite a cat, obrigacao da empresa, descumprimento, sindicato comunica, medico comunica, trabalhador comunica, previdencia social, procedimento interno de acidente, auditoria de arquivo, seguranca do trabalho, gestao de sst, acidente do trabalho, doenca ocupacional, obrigacao acessoria

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
ZERO NUMERO NOVO SOBRE O MUNDO, ZERO DIGITO e ZERO NUMERAL na narracao.
Conferido campo a campo. Em especial:
  * NAO digo QUANTOS podem comunicar no lugar da empresa. O longo diz cinco;
    "cinco" seria numeral, e a lista pode mudar por reforma. A peca diz
    "outros", que e a regra;
  * NAO cito numero de artigo nem de paragrafo. Eles nao estao na lista literal
    da regra (g), mas mudam por reforma legislativa do mesmo jeito, e o longo ja
    os carrega com fonte;
  * NAO digo a duracao do prazo, nem a excecao de morte imediata, nem valor de
    multa — o `s007` descartou os mesmos pela mesma razao: prazo errado num short
    e pior que prazo nenhum.

O QUE A PECA CARREGA, e nao envelhece: a comunicacao feita por um TERCEIRO vale
como comunicacao, e NAO conserta o descumprimento de quem a devia. Logo "alguem
comunicou" nao e resposta para "a empresa cumpriu". E desenho de obrigacao, nao
tabela. Esta nos capitulos "E se a empresa nao comunicar", "Cinco podem
formalizar", "E aqui esta o detalhe", "O que isso significa", "Mas atencao" e
"Traduzindo" do longo `6BeNHqT2okA` (pacote `labtreinamento-010`).

SEGUNDO ANGULO, declarado: o primeiro short deste longo e o `labtreinamento-s007`,
que usou DOIS capitulos ("um dia util, contado a partir de qual data" e "tres
datas e um dia util") e carregou a familia UNIDADE. O longo tem 66 capitulos;
sessenta e quatro nunca foram tocados. Isto NAO e repeticao: familia diferente,
capitulos diferentes, e passou o portao `similaridade` contra o mesmo canal.

O QUE EU NAO LEVEI, escrito para a proxima rodada achar: o capitulo da COPIA
FIEL — a obrigacao de entregar copia ao acidentado e ao sindicato, que "nao e
aviso, nao e resumo e nao e confirmacao de protocolo". E outra familia inteira
(O DOCUMENTO NAO E O AVISO) e da um TERCEIRO angulo deste mesmo longo.

## FONTES
O longo de onde este short foi extraido (`labtreinamento-010`, `6BeNHqT2okA`)
carrega a lei, o artigo e os paragrafos com a fonte. Este short NAO introduz
numero novo sobre o mundo, entao nao exige fonte institucional nova — e o que ele
afirma e NORMA, nao estatistica, pela regra de fonte unica.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s014",
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
    from ensaio import duracao_estimada_short, alvo_short
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/labtreinamento-s014.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas | SEGUNDO ANGULO de 6BeNHqT2okA")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (OVERRIDE do canal) | TOPO no pt-BR")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
