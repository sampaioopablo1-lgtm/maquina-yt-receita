# -*- coding: utf-8 -*-
"""O `mira.py` dizia se a peça ESTAVA na mira, nunca quanto escrever para ENTRAR.

MEDIDO em 19/10 às 14:2x, escrevendo o short do `labtreinamento-014`. Ele saiu
com edge **38,5 s** contra a mira medida do canal (20,0 a 26,0) — a mais
apertada da frota —, e a causa foi eu estimar o tamanho da frase de cabeça.

**O instrumento que dá esse número existe desde 11/10** (`ensaio.chars_por_cena`,
escrito justamente porque eu havia generalizado a sobrecarga de UMA voz para a
frota) **e o `mira.py` nunca o chamava**: ele conferia DEPOIS de escrever. É o
item 3 da §10 — o número morava no código e a conta continuava na minha cabeça.

Agora o relato imprime o ORÇAMENTO antes, e a conta é **DELEGADA**: refazer
`P + 0,300` dentro do `mira.py` criaria o segundo dono da sobrecarga por voz,
que é o defeito que congelou a legenda do short solto.

**E A PRIMEIRA EXECUÇÃO DESTE ARQUIVO ACHOU DOIS DEFEITOS DO INSTRUMENTO, uma
hora depois de ele existir:**

1. **ele mirava a mira do CANAL mesmo na spec que declara a PRÓPRIA faixa.** Das
   98 specs de canal com mira, duas declaram `short_alvo_s` — a peça de 2 min
   (95 a 135 s, 40 cenas) e a de 5 s (3 a 6 s, 2 cenas) — e a de 2 min saía com
   orçamento de **ZERO** caractere por cena, porque 40 cenas não cabem em 23 s.
   É o erro de enquadramento do 679/698/725: a mira do canal é sobre a duração
   real do short ORDINÁRIO. A faixa da spec sai de `ensaio.faixa_do_short`, que
   é a FONTE ÚNICA dela desde 16/10;
2. **zero caractere saía como se fosse orçamento.** Não é orçamento, é
   impossibilidade — agora sai como RECUSA com o máximo de cenas que cabe, do
   jeito que o `porta1` recusa janela curta.

**E o conserto validou-se FORA DA AMOSTRA, o que eu não planejei:** apontado
para a faixa certa, o orçamento dá **32** chars/cena para a peça de 2 min
(escrita com 31) e **23** para a de 5 s (escrita com 21) — as duas medidas como
corretas em produção.

**O alvo é o MEIO da faixa, não a borda** — mirar a borda é o que o 752/774
mostra que não sobrevive ao resíduo.
"""
import ast
import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import canal  # noqa: E402
import ensaio  # noqa: E402
import mira  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _especs():
    """Toda spec de short com voz modelada — varrida do DISCO."""
    saida = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(f))
        except Exception:
            continue
        if not (sp.get("short") or []):
            continue
        if sp.get("voz") not in ensaio.MODELO_VOZ:
            continue
        saida.append((os.path.basename(f)[:-5], sp))
    return saida


def _com_mira_propria():
    """As de canal que TEM mira própria."""
    return [(p, sp) for p, sp in _especs()
            if canal.da_spec(sp) in ensaio.ALVO_POR_CANAL]


def _declaram_faixa():
    """As que declaram `short_alvo_s` — formato próprio, não a mira do canal."""
    return [(p, sp) for p, sp in _com_mira_propria() if sp.get("short_alvo_s")]


def test_a_varredura_acha_spec_de_canal_com_mira():
    especs = _com_mira_propria()
    assert len(especs) > 20, (
        f"só {len(especs)} spec(s) de canal com mira própria — a varredura "
        "encolheu e este arquivo passaria por vacuidade"
    )


def test_o_orcamento_existe_para_quem_TEM_mira():
    for pacote, sp in _com_mira_propria():
        orc = mira.orcamento(sp)
        assert orc, f"{pacote}: canal com mira e sem orçamento"
        assert orc["cenas"] == len(sp["short"]), (pacote, orc)
        assert orc["cabe"] is (orc["chars"] > 0), (pacote, orc)
        if orc["cabe"]:
            assert orc["chars"] > 0, (pacote, orc)
        faixa = (ensaio.faixa_do_short(sp) if sp.get("short_alvo_s")
                 else ensaio.ALVO_POR_CANAL[canal.da_spec(sp)])
        assert faixa[0] < orc["alvo"] < faixa[1], (
            f"{pacote}: o alvo {orc['alvo']} não é o MEIO da faixa {faixa} — "
            "mirar a borda é o que o 752/774 mostra que não sobrevive ao resíduo"
        )


def test_a_faixa_da_spec_VENCE_a_mira_do_canal_quando_declarada():
    """O enquadramento do 679/698/725: formato declarado não é o short ordinário."""
    decl = _declaram_faixa()
    assert decl, (
        "nenhuma spec declara `short_alvo_s` — sem ela este arquivo não mede o "
        "defeito que o produziu (a peça de 2 min saindo com orçamento ZERO)"
    )
    for pacote, sp in decl:
        orc = mira.orcamento(sp)
        assert orc["fonte"] == "short_alvo_s da spec", (pacote, orc)
        fx = ensaio.faixa_do_short(sp)
        assert orc["alvo"] == pytest.approx((fx[0] + fx[1]) / 2.0), (pacote, orc)
        assert orc["cabe"], (
            f"{pacote}: declarou faixa própria e o orçamento ainda recusa — "
            "era este o sintoma, com 40 cenas contra os 23 s da mira do canal"
        )


def test_CONTRAPROVA_sem_faixa_declarada_a_fonte_e_o_CANAL():
    sem = [(p, sp) for p, sp in _com_mira_propria() if not sp.get("short_alvo_s")]
    assert len(sem) > 20, f"só {len(sem)} — a contraprova perdeu o objeto"
    for pacote, sp in sem[:60]:
        orc = mira.orcamento(sp)
        assert orc["fonte"] == "ALVO_POR_CANAL do canal", (pacote, orc)


def test_CONTRAPROVA_canal_sem_mira_nao_recebe_orcamento():
    """Inventar orçamento onde não há mira seria pior que calar."""
    sem = [(p, sp) for p, sp in _especs()
           if canal.da_spec(sp) not in ensaio.ALVO_POR_CANAL]
    assert sem, "nenhuma spec de canal SEM mira — a contraprova perdeu o objeto"
    for pacote, sp in sem[:40]:
        assert mira.orcamento(sp) is None, (
            f"{pacote}: orçamento inventado para canal sem mira medida"
        )


def test_cena_demais_RECUSA_em_vez_de_devolver_zero():
    """Zero caractere não é orçamento, é impossibilidade."""
    base = dict(_com_mira_propria()[-1][1])
    base.pop("short_alvo_s", None)
    canal_ = canal.da_spec(base)
    faixa = ensaio.ALVO_POR_CANAL[canal_]
    alvo = (faixa[0] + faixa[1]) / 2.0
    base["short"] = [{"nar": "x"}] * 40
    orc = mira.orcamento(base)
    assert orc["cabe"] is False, orc
    assert orc["chars"] == 0, orc
    assert orc["max_cenas"] > 0, orc
    # e o maximo e a FRONTEIRA, nao um numero qualquer
    assert ensaio.chars_por_cena(base["voz"], orc["max_cenas"], alvo) > 0, orc
    assert ensaio.chars_por_cena(base["voz"], orc["max_cenas"] + 1, alvo) <= 0, orc


def test_o_orcamento_e_DELEGADO_ao_ensaio_por_AST():
    """Refazer `P + 0,300` aqui criaria o segundo dono da sobrecarga por voz.

    Por AST e não por texto: o docstring do módulo CITA a fórmula em prosa para
    se explicar, e casar prosa pegaria a explicação em vez do código.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py")).read()
    arvore = ast.parse(fonte)
    alvo = next((n for n in ast.walk(arvore)
                 if isinstance(n, ast.FunctionDef) and n.name == "orcamento"), None)
    assert alvo is not None, "a função `orcamento` desapareceu do mira.py"

    chamadas = {ast.unparse(n.func) for n in ast.walk(alvo)
                if isinstance(n, ast.Call)}
    assert any("chars_por_cena" in c for c in chamadas), (
        f"o orçamento deixou de delegar ao ensaio: {sorted(chamadas)}"
    )
    assert any("faixa_do_short" in c for c in chamadas), (
        "a faixa da spec deixou de sair da FONTE ÚNICA (`ensaio.faixa_do_short`) "
        f"— e ela existe desde 16/10 justamente por isso: {sorted(chamadas)}"
    )
    # e a sobrecarga NAO se recalcula aqui
    numeros = {n.value for n in ast.walk(alvo)
               if isinstance(n, ast.Constant) and isinstance(n.value, float)}
    assert 0.300 not in numeros and 0.3 not in numeros, (
        f"o intervalo de montagem reapareceu dentro do orçamento: {numeros}. "
        "Dois donos da mesma regra é o defeito que congelou a legenda."
    )


def test_o_RELATO_imprime_o_orcamento_e_diz_de_onde_vem():
    especs = _com_mira_propria()
    assert especs, "sem spec não há relato a conferir"
    caminho = os.path.join(SPECS, especs[-1][0] + ".json")
    r = mira.relato(caminho)
    assert "ORCAMENTO" in r, r[:200]
    assert "chars_por_cena" in r, (
        "o relato não diz de onde o número sai — procedência ausente convida a "
        "refazer a conta à mão"
    )
    assert "caracteres por cena" in r, r[:200]


def test_o_relato_NOMEIA_a_faixa_declarada_em_vez_de_filtrar():
    """Silenciar a conferência é o sentido PERMISSIVO — custou seis peças."""
    decl = _declaram_faixa()
    assert decl, "sem spec de faixa declarada não há o que medir"
    r = mira.relato(os.path.join(SPECS, decl[-1][0] + ".json"))
    assert "faixa PROPRIA" in r, r[:400]
    # e o veredito da mira do canal CONTINUA saindo
    assert "FORA" in r or "cabe na mira" in r, r[:400]


def test_o_relato_NAO_virou_portao():
    """Pelo argumento do próprio `mira.py`: 44 avisos ensinam a ignorar."""
    especs = _com_mira_propria()
    assert especs, "sem spec não há o que medir"
    caminho = os.path.join(SPECS, especs[-1][0] + ".json")
    r = mira.relato(caminho)
    assert "NAO reprova" in r or "nao reprova" in r.lower(), r[:300]


def test_o_caso_REAL_que_produziu_isto_continua_escrito():
    """Conserto sem motivo escrito volta calado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py")).read()
    assert "labtreinamento-014" in fonte, (
        "o caso que produziu o orçamento saiu do módulo"
    )
    doc = open(__file__, encoding="utf-8").read()
    assert "38,5" in doc and "item 3 da §10" in doc
    assert "ZERO" in doc, (
        "a nota do orçamento zero saiu — é ela que impede o conserto de voltar"
    )
