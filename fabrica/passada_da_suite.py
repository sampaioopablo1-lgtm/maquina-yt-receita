# -*- coding: utf-8 -*-
"""A comparacao da suite lia ARQUIVO DE OUTRA SESSAO sem reclamar.

MEDIDO em 21/10 as 21:0x, e o erro foi meu, nesta rodada. Eu comparo a passada
contra a linha de base desta sessao assim:

    comm -13 base.norm s<rodada>.norm

e o `.norm` e escrito DEPOIS de o pytest sair. Logo "o arquivo existe" foi, por
semanas, o meu discriminador de "a passada terminou". **Nesta rodada ele mentiu:**
havia um `s2007b.norm` de **20/10 as 20:42** — resto de uma rodada da sessao
anterior, com o MESMO nome —, a suite estava em 43%, e o `comm` devolveu
*"identico a base"*. Eu quase relatei isso ao dono.

**A familia e a de 19/10 as 16:2x, na forma mais caustica dela:**

| | |
|---|---|
| 17/10 | instrumento que devolve **VAZIO** nao prova ausencia |
| 19/10 | arquivo **VAZIO** nao prova morte (o `.norm` a meio de escrever) |
| 20/10 01:4x | instrumento **CHEIO** nao prova presenca (o `pgrep` se vendo) |
| 20/10 09:3x | **000** nao diz de QUEM e o zero |
| **21/10 21:0x** | **arquivo que EXISTE nao prova que e DESTA execucao** |

E ela e a pior das cinco por um motivo: as outras devolvem silencio ou erro, e
**esta devolve a resposta CONFORTAVEL** — "nada mudou" e exatamente o que eu
espero ler.

**Quem me pegou foi o `processo_vivo`**, que respondeu VIVO contradizendo a
existencia do arquivo. Este modulo poe esse par numa chamada so e **RECUSA
comparar** quando a passada nao esta provada, do jeito que o `porta1` recusa
janela curta.

OS TRES DISCRIMINADORES, e nenhum basta sozinho:
  1. o log termina com a LINHA DE RESUMO do pytest (`N failed, M passed`) —
     sem ela a passada nao terminou, e foi por nao ter isto que eu li 43%;
  2. o `.norm` e mais NOVO que o log — resto de sessao e mais velho;
  3. a contagem de linhas do `.norm` BATE com o numero de falhas do resumo —
     se divergir, o `.norm` e de outra passada que por acaso e mais nova.
"""
from __future__ import annotations

import os
import re
import subprocess

RESUMO = re.compile(r"(\d+) failed,\s+(\d+) passed(?:,\s+(\d+) skipped)?")


def resumo_do_log(caminho: str) -> dict | None:
    """A linha de resumo do pytest, ou None se a passada nao terminou.

    Le o FIM do arquivo, porque o resumo e a ultima linha — e nao o comeco, que
    foi a fatia errada que me custou a leitura do proxy em 21/10 as 19:0x.
    """
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8", errors="replace") as f:
        try:
            f.seek(max(0, os.path.getsize(caminho) - 4096))
        except OSError:
            pass
        fim = f.read()
    m = None
    for m in RESUMO.finditer(fim):
        pass
    if m is None:
        return None
    return {"falhas": int(m.group(1)), "passam": int(m.group(2)),
            "skip": int(m.group(3) or 0)}


def passada_provada(log: str, norm: str) -> dict:
    """Os tres discriminadores. `provada: False` com o motivo, nunca silencio."""
    r = resumo_do_log(log)
    if r is None:
        return {"provada": False, "resumo": None,
                "motivo": ("o log nao termina com a linha de resumo do pytest: a"
                           " passada NAO terminou (ou morreu antes dela). Era"
                           " isto que faltava quando eu li 43%% como pronto.")}
    if not os.path.exists(norm):
        return {"provada": False, "resumo": r,
                "motivo": "o `.norm` nao existe: a normalizacao nao foi escrita."}
    if os.path.getmtime(norm) < os.path.getmtime(log):
        return {"provada": False, "resumo": r,
                "motivo": ("o `.norm` e MAIS VELHO que o log — ele e resto de"
                           " outra passada, e foi exatamente este o caso de"
                           " 21/10 as 21:0x (arquivo de 20/10 com o mesmo"
                           " nome).")}
    n = sum(1 for linha in open(norm, encoding="utf-8") if linha.strip())
    if n != r["falhas"]:
        return {"provada": False, "resumo": r, "linhas": n,
                "motivo": ("o `.norm` tem %d linha(s) e o resumo diz %d"
                           " falha(s): ele e de OUTRA passada, mesmo sendo mais"
                           " novo." % (n, r["falhas"]))}
    return {"provada": True, "resumo": r, "linhas": n,
            "motivo": "os tres discriminadores passaram."}


def compara(base: str, log: str, norm: str) -> dict:
    """Compara contra a base nos DOIS sentidos — ou RECUSA, com o motivo."""
    p = passada_provada(log, norm)
    if not p["provada"]:
        return {"comparou": False, "motivo": p["motivo"], "resumo": p["resumo"]}
    if not os.path.exists(base):
        return {"comparou": False, "resumo": p["resumo"],
                "motivo": ("a linha de base desta sessao nao existe em %s — e"
                           " comparar contra o numero ESCRITO na rotina e o que"
                           " envelhece (753)." % base)}
    novas = subprocess.run(["comm", "-13", base, norm],
                           capture_output=True, text=True).stdout.splitlines()
    sumidas = subprocess.run(["comm", "-23", base, norm],
                             capture_output=True, text=True).stdout.splitlines()
    return {"comparou": True, "resumo": p["resumo"], "linhas": p["linhas"],
            "novas": [x for x in novas if x.strip()],
            "desaparecidas": [x for x in sumidas if x.strip()],
            "identico": not [x for x in novas + sumidas if x.strip()]}


def vivo(padrao: str = "pytest tests") -> bool | None:
    """Delega ao `processo_vivo`, que e o dono — foi ele que me pegou."""
    try:
        import processo_vivo
        return processo_vivo.vivo(padrao)
    except Exception:
        return None


def relato(base: str, log: str, norm: str, padrao: str = "pytest tests") -> str:
    c = compara(base, log, norm)
    linhas = []
    if not c["comparou"]:
        v = vivo(padrao)
        linhas.append("SUITE: NAO COMPARADA — %s" % c["motivo"])
        if c.get("resumo"):
            linhas.append("  o resumo lido foi: %s" % c["resumo"])
        linhas.append("  processo de pytest VIVO agora? %s (do `processo_vivo`,"
                      " que e quem me pegou em 21/10 as 21:0x)" % v)
        linhas.append("  isto RECUSA em vez de devolver 'identico a base', que e"
                      " a resposta confortavel e era a errada.")
        return "\n".join(linhas)
    r = c["resumo"]
    linhas.append("SUITE: %d falhas, %d passam, %d skip — passada PROVADA (log"
                  " com resumo, `.norm` mais novo que o log, %d linha(s) batendo"
                  " com as falhas)." % (r["falhas"], r["passam"], r["skip"],
                                        c["linhas"]))
    if c["identico"]:
        linhas.append("  conjunto IDENTICO a linha de base desta sessao: `comm`"
                      " vazio nos DOIS sentidos.")
    else:
        if c["novas"]:
            linhas.append("  NOVAS (%d):" % len(c["novas"]))
            linhas.extend("    " + x for x in c["novas"])
        if c["desaparecidas"]:
            linhas.append("  DESAPARECIDAS (%d) — e isto tambem pede leitura:"
                          % len(c["desaparecidas"]))
            linhas.extend("    " + x for x in c["desaparecidas"])
    return "\n".join(linhas)


def main(argv=None) -> int:
    import sys as _sys
    argv = list(argv if argv is not None else _sys.argv[1:])
    if len(argv) < 3:
        print("uso: passada_da_suite.py <base.norm> <passada.log> <passada.norm>")
        return 0
    print(relato(argv[0], argv[1], argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
