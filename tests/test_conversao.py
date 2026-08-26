"""O teste que separa efeito de ruido, e o caso que quase me enganou.

Em 26/08/2026 eu olhei a frota inteira short a short — 79 shorts, 67 com zero
inscrito — e a primeira leitura foi que o aprendizado 482 estava lendo ruido.
Estava errado, e o erro foi de UNIDADE: por pacote o teste nao tem poder
nenhum, por grupo o mesmo dado da p = 0,00023. Os dois casos estao aqui para
que a proxima rodada nao repita nenhuma das duas leituras.
"""

import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import conversao as C  # noqa: E402


# Evidencia registrada no aprendizado 482, epomeno-epipedo.
METODO = [[204, 3], [30, 1]]
FATO = [[1444, 2], [1714, 2], [1888, 0]]


def test_o_482_passa_quando_medido_por_grupo():
    """21,6x com p exato de 0,00023 — o efeito e real e e grande."""
    vm, sm, tm = C.taxa(METODO)
    vf, sf, tf = C.taxa(FATO)
    assert (vm, sm) == (234, 4) and (vf, sf) == (5046, 4)
    assert 21.0 < tm / tf < 22.0
    p = C.p_exato(vm, sm, vf, sf)
    assert p < 0.001, p


def test_o_mesmo_dado_por_pacote_nao_diz_nada():
    """O pacote de 204 views sozinho contra o resto: nao separa.

    E o mesmo efeito de cima, olhado pela unidade errada. Serve para nao
    voltar a comparar porcentagem de um pacote com porcentagem de outro.
    """
    sozinho = [[204, 3]]
    resto = [[30, 1], [1444, 2], [1714, 2], [1888, 0]]
    vs, ss, _ = C.taxa(sozinho)
    vr, sr, _ = C.taxa(resto)
    p = C.p_exato(vs, ss, vr, sr)
    assert p > 0.001, p        # nao alcanca o que o agrupado alcanca


def test_zero_inscrito_e_falta_de_exposicao_e_o_modulo_diz_isso():
    """Com a taxa da frota, quase todo short da frota tem de dar zero."""
    frota = [[v, 0] for v in (5, 11, 19, 21, 25, 32, 41, 52, 63, 91)]
    base = 16 / 14657
    esperados = C.zeros_esperados(frota, base)
    assert esperados > len(frota) - 0.5   # praticamente todos, so por exposicao


def test_o_piso_de_exposicao_para_um_inscrito():
    """Um inscrito esperado pede ~916 views na taxa medida em 26/08/2026."""
    base = 16 / 14657
    assert 900 < 1 / base < 930


def test_quanto_maior_o_efeito_menos_exposicao_ele_pede():
    base = 16 / 14657
    ordem = [C.views_para_detectar(r, base) for r in (21.6, 5, 3, 2, 1.5)]
    assert ordem == sorted(ordem), ordem
    assert C.views_para_detectar(21.6, base) < 500
    # Separar duas formas BOAS (razao 2x) custa mais views do que a frota
    # inteira ja acumulou em short. E o motivo de nao tentar.
    assert C.views_para_detectar(2, base) > 14657


def test_razao_um_ou_menos_nao_e_detectavel():
    base = 16 / 14657
    assert C.views_para_detectar(1.0, base) == math.inf
    assert C.views_para_detectar(0.5, base) == math.inf


def test_compara_avisa_quando_nao_da_para_concluir():
    """Dois grupos pequenos e parecidos: o modulo tem de recusar a conclusao."""
    notas = C.compara({"a": [[100, 1]], "b": [[100, 0]]})
    junto = " | ".join(notas)
    assert "NAO distinguivel" in junto, junto
    assert "falta de exposicao" in junto, junto


def test_compara_confirma_quando_da():
    notas = C.compara({"metodo": METODO, "fato": FATO})
    junto = " | ".join(notas)
    assert "DISTINGUIVEL" in junto and "NAO distinguivel" not in junto, junto


def test_grupo_com_taxa_zero_nao_quebra_a_razao():
    notas = C.compara({"a": [[500, 3]], "b": [[500, 0]]})
    junto = " | ".join(notas)
    assert "a razao nao existe" in junto, junto


def test_precisa_de_dois_grupos():
    assert "exatamente dois grupos" in C.compara({"so_um": [[10, 1]]})[0]
