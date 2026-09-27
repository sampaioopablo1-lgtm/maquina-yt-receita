"""Acrescenta à picklist de `Investimento mensal em anúncios` as opções que o
formulário do Meta já grava e que o campo não tem.

O DEFEITO, medido em 27/09/2026 na subconta 1D53YTI9C7oIMBavcQxV
-----------------------------------------------------------------
`Investimento mensal em anúncios` (`bQithNwReQIBGlZBaNlI`) é `SINGLE_OPTIONS`
com quatro opções: `Até 1k`, `1k a 5k`, `5k a 10k`, `Acima de 10k`.

Os valores que os 38 contatos em `CONECTAR` realmente carregam são outros:

    Não invisto nada ainda   11 leads   <- fora da picklist
    Abaixo de 5k              5 leads   <- fora da picklist
    Até R$ 1.000              3 leads   <- fora da picklist
    Acima de 10k              3 leads   <- única que casa

Só 3 de 22 valores preenchidos casam com a picklist do próprio campo. Qualquer
`If/Else` de workflow ou filtro de lista inteligente que compare contra as
opções nunca casa para os outros 19 — e não falha em lugar nenhum, só deixa de
acontecer. É a mesma classe de bug silencioso que a §2.33 e a lista 8.17 já
pegaram sete vezes neste projeto, agora no dado em vez do nome da etapa.

POR QUE ACRESCENTAR, E NÃO REMAPEAR
-----------------------------------
São dois consertos possíveis e eles não são equivalentes:

1. **Acrescentar as opções** (o que este script faz). Reversível, não toca em
   nenhum dado de lead, e faz os portões voltarem a casar hoje. O preço é uma
   picklist com faixas que se sobrepõem (`Abaixo de 5k` cobre `Até 1k` e
   `1k a 5k`), que fica feia e tem que ser arrumada depois.
2. **Remapear o formulário do Meta e migrar os valores dos 22 leads.** Dado
   limpo no fim, mas reescreve o histórico de lead real e apaga a evidência do
   mapeamento errado — e o mapeamento é configurado na tela da integração, não
   aqui.

Para a abertura, o 1 é o certo: é o que não perde nada. O 2 fica para depois,
com o formulário na tela.

LIMITE DECLARADO — o caminho de escrita não foi testado contra o endpoint real
-----------------------------------------------------------------------------
Todos os domínios do GHL respondem `000` pelo proxy do contêiner onde este
arquivo foi escrito (conferido em 27/09/2026), então só o `--dump` foi exercido
de verdade. O `PUT` roda no Action (que tem rede e o secret `GHL_PIT`) ou no PC.
Rode sempre `--dump` primeiro e leia o corpo que sai antes de passar
`--aplicar`.

Assimetria de nome que este script trata de propósito: o `GET` devolve as
opções em `picklistOptions`, e o `PUT` as espera em `options`. Mandar
`picklistOptions` no `PUT` é aceito com 200 e não muda nada — falha silenciosa,
exatamente o que este arquivo existe para consertar.

USO
---
    python3 wesales/tools/patch_picklist_investimento.py --dump      # não escreve
    python3 wesales/tools/patch_picklist_investimento.py --aplicar   # escreve

Idempotente: opção que já existe não é duplicada, e sem nada a acrescentar ele
sai sem chamar o `PUT`.
"""

import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://services.leadconnectorhq.com"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
FIELD_ID = "bQithNwReQIBGlZBaNlI"
FIELD_NAME = "Investimento mensal em anúncios"
VERSION = "2021-07-28"

# Valores medidos nos 38 contatos de CONECTAR em 27/09/2026 que o campo grava e
# a picklist não tem. Não inventar: só entra aqui o que foi visto na conta.
OPCOES_FALTANDO = [
    "Não invisto nada ainda",
    "Abaixo de 5k",
    "Até R$ 1.000",
]

ROOT = Path(__file__).resolve().parent.parent
PIT_FILE = ROOT / ".local" / "_ghl_pit.txt"


def read_token():
    # Deliberadamente nunca registrado nem incluído em exceção.
    token = os.environ.get("GHL_PIT", "").strip()
    if token:
        return token
    return PIT_FILE.read_text(encoding="utf-8").strip()


def request(method, path, token, body=None):
    payload = None if body is None else json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + token,
        "Version": VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        with urlopen(Request(BASE_URL + path, data=payload, headers=headers,
                             method=method), timeout=30) as response:
            raw = response.read()
            return response.status, (json.loads(raw.decode("utf-8")) if raw else {})
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:300]
        # Ler o corpo antes de concluir a causa: em 27/09/2026 um 403 do
        # Cloudflare (1010, assinatura do cliente) foi diagnosticado como token
        # inválido sem base. O corpo separa os dois casos.
        if "1010" in detail or "cloudflare" in detail.lower():
            raise RuntimeError(
                "GHL %d: bloqueio de Cloudflare pela assinatura do cliente, "
                "não é o token — rode do Action ou do PC" % error.code) from None
        if error.code == 401:
            raise RuntimeError("GHL 401: PIT inválido ou expirado") from None
        if error.code == 403:
            raise RuntimeError(
                "GHL 403: confira os escopos do PIT "
                "(locations/customFields.readonly e .write)") from None
        if error.code == 429:
            raise RuntimeError("GHL 429: excesso de chamadas, tentar depois") from None
        raise RuntimeError("GHL %d: %s" % (error.code, detail)) from None
    except URLError as error:
        raise RuntimeError("GHL erro de rede: %s" % error.reason) from None


def campo_atual(token):
    _, data = request("GET", "/locations/%s/customFields/%s" % (LOCATION_ID, FIELD_ID),
                      token)
    campo = data.get("customField") or data.get("customFields") or data
    if isinstance(campo, list):
        campo = campo[0] if campo else {}
    return campo


def opcoes_de(campo):
    """O GET devolve `picklistOptions`; aceitar `options` também, por segurança."""
    for chave in ("picklistOptions", "options"):
        valor = campo.get(chave)
        if isinstance(valor, list):
            return [str(item) for item in valor]
    return []


def uniao(atuais, faltando):
    """Preserva a ordem das atuais e acrescenta só o que não está lá."""
    resultado = list(atuais)
    for opcao in faltando:
        if opcao not in resultado:
            resultado.append(opcao)
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--dump", action="store_true",
                       help="lê o campo e imprime o PUT que sairia, sem escrever")
    grupo.add_argument("--aplicar", action="store_true",
                       help="escreve as opções que faltam na picklist")
    args = parser.parse_args()

    token = read_token()
    campo = campo_atual(token)
    atuais = opcoes_de(campo)
    if not atuais:
        raise RuntimeError(
            "campo %s voltou sem picklist — confira o ID antes de escrever" % FIELD_ID)

    print("campo: %s (%s)" % (campo.get("name", FIELD_NAME), FIELD_ID))
    print("opções hoje:   %s" % atuais)
    novas = uniao(atuais, OPCOES_FALTANDO)
    acrescentar = [o for o in novas if o not in atuais]
    if not acrescentar:
        print("nada a acrescentar; picklist já cobre os valores medidos")
        return
    print("a acrescentar: %s" % acrescentar)
    print("opções depois: %s" % novas)

    # `options`, não `picklistOptions` — ver a nota de assimetria no topo.
    body = {"name": campo.get("name") or FIELD_NAME, "options": novas}

    if args.dump:
        print("\nPUT /locations/%s/customFields/%s" % (LOCATION_ID, FIELD_ID))
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print("\n--dump: nada foi escrito")
        return

    request("PUT", "/locations/%s/customFields/%s" % (LOCATION_ID, FIELD_ID),
            token, body)
    conferido = opcoes_de(campo_atual(token))
    faltou = [o for o in OPCOES_FALTANDO if o not in conferido]
    if faltou:
        raise RuntimeError(
            "PUT devolveu 200 mas a picklist não mudou; ainda falta %s "
            "(suspeita: a chave do corpo) " % faltou)
    print("aplicado e conferido; picklist agora: %s" % conferido)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("parou sem aplicar: " + str(error))
        raise SystemExit(1)
