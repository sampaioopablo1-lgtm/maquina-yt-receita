"""Empilhar plano gratuito: a saida do Gemini sem trocar por plano pago.

O problema nunca foi qualidade, foi cota — 20 requisicoes/dia do free tier do
Gemini contra os 30 que seis pacotes diarios consomem. A resposta obvia seria
assinar alguem; a resposta barata e empilhar quatro free tiers e deixar a
cadeia trocar de elo quando um bate no limite. Medido em 13/08/2026:

    Cerebras   1M tokens/dia,  30 RPM   (sem cartao)
    Groq       14.400 req/dia,  6k TPM  (sem cartao)
    Mistral    1B tokens/mes,   2 RPM   (sem cartao, pede telefone)
    Gemini     20 req/dia               (o que ja tinhamos)

Somados sobra folga de ordem de grandeza. Os limites por MINUTO e por REQUEST e
que mordem — 6k TPM da Groq nao cabe um roteiro de longo — e e por isso que a
cadeia precisa existir em vez de um provedor so.

Todos falam /chat/completions, entao uma classe cobre os quatro e trocar de
fornecedor vira uma linha de YAML.
"""

from __future__ import annotations

import json

import httpx
import pytest

from maquina.providers.base import ErroProvider
from maquina.providers.reais import LLMCompativelOpenAI


def _llm(monkeypatch, responder, modelo="gpt-oss-120b") -> tuple:
    monkeypatch.setenv("GROQ_API_KEY", "chave-de-teste")
    llm = LLMCompativelOpenAI(
        "groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY", modelo
    )
    pedidos: list[dict] = []

    def _handler(req: httpx.Request) -> httpx.Response:
        pedidos.append(json.loads(req.content) if req.content else {"url": str(req.url)})
        return responder(len(pedidos))

    llm._cli = httpx.Client(
        transport=httpx.MockTransport(_handler), base_url="https://api.groq.com/openai/v1"
    )
    return llm, pedidos


def _resposta(texto: str, motivo: str = "stop", tokens=(100, 200)) -> httpx.Response:
    return httpx.Response(200, json={
        "choices": [{"message": {"content": texto}, "finish_reason": motivo}],
        "usage": {"prompt_tokens": tokens[0], "completion_tokens": tokens[1]},
    })


def test_fala_o_dialeto_openai(monkeypatch):
    llm, pedidos = _llm(monkeypatch, lambda _: _resposta("ok"))

    assert llm.completar("escreva", sistema="voce e roteirista") == "ok"

    corpo = pedidos[0]
    assert corpo["model"] == "gpt-oss-120b"
    assert corpo["messages"][0] == {"role": "system", "content": "voce e roteirista"}
    assert corpo["messages"][1]["content"] == "escreva"


def test_rascunho_de_modelo_de_raciocinio_nao_vaza_para_o_roteiro(monkeypatch):
    """gpt-oss e qwen as vezes devolvem o <think> dentro do proprio content.

    O retorno vai direto para json.loads na etapa de roteiro: rascunho junto e
    JSONDecodeError com uma mensagem que nao diz nada sobre a causa.
    """
    bruto = '<think>vou fazer 5 cenas</think>{"cenas": []}'
    llm, _ = _llm(monkeypatch, lambda _: _resposta(bruto))

    assert llm.completar("x") == '{"cenas": []}'


def test_resposta_cortada_por_tamanho_e_denunciada(monkeypatch):
    """Truncar e o modo de falha mais comum aqui: os free tiers tem teto baixo
    de saida por request, e o JSON pela metade so aparece camadas acima."""
    llm, _ = _llm(monkeypatch, lambda _: _resposta('{"cenas": [{"narr', "length"))

    with pytest.raises(ErroProvider, match="truncado"):
        llm.completar("x")


def test_resposta_vazia_nao_passa_como_roteiro(monkeypatch):
    llm, _ = _llm(monkeypatch, lambda _: _resposta(""))

    with pytest.raises(ErroProvider, match="vazia"):
        llm.completar("x")


def test_free_tier_nao_soma_custo(monkeypatch):
    """O custo por video precisa continuar dizendo a verdade."""
    llm, _ = _llm(monkeypatch, lambda _: _resposta("ok"))

    llm.completar("x")

    assert llm.custo_usd == 0.0


def test_openai_paga_soma_custo(monkeypatch):
    from maquina.providers.reais import LLMOpenAI

    monkeypatch.setenv("OPENAI_API_KEY", "k")
    llm = LLMOpenAI("gpt-4o-mini")

    assert llm.preco["saida"] > 0, "a OpenAI nao e free tier — nao pode contar zero"


def test_429_de_cota_e_repetido_e_depois_vira_erro_de_provider(monkeypatch):
    """429 aqui e o sinal de trocar de elo — tem que chegar como ErroProvider."""
    monkeypatch.setattr("time.sleep", lambda _: None)
    llm, pedidos = _llm(monkeypatch, lambda _: httpx.Response(429, text="rate limit"))

    with pytest.raises(ErroProvider, match="429"):
        llm.completar("x")
    assert len(pedidos) == 3, "tenta de novo antes de desistir do provedor"


def test_lista_os_modelos_que_o_provedor_serve_hoje(monkeypatch):
    """Os ids mudam depressa: o qwen3-32b da Groq saiu em jun/2026, e duas
    fontes publicas discordavam do id certo no mesmo dia. Chumbar id em codigo
    e agendar um 404 — por isso o id vem do YAML e existe este comando."""
    resposta = httpx.Response(200, json={"data": [
        {"id": "openai/gpt-oss-120b"}, {"id": "llama-3.3-70b-versatile"},
    ]})
    llm, _ = _llm(monkeypatch, lambda _: resposta)

    assert llm.modelos_disponiveis() == ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]


def test_sem_chave_recusa_na_construcao_dizendo_qual_env(monkeypatch):
    monkeypatch.delenv("CEREBRAS_API_KEY", raising=False)

    with pytest.raises(ErroProvider, match="CEREBRAS_API_KEY"):
        LLMCompativelOpenAI(
            "cerebras", "https://api.cerebras.ai/v1", "CEREBRAS_API_KEY", "gpt-oss-120b"
        )
