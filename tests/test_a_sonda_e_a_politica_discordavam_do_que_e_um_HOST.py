# -*- coding: utf-8 -*-
"""A SONDA E A POLITICA DISCORDAVAM DO QUE E UM HOST — 22/10, 01:1x.

A `sonda_e_modo` nasceu as 00:3x para que os TRES controles do
`modo_de_fechamento` saissem do MESMO caminho de saida. Ela aceita host OU URL
para a sonda (monta `https://%s/` quando nao ha esquema) e passava as MESMAS
strings ao `politica_negou_hosts`, cujo casamento era `split(":")[0]` — tira a
PORTA e **nao tira o CAMINHO**.

MEDIDO com o status do proxy desta rodada: `www.youtube.com` e
`www.youtube.com:443` casavam; `www.youtube.com/watch?v=X` e
`https://www.youtube.com/watch?v=X` **nao**. O proxy nomeou
`www.youtube.com:443`, eu passei a URL do `watch`, e a politica saiu nomeando so
o `example.com`. **O modo final ficou certo por acidente** — o neutro tambem foi
negado —, a mesma forma do acordo acidental dos dois caminhos de 00:3x.

O custo e de VEREDITO e nao de relato: com so o host do YouTube na forma
natural, o modo cai para `indeterminado`, cujo remedio e OUTRO.

O que estes testes cobram e a PROPRIEDADE: existe UM dono da extracao do host,
as quatro formas concordam, e a mistura de porta e caminho nao volta.
"""
import ast
import inspect
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import vivacidade_publica as VP  # noqa: E402

HOST = "www.youtube.com"
# As quatro formas que de fato circulam: a sonda recebe URL, o proxy lista
# host:porta, e o CLI recebe host nu.
FORMAS = (
    HOST,
    "%s:443" % HOST,
    "%s/watch?v=OhrGlJvnBoM" % HOST,
    "https://%s/watch?v=OhrGlJvnBoM" % HOST,
)
DESDE = "2026-10-22T01:00:00"


def _status(hosts, ts="2026-10-22T01:07:24.909Z"):
    return {"recentRelayFailures": [
        {"ts": ts, "host": "%s:443" % h, "kind": "connect_rejected",
         "detail": "gateway answered 403 to CONNECT"} for h in hosts]}


def test_as_QUATRO_formas_dao_o_MESMO_host():
    """Sem isto as duas metades da mesma chamada discordam."""
    vistos = {VP.host_de(f) for f in FORMAS}
    assert vistos == {HOST}, vistos


def test_as_quatro_formas_CASAM_na_politica():
    """A contraprova do defeito: era so a terceira e a quarta que falhavam."""
    st = _status([HOST])
    for f in FORMAS:
        r = VP.politica_negou_hosts([f], DESDE, st)
        assert r["negou"] is True, (f, r["motivo"])
        assert r["hosts_nomeados"] == [HOST], (f, r["hosts_nomeados"])


def test_REPRODUZ_o_custo_de_veredito_medido_na_rodada():
    """So o YouTube com CAMINHO dava `indeterminado`; hoje da politica.

    Este e o caso que ocorreu, e ele mede VEREDITO e nao relato — por isso o
    assert passa pelo `modo_de_fechamento`, que e o dono do modo.
    """
    st = _status([HOST])
    com_caminho = VP.politica_negou_hosts(
        ["%s/watch?v=OhrGlJvnBoM" % HOST], DESDE, st)
    modo = VP.modo_de_fechamento(
        "", neutro_respondeu=False, sonda_pode_gravar=True,
        politica_negou=com_caminho["negou"])
    assert modo == "negado_por_politica", (modo, com_caminho["motivo"])


def test_o_ACIDENTE_que_salvou_a_rodada_fica_medido():
    """Com o NEUTRO tambem negado o modo saia certo por outro host.

    Sem este teste *"o veredito ficou certo por acidente"* seria afirmacao
    minha. Aqui ela e medida: o casamento ANTIGO (porta mas nao caminho)
    aplicado ao par devolve politica, e aplicado ao YouTube sozinho nao.
    """
    st = _status([HOST, "example.com"])

    def antigo(hosts):
        alvo = {str(h).split(":")[0] for h in hosts}
        falhas = st["recentRelayFailures"]
        return [f for f in falhas
                if str(f.get("host") or "").split(":")[0] in alvo]

    par = antigo(["%s/watch?v=X" % HOST, "example.com"])
    so_o_youtube = antigo(["%s/watch?v=X" % HOST])
    assert par, "o par tem de casar pelo neutro — e o acidente"
    assert not so_o_youtube, (
        "e o YouTube sozinho NAO casava: e isso que torna o acerto acidental")


def test_a_extracao_tem_UM_dono_por_AST():
    """`split(":")` solto no modulo volta a criar o segundo dono."""
    fonte = io.open(os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
                    encoding="utf-8").read()
    arvore = ast.parse(fonte)
    dono = None
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == "host_de":
            dono = n
    assert dono is not None, "o dono `host_de` desapareceu"
    for n in ast.walk(arvore):
        if not isinstance(n, ast.FunctionDef) or n is dono:
            continue
        corpo = ast.unparse(n)
        assert "split(':')" not in corpo.replace('"', "'"), (
            "`%s` fatia host por conta propria — o dono e o `host_de`" % n.name)


def test_a_politica_CHAMA_o_dono():
    """Import sem chamada e a classe dos layouts mortos."""
    fonte = inspect.getsource(VP.politica_negou_hosts)
    arvore = ast.parse(fonte.strip())
    chamadas = {n.func.id for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "host_de" in chamadas, chamadas


def test_CONTRAPROVA_host_que_nao_foi_negado_segue_sem_politica():
    """Senao bastaria o dono devolver qualquer coisa para tudo casar."""
    st = _status(["example.com"])
    for f in FORMAS:
        r = VP.politica_negou_hosts([f], DESDE, st)
        assert r["negou"] is None, (f, r["motivo"])


def test_entrada_VAZIA_nao_casa_com_tudo():
    """`host_de('')` devolve string vazia, e ela nao pode casar host nenhum."""
    assert VP.host_de("") == ""
    assert VP.host_de(None) == ""
    r = VP.politica_negou_hosts([""], DESDE, _status([HOST]))
    assert r["negou"] is None, r["motivo"]


def test_a_sonda_e_a_politica_concordam_na_MESMA_chamada():
    """O caminho INTEIRO, que e onde o defeito morava.

    A sonda nao toca a rede aqui porque `.invalid` nunca resolve; o que se mede
    e a concordancia entre a URL que ela monta e o host que a politica casa.
    """
    import tempfile
    base = tempfile.mkdtemp(prefix="sonda-host-")
    alvo = "youtube.invalid"
    st = _status([alvo, "example.invalid"])
    r = VP.sonda_e_modo(["%s/watch?v=X" % alvo, "example.invalid"],
                        base, DESDE, status=st)
    assert r["politica"]["hosts_nomeados"] == sorted([alvo, "example.invalid"]), \
        r["politica"]["hosts_nomeados"]
    assert r["modo"] == "negado_por_politica", r["politica"]["motivo"]


def test_a_MEDIDA_das_quatro_formas_continua_escrita():
    """Sem ela a rodada seguinte nao sabe por que o dono existe."""
    fonte = inspect.getsource(VP.host_de)
    for marca in ("22/10", "CAMINHO", "indeterminado", "watch"):
        assert marca in fonte, "a medida saiu do dono: falta %r" % marca
