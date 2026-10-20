# -*- coding: utf-8 -*-
"""O `irmaos_da_origem` mostrava resumo de TERCEIRO e nunca a peca do irmao.

**Medido em 20/10 as 15:3x, escrevendo o `labtreinamento-s093`.** A familia que
eu ia usar — COMPARAR TRES ORCAMENTOS PELO PRECO QUANDO O ESCOPO DIFERE — e o
eixo do `labtreinamento-s010`, e o relato me mostrou o `s010` **tres vezes**
como *"ORDEM DE CONTRATACAO"*, porque quem o descrevia eram os OUTROS irmaos. A
narracao dele diz *"o preco cai porque o escopo encolheu, nao porque alguem
negociou"*, e o modulo nunca a mostrava.

**O que estes testes cobram, e por que cada um existe:**
  * a varredura sai do DISCO e **reprova por vacuidade** se o parque encolher;
  * os DOIS lados existem — irmao com o campo e irmao sem ele — e o arquivo
    **se rele** se um dos dois desaparecer;
  * a narracao e de PRIMEIRA mao e sai **sem truncar**: truncar por tamanho foi o
    que quase cortou a frase que salvou o `s035` (776), e aqui cortaria
    justamente a ULTIMA cena, que e onde o `s010` escreve o eixo;
  * irmao COM o campo **nao** recebe o bloco: o campo e o dono quando existe, e
    imprimir os dois criaria o segundo dono da familia — a assinatura que
    congelou a legenda;
  * a procedencia vai **ROTULADA** nos dois niveis (primeira e segunda mao), em
    vez de o relato misturar as duas;
  * e um **reproduz a colisao desta rodada** sem nomear o id no assert: ele
    DERIVA o irmao cuja narracao contem o eixo, porque nomear `s010` seria
    identidade onde ha propriedade (743/753/761).
"""
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402

ORIGEM = "yrWVyqQtw00"          # a origem da rodada de 20/10 as 15:3x
PECA_DA_RODADA = "labtreinamento-s093"


def _irmaos():
    return [i for i in IO.irmaos(ORIGEM) if i["pacote"] != PECA_DA_RODADA]


def test_a_varredura_nao_passa_por_VACUIDADE():
    """Sem irmaos o arquivo inteiro passaria sem medir nada — o defeito do 743."""
    todos = _irmaos()
    assert len(todos) >= 3, (
        "a origem %s tem %d irmaos no disco: com menos de tres este arquivo nao"
        " mede o defeito, ele passa por vacuidade" % (ORIGEM, len(todos)))


def test_os_DOIS_lados_existem_na_origem_de_prova():
    """Se todos tiverem o campo, ou nenhum, o arquivo deixa de medir o defeito.

    **Falha de proposito quando um dos lados desaparecer**, para que esta nota
    seja relida em vez de o teste ser mantido vazio.
    """
    todos = _irmaos()
    com = [i for i in todos if i["tem_campo_familia"]]
    sem = [i for i in todos if not i["tem_campo_familia"]]
    assert com and sem, (
        "a origem de prova precisa dos DOIS lados e tem com=%d sem=%d — se o"
        " acervo foi uniformizado, o defeito mudou de forma e esta nota se rele"
        % (len(com), len(sem)))


def test_todo_irmao_SEM_o_campo_entrega_a_NARRACAO():
    """Era isto que faltava: 66 das 379 specs de short so tinham o titulo."""
    sem = [i for i in _irmaos() if not i["tem_campo_familia"]]
    assert sem
    for i in sem:
        assert i["narracao"], (
            "%s nao tem o campo da familia E nao entrega narracao: entao so o"
            " titulo sobra, que e o estado que produziu a colisao" % i["pacote"])


def test_a_narracao_sai_INTEIRA_no_relato_sem_truncar():
    """A ULTIMA cena e onde o `s010` escreve o eixo — truncar a perderia."""
    r = IO.relato(ORIGEM, excluir=(PECA_DA_RODADA,))
    for i in _irmaos():
        if i["tem_campo_familia"]:
            continue
        for n in i["narracao"]:
            assert n in r, (
                "a cena %r de %s nao chegou INTEIRA ao relato — truncar por"
                " tamanho foi o que quase cortou a frase que salvou o `s035`"
                % (n[:40], i["pacote"]))


def test_a_colisao_desta_rodada_e_REPRODUZIDA_pelo_relato():
    """O eixo escopo-contra-preco tem de SAIR do relato, e o irmao e DERIVADO.

    Nomear `labtreinamento-s010` no assert seria identidade onde ha propriedade
    (743/753/761): a propriedade e que o irmao cuja PECA fala do eixo apareca
    com essa fala no relato, qualquer que seja ele.
    """
    todos = _irmaos()
    dono = [i for i in todos
            if any("escopo encolheu" in n for n in i["narracao"])]
    if not dono:
        pytest.fail(
            "nenhum irmao de %s fala do escopo que encolheu: este teste perdeu a"
            " ancora da colisao de 20/10 as 15:3x, e o caso tem de ser"
            " reancorado em vez de o arquivo seguir verde" % ORIGEM)
    r = IO.relato(ORIGEM, excluir=(PECA_DA_RODADA,))
    assert "escopo encolheu" in r, (
        "o eixo que quase me fez repetir familia (%s) nao aparece no relato"
        % dono[0]["pacote"])


def test_irmao_COM_o_campo_NAO_recebe_o_bloco_da_narracao():
    """Contraprova no outro sentido: o campo e o DONO quando existe.

    Sem este teste bastaria imprimir a narracao de todos, e ai o campo e a
    narracao seriam dois donos da mesma familia — a assinatura que congelou a
    legenda.
    """
    r = IO.relato(ORIGEM, excluir=(PECA_DA_RODADA,))
    com = [i for i in _irmaos() if i["tem_campo_familia"]]
    assert com
    for i in com:
        marca = "[%s | NARRACAO" % i["pacote"]
        assert marca not in r, (
            "%s TEM o campo da familia e ainda assim recebeu o bloco da"
            " narracao: o campo deixou de ser o dono unico" % i["pacote"])


def test_a_PROCEDENCIA_vai_rotulada_nos_dois_niveis():
    """Primeira mao e segunda mao nao podem sair misturadas.

    Foi exatamente a mistura que me enganou: tres frases de SEGUNDA mao sobre o
    `s010`, lidas como se fossem a familia dele.
    """
    r = IO.relato(ORIGEM, excluir=(PECA_DA_RODADA,))
    assert "primeira mao" in r, "o relato nao rotula a fonte de PRIMEIRA mao"
    assert "SEGUNDA mao" in r, (
        "o relato nao rotula a citacao como SEGUNDA mao — sem o rotulo ela volta"
        " a parecer a familia do irmao citado")


def test_a_MEDIDA_que_autorizou_o_conserto_continua_escrita():
    """E ela e da populacao que o modulo SERVE — short solto, nao pacote.

    O numero que eu ia relatar (*"66 de 379"*) era de PACOTES, que `irmaos()`
    nem considera irmao. Quem me pegou foi o teste abaixo, antes de eu escrever.
    """
    fonte = open(IO.__file__, encoding="utf-8").read()
    for pedaco in ("240", "171", "15:3x", "PRIMEIRA mao"):
        assert pedaco in fonte, (
            "a medida %r saiu do modulo: numero que ninguem reconfere envelhece"
            " calado (753)" % pedaco)
    assert "eram PACOTES" in fonte, (
        "a retratacao do meu numero errado saiu do modulo — sem ela a rodada"
        " seguinte readota o 66 como se fosse dos shorts")


def _populacao_que_o_modulo_serve():
    """As specs de SHORT SOLTO com copy: `irmaos()` exige `longo` vazio."""
    import glob
    saida = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not (d.get("short") or []) or d.get("longo"):
            continue
        if not (d.get("copy") or "").strip():
            continue
        saida.append(d)
    return saida


def test_a_medida_e_RECONFERIDA_contra_o_disco_na_populacao_CERTA():
    """Nao se trava o valor — trava-se a propriedade, e a populacao.

    O acervo cresce a cada rodada, logo cravar 171 seria identidade onde ha
    propriedade (743/753/761). O que nao pode mudar calado e: existem irmaos SEM
    o campo, eles sao a MAIORIA, e **todos** tem um bloco de prosa — que e o
    bloco que o `relato` prometia e nao imprimia.
    """
    pop = _populacao_que_o_modulo_serve()
    assert len(pop) >= 150, (
        "so %d specs de short solto com copy: a medida nao se sustenta e este"
        " arquivo passa por vacuidade" % len(pop))
    sem = [d for d in pop if not IO._secao(d.get("copy") or "",
                                           IO.CAMPO_FAMILIA)]
    assert sem, (
        "nenhum short solto ficou sem o campo da familia: o acervo foi"
        " uniformizado, o defeito mudou de forma e esta nota se rele")
    com_prosa = [d for d in sem
                 if any(IO._secao(d["copy"], b) for b in IO.BLOCOS_DE_PROSA)]
    assert len(com_prosa) == len(sem), (
        "%d dos %d irmaos sem campo nao tem bloco de prosa: ai so o titulo"
        " sobra, e isso tem de ir DITO em vez de o conserto parecer completo"
        % (len(sem) - len(com_prosa), len(sem)))


def test_a_medida_ERRADA_que_eu_ia_relatar_fica_registrada():
    """Os 66 eram PACOTES, e pacote nao e irmao — `irmaos()` os exclui.

    Este teste existe para que o numero errado nao volte: ele mede que as duas
    populacoes de fato DIVERGEM, e reprova se elas convergirem (ai a distincao
    perdeu o objeto e a nota se rele).
    """
    import glob
    pacotes_so_titulo = 0
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not (d.get("short") or []) or not d.get("longo"):
            continue
        cp = d.get("copy") or ""
        if not cp.strip() or IO._secao(cp, IO.CAMPO_FAMILIA):
            continue
        if any(IO._secao(cp, b) for b in IO.BLOCOS_DE_PROSA):
            continue
        pacotes_so_titulo += 1
    soltos_so_titulo = 0
    for d in _populacao_que_o_modulo_serve():
        cp = d["copy"]
        if IO._secao(cp, IO.CAMPO_FAMILIA):
            continue
        if any(IO._secao(cp, b) for b in IO.BLOCOS_DE_PROSA):
            continue
        soltos_so_titulo += 1
    assert pacotes_so_titulo > soltos_so_titulo, (
        "as duas populacoes convergiram (pacotes=%d, soltos=%d): a confusao que"
        " produziu o meu 66 deixou de ser possivel, e esta nota se rele"
        % (pacotes_so_titulo, soltos_so_titulo))
    assert soltos_so_titulo == 0, (
        "%d short(s) solto(s) ficaram so com o titulo: o conserto da prosa nao"
        " os alcanca e isso tem de ir dito" % soltos_so_titulo)


def test_o_relato_IMPRIME_o_bloco_de_prosa_que_promete():
    """A linha de ATENCAO manda *"leia a PROSA abaixo"* — e ela tem de estar la.

    Contraprova no outro sentido: antes de 20/10 as 15:4x o `irmaos()` calculava
    a prosa e o `relato` a jogava fora, em 171 de 171 casos. Sem este teste o
    conserto volta calado.
    """
    r = IO.relato(ORIGEM, excluir=(PECA_DA_RODADA,))
    assert "leia a PROSA abaixo" in r, "o relato parou de prometer a prosa"
    sem = [i for i in _irmaos() if not i["tem_campo_familia"] and i["prosa"]]
    assert sem, "nenhum irmao sem campo tem prosa: o teste perdeu a ancora"
    for i in sem:
        for texto in i["prosa"].values():
            for par in texto.split("\n\n"):
                par = " ".join(par.split())
                if len(par) > 30:
                    assert par in r, (
                        "o paragrafo %r de %s nao chegou ao relato: a linha"
                        " promete a prosa e a saida nao a tem"
                        % (par[:50], i["pacote"]))


def test_a_narracao_sai_da_SPEC_e_nao_da_copy():
    """Contraprova: spec sem cena nenhuma devolve lista vazia, nao texto da copy.

    Se `_narracao` caisse na copy quando a spec esta vazia, ela deixaria de ser
    de primeira mao e voltaria a ser prosa — o estado que o conserto desfaz.
    """
    assert IO._narracao({}) == []
    assert IO._narracao({"short": [], "copy": "## NARRACAO\nqualquer coisa"}) == []
    assert IO._narracao({"short": [{"nar": "  uma fala  "}, {"nar": ""}]}) == [
        "uma fala"]
