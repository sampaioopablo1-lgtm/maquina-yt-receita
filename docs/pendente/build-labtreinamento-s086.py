# -*- coding: utf-8 -*-
"""labtreinamento-s086 — SEGUNDO angulo do longo publicado hoje neste canal.

PAUTA: origem `POBNoY16wG8` (o longo `labtreinamento-014`, publicado as
14:37:18Z), rank 1 do canal e com ZERO shorts declarados. O short que saiu NO
pacote usou a familia do DENOMINADOR (quem teve chance de treinar); este usa a
JANELA do periodo, dos capitulos 16 a 23.

FAMILIA DE ENTRADA ERRADA (nova no canal): somar os treinados do historico
INTEIRO e dividir pelas pessoas de HOJE — duas janelas na mesma conta.

ORCAMENTO: `mira.orcamento` da 25 caracteres por cena para NOVE cenas no MEIO da
mira medida do canal (20,0 a 26,0) NO MUNDO EDGE — e essa resposta e REJEITADA
pela propria mira: com 25 o piper cai a 18,6, abaixo do piso de 20,0. Varrido o
orcamento nos DOIS mundos, a janela que satisfaz os dois para nove cenas e
28 a 30 caracteres, e ela mora no TOPO da faixa, nao no meio — e a pinca do 748
aparecendo dentro do instrumento. Escrito com media 28.
"""
import json
import os

RAIZ = "/home/user/maquina-yt-receita"
PAC = "labtreinamento-s086"

SHORT = [
    dict(layout="titulo", kicker="Mesmo treino", sub="três números",
         nar="O mesmo treino dá três números."),
    dict(layout="item", kicker="Só muda a janela", preco="da conta",
         nar="Só muda a janela da conta."),
    dict(layout="lista", kicker="Todas valem",
         itens=["Ano corrido", "Ano fechado", "Trimestre", "Mês a mês"],
         nar="Nenhuma dessas janelas é errada."),
    dict(layout="barras", kicker="A mesma turma",
         barras=[{"rotulo": "Ano corrido", "valor": 62},
                 {"rotulo": "Ano fechado", "valor": 78},
                 {"rotulo": "Trimestre", "valor": 91}],
         nar="O percentual muda junto com ela."),
    dict(layout="titulo", kicker="O erro", sub="é usar duas",
         nar="O erro é usar duas delas."),
    dict(layout="item", kicker="Em cima", preco="o histórico",
         nar="Em cima, todo o histórico."),
    dict(layout="barras", kicker="Janelas diferentes",
         barras=[{"rotulo": "Cima", "valor": 100},
                 {"rotulo": "Baixo", "valor": 40}],
         nar="Embaixo, a folha de hoje."),
    dict(layout="item", kicker="A regra", preco="uma janela",
         nar="A mesma janela nos dois lados."),
    dict(layout="cta", kicker="Qual janela", sub="escreva aqui",
         nar="Qual janela você usou embaixo?"),
]

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "longo_existente": "POBNoY16wG8",
    "longo": [],
    "short": SHORT,
    "thumb": {"l1": "Duas janelas", "l2": "numero falso"},
    "paleta": {"bg": "#0E1117", "ink": "#EEF1F5", "c1": "#3DDBD9",
               "c2": "#1E2430", "red": "#FF5A5F", "ok": "#3CCB7F",
               "panel": "#161B24", "mut": "#8B95A5", "acc": "#3DDBD9"},
    "copy": "",
}

aqui = os.path.dirname(os.path.abspath(__file__))
sp["copy"] = open(os.path.join(aqui, "copy_lab086s.txt"), encoding="utf-8").read()
alvo = os.path.join(RAIZ, "fabrica", "specs", PAC + ".json")
with open(alvo, "w", encoding="utf-8") as fh:
    json.dump(sp, fh, ensure_ascii=False, indent=1)
print("spec gravada:", alvo)
print("cenas:", len(SHORT), "| media de chars:",
      sum(len(c["nar"]) for c in SHORT) // len(SHORT))
print("esqueleto:", "-".join(c["layout"] for c in SHORT))
