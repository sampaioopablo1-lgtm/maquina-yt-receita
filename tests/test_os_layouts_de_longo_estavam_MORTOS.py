"""O `layouts_longo.py` existia e NENHUM caminho do render o alcancava.

Medido em 19/10 as 04:2x, lendo o despacho do `fabrica.svg_cena`. O modulo foi
escrito na madrugada com `comparar` e `numero` -- coordenadas copiadas do
`motor/scenes.html` do pipeline que o dono mandou -- e o despacho do render 16:9
so conhecia `broll`, `titulo`, `cta`, `lista`, `barras` e `item`. Logo uma cena
com `layout: comparar` caia no ramo final e saia **como fundo vazio**: nenhum
erro, nenhum aviso, so um cartao em branco no meio do video.

**E e a mesma classe do defeito da legenda, pego algumas horas antes:** codigo
escrito que ninguem chama parece pronto e nao esta no ar. La eram dois donos da
mesma regra com um atualizado; aqui e um dono so, sem ninguem chamando.

O que estes testes travam e a PROPRIEDADE -- que todo layout declarado em
`LAYOUTS` e alcancavel pelo render e devolve DESENHO, e que ligar isso nao mexeu
nos layouts antigos --, nunca uma coordenada, que e do pipeline dele.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))
import fabrica as F  # noqa: E402
import layouts_longo as LL  # noqa: E402

PAL = {"bg": "#0E1117", "ink": "#EEF1F5", "c1": "#3DDBD9", "c2": "#1E2430",
       "red": "#FF5A5F", "ok": "#3CCB7F", "panel": "#161B24", "mut": "#8B95A5",
       "acc": "#3DDBD9"}

CENAS = {
    "comparar": {"layout": "comparar",
                 "esq": {"titulo": "PROCV", "itens": ["exige ordem", "quebra ao mover"]},
                 "dir": {"titulo": "PROCX", "itens": ["acha de tras", "sobrevive"]}},
    "numero": {"layout": "numero", "valor": "3x", "legenda": "mais caro",
               "nota": "mesmo cliente, mesmo dia"},
}


def test_TODO_layout_declarado_e_alcancavel_pelo_render():
    # a varredura sai de LAYOUTS, nao de uma lista minha: layout novo entra
    # nesta cobertura sozinho, e e esse o ponto.
    assert LL.LAYOUTS, "LAYOUTS vazio: este teste deixaria de medir"
    for nome in LL.LAYOUTS:
        cena = CENAS.get(nome)
        assert cena is not None, (
            f"layout {nome!r} entrou em LAYOUTS e nao tem cena de exemplo aqui: "
            "sem exemplo ele volta a nao ser exercitado por ninguem"
        )
        svg = F.svg_cena(cena, PAL, 1920, 1080)
        assert "<text" in svg, f"{nome} nao desenhou texto nenhum"


def test_o_conteudo_da_cena_CHEGA_ao_svg():
    # o defeito nao era 'nao desenha', era 'desenha o fundo e esquece a cena':
    # cobrar so o tamanho do svg deixaria o cartao em branco passar.
    svg = F.svg_cena(CENAS["comparar"], PAL, 1920, 1080)
    for pedaco in ("PROCV", "PROCX", "exige ordem", "sobrevive"):
        assert pedaco in svg, f"{pedaco!r} nao chegou ao svg"
    svg = F.svg_cena(CENAS["numero"], PAL, 1920, 1080)
    for pedaco in ("3x", "mais caro", "mesmo cliente"):
        assert pedaco in svg, f"{pedaco!r} nao chegou ao svg"


def test_o_svg_fecha_e_tem_o_fundo_do_tema():
    for nome, cena in CENAS.items():
        svg = F.svg_cena(cena, PAL, 1920, 1080)
        assert svg.startswith("<svg") and svg.endswith("</svg>"), nome
        assert PAL["bg"] in svg, f"{nome} perdeu o fundo do tema"


def test_ligar_isto_NAO_mexeu_nos_layouts_antigos():
    # contraprova no outro sentido: o despacho novo roda ANTES do antigo, logo
    # um bug nele apagaria titulo/item/lista/barras sem ninguem ver.
    antigos = {
        "titulo": {"layout": "titulo", "kicker": "Teste", "sub": "sub"},
        "cta": {"layout": "cta", "kicker": "Inscreva-se", "sub": "agora"},
        "item": {"layout": "item", "kicker": "Item", "preco": "R$ 1"},
        "lista": {"layout": "lista", "kicker": "Lista", "itens": ["a", "b"]},
        "barras": {"layout": "barras", "kicker": "Barras", "itens": ["1", "2"]},
    }
    for nome, cena in antigos.items():
        svg = F.svg_cena(cena, PAL, 1920, 1080)
        assert "<text" in svg, f"{nome} parou de desenhar"
    assert "Teste" in F.svg_cena(antigos["titulo"], PAL, 1920, 1080)


def test_layout_DESCONHECIDO_nao_vira_layout_de_longo():
    # `desenha` tem de devolver None para o que nao e dele, senao ele engole
    # o despacho inteiro.
    assert LL.desenha({"layout": "titulo"}, PAL, 1920, 1080) is None
    assert LL.desenha({"layout": "inventado"}, PAL, 1920, 1080) is None
    assert LL.desenha({}, PAL, 1920, 1080) is None


def test_o_RETRATO_nao_recebe_os_layouts_de_longo():
    # a geometria deles e em 1920x1080 e o 9:16 tem conta propria; deixar
    # passar produziria tinta na borda, que e o defeito do kp-plan-9233.
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text(encoding="utf-8")
    corpo = fonte.split("def svg_cena_retrato")[1].split("\ndef ")[0]
    assert "LL.desenha" not in corpo, (
        "o despacho de longo entrou no render de RETRATO: a geometria dele e "
        "de 1920x1080 e estouraria a borda do 9:16"
    )


def test_o_MOTIVO_de_terem_ficado_mortos_continua_escrito():
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text(encoding="utf-8")
    assert "MORTOS" in fonte, "a nota do defeito saiu do codigo"
    assert "ninguem chama" in fonte
