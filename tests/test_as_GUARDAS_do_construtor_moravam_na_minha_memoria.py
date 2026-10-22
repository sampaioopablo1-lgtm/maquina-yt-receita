# -*- coding: utf-8 -*-
"""As guardas do CONSTRUTOR moravam na minha memoria — 22/10 as 20:4x.

A peca se escreve num construtor que vive FORA do repo, e as guardas dele eu
redigitava a cada rodada: o `assert layout in SONDADOS` entrou depois do cartao
em branco de 19/10 as 18:18Z e a da thumbnail **nunca existiu**. A evidencia e
a contagem: a thumbnail estourou o limite em **dez** rodadas desta sessao, e em
18/10 as 08:1x um render inteiro morreu em `KeyError: 'longo'`.

A FORMA DOS TESTES:
  * a peca de prova e DERIVADA do disco e o arquivo **reprova dizendo que
    perdeu a ancora** se nenhuma passar;
  * a contraprova vai nos DOIS sentidos em cada guarda — senao bastaria
    levantar sempre;
  * todo limite e cobrado como LIDO do dono, por AST, e literal proibido;
  * a FRONTEIRA e cobrada (o limite cabe, o limite + 1 nao);
  * a medida que justifica NAO ser portao e RECONFERIDA contra o disco como
    PROPORCAO (a licao de 14:4x), e o arquivo **falha se ela zerar ou virar
    tudo**;
  * o `prontidao` **nao pode** importar isto, senao viraria portao e
    reprovaria o acervo.
"""
import ast
import copy
import glob
import inspect
import json
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as AR            # noqa: E402
import guardas_do_construtor as GC      # noqa: E402
import variedade as V                   # noqa: E402

PISO_SPECS = 150


def _fonte(obj):
    return textwrap.dedent(inspect.getsource(obj))


def _chamados(fn):
    out = set()
    for n in ast.walk(ast.parse(_fonte(fn))):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.add(f.id)
            elif isinstance(f, ast.Attribute):
                out.add(f.attr)
                if isinstance(f.value, ast.Name):
                    out.add("%s.%s" % (f.value.id, f.attr))
    return out


@pytest.fixture(scope="module")
def specs():
    p = sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")))
    assert len(p) >= PISO_SPECS, (
        "so %d spec(s) no disco: abaixo de %d este arquivo passa por VACUIDADE"
        % (len(p), PISO_SPECS))
    return p


@pytest.fixture(scope="module")
def limpa(specs):
    """Uma spec do disco que passa TODAS as guardas — DERIVADA, nao nomeada:
    nomear um pacote seria identidade onde ha propriedade (743/753/761)."""
    for caminho in reversed(specs):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        if not sp.get("short"):
            continue
        q = GC.confere(sp)
        # E ELA TEM DE SER DE CANAL COM TEMA: num canal PARADO a paleta do dono
        # nao existe, logo a contraprova da paleta nao mediria nada. Foi este
        # teste que me obrigou a dar o TERCEIRO estado a guarda.
        if q["ok"] and not (q["paleta"] or {}).get("sem_tema"):
            return sp
    pytest.fail("nenhuma spec do disco passa todas as guardas num canal COM "
                "tema: perdi a ancora, e sem ela as contraprovas nao medem "
                "nada")


# ------------------------------------------------------------------ os dois lados

def test_a_peca_do_disco_PASSA_todas(limpa):
    assert GC.exige(limpa) is limpa, (
        "`exige` devolve a propria spec, para poder ser usado em linha no "
        "construtor")


def test_a_thumbnail_de_CINCO_palavras_LEVANTA(limpa):
    ruim = copy.deepcopy(limpa)
    ruim["thumb"] = {"l1": "Nao e veredito", "l2": "e preco"}
    with pytest.raises(GC.GuardaDoConstrutor) as e:
        GC.exige(ruim)
    assert "thumb" in str(e.value)


def test_a_FRONTEIRA_da_thumbnail_nos_dois_lados(limpa):
    lim = V.THUMB_MAX_PALAVRAS
    cabe = copy.deepcopy(limpa)
    cabe["thumb"] = {"l1": " ".join(["a"] * lim), "l2": ""}
    assert GC.confere(cabe)["thumb"]["ok"] is True, (
        "o limite EXATO tem de caber: %d palavra(s)" % lim)
    nao = copy.deepcopy(limpa)
    nao["thumb"] = {"l1": " ".join(["a"] * lim), "l2": "b"}
    assert GC.confere(nao)["thumb"]["ok"] is False, (
        "o limite + 1 nao pode caber")


def test_layout_FORA_do_sondado_LEVANTA_e_o_conjunto_e_SONDADO(limpa):
    import layouts_do_short as LS
    desenham = set(LS.desenham())
    assert desenham, "a sonda do render devolveu conjunto vazio: vacuidade"
    candidato = None
    for nome in ("numero", "comparar", "formula", "erro", "divisor"):
        if nome not in desenham:
            candidato = nome
            break
    assert candidato, ("o retrato passou a desenhar TUDO — ai o cartao em "
                       "branco deixou de ser possivel e esta guarda se rele")
    ruim = copy.deepcopy(limpa)
    ruim["short"][1]["layout"] = candidato
    with pytest.raises(GC.GuardaDoConstrutor) as e:
        GC.exige(ruim)
    assert "layouts" in str(e.value) and "CARTAO EM BRANCO" in str(e.value)
    assert set(GC.confere(limpa)["layouts"]["desenham"]) == desenham, (
        "o conjunto tem de ser o SONDADO, nao uma lista escrita a mao")


def test_a_chave_longo_AUSENTE_levanta_e_a_lista_VAZIA_passa(limpa):
    """Ausencia de chave nao e valor vazio (18/10, 08:1x)."""
    sem = copy.deepcopy(limpa)
    del sem["longo"]
    with pytest.raises(GC.GuardaDoConstrutor) as e:
        GC.exige(sem)
    assert "longo" in str(e.value) and "KeyError" in str(e.value)
    vazia = copy.deepcopy(limpa)
    vazia["longo"] = []
    assert GC.confere(vazia)["longo"]["ok"] is True, (
        "lista VAZIA e o valor CERTO em short solto")


def test_a_paleta_a_mao_LEVANTA_e_SUBCONJUNTO_nao(limpa):
    """O subconjunto nao acusa — a licao de 20/10 as 00:3x, quando contar com
    `==` inflou o achado de 252 para 255."""
    uma = copy.deepcopy(limpa)
    uma["paleta"] = dict(uma["paleta"])
    k = sorted(uma["paleta"])[0]
    uma["paleta"][k] = "#010203"
    with pytest.raises(GC.GuardaDoConstrutor) as e:
        GC.exige(uma)
    assert "paleta" in str(e.value)
    menos = copy.deepcopy(limpa)
    menos["paleta"] = {kk: vv for kk, vv in list(menos["paleta"].items())[:3]}
    assert GC.confere(menos)["paleta"]["ok"] is True, (
        "paleta com MENOS chaves e todos os valores iguais nao contradiz nada")


def test_pacote_diferente_de_slug_LEVANTA(limpa):
    ruim = copy.deepcopy(limpa)
    ruim["pacote"] = str(ruim["slug"]) + "-x"
    with pytest.raises(GC.GuardaDoConstrutor) as e:
        GC.exige(ruim)
    assert "pacote" in str(e.value)


# -------------------------------------------------------------- a delegacao

def test_TODO_limite_e_LIDO_do_dono_por_AST():
    fonte = _fonte(GC)
    corpo = ast.parse(fonte)
    for proibido in ("THUMB_MAX_PALAVRAS =", "GANCHO_MAX_PALAVRAS ="):
        assert proibido not in fonte, (
            "o modulo redefine %r: copiar o limite aqui cria o SEGUNDO dono"
            % proibido)
    chamados = _chamados(GC.confere)
    for preciso in ("desenham", "primeira_frase", "conflitos", "da_spec"):
        assert preciso in chamados, (
            "`confere` nao chama %r: cada limite e cada conjunto sai do dono"
            % preciso)
    # nenhum hex de cor no modulo: a paleta e comparada pelo dono
    assert "#" not in "".join(
        n.value for n in ast.walk(corpo)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ).replace("#REF!", ""), (
        "ha literal de cor no modulo: a comparacao de paleta e do "
        "`paleta_da_spec`, e copiar hex aqui criaria o TERCEIRO dono da "
        "identidade visual")


def test_o_confere_NOMEIA_todas_as_guardas_e_so_o_exige_PARA(limpa):
    ruim = copy.deepcopy(limpa)
    ruim["thumb"] = {"l1": "a b c", "l2": "d e"}
    ruim["pacote"] = str(ruim["slug"]) + "-x"
    q = GC.confere(ruim)
    assert q["thumb"]["ok"] is False and q["pacote"]["ok"] is False, (
        "`confere` nao pode parar na primeira: o relato mostra o quadro "
        "inteiro, e so o `exige` interrompe")
    assert q["layouts"]["ok"] is True, "as guardas limpas seguem nomeadas"


# ---------------------------------------------------------- nao e portao

def test_NAO_e_portao_e_o_prontidao_NAO_o_importa():
    import prontidao
    fonte = _fonte(prontidao)
    corpo = ast.parse(fonte)
    nomes = set()
    for n in ast.walk(corpo):
        if isinstance(n, ast.Import):
            nomes.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            nomes.add(n.module or "")
    assert "guardas_do_construtor" not in nomes, (
        "o `prontidao` importou as guardas: ai elas viram PORTAO e reprovam o "
        "acervo, que e o argumento pelo qual o `mira.py` tambem nao e portao")


def test_a_medida_que_justifica_NAO_ser_portao_e_RECONFERIDA(specs):
    com_short = ruins = 0
    for caminho in specs:
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        if not sp.get("short"):
            continue
        com_short += 1
        if not GC.confere(sp)["thumb"]["ok"]:
            ruins += 1
    assert com_short >= PISO_SPECS, "vacuidade"
    frac = ruins / float(com_short)
    assert 0.02 <= frac <= 0.60, (
        "fracao de specs com thumbnail acima do limite em %.3f (%d de %d), "
        "fora da faixa OBSERVADA — RELEIA a nota em vez de mover o numero. A "
        "medida e PROPORCAO e nao contagem porque o acervo cresce uma spec por "
        "rodada (22/10, 14:4x), e e ela que diz por que isto nao e portao"
        % (frac, ruins, com_short))


def test_ele_esta_na_PASSADA_senao_e_layout_morto():
    assert "guardas_do_construtor" in AR.INSTRUMENTOS, (
        "instrumento fora da passada e codigo que ninguem chama — a classe dos "
        "layouts mortos, e foi assim que o `contagem_declarada` e o "
        "`layouts_do_short` ficaram de fora por dias")
    assert "guardas_do_construtor" not in (AR.FORA_DA_PASSADA or {})


def test_a_convencao_do_relato_e_caminho_spec(limpa):
    """A passada decide pela ARIDADE, nao pelo nome (20/10, 11:3x)."""
    a = GC.relato(None, spec=limpa)
    b = GC.relato(limpa)              # compatibilidade: a spec na 1a posicao
    assert a == b
    par = list(inspect.signature(GC.relato).parameters)
    assert par[:2] == ["caminho", "spec"], (
        "a assinatura tem de ser `(caminho, spec=None)`, que e o que a passada "
        "despacha")


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = GC.__doc__ or ""
    for pedaco in ("minha memoria", "dez", "KeyError", "433", "86",
                   "NAO E PORTAO"):
        assert pedaco in doc, (
            "o docstring perdeu %r: conserto sem motivo escrito volta calado"
            % pedaco)


def test_canal_SEM_tema_nao_sai_como_COMPATIVEL(specs):
    """O terceiro estado, e ele e o sentido permissivo se faltar: canal PARADO
    nao tem paleta do dono, e dizer `ok` sem dizer que nao conferiu e a classe
    da mira que parou de avisar por seis pecas."""
    achou = None
    for caminho in specs:
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        if not sp.get("short"):
            continue
        q = GC.confere(sp)
        if (q["paleta"] or {}).get("sem_tema"):
            achou = q
            break
    assert achou, ("nenhuma spec de canal SEM tema no disco — ai este estado "
                   "perde o objeto e esta guarda se rele")
    assert achou["paleta"]["ok"] is True, (
        "sem comparador nao ha o que reprovar: a guarda passa")
    assert achou["paleta"]["motivo"], (
        "e ela tem de DIZER que nao conferiu, em vez de calar")
    assert not achou["paleta"]["conflitos"]
    # e a spec de canal COM tema nao pode sair marcada assim
    import canal as CA
    for caminho in reversed(specs):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        if not sp.get("short"):
            continue
        q = GC.confere(sp)
        if not (q["paleta"] or {}).get("sem_tema"):
            assert q["paleta"].get("motivo") is None or q["paleta"]["conflitos"]
            return
    pytest.fail("nenhuma spec de canal COM tema: perdi o outro lado")
