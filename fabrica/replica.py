"""Escolhe qual das TRES leituras de contador vale, e qual gravar.

POR QUE ISTO EXISTE, e e a terceira vez que o mesmo defeito me pega.

O contador de view do YouTube e servido por REPLICAS, e algumas estao
atrasadas. Tres leituras na mesma rodada discordam, e a escolha entre elas foi
prosa na rotina ate 11/10/2026 — eu fazia no olho, toda rodada.

O que foi medido, em ordem:

  688 (09/10, `critico`) — a MEDIANA das tres devolve a replica ATRASADA. Das
  17 pecas que mudaram, TODAS subiram na terceira leitura e NENHUMA na segunda.
  Um contador de view so ATRASA, nunca adianta, entao o estimador e o MAXIMO,
  declarado como PISO, com a faixa ao lado.

  707 (10/10, `alto`) — `grava_metricas_janela` grava a replica DAQUELA
  chamada, nao o maximo. Gravar a chamada errada SUBESTIMA PARA SEMPRE: no
  `ZxHWcfDNovM` as leituras deram 830, 833, 830 e a gravacao guardou 830.

  708 (10/10, `alto`, e substitui o procedimento do 707) — a replica atrasada e
  da CHAMADA INTEIRA, nao de cada id. As quatro pecas que divergiram divergiram
  com a MESMA forma {alto, baixo, alto}; as outras dezesseis vieram identicas.
  Logo nao se caca o maximo peca por peca: compara-se a SOMA das tres chamadas
  e grava-se a de soma maxima, em UM statement (702).

E o que NAO sobreviveu: a ordem das replicas nao tem regra. A fresca foi a
terceira em 09/10, a segunda as 07:09 e a primeira e a terceira as 08:08.
**Nunca leia nada pela ORDEM.**
"""

from __future__ import annotations


def soma(leitura: dict[str, int]) -> int:
    """Soma dos contadores de uma chamada. E o criterio do 708."""
    return sum(leitura.values())


def chamada_para_gravar(leituras: list[dict[str, int]]) -> int:
    """Indice da chamada de SOMA MAXIMA — a que deve ir para o banco.

    Empate devolve a PRIMEIRA, porque com soma igual as chamadas sao
    equivalentes para o que o 708 mede e escolher a ultima so adicionaria
    dependencia da ordem, que e justamente o que o 708 enterrou.
    """
    if not leituras:
        raise ValueError("sem leituras")
    somas = [soma(x) for x in leituras]
    return somas.index(max(somas))


def piso(leituras: list[dict[str, int]]) -> dict[str, int]:
    """O estimador do 688: MAXIMO por id, entre as chamadas, como PISO.

    Id ausente numa chamada NAO vira zero — ausencia e silencio, nao leitura de
    zero, e tratar como zero puxaria o maximo para baixo em peca que so apareceu
    numa das chamadas. O 665 e do mesmo feitio: agregado esconde chamada que
    falhou, e por isso cada requisicao tem de ser conferida pelo `status_code`
    ANTES de chegar aqui.
    """
    fora: dict[str, int] = {}
    for leitura in leituras:
        for vid, n in leitura.items():
            if vid not in fora or n > fora[vid]:
                fora[vid] = n
    return fora


def faixa(leituras: list[dict[str, int]]) -> dict[str, tuple[int, int]]:
    """Minimo e maximo por id. O piso vai SEMPRE com a faixa ao lado (688)."""
    fora: dict[str, tuple[int, int]] = {}
    for leitura in leituras:
        for vid, n in leitura.items():
            if vid not in fora:
                fora[vid] = (n, n)
            else:
                lo, hi = fora[vid]
                fora[vid] = (min(lo, n), max(hi, n))
    return fora


def divergentes(leituras: list[dict[str, int]]) -> dict[str, tuple[int, ...]]:
    """Ids que NAO vieram identicos nas chamadas, com os valores na ordem lida.

    Serve para conferir a assinatura do 708: se a divergencia e da chamada, os
    divergentes compartilham a MESMA FORMA (todos {alto, baixo, alto}, por
    exemplo). Se as formas discordarem entre si, a hipotese do 708 nao se aplica
    aquela rodada e o relato tem de dizer isso em vez de gravar no automatico.
    """
    fora: dict[str, tuple[int, ...]] = {}
    for vid in piso(leituras):
        serie = tuple(x[vid] for x in leituras if vid in x)
        if len(set(serie)) > 1:
            fora[vid] = serie
    return fora


def mesma_forma(leituras: list[dict[str, int]]) -> bool:
    """True quando todo divergente tem a mesma forma relativa — a marca do 708.

    A forma e o RANKING dos valores na ordem lida, nao os valores: `833, 830,
    833` e `91, 90, 91` tem a mesma forma. Sem divergente, devolve True — nao
    ha contradicao a relatar.
    """
    formas = set()
    for serie in divergentes(leituras).values():
        ordenados = sorted(set(serie))
        formas.add(tuple(ordenados.index(n) for n in serie))
    return len(formas) <= 1


# ===========================================================================
# O PICO QUE NAO ERA REPLICA FRESCA — medido em 12/10/2026 as 20:1x
# ===========================================================================
#
# O procedimento do 708 (gravar a chamada de SOMA MAXIMA) assume que a chamada
# alta e a replica FRESCA, e portanto que o maximo e um PISO (688). Em 12/10 as
# 19:11 eu segui o procedimento com este modulo, e a rodada seguinte mostrou
# que ele gravou um PICO:
#
#     peca            17:10   18:21   19:11   20:11
#     MjeP-_yDni4        20      20    *24*      20
#     O1PNIRYoeGY         1       1     *7*       1
#     xhPyfHdTwds         0       2     *8*       2
#     nUrSPWKHy8I         -     114     115     122   <- esta subiu de verdade
#
# As TRES primeiras subiram so na chamada de soma maxima das 19:11 e voltaram
# ao valor anterior na rodada seguinte, nas TRES chamadas. Dentro da rodada das
# 19:11 as leituras eram {20,24,20}, {1,7,1}, {2,8,2}: a MODA acertou as tres e
# o MAXIMO errou as tres.
#
# E ISSO NAO CONTRADIZ O 688 — contradiz a leitura que eu fazia dele. No 688 as
# seventeen pecas subiram juntas na terceira leitura E a subida PERSISTIU. Hoje
# a subida nao persistiu. **Dentro de UMA rodada as duas situacoes sao
# indistinguiveis**: uma chamada alta e solitaria pode ser replica fresca (688)
# ou pico (hoje). Quem decide e a rodada SEGUINTE.
#
# Logo o maximo e o maximo OBSERVADO, nao um piso sobre a verdade. Um numero que
# tres chamadas depois ja nao existe nao era piso de nada.


def moda(leituras: list[dict[str, int]]) -> dict[str, int]:
    """O valor que a MAIORIA das chamadas da rodada reporta, por peca.

    Sem maioria (todas diferentes), devolve o maximo e deixa o caso para o
    `veredito_do_pico` da rodada seguinte.
    """
    ids = {i for l in leituras for i in l}
    out = {}
    for i in ids:
        vals = [l[i] for l in leituras if i in l]
        if not vals:
            continue
        contagem = {v: vals.count(v) for v in set(vals)}
        melhor = max(contagem.values())
        if melhor > 1:
            # Entre valores empatados em frequencia, o maior.
            out[i] = max(v for v, c in contagem.items() if c == melhor)
        else:
            out[i] = max(vals)
    return out


def veredito_do_pico(leituras_da_rodada: list[dict[str, int]],
                     seguinte: dict[str, int]) -> dict[str, str]:
    """Para cada peca divergente, a rodada SEGUINTE diz o que aquilo era.

    - "fresca": a leitura seguinte e >= o maximo da rodada anterior, logo a
      chamada alta era mesmo a replica fresca (o caso do 688);
    - "pico": a leitura seguinte voltou para a moda ou abaixo dela, logo o
      maximo era pico e a gravacao daquela rodada SUPERESTIMA;
    - "indeterminado": a seguinte caiu entre a moda e o maximo.

    `seguinte` e UMA leitura ja consolidada da rodada seguinte (a moda dela, de
    preferencia). Peca ausente na seguinte nao recebe veredito: ausencia e
    silencio, nunca zero.
    """
    div = divergentes(leituras_da_rodada)
    m = moda(leituras_da_rodada)
    out = {}
    for i, vals in div.items():
        if i not in seguinte:
            continue
        alto, base = max(vals), m.get(i, max(vals))
        v = seguinte[i]
        if v >= alto:
            out[i] = "fresca"
        elif v <= base:
            out[i] = "pico"
        else:
            out[i] = "indeterminado"
    return out


# ===========================================================================
# A RODADA INTEIRA PODE CAIR NA REPLICA ATRASADA — medido as 21:1x de 12/10,
# e isto RETRATA a conclusao do 720, que eu escrevi uma hora antes.
# ===========================================================================
#
# O 720 dizia que a chamada de soma maxima das 19:11 tinha gravado um PICO,
# porque as 20:11 as TRES chamadas devolveram o valor da moda anterior. As 21:1x
# o `veredito_do_pico` — escrito justamente para isso — devolveu **"fresca" nas
# quatro pecas**:
#
#     peca            17:10  18:21  19:11  20:11  21:1x
#     MjeP-_yDni4        20     20    *24*     20     40
#     O1PNIRYoeGY         1      1     *7*      1     10
#     xhPyfHdTwds         0      2     *8*      2      8
#     nUrSPWKHy8I         -    114    115     122    122
#
# O 8 do `xhPyfHdTwds` **voltou**, identico, nas tres chamadas das 21:1x. View
# nao ressuscita: logo o 8 das 19:11 era verdade, e **a rodada das 20:11 inteira
# — as tres chamadas — caiu na replica atrasada.**
#
# Entao o 708 era mais forte do que eu entendi: a replica atrasada nao e so da
# CHAMADA, ela pode ser da RODADA. E a consequencia e dura: **tres chamadas de
# acordo NAO sao evidencia de verdade.** Concordancia dentro da rodada mede uma
# coisa so — que as tres cairam na mesma particao.
#
# O discriminador nao esta DENTRO da rodada, esta no TEMPO: contador de view nao
# desce. Leitura mais nova abaixo de leitura mais velha e a NOVA que esta
# atrasada, em qualquer rodada, com qualquer concordancia.


def monotonia(serie: list[tuple[str, dict[str, int]]]) -> dict[str, list[str]]:
    """Viola a monotonia quem? `serie` = [(rotulo, {peca: views}), ...] em ordem.

    Devolve, por peca, os rotulos das leituras que estao ABAIXO de alguma
    leitura anterior — isto e, as que sao necessariamente de replica atrasada,
    porque contador de view nao desce.

    Esta e a unica conferencia de replica que NAO depende de concordancia dentro
    da rodada, e por isso e a que sobrevive ao caso de 20:11, em que as tres
    chamadas concordaram e as tres estavam atrasadas.

    Peca ausente numa leitura e SILENCIO: ela nao entra como zero e nao conta
    como violacao.
    """
    out: dict[str, list[str]] = {}
    maximo: dict[str, int] = {}
    for rotulo, leitura in serie:
        for peca, v in leitura.items():
            if peca in maximo and v < maximo[peca]:
                out.setdefault(peca, []).append(rotulo)
            maximo[peca] = max(maximo.get(peca, v), v)
    return out


def piso_por_rodadas(serie: list[tuple[str, dict[str, int]]]) -> dict[str, int]:
    """O maximo de cada peca ao longo das RODADAS — o piso que de fato vale.

    Diferente do `piso`, que olha as tres chamadas de UMA rodada. Aqui o
    argumento e temporal e nao estatistico: o contador nao desce, entao o maior
    valor ja observado e um limite inferior sobre a verdade, venha ele da rodada
    que vier.
    """
    out: dict[str, int] = {}
    for _, leitura in serie:
        for peca, v in leitura.items():
            out[peca] = max(out.get(peca, v), v)
    return out
