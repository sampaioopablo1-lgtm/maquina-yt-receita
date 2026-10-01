#!/usr/bin/env python3
"""Ordem da "Minha fila — SDR" (29/09, aprovado pelo dono).

QUEM entra na fila continua sendo decidido pela cadência 12x30 e pelo atuador das filas (tags).
Este arquivo só decide a ORDEM: escreve `Prioridade`, que a lista ordena de cima para baixo.
Roda no relógio a cada 30 min (seg–sex 07:30–21:00). Escreve só o que mudou.

    10  lead novo (< 2 h) sem nenhuma ligação real; reunião a confirmar (tag confirmar-reuniao);
        faltou à reunião e tem toque de remarcação a fazer (fila-noshow, cadencia_noshow.py)
     9  pediu retorno e o horário já passou (retorno-vencido); lead de até 72 h que nunca recebeu ligação
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

from atuador_filas import CONECTAR, PRIORIDADE, TESTE, contatos, etapa_por_contato, pedir, ultima_ligacao_horas, valor

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
    # lead novo = nenhuma ligação REAL ainda (30/09: a Cadência Inbound grava "Tentativa nº 1" na entrada e
    # um "Não atendeu" automático aos 25 min, então o contador não serve para saber se alguém ligou)
    entrou = c.get("dateAdded")
    if entrou:
        h = (agora - dt.datetime.fromisoformat(entrou.replace("Z", "+00:00"))).total_seconds() / 3600
        if h < 72 and ultima_ligacao_horas(c["id"]) is None:
            return (10, "lead novo sem ligação (%.1f h)" % h) if h < 2 else (9, "sem nenhuma ligação (%.0f h)" % h)
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
    if motivo.startswith("lead novo"):
        return "📞 LEAD NOVO: ligar já"
    if motivo.startswith("sem nenhuma ligação"):
        return "📞 Nunca ligado: ligar"
    if p == 10:
        return "📞 Confirmar reunião"
    if p == 9:
        return "📞 Retorno vencido"
    if p == 8:
        return "📞 Lead novo: ligar já"
    if p == 7:
        if "fechar-horario" in tags:
            return "🔥 Fechar horário"
        if "fila-wa" in tags and "fila-tel" not in tags:
            return "💬 Quente: ligar pelo WhatsApp"
        return "🔥 Quente: ligar" if "fila-tel" in tags else "⏳ Aguardar o dia do toque"
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
            if not any(t.get("title", "").startswith("[LIGAR AGORA]") and "onfirmar a reunião" in t.get("title", "") and not t.get("completed")
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


def toque_pendente(cs, etapas, aplicar):
    """Quem tem ligação a fazer hoje fica na Minha fila até ligar (01/10, dono: a lista só mostra quem tem
    tentativa vencida). A lista entra por `fila-tel`; a Cadência Inbound tira essa tag 25 min depois do toque,
    feito ou não. Aqui ela volta para quem tem tarefa de ligação ABERTA e ainda sem ligação depois dela —
    a mesma regra que fecha a tarefa no finalizar_tarefas.py. Dia de toque por WhatsApp fica na visão do WhatsApp."""
    from finalizar_tarefas import criadas, decidir, historico, regra
    n = 0
    for c in cs:
        tags = {str(t).lower() for t in c.get("tags") or []}
        if etapas.get(c["id"]) != CONECTAR or c.get("dnd") or not c.get("phone") or TESTE.search(c.get("contactName") or ""):
            continue
        if tags & FORA or tags & {"fila-tel", "fila-wa", "wa-feito-hoje", "falou-hoje"}:
            continue
        ts = [t for t in (pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or [])
              if not t.get("completed") and regra(t.get("title")) in ("ligacao", "resposta")]
        if not ts:
            continue
        datas = criadas(c["id"])
        for t in ts:
            t["dateAdded"] = t.get("dateAdded") or datas.get(t["id"]) or ""
        calls, msgs = historico(c["id"])
        if not any(t["dateAdded"] and decidir(t, c, calls, msgs) is None for t in ts):
            continue
        n += 1
        print("  + fila-tel  %s  (tarefa de ligação aberta, sem ligação depois)%s" % (c.get("contactName") or c["id"], "" if aplicar else " DRY"))
        if aplicar:
            pedir("POST", "/contacts/%s/tags" % c["id"], {"tags": ["fila-tel"]})
        c["tags"] = list(c.get("tags") or []) + ["fila-tel"]
    print("toque pendente: %d lead(s) de volta à fila%s" % (n, "" if aplicar else " (DRY)"))


def solta_toque_feito(cs, etapas, aplicar, agora):
    """Toque já feito sai da Minha fila (01/10, dono: o que não é do dia some). A Cadência Inbound deixa
    `fila-tel` por 22 h a 2 dias depois do toque e só o registro do Resultado a tira antes; sem registro, o
    lead ligado ontem reaparecia hoje. Sai quem já recebeu ligação e não tem motivo para ficar: nenhuma tarefa
    de ligação pendente, não voltou a falar depois da ligação, não é fechar horário nem retorno vencido, e
    (lead `sem-cadencia`) recebeu ligação há menos de 24 h."""
    from atuador_filas import ultimo_contato
    from finalizar_tarefas import criadas, decidir, historico, regra
    n = 0
    for c in cs:
        tags = {str(t).lower() for t in c.get("tags") or []}
        if "fila-tel" not in tags or etapas.get(c["id"]) != CONECTAR or tags & {"fechar-horario", "retorno-vencido"}:
            continue
        ligou, respondeu = ultimo_contato(c["id"])
        if ligou is None or (respondeu is not None and respondeu > ligou):
            continue
        if "sem-cadencia" in tags and (agora - ligou).total_seconds() >= 24 * 3600:
            continue
        ts = [t for t in (pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or [])
              if not t.get("completed") and regra(t.get("title")) in ("ligacao", "resposta")]
        if ts:
            datas = criadas(c["id"])
            for t in ts:
                t["dateAdded"] = t.get("dateAdded") or datas.get(t["id"]) or ""
            calls, msgs = historico(c["id"])
            if any(not t["dateAdded"] or decidir(t, c, calls, msgs) is None for t in ts):
                continue
        n += 1
        print("  - fila-tel  %s  (toque já feito, sem tarefa de ligação pendente)%s" % (c.get("contactName") or c["id"], "" if aplicar else " DRY"))
        if aplicar:
            pedir("DELETE", "/contacts/%s/tags" % c["id"], {"tags": ["fila-tel"]})
        c["tags"] = [t for t in c.get("tags") or [] if str(t).lower() != "fila-tel"]
    print("toque feito: %d lead(s) saíram da fila%s" % (n, "" if aplicar else " (DRY)"))


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(dt.timezone.utc)
    etapas = etapa_por_contato()
    cs = contatos()
    solta_confirmacao(cs, etapas, aplicar, agora)
    solta_toque_feito(cs, etapas, aplicar, agora)
    toque_pendente(cs, etapas, aplicar)
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
