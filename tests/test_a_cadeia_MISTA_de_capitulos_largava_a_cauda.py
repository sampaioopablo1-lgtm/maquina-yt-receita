# -*- coding: utf-8 -*-
"""A CADEIA que troca de forma no meio largava a cauda — 23/10 as 02:4x.

O `_citados` lia TRES formas de citar capitulo: a FAIXA (`N a M`), o UNICO
(`capitulo N`) e a ENUMERACAO (`N, M e K`, que entrou em 22/10 as 21:4x). A
QUARTA e a cadeia MISTA, que troca de forma no meio — e ela e a forma que a
PROPRIA copy do `labtreinamento-s091` usa: `capitulos 7, 24 e 26 a 30`.

A cadeia parava no primeiro elo que nao fosse virgula ou conjuncao, logo o
`a 30` do fim era largado e os capitulos 27 a 30 contavam como LIVRES.

**O CUSTO FOI MEDIDO NA RODADA EM QUE ELA APARECEU, e nao e de relato:** o
`pauta_do_momento` do `labtreinamento` ofereceu 27, 28, 29 e 30 como livres NAO
declarados, e era de la que eu ia escrever a familia — isto e, de territorio
declarado por irmao. E a mesma assinatura de 22/10 as 12:3x, que me custou duas
cenas do `kolejny-poziom-s093`.

E a faixa GREGA caia pelo outro lado: a forma 1 so conhecia o `a`, logo
`κεφάλαια 47 έως 49` entregava 47 e largava 48 e 49.

**Varrido o disco: 80 capitulos em 21 specs, ZERO regressoes.**

A forma dos testes: a ancora e DERIVADA do disco (nomear a `s091` seria
identidade onde ha propriedade — 743/753/761), o vocabulario da faixa e cobrado
como tendo UM dono e como MEDIDO (vocabulario de zero ocorrencia e o 725), a
contraprova vai nos DOIS sentidos, e a guarda do 725 e cobrada na FRONTEIRA.
"""
import ast
import glob
import io
import json
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402

DIR_SPECS = os.path.join(RAIZ, "fabrica", "specs")
FONTE = io.open(IO.__file__, encoding="utf-8").read()

# HISTORIA: foi esta copy que produziu o achado. NENHUM assert depende dela —
# ela esta aqui para a rodada seguinte saber onde olhar, nao como ancora.
COPY_DE_02H = "labtreinamento-s091"


def _copies():
    fora = []
    for a in sorted(glob.glob(os.path.join(DIR_SPECS, "*.json"))):
        try:
            sp = json.load(io.open(a, encoding="utf-8"))
        except Exception:
            continue
        cop = sp.get("copy") or ""
        if cop:
            fora.append((os.path.basename(a), cop))
    return fora


def _antigo(trecho):
    """O parser de 22/10 as 21:4x, reconstruido para MEDIR o delta.

    Sem ele, "o parser antigo perdia capitulo" seria afirmacao minha e nao
    medida — e um teste que so chama o parser novo passa com o defeito de volta.
    """
    ach = set()
    for m in re.finditer(IO.PALAVRA_CAPITULO + r"\s+(\d{1,3})\s*a\s*(\d{1,3})",
                         trecho, re.I):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b and b - a < 60:
            ach.update(range(a, b + 1))
    for m in re.finditer(IO.PALAVRA_CAPITULO + r"\s+(\d{1,3})\b", trecho, re.I):
        ach.add(int(m.group(1)))
        resto = trecho[m.end():]
        for _ in range(IO.MAX_ENCADEADOS):
            liga = re.match(r"\s*(?:,|;|\be\b|\bi\b|\band\b|\bκαι\b)"
                            r"\s*(\d{1,3})\b", resto, re.I)
            if not liga:
                break
            ach.add(int(liga.group(1)))
            resto = resto[liga.end():]
    return ach


def _fonte_de(fn):
    import inspect
    import textwrap
    return textwrap.dedent(inspect.getsource(fn))


# ---------------------------------------------------------------- vacuidade

def test_a_varredura_nao_passa_por_VACUIDADE():
    """Menos de 150 copies e varredura que nao mede nada (o 743 em forma de glob)."""
    assert len(_copies()) >= 150, (
        "so %d copies no disco: a varredura ficou vazia e os testes abaixo "
        "passariam sem medir nada" % len(_copies()))


# ------------------------------------------------- a QUARTA forma, nos dois

def test_a_cadeia_MISTA_entrega_a_cauda():
    """`N, M e K a P` tem de entregar K..P, e a faixa parte do ULTIMO numero."""
    lido = IO._citados(u"A familia sai dos capitulos\n7, 24 e 26 a 30: ...")
    assert lido == {7, 24, 26, 27, 28, 29, 30}, lido
    # e a faixa NAO parte do primeiro: 8..30 seria ler 23 capitulos alheios
    assert 8 not in lido and 25 not in lido


def test_a_cadeia_INVERSA_tambem_entrega():
    """`N a M e K` — a faixa primeiro, a enumeracao depois."""
    assert IO._citados(u"capitulos 13 a 16 e 60") == {13, 14, 15, 16, 60}


def test_o_parser_ANTIGO_de_fato_LARGAVA_a_cauda():
    """Sem isto, "o antigo perdia" e afirmacao minha. E reprova se ele parar de errar."""
    t = u"capitulos 7, 24 e 26 a 30"
    assert _antigo(t) == {7, 24, 26}, _antigo(t)
    assert IO._citados(t) - _antigo(t) == {27, 28, 29, 30}


def test_o_GANHO_no_disco_e_RECONFERIDO_e_sem_REGRESSAO():
    """A medida nao pode envelhecer calada (753), e regressao e proibida."""
    ganho, specs, regressao = 0, set(), []
    for nome, cop in _copies():
        t = IO._sem_reserva(cop)
        v, n = _antigo(t), IO._citados(t)
        if v - n:
            regressao.append((nome, sorted(v - n)))
        if n - v:
            ganho += len(n - v)
            specs.add(nome)
    assert not regressao, (
        "REGRESSAO: capitulo que o parser antigo lia e o novo nao: %r" % regressao[:3])
    assert ganho >= 40 and len(specs) >= 10, (
        "o ganho medido caiu para %d capitulos em %d specs (era 80 em 21). Se o "
        "ACERVO foi uniformizado, esta nota tem de ser RELIDA, nao o numero "
        "movido." % (ganho, len(specs)))


# ------------------------------------------------- a ancora DERIVADA do disco

def test_a_ancora_do_achado_sai_do_DISCO_e_nao_do_nome():
    """Existe no disco copy com cadeia mista cuja cauda o antigo largava."""
    achadas = []
    for nome, cop in _copies():
        t = IO._sem_reserva(cop)
        if IO._citados(t) - _antigo(t):
            achadas.append(nome)
    assert achadas, (
        "nenhuma copy do disco tem cadeia cuja cauda o parser antigo largava: "
        "o arquivo PERDEU A ANCORA e passa por vacuidade")
    assert COPY_DE_02H + ".json" in achadas or len(achadas) >= 5, achadas


# ------------------------------------------------------- UM dono, e MEDIDO

def test_o_vocabulario_da_faixa_tem_UM_dono():
    """A forma 1 e a cadeia tem de LER o mesmo `FAIXA_ATE`, nunca repeti-lo.

    Se a cadeia soubesse uma palavra que a faixa solta nao sabe, o MESMO texto
    sairia lido num caminho e perdido no outro — e era exatamente isso que
    acontecia com o grego.
    """
    assert hasattr(IO, "FAIXA_ATE")
    src = _fonte_de(IO._citados)
    arvore = ast.parse(src)
    nomes = {n.id for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    assert "FAIXA_ATE" in nomes, "o `_citados` nao LE o dono do vocabulario"
    # e nenhum literal de regex dentro dele pode recravar o vocabulario
    for s in [n.value for n in ast.walk(arvore)
              if isinstance(n, ast.Constant) and isinstance(n.value, str)]:
        assert u"\\s*a\\s*(\\d" not in s, (
            "o vocabulario da faixa voltou cravado dentro do `_citados`: %r" % s)


def test_o_vocabulario_e_MEDIDO_e_nao_suposto():
    """Todo elo de `FAIXA_ATE` tem de OCORRER no disco — zero ocorrencia e o 725.

    `do` e `az`, que eu ia escrever de cabeca, dao ZERO: um vocabulario sem
    ocorrencia nao amplia cobertura, ele amplia o risco de falso positivo.
    """
    elos = [e for e in IO.FAIXA_ATE.strip("(?:)").split("|") if e]
    assert elos, IO.FAIXA_ATE
    corpus = u"\n".join(c for _, c in _copies())
    for elo in elos:
        pat = re.compile(IO.PALAVRA_CAPITULO + r"[\s\d,;ei]{0,40}" + elo
                         + r"\s*\d{1,3}", re.I | re.S)
        assert pat.search(corpus), (
            "o elo %r nao ocorre no acervo: vocabulario sem procedencia e "
            "criterio inventado (725)" % elo)


# --------------------------------------------- contraprova no outro sentido

def test_numero_NU_continua_FORA():
    """Sem a palavra antes, numero nao entra — nem depois de uma cadeia."""
    lido = IO._citados(u"capitulos 30, 31 e 32 a mais disso, 9 por cento ao ano")
    assert lido == {30, 31, 32}, lido


def test_palavra_FORA_do_vocabulario_nao_liga():
    """`do` nao e elo de faixa: se fosse, `capitulo 26 do 30` leria 27 a 30."""
    assert IO._citados(u"capitulo 26 do 30") == {26}


def test_a_FRONTEIRA_do_encadeamento_e_respeitada():
    """O `MAX_ENCADEADOS` conta ELOS, nao numeros — e e cobrado na fronteira.

    A primeira versao deste teste cravou `== n` capitulos para n elos e
    reprovou o modulo CERTO: o numero casado pela palavra nao e elo, logo n
    elos entregam n+1 numeros. **Era o teste errado, nao o modulo** — e a
    propriedade que importa e a PARADA: o elo n+1 nao entra.
    """
    n = IO.MAX_ENCADEADOS
    cabe = u"capitulos 1" + u"".join(", %d" % (i + 2) for i in range(n))
    assert len(IO._citados(cabe)) == n + 1
    passa = cabe + u", %d" % (n + 2)
    assert len(IO._citados(passa)) == n + 1, (
        "a cadeia passou do teto de %d elos: sem a parada, uma frase cheia de "
        "numeros seria engolida inteira" % n)
    # e o elo de FAIXA conta no mesmo teto
    so_faixa = u"capitulos 1" + u"".join(", %d" % (i + 2) for i in range(n))
    assert max(IO._citados(so_faixa + u" a 40")) == n + 1, (
        "o elo de faixa entrou DEPOIS do teto de elos")


def test_faixa_ABSURDA_nao_entra():
    """A guarda de 60 capitulos vale tambem no elo de faixa da cadeia."""
    assert IO._citados(u"capitulos 1, 2 e 3 a 300") == {1, 2, 3}
    assert IO._citados(u"capitulos 1, 2 e 3 a 2") == {1, 2, 3}


# --------------------------------------------------- a nota nao pode sumir

def test_o_motivo_e_o_CUSTO_continuam_escritos():
    """Retratacao sem motivo escrito volta calada."""
    doc = IO._citados.__doc__ or ""
    assert "QUATRO formas" in doc
    assert "80 capitulos perdidos em 21 specs" in doc
    assert "s091" in doc and "27 a 30" in doc, (
        "o custo medido (o capitulo que eu ia escrever) saiu do docstring")
    assert "725" in doc
