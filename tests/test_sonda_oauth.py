"""A sonda pode errar de duas formas, e UMA delas é vazar segredo.

POR QUE ISTO EXISTE. `fabrica/sonda_oauth.py` nasceu em 11/10 para responder se
o runner publica sem o Supabase, e para isso ela precisa LER
`YT_OAUTH_JSON` — client_id, client_secret e refresh_token dos três canais. A
trava da rotina é absoluta: **nunca imprima refresh token.** Uma sonda que
imprime o que leu transforma o log de um workflow publico num vazamento.

Essa propriedade regride em SILENCIO: um `print(cfg)` de depuracao passa em
qualquer teste funcional e nao quebra nada visivel. Entao o teste central aqui
nao e "a sonda funciona" — e **"a sonda nao vaza"**, com sentinelas que seriam
obvias na saida.

O segundo grupo de testes cobre o que ela precisa ACERTAR para servir de
conferencia depois que o dono colar o segredo: distinguir ausente de presente,
refresh vivo de revogado, e dizer QUAIS escopos vieram — porque e o escopo que
decide se o longo sobe com legenda (`force-ssl`) e se a retencao volta
(`yt-analytics.readonly`).
"""

from __future__ import annotations

import io
import json
import sys
import urllib.error
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import sonda_oauth as S  # noqa: E402

# Sentinelas que ninguem confundiria com outra coisa numa saida de log.
SEGREDOS = {
    "client_secret": "SEGREDO-CLIENT-NAO-PODE-SAIR",
    "refresh_token": "SEGREDO-REFRESH-NAO-PODE-SAIR",
    "access_token": "SEGREDO-ACCESS-NAO-PODE-SAIR",
}

MAPA = {canal: {"client_id": f"id-de-{canal}",
                "client_secret": SEGREDOS["client_secret"],
                "refresh_token": SEGREDOS["refresh_token"]}
        for canal in S.FROTA}


def _liga(monkeypatch, resposta=None, erro=None):
    """Troca o urlopen por um que NAO vai à rede."""
    def falso(req, timeout=0):
        if erro is not None:
            raise erro
        return io.BytesIO(json.dumps(resposta).encode())
    monkeypatch.setattr(S.urllib.request, "urlopen", falso)


def test_a_sonda_NAO_VAZA_segredo_nenhum(monkeypatch, capsys):
    """O teste que mais importa. Se algum dia alguem puser um print de
    depuracao, ele cai aqui — e nao no log de um workflow."""
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(MAPA))
    _liga(monkeypatch, resposta={
        "access_token": SEGREDOS["access_token"],
        "scope": "https://www.googleapis.com/auth/youtube.upload "
                 "https://www.googleapis.com/auth/youtube.force-ssl"})

    S.main()
    saida = capsys.readouterr().out
    assert saida, "a sonda nao imprimiu nada — ela deixou de ser instrumento"
    for nome, valor in SEGREDOS.items():
        assert valor not in saida, f"A SONDA VAZOU {nome}"


def test_so_sai_presenca_e_contagem_de_caracteres(monkeypatch, capsys):
    """Contagem de caracteres é informação segura e necessária: distingue
    segredo ausente de segredo colado pela metade."""
    monkeypatch.setenv("YT_OAUTH_JSON", "")
    for canal in S.FROTA:
        monkeypatch.setenv("YT_TOKEN_" + canal.upper().replace("-", "_"), "")
    S.main()
    saida = capsys.readouterr().out
    assert "YT_OAUTH_JSON: AUSENTE (0 chars)" in saida
    assert "a rota sem banco depende deste segredo" in saida


def test_refresh_revogado_vai_NOMEADO_com_o_motivo(monkeypatch, capsys):
    """`invalid_grant` é token revogado e NÃO é cliente errado (667). A sonda
    tem de passar o motivo adiante, senão o dono recola o mesmo segredo morto."""
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(MAPA))
    corpo = json.dumps({"error": "invalid_grant",
                        "error_description": "Token has been expired or revoked."})
    _liga(monkeypatch, erro=urllib.error.HTTPError(
        "https://oauth2.googleapis.com/token", 400, "Bad Request", {},
        io.BytesIO(corpo.encode())))

    S.main()
    saida = capsys.readouterr().out
    assert "refresh FALHOU" in saida and "invalid_grant" in saida
    assert "nenhum canal da frota refresca" in saida
    for valor in SEGREDOS.values():
        assert valor not in saida, "vazou no caminho de ERRO"


def test_diz_quais_escopos_vieram_porque_e_o_escopo_que_decide(monkeypatch, capsys):
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(MAPA))
    _liga(monkeypatch, resposta={
        "access_token": SEGREDOS["access_token"],
        "scope": "https://www.googleapis.com/auth/youtube.upload "
                 "https://www.googleapis.com/auth/yt-analytics.readonly"})
    S.main()
    saida = capsys.readouterr().out
    assert "upload=sim" in saida
    assert "force-ssl=NAO" in saida      # o longo subiria sem legenda
    assert "analytics=sim" in saida      # a retencao voltaria
    assert "PUBLICACAO SEM BANCO possivel em" in saida


def test_canal_fora_do_mapa_e_denunciado(monkeypatch, capsys):
    """Segredo com um canal bom e outro faltando é o caso realista de colagem
    parcial, e passar batido seria pior que falhar."""
    parcial = {"labtreinamento": MAPA["labtreinamento"]}
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(parcial))
    _liga(monkeypatch, resposta={"access_token": SEGREDOS["access_token"],
                                 "scope": "youtube.upload youtube.force-ssl"})
    S.main()
    saida = capsys.readouterr().out
    assert "epomeno-epipedo: FORA do YT_OAUTH_JSON" in saida
    assert "kolejny-poziom: FORA do YT_OAUTH_JSON" in saida
    assert "labtreinamento: refresh OK" in saida


def test_entrada_incompleta_nao_vira_chamada_a_rede(monkeypatch, capsys):
    """Sem `refresh_token` não há o que refrescar: tem de dizer o que falta em
    vez de estourar um KeyError dentro do runner."""
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(
        {"labtreinamento": {"client_id": "x", "client_secret": "y"}}))

    def nunca(req, timeout=0):
        raise AssertionError("chamou a rede com entrada incompleta")
    monkeypatch.setattr(S.urllib.request, "urlopen", nunca)

    S.main()
    saida = capsys.readouterr().out
    assert "entrada incompleta, falta refresh_token" in saida


def test_json_invalido_nao_derruba_o_job(monkeypatch, capsys):
    """A sonda sai VERDE de propósito: "o segredo está torto" é resposta, não
    falha de infraestrutura, e vermelho recorrente deixa de ser sinal."""
    monkeypatch.setenv("YT_OAUTH_JSON", "isto nao e json")
    assert S.main() == 0
    assert "nao e JSON valido" in capsys.readouterr().out
