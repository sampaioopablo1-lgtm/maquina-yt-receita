# -*- coding: utf-8 -*-
"""No LONGO a previsao erra para CIMA — o sinal oposto ao da serie de shorts.

MEDIDO em 19/10, nos dois primeiros longos que a maquina produziu com trilho:

    | peca                  | previsao edge | real | residuo        |
    |-----------------------|---------------|------|----------------|
    | `epomeno-epipedo-068` | 551,7         | 537  | **-14,7 s** (-2,7%) |
    | `kolejny-poziom-020`  | 570,0         | 560  | **-10,0 s** (-1,8%) |

**OS DOIS SAO NEGATIVOS, e a serie do short e dominada por POSITIVO** — 119
pontos, banda `(-1,2; 4,0)`, com meia duzia de negativos todos do mesmo canal.
Logo o erro do modelo troca de SINAL entre os dois formatos.

**O QUE EU NAO AFIRMO, pelo 679/698/725 e pelo §3.8:** que exista banda de longo.
Sao DOIS pontos, de DOIS canais e DUAS vozes, e o percentual (-1,8% e -2,7%) e
pequeno o bastante para ser qualquer coisa. **O que esta medido e a negacao:**
nao se pode usar a banda do short — construida em pecas de 23 a 44 s e positiva
— para prever um longo, porque nos dois pontos que existem ela erra o LADO.

**A CONSEQUENCIA E PRATICA E E UMA:** no longo a previsao e um LIMITE SUPERIOR,
nao inferior. Peca mirada em 8:00 exatos pode sair ABAIXO de oito minutos, e
abaixo de oito minutos o YouTube nao da anuncio mid-roll — que e a unica receita
que o formato longo acrescenta. As duas pecas sairam em 8:57 e 9:20 porque foram
escritas com folga; a proxima, mirada no limite, nao teria.

**A REGRA QUE FICA: longo mira com folga sobre os 8 min, nunca em cima deles.**
"""
import glob
import json
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

PARQUE = os.path.join(RAIZ, "docs", "pendente", "duracoes-a-medir.jsonl")
SERIE = os.path.join(RAIZ, "tests",
                     "test_residuo_quebra_o_limite_de_dois_segundos.py")
PISO_MIDROLL_S = 480.0          # oito minutos, o limite do anuncio mid-roll


def _pontos_de_longo():
    """Os pontos de LONGO do parque — DERIVADOS do disco, nunca listados.

    O parque guarda o longo de um pacote com o sufixo `-longo`, porque a chave
    e o `pacote` e um pacote publica DUAS pecas.
    """
    saida = []
    for linha in open(PARQUE, encoding="utf-8"):
        linha = linha.strip()
        if not linha:
            continue
        d = json.loads(linha)
        if not str(d.get("pacote", "")).endswith("-longo"):
            continue
        real, prov = d.get("real"), d.get("provedor")
        prev = d.get(f"prev_{prov}") if prov else None
        if real is None or prev is None:
            continue
        saida.append((d["pacote"], float(prev), int(real), prov))
    return sorted(saida)


def test_a_varredura_acha_os_pontos_de_longo():
    p = _pontos_de_longo()
    assert len(p) >= 2, (
        f"so {len(p)} ponto(s) de longo no parque — com menos de dois este "
        "arquivo nao mede nada e passaria por vacuidade"
    )


def test_todo_ponto_de_longo_tem_provedor_MEDIDO():
    """Pelo 733: provedor inferido pela distancia e o erro que ele nomeia."""
    for pacote, _prev, _real, prov in _pontos_de_longo():
        assert prov in ("edge", "piper"), (pacote, prov)


def test_no_longo_o_residuo_e_NEGATIVO_nos_pontos_que_existem():
    """E FALHA se aparecer um positivo — para esta nota ser RELIDA.

    Um ponto positivo nao derruba a consequencia pratica (a previsao deixaria de
    ser limite superior, o que e melhor), mas derruba a descricao, e descricao
    reaproveitada sem releitura e como eu venho errando.
    """
    pontos = _pontos_de_longo()
    positivos = [(p, real - prev) for p, prev, real, _ in pontos
                 if real - prev > 0]
    assert not positivos, (
        f"ponto de longo com residuo POSITIVO: {positivos}. A nota deste "
        "arquivo descreve dois pontos negativos — releia em vez de mover o "
        "numero."
    )


def test_o_sinal_do_longo_e_OPOSTO_ao_da_serie_do_short():
    """A negacao que de fato esta medida: a banda do short erra o LADO aqui."""
    import mira

    piso, teto = mira.RESIDUO_OBSERVADO
    assert teto > 0, "a banda do short deixou de ser dominada por positivo"
    for pacote, prev, real, _ in _pontos_de_longo():
        r = real - prev
        assert r < piso, (
            f"{pacote}: residuo {r:.1f} caiu DENTRO da banda do short "
            f"({piso}; {teto}) — os dois formatos deixaram de divergir e esta "
            "nota tem de ser relida"
        )


def test_os_pontos_de_longo_NAO_entram_na_serie_do_short():
    """O erro de enquadramento do 679/698/725, travado."""
    serie = open(SERIE, encoding="utf-8").read()
    assert serie.count('", ') > 50, "a serie encolheu — o teste deixou de medir"
    for pacote, _prev, _real, _prov in _pontos_de_longo():
        base = pacote[: -len("-longo")]
        linhas = re.findall(rf'\("{re.escape(base)}", \s*([\d.]+), (\d+),', serie)
        for _prev_s, real_s in linhas:
            assert int(real_s) < 180, (
                f"{base}: a serie do short tem um ponto de {real_s} s. Ela e "
                "construida em pecas de 23 a 44 s, e somar um longo ali e o "
                "erro de enquadramento do 679/698/725."
            )


def test_as_duas_pecas_passam_dos_oito_minutos():
    """A consequencia pratica, medida nas pecas que existem.

    Abaixo de 480 s o YouTube nao da mid-roll, que e a unica receita que o
    formato longo acrescenta — e com a previsao errando para CIMA, mirar em
    8:00 exatos e mirar no lado errado.
    """
    pontos = _pontos_de_longo()
    assert pontos, "sem ponto nao ha o que conferir"
    for pacote, prev, real, _ in pontos:
        assert real > PISO_MIDROLL_S, (
            f"{pacote}: {real} s esta abaixo dos oito minutos — perdeu o "
            "mid-roll, que e o motivo de o formato existir"
        )
        assert prev > PISO_MIDROLL_S, (pacote, prev)


def test_a_REGRA_e_a_RESSALVA_continuam_escritas():
    """Conserto sem motivo escrito volta calado; ressalva apagada vira lei."""
    doc = open(__file__, encoding="utf-8").read()
    for pedaco in ("LIMITE SUPERIOR", "mira com folga sobre os 8 min",
                   "DOIS pontos", "O QUE EU NAO AFIRMO"):
        assert pedaco in doc, pedaco
