"""`Lembretes da Reunião v2` — do agendamento até a reunião, gerando valor.

PEDIDO DO DONO (23/09/2026, ao vivo): lembretes automáticos por WhatsApp e
e-mail em 3 dias, 1 dia, 3 horas e 10 min antes, já com o link; cada um curto,
objetivo e gerando valor — e conforme o que o SDR preencheu no formulário de
qualificação. Posicionamento: a O Próximo Cliente gera demanda E pode atender
esses leads e agendar a visita/reunião direto na agenda do vendedor do
cliente — muitas vezes o problema não é lead, é aproveitar o que já se investe.

TRILHAS (decididas uma vez, na confirmação, pelos campos do formulário):
  ATENDIMENTO  investe em anúncios = Sim  e  quem atende = Dono / Ninguém fixo
               -> o dinheiro já entra; o lead esfria antes do 1º contato.
  PROCESSO     investe = Sim  e  quem atende = SDR / Vendedor
               -> tem time; decide velocidade, tentativas e registro.
  DEMANDA      investe = Nunca / Já investiu e parou
               -> anúncio "que não funcionou" costuma ter perdido gente
                  depois do clique; demanda + atendimento juntos.
  GERAL        formulário sem esses campos -> mensagem neutra que vale p/ todos.

PONTOS (espera relativa à reunião, `appointmentCondition: skip`):
  confirmação (WA + e-mail) · D-3 (WA) · D-1 (WA + e-mail, com link) ·
  H-3 (WA, com a dor do lead quando o SDR preencheu) · M-10 (WA + e-mail, link)
Cada ponto passa por "Reunião ainda de pé?" (tag `etapa-reuniao` e sem
`nao-perturbe`) — condição por TAG: o gatilho não é de oportunidade.

TEXTOS: sem nome do lead nem {{user.*}} (saem vazios/errados em automação);
sem "amanhã"/"hoje" (se a espera for pulada a data explícita nunca mente);
sem número inventado. Link: {{appointment.meeting_location}} — depende de o
calendário ter Google Meet/Zoom como local (conferir no teste).

E-MAIL: a subconta não tem domínio de envio próprio (location.domain vazio);
sai pelo LC Email compartilhado. Configurar domínio antes de escalar.

Uso: python build_lembretes_reuniao_v2.py [--so-montar] [--publicar]
"""
import copy, io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Lembretes da Reunião v3"
MARCA = "lr-conf-agora"   # posta na confirmação; `Lembretes · limpa marca (2 h)` tira
F = {"investe": "x5JUx0YCWaZmH3Q85psI", "atende": "xjEcIFfdt2h29wBaKMQO",
     "dor": "qmIKSSDVYNLl5E8vnr3f"}
QUANDO = "{{appointment.only_start_date}} às {{appointment.only_start_time}}"
LINK = "{{appointment.meeting_location}}"
OPC = ("Além de gerar demanda, a O Próximo Cliente também pode atender esses "
       "leads por você e agendar a visita ou a reunião direto na agenda do seu vendedor.")

CONF = ("Reunião confirmada ✅ " + QUANDO + ".\nLink: " + LINK + "\n\n"
        "Na reunião a gente olha o caminho do seu cliente — do anúncio até a venda — "
        "e você sai com ajustes que dá pra aplicar na mesma semana. "
        "Se precisar remarcar, é só responder aqui.")
D3 = {
    "ATENDIMENTO": "Um ponto pra nossa conversa: lead de anúncio esfria rápido. Depois dos "
                   "primeiros minutos sem resposta, a chance de conversar cai muito. Na reunião "
                   "vamos ver quanto do que você já investe está se perdendo antes do primeiro contato.",
    "PROCESSO": "Um ponto pra nossa conversa: quando o lead chega no time, três coisas decidem a "
                "venda — a velocidade da primeira resposta, quantas tentativas são feitas e o que "
                "fica registrado. Vamos olhar essas três no seu processo.",
    "DEMANDA": "Um ponto pra nossa conversa: muito anúncio que \"não funcionou\" gerou contato, "
               "sim — o problema foi o que aconteceu depois do clique. Vamos ver onde o seu funil "
               "perde gente antes de você colocar mais dinheiro.",
    "GERAL": "Um ponto pra nossa conversa: na maioria das empresas, o problema não é falta de "
             "contato, é o que acontece com ele depois que chega. Vamos olhar isso no seu caso.",
}
D1 = ("Pra aproveitar bem a nossa reunião (" + QUANDO + "): pensa em dois números do último "
      "mês — quantos contatos chegaram e quantos viraram venda. Só com eles a gente já enxerga "
      "onde tem dinheiro parado.\nLink: " + LINK)
H3 = {
    "COM_DOR": "Daqui a pouco, às {{appointment.only_start_time}}. Você comentou que o maior "
               "desafio hoje é: \"{{contact.dor_principal}}\". É por aí que a gente começa.",
    "ATENDIMENTO": "Daqui a pouco, às {{appointment.only_start_time}}. " + OPC,
    "PROCESSO": "Daqui a pouco, às {{appointment.only_start_time}}. " + OPC,
    "DEMANDA": "Daqui a pouco, às {{appointment.only_start_time}}. A gente vai falar de gerar "
               "demanda qualificada — e de quem atende esse contato quando ele chega. " + OPC,
    "GERAL": "Daqui a pouco, às {{appointment.only_start_time}}. " + OPC,
}
M10 = "Começamos em 10 minutos. Link: " + LINK
REMET = {"from_name": "O Próximo Cliente", "from_email": "agencia.proximocliente@gmail.com"}


def sms(nome, corpo):
    return {"id": g.uid(), "name": "WhatsApp · " + nome, "type": "sms",
            "attributes": {"type": "sms", "body": corpo, "attachments": []}}


def email(nome, assunto, corpo):
    html = "".join('<p style="margin:0px 0px 12px 0px;">%s</p>' % p
                   for p in corpo.replace("\n", "\n\n").split("\n\n") if p.strip())
    return {"id": g.uid(), "name": "E-mail · " + nome, "type": "email",
            "attributes": dict(REMET, subject=assunto, html=html, attachments=[])}


def espera(minutos, rotulo):
    d, r = divmod(minutos, 1440)
    h, m = divmod(r, 60)
    return {"id": g.uid(), "name": "Aguardar até " + rotulo + " antes da reunião", "type": "wait",
            "attributes": {"type": "appointment", "name": "Aguardar até " + rotulo, "cat": "",
                           "appointmentStartAfter": {"when": "before", "type": "minutes",
                                                     "value": minutos, "distributed": {
                                                         "months": 0, "days": d, "hours": h,
                                                         "minutes": m}},
                           "appointmentCondition": "skip", "isHybridAction": True,
                           "hybridActionType": "wait", "convertToMultipath": False,
                           "transitions": []}}


def de_pe():
    return [g.cond("contact_detail", "tags", "index-of-true", ["etapa-reuniao"]),
            g.cond("contact_detail", "tags", "index-of-false", ["nao-perturbe"])]


def ponto(minutos, rotulo, trilha, envios, resto, longe=False):
    """espera -> 'ainda de pé?' -> envios -> resto.

    longe=True (D-3, D-1): além de "de pé", exige que a confirmação NÃO tenha
    saído há menos de 2 h (tag MARCA ausente). Reunião marcada em cima da hora
    pula a espera (skip) e cairia junto da confirmação — medido na simulação
    de 23/09: CONF + D-3 + D-1 no mesmo minuto. Se suprimido, segue o resto.
    """
    conds = de_pe() + ([g.cond("contact_detail", "tags", "index-of-false", [MARCA])] if longe else [])
    return [espera(minutos, rotulo),
            g.Branch("%s · %s · Reunião ainda de pé?" % (rotulo, trilha), conds,
                     envios + resto,
                     [g.goto_step(resto[0]["id"])] if (longe and resto) else [])]


def h3(trilha):
    return [g.Branch("H-3 · %s · SDR preencheu a dor?" % trilha,
                     [g.cond("contact_detail", F["dor"], "has_value", None)],
                     [sms("H-3 dor", H3["COM_DOR"])],
                     [sms("H-3 " + trilha, H3[trilha])])]


def trilha(t):
    m10 = ponto(10, "10 min", t, [sms("M-10", M10),
                                  email("M-10", "Começamos em 10 minutos", M10)], [])
    p3h = ponto(180, "3 h", t, [], h3(t))
    # h3 termina em Branch; o M-10 precisa vir depois dos dois ramos -> duplica
    p3h[1].sim[-1].sim += copy.deepcopy(m10)
    p3h[1].sim[-1].nao += copy.deepcopy(m10)
    p1d = ponto(1440, "1 dia", t, [sms("D-1", D1),
                                   email("D-1", "Nossa reunião: " + QUANDO, D1)], p3h, longe=True)
    p3d = ponto(4320, "3 dias", t, [sms("D-3 " + t, D3[t])], p1d, longe=True)
    return p3d


def novos_ids(passos):
    """copy.deepcopy + id novo em cada nó/Branch, reapontando os goto."""
    mapa = {}

    def troca(lista):
        out = []
        for p in lista:
            if isinstance(p, g.Branch):
                novo = g.uid(); mapa[p.id] = novo; p.id = novo
                p.sim, p.nao = troca(p.sim), troca(p.nao)
            else:
                novo = g.uid(); mapa[p["id"]] = novo; p["id"] = novo
            out.append(p)
        return out

    def reaponta(lista):
        for p in lista:
            if isinstance(p, g.Branch):
                reaponta(p.sim); reaponta(p.nao)
            elif p.get("type") == "goto":
                a = p["attributes"]; a["targetNodeId"] = mapa.get(a["targetNodeId"], a["targetNodeId"])

    out = troca(copy.deepcopy(passos))
    reaponta(out)
    return out


def cond_campo(campo, valores):
    return [g.cond("contact_detail", F[campo], "==", v) for v in valores]


escolha = g.Branch(
    "Trilha · Investe em anúncios?", cond_campo("investe", ["Sim"]),
    [g.Branch("Trilha · Quem atende tem time?", cond_campo("atende", ["SDR", "Vendedor"]),
              novos_ids(trilha("PROCESSO")), novos_ids(trilha("ATENDIMENTO")), operador="or")],
    [g.Branch("Trilha · Nunca investiu ou parou?",
              cond_campo("investe", ["Nunca", "Já investiu e parou"]),
              novos_ids(trilha("DEMANDA")), novos_ids(trilha("GERAL")), operador="or")])

passos = [g.Branch("Confirmação · Pode receber mensagem?",
                   [g.cond("contact_detail", "tags", "index-of-false", ["nao-perturbe"])],
                   [sms("Confirmação", CONF), g.tag_step([MARCA]),
                    email("Confirmação", "Reunião confirmada — " + QUANDO, CONF), escolha],
                   [])]

if __name__ == "__main__":
    if "--so-montar" in sys.argv:
        nos = g.montar(copy.deepcopy(passos))
        ids = [n["id"] for n in nos]
        print(len(nos), "nós | ids únicos:", len(ids) == len(set(ids)))
        for n in nos:
            if n["type"] in ("sms", "email") or (n["type"] == "if_else" and n["name"] not in ("Branch", "None")):
                print("  ", n["type"], "|", n["name"])
        sys.exit(0)
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    modelo = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId="
                                   + ids["Pós-agendamento v2"]) if not t.get("deleted")][0]
    gat = {k: copy.deepcopy(modelo[k]) for k in ("type", "conditions", "masterType") if k in modelo}
    gat.update({"status": "draft", "schedule_config": {}, "name": "Reunião confirmada",
                "active": True, "triggersChanged": True, "location_id": g.LOC})
    wf = ids.get(NOME) or g.create_workflow(c, NOME)
    g.preencher(c, wf, NOME, passos, [gat], allow_reentry=True, stop_on_response=False)
    g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                 "workflows-json", NOME + ".json"))
    print("rascunho:", wf, NOME)
    if "--publicar" in sys.argv:
        print("publicar:", g.publicar(c, wf))
