# -*- coding: utf-8 -*-
"""kolejny-poziom-s068 — SEGUNDO angulo do longo publicado hoje neste canal.

PAUTA: origem `GtmoaQMr_1c` (o longo `kolejny-poziom-020`, publicado as 13:49Z),
rank 1 do canal e com ZERO shorts declarados. O short que saiu NO pacote usou a
familia do DENOMINADOR (a stawka netto por hora); este usa outra, dos capitulos
51 e 52: QUAL despesa sai muito pior em horas do que parece em zloty — a
pequena e MENSAL, porque multiplica por doze.

FAMILIA DE ENTRADA ERRADA (nova no canal): julgar a despesa pelo tamanho do
valor UNICO, quando o que pesa e a repeticao. A grande e uma vez perde para a
pequena e todo mes.

E ELA E DIFERENTE DA QUE EU ESCREVI NO EPOMENO UMA HORA ANTES, de proposito: la
era o ALVO em meses (de onde sai a tua propria meta); aqui e QUAL conta medir
primeiro. Escrever o mesmo angulo nos tres canais seguidos seria o habito do 762
numa dimensao nova — mesma pauta atravessando canal.

ORCAMENTO: `mira.orcamento` da 45 caracteres por cena para dez cenas no PISO
(41,5), pela PREVISAO REAL do edge — a voz polonesa tem `P` maior, logo cabe
menos texto que no grego (55) e no pt-BR.
"""
import json
import os

RAIZ = "/home/user/maquina-yt-receita"
PAC = "kolejny-poziom-s068"

SHORT = [
    dict(layout="titulo", kicker="Duża czy mała", sub="to złe pytanie",
         nar="Duża czy mała to nie jest to właściwe pytanie."),
    dict(layout="item", kicker="Jedna duża kwota", preco="raz w roku",
         nar="Duży wydatek raz w roku widzisz i go pamiętasz."),
    dict(layout="item", kicker="Mała kwota", preco="dwanaście razy",
         nar="Mała kwota wraca co miesiąc i wcale nie boli."),
    dict(layout="barras", kicker="To samo w godzinach",
         barras=[{"rotulo": "Raz", "valor": 3},
                 {"rotulo": "Co miesiąc", "valor": 12}],
         nar="W godzinach ta mała wychodzi znacznie gorzej."),
    dict(layout="titulo", kicker="Mnożnik", sub="to dwanaście",
         nar="Ukryty mnożnik jest jeden i wynosi dwanaście."),
    dict(layout="lista", kicker="Tu liczba boli",
         itens=["Abonamenty", "Dojazd", "Drobne raty", "Opłaty stałe"],
         nar="Cztery rzeczy wychodzą gorzej, niż wyglądają."),
    dict(layout="item", kicker="Policz w godzinach", preco="nie w złotych",
         nar="Przelicz każdą z nich na swoje godziny pracy."),
    dict(layout="item", kicker="Potem porównaj", preco="z jedną dużą",
         nar="Dopiero wtedy porównaj je z tą jedną dużą kwotą."),
    dict(layout="item", kicker="Kolejność", preco="najpierw licz",
         nar="Najpierw licz, a granicę wyznaczaj na końcu."),
    dict(layout="cta", kicker="Która wyszła gorzej", sub="napisz pod spodem",
         nar="Napisz pod spodem, która wyszła u ciebie gorzej."),
]

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "longo_existente": "GtmoaQMr_1c",
    "longo": [],
    "short": SHORT,
    "thumb": {"l1": "Mała kwota", "l2": "boli dłużej"},
    "paleta": {"bg": "#0B0B0C", "ink": "#F2EEE8", "c1": "#E23B3B",
               "c2": "#D9C7A7", "red": "#FF4D4D", "ok": "#7FB77E",
               "panel": "#151517", "mut": "#8F877C", "acc": "#E23B3B"},
    "copy": "{COPY}",
}

alvo = os.path.join(RAIZ, "fabrica", "specs", PAC + ".json")
copy = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy_kp068s.txt"), encoding="utf-8").read()
sp["copy"] = copy
with open(alvo, "w", encoding="utf-8") as fh:
    json.dump(sp, fh, ensure_ascii=False, indent=1)
print("spec gravada:", alvo)
print("cenas:", len(SHORT), "| media de chars:",
      sum(len(c["nar"]) for c in SHORT) // len(SHORT))
print("esqueleto:", "-".join(c["layout"] for c in SHORT))
