# -*- coding: utf-8 -*-
"""O registro depois de publicar nao tinha dono — 23/10 as 04:4x.

Publicar termina em QUATRO escritas, sempre as mesmas e na mesma ordem, cada uma
com dono. **A SEQUENCIA nao tinha dono**, e eu a redigitava a cada rodada — e ela
produziu TRES defeitos distintos nesta sessao, todos de digitacao:

* 19/10 as 21:1x: `2>&1` em cima do `.sql`, prosa dentro do arquivo;
* 22/10 as 05:3x: o `job` vindo do run do `retomar`, onde nenhum job narra, logo
  o aviso do 733 contava zero por VACUIDADE (QUATRO pecas de 65);
* 23/10 as 01:3x: `c.append` num corpus que e `{"titulos": [...]}`.

A forma dos testes: nada toca a rede (a leitura dos runs e INJETADA), os parques
sao PROPRIOS (ancorar no vivo seria identidade onde ha propriedade —
743/753/761), cada guarda tem contraprova nos DOIS sentidos, e a delegacao e
cobrada por AST — reimplementar qualquer escrita aqui seria o segundo dono.
"""
import ast
import inspect
import io
import json
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import registro_da_rodada as RR  # noqa: E402

RENDER, PUB = "111111111", "222222222"
PAC, YID, TIT = "canalx-s001", "abcDEF12345", "Um titulo curto"


def _fonte(fn):
    return textwrap.dedent(inspect.getsource(fn))


def _jobs_do_render():
    """Um job que NARROU (emitiu SOM) e um que so publicou — os DOIS lados."""
    return {"jobs": [
        {"id": 900001, "name": "produzir (canalx, canalx-s001, pt-BR)",
         "status": "completed", "conclusion": "success",
         "steps": [{"status": "completed", "conclusion": "success"}],
         "_anotacoes": [
             {"message": "SOM short.mp4 canalx-s001: -14.0 LUFS, LRA 3.0, "
                         "pico -3.0 dBTP, desvio 0.0, 0 silencio(s)"},
         ]},
    ]}


@pytest.fixture
def parques(tmp_path, monkeypatch):
    """Parques PROPRIOS: duracao, som, sql e corpus, todos em tmp_path."""
    import corpus_atrasado as CA
    import duracao_a_medir as DM
    import som_parqueado as SP

    dur = tmp_path / "duracoes.jsonl"
    som = tmp_path / "som.jsonl"
    sql = tmp_path / "videos.sql"
    cor = tmp_path / "corpus.json"
    dur.write_text("", encoding="utf-8")
    som.write_text("", encoding="utf-8")
    sql.write_text("insert into videos (slug) values ('velha') "
                   "on conflict (slug) do nothing;\n", encoding="utf-8")
    cor.write_text(json.dumps({"titulos": ["ja estava"]}, ensure_ascii=False),
                   encoding="utf-8")
    monkeypatch.setattr(DM, "CAMINHO", str(dur), raising=False)
    monkeypatch.setattr(SP, "CAMINHO", str(som), raising=False)
    monkeypatch.setattr(CA, "CAMINHO", str(cor), raising=False)
    # os donos aceitam caminho por argumento; prendemos o default deles
    _dp, _sp, _ca = DM.parqueia, SP.parqueia, CA.aplicar
    monkeypatch.setattr(DM, "parqueia", lambda r, caminho=None: _dp(r, str(dur)))
    monkeypatch.setattr(SP, "parqueia", lambda r, caminho=None: _sp(r, str(som)))
    monkeypatch.setattr(CA, "aplicar", lambda n, caminho=None: _ca(n, str(cor)))
    monkeypatch.setattr(DM, "carrega", lambda caminho=None: [
        json.loads(l) for l in io.open(str(dur), encoding="utf-8") if l.strip()])
    monkeypatch.setattr(SP, "carrega", lambda caminho=None: [
        json.loads(l) for l in io.open(str(som), encoding="utf-8") if l.strip()])
    return {"dur": dur, "som": som, "sql": sql, "cor": cor}


@pytest.fixture
def leituras(monkeypatch):
    """A leitura dos runs vai INJETADA: nada aqui toca a rede."""
    import anotacoes_do_run as AR
    reg = {"slug": PAC + "-short", "status": "publicado", "formato": "shorts",
           "titulo": TIT, "youtube_id": YID, "canal": "canalx",
           "pacote": PAC, "origem_id": "orig123", "cenas": 7,
           "publicado_em": "2026-10-23T04:40:00Z"}
    # A lida vai na FORMA que o `leitura` de fato devolve — `{run, jobs: [...]}`
    # com as `mensagens` de cada job. Ela era `{"run": run}` so, isto e uma
    # forma que o dono NUNCA devolve, e por isso o teste passava por stub: em
    # 23/10 as 09:4x o cruzamento do titulo (que le o notice pela TESTEMUNHA)
    # levou `KeyError: 'jobs'` nos oito testes daqui. Fixture faithful e mais
    # forte, nao mais fraca — ela exercita o cruzamento no sentido que CONCORDA.
    _notice = ("PUBLICADO %s shorts youtube_id=%s titulo=%s "
               "em=2026-10-23T04:40:00Z" % (PAC, YID, TIT))
    monkeypatch.setattr(AR, "leitura", lambda run, **k: {
        "run": run,
        "jobs": [{"id": "900001", "nome": "job", "conclusao": "success",
                  "mensagens": [_notice] if run == PUB else []}]})
    monkeypatch.setattr(AR, "publicado",
                        lambda lida: [reg] if lida.get("run") == PUB else [])
    monkeypatch.setattr(AR, "provedor", lambda lida, pacote=None: (
        {"provedor": "edge", "job": "900001"} if lida.get("run") == RENDER
        else {"provedor": None, "job": None,
              "motivo": "nenhum job deste run emitiu SOM"}))
    monkeypatch.setattr(AR, "som_do_run", lambda lida, pacote=None: (
        [{"pacote": PAC, "arquivo": "short.mp4", "job": "900001",
          "run": RENDER, "pico_dbtp": -3.0, "lufs": -14.0}]
        if lida.get("run") == RENDER else []))
    return reg


# --------------------------------------------------------- o caminho inteiro

def test_as_QUATRO_escritas_acontecem_e_os_parques_sao_RELIDOS(parques, leituras):
    d = RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert d["youtube_id"] == YID and d["provedor"] == "edge"
    assert d["job"] == "900001", "o job nao saiu do run do RENDER"
    assert d["duracao_linhas"] == 1 and d["som_linhas"] == 1
    # e os quatro arquivos no DISCO, nao o retorno da funcao
    assert YID in parques["dur"].read_text(encoding="utf-8")
    assert PAC in parques["som"].read_text(encoding="utf-8")
    assert YID in parques["sql"].read_text(encoding="utf-8")
    assert TIT in parques["cor"].read_text(encoding="utf-8")


def test_o_relato_NOMEIA_os_quatro_parques(parques, leituras):
    r = RR.relato(RENDER, PUB, PAC, 25.0, 20.5,
                  sql_pendente=str(parques["sql"]))
    for marca in ("DURACAO", "SOM", "SQL pendente", "CORPUS", "RELIDO"):
        assert marca in r, (marca, r)
    assert "run do RENDER" in r


# ------------------------------------------- as guardas, nos dois sentidos

def test_os_DOIS_runs_sao_obrigatorios_e_sem_PADRAO():
    """Padrao faria a rodada passar o run errado em silencio (05:3x)."""
    sig = inspect.signature(RR.registra)
    for nome in ("run_render", "run_pub"):
        assert sig.parameters[nome].default is inspect.Parameter.empty, nome
    with pytest.raises(ValueError) as e:
        RR.registra(None, PUB, PAC, 25.0, 20.5)
    assert "obrigatorios" in str(e.value)


def test_o_MESMO_run_nos_dois_LEVANTA_citando_a_VACUIDADE(parques, leituras):
    with pytest.raises(ValueError) as e:
        RR.registra(PUB, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert "VACUIDADE" in str(e.value) and "733" in str(e.value)


def test_provedor_nao_estabelecido_LEVANTA_em_vez_de_parquear(parques, leituras):
    """Contraprova no outro sentido: o run do `retomar` como RENDER recusa."""
    with pytest.raises(ValueError) as e:
        RR.registra(PUB, RENDER, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    # o par invertido cai primeiro na falta de notice OU no provedor; os dois
    # sao recusas com motivo, e nenhuma delas parqueia
    assert "nenhum" in str(e.value).lower()
    assert parques["dur"].read_text(encoding="utf-8").strip() == ""


def test_sem_NOTICE_do_pacote_LEVANTA(parques, leituras):
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, "canalx-s999", 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert "PUBLICADO" in str(e.value)
    assert parques["dur"].read_text(encoding="utf-8").strip() == ""


def test_o_TITULO_divergente_LEVANTA(parques, leituras):
    """Gravar o meu no corpus poria la um titulo que o YouTube nao recebeu."""
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC, 25.0, 20.5, titulo="Outro titulo",
                    sql_pendente=str(parques["sql"]))
    assert "NAO e o que subiu" in str(e.value)
    assert "Outro titulo" not in parques["cor"].read_text(encoding="utf-8")


def test_o_TITULO_igual_PASSA(parques, leituras):
    """Contraprova: senao bastaria levantar sempre."""
    d = RR.registra(RENDER, PUB, PAC, 25.0, 20.5, titulo=TIT,
                    sql_pendente=str(parques["sql"]))
    assert d["titulo"] == TIT


# ------------------------------------------------- a prosa no SQL (21:1x)

def test_PROSA_no_pendente_LEVANTA_citando_o_2_para_1(parques, leituras):
    parques["sql"].write_text(
        "insert into videos (slug) values ('v') on conflict (slug) do nothing;\n"
        "REGISTRO: 1 linha(s) parqueada(s)\n", encoding="utf-8")
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert "2>&1" in str(e.value) or "stderr" in str(e.value)


def test_o_pendente_LIMPO_passa_e_a_contagem_SOBE(parques, leituras):
    antes = len([l for l in parques["sql"].read_text(encoding="utf-8").splitlines()
                 if l.strip()])
    d = RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert d["sql_linhas"] > antes


# --------------------------------------------------- delegacao, por AST

def test_nada_aqui_REIMPLEMENTA_escrita_alheia():
    """`json.dumps`, `open(..., 'a')` de parque e regex no notice reprovam."""
    fonte = io.open(RR.__file__, encoding="utf-8").read()
    arv = ast.parse(fonte)
    proibidos = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
            proibidos.add("%s.%s" % (n.value.id, n.attr))
    for p in ("json.dumps", "re.compile", "re.search", "re.findall"):
        assert p not in proibidos, (
            "o modulo reimplementa %s: a escrita e a leitura tem donos" % p)


def test_as_QUATRO_delegacoes_sao_CHAMADAS_por_AST():
    arv = ast.parse(_fonte(RR.registra))
    chamadas = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and isinstance(n.func.value, ast.Name):
            chamadas.add("%s.%s" % (n.func.value.id, n.func.attr))
    for dono in ("DM.parqueia", "DM.do_registro", "SP.parqueia", "CA.aplicar",
                 "AR.provedor", "AR.som_do_run"):
        assert dono in chamadas, (dono, sorted(chamadas))


def test_o_SQL_sai_do_dono_e_nao_e_montado_aqui():
    fonte = io.open(RR.__file__, encoding="utf-8").read()
    assert "RV.sql_insert" in fonte
    assert "insert into videos (" not in fonte, (
        "o modulo monta o INSERT por conta propria: o dono e o "
        "`registro_videos`")


def test_os_TRES_defeitos_medidos_continuam_escritos():
    doc = RR.__doc__ or ""
    for marca in ("21:1x", "05:3x", "01:3x", "VACUIDADE", "13:2x"):
        assert marca in doc, marca
    assert "redigitava" in doc or "digitacao" in doc


# ------------------------------- a RELEITURA, cobrada por quem ela protege
# A primeira contraprova deste arquivo derrubou UM de catorze ao desligar a
# releitura: no caminho feliz a peca ESTA no parque, logo nenhum teste via a
# guarda. E ela e justamente a lição de 20/10 as 13:2x. Estes dois cobram-na
# fazendo a escrita falhar em SILENCIO, que e o caso que ela existe para pegar.

def test_a_RELEITURA_pega_escrita_que_falha_em_SILENCIO(parques, leituras,
                                                        monkeypatch):
    import duracao_a_medir as DM
    monkeypatch.setattr(DM, "parqueia", lambda r, caminho=None: True)
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    # A frase era cobrada por IDENTIDADE (`"NAO esta no parque"`, no singular) e
    # o conserto do PACOTE de 23/10 as 14:1x a pluralizou, porque a recusa passou
    # a NOMEAR quais pecas faltam. Era o teste que estava atras, nao o modulo —
    # 743/753/761. A propriedade e: ela nomeia o parque, nomeia a peca que falta,
    # e carrega a procedencia.
    m = str(e.value)
    assert "parque de duracao" in m and YID in m, m
    assert "13:2x" in m, (
        "a recusa perdeu a procedencia: retorno de funcao nao prova presenca")


def test_a_RELEITURA_do_SOM_tambem_pega(parques, leituras, monkeypatch):
    import som_parqueado as SP
    monkeypatch.setattr(SP, "parqueia", lambda r, caminho=None: {})
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert "parque de som" in str(e.value)


def test_a_RELEITURA_do_PENDENTE_tambem_pega(parques, leituras, monkeypatch):
    """Se o INSERT sair sem o youtube_id, o arquivo passa mas a peca nao esta."""
    import registro_videos as RV
    monkeypatch.setattr(RV, "sql_insert", lambda linhas:
                        "insert into videos (slug) values ('x') "
                        "on conflict (slug) do nothing;")
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert "NAO esta no pendente" in str(e.value)


# ------------------------------------------------------- o PACOTE (14:1x)
# **MEDIDO em 23/10 as 14:1x, no PRIMEIRO pacote desde que o modulo nasceu:**
# ele parqueava `regs[0]` e so, logo o LONGO do `epomeno-epipedo-069` ficou FORA
# do parque de duracao e do corpus. O SQL ja saia certo (o `sql_insert` recebe a
# lista inteira), e e isso que torna a falha PARCIAL e mais facil de nao ver.
# Estes testes cobram as DUAS pecas e a previsao POR PECA, com contraprova no
# outro sentido — o short solto continua parqueando UMA linha e sem exigir nada.

PAC_P = "canalx-001"
YID_L, TIT_L = "LONGid00001", "O titulo do longo"
YID_S, TIT_S = "SHORTid0001", "O titulo do short"
PREV_L = (619.4, 548.8)


@pytest.fixture
def leituras_pacote(monkeypatch):
    """Um PACOTE: dois notices do mesmo pacote, o short PRIMEIRO.

    A ordem espelha o incidente — no `epomeno-epipedo-069` o `regs[0]` era o
    short, e foi o LONGO que ficou fora. Ela nao decide nada: parquear so o
    primeiro deixa uma peca de fora em qualquer ordem.
    """
    import anotacoes_do_run as AR
    base = {"status": "publicado", "canal": "canalx", "pacote": PAC_P,
            "publicado_em": "2026-10-23T13:46:00Z"}
    curto = dict(base, slug=PAC_P + "-short", formato="shorts", titulo=TIT_S,
                 youtube_id=YID_S, origem_id=YID_L, cenas=13)
    longo = dict(base, slug=PAC_P, formato="longo", titulo=TIT_L,
                 youtube_id=YID_L, origem_id=None, cenas=62)
    regs = [curto, longo]
    notices = ["PUBLICADO %s %s youtube_id=%s titulo=%s em=%s"
               % (PAC_P, r["formato"], r["youtube_id"], r["titulo"],
                  r["publicado_em"]) for r in regs]
    monkeypatch.setattr(AR, "leitura", lambda run, **k: {
        "run": run,
        "jobs": [{"id": "900001", "nome": "job", "conclusao": "success",
                  "mensagens": notices if run == PUB else []}]})
    monkeypatch.setattr(AR, "publicado",
                        lambda lida: list(regs) if lida.get("run") == PUB else [])
    monkeypatch.setattr(AR, "provedor", lambda lida, pacote=None: (
        {"provedor": "edge", "job": "900001"} if lida.get("run") == RENDER
        else {"provedor": None, "job": None, "motivo": "nenhum job emitiu SOM"}))
    monkeypatch.setattr(AR, "som_do_run", lambda lida, pacote=None: (
        [{"pacote": PAC_P, "arquivo": a, "job": "900001", "run": RENDER,
          "pico_dbtp": p, "lufs": -14.0}
         for a, p in (("longo.mp4", -3.2), ("short.mp4", -2.7))]
        if lida.get("run") == RENDER else []))
    return regs


def test_o_PACOTE_parqueia_as_DUAS_pecas(parques, leituras_pacote):
    d = RR.registra(RENDER, PUB, PAC_P, 41.6, 36.9, prev_longo=PREV_L,
                    sql_pendente=str(parques["sql"]))
    assert d["duracao_linhas"] == 2, "o pacote parqueou %s peca(s)" % \
        d["duracao_linhas"]
    texto = parques["dur"].read_text(encoding="utf-8")
    for yid in (YID_S, YID_L):
        assert yid in texto, "%s ficou FORA do parque de duracao" % yid


def test_a_previsao_e_POR_PECA_e_nao_compartilhada(parques, leituras_pacote):
    RR.registra(RENDER, PUB, PAC_P, 41.6, 36.9, prev_longo=PREV_L,
                sql_pendente=str(parques["sql"]))
    por = {r["youtube_id"]: r for r in (
        json.loads(l) for l in
        parques["dur"].read_text(encoding="utf-8").splitlines() if l.strip())}
    assert por[YID_L]["prev_edge"] == PREV_L[0]
    assert por[YID_S]["prev_edge"] == 41.6
    # sem esta guarda o teste passaria com as duas previsoes iguais, que e
    # exatamente o defeito: um longo de ~620 s com o numero de um short de ~42 s
    assert por[YID_L]["prev_edge"] != por[YID_S]["prev_edge"]
    assert por[YID_L]["prev_piper"] != por[YID_S]["prev_piper"]


def test_o_PACOTE_sem_prev_longo_LEVANTA(parques, leituras_pacote):
    with pytest.raises(ValueError) as e:
        RR.registra(RENDER, PUB, PAC_P, 41.6, 36.9,
                    sql_pendente=str(parques["sql"]))
    m = str(e.value)
    assert "prev_longo" in m and YID_L in m, m
    assert parques["dur"].read_text(encoding="utf-8").strip() == "", (
        "ele parqueou antes de recusar: a recusa tem de vir ANTES da escrita")


def test_o_defeito_MEDIDO_e_PARCIAL_e_o_regs_0_deixa_peca_FORA(leituras_pacote):
    """O que o modulo fazia: `regs[0]` e so. Sem isto, 'eu errei' seria minha."""
    import anotacoes_do_run as AR
    regs = RR._notices_do_pacote(AR.leitura(PUB), PAC_P)
    assert len(regs) >= 2, (
        "a fixture deixou de ter pacote com DUAS pecas — sem os dois lados "
        "este arquivo nao mede o defeito de 14:1x")
    so_o_primeiro = {regs[0]["youtube_id"]}
    todos = {r["youtube_id"] for r in regs}
    assert todos - so_o_primeiro, "parquear regs[0] nao deixaria peca de fora"
    # e o SQL saia CERTO no mesmo passo, que e o que torna a falha parcial
    import registro_videos as RV
    sql = RV.sql_insert(AR.publicado(AR.leitura(PUB)))
    for yid in todos:
        assert yid in sql


def test_o_PACOTE_poe_os_DOIS_titulos_no_corpus(parques, leituras_pacote):
    RR.registra(RENDER, PUB, PAC_P, 41.6, 36.9, prev_longo=PREV_L,
                sql_pendente=str(parques["sql"]))
    cor = parques["cor"].read_text(encoding="utf-8")
    for tit in (TIT_S, TIT_L):
        assert tit in cor, (
            "%r nao entrou no corpus: a trava de titulo duplicado do "
            "`prontidao` (773) fica cega nessa peca" % tit)


def test_o_SOM_do_pacote_parqueia_as_DUAS_leituras(parques, leituras_pacote):
    d = RR.registra(RENDER, PUB, PAC_P, 41.6, 36.9, prev_longo=PREV_L,
                    sql_pendente=str(parques["sql"]))
    assert d["som_linhas"] == 2
    som = parques["som"].read_text(encoding="utf-8")
    for arq in ("longo.mp4", "short.mp4"):
        assert arq in som


def test_o_short_SOLTO_nao_exige_prev_longo_e_parqueia_UMA(parques, leituras):
    """Contraprova no outro sentido: sem ela, exigir sempre passaria."""
    d = RR.registra(RENDER, PUB, PAC, 25.0, 20.5,
                    sql_pendente=str(parques["sql"]))
    assert d["duracao_linhas"] == 1
