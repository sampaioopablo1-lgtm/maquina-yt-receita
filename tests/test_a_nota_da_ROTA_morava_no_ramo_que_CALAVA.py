# -*- coding: utf-8 -*-
"""A nota da ROTA morava no ramo que PARA de disparar quando ela importa.

**Medido em 20/10 as 13:2x, na PRIMEIRA rodada em que o criterio do 723 passou
por TEMPO.** Em vinte e duas rodadas seguidas o `leitura_de_inscritos` recusou a
leitura de inscritos, e nas vinte e duas a recusa saiu do ramo
`degrau and not resolve_duas_contagens` — que e onde a nota da rota morava.
Nesta rodada a janela finalmente autorizou (27,05 h, piso 0,89/dia) e o relato
imprimiu **tres SIM e nada sobre a rota**, que estava `negado_por_politica`.
Falha PERMISSIVA no sentido pior: ela convida a gastar requisicao.

E a nota era PROSA CRAVADA (*"a rota que fechou por LIMITE em 19/10 as 06:1x"*),
isto e um modo MEDIDO naquele dia reescrito a mao numa string — o 753 em forma
de procedencia —, quando o modo desta rodada e outro e o remedio dele tambem.

O que estes testes cobram e PROPRIEDADE e nao a frase: que a linha da rota saia
nos DOIS ramos, que o conjunto de modos venha do DONO, e que sem sonda o modulo
RECUSE em vez de calar.
"""
import ast
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import leitura_de_inscritos as LI  # noqa: E402
import vivacidade_publica as VP  # noqa: E402
import passo_zero as PZ  # noqa: E402

MOD_LI = os.path.join(RAIZ, "fabrica", "leitura_de_inscritos.py")
MOD_PZ = os.path.join(RAIZ, "fabrica", "passo_zero.py")

# Uma leitura PROPRIA, com instante fixo, em vez do parque vivo: ancorar no vivo
# seria identidade onde ha propriedade (743/753/761), e o parque anda a cada
# rodada. O que importa e haver os dois lados da janela.
ANCORA = "2026-10-19T09:00:00Z"
RESOLVE = "2026-10-20T13:25:00Z"      # 28,4 h — passa o criterio do 723
NAO_RESOLVE = "2026-10-19T15:00:00Z"  # 6,0 h — passa a regra H e nao o 723


@pytest.fixture
def parque(tmp_path):
    p = tmp_path / "inscritos-lidos.jsonl"
    LI.grava(ANCORA, {"labtreinamento": 68, "epomeno-epipedo": 22,
                      "kolejny-poziom": 9},
             "fixture do teste", caminho=str(p))
    return str(p)


def _janela(parque):
    """Os DOIS lados da janela, conferidos antes de medir qualquer coisa."""
    a = LI.veredito(NAO_RESOLVE, caminho=parque)
    b = LI.veredito(RESOLVE, caminho=parque)
    assert a["degrau"] and not a["resolve_duas_contagens"], \
        "a fixture perdeu o lado que NAO resolve: %r" % (a,)
    assert b["resolve_duas_contagens"], \
        "a fixture perdeu o lado que RESOLVE: %r" % (b,)
    return a, b


def test_os_DOIS_lados_da_janela_existem_na_fixture(parque):
    """Sem os dois lados o arquivo passa por VACUIDADE e nao mede nada."""
    _janela(parque)


def test_a_linha_da_rota_sai_nos_DOIS_ramos(parque):
    """O DEFEITO: ela saia so no ramo da recusa, e calava quando importava."""
    _janela(parque)
    for agora in (NAO_RESOLVE, RESOLVE):
        r = LI.relato(agora, caminho=parque, modo_da_rota="negado_por_politica")
        assert "ROTA" in r, (
            "o ramo de %s nao fala da rota — e exatamente o defeito de 13:2x:\n%s"
            % (agora, r))
        assert "negado_por_politica" in r


def test_sem_sonda_ele_DIZ_que_a_rota_nao_foi_sondada(parque):
    """Ausencia de sonda nao e rota aberta — ele recusa, como o `porta1`."""
    _janela(parque)
    for agora in (NAO_RESOLVE, RESOLVE):
        r = LI.relato(agora, caminho=parque)
        assert "NAO SONDADA" in r, r
        v = LI.veredito(agora, caminho=parque)
        assert v["rota_sondada"] is False and v["modo_da_rota"] is None


def test_o_conjunto_de_modos_vem_do_DONO_nos_dois_sentidos():
    """`CONSEQUENCIA_DO_MODO` nao e lista minha: ela se confere com o dono.

    Nos DOIS sentidos de proposito. Chave a mais seria modo inventado como
    dado; chave a menos quer dizer que o dono ganhou um modo e ninguem escreveu
    o que ele significa para ESTA decisao — e a consequencia de cada modo e
    diferente (um pede economia, outro nao responde a volume nenhum).
    """
    donos = VP.modos()
    assert len(donos) >= 4, (
        "o dono devolveu %d modos: a derivacao por AST quebrou, e com ela toda "
        "conferencia deste arquivo passaria por vacuidade" % len(donos))
    nossas = set(LI.CONSEQUENCIA_DO_MODO)
    assert nossas - donos == set(), \
        "modo que o dono nao devolve: %s" % sorted(nossas - donos)
    assert donos - nossas == set(), \
        "modo do dono sem consequencia escrita: %s" % sorted(donos - nossas)


def test_modo_inventado_LEVANTA_em_vez_de_passar(parque):
    with pytest.raises(ValueError):
        LI.veredito(RESOLVE, caminho=parque, modo_da_rota="fechada")
    with pytest.raises(ValueError):
        LI.relato(RESOLVE, caminho=parque, modo_da_rota="rota_morta")


def test_o_aviso_das_duas_portas_NAO_dispara_com_a_rota_aberta(parque):
    """Contraprova no outro sentido: sem ela o aviso sairia sempre."""
    _janela(parque)
    fechada = LI.relato(RESOLVE, caminho=parque,
                        modo_da_rota="negado_por_politica")
    aberta = LI.relato(RESOLVE, caminho=parque, modo_da_rota="aberta")
    assert "a JANELA autoriza e a ROTA nao" in fechada
    assert "a JANELA autoriza e a ROTA nao" not in aberta, aberta
    assert "ROTA" in aberta, "com a rota aberta ele ainda tem de NOMEAR o modo"


def test_o_relato_nao_AFIRMA_mais_um_modo_por_prosa_cravada(parque):
    """O 753 em procedencia: modo medido num dia, reescrito a mao numa string.

    Cobrado na SAIDA e nao na fonte, porque o docstring do modulo cita a frase
    antiga como HISTORIA de proposito — e casar a fonte pegaria a explicacao em
    vez do codigo.
    """
    _janela(parque)
    for agora in (NAO_RESOLVE, RESOLVE):
        for modo in (None, "aberta", "limite", "negado_por_politica"):
            r = LI.relato(agora, caminho=parque, modo_da_rota=modo)
            assert "fechou por LIMITE em 19/10" not in r, r


def test_a_frase_da_rota_tem_UM_dono(parque):
    """Por AST: so o `_linha_da_rota` monta a linha da rota.

    Ter dois donos dela era o defeito — a nota vivia no ramo da recusa e o
    ramo que resolve nao tinha nenhuma.
    """
    with open(MOD_LI, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    fora = []
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef) or no.name == "_linha_da_rota":
            continue
        for dentro in ast.walk(no):
            if isinstance(dentro, ast.Constant) and \
                    isinstance(dentro.value, str) and \
                    dentro.value.strip().startswith("  ROTA"):
                fora.append(no.name)
    assert fora == [], "a linha da rota tem um segundo dono em %s" % fora


def test_o_passo_zero_REPASSA_o_modo_e_nao_o_confere():
    """Por AST: ele passa `modo_da_rota` ao dono, em vez de decidir aqui."""
    with open(MOD_PZ, encoding="utf-8") as f:
        fonte = f.read()
    arvore = ast.parse(fonte)
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "_secoes"]
    assert alvo, "o `_secoes` mudou de nome"
    assert any(a.arg == "modo_da_rota" for a in alvo[0].args.args), \
        "o `_secoes` nao recebe o modo da rota"
    repassa = False
    for no in ast.walk(alvo[0]):
        if isinstance(no, ast.Call):
            for kw in no.keywords:
                if kw.arg == "modo_da_rota":
                    repassa = True
    assert repassa, "o `passo_zero` recebe o modo e nao o repassa ao dono"
    # Por AST, e nao por `in fonte`: a PRIMEIRA versao deste teste casava a
    # prosa e reprovou o modulo CERTO, porque o docstring dele CITA
    # `modo_de_fechamento` para dizer de onde o modo vem. Era o teste errado,
    # e e a mesma licao do `test_NAO_virou_portao` do acento.
    proibidos = {"modo_de_fechamento", "CONSEQUENCIA_DO_MODO", "modos"}
    achados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Attribute) and no.attr in proibidos:
            achados.add(no.attr)
        if isinstance(no, ast.Name) and no.id in proibidos:
            achados.add(no.id)
    assert achados == set(), (
        "o `passo_zero` passou a decidir o modo: %s no CODIGO dele seria o "
        "segundo dono da pergunta" % sorted(achados))


def test_o_relato_do_passo_zero_carrega_a_rota():
    """O caminho inteiro, nao so a funcao: o defeito era de CHAMADOR."""
    import datetime
    agora = datetime.datetime(2026, 10, 20, 13, 25,
                              tzinfo=datetime.timezone.utc)
    r = PZ.relato(agora, modo_da_rota="negado_por_politica")
    assert "negado_por_politica" in r
    assert "Network access" in r, (
        "o remedio deste modo e do DONO e tem de ir em letra, senao ele se "
        "confunde com o `limite`, cujo remedio e economizar requisicao")
    sem = PZ.relato(agora)
    assert "NAO SONDADA" in sem


def test_o_MOTIVO_continua_escrito_no_modulo():
    """Sem ele a rodada seguinte devolve a nota para dentro do ramo."""
    with open(MOD_LI, encoding="utf-8") as f:
        fonte = f.read()
    for pedaco in ("13:2x", "PERMISSIVA", "vinte e duas"):
        assert pedaco in fonte, "o motivo do conserto perdeu %r" % pedaco
