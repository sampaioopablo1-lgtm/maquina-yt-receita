"""O video de 8 min da REFERENCIA, medido QUADRO POR QUADRO.

Pedido do dono em 16/10: *"Preciso que entenda o video publicado de 8 min do
canal labtreinamento frame por frame."*

A peca e `FtCtIJPsc_Q` (PROCV ou PROCX: qual usar no Excel (e quando)), o longo
MAIS NOVO do canal — rank 1 na ordem viva de uploads, e a mesma peca a que o
dono apontou quando disse que as producoes estavam *"muito distantes"* dela.

A ROTA VOLTOU, E ISSO E ESTADO E NAO PROPRIEDADE
------------------------------------------------
Em 16/10 as 11:xx o `yt-dlp` deu **403 em quatro player clients** com
*"Only images are available for download"*, e eu relatei ao dono que os efeitos
NAO estavam medidos em vez de inventar analise. Uma hora depois, no MESMO
sandbox, o `--list-formats` devolveu a **lista inteira** (144p a 1080p, audio,
HLS e DASH) e o formato 134 baixou 3,85 MiB em menos de um segundo.

E a licao e a tabela do proprio `CLAUDE.md`: a rota da duracao e a da legenda
fecharam e reabriram no mesmo dia. **Sonde antes de dizer que nao ha rota** — e,
do outro lado, nao prometa a rota porque ela abriu uma vez.

O QUE FOI MEDIDO (ffprobe + ffmpeg, formato 134, 640x360 30 fps)
----------------------------------------------------------------
    duracao real        530,03 s   (contra 531 s de `narracao_referencia`)
    quadros             ~15.900
    transicoes          28  (scene > 0,04)  ->  **18,9 s por plano**
    transicoes duras    **ZERO** (nada acima de scene 0,15)
    diferenca mediana   **0,072**  (metodo do 690/699: fps=10, tblend, signalstats)
    quadros congelados  **96%** (5.098 de 5.298 abaixo de 1,0)
    YAVG                mediana 37,3  (min 31,0  max 45,6)
    frames claros       **0 de 530** (nenhum YAVG > 180)
    SATAVG              3,4 a 5,6  -> praticamente MONOCROMATICO

**E ISTO DERRUBA A PERGUNTA DO DONO SOBRE "EFEITOS", no sentido oposto ao que eu
esperava.** Na MESMA escala absoluta de 0-255 e no MESMO metodo:

    peca                                      mediana   congelados
    REFERENCIA (este longo de 8 min)            0,072       96%
    `labtreinamento-s011` (o defeito do 690)    0,39        91%
    `kolejny-poziom-s017` (depois do 699)       0,63        73%

A referencia e **cinco vezes mais estatica** que a nossa peca pior e **nove
vezes** mais que a nossa peca consertada. Logo o que o dono percebe como
distancia **nao e efeito, nem dinamismo, nem movimento** — nos temos MAIS disso
que a referencia. Confundidor declarado: a referencia e um LONGO de 8 min e as
duas nossas sao SHORTS de ~40 s, e a referencia foi medida num reencode 360p.
O que o reencode NAO explica e o sinal: compressao nao transforma 0,63 em 0,072.

A ESTRUTURA, LIDA POR OCR DE 18 QUADROS (um a cada 30 s)
--------------------------------------------------------
    t=0     capa: "CONFIRA A SUA PLANILHA / SEU PROCV TEM TRES ARGUMENTOS"
    t=30    cartao de prova social: "SE ESTA CURTINDO / Inscrito / Curtido"
    t=60    "ATENCAO": quarto argumento vazio = busca aproximada
    t=90    "UM EXEMPLO": lista de 3 passos numerados
    t=120   comparacao DUAS COLUNAS: "x SEM O QUARTO ARGUMENTO" / "v COM FALSO"
    t=150   divisor de parte: "PARTE 2 / OS TRES LIMITES DO PROCV"
    t=180   "LIMITE 2": o PROCV so olha para a direita
    t=210   cartao de erro: "#REF!" e quando ele aparece
    t=240   cartao de NUMERO GRANDE: "2019"
    t=270   formula + os argumentos ANOTADOS um por um
    t=300   uma frase so: "No PROCV voce conta colunas. No PROCX voce le a formula."
    t=330   formula com o 4o argumento e os dois ramos (achou / nao achou)
    t=360   "QUINTO ARGUMENTO DO PROCX": voce escolhe o tipo de busca
    t=420   "O QUE CONTA": a versao de quem ABRE o arquivo
    t=450   "A REGRA PRATICA": versao recente -> use PROCX
    t=480   fechamento: "O PROCV nao e uma funcao ruim."
    t=510   "PROXIMO VIDEO" + "INSCREVA-SE"

**TRES COISAS QUE A REFERENCIA TEM E NOS NAO TEMOS, e sao elas a distancia:**

1. **UM TRILHO DE CAPITULOS PERMANENTE NO TOPO.** De t=240 em diante todo quadro
   carrega `1 A armadilha | 2 Os tres limites | 3 O que o PROCX muda |
   4 Quando usar cada um`, com o capitulo corrente destacado. **E por isso que
   nenhuma transicao passa de scene 0,15**: o trilho e a marca d'agua nao mudam,
   so o painel central troca. O espectador sempre sabe onde esta.
2. **18,9 s POR PLANO.** A nossa cadencia e **3,1 s** (medida em 690/699 e no
   `labtreinamento-s058`). Seis vezes mais tempo por tela e o que da espaco para
   uma formula anotada argumento por argumento — que em 3 s nao cabe.
3. **LAYOUTS QUE NOS NAO TEMOS NO `layout.py`**: formula com argumentos anotados,
   comparacao de duas colunas com x/v, cartao de erro (`#REF!`, `#N/D`),
   divisor de PARTE, e o cartao de numero grande.

**E TRES QUE ELA NAO TEM:** zero b-roll, zero fotografia, zero rosto. O mundo
visual e o MESMO que o nosso — painel escuro com texto — e isso e a parte boa da
medicao: a identidade nao precisa mudar.

A CONSEQUENCIA, E ELA CAI NA METADE NAO COMECADA DO PEDIDO DE 16/10
-------------------------------------------------------------------
O dono pediu *"1 video longo e outro curto"* por canal por dia. **A referencia e
um LONGO**, e os tres itens acima sao de longo: 18,9 s por plano nao existe em
short, e trilho de capitulo num 9:16 de 40 s nao tem onde morar. Logo isto NAO e
instrucao para mexer no short — mexer no `ALVO_SHORT` ou na cadencia seria a
trava da §10 — e **e** a especificacao do longo novo, que e o que ainda nao saiu.

NADA de parametro mudou nesta rodada. O que fica e MEDICAO.
"""

# Medido em 16/10/2026 no sandbox do Composio, formato 134 (640x360, 30 fps).
ID = "FtCtIJPsc_Q"
CANAL = "labtreinamento"
DURACAO_S = 530.03

# Metodo do 690/699: fps=10, tblend=all_mode=difference, signalstats, escala 0-255.
DINAMISMO = {
    "mediana": 0.072,
    "media": 0.246,
    "p90": 0.37,
    "maximo": 13.78,
    "amostras": 5298,
    "congelados": 5098,  # abaixo de 1,0
}

# As duas pecas NOSSAS medidas com o MESMO metodo, para comparacao honesta.
# Confundidor: as duas sao SHORTS de ~40 s; a referencia e um LONGO de 8 min.
NOSSAS = {
    "labtreinamento-s011": {"mediana": 0.39, "congelados_frac": 0.91},
    "kolejny-poziom-s017": {"mediana": 0.63, "congelados_frac": 0.73},
}

TRANSICOES_S = [
    2.5, 5.13, 5.17, 19.73, 37.7, 48.33, 92.03, 117.0, 135.87, 159.53,
    172.6, 196.7, 222.43, 232.17, 251.3, 262.7, 286.3, 308.1, 365.07,
    389.37, 400.77, 425.2, 439.97, 450.87, 473.63, 493.5, 499.83, 508.53,
]
TRANSICOES_DURAS = 0  # nada acima de scene 0,15 — o trilho nunca sai da tela

LUMINANCIA = {"yavg_mediana": 37.3, "yavg_min": 31.0, "yavg_max": 45.6}
SATURACAO = (3.44, 5.63)  # SATAVG min/max -> praticamente monocromatico

# O trilho permanente, lido por OCR a partir de t=240 s.
TRILHO = [
    "1 A armadilha",
    "2 Os tres limites",
    "3 O que o PROCX muda",
    "4 Quando usar cada um",
]
MARCA_DAGUA = "LABTREINAMENTO"  # presente em TODOS os 18 quadros amostrados

# Os layouts que a referencia usa e que o nosso `layout.py` NAO tem.
LAYOUTS_QUE_FALTAM = (
    "formula_anotada",   # a formula e, abaixo, cada argumento nomeado
    "duas_colunas",      # x errado / v certo, lado a lado
    "cartao_de_erro",    # #REF!, #N/D
    "divisor_de_parte",  # "PARTE 2 / titulo da parte"
    "numero_grande",     # "2019"
)

# O que a referencia NAO usa — e isso autoriza nao mexer na identidade.
AUSENTES = ("b-roll", "fotografia", "rosto", "fundo claro", "cor saturada")


def cadencia_s() -> float:
    """Segundos por plano, pelas transicoes medidas."""
    return round(DURACAO_S / len(TRANSICOES_S), 1)


def mais_estatica_que(peca: str) -> float:
    """Quantas vezes a REFERENCIA e mais estatica que uma peca nossa.

    Levanta para peca nao medida, em vez de devolver numero inventado.
    """
    if peca not in NOSSAS:
        raise KeyError(
            f"{peca} nao foi medida com o metodo do 690/699; "
            f"medidas: {sorted(NOSSAS)}"
        )
    return round(NOSSAS[peca]["mediana"] / DINAMISMO["mediana"], 1)


def relato() -> str:
    linhas = [
        f"REFERENCIA {ID} ({CANAL}) — {DURACAO_S:.0f} s, medido quadro a quadro",
        f"  cadencia .......... {cadencia_s()} s por plano "
        f"({len(TRANSICOES_S)} transicoes, {TRANSICOES_DURAS} duras)",
        f"  dinamismo ......... mediana {DINAMISMO['mediana']}, "
        f"{100 * DINAMISMO['congelados'] // DINAMISMO['amostras']}% congelados",
        f"  luminancia ........ YAVG {LUMINANCIA['yavg_mediana']} "
        f"(nenhum quadro claro)",
        f"  saturacao ......... {SATURACAO[0]} a {SATURACAO[1]} — monocromatico",
    ]
    for peca in sorted(NOSSAS):
        linhas.append(
            f"  contra {peca}: a referencia e {mais_estatica_que(peca)}x "
            f"MAIS estatica que a nossa peca"
        )
    linhas += [
        "  trilho permanente . " + " | ".join(TRILHO),
        "  layouts que faltam  " + ", ".join(LAYOUTS_QUE_FALTAM),
        "",
        "  A distancia NAO e efeito — nos temos mais movimento que ela.",
        "  E trilho de capitulo, 18,9 s por plano e layouts de formula,",
        "  e as tres coisas sao de LONGO, nao de short.",
    ]
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relato())
