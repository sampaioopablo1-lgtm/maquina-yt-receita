"""Persistencia de estado.

SQLite local por padrao (funciona offline e no runner). O mesmo schema roda no
Supabase — ver `supabase/schema.sql`. O runner do Actions e efemero, entao em
producao o estado deve viver no Supabase; o SQLite serve para rodar local e para
o job nao perder contexto no meio da execucao.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterator

from .models import Metricas, Status, Video

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
    slug        TEXT PRIMARY KEY,
    status      TEXT NOT NULL,
    formato     TEXT NOT NULL,
    titulo      TEXT,
    youtube_id  TEXT,
    payload     TEXT NOT NULL,
    criado_em   TEXT NOT NULL,
    publicado_em TEXT
);
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_publicado ON videos(publicado_em);

CREATE TABLE IF NOT EXISTS metricas (
    youtube_id  TEXT NOT NULL,
    coletado_em TEXT NOT NULL,
    payload     TEXT NOT NULL,
    PRIMARY KEY (youtube_id, coletado_em)
);
"""


class Store:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.path = db_path
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def salvar(self, video: Video) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO videos
                   (slug, status, formato, titulo, youtube_id, payload, criado_em, publicado_em)
                   VALUES (?,?,?,?,?,?,?,?)
                   ON CONFLICT(slug) DO UPDATE SET
                     status=excluded.status, titulo=excluded.titulo,
                     youtube_id=excluded.youtube_id, payload=excluded.payload,
                     publicado_em=excluded.publicado_em""",
                (
                    video.slug,
                    video.status.value,
                    video.formato.value,
                    video.roteiro.titulo if video.roteiro else (video.ideia.titulo if video.ideia else None),
                    video.youtube_id,
                    video.model_dump_json(),
                    video.criado_em.isoformat(),
                    video.publicado_em.isoformat() if video.publicado_em else None,
                ),
            )

    def obter(self, slug: str) -> Video | None:
        with self._conn() as c:
            row = c.execute("SELECT payload FROM videos WHERE slug=?", (slug,)).fetchone()
        return Video.model_validate_json(row["payload"]) if row else None

    def listar(self, status: Status | None = None, limite: int = 50) -> list[Video]:
        q = "SELECT payload FROM videos"
        args: tuple = ()
        if status:
            q += " WHERE status=?"
            args = (status.value,)
        q += " ORDER BY criado_em DESC LIMIT ?"
        with self._conn() as c:
            rows = c.execute(q, (*args, limite)).fetchall()
        return [Video.model_validate_json(r["payload"]) for r in rows]

    def publicados_hoje(self) -> int:
        hoje = date.today().isoformat()
        with self._conn() as c:
            row = c.execute(
                "SELECT COUNT(*) n FROM videos WHERE publicado_em LIKE ?", (f"{hoje}%",)
            ).fetchone()
        return int(row["n"])

    def roteiros_recentes(self, limite: int = 20) -> list[tuple[str, str]]:
        """(titulo, texto do roteiro) dos ultimos videos — base da checagem de similaridade."""
        with self._conn() as c:
            rows = c.execute(
                "SELECT payload FROM videos ORDER BY criado_em DESC LIMIT ?", (limite,)
            ).fetchall()
        saida = []
        for r in rows:
            v = Video.model_validate_json(r["payload"])
            if v.roteiro:
                saida.append((v.roteiro.titulo, v.roteiro.texto_completo))
        return saida

    def salvar_metricas(self, m: Metricas) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR REPLACE INTO metricas (youtube_id, coletado_em, payload) VALUES (?,?,?)",
                (m.youtube_id, m.coletado_em.isoformat(), m.model_dump_json()),
            )

    def ultimas_metricas(self, youtube_id: str) -> Metricas | None:
        with self._conn() as c:
            row = c.execute(
                "SELECT payload FROM metricas WHERE youtube_id=? ORDER BY coletado_em DESC LIMIT 1",
                (youtube_id,),
            ).fetchone()
        return Metricas.model_validate_json(row["payload"]) if row else None

    def titulos_publicados(self) -> list[str]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT titulo FROM videos WHERE titulo IS NOT NULL"
            ).fetchall()
        return [r["titulo"] for r in rows]
