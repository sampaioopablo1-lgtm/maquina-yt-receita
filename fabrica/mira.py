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

**E ESTE MÓDULO TINHA UM BURACO MEDIDO EM 13/10 ÀS 22:2x — aprendizado 739.** A
mira do `labtreinamento` é sobre a duração **REAL**, e o que eu confiro aqui é a
**PREVISÃO**. As duas peças do canal narradas pelo edge (`s033` e `s034`) passaram
por esta conferência com a previsão DENTRO e saíram em **27 e 28 s reais** — fora
da mira. O real fica **sempre acima** da previsão do provedor que de fato narrou
(14 de 14), pela banda OBSERVADA em `RESIDUO_OBSERVADO` — hoje 0,9 a
3,7 s (752). O teto dela JA foi ampliado uma vez por medicao; nunca escreva o
numero em outro lugar do modulo, porque foi exatamente isso que ficou atrasado
na mensagem do relato e eu so vi na rodada seguinte.

Então `faixa_real` acrescenta essa banda ao relato: previsão de 25,6 põe o real
entre 26,5 e 28,0, e o relato DIZ que isso passa do teto da mira. **Ele informa e
NÃO reprova**, e a razão é a amostra: n pequeno, e a banda varia sem lei
estável (duas previsões a um décimo deram reais a um segundo de distância), e
reprovar por uma banda assim seria inventar portão com cinco pontos. Quem decide
encurtar é quem escreve a peça, com o número na frente.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import ensaio  # noqa: E402

PROVEDORES = ("edge", "piper")

# Resíduo OBSERVADO entre a previsão do provedor que de fato narrou (medido pela
# anotação do job, 733) e a duração REAL. Cinco pontos, 13/10: +0,9 / +1,1 / +1,9
# / +1,3 / +2,4 s. Todos POSITIVOS. Isto NÃO é limiar — nada reprova por causa
# dele; ele entra no relato para que quem escreve veja onde o real deve cair.
RESIDUO_OBSERVADO = (0.5, 3.7)
# 752, 14/10 08:2x: o TETO da banda CAIU, e por medicao. O `labtreinamento-s043`
# previa 23,3 no edge (provedor MEDIDO pela anotacao) e saiu com 27 REAIS —
# residuo +3,7 s, contra o maximo de 2,4 que treze pontos sustentavam. Isto NAO
# e limiar novo: e a faixa OBSERVADA, e ela so se mexe quando a observacao sai
# dela. O piso de 0,9 nao mudou NAQUELE dia, e a largura passou de 1,5 para
# 2,8 s — ou seja,
# a banda agora cobre quase o dobro, o que a torna MENOS util e isso vai dito em
# vez de escondido.
RESIDUO_N = 27  # 741 acrescentou o s035 (24,8 -> 27, +2,2): DENTRO da banda,
#                 logo os LIMITES nao mudaram — so o numero de pontos que a sustenta.
#                 14/10 06:2x: o s041 (edge 24,6 -> real 27) deu +2,4 — EMPATADO
#                 com o teto da banda, o decimo segundo ponto e o segundo a tocar
#                 o limite superior. Os LIMITES seguem intocados porque 2,4 ja e
#                 o maximo; o proximo ponto acima dele QUEBRA a banda, e e isso
#                 que o teste do 739 existe para obrigar a reler.


def faixa_real(estimado: float) -> tuple[float, float]:
    """Onde o REAL deve cair, dada uma previsão, pela banda OBSERVADA do 739."""
    lo, hi = RESIDUO_OBSERVADO
    return (round(estimado + lo, 1), round(estimado + hi, 1))


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
    # o 739: a mira e sobre o REAL e isto acima confere a PREVISAO.
    teto = r["mira"][1]
    for prov, d in sorted(r["previsoes"].items()):
        lo, hi = faixa_real(d)
        aviso = (" PASSA do teto da mira" if lo > teto
                 else " pode passar do teto" if hi > teto else " cabe na mira")
        linhas.append(
            f"  se {prov} narrar, o REAL deve cair entre {lo} e {hi} s —{aviso}"
            f" ({teto}). Resíduo OBSERVADO, n={RESIDUO_N} (739): o real ficou"
            f" sempre ACIMA da previsão, por {RESIDUO_OBSERVADO[0]:.1f} a"
            f" {RESIDUO_OBSERVADO[1]:.1f} s. NAO reprova.")
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
