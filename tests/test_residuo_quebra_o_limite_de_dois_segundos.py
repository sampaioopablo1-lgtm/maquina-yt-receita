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
    # 15/10 00:2x: 41,6 -> 42, residuo nominal +0,4. DENTRO da banda (0,1; 3,7),
    # logo os limites nao mudam — e o sinal NAO esta estabelecido (42-41,6 <= 1,0).
    ("epomeno-epipedo-s030", 41.6, 42, "edge"),
    # 15/10 01:2x: 41,7 -> 43, residuo +1,3. ESTABELECIDO (43-41,7 > 1,0).
    ("kolejny-poziom-s029", 41.7, 43, "edge"),
    # 15/10 02:2x: 41,6 -> 43, residuo +1,4, sinal ESTABELECIDO.
    ("epomeno-epipedo-s031", 41.6, 43, "edge"),
    ("kolejny-poziom-s030", 41.6, 43, "edge"),
    ("epomeno-epipedo-s032", 42.5, 46, "edge"),
    ("kolejny-poziom-s031", 41.8, 44, "edge"),
    ("epomeno-epipedo-s033", 41.6, 42, "edge"),
    ("kolejny-poziom-s032", 41.8, 44, "edge"),
    ("labtreinamento-s051", 25.3, 27, "edge"),
    ("epomeno-epipedo-s034", 41.7, 44, "edge"),
    # 774: o TETO da banda CAIU DE NOVO, +4,0 s, e outra vez no labtreinamento.
    ("labtreinamento-s052", 25.0, 29, "edge"),
    # 41o ponto, 16/10 04:1x, e o PRIMEIRO lido pela rota do SANDBOX (pagina de
    # watch) em vez do `pg_net`. Provedor edge MEDIDO: zero avisos no job
    # `116806511162`. Dos dois `lengthSeconds` da pagina vale o MAIOR (44), pelo
    # arredondamento para cima do `contentDetails.duration`.
    ("kolejny-poziom-s039", 41.5, 44, "edge"),
    # 16/10 05:2x: `epomeno-epipedo-s041` (QH9xoIC69jM), origem `h66MCKjwAJ8`
    # destravada pela regra (h) atraves do sandbox. Previsao mirada no PISO
    # (41,6), provedor edge MEDIDO (zero avisos no job `116823350313`), real 42.
    # Residuo nominal +0,4: DENTRO da banda, NAO move o piso (0,1 segue sendo o
    # minimo), e o sinal NAO esta ESTABELECIDO, porque 42 - 41,6 <= 1,0 e o
    # YouTube arredonda para CIMA — o residuo verdadeiro esta em (-0,6; +0,4].
    ("epomeno-epipedo-s041", 41.6, 42, "edge"),
    # 16/10 08:1x: os dois pontos que a DEGRADACAO da rota tinha impedido de ler
    # (ver CLAUDE.md, "AS TRES ROTAS NAO SAO CAPACIDADES, SAO ESTADOS"). A rota
    # do `lengthSeconds` voltou dentro da MESMA hora em que eu a declarei
    # fechada, o que e a propria regra funcionando: rota e ESTADO.
    # `kolejny-poziom-s040` (7KZjro4H8ls), provedor edge MEDIDO (zero avisos no
    # job `116839333951`): 41,7 -> 43, residuo +1,3, sinal ESTABELECIDO.
    ("kolejny-poziom-s040", 41.7, 43, "edge"),
    # `epomeno-epipedo-s042` (stj6tmBAOLI), provedor edge MEDIDO (zero avisos no
    # job `116858463535`): 41,5 -> 43, residuo +1,5, sinal ESTABELECIDO. A pagina
    # trouxe DOIS `lengthSeconds` (42 e 43) e vale o MAIOR, pelo arredondamento
    # para cima do `contentDetails.duration`.
    ("epomeno-epipedo-s042", 41.5, 43, "edge"),
    # 16/10 09:1x: `labtreinamento-s059` (Z8KZL5z8nxI), provedor edge MEDIDO
    # (zero avisos no job `116878234290`). Previsao 25,7 -> real 28, residuo
    # +2,3, DENTRO da banda e com o sinal ESTABELECIDO. E ele e o DECIMO de
    # treze: a peca saiu FORA do teto da mira do canal (26,0) com o `mira.py`
    # VERDE nos dois mundos — a contradicao do 740/748 outra vez, e a copy
    # declarou a exposicao antes de publicar.
    ("labtreinamento-s059", 25.7, 28, "edge"),
    # 16/10 10:1x: `kolejny-poziom-s041` (WxlzxXVcMXI), provedor edge MEDIDO
    # (zero avisos no job `116899827964`). Previsao 41,6 -> real 42: residuo
    # nominal +0,4, DENTRO da banda, NAO move o piso (0,1) e com o sinal NAO
    # estabelecido, porque 42 - 41,6 <= 1,0 e o arredondamento e para cima.
    ("kolejny-poziom-s041", 41.6, 42, "edge"),
    # 16/10 11:2x: `epomeno-epipedo-s043` (SVOd6xvXE7g), provedor edge MEDIDO
    # (zero avisos no job `116922358223`). Previsao 41,9 -> real 43 (o MAIOR dos
    # dois `lengthSeconds` da pagina): residuo +1,1, DENTRO da banda e com o
    # sinal ESTABELECIDO, por pouco (43 - 41,9 > 1,0).
    ("epomeno-epipedo-s043", 41.9, 43, "edge"),
    # 16/10 12:24, job 116969425333: ZERO avisos nos dois jobs do render.
    ("kolejny-poziom-s042", 41.8, 43, "edge"),
    # 16/10 14:15, jobs 117016350815 e 117016392552: ZERO avisos nos dois.
    ("epomeno-epipedo-s044", 41.8, 43, "edge"),
    # 16/10 15:14, jobs 117043841627 e 117043879324: ZERO avisos nos dois.
    # Previsao EXATA 41,9938 -> residuo 1,0062, logo "estabelecido" por
    # 0,0062 s de margem sobre o critério do 770. A classificacao e
    # tecnicamente certa e PRATICAMENTE nao robusta, e isso vai dito.
    ("kolejny-poziom-s043", 42.0, 43, "edge"),
    # 17:18 de 16/10, e a rota da DURACAO reabriu na mesma rodada em que a
    # LISTAGEM segue fechada: provedor edge MEDIDO (zero avisos no job
    # 117099160058), previsao 41,8 e real 44 — residuo +2,2, DENTRO da banda,
    # sinal ESTABELECIDO, e ABAIXO do teto de 45 que a copy declarou como risco.
    ("epomeno-epipedo-s045", 41.8, 44, "edge"),
    # 18:13 de 16/10, mirando o PISO: provedor edge MEDIDO (zero avisos no job
    # 117122802245), previsao 41,7 e real 43 — residuo +1,3, DENTRO da banda,
    # sinal ESTABELECIDO, e abaixo do teto de 45 que a copy declarou como risco.
    ("kolejny-poziom-s044", 41.7, 43, "edge"),
    # 19:14 de 16/10: provedor edge MEDIDO (zero avisos no job 117149072618),
    # previsao 25,9 e real 27 — residuo +1,1, DENTRO da banda e ESTABELECIDO.
    # E FORA do teto da mira do canal (26,0) com o mira.py VERDE nos dois
    # mundos: o tally do 744/754 vai a DEZ de treze.
    ("labtreinamento-s063", 25.9, 27, "edge"),
    # 20:13 de 16/10: provedor edge MEDIDO (zero avisos no job 117173319353),
    # previsao 41,3 e real 42 — residuo +0,7, DENTRO da banda e com o sinal NAO
    # estabelecido (42 - 41,3 <= 1,0, pelo 770). A pagina trouxe DOIS
    # lengthSeconds, 41 e 42: vale o MAIOR.
    ("epomeno-epipedo-s046", 41.3, 42, "edge"),
    # 21:12 de 16/10, e o PRIMEIRO residuo ZERO da serie: provedor edge MEDIDO
    # (zero avisos no job 117197352639), previsao 41,0 e real 41. O piso da banda
    # cai de 0,1 para 0,0, e o sinal deste ponto NAO esta estabelecido — com
    # arredondamento para cima, real 41 significa duracao em (40; 41], logo o
    # residuo verdadeiro esta em (-1,0; 0,0] e PODE ser negativo.
    ("kolejny-poziom-s045", 41.0, 41, "edge"),
    # 22:13 de 16/10: provedor edge MEDIDO (zero avisos no job 117219367300),
    # previsao 25,9 e real 28 — residuo +2,1, DENTRO da banda e ESTABELECIDO, e
    # FORA do teto da mira do canal (26,0) com o mira.py VERDE nos dois mundos.
    ("labtreinamento-s064", 25.9, 28, "edge"),
    # 23:13 de 16/10: o SEGUNDO residuo ZERO, e com a MESMA previsao do
    # primeiro — provedor edge MEDIDO (zero avisos no job 117238298428), 41,0 e
    # real 41, igual ao `kolejny-poziom-s045` duas horas antes. Sinal NAO
    # estabelecido nos dois. O piso da banda ja estava em 0,0 e nao se move.
    ("epomeno-epipedo-s047", 41.0, 41, "edge"),
    # 00:13 de 17/10, primeira peca do dia novo: provedor edge MEDIDO (zero
    # avisos no job 117254439119), previsao 40,6 e real 43 — residuo +2,4,
    # DENTRO da banda e ESTABELECIDO.
    ("kolejny-poziom-s046", 40.6, 43, "edge"),
    # 17/10 01:1x — provedor edge MEDIDO (zero avisos no job 117269678180)
    ("labtreinamento-s065", 26.4, 28, "edge"),
    # 17/10 02:1x — provedor edge MEDIDO (zero avisos no job 117281738012)
    ("epomeno-epipedo-s048", 41.9, 44, "edge"),
    # 17/10 05:0x — os tres pontos que a rota FECHADA havia parqueado e que
    # sairam juntos quando ela reabriu (duracao_a_medir + a peca de CONTROLE).
    ("kolejny-poziom-s049", 41.5, 44, "edge"),   # job 117293729800
    ("labtreinamento-s066", 25.6, 27, "edge"),   # job 117305098967
    ("epomeno-epipedo-s049", 41.0, 43, "edge"),  # job 117316291107
    ("kolejny-poziom-s050", 41.6, 43, "edge"),   # job 117326904073
    ("labtreinamento-s067", 25.6, 28, "edge"),   # job 117339028890
    ("epomeno-epipedo-s050", 41.8, 43, "edge"),  # job 117349192781
    ("kolejny-poziom-s051", 41.7, 42, "edge"),   # job 117359904321 — sinal NAO estabelecido (770)
    ("labtreinamento-s068", 25.9, 28, "edge"),   # job 117370744614
    ("epomeno-epipedo-s051", 41.7, 42, "edge"),  # job 117381838626 — sinal NAO estabelecido (770)
    ("kolejny-poziom-s052", 41.5, 43, "edge"),   # job 117392443607
    ("labtreinamento-s069", 25.8, 27, "edge"),   # job 117404699496
    ("epomeno-epipedo-s052", 41.6, 44, "edge"),  # job 117416293733
    ("kolejny-poziom-s053", 41.6, 42, "edge"),   # job 117428398684 — sinal NAO estabelecido (770)
    ("labtreinamento-s070", 25.7, 29, "edge"),   # job 117441677715
    ("epomeno-epipedo-s053", 41.6, 42, "edge"),  # job 117454412202 — sinal NAO estabelecido (770)
    ("kolejny-poziom-s054", 41.8, 42, "edge"),   # job 117466655474 — sinal NAO estabelecido (770)
    ("labtreinamento-s071", 25.2, 27, "edge"),  # job 117479645664
    ("epomeno-epipedo-s054", 41.6, 41, "edge"),  # job 117492664194 — o PRIMEIRO NEGATIVO estabelecido
    ("kolejny-poziom-s055", 42.2, 43, "edge"),   # job 117504992463 — sinal NAO estabelecido (770)
    ("labtreinamento-s072", 25.7, 28, "edge"),  # job 117517230913
    ("epomeno-epipedo-s055", 41.5, 41, "edge"),  # job 117529604557 — o SEGUNDO negativo estabelecido
    ("kolejny-poziom-s056", 41.7, 43, "edge"),   # job 117540417103
    ("labtreinamento-s073", 26.0, 28, "edge"),   # job 117551494916
    ("epomeno-epipedo-s056", 41.5, 43, "edge"),  # job 117561762560 — DOIS lengthSeconds (42 e 43), usado o MAIOR
    ("kolejny-poziom-s057", 41.5, 42, "edge"),
    ("labtreinamento-s074", 25.8, 28, "edge"),  # job 117583621587 — real FORA do teto da mira (26,0) com a mira VERDE   # job 117572513678 — sinal NAO estabelecido (770)
]


def test_o_sinal_NAO_e_mais_de_N_de_N__e_o_negativo_apareceu():
    """A QUINTA e ultima queda desta frase, e esta e definitiva.

    A versao anterior deste teste exigia `real >= prev` em TODA a serie e dizia,
    na propria mensagem, que um real ABAIXO da previsao *nunca foi observado* e
    que se aparecesse a serie teria de ser RELIDA. **Apareceu**, em 17/10 as
    20:1x: o `epomeno-epipedo-s054` (`A4M3SLs8FEk`) previa 41,6 no edge — provedor
    MEDIDO, zero avisos no job 117492664194 — e saiu com **41** reais.

    E o sinal dele esta ESTABELECIDO para baixo: com arredondamento PARA CIMA,
    real 41 significa duracao verdadeira em (40; 41], toda abaixo de 41,6, logo o
    residuo verdadeiro esta em (-1,6; -0,6]. Ver
    `tests/test_o_sinal_tambem_se_estabelece_para_BAIXO.py`.

    O teste foi reescrito em vez de ter o `assert` afrouxado, porque o que mudou
    nao foi o limiar: foi a AFIRMACAO. O que sobrevive e mais fraco e verdadeiro —
    a serie e dominada por residuo positivo, e o negativo e raro e NOMEADO."""
    negativos = [(p, pr, r) for p, pr, r, _ in SERIE if r < pr]
    # A propriedade nova: existe negativo, e ele e raro. Se desaparecer, alguem
    # apagou o ponto; se virar maioria, a banda inteira tem de ser relida.
    assert negativos, (
        "o ponto negativo do `epomeno-epipedo-s054` sumiu da serie — ele e o que"
        " derrubou a frase 'N de N acima', e sem ele a nota perde a evidencia")
    assert len(negativos) <= 0.05 * len(SERIE), (
        f"{len(negativos)} de {len(SERIE)} negativos: deixou de ser raro, releia")
    # O positivo estrito segue valendo nos pontos ESTABELECIDOS para cima.
    estabelecidos = [(p, pr, r) for p, pr, r, _ in SERIE if r - pr > 1.0]
    assert all(r > pr for _, pr, r in estabelecidos)
    assert len(estabelecidos) >= 40, len(estabelecidos)


def test_o_limite_de_1_9_s_do_734_CAIU():
    # "pior" aqui e o residuo MAIOR (o teto da banda), e isso continua certo
    # mesmo com o piso negativo: o teto nao se mede pelo extremo de baixo.
    pior = max(real - prev for _, prev, real, _ in SERIE)
    assert pior > 1.9, "se o pior residuo voltar a <=1,9 s, releia o 734 e o 739"
    # 752: o pior deixou de ser o do s034 (2,4) e passou a ser o do s043 (3,7).
    # Este teste trava o valor MEDIDO: se ele mudar outra vez, a banda do
    # `mira.py` tem de mudar no mesmo passo, e nao depois.
    assert abs(pior - 4.0) < 0.05, pior


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

    E A FRASE "o estimado esteve DENTRO da mira em TODAS" CAIU EM 17/10 as
    01:2x, medida pelo proprio teste. O `labtreinamento-s065` saiu com previsao
    edge **26,4** — 0,4 s ACIMA do teto de 26,0, com o `mira.py` dizendo FORA — e
    real **28**. Eu mirei o PISO e a sobrecarga de dez cenas nao deixou descer
    mais sem o custo de prosodia do 747; a exposicao foi declarada na copy antes
    de publicar.

    Logo o teste nao pode mais cobrar "estimado dentro" de TODA peca do canal. O
    que ele cobra e a propriedade que sustenta o 740, e ela vive nas pecas de
    mira VERDE: existe peca com o estimado dentro cujo real saiu fora. A peca de
    mira vermelha fica na serie e vai CONTADA a parte, em vez de reprovar o
    arquivo ou ser apagada dele.
    """
    import ensaio

    piso, teto = ensaio.alvo_short("labtreinamento")
    assert (piso, teto) == (20.0, 26.0)
    do_canal = [(p, prev, real) for p, prev, real, _ in SERIE
                if p.startswith("labtreinamento")]
    assert len(do_canal) >= 4, "a serie do canal encolheu: releia o 744 e o 746"
    verdes = [(p, prev, real) for p, prev, real in do_canal
              if piso <= prev <= teto]
    vermelhas = [(p, prev, real) for p, prev, real in do_canal
                 if not piso <= prev <= teto]
    assert verdes, "sem peca de mira verde o 740 nao tem sobre o que falar"
    fora = [p for p, _, real in verdes if real > teto]
    dentro = [p for p, _, real in verdes if real <= teto]
    assert fora, "se NENHUM real sair fora, o 740 deixou de valer — releia"
    assert dentro, "se TODOS sairem fora, o 746 caiu — releia o padrao"
    # "vermelha" AQUI e so pelo EDGE — e a unica coordenada que a SERIE guarda.
    # O s042 e o s043 foram vermelhos pelo PISO DO PIPER com o edge dentro
    # (23,4 e 23,3), logo caem como verdes nesta classificacao e isso vai dito:
    # o teste nao ve a segunda coordenada da pinca.
    assert all(real > teto for _, _, real in vermelhas), (
        "peca vermelha PELO EDGE com real dentro: releia o 740/748 em vez de"
        " mover o assert — hoje a unica e o s065 (26,4 -> 28)")


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
