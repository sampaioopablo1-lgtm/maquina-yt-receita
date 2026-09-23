"""Faxina de Tarefas — exclui tarefa AUTOMATICA aberta que perdeu o contexto.

Decisao do dono (22/09/2026, D12 em PLANO-MULTICANAL.md): quando o lead muda
de etapa, de status ou de resultado, as tarefas abertas que nao valem mais
sao EXCLUIDAS (nao concluidas: concluir inventaria historico falso), e o
cancelamento vira uma NOTA no contato. Tarefa concluida nunca e tocada.
Tarefa sem prefixo de automacao (criada a mao) nunca e tocada.

Por estado, nao por tag: a cada execucao le todas as tarefas abertas da
subconta e confere cada uma contra o estado ATUAL do lead. Idempotente.

Roda de graca no GitHub Actions (repositorio publico = minutos ilimitados).
O LOG E PUBLICO: nunca imprime nome, telefone, e-mail ou texto de contato —
so contagens e ids.

Uso:
  GHL_TOKEN=<Private Integration Token> python faxina_tarefas.py           # so relatorio
  GHL_TOKEN=... python faxina_tarefas.py --aplicar                          # exclui
Escopos do token: contacts.readonly contacts.write opportunities.readonly
locations/tasks.readonly
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request

LOC = "1D53YTI9C7oIMBavcQxV"
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
ETAPA = {
    "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d": "NOVO LEAD",
    "deb60542-a5cd-43ae-b875-b467b120a72c": "CONECTAR",
    "3d26fcd1-220d-49ed-8325-705dfe9055b1": "REUNIAO",      # REUNIAO DE DIAGNOSTICO (era AGENDAR)
    "cbcf0229-5e19-4fdb-8c50-6c641b78b3bb": "NEGOCIAR",
    "b8485ec0-98e8-459f-b990-f40a5e3bd25b": "FORMALIZAR",
}
RESULTADO = "nPafc9c0JdSSptdPhUlF"      # campo "Resultado da tentativa"
BASE = "https://services.leadconnectorhq.com"
CARENCIA_MIN = 5          # tarefa mais nova que isto nunca e excluida (corrida com o workflow)
TETO_EXCLUSOES = 200      # por execucao
TETO_FRACAO = 0.5         # se for excluir mais que isto das tarefas automaticas abertas, so relata


def familia(titulo):
    """Familia da tarefa pelo prefixo do titulo. None = nao e automacao."""
    t = (titulo or "").strip().upper()
    if t.startswith("[CADENCIA] SINAL") or t.startswith("[SINAL]"):
        return "SINAL"
    if t.startswith("[CADENCIA] NS") or t.startswith("[NO-SHOW]"):
        return "NO-SHOW"
    if t.startswith("[CADENCIA]"):
        return "CADENCIA"
    if t.startswith("[RETORNO]"):
        return "RETORNO"
    if t.startswith("[FECHAR HORÁRIO]") or t.startswith("[FECHAR HORARIO]") \
            or t.startswith("[CONECTADO]"):
        return "FECHAR"
    if t.startswith("[CLOSER]"):
        return "CLOSER"
    return None


def validas(etapa, status, resultado):
    """Familias que podem ficar abertas neste estado do lead."""
    if status != "open" or etapa is None:
        return set()                                   # perdido, nutricao, ganho, sem oportunidade
    if etapa == "CONECTAR":
        if resultado == "Pediu retorno":
            return {"RETORNO", "SINAL"}
        if resultado == "Atendeu":
            return {"FECHAR", "SINAL"}
        return {"CADENCIA", "SINAL"}
    if etapa == "REUNIAO":
        return {"CLOSER", "NO-SHOW"}
    if etapa == "NEGOCIAR":
        return {"CLOSER"}
    return set()                                       # NOVO LEAD, FORMALIZAR


def motivo(etapa, status, resultado):
    if status != "open" or etapa is None:
        return {"lost": "oportunidade perdida", "abandoned": "lead foi para nutrição",
                "won": "negócio ganho"}.get(status, "lead sem oportunidade aberta")
    if etapa == "CONECTAR":
        return "resultado da tentativa: " + (resultado or "vazio")
    return "lead está na etapa " + {"REUNIAO": "REUNIÃO DE DIAGNÓSTICO"}.get(etapa, etapa)


class Api:
    def __init__(self, token):
        self.h = {"Authorization": "Bearer " + token, "Version": "2021-07-28",
                  "Accept": "application/json", "Content-Type": "application/json"}

    def req(self, metodo, caminho, corpo=None):
        dados = json.dumps(corpo).encode() if corpo is not None else None
        for tentativa in range(4):
            r = urllib.request.Request(BASE + caminho, data=dados, headers=self.h, method=metodo)
            try:
                with urllib.request.urlopen(r, timeout=60) as resp:
                    txt = resp.read().decode() or "{}"
                    return json.loads(txt)
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    time.sleep(2 * (tentativa + 1))
                    continue
                raise RuntimeError("%s %s -> HTTP %s" % (metodo, caminho.split("?")[0], e.code))
        raise RuntimeError("%s %s -> sem resposta" % (metodo, caminho.split("?")[0]))


def tarefas_abertas(api):
    out, pagina = [], 0
    while True:
        r = api.req("POST", "/locations/%s/tasks/search" % LOC,
                    {"completed": False, "limit": 100, "skip": pagina * 100})
        lote = r.get("tasks") or []
        out += lote
        if len(lote) < 100:
            return out
        pagina += 1


def estado(api, contato):
    c = api.req("GET", "/contacts/" + contato).get("contact") or {}
    res = next((f.get("value") for f in c.get("customFields") or []
                if f.get("id") == RESULTADO), None)
    ops = api.req("GET", "/opportunities/search?location_id=%s&contact_id=%s&pipeline_id=%s"
                  % (LOC, contato, PIPELINE)).get("opportunities") or []
    abertas = [o for o in ops if o.get("status") == "open"]
    alvo = sorted(abertas or ops, key=lambda o: o.get("updatedAt") or "", reverse=True)
    if not alvo:
        return None, None, res
    o = alvo[0]
    return ETAPA.get(o.get("pipelineStageId")), o.get("status"), res


def idade_min(t):
    s = t.get("dateAdded") or t.get("createdAt")
    if not s:
        return 1e9
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (dt.datetime.now(dt.timezone.utc) - d).total_seconds() / 60


def main():
    aplicar = "--aplicar" in sys.argv
    token = os.environ.get("GHL_TOKEN")
    if not token:
        sys.exit("falta GHL_TOKEN")
    api = Api(token)
    todas = tarefas_abertas(api)
    auto = [t for t in todas if familia(t.get("title")) and t.get("contactId")]
    por_contato = {}
    for t in auto:
        por_contato.setdefault(t["contactId"], []).append(t)

    excluir = []
    for contato, ts in por_contato.items():
        etapa, status, res = estado(api, contato)
        ok = validas(etapa, status, res)
        for t in ts:
            if familia(t["title"]) not in ok and idade_min(t) >= CARENCIA_MIN:
                excluir.append((contato, t, motivo(etapa, status, res)))

    print("tarefas abertas: %d | automaticas: %d | contatos: %d | a excluir: %d"
          % (len(todas), len(auto), len(por_contato), len(excluir)))
    if auto and len(excluir) > max(10, TETO_FRACAO * len(auto)):
        print("TRAVA: exclusao anormal (> %d%% das automaticas) — so relatorio" % (TETO_FRACAO * 100))
        aplicar = False
    if not aplicar:
        fams = {}
        for _, t, _m in excluir:
            fams[familia(t["title"])] = fams.get(familia(t["title"]), 0) + 1
        print("relatorio (nada excluido):", json.dumps(fams))
        return
    feitos = 0
    for contato, t, m in excluir[:TETO_EXCLUSOES]:
        quando = (t.get("dateAdded") or "")[:16].replace("T", " ")
        api.req("POST", "/contacts/%s/notes" % contato,
                {"body": "Tarefa \"%s\" (criada %s UTC) cancelada automaticamente pela "
                         "Faxina de Tarefas: %s." % (t.get("title"), quando, m)})
        api.req("DELETE", "/contacts/%s/tasks/%s" % (contato, t["id"]))
        feitos += 1
    print("excluidas: %d (nota registrada em cada contato)" % feitos)


if __name__ == "__main__":
    main()
