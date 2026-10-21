"""Ele aceitava os dois argumentos TROCADOS — 21/10 as 00:4x.

Eu chamei `novidade("labtreinamento", "titulo-lista-item-barras-item-titulo-item-cta")`
— canal no lugar do esqueleto, esqueleto no lugar da contagem — e ele devolveu
uma resposta BEM FORMADA sobre OUTRA pergunta: `forma_inedita=True`,
`tamanho_inedito=True`, `exemplares_do_tamanho=0`. **As duas metades sairam
"NOVO", que e a direcao PERMISSIVA**, e eu ia escrever isso na copy.

A CAUSA e que as duas contas comparam por IGUALDADE, e igualdade com tipo errado
nao levanta: ela devolve "nao casou", que e exatamente a resposta *inedito*.
Medido nos oito pares (texto, numero) adjacentes da fabrica que se pode chamar
sem banco, **SETE LEVANTAM** com os argumentos trocados e **so este CALAVA** —
logo nao e defeito de familia, e vai dito assim em vez de inflado.

E A GUARDA E DE TIPO, NAO DE COERENCIA: os dois argumentos nao sao redundantes.
A frota tem forma inedita com tamanho repetido, e ha teste que chama esqueleto
INVENTADO com contagem real de proposito. Cobrar `len(esq.split('-')) == cenas`
quebraria uso legitimo — e os testes abaixo exigem que ele continue passando.
"""
import ast
import inspect
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import esqueleto_entre_canais as EC  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "esqueleto_entre_canais.py")
# O caso MEDIDO, com os argumentos na ordem em que eu os digitei.
CANAL_NO_LUGAR_DO_ESQ = "labtreinamento"
ESQ_NO_LUGAR_DAS_CENAS = "titulo-lista-item-barras-item-titulo-item-cta"


def _uma_peca_real():
    """Uma peca do disco, DERIVADA — nomear um pacote seria identidade onde ha
    propriedade (743/753/761), e o disco muda a cada rodada."""
    pecas = EC.varre()
    assert len(pecas) >= 150, (
        "a varredura caiu para %d pecas; abaixo disso este arquivo passa por "
        "vacuidade" % len(pecas))
    return pecas[0]


def test_o_caso_MEDIDO_levanta_em_vez_de_responder():
    with pytest.raises(TypeError) as e:
        EC.novidade(CANAL_NO_LUGAR_DO_ESQ, ESQ_NO_LUGAR_DAS_CENAS)
    assert "cenas" in str(e.value), (
        "a mensagem tem de dizer QUAL argumento veio errado; saiu: %s" % e.value)
    assert "ordem" in str(e.value).lower(), (
        "a mensagem tem de dizer a ORDEM certa dos dois, senao quem a le nao "
        "sabe o que corrigir; saiu: %s" % e.value)


def test_os_DOIS_argumentos_sao_cobrados_e_bool_nao_passa_por_int():
    """`isinstance(True, int)` e True em Python, logo sem o ramo do bool um
    `cenas=True` entraria como a contagem UM."""
    with pytest.raises(TypeError):
        EC.novidade(8, "titulo-item-cta")          # os dois invertidos
    with pytest.raises(TypeError):
        EC.novidade(None, 8)                        # esq nao e texto
    with pytest.raises(TypeError):
        EC.novidade("titulo-item-cta", "8")         # cenas e texto de numero
    with pytest.raises(TypeError):
        EC.novidade("titulo-item-cta", True)        # bool nao e contagem
    with pytest.raises(TypeError):
        EC.novidade("titulo-item-cta", 3.0)         # float nao e contagem


def test_CONTRAPROVA_a_chamada_certa_continua_respondendo():
    """Sem isto, levantar sempre passaria por este arquivo."""
    p = _uma_peca_real()
    n = EC.novidade(p["esqueleto"], p["cenas"])
    assert n["esqueleto"] == p["esqueleto"]
    assert n["cenas"] == p["cenas"]
    assert n["exemplares_da_forma"] >= 1, (
        "a peca esta no disco, logo a forma dela tem ao menos um exemplar")


def test_a_guarda_e_de_TIPO_e_NAO_de_coerencia_entre_os_dois():
    """Esqueleto INVENTADO com contagem real tem de continuar passando — os dois
    argumentos respondem perguntas INDEPENDENTES, e ha teste da suite que usa
    exatamente essa forma."""
    n = EC.novidade("inventado-que-nao-existe-em-lugar-nenhum", 8)
    assert n["forma_inedita"] is True
    assert n["exemplares_do_tamanho"] >= 1, (
        "a contagem 8 existe na frota, logo a metade do TAMANHO tem de "
        "responder mesmo com o esqueleto inventado — se ela zerar, a guarda "
        "virou de coerencia e quebrou uso legitimo")
    # e o contrario: forma real com contagem que ninguem usou
    p = _uma_peca_real()
    m = EC.novidade(p["esqueleto"], 37)
    assert m["exemplares_da_forma"] >= 1 and m["tamanho_inedito"] is True, (
        "forma real com tamanho inedito tem de responder as duas metades")


def test_as_duas_metades_de_fato_DIVERGEM_na_frota():
    """Se forma e tamanho andassem juntos, a guarda de coerencia seria legitima
    e esta nota se releria. Medido no disco."""
    q = EC.quadro()
    por_tam = q["formas_por_contagem_de_cena"]
    com_varias = [c for c, fs in por_tam.items() if len(fs) >= 2]
    assert com_varias, (
        "nenhuma contagem de cena tem duas formas distintas no disco — as duas "
        "perguntas convergiram e esta nota tem de ser RELIDA")


def test_a_guarda_vem_ANTES_da_varredura_do_disco():
    """Chamada errada nao deve pagar a varredura das ~380 specs: a guarda e de
    porta. Cobrado por AST, na ORDEM dos statements."""
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    fn = [n for n in ast.walk(arvore)
          if isinstance(n, ast.FunctionDef) and n.name == "novidade"]
    assert fn, "a funcao `novidade` nao existe mais no modulo"
    corpo = [s for s in fn[0].body if not (
        isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    i_guarda = None
    i_varre = None
    for i, s in enumerate(corpo):
        txt = ast.unparse(s)
        if i_guarda is None and "raise TypeError" in txt:
            i_guarda = i
        if i_varre is None and "varre()" in txt:
            i_varre = i
    assert i_guarda is not None, "a guarda de tipo saiu do corpo da funcao"
    assert i_varre is not None, "a varredura saiu do corpo da funcao"
    assert i_guarda < i_varre, (
        "a guarda esta DEPOIS da varredura (posicoes %d e %d): chamada errada "
        "pagaria a leitura do disco inteiro antes de levantar"
        % (i_guarda, i_varre))


def test_o_par_dela_e_o_UNICO_que_calava_e_isso_e_RECONFERIDO():
    """Numero medido que ninguem reconfere envelhece calado (753). A afirmacao e
    *"sete dos oito levantam"*, e ela se refaz chamando os sete."""
    casos = [
        ("ensaio", "chars_por_cena", ("pt-BR-ThalitaMultilingualNeural", 8)),
        ("ensaio", "piso_de_caracteres", ("pt-BR-ThalitaMultilingualNeural", 8)),
        ("mira", "chars_no_alvo", ("pt-BR-ThalitaMultilingualNeural", 8)),
        ("mira", "janela_do_mundo", ("pt-BR-ThalitaMultilingualNeural", 8)),
        ("mira", "janela_dos_dois_mundos",
         ("pt-BR-ThalitaMultilingualNeural", 8)),
        ("legenda", "pedacos", ("uma frase qualquer aqui", 4)),
        ("contagem_de_cenas", "recentes_do_canal", ("labtreinamento", 2)),
    ]
    calam = []
    for mod, nome, args in casos:
        f = getattr(__import__(mod), nome)
        try:
            f(args[1], args[0])
            calam.append("%s.%s" % (mod, nome))
        except Exception:
            pass
    assert not calam, (
        "estes pares passaram a CALAR com os argumentos trocados: %s. A "
        "afirmacao do modulo e que aritmetica e busca em tabela se defendem "
        "sozinhas; se deixaram de se defender, o defeito virou de FAMILIA e "
        "esta nota tem de ser RELIDA em vez de reaproveitada" % (calam,))


def test_a_REGRA_e_o_caso_medido_continuam_escritos():
    doc = inspect.getdoc(EC.novidade) or ""
    assert "IGUALDADE" in doc.upper(), (
        "a regra — funcao que so compara por igualdade nao se defende sozinha — "
        "saiu do docstring, e e ela que impede a rodada seguinte de tirar a "
        "guarda por parecer defensiva demais")
    assert "SETE" in doc.upper() or "7" in doc, (
        "a medida dos oito pares saiu do docstring")
    assert "PERMISSIVA" in doc.upper(), (
        "o docstring tem de dizer que as duas metades saiam 'NOVO', que e a "
        "direcao permissiva — sem isso o defeito parece cosmetico")
