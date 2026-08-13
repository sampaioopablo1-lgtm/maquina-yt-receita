"""Guardas que passam a valer quando o repositorio e publico.

O repo virou publico em 13/08/2026 por um motivo economico: GitHub Actions nao
tem cota de minutos em repositorio publico, e a meta de dez longos por canal
(130 videos, ~17 min de runner cada) estoura sozinha os 2.000 min/mes do plano
privado. Nao ha nenhuma intencao de distribuir o codigo — sem LICENSE, o padrao
e "todos os direitos reservados": qualquer um le, ninguem pode reusar.

O que muda no risco: qualquer pessoa passa a poder abrir PR, e PR executa
workflow. Estes testes trancam as duas portas por onde um PR hostil levaria
credencial embora.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((RAIZ / ".github" / "workflows").glob("*.yml"))


def _gatilhos(caminho: Path) -> dict:
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    # `on:` em YAML e o booleano True — a chave literal "on" so aparece quando
    # esta entre aspas no arquivo.
    on = dados.get(True, dados.get("on"))
    return on if isinstance(on, dict) else {str(on): None}


@pytest.mark.parametrize("wf", WORKFLOWS, ids=lambda p: p.stem)
def test_nenhum_workflow_usa_pull_request_target(wf):
    """`pull_request_target` roda com os SEGREDOS do repo no contexto do PR.

    Num repo publico isso e a porta larga: um PR de fork que so altere um passo
    do workflow ja exfiltra SUPABASE_SERVICE_ROLE_KEY e os treze tokens do
    YouTube. `pull_request` normal nao passa segredo para fork — este e o que
    passa.
    """
    assert "pull_request_target" not in _gatilhos(wf), (
        f"{wf.name} usa pull_request_target; num repo publico isso entrega os "
        f"secrets a qualquer PR de fork"
    )


@pytest.mark.parametrize(
    "wf", [w for w in WORKFLOWS if "pull_request" in _gatilhos(w)], ids=lambda p: p.stem
)
def test_workflow_que_roda_em_pr_nao_le_secret(wf):
    """Defesa em profundidade.

    O GitHub ja nao entrega segredo a workflow disparado por PR de fork, mas um
    workflow que DEPENDE de segredo e que tambem roda em PR e uma armadilha: ele
    passa a falhar de um jeito confuso, e a tentacao de "consertar" trocando o
    gatilho para pull_request_target e exatamente o erro que o teste acima pega.
    """
    assert "secrets." not in wf.read_text(encoding="utf-8"), (
        f"{wf.name} roda em pull_request e referencia secrets"
    )


def test_credencial_nao_entra_no_repositorio():
    """secrets/ guarda os tokens do YouTube em runtime e nunca e versionado."""
    ignorados = (RAIZ / ".gitignore").read_text(encoding="utf-8")

    assert "token*.json" in ignorados
    assert "client_secret*.json" in ignorados
    assert ".env" in ignorados
