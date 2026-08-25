"""Capitulo perdido por TEMPO tem de ser acusado, e nomeado pelo nome certo.

MEDIDO EM 25/08/2026, na kolejny-poziom-011: dez capitulos desenhados, CINCO
produzidos, e o portao calado. Duas coisas conspiraram:

  1. o teto do portao era 8, e a spec tinha 10 — ele nem olhava;
  2. a causa nao era layout. As dez aberturas estavam em `titulo`, certinhas.
     O que derrubava era a DISTANCIA: `copy_md.capitulos` so abre capitulo
     `MIN_CAP` segundos depois do anterior, e capitulos de 56 a 58 s sumiam.

O teto de 8 nao era arbitrario — era a faixa que a rotina pedia. Mas a rotina
mudou no mesmo dia, por medida: o longo de melhor retencao do canal tem NOVE
capitulos e o de pior tem sete, entao ela passou a pedir MAIS capitulos. O
portao ficou, portanto, calado exatamente na faixa que a rotina agora
considera boa — e mais capitulos no mesmo video encurta cada um, que e
justamente o que faz este modo de falha aparecer.

O custo de nao acusar: descricao publicada com metade dos capitulos, e o
espectador sem como navegar um video de doze minutos. O custo de acusar com a
mensagem errada ("abertura tem de ser `titulo`") e mandar o autor conferir o
que ja esta certo.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import prontidao as P  # noqa: E402

VOZ = "pl-PL-MarekNeural"

# ~66 s de narracao nesta voz: acima do piso de 60 s do copy_md, com folga
# para o erro de ~2% do modelo.
LONGA = ("Podstawa sto tysiecy zlotych i dwanascie procent z tej kwoty. " * 15)
# ~28 s: abaixo do piso, e o capitulo que abre depois dela some.
CURTA = ("Podstawa sto tysiecy zlotych i dwanascie procent z tej kwoty. " * 5)


def _spec(duracoes, n_caps=10, layout="titulo"):
    """n_caps capitulos, cada um com uma cena de abertura e uma de corpo."""
    cenas = []
    for i, corpo in enumerate(duracoes):
        cenas.append({"layout": layout if i else "titulo", "kicker": f"k{i}",
                      "sub": "s", "nar": "Otwarcie rozdzialu.", "cap": f"cap{i}"})
        cenas.append({"layout": "item", "kicker": f"i{i}", "preco": "p",
                      "nar": corpo, "sem_cap": True})
    return {"voz": VOZ, "longo": cenas}


def test_dez_capitulos_folgados_passam():
    """A faixa nova tem de deixar passar o que esta certo."""
    assert P._gate_capitulos(_spec([LONGA] * 10)) == []


def test_dez_capitulos_apertados_sao_acusados():
    """Era este o silencio: 10 estava acima do teto de 8, e ninguem via."""
    faltas = P._gate_capitulos(_spec([CURTA] * 10))
    assert faltas, "dez capitulos apertados nao podem passar calados"


def test_a_mensagem_culpa_a_distancia_e_nao_o_layout():
    """Com todas as aberturas em `titulo`, culpar layout manda o autor no rumo errado."""
    msg = P._gate_capitulos(_spec([CURTA] * 10))[0]
    assert "DISTANCIA" in msg
    assert "layout que o render ignora" not in msg


def test_a_mensagem_nomeia_os_capitulos_curtos_e_o_tamanho():
    """Sem o nome e o numero, o autor tem de reencontrar sozinho o que ja foi medido."""
    msg = P._gate_capitulos(_spec([CURTA] * 10))[0]
    assert "'cap1'" in msg and "dura" in msg


def test_layout_errado_continua_culpando_o_layout():
    """A correcao nao pode apagar o diagnostico que ja existia (aprendizado 311)."""
    msg = P._gate_capitulos(_spec([LONGA] * 10, layout="item"))[0]
    assert "layout que o render ignora" in msg
    assert "DISTANCIA" not in msg


def test_treze_capitulos_continuam_fora_da_faixa():
    """Acima de 12, `cap` volta a ser marcador solto do acervo antigo."""
    assert P._gate_capitulos(_spec([CURTA] * 13)) == []


def test_a_spec_real_passa():
    """O portao novo tem de aprovar a spec que o motivou, ja corrigida."""
    import json

    caminho = os.path.join(RAIZ, "fabrica/specs/kolejny-poziom-011.json")
    if not os.path.exists(caminho):
        return
    sp = json.load(open(caminho, encoding="utf-8"))
    assert sum(1 for c in sp["longo"] if c.get("cap")) == 10
    assert P._gate_capitulos(sp) == []
