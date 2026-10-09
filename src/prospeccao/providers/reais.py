"""Providers reais. Cada um exige credencial propria (ver .env.example) e
lanca ErroProvider se a chamada falhar — quem instancia decide se cai para o
stub (ver providers/fabrica.py)."""

from __future__ import annotations

import logging
import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

import httpx

from ..models import ICP, Disponibilidade, Lead
from .base import ErroProvider

log = logging.getLogger("prospeccao.providers.reais")


# ---------------------------------------------------------------------------
# Leads: Apollo.io People Search API
# ---------------------------------------------------------------------------


class BuscadorLeadsApollo:
    """https://docs.apollo.io/reference/people-search"""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.getenv("APOLLO_API_KEY", "")
        if not self.api_key:
            raise ErroProvider("APOLLO_API_KEY ausente")

    def buscar(self, icp: ICP, limite: int) -> list[Lead]:
        payload: dict = {
            "page": 1,
            "per_page": min(limite, 100),
        }
        if icp.cargos:
            payload["person_titles"] = icp.cargos
        if icp.setores:
            payload["q_organization_industries"] = icp.setores
        if icp.tamanho_empresa:
            payload["organization_num_employees_ranges"] = [icp.tamanho_empresa]
        if icp.localizacao:
            payload["person_locations"] = [icp.localizacao]
        if icp.palavras_chave:
            payload["q_keywords"] = " ".join(icp.palavras_chave)

        try:
            resp = httpx.post(
                "https://api.apollo.io/api/v1/mixed_people/search",
                json=payload,
                headers={"x-api-key": self.api_key, "Content-Type": "application/json"},
                timeout=30,
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ErroProvider(f"Apollo falhou: {e}") from e

        dados = resp.json()
        leads: list[Lead] = []
        for pessoa in dados.get("people", [])[:limite]:
            org = pessoa.get("organization") or {}
            leads.append(
                Lead(
                    nome=pessoa.get("name", "").strip() or "Sem nome",
                    cargo=pessoa.get("title", ""),
                    empresa=org.get("name", ""),
                    setor=", ".join(org.get("industries") or []) if org.get("industries") else "",
                    localizacao=pessoa.get("city", "") or pessoa.get("country", ""),
                    linkedin_url=pessoa.get("linkedin_url", ""),
                    email=pessoa.get("email", "") or "",
                    origem="apollo",
                )
            )
        log.info("Apollo: %d leads encontrados", len(leads))
        return leads


# ---------------------------------------------------------------------------
# Email: SMTP generico (Gmail, SES, etc) ou Resend
# ---------------------------------------------------------------------------


class EmailSMTP:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "")
        self.porta = int(os.getenv("SMTP_PORT", "587"))
        self.usuario = os.getenv("SMTP_USER", "")
        self.senha = os.getenv("SMTP_PASSWORD", "")
        self.remetente = os.getenv("PROS_REMETENTE_EMAIL", self.usuario)
        if not (self.host and self.usuario and self.senha):
            raise ErroProvider("SMTP_HOST/SMTP_USER/SMTP_PASSWORD ausentes")

    def enviar(self, lead: Lead, assunto: str, corpo: str) -> None:
        if not lead.email:
            raise ErroProvider(f"lead {lead.id} sem email")
        msg = MIMEText(corpo, "plain", "utf-8")
        msg["Subject"] = assunto
        msg["From"] = self.remetente
        msg["To"] = lead.email
        try:
            with smtplib.SMTP(self.host, self.porta, timeout=20) as s:
                s.starttls()
                s.login(self.usuario, self.senha)
                s.send_message(msg)
        except smtplib.SMTPException as e:
            raise ErroProvider(f"SMTP falhou: {e}") from e

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        # IMAP fica fora do MVP: a deteccao de resposta por email real requer
        # ler a caixa de entrada (IMAP) e casar pelo header In-Reply-To/thread
        # id, o que precisa de mais configuracao (pasta, filtro de spam etc).
        # Por ora, resposta de email entra por `prospectar marcar-resposta`.
        return set()


class EmailResend:
    """https://resend.com/docs/api-reference/emails/send-email"""

    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY", "")
        self.remetente = os.getenv("PROS_REMETENTE_EMAIL", "")
        if not (self.api_key and self.remetente):
            raise ErroProvider("RESEND_API_KEY ou PROS_REMETENTE_EMAIL ausente")

    def enviar(self, lead: Lead, assunto: str, corpo: str) -> None:
        if not lead.email:
            raise ErroProvider(f"lead {lead.id} sem email")
        try:
            resp = httpx.post(
                "https://api.resend.com/emails",
                json={"from": self.remetente, "to": [lead.email], "subject": assunto, "text": corpo},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=20,
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ErroProvider(f"Resend falhou: {e}") from e

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        # Resposta chega por webhook (inbound email) — fora do MVP; ver
        # `prospectar marcar-resposta` como caminho manual por enquanto.
        return set()


# ---------------------------------------------------------------------------
# Calendario: Google Calendar
# ---------------------------------------------------------------------------


class CalendarioGoogle:
    """Usa o mesmo padrao de OAuth de src/maquina/stages/youtube.py (token em
    secrets/), mas com o escopo do Calendar."""

    def __init__(self, token_path: str = "", client_secret_path: str = ""):
        from pathlib import Path

        self.token_path = Path(token_path or os.getenv("PROS_GOOGLE_TOKEN", "secrets/prospeccao_calendar_token.json"))
        self.client_secret_path = Path(
            client_secret_path or os.getenv("PROS_GOOGLE_CLIENT_SECRET", "secrets/client_secret.json")
        )
        if not self.token_path.exists():
            raise ErroProvider(
                f"token do Google Calendar nao encontrado em {self.token_path} "
                "— rode `prospectar auth-google`"
            )
        self._service = self._construir_service()

    def _construir_service(self):
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(self.token_path))
        return build("calendar", "v3", credentials=creds)

    def horarios_livres(
        self, disponibilidade: list[Disponibilidade], dias_a_frente: int = 14
    ) -> list[tuple[datetime, datetime]]:
        from .stubs import CalendarioStub

        candidatos = CalendarioStub().horarios_livres(disponibilidade, dias_a_frente)
        if not candidatos:
            return []
        inicio = candidatos[0][0]
        fim = candidatos[-1][1]
        try:
            resp = (
                self._service.freebusy()
                .query(
                    body={
                        "timeMin": inicio.isoformat(),
                        "timeMax": fim.isoformat(),
                        "items": [{"id": "primary"}],
                    }
                )
                .execute()
            )
        except Exception as e:  # noqa: BLE001 - API do google levanta varios tipos
            raise ErroProvider(f"Google Calendar freebusy falhou: {e}") from e

        ocupados = resp["calendars"]["primary"]["busy"]
        ocupados_iv = [
            (datetime.fromisoformat(b["start"]), datetime.fromisoformat(b["end"])) for b in ocupados
        ]

        def livre(slot_ini: datetime, slot_fim: datetime) -> bool:
            return not any(slot_ini < b_fim and slot_fim > b_ini for b_ini, b_fim in ocupados_iv)

        return [s for s in candidatos if livre(*s)]

    def criar_evento(self, lead: Lead, inicio: datetime, fim: datetime) -> tuple[str, str]:
        corpo = {
            "summary": f"Reuniao de vendas — {lead.nome} ({lead.empresa})",
            "description": f"Lead: {lead.nome}\nCargo: {lead.cargo}\nOrigem: {lead.origem}",
            "start": {"dateTime": inicio.isoformat()},
            "end": {"dateTime": fim.isoformat()},
            "attendees": [{"email": lead.email}] if lead.email else [],
            "conferenceData": {
                "createRequest": {"requestId": f"pros-{lead.id}-{int(inicio.timestamp())}"}
            },
        }
        try:
            evento = (
                self._service.events()
                .insert(calendarId="primary", body=corpo, conferenceDataVersion=1, sendUpdates="all")
                .execute()
            )
        except Exception as e:  # noqa: BLE001
            raise ErroProvider(f"Google Calendar insert falhou: {e}") from e

        meet_url = ""
        for ep in evento.get("conferenceData", {}).get("entryPoints", []):
            if ep.get("entryPointType") == "video":
                meet_url = ep.get("uri", "")
        return evento["id"], meet_url
