"""A peça cabe no PORTÃO e erra a MIRA DO CANAL — e o modulo pegou o autor dele.

Medido em 13/10/2026 as 06:1x: escrevendo o `labtreinamento-s032` eu produzi uma
spec de 27,8 s reais no Piper. O portao `duracao` aprovou, corretamente — ele
cobra 18 a 45 s, a faixa da FROTA. Mas o `labtreinamento` tem
`ALVO_POR_CANAL = (20,0 a 26,0)`, medido no 698. **Portao verde nao dispensa a
mira.**

E o modulo pegou a peca do PROPRIO AUTOR um minuto depois de existir: a segunda
versao, ja encurtada, ainda dava 28,5 s no mundo `edge`. Terceira versao:
edge 25,3 e piper 20,7, os dois dentro. Por isso os dois mundos, e nao so o que
eu lembrei de olhar.

POR QUE NAO E AVISO DE PORTAO, e e medicao: 44 specs do labtreinamento ficam fora
da mira no mundo edge e 28 no piper, quase todas historicas. Aviso que dispara 44
vezes e aviso que se aprende a ignorar.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import ensaio  # noqa: E402
import mira as M  # noqa: E402
import prontidao as P  # noqa: E402

SPECS = os.path.join(os.path.dirname(__file__), "..", "fabrica", "specs")


def _spec(nome):
    with open(os.path.join(SPECS, nome), encoding="utf-8") as f:
        return json.load(f)


def test_a_mira_do_canal_e_MAIS_APERTADA_que_o_portao_e_e_por_isso_que_existe():
    lo, hi = ensaio.ALVO_POR_CANAL["labtreinamento"]
    assert P.SHORT_MIN_S < lo and hi < P.SHORT_MAX_S, (
        "se a mira do canal nao for mais apertada que o portao, este modulo "
        "nao tem razao de ser")


def test_o_s032_FINAL_cabe_na_mira_nos_DOIS_mundos():
    r = M.confere(_spec("labtreinamento-s032.json"))
    assert r["tem_mira"] is True
    assert r["fora"] == [], r
    lo, hi = r["mira"]
    assert all(lo <= d <= hi for d in r["previsoes"].values()), r["previsoes"]


def test_o_caso_que_o_modulo_pegou_28_ponto_5_no_EDGE_sai_como_FORA():
    # A segunda versao do s032: dentro no piper, FORA no edge. Se o modulo
    # olhasse so um mundo, ela teria ido ao ar assim.
    class _Spec(dict):
        pass
    sp = _spec("labtreinamento-s032.json")
    # Alonga a narracao ate o edge passar do teto, mantendo o piper dentro.
    for c in sp["short"]:
        c["nar"] = (c["nar"] or "") + " E tem mais um detalhe aqui."
    r = M.confere(sp)
    assert "edge" in r["fora"], r
    assert "portao verde nao dispensa a mira" in r["motivo"]


def test_canal_SEM_override_diz_que_nao_tem_mira_em_vez_de_inventar_uma():
    r = M.confere(_spec("epomeno-epipedo-s016.json"))
    assert r["tem_mira"] is False
    assert r["fora"] == []
    assert "nao tem ALVO_POR_CANAL" in r["motivo"]


def test_spec_sem_short_nao_levanta_e_nao_conclui():
    assert M.previsoes({"voz": "pt-BR-ThalitaMultilingualNeural"}) == {}
    assert M.previsoes({"short": [{"nar": "oi"}], "voz": "inexistente"}) == {}


def test_os_dois_mundos_sao_conferidos_e_o_piper_e_o_mais_curto():
    p = M.previsoes(_spec("labtreinamento-s032.json"))
    assert set(p) == {"edge", "piper"}
    assert p["piper"] < p["edge"], (
        "o Piper narra mais rapido (711); se isto inverter, FATOR_PIPER mudou")


def test_os_numeros_vem_de_ensaio_e_NAO_sao_limiar_novo():
    # Um teste contra mim mesmo: se alguem escrever numero solto no mira.py,
    # este cai.
    with open(os.path.join(os.path.dirname(__file__), "..", "fabrica",
                           "mira.py"), encoding="utf-8") as f:
        src = f.read()
    corpo = src.split('"""', 2)[2]          # fora do docstring
    assert "ALVO_POR_CANAL" in corpo and "duracao_real_prevista" in corpo
    for proibido in ("20.0", "26.0", "18,", "45)"):
        assert proibido not in corpo, (
            f"{proibido!r} escrito a mao no corpo do mira.py — os limites vem "
            "de ensaio.ALVO_POR_CANAL")


def test_o_relato_diz_DENTRO_quando_esta_dentro():
    t = M.relato(os.path.join(SPECS, "labtreinamento-s032.json"))
    assert "dentro da mira nos dois mundos" in t
