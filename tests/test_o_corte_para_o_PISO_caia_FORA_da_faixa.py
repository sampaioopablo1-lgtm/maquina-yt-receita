# -*- coding: utf-8 -*-
"""O corte para o PISO caia FORA da faixa — 21/10 as 16:3x.

O `mira.quanto_cortar`, escrito em 20/10, devolvia o valor CRU do inversor. E o
inversor, por forma, devolve o MAIOR numero de caracteres cuja previsao e <= o
alvo — logo, perguntado pelo PISO, ele entrega o ultimo valor de BAIXO dele.

**A medida ja estava escrita duas funcoes adiante:** o relato imprime
*"perguntado pelo piso ele responde com um valor cuja previsao cai ABAIXO dele
(54 de 54 pares)"*, e usa o `janela_do_mundo` para o piso EXECUTAVEL. O
`quanto_cortar` nao o chamava: dois donos de "quantos caracteres para o piso", e
o conselho vinha do lado errado.

**O custo foi medido na peca desta rodada:** o `epomeno-epipedo-s087` saiu em
42,4, o metodo pediu -26 caracteres, cortar os 26 entregou **40,6 — abaixo do
piso de 41,5** — e a terceira passada devolveu dez. Tres builds por um conselho
que o proprio relato sabia corrigir.
"""
import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio   # noqa: E402
import mira     # noqa: E402

VOZES = {
    "el-GR-NestorasNeural": (41.5, 43.0),
    "pl-PL-MarekNeural": (41.5, 43.0),
    "pt-BR-ThalitaMultilingualNeural": (20.0, 26.0),
}


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _prev(voz, n, chars, provedor="edge"):
    cenas = [{"nar": "x" * chars} for _ in range(n)]
    return ensaio.duracao_real_prevista(cenas, voz, provedor)


def _spec(voz, n, chars, faixa=None):
    sp = {"voz": voz, "idioma": "el", "slug": "x", "longo": [],
          "short": [{"layout": "titulo", "nar": "x" * chars}
                    for _ in range(n)]}
    if faixa:
        sp["short_alvo_s"] = list(faixa)
    return sp


def test_o_inversor_CRU_cai_abaixo_do_piso_em_TODO_par():
    """A medida que o conserto corrige — reconferida contra o codigo (753)."""
    pares = positivos = abaixo = zeros = 0
    for voz, faixa in VOZES.items():
        for n in range(2, 21):
            if not mira.janela_do_mundo(voz, n, faixa, "edge"):
                continue
            pares += 1
            cru = mira._chars_para_o_real(voz, n, faixa[0], "edge")
            if cru <= 0:
                zeros += 1
                continue
            positivos += 1
            if _prev(voz, n, cru) < faixa[0] - 1e-9:
                abaixo += 1
    assert pares >= 40, (
        "so %d par(es) (voz, cenas) com janela: a medida ficou fraca" % pares)
    assert positivos >= 40 and abaixo == positivos, (
        "o inversor deixou de cair abaixo do piso em %d de %d pares com valor"
        " positivo: ele mudou de forma, e esta nota tem de ser relida"
        % (abaixo, positivos))
    # E os ZEROS existem e vao contados em separado: a linha antiga do relato
    # dizia "54 de 54" somando-os aos que caem abaixo, e o numero certo e
    # 51 de 51. Se eles desaparecerem, a refinacao perde o objeto.
    assert zeros >= 1, (
        "nenhum par devolve ZERO: a distincao que a refinacao faz (valor cru"
        " abaixo do piso contra nenhum valor possivel) deixou de existir")


def test_o_corte_para_o_PISO_agora_cai_DENTRO():
    """A propriedade que importa, nos tres idiomas e em toda contagem."""
    testados = corrigidos = 0
    for voz, faixa in VOZES.items():
        for n in (6, 7, 9, 11, 13, 14):
            jan = mira.janela_do_mundo(voz, n, faixa, "edge")
            if not jan:
                continue
            q = mira.quanto_cortar(_spec(voz, n, jan[0], faixa), "piso")
            if not q:
                continue
            testados += 1
            p = _prev(voz, n, q["chars_alvo"])
            assert faixa[0] - 1e-9 <= p <= faixa[1] + 1e-9, (
                "%s com %d cenas: o alvo %d preve %.2f s, FORA de %.1f a %.1f"
                % (voz, n, q["chars_alvo"], p, faixa[0], faixa[1]))
            if q["executavel"]:
                corrigidos += 1
    assert testados >= 6, (
        "so %d caso(s) testado(s): a varredura ficou vacua" % testados)
    assert corrigidos >= 1, (
        "nenhum caso precisou de correcao: o defeito desapareceu e esta nota"
        " tem de ser relida")


def test_o_valor_CRU_continua_VISIVEL_no_retorno():
    """Corrigir em silencio seria trocar um conselho errado por um opaco."""
    voz, faixa = "el-GR-NestorasNeural", (41.5, 43.0)
    jan = mira.janela_do_mundo(voz, 13, faixa, "edge")
    q = mira.quanto_cortar(_spec(voz, 13, jan[0], faixa), "piso")
    assert "chars_cru" in q and "executavel" in q, (
        "o retorno esconde a diferenca: %r" % sorted(q))
    assert q["chars_cru"] <= q["chars_alvo"], (
        "o cru ficou ACIMA do corrigido, o que inverte o defeito: %r" % q)
    if q["executavel"]:
        assert q["chars_cru"] != q["chars_alvo"]
        assert _prev(voz, 13, q["chars_cru"]) < faixa[0], (
            "o cru nao cai abaixo neste caso, logo `executavel` mentiu")


def test_o_TOPO_e_o_MEIO_NAO_sao_tocados():
    """Contraprova no outro sentido: o conserto e so do lado de BAIXO."""
    for voz, faixa in VOZES.items():
        jan = mira.janela_do_mundo(voz, 11, faixa, "edge")
        if not jan:
            continue
        sp = _spec(voz, 11, jan[0], faixa)
        for rotulo in ("meio", "topo"):
            q = mira.quanto_cortar(sp, rotulo)
            if not q:
                continue
            assert not q["executavel"], (
                "%s/%s foi corrigido e nao devia: o inversor cai ABAIXO do"
                " alvo, e abaixo do meio ou do topo ainda esta DENTRO da faixa"
                % (voz, rotulo))
            assert q["chars_alvo"] == q["chars_cru"]


def test_a_frase_do_relato_DIZ_quando_corrigiu():
    voz, faixa = "el-GR-NestorasNeural", (41.5, 43.0)
    jan = mira.janela_do_mundo(voz, 13, faixa, "edge")
    sp = _spec(voz, 13, jan[0], faixa)
    linhas = "\n".join(mira._linha_do_corte(sp))
    assert "PISO" in linhas and "MEIO" in linhas, (
        "a frase deixou de dizer os DOIS alvos: %r" % linhas[:200])
    q = mira.quanto_cortar(sp, "piso")
    if q["executavel"]:
        assert "CRU" in linhas and "EXECUTAVEL" in linhas, (
            "ela corrigiu em silencio: %r" % linhas[:300])


def test_a_conta_e_DELEGADA_ao_dono_do_piso_executavel():
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"),
                 encoding="utf-8").read()
    defs = {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}
    corpo = _codigo(defs["quanto_cortar"])
    assert "janela_do_mundo" in corpo, (
        "o `quanto_cortar` nao chama o dono do piso executavel: %r"
        % corpo[-300:])
    assert "duracao_real_prevista" in corpo, (
        "ele deixou de conferir a previsao do valor cru contra a faixa")
    for proibido in ("MODELO_VOZ", "+ 0.300", "0.3 *"):
        assert proibido not in corpo, (
            "ele reimplementou a sobrecarga por voz (%r): seria o segundo dono"
            % proibido)


def test_o_motivo_e_o_custo_continuam_escritos():
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"),
                 encoding="utf-8").read()
    assert "epomeno-epipedo-s087" in fonte, (
        "a peca que pagou as tres passadas saiu do modulo")
    assert "51 de 51" in fonte or "51 devolvem" in fonte, (
        "a medida REFINADA que sustenta o conserto saiu do modulo")
    assert "40,6" in fonte or "40.6" in fonte, (
        "o custo medido (a previsao que caiu abaixo do piso) saiu do modulo")
