"""A conferencia da MIRA e o REAL dentro da mira nao cabem na mesma faixa — 740.

Aritmetica, nao opiniao. O `mira.py` confere a PREVISAO contra a mira do canal
(20,0 a 26,0 no labtreinamento) nos DOIS mundos de provedor. O 739 mediu que o
REAL fica 0,9 a 3,7 s ACIMA da previsao de quem narra (teto ampliado pelo 752). Com a razao piper/edge
que as specs de dez cenas deste canal produzem (~0,82):

  * para a PREVISAO passar:  piper >= 20,0  e  edge <= 26,0  ->  edge em [24,33; 26,00]
  * para o REAL cair dentro: edge <= 26,0-3,7 = 22,30  e  piper >= 20,0-0,9 = 19,10
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


def test_o_vao_medido_ABRIU_com_o_752():
    """O vao era de 0,73 s com a banda de 2,4; com 3,7 ele passou a ~2,0 s.

    Isto e PIOR, nao melhor: quanto maior o vao, mais longe esta de existir uma
    spec que satisfaca a previsao na mira E o real na mira. E mata a saida que o
    751 parecia abrir, porque real <= 26,0 passou a exigir edge <= 22,3, onde o
    piper cai para ~18,3 — bem abaixo do piso de 20,0.
    """
    (a_lo, _), (_, b_hi), _ = _janelas()
    vao = a_lo - b_hi
    assert 1.5 < vao < 2.5, vao
    assert vao > 0.73, "se o vao ENCOLHER, releia o 752 antes de comemorar"


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


def test_a_banda_e_a_OBSERVADA_e_o_teto_dela_foi_AMPLIADO_pelo_752():
    """O teto da banda nao e limiar: ele e o maior residuo JA OBSERVADO.

    De 739 a 751 ele foi 2,4 por treze pontos. O `s043` mediu 3,7 e o teto subiu
    no mesmo passo — e isso e reportar medicao, nao inventar criterio. O piso de
    0,9 segue intocado, e a largura passou de 1,5 para 2,8 s, o que torna a banda
    MENOS util como previsao; vai dito em vez de escondido.
    """
    assert mira.RESIDUO_OBSERVADO == (0.9, 3.7)
    assert mira.RESIDUO_N == 22


def test_a_pinca_fecha_por_RAZAO_contra_OFFSET_e_nao_por_numero_de_cenas():
    """748, medido em 14/10 as 05:1x, e e a forma FINAL da contradicao do 740.

    O `labtreinamento-s040` saiu com edge 23,5 / piper **19,3** na primeira
    versao -- FORA da mira pelo PISO, o lado que eu nunca havia tocado. Alongado
    para edge 24,7 / piper 20,3, o real deu **27**, igual ao do `s039`, que tinha
    a MESMA previsao de 24,7.

    E a conta que fecha o caso: o piso do piper e uma RAZAO (piper ~ 0,82 x edge),
    e o teto do real e um OFFSET (real ~ edge + 0,9 a 3,7). Entao

        piper >= 20,0  <=>  edge >= 24,4
        real  <= 26,0  <=>  edge <= 26,0 - 2,3 = 23,7

    e as duas faixas **nao se tocam, qualquer que seja o numero de cenas** --
    porque mudar cenas mexe na sobrecarga, nao na RAZAO entre os dois mundos.
    Logo nao existe spec deste canal que satisfaca as duas: as saidas sao as que
    ja estao na fila do dono (mover a mira, ou parar de cobrar REAL no estimado).
    """
    import ensaio

    piso, teto = ensaio.alvo_short("labtreinamento")
    razao = 0.82          # piper/edge, medido
    residuo_max = 3.7     # banda do 739, com o teto ampliado pelo 752
    residuo_min = 0.9

    edge_min_por_piper = piso / razao                  # 24,39
    edge_max_por_real = teto - residuo_min             # 25,10 (otimista)
    edge_max_por_real_pessimista = teto - residuo_max  # 22,30 depois do 752

    assert round(edge_min_por_piper, 1) == 24.4
    assert round(edge_max_por_real_pessimista, 1) == 22.3
    # no caso PESSIMISTA (o que de fato aconteceu duas vezes) nao ha intersecao:
    assert edge_min_por_piper > edge_max_por_real_pessimista, (
        "se as faixas voltarem a se tocar, releia o 748: a pinca teria aberto"
    )
    # e no caso OTIMISTA a sala e menor que um segundo -- nada de folga.
    assert 0 < edge_max_por_real - edge_min_por_piper < 1.0   # caso otimista


def test_o_mesmo_edge_devolveu_o_mesmo_real_duas_vezes():
    """Contra o 732 ("a previsao nao prediz"): s039 e s040, ambos 24,7 -> 27."""
    import importlib
    m = importlib.import_module("test_residuo_quebra_o_limite_de_dois_segundos")
    por_prev = {}
    for pacote, prev, real, _ in m.SERIE:
        por_prev.setdefault(prev, set()).add(real)
    assert por_prev.get(24.7) == {27}, por_prev.get(24.7)


def test_a_pinca_foi_confirmada_pelos_DOIS_lados_em_14_10():
    """751: a contradicao do 740/748 deixou de ser so aritmetica.

    Dez pecas escolheram manter a previsao DENTRO da mira nos dois mundos, e o
    real saiu FORA do teto em quatro das cinco narradas pelo edge. O `s042`
    inverteu a escolha de proposito — previsao edge 23,4, com o piper em 19,2,
    ABAIXO do piso, logo `mira.py` reprovando — e o real caiu em 25, DENTRO.

    Logo os dois lados da pinca estao MEDIDOS, nao deduzidos: mira verde entrega
    real fora, e real dentro exige mira vermelha pelo piso. Este teste falha se
    alguem apagar um dos dois lados da serie.
    """
    piso, teto = ensaio.alvo_short("labtreinamento")
    # (previsao edge, real, previsao piper)
    verde_fora = [(25.8, 28), (24.7, 27), (24.6, 27)]   # s037, s039/s040, s041
    vermelha_dentro = (23.4, 25, 19.2)                   # s042
    for prev, real in verde_fora:
        assert prev <= teto, prev            # previsao DENTRO da mira
        assert real > teto, (prev, real)     # e o real FORA
    prev, real, prev_piper = vermelha_dentro
    assert prev_piper < piso, prev_piper     # mira REPROVA pelo piso
    assert real <= teto, real                # e o real cai DENTRO
    assert 0.9 <= real - prev <= 3.7, real - prev
