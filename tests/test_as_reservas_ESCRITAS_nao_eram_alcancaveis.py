# -*- coding: utf-8 -*-
"""As reservas de pauta escritas em prosa nao eram alcancaveis por instrumento.

**Medido em 20/10 as 20:4x.** A peca daquela rodada saiu de uma indicacao que o
`kolejny-poziom-s019` havia escrito em prosa — *"O QUE EU NAO LEVEI, escrito para
a proxima rodada achar..."* — e **eu a achei por ACIDENTE**, porque o
`irmaos_da_origem` passou a imprimir o bloco de prosa dos irmaos sem campo as
15:3x do mesmo dia. O acervo carrega **vinte e quatro** reservas dessas e nenhuma
era consultavel: era DADO que ninguem podia chamar, a classe dos layouts mortos
virada do avesso.

A forma dos testes segue a disciplina da semana: a varredura sai do DISCO e
reprova por vacuidade, o marcador e cobrado como DELEGADO por AST, a guarda do
falso positivo e cobrada nos DOIS sentidos com o caso MEDIDO (uma citacao), a
reserva de prova e DERIVADA e nao nomeada, o chamador e cobrado (instrumento que
ninguem chama e o defeito que isto conserta), e os dois ramos do relato existem.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO    # noqa: E402
import reservas_escritas as RE   # noqa: E402

PISO_DE_RESERVAS = 15
FONTE = open(os.path.join(RAIZ, "fabrica", "reservas_escritas.py"),
             encoding="utf-8").read()


def _reservas():
    v = RE.varre()
    assert len(v) >= PISO_DE_RESERVAS, (
        "a varredura achou %d reservas, menos que o piso de %d: o glob ou o"
        " marcador deixaram de casar e TODO assert deste arquivo passaria por"
        " vacuidade" % (len(v), PISO_DE_RESERVAS))
    return v


def test_a_varredura_acha_as_reservas_do_acervo():
    v = _reservas()
    for r in v:
        assert r["pacote"] and r["texto"], r
        assert "NAO LEVEI" in r["texto"].upper(), (
            "%s: o texto nao contem o marcador" % r["pacote"])
    # cada reserva tem origem conhecida, senao ela nao serve a pauta nenhuma
    sem_origem = [r["pacote"] for r in v if not r["origem"]]
    assert not sem_origem, (
        "reserva sem `longo_existente` em %r: ela nao pode ser oferecida a"
        " origem nenhuma" % sem_origem)


def test_a_guarda_do_FALSO_POSITIVO_vale_nos_DOIS_sentidos():
    """O marcador tem de ABRIR paragrafo: citacao nao e reserva nova.

    Sem isso o instrumento ofereceria como reserva NOVA a mencao de uma reserva
    JA CONSUMIDA — detector inventando achado (725) no lugar mais caro, porque
    mandaria a rodada seguinte reescrever uma peca que acabou de sair.
    """
    marca = IO.MARCAS_DE_NEGACAO[0]
    abre = ("## FONTES\numa frase qualquer.\n\n" + marca
            + ", de proposito: os capitulos 7 a 9.\n")
    assert len(RE._blocos(abre)) == 1, (
        "marcador que ABRE paragrafo deixou de contar como reserva")
    citado = ('## FONTES\no irmao tem, no bloco *"' + marca
              + '"*, exatamente esta indicacao: os capitulos 7 a 9.\n')
    assert RE._blocos(citado) == [], (
        "marcador CITADO dentro de frase contou como reserva nova")

    # e o caso MEDIDO: existe no disco ao menos uma copy que o cita
    citacoes = 0
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        copy = d.get("copy") or ""
        if marca.lower() in copy.lower() and not RE._blocos(copy):
            citacoes += 1
    assert citacoes >= 1, (
        "nenhuma copy do disco CITA o marcador sem abrir paragrafo: perdi o"
        " caso que a guarda existe para excluir, e ela passa por vacuidade")


def test_o_MARCADOR_e_DELEGADO_e_nao_nasce_um_segundo_dono():
    arv = ast.parse(FONTE)
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and any(
                getattr(t, "id", "") == "MARCAS_DE_NEGACAO" for t in n.targets):
            raise AssertionError(
                "o modulo redefiniu `MARCAS_DE_NEGACAO`: o dono e o"
                " `irmaos_da_origem`, criado as 17:4x para o conserto do"
                " capitulo negado")
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    corpo = ast.unparse(defs["_blocos"])
    assert "MARCAS_DE_NEGACAO" in corpo, (
        "`_blocos` deixou de ler o marcador do dono: %r" % corpo)
    assert "O QUE EU NAO LEVEI" not in corpo, (
        "a string do marcador foi copiada para dentro de `_blocos`")
    # e os capitulos tambem sao do dono
    todo = ast.unparse(arv)
    assert "capitulos_negados" in todo, (
        "os capitulos deixaram de sair de `irmaos_da_origem.capitulos_negados`")
    for proibido in ("capitulos?", "[Cc]apitulo"):
        assert proibido not in todo, (
            "%r no modulo: segundo dono da leitura de faixa de capitulo"
            % proibido)


def test_ele_REPRODUZ_a_reserva_que_produziu_a_peca_da_rodada():
    """Derivada por PROPRIEDADE: a reserva cujo texto diz "TERCEIRO angulo".

    Nomear o `s019` seria identidade onde ha propriedade (743/753/761), e o
    acervo muda.
    """
    v = _reservas()
    terceiras = [r for r in v if "TERCEIRO" in r["texto"].upper()]
    assert terceiras, (
        "nenhuma reserva do acervo se declara um terceiro angulo — perdi a"
        " ancora do caso que produziu o instrumento")
    for r in terceiras:
        assert RE.da_origem(r["origem"]), (
            "%s: a reserva nao e devolvida quando se pergunta pela origem dela"
            % r["pacote"])


def test_os_DOIS_ramos_do_relato_existem():
    v = _reservas()
    com = v[0]["origem"]
    assert "deixada por" in RE.relato(com)
    sem = "ORIGEM-QUE-NAO-EXISTE"
    r = RE.relato(sem)
    assert "NENHUMA" in r and "segundo_angulo" in r, (
        "o ramo vazio nao diz para onde ir: %r" % r)
    # e o relato geral lista todas
    geral = RE.relato()
    assert str(len(v)) in geral


def test_o_relato_NAO_AFIRMA_mais_do_que_mede():
    """RETRATADO EM 21/10 as 14:0x, e ele travava o estado DEFEITUOSO.

    A versao de 20/10 cobrava a FRASE *"NAO diz que a reserva segue livre"* —
    isto e, exigia que o modulo continuasse sem poder responder. E ele nao podia
    por um defeito: o proprio bloco de reserva fazia o capitulo contar como
    MENCIONADO no `segundo_angulo`, e a remissao entre os dois modulos era
    CIRCULAR (medido em 20/10 as 12:4x, consertado ali). Com o circulo
    desfeito, o `estado` passou a dar veredito — e este teste reprovou um
    comportamento CORRETO. **Identidade onde a afirmacao era propriedade, a
    classe 743/753/761.**

    A propriedade que FICA e mais forte: o relato nao pode afirmar mais do que
    mede. Logo (a) todo veredito que ele imprime vem do `estado`, (b) a reserva
    que o instrumento NAO decide sai como RECUSA com o motivo, e (c) a ressalva
    de que mencao e INDICIO continua escrita.
    """
    v = _reservas()
    por_origem = {}
    for r in v:
        por_origem.setdefault(r["origem"], []).append(r)
    assert por_origem, "PERDEU A ANCORA: nenhuma reserva com origem"
    vistos = set()
    for origem, delas in por_origem.items():
        r = RE.relato(origem)
        assert "veredito:" in r, (
            "o relato de %r nao diz o veredito de nenhuma reserva" % origem)
        for e in RE.estado(origem):
            vistos.add(e["veredito"])
            if e["veredito"] == "indeterminada":
                assert "INDETERMINADA" in r, (
                    "reserva que o instrumento NAO decide saiu sem a recusa"
                    " em %r" % origem)
        assert "INDICIO" in r.upper(), (
            "a ressalva de que mencao e indicio e nao prova saiu do relato"
            " de %r" % origem)
    assert len(vistos) >= 2, (
        "o veredito convergiu para um valor so (%r): ele deixou de"
        " discriminar, e ai dizer 'veredito' nao afirma nada" % vistos)


def test_o_CHAMADOR_existe_e_e_a_escolha_de_pauta():
    """Instrumento que ninguem chama e exatamente o defeito que isto conserta.

    Por AST sobre o `pauta_do_momento`: import sem chamada nao basta.
    """
    alvo = os.path.join(RAIZ, "fabrica", "pauta_do_momento.py")
    arv = ast.parse(open(alvo, encoding="utf-8").read())
    importou = any(
        isinstance(n, ast.Import) and
        any(a.name == "reservas_escritas" for a in n.names)
        for n in ast.walk(arv))
    assert importou, "o `pauta_do_momento` nao importa o instrumento"
    chamou = False
    for n in ast.walk(arv):
        if isinstance(n, ast.Call):
            alvo_c = ast.unparse(n.func)
            if alvo_c.startswith("RE.") or "reservas_escritas." in alvo_c:
                chamou = True
    assert chamou, (
        "o `pauta_do_momento` importa e nao CHAMA: import sem chamada e a"
        " classe dos layouts mortos")


def test_o_dir_errado_LEVANTA_em_vez_de_devolver_vazio():
    """Lista vazia e bem formada e indistinguivel de acervo sem reserva."""
    try:
        RE.varre("caminho-que-nao-existe")
    except ValueError as e:
        assert "nao e um diretorio" in str(e)
    else:
        raise AssertionError("dir inexistente devolveu lista em vez de levantar")


def test_a_medida_e_o_motivo_continuam_escritos():
    for pedaco in ("24", "25", "ACIDENTE", "725"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: sem a medida e o motivo a rodada seguinte nao"
            " sabe por que a guarda existe" % pedaco)
