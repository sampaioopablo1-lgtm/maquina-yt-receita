"""Estado da máquina: leads, envios, mensagens lidas e lista de bloqueio, num arquivo SQLite.

No GitHub Actions o arquivo fica no repositório PRIVADO de dados (COLDMAIL_DB aponta para o clone dele;
o workflow faz commit a cada ciclo). Este repositório é público: nenhum dado de lead entra aqui.
No PC, sem COLDMAIL_DB, fica em coldmail/.local/coldmail.db (fora do git).

Filtros: lista de (coluna, operador, valor), operadores eq, neq, lte, gte, lt, in.
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

TABELAS_SQLITE = """
create table if not exists cold_leads (
    id integer primary key autoincrement,
    email text not null unique,
    primeiro_nome text, empresa text, cargo text, site text, abertura text, extra text,
    status text not null default 'ativo',
    passo integer not null default 0,
    proximo_envio text default (strftime('%Y-%m-%dT%H:%M:%S+00:00', 'now')),
    conta text, assunto text, thread_msgid text, ultimo_msgid text,
    categoria text, ghl_contato text,
    criado_em text default (strftime('%Y-%m-%dT%H:%M:%S+00:00', 'now')),
    atualizado_em text
);
create table if not exists cold_envios (
    id integer primary key autoincrement,
    lead_id integer not null, conta text not null, passo integer not null,
    message_id text not null, enviado_em text not null
);
create table if not exists cold_mensagens (
    message_id text primary key,
    lead_id integer, conta text not null, recebido_em text not null,
    tipo text not null, categoria text, confianca real, acao text
);
create table if not exists cold_bloqueio (
    email text primary key, motivo text,
    criado_em text default (strftime('%Y-%m-%dT%H:%M:%S+00:00', 'now'))
);
"""

OPS_SQL = {"eq": "=", "neq": "!=", "lte": "<=", "gte": ">=", "lt": "<"}


class Sqlite:
    def __init__(self, caminho: str | Path = ":memory:"):
        if caminho != ":memory:":
            Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(caminho))
        self.db.row_factory = sqlite3.Row
        self.db.executescript(TABELAS_SQLITE)

    def _onde(self, filtros):
        partes, args = [], []
        for col, op, val in filtros or []:
            if op == "in":
                vals = list(val)
                if not vals:
                    partes.append("0")
                    continue
                partes.append("%s in (%s)" % (col, ",".join("?" * len(vals))))
                args.extend(vals)
            else:
                partes.append("%s %s ?" % (col, OPS_SQL[op]))
                args.append(val)
        return (" where " + " and ".join(partes)) if partes else "", args

    def inserir(self, tabela: str, linhas: list[dict]) -> int:
        n = 0
        for linha in linhas:
            cols = list(linha)
            cur = self.db.execute("insert or ignore into %s (%s) values (%s)" % (
                tabela, ",".join(cols), ",".join("?" * len(cols))), [linha[c] for c in cols])
            n += cur.rowcount
        self.db.commit()
        return n

    def buscar(self, tabela: str, filtros=None, ordem: str | None = None, limite: int | None = None,
               colunas: str = "*") -> list[dict]:
        onde, args = self._onde(filtros)
        sql = "select %s from %s%s" % (colunas, tabela, onde)
        if ordem:
            sql += " order by " + ordem.replace(".asc", " asc").replace(".desc", " desc")
        if limite:
            sql += " limit %d" % limite
        return [dict(r) for r in self.db.execute(sql, args)]

    def atualizar(self, tabela: str, filtros, campos: dict) -> None:
        onde, args = self._onde(filtros)
        cols = list(campos)
        self.db.execute("update %s set %s%s" % (tabela, ",".join("%s = ?" % c for c in cols), onde),
                        [campos[c] for c in cols] + args)
        self.db.commit()


LOCAL = Path(__file__).resolve().parents[1] / ".local" / "coldmail.db"


def abrir(exigir_remoto: bool = False) -> Sqlite:
    """COLDMAIL_DB aponta para o banco dentro do clone do repositório PRIVADO de dados (no Actions);
    sem ela, banco local fora do git."""
    caminho = os.environ.get("COLDMAIL_DB")
    if caminho:
        return Sqlite(caminho)
    if exigir_remoto:
        raise SystemExit("sem COLDMAIL_DB: no Actions o banco precisa ficar no repositório privado de dados "
                         "(o runner apaga tudo ao terminar, e este repositório é público).")
    return Sqlite(LOCAL)
