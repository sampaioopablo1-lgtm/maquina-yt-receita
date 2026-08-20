"""O workflow que escreve as specs — a perna que faltava no ciclo.

Escrever pauta era a unica etapa humana da maquina: uma spec por disparo da
rotina horaria, no melhor dia 24 para treze canais, contra a meta de 65. Em
20/08/2026 oito dos treze canais tinham ZERO spec pendente com o teto ja em 5 —
o teto nunca foi o que segurava a frota.

Estes testes cercam o que, num workflow, so falha em producao: permissao que
falta, concorrencia que duplica, e o portao que se contorna.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

WF = RAIZ / ".github" / "workflows" / "autoria.yml"
FONTE = WF.read_text(encoding="utf-8")

yaml = pytest.importorskip("yaml")
DOC = yaml.safe_load(FONTE)

# YAML 1.1 le `on:` como o booleano true, entao a chave do gatilho nao e a
# string "on". Nao e curiosidade: um teste que procurasse DOC["on"] daria
# KeyError e seria "consertado" apagando o teste.
GATILHOS = DOC.get("on", DOC.get(True))

# O que o job EXECUTA, sem os comentarios. Os comentarios deste workflow citam
# `frota.yml` e `publicar.py` para explicar o que ele nao faz — procurar essas
# palavras no arquivo inteiro acusaria a propria explicacao.
EXECUTAVEL = "\n".join(l for l in FONTE.splitlines()
                       if not l.lstrip().startswith("#"))


def test_o_workflow_e_yaml_valido():
    assert DOC["name"]
    assert "escrever" in DOC["jobs"]


def test_precisa_de_permissao_para_commitar():
    """A spec so chega na frota pelo repositorio — `contents: read` faria o job
    passar verde e nao entregar nada."""
    assert DOC["permissions"]["contents"] == "write"


def test_a_concorrencia_nao_cancela_a_execucao_em_voo():
    """Duas autorias juntas escreveriam o MESMO numero de pacote: o
    `proximo_numero` le o diretorio, e o diretorio so muda depois do commit.
    Cancelar a que esta em voo jogaria fora uma geracao ja paga."""
    c = DOC["concurrency"]
    assert c["group"] == "autoria"
    assert c["cancel-in-progress"] is False


def test_o_disparo_padrao_e_conservador():
    """O custo por pacote ainda nao foi medido. Escolher o ritmo antes de ter a
    medida e escolher no escuro."""
    assert GATILHOS["workflow_dispatch"]["inputs"]["pacotes"]["default"] == "1"


def test_nao_publica_nem_renderiza():
    """Este workflow escreve e commita. Publicar daqui pularia o `prontidao`,
    o teto por canal do `orquestra` e a trava de titulo do `publicar`."""
    for proibido in ("publicar.py", "fabrica.py", "frota.yml", "videos.insert",
                     "workflows/frota.yml/dispatches"):
        assert proibido not in EXECUTAVEL, proibido


def test_a_chave_da_api_chega_ao_passo_que_escreve():
    passo = next(p for p in DOC["jobs"]["escrever"]["steps"]
                 if p.get("id") == "escrever")
    assert "ANTHROPIC_API_KEY" in passo["env"]
    assert "SUPABASE_SERVICE_ROLE_KEY" in passo["env"]


def test_instala_as_fontes_que_o_portao_de_glifos_exige():
    """Sem Devanagari o agla-level e reprovado por defeito do AMBIENTE, e o
    gerador tentaria consertar um roteiro que nao tem defeito nenhum."""
    assert "fonts-noto-core" in EXECUTAVEL


def test_a_spec_reprovada_vai_junto_no_commit():
    """Apagar a reprovada em silencio esconderia quanto o gerador erra — que e
    exatamente o numero que decide se isto continua ligado."""
    assert "git add fabrica/specs/" in EXECUTAVEL
    assert "reprovado" in FONTE


def test_o_push_retenta():
    assert re.search(r"for t in .*; do\s*\n\s*git push", EXECUTAVEL)


def test_o_cron_existe_e_nao_e_de_minuto_em_minuto():
    m = re.search(r'cron: "([^"]+)"', EXECUTAVEL)
    assert m
    minuto, hora = m.group(1).split()[:2]
    assert minuto != "*" and hora != "*", "autoria a cada minuto gastaria a conta"


# ------------------------------------------------------- o portao nao se pula

def test_o_gerador_carimba_autoria_de_maquina():
    """Sem o carimbo o `_gate_fatos` nao se aplica e o roteiro passa sem que
    nenhum numero tenha sido conferido."""
    import autor

    ctx = autor.contexto("labtreinamento")
    sp = autor._monta(ctx, {"longo": [], "short": [], "thumb": {}, "copy": ""}, 9)
    assert sp["autoria"] == "maquina"


def test_a_selecao_da_frota_confere_os_fatos():
    """`_falhas_baratas` e o que decide a matriz do frota.yml. Sem o portao de
    fatos ali, uma spec de maquina sem veredito entraria na matriz e so seria
    barrada depois do checkout — ou nao seria barrada."""
    import inspect

    import orquestra

    assert "_gate_fatos" in inspect.getsource(orquestra._falhas_baratas)


def test_spec_de_maquina_sem_veredito_nao_entra_na_matriz(tmp_path, monkeypatch):
    import json

    import orquestra

    sp = json.loads((RAIZ / "fabrica" / "specs" / "labtreinamento-003.json")
                    .read_text(encoding="utf-8"))
    sp["autoria"] = "maquina"
    sp.pop("fatos", None)
    alvo = RAIZ / "fabrica" / "specs" / "labtreinamento-999.json"
    alvo.write_text(json.dumps(sp, ensure_ascii=False), encoding="utf-8")
    try:
        faltas = orquestra._falhas_baratas("labtreinamento-999", sp)
        assert any("veredito de fatos" in f for f in faltas), faltas
    finally:
        alvo.unlink()
