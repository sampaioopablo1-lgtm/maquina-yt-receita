#!/usr/bin/env python3
"""Teste minimo do Jev: uma chamada, um fio real, zero dependencia e zero CRM.

Prova de vida do Jev antes de confiar nele para qualquer coisa. Usa o fio que
motivou tudo: em 23/09/2026 21:54 o dono falava com o SUPORTE da WeSales e a
`Porta de Entrada` transformou a atendente (`Rafaela de Paula - We Sales`) em
oportunidade aberta em `NOVO LEAD`, com `cad-inbound` e dono atribuido. Se o Jev
responder `suporte_ou_fornecedor`, ele resolve sozinho o filtro que o `G-16`
declarou impossivel para um workflow.

Nao le a conta, nao escreve nada, nao precisa do `GHL_PIT`. So a chave do Jev.

  OPENCODE_API_KEY   (ou TYPESAFE_API_KEY / OPENROUTER_API_KEY / AI_GATEWAY_API_KEY)

Uso:  python3 jev_teste_minimo.py
"""
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROVEDORES = [
    ("OPENCODE_API_KEY", "https://opencode.ai/zen/v1/systemone", "jev-1.13-free"),
    ("TYPESAFE_API_KEY", "https://api.typesafe.ai/v1/systemone", "jev-latest"),
    ("OPENROUTER_API_KEY", "https://openrouter.ai/api/alpha/decisions", "typesafe/jev-1.13"),
    ("AI_GATEWAY_API_KEY", "https://ai-gateway.vercel.sh/typesafe/v1/systemone", "typesafe-ai/jev"),
]

# Cloudflare recusa o User-Agent padrao do `urllib` ("Python-urllib/3.x") com
# erro 1010 — "banned based on your browser's signature". Medido em 27/09/2026:
# a primeira rodada no GitHub Action levou 403/1010 antes de chegar na chave.
UA = "wesales-jev/1.0 (+https://github.com/sampaioopablo1-lgtm/maquina-yt-receita)"

# Tres fios reais da subconta, com o que se espera de cada um. O terceiro e um
# lead de verdade, para o teste nao medir so o lado negativo.
CASOS = [
    ("Rafaela de Paula - We Sales", "suporte_ou_fornecedor", [
        "Nao estou tendo certo, sucesso com o suporte. Pode me ajudar?",
        "Comprei o numero telefonico",
        "E tambem sobre 20 dias a mais do teste, nao habilitou",
        "Se poder checar"]),
    ("Francisca", "pessoal", [
        "Oi Pablo, boa noite",
        "Te lembrando do pix",
        "E mais uma vez obrigado pela carona",
        "Salvou rs"]),
    ("Andre (lead do anuncio)", "lead_comercial", [
        "Vi o anuncio de voces",
        "Ja faco anuncios e quero melhorar meus resultados",
        "Preciso pra ontem, quanto custa?"]),
]

CRITERIOS = {
    "lead_comercial": ("Nao conhece o dono pessoalmente e demonstra interesse comercial: pergunta "
                       "sobre servico, preco, anuncios, resultados. Veio de anuncio ou indicacao."),
    "pessoal": ("Conversa da vida pessoal do dono: familia, amigos, pix, carona, assunto "
                "domestico. Chama o dono pelo nome com familiaridade e nao menciona negocio."),
    "suporte_ou_fornecedor": ("Suporte ou vendedor de plataforma/servico que o dono USA ou "
                              "contratou: fala de conta, plano, numero comprado, teste, fatura. "
                              "O dono e o cliente aqui, nao o vendedor."),
    "indeterminado": "Curto, vazio ou ambiguo demais para decidir.",
}


def provedor():
    for var, url, modelo in PROVEDORES:
        chave = os.environ.get(var, "").strip()
        if chave:
            return var, url, os.environ.get("JEV_MODEL", "").strip() or modelo, chave
    return None, None, None, None


def pergunta(url, modelo, chave, nome, mensagens):
    corpo = {"model": modelo,
             "state": {"nome_no_crm": nome,
                       "primeiras_mensagens": [{"de": "lead", "texto": m} for m in mensagens]},
             "questions": {"classe": {
                 "type": "choice",
                 "instructions": ("Este fio chegou ao WhatsApp comercial de uma agencia de trafego "
                                  "pago. Quem escreveu e um prospect, ou outra coisa?"),
                 "criteria": CRITERIOS}}}
    req = Request(url, data=json.dumps(corpo).encode(),
                  headers={"Authorization": "Bearer " + chave,
                           "Content-Type": "application/json",
                           "http-referer": "https://github.com/sampaioopablo1-lgtm/maquina-yt-receita",
                           "user-agent": UA,
                           "x-title": "wesales-jev-teste"}, method="POST")
    with urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode() or "{}")


def leia(r):
    """(escolha, confianca) tolerando variacao de envelope entre provedores."""
    for nivel in (r.get("answers"), r.get("results"), r):
        if isinstance(nivel, dict) and "classe" in nivel:
            a = nivel["classe"] or {}
            return (a.get("choice") if a.get("choice") is not None else a.get("value"),
                    a.get("confidence"))
    return None, None


def main():
    var, url, modelo, chave = provedor()
    if not chave:
        print("sem chave: defina %s" % " ou ".join(v for v, _, _ in PROVEDORES))
        return 2
    print("Jev via %s — %s — modelo %s\n" % (var, url, modelo))
    print("%-28s %-22s %-22s %5s  %s" % ("fio", "esperado", "Jev respondeu", "conf", "ok?"))
    print("-" * 88)
    acertos = 0
    for nome, esperado, msgs in CASOS:
        try:
            classe, conf = leia(pergunta(url, modelo, chave, nome, msgs))
        except HTTPError as e:
            print("%-28s HTTP %s: %s" % (nome[:28], e.code,
                                         (e.read() or b"")[:160].decode("utf-8", "replace")))
            return 1
        except URLError as e:
            print("rede indisponivel: %s" % e.reason)
            return 1
        ok = (classe == esperado)
        acertos += ok
        print("%-28s %-22s %-22s %5s  %s" % (
            nome[:28], esperado, classe,
            ("%.2f" % conf) if isinstance(conf, (int, float)) else "-", "SIM" if ok else "NAO"))
    print("\n%d de %d" % (acertos, len(CASOS)))
    print("Nada foi lido nem escrito no CRM.")
    return 0 if acertos == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main())
