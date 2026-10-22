# -*- coding: utf-8 -*-
"""A declaracao de capitulo era lida numa FORMA so — 22/10 as 21:4x.

O `_citados` casava **FAIXA** (`capitulos N a M`) e **capitulo UNICO**
(`capitulo N`), e so em portugues. Logo a ENUMERACAO (`capitulos 30, 31 e 32`)
e a palavra em outra lingua ficavam invisiveis, e capitulo declarado por um
irmao saia como LIVRE — que e o defeito de 12/10 as 12:3x, que me custou duas
cenas do `kolejny-poziom-s093`.

**EU FUI PROCURAR O 725 E ENCONTREI OUTRO DEFEITO, MAIOR.** A hipotese era
lingua (vocabulario de um idioma lido como cobertura da frota); medido, das 293
copies de short solto **181 citam capitulo** e o padrao antigo pegava **136** —
e dos 45 perdidos, **UM** era de lingua e **QUARENTA E QUATRO** de FORMA.

**E O CONSERTO REVELOU UM FALSO POSITIVO QUE JA EXISTIA:** das 26 copies com
secao `## RESERVA`, **DEZESSEIS** tinham capitulos dela contados como
DECLARADOS — e a reserva diz `LIVRES os capitulos N e M`, o oposto de usado.
Contar aquilo faria a rodada seguinte PULAR o que o irmao deixou livre, que e
detector inventando achado (725).

A FORMA DOS TESTES: a varredura sai do DISCO com piso de vacuidade, as TRES
formas sao cobradas uma a uma, a contraprova vai nos DOIS sentidos, a secao
`## RESERVA` e cobrada FORA, o encadeamento e cobrado na FRONTEIRA (ele PARA no
primeiro token que nao liga), a medida e RECONFERIDA como PROPORCAO (14:4x) e o
conteudo da reserva **nao pode ser reparseado** aqui, por AST.
"""
import ast
import glob
import inspect
import json
import os
import re
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO   # noqa: E402

PISO_COPIES = 150


@pytest.fixture(scope="module")
def copies():
    out = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if sp.get("short") and not sp.get("longo") and sp.get("copy"):
            out.append(sp)
    assert len(out) >= PISO_COPIES, (
        "so %d copy(ies) de short solto: abaixo de %d este arquivo passa por "
        "VACUIDADE" % (len(out), PISO_COPIES))
    return out


# ------------------------------------------------------------- as tres formas

def test_a_FAIXA_continua_sendo_lida():
    assert IO._citados("usei os capitulos 30 a 33 do longo") == {30, 31, 32, 33}


def test_o_capitulo_UNICO_continua_sendo_lido():
    assert IO._citados("o capitulo 42 diz isso") == {42}


def test_a_ENUMERACAO_passou_a_ser_lida():
    """44 dos 45 casos perdidos eram esta forma."""
    assert IO._citados("capitulos 30, 31 e 32") == {30, 31, 32}
    assert IO._citados("rozdzialy 30, 31 i 32") == {30, 31, 32}
    assert IO._citados("κεφαλαια 30, 31 και 32") == {30, 31, 32}


def test_a_PALAVRA_em_outra_lingua_e_lida():
    assert IO._citados("rozdzial 27 podaje kolejnosc") == {27}
    assert IO._citados("το κεφαλαιο 14 λεει") == {14}


def test_a_FRONTEIRA_do_encadeamento_PARA_no_primeiro_token_que_nao_liga():
    """Sem a parada, uma frase cheia de numeros seria engolida — o 725."""
    achados = IO._citados("capitulos 30, 31 e 32, com 9 por cento e 12 meses")
    assert 30 in achados and 31 in achados and 32 in achados
    assert 9 not in achados and 12 not in achados, (
        "o encadeamento engoliu numero que nao e capitulo: %r" % sorted(achados))
    # e o limite de encadeados existe e e respeitado
    longa = "capitulos 1" + "".join(", %d" % n for n in range(2, 30))
    assert len(IO._citados(longa)) <= IO.MAX_ENCADEADOS + 1


def test_numero_SEM_a_palavra_NAO_entra():
    """Contraprova no outro sentido: alargar para numero nu seria o 725."""
    assert IO._citados("nove por cento e doze meses, 42 e 43") == set()


# ------------------------------------------------------------- a reserva fora

def test_a_secao_RESERVA_fica_FORA_dos_declarados():
    copy = (
        "## FONTES\nusei os capitulos 30, 31 e 32.\n\n"
        "## RESERVA\n* LIVRES os capitulos 49 e 50 — familia propria;\n"
        "* NAO LEVAR os capitulos 41 e 44: territorio do s072.\n\n"
        "## HASHTAGS\n#x\n")
    decl = IO._capitulos_declarados(copy)
    assert set(decl) == {30, 31, 32}, (
        "a reserva vazou para os declarados: %r — e `LIVRES` e o OPOSTO de "
        "usado" % decl)
    # contraprova: sem a secao, os mesmos numeros ENTRAM
    assert {49, 50} <= IO._citados("LIVRES os capitulos 49 e 50")


def test_a_secao_RESERVA_nao_e_REPARSEADA_aqui_por_AST():
    fonte = textwrap.dedent(inspect.getsource(IO._sem_reserva))
    nomes = set()
    for n in ast.walk(ast.parse(fonte)):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
    for proibido in ("_citados", "capitulos_negados", "relato", "reservas"):
        assert proibido not in nomes, (
            "`_sem_reserva` chama %r: o dono do conteudo da reserva e o "
            "`reservas_escritas`, e reparsear aqui cria o segundo dono"
            % proibido)
    assert "_sem_reserva" in textwrap.dedent(
        inspect.getsource(IO._capitulos_declarados)), (
        "o `_capitulos_declarados` tem de CHAMAR a exclusao")


def test_o_bloco_de_NEGACAO_continua_fora():
    copy = ("## FONTES\ncapitulos 30, 31 e 32.\n\n"
            "O QUE EU NAO LEVEI: os capitulos 55 e 56, porque mudam.\n")
    assert set(IO._capitulos_declarados(copy)) == {30, 31, 32}


# ------------------------------------------------------- a medida, no disco

def test_a_cobertura_e_RECONFERIDA_contra_o_disco(copies):
    qualquer = re.compile(IO.PALAVRA_CAPITULO + r"\s+\d{1,3}", re.I)
    cita = pega = 0
    for sp in copies:
        corpo = IO._sem_reserva(sp["copy"])
        if not qualquer.search(corpo):
            continue
        cita += 1
        if IO._capitulos_declarados(sp["copy"]):
            pega += 1
    assert cita >= 50, "so %d copy(ies) citam capitulo: vacuidade" % cita
    frac = pega / float(cita)
    assert frac >= 0.95, (
        "o parser pega %.3f das %d copies que citam capitulo (%d) — abaixo de "
        "0,95 alguma FORMA de declaracao voltou a ficar invisivel, e capitulo "
        "declarado saindo como LIVRE e o defeito de 12/10 as 12:3x"
        % (frac, cita, pega))


def test_a_RESERVA_nao_vaza_em_NENHUMA_copy_do_disco(copies):
    com_reserva = vazam = 0
    for sp in copies:
        res = IO._secao(sp["copy"], "RESERVA")
        if not res:
            continue
        com_reserva += 1
        so_da_reserva = (set(IO._capitulos_declarados(sp["copy"]))
                         - IO._citados(IO._sem_reserva(sp["copy"])))
        if so_da_reserva:
            vazam += 1
    assert com_reserva >= 5, (
        "so %d copy(ies) com secao RESERVA: sem elas este teste nao mede nada, "
        "e ai esta nota se rele" % com_reserva)
    assert vazam == 0, (
        "%d de %d copies ainda contam capitulo da RESERVA como DECLARADO"
        % (vazam, com_reserva))


def test_o_motivo_e_as_DUAS_medidas_continuam_escritos():
    doc = (IO._citados.__doc__ or "") + (IO._sem_reserva.__doc__ or "")
    for pedaco in ("ENUMERACAO", "44", "DEZESSEIS", "LIVRES", "725"):
        assert pedaco in doc, (
            "a prosa perdeu %r: conserto sem motivo escrito volta calado"
            % pedaco)


# ------------------------------------------------- qual secao o balde pegou

def test_a_secao_do_BALDE_sai_NOMEADA_nos_dois_ramos():
    """Medido em 22/10 as 21:5x: 17 de 90 copies legiveis tinham o balde
    pegando a secao ERRADA, e o defeito e LATENTE — o comentario e parseado e
    nunca postado. O que faltava era NOMEAR, nao gated (20/10, 20:3x)."""
    import copy_secoes as CS
    base = (
        "## TITULO\nT\n\n## TITULO SHORT\nS\n\n## DESCRICAO\n"
        + ("palavra " * 210) + "\n\n%s\n\n## HASHTAGS\n#a\n\n"
        "## TAGS\na, b\n\n## MUSICA / LICENCA\nTrilha X.\n")
    ordem_certa = base % ("## COMENTARIO FIXADO\nPergunta ao leitor.\n\n"
                          "## FONTES\nOs capitulos 30 e 31.")
    ordem_errada = base % ("## FONTES\nOs capitulos 30 e 31.\n\n"
                           "## COMENTARIO FIXADO\nPergunta ao leitor.")
    sp = {"pacote": "x-001", "slug": "x-001", "idioma": "pt-BR",
          "short": [{"layout": "titulo", "nar": "a"}], "longo": []}
    certa = CS.secao_do_balde(dict(sp, copy=ordem_certa), ".")
    errada = CS.secao_do_balde(dict(sp, copy=ordem_errada), ".")
    assert certa["possivel"] and errada["possivel"]
    assert certa["bate"] is True, (
        "com a secao do comentario PRIMEIRO entre as nao casadas, o balde tem "
        "de pegar ela: pegou %r" % certa["balde"])
    assert errada["bate"] is False and errada["balde"] == "FONTES", (
        "com FONTES antes, o balde pega FONTES — e e isso que tem de sair "
        "NOMEADO: %r" % errada)
    assert "nunca postado" in (errada["motivo"] or ""), (
        "o motivo tem de dizer que o defeito e LATENTE, senao o achado infla")
    # a frase tem UM dono e sai nos DOIS ramos
    import inspect
    import textwrap as _tw
    fonte = _tw.dedent(inspect.getsource(CS))
    assert fonte.count("SECAO DO BALDE") == 3, (
        "a frase tem de ter UM dono com os TRES ramos: %d ocorrencia(s)"
        % fonte.count("SECAO DO BALDE"))
    assert "_linha_do_balde" in _tw.dedent(inspect.getsource(CS.relato)), (
        "o relato tem de CHAMAR a linha — calculado e descartado e a classe "
        "dos layouts mortos")
