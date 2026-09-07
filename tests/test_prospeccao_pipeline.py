"""Fim-a-fim em modo 100% stub: sem rede, sem credencial, sem tocar em conta
real de LinkedIn/email. Cobre o mesmo caminho que `prospectar rodar` chama."""

from __future__ import annotations

from pathlib import Path

from prospeccao.config import Config
from prospeccao.models import StatusLead
from prospeccao.pipeline import Pipeline
from prospeccao.storage import Store


def _cfg(tmp_path: Path) -> Config:
    return Config(
        leads_provider="stub",
        email_provider="stub",
        linkedin_provider="stub",
        calendario_provider="stub",
        data_dir=tmp_path,
    )


def test_buscar_novos_leads_respeita_teto(tmp_path):
    cfg = _cfg(tmp_path)
    cfg.limites.leads_novos_dia = 3
    p = Pipeline(cfg, Store(tmp_path / "db.sqlite"))

    novos = p.buscar_novos_leads()
    assert len(novos) == 3
    assert p.store.funil() == {"novo": 3}

    # teto ja bateu hoje — segunda chamada nao acrescenta
    mais = p.buscar_novos_leads()
    assert mais == []


def test_ciclo_avanca_ate_reuniao_marcada(tmp_path):
    cfg = _cfg(tmp_path)
    cfg.limites.leads_novos_dia = 10
    store = Store(tmp_path / "db.sqlite")
    p = Pipeline(cfg, store)

    # roda alguns ciclos "simulando dias" — cada ciclo dispara etapas cuja
    # proxima_acao_em ja passou, entao adiantamos o relogio do lead na mao.
    p.buscar_novos_leads()
    resultado = p.ciclo()
    assert resultado["mensagens_enviadas"] >= 1

    # forca todos os leads a estarem prontos para a proxima etapa AGORA,
    # para nao depender de esperar dias de verdade no teste.
    from datetime import datetime, timezone

    for lead in store.leads_por_status(StatusLead.EM_SEQUENCIA):
        lead.proxima_acao_em = datetime.now(timezone.utc)
        store.salvar_lead(lead)

    for _ in range(5):
        p.ciclo()
        for lead in store.leads_por_status(StatusLead.EM_SEQUENCIA):
            lead.proxima_acao_em = datetime.now(timezone.utc)
            store.salvar_lead(lead)

    funil = store.funil()
    assert funil.get(StatusLead.AGENDA_ENVIADA.value, 0) >= 1


def test_marcar_resposta_manual_dispara_agenda(tmp_path):
    cfg = _cfg(tmp_path)
    store = Store(tmp_path / "db.sqlite")
    p = Pipeline(cfg, store)

    [lead] = p.buscar_novos_leads()[:1] or p.leads.buscar(cfg.icp, 1)
    if not store.existe(lead.id):
        store.salvar_lead(lead)

    lead.status = StatusLead.RESPONDEU
    store.salvar_lead(lead)
    p.enviar_agenda(lead)

    atualizado = store.lead(lead.id)
    assert atualizado.status == StatusLead.AGENDA_ENVIADA
