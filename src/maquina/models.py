"""Modelos de dominio da maquina de video."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class Formato(str, Enum):
    """Formato de saida. Define resolucao, duracao alvo e estrategia de edicao."""

    SHORTS = "shorts"
    LONGO = "longo"

    @property
    def resolucao(self) -> tuple[int, int]:
        return (1080, 1920) if self is Formato.SHORTS else (1920, 1080)

    @property
    def duracao_alvo_s(self) -> int:
        # 780 s = 13 min, meio da faixa de 12-15 que a rotina pede, e o mesmo
        # valor que canais.duracao_alvo_s guarda no banco desde sempre.
        #
        # Era 8*60 com o comentario "mira acima de 8 min". Mirar EM 8 min e o
        # erro: 8 min e o PISO, nao o alvo, entao qualquer roteiro que ficasse
        # um pouco abaixo do pedido caia direto abaixo do minimo. Combinado com
        # o gerador pedindo 12 cenas em vez de 70, deu a mediana de 231 s dos
        # dez longos automaticos (aprendizado #181).
        # SHORTS: a rotina pede 30 a 45 s. Era 50 — o alvo do codigo nunca foi
        # alinhado com o pedido, e 50 mais a variacao normal do TTS entrega
        # acima da faixa: _5rPClaanvw saiu com 56 s em 12/08/2026. 38 e o meio
        # de 30-45, e sobra margem para o TTS passar um pouco sem sair fora.
        return 38 if self is Formato.SHORTS else 780

    @property
    def aspect(self) -> str:
        return "9:16" if self is Formato.SHORTS else "16:9"


class Status(str, Enum):
    IDEIA = "ideia"
    ROTEIRIZADO = "roteirizado"
    NARRADO = "narrado"
    ILUSTRADO = "ilustrado"
    RENDERIZADO = "renderizado"
    AGUARDANDO_REVISAO = "aguardando_revisao"
    APROVADO = "aprovado"
    # Aliases legados do Supabase — gerados por workflows externos.
    LISTADO_PARA_PUBLICACAO = "listado_para_publicacao"
    # Gerado pela fabrica/ (fluxo manual, fora desta pipeline — ver
    # pyproject.toml). Sem este membro, Video.model_validate rejeitava a linha
    # inteira e `puxar()` a descartava: o video nunca chegava ao SQLite local,
    # entao `maquina publicar <slug>` sempre respondia "nao encontrei" e o
    # workflow_dispatch que insiste nesse slug (labtreinamento-001) falhava a
    # cada tentativa — 6 vezes so em 12/08/2026, sempre pelo mesmo motivo.
    PRONTO_NAO_ENTREGUE = "pronto_nao_entregue"
    CANCELADO = "cancelado"
    PUBLICADO = "publicado"
    REJEITADO = "rejeitado"
    ERRO = "erro"


class Ideia(BaseModel):
    """Uma pauta candidata, antes de virar roteiro."""

    titulo: str
    angulo: str = ""
    palavras_chave: list[str] = Field(default_factory=list)
    formato: Formato = Formato.LONGO

    @property
    def slug(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.titulo.lower()).strip("-")[:60]
        digest = hashlib.sha1(self.titulo.encode()).hexdigest()[:6]
        return f"{base}-{digest}"


class Cena(BaseModel):
    """Unidade atomica de edicao: um trecho de narracao + um visual."""

    indice: int
    narracao: str
    prompt_visual: str
    # Preenchidos pelas etapas seguintes.
    audio_path: str | None = None
    imagem_path: str | None = None
    duracao_s: float | None = None

    @property
    def palavras(self) -> int:
        return len(self.narracao.split())


class Roteiro(BaseModel):
    titulo: str
    gancho: str
    cenas: list[Cena]
    descricao: str = ""
    tags: list[str] = Field(default_factory=list)
    prompt_thumbnail: str = ""
    texto_thumbnail: str = ""

    @property
    def texto_completo(self) -> str:
        return " ".join(c.narracao for c in self.cenas)

    @property
    def palavras(self) -> int:
        return len(self.texto_completo.split())


class Video(BaseModel):
    """Estado completo de um video ao longo da pipeline."""

    slug: str
    formato: Formato
    status: Status = Status.IDEIA
    idioma: str = "id"
    # A que canal este video pertence. Ausente ate 2026-08-12, e a falta doia em
    # dois lugares: o sync nunca gravava canal no Supabase (15 de 33 linhas
    # ficaram orfas e a v_maquina_fila nao as via), e a compliance nao conseguia
    # contar publicacoes POR CANAL — o teto diario media a frota inteira somada.
    canal: str | None = None

    ideia: Ideia | None = None
    roteiro: Roteiro | None = None

    video_path: str | None = None
    thumbnail_path: str | None = None
    legenda_path: str | None = None
    duracao_s: float | None = None

    youtube_id: str | None = None
    publicado_em: datetime | None = None
    agendado_para: datetime | None = None

    # Conteudo sintetico realista precisa ser divulgado no upload.
    conteudo_sintetico: bool = True

    erro: str | None = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custo_usd: float = 0.0

    # Linha que veio do Supabase com um `roteiro` que nao e um Roteiro (as da
    # fabrica/ guardam metricas ali) e foi reconstruida a partir do titulo so
    # para alimentar os contadores da compliance. Existe local, nunca volta ao
    # Supabase: o roteiro reconstruido tem titulo e nada mais, e empurrar
    # sobrescreveria o blob original — que e a unica copia de fonte_pauta,
    # trilha e dos IDs do Drive. Ver sincronizacao._resgatar.
    resgatado: bool = False

    def dir(self, base: Path) -> Path:
        d = base / self.slug
        d.mkdir(parents=True, exist_ok=True)
        return d


class Metricas(BaseModel):
    """Snapshot de performance vindo do YouTube Analytics."""

    youtube_id: str
    impressoes: int = 0
    views: int = 0
    ctr: float = 0.0
    retencao_media_pct: float = 0.0
    duracao_media_s: float = 0.0
    inscritos_ganhos: int = 0
    receita_estimada_usd: float = 0.0
    coletado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
