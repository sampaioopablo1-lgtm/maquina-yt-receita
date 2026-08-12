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
    assert len(canais) == 13
    vozes = []
    for slug in canais:
        cfg = Config.load(canal=slug)
        assert cfg.canal.estilo_visual in {"doodle", "voxlite"}
        assert cfg.canal.voz_edge
        vozes.append(cfg.canal.voz_edge)
    # Identidades distintas: voz repetida entre canais le como rede (anti-rede).
    #
    # EXCECAO UNICA E DOCUMENTADA: o edge-tts oferece tres vozes pt-BR e o
    # portfolio tem quatro canais pt-BR, entao a quarta identidade nao existe
    # para sortear — sx-educacao repete o pt-BR-AntonioNeural do nivel-do-jogo
    # ate a voz clonada do Pablo entrar. Qualquer OUTRA repeticao e defeito, e
    # e por isso que este teste compara o conjunto em vez de contar.
    repetidas = {v for v in vozes if vozes.count(v) > 1}
    assert repetidas == {"pt-BR-AntonioNeural"}
