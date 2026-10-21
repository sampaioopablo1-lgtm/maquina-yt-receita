# -*- coding: utf-8 -*-
"""A fatia da lista do proxy lia a ponta VELHA — 21/10 as 19:2x.

O quinto modo da rota (`negado_por_politica`, medido em 20/10 as 11:4x) depende
de o PROXY nomear o host, e esse argumento eu vinha passando A MAO: um `curl
$HTTPS_PROXY/__agentproxy/status` com um `python3 -c` e uma FATIA escrita na
hora.

A lista `recentRelayFailures` e **OLDEST-FIRST** e truncada nas 20 ultimas, logo
`[:3]` le as MAIS VELHAS. As 18:20 isso acertou por sorte (o buffer estava curto
e as tres primeiras eram da propria sonda); as 19:08 devolveu tres `sb:443` de
18:43 — de outra rodada — e eu quase li isso como "o proxy nao nomeou o YouTube
nesta rodada", o que daria `sem_egresso` onde o modo e `negado_por_politica`.

Sao DOIS defeitos numa fatia so: a ponta errada da lista, e a ausencia de
INSTANTE — negacao de uma rodada anterior contando como medicao desta.
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import vivacidade_publica as VP   # noqa: E402

HOSTS = ["www.youtube.com", "example.com"]
DESDE = "2026-10-21T19:18:00Z"

# O STATUS MEDIDO em 21/10 as 19:18, com a ordem REAL da lista (oldest-first) e
# entradas de OUTRA rodada (18:43, 19:07) antes das desta.
STATUS = {"recentRelayFailures": [
    {"ts": "2026-10-21T18:43:18.124Z", "host": "sb:443",
     "kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT"},
    {"ts": "2026-10-21T19:07:19.443Z", "host": "www.youtube.com:443",
     "kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT"},
    {"ts": "2026-10-21T19:18:31.103Z", "host": "www.youtube.com:443",
     "kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT"},
    {"ts": "2026-10-21T19:18:31.765Z", "host": "example.com:443",
     "kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT"},
]}


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _funcao(nome):
    fonte = open(VP.__file__, encoding="utf-8").read()
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.FunctionDef) and no.name == nome:
            return no
    raise AssertionError("funcao %s nao existe" % nome)


def test_o_caso_MEDIDO_sai_NEGADO():
    r = VP.politica_negou_hosts(HOSTS, DESDE, status=STATUS)
    assert r["negou"] is True, r
    assert set(r["hosts_nomeados"]) == {"www.youtube.com", "example.com"}, r


def test_a_FATIA_do_comeco_leria_a_ponta_ERRADA():
    """Reproduz o defeito: sem a funcao, as tres primeiras nao nomeiam o alvo.

    Sem este teste, "eu errei a fatia" seria afirmacao minha e nao medida.
    """
    primeiras = [f["host"].split(":")[0]
                 for f in STATUS["recentRelayFailures"][:3]]
    assert "example.com" not in primeiras, (
        "a fixture deixou de reproduzir o defeito: a ponta velha ja nomeia o "
        "host neutro, e ai a fatia errada acertaria")
    ultimas = [f["host"].split(":")[0]
               for f in STATUS["recentRelayFailures"][-3:]]
    assert "example.com" in ultimas and "www.youtube.com" in ultimas, (
        "a ponta NOVA tem de nomear os dois — e ela que a funcao le")


def test_negacao_de_OUTRA_rodada_nao_conta_como_desta():
    """O segundo defeito da fatia: ela nao tinha INSTANTE."""
    r = VP.politica_negou_hosts(HOSTS, "2026-10-21T19:30:00Z", status=STATUS)
    assert r["negou"] is None, (
        "entrada de 19:18 contou para uma sonda de 19:30 — o `desde` nao "
        "esta sendo aplicado: %r" % r)
    so_velha = {"recentRelayFailures": STATUS["recentRelayFailures"][:1]}
    r2 = VP.politica_negou_hosts(HOSTS, DESDE, status=so_velha)
    assert r2["negou"] is None, (
        "a entrada `sb:443` de 18:43 virou negacao do YouTube desta rodada")


def test_AUSENCIA_de_entrada_nao_e_permissao():
    """A licao de 17/10: instrumento que devolve vazio nao prova ausencia."""
    r = VP.politica_negou_hosts(HOSTS, DESDE,
                                status={"recentRelayFailures": []})
    assert r["negou"] is None, (
        "lista vazia devolveu %r — e ela e TRUNCADA nas 20 ultimas, logo nao "
        "prova que a politica deixou passar" % r["negou"])
    assert "TRUNCADA" in r["motivo"] or "truncada" in r["motivo"], r["motivo"]


def test_falha_de_LEITURA_nao_vira_ausencia_de_NEGACAO():
    """Status ilegivel devolve None, nao `negou: False`."""
    r = VP.politica_negou_hosts(HOSTS, DESDE, status="nao sou dicionario")
    assert r["negou"] is None, r
    codigo = _codigo(_funcao("_status_do_proxy"))
    assert "return {}" not in codigo, (
        "o leitor devolve dicionario VAZIO em falha — ai falha de leitura "
        "passaria pela funcao acima como 'nenhuma falha listada'")
    assert "return None" in codigo, (
        "o leitor tem de devolver None em falha de leitura")


def test_entrada_que_NAO_e_recusa_de_CONNECT_nao_vira_politica():
    """Contraprova no outro sentido: sem ela bastaria nomear o host."""
    outro = {"recentRelayFailures": [
        {"ts": "2026-10-21T19:18:31.103Z", "host": "www.youtube.com:443",
         "kind": "upstream_timeout", "detail": "upstream took too long"}]}
    r = VP.politica_negou_hosts(HOSTS, DESDE, status=outro)
    assert r["negou"] is None, (
        "timeout de upstream virou negacao por POLITICA — os dois pedem "
        "remedios diferentes: %r" % r)
    assert r["hosts_nomeados"] == ["www.youtube.com"], r


def test_o_desde_e_OBRIGATORIO_na_assinatura():
    """Parametro com padrao voltaria a permitir medicao sem instante."""
    import inspect
    sig = inspect.signature(VP.politica_negou_hosts)
    p = sig.parameters["desde"]
    assert p.default is inspect.Parameter.empty, (
        "`desde` ganhou padrao — ai negacao de rodada anterior volta a contar")


def test_a_funcao_nao_fatia_pelo_COMECO():
    """Por AST: o docstring CITA `[:3]` para se explicar, e casar prosa pegaria
    a explicacao em vez do codigo."""
    codigo = _codigo(_funcao("politica_negou_hosts"))
    assert "[:3]" not in codigo and "[:1]" not in codigo, (
        "a funcao voltou a fatiar pelo comeco da lista: %s" % codigo[:200])


def test_o_modo_de_fechamento_CONSOME_isto_e_o_None_vira_indeterminado():
    r = VP.politica_negou_hosts(HOSTS, DESDE, status=STATUS)
    assert VP.modo_de_fechamento("", neutro_respondeu=False,
                                 sonda_pode_gravar=True,
                                 politica_negou=r["negou"]) == \
        "negado_por_politica"
    vazio = VP.politica_negou_hosts(HOSTS, DESDE,
                                    status={"recentRelayFailures": []})
    assert VP.modo_de_fechamento("", neutro_respondeu=False,
                                 sonda_pode_gravar=True,
                                 politica_negou=vazio["negou"]) == \
        "indeterminado", (
        "ausencia de entrada no proxy passou a escolher um modo em vez de "
        "recusar")


def test_o_CLI_existe_e_o_codigo_de_saida_e_ZERO():
    """Sem CLI a rodada reescreve a fatia na linha de comando — foi o defeito."""
    r = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
                        DESDE, "www.youtube.com"],
                       capture_output=True, text=True)
    assert r.returncode == 0, (
        "o CLI passou a reprovar (saida %d) — ele informa:\n%s"
        % (r.returncode, r.stdout + r.stderr))
    assert "POLITICA NEGOU" in r.stdout, r.stdout
    assert "OLDEST-FIRST" in r.stdout, (
        "o CLI nao diz a ordem da lista — e e a ordem que produziu o defeito")


def test_o_motivo_continua_escrito_no_modulo():
    fonte = open(VP.__file__, encoding="utf-8").read()
    for marca in ("OLDEST-FIRST", "19:0x", "sb:443", "truncada"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo — sem ela a rodada seguinte "
            "reescreve a fatia" % marca)
