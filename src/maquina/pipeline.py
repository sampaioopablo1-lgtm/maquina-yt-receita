"""Orquestrador: encadeia as etapas com estado e retomada.

Cada etapa grava o estado antes de avancar. Se o job cair no meio (runner morre,
API fora do ar), `retomar()` continua de onde parou em vez de refazer — e
regerar audio e imagem custa dinheiro.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from .config import Config
from .models import Formato, Ideia, Status, Video
from .providers import obter_imagem, obter_llm, obter_tts
from .stages import compliance, diagnostico, producao, render, roteiro as roteiro_stage, youtube
from .storage import Store

log = logging.getLogger("maquina.pipeline")


class Pipeline:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.store = Store(cfg.data_dir / "maquina.db")
        self.llm = obter_llm(cfg)
        self.tts = obter_tts(cfg)
        self.imagem = obter_imagem(cfg)

    @property
    def custo_usd(self) -> float:
        return sum(
            getattr(p, "custo_usd", 0.0) for p in (self.llm, self.tts, self.imagem)
        )

    # ---------- etapas ----------

    def ideias(self, formato: Formato, n: int = 5) -> list[Ideia]:
        return roteiro_stage.gerar_ideias(
            self.llm, self.cfg, formato, n, self.store.titulos_publicados()
        )

    def pendente(self, formato: Formato) -> Video | None:
        """Roteiro ja pronto esperando produzir (ex.: gravado pela Edge Function
        `gerar-roteiro` no Supabase e trazido pro SQLite por `maquina sincronizar`).

        `maquina auto` consome isso antes de ideiar do zero — sem isto o roteiro
        so virava video se alguem rodasse `maquina retomar <slug>` na mao.
        """
        candidatos = [
            v for v in self.store.listar(Status.ROTEIRIZADO, limite=50) if v.formato is formato
        ]
        return min(candidatos, key=lambda v: v.criado_em) if candidatos else None

    def criar(self, ideia: Ideia) -> Video:
        video = Video(slug=ideia.slug, formato=ideia.formato, idioma=self.cfg.canal.idioma, ideia=ideia)
        self.store.salvar(video)
        return video

    def roteirizar(self, video: Video) -> Video:
        assert video.ideia
        video.roteiro = roteiro_stage.escrever_roteiro(self.llm, self.cfg, video.ideia)
        video.status = Status.ROTEIRIZADO
        self.store.salvar(video)
        log.info("roteiro pronto: %d cenas, %d palavras",
                 len(video.roteiro.cenas), video.roteiro.palavras)
        return video

    def narrar(self, video: Video) -> Video:
        assert video.roteiro
        producao.narrar(
            self.tts, video.roteiro, video.dir(self.cfg.out_dir), self.cfg.tts_voice_id
        )
        video.status = Status.NARRADO
        self.store.salvar(video)
        return video

    def ilustrar(self, video: Video) -> Video:
        assert video.roteiro
        producao.ilustrar(
            self.imagem, video.roteiro, video.dir(self.cfg.out_dir), video.formato
        )
        video.status = Status.ILUSTRADO
        self.store.salvar(video)
        return video

    def renderizar(self, video: Video) -> Video:
        assert video.roteiro
        destino = video.dir(self.cfg.out_dir)

        srt = producao.gerar_legendas(video.roteiro, destino / "legendas.srt")
        video.legenda_path = str(srt)

        caminho, dur = render.montar(
            video.roteiro, destino, video.formato, legendas=srt
        )
        video.video_path, video.duracao_s = str(caminho), dur

        video.thumbnail_path = str(
            render.montar_thumbnail(self.imagem, video.roteiro, destino)
        )
        video.status = Status.RENDERIZADO
        video.custo_usd = self.custo_usd
        self.store.salvar(video)
        return video

    def verificar(self, video: Video) -> compliance.Resultado:
        res = compliance.verificar(video, self.cfg, self.store)
        video.status = Status.AGUARDANDO_REVISAO if res.aprovado else Status.REJEITADO
        if not res.aprovado:
            video.erro = "; ".join(res.bloqueios)
        self.store.salvar(video)
        return res

    def publicar(
        self, video: Video, *, agendar_para: datetime | None = None, privacidade: str = "private"
    ) -> Video:
        video.youtube_id = youtube.publicar(
            video, self.cfg, privacidade=privacidade, agendar_para=agendar_para
        )
        video.status = Status.PUBLICADO
        # Aware, como criado_em e agendado_para: a coluna no Supabase e
        # timestamptz e uma string sem offset e lida como UTC, gravando a hora
        # local como se fosse UTC.
        video.publicado_em = datetime.now(timezone.utc)
        video.agendado_para = agendar_para
        self.store.salvar(video)
        return video

    # ---------- fluxos completos ----------

    def produzir(self, ideia: Ideia) -> Video:
        """Da ideia ao MP4 renderizado, sem publicar."""
        video = self.criar(ideia)
        try:
            self.roteirizar(video)
            self.narrar(video)
            self.ilustrar(video)
            self.renderizar(video)
        except Exception as e:
            video.status = Status.ERRO
            video.erro = f"{type(e).__name__}: {e}"
            self.store.salvar(video)
            raise
        return video

    def retomar(self, slug: str) -> Video:
        """Continua um video parado, pulando o que ja foi feito."""
        video = self.store.obter(slug)
        if not video:
            raise ValueError(f"video '{slug}' nao encontrado")

        ordem = [
            (Status.IDEIA, self.roteirizar),
            (Status.ROTEIRIZADO, self.narrar),
            (Status.NARRADO, self.ilustrar),
            (Status.ILUSTRADO, self.renderizar),
        ]
        # Status ERRO retoma da etapa correspondente ao ultimo artefato valido.
        if video.status is Status.ERRO:
            video.status = _ultimo_estado_valido(video)

        iniciar = False
        for estado, etapa in ordem:
            if video.status is estado:
                iniciar = True
            if iniciar:
                etapa(video)
        return video

    def diagnosticar(self, video: Video) -> diagnostico.Diagnostico | None:
        if not video.youtube_id:
            return None
        m = youtube.coletar_metricas(self.cfg, video.youtube_id)
        self.store.salvar_metricas(m)
        return diagnostico.diagnosticar(m, self.cfg)


def _ultimo_estado_valido(video: Video) -> Status:
    if not video.roteiro:
        return Status.IDEIA
    cenas = video.roteiro.cenas
    if not all(c.audio_path and Path(c.audio_path).exists() for c in cenas):
        return Status.ROTEIRIZADO
    if not all(c.imagem_path and Path(c.imagem_path).exists() for c in cenas):
        return Status.NARRADO
    return Status.ILUSTRADO
