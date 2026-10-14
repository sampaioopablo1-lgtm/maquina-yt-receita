"""O 734 dizia "o real fica acima por NO MAXIMO 1,9 s". O quinto ponto deu +2,4 s.

Medido em 13/10 as 22:2x, no `labtreinamento-s034` (`wWmHRDmQMO4`): provedor
MEDIDO pela anotacao (zero avisos do Piper, logo EDGE), previsao edge 25,6 e real
**28** -- resido **+2,4 s**, **+9,4%**, acima do maior desvio ja observado nos
dois eixos.

E o ponto que mais corta: o `s033` previa **25,7** edge e deu **27**; o `s034`
previa **25,6** e deu **28**. Mesmo canal, mesma voz, mesmas dez cenas, mesmo
provedor medido, previsoes a UM DECIMO de distancia -- e reais diferentes em um
segundo inteiro. Logo o OFFSET tambem nao descreve: ele teria de ser constante.

O que sobrevive: o SINAL. Cinco de cinco acima da previsao do provedor que de
fato narrou.

O que isto custa na producao, e vai dito em vez de virar limiar: a mira do
`labtreinamento` e sobre a duracao REAL (20,0 a 26,0) e o `mira.py` a cobra sobre
o ESTIMADO. Estimado dentro nos dois mundos NAO poe o real dentro: o `s033` saiu
em 27 e o `s034` em 28. NAO mexi na mira -- n=5, e a trava da secao 10 vale.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

# (pacote, previsao do provedor MEDIDO, real, provedor medido pela anotacao)
SERIE = [
    ("epomeno-epipedo-s024", 43.1, 44, "edge"),
    ("kolejny-poziom-s024", 42.9, 44, "edge"),
    ("epomeno-epipedo-s025", 42.1, 44, "edge"),
    ("labtreinamento-s033", 25.7, 27, "edge"),
    ("labtreinamento-s034", 25.6, 28, "edge"),
    # 741: PRIMEIRO ponto out-of-sample DA BANDA. A copy do s035 anunciou, antes
    # de publicar, que o real cairia entre 25,7 e 27,2 se o edge narrasse.
    # Provedor medido edge (zero avisos), real 27 -> residuo +2,2 s, DENTRO.
    ("labtreinamento-s035", 24.8, 27, "edge"),
    # 742: SEGUNDO ponto out-of-sample da banda, e ela acertou outra vez.
    ("labtreinamento-s036", 25.3, 27, "edge"),
    # 744: TERCEIRO ponto out-of-sample da banda, dentro outra vez.
    ("labtreinamento-s037", 25.8, 28, "edge"),
    # 746: primeira peca do canal narrada pelo edge a cair DENTRO da mira.
    ("labtreinamento-s038", 24.4, 26, "edge"),
    # 747: 24,7 deu 27 (FORA) -- 0,3 s de previsao, 1 s de real.
    ("labtreinamento-s039", 24.7, 27, "edge"),
    # 748: MESMA previsao, MESMO real -- reprodutibilidade, contra o 732.
    ("labtreinamento-s040", 24.7, 27, "edge"),
    # 14/10: s041, outra origem, mesma forma de dez cenas. +2,4 EMPATA o teto.
    ("labtreinamento-s041", 24.6, 27, "edge"),
    # 751: o OUTRO LADO da pinca — previsao ABAIXO do piso do piper (23,4),
    # e o real caiu DENTRO da mira (25). Primeira vez em seis pecas do edge.
    ("labtreinamento-s042", 23.4, 25, "edge"),
    # 752: previsao praticamente IGUAL a do s042 (23,3 contra 23,4) e real DOIS
    # segundos acima — residuo +3,7, que QUEBRA o teto de 2,4 de treze pontos.
    ("labtreinamento-s043", 23.3, 27, "edge"),
    # 753: de volta a mirar a mira VERDE (24,9). Real 27, residuo +2,1 — DENTRO
    # da banda ampliada, e o real FORA da mira, como a copy declarou.
    ("labtreinamento-s044", 24.9, 27, "edge"),
    ("labtreinamento-s045", 24.5, 27, "edge"),   # 754: +2,5, dentro da banda
    ("labtreinamento-s046", 24.6, 26, "edge"),
    # 756: previsao 25,4 (mira VERDE nos dois mundos, postura do 753), real 27 —
    # residuo +1,6, DENTRO da banda. FORA da mira, como a copy declarou antes de
    # publicar: o tally do 754 vai a SEIS de oito no mundo edge.
    ("labtreinamento-s047", 25.4, 27, "edge"),
    # 758: previsao 25,0 (mira VERDE), real 27 — residuo +2,0, dentro da banda.
    # FORA da mira outra vez: o tally do 754/757 vai a SETE de dez.
    ("labtreinamento-s048", 25.0, 27, "edge"),
    # 759: primeira peca da origem SEM SPEC LOCAL (regra h, legenda pelo pg_net).
    # Previsao 25,1 (mira VERDE), real 27 — residuo +1,9. Tally a OITO de onze.
    ("labtreinamento-s049", 25.1, 27, "edge"),
    # 760: previsao 24,9 (mira VERDE na PRIMEIRA versao), real 27 — residuo +2,1.
    # Tally a NOVE de doze, e as treze origens do canal passaram a ter >= 2 shorts.
    ("labtreinamento-s050", 24.9, 27, "edge"),
    # 763: o primeiro ponto do epomeno desde o s025 — e ele RECOLOCA a serie
    # como MULTICANAL, que ela sempre foi (os tres primeiros pontos do 734 sao
    # do epomeno e do kolejny). Previsao 41,4 no mundo edge, real 43, +1,6.
    ("epomeno-epipedo-s026", 41.4, 43, "edge"),   # 755: +1,4, e o real DENTRO da mira
    # 764: o primeiro ponto do KOLEJNY desde o s024, e o maior residuo da serie
    # FORA do labtreinamento: previsao edge 41,2 (mira da FROTA, piso), real 44,
    # residuo +2,8 — dentro da banda, e segundo maior valor dela.
    ("kolejny-poziom-s025", 41.2, 44, "edge"),
    # 766: previsao 41,3 e real 43 — o MESMO par do epomeno-epipedo-s026
    # (41,4 -> 43) a uma hora de distancia, logo a previsao REPRODUZ nesta
    # faixa, o que o 732 havia negado e o 748 ja tinha visto no lado curto.
    ("epomeno-epipedo-s027", 41.3, 43, "edge"),
    # 767: previsao 41,6 e real 43 — contra o kolejny-poziom-s025 (41,2 -> 44)
    # da hora anterior. Previsao MAIOR, real MENOR, mesmo canal e mesma voz:
    # some o apoio da frase "a previsao REPRODUZ" que eu escrevi no 766.
    ("kolejny-poziom-s026", 41.6, 43, "edge"),
    # 768: o QUINTO ponto na janela de 41,2 a 41,6 — e com ele as duas
    # afirmacoes das rodadas anteriores (766 "reproduz" e 767 "inverte") ficam
    # INDECIDIVEIS: a janela de previsao tem 0,4 s e a granularidade do real e
    # 1 s. Previsao nao ordena o que o instrumento nao resolve.
    ("epomeno-epipedo-s028", 41.5, 43, "edge"),
    # 769: o PISO da banda CAIU. Previsao edge 41,5 (o mesmo valor do s028) e
    # real 42 — residuo +0,5 s, abaixo do 0,9 que vinte e seis pontos
    # sustentavam. E o SEXTO ponto da janela do 768, que agora tem reais
    # 42, 43, 43, 43, 43 e 44 contra previsoes dentro de 0,4 s.
    ("kolejny-poziom-s027", 41.5, 42, "edge"),
    # 770, 22:2x: previsao 41,9 e real 42 — residuo NOMINAL +0,1, que derruba o
    # piso de 0,5 do 769. E o sinal DESTE ponto nao esta estabelecido: com
    # arredondamento para cima, real 42 significa (41; 42], e 41,9 cai dentro.
    ("epomeno-epipedo-s029", 41.9, 42, "edge"),
    # 23:1x: 41,6 -> 43, residuo +1,4. Sinal ESTABELECIDO (43-41,6 > 1,0, logo a
    # janela de arredondamento (42; 43] fica toda acima da previsao — 770).
    ("kolejny-poziom-s028", 41.6, 43, "edge"),
]


def test_o_sinal_sobrevive__cinco_de_cinco_acima():
    assert all(real > prev for _, prev, real, _ in SERIE)


def test_o_limite_de_1_9_s_do_734_CAIU():
    pior = max(real - prev for _, prev, real, _ in SERIE)
    assert pior > 1.9, "se o pior residuo voltar a <=1,9 s, releia o 734 e o 739"
    # 752: o pior deixou de ser o do s034 (2,4) e passou a ser o do s043 (3,7).
    # Este teste trava o valor MEDIDO: se ele mudar outra vez, a banda do
    # `mira.py` tem de mudar no mesmo passo, e nao depois.
    assert abs(pior - 3.7) < 0.05, pior


def test_duas_previsoes_a_um_decimo_dao_reais_diferentes_em_UM_SEGUNDO():
    s33 = dict((p, (prev, real)) for p, prev, real, _ in SERIE)["labtreinamento-s033"]
    s34 = dict((p, (prev, real)) for p, prev, real, _ in SERIE)["labtreinamento-s034"]
    assert abs(s33[0] - s34[0]) <= 0.1, "as previsoes tem de estar a um decimo"
    assert abs(s33[1] - s34[1]) == 1, "e os reais, a um segundo inteiro"


def test_o_OFFSET_tambem_nao_descreve():
    # offset constante exigiria residuo igual nas duas previsoes quase iguais
    r33, r34 = 27 - 25.7, 28 - 25.6
    assert abs(r34 - r33) > 1.0, "offset constante descreveria; ele nao descreve"


def test_o_PERCENTUAL_tambem_nao__e_a_dispersao_cresce_no_curto():
    pct = [(real - prev) / prev for _, prev, real, _ in SERIE]
    curtos = [p for (_, prev, _, _), p in zip(SERIE, pct) if prev < 30]
    longos = [p for (_, prev, _, _), p in zip(SERIE, pct) if prev >= 40]
    assert max(curtos) > max(longos), (
        "os dois pontos curtos trazem os maiores percentuais: 5,1% e 9,4%"
    )


def test_a_mira_do_canal_e_sobre_o_REAL_e_o_instrumento_cobra_o_ESTIMADO():
    """RETRATADO em 14/10 as 03:2x pelo `labtreinamento-s038`, e no lugar.

    A versao anterior deste teste exigia `real > teto` em TODAS as pecas do
    canal. Era verdade com n=3 (27, 27, 28) e o `s038` falsificou: previsao 24,4,
    real **26**, que e o teto exato. Logo o padrao do 744 ("tres de tres fora")
    virou **tres de quatro**, e o teste passou a travar o que segue medido em vez
    do que era conveniente.

    O que NAO muda: o estimado esteve DENTRO da mira nas quatro, logo
    "mira verde" continua nao garantindo "real dentro" (740).
    """
    import ensaio

    piso, teto = ensaio.alvo_short("labtreinamento")
    assert (piso, teto) == (20.0, 26.0)
    do_canal = [(p, prev, real) for p, prev, real, _ in SERIE
                if p.startswith("labtreinamento")]
    assert len(do_canal) >= 4, "a serie do canal encolheu: releia o 744 e o 746"
    for pacote, prev, real in do_canal:
        assert piso <= prev <= teto, f"{pacote}: o estimado tem de estar DENTRO"
    fora = [p for p, _, real in do_canal if real > teto]
    dentro = [p for p, _, real in do_canal if real <= teto]
    assert fora, "se NENHUM real sair fora, o 740 deixou de valer — releia"
    assert dentro, "se TODOS sairem fora, o 746 caiu — releia o padrao"


def test_mirar_o_PISO_e_o_que_pos_o_real_DENTRO():
    """A licao operacional do 746, e ela e aritmetica dos dois pontos vizinhos.

    `s037` previa 25,8 (perto do teto) e deu 28, fora. `s038` previa 24,4 e deu
    26, dentro. Um segundo e meio de previsao decidiu, e a conta do 740 dizia
    isso: para o real caber com folga o edge precisa ficar em <= 23,60.
    """
    d = {p: (prev, real) for p, prev, real, _ in SERIE}
    prev37, real37 = d["labtreinamento-s037"]
    prev38, real38 = d["labtreinamento-s038"]
    assert prev38 < prev37, "a peca de dentro foi a de previsao MENOR"
    assert real38 <= 26.0 < real37, "e o real seguiu a previsao menor"
    assert round(prev37 - prev38, 1) == 1.4


def test_o_provedor_de_todas_foi_MEDIDO_e_nao_inferido():
    # zero avisos `NARRACAO PELO PIPER` na anotacao do job = edge narrou (733)
    assert {prov for *_, prov in SERIE} == {"edge"}
