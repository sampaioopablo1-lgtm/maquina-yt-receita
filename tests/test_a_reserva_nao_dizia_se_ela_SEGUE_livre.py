# -*- coding: utf-8 -*-
"""A reserva escrita nao dizia se ela SEGUE livre — e so agora podia dizer.

**21/10 as 13:1x.** O docstring do `reservas_escritas` manda, desde que ele
nasceu, perguntar ao `segundo_angulo` se a reserva continua livre — e o
`segundo_angulo` **nao podia responder**, porque o proprio bloco de reserva
fazia o capitulo contar como MENCIONADO (medido em 20/10 as 12:4x). A remissao
era circular, e o conserto daquela rodada e o que destrava esta pergunta.

E ela custava uma rodada: para saber que a reserva do `epomeno-epipedo-s020` ja
havia sido consumida pelo `-s036`, eu li os quatro irmaos da origem um por um.

A forma destes testes: tudo sai do DISCO e por PROPRIEDADE, com guarda de
vacuidade — e a convencao do INDICE do capitulo e RECONFERIDA contra o disco em
vez de confiada a prosa do modulo (753).
"""
import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import reservas_escritas as RE    # noqa: E402
import segundo_angulo as SA       # noqa: E402


def _codigo(no):
    """O corpo da funcao SEM o docstring — ele CITA os donos para se explicar."""
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _defs(arquivo):
    fonte = open(os.path.join(RAIZ, "fabrica", arquivo), encoding="utf-8").read()
    return {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}, fonte


def test_a_varredura_nao_e_vacua():
    e = RE.estado()
    assert len(e) >= 15, (
        "so %d reserva(s) no acervo: os testes abaixo passariam por vacuidade"
        % len(e))
    assert all("veredito" in x for x in e), "alguma reserva saiu sem veredito"


def test_os_DOIS_lados_existem():
    """Sem os dois, 'ele decide' passaria devolvendo sempre a mesma coisa."""
    v = [x["veredito"] for x in RE.estado()]
    decidiveis = [x for x in v if x != "indeterminada"]
    assert decidiveis, (
        "PERDEU A ANCORA: nenhuma reserva do disco e decidivel, logo o"
        " instrumento recusa sempre e nao mede nada")
    assert "indeterminada" in v, (
        "nenhuma reserva INDETERMINADA no disco: era justamente a classe desta"
        " rodada (reserva que descreve o capitulo em prosa), e sem ela o ramo"
        " da RECUSA nao e exercitado")
    assert len(set(decidiveis)) >= 2, (
        "os decidiveis convergiram para um valor so (%r): o veredito deixou de"
        " discriminar" % set(decidiveis))


def test_a_BASE_do_indice_e_reconferida_contra_o_disco():
    """A convencao e MEDIDA: o indice citado na prosa conta de ZERO.

    Se ela mudar, este teste reprova em vez de o instrumento apontar capitulo
    errado em silencio — que e a falha permissiva de sempre.
    """
    casados = 0
    for e in RE.estado():
        if e["veredito"] == "indeterminada" or not e["kickers"]:
            continue
        pacote = e["pacote_da_origem"]
        caps = SA.capitulos_do_pacote(pacote)
        i = [x for x in e["capitulos"] if x < len(caps)][0]
        assert caps[i - RE.BASE_DO_INDICE] in e["kickers"], (
            "a reserva de %s cita o capitulo %d e o kicker na base %d nao esta"
            " entre os que o instrumento resolveu (%r)"
            % (e["pacote"], i, RE.BASE_DO_INDICE, e["kickers"][:3]))
        casados += 1
    assert casados >= 5, (
        "so %d reserva(s) com indice resolvido: a reconferencia da convencao"
        " ficou fraca demais para valer" % casados)


def test_o_veredito_concorda_com_o_dono_da_mencao():
    """Contraprova: quem decide mencao e o `segundo_angulo`, nao este modulo."""
    for e in RE.estado():
        if e["veredito"] == "indeterminada":
            continue
        d = SA.nao_mencionados(e["origem"])
        nao = set(d["nao_mencionados"])
        for k in e["livres"]:
            assert k in nao, (
                "%r saiu como LIVRE e o `segundo_angulo` o da como mencionado"
                % k)
        for k in e["mencionados"]:
            assert k not in nao, (
                "%r saiu como mencionado e o `segundo_angulo` o da como livre"
                % k)


def test_o_veredito_SAI_no_relato_e_tem_UM_dono():
    """Instrumento que o relato nao imprime e a classe dos layouts mortos."""
    alvo = [e for e in RE.estado() if e["veredito"] != "indeterminada"]
    assert alvo, "PERDEU A ANCORA (ver o teste dos dois lados)"
    r = RE.relato(alvo[0]["origem"])
    assert "veredito:" in r, (
        "o `relato` por origem nao imprime o veredito — ele foi calculado e"
        " jogado fora, que e o defeito do `contagem_de_cenas` em 20/10 as 03:2x")
    assert "veredito" in RE.relato().lower(), (
        "o relato GERAL nao diz nada sobre veredito")
    defs, fonte = _defs("reservas_escritas.py")
    assert "_linha_do_veredito" in defs, "a frase do veredito perdeu o dono"
    corpo_relato = _codigo(defs["relato"])
    assert corpo_relato.count("_linha_do_veredito") >= 2, (
        "a frase do veredito nao sai nos DOIS ramos do relato: %r"
        % corpo_relato[:200])
    assert "PARCIAL quer dizer" not in corpo_relato, (
        "a frase foi copiada para dentro do `relato`: o dono e o"
        " `_linha_do_veredito`")


def test_as_duas_contas_sao_DELEGADAS():
    defs, fonte = _defs("reservas_escritas.py")
    corpo = _codigo(defs["estado"])
    assert "SA." in corpo, (
        "o `estado` nao chama o `segundo_angulo`: %r" % corpo[:200])
    for proibido in ("glob", "listdir", "open("):
        assert proibido not in corpo, (
            "o `estado` %r por conta propria — seria o segundo dono da leitura"
            " do disco" % proibido)
    assert "nao_mencionados" in corpo and "capitulos_do_pacote" in corpo, (
        "ele deixou de usar as duas contas do dono")


def test_o_PARCIAL_nao_promete_meia_consumacao():
    """A ressalva e o que torna o rotulo honesto, e ela tem de estar no texto."""
    p = [e for e in RE.estado() if e["veredito"] == "parcial"]
    assert p, (
        "PERDEU A ANCORA: nenhuma reserva PARCIAL no disco, e e ela que exige a"
        " ressalva do papel da frase")
    linha = RE._linha_do_veredito(p[0])
    assert "LEIA A PROSA" in linha.upper(), (
        "a ressalva do PARCIAL saiu da frase: sem ela o rotulo promete"
        " 'metade consumida', que o modulo nao mede")


def test_a_RECUSA_nomeia_o_motivo():
    i = [e for e in RE.estado() if e["veredito"] == "indeterminada"]
    assert i, "PERDEU A ANCORA (ver o teste dos dois lados)"
    linha = RE._linha_do_veredito(i[0])
    assert "RECUSA" in linha.upper() and "prosa" in linha.lower(), (
        "a recusa deixou de dizer POR QUE recusa: %r" % linha)
    for e in i:
        assert not e["livres"] and not e["mencionados"], (
            "%s foi dado como indeterminado e ainda assim classificou"
            " capitulo" % e["pacote"])


def test_o_motivo_CIRCULAR_continua_escrito():
    _, fonte = _defs("reservas_escritas.py")
    baixo = fonte.lower()
    assert "circular" in baixo, (
        "o motivo (a remissao circular que impedia esta pergunta) saiu do"
        " modulo: conserto sem motivo escrito volta calado")
    assert "12:4x" in fonte, "a procedencia do destrave saiu do modulo"
