# -*- coding: utf-8 -*-
"""A ORIGEM PERTO DE ESGOTAR MORAVA SO NA MINHA PROSA.

Medido em 23/10 as 05:4x, na peca que eu acabei de escrever (`labtreinamento-
s114`). A rodada consome a reserva SEM DECLARACAO — nao a crua (22/10 as 17:3x)
— e na origem desta rodada ela estava em **NOVE de 40 livres**: eu li as nove
uma a uma, tomei quatro, e escrevi na copy, em PROSA, *"esta origem esta perto
de esgotar"* e *"quando as duas acima sairem, esta origem acabou"*.

**O fato morava so na prosa, e a decisao saiu de cabeca DUAS vezes:** as 02:07
eu desviei desta origem por esse mesmo numero, e as 05:07 eu segui porque nao
havia empate para onde desviar. Item 3 da §10 — todo numero que eu calculo a
mao vira um erro meu.

O denominador da pergunta e MEDIDO e vem do dono (`irmaos_da_origem.
mediana_declarada`): a reserva sem declaracao encolhe por exatamente o que a
peca seguinte DECLARA. E por isso o veredito e GROSSO (cabe / nao cabe) e nunca
uma contagem de rodadas: a faixa do declarado vai de 1 a 60 porque a forma de
FAIXA infla (`capitulos 66 a 74` conta nove), logo a mediana e um TETO do
consumo e dividir por ela seria falsa precisao.

O que este arquivo cobra, e por que nada aqui e identidade:
  * a mediana e **RECONFERIDA contra o disco** chamando o DONO do parse, e o que
    se cobra e a FAIXA dela e o piso de `n` — nunca uma contagem absoluta, que e
    identidade disfarcada de medida numa populacao que cresce uma spec por
    rodada (a licao de 22/10 as 14:4x);
  * os **DOIS lados** tem de existir no disco, e o arquivo **reprova se TODAS as
    origens couberem ou se NENHUMA couber** — nos dois casos a linha nao ordena
    nada e esta nota tem de ser relida;
  * o buraco do filtro e cobrado como **LATENTE**: `admitidas_sem_nada` e zero
    hoje, e o teste **reprova quando deixar de ser** — porque ai o `servem`
    passa a admitir origem sem nada a escrever e isto se rele;
  * origem SEM spec local **nao e esgotada** (ramo LEGITIMO da regra (h)), com
    contraprova no outro sentido;
  * a FRONTEIRA vai nos dois lados: a mediana exata CABE, um abaixo NAO;
  * a frase tem **UM dono**, sai nos **DOIS** ramos, e o `relato` a chama FORA
    do ramo da `escolhida` — que e o defeito de 20/10 as 13:2x, a nota que
    morava no ramo que para de disparar quando ela importa;
  * a conta e **DELEGADA** por AST nos dois sentidos.
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO     # noqa: E402
import pauta_do_momento as PM     # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")
PISO_SPECS = 50          # guarda de vacuidade: mediana de tres nao e mediana
FAIXA_MEDIANA = (3, 15)  # faixa OBSERVADA, nao a contagem de hoje

# HISTORIA, e nenhum assert depende dela: os ids e os numeros mudam com a pauta,
# e consumir pauta e o trabalho (18/10 as 09:2x).
MEDIDA_DE_05H = {"origem": "POBNoY16wG8", "livres": 40, "sem_declaracao": 9,
                 "consumidos": 4, "mediana_na_hora": 7}


def _fonte(f):
    return textwrap.dedent(inspect.getsource(f))


def _nomes_chamados(f):
    out = set()
    for n in ast.walk(ast.parse(_fonte(f))):
        if isinstance(n, ast.Call):
            alvo = n.func
            if isinstance(alvo, ast.Name):
                out.add(alvo.id)
            elif isinstance(alvo, ast.Attribute):
                out.add(alvo.attr)
                if isinstance(alvo.value, ast.Name):
                    out.add("%s.%s" % (alvo.value.id, alvo.attr))
    return out


@pytest.fixture(scope="module")
def quadros():
    qs = {c: PM.quadro(c) for c in CANAIS}
    total = sum(len(v) for v in qs.values())
    assert total >= 3 * 8, (
        "quadro curto (%d origens nos tres canais): a varredura nao mede nada, "
        "e vazio de instrumento nao prova ausencia (17/10)" % total)
    return qs


def _linha(sd, crua=None, usos=1, origem="x"):
    return {"origem": origem, "usos": usos,
            "reserva": (sd if crua is None else crua),
            "reserva_sem_declaracao": sd, "n_capitulos": 99,
            "pacote": "p", "suspeito_de_outro_canal": False,
            "dono_medido": None, "sem_spec_local": sd is None}


# ---------------------------------------------------------------- a mediana

def test_a_mediana_e_RECONFERIDA_contra_o_disco_pelo_DONO_do_parse():
    """Nao e a contagem de hoje que se cobra: e a faixa e o piso de `n`.

    Contagem absoluta sobre populacao que cresce uma spec por rodada e
    identidade disfarcada de medida — a licao de 22/10 as 14:4x, onde uma
    tolerancia de 15 sobre a contagem saiu do limite por CRESCIMENTO.
    """
    import glob
    import json
    med = IO.mediana_declarada()
    assert med["n"] >= PISO_SPECS, med
    assert FAIXA_MEDIANA[0] <= med["mediana"] <= FAIXA_MEDIANA[1], med
    # recontado aqui chamando o DONO do parse, nao reimplementando-o
    ns = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            sp = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(sp, dict) or sp.get("longo"):
            continue
        n = len(IO._capitulos_declarados(sp.get("copy") or ""))
        if n:
            ns.append(n)
    ns.sort()
    esperado = ns[len(ns) // 2] if len(ns) % 2 else (
        ns[len(ns) // 2 - 1] + ns[len(ns) // 2]) / 2
    assert med["n"] == len(ns) and med["mediana"] == esperado, (med, len(ns),
                                                               esperado)


def test_a_FAIXA_do_declarado_e_LARGA_e_por_isso_o_veredito_e_grosso():
    """Se a faixa encolher para perto da mediana, o quociente passa a informar.

    Enquanto ela for larga, dividir reserva por mediana e falsa precisao — e e
    por isso que `cabe_outra_peca` e booleano e nao uma contagem de rodadas.
    """
    med = IO.mediana_declarada()
    assert med["maximo"] - med["minimo"] > 2 * med["mediana"], med
    assert "infla" in IO.mediana_declarada.__doc__.lower()


def test_varredura_curta_LEVANTA_em_vez_de_devolver_mediana(tmp_path):
    (tmp_path / "a.json").write_text(
        '{"copy": "## FONTES\\ncapitulos 1 a 9"}', encoding="utf-8")
    with pytest.raises(ValueError) as ex:
        IO.mediana_declarada(dir_specs=str(tmp_path))
    assert "piso" in str(ex.value)
    # contraprova no outro sentido: o dir CERTO continua respondendo
    assert IO.mediana_declarada()["n"] >= PISO_SPECS


# ------------------------------------------------------------ a derivacao

def test_a_FRONTEIRA_vai_nos_dois_lados():
    m = IO.mediana_declarada()["mediana"]
    g = PM.esgotamento([_linha(m, origem="cabe"),
                        _linha(m - 1, origem="nao")], mediana=m)
    por = {x["origem"]: x for x in g["linhas"]}
    assert por["cabe"]["cabe_outra_peca"] is True
    assert por["nao"]["cabe_outra_peca"] is False
    assert g["nao_cabe_outra"] == ["nao"]


def test_zero_sem_declaracao_e_ESGOTADA_e_nao_cabe():
    g = PM.esgotamento([_linha(0, crua=40, origem="z")], mediana=7)
    assert g["esgotadas"] == ["z"]
    assert g["linhas"][0]["cabe_outra_peca"] is False
    assert "z" in g["admitidas_sem_nada"]


def test_origem_SEM_spec_local_nao_e_esgotada():
    """Ramo LEGITIMO da regra (h): ali nao se sabe, e nao saber nao e zero."""
    g = PM.esgotamento([_linha(None, crua=0, origem="h")], mediana=7)
    assert g["linhas"][0]["esgotada"] is None
    assert g["linhas"][0]["cabe_outra_peca"] is None
    assert g["esgotadas"] == [] and g["nao_cabe_outra"] == []
    assert g["sem_saber"] == ["h"]
    # contraprova no outro sentido: com numero ela entra num dos dois baldes
    g2 = PM.esgotamento([_linha(0, crua=1, origem="h")], mediana=7)
    assert g2["esgotadas"] == ["h"] and g2["sem_saber"] == []


def test_o_veredito_DEPENDE_da_mediana_medida():
    """Sem ela, nada seria "nao cabe" — contraprova do papel do denominador."""
    linhas = [_linha(4, origem="a"), _linha(9, origem="b")]
    assert PM.esgotamento(linhas, mediana=7)["nao_cabe_outra"] == ["a"]
    assert PM.esgotamento(linhas, mediana=0)["nao_cabe_outra"] == []
    assert PM.esgotamento(linhas, mediana=99)["nao_cabe_outra"] == ["a", "b"]


# ------------------------------------------------------------- sobre o disco

def test_os_DOIS_lados_existem_no_disco(quadros):
    """Reprova se TODAS couberem ou se NENHUMA couber: ai a linha nao ordena."""
    cabe = nao = 0
    for c in CANAIS:
        g = PM.esgotamento(quadros[c])
        for x in g["linhas"]:
            if x["cabe_outra_peca"] is True:
                cabe += 1
            elif x["cabe_outra_peca"] is False:
                nao += 1
    assert cabe > 0, "nenhuma origem da frota cabe outra peca: reler a nota"
    assert nao > 0, ("toda origem da frota cabe outra peca: o esgotamento nao "
                     "ordena nada hoje, e esta nota tem de ser relida em vez "
                     "de o numero ser movido")


def test_o_buraco_do_filtro_e_LATENTE_e_o_teste_reprova_quando_deixar_de_ser(
        quadros):
    """`servem` admite por reserva CRUA; origem crua>0 com ZERO sem declaracao
    entraria e a rodada leria os livres para achar tudo declarado. Hoje sao
    zero — quando nao forem, isto se rele."""
    ativas = []
    for c in CANAIS:
        ativas += PM.esgotamento(quadros[c])["admitidas_sem_nada"]
    assert ativas == [], (
        "o buraco do `servem` deixou de ser LATENTE em %s: a nota de 23/10 as "
        "05:4x tem de ser relida, e o filtro da regra escrita (do "
        "`concentracao.py`) passa a admitir origem sem nada a escrever"
        % ativas)


# ------------------------------------------------------------------ a frase

def test_a_frase_tem_UM_dono():
    fonte = open(os.path.join(RAIZ, "fabrica", "pauta_do_momento.py"),
                 encoding="utf-8").read()
    arv = ast.parse(fonte)
    donos = []
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef):
            if "_PRE_ESG" in textwrap.dedent(ast.unparse(n)):
                donos.append(n.name)
    assert donos == ["_linha_do_esgotamento"], donos


def test_a_frase_sai_nos_DOIS_ramos():
    m = IO.mediana_declarada()["mediana"]
    com = PM._linha_do_esgotamento(
        {"esgotamento": PM.esgotamento([_linha(0, crua=9, origem="z")],
                                       mediana=m)})
    sem = PM._linha_do_esgotamento(
        {"esgotamento": PM.esgotamento([_linha(m + 5, origem="ok")],
                                       mediana=m)})
    assert "ESGOTAMENTO" in com and "ESGOTAMENTO" in sem
    assert "ESGOTADAS" in com and "ESGOTADAS" not in sem
    assert "nao ordena nada" in sem
    assert "LATENTE" in com and "LATENTE" in sem


def test_o_relato_chama_a_frase_FORA_do_ramo_da_escolhida():
    """O defeito de 20/10 as 13:2x: a nota que mora no ramo que cala."""
    arv = ast.parse(_fonte(PM.relato))
    fn = arv.body[0]
    no_topo = any(
        isinstance(s, ast.Expr) and "_linha_do_esgotamento"
        in ast.unparse(s) for s in fn.body)
    assert no_topo, ("o `relato` tem de chamar `_linha_do_esgotamento` no "
                     "corpo, nunca dentro de um `if`: sem origem escolhida o "
                     "esgotamento e justamente o que importa")


# ------------------------------------------------------------- a delegacao

def test_a_conta_e_DELEGADA_nos_dois_sentidos():
    chamados = _nomes_chamados(PM.esgotamento)
    assert "mediana_declarada" in chamados, chamados
    for proibido in ("glob", "listdir", "open", "_capitulos_declarados",
                     "load", "finditer"):
        assert proibido not in chamados, (
            "`esgotamento` nao pode %s: ela deriva sobre o quadro que recebe, e "
            "reler o disco aqui seria o segundo dono" % proibido)
    # e o dono da mediana tem de CHAMAR o dono do parse, nao refazer o regex
    donos = _nomes_chamados(IO.mediana_declarada)
    assert "_capitulos_declarados" in donos, donos
    for proibido in ("finditer", "compile", "search"):
        assert proibido not in donos, donos


def test_o_escolha_EXPOE_o_esgotamento(quadros):
    """Derivacao que o chamador nao alcanca e a classe dos layouts mortos."""
    e = PM.escolha(CANAIS[0])
    assert "esgotamento" in e and e["esgotamento"]["linhas"]
    assert "mediana_declarada" in e["esgotamento"]


def test_o_motivo_continua_escrito():
    for texto, marcas in (
            (PM.esgotamento.__doc__, ("prosa", "LATENTE", "NOMEIA")),
            (IO.mediana_declarada.__doc__, ("DELEGADA", "infla", "LEVANTA"))):
        for m in marcas:
            # sem caixa: o que se cobra e o MOTIVO estar escrito, nao como eu o
            # grafei — casar prosa pela caixa foi o que reprovou a primeira
            # versao deste teste, e era o teste errado e nao o modulo.
            assert m.lower() in texto.lower(), (m, texto[:120])
