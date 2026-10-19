# -*- coding: utf-8 -*-
"""O trilho e os cinco layouts de longo nao passavam no portao `layout`.

MEDIDO EM 19/10 AS 12:3x, na PRIMEIRA spec de longo que os declarou. Eu havia
relatado em tres rodadas seguidas que eles "deixaram de ser promessa" — as 04:2x
(dois layouts), as 07:2x (os outros tres), as 08:1x (o trilho ligado ao render) e
as 09:2x (o trilho alimentado pela spec). Em nenhuma delas eu rodei o portao
sobre uma peca, porque nao havia peca. Quando houve:

    com a geometria de quadro cheio : 64 cenas reprovadas de 64
    so o trilho, sem os layouts     : 64 reprovadas (1,44% de tinta na borda)
    so os layouts, sem o trilho     :  7 reprovadas (comparar 20,64%)
    depois do conserto              :  0

**A CAUSA E DE ENQUADRAMENTO — o 679/698/725 em geometria.** O trilho tem a
posicao MEDIDA por variancia temporal no longo do dono, e aquele video tem ZERO
zoom; o nosso render aplica Ken Burns em toda cena e corta a borda antes de
mostrar. Transplantei uma posicao medida num quadro que nao se move para um
render que se move.

**E O PORTAO ESTA CERTO.** Ele existe porque o `kp-plan-9233` foi pego com 6/6
quadros com tinta na borda. Afrouxar `MARGEM_VISUAL` para a peca caber seria
limiar sem procedencia (§10) e, pior, afrouxar o portao para salvar a peca.

O conserto e `fabrica/area_segura.py`: a janela deixa de ser numero escrito em
dois lugares e passa a ser LIDA do proprio portao — era dois donos da mesma
regra, igual ao que congelou a legenda e parou a mira de conferir.
"""
import ast
import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import area_segura as AS  # noqa: E402
import canal  # noqa: E402
import layout as LA  # noqa: E402
import layouts_longo as LL  # noqa: E402
import prontidao as P  # noqa: E402
import trilho  # noqa: E402

W, H = 1920.0, 1080.0
PAL = {"bg": "#F4EFE6", "ink": "#1B1A17", "c1": "#C8502A", "c2": "#2B6CB0",
       "panel": "#FFFFFF", "mut": "#7A7263", "acc": "#C8502A", "red": "#B83227",
       "ok": "#2E8B57"}


def _specs_de_longo_com_trilho():
    """As specs do disco que declaram o campo `trilho` — DERIVADO do disco."""
    saida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            sp = json.load(open(f))
        except Exception:
            continue
        longo = sp.get("longo") or []
        if longo and any((c or {}).get("trilho") for c in longo):
            saida.append((os.path.basename(f)[:-5], sp))
    return saida


# ----- 1. a janela sai do PORTAO, nao de um numero meu -----

def test_a_janela_e_LIDA_do_portao():
    x0, x1 = AS.janela()
    assert x0 == pytest.approx(LA.faixa_de_risco() + AS.FOLGA)
    assert x1 == pytest.approx(1.0 - x0)
    assert 0.0 < x0 < 0.5, (x0, "janela degenerada nao mede nada")


def test_ninguem_RECOPIA_a_margem_do_portao():
    """Por AST: a fracao do portao nao reaparece cravada em modulo nenhum.

    E a varredura que impede o defeito voltar: foi numero escrito em dois
    lugares que produziu isto.
    """
    proibidos = {round(LA.MARGEM_VISUAL, 6),
                 round(LA.faixa_de_risco(), 6),
                 round(LA.faixa_de_risco() + AS.FOLGA, 6)}
    suspeitos = []
    for f in glob.glob(os.path.join(RAIZ, "fabrica", "*.py")):
        # `visual.py` e o DONO da faixa de 4% (mediu em 17/08) e o
        # `layout.py` passou a le-la dele em 19/10 as 13:0x — foi esta
        # varredura que achou os dois na primeira execucao.
        if os.path.basename(f) in ("layout.py", "area_segura.py",
                                   "visual.py"):
            continue
        for no in ast.walk(ast.parse(open(f).read())):
            if isinstance(no, ast.Constant) and isinstance(no.value, float):
                if round(no.value, 6) in proibidos:
                    suspeitos.append((os.path.basename(f), no.value))
    assert not suspeitos, (
        f"a margem do portao reaparece fora dele: {suspeitos}. "
        "Dois donos da mesma regra e exatamente o defeito que isto conserta."
    )


# ----- 2. o trilho, dentro da janela -----

def test_a_faixa_do_trilho_fica_DENTRO_da_janela():
    x0, x1 = AS.janela()
    assert trilho.faixa_y0() >= x0 - 1e-9, "a faixa comeca na area proibida"
    assert trilho.faixa_y1() <= x1 + 1e-9, "a faixa termina na area proibida"
    assert trilho.margem_x() >= x0 - 1e-9, "o recuo lateral invade a borda"


def test_a_ALTURA_medida_sobreviveu_e_a_posicao_e_nossa():
    """O que atravessa do video dele e a ALTURA; a posicao e derivada daqui."""
    assert trilho.FAIXA_ALT == pytest.approx(trilho.REF_Y1 - trilho.REF_Y0)
    assert trilho.faixa_y1() - trilho.faixa_y0() == pytest.approx(
        trilho.FAIXA_ALT)
    # e a posicao NAO e mais a dele
    assert trilho.faixa_y0() > trilho.REF_Y0, (
        "a faixa voltou para a posicao do video dele, que o portao reprova"
    )
    fonte = open(os.path.join(RAIZ, "fabrica", "trilho.py")).read()
    assert "RETRATACAO" in fonte and "area_segura" in fonte, (
        "o motivo saiu do modulo — conserto sem motivo escrito volta calado"
    )


# ----- 3. o portao, sobre peca de verdade -----

def test_a_spec_de_longo_do_disco_passa_no_portao_de_LAYOUT():
    specs = _specs_de_longo_com_trilho()
    assert specs, (
        "nenhuma spec do disco declara `trilho` — sem peca este arquivo passa "
        "por vacuidade, que e exatamente como o defeito durou tres rodadas"
    )
    for pacote, sp in specs:
        problemas = P._gate_layout(sp)
        assert not problemas, f"{pacote}: {len(problemas)} -> {problemas[:2]}"


def test_CONTRAPROVA_sem_o_mapeamento_o_portao_reprova():
    """Desligado o conserto, o portao volta a reprovar — nos dois pedacos."""
    specs = _specs_de_longo_com_trilho()
    assert specs, "sem spec nao ha contraprova"
    _, sp = specs[0]

    x0, esc = LL._x, LL._esc_geo
    try:
        LL._GEO.clear()
        LL._x = lambda f: float(f)
        LL._esc_geo = lambda f: float(f)
        assert P._gate_layout(sp), (
            "com a geometria de quadro cheio o portao PASSOU — ou ele deixou "
            "de medir a borda, ou o conserto nao era necessario"
        )
    finally:
        LL._x, LL._esc_geo = x0, esc
        LL._GEO.clear()
    assert not P._gate_layout(sp), "o conserto nao voltou"


def test_os_CINCO_layouts_sao_exercitados_pela_varredura():
    """Sai de `LAYOUTS`: layout novo entra na cobertura sozinho."""
    falta = []
    for nome in sorted(LL.LAYOUTS):
        g = LL.geo(nome.upper()) if nome.upper() in dir(LL) else None
        if g is None:
            falta.append(nome)
            continue
        for chave, valor in g.items():
            if LL._e_posicao(chave):
                assert AS.janela()[0] - 1e-9 <= valor <= AS.janela()[1] + 1e-9, (
                    f"{nome}.{chave} = {valor} fora da janela segura")
    assert not falta, f"layout sem dict de geometria: {falta}"


# ----- 4. a quarta forma de slug -----

def test_o_canal_sai_do_pacote_na_convencao_de_LONGO():
    """`<canal>-NNN` e a quarta forma, e foi ela que cegou a mira hoje."""
    assert canal.do_pacote("epomeno-epipedo-068") == "epomeno-epipedo"
    assert canal.do_pacote("labtreinamento-s083") == "labtreinamento"
    assert canal.do_pacote("labtreinamento") == "labtreinamento"
    # pacote com data, do docstring do `kolejny-poziom-s017`
    assert canal.do_pacote("kp-plan-9233-20260811") == "kp-plan-9233"


def test_os_prefixos_do_DISCO_nao_terminam_em_digito():
    """O que torna a regra do sufixo segura, e isso e MEDIDO e nao suposto.

    Se um canal novo terminar em digito, `do_pacote` passa a corta-lo errado —
    e este teste reprova antes de o erro chegar a producao.
    """
    import re
    nomes = [os.path.basename(p)[:-5]
             for p in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))]
    assert len(nomes) > 300, f"varredura encolheu para {len(nomes)}"
    prefixos = {re.sub(r"-s?\d+$", "", n) for n in nomes}
    maus = sorted(p for p in prefixos if p and p[-1].isdigit())
    assert not maus, (
        f"prefixo terminando em digito: {maus}. A regra do sufixo em "
        "`canal.do_pacote` passa a cortar o nome do canal, e o limite esta "
        "declarado no proprio modulo."
    )


def test_a_mira_acha_o_canal_de_um_PACOTE():
    """Contraprova no outro sentido: canal sem mira continua sem mira."""
    import mira
    specs = _specs_de_longo_com_trilho()
    assert specs, "sem spec de longo nao ha o que conferir"
    for pacote, sp in specs:
        r = mira.relato(os.path.join(RAIZ, "fabrica", "specs", pacote + ".json"))
        assert pacote not in r.split("(")[1].split(")")[0], (
            f"{pacote}: a mira imprimiu o PACOTE onde vai o canal — "
            "e o defeito de 05:2x, na forma do longo"
        )
