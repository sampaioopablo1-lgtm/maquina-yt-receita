# -*- coding: utf-8 -*-
"""O ";" grego encerra frase; nas outras linguas nao.

Aprendizado 313: FIM_DE_FRASE ignorava o ponto de interrogacao grego, que e
";" (U+003B) e o codepoint dedicado U+037E. A contagem de frases alimenta tres
portoes e o termo `frases x P` do modelo de duracao.

Uma troca GLOBAL consertaria o grego e quebraria polones, portugues e
indonesio, onde ";" e ponto-e-virgula comum.
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fabrica"))

from narracao import FIM_DE_FRASE, frases  # noqa: E402
from ensaio import MODELO_VOZ, duracao_cena  # noqa: E402


def test_pergunta_grega_encerra_frase():
    assert len(frases("Ας δούμε; Και μετά.", "el")) == 2


def test_codepoint_dedicado_tambem_encerra():
    """U+037E e canonicamente equivalente ao ";" e aparece em texto real."""
    assert len(frases("Ας δούμε; Και μετά.", "el")) == 2


def test_ponto_e_virgula_polones_NAO_encerra():
    assert len(frases("Jedno; drugie. Trzecie.", "pl")) == 2


def test_ponto_e_virgula_indonesio_NAO_encerra():
    assert len(frases("Satu; dua. Tiga.", "id")) == 2


def test_ponto_e_virgula_portugues_NAO_encerra():
    assert len(frases("Um; dois. Tres.", "pt-BR")) == 2


def test_idioma_desconhecido_cai_no_padrao():
    assert frases("A; b. C.", "xx") == frases("A; b. C.")


def test_sem_idioma_mantem_comportamento_antigo():
    assert len(frases("Ας δούμε; Και μετά.")) == 1


def test_danda_do_hindi_continua_encerrando():
    """O conserto do grego nao pode desfazer o do devanagari."""
    assert len(frases("पहला। दूसरा।", "hi")) == 2


def test_tabela_tem_o_padrao_sob_None():
    assert None in FIM_DE_FRASE
    assert ";" not in FIM_DE_FRASE[None]
    assert ";" in FIM_DE_FRASE["el"]


def test_duracao_usa_o_divisor_do_idioma_da_voz():
    """duracao_cena tira o idioma do prefixo da voz, sem parametro novo."""
    texto = "Ας δούμε; Και μετά."
    R, P = MODELO_VOZ["el-GR-NestorasNeural"]
    # duas frases, nao uma
    assert abs(duracao_cena(texto, "el-GR-NestorasNeural")
               - (len(texto) / R + 2 * P)) < 1e-9


def test_voz_polonesa_nao_ganha_frase_extra():
    texto = "Jedno; drugie. Trzecie."
    R, P = MODELO_VOZ["pl-PL-MarekNeural"]
    assert abs(duracao_cena(texto, "pl-PL-MarekNeural")
               - (len(texto) / R + 2 * P)) < 1e-9


def test_todas_as_vozes_da_frota_estao_medidas():
    """Voz sem medicao dimensiona roteiro no escuro."""
    import glob
    import json
    faltando = set()
    for p in glob.glob(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "fabrica", "specs", "*.json")):
        sp = json.load(open(p, encoding="utf-8"))
        # Nem todo .json em specs/ e uma spec de pacote; so cobra quem
        # declara voz.
        voz = sp.get("voz") if isinstance(sp, dict) else None
        if voz and voz not in MODELO_VOZ:
            faltando.add(voz)
    assert not faltando, f"vozes usadas em spec e sem medicao: {sorted(faltando)}"
