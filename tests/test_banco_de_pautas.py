"""Banco de pautas: as quatro ideias que sobravam de cada ideacao.

`gerar_ideias` pede CINCO ideias numa chamada e o `auto` usava uma, jogando
quatro fora. Parecia gratuito e nao era: o Gemini do plano gratuito da 20
requisicoes por DIA, e cada video gasta uma na ideacao, uma no roteiro, ate duas
na extensao e mais uma no short companheiro. Com seis disparos diarios a cota
estoura — foi o que derrubou next-level-money em 12/08/2026 com HTTP 429.
"""

from __future__ import annotations

import pytest

from maquina.config import Config
from maquina.models import Formato, Ideia, Status
from maquina.pipeline import Pipeline


@pytest.fixture
def p(tmp_path, monkeypatch):
    cfg = Config.load(canal="nivel-do-jogo")
    cfg.data_dir = tmp_path
    cfg.llm_provider = "stub"
    cfg.tts_provider = "stub"
    cfg.image_provider = "stub"
    return Pipeline(cfg)


def _ideias(n: int, prefixo: str = "Pauta") -> list[Ideia]:
    return [Ideia(titulo=f"{prefixo} numero {i}", formato=Formato.LONGO) for i in range(n)]


def test_sobras_da_ideacao_ficam_guardadas(p):
    assert p.guardar_ideias(_ideias(4)) == 4
    assert len(p.store.listar(Status.IDEIA, limite=50)) == 4


def test_ideacao_repetida_nao_duplica(p):
    p.guardar_ideias(_ideias(4))
    assert p.guardar_ideias(_ideias(4)) == 0, "mesmo titulo, mesmo slug"


def test_a_rodada_seguinte_usa_a_pauta_guardada(p):
    p.guardar_ideias(_ideias(4))
    achada = p.ideia_guardada(Formato.LONGO)
    assert achada is not None
    assert achada.ideia.titulo.startswith("Pauta")


def test_pega_a_mais_antiga_primeiro(p):
    """Fila, nao pilha: pauta guardada nao pode envelhecer no fundo."""
    p.guardar_ideias(_ideias(3, "Antiga"))
    p.guardar_ideias(_ideias(3, "Nova"))

    achada = p.ideia_guardada(Formato.LONGO)

    assert "Antiga" in achada.ideia.titulo


def test_nao_pega_pauta_de_outro_formato(p):
    """Short e longo tem alvo de duracao e estrutura diferentes."""
    p.guardar_ideias(_ideias(3))
    assert p.ideia_guardada(Formato.SHORTS) is None


def test_nao_pega_pauta_de_outro_canal(p):
    """O sync traz a frota inteira para o SQLite deste canal.

    Sem o filtro, o disparo de um canal produziria a pauta de outro — em outro
    idioma e outro nicho.
    """
    p.guardar_ideias(_ideias(2))
    for v in p.store.listar(Status.IDEIA, limite=50):
        v.canal = "outro-canal"
        p.store.salvar(v)

    assert p.ideia_guardada(Formato.LONGO) is None


def test_banco_vazio_devolve_nada(p):
    assert p.ideia_guardada(Formato.LONGO) is None
