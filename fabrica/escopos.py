#!/usr/bin/env python3
"""Quais canais conseguem medir retencao — e quais so sabem contar view.

Existe porque a resposta estava enterrada num comentario de codigo e o painel
mentia por cima dela. As 88 coletas em `metricas` traziam retencao, CTR,
impressoes, duracao media, inscritos e receita todos em ZERO, e nenhum desses
numeros jamais foi medido: os treze tokens carregam

    youtube, youtube.force-ssl, youtube.upload

e nao carregam `yt-analytics.readonly`. Sem esse escopo o
youtubeAnalytics.reports.query responde 403, o `diagnosticar` engole a excecao
num print vermelho, e o registro fica com o default do modelo — que ate hoje
era 0.0.

O estrago nao e faltar dado. E o banco AFIRMAR retencao de zero por cento, que
nao significa "nao medimos": significa "ninguem assiste nada". Passei a semana
inteira lendo isso como se fosse medicao.

Isto NAO se conserta em codigo. Cada canal precisa passar de novo pela tela de
consentimento do Google concedendo o escopo de analytics — treze vezes, uma vez
so. Este comando diz exatamente quais faltam.

Uso:
    python3 fabrica/escopos.py            # le os tokens do Supabase
    python3 fabrica/escopos.py --dados <arquivo.json>
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.request

ANALYTICS = "https://www.googleapis.com/auth/yt-analytics.readonly"
MONETARIO = "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"
UPLOAD = "https://www.googleapis.com/auth/youtube.upload"

# O que cada escopo destrava, para o relatorio dizer a consequencia e nao so o
# nome da permissao.
DEPENDE_DE_ANALYTICS = ("retencao", "CTR", "impressoes", "duracao media",
                        "inscritos ganhos")


def busca_tokens(sb_url: str, sb_key: str) -> dict[str, dict]:
    url = f"{sb_url}/rest/v1/config?chave=like.yt_token_*&select=chave,valor"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    with urllib.request.urlopen(req, timeout=60) as r:
        linhas = json.load(r)
    return {l["chave"].removeprefix("yt_token_"): l["valor"] for l in linhas}


def avalia(tokens: dict[str, dict]) -> dict:
    fora = {}
    for canal, tok in sorted(tokens.items()):
        escopos = set(tok.get("scopes") or [])
        fora[canal] = {
            "publica": UPLOAD in escopos,
            "mede_retencao": ANALYTICS in escopos,
            "mede_receita": MONETARIO in escopos,
            "escopos": sorted(escopos),
        }
    return fora


def relatorio(tokens: dict[str, dict]) -> str:
    est = avalia(tokens)
    sem = [c for c, i in est.items() if not i["mede_retencao"]]

    L = [f"ESCOPOS — {len(est)} canais", ""]
    L.append(f"{'canal':24} {'publica':>8} {'retencao':>9} {'receita':>8}")
    for canal, i in est.items():
        L.append(f"{canal:24} {'sim' if i['publica'] else 'NAO':>8} "
                 f"{'sim' if i['mede_retencao'] else 'NAO':>9} "
                 f"{'sim' if i['mede_receita'] else 'nao':>8}")
    L.append("")
    if sem:
        L.append(f"{len(sem)} de {len(est)} canais NAO medem "
                 f"{', '.join(DEPENDE_DE_ANALYTICS)}.")
        L.append("")
        L.append("Enquanto isso durar, qualquer mudanca de formato, b-roll ou")
        L.append("efeito visual e otimizacao as cegas: o video muda e o painel")
        L.append("continua sem resposta.")
        L.append("")
        L.append("CONSERTO — uma vez por canal, na maquina do Pablo:")
        L.append("    python3 -m maquina auth-youtube        # concede o escopo")
        L.append("Canais faltando: " + ", ".join(sem))
    else:
        L.append("Todos os canais medem retencao. O painel responde.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dados", default=None,
                   help="JSON {canal: token} para rodar sem rede")
    args = p.parse_args()

    if args.dados:
        tokens = json.load(open(args.dados, encoding="utf-8"))
    else:
        tokens = busca_tokens(os.environ["SUPABASE_URL"].rstrip("/"),
                              os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    print(relatorio(tokens))
    # Codigo 1 quando algum canal nao mede: da para usar como passo de workflow.
    return 1 if any(not i["mede_retencao"] for i in avalia(tokens).values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
