"""Publicar sem registrar cega a trava anti-duplicata.

Medido em 17/08/2026. O `publicar.py` subiu o seja-mais-magra-002 as 16:33 —
short 58oHNtVaAbg e longo 8ffwzHFW9ws, os dois publicos no canal certo — e
saiu com codigo 0 imprimindo os dois ids. A tabela `videos` nao ganhou uma
linha sequer.

O estrago nao e o registro faltando: e que as DUAS travas de `main()`
consultam `videos`. Se a frota publica sem registrar, elas nao enxergam
exatamente aquilo que a frota publicou. O disparo do cron das 17:01 recolocou
o mesmo pacote na fila e as duas o teriam liberado.
"""

import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402


SPEC = {
    "pacote": "seja-mais-magra-002",
    "slug": "seja-mais-magra-002",
    "fonte_pauta": "jVWCkaXZ83c",
    "longo": [{}] * 75,
    "short": [{}] * 4,
}
COPY = {
    "titulo": "Ozempic e Mounjaro: O Que Você Reganha Não É o Que Você Perdeu",
    "descricao": "abre\n\n0:00 Intro\n1:57 Como se mede\n3:35 O exame\n11:28 Os numeros",
}


@pytest.fixture
def espiao(monkeypatch, tmp_path):
    """Guarda cada POST/PATCH que o registro manda ao PostgREST."""
    enviados = []

    class Resp:
        def read(self):
            return b""

    def falso(url, data=None, method="GET", headers=None, timeout=60):
        enviados.append((method, url, json.loads(data) if data else None))
        return Resp()

    monkeypatch.setattr(P, "_req", falso)
    json.dump([10.0] * 75, open(tmp_path / "tempos.json", "w"))
    return enviados


def test_registra_as_duas_linhas(espiao, tmp_path):
    linhas = P.registrar({"short": "58oHNtVaAbg", "longo": "8ffwzHFW9ws"},
                         SPEC, COPY, str(tmp_path), "seja-mais-magra",
                         "https://sb", "k")
    por_formato = {l["formato"]: l for l in linhas}
    assert por_formato["longo"]["youtube_id"] == "8ffwzHFW9ws"
    assert por_formato["shorts"]["youtube_id"] == "58oHNtVaAbg"
    assert por_formato["longo"]["slug"] == "seja-mais-magra-002"
    assert por_formato["shorts"]["slug"] == "seja-mais-magra-002-short"
    assert por_formato["longo"]["cenas"] == 75
    assert por_formato["shorts"]["cenas"] == 4
    assert por_formato["longo"]["fonte_pauta"] == "jVWCkaXZ83c"


def test_a_trava_por_titulo_passa_a_enxergar_o_que_a_frota_publicou(espiao, tmp_path):
    """O nucleo do defeito: o titulo registrado e o mesmo que a trava procura."""
    linhas = P.registrar({"short": "58oHNtVaAbg", "longo": "8ffwzHFW9ws"},
                         SPEC, COPY, str(tmp_path), "seja-mais-magra",
                         "https://sb", "k")
    gravados = [l["titulo"] for l in linhas]
    assert COPY["titulo"] in gravados

    class Banco:
        def read(self):
            return json.dumps([{"pacote": l["pacote"], "formato": l["formato"],
                                "youtube_id": l["youtube_id"], "titulo": l["titulo"]}
                               for l in linhas]).encode()

    P._req = lambda *a, **k: Banco()
    assert P.ja_no_ar_pelo_titulo(COPY["titulo"], "https://sb", "k")


def test_conta_os_capitulos_da_descricao(espiao, tmp_path):
    linhas = P.registrar({"longo": "8ffwzHFW9ws"}, SPEC, COPY, str(tmp_path),
                         "seja-mais-magra", "https://sb", "k")
    assert linhas[0]["capitulos"] == 4


def test_duracao_sai_do_tempos_json(espiao, tmp_path):
    """O mesmo numero que o etapas.py imprime, e nao a estimativa da spec."""
    linhas = P.registrar({"longo": "8ffwzHFW9ws"}, SPEC, COPY, str(tmp_path),
                         "seja-mais-magra", "https://sb", "k")
    assert linhas[0]["duracao_s"] == 750.0


def test_manda_um_post_em_videos_e_um_patch_em_canais(espiao, tmp_path):
    P.registrar({"short": "58oHNtVaAbg", "longo": "8ffwzHFW9ws"}, SPEC, COPY,
                str(tmp_path), "seja-mais-magra", "https://sb", "k")
    metodos = [(m, u.split("/rest/v1/")[-1].split("?")[0]) for m, u, _ in espiao]
    assert ("POST", "videos") in metodos
    assert ("PATCH", "canais") in metodos


def test_falha_no_banco_nao_derruba_a_publicacao(monkeypatch, tmp_path, capsys):
    """Os videos ja estao no ar; levantar aqui mascararia o sucesso."""
    def explode(*a, **k):
        raise RuntimeError("PostgREST fora do ar")
    monkeypatch.setattr(P, "_req", explode)
    json.dump([10.0] * 75, open(tmp_path / "tempos.json", "w"))

    linhas = P.registrar({"longo": "8ffwzHFW9ws"}, SPEC, COPY, str(tmp_path),
                         "seja-mais-magra", "https://sb", "k")
    assert linhas
    assert "8ffwzHFW9ws" in capsys.readouterr().err


def test_sem_publicacao_nao_grava_nada(espiao, tmp_path):
    assert P.registrar({}, SPEC, COPY, str(tmp_path), "seja-mais-magra",
                       "https://sb", "k") == []
    assert espiao == []
