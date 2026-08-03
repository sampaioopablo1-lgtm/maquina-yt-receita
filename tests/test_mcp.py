"""Testes do servidor MCP, com providers offline."""

from __future__ import annotations

import asyncio
import json

import pytest

from maquina.mcp_server import mcp


def _texto(resultado) -> str:
    return resultado.content[0].text if resultado.content else ""


@pytest.fixture(autouse=True)
def ambiente_offline(tmp_path, monkeypatch):
    """Isola dados e força providers stub em todos os testes deste módulo."""
    for chave in ("LLM", "TTS", "IMAGE"):
        monkeypatch.setenv(f"MAQ_{chave}_PROVIDER", "stub")
    monkeypatch.setenv("MAQ_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("MAQ_OUT_DIR", str(tmp_path / "out"))


def _chamar(nome: str, args: dict | None = None) -> str:
    return _texto(asyncio.run(mcp.call_tool(nome, args or {})))


# ---------- registro ----------

def test_todas_ferramentas_registradas():
    tools = asyncio.run(mcp.list_tools())
    nomes = {t.name for t in tools}

    assert nomes == {
        "maquina_status",
        "maquina_listar_videos",
        "maquina_pesquisar_subnicho",
        "maquina_diagnosticar_video",
        "maquina_ler_comentarios",
        "maquina_revisar_roteiro",
        "maquina_gerar_ideias",
        "maquina_produzir_video",
        "maquina_publicar_video",
    }


def test_publicar_marcada_como_destrutiva():
    """Publicar é irreversível na prática — o cliente precisa saber disso."""
    tools = {t.name: t for t in asyncio.run(mcp.list_tools())}

    publicar = tools["maquina_publicar_video"].annotations
    assert publicar.destructive_hint is True
    assert publicar.read_only_hint is False

    # As de leitura não podem se anunciar como destrutivas.
    for nome in ("maquina_status", "maquina_listar_videos", "maquina_diagnosticar_video"):
        anot = tools[nome].annotations
        assert anot.read_only_hint is True
        assert anot.destructive_hint is False


def test_toda_ferramenta_tem_descricao():
    for t in asyncio.run(mcp.list_tools()):
        assert t.description and len(t.description) > 40, t.name


# ---------- comportamento ----------

def test_status_lista_pendencias_em_modo_offline():
    dados = json.loads(_chamar("maquina_status"))

    assert dados["canal"]["handle"] == "@SetiapLevelID"
    assert dados["providers_reais"] is False
    assert any("ANTHROPIC_API_KEY" in p for p in dados["pendencias"])


def test_listar_sem_videos_orienta_proximo_passo():
    saida = _chamar("maquina_listar_videos", {"params": {}})
    assert "maquina_produzir_video" in saida


def test_status_invalido_lista_opcoes_validas():
    """Erro acionável: dizer o que falhou não basta, tem que dizer o que serve."""
    saida = _chamar("maquina_listar_videos", {"params": {"status": "nao_existe"}})

    assert "invalido" in saida
    assert "publicado" in saida and "renderizado" in saida


def test_gerar_ideias_respeita_quantidade():
    dados = json.loads(
        _chamar("maquina_gerar_ideias", {"params": {"quantidade": 3, "formato_resposta": "json"}})
    )
    assert len(dados["ideias"]) == 3
    assert dados["eixo"]  # eixo da rotação sempre presente


def test_slug_inexistente_nao_quebra():
    for ferramenta in (
        "maquina_diagnosticar_video",
        "maquina_ler_comentarios",
        "maquina_revisar_roteiro",
    ):
        saida = _chamar(ferramenta, {"params": {"slug": "nao-existe"}})
        assert "Erro" in saida and "maquina_listar_videos" in saida


# ---------- proteção da publicação ----------

def test_publicar_sem_confirmar_nao_publica():
    """confirmar=false tem que simular, nunca publicar."""
    from maquina.config import Config
    from maquina.models import Formato, Ideia
    from maquina.pipeline import Pipeline

    cfg = Config.load()
    p = Pipeline(cfg)
    video = p.produzir(Ideia(titulo="Teste de protecao", formato=Formato.SHORTS))

    saida = _chamar("maquina_publicar_video", {"params": {"slug": video.slug}})
    dados = json.loads(saida)

    assert dados["simulacao"] is True
    assert "confirmar=true" in dados["para_publicar"]
    assert "publicado" not in dados

    # E o vídeo continua sem ID do YouTube — nada foi enviado.
    assert p.store.obter(video.slug).youtube_id is None


def test_publicar_video_inexistente():
    saida = _chamar("maquina_publicar_video", {"params": {"slug": "fantasma", "confirmar": True}})
    assert "Erro" in saida
