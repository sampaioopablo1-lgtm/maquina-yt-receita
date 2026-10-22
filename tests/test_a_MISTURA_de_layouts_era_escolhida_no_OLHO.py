# -*- coding: utf-8 -*-
"""A MISTURA de layouts era escolhida no OLHO — 22/10 as 19:3x.

O `formas_livres` (22/10, 03:3x) conta as ordens livres de uma mistura DADA, e
o `formas_usadas_do_tamanho` (16:3x) lista as formas usadas de um tamanho.
Entre os dois faltava a pergunta que a rodada faz primeiro: **qual MISTURA de
layouts escolher.** Eu a respondia contando layouts com os dedos.

**E o passo no olho ja errou DUAS vezes:** em 21/10 as 23:2x e em 22/10 as
14:4x a forma que eu compus a mao JA EXISTIA. Nesta rodada ela saiu inedita,
logo aqui o defeito era LATENTE — e isso vai dito em vez de inflado.

A FORMA DOS TESTES, e e ela que vale:
  * a varredura sai do DISCO e reprova por VACUIDADE;
  * toda mistura devolvida e DERIVADA do disco, nunca inventada;
  * as duas contas da MESMA coisa tem de concordar (a daqui e a do dono);
  * a delegacao e cobrada por AST nos dois sentidos;
  * os DOIS lados tem de existir (mistura esgotada e mistura com ordem livre),
    e o arquivo **falha se um deles desaparecer** — e ai esta nota se rele;
  * a FRONTEIRA e cobrada: a forma sugerida, gravada, deixa de ser livre e a
    contagem daquela mistura cai em UM;
  * a medida e RECONFERIDA como PROPORCAO e nao como contagem absoluta, porque
    o acervo cresce uma spec por rodada (a licao de 22/10 as 14:4x).
"""
import ast
import collections
import inspect
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import esqueleto_entre_canais as EC   # noqa: E402

PISO_PECAS = 200
PISO_TAMANHOS = 5

# HISTORIA, e nenhum assert depende dela (743/753/761): a mistura que eu
# escolhi a mao em 22/10 as 19:3x tinha 13.848 ordens livres, e a mais rica do
# mesmo tamanho tinha 41.579. Os numeros envelhecem; a propriedade, nao.
ESCOLHA_DE_19H = (("barras", 2), ("cta", 1), ("item", 6),
                  ("lista", 2), ("titulo", 2))


@pytest.fixture(scope="module")
def pecas():
    p = EC.varre()
    assert len(p) >= PISO_PECAS, (
        "varredura com %d peca(s): abaixo de %d este arquivo passa por "
        "VACUIDADE e nao mede nada" % (len(p), PISO_PECAS))
    return p


@pytest.fixture(scope="module")
def tamanhos(pecas):
    t = sorted({p["cenas"] for p in pecas
                if p.get("cenas") and p.get("esqueleto")})
    assert len(t) >= PISO_TAMANHOS, (
        "so %d tamanho(s) de cena no disco — sem variedade de tamanho os "
        "testes de proporcao nao medem nada" % len(t))
    return t


def _fonte(fn):
    # textwrap.dedent, nao inspect.cleandoc: o cleandoc desindenta a linha do
    # `def` e deixa o corpo torto (IndentationError), medido em 22/10 as 08:3x.
    return textwrap.dedent(inspect.getsource(fn))


def _corpo(fn):
    return ast.parse(_fonte(fn)).body[0]


def _nomes_chamados(fn):
    out = set()
    for n in ast.walk(_corpo(fn)):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.add(f.id)
            elif isinstance(f, ast.Attribute):
                out.add(f.attr)
                if isinstance(f.value, ast.Name):
                    out.add("%s.%s" % (f.value.id, f.attr))
    return out


# ---------------------------------------------------------------- derivacao

def test_toda_mistura_devolvida_e_DERIVADA_do_disco(pecas, tamanhos):
    """Mistura inventada seria limiar sem procedencia (§10)."""
    achou = 0
    for c in tamanhos:
        q = EC.misturas_do_tamanho(c, pecas=pecas)
        if not q["usado"]:
            continue
        reais = set()
        for p in pecas:
            if p.get("cenas") == c and p.get("esqueleto"):
                reais.add(EC._mult(p["esqueleto"].split(EC._separador())))
        for m in q["misturas"]:
            assert tuple(m["mult"]) in reais, (
                "em %d cenas o instrumento devolveu a mistura %r, que NENHUMA "
                "peca do disco usa — ela foi inventada" % (c, m["mult"]))
            achou += 1
    assert achou >= PISO_TAMANHOS, (
        "so %d mistura(s) conferida(s): vacuidade" % achou)


def test_o_tamanho_INEDITO_RECUSA_em_vez_de_inventar(pecas, tamanhos):
    livre = max(tamanhos) + 7
    assert livre not in tamanhos
    q = EC.sugere_forma(livre, pecas=pecas)
    assert q["usado"] is False
    assert q["n_misturas"] == 0
    assert q.get("sugerida") is None, (
        "sem peca no tamanho nao ha de onde DERIVAR a mistura, e sugerir uma "
        "seria inventar")
    assert q.get("motivo"), "recusa sem motivo manda conferir no lugar errado"


# ------------------------------------------------------- as duas contas batem

def test_as_DUAS_contas_da_mesma_coisa_CONCORDAM(pecas, tamanhos):
    """A contagem daqui e a do dono (`formas_livres`) tem de ser a mesma."""
    conferidas = 0
    for c in tamanhos:
        q = EC.misturas_do_tamanho(c, pecas=pecas)
        for m in q["misturas"]:
            r = EC.formas_livres(c, m["layouts"], pecas=pecas)
            assert m["possiveis"] == r.get("possiveis", 0), (
                "em %d cenas, mistura %r: possiveis %r aqui contra %r no dono"
                % (c, m["mult"], m["possiveis"], r.get("possiveis")))
            assert m["livres"] == r.get("livres", 0), (
                "em %d cenas, mistura %r: livres %r aqui contra %r no dono"
                % (c, m["mult"], m["livres"], r.get("livres")))
            conferidas += 1
    assert conferidas >= PISO_TAMANHOS


def test_a_conta_e_DELEGADA_e_a_varredura_tambem_por_AST():
    for fn in (EC.misturas_do_tamanho, EC.sugere_forma):
        chamados = _nomes_chamados(fn)
        assert "formas_livres" in chamados, (
            "%s nao chama o DONO da contagem — recontar o multinomial aqui "
            "seria o segundo dono da conta" % fn.__name__)
        for proibido in ("_multinomial", "factorial", "permutations",
                         "glob", "listdir", "open"):
            assert proibido not in chamados, (
                "%s chama %r: a conta e a varredura tem dono, e refaze-las "
                "aqui reconstroi o defeito de dois donos"
                % (fn.__name__, proibido))


def test_o_relato_CHAMA_a_linha_e_ela_tem_UM_dono():
    assert "_linha_das_misturas" in _nomes_chamados(EC.relato), (
        "import sem chamada e a classe dos layouts mortos: o relato tem de "
        "CHAMAR a linha")
    fonte = _fonte(EC)
    marca = "MISTURA em %d cenas"
    assert fonte.count(marca) == 2, (
        "a frase tem de ter UM dono e sair nos DOIS ramos (tamanho usado e "
        "tamanho inedito) — %d ocorrencia(s)" % fonte.count(marca))
    dono = _fonte(EC._linha_das_misturas)
    assert dono.count(marca) == 2, "as duas ocorrencias moram no dono"


# ------------------------------------------------------------- os dois lados

def test_os_DOIS_lados_existem_no_disco(pecas, tamanhos):
    """Mistura ESGOTADA e mistura com ordem livre. Se um lado desaparecer,
    esta nota se rele em vez de o numero ser movido."""
    tot = esg = 0
    for c in tamanhos:
        q = EC.misturas_do_tamanho(c, pecas=pecas)
        tot += q["n_misturas"]
        esg += q["n_esgotadas"]
    assert tot >= 10, "so %d mistura(s) na frota: vacuidade" % tot
    assert esg > 0, (
        "NENHUMA mistura esgotada no disco: a recusa do `sugere_forma` perde o "
        "objeto e esta nota tem de ser relida")
    assert esg < tot, (
        "TODAS as %d misturas esgotadas: ai nao existe forma livre em lugar "
        "nenhum e o instrumento nao serve para escolher" % tot)
    frac = esg / float(tot)
    assert 0.03 <= frac <= 0.50, (
        "fracao de misturas esgotadas em %.3f (%d de %d), fora da faixa "
        "OBSERVADA — RELEIA a nota em vez de mover o numero. A medida e "
        "PROPORCAO e nao contagem porque o acervo cresce uma spec por rodada "
        "(22/10, 14:4x)" % (frac, esg, tot))


def test_a_mistura_mais_RICA_nao_e_a_mais_USADA(pecas, tamanhos):
    """E a medida do passo no olho: escolher pelo habito nao e escolher onde
    ha espaco. Os DOIS lados tem de existir."""
    divergem = coincidem = 0
    for c in tamanhos:
        q = EC.misturas_do_tamanho(c, pecas=pecas)
        if q["n_misturas"] < 2:
            continue
        rica = q["misturas"][0]
        usada = max(q["misturas"], key=lambda m: m["n_pecas"])
        if tuple(rica["mult"]) == tuple(usada["mult"]):
            coincidem += 1
        else:
            divergem += 1
    assert divergem + coincidem >= 4, "poucos tamanhos com 2+ misturas"
    assert divergem > 0, (
        "a mistura mais rica coincide com a mais usada em TODOS os tamanhos: "
        "ai o passo no olho nao custava nada e esta nota se rele")
    assert coincidem > 0, (
        "elas NUNCA coincidem: sem o lado contrario a propriedade nao "
        "distingue nada")


# ---------------------------------------------------------------- a sugestao

def test_a_forma_sugerida_e_de_fato_LIVRE(pecas, tamanhos):
    testados = 0
    sep = EC._separador()
    for c in tamanhos:
        s = EC.sugere_forma(c, pecas=pecas)
        if not s.get("sugerida"):
            continue
        esq = s["sugerida"]
        lay = [x for x in esq.split(sep) if x]
        assert len(lay) == c, (
            "forma sugerida com %d layout(s) para %d cenas" % (len(lay), c))
        a, z = EC.PONTAS_MEDIDAS
        assert lay[0] == a and lay[-1] == z, (
            "a convencao MEDIDA das pontas e %r/%r e a sugestao e %r"
            % (a, z, esq))
        usadas = {p["esqueleto"] for p in pecas if p.get("cenas") == c}
        assert esq not in usadas, (
            "a forma sugerida em %d cenas JA EXISTE no disco: e exatamente o "
            "defeito que o instrumento existe para nao cometer" % c)
        assert EC._mult(lay) == tuple(s["mistura"]["mult"]), (
            "a sugestao nao e da mistura que ela diz ter escolhido")
        testados += 1
    assert testados >= PISO_TAMANHOS


def test_ela_sai_da_mistura_de_MAIOR_livres_e_nao_da_primeira(pecas, tamanhos):
    for c in tamanhos:
        s = EC.sugere_forma(c, pecas=pecas)
        vivas = [m for m in s["misturas"] if not m["esgotado"]]
        if not vivas or not s.get("mistura"):
            continue
        melhor = max(m["livres"] for m in vivas)
        assert s["mistura"]["livres"] == melhor, (
            "em %d cenas ele escolheu uma mistura com %d livres havendo uma "
            "com %d — ele tem de escolher onde mais sobra ordem"
            % (c, s["mistura"]["livres"], melhor))


def test_a_FRONTEIRA_a_forma_sugerida_gravada_deixa_de_ser_livre(pecas):
    alvo = None
    for c in sorted({p["cenas"] for p in pecas if p.get("cenas")}):
        s = EC.sugere_forma(c, pecas=pecas)
        if s.get("sugerida"):
            alvo = (c, s)
            break
    assert alvo, "nenhum tamanho do disco devolveu sugestao: perdi a ancora"
    c, s = alvo
    antes = s["mistura"]["livres"]
    nova = list(pecas) + [{"arquivo": "__fronteira__.json",
                           "pacote": "__fronteira__",
                           "canal": "canal-de-teste",
                           "cenas": c,
                           "esqueleto": s["sugerida"]}]
    s2 = EC.sugere_forma(c, pecas=nova)
    igual = [m for m in s2["misturas"]
             if tuple(m["mult"]) == tuple(s["mistura"]["mult"])]
    assert igual, "a mistura desapareceu depois de gravar a forma"
    assert igual[0]["livres"] == antes - 1, (
        "livres foi de %d para %d: gravar UMA forma tem de tirar exatamente "
        "UMA da contagem" % (antes, igual[0]["livres"]))
    assert s2.get("sugerida") != s["sugerida"], (
        "ele sugeriu outra vez a forma que acabou de ser gravada")


# ------------------------------------------------------------------- exceto

def test_o_exceto_vai_nos_DOIS_sentidos(pecas):
    """Contraprova: sem ele a peca da rodada se conta contra si mesma; e
    `exceto` que nao casa com nada nao pode filtrar nada."""
    alvo = None
    cont = collections.Counter(
        (p["cenas"], p["esqueleto"]) for p in pecas
        if p.get("cenas") and p.get("esqueleto"))
    for p in pecas:
        k = (p.get("cenas"), p.get("esqueleto"))
        if p.get("cenas") and p.get("esqueleto") and cont[k] == 1:
            alvo = p
            break
    assert alvo, ("nenhuma peca do disco e o unico exemplar da propria forma: "
                  "perdi a ancora")
    c = alvo["cenas"]
    # O registro do `varre` traz `arquivo`, nao `pacote` — e o `exceto` e
    # normalizado pelo `nome_da_spec`, dono das duas convencoes (20/10, 11:3x),
    # logo qualquer das duas formas serve e e a ASSINATURA que decide.
    com = EC.misturas_do_tamanho(c, pecas=pecas, exceto=alvo["arquivo"])
    sem_ = EC.misturas_do_tamanho(c, pecas=pecas)
    chave = EC._mult(alvo["esqueleto"].split(EC._separador()))
    a = [m for m in com["misturas"] if tuple(m["mult"]) == tuple(chave)]
    b = [m for m in sem_["misturas"] if tuple(m["mult"]) == tuple(chave)]
    assert b, "a mistura da ancora nao aparece sem `exceto`"
    if a:
        assert a[0]["livres"] == b[0]["livres"] + 1, (
            "com `exceto` a forma da propria peca tem de voltar a contar como "
            "LIVRE: %d contra %d" % (a[0]["livres"], b[0]["livres"]))
    nada = EC.misturas_do_tamanho(
        c, pecas=pecas, exceto="pacote-que-nao-existe-em-lugar-nenhum")
    assert [m["livres"] for m in nada["misturas"]] == \
           [m["livres"] for m in sem_["misturas"]], (
        "`exceto` que nao casa com nada filtrou alguma coisa")


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = EC.misturas_do_tamanho.__doc__ or ""
    for pedaco in ("no olho", "LATENTE", "54", "NOVE", "porta1"):
        assert pedaco in doc, (
            "o docstring perdeu %r: conserto sem motivo escrito volta calado"
            % pedaco)
