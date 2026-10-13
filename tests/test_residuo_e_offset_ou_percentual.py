"""O residuo do EDGE: quatro de quatro acima, e percentual NAO se distingue de
OFFSET com n=4. Medido 13/10 as 19:3x.

**Primeira previsao OUT-OF-SAMPLE do 733, e ela errou para baixo.** Eu escrevi na
copy do `labtreinamento-s033`, ANTES de publicar, que "o real deve sair ~2,5%
acima do estimado se o edge narrar, isto e ~26,3". Previsao edge **25,7**,
provedor medido **edge** (zero avisos de Piper), real **27** -- **+5,1%**, acima
do maximo que eu tinha observado (+4,5%).

As quatro pecas do edge, com o provedor MEDIDO pela anotacao (733):

    pacote                  prev edge   real   residuo   razao
    epomeno-epipedo-s024       43,1      44     +0,9 s   +2,1%
    kolejny-poziom-s024        42,9      44     +1,1 s   +2,5%
    epomeno-epipedo-s025       42,1      44     +1,9 s   +4,5%
    labtreinamento-s033        25,7      27     +1,3 s   +5,1%

**O sinal e o metodo do 733 ficam de pe: quatro de quatro acima.** O que NAO fica
e' o NUMERO: a mediana de +2,5% era de n=3 todas na mesma faixa de 42 a 43 s, e
nao se generalizou para 25,7 s.

**E o ponto de metodo: com n=4 e granularidade de 1 s, percentual e OFFSET nao se
distinguem.** O residuo em segundos vai de **0,9 a 1,9 s** (razao 2,1) e em
percentual de **2,1% a 5,1%** (razao 2,4) -- as duas dispersoes sao da mesma
ordem, logo os dados nao escolhem entre os dois modelos. O que eu posso afirmar
e' so o LIMITE: o real ficou **sempre** acima, por **no maximo 1,9 s**.

**A consequencia pratica, e e a unica que vale hoje:** quem mira perto do teto de
45 s tem de contar com **~2 s** de residuo, e nao com 2,5%. Para uma peca de
43 s previstos isso da 45 -- no limite. **E isto NAO autoriza mexer na mira nem no
portao:** e' n=4, e a trava da §10 vale.

**E a minha declaracao na copy do `s033` errou junto:** eu escrevi "~26,3, um
decimo acima do topo da mira" e o real foi **27, um segundo acima**. A peca segue
dentro do portao (18 a 45) e fora da mira do canal (20 a 26) por 1 s.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402

# Provedor MEDIDO pela contagem de `::warning::NARRACAO PELO PIPER` (733).
EDGE = {
    "epomeno-epipedo-s024": 44,
    "kolejny-poziom-s024": 44,
    "epomeno-epipedo-s025": 44,
    "labtreinamento-s033": 27,   # out-of-sample, render 38453856451, 0 avisos
}


def _prev(pacote):
    s = json.loads((RAIZ / "fabrica" / "specs" / f"{pacote}.json").read_text())
    return ensaio.duracao_real_prevista(s["short"], s["voz"], "edge")


def test_quatro_de_quatro_acima__o_sinal_do_733_fica():
    for pacote, real in EDGE.items():
        assert real > _prev(pacote), (pacote, real, _prev(pacote))


def test_a_previsao_out_of_sample_do_733_errou_PARA_BAIXO():
    """Eu previ ~26,3 (vies de 2,5%) e saiu 27."""
    prev = _prev("labtreinamento-s033")
    assert prev * 1.025 < EDGE["labtreinamento-s033"]


def test_o_residuo_em_SEGUNDOS_nao_passa_de_dois():
    """O limite que eu posso afirmar com n=4."""
    for pacote, real in EDGE.items():
        assert 0 < real - _prev(pacote) <= 2.0, (pacote, real - _prev(pacote))


def test_percentual_e_OFFSET_nao_se_distinguem_com_n_quatro():
    """As duas dispersoes sao da mesma ordem, logo os dados nao escolhem."""
    seg = [EDGE[p] - _prev(p) for p in EDGE]
    pct = [(EDGE[p] - _prev(p)) / _prev(p) for p in EDGE]
    r_seg = max(seg) / min(seg)
    r_pct = max(pct) / min(pct)
    assert 1.5 < r_seg < 3.5, seg
    assert 1.5 < r_pct < 3.5, pct
    assert abs(r_seg - r_pct) < 1.0, (r_seg, r_pct)


def test_a_peca_de_25_7_quebra_a_mediana_das_tres_de_42_a_43():
    """Por que a mediana de +2,5% nao se generalizou: as tres de n=3 estavam
    todas na MESMA faixa de duracao, e a quarta esta a 17 s de distancia."""
    altas = [_prev(p) for p in EDGE if _prev(p) > 40]
    baixa = [_prev(p) for p in EDGE if _prev(p) <= 40]
    assert len(altas) == 3 and len(baixa) == 1
    assert min(altas) - baixa[0] > 15


def test_a_s033_cabe_no_portao_e_NAO_na_mira_do_canal():
    """Dito em vez de escondido: 27 contra a mira 20 a 26."""
    from prontidao import SHORT_MAX_S, SHORT_MIN_S
    real = EDGE["labtreinamento-s033"]
    assert SHORT_MIN_S <= real <= SHORT_MAX_S
    piso, teto = ensaio.alvo_short("labtreinamento")
    assert real > teto, (real, teto)
    assert real - teto <= 1.5, (real, teto)
