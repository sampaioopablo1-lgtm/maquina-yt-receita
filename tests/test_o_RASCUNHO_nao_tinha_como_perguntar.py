# -*- coding: utf-8 -*-
"""O rascunho nao tinha como perguntar — 21/10 as 20:3x.

A peca se escreve num construtor que vive FORA do repo, e o comprimento da
narracao se acerta por iteracao: escreve, mede, move caracteres, mede outra vez.
Nessa iteracao a spec existe **so na memoria** — e de SEIS relatos da passada de
pre-render apenas UM aceitava dicionario.

A capacidade existia uma camada abaixo: `mira.quanto_cortar` e `mira.orcamento`
recebem dicionario, e DEZ dos DOZE portoes do `prontidao` nao abrem o arquivo
(recebem `sp` do despachante; o caminho so serve de NOME).

CUSTO MEDIDO nesta rodada: movi o comprimento em QUATRO builds, calculando
"~0,57 s por caractere" de cabeca, e PASSEI DO PONTO — previsao em 41,19 s
contra um piso de 41,5. O `quanto_cortar` devolve esse passo pronto.
"""
import ast
import inspect
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as AR     # noqa: E402
import prontidao                 # noqa: E402
import rascunho                  # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
# OS CINCO QUE ACEITAVAM RASCUNHO EM 21/10 AS 20:3x — fica como HISTORIA, porque
# e ela que explica o arquivo. **Nao se usa para decidir quem aceita:** em 23:2x
# outros TRES foram normalizados e esta tupla ficou atras, fazendo o teste da
# frase cobrar "nao conferiu" de quem passou a conferir. Identidade onde havia
# propriedade (743/753/761), e a propriedade e a ARIDADE — a mesma pela qual o
# despachante decide.
RELATOS_EM_20H = ("mira", "acento", "gancho", "layouts_do_short",
                  "paleta_da_spec")


def _aceita_rascunho(nome):
    """Quem o despachante alcanca: `relato` com DOIS positionals ou mais."""
    import importlib
    ps = [p for p in inspect.signature(
        importlib.import_module(nome).relato).parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    return len(ps) >= 2


RELATOS = tuple(n for n in RELATOS_EM_20H if _aceita_rascunho(n))
INEXISTENTE = os.path.join(SPECS, "nao-existe-ainda-neste-teste.json")


def _uma_spec():
    """Uma spec de short solto do disco, DERIVADA — nomear uma seria identidade
    onde ha propriedade (743/753/761), e a peca da rodada muda."""
    import glob
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json")), reverse=True):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("short") and not d.get("longo") and d.get("copy"):
            return f, d
    raise AssertionError("nenhuma spec de short solto com copy no disco")


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def test_os_CINCO_relatos_aceitam_dicionario():
    for nome in RELATOS:
        mod = __import__(nome)
        ps = list(inspect.signature(mod.relato).parameters.values())
        posicionais = [x for x in ps
                       if x.kind in (x.POSITIONAL_ONLY, x.POSITIONAL_OR_KEYWORD)]
        assert len(posicionais) >= 2, (
            "%s.relato aceita %d posicional(is) — o rascunho nao tem como "
            "perguntar a ele" % (nome, len(posicionais)))


def test_o_relato_do_RASCUNHO_bate_com_o_do_DISCO():
    """Contraprova no outro sentido: o dicionario nao pode mudar a resposta."""
    caminho, sp = _uma_spec()
    for nome in RELATOS:
        mod = __import__(nome)
        do_disco = mod.relato(caminho)
        do_dict = mod.relato(caminho, sp)
        assert do_disco == do_dict, (
            "%s responde DIFERENTE para o mesmo conteudo vindo do disco e do "
            "dicionario" % nome)


def test_o_aviso_do_rascunho_SAI_quando_o_arquivo_nao_existe():
    _caminho, sp = _uma_spec()
    r = AR.relato(INEXISTENTE, sp)
    assert "RASCUNHO" in r, (
        "a passada nao avisa que o arquivo nao esta no disco:\n%s" % r[:400])
    for marca in ("similaridade", "variedade", "identidade"):
        assert marca in r, (
            "o aviso nao NOMEIA o %s, que varre o acervo e nao ve esta peca"
            % marca)


def test_com_o_arquivo_no_DISCO_o_aviso_NAO_sai():
    """Sem este, bastaria avisar sempre — e aviso que sempre sai nao avisa."""
    caminho, sp = _uma_spec()
    assert "RASCUNHO:" not in AR.relato(caminho, sp)
    assert "RASCUNHO:" not in AR.relato(caminho)


def test_o_aviso_tem_UM_dono():
    arv = ast.parse(open(rascunho.__file__, encoding="utf-8").read())
    donos = [n.name for n in ast.walk(arv)
             if isinstance(n, ast.FunctionDef) and "RASCUNHO:" in _codigo(n)]
    assert donos == ["aviso_do_rascunho"], (
        "a frase do rascunho tem %d donos (%s)" % (len(donos), donos))
    for nome in ("mira", "antes_do_render"):
        fonte = open(__import__(nome).__file__, encoding="utf-8").read()
        assert "RASCUNHO: o arquivo" not in fonte, (
            "%s reescreveu a frase do rascunho em vez de a chamar" % nome)


def test_o_mira_imprime_o_aviso_nos_DOIS_ramos():
    """O `relato` do `mira` tem dois `return`, e o ramo do canal sem mira sai
    ANTES — foi nele que o orcamento ficou morto em 19/10 as 15:2x, e a primeira
    versao deste aviso repetiu o erro na MESMA funcao."""
    import glob
    import mira
    import ensaio
    com, sem = None, None
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("short") or d.get("longo"):
            continue
        if d.get("voz") not in ensaio.MODELO_VOZ:
            continue
        canal = mira.canal_da_spec(d)
        if canal in ensaio.ALVO_POR_CANAL and com is None:
            com = d
        elif canal not in ensaio.ALVO_POR_CANAL and sem is None:
            sem = d
        if com and sem:
            break
    assert com and sem, (
        "o disco nao tem os DOIS casos (canal com mira propria e sem) — sem "
        "eles este teste nao mede o ramo que saia antes do aviso")
    for d in (com, sem):
        r = mira.relato(INEXISTENTE, d)
        assert "RASCUNHO" in r, (
            "o aviso nao sai no ramo de %s:\n%s" % (d.get("pacote"), r[-300:]))


def test_os_PORTOES_rodam_sobre_o_dicionario_e_dao_o_MESMO_veredito():
    caminho, sp = _uma_spec()
    a = prontidao.avalia(caminho, sp)
    b = prontidao.avalia(caminho)
    assert a == b, "o veredito dos portoes mudou com a spec vinda do dicionario"
    assert len(a) >= 10, "so %d portoes rodaram" % len(a)


def test_DEZ_dos_DOZE_portoes_nao_abrem_o_arquivo():
    """A medida que torna o conserto possivel, RECONFERIDA contra o codigo
    (753): se os portoes passarem a reler o arquivo, o rascunho morre."""
    arv = ast.parse(open(prontidao.__file__, encoding="utf-8").read())
    gates = [n for n in ast.walk(arv)
             if isinstance(n, ast.FunctionDef) and n.name.startswith("_gate_")]
    assert len(gates) >= 12, "so %d portoes" % len(gates)
    abrem = [n.name for n in gates
             if "open(caminho" in _codigo(n) or "json.load(open(caminho"
             in _codigo(n)]
    assert len(abrem) <= 1, (
        "%d portoes releem o arquivo que o despachante ja carregou: %s"
        % (len(abrem), abrem))
    assert "_gate_narracao" not in abrem, (
        "o `_gate_narracao` voltou a reler o arquivo — era ele o segundo dono")


def test_o_despachante_decide_pela_ARIDADE_e_nao_pelo_NOME():
    """O `paleta_da_spec.relato` nasceu como `relato(spec)`: parametro chamado
    'spec' na PRIMEIRA posicao. Decidir pelo nome fazia a chamada levantar."""
    arv = ast.parse(open(AR.__file__, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)
            and n.name == "_relato_do_instrumento"]
    assert alvo, "`_relato_do_instrumento` desapareceu"
    codigo = _codigo(alvo[0])
    # O `ast.unparse` NORMALIZA a aspa para simples, logo casar `"spec" in`
    # (como eu escrevi na primeira versao) nunca casa e o assert passava com o
    # defeito religado. Pego pela propria contraprova desta rodada.
    assert "'spec' in" not in codigo, (
        "o despachante voltou a decidir pelo NOME do parametro")
    assert "kind" in codigo, (
        "ele nao olha mais a KIND dos parametros — a aridade e o critério")
    _c, sp = _uma_spec()
    r = AR.relato(INEXISTENTE, sp)
    assert "AMBIENTE" not in r, (
        "algum instrumento levantou na passada do rascunho:\n%s"
        % "\n".join(l for l in r.splitlines() if "AMBIENTE" in l))


def test_instrumento_que_NAO_aceita_rascunho_DIZ_que_nao_conferiu():
    """Calar seria o sentido permissivo — custou seis pecas da s077 a s082."""
    _c, sp = _uma_spec()
    r = AR.relato(INEXISTENTE, sp)
    faltam = [n for n in AR.INSTRUMENTOS if not _aceita_rascunho(n)]
    assert faltam, (
        "todos os instrumentos aceitam rascunho — esta nota se rele, porque a "
        "linha do 'NAO aceita rascunho' perdeu o objeto")
    for n in faltam:
        assert "%s: NAO aceita rascunho" % n in r, (
            "o %s calou no rascunho em vez de dizer que nao conferiu" % n)


def test_spec_VAZIA_e_nao_dicionario_LEVANTAM():
    import pytest
    with pytest.raises(ValueError):
        rascunho.spec_de("x", {})
    with pytest.raises(TypeError):
        rascunho.spec_de("x", "nao sou dicionario")


def test_o_motivo_continua_escrito():
    fonte = open(rascunho.__file__, encoding="utf-8").read()
    for marca in ("41,19", "41,5", "quanto_cortar", "DEZ dos DOZE"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo — sem ela a rodada seguinte volta "
            "a mover caracteres de cabeca" % marca)
