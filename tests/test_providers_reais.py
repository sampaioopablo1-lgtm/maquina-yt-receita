from __future__ import annotations

import httpx

from maquina.providers.reais import ImagemPollinations, _com_retry


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


def test_pollinations_sobrevive_fila_cheia_alem_do_retry_padrao(monkeypatch, tmp_path):
    # Reproduz a falha real de 2026-08-11 20:54: "Queue full for IP" (429) por
    # mais tentativas do que o padrao generico (3) cobre. ImagemPollinations
    # precisa da janela estendida (5 tentativas) para sobreviver a isso.
    esperas = []
    monkeypatch.setattr("maquina.providers.reais.time.sleep", lambda s: esperas.append(s))
    respostas = [429, 429, 429, 429, 200]
    chamadas = [0]

    def get_falso(url, timeout=None, follow_redirects=None):
        status = respostas[chamadas[0]]
        chamadas[0] += 1
        r = httpx.Response(status, request=httpx.Request("GET", url), content=b"fake-png")
        return r

    monkeypatch.setattr("maquina.providers.reais.httpx.get", get_falso)

    saida = tmp_path / "cena.png"
    resultado = ImagemPollinations().gerar("um robo", saida, largura=1024, altura=1024)

    assert resultado == saida
    assert saida.read_bytes() == b"fake-png"
    assert chamadas[0] == 5
    assert esperas == [6.0, 12.0, 24.0, 48.0]
