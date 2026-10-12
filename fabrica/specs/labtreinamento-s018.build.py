"""labtreinamento-s018 — peca 2 das DEZ do formato novo.

Executa as decisoes de `docs/decisoes-12-10.md`: canal labtreinamento (decisao
1), dinheiro do PROPRIO espectador (decisao 2), 20 a 26 s REAIS (decisao 3). A
leitura declarada antes e da decisao 4: romper e UMA peca acima de 5.000 views.

ORIGEM: longo `4OYBkCHFTV8` (pacote `labtreinamento-006`), **62 capitulos**,
"INSS do Autonomo: a escolha na sua guia". O short ORIGINAL dele usou a escolha
da guia e o conserto da diferenca; **os capitulos desta peca ele nao usou**:
"Voce pode consertar em partes", "Isso muda a conta", "Se o conserto custa
demais" e "A pergunta certa".

FAMILIA NOVA, a decima segunda: **O CONSERTO E DIVISIVEL — E A PERGUNTA E QUANTO
COMPRA, NAO QUANTO CUSTA**. A entrada errada e precificar o acerto INTEIRO como
um numero so, concluir "impossivel", e parar. O conserto e divisivel mes a mes, e
a comparacao certa e uma RAZAO: o que cada mes custa contra o que cada mes
compra. O proprio longo diz isso em letra: *"a pergunta certa nao e quanto custa.
E quantos meses eu antecipo, e quanto eu recebo a mais por mes depois disso."*

REGRA (f) CONFERIDA: o labtreinamento ja teve hoje SUBSTITUICAO QUE NAO
SUBSTITUI (s014), A GUARDA NAO E A ENTREGA (s015), COMPOSICAO (s016) e PROPORCAO
COM O PRAZO (s017). Esta e a quinta familia distinta do dia no canal.

E AQUI OS NUMEROS SAEM DE NOVO — a politica e POR PECA, nao um interruptor
global. O `s017` levou numero porque os dele eram de um exemplo aritmetico que
nao envelhece. Os deste longo sao **aliquota** e **taxa de juros**, que a regra
(g) manda deixar fora — e o proprio longo recusa dar a taxa, com a mesma razao:
*"ela muda conforme o periodo, e um numero fixo daria uma conta errada para
quase todo mundo que assiste."* Entao esta peca carrega a RAZAO sem nenhum
numero, e manda o espectador buscar os dele onde eles estao certos.

MIRA: 20 a 26 s REAIS. `estimativa_para_real(23,0)` = 28,0, e os chars por cena
sairam de `chars_por_cena`, nao da minha cabeca.

IDENTIDADE: faixa ATUAL do canal, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO DIGITO e ZERO NUMERAL, e aqui isso NAO e excesso de zelo: os numeros deste
# longo sao aliquota de contribuicao e taxa de juros de acerto retroativo, os
# dois na lista literal da regra (g). O proprio longo recusa dar a taxa.
#
# O QUE A PECA CARREGA, e nao envelhece: o acerto e DIVISIVEL mes a mes, e a
# decisao e uma RAZAO entre o que cada mes custa e o que cada mes compra — nao um
# numero absoluto. Isso e desenho de decisao, nao tabela.
#
# E ELA MANDA O ESPECTADOR AO LUGAR CERTO em vez de inventar numero: o calculo
# com juros, mes a mes e para o caso dele, aparece no proprio sistema do INSS.
#
# O QUE SOBRA PARA A PROXIMA: "Quando nao vale" + "Se voce ja esta perto da
# idade" — a familia QUANDO O CONSERTO NAO COMPRA NADA, que e o lado oposto
# desta e tambem nao tem numero. Seria o terceiro angulo deste longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Não é tudo", "sub": "ou nada", "nar": "Você acha que é tudo ou nada.", "sem_cap": True},
    {"layout": "item", "kicker": "O acerto", "nar": "O acerto da contribuição é divisível.", "sem_cap": True},
    {"layout": "item", "kicker": "Mês a mês", "nar": "Complemente só os meses que importam.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E aí muda", "sub": "de impossível para escolhível", "nar": "Isso muda de impossível para escolhível.", "sem_cap": True},
    {"layout": "item", "kicker": "Porque", "nar": "Você compra exatamente o tempo que precisa.", "sem_cap": True},
    {"layout": "item", "kicker": "E a pergunta", "nar": "Então a pergunta não é quanto custa.", "sem_cap": True},
    {"layout": "titulo", "kicker": "É quanto", "sub": "esse dinheiro compra", "nar": "É quanto ele compra de benefício.", "sem_cap": True},
    {"layout": "item", "kicker": "O cálculo", "nar": "O cálculo do seu caso está no Meu INSS.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se", "nar": "Abra a sua guia e confira. Inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "Divisível", "l2": "mês a mês"}

COPY = """# labtreinamento-s018

## TITULO
O Acerto Da Contribuição É Divisível — A Pergunta Não É Quanto Custa, É Quanto Ele Compra

## TITULO SHORT
Não é tudo ou nada

## DESCRICAO
Quem descobre que escolheu a contribuição mais barata costuma fazer uma coisa só: pede o valor para acertar tudo, vê um número grande, e desiste. A decisão morre ali — e ela morreu por um erro de forma, não de dinheiro.

Porque **o acerto é divisível**. Não precisa ser tudo de uma vez. Dá para complementar **só os meses que fazem diferença** para o seu caso e deixar os outros como estão. E isso costuma mudar a conversa de impossível para escolhível, porque você passa a comprar exatamente o tempo de que precisa — não o passado inteiro.

E é aí que a pergunta muda. Enquanto você pergunta **"quanto custa?"**, a resposta é sempre um número grande e sempre desanimador. A pergunta que decide é outra: **quantos meses eu antecipo, e quanto eu recebo a mais por mês depois disso?** Essa é uma razão, não um valor — e razão você compara.

Tem um detalhe que trabalha contra quem espera: cada mês que passa encarece o acerto dos meses que já passaram. Não é urgência inventada para te apressar; é como o cálculo funciona.

Este short não diz alíquota nem taxa de juros, de propósito, e o vídeo completo também não: a taxa muda conforme o período, e um número fixo aqui daria uma conta errada para quase todo mundo que assiste. O cálculo certo, mês a mês e para o seu caso, aparece no **Meu INSS** — e ele é gratuito.

O que vale fazer hoje, em dois minutos: abra a sua guia e veja o código. Ele diz qual das opções você está pagando. Essa é a informação que decide, e ela já está na sua mão.

No vídeo completo: as duas opções e o que a mais barata tira, como se faz o acerto, os três passos para estimar o seu caso, e os dois momentos em que acertar **não** vale a pena.

## COMENTARIO FIXADO
O que faz tanta gente desistir dessa decisão é a forma da pergunta, não o valor. "Quanto custa acertar tudo?" devolve um número grande e encerra o assunto. Mas o acerto é divisível: você pode comprar só os meses que mudam o seu caso. Aí a conta vira uma razão — o que cada mês custa contra o que cada mês compra de benefício depois — e razão é coisa que se compara. De propósito não coloquei aqui alíquota nem taxa de juros: a taxa muda conforme o período, e número fixo daria conta errada para quase todo mundo. O cálculo do seu caso é gratuito no Meu INSS. Conta nos comentários: você já sabe qual código está na sua guia?

## HASHTAGS
#Autonomo #Previdencia #LabTreinamento

## TAGS
contribuicao do autonomo, acerto retroativo, complementacao de contribuicao, meu inss, aposentadoria do autonomo, guia de contribuicao, tempo de contribuicao, decisao previdenciaria, planejamento previdenciario, mei e autonomo, financas para autonomo, beneficio por idade, codigo da guia, contribuinte individual, labtreinamento

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
ZERO NUMERO, ZERO DIGITO e ZERO NUMERAL na narracao — e aqui isso NAO e excesso
de zelo, ao contrario do que eu vinha fazendo nas pecas de conformidade. Os
numeros deste longo sao **aliquota de contribuicao** e **taxa de juros de acerto
retroativo**, os dois na lista LITERAL da regra (g). O proprio longo recusa dar a
taxa, e com a razao certa: *"ela muda conforme o periodo, e um numero fixo daria
uma conta errada para quase todo mundo que assiste."*

A POLITICA DE NUMERO E POR PECA, NAO UM INTERRUPTOR GLOBAL. O `s017` levou
numero porque os dele eram de um exemplo aritmetico que nao envelhece (dez por
cento, sessenta dias). Os deste nao: eles sao norma e taxa.

O QUE A PECA CARREGA, e nao envelhece: o acerto e DIVISIVEL mes a mes, e a
decisao e uma RAZAO entre o que cada mes custa e o que cada mes compra — nao um
numero absoluto. Esta nos capitulos "Voce pode consertar em partes", "Isso muda a
conta", "Se o conserto custa demais" e "A pergunta certa" do longo `4OYBkCHFTV8`
(pacote `labtreinamento-006`).

E ELA MANDA O ESPECTADOR AO LUGAR CERTO em vez de inventar numero: o calculo com
juros, mes a mes e para o caso dele, sai no proprio sistema do INSS, de graca.

SEGUNDO ANGULO, declarado: o short original deste longo usou a escolha da guia e
o conserto da diferenca. Os quatro capitulos acima ele nao usou. O longo tem 62.

REGRA (f) CONFERIDA: o labtreinamento ja teve hoje SUBSTITUICAO QUE NAO SUBSTITUI
(s014), A GUARDA NAO E A ENTREGA (s015), COMPOSICAO (s016) e PROPORCAO COM O
PRAZO (s017). Esta e a QUINTA familia distinta do dia no canal.

O QUE SOBRA PARA A PROXIMA: "Quando nao vale" + "Se voce ja esta perto da idade"
— a familia QUANDO O CONSERTO NAO COMPRA NADA, o lado oposto desta, e tambem sem
numero. Terceiro angulo deste longo.

## FONTES
O longo de onde este short foi extraido (`labtreinamento-006`, `4OYBkCHFTV8`)
carrega a norma com a fonte. Este short NAO introduz numero novo sobre o mundo —
ele nao introduz numero nenhum — entao nao exige fonte institucional nova.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s018",
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
    grava(SPEC, "fabrica/specs/labtreinamento-s018.json")
    est = duracao_estimada_short(SHORT, SPEC["voz"])
    real = duracao_real_prevista(SHORT, SPEC["voz"], "piper")
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"PECA 2 DAS DEZ | {len(SHORT)} cenas | dinheiro proprio | 4OYBkCHFTV8")
    print(f"estimado: {est:.1f}s | REAL previsto: {real:.1f}s | mira REAL {lo}-{hi}")
    print(f"real na mira? {'SIM' if lo <= real <= hi else 'NAO'}")
    print(f"por plano: {real/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
