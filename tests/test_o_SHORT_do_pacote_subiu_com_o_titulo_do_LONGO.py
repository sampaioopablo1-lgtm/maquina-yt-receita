# -*- coding: utf-8 -*-
"""O short do pacote subiu com o título do LONGO — e a máquina sabia fazer certo.

MEDIDO em 19/10 às 14:4x, na página publicada das TRÊS peças de hoje. O
`<meta name="title">` do short e do longo é **byte a byte o mesmo** nos três
pacotes:

| pacote | longo | short | título |
|---|---|---|---|
| `epomeno-epipedo-068` | `pqTc8jBrq0E` | `BaLtIWzaN84` | idêntico |
| `kolejny-poziom-020` | `GtmoaQMr_1c` | `9zfF0f4aDQM` | idêntico |
| `labtreinamento-014` | `POBNoY16wG8` | `HdzEm86V1HU` | idêntico, **62 chars** |

**E a causa é minha, não do código.** O `publicar.ler_copy` lê o
`## TITULO SHORT` **pelo CABEÇALHO** desde 01/09/2026, e a nota dele carrega o
incidente que o produziu: o `kolejny-poziom-014` publicou o short `lCXwLaqUHJI`
com os **68 caracteres** do título do longo, *"Ile Płacisz za Dane, Których Nie
Zużywasz? Policz z Własnego Rachunku"*, **num formato onde o feed vertical corta
o título antes da metade**. A máquina sabe fazer certo e eu escrevi três copies
sem a seção.

**É a classe do trilho das 09:2x invertida outra vez:** lá o código era chamado
e nunca recebia dado; aqui o código é chamado, sabe ler, e **quem não forneceu
o dado fui eu**.

**NÃO virou portão, e o motivo é MEDIDO:** dos **140** pacotes do disco, só
**35** trazem a seção e **105** não — um portão aqui reprovaria 105 specs, que é
exatamente o argumento pelo qual o `mira.py` não é portão (aviso que dispara 44
vezes deixa de avisar). O buraco é LATENTE no acervo e o lugar dele é a suíte.

**O que NÃO foi feito, e vai dito:** os três shorts já estão no ar com o título
do longo. Trocar título de peça publicada é mudança para fora que a autorização
de 09/10 não nomeia, custa cota e o `publicar.py:371` avisa que o
`videos.update` exige o snippet INTEIRO. **A regra que fica é de REDAÇÃO: todo
pacote novo leva `## TITULO SHORT` na copy.**
"""
import ast
import glob
import json
import os
import re
import sys
import tempfile

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
CAB_SHORT = re.compile(r"^##\s*.*\bSHORTS?\b", re.I | re.M)


def _pacotes():
    """Toda spec com longo E short — a varredura sai do DISCO."""
    saida = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(f))
        except Exception:
            continue
        if (sp.get("longo") or []) and (sp.get("short") or []):
            saida.append((os.path.basename(f)[:-5], sp))
    return saida


def _com_secao():
    return [(n, sp) for n, sp in _pacotes()
            if isinstance(sp.get("copy"), str) and CAB_SHORT.search(sp["copy"])]


def _sem_secao():
    return [(n, sp) for n, sp in _pacotes()
            if not (isinstance(sp.get("copy"), str) and CAB_SHORT.search(sp["copy"]))]


def _titulos(sp):
    """Chama o DONO da regra — `publicar.ler_copy` — com uma copy renderizada."""
    wd = tempfile.mkdtemp()
    cp = sp.get("copy") or ""
    cp = cp.replace("{CAPITULOS}", "00:00 Abre").replace("{TRILHA}", "Inspired (CC BY)")
    with open(os.path.join(wd, "copy.md"), "w", encoding="utf-8") as fh:
        fh.write(cp)
    d = publicar.ler_copy(sp, wd)
    return d["titulo"], (d.get("short_titulo") or "")


def test_a_varredura_acha_pacote_no_disco():
    pac = _pacotes()
    assert len(pac) > 50, (
        f"só {len(pac)} pacote(s) no disco — a varredura encolheu e este "
        "arquivo passaria por vacuidade"
    )


def test_OS_DOIS_LADOS_da_varredura_existem():
    """Sem os dois lados o arquivo não mede nada: um só passaria sozinho."""
    com, sem = _com_secao(), _sem_secao()
    assert com, "nenhum pacote COM `## TITULO SHORT` — a capacidade não é exercitada"
    assert sem, (
        "nenhum pacote SEM a seção — se isto acontecer, o buraco fechou e esta "
        "nota tem de ser RELIDA em vez de mantida"
    )


def test_a_maquina_SABE_fazer_certo_quando_a_secao_existe():
    com = _com_secao()
    assert com, "sem spec com a seção não há o que medir"
    conferidos = 0
    for nome, sp in com:
        try:
            longo, curto = _titulos(sp)
        except SystemExit:
            continue  # copy de geração antiga que o leitor recusa; não é o alvo
        if not curto:
            continue
        assert curto != longo, f"{nome}: a seção existe e o short herdou o longo"
        conferidos += 1
    assert conferidos, (
        "nenhum pacote com a seção chegou a produzir short_titulo — a detecção "
        "pelo CABEÇALHO parou de funcionar"
    )


def test_CONTRAPROVA_sem_a_secao_o_short_HERDA_o_titulo_do_longo():
    """É este o defeito, e ele tem de continuar visível em teste."""
    sem = _sem_secao()
    assert sem, "sem o lado vazio a contraprova perdeu o objeto"
    herdaram = 0
    for nome, sp in sem:
        try:
            longo, curto = _titulos(sp)
        except SystemExit:
            continue
        assert curto == "", f"{nome}: sem seção e com short_titulo — regex frouxa?"
        herdaram += 1
    assert herdaram, "nenhum pacote sem seção pôde ser lido — a contraprova é vazia"


def test_a_DETECCAO_e_pelo_CABECALHO_e_mora_no_publicar():
    """Reimplementar a regex aqui criaria o segundo dono — é o defeito da legenda.

    Por AST: o arquivo CITA `## TITULO SHORT` na prosa para se explicar, e casar
    prosa pegaria a explicação em vez do código.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "publicar.py"), encoding="utf-8").read()
    arvore = ast.parse(fonte)
    achou = False
    for n in ast.walk(arvore):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if "SHORTS?" in n.value and "\\b" in n.value:
                achou = True
    assert achou, (
        "o padrão de cabeçalho do título do short saiu do `publicar.py` — sem "
        "ele TODO short de pacote volta a herdar o título do longo"
    )


def test_o_INCIDENTE_que_criou_a_capacidade_continua_escrito():
    """Conserto sem motivo escrito volta calado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "publicar.py"), encoding="utf-8").read()
    assert "lCXwLaqUHJI" in fonte, (
        "a peça medida em 01/09 (short com o título de 68 chars do longo) saiu "
        "da nota — é ela que explica por que a seção existe"
    )
    assert "CABECALHO" in fonte or "CABEÇALHO" in fonte, fonte[:0]


def test_isto_NAO_virou_portao_e_o_motivo_e_medido():
    """105 de 140 reprovariam: aviso que dispara sempre deixa de avisar."""
    com, sem = len(_com_secao()), len(_sem_secao())
    assert sem > com, (
        f"a maioria passou a trazer a seção ({com} com, {sem} sem) — então o "
        "argumento contra o portão caiu e isto tem de ser RELIDO"
    )
    # Por AST e NAO por texto: o `prontidao` CITA "## TITULO SHORT" na prosa
    # para explicar o conserto do 773 (o corpus guarda a forma curta), e casar
    # prosa pegaria a explicacao em vez de um portao.
    pron = open(os.path.join(RAIZ, "fabrica", "prontidao.py"), encoding="utf-8").read()
    nomes = {n.name for n in ast.walk(ast.parse(pron))
             if isinstance(n, ast.FunctionDef) and n.name.startswith("_gate")}
    assert not any("short" in n for n in nomes), (
        f"isto virou portão sem a medição que o justifique: {sorted(nomes)}"
    )


def test_a_nota_do_caso_REAL_continua_no_CLAUDE_md():
    doc = open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8").read()
    assert "HdzEm86V1HU" in doc, (
        "o short que subiu com o título do longo saiu do CLAUDE.md — sem ele a "
        "rodada seguinte escreve o quarto pacote com o mesmo defeito"
    )
