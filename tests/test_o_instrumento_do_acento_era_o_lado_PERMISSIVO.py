# -*- coding: utf-8 -*-
"""O instrumento do acento era o lado PERMISSIVO — 21/10 as 15:3x.

Escrevendo o `labtreinamento-s101` eu recebi, na MESMA chamada do
`antes_do_render`, dois vereditos opostos sobre o mesmo texto: o portao
`ortografia` REPROVOU (1,7% das letras contra 4,5% nas specs de pt que acentuam)
e o `acento.py` disse *"carrega acento, como as outras deste idioma"*, porque
1,65% esta acima do piso OBSERVADO dele (1,57%).

**Conselho que o portao reprova e pior que conselho ausente** — e a quarta vez
desta familia, a mesma do `mira.orcamento` em 19/10 as 17:2x.

**Os dois criterios sao diferentes de PROPOSITO:** o portao compara com as
vizinhas do MESMO canal que acentuam; o instrumento, com a distribuicao do
IDIOMA. Nenhum esta errado — o errado era o instrumento nao dizer o do outro.

**E o buraco e LATENTE: no acervo os dois concordam, 264 de 264.** O caso que o
revelou e a peca desta rodada, e por isso o lugar disto nao e portao novo.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import acento      # noqa: E402
import prontidao   # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")

# A narracao da PRIMEIRA versao da peca desta rodada — o caso MEDIDO. Ela vive
# aqui como FIXTURE e nao como spec do disco, porque a peca publicada tem a
# narracao CORRIGIDA: ancorar no disco faria este arquivo medir o conserto em
# vez do defeito.
NARRACAO_V1 = [
    "A sua planilha tem uma linha por pessoa?",
    "Cada treinamento vence na própria data.",
    "Quem fez três treinamentos ocupa três linhas.",
    "Juntar tudo numa linha esconde o que importa.",
    "Com as linhas certas, ordene pelo vencimento.",
    "O topo da lista é a sua fila de trabalho.",
    "Olhe a sua lista hoje, e depois inscreva-se.",
]


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _spec_v1():
    alvo = os.path.join(SPECS, "labtreinamento-s101.json")
    assert os.path.exists(alvo), (
        "PERDEU A ANCORA: a peca que produziu o achado saiu do disco")
    sp = json.load(open(alvo, encoding="utf-8"))
    assert len(sp["short"]) == len(NARRACAO_V1), (
        "a peca mudou de tamanho (%d cenas contra %d na fixture): a reproducao"
        " do caso medido nao vale mais e esta nota tem de ser relida"
        % (len(sp["short"]), len(NARRACAO_V1)))
    for c, n in zip(sp["short"], NARRACAO_V1):
        c["nar"] = n
    return alvo, sp


def test_o_caso_MEDIDO_divergia_e_o_relato_agora_o_NOMEIA():
    alvo, v1 = _spec_v1()
    v = acento.veredito(v1)
    assert not v["suspeita"], (
        "o instrumento passou a suspeitar da narracao v1: o criterio dele"
        " mudou, e ai esta nota mede outra coisa")
    assert prontidao._gate_ortografia(alvo, v1), (
        "o portao parou de reprovar a narracao v1: PERDEU A ANCORA")
    linha = acento._linha_do_portao(alvo, v1, bool(v["suspeita"]))
    assert "REPROVA ISTO" in linha and "PERMISSIVO" in linha, (
        "o relato nao NOMEIA a divergencia: %r" % linha)


def test_a_peca_CORRIGIDA_sai_com_os_dois_de_acordo():
    """Contraprova no outro sentido: senao a frase sairia sempre."""
    alvo = os.path.join(SPECS, "labtreinamento-s101.json")
    sp = json.load(open(alvo, encoding="utf-8"))
    v = acento.veredito(sp)
    assert not v["suspeita"], "a peca publicada passou a ser suspeita"
    assert not prontidao._gate_ortografia(alvo, sp), (
        "o portao passou a reprovar a peca publicada")
    linha = acento._linha_do_portao(alvo, sp, bool(v["suspeita"]))
    assert "tambem nao reprova" in linha, (
        "o ramo de ACORDO nao sai: sem ele a ausencia da frase fica"
        " indistinguivel de o relato nao ter perguntado — %r" % linha)
    assert "REPROVA ISTO" not in linha


def test_a_frase_sai_nos_QUATRO_cruzamentos():
    """Os dois vereditos cruzados: quatro frases, todas distintas."""
    alvo, v1 = _spec_v1()
    sp = json.load(open(alvo, encoding="utf-8"))
    frases = {
        acento._linha_do_portao(alvo, v1, False),      # portao sim, instr. nao
        acento._linha_do_portao(alvo, v1, True),       # os dois sim
        acento._linha_do_portao(alvo, sp, True),       # instr. sim, portao nao
        acento._linha_do_portao(alvo, sp, False),      # os dois nao
    }
    assert len(frases) == 4, (
        "os quatro cruzamentos nao dao quatro frases distintas: %r" % frases)
    for f in frases:
        assert "PORTAO" in f, "frase sem o nome do portao: %r" % f


def test_no_ACERVO_os_dois_CONCORDAM_e_o_numero_e_reconferido():
    """A medida que decide o LUGAR do conserto: 264 de 264 concordam (753)."""
    n = concordam = 0
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        n += 1
        v = acento.veredito(d) or {}
        if bool(prontidao._gate_ortografia(f, d)) == bool(v.get("suspeita")):
            concordam += 1
    assert n >= 200, (
        "so %d spec(s) de short solto: a medida ficou vacua" % n)
    assert concordam == n, (
        "o acervo deixou de concordar (%d de %d): o buraco virou ATIVO e a"
        " decisao de nao fazer portao tem de ser relida" % (concordam, n))


def test_o_veredito_e_DELEGADO_ao_portao():
    fonte = open(os.path.join(RAIZ, "fabrica", "acento.py"),
                 encoding="utf-8").read()
    defs = {x.name: x for x in ast.walk(ast.parse(fonte))
            if isinstance(x, ast.FunctionDef)}
    assert "veredito_do_portao" in defs, "o delegador desapareceu"
    corpo = _codigo(defs["veredito_do_portao"])
    assert "prontidao" in corpo and "_gate_ortografia" in corpo, (
        "ele deixou de chamar o portao: %r" % corpo)
    for proibido in ("DIACRITICOS", "statistics", "median"):
        assert proibido not in corpo, (
            "ele reimplementou o criterio do portao (%r): seria o segundo dono"
            % proibido)


def test_o_portao_continua_SEM_importar_este_modulo():
    """O grafo so pode ir num sentido — e o teste de 19/10 cobra o outro lado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                 encoding="utf-8").read()
    for n in ast.walk(ast.parse(fonte)):
        if isinstance(n, ast.Import):
            for a in n.names:
                assert a.name != "acento", (
                    "o `prontidao` passou a importar o `acento`: com o import"
                    " novo do outro lado isso fecha um CICLO")
        if isinstance(n, ast.ImportFrom):
            assert n.module != "acento", (
                "o `prontidao` passou a importar do `acento`")


def test_o_codigo_de_saida_segue_ZERO():
    """Ele INFORMA: ganhar a frase do portao nao pode torna-lo um portao."""
    import subprocess
    alvo = os.path.join(SPECS, "labtreinamento-s101.json")
    r = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "acento.py"), alvo],
                       capture_output=True, text=True)
    assert r.returncode == 0, (
        "o `acento.py` passou a reprovar (saida %d)" % r.returncode)
    assert "PORTAO" in r.stdout, "a frase do portao nao chega ao CLI"


def test_a_falha_na_consulta_NAO_vira_aprovacao():
    v1 = _spec_v1()[1]
    linha = acento._linha_do_portao("/caminho/que/nao/existe.json", v1, False)
    assert "NAO CONSULTADO" in linha or "REPROVA" in linha, (
        "consulta impossivel saiu como aprovacao: %r" % linha)
    if "NAO CONSULTADO" in linha:
        assert "nao e aprovacao" in linha.lower(), (
            "ela nao diz que ausencia de consulta nao e aprovacao")


def test_o_motivo_e_a_medida_continuam_escritos():
    fonte = open(os.path.join(RAIZ, "fabrica", "acento.py"),
                 encoding="utf-8").read()
    assert "labtreinamento-s101" in fonte, (
        "a peca que produziu o achado saiu do modulo")
    assert "264" in fonte, (
        "a medida que decide o LUGAR do conserto saiu do modulo")
    assert "PERMISSIVO" in fonte, (
        "a direcao da divergencia — o instrumento e o lado permissivo — saiu"
        " do modulo")
