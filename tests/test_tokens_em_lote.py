"""Reautorizar canal a canal, toda semana, e trabalho manual que a maquina cria.

Em 19/08/2026 o dono reclamou de ter reautorizado "o tempo todo" — tres
rodadas em dois dias. A causa raiz (app OAuth em modo Testing, aprendizado
303) ja foi tratada; o que sobrou era o CUSTO de cada rodada e a
DESCOBERTA tardia. Estes testes cercam as duas coisas:

  * `trocar` aceita varias URLs de uma vez, entao a rodada custa uma
    interacao em vez de nove;
  * `vigiar` roda no ciclo de 30 min, entao token morto aparece no log
    antes de custar um render.
"""
from __future__ import annotations

import ast
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import tokens as T  # noqa: E402

FONTE = (RAIZ / "fabrica" / "tokens.py").read_text(encoding="utf-8")
DIARIO = (RAIZ / ".github" / "workflows" / "diario.yml").read_text(encoding="utf-8")


def test_os_tres_comandos_existem():
    assert set(T.COMANDOS) == {"link", "trocar", "vigiar"}


def test_o_ciclo_vigia_os_tokens():
    assert "tokens.py vigiar" in DIARIO, (
        "o ciclo nao vigia os tokens — token morto voltaria a aparecer so "
        "no meio de um render")


def test_o_vigia_nao_derruba_o_ciclo():
    """Producao dos canais vivos nao pode parar porque um canal morreu."""
    trecho = DIARIO[DIARIO.index("tokens.py vigiar"):][:200]
    assert "||" in trecho, "sem `|| true`/`|| echo`, um token morto aborta o ciclo inteiro"


def test_trocar_le_varias_urls_do_stdin():
    """O ponto do lote: nove URLs coladas juntas, uma passada so."""
    corpo = FONTE[FONTE.index("def cmd_trocar"):FONTE.index("def cmd_vigiar")]
    assert "sys.stdin.read().splitlines()" in corpo
    assert "for url in urls" in corpo


def test_o_canal_e_descoberto_pela_api_nunca_assumido():
    """Um pacote inteiro ja foi para o canal errado por assumir destino."""
    corpo = FONTE[FONTE.index("def cmd_trocar"):FONTE.index("def cmd_vigiar")]
    assert "canal_do_token(" in corpo, "trocar nao pergunta a API de quem e o token"
    assert "SEM SLUG" in corpo, "sem canal correspondente, o token tem que ser recusado"


def test_escopos_sao_os_tres_que_a_maquina_usa():
    assert T.ESCOPOS == [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtube.upload",
    ], ("escopo a mais no refresh e o que produziu invalid_scope em todos os "
        "canais uma vez")


def test_pede_consentimento_para_receber_refresh_token():
    """Sem prompt=consent o Google devolve access_token e nenhum refresh."""
    assert '"prompt": "consent"' in FONTE


def test_o_modulo_compila():
    ast.parse(FONTE)


# ------------------------------------- a idade do token, que ninguem guardava

def test_a_data_de_emissao_e_gravada_na_troca():
    """`config.atualizado_em` so tem default `now()` no INSERT e a tabela nao
    tem trigger — o `trocar` grava por PATCH. Sem escrever a coluna a mao, as
    doze linhas continuariam dizendo 11/08 depois de reautorizacoes em 12/08 e
    18/08, e a idade do token, que e o unico numero que PREVE a morte, seria
    inventada."""
    assert "atualizado_em" in FONTE, (
        "a troca nao grava a data de emissao — o vigia nao tera idade nenhuma")
    corpo = FONTE[FONTE.index("def cmd_trocar"):]
    assert '"atualizado_em":' in corpo[:corpo.index("def cmd_vigiar")], (
        "atualizado_em existe no arquivo mas nao no corpo do PATCH da troca")


def test_o_vigia_le_a_coluna_de_data():
    assert "select=chave,valor,atualizado_em" in FONTE, (
        "sem a coluna no select, `_emitido` chega vazio e a idade some")


def test_token_emitido_em_testing_tem_morte_prevista():
    """O pavio de 7 dias e do token, nao do app: publicar o app nao ressuscita
    quem nasceu antes. O agla-level nasceu 11/08 22:04 e morreu 18/08 22:15 —
    onze minutos depois do marco que esta funcao calcula."""
    import datetime as dt
    _, morre = T._idade("2026-08-11T22:04:03+00:00")
    assert morre == dt.datetime(2026, 8, 18, 22, 4, 3, tzinfo=dt.timezone.utc)


def test_token_emitido_depois_da_publicacao_nao_tem_morte_prevista():
    _, morre = T._idade("2026-08-18T17:45:00+00:00")
    assert morre is None, (
        "token emitido depois de o app ir a producao nao expira em 7 dias")


def test_idade_ausente_nao_quebra_o_vigia():
    """Linha antiga sem data legivel nao pode derrubar a vigilancia inteira —
    o vigia roda a cada 30 min e e a unica fonte de verdade sobre a frota."""
    assert T._idade(None) == (None, None)
    assert T._idade("nao e uma data") == (None, None)


def test_o_vigia_avisa_de_quem_ainda_carrega_o_pavio():
    """Token VIVO emitido em Testing e o caso mais perigoso: passa no teste
    agora e morre no meio do dia. Tem de sair reautorizado JUNTO com os
    mortos, nao na proxima surpresa."""
    corpo = FONTE[FONTE.index("def cmd_vigiar"):]
    assert "condenados" in corpo and "pavio" in corpo


# ------------------- token vivo depois do marco: a DATA e que esta errada

def test_vivo_depois_do_marco_nao_e_condenado(monkeypatch, capsys):
    """Defeito meu, publicado em 19/08 e visto no log do ciclo das 19:01:

        VIVO  8.2d  epomeno-epipedo  <- emitido em modo Testing, morre 18/08

    Vivo hoje com morte prevista ontem: as duas metades da linha se
    contradizem. O Google cumpre o prazo de sete dias — se o token NAO morreu,
    entao ele nao nasceu quando a linha diz. A conclusao certa e que a data
    esta furada, nao que o token esta condenado.

    Custo do defeito: o vigia mandava reautorizar dois canais saudaveis,
    gastando consentimento do dono e refresh token contra o teto da conta.
    """
    monkeypatch.setattr(T, "_sb", lambda: ("https://x", "k"))
    monkeypatch.setattr(T, "tokens_do_banco", lambda sb, sk: {
        # emitido em modo Testing pela linha, mas VIVO muito depois do marco
        "epomeno-epipedo": {"_emitido": "2026-08-11T15:12:35+00:00"},
        # emitido depois da publicacao do app: sem pavio nenhum
        "novo-canal": {"_emitido": "2026-08-18T18:00:00+00:00"},
    })
    monkeypatch.setattr(T, "refrescar", lambda tok: ("ya29.acc", None))

    assert T.cmd_vigiar([]) == 0
    saida = capsys.readouterr().out

    assert "FURADA" in saida, saida
    assert "pavio de 7 dias aceso" not in saida, (
        "mandou reautorizar um canal vivo por causa de uma data velha")
    assert "morre 18/08" not in saida, "ainda anuncia morte que ja nao aconteceu"
    assert "nao reautorize por causa da data" in saida


def test_vivo_antes_do_marco_continua_condenado(monkeypatch, capsys):
    """O aviso legitimo nao pode sumir junto: token emitido em Testing que
    AINDA nao chegou ao marco tem pavio aceso de verdade."""
    import datetime as dt

    daqui_a_2d = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=5)
    monkeypatch.setattr(T, "_sb", lambda: ("https://x", "k"))
    monkeypatch.setattr(T, "PUBLICACAO_DO_APP",
                        (daqui_a_2d + dt.timedelta(days=1)).isoformat())
    monkeypatch.setattr(T, "tokens_do_banco", lambda sb, sk: {
        "com-pavio": {"_emitido": daqui_a_2d.isoformat()}})
    monkeypatch.setattr(T, "refrescar", lambda tok: ("ya29.acc", None))

    T.cmd_vigiar([])
    saida = capsys.readouterr().out
    assert "pavio de 7 dias aceso" in saida, saida
    assert "FURADA" not in saida
