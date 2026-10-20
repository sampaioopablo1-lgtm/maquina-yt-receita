"""O `pgrep -f` se via no espelho, e eu reportei "VIVO" tres vezes.

Guarda o defeito de 20/10 as 01:4x e o discriminador que o desfaz. A forma e a
da semana: contraprova nos DOIS sentidos (processo real diz VIVO, espelho de
shell NAO conta), o criterio por AST, e um teste que falha se o MOTIVO sair do
modulo — conserto sem motivo escrito volta calado.
"""
import ast
import os
import subprocess
import sys
import time

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import processo_vivo as PV   # noqa: E402

MOD = os.path.join(RAIZ, "fabrica", "processo_vivo.py")
MARCA = "MARCA_DO_TESTE_processo_vivo_20251020"


@pytest.fixture
def python_rodando():
    """Um python de verdade, com a MARCA nos argumentos."""
    # O prefixo longo e DELIBERADO: ele empurra a marca para depois da
    # largura em que o `ps` cortava, que e o defeito que o teste do
    # truncamento mede.
    prefixo = "# " + ("x" * 70)
    p = subprocess.Popen([sys.executable, "-c",
                          f"import time  {prefixo}\n_ = {MARCA!r}\n"
                          f"time.sleep(30)"])
    for _ in range(50):
        if PV.candidatos(MARCA):
            break
        time.sleep(0.1)
    yield p
    p.kill()
    p.wait(timeout=10)


@pytest.fixture
def shell_que_se_ve():
    """Um laco de shell cuja PROPRIA linha de comando contem a MARCA.

    E este o espelho: foi um laco assim que devolveu quatro PIDs ao `pgrep` e
    me fez reportar "VIVO" com a suite encerrada.
    """
    p = subprocess.Popen(
        ["bash", "-c", f'until false; do sleep 1; done # {MARCA}'])
    for _ in range(50):
        if any(MARCA in x["args"] for x in PV.espelhos(MARCA)):
            break
        time.sleep(0.1)
    yield p
    p.kill()
    p.wait(timeout=10)


def test_processo_python_de_verdade_diz_VIVO(python_rodando):
    assert PV.vivo(MARCA) is True
    c = PV.candidatos(MARCA)
    assert c and all("python" in x["comm"] for x in c)


def test_o_ESPELHO_de_shell_NAO_conta_como_vivo(shell_que_se_ve):
    """O defeito, cobrado onde ele morava."""
    assert PV.vivo(MARCA) is False, (
        "um laco de shell que cita o padrao na propria linha de comando foi "
        "contado como o processo — e era exactamente esse o defeito de 20/10"
    )
    e = PV.espelhos(MARCA)
    assert any(MARCA in x["args"] for x in e), (
        "o instrumento tem de NOMEAR o espelho, nao so o descartar: foi "
        "vendo os PIDs de shell que eu descobri o engano"
    )


def test_o_pgrep_CRU_erraria_no_mesmo_caso(shell_que_se_ve):
    """Contraprova pela ferramenta antiga: sem isto, 'o pgrep errava' e
    afirmacao minha e nao medida."""
    r = subprocess.run(["pgrep", "-f", MARCA], capture_output=True, text=True)
    pids = [x for x in r.stdout.split() if x]
    assert pids, (
        "o `pgrep -f` NAO devolveu o espelho — se ele parou de casar a linha "
        "de comando de shell, este arquivo perde o objeto e a nota se rele"
    )
    assert PV.vivo(MARCA) is False, "e o instrumento novo tem de discordar dele"


def test_a_PROPRIA_chamada_sai_fora(python_rodando):
    """O pid deste pytest cita 'pytest tests'? Entao ele nao pode se contar."""
    meus = {os.getpid(), os.getppid()}
    for x in PV.candidatos(MARCA) + PV.espelhos(MARCA):
        assert x["pid"] not in meus, (
            "a propria chamada apareceu na resposta — e por aqui que o "
            "`pgrep` se via no espelho"
        )


def test_tabela_vazia_LEVANTA(monkeypatch):
    """Ausencia de leitura nao e 'nada rodando'."""
    monkeypatch.setattr(PV.os, "listdir", lambda *a, **k: [])
    with pytest.raises(RuntimeError, match="AUSENCIA DE LEITURA"):
        PV._tabela()


def test_a_leitura_NAO_e_TRUNCADA(python_rodando):
    """O segundo defeito desta rodada, cobrado onde ele morava.

    O `ps` corta a coluna `args` na largura do terminal, e sob pytest nao ha
    tty: ele cortava em 58 caracteres e a marca morava DEPOIS do corte, logo
    o instrumento dizia "nao achei" com o processo VIVO na frente dele. Este
    teste exige que a leitura alcance o padrao independentemente de ONDE ele
    cai na linha de comando — e e por isso que a fixture poe a marca depois de
    um prefixo longo.
    """
    c = PV.candidatos(MARCA)
    assert c, "o processo existe e nao foi achado"
    args = c[0]["args"]
    assert args.index(MARCA) > 60, (
        "a marca precisa cair DEPOIS da largura em que o `ps` cortava, senao "
        "este teste passa sem medir o truncamento"
    )
    assert len(args) > len(MARCA) + 60


def test_a_fonte_e_o_proc_e_nao_o_ps_por_AST():
    """Por AST, porque o modulo CITA o `ps` na prosa que explica o defeito."""
    arv = ast.parse(open(MOD, encoding="utf-8").read())
    fn = next(n for n in ast.walk(arv)
              if isinstance(n, ast.FunctionDef) and n.name == "_tabela")
    textos = [n.value for n in ast.walk(fn)
              if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    assert any("/proc" in x for x in textos), (
        "a tabela tem de sair do /proc, que nao tem largura"
    )
    for n in ast.walk(fn):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "run"):
            pytest.fail(
                "o `_tabela` voltou a chamar um processo externo — foi o "
                "truncamento do `ps` que escondeu o processo vivo"
            )


def test_o_criterio_e_o_EXECUTAVEL_por_AST():
    """O docstring explica o `-f` em prosa, logo casar prosa pegaria a
    explicacao em vez do codigo."""
    arv = ast.parse(open(MOD, encoding="utf-8").read())
    fn = next(n for n in ast.walk(arv)
              if isinstance(n, ast.FunctionDef) and n.name == "candidatos")
    corpo = ast.dump(fn)
    assert "executavel" in corpo and "comm" in corpo, (
        "o filtro de `candidatos` tem de olhar o EXECUTAVEL (`comm`), nao "
        "apenas os argumentos — era isso que faltava ao `pgrep -f`"
    )
    # e nenhum nome do que eu ESPERO pode estar cravado: seria identidade
    # onde ha propriedade (743/753/761).
    for n in ast.walk(fn):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            assert "pytest" not in n.value, (
                "o nome do processo esperado foi cravado dentro do filtro — "
                "o instrumento tem de valer para qualquer padrao"
            )


def test_a_lista_do_que_NAO_e_o_processo_e_de_shells_e_buscas():
    """Ela e propriedade ('nao e o interpretador'), nao lista do esperado."""
    assert "bash" in PV.NAO_SAO_O_PROCESSO
    assert "pgrep" in PV.NAO_SAO_O_PROCESSO
    assert not any("pytest" in n or "python" in n
                   for n in PV.NAO_SAO_O_PROCESSO)


def test_o_codigo_de_saida_serve_ao_until():
    """Ele existe para morar dentro de `until`, logo 0 = vivo e 1 = nao."""
    r = subprocess.run([sys.executable, MOD, "PADRAO_QUE_NAO_EXISTE_EM_LUGAR"],
                       capture_output=True, text=True, cwd=RAIZ, timeout=60)
    assert r.returncode == 1 and "NAO" in r.stdout


def test_o_MOTIVO_continua_escrito_no_modulo():
    """Conserto sem motivo escrito volta calado — e este voltou duas vezes."""
    t = open(MOD, encoding="utf-8").read()
    for frase in ("pgrep", "linha de comando", "16:2x", "CHEIO nao prova"):
        assert frase in t, (
            f"a frase {frase!r} saiu do modulo; sem ela a rodada seguinte "
            "reescreve o `until ! pgrep -f` que se ve no espelho"
        )
