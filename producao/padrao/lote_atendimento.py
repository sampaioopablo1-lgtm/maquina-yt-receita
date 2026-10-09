# -*- coding: utf-8 -*-
"""Lote 2 — atendimento de lead. Vinte pecas, quatro formatos.

POR QUE QUATRO FORMATOS E NAO UM. O lote inteiro sai no mesmo dia, para os
mesmos conjuntos. Vinte variacoes de um layout so e o defeito que a LISTA
catalogou em seis nichos seguidos (Fisio Nova com 11 anuncios iguais, WGP Fight
Gym com 10, Oticas Lillo com 6). Formato diferente disputa atencao de um jeito
diferente no mesmo feed.

DOIS FORMATOS VEM DO PADRAO (`padrao.py`): `agenda` e `pergunta`.
DOIS NASCEM AQUI, porque as copies deste lote pedem imagem que argumenta:
  - `relogio`  — a janela de tempo. O numero grande E o argumento.
  - `contagem` — vinte leads desenhados, poucos atendidos. A conta aparece
                 antes de a pessoa ler a frase.

SEM FOTO DE BANCO NESTE LOTE. Ordem do Pablo em 23/09: nada artificial ou
ficticio que gere estranheza. Foto posada de "empresario sorrindo apontando
para grafico" e exatamente isso. Tipografia e diagrama nao correm esse risco —
e o diagrama ainda carrega a mensagem, que foto de banco nao faz.

Uso (a partir da raiz do repo, que e onde ficam as fontes):
    ./producao/padrao/fontes.sh
    python3 producao/padrao/lote_atendimento.py --saida /caminho/de/saida
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw  # noqa: E402

from padrao import (  # noqa: E402
    L, A, MARGEM, TETO_DE_TEXTO,
    LARANJA, LARANJA_ESCURO, GRAFITE, CREME, BRANCO,
    MONT, PLAY,
    fonte, _pct, _rodape, _bloco,
    agenda, pergunta,
)


# ─────────────────────────────────────────────────────────────────────
# FORMATO 4 — RELOGIO. A janela de tempo desenhada. O numero ocupa o
# terco de cima inteiro: no feed, numero grande para o dedo antes de a
# frase ser lida. O anel mostra quanto da janela ja passou.
# ─────────────────────────────────────────────────────────────────────
def relogio(numero, unidade, chamada, apoio, kicker="A JANELA", fatia=0.82):
    im = Image.new("RGB", (L, A), GRAFITE)
    d = ImageDraw.Draw(im)
    cx = []

    f_k = fonte(MONT, 30, "Bold")
    d.text((MARGEM, 96), kicker, font=f_k, fill=LARANJA)
    cx.append(f_k.getbbox(kicker))

    # anel: o quanto da janela ja foi embora
    cxr, cyr, raio, grossura = L // 2, 430, 190, 22
    caixa = [cxr - raio, cyr - raio, cxr + raio, cyr + raio]
    d.arc(caixa, 0, 360, fill=(40, 45, 54), width=grossura)
    d.arc(caixa, -90, -90 + int(360 * fatia), fill=LARANJA, width=grossura)

    f_n = fonte(MONT, 176, "Black")
    bb = d.textbbox((0, 0), numero, font=f_n)
    d.text((cxr - (bb[2] - bb[0]) // 2, cyr - (bb[3] - bb[1]) // 2 - 30),
           numero, font=f_n, fill=BRANCO)
    cx.append((0, 0, bb[2] - bb[0], bb[3] - bb[1]))

    # O rotulo vai ABAIXO do anel, nunca dentro: dentro ele cruza o traco
    # e fica ilegivel — foi o defeito da primeira geracao deste lote.
    f_u = fonte(MONT, 30, "SemiBold")
    bu = d.textbbox((0, 0), unidade, font=f_u)
    d.text((cxr - (bu[2] - bu[0]) // 2, cyr + raio + 44), unidade,
           font=f_u, fill=(150, 157, 170))
    cx.append((0, 0, bu[2] - bu[0], bu[3] - bu[1]))

    y = _bloco(d, cx, chamada, 782, L - 160, 54, 84, 18)
    f_ap = fonte(MONT, 32, "Medium")
    for i, linha in enumerate(apoio):
        d.text((MARGEM, y + 26 + i * 44), linha, font=f_ap, fill=(150, 157, 170))
        cx.append(f_ap.getbbox(linha))
    _rodape(d, cx, BRANCO, (52, 58, 68))
    return im, _pct(cx)


# ─────────────────────────────────────────────────────────────────────
# FORMATO 5 — CONTAGEM. Vinte quadrados = vinte leads. Os preenchidos
# foram atendidos; os vazios ninguem tocou. A conta fica visivel antes
# de a frase ser lida, que e o oposto do anuncio que explica primeiro.
# ─────────────────────────────────────────────────────────────────────
def contagem(atendidos, total, chamada, apoio, kicker="SEUS ÚLTIMOS LEADS",
             rotulo_cheio="atendido", rotulo_vazio="ninguém ligou"):
    im = Image.new("RGB", (L, A), CREME)
    d = ImageDraw.Draw(im)
    cx = []

    d.rectangle([MARGEM, 120, MARGEM + 96, 130], fill=LARANJA_ESCURO)
    f_k = fonte(MONT, 28, "Bold")
    d.text((MARGEM, 170), kicker, font=f_k, fill=(138, 132, 120))
    cx.append(f_k.getbbox(kicker))

    # A grade se ajusta ao total: dez leads ou trinta cabem na MESMA faixa.
    # Sem isso, trinta quadrados de 150px empurram a manchete para fora do
    # quadro — foi o que aconteceu na primeira geração deste lote.
    colunas, gap = (5 if total <= 20 else 6), 20
    y0, faixa = 250, 630
    linhas_grade = (total + colunas - 1) // colunas
    lado_largura = (L - 2 * MARGEM - (colunas - 1) * gap) // colunas
    lado_altura = (faixa - (linhas_grade - 1) * gap) // linhas_grade
    lado = min(lado_largura, lado_altura)
    x0 = MARGEM
    raio = max(6, lado // 12)
    for i in range(total):
        col, lin = i % colunas, i // colunas
        x = x0 + col * (lado + gap)
        y = y0 + lin * (lado + gap)
        if i < atendidos:
            d.rounded_rectangle([x, y, x + lado, y + lado], raio, fill=LARANJA_ESCURO)
        else:
            d.rounded_rectangle([x, y, x + lado, y + lado], raio,
                                outline=(210, 205, 196), width=3)

    y_leg = y0 + linhas_grade * lado + (linhas_grade - 1) * gap + 30
    f_l = fonte(MONT, 24, "SemiBold")
    d.rounded_rectangle([MARGEM, y_leg + 4, MARGEM + 22, y_leg + 26], 5, fill=LARANJA_ESCURO)
    t1 = f"{atendidos} {rotulo_cheio}"
    d.text((MARGEM + 34, y_leg), t1, font=f_l, fill=(96, 92, 86))
    cx.append(f_l.getbbox(t1))
    d.rounded_rectangle([MARGEM + 300, y_leg + 4, MARGEM + 322, y_leg + 26], 5,
                        outline=(200, 195, 186), width=3)
    t2 = f"{total - atendidos} {rotulo_vazio}"
    d.text((MARGEM + 334, y_leg), t2, font=f_l, fill=(96, 92, 86))
    cx.append(f_l.getbbox(t2))

    y = _bloco(d, cx, chamada, y_leg + 88, L - 160, 54, 86, 18)
    f_ap = fonte(MONT, 30, "Medium")
    for i, linha in enumerate(apoio):
        d.text((MARGEM, y + 24 + i * 42), linha, font=f_ap, fill=(96, 92, 86))
        cx.append(f_ap.getbbox(linha))
    _rodape(d, cx, (24, 24, 26), (206, 202, 194))
    return im, _pct(cx)


# ─────────────────────────────────────────────────────────────────────
# AS VINTE PECAS. Cada uma sai de um dos dez roteiros; duas por roteiro,
# em formatos diferentes, para o par nunca se parecer no feed.
# ─────────────────────────────────────────────────────────────────────
PECAS = [
    # ---- roteiro 01 — a janela de 5 minutos
    ("A01_cinco_minutos", relogio, (
        "5", "MINUTOS DE VALIDADE",
        [("Depois disso,", MONT, BRANCO, "Bold"),
         ("ele já esqueceu.", PLAY, LARANJA, "Bold")],
        ["O lead que espera uma hora", "vira número na planilha."],
        "A JANELA", 0.88)),
    ("A02_ligou_no_dia_seguinte", pergunta, (
        [("Ligou no dia seguinte?", MONT, GRAFITE, "Bold"),
         ("Então já era.", PLAY, LARANJA_ESCURO, "Bold")],
        ["A pessoa preencheu com a carteira aberta.", "Uma hora depois nem lembra."],
        "QUEM ANUNCIA E ESPERA")),

    # ---- roteiro 02 — ninguém ligou
    ("A03_vinte_leads", contagem, (
        4, 20,
        [("Vinte leads.", MONT, GRAFITE, "Bold"),
         ("Quatro ligações.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Você pagou pelos vinte."],
        "SEUS ÚLTIMOS LEADS", "receberam ligação", "ninguém ligou")),
    ("A04_ligacao_nao_mensagem", pergunta, (
        [("Quantos receberam", MONT, GRAFITE, "Bold"),
         ("uma ligação?", PLAY, LARANJA_ESCURO, "Bold")],
        ["Não mensagem. Ligação.", "Se você não sabe, já é a resposta."],
        "DONO DE EMPRESA")),

    # ---- roteiro 03 — a meta
    ("A05_entrou_trinta", contagem, (
        8, 30,
        [("Entrou trinta.", MONT, GRAFITE, "Bold"),
         ("Falaram com oito.", PLAY, LARANJA_ESCURO, "Bold")],
        ["A meta não caiu por falta de lead."],
        "O MÊS QUE NÃO BATEU", "atendidos", "parados")),
    ("A06_investir_mais", pergunta, (
        [("Investir mais não", MONT, GRAFITE, "Bold"),
         ("conserta cano furado.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Mais verba com o mesmo atendimento", "é mais lead parado, mais caro."],
        "ANTES DE AUMENTAR A VERBA")),

    # ---- roteiro 04 — WhatsApp entupido
    ("A07_quarenta_conversas", contagem, (
        3, 20,
        [("O cliente bom está", MONT, GRAFITE, "Bold"),
         ("no meio da fila.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Junto com dezessete curiosos."],
        "SEU WHATSAPP AGORA", "vale a pena", "curiosos")),
    ("A08_curioso_ocupa_lugar", pergunta, (
        [("Curioso ocupa o", MONT, GRAFITE, "Bold"),
         ("lugar do cliente.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Mesma lista, mesma fila,", "e o seu vendedor sem saber qual é qual."],
        "MICRO-DOR DE TODO DIA")),

    # ---- roteiro 05 — controle
    ("A09_quantas_ligacoes", pergunta, (
        [("Quantas ligações por lead", MONT, GRAFITE, "Bold"),
         ("o seu time faz?", PLAY, LARANJA_ESCURO, "Bold")],
        ["Não quantas deveria.", "Quantas fez ontem."],
        "PERGUNTA DIFÍCIL")),
    ("A10_uma_tentativa", relogio, (
        "1", "TENTATIVA POR LEAD",
        [("Uma tentativa", MONT, BRANCO, "Bold"),
         ("não é atendimento.", PLAY, LARANJA, "Bold")],
        ["É sorte. E sorte não entra", "no relatório do mês."],
        "SEM MEDIÇÃO", 0.2)),

    # ---- roteiro 06 — o dinheiro
    ("A11_cem_leads_um_cliente", contagem, (
        1, 20,
        [("Cem leads.", MONT, GRAFITE, "Bold"),
         ("Um cliente.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Você não pagou por lead.", "Pagou por esse um."],
        "A CONTA QUE NINGUÉM FAZ", "fechou", "não fecharam")),
    ("A12_perde_depois", pergunta, (
        [("Você não perde no anúncio.", MONT, GRAFITE, "Bold"),
         ("Perde depois dele.", PLAY, LARANJA_ESCURO, "Bold")],
        ["O painel para onde começa", "o seu comercial."],
        "PARA QUEM JÁ INVESTE")),

    # ---- roteiro 07 — a oferta
    ("A13_planilha_ou_reuniao", agenda, (
        [("Planilha de nomes", MONT, BRANCO, "Bold"),
         ("ou agenda cheia?", PLAY, LARANJA, "Bold")],
        "A gente entrega a segunda.",
        "O QUE VOCÊ RECEBE", ((0, 0), (1, 1), (2, 2), (3, 1), (4, 3), (0, 4)))),
    ("A14_gente_de_verdade", pergunta, (
        [("Não é robô mandando", MONT, GRAFITE, "Bold"),
         ("“oi, tudo bem?”.", PLAY, LARANJA_ESCURO, "Bold")],
        ["É gente ligando, entendendo", "e marcando na agenda do seu vendedor."],
        "COMO A GENTE ATENDE")),

    # ---- roteiro 08 — fora do horário
    ("A15_dezoito_acumulados", contagem, (
        0, 18,
        [("Segunda, nove da manhã.", MONT, GRAFITE, "Bold"),
         ("Dezoito esperando.", PLAY, LARANJA_ESCURO, "Bold")],
        ["Metade já falou com o concorrente."],
        "CHEGARAM NO FIM DE SEMANA", "atendidos", "esperando")),
    ("A16_sabado_de_manha", relogio, (
        "48", "HORAS FECHADO",
        [("Seu cliente pesquisa", MONT, BRANCO, "Bold"),
         ("sábado de manhã.", PLAY, LARANJA, "Bold")],
        ["E é aí que a sua", "empresa está fechada."],
        "FORA DO HORÁRIO", 1.0)),

    # ---- roteiro 09 — agenda vs caixa
    ("A17_agenda_cheia", agenda, (
        [("Caixa cheia dá", MONT, BRANCO, "Bold"),
         ("sensação. Agenda paga.", PLAY, LARANJA, "Bold")],
        "Duas empresas, mesma verba.",
        "A DIFERENÇA REAL", ((0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 4), (3, 2), (4, 1), (4, 3)))),
    ("A18_movimento_nao_paga", pergunta, (
        [("Movimento não", MONT, GRAFITE, "Bold"),
         ("paga conta.", PLAY, LARANJA_ESCURO, "Bold")],
        ["O que paga é alguém sentado", "na frente do seu vendedor."],
        "DONO DE EMPRESA")),

    # ---- roteiro 10 — o relatório
    ("A19_relatorio_bonito", pergunta, (
        [("Relatório bonito,", MONT, GRAFITE, "Bold"),
         ("caixa que não bate.", PLAY, LARANJA_ESCURO, "Bold")],
        ["“Lead gerado” é o trabalho da agência", "terminando. Não o seu começando."],
        "TODO FIM DE MÊS")),
    ("A20_numero_que_importa", contagem, (
        2, 10,
        [("De cada dez leads,", MONT, GRAFITE, "Bold"),
         ("quantos viraram reunião?", PLAY, LARANJA_ESCURO, "Bold")],
        ["É esse número que a gente entrega."],
        "O NÚMERO QUE VOCÊ NÃO VÊ", "viraram reunião", "sumiram")),
]


def monta(pecas, saida):
    os.makedirs(saida, exist_ok=True)
    recusadas, feitas = [], []
    for nome, fn, args in pecas:
        im, pct = fn(*args)
        if pct > TETO_DE_TEXTO:
            recusadas.append((nome, pct))
            print(f"  {nome}: {pct:.1f}% — RECUSADA, encurte a chamada")
            continue
        caminho = os.path.join(saida, f"{nome}.jpg")
        im.save(caminho, quality=94)
        feitas.append((nome, pct))
        print(f"  {nome}: {pct:.1f}% de texto — ok")
    return feitas, recusadas


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--saida", default="entregas/campanha/imagens/lote-atendimento")
    a = p.parse_args()
    print(f"lote 2 — atendimento ({len(PECAS)} peças) → {a.saida}")
    feitas, recusadas = monta(PECAS, a.saida)
    print(f"\n{len(feitas)} salvas, {len(recusadas)} recusadas pelo teto de {TETO_DE_TEXTO}%")


if __name__ == "__main__":
    main()
