# -*- coding: utf-8 -*-
"""A serie tinha o `epomeno-epipedo-s058` DUAS vezes, e a culpa e do meu replace.

Medido em 18/10 as 11:2x, quando o `RESIDUO_N` e o `len(SERIE)` divergiram: 93
contra 94. Eu acrescento ponto a serie com

    t.replace(ancora, ancora + "\\n" + linha_nova)

e a ancora que eu escrevo e a linha SEM o comentario de job — por exemplo
`("labtreinamento-s075", 25.8, 29, "edge"),`. So que a linha no arquivo TEM
comentario. Logo o `replace` casa um PREFIXO de linha: a linha nova entra no
MEIO, e o comentario que estava no fim da linha antiga fica pendurado no fim da
NOVA.

Repetido por varias rodadas isso produziu dois estragos:
  * comentarios de job deslocados, acumulados numa linha so (seis jobs na
    mesma linha, cada um de uma rodada diferente);
  * e por fim um ponto DUPLICADO, porque uma ancora passou a casar dentro da
    linha corrompida em vez da linha pretendida.

**E o `assert t.count(ancora) == 1` que eu uso NAO pega isso**: o prefixo e
unico mesmo quando a linha inteira nao e. O assert mede o que eu pedi, e o que
eu pedi era insuficiente — a assinatura do 3.8 numa guarda que eu mesmo escrevi
para me proteger.

**A consequencia na medicao:** a banda contava um ponto que nao existe. Nao
mudou limite nenhum (o duplicado era +0,5, bem dentro), mas `RESIDUO_N` era um
numero que eu reportei ao dono e estava errado por um.

A regra que fica: ancore o replace na linha INTEIRA, ou insira por LINHA, e
confira a contagem de pontos DISTINTOS depois de gravar.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import mira  # noqa: E402

ARQ = os.path.join(os.path.dirname(__file__),
                   "test_residuo_quebra_o_limite_de_dois_segundos.py")
# `-s?\d+`: o sufixo de SHORT SOLTO e `-sNNN` e o de PACOTE e `-NNN`. A
# forma antiga, com `-s\d+` cravado, deixava o PRIMEIRO ponto de pacote
# (`epomeno-epipedo-068`, 19/10 as 13:1x) INVISIVEL para esta varredura — e
# ponto invisivel nao e so contagem errada: ele sai da medicao sem avisar.
LINHA = re.compile(r'^\s*\("([a-z-]+-s?\d+)",\s*([\d.]+),\s*(\d+),\s*"(\w+)"\),')


def _pontos():
    saida = []
    for ln in open(ARQ, encoding="utf-8"):
        m = LINHA.match(ln)
        if m:
            saida.append((m.group(1), float(m.group(2)), int(m.group(3)),
                          m.group(4), ln))
    return saida


def test_a_serie_NAO_tem_pacote_repetido():
    nomes = [p[0] for p in _pontos()]
    rep = [k for k, v in collections.Counter(nomes).items() if v > 1]
    assert rep == [], (
        "pacote repetido na serie do residuo — o replace entrou no meio de uma "
        "linha: " + ", ".join(rep))


def test_a_varredura_NAO_e_vazia():
    """Contraprova: um regex que deixa de casar faria os dois passarem."""
    n = len(_pontos())
    assert n >= 80, f"so {n} pontos lidos — o regex da linha quebrou"


def test_a_contagem_do_modulo_bate_com_a_SERIE():
    assert mira.RESIDUO_N == len(_pontos()), (
        f"RESIDUO_N={mira.RESIDUO_N} contra {len(_pontos())} pontos no arquivo "
        "— foi exatamente essa divergencia que revelou a duplicata")


def test_nenhuma_linha_carrega_DOIS_comentarios_de_job():
    """O sintoma visivel do replace no meio da linha, antes da duplicata."""
    ruins = [ln.rstrip() for _n, _p, _r, _v, ln in _pontos()
             if ln.count("# job") > 1]
    assert ruins == [], (
        "linha com mais de um `# job` — comentario deslocado pelo replace:\n"
        + "\n".join(ruins[:3]))


def test_o_job_citado_e_UNICO_por_ponto():
    """Dois pontos nao podem apontar para o mesmo render."""
    jobs = []
    for _n, _p, _r, _v, ln in _pontos():
        m = re.search(r'# job (\d+)', ln)
        if m:
            jobs.append(m.group(1))
    rep = [k for k, v in collections.Counter(jobs).items() if v > 1]
    assert rep == [], "mesmo job em dois pontos da serie: " + ", ".join(rep)
    assert len(jobs) >= 10, (
        f"so {len(jobs)} pontos trazem job — a procedencia esta sumindo da serie")


def test_a_licao_fica_escrita_no_CLAUDE_md():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    liso = " ".join(open(os.path.join(raiz, "CLAUDE.md"),
                         encoding="utf-8").read().split())
    assert re.search(r'replace.{0,80}(meio|PREFIXO)', liso, re.I), (
        "a licao do replace que casa prefixo saiu do CLAUDE.md")
