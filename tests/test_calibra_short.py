"""As constantes de short tem de continuar batendo com a medida.

`ensaio.VIES_SHORT` e `prontidao.MARGEM_SHORT` sao numeros CALCULADOS a partir
de `fabrica/medidas_short.tsv`, nao escolhidos. Antes de 20/08/2026 eles eram
escolhidos — MARGEM_SHORT subiu quatro vezes em dois dias, cada vez para cobrir
o pior caso recem-observado, o que nao converge. Este teste existe para que a
constante nao volte a andar sozinha: quem editar uma sem rodar
`calibra_short.py` quebra aqui.
"""
import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import calibra_short  # noqa: E402
import ensaio  # noqa: E402
import prontidao  # noqa: E402


@pytest.fixture(scope="module")
def r():
    return calibra_short.resumo()


def test_vies_short_e_o_que_a_medida_diz(r):
    """Tolerancia de meio ponto: arredondar 1,0472 para 1,047 e legitimo,
    trocar por 1,00 'porque parecia melhor' nao e."""
    assert ensaio.VIES_SHORT == pytest.approx(r["vies"], abs=0.005), (
        f"VIES_SHORT={ensaio.VIES_SHORT} mas medidas_short.tsv diz "
        f"{r['vies']:.3f}. Rode `python3 fabrica/calibra_short.py`.")


def test_margem_short_e_o_percentil_95_do_residuo(r):
    assert prontidao.MARGEM_SHORT == pytest.approx(
        r["residuo_p95_pct"] / 100, abs=0.005), (
        f"MARGEM_SHORT={prontidao.MARGEM_SHORT} mas o residuo p95 medido e "
        f"{r['residuo_p95_pct']/100:.3f}. Rode "
        f"`python3 fabrica/calibra_short.py`.")


def test_a_amostra_nao_encolheu(r):
    """Trinta medidas foi o que tirou a constante do chute. Se alguem apagar
    linhas do TSV, o percentil 95 volta a ser ruido e ninguem percebe."""
    assert r["n"] >= 30, f"so {r['n']} medidas validas — o TSV encolheu?"


def test_o_vies_e_vies_e_nao_ruido(r):
    """A justificativa inteira de VIES_SHORT existir e esta assimetria. No dia
    em que ela sumir — porque a esteira mudou, ou a voz — a correcao tem de ser
    revista, nao mantida por inercia."""
    assert r["positivos"] >= 0.8 * r["n"], (
        f"so {r['positivos']} de {r['n']} erram para cima. A assimetria que "
        f"justifica corrigir a previsao pode ter acabado — remeça a analise "
        f"em vez de manter a constante.")


def test_medida_com_spec_alterada_depois_nao_calibra():
    """A regra que salvou o diagnostico: os tres shorts esticados em 13/08
    apareciam como erro de -20%, e nao havia erro nenhum — o arquivo de hoje
    nao era o texto lido."""
    descartadas = [m for m in calibra_short.medidas() if not m["vale"]]
    assert descartadas, "nenhuma descartada — a regra de validade sumiu?"
    for m in descartadas:
        assert m["alterada_em"] > m["publicado_em"]


def test_short_corrigido_e_maior_que_o_cru():
    cenas = [{"nar": "Uma frase. Outra frase."}] * 5
    voz = "id-ID-GadisNeural"
    assert (ensaio.duracao_estimada_short(cenas, voz)
            > ensaio.duracao_estimada(cenas, voz))


def test_o_teto_do_portao_e_sobre_a_previsao():
    """`SHORT_MAX_S / (1 + margem)`, nunca `SHORT_MAX_S * (1 - margem)`.

    A segunda forma tambem 'da um numero menor que 45' e por isso passou meses
    sem ser notada, mas ela responde a outra pergunta. Um short previsto NO
    teto, errando exatamente a margem, tem de cair em cima de 45 s — nao antes.
    """
    teto = prontidao.SHORT_MAX_S / (1 + prontidao.MARGEM_SHORT)
    assert teto * (1 + prontidao.MARGEM_SHORT) == pytest.approx(
        prontidao.SHORT_MAX_S)
