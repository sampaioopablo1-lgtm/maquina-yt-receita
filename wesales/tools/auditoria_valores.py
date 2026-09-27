"""Audita o VALOR gravado nos campos contra a DEFINIÇÃO do campo. Só lê.

POR QUE ESTE ARQUIVO EXISTE
---------------------------
O projeto tem cinco auditorias e todas partem do dump ou da definição: conferem
que o campo existe, que a tag existe, que o nó aponta para o lugar certo.
**Nenhuma pergunta se o valor gravado num campo é um valor que aquele campo
aceita.** É exatamente onde estavam os seis defeitos achados em 27/09/2026:

    Investimento mensal em anúncios  19 de 22 valores fora da própria picklist
    Urgência (TEXT)                  recebendo resposta de budget em 4 leads
    Prazo (SINGLE_OPTIONS)           vazio nos 38, sendo o campo certo da pergunta
    Dor principal / Necessidade      a mesma pergunta em dois campos diferentes
    Nota de qualificação             ausente em todos, e é insumo da 9.2
    phone com 18 dígitos             ID de grupo do WhatsApp entrando como lead

Os seis sairiam de uma vez desta varredura, e ela roda de graça.

**Só lê.** Nenhum `PUT`, nenhum `POST`. Por isso pode rodar em cron sem linha no
`APROVADO.md`: aquele arquivo governa escrita, e aqui não há nenhuma. O código
de saída é a campainha — 0 não acorda ninguém, diferente de 0 sim.

OS CINCO ACHADOS QUE ELE PROCURA
--------------------------------
1. `fora-da-picklist` — valor num campo de opção que não está entre as opções.
   Todo `If/Else` que compare contra as opções falha calado para esse lead.
2. `tipo-errado` — texto onde o campo é NUMERICAL, data impossível onde é DATE.
3. `campo-morto` — campo definido que nenhum contato preenche. Ou ninguém usa,
   ou o mapeamento do formulário nunca dispara. `Prazo` é o caso real.
4. `campos-gemeos` — dois campos recebendo o mesmo conjunto de valores. Sinal de
   pergunta duplicada entre versões de formulário: filtrar por um vê metade da
   base. `Dor principal` x `Necessidade` é o caso real.
5. `telefone-improvavel` — `phone` com mais de 15 dígitos (E.164 não permite) ou
   com prefixo de JID de grupo do WhatsApp. Grupo não é lead.

LIMITE DECLARADO
----------------
Não foi executado contra a conta: todos os domínios do GHL respondem `000` pelo
proxy do contêiner onde foi escrito. As cinco funções de análise são puras e
estão cobertas por teste offline; o que não foi exercido é a leitura HTTP.
"""

import argparse
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://services.leadconnectorhq.com"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
PIPELINE_ID = "0Fo2xbeayE4EP6yuSUtq"
VERSION = "2021-07-28"

TIPOS_COM_OPCAO = ("SINGLE_OPTIONS", "RADIO", "CHECKBOX", "MULTIPLE_OPTIONS")
# Prefixo de JID de grupo do WhatsApp, visto na conta em 27/09/2026.
PREFIXO_GRUPO_WA = "120363"
MAX_DIGITOS_E164 = 15

ROOT = Path(__file__).resolve().parent.parent
PIT_FILE = ROOT / ".local" / "_ghl_pit.txt"


def read_token():
    # Deliberadamente nunca registrado nem incluído em exceção.
    token = os.environ.get("GHL_PIT", "").strip()
    if token:
        return token
    return PIT_FILE.read_text(encoding="utf-8").strip()


def request(path, token):
    headers = {"Authorization": "Bearer " + token, "Version": VERSION,
               "Accept": "application/json"}
    try:
        with urlopen(Request(BASE_URL + path, headers=headers, method="GET"),
                     timeout=30) as resposta:
            bruto = resposta.read()
            return json.loads(bruto.decode("utf-8")) if bruto else {}
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")[:300]
        if "1010" in detalhe or "cloudflare" in detalhe.lower():
            raise RuntimeError("GHL %d: Cloudflare barrou a assinatura do cliente "
                               "— rode do Action ou do PC" % erro.code) from None
        if erro.code == 401:
            raise RuntimeError("GHL 401: PIT inválido ou expirado") from None
        raise RuntimeError("GHL %d: %s" % (erro.code, detalhe)) from None
    except URLError as erro:
        raise RuntimeError("GHL erro de rede: %s" % erro.reason) from None


# ---------------------------------------------------------------- análise pura

def so_digitos(texto):
    return re.sub(r"\D", "", texto or "")


def checa_telefone(phone):
    """Achado 5. Devolve motivo ou None."""
    digitos = so_digitos(phone)
    if not digitos:
        return None
    if digitos.startswith(PREFIXO_GRUPO_WA):
        return "prefixo %s: é ID de grupo do WhatsApp, não telefone" % PREFIXO_GRUPO_WA
    if len(digitos) > MAX_DIGITOS_E164:
        return "%d dígitos; E.164 permite no máximo %d" % (len(digitos), MAX_DIGITOS_E164)
    return None


def e_numero(valor):
    try:
        float(valor)
        return True
    except (TypeError, ValueError):
        return False


def checa_valor(definicao, valor):
    """Achados 1 e 2. Devolve (tipo_do_achado, motivo) ou (None, None)."""
    if valor is None or valor == "" or valor == []:
        return None, None
    tipo = definicao.get("dataType")
    opcoes = definicao.get("picklistOptions") or definicao.get("options")

    if tipo in TIPOS_COM_OPCAO and opcoes:
        valores = valor if isinstance(valor, list) else [valor]
        fora = [str(v) for v in valores if str(v) not in [str(o) for o in opcoes]]
        if fora:
            return "fora-da-picklist", "%s — opções: %s" % (
                ", ".join(repr(f) for f in fora), ", ".join(map(str, opcoes)))
    if tipo == "NUMERICAL" and not e_numero(valor):
        return "tipo-errado", "campo NUMERICAL com %r" % valor
    if tipo == "DATE" and isinstance(valor, str) and valor.strip():
        if not re.match(r"^\d{4}-\d{2}-\d{2}|^\d{2}/\d{2}/\d{4}", valor.strip()):
            return "tipo-errado", "campo DATE com %r" % valor
    return None, None


def acha_campos_mortos(definicoes, preenchidos):
    """Achado 3: definido e nunca preenchido por ninguém."""
    return [d for d in definicoes if d["id"] not in preenchidos]


def acha_campos_gemeos(valores_por_campo, definicoes, minimo=2):
    """Achado 4: dois campos cujo conjunto de valores se sobrepõe.

    Só olha campos de texto/opção com pelo menos `minimo` valores distintos —
    campos numéricos coincidem por acidente (0, 1) e não querem dizer nada.
    """
    nomes = {d["id"]: d.get("name", d["id"]) for d in definicoes}
    tipos = {d["id"]: d.get("dataType") for d in definicoes}
    interessa = {cid: v for cid, v in valores_por_campo.items()
                 if tipos.get(cid) not in ("NUMERICAL", "DATE") and len(v) >= minimo}
    achados, ids = [], sorted(interessa)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            comum = interessa[a] & interessa[b]
            if len(comum) >= minimo:
                achados.append((nomes.get(a, a), nomes.get(b, b),
                                sorted(comum)[:4]))
    return achados


# ------------------------------------------------------------------- execução

def itens(dados, *chaves):
    if isinstance(dados, list):
        return dados
    for chave in chaves:
        valor = dados.get(chave) if isinstance(dados, dict) else None
        if isinstance(valor, list):
            return valor
    return []


def coleta(token, etapa=None):
    definicoes = itens(request("/locations/%s/customFields" % LOCATION_ID, token),
                       "customFields")
    consulta = {"location_id": LOCATION_ID, "pipeline_id": PIPELINE_ID,
                "limit": "100"}
    if etapa:
        consulta["pipeline_stage_id"] = etapa
    oportunidades = itens(request("/opportunities/search?" + urlencode(consulta), token),
                          "opportunities")
    vistos, contatos = set(), []
    for oportunidade in oportunidades:
        cid = oportunidade.get("contactId")
        if not cid or cid in vistos:
            continue
        vistos.add(cid)
        detalhe = request("/contacts/" + cid, token)
        contatos.append(detalhe.get("contact") or detalhe)
    return definicoes, contatos


def audita(definicoes, contatos):
    """Devolve a lista de achados. Pura: recebe dado, não busca nada."""
    por_id = {d["id"]: d for d in definicoes}
    achados = []
    preenchidos, valores_por_campo = set(), {}

    for contato in contatos:
        nome = contato.get("firstName") or contato.get("id") or "?"
        motivo = checa_telefone(contato.get("phone"))
        if motivo:
            achados.append(("telefone-improvavel", nome, "phone", motivo))
        for item in contato.get("customFields") or []:
            cid, valor = item.get("id"), item.get("value")
            if valor in (None, "", []):
                continue
            preenchidos.add(cid)
            valores_por_campo.setdefault(cid, set()).add(
                str(valor) if not isinstance(valor, list) else "|".join(map(str, valor)))
            definicao = por_id.get(cid)
            if not definicao:
                achados.append(("campo-desconhecido", nome, cid,
                                "valor gravado em campo que não está nas definições"))
                continue
            tipo, detalhe = checa_valor(definicao, valor)
            if tipo:
                achados.append((tipo, nome, definicao.get("name", cid), detalhe))

    for definicao in acha_campos_mortos(definicoes, preenchidos):
        achados.append(("campo-morto", "(base inteira)",
                        definicao.get("name", definicao["id"]),
                        "definido e nunca preenchido em %d contatos" % len(contatos)))
    for a, b, exemplos in acha_campos_gemeos(valores_por_campo, definicoes):
        achados.append(("campos-gemeos", "(base inteira)", "%s x %s" % (a, b),
                        "valores em comum: %s" % ", ".join(exemplos)))
    return achados


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--etapa", help="ID de etapa para restringir (opcional)")
    parser.add_argument("--json", action="store_true", help="saída em JSON")
    args = parser.parse_args()

    definicoes, contatos = coleta(read_token(), args.etapa)
    achados = audita(definicoes, contatos)

    if args.json:
        print(json.dumps([{"tipo": t, "quem": q, "campo": c, "detalhe": d}
                          for t, q, c, d in achados], ensure_ascii=False, indent=2))
    else:
        print("definições: %d · contatos lidos: %d · achados: %d"
              % (len(definicoes), len(contatos), len(achados)))
        porte = {}
        for tipo, _q, _c, _d in achados:
            porte[tipo] = porte.get(tipo, 0) + 1
        for tipo in sorted(porte):
            print("  %-22s %d" % (tipo, porte[tipo]))
        print()
        for tipo, quem, campo, detalhe in achados:
            print("[%s] %s · %s\n    %s" % (tipo, quem, campo, detalhe))

    # O código de saída é a campainha: vermelho passa a significar MUDOU.
    raise SystemExit(1 if achados else 0)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as erro:
        print("auditoria parou: " + str(erro))
        raise SystemExit(2)
