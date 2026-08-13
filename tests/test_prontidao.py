"""O medidor de prontidao nao pode aprovar o que o publicar.py reprova.

Ele existe para responder uma pergunta com numero — quantos pacotes a frota
dispara agora — e essa resposta so vale se os portoes dele forem os MESMOS que
a esteira aplica depois. Um medidor mais frouxo que a esteira e pior que nenhum:
ele promete pacotes que vao abortar depois do render.

Estes testes trancam a equivalencia nos dois pontos onde ela pode escorregar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao  # noqa: E402


def _spec_minima(**extra):
    base = {
        "slug": "nivel-do-jogo",
        "pacote": "nivel-do-jogo-002",
        "idioma": "pt-BR",
        "voz": "pt-BR-AntonioNeural",
        "paleta": {"ink": "#000", "c1": "#111", "c2": "#222", "bg": "#FFF"},
        "thumb": {"l1": "A", "l2": "B"},
        "longo": [{"layout": "titulo", "kicker": "k", "sub": "s", "nar": "Oi.",
                   "cap": "Um"}],
        "short": [],
    }
    base.update(extra)
    return base


def test_bilhete_reprova_no_portao_copy():
    """As specs com `copy` de bilhete abortam o publicar.py DEPOIS do render.

    O medidor tem que enxergar isso antes, senao ele conta como pronto um
    pacote que vai queimar dezessete minutos de runner e uma vaga de
    publicacao para morrer no fim.
    """
    faltas = prontidao._gate_copy(
        _spec_minima(copy="gerado a partir dos capitulos reais apos o render")
    )
    assert faltas and "bilhete" in faltas[0]


def test_descricao_curta_reprova():
    """A rotina pede descricao com 200+ palavras. Sete specs v1 tinham entre
    115 e 145 — passavam no publicar.py e mesmo assim nao servem."""
    copy = (
        "# t\n\n## TITULO\nUm titulo\n\n## DESCRICAO\n"
        + "palavra " * 50
        + "\n\n## TAGS\numa, duas, tres, quatro\n\n## HASHTAGS\n#a #b #c\n"
        "\n## COMENTARIO\nUma pergunta para o publico?\n"
    )
    faltas = prontidao._gate_copy(_spec_minima(copy=copy))
    assert any("200" in f for f in faltas), faltas


def test_tags_fora_do_orcamento_reprovam():
    """O limite de 500 do YouTube conta tag com espaco como len+2.

    orcamento_tags corta silenciosamente o que nao cabe; aqui o corte precisa
    virar reprovacao, porque tag cortada e busca perdida sem ninguem avisar.
    """
    tags = ", ".join(f"tag longa numero {i:02d} de teste" for i in range(30))
    copy = (
        "# t\n\n## TITULO\nUm titulo\n\n## DESCRICAO\n"
        + "palavra " * 250
        + f"\n\n## TAGS\n{tags}\n\n## HASHTAGS\n#a #b #c\n"
        "\n## COMENTARIO\nUma pergunta para o publico?\n"
    )
    faltas = prontidao._gate_copy(_spec_minima(copy=copy))
    assert any("orcamento" in f for f in faltas), faltas


def test_identidade_pega_pacote_divergente(tmp_path):
    caminho = tmp_path / "nivel-do-jogo-002.json"
    caminho.write_text(json.dumps(_spec_minima(pacote="outro-nome")), encoding="utf-8")
    faltas = prontidao._gate_identidade(str(caminho), json.loads(caminho.read_text()))
    assert any("pacote" in f for f in faltas)


def test_identidade_pega_idioma_divergente_do_canal(tmp_path):
    """A spec vence o config em publicar.py, entao spec errada nao e corrigida
    por ninguem: um video pt-BR subiria marcado como grego."""
    caminho = tmp_path / "nivel-do-jogo-002.json"
    caminho.write_text(json.dumps(_spec_minima(idioma="el")), encoding="utf-8")
    faltas = prontidao._gate_identidade(str(caminho), json.loads(caminho.read_text()))
    assert any("idioma" in f for f in faltas)


def test_falta_de_fonte_e_ambiente_e_nao_defeito_da_spec():
    """`usar_fonte` aborta sem a Noto Devanagari, que o agla-level pede.

    Se isso reprovasse a spec, a agla-level-003 apareceria como travada em toda
    maquina sem a fonte — e o frota.yml instala fonts-noto-core, que a traz.
    """
    faltas = prontidao._gate_layout(
        _spec_minima(fonte="Fonte Que Nao Existe Em Lugar Nenhum")
    )
    assert faltas and faltas[0].startswith("AMBIENTE")


SPECS_REAIS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))


@pytest.mark.parametrize(
    "spec",
    [p for p in SPECS_REAIS if json.loads(p.read_text(encoding="utf-8")).get("copy")
     and len(json.loads(p.read_text(encoding="utf-8"))["copy"]) > 200],
    ids=lambda p: p.stem,
)
def test_toda_spec_com_copy_real_passa_no_portao_copy(spec):
    """Regressao: uma spec que ja tem copy de verdade nao pode regredir.

    Cobre o caso que aconteceu de fato — parser de copy mudou e specs que
    publicavam pararam de publicar, sem teste nenhum reclamar.
    """
    sp = json.loads(spec.read_text(encoding="utf-8"))
    if not sp.get("longo"):
        pytest.skip("nao e spec de video")
    # As specs v1 sao as SEM sufixo -00N: sete pilotos com descricao entre 115 e
    # 145 palavras e sem hashtags. Elas nao vao a producao. O criterio e o nome,
    # nao a contagem de cenas — a epomeno-epipedo v1 tem 65 cenas e mesmo assim
    # e piloto, entao "poucas cenas" classificaria errado.
    if not re.search(r"-\d{3}$", spec.stem):
        pytest.skip("spec v1 sem sufixo de pacote, fora da producao")
    assert not prontidao._gate_copy(sp), f"{spec.stem}: {prontidao._gate_copy(sp)}"


def test_portao_de_glifos_morde_quando_nenhuma_fonte_cobre(monkeypatch):
    """A logica do portao, provada sem depender das fontes desta maquina.

    Nao da para exercitar isto com um caractere de verdade aqui: o container da
    sessao cobre TODO codepoint alfabetico testado (medido em 13/08/2026, nem
    Osage nem Cuneiforme ficam em zero). Um teste que dependesse disso passaria
    por acidente e nao provaria nada — entao a contagem de fontes e substituida.
    """
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    faltas = prontidao._gate_glifos(
        {"longo": [{"kicker": "abc"}], "short": [], "thumb": {}}
    )
    assert faltas and "tofu" in faltas[0]


def test_portao_de_glifos_ignora_o_nar_do_longo(monkeypatch):
    """O `nar` do longo vai para o .srt, que o YouTube renderiza com as fontes
    do espectador — nao passa pela fabrica e nao pode reprovar a spec."""
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    assert not prontidao._gate_glifos(
        {"longo": [{"nar": "texto so na narracao"}], "short": [], "thumb": {}}
    )


def test_portao_de_glifos_cobre_a_legenda_queimada_do_short(monkeypatch):
    """O `nar` do SHORT vira legenda queimada no pixel — esse entra."""
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    assert prontidao._gate_glifos(
        {"longo": [], "short": [{"nar": "legenda queimada"}], "thumb": {}}
    )


# --------------------------------------------------------------------------
# Thumbnail. A unica imagem que decide o clique, e ate 13/08/2026 nao passava
# por portao nenhum: o layout.py media as CENAS, o visual.py amostrava o VIDEO.

def _spec_thumb(l1, l2):
    return {"paleta": {"ink": "#102618", "c1": "#217346", "c2": "#F2B134",
                       "bg": "#F1F7F4"},
            "thumb": {"l1": l1, "l2": l2}, "longo": [], "short": []}


def test_thumbnail_com_titulo_de_duas_linhas_nao_colide():
    """O defeito real: com posicao fixa (l1 em y=300 corpo 150, l2 em y=480),
    a segunda linha do titulo caia em 487 — sete pixels DEPOIS do topo do
    subtitulo. Estava assim em todo pacote de titulo longo."""
    import layout as L

    assert not L.analisa_thumb(_spec_thumb("LICENCAS DORMINDO", "a planilha que acha"))


def test_geometria_do_thumb_mantem_as_faixas_separadas():
    """A conta e a fonte da verdade, e o portao le a MESMA conta que o desenho.

    Medir a imagem pronta nao serve: renderizar uma linha de cada vez para
    comparar faixas muda a geometria, porque ela depende das duas. Tentei
    assim primeiro e o portao reprovou as dezenove specs, inclusive as boas.
    """
    import fabrica as F

    for l1, l2 in [("R$ 333 MILHÕES", "a caixinha acabou"),
                   ("YOU ARE THE PRODUCT", "credit, explained"),
                   ("4 PILAR", "urutannya"),
                   ("UM TITULO BEM MAIS COMPRIDO QUE O NORMAL", "e um subtitulo longo tambem")]:
        g = F.geometria_thumb({"l1": l1, "l2": l2})
        assert g["base1"] <= g["topo2"], f"{l1!r} colide com {l2!r}"
        assert g["topo1"] >= 40 and g["base2"] <= 680, f"{l1!r} sai da caixa"


@pytest.mark.parametrize(
    "spec", [p for p in SPECS_REAIS
             if json.loads(p.read_text(encoding="utf-8")).get("longo")],
    ids=lambda p: p.stem,
)
def test_toda_spec_tem_thumbnail_legivel(spec):
    import layout as L

    assert not L.analisa_thumb(json.loads(spec.read_text(encoding="utf-8")))
