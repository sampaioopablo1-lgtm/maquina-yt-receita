"""A porta unica para a API — e o contador do que ela custa.

A escrita automatica de roteiro e a primeira coisa desta maquina que gasta
dinheiro POR PACOTE. A meta de 5 por canal por dia sao 65 pacotes; a diferenca
entre isso custar 50 ou 300 dolares decide se a meta e sustentavel. Esse numero
nao se estima, se mede — e quem mede e este contador.
"""
from __future__ import annotations

import json
import sys
import urllib.error
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import modelo  # noqa: E402


def _stream(eventos: list[dict]) -> list[bytes]:
    return [b"event: x\n"] + [
        f"data: {json.dumps(e)}\n".encode("utf-8") for e in eventos]


class _Resposta:
    def __init__(self, linhas):
        self._linhas = linhas

    def __iter__(self):
        return iter(self._linhas)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


@pytest.fixture(autouse=True)
def _zera(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-teste")
    modelo.GASTO = modelo.Gasto()


# ------------------------------------------------------------------- o custo

def test_o_uso_sai_do_stream_e_vira_dolar(monkeypatch):
    """message_start traz a entrada, message_delta traz a saida final. Somar so
    um dos dois subestima a conta pela metade."""
    eventos = [
        {"type": "message_start", "message": {"usage": {"input_tokens": 200_000}}},
        {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "oi"}},
        {"type": "message_delta", "usage": {"output_tokens": 40_000}},
    ]
    monkeypatch.setattr(modelo.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(_stream(eventos)))
    texto = modelo.chamar("s", [{"role": "user", "content": "x"}],
                          modelo="claude-opus-5")
    assert texto == "oi"
    # 200k entrada a US$5/M + 40k saida a US$25/M = 1,00 + 1,00
    assert modelo.GASTO.usd == pytest.approx(2.00, abs=0.01)
    assert modelo.GASTO.chamadas == 1


def test_o_cache_conta_como_entrada(monkeypatch):
    eventos = [{"type": "message_start",
                "message": {"usage": {"input_tokens": 1000,
                                      "cache_read_input_tokens": 99_000}}},
               {"type": "message_delta", "usage": {"output_tokens": 0}}]
    monkeypatch.setattr(modelo.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(_stream(eventos)))
    modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")
    assert modelo.GASTO.entrada == 100_000


def test_varias_chamadas_acumulam(monkeypatch):
    eventos = [{"type": "message_start", "message": {"usage": {"input_tokens": 1_000_000}}},
               {"type": "message_delta", "usage": {"output_tokens": 0}}]
    monkeypatch.setattr(modelo.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(_stream(eventos)))
    for _ in range(3):
        modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")
    assert modelo.GASTO.chamadas == 3
    assert modelo.GASTO.usd == pytest.approx(15.00, abs=0.01)


def test_modelo_fora_da_tabela_usa_o_preco_padrao(monkeypatch):
    eventos = [{"type": "message_start", "message": {"usage": {"input_tokens": 1_000_000}}},
               {"type": "message_delta", "usage": {"output_tokens": 0}}]
    monkeypatch.setattr(modelo.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(_stream(eventos)))
    modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-que-ainda-nao-existe")
    assert modelo.GASTO.usd > 0


def test_o_preco_bate_com_o_do_provider_antigo():
    """Duas tabelas de preco viram dois precos diferentes."""
    sys.path.insert(0, str(RAIZ / "src"))
    from maquina.providers.reais import PRECO_ANTHROPIC

    for m, (ent, sai) in modelo.PRECO.items():
        assert PRECO_ANTHROPIC[m] == {"entrada": ent, "saida": sai}, m


# ------------------------------------------------------------------ o retry

def _erro(code):
    return urllib.error.HTTPError("u", code, "m", {}, None)


def test_pedido_invalido_nao_e_retentado(monkeypatch):
    """Um 400 e defeito do pedido. Repetir tres vezes so gasta tres vezes."""
    chamadas = []

    def falha(*a, **k):
        chamadas.append(1)
        raise urllib.error.HTTPError("u", 400, "m", {}, __import__("io").BytesIO(b"ruim"))

    monkeypatch.setattr(modelo.urllib.request, "urlopen", falha)
    with pytest.raises(SystemExit) as e:
        modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")
    assert len(chamadas) == 1
    assert "400" in str(e.value)


def test_excesso_de_pedidos_e_retentado(monkeypatch):
    chamadas = []
    eventos = [{"type": "content_block_delta", "delta": {"type": "text_delta", "text": "ok"}}]

    def as_vezes(*a, **k):
        chamadas.append(1)
        if len(chamadas) < 3:
            raise _erro(429)
        return _Resposta(_stream(eventos))

    monkeypatch.setattr(modelo.urllib.request, "urlopen", as_vezes)
    monkeypatch.setattr(modelo, "TENTATIVAS", 3)
    import time

    monkeypatch.setattr(time, "sleep", lambda s: None)
    assert modelo.chamar("s", [{"role": "user", "content": "x"}],
                         modelo="claude-opus-5") == "ok"
    assert len(chamadas) == 3


def test_erro_de_servidor_e_retentado(monkeypatch):
    chamadas = []

    def falha(*a, **k):
        chamadas.append(1)
        raise _erro(503)

    monkeypatch.setattr(modelo.urllib.request, "urlopen", falha)
    import time

    monkeypatch.setattr(time, "sleep", lambda s: None)
    with pytest.raises(SystemExit):
        modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")
    assert len(chamadas) == modelo.TENTATIVAS


def test_erro_no_meio_do_stream_nao_vira_texto_truncado(monkeypatch):
    """Meia resposta parseada como JSON e o pior jeito de falhar: ela vira uma
    spec com metade das cenas e ninguem ve."""
    eventos = [{"type": "content_block_delta", "delta": {"type": "text_delta", "text": "{"}},
                {"type": "error", "error": {"type": "overloaded_error"}}][:2]
    monkeypatch.setattr(modelo.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(_stream(eventos)))
    with pytest.raises(SystemExit):
        modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")


def test_sem_chave_nao_tenta():
    import os

    guardada = os.environ.pop("ANTHROPIC_API_KEY")
    try:
        with pytest.raises(SystemExit):
            modelo.chamar("s", [{"role": "user", "content": "x"}], modelo="claude-opus-5")
    finally:
        os.environ["ANTHROPIC_API_KEY"] = guardada


# ------------------------------------------------------------------- o parse

def test_json_dentro_de_cerca_de_codigo():
    assert modelo.so_o_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_json_depois_de_comentario():
    assert modelo.so_o_json('Claro, aqui esta:\n{"a": 1}') == {"a": 1}


def test_texto_sem_json_falha_dizendo_o_que_veio():
    with pytest.raises(SystemExit) as e:
        modelo.so_o_json("nao consigo fazer isso")
    assert "nao consigo" in str(e.value)
