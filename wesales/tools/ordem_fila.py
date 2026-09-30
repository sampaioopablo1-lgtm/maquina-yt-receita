#!/usr/bin/env python3
"""Ordem da "Minha fila — SDR" (29/09, aprovado pelo dono).

QUEM entra na fila continua sendo decidido pela cadência 12x30 e pelo atuador das filas (tags).
Este arquivo só decide a ORDEM: escreve `Prioridade`, que a lista ordena de cima para baixo.
Roda no relógio a cada 30 min (seg–sex 07:30–21:00). Escreve só o que mudou.

    10  agendou sozinho pelo Calendly, ligação de confirmação pendente (tag confirmar-reuniao);
        faltou à reunião e tem toque de remarcação a fazer (fila-noshow, cadencia_noshow.py)
     9  pediu retorno e o horário já passou (retorno-vencido)
     8  lead novo: entrou há menos de 2 h e ninguém ligou ainda
     7  respondeu mensagem, ligou de volta (fila-quente), fechar horário ou nota >= 70
     5  toque da cadência vencido hoje (fila-tel / fila-wa)
     3  os demais em CONECTAR
     0  fora da fila: DND, nao-perturbe, pausado, telefone-invalido, status-perdido

`confirmar-reuniao` (posta pelo calendly_para_crm.py) sai quando a SDR conclui a tarefa
"[LIGAR AGORA] Agendou pelo Calendly", quando a reunião passa ou quando o lead deixa REUNIÃO.
Só mexe em quem está em CONECTAR ou tem `confirmar-reuniao`; o resto do funil não é tocado.

    python3 ordem_fila.py            # DRY
    python3 ordem_fila.py --aplicar
"""
from __future__ import annotations

import datetime as dt
import sys
from collections import Counter

from atuador_filas import CONECTAR, PRIORIDADE, TESTE, contatos, etapa_por_contato, pedir, valor

REUNIAO = "3d26fcd1"
TAG_CONF = "confirmar-reuniao"
FORA = {"nao-perturbe", "pausado", "telefone-invalido", "status-perdido", "grupo-whatsapp-nao-e-lead"}
CAMPO_TENTATIVA = "qHJGJKZBccASOKkKP8ge"
CAMPO_NOTA = "FHoXQnLYA8LW5mFzfdIq"
CAMPO_SINAL = "jfQgrZFnxhbn1qmCeFDC"


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def nota(c, etapa, agora):
    """Pura: (prioridade, motivo). None = não é da fila da SDR, não escrever."""
    tags = {str(t).lower() for t in c.get("tags") or []}
    if TAG_CONF in tags and etapa == REUNIAO:
        return (0, "DND") if c.get("dnd") else (10, "agendou pelo Calendly, confirmar")
    if "fila-noshow" in tags and etapa == REUNIAO:
        return (0, "DND") if c.get("dnd") else (10, "no-show: remarcar reunião")
    if etapa != CONECTAR:
        return None, ""
    if c.get("dnd"):
        return 0, "DND"
    if tags & FORA:
        return 0, "tag " + ",".join(sorted(tags & FORA))
    if "retorno-vencido" in tags:
        return 9, "retorno vencido"
    tent = num(valor(c, CAMPO_TENTATIVA)) or 0
    entrou = c.get("dateAdded")
    if entrou and tent == 0:
        h = (agora - dt.datetime.fromisoformat(entrou.replace("Z", "+00:00"))).total_seconds() / 3600
        if h < 2:
            return 8, "lead novo (%.1f h)" % h
    n = num(valor(c, CAMPO_NOTA))
    if valor(c, CAMPO_SINAL) == "Resposta de mensagem" or tags & {"fila-quente", "fechar-horario"} or (n is not None and n >= 70):
        return 7, "quente"
    if tags & {"fila-tel", "fila-wa"}:
        return 5, "toque vencido hoje"
    return 3, "demais"


ACAO = "oc7FTlIhIpiH90oZxPyx"   # Próxima ação (coluna da Minha fila, 30/09)


def acao(p, motivo, tags):
    """Pura: o que a SDR faz com o lead, em uma linha. None = quem escreve é outro robô (no-show 6x15)."""
    if motivo.startswith("no-show"):
        return None
    if p == 10:
        return "📞 Confirmar reunião"
    if p == 9:
        return "📞 Retorno vencido"
    if p == 8:
        return "📞 Lead novo: ligar já"
    if p == 7:
        return "🔥 Fechar horário"
    if p == 5:
        return "💬 Cadência: WhatsApp" if "fila-wa" in tags else "📞 Cadência: ligar"
    if p == 3:
        return "⏳ Aguardar"
    return "⛔ Fora (%s)" % motivo


def solta_confirmacao(cs, etapas, aplicar, agora):
    for c in cs:
        if TAG_CONF not in (c.get("tags") or []):
            continue
        motivo = None
        if etapas.get(c["id"]) != REUNIAO:
            motivo = "saiu de REUNIÃO"
        else:
            ts = pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or []
            if not any(t.get("title", "").startswith("[LIGAR AGORA] Agendou pelo Calendly") and not t.get("completed")
                       for t in ts):
                motivo = "SDR concluiu a ligação de confirmação"
            else:
                ap = pedir("GET", "/contacts/%s/appointments" % c["id"]).get("events") or []
                futuras = [e for e in ap if (e.get("appointmentStatus") or "") != "cancelled"
                           and dt.datetime.fromisoformat(e["startTime"].replace(" ", "T") + ("" if "+" in e["startTime"] or "-03" in e["startTime"] else "-03:00")) > agora]
                if not futuras:
                    motivo = "a reunião já passou"
        if motivo:
            print("  - %s  %s  (%s)%s" % (TAG_CONF, c.get("contactName") or c["id"], motivo, "" if aplicar else " DRY"))
            if aplicar:
                pedir("DELETE", "/contacts/%s/tags" % c["id"], {"tags": [TAG_CONF]})
            c["tags"] = [t for t in c.get("tags") or [] if t != TAG_CONF]


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(dt.timezone.utc)
    etapas = etapa_por_contato()
    cs = contatos()
    solta_confirmacao(cs, etapas, aplicar, agora)
    dist, mudou = Counter(), 0
    for c in cs:
        if TESTE.search(c.get("contactName") or ""):
            continue
        p, motivo = nota(c, etapas.get(c["id"]), agora)
        if p is None:
            continue
        dist[p] += 1
        texto = acao(p, motivo, {str(t).lower() for t in c.get("tags") or []})
        campos = []
        if num(valor(c, PRIORIDADE)) != p:
            campos.append({"id": PRIORIDADE, "field_value": p})
        if texto is not None and (valor(c, ACAO) or "") != texto:
            campos.append({"id": ACAO, "field_value": texto})
        if not campos:
            continue
        mudou += 1
        print("  %-28s %s -> %d  (%s) | %s" % ((c.get("contactName") or "?")[:28], valor(c, PRIORIDADE), p, motivo, texto))
        if aplicar:
            pedir("PUT", "/contacts/%s" % c["id"], {"customFields": campos})
    print("ordem da fila: %s | %d mudança(s)%s" % (dict(sorted(dist.items(), reverse=True)), mudou, "" if aplicar else " (DRY)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
