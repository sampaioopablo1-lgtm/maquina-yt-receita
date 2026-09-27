#!/usr/bin/env python3
"""Cria as pastas de campo do CRM e imprime o mapa de arrasto, medido.

O PROBLEMA QUE ISTO ATACA
-------------------------
53 dos 56 campos personalizados estao numa pasta unica (`gabsbU3jsUN7oIXCnYab`). O
SDR abre o contato e ve tudo em bloco, quando ele preenche **um** campo por tentativa
(`Resultado da tentativa`). E a origem literal da queixa do dono: "meio completo e
confuso".

RETRATACAO DE 27/09 15:16 — NADA DISTO SAI POR API. MEDIDO, NAO SUPOSTO.
------------------------------------------------------------------------
Este arquivo nasceu prometendo que criar pasta saia por API publica, porque as
ROTAS existem no spec oficial. Rodei na Action, com o PIT valido, e a conta
respondeu:

    GET  /custom-fields/object-key/contact   -> HTTP 400
    POST /custom-fields/folder objectKey=contact -> HTTP 400
    {"message":"Api does not support objectKey of type contact or opportunity"}

O grupo `/custom-fields/` da API v2 e para **objeto personalizado**, nao para os
campos do contato. Entao pasta de campo de contato **nao se cria, nao se renomeia
e nao se lista** por API publica. O truque de renomear a pasta grande para
economizar 29 arrastos morreu com o resto: o PUT de renome e do mesmo grupo.

    POST /custom-fields/folder      criar pasta          -> NAO (400 em contact)
    PUT  /custom-fields/folder/{id} renomear pasta       -> NAO (mesmo grupo)
    PUT  /custom-fields/{id}        MOVER campo existente-> NAO (corpo sem parentId)

**Terceira correcao minha no mesmo assunto, e a mais funda.** A primeira foi
anunciar antes de ler o `requestBody` (licao 2.12). Esta e: rota existir e corpo
ter o campo ainda nao e capacidade — **o servidor tem de aceitar o objectKey**, e
o spec nao diz quais valores de enum ele honra. Licao 2.19.

O QUE SOBRA DESTE ARQUIVO
-------------------------
So o mapa. `--plano` segue valendo como **especificacao do arrasto na tela**: os
56 campos agrupados, conferidos contra o snapshot da conta, na ordem que mais
reduz confusao por movimento. Criar as 5 pastas e arrastar os 56 campos e tela,
inteiro, sem atalho.

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

METADE DO ARRASTO SAI DE GRACA — RENOMEANDO, NAO MOVENDO
--------------------------------------------------------
Mover campo nao sai por API, mas **renomear pasta sai** (`PUT /custom-fields/folder/{id}`,
corpo `{name, locationId}` — conferido no spec, nao suposto).

E a pasta unica `gabsbU3jsUN7oIXCnYab` ja contem **29 dos 30 campos que a maquina
escreve**. Entao a pasta 5 nao precisa ser criada e povoada: ela **e** essa pasta, com
outro nome. Os 29 campos ficam exatamente onde estao, e zero arrasto.

    sem renomear: 56 arrastos
    renomeando:   27 arrastos   <- 3 + 17 + 3 + 3, mais `Conexoes WhatsApp` sozinho

O unico campo da maquina fora dela e `Conexoes WhatsApp` (`vCqedGd185RiQKNlU870`).

Este script **nao apaga pasta nenhuma**, inclusive as duas pequenas que sobram
(`zHU4yGXKHdxBHnGxUmai` com `Urgencia` e `Empresa`, e a do `Conexoes WhatsApp`): elas
ficam vazias depois do arrasto, e pasta vazia nao machuca ninguem. Apagar exigiria o
verbo que a regra 1 proibe.

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

# A pasta unica onde moram 53 dos 56 campos — a causa do "meio completo e confuso".
PASTA_GRANDE = "gabsbU3jsUN7oIXCnYab"

# A ordem e a de quem abre o contato: o que a SDR faz agora primeiro, o que a maquina
# escreve por ultimo. O numero no nome fixa a ordem na tela do GHL.
# A pasta 5 nao e criada: e a PASTA_GRANDE renomeada. Ver METADE DO ARRASTO, acima.
PASTA_MAQUINA = "5 · NAO MEXER — a maquina escreve"

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
    """Renomeia a pasta grande e cria as outras quatro. Idempotente.

    Idempotente de duas formas, porque sao duas operacoes diferentes: as quatro novas
    sao comparadas por nome antes de criar, e o rename so acontece se a pasta grande
    ainda nao se chamar PASTA_MAQUINA.
    """
    existentes = pastas_existentes()
    print("pastas que já existem: %s" % (sorted(existentes) or "nenhuma"))

    # 1) A pasta 5 e a grande renomeada — 29 dos 30 campos da maquina ja estao nela.
    atual = {v: k for k, v in existentes.items()}.get(PASTA_GRANDE)
    if atual == PASTA_MAQUINA:
        print("  = %-38s já é a pasta grande (%s)" % (PASTA_MAQUINA, PASTA_GRANDE))
    else:
        pedir("PUT", "/custom-fields/folder/%s" % PASTA_GRANDE,
              {"name": PASTA_MAQUINA, "locationId": LOC})
        print("  ~ pasta grande %s renomeada" % PASTA_GRANDE)
        print("      de:   %s" % (atual if atual else "(nome anterior não lido)"))
        print("      para: %s" % PASTA_MAQUINA)
        print("      29 campos da máquina ficaram onde estão — zero arrasto.")
        existentes[PASTA_MAQUINA] = PASTA_GRANDE

    # 2) As outras quatro nascem vazias e o arrasto as enche.
    for nome in PASTAS:
        if nome == PASTA_MAQUINA:
            continue
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
    campos_snap = snapshot()["campos"]
    cheios = {c["nome"]: c["preenchidos"] for c in campos_snap}
    onde = {c["nome"]: c["pastaAtual"] for c in campos_snap}
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
    total = 0
    for i, nome in enumerate(PASTAS, 1):
        campos = MAPA.get(nome) or []
        alvo = (" -> id %s" % pastas[nome]) if pastas and pastas.get(nome) else ""
        # Na pasta da maquina, campo que ja esta na pasta grande nao se arrasta:
        # a pasta grande E essa pasta, renomeada.
        mover = [c for c in campos
                 if not (nome == PASTA_MAQUINA and onde.get(c) == PASTA_GRANDE)]
        total += len(mover)
        print()
        print("%d) %s  (%d campos, %d a arrastar)%s"
              % (i, nome, len(campos), len(mover), alvo))
        if nome == PASTA_MAQUINA:
            print("      esta pasta É a pasta grande renomeada: %d dos %d campos"
                  % (len(campos) - len(mover), len(campos)))
            print("      já estão dentro dela e NÃO se arrastam.")
        for c in mover:
            print("      %3d/64  %s" % (cheios.get(c, 0), c))
    print()
    print("total a arrastar: %d   (seriam 56 sem renomear a pasta grande)" % total)


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
        print("--criar RETIRADO em 27/09. A API publica recusa objectKey=contact:")
        print('  {"message":"Api does not support objectKey of type contact or')
        print('   opportunity","error":"Bad Request","statusCode":400}')
        print("Medido na Action com PIT valido, no GET e no POST. Criar pasta de")
        print("campo de contato e tela. O mapa abaixo e a especificacao do arrasto.")
        plano()
        return 2
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
