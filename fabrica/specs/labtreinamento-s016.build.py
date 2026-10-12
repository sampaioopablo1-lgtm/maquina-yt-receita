"""labtreinamento-s016 — QUARTO angulo do mesmo longo, e a PRIMEIRA peca mirada
pela duracao REAL em vez da estimada.

DUAS COISAS NOVAS AQUI, e as duas vem de medicao desta mesma rodada.

(1) O ANGULO, pre-registrado pelo anterior. O AVISO do `labtreinamento-s015`
escreveu, antes de ver qualquer resultado, que "Duas vias diferentes",
"Confundir custa" e "Um teste simples" dariam o QUARTO angulo do `6BeNHqT2okA`,
com a familia COMPOSICAO: DUAS OBRIGACOES CONTADAS COMO UMA. E este. Com ele o
`6BeNHqT2okA` passa a ser o primeiro longo da frota com quatro shorts, e a
unidade de pauta (longo x familia de capitulo) deixa de ser teoria.
Familias ja usadas deste longo: UNIDADE (`s007`), SUBSTITUICAO QUE NAO SUBSTITUI
(`s014`), A GUARDA NAO E A ENTREGA (`s015`).

(2) A MIRA MUDOU DE OBJETO, e isto e o aprendizado 711/712. Medida a duracao
REAL das nove pecas de hoje, o Piper entrega 10,2% a 20,0% MENOS que o modelo
estima — e o portao `duracao` compara o ESTIMADO, entao ele aprovou em silencio
o `s014` com 29 s reais contra um piso de 30.
**Esta peca e a primeira a mirar pela inversa:** `estimativa_para_real(35,0,
voz)` = **42,6**, e nao a faixa de 33-37 do `ALVO_POR_CANAL`, que e faixa de
duracao REAL e foi calibrada em pecas de edge-tts. Mirei **42,0 estimados** para
sair em **~34,5 reais**, dentro da faixa medida do canal e abaixo do teto de
43,1 do portao. O numero de chars por cena veio de `chars_por_cena`, nao da
minha cabeca: 50.

**E POR QUE ESTA PECA SAI NESTE CANAL E NAO NOS OUTROS** (712): com o fator do
Piper, o teto de 43,1 na estimativa trava a duracao real em **38,2 s no grego** e
**36,7 s no polones**, os dois ABAIXO do piso de 41,5 da mira medida do epomeno e
do kolejny. Nesses dois canais a mira esta INALCANCAVEL enquanto o edge-tts
estiver em 403, e toda peca deles sai fora do braco do experimento 38 sem avisar.
O labtreinamento e o unico onde a mira ainda cabe.

MIRA: `alvo_short('labtreinamento')` = 33,0 a 37,0 **de duracao REAL** (698).
Confundidor que fica no relato: o fator do Piper no pt-BR tem **n=3**, e o
YouTube arredonda a duracao para cima. Se a peca sair fora de 33-37, o fator
e que precisa de remedicao — nao a mira.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO DIGITO e ZERO NUMERAL na narracao, conferido campo a campo:
#
#   * NAO digo QUAL e o prazo de nenhuma das duas obrigacoes. E o ponto da peca
#     que elas tem prazos DIFERENTES, e dizer os numeros os faria envelhecer;
#   * NAO cito artigo nem paragrafo;
#   * NAO nomeio a autoridade competente — e o proprio longo diz que o TEXTO
#     nao a nomeia, e inventar o nome seria pior que omitir.
#
# O QUE A PECA CARREGA, e nao envelhece: sao DUAS obrigacoes com destinos
# diferentes, e um fluxo unico cumpre o prazo do caso frequente e perde o do
# caso grave — que e o inverso do que a lei pede. Isso e desenho de obrigacao.
#
# E O QUE EU NAO LEVEI, escrito para a proxima rodada achar: "Quem caracteriza",
# "A hipotese", "De onde sai o nexo" e "Pode ser afastado" — o nexo entre o
# trabalho e a doenca e PRESUMIDO em certa hipotese e pode ser AFASTADO, o que e
# a familia PRESUNCAO QUE SE INVERTE. Seria o QUINTO angulo deste longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Um fluxo", "sub": "para duas obrigações", "nar": "Você tem um fluxo. A lei tem duas obrigações.", "sem_cap": True},
    {"layout": "item", "kicker": "A primeira", "nar": "Uma comunicação vai à Previdência Social.", "sem_cap": True},
    {"layout": "item", "kicker": "A segunda", "nar": "A outra vai, de imediato, à autoridade competente.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Destinos", "sub": "e prazos diferentes", "nar": "Destinos diferentes. E prazos diferentes.", "sem_cap": True},
    {"layout": "item", "kicker": "Mas o procedimento", "nar": "Mas o seu procedimento trata as duas igual.", "sem_cap": True},
    {"layout": "item", "kicker": "E aí", "nar": "E aí ele cumpre o prazo do caso comum.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E perde", "sub": "o do caso grave", "nar": "E perde o do caso mais grave.", "sem_cap": True},
    {"layout": "item", "kicker": "Que é", "nar": "Que é o inverso exato do que a lei pede.", "sem_cap": True},
    {"layout": "item", "kicker": "E o texto", "nar": "E o texto nem nomeia quem é essa autoridade.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Resolva antes", "sub": "não durante", "nar": "Então resolva isso antes do acidente, não durante.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se", "nar": "Se isso abriu um buraco no seu procedimento, inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "Duas obrigações", "l2": "um fluxo"}

COPY = """# labtreinamento-s016

## TITULO
São Duas Comunicações De Acidente, Não Uma — E O Fluxo Único Perde O Prazo Do Caso Mais Grave

## TITULO SHORT
Resolva antes, não durante

## DESCRICAO
Quase todo procedimento interno de resposta a acidente do trabalho tem um único fluxo. O texto da lei tem **duas obrigações**, com destinos diferentes e prazos diferentes — e é dessa diferença que nasce o erro.

Uma é a comunicação à Previdência Social. A outra é a comunicação **imediata** à autoridade competente. Não são duas vias do mesmo papel: são obrigações distintas, e o texto as separa de propósito.

E aqui está a parte desconfortável. Quem trata as duas com o mesmo fluxo tende a cumprir o prazo do caso **mais frequente** — porque é esse que o procedimento foi desenhado para atender — e a perder o do caso **mais grave**, que é exatamente o inverso do que a lei pede. O erro não aparece no dia a dia: ele aparece no pior dia.

Há um detalhe que agrava, e ele está no próprio texto: a lei diz "autoridade competente" **sem nomeá-la**. Quem define isso é a norma de cada situação. Ou seja, no momento do acidente grave, alguém vai precisar descobrir para quem comunicar — e esse é o pior momento possível para descobrir.

Daí o teste que fecha o short, e ele é de cinco minutos: abra o seu procedimento de resposta a acidentes e procure se existe um caminho próprio para o caso mais grave, com destinatário nomeado. Se não existe, o procedimento está incompleto — e está incompleto justamente onde custa mais.

Este short não diz qual é o prazo de nenhuma das duas obrigações, não cita artigo nem parágrafo, e não nomeia a autoridade competente: o prazo muda por reforma, e a autoridade o próprio texto não nomeia. Tudo isso está no vídeo completo, com a fonte.

No vídeo completo: as três datas candidatas e qual delas conta, a contagem em dia útil, a exceção que não admite prazo, quem pode comunicar na falta da empresa, e a obrigação de entregar cópia fiel que quase ninguém cumpre.

## COMENTARIO FIXADO
O que faz esse erro ser tão difícil de ver é que ele é consequência de uma coisa boa: o procedimento foi otimizado para o caso que acontece toda semana. Só que a lei separou as duas comunicações justamente porque o caso raro exige outro caminho — e um fluxo único sempre acaba servindo o frequente. O teste não é "temos procedimento?", é "existe um caminho próprio, com destinatário nomeado, para o caso mais grave?". De propósito não coloquei aqui prazo, artigo nem o nome da autoridade: o prazo muda por reforma e a autoridade o próprio texto não nomeia — está no vídeo com a fonte. Conta nos comentários: no seu procedimento, a palavra que descreve o caso mais grave aparece com um fluxo próprio, ou está no mesmo parágrafo de todo o resto?

## HASHTAGS
#SegurancaDoTrabalho #CAT #LabTreinamento

## TAGS
comunicacao de acidente, autoridade competente, comunicacao imediata, previdencia social, procedimento interno de acidente, caso grave, prazo diferente, duas obrigacoes, seguranca do trabalho, gestao de sst, acidente do trabalho, resposta a acidente, auditoria de procedimento, obrigacao acessoria, plano de emergencia

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
  * NAO digo QUAL e o prazo de nenhuma das duas obrigacoes. E justamente o ponto
    da peca que elas tem prazos DIFERENTES, e dizer os numeros os faria
    envelhecer dentro de um short que carrega a REGRA;
  * NAO cito artigo nem paragrafo — mudam por reforma e o longo os carrega com
    fonte;
  * NAO nomeio a autoridade competente, e isso nao e omissao: o PROPRIO texto
    nao a nomeia, e inventar o nome seria pior do que dizer que ele nao nomeia.

O QUE A PECA CARREGA, e nao envelhece: sao DUAS obrigacoes com destinos
diferentes, e um fluxo unico cumpre o prazo do caso frequente e perde o do caso
grave — o inverso do que a lei pede. Esta nos capitulos "Duas vias diferentes",
"Confundir custa", "Um teste simples" e "Quem e a autoridade competente" do
longo `6BeNHqT2okA` (pacote `labtreinamento-010`).

QUARTO ANGULO, declarado, e PRE-REGISTRADO pelo anterior: o AVISO do `s015`
escreveu estes tres capitulos e esta familia antes de ver qualquer resultado.
Familias ja usadas deste longo: UNIDADE (`s007`), SUBSTITUICAO QUE NAO SUBSTITUI
(`s014`), A GUARDA NAO E A ENTREGA (`s015`). Esta e COMPOSICAO: DUAS OBRIGACOES
CONTADAS COMO UMA. O longo tem 66 capitulos.

A MIRA DESTA PECA E DE DURACAO REAL, E ISSO E NOVO (aprendizados 711 e 712).
Medida a duracao REAL das nove pecas de 12/10, o Piper entrega 10,2% a 20,0%
MENOS que o modelo estima, e o portao `duracao` compara o ESTIMADO — foi assim
que o `s014` foi ao ar com 29 s reais contra um piso de 30. Esta peca mira pela
INVERSA: `estimativa_para_real(35,0, voz)` da 42,6, entao mirei ~42,0 estimados
para sair em ~34,5 REAIS, dentro da faixa medida do canal (33,0 a 37,0) e abaixo
do teto de 43,1 do portao.

E ELA SAI NESTE CANAL POR MEDICAO, nao por preferencia: com o fator do Piper, o
teto de 43,1 trava a duracao real em 38,2 s no grego e 36,7 s no polones, os
dois ABAIXO do piso de 41,5 da mira medida do epomeno e do kolejny. Nesses dois
a mira esta inalcancavel enquanto o edge-tts estiver em 403.

O QUE EU NAO LEVEI, escrito para a proxima rodada achar: "Quem caracteriza",
"A hipotese", "De onde sai o nexo" e "Pode ser afastado" — o nexo entre o
trabalho e a doenca e PRESUMIDO em certa hipotese e pode ser AFASTADO. Familia
PRESUNCAO QUE SE INVERTE, e seria o QUINTO angulo deste mesmo longo.

## FONTES
O longo de onde este short foi extraido (`labtreinamento-010`, `6BeNHqT2okA`)
carrega a lei, o artigo e os paragrafos com a fonte. Este short NAO introduz
numero novo sobre o mundo, entao nao exige fonte institucional nova — e o que
ele afirma e NORMA, nao estatistica.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s016",
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
    from ensaio import (duracao_estimada_short, alvo_short,
                        duracao_real_prevista, estimativa_para_real)
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/labtreinamento-s016.json")
    est = duracao_estimada_short(SHORT, SPEC["voz"])
    real = duracao_real_prevista(SHORT, SPEC["voz"], "piper")
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas | QUARTO ANGULO de 6BeNHqT2okA")
    print(f"estimado: {est:.1f}s (teto do portao 43,1) | "
          f"REAL previsto pelo Piper: {real:.1f}s")
    print(f"mira REAL do canal: {lo}-{hi} | "
          f"estimativa que ela pede: {estimativa_para_real(lo, SPEC['voz']):.1f}"
          f"-{estimativa_para_real(hi, SPEC['voz']):.1f}")
    print(f"real na mira? {'SIM' if lo <= real <= hi else 'NAO'}")
    print(f"por plano: {real/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
