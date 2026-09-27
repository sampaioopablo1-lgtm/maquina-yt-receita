"""Recalcula `Prioridade` na etapa CONECTAR — a fila do SDR numa tela só.

Implementa a **seção 9.2 do `build-wesales.md`** (a regra canônica, 8 condições
ordenadas, primeira que casa ganha), mais duas extensões declaradas no fim. Foi
escrito depois de rever os dumps dos workflows publicados, e a revisão mudou o
desenho: a primeira versão deste arquivo inventava uma régua própria e teria
brigado com o que já está no ar.

O QUE A REVISÃO DOS WORKFLOWS MOSTROU (27/09/2026)
--------------------------------------------------
Seis workflows publicados já escrevem `Prioridade`, com estes valores:

    Cadência Inbound ......... 5 na entrada
    Cadência 12x30 ........... 3 na entrada
    Interceptação (clique) ... 5
    Interceptação (resposta) . 5
    Pós-ligação v2 ........... 5 (dois ramos)
    Pós-agendamento v2 ....... 6 e 5

Ou seja: a escala real vai até **6**, e 6 significa *agendado* — acima do
"1 a 5" que a seção 9.2 declara. Este runner **nunca sobrescreve 6**.

O DEFEITO QUE ISSO CONSERTA
---------------------------
`Prioridade` vale **5 em todos os leads** da etapa: conferido em 37 contatos,
incluindo quatro lidos sem nenhuma escrita (Gerson, Ana Ruth, Ricardo, Carlos
Andrade). O campo é estampado na entrada e nunca recalculado. Com tudo em 5, a lista
"Fila Quente" devolve a base inteira e ordenar por `Prioridade` dá ordem
arbitrária: o SDR não tem por onde começar.

**O que este runner é, com precisão:** um reconciliador, não um priorizador
paralelo. A 9.2 manda recalcular em 4 momentos, todos por evento (entrada,
Pós-ligação, saída da IA, reativação) — e o envelhecimento por `Tentativa nº`
já vem de graça aí. O que não existe é alguém conferindo se o campo **de fato**
corresponde à regra: hoje 37 leads estão em 5 quando a regra 5 manda 4. Este
arquivo percorre a etapa e corrige a divergência, que é operação sobre conjunto
e workflow do GHL não faz. Some-se a isso a extensão 1, que é a única coisa
aqui que nenhum workflow cobre de jeito nenhum.

`Nota de qualificação` está **ausente em todos**, e a escala dela é **0 a 100**
(faixas 70+/45-69/25-44/0-24 da seção 9.1), não 0 a 10. A régua abaixo usa a
nota quando existe e cai para `Tentativa nº` quando não.

POR QUE CAMPO, E NÃO UMA TAG DIÁRIA
-----------------------------------
Tag é booleano que alguém tem de pôr **e tirar**: em 300 leads são ~600 escritas
por dia, e todo lead cuja remoção falha fica com a tag de ontem — o SDR liga
para quem não devia e para de confiar na lista. Campo numérico é sobrescrito:
uma escrita, sem estado residual. E as listas da seção 8 já ordenam por
`Prioridade` desc, então o valor certo no campo basta, sem tag nova.

DUAS EXTENSÕES À SEÇÃO 9.2, DECLARADAS
--------------------------------------
1. **`Prioridade` 0 para quem não deve aparecer na fila** (DND, `nao-perturbe`,
   `pausado`). A 9.2 não prevê isso e a escala dela começa em 1. É o furo medido
   em 27/09: os 30 leads travados para a rampa estão com DND e aparecem na fila
   com 5, porque **nem o DND nem a tag `nao-perturbe` param a execução da
   cadência** (medido no contato `lF8IdciftoNdPaLTLgE6`: aos 15 min a máquina
   escreveu `Prioridade` 5 e `atraso-1a-tentativa` com as duas proteções
   ligadas). Como as listas ordenam desc, 0 os joga para o fim sem quebrar
   filtro nenhum.
2. **Nunca sobrescreve 6**, o valor de agendado do Pós-agendamento.

DOIS DEFEITOS DA PRÓPRIA 9.2 QUE ESTE ARQUIVO NÃO CONSERTA, SÓ DENUNCIA
-----------------------------------------------------------------------
Reproduzo a ordem da 9.2 como está, e o `--dump` marca os casos:

- **A regra 8 está no fim.** `telefone-invalido` deveria tirar o lead da fila,
  mas a regra 5 (`Tentativa nº` <= 2 -> 4) casa antes dela. Um lead com telefone
  inválido e nenhuma tentativa recebe prioridade **4**. Sai marcado como
  `[9.2-r8-perdeu]`.
- **Há um furo de cobertura.** `Tentativa nº` >= 8 **com** `Total de conexões`
  > 0 não casa em nenhuma das 8 regras. Nesses casos este runner **não escreve
  nada** e marca `[9.2-sem-regra]`, em vez de inventar valor.

LIMITE DECLARADO
----------------
O caminho de escrita não foi testado contra o endpoint real: todos os domínios
do GHL respondem `000` pelo proxy do contêiner onde isto foi escrito. A função
`prioridade()` é pura e está coberta por teste offline. Rode `--dump` e leia a
tabela antes de `--aplicar`.

**Autorização:** escrever `Prioridade` em lead real precisa de linha `[x]` do
dono no `APROVADO.md`. Por isso o agendado do `wesales-prioridade.yml` roda
`--dump`, e `--aplicar` só sai por acionamento manual com a caixa marcada — a
própria rotina não se autoriza (regra do `APROVADO.md`).

USO
---
    python3 wesales/tools/recalcula_prioridade.py --dump      # não escreve
    python3 wesales/tools/recalcula_prioridade.py --aplicar    # escreve
"""

import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://services.leadconnectorhq.com"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
PIPELINE_ID = "0Fo2xbeayE4EP6yuSUtq"
CONECTAR = "deb60542-a5cd-43ae-b875-b467b120a72c"
VERSION = "2021-07-28"

CAMPO_PRIORIDADE = "chuJMRlKzY0Uq1f0lSkX"
CAMPO_TENTATIVA = "qHJGJKZBccASOKkKP8ge"
CAMPO_NOTA = "FHoXQnLYA8LW5mFzfdIq"
CAMPO_RESULTADO = "nPafc9c0JdSSptdPhUlF"
CAMPO_PERMISSAO_WA = "kdKnJecyZtssILfPPigl"
CAMPO_SINAL = "jfQgrZFnxhbn1qmCeFDC"
CAMPO_TOTAL_CONEXOES = "tQ7Fzo6cWeBDmEoaTBIZ"

# Extensão 1: quem não deve aparecer na fila do SDR. A 9.2 não prevê.
TAGS_FORA_DA_FILA = ("nao-perturbe", "pausado", "grupo-whatsapp-nao-e-lead")
# Regra 8 da 9.2, que só casa se nenhuma anterior casar.
TAGS_REGRA_8 = ("nutricao-90d", "telefone-invalido")
# AVISO medido em 27/09: nenhum workflow REMOVE `telefone-invalido` — quatro
# aplicam (Cadência 12x30, Cadência Inbound, Pós-ligação v2 e v3) e nenhum apaga
# (§9 do USABILIDADE.md). Então a regra 8 rebaixa para Prioridade 1 de forma
# PERMANENTE: número corrigido na mão continua rebaixado até alguém tirar a tag
# na tela. Não é defeito desta ferramenta — ela só aplica a §9.2 — mas quem lê o
# dump precisa saber por que um lead consertado não volta para a fila.
# Extensão 2: valor de agendado (Pós-agendamento v2). Nunca sobrescrever.
PRIORIDADE_AGENDADO = 6

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
        if "1010" in detail or "cloudflare" in detail.lower():
            raise RuntimeError(
                "GHL %d: bloqueio de Cloudflare pela assinatura do cliente, "
                "não é o token — rode do Action ou do PC" % error.code) from None
        if error.code == 401:
            raise RuntimeError("GHL 401: PIT inválido ou expirado") from None
        if error.code == 429:
            raise RuntimeError("GHL 429: excesso de chamadas, tentar depois") from None
        raise RuntimeError("GHL %d: %s" % (error.code, detail)) from None
    except URLError as error:
        raise RuntimeError("GHL erro de rede: %s" % error.reason) from None


def campo(contato, campo_id):
    for item in contato.get("customFields") or []:
        if item.get("id") == campo_id:
            return item.get("value")
    return None


def como_numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def prioridade(contato, dnd, atual=None):
    """Pura: devolve (nota, motivo). `None` como nota = não escrever.

    Ordem exata da seção 9.2 do `build-wesales.md` — primeira que casa ganha —
    precedida das duas extensões declaradas no topo deste arquivo.
    """
    tags = {str(t).lower() for t in (contato.get("tags") or [])}

    # Extensão 2: agendado não é rebaixado por ninguém.
    if como_numero(atual) == float(PRIORIDADE_AGENDADO):
        return None, "já é %d (agendado) — não sobrescrever" % PRIORIDADE_AGENDADO

    # Extensão 1: fora da fila do SDR.
    if dnd:
        return 0, "[ext] DND ligado"
    for tag in TAGS_FORA_DA_FILA:
        if tag in tags:
            return 0, "[ext] tag %s" % tag

    nota = como_numero(campo(contato, CAMPO_NOTA))
    tentativas = como_numero(campo(contato, CAMPO_TENTATIVA))
    if tentativas is None:
        tentativas = 0.0
    conexoes = como_numero(campo(contato, CAMPO_TOTAL_CONEXOES))
    if conexoes is None:
        conexoes = 0.0
    # Marca do defeito de ordenação da própria 9.2: a regra 8 é a última, então
    # uma regra anterior pode roubar um lead que deveria cair para 1.
    r8 = " [9.2-r8-perdeu]" if any(t in tags for t in TAGS_REGRA_8) else ""

    # 1
    if campo(contato, CAMPO_RESULTADO) == "Pediu retorno":
        return 5, "9.2 r1: pediu retorno" + r8
    # 2
    if nota is not None and nota >= 70:
        return 5, "9.2 r2: nota %g" % nota + r8
    # 3
    if (campo(contato, CAMPO_SINAL) == "Resposta de mensagem"
            or campo(contato, CAMPO_PERMISSAO_WA) == "Sim"):
        return 4, "9.2 r3: respondeu ou deu permissão de WhatsApp" + r8
    # 4
    if nota is not None and 45 <= nota <= 69:
        return 4, "9.2 r4: nota %g" % nota + r8
    # 5
    if tentativas <= 2:
        return 4, "9.2 r5: %g tentativas" % tentativas + r8
    # 6
    if 3 <= tentativas <= 7:
        return 3, "9.2 r6: %g tentativas" % tentativas + r8
    # 7
    if tentativas >= 8 and conexoes == 0:
        return 2, "9.2 r7: %g tentativas, nenhuma conexão" % tentativas + r8
    # 8
    for tag in TAGS_REGRA_8:
        if tag in tags:
            return 1, "9.2 r8: tag %s" % tag

    # Furo de cobertura da 9.2: >= 8 tentativas COM conexão. Não inventar.
    return None, "[9.2-sem-regra] %g tentativas, %g conexões" % (tentativas, conexoes)


def opportunity_items(data):
    if isinstance(data, list):
        return data
    for chave in ("opportunities", "data", "results"):
        valor = data.get(chave) if isinstance(data, dict) else None
        if isinstance(valor, list):
            return valor
    return []


def contatos_de_conectar(token):
    """Busca as oportunidades de CONECTAR e lê cada contato (o search não traz
    customFields nem dnd do contato — medido em 27/09/2026)."""
    query = urlencode({"location_id": LOCATION_ID, "pipeline_id": PIPELINE_ID,
                       "pipeline_stage_id": CONECTAR, "status": "open",
                       "limit": "100"})
    _, data = request("GET", "/opportunities/search?" + query, token)
    vistos, contatos = set(), []
    for oportunidade in opportunity_items(data):
        contact_id = oportunidade.get("contactId")
        if not contact_id or contact_id in vistos:
            continue
        vistos.add(contact_id)
        _, detalhe = request("GET", "/contacts/" + contact_id, token)
        contato = detalhe.get("contact") or detalhe
        contatos.append(contato)
    return contatos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--dump", action="store_true",
                       help="calcula e imprime a tabela, sem escrever nada")
    grupo.add_argument("--aplicar", action="store_true",
                       help="escreve a Prioridade recalculada")
    args = parser.parse_args()

    token = read_token()
    contatos = contatos_de_conectar(token)
    print("CONECTAR: %d contatos" % len(contatos))

    mudancas, distribuicao, achados = [], {}, []
    for contato in contatos:
        atual = como_numero(campo(contato, CAMPO_PRIORIDADE))
        nota, motivo = prioridade(contato, bool(contato.get("dnd")), atual)
        nome = (contato.get("firstName") or contato.get("id") or "?")[:28]
        if "[9.2-" in motivo:
            achados.append((nome, motivo))
        if nota is None:
            distribuicao["(não escrever)"] = distribuicao.get("(não escrever)", 0) + 1
            continue
        distribuicao[nota] = distribuicao.get(nota, 0) + 1
        if atual != float(nota):
            mudancas.append((contato, nome, nota, motivo, atual))

    for chave in sorted(distribuicao, key=lambda k: (isinstance(k, str), k), reverse=True):
        print("  prioridade %s: %d" % (chave, distribuicao[chave]))
    print("a mudar: %d de %d" % (len(mudancas), len(contatos)))

    for _contato, nome, nota, motivo, atual in mudancas:
        print("  %-28s %s -> %d  (%s)" % (
            nome, "-" if atual is None else "%g" % atual, nota, motivo))

    if achados:
        print("\ndefeitos da 9.2 encontrados nestes leads (não corrigidos aqui):")
        for nome, motivo in achados:
            print("  %-28s %s" % (nome, motivo))

    if args.dump:
        print("\n--dump: nada foi escrito")
        return
    if not mudancas:
        print("nada a escrever")
        return

    for contato, nome, nota, _motivo, _atual in mudancas:
        request("PUT", "/contacts/" + contato["id"], token,
                {"customFields": [{"id": CAMPO_PRIORIDADE, "fieldValue": nota}]})
    print("aplicado em %d contatos" % len(mudancas))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("parou sem aplicar: " + str(error))
        raise SystemExit(1)
