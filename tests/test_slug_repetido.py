"""Slug repetido no banco nao pode deixar video publicado fora do registro.

Medido em 18/08/2026, run 32096226460. O epomeno-epipedo-003 subiu inteiro —
short, longo, thumbnail, legenda, tudo verde — e o `registrar()` levou 409:
uma rodada de 11/08, cuja spec nunca entrou no repositorio, ja tinha usado o
slug `epomeno-epipedo-003` para OUTRO video. Resultado: video no ar e zero
linhas em `videos`, exatamente a cegueira que o registrar() existe para
impedir — as travas anti-duplicata consultam o banco e nao enxergam o que
nao foi registrado.

Duas licoes viram teste:

  1. O registrar reenvia com slug sufixado em vez de desistir. O slug e so a
     identidade da LINHA; quem deduplica producao e (pacote, titulo).

  2. So 409 ganha esse tratamento. Qualquer outro HTTPError continua caindo
     no aviso com SQL pronto, porque reenviar as cegas sobre um 500 e como
     esconder um erro de servidor atras de uma segunda tentativa.

A licao de NUMERACAO (o proximo numero de spec sai da uniao repo+banco, nao
so do repo) vive no aprendizado 298 do banco — teste local nao tem rede para
impor isso.
"""

from __future__ import annotations

import io
import json
import sys
import types
import urllib.error
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import publicar as P  # noqa: E402


SP = {"slug": "canal-x", "pacote": "canal-x-003",
      "longo": [{"nar": "a"}], "short": [{"nar": "b"}]}
CP = {"titulo": "Titulo", "descricao": "0:00 Abertura"}
SAIDA = {"longo": "LONGO_ID", "short": "SHORT_ID"}


def _http_error(code):
    return urllib.error.HTTPError("u", code, "conflict", {}, io.BytesIO(b""))


def _roda(monkeypatch, respostas):
    """`respostas` e uma lista de excecoes (ou None) por chamada a _req."""
    chamadas = []

    def falso_req(url, data=None, method=None, headers=None):
        chamadas.append({"url": url, "corpo": data and json.loads(data)})
        r = respostas.pop(0) if respostas else None
        if r:
            raise r
        return io.BytesIO(b"[]")

    monkeypatch.setattr(P, "_req", falso_req)
    monkeypatch.setattr(P, "_duracao", lambda d, sp: (777.0, 42.0))
    P.registrar(SAIDA, SP, CP, "/tmp/x", "canal-x", "http://sb", "chave")
    return chamadas


def test_409_reenvia_com_slug_sufixado(monkeypatch):
    chamadas = _roda(monkeypatch, [_http_error(409)])
    inserts = [c for c in chamadas if c["url"].endswith("/videos")]
    assert len(inserts) == 2, "esperava o insert original e o reenvio"
    slugs = sorted(l["slug"] for l in inserts[1]["corpo"])
    assert slugs == ["canal-x-003-r2", "canal-x-003-short-r2"], slugs


def test_o_reenvio_preserva_os_ids_do_youtube(monkeypatch):
    """Mudar o slug nao pode tocar em mais nada: o resto da linha e o video."""
    chamadas = _roda(monkeypatch, [_http_error(409)])
    corpo = [c for c in chamadas if c["url"].endswith("/videos")][1]["corpo"]
    assert {l["youtube_id"] for l in corpo} == {"LONGO_ID", "SHORT_ID"}
    assert all(l["pacote"] == "canal-x-003" for l in corpo)


def test_outros_erros_nao_ganham_reenvio(monkeypatch):
    """500 vira aviso com SQL na mao, como sempre — nunca segunda tentativa."""
    chamadas = _roda(monkeypatch, [_http_error(500)])
    inserts = [c for c in chamadas if c["url"].endswith("/videos")]
    assert len(inserts) == 1


def test_sem_conflito_nada_muda(monkeypatch):
    chamadas = _roda(monkeypatch, [])
    inserts = [c for c in chamadas if c["url"].endswith("/videos")]
    assert len(inserts) == 1
    assert all(not l["slug"].endswith("-r2") for l in inserts[0]["corpo"])
    # e o canais ainda e atualizado
    assert any("/canais" in c["url"] for c in chamadas)


def test_registrar_continua_sem_levantar(monkeypatch):
    """A garantia antiga permanece: com o video ja no ar, registrar jamais
    explode — nem quando ate o reenvio falha."""
    _roda(monkeypatch, [_http_error(409), _http_error(409)])
