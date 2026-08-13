"""Ausencia nao pode se disfarcar de medida.

O painel de metricas trazia retencao, CTR, impressoes, duracao media, inscritos
e receita em ZERO nas 88 coletas — e nenhum desses numeros jamais foi medido.
Zero ali nao dizia "nao medimos": dizia "ninguem assiste nada", que e uma
acusacao contra o roteiro. Passei a semana lendo default como se fosse dado.

A causa: nenhum dos treze tokens carrega `yt-analytics.readonly`.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))
sys.path.insert(0, str(RAIZ / "src"))

import escopos as S  # noqa: E402
from maquina.models import Metricas  # noqa: E402

TRES_ESCOPOS = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
]


def test_metrica_nao_medida_e_none_e_nunca_zero():
    """A regressao que mais custou: default 0.0 virando conclusao.

    Se algum dia alguem devolver estes campos para 0.0, o painel volta a
    afirmar retencao zero por cento em video que ninguem mediu.
    """
    m = Metricas(youtube_id="abc123")
    assert m.retencao_media_pct is None
    assert m.ctr is None
    assert m.impressoes is None
    assert m.duracao_media_s is None
    assert m.inscritos_ganhos is None
    assert m.receita_estimada_usd is None


def test_views_continua_com_zero_porque_e_medido_de_verdade():
    """`views` vem da Data API, que os tokens alcancam. Zero ali e medida."""
    assert Metricas(youtube_id="abc123").views == 0


def test_retencao_zero_de_verdade_sobrevive():
    """Nulo e ausencia; zero continua sendo um valor legitimo quando medido."""
    m = Metricas(youtube_id="abc123", retencao_media_pct=0.0)
    assert m.retencao_media_pct == 0.0 and m.retencao_media_pct is not None


def test_token_sem_escopo_de_analytics_e_reprovado():
    est = S.avalia({"agla-level": {"scopes": TRES_ESCOPOS}})
    assert est["agla-level"]["publica"] is True
    assert est["agla-level"]["mede_retencao"] is False


def test_token_com_escopo_de_analytics_passa():
    est = S.avalia({"x": {"scopes": TRES_ESCOPOS + [S.ANALYTICS]}})
    assert est["x"]["mede_retencao"] is True


def test_relatorio_nomeia_os_canais_que_faltam_e_o_conserto():
    """Relatorio que diz "faltou escopo" sem dizer QUAL canal e O QUE fazer
    manda a pessoa cacar a informacao — e ela nao caca."""
    texto = S.relatorio({
        "agla-level": {"scopes": TRES_ESCOPOS},
        "sx-educacao": {"scopes": TRES_ESCOPOS + [S.ANALYTICS]},
    })
    assert "agla-level" in texto
    assert "auth-youtube" in texto
    assert "1 de 2 canais NAO medem" in texto


def test_relatorio_liga_o_escopo_a_consequencia():
    """Nome de permissao nao explica nada. O relatorio tem que dizer que sem
    isso qualquer teste visual e cego."""
    texto = S.relatorio({"a": {"scopes": TRES_ESCOPOS}})
    assert "retencao" in texto and "cegas" in texto


def test_tudo_certo_tambem_e_dito():
    texto = S.relatorio({"a": {"scopes": TRES_ESCOPOS + [S.ANALYTICS]}})
    assert "Todos os canais medem retencao" in texto
