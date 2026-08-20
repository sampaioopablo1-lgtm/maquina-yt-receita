#!/usr/bin/env python3
"""A que horas o video encontra o publico dele.

## O que estava acontecendo

Nada decidia a hora de publicacao. O pacote subia quando o render terminava, e
o render comecava quando o `diario.yml` disparava — a cada trinta minutos,
sobre uma fila ordenada por distancia da meta. A hora era, literalmente, sobra
de escalonamento de runner.

Medido em 20/08/2026, hora UTC de publicacao dos shorts ja no ar:

    seviye-seviye  (Istambul, UTC+3)   00, 01, 06 UTC  ->  03h, 04h, 09h local
    kolejny-poziom (Varsovia, UTC+2)   00, 01, ...     ->  02h, 03h local
    next-level-money (Nova York)       00, 01, 22, 23  ->  20h, 21h, 18h, 19h
    epomeno-epipedo (Atenas, UTC+3)    03, 04, 05      ->  06h, 07h, 08h local

O `seviye-seviye` e o canal com o MELHOR short da frota — mediana de 81,5
views/dia — e dois tercos das publicacoes dele cairam na madrugada de Istambul.

## O que este arquivo afirma, e o que nao afirma

Ele NAO afirma saber a melhor hora de cada canal. Isso e dado que a frota ainda
nao tem: seriam necessarios shorts iguais publicados em horas diferentes, e a
amostra atual mistura hora, tema e formato.

Ele afirma o que da para defender sem medicao: **madrugada e pior**. Um short
depende do engajamento da primeira hora para o feed distribuir, e a primeira
hora as tres da manha compete com ninguem acordado.

Entao a regra e uma EXCLUSAO, nao uma escolha: entre 01h e 08h local o canal
sai do topo da fila. Ele nao e bloqueado — se nao houver mais nada pronto, ele
dispara igual, porque frota parada nao rende nada. E preferencia, nao portao.

A faixa boa fica registrada como experimento aberto. Quando houver dado de
verdade, o numero muda aqui e o motivo vai junto.

## Por que zoneinfo e nao offset fixo

Metade destes fusos tem horario de verao. Offset fixo acerta metade do ano e
erra a outra metade, calado — que e o tipo de defeito que esta operacao ja
colecionou demais.
"""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

# Fuso do PUBLICO do canal, nao do dono. O que decide e onde esta quem assiste.
#
# Os canais em ingles sao os unicos ambiguos de verdade: `en` nao e um pais. Vao
# para Nova York porque e o maior mercado unico de lingua inglesa em consumo de
# YouTube, e porque a janela de Nova York cobre parcialmente Londres a tarde. Se
# o dado mostrar publico majoritariamente britanico ou indiano, muda aqui.
FUSO = {
    "agla-level":         "Asia/Kolkata",
    "cocina-por-niveles": "America/Mexico_City",
    "epomeno-epipedo":    "Europe/Athens",
    "game-money-lab":     "America/New_York",
    "kolejny-poziom":     "Europe/Warsaw",
    "labtreinamento":     "America/Sao_Paulo",
    "next-level-money":   "America/New_York",
    "nivel-do-jogo":      "America/Sao_Paulo",
    "resep-naik-level":   "Asia/Jakarta",
    "seja-mais-magra":    "America/Sao_Paulo",
    "setiap-level":       "Asia/Jakarta",
    "seviye-seviye":      "Europe/Istanbul",
    "sx-educacao":        "America/Sao_Paulo",
}

# A faixa MORTA, em hora local. Deliberadamente conservadora: ela afirma so o
# que nao precisa de medicao para ser verdade. Tudo fora dela e tratado como
# igualmente bom, porque a frota ainda nao tem dado para ranquear as horas.
MORTA_DE, MORTA_ATE = 1, 8


def fuso(slug: str) -> ZoneInfo | None:
    z = FUSO.get(slug)
    return ZoneInfo(z) if z else None


def hora_local(slug: str, agora: dt.datetime | None = None) -> int | None:
    """Hora local do publico do canal, 0 a 23. `None` se o canal nao tem fuso."""
    z = fuso(slug)
    if z is None:
        return None
    agora = agora or dt.datetime.now(dt.timezone.utc)
    if agora.tzinfo is None:
        agora = agora.replace(tzinfo=dt.timezone.utc)
    return agora.astimezone(z).hour


def na_janela(slug: str, agora: dt.datetime | None = None) -> bool:
    """Este canal esta numa hora util agora?

    Canal sem fuso declarado devolve True — desconhecido nao vira penalidade,
    senao um canal novo ficaria no fim da fila para sempre por um dado que
    ninguem preencheu.
    """
    h = hora_local(slug, agora)
    if h is None:
        return True
    return not (MORTA_DE <= h < MORTA_ATE)


def horas_ate_a_janela(slug: str, agora: dt.datetime | None = None) -> int:
    """Quantas horas faltam para o canal sair da faixa morta. 0 se ja esta fora."""
    h = hora_local(slug, agora)
    if h is None or not (MORTA_DE <= h < MORTA_ATE):
        return 0
    return MORTA_ATE - h


def relatorio(agora: dt.datetime | None = None) -> str:
    agora = agora or dt.datetime.now(dt.timezone.utc)
    linhas = [f"janela de publicacao — {agora:%H:%M} UTC",
              f"(faixa morta: {MORTA_DE:02d}h as {MORTA_ATE:02d}h local)", ""]
    for slug in sorted(FUSO):
        h = hora_local(slug, agora)
        ok = na_janela(slug, agora)
        falta = horas_ate_a_janela(slug, agora)
        marca = "  " if ok else "->"
        obs = "" if ok else f"  dorme, abre em {falta}h"
        linhas.append(f"{marca} {slug:<20} {h:02d}h local{obs}")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relatorio())
