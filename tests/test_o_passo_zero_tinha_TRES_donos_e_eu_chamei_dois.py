"""O passo zero tinha TRES donos e eu chamei DOIS — 19/10/2026, 23:3x.

Nesta rodada eu pedi inscritos ao `leitura_de_inscritos` e o canal ao
`concentracao_frota`, e contei a COTA com um laco Python descartavel sobre o
`duracoes-a-medir.jsonl`, com o corte das 07:00 **digitado com a data de hoje**.
O `janela_de_cota.py` existe desde a manha, e o teste dele se chama
`test_contar_a_janela_de_cota_deixou_de_ser_de_cabeca`.

O custo esta MEDIDO e nao e estetico: a rodada das 00:07 cai entre 00:00 e
07:00 UTC, quando a janela corrente abriu no dia ANTERIOR. O corte digitado com
a data de hoje devolve ZERO envios onde a janela tem dezenove — isto e, eu
relataria *"a janela esta livre"* com 30.400 unidades dentro dela. E o 771 na
direcao que apaga as ultimas horas.

A FORMA DESTES TESTES e o que vale: a delegacao e cobrada por AST (o docstring
do modulo CITA os nomes dos donos na prosa, e casar prosa pegaria a
explicacao), o defeito da janela e medido com um parque PROPRIO em vez do
arquivo vivo — ancorar no arquivo vivo seria identidade onde ha propriedade
(743/753/761) e a proxima publicacao mudaria o numero —, e a contraprova vai
nos DOIS sentidos: fora da banda das 00:00-07:00 as duas contas CONCORDAM,
senao "o laco a mao erra sempre" passaria por qualquer motivo.
"""
import ast
import datetime
import json
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "passo_zero.py")
PARQUE = os.path.join(RAIZ, "docs", "pendente", "duracoes-a-medir.jsonl")
sys.path.insert(0, FABRICA)

UTC = datetime.timezone.utc


def _fonte():
    return open(MODULO, encoding="utf-8").read()


def _chamadas(arvore):
    """Todo `mod.func` chamado no codigo — por AST, nao por texto."""
    fora = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute):
            alvo = no.func.value
            if isinstance(alvo, ast.Name):
                fora.add("%s.%s" % (alvo.id, no.func.attr))
    return fora


def _parque_de_teste(caminho):
    """Um parque PROPRIO: um envio ANTES da virada e tres dentro da janela.

    Nada no FUTURO dos dois instantes de teste, de proposito: nem o laco a mao
    nem o `janela_de_cota.envios` tem limite de CIMA, e esse e outro defeito
    (medido em 19/10 as 13:2x, no irmao `concentracao_frota`). Misturar os dois
    aqui faria este arquivo medir duas coisas e provar nenhuma.
    """
    linhas = [
        {"pacote": "a-s000", "youtube_id": "ZZZ", "em": "2026-10-19T06:00:00Z"},
        {"pacote": "a-s001", "youtube_id": "AAA", "em": "2026-10-19T08:00:00Z"},
        {"pacote": "a-s002", "youtube_id": "BBB", "em": "2026-10-19T18:00:00Z"},
        {"pacote": "a-s003", "youtube_id": "CCC", "em": "2026-10-19T23:00:00Z"},
    ]
    with open(caminho, "w", encoding="utf-8") as f:
        for d in linhas:
            f.write(json.dumps(d) + "\n")
    return caminho


def _a_mao(caminho, agora):
    """O laco que eu escrevi nesta rodada: corte com a data de HOJE digitada."""
    corte = agora.strftime("%Y-%m-%dT07:00:00Z")
    n = 0
    for linha in open(caminho, encoding="utf-8"):
        linha = linha.strip()
        if not linha:
            continue
        if json.loads(linha)["em"] >= corte:
            n += 1
    return n


# ---------------------------------------------------------------- a delegacao

def test_ele_CHAMA_os_tres_donos_e_nao_refaz_conta_nenhuma():
    arvore = ast.parse(_fonte())
    chamadas = _chamadas(arvore)
    for esperada in ("leitura_de_inscritos.relato",
                     "concentracao_frota.escolha_do_momento",
                     "janela_de_cota.relato"):
        assert esperada in chamadas, (
            "o passo zero tem de PEDIR ao dono: falta %s. Refazer a conta aqui "
            "criaria o segundo dono." % esperada)


def test_ele_NAO_le_o_parque_nem_deriva_a_virada_por_conta_propria():
    arvore = ast.parse(_fonte())
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
            assert no.func.id != "open", (
                "o passo zero abriu arquivo: o parque tem UM dono, o "
                "`janela_de_cota`. Foi exactamente este laco que errou.")
    fonte = _fonte()
    corpo = fonte.split('"""', 2)[2] if fonte.count('"""') >= 2 else fonte
    for proibido in ("07:00:00Z", "HORA_DA_VIRADA =", "piso_de_resolucao("):
        assert proibido not in corpo, (
            "o corpo recalcula %r — isso e o segundo dono da mesma regra." % proibido)


# -------------------------------------------- o defeito medido, nos dois lados

def test_na_banda_das_00_as_07_o_laco_A_MAO_zera_e_o_instrumento_nao(tmp_path):
    import janela_de_cota as JC
    caminho = _parque_de_teste(str(tmp_path / "parque.jsonl"))
    agora = datetime.datetime(2026, 10, 20, 0, 7, tzinfo=UTC)

    assert JC.abertura(agora) == datetime.datetime(2026, 10, 19, 7, 0, tzinfo=UTC)
    do_instrumento = len(JC.envios(agora, caminho))
    assert do_instrumento == 3, do_instrumento
    assert _a_mao(caminho, agora) == 0, (
        "sem este zero o arquivo nao mede o defeito que o produziu")


def test_fora_da_banda_as_duas_contas_CONCORDAM(tmp_path):
    """Contraprova no outro sentido: o laco a mao nao erra SEMPRE."""
    import janela_de_cota as JC
    caminho = _parque_de_teste(str(tmp_path / "parque.jsonl"))
    agora = datetime.datetime(2026, 10, 19, 23, 10, tzinfo=UTC)
    assert len(JC.envios(agora, caminho)) == _a_mao(caminho, agora) == 3


def test_a_tabela_do_custo_medido_continua_escrita_no_modulo():
    fonte = _fonte()
    for marca in ("ZERO envios", "30.400", "11:2x"):
        assert marca in fonte, (
            "conserto sem o custo medido escrito volta calado: falta %r" % marca)


# ------------------------------------------------------------------- o relato

def test_o_relato_traz_as_TRES_secoes_na_ordem():
    import passo_zero
    agora = datetime.datetime(2026, 10, 19, 23, 10, tzinfo=UTC)
    texto = passo_zero.relato(agora)
    pos = [texto.index(m) for m in ("LEITURA DE INSCRITOS", "CANAL na janela",
                                    "JANELA DE COTA")]
    assert pos == sorted(pos), (
        "as tres secoes do passo zero tem de sair, e nesta ordem: %s" % pos)


def test_o_empate_do_canal_vai_NOMEADO_quando_houver():
    """Propriedade, nao identidade: nao nomeia canal nenhum (743/753/761)."""
    import passo_zero
    com = passo_zero._linha_do_canal(
        {"contagem": {"x": 9, "y": 9}, "janela_h": 24.0,
         "escolhido": "x", "empatados": ["x", "y"], "houve_empate": True})
    sem = passo_zero._linha_do_canal(
        {"contagem": {"x": 9, "y": 2}, "janela_h": 24.0,
         "escolhido": "y", "empatados": ["y"], "houve_empate": False})
    assert "EMPATE" in com and "EMPATE" not in sem


def test_ele_INFORMA_e_o_codigo_de_saida_e_SEMPRE_zero():
    r = subprocess.run([sys.executable, MODULO], cwd=FABRICA,
                       capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stderr[-800:]
    assert "NAO REPROVA" in r.stdout


# ----------------------------------------------------------------- vacuidade

def test_o_parque_vivo_tem_envio_bastante_para_a_conta_valer():
    with open(PARQUE, encoding="utf-8") as f:
        ids = {json.loads(l)["youtube_id"] for l in f
               if l.strip() and json.loads(l).get("youtube_id")}
    assert len(ids) >= 30, (
        "com parque pequeno a contagem da janela nao mede nada: %d ids" % len(ids))
