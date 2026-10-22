# -*- coding: utf-8 -*-
"""O INSTRUMENTO DIZIA SE A FORMA ERA NOVA, NUNCA QUAL USAR — 22/10, 03:3x.

Medido escrevendo o `labtreinamento-s105`. O `novidade` respondeu
`forma_inedita: False`, e para achar uma forma nova eu fui buscar as formas do
TAMANHO numa SEGUNDA chamada e escolhi A MAO, no olho. E a mesma falta do
`mira.orcamento` antes de 19/10 as 14:2x (*"esta na mira?"* sem *"quanto
escrever para entrar?"*) e do `contagem_de_cenas` antes de 20/10 as 03:2x, que
recusava sem ordenar.

E a colisao e recorrente: a primeira forma do `kolejny-poziom-s090` (21/10,
23:2x) tambem ja existia, e nas duas vezes quem pegou foi a segunda chamada.

O que estes testes cobram e a PROPRIEDADE: a contagem e EXATA, os dois lados
existem (ha mistura com ordem livre e ha mistura ESGOTADA), todo exemplo
devolvido e de fato livre, e o `exceto` do rascunho nao conta a propria peca.
"""
import ast
import collections
import inspect
import io
import math
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import esqueleto_entre_canais as EC  # noqa: E402
import variedade as V  # noqa: E402

PECAS = EC.varre()


def _mult(e):
    return tuple(sorted(collections.Counter(e.split("-")).items()))


def _usadas_por_tamanho():
    por = collections.defaultdict(set)
    for p in PECAS:
        if p.get("esqueleto"):
            por[p["cenas"]].add(p["esqueleto"])
    return por


def test_a_varredura_sai_do_DISCO_e_nao_pode_encolher():
    assert len(PECAS) >= 200, "a varredura caiu para %d peca(s)" % len(PECAS)


def test_a_contagem_de_possiveis_e_EXATA_e_nao_amostrada():
    """Recomputada contra o multinomial, para toda mistura do disco."""
    vistos = 0
    for cenas, formas in sorted(_usadas_por_tamanho().items()):
        if cenas > 14:
            continue
        for e in sorted(formas):
            lay = e.split("-")
            if lay[0] != "titulo" or lay[-1] != "cta":
                continue
            f = EC.formas_livres(cenas, lay, pecas=PECAS)
            meio = list(lay)
            meio.remove("titulo")
            meio.remove("cta")
            esperado = math.factorial(len(meio))
            for k in collections.Counter(meio).values():
                esperado //= math.factorial(k)
            assert f["possiveis"] == esperado, (e, f["possiveis"], esperado)
            assert f["livres"] == f["possiveis"] - f["tomadas"], (e, f)
            vistos += 1
    assert vistos >= 50, "so %d mistura(s) conferida(s)" % vistos


def test_os_DOIS_lados_existem__mistura_livre_e_mistura_ESGOTADA():
    """E falha se nenhuma estiver esgotada, ou se TODAS estiverem.

    Sem os dois lados o instrumento nao mede nada: se nada esgota, a recusa
    nunca dispara; se tudo esgota, livre nunca sai.
    """
    livres = esgotadas = 0
    for cenas, formas in _usadas_por_tamanho().items():
        if cenas > 14:
            continue
        for e in formas:
            lay = e.split("-")
            if lay[0] != "titulo" or lay[-1] != "cta":
                continue
            f = EC.formas_livres(cenas, lay, pecas=PECAS)
            if f["esgotado"]:
                esgotadas += 1
            else:
                livres += 1
    assert esgotadas >= 1, (
        "nenhuma mistura esta ESGOTADA — a recusa perdeu o objeto e a nota "
        "tem de ser relida")
    assert livres >= 1, "nenhuma mistura tem ordem livre"


def test_ESGOTADO_RECUSA_com_motivo_em_vez_de_lista_vazia():
    """Lista vazia faria a rodada seguinte procurar o que nao existe."""
    achou = None
    for cenas, formas in sorted(_usadas_por_tamanho().items()):
        for e in sorted(formas):
            lay = e.split("-")
            if lay[0] != "titulo" or lay[-1] != "cta":
                continue
            f = EC.formas_livres(cenas, lay, pecas=PECAS)
            if f["esgotado"]:
                achou = f
                break
        if achou:
            break
    assert achou, "o disco perdeu a mistura esgotada — rele a nota"
    assert achou["exemplos"] == []
    assert "ESGOTADO" in achou["motivo"]
    assert "MISTURA" in achou["motivo"], achou["motivo"]


def test_todo_exemplo_devolvido_e_de_fato_LIVRE():
    """Mesma mistura, mesmas pontas, e ausente do disco."""
    lay = "titulo-item-item-lista-barras-titulo-item-cta".split("-")
    f = EC.formas_livres(8, lay, pecas=PECAS)
    assert f["exemplos"], f
    usadas = _usadas_por_tamanho()[8]
    for e in f["exemplos"]:
        assert e not in usadas, e
        assert _mult(e) == _mult("-".join(lay)), e
        assert e.split("-")[0] == "titulo" and e.split("-")[-1] == "cta", e


def test_FRONTEIRA_um_exemplo_gravado_deixa_de_ser_livre():
    """Contraprova no outro sentido: sem ela bastaria devolver qualquer coisa."""
    lay = "titulo-item-item-lista-barras-titulo-item-cta".split("-")
    antes = EC.formas_livres(8, lay, pecas=PECAS)
    alvo = antes["exemplos"][0]
    mais = list(PECAS) + [{"arquivo": "ficticia-999.json", "canal": "ficticia",
                           "cenas": 8, "esqueleto": alvo}]
    depois = EC.formas_livres(8, lay, pecas=mais)
    assert depois["livres"] == antes["livres"] - 1, (antes["livres"],
                                                     depois["livres"])
    assert alvo not in depois["exemplos"]


def test_a_convencao_das_PONTAS_e_RECONFERIDA_contra_o_disco():
    """753: medida que ninguem reconfere envelhece calada."""
    formas = {p["esqueleto"] for p in PECAS if p.get("esqueleto")}
    a, z = EC.PONTAS_MEDIDAS
    ambas = sum(1 for e in formas
                if e.split("-")[0] == a and e.split("-")[-1] == z)
    frac = 1.0 * ambas / len(formas)
    assert 0.80 <= frac <= 0.99, (
        "a convencao das pontas mede %.3f das formas — fora da faixa em que "
        "ela foi medida (0,923). Rele a nota em vez de mover o numero" % frac)
    assert ambas < len(formas), (
        "a convencao virou universal — ai ela deixa de ser parametro")


def test_sem_a_convencao_das_pontas_o_espaco_e_MAIOR():
    """Os dois ramos existem, e o parametro muda a resposta."""
    lay = "titulo-item-item-lista-barras-titulo-item-cta".split("-")
    com = EC.formas_livres(8, lay, pecas=PECAS, pontas=True)
    sem = EC.formas_livres(8, lay, pecas=PECAS, pontas=False)
    assert sem["possiveis"] > com["possiveis"], (com["possiveis"],
                                                 sem["possiveis"])


def test_argumentos_que_DIVERGEM_levantam():
    """A licao de 21/10 as 00:4x: resposta bem formada sobre outra pergunta."""
    with pytest.raises(ValueError):
        EC.formas_livres(8, "titulo-item-cta", pecas=PECAS)


def test_o_exceto_do_RASCUNHO_nao_conta_a_PROPRIA_peca():
    """Medido em 22/10 as 03:4x, com o arquivo JA no disco.

    `relato(spec=sp)` nao recebe caminho, e o `exceto` caia para vazio: a peca
    se contava a si mesma. A falha e RESTRITIVA e nao permissiva, e custa
    trabalho jogado fora.
    """
    import json
    alvo = None
    for p in PECAS:
        caminho = os.path.join(RAIZ, "fabrica", "specs", p["arquivo"])
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            d = json.load(f)
        if not (d.get("short") and d.get("pacote")):
            continue
        esq = V.esqueleto(d["short"])
        n_sem = EC.novidade(esq, len(d["short"]), PECAS, "")
        n_com = EC.novidade(esq, len(d["short"]), PECAS, d["pacote"])
        if n_sem["exemplares_da_forma"] - n_com["exemplares_da_forma"] == 1:
            alvo = (d, esq)
            break
    assert alvo, "nenhuma peca do disco serve de ancora — rele a nota"
    d, esq = alvo
    r = EC.relato(spec=d)
    assert ("desta peca (%s)" % d["pacote"]) in r, r[:200]
    bloco = r.split("desta peca (%s):" % d["pacote"], 1)[1]
    n_com = EC.novidade(esq, len(d["short"]), PECAS, d["pacote"])
    if n_com["forma_inedita"]:
        assert "INEDITO" in bloco, bloco[:300]
    else:
        assert ("%d exemplar" % n_com["exemplares_da_forma"]) in bloco, bloco[:300]


def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos():
    """Por AST: frase duplicada e o 753 em forma de prosa."""
    fonte = io.open(os.path.join(RAIZ, "fabrica",
                                 "esqueleto_entre_canais.py"),
                    encoding="utf-8").read()
    assert fonte.count("ORDENS LIVRES destes mesmos layouts") == 1
    arvore = ast.parse(fonte)
    alvo = [n for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef)
            and n.name == "_frase_da_novidade"]
    assert alvo, "`_frase_da_novidade` desapareceu"
    chamadas = {ast.unparse(c.func) for c in ast.walk(alvo[0])
                if isinstance(c, ast.Call)}
    assert "_linha_das_livres" in chamadas, chamadas


def test_formas_livres_DELEGA_a_varredura_por_AST():
    """Ler o disco aqui seria o segundo dono da varredura."""
    fonte = inspect.getsource(EC.formas_livres)
    corpo = ast.unparse(ast.parse(fonte.strip()))
    for proibido in ("glob.glob", "os.listdir", "open("):
        assert proibido not in corpo, (
            "`formas_livres` le o disco por conta propria (%s) — o dono da "
            "varredura e o `varre`" % proibido)
    assert "varre(" in corpo


def test_o_separador_e_PERGUNTADO_ao_dono_e_UMA_vez():
    """Um dono e uma PERGUNTA, nao uma chamada por item.

    A primeira versao chamava `variedade.esqueleto` dentro do laco das
    permutacoes, e isso custou 47 s -> 228 s nos dois arquivos (medido). A
    propriedade que importa e dupla: o separador SEGUE o dono, e ele e
    perguntado uma vez so.
    """
    assert EC._separador() == "-"

    chamadas = []
    real = V.esqueleto

    def espiao(cenas):
        chamadas.append(1)
        return real(cenas)

    V.esqueleto = espiao
    try:
        lay = "titulo-item-item-lista-barras-titulo-item-cta".split("-")
        f = EC.formas_livres(8, lay, pecas=PECAS)
    finally:
        V.esqueleto = real
    assert f["possiveis"] == 120, f["possiveis"]
    assert len(chamadas) <= 2, (
        "o dono foi chamado %d vezes para 120 permutacoes — a pergunta voltou "
        "para dentro do laco" % len(chamadas))


def test_se_o_dono_trocar_de_separador_isto_ACOMPANHA():
    """Senao o separador voltaria a ser cravado, so escondido num helper."""
    real = V.esqueleto

    def outro(cenas):
        return "+".join((c or {}).get("layout") or "titulo" for c in cenas)

    V.esqueleto = outro
    try:
        assert EC._separador() == "+"
        lay = ["titulo", "item", "cta"]
        f = EC.formas_livres(3, lay, pecas=[])
        assert all("+" in e for e in f["exemplos"]), f["exemplos"]
    finally:
        V.esqueleto = real
