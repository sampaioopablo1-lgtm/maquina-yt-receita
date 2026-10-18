#!/usr/bin/env python3
"""O registro DEPOIS de publicar, feito pelo RUNNER e nao por mim.

POR QUE ISTO EXISTE, e e a soma de tres defeitos medidos no CLAUDE.md:
  * o corpus de titulos ficou SETE rodadas sem receber as pecas publicadas
    (13/10) — e corpus atrasado nao barra duplicata, falha permissiva;
  * a linha em `videos` ficou DOZE publicacoes sem ser escrita (726) porque o
    passo nao tinha instrumento;
  * dezessete duracoes parqueadas sairam da minha CABECA (16/10), e o
    parqueamento so virou incondicional em 18/10.
Os tres sao o MESMO erro: passo manual depois de publicar, que eu esqueco
exatamente na rodada em que estou olhando outra coisa. O dono pediu "100%
automatico" (09/10, 18/10). Este modulo da ao `retomar.yml` o que eu fazia a
mao: le o registro que o `publicar.py` ja escreve, e produz as DUAS gravacoes
que faltavam — o SQL parqueado sai pelo `registro_videos.py` e o corpus pelo
`corpus_atrasado.py`, que ja existiam; aqui mora o PARQUEAMENTO DA DURACAO,
que exige a previsao nos dois mundos e o PROVEDOR medido.

O provedor vem da contagem de avisos do run do render (`avisos_do_run.py`),
pelo 733. Contagem ausente ou regime MISTO nao parqueia: ponto sem mundo de
provedor nao entra na serie (`test_o_run_pode_ser_MISTO.py`), e inventar o
mundo e o erro que o 733 nomeia.
"""
from __future__ import annotations

import json
import sys

import duracao_a_medir as DM
import ensaio
import voz_unica as VU
from registro_anota import linhas_do_registro


def previsoes(sp: dict) -> tuple[float, float]:
    """Previsao do short nos DOIS mundos, pela mesma funcao do portao."""
    cenas, voz = sp["short"], sp["voz"]
    return (round(ensaio.duracao_real_prevista(cenas, voz, "edge"), 1),
            round(ensaio.duracao_real_prevista(cenas, voz, "piper"), 1))


def linhas_de_short(reg) -> list[dict]:
    """So a peca curta entra na serie do residuo: a banda foi medida em short."""
    return [l for l in linhas_do_registro(reg)
            if l.get("youtube_id") and (
                l.get("formato") == "shorts" or str(l.get("slug", "")).endswith("-short"))]


def registros(reg, sp: dict, avisos_piper, job, pacote: str | None = None) -> tuple[list[dict], str]:
    """Os registros para `duracao_a_medir.parqueia`, ou lista vazia e o motivo."""
    if avisos_piper is None or not job:
        return [], "sem contagem de avisos do render: nao parqueio (733 — provedor se mede)"
    cenas = len(sp.get("short") or [])
    regime = VU.regime(set(range(int(avisos_piper))), cenas)
    if regime == "misto":
        return [], (f"run MISTO ({avisos_piper} de {cenas} cenas pelo Piper): "
                    "ponto sem mundo de provedor, nao entra na serie")
    if regime == "nenhuma":
        return [], "spec sem cenas de short: nada a parquear"
    pe, pp = previsoes(sp)
    nome = pacote or sp.get("pacote") or (reg.get("pacote") if isinstance(reg, dict) else None)
    saida = []
    for l in linhas_de_short(reg):
        saida.append({"pacote": nome, "youtube_id": l["youtube_id"],
                      "prev_edge": pe, "prev_piper": pp, "provedor": regime,
                      "job": str(job), "em": l.get("publicado_em") or "?"})
    return saida, ("" if saida else "registro sem linha de short com youtube_id")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        print("uso: pos_publicacao.py <registro.json> <spec.json> --avisos N --job ID", file=sys.stderr)
        return 2
    reg = json.load(open(argv[0], encoding="utf-8"))
    sp = json.load(open(argv[1], encoding="utf-8"))
    avisos = job = None
    if "--avisos" in argv:
        v = argv[argv.index("--avisos") + 1]
        avisos = int(v) if v not in ("", "null", "None") else None
    if "--job" in argv:
        v = argv[argv.index("--job") + 1]
        job = v if v not in ("", "null", "None") else None
    regs, motivo = registros(reg, sp, avisos, job)
    if not regs:
        print(f"::warning::duracao NAO parqueada: {motivo}", flush=True)
        return 0
    for r in regs:
        novo = DM.parqueia(r)
        print(f"::notice::PARQUEADO {r['pacote']} {r['youtube_id']} provedor={r['provedor']} "
              f"edge={r['prev_edge']} piper={r['prev_piper']} job={r['job']}"
              + ("" if novo else " (ja estava)"), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
