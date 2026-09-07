"""Modelos de dominio da maquina de prospeccao."""

from __future__ import annotations

import hashlib
from datetime import date, datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class Canal(str, Enum):
    LINKEDIN = "linkedin"
    EMAIL = "email"


class StatusLead(str, Enum):
    NOVO = "novo"
    EM_SEQUENCIA = "em_sequencia"
    RESPONDEU = "respondeu"
    AGENDA_ENVIADA = "agenda_enviada"
    REUNIAO_MARCADA = "reuniao_marcada"
    DESQUALIFICADO = "desqualificado"
    ESGOTADO = "esgotado"  # sequencia terminou sem resposta


class Lead(BaseModel):
    """Um contato prospectado. `id` e estavel (hash de linkedin_url ou email)."""

    id: str = ""
    nome: str
    cargo: str = ""
    empresa: str = ""
    setor: str = ""
    localizacao: str = ""
    linkedin_url: str = ""
    email: str = ""
    origem: str = "stub"  # nome do provider que encontrou o lead
    status: StatusLead = StatusLead.NOVO
    etapa_sequencia: int = 0
    proxima_acao_em: datetime | None = None
    criado_em: datetime = Field(default_factory=_agora)
    atualizado_em: datetime = Field(default_factory=_agora)
    observacoes: str = ""

    def model_post_init(self, __context) -> None:  # noqa: D401
        if not self.id:
            base = self.linkedin_url or self.email or f"{self.nome}|{self.empresa}"
            self.id = hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]


class Mensagem(BaseModel):
    lead_id: str
    canal: Canal
    etapa: int
    texto: str
    enviado_em: datetime = Field(default_factory=_agora)
    resposta: bool = False


class Disponibilidade(BaseModel):
    """Janela recorrente de horarios livres para reuniao."""

    dia_semana: int  # 0=segunda ... 6=domingo
    hora_inicio: str  # "09:00"
    hora_fim: str  # "18:00"
    duracao_min: int = 30
    fuso: str = "America/Sao_Paulo"


class Reuniao(BaseModel):
    lead_id: str
    inicio: datetime
    fim: datetime
    calendar_event_id: str = ""
    meet_url: str = ""
    criado_em: datetime = Field(default_factory=_agora)


class EtapaSequencia(BaseModel):
    """Um passo da cadencia de prospeccao."""

    ordem: int
    dia_offset: int  # dias apos criado_em do lead (ou apos etapa anterior)
    canal: Canal
    template: str  # nome do template em config/sequencia.yaml


class ICP(BaseModel):
    """Perfil de cliente ideal — filtra quem a maquina vai buscar."""

    cargos: list[str] = Field(default_factory=list)
    setores: list[str] = Field(default_factory=list)
    tamanho_empresa: str = ""  # ex.: "11-50"
    localizacao: str = ""
    palavras_chave: list[str] = Field(default_factory=list)
