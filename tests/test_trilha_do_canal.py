"""A trilha e do CANAL, e o portao precisa saber disso ANTES do render.

Em 19/08/2026 o kolejny-poziom-005 foi ao ar com Deliberate_Thought num
canal cuja identidade sonora e Wholesome. Os SETE portoes passaram, porque
nenhum lia a trilha do canal: ela existia so em `canais.trilha`, no banco, e
os portoes rodam offline.

O unico que pegou foi um teste de repositorio que compara specs do mesmo
canal entre si — e ele so pode pegar DEPOIS de existir uma segunda spec para
divergir da primeira. Num canal com uma spec so, o erro passaria inteiro.

Conserto em duas partes: a identidade passa a ser versionada em
config/canais/<slug>.yaml, junto das specs que precisam obedece-la, e o
portao de identidade a confere.
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import orquestra as O  # noqa: E402
from publicar import trilha_do_canal_config  # noqa: E402

CONFIGS = sorted((RAIZ / "config" / "canais").glob("*.yaml"))


def test_todo_canal_declara_trilha():
    """Sem a linha no yaml o portao fica cego de novo, e em silencio."""
    sem = [p.stem for p in CONFIGS
           if p.stem != "default" and not trilha_do_canal_config(p.stem)]
    assert not sem, f"canais sem trilha em config/canais/: {sem}"


def test_a_trilha_declarada_existe_no_portfolio():
    import copy_md

    for p in CONFIGS:
        if p.stem == "default":
            continue
        faixa = trilha_do_canal_config(p.stem)
        if faixa:
            assert faixa in copy_md.TRILHAS_VALIDAS, \
                f"{p.stem} declara {faixa!r}, fora do portfolio"


def test_spec_com_trilha_errada_reprova():
    sp = json.loads((RAIZ / "fabrica/specs/kolejny-poziom-006.json")
                    .read_text(encoding="utf-8"))
    sp["trilha"] = "Deliberate_Thought"
    faltas = O._falhas_baratas("kolejny-poziom-006", sp)
    assert any("trilha" in f for f in faltas), faltas


def test_spec_com_trilha_certa_passa():
    sp = json.loads((RAIZ / "fabrica/specs/kolejny-poziom-006.json")
                    .read_text(encoding="utf-8"))
    assert not O._falhas_baratas("kolejny-poziom-006", sp)


def test_toda_spec_do_repo_bate_com_a_identidade_do_canal():
    """A varredura: o erro do 005 nao pode existir em nenhuma outra spec."""
    erradas = []
    for p in sorted((RAIZ / "fabrica" / "specs").glob("*.json")):
        sp = json.loads(p.read_text(encoding="utf-8"))
        slug, faixa = sp.get("slug"), sp.get("trilha")
        do_canal = trilha_do_canal_config(slug) if slug else ""
        if faixa and do_canal and faixa != do_canal:
            erradas.append(f"{p.stem}: {faixa} != {do_canal}")
    assert not erradas, "specs com trilha fora da identidade: " + "; ".join(erradas)
