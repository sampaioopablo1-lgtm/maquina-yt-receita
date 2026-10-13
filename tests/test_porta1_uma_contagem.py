"""Uma contagem de delta NAO resolve ritmo -- e vale nos DOIS sentidos.

Medido em 13/10/2026 as 09:1x, em producao. A leitura ao vivo deu
labtreinamento 68 -> 67 numa janela de 13,6 h, cujo piso de resolucao e
1,76/dia. O `porta1.quadro` chamou isso de ritmo resolvido de -1,76/dia e
projetou "chega NUNCA".

O criterio antigo era `agora != antes`: delta ZERO nao resolvia, delta de UMA
contagem resolvia. A assimetria nao tem justificativa -- o piso da janela E uma
contagem, logo |ritmo| == piso e a incerteza e da ordem do proprio valor. Este e
o MESMO argumento que ja estava escrito no CLAUDE.md para o +0,60/dia do
labtreinamento, e que eu nao havia aplicado ao codigo.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import porta1  # noqa: E402


def _linha(q, canal):
    return next(l for l in q["canais"] if l["canal"] == canal)


def test_o_caso_REAL_de_13_10_uma_contagem_PARA_BAIXO_nao_resolve():
    q = porta1.quadro({"labtreinamento": {"antes": 68, "agora": 67}}, horas=13.6)
    l = _linha(q, "labtreinamento")
    assert l["delta"] == -1
    assert l["ritmo_resolvido"] is False, (
        "uma contagem para baixo numa janela cujo piso E uma contagem nao "
        "mede ritmo -- foi assim que saiu 'chega NUNCA' em producao")


def test_uma_contagem_PARA_CIMA_tambem_nao_resolve():
    q = porta1.quadro({"x": {"antes": 67, "agora": 68}}, horas=13.6)
    assert _linha(q, "x")["ritmo_resolvido"] is False


def test_delta_zero_continua_nao_resolvendo():
    q = porta1.quadro({"x": {"antes": 19, "agora": 19}}, horas=13.6)
    assert _linha(q, "x")["ritmo_resolvido"] is False


def test_DUAS_contagens_resolvem_porque_saem_do_piso():
    q = porta1.quadro({"x": {"antes": 19, "agora": 21}}, horas=13.6)
    l = _linha(q, "x")
    assert l["ritmo_resolvido"] is True
    assert l["por_dia"] > porta1.piso_de_resolucao(13.6)


def test_nao_resolvido_NUNCA_imprime_a_palavra_nunca_naquela_linha():
    r = porta1.relato(porta1.quadro(
        {"labtreinamento": {"antes": 68, "agora": 67}}, horas=13.6))
    linha = next(x for x in r.splitlines() if "labtreinamento" in x)
    assert "nunca" not in linha
    assert "indet." in linha


def test_a_leitura_de_40_3_h_que_FUNCIONOU_continua_funcionando():
    # 68 contra 67 em 40,3 h tem piso 0,60/dia e delta de uma contagem --
    # tambem nao resolve. O que resolveu em 12/10 foi o epomeno, com +2.
    q = porta1.quadro({"epomeno-epipedo": {"antes": 17, "agora": 19}}, horas=40.3)
    assert _linha(q, "epomeno-epipedo")["ritmo_resolvido"] is True


def test_o_criterio_e_DUAS_contagens_e_nao_um_limiar_inventado():
    fonte = open(os.path.join(os.path.dirname(__file__), "..",
                              "fabrica", "porta1.py")).read()
    assert "abs(v[\"agora\"] - v[\"antes\"]) >= 2" in fonte, (
        "o criterio tem de ser contagem, nao um ritmo/dia cravado que envelhece")
