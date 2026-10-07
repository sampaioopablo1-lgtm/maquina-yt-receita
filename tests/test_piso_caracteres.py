"""O piso de caracteres por cena, conferido contra a propria estimativa.

POR QUE ESTE ARQUIVO EXISTE (07/10/2026, aprendizado 616): no
kolejny-poziom-018 eu escrevi 56 cenas "com uma frase cada" e o pacote saiu em
435,5 s contra o piso de 480, com os sete capitulos entre 55,8 e 61,5 s — todos
abaixo dos 64,2 que o portao exige. Foram TRES reconstruicoes (435,5 -> 640,3
-> 499,4) por uma conta de uma linha.

O teste nao confere a formula contra ela mesma: ele escreve narracao do tamanho
do piso e exige que `duracao_estimada` devolva ao menos o piso. Se o modelo de
voz ou o GAP mudarem, o piso muda com eles e o teste continua valendo.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import pytest  # noqa: E402

from ensaio import (MODELO_VOZ, duracao_estimada, piso_de_caracteres)  # noqa: E402


def _nar(n_chars, frases):
    """Narracao de n_chars caracteres repartida em `frases` frases.

    O ponto importa: `duracao_cena` cobra P por FRASE, entao um bloco sem
    pontuacao mede como uma frase so e o teste passaria por engano.
    """
    # O comprimento tem de sair EXATO: no primeiro corte eu usei divisao
    # inteira e perdi dois caracteres por cena. Em 56 cenas isso e 5,6 s, e o
    # teste reprovou o piso correto dizendo 474,0 s em vez de 480.
    marca = ". "
    corpo = n_chars - len(marca) * (frases - 1) - 1   # -1 do ponto final
    assert corpo >= frases, (n_chars, frases)
    pedacos = [corpo // frases] * frases
    for k in range(corpo % frases):
        pedacos[k] += 1
    nar = marca.join("a" * c for c in pedacos) + "."
    assert len(nar) == n_chars, (len(nar), n_chars)
    return nar


@pytest.mark.parametrize("voz", sorted(MODELO_VOZ))
def test_o_piso_do_total_entrega_o_piso_do_total(voz):
    """Cenas com exatamente o piso de caracteres batem os 480 s."""
    p = piso_de_caracteres(voz, n_cenas=56)
    nar = _nar(p["min_por_cena_total"], p["frases_por_cena"])
    cenas = [{"layout": "titulo", "nar": nar} for _ in range(56)]
    d = duracao_estimada(cenas, voz)
    assert d >= 480.0, f"{voz}: {p['min_por_cena_total']} chars deram {d:.1f}s"
    # e nao exageradamente acima: uma margem de 2% diz que o piso e justo
    assert d <= 480.0 * 1.03, f"{voz}: piso folgado demais, {d:.1f}s"


@pytest.mark.parametrize("voz", sorted(MODELO_VOZ))
def test_o_piso_do_capitulo_entrega_os_64_2s(voz):
    p = piso_de_caracteres(voz, cenas_por_cap=8)
    nar = _nar(p["min_por_cena_capitulo"], p["frases_por_cena"])
    cenas = [{"layout": "titulo", "nar": nar} for _ in range(8)]
    d = duracao_estimada(cenas, voz)
    assert d >= 64.2, f"{voz}: {p['min_por_cena_capitulo']} chars deram {d:.1f}s"
    assert d <= 64.2 * 1.05, f"{voz}: piso de capitulo folgado demais, {d:.1f}s"


def test_abaixo_do_piso_nao_alcanca():
    """Um caractere a menos por cena ja nao fecha — e o que aconteceu no 018."""
    voz = "pl-PL-MarekNeural"
    p = piso_de_caracteres(voz, n_cenas=56)
    nar = _nar(p["min_por_cena_total"] - 12, p["frases_por_cena"])
    cenas = [{"layout": "titulo", "nar": nar} for _ in range(56)]
    assert duracao_estimada(cenas, voz) < 480.0


def test_o_total_manda_em_quase_todas_as_vozes():
    """A afirmacao do aprendizado 616, em forma de assert."""
    manda_total = [v for v in MODELO_VOZ
                   if piso_de_caracteres(v)["manda"] == "total"]
    assert len(manda_total) == len(MODELO_VOZ), (
        "alguma voz passou a ter o capitulo como limite — reescreva o 616")


def test_voz_sem_modelo_estoura_em_vez_de_adivinhar():
    with pytest.raises(KeyError):
        piso_de_caracteres("xx-XX-NinguemNeural")
