#!/usr/bin/env python3
"""Quantos pacotes a frota dispara AGORA, e o que falta em cada um dos outros.

Existe porque a pergunta "quantos pacotes estao prontos?" vinha sendo respondida
de cabeca, e a resposta mudava. Cada spec passa por quatro portoes, cada um com
um custo de descoberta diferente:

  identidade   `pacote` e `idioma` presentes e coerentes com config/canais/.
               Custo de descobrir tarde: o render escreve num diretorio e a
               entrega procura noutro; ou o video sobe marcado na lingua errada.
  copy         >= 2 secoes reconheciveis, tags dentro do orcamento de 480, e a
               descricao acima das 200 palavras que a rotina pede. Custo tarde:
               o publicar.py aborta DEPOIS do render.
  narracao     0 erros duros (planilha falada, slop). Custo tarde: o video sai
               com uma cena que ninguem consegue ouvir.
  layout       0 cenas com texto na borda. Custo tarde: 17 min de render e uma
               vaga de publicacao, medido no nivel-do-jogo-002.

O portao `copy` roda contra o `copy` da spec, nao contra o copy.md do render —
entao ele valida a ESTRUTURA e as tags, e nao os capitulos cronometrados, que so
existem depois dos clipes. E o suficiente para separar spec publicavel de spec
que vai abortar.

Uso:
    python3 fabrica/prontidao.py            # todas as specs
    python3 fabrica/prontidao.py <spec.json>
"""
from __future__ import annotations

import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

MIN_PALAVRAS_DESCRICAO = 200


def _gate_identidade(caminho, sp):
    from publicar import idioma_do_canal

    faltas = []
    nome = os.path.basename(caminho)[:-5]
    if sp.get("pacote") != nome:
        faltas.append(f"pacote={sp.get('pacote')!r} != {nome!r}")
    do_canal = idioma_do_canal(sp["slug"])
    if sp.get("idioma"):
        if do_canal and sp["idioma"] != do_canal:
            faltas.append(f"idioma={sp['idioma']!r} mas canal e {do_canal!r}")
    elif not do_canal:
        faltas.append("sem idioma na spec e sem config/canais/")
    return faltas


def _gate_copy(sp):
    """Le a copy da spec como o publicar.py leria, sem exigir o render."""
    import publicar as P

    bruto = sp.get("copy")
    if not isinstance(bruto, str) or len(bruto) < 200:
        return ["copy e bilhete, nao markdown — publicar.py aborta"]

    # ler_copy prefere o copy.md do workdir; aqui forcamos a spec passando um
    # diretorio que nao tem copy.md, e trocamos os placeholders por conteudo
    # plausivel para o _sem_placeholder nao reprovar o que o render preencheria.
    falso = dict(sp)
    falso["copy"] = bruto.replace("{CAPITULOS}", "0:00 abertura").replace(
        "{TRILHA}", "Music: Cipher2 by Kevin MacLeod"
    )
    try:
        cp = P.ler_copy(falso, os.path.join(RAIZ, "nao-existe"))
    except SystemExit as e:
        return [str(e)]

    faltas = []
    if not cp["titulo"] or len(cp["titulo"]) > 100:
        faltas.append(f"titulo com {len(cp['titulo'])} chars (limite 100)")
    palavras = len(cp["descricao"].split())
    if palavras < MIN_PALAVRAS_DESCRICAO:
        faltas.append(f"descricao com {palavras} palavras (minimo {MIN_PALAVRAS_DESCRICAO})")
    if not cp["tags"]:
        faltas.append("sem tags")
    else:
        mantidas, total = P.orcamento_tags(cp["tags"])
        if len(mantidas) < len(cp["tags"]):
            faltas.append(
                f"orcamento de tags corta {len(cp['tags']) - len(mantidas)} de "
                f"{len(cp['tags'])} ({total} chars)"
            )
    if not cp.get("hashtags"):
        faltas.append("sem hashtags")
    if not cp.get("comentario"):
        faltas.append("sem comentario fixado")
    return faltas


def _gate_narracao(caminho):
    import narracao

    sp = json.load(open(caminho, encoding="utf-8"))
    erros, _avisos, _todas = narracao.analisa(sp, narracao.idioma_de(sp, None))
    return erros


def _gate_layout(sp):
    import layout

    try:
        return layout.analisa(sp)
    except RuntimeError as e:
        # `usar_fonte` aborta quando a fonte do canal nao esta na maquina — o
        # agla-level pede Noto Sans Devanagari. Isso e defeito do AMBIENTE, nao
        # da spec, e reprovar a spec por isso esconderia o que ela tem de bom.
        # (O frota.yml instala fonts-noto-core, que traz Devanagari; medido em
        # 13/08/2026 — quatro familias apos o apt-get.)
        return [f"AMBIENTE, nao a spec: {e}"]


PORTOES = (
    ("identidade", lambda c, s: _gate_identidade(c, s)),
    ("copy", lambda c, s: _gate_copy(s)),
    ("narracao", lambda c, s: _gate_narracao(c)),
    ("layout", lambda c, s: _gate_layout(s)),
)


def avalia(caminho):
    sp = json.load(open(caminho, encoding="utf-8"))
    if not sp.get("longo"):
        return None
    return {nome: fn(caminho, sp) for nome, fn in PORTOES}


def main() -> int:
    alvos = sys.argv[1:] or sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs/*.json")))
    prontas, travadas = [], []

    for caminho in alvos:
        r = avalia(caminho)
        if r is None:
            continue
        nome = os.path.basename(caminho)[:-5]
        falhas = {g: f for g, f in r.items() if f}
        if falhas:
            travadas.append((nome, falhas))
        else:
            prontas.append(nome)

    print(f"PRONTAS ({len(prontas)}):")
    for n in prontas:
        print("   ", n)
    print(f"\nTRAVADAS ({len(travadas)}):")
    for n, falhas in travadas:
        print(f"    {n}")
        for portao, itens in falhas.items():
            print(f"        {portao}: {len(itens)} problema(s)")
            for i in itens[:3]:
                print(f"          - {i[:150]}")
            if len(itens) > 3:
                print(f"          ... e mais {len(itens) - 3}")

    total = len(prontas) + len(travadas)
    print(f"\n-> {len(prontas)}/{total} specs disparam a frota hoje")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
