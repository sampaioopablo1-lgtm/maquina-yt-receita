"""Acento faltando nao reprova em portao nenhum — e muda a pronuncia.

Descoberto em 20/08/2026 escrevendo a seviye-seviye-004: escrevi as 72 cenas em
ASCII num canal cujas outras duas specs acentuam 12,7% das letras. Turco sem
acento continua parecendo turco, entao passou no portao de idioma; ASCII sempre
tem fonte, entao passou no de glifos; e chegou ao TTS, que pronuncia outra
coisa — "acacagim" nao e "acacagim", "sozlesme" nao e "sozlesme".

A varredura achou mais tres casos JA NO AR: kolejny-poziom-003 e -004 em
polones, e seja-mais-magra-004 em portugues, publicada nesta mesma manha.
"""
from __future__ import annotations

import json
import os
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao as P  # noqa: E402

SPECS = RAIZ / "fabrica" / "specs"


def _sem_acento(texto: str) -> str:
    base = "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")
    # o `i` sem ponto e o `g` mole do turco, e o `l` cortado polones, nao sao
    # combinacoes: NFD nao os separa, e sem isto o teste nao simula ASCII real
    return base.replace("ı", "i").replace("ğ", "g").replace("ł", "l")


def _carrega(nome):
    return json.loads((SPECS / f"{nome}.json").read_text(encoding="utf-8"))


def test_o_caso_que_criou_o_portao():
    """seviye-seviye-004 com acento passa; a mesma spec em ASCII reprova."""
    sp = _carrega("seviye-seviye-004")
    caminho = str(SPECS / "seviye-seviye-004.json")
    assert P._gate_ortografia(caminho, sp) == []

    sem = json.loads(json.dumps(sp))
    for c in sem["longo"]:
        c["nar"] = _sem_acento(c["nar"])
    faltas = P._gate_ortografia(caminho, sem)
    assert faltas and "0.0%" in faltas[0] and "12.7%" in faltas[0]


def test_o_portao_compara_com_o_canal_e_nao_com_uma_regra_fixa():
    """Ele NAO afirma que toda lingua precisa de acento — o corpus nao sustenta
    isso: varias specs em portugues nunca acentuaram. Ele afirma que uma spec
    nao pode divergir do PROPRIO canal."""
    sp = _carrega("seviye-seviye-004")
    sp = json.loads(json.dumps(sp))
    sp["slug"] = "canal-sem-vizinhas"
    assert P._gate_ortografia(str(SPECS / "canal-sem-vizinhas-001.json"), sp) == []


def test_lingua_sem_diacritico_nao_e_avaliada():
    """Indonesio e ingles nao tem acento; o portao precisa se calar neles."""
    for nome in ("setiap-level-009", "next-level-money-004"):
        sp = _carrega(nome)
        assert P._gate_ortografia(str(SPECS / f"{nome}.json"), sp) == []


def test_escrita_nao_latina__a_RAZAO_deste_teste_era_FALSA_para_o_GREGO():
    """RETRATADO em 19/10 as 22:4x, e a razao caiu nos DOIS casos que citava.

    O teste dizia: *"Grego e devanagari ja sao pegos pelo portao de idioma — la
    a falta de acento nem existe, o alfabeto inteiro seria outro."* **Medido, o
    portao `idioma` NAO pega nenhum dos dois:**

        narracao grega sem tonos   -> `_gate_idioma` LIMPO
          "O enas minas kryvei tin trimini kai tin etisia pliromi."
          (letras gregas sem tonos seguem sendo letras gregas)
        devanagari sem as marcas Mn -> `_gate_idioma` LIMPO
          "aaiteeaar kee taareekh nikal gaee, par raasata bad nahee haa."
          (virama e anusvara caem, a palavra vira outra, e o script continua
           devanagari)

    Logo a assercao era IDENTIDADE (`"el" not in DIACRITICOS`) onde a afirmacao
    era PROPRIEDADE (*"o portao de idioma pega"*) — a classe 743/753/761.

    **O `el` ENTROU em 19/10 as 22:3x, com a conta antes:** as 87 specs gregas
    de short medem 11,34% a 15,36% e ZERO fica abaixo do `PISO_REFERENCIA`,
    logo a entrada reprova a peca quebrada e nenhuma do acervo. E ela fechou um
    buraco real: a descricao grega do `epomeno-epipedo-s068` subiu sem tonos em
    19/10 as 15:3x e quem pegou fui eu relendo.

    **O `hi` FICA DE FORA, e agora pela razao MEDIDA e nao pela falsa:** as
    marcas de vogal do devanagari sao em boa parte `Mc` (espacejantes), nao
    `Mn`, logo "quanto esta spec acentua" e outra pergunta naquele script — e eu
    **nao medi** o acervo `hi` contra um piso. Entrar sem essa medicao seria
    ligar portao que pode reprovar o parque, que e o argumento do `mira.py`.
    """
    assert "el" in P.DIACRITICOS, (
        "o `el` saiu da tabela: o portao volta a CALAR no segundo maior idioma "
        "da frota, e foi assim que o grego ficou descoberto de 20/08 a 19/10"
    )
    assert "hi" not in P.DIACRITICOS, (
        "o `hi` entrou sem a medicao do acervo contra o piso — meca primeiro"
    )


def test_o_que_esta_na_TABELA_nao_reprova_o_acervo():
    """A propriedade que a razao antiga tentava proteger, cobrada de verdade.

    Entrar na tabela e autorizado pela conta: a densidade das specs daquele
    idioma tem de ficar ACIMA do piso, senao o portao passa a reprovar o parque.
    """
    import collections
    import glob

    por_idioma = collections.defaultdict(list)
    for caminho in glob.glob(str(SPECS / "*.json")):
        try:
            with open(caminho, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        base = (sp.get("idioma") or "").split("-")[0]
        tabela = P.DIACRITICOS.get(base)
        if not tabela or not sp.get("short"):
            continue
        d = P._densidade_diacritica(sp["short"], tabela)
        if d is not None and P._letras(sp["short"]) >= P.MINIMO_LETRAS_MEDIDAS:
            por_idioma[base].append((os.path.basename(caminho), d))

    assert por_idioma, "nenhuma spec medivel — este teste passa por vacuidade"
    for base, vals in sorted(por_idioma.items()):
        abaixo = [(n, round(d * 100, 2)) for n, d in vals
                  if d < P.PISO_REFERENCIA]
        # o acervo de `pt` e `pl` tem specs da fase ASCII, e elas sao a DIVIDA
        # conhecida das 25 falhas; o que este teste cobra e que um idioma NOVO
        # na tabela nao traga parque abaixo do piso junto com ele.
        if base in ("pt", "pl", "tr", "es"):
            continue
        assert not abaixo, (
            f"`{base}` esta na tabela e tem spec do acervo abaixo do piso: "
            f"{abaixo[:6]} — a entrada dele passou a reprovar o parque"
        )


def test_o_portao_esta_na_lista():
    """Escrever o portao e nao liga-lo e a forma silenciosa de nao ter portao."""
    assert "ortografia" in dict(P.PORTOES)


def test_a_folga_e_larga_de_proposito():
    """Metade da referencia: o alvo e ASCII puro, nao flutuacao normal de
    texto. Uma spec com 8% num canal de 12,7% nao pode reprovar."""
    sp = _carrega("seviye-seviye-004")
    d = P._densidade_diacritica(sp["longo"], P.DIACRITICOS["tr"])
    assert d > 0.10
    # simula uma spec com dois tercos do acento: tem de passar
    parcial = json.loads(json.dumps(sp))
    for i, c in enumerate(parcial["longo"]):
        if i % 3 == 0:
            c["nar"] = _sem_acento(c["nar"])
    assert P._gate_ortografia(str(SPECS / "seviye-seviye-004.json"), parcial) == []
