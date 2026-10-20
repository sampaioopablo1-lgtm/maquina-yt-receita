"""O parametro `exceto` tinha DUAS convencoes, e errar a convencao CALAVA.

Medido em 20/10 as 11:3x, escrevendo o `labtreinamento-s092`. Cinco funcoes da
fabrica aceitam `exceto` — a peca da PROPRIA rodada, que ja esta no disco quando
eu pergunto — e elas se dividiam em duas convencoes incompativeis: o
`concentracao.contagem` (e o `pauta_do_momento`, que delega a ele) queria o
PACOTE; o `esqueleto_entre_canais.novidade`, o `contagem_de_cenas` e o
`variedade._especs_do_canal` queriam o NOME DO ARQUIVO.

Errar falhava em SILENCIO: `exceto` que nao casa nao filtra nada, e nenhuma
levanta. Na rodada que produziu este arquivo eu passei o PACOTE ao
`EC.novidade`, ele devolveu `forma_inedita: False` com `1 exemplar` para uma
forma que a frota NAO tem, e eu ia escrever isso na copy.

A forma destes testes: o que se cobra e a PROPRIEDADE de as duas convencoes
CONCORDAREM nas cinco, nunca o valor de uma delas numa peca nomeada — nomear a
`s092` seria identidade onde ha propriedade (743/753/761). E ha contraprova nos
dois sentidos: `exceto` vazio nao pode filtrar nada, e `exceto` de peca que nao
existe tambem nao.
"""

import ast
import json
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAB = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FAB)

import concentracao as CC              # noqa: E402
import contagem_de_cenas as CDC        # noqa: E402
import esqueleto_entre_canais as EC    # noqa: E402
import nome_da_spec as NS              # noqa: E402
import variedade as V                  # noqa: E402

# Os cinco chamadores, com a convencao que CADA UM documenta. A lista e dos
# modulos, nao minha: um deles sem `exceto` na assinatura reprova abaixo.
CHAMADORES = {
    "concentracao.py": "contagem",
    "contagem_de_cenas.py": "contagens_da_frota",
    "esqueleto_entre_canais.py": "novidade",
    "pauta_do_momento.py": "quadro",
    "variedade.py": "_especs_do_canal",
}


def _uma_peca_do_disco():
    """Uma peca de short do disco, DERIVADA e nao nomeada.

    Ela tem de ser a UNICA do seu canal com o seu esqueleto, senao excluir
    ou nao excluir da no mesmo e o teste nao mede nada.
    """
    pecas = EC.varre()
    q = EC.quadro(pecas)
    for p in pecas:
        esq = p.get("esqueleto")
        if esq and q["contagem_da_forma"].get(esq) == 1:
            return p
    pytest.fail("nenhuma peca do disco e o unico exemplar da propria forma — "
                "sem ela este arquivo nao mede o silencio do `exceto`")


def test_a_varredura_nao_e_vacua():
    pecas = EC.varre()
    assert len(pecas) >= 200, (
        "menos de 200 pecas de short no disco: a varredura encolheu e os "
        "testes abaixo passariam por vacuidade")


def test_os_cinco_chamadores_AINDA_tem_o_parametro():
    """Se um perder o `exceto`, esta nota se rele em vez de ficar."""
    faltam = []
    for arq, fn in CHAMADORES.items():
        fonte = open(os.path.join(FAB, arq), encoding="utf-8").read()
        arvore = ast.parse(fonte)
        achou = False
        for no in ast.walk(arvore):
            if isinstance(no, ast.FunctionDef) and no.name == fn:
                nomes = [a.arg for a in no.args.args]
                if "exceto" in nomes:
                    achou = True
        if not achou:
            faltam.append("%s:%s" % (arq, fn))
    assert not faltam, "perderam o `exceto`: %s" % faltam


def test_as_DUAS_convencoes_concordam_no_ESQUELETO():
    """O defeito medido: PACOTE calava no `EC.novidade`."""
    p = _uma_peca_do_disco()
    arq, pac = p["arquivo"], NS.pacote(p["arquivo"])
    assert arq != pac, "a peca tem de ter as duas formas distintas"
    por_arq = EC.novidade(p["esqueleto"], p["cenas"], exceto=arq)
    por_pac = EC.novidade(p["esqueleto"], p["cenas"], exceto=pac)
    assert por_arq["exemplares_da_forma"] == por_pac["exemplares_da_forma"], (
        "as duas convencoes de `exceto` divergem no `EC.novidade`: "
        "arquivo=%d contra pacote=%d — e a errada CALA, nao levanta"
        % (por_arq["exemplares_da_forma"], por_pac["exemplares_da_forma"]))
    assert por_arq["forma_inedita"] and por_pac["forma_inedita"], (
        "peca que e o unico exemplar da propria forma tem de sair INEDITA "
        "com as duas convencoes — foi este o relato errado de 11:3x")


def test_as_DUAS_convencoes_concordam_na_CONTAGEM_de_pauta():
    """O defeito no outro sentido: ARQUIVO calava no `concentracao.contagem`."""
    pecas = [p for p in EC.varre() if p.get("canal")]
    assert pecas, "sem canal nas pecas, este teste nao mede nada"
    # uma peca que DECLARA origem, senao a contagem nao a conta de todo jeito
    alvo = None
    for p in pecas:
        d = json.load(open(os.path.join(FAB, "specs", p["arquivo"]),
                           encoding="utf-8"))
        if d.get("longo_existente"):
            alvo = (p, d["longo_existente"])
            break
    assert alvo, "nenhuma peca do disco declara `longo_existente`"
    p, origem = alvo
    canal = p["canal"]
    arq, pac = p["arquivo"], NS.pacote(p["arquivo"])
    por_arq = CC.contagem(canal, exceto=arq).get(origem)
    por_pac = CC.contagem(canal, exceto=pac).get(origem)
    sem = CC.contagem(canal).get(origem)
    assert por_arq == por_pac, (
        "as duas convencoes divergem no `concentracao.contagem`: "
        "arquivo=%s contra pacote=%s" % (por_arq, por_pac))
    assert por_arq == sem - 1, (
        "excluir a peca tem de descontar UM uso da origem dela "
        "(sem exceto=%s, com=%s) — se nao desconta, o `exceto` nao filtra"
        % (sem, por_arq))


def test_as_DUAS_convencoes_concordam_no_PORTAO():
    """O `variedade` e PORTAO, logo a concordancia ali vale por si."""
    pecas = [p for p in EC.varre() if p.get("canal")]
    p = pecas[0]
    d = json.load(open(os.path.join(FAB, "specs", p["arquivo"]),
                       encoding="utf-8"))
    slug = d.get("slug", "")
    raiz = os.path.join(FAB, "specs")
    por_arq = V._especs_do_canal(raiz, slug, p["arquivo"])
    por_pac = V._especs_do_canal(raiz, slug, NS.pacote(p["arquivo"]))
    assert len(por_arq) == len(por_pac), (
        "as duas convencoes divergem dentro do portao `variedade`: "
        "%d contra %d" % (len(por_arq), len(por_pac)))


def test_contraprova_exceto_VAZIO_nao_filtra_nada():
    """Sem esta, bastaria `casa` devolver True e tudo 'concordaria'."""
    pecas = EC.varre()
    assert len(EC.varre()) == len(pecas)
    p = _uma_peca_do_disco()
    com = EC.novidade(p["esqueleto"], p["cenas"], exceto=p["arquivo"])
    sem = EC.novidade(p["esqueleto"], p["cenas"], exceto="")
    assert sem["exemplares_da_forma"] == com["exemplares_da_forma"] + 1, (
        "`exceto` vazio tem de deixar a peca DENTRO da varredura")
    assert not NS.casa("qualquer.json", ""), (
        "`casa` com `exceto` vazio nao pode casar — filtraria a frota inteira")


def test_contraprova_exceto_de_peca_INEXISTENTE_nao_filtra():
    p = _uma_peca_do_disco()
    sem = EC.novidade(p["esqueleto"], p["cenas"], exceto="")
    fantasma = EC.novidade(p["esqueleto"], p["cenas"],
                           exceto="nao-existe-no-disco-99999.json")
    assert fantasma["exemplares_da_forma"] == sem["exemplares_da_forma"], (
        "`exceto` de peca que nao existe nao pode mudar a contagem")


def test_a_conversao_tem_UM_dono_por_AST():
    """Ninguem mais monta o nome do arquivo por conta propria.

    Por AST e nao por texto, porque o `nome_da_spec` CITA a forma antiga na
    prosa que explica o defeito, e casar prosa pegaria a explicacao.
    """
    maus = []
    for arq in CHAMADORES:
        caminho = os.path.join(FAB, arq)
        arvore = ast.parse(open(caminho, encoding="utf-8").read())
        for no in ast.walk(arvore):
            # `"%s.json" % exceto` e `exceto + ".json"`
            if isinstance(no, ast.BinOp) and isinstance(no.op, (ast.Mod,
                                                                ast.Add)):
                fonte = ast.dump(no)
                if "exceto" in fonte and ".json" in fonte:
                    maus.append("%s: %s" % (arq, ast.unparse(no)))
            # `p["arquivo"] != exceto` / `nome != exceto` crus
            if isinstance(no, ast.Compare) and any(
                    isinstance(o, (ast.Eq, ast.NotEq)) for o in no.ops):
                alvo = ast.dump(no)
                if "'exceto'" in alvo or "id='exceto'" in alvo:
                    maus.append("%s: %s" % (arq, ast.unparse(no)))
    assert not maus, (
        "comparacao de `exceto` fora do dono (`nome_da_spec.casa`): %s" % maus)


def test_o_dono_e_IDEMPOTENTE_nas_duas_formas():
    for x in ("abc", "abc.json", "specs/abc.json", "/a/b/abc.json"):
        assert NS.pacote(x) == "abc", x
        assert NS.arquivo(x) == "abc.json", x
    assert NS.arquivo(NS.arquivo("abc")) == "abc.json"
    assert NS.pacote(NS.pacote("abc.json")) == "abc"
    assert NS.arquivo("") == "" and NS.pacote("") == ""


def test_o_MOTIVO_continua_escrito_no_dono():
    fonte = open(os.path.join(FAB, "nome_da_spec.py"), encoding="utf-8").read()
    for marca in ("SILENCIO", "forma_inedita", "PERMISSIVA",
                  "concentracao.contagem", "esqueleto_entre_canais"):
        assert marca in fonte, (
            "o motivo do modulo perdeu a marca %r — sem ele a rodada seguinte "
            "reintroduz a segunda convencao" % marca)


def test_o_CLI_do_dono_responde_as_duas_formas():
    r = subprocess.run([sys.executable, os.path.join(FAB, "nome_da_spec.py"),
                        "a", "a.json"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("'a.json'") >= 2, r.stdout
