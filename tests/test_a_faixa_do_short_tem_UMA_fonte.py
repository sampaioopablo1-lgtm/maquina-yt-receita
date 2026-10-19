# -*- coding: utf-8 -*-
"""A faixa de duracao do short se le de UM lugar — medido pelo run que morreu.

Em 16/10/2026 eu abri a faixa no portao `duracao` do `prontidao` para a peca de
2 min que o dono pediu, os doze portoes passaram, e o run `38847013520` montou o
`short.mp4` de **123,6 s** e MORREU no fim, num `assert 20 <= ds <= 60` cravado a
mao no `etapas.py` — o MESMO limite escrito uma segunda vez. O vídeo existia, o
artefato subiu, e a regra reprovou o que a regra havia aprovado.

Estes testes travam as duas propriedades que o conserto precisa ter.
"""
import ast
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
import prontidao  # noqa: E402


def test_sem_o_campo_a_faixa_e_a_da_frota():
    """Contraprova: spec antiga nao muda de julgamento."""
    assert ensaio.faixa_do_short({}) == (18.0, 45.0)
    assert ensaio.faixa_do_short({"short_alvo_s": None}) == (18.0, 45.0)


def test_com_o_campo_vale_o_da_spec():
    assert ensaio.faixa_do_short({"short_alvo_s": [95, 135]}) == (95.0, 135.0)


def test_o_prontidao_DELEGA_em_vez_de_ter_a_propria_copia():
    """O portao nao pode recalcular a faixa — foi assim que nasceu o defeito."""
    assert prontidao._faixa_do_short({"short_alvo_s": [95, 135]}) == (95.0, 135.0)
    fonte = (RAIZ / "fabrica" / "prontidao.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    alvo = next(n for n in ast.walk(arvore)
                if isinstance(n, ast.FunctionDef) and n.name == "_faixa_do_short")
    corpo = ast.unparse(alvo)
    assert "faixa_do_short" in corpo, "o portao tem de chamar a fonte unica"
    assert "18" not in corpo and "45" not in corpo, (
        "o portao voltou a cravar numero: a faixa mora em ensaio.faixa_do_short")


def test_o_etapas_NAO_tem_mais_o_limite_cravado():
    """O assert do render le a faixa da spec, nao um par de numeros escrito."""
    fonte = (RAIZ / "fabrica" / "etapas.py").read_text(encoding="utf-8")
    # Pela AST, nao por texto. Este teste reprovou em 19/10 contra um COMENTARIO
    # que CITAVA o limite para explicar de onde veio o defeito da legenda: casar
    # prosa pega a explicacao em vez do codigo, e ai o conserto fica sem poder
    # ser explicado no lugar. Mesma licao do teste do `estado_ponte`.
    for no in ast.walk(ast.parse(fonte)):
        if not isinstance(no, ast.Assert):
            continue
        teste = no.test
        if not isinstance(teste, ast.Compare):
            continue
        nums = [x.value for x in [teste.left, *teste.comparators]
                if isinstance(x, ast.Constant) and isinstance(x.value, (int, float))]
        assert not (20 in nums and 60 in nums), (
            "o limite cravado voltou ao etapas.py — e ele roda DEPOIS de montar "
            "o arquivo, entao mata o run com o video pronto")
    assert "faixa_do_short(sp)" in fonte, (
        "o etapas.py tem de ler a faixa da mesma fonte que o portao")


def test_o_teto_do_formato_shorts_nao_se_negocia():
    """180 s: acima disso a peca deixa de ser Short, e o caminho dos 3 M morre."""
    assert ensaio.TETO_FORMATO_SHORT_S == 180
    for ruim in ([95, 200], [10, 181]):
        try:
            ensaio.faixa_do_short({"short_alvo_s": ruim})
        except ValueError:
            continue
        raise AssertionError(f"{ruim} passou, e nao deveria")


def test_faixa_mal_formada_levanta_em_vez_de_passar_calada():
    for ruim in ([135, 95], [0, 45], "120", [50]):
        try:
            ensaio.faixa_do_short({"short_alvo_s": ruim})
        except (ValueError, IndexError, TypeError):
            continue
        raise AssertionError(f"{ruim!r} passou calado")


def test_a_peca_de_2_min_cabe_na_tolerancia_do_render():
    """O real medido (123,6 s) tem de passar o assert do render com [95,135].

    Este e o numero REAL do run que morreu, lido por ffprobe no arquivo
    montado — nao uma previsao.
    """
    piso, teto = ensaio.faixa_do_short({"short_alvo_s": [95, 135]})
    assert piso / 1.5 <= 123.6 <= teto * 1.34
