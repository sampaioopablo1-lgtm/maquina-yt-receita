"""O medidor pode errar de tres formas, e as tres ja aconteceram de verdade.

`fabrica/medir.py` nasceu em 11/10, quando o segredo YT_OAUTH_JSON entrou e o
token passou a nascer no runner — ler a API deixou de depender do banco. Mas um
medidor novo repete os erros antigos se ninguem travar:

  * usar o `viewCount` do CANAL como denominador (697), ou normalizar um canal
    com acervo anterior a maquina (668);
  * deixar um lote que falhou virar um total menor (665) — agregado esconde
    chamada que falhou, e foi assim que "134/134 vivos" nasceu de um 401;
  * escolher a replica no olho (708) em vez de pela SOMA das chamadas.

E o de sempre: nao vazar segredo.
"""

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import medir  # noqa: E402


def test_sao_TRES_leituras_porque_a_replica_e_da_chamada():
    """708: uma leitura so nao distingue replica fresca de atrasada."""
    assert medir.LEITURAS == 3


def test_quem_escolhe_a_chamada_e_o_replica_pela_SOMA():
    fonte = __import__("inspect").getsource(medir.mede_canal)
    assert "replica.chamada_para_gravar(leituras)" in fonte
    assert "replica.piso(leituras)" in fonte
    assert "replica.mesma_forma(leituras)" in fonte


def test_o_denominador_sai_do_conversao_e_NAO_do_viewCount_do_canal():
    """697: o viewCount do CANAL nao e a soma e nem conta Shorts (638).

    O viewCount por VIDEO e justamente o que se le — o que nao pode entrar e o
    do `channels.list`, que veio byte a byte igual por doze horas enquanto as
    pecas somavam centenas (703). Entao o teste nao proibe a palavra: proibe
    tirar `viewCount` do dicionario de estatisticas DO CANAL.
    """
    fonte = __import__("inspect").getsource(medir.mede_canal)
    codigo = "\n".join(l for l in fonte.splitlines()
                       if not l.strip().startswith("#"))
    assert "conversao.relato_por_mil(" in codigo
    assert 'est.get("viewCount"' not in codigo
    assert 'est.get("subscriberCount"' in codigo
    assert '(it.get("statistics") or {}).get("viewCount"' in codigo


def test_labtreinamento_continua_sem_normalizacao():
    """668: canal com acervo anterior a maquina nao tem denominador valido."""
    assert medir.conversao.por_mil("labtreinamento", 67, [4165]) is None
    assert medir.conversao.por_mil("epomeno-epipedo", 17, [15454]) is not None


def test_lote_vazio_LEVANTA_em_vez_de_virar_total_menor():
    """665: o defeito nao e o erro, e o erro que vira numero plausivel."""
    import json
    import io

    chamadas = []

    def falso(url, token):
        chamadas.append(url)
        return {"items": []}

    original, medir._get = medir._get, falso
    try:
        try:
            medir.uma_chamada(["aaa", "bbb"], "tok")
        except RuntimeError as e:
            assert "vazio" in str(e)
        else:
            raise AssertionError("lote vazio passou calado")
    finally:
        medir._get = original
    del json, io


def test_a_peca_fora_de_processed_sai_NOMEADA():
    fora = medir.doentes({
        "vivo": {"status": {"uploadStatus": "processed"},
                 "contentDetails": {"duration": "PT41S"}},
        "Ta_KN8yXLaI": {"status": {"uploadStatus": "uploaded"},
                        "contentDetails": {"duration": "P0D"}},
    })
    assert fora == ["Ta_KN8yXLaI (uploaded, P0D)"]


def test_o_medidor_NAO_imprime_segredo(capsys, monkeypatch):
    """A mesma propriedade da sonda, pelo mesmo motivo: log publico."""
    import json

    SENTINELA = "SEGREDO-REFRESH-NAO-PODE-SAIR"
    monkeypatch.setenv("YT_OAUTH_JSON", json.dumps(
        {"outro-canal": {"client_id": "x", "client_secret": "y",
                         "refresh_token": SENTINELA}}))
    medir.main()
    saida = capsys.readouterr().out
    assert SENTINELA not in saida, "O MEDIDOR VAZOU O REFRESH TOKEN"
    # E diz, canal por canal, que nao mediu — silencio seria pior.
    for canal in medir.CANAIS:
        assert f"{canal}: FORA do YT_OAUTH_JSON" in saida


def test_sem_segredo_ele_diz_e_sai_verde(capsys, monkeypatch):
    monkeypatch.delenv("YT_OAUTH_JSON", raising=False)
    assert medir.main() == 0
    assert "sem YT_OAUTH_JSON" in capsys.readouterr().out


def test_os_ids_dos_canais_sao_os_da_frota():
    assert medir.CANAIS == {
        "labtreinamento": "UCtv_ewwSmwdi1ZRALW4_azg",
        "epomeno-epipedo": "UC1hk4k4QMjbPCfbw-S5xDyQ",
        "kolejny-poziom": "UCGe6sYpjzKyCC_K22ae1anw",
    }


def test_o_workflow_passa_o_segredo_e_so_ele():
    yml = (RAIZ / ".github/workflows/medir.yml").read_text()
    assert "YT_OAUTH_JSON: ${{ secrets.YT_OAUTH_JSON }}" in yml
    assert "python3 fabrica/medir.py" in yml
    assert "SUPABASE" not in yml, "medir sem banco e o ponto desta rota"


del os
