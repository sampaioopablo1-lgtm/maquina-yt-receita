"""Monta a spec do `kolejny-poziom-s102`.

FAMILIA: o `wynik techniczny` lido como o RESULTADO DA EMPRESA, quando ele e
uma conta SEPARADA — capitulos 40, 41 e 42 do `wb1RGIx7OJI`
(`kolejny-poziom-009`), com os 45 a 48 de apoio. Os quatro irmaos foram lidos
pelo `irmaos_da_origem` e, nos DOIS sem o campo da familia (`s013`, `s062`),
pela PROSA e pela NARRACAO de cada um, que e de primeira mao.

ZERO numero novo sobre o mundo: o eixo e o SIGNIFICADO de um sinal, nao o valor
de nada. Nem skladka media, nem szkoda media, nem percentual, nem przypis, nem
numero de grupo — e nenhum deles aparece na narracao.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import guardas_do_construtor as GC
import layouts_do_short as LS
import temas_do_dono as TD

PAC = "kolejny-poziom-s102"
CANAL = "kolejny-poziom"
SOND = set(LS.desenham())

short = [
    {"layout": "titulo",
     "kicker": "Ta linia zeszła pod zero",
     "sub": "to nie wiadomość o firmie",
     "nar": "Ta linia zeszła pod zero."},
    {"layout": "item",
     "kicker": "Bo to rachunek samych polis",
     "sub": "osobne konto, nie cała firma",
     "nar": "To rachunek samych polis."},
    {"layout": "lista",
     "kicker": "Trzy pozycje i koniec",
     "itens": ["Składki", "Szkody", "Koszty"],
     "nar": "Wchodzą składki, szkody i koszty."},
    {"layout": "barras",
     "kicker": "Czego w nim nie ma",
     "barras": [{"rot": "To konto", "v": 100},
                {"rot": "Zyski z lokat", "v": 0}],
     "nar": "Zysków z lokat w nim nie ma."},
    {"layout": "item",
     "kicker": "A tam zwykle nadrabia",
     "sub": "stratę z rachunku polis",
     "nar": "A tam firma zwykle nadrabia stratę."},
    {"layout": "item",
     "kicker": "Ale nie znaczy też",
     "sub": "że nic się nie zmienia",
     "nar": "Minus tu nie znaczy upadku firmy."},
    {"layout": "titulo",
     "kicker": "Więc minus to nie upadek",
     "sub": "osobne konto, osobny sens",
     "nar": "Ale nie znaczy też, że nic nie zmienia."},
    {"layout": "item",
     "kicker": "Pierwsza czyta to jako groźbę",
     "sub": "firma mi nie wypłaci",
     "nar": "Pierwsza lektura: nie wypłacą mi."},
    {"layout": "item",
     "kicker": "Druga jako nic",
     "sub": "przecież nadrobią gdzie indziej",
     "nar": "Druga: nadrobią, więc nic."},
    {"layout": "lista",
     "kicker": "Obie mylą to samo",
     "itens": ["Konto polis", "Wynik firmy"],
     "nar": "Obie mylą jedno konto z całą firmą."},
    {"layout": "barras",
     "kicker": "Oba równie mylne",
     "barras": [{"rot": "Groźba", "v": 100},
                {"rot": "Nic", "v": 100}],
     "nar": "A to mówi o cenie polisy, nie o firmie."},
    {"layout": "cta",
     "kicker": "Kolejny Poziom",
     "sub": "subskrybuj",
     "nar": "Sprawdź datę wznowienia i subskrybuj."},
]

for i, c in enumerate(short):
    assert c["layout"] in SOND, (i, c["layout"], "FORA do conjunto SONDADO")

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "longo_existente": "wb1RGIx7OJI",
    "longo": [],
    "thumb": {"l1": "Minus nie znaczy", "l2": "upadek"},
    "paleta": TD.paleta_do_canal(CANAL),
    "short": short,
    "copy": open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "copy-" + PAC + ".md"), encoding="utf-8").read(),
}

GC.exige(sp)
print(json.dumps(sp, ensure_ascii=False, indent=1))
