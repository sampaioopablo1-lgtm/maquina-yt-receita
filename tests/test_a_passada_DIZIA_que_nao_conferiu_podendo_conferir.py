# -*- coding: utf-8 -*-
"""A passada de pre-render declarava "NAO aceita rascunho" sobre quem ACEITAVA.

Medido em 21/10 as 23:2x. Dos CINCO instrumentos que o `antes_do_render` dizia
nao ter conferido no rascunho, TRES recebiam dicionario desde que nasceram —
`orcamento_da_copy`, `esqueleto_entre_canais` e `numerais_falados` —, cada um
com UM parametro cujo NOME anunciava aceitar "a spec OU o caminho". **O
despachante decide pela ARIDADE e nao pelo nome** (20/10 as 11:3x), logo a
passada afirmava nao ter conferido podendo conferir: silencio permissivo, a
mesma classe da mira que parou de avisar por seis pecas.

**E custou uma escolha nesta rodada.** Sem a resposta na passada eu fui conferir
a novidade do esqueleto a mao, li uma listagem que o meu proprio `tail -10`
havia CORTADO (as 7 ultimas de 10 formas de treze cenas) e escolhi uma forma que
JA EXISTIA no `epomeno-epipedo`. E a familia da fatia do proxy de 19/10 as
19:2x, agora com o `tail`.
"""
import ast
import importlib
import inspect
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as AR      # noqa: E402
import variedade as V             # noqa: E402

NORMALIZADOS = ("orcamento_da_copy", "esqueleto_entre_canais",
                "numerais_falados")


def _spec_do_disco():
    """Uma spec de short solto REAL, derivada — nomear uma seria identidade."""
    d = os.path.join(RAIZ, "fabrica", "specs")
    for n in sorted(os.listdir(d)):
        if not n.endswith(".json"):
            continue
        sp = json.load(open(os.path.join(d, n), encoding="utf-8"))
        if sp.get("short") and not sp.get("longo") and sp.get("copy"):
            return os.path.join(d, n), sp
    raise AssertionError("nenhuma spec de short solto com copy no disco —"
                         " o arquivo perdeu a ancora")


def _aridade(f):
    ps = [p for p in inspect.signature(f).parameters.values()
          if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    return len(ps)


def test_os_TRES_passaram_a_receber_dicionario():
    for nome in NORMALIZADOS:
        f = importlib.import_module(nome).relato
        assert _aridade(f) >= 2, (
            "%s voltou a UM parametro positional: o despachante decide pela"
            " ARIDADE, logo ele volta a ser declarado como nao conferido"
            % nome)
        ps = list(inspect.signature(f).parameters)
        assert ps[:2] == ["caminho", "spec"], (
            "%s nao segue a convencao (caminho, spec=None): %r" % (nome, ps))


def test_a_resposta_pelo_DICIONARIO_e_identica_a_do_disco():
    """Contraprova no outro sentido: sem isto o rascunho responderia OUTRA coisa."""
    caminho, sp = _spec_do_disco()
    for nome in NORMALIZADOS:
        mod = importlib.import_module(nome)
        assert mod.relato(caminho) == mod.relato(caminho, spec=sp), (
            "%s responde diferente pelo dicionario e pelo disco" % nome)


def test_a_spec_na_PRIMEIRA_posicao_continua_servindo():
    """Compatibilidade: havia chamador passando a spec posicional."""
    _, sp = _spec_do_disco()
    for nome in NORMALIZADOS:
        r = importlib.import_module(nome).relato(sp)
        assert isinstance(r, str) and len(r) > 10, (
            "%s quebrou com a spec na primeira posicao" % nome)


def test_a_LINHA_de_nao_conferido_sai_SO_para_aridade_UM():
    """A propriedade, nao a lista: quem o despachante alcanca nao e declarado.

    Sem esta correspondencia a frase volta a poder mentir nos dois sentidos.
    """
    caminho, sp = _spec_do_disco()
    r = AR.relato(caminho + ".NAO-EXISTE", spec=sp)
    for nome in AR.INSTRUMENTOS:
        f = importlib.import_module(nome).relato
        declarado = ("%s: NAO aceita rascunho" % nome) in r
        assert declarado == (_aridade(f) < 2), (
            "%s: a passada diz 'nao aceita rascunho' = %r e a aridade e %d —"
            " a frase deixou de corresponder a capacidade"
            % (nome, declarado, _aridade(f)))


def test_os_DOIS_lados_existem_e_a_medida_e_RECONFERIDA():
    """Tres passaram a conferir e ao menos um ainda nao — senao a linha perde o
    objeto, e se TODOS aceitarem a nota se rele em vez de o numero ficar."""
    aceitam, exigem = [], []
    for nome in AR.INSTRUMENTOS:
        f = importlib.import_module(nome).relato
        (aceitam if _aridade(f) >= 2 else exigem).append(nome)
    assert len(exigem) >= 1, (
        "TODOS os instrumentos passaram a aceitar rascunho — a linha do 'nao"
        " conferiu' perdeu o objeto e esta nota tem de ser RELIDA")
    assert len(aceitam) >= len(NORMALIZADOS), (
        "menos instrumentos aceitam rascunho do que os tres normalizados: %r"
        % aceitam)
    for nome in NORMALIZADOS:
        assert nome in aceitam, "%s saiu da lista de quem aceita" % nome


def test_a_NOVIDADE_do_esqueleto_e_respondida_no_RASCUNHO():
    """E a pergunta cuja ausencia custou a escolha desta rodada."""
    import esqueleto_entre_canais as EC
    caminho, sp = _spec_do_disco()
    r = EC.relato(caminho + ".NAO-EXISTE", spec=sp)
    assert "desta peca" in r, (
        "o relato nao respondeu a novidade da peca a partir do dicionario")
    assert ("INEDIT" in r) or ("JA EXISTE" in r), (
        "ele respondeu sem dizer se a forma e inedita")


def test_o_exceto_sai_do_NOME_do_arquivo_e_nao_do_disco():
    """Com a peca JA no disco, `exceto` tem de a tirar da varredura.

    Sem isso "inedita" nao poderia ser verdade nunca para uma spec gravada — o
    defeito de 20/10 as 01:3x, e e por isso que o `exceto` existe.
    """
    import esqueleto_entre_canais as EC
    caminho, sp = _spec_do_disco()
    esq = V.esqueleto(sp["short"])
    com = EC.novidade(esq, len(sp["short"]),
                      exceto=os.path.basename(caminho))
    sem = EC.novidade(esq, len(sp["short"]))
    assert sem["exemplares_da_forma"] >= com["exemplares_da_forma"] + 1, (
        "o `exceto` nao retirou a propria peca da contagem: %r contra %r"
        % (com["exemplares_da_forma"], sem["exemplares_da_forma"]))
    assert ("exceto" in inspect.signature(EC.relato).parameters
            or "os.path.basename(caminho)" in io.open(
                os.path.join(RAIZ, "fabrica", "esqueleto_entre_canais.py"),
                encoding="utf-8").read()), (
        "o relato deixou de derivar o `exceto` do nome do arquivo")


def test_NENHUM_decide_pelo_NOME_do_parametro():
    """A licao de 20/10 as 11:3x: nome de parametro nao e convencao.

    Por AST, no despachante: ele nao pode olhar os nomes dos parametros para
    decidir, porque foi assim que `relato(caminho, spec)` estourou no
    `paleta_da_spec`.
    """
    fonte = io.open(os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
                    encoding="utf-8").read()
    arvore = ast.parse(fonte)
    alvo = [n for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef)
            and n.name == "_relato_do_instrumento"]
    assert alvo, "o despachante mudou de nome"
    corpo = ast.unparse(alvo[0])
    assert "'spec' in" not in corpo and '"spec" in' not in corpo, (
        "o despachante voltou a decidir pelo NOME do parametro")
    assert "POSITIONAL" in corpo, (
        "ele deixou de decidir pela ARIDADE (contagem de positionals)")


def test_o_MOTIVO_continua_escrito_nos_tres_modulos():
    for nome in NORMALIZADOS:
        fonte = io.open(os.path.join(RAIZ, "fabrica", nome + ".py"),
                        encoding="utf-8").read()
        assert "ARIDADE" in fonte, (
            "%s deixou de dizer por que a assinatura mudou — sem o motivo a"
            " rodada seguinte volta ao parametro unico" % nome)
