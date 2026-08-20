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
#
# O inventario tem DOIS tipos de parada, e confundi-los foi um defeito real
# deste teste ate 19/08/2026. "portao" e spec que reprova num portao barato —
# se voltar a passar, tem de sair daqui, e e isso que o assert protege.
# "sem portao" e spec que passa em tudo e mesmo assim nao deve ser disparada,
# por um motivo que portao nenhum enxerga. Exigir falha de portao das duas
# obrigava a inventar defeito para justificar parada legitima.
PARADAS = {
    # Passa nos portoes e continua parada: o canal NAO EXISTE no YouTube
    # (canais.no_youtube = false e config.yt_token_cocina-por-niveles com
    # refresh_token nulo, conferidos em 19/08/2026). Renderizar quinze minutos
    # aqui e renderizar para o vazio. Encurtar o roteiro nao resolveria nada.
    #
    # Ela entrou aqui por outro motivo — "15,0 min, acima do teto" — que a
    # recalibracao de 19/08/2026 dissolveu: com o Dalia medido cena-a-cena
    # (17,20 -> 17,48 chars/s) a spec passou a prever 14,95 min. So que 14,95
    # contra teto de 15,00 e margem de 3 s, menor que o erro tipico do proprio
    # modelo (0,75% de 897 s = 6,7 s). Passar no portao por menos que a barra
    # de erro nao e passar.
    # Virou "portao" em 20/08/2026, sem que a spec mudasse uma linha: a quarta
    # medida de short (resep-naik-level-005, +6,6%) levou MARGEM_SHORT de 3%
    # para 5%, o teto previsto caiu de 43,6 para 42,8 s, e o short desta spec
    # mede 43,0. O motivo PRINCIPAL de ela estar parada continua sendo outro e
    # continua valendo — ver abaixo. O tipo mudou porque agora existe portao
    # que a segura, e o teste cobra que os dois batam.
    "cocina-por-niveles-002": ("portao",
                               "canal nao existe no YouTube (motivo principal, "
                               "que portao nenhum enxerga); alem disso short de "
                               "43,0 s contra teto de 42,8, e longo de 14,95 min "
                               "contra teto de 15,00 — margem menor que o erro "
                               "do proprio modelo"),
    # kolejny-poziom-003 saiu daqui em 18/08/2026: 88 cenas viraram 79
    # (16,6 -> 13,0 min no Marek) e a copy-bilhete virou markdown completo.
    # Os limites de 2026 do roteiro foram reconferidos antes (28.260 /
    # 11.304 / 16.956 zl — Analizy.pl, BDO e PZU batem).
    # labtreinamento-002 saiu daqui em 18/08/2026: encurtada de 92 para 87
    # cenas (15,33 -> 14,49 min) e devolvida a matriz.
    # resep-naik-level-003 saiu em 18/08/2026: encurtada de 86 para 76 cenas
    # (16,20 -> 14,32 min) e devolvida a matriz.
    # As tres abaixo entraram juntas em 20/08/2026, pelo MESMO motivo e sem que
    # nenhuma delas mudasse uma linha: a quarta medida de short
    # (resep-naik-level-005, previsto 37,8 s e real 40,3 s, +6,6%) levou a
    # mediana do erro para +4,8% e MARGEM_SHORT de 3% para 5%. O teto previsto
    # caiu de 43,6 para 42,8 s e elas ficaram do lado de fora por dois decimos.
    #
    # Nenhuma perdeu nada com isso: as TRES ja estao no ar, publicadas antes da
    # margem subir, e o orquestrador descarta pacote com youtube_id de qualquer
    # forma. Elas entram aqui porque o inventario mede spec contra portao, nao
    # contra o banco — e uma spec que sai da matriz sem registro e exatamente o
    # defeito que este teste existe para pegar. Se um dia forem reaproveitadas,
    # o corte e de uma frase no short.
    "labtreinamento-003":     ("portao", "short 43,4 s contra teto de 42,8 (MARGEM_SHORT 5%); ja no ar"),
    "seviye-seviye-003":      ("portao", "short 43,4 s contra teto de 42,8 (MARGEM_SHORT 5%); ja no ar"),
    "sx-educacao-002":        ("portao", "short 43,6 s contra teto de 42,8 (MARGEM_SHORT 5%); ja no ar"),
    "setiap-level-003":       ("portao", "26,0 min — desescalonado por medicao em 17/08"),
    "setiap-level-004":       ("portao", "28,1 min — desescalonado por medicao em 17/08"),
    "setiap-level-006":       ("portao", "copy ainda em bilhete"),
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
        tipo, motivo = PARADAS[spec.stem]
        if tipo == "portao":
            assert faltas, (f"{spec.stem} voltou a passar nos portoes — tire do "
                            f"inventario PARADAS, o motivo registrado era: "
                            f"{motivo}")
        else:
            assert not faltas, (
                f"{spec.stem} esta no inventario como parada SEM portao, mas "
                f"reprova em portao barato. Ou o motivo mudou, ou o tipo esta "
                f"errado:\n  " + "\n  ".join(faltas))
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
