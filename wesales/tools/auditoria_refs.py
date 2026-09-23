#!/usr/bin/env python3
"""Auditoria de referencia cruzada entre workflows (somente leitura).

Responde a pergunta que pegou o bug do `Mestre de saida v2` em 22/09/2026:
algum workflow no ar aponta, num no `remove_from_workflow` /
`add_to_workflow`, para um workflow desligado ou a ser apagado?

Um no assim nao da erro: ele roda, tira o lead do workflow errado e o deixa
preso no certo, calado. Rode ANTES de apagar qualquer workflow.

Limite honesto: le os dumps de `wesales/workflows-json/`, que sao fotografia
do payload ANTES de publicar. Um id corrigido ao vivo pela API continua
antigo aqui ate alguem redumpar, e workflow sem dump neste repositorio e
invisivel para esta auditoria. Para a resposta autoritativa, varra pela API
interna, do PC.

Uso:  python3 wesales/tools/auditoria_refs.py
Sai com codigo 1 se achar referencia para arquivado.
"""
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def carrega():
    """id -> (nome, arquivado?) de todo workflow com dump neste repositorio.

    Um backup em `_arquivo/` pode ter o MESMO id do workflow vivo (e tem: o
    `Mestre de saida v2` e dois `ZZ TESTE`). Nesse caso o vivo manda — senao a
    auditoria acusaria como arquivado um workflow que esta no ar, que e
    exatamente o alarme falso que ela existe para nao dar.
    """
    mapa = {}
    duplicados = {}
    # vivo primeiro; `_arquivo` so acrescenta id que o vivo nao tem
    padroes = (os.path.join(DUMPS, "*.json"), os.path.join(DUMPS, "_arquivo", "*.json"))
    for padrao in padroes:
        for caminho in sorted(glob.glob(padrao)):
            try:
                with open(caminho, encoding="utf-8") as fh:
                    dado = json.load(fh)
            except (ValueError, OSError):
                continue
            wf = dado.get("workflow") or {}
            wid = wf.get("id") or wf.get("_id")
            if not wid:
                continue
            nome = os.path.basename(caminho)[:-5]
            arquivado = os.sep + "_arquivo" + os.sep in caminho
            if wid in mapa:
                duplicados.setdefault(wid, [mapa[wid][0]]).append(nome)
                continue
            mapa[wid] = (nome, arquivado)
    return mapa, duplicados


def main():
    mapa, duplicados = carrega()
    if duplicados:
        print("%d id(s) com backup de mesmo id — o vivo tem precedencia:" % len(duplicados))
        for wid, nomes in sorted(duplicados.items()):
            print("   %s  %s" % (wid[:13], " | ".join(nomes)))
        print()
    if not mapa:
        print("nenhum dump encontrado em %s" % DUMPS)
        return 0

    achados = []
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        wf = dado.get("workflow") or {}
        eu = wf.get("id")
        nome = os.path.basename(caminho)[:-5]
        for i, no in enumerate((wf.get("workflowData") or {}).get("templates") or []):
            tipo = str(no.get("type") or "")
            if "workflow" not in tipo:
                continue
            for ref in sorted(set(UUID.findall(json.dumps(no)))):
                if ref == eu or ref not in mapa:
                    continue
                alvo, arquivado = mapa[ref]
                achados.append((nome, i, tipo, alvo, arquivado))

    print("%d workflows com id conhecido, %d arquivados" % (
        len(mapa), sum(1 for _, arq in mapa.values() if arq)))
    print()
    ruins = [a for a in achados if a[4]]
    for nome, i, tipo, alvo, arquivado in achados:
        marca = "  <<< APONTA PARA ARQUIVADO" if arquivado else ""
        print("%-34s no %-4s %-22s -> %s%s" % (nome, i, tipo, alvo, marca))
    print()
    if ruins:
        print("%d referencia(s) para workflow arquivado — conferir na tela" % len(ruins))
        return 1
    print("nenhuma referencia para workflow arquivado (no que os dumps mostram)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `... | head` fecha o pipe. Sem esta guarda o script morre com traceback
        # e exit=1, que parece falha de auditoria — a confusao que ele evita.
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
