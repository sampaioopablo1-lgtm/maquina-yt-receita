#!/usr/bin/env python3
"""Aviso de dump velho — compartilhado pelas tres auditorias que leem dumps.

Por que existe: em 23/09/2026 a `auditoria_tags.py` reportou 5 achados lendo um
dump de 22/09 16:27, e 3 deles ja estavam resolvidos na conta havia uma hora.
Dump de `wesales/workflows-json/` e FOTOGRAFIA, e envelhece em minutos quando
alguem esta trabalhando na conta. Achado tirado de dump e CANDIDATO, nao item.

Duas checagens, porque uma so nao bastou:

1. `backup_mais_novo` — o arquivo principal esta mais velho que um backup irmao
   em `_antes-*/`? Entao alguem aplicou patch e nao re-exportou. Prova direta,
   mas so funciona para workflow que TEM backup irmao.
2. `muito_atras` — o arquivo esta N horas atras do mais novo da pasta? Nao prova
   nada (workflow que ninguem toca ha dias aparece, e e correto que apareca),
   mas pega o caso que a (1) nao ve. Foi assim que apareceu o `AGENDAR
   Estagnado`: dizia `published` com dump de 28 h antes, e o dono ja o havia
   despublicado.

Uso: `from _frescor import aviso; aviso(DUMPS)` — imprime os blocos se houver o
que avisar, e devolve True se imprimiu alguma coisa.
"""
import datetime
import glob
import json
import os

_FMT = "%Y-%m-%dT%H:%M:%S"


def _updated(caminho):
    try:
        with open(caminho, encoding="utf-8") as fh:
            dado = json.load(fh)
    except (ValueError, OSError):
        return ""
    return ((dado.get("workflow") or dado) or {}).get("updatedAt") or ""


def backup_mais_novo(dumps):
    """{nome: (updatedAt do dump, updatedAt do backup mais novo)} — prova direta."""
    saida = {}
    for caminho in sorted(glob.glob(os.path.join(dumps, "*.json"))):
        arq = os.path.basename(caminho)
        meu = _updated(caminho)
        if not meu:
            continue
        novo = ""
        for backup in glob.glob(os.path.join(dumps, "_antes-*", arq)):
            u = _updated(backup)
            if u > novo:
                novo = u
        if novo and novo > meu:
            saida[arq[:-5]] = (meu, novo)
    return saida


def muito_atras(dumps, horas=12):
    """{nome: (updatedAt, horas atras do mais novo da pasta)} — heuristica."""
    stamps = {}
    for caminho in sorted(glob.glob(os.path.join(dumps, "*.json"))):
        u = _updated(caminho)
        if u:
            stamps[os.path.basename(caminho)[:-5]] = u
    if not stamps:
        return {}, ""
    novo = max(stamps.values())

    def delta(a, b):
        try:
            return (datetime.datetime.strptime(b[:19], _FMT)
                    - datetime.datetime.strptime(a[:19], _FMT)).total_seconds() / 3600.0
        except ValueError:
            return 0.0

    return ({k: (v, round(delta(v, novo), 1))
             for k, v in stamps.items() if delta(v, novo) >= horas}, novo)


def aviso(dumps, horas=12, limite=12):
    """Imprime os dois blocos de aviso. Devolve True se imprimiu algum."""
    falou = False
    atraso = backup_mais_novo(dumps)
    if atraso:
        falou = True
        print("=" * 72)
        print("AVISO DE FRESCOR — %d dump(s) com backup `_antes-*` MAIS NOVO que eles." % len(atraso))
        print("O arquivo principal nao foi re-exportado depois de um patch na conta.")
        print("QUALQUER achado abaixo que envolva estes workflows pode ja estar resolvido:")
        for arq, (meu, novo) in sorted(atraso.items()):
            print("   %-34s dump %s  <  backup %s" % (arq, meu[:19], novo[:19]))
        print("Conferir ao vivo antes de reportar. Em 23/09/2026 a auditoria de tags")
        print("reportou 5 achados e 3 ja estavam resolvidos na conta havia uma hora.")
        print("=" * 72 + "\n")

    velhos, novo = muito_atras(dumps, horas)
    if velhos:
        falou = True
        print("=" * 72)
        print("DUMPS POSSIVELMENTE DEFASADOS — %d exportado(s) %d h ou mais antes" % (len(velhos), horas))
        print("do mais novo da pasta (%s). Dump sem irmao em `_antes-*` nao" % novo[:19])
        print("e pego pela guarda acima, e pode estar velho igual. Nao prova")
        print("defasagem: workflow que ninguem toca ha dias aparece aqui, e e correto.")
        for arq, (u, h) in sorted(velhos.items(), key=lambda kv: -kv[1][1])[:limite]:
            print("   %-34s %s  (%.0f h atras)" % (arq, u[:19], h))
        if len(velhos) > limite:
            print("   ... e mais %d" % (len(velhos) - limite))
        print("Achado que envolva estes e CANDIDATO, nunca item.")
        print("=" * 72 + "\n")
    return falou
