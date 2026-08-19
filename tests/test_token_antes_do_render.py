"""Renderizar sem rota de publicacao gasta 20 minutos para produzir um pacote parado.

Medido em 19/08/2026: o agla-level-004 renderizou inteiro, foi entregue no
Storage, e so o passo de publicacao descobriu que o refresh token do canal
tinha morrido — 45 minutos depois de eu mesmo o ter testado vivo. Na mesma
madrugada 9 dos 12 tokens morreram em cascata (todos os emitidos enquanto o
app OAuth ainda estava em modo Testing expiram no seu proprio marco de 7
dias).

O conserto e ordem: conferir o token ANTES do render, onde falhar custa
trinta segundos. Estes testes existem para que o passo nao suma do workflow
num refactor — se sumir, cai aqui, e nao no proximo pacote de 20 minutos.
"""
from __future__ import annotations

import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FROTA = (RAIZ / ".github" / "workflows" / "frota.yml").read_text(encoding="utf-8")
SCRIPT = RAIZ / "fabrica" / "confere_token.py"


def test_o_workflow_confere_o_token():
    assert "confere_token.py" in FROTA, (
        "o frota.yml nao confere o token — um canal com token morto voltaria a "
        "renderizar 20 min para nada")


def test_a_conferencia_vem_ANTES_do_render():
    """A ordem e o conserto inteiro: conferir depois do render nao economiza nada."""
    assert FROTA.index("confere_token.py") < FROTA.index("etapas.py"), (
        "o passo de token esta DEPOIS do render — inverta, senao ele nao "
        "economiza o render que veio para economizar")


def test_so_confere_quando_vai_publicar():
    """Render com publicar=false e legitimo (pacote para o Drive) e nao pode
    ser barrado por token."""
    trecho = FROTA[FROTA.index("Conferir token do canal"):FROTA.index("confere_token.py")]
    assert "inputs.publicar" in trecho, (
        "sem a guarda `if: inputs.publicar`, um render deliberadamente sem "
        "publicacao passa a exigir token vivo")


def test_o_script_existe_e_compila():
    assert SCRIPT.exists(), "fabrica/confere_token.py sumiu"
    ast.parse(SCRIPT.read_text(encoding="utf-8"))


def test_a_mensagem_diz_o_que_fazer():
    """Erro que nao diz a acao vira ticket parado: a mensagem tem que mandar
    reautorizar."""
    fonte = SCRIPT.read_text(encoding="utf-8")
    assert "reautorizar" in fonte.lower()
    assert "TOKEN MORTO" in fonte
