"""Capítulo desenhado que o render não produz some calado.

`copy_md.capitulos` só trata como abertura de seção uma cena de layout `titulo`
ou `broll`. A heurística existe por um bom motivo: `cap` é usado SOLTO no acervo
antigo — a cocina-por-niveles-002 tem 69 cenas com `cap` — e honrar todos viraria
capítulo a cada minuto.

O caso novo é o oposto. Nas specs escritas com os ajudantes T/I/L/B/C o `cap`
aparece uma vez por capítulo e é marcador de autor. Quando um deles abre com
layout `item`, o render descarta: a seviye-seviye-004 desenhou 7 e publicou 6.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao as P  # noqa: E402

SPECS = RAIZ / "fabrica" / "specs"


def _carrega(nome):
    return json.loads((SPECS / f"{nome}.json").read_text(encoding="utf-8"))


def test_o_caso_que_criou_o_portao():
    sp = _carrega("seviye-seviye-004")
    faltas = P._gate_capitulos(sp)
    assert faltas and "7 capitulos desenhados e 6 produzidos" in faltas[0]


def test_a_falta_aponta_qual_capitulo_some():
    """Reprovar sem dizer QUAL capítulo obriga a conferir os setenta e dois."""
    sp = _carrega("seviye-seviye-004")
    assert "Altı aylık cep" in P._gate_capitulos(sp)[0]


def test_trocar_o_layout_para_titulo_resolve():
    sp = _carrega("seviye-seviye-004")
    sp = json.loads(json.dumps(sp))
    for c in sp["longo"]:
        if c.get("cap") and c.get("layout") not in ("titulo", "broll"):
            c["layout"] = "titulo"
            c["sub"] = c.pop("preco", "")
    assert P._gate_capitulos(sp) == []


def test_o_portao_se_cala_onde_cap_e_decoracao():
    """No acervo antigo `cap` aparece dezenas de vezes e não marca capítulo.
    Opinar ali quebraria specs que a heurística de layout já resolve bem."""
    sp = _carrega("cocina-por-niveles-002")
    assert sum(1 for c in sp["longo"] if c.get("cap")) > 8
    assert P._gate_capitulos(sp) == []


def test_o_portao_se_cala_sem_voz_medida():
    sp = _carrega("seviye-seviye-004")
    sp = json.loads(json.dumps(sp))
    sp["voz"] = "xx-XX-NinguemNeural"
    assert P._gate_capitulos(sp) == []


def test_o_portao_esta_na_lista():
    assert "capitulos" in dict(P.PORTOES)
