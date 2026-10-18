"""Dois defeitos medidos em 18/10 as 01:2x, e um falso positivo meu no meio.

1. A `contagem` conta origem USADA, logo origem de ZERO usos nao aparece nela —
   e e a de maior valor editorial. O `QiaGg03WSR0` (rank 4 da ordem viva do
   labtreinamento) nao rendeu short nenhum e era invisivel.
2. `kolejny-poziom-s004` e `-s035` declaram `longo_existente: QiaGg03WSR0`, um
   id MEDIDO como do LabTreinamento, enquanto as FONTES das duas dizem
   `kolejny-poziom-018`. Id errado, nao conteudo errado.

E o que vale mais que os dois: a PRIMEIRA versao do detector acusava origem
ausente da playlist `UU...` e deu DOIS falsos positivos — `StQNFMdpGdk` e
`XgqPVJuAk3o`, medidos como longos PUBLICOS do labtreinamento e os dois FORA da
playlist. Logo a playlist OMITE longo publico, e acusar por ausencia dela
inventa achado (725).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import concentracao  # noqa: E402

# A ordem viva medida em 18/10 as 01:1x pela playlist UUtv_... — TREZE ids.
ORDEM_VIVA_LAB = [
    "FtCtIJPsc_Q", "NNgAQLlpEzg", "Sr6VhvD_aPE", "QiaGg03WSR0", "lau1nnOUm1U",
    "6BeNHqT2okA", "dsoEo103l1o", "bQoujWaY7Hw", "ntrMxq89I4o", "4OYBkCHFTV8",
    "3KtwRYxl7_U", "yrWVyqQtw00", "KRUERlNPzDw",
]
# Dono MEDIDO pelo campo `author` da pagina de cada video.
DONO_MEDIDO = {
    "QiaGg03WSR0": "labtreinamento",
    "StQNFMdpGdk": "labtreinamento",
    "XgqPVJuAk3o": "labtreinamento",
}


def test_a_origem_de_zero_usos_NAO_aparece_na_contagem():
    """O defeito: a contagem nao pode nomear o que nunca se usou."""
    assert "QiaGg03WSR0" not in concentracao.contagem("labtreinamento")


def test_e_o_instrumento_novo_a_nomeia():
    """A contraprova no outro sentido: sem ela o achado nao existiria."""
    assert "QiaGg03WSR0" in concentracao.origens_sem_uso(
        "labtreinamento", ORDEM_VIVA_LAB
    )


def test_origem_JA_usada_nao_entra_em_sem_uso():
    """Se entrasse, a funcao devolveria a ordem inteira e nao diria nada."""
    semuso = concentracao.origens_sem_uso("labtreinamento", ORDEM_VIVA_LAB)
    assert "FtCtIJPsc_Q" not in semuso
    assert len(semuso) < len(ORDEM_VIVA_LAB)


def test_a_atribuicao_CRUZADA_do_kolejny_e_acusada():
    fora = concentracao.origem_de_outro_canal("kolejny-poziom", DONO_MEDIDO)
    assert fora.get("QiaGg03WSR0") == "labtreinamento"


def test_e_o_canal_DONO_nao_e_acusado_de_si_mesmo():
    """Contraprova: o mesmo id no canal certo nao e achado."""
    assert concentracao.origem_de_outro_canal("labtreinamento", DONO_MEDIDO) == {}


def test_origem_FORA_do_mapa_nao_e_acusada():
    """Desconhecido nao e 'de outro canal' — e o falso positivo do 725."""
    assert concentracao.origem_de_outro_canal("kolejny-poziom", {}) == {}


def test_o_detector_NAO_acusa_por_ausencia_da_playlist():
    """O falso positivo medido: dois longos PUBLICOS do canal estao fora da
    playlist `UU...`, logo ausencia dela nao pode acusar ninguem."""
    assert "StQNFMdpGdk" not in ORDEM_VIVA_LAB
    assert "XgqPVJuAk3o" not in ORDEM_VIVA_LAB
    assert DONO_MEDIDO["StQNFMdpGdk"] == "labtreinamento"
    assert DONO_MEDIDO["XgqPVJuAk3o"] == "labtreinamento"
    # e nenhum dos dois sai acusado para o canal que de fato os tem
    assert concentracao.origem_de_outro_canal("labtreinamento", DONO_MEDIDO) == {}


def test_a_assinatura_cobra_dono_MEDIDO_e_nao_a_ordem_viva():
    """Trava a correcao: quem passar a ordem viva no lugar do mapa nao acusa
    nada, em vez de acusar tudo o que ela omite."""
    como_lista = {i: None for i in ORDEM_VIVA_LAB}
    assert concentracao.origem_de_outro_canal("kolejny-poziom", como_lista) == {}


def test_a_nota_do_FALSO_POSITIVO_continua_escrita():
    """Se alguem apagar a explicacao, o proximo repete o erro."""
    doc = concentracao.origem_de_outro_canal.__doc__
    assert "falsos positivos" in doc
    assert "725" in doc
    assert "StQNFMdpGdk" in doc


def test_sem_uso_AVISA_que_lista_vazia_nao_prova():
    doc = concentracao.origens_sem_uso.__doc__
    assert "NAO PROVA" in doc.upper()
    assert "OMITE" in doc.upper()
