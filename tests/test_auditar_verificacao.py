"""Ausencia de resposta nao e resposta.

Em 19/08/2026 dez dos doze tokens da frota estavam mortos. O
auditar_verificacao.py imprimia ERRO em dez linhas, contava apenas os
`eligible` e terminava com "0 canal(is) sem verificacao" e codigo 0 — um
atestado de saude para uma frota que ele nao conseguiu medir. Mesma familia do
defeito que deixou a auditoria de canal auditar zero sem ninguem perceber.

Estes testes trancam as duas metades: o que foi medido e o que NAO foi.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))

import auditar_verificacao as A  # noqa: E402


def _frota(monkeypatch, canais, estados):
    """Instala uma frota falsa. estados: slug -> 'allowed' | 'eligible' |
    outro valor da API | Exception (token morto)."""
    corrente = {}

    def tokens():
        for s in canais:
            corrente["slug"] = s          # marca quem esta sendo pedido agora
            yield (s, "rt", "cs")

    def _get(url, headers):
        e = estados[corrente["slug"]]
        if isinstance(e, Exception):
            raise e
        return {"items": [{"status": {"longUploadsStatus": e},
                           "statistics": {"subscriberCount": "1", "videoCount": "2"}}]}

    monkeypatch.setattr(A, "tokens", tokens)
    monkeypatch.setattr(A, "acesso", lambda rt, cs: "acc")
    monkeypatch.setattr(A, "_get", _get)


def test_token_morto_conta_como_nao_medido_e_nao_como_saudavel(monkeypatch, capsys):
    """O caso real: dez tokens mortos viravam silencio e o script saia 0."""
    _frota(monkeypatch, ["a", "b", "c"], {
        "a": "allowed",
        "b": Exception("400 Token has been expired or revoked"),
        "c": Exception("400 Token has been expired or revoked"),
    })
    codigo = A.main()
    saida = capsys.readouterr().out
    assert "2 NAO medido(s)" in saida, saida
    assert "NAO conseguiu medir" in saida
    assert codigo != 0, "frota nao medida nao pode sair com sucesso"


def test_estado_inesperado_nao_vira_verificado(monkeypatch, capsys):
    """`longUploadsUnspecified` e o que a API devolve quando NAO se pede com o
    token do proprio canal: parece medida e nao e."""
    _frota(monkeypatch, ["a"], {"a": "longUploadsUnspecified"})
    codigo = A.main()
    saida = capsys.readouterr().out
    assert "1 NAO medido(s)" in saida, saida
    assert codigo != 0


def test_frota_inteira_verificada_sai_limpa(monkeypatch, capsys):
    """O sucesso continua sendo sucesso — o teste anterior nao pode ter
    transformado o script num alarme que nunca cala."""
    _frota(monkeypatch, ["a", "b"], {"a": "allowed", "b": "allowed"})
    codigo = A.main()
    saida = capsys.readouterr().out
    assert "2 verificado(s), 0 sem verificacao, 0 NAO medido(s)" in saida, saida
    assert codigo == 0


def test_canal_sem_verificacao_continua_sendo_apontado(monkeypatch, capsys):
    _frota(monkeypatch, ["a", "b"], {"a": "allowed", "b": "eligible"})
    codigo = A.main()
    saida = capsys.readouterr().out
    assert "youtube.com/verify" in saida
    assert "1 sem verificacao" in saida
    assert codigo != 0
