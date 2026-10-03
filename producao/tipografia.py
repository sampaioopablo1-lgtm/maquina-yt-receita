# -*- coding: utf-8 -*-
"""Piso de tamanho de letra, e quebra de linha em vez de encolhimento.

POR QUE ISTO EXISTE
O `cabe()` das primeiras versoes ia DIMINUINDO o corpo ate o texto caber numa
linha so. Parece razoavel e nao e: a promessa da mentoria tem 66 caracteres, e
para caber em 980 px numa linha ela precisava de 26 px de corpo. Resultado --
a frase mais importante da peca virou a menor letra do quadro, ilegivel no
feed. O Pablo viu isso na tela em 08/09/2026, depois de a versao anterior ja
ter passado no portao de area de 18-30%: area total nao mede legibilidade,
porque uma cursiva de 132 px e uma barra de CTA escondem qualquer letra miuda.

A regra agora e a inversa: LARGURA E NEGOCIAVEL, TAMANHO DE LETRA NAO E.
Se nao cabe, quebra em duas linhas. Se ainda nao cabe no piso, a peca reprova
e o texto precisa ser reescrito mais curto -- que e a decisao editorial certa,
nao um problema de layout.

PISOS, para quadro de 1080 px de largura visto no celular:
  34 px  o minimo absoluto (apoio, etiqueta, assinatura)
  42 px  promessa -- e mensagem central, nao pode ser a menor coisa do quadro
  48 px  barra de CTA
"""

PISO_APOIO = 34
PISO_PROMESSA = 42
PISO_CTA = 48


def quebrar(d, txt, f, larg):
    """Divide o texto em linhas que cabem em `larg`, SEM mexer no corpo."""
    linhas, atual = [], ""
    for palavra in txt.split():
        tentativa = (atual + " " + palavra).strip()
        if not atual or d.textlength(tentativa, font=f) <= larg:
            atual = tentativa
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def paragrafo(d, sentencas, y, larg, W, entre=8, entre_sent=10):
    """Desenha sentencas empilhadas e centradas.

    `sentencas` e uma lista de (texto, fonte, cor). Devolve (y_final, area),
    onde area soma a caixa de cada linha desenhada -- e o que entra na conta
    dos 18-30% de texto no quadro.
    """
    area = 0
    for k, (txt, f, cor) in enumerate(sentencas):
        for linha in quebrar(d, txt, f, larg):
            l, t, r, b = d.textbbox((0, 0), linha, font=f)
            x = (W - (r - l)) / 2 - l
            d.text((x + 2, y - t + 2), linha, font=f, fill=(0, 0, 0))
            d.text((x, y - t), linha, font=f, fill=cor)
            area += (r - l) * (b - t)
            y += (b - t) + entre
        y += entre_sent
    return y - entre - entre_sent, area
