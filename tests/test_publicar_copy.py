"""O `copy` das specs e markdown; `publicar.py` so aceitava dict.

`cp["titulo"]` num str e TypeError, entao o passo "Publicar no YouTube" do
frota.yml nunca completou com nenhuma das 22 specs versionadas — o render de 13
minutos terminava e a publicacao morria na primeira linha.

Estes testes rodam contra as specs REAIS do repositorio, em sete idiomas, porque
o parse nao pode depender de cabecalho traduzido: as secoes se chamam TITULO,
TITLE, TÍTULO, ΤΙΤΛΟΣ, TYTUŁ e BAŞLIK, e as specs antigas tem 5 secoes em ordem
diferente das novas, que tem 9.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
SPECS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))


def _publicar():
    spec = importlib.util.spec_from_file_location(
        "fab_publicar", RAIZ / "fabrica" / "publicar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pub = _publicar()


def _com_copy_markdown():
    """Specs cujo `copy` traz as secoes de fato.

    Cinco specs guardam ali so um bilhete ("gerado a partir dos capitulos reais
    apos o render") — para elas o copy.md do render nao e preferencia, e
    requisito, e o teste disso e o _exige_copy_md abaixo.
    """
    for caminho in SPECS:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        copy = dados.get("copy")
        if isinstance(copy, str) and copy.count("\n## ") >= 2:
            yield pytest.param(caminho, id=caminho.stem)


def _so_bilhete():
    for caminho in SPECS:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        copy = dados.get("copy")
        if isinstance(copy, str) and copy.strip() and copy.count("\n## ") < 2:
            yield pytest.param(caminho, id=caminho.stem)


@pytest.mark.parametrize("caminho", list(_so_bilhete()))
def test_spec_sem_secoes_exige_o_copy_md_em_vez_de_publicar_o_bilhete(caminho, tmp_path):
    """"gerado a partir dos capitulos reais apos o render" nao e uma descricao.

    O codigo antigo publicaria essa frase como descricao do video sem reclamar.
    """
    spec = json.loads(caminho.read_text(encoding="utf-8"))

    with pytest.raises(SystemExit, match="copy.md"):
        pub.ler_copy(spec, str(tmp_path))


@pytest.mark.parametrize("caminho", list(_com_copy_markdown()))
def test_toda_spec_do_repo_rende_titulo_e_descricao(caminho, tmp_path):
    spec = json.loads(caminho.read_text(encoding="utf-8"))

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"], "titulo vazio publicaria video sem nome"
    assert len(cp["titulo"]) <= 100, "o YouTube corta em 100"
    assert "\n" not in cp["titulo"]
    assert len(cp["descricao"]) > 200, "a rotina pede 200+ palavras de descricao"


@pytest.mark.parametrize("caminho", list(_com_copy_markdown()))
def test_nenhum_placeholder_vaza_para_a_descricao(caminho, tmp_path):
    """`{CAPITULOS}` literal na descricao do YouTube e o defeito visivel."""
    spec = json.loads(caminho.read_text(encoding="utf-8"))

    cp = pub.ler_copy(spec, str(tmp_path))

    # Da spec cru o placeholder AINDA existe — o teste abaixo cobre o caminho
    # certo, com copy.md. Aqui so garantimos que nao inventamos outro.
    assert "PLACEHOLDER" not in cp["descricao"].upper()


def test_o_copy_md_do_render_vence_a_spec(tmp_path):
    """O render substitui {CAPITULOS} pelos tempos medidos nos clipes.

    A spec tem so o placeholder, entao publicar dela poria "{CAPITULOS}" na
    descricao do video. A ordem das fontes e o que evita isso.
    """
    spec = {"copy": "# T\n\n## TITULO\nDa spec\n\n## DESCRICAO\n" + "x" * 250}
    (tmp_path / "copy.md").write_text(
        "# T\n\n## BAŞLIK\nDo render\n\n## AÇIKLAMA\n" + "y" * 250
        + "\n\n## BÖLÜMLER\n0:00 Giris\n1:30 Bolum 1\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"] == "Do render"
    assert "0:00 Giris" in cp["descricao"], "capitulos cronometrados entram na descricao"


def test_capitulos_reais_entram_na_descricao(tmp_path):
    (tmp_path / "copy.md").write_text(
        "# T\n\n## TITLE\nT\n\n## DESCRIPTION\n" + "d" * 250
        + "\n\n## CHAPTERS\n0:00 Intro\n2:14 Part 1\n11:40 Close\n"
        "\n## HASHTAGS\n#a #b #c\n\n## TAGS\numa, duas, tres, quatro\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy({}, str(tmp_path))

    assert "11:40 Close" in cp["descricao"]
    assert cp["tags"] == ["uma", "duas", "tres", "quatro"]
    assert cp["hashtags"] == "#a #b #c"


def test_hashtag_nao_e_confundida_com_tag(tmp_path):
    """As duas secoes sao uma linha so; o que separa e o `#`."""
    (tmp_path / "copy.md").write_text(
        "# T\n\n## BAŞLIK\nT\n\n## AÇIKLAMA\n" + "d" * 250
        + "\n\n## ETİKETLER\n#AsgariUcret #Enflasyon #SeviyeSeviye\n"
        "\n## TAGS\nasgari ücret 2026, açlık sınırı, tüik, enflasyon\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy({}, str(tmp_path))

    assert cp["tags"][0] == "asgari ücret 2026"
    assert not any(t.startswith("#") for t in cp["tags"])


def test_dict_continua_funcionando(tmp_path):
    """Specs futuras podem trazer copy ja estruturado — nao quebrar quem migrar."""
    cp = pub.ler_copy({"copy": {"titulo": "T", "descricao": "D", "tags": ["a"]}},
                      str(tmp_path))

    assert cp["titulo"] == "T"


def test_sem_copy_nenhum_e_erro_claro(tmp_path):
    with pytest.raises(SystemExit, match="sem copy"):
        pub.ler_copy({}, str(tmp_path))


def test_orcamento_de_tags_conta_as_aspas():
    """O limite de 500 conta tag com espaco entre aspas (len+2); somar so os
    caracteres aprova lista que o YouTube rejeita."""
    tags = ["com espaco"] * 60

    mantidas, total = pub.orcamento_tags(tags)

    assert total <= 480
    assert all(len(t) + 2 for t in mantidas)


def test_a_spec_do_seviye_002_esta_publicavel(tmp_path):
    """O pacote da vez: seviye-seviye-002, asgari ucret x aclik siniri."""
    spec = json.loads(
        (RAIZ / "fabrica" / "specs" / "seviye-seviye-002.json").read_text(encoding="utf-8")
    )

    assert spec.get("pacote") == "seviye-seviye-002", "frota.yml resolve o workdir por `pacote`"
    assert spec.get("idioma") == "tr"

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"].startswith("Asgari ücret")
    assert len(cp["tags"]) == 15
    mantidas, total = pub.orcamento_tags(cp["tags"])
    assert total <= 480, f"orcamento estourado: {total}"
