"""Orquestrador: encadeia as etapas com estado e retomada.

Cada etapa grava o estado antes de avancar. Se o job cair no meio (runner morre,
API fora do ar), `retomar()` continua de onde parou em vez de refazer — e
regerar audio e imagem custa dinheiro.
"""

from __future__ import annotations

import logging
import time
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

    def ideia_guardada(self, formato: Formato) -> Video | None:
        """Pauta ja escolhida em rodada anterior, esperando virar video.

        `gerar_ideias` pede CINCO ideias numa chamada e o `auto` usava uma,
        jogando quatro fora. Parecia gratuito e nao era: o Gemini do plano
        gratuito da 20 requisicoes por dia, e cada video gasta uma na ideacao,
        uma no roteiro, ate duas na extensao e mais uma no short companheiro.
        Com seis disparos diarios isso estoura a cota — foi o que derrubou
        next-level-money em 12/08/2026 com 429.

        Guardando as quatro sobras, a ideacao passa a custar UMA chamada a cada
        cinco rodadas em vez de uma por rodada.
        """
        candidatos = [
            v for v in self.store.listar(Status.IDEIA, limite=50)
            if v.formato is formato
            and v.ideia
            and (v.canal or None) == (self.cfg.canal_slug or None)
        ]
        return min(candidatos, key=lambda v: v.criado_em) if candidatos else None

    def guardar_ideias(self, ideias: list[Ideia]) -> int:
        """Salva pautas para as proximas rodadas. Devolve quantas entraram."""
        conhecidos = {v.slug for v in self.store.listar(limite=10_000)}
        novas = 0
        for ideia in ideias:
            if ideia.slug in conhecidos:
                continue
            self.criar(ideia)
            novas += 1
        return novas

    def criar(self, ideia: Ideia) -> Video:
        video = Video(slug=ideia.slug, formato=ideia.formato,
                      idioma=self.cfg.canal.idioma,
                      canal=self.cfg.canal_slug or None, ideia=ideia)
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
            render.montar_thumbnail(
                self.imagem,
                video.roteiro,
                destino,
                usar_canva=self.cfg.thumbnail_provider == "canva",
            )
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

        # Legenda no mesmo passo da publicacao.
        #
        # Ate 2026-08-12 o .srt so subia pelo legendar.yml, um workflow manual —
        # entao todo video do cron nascia com caption=false, medido em
        # iSby7u2ltf8. captions.insert exige o video publico ou nao-listado, o
        # que so passou a valer quando o caminho automatico parou de agendar
        # (publicacao.agendar_horas = 0).
        #
        # Nao derruba a publicacao: o video ja esta no ar, e legenda ausente e
        # um alerta da compliance, nao um bloqueio.
        if video.legenda_path and Path(video.legenda_path).exists():
            # Logo apos o insert o video ainda esta em processamento e a API
            # devolve 403 na faixa de legenda. Esperar e barato; perder a
            # legenda de um video de treze minutos nao e.
            for tentativa in range(4):
                try:
                    youtube.enviar_legenda(video, self.cfg)
                    break
                except Exception as e:
                    if tentativa == 3:
                        log.warning(
                            "legenda nao enviada para %s: %s", video.youtube_id, e
                        )
                    else:
                        time.sleep(30 * (tentativa + 1))
        else:
            log.warning("sem .srt em disco — %s fica com caption=false", video.youtube_id)

        return video

    def companheiro(self, longo: Video) -> Video:
        """Produz o short que leva publico ao longo. Nao publica.

        A regra mestra da rotina pede pacote — longo E short — e o caminho
        automatico sempre entregou um video sozinho. O custo disso estava
        medido: longo publicado sem short faz 0,14 view/dia, porque em canal
        frio o feed de Shorts entrega e o de longos nao.
        """
        if not longo.roteiro:
            raise ValueError(f"{longo.slug} nao tem roteiro para derivar o short")

        video = Video(
            slug=f"{longo.slug}-short",
            formato=Formato.SHORTS,
            idioma=longo.idioma,
            canal=longo.canal,
            roteiro=roteiro_stage.roteiro_companheiro(
                self.llm, self.cfg, longo.roteiro, longo.youtube_id or ""
            ),
            status=Status.ROTEIRIZADO,
        )
        self.store.salvar(video)
        log.info("short companheiro de %s: %d cenas", longo.slug, len(video.roteiro.cenas))

        self.narrar(video)
        self.ilustrar(video)
        self.renderizar(video)
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
