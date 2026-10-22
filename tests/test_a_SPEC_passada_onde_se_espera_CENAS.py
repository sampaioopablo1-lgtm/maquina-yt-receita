"""A SPEC passada onde se espera a lista de CENAS — e o erro saia de TIPO.

**O defeito e de 22/10 as 09:3x e foi meu, nesta rodada:** eu chamei
`ensaio.duracao_real_prevista(sp, voz, 'edge')` com a SPEC na posicao de `cenas`
e levei `AttributeError: 'str' object has no attribute 'get'` apontando
`ensaio.py:234` — uma linha de um modulo que o chamador nunca tocou. Erro de
TIPO manda conferir no lugar errado, que e a licao de 22/10 as 04:4x.

**O que este arquivo NAO cobra:** que a falha fosse permissiva. Ela e RUIDOSA
hoje e isso vai medido em vez de inflado — as doze formas LEVANTAM. O que o
guarda muda e o ENDERECO do motivo, e e isso que esta cobrado.
"""
import ast
import inspect
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import acento  # noqa: E402
import autor  # noqa: E402
import cadencia_longo  # noqa: E402
import cenas_da_spec as CS  # noqa: E402
import ensaio  # noqa: E402
import esqueleto_entre_canais as EC  # noqa: E402
import trilho  # noqa: E402
import variedade  # noqa: E402

DIR_SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _spec_de_prova():
    """DERIVADA do disco: a primeira spec de short solto com cenas e voz.

    Nomear um pacote aqui seria identidade onde ha propriedade (743/753/761), e
    o nome muda a cada rodada.
    """
    for f in sorted(os.listdir(DIR_SPECS)):
        if not f.endswith(".json"):
            continue
        try:
            sp = json.load(open(os.path.join(DIR_SPECS, f), encoding="utf-8"))
        except Exception:
            continue
        if (isinstance(sp.get("short"), list) and len(sp["short"]) >= 5
                and sp.get("voz") in ensaio.MODELO_VOZ and not sp.get("longo")):
            return sp
    pytest.fail("perdeu a ANCORA: nenhuma spec de short solto com voz modelada"
                " no disco — sem ela este arquivo passa por vacuidade")


SP = _spec_de_prova()

# As SEIS portas que CHAMAM o guarda. As outras seis chamadas o alcancam por
# dentro (o `duracao_estimada` e o chokepoint de cinco delas), logo o motivo
# nomeia o chokepoint — que e nosso codigo e nao `ensaio.py:234`.
PORTAS_DIRETAS = {
    "ensaio.duracao_estimada", "variedade.esqueleto", "acento.proporcao",
    "autor.chars", "trilho.capitulos_do_longo",
    "esqueleto_entre_canais.formas_livres",
}
VOZ = SP["voz"]

# As doze formas de chamada que eu de fato posso errar, uma por porta de entrada
# publica que recebe `cenas`. A lista sai da medicao de 09:3x; o teste da
# divergencia abaixo a reconta contra o disco, para ela nao envelhecer calada.
CHAMADAS = [
    ("ensaio.duracao_estimada", lambda s: ensaio.duracao_estimada(s, VOZ)),
    ("ensaio.duracao_estimada_short",
     lambda s: ensaio.duracao_estimada_short(s, VOZ)),
    ("ensaio.duracao_real_prevista",
     lambda s: ensaio.duracao_real_prevista(s, VOZ, "edge")),
    ("variedade.esqueleto", lambda s: variedade.esqueleto(s)),
    ("acento.proporcao", lambda s: acento.proporcao(s)),
    ("autor.chars", lambda s: autor.chars(s)),
    ("autor.medir", lambda s: autor.medir(s, VOZ)),
    ("cadencia_longo.cadencia_s", lambda s: cadencia_longo.cadencia_s(s, VOZ)),
    ("cadencia_longo.relato", lambda s: cadencia_longo.relato(s, VOZ)),
    ("trilho.capitulos_do_longo", lambda s: trilho.capitulos_do_longo(s)),
    ("trilho.aplica_no_longo", lambda s: trilho.aplica_no_longo(s)),
    # os layouts acompanham a contagem: o `formas_livres` exige que os dois
    # argumentos descrevam a MESMA peca (guarda dele, de 21/10 as 00:4x)
    ("esqueleto_entre_canais.formas_livres",
     lambda s: EC.formas_livres(
         s, ["titulo"] + ["item"] * (len(SP["short"]) - 2) + ["cta"])),
]


@pytest.mark.parametrize("nome,chamada", CHAMADAS, ids=[c[0] for c in CHAMADAS])
def test_a_spec_na_posicao_de_cenas_RECUSA_com_motivo_de_DADO(nome, chamada):
    """Nenhuma das doze pode aceitar a spec, e nenhuma pode dar erro de TIPO."""
    with pytest.raises(CS.CenasTrocadas) as e:
        chamada(SP)
    m = str(e.value)
    assert "CENAS" in m, "%s: a recusa nao diz o que se espera: %s" % (nome, m)
    assert "spec[" in m, "%s: a recusa nao nomeia o CAMPO a passar: %s" % (nome, m)
    assert any(("%s." % mod) in m for mod in
               ("ensaio", "variedade", "acento", "autor", "trilho",
                "esqueleto_entre_canais")), (
        "%s: a recusa nao nomeia FUNCAO nenhuma da fabrica, logo ela aponta"
        " onde o erro foi DETECTADO e nao o nosso codigo — que e exatamente o"
        " defeito: %s" % (nome, m))
    if nome in PORTAS_DIRETAS:
        assert nome in m, (
            "%s e porta DIRETA e a recusa nao a nomeia: %s" % (nome, m))


# A forma CERTA nao e a mesma em todas: `formas_livres` recebe a CONTAGEM de
# cenas e as outras onze recebem a LISTA. Passar a lista a ela foi a primeira
# versao deste arquivo, e o teste estava errado, nao o modulo.
CERTO = {"esqueleto_entre_canais.formas_livres": lambda sp: len(sp["short"])}


@pytest.mark.parametrize("nome,chamada", CHAMADAS, ids=[c[0] for c in CHAMADAS])
def test_CONTRAPROVA_a_forma_certa_continua_respondendo(nome, chamada):
    """Sem isto, bastaria LEVANTAR sempre para todo o arquivo passar."""
    r = chamada(CERTO.get(nome, lambda sp: sp["short"])(SP))
    assert r is not None


def test_a_DIVERGENCIA_que_torna_o_engano_facil_e_RECONFERIDA():
    """55 funcoes recebem `spec` e 14 recebem `cenas` — recontado por AST.

    Numero medido que ninguem reconfere envelhece calado (753). E se a frota
    convergir para UMA convencao, o guarda perde o objeto e esta nota se rele.
    """
    por_spec = por_cenas = 0
    d = os.path.join(RAIZ, "fabrica")
    for f in sorted(os.listdir(d)):
        if not f.endswith(".py"):
            continue
        try:
            t = ast.parse(open(os.path.join(d, f), encoding="utf-8").read())
        except SyntaxError:
            continue
        for n in t.body:
            if not isinstance(n, ast.FunctionDef) or n.name.startswith("_"):
                continue
            args = [a.arg for a in n.args.args]
            if not args:
                continue
            if args[0] == "cenas":
                por_cenas += 1
            elif args[0] in ("spec", "sp", "spec_ou_caminho", "sp_ou_caminho"):
                por_spec += 1
    assert por_cenas >= 10, (
        "as funcoes que recebem `cenas` cairam para %d: se a frota convergiu"
        " para `spec`, o guarda perdeu o objeto e a nota de 09:3x se rele"
        % por_cenas)
    assert por_spec > por_cenas * 2, (
        "a divergencia encolheu (%d por spec contra %d por cenas): era a"
        " MAIORIA por spec que tornava o engano facil" % (por_spec, por_cenas))


def test_o_guarda_NAO_aceita_as_duas_formas():
    """Extrair `spec["short"]` daria ao argumento um SEGUNDO significado.

    E a assinatura do `exceto` de 20/10 as 11:3x — o mesmo nome com duas
    convencoes em modulos irmaos, que falhava em silencio nos dois sentidos.
    """
    with pytest.raises(CS.CenasTrocadas):
        CS.exige(SP, "x")
    fonte = inspect.getsource(CS.exige) + inspect.getsource(CS.parece_spec)
    arvore = ast.parse(__import__("textwrap").dedent(
        inspect.getsource(CS.exige)))
    for n in ast.walk(arvore):
        if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                and n.value.id == "cenas"):
            pytest.fail(
                "o guarda indexa a ENTRADA: aceitar a spec e extrair o campo e"
                " o SEGUNDO significado que ele existe para proibir")
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "get" and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "cenas"
                and not isinstance(getattr(n, "parent", None), ast.BoolOp)):
            # `cenas.get(c)` aqui so TESTA o campo, nunca o devolve — a prova
            # e o `Subscript` acima e o retorno medido no teste de cima.
            pass
    assert "short" not in fonte.split('"""')[-1], (
        "o nome do campo so pode aparecer na MENSAGEM e em CAMPOS, nunca como"
        " extracao")


def test_dicionario_SEM_campo_de_cenas_tambem_RECUSA_e_com_outro_motivo():
    """Dizer 'nao e spec' sobre ele mandaria procurar outro defeito.

    E o discriminador e o TIPO e nao a presenca do campo — contraprova no outro
    sentido logo abaixo.
    """
    with pytest.raises(CS.CenasTrocadas) as e:
        CS.exige({"nada": 1}, "x")
    assert "nenhum dos campos" in str(e.value)
    with pytest.raises(CS.CenasTrocadas) as e2:
        CS.exige(SP, "x")
    assert "nenhum dos campos" not in str(e2.value), (
        "os dois motivos colapsaram: spec e dicionario-qualquer pedem"
        " conferencias diferentes"
    )


def test_CONTRAPROVA_o_que_NAO_e_dicionario_passa_intocado():
    """Lista, tupla e vazio nao sao a spec, e o guarda nao pode se meter."""
    for v in ([], [{"nar": "x"}], (), 11, None, "x"):
        assert CS.exige(v, "x") == v or CS.exige(v, "x") is v


def test_o_ramo_PERMISSIVO_existe_e_a_concordancia_foi_ACIDENTE():
    """Funcao que so fizesse `len(cenas)` contaria as CHAVES da spec.

    Na peca de 22/10 as 09:3x `len(spec)` e `len(spec["short"])` valiam os DOIS
    11 — concordancia por acidente, da familia de 22/10 as 01:1x. Nenhuma das
    doze faz isso hoje; este teste guarda o motivo de o guarda existir mesmo
    assim, e **falha se nenhuma spec do disco puder produzir esse acidente**.
    """
    acidentes = 0
    for f in sorted(os.listdir(DIR_SPECS)):
        if not f.endswith(".json"):
            continue
        try:
            sp = json.load(open(os.path.join(DIR_SPECS, f), encoding="utf-8"))
        except Exception:
            continue
        if isinstance(sp.get("short"), list) and len(sp) == len(sp["short"]):
            acidentes += 1
    assert acidentes >= 1, (
        "nenhuma spec do disco tem tantas chaves quanto cenas, logo o acidente"
        " medido em 09:3x nao se reproduz e esta nota se rele"
    )


def test_as_SEIS_portas_CHAMAM_o_dono_por_AST():
    """Guarda importado e nao chamado e a classe dos layouts mortos."""
    portas = [
        ("ensaio.py", "duracao_estimada"),
        ("variedade.py", "esqueleto"),
        ("acento.py", "proporcao"),
        ("autor.py", "chars"),
        ("trilho.py", "capitulos_do_longo"),
        ("esqueleto_entre_canais.py", "formas_livres"),
    ]
    for arq, fn in portas:
        t = ast.parse(open(os.path.join(RAIZ, "fabrica", arq),
                           encoding="utf-8").read())
        n = next((x for x in t.body
                  if isinstance(x, ast.FunctionDef) and x.name == fn), None)
        assert n is not None, "%s: %s desapareceu" % (arq, fn)
        achou = any(isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute)
                    and c.func.attr == "exige"
                    for c in ast.walk(n))
        assert achou, (
            "%s:%s nao chama o guarda — e a porta por onde a spec entra sem"
            " motivo de DADO" % (arq, fn))


def test_o_motivo_e_a_MEDIDA_continuam_escritos_no_dono():
    fonte = open(os.path.join(RAIZ, "fabrica", "cenas_da_spec.py"),
                 encoding="utf-8").read()
    for marca in ("09:3x", "ensaio.py:234", "RUIDOSA", "ACIDENTE"):
        assert marca in fonte, (
            "o dono perdeu %r: conserto sem motivo escrito volta calado" % marca)
