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
# A SERIE TEM UM DONO SO, E ELE NAO E ESTE ARQUIVO — conserto de 16/10 as 15:4x.
#
# ATE AGORA ela vivia em DUAS listas: a `SERIE` do
# `test_residuo_quebra_o_limite_de_dois_segundos` e uma copia `RESIDUOS` aqui.
# Eu alimentei a primeira em tres rodadas seguidas (s042, s044, s043) e **nao a
# segunda**, e o `assert mira.RESIDUO_N == len(RESIDUOS)` passou a reprovar com
# 50 contra 47 — a 26a falha da suite contra a linha de base de 25.
#
# E EU SO VI TRES RODADAS DEPOIS, porque entre elas rodei apenas os testes
# DIRECIONADOS a banda, e os direcionados nao incluiam este arquivo. Quebrou no
# commit `32321b7` (o `s042`, 12:3x) e a suite inteira anterior era das 12:0x.
#
# E a assinatura e a MESMA que matou o run `38847013520` descrito no `CLAUDE.md`:
# "mesma regra, dois donos, um atualizado". Ali era o teto do short no portao e
# no render; aqui e a serie do residuo em dois testes.
#
# Agora este arquivo DERIVA da `SERIE`, e nao ha o que esquecer de atualizar.
from test_residuo_quebra_o_limite_de_dois_segundos import SERIE as _SERIE

RESIDUOS = [(prev, real) for _pacote, prev, real, _prov in _SERIE]


def test_a_serie_tem_UM_dono_e_este_arquivo_nao_e_ele():
    """Contraprova do conserto: se a copia voltar, este teste reprova."""
    fonte = open(__file__, encoding="utf-8").read()
    corpo = fonte.split('"""', 2)[-1]
    assert "from test_residuo_quebra" in corpo, (
        "a RESIDUOS deste arquivo tem de DERIVAR da SERIE; lista propria aqui "
        "reconstroi o defeito de 16/10 as 15:4x (dois donos, um atualizado)"
    )
    assert len(RESIDUOS) == len(_SERIE)


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
    assert mira.faixa_real(25.6) == (25.7, 29.6)
    assert mira.faixa_real(10.0) == (10.1, 14.0)


def test_o_relato_do_s034_AVISA_que_o_real_passa_do_teto():
    t = mira.relato(str(RAIZ / "fabrica/specs/labtreinamento-s034.json"))
    assert "dentro da mira nos dois mundos" in t, "a previsao estava dentro"
    # 770: com o piso da banda em 0,1 a faixa do s034 passou a
    # ATRAVESSAR o teto de 26,0 em vez de ficar toda acima dele, e por isso o
    # relato caiu de "PASSA do teto" para "pode passar do teto". A piora do
    # AVISO e consequencia direta de a banda ter ficado mais larga, e vai
    # cobrada aqui em vez de passar em branco: o real daquela peca foi 28, logo
    # o aviso certo era o forte e hoje o instrumento so da o fraco.
    assert "pode passar do teto" in t, "e o real nao — isto e o 739"
    assert "PASSA do teto da mira" not in t, (
        "se o aviso FORTE voltou, o piso da banda subiu — releia o 770")
    assert "25.7 e 29.6" in t
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
    # 774: e o par de HOJE tambem nao se escreve a mao em lugar nenhum.
    assert "0,1 a 3,7" not in t and "0.1 a 3.7" not in t
