# -*- coding: utf-8 -*-
"""O bloco de reserva do irmao fazia o `segundo_angulo` contar o capitulo
como MENCIONADO — medido em 20/10 as 12:4x, escolhendo a pauta da rodada.

O `labtreinamento-s016` deixou escrito, para a rodada seguinte achar, uma
reserva nomeando quatro capitulos do `labtreinamento-010`. Conferidos no
`segundo_angulo`, TRES deles voltavam como MENCIONADOS — e quem os mencionou foi
o proprio bloco de reserva, que existe para dizer que eles NAO foram usados.

**A promessa virava uso**, e a direcao e perversa: quanto melhor a rodada
anterior documentou o que deixou, mais invisivel o capitulo fica como livre. E a
remissao era CIRCULAR — o `reservas_escritas` manda perguntar ao
`segundo_angulo` se a reserva segue livre, e o `segundo_angulo` era cegado pela
reserva.

A forma destes testes: tudo sai do DISCO e por PROPRIEDADE, nunca pelo id da
origem desta rodada — ancorar no vivo reprova quando a pauta for consumida, e
consumir pauta e o trabalho (18/10 as 09:2x, classe 743/753/761).
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import segundo_angulo as SA        # noqa: E402
import reservas_escritas as RE     # noqa: E402
import irmaos_da_origem as IO      # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
MARCA = IO.MARCAS_DE_NEGACAO[0]


def _codigo(no):
    """O corpo de uma funcao SEM o docstring.

    Os docstrings deste repo CITAM os nomes dos donos para se explicar, e casar
    prosa pega a explicacao em vez do codigo. A primeira versao do teste da
    porta publica reprovou exatamente assim, e o errado era o teste.
    """
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _origens_com_irmao():
    """{origem: [pacotes]} das specs de short solto do disco."""
    saida = {}
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo"):
            continue
        o = d.get("longo_existente")
        if o:
            saida.setdefault(o, []).append(os.path.basename(f)[:-5])
    return saida


def _quadro():
    """Por origem: capitulos vistos na copy CRUA e na copy SEM reserva."""
    saida = []
    for origem in sorted(_origens_com_irmao()):
        pacote = SA.pacote_do_id(origem)
        if not pacote:
            continue
        caps = [k for k in SA.capitulos_do_pacote(pacote) if k]
        if len(caps) < SA.MIN_CAPITULOS_PLAUSIVEL:
            continue
        usados = SA.shorts_da_origem(origem)
        cru = " ".join(c for _, c in usados).lower()
        limpo = " ".join(SA._sem_reserva(c) for _, c in usados).lower()
        fantasma = [k for k in caps
                    if k.lower() in cru and k.lower() not in limpo]
        saida.append({"origem": origem, "pacote": pacote, "caps": caps,
                      "fantasma": fantasma})
    return saida


def test_a_varredura_nao_e_vacua():
    q = _quadro()
    assert len(q) >= 20, (
        "so %d origens com short e %d+ capitulos: a varredura encolheu e os"
        " testes abaixo passariam por vacuidade"
        % (len(q), SA.MIN_CAPITULOS_PLAUSIVEL))
    com_reserva = [r for r in RE.varre() if r["origem"]]
    assert len(com_reserva) >= 10, (
        "so %d reserva(s) escrita(s) no acervo: sem elas este arquivo nao mede"
        " nada" % len(com_reserva))


def test_o_defeito_EXISTIA_e_sai_por_propriedade():
    """Tem de haver origem em que tirar a reserva MUDA a resposta."""
    q = [r for r in _quadro() if r["fantasma"]]
    assert q, (
        "PERDEU A ANCORA: nenhuma origem do disco tem capitulo mencionado SO"
        " pelo bloco de reserva de um irmao. Se o acervo deixou de ter esse"
        " caso, esta nota se rele em vez de o arquivo ser apagado.")
    # e e MINORIA: alarme de massa deixa de avisar
    assert len(q) < len(_quadro()) / 2.0, (
        "%d de %d origens afetadas: a maioria mudou de resposta, logo o"
        " conserto trocou a base da leitura e isto tem de ser relido"
        % (len(q), len(_quadro())))


def test_o_capitulo_sai_NOMEADO_e_nao_filtrado():
    q = [r for r in _quadro() if r["fantasma"]]
    assert q, "PERDEU A ANCORA (ver o teste anterior)"
    r = q[0]
    d = SA.nao_mencionados(r["origem"])
    assert "mencionados_so_na_reserva" in d, (
        "a chave desapareceu: sem ela o conserto FILTRA em vez de NOMEAR, e a"
        " rodada seguinte nao sabe que a reserva nomeou aquele capitulo")
    for k in d["mencionados_so_na_reserva"]:
        assert k in d["nao_mencionados"], (
            "%r saiu como 'so na reserva' e NAO esta entre os nao"
            " mencionados — as duas listas tem de concordar" % k)
        assert k not in d["mencionados"], (
            "%r esta nas DUAS listas" % k)
    assert d["mencionados_so_na_reserva"], (
        "a origem %r tem capitulo fantasma pela varredura e a funcao nao o"
        " nomeia" % r["origem"])


def test_a_secao_de_FONTES_continua_contando_como_mencao():
    """Contraprova no outro sentido: mencao LEGITIMA nao pode ser apagada."""
    cap = "Zebra Fosforescente"
    legitima = "## FONTES\nCapitulos desta peca: %s.\n" % cap
    reserva = "\n\n%s: o capitulo %s.\n\n" % (MARCA, cap)
    assert cap.lower() in SA._sem_reserva(legitima).lower(), (
        "o conserto apagou a secao de FONTES: ali o irmao nomeia o que de fato"
        " USOU, e aquilo e mencao legitima")
    assert cap.lower() not in SA._sem_reserva(reserva).lower(), (
        "o bloco de reserva sobreviveu a limpeza")
    # as duas na MESMA copy: a legitima vence
    assert cap.lower() in SA._sem_reserva(legitima + reserva).lower(), (
        "capitulo citado nas FONTES *e* na reserva tem de continuar"
        " MENCIONADO — senao usar e reservar ficam indistinguiveis")


def test_copy_sem_reserva_nao_muda_em_nada():
    """Se nao ha bloco, a limpeza e identidade — senao ela mede outra coisa."""
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json")))[:120]:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        copy = d.get("copy") or ""
        if not copy or MARCA.lower() in copy.lower():
            continue
        assert SA._sem_reserva(copy) == copy, (
            "%s nao tem bloco de reserva e a copy mudou na limpeza"
            % os.path.basename(f))


def test_a_extracao_e_DELEGADA_ao_dono():
    fonte = open(os.path.join(RAIZ, "fabrica", "segundo_angulo.py"),
                 encoding="utf-8").read()
    arvore = ast.parse(fonte)
    defs = {n.name: n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef)}
    assert "_sem_reserva" in defs, "o dono da limpeza desapareceu"
    corpo = _codigo(defs["_sem_reserva"])
    assert "reservas_escritas" in corpo, (
        "`_sem_reserva` deixou de chamar o dono do bloco: %r" % corpo[:200])
    assert "blocos_de_reserva" in corpo, (
        "ele deixou de usar a porta publica do dono")
    # e NAO pode nascer o segundo dono do marcador
    for n in ast.walk(arvore):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            assert MARCA.lower() not in n.value.lower() or "##" in n.value, (
                "a string do marcador foi copiada para o `segundo_angulo`: o"
                " dono e o `irmaos_da_origem.MARCAS_DE_NEGACAO`")


def test_a_porta_publica_nao_reimplementa_nada():
    fonte = open(os.path.join(RAIZ, "fabrica", "reservas_escritas.py"),
                 encoding="utf-8").read()
    defs = {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}
    assert "blocos_de_reserva" in defs, "a porta publica desapareceu"
    # SEM o docstring: ele CITA `MARCAS_DE_NEGACAO` na prosa que explica o
    # defeito, e casar prosa pegaria a explicacao em vez do codigo — a licao
    # dos testes por AST desta semana. Primeira versao deste teste reprovou
    # assim, e o errado era o TESTE.
    corpo = _codigo(defs["blocos_de_reserva"])
    assert "_blocos" in corpo, (
        "a porta publica reimplementou a extracao: %r" % corpo[:200])
    assert "finditer" not in corpo and "MARCAS_DE_NEGACAO" not in corpo, (
        "a porta publica virou o SEGUNDO dono da extracao: %r" % corpo[:200])
    # e o dono continua lendo o marcador do dono dele
    assert "MARCAS_DE_NEGACAO" in _codigo(defs["_blocos"]), (
        "`_blocos` deixou de ler o marcador do `irmaos_da_origem`")


def test_o_motivo_CIRCULAR_continua_escrito():
    sa = open(os.path.join(RAIZ, "fabrica", "segundo_angulo.py"),
              encoding="utf-8").read().lower()
    re_ = open(os.path.join(RAIZ, "fabrica", "reservas_escritas.py"),
               encoding="utf-8").read().lower()
    for fonte, nome in ((sa, "segundo_angulo"), (re_, "reservas_escritas")):
        assert "circular" in fonte, (
            "o motivo (a remissao CIRCULAR entre os dois modulos) saiu do"
            " %s: conserto sem motivo escrito volta calado" % nome)
    assert "12:4x" in sa, "a procedencia da medida saiu do `segundo_angulo`"


def test_as_reservas_continuam_alcancaveis():
    """O conserto nao pode cegar quem LE a reserva — ela e a pauta mais barata."""
    com = [r for r in RE.varre() if r["origem"] and r["capitulos"]]
    assert com, (
        "nenhuma reserva com capitulo legivel: o `reservas_escritas` parou de"
        " achar o que ele nasceu para achar")
    r = com[0]
    assert RE.da_origem(r["origem"]), (
        "a reserva de %r sumiu da consulta por origem" % r["origem"])
