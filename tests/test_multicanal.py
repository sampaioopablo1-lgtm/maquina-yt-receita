"""Portfolio multi-canal: cada canal carrega identidade e estado isolados."""

from __future__ import annotations

import pytest

from maquina.config import ROOT, Config


def test_canal_padrao_continua_setiap_level():
    cfg = Config.load()
    assert cfg.canal.nome == "Setiap Level"
    assert cfg.canal.estilo_visual == "doodle"
    assert cfg.data_dir == ROOT / "data"


def test_canal_do_portfolio_sobrepoe_e_isola_estado():
    cfg = Config.load(canal="kolejny-poziom")
    assert cfg.canal.nome == "Kolejny Poziom"
    assert cfg.canal.idioma == "pl"
    assert cfg.canal.estilo_visual == "voxlite"
    assert cfg.canal.voz_edge == "pl-PL-MarekNeural"
    # Estado separado: similaridade e teto diario sao por canal.
    assert cfg.data_dir == ROOT / "data" / "kolejny-poziom"
    assert cfg.out_dir == ROOT / "out" / "kolejny-poziom"
    assert cfg.yt_token.name == "youtube_token_kolejny-poziom.json"
    # Limites de compliance vem do default e continuam valendo.
    assert cfg.publicacao.max_por_dia == 6


def test_canal_inexistente_falha_alto():
    with pytest.raises(FileNotFoundError):
        Config.load(canal="canal-fantasma")


def test_todos_os_canais_do_portfolio_carregam():
    canais = sorted(p.stem for p in (ROOT / "config" / "canais").glob("*.yaml"))
    # Contagem minima, nao fixa: cada novo YAML de canal ja derrubou o CI tres
    # vezes (seja-mais-magra, labtreinamento, sx-educacao) por travar um numero
    # exato aqui. O que importa e que o portfolio carregue, nao quantos sao.
    assert len(canais) >= 13
    vozes = set()
    for slug in canais:
        cfg = Config.load(canal=slug)
        assert cfg.canal.estilo_visual in {"doodle", "voxlite"}
        assert cfg.canal.voz_edge
        vozes.add(cfg.canal.voz_edge)
    # Identidades distintas: nenhuma voz repetida no portfolio (anti-rede).
    assert len(vozes) == len(canais)
