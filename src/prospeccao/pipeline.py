"""Orquestrador: busca leads, avanca a cadencia, detecta resposta e manda o
link de agendamento. `ciclo()` e o que `prospectar rodar` chama — pensado para
rodar 1x/dia via cron/Actions, no mesmo espirito de src/maquina/pipeline.py."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from .config import Config
from .models import Canal, Lead, Mensagem, StatusLead
from .providers import fabrica
from .sequencias import extrair_assunto, renderizar
from .storage import Store

log = logging.getLogger("prospeccao.pipeline")


class Pipeline:
    def __init__(self, cfg: Config | None = None, store: Store | None = None):
        self.cfg = cfg or Config.load()
        self.store = store or Store(self.cfg.data_dir / "prospeccao.db")
        self.leads = fabrica.buscador_leads(self.cfg)
        self.email = fabrica.enviador_email(self.cfg)
        self.linkedin = fabrica.automacao_linkedin(self.cfg)
        self.calendario = fabrica.calendario(self.cfg)

    # ---- limites diarios ----

    def _hoje(self) -> str:
        return date.today().isoformat()

    def _pode(self, canal: str, tipo: str, teto: int) -> bool:
        return self.store.contagem_hoje(self._hoje(), canal, tipo) < teto

    def _registrar(self, canal: str, tipo: str) -> None:
        self.store.incrementar_contagem(self._hoje(), canal, tipo)

    # ---- etapas do ciclo ----

    def buscar_novos_leads(self) -> list[Lead]:
        ja_hoje = self.store.contagem_hoje(self._hoje(), "geral", "lead_novo")
        restante = max(0, self.cfg.limites.leads_novos_dia - ja_hoje)
        if restante == 0:
            log.info("teto diario de leads novos atingido")
            return []
        encontrados = self.leads.buscar(self.cfg.icp, restante)
        novos = []
        for lead in encontrados:
            if self.store.existe(lead.id):
                continue
            lead.proxima_acao_em = datetime.now(timezone.utc)
            self.store.salvar_lead(lead)
            self._registrar("geral", "lead_novo")
            novos.append(lead)
        log.info("buscar_novos_leads: %d leads novos", len(novos))
        return novos

    def _enviar_etapa(self, lead: Lead, texto: str, canal: Canal) -> bool:
        """Retorna False se o teto diario do canal foi atingido (reagenda p/ amanha)."""
        if canal is Canal.LINKEDIN:
            tipo = "convite" if lead.etapa_sequencia == 0 else "mensagem"
            teto = (
                self.cfg.limites.linkedin_convites_dia
                if tipo == "convite"
                else self.cfg.limites.linkedin_mensagens_dia
            )
            if not self._pode("linkedin", tipo, teto):
                return False
            if tipo == "convite":
                self.linkedin.conectar(lead, texto)
            else:
                self.linkedin.mensagem(lead, texto)
            self._registrar("linkedin", tipo)
        else:
            if not self._pode("email", "envio", self.cfg.limites.email_envios_dia):
                return False
            assunto, corpo = extrair_assunto(texto)
            self.email.enviar(lead, assunto, corpo)
            self._registrar("email", "envio")
        return True

    def executar_etapas_pendentes(self) -> int:
        pendentes = self.store.leads_com_acao_pendente(datetime.now(timezone.utc))
        enviados = 0
        for lead in pendentes:
            proxima_ordem = lead.etapa_sequencia + 1
            etapa = next((e for e in self.cfg.sequencia if e.ordem == proxima_ordem), None)
            if etapa is None:
                lead.status = StatusLead.ESGOTADO
                lead.proxima_acao_em = None
                self.store.salvar_lead(lead)
                continue

            texto = renderizar(etapa.template, nome=lead.nome, cargo=lead.cargo, empresa=lead.empresa)
            if not self._enviar_etapa(lead, texto, etapa.canal):
                lead.proxima_acao_em = datetime.now(timezone.utc) + timedelta(days=1)
                self.store.salvar_lead(lead)
                continue

            self.store.salvar_mensagem(
                Mensagem(lead_id=lead.id, canal=etapa.canal, etapa=etapa.ordem, texto=texto)
            )
            lead.etapa_sequencia = proxima_ordem
            lead.status = StatusLead.EM_SEQUENCIA
            proxima_etapa = next(
                (e for e in self.cfg.sequencia if e.ordem == proxima_ordem + 1), None
            )
            lead.proxima_acao_em = (
                lead.criado_em + timedelta(days=proxima_etapa.dia_offset)
                if proxima_etapa
                else None
            )
            if proxima_etapa is None:
                lead.status = StatusLead.ESGOTADO
            lead.atualizado_em = datetime.now(timezone.utc)
            self.store.salvar_lead(lead)
            enviados += 1
        log.info("executar_etapas_pendentes: %d mensagens enviadas", enviados)
        return enviados

    def checar_respostas(self) -> list[Lead]:
        ativos = self.store.leads_por_status(StatusLead.EM_SEQUENCIA) + self.store.leads_por_status(
            StatusLead.NOVO
        )
        if not ativos:
            return []
        respondidos_ids = self.email.checar_respostas(ativos) | self.linkedin.checar_respostas(ativos)
        respondidos = []
        for lead in ativos:
            if lead.id in respondidos_ids:
                lead.status = StatusLead.RESPONDEU
                lead.proxima_acao_em = None
                lead.atualizado_em = datetime.now(timezone.utc)
                self.store.salvar_lead(lead)
                respondidos.append(lead)
        log.info("checar_respostas: %d leads responderam", len(respondidos))
        return respondidos

    def enviar_agenda(self, lead: Lead) -> None:
        link = f"{self.cfg.calendly_like_base_url}/agenda/{lead.id}"
        texto = (
            f"Que bom, {lead.nome.split(' (')[0]}! Escolhe um horario que funcione pra "
            f"voce aqui: {link}"
        )
        canal = Canal.EMAIL if lead.email else Canal.LINKEDIN
        if canal is Canal.EMAIL:
            self.email.enviar(lead, "Bora marcar?", texto)
        else:
            self.linkedin.mensagem(lead, texto)
        lead.status = StatusLead.AGENDA_ENVIADA
        lead.atualizado_em = datetime.now(timezone.utc)
        self.store.salvar_lead(lead)
        self.store.salvar_mensagem(Mensagem(lead_id=lead.id, canal=canal, etapa=999, texto=texto))

    def ciclo(self) -> dict[str, int]:
        """Um ciclo completo: busca leads -> avanca sequencia -> detecta
        resposta -> manda link de agenda para quem respondeu."""
        novos = self.buscar_novos_leads()
        enviados = self.executar_etapas_pendentes()
        respondidos = self.checar_respostas()
        for lead in respondidos:
            self.enviar_agenda(lead)
        return {
            "leads_novos": len(novos),
            "mensagens_enviadas": enviados,
            "respostas": len(respondidos),
        }
