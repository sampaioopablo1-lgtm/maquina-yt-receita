"""A mira confere a PREVISAO, e a mira do canal e sobre o REAL — 739.

As duas pecas do `labtreinamento` narradas pelo edge passaram pelo `mira.py` com
a previsao DENTRO de 20,0 a 26,0 e sairam em **27 e 28 s reais**, fora. O buraco
nao era a faixa: era o modulo conferir uma grandeza e a mira cobrar outra.

Agora o relato acrescenta a banda OBSERVADA do residuo (0,9 a 3,7 s acima da
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
            (24.8, 27),
            # 742: segundo ponto out-of-sample, tambem dentro.
            (25.3, 27),
            # 744: terceiro ponto out-of-sample.
            (25.8, 28),
            # 746: nono ponto.
            (24.4, 26),
            # 747: decimo ponto, residuo +2,3.
            (24.7, 27),
    (24.6, 27),   # s041, 14/10: +2,4, EMPATA o teto da banda
    (23.3, 27),   # s043, 14/10: +3,7 — QUEBROU o teto (752)
    (24.9, 27),   # s044, 14/10: +2,1, dentro da banda ampliada
    (24.5, 27),   # s045, 14/10: +2,5
    (24.6, 26),   # s046, 14/10: +1,4
    (23.4, 25),   # s042, 14/10: +1,6, e o real DENTRO da mira
    (25.4, 27),   # s047, 14/10: +1,6, mira VERDE e o real FORA (756)
    (25.0, 27),   # s048, 14/10: +2,0, mira VERDE e o real FORA (758)
    (25.1, 27),   # s049, 14/10: +1,9, mira VERDE e o real FORA (759)
    (24.9, 27),   # s050, 14/10: +2,1, mira VERDE e o real FORA (760)
    (41.5, 42),   # kolejny-poziom-s027, 14/10: +0,5 — o PISO da banda caiu (769).
    (41.9, 42),   # epomeno-epipedo-s029, 14/10: +0,1 — o piso caiu OUTRA vez, e
                  # este ponto tem o SINAL nao estabelecido: real 42 significa
                  # (41; 42] e a previsao cai dentro (770).
    (41.6, 43),   # kolejny-poziom-s028, 14/10 23:1x: +1,4, dentro da banda
    (41.5, 43),   # epomeno-epipedo-s028, 14/10: +1,5 — quinto ponto da janela
                  # de 0,4 s em que a previsao NAO ordena o real (768).
    (41.6, 43),   # kolejny-poziom-s026, 14/10: +1,4 — previsao MAIOR que a do
                  # s025 (41,2) e real MENOR (43 contra 44). Ver 767.
    (41.3, 43),   # epomeno-epipedo-s027, 14/10: +1,7 — mesmo par que o s026
                  # (41,4 -> 43): a previsao REPRODUZ nesta faixa (766).
    (41.2, 44),   # kolejny-poziom-s025, 14/10: +2,8 — o maior residuo da serie
                  # FORA do labtreinamento (764).
    (41.4, 43),   # epomeno-epipedo-s026, 14/10: +1,6 — OUTRO canal e OUTRA voz,
                  # e a serie sempre foi multicanal (763)
            # 748: decimo primeiro ponto, previsao repetida.
            (24.7, 27)]


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
    # 770: o piso da banda caiu a 0,1, logo a soma desce com ele.
    assert mira.faixa_real(25.6) == (25.7, 29.3)
    assert mira.faixa_real(10.0) == (10.1, 13.7)


def test_o_relato_do_s034_AVISA_que_o_real_passa_do_teto():
    t = mira.relato(str(RAIZ / "fabrica/specs/labtreinamento-s034.json"))
    assert "dentro da mira nos dois mundos" in t, "a previsao estava dentro"
    # 770: com o piso da banda em 0,1 a faixa do s034 (25,7 a 29,3) passou a
    # ATRAVESSAR o teto de 26,0 em vez de ficar toda acima dele, e por isso o
    # relato caiu de "PASSA do teto" para "pode passar do teto". A piora do
    # AVISO e consequencia direta de a banda ter ficado mais larga, e vai
    # cobrada aqui em vez de passar em branco: o real daquela peca foi 28, logo
    # o aviso certo era o forte e hoje o instrumento so da o fraco.
    assert "pode passar do teto" in t, "e o real nao — isto e o 739"
    assert "PASSA do teto da mira" not in t, (
        "se o aviso FORTE voltou, o piso da banda subiu — releia o 770")
    assert "25.7 e 29.3" in t
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


def test_a_MENSAGEM_do_relato_le_a_banda_da_constante():
    """752/14-10: a mensagem tinha 0,9 a 2,4 CRAVADO no texto.

    Quando o teto da banda subiu para 3,7, a faixa calculada passou a dizer uma
    coisa e a frase ao lado dela outra — no mesmo relato, na mesma linha. Defeito
    meu, de nao ler a propria saida depois de mexer no numero. Este teste exige
    que os dois numeros da frase venham de `RESIDUO_OBSERVADO`.
    """
    t = mira.relato(str(RAIZ / "fabrica/specs/labtreinamento-s034.json"))
    lo, hi = mira.RESIDUO_OBSERVADO
    esperado = f"por {lo:.1f} a {hi:.1f} s".replace(".", ",")
    assert esperado in t.replace(".", ","), (esperado, t)
    # e o numero antigo nao pode reaparecer em lugar nenhum do relato
    assert "0,9 a 2,4" not in t and "0.9 a 2.4" not in t
    # 769: o PISO tambem caiu (0,9 -> 0,5). O par antigo nao pode reaparecer.
    assert "0,9 a 3,7" not in t and "0.9 a 3.7" not in t
    # 770: idem para o par de 769.
    assert "0,5 a 3,7" not in t and "0.5 a 3.7" not in t
