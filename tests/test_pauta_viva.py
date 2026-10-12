"""A pauta viva conta longo DA MAQUINA. Contar acervo alheio ja aconteceu.

Historia inteira, 12/10/2026, e sao DOIS erros meus em sequencia:

  1. com o banco em 402 eu reconstrui pauta do retrato `fabrica/ponte/videos.json`
     (06/10). Escrevi a ressalva certa — "longo publicado depois nao aparece, o
     numero SUBESTIMA" — e dai tratei o numero como estoque por tres rodadas,
     anunciando "a pauta acabou". O `medir.py` ja lia a playlist de UPLOADS pela
     API, viva, sem banco;
  2. o modulo novo, na PRIMEIRA execucao (run 38228176339), devolveu **65
     "origens livres" no labtreinamento** — e eram os VIDEOS DE CURSO DO DONO:
     "1.Seja bem-vindo", "2. Backstage", "Transmissao ao vivo de LabTreinamento".
     E o aprendizado 668 na forma de pauta: aquele canal tem acervo anterior a
     maquina. Sem filtro, a maquina escreveria short derivado de aula de
     Microsoft Project.

O conserto e o corpus como filtro, e estes testes ancoram nos SEIS casos reais
daquele run — tres longos da maquina que DEVEM passar e tres videos do dono que
NAO podem passar.
"""

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import pauta_viva as PV  # noqa: E402

# Titulos REAIS lidos no run 38228176339.
DA_MAQUINA = [
    "Μισθός 920€, Καθαρά 772€: Πού Πάνε τα 148€ σου το 2026;",
    "Το σύστημα 6 μηνών για να μηδενίσεις τα χρέη σου με μισθό 900€",
    "Emerytura z ZUS: 34,4% pensji w 2050 roku. Ile musisz odłożyć sam?",
]
ACERVO_DO_DONO = [
    "1.Seja bem-vindo",
    "2. Backstage",
    "Transmissão ao vivo de LabTreinamento",
]


def test_o_corpus_separa_maquina_de_acervo_nos_SEIS_casos_reais():
    """A ancora. Se ela cair, os testes abaixo nao medem mais nada."""
    m = PV.titulos_da_maquina()
    for t in DA_MAQUINA:
        assert t in m, f"longo da maquina fora do corpus: {t!r}"
    for t in ACERVO_DO_DONO:
        assert t not in m, (
            f"video do acervo do dono ENTROU no corpus: {t!r} — o filtro deixou "
            f"de separar e a pauta volta a contar aula de curso")


def test_acervo_anterior_a_maquina_NAO_entra_como_origem():
    """Era 65 origens falsas no labtreinamento (run 38228176339)."""
    itens = {
        "aaaaaaaaaaa": {"status": {"uploadStatus": "processed"},
                        "contentDetails": {"duration": "PT12M0S"},
                        "snippet": {"title": "1.Seja bem-vindo"}},
        "bbbbbbbbbbb": {"status": {"uploadStatus": "processed"},
                        "contentDetails": {"duration": "PT12M0S"},
                        "snippet": {"title": DA_MAQUINA[0]}},
    }
    passou = _filtra(itens, set(DA_MAQUINA))
    assert list(passou) == ["bbbbbbbbbbb"], passou


def _filtra(itens, da_maquina):
    """Reproduz o corpo do laco de `longos_no_ar` sem tocar a rede."""
    fora = {}
    for vid, it in itens.items():
        st = (it.get("status") or {}).get("uploadStatus")
        dur = PV.segundos((it.get("contentDetails") or {}).get("duration"))
        if st != "processed" or not dur or dur < PV.SEG_MIN_LONGO:
            continue
        titulo = ((it.get("snippet") or {}).get("title") or "").strip()
        if da_maquina is not None and titulo not in da_maquina:
            continue
        fora[vid] = titulo
    return fora


def test__filtra_reproduz_o_modulo_e_nao_uma_regra_inventada():
    """Se o modulo mudar e este helper nao, os testes mentem."""
    fonte = (RAIZ / "fabrica/pauta_viva.py").read_text()
    for pedaco in ('st != "processed"', "dur < PV.SEG_MIN_LONGO".replace("PV.", ""),
                   "titulo not in da_maquina"):
        assert pedaco in fonte, pedaco


def test_peca_fora_de_processed_nao_e_origem():
    """665: ela pode nem ficar no ar."""
    itens = {"x": {"status": {"uploadStatus": "uploaded"},
                   "contentDetails": {"duration": "PT12M0S"},
                   "snippet": {"title": DA_MAQUINA[0]}}}
    assert _filtra(itens, set(DA_MAQUINA)) == {}


def test_P0D_nao_e_origem_mesmo_com_titulo_certo():
    itens = {"x": {"status": {"uploadStatus": "processed"},
                   "contentDetails": {"duration": "P0D"},
                   "snippet": {"title": DA_MAQUINA[0]}}}
    assert _filtra(itens, set(DA_MAQUINA)) == {}


def test_short_nao_e_origem():
    itens = {"x": {"status": {"uploadStatus": "processed"},
                   "contentDetails": {"duration": "PT41S"},
                   "snippet": {"title": DA_MAQUINA[0]}}}
    assert _filtra(itens, set(DA_MAQUINA)) == {}


def test_o_limiar_longo_short_erra_para_o_lado_que_PRESERVA_pauta():
    """Classificar longo como short perde pauta; o contrario so adiciona ruido."""
    assert PV.SEG_MIN_LONGO > 43.1, "tem de ficar acima do teto do portao duracao"
    assert PV.SEG_MIN_LONGO <= 300, (
        "limiar alto demais descartaria longo curto de verdade")


def test_duracao_e_lida_do_contentDetails_e_nao_do_nome_do_pacote():
    for iso, esperado in (("PT12M31S", 751), ("PT1H2M3S", 3723),
                          ("PT41S", 41), ("P0D", None), ("PT0S", None),
                          (None, None), ("lixo", None)):
        assert PV.segundos(iso) == esperado, iso


def test_grupo_com_QUALQUER_copia_usada_sai_inteiro():
    por_canal = {"c": {"a": ("T", 0), "b": ("T", 0), "z": ("OUTRO", 0)}}
    assert PV.livres(por_canal, {"b"})["c"] == [("OUTRO", ["z"])]


def test_corpus_sem_titulos_PARA_em_vez_de_contar_acervo_alheio(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"titulos": []}))
    with pytest.raises(SystemExit):
        PV.titulos_da_maquina(str(p))


def test_nao_imprime_segredo():
    fonte = (RAIZ / "fabrica/pauta_viva.py").read_text()
    assert "refresh_token" not in fonte.replace(
        "refresh_token`", "").replace("client_secret, refresh_token", "")
    assert "print(mapa" not in fonte and "print(cfg" not in fonte


def test_o_workflow_passa_o_segredo_e_nada_mais():
    yml = (RAIZ / ".github/workflows/pauta-viva.yml").read_text()
    assert "YT_OAUTH_JSON: ${{ secrets.YT_OAUTH_JSON }}" in yml
    assert "pauta_viva.py" in yml


# ---------------------------------------------------------------------------
# A unidade de pauta e (longo, familia de capitulo) — nao o longo
# ---------------------------------------------------------------------------
def test_longo_com_UM_short_ainda_e_pauta():
    """Retrata "a pauta acabou" pela TERCEIRA vez no mesmo dia.

    Medido em 12/10: das 49 origens que as specs consomem, 48 foram usadas UMA
    vez e uma foi usada DUAS — `h04-UVlVevs` rendeu `epomeno-epipedo-s002` e
    `-s006`, as duas PUBLICADAS, com entradas erradas diferentes (periodo errado
    numa, media-contra-marginal na outra).

    A regra (e) da rotina ja dizia isso em letra: "a entrada errada vem do
    capitulo que o short ORIGINAL nao usou" pressupoe que o mesmo longo rende
    mais de um short. Eu tratava cada longo como uso UNICO por HABITO.
    """
    r = {"c": {"eZ697VNYCPU": ("usada uma vez", 0),
               "zzzzzzzzzzz": ("nunca usada", 0)}}
    d = PV.por_uso(r, set())["c"]
    assert [t for t, _ in d["um_short"]] == ["usada uma vez"]
    assert [t for t, _ in d["sem_short"]] == ["nunca usada"]


def test_o_PRECEDENTE_de_dois_shorts_do_mesmo_longo_existe_e_esta_no_ar():
    """A ancora. Se ela cair, o teste acima nao se apoia em nada real."""
    import glob
    usos = []
    for p in glob.glob(str(RAIZ / "fabrica/specs/*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            continue
        if sp.get("longo_existente") == "h04-UVlVevs":
            usos.append(Path(p).stem)
    assert len(usos) >= 2, (
        f"o precedente de dois shorts do mesmo longo desapareceu ({usos}) — "
        f"reveja este teste em vez de afrouxa-lo")
    corpus = set(json.load(open(RAIZ / "fabrica/corpus_publicados.json",
                                encoding="utf-8"))["titulos"])
    for nome in usos:
        sp = json.load(open(RAIZ / "fabrica/specs" / f"{nome}.json",
                            encoding="utf-8"))
        curto = sp["copy"].split("## TITULO SHORT\n")[1].split("\n")[0]
        assert curto in corpus, (
            f"{nome} nao esta no corpus — o precedente nao foi publicado, "
            f"entao nao prova nada")


def test_origem_usada_DUAS_vezes_sai_dos_dois_baldes():
    """Nao e "livre" nem "segundo angulo": ja teve dois angulos."""
    r = {"c": {"h04-UVlVevs": ("usada duas", 0)}}
    d = PV.por_uso(r, set())["c"]
    assert d["um_short"] == [] and d["sem_short"] == []


def test_grupo_de_copias_conta_UMA_vez_e_nao_somado():
    """Dez copias do mesmo titulo com um short nao sao dez segundos angulos."""
    r = {"c": {"eZ697VNYCPU": ("T", 0), "copia_irma": ("T", 0)}}
    d = PV.por_uso(r, set())["c"]
    assert len(d["um_short"]) == 1 and d["um_short"][0][1] == ["copia_irma",
                                                              "eZ697VNYCPU"]


def test_o_relato_do_vivo_DIZ_que_o_segundo_angulo_nao_e_automatico():
    fonte = (RAIZ / "fabrica/pauta_viva.py").read_text()
    assert "SEGUNDO ANGULO" in fonte
    assert "NAO e automatico" in fonte
    assert "similaridade" in fonte, (
        "o relato tem de lembrar que o segundo angulo passa pelo portao")
    assert "h04-UVlVevs" in fonte, "o precedente tem de estar nomeado"


# ===========================================================================
# RODAR SEM TOKEN NAO E DEFEITO, E A MENSAGEM NAO PODE DIZER QUE E (12/10)
#
# Medido na pele: rodei `pauta_viva.py` no container e recebi
# `::error::YT_OAUTH_JSON vazio`. Um `::error::` numa rodada que esta apenas no
# lugar errado fabrica o diagnostico "a maquina quebrou" — o mesmo efeito do
# §3.8 da rotina, em que o portao verde fabrica "esta tudo certo". A saida tem
# de dizer qual e a ROTA certa e qual e o PISO.
# ===========================================================================


def _sem_token(monkeypatch, capsys):
    import os
    monkeypatch.delenv("YT_OAUTH_JSON", raising=False)
    cod = PV.main()
    return cod, capsys.readouterr().out


def test_sem_token_nao_emite_error_de_workflow(monkeypatch, capsys):
    cod, saida = _sem_token(monkeypatch, capsys)
    assert cod == 2, "continua saindo diferente de zero: nao houve leitura"
    assert "::error::" not in saida, (
        "`::error::` aqui fabrica 'a maquina quebrou' quando o que houve foi "
        "rodar no lugar errado"
    )


def test_sem_token_diz_a_rota_e_o_piso(monkeypatch, capsys):
    _, saida = _sem_token(monkeypatch, capsys)
    assert "RUNNER" in saida, "tem de dizer ONDE este modulo roda"
    assert "pauta-viva.yml" in saida, "tem de nomear o workflow"
    assert "pauta_local.py" in saida, "tem de nomear o PISO"
    assert "segundo_angulo.py" in saida, (
        "capitulo intocado de longo ja usado nao precisa de token nenhum, e a "
        "rodada de 12/10 so achou isso porque eu me lembrei — a saida lembra"
    )


def test_sem_token_diz_que_o_piso_SUBESTIMA(monkeypatch, capsys):
    _, saida = _sem_token(monkeypatch, capsys)
    assert "SUBESTIMA" in saida, (
        "apontar o piso sem dizer que ele subestima reconstroi o erro de 12/10, "
        "em que eu tratei o retrato de 06/10 como estoque por tres rodadas e "
        "anunciei 'a pauta acabou'"
    )
