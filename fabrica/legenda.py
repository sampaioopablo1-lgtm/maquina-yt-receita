#!/usr/bin/env python3
"""A legenda queimada do short, em pedaços — e por que ela estava congelada.

POR QUE ESTE ARQUIVO EXISTE (09/10/2026). O dono disse: "tenho achado as
imagens, frames dos vídeos muito estáticos". Medi, e ele está certo com folga.

MEDIDO no `labtreinamento-s011` (41,6 s, o short publicado às 11:20), com
`tblend=all_mode=difference,signalstats` a 10 fps:

    diferença mediana entre quadros consecutivos   0,39   (escala 0-255)
    quadros com diferença < 1,0                    375 de 414 = 91%

Noventa e um por cento dos quadros estão praticamente congelados. A média de
4,34 é inteiramente puxada pelos CINCO cortes de cena (máximo 203). O vídeo é
uma sequência de cinco cartazes quase imóveis.

Três causas, e esta é a maior delas: **a legenda queimada era UMA fala só para a
cena INTEIRA**. O `fabrica.py` escrevia

    1
    00:00:00,200 --> 00:00:08,350
    <a frase inteira, ~110 caracteres>

ou seja ~18 a 20 palavras paradas na tela por oito segundos. O texto é a região
que o olho lê, e era justamente ela que nunca mudava. As outras duas causas são
o Ken Burns de ~7% em 8 s (abaixo do limiar perceptível) e o quadro preto em
t=0, e vão tratadas no `fabrica.py`.

O QUE ESTE MÓDULO NÃO É: não é "copiar o que viraliza". Eu procurei na web o que
o dono pediu e o que voltou foi blog de fornecedor de ferramenta de legenda, sem
teste controlado e com números que se contradizem — a própria rotina avisa que
busca na web para tendência devolve SEO. O único número externo que eu aproveito
daí é um limite de forma que aparece repetido e é coerente com a medição:
**quatro a cinco palavras na tela por vez** em vídeo vertical, acima disso o
espectador lê em vez de absorver. Nós estávamos em dezoito.

O instrumento que não mente, `chart=mostPopular` (categoria 26, e isso é PROXY,
aprendizado 610), diz outra coisa que importa: o que realmente tem milhões de
views dura **10 a 35 s** — mediana 26 s no BR, 35 no PL, 30 no GR, lido em
09/10/2026. Os nossos estão em 41-42 s porque EU os empurrei para lá nesta
semana (experimento 38). Isso NÃO vira mudança aqui: o 38 ainda não tem leitura
de 12 h, e trocar duração junto com legenda tornaria as duas imensuráveis.
"""
from __future__ import annotations

MAX_PALAVRAS = 4   # limite de forma; ver docstring
MIN_S = 0.45       # fala mais curta que isto pisca e cansa
FOLGA_FIM = 0.15   # o mesmo recuo que a versao de uma fala usava


def _marca(t: float) -> str:
    if t < 0:
        t = 0.0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def pedacos(nar: str, maximo: int = MAX_PALAVRAS) -> list[str]:
    """Quebra a narração em grupos de até `maximo` palavras.

    Quebra em PALAVRA, nunca em caractere: cortar palavra ao meio na tela é
    pior que texto parado. Pontuação fica colada na palavra que a precede, e é
    por isso que um grupo pode terminar em vírgula — o olho usa isso de pausa.
    """
    palavras = (nar or "").split()
    if not palavras:
        return []
    return [" ".join(palavras[i:i + maximo])
            for i in range(0, len(palavras), maximo)]


def srt(nar: str, duracao: float, inicio: float = 0.2,
        maximo: int = MAX_PALAVRAS) -> str:
    """O SRT da cena, uma fala por grupo de palavras.

    O tempo de cada grupo é proporcional ao seu número de CARACTERES, não ao de
    palavras: "e" e "antecedência" não se leem no mesmo tempo, e dividir igual
    fazia o grupo longo sumir antes de ser lido. É uma aproximação da fala, não
    um alinhamento de verdade — alinhamento real precisa de reconhecimento de
    fala, que está fora desta etapa.

    A última fala termina `FOLGA_FIM` antes do fim da cena, como a versão
    anterior fazia, porque a cena tem folga depois do áudio e legenda pendurada
    no corte lê como defeito.
    """
    gs = pedacos(nar, maximo)
    if not gs:
        return ""
    fim = max(duracao - FOLGA_FIM, inicio + MIN_S)
    total = fim - inicio
    pesos = [max(len(g), 1) for g in gs]
    soma = sum(pesos)

    # Reparte o tempo e depois GARANTE o minimo, tirando do maior. Sem isso uma
    # frase de muitas palavras numa cena curta dava falas de 0,1 s — pisca-pisca
    # ilegivel, que e trocar um defeito por outro.
    duracoes = [total * p / soma for p in pesos]
    for i, d in enumerate(duracoes):
        if d < MIN_S:
            falta = MIN_S - d
            duracoes[i] = MIN_S
            j = max(range(len(duracoes)), key=lambda k: duracoes[k])
            if j != i and duracoes[j] - falta >= MIN_S:
                duracoes[j] -= falta

    # Se nem assim cabe, a cena e curta demais para N grupos: junta tudo em
    # menos grupos em vez de entregar legenda ilegivel.
    if sum(duracoes) > total + 1e-6 and maximo < 12:
        return srt(nar, duracao, inicio, maximo + 2)

    linhas, t = [], inicio
    for i, (g, d) in enumerate(zip(gs, duracoes), start=1):
        linhas.append(f"{i}\n{_marca(t)} --> {_marca(t + d)}\n{g}\n")
        t += d
    return "\n".join(linhas)
