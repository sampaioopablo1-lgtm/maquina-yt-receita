"""Calibracao agregada da regua de qualificacao (secao 9.1) — F-28.

O F-03 ("Loop do closer") prometeu no proprio "Pronto quando": dar pra dizer
"nota >= 70 acerta X%" e corrigir a regua com dado, nao com achismo. O
workflow 5.1 (build-wesales.md) cumpre a metade em tempo real — compara a
nota com o veredito do closer no instante em que ele e registrado e avisa o
gestor quando os dois discordam (nota >= 70 e "Nao", ou nota < 45 e "Sim").
Mas nenhum lugar deste projeto soma esses casos ao longo do tempo: a mesma
pergunta que Reev/Meetime respondem com reuniao semanal manual (call review
entre SDR e closer) nunca ganhou aqui a versao automatica — so o caso
isolado, nunca a taxa agregada. Este script fecha essa metade, so leitura,
zero escrita no CRM: nao depende do `APROVADO.md`.

So conta contato que JA recebeu veredito do closer (`Data do veredito do
closer` preenchida) e que NAO e contato de teste — teste conta como acerto
ou erro falso e mentiria pro gestor logo na primeira leitura (foi o que
quase aconteceu nesta rodada: o unico veredito real na subconta em
28/09/2026 e do contato "9940", teste do proprio dono para o
build_estagnacao.py, ROADMAP-SALES-ENGAGEMENT.md G-23/F-28).

Uso:
  GHL_TOKEN=<Private Integration Token> python3 calibracao_regua.py            # so imprime
  GHL_TOKEN=... python3 calibracao_regua.py --escrever                          # tambem grava
                                                                                   RELATORIO-CALIBRACAO.md
Escopos do token: contacts.readonly opportunities.readonly

Roda de graca no GitHub Actions, mesmo padrao do faxina_tarefas.py — mas
publicar o cron fica fora deste script (arquivo .github/*, fora de
`wesales/`, regra 5 da rotina).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

LOC = "1D53YTI9C7oIMBavcQxV"
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
BASE = "https://services.leadconnectorhq.com"

# Etapas onde o closer ja pode ter atuado — antes de REUNIAO ninguem deu
# veredito (build-wesales.md, secao 5.1: o gatilho e o proprio preenchimento
# do closer, que so acontece depois do agendamento).
ETAPAS_COM_CLOSER = {
    "3d26fcd1-220d-49ed-8325-705dfe9055b1": "REUNIÃO DE DIAGNÓSTICO",
    "cbcf0229-5e19-4fdb-8c50-6c641b78b3bb": "NEGOCIAR",
    "b8485ec0-98e8-459f-b990-f40a5e3bd25b": "FORMALIZAR",
}

C_NOTA = "FHoXQnLYA8LW5mFzfdIq"          # Nota de qualificação
C_VEREDITO = "c470gqXWCkwqE9yVrcEi"      # Reunião foi qualificada
C_MOTIVO = "5L0RMR1HZVQ7IevyjOQX"        # Motivo da desqualificação
C_DATA_VEREDITO = "ffIpN8kTlhncr7K00Xzy"  # Data do veredito do closer

# Faixas da secao 9.1 (build-wesales.md) — os mesmos cortes que os nos 5/6
# do workflow 5.1 usam para o alerta de calibracao.
FAIXAS = [
    ("A (>=70)", lambda n: n >= 70),
    ("B (45-69)", lambda n: 45 <= n < 70),
    ("C (25-44)", lambda n: 25 <= n < 45),
    ("D (<25)", lambda n: n < 25),
]

# Contatos de teste conhecidos (APROVADO.md, secao "Contatos de teste", e o
# contato "9940" usado pelo dono para testar build_estagnacao.py — G-23 do
# ROADMAP-SALES-ENGAGEMENT.md). Lista fechada + heuristica de nome/e-mail
# como rede de seguranca para teste futuro que ainda nao tem ID registrado.
IDS_TESTE = {
    "Lj96CIFYaGKPiC0opzbc", "OIvOGQfdGg2Ndr5GtcAG", "vrwdERfR24ax6GylG6No",
    "qkHSdIMPJTB2JK5ECGrY", "2MXzDPjxGjuvvsxlp5V1", "c5r3ZxiAd8T5adL1Bt6j",
    "rdaijzR0ZVCmXLAJ6jT2",  # "Pablo Sampaio" / +55 21 98742-9940
}


def eh_teste(contato: dict) -> bool:
    if contato.get("id") in IDS_TESTE:
        return True
    alvo = " ".join([
        contato.get("firstName") or "", contato.get("lastName") or "",
        contato.get("email") or "",
    ]).lower()
    return "teste" in alvo or alvo.strip().startswith("zz ")


class Api:
    def __init__(self, token: str):
        self.h = {"Authorization": "Bearer " + token, "Version": "2021-07-28",
                  "Accept": "application/json",
                  "User-Agent": "Mozilla/5.0 (Calibracao-WeSales)"}

    def get(self, caminho: str, params: dict) -> dict:
        qs = "&".join("%s=%s" % (k, v) for k, v in params.items())
        r = urllib.request.Request(BASE + caminho + "?" + qs, headers=self.h)
        try:
            with urllib.request.urlopen(r, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError("GET %s -> HTTP %d: %s" % (caminho, e.code, e.read().decode()))


def valor(campos: list, campo_id: str):
    for c in campos:
        if c.get("id") == campo_id:
            return c.get("value")
    return None


def opos_com_closer(api: Api) -> list:
    achados = []
    for pagina in range(1, 6):  # teto de seguranca; a subconta tem 64 oportunidades no total
        r = api.get("/opportunities/search", {
            "location_id": LOC, "pipeline_id": PIPELINE, "status": "all",
            "limit": 100, "page": pagina,
        })
        pag = r.get("opportunities", [])
        if not pag:
            break
        achados.extend(o for o in pag if o.get("pipelineStageId") in ETAPAS_COM_CLOSER)
        if len(pag) < 100:
            break
    return achados


def calibrar(token: str) -> dict:
    api = Api(token)
    candidatas = opos_com_closer(api)
    linhas_teste, sem_veredito, com_veredito = [], [], []
    for opp in candidatas:
        cid = opp.get("contactId")
        if not cid:
            continue
        r = api.get("/contacts/%s" % cid, {})
        contato = r.get("contact", {})
        campos = contato.get("customFields", [])
        nome = "%s %s" % (contato.get("firstName") or "", contato.get("lastName") or "")
        if eh_teste(contato):
            linhas_teste.append(nome.strip())
            continue
        if not valor(campos, C_DATA_VEREDITO):
            sem_veredito.append(nome.strip())
            continue
        nota = valor(campos, C_NOTA)
        veredito = valor(campos, C_VEREDITO)
        if nota is None or veredito is None:
            continue
        com_veredito.append({
            "nome": nome.strip(), "nota": int(nota), "veredito": veredito,
            "motivo": valor(campos, C_MOTIVO),
        })

    por_faixa = {}
    alertas = []
    for rotulo, teste in FAIXAS:
        do_grupo = [c for c in com_veredito if teste(c["nota"])]
        sim = sum(1 for c in do_grupo if c["veredito"] == "Sim")
        por_faixa[rotulo] = {"n": len(do_grupo), "sim": sim}
    for c in com_veredito:
        alta = c["nota"] >= 70 and c["veredito"] == "Não"
        baixa = c["nota"] < 45 and c["veredito"] == "Sim"
        if alta or baixa:
            alertas.append(dict(c, tipo="alta" if alta else "baixa"))

    return {
        "gerado_em": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "com_veredito": com_veredito, "por_faixa": por_faixa, "alertas": alertas,
        "excluidos_teste": linhas_teste, "aguardando_veredito": sem_veredito,
    }


def formatar_md(r: dict) -> str:
    linhas = [
        "# Calibração da régua de qualificação — F-28",
        "",
        "Gerado automaticamente por `wesales/tools/calibracao_regua.py`. "
        "Não escreve no CRM — só leitura. Sobrescrito a cada rodada; não edite à mão.",
        "",
        "Gerado em: %s" % r["gerado_em"],
        "",
        "## Amostra",
        "",
        "| Faixa | Vereditos | \"Sim\" | Taxa |",
        "|---|---|---|---|",
    ]
    for rotulo, dados in r["por_faixa"].items():
        n, sim = dados["n"], dados["sim"]
        taxa = "%.0f%%" % (100 * sim / n) if n else "—"
        linhas.append("| %s | %d | %d | %s |" % (rotulo, n, sim, taxa))
    linhas += ["", "## Casos que já dispararam (ou deveriam disparar) o alerta de calibração do 5.1", ""]
    if r["alertas"]:
        linhas.append("| Contato | Nota | Veredito | Motivo | Alerta |")
        linhas.append("|---|---|---|---|---|")
        for a in r["alertas"]:
            linhas.append("| %s | %d | %s | %s | %s |" % (
                a["nome"], a["nota"], a["veredito"], a["motivo"] or "—", a["tipo"]))
    else:
        linhas.append("Nenhum, nesta leitura.")
    linhas += ["", "## Excluídos por serem contato de teste", ""]
    linhas.append(", ".join(r["excluidos_teste"]) if r["excluidos_teste"] else "Nenhum.")
    linhas += ["", "## Em `REUNIÃO`/`NEGOCIAR`/`FORMALIZAR` sem veredito do closer ainda", ""]
    linhas.append(", ".join(r["aguardando_veredito"]) if r["aguardando_veredito"] else "Nenhum.")
    linhas.append("")
    return "\n".join(linhas)


if __name__ == "__main__":
    token = os.environ.get("GHL_TOKEN")
    if not token:
        sys.exit("defina GHL_TOKEN (Private Integration Token, escopos "
                 "contacts.readonly opportunities.readonly)")
    resultado = calibrar(token)
    texto = formatar_md(resultado)
    print(texto)
    if "--escrever" in sys.argv:
        destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "RELATORIO-CALIBRACAO.md")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(texto)
