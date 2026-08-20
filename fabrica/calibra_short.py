"""Calibra o modelo de voz para SHORT, a partir dos shorts que ja foram ao ar.

## Por que este arquivo existe

O modelo `MODELO_VOZ` e ajustado so em cena de LONGO: a calibracao le os
`legendas.srt` do bucket, e short queima a legenda em vez de exportar `.srt`.
A constante (R, P) nunca viu uma cena de short.

Durante duas semanas eu compensei isso a mao. A cada short publicado eu media
UM erro, escrevia no comentario do `prontidao.MARGEM_SHORT` e subia a margem
para cobrir o pior caso ate ali — 3%, depois 5%, 7%, 7,5%, quatro vezes em
dias. Cada subida foi honesta e cada uma estava errada pelo mesmo motivo: o
MAXIMO de uma amostra cresce com n, entao "cobrir o pior caso" nunca converge.

O que fechou a questao nao foi estatistica melhor, foi olhar onde o dado ja
estava. A esteira grava `videos.duracao_s` com o ffprobe do arquivo montado —
ou seja, a duracao REAL de todo short publicado estava no banco desde o
primeiro dia. Eu media de um em um o que dava para medir de uma vez so, que e
a mesma classe de erro do aprendizado 378 (contar arquivo em vez de trabalho).

Com 30 medidas validas de uma vez o quadro muda de figura: nao e dispersao em
torno do certo, e VIES. 28 das 30 dao para cima, mediana +4,7%. Margem de
seguranca nao conserta vies — ela so esconde, e cobra o preco de reprovar
roteiro bom. O que conserta e corrigir a PREVISAO e deixar a margem cobrir so
o que sobra.

## Como rodar

    python3 fabrica/calibra_short.py

Le `medidas_short.tsv` (medida bruta, uma linha por short publicado) e a spec
de cada uma, e imprime o vies e o residuo. Quando entrar medida nova, atualize
o TSV com

    select slug, duracao_s from videos where slug like '%-short'
      and duracao_s is not null;

rode isto de novo e leve os dois numeros para `ensaio.VIES_SHORT` e
`prontidao.MARGEM_SHORT`. O teste `test_calibra_short.py` cobra que os tres
concordem, entao a constante nao pode mais andar sozinha.

## O que NAO entra na conta

Medida so calibra quando o texto de hoje e o texto que foi lido. Spec alterada
DEPOIS da publicacao entra no TSV mas fica fora da conta — sao os tres shorts
que eu estiquei em 13/08 e que apareciam como erro de -20%.
"""
import json
import math
import statistics
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from ensaio import MODELO_VOZ, duracao_estimada  # noqa: E402

TSV = RAIZ / "medidas_short.tsv"
SPECS = RAIZ / "specs"


def medidas() -> list[dict]:
    """Uma linha por short publicado, ja com previsao, erro e validade."""
    fora = []
    for linha in TSV.read_text(encoding="utf-8").splitlines():
        if not linha.strip() or linha.startswith("#"):
            continue
        slug, voz, real, publicado, alterada = linha.split("\t")
        spec = SPECS / f"{slug}.json"
        if not spec.exists():
            continue
        sp = json.loads(spec.read_text(encoding="utf-8"))
        short = sp.get("short") or []
        if voz not in MODELO_VOZ or not short:
            continue
        prev = duracao_estimada(short, voz)
        real = float(real)
        fora.append({
            "slug": slug, "voz": voz, "prev": prev, "real": real,
            "erro_pct": (real - prev) / prev * 100,
            # `>` e nao `>=`: alterar no MESMO dia da publicacao e o caso
            # normal — a spec nasce e publica junto. So descarta quem mudou
            # depois.
            "vale": alterada <= publicado,
            "publicado_em": publicado, "alterada_em": alterada,
        })
    return fora


def percentil(valores: list[float], q: float) -> float:
    v = sorted(valores)
    return v[math.ceil(q * len(v)) - 1]


def resumo() -> dict:
    """Vies a aplicar na previsao, e residuo que sobra depois dele."""
    validas = [m for m in medidas() if m["vale"]]
    if not validas:
        raise SystemExit("nenhuma medida valida em medidas_short.tsv")
    erros = [m["erro_pct"] for m in validas]
    vies = 1 + statistics.median(erros) / 100
    residuos = [(m["real"] - m["prev"] * vies) / (m["prev"] * vies) * 100
                for m in validas]
    return {
        "n": len(validas),
        "descartadas": len(medidas()) - len(validas),
        "vies": vies,
        "erro_mediano_pct": statistics.median(erros),
        "positivos": sum(1 for e in erros if e > 0),
        "residuo_p95_pct": percentil(residuos, 0.95),
        "residuo_max_pct": max(residuos),
        "residuo_desvio": statistics.pstdev(residuos),
    }


def main() -> None:
    todas = medidas()
    todas.sort(key=lambda m: m["erro_pct"])
    print(f"{'spec':24}{'voz':34}{'prev':>7}{'real':>7}{'erro':>8}")
    for m in todas:
        marca = "" if m["vale"] else "  <- fora: spec mudou depois de publicar"
        print(f"{m['slug']:24}{m['voz']:34}{m['prev']:7.1f}{m['real']:7.1f}"
              f"{m['erro_pct']:+7.1f}%{marca}")

    r = resumo()
    print(f"\nn={r['n']} validas ({r['descartadas']} descartadas)")
    print(f"  {r['positivos']} de {r['n']} erram para CIMA — e vies, nao ruido")
    print(f"  ensaio.VIES_SHORT      = {r['vies']:.3f}   "
          f"(mediana {r['erro_mediano_pct']:+.1f}%)")
    print(f"  prontidao.MARGEM_SHORT = {r['residuo_p95_pct']/100:.3f}   "
          f"(percentil 95 do residuo; maximo {r['residuo_max_pct']:+.1f}%)")

    # Por voz, so para ver se ja da para trocar a constante unica por tabela.
    por: dict[str, list[float]] = {}
    for m in todas:
        if m["vale"]:
            por.setdefault(m["voz"], []).append(m["erro_pct"])
    print("\npor voz (constante unica so vira tabela com n>=8 em cada uma):")
    for voz, e in sorted(por.items(), key=lambda kv: -len(kv[1])):
        print(f"  {voz:34} n={len(e):2}  mediana {statistics.median(e):+5.1f}%"
              f"  faixa {min(e):+5.1f} a {max(e):+5.1f}")


if __name__ == "__main__":
    main()
