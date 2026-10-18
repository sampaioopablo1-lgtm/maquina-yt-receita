# -*- coding: utf-8 -*-
"""Medido em 18/10 as 08:1x: o `prontidao` aprovou os ONZE portoes do
`epomeno-epipedo-s058` e o render morreu em `KeyError: 'longo'`.

A spec de short solto declara `"longo": []` — lista vazia, porque nao ha longo
a renderizar — e eu escrevi a spec SEM a chave. Os onze portoes passaram: eles
conferem duracao, identidade, variedade, ortografia, titulo duplicado,
similaridade, numeros. **Nenhum confere se a spec tem as chaves que o render
LE.** O run `39110638169` baixou as tres trilhas, montou o ambiente e so
entao estourou.

E a falha e CARA do jeito que o 3.8 descreve: portao verde fabricou "esta
tudo certo", e o custo foi um run inteiro mais a rodada de diagnose — o
`KeyError` nao sai pelas ANOTACOES, so pelo log, que nesta sessao exige baixar
o blob pelo sandbox porque o `gh` recusa redirecionamento entre hosts.

A regra que fica: ausencia de chave nao e valor vazio, e portao que nunca
abre a spec como o render a abre nao protege contra isso.

O que este teste NAO faz: nao vira portao novo dentro do `prontidao`. Pelo
argumento do `mira.py` (44 avisos), portao que dispara em peca historica
deixa de avisar — e aqui a varredura mostra que NENHUMA spec do disco esta
sem a chave, logo o buraco e LATENTE e o lugar dele e a suite.
"""
import glob
import json
import os

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(RAIZ, "fabrica", "specs")

# a peca que pagou pelo achado, com o run que morreu
PECA = "epomeno-epipedo-s058"
RUN_MORTO = "39110638169"

# as chaves que o render LE de uma spec de short solto. Nao e a lista completa
# do renderizador: e o conjunto cuja ausencia ja matou run, mais as que o
# `etapas.py` acessa por indice direto no caminho SO_SHORT.
CHAVES_DO_RENDER = ("slug", "idioma", "voz", "trilha", "paleta", "pacote",
                    "short", "longo")


def _specs_de_short_solto():
    for f in sorted(glob.glob(os.path.join(SPECS, "*-s[0-9]*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d.get("short"), list) and d["short"]:
            yield os.path.basename(f), d


def test_a_peca_do_achado_existe_e_tem_a_chave():
    """Sem isto o teste passaria por vacuidade depois do conserto."""
    p = os.path.join(SPECS, PECA + ".json")
    assert os.path.exists(p), f"{PECA} sumiu — este teste perde a ancora"
    d = json.load(open(p, encoding="utf-8"))
    assert "longo" in d, f"{PECA} voltou a ficar sem a chave que matou o run"
    assert d["longo"] == [], "short solto tem longo VAZIO, nao ausente"


def test_toda_spec_de_short_solto_tem_a_chave_longo():
    sem = [n for n, d in _specs_de_short_solto() if "longo" not in d]
    assert sem == [], (
        "spec de short solto sem a chave `longo` — o render morre em "
        "KeyError DEPOIS de baixar trilha: " + ", ".join(sem))


def test_nenhuma_spec_de_short_solto_perde_chave_que_o_render_le():
    faltas = []
    for n, d in _specs_de_short_solto():
        for k in CHAVES_DO_RENDER:
            if k not in d:
                faltas.append(f"{n}:{k}")
    assert faltas == [], "chave do render ausente: " + ", ".join(faltas[:12])


def test_a_varredura_NAO_e_vazia():
    """Contraprova: se o glob parar de achar spec, os dois testes acima
    passam sem medir nada — que e o defeito do 743 em forma de varredura."""
    n = sum(1 for _ in _specs_de_short_solto())
    assert n >= 50, f"so {n} specs de short solto varridas — o glob quebrou"


def test_a_chave_ausente_NAO_se_confunde_com_lista_vazia():
    """A contraprova no outro sentido: o criterio distingue os dois casos.
    Se ele aceitasse `None` ou ausencia como vazio, o run teria morrido
    igual e o teste teria passado."""
    ausente = {"short": [{"nar": "x"}]}
    vazia = {"short": [{"nar": "x"}], "longo": []}
    assert "longo" not in ausente
    assert "longo" in vazia and vazia["longo"] == []
    # `.get` NU distingue: devolve None, que nao e lista vazia. O que
    # MASCARA e o default — e e assim que esta ausencia passa calada por
    # qualquer leitor escrito com `.get(k, [])`.
    assert ausente.get("longo") is None
    assert ausente.get("longo") != vazia["longo"]
    assert ausente.get("longo", []) == vazia["longo"], (
        "o default do .get e o que apaga a diferenca — o criterio deste "
        "arquivo e `in`, nunca o valor lido com default")


def test_o_prontidao_NAO_ganhou_portao_novo():
    """O conserto e na suite, nao no portao — pelo argumento do mira.py.
    Falha se alguem transformar isto em portao, para que a decisao seja
    relida em vez de escorregar."""
    src = open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
               encoding="utf-8").read()
    assert "CHAVES_DO_RENDER" not in src, (
        "isto virou portao dentro do prontidao — releia a razao no docstring "
        "deste arquivo antes de manter")


def test_a_licao_fica_escrita_no_CLAUDE_md():
    t = open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8").read()
    liso = " ".join(t.split())
    assert RUN_MORTO in liso, (
        "o run que morreu saiu do CLAUDE.md — sem ele a licao nao tem "
        "procedencia")
    assert "KeyError" in liso, "o modo de falha saiu do documento"
