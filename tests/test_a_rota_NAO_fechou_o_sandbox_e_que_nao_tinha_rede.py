"""A rota nao fechou — o SANDBOX e que nao tinha rede. 19/10/2026, 23:4x.

A leitura da peca nova (`OHSGYkkkvtk`, publicada dois minutos antes) e a da
peca de CONTROLE (`OhrGlJvnBoM`, 44 s conhecidos) voltaram as duas com **HTTP
000 e ZERO byte**. Pelo discriminador do 17/10 isso le como ROTA e nao como
peca — e estaria errado: na mesma chamada o `example.com` tambem devolveu
**000**. Nao foi a rota do YouTube, foi o sandbox sem egresso.

**E o `modo_de_fechamento` dizia `consentimento`**, porque o ramo final dele
perguntava se o corpo tem `lengthSeconds` e corpo VAZIO nao tem. Isto e uma
afirmacao sobre a parede do `CONSENT` do YouTube a partir de uma falha em que o
YouTube nunca foi alcancado — e a parede, medida em 16/10, vem com **1,2 MB**.
Zero byte nao e parede nenhuma.

O que estes testes cobram e a FORMA da saida: com o discriminador na mao ele
NOMEIA `sem_egresso`; sem o discriminador ele devolve `indeterminado` em vez de
escolher, do jeito que o `porta1` recusa janela curta. E eles proibem o modo que
eu NAO medi — neutro respondendo e o YouTube nao —, porque nomea-lo seria
limiar sem procedencia (§10).
"""
import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "vivacidade_publica.py")
sys.path.insert(0, FABRICA)

import vivacidade_publica as VP  # noqa: E402

PAREDE = ("x" * 1200) + "CONSENT" + ("y" * 1200)   # 200 com pagina grande
SORRY = "https://www.google.com/sorry/index?continue=..."


def test_corpo_vazio_com_o_neutro_FORA_e_sem_egresso():
    assert VP.modo_de_fechamento("", "", neutro_respondeu=False) == "sem_egresso"


def test_corpo_vazio_SEM_a_sonda_do_neutro_recusa_em_vez_de_escolher():
    """Sem o discriminador os tres casos sao indistinguiveis — e ele diz isso."""
    assert VP.modo_de_fechamento("", "") == "indeterminado"


def test_corpo_vazio_com_o_neutro_DENTRO_tambem_e_indeterminado():
    """O caso 'o neutro responde e o YouTube nao' eu NAO medi (§10)."""
    assert VP.modo_de_fechamento("", "", neutro_respondeu=True) == "indeterminado"


def test_a_PAREDE_continua_sendo_consentimento_e_ela_e_GRANDE():
    """Contraprova no outro sentido: sem ela, 'vazio != parede' passaria sozinho."""
    assert len(PAREDE) > 1000
    assert VP.modo_de_fechamento(PAREDE) == "consentimento"
    assert VP.modo_de_fechamento(PAREDE, neutro_respondeu=False) == "consentimento"


def test_o_LIMITE_continua_sendo_lido_nos_dois_lugares():
    assert VP.modo_de_fechamento("", SORRY) == "limite"
    assert VP.modo_de_fechamento("..." + SORRY + "...") == "limite"
    # e ele vence a sonda do neutro, porque /sorry E resposta do Google
    assert VP.modo_de_fechamento("", SORRY, neutro_respondeu=False) == "limite"


def test_a_rota_ABERTA_segue_aberta():
    assert VP.modo_de_fechamento('"lengthSeconds":"44"') == "aberta"


def test_nenhum_modo_afirma_recusa_do_youtube_porque_eu_nao_a_medi():
    """Proibe o quarto modo inventado, por AST sobre as constantes devolvidas."""
    arvore = ast.parse(open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "modo_de_fechamento"]
    assert len(alvo) == 1
    # Todo literal de texto DENTRO de um `return` e um valor devolvido — num
    # ternario os dois ramos sao. Casar so `Return -> Constant` perdia o
    # `sem_egresso`, que mora num ternario: o teste estava errado, nao o modulo.
    devolvidos = set()
    for no in ast.walk(alvo[0]):
        if isinstance(no, ast.Return) and no.value is not None:
            for dentro in ast.walk(no.value):
                if isinstance(dentro, ast.Constant) and isinstance(dentro.value, str):
                    devolvidos.add(dentro.value)
    assert devolvidos == {"limite", "consentimento", "aberta",
                          "sem_egresso", "indeterminado"}, devolvidos


def test_o_incidente_MEDIDO_continua_escrito_no_modulo():
    fonte = open(MODULO, encoding="utf-8").read()
    for marca in ("sem_egresso", "example.com", "1,2 MB", "ZERO\n    byte"):
        assert marca.replace("\n    ", " ") in fonte.replace("\n    ", " "), (
            "conserto sem o incidente escrito volta calado: falta %r" % marca)
