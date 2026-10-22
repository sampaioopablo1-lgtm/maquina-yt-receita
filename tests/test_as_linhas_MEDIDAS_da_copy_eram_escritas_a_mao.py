"""As linhas MEDIDAS da copy eram escritas a mao — e envelheciam no corte.

**MEDIDO em 22/10 as 13:4x, e e a SEXTA vez na mesma sessao.** A copy afirma
coisas sobre a PROPRIA peca (numerais falados, previsao em cada mundo, media de
caracteres, ineditismo do esqueleto) e eu as escrevia a mao ANTES de a narracao
estar final. O corte de caracteres entra quase sempre — a previsao tem de cair
na faixa —, logo a afirmacao fica atras.

**E A CONFERENCIA NO OUTRO SENTIDO NAO E VIAVEL, e este arquivo trava a
MEDIDA que mostrou isso:** o `numerais_falados.declaracao_incompleta` cobre o
ramo "a narracao fala e a copy nao cita"; o ramo que falta e o meu defeito, e o
unico sinal mecanico para ele (numeral do idioma entre ASPAS na copy) produz
**4 falsos positivos em 5 achados** — a copy cita o numeral entre aspas para
dizer que ele esta AUSENTE, ou para falar da peca de um IRMAO. O 725 e
explicito, logo a acusacao NAO foi ligada e o que fecha o defeito e a GERACAO.
"""
import ast
import glob
import inspect
import json
import os
import re
import sys
import textwrap
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import linhas_medidas_da_copy as LM  # noqa: E402
import numerais_falados as NF  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
PISO_SPECS = 150
QUOTES = '[«"“”\'‘’]'

# HISTORIA: o unico caso REAL da varredura de 13:4x foi o `labtreinamento-s071`
# (declara "dois" e fala so "tres"). Nenhum assert depende dele — a copy dele
# pode ser corrigida, e ai o teste reprovaria pelo trabalho feito (743/753/761).
CASO_DE_13H = "labtreinamento-s071"


def _fonte(fn) -> ast.AST:
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def _dobra(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def _specs() -> list:
    out = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        out.append(d)
    return out


def test_a_varredura_sai_do_DISCO_e_reprova_por_vacuidade():
    assert len(_specs()) >= PISO_SPECS, (
        "menos de %d specs de short solto: o arquivo passa sem medir nada"
        % PISO_SPECS)


def test_toda_medida_e_DELEGADA_por_AST():
    """Recalcular aqui criaria o segundo dono da medida."""
    fonte = textwrap.dedent(inspect.getsource(LM.medidas))
    corpo = fonte.split('"""')[-1]
    for proibido in ("MODELO_VOZ", "0.300", "+ 0.3", "DIACRITICOS",
                     '"-".join', "glob.", "listdir", "open("):
        assert proibido not in corpo, (
            "o corpo recalcula %r em vez de pedir ao dono" % proibido)
    chamadas = {ast.unparse(n.func) for n in ast.walk(_fonte(LM.medidas))
                if isinstance(n, ast.Call)}
    for dono in ("NF.da_spec", "mira.confere", "V.esqueleto", "AC.proporcao",
                 "EC.novidade"):
        assert any(dono in c for c in chamadas), (
            "nao chama o dono %s — import sem chamada e a classe dos layouts "
            "mortos" % dono)


def test_ele_aceita_RASCUNHO_e_responde_o_MESMO_que_o_disco():
    alvo = None
    for d in _specs():
        p = os.path.join(SPECS, "%s.json" % d["pacote"])
        if os.path.exists(p):
            alvo = (p, d)
            break
    assert alvo, "perdi a ancora: nenhuma spec de short solto no disco"
    p, d = alvo
    a = LM.medidas(p)
    b = LM.medidas(None, d)
    assert a == b, (
        "a resposta pelo dicionario difere da do disco — entao o rascunho "
        "responderia OUTRA coisa, e e no rascunho que a copy se escreve")


def test_a_frase_dos_numerais_tem_UM_dono_e_sai_nos_TRES_ramos():
    assert hasattr(LM, "_linha_dos_numerais")
    chamadas = {ast.unparse(n.func) for n in ast.walk(_fonte(LM.linhas))
                if isinstance(n, ast.Call)}
    assert any("_linha_dos_numerais" in c for c in chamadas)
    fala = LM._linha_dos_numerais(
        {"numerais_sabe_ler": True, "numerais": ["tres"], "idioma": "pt"})
    muda = LM._linha_dos_numerais(
        {"numerais_sabe_ler": True, "numerais": [], "idioma": "pt"})
    naosabe = LM._linha_dos_numerais(
        {"numerais_sabe_ler": False, "numerais": [], "idioma": "xx"})
    assert "tres" in fala
    assert len({fala, muda, naosabe}) == 3, (
        "dois dos tres ramos dizem a mesma coisa")
    assert "nao sabe ler" in naosabe or "NAO sabe ler" in naosabe, (
        "idioma sem vocabulario tem de DIZER que o modulo nao sabe ler, em vez "
        "de afirmar que a narracao nao fala numeral (17/10)")


def test_as_DUAS_faixas_vao_NOMEADAS_e_divergem():
    """"faixa" e o nome de duas coisas no repo: o portao e a mira."""
    alvo = [d for d in _specs() if (d.get("idioma") or "")[:2] == "el"]
    assert alvo, "perdi a ancora: nenhuma spec grega"
    m = LM.medidas(None, alvo[-1])
    assert m["faixa_do_portao"] != m["mira"], (
        "as duas faixas coincidiram — se isso virar regra, a linha perde o "
        "objeto e esta nota se rele")
    linha = [x for x in LM.linhas(None, alvo[-1]) if "PREVISAO" in x]
    assert linha, "a linha da previsao nao saiu"
    assert "PORTAO" in linha[0] and "MIRA" in linha[0], (
        "a linha imprime UMA das duas faixas sem dizer qual — foi assim que a "
        "primeira versao imprimiu a do portao (18 a 45) onde se le mira")


def test_o_acento_NAO_e_multiplicado_duas_vezes():
    """1361%% na primeira execucao: o 753 em forma de UNIDADE."""
    alvo = _specs()[-1]
    m = LM.medidas(None, alvo)
    assert 0.0 <= m["acento"] <= 100.0, (
        "acento fora de 0 a 100 (%r): o `acento.proporcao` JA devolve "
        "percentual" % m["acento"])
    linha = [x for x in LM.linhas(None, alvo) if "REDACAO" in x]
    assert linha and "%" in linha[0]
    num = re.search(r"acento ([\d.]+)%", linha[0])
    assert num and float(num.group(1)) <= 100.0


def test_a_MEDIDA_dos_falsos_positivos_e_RECONFERIDA_contra_o_disco():
    """Numero que ninguem reconfere envelhece calado (753).

    E ele carrega a razao de a acusacao NAO existir: se os falsos positivos
    desaparecerem, o ramo passa a ser viavel e esta nota tem de ser relida.
    """
    reais, falsos = [], []
    for d in _specs():
        idi = ((d.get("idioma") or "")[:2]).lower()
        voc = NF.VOCABULARIO.get(idi)
        if not voc:
            continue
        falados = {_dobra(x) for x in (NF.da_spec(d)["total"] or [])}
        copy = d.get("copy") or ""
        cit = set()
        for m in re.finditer(
                QUOTES + r'\s*([^\s«"“”\'‘’]{1,24})\s*'
                + QUOTES, copy):
            tok = _dobra(m.group(1).strip(".,;:!?"))
            if tok in {_dobra(v) for v in voc}:
                cit.add(tok)
        for c in sorted(cit - falados):
            # o falso positivo tem forma: a copy cita o numeral para dizer que
            # ele esta AUSENTE, ou para falar da peca de um IRMAO
            ctx = " ".join(l for l in copy.splitlines() if c in _dobra(l))
            negado = any(k in _dobra(ctx) for k in
                         ("sem dizer", "nao e", "seria", "falava", "nao diz"))
            (falsos if negado else reais).append((d["pacote"], c))
    assert falsos, (
        "nenhum falso positivo no disco — entao a acusacao por ASPAS passou a "
        "ser viavel e a decisao de NAO a ligar tem de ser relida")
    assert len(falsos) > len(reais), (
        "os falsos positivos (%d) deixaram de ser a MAIORIA dos achados (%d "
        "reais): o 725 era o motivo de nao ligar a acusacao, e ele caiu"
        % (len(falsos), len(reais)))


def test_a_acusacao_por_ASPAS_nao_foi_ligada():
    """Por AST: nenhuma funcao do modulo casa aspas na copy."""
    fonte = inspect.getsource(LM)
    arvore = ast.parse(fonte)
    for n in ast.walk(arvore):
        if isinstance(n, ast.Call) and "finditer" in ast.unparse(n.func):
            raise AssertionError(
                "o modulo passou a casar padrao na copy — a acusacao por aspas "
                "produz 4 falsos em 5 achados (725)")
    assert "declaracao_incompleta" not in fonte.split('"""')[-1], (
        "o modulo nao deve reimplementar nem reaproveitar o ramo do "
        "`numerais_falados`: ele e o dono dele")


def test_o_codigo_de_saida_e_sempre_ZERO():
    """E o `sys.argv` vai posto nos DOIS casos.

    A primeira versao chamou `main()` sem o por, e o `main` leu o argv do
    PYTEST: `JSONDecodeError`. O teste estava errado, nao o modulo — e e a
    familia de 22/10 as 04:4x, onde a forma da chamada e que estava torta.
    """
    guardado = list(sys.argv)
    try:
        sys.argv = ["linhas_medidas_da_copy.py"]
        assert LM.main() == 0
        sys.argv = ["x", os.path.join(SPECS,
                                      "%s.json" % _specs()[-1]["pacote"])]
        assert LM.main() == 0
    finally:
        sys.argv = guardado


def test_o_motivo_continua_escrito_no_modulo():
    doc = LM.__doc__ or ""
    for pedaco in ("285", "725", "SEXTA", "NAO FEITA"):
        assert pedaco in doc, (
            "o motivo (%r) saiu do modulo — conserto sem motivo escrito volta "
            "calado" % pedaco)
