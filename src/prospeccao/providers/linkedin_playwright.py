"""Automacao de LinkedIn via Playwright.

AVISO DE RISCO — leia antes de ligar isto em producao
=======================================================
Automatizar acoes no LinkedIn (convites, mensagens, scraping de perfil) viola
os Termos de Uso da plataforma (clausula de "no automated means"). O LinkedIn
detecta e pune isso com restricao de conta ("weekly invitation limit
reached"), suspensao temporaria ou banimento definitivo — mesmo com limites
conservadores, o risco nunca vai a zero porque a deteccao e do lado deles, nao
do nosso.

Este modulo so roda de verdade se a variavel de ambiente
`PROS_LINKEDIN_RISCO_ACEITO=true` estiver setada — e uma decisao explicita,
nao um padrao. Sem ela, `fabrica.linkedin_provider()` cai automaticamente
para `LinkedInStub`. Mitigacoes aplicadas mesmo com o risco aceito:

- Login por sessao persistida (cookie do navegador), nunca usuario/senha em
  texto — evita acionar o desafio de seguranca a cada execucao.
- Teto diario BAIXO por padrao (ver Config.limites) e follow-up automatico
  suspenso se o LinkedIn mostrar qualquer aviso de limite.
- Atraso aleatorio entre acoes (nunca menos de alguns segundos) para nao
  parecer um robo em rajada.
- Um unico convite/mensagem por chamada — o chamador (pipeline.py) e quem
  decide QUANTAS chamadas fazer por dia, respeitando o teto.

Recomendacao pratica: comece com o teto bem abaixo do limite semanal real do
LinkedIn (~100-200 convites/semana para conta normal) e suba devagar
observando se a conta recebe algum aviso.
"""

from __future__ import annotations

import logging
import os
import random
import time
from pathlib import Path

from ..models import Lead
from .base import ErroProvider

log = logging.getLogger("prospeccao.providers.linkedin")

ROOT = Path(__file__).resolve().parents[3]
SESSAO_PADRAO = ROOT / "secrets" / "linkedin_state.json"


def _pausa_humana(min_s: float = 3.0, max_s: float = 9.0) -> None:
    time.sleep(random.uniform(min_s, max_s))


def login_persistir_sessao(destino: Path = SESSAO_PADRAO) -> Path:
    """Abre um navegador visivel para voce logar manualmente (usuario/senha e
    2FA, se houver) e salva a sessao — assim a automacao nunca ve sua senha.
    Rode uma vez via `prospectar linkedin-login`."""
    from playwright.sync_api import sync_playwright

    destino.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        contexto = browser.new_context()
        page = contexto.new_page()
        page.goto("https://www.linkedin.com/login")
        log.info("Faca login manualmente na janela aberta. Fechando em ate 5 minutos apos o feed carregar.")
        page.wait_for_url("**/feed/**", timeout=5 * 60 * 1000)
        contexto.storage_state(path=str(destino))
        browser.close()
    log.info("Sessao salva em %s", destino)
    return destino


class AutomacaoLinkedInPlaywright:
    def __init__(self, sessao_path: Path = SESSAO_PADRAO):
        if os.getenv("PROS_LINKEDIN_RISCO_ACEITO", "").lower() != "true":
            raise ErroProvider(
                "PROS_LINKEDIN_RISCO_ACEITO nao esta 'true' — automacao de LinkedIn "
                "viola os Termos de Uso da plataforma e pode banir a conta. "
                "Defina a variavel explicitamente para ligar isto (ver docstring do modulo)."
            )
        if not sessao_path.exists():
            raise ErroProvider(
                f"sessao do LinkedIn nao encontrada em {sessao_path} — rode `prospectar linkedin-login`"
            )
        self.sessao_path = sessao_path

    def _contexto(self):
        from playwright.sync_api import sync_playwright

        p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)
        contexto = browser.new_context(storage_state=str(self.sessao_path))
        return p, browser, contexto

    def conectar(self, lead: Lead, nota: str) -> None:
        if not lead.linkedin_url:
            raise ErroProvider(f"lead {lead.id} sem linkedin_url")
        p, browser, contexto = self._contexto()
        try:
            page = contexto.new_page()
            page.goto(lead.linkedin_url, wait_until="domcontentloaded")
            _pausa_humana()
            botao_conectar = page.get_by_role("button", name="Conectar").or_(
                page.get_by_role("button", name="Connect")
            )
            if botao_conectar.count() == 0:
                raise ErroProvider(f"botao Conectar nao encontrado no perfil de {lead.nome} (ja conectado?)")
            botao_conectar.first.click()
            _pausa_humana(1, 3)
            botao_nota = page.get_by_role("button", name="Adicionar nota").or_(
                page.get_by_role("button", name="Add a note")
            )
            if nota and botao_nota.count() > 0:
                botao_nota.first.click()
                page.get_by_role("textbox").first.fill(nota[:300])
            page.get_by_role("button", name="Enviar").or_(page.get_by_role("button", name="Send")).first.click()
            log.info("LinkedIn: convite enviado para %s", lead.nome)
        except ErroProvider:
            raise
        except Exception as e:  # noqa: BLE001 - UI do LinkedIn muda sem aviso
            raise ErroProvider(f"falha ao conectar com {lead.nome}: {e}") from e
        finally:
            browser.close()
            p.stop()

    def mensagem(self, lead: Lead, texto: str) -> None:
        if not lead.linkedin_url:
            raise ErroProvider(f"lead {lead.id} sem linkedin_url")
        p, browser, contexto = self._contexto()
        try:
            page = contexto.new_page()
            page.goto(lead.linkedin_url, wait_until="domcontentloaded")
            _pausa_humana()
            botao_msg = page.get_by_role("button", name="Mensagem").or_(page.get_by_role("button", name="Message"))
            if botao_msg.count() == 0:
                raise ErroProvider(f"botao Mensagem nao encontrado no perfil de {lead.nome} (ainda nao conectado?)")
            botao_msg.first.click()
            _pausa_humana(1, 3)
            caixa = page.get_by_role("textbox").last
            caixa.fill(texto)
            page.keyboard.press("Enter")
            log.info("LinkedIn: mensagem enviada para %s", lead.nome)
        except ErroProvider:
            raise
        except Exception as e:  # noqa: BLE001
            raise ErroProvider(f"falha ao mandar mensagem para {lead.nome}: {e}") from e
        finally:
            browser.close()
            p.stop()

    def checar_respostas(self, leads: list[Lead]) -> set[str]:
        # Best-effort: abre a caixa de mensagens e casa por nome. A UI de
        # mensagens do LinkedIn muda com frequencia — se o seletor quebrar,
        # isto so retorna vazio (log de aviso), nunca derruba o pipeline.
        respondidos: set[str] = set()
        try:
            p, browser, contexto = self._contexto()
            page = contexto.new_page()
            page.goto("https://www.linkedin.com/messaging/", wait_until="domcontentloaded")
            _pausa_humana(2, 4)
            nomes_por_lead = {lead.nome.split(" (")[0]: lead.id for lead in leads}
            for item in page.locator("li.msg-conversation-listitem").all():
                texto = item.inner_text()
                for nome, lead_id in nomes_por_lead.items():
                    if nome in texto and "unread" in (item.get_attribute("class") or "").lower():
                        respondidos.add(lead_id)
            browser.close()
            p.stop()
        except Exception as e:  # noqa: BLE001
            log.warning("checar_respostas do LinkedIn falhou (seletor pode ter mudado): %s", e)
        return respondidos
