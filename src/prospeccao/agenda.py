"""Logica de agendamento — o "Calendly proprio" citado no README.

`horarios_disponiveis` devolve os slots livres (Google Calendar real, ou
sinteticos no modo stub) e `confirmar` fecha a reuniao: cria o evento no
calendario, grava em Store e atualiza o status do lead."""

from __future__ import annotations

from datetime import datetime, timezone

from .config import Config
from .models import Lead, Reuniao, StatusLead
from .providers import fabrica
from .storage import Store


def horarios_disponiveis(cfg: Config, dias_a_frente: int = 14) -> list[tuple[datetime, datetime]]:
    cal = fabrica.calendario(cfg)
    return cal.horarios_livres(cfg.disponibilidade, dias_a_frente)


def confirmar(cfg: Config, store: Store, lead_id: str, inicio: datetime, fim: datetime) -> Reuniao:
    lead = store.lead(lead_id)
    if lead is None:
        raise ValueError(f"lead {lead_id} nao encontrado")

    cal = fabrica.calendario(cfg)
    event_id, meet_url = cal.criar_evento(lead, inicio, fim)

    reuniao = Reuniao(lead_id=lead_id, inicio=inicio, fim=fim, calendar_event_id=event_id, meet_url=meet_url)
    store.salvar_reuniao(reuniao)

    lead.status = StatusLead.REUNIAO_MARCADA
    lead.proxima_acao_em = None
    lead.atualizado_em = datetime.now(timezone.utc)
    store.salvar_lead(lead)
    return reuniao
