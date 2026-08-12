"""Espelha o estado local no Supabase e traz de volta o que nasceu la.

O runner do Actions e efemero: sem isto o historico morre com o job e as views
`painel_pilares` / `progresso_ypp` ficam vazias para sempre. Na outra direcao, a
Edge Function `gerar-roteiro` grava roteiros direto no banco — puxar traz esses
videos para o SQLite, onde `maquina retomar <slug>` sabe continuar.

Regra de conflito, deliberadamente assimetrica:
- empurrar sobrescreve o remoto (o Supabase e espelho do que o job produziu);
- puxar so cria o que nao existe local (nunca sobrescreve trabalho em andamento).

Sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY o modulo e inerte — a pipeline
continua rodando so com SQLite, como antes.
"""

from __future__ import annotations

import logging
import os

import httpx

from .models import Metricas, Video
from .storage import Store

log = logging.getLogger("maquina.sincronizacao")

TIMEOUT = 30.0


class ErroSincronizacao(RuntimeError):
    pass


def configurado() -> bool:
    return bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"))


def _cliente() -> httpx.Client:
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    chave = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not chave:
        raise ErroSincronizacao(
            "SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY ausentes — "
            "veja docs/01-arquitetura.md"
        )
    return httpx.Client(
        base_url=f"{url}/rest/v1",
        headers={
            "apikey": chave,
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
        },
        timeout=TIMEOUT,
    )


def _linha_video(v: Video) -> dict:
    # `canal` so entra quando existe. Mandar None faria o upsert SOBRESCREVER
    # com NULL o canal que a linha ja tinha no Supabase — e os payloads locais
    # foram gravados antes do campo existir, entao quase todos vem sem ele.
    # Medido em 2026-08-12: o primeiro sync depois de eu adicionar o campo
    # apagou o canal de linhas que estavam corretas, inclusive labtreinamento-001.
    linha = {
        "slug": v.slug,
        "status": v.status.value,
        "formato": v.formato.value,
        "titulo": v.roteiro.titulo if v.roteiro else (v.ideia.titulo if v.ideia else None),
        "youtube_id": v.youtube_id,
        "roteiro": v.roteiro.model_dump(mode="json") if v.roteiro else None,
        "duracao_s": v.duracao_s,
        "custo_usd": v.custo_usd,
        "erro": v.erro,
        "criado_em": v.criado_em.isoformat(),
        "publicado_em": v.publicado_em.isoformat() if v.publicado_em else None,
        "agendado_para": v.agendado_para.isoformat() if v.agendado_para else None,
    }
    if v.canal:
        linha["canal"] = v.canal
    return linha


def _linha_metrica(m: Metricas) -> dict:
    return {
        "youtube_id": m.youtube_id,
        "coletado_em": m.coletado_em.isoformat(),
        "impressoes": m.impressoes,
        "views": m.views,
        "ctr": m.ctr,
        "retencao_media_pct": m.retencao_media_pct,
        "duracao_media_s": m.duracao_media_s,
        "inscritos_ganhos": m.inscritos_ganhos,
        "receita_estimada_usd": m.receita_estimada_usd,
    }


def _upsert(cli: httpx.Client, tabela: str, linhas: list[dict], on_conflict: str) -> None:
    if not linhas:
        return
    r = cli.post(
        f"/{tabela}",
        params={"on_conflict": on_conflict},
        headers={"Prefer": "resolution=merge-duplicates,return=minimal"},
        json=linhas,
    )
    if r.status_code >= 400:
        raise ErroSincronizacao(f"{tabela} {r.status_code}: {r.text[:300]}")


def empurrar(store: Store) -> tuple[int, int]:
    """Manda videos e metricas locais para o Supabase. Devolve (videos, metricas)."""
    videos = store.listar(limite=10_000)
    # Videos primeiro: metricas.youtube_id tem FK para videos.youtube_id.
    linhas_v = [_linha_video(v) for v in videos]
    ids = [v.youtube_id for v in videos if v.youtube_id]
    linhas_m = [_linha_metrica(m) for m in store.todas_metricas()]
    # Metrica de video ausente no lote violaria a FK e derrubaria o job inteiro.
    linhas_m = [m for m in linhas_m if m["youtube_id"] in ids]

    with _cliente() as cli:
        _upsert(cli, "videos", linhas_v, "slug")
        _upsert(cli, "metricas", linhas_m, "youtube_id,coletado_em")
    return len(linhas_v), len(linhas_m)


def puxar(store: Store) -> list[str]:
    """Traz videos que so existem no Supabase (ex.: roteiro da Edge Function).

    Nunca sobrescreve um slug ja presente local. Devolve os slugs criados.
    """
    conhecidos = {v.slug for v in store.listar(limite=10_000)}
    with _cliente() as cli:
        r = cli.get("/videos", params={"select": "*", "roteiro": "not.is.null"})
    if r.status_code >= 400:
        raise ErroSincronizacao(f"videos {r.status_code}: {r.text[:300]}")

    novos: list[str] = []
    for linha in r.json():
        if linha["slug"] in conhecidos:
            continue
        try:
            video = Video.model_validate(
                {
                    "slug": linha["slug"],
                    "formato": linha["formato"],
                    "status": linha["status"],
                    "roteiro": linha["roteiro"],
                    "youtube_id": linha.get("youtube_id"),
                    "duracao_s": linha.get("duracao_s"),
                    "custo_usd": linha.get("custo_usd") or 0.0,
                    "erro": linha.get("erro"),
                    "criado_em": linha["criado_em"],
                    "publicado_em": linha.get("publicado_em"),
                    "agendado_para": linha.get("agendado_para"),
                }
            )
        except Exception as e:
            log.warning("slug %s ignorado (%s)", linha.get("slug"), e)
            continue
        store.salvar(video)
        novos.append(video.slug)
    return novos
