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
    """O VALOR mudou em 12/10; a INTENCAO deste teste nao.

    Ele fixava (33,0, 37,0) do 682/698. As decisoes de 12/10
    (`docs/decisoes-12-10.md`, autorizadas pelo dono em palavras explicitas)
    puseram o canal em 20,0 a 26,0 de duracao REAL, porque a faixa antiga media
    qual duracao era melhor DENTRO de um regime que nunca rompeu (713: 161
    pecas, 19 inscritos, nenhuma acima de dois).

    O que este teste continua guardando, e e o que importa: que o canal tem mira
    PROPRIA e que ela e mais curta que a da frota. Trocar o numero sem trocar
    isso seria perder o teste.
    """
    lo, hi = ensaio.alvo_short("labtreinamento")
    assert (lo, hi) == (20.0, 26.0), (
        "se isto voltou a 33-37, leia docs/decisoes-12-10.md antes de mexer"
    )
    assert hi < ensaio.ALVO_SHORT[0], "a mira do canal tem de ser MENOR que a da frota"


@pytest.mark.parametrize("canal", ["epomeno-epipedo", "kolejny-poziom"])
def test_os_outros_dois_canais_seguem_a_frota(canal):
    """Se alguem der override a estes, o braco do 38 morre sem veredito."""
    assert ensaio.alvo_short(canal) == ensaio.ALVO_SHORT


def test_canal_desconhecido_cai_na_frota():
    assert ensaio.alvo_short("canal-que-nao-existe") == ensaio.ALVO_SHORT
    assert ensaio.alvo_short(None) == ensaio.ALVO_SHORT


def test_a_mira_do_canal_cabe_no_portao_de_duracao():
    """Mira abaixo do piso do portao seria mira que reprova sempre.

    O piso era 30 s e caiu para 18 em 12/10 — ele era constante NUA, sem
    procedencia, e nao e regra do YouTube. Este teste le `prontidao.SHORT_MIN_S`
    em vez de repetir o numero, entao ele acompanha a mudanca sem mentir.
    """
    lo, hi = ensaio.alvo_short("labtreinamento")
    assert lo >= prontidao.SHORT_MIN_S, "a mira ficou abaixo do piso do portao"
    assert hi <= prontidao.SHORT_MAX_S / (1 + prontidao.MARGEM_SHORT)
