"""A barreira anti-republicacao comparava o ESPACAMENTO em grego e em hindi.

`_normalizar` era `[^a-z0-9\\s]`, a faixa ASCII. Em portugues isso custava os
acentos e a funcao seguia servindo. Em grego e em devanagari apagava toda
letra, e sobravam so os espacos — que sao muito parecidos entre si.

Nao chegou a custar video: a publicacao migrou para `fabrica/publicar.py` antes
de esta barreira rodar nesses dois canais. Achado em 20/08/2026, ao ligar a
escrita automatica de roteiro, que se apoia na mesma regra de 0,65.
"""
from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from maquina.stages.compliance import similaridade  # noqa: E402

LIMITE = 0.65    # publicacao.similaridade_max, o que a rotina exige

# Titulos sem nada em comum, nas escritas da frota que nao sao latinas.
GREGO = ("Ποσο κοστιζει ενα σπιτι στην Αθηνα",
         "Η αγορα εργασιας αλλαζει τωρα")
HINDI = ("सैलरी बढ़ाने के तरीके", "नौकरी बदलने का सही समय")


def _normalizar_antigo(texto: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", texto.lower())


def test_o_defeito_existia_e_reprovava_titulos_sem_relacao():
    """Documenta o comportamento antigo, para o conserto nao voltar sozinho."""
    a, b = (_normalizar_antigo(t) for t in GREGO)
    assert a.strip() == "" and b.strip() == ""      # so sobrou espaco
    assert SequenceMatcher(None, a, b).ratio() >= LIMITE


def test_grego_diferente_passa_longe_do_limite():
    assert similaridade(*GREGO) < LIMITE


def test_hindi_diferente_passa_longe_do_limite():
    assert similaridade(*HINDI) < LIMITE


def test_texto_identico_continua_valendo_um():
    """O conserto nao pode desligar a barreira: republicar o MESMO roteiro
    continua sendo o caso que ela existe para pegar."""
    for t in (GREGO[0], HINDI[0], "Planilha de transicao para a ISO 9001"):
        assert similaridade(t, t) == 1.0


def test_pontuacao_continua_sendo_ignorada():
    """`\\w` tira pontuacao, que e o que a funcao sempre quis dizer."""
    assert similaridade("Quanto custa: a conta!", "quanto custa a conta") == 1.0


def test_latino_com_acento_agora_conta_a_letra():
    """Antes "salario" e "salário" eram o mesmo texto porque o acento sumia
    junto com a letra acentuada. Agora o acento fica — e duas palavras que so
    diferem nele continuam parecidissimas, como devem ser."""
    assert similaridade("salário mínimo", "salario minimo") > 0.8
