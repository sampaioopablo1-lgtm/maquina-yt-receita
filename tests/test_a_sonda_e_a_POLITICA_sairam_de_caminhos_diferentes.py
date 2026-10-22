# -*- coding: utf-8 -*-
"""A SONDA E A POLITICA SAIRAM DE CAMINHOS DE SAIDA DIFERENTES — 22/10, 00:3x.

O `modo_de_fechamento` recebe TRES controles como booleanos independentes e nao
tem nocao de ONDE cada um foi medido. Nesta rodada eu medi o 000 dos hosts no
sandbox do Composio (que **nao tem** `HTTPS_PROXY`: variavel VAZIA, medido) e li
a negacao de politica NESTE container (que tem). Os dois devolveram 000 com o
controle de escrita passando — e so aqui a negacao e atribuivel.

A sonda do sandbox daria `indeterminado`; a deste container deu
`negado_por_politica`. Nas vinte e uma rodadas anteriores eu reportei o segundo
tendo sondado no primeiro: acertei pelo acordo ACIDENTAL dos dois caminhos.

O que estes testes cobram e a PROPRIEDADE: quem junta os tres controles e UMA
funcao, no MESMO processo, e o caminho vai NOMEADO. O veredito segue do
`modo_de_fechamento`.
"""
import ast
import inspect
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import vivacidade_publica as VP  # noqa: E402

# Hosts do TLD reservado `.invalid`: nunca resolvem, logo a sonda falha na hora
# e sem rede. O teste mede a MONTAGEM dos controles, nao a rede.
HOSTS = ["youtube.invalid", "example.invalid"]
DESDE = "2026-10-22T00:00:00"

CONTROLES = ("neutro_respondeu", "sonda_pode_gravar", "politica_negou")


def _status(hosts, ts="2026-10-22T00:30:00Z", kind="connect_rejected",
            detail=None):
    """O `detail` acompanha o `kind`, e isto nao e detalhe de fixture.

    A primeira versao deste helper cravava `"gateway answered 403 to CONNECT"`
    em TODA entrada, inclusive na de `upstream_timeout` — e o dono reconhece
    `403` no detail como recusa de CONNECT, com razao. Logo a contraprova do
    outro sentido reprovava o modulo CERTO: a fixture descrevia um estado que o
    proxy nao produz. Era o teste errado, nao o modulo.
    """
    if detail is None:
        detail = ("gateway answered 403 to CONNECT"
                  if "connect" in kind.lower() else "upstream read timeout")
    return {"recentRelayFailures": [
        {"ts": ts, "host": "%s:443" % h, "kind": kind,
         "detail": detail} for h in hosts]}


def _sem_proxy(monkeypatch):
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    monkeypatch.delenv("https_proxy", raising=False)


def test_o_caminho_de_saida_NAO_toca_a_rede():
    """Identificar o caminho e barato: se custasse rede, ninguem o chamaria."""
    fonte = inspect.getsource(VP.caminho_de_saida)
    arvore = ast.parse(fonte.strip())
    nomes = {n.id for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    for proibido in ("subprocess", "_sub", "run", "urlopen", "requests"):
        assert proibido not in nomes, (
            "o `caminho_de_saida` nao pode tocar a rede: achei %r" % proibido)
    r = VP.caminho_de_saida()
    assert set(r) >= {"proxy", "maquina", "tem_proxy"}


def test_a_identidade_do_caminho_MUDA_com_o_proxy(monkeypatch):
    """Sem isto a mistura de caminhos nao seria detectavel por ninguem."""
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:46791")
    com = VP.caminho_de_saida()
    _sem_proxy(monkeypatch)
    sem = VP.caminho_de_saida()
    assert com["tem_proxy"] is True and sem["tem_proxy"] is False
    assert com["proxy"] != sem["proxy"], (
        "o caminho tem de MUDAR quando o proxy muda — foi exatamente a"
        " diferenca entre o sandbox e este container")


def test_a_sonda_NAO_aceita_nenhum_dos_tres_controles():
    """Quem junta os controles e ela. Parametro aqui refaria a mistura."""
    sig = inspect.signature(VP.sonda_e_modo)
    for c in CONTROLES:
        assert c not in sig.parameters, (
            "`sonda_e_modo` nao pode receber %r: o defeito de 22/10 foi"
            " justamente combinar controles medidos em lugares diferentes" % c)


def test_REPRODUZ_o_caso_medido_no_sandbox(monkeypatch, tmp_path):
    """Caminho SEM proxy: `indeterminado`, e o motivo DIZ por que."""
    _sem_proxy(monkeypatch)
    r = VP.sonda_e_modo(HOSTS, str(tmp_path), DESDE)
    assert r["caminho"]["tem_proxy"] is False
    assert r["controles"]["sonda_pode_gravar"] is True
    assert r["controles"]["neutro_respondeu"] is False
    assert r["modo"] == "indeterminado", (
        "sem proxy a quem perguntar o quinto modo nao e estabelecivel, e"
        " ausencia de proxy NAO e politica que deixou passar")
    assert "NAO HA PROXY" in r["politica"]["motivo"].upper()


def test_CONTRAPROVA_com_o_proxy_nomeando_os_hosts(monkeypatch, tmp_path):
    """O outro sentido: caminho COM proxy que negou -> `negado_por_politica`."""
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:46791")
    r = VP.sonda_e_modo(HOSTS, str(tmp_path), DESDE, status=_status(HOSTS))
    assert r["modo"] == "negado_por_politica", r["politica"]["motivo"]
    assert r["politica"]["negou"] is True


def test_CONTRAPROVA_com_o_proxy_que_NAO_negou(monkeypatch, tmp_path):
    """Proxy presente e sem recusa dos hosts: `sem_egresso`, nao politica."""
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:46791")
    r = VP.sonda_e_modo(HOSTS, str(tmp_path), DESDE,
                        status=_status(HOSTS, kind="upstream_timeout"))
    assert r["modo"] != "negado_por_politica", (
        "entrada que nao e recusa de CONNECT nao pode virar politica")


def test_o_controle_de_ESCRITA_e_MEDIDO_e_nao_passado(monkeypatch, tmp_path):
    """Diretorio sem como gravar: o modo nao pode sair `sem_egresso`."""
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:46791")
    arq = tmp_path / "um_arquivo"
    arq.write_text("nao sou diretorio", encoding="utf-8")
    r = VP.sonda_e_modo(HOSTS, str(arq / "dentro"), DESDE,
                        status=_status(HOSTS, kind="upstream_timeout"))
    assert r["controles"]["sonda_pode_gravar"] is False
    assert r["modo"] != "sem_egresso", (
        "sem controle de escrita o 000 nao diz de QUEM e o zero (20/10 09:3x)")


def test_o_relato_NOMEIA_o_caminho_e_os_tres_controles(monkeypatch, tmp_path):
    _sem_proxy(monkeypatch)
    r = VP.sonda_e_modo(HOSTS, str(tmp_path), DESDE)
    t = VP.relato_do_modo(r)
    assert "caminho de saida" in t
    assert "AUSENTE" in t
    assert "ESCRITA" in t.upper() and "NEUTRO" in t.upper()
    assert "negado_por_politica" not in t, (
        "relato de caminho SEM proxy nao pode nomear o quinto modo")


def test_o_veredito_segue_do_modo_de_fechamento():
    """`sonda_e_modo` junta e NAO julga — o dono do modo e o de sempre."""
    fonte = inspect.getsource(VP.sonda_e_modo)
    arvore = ast.parse(fonte.strip())
    chamadas = {n.func.id for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "modo_de_fechamento" in chamadas, (
        "ela tem de DELEGAR o veredito; reimplementa-lo criaria o segundo dono")
    devolvidos = set()
    for n in ast.walk(arvore):
        if isinstance(n, ast.Return):
            for c in ast.walk(n):
                if isinstance(c, ast.Constant) and isinstance(c.value, str):
                    devolvidos.add(c.value)
    for m in VP.modos():
        assert m not in devolvidos, (
            "modo devolvido como literal dentro da sonda: %r — o veredito e do"
            " `modo_de_fechamento`" % m)


def test_a_lista_PADRAO_tem_os_dois_lados():
    """Sem um host neutro e um do YouTube, `neutro_respondeu` fica None sempre
    e o modo nunca se estabelece — a vacuidade que o 17/10 nomeia."""
    import tempfile
    base = tempfile.mkdtemp(prefix="sonda-padrao-")
    r = VP.sonda_e_modo(dir_sonda=base, desde=DESDE, status={})
    hosts = list(r["leituras"])
    assert any("youtube" in h for h in hosts), hosts
    assert any("youtube" not in h for h in hosts), hosts


def test_a_MEDIDA_dos_dois_caminhos_continua_escrita():
    """Sem ela a rodada seguinte volta a sondar num caminho e ler no outro."""
    fonte = io.open(os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
                    encoding="utf-8").read()
    for marca in ("sandbox", "container", "22/10"):
        assert marca in fonte, "a medida de 22/10 saiu do modulo: falta %r" % marca
