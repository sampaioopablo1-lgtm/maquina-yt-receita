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


def test_a_autoria_nao_tem_cron_e_so_roda_a_mao():
    """24/08/2026, decisao do dono: o processo nao usa credencial de LLM.

    A autoria era a UNICA etapa que exigia uma, e nunca teve — 54 falhas em 55
    execucoes desde 20/08, sempre no mesmo passo, duas vezes por hora. Workflow
    que so falha nao e recurso desligado, e alarme quebrado: treina quem olha o
    Actions a ignorar vermelho, e o proximo vermelho de verdade passa batido.

    O `workflow_dispatch` continua, de proposito — se um dia houver credencial,
    isto volta sem reescrever nada. Se o cron VOLTAR, o veredito de "sem chave"
    tem de voltar a ser vermelho junto (ver o teste da chave, abaixo): verde sem
    cron e "desligado"; verde com cron e o defeito do aprendizado 370.
    """
    assert re.search(r'cron: "([^"]+)"', EXECUTAVEL) is None, (
        "voltou cron na autoria: se foi de proposito, o passo da chave precisa "
        "voltar a derrubar o run quando o segredo faltar")
    # `on:` vira o booleano True no YAML 1.1 que o PyYAML fala — a chave do
    # dicionario e True, nao a string "on". Por isso a busca cobre os dois.
    gatilhos = DOC.get("on", DOC.get(True, {}))
    assert "workflow_dispatch" in gatilhos, (
        "sem cron E sem workflow_dispatch a autoria ficaria inalcancavel")
    assert "schedule" not in gatilhos


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


# ------------------------------------------- o que o primeiro disparo ensinou

def test_a_chave_e_conferida_antes_do_laco_e_governa_os_passos():
    """A conferencia continua vindo antes do laco, pelo motivo original: sem
    ela o `autor.py` falha por canal, o `|| true` engole o codigo de saida e o
    job termina verde sem escrever nada (run 32349960529, 20/08/2026).

    O que mudou em 24/08 e o VEREDITO, nao a conferencia. Sem cron, ausencia de
    chave e "desligado", nao erro. Mas entao os passos seguintes PRECISAM ser
    guardados por ela: com o `Escrever` pulado, `outputs.escritas` vem VAZIO, e
    `'' != '0'` e verdadeiro — sem a guarda, o passo de commit rodaria num job
    que nao escreveu nada.
    """
    passos = DOC["jobs"]["escrever"]["steps"]
    nomes = [p.get("name") for p in passos]
    i_chave = nomes.index("Conferir a chave da API")
    i_escrever = nomes.index("Escrever")
    assert i_chave < i_escrever

    chave = passos[i_chave]
    assert chave.get("id") == "chave", "os outros passos dependem deste id"
    assert "::notice::" in chave["run"], "sem cron, falta de chave e aviso"
    assert "exit 1" not in chave["run"], (
        "sem cron, falta de credencial nao e erro — e a decisao do dono")

    # Todo passo depois da conferencia tem de exigir a chave, senao roda a seco.
    for passo in passos[i_chave + 1:]:
        cond = str(passo.get("if", ""))
        assert "steps.chave.outputs.tem == 'sim'" in cond, (
            f"passo {passo.get('name')!r} roda mesmo sem credencial")


def test_o_laco_desliga_o_e_de_proposito_e_diz_por_que():
    """O shell padrao do runner e `bash -e`: sem `set +e`, um canal que falha
    aborta o passo e os outros doze nem sao tentados."""
    passo = next(p for p in DOC["jobs"]["escrever"]["steps"]
                 if p.get("id") == "escrever")
    assert "set +e" in passo["run"]
    assert "CODIGO=$?" in passo["run"]


def test_carencia_sem_escrita_vira_aviso_e_nao_recado_discreto():
    """A diferenca entre um notice e um warning aqui e a diferenca entre
    alguem descobrir hoje ou na semana que vem."""
    passo = next(p for p in DOC["jobs"]["escrever"]["steps"]
                 if p.get("id") == "escrever")
    assert "::warning::" in passo["run"]
    assert "carentes=" in passo["run"]


def test_pauta_esgotada_nao_e_lida_como_fila_cheia():
    """Codigo 3 do `carencia`: ha canal precisando de spec e nenhum com pauta.
    Sem um codigo proprio o workflow leria lista vazia como "nada a fazer"."""
    passo = next(p for p in DOC["jobs"]["escrever"]["steps"]
                 if p.get("id") == "escrever")
    assert '"$CARENCIA" = "3"' in passo["run"]
    assert "fila esta cheia" not in passo["run"].split('"$CARENCIA" = "3"')[1][:600]


def test_o_recado_final_so_aparece_quando_ha_carencia():
    passo = next(p for p in DOC["jobs"]["escrever"]["steps"]
                 if p.get("name") == "Nada escrito")
    assert "carentes != '0'" in passo["if"]


def test_carencia_devolve_tambem_quantas_pautas_ha():
    """Carencia sem pauta nao e trabalho disponivel, e um canal esperando
    pesquisa. Ordenar so por carencia entrega justamente o canal que nao tem
    como produzir — o canal mais carente costuma ser o que a pesquisa nao
    visita ha mais tempo."""
    import inspect

    import autor

    fonte = inspect.getsource(autor.carencia)
    assert "pautas_disponiveis" in fonte
    assert "(s, f, p)" in fonte
