"""Trava a medicao de 16/10 e a correcao do numero que eu dei errado.

O dono pediu replicar "qualidade, efeitos, narracao" para os tres canais. A
narracao foi medida contra a referencia (`FtCtIJPsc_Q`) e **ja bate**; o numero
de "25% mais rapida" que eu dei antes comparava taxa de FALA com taxa EFETIVA,
que e a classe de erro do 711.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao_referencia as N  # noqa: E402


def test_o_ritmo_da_referencia_sai_da_legenda_medida():
    assert abs(N.ritmo_da_referencia() - 13.98) < 0.05
    assert abs(N.palavras_por_frase_da_referencia() - 12.7) < 0.1


def test_a_nossa_narracao_bate_com_a_referencia():
    """O ponto que derruba o meu "25% mais rapida"."""
    for voz in N.RITMO_EFETIVO:
        d = N.desvio_do_ritmo(voz)
        assert abs(d) < 0.12, (voz, d)


def test_o_fator_do_rate_e_INDEPENDENTE_de_voz():
    vals = list(N.FATOR_RATE_4_PARA_23.values())
    assert max(vals) - min(vals) <= 0.002, vals
    assert abs(N.fator_do_rate() - 0.802) < 0.002


def test_o_fator_RECUSA_par_que_nao_foi_medido():
    """Interpolar rate nao medido e inventar numero (679/698)."""
    import pytest
    with pytest.raises(ValueError):
        N.fator_do_rate("-4%", "-10%")


def test_o_rate_em_producao_NAO_mudou():
    """A medicao nao autoriza mexer no botao: -23% poria o short fora do teto.

    Se alguem mudar o `rate` do `fabrica.py`, este teste reprova para que a
    conta da duracao seja refeita ANTES, nao depois.
    """
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text(encoding="utf-8")
    assert f'rate="{N.RATE_EM_PRODUCAO}"' in fonte, (
        "o `rate` do edge-tts mudou: o `R` de MODELO_VOZ escala por 0,802 para"
        " -23%, e sem cortar ~20% dos caracteres por cena o short passa do teto"
        " de 45 s e deixa de ser tratado como Short"
    )


def test_a_voz_pt_BR_fragil_vai_DECLARADA():
    """A Thalita nao sintetizou no sandbox, e isso e estado, nao propriedade."""
    doc = N.__doc__
    assert "ZERO audio" in doc
    assert "ESTADO e nao propriedade" in doc
    assert "proxy" in doc
