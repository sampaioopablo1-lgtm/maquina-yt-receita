# -*- coding: utf-8 -*-
"""Os usos por TEXTO existiam e NAO cruzavam com a escolha da pauta.

**Medido em 23/10 as 11:3x, escolhendo a pauta do `labtreinamento-s116`.** O
`_compartilhados` agrupa as origens por pacote desde 23/10 as 03:3x e o
`escolha` ja soma os usos em `usos_por_pacote` — e NENHUMA das duas leituras
do desempate era cruzada contra essa soma. Eu escrevi o laco na linha de
comando para decidir se desviava da regra escrita, que e o item 3 da §10.

E a conta MUDA a decisao, nao o relato: o vao da divergencia era de 64%, acima
do precedente de 62% em que a rodada de 22/10 as 17:3x desviou — e a leitura
SEM DECLARACAO apontava uma origem de pacote COMPARTILHADO com 14 usos por
TEXTO, o MAXIMO do canal. Desviar levaria a origem mais usada do canal, que e
o contrario do que o `concentracao.py` existe para evitar.

A medida de 23/10 as 11:3x vai como HISTORIA e **nenhum assert depende dela**:
contagem absoluta sobre populacao que cresce uma spec por rodada e identidade
disfarcada de medida (a licao de 22/10 as 14:4x). O que se cobra e a
PROPRIEDADE, canal por canal, lida do disco.
"""
import ast
import inspect
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
if FABRICA not in sys.path:
    sys.path.insert(0, FABRICA)

import pauta_do_momento as PM  # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

# HISTORIA da medicao de 23/10 as 11:3x, com a peca da rodada FORA da
# varredura. Nenhum assert depende destes numeros.
MEDIDA_DE_11H = {
    "labtreinamento": {"escrita": 7, "sem_declaracao": 14, "maximo": 14},
    "epomeno-epipedo": {"escrita": 5, "sem_declaracao": 5, "maximo": 12},
    "kolejny-poziom": {"escrita": 9, "sem_declaracao": 9, "maximo": 12},
}


@pytest.fixture(scope="module")
def escolhas():
    fora = {}
    for c in CANAIS:
        fora[c] = PM.escolha(c)
    return fora


def _fonte():
    return inspect.getsource(PM)


def _func(nome):
    for n in ast.walk(ast.parse(_fonte())):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    raise AssertionError("funcao %r nao existe" % nome)


# ------------------------------------------------------------ o disco responde

def test_a_varredura_sai_do_DISCO_e_reprova_por_vacuidade(escolhas):
    for c, e in escolhas.items():
        q = e["quadro"]
        assert len(q) >= 8, (c, len(q),
                             "quadro curto: o arquivo passaria por vacuidade")


def test_o_maximo_por_texto_nao_e_menor_que_nenhum_uso_por_id(escolhas):
    """PROPRIEDADE e nao numero: o maximo por texto limita por cima."""
    for c, e in escolhas.items():
        m = PM.concentracao_da_escolha(e)["maximo_por_texto"]
        for x in e["quadro"]:
            assert m >= x["usos"], (c, x["origem"], x["usos"], m)


# ------------------------------------------------------- as duas contas batem

def test_origem_FORA_de_pacote_compartilhado_conta_igual(escolhas):
    """Contraprova no outro sentido: sem pacote com duas origens as duas
    contas COINCIDEM, senao `usos_por_texto` inflaria tudo."""
    vistos = 0
    for c, e in escolhas.items():
        comp = e.get("compartilhados") or {}
        for x in e["quadro"]:
            if x.get("pacote") in comp:
                continue
            assert PM.usos_por_texto(e, x["origem"]) == x["usos"], (c, x)
            vistos += 1
    assert vistos >= 20, (vistos, "poucas origens fora de compartilhado: "
                                  "a contraprova nao mediu nada")


def test_origem_EM_pacote_compartilhado_conta_a_SOMA(escolhas):
    """E ela e ESTRITAMENTE maior que a do id, senao nao haveria defeito."""
    vistos = 0
    for c, e in escolhas.items():
        comp = e.get("compartilhados") or {}
        for pac, ids in comp.items():
            soma = (e.get("usos_por_pacote") or {}).get(pac)
            for oid in ids:
                v = PM.usos_por_texto(e, oid)
                assert v == soma, (c, pac, oid, v, soma)
                linha = [x for x in e["quadro"] if x["origem"] == oid][0]
                assert v > linha["usos"], (c, oid, v, linha["usos"])
                vistos += 1
    assert vistos >= 2, (vistos, "nenhum pacote compartilhado no disco: "
                                 "esta nota perdeu o objeto e se rele")


def test_as_duas_contas_da_mesma_coisa_CONCORDAM_com_o_dono(escolhas):
    for c, e in escolhas.items():
        for pac, soma in (e.get("usos_por_pacote") or {}).items():
            ids = (e.get("compartilhados") or {}).get(pac) or []
            assert ids, (c, pac)
            assert soma == sum(x["usos"] for x in e["quadro"]
                               if x["origem"] in ids), (c, pac)


def test_origem_que_nao_esta_no_quadro_devolve_None(escolhas):
    """Nao inventa contagem, do jeito que o `porta1` recusa janela curta."""
    e = escolhas["labtreinamento"]
    assert PM.usos_por_texto(e, "NAO-EXISTE-xxxxx") is None


# ------------------------------------------------------- os DOIS lados existem

def test_os_DOIS_lados_existem_no_disco(escolhas):
    """Reprova se TODOS os canais caírem no maximo OU se NENHUM cair.

    Sem o primeiro lado a frase do alerta nunca sai e o arquivo nao mede nada;
    sem o segundo ela sai sempre e, pelo argumento do `mira.py`, deixa de
    avisar.
    """
    caem = []
    for c, e in escolhas.items():
        ls = PM.concentracao_da_escolha(e)["leituras"]
        caem.append(any(x and x["e_o_maximo_do_canal"] for x in ls.values()))
    assert any(caem), "nenhum canal cai no maximo por texto — esta nota se rele"
    assert not all(caem), ("todos caem: a frase passaria a sair sempre e "
                           "deixaria de avisar")


def test_o_defeito_atinge_as_DUAS_leituras_e_nao_so_a_nova(escolhas):
    """O que torna o achado maior que o do desempate: em algum canal e a
    PROPRIA regra escrita que cai em pacote compartilhado."""
    comp_escrita = []
    for c, e in escolhas.items():
        x = PM.concentracao_da_escolha(e)["leituras"].get("regra_escrita")
        comp_escrita.append(bool(x and x["compartilhado"]))
    assert any(comp_escrita), ("nenhum canal tem a regra escrita em pacote "
                              "compartilhado — o achado vira so da leitura "
                              "nova e esta nota se rele")


# ------------------------------------------------------------------- a frase

def test_a_frase_tem_UM_dono_por_AST():
    """A deteccao inclui o NOME da constante, nao so o texto dela.

    Procurar o literal `"  USOS POR TEXTO..."` dentro das funcoes devolve
    lista VAZIA — ele mora na constante —, e ai o assert reprovaria por achar
    NADA em vez de por achar dois donos: teste que detecta por literal aprova
    qualquer coisa quando o literal se move (22/10, 21:4x).
    """
    arv = ast.parse(_fonte())
    donos = [n.name for n in ast.walk(arv)
             if isinstance(n, ast.FunctionDef)
             and ("_PRE_CONC" in ast.unparse(n)
                  or PM._PRE_CONC in ast.unparse(n))]
    assert donos == ["_linha_da_concentracao"], donos


def test_a_frase_sai_nos_DOIS_ramos_e_o_ramo_errado_nao_dispara(escolhas):
    com, sem = [], []
    for c, e in escolhas.items():
        s = PM._linha_da_concentracao(e)
        assert s.startswith(PM._PRE_CONC), (c, s[:60])
        assert "NOMEIA e NAO decide" in s, c
        ls = PM.concentracao_da_escolha(e)["leituras"]
        if any(x and x["e_o_maximo_do_canal"] for x in ls.values()):
            assert "MAIS USADA do canal" in s, c
            assert "o vao decide sozinho" not in s, c
            com.append(c)
        else:
            assert "o vao decide sozinho" in s, c
            assert "MAIS USADA do canal" not in s, c
            sem.append(c)
    assert com and sem, (com, sem)


def test_sem_escolha_ela_DIZ_que_nao_cruzou_em_vez_de_calar():
    e = {"quadro": [], "compartilhados": {}, "usos_por_pacote": {},
         "escolhida": None, "escolhida_por_reserva_sem_declaracao": None}
    s = PM._linha_da_concentracao(e)
    assert s.startswith(PM._PRE_CONC)
    assert "ausencia de cruzamento nao e ausencia de concentracao" in s, s


# -------------------------------------------------------------- a disciplina

def test_a_soma_e_DELEGADA_por_AST():
    """Refazer a soma aqui criaria o segundo dono de `usos_por_pacote`."""
    f = _func("usos_por_texto")
    # O docstring CITA `_compartilhados` para EXPLICAR o defeito, logo casar a
    # prosa pegaria a explicacao em vez do codigo — a licao do
    # `test_NAO_virou_portao` do acento.
    corpo_sem_prosa = list(f.body)
    if corpo_sem_prosa and isinstance(corpo_sem_prosa[0], ast.Expr) \
            and isinstance(corpo_sem_prosa[0].value, ast.Constant):
        corpo_sem_prosa = corpo_sem_prosa[1:]
    corpo = "\n".join(ast.unparse(x) for x in corpo_sem_prosa)
    for proibido in ("_compartilhados", "sum(", "CO.contagem",
                     "nao_mencionados", "glob", "open("):
        assert proibido not in corpo, proibido
    assert "usos_por_pacote" in corpo


def test_o_relato_a_CHAMA_fora_do_ramo_da_escolhida():
    """Dentro do ramo ela sairia so quando ha origem escolhida — e sem
    escolha o cruzamento e justamente o que importa (20/10, 13:2x)."""
    rel = _func("relato")
    dentro_de_if = set()
    for n in ast.walk(rel):
        if isinstance(n, ast.If):
            for f in list(n.body) + list(n.orelse):
                for m in ast.walk(f):
                    if isinstance(m, ast.Call) and "_linha_da_concentracao" \
                            in ast.unparse(m.func):
                        dentro_de_if.add(ast.unparse(m))
    todas = [ast.unparse(m) for m in ast.walk(rel)
             if isinstance(m, ast.Call)
             and "_linha_da_concentracao" in ast.unparse(m.func)]
    assert todas, "o `relato` nao chama a frase: import sem chamada e a " \
                  "classe dos layouts mortos"
    assert not dentro_de_if, dentro_de_if


def test_o_motivo_e_a_medida_continuam_escritos():
    f = _fonte()
    for marca in ("11:3x", "usos_por_pacote", "NOMEIA e NAO decide",
                  "concentracao.py"):
        assert marca in f, marca
