#!/usr/bin/env python3
"""Grava `Canal que conectou` onde o ramo JA SABE o canal (9c, decidido).

DECISAO DO DONO, 23/09/2026: "automatico onde o ramo ja sabe, manual no resto"
(`ESTADO-E-PLANO.md`, linha 9c). Este patch faz a parte automatica nos dois
ramos em que o canal e MENSAGEM e nao ha ambiguidade nenhuma — o contato
respondeu uma mensagem, logo foi a mensagem que conectou.

O campo: `Canal que conectou`, id `TxJmoWdkA8rTqC1uEsMW`, `SINGLE_OPTIONS` com
`Ligação WhatsApp` / `Ligação normal` / `Mensagem` (criado pelo dono em 23/09
01:06, `campos-e-tags.md`). Hoje **nenhum workflow escreve nele** — e por isso
ele aparece na `auditoria_campos.py` como "nem escrito nem lido".

ONDE, e por que so aqui:

| workflow                               | ramo                    | grava      |
|----------------------------------------|-------------------------|------------|
| `Interceptação de Sinal — Resposta v2` | sinal quente (no 11)    | `Mensagem` |
| `Triagem da Nutrição`                  | `Quer conversar?` ("1") | `Mensagem` |

O que fica FORA, de proposito:

- **`Opt-out por Palavra-chave`** tambem tem gatilho `customer_reply`, mas
  "pare de me mandar mensagem" nao e conexao comercial. Contar isso encheria a
  metrica que o campo existe para responder (*qual canal conecta?*).
- **`Triagem`, ramos "2 agora nao" e "3 sem interesse"**: sao respostas, nao
  conexoes que levam a conversa. O "3" ja liga o DND. Somar os tres inflaria a
  conta pelo mesmo motivo do opt-out.
- **`Pós-ligação v2`**: o ramo SABE o canal (ele testa `fila-wa` logo depois do
  `Resultado da tentativa` — presente = ligacao por WhatsApp, ausente = normal),
  e portanto entra na parte automatica. Mas **fica para depois de proposito**:
  a sessao paralela tem o `patch_remove_atendeu.py` ainda sem `--aplicar`
  inserindo nos NOS MESMOS ramos `Atendeu`. Dois patches montados a partir de
  leituras diferentes se atropelam — um sobrescreve o outro. Ordem: aplicar o
  `patch_remove_atendeu.py` primeiro, re-exportar o dump, depois estender este.

COMO, e por que quase nao cria no: 30 nos deste projeto ja gravam VARIOS campos
num unico `update_contact_field` (`Cadência 12x30 — parte 2` grava 3 de uma
vez), logo a forma e aceita pelo GHL. Onde o ramo ja tem um
`update_contact_field`, este patch so **acrescenta o campo ao array `fields`**
que existe: zero no novo, zero religacao de cadeia, zero risco de quebrar o
fluxo. So cria no onde o ramo nao tem nenhum — hoje, um caso.

Uso:  python patch_canal_conectou.py --dump     # confere pelos dumps, sem API
      python patch_canal_conectou.py            # le a conta, so imprime o plano
      python patch_canal_conectou.py --aplicar   # grava, com backup e conferencia

E IDEMPOTENTE: se o campo ja estiver gravado no ramo, nao duplica e nao conta
como troca. Rodar duas vezes nao faz nada na segunda.
"""
import copy
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g        # put preserva configuracoes

CAMPO = "TxJmoWdkA8rTqC1uEsMW"
TITULO = "Canal que conectou"
AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-canal-conectou")

# workflow -> (rotulo do ramo, valor, como achar o no ancora)
# `ancora` devolve o indice do no DEPOIS do qual o campo tem de ficar gravado.
ALVOS = [
    ("Interceptação de Sinal — Resposta v2", "sinal quente", "Mensagem",
     lambda tpl: _acha_update(tpl, "jfQgrZFnxhbn1qmCeFDC")),
    ("Triagem da Nutrição", 'Quer conversar? ("1")', "Mensagem",
     lambda tpl: _acha_tag(tpl, "reengajado")),
]


def _acha_update(tpl, campo_id):
    """Indice do `update_contact_field` que grava `campo_id`."""
    for i, t in enumerate(tpl):
        if t.get("type") != "update_contact_field":
            continue
        for f in ((t.get("attributes") or {}).get("fields") or []):
            if f.get("field") == campo_id:
                return i
    return None


def _acha_tag(tpl, tag):
    """Indice do `add_contact_tag` que aplica `tag`."""
    for i, t in enumerate(tpl):
        if t.get("type") == "add_contact_tag" and tag in ((t.get("attributes") or {}).get("tags") or []):
            return i
    return None


def ja_grava(tpl):
    """O campo ja e gravado em algum no deste workflow?"""
    for t in tpl:
        if t.get("type") != "update_contact_field":
            continue
        for f in ((t.get("attributes") or {}).get("fields") or []):
            if f.get("field") == CAMPO:
                return True
    return False


def campo(valor):
    return {"field": CAMPO, "value": valor, "title": TITULO, "type": "select", "date": ""}


def aplica(tpl_original, valor, ancora):
    """Grava o campo. Devolve (novo tpl, descricao do que fez) ou (tpl, None)."""
    tpl = copy.deepcopy(tpl_original)
    if ja_grava(tpl):
        return tpl, None                      # idempotente
    i = ancora(tpl)
    if i is None:
        return tpl, "ANCORA NAO ENCONTRADA — nada feito"

    no = tpl[i]
    if no.get("type") == "update_contact_field":
        # caminho barato: acrescenta ao array que ja existe. Zero no novo.
        campos = (no.setdefault("attributes", {})).setdefault("fields", [])
        campos.append(campo(valor))
        return tpl, ("campo acrescentado ao `update_contact_field` %s (agora %d campos, 0 no novo)"
                     % (no["id"][:8], len(campos)))

    # o ramo nao tem `update_contact_field`: cria um logo depois da ancora,
    # copiando a forma de um no que o GHL ja aceitou.
    novo_id = str(uuid.uuid4())
    novo = {
        "id": novo_id,
        "parent": no["id"],
        "parentKey": no["id"],
        "order": 1,
        "name": "Update contact field",
        "type": "update_contact_field",
        "attributes": {"type": "update_contact_field",
                       "actionType": "update_field_data",
                       "fields": [campo(valor)]},
    }
    seguinte = no.get("next")
    if seguinte:
        novo["next"] = seguinte
        # quem vinha depois da ancora passa a pendurar no no novo
        for t in tpl:
            if t.get("id") == seguinte and t.get("parentKey") == no["id"]:
                t["parent"] = t["parentKey"] = novo_id
    no["next"] = novo_id
    tpl.insert(i + 1, novo)
    return tpl, ("no novo %s depois de %s (%s)"
                 % (novo_id[:8], no["id"][:8], no.get("type")))


def confere(tpl, antes, esperado_a_mais):
    erros = []
    ids = [t["id"] for t in tpl]
    if len(ids) != len(set(ids)):
        erros.append("id repetido")
    conhecidos = set(ids)
    for t in tpl:
        for chave in ("parentKey", "next"):
            v = t.get(chave)
            if isinstance(v, str) and v and v not in conhecidos:
                erros.append("%s (%s) aponta em `%s` para no inexistente %s"
                             % (t["id"][:8], t.get("type"), chave, v[:8]))
    n = sum(1 for t in tpl if t.get("type") == "update_contact_field"
            for f in ((t.get("attributes") or {}).get("fields") or [])
            if f.get("field") == CAMPO)
    if n != 1:
        erros.append("campo gravado %dx, esperava exatamente 1" % n)
    if len(tpl) != len(antes) + esperado_a_mais:
        erros.append("%d nos, esperava %d" % (len(tpl), len(antes) + esperado_a_mais))
    return erros


def roda(pega_tpl, aplicar=False, c=None, ids=None):
    """pega_tpl(nome) -> (templates, rotulo da origem). Devolve True se tudo ok."""
    ok_geral = True
    for nome, ramo, valor, ancora in ALVOS:
        tpl, origem = pega_tpl(nome)
        if tpl is None:
            print("== %s: NAO ENCONTRADO (%s)" % (nome, origem))
            ok_geral = False
            continue
        print("== %s  [%s]  %d nos" % (nome, origem, len(tpl)))
        print("   ramo: %s  ->  `%s` = %r" % (ramo, TITULO, valor))
        if ja_grava(tpl):
            print("   JA GRAVA o campo — nada a fazer (idempotente)")
            continue
        novo, o_que = aplica(tpl, valor, ancora)
        if o_que is None:
            print("   JA GRAVA o campo — nada a fazer")
            continue
        print("   " + o_que)
        erros = confere(novo, tpl, len(novo) - len(tpl))
        if erros:
            print("   CONFERENCIA FALHOU:")
            for e in erros:
                print("      " + e)
            ok_geral = False
            continue
        print("   conferencia ok: ids unicos, nenhum `next`/`parentKey` orfao,")
        print("   campo gravado exatamente 1x, %d -> %d nos" % (len(tpl), len(novo)))
        if aplicar:
            os.makedirs(BACKUP, exist_ok=True)
            wf = ids[nome]
            g.export(c, wf, os.path.join(BACKUP, nome + ".json"))
            cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
            put(c, cur, novo)
            v = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
            vt = (v.get("workflowData") or {}).get("templates") or []
            n = sum(1 for t in vt if t.get("type") == "update_contact_field"
                    for f in ((t.get("attributes") or {}).get("fields") or [])
                    if f.get("field") == CAMPO)
            print("   gravado: status=%s nos=%d campo ao vivo=%dx" % (v.get("status"), len(vt), n))
            g.export(c, wf, os.path.join(DUMPS, nome + ".json"))
    return ok_geral


def do_dump():
    print("MODO --dump: nada e lido da conta e nada e gravado.\n")

    def pega(nome):
        caminho = os.path.join(DUMPS, nome + ".json")
        if not os.path.exists(caminho):
            return None, "sem dump em workflows-json/"
        with open(caminho, encoding="utf-8") as fh:
            dado = json.load(fh)
        wf = dado.get("workflow") or dado
        return ((wf.get("workflowData") or {}).get("templates") or [],
                "dump de %s" % (wf.get("updatedAt") or "")[:19])

    ok = roda(pega)
    print("\nDump e fotografia. Rode sem `--dump` para o plano contra a conta ao vivo.")
    return 0 if ok else 1


def main():
    if "--dump" in sys.argv:
        return do_dump()
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}

    def pega(nome):
        if nome not in ids:
            return None, "nao existe nesta subconta"
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[nome])
        return ((cur.get("workflowData") or {}).get("templates") or [],
                cur.get("status") or "?")

    ok = roda(pega, aplicar, c, ids)
    if not aplicar:
        print("\n(nada foi gravado — rode com --aplicar)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
