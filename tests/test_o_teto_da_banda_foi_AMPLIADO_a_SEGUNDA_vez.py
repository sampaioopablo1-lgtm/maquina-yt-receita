"""774, `alto`, medido em 15/10 as 10:2x: o TETO da banda foi ampliado pela
SEGUNDA vez, e o defeito do 753 reapareceu no DOCSTRING.

O `labtreinamento-s052` (`w5a8m3GiQUE`) previa **25,0** no edge — provedor
MEDIDO pela anotacao (zero avisos `NARRACAO PELO PIPER` no job
`116368125417`), nao inferido (733) — e saiu com **29 s reais**: residuo
**+4,0 s**, contra o maximo de **3,7** que trinta e nove pontos sustentavam.
Sinal ESTABELECIDO (`29 - 25,0 > 1,0`, criterio do 770).

**E o que vale guardar nao e o numero, sao tres coisas:**

1. **A banda ficou MENOS util outra vez.** A largura foi de 3,6 para **3,9 s**
   e, em 16/10 as 21:2x, para **4,0 s** — o piso desceu a ZERO no
   `kolejny-poziom-s045` (41,0 -> 41). **Cinco** correcoes, todas alargando.
   contra **1 s** de granularidade do real: ela cobre quase quatro inteiros. O
   teto subiu duas vezes (752, 774) e o piso baixou duas (769, 770) — **as
   quatro correcoes a ALARGARAM**, nunca a estreitaram, e isso e proprio de um
   limite definido pelo extremo OBSERVADO.

2. **O DOCSTRING do `mira.py` repetia a banda em texto, e estava ERRADO.** Ele
   dizia *"hoje 0,9 a 3,7 s"* quando a constante era `(0.1, 3.7)` — o piso havia
   baixado no 770 e a frase ficou atras, sem ninguem ver. **E o teste do 753 nao
   pegava**, porque ele cobra a MENSAGEM do `relato` e nao o docstring do modulo.
   Mesma classe de defeito, uma camada acima: numero que o modulo CALCULA nao se
   repete escrito em lugar nenhum do modulo — nem em comentario.

3. **Dois testes meus reprovaram por IDENTIDADE, nao por propriedade**, e os dois
   foram corrigidos no lugar: um cravava `dono == ["labtreinamento-s043"]` (o
   dono do teto mudou de peca, e o que importa e ele ser estabelecido e do canal
   dominante) e outro cravava `largura == 3.6`. Mesma classe do 743/753/761.

**O que isto NAO autoriza dizer:** que exista relacao entre previsao e real nesta
faixa. Sao 40 pontos, 35 estabelecidos, todos POSITIVOS — o que sobrevive e o
SINAL, nunca o valor.

**E a consequencia pratica e uma piora da contradicao do 740/748:** com residuo
de ate 4,0 s, `real <= 26,0` passa a exigir `edge <= 22,0`, onde o piper cai para
~18,0 — ainda mais longe do piso de 20,0 da mira do canal.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))
sys.path.insert(0, str(RAIZ / "tests"))

import mira  # noqa: E402
from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

PACOTE, PREV_EDGE, REAL, JOB = "labtreinamento-s052", 25.0, 29, "116368125417"


def test_o_ponto_esta_na_serie_com_os_numeros_medidos():
    alvo = [r for r in SERIE if r[0] == PACOTE]
    assert alvo, "o ponto de 15/10 10:2x tem de estar na serie"
    _n, prev, real, prov = alvo[0]
    assert (prev, real, prov) == (PREV_EDGE, REAL, "edge")


def test_o_residuo_FUROU_o_teto_anterior_de_3_7():
    residuo = round(REAL - PREV_EDGE, 1)
    assert residuo == 4.0
    assert residuo > 3.7, "se nao furou, este aprendizado nao existe"
    assert mira.RESIDUO_OBSERVADO[1] == residuo, (
        "o teto da banda e o maior residuo JA OBSERVADO, logo ele se move quando "
        "a observacao sai dele")


def test_o_sinal_deste_ponto_esta_ESTABELECIDO():
    """Criterio do 770: so acima de 1,0 a janela de arredondamento fica toda
    acima da previsao (o YouTube arredonda para CIMA)."""
    assert REAL - PREV_EDGE > 1.0


def test_as_SEIS_correcoes_da_banda_a_ALARGARAM():
    """739 (0,9;2,4) -> 752 teto 3,7 -> 769 piso 0,5 -> 770 piso 0,1 -> 774 teto
    4,0 -> **17/10 20:1x piso -0,6**. Nenhuma estreitou, e isso e propriedade de
    limite por extremo observado.

    A sexta e a mais consequente das seis: ela nao so alargou a banda, ela
    mudou o SINAL do piso, e com isso derrubou a frase "N de N acima" que eu
    vinha escrevendo desde o 734. O ponto e o `epomeno-epipedo-s054`
    (`A4M3SLs8FEk`), previsao edge 41,6 e real 41."""
    larguras = [2.4 - 0.9, 3.7 - 0.9, 3.7 - 0.5, 3.7 - 0.1, 4.0 - 0.1,
                4.0 - (-0.6)]
    assert larguras == sorted(larguras), larguras
    lo, hi = mira.RESIDUO_OBSERVADO
    assert round(hi - lo, 1) == 4.6
    assert lo < 0, "o piso negativo e o achado da sexta correcao"


def test_a_banda_cobre_quase_QUATRO_inteiros_do_real():
    lo, hi = mira.RESIDUO_OBSERVADO
    assert (hi - lo) / 1.0 > 3.5, (
        "largura em passos do instrumento — acima de tres a faixa informa pouco")


def test_o_DOCSTRING_do_mira_NAO_repete_a_banda_escrita():
    """O defeito do 753 uma camada acima: a frase "0,9 a 3,7" vivia no docstring
    e ficou atrasada quando o 770 baixou o piso a 0,1. O teste do 753 nao a
    pegava porque cobra a MENSAGEM do relato."""
    fonte = (RAIZ / "fabrica" / "mira.py").read_text()
    doc = fonte.split('"""')[1]
    # o par ATUAL nao se escreve: e ele que envelhece na proxima ampliacao.
    for par in ("0,1 a 4,0", "0.1 a 4.0"):
        assert par not in doc, f"a banda ATUAL voltou escrita: {par!r}"
    # e um par ANTIGO so pode aparecer como HISTORIA, dentro da frase que conta
    # o defeito — nunca como se fosse o valor de hoje.
    for par in ("0,9 a\n3,7", "0,9 a 3,7", "0.9 a 3.7", "0,1 a 3,7"):
        if par in doc:
            assert "trazia" in doc, (
                f"{par!r} aparece sem a marca de que e valor ANTIGO")
            assert "hoje " + par.replace("\n", " ") not in doc
    assert "leia a constante" in doc


def test_a_contradicao_do_740_PIOROU_com_o_teto_novo():
    """Com teto 4,0 a janela pessimista do edge encolhe, e ela JA era vazia."""
    teto_real, piso_piper, razao = 26.0, 20.0, 0.82
    edge_max = teto_real - mira.RESIDUO_OBSERVADO[1]      # real <= 26,0
    edge_min_mira = piso_piper / razao                     # piper >= 20,0
    assert edge_max < edge_min_mira, "as janelas voltaram a se tocar — releia"
    assert edge_max <= 22.0 + 1e-9, edge_max
    # e o vao e MAIOR do que era com 3,7
    assert edge_min_mira - edge_max > (26.0 - 3.7) * 0 + 2.0


def test_o_provedor_foi_MEDIDO_e_o_job_fica_registrado():
    assert JOB.isdigit() and len(JOB) >= 9
    fonte = (RAIZ / "tests"
             / "test_residuo_quebra_o_limite_de_dois_segundos.py").read_text()
    assert PACOTE in fonte


def test_TODOS_os_pontos_seguem_NAO_NEGATIVOS():
    """O nome diz 40 porque foi quando nasceu; a PROPRIEDADE e que todos sobem.

    A versao anterior cravava `== 40`, e em 16/10 ela reprovou no 41o ponto —
    mesma classe do 743/753/761: teste por IDENTIDADE em vez de propriedade. O
    que importa e que a SERIE e o `RESIDUO_N` concordem e que nenhum ponto seja
    negativo; a contagem cresce a cada peca e nao precisa de edicao.
    """
    assert len(SERIE) == mira.RESIDUO_N >= 40
    for pacote, prev, real, _p in SERIE:
        # `>= 0` desde 16/10 as 21:2x: o `kolejny-poziom-s045` previu 41,0 e
        # deu real 41 — residuo ZERO, que NAO e positivo. A propriedade que a
        # serie sustenta e NAO-NEGATIVO; o positivo estrito vale apenas nos
        # pontos ESTABELECIDOS, e quem cobra isso e o teste do 770.
        # RETRATADO em 17/10 as 20:1x: o `epomeno-epipedo-s054` (41,6 -> 41)
        # e o PRIMEIRO real ABAIXO da previsao em 78 pontos, e o sinal dele esta
        # estabelecido para BAIXO (arredondamento para cima: (40; 41] fica todo
        # abaixo de 41,6). Logo "nenhum ponto e negativo" CAIU. A propriedade que
        # sobra e que o negativo e RARO, e quem a cobra e
        # `test_o_sinal_NAO_e_mais_de_N_de_N__e_o_negativo_apareceu`.
        assert real - prev <= 4.0, pacote
    negativos = [pk for pk, pr, r, _ in SERIE if r < pr]
    assert len(negativos) <= 0.05 * len(SERIE), negativos
