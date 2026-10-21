# -*- coding: utf-8 -*-
"""O guarda que ENCOLHE texto estimava largura por CONTAGEM — 21/10 as 14:3x.

O `fabrica.corpo_que_cabe` e quem evita que texto estoure a zona segura: ele
devolve o maior corpo em que a linha mais larga cabe. Ate aqui ele estimava essa
largura como `caracteres * LARGURA_GLIFO`, uma razao MEDIA — e o medidor de
verdade, `fabrica.largura_do_texto`, vive no MESMO arquivo trinta linhas abaixo,
com o docstring DELE dizendo desde 18/08/2026 que a razao real *"varia por um
fator de tres"*. Dois donos da pergunta "quanto este texto mede", e o guarda
usava o velho.

**Quem pegou foi o portao, nesta rodada:** o kicker `Maksimum` do
`kolejny-poziom-s087` pediu corpo 162, o guarda APROVOU, e a largura medida deu
956 px contra 820 da zona segura — 1,12% de tinta na borda.

A forma destes testes: tudo sai do DISCO, os dois numeros sao RECONFERIDOS (753)
e a correcao da minha propria medida fica travada, porque ela era comparador
escolhido sem olhar.
"""
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import fabrica as F  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
W = 1080                      # o retrato da producao
SEG = W * F.LARGURA_SEGURA


def _corpo_pedido(t):
    """O degrau que o `svg_cena_retrato` pede para `titulo`/`cta`.

    Ele e por CONTAGEM de caracteres (0,15W ate oito, 0,10W depois), e e isso
    que torna o guarda indispensavel: oito caracteres LARGOS pedem o corpo
    grande.
    """
    return W * (0.15 if len(t) <= 8 else 0.10)


def _kickers():
    saida = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for c in d.get("short") or []:
            if c.get("layout") not in ("titulo", "cta"):
                continue
            t = c.get("kicker") or ""
            if t:
                saida.append((os.path.basename(f)[:-5], t))
    return saida


def test_a_varredura_nao_e_vacua():
    k = _kickers()
    assert len(k) >= 500, (
        "so %d cena(s) titulo/cta com kicker no disco: os testes abaixo"
        " passariam por vacuidade" % len(k))


def test_o_guarda_LE_o_medidor_e_nao_a_media():
    """O caso MEDIDO desta rodada: `Maksimum` tem de encolher."""
    t = "Maksimum"
    pedido = _corpo_pedido(t)
    assert F.largura_do_texto(t, pedido) > SEG, (
        "PERDEU A ANCORA: `Maksimum` no corpo %.0f ja nao excede a zona segura,"
        " logo o caso que produziu o conserto deixou de existir" % pedido)
    corpo = F.corpo_que_cabe(t, 11, pedido, SEG)
    assert corpo < pedido, (
        "o guarda NAO encolheu: devolveu %.1f para um texto que mede %.0f px"
        " contra %.0f da zona segura"
        % (corpo, F.largura_do_texto(t, pedido), SEG))
    assert F.largura_do_texto(t, corpo) <= SEG + 1, (
        "ele encolheu e ainda nao cabe: %.0f px contra %.0f"
        % (F.largura_do_texto(t, corpo), SEG))


def test_o_estimador_velho_ERRAVA_neste_caso():
    """Sem isto, 'o estimador velho errava' seria afirmacao minha, nao medida."""
    t = "Maksimum"
    pedido = _corpo_pedido(t)
    maior = max(len(l) for l in F.wrap(t, 11))
    velho = min(pedido, SEG / (maior * F.LARGURA_GLIFO))
    assert velho >= pedido - 0.5, (
        "o estimador por contagem nao aprovava o corpo cheio aqui, logo este"
        " arquivo nao mede o defeito que o produziu")
    assert F.largura_do_texto(t, velho) > SEG, (
        "o corpo que o estimador velho aprovava CABE pela medida: o defeito"
        " desapareceu e esta nota tem de ser relida")


def test_contraprova_no_outro_sentido_texto_estreito_NAO_encolhe():
    """Se ele encolhesse tudo, 'ele encolhe o que nao cabe' nao diria nada."""
    t = "Wybór"
    pedido = _corpo_pedido(t)
    assert F.largura_do_texto(t, pedido) <= SEG, (
        "a ancora estreita escolhida ja nao cabe: troque o exemplo")
    assert F.corpo_que_cabe(t, 11, pedido, SEG) == pedido, (
        "o guarda encolheu texto que CABE: ele passou a reprovar por"
        " construcao, e ai nao discrimina nada")


def test_a_largura_e_medida_LINHA_a_linha_e_nao_no_texto_corrido():
    """A correcao da MINHA medida: o render quebra por espaco e desenha linhas.

    Medir a string inteira numa linha deu 849 cenas 'excedidas'; com a quebra
    sao 90. Este teste trava os DOIS numeros contra o disco, para que a
    retratacao nao se perca e para que nenhum dos dois envelheca calado (753).
    """
    corrido = quebrado = 0
    for _, t in _kickers():
        pedido = _corpo_pedido(t)
        if F.largura_do_texto(t, pedido) > SEG:
            corrido += 1
        linhas = [l for l in F.wrap(t, 11) if l]
        if linhas and max(F.largura_do_texto(l, pedido)
                          for l in linhas) > SEG:
            quebrado += 1
    assert quebrado < corrido, (
        "medir por LINHA deixou de dar menos que medir o texto corrido"
        " (%d contra %d): a diferenca que a retratacao descreve desapareceu"
        % (quebrado, corrido))
    assert 40 <= quebrado <= 200, (
        "o numero de cenas que o conserto encolhe saiu da faixa observada"
        " (%d, medido 90): reconfira e atualize a nota no `fabrica.py`"
        % quebrado)
    fonte = open(os.path.join(RAIZ, "fabrica", "fabrica.py"),
                 encoding="utf-8").read()
    assert "849" in fonte and "efeito C" in fonte, (
        "a retratacao da minha primeira medida saiu do modulo: sem ela a"
        " rodada seguinte repete o numero errado")


def test_o_guarda_nunca_AUMENTA_o_corpo():
    """`min(size, ...)` e o que impede o conserto de inflar texto que cabe."""
    for _, t in _kickers()[:400]:
        pedido = _corpo_pedido(t)
        assert F.corpo_que_cabe(t, 11, pedido, SEG) <= pedido + 1e-9, (
            "o guarda devolveu corpo MAIOR que o pedido em %r" % t)


def test_o_ramo_degenerado_devolve_o_corpo_e_nao_zero():
    """Largura ou corpo invalidos: devolver zero apagaria o texto."""
    assert F.corpo_que_cabe("abc", 11, 100, 0) == 100
    assert F.corpo_que_cabe("", 11, 100, SEG) == 100
    assert F.corpo_que_cabe("abc", 11, 0, SEG) == 0


def test_o_motivo_e_a_procedencia_continuam_escritos():
    fonte = open(os.path.join(RAIZ, "fabrica", "fabrica.py"),
                 encoding="utf-8").read()
    assert "largura_do_texto" in fonte.split("def texto_na_caixa")[0], (
        "o `corpo_que_cabe` deixou de citar o medidor")
    assert "kolejny-poziom-s087" in fonte, (
        "a peca que produziu o achado saiu do modulo")
    assert "fator de tres" in fonte, (
        "a razao pela qual a media nao serve — o docstring do medidor diz que"
        " ela varia por um fator de tres — saiu do modulo")
