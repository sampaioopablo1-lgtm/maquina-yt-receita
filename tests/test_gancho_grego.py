"""O portao do gancho precisa saber que em grego a pergunta fecha com ";".

O grego nao usa "?". O ponto de interrogacao grego e ";" (U+003B), com o
codepoint dedicado U+037E canonicamente equivalente. Enquanto o portao so
aceitava "?", ele era IMPOSSIVEL de passar em grego: a ponte escrita certa
levava aviso e a escrita errada tambem, o que e o mesmo que nao ter portao.

Medido em 19/08/2026: 5 avisos no epomeno-epipedo-004 e 5 no 005, todos em
cenas que JA terminavam em pergunta. O 004 foi ao ar com o aviso ignorado —
que e exatamente o que um portao que grita sempre ensina a fazer.

O outro lado importa igual: ponto e virgula em portugues, ingles ou polones
NAO fecha pergunta, e aceitar ";' para todo mundo trocaria um portao cego
por um portao permissivo.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao  # noqa: E402


def _spec(fecho, idi="el"):
    """Duas cenas: a primeira e ponte, a segunda abre capitulo."""
    return {"longo": [
        {"layout": "titulo", "kicker": "ponte", "sub": "s",
         "nar": f"Μια πρόταση. Και τώρα η ερώτηση{fecho}", "sem_cap": True},
        {"layout": "titulo", "kicker": "abre", "sub": "s",
         "cap": "Κεφάλαιο δύο", "nar": "Δεύτερο κεφάλαιο."},
    ]}


def _avisos_de_gancho(sp, idi):
    _, avisos, _ = narracao.analisa(sp, idi)
    return [a for a in avisos if "ponto final morto" in a]


def test_grego_aceita_ponto_e_virgula_como_pergunta():
    assert _avisos_de_gancho(_spec(";"), "el") == []


def test_grego_aceita_o_codepoint_dedicado():
    assert _avisos_de_gancho(_spec(";"), "el") == []


def test_grego_aceita_a_interrogacao_latina_tambem():
    """Roteiro antigo escrito com '?' nao pode passar a falhar."""
    assert _avisos_de_gancho(_spec("?"), "el") == []


def test_grego_ainda_reprova_ponto_final():
    assert _avisos_de_gancho(_spec("."), "el") != []


def test_ponto_e_virgula_NAO_vale_gancho_fora_do_grego():
    """Em pt/en/pl ';' e ponto e virgula, nao pergunta."""
    for idi in ("pt", "en", "pl"):
        sp = {"longo": [
            {"layout": "titulo", "kicker": "p", "sub": "s",
             "nar": "Uma frase; e outra;", "sem_cap": True},
            {"layout": "titulo", "kicker": "a", "sub": "s",
             "cap": "Capitulo dois", "nar": "Segundo capitulo."},
        ]}
        assert _avisos_de_gancho(sp, idi) != [], f"{idi} aceitou ';' como gancho"


def test_as_pontes_do_005_passam_limpas():
    """O pacote que motivou o conserto, cercado por inteiro."""
    import json

    sp = json.load(open(RAIZ / "fabrica/specs/epomeno-epipedo-005.json",
                        encoding="utf-8"))
    erros, avisos, _ = narracao.analisa(sp, "el")
    assert erros == [], erros
    assert avisos == [], avisos
