# -*- coding: utf-8 -*-
"""O guarda do despacho media o DISCO e a frase dele falava do CHECKOUT.

MEDIDO em 23/10 as 10:2x, e o erro aconteceu nesta rodada. O `_spec` do
`despacho_da_rodada` conferia `os.path.exists` — o disco DESTA sessao — e o
docstring dele ja dizia, em letra, que *"spec que nao foi comitada nao existe
para ele [o runner]"*. Eu escrevi a spec, rodei os doze portoes, chamei o
modulo (que PASSOU) e despachei sem comitar: o passo `Baixar spec e trilhas`
do `frota.yml` roda com `set -euo pipefail`, caiu no ramo ELSE, buscou a spec
no Storage (402 continuo desde 25/08), o `curl --fail` saiu em 22 e o render
morreu antes de comecar.

E A ANOTACAO NAO DISTINGUE A CAUSA: `No files were found` e a mesma de tres
defeitos diferentes, e quem para nela ve o 402 e culpa o Storage — que **nao
era a causa**, porque o 402 e continuo e toda rodada normal passa por cima
dele. A causa e o ramo ELSE ter sido tomado.

O que estes testes cobram e PROPRIEDADE: os tres estados DIVERGEM, a recusa
vai nos dois medidos e NAO no indeterminado, a frase tem UM dono e sai nos
TRES ramos, e nada aqui toca a rede. O repo de prova e CONSTRUIDO (git de
verdade, com um `origin` bare), porque ancorar no repo vivo seria identidade
onde ha propriedade (743/753/761) — e porque so um repo proprio produz o
estado `divergente`, que e o PERMISSIVO e o pior dos tres.
"""
import ast
import inspect
import json
import os
import subprocess
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
if FABRICA not in sys.path:
    sys.path.insert(0, FABRICA)

import despacho_da_rodada as DR  # noqa: E402

# A peca e o run desta rodada sao HISTORIA: nenhum assert depende deles.
PECA_DE_10H = "epomeno-epipedo-s101"
RUN_QUE_MORREU = "39938649668"
# O ramo de prova e o do MODULO de proposito: o `_spec` nao recebe `ref`, logo
# so com o ramo real o caminho que de fato roda em producao e exercitado. Com
# outro nome o ref de rastreio nao existe no repo de prova e TUDO sai
# `sem_git` — isto e, o arquivo passaria por vacuidade.
RAMO = DR.BRANCH


def _corpo(mod, nome):
    """A fonte de UMA funcao, desindentada — `textwrap.dedent` e nao
    `inspect.cleandoc`, que desindenta a linha do `def` e deixa o corpo
    torto (a licao de 22/10 as 08:3x)."""
    return textwrap.dedent(inspect.getsource(getattr(mod, nome)))


def _git(args, cwd):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    assert p.returncode == 0, (args, p.stderr)
    return p.stdout.strip()


def _spec_minima(pacote):
    return {"slug": pacote, "pacote": pacote, "idioma": "el",
            "voz": "el-GR-NestorasNeural", "trilha": "Inspired",
            "longo": [], "short": [{"layout": "titulo", "kicker": "k",
                                    "sub": "s", "nar": "n"}]}


@pytest.fixture
def repo(tmp_path):
    """Um repo de VERDADE com um `origin` bare, para os tres estados.

    Sem o bare nao existe ref de rastreio, logo `origin/<ramo>` nao resolve
    e tudo sairia `sem_git` — isto e, o arquivo passaria por vacuidade sem
    medir nenhum dos estados que importam.
    """
    bare = tmp_path / "origin.git"
    _git(["init", "--bare", "-q", str(bare)], str(tmp_path))
    trab = tmp_path / "trab"
    trab.mkdir()
    _git(["init", "-q", "-b", RAMO], str(trab))
    _git(["remote", "add", "origin", str(bare)], str(trab))
    _git(["config", "user.email", "t@t"], str(trab))
    _git(["config", "user.name", "t"], str(trab))
    specs = trab / "fabrica" / "specs"
    specs.mkdir(parents=True)
    (trab / "semente.txt").write_text("x", encoding="utf-8")
    _git(["add", "-A"], str(trab))
    _git(["commit", "-q", "-m", "semente"], str(trab))
    _git(["push", "-q", "-u", "origin", RAMO], str(trab))
    return {"trab": str(trab), "specs": str(specs)}


def _escreve(repo, pacote, extra=None):
    sp = _spec_minima(pacote)
    if extra:
        sp.update(extra)
    caminho = os.path.join(repo["specs"], "%s.json" % pacote)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(sp, f, ensure_ascii=False)
    return caminho


def _comita(repo, empurra=True):
    _git(["add", "-A"], repo["trab"])
    _git(["commit", "-q", "-m", "spec"], repo["trab"])
    if empurra:
        _git(["push", "-q", "origin", RAMO], repo["trab"])


def _le(repo, pacote):
    return DR.no_checkout(pacote, dir_specs=repo["specs"], ref=RAMO,
                          raiz=repo["trab"])


# ---------------------------------------------------------------- o defeito

def test_REPRODUZ_o_defeito_desta_rodada(repo):
    """Spec no disco e NAO no checkout: estado `ausente`."""
    _escreve(repo, "p-nova")
    c = _le(repo, "p-nova")
    assert c["no_disco"] is True
    assert c["estado"] == "ausente", c
    assert "ausente" in c["estado"] and c["motivo"]


def test_o_guarda_ANTIGO_de_fato_PASSAVA_nesse_caso(repo):
    """Sem ele, *"eu errei"* seria afirmacao minha e nao medida.

    O guarda antigo era `os.path.exists`, e e justamente o que o campo
    `no_disco` devolve: ele passa no caso que matou o render.
    """
    _escreve(repo, "p-nova")
    c = _le(repo, "p-nova")
    assert c["no_disco"] is True          # o guarda antigo aprovava
    assert c["estado"] != "igual"         # e o checkout nao traz nada


def test_comitada_e_empurrada_sai_IGUAL(repo):
    """Contraprova no outro sentido: senao bastaria recusar sempre."""
    _escreve(repo, "p-ok")
    _comita(repo)
    c = _le(repo, "p-ok")
    assert c["estado"] == "igual", c
    assert c["blob_no_ref"] == c["blob_no_disco"]


def test_comitada_e_NAO_empurrada_sai_ausente(repo):
    """O runner clona o REMOTO: commit local nao basta."""
    _escreve(repo, "p-local")
    _comita(repo, empurra=False)
    c = _le(repo, "p-local")
    assert c["estado"] == "ausente", c


def test_editada_DEPOIS_do_commit_sai_divergente(repo):
    """O caso PERMISSIVO: o render passa, com a versao ANTIGA e em silencio."""
    _escreve(repo, "p-dif")
    _comita(repo)
    _escreve(repo, "p-dif", {"trilha": "Wholesome"})
    c = _le(repo, "p-dif")
    assert c["estado"] == "divergente", c
    assert c["blob_no_ref"] and c["blob_no_disco"]
    assert c["blob_no_ref"] != c["blob_no_disco"]


def test_no_ref_e_FORA_do_disco_tambem_e_divergente(repo):
    """O outro lado da divergencia, e ele nao pode sair `igual`."""
    _escreve(repo, "p-sumiu")
    _comita(repo)
    os.remove(os.path.join(repo["specs"], "p-sumiu.json"))
    c = _le(repo, "p-sumiu")
    assert c["no_disco"] is False
    assert c["estado"] == "divergente", c


def test_sem_git_NAO_afirma_ausencia(tmp_path):
    """Vazio de instrumento nao prova ausencia (17/10)."""
    fora = tmp_path / "fora"
    (fora / "specs").mkdir(parents=True)
    c = DR.no_checkout("p", dir_specs=str(fora / "specs"), ref=RAMO,
                       raiz=str(fora))
    assert c["estado"] == "sem_git", c
    assert c["estado"] not in ("ausente", "divergente")
    assert c["motivo"]


def test_os_TRES_estados_DIVERGEM(repo):
    """Funcao que devolve sempre o mesmo valor nao mede nada."""
    _escreve(repo, "a")
    vistos = {_le(repo, "a")["estado"]}
    _comita(repo)
    vistos.add(_le(repo, "a")["estado"])
    _escreve(repo, "a", {"trilha": "Wholesome"})
    vistos.add(_le(repo, "a")["estado"])
    assert vistos == {"ausente", "igual", "divergente"}, vistos
    assert vistos <= set(DR.NO_CHECKOUT)


def test_todo_estado_devolvido_esta_declarado_em_NO_CHECKOUT():
    """Por AST, nos DOIS sentidos: estado novo sem nome na constante e
    estado na constante que a funcao nao produz sao os dois defeito."""
    arv = ast.parse(_corpo(DR, "no_checkout"))
    lits = set()

    def _colhe(no):
        for d in ast.walk(no):
            if isinstance(d, ast.Constant) and isinstance(d.value, str):
                lits.add(d.value)

    for n in ast.walk(arv):
        # `fora["estado"] = ...`, inclusive quando o valor e um ternario
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Subscript)
                and isinstance(n.targets[0].slice, ast.Constant)
                and n.targets[0].slice.value == "estado"):
            _colhe(n.value)
        # e o literal do dicionario inicial, que e onde mora o estado PADRAO
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if (isinstance(k, ast.Constant) and k.value == "estado"):
                    _colhe(v)
    assert lits, "a varredura nao achou estado nenhum: ela quebrou"
    assert lits <= set(DR.NO_CHECKOUT), lits - set(DR.NO_CHECKOUT)
    assert set(DR.NO_CHECKOUT) == lits, set(DR.NO_CHECKOUT) - lits


# ------------------------------------------------------------- a recusa

def test_o_payload_RECUSA_nos_dois_estados_medidos(repo, monkeypatch):
    for pacote, prep in (("p1", lambda: None),
                         ("p2", lambda: (_comita(repo),
                                         _escreve(repo, "p2",
                                                  {"trilha": "Wholesome"})))):
        _escreve(repo, pacote)
        prep()
        monkeypatch.chdir(repo["trab"])
        with pytest.raises(ValueError) as e:
            DR.payload_do_render(pacote, dir_specs=repo["specs"])
        assert "CHECKOUT" in str(e.value) or "checkout" in str(e.value)


def test_o_payload_NAO_recusa_quando_o_checkout_traz_igual(repo, monkeypatch):
    """Contraprova: sem ela, recusar sempre passaria nos dois testes."""
    _escreve(repo, "p-ok")
    _comita(repo)
    monkeypatch.chdir(repo["trab"])
    p = DR.payload_do_render("p-ok", dir_specs=repo["specs"])
    assert p["publicar"] == "false"
    assert "p-ok" in p["pacotes"]


def test_o_payload_NAO_recusa_quando_nao_sabe(tmp_path, monkeypatch):
    """`sem_git` nao e ausencia, logo nao pode virar recusa."""
    fora = tmp_path / "fora"
    specs = fora / "specs"
    specs.mkdir(parents=True)
    pacote = "p-sem-git"
    with open(specs / ("%s.json" % pacote), "w", encoding="utf-8") as f:
        json.dump(_spec_minima(pacote), f)
    monkeypatch.chdir(str(fora))
    p = DR.payload_do_render(pacote, dir_specs=str(specs))
    assert p["publicar"] == "false"


# ------------------------------------------------------------- a disciplina

def test_nada_aqui_toca_a_REDE_por_AST():
    """Se custasse requisicao, ninguem chamaria isto antes de cada despacho
    — a mesma razao do `caminho_de_saida` e do `terminou`."""
    fonte = inspect.getsource(DR)
    arv = ast.parse(fonte)
    proibidos = {"fetch", "pull", "ls-remote", "remote", "clone", "push"}
    achados = []
    for n in ast.walk(arv):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if n.value in proibidos:
                achados.append(n.value)
        if isinstance(n, ast.Import):
            for a in n.names:
                assert a.name not in ("urllib", "requests", "http"), a.name
    assert not achados, achados


def test_a_frase_do_checkout_tem_UM_dono_por_AST():
    marca = "CHECKOUT ("
    donos = [n.name for n in ast.walk(ast.parse(inspect.getsource(DR)))
             if isinstance(n, ast.FunctionDef)
             and marca in ast.unparse(n)]
    assert donos == ["_linha_do_checkout"], donos


def test_a_frase_sai_nos_TRES_ramos(repo, tmp_path):
    _escreve(repo, "a")
    estados = []
    estados.append(_le(repo, "a"))
    _comita(repo)
    estados.append(_le(repo, "a"))
    fora = tmp_path / "fora2"
    (fora / "specs").mkdir(parents=True)
    estados.append(DR.no_checkout("a", dir_specs=str(fora / "specs"),
                                  ref=RAMO, raiz=str(fora)))
    for c in estados:
        linha = DR._linha_do_checkout(c)
        assert "CHECKOUT (" in linha
        assert c["estado"] in linha, (c["estado"], linha)
    # e os tres textos DIVERGEM: frase igual para estado diferente nao avisa
    assert len({DR._linha_do_checkout(c) for c in estados}) == 3


def test_o_relato_CHAMA_a_frase_FORA_de_ramo_condicional():
    """Dentro de um `if` ela sairia so quando algo chamasse atencao, que foi
    o defeito da nota da rota em 20/10 as 13:2x."""
    arv = ast.parse(_corpo(DR, "relato"))
    fn = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)][0]
    topo = [ast.unparse(s) for s in fn.body]
    assert any("_linha_do_checkout" in s for s in topo), topo
    for s in fn.body:
        if isinstance(s, (ast.If, ast.Try)) and "_linha_do_checkout" in ast.unparse(s):
            pytest.fail("a frase do checkout esta dentro de ramo condicional")


def test_as_TRES_causas_da_mesma_anotacao_continuam_escritas():
    """Sem elas, a rodada seguinte le o 402 e culpa o Storage — que nao era
    a causa, porque ele e continuo desde 25/08."""
    fonte = inspect.getsource(DR)
    assert "No files were found" in fonte
    assert "402" in fonte
    assert "KeyError" in fonte
    assert "Baixar spec e trilhas" in fonte


def test_o_motivo_DIFERE_por_estado(repo):
    """Cada estado pede outro remedio, logo um motivo so nao serve."""
    _escreve(repo, "a")
    m1 = _le(repo, "a")["motivo"]
    _comita(repo)
    _escreve(repo, "a", {"trilha": "Wholesome"})
    m2 = _le(repo, "a")["motivo"]
    assert m1 and m2 and m1 != m2, (m1, m2)
