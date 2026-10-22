#!/usr/bin/env python3
"""O `job` que da procedencia ao provedor tinha DOIS donos e eles divergiam.

Medido em 22/10 as 05:3x: de 65 pacotes com `job` nos dois parques, QUATRO
divergiam — e nos quatro o parque de DURACAO citava o job do `retomar`, que
emite `PUBLICADO` e **nunca narra**. Logo o *"zero avisos"* do 733 que eu
reportei para eles era zero por VACUIDADE.

A conclusao sobreviveu (os jobs `produzir` de verdade dao zero tambem), logo o
que se conserta e a PROCEDENCIA. Os quatro ids antigos ficam aqui como
HISTORIA, com o motivo escrito, para a rodada seguinte nao os readotar — e o
que o arquivo COBRA e propriedade, nao identidade (743/753/761).
"""
import ast
import inspect
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR  # noqa: E402
import duracao_a_medir as DM  # noqa: E402
import som_parqueado as SP  # noqa: E402

# HISTORIA, nao ancora: o par (job do `retomar`, job do `produzir`) de uma das
# quatro pecas de 22/10. Ele esta aqui para o motivo nao se perder; nenhum
# assert depende destes numeros.
PAR_DE_05H = ("118525086049", "118524197854")

MINIMO_COMUNS = 20


def _lida(jobs):
    return {"run": "9", "jobs": [
        {"id": i, "nome": n, "conclusao": "success", "mensagens": m}
        for i, n, m in jobs]}


SOM_OK = ('SOM short.mp4 labtreinamento-s106 {"lufs": -14.1, "lra": 1.8, '
          '"pico_dbtp": -3.7, "desvio_do_alvo": -0.1, "silencios": [], '
          '"pico_vs_teto": "dentro", "teto_dbtp": -1.5}')
PUB_OK = ("PUBLICADO labtreinamento-s106 shorts youtube_id=3r3Dbjtn-Fs "
          "titulo=A fonte e um instrumento em=2026-10-22T05:18:30Z")
PIPER = "::warning::NARRACAO PELO PIPER cena 3"


def test_o_zero_do_job_que_PUBLICA_e_vacuo_e_ele_RECUSA():
    """O defeito REPRODUZIDO: so o job do `retomar` no run."""
    lida = _lida([(PAR_DE_05H[0], "publicar", ["Node.js 20...", PUB_OK])])
    assert AR.jobs_que_narraram(lida) == [], (
        "job que so publicou nao narrou, logo contar o aviso do 733 nele e vacuo")
    with pytest.raises(AR.SemProcedencia) as e:
        AR.provedor(lida)
    assert "VACUIDADE" in str(e.value).upper()


def test_com_o_job_que_NARROU_ele_responde():
    """Contraprova no outro sentido: sem ela, recusar sempre passaria."""
    lida = _lida([(PAR_DE_05H[1], "produzir (x)", [SOM_OK])])
    p = AR.provedor(lida)
    assert p["provedor"] == "edge" and p["avisos_piper"] == 0
    assert p["job"] == PAR_DE_05H[1]


def test_ele_conta_o_aviso_e_nao_o_infere():
    lida = _lida([("1", "produzir (x)", [SOM_OK, PIPER, PIPER])])
    p = AR.provedor(lida)
    assert p["provedor"] == "piper" and p["avisos_piper"] == 2


def test_o_discriminador_e_a_ANOTACAO_e_nao_o_NOME_do_job():
    """Nos dois sentidos: nome estranho que narrou ENTRA; nome `produzir` que
    nao emitiu SOM fica FORA. Era o nome que eu usava sem dizer."""
    lida = _lida([("7", "render-novo", [SOM_OK])])
    assert [j["id"] for j in AR.jobs_que_narraram(lida)] == ["7"]
    lida2 = _lida([("8", "produzir (x)", ["Node.js 20...", PUB_OK])])
    assert AR.jobs_que_narraram(lida2) == []


def test_o_pacote_filtra_o_job_que_narrou():
    outro = SOM_OK.replace("labtreinamento-s106", "outro-pacote-s001")
    lida = _lida([("1", "produzir (a)", [outro]),
                  ("2", "produzir (b)", [SOM_OK, PIPER])])
    assert [j["id"] for j in
            AR.jobs_que_narraram(lida, "labtreinamento-s106")] == ["2"]
    assert AR.provedor(lida, "outro-pacote-s001")["provedor"] == "edge"
    assert AR.provedor(lida, "labtreinamento-s106")["provedor"] == "piper"


def test_run_sem_job_LEVANTA_em_vez_de_contar_zero():
    with pytest.raises(AR.SemProcedencia):
        AR.leitura("1", api=lambda c: {"jobs": []})


def test_as_duas_leituras_sao_DELEGADAS_aos_donos():
    """Por AST: reparsear a forma da anotacao aqui criaria o segundo dono.

    O modulo CITA `::notice:: SOM` e `PUBLICADO` na prosa que explica o
    defeito, logo casar prosa pegaria a explicacao em vez do codigo — a licao
    do `test_NAO_virou_portao` do acento.
    """
    fonte = inspect.getsource(AR)
    arvore = ast.parse(fonte)
    chamadas = {ast.unparse(n.func) for n in ast.walk(arvore)
                if isinstance(n, ast.Call)}
    assert any(c.endswith("do_notice") for c in chamadas), chamadas
    assert any(c.endswith("linhas_dos_notices") for c in chamadas), chamadas
    for f in arvore.body:
        if isinstance(f, ast.FunctionDef) and f.name in (
                "_som_do_job", "publicado", "divergencias_de_job"):
            corpo = ast.unparse(f)
            for proibido in ("re.compile", "re.match", "json.loads", "open("):
                assert proibido not in corpo, (f.name, proibido)


def test_o_cruzamento_le_os_parques_pelo_CARREGA_de_cada_um():
    fonte = inspect.getsource(AR.divergencias_de_job)
    assert "DM.carrega()" in fonte and "SP.carrega()" in fonte, fonte


def test_os_dois_parques_do_disco_CONCORDAM_e_a_base_nao_e_vazia():
    d, s = DM.carrega(), SP.carrega()
    assert len(d) >= 50 and len(s) >= MINIMO_COMUNS, (len(d), len(s))
    cruz = AR.divergencias_de_job(d, s)
    assert cruz["comuns"] >= MINIMO_COMUNS, (
        "com poucos pacotes em comum o cruzamento passa por VACUIDADE: %r"
        % cruz)
    assert cruz["divergentes"] == [], cruz["divergentes"]


def test_divergencia_SEMEADA_e_nomeada_e_nao_calada():
    """Contraprova no outro sentido: sem ela bastaria devolver sempre `[]`."""
    d = [{"pacote": "p-s001", "job": "111"}]
    s = [{"pacote": "p-s001", "job": "222", "arquivo": "short.mp4",
          "pico_dbtp": -3.0}]
    cruz = AR.divergencias_de_job(d, s)
    assert cruz["comuns"] == 1
    assert cruz["divergentes"] == [{"pacote": "p-s001", "duracao": "111",
                                    "som": ["222"]}]
    # NAO ponho aqui um assert condicionado a `hasattr`: assert que se desliga
    # quando o atributo nao existe passa com qualquer coisa, e e o `or True` de
    # 16/10 — portao verde FABRICADO, num arquivo escrito para guardar o
    # oposto. A frase do relato tem teste proprio logo abaixo.


def test_o_relato_NOMEIA_a_concordancia_em_vez_de_calar():
    saida = AR.relato()
    assert "JOB nos DOIS parques" in saida
    assert "concordam" in saida or "DIVERGE" in saida


def test_a_medida_e_o_motivo_continuam_escritos_no_modulo():
    doc = AR.__doc__ or ""
    assert "65" in doc and "QUATRO" in doc, (
        "a medida que torna o achado grave nao pode envelhecer calada (753)")
    assert "VACUO" in doc.upper()
    assert "733" in doc
    assert "SORTE" in doc.upper(), (
        "a conclusao ter sobrevivido foi sorte, e isso vai dito")


def test_a_marca_do_733_e_a_mesma_do_emissor():
    import voz_piper
    assert AR.MARCA_PIPER in inspect.getsource(voz_piper), (
        "se a marca divergir do emissor, a contagem do provedor volta a ser"
        " zero por vacuidade — agora no outro lado")
