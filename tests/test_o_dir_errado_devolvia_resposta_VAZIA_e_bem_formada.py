"""O `dir_specs` errado devolvia resposta VAZIA e BEM FORMADA.

Medido em 20/10 as 12:3x, escrevendo o `epomeno-epipedo-s075`. Eu chamei
`segundo_angulo.nao_mencionados('9Hg5A3H1Qe4', 'epomeno-epipedo')` passando o
CANAL na posicao do `dir_specs`, e a funcao devolveu

    {'pacote': None, 'n_capitulos': 0, 'shorts': [], 'nao_mencionados': []}

As cinco funcoes do modulo varrem com `glob.glob(os.path.join(dir_specs,
'*.json'))`, e `glob` de caminho inexistente devolve `[]` sem levantar.

**E o que torna isto pior que o 000 do `curl`: o vazio e CAMUFLADO por um estado
LEGITIMO que o proprio modulo reporta.** `pacote: None` significa, pelo
docstring do `pacote_do_id`, "a convencao nao foi seguida" — origem sem spec
local, que e a regra (h) e acontece de verdade. Logo "diretorio errado" e
"origem sem spec local" eram INDISTINGUIVEIS pela saida.

E a familia e a mesma de sempre, agora com o sexto membro: instrumento que
devolve VAZIO nao prova ausencia (17/10), arquivo vazio nao prova morte (19/10),
instrumento CHEIO nao prova presenca (20/10 01:4x), 000 nao diz de QUEM e o zero
(09:3x), 000 em todo host nao separa rede de POLITICA (11:4x) — e agora **vazio
camuflado por um estado legitimo do proprio instrumento.**

Conserto: `_dir_valido` LEVANTA com o motivo, do jeito que o `porta1` recusa
janela curta.
"""

import ast
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAB = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FAB, "segundo_angulo.py")
sys.path.insert(0, FAB)

import segundo_angulo as SA  # noqa: E402


def _uma_origem_resolvida():
    """Uma origem do DISCO que resolve para pacote — derivada, nao nomeada.

    Nomear um id seria identidade onde ha propriedade (743/753/761): a origem
    escolhida muda com a pauta, e consumir pauta e o trabalho (18/10 09:2x).
    """
    for p in sorted(os.listdir(os.path.join(FAB, "specs"))):
        if not p.endswith(".json"):
            continue
        import json
        try:
            sp = json.load(open(os.path.join(FAB, "specs", p), encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        oid = sp.get("longo_existente")
        if not oid:
            continue
        r = SA.nao_mencionados(oid)
        if r["pacote"] and r["n_capitulos"] > 0:
            return oid, r
    pytest.fail("nenhuma origem do disco resolve para pacote com capitulos — "
                "sem ela este arquivo nao mede nada")


def test_a_varredura_nao_e_vacua():
    n = len([p for p in os.listdir(os.path.join(FAB, "specs"))
             if p.endswith(".json")])
    assert n >= 200, (
        "menos de 200 specs no disco: a varredura encolheu e os testes abaixo "
        "passariam por vacuidade (n=%d)" % n)


def test_o_dir_ERRADO_agora_LEVANTA():
    oid, _ = _uma_origem_resolvida()
    with pytest.raises(ValueError) as e:
        SA.nao_mencionados(oid, "epomeno-epipedo")
    assert "dir_specs" in str(e.value)


def test_contraprova_o_dir_CERTO_continua_respondendo():
    """Sem esta, bastaria levantar sempre para o arquivo passar."""
    oid, r = _uma_origem_resolvida()
    assert r["pacote"] and r["n_capitulos"] > 0
    igual = SA.nao_mencionados(oid, os.path.join(FAB, "specs"))
    assert igual["n_capitulos"] == r["n_capitulos"]
    assert igual["pacote"] == r["pacote"]


def test_o_estado_LEGITIMO_de_origem_sem_spec_SOBREVIVE():
    """A camuflagem era este estado — e ele NAO pode ter desaparecido.

    Origem que nao resolve para pacote continua devolvendo `pacote: None` com
    listas vazias, porque isso e a regra (h) e nao e defeito. Se este ramo
    sumisse, o conserto teria trocado uma cegueira por outra.
    """
    r = SA.nao_mencionados("id-que-nenhuma-spec-declara-99999")
    assert r["pacote"] is None
    assert r["n_capitulos"] == 0
    assert r["nao_mencionados"] == [] and r["mencionados"] == []
    assert r["shorts"] == []


def test_os_DOIS_vazios_eram_indistinguiveis_ANTES():
    """A medicao que sustenta a nota: as duas saidas eram iguais.

    Reproduzida sem o dono, com a varredura crua — e se ela deixar de bater,
    esta nota perde o objeto e se rele.
    """
    import glob
    assert glob.glob(os.path.join("epomeno-epipedo", "*.json")) == []
    assert glob.glob(os.path.join(FAB, "specs", "*.json")) != []


def test_o_dono_tem_UM_lugar_por_AST():
    """`os.path.isdir` do `dir_specs` so dentro do `_dir_valido`."""
    arvore = ast.parse(open(MODULO, encoding="utf-8").read())
    fora = []
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef) or no.name == "_dir_valido":
            continue
        for d in ast.walk(no):
            if (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                    and d.func.attr == "isdir"):
                fora.append(no.name)
    assert not fora, "conferencia de diretorio fora do dono: %s" % fora


def test_as_portas_PUBLICAS_chamam_o_dono_por_AST():
    """As duas entradas que recebem `dir_specs` de fora."""
    arvore = ast.parse(open(MODULO, encoding="utf-8").read())
    precisam = {"nao_mencionados", "slugs_de_canal"}
    chamam = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef) and no.name in precisam:
            for d in ast.walk(no):
                if (isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
                        and d.func.id == "_dir_valido"):
                    chamam.add(no.name)
    assert chamam == precisam, (precisam - chamam)


def test_a_FAMILIA_dos_cinco_casos_continua_nomeada():
    fonte = open(MODULO, encoding="utf-8").read()
    for marca in ("17/10", "19/10", "01:4x", "09:3x", "CAMUFLADO"):
        assert marca in " ".join(fonte.split()), marca


def test_o_motivo_MEDIDO_continua_escrito():
    fonte = " ".join(open(MODULO, encoding="utf-8").read().split())
    for marca in ("12:3x", "regra (h)", "glob", "VAZIA"):
        assert marca in fonte, (
            "conserto sem o motivo escrito volta calado: falta %r" % marca)
