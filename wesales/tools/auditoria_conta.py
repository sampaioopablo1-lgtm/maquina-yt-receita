#!/usr/bin/env python3
"""Cruza a CONTA AO VIVO com os dumps — o conserto de fundo que faltava.

O BURACO QUE ISTO FECHA, anotado varias vezes e nunca resolvido: as cinco
auditorias leem `wesales/workflows-json/`, que e fotografia. **Nada cruzava a
lista de dumps com a lista real de workflows da conta**, e o descolamento correu
nos dois sentidos:

- em 23/09/2026 eu tratei o `Reengajamento 90 dias` como defeito vivo; era dump
  de workflow morto, substituido pela Nutricao em 22/09 (§2.40);
- no mesmo dia o G-23 achou o oposto: `F-13` publicado na conta com desenho
  diferente do documentado, e um alerta (`Proposta Pendente`) que **nenhum
  documento catalogava**.

Nenhuma das cinco auditorias podia pegar isso, porque todas partem do dump.

O QUE ESTE SCRIPT VE, e o que nao ve. Ele usa o **token publico** (`GHL_PIT`),
que lista workflows mas **nao devolve os nos**. O detalhe no-por-no vem da API
interna, que exige bearer de sessao logada (`.local/_ghl_bearer.txt`, renovado
por navegador headless) e **nao roda em GitHub Action**. Entao:

  ve   nome, status e data de cada workflow da conta; campos personalizados;
       etapas do pipeline; contagem por etapa
  nao  o conteudo dos nos ao vivo — para isso, o dono precisa re-exportar

Dividir assim e de proposito: o que da para conferir sem o PC roda todo dia de
graca, e o que exige o PC fica explicito em vez de silencioso.

Uso:  GHL_PIT=... python3 auditoria_conta.py
Sai 1 se houver divergencia entre a conta e os dumps.
"""
import glob
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"
LOC = "1D53YTI9C7oIMBavcQxV"
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
UA = "wesales-auditoria-conta/1.0 (+https://github.com/sampaioopablo1-lgtm/maquina-yt-receita)"

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")


def pede(caminho, token):
    req = Request(BASE + caminho, headers={
        "Authorization": "Bearer " + token, "Version": VERSION,
        "Accept": "application/json", "user-agent": UA})
    with urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode() or "{}")


def dos_dumps():
    """{nome: status} de cada dump que e workflow de verdade."""
    saida = {}
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        if not isinstance(dado, dict):          # `_campos.json` e lista
            continue
        wf = dado.get("workflow")
        if not isinstance(wf, dict) or not wf.get("id"):
            continue
        saida[wf.get("name") or os.path.basename(caminho)[:-5]] = wf.get("status")
    return saida


def secao(titulo):
    print("\n" + "=" * 72)
    print(titulo)
    print("=" * 72)


def main():
    token = os.environ.get("GHL_PIT", "").strip()
    if not token:
        print("sem GHL_PIT no ambiente — este script le a conta ao vivo")
        return 2

    divergencias = []

    # ---------- 1) workflows: a conta contra os dumps ----------
    secao("WORKFLOWS — a conta contra `workflows-json/`")
    try:
        r = pede("/workflows/?locationId=" + LOC, token)
    except HTTPError as e:
        corpo = (e.read() or b"")[:200].decode("utf-8", "replace")
        print("nao consegui listar workflows: HTTP %s %s" % (e.code, corpo))
        print("\nSe for 401/403, o `GHL_PIT` precisa do escopo `workflows.readonly`.")
        return 2
    except URLError as e:
        print("rede indisponivel: %s" % e.reason)
        return 1

    vivos = {w.get("name"): w for w in (r.get("workflows") or [])}
    dump = dos_dumps()
    print("  na conta: %d workflows | em dump: %d" % (len(vivos), len(dump)))

    so_conta = sorted(set(vivos) - set(dump))
    so_dump = sorted(set(dump) - set(vivos))
    if so_conta:
        print("\n  NA CONTA E SEM DUMP — nenhuma auditoria olha estes:")
        for n in so_conta:
            print("     %-40s [%s]" % (n[:40], (vivos[n] or {}).get("status")))
        divergencias.append("%d workflow(s) sem dump" % len(so_conta))
    if so_dump:
        print("\n  EM DUMP E NAO NA CONTA — dump de workflow morto:")
        for n in so_dump:
            print("     %-40s [%s no dump]" % (n[:40], dump[n]))
        divergencias.append("%d dump(s) de workflow inexistente" % len(so_dump))

    difere = [(n, dump[n], (vivos[n] or {}).get("status"))
              for n in sorted(set(vivos) & set(dump))
              if dump[n] != (vivos[n] or {}).get("status")]
    if difere:
        print("\n  STATUS DIFERENTE entre conta e dump:")
        for n, d, v in difere:
            print("     %-36s dump=%-10s conta=%s" % (n[:36], d, v))
        divergencias.append("%d workflow(s) com status divergente" % len(difere))
    if not (so_conta or so_dump or difere):
        print("  nenhuma divergencia: os dumps cobrem a conta, nome por nome")

    # ---------- 2) etapas do pipeline ----------
    secao("PIPELINE — etapas e contagem por etapa")
    try:
        p = pede("/opportunities/pipelines?locationId=" + LOC, token)
        funil = next((x for x in (p.get("pipelines") or []) if x.get("id") == PIPELINE), None)
        if not funil:
            print("  pipeline %s nao encontrado" % PIPELINE)
            divergencias.append("pipeline nao encontrado")
        else:
            for st in (funil.get("stages") or []):
                q = ("/opportunities/search?location_id=%s&pipeline_id=%s"
                     "&pipeline_stage_id=%s&status=open&limit=1" % (LOC, PIPELINE, st.get("id")))
                total = ((pede(q, token).get("meta") or {}).get("total"))
                print("  %-26s %4s open" % ((st.get("name") or "?")[:26], total))
    except HTTPError as e:
        print("  nao consegui ler o pipeline: HTTP %s" % e.code)

    # ---------- 3) campos personalizados ----------
    secao("CAMPOS PERSONALIZADOS — a conta contra `_campos.json`")
    try:
        cf = pede("/locations/" + LOC + "/customFields", token)
        na_conta = {c.get("name"): c.get("id") for c in (cf.get("customFields") or [])}
        print("  na conta: %d campos" % len(na_conta))
        caminho = os.path.join(DUMPS, "_campos.json")
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as fh:
                lista = json.load(fh)
            no_dump = {c.get("name"): c.get("id") for c in lista if isinstance(c, dict)}
            print("  em `_campos.json`: %d" % len(no_dump))
            novos = sorted(set(na_conta) - set(no_dump))
            sumidos = sorted(set(no_dump) - set(na_conta))
            for rot, lst in (("NA CONTA E FORA DO DUMP", novos),
                             ("NO DUMP E FORA DA CONTA", sumidos)):
                if lst:
                    print("\n  %s:" % rot)
                    for n in lst:
                        print("     %s" % n)
                    divergencias.append("%d campo(s): %s" % (len(lst), rot.lower()))
            if not (novos or sumidos):
                print("  nenhuma divergencia de campo")
        else:
            print("  `_campos.json` nao existe — nada com que comparar")
    except HTTPError as e:
        print("  nao consegui ler os campos: HTTP %s" % e.code)

    # ---------- veredito ----------
    secao("VEREDITO")
    if divergencias:
        for d in divergencias:
            print("  - %s" % d)
        print("\nDivergencia entre conta e dump e o unico achado que nenhuma das")
        print("cinco auditorias de dump consegue ver. Vale olhar.")
    else:
        print("  conta e dumps batem no que este token consegue ver.")
    print("\nLIMITE: o token publico nao devolve os NOS dos workflows. Auditoria")
    print("no-por-no ao vivo exige a API interna, que so roda no PC do dono.")
    return 1 if divergencias else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
