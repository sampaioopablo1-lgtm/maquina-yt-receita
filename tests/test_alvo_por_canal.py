"""A mira do short por CANAL. Ver o comentario em `fabrica/ensaio.py`.

Estes testes travam tres coisas:
  * que o labtreinamento tem mira PROPRIA e mais curta, porque o gatilho do 682
    disparou com idade casada (as duas pecas de mira nova abaixo do minimo das
    oito antigas);
  * que a mira da FROTA nao mudou, porque o experimento 38 segue aberto nos
    outros dois canais e mexer no global apagaria o braco;
  * que canal desconhecido cai na mira da frota em vez de explodir.
"""
import pytest

import ensaio
import prontidao


def test_a_mira_da_frota_continua_sendo_o_experimento_38():
    assert ensaio.alvo_short() == (41.5, 43.0)
    assert ensaio.ALVO_SHORT == (41.5, 43.0)


def test_o_labtreinamento_tem_mira_propria_e_mais_curta():
    lo, hi = ensaio.alvo_short("labtreinamento")
    assert (lo, hi) == (33.0, 37.0)
    assert hi < ensaio.ALVO_SHORT[0], "a mira do canal tem de ser MENOR que a da frota"


@pytest.mark.parametrize("canal", ["epomeno-epipedo", "kolejny-poziom"])
def test_os_outros_dois_canais_seguem_a_frota(canal):
    """Se alguem der override a estes, o braco do 38 morre sem veredito."""
    assert ensaio.alvo_short(canal) == ensaio.ALVO_SHORT


def test_canal_desconhecido_cai_na_frota():
    assert ensaio.alvo_short("canal-que-nao-existe") == ensaio.ALVO_SHORT
    assert ensaio.alvo_short(None) == ensaio.ALVO_SHORT


def test_a_mira_do_canal_cabe_no_portao_de_duracao():
    """Mira abaixo do piso de 30 s do portao seria mira que reprova sempre."""
    lo, hi = ensaio.alvo_short("labtreinamento")
    assert lo >= prontidao.SHORT_MIN_S, "a mira ficou abaixo do piso do portao"
    assert hi <= prontidao.SHORT_MAX_S / (1 + prontidao.MARGEM_SHORT)
