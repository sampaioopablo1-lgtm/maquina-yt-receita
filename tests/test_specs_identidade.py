"""Toda spec tem que saber QUEM ela e e em que LINGUA fala.

Dois campos, dois defeitos silenciosos — silenciosos e o que importa aqui: os
dois publicam ou entregam coisa errada sem levantar erro nenhum, e so aparecem
assistindo ao video pronto ou olhando a pagina do YouTube depois.

`pacote` decide o diretorio de trabalho. Sem ele, `dir_trabalho` cai no slug do
CANAL, e dois pacotes do mesmo canal dividem /tmp/f/<slug>: o RETOMA da fabrica
encontra clipes do pacote ANTERIOR ja renderizados, pula a geracao e costura
dois roteiros num video so. Em 13/08/2026 treze das vinte e quatro specs nao
declaravam `pacote`, e quatro pares colidiam — entre eles setiap-level-003 (166
cenas) e setiap-level-004 (196 cenas), os dois maiores pacotes do repositorio.

Ha um segundo estrago no mesmo campo: o frota.yml entrega e sobe artefato de
`/tmp/f/${{ matrix.pacote }}`, caminho que nao existiria. O laco de entrega usa
`[ -f ... ] || continue`, entao o job terminaria VERDE sem ter entregue nada.

`idioma` decide defaultLanguage, defaultAudioLanguage e a lingua da faixa de
legenda. A fonte de verdade e config/canais/<slug>.yaml, onde os treze canais
declaram idioma desde sempre — a matriz do frota.yml repetia esse valor a mao.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
SPECS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))


def _carrega(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# pastas.json nao tem cenas: e configuracao, nao pacote de video.
DE_VIDEO = [p for p in SPECS if _carrega(p).get("longo")]


@pytest.mark.parametrize("spec", DE_VIDEO, ids=lambda p: p.stem)
def test_spec_declara_pacote_igual_ao_nome_do_arquivo(spec):
    """O `pacote` e o nome do arquivo — e a matriz do frota.yml usa esse nome.

    Se divergirem, o render escreve num diretorio e a entrega procura noutro.
    """
    assert _carrega(spec).get("pacote") == spec.stem, (
        f"{spec.name} nao declara pacote={spec.stem!r}; sem ele o render cai no "
        f"diretorio do canal e o frota.yml entrega de um caminho que nao existe"
    )


def test_nenhum_par_de_specs_divide_diretorio_de_trabalho():
    por_dir = defaultdict(list)
    for p in DE_VIDEO:
        s = _carrega(p)
        por_dir[s.get("pacote") or s["slug"]].append(p.stem)
    colisoes = {d: v for d, v in por_dir.items() if len(v) > 1}
    assert not colisoes, (
        f"pacotes dividindo workdir (o RETOMA costuraria os dois roteiros): {colisoes}"
    )


@pytest.mark.parametrize("spec", DE_VIDEO, ids=lambda p: p.stem)
def test_idioma_da_spec_bate_com_o_do_canal(spec):
    """Quando a spec declara `idioma`, tem que ser o do canal.

    A spec vence o config em `publicar.py` — entao uma spec com idioma errado
    nao seria corrigida por ninguem.
    """
    import sys

    sys.path.insert(0, str(RAIZ / "fabrica"))
    from publicar import idioma_do_canal

    s = _carrega(spec)
    do_canal = idioma_do_canal(s["slug"])
    assert do_canal, f"canal {s['slug']} sem idioma em config/canais/"
    if s.get("idioma"):
        assert s["idioma"] == do_canal, (
            f"{spec.name} declara idioma={s['idioma']!r} mas o canal {s['slug']} "
            f"e {do_canal!r}; a spec vence o config, entao isto publicaria errado"
        )


def test_publicar_nao_tem_default_de_idioma():
    """Nao ha idioma seguro por omissao.

    O codigo antigo caia em "en" quando ninguem dizia nada, e como 21 das 24
    specs nao declaravam idioma, um disparo sem --idioma poria video em grego,
    hindi ou polones no ar marcado como ingles.
    """
    fonte = (RAIZ / "fabrica" / "publicar.py").read_text(encoding="utf-8")
    assert 'sp.get("idioma") or "en"' not in fonte
    assert "idioma indefinido" in fonte, (
        "publicar.py precisa parar quando nao consegue resolver o idioma"
    )


def test_idioma_do_canal_nao_depende_de_pyyaml():
    """O passo de publicacao do frota.yml instala edge-tts, cairosvg, pydantic e
    pillow — nao instala PyYAML.

    Um `import yaml` em publicar.py so quebraria DEPOIS do render, que e o
    momento mais caro possivel para descobrir uma dependencia faltando. Foi
    exatamente assim que o reparar-copy morreu com `import cairosvg`.
    """
    import ast

    arvore = ast.parse((RAIZ / "fabrica" / "publicar.py").read_text(encoding="utf-8"))
    importados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module:
            importados.add(no.module.split(".")[0])

    pesados = {"yaml", "cairosvg", "edge_tts", "PIL", "pydantic", "fabrica"}
    assert not (importados & pesados), (
        f"publicar.py importa {importados & pesados}; a publicacao roda depois do "
        f"render e nao pode morrer por dependencia que o workflow nao instala"
    )


def test_publicar_resolve_idioma_dos_treze_canais():
    import sys

    sys.path.insert(0, str(RAIZ / "fabrica"))
    from publicar import idioma_do_canal

    canais = sorted(p.stem for p in (RAIZ / "config" / "canais").glob("*.yaml"))
    assert len(canais) == 13, f"esperava 13 canais, achei {len(canais)}"
    for slug in canais:
        assert idioma_do_canal(slug), f"{slug} sem idioma legivel"
    assert idioma_do_canal("canal-que-nao-existe") == ""
