"""A mira confere a PREVISAO, e a mira do canal e sobre o REAL — 739.

As duas pecas do `labtreinamento` narradas pelo edge passaram pelo `mira.py` com
a previsao DENTRO de 20,0 a 26,0 e sairam em **27 e 28 s reais**, fora. O buraco
nao era a faixa: era o modulo conferir uma grandeza e a mira cobrar outra.

Agora o relato acrescenta a banda OBSERVADA do residuo (0,9 a 2,4 s acima da
previsao do provedor que de fato narrou, cinco pontos) e diz quando ela passa do
teto. **Ele informa e NAO reprova**, porque com n=5 e uma banda que varia por um
fator 2,7 sem lei estavel, reprovar seria inventar portao.
"""
import json
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import mira  # noqa: E402

# (previsao do provedor que narrou, real) — os cinco pontos do 739
RESIDUOS = [(43.1, 44), (42.9, 44), (42.1, 44), (25.7, 27), (25.6, 28),
            # 741: primeiro ponto OUT-OF-SAMPLE da banda, e ele caiu dentro.
            (24.8, 27)]


def test_a_banda_cobre_os_residuos_medidos():
    lo, hi = mira.RESIDUO_OBSERVADO
    for prev, real in RESIDUOS:
        r = real - prev
        assert lo - 0.05 <= r <= hi + 0.05, (prev, real, r)
    assert mira.RESIDUO_N == len(RESIDUOS)


def test_a_banda_nao_e_inventada__ela_e_o_minimo_e_o_maximo_observados():
    rs = [round(real - prev, 1) for prev, real in RESIDUOS]
    assert mira.RESIDUO_OBSERVADO == (min(rs), max(rs))


def test_faixa_real_e_soma_e_nao_fator():
    assert mira.faixa_real(25.6) == (26.5, 28.0)
    assert mira.faixa_real(10.0) == (10.9, 12.4)


def test_o_relato_do_s034_AVISA_que_o_real_passa_do_teto():
    t = mira.relato(str(RAIZ / "fabrica/specs/labtreinamento-s034.json"))
    assert "dentro da mira nos dois mundos" in t, "a previsao estava dentro"
    assert "PASSA do teto da mira" in t, "e o real nao — isto e o 739"
    assert "26.5 e 28.0" in t
    # o real medido desta peca foi 28, dentro da banda que o relato anuncia
    assert mira.faixa_real(25.6)[0] <= 28 <= mira.faixa_real(25.6)[1]


def test_ele_INFORMA_e_NAO_reprova__o_codigo_de_saida_continua_zero():
    r = subprocess.run(
        [sys.executable, str(RAIZ / "fabrica/mira.py"),
         str(RAIZ / "fabrica/specs/labtreinamento-s034.json")],
        capture_output=True, text=True)
    assert r.returncode == 0, "banda com n=5 nao vira portao"
    assert "FORA" not in r.stdout


def test_a_spec_que_a_PREVISAO_reprova_continua_reprovando():
    spec = json.loads(
        (RAIZ / "fabrica/specs/labtreinamento-s034.json").read_text())
    # estica a narracao ate a previsao sair da mira
    for c in spec["short"]:
        c["nar"] = c["nar"] + " " + c["nar"]
    r = mira.confere(spec)
    assert r["fora"], "previsao fora continua sendo FORA"


def test_canal_sem_mira_nao_recebe_banda_nenhuma():
    spec = json.loads(
        (RAIZ / "fabrica/specs/labtreinamento-s034.json").read_text())
    spec["slug"] = "kolejny-poziom"   # sem ALVO_POR_CANAL
    r = mira.confere(spec)
    assert r["tem_mira"] is False
