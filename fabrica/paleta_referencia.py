"""A paleta do `labtreinamento` DERIVADA do longo da referencia, nao inventada.

POR QUE (19/10/2026). O dono olhou a peca de 5 s publicada e disse: *"Video
postado nao tem nada a ver com ultimo video e estilo do video de 8 min
publicado."* Ele esta certo, e o numero que prova isso e MEU.

Em 16/10 eu medi o longo da referencia (`FtCtIJPsc_Q`, o PROCV de 8:51, que e
peca do PROPRIO DONO) quadro a quadro e gravei no `video_referencia.py`:

    YAVG mediana        37,3   (min 31,0  max 45,6)
    quadros claros      0 de 530   (nenhum YAVG > 180)
    SATAVG              3,4 a 5,6  -> praticamente MONOCROMATICO
    AUSENTES            (..., "fundo claro", "cor saturada")

E na mesma sessao eu escrevi, em letra: *"O mundo visual dela e o nosso — logo
a identidade por canal (601) nao muda."*

**As duas frases nao cabem juntas.** A paleta que a frota usava no
`labtreinamento` tem fundo `#F6F4EF`, cuja luminancia e **244** — isto e, ela e
"quadro claro" pelo limiar de 180 que eu mesmo usei, e 6,5x a mediana da
referencia. E o acento `#E9C46A` e "cor saturada". **A minha lista de AUSENTES
nomeava exatamente as duas coisas que as nossas pecas SAO**, e eu li a lista
como autorizacao para nao mexer. Era o contrario.

DE ONDE VEM A PALETA NOVA — e ela e medicao, nao gosto:

  * o FUNDO mira a mediana de luminancia dos quadros da referencia (37,3) e o
    chroma dentro da faixa dela (3,4 a 5,6);
  * as cores saem da CAPA da referencia, lida em 19/10 as 01:0x
    (`i.ytimg.com/vi/FtCtIJPsc_Q/maxresdefault.jpg`, 1280x720, HTTP 200),
    quantizada em 160x90: as dominantes sao `#546C6C` (11,6%), `#3C5454`
    (10,7%), `#0C0C24` (8,7%), `#242424` (5,6%) e um acento ciano `#3CE4E4`
    (4,4%). Mediana de luminancia da capa: **69,2**, com **2,2%** de pixels
    claros.

**O que isto NAO e, e vai dito:** nao e a paleta dos QUADROS lida ao vivo. A
rota do video (`yt-dlp -f 160/18`) devolveu **403 Forbidden** nesta rodada —
estado de rota, o mesmo de 16/10 as 03:3x, que reabriu uma hora depois. Logo a
LUMINANCIA vem da medicao de 16/10 (quadros) e as CORES da capa de hoje. As
duas fontes vao nomeadas em vez de misturadas num numero so.

**E o que ela NAO conserta:** a distancia que eu medi em 16/10 tinha TRES
partes, e cor nao e nenhuma delas. Faltam o trilho de capitulos permanente, os
18,9 s por plano e os cinco layouts que o `layout.py` nao tem. Isto aqui
aproxima o MUNDO VISUAL; a ESTRUTURA continua sendo construcao, e ela e de
LONGO.
"""

# Medido no `video_referencia.py` (16/10, quadros) — o alvo do fundo.
ALVO_LUMA_FUNDO = 37.3
ALVO_CHROMA = (3.4, 5.6)

# Dominantes da CAPA (19/10), na ordem de frequencia.
CAPA_DOMINANTES = ("#546C6C", "#3C5454", "#0C0C24", "#3C2424", "#242424",
                   "#0C0C0C", "#3C3C54", "#3CE4E4")
CAPA_LUMA_MEDIANA = 69.2
CAPA_FRACAO_CLARA = 2.2  # % de pixels com Y > 180

# A FONTE VERDADEIRA, achada em 19/10 as 01:3x: o dono disse "assista o video e
# como foi produzido, LOCALMENTE (Meu PC)", e o elo era o ZIP que ele mesmo
# mandou. O `pipeline_canal_dark_v1.2.zip` chegou em 12/10; o longo foi
# publicado em 14/10. O `motor/config.py` do pacote traz quatro temas prontos, e
# o `noite` e descrito como *"Escuro azulado com destaque turquesa"* — que e
# exatamente o que eu medi na capa.
#
# **ISTO VALIDA A MEDICAO E A SUBSTITUI.** Eu havia derivado o acento como
# `#3CE4E4` lendo a capa comprimida; o valor REAL do tema e `#3DDBD9`. A
# distancia e de quantizacao de JPEG, logo a leitura estava certa — mas usar o
# valor do arquivo do dono e melhor que usar a minha reconstrucao dele.
TEMA_DO_DONO = "noite"
CORES_DO_TEMA = {  # motor/config.py do pipeline, tema `noite`, copiado sem mudar
    "bg": "#0E1117", "panel": "#161B24", "panel2": "#1E2430", "line": "#2C3442",
    "txt": "#EEF1F5", "txt2": "#C9D1DC", "mut": "#8B95A5",
    "acc": "#3DDBD9", "acc2": "#F5A524", "red": "#FF5A5F", "ok": "#3CCB7F",
}
FONTES_DO_TEMA = ("Anton", "Inter")  # titulo, texto — e `maiusculas=True`

# O nosso render tem QUATRO campos; o tema dele tem onze. O mapeamento vai
# escrito porque ele e escolha e nao traducao automatica.
PALETA = {
    "bg":  CORES_DO_TEMA["bg"],      # o fundo dele, sem mudar
    "ink": CORES_DO_TEMA["txt"],     # o texto dele, sem mudar
    "c1":  CORES_DO_TEMA["acc"],     # o turquesa de destaque, sem mudar
    "c2":  CORES_DO_TEMA["panel2"],  # ESCOLHA: o nosso `c2` preenche forma, e
                                     # no video dele forma e PAINEL, nao acento.
                                     # `acc2` (#F5A524) existe no tema e ficou de
                                     # fora de proposito: ele e laranja saturado
                                     # e romperia o SATAVG medido nos quadros.
}

# A que a frota usava, guardada para a comparacao nao depender de memoria.
PALETA_ANTIGA = {"ink": "#14213D", "c1": "#2A9D8F", "c2": "#E9C46A", "bg": "#F6F4EF"}

LIMIAR_QUADRO_CLARO = 180  # o mesmo que o `video_referencia` usou


def luma(hexa: str) -> float:
    h = (hexa or "#000000").lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


def chroma(hexa: str) -> float:
    """Distancia do cinza em UV — a mesma grandeza do SATAVG do signalstats."""
    h = (hexa or "#000000").lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    u = -0.169 * r - 0.331 * g + 0.5 * b
    v = 0.5 * r - 0.419 * g - 0.081 * b
    return (u * u + v * v) ** 0.5


def e_quadro_claro(hexa: str) -> bool:
    return luma(hexa) > LIMIAR_QUADRO_CLARO


def relato() -> str:
    fora = []
    fora.append("PALETA do labtreinamento, derivada do longo da referencia:")
    for k in ("bg", "ink", "c1", "c2"):
        fora.append(f"  {k:4s} {PALETA[k]}  Y={luma(PALETA[k]):6.1f}  "
                    f"chroma={chroma(PALETA[k]):5.2f}")
    fora.append(f"  alvo do fundo: Y~{ALVO_LUMA_FUNDO} e chroma em "
                f"{ALVO_CHROMA[0]} a {ALVO_CHROMA[1]} (medido nos quadros em 16/10)")
    fora.append(f"  a ANTIGA tinha fundo Y={luma(PALETA_ANTIGA['bg']):.1f}, isto e "
                f"QUADRO CLARO pelo limiar de {LIMIAR_QUADRO_CLARO} — "
                f"{luma(PALETA_ANTIGA['bg']) / ALVO_LUMA_FUNDO:.1f}x a mediana dela")
    fora.append("  e isto NAO fecha a distancia: trilho de capitulos, 18,9 s por "
                "plano e os cinco layouts continuam faltando, e sao de LONGO.")
    return "\n".join(fora)


if __name__ == "__main__":
    print(relato())
