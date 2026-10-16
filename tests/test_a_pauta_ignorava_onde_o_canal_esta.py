"""A escolha de pauta nao tinha coordenada de TEMPO — e o dono viu antes de mim.

Palavras dele, 16/10: *"Estas producoes estao muito distantes do ultimo video
produzido e publicado no canal labtreinamento"*.

MEDIDO antes de concordar. Rank da origem de cada uma das dez ultimas pecas do
canal (1 = o longo mais NOVO, pela playlist de uploads VIVA):

    s051 14 | s052 13 | s053 12 | s054 7 | s055 3
    s056  2 | s057 11 | s058  1 | s059  1 | s060 14

As duas anteriores a ultima sairam do topo do canal e a seguinte voltou treze
posicoes. Ele estava certo, e o numero diz quanto.

E A MINHA PRIMEIRA HIPOTESE ESTAVA ERRADA, o que vai registrado porque custou
uma conta: eu supus que espalhar uso puxaria sistematicamente para o passado.
Spearman(usos, rank) = **-0,21** com uso quase plano (4 em doze das catorze
origens) — o criterio nao puxa para tras em media, ele e CEGO, e com uso
empatado o desempate cai em qualquer lugar.

A CAUSA ESTRUTURAL e outra, e esta travada abaixo: o filtro `escrevivel`
exclui exatamente o **rank 1**, porque o longo mais novo e justamente o que
ainda nao tem spec local. Entao a pauta e empurrada para fora do topo por um
filtro que fala de DISPONIBILIDADE DE TEXTO, nao de valor editorial — e a rota
da regra (h) ja resolve isso (o `s058` e o `s059` sairam do rank 1 por ela).
"""
import collections
import glob
import json
import os
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import concentracao as C  # noqa: E402
import recencia  # noqa: E402

# Ordem VIVA lida da playlist de uploads em 16/10 (1 = mais novo).
ORDEM = [
    "FtCtIJPsc_Q", "NNgAQLlpEzg", "Sr6VhvD_aPE", "QiaGg03WSR0", "lau1nnOUm1U",
    "6BeNHqT2okA", "dsoEo103l1o", "bQoujWaY7Hw", "ntrMxq89I4o", "4OYBkCHFTV8",
    "3KtwRYxl7_U", "yrWVyqQtw00", "KRUERlNPzDw", "StQNFMdpGdk", "JW-CqcPR-3g",
    "7_4ww12Y3tU", "R2AvmiPohHA", "F5p-7MDmlbE", "qwGkZCTdQJQ", "XgqPVJuAk3o",
]

# O que de fato aconteceu, medido nas specs.
RANKS_DAS_DEZ = {
    "s051": 14, "s052": 13, "s053": 12, "s054": 7, "s055": 3,
    "s056": 2, "s057": 11, "s058": 1, "s059": 1, "s060": 14,
}


def _usos():
    u = collections.Counter()
    for f in glob.glob(str(RAIZ / "fabrica" / "specs" / "labtreinamento-s*.json")):
        with open(f, encoding="utf-8") as fh:
            o = json.load(fh).get("longo_existente")
        if o:
            u[o] += 1
    return dict(u)


def test_o_salto_que_o_dono_apontou_esta_medido():
    assert RANKS_DAS_DEZ["s058"] == RANKS_DAS_DEZ["s059"] == 1
    assert RANKS_DAS_DEZ["s060"] == 14
    salto = RANKS_DAS_DEZ["s060"] - RANKS_DAS_DEZ["s059"]
    assert salto == 13, salto


def test_as_specs_confirmam_os_ranks_das_duas_pontas():
    """O rank nao e anotacao minha: ele sai do `longo_existente` da spec."""
    for pacote, esperado in (("labtreinamento-s059", 1),
                             ("labtreinamento-s060", 14)):
        with open(RAIZ / "fabrica" / "specs" / f"{pacote}.json", encoding="utf-8") as fh:
            o = json.load(fh)["longo_existente"]
        assert recencia.rank(o, ORDEM) == esperado, (pacote, o)


def test_o_filtro_escrevivel_exclui_EXATAMENTE_o_topo():
    """A causa estrutural, e o que ela NAO e.

    Entre as origens recentes, a unica que o filtro exclui e o rank 1 — porque
    longo novo ainda nao tem spec local. Os outros `False` sao ranks 15 a 19,
    que sao copias do mesmo titulo e nao disputam pauta.
    """
    nao_escreviveis = [i for i, o in enumerate(ORDEM, 1)
                       if not C.escrevivel(o, "labtreinamento")]
    assert 1 in nao_escreviveis, (
        "o topo do canal passou a ter spec local: refaca a leitura, porque a"
        " causa estrutural desta nota deixou de existir"
    )
    recentes_excluidas = [i for i in nao_escreviveis if i <= 14]
    assert recentes_excluidas == [1], recentes_excluidas


def test_a_hipotese_do_uso_puxando_para_tras_NAO_se_sustenta():
    """Registrado porque era a minha primeira explicacao, e estava errada.

    CORRIGIDO EM 16/10 as 19:3x, e o defeito era do TESTE, nao da nota. Ele
    cobrava `abs(rho) < 0,5` — dois lados — enquanto a hipotese que ele nega e de
    UM lado so: "espalhar uso puxa a pauta para o PASSADO" exige uso alto em rank
    ALTO, isto e, rho POSITIVO. Qualquer correlacao negativa forte reprovava o
    teste sem por aquela hipotese de volta na mesa.

    E ela apareceu: medido nesta rodada, `rho = -0,54`. O sinal e o OPOSTO do que
    a hipotese descartada previa, e a causa e conhecida e minha — a regra de
    RECENCIA, aplicada desde 16/10, serve o longo MAIS NOVO primeiro, logo as
    origens de rank baixo acumulam uso. **Isso nao ressuscita nada; e o efeito
    medido da regra nova.**

    O teste passa a cobrar o lado certo, e so esse: rho POSITIVO e forte reabre a
    hipotese e obriga a reler. O lado negativo sai IMPRESSO na mensagem em vez de
    reprovar, porque la a leitura ja esta escrita.
    """
    usos = _usos()
    pares = [(n, recencia.rank(o, ORDEM)) for o, n in usos.items()
             if recencia.rank(o, ORDEM)]
    assert len(pares) >= 13

    def _rk(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for k, i in enumerate(s):
            r[i] = k + 1
        return r

    xs = _rk([p[0] for p in pares])
    ys = _rk([p[1] for p in pares])
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    rho = num / den
    assert rho < 0.5, (
        f"Spearman(usos, rank) = {rho:+.2f}, POSITIVO e forte: uso alto em rank"
        " alto e exatamente a hipotese que eu descartei em 16/10, e ela volta a"
        " estar na mesa. RELEIA a nota em vez de mover este numero."
    )
    # O outro lado nao reprova, e o motivo esta no docstring: rho negativo forte
    # e o efeito ESPERADO da regra de recencia servindo o topo.


def test_o_relato_RECUSA_ordenar_pelo_retrato_de_06_10():
    """O retrato nao conhece os longos novos — e sao eles a pergunta."""
    texto = recencia.relato(_usos(), recencia.ordem_do_retrato("labtreinamento"),
                            topo_vivo="FtCtIJPsc_Q")
    assert "nao ordena" in texto
    assert "playlist de uploads VIVA" in texto


def test_o_relato_NOMEIA_o_custo_da_escolha_cega():
    """Com a ordem viva ele imprime as duas coordenadas e o rank de cada uma."""
    texto = recencia.relato(_usos(), ORDEM, topo_vivo="FtCtIJPsc_Q")
    assert "1 = o longo MAIS NOVO" in texto
    assert "menos usada:" in texto
    assert "rank=1" in texto
    assert "critério inventado" in texto   # nao vira peso sem procedencia


def test_o_modulo_nao_escolhe_sozinho():
    """Trava de desenho: ele CONTA, nao decide — peso entre as duas coordenadas
    nao esta medido, e inventar um seria o erro que a §10 proibe."""
    fonte = (RAIZ / "fabrica" / "recencia.py").read_text(encoding="utf-8")
    assert "nao escolhe sozinho" in fonte
    a = recencia.analise(_usos(), ORDEM, topo_vivo="FtCtIJPsc_Q")
    assert a["ok"] and "corte_de_recente" in a
