#!/usr/bin/env python3
"""Governador do WhatsApp automático — no máximo ~15 envios por dia, espalhados.

Regra do dono (27/09 21:00): WhatsApp automático não pode sair em lote. No máximo
15 por dia, espalhados ao longo do horário comercial, com a quantidade do dia
variando; o que passar do limite fica manual, com o SDR.

Como funciona (contrato com os workflows):
  1. Antes de cada WhatsApp automático de prospecção, o workflow aplica a tag
     `wa-aguardando` e espera (Wait for condition) a tag `wa-liberado`, com
     timeout de 4 h dentro da janela.
  2. Este script roda a cada 30 min (seg-sex, 08:30-18:30 America/Sao_Paulo).
     Ele sorteia a meta do dia (11 a 15, fixa por data), calcula quantos já
     deveriam ter saído até agora e libera no máximo 1 ou 2 por rodada: tira
     `wa-aguardando`, põe `wa-liberado` e a tag do dia `wa-lib-AAAA-MM-DD`
     (é por ela que o script conta o que já saiu hoje).
  3. O workflow, ao ver `wa-liberado`, envia e remove `wa-liberado`. Se der
     timeout, remove `wa-aguardando` e cria tarefa "[WHATSAPP MANUAL]" para o
     SDR com o texto da mensagem.

Leitura e escrita só por tags, pela API pública. Nada é apagado. Ordem de
liberação: quem está esperando há mais tempo (dateUpdated mais antigo) primeiro.

Uso:
  python wa_governador.py            # ensaio: mostra o que faria
  python wa_governador.py --aplicar  # libera de verdade
"""
from __future__ import annotations

import datetime as dt
import hashlib
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from campos_bant import ghl, LOC  # noqa: E402

AGUARDA, LIBERADO = "wa-aguardando", "wa-liberado"
META_MIN, META_MAX = 11, 15
INICIO, FIM = (8, 30), (18, 30)          # horário de Brasília
POR_RODADA = 2
BRT = dt.timezone(dt.timedelta(hours=-3))


def contatos() -> list:
    todos, depois = [], None
    while True:
        corpo = {"locationId": LOC, "pageLimit": 100}
        if depois:
            corpo["searchAfter"] = depois
        st, r = ghl("POST", "/contacts/search", corpo)
        lote = r.get("contacts") or []
        todos += lote
        if not lote or len(todos) >= (r.get("total") or 0):
            return todos
        depois = lote[-1].get("searchAfter")
        if not depois:
            return todos


def meta_do_dia(hoje: dt.date) -> int:
    h = int(hashlib.sha256(hoje.isoformat().encode()).hexdigest(), 16)
    return META_MIN + h % (META_MAX - META_MIN + 1)


def fracao_do_dia(agora: dt.datetime) -> float:
    ini = agora.replace(hour=INICIO[0], minute=INICIO[1], second=0, microsecond=0)
    fim = agora.replace(hour=FIM[0], minute=FIM[1], second=0, microsecond=0)
    if agora <= ini:
        return 0.0
    if agora >= fim:
        return 1.0
    return (agora - ini) / (fim - ini)


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(BRT)
    hoje = agora.date()
    so = sys.argv[sys.argv.index("--so") + 1] if "--so" in sys.argv else None
    if so:
        # teste de um contato só (27/09): ignora dia e janela e libera só esse contato
        cs = [c for c in contatos() if c["id"] == so and AGUARDA in (c.get("tags") or [])]
        for c in cs:
            if aplicar:
                ghl("DELETE", "/contacts/%s/tags" % c["id"], {"tags": [AGUARDA]})
                ghl("POST", "/contacts/%s/tags" % c["id"],
                    {"tags": [LIBERADO, "wa-lib-" + hoje.isoformat()]})
            print("teste --so: %s %s" % ("liberado" if aplicar else "liberaria", c["id"]))
        if not cs:
            print("teste --so: contato não está em %s" % AGUARDA)
        return 0
    if hoje.weekday() >= 5:
        print("fim de semana: nada a liberar")
        return 0
    tag_dia = "wa-lib-" + hoje.isoformat()
    meta = meta_do_dia(hoje)
    cs = contatos()
    ja = [c for c in cs if tag_dia in (c.get("tags") or [])]
    fila = sorted([c for c in cs if AGUARDA in (c.get("tags") or [])],
                  key=lambda c: c.get("dateUpdated") or "")
    devido = round(meta * fracao_do_dia(agora))
    soltar = max(0, min(POR_RODADA, devido - len(ja), meta - len(ja), len(fila)))
    print("hoje %s | meta %d | ja liberados %d | devido ate agora %d | na fila %d | libera agora %d"
          % (hoje, meta, len(ja), devido, len(fila), soltar))
    for c in fila[:soltar]:
        nome = c.get("firstName") or c.get("contactName") or c["id"]
        if aplicar:
            ghl("DELETE", "/contacts/%s/tags" % c["id"], {"tags": [AGUARDA]})
            ghl("POST", "/contacts/%s/tags" % c["id"], {"tags": [LIBERADO, tag_dia]})
        print("  %s %s (%s)" % ("liberado" if aplicar else "liberaria", nome, c["id"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
