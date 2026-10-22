# -*- coding: utf-8 -*-
"""A RESERVA QUE DESEMPATA VINHA INFLADA PELO CAPITULO QUE O IRMAO DECLARA.

Medido em 22/10 as 17:3x, escrevendo o `labtreinamento-s110`. A regra escrita no
`concentracao.py` e *"MENOR contagem com capitulos intocados, desempate pela
MAIOR reserva"*, e o `pauta_do_momento` lia a reserva CRUA do
`segundo_angulo.nao_mencionados`. Desde 22/10 as 12:3x esta MEDIDO que capitulo
que o irmao DECLARA sai como livre, porque o `nao_mencionados` casa o TEXTO do
kicker e a copy declara FAIXA em digitos — logo a reserva que DESEMPATA vinha
inflada, e o `relato` marcava os declarados sem que o desempate os descontasse.

**E a inversao foi maxima na primeira medicao:** dos cinco empatados em 6 usos do
`labtreinamento`, a reserva crua escolhia a origem de 40 livres com so 14 sem
declaracao, contra uma de 38 livres com 37 sem declaracao.

E a classe e a de 20/10 as 14:3x — *"o `exceto` chegava a UMA das duas contas, e
a que desempata era a outra"*: conserto aplicado a UM de dois donos nao e
conserto. Aqui o conserto de 12:3x chegou ao RELATO e nao ao DESEMPATE.

O que este arquivo cobra, e por que nada aqui e identidade:
  * a divergencia e cobrada como PROPRIEDADE sobre o disco, nos DOIS lados — ha
    canal em que as duas leituras divergem e ha canal em que concordam —, e
    **reprova se TODOS divergirem ou se NENHUM divergir**, porque nos dois casos
    a nota tem de ser relida em vez de o numero ser movido (743/753/761);
  * a juncao e DELEGADA ao `texto_dos_livres`, dono dela desde 12:3x, cobrado por
    AST: refazer a juncao no `quadro` seria o segundo dono;
  * a `escolhida` NAO muda — contraprova no outro sentido, senao "nomear" teria
    virado "filtrar";
  * a frase tem UM dono e sai nos TRES ramos, e o `relato` a chama FORA do ramo
    do empate — que e o defeito de 20/10 as 13:2x, a nota que morava no ramo que
    para de disparar quando ela importa.
"""
import ast
import inspect
import io
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao as CO          # noqa: E402
import pauta_do_momento as PM      # noqa: E402
import segundo_angulo as SA        # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")
PISO_ORIGENS = 8          # guarda de vacuidade: quadro curto nao mede nada
PISO_CANAIS_COM_EMPATE = 1

# HISTORIA, e nenhum assert depende dela: os ids e os numeros mudam com a pauta,
# e consumir pauta e o trabalho (18/10 as 09:2x).
MEDIDA_DE_17H = {
    "canal": "labtreinamento",
    "crua": ("labtreinamento-014", 40, 14),
    "sem_declaracao": ("labtreinamento-010", 38, 37),
    "divergiram": 1,
    "concordaram": 2,
}


def _fonte(fn):
    """`textwrap.dedent`, nunca `inspect.cleandoc`.

    O `cleandoc` desindenta a linha do `def` e deixa o corpo torto — custou dois
    testes em 22/10 as 08:3x.
    """
    return textwrap.dedent(inspect.getsource(fn))


def _corpo(mod, nome):
    arv = ast.parse(io.open(mod.__file__, encoding="utf-8").read())
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    raise AssertionError("funcao %r nao existe em %s" % (nome, mod.__file__))


@pytest.fixture(scope="module")
def quadros():
    q = {c: PM.quadro(c) for c in CANAIS}
    for c, linhas in q.items():
        assert len(linhas) >= PISO_ORIGENS, (
            "o quadro de %s tem %d origens, abaixo do piso de %d — com quadro "
            "curto este arquivo passa por VACUIDADE e nao mede nada"
            % (c, len(linhas), PISO_ORIGENS))
    return q


@pytest.fixture(scope="module")
def escolhas():
    return {c: PM.escolha(c) for c in CANAIS}


def test_o_quadro_traz_a_reserva_SEM_DECLARACAO(quadros):
    for canal, linhas in quadros.items():
        com = [x for x in linhas if x["pacote"]]
        assert com, "nenhuma origem de %s tem spec local" % canal
        for x in com:
            sd = x["reserva_sem_declaracao"]
            assert isinstance(sd, int), (
                "%s: a reserva sem declaracao tem de ser um numero, e veio %r"
                % (x["origem"], sd))
            assert 0 <= sd <= x["reserva"], (
                "%s: sem declaracao %d fora de [0, %d] — descontar declarado "
                "nunca pode somar" % (x["origem"], sd, x["reserva"]))


def test_origem_SEM_spec_local_devolve_None_e_nao_zero(quadros):
    """Vazio de instrumento nao e zero medido (17/10)."""
    vistos = 0
    for linhas in quadros.values():
        for x in linhas:
            if x["sem_spec_local"]:
                vistos += 1
                assert x["reserva_sem_declaracao"] is None, (
                    "%s nao tem spec local (regra h), logo a reserva nao se "
                    "separa entre declarada e livre — e isso e None, nunca 0"
                    % x["origem"])
    assert vistos, ("nenhuma origem sem spec local no disco: sem ela este teste "
                    "passa por vacuidade e a distincao None/0 nao e medida")


def test_a_divergencia_EXISTE_e_nao_e_universal(escolhas):
    """Os DOIS lados, e reprova se todos ou nenhum divergirem."""
    com_empate = {c: e for c, e in escolhas.items()
                  if len(e["empatados_na_contagem"]) > 1}
    assert len(com_empate) >= PISO_CANAIS_COM_EMPATE, (
        "nenhum canal tem empate de usos: sem empate o desempate nao decide "
        "nada e este arquivo nao mede o defeito que o produziu")
    div = [c for c, e in com_empate.items() if e["desempate_diverge"]]
    igual = [c for c, e in com_empate.items() if not e["desempate_diverge"]]
    assert div or igual
    if not div:
        pytest.fail(
            "nenhum canal com empate DIVERGE mais (%s) — o defeito medido em "
            "22/10 as 17:3x desapareceu, e esta nota tem de ser RELIDA em vez "
            "de o numero ser movido" % ", ".join(sorted(com_empate)))
    if not igual and len(com_empate) > 1:
        pytest.fail(
            "TODOS os canais com empate divergem (%s) — sem o lado contrario a "
            "divergencia nao distingue nada, e a nota se rele"
            % ", ".join(sorted(div)))


def test_onde_DIVERGE_a_crua_escolhe_a_de_MENOS_capitulo_livre(escolhas):
    """A inversao e o que torna o achado grave, e ela e RECONFERIDA."""
    houve = 0
    for canal, e in escolhas.items():
        if not e["desempate_diverge"]:
            continue
        houve += 1
        crua = e["escolhida"]
        sem = e["escolhida_por_reserva_sem_declaracao"]
        assert crua["reserva"] >= sem["reserva"], (
            "%s: a crua tem de ganhar pela reserva CRUA, senao ela nao a "
            "escolheu" % canal)
        assert sem["reserva_sem_declaracao"] > crua["reserva_sem_declaracao"], (
            "%s: a divergencia so e divergencia se a outra tiver MAIS capitulo "
            "sem declaracao (%d contra %d)"
            % (canal, sem["reserva_sem_declaracao"],
               crua["reserva_sem_declaracao"]))
    assert houve, "nenhum canal divergiu — ja coberto pelo teste dos dois lados"


def test_a_juncao_e_DELEGADA_ao_texto_dos_livres(quadros):
    """Refazer a juncao no `quadro` seria o SEGUNDO dono dela (12:3x)."""
    f = _corpo(PM, "quadro")
    chamadas = {n.func.attr for n in ast.walk(f)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    assert "texto_dos_livres" in chamadas, (
        "o `quadro` tem de pedir a juncao ao dono dela (`texto_dos_livres`)")
    for proibida in ("declarados_pelos_irmaos", "capitulos_do_pacote"):
        assert proibida not in chamadas, (
            "o `quadro` chama %r: refazer a juncao capitulo-livre x faixa "
            "declarada aqui e o segundo dono, a assinatura que congelou a "
            "legenda" % proibida)
    fonte = _fonte(PM.quadro)
    assert "por_indice" not in fonte, (
        "`por_indice` no corpo do `quadro`: a juncao voltou a ser refeita aqui")


def test_a_escolhida_NAO_muda_pela_leitura_nova(escolhas, quadros):
    """Contraprova no outro sentido: NOMEAR nao e FILTRAR."""
    for canal, e in escolhas.items():
        esc = e["escolhida"]
        if not esc:
            continue
        servem = [x for x in quadros[canal]
                  if not x["suspeito_de_outro_canal"] and x["reserva"] > 0]
        pela_regra = sorted(servem,
                            key=lambda x: (x["usos"], -x["reserva"],
                                           x["origem"]))[0]
        assert esc["origem"] == pela_regra["origem"], (
            "%s: a `escolhida` deixou de seguir a regra ESCRITA do "
            "`concentracao.py` — a leitura nova passou a FILTRAR em vez de "
            "NOMEAR, e a regra nao e minha de mudar" % canal)
        # e a origem nomeada pela outra leitura NAO sai da lista
        s = e["escolhida_por_reserva_sem_declaracao"]
        if s:
            assert any(x["origem"] == s["origem"] for x in quadros[canal]), (
                "%s: a origem nomeada pela reserva sem declaracao saiu do "
                "quadro — nomear nao tira ninguem da lista" % canal)


def test_a_frase_tem_UM_dono_e_sai_nos_TRES_ramos():
    assert hasattr(PM, "_linha_do_desempate")
    marca = "DESEMPATE pela reserva SEM DECLARACAO"
    arv = ast.parse(io.open(PM.__file__, encoding="utf-8").read())
    fora = []
    for n in arv.body:
        if not isinstance(n, ast.FunctionDef) or n.name == "_linha_do_desempate":
            continue
        for s in ast.walk(n):
            if isinstance(s, ast.Constant) and isinstance(s.value, str) \
                    and marca in s.value:
                fora.append(n.name)
    assert not fora, (
        "a marca %r aparece fora do dono, em %s — a frase do teto nasceu "
        "duplicada em outro modulo e foi isso que a fez divergir (753)"
        % (marca, sorted(set(fora))))
    # os TRES ramos: sem empate, empate que concorda, empate que diverge.
    base = {"escolhida": {"origem": "A", "pacote": "pa", "reserva": 40,
                          "reserva_sem_declaracao": 14},
            "escolhida_por_reserva_sem_declaracao":
                {"origem": "B", "pacote": "pb", "reserva": 38,
                 "reserva_sem_declaracao": 37}}
    sem_empate = dict(base, empatados_na_contagem=["A"], desempate_diverge=False)
    concorda = dict(base, empatados_na_contagem=["A", "B"],
                    desempate_diverge=False)
    diverge = dict(base, empatados_na_contagem=["A", "B"],
                   desempate_diverge=True)
    t1 = PM._linha_do_desempate(sem_empate)
    t2 = PM._linha_do_desempate(concorda)
    t3 = PM._linha_do_desempate(diverge)
    for t in (t1, t2, t3):
        assert marca in t, "a frase tem de sair nos TRES ramos: %r" % t
    assert len({t1, t2, t3}) == 3, (
        "os tres ramos devolvem a MESMA frase, logo ela nao distingue nada")
    assert "DIVERGEM" in t3 and "DIVERGEM" not in t2, (
        "o ramo da divergencia tem de se distinguir do ramo do acordo")
    assert "pb" in t3 and "37" in t3 and "14" in t3, (
        "o ramo da divergencia tem de NOMEAR a outra origem e os DOIS numeros")
    # e sem a outra leitura ele RECUSA, em vez de calar
    recusa = PM._linha_do_desempate(
        dict(base, empatados_na_contagem=["A", "B"],
             escolhida_por_reserva_sem_declaracao=None,
             desempate_diverge=False))
    assert marca in recusa and "nao ha como medir" in recusa


def test_o_relato_a_CHAMA_fora_do_ramo_do_EMPATE():
    """O defeito de 20/10 as 13:2x: nota no ramo que para de disparar."""
    f = _corpo(PM, "relato")
    chamadas = [n for n in ast.walk(f)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "_linha_do_desempate"]
    assert chamadas, "o `relato` nao chama a frase — import sem chamada e a " \
                     "classe dos layouts mortos"
    dentro = []
    for n in ast.walk(f):
        if not isinstance(n, ast.If):
            continue
        teste = ast.dump(n.test)
        if "empatados_na_contagem" not in teste:
            continue
        for s in ast.walk(n):
            if s in chamadas:
                dentro.append(teste)
    assert not dentro, (
        "a frase do desempate esta DENTRO do ramo do empate: ela precisa sair "
        "tambem quando nao houve empate, senao e a nota que mora no ramo que "
        "cala (20/10, 13:2x)")


def test_o_exceto_chega_a_CONTA_NOVA_tambem(quadros):
    """A licao de 20/10 as 14:3x, aplicada a terceira conta."""
    canal = "labtreinamento"
    alvo = next((x for x in quadros[canal]
                 if x["pacote"] and x["reserva_sem_declaracao"]), None)
    assert alvo, "perdi a ancora: nenhuma origem de %s com spec local e " \
                 "reserva sem declaracao" % canal
    irmaos = SA.shorts_da_origem(alvo["origem"])
    # `shorts_da_origem` devolve (pacote, copy): o nome e o primeiro item, e
    # supor dicionario aqui era suposicao minha sobre a forma do retorno alheio.
    nomes = [s[0] if isinstance(s, (tuple, list)) else s for s in irmaos]
    nomes = [n for n in nomes if isinstance(n, str)]
    assert nomes, "perdi a ancora: a origem %s nao tem irmao no disco" \
                  % alvo["origem"]
    com = PM.quadro(canal, exceto=nomes[0])
    linha = next(x for x in com if x["origem"] == alvo["origem"])
    assert linha["reserva_sem_declaracao"] is not None, (
        "com `exceto` a conta nova devolveu None: o parametro nao chegou a ela")
    assert linha["reserva_sem_declaracao"] >= alvo["reserva_sem_declaracao"], (
        "tirar um irmao da varredura nao pode REDUZIR o que sobra sem "
        "declaracao (%d contra %d) — e sinal de que o `exceto` chegou a uma "
        "conta e nao a outra, que e exatamente o defeito de 20/10 as 14:3x"
        % (linha["reserva_sem_declaracao"], alvo["reserva_sem_declaracao"]))


def test_a_medida_e_o_MOTIVO_continuam_escritos():
    fonte = io.open(PM.__file__, encoding="utf-8").read()
    for pedaco in ("17:3x", "12:3x", "14:3x", "sem declaracao"):
        assert pedaco in fonte, (
            "o modulo perdeu %r: conserto sem motivo escrito volta calado"
            % pedaco)
    # a propriedade e a presenca da frase, nao a caixa dela: o modulo escreve
    # `NAO` em caixa alta de proposito, e cobrar a caixa seria casar prosa.
    doc = " ".join((PM._linha_do_desempate.__doc__ or "").split()).lower()
    assert "nao e veredito nos dois sentidos" in doc, (
        "o docstring tem de dizer que declaracao em prosa NAO e veredito nos "
        "dois sentidos — e por isso que a `escolhida` nao troca")
