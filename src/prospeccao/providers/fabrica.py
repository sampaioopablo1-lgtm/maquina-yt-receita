"""Selecao de provider com degradacao para stub.

Regra: se a credencial nao existe (ou, no caso do LinkedIn, se o risco nao foi
aceito explicitamente), o pipeline nao quebra — ele avisa e continua offline.
"""

from __future__ import annotations

import logging
import os

from ..config import Config
from .base import BuscadorLeads, Calendario, EnviadorEmail, AutomacaoLinkedIn, ErroProvider
from .stubs import BuscadorLeadsStub, CalendarioStub, EmailStub, LinkedInStub

log = logging.getLogger("prospeccao.providers")


def _tentar(nome: str, fabrica, stub):
    try:
        return fabrica()
    except ErroProvider as e:
        log.warning("provider %s indisponivel (%s) — usando stub offline", nome, e)
        return stub


def buscador_leads(cfg: Config) -> BuscadorLeads:
    if cfg.leads_provider == "stub":
        return BuscadorLeadsStub()
    if cfg.leads_provider in ("auto", "apollo"):
        from .reais import BuscadorLeadsApollo

        return _tentar("apollo", BuscadorLeadsApollo, BuscadorLeadsStub())
    raise ValueError(f"leads_provider desconhecido: {cfg.leads_provider}")


def enviador_email(cfg: Config) -> EnviadorEmail:
    if cfg.email_provider == "stub":
        return EmailStub()
    if cfg.email_provider in ("auto", "resend") and os.getenv("RESEND_API_KEY"):
        from .reais import EmailResend

        return _tentar("resend", EmailResend, EmailStub())
    if cfg.email_provider in ("auto", "smtp"):
        from .reais import EmailSMTP

        return _tentar("smtp", EmailSMTP, EmailStub())
    return EmailStub()


def automacao_linkedin(cfg: Config) -> AutomacaoLinkedIn:
    if cfg.linkedin_provider == "stub":
        return LinkedInStub()
    if cfg.linkedin_provider in ("auto", "playwright"):
        from .linkedin_playwright import AutomacaoLinkedInPlaywright

        return _tentar("linkedin-playwright", AutomacaoLinkedInPlaywright, LinkedInStub())
    raise ValueError(f"linkedin_provider desconhecido: {cfg.linkedin_provider}")


def calendario(cfg: Config) -> Calendario:
    if cfg.calendario_provider == "stub":
        return CalendarioStub()
    if cfg.calendario_provider in ("auto", "google"):
        from .reais import CalendarioGoogle

        return _tentar("google-calendar", CalendarioGoogle, CalendarioStub())
    raise ValueError(f"calendario_provider desconhecido: {cfg.calendario_provider}")
