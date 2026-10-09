"""kolejny-poziom-s015 — nao, a pensao inteira nao entra na faixa de cima.

ALAVANCA desta rodada, uma coisa so na FORMA: o RITMO DE CORTE. Dez cenas em vez
de cinco, mantendo a duracao. Experimento 40.
NUMERO DE PARTIDA: 8,3 s por plano e 91% dos quadros com diferenca abaixo de 1,0
numa escala de 0-255 (aprendizado 690). Esta peca sai com 4,2 s por plano e
VINTE falas de legenda contra cinco.

E O CANAL MUDOU DE PRIORIDADE, por dado e nao por gosto. Com os 388 registros
reais de Analytics, inscrito por VIDEO DISTINTO: kolejny short 1,00 (16 videos,
16 inscritos) contra epomeno short 0,45 e labtreinamento short 0,29. O unico que
bate isso e o LONGO do epomeno, com 1,25 — e ele custa ~80 cenas contra 10, logo
o short do kolejny e ~14x mais eficiente por unidade de producao. A 1,00 por
peca, os 492 inscritos que faltam sao 492 shorts: a sete por dia, ~70 dias,
DENTRO dos 115 que restam para 1/FEV/2027. E o unico canal com caminho.
Aprendizado 691.

O QUE DEU CERTO: o conserto do dinamismo. A legenda queimada era UMA fala para a
cena inteira e virou grupos de quatro palavras; medido em render real, 3 -> 8
quadros DISTINTOS em 273. E a cena ZERO perdeu o fade de entrada, que punha preto
de t=0 a t=0,067 dentro do primeiro segundo.

O QUE NAO DEU, e e correcao de uma regra que eu escrevi HOJE: eu pus "dez a
CATORZE cenas" no CLAUDE.md sem conferir a sobrecarga. Ha ~1,9 s FIXOS por cena,
entao doze cenas gastariam 22 s so em padding e estourariam o teto. O teto real
no alvo atual e ONZE. Corrigido para "dez a onze".

O QUE VOU MUDAR: nada alem do ritmo. O `epomeno-s011` cruza as 12 h as 12:31 e e
a primeira leitura limpa do experimento 38; mexer na duracao agora cegaria a
unica medida limpa do dia.

DE ONDE SAI: longo `SP7Vz8qHdRY` (kolejny-poziom, o limiar da escala), e a
entrada errada e a mais classica da aritmetica tributaria: presume-se que
atravessar o limiar poe a PENSAO INTEIRA na aliquota de cima. Nao poe — a escala
age em CAMADAS, e so a NADWYZKA, a parte acima do limiar, muda de aliquota. O
medo do limiar custa mais que o limiar.

TITULO EM PERGUNTA, que e a forma do PL/26 (seis de quinze, contra dois a tres
no BR e no GR).
FEED PL NAO RELIDO nesta rodada — lido as 11:1x, uma hora, DENTRO da janela de
quatro horas e meia do 623.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o valor do
# limiar, nao cita nenhuma das duas aliquotas, nao cita salario e nao cita data.
# Conferido A MAO campo por campo, porque o portao `narracao` conta QUANTIDADES
# por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA: o valor do limiar e as aliquotas da escala vem de lei e
# mudam — o proprio titulo do longo carrega "propozycja na 2027", ou seja ja
# existe proposta de mudanca. Um short com o numero deste ano fica errado e
# continua no ar. O que NAO envelhece e a MECANICA DE CAMADAS, e e ela que este
# short carrega.
#
# NUMERAIS NA NARRACAO: "krok jeden" e "krok dwa", que numeram os passos do
# raciocinio, e "dwa odejmowania" saiu na reducao. Uma quantidade por frase; o
# limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que a aliquota maior incide SO sobre a parte do
# rendimento acima do limiar, nao sobre o rendimento inteiro; que por isso um
# aumento nunca reduz o que sobra; e que a conta e subtrair o limiar do
# rendimento e aplicar a aliquota maior somente sobre essa diferenca. Esta no
# longo `SP7Vz8qHdRY` (kolejny-poziom, o limiar da escala).
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o valor do limiar e as duas aliquotas — de lei, e com proposta de
#       mudanca ja no titulo do longo;
#   (2) qualquer salario de exemplo, que depende do espectador;
#   (3) a data de vigencia da proposta, que e de calendario.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Cała pensja?", "sub": "nie, tylko nadwyżka", "nar": "Dostałeś podwyżkę i boisz się progu podatkowego.", "sem_cap": True},
    {"layout": "item", "kicker": "Mit", "preco": "cała pensja", "nar": "Myślisz, że wyższa stawka obejmie wszystko.", "sem_cap": True},
    {"layout": "item", "kicker": "Prawda", "preco": "tylko nadwyżka", "nar": "Obejmuje tylko złotówki ponad samym progiem.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Skala działa", "sub": "warstwami", "nar": "Skala działa warstwami, nie przełącznikiem.", "sem_cap": True},
    {"layout": "item", "kicker": "Pod progiem", "preco": "stawka niższa", "nar": "Co mieści się pod progiem, zostaje niżej.", "sem_cap": True},
    {"layout": "item", "kicker": "Ponad progiem", "preco": "stawka wyższa", "nar": "Dopiero reszta wchodzi na wyższą stawkę.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dlatego", "sub": "podwyżka nie zabiera", "nar": "Dlatego podwyżka nigdy nie zmniejsza wypłaty.", "sem_cap": True},
    {"layout": "item", "kicker": "Krok jeden", "preco": "odejmij próg", "nar": "Odejmij próg od dochodu. To jest nadwyżka.", "sem_cap": True},
    {"layout": "item", "kicker": "Krok dwa", "preco": "licz tylko ją", "nar": "Wyższą stawkę licz tylko od nadwyżki.", "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne", "nar": "Strach przed progiem kosztuje więcej niż sam próg.", "sem_cap": True}
]

THUMB = {"l1": "Tylko", "l2": "nadwyżka"}

COPY = """# kolejny-poziom-s015

## TITULO
Czy Przekroczenie Progu Podatkowego Obejmuje Całą Pensję? Skala Działa Warstwami

## TITULO SHORT
Czy cała pensja wchodzi w wyższy próg?

## DESCRICAO
To jest najczęstszy błąd arytmetyczny w rozmowie o podatkach, i kosztuje prawdziwe pieniądze: ludzie odmawiają podwyżki albo nadgodzin, bo sądzą, że przekroczenie progu przeniesie **całą** pensję na wyższą stawkę. Nie przeniesie.

Skala działa warstwami, nie jednym przełącznikiem. To, co mieści się pod progiem, zostaje na niższej stawce — całe, bez zmian. Dopiero nadwyżka, czyli złotówki ponad progiem, wchodzi na wyższą stawkę. Pierwsza złotówka ponad progiem jest opodatkowana wyżej, i jest to dokładnie jedna złotówka, nie cała pensja.

Dlatego podwyżka nigdy nie zmniejsza tego, co zostaje w kieszeni. Może zmniejszyć procent, który zostaje z każdej kolejnej złotówki — i to jest zupełnie inne zdanie niż "stracę na podwyżce".

Rachunek, który to rozstrzyga, to dwa odejmowania, nie jedno mnożenie: odejmij próg od swojego dochodu, i wyższą stawkę licz tylko od tej różnicy. Resztę zostaw na niższej. Jeśli ktoś mnoży cały dochód przez wyższą stawkę, liczy inny kraj.

Nie ma tu wysokości progu ani żadnej ze stawek, i jest to świadome: te liczby są ustalane ustawą i już jest propozycja ich zmiany — sam tytuł pełnego filmu ją wymienia. Mechanika warstw nie zmienia się wcale. Kwoty z datą, obie stawki, miejsce na skali i co zmienia propozycja — są w pełnym filmie.

## COMENTARIO FIXADO
Najdroższy błąd w tej rozmowie nie jest w stawce, jest w ZAKRESIE: wyższa stawka obejmuje tylko NADWYŻKĘ ponad progiem, nigdy całej pensji. Skala działa warstwami — co pod progiem, zostaje niżej; dopiero reszta idzie wyżej. Dlatego podwyżka nie zmniejsza wypłaty, a rachunek to dwa odejmowania, nie jedno mnożenie: dochód minus próg, i wyższą stawkę licz tylko od różnicy. I żeby było jasno, bo film nie twierdzi, że progi są nieważne: zmieniają procent z KAŻDEJ NASTĘPNEJ złotówki, i to warto planować. Kto odmówił kiedyś nadgodzin z powodu progu, napiszcie w komentarzach tylko czy policzyliście to przed, czy po — bez kwot.

## HASHTAGS
#Podatki #ProgPodatkowy #KolejnyPoziom

## TAGS
prog podatkowy, skala podatkowa, nadwyzka, stawka podatku, podwyzka a podatek, nadgodziny podatek, dochod a prog, finanse osobiste, rozliczenie roczne, planowanie podatkowe, kolejny poziom, wyplata netto, zaliczka na podatek, kwota ponad progiem, dwie stawki

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o valor do
limiar, nao cita aliquota, nao cita salario e nao cita data. Conferido a mao
campo por campo.

A REGRA (g) MANDA: o limiar e as aliquotas vem de lei e ja existe PROPOSTA DE
MUDANCA — o proprio titulo do longo a cita. A MECANICA DE CAMADAS nao envelhece,
e e ela que este short carrega.

NUMERAIS NA NARRACAO: "krok jeden" e "krok dwa", que numeram os passos.

O QUE O VIDEO AFIRMA: que a aliquota maior incide SO sobre a parte acima do
limiar e nao sobre o rendimento inteiro; que por isso um aumento nunca reduz o
que sobra; e que a conta e subtrair o limiar e aplicar a aliquota maior somente
sobre a diferenca. Esta no longo SP7Vz8qHdRY.

DESCARTADO, e vai escrito:
  (1) o valor do limiar e as duas aliquotas, de lei e com proposta de mudanca;
  (2) qualquer salario de exemplo, que depende do espectador;
  (3) a data de vigencia da proposta.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom, SP7Vz8qHdRY) traz as
fontes oficiais e as datas. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s015",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "SP7Vz8qHdRY",
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-s015.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas (antes 5)")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | PISO no pl, centro +2,2%")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*1.004:.1f} a {s*1.044:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s (antes 8,3s)")
    print(f"falas de legenda: {sum(len(LG.pedacos(c['nar'])) for c in SHORT)} (antes 5)")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"esqueleto: {variedade.esqueleto(SHORT)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
