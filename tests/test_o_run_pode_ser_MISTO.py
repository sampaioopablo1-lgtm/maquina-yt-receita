"""O run pode ser MISTO — e ai o residuo nao pertence a mundo nenhum.

Aprendizado de 16/10 as 11:3x, medido na anotacao do job `116943785023`
(`labtreinamento-s060`): a contagem de avisos `NARRACAO PELO PIPER` voltou
**DOIS**, nao zero e nao dez. Duas cenas pelo Piper, oito pelo edge.

POR QUE ISSO IMPORTA, e e mais que curiosidade: o `fabrica.py:598-620` tenta o
`edge_tts` TRES vezes POR CENA e cai no Piper na terceira falha — logo o
provedor sempre pôde ser misto, e o 730/733 ja dizia "por cena e por run". Mas
em todos os pontos que eu medi ate aqui a contagem veio 0 (dez de dez cenas no
edge) ou 10 (dez no Piper), e **eu passei a tratar a contagem como um
INTERRUPTOR de duas posicoes**. Era amostra, nao propriedade.

A CONSEQUENCIA PARA A BANDA: um run misto nao tem mundo de provedor. Nem
`duracao_real_prevista(..., 'edge')` nem `...'piper'` descreve a peca, porque a
duracao real e a SOMA de cenas narradas por provedores diferentes — e a razao
piper/edge (~0,82) nao se aplica a parte nenhuma inteira. Logo o ponto **NAO
ENTRA** na `SERIE` do 739 como ponto de edge, que seria o que eu faria por
habito, lendo "dois avisos" como "quase zero".

O que este teste trava: que a leitura do provedor e uma CONTAGEM com tres
regimes (todo edge, todo Piper, MISTO), e que o terceiro existe medido.
"""
import pathlib
import sys

sys.path.insert(0, "fabrica")

RAIZ = pathlib.Path(__file__).resolve().parents[1]

# A contagem real do job `116943785023`, e as duas que eu vinha tratando como as
# unicas possiveis. `cenas` e dez em todas as tres (esqueleto de dez cenas).
MEDIDOS = [
    ("labtreinamento-s059", 0, 10),   # job 116878234290: todo edge
    ("kolejny-poziom-s023", 10, 10),  # job do 733: todo Piper
    ("labtreinamento-s060", 2, 10),   # job 116943785023: MISTO, 16/10 11:3x
]


def _regime(avisos: int, cenas: int) -> str:
    if avisos == 0:
        return "edge"
    if avisos == cenas:
        return "piper"
    return "misto"


def test_o_regime_MISTO_existe_medido():
    regimes = {n: _regime(a, c) for n, a, c in MEDIDOS}
    assert regimes["labtreinamento-s060"] == "misto", regimes
    assert "misto" in regimes.values()


def test_os_tres_regimes_sao_possiveis_e_distintos():
    assert {_regime(a, c) for _, a, c in MEDIDOS} == {"edge", "piper", "misto"}


def test_misto_NAO_tem_mundo_de_provedor():
    """A regra que sai do achado: ponto misto nao entra na serie do residuo."""
    from test_residuo_quebra_o_limite_de_dois_segundos import SERIE

    mistos = {n for n, a, c in MEDIDOS if _regime(a, c) == "misto"}
    na_serie = {n for n, *_ in SERIE} & mistos
    assert not na_serie, (
        "ponto de run MISTO entrou na serie do residuo: nem o mundo edge nem o"
        f" piper descreve a duracao dele. {na_serie}"
    )


def test_a_contagem_NAO_e_um_interruptor():
    """Travado porque o habito era ler a contagem como booleano.

    Se alguem reescrever a leitura como `avisos == 0`, este teste continua
    passando — por isso ele cobra a FORMA da contagem, nao o codigo: existe
    valor medido que nao e nem zero nem o total.
    """
    assert any(0 < a < c for _, a, c in MEDIDOS)


def test_o_aviso_do_piper_nomeia_a_voz_e_a_descalibracao():
    """A anotacao real diz a voz e manda remedir — e isso e o que a torna util."""
    aviso = (
        "NARRACAO PELO PIPER (fallback) na voz pt-BR-ThalitaMultilingualNeural:"
        " o R e o P de MODELO_VOZ sao do edge-tts e NAO valem para esta voz."
    )
    assert "NARRACAO PELO PIPER" in aviso
    assert "pt-BR-ThalitaMultilingualNeural" in aviso
    assert "NAO valem" in aviso


def test_o_emissor_do_aviso_continua_sendo_warning():
    """Se virar `print`, o provedor volta a ser inferido no olho (733)."""
    fonte = (RAIZ / "fabrica" / "voz_piper.py").read_text(encoding="utf-8")
    assert "::warning::" in fonte, (
        "o aviso do Piper deixou de sair pelas ANOTACOES do job, e sem ele o"
        " regime do run deixa de ser observavel"
    )
