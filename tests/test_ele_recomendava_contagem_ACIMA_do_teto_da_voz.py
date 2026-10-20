# -*- coding: utf-8 -*-
"""O `contagem_de_cenas` recomendava contagem acima do TETO MEDIDO da voz.

Medido em 20/10 as 04:1x, na PRIMEIRA rodada depois de ele passar a ordenar na
pinca. No `kolejny-poziom` ele deu **15 cenas** como "melhor cadencia entre as
INEDITAS" — e o teto MEDIDO da voz polonesa e **14** (`mira.teto_de_cenas`,
contra o piso OBSERVADO de 21 caracteres por cena).

Nos tres canais ele oferecia 15 a 20 como ineditas recomendadas, com tetos de
11, 15 e 14. **Quinta vez da mesma assinatura: nao chamar quem ja sabe** — o
`MAX_CENAS = 20` do modulo e limite de VARREDURA, nao teto de voz.
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FABRICA)

import contagem_de_cenas as CC            # noqa: E402
import ensaio                             # noqa: E402
import mira                               # noqa: E402

MODULO = os.path.join(FABRICA, "contagem_de_cenas.py")

VOZES = {
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
}


def _escolhas():
    return {c: CC.escolha(c, v) for c, v in VOZES.items()}


def test_o_teto_e_DELEGADO_ao_mira_e_nao_recalculado():
    """Recalcular aqui criaria o segundo dono do piso de caracteres."""
    for canal, voz in VOZES.items():
        faixa = ensaio.alvo_short(canal)
        esperado = mira.teto_de_cenas(voz, faixa)["teto"]
        assert CC.teto_da_voz(voz, faixa) == esperado, canal

    arv = ast.parse(open(MODULO, encoding="utf-8").read())
    chama_o_dono = False
    for no in ast.walk(arv):
        if isinstance(no, ast.Call):
            f = no.func
            if isinstance(f, ast.Attribute) and f.attr == "teto_de_cenas":
                chama_o_dono = True
    assert chama_o_dono, (
        "o modulo deixou de chamar `mira.teto_de_cenas`: o teto volta a ser "
        "conta propria, que e o defeito de 04:1x"
    )
    corpo = open(MODULO, encoding="utf-8").read()
    # 21 e o piso OBSERVADO de caracteres por cena, e ele tem UM dono.
    for no in ast.walk(arv):
        if isinstance(no, ast.Constant) and no.value == 21:
            raise AssertionError(
                "o piso de 21 caracteres apareceu como literal no modulo: ele "
                "mora no `mira.teto_de_cenas`"
            )
    assert "mira.teto_de_cenas" in corpo


def test_os_TRES_tetos_DIVERGEM_senao_volta_a_haver_teto_de_frota():
    tetos = {c: CC.teto_da_voz(v, ensaio.alvo_short(c))
             for c, v in VOZES.items()}
    assert len(set(tetos.values())) >= 2, (
        f"os tetos convergiram ({tetos}): volta a existir teto de FROTA e a "
        "nota de 20/10 as 00:3x tem de ser relida"
    )
    assert all(2 <= t <= CC.MAX_CENAS for t in tetos.values()), tetos


def test_NENHUMA_recomendacao_passa_do_teto_da_voz():
    """Era exatamente isto que ele fazia nos tres canais."""
    for canal, e in _escolhas().items():
        teto = e["teto_da_voz"]
        assert e["por_cadencia_geral"]["cenas"] <= teto, (canal, e["por_cadencia_geral"])
        if e["por_novidade"]:
            assert e["por_novidade"]["cenas"] <= teto, (canal, e["por_novidade"])
        assert all(n <= teto for n in e["ineditas"]), (canal, e["ineditas"], teto)
        if e["por_cadencia"]:
            assert e["por_cadencia"]["cenas"] <= teto, canal
        if e["por_largura"]:
            assert e["por_largura"]["cenas"] <= teto, canal


def test_o_que_ficou_acima_do_teto_e_NOMEADO_e_nao_filtrado():
    """Filtrar em silencio faria a rodada seguinte perguntar por que encurtou."""
    for canal, e in _escolhas().items():
        assert e["acima_do_teto"], (
            f"{canal}: nada acima do teto — sem isso o arquivo nao mede o "
            "defeito, porque filtrar e nomear ficam indistinguiveis"
        )
        r = CC.relato(canal, VOZES[canal])
        assert "TETO MEDIDO" in r, canal
        assert str(e["acima_do_teto"][0]) in r, (canal, r)


def test_a_FRONTEIRA_do_teto_e_cobrada_nos_dois_lados():
    for canal, voz in VOZES.items():
        teto = CC.teto_da_voz(voz, ensaio.alvo_short(canal))
        q = {x["cenas"]: x for x in CC.quadro(canal, voz)}
        assert q[teto]["cabe_na_voz"] is True, (canal, teto)
        if teto + 1 in q:
            assert q[teto + 1]["cabe_na_voz"] is False, (canal, teto + 1)


def test_a_NOVIDADE_de_tamanho_esgotou_em_ALGUNS_canais_e_nao_na_frota():
    """E a PRIMEIRA versao deste teste era uma frase de frota, e ele a pegou.

    Eu escrevi que *"abaixo do teto, o unico tamanho que a frota nunca usou e
    TRES"* — verdade no `kolejny-poziom` (teto 14) e no `labtreinamento`
    (teto 11), e **FALSA** no `epomeno-epipedo`, cujo teto e 15 e onde QUINZE
    segue livre com |dif| 0,28 da cadencia medida. **O 679/698/725 outra vez:
    a frase do canal em que eu estava, vestida de frase da frota** — pego pelo
    teste antes de eu a relatar.

    A propriedade cobrada e a de DOIS LADOS: existe canal em que a novidade de
    tamanho esgotou (so sobra tamanho de cadencia inutavel) e existe canal em
    que ela NAO esgotou. Se um dos dois lados desaparecer, isto se rele.
    """
    LIMITE_UTIL = 2.0   # s por plano de distancia da cadencia medida
    esgotados, abertos = [], []
    for canal in VOZES:
        uteis = [x["cenas"] for x in CC.quadro(canal, VOZES[canal])
                 if x["tamanho_inedito"] and x["cabe_na_voz"]
                 and x["distancia_da_cadencia"] <= LIMITE_UTIL]
        (abertos if uteis else esgotados).append(canal)
    assert esgotados, (
        f"nenhum canal com a novidade de tamanho esgotada ({abertos}): a nota "
        "de 04:2x perdeu o objeto e tem de ser relida"
    )
    assert abertos, (
        f"TODOS os canais esgotaram ({esgotados}): ai a frase passa a ser da "
        "FROTA e esta nota tem de ser reescrita como tal"
    )
    for canal, e in _escolhas().items():
        assert e["ineditas"], (
            f"{canal}: nenhum tamanho inedito abaixo do teto — sem isso o teste "
            "passa por vacuidade"
        )


def test_a_linha_do_teto_tem_UM_dono_e_sai_nos_DOIS_ramos():
    """Frase duplicada e o 753 em forma de texto."""
    assert hasattr(CC, "_linha_do_teto")
    corpo = open(MODULO, encoding="utf-8").read()
    assert corpo.count("TETO MEDIDO desta voz") == 1, (
        "a frase do teto voltou a nascer duplicada"
    )
    fechado = CC.relato("kolejny-poziom", VOZES["kolejny-poziom"])
    aberto = CC.relato("labtreinamento", VOZES["labtreinamento"])
    assert "pinca" in fechado and "TETO MEDIDO" in fechado
    assert "pinca" not in aberto and "TETO MEDIDO" in aberto, (
        "o ramo com janela ABERTA deixou de nomear o teto — foi um bloco depois "
        "do `return` que escondeu o orcamento em 19/10 as 15:2x"
    )


def test_o_codigo_de_saida_e_SEMPRE_zero():
    for canal in VOZES:
        p = subprocess.run([sys.executable, MODULO, canal],
                           capture_output=True, text=True, cwd=RAIZ)
        assert p.returncode == 0, (canal, p.returncode, p.stderr[-300:])
        assert "TETO MEDIDO" in p.stdout, canal


def test_a_MEDIDA_dos_tres_tetos_continua_escrita_no_modulo():
    """Conserto sem o numero que o motivou volta calado."""
    t = open(MODULO, encoding="utf-8").read()
    for n in ("11", "14", "15"):
        assert n in t, f"o teto {n} saiu da tabela do modulo"
    assert "04:1x" in t, "a data da medicao saiu do modulo"
    assert "QUINTA vez" in t, (
        "a contagem da assinatura ('nao chamar quem ja sabe') saiu do modulo"
    )
