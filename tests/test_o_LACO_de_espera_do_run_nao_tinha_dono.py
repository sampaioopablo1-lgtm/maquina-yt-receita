# -*- coding: utf-8 -*-
"""O laco de espera do run falhou TRES vezes por INVOCACAO — 23/10 as 01:3x.

O `terminou` ja decide se um run acabou; o que nao tinha dono era o LACO que
pergunta a ele, e eu o redigitava a cada rodada. As tres falhas medidas estao
no docstring do modulo: o `pgrep` que se via no espelho, o `until` sem o `!` e
o `grep -q '0 pendente'` que saiu com a matriz ainda por criar — este ultimo na
MESMA rodada em que eu escrevi o `until` sem `sleep`.

A forma dos testes:
  * a decisao e cobrada como saindo do ESTADO, por **AST**: `relato_do_termino`
    e qualquer casamento de texto dentro do `espera` REPROVAM, porque veredito
    tirado da propria saida impressa e o defeito de 19/10 as 17:2x;
  * INDETERMINADO **nao** encerra a espera, e ha contraproba no outro sentido
    (SIM encerra) — sem ela bastaria nunca parar;
  * o TETO e cobrado com um run que nunca termina, e ele e **enforced**: o laco
    para e devolve `desistiu`, em vez de girar. A FRONTEIRA vai nos dois lados;
  * a dormida e cobrada como > 0 e como CHAMADA entre consultas, porque laco
    sem dormida e laco ocupado;
  * o codigo de saida sai do veredito, nos DOIS sentidos.
"""

import ast
import inspect
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR  # noqa: E402
import espera_do_run as E  # noqa: E402


# ---------------------------------------------------------------- fixtures

def _passos(n_feitos, n_total):
    return [{"status": "completed", "conclusion": "success"} for _ in range(n_feitos)] + \
           [{"status": "in_progress", "conclusion": None} for _ in range(n_total - n_feitos)]


def _jobs(*specs):
    """specs: (nome, feitos, total, conclusion)"""
    return {"jobs": [{"id": 100 + i, "name": n, "conclusion": c,
                      "steps": _passos(f, t)}
                     for i, (n, f, t, c) in enumerate(specs)]}


def _api_de(roteiro):
    """Devolve um `api` falso que serve um par (jobs, status) por consulta.

    O roteiro e uma lista de (jobs, status_do_run); a ultima entrada repete,
    para o caso do run que nunca termina.
    """
    estado = {"i": 0}

    def api(caminho):
        i = min(estado["i"], len(roteiro) - 1)
        jobs, status = roteiro[i]
        if caminho.endswith("/jobs"):
            return jobs
        estado["i"] += 1
        return {"status": status}

    return api


def _relogio():
    """Relogio FALSO que anda com as dormidas — o teste nao dorme de verdade."""
    t = {"s": 0.0}
    return t, (lambda: t["s"]), (lambda d: t.__setitem__("s", t["s"] + d))


# ---------------------------------------------------------------- o defeito

def test_INDETERMINADO_nao_encerra_a_espera():
    """O defeito de 23/10 as 00:07: run ABERTO com zero pendente nao e 'terminou'.

    Primeira consulta: um job so, concluido, e o run ainda `in_progress` — a
    lista esta sendo POVOADA. Se o laco sair aqui, ele sai antes de o job do
    render existir, que foi exatamente o que aconteceu.
    """
    roteiro = [
        (_jobs(("preparar", 5, 5, "success")), "in_progress"),
        (_jobs(("preparar", 5, 5, "success"), ("produzir", 19, 19, "success")), "completed"),
    ]
    t, agora, dorme = _relogio()
    q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora, intervalo_s=1.0)
    assert q["todos_terminaram"] is True
    assert q["polls"] >= 2, (
        "o laco saiu na PRIMEIRA consulta, em que o veredito era INDETERMINADO — "
        "e o defeito de 23/10 as 00:07 de volta"
    )


def test_a_PRIMEIRA_consulta_sozinha_sai_INDETERMINADO():
    """Sem este par, 'INDETERMINADO nao encerra' nao mede nada.

    Ele prova que o estado que o teste acima atravessa e de fato INDETERMINADO
    pelo DONO do veredito, nao por construcao do laco.
    """
    jobs = _jobs(("preparar", 5, 5, "success"))
    assert AR.terminou(jobs, "in_progress")["todos_terminaram"] is None


def test_terminado_de_primeira_encerra_na_PRIMEIRA_consulta():
    """Contraproba no outro sentido: senao bastaria nunca parar."""
    roteiro = [(_jobs(("preparar", 5, 5, "success"), ("produzir", 19, 19, "success")),
                "completed")]
    t, agora, dorme = _relogio()
    q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora, intervalo_s=1.0)
    assert q["todos_terminaram"] is True
    assert q["polls"] == 1
    assert q["desistiu"] is False


# ---------------------------------------------------------------- o teto

def test_run_que_NUNCA_termina_desiste_no_teto():
    """O laco PARA. Girar para sempre foi o defeito de 20/10 as 01:4x."""
    roteiro = [(_jobs(("produzir", 3, 19, None)), "in_progress")]
    t, agora, dorme = _relogio()
    q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora,
                 intervalo_s=10.0, limite_s=100.0)
    assert q["desistiu"] is True
    assert q["todos_terminaram"] is not True
    assert q["esperou_s"] >= 100.0
    assert q["polls"] >= 2


def test_o_teto_e_cobrado_na_FRONTEIRA_nos_dois_lados():
    """Teto que nao e respeitado nao e teto; teto que corta antes some com a espera."""
    roteiro = [(_jobs(("produzir", 3, 19, None)), "in_progress")]
    for limite, maximo in ((0.0, 1), (10.0, 2)):
        t, agora, dorme = _relogio()
        q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora,
                     intervalo_s=10.0, limite_s=limite)
        assert q["desistiu"] is True
        assert q["polls"] == maximo, (
            "com teto %r eu esperava %d consulta(s) e vieram %d" % (limite, maximo, q["polls"])
        )


def test_desistir_NAO_e_terminar():
    """O rotulo do relato tem de distinguir os dois, senao desistir passa por pronto."""
    roteiro = [(_jobs(("produzir", 3, 19, None)), "in_progress")]
    t, agora, dorme = _relogio()
    q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora,
                 intervalo_s=10.0, limite_s=10.0)
    r = E.relato_da_espera(q)
    assert "DESISTIU" in r
    assert "TERMINOU: SIM" not in r


# ---------------------------------------------------------------- a dormida

def test_ele_DORME_entre_as_consultas():
    """Laco sem dormida e laco OCUPADO — 23/10 as 00:07, dois deles girando."""
    vistos = []
    roteiro = [
        (_jobs(("produzir", 3, 19, None)), "in_progress"),
        (_jobs(("produzir", 19, 19, "success")), "completed"),
    ]
    t, agora, _ = _relogio()

    def dorme(d):
        vistos.append(d)
        t["s"] += d

    q = E.espera("1", api=_api_de(roteiro), dorme=dorme, agora=agora, intervalo_s=7.0)
    assert q["todos_terminaram"] is True
    assert vistos == [7.0], "esperava UMA dormida de 7 s entre as duas consultas, vi %r" % vistos


def test_intervalo_zero_LEVANTA():
    with pytest.raises(ValueError) as e:
        E.espera("1", api=_api_de([(_jobs(("p", 1, 1, "success")), "completed")]),
                 intervalo_s=0.0)
    assert "OCUPADO" in str(e.value)


def test_o_intervalo_padrao_e_positivo():
    assert E.INTERVALO_S > 0
    assert E.LIMITE_S > E.INTERVALO_S


# ------------------------------------------------- a decisao sai do ESTADO

def _corpo(fn):
    import textwrap
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def test_a_decisao_sai_do_ESTADO_e_nao_do_TEXTO():
    """Por AST: o `espera` nao pode chamar o relato nem casar texto.

    Veredito tirado da propria saida impressa e o defeito de 19/10 as 17:2x, e
    o laco que eu digitei em 00:07 fazia exatamente isso com um `grep`.
    """
    arvore = _corpo(E.espera)
    chamadas = [n.func.attr for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]
    chamadas += [n.func.id for n in ast.walk(arvore)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    for proibida in ("relato_do_termino", "relato_da_espera", "relato"):
        assert proibida not in chamadas, (
            "o `espera` chama %r: a decisao voltou a sair do TEXTO" % proibida
        )
    # nenhum casamento de texto: `in` sobre string, `find`, `startswith`, regex
    for n in ast.walk(arvore):
        if isinstance(n, ast.Compare):
            for op in n.ops:
                assert not isinstance(op, (ast.In, ast.NotIn)) or not any(
                    isinstance(c, ast.Constant) and isinstance(c.value, str)
                    for c in (n.left,)
                ), "o `espera` casa texto; a decisao tem de sair do estado"
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            assert n.func.attr not in ("find", "startswith", "search", "match"), (
                "casamento de texto dentro do `espera`: %s" % n.func.attr
            )


def test_o_veredito_e_DELEGADO_ao_dono():
    """Refazer a conta dos passos aqui criaria o SEGUNDO dono do veredito."""
    arvore = _corpo(E.veredito)
    atribs = [n.func.attr for n in ast.walk(arvore)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)]
    assert "terminou" in atribs, "o `veredito` tem de CHAMAR o `anotacoes_do_run.terminou`"
    fonte = inspect.getsource(E)
    assert "steps" not in fonte, (
        "este modulo le `steps` por conta propria: o dono dessa leitura e o "
        "`anotacoes_do_run.terminou`"
    )


def test_os_DOIS_campos_vao_ao_dono():
    """Sem o status do RUN o `terminou` sai True sobre lista povoada (00:1x)."""
    pedidos = []
    roteiro = [(_jobs(("p", 1, 1, "success")), "completed")]
    api = _api_de(roteiro)

    def espiao(caminho):
        pedidos.append(caminho)
        return api(caminho)

    E.veredito("1", api=espiao)
    assert any(c.endswith("/jobs") for c in pedidos)
    assert any(not c.endswith("/jobs") for c in pedidos), (
        "o status do RUN nao foi pedido: sem ele o veredito volta a mentir no "
        "sentido do 00:1x"
    )


def test_sem_run_LEVANTA():
    for ruim in (None, "", "   "):
        with pytest.raises(ValueError):
            E.veredito(ruim)


# ---------------------------------------------------------------- a saida

def test_o_codigo_de_saida_sai_do_VEREDITO_nos_dois_sentidos(monkeypatch, capsys):
    """Saida 0 so quando o veredito e SIM — e 1 quando ele desiste.

    O `veredito` e trocado por um fixo e o TETO vai a zero: assim o `main`
    roda o `espera` DE VERDADE, numa consulta e sem dormir, e o que se mede e
    o codigo de saida contra o estado.
    """
    monkeypatch.setattr(E, "LIMITE_S", 0.0)

    for estado, esperado in ((True, 0), (False, 1), (None, 1)):
        monkeypatch.setattr(
            E, "veredito",
            lambda run, api=None, _e=estado: {"todos_terminaram": _e, "pendentes": 0,
                                              "jobs": 1, "status_do_run": "x",
                                              "run_aberto": False})
        assert E.main(["1"]) == esperado, (
            "estado %r devia dar codigo %d" % (estado, esperado))
        saida = capsys.readouterr().out
        assert "ESPERA DO RUN" in saida


def test_o_motivo_das_TRES_falhas_continua_escrito():
    """Conserto sem motivo escrito volta calado — e este voltou tres vezes."""
    fonte = inspect.getsource(E)
    for marca in ("pgrep", "0 pendente", "OCUPADO", "invocacao"):
        assert marca in fonte, "a licao %r saiu do modulo" % marca


def test_o_TETO_nao_depende_do_RELOGIO_sozinho():
    """A contraproba desta rodada: sem a dormida, teto por tempo nao termina.

    Com o relogio injetado, quem fazia o tempo andar era a propria dormida —
    logo retirar a dormida nao REPROVAVA o teste, girava para sempre. Teto que
    depende da dormida que ele deveria tornar desnecessaria nao e teto, e vazio
    de instrumento nao prova ausencia (17/10): aqui o teste nem chegava a
    falhar. O teto conta tambem CONSULTAS.
    """
    roteiro = [(_jobs(("produzir", 3, 19, None)), "in_progress")]
    parado = lambda: 0.0  # relogio que NAO anda, como se ninguem dormisse
    q = E.espera("1", api=_api_de(roteiro), dorme=lambda d: None, agora=parado,
                 intervalo_s=10.0, limite_s=100.0)
    assert q["desistiu"] is True, "sem o relogio andar, o laco nao terminou"
    assert q["polls"] == q["limite_polls"]
    assert q["esperou_s"] == 0.0, (
        "o relogio nao andou e ele parou de todo modo: quem o parou foi a "
        "contagem de consultas, nao o tempo"
    )
