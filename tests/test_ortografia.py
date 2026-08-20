"""Acento faltando nao reprova em portao nenhum — e muda a pronuncia.

Descoberto em 20/08/2026 escrevendo a seviye-seviye-004: escrevi as 72 cenas em
ASCII num canal cujas outras duas specs acentuam 12,7% das letras. Turco sem
acento continua parecendo turco, entao passou no portao de idioma; ASCII sempre
tem fonte, entao passou no de glifos; e chegou ao TTS, que pronuncia outra
coisa — "acacagim" nao e "acacagim", "sozlesme" nao e "sozlesme".

A varredura achou mais tres casos JA NO AR: kolejny-poziom-003 e -004 em
polones, e seja-mais-magra-004 em portugues, publicada nesta mesma manha.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao as P  # noqa: E402

SPECS = RAIZ / "fabrica" / "specs"


def _sem_acento(texto: str) -> str:
    base = "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")
    # o `i` sem ponto e o `g` mole do turco, e o `l` cortado polones, nao sao
    # combinacoes: NFD nao os separa, e sem isto o teste nao simula ASCII real
    return base.replace("ı", "i").replace("ğ", "g").replace("ł", "l")


def _carrega(nome):
    return json.loads((SPECS / f"{nome}.json").read_text(encoding="utf-8"))


def test_o_caso_que_criou_o_portao():
    """seviye-seviye-004 com acento passa; a mesma spec em ASCII reprova."""
    sp = _carrega("seviye-seviye-004")
    caminho = str(SPECS / "seviye-seviye-004.json")
    assert P._gate_ortografia(caminho, sp) == []

    sem = json.loads(json.dumps(sp))
    for c in sem["longo"]:
        c["nar"] = _sem_acento(c["nar"])
    faltas = P._gate_ortografia(caminho, sem)
    assert faltas and "0.0%" in faltas[0] and "12.7%" in faltas[0]


def test_o_portao_compara_com_o_canal_e_nao_com_uma_regra_fixa():
    """Ele NAO afirma que toda lingua precisa de acento — o corpus nao sustenta
    isso: varias specs em portugues nunca acentuaram. Ele afirma que uma spec
    nao pode divergir do PROPRIO canal."""
    sp = _carrega("seviye-seviye-004")
    sp = json.loads(json.dumps(sp))
    sp["slug"] = "canal-sem-vizinhas"
    assert P._gate_ortografia(str(SPECS / "canal-sem-vizinhas-001.json"), sp) == []


def test_lingua_sem_diacritico_nao_e_avaliada():
    """Indonesio e ingles nao tem acento; o portao precisa se calar neles."""
    for nome in ("setiap-level-009", "next-level-money-004"):
        sp = _carrega(nome)
        assert P._gate_ortografia(str(SPECS / f"{nome}.json"), sp) == []


def test_escrita_nao_latina_fica_de_fora():
    """Grego e devanagari ja sao pegos pelo portao de idioma — la a falta de
    acento nem existe, o alfabeto inteiro seria outro."""
    assert "el" not in P.DIACRITICOS
    assert "hi" not in P.DIACRITICOS


def test_o_portao_esta_na_lista():
    """Escrever o portao e nao liga-lo e a forma silenciosa de nao ter portao."""
    assert "ortografia" in dict(P.PORTOES)


def test_a_folga_e_larga_de_proposito():
    """Metade da referencia: o alvo e ASCII puro, nao flutuacao normal de
    texto. Uma spec com 8% num canal de 12,7% nao pode reprovar."""
    sp = _carrega("seviye-seviye-004")
    d = P._densidade_diacritica(sp["longo"], P.DIACRITICOS["tr"])
    assert d > 0.10
    # simula uma spec com dois tercos do acento: tem de passar
    parcial = json.loads(json.dumps(sp))
    for i, c in enumerate(parcial["longo"]):
        if i % 3 == 0:
            c["nar"] = _sem_acento(c["nar"])
    assert P._gate_ortografia(str(SPECS / "seviye-seviye-004.json"), parcial) == []
