"""kolejny-poziom-s016 — a cena que o jornal anuncia pode nao ser a sua.

ALAVANCA desta rodada, uma coisa so: NADA de forma. Esta peca repete
exatamente o `kolejny-poziom-s015` — dez cenas, mesmo esqueleto, piso polones —
porque o aprendizado 693 acabou de dizer que, com CV 0,66 entre pecas, eu
preciso de SETE pecas por braco para enxergar ate um DOBRO. Mudar a forma de
novo agora comecaria um terceiro braco com n=1 e nenhum dos tres fecharia.
NUMERO DE PARTIDA: o braco de dez cenas tem n=1 (o s015). Esta e a segunda.

O QUE DEU CERTO: o epomeno ganhou UM inscrito, 16 -> 17, primeiro delta do dia
em ~14 h. E e UM evento, nao uma medida de conversao.

O QUE NAO DEU, e e a conta mais dura do dia: medi a dispersao DENTRO do mesmo
tratamento e canal e deu CV 0,66 — epomeno 218-445, kolejny 96-462,
labtreinamento 41-162. Com esse CV, detectar 25% pede ~109 pecas por braco, 50%
pede 28, e so um DOBRO cabe em 7. Views por peca e cego para qualquer coisa
menor que o dobro, e isso tira a confianca de varias leituras que eu dei como
fortes hoje. Aprendizado 693, critico.
O experimento 38 segue SEM VEREDITO: o epomeno novo le 412 contra mediana antiga
332, e o 412 cai DENTRO da faixa antiga de 218-445.

O QUE VOU MUDAR: nada. Esta rodada e volume no braco que ja existe.

DE ONDE SAI: longo `vcJf6WipLtY` (kolejny-poziom-012, a conta de luz), capitulos
"Taryfa to nie to samo co oferta" e "Dystrybucja sie nie zmienia". O short
ORIGINAL do pacote faz as DUAS METADES da fatura e manda dividir o valor pelo
consumo — e PARA ali. A entrada errada e outra e nao foi usada: presume-se que a
cena que o regulador aprova e A SUA. Nao e, se voce esta numa OFERTA assinada; e
mesmo que fosse, trocar de vendedor mexe em UMA das duas metades, porque a
distribuicao nao muda com assinatura nenhuma.

FAMILIA DIFERENTE da peca de 12:17 de hoje no mesmo canal, como a regra (f)
exige: o `s015` era limiar e camadas; esta e COMPOSICAO — duas metades, e so uma
responde ao contrato.

TITULO EM PERGUNTA, a forma do PL/26.
FEED PL NAO RELIDO — lido as 11:1x, tres horas, dentro da janela do 623.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita preco
# aprovado, nao cita tarifa de distribuicao, nao cita percentual, nao cita data e
# nao nomeia vendedor nem regiao. Conferido A MAO campo por campo, porque o
# portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA, e o proprio longo prova: ele tem um capitulo chamado "a
# liczba z naglowka starzeje sie szybciej niz metoda" — o numero do cabecalho
# envelhece mais rapido que o metodo. O preco aprovado muda por ato do
# regulador e a tarifa de distribuicao depende da REGIAO. O que NAO envelhece e
# a distincao TARIFA vs OFERTA, e que a distribuicao nao se move com assinatura.
#
# NUMERAIS NA NARRACAO: "jedna polowe" e "dwie polowy" — uma e duas metades,
# que descrevem a ESTRUTURA da fatura e nao um valor do mundo. Uma quantidade
# por frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que o preco aprovado pelo regulador e a TARIFA, e que
# quem assinou uma OFERTA nao esta nela; que o nome da tarifa e a data de fim do
# contrato estao na fatura; e que trocar de vendedor move apenas a metade de
# venda, porque a distribuicao nao muda com a assinatura. Esta no longo
# kolejny-poziom-012 (`vcJf6WipLtY`), capitulos "Taryfa to nie to samo co
# oferta" e "Dystrybucja sie nie zmienia, cokolwiek podpiszesz".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o preco aprovado e qualquer percentual — ato do regulador, muda;
#   (2) a tarifa de distribuicao, que depende da REGIAO do espectador;
#   (3) datas de vigencia e o mecanismo de congelamento, que o proprio longo diz
#       que ele mesmo nao soube prever.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Zatwierdzona cena", "sub": "to nie twoja cena", "nar": "Cena prądu spadła, a ty czekasz na niższy rachunek.", "sem_cap": True},
    {"layout": "item", "kicker": "Taryfa", "preco": "z urzędu", "nar": "Taryfę zatwierdza regulator. Nie każdego dotyczy.", "sem_cap": True},
    {"layout": "item", "kicker": "Oferta", "preco": "twój podpis", "nar": "Oferta to umowa, którą podpisałeś.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Jeśli masz ofertę", "sub": "nagłówek cię nie dotyczy", "nar": "Na ofercie ta cena cię nie dotyczy.", "sem_cap": True},
    {"layout": "item", "kicker": "Gdzie sprawdzić", "preco": "na fakturze", "nar": "Nazwa taryfy jest na fakturze.", "sem_cap": True},
    {"layout": "item", "kicker": "I druga rzecz", "preco": "data końca", "nar": "Obok niej sprawdź datę końca umowy.", "sem_cap": True},
    {"layout": "titulo", "kicker": "A zmiana sprzedawcy", "sub": "rusza tylko połowę", "nar": "Zmiana sprzedawcy rusza jedną połowę.", "sem_cap": True},
    {"layout": "item", "kicker": "Dystrybucja", "preco": "nie drgnie", "nar": "Dystrybucja nie drgnie, cokolwiek podpiszesz.", "sem_cap": True},
    {"layout": "item", "kicker": "Dlatego licz", "preco": "cenę końcową", "nar": "Porównuj cenę końcową, nie hasło z reklamy.", "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne", "nar": "Dwie połowy oglądaj osobno. Zasubskrybuj.", "sem_cap": True}
]

THUMB = {"l1": "Taryfa", "l2": "czy oferta"}

COPY = """# kolejny-poziom-s016

## TITULO
Zatwierdzona Cena Prądu a Twoja Umowa: Dlaczego Nagłówek Może Cię Nie Dotyczyć

## TITULO SHORT
Zatwierdzona cena to twoja cena?

## DESCRICAO
Co roku wraca ten sam nagłówek: cena prądu zatwierdzona, w górę albo w dół. I co roku wraca to samo rozczarowanie przy fakturze. Powód nie jest w rachunku — jest w tym, że nagłówek mówi o **taryfie**, a ty możesz być na **ofercie**.

To dwie różne rzeczy i warto je rozdzielić raz na zawsze. Taryfę zatwierdza regulator i obowiązuje odbiorców, którzy na niej są. Oferta to umowa, którą kiedyś podpisałeś z konkretnym sprzedawcą — i jej cena nie zmienia się, bo regulator coś ogłosił. Jeśli jesteś na ofercie, zatwierdzona cena po prostu cię nie dotyczy.

Sprawdzenie zajmuje minutę i jest na fakturze: nazwa twojej taryfy, a obok niej data końca umowy. Ta data jest twoją jedyną dźwignią — przed nią nie masz wyboru, po niej masz.

Druga rzecz, którą warto wiedzieć przed jakąkolwiek zmianą: zmiana sprzedawcy rusza tylko jedną połowę rachunku. Dystrybucja nie drgnie, cokolwiek podpiszesz, bo nie kupujesz jej od sprzedawcy. Dlatego porównuje się cenę końcową za cały rok, nie hasło z reklamy — hasło dotyczy połowy, którą można zmienić, i milczy o połowie, której nie można.

Nie ma tu zatwierdzonej ceny, stawki dystrybucyjnej ani żadnej daty, i jest to świadome: te liczby ustala regulator, zależą od regionu i starzeją się szybciej niż metoda. Pełne liczby, sposób policzenia własnej ceny z faktury i co zrobić z datą końca umowy — są w pełnym filmie.

## COMENTARIO FIXADO
Najczęstsze nieporozumienie nie jest w rachunku, jest w słowie: nagłówek mówi o TARYFIE, a bardzo wielu z nas jest na OFERCIE — czyli na umowie podpisanej ze sprzedawcą, której zatwierdzona cena nie dotyczy. Jedna minuta z fakturą rozstrzyga: nazwa taryfy, i obok data końca umowy. Ta data jest całą dźwignią. I druga rzecz: zmiana sprzedawcy rusza tylko połowę rachunku — dystrybucji nie kupujesz od sprzedawcy, więc nie drgnie, cokolwiek podpiszesz. Dlatego porównuj cenę końcową na rok, nie hasło z reklamy. Żeby było jasno, bo film nie mówi, że zmiana się nie opłaca: mówi, że opłaca się policzona. Kto sprawdził na fakturze, napiszcie w komentarzach tylko czy był na taryfie czy na ofercie — bez nazw sprzedawców.

## HASHTAGS
#Prad #Rachunki #KolejnyPoziom

## TAGS
taryfa czy oferta, zatwierdzona cena pradu, dystrybucja energii, rachunek za prad, zmiana sprzedawcy, cena koncowa, faktura za prad, data konca umowy, dwie polowy rachunku, oszczedzanie energii, finanse osobiste, kolejny poziom, regulator energii, sprzedaz energii, koszty stale

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita preco
aprovado, tarifa de distribuicao, percentual nem data, e nao nomeia vendedor ou
regiao. Conferido a mao campo por campo.

A REGRA (g) MANDA, e o longo prova: ele tem um capitulo dizendo que o numero do
cabecalho envelhece mais rapido que o metodo. O preco aprovado muda por ato do
regulador e a distribuicao depende da REGIAO. A distincao TARIFA vs OFERTA nao
envelhece, e e ela que este short carrega.

NUMERAIS NA NARRACAO: "jedna polowe" e "dwie polowy", que descrevem a ESTRUTURA
da fatura.

O QUE O VIDEO AFIRMA: que o preco aprovado e a TARIFA e nao alcanca quem assinou
OFERTA; que o nome da tarifa e a data de fim do contrato estao na fatura; e que
trocar de vendedor move so a metade de venda. Esta no longo kolejny-poziom-012
(vcJf6WipLtY).

DESCARTADO, e vai escrito:
  (1) o preco aprovado e qualquer percentual;
  (2) a tarifa de distribuicao, que depende da regiao;
  (3) datas e o mecanismo de congelamento, que o proprio longo nao soube prever.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-012, vcJf6WipLtY) traz as
fontes oficiais e as datas. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s016",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "vcJf6WipLtY",
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-s016.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | PISO no pl")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*1.004:.1f} a {s*1.044:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
