"""O `sem_egresso` eram DOIS modos, e um deles e POLITICA que nega CONNECT.

Medido em 20/10 as 11:4x, no container desta sessao. Com o controle de escrita
passando (`escrita OK`), os TRES hosts — a peca, o controle `OhrGlJvnBoM` e o
NEUTRO `example.com` — voltaram **000 sem arquivo**, que pelo ramo de 09:3x le
`sem_egresso`, isto e *"a minha rede nao sai"*.

**O proxy do proprio ambiente diz outra coisa, e diz nomeando o host:** o
`__agentproxy/status` lista `www.youtube.com:443` **e** `example.com:443` em
`recentRelayFailures` com
`"gateway answered 403 to CONNECT (policy denial or upstream failure)"`.

Logo o 000 em todos os hosts, o neutro inclusive, **nao estabelece ausencia de
rede** — ele e compativel com uma politica que nega todo CONNECT. A consequencia
pratica e a mesma (sem leitura, sem ponto de residuo, peca parqueada) e o
REMEDIO e diferente, que e a mesma razao pela qual `limite` e `consentimento`
vivem separados: politica e do dono, rede ausente nao se conserta.

**E a classe e a de 09:3x uma camada para fora**, com a mesma assinatura dos
quatro casos que o `CLAUDE.md` ja lista: instrumento que devolve VAZIO nao prova
ausencia (17/10), arquivo vazio nao prova morte (19/10), instrumento CHEIO nao
prova presenca (20/10 as 01:4x), 000 nao diz de QUEM e o zero (09:3x) — e agora
**000 em todo host nao diz se o silencio e da rede ou da POLITICA.**
"""

import ast
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "vivacidade_publica.py")
sys.path.insert(0, FABRICA)

import vivacidade_publica as VP  # noqa: E402

PAREDE = ("x" * 1200) + "CONSENT" + ("y" * 1200)
SORRY = "https://www.google.com/sorry/index?continue=..."
# os tres controles da sonda, do caso MEDIDO nesta rodada
MEDIDO = dict(neutro_respondeu=False, sonda_pode_gravar=True)


def test_o_caso_MEDIDO_desta_rodada_sai_negado_por_politica():
    assert VP.modo_de_fechamento(
        "", "", politica_negou=True, **MEDIDO) == "negado_por_politica"


def test_o_mesmo_000_com_a_politica_LIMPA_sai_sem_egresso():
    """Contraprova no outro sentido: sem ela o modo novo sairia sempre."""
    assert VP.modo_de_fechamento(
        "", "", politica_negou=False, **MEDIDO) == "sem_egresso"


def test_SEM_a_leitura_do_proxy_ele_RECUSA_em_vez_de_escolher():
    """E a retratacao: era exatamente esta chamada que eu vinha fazendo."""
    assert VP.modo_de_fechamento("", "", **MEDIDO) == "indeterminado"


def test_os_TRES_controles_tem_de_falar_e_nenhum_PAR_basta():
    """Sem este trio bastaria devolver um valor fixo para o arquivo passar."""
    pares = [
        dict(neutro_respondeu=False, sonda_pode_gravar=True),
        dict(neutro_respondeu=False, politica_negou=True),
        dict(sonda_pode_gravar=True, politica_negou=True),
    ]
    for kw in pares:
        assert VP.modo_de_fechamento("", "", **kw) == "indeterminado", kw
    assert VP.modo_de_fechamento(
        "", "", politica_negou=True, **MEDIDO) == "negado_por_politica"


def test_a_politica_NAO_atropela_os_modos_de_ROTA():
    """Politica negada nao pode reescrever `limite` nem `consentimento`.

    Os dois modos de rota se estabelecem pelo que a pagina trouxe, e uma leitura
    do proxy nao os desfaz — se ela os desfizesse, a parede do CONSENT passaria
    a se chamar politica.
    """
    assert VP.modo_de_fechamento(
        "", SORRY, politica_negou=True, **MEDIDO) == "limite"
    assert VP.modo_de_fechamento(
        PAREDE, "", politica_negou=True,
        neutro_respondeu=True, sonda_pode_gravar=True) == "consentimento"


def test_o_quarto_modo_que_eu_NAO_medi_segue_sem_nome():
    """Neutro RESPONDE e o YouTube nao: continua `indeterminado`."""
    for pol in (None, False, True):
        assert VP.modo_de_fechamento(
            "", "", neutro_respondeu=True, sonda_pode_gravar=True,
            politica_negou=pol) == "indeterminado", pol


def test_o_parametro_esta_na_ASSINATURA_por_AST():
    """Por AST porque o modulo CITA o nome na prosa que explica o defeito."""
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef)
            and n.name == "modo_de_fechamento"]
    assert len(alvo) == 1
    nomes = [a.arg for a in alvo[0].args.args]
    for esperado in ("neutro_respondeu", "sonda_pode_gravar",
                     "politica_negou"):
        assert esperado in nomes, (esperado, nomes)
    # os tres controles seguem OPCIONAIS, senao todo chamador antigo levanta
    assert len(alvo[0].args.defaults) >= 4, ast.unparse(alvo[0].args)


def test_a_MEDICAO_do_modo_novo_continua_escrita_no_modulo():
    fonte = io.open(MODULO, encoding="utf-8").read()
    achatada = " ".join(fonte.split())
    for marca in ("negado_por_politica", "example.com:443", "CONNECT",
                  "403", "recentRelayFailures", "RETRATA"):
        assert marca in achatada, (
            "conserto sem a medicao escrita volta calado: falta %r" % marca)


def test_a_FAMILIA_dos_quatro_casos_continua_nomeada_aqui():
    """Sem ela a rodada seguinte trata isto como incidente solto."""
    fonte = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    for marca in ("17/10", "19/10", "01:4x", "09:3x"):
        assert marca in fonte, marca
