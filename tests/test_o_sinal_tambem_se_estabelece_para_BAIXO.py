"""O criterio do 770 era de UM LADO SO, e isso escondeu o primeiro residuo
NEGATIVO estabelecido da serie.

MEDIDO em 17/10 as 20:1x. O `epomeno-epipedo-s054` (`A4M3SLs8FEk`) previa 41,6 no
edge — provedor MEDIDO pela anotacao (zero avisos `NARRACAO PELO PIPER` no job
117492664194) — e saiu com **41** segundos reais. O `duracao_a_medir.relato`
imprimiu "sinal NAO estabelecido (770)", e eu ia relatar isso.

**Estava errado, e a conta e de duas linhas.** O YouTube arredonda PARA CIMA,
logo real `R` significa duracao verdadeira em `(R-1, R]`. Com R=41 isso e
`(40; 41]`, e a previsao de 41,6 esta ACIMA de todo o intervalo. O residuo
verdadeiro vive em `(-1,6; -0,6]`: estritamente NEGATIVO. O sinal esta
estabelecido — para baixo.

O criterio escrito no 770 (`real - previsao > 1,0`) estabelece so o lado
POSITIVO, porque foi escrito quando todos os pontos eram positivos. Ele nao
tinha o outro ramo, e um criterio sem o ramo que falta **devolve "nao sei" onde a
aritmetica sabe**.

E a consequencia maior e documental: **a frase "N de N acima", que eu venho
escrevendo desde o 734, CAIU.** Nao e mais verdade que todos os pontos estao
acima da previsao do provedor que narrou. O que sobrevive e que a grande maioria
esta, e que o piso da banda passou a ser NEGATIVO (-0,6) pela primeira vez em 78
pontos.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fabrica"))

import duracao_a_medir as dm
import mira


# O ponto real que forcou a correcao.
PREV, REAL = 41.6, 41


def test_o_ponto_real_tem_sinal_NEGATIVO_estabelecido():
    assert dm._sinal(REAL, PREV) == -1


def test_o_criterio_antigo_de_um_lado_so_NAO_pegaria_este_ponto():
    # Contraprova: a regra antiga, escrita aqui de proposito, cala neste ponto.
    antigo = (REAL - PREV) > 1.0
    assert antigo is False
    assert dm._sinal(REAL, PREV) != 0, (
        "a aritmetica do arredondamento estabelece o sinal; o criterio antigo nao"
    )


def test_o_lado_POSITIVO_continua_exigindo_mais_de_um_segundo():
    # O que o 770 estabeleceu NAO foi afrouxado: real 42 contra previsao 41,6
    # segue sem sinal, porque (41; 42] contem 41,6.
    assert dm._sinal(42, 41.6) == 0
    # E 27 contra 25,2 segue estabelecido e positivo.
    assert dm._sinal(27, 25.2) == 1


def test_a_fronteira_dos_dois_lados():
    # Exatamente zero: o intervalo (prev-1, prev] encosta em zero pelo teto, e o
    # residuo pode ser zero — logo NAO esta estabelecido.
    assert dm._sinal(41, 41.0) == 0
    # RETRATADO em 18/10 as 15:2x, e a retratacao fica AQUI porque foi aqui que
    # eu afirmei: eu escrevi que `d == 1,0` tambem nao estabelece, pelo motivo
    # "o piso do intervalo encosta em zero". **Encostar nao e conter.** O
    # intervalo e `(0; 1]`, ABERTO embaixo, logo cada valor dele e estritamente
    # positivo e o sinal ESTA estabelecido. Ver
    # `tests/test_o_criterio_do_sinal_perdia_a_BORDA.py`.
    assert dm._sinal(42, 41.0) == 1
    # E logo ABAIXO da borda segue indecidivel: (-0,1; +0,9] contem zero.
    assert dm._sinal(42, 41.1) == 0
    # Um decimo abaixo de zero ja estabelece.
    assert dm._sinal(41, 41.1) == -1


def test_ausencia_de_leitura_nao_tem_sinal():
    assert dm._sinal(None, 41.6) == 0


def test_o_relato_DIZ_que_o_ponto_e_negativo_em_vez_de_calar():
    linhas = dm.residuos({"A4M3SLs8FEk": REAL})
    alvo = [l for l in linhas if l["youtube_id"] == "A4M3SLs8FEk"]
    if not alvo:   # o parque e um log vivo; se a peca saiu dele, o resto basta
        return
    l = alvo[0]
    assert l["sinal"] == -1 and l["estabelecido"] is True
    texto = dm.relato({"A4M3SLs8FEk": REAL})
    assert "NEGATIVO" in texto, "relato que cala sobre o sinal perde o achado"


def test_o_PISO_da_banda_ficou_negativo():
    lo, hi = mira.RESIDUO_OBSERVADO
    assert lo < 0, (
        "o piso da banda tem de refletir o ponto negativo observado; se alguem o"
        " devolveu para zero, o ponto do `epomeno-epipedo-s054` foi apagado"
    )
    assert lo <= -0.6
    assert hi >= 4.0


def test_a_QUEDA_da_frase_N_DE_N_ACIMA_fica_registrada_no_modulo():
    """A primeira versao deste teste era MINHA e estava errada: ela proibia a
    STRING "N de N acima" no modulo, e a string esta lá — citada como HISTORIA
    RETRATADA, duas vezes, que e exatamente o que a §10 manda fazer ("retrate no
    mesmo lugar onde afirmou"). Um teste que proibe a mencao proibe tambem a
    retratacao, e aí o proximo a ler o arquivo nao descobre que a frase caiu.

    A propriedade certa nao e a ausencia da frase: e a presenca da QUEDA ao lado
    dela, junto do ponto que a derrubou."""
    fonte = (pathlib.Path(__file__).resolve().parents[1]
             / "fabrica" / "mira.py").read_text()
    assert "N de N acima" in fonte, "a frase historica some e ninguem sabe que caiu"
    assert "derruba a frase" in fonte, "mencao sem retratacao vira afirmacao viva"
    # E o ponto que a derrubou vai NOMEADO, para que a queda seja verificavel.
    assert "A4M3SLs8FEk" in fonte
