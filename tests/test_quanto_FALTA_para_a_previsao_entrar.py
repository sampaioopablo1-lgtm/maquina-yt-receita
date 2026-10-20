# -*- coding: utf-8 -*-
"""Nada dizia quantos CARACTERES faltam quando a previsao cai fora da faixa.

**Medido em 20/10 as 22:3x.** O `orcamento` diz quanto escrever ANTES de
escrever e o `janela_do_mundo` da a janela — e nenhum dos dois responde a
pergunta em que eu de fato estou toda rodada: a peca JA esta escrita e a
previsao caiu fora, quantos caracteres faltam?

**O caso que produziu o instrumento:** a primeira versao do
`epomeno-epipedo-s079` saiu com previsao 41,31 contra um piso de 41,5 — **quatro
caracteres**. Eu somei de cabeca e acrescentei **quinze**, um fator 3,7. A peca
ficou dentro e por isso o erro nao apareceu: **conta de cabeca que acerta o lado
e erra a magnitude e a mais facil de nao ver.**

A forma dos testes segue a disciplina da semana: a varredura sai do DISCO e
reprova por vacuidade, o caso e REPRODUZIDO por construcao em vez de nomeado, os
TRES ramos sao cobrados, a FRONTEIRA vale nos dois sentidos, a conta e cobrada
como DELEGADA por AST, e a frase tem UM dono e sai nos DOIS ramos.
"""
import ast
import glob
import json
import os
import statistics
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import mira    # noqa: E402

PISO_DE_SPECS = 150
FONTE = open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8").read()


def _corpo_sem_docstring(fn: ast.FunctionDef) -> str:
    """O CODIGO da funcao, sem o docstring.

    **A primeira versao destes testes casava o corpo INTEIRO**, e reprovou por
    `/ R` escrito dentro do docstring que EXPLICA por que `/ R` nao pode estar
    no codigo. E a licao da semana — casar prosa pega a explicacao em vez do
    codigo — cometida no teste escrito para a cobrar.
    """
    corpo = list(fn.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(n) for n in corpo)


def _cadeia(defs: dict, raiz: str) -> list:
    """Os nomes alcancaveis a partir de `raiz` dentro do proprio modulo.

    O `relato` nao chama o dono da frase DIRETAMENTE: ele chama o
    `_linha_do_orcamento`, que a chama. Travar a chamada direta seria
    identidade de FUNCAO onde a afirmacao e que a frase CHEGA ao relato — o
    defeito 743/753/761 que eu ja retratei num teste de delegacao em 20/10.
    """
    vistos, fila, saida = set(), [raiz], []
    while fila:
        nome = fila.pop()
        if nome in vistos or nome not in defs:
            continue
        vistos.add(nome)
        saida.append(nome)
        for c in ast.walk(defs[nome]):
            if isinstance(c, ast.Call):
                fila.append(ast.unparse(c.func).rsplit(".", 1)[-1])
    return saida


def _specs():
    saida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("short") and d.get("voz") in ensaio.MODELO_VOZ:
            saida.append((os.path.basename(f)[:-5], d))
    assert len(saida) >= PISO_DE_SPECS, (
        "a varredura achou %d specs com voz modelada, menos que o piso de %d:"
        " TODO assert passaria por vacuidade" % (len(saida), PISO_DE_SPECS))
    return saida


def test_os_TRES_ramos_existem_no_disco():
    """DENTRO, ACRESCENTAR e CORTAR — se um faltar, o ramo nao e conferido."""
    vistos = {}
    for nome, d in _specs():
        q = mira.quanto_falta(d)
        if q:
            vistos.setdefault(q["sentido"], nome)
    for ramo in ("DENTRO", "ACRESCENTAR", "CORTAR"):
        assert ramo in vistos, (
            "nenhuma spec do disco cai no ramo %r: ele nao e conferido por"
            " ninguem, e o acervo e que da os tres" % ramo)


def test_REPRODUZ_o_caso_que_produziu_o_instrumento():
    """Por CONSTRUCAO, nao por nome: encurta uma peca que esta dentro ate ela
    cair abaixo do piso, e cobra que o numero devolvido POE a peca dentro."""
    base = None
    for _, d in _specs():
        q = mira.quanto_falta(d)
        if q and q["sentido"] == "DENTRO" and not d.get("longo"):
            base = d
            break
    assert base is not None, "nenhuma spec DENTRO da faixa no disco"

    curta = json.loads(json.dumps(base))
    # tira caracteres de cada cena ate cair abaixo do piso
    while True:
        q = mira.quanto_falta(curta)
        if q["sentido"] == "ACRESCENTAR":
            break
        mudou = False
        for c in curta["short"]:
            nar = c.get("nar") or ""
            if len(nar) > 12:
                c["nar"] = nar[:-2] + nar[-1]
                mudou = True
        assert mudou, "nao consegui encurtar a peca o bastante"

    falta = q["caracteres"]
    assert falta > 0
    # acrescentar EXATAMENTE o que ele pede poe a previsao dentro
    cheia = json.loads(json.dumps(curta))
    cheia["short"][0]["nar"] = (cheia["short"][0]["nar"] or "") + "x" * falta
    q2 = mira.quanto_falta(cheia)
    assert q2["sentido"] == "DENTRO", (
        "acrescentar os %d caracteres que ele pediu deixou a previsao em %.2f,"
        " ainda %s" % (falta, q2["previsao"], q2["sentido"]))
    # e UM a menos NAO poe (fronteira)
    if falta > 1:
        quase = json.loads(json.dumps(curta))
        quase["short"][0]["nar"] = (quase["short"][0]["nar"] or "") + "x" * (falta - 1)
        assert mira.quanto_falta(quase)["sentido"] == "ACRESCENTAR", (
            "um caractere a MENOS que o pedido ja entrou na faixa: o numero"
            " devolvido esta alto e nao e a fronteira")


def test_o_ramo_CORTAR_tambem_e_cobrado_na_fronteira():
    base = None
    for _, d in _specs():
        q = mira.quanto_falta(d)
        if q and q["sentido"] == "DENTRO" and not d.get("longo"):
            base = d
            break
    assert base is not None
    longa = json.loads(json.dumps(base))
    longa["short"][0]["nar"] = (longa["short"][0]["nar"] or "") + "x" * 400
    q = mira.quanto_falta(longa)
    assert q["sentido"] == "CORTAR" and q["caracteres"] > 0
    cortada = json.loads(json.dumps(longa))
    n = q["caracteres"]
    cortada["short"][0]["nar"] = cortada["short"][0]["nar"][:-n]
    assert mira.quanto_falta(cortada)["sentido"] == "DENTRO", (
        "cortar os %d caracteres pedidos nao poe a peca dentro" % n)


def test_a_conta_e_DELEGADA_e_nao_nasce_um_segundo_dono_do_R():
    """O `R` da voz tem UM dono. Escrever `len(nar) / R` aqui seria o segundo."""
    arv = ast.parse(FONTE)
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    corpo = _corpo_sem_docstring(defs["quanto_falta"])
    assert corpo.count("duracao_real_prevista") >= 2, (
        "o segundo por caractere deixou de ser MEDIDO por duas chamadas ao"
        " dono: %r" % corpo)
    assert "MODELO_VOZ[" not in corpo, (
        "`quanto_falta` passou a ler o `R` da tabela: segundo dono da"
        " sobrecarga por voz")
    for proibido in ("/ R", "R)", "20.61", "17.47", "20.07"):
        assert proibido not in corpo, (
            "%r dentro de `quanto_falta`: o `R` tem UM dono" % proibido)


def test_a_faixa_da_peca_e_DELEGADA_com_a_precedencia_do_ensaio():
    """Faixa DECLARADA > mira do canal > faixa da frota, e nenhuma nasce aqui.

    Repetir a precedencia foi o terceiro defeito do `orcamento` em 19/10 as
    15:2x: ele cobria um canal de tres por nao chamar o acessor.
    """
    arv = ast.parse(FONTE)
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    corpo = _corpo_sem_docstring(defs["_faixa_da_peca"])
    assert "alvo_short" in corpo and "faixa_do_short" in corpo, (
        "a precedencia deixou de sair do `ensaio`: %r" % corpo)
    for proibido in ("41.5", "43.0", "20.0", "26.0", "18.0", "45.0"):
        assert proibido not in corpo, (
            "%r cravado em `_faixa_da_peca`: a faixa tem UM dono" % proibido)
    # e ela cobre os TRES canais vivos, nao um
    vistas = set()
    for _, d in _specs():
        f = mira._faixa_da_peca(d)
        if f:
            vistas.add(tuple(f))
    assert len(vistas) >= 2, (
        "so %d faixa(s) distinta(s) em todo o disco: a precedencia nao esta"
        " distinguindo canal com mira propria de canal sem" % len(vistas))


def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos():
    arv = ast.parse(FONTE)
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    assert "_linha_do_quanto_falta" in defs
    cadeia = _cadeia(defs, "relato")
    assert "_linha_do_quanto_falta" in cadeia, (
        "o dono da frase nao e alcancavel a partir do `relato`: a cadeia e %r"
        % (cadeia,))
    for outro in defs:
        if outro == "_linha_do_quanto_falta":
            continue
        assert "QUANTO FALTA" not in _corpo_sem_docstring(defs[outro]), (
            "a frase ganhou um segundo dono em `%s`" % outro)
    dentro = fora = None
    for _, d in _specs():
        q = mira.quanto_falta(d)
        if not q:
            continue
        if q["sentido"] == "DENTRO" and dentro is None:
            dentro = d
        if q["sentido"] != "DENTRO" and fora is None:
            fora = d
        if dentro is not None and fora is not None:
            break
    assert dentro is not None and fora is not None
    l_d = "\n".join(mira._linha_do_quanto_falta(dentro))
    l_f = "\n".join(mira._linha_do_quanto_falta(fora))
    assert "QUANTO FALTA" in l_d and "QUANTO FALTA" in l_f, (
        "a linha CALA num dos ramos — e o ramo DENTRO e justamente onde quem le"
        " precisa saber qual e a margem")
    assert "nada" in l_d and "nada" not in l_f


def test_a_MEDIDA_do_tamanho_e_reconferida_contra_o_disco():
    """753: numero que ninguem reconfere envelhece calado."""
    specs = _specs()
    fora, difs = [], []
    for nome, d in specs:
        q = mira.quanto_falta(d)
        if q and q["sentido"] != "DENTRO":
            fora.append(nome)
            difs.append(q["caracteres"])
    assert difs, "nenhuma spec fora do alvo: a pergunta perdeu o objeto"
    med = statistics.median(difs)
    assert abs(len(fora) - 192) <= 25, (
        "as specs FORA do alvo foram de 192 para %d: a medida do modulo precisa"
        " ser reconferida" % len(fora))
    assert abs(med - 79) <= 30, (
        "a distancia mediana foi de 79 para %.0f caracteres" % med)
    for pedaco in ("192", "79", "41,31", "15 onde faltavam 4"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: sem a medida e o caso a rodada seguinte nao sabe"
            " o tamanho da pergunta" % pedaco)


def test_isto_INFORMA_e_o_codigo_de_saida_segue_ZERO():
    import subprocess
    alvo = None
    for nome, d in _specs():
        q = mira.quanto_falta(d)
        if q and q["sentido"] != "DENTRO" and not d.get("longo"):
            alvo = os.path.join(RAIZ, "fabrica", "specs", nome + ".json")
            break
    assert alvo, "nenhuma spec de short solto fora do alvo"
    p = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                        alvo], capture_output=True, text=True)
    assert "QUANTO FALTA" in p.stdout
    # a peca esta FORA do alvo do canal, e o veredito do `confere` e quem decide
    # o codigo de saida — nao esta linha.
    assert p.returncode in (0, 1)
    dentro = None
    for nome, d in _specs():
        q = mira.quanto_falta(d)
        if q and q["sentido"] == "DENTRO" and not d.get("longo"):
            dentro = os.path.join(RAIZ, "fabrica", "specs", nome + ".json")
            break
    assert dentro
    p2 = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                         dentro], capture_output=True, text=True)
    assert p2.returncode == 0, (
        "peca DENTRO da faixa passou a devolver %d: a linha nova reprovou"
        % p2.returncode)
