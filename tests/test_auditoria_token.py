"""A auditoria de canal nao pode depender do token de UM canal.

Ela existe por um caso medido em 14/08/2026: o pacote resep-naik-level-002
inteiro foi publicado no canal errado, e isso nao aparece como falha em lugar
nenhum — aparece como pauta que nao pegou.

Em 19/08/2026 dez dos doze tokens morreram e a auditoria passou a estourar
traceback cru no PRIMEIRO canal, sem auditar nada. O comentario no codigo ja
dizia "o token de QUALQUER canal serve"; o codigo e que nao fazia isso.
Perder a conferencia em silencio e pior que o traceback.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))


def _fabrica_tokens(monkeypatch, vivos, registrar=None):
    """Instala um modulo `tokens` falso onde so `vivos` refrescam."""
    todos = {s: s for s in ("agla-level", "epomeno-epipedo", "kolejny-poziom",
                            "setiap-level")}
    falso = types.ModuleType("tokens")
    falso.tokens_do_banco = lambda sb, sk: todos

    def refrescar(slug):
        if registrar is not None:
            registrar.append(slug)
        return (f"ACC-{slug}", None) if slug in vivos else (None, "400 revoked")

    falso.refrescar = refrescar
    monkeypatch.setitem(sys.modules, "tokens", falso)


@pytest.fixture
def A(monkeypatch):
    import auditoria_canal
    monkeypatch.setattr(auditoria_canal, "_TOKENS", {}, raising=False)
    return auditoria_canal


def test_usa_o_token_do_proprio_canal_quando_ele_vive(A, monkeypatch):
    _fabrica_tokens(monkeypatch, vivos={"agla-level", "setiap-level"})
    assert A._algum_access_token("agla-level", "u", "k") == "ACC-agla-level"


def test_cai_em_qualquer_outro_token_quando_o_proprio_morreu(A, monkeypatch):
    """Era aqui que a auditoria morria: token proprio morto virava traceback."""
    _fabrica_tokens(monkeypatch, vivos={"kolejny-poziom"})
    assert A._algum_access_token("agla-level", "u", "k") == "ACC-kolejny-poziom"


def test_canal_sem_token_nenhum_no_banco_ainda_e_auditavel(A, monkeypatch):
    """`videos.list` e leitura publica — o canal auditado nem precisa ter token."""
    _fabrica_tokens(monkeypatch, vivos={"epomeno-epipedo"})
    assert A._algum_access_token("canal-sem-token", "u", "k") == "ACC-epomeno-epipedo"


def test_frota_inteira_morta_devolve_none_em_vez_de_estourar(A, monkeypatch):
    """None deixa o chamador dizer o que fazer; excecao derruba a auditoria toda."""
    _fabrica_tokens(monkeypatch, vivos=set())
    assert A._algum_access_token("agla-level", "u", "k") is None


def test_cada_token_refresca_no_maximo_uma_vez(A, monkeypatch):
    """Treze canais com um token vivo custam um refresh, nao treze — e era isso
    que a docstring prometia enquanto o cache guardava por CANAL."""
    feitos: list[str] = []
    _fabrica_tokens(monkeypatch, vivos={"setiap-level"}, registrar=feitos)
    for canal in ("agla-level", "epomeno-epipedo", "kolejny-poziom", "outro"):
        assert A._algum_access_token(canal, "u", "k") == "ACC-setiap-level"
    assert len(feitos) == len(set(feitos)), f"refresh repetido: {feitos}"
    assert set(feitos) <= {"agla-level", "epomeno-epipedo", "kolejny-poziom",
                           "setiap-level"}


def test_a_escolha_do_substituto_e_estavel(A, monkeypatch):
    """Ordem alfabetica: duas execucoes seguidas escolhem o MESMO substituto,
    senao o log da auditoria muda de causa sem nada ter mudado."""
    _fabrica_tokens(monkeypatch, vivos={"kolejny-poziom", "setiap-level"})
    primeiro = A._algum_access_token("agla-level", "u", "k")
    monkeypatch.setattr(A, "_TOKENS", {})
    assert A._algum_access_token("agla-level", "u", "k") == primeiro
