"""Renderizacao de templates da cadencia de outreach."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_PATH = ROOT / "config" / "prospeccao_templates.yaml"

# Preenchidos pela config do operador (config/prospeccao.yaml ou env) — ficam
# aqui como default para o modo stub/demo funcionar sem configuracao nenhuma.
PROPOSTA_VALOR_PADRAO = "ajudar seu time comercial a agendar mais reunioes qualificadas"
PROPOSTA_VALOR_CURTA_PADRAO = "mais reunioes qualificadas"


def _carregar_templates() -> dict[str, str]:
    if not TEMPLATES_PATH.exists():
        return {}
    return yaml.safe_load(TEMPLATES_PATH.read_text(encoding="utf-8")) or {}


def renderizar(
    nome_template: str,
    *,
    nome: str,
    cargo: str,
    empresa: str,
    link_agenda: str = "",
    proposta_valor: str = PROPOSTA_VALOR_PADRAO,
    proposta_valor_curta: str = PROPOSTA_VALOR_CURTA_PADRAO,
) -> str:
    templates = _carregar_templates()
    bruto = templates.get(nome_template, "")
    if not bruto:
        raise KeyError(f"template '{nome_template}' nao existe em {TEMPLATES_PATH}")
    nome_curto = nome.split(" (")[0].split(" ")[0]
    return bruto.format(
        nome_curto=nome_curto,
        cargo=cargo or "responsavel comercial",
        empresa=empresa or "sua empresa",
        link_agenda=link_agenda,
        proposta_valor=proposta_valor,
        proposta_valor_curta=proposta_valor_curta,
    ).strip()


def extrair_assunto(texto_renderizado: str) -> tuple[str, str]:
    """Templates de email podem comecar com 'Assunto: ...\\n\\n'. Separa
    assunto do corpo; se nao houver, usa um assunto generico."""
    linhas = texto_renderizado.split("\n", 1)
    if linhas[0].lower().startswith("assunto:"):
        assunto = linhas[0].split(":", 1)[1].strip()
        corpo = linhas[1].strip() if len(linhas) > 1 else ""
        return assunto, corpo
    return "Vamos conversar?", texto_renderizado
