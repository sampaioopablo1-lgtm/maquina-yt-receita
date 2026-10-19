"""A rota da duracao fechou com 302 para `/sorry` — modo NOVO, e ele e acionavel.

MEDIDO em 19/10 as 06:1x. Depois de publicar o `epomeno-epipedo-s066`, a leitura
de duracao do `kLsLXWCeI8Q` voltou com **402 bytes**, e o controle
`OhrGlJvnBoM` (44 s conhecidos) voltou igual na mesma chamada — logo ROTA e nao
peca, pelo discriminador do 17/10 as 03:1x.

**O que e novo e o MODO:** nao foi a parede de consentimento que a tabela do
`CLAUDE.md` descreve (200, pagina de 1,2 MB, zero `lengthSeconds`, marcadores
`CONSENT`/`captcha`) — foi **302 para `google.com/sorry/index`**, que e recusa
por VOLUME de requisicao.

E a diferenca importa porque o remedio nao e o mesmo: a parede de consentimento
nao responde a volume nenhum (cookie, User-Agent e `&hl=en` foram testados em
16/10 e nao resolvem), e o limite responde — **gastar menos requisicao por
rodada e ler inscritos e duracao na MESMA passagem.**

**A causa fica como HIPOTESE, nao como achado:** as seis requisicoes que eu fiz
nos sete minutos anteriores sao o candidato obvio, e uma rodada nao separa a
minha carga da de todo o resto que sai deste IP. O que esta medido e a
sequencia — 200 com 1,2 MB as 05:3x, 302 as 06:14.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import vivacidade_publica as V  # noqa: E402

# O corpo e o Location REAIS da leitura de 06:14:50 GMT, truncados.
LOCATION_REAL = ("https://www.google.com/sorry/index?continue="
                 "https://www.youtube.com/watch%3Fv%3DOhrGlJvnBoM&q=EgQI5VGXG")
CORPO_REAL = ('<HTML><HEAD><meta http-equiv="content-type" '
              'content="text/html;charset=utf-8">\n<TITLE>302 Moved</TITLE>'
              '</HEAD><BODY>\n<H1>302 Moved</H1>\nThe document has moved\n'
              '<A HREF="https://www.google.com/sorry/index?continue='
              'https://www.youtube.com/watch%3Fv%3DOhrGlJvnBoM">here</A>.\n'
              '</BODY></HTML>')


def test_o_302_para_sorry_sai_como_LIMITE():
    assert V.modo_de_fechamento(CORPO_REAL, LOCATION_REAL) == "limite"
    # e tambem pelo corpo sozinho, porque nem toda chamada guarda o header
    assert V.modo_de_fechamento(CORPO_REAL) == "limite"
    assert V.modo_de_fechamento("", LOCATION_REAL) == "limite"


def test_a_parede_de_CONSENTIMENTO_nao_e_confundida_com_limite():
    """Contraprova no outro sentido: 200 com pagina grande e sem campo e o modo
    ANTIGO, e ele nao responde a volume."""
    pagina = "x" * 50000 + "CONSENT" + "y" * 50000 + "captcha"
    assert V.modo_de_fechamento(pagina) == "consentimento"
    assert V.modo_de_fechamento(pagina, "") == "consentimento"


def test_rota_ABERTA_continua_aberta():
    assert V.modo_de_fechamento('..."lengthSeconds":"44"...') == "aberta"
    assert V.modo_de_fechamento(
        '"lengthSeconds":"43" e "lengthSeconds":"44"') == "aberta"


def test_o_modo_NAO_substitui_a_peca_de_CONTROLE():
    """Nos DOIS modos a leitura da peca nova vem vazia do mesmo jeito, logo
    saber o modo nao decide se o defeito e da peca. O discriminador segue sendo
    o controle, e o `veredito_da_rota` e quem o aplica."""
    assert V.duracao_do_html(CORPO_REAL) is None
    assert V.veredito_da_rota(None, None, 44) == "rota_fechada"
    # e quando o controle responde, a leitura vazia volta a ser da peca
    assert V.veredito_da_rota(None, 44, 44) == "peca_sem_leitura"


def test_a_HIPOTESE_vai_escrita_como_hipotese():
    """Causa suposta apresentada como medida e o efeito (C) da rotina. O modulo
    tem de dizer que e hipotese e dizer o que esta medido."""
    with open(os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
              encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    assert "HIPOTESE DECLARADA" in texto
    assert "NAO medi" in texto
    for frase in ("05:3x", "06:14"):
        assert frase in texto, f"a sequencia medida perdeu {frase!r}"


def test_a_consequencia_pratica_vale_mesmo_se_a_hipotese_cair():
    """Ela e sobre gastar menos requisicao, e isso nao depende da causa."""
    with open(os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
              encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    assert "mesmo se a hipotese estiver errada" in texto
    assert "MESMA passagem" in texto


def test_os_tres_modos_sao_DISTINTOS_dois_a_dois():
    """Sem isto, um deles poderia virar sinonimo de outro sem ninguem ver."""
    modos = {V.modo_de_fechamento(CORPO_REAL, LOCATION_REAL),
             V.modo_de_fechamento("x" * 1000 + "CONSENT"),
             V.modo_de_fechamento('"lengthSeconds":"44"')}
    assert modos == {"limite", "consentimento", "aberta"}, modos
