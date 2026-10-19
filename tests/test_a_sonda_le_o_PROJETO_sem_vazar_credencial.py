"""A sonda passou a dizer se o teto de cota e 6/dia na FROTA ou 6/dia por CANAL.

POR QUE (19/10/2026). Em 18/10 o zip v2.0 do dono expos um erro nosso: o teto de
envio e `10.000 / 1.600` = SEIS videos por dia **por projeto** do Google Cloud, e
nao os "~40 videos/janela" que a rotina dizia. Isso abriu uma pergunta cujo
resultado muda o teto por um fator de TRES — seis por canal (dezoito na frota) ou
seis para os tres juntos? —, e a resposta depende de a frota usar um projeto ou
tres. O `execute_sql` esta negado, logo o banco nao responde.

A resposta nao precisava do banco: o `client_id` de um cliente OAuth comeca com o
NUMERO DO PROJETO, que nao e segredo. A `sonda_oauth` ja le o `YT_OAUTH_JSON` no
runner e ja existe com a trava de nunca imprimir segredo.

**O que este arquivo trava e a TRAVA, nao o achado** — porque o achado ainda nao
foi medido (a sonda precisa rodar), e porque uma sonda que vaza credencial e pior
que nao ter sonda:

  1. so os digitos iniciais saem, nunca o `client_id` inteiro;
  2. entrada mal formada devolve VAZIO, e nao "o que sobrou";
  3. o veredito da cota NAO inventa limiar: ele deriva de 10.000/1.600;
  4. com projeto lido em menos canais que a frota, o relato DIZ isso em vez de
     generalizar;
  5. e as travas antigas da sonda continuam de pe (nada de refresh token,
     client_secret ou access token no que ela imprime).
"""
import ast
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))
FONTE = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")

import sonda_oauth as so  # noqa: E402

CID_BOM = "123456789012-a1b2c3d4e5f6g7h8.apps.googleusercontent.com"


def test_devolve_SO_os_digitos_do_projeto():
    assert so.projeto_do_client_id(CID_BOM) == "123456789012"


def test_nao_devolve_a_parte_ALEATORIA_do_client_id():
    """A metade aleatoria e o que mais se parece com credencial."""
    saida = so.projeto_do_client_id(CID_BOM)
    assert "a1b2c3d4e5f6g7h8" not in saida
    assert "googleusercontent" not in saida
    assert saida in CID_BOM and len(saida) < len(CID_BOM) / 2


def test_entrada_MAL_FORMADA_devolve_vazio_e_nao_o_resto():
    """Devolver "o resto" e como um client_id torto viraria vazamento."""
    for ruim in ("", None, "sem-digito.apps.googleusercontent.com",
                 "12345-curto.apps.googleusercontent.com", "semhifen", "abc-123"):
        assert so.projeto_do_client_id(ruim) == "", repr(ruim)


def test_o_veredito_de_projeto_COMPARTILHADO_fala_da_FROTA(capsys):
    so._relata_cota({"labtreinamento": "111111111111",
                     "epomeno-epipedo": "111111111111",
                     "kolejny-poziom": "111111111111"})
    saida = capsys.readouterr().out
    assert "COMPARTILHAM" in saida
    assert "FROTA" in saida
    assert "6" in saida


def test_o_veredito_de_projetos_DISTINTOS_fala_por_CANAL(capsys):
    so._relata_cota({"labtreinamento": "111111111111",
                     "epomeno-epipedo": "222222222222",
                     "kolejny-poziom": "333333333333"})
    saida = capsys.readouterr().out
    assert "POR" in saida and "CANAL" in saida
    assert "3 projetos distintos" in saida
    assert "18" in saida, "a conta da frota (6 x 3) nao saiu"


def test_projeto_lido_em_MENOS_canais_nao_vira_veredito_da_frota(capsys):
    """Dois de tres nao autoriza falar pelos tres — e o 679/698 outra vez."""
    so._relata_cota({"labtreinamento": "111111111111",
                     "epomeno-epipedo": "111111111111"})
    saida = capsys.readouterr().out
    assert "2 de 3" in saida or "so 2" in saida
    assert "nao para a frota" in saida


def test_sem_projeto_nenhum_o_teto_sai_INDETERMINADO(capsys):
    so._relata_cota({"labtreinamento": "", "epomeno-epipedo": ""})
    saida = capsys.readouterr().out
    assert "INDETERMINADO" in saida
    assert "6/dia na frota" in saida and "6/dia por canal" in saida


def test_o_veredito_DERIVA_o_seis_e_nao_o_crava_sozinho():
    """Limiar sem procedencia e criterio inventado: a conta vai escrita."""
    assert "10.000/1.600" in FONTE
    assert "1.600" in FONTE and "10.000" in FONTE


def test_as_TRAVAS_antigas_da_sonda_continuam_de_pe():
    """Uma sonda que vaza segredo e pior que nao ter sonda.

    Por AST, e nao por casar prosa: o docstring do modulo NOMEIA refresh token e
    client_secret para se explicar, e procurar a palavra pegaria a explicacao em
    vez do codigo. E o mesmo motivo do teste por AST do 729.

    A primeira versao deste assert procurava a PALAVRA "refresh_token" no dump
    de toda chamada que imprime, e reprovou — porque a sonda imprime uma
    mensagem de AJUDA que nomeia as chaves esperadas
    (`{"client_id", "client_secret", "refresh_token"}`). **Nomear a chave nao e
    vazar o valor**, e proibir a grafia proibiria a mensagem de ajuda.

    E e a TERCEIRA vez em dois dias que eu escrevo um teste contra a GRAFIA
    quando a propriedade era outra: em 16/10 proibi "N de N acima" e proibi a
    propria retratacao, e em 18/10 as 23:4x proibi "~500 unidades" e proibi a
    correcao que a cita. A regra que fica: **proiba o CAMINHO DO VALOR, nunca a
    palavra.**

    O que se cobra aqui: nenhum no que LE o valor de um segredo (`cfg[...]`,
    `os.environ[...]`, atributo) alcanca uma chamada que imprime. Literal de
    string que apenas nomeia a chave passa.
    """
    arvore = ast.parse(FONTE)
    SEGREDOS = ("refresh_token", "client_secret", "access_token", "client_id")
    impressos = 0
    for no in ast.walk(arvore):
        if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id in ("print", "nota", "aviso")):
            continue
        impressos += 1
        for dentro in ast.walk(no):
            # leitura por indice: cfg["refresh_token"], os.environ["..."]
            if isinstance(dentro, ast.Subscript):
                chave = getattr(dentro.slice, "value", None)
                assert chave not in SEGREDOS, (
                    f"{chave!r} e LIDO dentro de uma chamada que imprime"
                )
            # leitura por atributo: cfg.refresh_token
            if isinstance(dentro, ast.Attribute):
                assert dentro.attr not in SEGREDOS, dentro.attr
    assert impressos >= 5, f"a varredura por AST achou so {impressos} prints"

    # E o client_id so pode chegar perto de um print ATRAVES do extrator, que
    # devolve digitos. Conferido no CODIGO: toda leitura dele passa por ele.
    assert "projeto_do_client_id(cfg[\"client_id\"])" in FONTE
