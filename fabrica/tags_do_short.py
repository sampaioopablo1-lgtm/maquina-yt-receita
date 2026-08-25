#!/usr/bin/env python3
"""Repoe as tags dos shorts que o `apontar_para_longo` apagou.

O DEFEITO, medido em 25/08/2026 perguntando a API e nao lendo o codigo: de 138
videos da frota, 40 estao sem tag nenhuma. Conferi 21 deles contra a tabela
`videos`: os 21 sao `shorts`. Nenhum longo. Zero.

Essa assimetria e a prova. O unico passo que o short atravessa e o longo nao e
o `apontar_para_longo`, que le o snippet do short e o grava de volta com o link
do longo no fim. Logo apos o upload essa leitura as vezes volta SEM `tags` — o
video ainda esta sendo indexado — e o write-back grava o snippet incompleto por
cima. Intermitente, silencioso, e nada falha: quatro de seis shorts numa
amostra, 45% dos shorts da frota no total.

A causa esta corrigida no `publicar.py` (o snippet do upload volta como `base`
e repoe o que a leitura perdeu). Este arquivo trata do que ja esta no ar, que e
o que esta em uso.

DE ONDE VEM A TAG CERTA, e esta e a parte que evita inventar: do LONGO DO MESMO
PACOTE. O `publicar.py` monta as tags do short como os OITO PRIMEIROS da lista
do longo — `(cp["short_tags"] or cp["tags"])[:8]` — e o `orcamento_tags` so
corta acima de 480 caracteres, teto que oito tags nunca alcancam. Entao os oito
primeiros do longo publicado SAO, caractere a caractere, o que o short tinha
antes de ser apagado. Nao ha reconstrucao nem palpite: a fonte esta no ar, no
video irmao, com as quinze tags intactas.

Short cujo longo tambem esta sem tags nao e reparado aqui — sem fonte confiavel
nao se escreve tag, e o script diz qual ficou de fora em vez de adivinhar.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://youtube.googleapis.com/youtube/v3"

# O mesmo corte que o `publicar.py` aplica ao montar o short.
TAGS_DO_SHORT = 8


def _req(url, data=None, method=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers=headers or {})
    return urllib.request.urlopen(req, timeout=60)


def snippets(acc, ids):
    """Le ate 50 snippets por chamada — `videos.list` custa 1 unidade."""
    fora = {}
    for i in range(0, len(ids), 50):
        lote = ids[i:i + 50]
        r = json.load(_req(f"{API}/videos?part=snippet&id=" + ",".join(lote),
                           headers={"Authorization": "Bearer " + acc}))
        for it in r.get("items", []):
            fora[it["id"]] = it["snippet"]
    return fora


def repor(acc, short_id, snip, tags, seco=False):
    """Grava o snippet INTEIRO com as tags de volta.

    Manda o snippet lido inteiro, e nao um objeto novo: `videos.update` apaga
    todo campo de snippet que nao chegar. Escrever so `tags` aqui repetiria o
    defeito que este arquivo existe para consertar, um degrau adiante.
    """
    if snip.get("tags"):
        return "ja tinha tags"
    if not tags:
        return "sem fonte: o longo do mesmo pacote tambem esta sem tags"
    novo = dict(snip)
    novo["tags"] = tags
    if seco:
        return f"CABE ({len(tags)} tags) — nada enviado"
    try:
        _req(f"{API}/videos?part=snippet",
             data=json.dumps({"id": short_id, "snippet": novo}).encode(),
             method="PUT",
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "application/json; charset=UTF-8"})
    except urllib.error.HTTPError as e:
        return f"erro: HTTP {e.code} {e.read()[:160].decode('utf-8', 'replace')}"
    return f"reposto ({len(tags)} tags)"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trabalho", required=True,
                   help='JSON [{"canal":..,"token":..,'
                        '"pares":[{"short":id,"longo":id}, ..]}, ..]')
    p.add_argument("--limite", type=int, default=40,
                   help="teto de shorts ALTERADOS nesta rodada (cada update "
                        "custa 50 unidades; publicar um pacote custa ~3.855)")
    p.add_argument("--seco", action="store_true",
                   help="le e diz o que faria, sem gravar nada")
    args = p.parse_args()

    trabalho = json.load(open(args.trabalho, encoding="utf-8"))
    linhas, mudados = [], 0
    for lote in trabalho:
        canal, acc = lote["canal"], lote["token"]
        if not acc:
            linhas.append(f"{canal}\t—\tsem token (reautorize o canal)")
            continue
        pares = lote["pares"]
        vistos = snippets(acc, [x["short"] for x in pares]
                          + [x["longo"] for x in pares])
        for par in pares:
            s, l = par["short"], par["longo"]
            if mudados >= args.limite:
                linhas.append(f"{canal}\t{s}\tadiado (limite {args.limite})")
                continue
            snip = vistos.get(s)
            if not snip:
                linhas.append(f"{canal}\t{s}\tsumiu (apagado, privado ou de outro canal)")
                continue
            fonte = (vistos.get(l) or {}).get("tags") or []
            r = repor(acc, s, snip, fonte[:TAGS_DO_SHORT], seco=args.seco)
            if r.startswith("reposto"):
                mudados += 1
            linhas.append(f"{canal}\t{s}\t{r}")
            print(linhas[-1], flush=True)

    resumo = {}
    for l in linhas:
        chave = l.split("\t")[2].split("(")[0].split(":")[0].strip()
        resumo[chave] = resumo.get(chave, 0) + 1
    print("\nRESUMO:", json.dumps(resumo, ensure_ascii=False))
    return 1 if any("\terro" in l for l in linhas) else 0


if __name__ == "__main__":
    sys.exit(main())
