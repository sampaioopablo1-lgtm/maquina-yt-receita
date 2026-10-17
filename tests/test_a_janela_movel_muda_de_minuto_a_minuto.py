"""A contagem da janela MOVEL e funcao do MINUTO — medido em 17/10 as 01:1x.

As 01:09 a janela de 24 h deu 8 / 8 / 9 e a escolha de `labtreinamento` saiu
de um EMPATE em 8, desfeito pela peca mais antiga (22:13). As 01:13 a mesma
janela deu 7 / 8 / 9 e `labtreinamento` era minimo ABSOLUTO. A escolha nao
mudou; a RAZAO mudou, e eu havia relatado o desempate.

A frota publica de hora em hora, logo a janela de 24 h perde ~1 peca por canal
por hora. Ler a contagem numa chamada e decidir noutra e o 760 na contagem.
O conserto e `escolha_do_momento`, que fixa `agora` uma vez.
"""
import sys, os
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import concentracao_frota as cf

AS_01_09 = {"labtreinamento": 8, "epomeno-epipedo": 8, "kolejny-poziom": 9}
AS_01_13 = {"labtreinamento": 7, "epomeno-epipedo": 8, "kolejny-poziom": 9}
ULTIMA = {
    "kolejny-poziom": "2026-10-17T00:13:08Z",
    "epomeno-epipedo": "2026-10-16T23:13:14Z",
    "labtreinamento": "2026-10-16T22:13:18Z",
}


def test_as_duas_leituras_escolhem_o_MESMO_canal():
    a, _ = cf.mais_baixo(AS_01_09, ULTIMA)
    b, _ = cf.mais_baixo(AS_01_13, ULTIMA)
    assert a == b == "labtreinamento"


def test_e_a_RAZAO_da_escolha_e_que_muda__empate_contra_minimo():
    _, emp_a = cf.mais_baixo(AS_01_09, ULTIMA)
    _, emp_b = cf.mais_baixo(AS_01_13, ULTIMA)
    assert len(emp_a) == 2, "as 01:09 havia EMPATE, e foi isso que eu relatei"
    assert len(emp_b) == 1, "as 01:13 nao havia empate nenhum"


def test_quatro_minutos_bastaram_para_uma_peca_sair_da_janela():
    delta = sum(AS_01_09.values()) - sum(AS_01_13.values())
    assert delta == 1, "uma peca, e ela saiu pelo CORTE, nao por publicacao"


def test_escolha_do_momento_devolve_contagem_e_escolha_JUNTAS():
    r = cf.escolha_do_momento(agora=datetime(2026, 10, 17, 1, 13,
                                             tzinfo=timezone.utc))
    for k in ("agora", "corte", "contagem", "ultima", "escolhido",
              "empatados", "houve_empate"):
        assert k in r, f"falta {k}: quem relata nao pode voltar a ler em outra chamada"
    assert r["escolhido"] in cf.FROTA or r["escolhido"] is None


def test_o_corte_sai_do_agora_FIXADO__nao_de_um_now_novo():
    ag = datetime(2026, 10, 17, 1, 13, tzinfo=timezone.utc)
    r = cf.escolha_do_momento(agora=ag, janela_h=24.0)
    assert r["agora"] == ag.isoformat()
    assert r["corte"] == (ag - timedelta(hours=24)).isoformat()


def test_duas_chamadas_com_o_MESMO_agora_devolvem_a_MESMA_coisa():
    ag = datetime(2026, 10, 17, 1, 13, tzinfo=timezone.utc)
    a = cf.escolha_do_momento(agora=ag)
    b = cf.escolha_do_momento(agora=ag)
    assert a == b, "sem isso o relato nao e reproduzivel nem dentro da rodada"


def test_a_janela_maior_nao_perde_peca_tao_rapido():
    """Contraprova do mecanismo: o que muda a contagem e o CORTE."""
    ag = datetime(2026, 10, 17, 1, 13, tzinfo=timezone.utc)
    curta = cf.escolha_do_momento(agora=ag, janela_h=24.0)
    longa = cf.escolha_do_momento(agora=ag, janela_h=48.0)
    assert sum(longa["contagem"].values()) >= sum(curta["contagem"].values())


def test_o_defeito_vai_NOMEADO_no_docstring_do_modulo():
    d = cf.escolha_do_momento.__doc__
    assert "760" in d, "a assinatura e a do 760, e isso tem de ficar escrito"
    assert "8 / 8 / 9" in d and "7 / 8 / 9" in d, "as duas leituras reais"
