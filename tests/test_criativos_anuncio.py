"""A peca de anuncio: se a tipografia vaza ou some, a verba paga por isso.

O feed julga em menos de 2 segundos. Os defeitos que estes testes cercam sao os
que sobrevivem ao olho no editor e so aparecem depois de publicado:
texto sangrando fora da arte, chamada espremida em fonte minuscula, e texto
branco sobre foto clara sem contraste.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import criativos_anuncio as C  # noqa: E402


def foto(larg=1600, alt=2000, claro=True):
    img = Image.new("RGB", (larg, alt), (245, 243, 238) if claro else (20, 20, 30))
    return img


def test_toda_peca_sai_no_formato_do_feed():
    for peca in C.PECAS:
        assert C.compor(foto(), peca).size == (C.L, C.A), peca[0]


def test_foto_deitada_e_recortada_sem_distorcer():
    # Foto 3:2 tem de virar 4:5 por corte, nao por esticar.
    assert C.cobrir(foto(3000, 2000)).size == (C.L, C.A)


def test_foto_menor_que_a_arte_ainda_preenche():
    assert C.cobrir(foto(400, 300)).size == (C.L, C.A)


def test_texto_nunca_passa_da_margem():
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    util = C.L - 2 * C.MARGEM
    for peca in C.PECAS:
        fnt, linhas = C.ajustar(peca[4], util, d, 92, 52, 3)
        for ln in linhas:
            assert d.textlength(ln, font=fnt) <= util, f"{peca[0]}: {ln!r}"


def test_chamada_cabe_em_tres_linhas_sem_encolher_demais():
    # Abaixo de 52px a chamada some no celular; acima de 3 linhas vira parede.
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for peca in C.PECAS:
        fnt, linhas = C.ajustar(peca[4], C.L - 2 * C.MARGEM, d, 92, 52, 3)
        assert len(linhas) <= 3, f"{peca[0]}: {len(linhas)} linhas"
        assert fnt.size >= 52, f"{peca[0]}: {fnt.size}px"


def test_rodape_fica_escuro_mesmo_sobre_foto_clara():
    # O modo de falha real: foto de ceu/parede branca e texto branco sumindo.
    img = C.escurecer(C.cobrir(foto(claro=True)))
    for x in (C.MARGEM // 2, C.L // 2, C.L - 20):
        r, g, b = img.getpixel((x, C.A - 24))
        assert (r + g + b) / 3 < 90, f"x={x} claro demais: {(r, g, b)}"


def test_topo_da_arte_continua_sendo_a_foto():
    # O veu nao pode cobrir a imagem inteira: sem foto visivel a peca vira placa.
    img = C.escurecer(C.cobrir(foto(claro=True)))
    r, g, b = img.getpixel((C.L // 2, 60))
    assert (r + g + b) / 3 > 170


def test_toda_peca_declara_funil_busca_e_botao():
    for peca in C.PECAS:
        pid, funil, q, sobr, cham, apoio, botao = peca
        assert funil in ("topo", "fundo"), pid
        assert q and sobr and cham and apoio and botao, pid


def test_topo_nao_oferece_reuniao_e_fundo_oferece():
    # Publico frio que leva oferta na cara nao converte: o topo nomeia a dor.
    for peca in C.PECAS:
        botao = peca[6].lower()
        if peca[1] == "topo":
            assert "agende" not in botao, peca[0]
        else:
            assert "agende" in botao, peca[0]


def test_ids_sao_unicos():
    ids = [p[0] for p in C.PECAS]
    assert len(ids) == len(set(ids))
    assert len(ids) == 20
