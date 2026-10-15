#!/usr/bin/env python3
"""O DIA CALENDARIO zera a meia-noite e nao ordena nada nas primeiras horas.

POR QUE ISTO EXISTE, e e um defeito do PROCEDIMENTO, nao de uma peca. O
`concentracao_frota.relato(por_dia=...)` escolheu o canal em SEIS rodadas
seguidas (762/765/767/768/769/770 e a de 23:0x). Às 00:0x de 15/10/2026 ele
devolveu **0 / 0 / 0** — porque o dia calendario acabara de comecar — e, com
isso, **nao ordenou nada exatamente na rodada que precisava escolher**.

**E a cegueira e SIMETRICA da que ele nasceu para consertar.** O achado de
14/10 as 16:1x (762) foi que o ACERVO dilui a rodada: 50/25/22 esta dentro do
dobro e nao alerta, enquanto o DIA estava em 16/0/0 e alerta. Agora o outro
lado: **o dia calendario recem-comecado APAGA as ultimas horas.** As duas
contagens tem janela errada, em sentidos opostos.

**A saida e a JANELA MOVEL, e ela estava medida no mesmo instante:** com
`publicado_em >= now() - interval '24 hours'` os numeros eram
**16 / 4 / 4**, que ALERTA e ainda empata os dois canais baixos — ou seja, a
janela movel preserva a informacao que o dia calendario jogou fora as 00:00.

**O que este conserto NAO e:** limiar novo. A `janela=` usa a MESMA `analise`
e o MESMO limiar do irmao (mais que o dobro do segundo), pela razao escrita no
762 — limiar novo aqui seria critério sem procedencia.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fabrica"))

import concentracao_frota as cf  # noqa: E402

# Medido no banco as 00:0x de 15/10/2026, nas duas janelas, na mesma rodada.
DIA_CALENDARIO = {"labtreinamento": 0, "epomeno-epipedo": 0, "kolejny-poziom": 0}
JANELA_24H = {"labtreinamento": 16, "epomeno-epipedo": 4, "kolejny-poziom": 4}


def test_o_dia_em_zero_DIZ_que_nao_ordena_em_vez_de_calar():
    t = cf.relato(por_dia=DIA_CALENDARIO)
    assert "DIA CALENDARIO ESTA EM ZERO" in t
    assert "nao ordena nada" in t
    assert "janela=" in t, "tem de dizer PARA ONDE ir, nao so que nao sabe"


def test_o_dia_em_zero_NAO_finge_alerta_nem_dominante():
    """Zero em todos nao e concentracao — e ausencia de dado."""
    t = cf.relato(por_dia=DIA_CALENDARIO)
    assert "ALERTA DO DIA" not in t


def test_a_janela_movel_PRESERVA_o_que_o_dia_calendario_jogou_fora():
    t = cf.relato(por_dia=DIA_CALENDARIO, janela=JANELA_24H)
    assert "NAS ULTIMAS 24 H" in t
    assert "ALERTA DA JANELA" in t, (
        "a janela de 24 h media 16 contra 4 — mais que o dobro, logo alerta")
    assert "labtreinamento 16" in t and "epomeno-epipedo 4" in t


def test_a_janela_usa_o_MESMO_limiar_do_irmao():
    """Nao ha limiar novo aqui: e a mesma `analise`, mais que o dobro."""
    no_limite = {"labtreinamento": 8, "epomeno-epipedo": 4, "kolejny-poziom": 4}
    t = cf.relato(janela=no_limite)
    assert "ALERTA DA JANELA" not in t, "8 nao e MAIOR que 8 — fronteira exata"
    passou = {"labtreinamento": 9, "epomeno-epipedo": 4, "kolejny-poziom": 4}
    assert "ALERTA DA JANELA" in cf.relato(janela=passou)


def test_a_janela_NOMEIA_canal_zerado_nela():
    t = cf.relato(janela={"labtreinamento": 3, "epomeno-epipedo": 1,
                          "kolejny-poziom": 0})
    assert "SEM NENHUMA PECA NAS ULTIMAS 24 H" in t
    assert "kolejny-poziom" in t


def test_sem_janela_e_sem_dia_o_relato_ainda_AVISA_que_le_acervo():
    """A nota do 762 nao pode ter sido apagada por este conserto."""
    t = cf.relato()
    assert "ACERVO NAO E O DIA" in t


def test_alerta_do_dia_com_MENOS_pecas_que_canais_e_ARTEFATO_e_vai_dito():
    """15/10 01:0x, e e a mesma familia do 771.

    Com UMA peca no dia o relato gritou *"ALERTA DO DIA: epomeno 1 contra 0"*.
    Isso nao e concentracao: com menos pecas que canais a distribuicao uniforme
    e IMPOSSIVEL, e a peca tem de cair em algum canal. O limiar nao mudou — o
    que mudou e que o relato DIZ que o alerta seria artefato do total, em vez de
    emiti-lo. E aritmetica, nao criterio novo.
    """
    t = cf.relato(por_dia={"labtreinamento": 0, "epomeno-epipedo": 1,
                           "kolejny-poziom": 0})
    assert "ALERTA DO DIA" not in t
    assert "artefato do total" in t
    assert "distribuicao uniforme e IMPOSSIVEL" in t
    # e ele ainda NOMEIA os canais em zero, que e informacao de verdade
    assert "SEM NENHUMA PECA HOJE" in t
    assert "labtreinamento" in t and "kolejny-poziom" in t


def test_com_pecas_SUFICIENTES_o_alerta_do_dia_volta_a_sair():
    """A supressao e so para total < numero de canais. O caso do 762 (16/0/0)
    tem de seguir alertando, senao o conserto apagaria o achado que criou o
    contador."""
    t = cf.relato(por_dia={"labtreinamento": 16, "epomeno-epipedo": 0,
                           "kolejny-poziom": 0})
    assert "ALERTA DO DIA" in t
    assert "artefato do total" not in t
    # e a fronteira: tres pecas para tres canais ja permite uniforme
    t3 = cf.relato(por_dia={"labtreinamento": 3, "epomeno-epipedo": 0,
                            "kolejny-poziom": 0})
    assert "ALERTA DO DIA" in t3


def test_o_rotulo_da_janela_segue_o_argumento_e_nao_e_cravado():
    t = cf.relato(janela={"labtreinamento": 2, "epomeno-epipedo": 1,
                          "kolejny-poziom": 1}, janela_h=6)
    assert "NAS ULTIMAS 6 H" in t
    assert "NAS ULTIMAS 24 H" not in t
