# -*- coding: utf-8 -*-
"""Cena de SHORT com layout que o retrato nao conhece sai em BRANCO.

MEDIDO em 19/10 as 19:1x, numa peca que eu publiquei QUARENTA MINUTOS antes: o
`epomeno-epipedo-s069` (`ZySLot-Cvo4`) tem a cena 1 com `layout: numero`, e o
`fabrica.svg_cena_retrato` despacha so `titulo`/`cta`, `item`, `lista` e
`barras`. A cena saiu com **146 bytes e ZERO `<text>`** — o retangulo do fundo e
mais nada —, contra 600 a 1.500 bytes e 2 a 5 `<text>` nas outras nove.

**E a classe esta escrita no `CLAUDE.md` desde 04:2x do mesmo dia**, nos layouts
de longo *"escritos e MORTOS"*: cena que cai no ramo final e sai como fundo
vazio, sem erro e sem aviso. La o render nao chamava o codigo; aqui eu chamei um
layout que o render do SHORT nao conhece. **A diferenca pratica e nenhuma.**

**Por que isto virou PORTAO e nao aviso de suite:** de 2.750 cenas de short no
disco exatamente UMA reprova, e e a que eu quebrei nesta hora. O argumento do
`mira.py` — aviso que reprova o acervo deixa de avisar — nao se aplica quando o
aviso reprova so o defeito.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import layouts_do_short as LS  # noqa: E402
import prontidao  # noqa: E402


def _specs():
    out = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if sp.get("short"):
            out.append((os.path.basename(p), sp))
    return out


def test_a_varredura_sai_do_DISCO_e_nao_pode_encolher():
    cenas = sum(len(sp["short"]) for _, sp in _specs())
    assert cenas >= 1000, (
        f"so {cenas} cenas de short no disco: a varredura deixou de medir o "
        "parque e os testes deste arquivo passariam por vacuidade")


def test_os_DOIS_lados_existem__layout_que_desenha_e_layout_que_NAO():
    """Se o retrato passar a desenhar tudo, esta nota se rele.

    Sem o lado que NAO desenha o instrumento nao guarda nada; sem o que
    desenha, ele reprovaria o short inteiro.
    """
    cands = LS.candidatos()
    bons = LS.desenham()
    assert bons, "o retrato nao desenha layout nenhum: a sonda quebrou"
    assert bons < cands, (
        "o retrato passou a desenhar TODOS os layouts candidatos "
        f"({sorted(cands)}) — o buraco fechou e esta nota tem de ser relida, "
        "nao reaproveitada")


def test_o_criterio_do_BRANCO_e_medido_e_nao_suposto():
    """O ramo final devolve so o fundo: sem `<text>` e muito menor."""
    import fabrica as F

    cena_boa = dict(LS.CENA_DE_SONDA, layout="item")
    svg_bom = F.svg_cena_retrato(cena_boa, LS.PALETA_DE_SONDA, 1080, 1920)
    fora = sorted(LS.candidatos() - LS.desenham())
    assert fora, "nenhum layout fora do despacho: nada a medir aqui"
    cena_ma = dict(LS.CENA_DE_SONDA, layout=fora[0])
    svg_mau = F.svg_cena_retrato(cena_ma, LS.PALETA_DE_SONDA, 1080, 1920)
    assert "<text" in svg_bom and "<text" not in svg_mau, (
        "o discriminador `<text>` deixou de separar os dois ramos")
    assert len(svg_mau) * 2 < len(svg_bom), (
        f"o SVG do ramo vazio ({len(svg_mau)} bytes) deixou de ser muito menor "
        f"que o que desenha ({len(svg_bom)}): o criterio tem de ser relido")


def test_CONTRAPROVA_a_MESMA_cena_com_layout_conhecido_NAO_e_acusada():
    fora = sorted(LS.candidatos() - LS.desenham())
    bom = sorted(LS.desenham())[0]
    sp_mau = {"short": [dict(LS.CENA_DE_SONDA, layout=fora[0])]}
    sp_bom = {"short": [dict(LS.CENA_DE_SONDA, layout=bom)]}
    assert LS.cenas_vazias(sp_mau) == [(0, fora[0])], (
        "o instrumento nao acusou a cena que sai em branco")
    assert LS.cenas_vazias(sp_bom) == [], (
        f"o instrumento acusou uma cena de layout {bom!r}, que DESENHA")


def test_o_PORTAO_reprova_a_cena_em_branco_e_passa_a_que_desenha():
    """A fiacao: o portao `layout` carrega o aviso, nos dois sentidos."""
    fora = sorted(LS.candidatos() - LS.desenham())
    base = {"slug": "sonda", "pacote": "sonda", "idioma": "pt-BR",
            "voz": "pt-BR-ThalitaMultilingualNeural", "longo": [],
            "paleta": LS.PALETA_DE_SONDA}
    mau = dict(base, short=[dict(LS.CENA_DE_SONDA, layout=fora[0])])
    bom = dict(base, short=[dict(LS.CENA_DE_SONDA, layout="item")])
    msgs_mau = prontidao._gate_layout(mau)
    msgs_bom = prontidao._gate_layout(bom)
    assert any("CARTAO EM BRANCO" in m for m in msgs_mau), (
        f"o portao `layout` nao reprovou a cena em branco: {msgs_mau}")
    assert not any("CARTAO EM BRANCO" in m for m in msgs_bom), (
        f"o portao `layout` acusou uma cena que desenha: {msgs_bom}")


def test_o_portao_e_o_instrumento_CONCORDAM_em_toda_spec_do_disco():
    """Fiacao cobrada por PROPRIEDADE, nao pelo nome de uma spec.

    Nomear a `s069` seria identidade onde ha propriedade (743/753/761, OITAVA
    vez). O que vale e: o portao acusa exatamente as specs que o instrumento
    aponta — e isso continua verdadeiro se eu consertar a `s069`.
    """
    todas = _specs()
    # O `_gate_layout` tambem roda o `layout.analisa`, que RENDERIZA — logo ele
    # e caro e a varredura aqui e por AMOSTRA, com os dois lados garantidos:
    # as specs que o instrumento acusa, mais algumas que ele nao acusa.
    acusadas = [(n, s) for n, s in todas if LS.cenas_vazias(s)]
    limpas = [(n, s) for n, s in todas if not LS.cenas_vazias(s)][:4]
    assert limpas, "nenhuma spec limpa: o lado negativo da amostra sumiu"
    for nome, sp in acusadas + limpas:
        esperado = bool(LS.cenas_vazias(sp))
        msgs = prontidao._gate_layout(sp)
        acusou = any("CARTAO EM BRANCO" in m for m in msgs)
        assert acusou == esperado, (
            f"{nome}: instrumento diz {esperado} e o portao diz {acusou}")


def test_o_conjunto_NAO_e_lista_escrita_a_mao():
    """Lista cravada aqui seria um SEGUNDO dono do despacho.

    Por AST, porque o docstring do modulo CITA os quatro nomes numa tabela
    para se explicar, e casar prosa pegaria a explicacao em vez do codigo.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "layouts_do_short.py"),
                 encoding="utf-8").read()
    arv = ast.parse(fonte)
    alvo = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)
            and n.name == "desenham"]
    assert alvo, "`desenham` desapareceu do modulo"
    corpo = ast.unparse(alvo[0])
    chamadas = [ast.unparse(c.func) for c in ast.walk(alvo[0])
                if isinstance(c, ast.Call)]
    assert any("svg_cena_retrato" in c for c in chamadas), (
        f"`desenham` deixou de SONDAR o render: chama {chamadas}")
    for nome in ("'titulo'", '"titulo"', "'item'", '"item"', "'lista'",
                 '"lista"', "'barras'", '"barras"'):
        assert nome not in corpo, (
            f"{nome} cravado dentro de `desenham`: o conjunto voltou a ser "
            "uma lista escrita, que e o segundo dono do despacho")


def test_a_sonda_entrega_TODOS_os_campos():
    """Senao ela confunde "nao desenha" com "faltou o campo"."""
    campos = set(LS.CENA_DE_SONDA)
    for exigido in ("kicker", "sub", "preco", "itens", "barras", "nar"):
        assert exigido in campos, (
            f"a cena de sonda perdeu o campo {exigido!r}: um layout que dependa "
            "dele passaria a contar como 'nao desenha'")


def test_o_MOTIVO_continua_escrito_nos_DOIS_lugares():
    """Conserto sem motivo escrito volta calado."""
    mod = open(os.path.join(RAIZ, "fabrica", "layouts_do_short.py"),
               encoding="utf-8").read()
    pront = open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                 encoding="utf-8").read()
    for marca in ("epomeno-epipedo-s069", "mira.py", "2.750"):
        assert marca in mod, f"{marca!r} saiu do `layouts_do_short.py`"
    assert "layouts_do_short" in pront, (
        "o `prontidao` deixou de chamar o instrumento: o portao voltou a nao "
        "cobrar a cena em branco")
