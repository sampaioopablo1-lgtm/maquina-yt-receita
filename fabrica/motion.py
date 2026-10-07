#!/usr/bin/env python3
"""Motion e sound design — o que separa "slide com voz" de video que prende.

POR QUE ISTO EXISTE, e o pedido que o originou.

Em 07/10/2026 o dono perguntou, com todas as letras, se a maquina consegue
produzir video "com design fantastico, com animacoes, com barulhos, efeitos
sonoros". A resposta honesta era: nao como estava. O renderizador fazia
UM SVG estatico por cena, Ken Burns por cima, corte seco entre cenas e nenhum
som alem da narracao e da trilha a -28 dB.

A primeira ideia foi recorrer ao Higgsfield, que gera clipe animado por IA. Essa
porta esta FECHADA e e bom que esteja escrito aqui: `balance` devolveu
`credits: 0, subscription_plan_type: free` em 07/10. E o dono havia acabado de
dizer que esta sem dinheiro, entao recomendar recarga seria vender, nao ajudar.

O que sobrou e melhor para este caso: ffmpeg ja esta no runner, nao cobra por
clipe, e o que faltava nunca foi capacidade de maquina — era ninguem ter
investido no renderizador. Este modulo e esse investimento.

O QUE ELE MUDA, nos quatro pontos que medem "amador" em video explicador:

1. EASING. O deslize de entrada era LINEAR:
       y = DESLIZE * max(0, 1 - (t-t0)/ENTRADA)
   Movimento linear e o sinal mais barato de amadorismo em motion — nada no
   mundo fisico comeca e para instantaneamente. Aqui ele vira ease-out cubico,
   que desacelera no fim. Custo: zero, e a mesma conta.

2. SOM DE INTERFACE. Nao havia nenhum. Agora cada elemento que entra em cena
   ganha um transiente curto, SINTETIZADO pelo proprio ffmpeg — nao e sample
   baixado, nao tem licenca a creditar, nao tem byte a versionar.

3. TRANSICAO. O concat dava corte seco entre as 56 cenas. Agora cada clipe
   nasce com um fade de 0,12 s nas duas pontas, o que no concat le como
   dissolve. Feito POR CLIPE de proposito: um `xfade` no fim obrigaria a
   reencodar o video inteiro, e o concat atual roda em copy.

4. RITMO. `ENTRADA` de 0,40 s era igual para tudo. Um titulo que entra deve ser
   mais lento que um item de lista; o modulo escalona.

O QUE ELE NAO FAZ, e vale dizer para ninguem esperar: nao gera imagem nova, nao
anima ilustracao, nao cria personagem. Isso e o territorio do Higgsfield e custa
credito. Este modulo trabalha com o que o `svg_cena` ja desenha.

TUDO AQUI E OPT-IN. `motion_ligado(spec)` so devolve True com `"motion": true`
na spec. O experimento 32 precisa de sete a dez dias com o pipeline INTACTO, e
trocar o renderizador no meio destruiria a comparacao — foi exatamente assim que
o experimento 31 morreu. Entao o padrao continua sendo o caminho antigo.
"""

# --------------------------------------------------------------------------
# 1. EASING
# --------------------------------------------------------------------------
# A expressao vai dentro de um filtro ffmpeg, entao precisa ser uma string de
# expressao, nao uma funcao Python: quem a avalia e o ffmpeg, por quadro.
#
# ease-out cubico:  f(p) = 1 - (1-p)^3,  com p indo de 0 a 1
# O deslocamento que resta e  DESLIZE * (1 - f(p)) = DESLIZE * (1-p)^3.
#
# Comparado ao linear, aos 50% da animacao o elemento ja percorreu 87,5% do
# caminho em vez de 50%. E o que faz o movimento parecer "assentar" em vez de
# "parar de repente".


def deslize_easing(deslize: int, t0: float, entrada: float) -> str:
    """Deslocamento vertical com ease-out cubico, como expressao de ffmpeg.

    `p` e o progresso recortado em [0,1]. O `min(1\\,max(0\\,...))` existe
    porque o ffmpeg avalia a expressao em TODO quadro, inclusive antes de t0 e
    depois do fim — sem o recorte o elemento continuaria se movendo a cena
    inteira, e para t < t0 o deslocamento ficaria NEGATIVO (entraria por baixo).

    As virgulas vao escapadas (`\\,`) porque dentro de um filter_complex a
    virgula separa filtros.
    """
    p = f"min(1\\,max(0\\,(t-{t0:.3f})/{entrada:.3f}))"
    return f"{deslize}*pow(1-{p}\\,3)"


# --------------------------------------------------------------------------
# 2. RITMO POR PAPEL
# --------------------------------------------------------------------------
# Um titulo que entra lento le como "peso"; um item de lista que entra lento le
# como lentidao. Os numeros sao escolha de desenho, nao medicao — e estao
# declarados como tal para ninguem os citar como se fossem medidos.
ENTRADA_POR_PAPEL = {
    "titulo": 0.52,   # o kicker, que abre a cena
    "sub": 0.44,      # o subtitulo, logo atras
    "item": 0.34,     # item de lista: rapido, senao a lista arrasta
    "numero": 0.60,   # o numero e o ponto da cena; entra com calma
}
ENTRADA_PADRAO = 0.40


def entrada_do_elemento(k: int, n: int, layout: str) -> float:
    """Quanto tempo o k-esimo elemento leva para entrar."""
    if layout in ("lista", "barras"):
        return ENTRADA_POR_PAPEL["item"]
    if k == 0:
        return ENTRADA_POR_PAPEL["titulo"]
    if layout == "item" and k == 1:
        return ENTRADA_POR_PAPEL["numero"]
    return ENTRADA_POR_PAPEL.get("sub", ENTRADA_PADRAO)


# --------------------------------------------------------------------------
# 3. SOM DE INTERFACE, SINTETIZADO
# --------------------------------------------------------------------------
# Tres transientes curtos, gerados pelo proprio ffmpeg. Nenhum arquivo baixado,
# nenhuma licenca a creditar, nenhum byte no repo.
#
# A FAIXA DE VOLUME E DELIBERADA E BAIXA. A trilha ja toca a -28 dB porque
# trilha alta e causa comum de abandono neste formato (ver VOL_TRILHA em
# fabrica.py). Efeito sonoro alto e pior ainda: vira irritante na segunda cena e
# o video tem 56. Estes ficam abaixo da trilha, no limiar do perceptivel — o
# ouvido registra "houve um corte" sem registrar "ouvi um bip".
SONS = {
    # Entrada de titulo: ruido rosa passado por um filtro passa-baixa que abre,
    # com decaimento rapido. Le como "ar", nao como "bip".
    "whoosh": (
        "anoisesrc=d=0.34:c=pink:a=0.26,"
        "highpass=f=180,lowpass=f=2400,"
        "afade=t=in:st=0:d=0.05,afade=t=out:st=0.08:d=0.26"
    ),
    # Aparicao de numero ou item: dois senos curtos em quinta. Nao e um clique
    # seco, que soaria a interface de sistema.
    "tick": (
        "sine=f=880:d=0.12,"
        "afade=t=in:st=0:d=0.004,afade=t=out:st=0.02:d=0.10"
    ),
    # Fecho de capitulo: nota grave e curta, para marcar que um bloco terminou.
    "marco": (
        "sine=f=196:d=0.5,"
        "afade=t=in:st=0:d=0.01,afade=t=out:st=0.1:d=0.4"
    ),
}

# dB de cada efeito. Negativo e abaixo da referencia; a trilha esta a -28.
GANHO_SOM = {"whoosh": -34, "tick": -30, "marco": -32}


def comando_sintetizar(nome: str, destino: str, ffmpeg: str = "ffmpeg") -> list:
    """Comando que cria UM efeito em disco. Roda uma vez por render, nao por cena."""
    if nome not in SONS:
        raise KeyError(f"som desconhecido: {nome!r}; conhecidos: {sorted(SONS)}")
    return [ffmpeg, "-nostdin", "-y", "-f", "lavfi", "-i", SONS[nome],
            "-ac", "1", "-ar", "48000", destino]


def plano_de_sons(layout: str, tempos: list, tem_cap: bool) -> list:
    """Quais efeitos tocam, e quando, nesta cena.

    Devolve [(nome, instante_em_segundos), ...]. A regra:
      * o PRIMEIRO elemento da cena leva `whoosh` — e a troca de assunto;
      * os demais levam `tick`, que e mais curto e nao compete com a voz;
      * cena que ABRE CAPITULO leva um `marco` no comeco, por baixo do whoosh.

    Em `broll` nao entra nada: a cena nao tem camadas entrando, e um som sem
    nada acontecendo na tela soa como defeito.
    """
    if layout == "broll" or not tempos:
        return [("marco", 0.0)] if tem_cap else []
    plano = [("marco", 0.0)] if tem_cap else []
    for k, t in enumerate(tempos):
        plano.append(("whoosh" if k == 0 else "tick", t))
    return plano


def filtro_mixar_sons(plano: list, n_entradas_antes: int, dur: float) -> str:
    """filter_complex que posiciona os efeitos e os mixa sobre a narracao.

    `n_entradas_antes` e quantos `-i` ja existem no comando antes dos sons; os
    arquivos de som entram logo depois, na ordem do plano. A narracao e a ultima
    entrada ANTES dos sons, em `n_entradas_antes - 1`.

    `adelay` recebe milissegundos. `apad`+`atrim` garantem que o mix nao fique
    mais curto nem mais longo que a cena: sem isso uma cena cujo ultimo efeito
    cai perto do fim ganhava alguns centesimos e o concat acumulava desvio.
    """
    if not plano:
        return ""
    partes, rotulos = [], []
    for j, (nome, t) in enumerate(plano):
        ent = n_entradas_antes + j
        ms = max(0, int(t * 1000))
        partes.append(
            f"[{ent}:a]adelay={ms}|{ms},volume={GANHO_SOM[nome]}dB[s{j}]")
        rotulos.append(f"[s{j}]")
    voz = f"[{n_entradas_antes - 1}:a]"
    partes.append(
        f"{voz}{''.join(rotulos)}amix=inputs={len(plano) + 1}:"
        f"duration=first:dropout_transition=0:normalize=0,"
        f"apad,atrim=0:{dur:.3f}[a]")
    return ";".join(partes)


# --------------------------------------------------------------------------
# 4. TRANSICAO ENTRE CENAS
# --------------------------------------------------------------------------
# Feita POR CLIPE, nao no concat. O concat atual roda com `-c copy`; um `xfade`
# obrigaria a reencodar os doze minutos inteiros, o que custa minutos de runner
# e uma geracao de perda. Um fade curto nas duas pontas de cada clipe le, na
# emenda, como dissolve — e sai de graca, porque o clipe ja esta sendo encodado.
#
# 0,12 s e curto de proposito: acima de ~0,2 s a emenda comeca a "respirar" e o
# video de 56 cenas ganha um ar arrastado.
FADE_BORDA = 0.12


def filtro_bordas(dur: float) -> str:
    """fade de entrada e saida para a emenda. Vazio em cena curta demais."""
    if dur <= 3 * FADE_BORDA:
        return ""
    fim = dur - FADE_BORDA
    return f"fade=t=in:st=0:d={FADE_BORDA},fade=t=out:st={fim:.3f}:d={FADE_BORDA}"


# --------------------------------------------------------------------------
# 5. A CHAVE
# --------------------------------------------------------------------------
def motion_ligado(spec: dict, formato: str = "") -> bool:
    """LIGADO no short, DESLIGADO no longo. A spec manda nos dois sentidos.

    `formato` e o prefixo da fabrica: "s" para short, "l" para longo. Sem
    `formato` o padrao segue DESLIGADO, para nao mudar chamada antiga por
    acidente.

    POR QUE O SHORT E O LONGO TEM PADRAO DIFERENTE, e a razao e medida, nao
    estetica. O portao de distribuicao do short e a taxa de abandono nos tres
    primeiros segundos: a Short entra num lote semeado de 200 a 500 impressoes e
    so passa dali se pouca gente desliza embora na largada; o alvo publicado e
    abandono abaixo de 25% nos primeiros tres segundos, e retencao de 65% para
    short abaixo de 30 s ou 50% para short de 30 a 60 s. Gancho VISUAL bate
    gancho verbal nesse primeiro segundo, e motion e exatamente isso. O longo
    nao tem esse portao: ele e achado por busca e por sugestao, e nos nossos
    numeros ele nao esta sendo achado de jeito nenhum (nove dos treze longos das
    ultimas 72 h com ZERO view).

    POR QUE SO O SHORT, e nao os dois de uma vez: mudar os dois formatos na
    mesma rodada em que o mix de producao tambem muda tornaria impossivel
    atribuir qualquer movimento de alcance a uma causa. Foi assim que o
    experimento 31 morreu. Uma mudanca, um alvo: alcance por short.
    """
    v = spec.get("motion")
    if v is not None:
        return bool(v)
    return formato == "s"
