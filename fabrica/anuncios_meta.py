# -*- coding: utf-8 -*-
"""Cria anuncio de formulario instantaneo direto na API da Meta.

POR QUE ISTO EXISTE. O conector Ads MCP do claude.ai nao consegue criar anuncio
de lead nesta conta. Medido em 11/09/2026, com o `lead_gen_form_id` correto:

    Terms of Service Not Accepted (1892181)
    ... reading it requires the pages_manage_ads permission on the Page, which
    the Ads MCP connection does not currently request ...
    If the Page has already accepted, this request cannot be completed over
    MCP; use Ads Manager.

A pagina JA aceitou os termos (`leadgen_tos_accepted: true`, medido em 09/09). O
que falta e a conexao poder LER essa aceitacao. Um token de usuario do sistema
com `pages_manage_ads` le, e a documentacao da Meta trata esse token como o
caminho de automacao: ele nao depende de ninguem estar logado e nao expira.

Entao o caminho automatico nao passa por conector nenhum — passa por aqui, com
o token num segredo do repositorio. Um passo humano, uma vez: gerar o token.
Depois disso, mexer no spec e dar push publica os anuncios sozinho.

    META_ACCESS_TOKEN=... python3 fabrica/anuncios_meta.py spec.json
    META_ACCESS_TOKEN=... python3 fabrica/anuncios_meta.py spec.json --ativar

Sem `--ativar` o anuncio nasce PAUSADO, que e como a Meta cria e como as regras
desta conta mandam: ligar e uma decisao separada da de criar.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0"

# Campos que este programa NUNCA envia, em nenhuma circunstancia. Orcamento e
# lance sao decisao do Pablo (REGRA — corte de anuncio em 48 horas, trava 1).
# A lista nao e decorativa: `conferir_spec` reprova o spec que os contenha,
# entao nem um spec escrito errado consegue mexer em dinheiro por este caminho.
PROIBIDOS = ("daily_budget", "lifetime_budget", "bid_amount", "spend_cap",
             "budget_remaining", "daily_spend_cap")

# Minimo de anuncios entregando num conjunto. Trava 3 da mesma regra: conjunto
# com um anuncio so nao tem com o que comparar, e se ele for pausado o conjunto
# morre. Vale na hora de ATIVAR, nao na de criar.
MINIMO_ATIVOS = 2


class ErroMeta(Exception):
    """Erro devolvido pela Meta, com o texto dela — nao um 500 generico.

    O codigo importa: 1892181 e permissao de leitura dos termos, 3390001 e
    formulario faltando, 1885274 e conjunto de criativo dinamico. Cada um tem
    conserto diferente, e engolir a mensagem apaga essa diferenca.
    """


def _chamar(caminho, token, dados=None, metodo=None):
    url = f"{API}/{caminho}"
    corpo = None
    if dados is not None:
        corpo = urllib.parse.urlencode(dados).encode()
    req = urllib.request.Request(url, data=corpo, method=metodo)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            erro = json.load(e)["error"]
        except Exception:
            raise ErroMeta(f"HTTP {e.code} sem corpo JSON") from None
        cod = erro.get("error_subcode") or erro.get("code")
        raise ErroMeta(f"[{cod}] {erro.get('message', '')}") from None


def conferir_spec(spec):
    """Reprova o spec antes de qualquer chamada. Erro barato vem primeiro.

    Uma peca sem `conjunto` ou sem `form_id` so falharia depois de ja ter criado
    o criativo — e criativo e imutavel, entao o lixo fica na conta para sempre.
    """
    problemas = []
    vistos = set()
    # Tipos que fazem sentido num anuncio de formulario instantaneo. APPLY_NOW
    # e "Candidatar-se", que e o que FORMULARIO — campanha 2 decidiu: "Saiba
    # mais" convida a passear, "Candidatar-se" avisa que existe um criterio.
    CTAS = ("APPLY_NOW", "SIGN_UP", "LEARN_MORE", "GET_QUOTE", "SUBSCRIBE",
            "DOWNLOAD", "GET_OFFER", "BOOK_NOW", "CONTACT_US")
    for i, p in enumerate(spec):
        onde = p.get("slug") or f"peca {i}"
        for campo in ("slug", "conjunto", "form_id", "headline", "message", "cta"):
            if not p.get(campo):
                problemas.append(f"{onde}: falta `{campo}`")
        if not (p.get("image_hash") or p.get("image_url")):
            problemas.append(f"{onde}: precisa de `image_hash` ou `image_url`")
        for campo in PROIBIDOS:
            if campo in p:
                problemas.append(f"{onde}: `{campo}` nao passa por aqui — orcamento e do Pablo")
        if p.get("cta") and p["cta"] not in CTAS:
            problemas.append(f"{onde}: `cta` precisa ser um tipo da Meta "
                             f"({', '.join(CTAS)}), nao um rotulo")
        chave = (p.get("slug"), p.get("conjunto"))
        if chave in vistos:
            problemas.append(f"{onde}: repetido no mesmo conjunto")
        vistos.add(chave)
    return problemas


def anuncios_do_conjunto(conjunto, token):
    """Nome -> estado dos anuncios que ja existem no conjunto.

    Serve para nao criar duas vezes a mesma peca: rodar de novo com o mesmo
    spec nao pode encher o conjunto de copias. O nome e a chave porque e o que
    o spec controla; o id a Meta escolhe.
    """
    dados = _chamar(f"{conjunto}/ads?fields=name,effective_status&limit=200", token)
    return {a["name"]: a.get("effective_status") for a in dados.get("data", [])}


def criar_criativo(conta, peca, token):
    """Criativo com o formulario instantaneo grudado.

    `lead_gen_form_id` mora dentro de `call_to_action.value` — nao e campo de
    primeiro nivel, e e por isso que ferramenta que so aceita `image_hash` e
    `call_to_action_type` nunca consegue montar anuncio de lead.
    """
    link_data = {
        "link": f"https://fb.me/{peca['form_id']}",
        "name": peca["headline"],
        "message": peca["message"],
        "call_to_action": {
            # O `cta` do spec E o tipo da API, nao um rotulo solto. Na primeira
            # versao ele era exigido e nao era usado: o botao saia sempre
            # "Cadastre-se" enquanto o spec dizia outra coisa, e ninguem
            # perceberia sem abrir o anuncio. Campo que nao faz nada e pior
            # que campo que falta.
            "type": peca["cta"],
            "value": {"lead_gen_form_id": str(peca["form_id"])},
        },
    }
    if peca.get("image_hash"):
        link_data["image_hash"] = peca["image_hash"]
    else:
        link_data["picture"] = peca["image_url"]
    if peca.get("description"):
        link_data["description"] = peca["description"]

    spec = {"page_id": str(peca["page_id"]), "link_data": link_data}
    if peca.get("instagram_id"):
        spec["instagram_user_id"] = str(peca["instagram_id"])

    r = _chamar(f"act_{conta}/adcreatives", token, {
        "name": peca["slug"],
        "object_story_spec": json.dumps(spec, ensure_ascii=False),
    })
    return r["id"]


def criar_anuncio(conta, peca, criativo, token, ativar=False):
    return _chamar(f"act_{conta}/ads", token, {
        "name": peca["slug"],
        "adset_id": str(peca["conjunto"]),
        "creative": json.dumps({"creative_id": criativo}),
        "status": "ACTIVE" if ativar else "PAUSED",
    })["id"]


def pode_ativar(conjunto, token, entrando):
    """So liga se o conjunto ficar com MINIMO_ATIVOS entregando.

    `entrando` sao as pecas desta rodada. Conta junto porque ligar duas de uma
    vez e legitimo — o que nao vale e deixar o conjunto com uma so.
    """
    ativos = sum(1 for e in anuncios_do_conjunto(conjunto, token).values()
                 if e == "ACTIVE")
    return ativos + entrando >= MINIMO_ATIVOS


def publicar(conta, spec, token, ativar=False):
    problemas = conferir_spec(spec)
    if problemas:
        raise ValueError("spec reprovado:\n  " + "\n  ".join(problemas))

    por_conjunto = {}
    for p in spec:
        por_conjunto.setdefault(str(p["conjunto"]), []).append(p)

    linhas = []
    for conjunto, pecas in por_conjunto.items():
        existentes = anuncios_do_conjunto(conjunto, token)
        faltando = [p for p in pecas if p["slug"] not in existentes]
        for p in pecas:
            if p["slug"] in existentes:
                linhas.append(f"{p['slug']}: ja existe, nao mexi")

        liga = ativar and pode_ativar(conjunto, token, len(faltando))
        if ativar and not liga:
            linhas.append(f"conjunto {conjunto}: criado PAUSADO — "
                          f"ativar deixaria menos de {MINIMO_ATIVOS} anuncios entregando")
        for p in faltando:
            criativo = criar_criativo(conta, p, token)
            anuncio = criar_anuncio(conta, p, criativo, token, ativar=liga)
            linhas.append(f"{p['slug']}: {'ATIVO' if liga else 'pausado'} "
                          f"(anuncio {anuncio}, criativo {criativo})")
    return linhas


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    token = os.environ.get("META_ACCESS_TOKEN")
    if not token:
        print("Falta META_ACCESS_TOKEN no ambiente.", file=sys.stderr)
        return 1
    conta = os.environ.get("META_AD_ACCOUNT_ID", "1695865631502778")
    spec = json.load(open(argv[1], encoding="utf-8"))
    try:
        for linha in publicar(conta, spec, token, ativar="--ativar" in argv):
            print(linha)
    except (ErroMeta, ValueError) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
