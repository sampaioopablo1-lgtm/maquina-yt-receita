"""A cadencia de plano do longo — a terceira das tres distancias, com instrumento.

POR QUE EXISTE. Em 16/10/2026 eu medi o longo da referencia (`FtCtIJPsc_Q`,
530,03 s) quadro a quadro e escrevi que a distancia entre a peca do dono e as
nossas sao TRES coisas, todas de longo: o trilho de capitulos permanente, os
**18,9 s por plano**, e cinco layouts que o `layout.py` nao tinha. Em 19/10 as
04:2x e as 07:2x os cinco layouts entraram; as 08:1x o trilho foi ligado ao
render. **Sobrava a cadencia, e ela era a unica que eu vinha calculando DE
CABECA** — "530 dividido por 28" — que e o item 3 da §10 da rotina: toda conta
que eu faco a mao vira um erro meu.

A PROCEDENCIA DO NUMERO DA REFERENCIA, e ela e medida e nao escolhida:

    530,03 s de duracao  /  28 transicoes  =  18,93 s por plano

As 28 transicoes sairam do mesmo metodo do 690/699 (`tblend=all_mode=difference`
+ `signalstats`, escala absoluta 0-255) aplicado ao arquivo baixado — nenhuma
delas passa de `scene 0,15`, que e o que diz que o trilho e a marca d'agua nunca
saem da tela e so o painel troca. Ver `fabrica/video_referencia.py`.

**O QUE ESTE MODULO NAO FAZ, e vai dito antes de qualquer numero: ele nao decide
que 18,9 s e o alvo certo.** A referencia e UMA peca, feita a mao pelo dono, e o
veredito de desempenho dela e view — que nos nao medimos por falta do escopo de
analytics. Chamar 18,9 de alvo seria limiar sem procedencia (§10). O que ele faz
e dizer ONDE a nossa peca esta em relacao a ela, e quantas cenas uma duracao
pediria para chegar la. Decidir e do dono.

**E ELE NAO E PORTAO**, pelo mesmo argumento do `mira.py`: varrido o disco, TODA
spec de longo da frota esta a mais de 10 s de distancia da referencia, logo um
portao aqui reprovaria tudo e um aviso que dispara sempre deixa de avisar.
"""

import ensaio

# Medido, nao escolhido — ver o docstring. Os dois numeros ficam separados de
# proposito: a divisao e feita AQUI, e nao copiada de nenhum texto meu, porque
# foi copiar o resultado que me fez repetir "18,9" sem instrumento por tres dias.
REFERENCIA_DUR_S = 530.03
REFERENCIA_TRANSICOES = 28


def cadencia_da_referencia() -> float:
    """Os segundos por plano da peca do dono. DERIVADO, nunca escrito."""
    return REFERENCIA_DUR_S / REFERENCIA_TRANSICOES


def cadencia_s(cenas, voz: str) -> float:
    """Segundos por plano de uma lista de cenas, pela duracao ESTIMADA.

    Usa o mesmo `ensaio` que a mira e os portoes usam, para que nao existam
    duas contas da mesma coisa — o defeito de dois donos que congelou a legenda.
    """
    if not cenas:
        raise ValueError(
            "lista de cenas VAZIA: cadencia de nada nao e zero, e ausencia de "
            "leitura. O 739 nomeia isto — ausencia sai None ou levanta, nunca 0."
        )
    return ensaio.duracao_estimada(cenas, voz) / len(cenas)


def distancia_da_referencia(cenas, voz: str) -> float:
    """Quanto a peca esta ABAIXO da cadencia da referencia, em segundos.

    Positivo significa plano mais CURTO que o dela, que e o nosso caso em toda
    peca medida ate hoje.
    """
    return cadencia_da_referencia() - cadencia_s(cenas, voz)


def cenas_para_cadencia(total_s: float, alvo_s: float) -> int:
    """Quantas cenas uma duracao total pediria para bater uma cadencia.

    Esta e a conta que eu fazia de cabeca ao propor "o longo com 18,9 s por
    plano" sem nunca dizer quantas cenas isso da. Para 530 s sao 28; para os
    ~8 min que a maquina ja publica, 25 a 28.
    """
    if alvo_s <= 0:
        raise ValueError("cadencia alvo tem de ser positiva")
    return max(1, round(total_s / alvo_s))


def chars_por_cena_na_cadencia(voz: str, alvo_s: float) -> int:
    """Quantos caracteres uma cena precisa para DURAR a cadencia alvo.

    O ponto que a conta de cabeca escondia: cadencia longa nao se obtem tirando
    cenas, se obtem ESCREVENDO mais por cena. A sobrecarga e `P + 0,300` por
    FRASE e e por VOZ (11/10), logo o numero e por voz e nao da frota — o erro
    do 679/698 que eu ja cometi duas vezes.

    **E a conta NAO e feita aqui.** Ela e `ensaio.chars_por_cena(voz, 1, alvo_s)`
    — uma cena tem zero intervalos entre cenas, logo o caso n=1 daquela funcao e
    exatamente este. Refazer a aritmetica neste modulo criaria o SEGUNDO dono da
    mesma regra, que e a assinatura que congelou a legenda do short solto e que
    parou a mira de conferir por seis pecas. O dono e o `ensaio`.
    """
    if alvo_s <= 0:
        raise ValueError("cadencia alvo tem de ser positiva")
    return ensaio.chars_por_cena(voz, 1, alvo_s)


def relato(cenas, voz: str) -> str:
    ref = cadencia_da_referencia()
    nossa = cadencia_s(cenas, voz)
    d = ref - nossa
    chars = chars_por_cena_na_cadencia(voz, ref)
    linhas = [
        f"CADENCIA: {len(cenas)} cenas, {nossa:.1f} s por plano, "
        f"contra {ref:.1f} s da referencia ({REFERENCIA_DUR_S:.0f} s / "
        f"{REFERENCIA_TRANSICOES} transicoes, DERIVADO).",
        f"  distancia: {d:+.1f} s por plano.",
        f"  para a cadencia dela, a voz {voz} precisa de ~{chars} caracteres "
        f"por cena de UMA frase.",
        "  isto INFORMA e nao reprova: a referencia e UMA peca, feita a mao pelo "
        "dono, e o veredito dela e view, que nao medimos. Alvo e decisao do dono.",
    ]
    return "\n".join(linhas)


if __name__ == "__main__":
    import json
    import sys

    sp = json.load(open(sys.argv[1]))
    cenas = sp.get("longo") or sp.get("short") or []
    print(relato(cenas, sp["voz"]))
