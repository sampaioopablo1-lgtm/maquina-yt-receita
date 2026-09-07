"""Stubs deterministicos: rodam offline, sem credencial, sem tocar em conta
real. Mesma filosofia de src/maquina/providers/stubs.py — a pipeline inteira
tem que executar de ponta a ponta sem chave nenhuma, para dar para testar e
para o CI ficar verde."""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timedelta, timezone

from ..models import ICP, Disponibilidade, Lead

log = logging.getLogger("prospeccao.providers.stub")

_NOMES = [
    "Ana Ribeiro", "Bruno Alves", "Carla Nunes", "Diego Souza", "Elisa Prado",
    "Fabio Lima", "Giovana Melo", "Heitor Braga", "Isabela Rocha", "Joao Vidal",
]
_EMPRESAS = [
    "Nimbus Tech", "Vetor SaaS", "Orbita Digital", "Cadence Software",
    "Prisma Cloud", "Astra Sistemas", "Lumen Growth", "Zenith Data",
]


class BuscadorLeadsStub:
    """Gera leads sinteticos deterministicos a partir do ICP, so para exercitar
    o funil inteiro (busca -> sequencia -> agenda) sem depender de Apollo."""

    def buscar(self, icp: ICP, limite: int) -> list[Lead]:
        cargo = (icp.cargos or ["Diretor Comercial"])[0]
        leads = []
        for i in range(limite):
            nome = _NOMES[i % len(_NOMES)]
            empresa = _EMPRESAS[i % len(_EMPRESAS)]
            slug = hashlib.sha1(f"{nome}{empresa}{i}".encode()).hexdigest()[:8]
            leads.append(
                Lead(
                    nome=f"{nome} ({slug})",
                    cargo=cargo,
                    empresa=empresa,
                    setor=(icp.setores or ["Tecnologia"])[0],
                    localizacao=icp.localizacao or "Sao Paulo, BR",
                    linkedin_url=f"https://www.linkedin.com/in/stub-{slug}",
                    email=f"{slug}@{empresa.lower().replace(' ', '')}.com",
                    origem="stub",
                )
            )
        log.info("BuscadorLeadsStub: %d leads sinteticos gerados (sem credencial Apollo)", len(leads))
        return leads


class EmailStub:
    def enviar(self, lead: Lead, assunto: str, corpo: str) -> None:
        log.info("EmailStub -> %s <%s>: %s", lead.nome, lead.email, assunto)

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        # Determinístico: ~1 em cada 5 leads "responde" depois da 2a etapa,
        # so para o funil de demonstracao ter reuniao marcada no fim.
        respondidos = set()
        for lead in leads:
            if lead.etapa_sequencia >= 2 and int(lead.id, 16) % 5 == 0:
                respondidos.add(lead.id)
        return respondidos


class LinkedInStub:
    def conectar(self, lead: Lead, nota: str) -> None:
        log.info("LinkedInStub: convite para %s — %r", lead.nome, nota[:60])

    def mensagem(self, lead: Lead, texto: str) -> None:
        log.info("LinkedInStub: mensagem para %s — %r", lead.nome, texto[:60])

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        return set()


class CalendarioStub:
    """Gera horarios livres a partir da disponibilidade configurada, sem
    checar um calendario real — util para testar a pagina de agendamento."""

    def horarios_livres(
        self, disponibilidade: list[Disponibilidade], dias_a_frente: int = 14
    ) -> list[tuple[datetime, datetime]]:
        if not disponibilidade:
            disponibilidade = [
                Disponibilidade(dia_semana=d, hora_inicio="09:00", hora_fim="18:00")
                for d in range(5)
            ]
        slots: list[tuple[datetime, datetime]] = []
        hoje = datetime.now(timezone.utc).date()
        for i in range(1, dias_a_frente + 1):
            dia = hoje + timedelta(days=i)
            for disp in disponibilidade:
                if dia.weekday() != disp.dia_semana:
                    continue
                h_ini = datetime.strptime(disp.hora_inicio, "%H:%M").time()
                h_fim = datetime.strptime(disp.hora_fim, "%H:%M").time()
                cursor = datetime.combine(dia, h_ini, tzinfo=timezone.utc)
                fim_janela = datetime.combine(dia, h_fim, tzinfo=timezone.utc)
                passo = timedelta(minutes=disp.duracao_min)
                while cursor + passo <= fim_janela:
                    slots.append((cursor, cursor + passo))
                    cursor += passo
        return slots

    def criar_evento(self, lead: Lead, inicio: datetime, fim: datetime) -> tuple[str, str]:
        fake_id = hashlib.sha1(f"{lead.id}{inicio.isoformat()}".encode()).hexdigest()[:12]
        log.info("CalendarioStub: evento %s criado para %s em %s", fake_id, lead.nome, inicio)
        return fake_id, f"https://meet.stub.local/{fake_id}"
