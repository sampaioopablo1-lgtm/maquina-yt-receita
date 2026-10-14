"""A conferencia da MIRA e o REAL dentro da mira nao cabem na mesma faixa — 740.

Aritmetica, nao opiniao. O `mira.py` confere a PREVISAO contra a mira do canal
(20,0 a 26,0 no labtreinamento) nos DOIS mundos de provedor. O 739 mediu que o
REAL fica 0,9 a 2,4 s ACIMA da previsao de quem narra. Com a razao piper/edge
que as specs de dez cenas deste canal produzem (~0,82):

  * para a PREVISAO passar:  piper >= 20,0  e  edge <= 26,0  ->  edge em [24,33; 26,00]
  * para o REAL cair dentro: edge <= 26,0-2,4 = 23,60  e  piper >= 20,0-0,9 = 19,10
                                                        ->  edge em [23,23; 23,60]

As duas janelas NAO se tocam -- vao de 0,73 s. Logo mira verde NAO significa real
dentro, e nenhuma spec satisfaz as duas ao mesmo tempo.

NAO resolvido de proposito: as duas saidas mexem em parametro de producao (a
mira, ou o que o instrumento confere), e a trava da secao 10 e explicita. O teste
existe para que a contradicao nao volte a ficar invisivel -- e para FALHAR se
alguem mexer num dos numeros sem reler o 740.
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
import mira  # noqa: E402

SPEC = RAIZ / "fabrica/specs/labtreinamento-s035.json"


def _janelas():
    spec = json.loads(SPEC.read_text())
    pv = mira.previsoes(spec)
    razao = pv["piper"] / pv["edge"]
    piso, teto = ensaio.alvo_short("labtreinamento")
    lo, hi = mira.RESIDUO_OBSERVADO
    return (piso / razao, teto), ((piso - lo) / razao, teto - hi), razao


def test_a_razao_piper_edge_deste_canal_e_de_ordem_0_82():
    *_, razao = _janelas()
    assert 0.80 <= razao <= 0.84, razao


def test_as_duas_janelas_NAO_se_tocam():
    (a_lo, a_hi), (b_lo, b_hi), _ = _janelas()
    assert a_lo > b_hi, (
        f"janela da mira [{a_lo:.2f}, {a_hi:.2f}] e do real "
        f"[{b_lo:.2f}, {b_hi:.2f}] passaram a se tocar — releia o 740, pode ser "
        "que a mira ou a banda tenham mudado com motivo"
    )


def test_o_vao_medido_e_de_ordem_0_7_s():
    (a_lo, _), (_, b_hi), _ = _janelas()
    assert 0.5 < a_lo - b_hi < 1.0, a_lo - b_hi


def test_a_peca_escolhida_fica_na_janela_da_MIRA_e_isso_vai_dito():
    spec = json.loads(SPEC.read_text())
    r = mira.confere(spec)
    assert not r["fora"], "a escolha foi manter a mira verde"
    teto = r["mira"][1]
    # e o real pelo edge PODE passar do teto — a copy diz isso
    assert mira.faixa_real(r["previsoes"]["edge"])[1] > teto
    # enquanto pelo piper cabe
    assert mira.faixa_real(r["previsoes"]["piper"])[1] <= teto
    assert "INTERSECCAO VAZIA" in spec["copy"] or "interseccao VAZIA" in spec["copy"] \
        or "INTERSECCAO\nVAZIA" in spec["copy"] or "VAZIA" in spec["copy"]


def test_a_mira_do_canal_nao_foi_mexida_nesta_rodada():
    assert ensaio.alvo_short("labtreinamento") == (20.0, 26.0)


def test_a_banda_do_739_nao_foi_mexida_nesta_rodada():
    assert mira.RESIDUO_OBSERVADO == (0.9, 2.4)
    # 741 somou um ponto DENTRO da banda: n sobe, os LIMITES nao.
    assert mira.RESIDUO_N == 8
