"""Turnos da equipe, lidos de `wesales/equipe.json` (pedido do dono, 28/09: SDRs em turnos
diferentes, 09:00-18:00 e 13:00-21:00, e closers). Usado pelo governador do WhatsApp (janela
de envio automático) e pelo atuador das filas (lead novo vai para uma SDR em turno)."""
import datetime as dt
import json
import os

BRT = dt.timezone(dt.timedelta(hours=-3))
ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "equipe.json")


def equipe() -> dict:
    with open(ARQ, encoding="utf-8") as f:
        return json.load(f)


def _hm(s):
    h, m = s.split(":")
    return int(h), int(m)


def janela(dia: dt.date, papel="sdrs"):
    """(início, fim) do dia = começo do primeiro turno e fim do último, entre todos os turnos
    cadastrados (mesmo sem userId: o horário da operação já está decidido). None se ninguém
    trabalha nesse dia."""
    ts = [p["turno"] for p in equipe()[papel] if dia.isoweekday() in p["turno"]["dias"]]
    if not ts:
        return None
    return min(_hm(t["inicio"]) for t in ts), max(_hm(t["fim"]) for t in ts)


def em_turno(agora: dt.datetime, papel="sdrs") -> list:
    """userIds de quem está em turno agora (só quem já tem usuário no CRM)."""
    agora = agora.astimezone(BRT)
    hm = (agora.hour, agora.minute)
    return [p["userId"] for p in equipe()[papel] if p.get("userId")
            and agora.isoweekday() in p["turno"]["dias"]
            and _hm(p["turno"]["inicio"]) <= hm < _hm(p["turno"]["fim"])]


def ids(papel="sdrs") -> list:
    return [p["userId"] for p in equipe()[papel] if p.get("userId")]
