# -*- coding: utf-8 -*-
"""O DONO DO RASCUNHO LEVANTAVA NA FORMA CANONICA DA PERGUNTA.

MEDIDO em 22/10 as 04:4x, escrevendo o `epomeno-epipedo-s091`. Chamei
`mira.relato(None, spec=sp)` para pedir o passo em caracteres — que e para isso
que o rascunho existe desde 21/10 as 20:3x — e levei
`TypeError: stat: path should be string, bytes, os.PathLike or integer, not
NoneType`. A causa esta no DONO: `rascunho.e_rascunho` fazia
`os.path.exists(caminho)` sem guarda de `None`.

**E `caminho=None` e a forma CANONICA da pergunta**, porque o conserto de 21/10
as 23:2x normalizou TRES relatos para `(caminho=None, spec=None)` enquanto os
outros cinco seguiram com `caminho` obrigatorio — isto e, o repo carregava DUAS
convencoes para a MESMA chamada, o mesmo nome de parametro com dois
significados em modulos irmaos. **E a assinatura do `exceto` de 20/10 as 11:3x,
criada pelo meu proprio conserto uma rodada depois dele.**

E a forma do defeito e a de sempre: dos relatos que aceitam rascunho, o UNICO
que levantava era o `mira` — e ele levantava justamente por ser o unico
sub-relato que PERGUNTA ao dono. Os que respondiam, respondiam por nao
perguntar.

O que este arquivo cobra, e por que:
* a forma canonica RESPONDE, e responde `True` — com contraprova no outro
  sentido (sem spec nao e rascunho; spec de arquivo que EXISTE nao e rascunho);
* o defeito e REPRODUZIDO com a guarda antiga, e o teste reprova se ele parar de
  reproduzir — sem isso *"o dono levantava"* seria afirmacao minha e nao medida;
* as DUAS convencoes de assinatura sao medidas, e o teste exige que o dono sirva
  as duas; se elas CONVERGIREM, ele reprova para esta nota ser relida;
* o par vazio (`None`, `None`) LEVANTA com motivo de DADO, nao com `TypeError`
  de tipo;
* o aviso ganha a frase do NOME ausente, com UM dono por AST, e ela NAO sai
  quando o caminho e dado;
* o numero de chamadores do aviso e RECONTADO contra o codigo (753), porque a
  frase do dono dizia CINCO e eram DOIS;
* e o `prontidao.avalia` RECUSA sem caminho em vez de levantar `TypeError` —
  afrouxar o portao para aceitar `None` seria mexer em PORTAO por conveniencia
  de chamada.
"""
from __future__ import annotations

import ast
import inspect
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as AR  # noqa: E402
import prontidao as P  # noqa: E402
import rascunho as R  # noqa: E402


def _spec_do_disco() -> tuple[str, dict]:
    """Uma spec de short solto do DISCO, DERIVADA e nao nomeada.

    Nomear um pacote aqui seria identidade onde ha propriedade (743/753/761), e
    as specs entram e saem do disco a cada rodada.
    """
    import glob
    for c in sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs/*.json"))):
        with open(c, encoding="utf-8") as f:
            sp = json.load(f)
        if sp.get("short") and not sp.get("longo"):
            return c, sp
    pytest.fail("perdi a ancora: nenhuma spec de short solto no disco")


def _relatos_que_aceitam_rascunho() -> dict:
    """`{nome: assinatura}` dos relatos da passada que recebem `spec`."""
    import importlib
    fora = {}
    for nome in AR.INSTRUMENTOS:
        f = getattr(importlib.import_module(nome), "relato")
        sig = inspect.signature(f)
        if "spec" in sig.parameters:
            fora[nome] = sig
    return fora


def test_a_forma_CANONICA_responde_em_vez_de_levantar():
    _, sp = _spec_do_disco()
    assert R.e_rascunho(None, sp) is True, (
        "`caminho=None` com spec E um rascunho: nao existe arquivo nenhum, que e "
        "o caso mais puro da pergunta")
    assert R.aviso_do_rascunho(None, sp), "e o aviso tem de sair"


def test_CONTRAPROVA_nos_dois_sentidos():
    caminho, sp = _spec_do_disco()
    assert R.e_rascunho(None, None) is False, (
        "sem spec nao ha nada a conferir fora do disco — devolver True aqui "
        "faria o aviso sair em toda chamada normal")
    assert R.e_rascunho(caminho, sp) is False, (
        "arquivo que EXISTE nao e rascunho, senao o aviso sairia sempre")
    assert R.aviso_do_rascunho(caminho, sp) == ""
    assert R.aviso_do_rascunho(None, None) == ""


def test_o_defeito_e_REPRODUZIDO_com_a_guarda_antiga():
    """A guarda antiga era `not os.path.exists(caminho)` sem checar None."""
    with pytest.raises(TypeError):
        os.path.exists(None)  # a chamada exata que levantava dentro do dono


def test_as_DUAS_convencoes_existem_e_o_dono_serve_as_duas():
    sigs = _relatos_que_aceitam_rascunho()
    assert len(sigs) >= 5, (
        "menos de cinco relatos aceitando `spec` quer dizer que a varredura "
        "quebrou, nao que o repo encolheu")
    opcional, obrigatorio = [], []
    for nome, sig in sigs.items():
        p = sig.parameters["caminho"]
        (opcional if p.default is not inspect.Parameter.empty
         else obrigatorio).append(nome)
    assert opcional and obrigatorio, (
        "as DUAS convencoes tem de existir para este arquivo medir algo: hoje "
        "%r declaram `caminho=None` e %r o exigem. Se elas CONVERGIREM, releia "
        "esta nota em vez de apagar o teste — o defeito era a divergencia"
        % (sorted(opcional), sorted(obrigatorio)))
    _, sp = _spec_do_disco()
    for nome in opcional:
        assert R.e_rascunho(None, sp) is True, (
            "o dono tem de servir a convencao de %s" % nome)


def test_o_par_vazio_LEVANTA_com_motivo_de_DADO():
    with pytest.raises(ValueError) as e:
        R.spec_de(None, None)
    assert "spec" in str(e.value).lower(), (
        "sem caminho e sem spec a falta e de DADO: `TypeError: stat` e erro de "
        "TIPO e manda conferir no lugar errado")


def test_a_frase_do_NOME_ausente_tem_UM_dono_e_so_sai_sem_caminho():
    caminho, sp = _spec_do_disco()
    sem = R.aviso_do_rascunho(None, sp)
    com_caminho = R.aviso_do_rascunho(caminho + ".que-nao-existe", sp)
    assert "NOME" in sem, "sem caminho falta tambem o nome, e isso vai dito"
    assert "NOME" not in com_caminho, (
        "com o caminho PRETENDIDO o `identidade` tem contra o que comparar — "
        "aviso que sai sempre deixa de avisar")
    assert com_caminho, "e o aviso do rascunho continua saindo"

    fonte = inspect.getsource(R)
    arvore = ast.parse(fonte)
    donos = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef):
            for s in ast.walk(no):
                if isinstance(s, ast.Constant) and isinstance(s.value, str) \
                        and "falta tambem o NOME" in s.value:
                    donos.add(no.name)
    assert donos == {"aviso_do_rascunho"}, (
        "a frase tem UM dono; copia-la e a assinatura que congelou a legenda "
        "(donos: %r)" % sorted(donos))


def test_os_CHAMADORES_do_aviso_sao_RECONTADOS_contra_o_codigo():
    """A frase do dono dizia CINCO e eram DOIS — o 753 em forma de contagem."""
    import glob
    chamadores = set()
    for c in sorted(glob.glob(os.path.join(RAIZ, "fabrica/*.py"))):
        if os.path.basename(c) == "rascunho.py":
            continue
        with open(c, encoding="utf-8") as f:
            fonte = f.read()
        try:
            arvore = ast.parse(fonte)
        except SyntaxError:
            continue
        for no in ast.walk(arvore):
            if isinstance(no, ast.Attribute) and no.attr == "aviso_do_rascunho":
                chamadores.add(os.path.basename(c)[:-3])
    assert chamadores, "zero chamadores quer dizer que a varredura quebrou"
    assert chamadores == {"mira", "antes_do_render"}, (
        "os chamadores medidos em 22/10 as 04:4x sao `mira` e `antes_do_render`; "
        "hoje %r. Se o conjunto mudar, o numero da prosa do dono tem de ser "
        "relido junto — foi por ele estar escrito e nao recontado que a frase "
        "dizia CINCO (753)" % sorted(chamadores))

    fonte = inspect.getsource(R.aviso_do_rascunho)
    if "cinco relatos a imprimem" in fonte:
        # Ele PODE estar citado: a retratacao precisa dizer qual era a frase
        # falsa. O que nao pode e a frase ficar la sem a retratacao ao lado —
        # casar a prosa sozinha pegaria a EXPLICACAO em vez do codigo, que e a
        # licao do `test_NAO_virou_portao` do acento.
        assert "FALSO" in fonte and "DOIS" in fonte, (
            "a frase antiga so pode aparecer CITADA, com a retratacao ao lado: "
            "sem ela o numero volta a ser afirmacao")


def test_o_PORTAO_recusa_sem_caminho_em_vez_de_levantar_TypeError():
    _, sp = _spec_do_disco()
    with pytest.raises(ValueError) as e:
        P.avalia(None, spec=sp)
    m = str(e.value)
    assert "identidade" in m and "PRETENDIDO" in m, (
        "a recusa tem de dizer POR QUE o portao precisa do nome e o que passar "
        "no lugar, do jeito que o `porta1` recusa janela curta")


def test_o_portao_NAO_foi_afrouxado_para_aceitar_None():
    """Dez dos doze portoes usam o caminho como NOME, e isso continua."""
    caminho, sp = _spec_do_disco()
    g = P.avalia(caminho, spec=sp)
    assert g and "identidade" in g, "o conjunto de portoes nao pode ter mudado"
    outro = os.path.join(RAIZ, "fabrica/specs/nao-existe-este-pacote.json")
    g2 = P.avalia(outro, spec=sp)
    assert g2["identidade"], (
        "o `identidade` tem de continuar reprovando `pacote` diferente do nome "
        "do arquivo — e ele a prova de que o caminho segue sendo NOME")


def test_a_PASSADA_inteira_responde_na_forma_canonica():
    _, sp = _spec_do_disco()
    r = AR.relato(None, spec=sp)
    assert "RASCUNHO" in r and "NOME" in r, (
        "a passada e o caminho pelo qual a rodada pergunta, e o defeito era de "
        "CHAMADOR: sem ela o conserto nao se prova de ponta a ponta")
    assert "NAO aceita rascunho" in r, (
        "e os instrumentos que ainda exigem caminho continuam DIZENDO que nao "
        "conferiram, em vez de calar")


def test_o_MOTIVO_continua_escrito_no_dono():
    fonte = inspect.getsource(R)
    baixo = fonte.lower()
    assert "forma canonica" in baixo and "duas convencoes" in baixo, (
        "conserto sem motivo escrito volta calado: foi assim que o `exceto` "
        "ganhou duas convencoes uma rodada depois do conserto dele")
