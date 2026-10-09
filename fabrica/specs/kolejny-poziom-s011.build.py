"""kolejny-poziom-s011 — a sua nadplata encurta o PRAZO ou a PRESTACAO?

ALAVANCA: segundo ponto do experimento 38 (duracao ao teto), agora na voz de
PIOR caso. A `pl-PL-Marek` e a unica das tres com residuo POSITIVO medido
(+4,4% a −1,8%), entao miro o PISO da faixa `ALVO_SHORT` e nao o topo: 41,5
estimados x 1,044 = 43,3 reais, ainda abaixo dos 45 do portao. O topo da faixa
(43,0) e para pt-BR e el, cujos residuos sao sempre negativos. **A faixa tem dois
extremos justamente para isso; usar o topo aqui seria ignorar a medicao.**

O QUE DEU CERTO: o primeiro ponto do 38, `labtreinamento-s008`, saiu em 40,63 s
reais contra 42,4 estimados (−4,2%, dentro da faixa da Thalita) — **+16,8% de
duracao** contra a media real de 34,8 s das dezenove pecas de 08/10, pelo mesmo
custo de producao.

O QUE NAO DEU, e e sobre mim: em duas rodadas seguidas a minha propria correcao
precisou de correcao. As 00:44 afirmei que o `epomeno-s009` tinha 326 views, "a
mediana de tres leituras", e que o 415 era outlier. Com cinco leituras a serie e
415, 326, 326, 415, 362 — o 415 voltou e apareceu um terceiro valor. Nao havia
outlier, havia DISPERSAO: faixa de 89, ou 27%. No mesmo intervalo o
`kolejny-s009` deu 441, 457, 457, 441, 458 — faixa de 17, ou 3,9%. **A amplitude
e da PECA, nao da API.** Aprendizado 674; o 673 foi invalidado.

O QUE VOU MUDAR: uma coisa so, e e a FORMA DO TITULO. O feed PL/26 desta rodada
(200, 15 itens, lido) nao tem nada educacional, e **seis de quinze titulam em
PERGUNTA** — Czy, Dlaczego, Ktory, Ktora, Jak, Czemu — mais dois imperativos em
segunda pessoa: oito de quinze enderecam o espectador. O feed BR/26 da rodada
anterior mostrou o mesmo padrao. Os meus titulos vinham sendo afirmacao ou
aforismo. Este e pergunta, e e a pergunta que a peca responde.
NUMERO DE PARTIDA: 27 views do short do pacote de origem; mediana de 457 do
melhor solto do canal, as 6,9 h.

DE ONDE SAI: longo `EwUkhdwyuuo` (kolejny-poziom-013, o preco do prazo do
credito), capitulo "Trzecia opcja | ktorej nikt nie liczy", itens "I co skraca",
"Bo tylko jedno" e "I policz obie wersje". O short ORIGINAL do pacote faz as
quatro liberacoes e as duas multiplicacoes, e para ali — a terceira opcao e o que
a nadplata encurta ficam inteiros de fora.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita taxa, nao
# cita prazo, nao cita valor de prestacao, nao cita percentual e nao nomeia
# banco. Conferido A MAO campo por campo, porque o portao `narracao` conta
# QUANTIDADES por frase e NAO pega digito cru.
#
# UNICO NUMERAL NA NARRACAO: "dwa mnozenia" (duas multiplicacoes). E o NOME da
# operacao, herdado do proprio longo, nao afirmacao sobre o mundo. Uma quantidade
# na frase; o limite do portao e tres.
#
# E ESTE E O PONTO: a resposta certa esta na UMOWA do espectador, nao numa regra
# geral. Bancos e contratos diferem em se a nadplata encurta o prazo ou reduz a
# prestacao, e dizer qual e "o normal" seria inventar regra onde existe cláusula.
#
# O QUE O VIDEO AFIRMA: que a nadplata pode encurtar o PRAZO ou reduzir a
# PRESTACAO, que sao efeitos diferentes; que encurtar o prazo retira mais juros
# que reduzir a prestacao; e que a conta e a MESMA do short original, trocando o
# segundo prazo. Esta no longo kolejny-poziom-013 (`EwUkhdwyuuo`), capitulo
# "Trzecia opcja", itens "I co skraca", "Bo tylko jedno" e "I policz obie wersje".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qual das duas formas o banco aplica por padrao — e CLAUSULA e varia por
#       contrato; o video manda CONFERIR, nao presumir;
#   (2) se a nadplata tem custo ou limite, que o longo manda verificar e que NAO
#       foi reconferido nesta rodada em duas fontes;
#   (3) se vale nadplatar, que depende da alternativa de uso do dinheiro.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Nadpłacasz kredyt?", "sub": "co ona skraca?",
     "nar": "Zdecydowałeś, że będziesz nadpłacać kredyt. Ale wiesz, co dokładnie "
            "twoja nadpłata skraca?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Prawie każdy zakłada", "sub": "że okres",
     "nar": "Prawie każdy zakłada, że skraca okres. Umowa może zamiast tego "
            "obniżyć ratę, a okres zostawić bez zmian.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "To nie to samo", "sub": "i to kosztuje",
     "nar": "To nie to samo. Skracanie okresu zabiera więcej odsetek, bo zabiera "
            "właśnie te miesiące, w których odsetki by narosły.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Sprawdź w umowie", "sub": "potem policz",
     "nar": "Sprawdź w umowie, co wybiera twoja nadpłata, a potem policz to tym "
            "samym rachunkiem: dwa mnożenia i odejmowanie.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Subskrybuj", "sub": "na kolejne",
     "nar": "Policz na swojej umowie, nie na przykładzie. Subskrybuj na kolejne, "
            "a cały rachunek jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Okres", "l2": "czy rata?"}

COPY = """# kolejny-poziom-s011

## TITULO
Nadpłata Kredytu: Skraca Okres czy Obniża Ratę? To Dwie Różne Decyzje

## TITULO SHORT
Nadpłata skraca okres czy ratę?

## DESCRICAO
Decyzja o nadpłacaniu kredytu wydaje się jedną decyzją, a są w niej dwie. Pierwsza to czy nadpłacać. Druga, o której prawie nikt nie myśli, to co ta nadpłata ma skrócić — i od niej zależy, ile odsetek faktycznie zostaje w twojej kieszeni.

Nadpłata może działać na dwa sposoby. Może skrócić okres kredytu, zostawiając ratę taką, jaka była. Albo może obniżyć ratę, zostawiając okres bez zmian. Z zewnątrz obie wyglądają jak sukces, bo w obu coś spada. Ale to nie są równoważne wyniki: skracanie okresu zabiera z kredytu więcej odsetek niż obniżanie raty, bo odsetki naliczają się od pozostałego kapitału przez pozostałe miesiące — a tutaj skracasz właśnie te miesiące.

Z tego wynika praktyczna kolejność. Najpierw sprawdź w umowie, co dokładnie robi twoja nadpłata, bo to jest zapis umowny i różni się między bankami i produktami — nie jest to ogólna zasada, którą ktoś może ci podać z zewnątrz. Potem, jeśli masz wybór, wybierz go świadomie: niższa rata daje margines bezpieczeństwa w gorszym miesiącu, krótszy okres daje niższą sumę na końcu.

A policzyć to możesz tym samym rachunkiem, który już znasz z tego kanału: dwa mnożenia i jedno odejmowanie. Pomnóż ratę przez liczbę miesięcy w jednym wariancie, zrób to samo w drugim, i odejmij jedną sumę od drugiej. Jedyna zmiana polega na tym, że drugim okresem nie jest okres z oferty, lecz okres, do którego realnie skrócisz kredyt nadpłatami.

Zanim oprzesz na tym decyzję, sprawdź jeszcze w umowie, czy nadpłata jest możliwa bez ograniczeń i bez dodatkowych kosztów — tego nie da się założyć. Gdzie znaleźć każdą z liczb, czego ten rachunek nie obejmuje i jak wygląda trzecia opcja, czyli dłuższy okres z nadpłatą — jest w pełnym filmie.

## COMENTARIO FIXADO
Dwie rzeczy do sprawdzenia w umowie, zanim nadpłacisz pierwszą złotówkę. PIERWSZA: czy nadpłata skraca OKRES, czy obniża RATĘ. To zapis umowny, różni się między bankami, i nikt z zewnątrz nie odpowie na to za ciebie. DRUGA: czy nadpłata jest w ogóle możliwa bez limitów i bez dodatkowych kosztów. Jeśli masz wybór i celujesz w niższą sumę odsetek — kierunkiem jest skracanie okresu, nie obniżanie raty. Jeśli bardziej potrzebujesz oddechu w miesiącu, odwrotnie, i to też jest sensowna decyzja. Kto sprawdzi w swojej umowie, niech napisze w komentarzu tylko, który z dwóch wariantów tam znalazł — bez kwot.

## HASHTAGS
#Kredyt #Nadpłata #KolejnyPoziom

## TAGS
nadplata kredytu, skrocenie okresu kredytu, obnizenie raty, kredyt hipoteczny, odsetki kredytu, umowa kredytowa, okres kredytowania, jak nadplacac, finanse osobiste, polska, rachunek kredytu, dwa mnozenia, kolejny poziom, decyzja kredytowa, co skraca nadplata

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pl
defaultAudioLanguage: pl
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita taxa, prazo,
valor de prestacao nem percentual, e nao nomeia banco. Conferido a mao.

UNICO NUMERAL NA NARRACAO: "dwa mnozenia". E o NOME da operacao, herdado do
proprio longo, nao afirmacao sobre o mundo.

E ESTE E O PONTO: a resposta certa esta na UMOWA do espectador. Bancos e
contratos diferem em se a nadplata encurta o prazo ou reduz a prestacao, e dizer
qual e "o normal" seria inventar regra onde existe clausula.

O QUE O VIDEO AFIRMA: que a nadplata pode encurtar o PRAZO ou reduzir a
PRESTACAO, que sao efeitos diferentes; que encurtar o prazo retira mais juros; e
que a conta e a MESMA do short original, trocando o segundo prazo. Esta no longo
kolejny-poziom-013 (EwUkhdwyuuo), capitulo "Trzecia opcja", itens "I co skraca",
"Bo tylko jedno" e "I policz obie wersje".

DESCARTADO, e vai escrito:
  (1) qual das duas formas o banco aplica por padrao — e CLAUSULA e varia;
  (2) se a nadplata tem custo ou limite, que o longo manda verificar e que NAO
      foi reconferido nesta rodada em duas fontes;
  (3) se vale nadplatar, que depende da alternativa de uso do dinheiro.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-013, EwUkhdwyuuo) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s011",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "EwUkhdwyuuo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s011.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    # Em pl o residuo medido chega a +4,4%: miro o PISO da faixa, nao o topo.
    teto_pl = 45.0 / 1.044
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | teto pl seguro {teto_pl:.1f}")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*0.982:.1f} a {s*1.044:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars) | pergunta? "
          f"{'SIM' if tit.rstrip().endswith('?') else 'NAO'}")
    print(f"aponta para: {SPEC['longo_existente']}")
