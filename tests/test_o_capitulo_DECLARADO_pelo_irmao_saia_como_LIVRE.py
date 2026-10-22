"""O capitulo que o irmao DECLARA saia como LIVRE — e me custou duas cenas.

**MEDIDO em 22/10 as 12:3x, escrevendo o `kolejny-poziom-s093`.** O
`segundo_angulo.nao_mencionados` casa o TEXTO do kicker contra a copy do irmao,
e a copy declara FAIXA em digitos (*"Capitulos 66 a 74 do longo"*). Logo
capitulo DECLARADO continuava saindo na lista de livres, e e dessa lista que a
rodada escolhe familia.

**O custo nao e teorico.** As duas cenas finais da primeira versao daquela peca
repetiam o fechamento do `kolejny-poziom-s076`: ele declara 66 a 74 e a narracao
dele diz, em letra, *"Sprawdz ponownie po trzech miesiacach"* — a mesma frase da
minha cena 11. **Nenhum portao pegaria isso:** o `similaridade` compara TITULO,
nao cena. E a reserva que DESEMPATOU a pauta daquela rodada (71 de 84) esta
inflada pelo mesmo defeito.

Eram DOIS donos do mesmo fato e eles discordavam: a faixa e lida pelo
`irmaos_da_origem._capitulos_declarados`. O conserto DELEGA a ele e **NOMEIA em
vez de filtrar** (disciplina do `origens_sem_uso`): o `nao_mencionados` segue
devolvendo a MESMA lista, e o `declarados_pelos_irmaos` diz quais daqueles
indices um irmao declara.

**E O CONSERTO CAIU NO DEFEITO QUE CONSERTA, uma camada abaixo:** a primeira
versao chamou `IO.irmaos(yid, dir_specs)` e o `irmaos` recebe **raiz**, nao
`dir_specs`. O `glob` varreu `<dir_specs>/fabrica/specs`, que nao existe, e
devolveu **lista VAZIA e bem formada** — `n = 0`, indistinguivel de origem sem
irmao nenhum. E a familia de 20/10 as 12:3x, e por isso o `irmaos` ganhou a
guarda de vacuidade (DELEGADA ao dono dela) e nasceu o inverso
`raiz_do_dir_specs`.
"""
import ast
import glob
import inspect
import json
import os
import re
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402
import segundo_angulo as SA  # noqa: E402

PISO_ORIGENS = 20
SPECS = os.path.join(RAIZ, "fabrica", "specs")

# HISTORIA, e nenhum assert depende disto: o par que custou as duas cenas foi
# (`-5aMrDsxlZE`, capitulo 74, declarado pelo `kolejny-poziom-s076`). Cravar o
# id seria identidade onde ha propriedade (743/753/761) — pauta se consome e
# capitulo se usa, e a rodada seguinte veria o teste reprovar pelo trabalho
# feito (18/10 as 09:2x).
PAR_DE_12H = ("-5aMrDsxlZE", 74, "kolejny-poziom-s076")


def _fonte(fn) -> ast.AST:
    """`textwrap.dedent`, nao `inspect.cleandoc`: o cleandoc desindenta a linha
    do `def` e deixa o corpo torto (IndentationError) — 22/10 as 08:3x."""
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def _origens() -> list:
    saida = {}
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("longo_existente"):
            continue
        saida[d["longo_existente"]] = True
    return sorted(saida)


def _quadro() -> list:
    out = []
    for yid in _origens():
        try:
            r = SA.declarados_pelos_irmaos(yid)
        except Exception:
            continue
        if r["pacote"]:
            out.append(r)
    return out


def test_a_varredura_sai_do_DISCO_e_reprova_por_vacuidade():
    q = _quadro()
    assert len(q) >= PISO_ORIGENS, (
        "menos de %d origens com spec local (%d): com acervo curto este arquivo "
        "passa sem medir nada, que e o defeito do 743 em forma de glob"
        % (PISO_ORIGENS, len(q)))


def test_REPRODUZ_o_defeito_e_relê_se_ele_desaparecer():
    """Existe capitulo que um irmao DECLARA e que sai como LIVRE."""
    q = _quadro()
    com = [r for r in q if r["n"]]
    assert com, (
        "nenhuma origem tem capitulo livre que um irmao declara — entao o "
        "defeito medido em 22/10 as 12:3x nao ocorre mais, e esta nota tem de "
        "ser RELIDA em vez de ficar")
    for r in com:
        d = SA.nao_mencionados([y for y in _origens()
                                if SA.nao_mencionados(y)["pacote"]
                                == r["pacote"]][0])
        break
    assert sum(r["n"] for r in com) >= 1


def test_ele_NOMEIA_e_NAO_filtra():
    """O capitulo declarado CONTINUA em `nao_mencionados`, e vem marcado."""
    q = [r for r in _quadro() if r["n"]]
    assert q, "sem conflito no disco, este teste nao mede nada"
    alvo = q[0]
    yid = None
    for y in _origens():
        try:
            if SA.nao_mencionados(y)["pacote"] == alvo["pacote"]:
                yid = y
                break
        except Exception:
            continue
    assert yid, "perdi a ancora: nenhuma origem resolve para %s" % alvo["pacote"]
    nm = SA.nao_mencionados(yid)
    t = SA.texto_dos_livres(yid)
    i = sorted(alvo["por_indice"])[0]
    marcados = {x["indice"]: x["declarado_por"] for x in t["livres"]}
    assert i in marcados and marcados[i], (
        "indice %d declarado por irmao e NAO vem marcado em texto_dos_livres" % i)
    kick = [x["kicker"] for x in t["livres"] if x["indice"] == i][0]
    assert kick in nm["nao_mencionados"], (
        "o conserto FILTROU o capitulo da lista de livres em vez de o NOMEAR — "
        "filtrar esconde o conflito e muda a base de toda leitura historica")


def test_contraprova_no_outro_sentido_NEM_TODO_livre_e_declarado():
    q = [r for r in _quadro() if r["n"]]
    assert q, "sem conflito no disco, este teste nao mede nada"
    algum_sobra = False
    for r in q:
        yid = None
        for y in _origens():
            try:
                if SA.nao_mencionados(y)["pacote"] == r["pacote"]:
                    yid = y
                    break
            except Exception:
                continue
        if not yid:
            continue
        t = SA.texto_dos_livres(yid)
        if any(not x["declarado_por"] for x in t["livres"]):
            algum_sobra = True
            break
    assert algum_sobra, (
        "TODO capitulo livre e declarado por algum irmao — entao a marca nao "
        "distingue nada e ela deixa de avisar, que e o argumento pelo qual o "
        "`mira.py` nao e portao")


def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos():
    assert hasattr(SA, "_linha_dos_declarados")
    fonte = inspect.getsource(SA)
    # a frase da marca mora num dono so; o `relato_dos_livres` a CHAMA
    corpo = _fonte(SA.relato_dos_livres)
    nomes = {n.func.id for n in ast.walk(corpo)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "_linha_dos_declarados" in nomes, (
        "o `relato_dos_livres` nao chama o dono da frase — import sem chamada e "
        "a classe dos layouts mortos")
    com = SA._linha_dos_declarados({"declarados_por_irmao": [7, 9]})
    sem = SA._linha_dos_declarados({"declarados_por_irmao": []})
    assert "7" in com and "9" in com
    assert sem.strip(), (
        "sem conflito a linha CALA — e ausencia de linha e indistinguivel de "
        "linha que nao foi escrita, que e exatamente o que me levou ao 74")
    assert com != sem


def test_o_exceto_vai_nos_DOIS_sentidos():
    """A peca da propria rodada nao conta como irmao declarante."""
    q = [r for r in _quadro() if r["n"]]
    assert q, "sem conflito no disco, este teste nao mede nada"
    alvo, yid = None, None
    for r in q:
        for y in _origens():
            try:
                if SA.nao_mencionados(y)["pacote"] == r["pacote"]:
                    yid = y
                    break
            except Exception:
                continue
        if yid:
            alvo = r
            break
    assert alvo, "perdi a ancora"
    quem = sorted({p for v in alvo["por_indice"].values() for p in v})
    assert quem, "nenhum irmao declarante nomeado"
    fora = SA.declarados_pelos_irmaos(yid, exceto=quem[0])
    restam = {p for v in fora["por_indice"].values() for p in v}
    assert quem[0] not in restam, (
        "`exceto` nao tirou %s da contagem de declarantes" % quem[0])
    # e no outro sentido: nome que nao casa nao filtra nada
    igual = SA.declarados_pelos_irmaos(yid, exceto="pacote-que-nao-existe-000")
    assert igual["n"] == alvo["n"], (
        "`exceto` que nao casa FILTROU alguem — ausencia de nome nao e ausencia "
        "de peca (17/10)")


def test_a_declaracao_e_DELEGADA_por_AST():
    corpo = _fonte(SA.declarados_pelos_irmaos)
    chamadas = {ast.unparse(n.func) for n in ast.walk(corpo)
                if isinstance(n, ast.Call)}
    assert any("IO.irmaos" in c for c in chamadas), (
        "o conserto nao chama o dono da declaracao (`irmaos_da_origem`)")
    fonte = textwrap.dedent(inspect.getsource(SA.declarados_pelos_irmaos))
    for proibido in ("_citados", "capitulos_negados", "findall", "re."):
        assert proibido not in fonte.split('"""')[-1], (
            "o corpo reimplementa a leitura da declaracao (%s) — isso cria o "
            "SEGUNDO dono dela, que e o defeito que este arquivo mede"
            % proibido)


def test_a_guarda_de_vacuidade_LEVANTA_em_vez_de_devolver_vazio():
    """`dir_specs` na posicao de `raiz` e o defeito de 20/10 as 12:3x."""
    with pytest.raises(Exception):
        IO.irmaos("-5aMrDsxlZE", SPECS)   # posicao de `raiz`: caminho nao existe
    # contraprova: a raiz CERTA continua respondendo
    assert IO.irmaos(PAR_DE_12H[0], RAIZ), (
        "a guarda calou a chamada certa — ela tem de levantar so no caminho "
        "inexistente")


def test_o_dir_specs_ARBITRARIO_continua_servindo():
    """A regressao que a suite pegou: 26 falhas contra 25.

    A segunda versao do conserto derivava a raiz do `dir_specs` por convencao, e
    o `texto_dos_livres` e chamado com diretorio ARBITRARIO (parque proprio de
    teste). Exigir `fabrica/specs` no caminho quebrou todo chamador que nao a
    cumpre — e o certo era o TESTE dele, nao o meu conserto.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        # diretorio que EXISTE e esta fora da convencao: nao levanta e nao
        # inventa irmao nenhum
        assert IO.irmaos("qualquer-origem", dir_specs=d) == []
        assert SA.texto_dos_livres("qualquer-origem", d)["pacote"] is None
    # e o `dir_specs` VENCE a raiz quando os dois vem
    assert IO.irmaos(PAR_DE_12H[0], "/caminho/que/nao/existe",
                     dir_specs=SPECS), (
        "o `dir_specs` nao venceu a raiz — se perder, o chamador que o passa "
        "volta a depender da convencao que esta regressao mostrou nao valer")


def test_a_passagem_e_por_NOME_e_nao_por_POSICAO():
    """Por AST: o defeito original era o `dir_specs` na segunda posicao."""
    corpo = _fonte(SA.declarados_pelos_irmaos)
    for n in ast.walk(corpo):
        if isinstance(n, ast.Call) and ast.unparse(n.func).endswith("irmaos"):
            assert len(n.args) <= 1, (
                "`IO.irmaos` chamado com segundo argumento POSICIONAL: ali mora "
                "a `raiz`, e foi exatamente esse engano que devolveu n = 0")
            assert any(k.arg == "dir_specs" for k in n.keywords), (
                "o diretorio nao vai pelo argumento proprio dele")
            return
    raise AssertionError("nao achei a chamada a `IO.irmaos`")


def test_a_DECLARACAO_tambem_e_indicio_e_a_medida_e_RECONFERIDA():
    """Numero do docstring que ninguem reconfere envelhece calado (753)."""
    q = _quadro()
    pares = sum(len(v) for r in q for v in r["por_indice"].values())
    assert pares > 0
    so_na_reserva = 0
    copies = {}
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        copies[d.get("pacote", "")] = d.get("copy", "") or ""
    for r in q:
        for i, pacs in r["por_indice"].items():
            for pac in pacs:
                cp = copies.get(pac, "")
                m = re.search(r"^## RESERVA\s*$(.*?)(?=^## |\Z)", cp,
                              re.S | re.M)
                res = m.group(1) if m else ""
                if not res:
                    continue
                fora = cp.replace(res, "")
                if str(i) in re.findall(r"\d+", res) and \
                        str(i) not in re.findall(r"\d+", fora):
                    so_na_reserva += 1
    frac = so_na_reserva / float(pares)
    assert frac < 0.5, (
        "a MAIORIA das declaracoes (%.1f%%) vem de uma secao `## RESERVA`, isto "
        "e, de territorio ALHEIO e nao de uso — entao 'declarado' deixou de "
        "indicar uso e esta nota tem de ser relida" % (100 * frac))
