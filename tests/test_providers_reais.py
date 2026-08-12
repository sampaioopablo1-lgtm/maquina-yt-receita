from __future__ import annotations

import httpx

from maquina.providers.reais import _com_retry


def _resposta(status: int) -> httpx.Response:
    return httpx.Response(status, request=httpx.Request("GET", "https://x"))


def test_com_retry_sucesso_de_primeira(monkeypatch):
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)
    chamadas = [0]

    def chamar():
        chamadas[0] += 1
        return _resposta(200)

    r = _com_retry(chamar)
    assert r.status_code == 200
    assert chamadas[0] == 1


def test_com_retry_recupera_apos_429(monkeypatch):
    esperas = []
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: esperas.append(s))
    respostas = [429, 429, 200]
    chamadas = [0]

    def chamar():
        r = _resposta(respostas[chamadas[0]])
        chamadas[0] += 1
        return r

    r = _com_retry(chamar)
    assert r.status_code == 200
    assert chamadas[0] == 3
    assert esperas == [4.0, 8.0]


def test_com_retry_desiste_apos_esgotar_tentativas(monkeypatch):
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)
    chamadas = [0]

    def chamar():
        chamadas[0] += 1
        return _resposta(503)

    r = _com_retry(chamar, tentativas=3)
    assert r.status_code == 503
    assert chamadas[0] == 3


def test_com_retry_nao_repete_erro_definitivo(monkeypatch):
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: None)
    chamadas = [0]

    def chamar():
        chamadas[0] += 1
        return _resposta(401)

    r = _com_retry(chamar)
    assert r.status_code == 401
    assert chamadas[0] == 1
