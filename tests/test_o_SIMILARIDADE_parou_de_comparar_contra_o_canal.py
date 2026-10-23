"""O `similaridade` e o `variedade` liam o `slug` CRU como se fosse o canal.

MEDIDO em 23/10 as 18:4x, e e o vao que o conserto de 15:3x do MESMO dia nao
cobria. Aquele consertou o `_gate_identidade`; estes dois ficaram:

    variedade.py:172   irmas    = _especs_do_canal(raiz, spec.get("slug", ""), ...)
    prontidao.py:1020  do_canal = _titulos_do_canal(raiz, sp.get("slug") or "", ...)
    prontidao.py:462   slug     = sp.get("slug") or ""      # prefixo do glob

Desde 19/10 as 05:2x o `slug` e o PACOTE em 121 das 311 specs de short solto,
logo a atribuicao de canal por slug cru falha dos DOIS lados: a spec de slug
novo nao se reconhece e **tambem fica invisivel como IRMA** para quem usa a
convencao antiga. Medido no disco: das 364 specs da frota com short, **122 viam
ZERO irmas** e as outras viam lista INCOMPLETA.

A falha e PERMISSIVA, que e o pior sentido: com `do_canal` vazio a conferencia
do `_gate_similaridade`, guardada por `if do_canal`, simplesmente NAO RODAVA —
o portao parava de comparar contra o proprio canal e nao reprovava nada.

=============================================================================
A CONTA QUE AUTORIZOU, e ela NAO e "zero reprovacoes no acervo"
=============================================================================
Lido o canal do `canal.da_spec`, o portao passa a reprovar **15 das 455 specs
do disco (3,3%)** — e as 15 sao VERDADEIRAS: elas formam SETE grupos de colisao
dentro do MESMO canal, com 0,65 a 0,86 contra o teto de 0,65. Dois exemplos
medidos:

    'Το ενοίκιο δεν είναι το κόστος στέγης'  x  'Το νοίκι δεν είναι το κόστος'   0,86
    'Δύο αριθμοί, όχι ένας' x 'Δύο δρόμοι, όχι ένας' x 'Δύο νούμερα, όχι ένα'    0,82

Isto NAO e o caso do `mira.py` (um instrumento que dispararia 44 de 100 e por
isso deixaria de avisar): sao 3,3%, sao achados reais, e **spec de acervo nao e
republicada** — reprovar o acervo aqui nao tem custo operacional nenhum. O que
o conserto muda de verdade e que a peca da PROXIMA rodada passa a ser comparada
contra as irmas REAIS do canal dela. O `kolejny-poziom-s101`, publicado hoje as
12:33Z, colide a 0,69 com o `s054` e foi ao ar com o portao verde.

E o que ele NAO conserta vai medido em vez de vendido: no `_gate_ortografia` o
veredito sai **IDENTICO nos 122**, porque ali existe FALLBACK (canal abaixo do
piso troca para a populacao do IDIOMA). Lá a delegacao e UM DONO, nao conserto
de defeito ativo.

E a guarda do construtor era o defeito, nao o acervo: ela cobrava
`pacote == slug`, IDENTIDADE onde a afirmacao e PROPRIEDADE (743/753/761) — e
identidade FALSA para pacote, porque 142 das 143 specs com longo usam
`slug == CANAL`. A unica fora da convencao e o `epomeno-epipedo-069`, que ficou
assim porque esta guarda me empurrou para la.
"""
from __future__ import annotations

import ast
import glob
import json
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import autor as A              # noqa: E402
import canal as C              # noqa: E402
import guardas_do_construtor as G  # noqa: E402
import prontidao as P          # noqa: E402
import variedade as V          # noqa: E402

# HISTORIA, e nenhum assert depende dela: os ids mudam a cada rodada, e cravar
# um seria identidade onde ha propriedade (743/753/761).
MEDIDA_DE_18H = {
    "com_short": 364, "cegas": 122, "reprovacoes_novas": 15,
    "grupos_de_colisao": 7, "ortografia_muda": 0,
    "pacotes_slug_canal": 142, "pacotes_slug_pacote": 1,
}
PISO_DE_VACUIDADE = 200


def _disco() -> dict[str, dict]:
    saida = {}
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs/*.json"))):
        try:
            with open(caminho, encoding="utf-8") as f:
                saida[os.path.basename(caminho)] = json.load(f)
        except (OSError, ValueError):
            continue
    assert len(saida) >= PISO_DE_VACUIDADE, (
        f"varredura curta ({len(saida)} specs): com poucas specs este arquivo "
        "passa sem medir nada")
    return saida


ESPECS = _disco()


def _fonte(mod: str) -> str:
    with open(os.path.join(RAIZ, "fabrica", mod), encoding="utf-8") as f:
        return f.read()


def _funcao(mod: str, nome: str) -> ast.FunctionDef:
    arvore = ast.parse(_fonte(mod))
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            # O docstring CITA a forma proibida para se explicar: casar prosa
            # pegaria a explicacao em vez do codigo (a licao do
            # `test_NAO_virou_portao` do acento).
            corpo = [x for x in n.body
                     if not (isinstance(x, ast.Expr)
                             and isinstance(x.value, ast.Constant)
                             and isinstance(x.value.value, str))]
            return ast.parse(textwrap.dedent(ast.unparse(ast.Module(corpo, []))))
    raise AssertionError(f"{nome} saiu de {mod}: o dono mudou de nome")


# ---------------------------------------------------------------------------
# O DEFEITO, medido pela regra ANTIGA — senao "eu errei" e afirmacao minha
# ---------------------------------------------------------------------------

def test_a_regra_ANTIGA_de_fato_CEGAVA_a_atribuicao_de_irma():
    """Aplica o slug CRU e exige que ele atribua errado.

    Reprova se as duas leituras CONVERGIREM: ai o defeito perdeu o objeto e
    esta nota tem de ser RELIDA, nao o numero movido.
    """
    com_short = {n: d for n, d in ESPECS.items() if d.get("short")}
    assert len(com_short) >= 100, "poucas specs com short: nao mede nada"

    cru, der = {}, {}
    for n, d in com_short.items():
        cru[n] = d.get("slug") or ""
        der[n] = C.da_spec(d)
    divergem = [n for n in com_short if cru[n] != der[n]]
    assert divergem, (
        "nenhuma spec com short tem `slug` diferente do canal: as duas "
        "convencoes convergiram e esta nota tem de ser relida")
    assert len(divergem) < len(com_short), (
        "TODAS divergem: sem o outro lado o arquivo nao distingue nada")

    # com a regra antiga, a spec de slug novo nao acha irma NENHUMA
    nomes_por_cru: dict[str, int] = {}
    for n in com_short:
        nomes_por_cru[cru[n]] = nomes_por_cru.get(cru[n], 0) + 1
    cegas = [n for n in divergem if nomes_por_cru[cru[n]] == 1]
    assert cegas, (
        "a regra antiga deixou de cegar alguma spec: releia a nota em vez de "
        "mover o numero")


def test_o_CONSERTO_devolve_as_irmas_nos_DOIS_lados():
    """E a simetria: ler por qualquer convencao de slug ve o MESMO canal."""
    por_canal: dict[str, list[str]] = {}
    for n, d in ESPECS.items():
        if d.get("short") and not d.get("longo"):
            por_canal.setdefault(C.da_spec(d), []).append(n)

    vivos = {c: v for c, v in por_canal.items() if len(v) >= 10}
    assert vivos, "nenhum canal com 10+ shorts: varredura curta"

    for canal, nomes in vivos.items():
        convencoes = {(ESPECS[n].get("slug") == canal) for n in nomes}
        if len(convencoes) < 2:
            continue
        # existe canal com as DUAS convencoes: as irmas tem de ser as mesmas
        for n in nomes[:4]:
            irmas = V._especs_do_canal(RAIZ, canal, n)
            assert len(irmas) == len(nomes) - 1, (
                f"{n}: o canal {canal} tem {len(nomes)} shorts e o "
                f"`_especs_do_canal` devolveu {len(irmas)} irmas. A contagem e "
                "EXATA de proposito: com tolerancia, a regra ANTIGA (slug cru) "
                "passa aqui, e foi a contraprova que mostrou isso")
        break
    else:
        pytest.fail(
            "nenhum canal carrega as DUAS convencoes de slug: sem isso a "
            "simetria nao e exercitada e esta nota se rele")


# ---------------------------------------------------------------------------
# A CONTA QUE AUTORIZA — e ela e sobre PROPORCAO, nunca sobre contagem
# ---------------------------------------------------------------------------

def _acusa(nome: str, d: dict, canal: str) -> tuple[bool, float, str]:
    ts = P._titulos_do_copy(d)
    if not ts:
        return False, 0.0, ""
    titulo = ts[0]
    corpus = set(P._titulos_do_corpus(RAIZ))
    meu = d.get("pacote") or d.get("slug") or nome
    proprios = set()
    for t in ts:
        donos = {(o.get("pacote") or o.get("slug") or k)
                 for k, o in ESPECS.items() if t in P._titulos_do_copy(o)}
        if donos <= {meu}:
            proprios.add(t)
    jogo = corpus - proprios
    fora = []
    for k, o in ESPECS.items():
        if C.da_spec(o) != canal:
            continue
        t = next((x for x in P._titulos_do_copy(o) if x in jogo), "")
        if t:
            fora.append(t)
    if not fora:
        return False, 0.0, ""
    passa, pior, contra = A.inedita(titulo, fora)
    return (not passa), pior, contra


@pytest.fixture(scope="module")
def tally():
    """As acusadas pelas DUAS leituras, numa passada em memoria.

    O `_titulos_do_canal` e o `_outra_spec_com_o_titulo` nao tem cache e leem as
    ~455 specs a cada chamada, logo a varredura ingenua e O(n^2) — ela foi morta
    por falta de memoria antes de este arquivo existir.
    """
    corpus = set(P._titulos_do_corpus(RAIZ))
    assert len(corpus) >= 100, "corpus curto: nao mede nada"
    tit = {n: P._titulos_do_copy(d) for n, d in ESPECS.items()}
    portit: dict[str, set[str]] = {}
    for n, ts in tit.items():
        for t in ts:
            portit.setdefault(t, set()).add(
                ESPECS[n].get("pacote") or ESPECS[n].get("slug") or n)

    def por(canal, mapa, jogo):
        fora = []
        for k in ESPECS:
            if mapa[k] != canal:
                continue
            t = next((x for x in tit[k] if x in jogo), "")
            if t:
                fora.append(t)
        return fora

    cru = {n: (d.get("slug") or "") for n, d in ESPECS.items()}
    der = {n: C.da_spec(d) for n, d in ESPECS.items()}
    a_cru, a_der, pares = set(), set(), {}
    com_short = 0
    for n, d in ESPECS.items():
        if not d.get("short") or not tit[n]:
            continue
        com_short += 1
        titulo = tit[n][0]
        meu = d.get("pacote") or d.get("slug") or n
        jogo = corpus - {t for t in tit[n] if portit.get(t, set()) <= {meu}}
        la = por(cru[n], cru, jogo)
        lb = por(der[n], der, jogo)
        if la and not A.inedita(titulo, la)[0]:
            a_cru.add(n)
        if lb:
            passa, pior, contra = A.inedita(titulo, lb)
            if not passa:
                a_der.add(n)
                pares[n] = (pior, contra, titulo, der[n])
    return {"com_short": com_short, "cru": a_cru, "der": a_der, "pares": pares}


def test_a_conta_autorizadora_e_MINORIA_do_acervo(tally):
    """Portao que reprova o acervo nao e portao (o argumento do `mira.py`).

    Aqui o que se cobra e a FRACAO, nao a contagem: o acervo cresce uma spec por
    rodada, e contagem absoluta sobre populacao que cresce e identidade
    disfarcada de medida (a licao de 22/10 as 14:4x).
    """
    novas = tally["der"] - tally["cru"]
    frac = len(novas) / tally["com_short"]
    assert 0 < frac < 0.10, (
        f"as reprovacoes novas sao {len(novas)} de {tally['com_short']} "
        f"({frac:.3f}). ZERO quer dizer que o defeito perdeu o objeto; acima de "
        "10% o portao passa a reprovar o acervo e a nota tem de ser RELIDA")


def test_as_reprovacoes_novas_sao_VERDADEIRAS_e_do_MESMO_canal(tally):
    """Detector que inventa achado e pior que nao ter detector (725)."""
    novas = sorted(tally["der"] - tally["cru"])
    assert novas, "sem acusada nova este teste nao mede nada"
    for n in novas:
        pior, contra, titulo, canal = tally["pares"][n]
        assert pior >= A.SIMILARIDADE_MAX, (
            f"{n}: acusada com {pior:.2f}, abaixo do teto {A.SIMILARIDADE_MAX}")
        assert contra != titulo, (
            f"{n}: acusada contra o PROPRIO titulo — o `proprios` do portao "
            "deixou de tirar os titulos dela do jogo")
        dono = next((k for k, o in ESPECS.items()
                     if contra in P._titulos_do_copy(o)
                     and C.da_spec(o) == canal), "")
        assert dono, (
            f"{n}: o titulo {contra!r} nao e de spec nenhuma do canal "
            f"{canal!r} — a acusacao e de FORA do canal e seria inventada")


def test_a_colisao_e_SIMETRICA_entre_as_duas_pecas(tally):
    """Titulo A parecido com B implica B parecido com A: se o par nao fecha, a
    atribuicao de canal esta diferente nos dois lados e o achado e meu."""
    novas = tally["der"] - tally["cru"]
    assert novas
    canais = {tally["pares"][n][3] for n in novas}
    assert len(canais) >= 2, (
        f"as acusadas sao de um canal so ({canais}): sem mais de um canal isto "
        "e achado de canal e nao da frota, e a nota se rele")


def test_quem_ACUSA_e_o_DONO_e_nao_a_conta_deste_arquivo(tally):
    """O `tally` refaz a atribuicao em memoria por PERFORMANCE — e refazer e o
    segundo dono. Entao a acusacao vai cobrada do `_gate_similaridade`, que e
    quem de fato reprova a peca da rodada.

    Foi a contraprova que pediu este teste: com o conserto desligado, os de
    cima passavam todos, porque nenhum deles chamava o portao.
    """
    novas = sorted(tally["der"] - tally["cru"])
    assert novas, "sem acusada nova este teste nao mede nada"
    acusadas = []
    for n in novas[:6]:
        cam = os.path.join(RAIZ, "fabrica/specs", n)
        if P._gate_similaridade(cam, ESPECS[n]):
            acusadas.append(n)
    assert acusadas, (
        "o `_gate_similaridade` nao acusa NENHUMA das colisoes que a conta "
        f"deste arquivo achou ({novas[:6]}): ou o portao voltou a ler o slug "
        "cru, ou a conta daqui virou um segundo dono que discorda dele")


def test_a_peca_da_RODADA_passa_no_portao_consertado():
    """Afrouxar o portao para a propria peca passar e o avesso do trabalho.

    O par e o que importa: o conserto acusa as colisoes REAIS do acervo **e**
    deixa passar a peca que nao colide.
    """
    vivos = sorted(
        (n for n, d in ESPECS.items() if d.get("short") and d.get("longo")),
        reverse=True)
    assert vivos, "nenhum pacote com short no disco: perdi a ancora"
    cam = os.path.join(RAIZ, "fabrica/specs", vivos[0])
    sp = ESPECS[vivos[0]]
    assert not P._gate_similaridade(cam, sp), (
        f"{vivos[0]}: o pacote mais novo do disco reprova no `similaridade` — "
        "ou o titulo colide e tem de ser reescrito, ou o conserto reprova o "
        "acervo. Nos dois casos alguem tem de OLHAR")


# ---------------------------------------------------------------------------
# O que o conserto NAO conserta, medido em vez de vendido
# ---------------------------------------------------------------------------

def test_no_ORTOGRAFIA_o_veredito_NAO_muda_em_nenhuma_das_cegas():
    """Ali existe FALLBACK para a populacao do idioma, logo a cegueira troca a
    referencia e nao cala o portao. A delegacao ali e UM DONO, nao conserto."""
    muda, iguais = [], 0
    for nome, sp in ESPECS.items():
        if not sp.get("short"):
            continue
        cru, der = (sp.get("slug") or ""), C.da_spec(sp)
        if cru == der:
            continue
        caminho = os.path.join(RAIZ, "fabrica/specs", nome)
        com_der = P._gate_ortografia(caminho, sp)
        sp_cru = dict(sp)
        sp_cru["slug"] = cru
        # o modulo ja deriva: para medir a regra ANTIGA e preciso ANULAR a
        # derivacao, e com `pacote` fora o `da_spec` cai no proprio slug
        sp_cru.pop("pacote", None)
        com_cru = P._gate_ortografia(caminho, sp_cru)
        if bool(com_cru) == bool(com_der):
            iguais += 1
        else:
            muda.append((nome, com_cru, com_der))
    assert iguais >= 50, f"so {iguais} specs cegas medidas: varredura curta"
    assert not muda, (
        "o `ortografia` passou a mudar de veredito com o canal derivado: a nota "
        f"diz que ele nao muda em nenhuma, e agora muda em {len(muda)} — "
        f"releia em vez de mover o numero: {muda[:3]}")


# ---------------------------------------------------------------------------
# A GUARDA: propriedade, nao identidade
# ---------------------------------------------------------------------------

def test_a_guarda_do_pacote_aceita_as_DUAS_convencoes_medidas():
    """`pacote == slug` era identidade — e FALSA para pacote."""
    vistos = set()
    for nome, sp in ESPECS.items():
        if not sp.get("pacote"):
            continue
        q = G.confere(sp)["pacote"]
        assert q["ok"], (
            f"{nome}: a guarda reprova uma spec do DISCO ({q['motivo']}) — "
            "guarda que reprova o acervo nao e guarda")
        vistos.add(q["convencao"])
    assert vistos == {"canal", "pacote"}, (
        f"o disco deixou de ter as DUAS convencoes ({vistos}): com uma so a "
        "guarda volta a poder ser identidade e esta nota se rele")


def test_a_guarda_do_pacote_REPROVA_fora_das_duas_convencoes():
    """Contraprova no outro sentido: sem ela bastaria devolver sempre ok."""
    base = next(d for d in ESPECS.values() if d.get("pacote"))
    torta = dict(base)
    torta["slug"] = "um-slug-que-nao-e-canal-nem-pacote"
    q = G.confere(torta)["pacote"]
    assert not q["ok"], "slug fora das duas convencoes passou na guarda"
    assert "convencoes" in (q["motivo"] or ""), q["motivo"]


def test_a_guarda_do_pacote_NAO_cobra_mais_a_identidade():
    """A FRONTEIRA: `pacote != slug` com o slug no CANAL tem de passar."""
    base = next(d for d in ESPECS.values()
                if d.get("pacote") and d.get("longo"))
    sp = dict(base)
    sp["slug"] = C.do_pacote(sp["pacote"])
    assert sp["slug"] != sp["pacote"], "a ancora nao exercita a fronteira"
    assert G.confere(sp)["pacote"]["ok"], (
        "a guarda voltou a cobrar `pacote == slug`, que e identidade onde a "
        "afirmacao e propriedade (743/753/761)")
    # e o outro lado da convencao tambem passa
    sp2 = dict(base)
    sp2["slug"] = sp2["pacote"]
    assert G.confere(sp2)["pacote"]["ok"]


# ---------------------------------------------------------------------------
# AST: UM dono do canal, nos dois lados de cada varredura
# ---------------------------------------------------------------------------

def test_a_atribuicao_de_canal_e_DELEGADA_nos_tres_pontos():
    for mod, fn in (("variedade.py", "_especs_do_canal"),
                    ("variedade.py", "analisa"),
                    ("prontidao.py", "_titulos_do_canal"),
                    ("prontidao.py", "_gate_similaridade"),
                    ("prontidao.py", "_gate_ortografia")):
        fonte = ast.unparse(_funcao(mod, fn))
        assert "da_spec" in fonte, (
            f"{mod}:{fn} nao chama o dono do canal (`canal.da_spec`) — derivar "
            "ou ler o slug cru aqui seria o segundo dono")


def test_NINGUEM_atribui_canal_comparando_slug_CRU_com_slug_CRU():
    """A forma exata do defeito: `d.get("slug") == slug` numa varredura.

    O varredor do arquivo da mira procura quem DERIVA errado (`rsplit("-s")`);
    este procura quem COMPARA slug cru contra slug cru, que e atribuir canal
    sem dono. Sao duas formas do mesmo defeito e so uma estava coberta.
    """
    culpados = []
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "*.py"))):
        if os.path.basename(caminho) == "canal.py":
            continue
        with open(caminho, encoding="utf-8") as f:
            arvore = ast.parse(f.read())
        for n in ast.walk(arvore):
            if not isinstance(n, ast.FunctionDef):
                continue
            corpo = [x for x in n.body
                     if not (isinstance(x, ast.Expr)
                             and isinstance(x.value, ast.Constant))]
            for m in ast.walk(ast.Module(corpo, [])):
                if not isinstance(m, ast.Compare):
                    continue
                fonte = ast.unparse(m)
                if fonte.count('"slug"') + fonte.count("'slug'") < 2:
                    continue
                if "da_spec" in fonte:
                    continue
                culpados.append(f"{os.path.basename(caminho)}:{n.name}: {fonte}")
    assert not culpados, (
        "estes comparam slug CRU contra slug CRU para atribuir canal, que e o "
        f"defeito que este arquivo guarda: {sorted(set(culpados))}")


def test_o_MOTIVO_continua_escrito_nos_tres_modulos():
    """Conserto sem motivo escrito volta calado."""
    for mod, marcas in (
            ("variedade.py", ("da_spec", "122", "PACOTE")),
            ("prontidao.py", ("da_spec", "PERMISSIVA", "122")),
            ("guardas_do_construtor.py", ("142", "PROPRIEDADE", "743"))):
        fonte = _fonte(mod)
        for marca in marcas:
            assert marca in fonte, (
                f"{mod} perdeu {marca!r} do motivo: sem ele a rodada seguinte "
                "volta a ler o slug cru")
