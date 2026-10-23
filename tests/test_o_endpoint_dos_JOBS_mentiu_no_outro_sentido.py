# -*- coding: utf-8 -*-
"""O endpoint dos JOBS mentiu no OUTRO sentido — 22/10 as 19:4x.

Em 13:4x o RUN disse `completed/success` com o job `produzir` ainda
`in_progress`, e a regra que saiu daquela medicao foi *"espere pelos JOBS, nao
pelo RUN"*. **Nesta rodada foi o endpoint dos JOBS que mentiu:** o `retomar`
publicou as 19:20:07, o run voltou `completed/success`, o artefato existia — e
`/actions/runs/<id>/jobs` devolveu `in_progress`/`conclusion: null` por vinte e
cinco minutos.

Logo os dois endpoints discordam nos DOIS sentidos e **nenhum campo de status e
autoridade sozinho**. O discriminador estava dentro do MESMO payload: o `/jobs`
traz `steps` por job, e os quinze passos estavam concluidos.

A FORMA DOS TESTES: o caso MEDIDO e reproduzido, a contraprova vai nos DOIS
sentidos, o ramo de passo ausente devolve `None` (vazio nao e ausencia — 17/10),
a frase tem UM dono e sai nos DOIS ramos, e a retratacao tem de continuar
escrita no modulo.
"""
import ast
import inspect
import os
import sys
import textwrap

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR   # noqa: E402


def _passos(n, concluidos):
    return [{"number": i + 1,
             "status": "completed" if i < concluidos else "in_progress",
             "conclusion": "success" if i < concluidos else None}
            for i in range(n)]


# O CASO MEDIDO em 22/10 as 19:4x: o job do `retomar` com os quinze passos
# concluidos e `conclusion` nulo. O id vai como HISTORIA e nenhum assert
# depende dele (743/753/761).
JOB_DE_19H = {"id": 120035190237, "name": "retomar",
              "status": "in_progress", "conclusion": None,
              "steps": _passos(15, 15)}


def test_o_caso_MEDIDO_sai_TERMINADO_pelos_passos():
    q = AR.terminou([JOB_DE_19H])
    j = q["jobs"][0]
    assert j["terminado"] is True, (
        "o job com os quinze passos concluidos tem de sair TERMINADO: esperar "
        "o campo `conclusion` custou 25 minutos com a peca ja publicada")
    assert j["por_passo"] is True and j["por_campo"] is False
    assert q["pendentes"] == 0
    assert q["todos_terminaram"] is True
    assert q["divergem"] == 1
    assert q["motivo"] and "passos" in q["motivo"], (
        "a divergencia tem de sair NOMEADA: esconde-la faz a rodada seguinte "
        "esperar o campo que nao vem")


def test_a_contraprova_no_OUTRO_sentido_job_de_verdade_pendente():
    """Sem este teste bastaria devolver sempre TERMINADO."""
    meio = {"id": 1, "name": "produzir", "status": "in_progress",
            "conclusion": None, "steps": _passos(10, 4)}
    q = AR.terminou([meio])
    j = q["jobs"][0]
    assert j["terminado"] is False, (
        "job com 4 de 10 passos esta rodando de verdade e nao pode sair "
        "terminado")
    assert q["pendentes"] == 1
    assert q["todos_terminaram"] is False
    assert q["divergem"] == 0
    assert not q["motivo"]


def test_o_campo_SOZINHO_ainda_basta_quando_ele_chega():
    """O caso normal: `conclusion` preenchido decide sem olhar passo."""
    ok = {"id": 2, "name": "preparar", "status": "completed",
          "conclusion": "success", "steps": _passos(5, 5)}
    sem_passo = {"id": 3, "name": "preparar", "status": "completed",
                 "conclusion": "success", "steps": []}
    q = AR.terminou([ok, sem_passo])
    assert q["jobs"][0]["terminado"] is True
    assert q["jobs"][1]["terminado"] is None, (
        "sem passo visivel ele NAO decide, mesmo com o campo preenchido — "
        "passo ausente e vazio de instrumento, nao ausencia (17/10)")


def test_passo_NENHUM_visivel_nao_decide():
    cru = {"id": 4, "name": "x", "status": "queued", "conclusion": None,
           "steps": []}
    q = AR.terminou([cru])
    assert q["jobs"][0]["terminado"] is None, (
        "job sem passo visivel tambem nao tem passo concluido, e chamar isso "
        "de terminado seria ler vazio como ausencia")
    assert q["pendentes"] == 1


def test_lista_VAZIA_nao_diz_que_todos_terminaram():
    q = AR.terminou([])
    assert q["n"] == 0
    assert q["todos_terminaram"] is False, (
        "zero job nao e 'todos terminaram' — e a vacuidade do `or True`")


def test_ele_aceita_o_PAYLOAD_do_endpoint_e_nao_so_a_lista():
    payload = {"total_count": 1, "jobs": [JOB_DE_19H]}
    a = AR.terminou(payload)
    b = AR.terminou([JOB_DE_19H])
    assert a["jobs"][0]["terminado"] == b["jobs"][0]["terminado"]
    assert a["divergem"] == b["divergem"]


def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos():
    com = AR.relato_do_termino([JOB_DE_19H])
    sem = AR.relato_do_termino([{"id": 9, "name": "y", "status": "completed",
                                 "conclusion": "success",
                                 "steps": _passos(3, 3)}])
    assert "TERMINO DO RUN" in com and "TERMINO DO RUN" in sem
    assert "passos sao a medida" in com or "passos" in com
    assert "DOIS sentidos" in sem, (
        "no ramo sem divergencia a frase tem de dizer que os dois campos "
        "discordam nos DOIS sentidos — senao a leitura confortavel volta")
    fonte = textwrap.dedent(inspect.getsource(AR))
    marca = "TERMINO DO RUN"
    assert fonte.count(marca) == 1, (
        "a frase tem UM dono — %d ocorrencia(s)" % fonte.count(marca))


def test_ele_NAO_toca_a_rede_por_AST():
    """Se custasse requisicao, ninguem o chamaria dentro de um laco de espera."""
    corpo = ast.parse(textwrap.dedent(inspect.getsource(AR.terminou)))
    nomes = set()
    for n in ast.walk(corpo):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
    for proibido in ("_api", "leitura", "urlopen", "run", "check_output"):
        assert proibido not in nomes, (
            "`terminou` chama %r: ele decide sobre o payload que o chamador ja "
            "tem, e tocar a rede o tornaria caro de chamar em laco" % proibido)


def test_a_RETRATACAO_continua_escrita_no_modulo():
    doc = AR.terminou.__doc__ or ""
    for pedaco in ("13:4x", "DOIS sentidos", "RETRATADA", "steps"):
        assert pedaco in doc, (
            "o docstring perdeu %r: retratacao sem motivo escrito volta "
            "calada, e esta corrige uma regra de nove horas antes" % pedaco)


def test_o_CLI_chama_a_frase_senao_ela_e_layout_morto():
    """Import sem chamada e a classe dos layouts mortos (19/10, 04:2x)."""
    corpo = ast.parse(textwrap.dedent(inspect.getsource(AR.main)))
    nomes = set()
    for n in ast.walk(corpo):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
    assert "relato_do_termino" in nomes, (
        "o `main` nao chama a frase do termino: codigo que ninguem chama "
        "PARECE pronto e nao esta no ar")


# --------------------------------------------------------------------------
# E O `todos_terminaram` SAIA TRUE SOBRE UMA LISTA AINDA SENDO POVOADA.
#
# MEDIDO em 23/10 as 00:1x: o laco de espera perguntou pelo run 39876950273
# antes de a matriz existir. Havia UM job (`preparar`, concluido), logo
# `pendentes` era zero e `todos_terminaram` saiu True com o `produzir` ainda
# por criar. O que me salvou foi a guarda de 22/10 as 05:3x, que RECUSOU
# estabelecer o provedor por vacuidade — nao este campo.
# --------------------------------------------------------------------------

JOB_FEITO = {"id": 1, "name": "preparar", "status": "completed",
             "conclusion": "success",
             "steps": [{"name": "a", "conclusion": "success"}]}
JOB_ANDANDO = {"id": 2, "name": "produzir (x)", "status": "in_progress",
               "conclusion": None,
               "steps": [{"name": "a", "conclusion": "success"},
                         {"name": "b", "conclusion": None}]}


def test_o_caso_MEDIDO_sai_INDETERMINADO_e_nao_True():
    """A lista com um job feito, e o RUN ainda em andamento."""
    q = AR.terminou([JOB_FEITO], status_do_run="in_progress")
    assert q["pendentes"] == 0
    assert q["todos_terminaram"] is None, q["todos_terminaram"]
    assert q["run_aberto"] is True


def test_contraprova_com_o_RUN_completed_ele_decide():
    """Sem este par bastaria devolver sempre None."""
    q = AR.terminou([JOB_FEITO], status_do_run="completed")
    assert q["todos_terminaram"] is True
    q2 = AR.terminou([JOB_FEITO, JOB_ANDANDO], status_do_run="completed")
    assert q2["todos_terminaram"] is False, (
        "run `completed` com job em andamento e o caso de 19/4x: os passos "
        "mandam, e aqui eles dizem que falta")


def test_sem_o_argumento_ele_se_comporta_como_antes():
    """O payload dos jobs nao traz o status do run, e inventar um padrao faria
    a recusa depender de quem chamou lembrar de passa-lo."""
    q = AR.terminou([JOB_FEITO])
    assert q["todos_terminaram"] is True
    assert q["run_aberto"] is False
    assert q["status_do_run"] is None


def test_os_DOIS_campos_sao_necessarios_e_nenhum_basta():
    """O run pode adiantar (13:4x) e o job pode atrasar (19:4x)."""
    # job com TODOS os passos feitos e `conclusion` nulo, run completed
    atrasado = dict(JOB_ANDANDO)
    atrasado["steps"] = [{"name": "a", "conclusion": "success"},
                         {"name": "b", "conclusion": "success"}]
    q = AR.terminou([atrasado], status_do_run="completed")
    assert q["todos_terminaram"] is True and q["divergem"] == 1
    # os mesmos passos feitos, mas o run ainda aberto: INDETERMINADO
    q2 = AR.terminou([atrasado], status_do_run="queued")
    assert q2["todos_terminaram"] is None


def test_a_PRIMEIRA_linha_do_relato_carrega_o_VEREDITO():
    """O laco de espera grepava `0 pendente`, e essa contagem E zero no caso
    medido. O campo que decide tem de sair em letra."""
    r = AR.relato_do_termino([JOB_FEITO], "in_progress")
    primeira = r.splitlines()[0]
    assert "TERMINOU: INDETERMINADO" in primeira, primeira
    assert "0 pendente" in primeira, (
        "a contagem continua saindo — o que muda e que ela nao decide")
    assert "POVOADA" in r, r
    ok = AR.relato_do_termino([JOB_FEITO], "completed")
    assert "TERMINOU: SIM" in ok.splitlines()[0]
    assert "POVOADA" not in ok, (
        "o aviso da lista sendo povoada nao pode sair quando o run fechou")


def test_o_CLI_passa_o_status_do_run_por_AST():
    """Conserto no modulo nao protege contra a INVOCACAO: sem o chamador
    passar o status, o campo volta a ser o de antes."""
    import ast
    import inspect
    import textwrap
    fonte = textwrap.dedent(inspect.getsource(AR.main))
    arv = ast.parse(fonte)
    chamadas = [n for n in ast.walk(arv)
                if isinstance(n, ast.Call)
                and ast.unparse(n.func) == "relato_do_termino"]
    assert chamadas, "o CLI deixou de chamar o relato do termino"
    assert all(len(c.args) >= 2 for c in chamadas), (
        "o `relato_do_termino` esta sendo chamado sem o status do run")
    assert "actions/runs/%s" % "" in fonte or "actions/runs/" in fonte
