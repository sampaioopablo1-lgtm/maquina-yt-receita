#!/usr/bin/env python3
"""Monitor do CRM (01/10, pedido do dono): "monitorar todos os logs, e quando voltarmos vermos os avanços, erros".

Roda no GitHub (wesales-monitor.yml), de hora em hora. Só LÊ. Junta num relatório:

  1. Robôs       cada robô do relógio rodado em simulação (DRY): quebrou? o que faria agora?
  2. GitHub      rodadas das rotinas wesales-* nas últimas 26 h e os "falhou nesta rodada" do relógio
  3. CRM         leads novos, réguas, Minha fila, ligações e registros de hoje, mensagens automáticas,
                 lead sem resposta, tarefas abertas, reuniões
  4. Inscrições  histórico de inscrição de todos os workflows publicados: presas e esperas vencidas
                 (monitor_inscricoes.js, com a sessão do CRM), e em que passo das cadências os leads estão
  5. Avanços     diferença para a leitura anterior

Grava em MONITOR_DIR (na nuvem: repositório PRIVADO opc-crm-dados/monitor — este repositório é público e
nunca recebe nome de lead):
  ULTIMO.md          a leitura mais recente, completa
  AAAA-MM-DD.md      resumo de cada leitura do dia, a mais nova em cima
  historico.csv      uma linha de números por leitura (para ver tendência)
  estado.json        números da última leitura (base da comparação)

    python monitor.py            # lê e grava em wesales/.local/monitor
    python monitor.py --rapido   # pula a simulação dos robôs e as inscrições
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from atuador_filas import CONECTAR, LOC, PRIORIDADE, TESTE, contatos, etapa_por_contato, pedir, valor  # noqa: E402

DIR = os.environ.get("MONITOR_DIR") or os.path.join(AQUI, "..", ".local", "monitor")
REPO = os.environ.get("GITHUB_REPOSITORY") or "sampaioopablo1-lgtm/maquina-yt-receita"
RAMO = os.environ.get("GITHUB_REF_NAME") or "claude/youtube-publication-next-steps-v7o4el"
BR = dt.timezone(dt.timedelta(hours=-3))
AGORA = dt.datetime.now(dt.timezone.utc)
HOJE = AGORA.astimezone(BR).date()
ACAO = "oc7FTlIhIpiH90oZxPyx"
AGENDAS = {"oOfR9ADPJM0WyVyHRgKE": "closer", "3uNQFjCEDe7b4gKZJuOZ": "SDR"}
CADENCIAS = {"c2375e2f": "Cadência Inbound", "c64a808b": "Cadência 12x30", "17e6dc19": "12x30 parte 2",
             "02511c72": "MI-0", "10065adb": "Lembretes da Reunião"}
CORTE_JANELA = dt.datetime(2026, 9, 30, 23, 40, tzinfo=dt.timezone.utc)
ROBOS = ["calendly_para_crm", "preencher_qualificacao", "finalizar_tarefas", "cadencia_noshow", "reunioes_robo",
         "link_formulario", "atuador_filas", "wa_governador", "ordem_fila"]

alertas: list[str] = []
numeros: dict = {}


def ts(s: str) -> dt.datetime:
    d = dt.datetime.fromisoformat(str(s).replace(" ", "T").replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=BR)


def hm(s) -> str:
    return ts(s).astimezone(BR).strftime("%d/%m %H:%M")


def primeiro(c) -> str:
    return ((c.get("firstName") or c.get("contactName") or c.get("firstNameLowerCase") or "?").split() or ["?"])[0].title()


def gh(*args) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    if r.returncode:
        raise RuntimeError((r.stderr or r.stdout)[:200])
    return r.stdout


# ---------------------------------------------------------------- 1. robôs em simulação
def robos() -> list[str]:
    out = ["| Robô | Estado | Última linha |", "|---|---|---|"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    ruins = 0
    for nome in ROBOS:
        if nome == "calendly_para_crm" and not os.environ.get("CALENDLY_TOKEN"):
            out.append("| %s | sem token aqui | — |" % nome)
            continue
        try:
            r = subprocess.run([sys.executable, os.path.join(AQUI, nome + ".py")], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=900, env=env)
            txt = (r.stdout or "") + (r.stderr or "")
            ultima = ([l for l in txt.strip().splitlines() if l.strip()] or ["(sem saída)"])[-1].strip()[:110]
            ok = r.returncode == 0 and "Traceback" not in txt
        except subprocess.TimeoutExpired:
            ok, ultima = False, "passou de 15 min"
        if not ok:
            ruins += 1
            alertas.append("Robô `%s` quebrou na simulação: %s" % (nome, ultima))
        out.append("| %s | %s | %s |" % (nome, "ok" if ok else "**ERRO**", ultima.replace("|", "/")))
    numeros["robos_com_erro"] = ruins
    return out


# ---------------------------------------------------------------- 2. rotinas do GitHub
def github() -> list[str]:
    desde = (AGORA - dt.timedelta(hours=26)).strftime("%Y-%m-%dT%H:%M:%SZ")
    runs = json.loads(gh("api", "repos/%s/actions/runs?per_page=100&created=>=%s" % (REPO, desde))).get("workflow_runs", [])
    # só a ramificação onde o CRM roda: outras ramificações carregam cópias velhas dos mesmos arquivos e falham à toa
    runs = [r for r in runs if ("wesales" in (r.get("path") or "").lower() or "faxina" in (r.get("path") or "").lower())
            and r.get("head_branch") == RAMO]
    por = {}
    for r in runs:
        por.setdefault(r["name"], Counter())[r.get("conclusion") or r.get("status")] += 1
    out = ["| Rotina | Rodadas em 26 h |", "|---|---|"]
    falhas = 0
    for nome, c in sorted(por.items()):
        out.append("| %s | %s |" % (nome, ", ".join("%s %d" % (k, v) for k, v in c.most_common())))
        # o relógio aparece "cancelled" por desenho (laço que se relança); falha de verdade é "failure"
        falhas += c.get("failure", 0) + c.get("timed_out", 0)
        if c.get("failure") or c.get("timed_out"):
            alertas.append("Rotina **%s** falhou %d vez(es) nas últimas 26 h" % (nome, c.get("failure", 0) + c.get("timed_out", 0)))
    numeros["rotinas_falhas_26h"] = falhas
    rel = [r for r in runs if "relogio" in (r.get("path") or "") and r.get("status") == "completed" and r.get("conclusion") == "success"]
    andando = [r for r in runs if "relogio" in (r.get("path") or "") and r.get("status") in ("in_progress", "queued")]
    if not andando:
        alertas.append("O **relógio** (filas, tarefas, Calendly, reuniões) não está rodando agora")
    numeros["relogio_rodando"] = int(bool(andando))
    if rel:
        r = sorted(rel, key=lambda x: x["created_at"])[-1]
        log = gh("run", "view", str(r["id"]), "--repo", REPO, "--log")
        linhas = [l for l in log.splitlines() if " || echo " not in l]
        rodadas = sum(1 for l in linhas if "==== " in l and " ====" in l)
        quebras = Counter(re.sub(r"^.*?Z ", "", l).strip()[:60] for l in linhas if "falhou nesta rodada" in l or "Traceback" in l)
        out += ["", "Última rodada completa do relógio: começou %s, %d ciclo(s) em horário comercial." % (hm(r["created_at"]), rodadas)]
        for k, v in quebras.most_common():
            out.append("- %d× %s" % (v, k))
            alertas.append("No relógio: %d× \"%s\"" % (v, k))
        if not quebras:
            out.append("- nenhum robô falhou dentro dela")
        numeros["relogio_falhas_ultima"] = sum(quebras.values())
    return out


# ---------------------------------------------------------------- 3. CRM
def crm(cs, etapas) -> list[str]:
    reais = [c for c in cs if not TESTE.search(c.get("contactName") or "")]
    con = [c for c in reais if etapas.get(c["id"]) == CONECTAR]
    tg = lambda c: {str(t).lower() for t in c.get("tags") or []}
    dia = lambda c: ts(c["dateAdded"]).astimezone(BR).date()
    numeros.update(leads_total=len(reais), leads_hoje=sum(1 for c in reais if dia(c) == HOJE),
                   leads_ontem=sum(1 for c in reais if dia(c) == HOJE - dt.timedelta(days=1)),
                   conectar=len(con),
                   regua_inbound=sum(1 for c in con if "cad-inbound" in tg(c) and "sem-cadencia" not in tg(c)),
                   regua_12x30=sum(1 for c in con if "cad-outbound" in tg(c)),
                   fora_da_cadencia=sum(1 for c in con if "sem-cadencia" in tg(c)),
                   fila_whatsapp=sum(1 for c in con if "fila-wa" in tg(c)),
                   wa_esperando=sum(1 for c in reais if "wa-aguardando" in tg(c)),
                   wa_liberados_hoje=sum(1 for c in reais if "wa-lib-%s" % HOJE.isoformat() in tg(c)))
    fila = []
    for c in reais:
        t = tg(c)
        if "nao-perturbe" in t:
            continue
        if (etapas.get(c["id"]) == CONECTAR and not t & {"status-perdido", "falou-hoje"}
                and t & {"fila-tel", "fechar-horario", "retorno-vencido"}) or t & {"confirmar-reuniao", "fila-noshow"}:
            fila.append(c)
    numeros["minha_fila"] = len(fila)
    acoes = Counter(re.sub(r"[^\w\s:áéíóúâêôãõç/-]", "", str(valor(c, ACAO) or "sem texto")).strip() for c in fila)

    # conversas de quem mexeu nas últimas 48 h
    ini = dt.datetime.combine(HOJE, dt.time(0, 0), BR)
    lig, conv, auto, entrou, sem_resp = 0, 0, Counter(), 0, []
    reg = Counter()
    recentes = [c for c in reais if c.get("dateUpdated") and ts(c["dateUpdated"]) > AGORA - dt.timedelta(hours=48)]
    for c in recentes:
        ult_in = ult_out = None
        teve = False
        for cv in pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, c["id"])).get("conversations") or []:
            for m in ((pedir("GET", "/conversations/%s/messages?limit=40" % cv["id"]).get("messages") or {}).get("messages") or []):
                if not m.get("dateAdded"):
                    continue
                q = ts(m["dateAdded"])
                if m.get("direction") == "inbound":
                    ult_in = q if ult_in is None or q > ult_in else ult_in
                    entrou += q >= ini
                    continue
                if m.get("source") != "workflow":
                    ult_out = q if ult_out is None or q > ult_out else ult_out
                if q < ini:
                    continue
                if m.get("messageType") == "TYPE_CALL":
                    if m.get("userId"):
                        lig += 1
                        teve = True
                        conv += (((m.get("meta") or {}).get("call") or {}).get("duration") or 0) >= 25
                elif m.get("source") == "workflow":
                    auto[m.get("status") or "?"] += 1
        if ult_in and (ult_out is None or ult_out < ult_in) and AGORA - ult_in > dt.timedelta(minutes=30) \
                and not tg(c) & {"nao-perturbe", "status-perdido"}:
            sem_resp.append((ult_in, primeiro(c)))
        if teve or ts(c["dateUpdated"]) >= ini:
            for n in pedir("GET", "/contacts/%s/notes" % c["id"]).get("notes") or []:
                corpo = re.sub("<[^>]+>", "", n.get("body") or "")
                if "Ligação registrada:" in corpo and n.get("dateAdded") and ts(n["dateAdded"]) >= ini:
                    reg[corpo.split("Ligação registrada:")[1].strip()[:30]] += 1
    numeros.update(ligacoes_hoje=lig, conversas_25s_hoje=conv, registros_hoje=sum(reg.values()),
                   msgs_automaticas_hoje=sum(auto.values()), msgs_do_lead_hoje=entrou, leads_sem_resposta=len(sem_resp))
    falhou = sum(v for k, v in auto.items() if k in ("failed", "undelivered"))
    if falhou:
        alertas.append("%d mensagem(ns) automática(s) com falha de entrega hoje" % falhou)
    for q, nome in sorted(sem_resp)[:8]:
        alertas.append("Lead **%s** escreveu às %s e ninguém respondeu" % (nome, hm(q.isoformat())))
    local = AGORA.astimezone(BR)
    if local.weekday() < 5 and local.hour >= 11 and lig == 0:
        alertas.append("Nenhuma ligação de pessoa hoje até %s" % local.strftime("%H:%M"))

    # tarefas abertas
    tarefas, depois = [], None
    for _ in range(20):
        corpo = {"completed": False, "limit": 100}
        if depois:
            corpo["searchAfter"] = depois
        lote = pedir("POST", "/locations/%s/tasks/search" % LOC, corpo).get("tasks") or []
        tarefas += lote
        if len(lote) < 100:
            break
        depois = lote[-1].get("searchAfter")
    tipo = lambda t: (re.match(r"\[[^\]\d]+", t.get("title") or "") or re.match(r"", "")).group(0).strip("[ ") or "outras"
    por_tipo = Counter(tipo(t) for t in tarefas)
    vencidas = Counter(tipo(t) for t in tarefas if t.get("dueDate") and ts(t["dueDate"]) < AGORA - dt.timedelta(hours=24))
    numeros.update(tarefas_abertas=len(tarefas), tarefas_vencidas_24h=sum(vencidas.values()))

    # reuniões
    reun = []
    for cal, dono in AGENDAS.items():
        a = int((AGORA - dt.timedelta(days=3)).timestamp() * 1000)
        b = int((AGORA + dt.timedelta(days=3)).timestamp() * 1000)
        for e in pedir("GET", "/calendars/events?locationId=%s&calendarId=%s&startTime=%d&endTime=%d" % (LOC, cal, a, b)).get("events") or []:
            reun.append((ts(e["startTime"]), e.get("appointmentStatus") or "?", e.get("contactId"), dono))
    por_id = {c["id"]: c for c in cs}
    futuras = sorted(r for r in reun if r[0] > AGORA and r[1] == "confirmed")
    passadas = Counter(r[1] for r in reun if r[0] <= AGORA)
    numeros.update(reunioes_futuras=len(futuras), reunioes_compareceu_3d=passadas.get("showed", 0),
                   reunioes_noshow_3d=passadas.get("noshow", 0), reunioes_sem_resultado=passadas.get("confirmed", 0))
    for r in futuras:
        c = por_id.get(r[2]) or {}
        if r[0] - AGORA < dt.timedelta(hours=6) and "confirmar-reuniao" in tg(c):
            alertas.append("Reunião de **%s** às %s ainda sem confirmação" % (primeiro(c), hm(r[0].isoformat())))
    if passadas.get("confirmed"):
        alertas.append("%d reunião(ões) já passaram sem resultado (compareceu/faltou) marcado" % passadas["confirmed"])

    n = numeros
    out = ["| Leads | |", "|---|---|",
           "| Novos hoje / ontem | %d / %d |" % (n["leads_hoje"], n["leads_ontem"]),
           "| Em CONECTAR | %d |" % n["conectar"],
           "| Na cadência de lead novo (5 toques) | %d |" % n["regua_inbound"],
           "| Na cadência de 12 toques | %d |" % n["regua_12x30"],
           "| Fora da cadência, esperando a entrada gradual | %d |" % n["fora_da_cadencia"],
           "", "| Trabalho de hoje | |", "|---|---|",
           "| Minha fila agora | %d (%s) |" % (n["minha_fila"], "; ".join("%s: %d" % kv for kv in acoes.most_common(6)) or "vazia"),
           "| Visão Ligar pelo WhatsApp | %d |" % n["fila_whatsapp"],
           "| Ligações de pessoa hoje | %d (%d com 25 s ou mais) |" % (lig, conv),
           "| Resultados registrados hoje | %d%s |" % (sum(reg.values()), (" — " + ", ".join("%s: %d" % kv for kv in reg.most_common(6))) if reg else ""),
           "| Mensagens automáticas hoje | %d%s |" % (sum(auto.values()), (" — " + ", ".join("%s: %d" % kv for kv in auto.most_common())) if auto else ""),
           "| WhatsApp liberado hoje / esperando o limite | %d / %d |" % (n["wa_liberados_hoje"], n["wa_esperando"]),
           "| Mensagens de lead hoje / leads sem resposta há 30 min+ | %d / %d |" % (entrou, len(sem_resp)),
           "", "| Tarefas abertas | Total | Vencidas há mais de 24 h |", "|---|---|---|"]
    for k, v in por_tipo.most_common(10):
        out.append("| %s | %d | %d |" % (k, v, vencidas.get(k, 0)))
    out += ["", "| Reuniões | |", "|---|---|",
            "| Próximas (3 dias) | %s |" % (", ".join("%s %s" % (primeiro(por_id.get(r[2]) or {}), hm(r[0].isoformat())) for r in futuras) or "nenhuma"),
            "| Últimos 3 dias | %s |" % (", ".join("%s: %d" % kv for kv in passadas.most_common()) or "nenhuma")]
    return out


# ---------------------------------------------------------------- 4. inscrições dos workflows
def inscricoes() -> list[str]:
    wfs = {w["id"]: w["name"] for w in pedir("GET", "/workflows/?locationId=%s" % LOC).get("workflows") or [] if w.get("status") == "published"}
    numeros["workflows_publicados"] = len(wfs)
    arq = os.path.join(DIR, "_inscricoes.json")
    for _ in range(2):   # a tela às vezes demora a mandar os cabeçalhos: tenta de novo antes de desistir
        r = subprocess.run(["node", os.path.join(AQUI, "monitor_inscricoes.js"), arq, *wfs], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900)
        if r.returncode == 0:
            break
    if r.returncode:
        alertas.append("Não li o histórico de inscrições (sessão do CRM vencida? recadastrar o segredo GHL_STORAGE_STATE): %s"
                       % (r.stdout + r.stderr).strip()[-120:])
        numeros["inscricoes_lidas"] = 0
        return ["Não foi possível ler: %s" % (r.stdout + r.stderr).strip()[-160:]]
    d = json.load(open(arq, encoding="utf-8"))
    os.remove(arq)
    limite = AGORA - dt.timedelta(hours=1)
    presas, residuo, out = 0, 0, []
    for w, v in d.items():
        st = v.get("statuses") or []
        ruins, velhas = Counter(), 0
        for s in st:
            if s["status"] not in ("finished", "wait_time", "wait", "waiting"):
                motivo = "%s (%s)" % (s["passo"] or "?", s["status"])
            elif s["status"] != "finished" and s.get("retoma") and ts(s["retoma"]) < limite:
                motivo = "%s (espera vencida)" % (s["passo"] or "?")
            else:
                continue
            # travou ANTES da retirada da janela de horário (30/09 20:36 BRT): resíduo conhecido, não é erro novo
            if ts(s["mexida"]) < CORTE_JANELA:
                velhas += 1
            else:
                ruins[motivo] += 1
        residuo += velhas
        if velhas:
            out.append("- %s: %d presa(s) de antes de 30/09 (resíduo conhecido da janela de horário)" % (wfs.get(w, w), velhas))
        if ruins:
            presas += sum(ruins.values())
            out.append("- **%s**: %s" % (wfs.get(w, w), "; ".join("%d em %s" % (n, k) for k, n in ruins.most_common(5))))
            alertas.append("%d inscrição(ões) presa(s) em **%s** (travaram depois de 30/09)" % (sum(ruins.values()), wfs.get(w, w)))
        if v.get("total") and v["total"] > len(st):
            out.append("- %s: li %d de %d inscrições (as mais recentes)" % (wfs.get(w, w), len(st), v["total"]))
    numeros.update(inscricoes_lidas=len(d), inscricoes_presas=presas, inscricoes_residuo_antigo=residuo)
    out = ["%d workflows publicados lidos. Inscrições presas novas: **%d**. Resíduo antigo: %d." % (len(d), presas, residuo)] + out
    out += ["", "| Cadência | Em andamento | Onde os leads estão |", "|---|---|---|"]
    for w, v in d.items():
        nome = CADENCIAS.get(w[:8])
        if not nome:
            continue
        vivos = [s for s in v.get("statuses") or [] if s["status"] != "finished"]
        numeros["andando_" + w[:8]] = len(vivos)
        passos = Counter(s["passo"] or "?" for s in vivos)
        out.append("| %s | %d | %s |" % (nome, len(vivos), "; ".join("%s: %d" % kv for kv in passos.most_common(5)) or "—"))
    return out


# ---------------------------------------------------------------- 5. avanços e gravação
ROTULO = {"leads_total": "leads no CRM", "conectar": "leads em CONECTAR", "regua_12x30": "leads na cadência de 12 toques",
          "fora_da_cadencia": "leads fora da cadência", "ligacoes_hoje": "ligações de pessoa hoje",
          "registros_hoje": "resultados registrados hoje", "msgs_automaticas_hoje": "mensagens automáticas hoje",
          "minha_fila": "leads na Minha fila", "tarefas_abertas": "tarefas abertas",
          "reunioes_futuras": "reuniões marcadas à frente", "inscricoes_presas": "inscrições presas",
          "leads_sem_resposta": "leads sem resposta"}


def avancos(ant: dict) -> list[str]:
    if not ant:
        return ["Primeira leitura: sem comparação."]
    out = []
    mesmo_dia = ant.get("_dia") == HOJE.isoformat()
    for k, rot in ROTULO.items():
        a, b = ant.get(k), numeros.get(k)
        if a is None or b is None or a == b or (k.endswith("_hoje") and not mesmo_dia):
            continue
        out.append("- %s: %s → **%s** (%+d)" % (rot, a, b, b - a))
    return out or ["Nenhum número mudou desde %s." % ant.get("_quando", "a leitura anterior")]


def secao(titulo: str, f, *args) -> list[str]:
    try:
        corpo = f(*args)
    except Exception as e:  # uma parte que falha não derruba o relatório
        alertas.append("O monitor não conseguiu ler \"%s\": %s" % (titulo, str(e)[:140]))
        corpo = ["Não foi possível ler: %s" % str(e)[:200]]
    return ["", "## " + titulo, ""] + corpo


def main() -> int:
    rapido = "--rapido" in sys.argv
    os.makedirs(DIR, exist_ok=True)
    arq_estado = os.path.join(DIR, "estado.json")
    ant = json.load(open(arq_estado, encoding="utf-8")) if os.path.exists(arq_estado) else {}
    quando = AGORA.astimezone(BR).strftime("%d/%m/%Y %H:%M")
    etapas, cs = etapa_por_contato(), contatos()
    corpo = []
    corpo += secao("CRM", crm, cs, etapas)
    if not rapido:
        corpo += secao("Inscrições nos workflows", inscricoes)
        corpo += secao("Robôs (simulação)", robos)
    corpo += secao("Rotinas do GitHub", github)
    av = avancos(ant)
    topo = ["# Monitor do CRM — %s" % quando, "",
            "## Erros e alertas (%d)" % len(alertas), ""] + (["- " + a for a in alertas] or ["Nenhum."]) + \
           ["", "## Avanços desde %s" % ant.get("_quando", "o início"), ""] + av
    open(os.path.join(DIR, "ULTIMO.md"), "w", encoding="utf-8", newline="\n").write("\n".join(topo + corpo) + "\n")

    # resumo do dia, o mais novo em cima
    arq_dia = os.path.join(DIR, HOJE.isoformat() + ".md")
    velho = open(arq_dia, encoding="utf-8").read() if os.path.exists(arq_dia) else ""
    velho = re.sub(r"^# .*\n\n", "", velho)
    n = numeros
    bloco = ["## %s" % quando[-5:], "",
             "Leads novos %s · CONECTAR %s · Minha fila %s · ligações %s · registros %s · mensagens automáticas %s · inscrições presas %s"
             % tuple(n.get(k, "?") for k in ("leads_hoje", "conectar", "minha_fila", "ligacoes_hoje", "registros_hoje",
                                              "msgs_automaticas_hoje", "inscricoes_presas")), ""] + \
            (["Alertas:"] + ["- " + a for a in alertas] if alertas else ["Sem alertas."]) + \
            ["", "Avanços:"] + av + [""]
    open(arq_dia, "w", encoding="utf-8", newline="\n").write("# Monitor do CRM — %s\n\n%s\n%s" % (HOJE.strftime("%d/%m/%Y"), "\n".join(bloco), velho))

    cols = ["quando"] + sorted(k for k in numeros)
    arq_csv = os.path.join(DIR, "historico.csv")
    linhas = list(csv.DictReader(open(arq_csv, encoding="utf-8"))) if os.path.exists(arq_csv) else []
    linhas.append(dict(numeros, quando=AGORA.astimezone(BR).strftime("%Y-%m-%d %H:%M"), alertas=len(alertas)))
    cols = ["quando", "alertas"] + sorted({k for l in linhas for k in l} - {"quando", "alertas"})
    with open(arq_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(linhas)
    json.dump(dict(numeros, _quando=quando, _dia=HOJE.isoformat(), _alertas=len(alertas)), open(arq_estado, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    # no log público do Actions só vão números
    print("monitor %s | alertas %d | %s" % (quando, len(alertas), json.dumps(numeros, ensure_ascii=False)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
