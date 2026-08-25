#!/usr/bin/env python3
"""Poe o credito CC-BY na descricao de video JA PUBLICADO.

POR QUE ISTO EXISTE. Ate 25/08/2026 o `ler_copy` perdia a secao da musica
quando ela vinha depois do comentario fixado, e o video subia sem atribuicao.
Medido ao vivo, pedindo o snippet a API: NENHUM dos videos da frota tinha o
credito. O defeito foi corrigido no `publicar.py`, mas correcao de codigo nao
alcanca o que ja esta no ar — e o que ja esta no ar e o que esta em uso.

Nao e detalhe de estilo. As faixas sao CC-BY do Kevin MacLeod, e a licenca
exige atribuicao ONDE A OBRA E USADA. Sem ela o uso simplesmente nao esta
licenciado, em doze canais e oito idiomas.

O CORTE POR DATA, e ele e o coracao deste arquivo. Creditar a faixa ERRADA e
tao ruim quanto nao creditar — o docstring do `copy_md.credito_trilha` diz
isso com todas as letras. Ate o commit 8544196 (13/08/2026 19:23 UTC) a faixa
saia de um HASH do slug, e o hash divide pelos arquivos PRESENTES: bastava um
mp3 faltar no bucket para o canal receber outra faixa, calado. Depois desse
commit quem manda e `canais.trilha`, e a MESMA funcao decide o audio e o
credito — entao para esses videos `canais.trilha` e prova, nao palpite.

Por isso o padrao e `--desde 2026-08-13T19:23:31Z` e o script RECUSA rodar sem
corte. Os videos anteriores existem e continuam sem credito; o que falta neles
nao e execucao, e saber qual faixa esta no audio. Isso se descobre ouvindo, e
nao consultando o banco.

QUOTA, e aqui esta a parte que engana. `videos.update` custa 50 unidades,
`videos.list` custa 1, e subir um video custa 1.600. O teto de 10.000 e POR
PROJETO do Google Cloud, nao por canal — e conferido em 25/08/2026, os treze
canais usam o MESMO projeto (777159180424). Entao os treze dividem um unico
teto diario, e a frota inteira (132 updates = 6.600) somada a uma publicacao
(~3.800 entre os dois formatos, thumbnail, legenda e playlist) passa dos
10.000. Um pedaco por ciclo, com `--limite`, e o que cabe: terminar hoje nao
vale parar a esteira, porque quota estourada derruba a publicacao do dia
inteiro e o credito atrasado pode esperar mais um ciclo.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://youtube.googleapis.com/youtube/v3"

# O commit 8544196: a partir dele `canais.trilha` vence o hash, no audio e no
# credito. Antes disso o banco nao prova qual faixa foi usada.
CORTE_TRILHA_CONFIAVEL = "2026-08-13T19:23:31Z"

MAX_DESCRICAO = 5000        # teto do YouTube para snippet.description


def credito(faixa: str) -> str:
    """O MESMO texto que `copy_md.credito_trilha` poe no copy.md.

    Nao chamo `credito_trilha` aqui porque ela lista os mp3 do disco para
    descobrir a faixa, e neste script a faixa ja vem do banco. O formato,
    porem, tem de ser identico ao que a esteira escreve — senao o mesmo canal
    passa a ter duas redacoes do mesmo credito. `test_credito_atrasado` cobra
    essa igualdade contra a funcao de verdade.
    """
    nome = faixa.replace("_", " ")
    return (f"Music: {nome} by Kevin MacLeod (incompetech.com) — Licensed under "
            "Creative Commons: By Attribution 4.0\n"
            "http://creativecommons.org/licenses/by/4.0/")


def _req(url, data=None, method=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers=headers or {})
    return urllib.request.urlopen(req, timeout=60)


def ja_credita(descricao: str) -> bool:
    """Pela URL da licenca, nao pelo nome da faixa.

    O nome muda de canal para canal; a URL nao muda nunca. E se a descricao ja
    traz a URL, o credito ja esta la de alguma forma — reescrever so criaria
    uma segunda copia.
    """
    return "creativecommons.org/licenses" in (descricao or "")


def consertar(acc: str, youtube_id: str, faixa: str, seco: bool = False) -> str:
    """Le o snippet, decide, e devolve o que aconteceu — sempre uma string.

    `videos.update` exige o snippet INTEIRO: mandar so a descricao APAGA
    titulo, tags e categoria. Por isso le antes, e por isso nunca monta um
    snippet do zero.
    """
    try:
        r = json.load(_req(f"{API}/videos?part=snippet&id={youtube_id}",
                           headers={"Authorization": "Bearer " + acc}))
    except urllib.error.HTTPError as e:
        return f"erro ao ler: HTTP {e.code} {e.read()[:120].decode('utf-8', 'replace')}"
    itens = r.get("items") or []
    if not itens:
        # Video apagado, privado ou de outro canal. Nao e falha do script.
        return "sumiu (apagado, privado, ou fora deste canal)"

    snip = itens[0]["snippet"]
    desc = snip.get("description") or ""
    if ja_credita(desc):
        return "ja creditava"

    novo = f"{desc.rstrip()}\n\n{credito(faixa)}"
    if len(novo) > MAX_DESCRICAO:
        # Truncar a descricao para caber o credito trocaria um problema por
        # outro. Quem decide o que sai e uma pessoa, nao este laco.
        return f"nao coube: {len(novo)} chars, teto {MAX_DESCRICAO}"
    if seco:
        return f"CABE (+{len(novo) - len(desc)} chars) — nada enviado"

    snip["description"] = novo
    try:
        _req(f"{API}/videos?part=snippet",
             data=json.dumps({"id": youtube_id, "snippet": snip}).encode(),
             method="PUT",
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "application/json; charset=UTF-8"})
    except urllib.error.HTTPError as e:
        corpo = e.read()[:200].decode("utf-8", "replace")
        return f"erro ao gravar: HTTP {e.code} {corpo}"
    return "creditado"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trabalho", required=True,
                   help='JSON [{"canal":..,"token":..,"faixa":..,'
                        '"videos":[id,..]}, ..]')
    p.add_argument("--limite", type=int, default=60,
                   help="teto de videos ALTERADOS nesta rodada (quota: cada "
                        "update custa 50 unidades e subir video custa 1.600)")
    p.add_argument("--seco", action="store_true",
                   help="le e diz o que faria, sem gravar nada")
    p.add_argument("--saida", default="",
                   help="grava o relatorio linha a linha neste arquivo")
    args = p.parse_args()

    trabalho = json.load(open(args.trabalho, encoding="utf-8"))
    linhas, mudados = [], 0
    for lote in trabalho:
        canal, acc, faixa = lote["canal"], lote["token"], lote["faixa"]
        if not acc:
            linhas.append(f"{canal}\t—\tsem token (reautorize o canal)")
            continue
        for vid in lote["videos"]:
            if mudados >= args.limite:
                linhas.append(f"{canal}\t{vid}\tadiado (limite {args.limite})")
                continue
            r = consertar(acc, vid, faixa, seco=args.seco)
            if r == "creditado":
                mudados += 1
            linhas.append(f"{canal}\t{vid}\t{r}")
            print(linhas[-1], flush=True)

    resumo = {}
    for l in linhas:
        resumo[l.split("\t")[2].split(":")[0]] = \
            resumo.get(l.split("\t")[2].split(":")[0], 0) + 1
    print("\nRESUMO:", json.dumps(resumo, ensure_ascii=False))
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas) + "\n")
    # Erro de gravacao nao pode sair verde: e justamente o caso em que alguem
    # precisa olhar de novo.
    return 1 if any("\terro" in l for l in linhas) else 0


if __name__ == "__main__":
    sys.exit(main())
