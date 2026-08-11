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
    """Barreiras anti-spam. Ver docs/03-compliance-monetizacao.md.

    Em ritmo diario a similaridade fica mais rigorosa (0.65) e a janela de
    comparacao mais longa (30): 30 videos/mes no mesmo subnicho convergem
    sozinhos se nao houver pressao ativa por variacao.
    """

    max_por_dia: int = 6
    similaridade_max: float = 0.65
    exigir_revisao: bool = True
    janela_similaridade: int = 30


class CanalConfig(BaseModel):
    nome: str = "Setiap Level"
    handle: str = "@SetiapLevelID"
    idioma: str = "id"
    tema: str = "dinheiro, trabalho, status e decisoes"
    publico_infantil: bool = False
    categoria_id: str = "22"  # People & Blogs
    estilo_narracao: str = "direto, calmo, com autoridade"
    # doodle (traco a mao, fundo branco) ou voxlite (colagem editorial).
    # Cada canal do portfolio tem identidade propria — ver docs/12.
    estilo_visual: str = "doodle"
    # Voz edge-tts do canal (gratuita, sem cota). Vazio = escolhida pelo idioma.
    voz_edge: str = "id-ID-ArdiNeural"
    referencias_titulo: list[str] = Field(default_factory=list)
    # Eixos tematicos rotacionados a cada video. Em ritmo diario esta e a
    # principal defesa contra convergencia: forca angulos estruturalmente
    # diferentes dentro do mesmo subnicho.
    eixos_tematicos: list[str] = Field(default_factory=list)
    # Idioma do operador — usado para traduzir comentarios e roteiros na revisao.
    idioma_revisao: str = "pt-BR"


class Config(BaseModel):
    canal: CanalConfig = Field(default_factory=CanalConfig)
    metas: MetasQualidade = Field(default_factory=MetasQualidade)
    publicacao: LimitesPublicacao = Field(default_factory=LimitesPublicacao)

    # Providers - caem para "stub" automaticamente se faltar credencial.
    llm_provider: str = "anthropic"
    tts_provider: str = "elevenlabs"
    image_provider: str = "openai"
    # "canva" usa o Canva Connect API para o thumbnail final (layout editorial
    # profissional, maior CTR). Requer CANVA_CLIENT_ID, CANVA_CLIENT_SECRET e
    # CANVA_TEMPLATE_ID. Qualquer outro valor usa PIL+OpenAI.
    thumbnail_provider: str = "openai"

    llm_model: str = "claude-sonnet-4-5"
    tts_model: str = "eleven_multilingual_v2"
    tts_voice_id: str = ""
    image_model: str = "gpt-image-1"

    data_dir: Path = ROOT / "data"
    out_dir: Path = ROOT / "out"

    yt_client_secret: Path = ROOT / "secrets" / "client_secret.json"
    yt_token: Path = ROOT / "secrets" / "youtube_token.json"

    @classmethod
    def load(cls, path: Path | None = None, canal: str = "") -> "Config":
        """Carrega default.yaml e, se `canal` (ou MAQ_CANAL) apontar um slug,
        mescla config/canais/<slug>.yaml por cima e isola data/ e out/ por
        canal — 10 canais nao podem compartilhar janela de similaridade nem
        contadores de publicacao (docs/12-portfolio-10-canais.md)."""
        raw: dict[str, Any] = {}
        cfg_file = path or ROOT / "config" / "default.yaml"
        if cfg_file.exists():
            raw = yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}

        slug = canal or os.getenv("MAQ_CANAL", "")
        if slug and slug != "default":
            canal_file = ROOT / "config" / "canais" / f"{slug}.yaml"
            if not canal_file.exists():
                raise FileNotFoundError(
                    f"canal '{slug}' nao existe: crie {canal_file}"
                )
            extra = yaml.safe_load(canal_file.read_text(encoding="utf-8")) or {}
            for chave, valor in extra.items():
                if isinstance(valor, dict) and isinstance(raw.get(chave), dict):
                    raw[chave] = {**raw[chave], **valor}
                else:
                    raw[chave] = valor
            raw.setdefault("data_dir", ROOT / "data" / slug)
            raw.setdefault("out_dir", ROOT / "out" / slug)
            raw.setdefault(
                "yt_token", ROOT / "secrets" / f"youtube_token_{slug}.json"
            )

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
