"""Eu escrevi a paleta a MAO e os dez portoes passaram limpos — 20/10, 00:3x.

Escrevendo o `epomeno-epipedo-s071` eu inventei a paleta de cabeca, e as NOVE
chaves contradiziam a do canal. O `CLAUDE.md` diz desde 19/10 que a identidade
visual sai de `temas_do_dono.paleta_do_canal` e **nunca se escreve a mao** — e o
`antes_do_render` rodou os dez portoes baratos LIMPOS com a paleta errada.

O custo e exatamente o que o dono reclamou em 19/10 (*"me parecem todos a mesma
dinamica... em todos os canais"*): peca com identidade inventada, com portao
verde.

A FORMA DESTES TESTES: a varredura sai do DISCO e reprova por vacuidade, a
contraprova vai nos DOIS sentidos (a peca certa sai compativel, e a mesma peca
com UMA chave trocada e acusada), o conjunto que contradiz tem de ser MAIORIA —
e por isso que isto nao e portao —, a delegacao e cobrada por AST, e um teste
**falha se os portoes passarem a pegar paleta errada**, porque ai esta nota se
rele em vez de ficar.
"""
import ast
import copy
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "paleta_da_spec.py")
sys.path.insert(0, FABRICA)

import paleta_da_spec as PS  # noqa: E402
import temas_do_dono as TD  # noqa: E402


def _spec_viva():
    """Uma spec de short de canal VIVO cuja paleta esta compativel."""
    d = PS.distribuicao()
    assert d["compativeis"], "sem spec compativel o arquivo nao mede nada"
    for nome in reversed(d["compativeis"]):
        p = os.path.join(FABRICA, "specs", nome + ".json")
        sp = json.load(open(p, encoding="utf-8"))
        if sp.get("short"):
            return p, sp
    raise AssertionError("nenhuma compativel com short")


# ---------------------------------------------------------------- a varredura

def test_a_varredura_sai_do_DISCO_e_nao_fica_vazia():
    d = PS.distribuicao()
    total = len(d["contradizem"]) + len(d["compativeis"]) + len(d["sem_paleta"])
    assert total >= 100, "varredura pequena nao mede o acervo: %d" % total


def test_os_que_CONTRADIZEM_sao_MAIORIA_e_e_por_isso_que_nao_e_portao():
    d = PS.distribuicao()
    assert len(d["contradizem"]) > len(d["compativeis"]), (
        "se a maioria passar a ser compativel, isto pode virar portao e esta "
        "nota tem de ser RELIDA: %d contra %d"
        % (len(d["contradizem"]), len(d["compativeis"])))


# -------------------------------------------- contraprova nos dois sentidos

def test_a_peca_CERTA_sai_compativel():
    _, sp = _spec_viva()
    assert not PS.conflitos(sp)["conflitos"]


def test_UMA_chave_trocada_JA_e_acusada():
    _, sp = _spec_viva()
    canal = PS.conflitos(sp)["canal"]
    chave = sorted(TD.paleta_do_canal(canal))[0]
    torta = copy.deepcopy(sp)
    torta["paleta"][chave] = "#123456"
    v = PS.conflitos(torta)
    assert list(v["conflitos"]) == [chave], v


def test_subconjunto_NAO_e_contradicao():
    """Foi contar assim que inflou a minha primeira medicao (725)."""
    _, sp = _spec_viva()
    menos = copy.deepcopy(sp)
    chave = sorted(menos["paleta"])[0]
    del menos["paleta"][chave]
    assert not PS.conflitos(menos)["conflitos"]


# ------------------------------------------------------- o portao vai LIMPO

def test_os_portoes_baratos_passam_LIMPOS_com_a_paleta_ERRADA(tmp_path):
    """E a base da conclusao: se eles passarem a pegar, esta nota se rele."""
    import antes_do_render as AR
    caminho, sp = _spec_viva()
    torta = copy.deepcopy(sp)
    for k in torta["paleta"]:
        torta["paleta"][k] = "#123456"
    # o nome do ARQUIVO tem de ser o do pacote: o `identidade` confere os dois,
    # e a primeira versao deste teste reprovou por isso — o teste estava errado,
    # nao o modulo, e a reprovacao nao era o portao pegando a paleta.
    alvo = tmp_path / os.path.basename(caminho)
    alvo.write_text(json.dumps(torta, ensure_ascii=False), encoding="utf-8")
    ruins = {k: v for k, v in AR.portoes(str(alvo)).items() if v}
    assert not ruins, (
        "os portoes passaram a PEGAR paleta errada — releia a nota de 20/10 em "
        "vez de manter o instrumento como unica cobertura: %s" % ruins)
    # e o instrumento acusa o que eles deixam passar
    assert PS.conflitos(torta)["conflitos"]


# --------------------------------------------------------------- a delegacao

def test_a_paleta_e_DELEGADA_e_nenhum_hex_mora_neste_modulo():
    fonte = open(MODULO, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    chamadas = {
        "%s.%s" % (n.func.value.id, n.func.attr)
        for n in ast.walk(arvore)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
    }
    assert "temas_do_dono.paleta_do_canal" in chamadas, chamadas
    assert any(c.startswith("mod_canal.") or c.startswith("canal.")
               for c in chamadas), chamadas
    corpo = fonte.split('"""', 2)[2]
    import re
    hexes = re.findall(r"#[0-9A-Fa-f]{6}", corpo)
    assert hexes == [] or set(hexes) == {"#123456"}, (
        "hex no corpo criaria o TERCEIRO dono da identidade visual: %s" % hexes)


def test_ele_INFORMA_e_o_codigo_de_saida_e_SEMPRE_zero():
    caminho, _ = _spec_viva()
    r = subprocess.run([sys.executable, MODULO, caminho], cwd=FABRICA,
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-600:]
    assert "PALETA de" in r.stdout


def test_o_pedido_do_dono_continua_citado_no_modulo():
    fonte = open(MODULO, encoding="utf-8").read()
    for marca in ("mesma dinamica", "nunca", "19/10"):
        assert marca in fonte, "falta %r: conserto sem motivo volta calado" % marca
