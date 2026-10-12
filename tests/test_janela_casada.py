"""A comparacao em janela casada, travada nos numeros REAIS de 698, 701 e 12/10.

Este arquivo existe porque eu fazia esta comparacao DE CABECA, e de cabeca eu
errei no 684 (comparador escolhido a dedo) e no 682 (idades diferentes). Os tres
casos ancorados aqui sao medicoes de producao, nao exemplos inventados — se
alguem reescrever o modulo e um deles mudar de veredito, o teste diz qual.
"""
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import janela_casada as JC  # noqa: E402


# ---------------------------------------------------------------------------
# Os tres casos medidos
# ---------------------------------------------------------------------------

def test_698_labtreinamento_separou_e_o_p_e_um_nono():
    # Aprendizado 698, janela casada de 9 a 21 h: as duas pecas de mira nova
    # cairam ABAIXO do minimo das oito antigas. Eu reportei "~1%" de cabeca.
    r = JC.separacao(novo=[18, 9], antigo=[20, 21, 34, 48, 60, 68, 173, 196])
    assert r["ha_leitura"] is True
    assert r["direcao"] == "novo ABAIXO"
    assert r["n_total"] == 10
    # C(10,2) = 45, logo 2,2% — e NAO o "~1%" que eu disse. A conta de cabeca
    # usou ~1/9 (a chance de UMA peca ficar abaixo de oito), e depois tratou as
    # duas como independentes. Elas nao sao: e uma escolha sem reposicao.
    assert r["p_sob_a_nula"] == pytest.approx(1 / 45)


def test_701_kolejny_separou_no_sentido_OPOSTO_e_o_p_e_1_ponto_4():
    # Aprendizado 701, janela casada de 4 a 8 h: quatro de mira nova ACIMA dos
    # quatro antigos. Aqui o "1/C(8,4) = 1,4%" que eu escrevi estava certo.
    r = JC.separacao(novo=[209, 117, 115, 83], antigo=[17, 13, 4, 0])
    assert r["ha_leitura"] is True
    assert r["direcao"] == "novo ACIMA"
    assert r["p_sob_a_nula"] == pytest.approx(1 / 70)
    assert round(r["p_sob_a_nula"] * 100, 1) == 1.4


def test_os_dois_canais_apontam_para_LADOS_OPOSTOS():
    # E e por isso que a mira e POR CANAL e nao da frota: o mesmo tratamento
    # separou para baixo num canal e para cima no outro.
    lab = JC.separacao([18, 9], [20, 21, 34, 48, 60, 68, 173, 196])
    kol = JC.separacao([209, 117, 115, 83], [17, 13, 4, 0])
    assert lab["direcao"] != kol["direcao"]
    assert lab["ha_leitura"] and kol["ha_leitura"]


def test_12_10_as_faixas_SE_SOBREPOEM_entao_NAO_HA_LEITURA():
    # Medido em 12/10 as 19:1x, janela casada de 2,5 a 4,5 h de vida.
    # Mira nova (24 a 26 s reais): s018 = 16, s017 = 8
    # Mira antiga (29 a 35 s reais): s013 = 31, s015 = 20, s014 = 11, s016 = 1
    # As duas novas caem DENTRO de [1, 31]. A mediana nova (12) e menor que a
    # antiga (15,5), e isso NAO autoriza conclusao nenhuma.
    r = JC.separacao(novo=[16, 8], antigo=[31, 20, 11, 1])
    assert r["ha_leitura"] is False
    assert r["sobrepoe"] is True
    assert r["p_sob_a_nula"] is None
    assert "SOBREPOEM" in r["motivo"]
    # A mediana existe no retorno, mas nao pode ser o que decide.
    assert r["mediana_novo"] == 12.0
    assert r["mediana_antigo"] == 15.5
    assert "NAO HA LEITURA" in JC.relato(
        {**r, "faixa_h": (2.5, 4.5), "sem_leitura": [],
         "braco_novo": "mira nova", "braco_antigo": "mira antiga"})


# ---------------------------------------------------------------------------
# As recusas — e elas sao o ponto do modulo
# ---------------------------------------------------------------------------

def test_uma_peca_boa_no_braco_novo_NAO_compra_leitura():
    # O efeito do paragrafo 3.8: n pequeno sob CV 0,66 fabrica "o tratamento
    # funcionou" a partir de UMA peca boa. Se ela nao supera o MAXIMO antigo,
    # nao ha separacao, e o modulo tem de dizer isso.
    r = JC.separacao(novo=[150], antigo=[196, 20, 9])
    assert r["ha_leitura"] is False


def test_separacao_com_n_UM_de_cada_lado_declara_o_p_honesto():
    # Um contra um separa trivialmente, e o p e 1/2. O modulo nao esconde isso:
    # quem ler o p ve que a separacao nao vale nada.
    r = JC.separacao(novo=[10], antigo=[5])
    assert r["ha_leitura"] is True
    assert r["p_sob_a_nula"] == pytest.approx(0.5)


def test_braco_vazio_LEVANTA_em_vez_de_devolver_veredito():
    with pytest.raises(ValueError):
        JC.separacao(novo=[], antigo=[1, 2])
    with pytest.raises(ValueError):
        JC.separacao(novo=[1], antigo=[])


def test_ausencia_de_leitura_na_faixa_e_SILENCIO_e_nao_zero():
    # O mesmo principio do `replica.piso`: id ausente nao e leitura de zero.
    with pytest.raises(JC.SemLeituraNaFaixa):
        JC.leitura_na_faixa([(0.9, 0), (12.0, 400)], 2.5, 4.5)


def test_leitura_na_faixa_toma_o_MAXIMO_pelo_estimador_do_688():
    # Duas leituras dentro da faixa: vale a maior, porque o contador so atrasa.
    assert JC.leitura_na_faixa([(3.0, 11), (4.1, 8), (12.0, 99)], 2.5, 4.5) == 11


def test_compara_exige_exatamente_DOIS_bracos():
    pecas = {"a": [(3.0, 5)], "b": [(3.0, 7)], "c": [(3.0, 9)]}
    with pytest.raises(ValueError):
        JC.compara(pecas, {"x": ["a"], "y": ["b"], "z": ["c"]}, 2.5, 4.5)
    with pytest.raises(ValueError):
        JC.compara(pecas, {"x": ["a"]}, 2.5, 4.5)


def test_compara_separa_quem_nao_tem_leitura_na_faixa_em_sem_leitura():
    # A peca de 0,86 h (o s020 recem-publicado) nao entra como zero: ela sai
    # NOMEADA em `sem_leitura`, que e o que o relato ao dono precisa dizer.
    pecas = {
        "s018": [(2.93, 16)],
        "s017": [(3.64, 8)],
        "s020": [(0.86, 0)],          # fora da faixa
        "s013": [(3.01, 31)],
        "s015": [(3.01, 20)],
    }
    r = JC.compara(pecas, {"mira nova": ["s018", "s017", "s020"],
                           "mira antiga": ["s013", "s015"]}, 2.5, 4.5)
    assert r["sem_leitura"] == ["s020"]
    assert r["valores"] == {"s018": 16, "s017": 8, "s013": 31, "s015": 20}
    # Com o braco antigo TRUNCADO em duas pecas, [8, 16] fica abaixo de
    # [20, 31] e o modulo diz que separa. Isto esta CERTO para os dados dados —
    # e e o aviso do teste seguinte.
    assert r["ha_leitura"] is True
    assert r["direcao"] == "novo ABAIXO"


def test_TRUNCAR_o_braco_antigo_FABRICA_a_leitura_e_e_o_erro_do_684():
    # O mesmo dado de 12/10, mudando SO quantas pecas antigas eu deixo entrar.
    # Com as quatro que existem (31, 20, 11, 1) nao ha leitura; tirando as duas
    # piores (11 e 1) aparece uma "separacao" com p = 1/15.
    #
    # Nenhuma peca mudou de valor. Mudou o comparador que EU escolhi — que e
    # literalmente o aprendizado 684. Este teste existe para que o modulo nunca
    # seja usado com um braco antigo escolhido a dedo sem alguem notar.
    completo = JC.separacao(novo=[16, 8], antigo=[31, 20, 11, 1])
    truncado = JC.separacao(novo=[16, 8], antigo=[31, 20])
    assert completo["ha_leitura"] is False
    assert truncado["ha_leitura"] is True
    assert truncado["p_sob_a_nula"] == pytest.approx(1 / 6)


def test_o_relato_NOMEIA_quem_ficou_sem_leitura():
    pecas = {"a": [(3.0, 5)], "b": [(0.5, 0)], "c": [(3.0, 50)]}
    r = JC.compara(pecas, {"novo": ["a", "b"], "antigo": ["c"]}, 2.5, 4.5)
    texto = JC.relato(r)
    assert "SEM leitura na faixa" in texto
    assert "silencio, nao zero" in texto
    assert "b" in texto
