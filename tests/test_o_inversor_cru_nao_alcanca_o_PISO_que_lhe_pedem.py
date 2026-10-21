"""O inversor publico nao alcanca o piso que lhe pedem — 21/10 as 02:3x.

`mira.chars_no_alvo(voz, n, piso)` responde "quantos caracteres por cena para a
previsao cair em `piso`" com um valor cuja previsao cai **ABAIXO** de `piso`, em
**54 de 54** pares (voz, contagem) das tres vozes vivas de 2 a 20 cenas —
deficit mediano **0,206 s**, maximo **0,870 s**.

E A MESMA CONTA TINHA TRES DONOS: o inversor cru (erra sempre), o
`contagem_de_cenas` com um `faixa[0] + 0.05` escrito A MAO, e o relato do
`mira.orcamento`, que ja chamava o dono CERTO (`janela_do_mundo`, cujo menor
acerta 54 de 54 e difere do cru por +1 caractere em 51 deles). **E o epsilon do
chamador consertava 5 dos 54** — parecia correcao e nao era.

E O CONSERTO INTRODUZIU UM DEFEITO NOVO, na MESMA rodada: `janela_do_mundo`
devolve `None` tambem quando a janela mora ACIMA do teto de varrimento do dono
(`MAX_CHARS_VARRIDOS`), e colapsar isso em zero le como "piso inalcancavel". Com
tres cenas no grego a previsao entra em 242 caracteres e com duas em 380 — a
janela EXISTE. E a familia de 17/10 (vazio de instrumento nao prova ausencia)
dentro do conserto de outra coisa, e por isso a coluna tem TRES estados.
"""
import ast
import inspect
import os
import statistics as st
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import contagem_de_cenas as CC  # noqa: E402
import ensaio                   # noqa: E402
import mira                     # noqa: E402

CANAIS = {
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
}
FONTE_CC = os.path.join(RAIZ, "fabrica", "contagem_de_cenas.py")


def _prev(voz, n, c):
    return ensaio.duracao_real_prevista(
        [{"nar": "x" * c} for _ in range(n)], voz, "edge")


def _pares():
    for canal, voz in CANAIS.items():
        faixa = ensaio.alvo_short(canal)
        for n in range(CC.MIN_CENAS, CC.MAX_CENAS + 1):
            yield canal, voz, faixa, n


def test_o_inversor_CRU_erra_e_isso_e_RECONFERIDO():
    """Numero medido que ninguem reconfere envelhece calado (753), e este e o
    numero que justifica o conserto inteiro."""
    abaixo, dentro, deficit = 0, 0, []
    for _, voz, faixa, n in _pares():
        c = mira.chars_no_alvo(voz, n, faixa[0])
        if not c:
            continue
        p = _prev(voz, n, c)
        if p < faixa[0]:
            abaixo += 1
            deficit.append(faixa[0] - p)
        else:
            dentro += 1
    assert abaixo + dentro >= 40, (
        "so %d pares varridos; abaixo disso este arquivo nao mede nada"
        % (abaixo + dentro))
    assert dentro == 0, (
        "o inversor cru passou a acertar em %d pares. Se ele foi consertado na "
        "RAIZ, esta nota tem de ser RELIDA e a delegacao revista, nao mantida "
        "por inercia" % dentro)
    assert st.median(deficit) > 0.1, (
        "o deficit mediano caiu para %.3f s; abaixo de 0,1 s o erro deixa de "
        "trocar um caractere e a nota se rele" % st.median(deficit))


def test_o_DONO_certo_acerta_e_difere_do_cru_por_UM():
    """`janela_do_mundo[0]` e o piso EXECUTAVEL, e e ele que o relato do `mira`
    ja chamava."""
    acerta, erra, difs = 0, 0, []
    for _, voz, faixa, n in _pares():
        j = mira.janela_do_mundo(voz, n, faixa, "edge")
        if not j:
            continue
        if _prev(voz, n, j[0]) >= faixa[0]:
            acerta += 1
        else:
            erra += 1
        cru = mira.chars_no_alvo(voz, n, faixa[0])
        if cru:
            difs.append(j[0] - cru)
    assert erra == 0, "o dono certo errou em %d pares" % erra
    assert acerta >= 40, "so %d pares com janela; varredura curta" % acerta
    assert difs and max(difs) <= 2 and min(difs) >= 0, (
        "a diferenca contra o cru saiu de [0, 2]: %r — se ela crescer, a causa "
        "nao e mais arredondamento e isto se rele"
        % (sorted(set(difs)),))


def test_o_EPSILON_escrito_a_mao_nao_era_correcao():
    """O `+ 0.05` do chamador antigo consertava uma minoria — e e por isso que
    ele saiu, em vez de ser aumentado para outro numero escrito a mao."""
    ab, de = 0, 0
    for _, voz, faixa, n in _pares():
        c = mira.chars_no_alvo(voz, n, faixa[0] + 0.05)
        if not c:
            continue
        if _prev(voz, n, c) < faixa[0]:
            ab += 1
        else:
            de += 1
    assert ab > de, (
        "o epsilon de 0,05 passou a consertar a MAIORIA (%d de %d): se ele "
        "bastasse, a delegacao seria desnecessaria e esta nota se releria"
        % (de, ab + de))


def test_a_coluna_tem_TRES_estados_e_nenhum_colapsa_nos_outros():
    """alcancavel (inteiro >= 0), inalcancavel (negativo) e NAO MEDIDO (None).
    Colapsar o terceiro em zero foi o defeito que o conserto introduziu."""
    vistos = {"alcancavel": 0, "inalcancavel": 0, "nao_medido": 0}
    for canal, voz in CANAIS.items():
        for r in CC.quadro(canal, voz):
            f = r["folga_no_piso"]
            if f is None:
                vistos["nao_medido"] += 1
                assert r["piso_nao_medido"] is True, (
                    "%s %d cenas: folga None sem a bandeira `piso_nao_medido`"
                    % (canal, r["cenas"]))
                assert r["chars_no_piso"] is None, (
                    "%s %d cenas: nao medido com `chars_no_piso` preenchido"
                    % (canal, r["cenas"]))
            else:
                assert r["piso_nao_medido"] is False
                vistos["inalcancavel" if f < 0 else "alcancavel"] += 1
    for k, v in vistos.items():
        assert v > 0, (
            "o estado %r nao aparece em canal nenhum (%r). Os tres tem de "
            "existir, senao o arquivo nao mede a distincao" % (k, vistos))


def test_o_NAO_MEDIDO_e_cap_de_busca_e_a_janela_EXISTE_acima_dele():
    """A prova de que zero seria FALSO ali: a previsao entra, so acima do teto
    de varrimento."""
    achou = False
    for canal, voz in CANAIS.items():
        faixa = ensaio.alvo_short(canal)
        for r in CC.quadro(canal, voz):
            if not r["piso_nao_medido"]:
                continue
            n = r["cenas"]
            cru = mira.chars_no_alvo(voz, n, faixa[0])
            assert cru and cru >= mira.MAX_CHARS_VARRIDOS, (
                "%s %d cenas saiu NAO MEDIDO sem que o inversor cru encoste no "
                "teto de varrimento (cru=%r, teto=%d) — ai o motivo nao e o cap"
                % (canal, n, cru, mira.MAX_CHARS_VARRIDOS))
            # e a janela de fato existe logo acima
            for c in range(cru, cru + 4):
                if faixa[0] <= _prev(voz, n, c) <= faixa[1]:
                    achou = True
                    break
            assert achou, (
                "%s %d cenas: nao achei media que ponha a previsao dentro nem "
                "quatro caracteres acima do cru — ai 'inalcancavel' seria a "
                "leitura certa e esta nota se rele" % (canal, n))
    assert achou, (
        "nenhum caso NAO MEDIDO no disco — sem ele o terceiro estado nunca e "
        "exercido e a nota perde o objeto")


def test_o_NAO_MEDIDO_nao_entra_na_ESCOLHA_e_sai_NOMEADO():
    """Nao-medido nao serve, e por um motivo DIFERENTE de folga rente — o
    relato tem de separar os dois, do jeito que o `origens_sem_uso` nomeia em
    vez de filtrar."""
    for canal, voz in CANAIS.items():
        nm = [r["cenas"] for r in CC.quadro(canal, voz)
              if r["piso_nao_medido"]]
        if not nm:
            continue
        e = CC.escolha(canal, voz)
        assert e.get("por_cadencia_servivel") not in nm, (
            "%s: a escolha devolveu %r, que esta entre as NAO MEDIDAS %r"
            % (canal, e.get("por_cadencia_servivel"), nm))
        rel = CC.relato(canal, voz)
        assert "NAO FOI MEDIDO" in rel, (
            "%s tem contagem nao medida %r e o relato nao a NOMEIA" % (canal, nm))
        assert "nao prova ausencia" in rel, (
            "%s: o relato nao carrega a razao (vazio de instrumento nao prova "
            "ausencia)" % canal)


def test_a_DELEGACAO_e_por_AST_e_o_epsilon_esta_PROIBIDO():
    fonte = open(FONTE_CC, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    fn = [n for n in ast.walk(arvore)
          if isinstance(n, ast.FunctionDef) and n.name == "_piso_executavel"]
    assert fn, "`_piso_executavel` saiu do modulo"
    txt = ast.unparse(fn[0])
    assert "janela_do_mundo" in txt, (
        "o piso executavel deixou de ser delegado ao dono")
    # o epsilon escrito a mao nao volta em NENHUMA funcao do modulo
    for n in ast.walk(arvore):
        if not isinstance(n, ast.FunctionDef):
            continue
        corpo = ast.unparse(n)
        assert "+ 0.05" not in corpo, (
            "o epsilon escrito a mao voltou em `%s`: ele consertava 5 de 54 e "
            "parecia correcao" % n.name)


def test_a_medida_e_o_motivo_continuam_escritos():
    doc = inspect.getsource(CC._piso_executavel)
    for marca in ("MAX_CHARS_VARRIDOS", "242", "380", "17/10"):
        assert marca in doc, (
            "a marca %r saiu do `_piso_executavel`; sem ela a rodada seguinte "
            "volta a colapsar nao-medido em zero" % marca)
    fonte = open(FONTE_CC, encoding="utf-8").read()
    assert "54 de 54" in fonte, (
        "a medida que justifica a delegacao saiu do modulo")
