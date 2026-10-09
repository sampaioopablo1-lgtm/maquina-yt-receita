"""Persistencia de estado.

SQLite local por padrao (funciona offline). O mesmo schema roda no Supabase —
ver supabase/migrations/ — para sobreviver a um runner efemero.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from .models import Lead, Mensagem, Reuniao, StatusLead

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id               TEXT PRIMARY KEY,
    status           TEXT NOT NULL,
    etapa_sequencia  INTEGER NOT NULL DEFAULT 0,
    proxima_acao_em  TEXT,
    payload          TEXT NOT NULL,
    criado_em        TEXT NOT NULL,
    atualizado_em    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_proxima_acao ON leads(proxima_acao_em);

CREATE TABLE IF NOT EXISTS mensagens (
    lead_id     TEXT NOT NULL,
    canal       TEXT NOT NULL,
    etapa       INTEGER NOT NULL,
    texto       TEXT NOT NULL,
    resposta    INTEGER NOT NULL DEFAULT 0,
    enviado_em  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_mensagens_lead ON mensagens(lead_id);

CREATE TABLE IF NOT EXISTS reunioes (
    lead_id            TEXT NOT NULL,
    inicio             TEXT NOT NULL,
    fim                TEXT NOT NULL,
    calendar_event_id  TEXT,
    meet_url           TEXT,
    criado_em          TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reunioes_lead ON reunioes(lead_id);

CREATE TABLE IF NOT EXISTS envios_dia (
    dia    TEXT NOT NULL,
    canal  TEXT NOT NULL,
    tipo   TEXT NOT NULL,  -- 'convite' | 'mensagem' | 'lead_novo'
    total  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (dia, canal, tipo)
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

    # ---- leads ----

    def salvar_lead(self, lead: Lead) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO leads
                   (id, status, etapa_sequencia, proxima_acao_em, payload, criado_em, atualizado_em)
                   VALUES (?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET
                     status=excluded.status, etapa_sequencia=excluded.etapa_sequencia,
                     proxima_acao_em=excluded.proxima_acao_em, payload=excluded.payload,
                     atualizado_em=excluded.atualizado_em""",
                (
                    lead.id,
                    lead.status.value,
                    lead.etapa_sequencia,
                    lead.proxima_acao_em.isoformat() if lead.proxima_acao_em else None,
                    lead.model_dump_json(),
                    lead.criado_em.isoformat(),
                    lead.atualizado_em.isoformat(),
                ),
            )

    def lead(self, lead_id: str) -> Lead | None:
        with self._conn() as c:
            row = c.execute("SELECT payload FROM leads WHERE id=?", (lead_id,)).fetchone()
        return Lead.model_validate_json(row["payload"]) if row else None

    def existe(self, lead_id: str) -> bool:
        with self._conn() as c:
            row = c.execute("SELECT 1 FROM leads WHERE id=?", (lead_id,)).fetchone()
        return row is not None

    def leads_por_status(self, status: StatusLead) -> list[Lead]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT payload FROM leads WHERE status=? ORDER BY criado_em", (status.value,)
            ).fetchall()
        return [Lead.model_validate_json(r["payload"]) for r in rows]

    def leads_com_acao_pendente(self, ate: datetime) -> list[Lead]:
        with self._conn() as c:
            rows = c.execute(
                """SELECT payload FROM leads
                   WHERE proxima_acao_em IS NOT NULL AND proxima_acao_em <= ?
                     AND status IN ('novo','em_sequencia')
                   ORDER BY proxima_acao_em""",
                (ate.isoformat(),),
            ).fetchall()
        return [Lead.model_validate_json(r["payload"]) for r in rows]

    def funil(self) -> dict[str, int]:
        with self._conn() as c:
            rows = c.execute("SELECT status, COUNT(*) n FROM leads GROUP BY status").fetchall()
        return {r["status"]: r["n"] for r in rows}

    # ---- mensagens ----

    def salvar_mensagem(self, msg: Mensagem) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO mensagens (lead_id, canal, etapa, texto, resposta, enviado_em)
                   VALUES (?,?,?,?,?,?)""",
                (
                    msg.lead_id,
                    msg.canal.value,
                    msg.etapa,
                    msg.texto,
                    int(msg.resposta),
                    msg.enviado_em.isoformat(),
                ),
            )

    # ---- reunioes ----

    def salvar_reuniao(self, r: Reuniao) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO reunioes (lead_id, inicio, fim, calendar_event_id, meet_url, criado_em)
                   VALUES (?,?,?,?,?,?)""",
                (r.lead_id, r.inicio.isoformat(), r.fim.isoformat(), r.calendar_event_id, r.meet_url, r.criado_em.isoformat()),
            )

    # ---- limites diarios ----

    def contagem_hoje(self, dia: str, canal: str, tipo: str) -> int:
        with self._conn() as c:
            row = c.execute(
                "SELECT total FROM envios_dia WHERE dia=? AND canal=? AND tipo=?",
                (dia, canal, tipo),
            ).fetchone()
        return row["total"] if row else 0

    def incrementar_contagem(self, dia: str, canal: str, tipo: str) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO envios_dia (dia, canal, tipo, total) VALUES (?,?,?,1)
                   ON CONFLICT(dia, canal, tipo) DO UPDATE SET total = total + 1""",
                (dia, canal, tipo),
            )
