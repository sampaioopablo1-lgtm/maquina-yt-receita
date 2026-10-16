"""Trava o estudo do prompt que o dono trouxe em 16/10.

Testavel SEM gastar credito: o montador e transformacao de texto. O que ele
guarda e o que eu nao posso esquecer quando o credito existir — o aspecto por
formato, a proibicao de texto na imagem, e a recusa de ilustrar cena sem fala.
"""
import json
import pathlib
import sys

import pytest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import estilo_paint as E  # noqa: E402


def _spec(pacote):
    with open(RAIZ / "fabrica" / "specs" / f"{pacote}.json", encoding="utf-8") as fh:
        return json.load(fh)


def test_o_aspecto_vem_do_FORMATO_e_nao_do_prompt():
    """O prompt do dono diz 16:9 porque descreve o LONGO; o short e 9:16."""
    assert E.aspecto_da_peca(_spec("labtreinamento-s060")) == "9:16"
    assert E.aspecto_da_peca({"longo": [{"nar": "x"}]}) == "16:9"


def test_a_imagem_sai_SEM_TEXTO():
    """A regra da casa, e ela tem motivo: dois tercos da frota nao e latim."""
    p = E.prompt_da_cena({"nar": "A posição anda com a tabela."})
    assert "no text" in p.lower()
    assert "no letters" in p.lower()


def test_o_prompt_carrega_a_PROIBICAO_inteira():
    """Sem as proibicoes o gerador 'melhora' o desenho e perde o ponto."""
    p = E.prompt_da_cena({"nar": "qualquer coisa"})
    for proibido in ("no 3D", "no Disney", "no anime", "no polished",
                     "intentionally bad"):
        assert proibido.lower() in p.lower(), proibido


def test_cena_sem_fala_LEVANTA():
    with pytest.raises(ValueError):
        E.prompt_da_cena({"kicker": "só tela", "nar": "   "})


def test_um_pedido_por_cena_com_indice_estavel():
    sp = _spec("labtreinamento-s060")
    pedidos = E.prompts_da_spec(sp)
    assert len(pedidos) == len(sp["short"])
    assert [p["index"] for p in pedidos] == list(range(len(sp["short"])))
    # a fala da cena entra no prompt dela, nao a de outra
    assert sp["short"][3]["nar"].rstrip(".") in pedidos[3]["params"]["prompt"]


def test_o_custo_sai_MEDIDO_e_nao_estimado():
    sp = _spec("labtreinamento-s060")
    assert E.CREDITO_POR_IMAGEM == 0.25          # preflight de 16/10
    assert E.custo(sp) == len(sp["short"]) * 0.25


def test_o_relato_diz_a_rota_e_o_que_acontece_se_a_imagem_faltar():
    texto = E.relato(_spec("labtreinamento-s060"))
    assert "broll_url" in texto
    assert "NAO para" in texto
    assert "SEM TEXTO" in texto


def test_o_modulo_nomeia_o_bloqueio_de_credito():
    """Se alguem ler so o codigo, tem de topar com o motivo de nada ter rodado."""
    doc = E.__doc__
    assert "ZERO" in doc and "free" in doc
