#!/usr/bin/env python3
"""Cria as pastas de campo do CRM e imprime o mapa de arrasto, medido.

O PROBLEMA QUE ISTO ATACA
-------------------------
53 dos 56 campos personalizados estao numa pasta unica (`gabsbU3jsUN7oIXCnYab`). O
SDR abre o contato e ve tudo em bloco, quando ele preenche **um** campo por tentativa
(`Resultado da tentativa`). E a origem literal da queixa do dono: "meio completo e
confuso".

O QUE DA E O QUE NAO DA, conferido no spec oficial (GoHighLevel/highlevel-api-docs)
-----------------------------------------------------------------------------------
    POST /custom-fields/folder      criar pasta          -> SIM
    PUT  /custom-fields/folder/{id} renomear pasta       -> SIM
    POST /custom-fields/            campo NOVO em pasta  -> SIM (aceita parentId)
    PUT  /custom-fields/{id}        MOVER campo existente-> **NAO**: o corpo nao tem
                                                            parentId

Ou seja: este script faz a parte automatizavel (as pastas) e **nao consegue mover os
campos** — nao por falta de permissao, e porque o endpoint nao existe. Mover fica na
tela, e o script existe para que a parte de tela seja a menor e mais eficaz possivel.

Registrado porque eu errei nisso: anunciei ao dono que o reagrupamento inteiro saia
por API depois de ver as duas primeiras rotas, antes de ler o `requestBody` do PUT.
Entrada 2.12 do `LICOES-DO-PROJETO.md`.

POR QUE O MAPA MUDOU EM 27/09 — E A MEDICAO QUE MUDOU
-----------------------------------------------------
A §4 do `USABILIDADE.md` tinha uma pasta `4 · VEIO DO ANUNCIO` com 20 campos: todo o
BANT (`Budget`, `Decisor`, `Prazo`, `Tem time comercial`...). O dono corrigiu o
entendimento: **sao dois formularios diferentes**. O do Meta Ads traz o lead; o de
qualificacao e preenchido **pela SDR** para marcar a reuniao com o closer, e os campos
entram no lead ao longo do processo.

Medi, em vez de supor. Contagem de preenchimento nos 64 contatos da conta
(`wesales/dados/campos-27-09.json`):

    Urgencia ............................ 40/64   <- vem do anuncio
    Necessidade ......................... 34/64   <- vem do anuncio
    Investimento mensal em anuncios ..... 32/64   <- vem do anuncio
    ---------------------------------------------
    Dor principal ....................... 6/64
    Budget / Decisor / Prazo ............ 3/64
    Segmento, Site, Instagram, Usa CRM .. 0/64

A separacao e limpa: **tres campos** chegam com o lead, e os outros 17 do bloco antigo
ficam entre 0 e 6 — sao preenchidos depois, a mao. Se viessem do formulario do anuncio,
os 64 teriam. Entao a pasta `VEIO DO ANUNCIO` tem 3 campos, e o BANT ganhou pasta
propria: `SDR PREENCHE NA QUALIFICACAO`.

Isso nao e cosmetico. Chamar de "veio do anuncio" um campo que a SDR precisa preencher
esconde trabalho dela na tela — o campo vazio pareceria dado que o anuncio nao mandou,
em vez de pergunta que falta fazer.

NUNCA APAGA NADA
----------------
O grupo `/custom-fields/` tem `DELETE` de campo e de pasta. **Este arquivo nao contem
o verbo**, de proposito: a regra 1 do projeto proibe excluir, e apagar campo levaria o
dado de todos os contatos com ele. Nao e questao de nao chamar; e de nao existir o
caminho.

ONDE RODA
---------
A API publica e `services.leadconnectorhq.com`, que o proxy deste conteiner nega.
Roda na Action `wesales-pastas.yml`, que tem rede e o segredo `GHL_PIT` — o mesmo
padrao de outras seis Actions deste repositorio.

USO
---
    python3 pastas_de_campo.py --plano     # offline: confere o mapa e imprime o arrasto
    python3 pastas_de_campo.py --criar     # cria as pastas que faltam (idempotente)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://services.leadconnectorhq.com"
LOC = "1D53YTI9C7oIMBavcQxV"
VERSION = "2021-07-28"
OBJECT_KEY = "contact"

AQUI = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(AQUI, "..", "dados", "campos-27-09.json")

# A ordem e a de quem abre o contato: o que a SDR faz agora primeiro, o que a maquina
# escreve por ultimo. O numero no nome fixa a ordem na tela do GHL.
PASTAS = [
    "1 · SDR PREENCHE A CADA TENTATIVA",
    "2 · SDR PREENCHE NA QUALIFICACAO",
    "3 · VEIO DO ANUNCIO",
    "4 · CLOSER PREENCHE",
    "5 · NAO MEXER — a maquina escreve",
]

# Mapa campo -> pasta, pelos NOMES que `locations_get-custom-fields` devolve.
# Cada bloco esta justificado pela medicao no docstring.
MAPA = {
    # O que a SDR toca a cada ligacao. Tres campos: e o dia dela.
    "1 · SDR PREENCHE A CADA TENTATIVA": [
        "Resultado da tentativa",
        "Data de retorno",
        "Hora do retorno",
    ],
    # O formulario de qualificacao — o que a SDR pergunta para marcar com o closer.
    # Preenchimento medido: 0 a 6 de 64. Nao vem do anuncio.
    "2 · SDR PREENCHE NA QUALIFICACAO": [
        "Budget", "Decisor", "Prazo", "Dor principal",
        "Tem time comercial", "Clientes novos por mês", "Quem atende os leads",
        "Canal principal de venda", "Usa CRM", "Investe em anúncios",
        "Plataformas de anúncio", "Já teve agência?", "Experiência com agência",
        "Segmento", "Site", "Instagram", "Empresa",
    ],
    # So o que o formulario do Meta Ads realmente entrega. Medido: 32 a 40 de 64.
    "3 · VEIO DO ANUNCIO": [
        "Urgência",
        "Necessidade",
        "Investimento mensal em anúncios",
    ],
    "4 · CLOSER PREENCHE": [
        "Reunião foi qualificada",
        "Motivo da desqualificação",
        "Data do veredito do closer",
    ],
    # O nome desta pasta e metade do valor dela: quem "ajuda" a automacao a mao quebra
    # a contagem e o roteamento sem ver erro nenhum.
    "5 · NAO MEXER — a maquina escreve": [
        "Prioridade", "Tentativa nº", "Entrada em", "1ª tentativa em",
        "Checkpoint — Tentativa nº", "Checkpoint — Data de retorno",
        "Toques na semana", "Total de ligações", "Total de conexões",
        "Tentativas telefone", "Conexões telefone", "Tentativas WhatsApp",
        "Conexões WhatsApp", "Conexões reais telefone", "Duração da ligação",
        "Ligações com transcrição", "Conexão real", "Canal que conectou",
        "WA não atendidas seguidas", "Template usado", "Nota de qualificação",
        "Sinal recebido", "Data e hora do sinal", "Data conectado",
        "Data agendado", "Data compareceu", "Nº de no-shows",
        "Hora da conexão", "Permissão WhatsApp", "Qualificação",
    ],
}


def snapshot() -> dict:
    with open(SNAPSHOT, encoding="utf-8") as fh:
        return json.load(fh)


def conferir() -> list:
    """Confere o MAPA contra o snapshot da conta. Offline, roda em qualquer lugar.

    Existe porque um mapa escrito a mao erra silenciosamente: campo com nome trocado
    nunca aparece no arrasto, e campo novo na conta fica de fora sem avisar.
    """
    problemas = []
    campos = {c["nome"] for c in snapshot()["campos"]}
    mapeados = [n for v in MAPA.values() for n in v]
    if len(mapeados) != len(set(mapeados)):
        vistos, repetidos = set(), set()
        for n in mapeados:
            (repetidos if n in vistos else vistos).add(n)
        problemas.append("campo em duas pastas: %s" % sorted(repetidos))
    for n in sorted(set(mapeados) - campos):
        problemas.append("no MAPA mas nao existe na conta: %r" % n)
    for n in sorted(campos - set(mapeados)):
        problemas.append("existe na conta mas ficou fora do MAPA: %r" % n)
    for p in MAPA:
        if p not in PASTAS:
            problemas.append("pasta do MAPA fora de PASTAS: %r" % p)
    return problemas


def token() -> str:
    t = (os.environ.get("GHL_PIT") or "").strip()
    if not t:
        raise SystemExit("sem GHL_PIT no ambiente — este script roda na Action.")
    return t


def pedir(metodo: str, caminho: str, corpo: dict | None = None):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(BASE + caminho, data=dados, method=metodo)
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("Version", VERSION)
    req.add_header("Accept", "application/json")
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            detalhe = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        raise SystemExit("%s %s -> HTTP %s %s" % (metodo, caminho, e.code, detalhe))
    except urllib.error.URLError as e:
        raise SystemExit(
            "%s %s -> rede recusou: %s. A API publica e negada pelo proxy do "
            "conteiner; rode pela Action." % (metodo, caminho, e.reason))


def pastas_existentes() -> dict:
    """Le as pastas ja criadas, pelo nome.

    O `GET /custom-fields/object-key/{objectKey}` devolve DUAS listas, `fields` e
    `folders` (conferido no spec). A primeira versao deste script lia so `fields` e
    procurava pasta la dentro — nao acharia nenhuma, e criaria as cinco de novo a cada
    execucao. O conector MCP tambem so devolve `fields`, o que escondia o erro.
    """
    r = pedir("GET", "/custom-fields/object-key/%s?locationId=%s" % (OBJECT_KEY, LOC))
    pastas = (r or {}).get("folders") or []
    return {p.get("name"): p.get("id") for p in pastas if p.get("name")}


def criar_pastas() -> dict:
    """Cria as pastas que faltam. Idempotente: compara por nome antes."""
    existentes = pastas_existentes()
    print("pastas que já existem: %s" % (sorted(existentes) or "nenhuma"))
    for nome in PASTAS:
        if nome in existentes:
            print("  = %-38s já existe (%s)" % (nome, existentes[nome]))
            continue
        r = pedir("POST", "/custom-fields/folder",
                  {"objectKey": OBJECT_KEY, "name": nome, "locationId": LOC})
        novo = (r.get("folder") or r).get("id") if isinstance(r, dict) else None
        existentes[nome] = novo
        print("  + %-38s criada (%s)" % (nome, novo))
    return existentes


def plano(pastas: dict | None = None) -> None:
    """Imprime o mapa de arrasto, agrupado e na ordem de maior alívio primeiro."""
    cheios = {c["nome"]: c["preenchidos"] for c in snapshot()["campos"]}
    print()
    print("=" * 74)
    print("MAPA DE ARRASTO — o que a tela ainda precisa fazer")
    print("=" * 74)
    print("O `PUT /custom-fields/{id}` NAO aceita parentId, entao mover campo")
    print("existente nao sai por API. O numero ao lado de cada campo e quantos")
    print("dos 64 contatos o tem preenchido — foi o que separou o que vem do")
    print("anuncio do que a SDR ainda precisa perguntar.")
    print()
    print("Comece pela pasta 1: sao 3 campos e e o que a SDR toca a cada ligacao.")
    print("Se parar depois dela, o dia da SDR ja fica limpo.")
    for i, nome in enumerate(PASTAS, 1):
        campos = MAPA.get(nome) or []
        alvo = (" -> id %s" % pastas[nome]) if pastas and pastas.get(nome) else ""
        print()
        print("%d) %s  (%d campos)%s" % (i, nome, len(campos), alvo))
        for c in campos:
            print("      %3d/64  %s" % (cheios.get(c, 0), c))
    print()
    print("total de campos a mover: %d" % sum(len(v) for v in MAPA.values()))


def main() -> int:
    problemas = conferir()
    if problemas:
        print("MAPA nao fecha com a conta — nao sigo:")
        for p in problemas:
            print("  - %s" % p)
        return 1
    if "--plano" in sys.argv:
        plano()
        return 0
    if "--criar" in sys.argv:
        plano(criar_pastas())
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
