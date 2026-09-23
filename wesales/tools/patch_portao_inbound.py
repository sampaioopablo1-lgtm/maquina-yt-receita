#!/usr/bin/env python3
"""Porta os dois portoes de capacidade da `Cadência 12x30` para a `Cadência Inbound`.

O PROBLEMA (F-05 / pendencia 9e). O `GUIA-SDR.md` promete ao SDR, sem
ressalva: "se voce passar de 100 toques no dia ou tiver 50 ou mais tarefas
vencidas, o sistema segura os toques novos". Na `Cadência 12x30` isso e
verdade — cada um dos 6 toques passa por dois portoes antes de gerar tarefa.
Na `Cadência Inbound` **nao existe nenhum dos dois**: os 5 toques (TI1..TI5)
tem `Lead pausado?` e `Ainda vale ligar?`, mas nada que olhe capacidade. Lead
de anuncio fura a fila de um SDR lotado, e a promessa do guia e falsa para
ele. A `faxina_tarefas.py` (197-213) aplica `sdr-lotado` e a Inbound nunca le
a tag.

Medido nos dumps de 23/09/2026:

| portao                      | 12x30 p1 | 12x30 p2 | Inbound |
|-----------------------------|----------|----------|---------|
| `Teto de toques da semana?` |    6     |    6     |  **0**  |
| `SDR lotado?`               |    6     |    6     |  **0**  |

Sao 2 portoes x 5 toques = **10 portoes logicos**, e cada portao logico sao
**5 nos** (`if_else` + `Branch` + `None` + `wait` + `goto`): 50 nos novos, de
272 para 322. Por isso isto e script, e nao clique na tela.

COMO. Nao monta nada a mao: **clona** o grupo de 5 nos que ja existe e
funciona na `Cadência 12x30 — parte 2`, remapeando todo uuid que aparece
dentro do grupo (`id`, `next`, `parent`, `parentKey`, `branches[].id`,
`__segmentId`, `__conditionId`, `goto.targetNodeId`). Assim os atributos vao
byte a byte iguais ao que o GHL ja aceitou — nenhum `nestedDropdownTypes`
inventado, nenhum campo faltando.

ONDE. Em cada toque, entre o `None` (else) do `TI{n} · Lead pausado?` e o
`TI{n} · Ainda vale ligar?`, na mesma ordem do 12x30:

    Lead pausado?  ->  Teto de toques da semana?  ->  SDR lotado?  ->  Ainda vale ligar?

PARAMETROS, iguais aos do 12x30 — e esta e a unica escolha de desenho aqui,
que o dono confirma ou muda:
  - teto semanal: campo `c1xuCuLyJheHOQoJ3grH` >= 6, espera 1 dia e volta;
  - `sdr-lotado`: tag presente, espera 1 hora e volta.
O `Lead pausado?` da Inbound espera 30 min (a Inbound e mais apertada que a
12x30 de proposito); nao mexo nele. Os dois portoes novos esperam o tempo do
12x30 porque o que eles esperam e o mesmo: um contador de semana e uma
sobrecarga de dia.

NAO E APROVADO.md. Nenhuma tag nova, nenhum campo novo: `sdr-lotado` e
`c1xuCuLyJheHOQoJ3grH` ja existem e o 12x30 ja os le. Mas isto ALTERA um
workflow publicado que toca lead real — por isso `--aplicar` so deve rodar
depois do dono ver o plano, e a alteracao de workflow nao sai por MCP: e este
script, do PC.

Uso:  python patch_portao_inbound.py --dump     # confere pelos dumps, sem API
      python patch_portao_inbound.py            # le a conta, so imprime o plano
      python patch_portao_inbound.py --aplicar   # grava, com backup e conferencia

`--dump` roda em qualquer maquina, sem token e sem rede: le
`wesales/workflows-json/`, monta o resultado em memoria e passa pelas mesmas
conferencias. E como a insercao foi validada em 23/09/2026 antes de existir
qualquer aprovacao para escrever na conta.
"""
import copy
import json
import os
import re
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g        # put preserva configuracoes

DOADOR = "Cadência 12x30 — parte 2"
ALVO = "Cadência Inbound"
PORTOES = ["Teto de toques da semana?", "SDR lotado?"]
TOQUES = ["TI1", "TI2", "TI3", "TI4", "TI5"]
AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-portao-inbound")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def grupo(tpl, sufixo):
    """Os 5 nos do portao cujo nome termina em `sufixo`, na ordem do template.

    `if_else` nomeado + `Branch` + `None` + `wait` + `goto`. Devolve a lista e
    o id do no `None`, que e por onde a cadeia segue.
    """
    i = next((k for k, t in enumerate(tpl) if (t.get("name") or "").endswith(sufixo)), None)
    if i is None:
        raise SystemExit("nao achei o portao %r em %s" % (sufixo, DOADOR))
    g5 = tpl[i:i + 5]
    tipos = [t.get("type") for t in g5]
    if tipos != ["if_else", "if_else", "if_else", "wait", "goto"]:
        raise SystemExit("grupo de %r nao tem a forma esperada: %s" % (sufixo, tipos))
    nones = [t["id"] for t in g5 if (t.get("attributes") or {}).get("else")]
    if len(nones) != 1:
        raise SystemExit("grupo de %r nao tem exatamente um no `None`" % sufixo)
    return g5, nones[0]


def clona(g5, none_id, novo_nome, entra_de, x):
    """Copia o grupo com uuids novos. Devolve (nos, id do `None` novo)."""
    bruto = json.dumps(g5, ensure_ascii=False)
    mapa = {u: str(uuid.uuid4()) for u in sorted(set(UUID.findall(bruto)))}
    for velho, novo in mapa.items():
        bruto = bruto.replace(velho, novo)
    novos = json.loads(bruto)
    # o primeiro no do grupo passa a pendurar em quem o chama
    novos[0]["name"] = novo_nome
    novos[0]["parent"] = novos[0]["parentKey"] = entra_de
    for k, t in enumerate(novos):        # canvas legivel, nao funcional
        t.setdefault("advanceCanvasMeta", {})["position"] = {"x": x + 200 * k, "y": 0}
    return novos, mapa[none_id]


def encadeia(tpl, entra_id, novos, depois_id):
    """Acerta os ponteiros `next` (o GHL valida `next`, nao so `parentKey`).

    `entra_id` passa a apontar para a cabeca do primeiro portao; o `None` de
    cada portao aponta para a cabeca do seguinte, e o ultimo para `depois_id`.
    """
    por_id = {t["id"]: t for t in tpl}
    cabecas = [n for n in novos if n.get("type") == "if_else"
               and not (n.get("attributes") or {}).get("else")
               and isinstance(n.get("next"), list)]
    nones = [n for n in novos if (n.get("attributes") or {}).get("else")]
    por_id[entra_id]["next"] = cabecas[0]["id"]
    for k, n in enumerate(nones):
        n["next"] = cabecas[k + 1]["id"] if k + 1 < len(cabecas) else depois_id


def insere(tpl_alvo, tpl_doador):
    """Insere os dois portoes em cada toque. Devolve (novo template, log)."""
    tpl = copy.deepcopy(tpl_alvo)
    grupos = [grupo(tpl_doador, s) for s in PORTOES]
    log = []
    for toque in TOQUES:
        nome_pausado = "%s · Lead pausado?" % toque
        i = next((k for k, t in enumerate(tpl) if t.get("name") == nome_pausado), None)
        if i is None:
            log.append("%s: nao achei %r — PULADO" % (toque, nome_pausado))
            continue
        porta = tpl[i]
        # o `None` (else) do Lead pausado? e por onde a cadeia segue hoje
        else_id = next((t["id"] for t in tpl
                        if t.get("parentKey") == porta["id"]
                        and (t.get("attributes") or {}).get("else")), None)
        if not else_id:
            log.append("%s: %r sem no `None` — PULADO" % (toque, nome_pausado))
            continue
        seguintes = [t for t in tpl if t.get("parentKey") == else_id]
        if len(seguintes) != 1:
            log.append("%s: o `None` tem %d filhos, esperava 1 — PULADO"
                       % (toque, len(seguintes)))
            continue
        depois = seguintes[0]

        novos, entra = [], else_id
        base_x = (porta.get("advanceCanvasMeta") or {}).get("position", {}).get("x", 0)
        for j, (g5, none_id) in enumerate(grupos):
            bloco, entra = clona(g5, none_id, "%s · %s" % (toque, PORTOES[j]),
                                 entra, base_x + 1100 * (j + 1))
            novos += bloco
        # o que vinha depois do Lead pausado? passa a vir depois do ultimo portao
        depois["parent"] = depois["parentKey"] = entra
        encadeia(tpl, else_id, novos, depois["id"])
        # insere os 10 nos logo depois do grupo do Lead pausado?
        pos = max(k for k, t in enumerate(tpl)
                  if t["id"] in {porta["id"], else_id}
                  or t.get("parentKey") in {porta["id"], else_id}) + 1
        tpl[pos:pos] = novos
        log.append("%s: +%d nos (%s), %r religado ao ultimo portao"
                   % (toque, len(novos), " -> ".join(PORTOES), depois.get("name")))
    return tpl, log


def confere(tpl, antes):
    """Invariantes que tem de valer depois da insercao. Devolve lista de erros."""
    erros = []
    ids = [t["id"] for t in tpl]
    if len(ids) != len(set(ids)):
        erros.append("id repetido no template")
    conhecidos = set(ids)
    for t in tpl:
        p = t.get("parentKey")
        if p and p not in conhecidos:
            erros.append("%s (%r) pendura em pai inexistente %s"
                         % (t["id"][:8], t.get("name"), str(p)[:8]))
        nx = t.get("next")
        for n in (nx if isinstance(nx, list) else [nx] if nx else []):
            if n not in conhecidos:
                erros.append("%s (%r) next para no inexistente %s"
                             % (t["id"][:8], t.get("name"), str(n)[:8]))
        if t.get("type") == "goto":
            alvo = (t.get("attributes") or {}).get("targetNodeId")
            if alvo not in conhecidos:
                erros.append("goto %s aponta para no inexistente %s"
                             % (t["id"][:8], str(alvo)[:8]))
    for nome in PORTOES:
        n = sum(1 for t in tpl if (t.get("name") or "").endswith(nome))
        if n != len(TOQUES):
            erros.append("portao %r aparece %dx, esperava %d" % (nome, n, len(TOQUES)))
    esperado = len(antes) + 10 * len(TOQUES)
    if len(tpl) != esperado:
        erros.append("%d nos, esperava %d" % (len(tpl), esperado))
    return erros


def relatorio(ta, td, aplicavel):
    """Imprime plano + conferencia. Devolve (novo template, ok?)."""
    novo, log = insere(ta, td)
    for l in log:
        print("   " + l)
    erros = confere(novo, ta)
    print("\n%d -> %d nos" % (len(ta), len(novo)))
    if erros:
        print("CONFERENCIA FALHOU%s:" % (" — nao aplico" if aplicavel else ""))
        for e in erros:
            print("   " + e)
        return novo, False
    print("conferencia ok: ids unicos, nenhum pai orfao, todo goto aponta para no que")
    print("existe, os dois portoes aparecem %dx cada." % len(TOQUES))
    return novo, True


def do_dump():
    """Valida a insercao pelos dumps do repositorio — sem API, sem token."""
    def tpl(nome):
        caminho = os.path.join(DUMPS, nome + ".json")
        with open(caminho, encoding="utf-8") as fh:
            dado = json.load(fh)
        wf = dado.get("workflow") or dado
        return (wf.get("workflowData") or {}).get("templates") or [], wf.get("updatedAt")
    ta, ua = tpl(ALVO)
    td, ud = tpl(DOADOR)
    print("MODO --dump: nada e lido da conta e nada e gravado.")
    print("doador %s: %d nos (dump de %s)" % (DOADOR, len(td), (ud or "")[:19]))
    print("alvo   %s: %d nos (dump de %s)\n" % (ALVO, len(ta), (ua or "")[:19]))
    print("Dump e fotografia: se a conta mudou depois destes horarios, o plano aqui")
    print("descreve o estado do arquivo, nao o da conta. Rode sem `--dump` para o")
    print("plano contra a conta ao vivo.\n")
    _, ok = relatorio(ta, td, aplicavel=False)
    return 0 if ok else 1


def main():
    if "--dump" in sys.argv:
        return do_dump()
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    for nome in (DOADOR, ALVO):
        if nome not in ids:
            raise SystemExit("workflow %r nao existe nesta subconta" % nome)

    doador = c.request("GET", "/workflow/" + g.LOC + "/" + ids[DOADOR])
    alvo = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    td = (doador.get("workflowData") or {}).get("templates") or []
    ta = (alvo.get("workflowData") or {}).get("templates") or []
    print("doador %s: %d nos | alvo %s: %d nos [%s]\n"
          % (DOADOR, len(td), ALVO, len(ta), alvo.get("status")))

    novo, ok = relatorio(ta, td, aplicavel=True)
    if not ok:
        return 1

    if not aplicar:
        print("\n(nada foi gravado — rode com --aplicar depois de o dono aprovar)")
        return 0

    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    r = put(c, alvo, novo)
    if r is None or r.get("_error"):
        print("PUT RECUSADO:", r)
        return 1
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    trs = [t.get("active") for t in
           c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + ids[ALVO])
           if not t.get("deleted")]
    print("gravado: status=%s nos=%d gatilhos=%s" % (v.get("status"), len(vt), trs))
    for nome in PORTOES:
        print("   %r ao vivo: %dx" % (nome, sum(1 for t in vt
                                                if (t.get("name") or "").endswith(nome))))
    g.export(c, ids[ALVO], os.path.join(DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
