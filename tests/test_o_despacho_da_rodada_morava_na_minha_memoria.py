# -*- coding: utf-8 -*-
"""A rota do despacho vivia na memoria, e nesta rodada eu digitei `true`.

MEDIDO em 22/10 as 23:5x: nos 30 dispatches anteriores do `frota.yml` o
passo `Conferir token do canal` saiu SKIPPED em 28 de 28 que rodaram, e na
UNICA vez em que ele rodou — esta rodada, porque eu passei `publicar=true`
— ele REPROVOU e o render inteiro foi pulado. O input tem DEFAULT `true`,
logo a rota da rodada e a NAO-padrao.

O que estes testes cobram e PROPRIEDADE e nao o numero: a rota recusa o
ramo medido, os payloads saem da SPEC e dos DONOS, e o `estado_b64` nao
pode ser remontado em lugar nenhum.
"""
import ast
import base64
import inspect
import json
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
if FABRICA not in sys.path:
    sys.path.insert(0, FABRICA)

import despacho_da_rodada as DR  # noqa: E402
import estado_ponte as EP  # noqa: E402

PECA = "labtreinamento-s112"      # a peca desta rodada, e ela e HISTORIA:
RUN_DO_RENDER = "39874476913"     # nenhum assert depende dos valores dela


def _corpo(mod, nome):
    """A fonte de UMA funcao, desindentada — `textwrap.dedent` e nao
    `inspect.cleandoc`, que desindenta a linha do `def` e deixa o corpo
    torto (a licao de 22/10 as 08:3x)."""
    import textwrap
    return textwrap.dedent(inspect.getsource(getattr(mod, nome)))


def _nomes_chamados(fonte):
    arv = ast.parse(fonte)
    fora = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Call):
            fora.add(ast.unparse(n.func))
    return fora


def _peca_do_disco():
    """A peca de prova sai do DISCO, por PROPRIEDADE: a mais recente spec de
    short solto do `labtreinamento`. Nomear um pacote seria identidade onde
    ha propriedade (743/753/761) e envelhece a cada rodada."""
    import glob
    cand = []
    for c in glob.glob(os.path.join(FABRICA, "specs", "labtreinamento-s*.json")):
        with open(c, encoding="utf-8") as f:
            sp = json.load(f)
        if sp.get("short") and not sp.get("longo"):
            cand.append(os.path.basename(c)[:-5])
    assert len(cand) >= 5, (
        "menos de cinco specs de short solto do labtreinamento no disco — o "
        "arquivo perdeu a ancora e passaria por vacuidade")
    return sorted(cand)[-1]


# ---------------------------------------------------------------- a rota

def test_a_rota_medida_e_publicar_FALSE():
    assert DR.PUBLICAR_NO_RENDER is False
    p = DR.payload_do_render(_peca_do_disco())
    assert p["publicar"] == "false"


def test_publicar_TRUE_e_RECUSADO_com_o_motivo():
    """O ramo que de fato matou o render desta rodada."""
    with pytest.raises(ValueError) as e:
        DR.payload_do_render(_peca_do_disco(), publicar=True)
    m = str(e.value)
    assert "YT_TOKEN_JSON" in m and "YT_OAUTH_JSON" in m, m
    assert "force-ssl" in m, m
    assert "retomar" in m, m


def test_a_medida_dos_dispatches_esta_na_FRASE_e_nao_escrita_duas_vezes():
    """753: numero que o modulo calcula nao se repete em string nenhuma."""
    linha = DR._linha_da_rota()
    assert str(DR.DISPATCHES_MEDIDOS) in linha
    fonte = _corpo(DR, "_linha_da_rota")
    assert "DISPATCHES_MEDIDOS" in fonte, (
        "a frase tem de LER a constante, nao repetir o numero")
    arv = ast.parse(fonte)
    crus = [n.value for n in ast.walk(arv)
            if isinstance(n, ast.Constant) and isinstance(n.value, int)]
    assert DR.DISPATCHES_MEDIDOS not in crus, (
        "o numero reaparece cravado dentro da propria frase")


def test_a_frase_da_rota_tem_UM_dono_e_sai_nos_DOIS_ramos():
    marca = "ROTA MEDIDA"
    donos = [n for n in dir(DR)
             if callable(getattr(DR, n, None))
             and not n.startswith("__")
             and getattr(getattr(DR, n), "__module__", "") == DR.__name__
             and marca in _corpo(DR, n)]
    assert donos == ["_linha_da_rota"], donos
    # ramo ACEITO
    assert marca in DR.relato(_peca_do_disco(), RUN_DO_RENDER)
    # ramo RECUSADO (spec que nao existe no disco)
    r = DR.relato("canal-que-nao-existe-s999")
    assert "RECUSADO" in r and marca in r, r


# -------------------------------------------------------- forma do payload

def test_pacotes_e_lista_de_OBJETOS_e_nao_de_strings():
    """738: `["labtreinamento-s034"]` deu matriz vazia e ZERO anotacao util."""
    peca = _peca_do_disco()
    p = DR.payload_do_render(peca)
    lista = json.loads(p["pacotes"])
    assert isinstance(lista, list) and len(lista) == 1
    um = lista[0]
    assert isinstance(um, dict), um
    assert set(um) == {"canal", "pacote", "idioma"}, um
    assert um["pacote"] == peca


def test_canal_e_idioma_saem_da_SPEC_do_disco():
    peca = _peca_do_disco()
    with open(os.path.join(FABRICA, "specs", "%s.json" % peca),
              encoding="utf-8") as f:
        sp = json.load(f)
    um = json.loads(DR.payload_do_render(peca)["pacotes"])[0]
    import canal
    assert um["canal"] == canal.da_spec(sp)
    assert um["idioma"] == sp["idioma"]


def test_o_canal_e_DELEGADO_ao_dono_por_AST():
    """19/10 as 05:2x: derivar canal por conta propria parou a mira de
    conferir por SEIS pecas."""
    for nome in ("payload_do_render", "payload_do_retomar"):
        fonte = _corpo(DR, nome)
        assert "canal.da_spec" in _nomes_chamados(fonte), nome
        for proibido in ("rsplit", "split"):
            assert proibido + "(" not in fonte, (nome, proibido)


def test_spec_fora_do_disco_LEVANTA():
    with pytest.raises(ValueError) as e:
        DR.payload_do_render("nao-existe-s001")
    assert "checkout" in str(e.value), str(e.value)


def test_retomar_sem_run_id_LEVANTA():
    with pytest.raises(ValueError) as e:
        DR.payload_do_retomar(_peca_do_disco(), "")
    assert "artefato" in str(e.value).lower(), str(e.value)


def test_o_payload_do_retomar_NAO_leva_access_token():
    """Trava: nao mande token OAuth por input de workflow. Vazio faz o
    runner refrescar sozinho pelo `YT_OAUTH_JSON`."""
    p = DR.payload_do_retomar(_peca_do_disco(), RUN_DO_RENDER)
    assert "access_token" not in p, p
    assert set(p) == {"pacote", "canal", "idioma", "run_id", "estado_b64"}


# --------------------------------------------------------- o estado_b64

def test_o_estado_b64_e_DELEGADO_e_nao_remontado_aqui():
    """718/729: `estado_b64` montado a mao matou tres runs."""
    fonte = _corpo(DR, "payload_do_retomar")
    assert "estado_ponte.b64" in _nomes_chamados(fonte), fonte
    inteiro = open(os.path.join(FABRICA, "despacho_da_rodada.py"),
                   encoding="utf-8").read()
    arv = ast.parse(inteiro)
    importados = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Import):
            importados |= {a.name for a in n.names}
        if isinstance(n, ast.ImportFrom):
            importados.add(n.module or "")
    assert "base64" not in importados, (
        "importar base64 aqui cria o SEGUNDO dono da codificacao")


def test_o_b64_tem_UM_dono_no_estado_ponte_e_o_main_o_CHAMA():
    fonte_mod = open(os.path.join(FABRICA, "estado_ponte.py"),
                     encoding="utf-8").read()
    arv = ast.parse(fonte_mod)
    com_encode = []
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef):
            if "b64encode" in ast.unparse(n):
                com_encode.append(n.name)
    assert com_encode == ["b64"], com_encode
    assert "b64" in _nomes_chamados(_corpo(EP, "main")), (
        "o `main` tem de chamar o dono, senao sao dois caminhos")


def test_o_b64_RECUSA_estado_invalido(tmp_path):
    """Contraprova nos dois sentidos: corpus bom devolve payload decodavel,
    corpus com a contagem truncada LEVANTA — e e essa contagem que o runner
    recusa do outro lado."""
    bom = EP.b64()
    est = json.loads(base64.b64decode(bom))
    assert est["titulos_no_ar_n"] == len(est["titulos_no_ar"])

    ruim = tmp_path / "corpus.json"
    ruim.write_text("[]", encoding="utf-8")
    with pytest.raises(Exception):
        EP.b64(str(ruim))


# ------------------------------------------------- o modulo nao toca a rede

def test_ele_NAO_toca_a_rede():
    """Se custasse requisicao, ninguem o chamaria antes de cada despacho."""
    inteiro = open(os.path.join(FABRICA, "despacho_da_rodada.py"),
                   encoding="utf-8").read()
    arv = ast.parse(inteiro)
    importados = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Import):
            importados |= {a.name.split(".")[0] for a in n.names}
        if isinstance(n, ast.ImportFrom):
            importados.add((n.module or "").split(".")[0])
    for proibido in ("subprocess", "urllib", "requests", "http", "socket"):
        assert proibido not in importados, proibido


def test_o_codigo_de_saida_e_sempre_zero():
    r = subprocess.run([sys.executable,
                        os.path.join(FABRICA, "despacho_da_rodada.py"),
                        "nao-existe-s001"],
                       capture_output=True, text=True, cwd=RAIZ)
    assert r.returncode == 0, r.stderr
    assert "RECUSADO" in r.stdout, r.stdout


def test_ele_REPRODUZ_o_despacho_desta_rodada():
    """Sem isto a nota nao prova que o modulo serve para a decisao que de
    fato foi tomada."""
    caminho = os.path.join(FABRICA, "specs", "%s.json" % PECA)
    if not os.path.exists(caminho):
        pytest.skip("a peca de 23:0x saiu do disco; a propriedade esta nos "
                    "outros testes, que derivam a peca")
    p = DR.payload_do_render(PECA)
    assert json.loads(p["pacotes"]) == [
        {"canal": "labtreinamento", "pacote": PECA, "idioma": "pt-BR"}]
    assert p["publicar"] == "false"
    q = DR.payload_do_retomar(PECA, RUN_DO_RENDER)
    assert q["run_id"] == RUN_DO_RENDER and q["canal"] == "labtreinamento"


def test_a_medida_e_a_divergencia_dos_segredos_continuam_escritas():
    """Conserto sem o motivo escrito volta calado."""
    inteiro = open(os.path.join(FABRICA, "despacho_da_rodada.py"),
                   encoding="utf-8").read()
    for marca in ("YT_TOKEN_JSON", "YT_OAUTH_JSON", "force-ssl",
                  "38476203962", "DEFAULT"):
        assert marca in inteiro, marca
