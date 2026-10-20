# -*- coding: utf-8 -*-
"""O "mire o PISO" do 772 nao e aplicavel em toda contagem de cena.

Medido em 20/10 as 06:3x, depois de eu recusar o TETO da voz **a mao** pela
segunda vez — catorze no `kolejny` as 04:1x e quinze no `epomeno` as 06:2x, as
duas com a mesma aritmetica: o orcamento no piso da faixa dava 22 caracteres por
cena, UM acima do piso OBSERVADO. O `cabe_na_voz` do modulo e um BOOLEANO: diz
que cabe e nao diz com quanta folga.

E ao medir a folga apareceu o fato que este arquivo guarda: **existem contagens
em que o PISO da faixa nao e alcancavel com texto legivel** — e uma delas e DEZ
cenas no `labtreinamento`, a forma mais usada da frota. Logo `teto_de_cenas`
("algum numero de caracteres cai DENTRO da faixa?") e "o piso e alcancavel?" sao
perguntas DIFERENTES, e eu as tratei como uma.
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FABRICA)

import contagem_de_cenas as CC            # noqa: E402
import ensaio                             # noqa: E402
import mira                               # noqa: E402
import esqueleto_entre_canais as EC        # noqa: E402

MODULO = os.path.join(FABRICA, "contagem_de_cenas.py")

VOZES = {
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
}


def _fonte(caminho=MODULO):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def _func(nome, caminho=MODULO):
    for no in ast.walk(ast.parse(_fonte(caminho))):
        if isinstance(no, ast.FunctionDef) and no.name == nome:
            return no
    raise AssertionError("funcao %r nao existe em %s" % (nome, caminho))


def _chamadas(no):
    fora = set()
    for n in ast.walk(no):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                fora.add("%s.%s" % (f.value.id, f.attr))
            elif isinstance(f, ast.Name):
                fora.add(f.id)
    return fora


def _quadros():
    saida = {}
    for c, v in VOZES.items():
        saida[c] = CC.quadro(c, v)
    return saida


def test_a_conta_e_DELEGADA_e_o_piso_vem_do_dono():
    """Refazer a inversao ou copiar o piso aqui criaria o segundo dono."""
    chamadas = _chamadas(_func("quadro"))
    assert "mira.chars_no_alvo" in chamadas, (
        "a conta dos caracteres tem de vir do inversor do `mira`: %s"
        % sorted(chamadas))
    assert "mira.teto_de_cenas" in chamadas, (
        "o piso de caracteres tem de vir do dono do teto: %s" % sorted(chamadas))
    fonte = _fonte()
    corpo = fonte.split('"""', 2)[-1]   # fora do docstring do modulo
    assert "chars_minimos" in corpo, (
        "o piso tem de ser LIDO pelo nome da chave do dono")


def test_o_nome_publico_do_inversor_DELEGA_e_nao_reimplementa():
    """`chars_no_alvo` existe para nao haver segunda inversao."""
    no = _func("chars_no_alvo", os.path.join(FABRICA, "mira.py"))
    assert "_chars_para_o_real" in _chamadas(no), (
        "o nome publico tem de delegar ao inversor privado")
    voz = VOZES["epomeno-epipedo"]
    for n in (10, 13, 15):
        assert mira.chars_no_alvo(voz, n, 41.55) == \
            mira._chars_para_o_real(voz, n, 41.55), (
            "o publico divergiu do privado em %d cenas" % n)


def test_os_DOIS_lados_existem_e_o_piso_e_INALCANCAVEL_em_alguma_contagem():
    """Se nenhuma for inalcancavel, esta nota se rele; se TODAS forem, o
    instrumento deixou de discriminar."""
    q = _quadros()
    cabem = [(c, x) for c, xs in q.items() for x in xs if x["cabe_na_voz"]]
    assert len(cabem) >= 20, "varredura pequena: %d pares" % len(cabem)
    inalc = [(c, x["cenas"]) for c, x in cabem if x["folga_no_piso"] < 0]
    folgadas = [(c, x["cenas"]) for c, x in cabem
                if x["folga_no_piso"] > CC.FOLGA_RENTE]
    assert inalc, (
        "NENHUMA contagem tem o piso inalcancavel — o fato que este arquivo "
        "guarda deixou de ocorrer, releia a nota")
    assert folgadas, "TODAS as contagens ficaram sem folga — releia a nota"
    assert len(inalc) < len(cabem) / 2, (
        "a maioria dos pares ficou inalcancavel (%d de %d): isto deixou de ser "
        "excecao e a nota tem de ser relida" % (len(inalc), len(cabem)))


def test_as_DUAS_perguntas_sao_diferentes_e_isso_e_o_achado():
    """`teto_de_cenas` diz que CABE na faixa; o piso dela pode nao ser
    alcancavel na mesma contagem. Provado chamando os DOIS donos."""
    canal = "labtreinamento"
    voz = VOZES[canal]
    faixa = ensaio.alvo_short(canal)
    t = mira.teto_de_cenas(voz, faixa)
    piso_chars = int(t["chars_minimos"])
    achou = []
    for n in range(2, int(t["teto"]) + 1):
        ch = mira.chars_no_alvo(voz, n, faixa[0] + 0.05)
        if ch < piso_chars:
            achou.append(n)
    assert achou, (
        "neste canal nenhuma contagem abaixo do teto tem o piso inalcancavel")
    n = achou[0]
    assert n <= int(t["teto"]), (
        "o caso tem de estar DENTRO do teto, senao nao ha contradicao nenhuma")
    cenas = [{"nar": "x" * piso_chars} for _ in range(n)]
    real = ensaio.duracao_real_prevista(cenas, voz, "edge")
    assert real > faixa[0], (
        "com o piso de caracteres a previsao tinha de passar do piso da faixa "
        "(%0.2f contra %0.2f)" % (real, faixa[0]))
    assert real <= faixa[1], (
        "e ainda caber na faixa — e isso que faz o `teto_de_cenas` aceitar")


def test_a_FRONTEIRA_do_rente_reproduz_as_duas_recusas_a_mao():
    """As duas recusas foram no TETO de cada voz, com folga de UM."""
    for canal in ("epomeno-epipedo", "kolejny-poziom"):
        voz = VOZES[canal]
        faixa = ensaio.alvo_short(canal)
        teto = int(mira.teto_de_cenas(voz, faixa)["teto"])
        q = {x["cenas"]: x for x in CC.quadro(canal, voz)}
        assert q[teto]["folga_no_piso"] <= CC.FOLGA_RENTE, (
            "%s: o teto (%d cenas) tinha de sair RENTE, e deu folga %d"
            % (canal, teto, q[teto]["folga_no_piso"]))
        assert q[teto - 1]["folga_no_piso"] > CC.FOLGA_RENTE, (
            "%s: a contagem que eu ACEITEI (%d cenas) nao pode sair rente — "
            "folga %d" % (canal, teto - 1, q[teto - 1]["folga_no_piso"]))


def test_ele_NOMEIA_e_NAO_filtra_contagem_nenhuma():
    """Filtrar esconderia a contagem, que e a cegueira do `origens_sem_uso`."""
    canal, voz = "labtreinamento", VOZES["labtreinamento"]
    q = CC.quadro(canal, voz)
    inalc = [x["cenas"] for x in q if x["cabe_na_voz"] and x["folga_no_piso"] < 0]
    assert inalc, "sem caso inalcancavel aqui o teste nao mede nada"
    r = CC.relato(canal, voz)
    assert "FOLGA DE CARACTERES" in r, "o relato nao nomeia a folga"
    for n in inalc:
        assert str(n) in r, "a contagem %d desapareceu do relato" % n
    e = CC.escolha(canal, voz)
    assert e["por_cadencia_geral"]["cenas"] in [x["cenas"] for x in q], (
        "a coluna nova nao pode mexer na escolha por cadencia")


def test_a_frase_da_folga_tem_UM_dono_e_sai_nos_DOIS_ramos():
    """A frase do teto nasceu duplicada e foi isso que a fez divergir (753)."""
    donos = []
    for no in ast.walk(ast.parse(_fonte())):
        if not isinstance(no, ast.FunctionDef):
            continue
        for n in ast.walk(no):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                    and "FOLGA DE CARACTERES" in n.value:
                donos.append(no.name)
    assert set(donos) == {"_linha_da_folga"}, (
        "a frase da folga tem mais de um dono: %r" % sorted(set(donos)))
    for c, v in VOZES.items():
        assert "FOLGA DE CARACTERES" in CC.relato(c, v), (
            "o relato de %s nao traz a linha da folga" % c)


def test_DEZ_cenas_e_a_forma_mais_usada_da_frota_RECONFERIDA():
    """O numero que torna o achado grave nao pode envelhecer calado (753)."""
    por_contagem = EC.quadro(EC.varre())["por_contagem_de_cena"]
    mais_usada = max(por_contagem, key=lambda k: por_contagem[k])
    assert mais_usada == 10, (
        "a forma mais usada da frota deixou de ser dez cenas (e %r): releia a "
        "nota, porque e ela que torna o achado grave" % mais_usada)
    assert por_contagem[10] >= 100, (
        "dez cenas caiu para %d pecas — o 'mais usado' precisa de massa"
        % por_contagem[10])
    canal, voz = "labtreinamento", VOZES["labtreinamento"]
    x = {y["cenas"]: y for y in CC.quadro(canal, voz)}[10]
    assert x["folga_no_piso"] < 0, (
        "em dez cenas o piso daquele canal voltou a ser alcancavel: folga %d"
        % x["folga_no_piso"])


def test_a_medida_e_as_duas_recusas_continuam_ESCRITAS():
    fonte = _fonte()
    for marca in ("FOLGA_RENTE", "REDACAO DECLARADA", "04:1x", "06:2x",
                  "772", "teto_de_cenas"):
        assert marca in fonte, "a nota perdeu %r" % marca
    assert "37" in fonte, "a medida dos pares (3 de 37) saiu do modulo"


def test_o_codigo_de_saida_continua_ZERO():
    for c in VOZES:
        p = subprocess.run([sys.executable, MODULO, c], capture_output=True,
                           text=True, timeout=900)
        assert p.returncode == 0, (
            "%s devolveu %d — isto virou portao" % (c, p.returncode))
        assert "FOLGA DE CARACTERES" in p.stdout, (
            "a linha da folga nao chegou ao stdout de %s" % c)
