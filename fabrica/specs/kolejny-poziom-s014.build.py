"""kolejny-poziom-s014 — stawka podatku nie jest kosztem; oplata jest.

ALAVANCA desta rodada, uma coisa so: MIRAR O PISO DO `ALVO_SHORT` (41,5) NO
POLONES. O aprendizado 679 prescreveu isso e eu nao apliquei em nenhuma peca
polonesa ainda — as duas ultimas foram no TOPO e sairam em 43,37 (kol-s011,
+3,5%) e PT43S (kol-s013), a um fio dos 45 s que o YouTube arredonda PARA CIMA.
O centro do residuo polones e ~+2,2, o unico das tres vozes que e POSITIVO.
NUMERO DE PARTIDA: 43,37 s reais do kol-s011, e PT44S no contador do YouTube.

O QUE DEU CERTO: o kolejny e o epomeno estao fortes com mediana de tres leituras
concordantes — kol-s009 460 as 15 h, epo-s009 440 as 16 h, epo-s011 406 as 8,7 h,
epo-s012 333 as 7 h, kol-s011 299 as 7,9 h. Nenhuma peca de 09/10 passou das
12 h, entao o experimento 38 (duracao ao teto) NAO tem veredito.

O QUE NAO DEU, e e a correcao desta rodada: eu disse que o tratamento novo tinha
aberto um buraco de fator 30 no labtreinamento. O comparador estava escolhido a
dedo. Usei o lab-s007 (149 as 13 h) como "linha de base do tratamento antigo", e
ele e a MELHOR peca do canal — as outras tres do mesmo tratamento fazem 41, 36 e
41. A mediana antiga e 41, nao 149. Contra 41, o lab-s008 com 14 as 8,6 h nao e
buraco nenhum. O que os numeros dizem e mais simples e mais duro: o
labtreinamento faz ~41 onde os outros dois fazem 212 a 460, NOS DOIS TRATAMENTOS.
Invalidei o 682 e escrevi o 684.

E O NUMERO QUE IMPORTA NAO ANDOU: inscritos em 8 / 16 / 67 na NONA leitura
consecutiva igual, contra ~2.100 views acumuladas hoje. O experimento 37 (pedido
de inscricao no kicker do CTA) esta em NOVE pecas com zero inscrito novo. A 1,3
por mil, 2.100 views valem ~2,7 inscritos; zero ainda cabe no ruido de Poisson
(~7%), entao NAO refuto — mas a regra 7 manda desfazer o que nao move o numero em
tres pacotes, e esta em nove.

DE ONDE SAI: longo `iqV7m6tKb5A` (kolejny-poziom-004), capitulo "TERAZ WAZNE —
kolejnosc, nie stawka". O short ORIGINAL do pacote faz a conta da taxa de dois
por cento e PARA ali: nao toca na INVERSAO entre taxa e imposto, que e a entrada
errada e e aritmetica pura. A inversao nao vem das aliquotas, vem do TEMPO: a
taxa age todo ano sobre capital que ia trabalhar, o imposto age UMA vez sobre
ganho que ja aconteceu.

TITULO EM PERGUNTA, que e a forma que o PL/26 realmente premia (seis de quinze,
contra dois a tres no BR e no GR).
FEED PL NAO RELIDO nesta rodada — lido as 06:1x, tres horas, dentro da janela do
623, que mediu 14 de 15 titulos identicos em quatro horas e meia.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita aliquota de
# imposto, nao cita taxa de administracao, nao cita limite de conta, nao cita
# prazo nem idade, e nao nomeia produto. Conferido A MAO campo por campo, porque
# o portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA: a aliquota do imposto sobre o ganho e os limites anuais das
# contas sao definidos por lei e por obwieszczenie, e mudam de ano para ano. O
# proprio longo datou o limite do IKE num obwieszczenie de novembro — um short
# com aquele numero fica errado e continua no ar. O que NAO envelhece e a
# INVERSAO, e e ela que este short carrega.
#
# NUMERAIS NA NARRACAO: "raz" (uma vez) e "co roku" (todo ano) — descrevem a
# FREQUENCIA, que e exatamente o mecanismo, nao o mundo. Uma quantidade por
# frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que uma taxa anual pode custar mais que um imposto de
# aliquota varias vezes maior, porque a taxa age todo ano sobre capital que ia
# render e corta tambem o crescimento futuro, enquanto o imposto age uma vez
# sobre ganho que ja aconteceu; e que por isso se compara PRIMEIRO a taxa anual.
# Esta no longo kolejny-poziom-004 (`iqV7m6tKb5A`), capitulo "TERAZ WAZNE —
# kolejnosc, nie stawka".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a aliquota do imposto sobre o ganho — definida por lei, muda;
#   (2) a taxa de administracao em pontos percentuais e os valores em zloty, que
#       dependem do produto DELE e da propria simulacao do longo;
#   (3) os limites anuais das contas e as idades de saque, que vem de
#       obwieszczenie anual e envelhecem em meses.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Co kosztuje więcej?", "sub": "podatek czy opłata",
     "nar": "Porównujesz stawkę podatku, bo jest większa. A koszt siedzi w "
            "opłacie, która wygląda na nic.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Opłatę płacisz", "sub": "co roku",
     "nar": "Opłatę płacisz co roku, z kapitału, który miał pracować. Zabrana "
            "złotówka już nie zarobi.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Podatek płacisz", "sub": "raz",
     "nar": "Podatek płacisz raz, od zysku, który już się zdarzył. Do tego "
            "momentu cała kwota pracuje dla ciebie.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Odwrotność", "sub": "z czasu, nie ze stawek",
     "nar": "Dlatego niższa stawka opłaty kosztuje więcej niż wyższa stawka "
            "podatku. Ta odwrotność bierze się z czasu.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne",
     "nar": "Porównuj najpierw opłatę roczną, a potem podatek. Zasubskrybuj na "
            "następne, a cała kwota jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Opłata", "l2": "co roku"}

COPY = """# kolejny-poziom-s014

## TITULO
Dlaczego Opłata Roczna Kosztuje Więcej Niż Podatek od Zysku, Choć Jej Stawka Jest Niższa

## TITULO SHORT
Co kosztuje więcej: podatek czy opłata?

## DESCRICAO
Kiedy porównujesz dwa produkty emerytalne, pierwsze, co widzisz, to stawka podatku — bo jest duża i napisana grubą czcionką. Opłata za zarządzanie wygląda przy niej na zaokrąglenie. I właśnie dlatego kosztuje więcej.

Mechanizm jest arytmetyczny i nie ma w nim nic spornego. Opłatę płacisz co roku, z kapitału, który miał pracować — a złotówka zabrana w piątym roku nie zarobi już nic przez wszystkie lata, które zostały. Podatek płacisz raz, przy wypłacie, od zysku, który już się zdarzył; do tego momentu cała kwota pracuje dla ciebie, podatek i tak.

Stąd odwrotność, która brzmi nielogicznie, dopóki nie policzysz: niższa stawka opłaty może cię kosztować więcej niż wyższa stawka podatku. Ta odwrotność nie bierze się ze stawek — bierze się z czasu. Procent zabierany co roku wycina także przyszły wzrost. Podatek zabiera plaster z tortu, który już urósł.

Wniosek praktyczny jest jednym zdaniem: jeśli masz porównać dwa produkty, najpierw porównaj opłatę roczną, a dopiero potem zastanawiaj się nad podatkiem. I to działa też w drugą stronę — każdy obniżony punkt procentowy opłaty pracuje dla ciebie przez cały okres, bez żadnego ryzyka.

Nie ma tu stawki podatku, wysokości opłaty, limitów rocznych ani wieku wypłaty, i jest to świadome: te liczby są ustalane ustawą i obwieszczeniem, i zmieniają się rok do roku. Odwrotność nie zmienia się wcale. Pełna kwota w złotych, oba rachunki obok siebie, limity z datą obwieszczenia i legalne obejście podatku — są w pełnym filmie.

## COMENTARIO FIXADO
Najczęstszy błąd nie jest w rachunku, jest w kolejności patrzenia: najpierw sprawdzasz stawkę podatku, bo jest większa, a koszt siedzi w opłacie. Opłata działa co roku i wycina także przyszły wzrost; podatek działa raz, od zysku, który już urósł. Dlatego niższa stawka opłaty może kosztować więcej niż wyższa stawka podatku — i ta odwrotność nie bierze się ze stawek, tylko z czasu. Praktycznie: porównuj najpierw opłatę roczną. I żeby było jasno, bo film nie jest przeciw podatkowi: podatku nie unikniesz wyborem produktu, a opłatę owszem. Kto porównywał dwa produkty, napiszcie w komentarzach tylko, czy opłata była w tabeli czy w regulaminie — bez kwot.

## HASHTAGS
#Oszczedzanie #Emerytura #KolejnyPoziom

## TAGS
oplata za zarzadzanie, podatek od zysku, procent skladany, koszt oplaty, porownanie produktow, oszczedzanie dlugoterminowe, emerytura, finanse osobiste, kapital, stopa zwrotu, wplaty miesieczne, kolejny poziom, planowanie finansowe, oplata roczna, wzrost kapitalu

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita aliquota,
taxa, limite anual, prazo nem idade, e nao nomeia produto. Conferido a mao campo
por campo.

A REGRA (g) MANDA: aliquota do imposto e limites anuais vem de lei e de
obwieszczenie e mudam de ano para ano. A INVERSAO nao envelhece, e e ela que este
short carrega.

NUMERAIS NA NARRACAO: "raz" e "co roku", que descrevem a FREQUENCIA — o proprio
mecanismo, nao o mundo.

O QUE O VIDEO AFIRMA: que uma taxa anual pode custar mais que um imposto de
aliquota varias vezes maior, porque a taxa age todo ano sobre capital que ia
render e corta tambem o crescimento futuro, enquanto o imposto age uma vez sobre
ganho que ja aconteceu; logo compara-se PRIMEIRO a taxa anual. Esta no longo
kolejny-poziom-004 (iqV7m6tKb5A), capitulo "TERAZ WAZNE — kolejnosc, nie stawka".

DESCARTADO, e vai escrito:
  (1) a aliquota do imposto sobre o ganho, definida por lei;
  (2) a taxa em pontos percentuais e os valores em zloty, que dependem do produto
      DELE;
  (3) os limites anuais e as idades de saque, de obwieszczenie anual.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-004, iqV7m6tKb5A) traz as
fontes oficiais, inclusive a data do obwieszczenie dos limites. Este short nao
introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s014",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "iqV7m6tKb5A",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s014.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (PISO: centro pl ~ +2,2%)")
    print(f"na mira? {'SIM' if lo <= s <= lo + 0.6 else 'NAO — mire o PISO'} | "
          f"real previsto {s*1.004:.1f} a {s*1.044:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
