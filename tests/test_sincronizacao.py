"""Sincronizacao com o Supabase, contra um PostgREST falso em localhost.

Sem servidor de verdade nao da para afirmar que o corpo, os headers e o
on_conflict estao certos — e um upsert com conflito errado duplica linha em
producao em vez de atualizar.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from maquina.models import Cena, Formato, Metricas, Roteiro, Status, Video
from maquina.sincronizacao import empurrar, puxar
from maquina.storage import Store

RECEBIDO: list[dict] = []
REMOTO: list[dict] = []


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silencia o log do http.server
        pass

    def do_POST(self):
        corpo = self.rfile.read(int(self.headers["Content-Length"]))
        RECEBIDO.append(
            {
                "path": self.path,
                "prefer": self.headers.get("Prefer", ""),
                "apikey": self.headers.get("apikey", ""),
                "linhas": json.loads(corpo),
            }
        )
        self.send_response(201)
        self.end_headers()

    def do_GET(self):
        corpo = json.dumps(REMOTO).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


@pytest.fixture
def servidor(monkeypatch):
    RECEBIDO.clear()
    REMOTO.clear()
    srv = HTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    monkeypatch.setenv("SUPABASE_URL", f"http://127.0.0.1:{srv.server_port}")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "chave-de-teste")
    yield srv
    srv.shutdown()


def _video(slug: str, **kw) -> Video:
    return Video(
        slug=slug,
        formato=Formato.LONGO,
        roteiro=Roteiro(
            titulo="Titulo",
            gancho="Gancho",
            cenas=[Cena(indice=0, narracao="Halo dunia", prompt_visual="doodle")],
        ),
        **kw,
    )


def test_empurrar_envia_upsert_com_conflito_certo(servidor, tmp_path):
    store = Store(tmp_path / "t.db")
    store.salvar(_video("um", youtube_id="ABC", status=Status.PUBLICADO))
    store.salvar_metricas(Metricas(youtube_id="ABC", views=10, impressoes=800, ctr=0.06))

    assert empurrar(store) == (1, 1)

    videos, metricas = RECEBIDO
    assert videos["path"] == "/rest/v1/videos?on_conflict=slug"
    assert "resolution=merge-duplicates" in videos["prefer"]
    assert videos["apikey"] == "chave-de-teste"
    assert videos["linhas"][0]["slug"] == "um"
    # roteiro precisa ir como objeto (coluna jsonb), nao como string.
    assert videos["linhas"][0]["roteiro"]["cenas"][0]["narracao"] == "Halo dunia"

    assert metricas["path"] == "/rest/v1/metricas?on_conflict=youtube_id%2Ccoletado_em"
    assert metricas["linhas"][0]["views"] == 10


def test_empurrar_descarta_metrica_sem_video_no_lote(servidor, tmp_path):
    """metricas.youtube_id tem FK para videos.youtube_id: mandar orfa derruba o job."""
    store = Store(tmp_path / "t.db")
    store.salvar(_video("um"))  # sem youtube_id
    store.salvar_metricas(Metricas(youtube_id="ORFAO", views=3))

    assert empurrar(store) == (1, 0)
    assert [r["path"] for r in RECEBIDO] == ["/rest/v1/videos?on_conflict=slug"]


def test_puxar_traz_roteiro_da_edge_function(servidor, tmp_path):
    store = Store(tmp_path / "t.db")
    REMOTO.append(
        {
            "slug": "gaji-abc123",
            "status": "roteirizado",
            "formato": "longo",
            "titulo": "7 Level Gaji",
            "youtube_id": None,
            "duracao_s": None,
            "custo_usd": 0,
            "erro": None,
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "publicado_em": None,
            "agendado_para": None,
            "roteiro": {
                "titulo": "7 Level Gaji",
                "gancho": "Gancho",
                "cenas": [
                    {
                        "indice": 0,
                        "narracao": "Halo",
                        "prompt_visual": "doodle",
                        "audio_path": None,
                        "imagem_path": None,
                        "duracao_s": None,
                    }
                ],
                "descricao": "d",
                "tags": ["gaji"],
                "prompt_thumbnail": "p",
                "texto_thumbnail": "GAJI",
            },
        }
    )

    assert puxar(store) == ["gaji-abc123"]
    salvo = store.obter("gaji-abc123")
    assert salvo.status is Status.ROTEIRIZADO
    assert salvo.roteiro.cenas[0].narracao == "Halo"


def test_puxar_nao_sobrescreve_trabalho_local(servidor, tmp_path):
    store = Store(tmp_path / "t.db")
    store.salvar(_video("gaji-abc123", status=Status.RENDERIZADO))
    REMOTO.append(
        {
            "slug": "gaji-abc123",
            "status": "roteirizado",
            "formato": "longo",
            "titulo": "outro",
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "roteiro": {"titulo": "outro", "gancho": "g", "cenas": []},
        }
    )

    assert puxar(store) == []
    assert store.obter("gaji-abc123").status is Status.RENDERIZADO
