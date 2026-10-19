"""O `mira.confere` parou de conferir a mira do canal e DISSE que nao havia mira.

MEDIDO em 19/10 as 05:2x, escrevendo o `labtreinamento-s083`. O relato saiu com
`canal 'labtreinamento-s083' nao tem ALVO_POR_CANAL medido` — isto e, o
instrumento nao achou o canal porque lia `spec["slug"]`, e o slug da spec de
short solto passou a ser o PACOTE a partir do `s077`.

**A falha e PERMISSIVA: ele nao reprova nada, so para de avisar.** As SEIS pecas
`s077` a `s082` foram ao ar assim, e nas seis eu escrevi na copy "os dois DENTRO
da mira medida do canal" fazendo a conta de cabeca — o item 3 da §10, que diz
que toda conta que eu faco a mao vira um erro meu.

**E a assinatura e a de DOIS DONOS DA MESMA REGRA, UM ATUALIZADO** — a mesma do
`assert 20 <= ds <= 60` do `etapas.py` e a da legenda congelada do short solto:
o `tally_fora_da_mira`, escrito depois, derivava o canal CERTO com
`pacote.rsplit("-s", 1)[0]`, e ninguem voltou ao `confere`.

Este arquivo cobra PROPRIEDADE e nao identidade (743/753/761): ele varre o
disco em vez de listar as sete specs, e **reprova se a varredura ficar vazia**.
"""
import ast
import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import mira  # noqa: E402


def _specs():
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            yield caminho, json.load(f)


def _com_mira():
    """Specs cujo CANAL tem `ALVO_POR_CANAL`, derivadas do disco."""
    fora = []
    for caminho, spec in _specs():
        base = spec.get("pacote") or spec.get("slug") or ""
        canal = base.rsplit("-s", 1)[0] if "-s" in base else base
        if canal in ensaio.ALVO_POR_CANAL and spec.get("short"):
            fora.append((caminho, spec, canal))
    return fora


def test_o_canal_sai_das_DUAS_convencoes_de_slug():
    """A antiga (`slug` = canal) e a nova (`slug` = pacote) dao o mesmo canal."""
    antiga = {"slug": "labtreinamento", "pacote": "labtreinamento-s060"}
    nova = {"slug": "labtreinamento-s083", "pacote": "labtreinamento-s083"}
    assert mira.canal_da_spec(antiga) == "labtreinamento"
    assert mira.canal_da_spec(nova) == "labtreinamento"


def test_toda_spec_de_canal_COM_mira_e_de_fato_conferida():
    alvo = _com_mira()
    assert len(alvo) >= 20, (
        "a varredura perdeu a ancora: sem specs de canal com mira este arquivo "
        f"nao mede nada (achou {len(alvo)})")
    sem = [os.path.basename(c) for c, spec, _ in alvo
           if not mira.confere(spec)["tem_mira"]]
    assert not sem, (
        "o instrumento diz que estas specs nao tem mira a conferir, e o canal "
        f"delas TEM: {sem[:10]}")


def test_a_convencao_NOVA_de_slug_existe_no_disco():
    """Sem spec de `slug` = pacote, o defeito nao reaparece aqui e o arquivo
    passa por vacuidade — era exatamente nessas que o instrumento cegava."""
    novas = [os.path.basename(c) for c, spec, _ in _com_mira()
             if (spec.get("slug") or "") not in ensaio.ALVO_POR_CANAL]
    assert len(novas) >= 6, (
        "as specs cuja convencao de slug causou a cegueira sairam do disco "
        f"(achei {len(novas)}); sem elas este teste nao prova nada")


def test_canal_SEM_mira_continua_sem_mira():
    """Contraprova no outro sentido: o conserto nao INVENTOU mira para ninguem.

    `epomeno-epipedo` e `kolejny-poziom` nao tem `ALVO_POR_CANAL`, e dizer que
    tem seria pior que a cegueira — seria reprovar peca por uma faixa que
    medicao nenhuma sustenta."""
    for canal in ("epomeno-epipedo", "kolejny-poziom"):
        assert canal not in ensaio.ALVO_POR_CANAL, (
            f"{canal} ganhou mira propria — releia este arquivo em vez de "
            "apagar o teste")
        r = mira.confere({"pacote": f"{canal}-s001", "voz": "x", "short": []})
        assert r["tem_mira"] is False
        assert canal in r["motivo"]


def test_o_canal_tem_UM_dono_so():
    """Nenhuma outra funcao do modulo deriva canal por conta propria.

    Por AST, porque o docstring do `canal_da_spec` CITA o `rsplit` antigo para
    se explicar — casar a prosa pegaria a explicacao em vez do codigo, que e a
    licao do teste do `estado_ponte` e do da paleta."""
    with open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    culpados = []
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef) or no.name == "canal_da_spec":
            continue
        for d in ast.walk(no):
            if (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                    and d.func.attr == "rsplit"
                    and any(isinstance(a, ast.Constant) and a.value == "-s"
                            for a in d.args)):
                culpados.append(no.name)
    assert not culpados, (
        "estas funcoes voltaram a derivar o canal sozinhas, que e o defeito de "
        f"dois donos que este arquivo guarda: {culpados}")


def test_o_MOTIVO_do_conserto_continua_escrito():
    """Conserto sem motivo escrito volta calado."""
    with open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    for frase in ("DOIS DONOS DA MESMA REGRA", "PERMISSIVO", "s077"):
        assert frase in texto, f"o motivo perdeu {frase!r}"


def test_a_peca_que_PEGOU_o_defeito_cai_na_mira():
    """A `s083` e a primeira peca em sete de fato conferida, e ela passa.

    Ancorada em PROPRIEDADE: a spec existe, o canal dela tem mira, e as duas
    previsoes caem dentro. Nao crava os valores, porque previsao muda com o
    texto e o que importa e o veredito."""
    caminho = os.path.join(RAIZ, "fabrica", "specs", "labtreinamento-s083.json")
    if not os.path.exists(caminho):
        pytest.skip("a s083 saiu do disco")
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    r = mira.confere(spec)
    assert r["tem_mira"] is True and r["canal"] == "labtreinamento"
    assert not r["fora"], r["motivo"]
