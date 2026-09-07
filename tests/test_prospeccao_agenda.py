from __future__ import annotations

from pathlib import Path

from prospeccao import agenda
from prospeccao.config import Config
from prospeccao.models import StatusLead
from prospeccao.providers.stubs import BuscadorLeadsStub
from prospeccao.storage import Store


def _cfg(tmp_path: Path) -> Config:
    return Config(
        leads_provider="stub",
        email_provider="stub",
        linkedin_provider="stub",
        calendario_provider="stub",
        data_dir=tmp_path,
    )


def test_horarios_disponiveis_respeita_disponibilidade(tmp_path):
    cfg = _cfg(tmp_path)
    slots = agenda.horarios_disponiveis(cfg, dias_a_frente=7)
    assert slots
    for inicio, fim in slots:
        assert inicio.weekday() < 5  # so dias uteis, por padrao
        assert (fim - inicio).total_seconds() == 30 * 60


def test_confirmar_marca_reuniao_e_atualiza_lead(tmp_path):
    cfg = _cfg(tmp_path)
    store = Store(tmp_path / "db.sqlite")
    [lead] = BuscadorLeadsStub().buscar(cfg.icp, 1)
    store.salvar_lead(lead)

    inicio, fim = agenda.horarios_disponiveis(cfg)[0]
    reuniao = agenda.confirmar(cfg, store, lead.id, inicio, fim)

    assert reuniao.calendar_event_id
    atualizado = store.lead(lead.id)
    assert atualizado.status == StatusLead.REUNIAO_MARCADA
