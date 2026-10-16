"""O ritmo da narracao da REFERENCIA, e o fator do botao de velocidade.

Pedido do dono em 16/10: *"Qualidade da nova producao, efeitos, narracao,
preciso replicar para todos os canais"*.

A referencia e o ultimo video do canal `labtreinamento` — `FtCtIJPsc_Q`
(PROCV ou PROCX), 531 s. Medido pela legenda que a propria maquina subiu:
1.381 palavras, 7.425 chars, **109 frases**.

    ritmo EFETIVO      13,98 chars/s  (156 palavras/min)
    frase              12,7 palavras, 4,9 s

E AQUI EU ERREI UM NUMERO E O CORRIJO NO LUGAR: eu disse ao dono que a nossa
narracao era "25% mais rapida", comparando esse 13,98 com o `R = 17,47` de
`MODELO_VOZ`. **Sao quantidades diferentes** — o `R` e taxa de FALA, e o 13,98 e
taxa EFETIVA, com as pausas de fim de frase dentro. E a classe de erro do 711:
comparar o real contra um modelo que mede outra coisa.

Medido como-por-como, sintetizando texto real de cada canal (cinco a seis frases,
logo com as pausas dentro, igual a referencia):

    voz                      R efetivo @ rate -4%
    pt-BR-Francisca*               14,87
    el-GR-Nestoras                 14,41
    pl-PL-Marek                    12,86

**Logo a nossa narracao JA esta no ritmo da referencia** — 14,87 contra 13,98 e
+6%, dentro do ruido de uma amostra de cinco frases. O que difere de verdade e o
TAMANHO DA FRASE: 12,7 palavras na referencia contra ~5 nas nossas, e isso e
escolha de FORMATO (a cadencia de ~3 s por plano que o 690/699 mediu como a
alavanca do dinamismo), nao defeito.

(*) A `pt-BR-ThalitaMultilingualNeural` **devolveu ZERO audio** no sandbox, em
duas tentativas, com e sem `rate`, enquanto a `Francisca` sintetizou na mesma
chamada — por isso ela entrou como proxy do pt-BR, e isso vai declarado em vez
de escondido. E e consistente com o run MISTO do `labtreinamento-s060` (dois
avisos de Piper em dez cenas): a voz Multilingual e a fragil da lista. NAO
concluo que ela esta quebrada no runner — em quase todas as pecas do canal ela
narrou com zero avisos, logo isto e ESTADO e nao propriedade.

O FATOR DO BOTAO, que e o resultado reusavel: `fabrica.py:599` chama o edge-tts
com `rate="-4%"`, e descer para `-23%` multiplica o ritmo por

    0,803  (pt-BR)   0,802  (el-GR)   0,802  (pl-PL)

— **0,802 nas tres vozes, com tres decimais de acordo**, logo o botao e
independente de voz. Qualquer mudanca de `rate` escala o `R` por esse fator, e
`ensaio.chars_por_cena` recalcula o resto sozinho.

**O QUE ISTO NAO AUTORIZA:** mexer no `rate` hoje. Descer para -23% alongaria
cada peca em ~25% — um short de 41,9 s previstos iria a ~52 s, fora do teto de
45 do portao e fora da faixa em que o YouTube trata a peca como Short, que e o
unico caminho de monetizacao vivo. Para manter a duracao seria preciso cortar
~20% dos caracteres por cena. **E, medido acima, nao ha motivo: o ritmo ja bate
com a referencia.** Fica registrado para quando a decisao for de FORMATO.
"""

# Referencia medida (legenda de `FtCtIJPsc_Q`, 531 s).
REFERENCIA = {
    "id": "FtCtIJPsc_Q",
    "segundos": 531.0,
    "palavras": 1381,
    "chars": 7425,
    "frases": 109,
}

# Ritmo efetivo medido por voz com `rate="-4%"`, em chars/s, sobre texto real
# de cinco a seis frases (as pausas de fim de frase estao dentro).
RITMO_EFETIVO = {
    "pt-BR-FranciscaNeural": 14.87,     # proxy: a Thalita nao sintetizou
    "el-GR-NestorasNeural": 14.41,
    "pl-PL-MarekNeural": 12.86,
}

# Fator medido ao trocar `rate` de -4% para -23%, nas tres vozes.
FATOR_RATE_4_PARA_23 = {
    "pt-BR-FranciscaNeural": 0.803,
    "el-GR-NestorasNeural": 0.802,
    "pl-PL-MarekNeural": 0.802,
}

RATE_EM_PRODUCAO = "-4%"


def ritmo_da_referencia() -> float:
    """chars/s EFETIVOS da referencia — com as pausas dentro."""
    return REFERENCIA["chars"] / REFERENCIA["segundos"]


def palavras_por_frase_da_referencia() -> float:
    return REFERENCIA["palavras"] / REFERENCIA["frases"]


def desvio_do_ritmo(voz: str) -> float | None:
    """Quanto a voz corre acima (+) ou abaixo (-) da referencia, em fracao."""
    r = RITMO_EFETIVO.get(voz)
    return None if r is None else r / ritmo_da_referencia() - 1.0


def fator_do_rate(de: str = "-4%", para: str = "-23%") -> float:
    """O fator MEDIDO, e ele recusa par que nao foi medido.

    Interpolar entre rates nao medidos seria inventar numero — o 679/698 em
    forma de velocidade.
    """
    if (de, para) != ("-4%", "-23%"):
        raise ValueError(
            f"fator de {de} para {para} NAO foi medido; o unico par medido e"
            " -4% -> -23% (0,802 nas tres vozes). Meca antes de usar."
        )
    vals = list(FATOR_RATE_4_PARA_23.values())
    return sum(vals) / len(vals)
