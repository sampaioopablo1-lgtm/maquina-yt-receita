"""O cron mandava renderizar o que ja estava no ar.

Medido em 17/08/2026. Cada disparo levava seis pacotes e CINCO deles ja tinham
video publicado: renderizavam doze minutos cada e abortavam na trava do
`publicar.py`. Um pacote util por rodada, e o resto de Actions queimado.

A causa e a mesma que a trava do publicar.py ja tinha resolvido do outro lado:
`videos.pacote` guarda o nome da RODADA que publicou
(nivel-do-jogo-cron-2026-08-13), nao o nome da spec (nivel-do-jogo-002).
Perguntar so pelo pacote devolve "nunca publicado", que e verdade sobre o nome
e mentira sobre o video.
"""

import json
import os
import sys
import types

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import orquestra as O  # noqa: E402


SPEC_COM_TITULO = {
    "slug": "nivel-do-jogo",
    "copy": ("# bilhete interno\n\n## TITULO\nLei Felca nos Games: R$ 333 Milhões\n\n"
             "## DESCRICAO\ntexto\n\n## CAPITULOS\n{CAPITULOS}\n"),
}


def test_titulo_sai_da_spec_mesmo_com_placeholder():
    """O caso que me enganou primeiro: tentei por `publicar.ler_copy` e ele
    recusa qualquer copy com {CAPITULOS} — que e o estado NORMAL de uma spec
    antes do render. A funcao devolvia vazio para todas, e a trava nao barrava
    nada."""
    assert O.titulo_da_spec(SPEC_COM_TITULO) == "Lei Felca nos Games: R$ 333 Milhões"


def test_titulo_aceita_copy_em_dict():
    assert O.titulo_da_spec({"copy": {"titulo": "X"}}) == "X"


@pytest.mark.parametrize("copy", [None, "", "sem secao nenhuma", 42])
def test_spec_sem_titulo_nao_explode(copy):
    assert O.titulo_da_spec({"copy": copy}) == ""


# --- as duas perguntas -------------------------------------------------------

def test_pega_pelo_titulo_quando_o_pacote_tem_outro_nome():
    """O nucleo do defeito, explicito."""
    por_pacote = {"nivel-do-jogo-cron-2026-08-13"}      # o que o banco guarda
    por_titulo = {"lei felca nos games: r$ 333 milhões"}
    motivo = O.ja_no_ar("nivel-do-jogo-002", SPEC_COM_TITULO, por_pacote, por_titulo)
    assert motivo
    assert "titulo" in motivo


def test_a_pergunta_pelo_pacote_sozinha_teria_liberado():
    """Ela nao esta com defeito; responde outra pergunta."""
    assert "nivel-do-jogo-002" not in {"nivel-do-jogo-cron-2026-08-13"}


def test_pega_pelo_pacote_quando_o_nome_bate():
    assert O.ja_no_ar("x-002", {"copy": ""}, {"x-002"}, set())


def test_spec_inedita_passa():
    assert O.ja_no_ar("x-009", SPEC_COM_TITULO, {"outro"}, {"outro titulo"}) == ""


def test_compara_titulo_ignorando_caixa_e_espaco():
    sp = {"copy": "# b\n\n## TITULO\n  LEI FELCA NOS GAMES: R$ 333 MILHÕES  \n"}
    assert O.ja_no_ar("z-002", sp, set(), {"lei felca nos games: r$ 333 milhões"})


# --- canal que nao existe ----------------------------------------------------

def test_canal_sem_destino_no_youtube_sai_da_matriz(tmp_path):
    """O cocina-por-niveles renderizava doze minutos desde 05/08 sem ter onde
    publicar. `None` desliga a conferencia, que e o que o teste sem rede usa."""
    videos = []
    esc, desc = O.proximo(videos, 10, com_destino=set())
    assert esc == []
    assert any("nao existe no YouTube" in d["motivo"] for d in desc)


def test_sem_conjunto_de_destino_a_conferencia_fica_desligada():
    """Passar None tem de manter o comportamento antigo, senao todo teste que
    nao conhece os canais passa a receber matriz vazia por engano."""
    _, desc = O.proximo([], 10, com_destino=None)
    assert not any("nao existe no YouTube" in d["motivo"] for d in desc)


# --- a coluna que faz tudo funcionar -----------------------------------------

def test_a_busca_traz_o_titulo():
    """Sem `titulo` no select, `titulos_no_ar` devolve conjunto vazio e a trava
    por titulo nao barra nada — o defeito voltaria calado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "orquestra.py"), encoding="utf-8").read()
    trecho = fonte.split("def busca_videos")[1].split("def ")[0]
    assert "titulo" in trecho.split("select=")[1].split('"')[0]


def test_titulos_no_ar_ignora_linha_sem_youtube_id():
    videos = [{"titulo": "no ar", "youtube_id": "abc"},
              {"titulo": "so renderizado", "youtube_id": None},
              {"titulo": None, "youtube_id": "def"}]
    assert O.titulos_no_ar(videos) == {"no ar"}


# --- os limites do workflow --------------------------------------------------

def _yaml(nome):
    return open(os.path.join(RAIZ, ".github", "workflows", nome),
                encoding="utf-8").read()


def test_o_job_tem_teto_curto_de_tempo():
    """120 min era o teto do render e virou o tempo que um job PENDURADO segura
    a frota. Tres vezes em 17/08/2026 um job ficou preso em `Instalar ffmpeg`
    — passo de 40 s — por 45 a 100 minutos, e os disparos seguintes se
    cancelavam na fila. Nenhum render legitimo passa de 15 min."""
    linha = [l for l in _yaml("frota.yml").splitlines()
             if l.strip().startswith("timeout-minutes:")]
    assert linha, "frota.yml sem timeout-minutes"
    assert int(linha[0].split(":")[1]) <= 30


def test_o_cron_espera_mais_que_um_run():
    """A cada 15 min o disparo chegava antes de o anterior terminar; o
    `concurrency` deixa 1 rodando e 1 pendente, e o terceiro cancela o
    pendente."""
    crons = [l.split('"')[1] for l in _yaml("diario.yml").splitlines()
             if "- cron:" in l]
    assert crons
    for c in crons:
        minuto = c.split()[0]
        if minuto.startswith("*/"):
            assert int(minuto[2:]) >= 30, f"cron {c} dispara antes do run acabar"
