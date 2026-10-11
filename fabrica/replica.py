"""Escolhe qual das TRES leituras de contador vale, e qual gravar.

POR QUE ISTO EXISTE, e e a terceira vez que o mesmo defeito me pega.

O contador de view do YouTube e servido por REPLICAS, e algumas estao
atrasadas. Tres leituras na mesma rodada discordam, e a escolha entre elas foi
prosa na rotina ate 11/10/2026 — eu fazia no olho, toda rodada.

O que foi medido, em ordem:

  688 (09/10, `critico`) — a MEDIANA das tres devolve a replica ATRASADA. Das
  17 pecas que mudaram, TODAS subiram na terceira leitura e NENHUMA na segunda.
  Um contador de view so ATRASA, nunca adianta, entao o estimador e o MAXIMO,
  declarado como PISO, com a faixa ao lado.

  707 (10/10, `alto`) — `grava_metricas_janela` grava a replica DAQUELA
  chamada, nao o maximo. Gravar a chamada errada SUBESTIMA PARA SEMPRE: no
  `ZxHWcfDNovM` as leituras deram 830, 833, 830 e a gravacao guardou 830.

  708 (10/10, `alto`, e substitui o procedimento do 707) — a replica atrasada e
  da CHAMADA INTEIRA, nao de cada id. As quatro pecas que divergiram divergiram
  com a MESMA forma {alto, baixo, alto}; as outras dezesseis vieram identicas.
  Logo nao se caca o maximo peca por peca: compara-se a SOMA das tres chamadas
  e grava-se a de soma maxima, em UM statement (702).

E o que NAO sobreviveu: a ordem das replicas nao tem regra. A fresca foi a
terceira em 09/10, a segunda as 07:09 e a primeira e a terceira as 08:08.
**Nunca leia nada pela ORDEM.**
"""

from __future__ import annotations


def soma(leitura: dict[str, int]) -> int:
    """Soma dos contadores de uma chamada. E o criterio do 708."""
    return sum(leitura.values())


def chamada_para_gravar(leituras: list[dict[str, int]]) -> int:
    """Indice da chamada de SOMA MAXIMA — a que deve ir para o banco.

    Empate devolve a PRIMEIRA, porque com soma igual as chamadas sao
    equivalentes para o que o 708 mede e escolher a ultima so adicionaria
    dependencia da ordem, que e justamente o que o 708 enterrou.
    """
    if not leituras:
        raise ValueError("sem leituras")
    somas = [soma(x) for x in leituras]
    return somas.index(max(somas))


def piso(leituras: list[dict[str, int]]) -> dict[str, int]:
    """O estimador do 688: MAXIMO por id, entre as chamadas, como PISO.

    Id ausente numa chamada NAO vira zero — ausencia e silencio, nao leitura de
    zero, e tratar como zero puxaria o maximo para baixo em peca que so apareceu
    numa das chamadas. O 665 e do mesmo feitio: agregado esconde chamada que
    falhou, e por isso cada requisicao tem de ser conferida pelo `status_code`
    ANTES de chegar aqui.
    """
    fora: dict[str, int] = {}
    for leitura in leituras:
        for vid, n in leitura.items():
            if vid not in fora or n > fora[vid]:
                fora[vid] = n
    return fora


def faixa(leituras: list[dict[str, int]]) -> dict[str, tuple[int, int]]:
    """Minimo e maximo por id. O piso vai SEMPRE com a faixa ao lado (688)."""
    fora: dict[str, tuple[int, int]] = {}
    for leitura in leituras:
        for vid, n in leitura.items():
            if vid not in fora:
                fora[vid] = (n, n)
            else:
                lo, hi = fora[vid]
                fora[vid] = (min(lo, n), max(hi, n))
    return fora


def divergentes(leituras: list[dict[str, int]]) -> dict[str, tuple[int, ...]]:
    """Ids que NAO vieram identicos nas chamadas, com os valores na ordem lida.

    Serve para conferir a assinatura do 708: se a divergencia e da chamada, os
    divergentes compartilham a MESMA FORMA (todos {alto, baixo, alto}, por
    exemplo). Se as formas discordarem entre si, a hipotese do 708 nao se aplica
    aquela rodada e o relato tem de dizer isso em vez de gravar no automatico.
    """
    fora: dict[str, tuple[int, ...]] = {}
    for vid in piso(leituras):
        serie = tuple(x[vid] for x in leituras if vid in x)
        if len(set(serie)) > 1:
            fora[vid] = serie
    return fora


def mesma_forma(leituras: list[dict[str, int]]) -> bool:
    """True quando todo divergente tem a mesma forma relativa — a marca do 708.

    A forma e o RANKING dos valores na ordem lida, nao os valores: `833, 830,
    833` e `91, 90, 91` tem a mesma forma. Sem divergente, devolve True — nao
    ha contradicao a relatar.
    """
    formas = set()
    for serie in divergentes(leituras).values():
        ordenados = sorted(set(serie))
        formas.add(tuple(ordenados.index(n) for n in serie))
    return len(formas) <= 1
