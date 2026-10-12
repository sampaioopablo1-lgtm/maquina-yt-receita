"""O estado da ponte tem uma FORMA, e errar a forma custou uma publicacao.

Run `38217254505`, 12/10/2026: a publicacao do `kolejny-poziom-s018` morreu em
`AttributeError: 'str' object has no attribute 'get'` dentro de
`publicar._iguais_no_estado`, porque eu montei `titulos_no_ar` a mao como lista
de STRINGS e a trava por titulo le lista de OBJETOS. O passo de conferencia do
runner passou verde: ele contava o TAMANHO da lista, nao a forma dela.

O que estes testes travam:

  1. `monta` produz a forma que `publicar` LE DE VERDADE — conferido chamando a
     propria trava, nao reescrevendo o que eu acho que ela faz;
  2. `confere` RECUSA a forma exata que falhou em producao, e diz o numero do
     run;
  3. `confere` devolve TODOS os motivos, nao o primeiro;
  4. o `retomar.yml` CHAMA o `confere` — validador que a producao nao chama e
     validador decorativo, e foi assim que este defeito passou.

**O que NAO esta aqui de proposito:** nenhum teste pedindo que a trava TOLERE
lista de strings. Ela levantou e isso foi certo — estado malformado virando
"nenhum titulo no ar" publicaria duplicata calada, que e pior que traceback.
"""

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import estado_ponte as EP  # noqa: E402


def test_monta_produz_a_forma_que_a_PROPRIA_trava_sabe_ler():
    """Chamando `publicar._iguais_no_estado`, nao uma copia da regra dela."""
    publicar = pytest.importorskip("publicar")
    est = EP.monta()
    titulo = est["titulos_no_ar"][0]["titulo"]
    assert publicar._iguais_no_estado(est, titulo), (
        "o estado montado nao casa um titulo que esta nele — a trava nao "
        "barraria duplicata nenhuma")
    assert publicar._iguais_no_estado(est, "titulo que nao existe em 2026") == []


def test_a_forma_que_FALHOU_em_producao_e_recusada():
    """Lista de strings: exatamente o run 38217254505."""
    mau = {"ja_publicado": {}, "titulos_no_ar": ["um", "dois"],
           "titulos_no_ar_n": 2}
    ruins = EP.confere(mau)
    assert ruins, "a forma que derrubou a producao passaria de novo"
    assert any("38217254505" in r for r in ruins), (
        "o motivo tem de citar o run — quem ler o erro precisa achar o caso")


def test_a_forma_CERTA_passa():
    assert EP.confere(EP.monta()) == []


def test_lista_truncada_continua_recusada():
    est = EP.monta()
    est["titulos_no_ar"] = est["titulos_no_ar"][:5]
    assert any("TRUNCADO" in r for r in EP.confere(est))


def test_sem_o_n_declarado_recusa():
    est = EP.monta()
    del est["titulos_no_ar_n"]
    assert any("titulos_no_ar_n" in r for r in EP.confere(est))


def test_devolve_TODOS_os_motivos_e_nao_o_primeiro():
    """Quem monta o disparo corrige de uma vez, nao um por rodada."""
    mau = {"titulos_no_ar": ["um", "dois", "tres"]}          # sem n E strings
    ruins = EP.confere(mau)
    assert len(ruins) >= 2, ruins


def test_titulo_vazio_em_todas_as_entradas_e_recusado():
    """Trava comparando contra vazio nunca barra nada, e passaria verde."""
    assert any("nunca barraria" in r for r in
               EP.confere({"titulos_no_ar": [{"titulo": " "}],
                           "titulos_no_ar_n": 1}))


def test_o_retomar_yml_CHAMA_o_confere():
    """Validador que a producao nao chama e decoracao — foi o defeito."""
    yml = (RAIZ / ".github/workflows/retomar.yml").read_text()
    assert "from estado_ponte import confere" in yml
    assert "confere(d)" in yml
    # e a recusa tem de PARAR o job, nao so imprimir
    assert "estado invalido — nada foi baixado nem publicado" in yml


def test_o_motivo_da_falha_do_publicar_chega_as_ANOTACOES():
    """O log de job nao e legivel por API daqui; a anotacao e o canal."""
    yml = (RAIZ / ".github/workflows/retomar.yml").read_text()
    assert "::error::publicar.py saiu" in yml
    assert "PIPESTATUS" in yml, (
        "com `| tee` o `$?` e do tee: o codigo do publicar.py se perderia")


def test_o_youtube_id_do_que_foi_publicado_chega_as_ANOTACOES():
    """Sem isto, quem publica nao descobre o id — run 38217420591."""
    yml = (RAIZ / ".github/workflows/retomar.yml").read_text()
    assert "::notice::PUBLICADO" in yml
    assert "youtube_id=" in yml


def test_corpus_sem_a_lista_de_titulos_para_em_vez_de_seguir(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"titulos": []}))
    with pytest.raises(SystemExit):
        EP.monta(str(p))
