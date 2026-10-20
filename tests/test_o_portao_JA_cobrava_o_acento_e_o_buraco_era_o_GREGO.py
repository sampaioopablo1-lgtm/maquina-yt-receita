# -*- coding: utf-8 -*-
"""Eu escrevi "nenhum portao cobra acento da NARRACAO" e era FALSO.

RETRATACAO de 19/10 as 22:3x. O portao `ortografia` cobra a acentuacao da
narracao do SHORT desde 25/08/2026, e o docstring dele carrega o MESMO incidente
que eu descrevi ao justificar o `fabrica/acento.py` quatro horas antes.

Medido pelo discriminador — tirar os acentos de uma spec e rodar o portao:
pt-BR acusava, pl acusava, e **el passava LIMPO**. A causa era a tabela
`prontidao.DIACRITICOS` nao ter `el`, que e 87 das specs de short da frota e o
canal onde a falha de fato aconteceu. E o 725 DENTRO do portao.

**E O DISCRIMINADOR TINHA UM BURACO PROPRIO, retratado em 20/10 as 21:0x:**
"tirar os acentos" era NFD + descartar `Mn`, e isso nao alcanca letra cujo sinal
nao decompoe — o `l` com traco do polones sobrevive. Em 20/10 este teste
REPROVOU acusando o portao de calar em `pl`, e o portao estava certo: onze das
34 letras acentuadas da narracao tinham sobrevivido a "remocao". O conserto esta
no `_sem_acento`, que agora DERIVA a base da letra do nome Unicode dela e
**confere** que nao sobrou nenhuma letra da tabela do idioma antes de julgar o
portao.
"""
import glob
import json
import os
import sys
import re
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import acento as A  # noqa: E402
import prontidao as P  # noqa: E402

PISO_DE_SPECS_EL = 50


def _base_da_letra(c: str) -> str:
    """A letra sem o sinal, para o caractere que NAO decompoe.

    `unicodedata.name('l')` do `l` com traco e
    *"LATIN SMALL LETTER L WITH STROKE"* — a base esta no proprio nome, e por
    isso ela e DERIVADA em vez de escrita numa tabela minha.
    """
    try:
        nome = unicodedata.name(c)
    except ValueError:
        return ""
    m = re.search(r"LETTER ([A-Z]) WITH ", nome)
    if not m:
        return ""
    base = m.group(1)
    return base.lower() if "SMALL" in nome else base


def _sem_acento(texto: str, idi: str = None) -> str:
    """Tira o sinal, e **conferindo que tirou**.

    **RETRATADO EM 20/10 as 21:0x, e o errado era este helper, nao o portao.**
    A versao anterior era NFD + descartar `Mn`, e isso NAO alcanca letra cujo
    sinal nao decompoe: o `l` com traco do polones (U+0142) sobrevive intacto.
    Medido no `kolejny-poziom-s078`, a primeira peca `pl` cujo orcamento de
    acento e carregado por ele: das 34 letras acentuadas da narracao, **ONZE
    sobreviviam** a "remocao", e o portao — corretamente — nao acusava.

    Logo o teste acusava o portao de CALAR quando o que falhava era a entrada
    dele. **E a familia de 17/10: instrumento que devolve vazio nao prova
    ausencia** — aqui, "o portao nao acusou" nao provava que a narracao estava
    sem acento. O discriminador e barato e agora e obrigatorio: conferir, no
    PROPRIO texto, que nao sobrou nenhuma letra da tabela do idioma.
    """
    saida = "".join(
        c for c in unicodedata.normalize("NFD", texto or "")
        if unicodedata.category(c) != "Mn"
    )
    tabela = (P.DIACRITICOS.get(idi) or "") if idi else ""
    if tabela:
        saida = "".join(_base_da_letra(c) if c in tabela else c for c in saida)
    return saida


def _specs(idioma: str):
    fora = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            with open(p, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        if (sp.get("idioma") or "").split("-")[0] != idioma:
            continue
        if sp.get("short") and sp.get("voz"):
            fora.append((os.path.basename(p), sp))
    return fora


def _roda_o_portao(nome: str, sp: dict):
    """Grava uma spec temporaria e roda o portao DONO da regra."""
    destino = os.path.join(RAIZ, "fabrica", "specs", "zz-teste-acento.json")
    q = json.loads(json.dumps(sp))
    q["slug"] = q["pacote"] = "zz-teste-acento"
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(q, f, ensure_ascii=False)
    try:
        return list(P._gate_ortografia(destino, q) or [])
    finally:
        os.remove(destino)


def test_o_portao_tem_tabela_para_os_CINCO_idiomas_da_frota():
    """`el` entrou em 19/10; sem ele o portao calava no segundo maior idioma."""
    for idi in ("pt", "pl", "tr", "es", "el"):
        assert idi in P.DIACRITICOS, (
            f"`{idi}` saiu de `DIACRITICOS` — o portao volta a CALAR nesse "
            "idioma, que e como o grego ficou descoberto de 20/08 a 19/10"
        )


def test_CONTRAPROVA_o_portao_ACUSA_narracao_sem_acento_nos_tres_idiomas_vivos():
    """A prova chama o DONO da regra, nao reimplementa a densidade."""
    vistos = {}
    for idi in ("pt", "pl", "el"):
        specs = _specs(idi)
        assert specs, f"nenhuma spec de short em `{idi}` no disco"
        nome, sp = specs[-1]
        q = json.loads(json.dumps(sp))
        for c in q["short"]:
            c["nar"] = _sem_acento(c["nar"], idi)
        # CONFERIR a entrada antes de julgar a saida: "o portao nao acusou" nao
        # prova que a narracao esta sem acento (20/10, 21:0x).
        tabela = P.DIACRITICOS.get(idi) or ""
        resto = sorted({c for c in "".join(x["nar"] for x in q["short"])
                        if c in tabela})
        assert not resto, (
            "o helper nao tirou %r da narracao de `%s` (%s): o teste mediria o"
            " PROPRIO stripper em vez do portao" % (resto, idi, nome))
        vistos[idi] = _roda_o_portao(nome, q)
        assert vistos[idi], (
            f"o portao CALOU com a narracao de `{idi}` sem acento ({nome}) — "
            "era exatamente este o buraco do grego"
        )
        assert any("acentua" in str(x) for x in vistos[idi]), vistos[idi]


def test_CONTRAPROVA_no_outro_sentido_a_peca_REAL_passa():
    """Sem este, um portao que acusa sempre passaria."""
    for idi in ("pt", "pl", "el"):
        nome, sp = _specs(idi)[-1]
        assert not _roda_o_portao(nome, sp), (
            f"o portao reprovou a spec REAL de `{idi}` ({nome}) — ele passou a "
            "reprovar o acervo, que e o argumento pelo qual o `mira.py` nao e "
            "portao"
        )


def test_a_entrada_do_GREGO_nao_reprova_NENHUMA_spec_do_acervo():
    """A conta que autorizou ligar: reprova a peca quebrada e nada do parque."""
    specs = _specs("el")
    assert len(specs) >= PISO_DE_SPECS_EL, (
        f"so {len(specs)} specs de short em `el` — abaixo do piso de "
        f"{PISO_DE_SPECS_EL} este teste passa por VACUIDADE"
    )
    tabela = P.DIACRITICOS["el"]
    abaixo = []
    for nome, sp in specs:
        d = P._densidade_diacritica(sp["short"], tabela)
        if d is not None and d < P.PISO_REFERENCIA:
            abaixo.append((nome, round(d * 100, 2)))
    assert not abaixo, (
        "specs gregas do acervo abaixo do piso: " + str(abaixo[:8])
        + " — se isso passar a existir, a entrada do `el` deixa de reprovar so "
          "a peca quebrada e esta nota tem de ser relida"
    )


def test_o_acento_py_DECLARA_que_o_portao_e_o_dono__e_retrata_a_frase():
    """Conserto sem o motivo escrito volta calado — e aqui o motivo e a frase."""
    with open(os.path.join(RAIZ, "fabrica", "acento.py"), encoding="utf-8") as f:
        t = f.read()
    assert "RETRATADO" in t, (
        "a retratacao saiu do modulo; sem ela a frase falsa volta a governar"
    )
    assert "25/08" in t, (
        "saiu a data em que o portao passou a cobrar o short — e ela que prova "
        "que a minha frase era falsa"
    )
    for marca in ("SEGUNDO DONO", "725"):
        assert marca in t, f"saiu do modulo a marca {marca!r}"


def test_o_acento_py_continua_INFORMATIVO_e_nao_virou_portao():
    """Ele cobre os idiomas sem tabela; quem reprova e o `ortografia`."""
    import subprocess

    nome, _ = _specs("pl")[-1]
    alvo = os.path.join(RAIZ, "fabrica", "specs", nome)
    r = subprocess.run(
        [sys.executable, os.path.join(RAIZ, "fabrica", "acento.py"), alvo],
        capture_output=True, text=True, cwd=RAIZ, timeout=600,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "NAO reprova" in r.stdout or "RECUSA" in r.stdout


def test_ele_RECUSA_nos_idiomas_sem_diacritico__em_vez_de_alarmar():
    """A parte do `acento.py` que NAO e duplicata, e ela NAO e cobertura.

    A primeira versao deste teste cobrava uma chave `valores` que o modulo nao
    tem, e reprovou: o teste estava errado, nao o modulo. Corrigido para a
    propriedade que ele de fato carrega, que e melhor do que eu havia escrito —
    nos idiomas sem diacritico ele MEDE e declara que NAO discrimina, com o
    motivo em letra, em vez de alarmar. Alarmar ali seria detector que inventa
    achado (725), e e por isso que o portao nao tem tabela para eles.
    """
    sem_tabela = [i for i in ("id", "hi", "en") if i not in P.DIACRITICOS]
    assert sem_tabela, (
        "a tabela do portao passou a cobrir id/hi/en — releia o papel do "
        "`acento.py`, porque ai ele vira duplicata inteira"
    )
    for idi in sem_tabela:
        d = A.distribuicao(idi)
        assert d and d.get("n"), f"o modulo nao mede `{idi}`: {d}"
        assert d["discrimina"] is False, (
            f"`{idi}` passou a discriminar ({d}) — se o idioma ganhou acento no "
            "acervo, esta nota tem de ser relida"
        )
        assert d.get("motivo") and "725" in d["motivo"], (
            f"o motivo da recusa em `{idi}` perdeu a procedencia: {d}"
        )
    # e nos idiomas COM tabela ele discrimina, senao a recusa seria universal
    for idi in ("pl", "el"):
        d = A.distribuicao(idi)
        assert d["discrimina"] is True, (idi, d)
