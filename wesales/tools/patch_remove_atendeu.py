#!/usr/bin/env python3
"""Ramo `Atendeu` do `Pós-ligação v2` sem a 2ª linha de defesa do `Não ligar` — G-18.

O PROBLEMA (G-13, pendência 2, achada em 23/09/2026 por auditoria de dump ao
vivo — ficou registrada dentro do item, nunca virou item de roadmap com
"Pronto quando" próprio, até esta rodada, G-18). Desde a D3 do
`PLANO-MULTICANAL.md`, `Atendeu` não move mais a oportunidade de etapa (fica
em `CONECTAR`, fase "fechar horário") — e por isso não aciona o
`Mestre de saída v2`, que só dispara por mudança de etapa/status.

**Isto NÃO é "o lead nunca sai da Cadência 12x30"** — conferido no dump da
própria `Cadência 12x30`: o nó 10 de cada uma das 12 tentativas já faz
`Remove from Workflow: este` quando `Resultado da tentativa` é `Atendeu`,
**enquanto o `Aguardar resultado` daquela tentativa específica ainda está
ativo** (até 18:30 do mesmo dia — 12 nós `remove_from_workflow` confirmados
no dump, um por tentativa). No caso comum (SDR liga e classifica no mesmo
dia, dentro da janela), o lead já sai sozinho.

O que falta é a **segunda linha de defesa**, independente de timing: o ramo
`Não ligar` do `Pós-ligação v2` tem um `remove_from_workflow` próprio (não
depende de nenhuma tentativa estar com o "Aguardar resultado" ainda aberto),
porque uma resposta de opt-out que chega tarde é cara demais para depender
só da janela da tentativa. O ramo `Atendeu` nunca ganhou o mesmo tratamento
— então se a classificação chega **fora** da janela ativa (por exemplo, o
SDR corrige de `Não atendeu` para `Atendeu` depois, com a cadência já no
`Wait` de dias entre tentativas, não no `Aguardar resultado`), não há mais
ninguém para tirar o lead da régua — ele seguiria para a próxima tentativa
automática ao mesmo tempo que o `Fechar Horário` tenta agendar a reunião —
a mesma classe de duplicidade que o F-04 (teto de toques) e o G-15 (dedupe
cross-canal) já trataram para outros casos; aqui, sem essa segunda rede.

Medido no dump publicado (`wesales/workflows-json/Pós-ligação v2.json`,
version 7), não deduzido do texto: o switch por `Resultado da tentativa`
existe em DUAS cópias (uma para cada lado do nó 2, o canal-check por tag
`fila-wa` que existia de quando a régua ainda ligava por WhatsApp — d52e61d
tirou o WhatsApp, mas as duas cópias continuam no ar). Só a cópia alcançada
quando `fila-wa` está AUSENTE é a que roda de verdade hoje (100% da operação
é telefone). Dentro de cada cópia, o ramo `Atendeu` tem um segundo If/Else
por canal (nó 1 da tabela em `build-wesales.md`, seção 4) — os quatro
caminhos finais (WA/telefone × cópia 1/cópia 2) terminam sempre num nó sem
`next`, e NENHUM tem `remove_from_workflow`:

    caminho                                  | nó terminal | remove_from_workflow?
    cópia 1 (fila-wa presente), ramo WA      | 627573c8…   | não
    cópia 1 (fila-wa presente), ramo telefone| a39fe8fc…   | não (e também é beco sem saída — ver nota)
    cópia 2 (fila-wa ausente), ramo WA       | ca6a4dba…   | não
    cópia 2 (fila-wa ausente), ramo telefone | b5167da9…   | não — **este é o caminho real, 100% da operação hoje**

Nota à parte, que este patch NÃO resolve por não afetar lead real: o caminho
`a39fe8fc…` (cópia 1, telefone) é um beco sem saída de verdade — só
`Math: Conexões telefone +1`, sem tag, tarefa ou nota. Parecia achado grave
até confirmar que só é alcançado quando `fila-wa` está presente no nó 2 e de
novo dentro do próprio ramo `Atendeu` — ou seja, é código morto pelas mesmas
tags que já o levaram até ali (a régua atual nunca deixa `fila-wa` presente
nesse ponto). Registrado para quem revisar não redescobrir o susto; não é
item de roadmap por não afetar nenhum lead na régua 100%-telefone publicada.
Ainda assim este patch adiciona o `remove_from_workflow` também aqui (barato,
e protege se o WhatsApp voltar a ser usado um dia).

COMO. Mesma ação que o ramo `Não ligar` já usa e o dono já aprovou (mesma
lista de `workflow_id`, não "All Except Current Workflow" — essa opção
removeria o lead também do `Fechar Horário`, que acabou de ser inscrito pela
tag `fechar-horario` no mesmo ramo, alguns nós antes): um nó
`remove_from_workflow` novo ao final de cada um dos quatro caminhos, colado
depois do último nó (não antes) — para dar ao `Fechar Horário` a chance de
começar a própria inscrição (que a tag deste mesmo ramo acabou de disparar)
antes de este nó rodar. Mesma ressalva de janela de corrida que a seção
2.9.5 do `build-wesales.md` já registra para outro par de workflows — não
eliminada por este patch, só não piorada por ele.

NÃO É APROVADO.md. Nenhuma tag nova, nenhum campo novo — só um
`Remove from Workflow` a mais em quatro pontos de um workflow já publicado.
Mas isto ALTERA workflow publicado que toca lead real: `--aplicar` só depois
de o dono ver o plano, e só roda no PC dele (`ghl_api.py` usa bearer local e
um path do Windows do dono — não existe nesta sessão na nuvem).

Uso:  python patch_remove_atendeu.py --dump      # confere pelos dumps, sem API
      python patch_remove_atendeu.py             # lê a conta, só imprime o plano
      python patch_remove_atendeu.py --aplicar    # grava, com backup e conferência

`--dump` roda em qualquer máquina, sem token e sem rede: lê
`wesales/workflows-json/Pós-ligação v2.json`, monta o resultado em memória e
passa pelas mesmas conferências. Foi assim que este patch foi validado nesta
rodada, antes de existir qualquer aprovação para escrever na conta — mesmo
método do `patch_portao_inbound.py` (G-17).
"""
import copy
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g

ALVO = "Pós-ligação v2"

# Mesma lista que o ramo `Não ligar` já usa nos dois nós irmãos (bc47a7a3…,
# 8c31b36e…) — reaproveitada de propósito, não escolhida de novo aqui.
WORKFLOW_IDS = [
    "c64a808b-3040-431e-8015-642a265e1022",  # Cadência 12x30
    "319ae603-2e33-4ea9-a8b7-fe63a914a40e",  # sem workflow vivo nos dumps atuais — inofensivo, mesma lista do ramo `Não ligar`
    "17e6dc19-3eca-42e8-83ff-e25a9d5c28e8",  # Cadência 12x30 — parte 2
]

# Os 4 nós terminais (sem `next`) do ramo `Atendeu`, medidos no dump de
# 23/09/2026 (version 7): duas cópias do switch por `Resultado da tentativa`
# (nó 2, canal-check por `fila-wa`) × dois canais dentro do próprio ramo
# `Atendeu` (nó 1 da tabela em build-wesales.md §4). Ver docstring.
TERMINAIS = [
    ("627573c8-908c-4f3c-a274-6530f05f45b7", "add_notes", "cópia 1, WA (inativa hoje)"),
    ("a39fe8fc-88d8-4f49-bd32-15dede515f2c", "math_operation", "cópia 1, telefone — código morto, ver nota"),
    ("ca6a4dba-37db-41fa-973c-4c0caebc98b9", "add_notes", "cópia 2, WA (inativa hoje)"),
    ("b5167da9-7748-4cc7-948d-22be94620c00", "add_notes", "cópia 2, telefone — CAMINHO REAL"),
]

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-patch-remove-atendeu")


def insere(tpl):
    """Acrescenta o `remove_from_workflow` depois de cada terminal. Devolve (novo template, log)."""
    tpl = copy.deepcopy(tpl)
    by_id = {t["id"]: t for t in tpl}
    log = []
    for tid, tipo_esperado, descricao in TERMINAIS:
        t = by_id.get(tid)
        if t is None:
            log.append("%s (%s): NÃO ACHEI NO DUMP ATUAL — PULADO (a tela mudou desde 23/09?)" % (tid[:8], descricao))
            continue
        if t.get("type") != tipo_esperado:
            log.append("%s (%s): tipo mudou para %r, esperava %r — PULADO"
                        % (tid[:8], descricao, t.get("type"), tipo_esperado))
            continue
        if "next" in t and t["next"]:
            log.append("%s (%s): já tem `next` (%s) — não é mais terminal, PULADO"
                        % (tid[:8], descricao, str(t["next"])[:8]))
            continue
        novo = {
            "id": str(uuid.uuid4()),
            "parent": t["id"],
            "parentKey": t["id"],
            "order": t.get("order", 0) + 1,
            "name": "Remove from Workflow",
            "type": "remove_from_workflow",
            "attributes": {"type": "remove_from_workflow", "workflow_id": list(WORKFLOW_IDS)},
        }
        t["next"] = novo["id"]
        tpl.insert(tpl.index(t) + 1, novo)
        by_id[novo["id"]] = novo
        log.append("%s (%s): +1 nó (remove_from_workflow -> %s)"
                    % (tid[:8], descricao, novo["id"][:8]))
    return tpl, log


def confere(tpl, antes):
    """Invariantes que têm de valer depois da inserção."""
    erros = []
    ids = [t["id"] for t in tpl]
    if len(ids) != len(set(ids)):
        erros.append("id repetido no template")
    conhecidos = set(ids)
    for t in tpl:
        p = t.get("parentKey")
        if p and p not in conhecidos:
            erros.append("%s (%r) pendura em pai inexistente %s" % (t["id"][:8], t.get("name"), str(p)[:8]))
    ids_antes = {t["id"] for t in antes}
    n_novos = sum(1 for t in tpl if t["id"] not in ids_antes and t.get("type") == "remove_from_workflow"
                  and t.get("attributes", {}).get("workflow_id") == WORKFLOW_IDS)
    if n_novos < 1:
        erros.append("nenhum remove_from_workflow novo foi inserido")
    esperado_max = len(antes) + len(TERMINAIS)
    if len(tpl) > esperado_max:
        erros.append("%d nós, esperava no máximo %d" % (len(tpl), esperado_max))
    return erros, n_novos


def relatorio(tpl):
    novo, log = insere(tpl)
    for l in log:
        print("   " + l)
    erros, n_novos = confere(novo, tpl)
    print("\n%d -> %d nós (%d remove_from_workflow novo(s))" % (len(tpl), len(novo), n_novos))
    if erros:
        print("CONFERÊNCIA FALHOU:")
        for e in erros:
            print("   " + e)
        return novo, False
    print("conferência ok: ids únicos, nenhum pai órfão, %d nó(s) novo(s) com o alvo certo." % n_novos)
    return novo, True


def do_dump():
    """Valida a inserção pelo dump do repositório — sem API, sem token."""
    caminho = os.path.join(DUMPS, ALVO + ".json")
    with open(caminho, encoding="utf-8") as fh:
        dado = json.load(fh)
    wf = dado.get("workflow") or dado
    tpl = (wf.get("workflowData") or {}).get("templates") or []
    print("MODO --dump: nada é lido da conta e nada é gravado.")
    print("%s: %d nós (dump de %s, status=%s)\n" % (ALVO, len(tpl), (wf.get("updatedAt") or "")[:19], wf.get("status")))
    print("Dump é fotografia: se a conta mudou depois deste horário, o plano aqui")
    print("descreve o estado do arquivo, não o da conta. Rode sem `--dump` para o")
    print("plano contra a conta ao vivo.\n")
    _, ok = relatorio(tpl)
    return 0 if ok else 1


def main():
    if "--dump" in sys.argv:
        return do_dump()
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    if ALVO not in ids:
        raise SystemExit("workflow %r não existe nesta subconta" % ALVO)
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    tpl = (cur.get("workflowData") or {}).get("templates") or []
    print("%s: %d nós [%s]\n" % (ALVO, len(tpl), cur.get("status")))

    novo, ok = relatorio(tpl)
    if not ok:
        return 1

    if not aplicar:
        print("\n(nada foi gravado — rode com --aplicar depois de o dono aprovar)")
        return 0

    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    put(c, cur, novo)
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    n_vivo = sum(1 for t in vt if t.get("type") == "remove_from_workflow"
                 and t.get("attributes", {}).get("workflow_id") == WORKFLOW_IDS)
    print("gravado: status=%s nós=%d remove_from_workflow(novos)=%d" % (v.get("status"), len(vt), n_vivo))
    g.export(c, ids[ALVO], os.path.join(DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
