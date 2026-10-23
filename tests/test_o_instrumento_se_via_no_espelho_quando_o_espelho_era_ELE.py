# -*- coding: utf-8 -*-
"""O instrumento se via no espelho quando o espelho era ELE MESMO.

MEDIDO em 23/10 as 00:0x. O `processo_vivo` nasceu em 20/10 as 01:4x porque
o `pgrep -f` casava a propria linha de comando do laco de espera. Ele tirou
de fora o PID da chamada e o do pai dela — e uma SEGUNDA copia concorrente
do modulo tem outro PID, executavel `python3` e os argumentos com o padrao
dentro, logo passava todos os filtros e era contada como o PROCESSO.

No relato das 00:00, com a suite rodando, ele disse `VIVO: 2 processo(s)`:
o pytest e o observador do laco de espera, que era ele mesmo.

A falha e PERMISSIVA no sentido pior — dois observadores concorrentes veem
um ao outro e os dois dizem VIVO para sempre, que e o laco infinito do
`pgrep`. E o `NAO_SAO_O_PROCESSO` nao podia pega-la: ele casa o EXECUTAVEL,
e o executavel de uma copia deste modulo e `python3`.
"""
import ast
import inspect
import os
import subprocess
import sys
import textwrap
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
if FABRICA not in sys.path:
    sys.path.insert(0, FABRICA)

import processo_vivo as PV  # noqa: E402

PADRAO = "MARCA_DO_TESTE_DO_ESPELHO"


def _corpo(nome):
    return textwrap.dedent(inspect.getsource(getattr(PV, nome)))


def _espera(cond, limite=8.0):
    fim = time.time() + limite
    while time.time() < fim:
        if cond():
            return True
        time.sleep(0.1)
    return False


def test_uma_copia_do_modulo_NAO_e_o_processo():
    """O caso medido: outro processo python cujos ARGUMENTOS nomeiam este
    modulo e carregam o padrao procurado — que e o que uma segunda copia
    concorrente do `processo_vivo.py` e. A propriedade cobrada e essa, e nao
    a CLI dele dormir: o `main` sai na hora, de proposito."""
    p = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)",
         os.path.join(FABRICA, "processo_vivo.py"), PADRAO],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert _espera(lambda: any(
            str(pid) == str(p.pid) for pid, _c, a in PV._tabela()
            if PADRAO in (a or ""))), "o processo de prova nao subiu"
        assert PV.vivo(PADRAO) is False, (
            "uma copia do modulo foi contada como o processo")
        esp = PV.espelhos(PADRAO)
        assert any(str(e["pid"]) == str(p.pid) for e in esp), esp
        assert any("copia" in e["comm"] for e in esp), (
            "o espelho tem de ir NOMEADO, nao apenas descartado")
    finally:
        p.kill()
        p.wait()


def test_contraprova_um_python_de_VERDADE_continua_VIVO():
    """Sem este par, bastaria devolver sempre False."""
    p = subprocess.Popen(
        [sys.executable, "-c",
         "import time; _ = '%s'; time.sleep(30)" % PADRAO],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert _espera(lambda: PV.vivo(PADRAO) is True), (
            "python de verdade com o padrao tem de sair VIVO")
    finally:
        p.kill()
        p.wait()


def test_o_dono_do_sou_eu_e_UM_e_e_pelo_ARGUMENTO():
    """O `NAO_SAO_O_PROCESSO` casa o EXECUTAVEL e nao podia pegar isto."""
    assert PV.sou_eu("python3 /x/fabrica/processo_vivo.py algo") is True
    assert PV.sou_eu("python3 -m pytest tests -q") is False
    assert PV.sou_eu("") is False
    assert PV.sou_eu(None) is False
    # o `candidatos` CHAMA o dono, e nao refaz a conta
    fonte = _corpo("candidatos")
    arv = ast.parse(fonte)
    chamadas = {ast.unparse(n.func) for n in ast.walk(arv)
                if isinstance(n, ast.Call)}
    assert "sou_eu" in chamadas, chamadas
    assert "basename" not in fonte and "__file__" not in fonte, (
        "o nome do proprio arquivo tem UM dono")


def test_o_nome_do_modulo_NAO_esta_cravado_em_string():
    """753: o nome sai do `__file__`, senao renomear o arquivo o quebra em
    silencio."""
    inteiro = open(os.path.join(FABRICA, "processo_vivo.py"),
                   encoding="utf-8").read()
    arv = ast.parse(inteiro)
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and any(
                getattr(t, "id", "") == "EU" for t in n.targets):
            assert isinstance(n.value, ast.Call), ast.unparse(n.value)
            assert "__file__" in ast.unparse(n.value), ast.unparse(n.value)
            break
    else:
        raise AssertionError("a constante EU desapareceu")


def test_a_medida_e_o_motivo_continuam_escritos():
    inteiro = open(os.path.join(FABRICA, "processo_vivo.py"),
                   encoding="utf-8").read()
    for marca in ("VIVO: 2 processo(s)", "PERMISSIVA", "NAO_SAO_O_PROCESSO",
                  "EXECUTAVEL"):
        assert marca in inteiro, marca
