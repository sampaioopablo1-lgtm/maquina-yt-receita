#!/usr/bin/env python3
"""O SOM do run morava DENTRO do `provedor`, e eu o procurei no `leitura`.

Medido em 22/10 as 08:3x, parqueando a peca da propria rodada. A `leitura`
devolve exatamente DUAS chaves — `run` e `jobs` — e `som` nunca foi uma delas;
eu escrevi `for s in leitura(run).get("som", []):` e o laco **nao rodou nenhuma
vez**. Nada levantou, nada foi parqueado, e a chamada imprimiu o `run` como se
tivesse funcionado. O unico discriminador foi RELER o parque.

E o `.get` com default e a forma mais confortavel da familia do vazio: a chave
nunca existiu naquela resposta, e o default a faz parecer lista legitimamente
vazia. O que este arquivo cobra e PROPRIEDADE, nao os ids desta rodada
(743/753/761).
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR  # noqa: E402

SOM_OK = ('SOM short.mp4 labtreinamento-s107 {"lufs": -13.6, "lra": 2.6, '
          '"pico_dbtp": -1.4, "desvio_do_alvo": 0.4, "silencios": [], '
          '"pico_vs_teto": "acima_do_teto", "teto_dbtp": -1.5}')
PUB_OK = ("PUBLICADO labtreinamento-s107 shorts youtube_id=0DHQwyvqJnE "
          "titulo=Parece desconto, e troca em=2026-10-22T08:21:38Z")
PIPER = "::warning::NARRACAO PELO PIPER cena 2"


def _lida(jobs, run="39746729706"):
    return {"run": run, "jobs": [
        {"id": i, "nome": n, "conclusao": "success", "mensagens": m}
        for i, n, m in jobs]}


# Os DOIS lados, e sem eles este arquivo nao mede nada: um job que narrou (ele
# emitiu SOM) e um que so publicou.
NARROU = ("119716961370", "produzir (labtreinamento, labtreinamento-s107)",
          ["Node.js 20...", SOM_OK])
SO_PUBLICOU = ("119717111111", "publicar", ["Node.js 20...", PUB_OK])


def test_a_fixture_tem_os_DOIS_lados():
    """Sem um job que narrou e um que nao, recusar sempre passaria."""
    assert AR.jobs_que_narraram(_lida([NARROU])), (
        "o lado que NARROU tem de existir, senao o teste da resposta e vacuo")
    assert AR.jobs_que_narraram(_lida([SO_PUBLICOU])) == [], (
        "o lado que NAO narrou tem de existir, senao o teste da recusa e vacuo")


def test_o_DEFEITO_reproduzido_a_chave_som_nao_existe_no_leitura():
    """E ele reprova se a `leitura` passar a ter a chave — ai isto se rele."""
    lida = _lida([NARROU])
    assert "som" not in lida, (
        "a `leitura` passou a trazer `som` no topo: o defeito de 08:3x perdeu o"
        " objeto e esta nota tem de ser RELIDA em vez de ficar")
    # E a forma do defeito: `.get` com default devolve vazio BEM FORMADO, sem
    # levantar e sem dizer que a chave nunca existiu.
    assert lida.get("som", []) == []
    assert sorted(AR.leitura.__doc__ and lida.keys()) == ["jobs", "run"], (
        "a `leitura` tem de ter exatamente DUAS chaves — e a medida dessas duas"
        " e o que torna o `.get('som')` silenciosamente vazio")


def test_som_do_run_devolve_a_lista_FLAT():
    sons = AR.som_do_run(_lida([NARROU]))
    assert len(sons) == 1, sons
    assert sons[0]["pacote"] == "labtreinamento-s107"
    assert sons[0]["pico_dbtp"] == -1.4
    assert sons[0]["job"] == NARROU[0]
    assert sons[0]["run"] == "39746729706", (
        "o `run` tem de DESCER ao registro: foi ele que faltou em 06:2x")


def test_ela_RECUSA_em_vez_de_devolver_vazio():
    """Devolver `[]` aqui seria refazer o defeito que ela conserta."""
    with pytest.raises(AR.SemProcedencia) as e:
        AR.som_do_run(_lida([SO_PUBLICOU]))
    msg = str(e.value)
    assert "vazio" in msg.lower() and "08:3x" in msg, msg


def test_o_filtro_por_pacote_vai_nos_DOIS_sentidos():
    lida = _lida([NARROU, SO_PUBLICOU])
    assert len(AR.som_do_run(lida, "labtreinamento-s107")) == 1
    with pytest.raises(AR.SemProcedencia):
        AR.som_do_run(lida, "kolejny-poziom-s999")


def test_o_provedor_DELEGA_a_lista_flat_e_as_duas_concordam():
    lida = _lida([NARROU, SO_PUBLICOU])
    p = AR.provedor(lida, "labtreinamento-s107")
    assert p["provedor"] == "edge" and p["avisos_piper"] == 0
    assert p["som"] == AR.som_do_run(lida, "labtreinamento-s107"), (
        "duas contas da mesma coisa tem de concordar — e e por isso que a lista"
        " flat tem UM dono")
    # contraprova no outro sentido: com o aviso do 733, o provedor vira piper e
    # a lista flat NAO muda (ela e do som, nao do provedor).
    lida2 = _lida([(NARROU[0], NARROU[1], NARROU[2] + [PIPER])])
    p2 = AR.provedor(lida2)
    assert p2["provedor"] == "piper" and p2["avisos_piper"] == 1
    assert [s["pacote"] for s in p2["som"]] == ["labtreinamento-s107"]


def _corpo(fn):
    """A arvore da funcao SO.

    O `cleandoc` nao serve aqui: ele desindenta a linha do `def` e deixa o
    corpo torto, e foi essa a PRIMEIRA versao deste helper — o teste estava
    errado, nao o modulo.
    """
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def test_som_do_run_NAO_reparseia_a_anotacao_por_AST():
    """Ela DELEGA ao `jobs_que_narraram`; reparsear criaria o segundo dono."""
    arvore = _corpo(AR.som_do_run)
    chamadas = {n.func.id for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "jobs_que_narraram" in chamadas, (
        "sem chamar o dono, ela volta a ser um segundo leitor da anotacao")
    atributos = {n.attr for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    for proibido in ("do_notice", "startswith", "loads"):
        assert proibido not in atributos, (
            "`%s` dentro do `som_do_run` e o segundo dono da forma da anotacao"
            % proibido)


def test_o_provedor_NAO_remonta_a_lista_por_AST():
    arvore = _corpo(AR.provedor)
    chamadas = {n.func.id for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "som_do_run" in chamadas, (
        "o `provedor` tem de CHAMAR o dono da lista flat — remonta-la ali foi"
        " o que a escondeu atras de um nome sobre o provedor")
    for n in ast.walk(arvore):
        if isinstance(n, ast.ListComp):
            fonte = ast.dump(n)
            assert '"som"' not in fonte and "'som'" not in fonte, (
                "compreensao sobre `j['som']` dentro do `provedor` e a lista"
                " flat com DOIS donos outra vez")


def test_a_FAMILIA_e_a_medida_continuam_escritas():
    doc = AR.som_do_run.__doc__ or ""
    for marca in ("08:3x", "BEM FORMADO", "DUAS chaves", "RELER o parque",
                  "oitavo membro"):
        assert marca in doc, (
            "sem %r a rodada seguinte nao sabe por que esta funcao existe, e"
            " volta a procurar o som no `leitura`" % marca)
    assert "12:3x" in doc and "03:2x" in doc, (
        "as duas notas irmas — o vazio CAMUFLADO e o `quadro` jogado fora —"
        " sao o que situa este defeito na familia")
