"""A banda de residuo NAO e de um canal — e eu ia escrever que era (763).

ESTE ARQUIVO NASCEU DE UM ERRO MEU, pego pelo primeiro teste que escrevi nele.
Em 14/10 as 16:2x o `epomeno-epipedo-s026` (`rbbz6DNuXL4`, provedor **edge**
medido, zero avisos no job `115963870489`) previa **41,4** e saiu com **43 s
REAIS** — residuo **+1,6**, dentro da banda. Eu ia registrar isso como "o
primeiro ponto FORA do labtreinamento" e travar a serie como sendo de UM canal.

**O teste reprovou na hora:** a serie tem `epomeno-epipedo-s024`, `-s025` e
`kolejny-poziom-s024` desde o 734 — ela e MULTICANAL desde o primeiro dia. A
minha premissa era falsa, e o ponto do epomeno PERTENCE a ela.

**E o que sobra e um achado melhor do que o que eu ia escrever:** a serie e
**dominada por um canal** (18 de 22) e **bimodal na previsao** — dezoito pontos
entre 23 e 26 s, quatro entre 41 e 44. O teto de 3,7 vem do
`labtreinamento-s043`. Logo "0,9 a 3,7" e, na pratica, a banda do
`labtreinamento` usando cracha de frota, e isso tem de ir dito em vez de
desaparecer na contagem.
"""
import collections
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import mira  # noqa: E402
from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402


def _canais():
    return collections.Counter(p.rsplit("-s", 1)[0] for p, *_ in SERIE)


def test_a_serie_e_MULTICANAL__a_minha_premissa_era_falsa():
    c = _canais()
    assert len(c) >= 3, c
    assert {"labtreinamento", "epomeno-epipedo", "kolejny-poziom"} <= set(c)


def test_UM_canal_domina_a_serie__e_isso_vai_dito():
    c = _canais()
    dom, n_dom = c.most_common(1)[0]
    assert dom == "labtreinamento"
    assert n_dom / sum(c.values()) > 0.75, (
        "se a dominancia cair, a banda deixou de ser 'de um canal com cracha de "
        "frota' e esta nota tem de ser relida")


def test_o_TETO_da_banda_vem_do_canal_dominante():
    """Quem define 3,7 e o `labtreinamento-s043`, nao a frota."""
    pior = max(SERIE, key=lambda r: r[2] - r[1])
    assert pior[0].startswith("labtreinamento"), pior
    assert abs((pior[2] - pior[1]) - mira.RESIDUO_OBSERVADO[1]) < 0.05


def test_a_serie_e_BIMODAL_na_previsao__nao_e_uma_faixa_so():
    curtos = [p for _, p, _, _ in SERIE if p < 30]
    longos = [p for _, p, _, _ in SERIE if p >= 30]
    assert len(curtos) >= 15 and len(longos) >= 3
    assert min(longos) - max(curtos) > 10, (
        "as duas nuvens estao a mais de dez segundos — uma banda unica sobre as "
        "duas e uma escolha, nao um dado")


def test_TODOS_os_residuos_seguem_positivos():
    for pacote, prev, real, _prov in SERIE:
        assert real - prev > 0, pacote
    assert mira.RESIDUO_N == len(SERIE)


def test_o_ponto_do_epomeno_de_14_10_esta_na_serie_e_caiu_DENTRO():
    alvo = [r for r in SERIE if r[0] == "epomeno-epipedo-s026"]
    assert alvo, "o ponto medido na rodada das 16:07 tem de estar aqui"
    _p, prev, real, prov = alvo[0]
    assert (prev, real, prov) == (41.4, 43, "edge")
    lo, hi = mira.RESIDUO_OBSERVADO
    assert lo <= real - prev <= hi
