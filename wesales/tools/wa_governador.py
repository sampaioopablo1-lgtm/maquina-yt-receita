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

AGUARDA, LIBERADO, MANUAL = "wa-aguardando", "wa-liberado", "wa-manual"
# FIM DA ESPERA (27/09): a conta não tem nó de "esperar condição com tempo limite" para
# copiar, e a trava nos workflows é um laço (tem wa-liberado? tem wa-manual? senão espera
# 15 min). Quem encerra a espera é este script, aplicando `wa-manual` (o workflow então
# cria a tarefa [WHATSAPP MANUAL]):
#   - as vagas que restam no dia (meta - já liberados) ficam reservadas para os primeiros
#     da fila, que saem espalhados até 18:30;
#   - quem passa das vagas vira manual NA HORA (a SDR manda cedo, em vez de esperar);
#   - às 18:30, o que ainda estiver esperando vira manual.
# Simulado para 36 entradas às 08:30: 14 automáticos espalhados + 22 manuais às 08:30.
META_MIN, META_MAX = 11, 15
INICIO, FIM = (8, 30), (18, 30)          # horário de Brasília (padrão; o dia usa equipe.json)
# 28/09: a janela do dia vem dos turnos das SDRs (equipe.json): do início do primeiro turno a
# 30 min antes do fim do último, para a tarefa [WHATSAPP MANUAL] ainda cair com alguém em turno.
try:
    from turnos import janela as _janela_turnos
except Exception:  # sem o arquivo, fica o padrão
    _janela_turnos = None


def _janela(dia):
    global INICIO, FIM
    j = _janela_turnos(dia) if _janela_turnos else None
    if j:
        ini, (fh, fm) = j
        fim_min = fh * 60 + fm - 30
        INICIO, FIM = ini, (fim_min // 60, fim_min % 60)
POR_RODADA = 1   # 28/09: 1 por rodada + rodadas puladas ao acaso = envios espaçados, sem intervalo fixo
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
    _janela(hoje)
    tag_dia = "wa-lib-" + hoje.isoformat()
    meta = meta_do_dia(hoje)
    cs = contatos()
    ini = agora.replace(hour=INICIO[0], minute=INICIO[1], second=0, microsecond=0)
    fim = agora.replace(hour=FIM[0], minute=FIM[1], second=0, microsecond=0)
    if agora < ini:
        print("antes das %02d:%02d: nada a fazer" % INICIO)
        return 0

    def tags(c):
        return c.get("tags") or []

    ja = [c for c in cs if tag_dia in tags(c)]
    fila = sorted([c for c in cs if AGUARDA in tags(c) and MANUAL not in tags(c)],
                  key=lambda c: c.get("dateUpdated") or "")
    vagas = 0 if agora >= fim else max(0, meta - len(ja))
    for c in fila[vagas:]:
        nome = c.get("firstName") or c.get("contactName") or c["id"]
        if aplicar:
            ghl("POST", "/contacts/%s/tags" % c["id"], {"tags": [MANUAL]})
        print("  %s %s (%s): sem vaga automática hoje, vira WhatsApp manual"
              % ("manual" if aplicar else "iria para manual", nome, c["id"]))
    fila = fila[:vagas]
    if agora >= fim:
        print("depois das %02d:%02d: nada mais a liberar hoje" % FIM)
        return 0
    devido = round(meta * fracao_do_dia(agora))
    soltar = max(0, min(POR_RODADA, devido - len(ja), meta - len(ja), len(fila)))
    # 28/09 (dono): o WhatsApp não pode perceber padrão de robô. Pula ~1/3 das rodadas ao acaso
    # (só quando não está atrasado em relação à meta do dia), então o intervalo entre envios
    # varia (30, 60, 90 min), somado à espera de 15 min do portão em cada workflow.
    import random
    if soltar and devido - len(ja) <= 1 and random.random() < 0.35:
        print("  rodada pulada ao acaso (intervalo irregular entre envios)")
        soltar = 0
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
