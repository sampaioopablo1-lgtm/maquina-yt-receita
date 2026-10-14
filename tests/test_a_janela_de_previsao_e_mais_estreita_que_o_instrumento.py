"""Cinco pontos numa janela de 0,4 s, e um real com granularidade de 1 s.

NASCEU DE DUAS AFIRMACOES MINHAS SEGUIDAS, as duas sobre os MESMOS dados e as
duas em excesso:

  * as 18:2x (766) eu escrevi que "a previsao REPRODUZ nesta faixa", a partir de
    dois pontos do epomeno (41,4 -> 43 e 41,3 -> 43);
  * as 19:1x (767) eu retratei isso, a partir de dois pontos do kolejny que
    INVERTEM (41,2 -> 44 e 41,6 -> 43).

O quinto ponto (epomeno-epipedo-s028, 41,5 -> 43, as 20:1x) fecha a conta e
mostra que NENHUMA das duas podia ser medida: as cinco previsoes caem numa
janela de **0,4 s** e o real tem granularidade de **1 s, arredondado para
cima**. Uma janela mais ESTREITA que o passo do instrumento nao pode ordenar
nada — e o 733 ja havia dito isso sobre o "paradoxo" do 732, com tres pontos
dentro de 1,0 s. Eu reapliquei o erro que aquele aprendizado nomeia, duas vezes,
em duas horas.

O QUE ESTES TESTES AFIRMAM: a propriedade de FORMA — que a janela e mais estreita
que a granularidade, logo a serie nesta faixa nao decide reprodutibilidade em
sentido nenhum.

O QUE ELES NAO AFIRMAM: que a previsao reproduz, nem que nao reproduz. Para
decidir isso e preciso previsao separada por MAIS de 1 s, e isso e desenho, nao
leitura dos dados que ja existem.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

GRANULARIDADE_DO_REAL = 1.0  # o YouTube devolve segundo inteiro, para CIMA
FAIXA = (41.0, 42.0)


def _janela():
    return [(p, prev, real) for p, prev, real, _ in SERIE
            if FAIXA[0] <= prev <= FAIXA[1]]


def test_a_janela_existe_e_tem_pelo_menos_CINCO_pontos():
    j = _janela()
    assert len(j) >= 5, f"a nota do 768 foi escrita com cinco pontos, achei {len(j)}"


def test_a_largura_da_PREVISAO_e_menor_que_a_granularidade_do_REAL():
    """E esta e a razao pela qual as duas afirmacoes cairam."""
    j = _janela()
    largura = max(p for _, p, _ in j) - min(p for _, p, _ in j)
    assert largura < GRANULARIDADE_DO_REAL, (
        f"largura {largura:.2f} s já passou do passo do instrumento "
        f"({GRANULARIDADE_DO_REAL} s): agora a serie PODE ordenar, e a nota do "
        "768 tem de ser RELIDA em vez de reaproveitada")


def test_a_janela_e_MULTICANAL__nao_e_efeito_de_um_canal():
    j = _janela()
    canais = {p.rsplit("-s", 1)[0] for p, _, _ in j}
    assert len(canais) >= 2, canais


def test_o_real_da_janela_e_quase_CONSTANTE():
    """Quatro de cinco no mesmo inteiro — o que se espera sob falta de resolucao."""
    j = _janela()
    reais = [r for _, _, r in j]
    moda = max(set(reais), key=reais.count)
    assert reais.count(moda) >= len(reais) - 1, reais


def test_o_ponto_DIVERGENTE_nao_e_o_de_maior_previsao():
    """Se a previsao ordenasse, o real maior viria da previsao maior.

    O ponto de real 44 e justamente o de previsao MENOR da janela (41,2), que e
    o oposto do que uma relacao monotona daria. Isso NAO prova desordem — prova
    que nesta largura o sinal nao se distingue do arredondamento.
    """
    j = _janela()
    maior_real = max(r for _, _, r in j)
    divergentes = [p for _, p, r in j if r == maior_real]
    menor_prev = min(p for _, p, _ in j)
    assert menor_prev in divergentes, (
        "se o real maior passar a vir da previsao maior, releia o 766/767/768 — "
        "pode ter aparecido ordenacao de verdade")


def test_todos_os_residuos_da_janela_seguem_POSITIVOS():
    """O que sobrevive dos tres aprendizados e so o SINAL."""
    for p, prev, real in _janela():
        assert real - prev > 0, (p, prev, real)
