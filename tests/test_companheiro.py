"""O short que leva publico ao longo.

A regra mestra da rotina pede pacote — longo E short — e o caminho automatico
sempre entregou um video sozinho. O custo estava medido em 12/08/2026: longo
publicado sem short faz 0,14 view/dia contra 22,97 do short, mesmo canal, mesma
semana. Em canal frio o feed de Shorts entrega e o de longos nao — o longo nao e
o produto que falha, e o produto que ninguem alcanca.
"""

from __future__ import annotations

import json

import pytest

from maquina.config import Config
from maquina.models import Cena, Formato, Roteiro
from maquina.stages import roteiro as R


class LLMDeShort:
    def __init__(self, n_cenas: int = 5, chars_por_cena: int = 110):
        self.n_cenas = n_cenas
        self.chars_por_cena = chars_por_cena
        self.prompts: list[str] = []

    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str:
        self.prompts.append(prompt)
        return json.dumps({
            "titulo": "O erro que custa caro",
            "gancho": "Voce esta perdendo dinheiro agora",
            "cenas": [
                {"narracao": "a" * self.chars_por_cena, "prompt_visual": "vertical doodle"}
                for _ in range(self.n_cenas)
            ],
            "descricao": "Descricao do short",
            "tags": ["curto"],
            "prompt_thumbnail": "p",
            "texto_thumbnail": "ERRO",
        })


@pytest.fixture
def cfg():
    return Config.load(canal="nivel-do-jogo")


def _longo() -> Roteiro:
    return Roteiro(
        titulo="Por Que a Inflacao nos Games E Mais Perigosa",
        gancho="A economia do seu jogo favorito esta quebrando",
        cenas=[
            Cena(indice=i, narracao=f"argumento numero {i} do longo", prompt_visual="doodle")
            for i in range(80)
        ],
        descricao="d", tags=["games", "economia"],
    )


def test_short_aponta_o_longo_na_descricao(cfg):
    r = R.roteiro_companheiro(LLMDeShort(), cfg, _longo(), youtube_id="iSby7u2ltf8")
    assert "https://youtu.be/iSby7u2ltf8" in r.descricao


def test_sem_youtube_id_nao_inventa_link(cfg):
    """Longo ainda nao publicado: melhor sem link que com link quebrado."""
    r = R.roteiro_companheiro(LLMDeShort(), cfg, _longo(), youtube_id="")
    assert "youtu.be" not in r.descricao


def test_o_prompt_leva_o_miolo_do_longo_nao_o_fechamento(cfg):
    """As primeiras cenas sao gancho e as ultimas sao despedida — nenhuma
    das duas ajuda a escolher a ideia forte."""
    llm = LLMDeShort()
    R.roteiro_companheiro(llm, cfg, _longo())

    prompt = llm.prompts[0]
    for i in (0, 1, 2, 77, 78, 79):
        assert f"argumento numero {i} do longo" not in prompt, f"cena {i} nao e miolo"

    do_miolo = [i for i in range(3, 77) if f"argumento numero {i} do longo" in prompt]
    assert do_miolo, "nenhuma cena do miolo chegou ao prompt"
    # Amostra espalhada, nao um bloco: um trecho contiguo daria so um pedaco do
    # argumento e o LLM escolheria a ideia forte dentro de uma janela estreita.
    assert max(do_miolo) - min(do_miolo) > 30


def test_o_prompt_pede_uma_ideia_e_cta_falado(cfg):
    llm = LLMDeShort()
    R.roteiro_companheiro(llm, cfg, _longo())

    prompt = llm.prompts[0]
    assert "UMA ideia" in prompt
    assert "CTA FALADO" in prompt
    # "link na descricao" nao existe em Shorts e vira CTA morto.
    assert "Sem \"link na descricao\"" in prompt


def test_short_sai_dimensionado_para_a_faixa_da_rotina(cfg):
    """O alvo em caracteres tem que vir da taxa da voz do canal."""
    llm = LLMDeShort()
    R.roteiro_companheiro(llm, cfg, _longo())

    esperado = int(Formato.SHORTS.duracao_alvo_s * R._chars_por_s(cfg))
    assert str(esperado) in llm.prompts[0]


def test_llm_sem_cena_falha_alto(cfg):
    class Vazio(LLMDeShort):
        def completar(self, prompt, *, sistema="", max_tokens=4096, esforco=""):
            return json.dumps({"cenas": []})

    with pytest.raises(ValueError, match="nao devolveu cena"):
        R.roteiro_companheiro(Vazio(), cfg, _longo())
