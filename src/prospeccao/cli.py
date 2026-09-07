"""CLI da maquina de prospeccao."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config import Config
from .models import StatusLead
from .pipeline import Pipeline
from .storage import Store

app = typer.Typer(add_completion=False, help="Maquina de prospeccao e agendamento de reunioes")
console = Console()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
)


def _cfg() -> Config:
    return Config.load()


@app.command()
def doctor():
    """Mostra ICP, limites e quais providers estao ativos vs. em stub."""
    cfg = _cfg()
    console.print(f"[bold]ICP[/bold]: {', '.join(cfg.icp.cargos) or '(sem cargo definido)'} "
                  f"em {', '.join(cfg.icp.setores) or '(sem setor)'} — {cfg.icp.localizacao or 'qualquer local'}")

    tabela = Table("credencial", "presente?")
    for nome, chave in [
        ("APOLLO_API_KEY (leads)", "APOLLO_API_KEY"),
        ("RESEND_API_KEY (email)", "RESEND_API_KEY"),
        ("SMTP_HOST (email)", "SMTP_HOST"),
        ("PROS_LINKEDIN_RISCO_ACEITO", "PROS_LINKEDIN_RISCO_ACEITO"),
        ("PROS_GOOGLE_TOKEN (calendario)", "PROS_GOOGLE_TOKEN"),
    ]:
        tabela.add_row(nome, "sim" if os.getenv(chave) else "nao — cai no stub")
    console.print(tabela)

    console.print(
        f"[bold]Limites/dia[/bold]: LinkedIn {cfg.limites.linkedin_convites_dia} convites / "
        f"{cfg.limites.linkedin_mensagens_dia} mensagens · Email {cfg.limites.email_envios_dia} · "
        f"Leads novos {cfg.limites.leads_novos_dia}"
    )


@app.command("buscar-leads")
def buscar_leads(n: int = typer.Option(10, help="quantos leads buscar")):
    """Busca leads novos que batem no ICP, sem disparar a sequencia."""
    p = Pipeline(_cfg())
    icp = p.cfg.icp
    encontrados = p.leads.buscar(icp, n)
    tabela = Table("Nome", "Cargo", "Empresa", "LinkedIn")
    for lead in encontrados:
        tabela.add_row(lead.nome, lead.cargo, lead.empresa, lead.linkedin_url)
    console.print(tabela)


@app.command()
def rodar():
    """Um ciclo completo: busca leads, avanca a cadencia, detecta resposta e
    manda o link de agendamento. Pensado para rodar 1x/dia (cron/Actions)."""
    p = Pipeline(_cfg())
    resultado = p.ciclo()
    console.print(
        f"[bold green]ciclo concluido[/bold green]: {resultado['leads_novos']} leads novos, "
        f"{resultado['mensagens_enviadas']} mensagens enviadas, {resultado['respostas']} respostas"
    )


@app.command()
def status():
    """Funil: quantos leads em cada estagio."""
    cfg = _cfg()
    store = Store(cfg.data_dir / "prospeccao.db")
    funil = store.funil()
    tabela = Table("Status", "Total")
    for s in StatusLead:
        tabela.add_row(s.value, str(funil.get(s.value, 0)))
    console.print(tabela)


@app.command("marcar-resposta")
def marcar_resposta(lead_id: str):
    """Marca manualmente um lead como 'respondeu' (caminho manual enquanto
    deteccao automatica de resposta por email/LinkedIn nao esta configurada)."""
    cfg = _cfg()
    store = Store(cfg.data_dir / "prospeccao.db")
    lead = store.lead(lead_id)
    if lead is None:
        console.print(f"[red]lead {lead_id} nao encontrado[/red]")
        raise typer.Exit(1)
    lead.status = StatusLead.RESPONDEU
    store.salvar_lead(lead)
    p = Pipeline(cfg, store)
    p.enviar_agenda(lead)
    console.print(f"[green]lead {lead.nome} marcado como respondeu e agenda enviada[/green]")


@app.command("agenda-web")
def agenda_web(porta: int = 8000):
    """Sobe a pagina publica de agendamento (uvicorn) em modo dev."""
    import uvicorn

    uvicorn.run("prospeccao.web:app", host="0.0.0.0", port=porta, reload=True)


@app.command("linkedin-login")
def linkedin_login():
    """Abre um navegador para voce logar no LinkedIn manualmente e salva a
    sessao (cookie) para a automacao usar depois. Nao guarda usuario/senha."""
    from .providers.linkedin_playwright import login_persistir_sessao

    destino = login_persistir_sessao()
    console.print(f"[green]sessao salva em {destino}[/green]")


@app.command("auth-google")
def auth_google(
    client_secret: Path = typer.Option(Path("secrets/client_secret.json")),
    token_saida: Path = typer.Option(Path("secrets/prospeccao_calendar_token.json")),
):
    """Autoriza o acesso ao Google Calendar (escopo calendar.events) uma vez;
    o token fica salvo para os proximos runs."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not client_secret.exists():
        console.print(f"[red]{client_secret} nao existe — baixe do Google Cloud Console[/red]")
        raise typer.Exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(
        str(client_secret), scopes=["https://www.googleapis.com/auth/calendar"]
    )
    creds = flow.run_local_server(port=0)
    token_saida.parent.mkdir(parents=True, exist_ok=True)
    token_saida.write_text(creds.to_json(), encoding="utf-8")
    console.print(f"[green]token salvo em {token_saida}[/green]")


if __name__ == "__main__":
    app()
