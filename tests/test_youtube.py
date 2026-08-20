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


# --- coleta: ausencia de linha nao e linha de zeros ------------------------


class _Relatorios:
    """Analytics falso. `linhas` None simula o periodo sem nada a reportar."""

    def __init__(self, linhas):
        self.linhas = linhas

    def query(self, **kwargs):
        pedido = kwargs.get("metrics", "")
        if "estimatedRevenue" in pedido or "impressions" in pedido:
            raise RuntimeError("sem escopo — e o caso normal fora do YPP")
        resp = {} if self.linhas is None else {"rows": [self.linhas]}
        return _Execucao(resp)


class _Execucao:
    def __init__(self, resp):
        self.resp = resp

    def execute(self):
        return self.resp


class _Analytics:
    def __init__(self, linhas):
        self.linhas = linhas

    def reports(self):
        return _Relatorios(self.linhas)


def _coleta(monkeypatch, linhas):
    monkeypatch.setattr(youtube, "_servico", lambda *a, **k: _Analytics(linhas))
    return youtube.coletar_metricas(Config(), "VID123")


def test_analytics_sem_linha_grava_ausencia_e_nao_zero(monkeypatch):
    """O defeito que poluiu 1.773 das 1.932 linhas de `metricas`.

    `rows` vazio quer dizer "nada a reportar", e a versao anterior substituia
    isso por uma linha de zeros. Zero em retencao nao e ausencia de medida: e
    a afirmacao de que ninguem assistiu — uma acusacao contra o roteiro, feita
    por um relatorio que nunca existiu.
    """
    m = _coleta(monkeypatch, None)
    assert m.retencao_media_pct is None
    assert m.duracao_media_s is None
    assert m.inscritos_ganhos is None


def test_analytics_com_linha_de_zero_grava_o_zero(monkeypatch):
    """O outro lado, que importa tanto quanto: quando o relatorio EXISTE e diz
    zero, zero e medida e tem de ser gravado."""
    m = _coleta(monkeypatch, [0, 0, 0.0, 0.0, 0])
    assert m.views == 0
    assert m.retencao_media_pct == 0.0
    assert m.duracao_media_s == 0.0


def test_analytics_com_numeros_preserva_os_numeros(monkeypatch):
    m = _coleta(monkeypatch, [292, 58, 12.0, 33.0, 4])
    assert (m.views, m.duracao_media_s, m.retencao_media_pct,
            m.inscritos_ganhos) == (292, 12.0, 33.0, 4)
