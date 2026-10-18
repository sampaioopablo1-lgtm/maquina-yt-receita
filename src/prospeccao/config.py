"""Configuracao: env (segredos) + YAML (ICP, cadencia, limites)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from .models import Canal, Disponibilidade, EtapaSequencia, ICP

ROOT = Path(__file__).resolve().parents[2]


class LimitesEnvio(BaseModel):
    """Tetos diarios. Numeros conservadores de proposito — sao a principal
    defesa contra bloqueio de conta (LinkedIn) e spam-flag (email)."""

    linkedin_convites_dia: int = 15
    linkedin_mensagens_dia: int = 25
    email_envios_dia: int = 40
    leads_novos_dia: int = 20


class Config(BaseModel):
    icp: ICP = Field(default_factory=ICP)
    sequencia: list[EtapaSequencia] = Field(
        default_factory=lambda: [
            EtapaSequencia(ordem=1, dia_offset=0, canal=Canal.LINKEDIN, template="convite"),
            EtapaSequencia(ordem=2, dia_offset=0, canal=Canal.EMAIL, template="intro"),
            EtapaSequencia(ordem=3, dia_offset=3, canal=Canal.LINKEDIN, template="follow_up_1"),
            EtapaSequencia(ordem=4, dia_offset=7, canal=Canal.EMAIL, template="follow_up_2"),
            EtapaSequencia(ordem=5, dia_offset=12, canal=Canal.EMAIL, template="breakup"),
        ]
    )
    limites: LimitesEnvio = Field(default_factory=LimitesEnvio)
    disponibilidade: list[Disponibilidade] = Field(
        default_factory=lambda: [
            Disponibilidade(dia_semana=d, hora_inicio="09:00", hora_fim="18:00", duracao_min=30)
            for d in range(5)  # segunda a sexta
        ]
    )

    # Providers - caem para "stub" automaticamente se faltar credencial.
    leads_provider: str = "auto"  # auto | apollo | stub
    email_provider: str = "auto"  # auto | smtp | resend | stub
    linkedin_provider: str = "auto"  # auto | playwright | stub
    calendario_provider: str = "auto"  # auto | google | stub

    remetente_nome: str = ""
    remetente_email: str = ""
    calendly_like_base_url: str = "http://localhost:8000"

    data_dir: Path = ROOT / "data" / "prospeccao"

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        raw: dict[str, Any] = {}
        cfg_file = path or ROOT / "config" / "prospeccao.yaml"
        if cfg_file.exists():
            raw = yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}

        for env_key, field in [
            ("PROS_LEADS_PROVIDER", "leads_provider"),
            ("PROS_EMAIL_PROVIDER", "email_provider"),
            ("PROS_LINKEDIN_PROVIDER", "linkedin_provider"),
            ("PROS_CALENDARIO_PROVIDER", "calendario_provider"),
            ("PROS_REMETENTE_NOME", "remetente_nome"),
            ("PROS_REMETENTE_EMAIL", "remetente_email"),
            ("PROS_BOOKING_BASE_URL", "calendly_like_base_url"),
        ]:
            if os.getenv(env_key):
                raw[field] = os.environ[env_key]

        if os.getenv("PROS_DATA_DIR"):
            raw["data_dir"] = Path(os.environ["PROS_DATA_DIR"])

        cfg = cls(**raw)
        cfg.data_dir.mkdir(parents=True, exist_ok=True)
        return cfg
