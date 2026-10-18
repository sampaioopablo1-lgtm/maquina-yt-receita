# -*- coding: utf-8 -*-
"""A PLAYLIST `UU...` OMITE UM CONJUNTO DIFERENTE EM CADA LEITURA — 18/10 06:1x→07:1x.

A nota de 01:2x diz que a playlist de uploads e INCOMPLETA: ela devolveu
treze longos do `labtreinamento` enquanto `StQNFMdpGdk` e `XgqPVJuAk3o`
eram publicos do mesmo canal e nao apareciam. Eu tratei isso como um
defeito ESTAVEL — "ela omite esses dois".

**Medido as 07:0x, tres horas depois: ela devolveu DOZE.** O
`KRUERlNPzDw` saiu da leitura, e ele e **publico** (`isUnlisted: false`,
`isPrivate: false`), do mesmo canal (`author` LabTreinamento), 823 s,
com QUATRO shorts ja tirados dele. Nada foi publicado nem despublicado
entre as duas leituras.

**Logo a omissao nao e um conjunto fixo: ela VARIA entre leituras.** E a
consequencia bate na regra de 16/10 — *"a pauta serve o longo MAIS NOVO
primeiro"* — porque o rank de uma origem, e a propria presenca dela,
mudam de uma rodada para a outra sem nada ter acontecido no canal.

O que isto NAO prova: qual e a causa, nem que a omissao e aleatoria.
Duas leituras nao medem distribuicao. O que esta medido e a NEGACAO de
"a playlist omite um conjunto fixo".

A regra que fica: **a ordem viva ordena, nao enumera — e o conjunto que
ela devolve numa leitura nao e o conjunto que ela devolve na seguinte.**
Antes de dizer que uma origem nao existe mais, leia a PAGINA dela.
"""
import os, re

AQUI = os.path.dirname(__file__)
CLAUDE = os.path.join(AQUI, '..', 'CLAUDE.md')

# As duas leituras, medidas na mesma sessao com ~3 h de intervalo.
LEITURA_04 = ["FtCtIJPsc_Q", "NNgAQLlpEzg", "Sr6VhvD_aPE", "QiaGg03WSR0",
              "lau1nnOUm1U", "6BeNHqT2okA", "dsoEo103l1o", "bQoujWaY7Hw",
              "ntrMxq89I4o", "4OYBkCHFTV8", "3KtwRYxl7_U", "yrWVyqQtw00",
              "KRUERlNPzDw"]
LEITURA_07 = ["FtCtIJPsc_Q", "NNgAQLlpEzg", "Sr6VhvD_aPE", "QiaGg03WSR0",
              "lau1nnOUm1U", "6BeNHqT2okA", "dsoEo103l1o", "bQoujWaY7Hw",
              "ntrMxq89I4o", "4OYBkCHFTV8", "3KtwRYxl7_U", "yrWVyqQtw00"]

# Medido na pagina de cada uma, com Accept-Language pt-BR.
PUBLICAS_DO_CANAL = {
    "KRUERlNPzDw": {"unlisted": False, "private": False,
                    "author": "LabTreinamento", "len": 823},
    "StQNFMdpGdk": {"unlisted": False, "private": False,
                    "author": "LabTreinamento", "len": 872},
    "XgqPVJuAk3o": {"unlisted": False, "private": False,
                    "author": "LabTreinamento", "len": 786},
}
USOS_DO_KRUER = 4      # ele ja rendeu shorts: nao e origem desconhecida


def test_as_duas_leituras_DIFEREM():
    """O fato cru. Sem ele o arquivo nao retrata nada."""
    assert set(LEITURA_04) != set(LEITURA_07), (
        "as duas leituras passaram a ser iguais. Se a playlist ficou "
        "estavel, esta nota tem de ser RELIDA — o risco era de metodo, nao "
        "daquela hora.")


def test_o_que_saiu_e_PUBLICO_do_proprio_canal():
    """Omissao de peca publica e o achado; omissao de peca removida nao
    seria achado nenhum."""
    saiu = set(LEITURA_04) - set(LEITURA_07)
    assert saiu, "nada saiu entre as leituras."
    for vid in saiu:
        m = PUBLICAS_DO_CANAL.get(vid)
        assert m, f"{vid} saiu da playlist e nao foi medido na pagina."
        assert m["unlisted"] is False and m["private"] is False, (
            f"{vid} nao e publica, logo a omissao e esperada e esta nota "
            "perde o caso.")
        assert m["author"] == "LabTreinamento", (
            f"{vid} nao e do canal, logo a omissao e esperada.")
        assert m["len"] > 180, f"{vid} nao e longo."


def test_a_omissao_NAO_e_um_conjunto_fixo():
    """O que a nota de 01:2x supunha sem dizer."""
    omitidas_sempre = set(PUBLICAS_DO_CANAL) - set(LEITURA_04) - set(LEITURA_07)
    omitidas_so_numa = (set(PUBLICAS_DO_CANAL) & set(LEITURA_04)) - set(LEITURA_07)
    assert omitidas_sempre, (
        "nenhuma peca publica ficou fora das DUAS leituras — a nota de "
        "01:2x perdeu o apoio e tem de ser relida.")
    assert omitidas_so_numa, (
        "nenhuma peca entrou numa leitura e saiu da outra. Sem isso a "
        "omissao pode ser fixa, e o achado desta rodada cai.")


def test_a_peca_omitida_NAO_era_origem_desconhecida():
    """Ela ja rendeu shorts, logo o efeito atinge pauta em uso, nao so
    pauta virgem."""
    assert USOS_DO_KRUER >= 1, (
        "se a peca omitida nunca rendeu short, o efeito e menor do que a "
        "nota diz — releia antes de reaproveitar."
    )


def test_a_contagem_de_longos_do_canal_e_um_PISO_em_qualquer_leitura():
    """A propriedade util: a leitura da um limite inferior, nunca o total."""
    for leitura in (LEITURA_04, LEITURA_07):
        conhecidas = set(PUBLICAS_DO_CANAL) | set(leitura)
        assert len(conhecidas) > len(leitura), (
            "a leitura passou a conter tudo o que conhecemos. Se isso "
            "persistir, a nota muda de 'omite' para 'omitia'."
        )


def test_a_nota_fica_escrita_no_CLAUDE_md():
    t = re.sub(r'\s+', ' ', open(CLAUDE, encoding='utf-8').read())
    assert 'KRUERlNPzDw' in t, (
        "a peca que saiu da playlist nao esta nomeada no CLAUDE.md; sem o "
        "id ninguem refaz a medicao.")
    # case-insensitive de proposito: o documento usa caixa alta para enfase, e
    # travar a CAIXA e travar formatacao em vez da propriedade (743/753).
    assert re.search(r'varia\s+entre\s+leituras', t, re.I), (
        "o CLAUDE.md nao diz que a omissao VARIA. Sem isso a nota de 01:2x "
        "segue lida como 'ela omite esses dois', que e o que esta rodada "
        "falsificou.")


def test_e_a_nota_de_01_2x_NAO_foi_apagada_por_esta():
    """Esta rodada FORTALECE aquela; apagar a de 01:2x perderia o achado
    original (a playlist nao e o conjunto)."""
    t = re.sub(r'\s+', ' ', open(CLAUDE, encoding='utf-8').read())
    assert 'StQNFMdpGdk' in t and 'XgqPVJuAk3o' in t, (
        "os dois ids da nota de 01:2x sairam do CLAUDE.md.")
    assert re.search(r'ordem.{0,40}n[aã]o.{0,30}conjunto|'
                     r'Ela d[aá] uma \*\*ordem\*\*', t, re.I), (
        "a frase que distingue ORDEM de CONJUNTO saiu do CLAUDE.md — ela e "
        "a parte da nota de 01:2x que esta rodada confirma.")
