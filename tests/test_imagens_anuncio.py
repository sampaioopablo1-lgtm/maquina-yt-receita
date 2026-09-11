"""A escolha da foto do anuncio, que e onde o criativo estraga em silencio.

O corte final e 1200x628 (1.91:1). Foto quase quadrada ou pequena passa no
download, entra no Meta e so aparece como erro quando metade do enquadramento
sumiu no crop — com verba ja gasta. Estes testes cercam os dois casos.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import imagens_anuncio as IA  # noqa: E402


def foto(larg, alt, fid=1):
    return {"id": fid, "width": larg, "height": alt, "photographer": "Fulano",
            "url": "https://pexels.com/photo/1",
            "src": {"large2x": "https://images.pexels.com/a.jpg"}}


def test_recusa_retrato():
    assert IA.escolher({"photos": [foto(1200, 1600)]}) is None


def test_recusa_quase_quadrada():
    # 1.33:1 sobrevive ao download e morre no corte para 1.91:1.
    assert IA.escolher({"photos": [foto(2000, 1500)]}) is None


def test_recusa_estreita_demais():
    # Proporcao certa, largura insuficiente: o crop tira e nao devolve.
    assert IA.escolher({"photos": [foto(1200, 628)]}) is None


def test_aceita_paisagem_grande():
    escolha = IA.escolher({"photos": [foto(2400, 1200, fid=7)]})
    assert escolha is not None
    link, credito = escolha
    assert link.endswith("a.jpg")
    assert credito["pexels_id"] == 7
    assert credito["autor"] == "Fulano"


def test_pula_a_ruim_e_pega_a_boa():
    dados = {"photos": [foto(1200, 1600, fid=1), foto(2400, 1200, fid=2)]}
    assert IA.escolher(dados)[1]["pexels_id"] == 2


def test_sem_foto_nao_levanta():
    assert IA.escolher({"photos": []}) is None
    assert IA.escolher({}) is None


def test_toda_peca_tem_busca_alternativa():
    # A alternativa e o que salva o run quando o termo principal volta so com
    # retrato: sem ela a peca some da entrega sem aviso.
    for nome, q, alt in IA.PECAS:
        assert q and alt and q != alt, nome
