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
    """RETRATADO NO LUGAR em 20/10 as 09:3x: o neutro calado NAO bastava.

    A versao original deste teste cobrava `sem_egresso` com o host neutro como
    UNICO controle. Medido naquela rodada: a sonda e
    `curl -s -o ARQ -w '%{http_code}'`, e quando o `-o` nao consegue abrir o
    arquivo o curl sai em 23 e o `%{http_code}` imprime o MESMO 000 — logo o
    000 do neutro tambem e "a resposta nao tinha onde ser gravada". O teste
    estava afirmando a CAUSA com um controle a menos; o modulo agora pede os
    dois, e a propriedade cobrada aqui passou a ser essa.
    """
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False, sonda_pode_gravar=True,
        politica_negou=False) == "sem_egresso"
    # e o neutro SOZINHO nao conclui mais — ver
    # tests/test_o_000_tambem_e_a_RESPOSTA_sem_onde_gravar.py
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False) == "indeterminado"
    # RETRATADO OUTRA VEZ em 20/10 as 11:4x: com os dois controles e SEM a
    # leitura do proxy, `sem_egresso` tambem era afirmacao de CAUSA — o 000 em
    # todos os hosts e compativel com uma POLITICA que nega todo CONNECT, e foi
    # isso que o `__agentproxy/status` mostrou, nomeando `example.com:443`.
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False, sonda_pode_gravar=True
    ) == "indeterminado"


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
    assert VP.modo_de_fechamento(
        PAREDE, neutro_respondeu=False,
        sonda_pode_gravar=True) == "consentimento"


def test_o_LIMITE_continua_sendo_lido_nos_dois_lugares():
    assert VP.modo_de_fechamento("", SORRY) == "limite"
    assert VP.modo_de_fechamento("..." + SORRY + "...") == "limite"
    # e ele vence a sonda do neutro, porque /sorry E resposta do Google
    assert VP.modo_de_fechamento("", SORRY, neutro_respondeu=False) == "limite"


def test_a_rota_ABERTA_segue_aberta():
    assert VP.modo_de_fechamento('"lengthSeconds":"44"') == "aberta"


def test_nenhum_modo_afirma_recusa_do_youtube_porque_eu_nao_a_medi():
    """Proibe modo INVENTADO, por AST sobre as constantes devolvidas.

    RETRATADO NO LUGAR em 20/10 as 11:4x, e e a classe 743/753/761: eu cravei o
    CONJUNTO de modos quando a afirmacao era uma PROPRIEDADE — "nenhum modo sem
    medicao escrita". Quando o `negado_por_politica` entrou MEDIDO (o
    `__agentproxy/status` nomeando `example.com:443` com 403 ao CONNECT), este
    teste reprovou um comportamento CORRETO. E afrouxar a guarda seria o avesso
    do trabalho, logo ela ficou: todo modo devolvido tem de estar NOMEADO no
    docstring da propria funcao, que e onde a medicao dele mora. Modo novo sem
    medicao escrita continua reprovando.
    """
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
    doc = ast.get_docstring(alvo[0]) or ""
    sem_medicao = [m for m in devolvidos
                   if m != "indeterminado" and m not in doc]
    assert not sem_medicao, (
        "modo devolvido sem a medicao escrita no docstring da funcao: %s"
        % sem_medicao)
    # e a RECUSA tem de continuar existindo, senao a funcao volta a escolher
    assert "indeterminado" in devolvidos, devolvidos
    # contraprova de que o conjunto nao esta vazio nem colapsou
    assert {"limite", "consentimento", "aberta"} <= devolvidos, devolvidos


def test_o_incidente_MEDIDO_continua_escrito_no_modulo():
    fonte = open(MODULO, encoding="utf-8").read()
    for marca in ("sem_egresso", "example.com", "1,2 MB", "ZERO\n    byte"):
        assert marca.replace("\n    ", " ") in fonte.replace("\n    ", " "), (
            "conserto sem o incidente escrito volta calado: falta %r" % marca)
