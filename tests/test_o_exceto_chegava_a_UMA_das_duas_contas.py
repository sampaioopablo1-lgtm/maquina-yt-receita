# -*- coding: utf-8 -*-
"""O `exceto` chegava a UMA das duas contas, e a que DESEMPATA era a outra.

**Medido em 20/10 as 14:3x.** Em 08:2x o `pauta_do_momento` ganhou `exceto`
porque a spec da PROPRIA rodada ja esta no disco quando eu pergunto, e inflava a
contagem de usos da origem dela. O parametro foi ao DONO daquela conta
(`concentracao.contagem`) e **nunca ao dono da RESERVA**
(`segundo_angulo.nao_mencionados`) — que e exatamente o critetio de DESEMPATE da
regra escrita.

Com a peca desta rodada no disco a reserva do `-5aMrDsxlZE` caiu de **76 para
71** (as mencoes da peca que eu acabara de escrever) e a escolha **TROCOU** para
o `42hpD7eaptE` (73) **mesmo com o `exceto` ligado**. Conserto aplicado a UM de
dois donos nao e conserto.

O que estes testes cobram e PROPRIEDADE: que o `exceto` chegue aos DOIS donos,
que ele valha nas DUAS convencoes de nome (11:3x), e que sem ele a reserva de
fato caia — senao o arquivo nao mede o defeito que o produziu.
"""
import ast
import glob
import inspect
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import segundo_angulo as SA  # noqa: E402
import pauta_do_momento as PM  # noqa: E402
import concentracao as CO  # noqa: E402
import nome_da_spec as NS  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
MOD_SA = os.path.join(RAIZ, "fabrica", "segundo_angulo.py")
MOD_PM = os.path.join(RAIZ, "fabrica", "pauta_do_momento.py")


def _origem_com_irmaos():
    """Uma origem DERIVADA do disco com 2+ shorts e capitulos de sobra.

    Nomear um id seria identidade onde ha propriedade (743/753/761) — e aqui
    seria pior, porque consumir pauta e o trabalho e o id muda toda rodada.
    """
    contagem = {}
    for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        le = sp.get("longo_existente")
        if le and (sp.get("short") or []):
            contagem.setdefault(le, []).append(os.path.basename(p)[:-5])
    for oid, irmaos in sorted(contagem.items(), key=lambda kv: -len(kv[1])):
        d = SA.nao_mencionados(oid, SPECS)
        if d.get("pacote") and len(irmaos) >= 2 and len(d["nao_mencionados"]) > 5:
            return oid, sorted(irmaos), d
    pytest.fail("perdeu a ancora: nenhuma origem do disco tem 2+ shorts com "
                "reserva — o arquivo passaria por vacuidade")


def test_a_varredura_do_disco_nao_esta_vazia():
    oid, irmaos, d = _origem_com_irmaos()
    assert len(irmaos) >= 2 and len(d["nao_mencionados"]) > 5, (oid, irmaos)


def test_nao_mencionados_ACEITA_exceto():
    """O dono da RESERVA tem de receber o parametro — era isso que faltava."""
    assert "exceto" in inspect.signature(SA.nao_mencionados).parameters
    assert "exceto" in inspect.signature(SA.shorts_da_origem).parameters
    # e o outro dono, que ja tinha, continua tendo
    assert "exceto" in inspect.signature(CO.contagem).parameters


def test_o_exceto_MUDA_a_reserva_e_remove_o_irmao():
    """Nos DOIS sentidos: com ele a reserva SOBE e o irmao sai da lista."""
    oid, irmaos, _ = _origem_com_irmaos()
    alvo = irmaos[-1]
    sem = SA.nao_mencionados(oid, SPECS)
    com = SA.nao_mencionados(oid, SPECS, exceto=alvo)
    assert alvo in sem["shorts"], (alvo, sem["shorts"])
    assert alvo not in com["shorts"], (alvo, com["shorts"])
    assert len(com["nao_mencionados"]) >= len(sem["nao_mencionados"]), (
        "excluir um irmao nunca pode ENCOLHER a reserva")


def test_as_DUAS_convencoes_de_nome_concordam():
    """11:3x: `exceto` tinha duas convencoes e errar calava."""
    oid, irmaos, _ = _origem_com_irmaos()
    alvo = irmaos[-1]
    a = SA.nao_mencionados(oid, SPECS, exceto=alvo)
    b = SA.nao_mencionados(oid, SPECS, exceto=NS.arquivo(alvo))
    assert a["shorts"] == b["shorts"]
    assert a["nao_mencionados"] == b["nao_mencionados"]


def test_exceto_que_nao_casa_NAO_filtra_nada():
    """Contraprova no outro sentido: senao bastaria filtrar sempre."""
    oid, irmaos, _ = _origem_com_irmaos()
    sem = SA.nao_mencionados(oid, SPECS)
    for ruim in ("", None, "pacote-que-nao-existe-123"):
        r = SA.nao_mencionados(oid, SPECS, exceto=ruim)
        assert r["shorts"] == sem["shorts"], ruim
        assert r["nao_mencionados"] == sem["nao_mencionados"], ruim


def test_o_pauta_do_momento_passa_o_exceto_aos_DOIS_donos():
    """Por AST: o defeito era de CHAMADOR, nao do dono da reserva."""
    with open(MOD_PM, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "quadro"]
    assert alvo, "o `quadro` mudou de nome"
    donos = {}
    for no in ast.walk(alvo[0]):
        if not isinstance(no, ast.Call):
            continue
        f = no.func
        if isinstance(f, ast.Attribute) and f.attr in ("contagem", "nao_mencionados"):
            donos[f.attr] = any(kw.arg == "exceto" for kw in no.keywords)
    assert donos.get("contagem") is True, "a CONTAGEM perdeu o `exceto`"
    assert donos.get("nao_mencionados") is True, (
        "a RESERVA nao recebe o `exceto` — e ela e o DESEMPATE da regra")


def test_a_escolha_DIVERGE_sem_o_exceto_e_isso_e_o_defeito():
    """Se parar de divergir, o defeito desapareceu e esta nota se rele.

    Cobrado por PROPRIEDADE: existe canal do disco em que a escolha COM e SEM
    `exceto` difere quando se exclui o irmao mais recente daquela origem.
    """
    canais = sorted({os.path.basename(p)[:-5].rsplit("-s", 1)[0]
                     for p in glob.glob(os.path.join(SPECS, "*-s*.json"))})
    divergiu = []
    for canal in canais:
        try:
            base = PM.escolha(canal)
        except Exception:                                   # noqa: BLE001
            continue
        esc = (base.get("escolhida") or {}).get("origem")
        if not esc:
            continue
        irmaos = SA.nao_mencionados(esc, SPECS)["shorts"]
        if not irmaos:
            continue
        com = PM.escolha(canal, exceto=sorted(irmaos)[-1])
        if (com.get("escolhida") or {}).get("reserva") != \
                (base.get("escolhida") or {}).get("reserva"):
            divergiu.append(canal)
    assert divergiu, (
        "nenhum canal do disco muda a RESERVA com o `exceto` — ou o conserto "
        "ficou sem objeto, e ai esta nota se rele, ou o parametro parou de "
        "chegar ao dono da reserva")


def test_o_PONTO_CEGO_do_kicker_repetido_continua_DECLARADO():
    """Ele NAO foi consertado, e o numero que o torna grave e reconferido.

    Numero medido que ninguem reconfere envelhece calado (753), logo o teste
    mede o disco em vez de confiar na prosa.
    """
    import collections
    com_rep = cenas = total = 0
    for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        lg = sp.get("longo") or []
        if len(lg) < SA.MIN_CAPITULOS_PLAUSIVEL:
            continue
        total += 1
        c = collections.Counter(
            (x.get("kicker") or "").strip() for x in lg
            if (x.get("kicker") or "").strip())
        dup = {k for k, v in c.items() if v > 1}
        if dup:
            com_rep += 1
            cenas += sum(c[k] for k in dup)
    assert total >= 50, "varredura curta: %d specs de longo" % total
    assert com_rep > 0 and cenas > 0, (
        "nenhum kicker repetido no disco — o ponto cego perdeu o objeto e a "
        "nota do modulo tem de ser relida")
    fonte = open(MOD_SA, encoding="utf-8").read()
    assert "PONTO CEGO" in fonte and "kicker REPETIDO" in fonte, (
        "o ponto cego saiu do modulo; ele nao foi consertado e tem de ir dito")


def test_o_MOTIVO_continua_escrito_nos_DOIS_modulos():
    for caminho, pedacos in ((MOD_SA, ("14:3x", "DESEMPATE", "76")),
                             (MOD_PM, ("14:3x", "RESERVA", "DESEMPATE"))):
        fonte = open(caminho, encoding="utf-8").read()
        for p in pedacos:
            assert p in fonte, "%s perdeu %r" % (os.path.basename(caminho), p)
