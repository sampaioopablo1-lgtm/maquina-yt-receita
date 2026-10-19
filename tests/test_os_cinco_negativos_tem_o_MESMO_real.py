"""Os cinco residuos NEGATIVOS da serie tem real EXATAMENTE 41.

Medido em 18/10 as 17:2x, no quinto deles (`epomeno-epipedo-s061`, previsao 41,5
no edge, provedor MEDIDO pelo job 117736668345, real 41).

A propriedade que este arquivo guarda e sobre o REAL, nao sobre a previsao — e
e a terceira forma de descrever a mesma serie:
  * 17/10: "o negativo mora na janela estreita de 41,4 a 41,6" (caiu no 4o ponto,
    que previa 42,2);
  * 18/10 11:1x: "o negativo nao esta confinado a um ponto da previsao";
  * 18/10 17:2x, esta: **em TODOS eles o real e o mesmo inteiro.**

As duas primeiras olhavam a previsao, que varia. A regularidade esta no real, e
dela sai a leitura certa: o residuo negativo e a distancia entre uma previsao
qualquer da janela e o MENOR real que a janela produz — e nesta mesma janela o
canal ja deu 42, 43 e 44. Logo 41 e o PISO do espalhamento do 769/771, nao um
regime proprio.

O que isto NAO prova: que a voz grega encurte, nem que 41 seja piso fisico.
Cinco pontos de um canal — o enquadramento do 679/698/725. O que esta medido e
que o negativo e raro, e deste canal, e sempre no mesmo inteiro.
"""
import os
import re

SERIE = os.path.join(
    os.path.dirname(__file__), "test_residuo_quebra_o_limite_de_dois_segundos.py"
)
# `-s?\d+`: o sufixo de SHORT SOLTO e `-sNNN` e o de PACOTE e `-NNN`. A
# forma antiga, com `-s\d+` cravado, deixava o PRIMEIRO ponto de pacote
# (`epomeno-epipedo-068`, 19/10 as 13:1x) INVISIVEL para esta varredura — e
# ponto invisivel nao e so contagem errada: ele sai da medicao sem avisar.
LINHA = re.compile(r'^\s*\("([a-z-]+-s?\d+)",\s*([\d.]+),\s*(\d+),\s*"(\w+)"\),')
REAL_DOS_NEGATIVOS = 41


def _pontos():
    saida = []
    for linha in open(SERIE, encoding="utf-8"):
        m = LINHA.match(linha)
        if m:
            saida.append((m.group(1), float(m.group(2)), int(m.group(3))))
    return saida


def _negativos():
    return [(p, pv, r) for p, pv, r in _pontos() if r - pv < 0]


def test_a_varredura_nao_fica_vazia():
    """Regex que deixa de casar faria todos os outros passarem por vacuidade."""
    assert len(_pontos()) >= 90, len(_pontos())


def test_existem_pelo_menos_cinco_negativos():
    negs = _negativos()
    assert len(negs) >= 5, (
        f"a serie tem {len(negs)} negativo(s); este arquivo foi escrito com CINCO "
        "e perde a ancora com menos — releia a nota acima"
    )


def test_TODO_negativo_tem_o_MESMO_real():
    """O achado. Falha se aparecer negativo com real diferente — e ai a nota
    tem de ser RELIDA, nao o numero movido."""
    reais = sorted({r for _, _, r in _negativos()})
    assert reais == [REAL_DOS_NEGATIVOS], (
        f"os negativos agora tem reais {reais}; a nota de 18/10 17:2x diz que "
        "TODOS tem o mesmo inteiro, e um real diferente a derruba — releia em "
        "vez de ajustar a constante"
    )


def test_a_PREVISAO_dos_negativos_VARIA():
    """Contraprova da leitura: e a previsao que varia, nao o real."""
    prevs = {pv for _, pv, _ in _negativos()}
    assert len(prevs) >= 3, prevs
    assert max(prevs) - min(prevs) >= 0.5, prevs


def test_os_negativos_sao_do_MESMO_canal():
    canais = {p.rsplit("-s", 1)[0] for p, _, _ in _negativos()}
    assert canais == {"epomeno-epipedo"}, canais


def test_a_MESMA_janela_produz_real_MAIOR_no_mesmo_canal():
    """Sem isto, '41 sempre' leria como teto do canal em vez de PISO."""
    janela = [
        (p, pv, r)
        for p, pv, r in _pontos()
        if p.startswith("epomeno-epipedo") and 41.0 <= pv <= 42.5
    ]
    reais = sorted({r for _, _, r in janela})
    assert len(reais) >= 3, reais
    assert max(reais) > REAL_DOS_NEGATIVOS, (
        f"a janela deste canal so produz {reais}; a leitura de 41 como PISO do "
        "espalhamento depende de existir real maior na MESMA faixa de previsao"
    )


def test_o_negativo_continua_MINORIA_na_janela_comparavel():
    """"RARO" se cobra por MINORIA MEDIDA, nao por fracao inventada.

    A primeira versao deste assert era `negs/todos < 0,15` — numero meu, da
    mesma classe do `0,05` que reprovou em tres testes nesta rodada. A forma
    honesta compara os negativos com os NAO-negativos da MESMA janela de
    previsao, que e o unico conjunto contra o qual eles sao comparaveis.
    """
    janela = [
        (p, pv, r)
        for p, pv, r in _pontos()
        if p.startswith("epomeno-epipedo") and 41.0 <= pv <= 42.5
    ]
    assert janela, "a janela comparavel ficou vazia — este teste deixou de medir"
    neg = [p for p, pv, r in janela if r - pv < 0]
    assert len(neg) < len(janela) - len(neg), (
        f"{len(neg)} negativos contra {len(janela) - len(neg)} nao-negativos na "
        "mesma janela: deixou de ser minoria, releia a nota"
    )
