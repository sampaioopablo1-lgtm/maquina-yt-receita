#!/usr/bin/env python3
"""O relato tinha o TITULO na mao e imprimia so o par pacote -> id.

**Medido em 23/10 as 08:4x, fechando a rodada da `labtreinamento-s115`.** Eu fui
ler o `::notice:: PUBLICADO` A MAO —

    gh api .../actions/runs/<run>/jobs --jq '.jobs[0].id'
    gh api .../check-runs/<job>/annotations

— quando o `anotacoes_do_run` ja responde isso. Dois defeitos numa rota so:

1. **O TITULO era JOGADO FORA.** A linha de `videos` que o `publicado` devolve
   carrega `titulo`, `publicado_em`, `canal`, `origem_id` e `cenas`, e o relato
   imprimia so `pacote -> youtube_id`. Logo a UNICA leitura do titulo que de
   fato subiu era a minha vista sobre o notice — e o titulo e exatamente o valor
   que o `registro_da_rodada` CONFERE e que o faz LEVANTAR quando divergir,
   porque o corpus guarda o titulo CURTO e a trava de titulo duplicado do
   `prontidao` compara contra ele (773). Titulo meu no corpus poe no
   anti-duplicata um titulo que o YouTube nunca recebeu, e a trava fica cega
   naquela peca, em silencio e no sentido PERMISSIVO;
2. **o `[0]` e uma FATIA.** Medido nos dois runs desta rodada: no RENDER
   `jobs[0]` e o `preparar` e quem narrou e o `produzir`; no `retomar` ha UM
   job, logo a fatia acerta. **A rota a mao esta errada em todo run de render e
   acertou aqui por ACIDENTE** — a forma do acordo acidental dos dois caminhos
   de saida (22/10 as 00:3x) e do casamento de host (01:1x). E contar o aviso do
   733 no `preparar` devolve zero por VACUIDADE, que e o defeito das quatro
   pecas com o job do `retomar` como procedencia.

**Contraprova:** desligada a linha do titulo, reprova o teste que a mede;
desligado o ramo da ausencia, reprova o outro.
"""
from __future__ import annotations

import ast
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR  # noqa: E402
import registro_videos as RV  # noqa: E402

# HISTORIA da medicao de 23/10 as 08:4x. NENHUM assert depende destes ids: eles
# mudam a cada rodada, e ancorar neles seria identidade onde ha propriedade
# (743/753/761).
PAR_DE_08H = {
    "render": {"run": "39923653381", "fatia": "120314658279",
               "narrou": "120314685498"},
    "publicacao": {"run": "39924132717", "job": "120316257870",
                   "id_no_ar": "ydD3c_o6C70"},
}

NOTICE_SOM = ('SOM short.mp4 %s {"lufs": -14.1, "lra": 1.4, '
              '"pico_dbtp": -3.6, "desvio_do_alvo": -0.1, "silencios": [], '
              '"pico_vs_teto": "dentro", "teto_dbtp": -1.5}')


def _ancora() -> tuple:
    """Um pacote do DISCO com short E com `## TITULO SHORT`, e o titulo dele.

    DERIVADO, e nao nomeado: o dono do notice ABRE a spec no disco, logo pacote
    inventado nao resolve — e nomear um pacote seria identidade onde ha
    propriedade (743/753/761), porque o disco cresce uma spec por rodada.
    """
    import glob
    import json
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json")), reverse=True):
        try:
            sp = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(sp, dict) or not sp.get("short") or sp.get("longo"):
            continue
        tit = RV.titulo_short(sp)
        if tit:
            return os.path.basename(f)[:-5], tit
    pytest.fail("o arquivo perdeu a ancora: nenhuma spec de short solto do "
                "disco traz `## TITULO SHORT`, e sem ela nada aqui mede.")


PACOTE, TITULO_DA_SPEC = _ancora()
NOTICE_PUB = ("PUBLICADO %s shorts youtube_id=AAAAAAAAAAA titulo=%s "
              "em=2026-10-23T08:22:19Z" % (PACOTE, TITULO_DA_SPEC))
NOTICE_OUTRO = ("PUBLICADO %s shorts youtube_id=AAAAAAAAAAA "
                "titulo=UM TITULO QUE A SPEC NAO TEM "
                "em=2026-10-23T08:22:19Z" % PACOTE)


def _lida(jobs: list, run: str = "1") -> dict:
    return {"run": run, "jobs": jobs}


def _job(jid: str, nome: str, mensagens: list) -> dict:
    return {"id": jid, "nome": nome, "conclusao": "success",
            "mensagens": mensagens}


@pytest.fixture
def render() -> dict:
    """Run de RENDER: `jobs[0]` NAO narra, `jobs[1]` narra.

    E a forma MEDIDA do run desta rodada, e os dois lados tem de existir: sem um
    job que narra e um que nao, a fatia nao distingue nada e o arquivo passaria
    por vacuidade.
    """
    return _lida([_job("111", "preparar", ["alguma anotacao do runner"]),
                  _job("222", "produzir (%s, pt-BR)" % PACOTE,
                       [NOTICE_SOM % PACOTE])])


@pytest.fixture
def publicacao() -> dict:
    """Run do `retomar`: UM job, que publica e nao narra."""
    return _lida([_job("333", "retomar", [NOTICE_PUB])])


@pytest.fixture
def publicacao_divergente() -> dict:
    """O MESMO run, com o notice dizendo outro titulo que a spec."""
    return _lida([_job("333", "retomar", [NOTICE_OUTRO])])


def _fonte(fn) -> str:
    import inspect
    import textwrap
    return textwrap.dedent(inspect.getsource(fn))


def _chamadas(fn) -> set:
    nomes = set()
    for n in ast.walk(ast.parse(_fonte(fn))):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
    return nomes


# ---------------------------------------------------------------- o TITULO

def test_o_TITULO_chega_a_linha(publicacao):
    """E ele vem do DONO da linha de `videos`, nao remontado aqui."""
    do_dono = RV.linhas_dos_notices(NOTICE_PUB)
    assert len(do_dono) == 1, do_dono
    tit = do_dono[0]["titulo"]
    assert tit and tit.strip() == tit, repr(tit)

    linhas = AR._linha_do_publicado(publicacao)
    assert len(linhas) == 1, linhas
    assert tit in linhas[0], (tit, linhas)


def test_a_linha_NAO_e_mais_so_o_par_pacote_id(publicacao):
    """A propriedade e que a linha carrega o titulo E o instante, nao a string.

    Cobrada contra os campos do DONO: o que o notice traz e a linha nao imprime
    volta a ser leitura da minha vista.
    """
    ln = RV.linhas_dos_notices(NOTICE_PUB)[0]
    saida = "\n".join(AR._linha_do_publicado(publicacao))
    for campo in ("pacote", "youtube_id", "titulo", "publicado_em"):
        assert str(ln[campo]) in saida, (campo, ln[campo], saida)


def test_sem_notice_a_linha_DIZ_e_nao_inventa(render):
    """Contraprova no outro sentido: ausencia de notice e o NORMAL no render.

    Sem este ramo, imprimir nada e dizer "nao publicou" ficariam
    indistinguiveis — e ausencia de notice nao prova peca sem publicar (17/10).
    """
    linhas = AR._linha_do_publicado(render)
    assert len(linhas) == 1, linhas
    assert "nenhum" in linhas[0].lower(), linhas
    assert "RENDER" in linhas[0], linhas
    # e ela nao pode fabricar id nem titulo
    assert "youtube_id=" not in linhas[0], linhas


def test_a_linha_tem_UM_dono_por_AST():
    """O prefixo so pode aparecer dentro do dono, e o relato tem de o CHAMAR.

    Prefixo escrito a mao em outro lugar e o segundo dono da frase — a
    assinatura que congelou a legenda.
    """
    fonte = io.open(os.path.join(RAIZ, "fabrica", "anotacoes_do_run.py"),
                    encoding="utf-8").read()
    arv = ast.parse(fonte)
    donos, cravaram = set(), set()
    for n in ast.walk(arv):
        if not isinstance(n, ast.FunctionDef):
            continue
        corpo = ast.unparse(n)
        # O prefixo mora numa CONSTANTE, logo quem o usa cita o NOME dela; e
        # quem reescreve o literal e o segundo dono, que e o que se proibe.
        if "_PRE_PUB" in corpo:
            donos.add(n.name)
        if AR._PRE_PUB in corpo:
            cravaram.add(n.name)
    assert donos == {"_linha_do_publicado"}, donos
    assert not cravaram, cravaram
    assert "_linha_do_publicado" in _chamadas(AR.relato), _chamadas(AR.relato)


def test_o_relato_NAO_remonta_a_linha_do_publicado():
    """`publicado(` dentro do `relato` seria a volta do par cru."""
    assert "publicado" not in _chamadas(AR.relato) or \
        "_linha_do_publicado" in _chamadas(AR.relato)
    fonte = _fonte(AR.relato)
    assert "youtube_id" not in fonte, fonte


# ------------------------------------------------------------------ a FATIA

def test_a_FATIA_do_render_NAO_e_o_job_que_narrou(render):
    """O defeito REPRODUZIDO: `jobs[0]` nao e de onde a procedencia sai."""
    f = AR.fatia_de_job(render, PACOTE)
    assert f["n_jobs"] > 1, f
    assert f["primeiro"] == "111", f
    assert f["job_do_provedor"] == "222", f
    assert f["fatia_acerta"] is False, f


def test_contar_na_FATIA_devolve_zero_por_VACUIDADE(render):
    """E o `provedor` RECUSA ali, em vez de chamar o zero de medicao.

    Sem esta metade, "a fatia erra" seria afirmacao minha e nao medida.
    """
    so_a_fatia = _lida([render["jobs"][0]], run=render["run"])
    with pytest.raises(AR.SemProcedencia):
        AR.provedor(so_a_fatia, PACOTE)
    # contado a mao naquele job, o aviso do 733 da ZERO — e zero ali nao mede
    avisos = sum(1 for m in render["jobs"][0]["mensagens"]
                 if AR.MARCA_PIPER in m)
    assert avisos == 0, avisos
    # enquanto no job que narrou ele mede
    assert AR.provedor(render, PACOTE)["provedor"] == "edge"


def test_com_UM_job_que_narra_a_fatia_ACERTA(render):
    """Contraprova no outro sentido: senao `fatia_acerta` sairia sempre False."""
    so_quem_narra = _lida([render["jobs"][1]], run=render["run"])
    f = AR.fatia_de_job(so_quem_narra, PACOTE)
    assert f["n_jobs"] == 1, f
    assert f["fatia_acerta"] is True, f


def test_sem_ninguem_narrando_a_fatia_e_INDETERMINADA(publicacao):
    """`None`, nao False: nao saber se a fatia acerta e outra coisa de saber
    que ela erra — do jeito que o `porta1` recusa janela curta."""
    f = AR.fatia_de_job(publicacao, PACOTE)
    assert f["job_do_provedor"] is None, f
    assert f["fatia_acerta"] is None, f


def test_a_fatia_NAO_decide_o_provedor_por_AST():
    """O veredito sai do discriminador MEDIDO, nunca do indice nem do NOME."""
    for fn in (AR.provedor, AR.jobs_que_narraram):
        ch = _chamadas(fn)
        assert "fatia_de_job" not in ch, (fn.__name__, ch)
    fonte = _fonte(AR.jobs_que_narraram)
    assert "jobs[0]" not in fonte.replace(" ", ""), fonte
    # e o discriminador continua sendo o SOM, nao o nome do job
    assert "_som_do_job" in _chamadas(AR.jobs_que_narraram)
    assert "produzir" not in _fonte(AR.jobs_que_narraram)


def test_o_relato_NOMEIA_a_fatia_quando_ela_erra(render, publicacao,
                                                 monkeypatch):
    """E NAO a nomeia quando ela nao erra — aviso que sempre sai nao avisa."""
    monkeypatch.setattr(AR, "divergencias_de_job",
                        lambda *a, **k: {"comuns": 9, "divergentes": []})
    monkeypatch.setattr(AR, "leitura", lambda *a, **k: render)
    r = AR.relato("1", PACOTE)
    assert "FATIA" in r, r
    assert "VACUIDADE" in r, r

    monkeypatch.setattr(AR, "leitura", lambda *a, **k: publicacao)
    r2 = AR.relato("1", PACOTE)
    assert "FATIA" not in r2, r2


def test_a_medicao_e_a_familia_continuam_escritas():
    """Conserto sem motivo escrito volta calado."""
    fonte = io.open(os.path.join(RAIZ, "fabrica", "anotacoes_do_run.py"),
                    encoding="utf-8").read()
    for marca in ("08:4x", "FATIA", "VACUIDADE", "773", "preparar",
                  "produzir", "ACIDENTE"):
        assert marca in fonte, marca
    assert PAR_DE_08H["render"]["fatia"] in fonte
    assert PAR_DE_08H["render"]["narrou"] in fonte


# ------------------------------------------- os DOIS donos do TITULO

def test_a_LINHA_prefere_a_SPEC_e_IGNORA_o_notice():
    """O defeito REPRODUZIDO, e e ele que torna a conferencia antiga vazia."""
    ln = RV.linhas_dos_notices(NOTICE_OUTRO)
    assert len(ln) == 1, ln
    assert ln[0]["titulo"] == TITULO_DA_SPEC, ln
    assert "UM TITULO QUE A SPEC NAO TEM" not in ln[0]["titulo"]


def test_os_DOIS_lados_existem_no_DISCO():
    """Spec COM a secao (a spec vence) e spec SEM (a linha cai no notice).

    Sem os dois lados o cruzamento nao distingue nada, e o arquivo passaria por
    vacuidade. A medida vai como PROPORCAO e nao como contagem: o disco cresce
    uma spec por rodada, e contagem absoluta sobre populacao que cresce e
    identidade disfarcada de medida (a licao de 22/10 as 14:4x).
    """
    import glob
    import json
    com = sem = 0
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            sp = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(sp, dict) or not sp.get("short"):
            continue
        if RV.titulo_short(sp):
            com += 1
        else:
            sem += 1
    assert com + sem >= 200, (com, sem)
    assert com and sem, (com, sem)
    frac = com / float(com + sem)
    assert 0.5 <= frac <= 0.95, frac


def test_a_divergencia_e_NOMEADA(publicacao_divergente):
    d = AR.divergencia_de_titulo(publicacao_divergente)
    assert d["pares"] == 1, d
    assert len(d["divergentes"]) == 1, d
    x = d["divergentes"][0]
    assert x["da_linha"] == TITULO_DA_SPEC, x
    assert x["do_notice"] == "UM TITULO QUE A SPEC NAO TEM", x


def test_sem_divergencia_ele_NAO_acusa(publicacao):
    """Contraprova no outro sentido: senao ele acusaria toda rodada e, pelo
    argumento do `mira.py`, deixaria de avisar."""
    d = AR.divergencia_de_titulo(publicacao)
    assert d["pares"] == 1, d
    assert d["divergentes"] == [], d


def test_a_linha_imprime_os_DOIS_titulos_e_marca_a_divergencia(
        publicacao, publicacao_divergente):
    limpo = "\n".join(AR._linha_do_publicado(publicacao))
    assert "SUBIU" in limpo and "LINHA" in limpo, limpo
    assert "DIVERGEM" not in limpo, limpo

    sujo = "\n".join(AR._linha_do_publicado(publicacao_divergente))
    assert "DIVERGEM" in sujo, sujo
    assert "773" in sujo, sujo
    # os DOIS valores aparecem, para a divergencia ser LEGIVEL e nao so dita
    assert TITULO_DA_SPEC in sujo and "UM TITULO QUE A SPEC NAO TEM" in sujo


def test_as_duas_leituras_sao_DELEGADAS_por_AST():
    """Reparsear o notice aqui seria o TERCEIRO dono da forma dele."""
    fonte = _fonte(AR.divergencia_de_titulo)
    for proibido in ("re.", "findall", "split(", "startswith"):
        assert proibido not in fonte, (proibido, fonte)
    ch = _chamadas(AR.divergencia_de_titulo)
    assert "titulos_dos_notices" in ch, ch
    assert "publicado" in ch, ch


def test_quem_GRAVA_recusa_a_divergencia(monkeypatch, publicacao_divergente):
    """O `anotacoes_do_run` NOMEIA; quem RECUSA e quem escreve no corpus."""
    import registro_da_rodada as RR
    chamou = {"aplicar": 0}
    monkeypatch.setattr(RR.CA, "aplicar",
                        lambda *a, **k: chamou.__setitem__("aplicar", 1))
    monkeypatch.setattr(RR.AR, "leitura",
                        lambda run, **k: publicacao_divergente)
    with pytest.raises(ValueError) as e:
        RR.registra("1", "2", PACOTE, 25.0, 20.5)
    assert "SUBIU" in str(e.value), str(e.value)
    assert "773" in str(e.value), str(e.value)
    # e ele recusa ANTES de tocar o corpus
    assert chamou["aplicar"] == 0


def test_a_recusa_e_DELEGADA_ao_cruzamento_por_AST():
    import registro_da_rodada as RR
    ch = _chamadas(RR.registra)
    assert "divergencia_de_titulo" in ch, ch
    fonte = _fonte(RR.registra)
    assert "titulos_dos_notices" not in fonte, fonte


def test_a_RETRATACAO_continua_escrita():
    """Retratacao sem teste volta, e esta e de uma frase do proprio modulo."""
    import registro_da_rodada as RR
    doc = RR.registra.__doc__ or ""
    assert "RETRATACAO" in doc, doc
    assert "338" in doc and "107" in doc, doc
    assert "14:4x" in doc, doc
    fonte = io.open(os.path.join(RAIZ, "fabrica", "anotacoes_do_run.py"),
                    encoding="utf-8").read()
    for marca in ("testemunha", "338", "107", "773", "14:4x"):
        assert marca in fonte, marca
