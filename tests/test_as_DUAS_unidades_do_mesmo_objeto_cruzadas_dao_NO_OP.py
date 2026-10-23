# -*- coding: utf-8 -*-
"""AS DUAS UNIDADES DO MESMO OBJETO, CRUZADAS, DAO UM NO-OP SILENCIOSO.

Medido em 23/10 as 06:4x, escolhendo a familia do `kolejny-poziom-s099`. O
`segundo_angulo` expoe o MESMO objeto — o capitulo livre — em DUAS unidades:
`nao_mencionados` devolve **KICKER** (`str`) e `declarados_por_irmao` devolve
**INDICE** (`int`). Logo `set(livres) - set(declarados)` **nao remove nada**: a
intersecao crua e sempre vazia e a subtracao devolve o conjunto INTEIRO, bem
formado e com cara de resposta.

**Eu fiz essa conta a mao nesta rodada e ela me devolveu "53 estritamente
livres" onde a leitura certa da 32.** E o decimo primeiro membro da familia
desta sessao, e o pior tipo dela: o no-op devolve a resposta CONFORTAVEL (*"esta
tudo livre"*), como o `success` do RUN (22/10 as 13:4x) e o `.get(chave,
default)` sobre a resposta errada (08:3x). **E os dois donos sao MEUS e moram no
MESMO modulo.**

E o fato que o instrumento de 23/10 as 03:3x nomeia um nivel acima: quando dois
ids resolvem para o MESMO pacote, cada um ve so os irmaos que o declaram, logo a
leitura POR ID **subconta** o que ja foi usado.

O que este arquivo cobra, e por que nada aqui e identidade:
  * o no-op e **REPRODUZIDO** e **reprova se as unidades CONVERGIREM** — porque
    ai ele perde o objeto e esta nota tem de ser relida, nao o numero movido;
  * a subconta por id e cobrada como **PROPRIEDADE sobre o disco** (a uniao nunca
    e menor que a leitura por id) e o arquivo **reprova se NENHUM pacote for
    compartilhado** ou se TODOS forem — nos dois casos a frase nao distingue;
  * a aritmetica do `pauta_do_momento.quadro` e **RECONFERIDA** e o resultado e
    NEGATIVO: ela esta certa, e isso vai medido em vez de suposto;
  * a **FRONTEIRA** vai nos dois lados: capitulo declarado por irmao do OUTRO id
    entra na leitura por id e sai na do pacote;
  * a frase tem **UM dono**, sai nos **DOIS** ramos, e o `relato` a chama FORA de
    ramo condicional (20/10, 13:2x);
  * a conta e **DELEGADA** por AST ao `texto_dos_livres`, dono da juncao.
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao as CO         # noqa: E402
import pauta_do_momento as PM     # noqa: E402
import segundo_angulo as SA       # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")
PISO_ORIGENS = 20

# HISTORIA, e nenhum assert depende dela: os ids e os numeros mudam com a pauta,
# e consumir pauta e o trabalho (18/10 as 09:2x).
MEDIDA_DE_06H = {"pacote": "kolejny-poziom-004", "por_id": (30, 6), "uniao": 33,
                 "a_mao_dizia": 53, "certo": 32}


def _fonte(f):
    return textwrap.dedent(inspect.getsource(f))


def _chamados(f):
    out = set()
    for n in ast.walk(ast.parse(_fonte(f))):
        if isinstance(n, ast.Call):
            a = n.func
            if isinstance(a, ast.Name):
                out.add(a.id)
            elif isinstance(a, ast.Attribute):
                out.add(a.attr)
    return out


@pytest.fixture(scope="module")
def origens():
    """Toda origem com spec local dos tres canais, com o pacote resolvido."""
    out = []
    for canal in CANAIS:
        for oid in CO.contagem(canal):
            nm = SA.nao_mencionados(oid)
            if nm.get("pacote"):
                out.append((canal, oid, nm["pacote"]))
    assert len(out) >= PISO_ORIGENS, (
        "so %d origem(ns) com spec local: a varredura nao mede nada, e vazio de "
        "instrumento nao prova ausencia (17/10)" % len(out))
    return out


# ------------------------------------------------------------------ o no-op

def test_o_NO_OP_e_reproduzido_e_o_teste_reprova_se_as_unidades_convergirem(
        origens):
    """Sem isto, "eu errei a conta" seria afirmacao minha e nao medida."""
    testadas = 0
    for _, oid, _ in origens:
        nm = SA.nao_mencionados(oid)
        tl = SA.texto_dos_livres(oid)
        livres, decl = nm["nao_mencionados"], tl["declarados_por_irmao"]
        if not livres or not decl:
            continue
        testadas += 1
        assert isinstance(livres[0], str) and isinstance(decl[0], int), (
            "as unidades CONVERGIRAM em %s (%r contra %r): o no-op perde o "
            "objeto e esta nota tem de ser RELIDA" % (oid, livres[0], decl[0]))
        # o no-op: a subtracao crua nao remove NADA
        assert set(livres) - set(decl) == set(livres)
        assert set(livres) & set(decl) == set()
    assert testadas >= 5, testadas


def test_a_forma_CRUZAVEL_traz_as_duas_unidades(origens):
    _, oid, _ = origens[0]
    d = SA.livres_sem_declaracao(oid)
    assert len(d["indices"]) == len(d["kickers"]) == len(
        d["livres_sem_declaracao"])
    for x in d["livres_sem_declaracao"]:
        assert isinstance(x["indice"], int) and isinstance(x["kicker"], str)
        assert not x["declarado_por"]


def test_a_forma_cruzavel_CONCORDA_com_a_contagem_do_dono(origens):
    """Duas contas da mesma coisa tem de concordar com o dono da juncao."""
    for _, oid, _ in origens[:8]:
        tl = SA.texto_dos_livres(oid)
        d = SA.livres_sem_declaracao(oid)
        esperado = [x for x in tl["livres"] if not x.get("declarado_por")]
        assert d["indices"] == sorted(x["indice"] for x in esperado)


# -------------------------------------------------------- o pacote partilhado

def test_os_DOIS_lados_existem_no_disco_e_a_uniao_nunca_SUBCONTA(origens):
    """Reprova se NENHUM pacote for compartilhado ou se TODOS forem."""
    comp = nao = 0
    for _, oid, _ in origens:
        b = SA.livres_sem_declaracao_do_pacote(oid)
        a = SA.livres_sem_declaracao(oid)
        assert len(b["indices"]) <= len(a["indices"]), (
            "a leitura do PACOTE nao pode devolver MAIS livres que a por id "
            "em %s: a uniao das declaracoes so cresce" % oid)
        if b["compartilhado"]:
            comp += 1
            assert len(b["ids"]) > 1
        else:
            nao += 1
            assert b["indices"] == a["indices"]
    assert comp > 0, ("nenhum pacote da frota e compartilhado por dois ids: a "
                      "frase nao distingue nada e esta nota se rele")
    assert nao > 0, "todos compartilhados: o outro ramo nao existe mais"


def test_a_FRONTEIRA_vai_nos_dois_lados(origens):
    """Capitulo declarado por irmao do OUTRO id entra por id e sai por pacote."""
    achou = None
    for _, oid, _ in origens:
        b = SA.livres_sem_declaracao_do_pacote(oid)
        if not b["compartilhado"]:
            continue
        a = SA.livres_sem_declaracao(oid)
        so_por_id = set(a["indices"]) - set(b["indices"])
        if so_por_id:
            achou = (oid, so_por_id, a, b)
            break
    assert achou, ("perdeu a ancora: nenhum pacote compartilhado do disco tem "
                   "capitulo que a leitura por id da como livre e a do pacote "
                   "tira — sem ele este teste nao mede a subconta")
    oid, so_por_id, a, b = achou
    i = sorted(so_por_id)[0]
    assert i in a["indices"] and i not in b["indices"]
    assert i in b["declarados"], (i, b["declarados"][:8])


# ---------------------------------------------- o que NAO estava quebrado

def test_a_aritmetica_do_quadro_esta_CERTA_e_isso_e_MEDIDO(origens):
    """Resultado NEGATIVO: o `len(reserva) - len(declarados)` nao e o defeito.

    Vender conserto de defeito que nao ocorreu seria o avesso da medicao.
    """
    for _, oid, _ in origens:
        nm = SA.nao_mencionados(oid)
        tl = SA.texto_dos_livres(oid)
        livres_idx = {x["indice"] for x in tl["livres"]}
        decl = set(tl["declarados_por_irmao"])
        assert decl <= livres_idx, (
            "indice declarado FORA dos livres em %s: a subtracao de CONTAGENS "
            "do `pauta_do_momento` passa a subcontar e isto se rele" % oid)
        assert len(nm["nao_mencionados"]) - len(decl) >= 0, oid


# ------------------------------------------------------------------ a frase

def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos(origens):
    fonte = open(os.path.join(RAIZ, "fabrica", "segundo_angulo.py"),
                 encoding="utf-8").read()
    donos = [n.name for n in ast.walk(ast.parse(fonte))
             if isinstance(n, ast.FunctionDef)
             and "_PRE_UNID" in textwrap.dedent(ast.unparse(n))]
    assert donos == ["_linha_das_unidades"], donos
    com = sem = None
    for _, oid, _ in origens:
        b = SA.livres_sem_declaracao_do_pacote(oid)
        if b["compartilhado"] and com is None:
            com = SA._linha_das_unidades(b)
        if not b["compartilhado"] and sem is None:
            sem = SA._linha_das_unidades(b)
    assert com and sem
    for t in (com, sem):
        assert "no-op" in t and "KICKER" in t and "INDICE" in t
    assert "COMPARTILHADO" in com and "COMPARTILHADO" not in sem


def test_o_relato_chama_a_frase_FORA_de_ramo_condicional():
    fn = ast.parse(_fonte(SA.relato_dos_livres)).body[0]
    assert any(isinstance(s, ast.Expr) and "_linha_das_unidades"
               in ast.unparse(s) for s in fn.body), (
        "a frase tem de sair no corpo do `relato`, nunca dentro de um `if`: "
        "conta a mao se faz nas rodadas em que nada chama atencao")


# ------------------------------------------------------------- a delegacao

def test_a_conta_e_DELEGADA_por_AST():
    for f in (SA.livres_sem_declaracao, SA.livres_sem_declaracao_do_pacote):
        ch = _chamados(f)
        assert "texto_dos_livres" in ch, (f.__name__, ch)
        for proibido in ("finditer", "glob", "load", "_cenas_do_longo",
                         "declarados_pelos_irmaos"):
            assert proibido not in ch, (
                "%s nao pode %s: a juncao das duas unidades tem UM dono"
                % (f.__name__, proibido))
    # e o dono da resolucao id -> pacote e o `pacote_do_id`
    assert "pacote_do_id" in _chamados(SA._ids_do_pacote)


def test_o_mapa_id_pacote_tem_MEMORIA_e_ela_se_invalida(tmp_path):
    """Sem memoria ele custa 7,6 s por chamada e ninguem o chama (classe dos
    layouts mortos); com memoria presa ao DIRETORIO ele leria o mapa velho."""
    import json as _json
    import time as _time
    d = tmp_path / "specs"
    d.mkdir()
    (d / "canalx-001.json").write_text(_json.dumps(
        {"pacote": "canalx-001", "slug": "canalx-001",
         "longo": [{"kicker": "A", "nar": "a"}], "copy": "# canalx-001"}),
        encoding="utf-8")
    (d / "canalx-s001.json").write_text(_json.dumps(
        {"pacote": "canalx-s001", "slug": "canalx-s001", "longo": [],
         "longo_existente": "AAAAAAAAAAA",
         "copy": "# canalx-s001\n\n## FONTES\nOrigem canalx-001."}),
        encoding="utf-8")
    t0 = _time.time()
    m1 = SA._mapa_id_pacote(str(d))
    frio = _time.time() - t0
    t0 = _time.time()
    m2 = SA._mapa_id_pacote(str(d))
    quente = _time.time() - t0
    assert m1 == m2 == {"AAAAAAAAAAA": "canalx-001"}, m1
    assert quente <= frio, (frio, quente)
    # a memoria se INVALIDA com spec nova no MESMO diretorio
    (d / "canalx-s002.json").write_text(_json.dumps(
        {"pacote": "canalx-s002", "slug": "canalx-s002", "longo": [],
         "longo_existente": "BBBBBBBBBBB",
         "copy": "# canalx-s002\n\n## FONTES\nOrigem canalx-001."}),
        encoding="utf-8")
    m3 = SA._mapa_id_pacote(str(d))
    assert set(m3) == {"AAAAAAAAAAA", "BBBBBBBBBBB"}, m3


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = SA.livres_sem_declaracao.__doc__ + \
        SA.livres_sem_declaracao_do_pacote.__doc__
    for m in ("no-op", "KICKER", "INDICE", "53", "32", "UNIAO", "47"):
        assert m in doc, m
    # e a medida do custo, que e o motivo da memoria
    assert "7,6 s" in SA._mapa_id_pacote.__doc__
