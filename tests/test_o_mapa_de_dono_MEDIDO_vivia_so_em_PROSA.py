# -*- coding: utf-8 -*-
"""O mapa de dono MEDIDO vivia so em PROSA. 20/10/2026, 10:1x.

O `concentracao.origem_de_outro_canal` existe desde 18/10 e exige um
`dono_medido` — "{youtube_id: canal}, e tem de vir de MEDICAO". O
`pauta_do_momento` nasceu em 20/10 as 08:2x chamando-o, e nas DUAS rodadas em
que ele teve o que dizer o relato saiu com "mapa de dono MEDIDO ausente":
ninguem passava o mapa porque ele nao existia como DADO.

E a medicao existia, escrita em PROSA no `CLAUDE.md` e nos docstrings de dois
modulos — em nenhum lugar que um instrumento pudesse LER.

O custo e de ESCOLHA DE PAUTA e esta medido: nesta rodada o instrumento deu o
`QiaGg03WSR0` como ESCOLHIDA no `kolejny-poziom` (a maior reserva do empate), e
esse id foi medido como longo do LabTreinamento. Com o mapa ele sai NOMEADO e a
vez passa a outra origem. Nas rodadas de 01:3x e 07:4x eu o tirei A MAO.
"""
import ast
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FABRICA)

import concentracao as CO      # noqa: E402
import dono_medido as DM       # noqa: E402
import pauta_do_momento as PM  # noqa: E402

FONTE_MAPA = os.path.join(FABRICA, "dono_medido.py")
FONTE_PM = os.path.join(FABRICA, "pauta_do_momento.py")
# O caso MEDIDO em 18/10 as 01:2x, e o canal que o declara por engano.
CASO = "QiaGg03WSR0"
CANAL = "kolejny-poziom"
DONO = "labtreinamento"


def test_o_mapa_NAO_esta_vazio_e_tem_o_caso_medido():
    """Vacuidade: mapa vazio faria todo teste abaixo passar sem medir nada."""
    m = DM.mapa()
    assert len(m) >= 1, m
    assert m.get(CASO) == DONO, m


def test_TODA_entrada_carrega_PROCEDENCIA_e_sem_ela_LEVANTA():
    """Mapa de dono sem medicao ao lado e palpite com cara de dado (733)."""
    for oid in DM.MEDIDOS:
        p = DM.procedencia(oid)
        assert p and len(p) >= 40, (oid, p)
    for torto in ({CASO: DONO},                      # sem a tupla
                  {CASO: (DONO, "")},                # procedencia vazia
                  {CASO: (DONO, "medido")},          # curta demais
                  {CASO: ("", "x" * 80)}):           # sem canal
        with pytest.raises(ValueError):
            DM._valida(torto)


def test_id_FORA_do_mapa_e_DESCONHECIDO_e_nao_do_proprio_canal():
    """A guarda do 725: desconhecido nao entra como "de outro canal"."""
    assert DM.procedencia("id-que-nunca-foi-medido") is None
    fora = CO.origem_de_outro_canal(CANAL, DM.mapa())
    assert set(fora) <= set(DM.mapa()), fora
    assert "o mapa NAO e exaustivo" in DM.relato()


def test_o_PADRAO_do_pauta_do_momento_traz_o_mapa():
    e = PM.escolha(CANAL)
    assert e["sem_mapa_de_dono"] is False
    r = PM.relato(CANAL)
    assert "mapa de dono MEDIDO presente" in r
    assert "NAO e exaustivo" in r


def test_o_DEFEITO_medido_e_a_mudanca_de_ESCOLHA():
    """Contraprova nos DOIS sentidos, e e o defeito desta rodada.

    Cobrado por PROPRIEDADE: sem o mapa a origem medida como de OUTRO canal e
    escolhivel; com o mapa ela nao e. Cravar o id da escolha nova seria
    identidade onde ha propriedade (743/753/761) — ela muda com a contagem.
    """
    sem = PM.escolha(CANAL, dono_medido={})
    com = PM.escolha(CANAL)
    if sem["escolhida"] is None or com["escolhida"] is None:
        pytest.skip("o canal ficou sem origem com reserva; a regra segue cobrada")
    if sem["escolhida"]["origem"] != CASO:
        pytest.skip(
            "a contagem andou e o caso medido ja nao e o primeiro do empate; "
            "o que importa e a propriedade cobrada abaixo")
    assert com["escolhida"]["origem"] != CASO, (
        "com o mapa, a origem MEDIDA como de outro canal nao pode ser a "
        "escolhida: %r" % (com["escolhida"],))
    assert CASO in com["nomeados_como_suspeitos"]


def test_ela_e_NOMEADA_e_nao_FILTRADA():
    """Esconder faria a rodada seguinte perguntar por que a lista encurtou."""
    com = PM.escolha(CANAL)
    ids = [x["origem"] for x in com["quadro"]]
    assert CASO in ids, "a origem suspeita saiu da LISTA, nao so da escolha"
    r = PM.relato(CANAL)
    assert CASO in r
    assert "SUSPEITA de ser do %s" % DONO in r


def test_os_DOIS_ramos_existem_e_a_resolucao_tem_UM_dono():
    """Por AST: `None` = mapa medido, `{}` = sem mapa, e um so lugar decide.

    A primeira versao deste conserto resolvia no `quadro` e calculava a FLAG no
    `escolha` a partir do argumento NAO resolvido — dois donos do mesmo fato,
    dentro do conserto da mesma assinatura.
    """
    assert PM.escolha(CANAL, dono_medido={})["sem_mapa_de_dono"] is True
    assert "mapa de dono MEDIDO ausente" in PM.relato(CANAL, dono_medido={})
    arvore = ast.parse(io.open(FONTE_PM, encoding="utf-8").read())
    donos = set()
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        for d in ast.walk(no):
            if (isinstance(d, ast.Call)
                    and isinstance(d.func, ast.Attribute)
                    and getattr(d.func.value, "id", None) == "DM"
                    and d.func.attr == "mapa"):
                donos.add(no.name)
    assert donos == {"_resolve_mapa"}, donos


def test_o_mapa_NAO_reimplementa_a_deteccao():
    """Por AST: quem cruza canal com dono e o `concentracao`, nao este modulo.

    Um segundo detector aqui seria o segundo dono da regra — a assinatura que
    congelou a legenda.
    """
    fonte = io.open(FONTE_MAPA, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call):
            nome = getattr(no.func, "attr", None) or getattr(no.func, "id", None)
            assert nome not in ("contagem", "origem_de_outro_canal", "glob",
                                "listdir", "open"), nome
    assert "import" not in fonte.split('"""')[2], (
        "o modulo de dado nao importa ninguem: ele e so o mapa")


def test_o_MOTIVO_continua_escrito_nos_DOIS_modulos():
    mapa = io.open(FONTE_MAPA, encoding="utf-8").read()
    for marca in ("em PROSA", "a mao", "item 3", "725", "733", CASO):
        assert marca in mapa, (
            "conserto sem o motivo escrito volta calado: falta %r" % marca)
    pm = io.open(FONTE_PM, encoding="utf-8").read()
    assert "dono_medido.mapa()" in pm
    assert "dois donos do mesmo fato" in pm


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
