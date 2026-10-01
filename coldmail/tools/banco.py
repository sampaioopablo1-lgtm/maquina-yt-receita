"""Estado da máquina: leads, envios, mensagens lidas e lista de bloqueio.

Duas implementações com a mesma interface mínima (inserir / buscar / atualizar):
  - Supabase (PostgREST) quando SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY estão no ambiente. É o que roda
    no GitHub Actions: o runner é efêmero e o repositório é público, então nenhum dado de lead fica em
    arquivo do repo. Tabelas em coldmail/schema.sql.
  - SQLite local (coldmail/.local/coldmail.db, fora do git) para testar no PC sem nada configurado.

Filtros: lista de (coluna, operador, valor), operadores eq, neq, lte, gte, lt, in.
"""
from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TABELAS_SQLITE = """
create table if not exists cold_leads (
    id integer primary key autoincrement,
    email text not null unique,
    primeiro_nome text, empresa text, cargo text, site text, abertura text, extra text,
    status text not null default 'ativo',
    passo integer not null default 0,
    proximo_envio text,
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

CHAVE = {"cold_leads": "email", "cold_mensagens": "message_id", "cold_bloqueio": "email"}
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


class Supabase:
    def __init__(self, url: str, chave: str):
        self.base = url.rstrip("/") + "/rest/v1/"
        self.chave = chave

    def _pedir(self, metodo: str, caminho: str, corpo=None, prefer: str = ""):
        dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
        req = urllib.request.Request(self.base + caminho, data=dados, method=metodo)
        req.add_header("apikey", self.chave)
        req.add_header("Authorization", "Bearer " + self.chave)
        req.add_header("Content-Type", "application/json")
        if prefer:
            req.add_header("Prefer", prefer)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read().decode("utf-8")
                return json.loads(t) if t else None
        except urllib.error.HTTPError as e:
            det = e.read().decode("utf-8", "replace")[:300]
            raise SystemExit("Supabase %s %s -> HTTP %s %s" % (metodo, caminho.split("?")[0], e.code, det))

    @staticmethod
    def _filtros(filtros) -> list[tuple[str, str]]:
        q = []
        for col, op, val in filtros or []:
            if op == "in":
                vals = ",".join('"%s"' % str(v).replace('"', "") for v in val)
                q.append((col, "in.(%s)" % vals))
            else:
                q.append((col, "%s.%s" % (op, val)))
        return q

    def inserir(self, tabela: str, linhas: list[dict]) -> int:
        n = 0
        for i in range(0, len(linhas), 500):
            lote = linhas[i:i + 500]
            caminho = tabela
            if tabela in CHAVE:
                caminho += "?on_conflict=" + CHAVE[tabela]
            r = self._pedir("POST", caminho, lote, "resolution=ignore-duplicates,return=representation")
            n += len(r or [])
        return n

    def buscar(self, tabela: str, filtros=None, ordem: str | None = None, limite: int | None = None,
               colunas: str = "*") -> list[dict]:
        q = [("select", colunas)] + self._filtros(filtros)
        if ordem:
            q.append(("order", ordem))
        if limite:
            q.append(("limit", str(limite)))
        return self._pedir("GET", tabela + "?" + urllib.parse.urlencode(q)) or []

    def atualizar(self, tabela: str, filtros, campos: dict) -> None:
        q = urllib.parse.urlencode(self._filtros(filtros))
        self._pedir("PATCH", tabela + "?" + q, campos, "return=minimal")


LOCAL = Path(__file__).resolve().parents[1] / ".local" / "coldmail.db"


def abrir(exigir_remoto: bool = False):
    url, chave = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if url and chave:
        return Supabase(url, chave)
    if exigir_remoto:
        raise SystemExit("sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY: no Actions o estado precisa ficar no "
                         "Supabase (o runner apaga tudo ao terminar).")
    return Sqlite(LOCAL)
