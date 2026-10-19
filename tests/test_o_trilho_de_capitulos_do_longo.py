"""O trilho permanente do topo — primeiro tijolo do longo na nuvem.

Em 19/10/2026 o dono decidiu a direcao: *"busco deixar tudo por aqui na nuvem,
produzindo videos melhores que este de 8 min"*. O trilho e a primeira das tres
distancias que eu medi em 16/10 entre a peca dele e as nossas.

**A GEOMETRIA E MEDIDA.** O trilho e, por definicao, o que nao muda entre
quadros, logo ele se acha por VARIANCIA TEMPORAL. Medido no proprio video, 21
quadros a 1/25 s: as linhas 4 a 9 de 144 tem desvio 10 a 28 e brilho 26 a 42,
entre duas faixas quietas e escuras (0-3 e 10-15). `4/144 = 0,028`,
`9/144 = 0,069`.

O que este arquivo trava e a PROPRIEDADE, nunca o pixel:

  1. o trilho CABE na largura util, com qualquer numero de capitulos — ele
     encolhe em vez de cortar, porque capitulo cortado desfaz a funcao dele;
  2. o capitulo CORRENTE se distingue dos outros (cor E peso);
  3. a faixa fica DENTRO da banda medida;
  4. destacar capitulo inexistente LEVANTA, em vez de desenhar o errado;
  5. e a procedencia da medicao continua escrita no modulo.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import trilho  # noqa: E402
import paleta_referencia as pr  # noqa: E402

CAPS4 = ["A armadilha", "Os três limites", "O que o PROCX muda",
         "Quando usar cada um"]
W, H = 1920, 1080


def test_o_trilho_CABE_com_quatro_capitulos():
    assert trilho.cabe(CAPS4, W, H), trilho.relato(CAPS4, W, H)


def test_ele_ENCOLHE_em_vez_de_cortar_quando_ha_muitos():
    """Capitulo que some do trilho desfaz a unica funcao dele."""
    muitos = [f"Capitulo numero {i}" for i in range(1, 11)]
    c4 = trilho.corpo_que_cabe(CAPS4, W, H)
    c10 = trilho.corpo_que_cabe(muitos, W, H)
    assert c10 < c4, (c4, c10)
    # e o texto de TODOS continua no SVG
    svg = trilho.faixa(muitos, 3, pr.PALETA, W, H)
    for cap in muitos:
        assert cap in svg, cap


def test_o_capitulo_CORRENTE_se_distingue():
    svg = trilho.faixa(CAPS4, 2, pr.PALETA, W, H)
    aceso = pr.PALETA["c1"]
    # o corrente sai no acento, e ele aparece UMA vez so
    assert svg.count(f'fill="{aceso}"') == 1, svg.count(f'fill="{aceso}"')
    # e o par cor+peso: so o corrente e 700
    assert svg.count('font-weight="700"') == 1
    # o trecho do corrente carrega o acento
    # o corrente vive num tspan proprio, com o acento e o peso
    corrente = re.findall(
        r'<tspan fill="' + re.escape(aceso) + r'"[^>]*font-weight="700">([^<]*)</tspan>', svg)
    assert corrente == ["3 O que o PROCX muda"], corrente


def test_a_faixa_fica_DENTRO_da_banda_medida():
    svg = trilho.faixa(CAPS4, 0, pr.PALETA, W, H)
    # `y="..."` precisa do espaco antes: sem ele o regex casa o `y` de
    # `opacitY="1.0"` e o teste mede 1,0 em vez da linha de base. Pego na
    # primeira execucao — defeito do INSTRUMENTO, nao do codigo.
    ys = [float(y) for y in re.findall(r'\sy="([0-9.]+)"', svg)]
    corpo = trilho.corpo_que_cabe(CAPS4, W, H)
    assert ys, "nenhum texto no trilho — o teste deixaria de medir"
    for y in ys:
        # `y` e a linha de base; o topo das maiusculas fica ~0,72 corpo acima
        assert y - corpo * 0.75 >= H * trilho.faixa_y0() - 1, (y, corpo)
        assert y <= H * trilho.faixa_y1() + corpo * 0.30, (y, corpo)


def test_capitulo_corrente_FORA_da_lista_levanta():
    """Trilho que destaca o capitulo errado e pior que trilho nenhum."""
    for mau in (-1, 4, 99):
        try:
            trilho.faixa(CAPS4, mau, pr.PALETA, W, H)
        except ValueError:
            continue
        raise AssertionError(f"aceitou capitulo {mau}")


def test_lista_vazia_devolve_vazio_em_vez_de_quebrar():
    assert trilho.faixa([], 0, pr.PALETA, W, H) == ""


def test_o_texto_e_escapado_para_XML():
    svg = trilho.faixa(["Risco & retorno", "A <regra>"], 0, pr.PALETA, W, H)
    assert "&amp;" in svg and "&lt;regra&gt;" in svg
    assert "& " not in svg.replace("&amp;", "").replace("&lt;", "").replace("&gt;", "")


def test_a_PROCEDENCIA_da_medicao_continua_escrita():
    """Geometria sem procedencia vira numero inventado na rodada seguinte."""
    fonte = (RAIZ / "fabrica" / "trilho.py").read_text(encoding="utf-8")
    assert "variancia temporal" in fonte
    assert "4/144" in fonte and "9/144" in fonte
    assert "FtCtIJPsc_Q" in fonte
    # e o que a medicao NAO cobre vai declarado
    assert "nao mede" in fonte.lower() or "NAO mede" in fonte
