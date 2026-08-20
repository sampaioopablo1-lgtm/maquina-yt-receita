"""O guarda que faltava quando eu sobrescrevi um pacote publicado.

Em 20/08/2026 escolhi o numero `epomeno-epipedo-005` para um pacote novo sem
olhar quais existiam. O -005 existia, estava commitado e o video ja estava NO
AR. O build script reescreveu o `.json` inteiro e nenhum portao reclamou: os
portoes conferem se a spec esta CERTA, nao se ela e a spec CERTA.

O que me salvou foi acidente — a extracao das tags falhou e fui ver por que.
Estes testes existem para o proximo caso nao depender de sorte.
"""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import grava_spec as G  # noqa: E402


def _spec(pacote, titulo, slug="canal-teste"):
    return {"slug": slug, "pacote": pacote, "voz": "el-GR-NestorasNeural",
            "longo": [{"nar": "x"}], "short": [{"nar": "y"}],
            "copy": f"# {titulo}\n\n## TITULO\n{titulo}\n\n" + "-" * 600}


@pytest.fixture
def specs(tmp_path, monkeypatch):
    monkeypatch.setattr(G, "SPECS", tmp_path)
    return tmp_path


def test_recusa_gravar_por_cima_de_outro_video(specs):
    """O caso real: numero ocupado por um video que ja esta no ar."""
    G.grava(_spec("canal-teste-005", "Juros 2026: 0,03% e 14,49%"))
    with pytest.raises(SystemExit) as e:
        G.grava(_spec("canal-teste-005", "ENFIA: a isencao de 20%"))
    msg = str(e.value)
    assert "ja existe e e outro video" in msg
    # a mensagem tem de dizer o que fazer, nao so que deu errado
    assert "canal-teste-006" in msg, "precisa apontar o proximo numero livre"
    # e o arquivo em disco continua sendo o original
    disco = json.loads((specs / "canal-teste-005.json").read_text("utf-8"))
    assert "Juros 2026" in disco["copy"]


def test_reescrever_a_propria_spec_continua_livre(specs):
    """Revisar o roteiro do proprio pacote e o caso NORMAL e nao pode travar."""
    G.grava(_spec("canal-teste-005", "ENFIA: a isencao de 20%"))
    sp = _spec("canal-teste-005", "ENFIA: a isencao de 20%")
    sp["longo"] = [{"nar": "roteiro revisado"}]
    G.grava(sp)
    disco = json.loads((specs / "canal-teste-005.json").read_text("utf-8"))
    assert disco["longo"][0]["nar"] == "roteiro revisado"


def test_forcar_substitui_de_proposito(specs):
    G.grava(_spec("canal-teste-005", "Juros 2026"))
    G.grava(_spec("canal-teste-005", "ENFIA 2026"), forcar=True)
    disco = json.loads((specs / "canal-teste-005.json").read_text("utf-8"))
    assert "ENFIA" in disco["copy"]


def test_proximo_livre_e_max_mais_um_nao_o_primeiro_buraco(specs):
    """Buraco costuma ser pacote apagado de proposito. Reusar o numero
    misturaria dois historicos no mesmo nome."""
    for n in (2, 3, 5):
        G.grava(_spec(f"canal-teste-{n:03d}", f"video {n}"))
    assert G.ocupados("canal-teste") == [2, 3, 5]
    assert G.proximo_livre("canal-teste") == "canal-teste-006"


def test_canal_sem_nenhuma_spec_comeca_no_001(specs):
    assert G.proximo_livre("canal-novo") == "canal-novo-001"


def test_numero_de_pacote_bate_com_o_nome_do_arquivo():
    """Vale para o repositorio inteiro: spec cujo `pacote` interno diverge do
    nome do arquivo e spec que alguem copiou e esqueceu de renomear."""
    ruins = []
    for p in sorted((RAIZ / "fabrica" / "specs").glob("*-[0-9][0-9][0-9].json")):
        sp = json.loads(p.read_text(encoding="utf-8"))
        if sp.get("pacote") and sp["pacote"] != p.stem:
            ruins.append(f"{p.name}: pacote={sp['pacote']!r}")
    assert not ruins, "spec com pacote trocado:\n  " + "\n  ".join(ruins)
