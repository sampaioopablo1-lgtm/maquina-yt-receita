#!/usr/bin/env python3
"""A peça cabe no PORTÃO e erra a MIRA DO CANAL — dizer isso antes do render.

POR QUE ISTO EXISTE, medido em 13/10/2026 às 06:1x. Escrevendo o
`labtreinamento-s032` eu produzi uma spec de **27,8 s reais previstos** no Piper.
O portão `duracao` aprovou, e com razão: ele cobra 18 a 45 s, que é a faixa da
FROTA. Mas o `labtreinamento` tem `ALVO_POR_CANAL = (20,0 a 26,0)` desde 09/10,
medido (698) — e 27,8 está fora dela. **Portão verde não dispensa a mira.**

Eu peguei à mão nesta rodada. Na próxima eu não pegaria, e é por isso que a
conta sai da minha cabeça.

**POR QUE ISTO NÃO É UM AVISO DENTRO DO `prontidao`, e a razão é medida:** das
specs do `labtreinamento` com voz modelada, **44 ficam fora da mira no mundo
`edge` e 28 no `piper`** — quase todas peças históricas, escritas antes de o
override existir. Um aviso de portão que dispara 44 vezes é um aviso que as
pessoas aprendem a ignorar, e aí ele deixa de avisar o caso que importa. Então
isto é um RELATO que se roda na spec que está sendo escrita, como o
`concentracao.py`.

**E não é limiar novo:** os números são `ensaio.ALVO_POR_CANAL`, que é medição do
próprio canal, e `ensaio.duracao_real_prevista`, que é o fator do Piper medido no
711/714. Canal sem override não tem mira própria e o relato diz isso em vez de
inventar uma.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import ensaio  # noqa: E402

PROVEDORES = ("edge", "piper")


def previsoes(spec: dict) -> dict[str, float]:
    """Duração REAL prevista em cada mundo de provedor. Vazio sem short/voz."""
    short, voz = spec.get("short") or [], spec.get("voz", "")
    if not short or voz not in ensaio.MODELO_VOZ:
        return {}
    return {p: round(ensaio.duracao_real_prevista(short, voz, p), 1)
            for p in PROVEDORES}


def confere(spec: dict) -> dict:
    """A peça cai na mira MEDIDA do canal, nos dois mundos de provedor?

    `tem_mira` é False quando o canal não tem override — e aí não há o que
    conferir, porque a mira da frota é o que o portão já cobra.
    """
    canal = spec.get("slug") or ""
    prev = previsoes(spec)
    if canal not in ensaio.ALVO_POR_CANAL:
        return {"canal": canal, "tem_mira": False, "previsoes": prev,
                "fora": [], "motivo": f"canal {canal!r} nao tem ALVO_POR_CANAL "
                "medido — a mira da frota e a que o portao `duracao` ja cobra"}
    lo, hi = ensaio.ALVO_POR_CANAL[canal]
    fora = [p for p, d in prev.items() if not (lo <= d <= hi)]
    return {"canal": canal, "tem_mira": True, "mira": (lo, hi),
            "previsoes": prev, "fora": fora,
            "motivo": None if not fora else (
                f"{', '.join(fora)} fora da mira medida {lo} a {hi} s. O portao "
                "`duracao` cobra a faixa da FROTA, que e mais larga, e NAO "
                "reprova isto — portao verde nao dispensa a mira do canal "
                "(698).")}


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    r = confere(spec)
    nome = spec.get("pacote", caminho)
    if not r["previsoes"]:
        return f"{nome}: sem short ou voz sem modelo — nada a conferir."
    linhas = [f"MIRA de {nome} ({r['canal']}): " + ", ".join(
        f"{p} {d} s" for p, d in sorted(r["previsoes"].items()))]
    if not r["tem_mira"]:
        linhas.append("  " + r["motivo"])
        return "\n".join(linhas)
    linhas.append(f"  mira medida do canal: {r['mira'][0]} a {r['mira'][1]} s")
    if r["fora"]:
        linhas.append("  >> FORA: " + r["motivo"])
    else:
        linhas.append("  dentro da mira nos dois mundos de provedor.")
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("uso: mira.py fabrica/specs/<spec>.json [...]")
        return 2
    ruim = 0
    for a in sys.argv[1:]:
        t = relato(a)
        print(t)
        if "FORA" in t:
            ruim += 1
    return 1 if ruim else 0


if __name__ == "__main__":
    raise SystemExit(main())
