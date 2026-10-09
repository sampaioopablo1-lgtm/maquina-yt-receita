"""Pagina publica de agendamento — o equivalente ao link do Calendly que a
maquina manda para o lead depois que ele responde. Rodar local:

    uvicorn prospeccao.web:app --reload

Em producao, aponte PROS_BOOKING_BASE_URL para onde isto estiver hospedado.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

from . import agenda
from .config import Config
from .storage import Store

app = FastAPI(title="Agenda de reunioes")


def _cfg_store() -> tuple[Config, Store]:
    cfg = Config.load()
    return cfg, Store(cfg.data_dir / "prospeccao.db")


def _pagina(corpo: str) -> str:
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agendar reuniao</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 560px; margin: 40px auto; padding: 0 16px; color: #1a1a1a; }}
  h1 {{ font-size: 1.4rem; }}
  .slot {{ display: block; width: 100%; text-align: left; padding: 12px 16px; margin: 6px 0;
           border: 1px solid #ddd; border-radius: 8px; background: #fafafa; cursor: pointer; font-size: 1rem; }}
  .slot:hover {{ background: #f0f0f0; }}
  .ok {{ color: #147a3d; }}
</style></head>
<body>{corpo}</body></html>"""


@app.get("/agenda/{lead_id}", response_class=HTMLResponse)
def pagina_agenda(lead_id: str):
    cfg, store = _cfg_store()
    lead = store.lead(lead_id)
    if lead is None:
        raise HTTPException(404, "lead nao encontrado")

    slots = agenda.horarios_disponiveis(cfg)[:20]
    nome = lead.nome.split(" (")[0]
    itens = "\n".join(
        f'<form method="post" action="/agenda/{lead_id}/confirmar" class="slot" style="padding:0;">'
        f'<button type="submit" name="inicio" value="{ini.isoformat()}" '
        f'style="all:unset;display:block;width:100%;padding:12px 16px;cursor:pointer;">'
        f"{ini.strftime('%d/%m %H:%M')}</button></form>"
        for ini, _fim in slots
    )
    corpo = f"""
    <h1>Oi, {nome} — escolha um horario</h1>
    <p>Reuniao de 30 min. Fuso: horario de Brasilia.</p>
    {itens or '<p>Sem horarios livres nos proximos dias — responda o email/LinkedIn.</p>'}
    """
    return _pagina(corpo)


@app.post("/agenda/{lead_id}/confirmar", response_class=HTMLResponse)
def confirmar(lead_id: str, inicio: str = Form(...)):
    cfg, store = _cfg_store()
    lead = store.lead(lead_id)
    if lead is None:
        raise HTTPException(404, "lead nao encontrado")

    dt_inicio = datetime.fromisoformat(inicio)
    duracao_min = cfg.disponibilidade[0].duracao_min if cfg.disponibilidade else 30
    from datetime import timedelta

    dt_fim = dt_inicio + timedelta(minutes=duracao_min)

    reuniao = agenda.confirmar(cfg, store, lead_id, dt_inicio, dt_fim)
    nome = lead.nome.split(" (")[0]
    meet = f'<p><a href="{reuniao.meet_url}">{reuniao.meet_url}</a></p>' if reuniao.meet_url else ""
    corpo = f"""
    <h1 class="ok">Reuniao marcada!</h1>
    <p>{nome}, confirmado para {dt_inicio.strftime('%d/%m as %H:%M')}.</p>
    {meet}
    """
    return _pagina(corpo)
