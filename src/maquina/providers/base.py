"""Protocolos dos providers.

Todo provider externo fica atras de uma interface, por dois motivos praticos:
trocar de fornecedor sem reescrever a pipeline, e ter um stub deterministico que
roda offline (CI, teste, dry-run) sem gastar credito.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class LLM(Protocol):
    # `esforco` e uma dica de quanto o modelo deve raciocinar ("low" a "max").
    # So a Anthropic a implementa; os demais aceitam e ignoram, para que a
    # etapa possa pedir esforco sem saber quem esta atendendo.
    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str: ...

    @property
    def custo_usd(self) -> float: ...


class TTS(Protocol):
    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path: ...

    @property
    def custo_usd(self) -> float: ...


class GeradorImagem(Protocol):
    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path: ...

    @property
    def custo_usd(self) -> float: ...


class ErroProvider(RuntimeError):
    """Falha recuperavel de provider externo."""


class ErroOrcamento(RuntimeError):
    """Teto de gasto do run estourado.

    NAO herda de ErroProvider de proposito: a cadeia de fallback trata
    ErroProvider trocando de fornecedor, e trocar de fornecedor por causa de
    orcamento so moveria o gasto de lugar. Estourou o teto, o run para.
    """
