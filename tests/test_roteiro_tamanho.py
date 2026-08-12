"""Dimensionamento do roteiro longo.

A rotina pede 12 a 15 minutos. O primeiro longo do caminho automatico saiu com
623 s contra 780 de alvo — 80%, acima do piso de 8 min, entao passou por todas
as barreiras e foi publicado como 10:23. Estava dentro das regras e fora do que
o dono pediu. Estes testes fixam o comportamento que fecha essa folga.
"""

from __future__ import annotations

import json

import pytest

from maquina.config import Config
from maquina.models import Formato, Ideia
from maquina.stages import roteiro as R


class LLMFalso:
    """Devolve cenas de tamanho controlado e conta as chamadas."""

    def __init__(self, chars_primeira: int, chars_extensao: int = 0, cenas: int = 80):
        self.chars_primeira = chars_primeira
        self.chars_extensao = chars_extensao
        self.cenas = cenas
        self.prompts: list[str] = []

    def completar(self, prompt: str, *, sistema: str = "", max_tokens: int = 4096) -> str:
        self.prompts.append(prompt)
        primeira = len(self.prompts) == 1
        total = self.chars_primeira if primeira else self.chars_extensao
        n = self.cenas if primeira else 10
        texto = "a" * max(total // n, 1)
        cenas = [{"narracao": texto, "prompt_visual": "doodle"} for _ in range(n)]
        if primeira:
            return json.dumps(
                {
                    "titulo": "T", "gancho": "G", "cenas": cenas,
                    "descricao": "d", "tags": ["t"],
                    "prompt_thumbnail": "p", "texto_thumbnail": "TT",
                }
            )
        return json.dumps({"cenas": cenas})


@pytest.fixture
def cfg():
    c = Config.load(canal="nivel-do-jogo")
    assert c.canal.voz_edge in R.CHARS_POR_S, "a voz precisa de taxa medida"
    return c


def _alvo(cfg) -> int:
    return int(Formato.LONGO.duracao_alvo_s * R._chars_por_s(cfg))


def _ideia() -> Ideia:
    return Ideia(titulo="Por Que a Inflacao nos Games", formato=Formato.LONGO)


def test_roteiro_no_alvo_nao_pede_extensao(cfg):
    llm = LLMFalso(chars_primeira=_alvo(cfg))
    R.escrever_roteiro(llm, cfg, _ideia())
    assert len(llm.prompts) == 1


def test_roteiro_a_80_por_cento_e_estendido(cfg):
    """O caso real: 623 s contra 780. Passava limpo e saia 10:23."""
    alvo = _alvo(cfg)
    llm = LLMFalso(chars_primeira=int(alvo * 0.80), chars_extensao=int(alvo * 0.15))

    r = R.escrever_roteiro(llm, cfg, _ideia())

    assert len(llm.prompts) == 2, "deveria ter pedido as cenas que faltavam"
    chars = sum(len(c.narracao) for c in r.cenas)
    assert chars >= alvo * R.ALVO_MINIMO
    duracao_min = chars / R._chars_por_s(cfg) / 60
    assert duracao_min >= 11.5, f"{duracao_min:.1f} min ainda esta abaixo do pedido"


def test_cenas_novas_entram_antes_do_fechamento(cfg):
    """As tres ultimas cenas sao sintese e convite — o video nao pode terminar duas vezes."""
    alvo = _alvo(cfg)
    llm = LLMFalso(chars_primeira=int(alvo * 0.80), chars_extensao=int(alvo * 0.15))
    original = json.loads(llm.completar("previa"))["cenas"]
    fecho_original = original[-3:]
    llm.prompts.clear()

    r = R.escrever_roteiro(llm, cfg, _ideia())

    assert len(r.cenas) > len(original)
    assert [c.narracao for c in r.cenas[-3:]] == [c["narracao"] for c in fecho_original]
    assert [c.indice for c in r.cenas] == list(range(len(r.cenas)))


def test_extensao_que_falha_nao_derruba_o_roteiro(cfg):
    """Estender e melhoria, nao requisito: 80% ainda passa do piso de 75%."""

    class Quebra(LLMFalso):
        def completar(self, prompt, *, sistema="", max_tokens=4096):
            if self.prompts:
                self.prompts.append(prompt)
                raise RuntimeError("gemini fora do ar")
            return super().completar(prompt, sistema=sistema, max_tokens=max_tokens)

    llm = Quebra(chars_primeira=int(_alvo(cfg) * 0.80))
    r = R.escrever_roteiro(llm, cfg, _ideia())
    assert len(r.cenas) > 0


def test_roteiro_curto_demais_ainda_e_recusado(cfg):
    """Abaixo do piso, com a extensao sem ajudar, tem que morrer antes de renderizar."""
    llm = LLMFalso(chars_primeira=int(_alvo(cfg) * 0.30), chars_extensao=0)
    with pytest.raises(ValueError, match="curto demais"):
        R.escrever_roteiro(llm, cfg, _ideia())


def test_shorts_nao_e_estendido(cfg):
    """50 s de alvo: estender um short o tira do formato."""
    alvo_short = int(Formato.SHORTS.duracao_alvo_s * R._chars_por_s(cfg))
    llm = LLMFalso(chars_primeira=int(alvo_short * 0.80), cenas=5)
    R.escrever_roteiro(llm, cfg, Ideia(titulo="Curto", formato=Formato.SHORTS))
    assert len(llm.prompts) == 1
