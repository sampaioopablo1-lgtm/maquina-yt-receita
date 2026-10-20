# -*- coding: utf-8 -*-
"""O modulo devolvia PECAS do tamanho e a copy escreve FORMAS do tamanho.

**Medido em 20/10 as 18:4x.** Eu venho escrevendo na copy *"inedito nas SETE
formas de onze cenas"*, *"as DUAS formas de sete cenas"*, *"a TERCEIRA forma de
oito cenas"* — e o `esqueleto_entre_canais.novidade` devolvia
`exemplares_do_tamanho`, que e o numero de PECAS. **As duas grandezas ocupam o
MESMO lugar na frase** e divergem por um fator de ate 5,5 (34 pecas contra 7
formas em seis cenas; 149 contra 65 em dez). E o 753 em forma de UNIDADE.

**E AS CINCO AFIRMACOES DO ACERVO ESTAO CERTAS** — reconferidas aqui contra o
disco. Logo isto **nao e numero errado publicado**, e o arquivo cobra isso em vez
de inflar o achado: e uma conta que eu acertei cinco vezes a mao, com o numero
errado para a mesma frase disponivel no campo vizinho.

A forma dos testes segue a disciplina da semana: a varredura sai do DISCO e
reprova por vacuidade, as duas grandezas tem de DIVERGIR (se convergirem a nota
se rele), a frase tem UM dono cobrado por AST, e as cinco afirmacoes do acervo
sao derivadas por PROPRIEDADE — nenhuma spec e nomeada num assert.
"""
import ast
import collections
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import esqueleto_entre_canais as EC  # noqa: E402

PISO_DE_PECAS = 200
FONTE = open(os.path.join(RAIZ, "fabrica", "esqueleto_entre_canais.py"),
             encoding="utf-8").read()

NUMERO = {"uma": 1, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6,
          "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12,
          "treze": 13, "catorze": 14, "quinze": 15}
AFIRMACAO = re.compile(
    r"(?i)nas?\s+([a-z]+|\d+)\s+formas?\s+de\s+([A-Za-z]+)\s+cenas?")


def _pecas():
    pecas = EC.varre()
    assert len(pecas) >= PISO_DE_PECAS, (
        "a varredura achou %d pecas, menos que o piso de %d: o glob deixou de"
        " casar e TODO assert deste arquivo passaria por vacuidade"
        % (len(pecas), PISO_DE_PECAS))
    return pecas


def test_o_quadro_passa_a_ter_as_FORMAS_por_tamanho():
    q = EC.quadro(_pecas())
    assert "formas_por_contagem_de_cena" in q, (
        "o dono das FORMAS por tamanho desapareceu do quadro")
    fpc = q["formas_por_contagem_de_cena"]
    assert fpc, "o mapa de formas por tamanho veio vazio"
    # ele e DERIVADO das mesmas pecas, nao uma segunda varredura
    esperado = collections.defaultdict(set)
    for p in _pecas():
        esperado[p["cenas"]].add(p["esqueleto"])
    for n, formas in fpc.items():
        assert set(formas) == esperado[n], (
            "o mapa divergiu da varredura no tamanho %d" % n)


def test_PECAS_e_FORMAS_DIVERGEM_e_e_isso_que_torna_o_lugar_perigoso():
    """Se as duas convergirem, esta nota se rele em vez de o campo ficar.

    O fator vai MEDIDO em vez de repetido: e ele que mede o custo de trocar uma
    grandeza pela outra.
    """
    q = EC.quadro(_pecas())
    pares = []
    for n, pecas_n in q["por_contagem_de_cena"].items():
        formas_n = len(q["formas_por_contagem_de_cena"].get(n, []))
        assert formas_n <= pecas_n, (
            "tamanho %d: %d formas em %d pecas — forma sem peca e impossivel"
            % (n, formas_n, pecas_n))
        if formas_n:
            pares.append((n, pecas_n, formas_n, pecas_n / float(formas_n)))
    assert len(pares) >= 5, "poucos tamanhos para medir a divergencia"
    pior = max(pares, key=lambda x: x[3])
    assert pior[3] >= 2.0, (
        "o maior fator entre PECAS e FORMAS caiu para %.1f (tamanho %d): as duas"
        " grandezas convergiram e esta nota tem de ser RELIDA, porque o lugar"
        " deixou de ser perigoso" % (pior[3], pior[0]))


def test_novidade_devolve_as_DUAS_e_nao_troca_uma_pela_outra():
    pecas = _pecas()
    # derivado: o tamanho de MAIOR divergencia, para o assert nao depender de um
    # numero de cena que a producao muda
    q = EC.quadro(pecas)
    alvo, melhor = None, 0.0
    for n, pn in q["por_contagem_de_cena"].items():
        fn = len(q["formas_por_contagem_de_cena"].get(n, []))
        if fn and pn / float(fn) > melhor:
            alvo, melhor = n, pn / float(fn)
    assert alvo is not None
    nov = EC.novidade("x-y-z", alvo, pecas)
    for chave in ("exemplares_do_tamanho", "formas_do_tamanho",
                  "formas_do_tamanho_lista"):
        assert chave in nov, "`%s` saiu do retorno" % chave
    assert nov["formas_do_tamanho"] == len(nov["formas_do_tamanho_lista"])
    assert nov["formas_do_tamanho"] < nov["exemplares_do_tamanho"], (
        "no tamanho de maior divergencia as duas vieram iguais")


def test_o_exceto_vale_para_as_FORMAS_tambem():
    """Sem ele a forma da propria peca conta, e "inedita" nunca pode ser verdade.

    A peca de prova e DERIVADA: a unica do disco que e o UNICO exemplar da
    propria forma dentro do proprio tamanho. Nomear uma spec seria identidade
    onde ha propriedade (743/753/761).
    """
    pecas = _pecas()
    por_forma = collections.Counter(p["esqueleto"] for p in pecas)
    unica = None
    for p in pecas:
        if por_forma[p["esqueleto"]] == 1:
            unica = p
            break
    assert unica is not None, (
        "nenhuma peca do disco e o unico exemplar da propria forma — perdi a"
        " ancora e este teste nao mede o `exceto`")
    com = EC.novidade(unica["esqueleto"], unica["cenas"], pecas)
    sem = EC.novidade(unica["esqueleto"], unica["cenas"], pecas,
                      exceto=unica["arquivo"])
    assert com["formas_do_tamanho"] == sem["formas_do_tamanho"] + 1, (
        "o `exceto` nao retirou a forma da PROPRIA peca da contagem de formas:"
        " %d contra %d" % (com["formas_do_tamanho"], sem["formas_do_tamanho"]))
    assert com["forma_inedita"] is False and sem["forma_inedita"] is True
    # e o campo tem de continuar sendo o de FORMAS: se ele voltar a devolver
    # PECAS, a conta do `exceto` ainda fecha (uma peca a menos e uma forma a
    # menos), e so esta comparacao pega a troca.
    if sem["exemplares_do_tamanho"] > sem["formas_do_tamanho"]:
        assert sem["formas_do_tamanho"] < sem["exemplares_do_tamanho"]
    else:
        q = EC.quadro(pecas)
        maior = max(
            (p for p in q["por_contagem_de_cena"].items()
             if len(q["formas_por_contagem_de_cena"].get(p[0], [])) ),
            key=lambda kv: kv[1] / float(
                len(q["formas_por_contagem_de_cena"][kv[0]])))
        n = EC.novidade("x-y", maior[0], pecas)
        assert n["formas_do_tamanho"] < n["exemplares_do_tamanho"], (
            "`formas_do_tamanho` voltou a devolver o numero de PECAS")


def test_as_CINCO_afirmacoes_do_acervo_estao_CERTAS():
    """Reconferidas contra o disco, por PROPRIEDADE: nenhuma spec nomeada.

    O numero escrito em cada copy e o de formas do tamanho **excluindo a propria
    peca e as que vieram depois dela**. Como o disco nao guarda data, a
    conferencia e por limite: o escrito nao pode passar das formas que existem
    hoje, e tem de ser pelo menos UMA.
    """
    pecas = _pecas()
    q = EC.quadro(pecas)
    vistas = 0
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for m in AFIRMACAO.finditer(d.get("copy") or ""):
            escrito, tam = m.group(1).lower(), m.group(2).lower()
            if escrito not in NUMERO or tam not in NUMERO:
                continue
            vistas += 1
            hoje = len(q["formas_por_contagem_de_cena"].get(NUMERO[tam], []))
            assert 1 <= NUMERO[escrito] <= hoje, (
                "%s afirma %d formas de %d cenas, e o disco tem %d hoje"
                % (os.path.basename(f), NUMERO[escrito], NUMERO[tam], hoje))
    assert vistas >= 4, (
        "achei %d afirmacoes de 'N formas de M cenas' no acervo, e eram CINCO:"
        " sem elas este teste nao mede nada" % vistas)


def test_a_frase_tem_UM_dono_e_NOMEIA_as_duas_grandezas():
    """Imprimir uma so faria o leitor escrever a outra, que e o defeito."""
    arv = ast.parse(FONTE)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    assert "_frase_da_novidade" in defs, "o dono da frase desapareceu"
    corpo = ast.unparse(defs["_frase_da_novidade"])
    assert "exemplares_do_tamanho" in corpo and "formas_do_tamanho" in corpo, (
        "a frase deixou de nomear as DUAS grandezas: %r" % corpo)
    for outro in defs:
        if outro == "_frase_da_novidade":
            continue
        c = ast.unparse(defs[outro])
        assert "PECA(S)" not in c and "FORMA(S)" not in c, (
            "a frase ganhou um segundo dono em `%s`" % outro)

    pecas = _pecas()
    linha = EC._frase_da_novidade(EC.novidade("a-b-c", 6, pecas))
    assert "PECA(S)" in linha and "FORMA(S)" in linha, linha


def test_o_relato_CHAMA_o_dono_da_frase():
    """Instrumento consertado que o chamador nao alcanca e a classe dos mortos."""
    arv = ast.parse(FONTE)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    chamadas = [ast.unparse(c.func) for c in ast.walk(defs["relato"])
                if isinstance(c, ast.Call)]
    assert any("_frase_da_novidade" in c for c in chamadas), (
        "o `relato` nao chama o dono da frase: %r" % (chamadas,))
    alvo = sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")))
    escolhida = None
    for f in alvo:
        d = json.load(open(f, encoding="utf-8"))
        if d.get("short") and not d.get("longo"):
            escolhida = f
            break
    assert escolhida, "nenhuma spec de short solto no disco"
    r = EC.relato(escolhida)
    assert "FORMA(S) distinta(s)" in r, (
        "a frase nova nao chega ao relato de uma spec de verdade")


def test_a_medida_e_a_RETRATACAO_continuam_escritas():
    for pedaco in ("5,5", "formas_por_contagem_de_cena", "UNIDADE",
                   "CINCO estao CERTAS"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: sem isso a rodada seguinte nao sabe que as duas"
            " grandezas divergem, nem que o acervo esta certo" % pedaco)


def test_isto_NAO_virou_portao():
    """Pelo argumento do `mira.py`: aqui nao ha nada a reprovar."""
    arv = ast.parse(open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                         encoding="utf-8").read())
    importados = []
    for n in ast.walk(arv):
        if isinstance(n, ast.Import):
            importados += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            importados.append(n.module or "")
    assert not any("esqueleto_entre_canais" in (m or "") for m in importados), (
        "o `prontidao` passou a importar o instrumento: ele reprovaria o acervo")
