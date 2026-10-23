"""O PORTAO da identidade lia o `slug` CRU, e o slug virou o PACOTE.

MEDIDO em 23/10 as 15:3x, pela suite: a passada acusou UMA falha nova contra as
25 da linha de base, e ela era o `test_idioma_da_spec_bate_com_o_do_canal` no
`epomeno-epipedo-069` — o primeiro pacote cujo `slug` nao e mais o canal. O
teste estava errado e foi retratado no lugar; **consertando-o apareceu o defeito
de verdade, e ele e no `prontidao._gate_identidade`**:

    do_canal        = idioma_do_canal(sp["slug"])
    do_canal_trilha = trilha_do_canal_config(sp["slug"])

Desde 19/10 as 05:2x o `slug` e o PACOTE, logo as duas leituras devolviam `""` —
e as duas conferencias de baixo estao guardadas por `do_canal and`. **O portao
parou de conferir e nao reprovou nada.** E a falha PERMISSIVA da mira daquele
dia, agora num PORTAO: o da mira INFORMA, este AUTORIZA.

  * **120 das 451** specs de video do disco cegavam as DUAS conferencias;
  * reproduzido no `epomeno-epipedo-069`: a spec com a trilha do KOLEJNY e a
    spec declarando `pl` num canal grego passavam as duas **LIMPAS**;
  * e a trilha e justamente o portao que existe porque o `kolejny-poziom-005`
    foi ao ar com `Deliberate_Thought` num canal `Wholesome` — "o equivalente
    sonoro de trocar de logo", diz o comentario dele.

**E O VARREDOR POR AST DO ARQUIVO DA MIRA NAO PODIA PEGAR ISTO**, que e o vao
que este arquivo fecha: ele procura quem **DERIVA** o canal errado
(`rsplit("-s")`), e aqui ninguem deriva — le-se o slug cru, como se ele ja fosse
o canal. Sao duas formas do mesmo defeito e so uma estava coberta.

**A CONTA QUE AUTORIZOU O CONSERTO VAI ANTES DELE:** com o canal saindo do
`canal.da_spec`, o portao reprova **ZERO** specs do acervo e nao sobra canal sem
yaml. E a mesma aritmetica que pos o grego no `DIACRITICOS` e o cartao em branco
no portao `layout` — reprova a peca quebrada e nenhuma do parque.
"""

from __future__ import annotations

import ast
import copy
import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import canal as C  # noqa: E402
import prontidao as PR  # noqa: E402
from publicar import idioma_do_canal, trilha_do_canal_config  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "prontidao.py")

# A peca que PEGOU o defeito fica como HISTORIA, e nenhum assert depende dela:
# ela e um pacote como qualquer outro e o id envelhece (743/753/761).
PECA_DE_15H = "epomeno-epipedo-069"


def _specs():
    fora = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        if s.get("longo") or s.get("short"):
            fora.append((p, s))
    return fora


def _ancora(slug_e_canal_iguais: bool):
    """Uma spec do DISCO em cada convencao de slug, DERIVADA e nao nomeada."""
    for p, s in _specs():
        if (s.get("slug") == C.da_spec(s)) is not slug_e_canal_iguais:
            continue
        if not (s.get("idioma") and s.get("trilha")):
            continue
        if idioma_do_canal(C.da_spec(s)) and trilha_do_canal_config(C.da_spec(s)):
            return p, s
    pytest.fail(
        "perdi a ancora: nenhuma spec do disco com "
        f"slug {'==' if slug_e_canal_iguais else '!='} canal e com idioma e "
        "trilha conferiveis — sem ela este arquivo nao mede o defeito")


def _sem_prosa(fn) -> ast.FunctionDef:
    with open(FONTE, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == fn:
            return n
    pytest.fail(f"{fn} desapareceu do prontidao — o teste nao mede nada")


# ---------------------------------------------------------------- o defeito

def test_a_leitura_ANTIGA_de_fato_CEGAVA_o_portao():
    """Sem isto, *"o portao parou de conferir"* seria afirmacao minha.

    Aplica a regra ANTIGA (o slug cru) e exige que ela devolva vazio nas duas
    conferencias — e **reprova se ela deixar de errar**, porque ai o defeito
    desapareceu e esta nota se rele."""
    _, s = _ancora(slug_e_canal_iguais=False)
    assert idioma_do_canal(s["slug"]) == "", (
        "o slug cru voltou a resolver idioma: a convencao de nome mudou e esta "
        "nota tem de ser relida")
    assert trilha_do_canal_config(s["slug"]) == "", (
        "o slug cru voltou a resolver trilha — releia esta nota")
    assert idioma_do_canal(C.da_spec(s)), "o DONO deixou de resolver o canal"
    assert trilha_do_canal_config(C.da_spec(s)), "o DONO deixou de resolver"


def test_o_portao_ACUSA_trilha_de_outro_canal_nas_DUAS_convencoes():
    """A contraproba que importa: a trilha e o portao do `kolejny-poziom-005`."""
    for iguais in (True, False):
        cam, s = _ancora(slug_e_canal_iguais=iguais)
        certa = trilha_do_canal_config(C.da_spec(s))
        outra = "Wholesome" if certa != "Wholesome" else "Inspired"
        t = copy.deepcopy(s)
        t["trilha"] = outra
        faltas = PR._gate_identidade(cam, t)
        assert any("trilha" in f for f in faltas), (
            f"slug{'==' if iguais else '!='}canal: trilha {outra!r} num canal "
            f"{certa!r} passou LIMPA pelo portao — {faltas}")


def test_o_portao_ACUSA_idioma_de_outro_canal_nas_DUAS_convencoes():
    for iguais in (True, False):
        cam, s = _ancora(slug_e_canal_iguais=iguais)
        certo = idioma_do_canal(C.da_spec(s))
        outro = "pl" if certo != "pl" else "el"
        t = copy.deepcopy(s)
        t["idioma"] = outro
        faltas = PR._gate_identidade(cam, t)
        assert any("idioma" in f for f in faltas), (
            f"slug{'==' if iguais else '!='}canal: idioma {outro!r} num canal "
            f"{certo!r} passou LIMPO pelo portao — {faltas}")


def test_contraproba_a_spec_CERTA_continua_passando():
    """Sem ela bastaria o portao reprovar sempre."""
    for iguais in (True, False):
        cam, s = _ancora(slug_e_canal_iguais=iguais)
        assert PR._gate_identidade(cam, s) == [], (
            f"slug{'==' if iguais else '!='}canal: o portao passou a reprovar a "
            "spec CERTA")


# ----------------------------------------------------- os dois lados no disco

def test_os_DOIS_lados_da_convencao_de_slug_existem_no_disco():
    """Se todas convergirem, este arquivo passa por vacuidade e se rele."""
    todas = _specs()
    assert len(todas) >= 200, f"varredura curta ({len(todas)}): nao mede nada"
    pacote = [p for p, s in todas if s.get("slug") != C.da_spec(s)]
    canal = [p for p, s in todas if s.get("slug") == C.da_spec(s)]
    assert pacote, (
        "nenhuma spec tem slug != canal: a convencao NOVA desapareceu do disco "
        "e o defeito deixou de ter objeto")
    assert canal, (
        "nenhuma spec tem slug == canal: sem a convencao ANTIGA o teste das "
        "duas convencoes mede uma so")


def test_a_FRACAO_cegada_e_RECONFERIDA_contra_o_disco():
    """O numero vai como PROPORCAO e nao como contagem.

    Contagem absoluta sobre populacao que cresce uma spec por rodada e
    identidade disfarcada de medida — a licao de 22/10 as 14:4x, onde um
    `abs(com - 144) <= 15` saiu do limite por CRESCIMENTO do acervo e nao por
    mudanca de carater. O que se cobra e que a fracao cegada esteja na faixa
    OBSERVADA e que ela nao seja nem zero nem tudo."""
    todas = _specs()
    cegadas = [p for p, s in todas
               if s.get("slug") != C.da_spec(s)
               and not idioma_do_canal(s["slug"])
               and idioma_do_canal(C.da_spec(s))]
    frac = len(cegadas) / len(todas)
    assert 0.10 <= frac <= 0.80, (
        f"a fracao cegada pela leitura ANTIGA saiu da faixa observada: "
        f"{len(cegadas)}/{len(todas)} = {frac:.3f}. Em 23/10 as 15:3x eram "
        f"120/451 = 0.266. Releia esta nota em vez de mover o numero")


def test_o_conserto_NAO_reprova_o_acervo():
    """A conta que autorizou o portao, reconferida.

    Se ela cair, o portao passou a reprovar peca publicada — e ai o lugar disto
    deixa de ser o portao e passa a ser a suite, pelo argumento do `mira.py`."""
    todas = _specs()
    assert len(todas) >= 200, f"varredura curta ({len(todas)}): nao mede nada"
    reprovadas = []
    for cam, s in todas:
        faltas = [f for f in PR._gate_identidade(cam, s)
                  if "idioma" in f or "trilha" in f]
        if faltas:
            reprovadas.append((os.path.basename(cam), faltas))
    assert not reprovadas, (
        "o portao consertado reprova spec do acervo, o que nao e o que a "
        f"medicao de 23/10 autorizou: {reprovadas[:6]}")


# ------------------------------------------------------------- a delegacao

def test_o_portao_DELEGA_o_canal_por_AST():
    """`sp["slug"]` nao pode chegar as duas leituras do canal.

    Por AST porque o comentario do proprio portao CITA a forma antiga para se
    explicar, e casar prosa pegaria a explicacao em vez do codigo.

    E a PRIMEIRA versao deste assert estava errada, pela licao de sempre: ela
    proibia a *substring* `"slug"` no argumento, e o nome da variavel que
    carrega o canal derivado e `do_canal_slug` — logo ela reprovava o codigo
    CERTO. **Era o teste errado, nao o modulo.** A propriedade e de FORMA: o
    argumento nao pode ser um `sp["slug"]` (um Subscript com a chave `slug`), e
    o nome que chega ali tem de vir do dono."""
    fn = _sem_prosa("_gate_identidade")
    chama_dono = False
    do_dono = set()
    for n in ast.walk(fn):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "da_spec"):
            chama_dono = True
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) \
                and isinstance(n.value.func, ast.Attribute) \
                and n.value.func.attr == "da_spec":
            for alvo in n.targets:
                if isinstance(alvo, ast.Name):
                    do_dono.add(alvo.id)
    for n in ast.walk(fn):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in ("idioma_do_canal", "trilha_do_canal_config")):
            continue
        for a in n.args:
            crua = (isinstance(a, ast.Subscript)
                    and isinstance(a.slice, ast.Constant)
                    and a.slice.value == "slug")
            assert not crua, (
                f"{n.func.id} voltou a receber o slug CRU: {ast.unparse(a)}")
            if isinstance(a, ast.Name):
                assert a.id in do_dono, (
                    f"{n.func.id} recebe {a.id!r}, que nao vem do "
                    f"`canal.da_spec` (vem do dono: {sorted(do_dono)})")
            elif not crua:
                assert "da_spec" in ast.unparse(a), (
                    f"{n.func.id} recebe {ast.unparse(a)}, que nao passa pelo "
                    "dono do canal")
    assert chama_dono, (
        "o portao deixou de chamar `canal.da_spec`: o canal tem UM dono desde "
        "19/10 as 05:2x, e derivar aqui seria o SEXTO")


def test_NINGUEM_na_fabrica_passa_o_SLUG_cru_para_o_canal():
    """O vao que o varredor da mira nao cobria.

    Aquele procura quem DERIVA errado (`rsplit("-s")`); este procura quem LE o
    slug como se ele ja fosse o canal. Sao duas formas do mesmo defeito."""
    culpados = []
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "*.py"))):
        with open(caminho, encoding="utf-8") as f:
            arvore = ast.parse(f.read())
        for n in ast.walk(arvore):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)):
                continue
            if n.func.id not in ("idioma_do_canal", "trilha_do_canal_config"):
                continue
            for a in n.args:
                fonte = ast.unparse(a)
                if '"slug"' in fonte or "'slug'" in fonte:
                    if "da_spec" not in fonte:
                        culpados.append(f"{os.path.basename(caminho)}: {fonte}")
    assert not culpados, (
        "estes modulos leem o `slug` da spec como se fosse o canal, que e o "
        f"defeito que este arquivo guarda: {sorted(set(culpados))}")


def test_o_MOTIVO_continua_escrito_no_portao():
    """Conserto sem motivo escrito volta calado."""
    with open(FONTE, encoding="utf-8") as f:
        fonte = f.read()
    for marca in ("canal.da_spec", "PERMISSIVA", "120", "451", "kolejny-poziom-005"):
        assert marca in fonte, (
            f"o motivo do conserto perdeu {marca!r}: sem ele a rodada seguinte "
            "volta a ler o slug cru")
    assert PECA_DE_15H in fonte, (
        "a peca que pegou o defeito saiu do comentario — ela e a procedencia")
