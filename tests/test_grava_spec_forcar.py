"""A trava anti-sobrescrita estava DESLIGADA em 114 dos 166 builders.

Medido em 12/10/2026. A assinatura era `grava(spec, forcar=False)`, e a
convencao dos builders era chamar
`grava(SPEC, "fabrica/specs/<pacote>.json")` — passando um CAMINHO na posicao do
`forcar`. String nao vazia e verdadeira, logo esses builders rodavam com
`forcar=True` e **pulavam a conferencia inteira**.

A trava existe por causa do defeito de 19/08: o `kolejny-poziom-007` renderizou
89 cenas e dezessete minutos de runner para so entao descobrir que o nome ja
pertencia a um video de 11/08. Ela estava desligada justamente nos builders que
a usariam — e silenciosamente, porque so morde quando um numero colide, que e
exatamente quando ninguem esta olhando.

Conserto: `forcar` virou KEYWORD-ONLY e o `caminho` deixou de ser ignorado,
passando a ser CONFERIDO contra o destino derivado do `pacote`. Medido antes de
mudar: nos 114 builders que passam caminho, ele bate com o derivado em 114 de
114, entao a conferencia nao quebra ninguem.
"""

import inspect
import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import grava_spec  # noqa: E402

# `_titulo` le a PRIMEIRA linha que comeca com `#` — e a copy de producao
# abre com `# <titulo>`. Fixture com o mesmo `# a` nos dois nao exercita
# nada: `tv == tn` e a conferencia passa de largo.
COPY_A = "# Titulo Um\n\ncorpo\n"
COPY_B = "# Titulo Dois, outro video\n\ncorpo\n"


def _spec(copy):
    return {"pacote": "teste-trava-001", "slug": "teste-trava", "copy": copy,
            "short": [], "longo": []}


def test_forcar_e_KEYWORD_ONLY():
    """Posicional e o que deixava um caminho virar forcar=True."""
    p = inspect.signature(grava_spec.grava).parameters
    assert p["forcar"].kind is inspect.Parameter.KEYWORD_ONLY


def test_passar_CAMINHO_nao_desliga_mais_a_trava(tmp_path, monkeypatch):
    """O caso real: 114 builders faziam exatamente esta chamada."""
    monkeypatch.setattr(grava_spec, "SPECS", tmp_path)
    grava_spec.grava(_spec(COPY_A), "fabrica/specs/teste-trava-001.json")
    with pytest.raises(SystemExit) as e:
        grava_spec.grava(_spec(COPY_B), "fabrica/specs/teste-trava-001.json")
    assert "ja existe e e outro video" in str(e.value)


def test_reescrever_a_PROPRIA_spec_continua_livre(tmp_path, monkeypatch):
    """O caso normal: mesmo titulo, roteiro revisado."""
    monkeypatch.setattr(grava_spec, "SPECS", tmp_path)
    grava_spec.grava(_spec(COPY_A), "fabrica/specs/teste-trava-001.json")
    grava_spec.grava(_spec(COPY_A), "fabrica/specs/teste-trava-001.json")


def test_forcar_por_palavra_chave_continua_funcionando(tmp_path, monkeypatch):
    monkeypatch.setattr(grava_spec, "SPECS", tmp_path)
    grava_spec.grava(_spec(COPY_A), "fabrica/specs/teste-trava-001.json")
    grava_spec.grava(_spec(COPY_B), forcar=True)


def test_caminho_que_NAO_e_o_destino_e_recusado(tmp_path, monkeypatch):
    """Argumento inerte virou verificacao."""
    monkeypatch.setattr(grava_spec, "SPECS", tmp_path)
    with pytest.raises(SystemExit) as e:
        grava_spec.grava(_spec(COPY_A), "fabrica/specs/outro-pacote-999.json")
    assert "nao e o destino desta spec" in str(e.value)


def test_os_builders_que_passam_caminho_batem_com_o_pacote():
    """Medido: 114 de 114. Se um divergir, a conferencia nova o pega — e este
    teste diz ANTES, no commit, em vez de no proximo build."""
    div = []
    for p in sorted((RAIZ / "fabrica/specs").glob("*.build.py")):
        t = p.read_text()
        m = re.search(r'grava\(SPEC,\s*"([^"]+)"', t)
        if not m:
            continue
        pac = re.search(r'"pacote":\s*"([^"]+)"', t)
        if not pac:
            div.append((p.name, "sem pacote legivel"))
            continue
        if m.group(1) != f"fabrica/specs/{pac.group(1)}.json":
            div.append((p.name, m.group(1), pac.group(1)))
    assert not div, div


def test_a_PROCEDENCIA_do_conserto_esta_escrita():
    fonte = (RAIZ / "fabrica/grava_spec.py").read_text()
    assert "114" in fonte and "166" in fonte
    assert "19/08" in fonte, "o motivo da trava tem de ficar escrito"
    assert "KEYWORD-ONLY" in fonte
