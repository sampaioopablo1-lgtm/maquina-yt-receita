"""O quadro da Porta 1 tem de ser calculado, nunca estimado de cabeca.

Pedido do dono em 12/10/2026: o quadro de resultados, projecao, tendencia e
"quando o canal ira monetizar" tem de sair em CADA rodada. Eu vinha respondendo
de cabeca, e todo numero que eu calculo de cabeca vira um erro meu — 652/655,
658, 682, 685, os "~1,9 s por cena", os "3,7 GB de Storage".

O teste mais importante deste arquivo e o ultimo: ele exige que a projecao seja
confrontada com a BARRA QUE SOBE em 1/FEV/2027. Projetar 500 inscritos para uma
data em que a barra ja vale 1.000 e prometer monetizacao que nao existe.
"""

import datetime as dt
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import porta1 as P  # noqa: E402

# A leitura REAL de 12/10/2026 14:35, contra a de 10/10 22:15 (40,3 h).
REAL = {"labtreinamento": {"antes": 67, "agora": 68},
        "epomeno-epipedo": {"antes": 17, "agora": 19},
        "kolejny-poziom": {"antes": 8, "agora": 8}}
HORAS = 40.3


def test_janela_curta_LEVANTA_em_vez_de_devolver_ruido():
    """O contador de canal anda em degrau (686/703)."""
    with pytest.raises(P.LeituraCurta) as e:
        P.ritmo(17, 19, 1.0)
    assert "DEGRAU" in str(e.value)


def test_quatro_horas_passa_e_tres_nao():
    P.ritmo(17, 19, 4.0)
    with pytest.raises(P.LeituraCurta):
        P.ritmo(17, 19, 3.9)


def test_ritmo_zero_devolve_NUNCA_e_nao_divisao_por_zero():
    assert P.dias_para(500, 8, 0.0) is None
    assert P.dias_para(500, 8, -1.0) is None


def test_canal_que_ja_passou_devolve_zero_dias():
    assert P.dias_para(500, 500, 0.1) == 0.0
    assert P.dias_para(500, 700, 0.0) == 0.0


def test_o_quadro_real_de_12_10_nao_chega_a_tempo_em_canal_nenhum():
    """A medicao que gerou o pedido. Se isto passar a FALHAR, algo bom mudou."""
    q = P.quadro(REAL, HORAS, hoje=dt.date(2026, 10, 12))
    assert q["dias_ate_fim_do_mes"] == 19
    por_canal = {l["canal"]: l for l in q["canais"]}
    assert por_canal["kolejny-poziom"]["dias_para_porta1"] is None, (
        "kolejny leu +0 em 40 h; ritmo zero nao chega"
    )
    for nome in ("labtreinamento", "epomeno-epipedo"):
        assert por_canal[nome]["pct_no_fim_do_mes"] < 20.0, (
            f"{nome} fecharia o mes abaixo de 20% da Porta 1 — se passou de "
            "20%, releia o quadro antes de prometer prazo ao dono"
        )


def test_o_melhor_canal_e_o_de_MAIS_INSCRITOS_e_nao_o_de_maior_ritmo():
    """O portao conta o ABSOLUTO. Ordenar por ritmo escolheria o canal errado."""
    q = P.quadro(REAL, HORAS, hoje=dt.date(2026, 10, 12))
    assert q["melhor_canal"] == "labtreinamento"
    # e o de maior ritmo e OUTRO, o que prova que a ordenacao importa
    maior_ritmo = max(q["canais"], key=lambda l: l["por_dia"])["canal"]
    assert maior_ritmo == "epomeno-epipedo"


def test_views_por_dia_para_fechar_sai_em_TRES_taxas_de_conversao():
    """Uma taxa so esconde que a conversao e a alavanca, nao o volume."""
    q = P.quadro(REAL, HORAS, hoje=dt.date(2026, 10, 12))
    l = [x for x in q["canais"] if x["canal"] == "labtreinamento"][0]
    a = l["views_por_dia_para_fechar_no_mes_a_1_2_por_mil"]
    b = l["views_por_dia_para_fechar_no_mes_a_5_por_mil"]
    c = l["views_por_dia_para_fechar_no_mes_a_20_por_mil"]
    assert a > b > c, "mais conversao tem de pedir MENOS view"
    assert a > 10000, (
        "na conversao medida o numero tem de ser absurdo mesmo — e o que prova "
        "que volume nao fecha a Porta 1"
    )


def test_A_BARRA_QUE_SOBE_entra_na_projecao():
    """O teste que mais importa aqui.

    A Porta 1 pede 500 inscritos ATE 31/01/2027. De 1/FEV/2027 em diante a barra
    e 1.000. Projetar 500 para depois dessa data e prometer uma monetizacao que
    nao existe mais — e no quadro real de 12/10 as duas datas (2027-11-20 e
    2028-10-06) caem DEPOIS dela.
    """
    q = P.quadro(REAL, HORAS, hoje=dt.date(2026, 10, 12))
    for l in q["canais"]:
        if l["data_porta1"] is None:
            continue
        assert l["chega_antes_da_barra_subir"] is False, (
            f"{l['canal']} passou a chegar antes de {P.BARRA_SOBE_EM} — refaca "
            "o relato ao dono, porque isso muda a resposta dele"
        )
        assert l["alvo_que_vale_na_chegada"] == P.INSCRITOS_APOS_A_BARRA_SUBIR


def test_alvo_na_data_muda_exatamente_na_virada():
    assert P.alvo_na_data(dt.date(2027, 1, 31)) == 500
    assert P.alvo_na_data(dt.date(2027, 2, 1)) == 1000


def test_o_relato_diz_as_tres_ressalvas_em_vez_de_so_o_numero():
    r = P.relato(P.quadro(REAL, HORAS, hoje=dt.date(2026, 10, 12)))
    assert "LINEAR" in r, "ritmo linear tem de ir declarado"
    assert "barra" in r.lower() and "1.000" in r, "a barra que sobe tem de ir"
    assert "668" in r, (
        "canal com acervo anterior a maquina tem de carregar a ressalva do 668 "
        "no proprio relato"
    )


# ---------------------------------------------------------------------------
# O PISO DE RESOLUCAO — medido em 12/10/2026 as 18:1x, e e um defeito meu que
# quase foi ao relato do dono. As >= 4 h da regra H (686) bastam para pular o
# DEGRAU da replica; eu tratei isso como se bastassem para medir RITMO.
# ---------------------------------------------------------------------------

def test_o_piso_de_resolucao_de_quatro_horas_e_SEIS_por_dia():
    # O contador anda de um em um: numa janela de 4 h o menor ritmo diferente
    # de zero que ele consegue expressar e 24/4 = 6 por dia.
    assert P.piso_de_resolucao(4.0) == 6.0


def test_o_piso_de_quatro_horas_esta_ACIMA_do_ritmo_medido_da_frota():
    # O ritmo medido da frota inteira em 12/10 foi +1,79/dia. Se o piso de uma
    # janela de 4 h e 6,00/dia, essa janela NAO distingue 1,79 de zero — e o
    # relato que dissesse "nunca" a partir dela estaria inventando precisao.
    assert P.piso_de_resolucao(4.0) > 1.79


def test_a_janela_de_quarenta_horas_resolve_o_ritmo_que_ela_mediu():
    # E por isso que a leitura de 40,3 h funcionou e nao foi sorte: o piso dela
    # e 0,60/dia, que e exatamente o ritmo que ela mediu no labtreinamento.
    assert P.piso_de_resolucao(40.3) < 0.61


def test_horas_para_resolver_e_a_INVERSA_do_piso():
    for por_dia in (0.6, 1.79, 6.0):
        h = P.horas_para_resolver(por_dia)
        assert abs(P.piso_de_resolucao(h) - por_dia) < 1e-9


def test_horas_para_resolver_devolve_None_quando_o_ritmo_e_zero():
    # Ritmo zero nunca se resolve: nao existe janela que mostre a mudanca que
    # nao acontece. None, nao infinito e nao um numero grande qualquer.
    assert P.horas_para_resolver(0.0) is None
    assert P.horas_para_resolver(-1.0) is None


def test_DELTA_ZERO_sai_como_NAO_RESOLVIDO_e_nao_como_nunca():
    # A leitura REAL de 12/10 as 18:17: os tres contadores byte a byte iguais
    # aos de 14:35. Se isto virar "nunca" no relato, a maquina mentiu com
    # numero — e foi o que eu quase reportei.
    q = P.quadro({"labtreinamento": {"antes": 68, "agora": 68}}, 4.0)
    linha = q["canais"][0]
    assert linha["ritmo_resolvido"] is False
    assert linha["por_dia"] == 0.0
    texto = P.relato(q)
    assert "indet" in texto
    assert "RITMO NAO RESOLVIDO" in texto
    # A palavra "nunca" nao pode sair para um canal cujo ritmo nao foi resolvido.
    linha_da_tabela = [x for x in texto.splitlines() if "labtreinamento" in x][0]
    assert "nunca" not in linha_da_tabela


def test_DELTA_POSITIVO_continua_resolvido_e_continua_projetando():
    # A guarda nova nao pode calar o caso em que o ritmo FOI medido.
    q = P.quadro({"epomeno-epipedo": {"antes": 17, "agora": 19}}, 40.3)
    linha = q["canais"][0]
    assert linha["ritmo_resolvido"] is True
    assert linha["por_dia"] > 1.0
    assert linha["data_porta1"] is not None


def test_o_quadro_declara_o_proprio_piso():
    # O numero tem de SAIR no quadro, senao quem le o json nao sabe o que o
    # delta zero significa.
    q = P.quadro({"kolejny-poziom": {"antes": 8, "agora": 8}}, 40.3)
    assert abs(q["piso_de_resolucao_por_dia"] - 0.6) < 0.01
