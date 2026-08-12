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


def _linha_da_fabrica(slug: str, **kw) -> dict:
    """Linha como a fabrica/ grava: `roteiro` e um saco de metricas, nao um Roteiro.

    Nao e hipotetico — 23 das 30 linhas da tabela em 12/08/2026 eram assim.
    """
    linha = {
        "slug": slug,
        "status": "publicado",
        "formato": "longo",
        "titulo": "Nadplacac Kredyt czy Inwestowac",
        "youtube_id": "MjI4ZGJAhIo",
        "canal": "kolejny-poziom",
        "duracao_s": 686.6,
        "custo_usd": 0,
        "erro": None,
        "criado_em": datetime.now(timezone.utc).isoformat(),
        "publicado_em": datetime.now(timezone.utc).isoformat(),
        "agendado_para": None,
        "roteiro": {"mb": 29, "lufs": -14.1, "cenas": 57},
    }
    linha.update(kw)
    return linha


def test_puxar_resgata_linha_da_fabrica_em_vez_de_descartar(servidor, tmp_path):
    """Descartar essas linhas cegava a compliance.

    Num runner novo o SQLite nasce vazio e e o puxar que enche a janela usada
    por publicados_hoje, titulos_publicados e a checagem de similaridade. Com
    a maioria das linhas caindo fora, as tres barreiras anti-spam decidiam
    sobre um setimo do historico real.
    """
    store = Store(tmp_path / "t.db")
    REMOTO.append(_linha_da_fabrica("kolejny-poziom-007"))

    assert puxar(store) == ["kolejny-poziom-007"]
    salvo = store.obter("kolejny-poziom-007")
    assert salvo.status is Status.PUBLICADO
    assert salvo.roteiro.titulo == "Nadplacac Kredyt czy Inwestowac"
    # Sem cenas: a similaridade compara texto vazio e nao acusa falso positivo.
    assert salvo.roteiro.cenas == []
    # O canal precisa sobreviver, senao o teto por canal nao consegue separar.
    assert salvo.canal == "kolejny-poziom"
    assert "Nadplacac Kredyt czy Inwestowac" in store.titulos_publicados()
    assert store.publicados_hoje_canal("kolejny-poziom") == 1


def test_puxar_nao_resgata_roteirizado(servidor, tmp_path):
    """Roteiro sem cenas nao pode virar candidato de `maquina auto`.

    Linhas em `roteirizado` existem para serem RETOMADAS. Um Roteiro
    reconstruido so com titulo produziria um video sem uma unica cena.
    """
    store = Store(tmp_path / "t.db")
    REMOTO.append(_linha_da_fabrica("meio-do-caminho", status="roteirizado"))

    assert puxar(store) == []
    assert store.obter("meio-do-caminho") is None


def test_puxar_preserva_canal_da_linha_valida(servidor, tmp_path):
    store = Store(tmp_path / "t.db")
    REMOTO.append(
        {
            "slug": "com-canal",
            "status": "publicado",
            "formato": "longo",
            "titulo": "t",
            "canal": "labtreinamento",
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "publicado_em": datetime.now(timezone.utc).isoformat(),
            "roteiro": {"titulo": "t", "gancho": "g", "cenas": []},
        }
    )

    assert puxar(store) == ["com-canal"]
    assert store.obter("com-canal").canal == "labtreinamento"


def test_empurrar_separa_lotes_por_presenca_de_canal(servidor, tmp_path):
    """PostgREST recusa um POST em massa com chaves diferentes entre as linhas.

    `canal` so entra na linha quando existe, para nao sobrescrever com NULL o
    que o Supabase ja tem. Misturado num lote so, o PostgREST devolve
    PGRST102 "All object keys must match" e derruba o job — medido no run
    31630852095, que morreu no primeiro passo.
    """
    store = Store(tmp_path / "t.db")
    store.salvar(_video("com", canal="labtreinamento"))
    store.salvar(_video("sem"))

    assert empurrar(store) == (2, 0)

    lotes = [r["linhas"] for r in RECEBIDO if r["path"].startswith("/rest/v1/videos")]
    assert len(lotes) == 2
    for lote in lotes:
        assert len({frozenset(linha) for linha in lote}) == 1
    assert {linha["slug"] for lote in lotes for linha in lote} == {"com", "sem"}


def test_linha_resgatada_nunca_volta_para_o_supabase(servidor, tmp_path):
    """Mao unica: o resgate le, nao devolve.

    O Roteiro reconstruido tem titulo e nada mais. Empurrar isso sobrescreveria
    o blob original da linha — nas linhas da fabrica/ ele e a UNICA copia de
    fonte_pauta (peer group, outlier, dado ancora), da trilha e dos IDs do
    Drive. Um puxar seguido de empurrar apagaria tudo isso em silencio.
    """
    store = Store(tmp_path / "t.db")
    REMOTO.append(_linha_da_fabrica("kp-emerytura-zus-34"))
    assert puxar(store) == ["kp-emerytura-zus-34"]
    assert store.obter("kp-emerytura-zus-34").resgatado is True

    RECEBIDO.clear()
    store.salvar(_video("produzido-aqui", canal="kolejny-poziom"))

    assert empurrar(store) == (1, 0)
    enviados = {
        linha["slug"]
        for r in RECEBIDO
        if r["path"].startswith("/rest/v1/videos")
        for linha in r["linhas"]
    }
    assert enviados == {"produzido-aqui"}
