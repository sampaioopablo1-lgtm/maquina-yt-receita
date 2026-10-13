"""O portao `duracao` tem de valer para QUEM NARRAR, nao so para o edge-tts.

Este arquivo existe por causa do aprendizado 711 e de UMA peca real que foi ao
ar fora da faixa: `labtreinamento-s014` (`K-k8vT0IY2M`), 29 s REAIS contra um
piso de 30 s na epoca, com o portao VERDE. O portao comparava a estimativa do
`MODELO_VOZ`, que e do edge-tts, enquanto o Piper -- 10 a 20% mais rapido, oito
pecas e todas negativas -- era quem narrava.

O provedor NAO esta na spec: ele se decide no runner, depois das tres tentativas
do edge. Logo a peca precisa caber na faixa nos DOIS mundos possiveis, e e isso
que o portao passou a cobrar.

O que estes testes NAO fazem: nao mexem em limiar. `SHORT_MIN_S` e
`SHORT_MAX_S` continuam 18 e 45, e o fator do Piper e medido em
`ensaio.FATOR_PIPER`. Um teste abaixo falha se alguem transformar isto em
limiar novo.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import ensaio  # noqa: E402
import prontidao as P  # noqa: E402

VOZ_BR = "pt-BR-ThalitaMultilingualNeural"


def _spec(cenas, voz=VOZ_BR):
    return {"voz": voz, "longo": [], "short": cenas}


def _cenas(n, chars):
    return [{"layout": "item", "nar": "a" * chars} for _ in range(n)]


def test_a_faixa_NAO_mudou_e_isto_nao_e_limiar_novo():
    # Se alguem "consertar" o portao afrouxando a faixa, este cai primeiro.
    assert (P.SHORT_MIN_S, P.SHORT_MAX_S) == (18, 45)


def test_o_fator_do_piper_continua_MEDIDO_e_menor_que_um():
    # O conserto se apoia em medicao, nao em palpite: as oito pecas do 711
    # vieram TODAS mais curtas que o estimado.
    assert ensaio.FATOR_PIPER[VOZ_BR] < 1.0
    assert 0.7 < ensaio.FATOR_PIPER[VOZ_BR] < 0.95


def test_peca_que_o_EDGE_salva_mas_o_PIPER_joga_abaixo_do_piso_REPROVA():
    # O caso do s014 em forma generica: estimado dentro da faixa, real do Piper
    # abaixo do piso. Antes passava CALADO.
    for chars in range(10, 120):
        sp = _spec(_cenas(5, chars))
        est = ensaio.duracao_estimada_short(sp["short"], VOZ_BR)
        piper = ensaio.duracao_real_prevista(sp["short"], VOZ_BR, "piper")
        if est >= P.SHORT_MIN_S and piper < P.SHORT_MIN_S:
            faltas = P._gate_duracao(sp)
            assert faltas, (
                f"estimado {est:.1f} dentro da faixa e Piper {piper:.1f} abaixo "
                f"do piso de {P.SHORT_MIN_S}: o portao TEM de reprovar")
            assert any("REAIS" in f and "piper" in f for f in faltas), faltas
            break
    else:
        raise AssertionError("nao achei o caso — o modelo mudou de forma")


def test_a_reprovacao_DIZ_o_provedor_e_o_numero_real():
    # Mensagem de portao que nao diz qual mundo falhou nao serve para decidir.
    sp = _spec(_cenas(3, 20))
    faltas = P._gate_duracao(sp)
    assert faltas
    assert any("provedor se decide no RUNNER" in f for f in faltas), faltas


def test_peca_confortavel_nos_DOIS_mundos_PASSA():
    sp = json.load(open(os.path.join(
        os.path.dirname(__file__), "..", "fabrica", "specs",
        "labtreinamento-s028.json"), encoding="utf-8"))
    assert P._gate_duracao(sp) == []


def test_NENHUMA_spec_existente_passa_com_o_piper_fora_da_faixa():
    # Medido em 13/10 ANTES de ligar o conserto: zero. Este teste trava esse
    # zero, e serve de dois jeitos — se alguem escrever spec nova nessa
    # condicao, ela aparece aqui em vez de ir ao ar calada.
    teto = P.SHORT_MAX_S / (1 + P.MARGEM_SHORT)
    culpados = []
    for f in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__), "..", "fabrica", "specs", "*.json"))):
        sp = json.load(open(f, encoding="utf-8"))
        short, voz = sp.get("short") or [], sp.get("voz", "")
        if not short or voz not in ensaio.MODELO_VOZ:
            continue
        est = ensaio.duracao_estimada_short(short, voz)
        if not (P.SHORT_MIN_S <= est <= teto):
            continue          # ja reprovava pelo estimado; nao e o caso silencioso
        piper = ensaio.duracao_real_prevista(short, voz, "piper")
        if not (P.SHORT_MIN_S <= piper <= P.SHORT_MAX_S):
            culpados.append((sp.get("pacote"), round(est, 1), round(piper, 1)))
    assert culpados == [], (
        "spec que o portao aprova pelo estimado e cujo real do Piper cai fora "
        f"da faixa: {culpados}")
