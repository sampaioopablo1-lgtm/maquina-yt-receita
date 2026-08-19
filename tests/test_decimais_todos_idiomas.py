"""Um numero decimal com percentual vale UM, em todos os sete idiomas.

Este e o teste que o aprendizado 316 pediu depois de dois defeitos gregos
seguidos com a mesma forma: tabela por idioma com uma linha faltando. Em vez
de esperar o terceiro aparecer num pacote, a varredura roda aqui.

Ela ja pagou na primeira execucao (19/08/2026), achando DOIS:

  * `pl` nao tinha "przecinek" em lugar nenhum — mesmo defeito do grego, e
    encontrado ANTES de custar um pacote polones.
  * `el` ainda contava 2 mesmo depois do conserto do "κομμα", porque o
    percentual grego "τοις εκατο" tem DUAS palavras e o contador separa por
    espaco: "τοις" nao era numero nem conector, fechava o grupo, e "εκατο"
    abria outro. Como quase toda frase de dados termina em percentual, cada
    uma custava um numero a mais — o teto de quatro caia com dois numeros de
    verdade. O portugues e o espanhol escapavam por acidente feliz: "por" ja
    estava na lista de conectores deles.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao  # noqa: E402

# Um unico numero decimal seguido do percentual, no idioma.
UM_DECIMAL_COM_PERCENTUAL = {
    "pt": "A taxa foi de tres virgula quatro por cento.",
    "en": "The rate was three point four percent.",
    "es": "La tasa fue de tres coma cuatro por ciento.",
    "id": "Tingkatnya tiga koma empat persen.",
    "el": "Ο ρυθμός ήταν τρία κόμμα τέσσερα τοις εκατό.",
    "tr": "Oran yuzde uc virgul dort oldu.",
    "pl": "Stawka wyniosla trzy przecinek cztery procent.",
}

# Dois numeros decimais com percentual: tem de contar DOIS, nao mais.
DOIS_DECIMAIS = {
    "pt": "Caiu de quatro virgula quatro por cento para tres virgula quatro por cento.",
    # NAO usar "to" entre os dois: "to" e conector em ingles, entao ele une as
    # duas corridas e o contador devolve 1. Isso e limitacao CONHECIDA do
    # desenho — o mesmo mecanismo que faz "forty two" valer 1 — e nao um
    # defeito introduzido aqui. Fica registrado em vez de escondido.
    "en": "Four point four percent last month, three point four percent now.",
    "es": "Bajo de cuatro coma cuatro por ciento a tres coma cuatro por ciento.",
    "id": "Turun dari empat koma empat persen ke tiga koma empat persen.",
    "el": "Έπεσε από τέσσερα κόμμα τέσσερα τοις εκατό σε τρία κόμμα τέσσερα τοις εκατό.",
    "tr": "Yuzde dort virgul dortten yuzde uc virgul dorde dustu.",
    "pl": "Spadla z cztery przecinek cztery procent do trzy przecinek cztery procent.",
}


@pytest.mark.parametrize("idi", sorted(UM_DECIMAL_COM_PERCENTUAL))
def test_um_decimal_com_percentual_vale_um(idi):
    assert narracao.conta_numeros(UM_DECIMAL_COM_PERCENTUAL[idi], idi) == 1


@pytest.mark.parametrize("idi", sorted(DOIS_DECIMAIS))
def test_dois_decimais_valem_dois(idi):
    """Nem inflar (o defeito) nem colapsar (o risco do conserto)."""
    assert narracao.conta_numeros(DOIS_DECIMAIS[idi], idi) == 2


@pytest.mark.parametrize("idi", sorted(UM_DECIMAL_COM_PERCENTUAL))
def test_todo_idioma_tem_um_caso_coberto(idi):
    """Idioma novo na tabela NUMEROS tem de aparecer aqui tambem."""
    assert idi in narracao.NUMEROS, f"{idi} sumiu de NUMEROS"


def test_nenhum_idioma_de_numeros_ficou_de_fora_da_varredura():
    faltam = set(narracao.NUMEROS) - set(UM_DECIMAL_COM_PERCENTUAL) - {"hi"}
    assert not faltam, (
        f"idioma(s) sem caso decimal nesta varredura: {sorted(faltam)} — "
        "adicione a frase antes que o defeito apareca num pacote")


def test_planilha_falada_continua_reprovando_em_todo_idioma():
    """O conserto nao pode cegar o portao."""
    cinco = {
        "pt": ("Carne subiu quatorze, leite tres, pao um, ovo dois e "
               "azeite caiu vinte."),
        "pl": ("Emerytalna dziewiec, rentowa szesc, wypadkowa jeden, "
               "Fundusz Pracy dwa, FGSP dziesiec."),
        "el": ("Μοσχάρι δεκατέσσερα, αρνί δώδεκα, ψάρια εννέα, "
               "μαργαρίνη οκτώ και ψωμί ένα."),
    }
    for idi, f in cinco.items():
        assert narracao.conta_numeros(f, idi) >= narracao.MAX_NUM_FRASE, idi
