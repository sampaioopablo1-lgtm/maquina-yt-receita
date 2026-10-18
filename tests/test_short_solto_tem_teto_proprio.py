"""O short solto tem teto PROPRIO no orquestrador — 18/10/2026.

O teto de pacote (1/dia) contava o short solto como pacote, logo o caminho
automatico ficava em UMA peca por canal por dia, contra o alvo escrito no
proprio comentario do teto ("7 shorts/dia por canal com um longo/dia") e o
pedido do dono (16/10: ao menos 2/dia/canal, 1 longo e 1 curto; 18/10: 100%
automatico). Agora os dois formatos tem tetos separados e contados separados.
"""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, "fabrica")
import orquestra as M  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]
AGORA = dt.datetime(2026, 10, 18, 12, 0, tzinfo=dt.timezone.utc)
HA_1H = (AGORA - dt.timedelta(hours=1)).isoformat()


def _v(canal, pacote, slug, formato):
    return {"canal": canal, "pacote": pacote, "slug": slug, "formato": formato,
            "status": "publicado", "criado_em": HA_1H}


def test_short_solto_e_longo_PRESENTE_e_vazio__chave_ausente_nao_e():
    assert M.e_short_solto({"longo": [], "short": [{}]})
    assert not M.e_short_solto({"longo": [{"nar": "x"}], "short": [{}]})
    assert not M.e_short_solto({"short": [{}]}), "chave ausente nao e lista vazia (KeyError de 18/10)"


def test_os_dois_tetos_sao_separados_e_o_de_short_e_o_7_do_dono():
    assert M.teto_short_solto("labtreinamento") == 7
    assert M.teto_do_canal("labtreinamento") == 1
    assert M.teto_short_solto("labtreinamento") > M.teto_do_canal("labtreinamento")


def test_shorts_soltos_na_janela_conta_so_pacote_SEM_longo():
    videos = [
        _v("c", "c-s001", "c-s001-short", "shorts"),          # solto
        _v("c", "c-s002", "c-s002-short", "shorts"),          # solto
        _v("c", "c-010", "c-010", "longo"),                   # pacote
        _v("c", "c-010", "c-010-short", "shorts"),            # mesmo pacote
        _v("d", "d-s001", "d-s001-short", "shorts"),
    ]
    assert M.shorts_soltos_na_janela(videos, agora=AGORA) == {"c": 2, "d": 1}
    assert M.pacotes_na_janela(videos, agora=AGORA) == {"c": 3, "d": 1}
    # o de pacote e a DIFERENCA, como o proximo() calcula
    assert M.pacotes_na_janela(videos, agora=AGORA)["c"] - M.shorts_soltos_na_janela(videos, agora=AGORA)["c"] == 1


def test_fora_da_janela_e_erro_nao_contam():
    antigo = dict(_v("c", "c-s001", "c-s001-short", "shorts"), criado_em="2026-10-01T00:00:00Z")
    erro = dict(_v("c", "c-s002", "c-s002-short", "shorts"), status="erro")
    assert M.shorts_soltos_na_janela([antigo, erro], agora=AGORA) == {}


def test_o_proximo_usa_os_dois_tetos_e_semeia_os_soltos():
    fonte = (RAIZ / "fabrica/orquestra.py").read_text()
    i = fonte.index("def proximo(")
    corpo = fonte[i:fonte.index("# ------------------------------------------------------------------ relatorio")]
    assert "shorts_soltos_na_janela(videos)" in corpo
    assert "teto_short_solto(canal)" in corpo and "teto_do_canal(canal)" in corpo
    assert "soltos_hoje[canal] = soltos_hoje.get(canal, 0) + 1" in corpo


def test_a_condicao_de_parada_esta_escrita_junto_do_teto():
    fonte = (RAIZ / "fabrica/orquestra.py").read_text()
    i = fonte.index("MAX_SHORTS_SOLTOS_POR_DIA_POR_CANAL = 7")
    bloco = fonte[max(0, i - 2500):i]
    assert "CONDICAO DE PARADA" in bloco and "zere" in bloco.lower()
