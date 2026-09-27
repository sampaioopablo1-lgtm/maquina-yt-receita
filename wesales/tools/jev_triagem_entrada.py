#!/usr/bin/env python3
"""Pergunta ao Jev se o fio que entrou pela porta e LEAD ou nao — modo relatorio.

O DEFEITO QUE ISTO ATACA, medido duas vezes em 23/09/2026: a `Porta de Entrada`
cria oportunidade para qualquer contato novo do WhatsApp, e o GHL nao tem campo
que distinga prospect de gente da vida do dono. Em 5 horas entraram como lead a
`Francisca` (conversa pessoal — pix, carona) e a `Rafaela de Paula - We Sales`
(a atendente da propria plataforma). O G-16 escreveu, e esta certo: "o filtro
que falta nao e algo que um workflow consiga decidir sozinho". Nao e mesmo — e
uma pergunta de classificacao, e o Jev existe para isso.

**NAO ESCREVE NADA NO CRM.** Le, pergunta, imprime tabela. Aplicar tag depende
de `[x]` no `APROVADO.md`, e nao existe. Modo relatorio e tambem o unico jeito
honesto de comecar: da para comparar o palpite com a realidade antes de dar
autonomia a ele.

Chaves, as duas por variavel de ambiente (secret no GitHub, nunca no chat):
  GHL_PIT           token da subconta
  OPENCODE_API_KEY  (ou TYPESAFE_API_KEY / OPENROUTER_API_KEY / AI_GATEWAY_API_KEY)

Uso:
  python3 jev_triagem_entrada.py --pergunta   # imprime o corpo que enviaria; SEM rede
  python3 jev_triagem_entrada.py --limite 10  # le a conta, pergunta ao Jev, imprime
"""
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

GHL = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
PIPELINE_ID = "0Fo2xbeayE4EP6yuSUtq"
NOVO_LEAD = "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d"
CONECTAR = "deb60542-a5cd-43ae-b875-b467b120a72c"

# As duas etapas onde um lead novo pode estar. `CONECTAR` entrou em 27/09/2026:
# o backfill do G-03 promoveu 38 de `NOVO LEAD` para la, e e em `CONECTAR` que a
# `Cadência Inbound` toca o lead — varrer so `NOVO LEAD` olharia a fila vazia.
ETAPAS = [("NOVO LEAD", NOVO_LEAD), ("CONECTAR", CONECTAR)]

# Onde o Jev atende. Mesma tabela do `jev-gateway` (src/providers.json).
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
# O `jev-1.13-free` do OpenCode Zen e gratuito "por tempo limitado" (README do
# `jev-gateway`). Quando sair do ar, o endpoint responde 404 ou 410 — e sem este
# aviso a rodada pareceria defeito do script. `JEV_MODEL=jev-1.13` opta pelo pago.
FIM_DO_FREE = (404, 410)


def avisa_free_acabou(codigo, modelo):
    """True se o codigo HTTP indica que o modelo gratuito saiu do ar."""
    if codigo in FIM_DO_FREE and "free" in (modelo or ""):
        print("")
        print("=" * 72)
        print("O MODELO GRATUITO DO JEV SAIU DO AR (HTTP %s em %s)." % (codigo, modelo))
        print("Nao e defeito do script nem chave invalida: o `jev-1.13-free` do")
        print("OpenCode Zen era gratuito por tempo limitado.")
        print("")
        print("Para continuar, escolha uma:")
        print("  - pagar no OpenCode: defina JEV_MODEL=jev-1.13")
        print("  - ir para a TypeSafe oficial: defina TYPESAFE_API_KEY")
        print("=" * 72)
        return True
    return False

# As quatro saidas. O rotulo e o que o Jev devolve; a descricao e o que ele le.
CRITERIOS = {
    "lead_comercial": (
        "Alguem que nao conhece o dono pessoalmente e demonstra interesse comercial: "
        "pergunta sobre o servico, preco, anuncios, resultados, agencia, ou responde a "
        "uma abordagem de vendas. Veio de anuncio, formulario ou indicacao."),
    "pessoal": (
        "Conversa da vida pessoal do dono: familia, amigos, vizinhos, dinheiro emprestado, "
        "carona, encontro, assunto domestico. Chama o dono pelo primeiro nome com "
        "familiaridade e nao menciona negocio nenhum."),
    "suporte_ou_fornecedor": (
        "Atendimento, suporte tecnico, vendedor de ferramenta, plataforma ou servico que o "
        "dono USA ou contratou: fala de conta, plano, assinatura, numero comprado, teste, "
        "fatura, ou pede/oferece ajuda tecnica. O dono e o cliente aqui, nao o vendedor."),
    "indeterminado": (
        "O fio e curto, vazio ou ambiguo demais para decidir: so saudacao, so emoji, "
        "so um audio sem texto, ou nada que indique o motivo do contato."),
}

PERGUNTAS = {
    "classe": {"type": "choice",
               "instructions": ("Este fio de WhatsApp chegou ao numero comercial de uma agencia de "
                                "trafego pago. Quem escreveu e um prospect, ou e outra coisa? "
                                "Escolha a unica opcao que descreve o fio."),
               "criteria": CRITERIOS},
    "vale_abordar": {"type": "noul",
                     "instructions": ("Um SDR deveria abordar comercialmente quem escreveu este fio? "
                                      "Responda nao se for conversa pessoal do dono, suporte, "
                                      "fornecedor, ou se o fio nao der para saber.")},
}


def pede(url, headers, body=None, metodo="GET"):
    dados = json.dumps(body).encode() if body is not None else None
    req = Request(url, data=dados, headers=headers, method=metodo)
    with urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode() or "{}")


def ghl(caminho, token, body=None, metodo="GET"):
    # O `user-agent` vale aqui tambem, nao so no Jev: o `services.leadconnectorhq.com`
    # esta atras do mesmo Cloudflare e recusa `Python-urllib/3.x` com erro 1010.
    # Medido em 27/09/2026 — o primeiro conserto pos UA so nas chamadas do Jev, e
    # esta busca continuou levando 403/1010, que eu li errado como problema de token.
    return pede(GHL + caminho,
                {"Authorization": "Bearer " + token, "Version": VERSION,
                 "Accept": "application/json", "Content-Type": "application/json",
                 "user-agent": UA},
                body, metodo)


def provedor():
    """(nome da variavel, url, modelo, chave) do primeiro provedor com chave no ambiente."""
    for var, url, modelo in PROVEDORES:
        chave = os.environ.get(var, "").strip()
        if chave:
            return var, os.environ.get("JEV_URL", "").strip() or url, \
                   os.environ.get("JEV_MODEL", "").strip() or modelo, chave
    return None, None, None, None


def estado(contato, mensagens):
    """O `state` do Jev: contexto cru, sem opiniao. Ele decide, nao eu."""
    return {
        "nome_no_crm": contato.get("contactName") or contato.get("fullName") or "",
        "telefone": contato.get("phone") or "",
        "origem_no_crm": contato.get("source") or "(vazia)",
        "primeiras_mensagens": mensagens,
    }


def fio(token, contact_id, quantas=8):
    """As primeiras mensagens da conversa, em ordem, so direcao e texto."""
    try:
        conv = ghl("/conversations/search?locationId=%s&contactId=%s&limit=1"
                   % (LOCATION_ID, contact_id), token)
    except (HTTPError, URLError):
        return []
    achadas = (conv.get("conversations") or [])
    if not achadas:
        return []
    try:
        msgs = ghl("/conversations/%s/messages?limit=%d" % (achadas[0]["id"], quantas), token)
    except (HTTPError, URLError):
        return []
    saida = []
    for m in reversed(((msgs.get("messages") or {}).get("messages")) or []):
        corpo = (m.get("body") or "").strip()
        if not corpo or m.get("type") == 28:      # 28 = atividade de sistema
            continue
        saida.append({"de": "lead" if m.get("direction") == "inbound" else "nos",
                      "texto": corpo[:400]})
    return saida


def pergunta_ao_jev(url, modelo, chave, st):
    corpo = {"model": modelo, "state": st, "questions": PERGUNTAS}
    return pede(url, {"Authorization": "Bearer " + chave, "Content-Type": "application/json",
                      "http-referer": "https://github.com/sampaioopablo1-lgtm/maquina-yt-receita",
                      "user-agent": UA,
                      "x-title": "wesales-triagem-entrada"}, corpo, "POST")


def resposta(r, chave_pergunta):
    """(valor, confianca) para `choice` e para `noul`.

    O `noul` NAO vem em `choice` nem em `value`: vem no campo `noul`, como
    probabilidade 0..1 (o `jev-gateway` le exatamente assim — `needs.noul >= 0.5`).
    Medido em 27/09/2026: era por isso que a coluna `abordar?` saia `None` na
    primeira triagem, com a classe respondida corretamente ao lado.
    """
    for caminho in (r.get("answers"), r.get("results"), r):
        if isinstance(caminho, dict) and chave_pergunta in caminho:
            a = caminho[chave_pergunta] or {}
            if a.get("type") == "noul" or isinstance(a.get("noul"), (int, float)):
                n = a.get("noul")
                if not isinstance(n, (int, float)):
                    return None, None
                # confianca de um noul e a distancia da duvida: 0.9 -> 0.9, 0.1 -> 0.9
                return ("sim" if n >= 0.5 else "nao"), max(n, 1 - n)
            return (a.get("choice") if a.get("choice") is not None else a.get("value"),
                    a.get("confidence"))
    return None, None


def main():
    if "--pergunta" in sys.argv:
        print("Corpo que seria enviado (sem rede, sem chave, com um fio de exemplo):\n")
        exemplo = estado({"contactName": "Rafaela de Paula - We Sales", "phone": "+5547991548812"},
                         [{"de": "nos", "texto": "Comprei o número telefônico"},
                          {"de": "nos", "texto": "E também sobre 20 dias a mais do teste, não habilitou"}])
        print(json.dumps({"model": "jev-1.13-free", "state": exemplo, "questions": PERGUNTAS},
                         ensure_ascii=False, indent=2))
        print("\nPOST para o `url` do provedor com chave no ambiente. Nada e gravado no CRM.")
        return 0

    var, url, modelo, chave = provedor()
    if not chave:
        print("sem chave do Jev: defina uma de %s" % ", ".join(v for v, _, _ in PROVEDORES))
        return 2
    token = os.environ.get("GHL_PIT", "").strip()
    if not token:
        print("sem GHL_PIT no ambiente")
        return 2

    limite = 20
    if "--limite" in sys.argv:
        limite = int(sys.argv[sys.argv.index("--limite") + 1])

    print("Jev via %s (%s), modelo %s" % (var, url, modelo))
    ops = []
    try:
        for rotulo, etapa in ETAPAS:
            busca = ("/opportunities/search?location_id=%s&pipeline_id=%s"
                     "&pipeline_stage_id=%s&status=open&limit=%d"
                     % (LOCATION_ID, PIPELINE_ID, etapa, limite))
            desta = (ghl(busca, token).get("opportunities")) or []
            print("  %-10s %d oportunidade(s) open" % (rotulo, len(desta)))
            for o in desta:
                o["_etapa"] = rotulo
            ops += desta
    except HTTPError as e:
        # 403 aqui e o GHL recusando o PIT, nao defeito do script. Medido em
        # 27/09/2026: o Jev respondeu 3 de 3 e esta busca levou 403 na mesma
        # rodada, o que localiza o problema no token e nao na integracao.
        corpo = (e.read() or b"")[:200].decode("utf-8", "replace")
        print("O GHL recusou a leitura: HTTP %s %s" % (e.code, corpo))
        if "1010" in corpo or "cloudflare" in corpo.lower():
            print("\nErro 1010 e do CLOUDFLARE, nao do seu token: ele barra o cliente")
            print("pela assinatura antes de olhar a chave. O `user-agent` deste script")
            print("deveria resolver; se persistir, o IP do runner esta na lista.")
            return 2
        if e.code in (401, 403):
            print("\nIsto e o `GHL_PIT`, nao o Jev. Confira, nesta ordem:")
            print("  1. o token do secret `GHL_PIT` ainda e valido (nao foi rotacionado);")
            print("  2. ele e da subconta %s;" % LOCATION_ID)
            print("  3. tem os escopos de LEITURA: opportunities.readonly,")
            print("     contacts.readonly e conversations.readonly.")
            print("\nO teste minimo (`jev_teste_minimo.py`) nao usa o GHL — se ele")
            print("passa e este falha, o Jev esta certo e o token nao.")
        return 2
    except URLError as e:
        print("rede indisponivel ao falar com o GHL: %s" % e.reason)
        return 1
    print("\n%d oportunidade(s) no total\n" % len(ops))
    print("%-28s %-10s %-22s %5s  %s" % ("contato", "etapa", "classe", "conf", "abordar?"))
    print("-" * 88)

    contagem = {}
    for o in ops:
        rel = (o.get("relations") or [{}])[0]
        msgs = fio(token, o.get("contactId"))
        if not msgs:
            print("%-28s %-10s %-22s %5s  %s" % ((rel.get("contactName") or "?")[:28],
                                                 o.get("_etapa", "?"), "(sem mensagem)", "-", "-"))
            contagem["(sem mensagem)"] = contagem.get("(sem mensagem)", 0) + 1
            continue
        try:
            r = pergunta_ao_jev(url, modelo, chave, estado(rel, msgs))
        except HTTPError as e:
            corpo = (e.read() or b"")[:120].decode("utf-8", "replace")
            print("%-28s ERRO %s: %s" % ((rel.get("contactName") or "?")[:28], e.code, corpo))
            if avisa_free_acabou(e.code, modelo):
                return 2
            continue
        except URLError as e:
            print("rede indisponivel: %s" % e)
            return 1
        classe, conf = resposta(r, "classe")
        abordar, _ = resposta(r, "vale_abordar")
        contagem[classe] = contagem.get(classe, 0) + 1
        print("%-28s %-10s %-22s %5s  %s" % (
            (rel.get("contactName") or "?")[:28], o.get("_etapa", "?"), classe,
            ("%.2f" % conf) if isinstance(conf, (int, float)) else "-",
            abordar if abordar is not None else "-"))

    print("\nresumo: " + ", ".join("%s=%d" % x for x in sorted(contagem.items())))
    print("\nMODO RELATORIO: nada foi escrito no CRM. Para virar tag, precisa de `[x]`")
    print("no APROVADO.md — compare esta tabela com a realidade antes de autorizar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
