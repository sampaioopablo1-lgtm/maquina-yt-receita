"""Em grego a virgula decimal falada e "κόμμα", e ela conta como UM numero.

O contador de quantidades trata como UM grupo uma corrida de palavras de
numero atravessada por conectores — e o separador decimal E um conector
nesta tabela: "koma" ja estava la para indonesio e "point" para ingles. O
grego era o unico idioma decimal da frota sem o seu.

O custo era invisivel e sistematico: cada decimal grego valia 2, entao uma
frase com DUAS casas decimais batia no teto de quatro e virava erro. Um
roteiro que cita "3,4%" e "4,4%" na mesma frase e leitura normal de dados,
nao planilha falada. Medido em 19/08/2026: duas frases reprovadas assim no
epomeno-epipedo-006 (aprendizado 315).

Detalhe que custou uma tentativa: `conta_numeros` compara sobre
`normaliza()`, que tira acento. "κόμμα" com tonos na tabela nunca casava.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao  # noqa: E402


def test_um_decimal_grego_e_um_numero():
    assert narracao.conta_numeros("Ο πληθωρισμός στο τρία κόμμα τέσσερα.", "el") == 1


def test_dois_decimais_gregos_sao_dois_numeros():
    """O caso que reprovava: leitura normal de dados, nao planilha falada."""
    f = "Από τέσσερα κόμμα τέσσερα σε τρία κόμμα τέσσερα, οι τιμές δεν πέφτουν."
    assert narracao.conta_numeros(f, "el") == 2


def test_lista_de_tres_decimais_ainda_conta_tres():
    """A correcao nao pode cegar o portao: separados por palavra, contam."""
    f = ("Μοσχάρι δεκατέσσερα κόμμα τρία, αρνί δώδεκα κόμμα τέσσερα, "
         "ψωμί ένα κόμμα δύο.")
    assert narracao.conta_numeros(f, "el") == 3


def test_planilha_falada_grega_ainda_reprova():
    """Cinco quantidades continuam sendo planilha falada."""
    f = ("Μοσχάρι δεκατέσσερα κόμμα τρία, αρνί δώδεκα κόμμα τέσσερα, ψάρια "
         "εννέα κόμμα έξι, μαργαρίνη οκτώ κόμμα έξι, ψωμί ένα κόμμα δύο.")
    assert narracao.conta_numeros(f, "el") >= narracao.MAX_NUM_FRASE


def test_a_tabela_grega_esta_sem_tonos():
    """`conta_numeros` compara depois de normaliza(); com tonos nao casa."""
    assert "κομμα" in narracao.CONECTOR["el"]
    assert "κόμμα" not in narracao.CONECTOR["el"]


def test_os_outros_idiomas_nao_mudaram():
    assert narracao.conta_numeros("A inflacao foi de tres virgula quatro por cento.", "pt") == 1
    assert narracao.conta_numeros("Inflation was three point four percent.", "en") == 1
    assert narracao.conta_numeros("Inflasi tiga koma empat persen.", "id") == 1


def test_o_006_passa_limpo():
    import json

    sp = json.load(open(RAIZ / "fabrica/specs/epomeno-epipedo-006.json",
                        encoding="utf-8"))
    erros, avisos, _ = narracao.analisa(sp, "el")
    assert erros == [], erros
    assert avisos == [], avisos
