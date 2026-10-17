"""Peca publicada com a rota da duracao FECHADA nao perde o ponto de residuo.

MEDIDO em 17/10. A rota `watch?v=` fechou as 03:1x e seguia fechada as 04:1x
(confirmado pela peca de CONTROLE). Duas pecas foram ao ar nesse intervalo e
ficaram sem duracao REAL: o `kolejny-poziom-s049` e o `labtreinamento-s066`.

Em 16/10 a mesma coisa aconteceu com DEZESSETE pecas, e elas foram parqueadas na
minha cabeca — sairam porque eu me lembrei, nao porque havia instrumento.

O campo que carrega o risco e o PROVEDOR: ele se MEDE pela anotacao do job (733),
e anotacao envelhece. Parquear sem ele obrigaria a rodada futura a INFERIR qual
mundo narrou pela distancia entre previsao e real — o erro exato do 733.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import duracao_a_medir as dm

REG = {
    "pacote": "labtreinamento-s066", "youtube_id": "6jHGn7fae4c",
    "prev_edge": 25.6, "prev_piper": 21.0, "provedor": "edge",
    "job": "117305098967", "em": "2026-10-17T04:11:02Z",
}


def test_o_PROVEDOR_e_obrigatorio__pelo_733(tmp_path):
    sem = {k: v for k, v in REG.items() if k != "provedor"}
    with pytest.raises(ValueError) as e:
        dm.parqueia(sem, str(tmp_path / "x.jsonl"))
    assert "733" in str(e.value), "o motivo tem de NOMEAR o aprendizado"


def test_o_JOB_tambem__porque_e_de_onde_sai_a_anotacao(tmp_path):
    sem = {k: v for k, v in REG.items() if k != "job"}
    with pytest.raises(ValueError):
        dm.parqueia(sem, str(tmp_path / "x.jsonl"))


def test_provedor_desconhecido_LEVANTA_em_vez_de_entrar(tmp_path):
    with pytest.raises(ValueError):
        dm.parqueia({**REG, "provedor": "piper-low"}, str(tmp_path / "x.jsonl"))


def test_parquear_duas_vezes_NAO_duplica_o_ponto(tmp_path):
    p = str(tmp_path / "x.jsonl")
    assert dm.parqueia(REG, p) is True
    assert dm.parqueia(REG, p) is False
    assert len(dm.carrega(p)) == 1, "duplicar infla a serie do 739 sem medicao"


def test_o_residuo_sai_contra_a_previsao_do_provedor_GRAVADO(tmp_path):
    p = str(tmp_path / "x.jsonl")
    dm.parqueia(REG, p)
    r = dm.residuos({"6jHGn7fae4c": 28}, p)[0]
    assert r["previsao"] == 25.6, "edge gravado -> previsao do edge"
    assert r["residuo"] == pytest.approx(2.4)
    # e com provedor piper a MESMA leitura real da outro residuo
    p2 = str(tmp_path / "y.jsonl")
    dm.parqueia({**REG, "provedor": "piper"}, p2)
    assert dm.residuos({"6jHGn7fae4c": 28}, p2)[0]["previsao"] == 21.0


def test_sinal_estabelecido_segue_o_criterio_do_770(tmp_path):
    p = str(tmp_path / "x.jsonl")
    dm.parqueia(REG, p)
    assert dm.residuos({"6jHGn7fae4c": 28}, p)[0]["estabelecido"] is True
    assert dm.residuos({"6jHGn7fae4c": 26}, p)[0]["estabelecido"] is False, (
        "26 - 25,6 = 0,4 <= 1,0: a janela de arredondamento contem a previsao")


def test_ausencia_de_leitura_NAO_e_residuo_zero(tmp_path):
    p = str(tmp_path / "x.jsonl")
    dm.parqueia(REG, p)
    r = dm.residuos({}, p)[0]
    assert r["real"] is None and r["residuo"] is None
    assert r["estabelecido"] is False


def test_o_relato_MANDA_conferir_a_rota_com_a_peca_de_controle(tmp_path):
    p = str(tmp_path / "x.jsonl")
    dm.parqueia(REG, p)
    t = dm.relato({}, p)
    assert "CONTROLE" in t and "veredito_da_rota" in t, (
        "sem isso a rodada le 'sem leitura' como defeito da peca — 17/10 03:1x")


def test_as_DUAS_pecas_de_17_10_estao_no_arquivo_do_repo():
    """Ancora real: se alguem apagar o parque, a medicao perdida volta a perder."""
    regs = dm.carrega()
    ids = {r["youtube_id"] for r in regs}
    assert {"O5o2SnovdEo", "6jHGn7fae4c"} <= ids
    for r in regs:
        assert r["provedor"] in ("edge", "piper") and r["job"]


def test_o_arquivo_parqueado_e_JSONL_valido_linha_a_linha():
    with open(dm.CAMINHO, encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                json.loads(linha)
