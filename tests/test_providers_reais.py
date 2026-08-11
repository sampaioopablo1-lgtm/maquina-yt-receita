"""Testes de resiliencia dos providers reais (sem rede: httpx mockado)."""

from __future__ import annotations

import httpx
import pytest

from maquina.providers.base import ErroProvider
from maquina.providers.reais import ImagemPollinations


class _RespostaFalsa:
    def __init__(self, status_code: int, content: bytes = b"", text: str = ""):
        self.status_code = status_code
        self.content = content
        self.text = text or content.decode(errors="ignore")


def test_pollinations_repete_apos_429_e_entrega(monkeypatch, tmp_path):
    respostas = [
        _RespostaFalsa(429, text='{"error":"Too Many Requests"}'),
        _RespostaFalsa(200, content=b"png-fake"),
    ]
    chamadas = []

    def get_fake(url, timeout=None, follow_redirects=None):
        chamadas.append(url)
        return respostas.pop(0)

    monkeypatch.setattr(httpx, "get", get_fake)
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)

    saida = tmp_path / "cena_001.png"
    resultado = ImagemPollinations().gerar("por do sol", saida, largura=1280, altura=720)

    assert resultado == saida
    assert saida.read_bytes() == b"png-fake"
    assert len(chamadas) == 2


def test_pollinations_desiste_apos_esgotar_tentativas(monkeypatch, tmp_path):
    def get_sempre_429(url, timeout=None, follow_redirects=None):
        return _RespostaFalsa(429, text='{"error":"Too Many Requests"}')

    monkeypatch.setattr(httpx, "get", get_sempre_429)
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)

    with pytest.raises(ErroProvider, match="429"):
        ImagemPollinations().gerar("por do sol", tmp_path / "cena_001.png", largura=1280, altura=720)


def test_pollinations_erro_definitivo_nao_repete(monkeypatch, tmp_path):
    chamadas = []

    def get_400(url, timeout=None, follow_redirects=None):
        chamadas.append(url)
        return _RespostaFalsa(400, text="prompt invalido")

    monkeypatch.setattr(httpx, "get", get_400)
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)

    with pytest.raises(ErroProvider, match="400"):
        ImagemPollinations().gerar("x", tmp_path / "cena_001.png", largura=1280, altura=720)

    assert len(chamadas) == 1
