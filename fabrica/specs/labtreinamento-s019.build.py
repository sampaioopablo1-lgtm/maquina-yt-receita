"""labtreinamento-s019 — peca 3 das DEZ do formato novo.

Executa `docs/decisoes-12-10.md`: labtreinamento (1), dinheiro do PROPRIO
espectador (2), 20 a 26 s REAIS (3). Leitura declarada antes (4): romper e UMA
peca acima de 5.000 views.

ORIGEM: longo `4OYBkCHFTV8` (`labtreinamento-006`), 62 capitulos. TERCEIRO
angulo, e ele foi **pre-registrado pelo anterior**: o AVISO do `s018`, escrito
antes de ver qualquer resultado, nomeou "Quando nao vale" e "Se voce ja esta
perto da idade" como a familia seguinte. Capitulos usados: esses dois mais
"A pergunta certa" e "Sem esses dois numeros".

FAMILIA NOVA, a decima terceira: **QUANDO O CONSERTO NAO COMPRA NADA — A PORTA
QUE VOCE JA TEM CHEGA ANTES**. A entrada errada e tratar o acerto como sempre
vantajoso, quando a comparacao que decide e de DATA DE CHEGADA, nao de preco:
se a porta que voce ja tem abre antes da que compraria, o dinheiro compra tempo
que voce nunca usaria. O longo diz isso em letra: *"a porta que voce ja tem pode
chegar antes da que voce compraria"* e *"quem te disser que sempre vale a pena
nao fez a conta"*.

E ELA E O LADO OPOSTO DA PECA ANTERIOR, de proposito. O `s018` disse "nao desista
porque o conserto e divisivel". Esta diz "e ha casos em que ele nao compra nada".
As duas juntas sao a decisao inteira, e publicar so a primeira seria vender uma
metade — o que o proprio longo chama de "a parte que quase nenhum video faz".

REGRA (f) CONFERIDA: o labtreinamento ja teve hoje SUBSTITUICAO QUE NAO
SUBSTITUI (s014), A GUARDA NAO E A ENTREGA (s015), COMPOSICAO (s016), PROPORCAO
COM O PRAZO (s017) e O CONSERTO E DIVISIVEL (s018). Esta e a SEXTA familia
distinta do dia no canal.

MIRA: 20 a 26 s REAIS. `estimativa_para_real(22,0)` = 26,8, e os chars por cena
sairam de `chars_por_cena`.

IDENTIDADE: faixa ATUAL do canal, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO DIGITO e ZERO NUMERAL, pela mesma razao do `s018`: os numeros deste longo
# sao aliquota e taxa de juros, os dois na lista literal da regra (g). E a idade
# de aposentadoria TAMBEM fica fora — ela e limite legal e muda por reforma, que
# e exatamente o tipo de numero que envelhece dentro de um short.
#
# O QUE A PECA CARREGA, e nao envelhece: a comparacao que decide e de DATA DE
# CHEGADA entre duas portas, nao de preco. Isso e desenho de decisao.
#
# O QUE SOBRA PARA A PROXIMA: "E tem o meio-termo" + "Esse caminho serve bem" +
# "E serve mal" — a familia O MEIO-TERMO TEM DONO, isto e, a terceira opcao
# serve bem a um perfil e mal a outro. Quarto angulo deste longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Às vezes", "sub": "não vale consertar", "nar": "Às vezes não vale a pena consertar.", "sem_cap": True},
    {"layout": "item", "kicker": "E quase", "nar": "E quase ninguém te diz isso.", "sem_cap": True},
    {"layout": "item", "kicker": "Você tem", "nar": "Você já tem uma porta de aposentadoria.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E compraria", "sub": "uma outra", "nar": "E o acerto compraria uma segunda.", "sem_cap": True},
    {"layout": "item", "kicker": "A pergunta", "nar": "Qual das duas chega primeiro?", "sem_cap": True},
    {"layout": "item", "kicker": "Se for", "nar": "Se a que você já tem chega antes,", "sem_cap": True},
    {"layout": "titulo", "kicker": "Você paga", "sub": "por tempo que não usa", "nar": "Você paga por tempo que não vai usar.", "sem_cap": True},
    {"layout": "item", "kicker": "E quem diz", "nar": "Quem diz que sempre vale não fez a conta.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se", "nar": "Compare as duas datas antes. Inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "Qual porta", "l2": "chega antes?"}

COPY = """# labtreinamento-s019

## TITULO
Quando Consertar A Contribuição Não Compra Nada — A Porta Que Você Já Tem Pode Chegar Antes

## TITULO SHORT
Qual porta chega antes?

## DESCRICAO
Quase todo conteúdo sobre acerto de contribuição assume uma coisa: que acertar é sempre bom. Existe um caso em que não é, ele é comum, e quase ninguém fala dele.

Você já tem uma porta de aposentadoria — a que a sua contribuição atual te dá. O acerto compraria **uma segunda porta**, por outro caminho. E a pergunta que decide não é quanto a segunda custa. É **qual das duas chega primeiro**.

Se a porta que você já tem abre antes da que você compraria, o dinheiro do acerto compra tempo que você nunca vai usar. Não é um mau negócio por ser caro — é um mau negócio por ser **inútil naquele caso específico**. E isso não aparece em nenhuma calculadora que só te mostra o valor do acerto.

Daí a frase que vale guardar: quem te disser que **sempre** vale a pena acertar não fez a conta. Porque a conta tem dois lados, e o lado que quase ninguém mostra é o da data.

O que fazer, então, antes de pagar qualquer coisa: descubra as duas datas. A data em que a porta que você já tem abre, e a data em que a porta comprada abriria. Compare as duas. Só depois olhe o preço — e aí o preço passa a significar algo, porque você sabe o que ele está comprando.

Este short não cita alíquota, taxa de juros nem idade de aposentadoria, de propósito: alíquota e taxa mudam conforme o período, e idade muda por reforma. Um número fixo aqui daria uma conta errada para quase todo mundo que assiste. As duas datas do **seu** caso saem no Meu INSS, que é gratuito.

No vídeo completo: as duas opções e o que a mais barata tira, como se faz o acerto e por que ele é divisível, os três passos para estimar o seu caso, o outro momento em que não vale, e o meio-termo que serve bem para um perfil e mal para outro.

## COMENTARIO FIXADO
Esse é o lado da decisão que quase nenhum conteúdo mostra, e não por má-fé: é que mostrar "quanto custa acertar" rende um número impressionante, e mostrar "qual porta chega antes" dá trabalho. Mas é a segunda que decide. Se a aposentadoria que você já tem direito abre antes da que o acerto compraria, você estaria comprando tempo que nunca ia usar — e isso não tem a ver com o acerto ser caro ou barato. De propósito não coloquei aqui alíquota, taxa nem idade: os três mudam, e número fixo num short vira conta errada. As duas datas do seu caso saem de graça no Meu INSS. Conta nos comentários: você já sabe qual das duas chega primeiro no seu caso?

## HASHTAGS
#Autonomo #Previdencia #LabTreinamento

## TAGS
quando nao vale acertar contribuicao, aposentadoria por idade, aposentadoria por tempo de contribuicao, acerto retroativo, meu inss, decisao previdenciaria, planejamento previdenciario, contribuinte individual, autonomo, financas para autonomo, comparar beneficios, data de aposentadoria, erro comum previdencia, labtreinamento, dinheiro proprio

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
ZERO NUMERO, ZERO DIGITO e ZERO NUMERAL na narracao. Os numeros deste longo sao
**aliquota** e **taxa de juros**, os dois na lista literal da regra (g) — e aqui
entra um TERCEIRO que eu tambem deixo fora: a **idade de aposentadoria**, que e
limite legal e muda por reforma. Um numero fixo daria conta errada para quase
todo mundo que assiste, que e a mesma razao pela qual o proprio longo recusa dar
a taxa.

O QUE A PECA CARREGA, e nao envelhece: a comparacao que decide e de DATA DE
CHEGADA entre duas portas, nao de preco. Esta nos capitulos "Quando nao vale",
"Se voce ja esta perto da idade", "A pergunta certa" e "Sem esses dois numeros"
do longo `4OYBkCHFTV8` (pacote `labtreinamento-006`).

TERCEIRO ANGULO, e PRE-REGISTRADO pelo anterior: o AVISO do `s018` nomeou estes
capitulos e esta familia antes de ver qualquer resultado.

E ELA E O LADO OPOSTO DO `s018`, DE PROPOSITO. O `s018` disse "nao desista, o
conserto e divisivel". Esta diz "e ha casos em que ele nao compra nada". As duas
juntas sao a decisao inteira; publicar so a primeira seria vender uma metade — o
que o proprio longo chama de "a parte que quase nenhum video faz".

REGRA (f) CONFERIDA: o labtreinamento ja teve hoje SUBSTITUICAO QUE NAO
SUBSTITUI (s014), A GUARDA NAO E A ENTREGA (s015), COMPOSICAO (s016), PROPORCAO
COM O PRAZO (s017) e O CONSERTO E DIVISIVEL (s018). Esta e a SEXTA familia
distinta do dia no canal.

O QUE SOBRA PARA A PROXIMA: "E tem o meio-termo" + "Esse caminho serve bem" +
"E serve mal" — a familia O MEIO-TERMO TEM DONO. Quarto angulo deste longo.

## FONTES
O longo de onde este short foi extraido (`labtreinamento-006`, `4OYBkCHFTV8`)
carrega a norma com a fonte. Este short NAO introduz numero nenhum sobre o
mundo, entao nao exige fonte institucional nova.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s019",
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
    from ensaio import (duracao_estimada_short, alvo_short,
                        duracao_real_prevista)
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/labtreinamento-s019.json")
    est = duracao_estimada_short(SHORT, SPEC["voz"])
    real = duracao_real_prevista(SHORT, SPEC["voz"], "piper")
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"PECA 3 DAS DEZ | {len(SHORT)} cenas | dinheiro proprio | 4OYBkCHFTV8")
    print(f"estimado: {est:.1f}s | REAL previsto: {real:.1f}s | mira REAL {lo}-{hi}")
    print(f"real na mira? {'SIM' if lo <= real <= hi else 'NAO'}")
    print(f"por plano: {real/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
