#!/usr/bin/env python3
"""A peça cabe no PORTÃO e erra a MIRA DO CANAL — dizer isso antes do render.

POR QUE ISTO EXISTE, medido em 13/10/2026 às 06:1x. Escrevendo o
`labtreinamento-s032` eu produzi uma spec de **27,8 s reais previstos** no Piper.
O portão `duracao` aprovou, e com razão: ele cobra 18 a 45 s, que é a faixa da
FROTA. Mas o `labtreinamento` tem `ALVO_POR_CANAL = (20,0 a 26,0)` desde 09/10,
medido (698) — e 27,8 está fora dela. **Portão verde não dispensa a mira.**

Eu peguei à mão nesta rodada. Na próxima eu não pegaria, e é por isso que a
conta sai da minha cabeça.

**POR QUE ISTO NÃO É UM AVISO DENTRO DO `prontidao`, e a razão é medida:** das
specs do `labtreinamento` com voz modelada, **44 ficam fora da mira no mundo
`edge` e 28 no `piper`** — quase todas peças históricas, escritas antes de o
override existir. Um aviso de portão que dispara 44 vezes é um aviso que as
pessoas aprendem a ignorar, e aí ele deixa de avisar o caso que importa. Então
isto é um RELATO que se roda na spec que está sendo escrita, como o
`concentracao.py`.

**E não é limiar novo:** os números são `ensaio.ALVO_POR_CANAL`, que é medição do
próprio canal, e `ensaio.duracao_real_prevista`, que é o fator do Piper medido no
711/714. Canal sem override não tem mira própria e o relato diz isso em vez de
inventar uma.

**E ESTE MÓDULO TINHA UM BURACO MEDIDO EM 13/10 ÀS 22:2x — aprendizado 739.** A
mira do `labtreinamento` é sobre a duração **REAL**, e o que eu confiro aqui é a
**PREVISÃO**. As duas peças do canal narradas pelo edge (`s033` e `s034`) passaram
por esta conferência com a previsão DENTRO e saíram em **27 e 28 s reais** — fora
da mira. O real ficou acima da previsão do provedor que de fato narrou em **25 dos 28**
pontos em que o instrumento RESOLVE o sinal — nos outros três a previsão cai
DENTRO da janela de arredondamento do real, e ali o sinal não está estabelecido
(770). A banda vive em `RESIDUO_OBSERVADO`, e o NUMERO NAO SE REPETE AQUI —
esta linha trazia "0,9 a 3,7" e, quando o 770 baixou o piso para 0,1, ela ficou
atrasada e ninguem viu: o teste do 753 cobra a MENSAGEM do relato e nao o
docstring. O teto ja foi ampliado DUAS vezes por medicao (752, e o 774 em 15/10
as 10:2x) e o piso baixou duas (769, 770); por isso leia a constante.

Então `faixa_real` acrescenta essa banda ao relato: previsão de 25,6 põe o real
entre 26,5 e 28,0, e o relato DIZ que isso passa do teto da mira. **Ele informa e
NÃO reprova**, e a razão é a amostra: n pequeno, e a banda varia sem lei
estável (duas previsões a um décimo deram reais a um segundo de distância), e
reprovar por uma banda assim seria inventar portão com cinco pontos. Quem decide
encurtar é quem escreve a peça, com o número na frente.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import ensaio  # noqa: E402

PROVEDORES = ("edge", "piper")

# Resíduo OBSERVADO entre a previsão do provedor que de fato narrou (medido pela
# anotação do job, 733) e a duração REAL. Cinco pontos, 13/10: +0,9 / +1,1 / +1,9
# / +1,3 / +2,4 s. Todos POSITIVOS. Isto NÃO é limiar — nada reprova por causa
# dele; ele entra no relato para que quem escreve veja onde o real deve cair.
RESIDUO_OBSERVADO = (-1.2, 4.0)
# 17/10 20:1x: o PISO DA BANDA FICOU NEGATIVO, e e a PRIMEIRA vez em 78 pontos.
# O `epomeno-epipedo-s054` (`A4M3SLs8FEk`) previa 41,6 no edge (provedor MEDIDO:
# zero avisos no job 117492664194) e saiu com **41** reais — residuo -0,6.
#
# E o sinal dele ESTA estabelecido, ao contrario do que o meu proprio criterio
# dizia: o YouTube arredonda PARA CIMA, logo real 41 significa duracao verdadeira
# em (40; 41], e a previsao de 41,6 esta ACIMA de todo esse intervalo. O residuo
# verdadeiro vive em (-1,6; -0,6] e e ESTRITAMENTE negativo.
#
# O criterio do 770 era de UM LADO SO (`real - previsao > 1,0`) e por isso
# devolvia "nao estabelecido" aqui — conserto em `duracao_a_medir._sinal`, que
# agora estabelece os dois lados. **E isto derruba a frase "N de N acima" que eu
# venho escrevendo desde o 734**: ela nao vale mais, e o que sobrevive e que a
# grande maioria e positiva.
# 774, 15/10 10:2x: o TETO da banda CAIU DE NOVO, e e a SEGUNDA ampliacao. O
# `labtreinamento-s052` previa 25,0 no edge (provedor MEDIDO: zero avisos
# `NARRACAO PELO PIPER` no job 116368125417) e saiu com 29 REAIS — residuo
# +4,0 s, contra o maximo de 3,7 que trinta e nove pontos sustentavam. A largura
# foi de 3,6 para 3,9 s, contra 1 s de granularidade do real: a banda informa
# cada vez MENOS, e isso vai dito em vez de escondido. E o teto veio OUTRA VEZ do
# `labtreinamento`, o canal dominante da serie.
# 752, 14/10 08:2x: o TETO da banda CAIU, e por medicao. O `labtreinamento-s043`
# previa 23,3 no edge (provedor MEDIDO pela anotacao) e saiu com 27 REAIS —
# residuo +3,7 s, contra o maximo de 2,4 que treze pontos sustentavam. Isto NAO
# e limiar novo: e a faixa OBSERVADA, e ela so se mexe quando a observacao sai
# dela. O piso de 0,9 nao mudou NAQUELE dia, e a largura passou de 1,5 para
# 2,8 s — ou seja,
# a banda agora cobre quase o dobro, o que a torna MENOS util e isso vai dito em
# vez de escondido.
# 770, 14/10 22:2x: o piso caiu outra vez, de 0,5 para 0,1 — e esta queda vale
# mais pelo que ela REVELA do que pelo numero. O `epomeno-epipedo-s029` previa
# 41,9 no edge (provedor MEDIDO: zero avisos no job 116135075389) e saiu com
# 42 s. O YouTube ARREDONDA PARA CIMA, logo real 42 significa duracao verdadeira
# em (41; 42], e a previsao de 41,9 cai DENTRO desse intervalo: o residuo
# verdadeiro esta em (-0,9; +0,1], e o SINAL DELE NAO ESTA ESTABELECIDO.
#
# Conferida a serie inteira por esse critério, o sinal so esta estabelecido
# quando `real - previsao > 1,0` (a janela de arredondamento fica toda acima da
# previsao). Tres dos 28 pontos NAO passam: o `epomeno-epipedo-s024` (+0,9, que
# era o PISO original do 734), o `kolejny-poziom-s027` (+0,5, o piso do 769) e
# este (+0,1). Logo "N de N acima" sempre foi 25 de 28 estabelecidos, e os tres
# pontos que definiram o piso da banda ao longo do tempo sao exatamente os tres
# cujo sinal o instrumento nao resolve. Entre os 25 estabelecidos o piso nominal
# e 1,1.
#
# O piso daqui segue sendo o MENOR residuo NOMINAL observado (0,1), porque e ele
# que a `faixa_real` precisa para nao prometer o que nao se mediu — e a largura
# foi de 3,2 para 3,6 s, o que torna a banda AINDA menos util como previsao.
# 14/10 23:1x: o `kolejny-poziom-s028` (41,6 -> 43, +1,4) e o 29o ponto e cai
# DENTRO da banda, logo os LIMITES nao mudam — e o sinal dele esta ESTABELECIDO
# pelo critério do 770, levando os estabelecidos a 26 de 29.
# 15/10 00:2x: o `epomeno-epipedo-s030` (41,6 -> 42, +0,4) e o 30o ponto. Cai
# DENTRO da banda, logo os limites nao mudam — e o SINAL dele NAO esta
# estabelecido pelo critério do 770, levando os estabelecidos a 26 de 30. E ele
# REFINA o 770: ser nao-estabelecido NAO implica ter movido o piso (este nao
# moveu), so a volta vale — piso baixo e necessariamente nao-estabelecido.
# 15/10 01:2x: o `kolejny-poziom-s029` (41,7 -> 43, +1,3) e o 31o ponto, cai
# DENTRO da banda e tem o sinal ESTABELECIDO — 27 de 31.
# 15/10 02:2x: o `epomeno-epipedo-s031` (41,6 -> 43, +1,4) e o 32o ponto, dentro
# da banda e com o sinal ESTABELECIDO — 28 de 32.
# 16/10 04:1x: o `kolejny-poziom-s039` (`RT_qRi_S1Mw`) e o 41o ponto. Previsao
# edge 41,5, provedor **edge** MEDIDO (zero avisos `NARRACAO PELO PIPER` no job
# `116806511162`), real **44** lido no ar: residuo **+2,5**, DENTRO da banda e
# com o sinal ESTABELECIDO (44 - 41,5 > 1,0) — 36 de 41. Os LIMITES nao mudaram.
# E ele e o PRIMEIRO ponto lido pela rota do SANDBOX em vez do `pg_net`: a
# pagina de watch da `lengthSeconds`, e dos dois valores dela vale o MAIOR,
# porque a banda foi construida sobre `contentDetails.duration`, que arredonda
# para cima. As outras dezessete duracoes parqueadas NAO entraram, porque o
# provedor delas nao esta medido e comparar contra o mundo `edge` sem contar os
# avisos e o erro que o 733 nomeia.
# 42o ponto, 16/10 05:2x: `epomeno-epipedo-s041` (edge 41,6 -> real 42,
# provedor MEDIDO, zero avisos no job `116823350313`). Residuo nominal +0,4,
# DENTRO da banda, e o sinal NAO esta ESTABELECIDO (42 - 41,6 <= 1,0, e o
# arredondamento e para cima) — 36 de 42 estabelecidos. Os LIMITES nao
# mudaram: 0,4 nao e menor que o piso de 0,1.
RESIDUO_N = 128  # 741 acrescentou o s035 (24,8 -> 27, +2,2): DENTRO da banda,
#                 logo os LIMITES nao mudaram — so o numero de pontos que a sustenta.
#                 14/10 06:2x: o s041 (edge 24,6 -> real 27) deu +2,4 — EMPATADO
#                 com o teto da banda, o decimo segundo ponto e o segundo a tocar
#                 o limite superior. Os LIMITES seguem intocados porque 2,4 ja e
#                 o maximo; o proximo ponto acima dele QUEBRA a banda, e e isso
#                 que o teste do 739 existe para obrigar a reler.


def faixa_real(estimado: float) -> tuple[float, float]:
    """Onde o REAL deve cair, dada uma previsão, pela banda OBSERVADA do 739."""
    lo, hi = RESIDUO_OBSERVADO
    return (round(estimado + lo, 1), round(estimado + hi, 1))


def previsoes(spec: dict) -> dict[str, float]:
    """Duração REAL prevista em cada mundo de provedor. Vazio sem short/voz."""
    short, voz = spec.get("short") or [], spec.get("voz", "")
    if not short or voz not in ensaio.MODELO_VOZ:
        return {}
    return {p: round(ensaio.duracao_real_prevista(short, voz, p), 1)
            for p in PROVEDORES}


def canal_da_spec(spec: dict) -> str:
    """O CANAL de uma spec. Delega ao `fabrica/canal.py`, que e o dono UNICO.

    MEDIDO em 19/10 as 05:2x. O `confere` lia `spec["slug"]` como se fosse o
    canal, e o `tally_fora_da_mira` derivava com `pacote.rsplit("-s", 1)[0]`.
    Enquanto a spec de short solto trazia `slug: "labtreinamento"` as duas
    concordavam por acidente; quando o `slug` passou a ser o PACOTE
    (`labtreinamento-s077` em diante), o `confere` deixou de achar o canal no
    `ALVO_POR_CANAL` e passou a devolver `tem_mira: False` — isto e, **o
    instrumento parou de conferir a mira e disse que nao havia mira a conferir**.
    SEIS pecas publicadas (`s077` a `s082`) sairam assim, e eu reportei
    "mira verde nos dois mundos" nas seis fazendo a conta de cabeca, que e
    exatamente o item 3 da §10.

    E eram TRES, nao dois: o `registro_videos` fazia o mesmo para a coluna
    `canal` de `videos`, e DEZENOVE linhas parqueadas sairam com o pacote no
    lugar do canal. E a assinatura e a do `assert 20 <= ds <= 60` e a da legenda
    congelada: DOIS DONOS DA MESMA REGRA, UM ATUALIZADO. A falha e no sentido
    PERMISSIVO — ela nao reprova nada, so para de avisar. **O motivo pelo qual
    esta funcao nao faz a conta aqui e esse mesmo:** o dono mora em `canal.py`.
    """
    import canal as _canal
    return _canal.da_spec(spec)


def confere(spec: dict) -> dict:
    """A peça cai na mira MEDIDA do canal, nos dois mundos de provedor?

    `tem_mira` é False quando o canal não tem override — e aí não há o que
    conferir, porque a mira da frota é o que o portão já cobra.
    """
    canal = canal_da_spec(spec)
    prev = previsoes(spec)
    if canal not in ensaio.ALVO_POR_CANAL:
        return {"canal": canal, "tem_mira": False, "previsoes": prev,
                "fora": [], "motivo": f"canal {canal!r} nao tem ALVO_POR_CANAL "
                "medido — a mira da frota e a que o portao `duracao` ja cobra"}
    lo, hi = ensaio.ALVO_POR_CANAL[canal]
    fora = [p for p, d in prev.items() if not (lo <= d <= hi)]
    return {"canal": canal, "tem_mira": True, "mira": (lo, hi),
            "previsoes": prev, "fora": fora,
            "motivo": None if not fora else (
                f"{', '.join(fora)} fora da mira medida {lo} a {hi} s. O portao "
                "`duracao` cobra a faixa da FROTA, que e mais larga, e NAO "
                "reprova isto — portao verde nao dispensa a mira do canal "
                "(698).")}


def chars_no_alvo(voz: str, n_cenas: int, alvo_s: float,
                  provedor: str = "edge") -> int:
    """O nome PUBLICO do inversor, para quem precisa dele de fora.

    Ele existe porque o `contagem_de_cenas` passou a perguntar quantos
    caracteres a peca precisa para encostar no PISO da faixa — e a alternativa
    era refazer a inversao la, que seria o segundo dono da conta (a assinatura
    que congelou a legenda). Nenhuma logica mora aqui: isto delega.

    **E ELE NAO RESPONDE "MIRE O PISO DA FAIXA" — medido em 20/10 as 16:4x.**
    O `_chars_para_o_real` desce ate a previsao caber `<= alvo_s`, logo com o
    PISO no lugar do alvo ele devolve o maior numero que fica **ABAIXO** dele.
    Varridos os 54 pares (canal, n) da frota com resposta para o piso, a
    previsao da resposta cai FORA da faixa em **54 de 54**, e nos 54 pelo lado
    de BAIXO: na voz grega com doze cenas ele devolve 36, que preve **41,39**
    contra um piso de 41,5. **Logo a regra de redacao do 772 — "mire o PISO" —
    era inexecutavel por este caminho**, e eu a vinha cumprindo somando de
    cabeca, que e o item 3 da §10.

    O docstring do `_chars_para_o_real` guardava o outro lado desta mesma
    armadilha (*"dizer 'mirei o piso' e entregar peca acima do TOPO"*) e nao
    este — a assinatura do 771: criterio escrito so no lado em que eu estava
    olhando. Quem responde "mire o piso" e o `janela_do_mundo`, cujo PRIMEIRO
    elemento e a menor media que fica DENTRO da faixa.
    """
    return _chars_para_o_real(voz, n_cenas, alvo_s, provedor)


def _chars_para_o_real(voz: str, n_cenas: int, alvo_s: float,
                       provedor: str = "edge") -> int:
    """Caracteres por cena para a PREVISAO REAL caber em `alvo_s`.

    POR QUE NAO E O `chars_por_cena` DIRETO (19/10, 15:2x): aquele mira a
    `duracao_estimada`, e a mira e o portao cobram a `duracao_real_prevista`.
    Medido no `epomeno-epipedo-s068`: 53 caracteres por cena dao estimativa
    41,44 e previsao real 43,38 — 1,94 s de diferenca, que e o fator do
    provedor. Dizer "mirei o piso" e entregar peca acima do TOPO e o 753 em
    forma de unidade: duas grandezas com o mesmo nome dentro do mesmo relato.

    A conta NAO se refaz aqui: isto INVERTE numericamente a funcao que ja e
    dona dela. O chute inicial sai do `chars_por_cena` (que erra para cima, por
    medida) e desce de um em um ate a previsao caber — no maximo algumas
    iteracoes, porque a distancia e o fator do provedor.

    O mundo e o `edge` por MEDIcao: ele e o maior dos dois (43,38 contra 38,44
    na mesma peca), logo e ele que encosta no teto do portao e no topo da mira.
    """
    if n_cenas < 1:
        return 0
    chute = ensaio.chars_por_cena(voz, n_cenas, alvo_s)
    for c in range(chute, 0, -1):
        cenas = [{"nar": "x" * c} for _ in range(n_cenas)]
        if ensaio.duracao_real_prevista(cenas, voz, provedor) <= alvo_s:
            return c
    return 0


MAX_CHARS_VARRIDOS = 240   # teto do varrimento de media por cena, herdado do
                           # `janela_dos_dois_mundos` de 19/10. Ele NAO e um
                           # limite de redacao: e onde o laco para. Com poucas
                           # cenas a janela ENCOSTA nele — medido em 20/10 as
                           # 16:5x, no polones com TRES cenas, cuja janela sai
                           # (233, 240) quando 241 e 242 ainda cabem. Logo o
                           # MAIOR da janela e a borda do laco, nao a da faixa,
                           # quando ele chega aqui. Quem precisa da fronteira de
                           # cima confere se o maior e menor que isto.


def _janela(voz: str, n_cenas: int, faixa: tuple,
            provedores: tuple) -> tuple[int, int] | None:
    """UM dono do varrimento: as medias em que TODOS os `provedores` cabem.

    Nasceu em 20/10 as 16:4x, quando o `janela_do_mundo` precisou do MESMO
    laco que o `janela_dos_dois_mundos` ja tinha. Escrever o laco duas vezes
    seria o segundo dono do varrimento — a assinatura que congelou a legenda,
    parou a mira de conferir por seis pecas e pos job inventado na serie.

    Ele varre em vez de inverter de proposito: inverter devolve UM ponto e
    arredonda para um lado, e foi assim que a resposta do PISO passou a cair
    FORA da faixa em 54 de 54 pares. Varrer responde com o CONJUNTO que de
    fato cabe, e ai o piso executavel e o primeiro elemento dele.
    """
    if n_cenas < 1 or not provedores:
        return None
    piso, teto = float(faixa[0]), float(faixa[1])
    ok = []
    for c in range(1, MAX_CHARS_VARRIDOS + 1):
        cenas = [{"nar": "x" * c} for _ in range(n_cenas)]
        ds = [ensaio.duracao_real_prevista(cenas, voz, p) for p in provedores]
        if min(ds) > teto:
            break
        if all(piso <= d <= teto for d in ds):
            ok.append(c)
    return (ok[0], ok[-1]) if ok else None


def janela_do_mundo(voz: str, n_cenas: int, faixa: tuple,
                    provedor: str = "edge") -> tuple[int, int] | None:
    """Caracteres por cena em que UM mundo de provedor cabe na faixa.

    POR QUE EXISTE (20/10, 16:4x): a regra de redacao do 772 manda **mirar o
    PISO**, e o inversor publico (`chars_no_alvo`) responde o piso com um valor
    cuja previsao cai ABAIXO dele — 54 de 54 pares medidos. O primeiro elemento
    desta janela e a resposta executavel: a MENOR media que fica DENTRO.

    **Ele nao substitui o `janela_dos_dois_mundos`, e isso vai dito:** a mira e
    o portao cobram os DOIS mundos (730/733), logo quem usa este sabe que esta
    declarando exposicao no outro — e nos dois canais da pinca (740/748) e a
    unica coisa que se pode fazer, porque lá a janela dos dois e sempre vazia.
    """
    return _janela(voz, n_cenas, faixa, (provedor,))


def janela_dos_dois_mundos(voz: str, n_cenas: int,
                           faixa: tuple) -> tuple[int, int] | None:
    """Caracteres por cena em que os DOIS mundos de provedor cabem na faixa.

    POR QUE EXISTE (19/10, 17:2x, e e o QUARTO defeito do mesmo instrumento):
    o `_chars_para_o_real` mira o `edge`, porque e ele que encosta no teto. Mas
    **a mira e o portao cobram os DOIS mundos** desde 13/10 as 02:1x — o
    provedor se decide no runner, por cena e por run (730/733). Logo o orcamento
    respondia uma pergunta e a conferencia fazia outra.

    MEDIDO no `labtreinamento-s086`: para nove cenas o orcamento do MEIO da
    mira (23,0) deu **25** caracteres, e com 25 a peca sai em edge 22,6 e o
    **piper a 18 s e meio — abaixo do piso de 20,0**. Isto e, a mira REPROVA a
    resposta que o orcamento acabou de dar. A janela que satisfaz os dois e
    **28 a 30**, e ela mora no TOPO da faixa e nao no meio: e a pinca do
    740/748 aparecendo DENTRO do instrumento, porque o piso do piper e uma
    RAZAO e o teto do edge e outro ponto da mesma faixa.

    Devolve None quando nenhum orcamento satisfaz os dois — e ai a pinca esta
    FECHADA para essa contagem de cenas, que e informacao e nao erro. Nao
    filtra nem escolhe: NOMEIA, como o `origens_sem_uso` nomeia em vez de
    esconder.
    """
    return _janela(voz, n_cenas, faixa, ("edge", "piper"))


CHARS_MINIMOS_OBSERVADOS = 21   # media por cena do `labtreinamento-s081`, a
                                # MENOR do disco (a peca de 5 s, 2 cenas).
                                # Nao e limiar escolhido: e o piso que a
                                # producao real ja usou e que foi medido como
                                # correto. Quem o reconfere e o teste, varrendo
                                # o disco — numero medido que ninguem reconfere
                                # envelhece calado (753).


def teto_de_cenas(voz: str, faixa: tuple,
                  chars_minimos: int = CHARS_MINIMOS_OBSERVADOS) -> dict:
    """Quantas cenas AINDA cabem na faixa, nesta voz, com texto legivel.

    POR QUE EXISTE (20/10, 00:3x). O `CLAUDE.md` dizia, desde 11/10, que *"doze
    cenas estourariam o teto de 43,1 so em silencio, entao o teto real no alvo
    atual e onze"*. **Medido, doze cenas custam 20,06 s de silencio na voz
    grega** — menos da METADE do teto — e o numero de 11/10 foi generalizado de
    UMA voz e de um alvo que mudou depois. Eu venho limitando o esqueleto a onze
    cenas por causa dele, e por isso a frota nao tinha nenhuma peca de doze.

    **A sobrecarga por cena e `P + 0,300` e P e por VOZ** (nota de 11/10), logo o
    teto nao pode ser um numero da frota: ele e 15 na voz grega, 14 na polonesa
    e maior no pt-BR, para a faixa da frota.

    O teto SO faz sentido com um piso de caracteres, senao a resposta e "cenas
    de um caractere", que nao e peca. O piso e OBSERVADO
    (`CHARS_MINIMOS_OBSERVADOS`), nao escolhido.

    Devolve `teto`, a `janela` de caracteres nesse teto, e o `silencio` — o
    quanto a contagem custa sem texto nenhum, que e a conta que o numero de
    11/10 errou.
    """
    piso, teto_s = float(faixa[0]), float(faixa[1])
    maior, janela = None, None
    for n in range(1, 61):
        so_silencio = ensaio.duracao_real_prevista(
            [{"nar": "x"} for _ in range(n)], voz, "edge")
        if so_silencio > teto_s:
            break
        ok = [c for c in range(int(chars_minimos), 241)
              if piso <= ensaio.duracao_real_prevista(
                  [{"nar": "x" * c} for _ in range(n)], voz, "edge") <= teto_s]
        if ok:
            maior, janela = n, (ok[0], ok[-1])
    return {"voz": voz, "faixa": (piso, teto_s), "chars_minimos": int(chars_minimos),
            "teto": maior, "janela": janela,
            "silencio_no_teto": None if maior is None else round(
                ensaio.duracao_real_prevista(
                    [{"nar": "x"} for _ in range(maior)], voz, "edge"), 2)}


def frases_por_cena(spec: dict) -> list:
    """Quantas FRASES cada cena do short tem — contadas por quem ja sabe.

    A contagem e DELEGADA a `narracao.frases`, que e o dono dela e sabe que o
    fim de frase do hindi e do grego nao e o ponto do portugues. Reescrever o
    `split` aqui criaria o segundo dono, que e a assinatura que congelou a
    legenda.
    """
    import narracao
    idi = (spec.get("voz") or "").split("-")[0] or None
    return [len(narracao.frases(c.get("nar") or "", idi))
            for c in (spec.get("short") or [])]


def custo_das_frases_extra(spec: dict) -> dict | None:
    """Quanto a peca paga por ter cena de MAIS DE UMA frase.

    **POR QUE EXISTE (20/10, 19:4x): o orcamento fala em caracteres POR CENA e a
    conta e por FRASE.** O `ensaio.chars_por_cena` DIZ isso no docstring desde
    11/10 — *"assume UMA FRASE por cena ... cena com duas frases paga 2P"* — e a
    ressalva **nunca atravessava** para o relato, que e onde o numero e LIDO.
    O `_janela`, o `chars_no_alvo` e a tabela do `contagem_de_cenas` montam
    cenas de UMA frase (`"x" * c`), logo a resposta deles vale para esse caso e
    para nenhum outro.

    **Pego escrevendo o `epomeno-epipedo-s078`, e ele quase saiu FORA da faixa
    com a media de caracteres CERTA:** a primeira versao punha duas frases na
    cena do CTA, e a previsao foi de 42,15 para **43,18** — 1,27 s a mais, com o
    mesmo numero de caracteres por cena. Logo a media nao determina a duracao.

    **O TAMANHO VAI MEDIDO, e e maior do que o do defeito que o produziu:** das
    384 specs de short do disco, **216** tem ao menos uma cena de duas ou mais
    frases (**631** cenas de 3.013), e para essas a diferenca entre a duracao
    real e a que o orcamento supoe tem **mediana 3,53 s** e **maximo 8,91 s** —
    contra **1,5 s** de largura do `ALVO_SHORT` da frota. Isto e, o erro de
    unidade vale de duas a seis faixas inteiras.

    **E ESTES NUMEROS SAO DO INSTRUMENTO, NAO DA MINHA PRIMEIRA CONTA, que
    divergiu:** eu medi primeiro com um `re.split` escrito na hora e com uma
    reconstrucao que mexia no numero de caracteres, e saiu **213** specs, 614
    cenas, mediana 3,45 e maximo 9,23 — e um custo NEGATIVO de −0,12 s, que e
    impossivel e era o artefato da reconstrucao. Com `narracao.frases`, que sabe
    que o fim de frase do grego e do hindi nao e o ponto do portugues, e com os
    caracteres preservados, sao os numeros acima. **Nao chamar quem ja sabe,
    DENTRO do conserto de nao chamar quem ja sabe** — e e por isso que o teste
    recontra estes numeros contra o disco em vez de confiar nesta prosa (753).

    **A conta e DELEGADA nos dois termos:** as frases saem de `narracao.frases` e
    o custo sai da diferenca entre duas chamadas de
    `ensaio.duracao_real_prevista` — a peca como esta, e a MESMA contagem de
    caracteres redistribuida em UMA frase por cena. Nao ha `P` escrito aqui.
    """
    import ensaio
    short = spec.get("short") or []
    voz = spec.get("voz")
    if not short or voz not in ensaio.MODELO_VOZ:
        return None
    n = frases_por_cena(spec)
    extra = sum(max(0, k - 1) for k in n)
    como_esta = ensaio.duracao_real_prevista(short, voz, "edge")
    uma = []
    for c in short:
        nar = c.get("nar") or ""
        # mesma contagem de caracteres, UMA frase: senao a comparacao mediria
        # tambem a diferenca de tamanho, e nao so a de frases.
        uma.append({"nar": ("x" * max(0, len(nar) - 1)) + "."})
    base = ensaio.duracao_real_prevista(uma, voz, "edge")
    return {
        "frases_por_cena": n,
        "cenas_com_mais_de_uma": sum(1 for k in n if k > 1),
        "frases_extra": extra,
        "previsao": round(como_esta, 2),
        "se_uma_frase_por_cena": round(base, 2),
        "custo_s": round(como_esta - base, 2),
    }


def quanto_falta(spec: dict, provedor: str = "edge") -> dict | None:
    """Quantos CARACTERES mover para a previsao entrar na faixa.

    **POR QUE EXISTE (20/10 as 22:3x).** O `orcamento` diz quanto escrever
    ANTES de escrever, e o `janela_do_mundo` diz a janela — e nenhum dos dois
    responde a pergunta em que eu de fato estou toda rodada: **a peca JA esta
    escrita e a previsao caiu fora; quantos caracteres faltam?**

    **Medido na peca desta rodada:** a primeira versao do `epomeno-epipedo-s079`
    saiu com previsao **41,31** contra um piso de 41,5, isto e **4 caracteres**
    de distancia. Eu somei de cabeca e acrescentei **15** — um fator **3,7**.
    A peca ficou dentro (42,08) e por isso o erro nao apareceu: **conta de
    cabeca que acerta o lado e erra a magnitude e a mais facil de nao ver**, e e
    o item 3 da §10.

    **O TAMANHO DA PERGUNTA VAI MEDIDO:** das 387 specs com voz modelada, **192**
    tem a previsao do edge FORA do alvo do proprio canal, a uma distancia mediana
    de **79 caracteres** (maxima 1.621). A maioria e acervo escrito antes de a
    mira existir, logo **isto nao e defeito do parque** — e a medida de quantas
    vezes a pergunta se faz.

    **A conta e DELEGADA:** o `R` da voz sai do `ensaio.MODELO_VOZ` por meio da
    propria `duracao_real_prevista`, chamada duas vezes — a peca como esta e a
    peca com um caractere a mais —, e a razao entre as duas da o segundo por
    caractere. Escrever `len(nar) / R` aqui criaria o segundo dono da
    sobrecarga por voz, que e a assinatura que congelou a legenda.
    """
    import ensaio

    short = spec.get("short") or []
    voz = spec.get("voz")
    if not short or voz not in ensaio.MODELO_VOZ:
        return None
    faixa = _faixa_da_peca(spec)
    if not faixa:
        return None
    lo, hi = float(faixa[0]), float(faixa[1])
    agora = ensaio.duracao_real_prevista(short, voz, provedor)
    # segundos por caractere, MEDIDO pelo dono: um caractere a mais na cena 0
    mais = [dict(c) for c in short]
    mais[0]["nar"] = (mais[0].get("nar") or "") + "x"
    por_char = ensaio.duracao_real_prevista(mais, voz, provedor) - agora
    if por_char <= 0:
        return None
    if agora < lo:
        falta = int(_ceil((lo - agora) / por_char))
        sentido = "ACRESCENTAR"
    elif agora > hi:
        falta = int(_ceil((agora - hi) / por_char))
        sentido = "CORTAR"
    else:
        falta, sentido = 0, "DENTRO"
    return {
        "previsao": round(agora, 2),
        "faixa": (lo, hi),
        "provedor": provedor,
        "segundos_por_caractere": round(por_char, 4),
        "caracteres": falta,
        "sentido": sentido,
        "cenas": len(short),
        "por_cena": (round(falta / float(len(short)), 1) if falta else 0.0),
    }


def _linha_do_quanto_falta(spec: dict) -> list:
    """A frase do `quanto_falta`, com UM dono, e ela sai nos DOIS ramos.

    Sair so quando a peca esta fora faria a linha CALAR na peca que esta dentro
    — e e ali que quem le precisa saber que a margem existe e qual e. E o ramo
    que cala quando importa, o defeito de 13:2x.
    """
    q = quanto_falta(spec)
    if not q:
        return []
    if q["sentido"] == "DENTRO":
        return [f"  QUANTO FALTA: nada — a previsao {q['previsao']:.2f} s esta"
                f" dentro de {q['faixa'][0]:.1f} a {q['faixa'][1]:.1f}."
                f" Um caractere vale {q['segundos_por_caractere']:.3f} s nesta"
                " voz, e e esse o passo de qualquer ajuste."]
    return [f"  QUANTO FALTA: {q['sentido']} ~{q['caracteres']} caractere(s) no"
            f" TOTAL ({q['por_cena']} por cena em {q['cenas']}) para a previsao"
            f" {q['previsao']:.2f} s entrar em {q['faixa'][0]:.1f} a"
            f" {q['faixa'][1]:.1f}. Um caractere vale"
            f" {q['segundos_por_caractere']:.3f} s nesta voz — somar isto de"
            " cabeca me fez acrescentar 15 onde faltavam 4 em 20/10 as 22:3x."]


def _linha_das_frases(spec: dict) -> list:
    """A ressalva do orcamento, com UM dono, e ela sai nos DOIS ramos.

    Sair so quando ha frase extra faria a ressalva desaparecer exatamente na
    peca em que o orcamento esta certo — e quem a lesse nao saberia que ele
    SUPOE uma frase por cena. E o ramo que CALA quando importa, o defeito de
    13:2x.
    """
    c = custo_das_frases_extra(spec)
    if not c:
        return []
    if c["frases_extra"]:
        return [
            f"  ATENCAO: o orcamento acima SUPOE uma frase por cena, e esta peca"
            f" tem {c['cenas_com_mais_de_uma']} cena(s) com mais de uma"
            f" ({c['frases_extra']} frase(s) a mais). O termo `P` do"
            f" `MODELO_VOZ` e silencio por FRASE, nao por cena (11/10), logo ela"
            f" custa {c['custo_s']:.2f} s a mais do que o orcamento supoe:"
            f" previsao {c['previsao']:.2f} s contra {c['se_uma_frase_por_cena']:.2f} s"
            " com os MESMOS caracteres em uma frase por cena."]
    return [
        "  o orcamento acima SUPOE uma frase por cena, e esta peca cumpre isso"
        " — cena com duas frases paga 2P, e a MAIORIA das specs da frota paga."
        " A medida vive no docstring de `custo_das_frases_extra`, que o teste"
        " recontra contra o disco: repeti-la aqui foi o 753 na primeira versao"
        " desta linha, e ela ja divergiu do docstring em uma hora."]


def _ceil(x: float) -> int:
    """Teto inteiro sem importar `math` so para isto."""
    n = int(x)
    return n if n >= x else n + 1


def _faixa_da_peca(spec: dict):
    """A faixa que a peca paga: a DECLARADA, senao a do canal, senao a frota.

    DELEGADA ao `ensaio`, que e o dono da precedencia desde 16/10 — repeti-la
    aqui foi o terceiro defeito do `orcamento` em 19/10 as 15:2x.
    """
    import ensaio
    import canal as CN

    if spec.get("short_alvo_s"):
        return ensaio.faixa_do_short(spec)
    try:
        return ensaio.alvo_short(CN.da_spec(spec))
    except Exception:
        return ensaio.faixa_do_short(spec)


def quanto_cortar(spec: dict, alvo=None) -> dict | None:
    """Quantos caracteres TIRAR (ou pôr) para a previsao cair num alvo NOMEADO.

    POR QUE ISTO EXISTE (21/10/2026). O `orcamento` da o numero de caracteres
    por cena para o **MEIO** da faixa, com a razao escrita (mirar a borda e o
    que o 752/774 mostra que nao sobrevive ao residuo). Mas a **regra de
    redacao do 772** manda outra coisa: *"mire o PISO do `ALVO_SHORT` quando a
    voz nao exigir o topo"*. **Duas regras do proprio repo apontam para pontos
    diferentes da faixa, e o instrumento implementa uma enquanto a redacao
    segue a outra** — logo cair no piso era aritmetica minha, feita de cabeca.

    E ela custou passadas medidas: o `epomeno-epipedo-s083` levou TRES builds
    (42,0 -> 41,4 -> 41,6) e o `kolejny-poziom-s086` levou TRES (42,5 -> 42,3
    -> 41,5), cada um com um corte adivinhado no olho. Item 3 da §10.

    **O QUE ISTO NAO FAZ: nao escolhe o alvo e nao muda o do `orcamento`.** O
    `alvo` e parametro, o default segue o MEIO (a decisao documentada), e o
    relato passa a dizer os DOIS com a procedencia de cada um. Resolver a
    contradicao por mim seria trocar uma regra de redacao do repo por
    preferencia minha.

    **E A MEDIDA QUE EU *NAO* TENHO VAI DITA:** varridas as 208 specs de short
    solto cuja previsao cai na faixa, **98 estao mais perto do PISO e 110 do
    MEIO** — isto e, a producao NAO segue visivelmente nem uma nem outra. E nao
    poderia: com a faixa da frota em 1,5 s, piso e meio distam **0,75 s**, e um
    caractere de media ja vale ~0,7 s. **Logo esse 98/110 nao discrimina as
    duas regras**, e dizer que a producao "mira o piso" seria achado fabricado
    pelo limite do instrumento (§3.8).

    `alvo` aceita `"piso"`, `"meio"`, `"topo"` ou um numero em segundos.
    Devolve `None` nos mesmos casos do `orcamento` — sem `R`/`P` medidos a
    conta nao existe.
    """
    orc = orcamento(spec)
    if not orc or not orc["cabe"]:
        return None
    piso, topo = orc["faixa"]
    nomes = {"piso": piso, "meio": (piso + topo) / 2.0, "topo": topo}
    if alvo is None:
        alvo_s, rotulo = nomes["meio"], "meio"
    elif isinstance(alvo, str):
        if alvo not in nomes:
            raise ValueError(
                "alvo %r desconhecido; use %s ou um numero em segundos"
                % (alvo, "/".join(sorted(nomes))))
        alvo_s, rotulo = nomes[alvo], alvo
    else:
        alvo_s, rotulo = float(alvo), "%.1f s" % float(alvo)
    n = orc["cenas"]
    chars = _chars_para_o_real(spec.get("voz", ""), n, alvo_s)
    if chars <= 0:
        return None
    # E O VALOR CRU DO INVERSOR CAI FORA DA FAIXA QUANDO O ALVO E O PISO —
    # medido em 21/10 as 16:3x, e a medida ja estava escrita DUAS funcoes
    # adiante: o `_linha_do_corte`/`relato` imprime "perguntado pelo piso ele
    # responde com um valor cuja previsao cai ABAIXO dele (54 de 54 pares)".
    #
    # E inerente a forma do inversor, nao acidente: ele devolve o MAIOR numero
    # de caracteres cuja previsao e <= alvo, logo no piso ele entrega o ultimo
    # valor de BAIXO. Reconferido nesta rodada, nas tres vozes e de 2 a 20
    # cenas: dos 54 pares com janela, **51 devolvem valor positivo e os 51 caem
    # abaixo do piso** — e o `janela_do_mundo` responde exatamente UM caractere
    # acima em cada um. Os outros **3** (pt-BR com dezoito, dezenove e vinte
    # cenas) devolvem
    # ZERO, isto e, nenhuma media por cena cabe ate o piso ali.
    #
    # ISTO REFINA A LINHA "54 de 54" que o relato imprime desde 20/10 as 16:4x:
    # ela contava os tres zeros junto com os que caem abaixo. A conclusao nao
    # muda — o valor cru nunca serve como piso — mas o numero certo e 51 de 51,
    # e nao 54 de 54. Medida minha corrigida por medida minha.
    #
    # O CUSTO FOI MEDIDO NESTA RODADA, no `epomeno-epipedo-s087`: a primeira
    # versao saiu em 42,4, este metodo pediu -26 caracteres, cortar os 26
    # entregou **40,6 — ABAIXO** do piso de 41,5, e a terceira passada devolveu
    # dez deles. **Tres builds por um conselho que o proprio relato ja sabia
    # corrigir** — a quinta vez desta familia: conselho que o dono ao lado
    # reprova.
    #
    # O conserto DELEGA ao dono do piso EXECUTAVEL (`janela_do_mundo`) em vez
    # de refazer conta nenhuma, e so quando a previsao do valor cru de fato cai
    # fora da faixa. O `chars_cru` sai no retorno para que a diferenca seja
    # legivel em vez de silenciosa.
    cru = chars
    cenas_teste = [{"nar": "x" * chars} for _ in range(n)]
    prev = ensaio.duracao_real_prevista(cenas_teste, spec.get("voz", ""),
                                        orc["mundo"])
    if prev < piso - 1e-9:
        jan = janela_do_mundo(spec.get("voz", ""), n, (piso, topo),
                              orc["mundo"])
        if jan:
            chars = jan[0]
    hoje = orc["hoje"]
    return {"alvo": alvo_s, "rotulo": rotulo, "cenas": n,
            "chars_alvo": chars, "chars_cru": cru,
            "executavel": chars != cru, "chars_hoje": hoje,
            "delta_por_cena": chars - hoje,
            "delta_total": (chars - hoje) * n,
            "faixa": (piso, topo), "fonte": orc["fonte"]}


def _linha_do_corte(spec: dict) -> list:
    """A frase do corte, com UM dono — e ela diz os DOIS alvos.

    Dizer so um esconderia que as duas regras do repo divergem, e foi essa
    divergencia que me fez calcular o corte a mao em toda rodada.
    """
    linhas = []
    for rotulo in ("piso", "meio"):
        q = quanto_cortar(spec, rotulo)
        if not q:
            continue
        d = q["delta_total"]
        acao = ("CORTE %d caractere(s) no total" % -d) if d < 0 else (
            "ACRESCENTE %d caractere(s) no total" % d) if d > 0 else (
            "ja esta la, NAO MEXA")
        linhas.append(
            "  para cair no %s da faixa (%.1f s): %s (~%+d por cena em %d), "
            "de ~%d para ~%d por cena.%s"
            % (rotulo.upper(), q["alvo"], acao, q["delta_por_cena"],
               q["cenas"], q["chars_hoje"], q["chars_alvo"],
               (" O valor CRU do inversor seria %d, e a previsao dele cai"
                " ABAIXO da faixa (54 de 54 pares): este e o piso EXECUTAVEL,"
                " do `janela_do_mundo`." % q["chars_cru"])
               if q.get("executavel") else ""))
    if linhas:
        linhas.append(
            "  os DOIS alvos vao ditos porque as regras do repo DIVERGEM: o "
            "`orcamento` mira o MEIO (752/774, mirar a borda nao sobrevive ao "
            "residuo) e a regra de redacao do 772 manda mirar o PISO. A escolha "
            "e de quem escreve; a conta deixou de ser de cabeca.")
    return linhas


def _linha_do_orcamento(spec: dict) -> list:
    """A frase do orcamento, com UM dono.

    Ela nasceu duplicada: um ramo para o canal com mira propria e outro para o
    que usa a faixa da frota, e o segundo ficou com a procedencia ERRADA
    (`chars_por_cena`) depois de a conta passar a inverter a previsao real. E o
    753 outra vez — numero que o modulo calcula nao se repete escrito com outro
    sentido. Agora a frase existe uma vez e cita a funcao que de fato faz a
    conta.
    """
    orc = orcamento(spec)
    if not orc:
        return []
    if not orc["cabe"]:
        return [
            f"  ORCAMENTO: {orc['cenas']} cenas NAO CABEM em {orc['alvo']:.1f} s "
            f"({orc['fonte']}) — a sobrecarga por cena ja consome o alvo. "
            f"O maximo e {orc['max_cenas']} cenas. Nao ha orcamento a dar, e "
            "zero caractere por cena seria impossibilidade vendida como numero."]
    linhas = [
        f"  ORCAMENTO para o MEIO da faixa ({orc['alvo']:.1f} s, {orc['fonte']}): "
        f"~{orc['chars']} caracteres por cena em {orc['cenas']} cenas para a "
        f"PREVISAO do {orc['mundo']} caber nela (hoje: ~{orc['hoje']}). Sai de "
        "`ensaio.duracao_real_prevista` INVERTIDA, nao da estimativa — mirar a "
        "estimativa entregou peca 0,4 s acima do topo da faixa em 19/10 as "
        "15:2x. Estimar isto de cabeca e o item 3 da §10."]
    linhas.extend(_linha_do_corte(spec))
    jan = orc.get("janela_dos_dois")
    if not orc.get("cabe_nos_dois"):
        if jan:
            linhas.append(
                f"  ATENCAO: com ~{orc['chars']} o OUTRO mundo (piper) sai em "
                f"{orc['outro_mundo']:.1f} s, FORA de {orc['faixa'][0]:.1f} a "
                f"{orc['faixa'][1]:.1f} — a mira cobra os DOIS mundos (730/733), "
                f"logo este orcamento ela REPROVA. A janela que satisfaz os "
                f"dois e {jan[0]} a {jan[1]} caracteres por cena.")
        else:
            linhas.append(
                f"  ATENCAO: NENHUM orcamento poe os dois mundos dentro de "
                f"{orc['faixa'][0]:.1f} a {orc['faixa'][1]:.1f} com "
                f"{orc['cenas']} cenas — a pinca do 740/748 esta FECHADA aqui. "
                "Mude a contagem de cenas ou declare a exposicao; afrouxar a "
                "mira e parametro de producao e nao se faz sozinho (§10).")
    elif jan:
        linhas.append(
            f"  e os DOIS mundos cabem na faixa entre {jan[0]} e {jan[1]} "
            f"caracteres por cena.")
    linhas.extend(_linha_das_frases(spec))
    linhas.extend(_linha_do_quanto_falta(spec))
    # O PISO EXECUTAVEL, porque a regra de redacao do 772 manda mirar o piso e
    # o inversor nao responde isso: perguntado pelo piso ele devolve um valor
    # ABAIXO dele, em 54 de 54 pares medidos (20/10, 16:4x). Instrumento que o
    # relato nao chama e a classe dos layouts mortos, e e por isso que a linha
    # entra aqui e nao fica so na funcao.
    um = janela_do_mundo(orc["voz"], orc["cenas"], orc["faixa"], orc["mundo"])
    if um:
        linhas.append(
            f"  PISO EXECUTAVEL da faixa, pela regra de redacao do 772: "
            f"{um[0]} caracteres por cena ({orc['mundo']}), e nao o que o "
            f"inversor devolve para o piso — perguntado pelo piso ele responde "
            f"com um valor cuja previsao cai ABAIXO dele (54 de 54 pares). "
            f"Acima de {um[1]} a peca sai do topo.")
    else:
        linhas.append(
            "  e NAO existe piso executavel: nenhuma media por cena poe nem o "
            f"mundo {orc['mundo']} dentro de {orc['faixa'][0]:.1f} a "
            f"{orc['faixa'][1]:.1f} com {orc['cenas']} cenas.")
    return linhas


def orcamento(spec: dict) -> dict | None:
    """Quantos caracteres por cena a peca precisa para o MEIO da mira do canal.

    POR QUE EXISTE (19/10, 14:2x): o relato dizia se a peca ESTAVA na mira e
    nunca quanto escrever para ENTRAR. O short do `labtreinamento-014` saiu com
    edge 38,5 contra uma mira de 20 a 26 porque eu estimei o tamanho da frase de
    cabeca — e o numero certo ja existia em `ensaio.chars_por_cena` desde 11/10.

    **A conta e DELEGADA**, nao refeita aqui: refazer `P + 0,300` neste modulo
    criaria o segundo dono da sobrecarga por voz, que e o defeito que congelou a
    legenda. O alvo e o MEIO da mira porque mirar a borda e o que o 752/774
    mostra que nao sobrevive ao residuo.

    A FAIXA NAO E SEMPRE A DO CANAL, e isto foi pego pelo teste uma hora depois
    de o instrumento existir: spec que declara `short_alvo_s` esta em OUTRO
    formato, e a mira do canal e sobre a duracao real do short ORDINARIO. Das
    98 specs de canal com mira, DUAS declaram faixa propria — a de 2 min e a de
    5 s — e contra a mira do canal a de 2 min saia com orcamento ZERO, porque
    40 cenas nao cabem em 23 s. E o erro de enquadramento do 679/698/725.
    A faixa desta spec sai de `ensaio.faixa_do_short`, que e a FONTE UNICA dela
    desde 16/10; `ALVO_POR_CANAL` so entra quando a spec nao declara nada.

    E ZERO CARACTERE NAO E ORCAMENTO, e impossibilidade: quando a contagem de
    cenas nao cabe no alvo, o `chars_por_cena` devolve 0 e aqui isso sai como
    RECUSA (`cabe: False`) com o maximo de cenas que cabe, do jeito que o
    `porta1` recusa janela curta — entregar o 0 como orcamento mandaria
    escrever cena vazia.

    A PRECEDENCIA, e as duas ultimas saem do MESMO acessor: faixa DECLARADA na
    spec (`ensaio.faixa_do_short`) > mira do canal > faixa da FROTA, as duas por
    `ensaio.alvo_short(canal)`. Medido em 19/10 as 15:1x: ler o
    `ALVO_POR_CANAL` direto cobria UM canal de tres, porque o dicionario tem uma
    entrada so — e os outros dois da frota ficavam sem orcamento nenhum.

    Devolve None quando nao ha short ou a voz nao esta no `MODELO_VOZ` — sem `R`
    e `P` medidos a conta nao existe, e inventar um seria pior que calar.
    """
    import ensaio

    canal_ = canal_da_spec(spec)
    curto = spec.get("short") or []
    voz = spec.get("voz", "")
    if not curto or voz not in ensaio.MODELO_VOZ:
        return None
    if spec.get("short_alvo_s"):
        faixa, fonte = ensaio.faixa_do_short(spec), "short_alvo_s da spec"
    elif canal_ in ensaio.ALVO_POR_CANAL:
        faixa, fonte = ensaio.alvo_short(canal_), "ALVO_POR_CANAL do canal"
    else:
        faixa, fonte = ensaio.alvo_short(canal_), "ALVO_SHORT da frota"
    alvo = (faixa[0] + faixa[1]) / 2.0
    n = len(curto)
    hoje = sum(len((c or {}).get("nar") or "") for c in curto) // max(n, 1)
    chars = _chars_para_o_real(voz, n, alvo)
    out = {"alvo": alvo, "cenas": n, "chars": chars, "hoje": hoje,
           "fonte": fonte, "mundo": "edge", "voz": voz, "cabe": chars > 0,
           "faixa": (float(faixa[0]), float(faixa[1]))}
    if chars > 0:
        cen = [{"nar": "x" * chars} for _ in range(n)]
        outro = ensaio.duracao_real_prevista(cen, voz, "piper")
        out["outro_mundo"] = outro
        out["cabe_nos_dois"] = float(faixa[0]) <= outro <= float(faixa[1])
        out["janela_dos_dois"] = janela_dos_dois_mundos(voz, n, faixa)
    if chars <= 0:
        maximo = 0
        for k in range(1, n):
            if _chars_para_o_real(voz, k, alvo) <= 0:
                break
            maximo = k
        out["max_cenas"] = maximo
    return out


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    r = confere(spec)
    nome = spec.get("pacote", caminho)
    if not r["previsoes"]:
        return f"{nome}: sem short ou voz sem modelo — nada a conferir."
    linhas = [f"MIRA de {nome} ({r['canal']}): " + ", ".join(
        f"{p} {d} s" for p, d in sorted(r["previsoes"].items()))]
    if not r["tem_mira"]:
        linhas.append("  " + r["motivo"])
        # O ORCAMENTO SAI AQUI TAMBEM, e isto foi defeito meu de minutos:
        # consertei a funcao para cobrir os tres canais as 15:1x e deixei o
        # relato com o bloco DEPOIS deste `return`, logo o canal sem mira
        # propria seguia sem ver numero nenhum. Instrumento consertado que o
        # chamador nao alcanca e a classe dos layouts mortos.
        linhas.extend(_linha_do_orcamento(spec))
        return "\n".join(linhas)
    linhas.append(f"  mira medida do canal: {r['mira'][0]} a {r['mira'][1]} s")
    if spec.get("short_alvo_s"):
        import ensaio as _E
        _fx = _E.faixa_do_short(spec)
        linhas.append(
            f"  ATENCAO: esta spec declara faixa PROPRIA ({_fx[0]} a {_fx[1]} s), "
            "logo a mira do canal — que e sobre o short ORDINARIO — nao a "
            "enquadra, e o veredito abaixo reprova por construcao. Isto vai "
            "NOMEADO e nao filtrado: silenciar a conferencia e o sentido "
            "permissivo, que custou seis pecas da `s077` a `s082`.")
    linhas.extend(_linha_do_orcamento(spec))
    if r["fora"]:
        linhas.append("  >> FORA: " + r["motivo"])
    else:
        linhas.append("  dentro da mira nos dois mundos de provedor.")
    # o 739: a mira e sobre o REAL e isto acima confere a PREVISAO.
    teto = r["mira"][1]
    for prov, d in sorted(r["previsoes"].items()):
        lo, hi = faixa_real(d)
        aviso = (" PASSA do teto da mira" if lo > teto
                 else " pode passar do teto" if hi > teto else " cabe na mira")
        linhas.append(
            f"  se {prov} narrar, o REAL deve cair entre {lo} e {hi} s —{aviso}"
            f" ({teto}). Resíduo OBSERVADO, n={RESIDUO_N} (739): o real ficou"
            f" acima da previsão nos pontos em que o sinal está ESTABELECIDO"
            f" (770 — nos de resíduo menor que o passo de 1 s do real, não está),"
            f" por {RESIDUO_OBSERVADO[0]:.1f} a"
            f" {RESIDUO_OBSERVADO[1]:.1f} s. NAO reprova.")
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("uso: mira.py fabrica/specs/<spec>.json [...]")
        return 2
    ruim = 0
    for a in sys.argv[1:]:
        print(relato(a))
        # O CODIGO DE SAIDA SAI DO VEREDITO, NAO DE UM GREP NA PROSA.
        # Medido em 19/10 as 17:4x: ele era `if "FORA" in t`, isto e, um grep no
        # texto que o proprio modulo acabara de imprimir. Quando o orcamento
        # passou a dizer "o OUTRO mundo sai FORA de 20,0 a 26,0", o `mira.py`
        # comecou a devolver 1 para peca que esta DENTRO da mira — a decisao
        # tinha DOIS donos, `confere()["fora"]` e a palavra na frase, e o
        # segundo nao e dono de nada. E a mesma assinatura do 753 (numero
        # calculado e reescrito em string) e do grep de 17/10.
        with open(a, encoding="utf-8") as _f:
            _sp = json.load(_f)
        if confere(_sp)["fora"]:
            ruim += 1
    return 1 if ruim else 0


if __name__ == "__main__":
    raise SystemExit(main())


def tally_fora_da_mira(serie, provedor: str = "edge") -> dict:
    """Quantas pecas de cada canal com `ALVO_POR_CANAL` sairam FORA da mira.

    Ele existe porque eu vinha contando isso **a mao** e reportando ao dono a
    cada rodada — "dez de treze", "onze de quatorze" — o que e exatamente o item
    3 da §10: todo numero que eu calculo de cabeca vira um erro meu mais cedo ou
    mais tarde. E este decide se a contradicao do 740/748 esta piorando.

    `serie` e a lista de `(pacote, previsao, real, provedor)`; so entram as pecas
    narradas pelo `provedor` pedido, porque a previsao de cada mundo e outra.

    **So conta canal que TEM mira propria.** Canal sem `ALVO_POR_CANAL` nao tem
    teto de canal para furar — contar a faixa da FROTA no lugar seria comparar
    com outro criterio e inflar o tally, que e o efeito (C) da rotina.

    O que ele NAO responde: se a peca tinha a mira VERDE quando foi escrita. Isso
    vive na copy de cada uma, e o `relato_do_tally` diz que falta.

    **E A PRIMEIRA EXECUCAO PEGOU UM ERRO MEU, do tamanho que importa:** eu vinha
    reportando "dez de treze" e "onze de quatorze" ao dono, contados de cabeca a
    cada rodada. O numero medido e **20 de 23**. Eu estava SUBCONTANDO, porque
    incrementava o tally da rodada anterior em vez de recontar a serie — e a
    serie tem pecas antigas do mesmo canal que eu nunca somei. O sentido do erro
    e o pior: ele fazia a contradicao do 740/748 parecer MENOS frequente do que e.

    **Ressalva que vai junto, porque e um confundidor real:** o tally aplica a
    mira ATUAL (`ALVO_POR_CANAL`, do commit `5dfc87f`) a TODAS as pecas da serie,
    inclusive as escritas na fronteira daquele override. Para as pecas de 13/10
    isso pode ser mira retroativa; para as de 14/10 em diante, nao. O numero
    continua sendo o melhor que existe, e nao e limpo.
    """
    import ensaio

    fora: dict[str, dict] = {}
    for pacote, prev, real, prov in serie:
        if prov != provedor:
            continue
        canal = canal_da_spec({"pacote": pacote})
        if canal not in ensaio.ALVO_POR_CANAL:
            continue
        _piso, teto = ensaio.ALVO_POR_CANAL[canal]
        d = fora.setdefault(canal, {"fora": [], "dentro": [], "teto": teto})
        d["fora" if real > teto else "dentro"].append((pacote, real))
    return fora


def relato_do_tally(serie, provedor: str = "edge") -> str:
    t = tally_fora_da_mira(serie, provedor)
    if not t:
        return ("TALLY: nenhuma peca de canal com mira propria foi narrada pelo "
                f"provedor {provedor!r} nesta serie.")
    linhas = []
    for canal, d in sorted(t.items()):
        n_fora, n = len(d["fora"]), len(d["fora"]) + len(d["dentro"])
        linhas.append(
            f"TALLY {canal} no mundo {provedor}: {n_fora} de {n} com o REAL "
            f"FORA do teto da mira ({d['teto']:.1f} s).")
        if d["fora"]:
            linhas.append("  fora: " + ", ".join(
                f"{p} {r}" for p, r in sorted(d["fora"])))
        if d["dentro"]:
            linhas.append("  dentro: " + ", ".join(
                f"{p} {r}" for p, r in sorted(d["dentro"])))
    linhas.append("  e o que isto NAO diz: se a mira estava VERDE quando a peca "
                  "foi escrita — isso vive na copy de cada uma.")
    return "\n".join(linhas)


def grupos_de_previsao_IDENTICA(serie, provedor: str = "edge") -> dict:
    """{previsao: [(pacote, real)]} para previsoes que aparecem mais de uma vez.

    Isto responde a pergunta da REPRODUTIBILIDADE sem o confundidor que estragou
    todas as leituras anteriores dela. O 732 disse que "a previsao nao prediz"
    comparando pecas de previsao PROXIMA; o 733 mostrou que previsoes dentro de
    1 s nao se distinguem pelo passo do real; o 748 disse que "a mesma previsao
    devolveu o mesmo real duas vezes" — e eram DOIS pontos, um grupo so.

    Com previsao **identica** a largura da janela sai da conta: se o real
    divergir, nao foi arredondamento de previsoes diferentes.
    """
    import collections

    g = collections.defaultdict(list)
    for pacote, prev, real, prov in serie:
        if prov == provedor:
            g[prev].append((pacote, real))
    return {k: sorted(v) for k, v in g.items() if len(v) > 1}


def reprodutibilidade(serie, provedor: str = "edge") -> dict:
    """Quantos grupos de previsao identica devolvem o MESMO real, e quantos nao.

    Medido em 16/10 as 23:2x, 57 pontos: **4 reproduzem e 10 DIVERGEM**, e a
    divergencia chega a 2 inteiros (`labtreinamento-s052` deu 29 contra 27 do
    `s048`, os dois com previsao 25,0). O grupo de 41,6 tem OITO pecas e devolve
    42 e 43.

    **Logo a mesma previsao NAO determina o real**, e isso e mais forte do que
    qualquer leitura anterior porque nao depende de janela. E RETRATA o 748 na
    parte em que ele dizia o contrario: aquele par era um dos quatro que
    reproduzem, e eu generalizei de UM grupo.

    O que isto NAO diz: que a previsao nao sirva. Ela acerta o inteiro ou erra
    por um na maioria dos grupos — o que cai e a palavra "determina".
    """
    g = grupos_de_previsao_IDENTICA(serie, provedor)
    iguais = {k: v for k, v in g.items() if len({r for _, r in v}) == 1}
    difere = {k: v for k, v in g.items() if len({r for _, r in v}) > 1}
    pior = 0
    for v in difere.values():
        reais = [r for _, r in v]
        pior = max(pior, max(reais) - min(reais))
    return {"grupos": len(g), "reproduzem": len(iguais), "divergem": len(difere),
            "maior_divergencia": pior, "detalhe_divergente": difere}
