"""Simula, SEM ENVIAR NADA, o `Lembretes da Reunião v2` publicado.

Lê o workflow ao vivo da conta, percorre o grafo nó a nó para um perfil de
lead (tags + campos do formulário), avalia as condições como o GHL avalia,
calcula o horário de cada espera relativa à reunião e imprime a linha do tempo
com as mensagens já renderizadas (variáveis trocadas pelos dados do perfil).

Premissa declarada (a única que só o teste real confirma): espera cujo
horário já passou no momento em que é alcançada segue na hora
(`appointmentCondition: skip`). A saída marca esses casos com [SKIP].

Uso: python simular_lembretes.py
"""
import io, json, os, re, sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

W = "7c5cbf03-ab17-4a3f-bb7a-d720607d2f51"
MESES = "jan fev mar abr mai jun jul ago set out nov dez".split()


def render(txt, p, reuniao):
    txt = re.sub(r"<[^>]+>", "\n", txt or "").strip()
    rep = {"appointment.only_start_date": reuniao.strftime("%d/%m/%Y"),
           "appointment.only_start_time": reuniao.strftime("%H:%M"),
           "appointment.meeting_location": p.get("link", "")}
    rep.update({"contact." + k: v for k, v in p["campos_chave"].items()})
    return re.sub(r"\{\{\s*([a-z_.]+)\s*\}\}", lambda m: str(rep.get(m.group(1), "{{%s}}" % m.group(1))), txt)


def avalia(cond, p, agora=None):
    sub, op, val = cond["conditionSubType"], cond["conditionOperator"], cond.get("conditionValue")
    if sub == "tags":
        vivas = set(p["tags"]) | {k for k, ate in p.get("tags_ate", {}).items() if agora < ate}
        tem = any(v in vivas for v in (val or []))
        return tem if op == "index-of-true" else not tem
    atual = p["campos"].get(sub)
    if op == "has_value":
        return bool(atual)
    if op == "==":
        return atual == val
    if op == "!=":
        return atual != val
    raise ValueError(op)


def simula(tpl, p, marcada, reuniao):
    by = {t["id"]: t for t in tpl}
    raiz = [t for t in tpl if not t.get("parentKey")][0]
    agora, no, linha = marcada, raiz, []
    while no:
        a = no.get("attributes") or {}
        prox = no.get("next")
        if no["type"] == "if_else" and not a.get("else") and a.get("branches"):
            b = a["branches"][0]
            op = b["segments"][0]["operator"]
            res = [avalia(c, p, agora) for c in b["segments"][0]["conditions"]]
            ok = all(res) if op == "and" else any(res)
            linha.append((agora, "   ? %s -> %s" % (no["name"], "SIM" if ok else "NÃO")))
            alvo = prox[0] if ok else prox[1]
            no = by.get(by[alvo].get("next")) if by[alvo].get("next") else None
            continue
        if no["type"] == "wait" and a.get("type") == "appointment":
            quando = reuniao - timedelta(minutes=a["appointmentStartAfter"]["value"])
            if quando > agora:
                agora = quando
                linha.append((agora, "   … " + no["name"]))
            else:
                linha.append((agora, "   … %s [SKIP: já passou, segue na hora]" % no["name"]))
        elif no["type"] == "add_contact_tag":
            for tg in a.get("tags") or []:
                p.setdefault("tags_ate", {})[tg] = agora + timedelta(hours=2)   # limpa marca (2 h)
            linha.append((agora, "   + tag %s (sai em 2 h)" % ",".join(a.get("tags") or [])))
        elif no["type"] == "goto":
            no = by.get(a.get("targetNodeId")); continue
        elif no["type"] == "sms":
            linha.append((agora, "WhatsApp  %s\n%s" % (no["name"], "\n".join(
                "           " + l for l in render(a.get("body"), p, reuniao).split("\n")))))
        elif no["type"] == "email":
            linha.append((agora, "E-mail    %s | assunto: %s" % (no["name"], render(a.get("subject"), p, reuniao))))
        no = by.get(prox) if isinstance(prox, str) else None
    return linha


PERFIS = [
    ("9940 · trilha ATENDIMENTO (investe Sim, Ninguém fixo, dor preenchida)",
     {"tags": ["etapa-reuniao"], "campos": {"x5JUx0YCWaZmH3Q85psI": "Sim", "xjEcIFfdt2h29wBaKMQO": "Ninguém fixo",
                                            "qmIKSSDVYNLl5E8vnr3f": "os leads chegam e ninguém responde rápido"},
      "campos_chave": {"dor_principal": "os leads chegam e ninguém responde rápido"}, "link": ""}),
    ("Lead · trilha PROCESSO (investe Sim, tem Vendedor, sem dor)",
     {"tags": ["etapa-reuniao"], "campos": {"x5JUx0YCWaZmH3Q85psI": "Sim", "xjEcIFfdt2h29wBaKMQO": "Vendedor"},
      "campos_chave": {}, "link": "https://meet.google.com/abc-defg-hij"}),
    ("Lead · trilha DEMANDA (já investiu e parou)",
     {"tags": ["etapa-reuniao"], "campos": {"x5JUx0YCWaZmH3Q85psI": "Já investiu e parou"},
      "campos_chave": {}, "link": "https://meet.google.com/abc-defg-hij"}),
    ("Lead · trilha GERAL (formulário em branco)",
     {"tags": ["etapa-reuniao"], "campos": {}, "campos_chave": {}, "link": "https://meet.google.com/abc-defg-hij"}),
    ("Lead que pediu para parar (nao-perturbe)",
     {"tags": ["etapa-reuniao", "nao-perturbe"], "campos": {}, "campos_chave": {}, "link": ""}),
]

if __name__ == "__main__":
    if "--v3" in sys.argv:
        import copy, importlib.util
        spec = importlib.util.spec_from_file_location(
            "b3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_lembretes_reuniao_v3.py"))
        b3 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(b3)
        tpl = g.montar(copy.deepcopy(b3.passos))
        print("v3 montada localmente (ainda não publicada): %d nós\n" % len(tpl))
    else:
        c = g.client()
        v = c.request("GET", "/workflow/" + g.LOC + "/" + W)
        tpl = v["workflowData"]["templates"]
        print("workflow ao vivo: %s [%s] %d nós\n" % (v["name"], v["status"], len(tpl)))
    cenarios = [("marcada 23/09 19:50 para 24/09 17:30 (22 h antes)", datetime(2026, 9, 23, 19, 50), datetime(2026, 9, 24, 17, 30)),
                ("marcada 23/09 19:50 para 28/09 17:30 (5 dias antes)", datetime(2026, 9, 23, 19, 50), datetime(2026, 9, 28, 17, 30))]
    for nome_c, marcada, reuniao in cenarios:
        for i, (nome, p) in enumerate(PERFIS):
            if i not in (0, 4) and nome_c.startswith("marcada 23/09 19:50 para 24"):
                continue      # cenário curto: 9940 e nao-perturbe
            p = json.loads(json.dumps(p))
            print("=" * 78)
            print(nome_c, "\n", nome)
            print("=" * 78)
            for t, l in simula(tpl, p, marcada, reuniao):
                print(t.strftime("%a %d/%m %H:%M"), l)
            print()
