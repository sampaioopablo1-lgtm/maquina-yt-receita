"""A capa e a unica imagem que decide o clique, e ela saia pequena e cortada.

Medido em 18/08/2026, olhando as capas renderizadas em vez de so rodar portao.
Dois defeitos, e o segundo so existia por causa de uma constante.

1. TAMANHO. `geometria_thumb` tinha uma escada que so ENCOLHIA a partir de 150.
   Nas vinte e quatro specs de producao ela nunca disparou uma vez: as vinte e
   quatro paravam em 150, o teto. "61 HORAS" — sete caracteres — saia no mesmo
   corpo de um titulo de duas linhas, com metade do quadro em branco. No feed a
   capa aparece com 120 px de altura e ali so o tamanho decide. Agora a busca
   vai do maior para o menor: a mediana subiu de 150 para 206 e "4 PILAR" chega
   a 280.

2. LARGURA. A quebra era por CONTAGEM DE CARACTERE e a largura vinha de
   `LARGURA_GLIFO = 0,62`, medido em 'LabTreinamento' — caixa mista. Medida na
   fonte de producao, a razao real vai de 0,324 ('iiiiiiiiii') a 1,094
   ('WWWWWWWWWW'), com maiuscula em 0,704. Com 0,62 para tudo, 'BERAPA LAMA?'
   foi calculado em 1.101 px e renderizou com 1.251.

   O modo de falha e pior do que corte, e e por isso que ninguem tinha visto:
   `l2` e desenhado em `c1`, a MESMA cor da moldura. A linha que transborda nao
   sai cortada — sai INVISIVEL, verde sobre verde. Nenhuma varredura por
   luminancia distingue isso da moldura, e `analisa_thumb` so conferia a faixa
   VERTICAL da tinta. Por isso o portao novo mede a largura pela conta.

O terceiro item nao e defeito, e tipografia: 'x 4.503' vale mais que um 'x'
orfao no fim da linha de cima, porque o `x` E a comparacao do video.
"""

from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import fabrica as F  # noqa: E402

SPECS = [p for p in sorted((RAIZ / "fabrica" / "specs").glob("*.json"))
         if re.search(r"-\d{3}$", p.stem)
         and json.loads(p.read_text(encoding="utf-8")).get("thumb")]

UTIL = 1280 - 2 * 40          # a caixa branca, que e ate onde a tinta pode ir


@pytest.fixture
def fonte_latina():
    """Fixa a fonte, e devolve a anterior no fim.

    `F.FONTE` e global e `usar_fonte` nunca desfaz: basta um teste anterior
    medir a capa do agla-level, que declara Devanagari, para a familia ficar
    trocada pelo resto da sessao. Isolado, W mede 1.094 e i mede 324; depois de
    uma spec em Devanagari os dois mediram 581 — a largura de uma fonte de
    fallback monoespacada, onde W e i tem o mesmo avanco.

    Em producao isso nao morde, porque cada job cuida de UMA spec. Aqui morde,
    e o teste que afirma "a largura e medida" nao pode depender de qual spec
    passou antes dele.
    """
    antes = F.FONTE
    F.FONTE = "DejaVu Sans"
    yield
    F.FONTE = antes


# --- largura: o defeito que sumia em vez de aparecer -------------------------

@pytest.mark.parametrize("spec", SPECS, ids=lambda p: p.stem)
def test_nenhuma_linha_da_capa_passa_da_caixa_branca(spec):
    """O que sobra da caixa cai na moldura, e em `c1` a sobra fica INVISIVEL."""
    sp = json.loads(spec.read_text(encoding="utf-8"))
    F.usar_fonte(sp.get("fonte", ""))          # a mesma que o portao usa
    g = F.geometria_thumb(sp["thumb"], 720)
    for rotulo, linhas, corpo in (("l1", g["l1"], g["s1"]),
                                  ("l2", g["l2"], g["s2"])):
        for linha in linhas:
            larg = F.largura_do_texto(linha, corpo)
            assert larg <= UTIL, f"{rotulo} {linha!r}: {larg:.0f} px de {UTIL}"


def test_a_largura_e_medida_e_nao_uma_constante(fonte_latina):
    """Se `largura_do_texto` voltar a ser `len(t) * size * 0,62`, estas tres
    medidas viram a mesma e o defeito volta calado."""
    caixa_alta = F.largura_do_texto("WWWWWWWWWW", 100)
    caixa_baixa = F.largura_do_texto("iiiiiiiiii", 100)
    assert caixa_alta > 2 * caixa_baixa, (
        f"W={caixa_alta:.0f} e i={caixa_baixa:.0f} — a largura nao esta sendo "
        f"medida, esta sendo estimada por contagem de caractere")


def test_a_constante_antiga_erraria_este_caso(fonte_latina):
    """O caso exato que cortou o setiap-level-007, com o numero na mao."""
    real = F.largura_do_texto("BERAPA LAMA?", 148)
    estimado = len("BERAPA LAMA?") * 148 * F.LARGURA_GLIFO
    assert real > estimado, f"real {real:.0f} <= estimado {estimado:.0f}"


def test_a_largura_escala_linear_com_o_corpo(fonte_latina):
    """A regra de tres do cache so vale porque fonte vetorial escala linear.
    Se um dia a medida passar a vir de bitmap, este teste cai antes do render."""
    a = F.largura_do_texto("BERTAHAN", 100)
    b = F.largura_do_texto("BERTAHAN", 200)
    assert abs(b - 2 * a) <= 0.02 * b, f"{a:.1f} e {b:.1f} nao sao proporcionais"


# --- tamanho: a escada que nunca disparou ------------------------------------

def test_titulo_curto_cresce_muito_acima_do_teto_antigo(fonte_latina):
    """'61 HORAS' cabia em 240 e saia em 150 porque 150 era o topo da escada."""
    g = F.geometria_thumb({"l1": "61 HORAS", "l2": "DE TRABALHO"}, 720)
    assert g["s1"] > 190, f"corpo {g['s1']} — a busca nao esta crescendo"


def test_titulo_longo_ainda_encolhe(fonte_latina):
    """Crescer nao pode custar a protecao antiga: capa cortada continua pior
    que capa pequena."""
    g = F.geometria_thumb({"l1": "UM TITULO BEM MAIS COMPRIDO QUE O NORMAL",
                           "l2": "e um subtitulo longo tambem"}, 720)
    assert g["topo1"] >= 40 and g["base2"] <= 680
    assert g["base1"] <= g["topo2"]


def test_a_mediana_do_corpo_subiu_bem_acima_do_teto_antigo(fonte_latina):
    """150 era o corpo de TODAS as vinte e quatro, porque era o topo da escada.
    A medida que importa e a do conjunto, e nao a de uma capa: crescer o titulo
    curto sem encolher o longo e o resultado inteiro."""
    import statistics

    corpos = []
    for p in SPECS:
        sp = json.loads(p.read_text(encoding="utf-8"))
        F.usar_fonte(sp.get("fonte", ""))
        corpos.append(F.geometria_thumb(sp["thumb"], 720)["s1"])
    assert statistics.median(corpos) > 190, corpos


def test_o_unico_que_encolheu_encolheu_com_razao(fonte_latina):
    """labtreinamento-002 e a excecao, e ela e a PROVA e nao o contraexemplo:
    'PSICOSSOCIAL' mede 1.212 px no corpo 150 — mais larga que a caixa branca
    inteira. O 150 antigo ja estava derramando na moldura; 140 e o primeiro
    corpo em que a palavra cabe de verdade."""
    assert F.largura_do_texto("PSICOSSOCIAL", 150) > UTIL
    g = F.geometria_thumb({"l1": "NR-1 PSICOSSOCIAL",
                           "l2": "o inventario que falta"}, 720)
    assert g["s1"] < 150
    assert F.largura_do_texto("PSICOSSOCIAL", g["s1"]) <= UTIL


# --- a linha orfa ------------------------------------------------------------

def test_o_x_da_comparacao_nao_fica_orfao(fonte_latina):
    """'10.685 x' / '4.503' partia a comparacao ao meio — e a comparacao e o
    video inteiro."""
    g = F.geometria_thumb({"l1": "10.685 x 4.503", "l2": "concurso ou CLT"}, 720)
    assert len(g["l1"]) == 2
    assert not g["l1"][0].split()[-1] == "x", g["l1"]
    assert g["l1"][1].startswith("x"), g["l1"]


def test_a_palavrinha_nao_desce_se_estourar_a_linha_de_baixo(fonte_latina):
    """Consertar orfao nao pode virar estouro de largura: quando nao cabe, o
    orfao fica onde esta."""
    linhas = F._sem_orfao(["AAAA =", "BBBBBBBB"], 100, F.largura_do_texto("BBBBBBBB", 100))
    assert linhas == ["AAAA =", "BBBBBBBB"]


def test_linha_de_uma_palavra_so_nunca_esvazia(fonte_latina):
    """'2%' e a linha inteira; descer ela deixaria a primeira linha vazia, e
    linha vazia empurra o bloco para fora do quadro."""
    assert F._sem_orfao(["2%", "ROCZNIE"], 100, 10_000) == ["2%", "ROCZNIE"]


# --- quem mede e quem desenha olham as mesmas linhas -------------------------

def test_o_desenho_usa_as_linhas_que_a_geometria_quebrou():
    """Antes o `svg_thumb` refazia o `wrap` com outro `n`. Funcionava por
    coincidencia: bastava discordarem de uma linha para o portao aprovar uma
    capa colidindo."""
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text(encoding="utf-8")
    corpo = fonte.split("def svg_thumb")[1].split("\ndef ")[0]
    # sem os comentarios: eles CITAM o `n=12` antigo para explicar por que ele
    # saiu, e a citacao nao pode reprovar o teste
    codigo = "\n".join(l for l in corpo.splitlines() if not l.strip().startswith("#"))
    assert 'g["l1"]' in codigo and 'g["l2"]' in codigo, codigo
    assert "n=12" not in codigo and "n=16" not in codigo, "voltou a quebrar sozinho"


def test_o_portao_reprova_uma_capa_larga_demais(fonte_latina):
    """O portao novo, contra o caso que ele existe para pegar."""
    import layout as L

    sp = {"paleta": {"ink": "#10261C", "c1": "#217346", "c2": "#F2B134",
                     "bg": "#F1F7F4"},
          "thumb": {"l1": "OK", "l2": "OK"}}
    assert not L.analisa_thumb(sp)

    # uma palavra sozinha, larga demais para qualquer corpo da busca
    sp["thumb"] = {"l1": "W" * 60, "l2": "ok"}
    assert L.analisa_thumb(sp)
