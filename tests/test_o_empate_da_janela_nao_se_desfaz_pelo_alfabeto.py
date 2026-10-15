"""O empate no mais baixo da janela NAO se desfaz pelo ALFABETO.

MEDIDO em 15/10 as 04:0x, e e uma divergencia doc<->codigo do meu proprio
modulo, feita duas rodadas antes. O comentario da regra dos dois niveis, escrito
as 02:0x, dizia em letra: "Empate na janela se desfaz pela peca mais ANTIGA".
O codigo desfazia com `min(FROTA, key=lambda c: (janela.get(c, 0), c))` — isto
e, pelo segundo elemento da chave, que e o NOME DO CANAL.

A janela desta rodada veio **12 / 6 / 6**, empatada entre `epomeno-epipedo` e
`kolejny-poziom`, e o relato anunciou `epomeno-epipedo` como "o mais baixo da
janela" por ele vir antes no alfabeto. **Ordem alfabetica nao e critério
medido**, e criterio sem procedencia e o que a §10 da rotina proibe — e aqui ele
governava a escolha de CANAL, que e a decisao mais consequente da rodada.

E a assinatura e a mesma do caso da mira de 13/10 as 20:2x: documento e codigo
discordando, com o documento prometendo a regra certa e o codigo aplicando
outra. A diferenca e que ali o doc estava ATRASADO contra o codigo, e aqui o doc
estava ADIANTE — a regra certa nunca tinha sido implementada.

O conserto NAO inventa limiar: `mais_baixo` devolve `None` quando empata e nao
tem como desempatar com dado medido, e quem chama DIZ que nao decidiu. Com
`ultima=` (o `max(publicado_em)` por canal) o desempate e o que o comentario ja
prometia: vence o canal cuja ultima peca e a mais ANTIGA.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import concentracao_frota as cf  # noqa: E402

# a janela REAL de 15/10 as 04:07, de `videos.publicado_em`
JANELA = {"labtreinamento": 12, "epomeno-epipedo": 6, "kolejny-poziom": 6}
ULTIMA = {
    "labtreinamento": "2026-10-14T15:12:24",
    "epomeno-epipedo": "2026-10-15T02:16:33",
    "kolejny-poziom": "2026-10-15T03:17:46",
}
DIA = {"labtreinamento": 0, "epomeno-epipedo": 2, "kolejny-poziom": 2}


def test_sem_dado_de_desempate_a_funcao_NAO_escolhe():
    baixo, empatados = cf.mais_baixo(JANELA)
    assert baixo is None
    assert empatados == ["epomeno-epipedo", "kolejny-poziom"]


def test_o_desempate_e_a_peca_mais_ANTIGA_e_nao_o_alfabeto():
    baixo, empatados = cf.mais_baixo(JANELA, ULTIMA)
    assert baixo == "epomeno-epipedo", baixo
    assert len(empatados) == 2
    # a contraprova que separa o criterio do acidente: invertendo as HORAS, o
    # vencedor inverte, embora a ordem alfabetica seja a MESMA.
    trocado = dict(ULTIMA)
    trocado["epomeno-epipedo"] = "2026-10-15T03:17:46"
    trocado["kolejny-poziom"] = "2026-10-15T02:16:33"
    assert cf.mais_baixo(JANELA, trocado)[0] == "kolejny-poziom"


def test_sem_empate_o_dado_de_desempate_e_irrelevante():
    j = {"labtreinamento": 12, "epomeno-epipedo": 6, "kolejny-poziom": 7}
    assert cf.mais_baixo(j)[0] == "epomeno-epipedo"
    assert cf.mais_baixo(j, ULTIMA)[0] == "epomeno-epipedo"
    assert cf.mais_baixo(j)[1] == ["epomeno-epipedo"]


def test_ultima_INCOMPLETA_nao_desempata_em_silencio():
    """Faltando a data de UM dos empatados, nao se escolhe: meia medicao nao e
    medicao, e preencher o ausente com um default seria inventar."""
    parcial = {"epomeno-epipedo": "2026-10-15T02:16:33"}
    assert cf.mais_baixo(JANELA, parcial)[0] is None


def test_o_relato_DIZ_que_empatou_e_nomeia_os_empatados():
    r = cf.relato(por_dia=DIA, janela=JANELA)
    assert "A JANELA EMPATOU" in r
    assert "epomeno-epipedo" in r and "kolejny-poziom" in r
    assert "ALFABETICA NAO DESEMPATA" in r
    # e NAO anuncia um mais baixo da janela que ele nao mediu
    assert "OS DOIS NIVEIS DISCORDAM" not in r


def test_com_ultima_o_relato_desempata_e_DECLARA_o_criterio():
    r = cf.relato(por_dia=DIA, janela=JANELA, ultima=ULTIMA)
    assert "o desempate foi MEDIDO" in r
    assert "mais\nANTIGA" in r or "mais ANTIGA" in r
    assert "OS DOIS NIVEIS DISCORDAM" in r
    assert "o da janela e epomeno-epipedo" in r


def test_a_regra_dos_dois_niveis_do_762_771_continua_inteira():
    """Falha se o conserto do empate tiver apagado a regra que ele acompanha."""
    r = cf.relato(por_dia=DIA, janela=JANELA, ultima=ULTIMA)
    assert "Quem governa a ESCOLHA e a JANELA" in r
    assert "INAUTENTICO" in r
    assert "7/dia por canal" in r
    assert "SEM NENHUMA PECA HOJE: labtreinamento" in r
