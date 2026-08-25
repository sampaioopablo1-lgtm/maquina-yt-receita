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

O corte NAO e uma opcao deste script: ele entra na consulta que monta o arquivo
de `--trabalho`, filtrando `videos.publicado_em >= CORTE_TRILHA_CONFIAVEL`. Os
videos anteriores existem e continuam sem credito; o que falta neles nao e
execucao, e saber qual faixa esta no audio. Isso se descobre ouvindo, e nao
consultando o banco.

DOIS LIMITES DIFERENTES, e confundi-los custou um dia. `videos.update` custa 50
unidades, `videos.list` custa 1, e subir um video custa 1.600, tudo contra um
teto DIARIO por projeto do Google Cloud — e os treze canais usam o mesmo
projeto (777159180424), entao dividem um teto so. Esse e o primeiro limite, e
`--limite` existe para ele: um pedaco por ciclo, reservando antes a publicacao
do dia.

O segundo limite e de TAXA, por janela curta, e nao tem nada a ver com o
volume do dia. Em 25/08/2026 eu disparei cerca de noventa escritas em rajada e
tomei 403 "exceeded your quota" na metade do lote. Concluí que era o teto
diario e parei o trabalho ate a virada — e cinquenta minutos depois a mesma
chamada respondeu 200. Era taxa.

A mensagem dos dois e IDENTICA; quem separa e o `reason`. Dai `--pausa` entre
gravacoes, `--esperas` para recuar e tentar de novo quando for taxa, e parada
imediata do lote quando for cota diaria — porque nesse caso insistir so gasta
tentativa. `motivo_403` faz essa separacao e `test_credito_atrasado` a prende.
"""

import argparse
import json
import os
import sys
import time
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
        corpo = e.read()[:400].decode("utf-8", "replace")
        return f"{PREFIXO_ERRO[motivo_403(e.code, corpo)]}: HTTP {e.code} {corpo[:160]}"
    return "creditado"


# Os dois 403 da API do YouTube parecem iguais no texto e pedem coisas
# opostas. Medido em 25/08/2026: rodei cerca de noventa escritas em rajada,
# tomei 403 "exceeded your quota", concluí que era o teto DIARIO e parei o
# trabalho ate a virada — e cinquenta minutos depois a mesma chamada
# funcionou. Nao era o teto do dia, era o limite de TAXA por janela curta.
#
# A diferenca importa porque a acao e oposta: taxa pede PAUSA e retomada em
# minutos; cota diaria pede parar ate a virada. Confundir as duas custa um dia
# inteiro de trabalho que estava disponivel.
#
# `reason` e o campo que separa, e nao a mensagem: rateLimitExceeded e
# userRateLimitExceeded sao taxa; quotaExceeded e dia.
MOTIVO_TAXA = "taxa"
MOTIVO_DIA = "dia"
MOTIVO_OUTRO = "outro"
PREFIXO_ERRO = {MOTIVO_TAXA: "erro de taxa", MOTIVO_DIA: "erro de cota diaria",
                MOTIVO_OUTRO: "erro ao gravar"}


def motivo_403(codigo, corpo):
    """Separa limite de TAXA de cota DIARIA pelo `reason`, nao pela mensagem."""
    if codigo != 403:
        return MOTIVO_OUTRO
    try:
        erros = json.loads(corpo).get("error", {}).get("errors") or []
        razoes = {e.get("reason", "") for e in erros}
    except (ValueError, AttributeError):
        razoes = set()
    if razoes & {"rateLimitExceeded", "userRateLimitExceeded"}:
        return MOTIVO_TAXA
    if "quotaExceeded" in razoes:
        return MOTIVO_DIA
    return MOTIVO_OUTRO


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
    p.add_argument("--pausa", type=float, default=1.5,
                   help="segundos entre GRAVACOES. Existe porque rajada toma "
                        "403 de TAXA: em 25/08 cerca de noventa escritas "
                        "seguidas derrubaram o lote pela metade")
    p.add_argument("--esperas", type=int, default=3,
                   help="quantas vezes recuar e tentar de novo quando o 403 "
                        "for de taxa (espera 30s, 60s, 120s)")
    args = p.parse_args()

    trabalho = json.load(open(args.trabalho, encoding="utf-8"))
    linhas, mudados, parar = [], 0, False
    for lote in trabalho:
        if parar:
            break
        canal, acc, faixa = lote["canal"], lote["token"], lote["faixa"]
        if not acc:
            linhas.append(f"{canal}\t—\tsem token (reautorize o canal)")
            continue
        for vid in lote["videos"]:
            if parar:
                linhas.append(f"{canal}\t{vid}\tadiado (cota diaria acabou)")
                continue
            if mudados >= args.limite:
                linhas.append(f"{canal}\t{vid}\tadiado (limite {args.limite})")
                continue

            r = consertar(acc, vid, faixa, seco=args.seco)

            # Limite de TAXA e transitorio: recua e tenta de novo. Cota DIARIA
            # nao adianta insistir — para o lote inteiro e deixa dito no
            # relatorio o que ficou para a virada.
            espera, tentativa = 30, 0
            while r.startswith(PREFIXO_ERRO[MOTIVO_TAXA]) and tentativa < args.esperas:
                tentativa += 1
                print(f"{canal}\t{vid}\ttaxa — esperando {espera}s "
                      f"({tentativa}/{args.esperas})", flush=True)
                time.sleep(espera)
                espera *= 2
                r = consertar(acc, vid, faixa, seco=args.seco)
            if r.startswith(PREFIXO_ERRO[MOTIVO_DIA]):
                parar = True

            if r == "creditado":
                mudados += 1
                time.sleep(args.pausa)
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
