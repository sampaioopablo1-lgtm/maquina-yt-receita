"""A2 — `Lembretes da Reunião`: confirmação + 3 lembretes pelo WhatsApp (Stevo).

POR QUÊ. O `Pós-agendamento v2` tem as esperas de 24h/3h/30min antes da
reunião, mas manda 0 mensagem ao lead (medido ao vivo, 23/09/2026): os PA-*
da biblioteca nunca foram ligados. Lembrete é a alavanca mais barata de
comparecimento. Workflow à parte, sem mexer no Pós-agendamento (180 nós).

GATILHO: o mesmo do Pós-agendamento v2 (reunião confirmada no calendário
`3uNQFjCEDe7b4gKZJuOZ`), copiado ao vivo daquele workflow.

TEXTOS (PA-CONF/R24/R3H/R30 da biblioteca, versão v2 de 23/09):
  - sem {{user.first_name}}: em mensagem automática sai vazio (APRENDIZADOS);
  - sem primeiro nome do lead (A8: a Porta grava o nome do WhatsApp como vier);
  - sem "amanhã"/"hoje": se a reunião foi marcada em cima da hora, a espera
    é pulada e o lembrete sai na hora — a data explícita nunca fica errada;
  - sem a promessa de "link 30 min antes" (nenhum workflow a cumpre).

TRAVAS: PA-CONF só sem `nao-perturbe`; cada lembrete só se o contato ainda
tem `etapa-reuniao` e não tem `nao-perturbe` (lead que desmarcou e o SDR
moveu de etapa não recebe lembrete). Condição por TAG, não por etapa de
oportunidade: o gatilho não é de oportunidade (REGRA do projeto).

Uso: python build_lembretes_reuniao.py [--so-montar] [--publicar]
"""
import copy, io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Lembretes da Reunião"
QUANDO = "{{appointment.only_start_date}} às {{appointment.only_start_time}}"
MSG = {
    "PA-CONF-v2": "Oi! Sua reunião de diagnóstico com a O Próximo Cliente está confirmada "
                  "para " + QUANDO + ". Se precisar remarcar, é só responder esta mensagem.",
    "PA-R24-v2": "Oi! Passando pra confirmar a nossa reunião de diagnóstico: " + QUANDO +
                 ". Segue valendo? Se precisar remarcar, responde por aqui.",
    "PA-R3H-v2": "Oi! Lembrete: nossa reunião de diagnóstico é " + QUANDO + ". Te espero!",
    "PA-R30-v2": "Oi! Nossa reunião de diagnóstico começa em 30 minutos, às "
                 "{{appointment.only_start_time}}.",
}


def sms(codigo):
    return {"id": g.uid(), "name": "WhatsApp · " + codigo, "type": "sms",
            "attributes": {"type": "sms", "body": MSG[codigo], "attachments": []}}


def espera(minutos, rotulo):
    d, r = divmod(minutos, 1440)
    h, m = divmod(r, 60)
    return {"id": g.uid(), "name": "Aguardar até " + rotulo + " antes da reunião",
            "type": "wait",
            "attributes": {"type": "appointment", "name": "Aguardar até " + rotulo,
                           "cat": "", "appointmentStartAfter": {
                               "when": "before", "type": "minutes", "value": minutos,
                               "distributed": {"months": 0, "days": d, "hours": h, "minutes": m}},
                           "appointmentCondition": "skip", "isHybridAction": True,
                           "hybridActionType": "wait", "convertToMultipath": False,
                           "transitions": []}}


def sem_npt():
    return g.cond("contact", "tags", "index-of-false", ["nao-perturbe"])


def ainda_marcada():
    return [g.cond("contact", "tags", "index-of-true", ["etapa-reuniao"]), sem_npt()]


def lembrete(minutos, rotulo, codigo, resto):
    return [espera(minutos, rotulo),
            g.Branch(codigo[:6] + " · Reunião ainda de pé?", ainda_marcada(),
                     [sms(codigo)] + resto, [])]


r30 = lembrete(30, "30 min", "PA-R30-v2", [])
r3h = lembrete(180, "3 h", "PA-R3H-v2", r30)
r24 = lembrete(1440, "24 h", "PA-R24-v2", r3h)
passos = [g.Branch("PA-CONF · Pode receber mensagem?", [sem_npt()],
                   [sms("PA-CONF-v2")] + r24, [])]

if "--so-montar" in sys.argv:
    nos = g.montar(copy.deepcopy(passos))
    print(len(nos), "nós")
    for n in nos:
        print("  ", n["type"], "|", n.get("name"))
    sys.exit(0)

c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
modelo = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId="
                               + ids["Pós-agendamento v2"]) if not t.get("deleted")][0]
gatilho = {k: copy.deepcopy(modelo[k]) for k in ("type", "conditions", "masterType")
           if k in modelo}
gatilho.update({"status": "draft", "schedule_config": {}, "name": "Reunião confirmada",
                "active": True, "triggersChanged": True, "location_id": g.LOC})
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.preencher(c, wf, NOME, passos, [gatilho], allow_reentry=True, stop_on_response=False)
g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                             "workflows-json", NOME + ".json"))
print("rascunho:", wf, NOME)
if "--publicar" in sys.argv:
    print("publicar:", g.publicar(c, wf))
