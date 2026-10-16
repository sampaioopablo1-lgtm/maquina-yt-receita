"""O estilo de desenho que o dono trouxe em 16/10, virado em prompt POR CENA.

Ele colou um prompt de geracao de imagem — stickman de MS Paint, um quadro por
timestamp — e pediu para estudar. Estudado contra o codigo, e o que sai e isto.

O QUE O PROMPT DELE DESCREVE, e e preciso dizer: **video 16:9**. A linha "Every
image must be horizontal 16:9 (wide YouTube frame) — not vertical, not square"
e incompativel com o short 9:16 da maquina (`fabrica.svg_cena_retrato`), e
compativel com os LONGOS do canal. O ESTILO atravessa os dois formatos; o
ASPECTO nao. Entao aqui o aspecto vem do formato da peca, e isso vai declarado
em vez de copiado.

ONDE ISSO ENTRA SEM MEXER NO RENDER: a cena com `layout: "broll"` e
`broll_url` ja existe e e deliberadamente nao invasiva (`fabrica/broll.py`) —
se a imagem falhar, a cena cai no caminho de texto sobre fundo escuro e o render
NUNCA para por causa de enfeite. Logo imagem por cena e um passo NOVO que grava
`broll_url`, nao um render novo.

A REGRA QUE EU ACRESCENTO AO PROMPT DELE, e ela tem motivo medido: **a imagem
sai SEM TEXTO.** O prompt original admite texto escrito a mao ("Handwritten text
only when it helps explain the idea... it must be spelled correctly"). Dois
tercos da frota narram em GREGO e POLONES, e gerador de imagem erra diacritico —
enquanto o nosso texto e desenhado por `cairosvg` e sai sempre correto, e e ele
que os portoes `ortografia` e `variedade` conferem. Pedir texto na imagem
trocaria a unica parte que esta provada em tres idiomas por uma que nao esta.
Entao: desenho embaixo, texto nosso em cima.

CUSTO, medido em 16/10: **0,25 credito por imagem** (`gpt_image_2_5`, que e a
familia "GPT Image" que o proprio prompt nomeia). Short de dez cenas = 2,50;
peca de 2 min = 10,00; longo de ~9 min = 27,25. No alvo de 7 pecas/dia/canal dá
~52 cr/dia. **E o saldo medido era ZERO, em plano free, sem cota gratuita** —
logo nem uma imagem de teste sai hoje. Isto esta na fila do dono.
"""
from __future__ import annotations

# Bloco de estilo, condensado do prompt do dono. O que ele PROIBE vale tanto
# quanto o que ele pede: e a proibicao que impede o gerador de "melhorar" o
# desenho e perder o ponto.
ESTILO = (
    "extremely simple beginner drawing made in MS Paint, as if drawn quickly by "
    "hand by someone bad at drawing. Stickman / childish style: white "
    "background, thick uneven black outlines, wobbly hand-drawn lines, stick "
    "figure humans with round heads and line bodies, simple dot eyes, very "
    "basic facial expressions, flat colors only. Objects built from basic "
    "shapes: squares, circles, rectangles, arrows, simple tables, boxes, signs, "
    "screens, question marks. Mostly white empty space. Occasional flat colors: "
    "green, brown, gray, red, yellow, orange, blue. Red arrows or red question "
    "marks when they help. Clear, simple, centered composition with space "
    "around the objects."
)

PROIBIDO = (
    "no realistic shading, no 3D, no cinematic lighting, no realistic cartoon "
    "style, no Disney style, no anime style, no polished illustration, no "
    "professional vector art, no highly detailed background, no complex "
    "texture, no realistic humans. Do not make it look good or professional: "
    "amateur, funny and intentionally bad is the point. No glitches, no broken "
    "anatomy, no messy overlapping objects."
)

# A regra da casa, e ela NAO e do prompt dele: nada de texto na imagem.
SEM_TEXTO = (
    "Absolutely no text, no letters, no numbers, no captions and no labels "
    "anywhere in the image."
)

# Aspecto por formato da peca. O prompt dele diz 16:9 porque descreve o LONGO.
ASPECTO = {"short": "9:16", "longo": "16:9"}

MODELO = "gpt_image_2_5"
CREDITO_POR_IMAGEM = 0.25


def aspecto_da_peca(sp: dict) -> str:
    """9:16 quando a spec e short solto; 16:9 quando tem longo."""
    return ASPECTO["longo"] if (sp or {}).get("longo") else ASPECTO["short"]


def prompt_da_cena(cena: dict, sp: dict = None, cena_em: str = None) -> str:
    """O prompt de UMA cena, a partir do que o narrador diz nela.

    Levanta quando a cena nao tem narracao: imagem que nao ilustra a fala e
    exatamente o "random image" que o prompt do dono proibe.
    """
    nar = (cena or {}).get("nar", "").strip()
    if not nar:
        raise ValueError(
            "cena sem `nar`: nao da para ilustrar o que o narrador diz, e"
            " imagem solta e o 'random image' que o prompt proibe"
        )
    ideia = nar.rstrip(".!?;")
    quando = f" (momento {cena_em})" if cena_em else ""
    return (
        f"A single simple drawing that illustrates this idea{quando}: "
        f"\"{ideia}\". {ESTILO} {PROIBIDO} {SEM_TEXTO}"
    )


def prompts_da_spec(sp: dict, chave: str = "short") -> list[dict]:
    """Um pedido por cena, com indice estavel — a forma do `generate_image_batch`."""
    cenas = (sp or {}).get(chave) or []
    asp = aspecto_da_peca(sp)
    saida = []
    for i, c in enumerate(cenas):
        saida.append({
            "index": i,
            "params": {
                "model": MODELO,
                "aspect_ratio": asp,
                "prompt": prompt_da_cena(c, sp, cena_em=f"{i + 1}/{len(cenas)}"),
            },
        })
    return saida


def custo(sp: dict, chave: str = "short") -> float:
    return len((sp or {}).get(chave) or []) * CREDITO_POR_IMAGEM


def relato(sp: dict, chave: str = "short") -> str:
    cenas = (sp or {}).get(chave) or []
    asp = aspecto_da_peca(sp)
    return (
        f"ESTILO PAINT: {len(cenas)} cenas -> {len(cenas)} imagens em {asp}, "
        f"{custo(sp, chave):.2f} credito ({MODELO}).\n"
        "  o desenho sai SEM TEXTO e o texto continua sendo o nosso "
        "(`cairosvg`), porque gerador erra diacritico em grego e polones.\n"
        "  cada cena grava `broll_url`; se a imagem faltar, o render cai no "
        "caminho de texto e NAO para (`fabrica/broll.py`)."
    )
