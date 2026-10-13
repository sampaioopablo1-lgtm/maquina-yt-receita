"""O corpus anti-duplicata atrasado, ancorado nas SETE pecas reais que escaparam.

Este arquivo existe porque eu deixei de registrar titulo publicado por SETE
rodadas seguidas (s020 a s026, de 18:19 de 12/10 a 00:15 de 13/10) e nada
reclamou: nenhum portao le o corpus contra o que esta no ar, e corpus atrasado
falha no sentido PERMISSIVO -- deixa passar titulo repetido em vez de barrar.

Os titulos aqui sao os `titulo=` dos notices reais do `retomar.yml`, nao
exemplos. Dois deles travam erros MEUS desta mesma rodada:
  * o corpus guarda o TITULO SHORT, nao o `## TITULO` longo -- eu grepei a forma
    longa, achei zero em dezessete pecas e quase relatei que o corpus "parou de
    crescer quando a publicacao mudou para o retomar.yml";
  * a linha com `youtube_id=?` e de run abortado e NAO pode entrar no corpus.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import corpus_atrasado as CA  # noqa: E402


# Os notices REAIS, copiados das anotacoes dos runs do `retomar.yml`.
NOTICES = """
PUBLICADO epomeno-epipedo-s017  youtube_id=? titulo=
PUBLICADO labtreinamento-s019 shorts youtube_id=oAAxm8VzjOc titulo=Qual porta chega antes? em=2026-10-12T17:13:09Z
PUBLICADO labtreinamento-s020 shorts youtube_id=JMCd5A3EkAk titulo=O meio-termo tem dono em=2026-10-12T18:19:43Z
PUBLICADO labtreinamento-s026 shorts youtube_id=CdUiplaeP5g titulo=Mude uma coisa so no seu preco em=2026-10-13T00:15:47Z
"""

SETE_QUE_ESCAPARAM = [
    "O meio-termo tem dono",
    "O maior trabalho do ano engana",
    "Desculpa de preço tem prazo",
    "Um é caso, três é padrão",
    "Quem já sabe está vendendo",
    "Não anotou? Dá para reconstruir",
    "Mude uma coisa só no seu preço",
]


def test_as_SETE_que_escaparam_estao_no_corpus_agora():
    # Se alguem reverter o conserto, ou publicar sem registrar de novo, isto cai.
    corpus = CA.carrega()
    falta = CA.faltantes(SETE_QUE_ESCAPARAM, corpus)
    assert falta == [], f"voltaram a faltar no corpus: {falta}"


def test_o_titulo_lido_e_o_SHORT_e_nao_o_TITULO_longo():
    # O erro que eu cometi em 13/10: grepar `## TITULO` em vez de
    # `## TITULO SHORT`. O corpus guarda o que o YouTube recebe.
    import re
    caminho = os.path.join(os.path.dirname(__file__), "..", "fabrica",
                           "specs", "labtreinamento-s026.json")
    with open(caminho, encoding="utf-8") as f:
        copy = json.load(f)["copy"]
    curto = re.search(r"## TITULO SHORT\n(.+)", copy).group(1).strip()
    longo = re.search(r"## TITULO\n(.+)", copy).group(1).strip()
    corpus = set(CA.carrega())
    assert curto in corpus, "o TITULO SHORT tem de estar no corpus"
    assert longo not in corpus, (
        "o `## TITULO` longo NAO e o que o corpus guarda — se ele comecar a "
        "aparecer, a forma mudou e o `faltantes` passa a mentir")


def test_notice_de_run_ABORTADO_nao_entra():
    # `youtube_id=?` com titulo vazio e run que morreu antes de subir. Registrar
    # titulo de peca que nao esta no ar poluiria a trava nos dois sentidos.
    lidos = CA.titulos_dos_notices(NOTICES)
    assert all(yid != "?" for _, yid, _ in lidos)
    assert all(t for _, _, t in lidos)
    assert [p for p, _, _ in lidos] == [
        "labtreinamento-s019", "labtreinamento-s020", "labtreinamento-s026"]


def test_titulo_com_espaco_e_lido_INTEIRO_ate_o_em():
    lidos = dict((p, t) for p, _, t in CA.titulos_dos_notices(NOTICES))
    assert lidos["labtreinamento-s020"] == "O meio-termo tem dono"
    assert lidos["labtreinamento-s026"] == "Mude uma coisa so no seu preco"


def test_faltantes_nao_repete_o_mesmo_titulo_duas_vezes():
    r = CA.faltantes(["Novo A", "Novo A", "Novo B"], corpus=["Velho"])
    assert r == ["Novo A", "Novo B"]


def test_faltantes_ignora_diferenca_de_espaco_em_branco():
    # "titulo   com  espaco" e "titulo com espaco" sao o MESMO titulo publicado;
    # tratar como dois registraria duplicata no proprio corpus.
    assert CA.faltantes(["  O meio-termo   tem dono "],
                        corpus=["O meio-termo tem dono"]) == []


def test_aplicar_em_corpus_JA_EM_DIA_nao_mexe_no_arquivo(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"titulos": ["A", "B"]}, ensure_ascii=False),
                 encoding="utf-8")
    antes = p.read_text(encoding="utf-8")
    assert CA.aplicar(["A", "B"], str(p)) == 0
    assert p.read_text(encoding="utf-8") == antes


def test_aplicar_acrescenta_no_FIM_e_preserva_a_ordem_existente(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"titulos": ["A", "B"]}, ensure_ascii=False),
                 encoding="utf-8")
    assert CA.aplicar(["C", "A", "D"], str(p)) == 2
    assert json.loads(p.read_text(encoding="utf-8"))["titulos"] == [
        "A", "B", "C", "D"]


def test_o_relato_DIZ_que_a_falha_e_permissiva():
    # O relato tem de explicar POR QUE isto importa, senao a proxima rodada
    # le "atrasado em 7" e trata como cosmetico.
    texto = CA.relato(["Titulo que nao existe no corpus"], corpus=["X"])
    assert "ATRASADO em 1" in texto
    assert "permissiva" in texto
    assert "COMITE" in texto


def test_corpus_em_dia_sai_como_em_dia():
    assert "em dia" in CA.relato(["X"], corpus=["X"])
