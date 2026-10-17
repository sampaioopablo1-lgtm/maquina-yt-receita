"""Zero `lengthSeconds` tem DUAS explicacoes, e a leitura sozinha nao separa.

Medido em 17/10 as 03:1x. O `kolejny-poziom-s049` (`O5o2SnovdEo`), publicado
dois minutos antes, devolveu 200 com 1.219.721 bytes e ZERO `lengthSeconds`.
Eu ia relatar "a peca ainda nao indexou", que e o caminho normal do 672/758.

O discriminador foi uma peca de CONTROLE: o `OhrGlJvnBoM`, da rodada anterior,
que havia lido **44 s** uma hora antes. Na mesma chamada ele tambem voltou
VAZIO — e peca de uma hora de vida nao desindexa. Logo o que mudou foi a ROTA,
e e a quinta linha da tabela de rotas do CLAUDE.md aparecendo de novo: 200,
pagina grande, cinco marcadores CONSENT, dois `captcha`, zero campo.

A consequencia que importa: NAO existe ponto de residuo nesta rodada, e isso
vai dito em vez de ser estimado.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import vivacidade_publica as vp

MEDIDO_03_1X = {"O5o2SnovdEo": None, "OhrGlJvnBoM": None}
CONTROLE_VALIA = 44  # lido as 02:1x, na rodada anterior
PAGINA_03_1X = {"http": 200, "bytes": 1219721, "lengthSeconds": 0,
                "CONSENT": 5, "captcha": 2}


def test_o_controle_vazio_acusa_a_ROTA_e_nao_a_peca():
    v = vp.veredito_da_rota(MEDIDO_03_1X["O5o2SnovdEo"],
                            MEDIDO_03_1X["OhrGlJvnBoM"], CONTROLE_VALIA)
    assert v == "rota_fechada"


def test_se_o_controle_RESPONDE_a_leitura_vazia_e_da_peca():
    """Contraprova no outro sentido: sem ela o veredito seria sempre o mesmo."""
    v = vp.veredito_da_rota(None, CONTROLE_VALIA, CONTROLE_VALIA)
    assert v == "peca_sem_leitura", "aqui o 672/758 se aplica, nao a rota"


def test_rota_aberta_e_peca_lida_da_ok():
    assert vp.veredito_da_rota(43, CONTROLE_VALIA, CONTROLE_VALIA) == "ok"


def test_controle_com_valor_DIFERENTE_nao_e_caso_previsto():
    """View nao desce e duracao nao muda: valor outro pede releitura, nao palpite."""
    assert vp.veredito_da_rota(43, 41, CONTROLE_VALIA) == "controle_divergente"


def test_a_pagina_media_200_e_GRANDE__o_codigo_nao_denuncia_nada():
    assert PAGINA_03_1X["http"] == 200
    assert PAGINA_03_1X["bytes"] > 1_000_000
    assert PAGINA_03_1X["lengthSeconds"] == 0
    assert PAGINA_03_1X["CONSENT"] >= 1 and PAGINA_03_1X["captcha"] >= 1


def test_o_relato_DIZ_que_nao_ha_ponto_de_residuo():
    r = vp.relato_da_rota(None, None, CONTROLE_VALIA, "O5o2SnovdEo")
    assert "FECHADA" in r
    assert "residuo" in r.lower(), "sem isso a rodada estima o residuo calada"


def test_o_relato_do_outro_ramo_manda_RELER_em_vez_de_acusar():
    r = vp.relato_da_rota(None, CONTROLE_VALIA, CONTROLE_VALIA, "X")
    assert "672" in r and "nao acuse" in r.lower()


def test_o_controle_do_dia_esta_NOMEADO_no_modulo():
    assert vp.CONTROLE_17_10 == ("OhrGlJvnBoM", 44)


def test_duracao_do_html_conta_o_CAMPO_e_nao_o_codigo():
    """A funcao que alimenta tudo isto nao pode ler 200 como leitura."""
    assert vp.duracao_do_html("x" * 1_200_000) is None
    assert vp.duracao_do_html('"lengthSeconds":"41" "lengthSeconds":"42"') == 42
