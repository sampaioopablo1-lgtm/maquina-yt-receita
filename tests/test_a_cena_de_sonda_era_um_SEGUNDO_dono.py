# -*- coding: utf-8 -*-
"""A CENA DE SONDA ERA UM SEGUNDO DONO DO CONTRATO DO RENDER — 22/10, 02:5x.

O `layouts_do_short.desenham()` SONDA o render para saber que layouts desenham,
e a cena que ele entregava a sonda era um dicionario ESCRITO A MAO. Logo *"que
campos cada layout consome"* tinha DOIS donos — o render e aquele dicionario — e
eles ja divergiam: campos inventados que nao existem em cena nenhuma do disco, e
campos do disco que faltavam.

E a divergencia LEVANTA: com a cena antiga, `comparar` no 16:9 morre em
`AttributeError`, porque ali `esq`/`dir` eram strings e o layout le dicionario. O
`desenham()` engole a excecao, logo o layout seria reportado como NAO desenhando
e o portao `layout` chamaria CARTAO EM BRANCO uma cena que desenha.

O que estes testes cobram e a PROPRIEDADE: existe UM dono, ele sai do DISCO, a
cena antiga de fato errava, e o conserto NAO mudou o veredito de hoje.
"""
import ast
import glob
import inspect
import io
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import cena_de_sonda as CS  # noqa: E402
import fabrica as F  # noqa: E402
import layouts_do_short as LS  # noqa: E402
import layouts_longo as LL  # noqa: E402

P = dict(LS.PALETA_DE_SONDA)


def _candidatos():
    return sorted(set(LL.LAYOUTS) | LS.candidatos(RAIZ))


def test_a_cena_sai_do_DISCO_e_nao_de_uma_lista():
    """Vacuidade: poucos layouts e varredura quebrada, nao disco pobre."""
    vis = CS.campos_do_disco(RAIZ)
    assert len(vis) >= 8, ("a varredura do disco encolheu para %d layout(s) — "
                           "com tao pouco a sonda nao mede nada" % len(vis))
    for lay, campos in vis.items():
        assert campos, "layout %r sem campo nenhum no disco" % lay


def test_raiz_sem_spec_LEVANTA_em_vez_de_cena_pobre():
    """Cena pobre faz a sonda confundir 'nao desenha' com 'faltou o campo'."""
    import tempfile
    vazia = tempfile.mkdtemp(prefix="sonda-vazia-")
    with pytest.raises(SystemExit) as e:
        CS.campos_do_disco(vazia)
    assert "cena pobre" in str(e.value)


def test_a_cena_ANTIGA_de_fato_LEVANTAVA_no_comparar():
    """Sem isto *"eu errei a cena"* seria afirmacao minha, nao medida.

    Reprova se ela parar de levantar: ai a nota tem de ser relida, porque o
    custo que ela descreve deixou de existir.
    """
    c = dict(LS.CENA_DE_SONDA)
    c["layout"] = "comparar"
    with pytest.raises(AttributeError):
        F.svg_cena(c, P, 1920, 1080)


def test_a_cena_DERIVADA_nao_levanta_em_layout_nenhum():
    """Nos DOIS renders, porque o despacho e diferente em cada um."""
    for lay in _candidatos():
        c = CS.cena(lay, RAIZ)
        F.svg_cena(c, P, 1920, 1080)
        F.svg_cena_retrato(c, P, 1080, 1920)


def test_o_comparar_passa_a_DESENHAR_no_16_9():
    """O caso que levantava: ele desenha, e com conteudo dos dois lados."""
    c = CS.cena("comparar", RAIZ)
    svg = F.svg_cena(c, P, 1920, 1080)
    assert svg.count("<text") >= 8, svg.count("<text")


def test_CONTRAPROVA_o_veredito_do_retrato_NAO_muda():
    """O buraco era LATENTE, e isso vai medido em vez de afirmado.

    Se o conserto mudasse o conjunto que o portao usa, ele seria mudanca de
    comportamento de portao e nao conserto de instrumento.
    """
    com_derivada = set()
    for lay in _candidatos():
        if "<text" in F.svg_cena_retrato(CS.cena(lay, RAIZ), P, 1080, 1920):
            com_derivada.add(lay)
    assert com_derivada == LS.desenham(RAIZ), (
        sorted(com_derivada), sorted(LS.desenham(RAIZ)))


def test_a_divergencia_e_RECONFERIDA_contra_o_disco():
    """753: medida que ninguem reconfere envelhece calada.

    Cobra PROPRIEDADE e nao os numeros: campo inventado e campo que nao existe
    em cena nenhuma, e os dois lados tem de existir — se a divergencia zerar, a
    nota se rele em vez de ficar.
    """
    d = CS.divergencia(LS.CENA_DE_SONDA, RAIZ)
    vis = CS.campos_do_disco(RAIZ)
    no_disco = set()
    for lay in vis:
        no_disco |= set(vis[lay])
    assert d["no_disco"] == len(no_disco)
    assert d["inventados"], "a cena antiga nao tem mais campo inventado — rele a nota"
    assert d["ausentes"], "a cena antiga nao perde mais campo nenhum — rele a nota"
    for k in d["inventados"]:
        assert k not in no_disco
    for k in d["ausentes"]:
        assert k in no_disco


def test_os_valores_vem_de_cena_REAL_com_a_FORMA_dela():
    """Foi a FORMA errada (`esq` como string) que fez o `comparar` levantar."""
    c = CS.cena("comparar", RAIZ)
    assert isinstance(c["esq"], dict) and isinstance(c["dir"], dict), c["esq"]
    assert c["esq"].get("itens"), c["esq"]
    n = CS.cena("numero", RAIZ)
    assert str(n.get("valor")), n


def test_os_campos_de_COMPORTAMENTO_e_de_REDE_ficam_FORA():
    """E o motivo e MEDIDO: sem eles o `broll` continua desenhando."""
    for lay in _candidatos():
        c = CS.cena(lay, RAIZ)
        for k in CS.COMPORTAMENTO + CS.SEM_REDE:
            assert k not in c, (lay, k)
    assert "<text" in F.svg_cena(CS.cena("broll", RAIZ), P, 1920, 1080)


def test_o_desenham_CHAMA_o_dono_por_AST():
    """Import sem chamada e a classe dos layouts mortos.

    O ALIAS e resolvido a partir do proprio `import`, porque casar o nome do
    modulo dentro da chamada pegaria a importacao e nao a chamada — a primeira
    versao deste teste reprovou por isso, e o errado era o teste.
    """
    fonte = inspect.getsource(LS.desenham)
    arvore = ast.parse(fonte.strip())
    aliases = {(n.asname or n.name) for imp in ast.walk(arvore)
               if isinstance(imp, ast.Import) for n in imp.names
               if n.name == "cena_de_sonda"}
    assert aliases, "`desenham` nao importa mais o dono `cena_de_sonda`"
    chamadas = {ast.unparse(n.func) for n in ast.walk(arvore)
                if isinstance(n, ast.Call)}
    assert any("%s.cena" % a in chamadas for a in aliases), (aliases, chamadas)


def test_o_retrato_NAO_remonta_a_cena_por_conta_propria():
    """Montar a cena dentro do `desenham` reconstroi o segundo dono."""
    fonte = io.open(os.path.join(RAIZ, "fabrica", "layouts_do_short.py"),
                    encoding="utf-8").read()
    arvore = ast.parse(fonte)
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == "desenham":
            corpo = ast.unparse(n)
            assert "CENA_DE_SONDA" not in corpo, (
                "o `desenham` voltou a montar a cena a mao — o dono e o "
                "`cena_de_sonda`")


def test_o_LONGO_nao_tem_cartao_em_branco_e_isso_fica_travado():
    """Resultado NEGATIVO da medicao, travado para ninguem o recacar.

    Varridas as specs de longo do disco: zero cenas com layout que o `svg_cena`
    nao desenhe. Reprova por vacuidade com pouca spec, e reprova se aparecer
    cena em branco — ai existe buraco no longo e a nota se rele.
    """
    bons = set()
    for lay in _candidatos():
        if "<text" in F.svg_cena(CS.cena(lay, RAIZ), P, 1920, 1080):
            bons.add(lay)
    specs, cenas, brancas = 0, 0, []
    for caminho in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
        try:
            with open(caminho, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        L = sp.get("longo") or []
        if len(L) < 20:
            continue
        specs += 1
        for i, c in enumerate(L):
            cenas += 1
            lay = ((c or {}).get("layout") or "titulo")
            if lay not in bons:
                brancas.append((os.path.basename(caminho), i, lay))
    assert specs >= 50, "so %d spec(s) de longo — a varredura quebrou" % specs
    assert cenas >= 2000, cenas
    assert not brancas, brancas[:5]
