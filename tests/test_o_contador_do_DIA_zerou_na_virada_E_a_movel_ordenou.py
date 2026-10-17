"""A primeira virada de meia-noite depois do 771 — e o instrumento funcionou.

O **771** nasceu em 15/10 as 00:0x de um defeito: depois de eu escolher o canal
em seis rodadas seguidas pelo contador, o `relato(por_dia=...)` devolveu
**0 / 0 / 0** — o dia calendario acabara de comecar — e NAO ordenou nada
exatamente na rodada que precisava escolher. A saida foi a JANELA MOVEL de 24 h,
que preserva as ultimas horas em vez de apaga-las na meia-noite.

Isso era conserto sem verificacao em producao: a partir dali as rodadas cairam
todas DENTRO do dia, e o caso nunca se repetiu.

**Medido em 17/10 as 00:0x, na primeira virada depois do conserto:**

| contagem | labtreinamento | epomeno | kolejny | ordena? |
|---|---|---|---|---|
| dia calendario (17/10) | 0 | 0 | 0 | **nao** |
| janela movel de 24 h | 8 | 9 | 8 | **sim** |

A movel escolheu `kolejny-poziom` pelo desempate da peca mais ANTIGA
(21:12:51 contra 22:13:18 do labtreinamento), e a peca saiu dali.

**O que este arquivo NAO afirma:** que a escolha foi a melhor possivel. Ela foi a
escolha que o criterio DECLARADO produz — e o valor do 771 nao e acertar o canal,
e nao ficar sem criterio na unica hora do dia em que o contador do dia e cego.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import concentracao_frota as cf  # noqa: E402

DIA_ZERADO = {"labtreinamento": 0, "epomeno-epipedo": 0, "kolejny-poziom": 0}
MOVEL_17_10 = {"labtreinamento": 8, "epomeno-epipedo": 9, "kolejny-poziom": 8}
ULTIMA_17_10 = {
    "kolejny-poziom": "2026-10-16T21:12:51Z",
    "epomeno-epipedo": "2026-10-16T23:13:14Z",
    "labtreinamento": "2026-10-16T22:13:18Z",
}


def test_o_dia_recem_virado_NAO_ordena():
    """A premissa do 771, reproduzida: tudo em zero nao desempata nada."""
    assert len(set(DIA_ZERADO.values())) == 1
    escolha, empatados = cf.mais_baixo(DIA_ZERADO, ultima=ULTIMA_17_10)
    # Com tudo zerado, o desempate por DATA e a unica informacao que resta.
    assert len(empatados) == 3, empatados
    assert escolha == "kolejny-poziom", escolha


def test_a_janela_MOVEL_ordena_na_mesma_hora():
    escolha, empatados = cf.mais_baixo(MOVEL_17_10, ultima=ULTIMA_17_10)
    assert set(empatados) == {"labtreinamento", "kolejny-poziom"}, empatados
    assert escolha == "kolejny-poziom", escolha


def test_as_duas_contagens_DISCORDAM_do_numero_e_nao_da_escolha():
    """O ponto fino: elas dao o mesmo canal por razoes diferentes.

    No dia zerado a escolha vem SO da data; na movel vem da contagem mais a data.
    Coincidirem aqui NAO valida o dia calendario — ele seguiria dando a mesma
    resposta com qualquer historico, porque nao ve historico nenhum.
    """
    por_dia = cf.mais_baixo(DIA_ZERADO, ultima=ULTIMA_17_10)[0]
    por_movel = cf.mais_baixo(MOVEL_17_10, ultima=ULTIMA_17_10)[0]
    assert por_dia == por_movel
    # Contraprova: trocando as contagens da movel, ela muda de canal e o dia nao.
    outra = dict(MOVEL_17_10, **{"labtreinamento": 2})
    assert cf.mais_baixo(outra, ultima=ULTIMA_17_10)[0] == "labtreinamento"
    assert cf.mais_baixo(DIA_ZERADO, ultima=ULTIMA_17_10)[0] == por_dia


def test_a_movel_PRESERVA_o_que_a_meia_noite_apagaria():
    assert sum(MOVEL_17_10.values()) == 25
    assert sum(DIA_ZERADO.values()) == 0, (
        "vinte e cinco pecas das ultimas 24 h sumiriam do criterio se so o dia "
        "calendario decidisse — e esse e o defeito que o 771 nomeia")


def test_o_contador_REAL_reproduz_as_duas_contagens():
    """Ancorado no arquivo de verdade, nao na minha anotacao."""
    dia = cf.contagem_do_pendente("2026-10-17")
    movel = cf.contagem_do_pendente("2026-10-16T00:07:00Z")
    assert sum(movel.values()) >= sum(dia.values())
    assert sum(movel.values()) >= 20, (
        "se o pendente for esvaziado (o execute_sql voltou), este teste tem de "
        "ser RELIDO em vez de ajustado")


def test_o_docstring_nao_reivindica_a_escolha_CERTA():
    texto = " ".join(__doc__.split())
    assert "NAO afirma" in texto
    assert "nao e acertar o canal" in texto
