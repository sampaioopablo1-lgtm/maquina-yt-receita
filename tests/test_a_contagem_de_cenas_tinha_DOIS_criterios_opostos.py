"""A contagem de cenas tem dois criterios opostos, e eu os conciliei de cabeca.

Guarda o achado de 20/10 as 02:2x. A forma e a da semana: a varredura sai dos
DONOS (nao de uma tabela minha), a delegacao e cobrada por AST, os DOIS lados do
trade-off tem de existir, e um teste **falha se eles passarem a coincidir** —
porque ai o trade-off deixou de existir e esta nota tem de ser relida.
"""
import ast
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import contagem_de_cenas as CC   # noqa: E402
import ensaio                    # noqa: E402
import mira                      # noqa: E402

MOD = os.path.join(RAIZ, "fabrica", "contagem_de_cenas.py")

VOZ = {"labtreinamento": "pt-BR-ThalitaMultilingualNeural",
       "epomeno-epipedo": "el-GR-NestorasNeural",
       "kolejny-poziom": "pl-PL-MarekNeural"}


def test_o_canal_com_mira_propria_ABRE_janela():
    e = CC.escolha("labtreinamento", VOZ["labtreinamento"])
    assert e["abertas"] >= 10, (
        "o canal de mira larga deixou de abrir janela em quase toda contagem "
        "de cena — sem esse lado o arquivo nao mede trade-off nenhum"
    )


def test_os_OUTROS_dois_canais_NAO_abrem_nenhuma():
    """Contraprova no outro sentido: sem ela, 'abre janela' passaria sempre."""
    for canal in ("epomeno-epipedo", "kolejny-poziom"):
        e = CC.escolha(canal, VOZ[canal])
        assert e["abertas"] == 0, (
            f"{canal} passou a abrir janela nos dois mundos — a pinca do "
            "740/748 afrouxou e esta nota tem de ser relida"
        )
        assert e["por_cadencia"] is None and e["por_largura"] is None
        assert "740/748" in e["motivo"], (
            "a recusa tem de NOMEAR a pinca em vez de so devolver vazio"
        )


def test_os_DOIS_criterios_NAO_coincidem():
    """O achado. Falha se eles passarem a apontar a mesma contagem."""
    e = CC.escolha("labtreinamento", VOZ["labtreinamento"])
    assert e["coincidem"] is False, (
        "a janela mais larga e a melhor cadencia passaram a coincidir — o "
        "trade-off desapareceu e esta nota tem de ser relida, nao reaproveitada"
    )
    assert e["custo_em_caracteres"] > 0
    # e a cadencia escolhida paga MESMO o preco: a janela dela e estreita
    assert e["por_cadencia"]["largura"] < e["por_largura"]["largura"]


def test_a_largura_ENCOLHE_mas_NAO_e_monotona():
    """As duas metades da frase, porque a primeira versao dizia so a primeira.

    Eu escrevi "cai monotonamente" e a propria saida me desmentiu. O teste
    cobra a TENDENCIA (as poucas cenas tem janela muito mais larga que as
    muitas) e PROIBE a afirmacao de monotonia, exigindo que exista ao menos
    uma subida — porque enquanto ela existir a palavra "monotona" e falsa.
    """
    q = [x for x in CC.quadro("labtreinamento", VOZ["labtreinamento"])
         if x["janela"]]
    larguras = [x["largura"] for x in q]
    assert larguras[0] > larguras[-1] * 3, "a tendencia de queda desapareceu"
    subidas = [i for i in range(1, len(larguras))
               if larguras[i] > larguras[i - 1]]
    assert subidas, (
        "a largura passou a cair monotonamente — entao a correcao do docstring "
        "deixou de valer e a frase tem de ser reescrita no lugar"
    )


def test_a_janela_e_a_faixa_sao_DELEGADAS_por_AST():
    """Por AST, porque o docstring CITA os nomes na prosa que se explica."""
    arv = ast.parse(open(MOD, encoding="utf-8").read())
    chama = set()
    for n in ast.walk(arv):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if isinstance(n.func.value, ast.Name):
                chama.add(f"{n.func.value.id}.{n.func.attr}")
    assert "mira.janela_dos_dois_mundos" in chama, (
        "a janela tem de sair do dono (`mira`), nunca ser recalculada aqui"
    )
    assert "ensaio.alvo_short" in chama, (
        "a faixa tem de sair do acessor de fonte unica (`ensaio.alvo_short`)"
    )


def test_a_CADENCIA_tem_UM_dono_e_declara_a_procedencia():
    t = open(MOD, encoding="utf-8").read()
    assert CC.CADENCIA_MEDIDA_S == 3.1
    assert "690/699" in t, (
        "a procedencia da cadencia tem de ir escrita: sem ela 3,1 e limiar sem "
        "procedencia (§10)"
    )
    # e ela NAO pode aparecer recopiada noutro lugar do corpo
    corpo = t.split('"""', 2)[-1]
    assert corpo.count("3.1") == 1, (
        "a cadencia aparece mais de uma vez no corpo — numero calculado que se "
        "repete escrito e o 753"
    )


def test_a_cadencia_sai_da_duracao_REAL_e_nao_da_estimada():
    """A distincao de unidade, cobrada pelo valor.

    O vao entre as duas grandezas e ~1,14 s numa peca de 7 cenas nesta mira. Se
    o modulo passasse a dividir a estimada, a cadencia de 7 cenas cairia de
    ~3,29 para ~3,14 — este teste ancora no valor da REAL.
    """
    q = {x["cenas"]: x for x in CC.quadro("labtreinamento",
                                          VOZ["labtreinamento"])}
    faixa = ensaio.alvo_short("labtreinamento")
    meio = (faixa[0] + faixa[1]) / 2
    assert abs(q[7]["cadencia_s"] - meio / 7) < 1e-9, (
        "a cadencia deixou de ser o MEIO da faixa (uma duracao REAL) dividido "
        "pelas cenas — se virou a estimada, sao duas grandezas com um nome"
    )
    assert q[7]["cadencia_s"] > 3.2, (
        "a cadencia de 7 cenas caiu abaixo de 3,2: isso e o valor da ESTIMADA, "
        "nao da real"
    )


def test_faixa_ausente_LEVANTA():
    with pytest.raises(ValueError, match="nao tem faixa"):
        CC.quadro("canal-que-nao-existe", VOZ["labtreinamento"], faixa=())


def test_a_peca_da_rodada_confirma_a_escolha_do_instrumento():
    """A `s089` foi escrita com 7 cenas por conta de cabeca; o instrumento,
    escrito depois, devolve 7. Sem este teste a nota nao prova que ele
    reproduz a decisao que de fato foi tomada."""
    import json
    sp = json.load(open(os.path.join(RAIZ, "fabrica", "specs",
                                     "labtreinamento-s089.json"),
                        encoding="utf-8"))
    e = CC.escolha("labtreinamento", sp["voz"])
    assert e["por_cadencia"]["cenas"] == len(sp["short"]) == 7
    media = sum(len(c["nar"]) for c in sp["short"]) / len(sp["short"])
    lo, hi = e["por_cadencia"]["janela"]
    assert lo <= media <= hi, (
        f"a media de {media:.1f} caracteres saiu fora da janela {(lo,hi)} que "
        "o instrumento aponta para essa contagem"
    )


def test_NAO_e_portao_e_a_saida_e_zero():
    r = subprocess.run([sys.executable, MOD, "labtreinamento"],
                       capture_output=True, text=True, cwd=RAIZ, timeout=300)
    assert r.returncode == 0, "isto INFORMA: o codigo de saida e sempre zero"
    assert "NAO coincidem" in r.stdout
    # e o canal sem janela tambem sai zero, com o motivo escrito
    r2 = subprocess.run([sys.executable, MOD, "kolejny-poziom"],
                        capture_output=True, text=True, cwd=RAIZ, timeout=300)
    assert r2.returncode == 0 and "740/748" in r2.stdout
