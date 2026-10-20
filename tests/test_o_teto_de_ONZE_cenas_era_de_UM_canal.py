"""O teto de ONZE cenas era de UM canal, e eu o li como da frota — 20/10, 00:3x.

O `CLAUDE.md` dizia, desde 11/10: *"doze cenas estourariam o teto de 43,1 so em
silencio, entao o teto real no alvo atual e onze"*. Medido com o `ensaio`, doze
cenas custam **20,06 s** de silencio na voz grega — menos da METADE do teto. E a
medicao devolve a forma exata do erro, que e a melhor parte:

| voz | faixa | teto |
|---|---|---|
| `pt-BR` | mira do `labtreinamento` (20,0 a 26,0) | **11** |
| `el-GR` | `ALVO_SHORT` da frota (41,5 a 43,0) | **15** |
| `pl-PL` | idem | **14** |

**Logo o onze estava CERTO no quadro dele e errado como frase da frota** — a
assinatura do 679/698/725. E o custo foi de variedade: eu limitei todo esqueleto
a onze cenas, e a frota nao tinha nenhuma peca de doze ate esta rodada.

A FORMA DESTES TESTES: o teto e cobrado na FRONTEIRA (o teto cabe, o teto + 1
nao), os tres quadros tem de DIVERGIR entre si — se convergirem, volta a existir
um teto da frota e esta nota se rele —, o piso de caracteres e **reconferido
contra o disco** em vez de ficar cravado em prosa (753), e a conta e delegada ao
`ensaio` por AST, porque refazer `P + 0,300` aqui criaria o segundo dono da
sobrecarga por voz — o defeito que congelou a legenda.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "mira.py")
sys.path.insert(0, FABRICA)

import ensaio  # noqa: E402
import mira  # noqa: E402

EL = "el-GR-NestorasNeural"
PL = "pl-PL-MarekNeural"
PT = "pt-BR-ThalitaMultilingualNeural"


def _dur(voz, n, chars):
    return ensaio.duracao_real_prevista(
        [{"nar": "x" * chars} for _ in range(n)], voz, "edge")


def test_doze_cenas_NAO_estouram_o_teto_so_em_silencio():
    """A frase de 11/10 dizia o contrario, e e ela que cai."""
    for voz in (EL, PL, PT):
        assert _dur(voz, 12, 1) < ensaio.ALVO_SHORT[1], voz


def test_o_teto_e_cobrado_na_FRONTEIRA():
    for voz in (EL, PL):
        r = mira.teto_de_cenas(voz, ensaio.ALVO_SHORT)
        n = r["teto"]
        assert n and n >= 12, r
        piso, teto = ensaio.ALVO_SHORT
        # no teto existe orcamento na faixa
        cabe = [c for c in range(r["chars_minimos"], 241)
                if piso <= _dur(voz, n, c) <= teto]
        assert cabe, r
        # no teto + 1 nenhum orcamento com texto legivel cabe
        passa = [c for c in range(r["chars_minimos"], 241)
                 if piso <= _dur(voz, n + 1, c) <= teto]
        assert not passa, (voz, n + 1, passa[:5])


def test_os_TRES_quadros_DIVERGEM_e_e_por_isso_que_nao_ha_teto_da_frota():
    el = mira.teto_de_cenas(EL, ensaio.ALVO_SHORT)["teto"]
    pl = mira.teto_de_cenas(PL, ensaio.ALVO_SHORT)["teto"]
    pt = mira.teto_de_cenas(PT, ensaio.ALVO_POR_CANAL["labtreinamento"])["teto"]
    assert len({el, pl, pt}) >= 2, (
        "se os quadros convergirem, volta a existir um teto da frota e esta "
        "nota tem de ser RELIDA: %s" % [el, pl, pt])
    assert el > pt, (el, pt)


def test_o_ONZE_de_11_10_estava_CERTO_no_quadro_dele():
    """Sem este, a retratacao viraria 'o numero era lixo', e nao era."""
    r = mira.teto_de_cenas(PT, ensaio.ALVO_POR_CANAL["labtreinamento"])
    assert r["teto"] == 11, r


def test_o_piso_de_caracteres_e_RECONFERIDO_contra_o_disco():
    """Numero medido que ninguem reconfere envelhece calado (753)."""
    menor = None
    for p in glob.glob(os.path.join(FABRICA, "specs", "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        sh = sp.get("short") or []
        if len(sh) < 2:
            continue
        nars = [c.get("nar") or "" for c in sh]
        if not all(nars):
            continue
        m = sum(len(n) for n in nars) / len(nars)
        if menor is None or m < menor:
            menor = m
    assert menor is not None, "varredura vazia nao mede nada"
    assert abs(menor - mira.CHARS_MINIMOS_OBSERVADOS) <= 1.0, (
        "o piso OBSERVADO mudou no disco (%0.1f) e a constante nao: %d"
        % (menor, mira.CHARS_MINIMOS_OBSERVADOS))


def test_a_conta_e_DELEGADA_ao_ensaio_e_nenhuma_sobrecarga_mora_aqui():
    fonte = open(MODULO, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "teto_de_cenas"]
    assert len(alvo) == 1
    chamadas = {
        "%s.%s" % (n.func.value.id, n.func.attr)
        for n in ast.walk(alvo[0])
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
    }
    assert "ensaio.duracao_real_prevista" in chamadas, chamadas
    # e nenhum numero de sobrecarga por voz recopiado
    for proibido in ("0.300", "1.573", "1.719", "1.037"):
        assert proibido not in ast.unparse(alvo[0]), proibido


def test_a_peca_de_DOZE_cenas_existe_no_disco():
    """Sem ela o arquivo nao mede o que o conserto destravou."""
    doze = []
    for p in glob.glob(os.path.join(FABRICA, "specs", "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if len(sp.get("short") or []) == 12:
            doze.append(os.path.basename(p))
    assert doze, "nenhuma spec de doze cenas: o teto voltou a limitar"
