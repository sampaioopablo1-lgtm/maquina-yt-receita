"""O desenho tem de caber na faixa que o Ken Burns deixa visivel.

Medido em 17/08/2026. O portao de enquadramento passou a simular o movimento e
reprovou 19 das 22 specs — 40 cenas. Nenhuma era spec infeliz: eram quatro
defeitos de geometria, cada um deterministico.

    1. lista de QUATRO itens, passo fixo de 0,17H a partir de 0,38H: o quarto
       item caia em 0,89H, e a zona de risco comeca em 0,88H. Toda lista de
       quatro reprovava, sempre.
    2. rotulo de barra que quebra em duas linhas crescia PARA BAIXO a partir de
       0,865H, chegando a 0,912H.
    3. kicker de `barras` em 0,16H com corpo 0,08H punha o ascender em 0,102H,
       e o pan vertical sobe a faixa de topo ate 0,115H.
    4. `wrap` divide por espaco e nunca parte palavra, entao o `n` que parecia
       limitar a largura nao limitava nada: 'LabTreinamento' com n=11 saiu numa
       linha de 981 px num quadro de 1080.

O portao ja pega os quatro, mas so olhando pixel de spec real. Estes testes
olham a GEOMETRIA, entao continuam valendo para spec que ainda nao existe.
"""

import os
import sys
import types

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import fabrica as F  # noqa: E402
import layout as L  # noqa: E402

PAL = {"bg": "#FFFFFF", "c1": "#C9184A", "c2": "#7FB069", "ink": "#2B1B1F"}
W, H = 1280, 720
RW, RH = 1080, 1920


def test_a_margem_segura_do_desenho_e_a_do_portao():
    """Se as duas contas divergirem, o desenho volta a mirar fora do alvo."""
    assert F.MARGEM_SEGURA == pytest.approx(L.faixa_de_risco(), abs=1e-4)


# --- 1. lista de quatro itens -------------------------------------------------

@pytest.mark.parametrize("n_itens", [2, 3, 4, 5, 6])
def test_lista_cabe_na_faixa_segura(n_itens):
    cena = {"layout": "lista", "kicker": "k",
            "itens": [f"item {i}" for i in range(n_itens)]}
    assert L.tinta_na_borda(F.svg_cena(cena, PAL, W, H), W, H, 2) < L.LIMITE_PCT


def test_a_lista_de_tres_nao_mudou():
    """Com tres itens o passo antigo ja cabia; encolher seria regressao visual."""
    itens = ["um", "dois", "tres"]
    assert min(H * 0.17, H * 0.42 / (len(itens) - 1)) == pytest.approx(H * 0.17)


def test_a_lista_de_quatro_mudou():
    itens = ["um", "dois", "tres", "quatro"]
    passo = min(H * 0.17, H * 0.42 / (len(itens) - 1))
    assert passo < H * 0.17
    ultimo = H * 0.38 + passo * (len(itens) - 1)
    assert ultimo < H * (1 - F.MARGEM_SEGURA)


# --- 2. rotulo de barra que quebra -------------------------------------------

def test_rotulo_de_duas_linhas_cresce_para_cima():
    """`subindo` poe a ULTIMA linha onde a unica ficaria."""
    uma = F.tsp("curto", 100, 500, 40, "#000", n=14, subindo=True)
    duas = F.tsp("antes: caixa aleatoria", 100, 500, 40, "#000", n=14, subindo=True)
    assert 'y="500"' in uma
    assert 'y="450"' in duas          # subiu uma entrelinha, 40*1,25


def test_barras_com_rotulo_longo_cabem():
    cena = {"layout": "barras", "kicker": "A receita migra, nao some",
            "itens": ["antes: caixa aleatoria", "depois: preco fixo mais alto"],
            "alturas": [3, 7]}
    for i in range(4):               # os quatro movimentos do ken_burns
        assert L.tinta_na_borda(F.svg_cena(cena, PAL, W, H), W, H, i) < L.LIMITE_PCT


# --- 3. kicker alto demais para o pan vertical --------------------------------

def test_kicker_de_barras_sai_da_faixa_de_topo():
    """O pan vertical e o i%4 em 2 e 3 — e la que a borda de cima aparece."""
    cena = {"layout": "barras", "kicker": "Kapital po 30 latach (5% realnie)",
            "itens": ["300 zl", "500 zl", "1000 zl"], "alturas": [2, 4, 9]}
    for i in (2, 3):
        assert L.tinta_na_borda(F.svg_cena(cena, PAL, W, H), W, H, i) < L.LIMITE_PCT


# --- 4. wrap nao parte palavra ------------------------------------------------

def test_wrap_nao_parte_palavra_e_por_isso_n_nao_limita_largura():
    """O defeito raiz, explicito: n=11 devolve uma linha de 14 caracteres."""
    assert F.wrap("LabTreinamento", 11) == ["LabTreinamento"]


def test_wrap_nao_devolve_linha_vazia_na_frente():
    """Sem o guarda, a palavra longa vinha depois de um <tspan> vazio, e o
    bloco descia uma entrelinha inteira rumo a borda."""
    assert F.wrap("LabTreinamento", 11)[0] != ""
    assert F.wrap("a LabTreinamento b", 11) == ["a", "LabTreinamento", "b"]


def test_corpo_encolhe_quando_a_palavra_nao_cabe():
    """O caso real e o RETRATO: 1080 de largura, nao 1280."""
    cabe = F.corpo_que_cabe("LabTreinamento", 11, 108, RW * F.LARGURA_SEGURA)
    assert cabe < 108
    assert 14 * cabe * F.LARGURA_GLIFO <= RW * F.LARGURA_SEGURA + 1


def test_corpo_nao_cresce_quando_ja_cabe():
    assert F.corpo_que_cabe("ok", 11, 40, 10_000) == 40


def test_cta_com_palavra_longa_cabe_no_retrato():
    cena = {"layout": "cta", "kicker": "LabTreinamento", "sub": "a planilha completa"}
    for i in range(4):
        assert L.tinta_na_borda(F.svg_cena(cena, PAL, RW, RH), RW, RH, i) < L.LIMITE_PCT


# --- caixa do `preco` ---------------------------------------------------------

def test_preco_com_frase_inteira_cabe_na_tarja():
    """`preco` foi feito para um preco e chega frase de 54 caracteres."""
    cena = {"layout": "item", "kicker": "Kendaraan",
            "preco": "dari lima koma enam tiga ke tiga koma sembilan sembilan"}
    for i in range(4):
        assert L.tinta_na_borda(F.svg_cena(cena, PAL, W, H), W, H, i) < L.LIMITE_PCT


def test_texto_na_caixa_encolhe_nos_dois_eixos():
    curto = F.texto_na_caixa("9,90", 640, 400, 280, 90, "#FFF", corpo_max=43)
    longo = F.texto_na_caixa("dari lima koma enam tiga ke tiga koma sembilan sembilan",
                             640, 400, 280, 90, "#FFF", corpo_max=43)

    def corpo(svg):
        return int(svg.split('font-size="')[1].split('"')[0])

    assert corpo(curto) == 43
    assert corpo(longo) < 43


# --- o acervo inteiro ---------------------------------------------------------

def test_o_bullet_da_lista_em_retrato_nao_encosta():
    """Bolinha em 0,12W com raio 0,022W comecava em 0,098W; a zona e 0,1204W."""
    assert RW * 0.15 - RW * 0.022 > RW * F.MARGEM_SEGURA
