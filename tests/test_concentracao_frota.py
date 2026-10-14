"""O contador de concentracao ENTRE canais (762).

Ele nasceu porque eu reproduzi, uma camada acima, o habito que o
`concentracao.py` consertou: 16 das 16 pecas de 14/10 sairam no mesmo canal.
Os testes travam (a) o limiar REUSADO do irmao, (b) a fronteira exata do dobro,
(c) que acervo e dia sao contagens DIFERENTES, e (d) que o relato nao cala
quando o dia nao foi passado.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import concentracao  # noqa: E402
import concentracao_frota as F  # noqa: E402


def test_a_frota_e_os_tres_canais_da_decisao_do_dono():
    assert F.FROTA == ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def test_o_limiar_e_o_MESMO_do_irmao_e_nao_um_numero_novo():
    """Inventar limiar aqui seria criterio sem procedencia (trava da §10)."""
    fonte = (RAIZ / "fabrica" / "concentracao_frota.py").read_text(encoding="utf-8")
    assert "2 * n_seg" in fonte
    irmao = (RAIZ / "fabrica" / "concentracao.py").read_text(encoding="utf-8")
    assert "2 *" in irmao, "se o irmao mudar de limiar, este modulo tem de ser relido"


def test_a_fronteira_do_dobro_nao_alerta__o_caso_real_do_acervo():
    """50 contra 25 e EXATAMENTE o dobro, e o dobro nao e MAIS que o dobro.

    E o acervo real de 14/10 as 16:1x. Eu relato "dentro do dobro" em vez de
    arredondar para alertou — foi o mesmo cuidado do caso 10-contra-5 do irmao.
    """
    a = F.analise({"labtreinamento": 50, "epomeno-epipedo": 25, "kolejny-poziom": 22})
    assert a["dominante"] == "labtreinamento"
    assert a["n_segunda"] == 25
    assert a["alerta"] is False
    a2 = F.analise({"labtreinamento": 51, "epomeno-epipedo": 25, "kolejny-poziom": 22})
    assert a2["alerta"] is True


def test_o_DIA_de_14_10_alerta_e_nomeia_os_canais_zerados():
    """16 / 0 / 0, medido em `videos.publicado_em`."""
    a = F.analise({"labtreinamento": 16, "epomeno-epipedo": 0, "kolejny-poziom": 0})
    assert a["alerta"] is True
    assert set(a["zerados"]) == {"epomeno-epipedo", "kolejny-poziom"}
    assert a["total"] == 16


def test_canal_zerado_NAO_entra_como_segundo_colocado():
    """Senao um canal morto viraria o comparador e o dobro nunca dispararia."""
    a = F.analise({"labtreinamento": 16, "epomeno-epipedo": 0, "kolejny-poziom": 0})
    assert a["n_segunda"] == 0 and a["alerta"] is True


def test_frota_inteira_em_zero_nao_estoura():
    a = F.analise({c: 0 for c in F.FROTA})
    assert a["dominante"] is None and a["alerta"] is False


def test_o_relato_SEM_o_dia_declara_que_esta_lendo_ACERVO():
    """O buraco que a primeira execucao mostrou: acervo DILUI rodada."""
    t = F.relato()
    assert "ACERVO NAO E O DIA" in t
    assert "por_dia" in t


def test_o_relato_COM_o_dia_nomeia_os_zerados_e_alerta():
    t = F.relato(por_dia={"labtreinamento": 16, "epomeno-epipedo": 0,
                          "kolejny-poziom": 0})
    assert "NO DIA: 16" in t
    assert "ALERTA DO DIA" in t
    assert "epomeno-epipedo" in t and "kolejny-poziom" in t
    assert "ACERVO NAO E O DIA" not in t


def test_o_relato_DIZ_que_concentrar_e_o_plano__e_nao_reprova():
    """A ressalva nao e decorativa: os 500 sao limite POR CANAL."""
    t = F.relato()
    assert "nao reprova" in t
    assert "POR CANAL" in t


def test_o_ranking_do_713_tem_o_epomeno_longo_no_topo_e_o_labtreinamento_no_fim():
    r = F.ranking_713()
    assert r[0][0] == ("epomeno-epipedo", "longo")
    assert r[-1][0] == ("labtreinamento", "longo")
    assert F.par_do_dia("labtreinamento", "shorts") == 0.07
    assert F.par_do_dia("epomeno-epipedo", "longo") == 0.33
    assert F.par_do_dia("nao-existe", "shorts") is None


def test_a_contagem_le_a_MESMA_fonte_do_irmao():
    ct = F.contagem()
    assert set(ct) == set(F.FROTA)
    assert ct["labtreinamento"] == sum(concentracao.contagem("labtreinamento").values())
    assert all(n > 0 for n in ct.values()), "os tres canais da frota tem shorts"
