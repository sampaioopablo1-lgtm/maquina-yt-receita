"""O portao que faltava: a narracao inteira na lingua da voz.

Existe por um caso com nome. Escrevi o `blocos_006` comecando em indonesio e
derrapando para portugues a partir do capitulo 2, e os seis portoes passaram
limpos — a docstring do proprio arquivo registra o diagnostico: "o linter de
narracao nao pega troca de idioma, so o autor pega".

Estes testes trancam as duas pontas que um detector de lingua pode errar, e
elas puxam para lados opostos:

  * acusar texto correto (o corpus inteiro tem que passar), e
  * deixar passar texto virado (a derrapagem tem que doer).

Afrouxar um lado conserta o outro, entao os dois moram no mesmo arquivo.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import idioma as I  # noqa: E402

SPECS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))
COM_LONGO = [p for p in SPECS
             if json.loads(p.read_text(encoding="utf-8")).get("longo")]


def _spec(nome):
    return json.loads((RAIZ / "fabrica" / "specs" / f"{nome}.json")
                      .read_text(encoding="utf-8"))


# --------------------------------------------------------------- as listas

def test_nenhuma_palavra_funcional_serve_a_duas_linguas():
    """Palavra em duas listas empata, e empate vira acusacao.

    Nao e hipotese: a primeira versao deste portao acusou a cena 45 da
    sx-educacao-001 — portugues corrente — de parecer espanhol, porque `ser`,
    `cada` e `por` estavam nas listas das duas.
    """
    colisoes = {}
    for a, b in itertools.combinations(I.FUNCIONAIS, 2):
        comum = I.FUNCIONAIS[a] & I.FUNCIONAIS[b]
        if comum:
            colisoes[f"{a}/{b}"] = sorted(comum)
    assert not colisoes, colisoes


def test_toda_voz_do_portfolio_tem_perfil_de_idioma():
    """Voz sem perfil e spec que o portao nao consegue julgar."""
    from ensaio import MODELO_VOZ

    sem = [v for v in MODELO_VOZ
           if I._base("-".join(v.split("-")[:2])) not in
           (set(I.FUNCIONAIS) | set(I.ESCRITAS))]
    assert not sem, sem


# ------------------------------------------------- nao acusar o que esta certo

@pytest.mark.parametrize("spec", COM_LONGO, ids=lambda p: p.stem)
def test_nenhuma_spec_do_repositorio_e_acusada(spec):
    """O corpus inteiro e monolingue e tem que passar.

    Este e o teste que segura a mao: qualquer aperto de limiar que aumente a
    deteccao as custas de acusar texto bom morre aqui.
    """
    assert not I.analisa(json.loads(spec.read_text(encoding="utf-8")))


def test_o_idioma_sai_da_voz_e_nao_do_campo_idioma():
    """A voz e o que o TTS usa. Uma spec marcada pt-BR que renderiza com
    id-ID-Gadis sai em indonesio, e e a voz que manda."""
    assert I.idioma_da_spec({"voz": "id-ID-GadisNeural", "idioma": "pt-BR"}) == "id"
    assert I.idioma_da_spec({"voz": "pt-BR-ThalitaMultilingualNeural"}) == "pt"


def test_cena_curta_nao_e_acusada():
    """Kicker e CTA curtos nao tem evidencia, e acusar ali seria ruido."""
    assert I.analisa_cena("Excel, dados e decisao.", "id") is None


# ----------------------------------------------- doer quando o texto e virado

def test_o_caso_que_aconteceu_de_verdade():
    """A derrapagem do blocos_006: indonesio ate o capitulo um, portugues do
    dois em diante. Reconstruida com cenas REAIS das duas specs."""
    virada = dict(_spec("setiap-level-006"))
    virada["longo"] = (_spec("setiap-level-006")["longo"][:20]
                       + _spec("sx-educacao-001")["longo"][:30])
    assert I.analisa(virada)


def test_um_capitulo_virado_doi():
    """Oito cenas — um capitulo — e o menor trecho que a rotina produz de uma
    vez, porque o roteiro se escreve por bloco."""
    virada = dict(_spec("setiap-level-006"))
    virada["longo"] = (_spec("setiap-level-006")["longo"][:20]
                       + _spec("sx-educacao-001")["longo"][:8])
    assert I.analisa(virada)


def test_uma_frase_rica_em_palavra_de_funcao_e_pega_sozinha():
    motivo = I.analisa_cena(
        "O problema nao e o valor da parcela. Voce ja sabe quanto paga por mes, "
        "e isso nunca foi o que estava escondido de voce.", "id")
    assert motivo and "parece pt" in motivo


def test_escrita_errada_e_erro_imediato():
    """Grego e devanagari se separam por codepoint. Isso e certeza, nao
    estimativa, e nao depende de nenhuma lista de palavras."""
    grego = _spec("epomeno-epipedo-002")["longo"][3]["nar"]
    assert I.analisa_cena(grego, "en")
    assert I.analisa_cena("This is plain English with enough words here.", "el")


def test_nome_proprio_em_outra_escrita_nao_reprova_a_cena():
    """Uma palavra grega citada num roteiro em ingles e citacao, nao troca de
    lingua. O portao exige escrita PREDOMINANTE."""
    assert I.analisa_cena(
        "The Greek word for household is οἶκος, and that is where the word "
        "economy actually comes from.", "en") is None


def test_o_short_tambem_passa_pelo_portao():
    """O short e o formato que entrega — 25 a 96x o longo do mesmo pacote.
    Deixa-lo de fora seria proteger o que rende menos."""
    virada = dict(_spec("setiap-level-006"))
    virada["short"] = _spec("sx-educacao-001")["short"]
    faltas = I.analisa(virada)
    assert any(f.startswith("short") for f in faltas), faltas


VOZ_DE = {"pt": "pt-BR-AntonioNeural", "es": "es-MX-DaliaNeural",
          "en": "en-US-AndrewNeural", "id": "id-ID-GadisNeural",
          "pl": "pl-PL-MarekNeural", "tr": "tr-TR-AhmetNeural",
          "el": "el-GR-NestorasNeural", "hi": "hi-IN-MadhurNeural"}


def _uma_spec_por_lingua():
    por = {}
    for p in COM_LONGO:
        sp = json.loads(p.read_text(encoding="utf-8"))
        if len(sp["longo"]) >= 30:
            por.setdefault(I.idioma_da_spec(sp), sp)
    return por


@pytest.mark.parametrize("real,declarada",
                         [(a, b) for a in VOZ_DE for b in VOZ_DE])
def test_matriz_de_idiomas(real, declarada):
    """Cada roteiro real declarado como CADA lingua do portfolio.

    A prova mais forte que este portao consegue dar: na diagonal ele tem que
    ficar calado, e fora dela tem que doer. Sao as duas pontas de uma vez, e
    qualquer lista que fique parecida demais com outra quebra aqui — foi assim
    que as colisoes pt/es apareceram.
    """
    por = _uma_spec_por_lingua()
    if real not in por:
        pytest.skip(f"sem spec longa em {real}")
    sp = dict(por[real])
    sp["voz"] = VOZ_DE[declarada]
    faltas = I.analisa(sp)
    if real == declarada:
        assert not faltas, faltas[:3]
    else:
        assert faltas, f"{real} passou como {declarada}"
