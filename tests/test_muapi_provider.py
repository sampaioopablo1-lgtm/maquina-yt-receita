"""ImagemMuapi (src/maquina/providers/muapi.py) fala o protocolo da Muapi e
entra na selecao de provider como os outros: sem chave, stub; com chave, real.
"""
from __future__ import annotations

import json

import httpx
import pytest

from maquina.config import Config
from maquina.providers import muapi as M
from maquina.providers import obter_imagem
from maquina.providers.base import ErroProvider


def _transport(respostas):
    def handler(req: httpx.Request) -> httpx.Response:
        respostas.append(req)
        assert req.headers.get("x-api-key") == "k"
        if req.url.path.endswith("/flux-schnell-image"):
            corpo = json.loads(req.content)
            assert corpo["width"] % 64 == 0 and corpo["height"] % 64 == 0
            return httpx.Response(200, json={"request_id": "r1"})
        if req.url.path.endswith("/predictions/r1/result"):
            n = sum(1 for r in respostas if r.url.path.endswith("/result"))
            if n == 1:
                return httpx.Response(503, text="fila")
            if n == 2:
                return httpx.Response(200, json={"status": "processing"})
            return httpx.Response(200, json={"status": "completed",
                                             "outputs": ["https://cdn/img.png"]})
        if req.url.host == "cdn":
            return httpx.Response(200, content=b"\x89PNG-fake")
        return httpx.Response(404, text=str(req.url))
    return httpx.MockTransport(handler)


def test_gera_imagem_via_submit_poll_download(tmp_path, monkeypatch):
    monkeypatch.setenv("MUAPI_API_KEY", "k")
    vistas: list[httpx.Request] = []
    g = M.ImagemMuapi("flux-schnell")
    g._api._cli = httpx.Client(base_url=M.BASE, headers={"x-api-key": "k"},
                               transport=_transport(vistas))
    g._api._dormir = lambda s: None
    saida = g.gerar("a desk", tmp_path / "c.png", largura=1280, altura=720)
    assert saida.read_bytes() == b"\x89PNG-fake"
    assert g.custo_usd > 0
    assert vistas[0].method == "POST"


def test_modelo_de_outro_provider_cai_no_padrao(monkeypatch):
    monkeypatch.setenv("MUAPI_API_KEY", "k")
    assert M.ImagemMuapi("gpt-image-1").modelo == M.MODELO_IMAGEM_PADRAO
    assert M.ImagemMuapi("nano-banana-2").modelo == "nano-banana-2"


def test_sem_chave_levanta_e_a_selecao_cai_no_stub(monkeypatch):
    monkeypatch.delenv("MUAPI_API_KEY", raising=False)
    with pytest.raises(ErroProvider):
        M.Muapi()
    cfg = Config()
    cfg.image_provider = "muapi"
    assert type(obter_imagem(cfg)).__name__ == "ImagemStub"


def test_com_chave_a_selecao_devolve_muapi(monkeypatch):
    monkeypatch.setenv("MUAPI_API_KEY", "k")
    cfg = Config()
    cfg.image_provider = "muapi"
    cfg.image_model = "seedream-5.0"
    g = obter_imagem(cfg)
    assert isinstance(g, M.ImagemMuapi) and g.modelo == "seedream-5.0"


def test_payload_por_catalogo():
    assert M.payload_imagem("flux-schnell", "x", 1280, 720) == {
        "prompt": "x", "width": 1280, "height": 704}
    assert M.payload_imagem("seedream-5.0", "x", 720, 1280) == {
        "prompt": "x", "aspect_ratio": "9:16"}
    # kling so aceita 16:9, 9:16 e 1:1 — 4:3 vira o mais proximo permitido
    assert M.proporcao(4, 3, ["16:9", "9:16", "1:1"]) == "1:1"


def test_falha_reportada_vira_erro_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("MUAPI_API_KEY", "k")

    def handler(req):
        if req.url.path.endswith("/result"):
            return httpx.Response(200, json={"status": "failed", "error": "moderado"})
        return httpx.Response(200, json={"request_id": "r9"})
    api = M.Muapi(dormir=lambda s: None)
    api._cli = httpx.Client(base_url=M.BASE, headers={"x-api-key": "k"},
                            transport=httpx.MockTransport(handler))
    with pytest.raises(ErroProvider, match="moderado"):
        api.gerar("nano-banana", {"prompt": "x"}, tmp_path / "x.png")
