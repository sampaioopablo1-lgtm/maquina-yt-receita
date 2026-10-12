"""A escolha entre as tres leituras, travada com os dados REAIS que a mediram.

Os numeros daqui nao sao inventados: sao as leituras de 08/10/2026 que
produziram o aprendizado 708, e a do `ZxHWcfDNovM` de 07/10 que produziu o 707.
Se alguem voltar a usar mediana, ou a cacar o maximo peca por peca, estes
testes caem.
"""

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import replica as R  # noqa: E402

# 08/10/2026, 08:08 — quatro pecas divergiram com a forma {alto, baixo, alto},
# e as outras dezesseis vieram identicas nas tres chamadas (708).
L1 = {"ZxHWcfDNovM": 833, "aT1y_jxUejM": 91, "cBBYHdP5JYA": 23, "JEnKrpgLJ0A": 22,
      "estavel": 500}
L2 = {"ZxHWcfDNovM": 830, "aT1y_jxUejM": 90, "cBBYHdP5JYA": 22, "JEnKrpgLJ0A": 21,
      "estavel": 500}
L3 = dict(L1)
OITO_OITO = [L1, L2, L3]


def test_grava_a_chamada_de_soma_maxima_e_nao_a_do_meio():
    """A leitura 2 caiu INTEIRA numa replica atrasada — ela nao pode ser escolhida."""
    assert R.chamada_para_gravar(OITO_OITO) == 0
    assert R.soma(L2) < R.soma(L1)


def test_o_piso_e_o_maximo_por_id_e_nao_a_mediana():
    """Com mediana, `ZxHWcfDNovM` sairia 833 por acaso aqui — mas em 07/10 as
    leituras foram 830, 833, 830 e a mediana devolveria 830, que foi o numero
    subestimado que o 707 pegou."""
    sete_zero_nove = [{"ZxHWcfDNovM": 830}, {"ZxHWcfDNovM": 833},
                      {"ZxHWcfDNovM": 830}]
    assert R.piso(sete_zero_nove)["ZxHWcfDNovM"] == 833
    assert R.chamada_para_gravar(sete_zero_nove) == 1


def test_a_faixa_acompanha_o_piso():
    assert R.faixa(OITO_OITO)["ZxHWcfDNovM"] == (830, 833)
    assert R.faixa(OITO_OITO)["estavel"] == (500, 500)


def test_so_os_divergentes_aparecem():
    assert set(R.divergentes(OITO_OITO)) == {
        "ZxHWcfDNovM", "aT1y_jxUejM", "cBBYHdP5JYA", "JEnKrpgLJ0A"}


def test_a_assinatura_do_708_e_a_mesma_forma_em_todos():
    """`833,830,833` e `91,90,91` tem a mesma forma — a replica e da CHAMADA."""
    assert R.mesma_forma(OITO_OITO)


def test_formas_que_discordam_derrubam_a_hipotese_da_chamada():
    """Se uma peca sobe onde outra desce, a divergencia NAO e da chamada.

    Aqui o relato tem de dizer isso em vez de gravar no automatico — e este
    teste existe para que a funcao nao devolva True por descuido.
    """
    a = [{"x": 10, "y": 5}, {"x": 9, "y": 6}, {"x": 10, "y": 5}]
    assert not R.mesma_forma(a)


def test_id_ausente_nao_vira_zero():
    """Ausencia e silencio, nao leitura de zero — zerar puxaria o piso."""
    a = [{"so_na_primeira": 7}, {}, {}]
    assert R.piso(a)["so_na_primeira"] == 7
    assert R.faixa(a)["so_na_primeira"] == (7, 7)


def test_sem_leitura_nenhuma_levanta_em_vez_de_adivinhar():
    with pytest.raises(ValueError):
        R.chamada_para_gravar([])


# ===========================================================================
# O PICO QUE NAO ERA REPLICA FRESCA — 12/10/2026, e refuta a LEITURA que eu
# fazia do 688 ("o maximo e um PISO").
# ===========================================================================

_RODADA_19H11 = [
    {"MjeP-_yDni4": 20, "O1PNIRYoeGY": 1, "xhPyfHdTwds": 2, "nUrSPWKHy8I": 114},
    {"MjeP-_yDni4": 24, "O1PNIRYoeGY": 7, "xhPyfHdTwds": 8, "nUrSPWKHy8I": 115},
    {"MjeP-_yDni4": 20, "O1PNIRYoeGY": 1, "xhPyfHdTwds": 2, "nUrSPWKHy8I": 114},
]
# A rodada seguinte, as 20:11, com as TRES chamadas de acordo nas quatro pecas
# menos a `nUrSPWKHy8I`, que subiu de verdade.
_RODADA_20H11 = {"MjeP-_yDni4": 20, "O1PNIRYoeGY": 1, "xhPyfHdTwds": 2,
                 "nUrSPWKHy8I": 122}


def test_a_chamada_de_soma_maxima_das_19h11_era_um_PICO_em_tres_pecas():
    # O procedimento do 708 manda gravar a chamada de soma maxima, e foi o que
    # eu fiz com este modulo. A rodada seguinte mostrou que ela gravou um pico
    # em tres das quatro pecas.
    assert R.chamada_para_gravar(_RODADA_19H11) == 1
    v = R.veredito_do_pico(_RODADA_19H11, _RODADA_20H11)
    assert v["MjeP-_yDni4"] == "pico"
    assert v["O1PNIRYoeGY"] == "pico"
    assert v["xhPyfHdTwds"] == "pico"
    # E na QUARTA ela era mesmo a replica fresca. A mesma chamada estava certa
    # para uma peca e errada para tres — e e por isso que nao se decide dentro
    # da rodada.
    assert v["nUrSPWKHy8I"] == "fresca"


def test_a_MODA_acertou_as_tres_que_o_MAXIMO_errou():
    m = R.moda(_RODADA_19H11)
    p = R.piso(_RODADA_19H11)
    for i in ("MjeP-_yDni4", "O1PNIRYoeGY", "xhPyfHdTwds"):
        assert m[i] == _RODADA_20H11[i], i      # a moda bateu com a verdade
        assert p[i] != _RODADA_20H11[i], i      # o maximo nao bateu


def test_o_caso_do_688_continua_dando_fresca():
    # No 688 as pecas subiram numa chamada E a subida PERSISTIU. O veredito
    # tem de dizer "fresca" ali, senao o modulo trocaria um erro pelo outro.
    rodada = [{"a": 830}, {"a": 833}, {"a": 830}]
    assert R.veredito_do_pico(rodada, {"a": 840}) == {"a": "fresca"}
    assert R.veredito_do_pico(rodada, {"a": 833}) == {"a": "fresca"}


def test_queda_para_entre_a_moda_e_o_maximo_sai_INDETERMINADO():
    rodada = [{"a": 10}, {"a": 20}, {"a": 10}]
    assert R.veredito_do_pico(rodada, {"a": 15}) == {"a": "indeterminado"}


def test_peca_ausente_na_rodada_seguinte_NAO_recebe_veredito():
    # Ausencia e silencio, nao zero — o mesmo principio do `piso`.
    rodada = [{"a": 10, "b": 1}, {"a": 20, "b": 1}, {"a": 10, "b": 1}]
    assert R.veredito_do_pico(rodada, {}) == {}


def test_moda_sem_maioria_cai_no_maximo_e_deixa_para_a_rodada_seguinte():
    assert R.moda([{"a": 1}, {"a": 2}, {"a": 3}]) == {"a": 3}


def test_moda_com_empate_de_frequencia_toma_o_maior():
    assert R.moda([{"a": 5}, {"a": 5}, {"a": 9}, {"a": 9}]) == {"a": 9}
