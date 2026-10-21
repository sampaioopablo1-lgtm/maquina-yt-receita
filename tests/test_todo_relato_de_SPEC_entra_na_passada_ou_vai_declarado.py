"""Instrumento de SPEC fora da passada — 21/10 as 05:3x, e agora por VARREDURA.

Em 20/10 as 22:1x eu descobri que rodava os MEUS instrumentos e nao o portao; em
21/10 as 03:3x, que o `esqueleto_entre_canais` ja aceitava o caminho da spec e
nunca era chamado. **Dois achados da mesma forma, um por rodada, por acidente.**

Esta rodada virou a pergunta numa varredura: todo modulo da fabrica com um
`relato` cujo PRIMEIRO argumento e spec ou caminho de spec tem de estar NA
passada (`antes_do_render.INSTRUMENTOS`) **ou** em `FORA_DA_PASSADA` com o
motivo escrito. Medido quando a varredura entrou: CINCO estavam fora e DOIS
pertenciam — o `contagem_declarada` (o detector de "declara CINCO e enumera
SEIS", de 13/10) e o `layouts_do_short` (a sonda do render, que pega cartao em
branco SEM renderizar).

**A forma importa mais que os dois achados:** modulo novo com relato de spec
REPROVA este arquivo ate alguem decidir, e a decisao fica escrita. Silencio foi
o que deixou os dois de fora por dias.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as ADR  # noqa: E402

# Nomes de primeiro argumento que significam "uma spec, ou o caminho dela".
# MEDIDOS nos modulos da fabrica, nao escolhidos.
ARGS_DE_SPEC = ("caminho", "spec", "spec_ou_caminho", "sp", "sp_ou_caminho")


def _relatos_de_spec():
    """{modulo: nome do primeiro argumento} para todo `relato` de spec."""
    saida = {}
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "*.py"))):
        nome = os.path.basename(p)[:-3]
        if nome == "antes_do_render":
            continue
        try:
            a = ast.parse(open(p, encoding="utf-8").read())
        except Exception:
            continue
        fn = [n for n in a.body
              if isinstance(n, ast.FunctionDef) and n.name == "relato"]
        if not fn or not fn[0].args.args:
            continue
        a0 = fn[0].args.args[0].arg
        if a0 in ARGS_DE_SPEC:
            saida[nome] = a0
    return saida


def test_a_varredura_nao_passa_por_VACUIDADE():
    r = _relatos_de_spec()
    assert len(r) >= 8, (
        "so %d modulos com relato de spec; abaixo disso a varredura nao mede "
        "nada e este arquivo passa por vacuidade" % len(r))


def test_TODO_relato_de_spec_esta_na_passada_ou_DECLARADO():
    """O teste que torna a decisao obrigatoria."""
    r = _relatos_de_spec()
    dentro = set(ADR.INSTRUMENTOS)
    fora = set(ADR.FORA_DA_PASSADA)
    orfaos = sorted(set(r) - dentro - fora)
    assert not orfaos, (
        "estes modulos tem `relato` de SPEC e nao estao nem na passada nem em "
        "`FORA_DA_PASSADA`: %r. Decida: ou entra em `INSTRUMENTOS`, ou entra "
        "em `FORA_DA_PASSADA` com o MOTIVO escrito. Silencio foi o que deixou "
        "o `contagem_declarada` e o `layouts_do_short` de fora por dias"
        % (orfaos,))


def test_os_DOIS_conjuntos_nao_se_cruzam_e_nenhum_e_vazio():
    dentro = set(ADR.INSTRUMENTOS)
    fora = set(ADR.FORA_DA_PASSADA)
    assert dentro and fora, (
        "um dos dois conjuntos ficou vazio: dentro=%r fora=%r" % (dentro, fora))
    assert not (dentro & fora), (
        "modulo nos DOIS conjuntos: %r" % sorted(dentro & fora))


def test_cada_EXCLUSAO_carrega_um_motivo_de_verdade():
    for nome, motivo in ADR.FORA_DA_PASSADA.items():
        assert isinstance(motivo, str) and len(motivo) >= 60, (
            "a exclusao de %r tem motivo de %d caracteres: motivo curto e "
            "silencio com aparencia de decisao" % (nome, len(motivo or "")))
        assert nome not in ADR.INSTRUMENTOS


def test_as_EXCLUIDAS_de_fato_nao_servem_para_uma_spec():
    """Contraprova no outro sentido: se uma excluida passar a responder bem
    para uma spec, a exclusao perdeu o objeto e tem de ser RELIDA."""
    alvo = _uma_spec()
    for nome in ADR.FORA_DA_PASSADA:
        mod = __import__(nome)
        try:
            saida = mod.relato(alvo)
        except Exception:
            continue          # levantar e um jeito legitimo de nao servir
        baixo = (saida or "").lower()
        serve = not any(m in baixo for m in
                        ("defeito", "nao tem faixa", "0\n", "credito"))
        assert not serve, (
            "o modulo %r, declarado FORA da passada, respondeu util para uma "
            "spec real:\n%s\n\nSe ele passou a servir, a exclusao tem de ser "
            "RELIDA — nao mantida por inercia" % (nome, saida[:200]))


def _uma_spec():
    """Uma spec de short solto DERIVADA do disco."""
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short") or not (d.get("copy") or ""):
            continue
        return p
    raise AssertionError("perdi a ancora: nenhuma spec de short solto com copy")


def test_os_DOIS_que_entraram_RESPONDEM_e_o_relato_os_carrega():
    alvo = _uma_spec()
    for nome in ("contagem_declarada", "layouts_do_short"):
        assert nome in ADR.INSTRUMENTOS, (
            "%r saiu da passada; ele foi medido como pertencente em 05:3x"
            % nome)
        saida = ADR._relato_do_instrumento(nome, alvo)
        assert saida and "AMBIENTE, nao a spec" not in saida, (
            "%r nao respondeu para uma spec real: %r" % (nome, saida[:120]))
    r = ADR.relato(alvo)
    assert "LAYOUT DO SHORT" in r, (
        "a sonda dos layouts nao aparece no relato da passada")
    assert "contagem declarada" in r.lower() or "CONTAGEM" in r, (
        "o detector da contagem declarada nao aparece no relato da passada")


def test_a_SONDA_dos_layouts_e_um_proxy_BARATO_do_portao_caro():
    """O `layout` fica fora da passada por RENDERIZAR; a sonda responde a mesma
    pergunta sem render, e e por isso que ela entra."""
    assert "layout" in ADR.PORTOES_CAROS, (
        "o portao `layout` saiu de `PORTOES_CAROS`: se ele ficou barato, a "
        "sonda deixa de ser proxy e esta nota se rele")
    assert "layouts_do_short" in ADR.INSTRUMENTOS


def test_o_motivo_da_varredura_continua_escrito():
    fonte = open(os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
                 encoding="utf-8").read()
    for marca in ("CINCO", "contagem_declarada", "layouts_do_short",
                  "13/10", "19:1x"):
        assert marca in fonte, (
            "a marca %r saiu do modulo; sem ela a rodada seguinte tira um dos "
            "dois da passada por parecer redundante" % marca)
