"""A SOMA MAXIMA e CEGA quando as divergencias se CANCELAM -- medido 20:2x 13/10.

O procedimento do 708/722 manda comparar a SOMA das chamadas e gravar a de soma
maxima. Medido hoje, em duas chamadas separadas por segundos sobre os mesmos
oito ids (`status_code` 200 nas duas):

    id              chamada 992   chamada 994   piso por peca
    CdUiplaeP5g           5             6              6
    uhhg3nZ1ZEY          12            11             12
    UOLpIvPCl58           9             9              9
    rWDgoEwwEWY          12            10             12
    UEz0xdb3CL0          17            17             17
    xwqCqRlE3jg          28            23             28
    vHknlJnkUNA          30            38             38
    SOMA                113           114            122

**As somas diferem em UM (113 contra 114) enquanto pecas individuais diferem em
ate OITO**, e as divergencias se CANCELAM: `vHknlJnkUNA` sobe +8 e `xwqCqRlE3jg`
cai −5 na mesma chamada. **A chamada de soma maxima NAO e a de maiores valores
por peca** -- o piso somado e 122, que chamada nenhuma devolveu.

**O que isto NAO derruba:** o 708 segue valido quando a divergencia tem a MESMA
FORMA (replica atrasada inteira), e o `replica.mesma_forma` devolveu **False**
aqui, isto e, o proprio instrumento avisou que a hipotese do 708 nao se aplicava
a esta rodada. O procedimento ja previa isso; **eu gravei de todo modo**, e o
resultado foi subestimar TRES pecas: 11 contra 12, 10 contra 12, e 23 contra 28.

**O que isto acrescenta, e e a parte nova:** a soma empatada nao e evidencia de
que as chamadas concordam. **Soma proxima com dispersao alta por peca e o caso em
que a soma maxima mais engana**, porque a estatistica escolhida agrega exatamente
o que precisava ser visto separado.

**A linha de `metricas` NAO se corrige** (722): ela e o que aquela chamada disse.
O que se faz e DECLARAR a diferenca, e e isto.

**Procedimento que fica:** antes de gravar, compare a soma do PISO POR PECA com a
soma da chamada escolhida. Se a diferenca passar de ~5%, a soma esta mascarando
dispersao e o relato tem de dizer quais pecas ficaram subestimadas.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import replica  # noqa: E402

# Medido as 20:2x de 13/10, reqs 992 e 994 do pg_net, status_code 200 nas duas.
C992 = {"CdUiplaeP5g": 5, "uhhg3nZ1ZEY": 12, "UOLpIvPCl58": 9, "rWDgoEwwEWY": 12,
        "UEz0xdb3CL0": 17, "xwqCqRlE3jg": 28, "vHknlJnkUNA": 30}
C994 = {"CdUiplaeP5g": 6, "uhhg3nZ1ZEY": 11, "UOLpIvPCl58": 9, "rWDgoEwwEWY": 10,
        "UEz0xdb3CL0": 17, "xwqCqRlE3jg": 23, "vHknlJnkUNA": 38}
GRAVADA = C994   # soma maxima, 114


def test_as_somas_quase_empatam_e_as_pecas_divergem_muito():
    """O fato central."""
    assert abs(sum(C992.values()) - sum(C994.values())) == 1
    deltas = [abs(C992[k] - C994[k]) for k in C992]
    assert max(deltas) >= 8, deltas


def test_as_divergencias_se_CANCELAM_na_soma():
    """Uma sobe, outra desce, e a soma nao sente."""
    sobe = [k for k in C992 if C994[k] > C992[k]]
    desce = [k for k in C992 if C994[k] < C992[k]]
    assert sobe and desce, (sobe, desce)


def test_o_piso_por_peca_e_MAIOR_que_qualquer_chamada():
    piso = {k: max(C992[k], C994[k]) for k in C992}
    assert sum(piso.values()) > max(sum(C992.values()), sum(C994.values()))
    assert sum(piso.values()) == 122


def test_a_chamada_gravada_subestima_TRES_pecas():
    """Declarado em vez de corrigido, pelo 722."""
    piso = {k: max(C992[k], C994[k]) for k in C992}
    menores = {k for k in piso if GRAVADA[k] < piso[k]}
    assert menores == {"uhhg3nZ1ZEY", "rWDgoEwwEWY", "xwqCqRlE3jg"}, menores


def test_o_proprio_instrumento_avisou__mesma_forma_False():
    """O 708 nao se aplicava a esta rodada, e o modulo disse isso ANTES."""
    assert replica.mesma_forma([C992, C994]) is False


def test_o_criterio_novo__piso_somado_contra_a_chamada_passa_de_cinco_porcento():
    """O gatilho que o relato tem de observar."""
    piso = sum(max(C992[k], C994[k]) for k in C992)
    esc = sum(GRAVADA.values())
    assert (piso - esc) / esc > 0.05
