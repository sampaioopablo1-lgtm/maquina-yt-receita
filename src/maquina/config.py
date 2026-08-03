"""Configuracao: env (segredos) + YAML (parametros editoriais)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]


class MetasQualidade(BaseModel):
    """Os 3 pilares viram numeros. Ver docs/02-playbook-youtube.md."""

    ctr_min: float = 0.05
    ctr_bom: float = 0.08
    retencao_min_pct: float = 30.0


class LimitesPublicacao(BaseModel):
    """Barreiras anti-spam. Ver docs/03-compliance-monetizacao.md."""

    max_por_dia: int = 2
    similaridade_max: float = 0.75
    exigir_revisao: bool = True
    janela_similaridade: int = 20


class CanalConfig(BaseModel):
    nome: str = "Setiap Level"
    handle: str = "@SetiapLevelID"
    idioma: str = "id"
    tema: str = "dinheiro, trabalho, status e decisoes"
    publico_infantil: bool = False
    categoria_id: str = "22"  # People & Blogs
    estilo_narracao: str = "direto, calmo, com autoridade"
    referencias_titulo: list[str] = Field(default_factory=list)


class Config(BaseModel):
    canal: CanalConfig = Field(default_factory=CanalConfig)
    metas: MetasQualidade = Field(default_factory=MetasQualidade)
    publicacao: LimitesPublicacao = Field(default_factory=LimitesPublicacao)

    # Providers - caem para "stub" automaticamente se faltar credencial.
    llm_provider: str = "anthropic"
    tts_provider: str = "elevenlabs"
    image_provider: str = "openai"

    llm_model: str = "claude-sonnet-4-5"
    tts_model: str = "eleven_multilingual_v2"
    tts_voice_id: str = ""
    image_model: str = "gpt-image-1"

    data_dir: Path = ROOT / "data"
    out_dir: Path = ROOT / "out"

    yt_client_secret: Path = ROOT / "secrets" / "client_secret.json"
    yt_token: Path = ROOT / "secrets" / "youtube_token.json"

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        raw: dict[str, Any] = {}
        cfg_file = path or ROOT / "config" / "default.yaml"
        if cfg_file.exists():
            raw = yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}

        # Env sobrepoe YAML, para o Actions injetar sem editar arquivo.
        for env_key, field in [
            ("MAQ_LLM_PROVIDER", "llm_provider"),
            ("MAQ_TTS_PROVIDER", "tts_provider"),
            ("MAQ_IMAGE_PROVIDER", "image_provider"),
            ("MAQ_LLM_MODEL", "llm_model"),
            ("MAQ_TTS_MODEL", "tts_model"),
            ("MAQ_TTS_VOICE_ID", "tts_voice_id"),
            ("MAQ_IMAGE_MODEL", "image_model"),
        ]:
            if os.getenv(env_key):
                raw[field] = os.environ[env_key]

        for env_key, field in [
            ("MAQ_DATA_DIR", "data_dir"),
            ("MAQ_OUT_DIR", "out_dir"),
            ("MAQ_YT_CLIENT_SECRET", "yt_client_secret"),
            ("MAQ_YT_TOKEN", "yt_token"),
        ]:
            if os.getenv(env_key):
                raw[field] = Path(os.environ[env_key])

        cfg = cls(**raw)
        cfg.data_dir.mkdir(parents=True, exist_ok=True)
        cfg.out_dir.mkdir(parents=True, exist_ok=True)
        return cfg
