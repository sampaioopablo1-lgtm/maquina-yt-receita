"""Publicacao e coleta de metricas via YouTube Data / Analytics API."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..config import Config
from ..models import Metricas, Video

log = logging.getLogger("maquina.youtube")

ESCOPOS = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def _credenciais(cfg: Config, permitir_interativo: bool = False):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    cred = None
    if cfg.yt_token.exists():
        cred = Credentials.from_authorized_user_file(str(cfg.yt_token), ESCOPOS)

    if cred and cred.valid:
        return cred

    if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
    elif permitir_interativo:
        from google_auth_oauthlib.flow import InstalledAppFlow

        if not cfg.yt_client_secret.exists():
            raise FileNotFoundError(
                f"client secret ausente em {cfg.yt_client_secret}. "
                "Google Cloud Console > OAuth client ID > Desktop app."
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(cfg.yt_client_secret), ESCOPOS
        )
        # console flow: funciona em ambiente sem browser (servidor, container).
        cred = flow.run_local_server(port=0)
    else:
        raise RuntimeError(
            "sem credencial valida do YouTube. Rode `maquina auth-youtube` uma vez "
            "e guarde o token resultante no secret YT_TOKEN_JSON."
        )

    cfg.yt_token.parent.mkdir(parents=True, exist_ok=True)
    cfg.yt_token.write_text(cred.to_json(), encoding="utf-8")
    return cred


def autenticar(cfg: Config) -> Path:
    """Fluxo OAuth interativo, executado uma vez pelo operador."""
    _credenciais(cfg, permitir_interativo=True)
    log.info("token salvo em %s", cfg.yt_token)
    return cfg.yt_token


def canal_autorizado(cfg: Config) -> dict[str, str]:
    """Qual canal a credencial atual controla.

    Uma conta Google pode ter varios canais (Contas de Marca), e a escolha
    acontece na tela do Google. Confirmar depois evita o erro caro: publicar
    no canal errado.
    """
    yt = _servico(cfg)
    resp = yt.channels().list(part="snippet,statistics", mine=True).execute()

    itens = resp.get("items") or []
    if not itens:
        raise RuntimeError(
            "a credencial nao controla nenhum canal. Refaca `maquina auth-youtube` "
            "e selecione um canal na tela do Google."
        )

    snip = itens[0]["snippet"]
    stats = itens[0].get("statistics", {})
    return {
        "id": itens[0]["id"],
        "titulo": snip.get("title", ""),
        "handle": snip.get("customUrl", ""),
        "inscritos": stats.get("subscriberCount", "0"),
        "videos": stats.get("videoCount", "0"),
    }


def _servico(cfg: Config, nome: str = "youtube", versao: str = "v3"):
    from googleapiclient.discovery import build

    return build(nome, versao, credentials=_credenciais(cfg), cache_discovery=False)


def publicar(
    video: Video,
    cfg: Config,
    *,
    privacidade: str = "private",
    agendar_para: datetime | None = None,
) -> str:
    """Upload resumable + thumbnail. Devolve o videoId.

    Padrao e `private` com agendamento: o video sobe, e processado, e so entao
    fica publico no horario marcado. Subir direto como `public` significa expor
    um video ainda em processamento, com qualidade degradada nos primeiros
    minutos.
    """
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    if not video.video_path:
        raise ValueError("video sem arquivo renderizado")
    if not video.roteiro:
        raise ValueError("video sem roteiro/metadados")

    yt = _servico(cfg)

    status: dict = {
        "privacyStatus": "private" if agendar_para else privacidade,
        "selfDeclaredMadeForKids": cfg.canal.publico_infantil,
        # Divulgacao de conteudo alterado/sintetico, obrigatoria para conteudo
        # realista. Vai aqui, no insert, porque `containsSyntheticMedia` pertence
        # ao schema VideoStatus — nao a contentDetails, e nao e legivel de volta
        # num videos.update posterior.
        # https://support.google.com/youtube/answer/14328491
        "containsSyntheticMedia": video.conteudo_sintetico,
    }
    if agendar_para:
        status["publishAt"] = agendar_para.astimezone(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )

    corpo = {
        "snippet": {
            "title": video.roteiro.titulo[:100],
            "description": video.roteiro.descricao[:5000],
            "tags": video.roteiro.tags[:30],
            "categoryId": cfg.canal.categoria_id,
            "defaultLanguage": cfg.canal.idioma,
            "defaultAudioLanguage": cfg.canal.idioma,
        },
        "status": status,
    }

    midia = MediaFileUpload(
        video.video_path, mimetype="video/mp4", resumable=True, chunksize=8 * 1024 * 1024
    )
    req = yt.videos().insert(part="snippet,status", body=corpo, media_body=midia)

    resposta = None
    while resposta is None:
        # num_retries=0 (o default) tenta o chunk UMA vez: um 502 transitorio
        # perderia o upload de um video ja produzido e revisado.
        progresso, resposta = req.next_chunk(num_retries=5)
        if progresso:
            log.info("upload %d%%", int(progresso.progress() * 100))

    video_id = resposta["id"]
    log.info("publicado: https://youtu.be/%s", video_id)

    if video.thumbnail_path and Path(video.thumbnail_path).exists():
        try:
            yt.thumbnails().set(
                videoId=video_id, media_body=MediaFileUpload(video.thumbnail_path)
            ).execute()
        except HttpError as e:
            # Thumbnail custom exige canal verificado — nao e motivo para falhar o job.
            log.warning("thumbnail nao aplicada: %s", e)

    return video_id


def coletar_metricas(cfg: Config, video_id: str, dias: int = 28) -> Metricas:
    """Puxa os numeros dos 3 pilares do YouTube Analytics."""
    analytics = _servico(cfg, "youtubeAnalytics", "v2")
    fim = datetime.now(timezone.utc).date()
    inicio = fim - timedelta(days=dias)

    resp = (
        analytics.reports()
        .query(
            ids="channel==MINE",
            startDate=inicio.isoformat(),
            endDate=fim.isoformat(),
            # Sem `estimatedRevenue` de proposito: e metrica monetaria e exige o
            # escopo yt-analytics-monetary.readonly, que nao esta em ESCOPOS.
            # Pedir aqui devolvia 403 e derrubava a coleta INTEIRA — os 3 pilares
            # junto com a receita. Ela vem depois, em query separada e opcional.
            metrics=(
                "views,estimatedMinutesWatched,averageViewDuration,"
                "averageViewPercentage,subscribersGained"
            ),
            filters=f"video=={video_id}",
        )
        .execute()
    )

    linhas = resp.get("rows") or [[0, 0, 0, 0, 0]]
    v, _min_assistidos, dur_media, pct_media, inscritos = linhas[0]

    m = Metricas(
        youtube_id=video_id,
        views=int(v),
        duracao_media_s=float(dur_media),
        retencao_media_pct=float(pct_media),
        inscritos_ganhos=int(inscritos),
    )

    # Receita: so responde com o escopo monetario E canal no YPP. Enquanto o
    # canal nao monetiza, isto e 403 esperado — nao e falha de coleta.
    try:
        rec = (
            analytics.reports()
            .query(
                ids="channel==MINE",
                startDate=inicio.isoformat(),
                endDate=fim.isoformat(),
                metrics="estimatedRevenue",
                filters=f"video=={video_id}",
            )
            .execute()
        )
        if linhas_rec := rec.get("rows"):
            m.receita_estimada_usd = float(linhas_rec[0][0] or 0)
    except Exception as e:
        log.info("receita indisponivel (escopo monetario ou canal fora do YPP): %s", e)

    # CTR e impressoes vivem num relatorio separado.
    try:
        imp = (
            analytics.reports()
            .query(
                ids="channel==MINE",
                startDate=inicio.isoformat(),
                endDate=fim.isoformat(),
                metrics="impressions,impressionsClickThroughRate",
                filters=f"video=={video_id}",
            )
            .execute()
        )
        if linhas_imp := imp.get("rows"):
            m.impressoes = int(linhas_imp[0][0])
            m.ctr = float(linhas_imp[0][1]) / 100.0
    except Exception as e:
        log.warning("metricas de impressao indisponiveis: %s", e)

    return m
