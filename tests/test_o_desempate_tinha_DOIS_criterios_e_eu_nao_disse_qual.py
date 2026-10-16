"""Eu desempatei o canal a mao com um criterio que o modulo RECUSA.

Medido em 16/10 as 14:2x. O dia veio **5 / 5 / 5** e o `concentracao_frota`,
sem `ultima=`, devolve `None` de proposito — ele nao escolhe. Eu entao escolhi
pela tabela do 713 (melhor inscrito/peca), que vive neste modulo em
`POR_PECA_713` e **que ele deliberadamente nao usa para desempate**: o criterio
dele e a peca mais ANTIGA, que e medida e nao depende de uma amostra de 161
pecas para 19 inscritos.

OS DOIS CONCORDARAM nesta rodada, e isso nao e evidencia de nada — e
coincidencia de uma rodada. O defeito e eu nao ter DITO qual criterio estava
usando: escolher entre dois sem declarar qual e o efeito (C) da rotina.

E a causa de fundo era falta de FONTE: com o `execute_sql` negado pela setima
rodada, o `ultima=` nao tinha de onde sair. Agora sai do pendente.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import concentracao_frota as cf  # noqa: E402

# A leitura real das 14:2x, do `docs/pendente/videos-a-inserir.sql`.
ULTIMA_REAL = {
    "kolejny-poziom": "2026-10-16T12:24:36Z",
    "epomeno-epipedo": "2026-10-16T10:13:48Z",
    "labtreinamento": "2026-10-16T13:16:24Z",
}
DIA_EMPATADO = {"epomeno-epipedo": 5, "kolejny-poziom": 5, "labtreinamento": 5}


def test_sem_fonte_o_modulo_RECUSA_e_e_por_isso_que_eu_desempatei_a_mao():
    escolha, empatados = cf.mais_baixo(DIA_EMPATADO)
    assert escolha is None, "a recusa e o comportamento certo, nao um bug"
    assert len(empatados) == 3


def test_o_criterio_DO_MODULO_e_a_peca_mais_ANTIGA_nao_a_tabela_do_713():
    escolha, _ = cf.mais_baixo(DIA_EMPATADO, ultima=ULTIMA_REAL)
    assert escolha == "epomeno-epipedo"
    # e a razao e a data, nao o inscrito/peca:
    assert ULTIMA_REAL[escolha] == min(ULTIMA_REAL.values())


def test_os_dois_criterios_CONCORDARAM_e_isso_nao_prova_nada():
    """Se um dia discordarem, este teste reprova e obriga a declarar qual vale."""
    por_data, _ = cf.mais_baixo(DIA_EMPATADO, ultima=ULTIMA_REAL)
    melhor_par = cf.ranking_713()[0][0][0]
    assert por_data == melhor_par, (
        "os dois criterios DIVERGIRAM. Isto nao e falha de codigo: e o caso em "
        "que a escolha precisa declarar QUAL criterio usou, porque ja nao da "
        "para esconder a decisao atras de um acordo acidental"
    )


def test_a_tabela_do_713_NAO_e_usada_pelo_desempate():
    """Contraprova: mudar a tabela nao muda a escolha por data."""
    guardado = dict(cf.POR_PECA_713)
    try:
        cf.POR_PECA_713.clear()
        cf.POR_PECA_713[("labtreinamento", "shorts")] = 9.99
        escolha, _ = cf.mais_baixo(DIA_EMPATADO, ultima=ULTIMA_REAL)
        assert escolha == "epomeno-epipedo", (
            "o desempate passou a depender da tabela do 713; isso seria trocar "
            "um criterio medido por um de amostra fraca sem dizer"
        )
    finally:
        cf.POR_PECA_713.clear()
        cf.POR_PECA_713.update(guardado)


def test_o_pendente_e_fonte_do_ultima_e_ela_bate_com_a_leitura_real():
    lido = cf.ultima_do_pendente()
    assert lido, "sem fonte o `ultima=` volta a nao ter origem"
    for canal, quando in ULTIMA_REAL.items():
        assert lido.get(canal, "") >= quando, (
            f"{canal}: o pendente nao pode ANDAR PARA TRAS — ele so cresce"
        )


def test_canal_AUSENTE_do_pendente_nao_vale_como_nunca_publicou():
    """Ausencia e silencio: o `mais_baixo` recusa em vez de inventar."""
    escolha, empatados = cf.mais_baixo(
        DIA_EMPATADO, ultima={"epomeno-epipedo": "2026-10-16T10:13:48Z"})
    assert escolha is None
    assert len(empatados) == 3


def test_o_modulo_DIZ_que_os_dois_criterios_existem():
    fonte = open(cf.__file__, encoding="utf-8").read()
    assert "nao a usa para desempate" in fonte
    assert "coincidencia de uma rodada" in fonte
