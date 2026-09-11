"""O spec e o portao antes da conta: erro barato antes de erro caro.

Criativo no Meta e IMUTAVEL. Uma peca com campo faltando so quebraria depois de
ja ter criado o criativo, e ai o lixo fica na conta para sempre — nao da para
editar nem, nesta conta, apagar (`ads_creative_delete` responde "rolling out").
Por isso a conferencia roda inteira antes da primeira chamada.

O outro defeito que estes testes prendem e mais serio: orcamento. A regra de
corte (REGRA — corte de anuncio em 48 horas) diz que nada automatico mexe em
dinheiro. Um spec com `daily_budget` dentro nao pode chegar na API nem por
engano de quem edita o JSON.
"""
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anuncios_meta as A  # noqa: E402

SPEC = os.path.join(RAIZ, "entregas", "campanha", "ANUNCIOS — spec dos conjuntos.json")


def peca(**troca):
    base = {
        "slug": "AG99 — teste",
        "conjunto": "120247356527930766",
        "form_id": "2412763482587375",
        "page_id": "1117439194786453",
        "image_hash": "abc123",
        "headline": "Manchete",
        "message": "Corpo do anuncio.",
        "cta": "Candidatar-se",
    }
    base.update(troca)
    return base


def test_spec_entregue_passa_na_conferencia():
    assert A.conferir_spec(json.load(open(SPEC, encoding="utf-8"))) == []


def test_spec_entregue_cobre_os_dois_conjuntos_com_cinco_cada():
    # O pedido do Pablo foi "ao menos 5 variacoes por conjunto". Se alguem
    # apagar uma peca sem perceber, o conjunto fica com quatro e alguem so
    # descobre olhando o gerenciador.
    spec = json.load(open(SPEC, encoding="utf-8"))
    por_conjunto = {}
    for p in spec:
        por_conjunto.setdefault(p["conjunto"], []).append(p)
    assert len(por_conjunto) == 2
    for conjunto, pecas in por_conjunto.items():
        assert len(pecas) >= 5, conjunto


@pytest.mark.parametrize("campo", ["slug", "conjunto", "form_id", "headline", "message", "cta"])
def test_campo_faltando_reprova(campo):
    p = peca()
    del p[campo]
    assert A.conferir_spec([p]), f"faltou {campo} e passou"


def test_sem_imagem_reprova():
    p = peca()
    del p["image_hash"]
    assert A.conferir_spec([p])


def test_image_url_serve_no_lugar_do_hash():
    p = peca()
    del p["image_hash"]
    p["image_url"] = "https://exemplo/foto.jpg"
    assert A.conferir_spec([p]) == []


@pytest.mark.parametrize("campo", A.PROIBIDOS)
def test_orcamento_nunca_passa(campo):
    assert A.conferir_spec([peca(**{campo: 5000})])


def test_peca_repetida_no_mesmo_conjunto_reprova():
    assert A.conferir_spec([peca(), peca()])


def test_mesma_peca_em_conjuntos_diferentes_pode():
    outra = peca(conjunto="120247356496360766")
    assert A.conferir_spec([peca(), outra]) == []


def test_criativo_leva_o_formulario_dentro_do_call_to_action():
    # O `lead_gen_form_id` mora em call_to_action.value. Fora dali a Meta
    # devolve "Missing Lead Form (3390001)" — foi o erro de 11/09.
    enviado = {}

    def falso(caminho, token, dados=None, metodo=None):
        enviado.update(dados)
        return {"id": "1"}

    A._chamar, original = falso, A._chamar
    try:
        A.criar_criativo("123", peca(), "tok")
    finally:
        A._chamar = original
    spec = json.loads(enviado["object_story_spec"])
    cta = spec["link_data"]["call_to_action"]
    assert cta["value"]["lead_gen_form_id"] == "2412763482587375"
    assert spec["page_id"] == "1117439194786453"


def test_anuncio_nasce_pausado_quando_nao_pedem_para_ativar():
    enviado = {}

    def falso(caminho, token, dados=None, metodo=None):
        enviado.update(dados)
        return {"id": "1"}

    A._chamar, original = falso, A._chamar
    try:
        A.criar_anuncio("123", peca(), "cri", "tok")
    finally:
        A._chamar = original
    assert enviado["status"] == "PAUSED"


def test_nao_liga_se_o_conjunto_ficar_com_menos_de_dois_ativos():
    def falso(caminho, token, dados=None, metodo=None):
        return {"data": [{"name": "velho", "effective_status": "PAUSED"}]}

    A._chamar, original = falso, A._chamar
    try:
        assert A.pode_ativar("999", "tok", entrando=1) is False
        assert A.pode_ativar("999", "tok", entrando=2) is True
    finally:
        A._chamar = original
