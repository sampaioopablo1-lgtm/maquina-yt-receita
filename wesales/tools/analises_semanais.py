#!/usr/bin/env python3
"""Análises semanais da operação SDR/Closer — pedido do dono em 28/09.

Lê a conta pela API pública (GHL_PIT) e responde:
  1. Tentativas até agendar: leads com "Data agendado" -> Tentativas telefone + Tentativas WhatsApp.
     A cadência para quando a reunião é marcada (Pós-agendamento remove dos fluxos paralelos),
     então o contador atual equivale ao número de tentativas até o agendamento.
  2. Tentativas até qualificar: leads com Budget e Decisor preenchidos (a ficha BANT), mesma
     contagem. No fluxo novo qualificar e agendar são o mesmo envio.
  3. Velocidade de resposta: da entrada do lead até a 1ª ligação do discador (TYPE_CALL), em
     faixas, e a taxa de agendamento em cada faixa.
  4. Conexão por tentativa, horário e canal: nas ligações do discador, "conectou" = chamada
     completada com 20 s ou mais; por nº da tentativa e por hora do dia; e, pelos contadores,
     conexão por telefone × WhatsApp. (Ligação por WhatsApp no app da SDR não aparece na
     conversa — só nos contadores.)
  5. Resultado por origem: por formulário/campanha do Meta -> leads, qualificados, agendados,
     compareceram, ganhos.

    python analises_semanais.py            # imprime
    python analises_semanais.py --nota     # imprime e grava a nota fixa no painel "Decisão"
"""
from __future__ import annotations

import collections
import datetime as dt
import statistics
import sys

from campos_bant import ghl, LOC

F = {"tel": "wCzdqF7uLQwtrZ1JyZRn", "wa": "5j9SerJeZ6ngfZCPb2Wg", "con_tel": "LB11ao0AdSI1QSHyZBOP",
     "con_wa": "Og1CkI9x9OztsV242nIM", "agendado": "aY5cwLe9y13CEyv8ecwv", "compareceu": "EsisfhEZWFLcnEYEzx3k",
     "budget": "SZVgh0Y5HRcWWZG4fO9V", "decisor": "3dphGCPCoFcYXEQC2jeB"}
PAINEL = "6ab9b477ea8a8a09aee49d8b"
BRT = dt.timezone(dt.timedelta(hours=-3))
TESTE = ("teste", "zz ", "sem nome")


def contatos():
    out, depois = [], None
    while True:
        corpo = {"locationId": LOC, "pageLimit": 100}
        if depois:
            corpo["searchAfter"] = depois
        st, r = ghl("POST", "/contacts/search", corpo)
        lote = r.get("contacts") or []
        out += lote
        if len(lote) < 100 or not lote[-1].get("searchAfter"):
            return out
        depois = lote[-1]["searchAfter"]


def ligacoes(cid):
    st, r = ghl("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, cid))
    out = []
    for cv in r.get("conversations", []):
        st, m = ghl("GET", "/conversations/%s/messages?limit=100" % cv["id"])
        for x in (m.get("messages", {}).get("messages") or []):
            if x.get("messageType") == "TYPE_CALL" and x.get("direction") == "outbound":
                call = (x.get("meta") or {}).get("call") or {}
                out.append((dt.datetime.fromisoformat(x["dateAdded"].replace("Z", "+00:00")),
                            call.get("status") == "completed" and (call.get("duration") or 0) >= 20))
    return sorted(out)


def ganhos():
    st, r = ghl("GET", "/opportunities/search?location_id=%s&status=won&limit=100" % LOC)
    return {o.get("contactId") or o.get("contact", {}).get("id") for o in r.get("opportunities", [])}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def resumo(vals):
    if not vals:
        return "sem dados ainda"
    return "média %.1f · mediana %.1f · n=%d" % (statistics.mean(vals), statistics.median(vals), len(vals))


def origem(c):
    a = c.get("attributionSource") or {}
    return (a.get("formName") or a.get("campaign") or a.get("utmCampaign") or a.get("medium")
            or c.get("source") or "sem origem")[:40]


def main():
    cs = [c for c in contatos() if not any(t in (c.get("contactName") or c.get("firstName") or "").lower()
                                           for t in TESTE)]
    won = ganhos()
    linhas = []
    ate_agendar, ate_qualif = [], []
    por_origem = collections.defaultdict(lambda: collections.Counter())
    faixas = collections.defaultdict(lambda: [0, 0])
    tent_ord = collections.defaultdict(lambda: [0, 0])
    por_hora = collections.defaultdict(lambda: [0, 0])
    tel_t = tel_c = wa_t = wa_c = 0
    for c in cs:
        v = {f["id"]: f.get("value") for f in c.get("customFields", [])}
        tent = num(v.get(F["tel"])) + num(v.get(F["wa"]))
        agendado = bool(v.get(F["agendado"]))
        qualif = bool(v.get(F["budget"])) and bool(v.get(F["decisor"]))
        if agendado and tent:
            ate_agendar.append(tent)
        if qualif and tent:
            ate_qualif.append(tent)
        tel_t += num(v.get(F["tel"])); wa_t += num(v.get(F["wa"]))
        tel_c += num(v.get(F["con_tel"])); wa_c += num(v.get(F["con_wa"]))
        o = por_origem[origem(c)]
        o["leads"] += 1; o["qualificados"] += qualif; o["agendados"] += agendado
        o["compareceram"] += bool(v.get(F["compareceu"])); o["ganhos"] += c["id"] in won
        if not num(v.get(F["tel"])):
            continue
        ls = ligacoes(c["id"])
        if not ls:
            continue
        entrada = dt.datetime.fromisoformat(c["dateAdded"].replace("Z", "+00:00"))
        minutos = (ls[0][0] - entrada).total_seconds() / 60
        faixa = "até 5 min" if minutos <= 5 else "até 1 h" if minutos <= 60 else "até 24 h" if minutos <= 1440 else "mais de 24 h"
        faixas[faixa][0] += 1; faixas[faixa][1] += agendado
        for i, (quando, conectou) in enumerate(ls, 1):
            tent_ord[min(i, 6)][0] += 1; tent_ord[min(i, 6)][1] += conectou
            h = quando.astimezone(BRT).hour
            por_hora[h][0] += 1; por_hora[h][1] += conectou

    pct = lambda a, b: "%d%%" % round(100 * a / b) if b else "—"
    hoje = dt.datetime.now(BRT).strftime("%d/%m/%Y %H:%M")
    linhas.append("ANÁLISES DA OPERAÇÃO — atualizado em %s (%d leads, sem contatos de teste)" % (hoje, len(cs)))
    linhas.append("")
    linhas.append("1. Tentativas até AGENDAR: " + resumo(ate_agendar))
    linhas.append("2. Tentativas até QUALIFICAR (ficha BANT): " + resumo(ate_qualif))
    linhas.append("")
    linhas.append("3. Velocidade da 1ª ligação × agendamento:")
    for f in ("até 5 min", "até 1 h", "até 24 h", "mais de 24 h"):
        n, a = faixas[f]
        linhas.append("   %-13s %3d leads · agendaram %s" % (f, n, pct(a, n)))
    linhas.append("")
    linhas.append("4. Conexão (ligação completada ≥ 20 s):")
    linhas.append("   por tentativa: " + " · ".join("%s: %s (n=%d)" % ("6+" if k == 6 else "%dª" % k, pct(c2, n), n)
                                                  for k, (n, c2) in sorted(tent_ord.items())) if tent_ord else "   por tentativa: sem dados ainda")
    melhores = sorted(((pct(c2, n), h, n) for h, (n, c2) in por_hora.items() if n >= 3), reverse=True)[:3]
    linhas.append("   melhores horários: " + (", ".join("%dh (%s de %d)" % (h, p, n) for p, h, n in melhores) or "sem dados ainda"))
    linhas.append("   por canal: telefone %s (%d de %d) · WhatsApp %s (%d de %d)" % (
        pct(tel_c, tel_t), tel_c, tel_t, pct(wa_c, wa_t), wa_c, wa_t))
    linhas.append("")
    linhas.append("5. Resultado por origem (leads → qualificados → agendados → compareceram → ganhos):")
    for nome, o in sorted(por_origem.items(), key=lambda x: -x[1]["leads"])[:8]:
        linhas.append("   %-40s %3d → %d → %d → %d → %d" % (nome, o["leads"], o["qualificados"], o["agendados"],
                                                         o["compareceram"], o["ganhos"]))
    texto = "\n".join(linhas)
    print(texto)
    if "--nota" in sys.argv:
        import ghl_interno as g
        url = "/reporting/dashboards/%s/sticky-notes" % PAINEL
        notas = g.pedir("GET", url + "?locationId=" + LOC).get("data") or []
        doc = {"text": texto[:5000]}   # formato exigido pela API da nota (content.text, até 5.000)
        minha = [n for n in notas if "ANÁLISES DA OPERAÇÃO" in str(n.get("content", ""))]
        if minha:
            nid = minha[0].get("_id") or minha[0].get("id")
            g.pedir("PATCH", url + "/%s?locationId=%s" % (nid, LOC), {"content": doc})
            print("\n[nota atualizada no painel]")
        else:
            g.pedir("POST", url + "?locationId=" + LOC, {"content": doc})
            print("\n[nota criada no painel]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
