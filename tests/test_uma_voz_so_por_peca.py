"""UMA VOZ SO POR PECA — o provedor e da PECA, nao da cena.

Medido em 16/10/2026 e registrado em `test_o_run_pode_ser_MISTO.py`: tres pecas
do `labtreinamento` foram ao ar com 1-2 de 10 cenas pelo Piper (`faber`,
masculino) dentro da Thalita (feminina). Aquele arquivo tratou o misto como
problema de BANDA. Este trata o que ele tambem e: defeito audivel publicado.

A regra entrou por convergencia com o `pipeline_canal_dark_v2.0` (18/10), que a
escreve em letra ("uma voz so por video") — e a medicao que a justifica e nossa.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, "fabrica")
import voz_unica as VU  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]

# Os tres mistos publicados, na forma (cenas pelo Piper, total). Os indices das
# cenas nao estao na anotacao — so a contagem —, entao sao ilustrativos; a
# contagem e a medida.
MISTOS = {"labtreinamento-s060": ({3, 7}, 10),
          "labtreinamento-s061": ({5}, 10),
          "labtreinamento-s062": ({0, 9}, 10)}


def _vozes_fonte() -> str:
    texto = (RAIZ / "fabrica/fabrica.py").read_text()
    i = texto.index("async def vozes(")
    j = texto.index("\nfrom caminhos import", i)
    return texto[i:j]


def test_os_tres_regimes_do_733_e_mais_o_vazio():
    assert VU.regime(set(), 10) == "edge"
    assert VU.regime(set(range(10)), 10) == "piper"
    assert VU.regime({2}, 10) == "misto"
    assert VU.regime(set(), 0) == "nenhuma"
    assert set(VU.REGIMES) == {"nenhuma", "edge", "piper", "misto"}


def test_os_tres_mistos_publicados_sao_lidos_como_misto():
    for nome, (piper, total) in MISTOS.items():
        assert VU.regime(piper, total) == "misto", nome


def test_o_plano_do_misto_refaz_as_cenas_do_EDGE_e_fecha_em_piper():
    for nome, (piper, total) in MISTOS.items():
        pl = VU.plano(piper, total)
        assert pl["com"] == "piper", nome
        assert set(pl["refazer"]) == set(range(total)) - piper, nome
        # depois de refeito, a contagem do 733 e N, nao entre 0 e N
        assert VU.regime(piper | set(pl["refazer"]), total) == "piper", nome


def test_regime_puro_nao_refaz_nada():
    for piper in (set(), set(range(10))):
        pl = VU.plano(piper, 10)
        assert pl["refazer"] == [] and pl["com"] is None, pl


def test_a_marca_lateral_sobrevive_a_RETOMA(tmp_path):
    """O fabrica.py reaproveita mp3 valido de run anterior; sem a marca ele
    nao saberia que aquele mp3 e do Piper e a peca sairia mista outra vez."""
    alvo = str(tmp_path / "s03.mp3")
    assert not VU.marcado(alvo)
    VU.marcar(alvo)
    assert VU.marcado(alvo) and VU.marca(alvo).endswith(".mp3" + VU.MARCA)
    VU.desmarcar(alvo)
    assert not VU.marcado(alvo)
    VU.desmarcar(alvo)   # idempotente: desmarcar o que nao existe nao levanta


def test_o_fabrica_LE_a_marca_na_retoma_e_ESCREVE_ao_cair_no_piper():
    fonte = _vozes_fonte()
    assert "VU.marcado(alvo)" in fonte, "a retoma ignora quem narrou o mp3 antigo"
    assert fonte.count("VU.marcar(alvo)") >= 2, (
        "a marca tem de ser escrita nas DUAS quedas: a da cena e a da unificacao")


def test_o_fabrica_tenta_o_edge_UMA_vez_antes_de_unificar_para_o_piper():
    """Identidade (601) primeiro: a queda medida foi de 1-2 em 10, logo o edge
    estava de pe e vale um timeout por cena para a voz do canal voltar."""
    fonte = _vozes_fonte()
    i_retry = fonte.index("_edge_uma_vez(")
    i_unif = fonte.index('pl["refazer"]')
    assert i_retry < i_unif
    texto = (RAIZ / "fabrica/fabrica.py").read_text()
    assert "async def _edge_uma_vez(" in texto
    # escreve num temporario: uma queda no meio nao pode deixar mp3 pela metade
    # com cara de bom
    assert ".edge.tmp" in texto and "os.replace(tmp, alvo)" in texto


def test_o_aviso_do_733_sai_DEPOIS_da_unificacao_e_UMA_vez_por_cena():
    """Se o aviso sair na hora da queda, a anotacao conta um estado que a peca
    publicada nao tem — e a contagem deixa de ser 0 ou N."""
    fonte = _vozes_fonte()
    i_plano = fonte.index("VU.plano(")
    i_aviso = fonte.index("aviso_de_calibracao")
    assert i_plano < i_aviso
    assert fonte.count("aviso_de_calibracao") == 1, (
        "o aviso aparece em mais de um lugar: um deles conta estado intermediario")
    assert "for i in sorted(pela_piper):\n        print(VP.aviso_de_calibracao" in fonte


def test_unificacao_que_falha_LEVANTA_em_vez_de_publicar_misto():
    fonte = _vozes_fonte()
    assert "UMA VOZ SO: a cena" in fonte and "raise RuntimeError" in fonte


def test_o_piper_continua_sendo_fallback_e_nao_primeira_voz():
    """A trava do `test_voz_piper.py` continua valendo com a unificacao."""
    fonte = _vozes_fonte()
    assert fonte.index("edge_tts.Communicate") < fonte.index("voz_piper")
    assert "if tentativa == 2:" in fonte


def test_o_motivo_esta_escrito_no_modulo_com_as_tres_pecas():
    """Conserto sem motivo escrito volta calado (regra do 18/10 as 15:2x)."""
    fonte = (RAIZ / "fabrica/voz_unica.py").read_text()
    for peca in MISTOS:
        assert peca in fonte, peca
    assert "MASCULINA" in fonte and "FEMININA" in fonte
    assert "pipeline_canal_dark_v2.0" in fonte


def test_relato_diz_regime_contagem_e_recuperadas():
    r = VU.relato({1, 2}, 10, recuperadas=[4])
    assert "misto" in r and "2 de 10" in r and "1 cena(s) voltaram ao edge" in r
    assert "edge" in VU.relato(set(), 10)
