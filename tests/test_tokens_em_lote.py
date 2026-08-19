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
