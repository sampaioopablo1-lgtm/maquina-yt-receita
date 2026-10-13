"""O 734 dizia "o real fica acima por NO MAXIMO 1,9 s". O quinto ponto deu +2,4 s.

Medido em 13/10 as 22:2x, no `labtreinamento-s034` (`wWmHRDmQMO4`): provedor
MEDIDO pela anotacao (zero avisos do Piper, logo EDGE), previsao edge 25,6 e real
**28** -- resido **+2,4 s**, **+9,4%**, acima do maior desvio ja observado nos
dois eixos.

E o ponto que mais corta: o `s033` previa **25,7** edge e deu **27**; o `s034`
previa **25,6** e deu **28**. Mesmo canal, mesma voz, mesmas dez cenas, mesmo
provedor medido, previsoes a UM DECIMO de distancia -- e reais diferentes em um
segundo inteiro. Logo o OFFSET tambem nao descreve: ele teria de ser constante.

O que sobrevive: o SINAL. Cinco de cinco acima da previsao do provedor que de
fato narrou.

O que isto custa na producao, e vai dito em vez de virar limiar: a mira do
`labtreinamento` e sobre a duracao REAL (20,0 a 26,0) e o `mira.py` a cobra sobre
o ESTIMADO. Estimado dentro nos dois mundos NAO poe o real dentro: o `s033` saiu
em 27 e o `s034` em 28. NAO mexi na mira -- n=5, e a trava da secao 10 vale.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

# (pacote, previsao do provedor MEDIDO, real, provedor medido pela anotacao)
SERIE = [
    ("epomeno-epipedo-s024", 43.1, 44, "edge"),
    ("kolejny-poziom-s024", 42.9, 44, "edge"),
    ("epomeno-epipedo-s025", 42.1, 44, "edge"),
    ("labtreinamento-s033", 25.7, 27, "edge"),
    ("labtreinamento-s034", 25.6, 28, "edge"),
]


def test_o_sinal_sobrevive__cinco_de_cinco_acima():
    assert all(real > prev for _, prev, real, _ in SERIE)


def test_o_limite_de_1_9_s_do_734_CAIU():
    pior = max(real - prev for _, prev, real, _ in SERIE)
    assert pior > 1.9, "se o pior residuo voltar a <=1,9 s, releia o 734 e o 739"
    assert abs(pior - 2.4) < 0.05


def test_duas_previsoes_a_um_decimo_dao_reais_diferentes_em_UM_SEGUNDO():
    s33 = dict((p, (prev, real)) for p, prev, real, _ in SERIE)["labtreinamento-s033"]
    s34 = dict((p, (prev, real)) for p, prev, real, _ in SERIE)["labtreinamento-s034"]
    assert abs(s33[0] - s34[0]) <= 0.1, "as previsoes tem de estar a um decimo"
    assert abs(s33[1] - s34[1]) == 1, "e os reais, a um segundo inteiro"


def test_o_OFFSET_tambem_nao_descreve():
    # offset constante exigiria residuo igual nas duas previsoes quase iguais
    r33, r34 = 27 - 25.7, 28 - 25.6
    assert abs(r34 - r33) > 1.0, "offset constante descreveria; ele nao descreve"


def test_o_PERCENTUAL_tambem_nao__e_a_dispersao_cresce_no_curto():
    pct = [(real - prev) / prev for _, prev, real, _ in SERIE]
    curtos = [p for (_, prev, _, _), p in zip(SERIE, pct) if prev < 30]
    longos = [p for (_, prev, _, _), p in zip(SERIE, pct) if prev >= 40]
    assert max(curtos) > max(longos), (
        "os dois pontos curtos trazem os maiores percentuais: 5,1% e 9,4%"
    )


def test_a_mira_do_canal_e_sobre_o_REAL_e_o_instrumento_cobra_o_ESTIMADO():
    import ensaio

    piso, teto = ensaio.alvo_short("labtreinamento")
    assert (piso, teto) == (20.0, 26.0)
    # as duas pecas narradas pelo edge sairam ACIMA do teto da mira, no REAL,
    # com o estimado dentro -- e e isso que o relato tem de dizer.
    for pacote, prev, real, _ in SERIE:
        if pacote.startswith("labtreinamento"):
            assert piso <= prev <= teto, "o estimado estava DENTRO"
            assert real > teto, "e o real saiu FORA"


def test_o_provedor_de_todas_foi_MEDIDO_e_nao_inferido():
    # zero avisos `NARRACAO PELO PIPER` na anotacao do job = edge narrou (733)
    assert {prov for *_, prov in SERIE} == {"edge"}
