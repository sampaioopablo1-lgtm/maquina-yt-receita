#!/usr/bin/env python3
"""Compara conversao de shorts entre DUAS FORMAS, e diz quando nao da para comparar.

POR QUE ISTO EXISTE, medido em 26/08/2026.

A rotina manda medir INSCRITO POR VIEW, pacote a pacote. Medido pacote a
pacote, o numero mente quase sempre, e da para dizer o quanto:

    frota inteira, 79 shorts publicados:  14.657 views, 16 inscritos
    taxa base: 0,109% — um inscrito a cada 916 views

    67 dos 79 shorts tem ZERO inscrito.
    Sob uma taxa UNICA para todos, o esperado seria 67,4.

Os zeros nao pedem explicacao nenhuma: eles sao exatamente o que a exposicao
prevê. E o teste por short nao salva: o short mais improvavel da frota
(nivel-do-jogo-004-short, 2 inscritos em 94 views) tem p bruto de 0,005, que
corrigido pelas 79 comparacoes vira 0,39. Nenhum short da frota e distinguivel
de nenhum outro.

O QUE ISSO NAO SIGNIFICA. Nao significa que a forma nao importa — significa que
a unidade de medida errada esconde o efeito. O aprendizado 482 foi RE-TESTADO
aqui com a evidencia que ele mesmo registrou, agrupando por forma em vez de por
pacote, e ele passa com folga:

    metodo:  234 views, 4 inscritos -> 1,71%
    fato:  5.046 views, 4 inscritos -> 0,08%
    razao 21,6x, p exato = 0,00023

Ou seja: agrupado, o efeito e enorme e aparece; por pacote, o mesmo dado nao
diz nada. A diferenca esta em quantos inscritos caem em cada lado, e um pacote
sozinho quase nunca tem inscrito nenhum para cair.

ATE ONDE DA PARA IR. Com a taxa base de hoje, o tamanho minimo por grupo para
80% de poder e alfa de 5%:

    razao 21,6x  ->    270 views por grupo   (por isso o 482 apareceu)
    razao    5x  ->  2.350 views por grupo
    razao    3x  ->  6.701 views por grupo
    razao    2x  -> 20.930 views por grupo   (mais que a frota inteira ja teve)

Entao: diferenca GROSSA de forma da para medir; escolher entre duas formas boas
nao da, e nao vai dar tao cedo. Quem afirmar que uma forma boa bate outra forma
boa esta lendo ruido.

Uso:
    python3 fabrica/conversao.py grupos.json
    # {"metodo": [[204,3],[30,1]], "fato": [[1444,2],[1714,2],[1888,0]]}
"""
from __future__ import annotations

import json
import math
import sys

# 80% de poder, alfa 5% bicaudal.
Z_PODER, Z_ALFA = 0.84, 1.96


def taxa(pares) -> tuple[int, int, float]:
    """(views, inscritos, taxa) de uma lista de [views, inscritos]."""
    v = sum(int(a) for a, _ in pares)
    s = sum(int(b) for _, b in pares)
    return v, s, (s / v if v else 0.0)


def p_exato(va: int, sa: int, vb: int, sb: int) -> float:
    """P(grupo A ficar com >= sa inscritos | a taxa e a MESMA nos dois).

    Teste exato condicional: dado o total de inscritos, a divisao entre os dois
    grupos segue uma binomial com p = views_A / views_totais. E o teste certo
    aqui porque nao supoe nada sobre a taxa — so sobre ela ser igual.
    """
    n = sa + sb
    if n == 0 or (va + vb) == 0:
        return 1.0
    pa = va / (va + vb)
    return sum(math.comb(n, i) * pa**i * (1 - pa)**(n - i)
               for i in range(sa, n + 1))


def views_para_detectar(razao: float, base: float) -> float:
    """Views POR GRUPO para separar duas taxas cuja razao e `razao`.

    Aproximacao de Poisson com a raiz quadrada estabilizando a variancia. Serve
    para dizer 'ainda nao da', que e a resposta na maioria das rodadas.
    """
    if razao <= 1 or base <= 0:
        return float("inf")
    return (Z_ALFA + Z_PODER)**2 / 2 / (base * (math.sqrt(razao) - 1)**2)


def zeros_esperados(pares, base: float) -> float:
    """Quantos itens com ZERO inscrito uma taxa unica ja explicaria."""
    return sum(math.exp(-base * int(v)) for v, _ in pares)


def compara(grupos: dict) -> list[str]:
    nomes = list(grupos)
    if len(nomes) != 2:
        return [f"precisa de exatamente dois grupos, vieram {len(nomes)}"]
    a, b = nomes
    va, sa, ta = taxa(grupos[a])
    vb, sb, tb = taxa(grupos[b])
    base = (sa + sb) / (va + vb) if (va + vb) else 0.0

    notas = [f"{a}: {va} views, {sa} inscritos -> {100*ta:.2f}%",
             f"{b}: {vb} views, {sb} inscritos -> {100*tb:.2f}%"]
    if not (ta and tb):
        maior, menor = max(ta, tb), min(ta, tb)
        notas.append("um dos grupos tem taxa zero — a razao nao existe, "
                     "e o que decide e o teste exato abaixo")
    else:
        notas.append(f"razao: {max(ta,tb)/min(ta,tb):.1f}x")

    p = p_exato(va, sa, vb, sb) if ta >= tb else p_exato(vb, sb, va, sa)
    notas.append(f"P(essa divisao ou mais extrema | mesma taxa) = {p:.5f}")
    notas.append("DISTINGUIVEL de acaso" if p < 0.05
                 else "NAO distinguivel de acaso — nao conclua nada da razao")

    # E o aviso que evita a leitura errada mais comum.
    todos = grupos[a] + grupos[b]
    esperado = zeros_esperados(todos, base) if base else 0.0
    observado = sum(1 for _, s in todos if not int(s))
    notas.append(f"itens com zero inscrito: {observado} observados, "
                 f"{esperado:.1f} ja explicados so pela exposicao")
    if base:
        notas.append(f"na taxa base ({100*base:.3f}%) um inscrito esperado "
                     f"pede {1/base:,.0f} views — abaixo disso, zero nao e "
                     f"resultado, e falta de exposicao")
    return notas


def main(caminho: str) -> int:
    grupos = json.load(open(caminho, encoding="utf-8"))
    for linha in compara(grupos):
        print(f"  {linha}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    raise SystemExit(main(sys.argv[1]))
