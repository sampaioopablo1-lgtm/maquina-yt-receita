"""O Ken Burns tem de ANDAR, e nao travar e saltar.

Pablo assistiu aos videos publicados e disse "imagens tremendo". Nao era
impressao: o `zoompan` do ffmpeg avalia x e y por quadro e ARREDONDA PARA PIXEL
INTEIRO. Com AMP_ZOOM 0,12 e AMP_PAN 0,5 o pan anda de 0,13 a 0,53 px por quadro
sobre um quadro de 1280 — sempre menos de um pixel. A imagem fica parada de dois
a oito quadros e entao salta 1px de uma vez.

MEDIDO em 17/08/2026 numa cena `lista` de quatro itens com camadas, quarenta
quadros, contando os praticamente identicos ao anterior:

    variante                              travados   desvio   custo/clipe
    antes: overlay 1x -> 960x540           8 de 39    0,476       9,3 s
    depois: ampliar 2x antes do zoompan    0 de 39    0,271      11,7 s

Estes testes olham a GEOMETRIA do movimento e a forma do filtro, nao pixel de
video: rodam em milissegundos e continuam valendo para spec que nao existe.
"""

import os
import sys
import types

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import fabrica as F  # noqa: E402


def avanco_por_quadro(largura, nf, i=0):
    """Quantos pixels da FONTE o recorte anda entre dois quadros."""
    def x(on):
        zoom = 1 + F.AMP_ZOOM * (on / nf)
        frac = (1 - F.AMP_PAN) / 2 + F.AMP_PAN * (on / nf)
        return (largura - largura / zoom) * frac
    return [x(n + 1) - x(n) for n in range(nf)]


def test_o_pan_anda_menos_de_um_pixel_por_quadro():
    """O defeito raiz, explicito. Nao e um bug do calculo — e a consequencia
    de um movimento lento sobre uma grade inteira, e por isso a correcao NAO
    esta em mudar a amplitude."""
    d = avanco_por_quadro(1280, 300)
    assert max(d) < 1.0, f"maior avanco {max(d):.3f}px"


def test_ampliar_poe_o_avanco_acima_de_um_pixel():
    """Com SUAVIZA a mesma cena anda mais de 1px por quadro na grade que o
    zoompan enxerga — e so ai o arredondamento para de travar a imagem."""
    d = avanco_por_quadro(1280 * F.SUAVIZA, 300)
    assert min(d) > 0.25, f"menor avanco {min(d):.3f}px"
    assert max(d) > 1.0


def test_suaviza_vale_pelo_menos_dois():
    """Abaixo de 2 o travamento volta: foi medido em 1x com 8 quadros travados
    de 39."""
    assert F.SUAVIZA >= 2


# --- a forma do filtro -------------------------------------------------------

@pytest.mark.parametrize("n_camadas", [0, 1, 4])
def test_todo_zoompan_vem_depois_de_um_scale(n_camadas):
    """Um zoompan sem o scale na frente e um clipe que treme. Sao quatro pontos
    no arquivo e e facil acrescentar um quinto sem lembrar deste."""
    f = F.filtro_camadas(n_camadas, 10.0, 0, 300, 1280, 720)
    assert "zoompan" in f
    antes = f.split("zoompan")[0]
    assert f"scale=iw*{F.SUAVIZA}:ih*{F.SUAVIZA}" in antes, f


def test_nenhum_zoompan_no_codigo_fica_sem_scale():
    """Varre o fonte: todo `zoompan=` tem de ter um `scale=iw*SUAVIZA` colado
    antes dele, na mesma expressao de filtro."""
    fonte = open(os.path.join(RAIZ, "fabrica", "fabrica.py"), encoding="utf-8").read()
    pedacos = fonte.split("zoompan=z=")
    assert len(pedacos) - 1 >= 4, "esperava ao menos quatro zoompan"
    for antes in pedacos[:-1]:
        # a ampliacao pode estar na linha anterior da mesma f-string
        assert "scale=iw*{SUAVIZA}:ih*{SUAVIZA}" in antes[-400:], antes[-200:]


# --- resolucao de saida ------------------------------------------------------

def test_render_sai_em_hd_sem_upscale():
    """ESCALA_RENDER era 0,75: o clipe saia em 960x540 e o concat ampliava para
    1280x720. Texto fino ampliado sai borrado, e isso somava ao tremor."""
    assert F.render_wh(1280, 720) == (1280, 720)
    assert F.render_wh(720, 1280) == (720, 1280)


def test_a_escala_de_render_nao_encolhe():
    assert F.ESCALA_RENDER >= 1.0


# --- o deslize das camadas ---------------------------------------------------

def test_deslize_nao_escala_com_suaviza():
    """`SUAVIZA` amplia DEPOIS dos overlays, entao o deslize continua em pixels
    da resolucao de composicao. Se um dia a ampliacao mudar de lugar, este teste
    e o lembrete de que o deslize muda junto."""
    f = F.filtro_camadas(1, 10.0, 0, 300, 1280, 720)
    assert f"{F.DESLIZE}*max(" in f
    # e a ampliacao vem depois do ultimo overlay
    assert f.index("overlay") < f.index("scale=iw*")
