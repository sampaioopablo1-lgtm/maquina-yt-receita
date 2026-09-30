#!/usr/bin/env python3
"""Cadência de no-show 6x15 (30/09, decisão do dono): 6 toques em 15 dias depois da reunião perdida.

    toque  dia  canal
      1     0   📞 ligação (telefone)
      2     0   💬 WhatsApp: mensagem pronta "10 · Faltou na reunião" (a SDR clica e envia)
      3     2   🟢 ligação pelo WhatsApp (botão "Ligar via WhatsApp" na conversa)
      4     5   📞 ligação (telefone)
      5     9   🟢 ligação pelo WhatsApp
      6    14   📞 ligação (telefone), a última

Substitui o workflow "Recuperação de No-show" (NS1–NS3), que parava no envio automático do WhatsApp
(Ana e Robson, 30/09). Aqui a mensagem é enviada por uma pessoa: nada automático sai para o lead.

Quem entra: reunião marcada como No-show (agendas do closer e da SDR) nos últimos 16 dias, lead ainda
em REUNIÃO e sem nova reunião depois dela. Sai quando remarca, sai de REUNIÃO, vira DND/nao-perturbe,
ou quando os 6 toques terminam (tag `noshow-fim`, a passagem para a 12x30 parte 2 é o próximo passo).

Cada toque vira tarefa "[NS k/6] ..." (o finalizar_tarefas fecha quando a ação acontece). Enquanto há
tarefa vencendo hoje, o lead leva a tag `fila-noshow` (entra na Minha fila) e o campo "Próxima ação"
diz o que fazer. Roda no relógio.

    python3 cadencia_noshow.py            # DRY
    python3 cadencia_noshow.py --aplicar
"""
from __future__ import annotations

import datetime as dt
import sys
import time

from atuador_filas import LOC, contatos, etapa_por_contato, pedir, valor

BR = dt.timezone(dt.timedelta(hours=-3))
REUNIAO = "3d26fcd1"
AGENDAS = {"oOfR9ADPJM0WyVyHRgKE": "Reunião com closer", "3uNQFjCEDe7b4gKZJuOZ": "Agendamento pela SDR"}
INICIO = "i5V0ZaltEMU2sDrWCNjJ"          # No-show: início da recuperação (data)
ACAO = "oc7FTlIhIpiH90oZxPyx"            # Próxima ação (coluna da Minha fila)
SDR = "ML69c5kAJ93cliAGgBj6"             # Andreyna
TAG, FILA, FIM = "noshow-6x15", "fila-noshow", "noshow-fim"
FORA = {"nao-perturbe", "status-perdido", "telefone-invalido"}
TOQUES = [
    (1, 0, "📞", "Ligar (telefone)",
     "Ligue e remarque. Se remarcar, marque pela ficha: ícone de calendário, agenda \"Agendamento pela SDR\"."),
    (2, 0, "💬", "WhatsApp: enviar a mensagem pronta",
     "Clique no nome do lead para abrir a conversa, digite / e escolha \"10 · Faltou na reunião\". Depois, Enviar."),
    (3, 2, "🟢", "Ligar pelo WhatsApp",
     "Na conversa do lead, botão \"Ligar via WhatsApp\"."),
    (4, 5, "📞", "Ligar (telefone)", "Segunda ligação normal. Objetivo: remarcar."),
    (5, 9, "🟢", "Ligar pelo WhatsApp", "Na conversa do lead, botão \"Ligar via WhatsApp\"."),
    (6, 14, "📞", "Ligar (telefone), última tentativa",
     "Última tentativa da recuperação. Não remarcou: o lead segue para a 12x30."),
]


def titulo(k, emoji, acao, nome):
    return "[NS %d/6] %s %s — %s" % (k, emoji, acao, nome)


def data_local(s: str) -> dt.datetime:
    """A agenda devolve hora de São Paulo sem fuso ("2026-09-29 20:00:00") ou ISO com fuso."""
    s = s.replace(" ", "T")
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=BR)


def eventos(agora) -> dict:
    por = {}
    ini, fim = int((agora - dt.timedelta(days=20)).timestamp() * 1000), int((agora + dt.timedelta(days=90)).timestamp() * 1000)
    for cal in AGENDAS:
        for e in pedir("GET", "/calendars/events?locationId=%s&calendarId=%s&startTime=%d&endTime=%d"
                       % (LOC, cal, ini, fim)).get("events") or []:
            if e.get("contactId"):
                por.setdefault(e["contactId"], []).append(e)
    return por


def situacao(evs, agora):
    """Pura: (reunião perdida, motivo de saída ou None)."""
    ns = [e for e in evs if (e.get("appointmentStatus") or "") == "noshow"
          and agora - data_local(e["startTime"]) <= dt.timedelta(days=16)]
    if not ns:
        return None, "sem no-show recente"
    ultimo = max(ns, key=lambda e: data_local(e["startTime"]))
    depois = [e for e in evs if (e.get("appointmentStatus") or "") not in ("cancelled", "noshow", "invalid")
              and data_local(e["startTime"]) > data_local(ultimo["startTime"])]
    return ultimo, ("remarcou para %s" % depois[0]["startTime"][:16]) if depois else None


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(dt.timezone.utc)
    hoje = agora.astimezone(BR).date()
    etapas, por_ev = etapa_por_contato(), eventos(agora)
    for c in contatos():
        tags = set(c.get("tags") or [])
        evs = por_ev.get(c["id"], [])
        perdida, saida = situacao(evs, agora)
        ativo = TAG in tags
        if not perdida and not ativo:
            continue
        nome = (c.get("contactName") or c.get("firstName") or "?").strip()
        if not saida and etapas.get(c["id"]) != REUNIAO:
            saida = "saiu de REUNIÃO"
        if not saida and (c.get("dnd") or tags & FORA):
            saida = "DND/nao-perturbe"
        if saida or not perdida:
            if ativo:
                print("  sai   %-26s %s" % (nome[:26], saida or "sem no-show recente"))
                if aplicar:
                    pedir("DELETE", "/contacts/%s/tags" % c["id"], {"tags": [TAG, FILA]})
                    pedir("PUT", "/contacts/%s" % c["id"], {"customFields": [{"id": ACAO, "field_value": ""}]})
                    for t in pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or []:
                        if t.get("title", "").startswith("[NS ") and not t.get("completed"):
                            pedir("PUT", "/contacts/%s/tasks/%s/completed" % (c["id"], t["id"]), {"completed": True})
            continue
        if FIM in tags:
            continue
        inicio = valor(c, INICIO)
        base = dt.date.fromisoformat(str(inicio)[:10]) if inicio else hoje
        dia = (hoje - base).days
        tarefas = pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or []
        feitos = {t["title"].split("]")[0] + "]": t for t in tarefas if t.get("title", "").startswith("[NS ")}
        quando_perdida = data_local(perdida["startTime"]).strftime("%d/%m %H:%M")
        novos = []
        for k, off, emoji, acao, como in TOQUES:
            if off <= dia and "[NS %d/6]" % k not in feitos:
                vence = dt.datetime.combine(base + dt.timedelta(days=off), dt.time(18, 0), BR)
                novos.append((k, titulo(k, emoji, acao, nome),
                              "Faltou à reunião de %s. %s" % (quando_perdida, como), vence))
        # tarefa só nasce no dia do toque: aberta = toque a fazer (hoje ou atrasado)
        vencendo = sorted([t["title"] for t in feitos.values() if not t.get("completed")] + [n[1] for n in novos])
        proximo = next(((k, off, e, a) for k, off, e, a, _ in TOQUES if off > dia), None)
        terminou = dia >= 14 and not proximo and not vencendo
        if vencendo:
            k0 = int(vencendo[0][4])
            curto = {1: "ligar", 2: "WhatsApp", 3: "ligar WhatsApp", 4: "ligar", 5: "ligar WhatsApp", 6: "última ligação"}[k0]
            acao_txt = "%s No-show %d/6: %s" % (TOQUES[k0 - 1][2], k0, curto)
        elif terminou:
            acao_txt = "✅ No-show: 6 toques feitos"
        elif proximo:
            acao_txt = "⏳ No-show %d/6 em %s" % (proximo[0], (base + dt.timedelta(days=proximo[1])).strftime("%d/%m"))
        else:
            acao_txt = "No-show: aguardando conclusão das tarefas"
        print("  %-5s %-26s dia %2d | novas %s | %s" % ("ativo" if ativo else "entra", nome[:26], dia,
                                                         [n[0] for n in novos], acao_txt))
        if not aplicar:
            continue
        campos = [{"id": ACAO, "field_value": acao_txt}]
        if not inicio:
            campos.append({"id": INICIO, "field_value": base.isoformat()})
        pedir("PUT", "/contacts/%s" % c["id"], {"customFields": campos})
        for k, tt, corpo, vence in novos:
            pedir("POST", "/contacts/%s/tasks" % c["id"], {"title": tt, "body": corpo, "assignedTo": SDR,
                  "dueDate": vence.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"), "completed": False})
            time.sleep(0.2)
        quer = {FIM} if terminou else ({TAG, FILA} if vencendo else {TAG})
        if quer - tags:
            pedir("POST", "/contacts/%s/tags" % c["id"], {"tags": sorted(quer - tags)})
        if ({TAG, FILA, FIM} - quer) & tags:
            pedir("DELETE", "/contacts/%s/tags" % c["id"], {"tags": sorted(({TAG, FILA, FIM} - quer) & tags)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
