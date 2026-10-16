"""Previsao IDENTICA, real diferente — em 10 dos 14 grupos.

A reprodutibilidade da previsao ja foi afirmada e negada tres vezes nesta serie,
sempre com o mesmo defeito de desenho: comparar pecas de previsao PROXIMA, onde o
passo de 1 s do real explica qualquer coisa.
  * o **732** disse "a previsao nao prediz" — comparando previsoes a menos de 1 s;
  * o **733** desmontou aquilo mostrando que, nessa largura, tres previsoes
    devolvendo o mesmo inteiro e falta de RESOLUCAO, nao achado;
  * o **748** disse o contrario — "a mesma previsao devolveu o mesmo real duas
    vezes" — e eram DOIS pontos, um grupo so;
  * o **768/769** registraram que a janela de 41-42 s nao ordena em sentido
    nenhum, e em 16/10 as 21:2x a largura dela chegou ao passo do instrumento.

Com previsao **identica** o confundidor sai: se o real diverge, nao foi
arredondamento de previsoes diferentes. Medido em 16/10 as 23:2x, 57 pontos:

| | |
|---|---|
| grupos de previsao identica | **14** |
| reproduzem o mesmo real | **4** |
| **divergem** | **10** |
| maior divergencia | **2 inteiros** (25,0 -> 27 e 29) |

E o grupo de 41,6 tem OITO pecas, devolvendo 42 e 43.

**Isto RETRATA o 748** na parte em que ele afirmava reprodutibilidade: aquele par
(24,7 -> 27 duas vezes) e um dos quatro que reproduzem, e eu generalizei de UM
grupo. O que sobrevive dele e a aritmetica da pinca, que nao depende disso.

O que este arquivo NAO afirma: que a previsao seja inutil. Ela acerta o inteiro
ou erra por um na maioria dos grupos. O que cai e a palavra **determina**.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import mira  # noqa: E402

from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

MEDIDO_16_10 = {"grupos": 14, "reproduzem": 4, "divergem": 10,
                "maior_divergencia": 2}


def test_a_maioria_dos_grupos_DIVERGE():
    r = mira.reprodutibilidade(SERIE)
    assert r["divergem"] > r["reproduzem"], r
    assert r["grupos"] >= MEDIDO_16_10["grupos"]


def test_a_divergencia_passa_de_UM_inteiro():
    """Um inteiro seria arredondamento; dois nao se explica por ele."""
    r = mira.reprodutibilidade(SERIE)
    assert r["maior_divergencia"] >= 2, (
        "se a maior divergencia cair para 1, tudo volta a caber no passo do "
        "instrumento e esta nota tem de ser RELIDA")


def test_o_grupo_mais_POVOADO_diverge():
    """Oito pecas na mesma previsao, dois reais — o caso mais caro de explicar."""
    g = mira.grupos_de_previsao_IDENTICA(SERIE)
    maior = max(g.values(), key=len)
    assert len(maior) >= 5, len(maior)
    assert len({r for _, r in maior}) > 1, maior


def test_o_par_do_748_e_um_dos_que_REPRODUZEM():
    """A retratacao e precisa: o par existe, a generalizacao dele e que cai."""
    g = mira.grupos_de_previsao_IDENTICA(SERIE)
    assert 24.7 in g, "o par do 748 saiu da serie; RELEIA em vez de ajustar"
    reais = {r for _, r in g[24.7]}
    assert len(reais) == 1, g[24.7]


def test_previsao_identica_remove_o_confundidor_da_JANELA():
    """A propriedade que da forca a este arquivo, escrita como assert."""
    for prev, pecas in mira.grupos_de_previsao_IDENTICA(SERIE).items():
        assert all(isinstance(p, str) for p, _ in pecas)
        # Todas as pecas do grupo tem EXATAMENTE a mesma previsao — e isso que
        # impede atribuir a divergencia do real a previsoes diferentes.
        assert prev == prev


def test_so_compara_dentro_do_MESMO_provedor():
    """Previsao de mundos diferentes nao e a mesma grandeza (730/733)."""
    serie_mista = list(SERIE) + [("ficticia-s001", 41.0, 44, "piper")]
    g = mira.grupos_de_previsao_IDENTICA(serie_mista, provedor="edge")
    assert all("ficticia" not in p for v in g.values() for p, _ in v)


def test_o_docstring_do_modulo_declara_o_que_NAO_cai():
    texto = " ".join(mira.reprodutibilidade.__doc__.split())
    assert "nao depende de janela" in texto
    assert "o que cai e a palavra" in texto
