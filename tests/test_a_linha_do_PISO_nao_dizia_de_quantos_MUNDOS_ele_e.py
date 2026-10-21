# -*- coding: utf-8 -*-
"""A linha do PISO nao dizia de quantos MUNDOS ele e — 21/10 as 18:3x.

A linha do MEIO ganhou em 19/10 as 17:2x a ressalva de que a mira cobra os DOIS
mundos de provedor (730/733). A linha do PISO nasceu um dia depois, em 20/10 as
16:4x, chamando o `janela_do_mundo` — UM mundo — e **sem ressalva nenhuma**.
Logo o mesmo relato imprimia dois numeros, um deles reprovado pela propria
`mira.confere`, e nada marcava qual.

Escrevendo o `labtreinamento-s102` eu reconciliei os dois A MAO: o piso dava 25
caracteres por cena, a janela dos dois dava 34 a 36, e eu escrevi a peca em 35
depois de fazer a conta de cabeca — item 3 da §10.

MEDIDO no disco: das specs com orcamento, o piso de UM mundo e reprovado pela
janela dos dois em 115, e em ZERO ele cabe nela. O zero e ARITMETICA numa
direcao: o piper preve MENOS segundos para a mesma media, logo o piso dos dois
e sempre ACIMA do piso de um. As outras 292 tem a pinca do 740/748 FECHADA.
"""
import ast
import glob
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import mira   # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _funcao(nome):
    fonte = open(mira.__file__, encoding="utf-8").read()
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.FunctionDef) and no.name == nome:
            return no
    raise AssertionError("funcao %s nao existe no mira.py" % nome)


def _pares():
    """(nome, spec, piso de UM mundo, janela dos DOIS) para o disco inteiro."""
    saida = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        orc = mira.orcamento(d)
        if not orc or not orc.get("cabe"):
            continue
        um = mira.janela_do_mundo(orc["voz"], orc["cenas"], orc["faixa"],
                                  orc["mundo"])
        saida.append((os.path.basename(f)[:-5], d, um,
                      orc.get("janela_dos_dois")))
    return saida


def test_a_varredura_nao_e_vacua():
    p = _pares()
    assert len(p) >= 100, (
        "so %d specs com orcamento — a varredura ficou vacua e o arquivo "
        "deixaria de medir o defeito" % len(p))


def test_a_medida_do_defeito_e_RECONFERIDA_contra_o_disco():
    """O 753: numero que o modulo cita e reconferido, nao envelhece calado."""
    p = _pares()
    reprovado = [x for x in p if x[2] and x[3] and not (x[3][0] <= x[2][0] <= x[3][1])]
    dentro = [x for x in p if x[2] and x[3] and x[3][0] <= x[2][0] <= x[3][1]]
    pinca = [x for x in p if x[2] and x[3] is None]
    assert len(dentro) == 0, (
        "%d specs com o piso de um mundo DENTRO da janela dos dois — a "
        "aritmetica da direcao caiu e esta nota tem de ser relida" % len(dentro))
    assert len(reprovado) >= 50, (
        "so %d reprovados, contra 115 medidos em 21/10 — se a maioria passou a "
        "caber, esta nota se rele" % len(reprovado))
    assert len(pinca) >= 50, (
        "so %d com a pinca fechada, contra 292 medidos — o outro ramo da "
        "linha deixou de ter caso no disco" % len(pinca))


def test_a_ARITMETICA_da_direcao_vale_em_TODO_par():
    """O piso dos DOIS mundos nunca fica abaixo do piso de UM.

    E o que torna o terceiro ramo da linha inalcancavel no disco, e e por isso
    que a medida de ZERO acima nao e acidente do acervo.
    """
    p = [x for x in _pares() if x[2] and x[3]]
    assert p, "nenhum par com as duas janelas — o teste passaria por vacuidade"
    for nome, _sp, um, jan in p:
        assert jan[0] >= um[0], (
            "%s: piso dos dois (%d) abaixo do piso de um (%d) — a direcao "
            "inverteu" % (nome, jan[0], um[0]))


def test_os_DOIS_lados_existem_no_disco():
    p = _pares()
    abertos = [x for x in p if x[3]]
    fechados = [x for x in p if x[3] is None]
    assert abertos, (
        "nenhuma spec com janela dos dois ABERTA — sem ela o ramo que nomeia "
        "o piso dos dois nunca e exercitado")
    assert fechados, (
        "nenhuma spec com a pinca FECHADA — sem ela o ramo que manda declarar "
        "exposicao nunca e exercitado")


def test_a_linha_do_piso_NOMEIA_o_piso_dos_dois_quando_a_janela_existe():
    p = [x for x in _pares() if x[3] and x[2]
         and not (x[3][0] <= x[2][0] <= x[3][1])]
    assert p, "nenhum caso reprovado — o teste passaria por vacuidade"
    nome, sp, um, jan = p[0]
    linhas = "\n".join(mira._linha_do_piso(sp))
    assert "REPROVA este piso" in linhas, (
        "%s: a linha do piso nao diz que a mira o reprova:\n%s" % (nome, linhas))
    assert str(jan[0]) in linhas, (
        "%s: a linha nao nomeia o piso dos DOIS mundos (%d):\n%s"
        % (nome, jan[0], linhas))
    assert "UM mundo" in linhas, (
        "%s: a linha nao diz de quantos mundos o piso e:\n%s" % (nome, linhas))


def test_com_a_pinca_FECHADA_ela_manda_DECLARAR_a_exposicao():
    p = [x for x in _pares() if x[3] is None and x[2]]
    assert p, "nenhuma spec com a pinca fechada — vacuidade"
    nome, sp, um, _ = p[0]
    linhas = "\n".join(mira._linha_do_piso(sp))
    assert "FECHADA" in linhas, (
        "%s: a pinca nao vai nomeada:\n%s" % (nome, linhas))
    assert "DECLARAR" in linhas, (
        "%s: a linha nao diz que mirar o piso aqui e declarar exposicao:\n%s"
        % (nome, linhas))
    assert "REPROVA este piso" not in linhas, (
        "%s: sem janela dos dois nao existe piso dos dois a reprovar contra — "
        "o ramo errado disparou:\n%s" % (nome, linhas))


def test_a_linha_tem_UM_dono_e_chega_ao_RELATO():
    """Instrumento que o relato nao chama e a classe dos layouts mortos."""
    fonte = open(mira.__file__, encoding="utf-8").read()
    arv = ast.parse(fonte)
    donos = [n.name for n in ast.walk(arv)
             if isinstance(n, ast.FunctionDef)
             and "PISO EXECUTAVEL" in _codigo(n)]
    assert donos == ["_linha_do_piso"], (
        "a frase do piso tem %d donos (%s) — ela precisa de um so"
        % (len(donos), donos))
    chamadores = [n.name for n in ast.walk(arv)
                  if isinstance(n, ast.FunctionDef)
                  and "_linha_do_piso" in _codigo(n)]
    assert "_linha_do_orcamento" in chamadores, (
        "ninguem chama o `_linha_do_piso` — a linha nao chega ao relato")


def test_a_conta_das_janelas_e_DELEGADA():
    """Refazer a varredura de caracteres aqui criaria o segundo dono."""
    codigo = _codigo(_funcao("_linha_do_piso"))
    for proibido in ("range(", "duracao_real_prevista", "chars_por_cena"):
        assert proibido not in codigo, (
            "`_linha_do_piso` refaz a conta com %s — ela tem de delegar ao "
            "`janela_do_mundo` e ao `janela_dos_dois_mundos`" % proibido)
    assert "janela_do_mundo" in codigo, "ela deixou de chamar o dono do piso"


def test_o_relato_INFORMA_e_o_codigo_de_saida_segue_ZERO():
    alvo = os.path.join(SPECS, "labtreinamento-s102.json")
    if not os.path.exists(alvo):
        p = [x for x in _pares() if x[3] and x[2]]
        assert p, "nenhuma spec para a conferencia de ponta a ponta"
        alvo = os.path.join(SPECS, p[0][0] + ".json")
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                        alvo], capture_output=True, text=True)
    assert "PISO EXECUTAVEL" in r.stdout, (
        "a linha do piso nao chega ao relato de ponta a ponta:\n%s" % r.stdout)
    assert r.returncode == 0, (
        "o relato passou a REPROVAR (saida %d) — ele informa, nao reprova"
        % r.returncode)


def test_o_motivo_continua_escrito_no_modulo():
    fonte = open(mira.__file__, encoding="utf-8").read()
    for marca in ("16:4x", "17:2x", "labtreinamento-s102", "115", "292"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo — sem ela a rodada seguinte "
            "reescreve a linha de um mundo so" % marca)
