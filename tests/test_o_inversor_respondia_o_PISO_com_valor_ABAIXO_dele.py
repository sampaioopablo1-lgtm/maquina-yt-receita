# -*- coding: utf-8 -*-
"""O inversor respondia "mire o PISO" com um valor cuja previsao cai ABAIXO dele.

**Medido em 20/10 as 16:4x, escrevendo o `epomeno-epipedo-s077`.** O
`mira.chars_no_alvo(voz, 12, 41.5)` devolve **36** caracteres por cena, e 36
preve **41,39** — fora da faixa, pelo lado de baixo. Varridos os 54 pares
(canal, contagem) da frota com resposta para o piso, isso ocorre em **54 de
54**: o inversor desce ate a previsao caber `<= alvo`, logo com o PISO no lugar
do alvo ele entrega sempre peca ABAIXO da faixa.

**Logo a regra de redacao do 772 — "mire o PISO do `ALVO_SHORT`" — era
inexecutavel por aquele caminho**, e eu a vinha cumprindo somando de cabeca
(item 3 da §10). O docstring do `_chars_para_o_real` guardava o OUTRO lado da
mesma armadilha (*"dizer 'mirei o piso' e entregar peca acima do TOPO"*) e nao
este: a assinatura do **771**, criterio escrito so no lado em que eu olhava.

**O que estes testes cobram, e por que cada um existe:**
  * a varredura sai dos CANAIS VIVOS e **reprova por vacuidade** se encolher;
  * o defeito e medido por **PROPRIEDADE**, nao pelo numero 36 nem pelo par
    (grego, 12), que mudam se `ALVO_SHORT` ou o modelo de voz mudarem;
  * a janela nova e cobrada na **FRONTEIRA** nos dois sentidos — o primeiro
    elemento cabe e o anterior NAO —, porque so isso distingue "a menor que
    cabe" de "qualquer uma que cabe";
  * os **DOIS** lados existem: ha contagem com janela ABERTA e contagem com
    janela FECHADA, senao a funcao poderia devolver sempre o mesmo e passar;
  * o varrimento tem **UM dono** por AST — duas copias do laco seriam a
    assinatura que congelou a legenda, e o `janela_dos_dois_mundos` **nao pode
    mudar de resposta** com o conserto;
  * e um **reproduz a escolha desta rodada**, derivando-a em vez de a nomear.
"""
import ast
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import mira    # noqa: E402

VOZES = {
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
}
PECA_DA_RODADA = "epomeno-epipedo-s077"   # HISTORIA: a peca em que isto foi
                                          # medido. Nenhum assert depende dela.


def _previsao(voz, n, chars, provedor="edge"):
    cenas = [{"layout": "item", "nar": "x" * chars} for _ in range(n)]
    return ensaio.duracao_real_prevista(cenas, voz, provedor)


def _pares():
    saida = []
    for canal, voz in VOZES.items():
        faixa = ensaio.alvo_short(canal)
        for n in range(2, 21):
            ch = mira.chars_no_alvo(voz, n, faixa[0])
            if ch:
                saida.append((canal, voz, faixa, n, ch))
    return saida


def test_a_varredura_nao_passa_por_VACUIDADE():
    pares = _pares()
    assert len(pares) >= 40, (
        "so %d pares (canal, contagem) com resposta para o piso: com menos que"
        " isso este arquivo nao mede o defeito, ele passa por vacuidade"
        % len(pares))
    assert len(VOZES) == 3, "a frota deixou de ter tres canais vivos"


def test_a_resposta_do_PISO_cai_ABAIXO_dele_e_isso_e_PROPRIEDADE():
    """Nao se trava o 36 nem o par (grego, 12): trava-se o SENTIDO do erro.

    A propriedade e que o inversor, perguntado pelo piso, devolve um valor cuja
    previsao fica estritamente ABAIXO do piso — e que isso e a REGRA e nao o
    acidente de um par.
    """
    pares = _pares()
    abaixo = []
    for canal, voz, faixa, n, ch in pares:
        d = _previsao(voz, n, ch)
        if d < faixa[0]:
            abaixo.append((canal, n, ch, round(d, 2)))
    assert abaixo, (
        "nenhuma resposta do piso cai abaixo dele: o inversor foi consertado"
        " para arredondar para dentro, e ai esta nota se rele em vez de o teste"
        " ficar verde por vacuidade")
    assert len(abaixo) > len(pares) / 2, (
        "so %d de %d respostas do piso caem abaixo dele — deixou de ser a REGRA"
        " e passou a ser excecao; releia a nota" % (len(abaixo), len(pares)))


def test_a_janela_de_UM_mundo_responde_o_piso_EXECUTAVEL():
    """O primeiro elemento dela cabe; o anterior, nao. FRONTEIRA nos dois lados."""
    achou = 0
    encostadas = []
    for canal, voz, faixa, n, _ch in _pares():
        j = mira.janela_do_mundo(voz, n, faixa)
        if not j:
            continue
        achou += 1
        menor, maior = j
        d = _previsao(voz, n, menor)
        assert faixa[0] <= d <= faixa[1], (
            "%s/%d: a janela diz %d e ele preve %.2f, FORA de %s"
            % (canal, n, menor, d, faixa))
        if menor > 1:
            antes = _previsao(voz, n, menor - 1)
            assert not (faixa[0] <= antes <= faixa[1]), (
                "%s/%d: %d tambem cabe (%.2f), logo %d nao e o MENOR"
                % (canal, n, menor - 1, antes, menor))
        # A fronteira de CIMA so e da FAIXA quando o maior esta abaixo do teto
        # do varrimento: encostado nele, o limite e o laco e nao a faixa —
        # medido no polones com tres cenas, janela (233, 240) com 241 cabendo.
        # O teto e LIDO do modulo, nunca escrito aqui (753).
        if maior < mira.MAX_CHARS_VARRIDOS:
            depois = _previsao(voz, n, maior + 1)
            assert not (faixa[0] <= depois <= faixa[1]), (
                "%s/%d: %d tambem cabe (%.2f), logo %d nao e o MAIOR"
                % (canal, n, maior + 1, depois, maior))
        else:
            encostadas.append((canal, n))
    assert achou >= 10, (
        "so %d contagens abriram janela de um mundo: a fronteira nao foi"
        " exercitada o bastante" % achou)
    assert len(encostadas) < achou, (
        "TODAS as janelas encostaram no teto do varrimento (%s): a fronteira de"
        " cima nao foi medida em nenhuma" % encostadas)


def test_os_DOIS_lados_existem_aberta_e_FECHADA():
    """Funcao que devolve sempre o mesmo nao mede nada.

    **Falha se TODA contagem abrir janela, ou se NENHUMA abrir** — nos dois
    casos a nota tem de ser relida.
    """
    abertas = fechadas = 0
    for canal, voz in VOZES.items():
        faixa = ensaio.alvo_short(canal)
        for n in range(2, 21):
            if mira.janela_do_mundo(voz, n, faixa):
                abertas += 1
            else:
                fechadas += 1
    assert abertas and fechadas, (
        "janela de um mundo: abertas=%d fechadas=%d — sem os dois lados a"
        " funcao nao discrimina" % (abertas, fechadas))


def test_a_janela_dos_DOIS_mundos_nao_mudou_de_resposta():
    """O conserto moveu o laco; ele nao pode ter mudado o veredito.

    E o subconjunto e cobrado na direcao certa: o que cabe nos DOIS cabe em UM.
    """
    conferidos = 0
    for canal, voz in VOZES.items():
        faixa = ensaio.alvo_short(canal)
        for n in range(2, 21):
            dois = mira.janela_dos_dois_mundos(voz, n, faixa)
            if dois is None:
                continue
            conferidos += 1
            um = mira.janela_do_mundo(voz, n, faixa)
            assert um is not None, (
                "%s/%d: cabe nos DOIS mundos e nao cabe em UM — impossivel"
                % (canal, n))
            assert um[0] <= dois[0] and dois[1] <= um[1], (
                "%s/%d: a janela dos dois (%s) nao esta dentro da de um (%s)"
                % (canal, n, dois, um))
    assert conferidos >= 5, (
        "so %d contagens com janela dos dois mundos: a pinca fechou em toda a"
        " frota e esta comparacao perdeu o objeto" % conferidos)


def test_o_varrimento_tem_UM_dono_por_AST():
    """Duas copias do laco seriam o segundo dono — a assinatura da legenda."""
    fonte = open(mira.__file__, encoding="utf-8").read()
    arv = ast.parse(fonte)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    for nome in ("_janela", "janela_do_mundo", "janela_dos_dois_mundos"):
        assert nome in defs, "`%s` desapareceu do modulo" % nome
    # A propriedade e sobre as funcoes de JANELA, nao sobre o modulo todo: o
    # `teto_de_cenas`, o `orcamento` e o `_chars_para_o_real` tambem varrem
    # previsao, e legitimamente, porque respondem OUTRAS perguntas. Cravar a
    # lista inteira seria identidade onde ha propriedade (743/753/761) — e foi
    # exatamente o que a primeira versao deste assert fez, reprovando por
    # `teto_de_cenas` e `orcamento`.
    janelas = [n for n in defs if n.startswith("janela_")]
    assert len(janelas) >= 2, "as funcoes de janela desapareceram: %s" % janelas
    for nome in janelas:
        no = defs[nome]
        varre = any(isinstance(c, ast.Call)
                    and "duracao_real_prevista" in ast.unparse(c.func)
                    for c in ast.walk(no))
        assert not varre, (
            "`%s` varre previsao por conta propria: segundo dono do laco" % nome)
    for nome in ("janela_do_mundo", "janela_dos_dois_mundos"):
        corpo = ast.unparse(defs[nome])
        assert "_janela" in corpo, (
            "`%s` deixou de delegar ao `_janela`" % nome)
        assert "duracao_real_prevista" not in corpo, (
            "`%s` voltou a varrer por conta propria" % nome)


def test_ele_reproduz_a_escolha_desta_rodada():
    """A peca da rodada esta no piso EXECUTAVEL, e o id NAO entra no assert.

    A propriedade e que a media escrita caia na janela de um mundo e no PRIMEIRO
    degrau dela — nomear a `s077` seria identidade onde ha propriedade
    (743/753/761).
    """
    caminho = os.path.join(RAIZ, "fabrica", "specs", "%s.json" % PECA_DA_RODADA)
    if not os.path.exists(caminho):
        pytest.skip("a peca de 16:4x saiu do disco; a propriedade segue nos"
                    " outros testes")
    sp = json.load(open(caminho, encoding="utf-8"))
    cenas = sp["short"]
    voz = sp["voz"]
    faixa = ensaio.alvo_short(mira.canal_da_spec(sp))
    j = mira.janela_do_mundo(voz, len(cenas), faixa)
    assert j, "a janela de um mundo fechou para esta peca"
    media = sum(len(c["nar"]) for c in cenas) / float(len(cenas))
    assert j[0] <= media <= j[1], (
        "media %.1f fora da janela de um mundo %s" % (media, j))
    assert media - j[0] < 1.0, (
        "media %.1f esta %.1f acima do piso executavel %d: a peca nao mirou o"
        " piso" % (media, media - j[0], j[0]))


def test_a_MEDIDA_e_o_MOTIVO_continuam_escritos():
    fonte = open(mira.__file__, encoding="utf-8").read()
    for pedaco in ("54 de 54", "16:4x", "janela_do_mundo", "771"):
        assert pedaco in fonte, (
            "%r saiu do modulo: medida ou motivo que ninguem reconfere"
            " envelhece calado (753)" % pedaco)


def test_o_RELATO_chama_a_janela_e_nao_a_deixa_morta():
    """Instrumento que o relato nao chama e a classe dos layouts mortos.

    Por AST na fiacao (o docstring cita os nomes em prosa, e casar prosa pegaria
    a explicacao), e pela SAIDA numa peca de verdade — sem o segundo, bastaria
    importar sem usar.
    """
    fonte = open(mira.__file__, encoding="utf-8").read()
    arv = ast.parse(fonte)
    alvo = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)
            and n.name == "_linha_do_orcamento"]
    assert alvo, "`_linha_do_orcamento` desapareceu"
    chamadas = [ast.unparse(c.func) for c in ast.walk(alvo[0])
                if isinstance(c, ast.Call)]
    assert any("janela_do_mundo" in c for c in chamadas), (
        "a linha do orcamento nao chama o `janela_do_mundo`: ele nasceu morto")

    caminho = os.path.join(RAIZ, "fabrica", "specs", "%s.json" % PECA_DA_RODADA)
    if not os.path.exists(caminho):
        pytest.skip("a peca de 16:4x saiu do disco")
    r = mira.relato(caminho)
    assert "PISO EXECUTAVEL" in r or "NAO existe piso executavel" in r, (
        "o relato nao diz nada sobre o piso executavel:\n%s" % r)


def test_o_relato_continua_INFORMANDO_e_nao_reprovando():
    """Contraprova no outro sentido: a linha nova nao pode virar portao.

    O veredito sai do ESTADO (`confere`), nunca do texto — a licao de 19/10 as
    18:1x, quando o codigo de saida saia de um grep na propria prosa.
    """
    import subprocess
    caminho = os.path.join(RAIZ, "fabrica", "specs", "%s.json" % PECA_DA_RODADA)
    if not os.path.exists(caminho):
        pytest.skip("a peca de 16:4x saiu do disco")
    p = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                        caminho], capture_output=True, text=True)
    assert p.returncode == 0, (
        "a linha do piso executavel passou a reprovar: saida %d\n%s"
        % (p.returncode, p.stdout))
    sp = json.load(open(caminho, encoding="utf-8"))
    assert not mira.confere(sp).get("fora"), (
        "o veredito do `confere` mudou: a peca da rodada estava DENTRO")
