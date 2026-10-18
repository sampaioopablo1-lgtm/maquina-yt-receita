"""Protocolos dos providers.

Todo provider externo fica atras de uma interface: troca de fornecedor sem
reescrever o pipeline, e um stub deterministico roda offline (CI, teste,
dry-run) sem gastar credito nem tocar em conta real do LinkedIn/email.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from ..models import ICP, Disponibilidade, Lead


class ErroProvider(RuntimeError):
    """Falha recuperavel de provider externo."""


class BuscadorLeads(Protocol):
    def buscar(self, icp: ICP, limite: int) -> list[Lead]: ...


class EnviadorEmail(Protocol):
    def enviar(self, lead: Lead, assunto: str, corpo: str) -> None: ...

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        """Retorna o subconjunto de lead_id que respondeu desde o ultimo check."""
        ...


class AutomacaoLinkedIn(Protocol):
    def conectar(self, lead: Lead, nota: str) -> None: ...

    def mensagem(self, lead: Lead, texto: str) -> None: ...

    def checar_respostas(self, leads: list[Lead]) -> set[str]: ...


class Calendario(Protocol):
    def horarios_livres(
        self, disponibilidade: list[Disponibilidade], dias_a_frente: int
    ) -> list[tuple[datetime, datetime]]: ...

    def criar_evento(
        self, lead: Lead, inicio: datetime, fim: datetime
    ) -> tuple[str, str]:
        """Retorna (calendar_event_id, meet_url)."""
        ...
