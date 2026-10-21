# -*- coding: utf-8 -*-
"""A comparacao da suite lia ARQUIVO DE OUTRA SESSAO — 21/10 as 21:0x.

Eu comparo a passada contra a linha de base desta sessao com `comm`, e o `.norm`
e escrito DEPOIS de o pytest sair. Logo "o arquivo existe" foi, por semanas, o
meu discriminador de "a passada terminou".

NESTA RODADA ELE MENTIU: havia um `.norm` de 20/10 as 20:42 — resto da sessao
anterior, com o MESMO nome —, a suite estava em 43%, e o `comm` devolveu
"identico a base". Quem me pegou foi o `processo_vivo`, respondendo VIVO.

E a familia e a de 17/10 / 19/10 / 20/10 na forma mais caustica: as outras
devolvem silencio ou erro, e esta devolve a resposta CONFORTAVEL.
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import passada_da_suite as PS   # noqa: E402

RESUMO = "25 failed, 3654 passed, 1132 skipped in 1275.91s (0:21:15)\n"
EM_43 = ("........................................................ [ 41%]\n"
         "........................................................ [ 43%]\n"
         "..........")
FALHAS = ["FAILED tests/test_a.py::test_um", "FAILED tests/test_b.py::test_dois"]


def _escreve(tmp, nome, texto, idade=None):
    p = os.path.join(str(tmp), nome)
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto)
    if idade is not None:
        os.utime(p, (idade, idade))
    return p


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def test_o_caso_MEDIDO_norm_de_outra_sessao_RECUSA(tmp_path):
    """O log em 43% e um `.norm` VELHO: era isto, e deu 'identico'."""
    log = _escreve(tmp_path, "p.log", EM_43, idade=2_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "\n".join(FALHAS) + "\n",
                    idade=1_000_000_000)
    base = _escreve(tmp_path, "base.norm", "\n".join(FALHAS) + "\n")
    c = PS.compara(base, log, norm)
    assert c["comparou"] is False, (
        "comparou com o log em 43%% e o `.norm` de outra sessao: %r" % c)
    r = PS.relato(base, log, norm)
    assert "NAO COMPARADA" in r, r
    # A AFIRMACAO de identidade tem UM dono e e a linha "conjunto IDENTICO".
    # A primeira versao deste assert proibia a palavra "identico" em qualquer
    # caixa, e a propria frase da RECUSA a cita para se explicar ("isto RECUSA
    # em vez de devolver 'identico a base'") — casar prosa pegou a explicacao
    # em vez do codigo, a licao do `test_NAO_virou_portao` do acento. Era o
    # teste errado, nao o modulo.
    assert "conjunto IDENTICO" not in r, (
        "o relato AFIRMA identidade numa passada que ele mesmo recusou:\n%s" % r)


def test_sem_a_linha_de_RESUMO_a_passada_nao_esta_provada(tmp_path):
    log = _escreve(tmp_path, "p.log", EM_43)
    norm = _escreve(tmp_path, "p.norm", "\n".join(FALHAS) + "\n")
    p = PS.passada_provada(log, norm)
    assert p["provada"] is False and p["resumo"] is None, p
    assert "resumo" in p["motivo"], p["motivo"]


def test_norm_MAIS_VELHO_que_o_log_nao_vale(tmp_path):
    log = _escreve(tmp_path, "p.log", RESUMO, idade=2_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "x\n" * 25, idade=1_000_000_000)
    p = PS.passada_provada(log, norm)
    assert p["provada"] is False, p
    assert "MAIS VELHO" in p["motivo"], p["motivo"]


def test_norm_mais_novo_mas_de_OUTRA_passada_nao_vale(tmp_path):
    """Terceiro discriminador: a contagem tem de BATER com o resumo.

    Sem ele bastaria tocar o arquivo para a comparacao passar.
    """
    log = _escreve(tmp_path, "p.log", RESUMO, idade=1_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "x\n" * 7, idade=2_000_000_000)
    p = PS.passada_provada(log, norm)
    assert p["provada"] is False, p
    assert "OUTRA passada" in p["motivo"], p["motivo"]


def test_a_passada_BOA_compara_e_diz_IDENTICO(tmp_path):
    """Contraprova no outro sentido: sem ela, recusar sempre passaria."""
    log = _escreve(tmp_path, "p.log",
                   "...\n2 failed, 10 passed, 3 skipped in 9.0s (0:00:09)\n",
                   idade=1_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "\n".join(FALHAS) + "\n",
                    idade=2_000_000_000)
    base = _escreve(tmp_path, "base.norm", "\n".join(FALHAS) + "\n")
    c = PS.compara(base, log, norm)
    assert c["comparou"] is True and c["identico"] is True, c
    assert c["resumo"]["falhas"] == 2, c
    assert "IDENTICO" in PS.relato(base, log, norm)


def test_ele_acusa_NOVAS_e_DESAPARECIDAS_nos_dois_sentidos(tmp_path):
    log = _escreve(tmp_path, "p.log",
                   "1 failed, 10 passed, 3 skipped in 9.0s (0:00:09)\n",
                   idade=1_000_000_000)
    norm = _escreve(tmp_path, "p.norm", FALHAS[1] + "\n", idade=2_000_000_000)
    base = _escreve(tmp_path, "base.norm", FALHAS[0] + "\n")
    c = PS.compara(base, log, norm)
    assert c["comparou"] is True, c
    assert c["novas"] == [FALHAS[1]], c
    assert c["desaparecidas"] == [FALHAS[0]], c
    r = PS.relato(base, log, norm)
    assert "NOVAS" in r and "DESAPARECIDAS" in r, r


def test_sem_a_BASE_desta_sessao_ele_RECUSA(tmp_path):
    """Comparar contra o numero ESCRITO na rotina e o que envelhece (753)."""
    log = _escreve(tmp_path, "p.log",
                   "2 failed, 10 passed, 3 skipped in 9.0s (0:00:09)\n",
                   idade=1_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "\n".join(FALHAS) + "\n",
                    idade=2_000_000_000)
    c = PS.compara(os.path.join(str(tmp_path), "nao-existe.norm"), log, norm)
    assert c["comparou"] is False, c
    assert "base" in c["motivo"], c["motivo"]


def test_o_resumo_sai_do_FIM_do_log_e_nao_do_comeco(tmp_path):
    """A fatia errada me custou a leitura do proxy em 21/10 as 19:0x.

    Um log com DUAS linhas de resumo (reexecucao no mesmo arquivo) tem de
    devolver a ULTIMA.
    """
    log = _escreve(tmp_path, "p.log",
                   "9 failed, 1 passed, 0 skipped in 1.0s\n"
                   "..\n"
                   "2 failed, 10 passed, 3 skipped in 9.0s\n")
    assert PS.resumo_do_log(log)["falhas"] == 2, PS.resumo_do_log(log)


def test_a_liveness_e_DELEGADA_ao_processo_vivo():
    """Foi ele que me pegou; reimplementar aqui criaria o segundo dono."""
    codigo = "\n".join(_codigo(n) for n in ast.walk(
        ast.parse(open(PS.__file__, encoding="utf-8").read()))
        if isinstance(n, ast.FunctionDef))
    assert "processo_vivo" in codigo, "a liveness deixou de ser delegada"
    for proibido in ("/proc/", "pgrep", "comm=", "subprocess.run(['ps'"):
        assert proibido not in codigo, (
            "o modulo reimplementa a deteccao de processo com %r" % proibido)


def test_os_TRES_discriminadores_existem_e_nenhum_basta(tmp_path):
    """Propriedade e nao contagem: cada um sozinho deixa passar um caso ruim."""
    base = _escreve(tmp_path, "base.norm", "\n".join(FALHAS) + "\n")
    casos = [
        (EM_43, "\n".join(FALHAS) + "\n", 1_000_000_000, 2_000_000_000),
        (RESUMO, "x\n" * 25, 2_000_000_000, 1_000_000_000),
        (RESUMO, "x\n" * 7, 1_000_000_000, 2_000_000_000),
    ]
    for i, (tlog, tnorm, ilog, inorm) in enumerate(casos):
        log = _escreve(tmp_path, "c%d.log" % i, tlog, idade=ilog)
        norm = _escreve(tmp_path, "c%d.norm" % i, tnorm, idade=inorm)
        assert PS.compara(base, log, norm)["comparou"] is False, (
            "o caso %d passou: um dos tres discriminadores nao esta ligado" % i)


def test_o_motivo_continua_escrito_no_modulo():
    fonte = open(PS.__file__, encoding="utf-8").read()
    for marca in ("20/10 as 20:42", "43%", "CONFORTAVEL", "processo_vivo"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo — sem ela a rodada seguinte volta "
            "a confiar na existencia do arquivo" % marca)


def test_o_CLI_existe_e_nao_reprova(tmp_path):
    log = _escreve(tmp_path, "p.log",
                   "2 failed, 10 passed, 3 skipped in 9.0s\n",
                   idade=1_000_000_000)
    norm = _escreve(tmp_path, "p.norm", "\n".join(FALHAS) + "\n",
                    idade=2_000_000_000)
    base = _escreve(tmp_path, "base.norm", "\n".join(FALHAS) + "\n")
    r = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "passada_da_suite.py"),
                        base, log, norm], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SUITE:" in r.stdout, r.stdout
