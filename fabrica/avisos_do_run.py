#!/usr/bin/env python3
"""Conta os avisos `NARRACAO PELO PIPER` do run do RENDER, pela API do GitHub.

POR QUE ISTO EXISTE. O provedor de narracao se MEDE pela anotacao do job (733):
um aviso por cena do Piper, zero se o edge narrou. Ate 18/10 essa contagem era
feita por MIM, a mao, depois de cada publicacao — e o `duracao_a_medir` exige o
provedor na gravacao justamente porque inferi-lo depois e o erro do 733. Para a
publicacao registrar sozinha o ponto da serie, a contagem tem de sair do
runner, no mesmo passo que publica.

O QUE ELE NAO FAZ: nao adivinha. Se o run tem mais de um job com anotacao e
nenhum nome casa com o pacote, devolve `job=None` e quem chama NAO parqueia —
parquear com job errado inventaria provedor, que e pior que nao ter ponto.

Rede so por `get`, injetavel: os testes passam um dicionario no lugar.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

API = "https://api.github.com"
MARCA = "NARRACAO PELO PIPER"


def _get_github(url: str, token: str | None = None):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "maquina-yt-receita",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def jobs_do_run(repo: str, run_id: str, get) -> list[dict]:
    d = get(f"{API}/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100")
    return list(d.get("jobs", [])) if isinstance(d, dict) else []


def anotacoes_do_job(repo: str, job_id, get) -> list[dict]:
    d = get(f"{API}/repos/{repo}/check-runs/{job_id}/annotations?per_page=100")
    return list(d) if isinstance(d, list) else []


def escolhe_job(jobs: list[dict], pacote: str, com_anotacao: set) -> dict | None:
    """O job do render DESTE pacote. Pelo nome quando a matriz e de varios;
    pelo unico com anotacao quando so ha um; None quando e ambiguo."""
    pelo_nome = [j for j in jobs if pacote and pacote in (j.get("name") or "")]
    if len(pelo_nome) == 1:
        return pelo_nome[0]
    if len(pelo_nome) > 1:
        return None
    unicos = [j for j in jobs if j.get("id") in com_anotacao]
    return unicos[0] if len(unicos) == 1 else None


def contar(repo: str, run_id: str, pacote: str, get) -> dict:
    jobs = jobs_do_run(repo, run_id, get)
    por_job = {}
    for j in jobs:
        anots = anotacoes_do_job(repo, j.get("id"), get)
        if anots:
            por_job[j.get("id")] = anots
    job = escolhe_job(jobs, pacote, set(por_job))
    if job is None:
        return {"avisos_piper": None, "job": None, "jobs": len(jobs),
                "motivo": "job do render ambiguo ou sem anotacao: nao conto"}
    n = sum(1 for a in por_job.get(job.get("id"), [])
            if MARCA in (a.get("message") or ""))
    return {"avisos_piper": n, "job": str(job.get("id")), "jobs": len(jobs),
            "motivo": ""}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        print("uso: avisos_do_run.py <run_id> <pacote> [owner/repo]", file=sys.stderr)
        return 2
    run_id, pacote = argv[0], argv[1]
    repo = argv[2] if len(argv) > 2 else os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    try:
        r = contar(repo, run_id, pacote, lambda u: _get_github(u, token))
    except Exception as e:                                  # noqa: BLE001
        r = {"avisos_piper": None, "job": None, "jobs": 0, "motivo": f"api: {e}"}
    print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
