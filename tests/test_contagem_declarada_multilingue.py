"""O detector de contagem era SO PORTUGUES, e "1 conflito em 207" era vacuo.

Medido em 13/10/2026 as 12:1x, escolhendo pauta no `epomeno-epipedo-006`: o
capitulo 73 declara `Τέσσερα λάθη` (QUATRO erros) e os capitulos enumeram CINCO
-- o 79 diz literalmente "Υπάρχει και ένα πέμπτο". O detector passou em silencio,
porque o vocabulario dele era inteiro em portugues e as specs do epomeno sao
gregas, as do kolejny polonesas.

Eu havia reportado "1 conflito em 207 specs" como medicao da FROTA. Nao era: era
medicao de um terco dela, com "0 conflitos" VACUO nas outras duas. O mesmo erro
de enquadramento do 679/698 -- tratar como da frota o que e de uma parte.

E O CONSERTO DEU TRES FALSOS POSITIVOS ANTES DE FICAR DE PE, todos na mesma
rodada, e e por isso que cada um tem teste proprio aqui:

 1. **vocabulario so** levou a frota de 1 para 13 "conflitos", DOZE falsos: a
    fonte diz "cztery błędy" e tem tres kickers `<ordinal> błąd`, porque o
    PRIMEIRO item mora na NARRACAO do capitulo que declara. Conserto: contar a
    POSICAO MAIS ALTA alcancada, lendo kicker E narracao;
 2. **ainda sobravam subcontagens** (`quatro passos` contra 1): a fonte enumera
    com ordinal NU seguido de dois-pontos ("Primeiro:") ou com o numeral DEPOIS
    do substantivo ("Passo um"), formas que o detector nao le. Conserto: so
    reportar quando a enumeracao PASSA da declaracao -- achar um quinto prova
    que existem cinco, enquanto nao achar o primeiro prova apenas que eu nao sei
    ler aquela forma;
 3. **o ordinal NU produzia acusacao** no outro sentido: `τις δύο στήλες` (sao
    duas) pareou com `πρώτο/δεύτερο/τρίτο` de OUTRA lista doze capitulos adiante.
    Conserto: ordinal sem o substantivo nao conta, e perder achado e melhor que
    inventar achado.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import contagem_declarada as cd  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..", "fabrica", "specs")


def _spec(nome):
    return json.load(open(os.path.join(RAIZ, nome + ".json"), encoding="utf-8"))


def _div(nome):
    return cd.divergencias(_spec(nome))


# ---- os QUATRO conflitos reais, conferidos a mao ------------------------------
# Assinatura comum: a fonte declara N e depois acrescenta "existe tambem um N+1".
REAIS = {
    "epomeno-epipedo-005": (4, 5),    # Τέσσερα λάθη -> cap 75 "Πέμπτο λάθος"
    "epomeno-epipedo-006": (4, 5),    # Τέσσερα λάθη -> cap 79 "Πέμπτο λάθος"
    "epomeno-epipedo-014": (3, 4),    # Τρία λάθη    -> cap 54 "ένα τέταρτο λάθος"
    "labtreinamento-009": (5, 6),     # o caso original, que motivou o modulo
}


def test_os_quatro_conflitos_reais_sao_achados():
    for nome, (declarado, enumerado) in REAIS.items():
        d = _div(nome)
        assert d, f"{nome} deveria acusar conflito"
        x = d[0]
        assert (x["declarado"], x["enumerados"]) == (declarado, enumerado), (
            f"{nome}: esperava {declarado} contra {enumerado}, veio "
            f"{x['declarado']} contra {x['enumerados']}")


def test_o_caso_GREGO_e_o_que_o_detector_portugues_perdia():
    # Se isto falhar, o vocabulario grego saiu e a frota volta a ser medida
    # so em portugues -- que foi o defeito inteiro.
    assert _div("epomeno-epipedo-006")[0]["substantivo"] == "λάθος"


def test_o_caso_PORTUGUES_original_continua_de_pe():
    assert _div("labtreinamento-009")[0]["declaracao"] == "esses cinco casos"


# ---- os falsos positivos, um teste por conserto -------------------------------
def test_NAO_acusa_quando_o_primeiro_item_esta_na_narracao():
    # `cztery błędy` com tres kickers `<ordinal> błąd`: a fonte esta CERTA, o
    # primeiro erro esta na narracao do capitulo que declara.
    assert _div("kolejny-poziom-008") == []


def test_NAO_acusa_ordinal_nu_seguido_de_dois_pontos():
    # "quatro passos" com "Primeiro: ... Segundo: ..." na narracao, e os kickers
    # sao `Passo um` / `Passo dois` -- numeral DEPOIS do substantivo.
    assert _div("labtreinamento-004") == []
    assert _div("nivel-do-jogo-008") == []
    assert _div("kolejny-poziom-012") == []


def test_NAO_pareia_ordinal_nu_de_OUTRA_lista():
    # `τις δύο στήλες` sao de fato duas; `πρώτο/δεύτερο/τρίτο` doze capitulos
    # adiante sao outra lista.
    assert _div("epomeno-epipedo-003") == []
    assert _div("epomeno-epipedo-011") == []


def test_a_assimetria_e_declarada_e_nao_estetica():
    # Subcontar e defeito MEU; superenumerar e defeito da FONTE. O modulo so
    # reporta o segundo, e o codigo tem de dizer isso.
    fonte = open(os.path.join(os.path.dirname(__file__), "..", "fabrica",
                              "contagem_declarada.py"), encoding="utf-8").read()
    assert "n > declarado" in fonte


def test_a_frota_tem_QUATRO_achados_e_este_numero_e_medido():
    culpados = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("longo"):
            continue
        if cd.divergencias(d):
            culpados.append(os.path.basename(f)[:-5])
    assert sorted(culpados) == sorted(REAIS), culpados


def test_os_tres_idiomas_da_frota_estao_no_vocabulario():
    for palavra in ("quatro", "τέσσερα", "cztery"):
        assert palavra in cd.NUMERAL
    for palavra in ("quinto", "πέμπτο", "piąty"):
        assert palavra in cd.ORDINAL
