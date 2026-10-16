"""O heatmap publico NAO e retencao, e confundir os dois era o erro facil.

Pesquisa de 16/10 pedida pelo dono. O achado barato (o heatmap sai de graca pelo
`yt-dlp`, sem OAuth) vem com a ressalva que vale mais que ele: e a curva de
REPLAY. Nos quatro vencedores do nicho lidos, o pico cai no MEIO da peca e a
media dos tres primeiros segundos e MENOR que a do resto em 4 de 4 — logo quem
lesse isso como "abandono nos tres segundos" leria ao contrario.

Estes testes travam a distincao, o limiar MEDIDO (que corrige o numero da web) e
a forma exata da chamada da rota que de fato mede retencao.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import retencao as r  # noqa: E402

# As quatro curvas reais lidas em 16/10 (nicho excel/planilha, com heatmap).
VENCEDORES = [
    # (id, duracao_s, media_inicio_3s, media_resto, t_do_pico_s)
    ("OaC5PA5EVlM", 57, 0.114, 0.312, 19.9),
    ("39UFqdjlsEA", 70, 0.092, 0.330, 25.9),
    ("yxkmnVrd860", 66, 0.040, 0.625, 36.3),
    ("4JbMqtjQhRg", 29, 0.437, 0.600, 11.6),
]


def test_nos_QUATRO_vencedores_o_inicio_NAO_e_o_pico():
    """Se isto virar falso um dia, a leitura de replay tem de ser relida."""
    for vid, dur, ini, resto, t_pico in VENCEDORES:
        assert ini < resto, f"{vid}: inicio {ini} nao e menor que resto {resto}"
        assert t_pico > 3.0, f"{vid}: o pico caiu dentro dos 3 s"


def test_o_limiar_do_heatmap_foi_MEDIDO_e_nao_e_o_numero_da_web():
    lo, hi = r.LIMIAR_HEATMAP_OBSERVADO
    assert lo < hi
    assert lo > 10000, (
        "o blog dizia ~10 mil views; a medicao de doze pecas poe o limiar entre "
        f"{lo} e {hi}. Se alguem baixar isto para 10 mil, pediu fonte primaria"
    )


def test_o_limiar_NAO_e_funcao_so_de_views_e_o_modulo_diz_isso():
    """Um short de 29 s com 2,1 MILHOES veio SEM heatmap."""
    exc = r.SEM_HEATMAP_APESAR_DE_VIEWS
    assert exc["views"] > r.LIMIAR_HEATMAP_OBSERVADO[1] * 10
    assert "nao se preve pela contagem de views" in r.__doc__


def test_heatmap_vazio_LEVANTA_porque_e_ausencia_de_leitura():
    with pytest.raises(ValueError) as e:
        r.forma_do_replay([], 30.0)
    assert "AUSENCIA DE LEITURA" in str(e.value)


def test_a_funcao_se_chama_REPLAY_e_nao_devolve_chave_de_retencao():
    hm = [{"start_time": i * 0.3, "end_time": (i + 1) * 0.3, "value": 0.1}
          for i in range(100)]
    hm[40]["value"] = 1.0
    out = r.forma_do_replay(hm, 30.0)
    assert not any("reten" in k.lower() for k in out), (
        "nenhuma chave pode se chamar retencao: isto e replay"
    )
    assert out["balde_do_pico"] == 40 and out["inicio_e_o_pico"] is False


def test_a_resolucao_do_balde_em_short_e_sub_segundo():
    """Em 30 s cada balde mede 0,3 s — fino o bastante para os 3 s iniciais."""
    assert r.heatmap_tem_resolucao(30.0) == pytest.approx(0.3)
    assert r.baldes_ate(30.0, 3.0) == 10
    assert r.baldes_ate(530.0, 3.0) == 1  # num longo de 8 min, 3 s e UM balde


def test_a_query_de_retencao_exige_UM_video():
    q = r.query_de_retencao("abc12345678", "2026-10-01", "2026-10-16")
    assert q["dimensions"] == "elapsedVideoTimeRatio"
    assert q["filters"] == "video==abc12345678"
    assert "audienceWatchRatio" in q["metrics"]
    assert "relativeRetentionPerformance" in q["metrics"]
    for ruim in ("", "a,b"):
        with pytest.raises(ValueError):
            r.query_de_retencao(ruim, "2026-10-01", "2026-10-16")


def test_a_metrica_de_SWIPE_nao_existe_na_API_e_isso_vai_declarado():
    """Para eu nao prometer ao dono o que o clique dele nao compra."""
    assert r.METRICA_DE_SWIPE_EXISTE_NA_API is False
    assert "so do Studio" in r.__doc__


def test_o_escopo_necessario_JA_esta_no_codigo_de_producao():
    """A pendencia 1 e o CLIQUE, nao o codigo — e isto prova, abrindo o arquivo."""
    caminho = os.path.join(os.path.dirname(r.__file__), "tokens.py")
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    assert "yt-analytics.readonly" in fonte, (
        "se o escopo saiu de ESCOPOS, a pendencia 1 deixou de ser so o clique"
    )


def test_o_relato_NAO_promete_medir_as_NOSSAS_pecas_pelo_heatmap():
    texto = r.relato()
    assert "nao serve para NOS" in texto
