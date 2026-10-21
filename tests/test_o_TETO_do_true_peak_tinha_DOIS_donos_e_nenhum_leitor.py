# -*- coding: utf-8 -*-
"""O teto do true peak tinha DOIS donos e NENHUM leitor — 21/10 as 13:4x.

O `fabrica.AUDIO_ARGS` cravava `loudnorm=I=-14:TP=-1.5` na linha do filtro e o
`som.py` guardava os MESMOS dois numeros em `ALVO_LUFS` e `TP_MAX_DBTP` — e o
comentario do `som.py` chamava o -1.5 de *"teto do nosso filtro"*, enquanto o
filtro morava em outro arquivo. Dois donos da mesma regra.

**E ninguem comparava a MEDIDA contra o teto:** o `relato` imprimia os dois lado
a lado e so avisava sobre LUFS. Nas anotacoes dos 38 renders mais recentes da
frota, NOVE ficaram acima de -1.5 e UM passou de ZERO — o
`epomeno-epipedo-s086`, com +0,7 dBFS, publicado na mesma rodada deste conserto.
**Essa medida sai das anotacoes de job e nenhum teste a reconfere**, porque ela
nao esta no disco; ela vai declarada como tal no modulo.

O numero NAO muda (§10): -14.0 e -1.5 continuam sendo os mesmos. O que muda e
haver UM dono e haver um LEITOR.
"""
import ast
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import som  # noqa: E402


def _fonte(arquivo):
    return open(os.path.join(RAIZ, "fabrica", arquivo), encoding="utf-8").read()


def test_o_filtro_LE_as_duas_constantes_do_dono():
    import fabrica as F
    af = F.AUDIO_ARGS[F.AUDIO_ARGS.index("-af") + 1]
    assert "loudnorm" in af, "o filtro de audio mudou de nome: %r" % af
    assert ("I=%g" % som.ALVO_LUFS) in af, (
        "o alvo do filtro nao e o do `som.ALVO_LUFS`: %r" % af)
    assert ("TP=%g" % som.TP_MAX_DBTP) in af, (
        "o teto do filtro nao e o do `som.TP_MAX_DBTP`: %r" % af)


def test_o_numero_NAO_mudou():
    """§10: isto e conserto de dono, nao mudanca de parametro de producao."""
    assert som.ALVO_LUFS == -14.0, (
        "`ALVO_LUFS` virou %r: parametro de producao nao se mexe sozinho"
        % som.ALVO_LUFS)
    assert som.TP_MAX_DBTP == -1.5, (
        "`TP_MAX_DBTP` virou %r: parametro de producao nao se mexe sozinho"
        % som.TP_MAX_DBTP)


def test_o_filtro_nao_crava_mais_os_numeros():
    fonte = _fonte("fabrica.py")
    arvore = ast.parse(fonte)
    for n in ast.walk(arvore):
        if not isinstance(n, ast.Assign):
            continue
        if not any(getattr(t, "id", "") == "AUDIO_ARGS" for t in n.targets):
            continue
        corpo = ast.unparse(n)
        assert "TP=-1.5" not in corpo and "I=-14" not in corpo, (
            "o `AUDIO_ARGS` voltou a cravar o numero: %r" % corpo)
        assert "som" in corpo, (
            "o `AUDIO_ARGS` deixou de ler o dono: %r" % corpo)
        return
    raise AssertionError("`AUDIO_ARGS` desapareceu do `fabrica.py`")


def test_os_TRES_estados_existem_e_a_fronteira_e_cobrada():
    """A fronteira nos dois lados — teto EXATO cabe, um passo acima nao."""
    t = som.TP_MAX_DBTP
    assert som.pico_acima_do_teto(t)["estado"] == "dentro", (
        "o pico EXATAMENTE no teto deixou de caber: o teto e inclusivo")
    assert som.pico_acima_do_teto(t + 0.1)["estado"] == "acima_do_teto", (
        "um decimo acima do teto nao foi acusado")
    assert som.pico_acima_do_teto(0.0)["estado"] == "acima_do_teto", (
        "zero EXATO nao e clipe: acima de zero e que estoura")
    assert som.pico_acima_do_teto(0.1)["estado"] == "clipa", (
        "pico acima de zero deixou de sair como clipe")
    assert som.pico_acima_do_teto(t - 5)["estado"] == "dentro"
    estados = {som.pico_acima_do_teto(v)["estado"]
               for v in (-9.0, t + 0.1, 0.7, None)}
    assert estados == {"dentro", "acima_do_teto", "clipa", "sem_leitura"}, (
        "os quatro estados nao sao distintos: %r" % estados)


def test_ausencia_de_leitura_NAO_e_zero():
    d = som.pico_acima_do_teto(None)
    assert d["estado"] == "sem_leitura", (
        "pico None caiu num estado de valor: ausencia de leitura nao e zero"
        " (a licao do 17/10)")
    assert "folga" not in d, (
        "ele inventou folga sem leitura: %r" % d)
    assert "SEM LEITURA" in som._linha_do_pico(None).upper()


def test_a_frase_tem_UM_dono_e_sai_em_TODO_estado():
    fonte = _fonte("som.py")
    defs = {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}
    assert "_linha_do_pico" in defs, "a frase do pico perdeu o dono"
    corpo = ast.unparse(defs["relato"])
    assert "_linha_do_pico" in corpo, (
        "o `relato` nao chama o dono da frase — ele foi calculado e jogado"
        " fora, que e o defeito do `contagem_de_cenas` em 20/10 as 03:2x")
    assert "estoura a escala" not in corpo, (
        "a frase foi copiada para dentro do `relato`")
    # e ela sai em QUALQUER estado: sem o ramo `dentro`, ausencia de frase
    # ficaria indistinguivel de o relato nao ter olhado
    for v in (-9.0, som.TP_MAX_DBTP + 0.1, 0.7, None):
        assert "pico" in som._linha_do_pico(v).lower(), (
            "o estado de pico %r saiu sem frase" % v)


def test_o_estado_vai_no_JSON_que_o_workflow_LE():
    """O `frota.yml` chama `som.py --json`, nao o `relato`."""
    fonte = _fonte("som.py")
    defs = {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}
    corpo = ast.unparse(defs["main"])
    assert "pico_vs_teto" in corpo and "pico_acima_do_teto" in corpo, (
        "o JSON nao leva o estado do pico: a frase ficaria so no `relato`, que"
        " workflow nenhum le — instrumento que ninguem chama")
    wf = open(os.path.join(RAIZ, ".github", "workflows", "frota.yml"),
              encoding="utf-8").read()
    assert "som.py" in wf and "--json" in wf, (
        "o workflow deixou de chamar o `som.py --json`: o caminho que carrega"
        " o estado mudou e esta nota tem de ser relida")


def test_a_medida_e_a_procedencia_continuam_escritas():
    """RETRATADO EM 21/10 AS 22:4x, e o errado era este teste.

    Ele cobrava que o `som.py` continuasse dizendo *"a medida sai das anotacoes
    de job e NENHUM TESTE A RECONFERE, porque ela nao esta no disco"* — isto e,
    **ele travava o estado DEFEITUOSO**, exatamente como o
    `test_sem_mapa_ele_DIZ_que_o_mapa_falta` em 20/10 as 10:1x. O
    `som_parqueado` pos a leitura no disco e o teste dele a reconta, logo a
    frase cobrada virou falsa.

    A propriedade DURAVEL e outra, e e ela que fica: a medida continua com
    PROCEDENCIA escrita, a peca que produziu o achado continua nomeada, e o
    modulo aponta para onde a contagem viva se reconfere — em vez de repetir o
    numero, que e o 753.
    """
    fonte = _fonte("som.py")
    assert "epomeno-epipedo-s086" in fonte, (
        "a peca que produziu o achado saiu do modulo: sem ela a medida fica"
        " sem caso")
    assert "38" in fonte and re.search(r"NOVE|nove", fonte), (
        "a contagem a mao de 21/10 saiu do modulo — ela fica como HISTORIA,"
        " porque e ela que explica por que o parque passou a existir")
    assert re.search(r"HISTORIA|historia", fonte), (
        "a contagem antiga deixou de ir marcada como historia, e assim ela"
        " volta a ler como medida viva")
    assert "som_parqueado" in fonte, (
        "o modulo deixou de apontar para onde a contagem viva mora — sem isso"
        " quem le o `som.py` nao sabe que ela e reconferivel")
