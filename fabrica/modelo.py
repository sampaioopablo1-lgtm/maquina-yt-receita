#!/usr/bin/env python3
"""A unica porta da fabrica para a API do modelo — e o contador do que ela custa.

Existe por duas razoes, e a segunda e a que importa mais.

A primeira e que `autor.py` e `fatos.py` nasceram no mesmo dia com o mesmo
laco de SSE copiado, e codigo de rede duplicado diverge: um ganha um retry, o
outro nao, e a diferenca so aparece no dia em que a rede pisca no meio de uma
geracao.

A segunda e o CUSTO. A escrita automatica de roteiro e a primeira coisa nesta
maquina que gasta dinheiro por pacote, e a conta escala com a meta: 5 pacotes
por canal por dia, treze canais, sao 65 pacotes. A diferenca entre isso custar
50 ou 300 dolares por dia decide se a meta e sustentavel, e essa diferenca nao
se estima — se mede. Toda chamada que passa por aqui soma tokens e dolares num
contador de processo, e quem chama imprime o total no fim.

Streaming e obrigatorio, nao preferencia: com busca na web a resposta leva
minutos, e sem stream a requisicao morre no timeout do proxy antes de o modelo
terminar. Nao ha caminho sem stream neste arquivo de proposito.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

API = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

# ----------------------------------------------------------------------------
# DUAS CREDENCIAIS, DUAS CARTEIRAS — e a diferenca e de DINHEIRO, nao de gosto.
#
# `ANTHROPIC_API_KEY` gasta credito do Console, que e uma carteira separada da
# assinatura do Claude: quem tem assinatura NAO tem credito de API por isso.
# `CLAUDE_CODE_OAUTH_TOKEN` (o que o `claude setup-token` emite) autentica
# contra a ASSINATURA que o dono ja paga. Foi o dono quem apontou isso em
# 14/10, depois de eu ter recomendado a chave de API olhando so o nome da
# variavel que este arquivo lia.
#
# O que eu NAO AFIRMO, porque nao tenho token para medir: que o token do
# `setup-token` seja aceito por `POST /v1/messages` chamado deste script. Ele
# nasceu para autenticar a CLI do Claude Code, e a CLI pode falar por uma rota
# que nao e esta. O que este modulo garante e so o mapeamento do CABECALHO:
# chave de API vai em `x-api-key`; token de OAuth vai em `Authorization:
# Bearer` com o cabecalho de beta. Se o servidor recusar, a mensagem do 401/403
# aparece inteira pelo caminho de erro que ja existe, e a leitura disso e
# medicao — nao suposicao minha escrita aqui.
#
# A ORDEM e deliberada: a chave de API vem primeiro porque e a rota VERIFICADA.
# Quem tiver as duas coisas no ambiente usa a que sabemos que funciona.
# ----------------------------------------------------------------------------

BETA_OAUTH = "oauth-2025-04-20"


class Credencial:
    """O segredo mais a FORMA de apresenta-lo. Nao imprime o valor."""

    def __init__(self, tipo: str, valor: str):
        self.tipo = tipo          # "api_key" ou "oauth"
        self.valor = valor

    def __repr__(self) -> str:   # pragma: no cover - so para log acidental
        return f"Credencial(tipo={self.tipo!r}, valor=<{len(self.valor)} chars>)"

    __str__ = __repr__


def credencial(env: dict[str, str] | None = None) -> Credencial:
    """Le o ambiente e devolve a credencial, ou morre dizendo os DOIS nomes."""
    env = os.environ if env is None else env
    chave = (env.get("ANTHROPIC_API_KEY") or "").strip()
    if chave:
        return Credencial("api_key", chave)
    token = (env.get("CLAUDE_CODE_OAUTH_TOKEN") or "").strip()
    if token:
        return Credencial("oauth", token)
    raise SystemExit(
        "credencial ausente: defina ANTHROPIC_API_KEY (credito do Console) ou "
        "CLAUDE_CODE_OAUTH_TOKEN (assinatura, pelo `claude setup-token`)")


def cabecalhos(cred: Credencial) -> dict[str, str]:
    """O mapeamento credencial -> cabecalho. E a unica coisa que este modulo
    afirma sobre o token de OAuth."""
    base = {"anthropic-version": "2023-06-01", "content-type": "application/json"}
    if cred.tipo == "api_key":
        return {**base, "x-api-key": cred.valor}
    if cred.tipo == "oauth":
        return {**base, "authorization": f"Bearer {cred.valor}",
                "anthropic-beta": BETA_OAUTH}
    raise SystemExit(f"tipo de credencial desconhecido: {cred.tipo!r}")

# US$ por milhao de tokens. Espelha PRECO_ANTHROPIC de
# src/maquina/providers/reais.py; quando a tabela de precos mudar, muda nos
# dois — o contador so vale enquanto o preco for o de verdade.
PRECO = {
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
}
PRECO_PADRAO = (5.00, 25.00)

TENTATIVAS = 3


class Gasto:
    """Contador de processo. Zerado a cada execucao, impresso no fim."""

    def __init__(self):
        self.entrada = self.saida = self.chamadas = 0
        self.usd = 0.0

    def soma(self, modelo: str, uso: dict) -> None:
        ent = uso.get("input_tokens", 0) + uso.get("cache_read_input_tokens", 0)
        sai = uso.get("output_tokens", 0)
        pe, ps = PRECO.get(modelo, PRECO_PADRAO)
        self.entrada += ent
        self.saida += sai
        self.chamadas += 1
        self.usd += ent / 1e6 * pe + sai / 1e6 * ps

    def __str__(self) -> str:
        return (f"{self.chamadas} chamada(s), {self.entrada} tokens de entrada, "
                f"{self.saida} de saida, US$ {self.usd:.2f}")


GASTO = Gasto()


def chamar(sistema: str, mensagens: list[dict], *, modelo: str,
           max_tokens: int = 32000, ferramentas: list[dict] | None = None,
           timeout: int = 1800) -> str:
    """POST /v1/messages em streaming. Devolve so o texto, e contabiliza o uso.

    Retenta apenas o que faz sentido retentar: erro de transporte e 429/5xx.
    Um 400 e defeito do pedido e repetir tres vezes so gasta tres vezes.
    """
    cred = credencial()

    corpo = {"model": modelo, "max_tokens": max_tokens, "system": sistema,
             "messages": mensagens, "thinking": {"type": "adaptive"},
             "stream": True}
    if ferramentas:
        corpo["tools"] = ferramentas

    ultimo = None
    for tentativa in range(TENTATIVAS):
        try:
            return _uma_vez(corpo, cred, modelo, timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                detalhe = e.read().decode("utf-8", "replace")[:500]
                raise SystemExit(f"API recusou o pedido ({e.code}): {detalhe}")
            ultimo = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            ultimo = e
        if tentativa < TENTATIVAS - 1:
            import time

            time.sleep(2 ** (tentativa + 1))
    raise SystemExit(f"API inalcancavel apos {TENTATIVAS} tentativas: {ultimo}")


def _uma_vez(corpo: dict, cred: Credencial, modelo: str, timeout: int) -> str:
    req = urllib.request.Request(
        f"{API}/v1/messages", data=json.dumps(corpo).encode("utf-8"), method="POST",
        headers=cabecalhos(cred))
    partes, uso = [], {}
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for linha in r:
            linha = linha.decode("utf-8", "replace").strip()
            if not linha.startswith("data:"):
                continue
            try:
                ev = json.loads(linha[5:].strip())
            except json.JSONDecodeError:
                continue
            tipo = ev.get("type")
            if tipo == "content_block_delta":
                d = ev.get("delta") or {}
                if d.get("type") == "text_delta":
                    partes.append(d.get("text") or "")
            elif tipo == "message_start":
                uso.update((ev.get("message") or {}).get("usage") or {})
            elif tipo == "message_delta":
                uso.update(ev.get("usage") or {})
            elif tipo == "error":
                raise SystemExit(f"API devolveu erro: {ev.get('error')}")
    GASTO.soma(modelo, uso)
    return "".join(partes)


def so_o_json(texto: str) -> dict:
    """O modelo as vezes embrulha em cerca, as vezes comenta antes.

    Do primeiro `{` ao ultimo `}` resolve os dois casos sem regex fragil.
    """
    a, b = texto.find("{"), texto.rfind("}")
    if a < 0 or b <= a:
        raise SystemExit(f"resposta sem JSON reconhecivel: {texto[:300]!r}")
    return json.loads(texto[a:b + 1])
