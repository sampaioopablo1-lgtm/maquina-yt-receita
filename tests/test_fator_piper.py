"""O Piper narra mais rapido que o modelo, e o portao nao percebia.

Aprendizado 711, medido as 14:1x de 12/10/2026 na duracao REAL de nove pecas
publicadas. As oito narradas pelo Piper vieram 10,2% a 20,0% MAIS CURTAS que o
estimado; a unica do edge-tts veio a +0,9%. Oito de oito no mesmo sentido da
1/256 sob a nula.

ESTE ARQUIVO EXISTE PORQUE O DANO JA ACONTECEU, nao por zelo: o portao `duracao`
compara o ESTIMADO contra 30,0-43,1 s, entao ele aprovou em silencio o
`labtreinamento-s014` (`K-k8vT0IY2M`), que foi ao ar com 29 s REAIS contra um
piso de 30. Se alguem apagar `fator_piper` ou `duracao_real_prevista`, o defeito
volta — e volta CALADO, que e a pior forma.
"""

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio as E  # noqa: E402

VOZES = ("pt-BR-ThalitaMultilingualNeural",
         "el-GR-NestorasNeural",
         "pl-PL-MarekNeural")

# As nove pecas medidas: (pacote, voz, estimado, real, provedor)
MEDIDO = [
    ("epomeno-epipedo-s016", "el-GR-NestorasNeural",            41.6, 42, "edge"),
    ("epomeno-epipedo-s017", "el-GR-NestorasNeural",            42.9, 38, "piper"),
    ("epomeno-epipedo-s018", "el-GR-NestorasNeural",            41.9, 35, "piper"),
    ("epomeno-epipedo-s019", "el-GR-NestorasNeural",            41.6, 36, "piper"),
    ("kolejny-poziom-s018",  "pl-PL-MarekNeural",               42.3, 34, "piper"),
    ("kolejny-poziom-s019",  "pl-PL-MarekNeural",               42.3, 38, "piper"),
    ("labtreinamento-s013",  "pt-BR-ThalitaMultilingualNeural", 37.5, 32, "piper"),
    ("labtreinamento-s014",  "pt-BR-ThalitaMultilingualNeural", 36.2, 29, "piper"),
    ("labtreinamento-s015",  "pt-BR-ThalitaMultilingualNeural", 36.5, 30, "piper"),
]


def test_o_fator_existe_para_as_tres_vozes_da_frota():
    for v in VOZES:
        f = E.fator_piper(v)
        assert 0.70 < f < 1.0, (
            f"{v}: fator {f} fora do plausivel. Abaixo de 0,70 ou acima de 1,0 "
            "nao foi medido em nada — e 1,0 significaria apagar o 711"
        )


def test_voz_nao_medida_cai_na_mediana_da_frota_e_nao_em_1():
    f = E.fator_piper("tr-TR-InventadaNeural")
    assert f == E.FATOR_PIPER_FROTA, (
        "voz fora da tabela tem de cair na mediana MEDIDA. Devolver 1,0 seria "
        "dizer que o Piper acerta, que e exatamente o que foi falsificado"
    )
    assert f < 1.0


def test_edge_nao_recebe_correcao_nenhuma():
    """O modelo ACERTA no edge-tts (+0,9%). Corrigi-lo seria estragar."""
    cenas = [{"nar": "Uma frase curta de teste."} for _ in range(11)]
    for v in VOZES:
        assert (E.duracao_real_prevista(cenas, v, "edge")
                == E.duracao_estimada_short(cenas, v))


def test_piper_encurta_sempre_e_nunca_alonga():
    cenas = [{"nar": "Uma frase curta de teste."} for _ in range(11)]
    for v in VOZES:
        crua = E.duracao_estimada_short(cenas, v)
        piper = E.duracao_real_prevista(cenas, v, "piper")
        assert piper < crua, f"{v}: o Piper tem de encurtar, e veio {piper} >= {crua}"


def test_provedor_desconhecido_LEVANTA_em_vez_de_adivinhar():
    """Silencio aqui volta a esconder o 711."""
    cenas = [{"nar": "Uma frase."}]
    with pytest.raises(ValueError) as e:
        E.duracao_real_prevista(cenas, VOZES[0], "elevenlabs")
    assert "edge" in str(e.value) and "piper" in str(e.value)


def test_a_inversa_fecha_com_a_direta():
    for v in VOZES:
        for alvo in (30.0, 33.0, 35.0, 37.0, 43.0):
            est = E.estimativa_para_real(alvo, v)
            assert abs(est * E.fator_piper(v) - alvo) < 0.01, (
                f"{v} @ {alvo}: a inversa nao fecha, e e ela que decide a mira"
            )


def test_a_inversa_no_edge_e_a_identidade():
    for v in VOZES:
        assert E.estimativa_para_real(35.0, v, "edge") == 35.0


@pytest.mark.parametrize("pacote,voz,est,real,prov", MEDIDO,
                         ids=[m[0] + "-" + m[4] for m in MEDIDO])
def test_o_fator_explica_as_nove_pecas_medidas(pacote, voz, est, real, prov):
    """Ancora nos numeros REAIS. Sem isto o fator e opiniao minha.

    A tolerancia e de 3,0 s e nao de decimo, por tres razoes declaradas: o
    YouTube ARREDONDA a duracao PARA CIMA, o n por voz e de 2 a 4, e a
    dispersao dentro da propria voz chega a 5 pontos percentuais.
    """
    previsto = est * (E.fator_piper(voz) if prov == "piper" else 1.0)
    assert abs(previsto - real) <= 3.0, (
        f"{pacote}: previsto {previsto:.1f} contra real {real}. O fator deixou "
        "de explicar a peca que o gerou — remeca antes de mexer"
    )


def test_a_MIRA_de_epomeno_e_kolejny_e_INALCANCAVEL_com_piper():
    """A consequencia que eu nao esperava, e ela e o achado maior.

    O portao `duracao` recusa estimativa acima de 43,1. Com o fator do Piper,
    isso TRAVA a duracao real em 38,2 s no grego e 36,7 s no polones — os dois
    ABAIXO do piso de 41,5 da mira medida desses canais (701). Logo toda peca
    desses dois canais narrada pelo Piper sai FORA do braco do experimento 38,
    em silencio, e nenhuma delas informa a mira.

    Se este teste passar a FALHAR, uma de duas coisas boa aconteceu: o edge-tts
    voltou, ou alguem remediu o fator. Nos dois casos, releia a mira antes de
    confiar nela.
    """
    TETO = 43.1
    for canal, voz in (("epomeno-epipedo", "el-GR-NestorasNeural"),
                       ("kolejny-poziom", "pl-PL-MarekNeural")):
        piso_real, _ = E.alvo_short(canal)
        real_maximo = TETO * E.fator_piper(voz)
        assert real_maximo < piso_real, (
            f"{canal}: real maximo {real_maximo:.1f} ja alcanca o piso "
            f"{piso_real} — a mira voltou a ser alcancavel, releia o 711"
        )


def test_a_mira_do_labtreinamento_CONTINUA_alcancavel():
    """E e por isso que a peca desta rodada sai nesse canal, e nao nos outros."""
    voz = "pt-BR-ThalitaMultilingualNeural"
    piso, teto = E.alvo_short("labtreinamento")
    assert E.estimativa_para_real(piso, voz) <= 43.1, (
        "se o piso do labtreinamento deixar de caber no teto do portao, nao "
        "sobra canal nenhum com mira alcancavel sob o Piper"
    )
