# -*- coding: utf-8 -*-
"""Os limites da copy nao tinham quem dissesse quanto AINDA CABE.

**Medido em 20/10 as 21:3x.** Os portoes `copy` e `variedade` cobram cinco
limites da copy e respondem *"esta dentro?"* DEPOIS de ela existir. E a mesma
assinatura do `mira.orcamento` de 19/10 as 14:2x — e o custo desta sessao sao
SETE passadas: thumbnail com cinco palavras quatro vezes, titulo com 106
caracteres uma vez, e `## TAGS` em varias linhas duas vezes.

A forma dos testes segue a disciplina da semana: a varredura sai do DISCO e
reprova por vacuidade, TODO limite e cobrado como LIDO do dono por AST, a
FRONTEIRA e cobrada nos dois sentidos (folga ZERO passa, porque o portao reprova
ACIMA do teto e ABAIXO do piso), a prova chama o PORTAO e nao reimplementa a
regra, e um exige que isto NAO tenha virado portao.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import orcamento_da_copy as OC  # noqa: E402
import prontidao as P           # noqa: E402
import variedade as V           # noqa: E402

PISO_DE_SPECS = 100
FONTE = open(os.path.join(RAIZ, "fabrica", "orcamento_da_copy.py"),
             encoding="utf-8").read()


def _specs():
    saida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("short") and isinstance(d.get("copy"), str):
            saida.append((os.path.basename(f)[:-5], d))
    assert len(saida) >= PISO_DE_SPECS, (
        "a varredura achou %d specs com copy, menos que o piso de %d: o glob"
        " deixou de casar e TODO assert passaria por vacuidade"
        % (len(saida), PISO_DE_SPECS))
    return saida


def test_os_limites_sao_LIDOS_dos_donos():
    lim = OC.limites()
    assert lim["thumb_palavras"] == V.THUMB_MAX_PALAVRAS
    assert lim["gancho_palavras"] == V.GANCHO_MAX_PALAVRAS
    assert lim["descricao_min_palavras"] == P.MIN_PALAVRAS_DESCRICAO
    assert lim["descricao_max_chars"] == P.MAX_DESCRICAO - P.RESERVA_LINK_SHORT
    # e por AST: nenhum dos numeros dos donos aparece cravado no modulo
    arv = ast.parse(FONTE)
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    corpo = ast.unparse(defs["limites"])
    for proibido in (str(V.THUMB_MAX_PALAVRAS), str(V.GANCHO_MAX_PALAVRAS),
                     str(P.MIN_PALAVRAS_DESCRICAO), str(P.MAX_DESCRICAO)):
        assert proibido not in corpo, (
            "%r cravado em `limites`: o numero tem UM dono, e orcamento que"
            " cita outro numero que o portao e pior que orcamento ausente"
            % proibido)


def test_a_FRONTEIRA_vale_nos_DOIS_sentidos():
    """Folga ZERO PASSA: o portao reprova ACIMA do teto e ABAIXO do piso.

    A primeira versao usava `<= 0` e acusava a peca da rodada, que tem
    exatamente quatro palavras na thumbnail e passa o portao — o instrumento
    inventando achado na fronteira (725).
    """
    base = None
    for _, d in _specs():
        if OC.orcamento(d):
            base = d
            break
    assert base is not None, "nenhuma spec do disco rende orcamento"

    def _relato(th):
        q = json.loads(json.dumps(base))
        q["thumb"] = th
        return OC.relato(q)

    lim = V.THUMB_MAX_PALAVRAS
    no_limite = _relato({"l1": " ".join(["a"] * lim), "l2": ""})
    assert "JA ESTOURA" not in no_limite, (
        "thumbnail no limite EXATO foi acusada, e o portao a aceita")
    assert "LIMITE exato" in no_limite
    passou = _relato({"l1": " ".join(["a"] * (lim + 1)), "l2": ""})
    assert "JA ESTOURA" in passou, (
        "thumbnail com %d palavras nao foi acusada, e o portao reprova"
        % (lim + 1))
    # e a conferencia chama o PORTAO, nao a minha leitura
    q = json.loads(json.dumps(base))
    q["thumb"] = {"l1": " ".join(["a"] * (lim + 1)), "l2": ""}
    # `analisa` devolve (problemas, avisos) — uma TUPLA, e a primeira versao
    # deste assert chamou `.get` nela. Era o teste errado, nao o portao.
    problemas, _avisos = V.analisa(q)
    achados = [m for m in problemas if "thumbnail" in m]
    assert achados, (
        "o portao `variedade` nao reprovou a thumbnail de %d palavras: o teste"
        " estaria medindo a minha leitura" % (lim + 1))


def test_o_piso_da_descricao_tambem_e_cobrado_nos_dois_sentidos():
    base = None
    for _, d in _specs():
        o = OC.orcamento(d)
        if o and o["descricao_min_palavras"]["folga"] > 0:
            base = d
            break
    assert base is not None, "nenhuma spec com descricao acima do piso"
    o = OC.orcamento(base)
    assert o["descricao_min_palavras"]["sentido"] == "piso"
    curta = json.loads(json.dumps(base))
    curta["copy"] = curta["copy"].replace(
        o_desc := "", "")  # placeholder, a copy curta vem abaixo
    # monta uma copy valida com descricao ABAIXO do piso
    curta["copy"] = (
        "# x\n\n## TITULO\nt\n\n## TITULO SHORT\nts\n\n## DESCRICAO\n"
        + ("palavra " * 10)
        + "\n\n## COMENTARIO FIXADO\nc\n\n## HASHTAGS\n#a\n\n## TAGS\na, b\n")
    o2 = OC.orcamento(curta)
    assert o2 is None or o2["descricao_min_palavras"]["folga"] < 0, (
        "descricao de dez palavras nao ficou abaixo do piso")


def test_a_leitura_da_copy_e_DELEGADA_ao_dono():
    """Reimplementar a classificacao de secoes faria o orcamento medir uma copy
    que o portao le de outro jeito — foi assim que `## TAGS` em varias linhas
    saiu como "sem tags" sem eu entender por que."""
    arv = ast.parse(FONTE)
    defs = {d.name: d for d in ast.walk(arv) if isinstance(d, ast.FunctionDef)}
    corpo = ast.unparse(defs["_copy_lida"])
    assert "ler_copy" in corpo, (
        "`_copy_lida` deixou de delegar ao `publicar.ler_copy`: %r" % corpo)
    todo = ast.unparse(arv)
    for proibido in ("re.search", "re.findall", "## TITULO", "## DESCRICAO"):
        assert proibido not in todo, (
            "%r no modulo: segundo dono da classificacao de secoes" % proibido)


def test_o_relato_NOMEIA_o_caso_das_TAGS_em_varias_linhas():
    base = None
    for _, d in _specs():
        if OC.orcamento(d):
            base = d
            break
    r = OC.relato(base)
    assert "UMA linha" in r and "sem tags" in r, (
        "o relato nao nomeia o caso do `## TAGS` quebrado, que custou duas"
        " passadas nesta sessao: %r" % r)


def test_ele_mede_a_FROTA_e_nao_so_uma_peca():
    """Vacuidade do outro lado: se ele devolvesse None para a maioria, os
    asserts acima passariam medindo uma spec so."""
    specs = _specs()
    com = [n for n, d in specs if OC.orcamento(d) is not None]
    assert len(com) > len(specs) / 2, (
        "so %d de %d specs renderam orcamento: o instrumento cobre a minoria"
        % (len(com), len(specs)))


def test_isto_NAO_virou_portao_e_a_saida_e_ZERO():
    import subprocess
    arv = ast.parse(open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                         encoding="utf-8").read())
    nomes = []
    for n in ast.walk(arv):
        if isinstance(n, ast.Import):
            nomes += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            nomes.append(n.module or "")
    assert not any("orcamento_da_copy" in (m or "") for m in nomes), (
        "o `prontidao` passou a importar o orcamento: quem reprova sao os dois"
        " portoes, e este diz a FOLGA")
    alvo = None
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("short") and isinstance(d.get("copy"), str) and not d.get("longo"):
            alvo = f
            break
    assert alvo
    p = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "orcamento_da_copy.py"),
                        alvo], capture_output=True, text=True)
    assert p.returncode == 0, (
        "o orcamento passou a reprovar: codigo de saida %d" % p.returncode)
    assert "ORCAMENTO DA COPY" in p.stdout


def test_o_CHAMADOR_existe_no_antes_do_render():
    """Instrumento que ninguem chama e a classe dos layouts mortos."""
    fonte = open(os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
                 encoding="utf-8").read()
    arv = ast.parse(fonte)
    inst = None
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and any(
                getattr(t, "id", "") == "INSTRUMENTOS" for t in n.targets):
            inst = ast.literal_eval(n.value)
    assert inst, "`INSTRUMENTOS` desapareceu do `antes_do_render`"
    assert "orcamento_da_copy" in inst, (
        "o orcamento nao entrou na passada do `antes_do_render`: %r" % (inst,))


def test_as_SETE_passadas_continuam_escritas():
    for pedaco in ("s071", "s089", "s075", "s095", "106", "s072", "s092"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: sem os casos a friccao parece zelo e nao"
            " medicao" % pedaco)
    assert "friccao" in FONTE, (
        "o modulo deixou de dizer que isto e FRICCAO e nao buraco — nenhuma das"
        " sete chegou ao ar, e inflar isso seria achado inventado")
