"""Corpo da requisicao de upload, sem tocar a rede.

O que se testa aqui nao e "a API respondeu" — e onde cada campo vai parar no
corpo. A divulgacao de conteudo sintetico e obrigatoria e o modo de falha dela e
silencioso: o campo no lugar errado nao levanta erro, so nao divulga nada.
"""

from __future__ import annotations

import pytest

from maquina.config import Config
from maquina.models import Formato, Roteiro, Cena, Video
from maquina.stages import youtube


class _Req:
    def __init__(self, registro: dict):
        self.registro = registro

    def next_chunk(self, num_retries=0):
        self.registro["num_retries"] = num_retries
        return None, {"id": "VIDEOID123"}


class _Videos:
    def __init__(self, registro: dict):
        self.registro = registro

    def insert(self, *, part, body, media_body):
        self.registro["part"] = part
        self.registro["body"] = body
        return _Req(self.registro)


class _Servico:
    def __init__(self, registro: dict):
        self.registro = registro

    def videos(self):
        return _Videos(self.registro)


@pytest.fixture
def upload(monkeypatch, tmp_path):
    registro: dict = {}
    monkeypatch.setattr(youtube, "_servico", lambda cfg, *a, **k: _Servico(registro))

    arquivo = tmp_path / "final.mp4"
    arquivo.write_bytes(b"\x00" * 1024)

    video = Video(
        slug="teste",
        formato=Formato.LONGO,
        video_path=str(arquivo),
        roteiro=Roteiro(
            titulo="Titulo",
            gancho="Gancho",
            cenas=[Cena(indice=0, narracao="Halo", prompt_visual="doodle")],
            descricao="d",
            tags=["gaji"],
        ),
    )
    return registro, video


def test_conteudo_sintetico_vai_no_status_do_insert(upload):
    """containsSyntheticMedia pertence ao schema VideoStatus. Em contentDetails
    (onde estava) a API ignora o campo e o canal publica sem divulgacao."""
    registro, video = upload
    assert video.conteudo_sintetico is True

    assert youtube.publicar(video, Config.load()) == "VIDEOID123"

    assert registro["body"]["status"]["containsSyntheticMedia"] is True
    assert "status" in registro["part"]
    assert "containsSyntheticMedia" not in registro["body"].get("contentDetails", {})


def test_upload_pede_retry_no_chunk(upload):
    """next_chunk() sem num_retries tenta uma vez so: um 502 transitorio perde
    o upload de um video ja produzido e revisado."""
    registro, video = upload
    youtube.publicar(video, Config.load())
    assert registro["num_retries"] >= 1
