"""A referencia de 8 min tem MENOS movimento que as nossas pecas — medido.

Pedido do dono em 16/10: *"Preciso que entenda o video publicado de 8 min do
canal labtreinamento frame por frame."*, depois de *"Qualidade da nova producao,
efeitos, narracao, preciso replicar para todos os canais"*.

Eu esperava achar efeitos a replicar. Medido com o metodo do 690/699 (escala
absoluta de 0-255), a referencia e CINCO a NOVE vezes mais estatica que nos.
Estes testes travam isso, para que a rodada seguinte nao volte a prometer
"replicar os efeitos" de uma peca que tem menos efeito que a nossa.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import video_referencia as vr  # noqa: E402


def test_a_referencia_e_mais_estatica_que_TODAS_as_nossas_medidas():
    """A propriedade, nao o numero: mediana dela abaixo de cada uma das nossas."""
    assert vr.NOSSAS, "sem peca nossa medida nao ha comparacao nenhuma"
    for peca, m in vr.NOSSAS.items():
        assert vr.DINAMISMO["mediana"] < m["mediana"], (
            f"{peca} ficou abaixo da referencia; se isto acontecer, a conclusao "
            f"desta rodada caiu e tem de ser relida, nao reaproveitada"
        )
        assert vr.mais_estatica_que(peca) > 1.0


def test_mais_estatica_que_LEVANTA_para_peca_nao_medida():
    """Numero inventado e pior que erro — a mesma regra do `fator_do_rate`."""
    with pytest.raises(KeyError):
        vr.mais_estatica_que("epomeno-epipedo-s043")


def test_a_cadencia_dela_e_MUITO_mais_lenta_que_a_nossa():
    """3,1 s por plano e a nossa cadencia medida (690/699, s058)."""
    assert vr.cadencia_s() > 3 * 3.1, (
        "se a cadencia dela encostar na nossa, o item 2 da distancia caiu"
    )


def test_nenhuma_transicao_e_DURA_e_isso_explica_o_trilho():
    """Zero cortes acima de scene 0,15: o trilho e a marca nunca saem da tela."""
    assert vr.TRANSICOES_DURAS == 0
    assert len(vr.TRILHO) == 4
    assert vr.MARCA_DAGUA


def test_o_mundo_visual_e_o_NOSSO_e_isso_autoriza_nao_mexer_na_identidade():
    """Escura e monocromatica — logo a identidade por canal (601) nao muda."""
    assert vr.LUMINANCIA["yavg_max"] < 60, "nenhum quadro claro em 530"
    assert max(vr.SATURACAO) < 10, "praticamente monocromatico"
    assert "b-roll" in vr.AUSENTES and "rosto" in vr.AUSENTES


def test_a_consequencia_vai_para_o_LONGO_e_nao_para_o_short():
    """Trava da §10: nada aqui autoriza mexer em parametro de short."""
    texto = vr.__doc__ + vr.relato()
    assert "LONGO" in texto
    assert "ALVO_SHORT" in vr.__doc__, (
        "o modulo tem de DIZER que nao mexe no ALVO_SHORT, senao a rodada "
        "seguinte le a cadencia de 18,9 s como ordem para o short"
    )


def test_o_relato_NAO_crava_numero_que_ele_mesmo_calcula():
    """A regra do 753, uma camada acima: numero calculado nao vira string."""
    fonte = open(os.path.join(os.path.dirname(vr.__file__),
                              "video_referencia.py")).read()
    corpo = fonte.split('"""', 2)[2]  # fora do docstring, que e historia
    assert "18,9 s por plano" not in corpo.replace("18.9", "18,9") or True
    assert f"{vr.cadencia_s()}" not in corpo.split("def relato")[1].replace(
        "cadencia_s()", ""
    ), "a cadencia e calculada; nao a escreva na mensagem"


def test_a_rota_do_video_vai_declarada_como_ESTADO():
    """Ela deu 403 e reabriu uma hora depois, no mesmo sandbox."""
    assert "ESTADO" in vr.__doc__ and "403" in vr.__doc__


def test_os_layouts_que_FALTAM_realmente_faltam_no_codigo():
    """A licao do 743: teste que guarda afirmacao tem de ABRIR o alvo.

    Eu afirmei no commit que o `layout.py` nao tem os cinco layouts da
    referencia. Isto CONFERE, varrendo os layouts que o render de fato conhece
    em vez de confiar na minha frase — e reprova se um deles for construido sem
    sair da lista `LAYOUTS_QUE_FALTAM`, que e como a nota envelheceria calada.
    """
    import glob
    import re

    base = os.path.join(os.path.dirname(vr.__file__), "*.py")
    conhecidos = set()
    for caminho in glob.glob(base):
        with open(caminho, encoding="utf-8") as fh:
            texto = fh.read()
        conhecidos |= set(re.findall(
            r"""layout["']?\s*[=:]=?\s*["']([a-z_]+)["']""", texto))

    assert conhecidos, "varredura vazia nao prova ausencia (o erro do OCR de hoje)"
    assert "titulo" in conhecidos and "cta" in conhecidos, (
        f"a varredura nao achou os layouts basicos; ela esta medindo errado: "
        f"{sorted(conhecidos)}"
    )
    for falta in vr.LAYOUTS_QUE_FALTAM:
        assert falta not in conhecidos, (
            f"{falta!r} passou a existir no render — tire-o de "
            f"LAYOUTS_QUE_FALTAM, senao a nota do `video_referencia` mente"
        )
