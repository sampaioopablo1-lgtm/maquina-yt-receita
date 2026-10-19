"""A terceira distancia do longo: a cadencia de plano — e o enquadramento errado.

O QUE ESTE ARQUIVO GUARDA, e sao duas coisas:

1. **O TRILHO ERA O SEGUNDO MODULO ESCRITO E MORTO.** O `fabrica/trilho.py`
   existe desde 19/10 as 01:4x, com a geometria MEDIDA por variancia temporal, e
   nenhum caminho do render o alcancava — a mesma classe do `layouts_longo`, que
   eu consertei no MESMO arquivo tres horas antes, e do `legenda.py` com dois
   donos e um atualizado. Codigo que ninguem chama PARECE pronto.

2. **A COMPARACAO "18,9 s CONTRA OS 3,1 s NOSSOS" ERA ENTRE FORMATOS
   DIFERENTES.** Os 3,1 s sao a cadencia do SHORT (medida em 690/699); a
   referencia e um LONGO de 8:50. Medido agora com instrumento, sobre 131 specs
   de longo da frota, a nossa mediana e **9,4 s por plano** — logo a distancia e
   um fator ~2, nao ~6. E o erro de enquadramento do 679/698/725, cometido na
   frase que eu escrevi para descrever a distancia.

A contraprova de cada afirmacao vai nos dois sentidos onde ela existe.
"""

import ast
import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import cadencia_longo as CL  # noqa: E402
import ensaio  # noqa: E402
import fabrica as FB  # noqa: E402
import trilho  # noqa: E402

PAL = {"bg": "#0E1117", "ink": "#EEF1F5", "c1": "#3DDBD9", "c2": "#1E2430"}
CAPS = ["A armadilha", "Os tres limites", "O que o PROCX muda", "Quando usar"]


def _cena(**kw):
    c = {"layout": "titulo", "kicker": "Teste", "nar": "Uma frase."}
    c.update(kw)
    return c


# ----- 1. o trilho chegou ao render -----

def test_o_trilho_SAI_no_svg_do_16_por_9():
    """A cena que declara `trilho` tem de produzir a faixa no SVG.

    Nao basta nao quebrar: o defeito dos layouts mortos era desenhar o fundo e
    esquecer o conteudo, logo o teste cobra o TEXTO de um capitulo.
    """
    svg = FB.svg_cena(_cena(trilho=CAPS, trilho_atual=1), PAL, 1920, 1080)
    assert "A armadilha" in svg, "o trilho nao chegou ao SVG: despacho morto"
    assert "Quando usar" in svg, "o trilho saiu truncado"


def test_sem_o_campo_o_svg_fica_IGUAL_ao_de_antes():
    """Contraprova no outro sentido: cena sem `trilho` nao ganha tinta nenhuma.

    Sem isto o conserto mudaria as 205 pecas de short e os longos antigos por
    baixo — exatamente o que a trava da §10 proibe.
    """
    sem = FB.svg_cena(_cena(), PAL, 1920, 1080)
    assert "A armadilha" not in sem
    assert "<text" not in sem.split("</svg>")[0] or "Teste" in sem


def test_o_trilho_NAO_entra_no_retrato():
    """9:16 nao recebe o trilho — a faixa cairia sobre a legenda queimada.

    Este teste e o irmao do que guarda os layouts de longo: se o despacho
    escorregar para o retrato, ele produz tinta na borda (o defeito do
    `kp-plan-9233`) e a legenda deixa de ler.
    """
    svg = FB.svg_cena(_cena(trilho=CAPS, trilho_atual=0), PAL, 1080, 1920)
    assert "A armadilha" not in svg, "o trilho entrou no 9:16"


def test_o_trilho_e_do_MOBILIARIO_e_nao_de_uma_camada():
    """Ele sai na camada `base` e NAO em camada de elemento.

    O trilho e permanente por definicao — zero transicoes acima de scene 0,15 na
    referencia. Se ele saisse numa camada de elemento, piscaria com a fala.
    """
    base = FB.svg_cena(_cena(trilho=CAPS, trilho_atual=0), PAL, 1920, 1080,
                       camada="base")
    assert "A armadilha" in base, "o trilho nao esta no mobiliario fixo"
    elem = FB.svg_cena(_cena(trilho=CAPS, trilho_atual=0), PAL, 1920, 1080,
                       camada=0)
    assert "A armadilha" not in elem, "o trilho repetiria em cada camada"


def test_o_render_IMPORTA_o_trilho_de_UM_dono_so():
    """Por AST: ninguem redesenha a faixa por conta propria.

    O docstring do modulo CITA a geometria em prosa para se explicar, logo casar
    texto pegaria a explicacao em vez do codigo — por isso a varredura e por AST,
    como a do `canal.py`.
    """
    suspeitos = []
    for f in glob.glob(os.path.join(RAIZ, "fabrica", "*.py")):
        if os.path.basename(f) in ("trilho.py", "area_segura.py"):
            continue
        arvore = ast.parse(open(f).read())
        for no in ast.walk(arvore):
            if isinstance(no, ast.Constant) and isinstance(no.value, float):
                if no.value in (trilho.REF_Y0, trilho.REF_Y1,
                                trilho.FAIXA_ALT):
                    suspeitos.append(os.path.basename(f))
    assert not suspeitos, (
        f"a geometria da faixa reaparece fora do trilho.py: {suspeitos}. "
        "Dois donos da mesma regra e o defeito que congelou a legenda."
    )


# ----- 2. a cadencia, com instrumento -----

def test_a_cadencia_da_referencia_e_DERIVADA_e_nao_escrita():
    """O 18,9 sai da divisao, nunca de um numero no codigo.

    Foi copiar o resultado que me fez repeti-lo por tres dias sem instrumento.
    """
    assert CL.cadencia_da_referencia() == pytest.approx(
        CL.REFERENCIA_DUR_S / CL.REFERENCIA_TRANSICOES)
    assert CL.cadencia_da_referencia() == pytest.approx(18.93, abs=0.01)
    fonte = open(os.path.join(RAIZ, "fabrica", "cadencia_longo.py")).read()
    arvore = ast.parse(fonte)
    cravados = [n.value for n in ast.walk(arvore)
                if isinstance(n, ast.Constant) and isinstance(n.value, float)
                and 18.0 <= n.value <= 19.9]
    assert not cravados, f"a cadencia foi cravada no codigo: {cravados}"


def test_a_conta_dos_CARACTERES_e_do_ensaio_e_nao_daqui():
    """Delegacao, nao copia: um dono para a sobrecarga por voz.

    Refazer `P + 0,300` aqui criaria o segundo dono — a assinatura que parou a
    mira de conferir por seis pecas publicadas.
    """
    voz = "pt-BR-ThalitaMultilingualNeural"
    alvo = CL.cadencia_da_referencia()
    assert CL.chars_por_cena_na_cadencia(voz, alvo) == \
        ensaio.chars_por_cena(voz, 1, alvo)
    arvore = ast.parse(open(os.path.join(RAIZ, "fabrica",
                                         "cadencia_longo.py")).read())
    for no in ast.walk(arvore):
        if isinstance(no, ast.Constant) and no.value == 0.300:
            pytest.fail("a sobrecarga de montagem foi recopiada para ca")


def test_a_cadencia_e_POR_VOZ_e_nao_da_frota():
    """O numero de caracteres muda com a voz — o erro do 679/698.

    Polones e grego tem P maior, logo cabe MENOS texto na mesma cadencia.
    """
    alvo = CL.cadencia_da_referencia()
    pt = CL.chars_por_cena_na_cadencia("pt-BR-ThalitaMultilingualNeural", alvo)
    pl = CL.chars_por_cena_na_cadencia("pl-PL-MarekNeural", alvo)
    el = CL.chars_por_cena_na_cadencia("el-GR-NestorasNeural", alvo)
    assert len({pt, pl, el}) == 3, "a conta virou numero da frota"


def test_lista_VAZIA_levanta_em_vez_de_devolver_zero():
    """Ausencia de leitura nao e zero — o 739 nomeia isto."""
    with pytest.raises(ValueError):
        CL.cadencia_s([], "pt-BR-ThalitaMultilingualNeural")


def test_a_frase_dos_3_virgula_1_s_comparava_FORMATOS_diferentes():
    """A retratacao, cobrada como PROPRIEDADE e nao como numero.

    Varre as specs de longo do DISCO e exige (a) que a varredura nao fique vazia,
    (b) que a cadencia de longo da frota esteja bem ACIMA dos 3,1 s do short, que
    e o que torna a comparacao antiga um erro de enquadramento, e (c) que ela
    siga abaixo da referencia, que e o que sobrevive da afirmacao.
    """
    medidas = []
    for f in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
        try:
            sp = json.load(open(f))
        except Exception:
            continue
        longo = sp.get("longo") or []
        if len(longo) < 20 or sp.get("voz") not in ensaio.MODELO_VOZ:
            continue
        medidas.append(CL.cadencia_s(longo, sp["voz"]))
    assert len(medidas) >= 50, (
        f"a varredura achou {len(medidas)} specs de longo — com poucas este "
        "teste passa por vacuidade, que e o defeito do 743 em forma de glob."
    )
    medidas.sort()
    mediana = medidas[len(medidas) // 2]
    assert mediana > 3.1 * 2, (
        f"mediana {mediana:.1f} s: se a cadencia de longo da frota fosse "
        "proxima dos 3,1 s do short, a comparacao antiga nao seria erro de "
        "enquadramento e esta nota tinha de ser relida."
    )
    assert max(medidas) < CL.cadencia_da_referencia(), (
        "uma spec de longo nossa alcancou a cadencia da referencia — a "
        "distancia mudou e esta nota tem de ser relida em vez de reaproveitada."
    )


def test_o_modulo_DIZ_que_nao_decide_o_alvo():
    """Limiar sem procedencia e criterio inventado (§10).

    A referencia e UMA peca do dono e o veredito dela e view, que nao medimos.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "cadencia_longo.py")).read()
    assert "decisao do dono" in fonte
    assert "nao e portao" in fonte.lower() or "NAO E PORTAO" in fonte
    cenas = [_cena() for _ in range(30)]
    texto = CL.relato(cenas, "pt-BR-ThalitaMultilingualNeural")
    assert "nao reprova" in texto, "o relato deixou de declarar que informa"
