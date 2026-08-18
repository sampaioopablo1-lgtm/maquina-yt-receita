"""Erro duro de narracao nao reprova: some da matriz e ninguem ve.

Medido em 18/08/2026. A spec sx-educacao-002 passou nos 698 testes da suite e
mesmo assim o cron NAO a escolheria: `orquestra.proximo` roda os portoes de
`prontidao` por spec e descarta em silencio quem tem falta. Duas cenas tinham
quatro quantidades numa frase — a regra `MAX_NUM_FRASE`, "planilha falada".

O estrago tem a forma que este repositorio ja conhece de outros lugares: nada
fica vermelho. O disparo produz um pacote a menos, e a spec fica no diretorio
parecendo pronta. Se eu nao tivesse rodado `proximo` a mao antes de empurrar,
teria esperado o video de um pacote que nunca entraria na fila.

O teste roda os MESMOS quatro portoes que `orquestra._falhas_baratas` roda, e pela
mesma porta — nao uma reimplementacao deles. Duas armadilhas dessa porta,
porque as duas me custaram tempo hoje:

  * `narracao.analisa` devolve TRES coisas (erros, avisos, todas). Desempacotar
    duas levanta ValueError, e desempacotar so `erros` esconde os avisos.
  * o idioma que ela espera e a BASE ("pt"), nao a tag da spec ("pt-BR").
    `NUMEROS.get("pt-BR")` nao existe, a funcao cai no ramo que so conta
    digito, e um roteiro inteiro por extenso passa com zero numeros contados.
    Uma auditoria minha da suite inteira deu "0 specs com erro" por isso —
    estava certa por acidente, o que e pior do que errada.
"""

from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao  # noqa: E402
import orquestra as O  # noqa: E402

SPECS = [p for p in sorted((RAIZ / "fabrica" / "specs").glob("*.json"))
         if re.search(r"-\d{3}$", p.stem)
         and json.loads(p.read_text(encoding="utf-8")).get("longo")]


# As specs que HOJE nao entram na matriz, e o motivo de cada uma. Ficar de
# fora nao e sempre defeito: setiap-level-003 e -004 sao os 26 e 28 min que eu
# mesmo tirei do escalonamento em 17/08/2026, porque longos de 25 a 28 min
# rendiam 0,30 view/dia contra 91,25 da mediana do nicho. O que nao pode e
# alguem descobrir isso esperando um video que nunca vem.
PARADAS = {
    "cocina-por-niveles-002": "15,0 min — acima do teto, canal sem escalonamento",
    "kolejny-poziom-003":     "copy ainda em bilhete + 16,6 min",
    "labtreinamento-002":     "15,3 min — acima do teto",
    "resep-naik-level-003":   "16,2 min — acima do teto",
    "setiap-level-003":       "26,0 min — desescalonado por medicao em 17/08",
    "setiap-level-004":       "28,1 min — desescalonado por medicao em 17/08",
    "setiap-level-006":       "copy ainda em bilhete",
}


@pytest.mark.parametrize("spec", SPECS, ids=lambda p: p.stem)
def test_spec_de_producao_ou_entra_na_matriz_ou_esta_no_inventario(spec):
    """O defeito nao e ter spec parada — e ter spec parada que ninguem sabe.

    Uma spec nova que comeca a reprovar cai aqui em vez de sumir calada; uma
    spec parada de proposito fica no inventario acima, com o motivo escrito.
    """
    sp = json.loads(spec.read_text(encoding="utf-8"))
    faltas = O._falhas_baratas(spec.stem, sp)
    if spec.stem in PARADAS:
        assert faltas, (f"{spec.stem} voltou a passar nos portoes — tire do "
                        f"inventario PARADAS, o motivo registrado era: "
                        f"{PARADAS[spec.stem]}")
        return
    assert not faltas, (f"{spec.stem} sairia da matriz calada:\n  "
                        + "\n  ".join(faltas))


# --- a regra que pegou, explicita ------------------------------------------

def _erros(nar: str, idi: str = "pt") -> list[str]:
    return narracao.analisa({"longo": [{"nar": nar}]}, idi)[0]


def test_quatro_quantidades_numa_frase_e_erro_duro():
    """O caso real: salario nominal e adicional na mesma frase, cada um com
    reais E centavos, dao quatro grupos de numero."""
    erros = _erros("Sao nove mil quatrocentos e vinte e tres reais e trinta "
                   "centavos de salario nominal, mais mil duzentos e sessenta "
                   "e dois reais e catorze centavos de adicional.")
    assert any("planilha falada" in e for e in erros)


def test_a_mesma_conta_quebrada_em_duas_frases_passa():
    """A correcao nao e cortar o numero, e distribuir: um por frase."""
    assert not _erros("O salario nominal e nove mil quatrocentos e vinte e "
                      "tres reais. Em cima dele vem um adicional de atividade "
                      "de mil duzentos e sessenta e dois.")


def test_o_conector_nao_parte_a_quantidade():
    """"quarenta e dois" e UM numero, nao dois — senao qualquer frase com dois
    valores por extenso reprovaria e a regra viraria ruido."""
    assert narracao.conta_numeros("Sao quarenta e dois reais.", "pt") == 1


def test_a_tag_da_spec_nao_serve_como_idioma():
    """O motivo de este arquivo existir com esta forma. Passar "pt-BR" nao
    levanta erro: devolve zero e a regra fica desligada em silencio."""
    frase = ("Sao nove mil reais, mais mil duzentos reais, mais sete mil "
             "reais, mais dez mil reais.")
    assert narracao.conta_numeros(frase, "pt") >= 4
    assert narracao.conta_numeros(frase, "pt-BR") == 0
    assert narracao.idioma_de({"voz": "pt-BR-AntonioNeural"}, None) == "pt"


# --- o elo que faltava ------------------------------------------------------

def test_analisa_devolve_tres_coisas():
    """Desempacotar em duas levanta ValueError na hora de checar uma spec, que
    e exatamente quando ninguem quer descobrir a assinatura."""
    assert len(narracao.analisa({"longo": [{"nar": "Oi."}]}, "pt")) == 3


def test_a_matriz_consulta_os_portoes_mesmo():
    """Se um dia `proximo` parar de chamar `_falhas_baratas`, este arquivo deixa de
    proteger alguma coisa sem que nenhum teste caia."""
    fonte = (RAIZ / "fabrica" / "orquestra.py").read_text(encoding="utf-8")
    corpo = fonte.split("def proximo")[1].split("\ndef ")[0]
    assert "_falhas_baratas(" in corpo, "proximo nao roda mais os portoes por spec"
