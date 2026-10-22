# -*- coding: utf-8 -*-
"""A sonda aceitava o ID da peca como HOST — e respondia como se tivesse sondado.

Medido em 22/10 as 07:2x. A `sonda_e_modo` aceita host OU URL e monta
`https://%s/` para o que nao tem esquema; eu lhe passei os IDS das pecas
(`-ZjnZjLVXss`, `OhrGlJvnBoM`), ela montou `https://-ZjnZjLVXss/`, levou HTTP
000 e o relato imprimiu a linha como se a peca tivesse sido sondada.

O que o arquivo cobra e a RECUSA (a familia do `porta1` recusando janela curta)
e a CONCORDANCIA das duas metades: o alvo, o host NEUTRO e o corpo do YouTube
tem de sair do MESMO dono, porque foi medi-los por regras diferentes que
produziu as notas de 00:3x (dois caminhos de saida) e 01:1x (duas ideias de
host) nesta mesma funcao.
"""
import ast
import inspect
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import vivacidade_publica as VP  # noqa: E402

# HISTORIA: foi esta a chamada que eu fiz. Nenhum assert depende do id em si —
# o que o arquivo mede e a PROPRIEDADE "nao tem esquema e nao tem ponto"
# (743/753/761), e os ids mudam toda rodada.
CHAMADA_DE_07H = ["-ZjnZjLVXss", "OhrGlJvnBoM", "example.com"]

BONS = ["https://www.youtube.com/watch?v=X",
        "www.youtube.com",
        "www.youtube.com:443",
        "example.com",
        "https://example.com/"]


def test_id_de_peca_LEVANTA_em_vez_de_virar_host():
    for mau in ("-ZjnZjLVXss", "OhrGlJvnBoM", "dQw4w9WgXcQ"):
        with pytest.raises(VP.AlvoSemHost):
            VP.alvo_de_sonda(mau)


def test_alvo_vazio_LEVANTA():
    for mau in ("", None, "   "):
        with pytest.raises(VP.AlvoSemHost):
            VP.alvo_de_sonda(mau)


def test_contraprova_no_outro_sentido_host_e_URL_continuam_passando():
    # Sem isto, bastaria levantar sempre para o arquivo inteiro passar.
    for bom in BONS:
        a = VP.alvo_de_sonda(bom)
        assert a["host"], (bom, a)
        assert "://" in a["url"], (bom, a)
        assert a["host"] == VP.host_de(bom), (bom, a)


def test_o_YOUTUBE_se_decide_pelo_HOST_e_nao_pela_string_crua():
    # A URL do `watch` tem "youtube" na string E no host; o id da peca nao tem
    # em nenhum dos dois. O que distingue um caso do outro e o HOST.
    assert VP.alvo_de_sonda("https://www.youtube.com/watch?v=X")["e_youtube"]
    assert VP.alvo_de_sonda("www.youtube.com:443")["e_youtube"]
    assert not VP.alvo_de_sonda("example.com")["e_youtube"]
    # e um host que CITA youtube no caminho e nao no host nao e do YouTube
    assert not VP.alvo_de_sonda("https://example.com/youtube")["e_youtube"]


def test_o_CUSTO_dos_dois_discriminadores_e_MEDIDO_e_nao_afirmado():
    """Sem isto, "eu errei o alvo" seria afirmacao minha e nao medida."""
    crua_neutros = [h for h in CHAMADA_DE_07H if "youtube" not in h]
    crua_corpo = [h for h in CHAMADA_DE_07H if "youtube" in h]
    # a regra CRUA classificava os TRES como neutros e NENHUM como do YouTube
    assert len(crua_neutros) == len(CHAMADA_DE_07H), crua_neutros
    assert crua_corpo == [], crua_corpo
    # e o dono novo RECUSA a chamada inteira, em vez de responder sobre nada
    with pytest.raises(VP.AlvoSemHost):
        [VP.alvo_de_sonda(h) for h in CHAMADA_DE_07H]
    # a forma CERTA da mesma pergunta classifica UM neutro e DOIS do YouTube
    bons = ["https://www.youtube.com/watch?v=-ZjnZjLVXss",
            "https://www.youtube.com/watch?v=OhrGlJvnBoM",
            "https://example.com/"]
    alvos = [VP.alvo_de_sonda(h) for h in bons]
    assert sum(1 for a in alvos if not a["e_youtube"]) == 1, alvos
    assert sum(1 for a in alvos if a["e_youtube"]) == 2, alvos


def test_as_DUAS_metades_da_sonda_saem_do_MESMO_dono_por_AST():
    fonte = inspect.getsource(VP.sonda_e_modo)
    arvore = ast.parse(fonte.lstrip())
    # nenhuma comparacao crua com a string "youtube" dentro da sonda: ela foi
    # a regra que classificou id de peca como host neutro
    for no in ast.walk(arvore):
        if isinstance(no, ast.Constant) and no.value == "youtube":
            raise AssertionError(
                "a sonda voltou a decidir 'e do YouTube?' pela string crua; "
                "quem decide e `alvo_de_sonda`, pelo HOST")
    # e ela tem de CHAMAR o dono (import sem chamada e a classe dos layouts
    # mortos)
    chama = [n.func.id for n in ast.walk(arvore)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    assert "alvo_de_sonda" in chama, chama


def test_a_sonda_RECUSA_a_chamada_errada_antes_de_tocar_a_rede(tmp_path):
    # Ela nao pode gastar requisicao para depois descobrir que o alvo nao e
    # host: a recusa vem do dono, na montagem dos alvos.
    with pytest.raises(VP.AlvoSemHost):
        VP.sonda_e_modo(["-ZjnZjLVXss"], dir_sonda=str(tmp_path))


def test_o_motivo_e_o_limite_continuam_escritos_no_dono():
    d = VP.alvo_de_sonda.__doc__ or ""
    for pedaco in ("07:2x", "NEUTROS", "INALCANCAVEL", "ACIDENTE", "localhost"):
        assert pedaco in d, pedaco
    # a medida dos dois discriminadores vai no docstring, e o teste acima a
    # reconfere (753)
    assert "3 de 3" in d and "0 de 3" in d, d[:200]


def test_a_recusa_NOMEIA_o_que_fazer():
    try:
        VP.alvo_de_sonda("-ZjnZjLVXss")
    except VP.AlvoSemHost as e:
        msg = str(e)
    else:
        raise AssertionError("nao levantou")
    assert "watch" in msg, msg
    assert "-ZjnZjLVXss" in msg, msg


def test_o_modulo_nao_tem_SEGUNDO_dono_do_alvo():
    fonte = io.open(os.path.join(RAIZ, "fabrica", "vivacidade_publica.py"),
                    encoding="utf-8").read()
    arvore = ast.parse(fonte)
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        if no.name in ("alvo_de_sonda",):
            continue
        for sub in ast.walk(no):
            if (isinstance(sub, ast.BinOp)
                    and isinstance(sub.left, ast.Constant)
                    and isinstance(sub.left.value, str)
                    and "https://%s/" in sub.left.value):
                raise AssertionError(
                    "%s voltou a montar a URL da sonda por conta propria; "
                    "o dono e `alvo_de_sonda`" % no.name)
