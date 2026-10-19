"""Os tres canais usavam o mesmo mundo visual — contado, nao achado.

O dono disse em 19/10: *"os videos publicados, me parecem todos a mesma
dinamica, imagens, formas, estilo. Em todos os canais. Ajuste."* Varridas as
specs de short da frota ANTES de concordar:

    layouts que existem no short     4  (titulo, item, lista, cta)
    cenas em `item` + `titulo`       93%
    esqueleto mais repetido          titulo-titulo-titulo-titulo-cta,
                                     o MESMO nos TRES canais
    fundos                           #F3F7FA, #F4F1EA, #F5F3ED -- tres claros
                                     quase iguais

O conserto sai da DOCUMENTACAO DELE (`motor/config.py` do zip que ele mandou),
que tem quatro temas prontos com descricao escrita por ele. Estes testes travam
a PROPRIEDADE -- que os canais sao DISTINTOS entre si e que cada escolha tem
procedencia escrita --, nunca o valor de um hex, que e dele e pode mudar.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))
import temas_do_dono as TD  # noqa: E402
import paleta_referencia as PR  # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def test_os_quatro_temas_do_dono_estao_inteiros():
    assert set(TD.TEMAS) == {"noite", "misterio", "papel", "neon"}
    for nome, t in TD.TEMAS.items():
        assert t["descricao"].strip(), nome
        for chave in ("bg", "txt", "acc", "acc2"):
            assert t["cores"][chave].startswith("#"), (nome, chave)


def test_cada_canal_da_frota_tem_tema_e_PROCEDENCIA_escrita():
    for c in CANAIS:
        tema, porque = TD.TEMA_DO_CANAL[c]
        assert tema in TD.TEMAS
        assert len(porque) > 20, f"{c} sem procedencia: escolha sem motivo volta"


def test_os_TRES_canais_tem_FUNDOS_distintos():
    # e o defeito que o dono viu: tres fundos claros quase iguais
    fundos = {c: TD.paleta_do_canal(c)["bg"] for c in CANAIS}
    assert len(set(fundos.values())) == 3, f"fundo repetido entre canais: {fundos}"


def test_os_TRES_canais_tem_ACENTOS_distintos():
    acentos = {c: TD.paleta_do_canal(c)["c1"] for c in CANAIS}
    assert len(set(acentos.values())) == 3, f"acento repetido: {acentos}"


def test_nenhum_canal_divide_o_TEMA_com_outro():
    # a trava 601 ao contrario: paleta de um canal nao se copia para outro
    temas = [TD.TEMA_DO_CANAL[c][0] for c in CANAIS]
    assert len(set(temas)) == 3, f"dois canais no mesmo tema: {temas}"


def test_canal_desconhecido_LEVANTA_em_vez_de_cair_num_padrao():
    # padrao silencioso foi exatamente como os tres fundos convergiram
    for alvo in (TD.paleta_do_canal, TD.fundo_escuro):
        try:
            alvo("canal-que-nao-existe")
        except KeyError:
            continue
        raise AssertionError(f"{alvo.__name__} devolveu padrao para canal desconhecido")


def test_tema_inventado_LEVANTA():
    try:
        TD.paleta_do_tema("turquesa-que-eu-gosto")
    except KeyError:
        return
    raise AssertionError("tema fora dos quatro do dono passou")


def test_a_paleta_do_labtreinamento_tem_UMA_fonte_so():
    # dois arquivos com os mesmos hex foi o defeito que congelou a legenda do
    # short solto por catorze dias: um dono atualizado, o outro nao.
    assert PR.PALETA == TD.paleta_do_canal("labtreinamento")
    # pela AST, nao por texto: o modulo CITA um hex na prosa para explicar a
    # medida da capa, e casar prosa pegaria a explicacao em vez do codigo --
    # o mesmo motivo pelo qual o teste do `estado_ponte` virou AST.
    import ast
    arv = ast.parse((RAIZ / "fabrica" / "paleta_referencia.py").read_text())
    for no in ast.walk(arv):
        if isinstance(no, ast.Constant) and isinstance(no.value, str):
            v = no.value.strip()
            if v.startswith("#") and len(v) == 7 and v != PR.PALETA_ANTIGA["bg"]:
                assert v not in PR.PALETA.values(), (
                    f"{v} escrito a mao no paleta_referencia: a cor tem de vir "
                    "do temas_do_dono, senao os dois divergem"
                )


def test_o_ajuste_do_c2_do_labtreinamento_carrega_a_MEDIDA():
    # o c2 dele e PAINEL e nao acento, pelo SATAVG medido nos 530 quadros
    assert TD.AJUSTES["labtreinamento"]["c2"] == "panel2"
    assert TD.paleta_do_canal("labtreinamento")["c2"] == TD.TEMAS["noite"]["cores"]["panel2"]
    doc = (RAIZ / "fabrica" / "temas_do_dono.py").read_text()
    assert "SATAVG" in doc, "o motivo do ajuste saiu do modulo"


def test_a_FONTE_nao_atravessa_e_o_motivo_esta_escrito():
    # trocar familia de fonte arrisca glifo ausente em grego e polones, e isso
    # so aparece DEPOIS de publicar
    pal = TD.paleta_do_canal("kolejny-poziom")
    assert "fonte" not in str(pal).lower()
    doc = (RAIZ / "fabrica" / "temas_do_dono.py").read_text()
    assert "glifo ausente" in doc


def test_a_escolha_por_ELIMINACAO_vai_declarada_como_tal():
    # vender escolha fraca como medicao e o defeito que custou mais caro aqui
    _, porque = TD.TEMA_DO_CANAL["kolejny-poziom"]
    assert "ELIMINACAO" in porque.upper()


def test_fundo_escuro_usa_o_MESMO_limiar_do_paleta_referencia():
    assert PR.LIMIAR_QUADRO_CLARO == 180
    assert TD.fundo_escuro("labtreinamento") is True
    assert TD.fundo_escuro("kolejny-poziom") is True
    assert TD.fundo_escuro("epomeno-epipedo") is False  # `papel` e claro de proposito


def test_toda_spec_NOVA_usa_a_paleta_do_proprio_canal():
    """De `s064` em diante a paleta sai do modulo, nunca escrita na spec.

    Por que a partir dali e nao de todas: as 205 anteriores foram publicadas com
    a paleta antiga, e reescrever spec publicada em massa e o que a §10 proibe.
    O corte e a peca em que o tema entrou em cada canal.

    E por que isto e TESTE e nao PORTAO: portao que reprova 205 vezes deixa de
    avisar -- o mesmo argumento pelo qual o `mira.py` nunca virou portao.
    """
    import glob
    import json
    import re

    # O corte e POR CANAL, porque o tema entrou em cada um numa peca diferente:
    # o labtreinamento no `s082` (19/10 01:3x, depois de o dono apontar a
    # distancia para o longo dele), o kolejny no `s064` (19/10 02:4x) e o
    # epomeno a partir do `s065` -- o `s064` dele foi publicado as 02:30, uma
    # hora ANTES de o tema existir, e reescrever spec publicada e o que a §10
    # proibe. Um corte unico aqui seria numero meu em cima de historia real.
    CORTE = {"labtreinamento": 82, "kolejny-poziom": 64, "epomeno-epipedo": 65}
    vistas = 0
    for f in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*-s*.json"))):
        nome = pathlib.Path(f).stem
        m = re.match(r"(labtreinamento|epomeno-epipedo|kolejny-poziom)-s(\d+)$", nome)
        if not m or int(m.group(2)) < CORTE[m.group(1)]:
            continue
        canal = m.group(1)
        pal = json.loads(pathlib.Path(f).read_text(encoding="utf-8")).get("paleta") or {}
        do_tema = TD.paleta_do_canal(canal)
        vistas += 1
        for chave in ("bg", "ink", "c1", "c2"):
            assert pal.get(chave) == do_tema[chave], (
                f"{nome}: {chave} e {pal.get(chave)!r} e o tema do canal pede "
                f"{do_tema[chave]!r} — a paleta tem de vir de "
                "temas_do_dono.paleta_do_canal, nunca escrita a mao"
            )
    assert vistas, (
        "nenhuma spec de s064 em diante: a varredura ficou vazia e este teste "
        "deixaria de medir"
    )
