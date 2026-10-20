#!/usr/bin/env python3
"""A CONTAGEM DE CENAS tem dois criterios opostos, e eu os conciliei de cabeca.

Medido em 20/10 as 02:2x, escrevendo o `labtreinamento-s089`.

Para escolher quantas cenas a peca teria eu escrevi, na linha de comando, um
laco sobre `range(6, 13)` chamando `mira.janela_dos_dois_mundos` e comparando a
cadencia resultante com os ~3,1 s medidos em 690/699. **Isto e o item 3 da §10 —
toda conta que eu faco a mao vira um erro meu — e e a MESMA forma do defeito de
19/10 as 11:2x** (a contagem de canal, cujo instrumento eu reescrevi a mao cinco
rodadas seguidas) **e das 23:3x** (a contagem de cota). Terceira dimensao, mesma
assinatura.

E o que o laco mostrou vale guardar, porque e um TRADE-OFF que nenhum documento
nosso tinha escrito. Medido no `labtreinamento`, o unico canal cuja mira e larga
o bastante para abrir janela nos dois mundos:

    | cenas | janela dos dois mundos | largura | cadencia (s/plano) |
    |---|---|---|---|
    | 2  | 188 a 201 | **14** | 11,50 |
    | 6  | 51 a 55   | 5      | 3,83 |
    | **7**  | **41 a 44**   | **4** | **3,29** |
    | 8  | 34 a 36   | 3      | 2,88 |
    | 11 | 20 a 21   | 2      | 2,09 |
    | 20 | 3 a 3     | 1      | 1,15 |

**A largura da janela ENCOLHE com a contagem de cenas — de 14 caracteres em
duas para 1 ou 2 acima de dezessete — e a cadencia so chega perto de 3,1 s em
SETE ou OITO.** E ela **NAO e monotona**, e isso tambem foi medido em vez de
suposto: eu escrevi "monotonamente" na primeira versao deste docstring e a
propria saida do modulo me desmentiu — 17 cenas da largura 1, 18 da 2, 19 da 1.
A janela e INTEIRA, logo o arredondamento oscila. A tendencia e de queda; a
monotonia nao existe. Logo os dois criterios apontam para
lados opostos: a janela mais larga esta em DUAS cenas e a melhor cadencia em
SETE, e elas **nunca coincidem**. Escolher a cadencia medida custa quase toda a
latitude de escrita — em sete cenas a janela tem **quatro** caracteres.

**E nos outros dois canais NAO EXISTE escolha:** com o `ALVO_SHORT` da frota
(41,5 a 43,0) **nenhuma** contagem de cena de 2 a 20 abre janela nos dois
mundos, nas duas vozes. E a pinca do 740/748, que a nota de 19/10 as 17:2x ja
mede de 1 a 40 cenas. Ali o que se escolhe e a EXPOSICAO declarada, nao a
contagem.

**UMA HIPOTESE MINHA CAIU AQUI, e vai dita porque eu quase a relatei como
achado:** o `cadencia_longo.cadencia_s` mede pela duracao **ESTIMADA**, enquanto
a mira, o portao e o orcamento leem a **REAL PREVISTA** — duas grandezas com o
mesmo nome `cadencia`, que e o 753 em forma de UNIDADE (o defeito de 19/10 as
15:2x). Eu supus que isso **trocaria a resposta**. Medido na peca: o vao e de
1,14 s no total e **0,16 s por plano**, e as duas grandezas escolhem a MESMA
contagem (sete, com |dif| 0,19 pela real e 0,04 pela estimada). **Logo a
diferenca de unidade existe e NAO move a escolha neste caso**, e eu registro
isso em vez de inflar. O que sobra e a disciplina: a cadencia que o espectador
ve e da duracao REAL, e e por ela que este modulo calcula.

**E ELE CALAVA JUSTAMENTE ONDE A PINCA FECHA — medido em 20/10 as 03:2x, na
primeira rodada depois de ele existir, escrevendo o `epomeno-epipedo-s072`.**
O `relato` devolvia UMA linha quando nenhuma contagem abre janela e **jogava
fora o `quadro` que ele acabara de calcular**, inclusive a coluna da cadencia —
que **nao depende da janela em sentido nenhum**. Medido: **38 dos 57 pares
(canal, contagem) ficavam sem uma palavra**, isto e DOIS dos tres canais, todas
as dezenove contagens. Logo o instrumento escrito para tirar a conta da minha
cabeca ordenava no canal em que eu nao precisava dele e se calava nos dois em
que eu precisava — e nesta rodada eu escolhi o catorze **a mao outra vez**,
lendo `contagens_existentes` de um SEGUNDO instrumento.

**E a recusa estava CERTA sobre a janela e ERRADA como silencio**, que e a mesma
forma do `origens_sem_uso`: nomear em vez de filtrar. A janela nao existe; a
cadencia existe e ordena.

**E A DIMENSAO QUE FALTAVA E A DO PEDIDO DO DONO.** Palavras dele em 19/10: *"os
videos publicados me parecem todos a mesma dinamica, imagens, formas, estilo.
Em todos os canais."* A pergunta *"que contagem de cena a frota nunca usou"* e
dessa dimensao, e ela morava no `esqueleto_entre_canais` — que este modulo nao
chamava. Agora chama, e **a contagem da frota e DELEGADA** (
`esqueleto_entre_canais.quadro()["por_contagem_de_cena"]`): recontar aqui criaria
o segundo dono da varredura do disco, que e a assinatura que congelou a legenda.

NAO E PORTAO, pelo argumento do `mira.py`: ele reprovaria quase toda spec do
acervo, que foi escrita antes de a janela dos dois mundos existir. Codigo de
saida SEMPRE zero.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ensaio   # noqa: E402  — DONO da duracao e do orcamento de caracteres
import mira     # noqa: E402  — DONO da janela dos dois mundos
import esqueleto_entre_canais as EC   # noqa: E402  — DONO das contagens da frota

# A cadencia MEDIDA do short, em segundos por plano. Ela e de 690/699 — a
# correcao do dinamismo visual de 09/10, medida com `tblend=difference` e
# `signalstats` em escala absoluta — e ate hoje ela morava SO NA PROSA do
# `video_referencia.py`, sem dono nenhum no codigo. Este e o dono.
#
# NAO e alvo e nao e limiar: e o valor que a medicao daquele dia produziu, e
# chamar de alvo seria limiar sem procedencia (§10). O que ele faz aqui e
# ORDENAR contagens de cena por distancia, que e a conta que eu fazia a mao.
CADENCIA_MEDIDA_S = 3.1

# A varredura vai de 2 a 20 porque 1 cena nao tem cadencia (zero transicoes) e
# acima de 20 a janela dos dois mundos cai a UM caractere por cena, que esta
# abaixo do piso OBSERVADO de 21 que o `mira.teto_de_cenas` usa.
MIN_CENAS, MAX_CENAS = 2, 20


def quadro(canal: str, voz: str, faixa=None, por_contagem=None,
           exceto: str = "") -> list[dict]:
    """Por contagem de cena: a janela, a cadencia e se a frota ja a usou.

    A janela e DELEGADA a `mira.janela_dos_dois_mundos` e a faixa a
    `ensaio.alvo_short` — refazer qualquer uma aqui criaria o segundo dono, que
    e a assinatura que congelou a legenda e parou a mira de conferir por seis
    pecas.
    """
    faixa = faixa if faixa is not None else ensaio.alvo_short(canal)
    if not faixa:
        raise ValueError(
            f"canal {canal!r} nao tem faixa: sem ela nao existe janela nem "
            "cadencia, e devolver lista vazia faria o chamador ler 'nenhuma "
            "contagem serve' onde o que falta e a faixa"
        )
    alvo_s = (faixa[0] + faixa[1]) / 2.0
    # As contagens que a frota JA usou saem do dono da varredura do disco.
    # Recontar aqui seria o segundo dono — e e essa coluna que faltava quando a
    # janela nao abre, porque ela e a dimensao do pedido do dono ("em todos os
    # canais").
    if por_contagem is None:
        por_contagem = contagens_da_frota(exceto)
    saida = []
    for n in range(MIN_CENAS, MAX_CENAS + 1):
        j = mira.janela_dos_dois_mundos(voz, n, faixa)
        cad = alvo_s / n   # pela duracao REAL, que e a que a mira cobra
        exemplares = int(por_contagem.get(n, 0) or 0)
        saida.append({
            "cenas": n,
            "janela": j,
            "largura": (j[1] - j[0] + 1) if j else 0,
            "cadencia_s": cad,
            "distancia_da_cadencia": abs(cad - CADENCIA_MEDIDA_S),
            "exemplares_na_frota": exemplares,
            "tamanho_inedito": exemplares == 0,
        })
    return saida


def escolha(canal: str, voz: str, faixa=None, por_contagem=None,
            exceto: str = "") -> dict:
    """As duas pontas do trade-off, e o que elas custam uma a outra.

    Devolve `None` em `por_cadencia` e `por_largura` quando NENHUMA contagem
    abre janela — que e o caso dos dois canais sem mira propria. Inventar uma
    escolha ali seria esconder a pinca do 740/748 em vez de a nomear, que e o
    que o `origens_sem_uso` ensina a nao fazer.
    """
    q = quadro(canal, voz, faixa, por_contagem=por_contagem, exceto=exceto)
    abertas = [x for x in q if x["janela"]]
    # A CADENCIA e a NOVIDADE nao dependem da janela, logo elas saem SEMPRE.
    # Era deixa-las de fora que fazia o relato calar nos dois canais da pinca.
    por_cad_geral = min(q, key=lambda x: x["distancia_da_cadencia"])
    ineditas = [x for x in q if x["tamanho_inedito"]]
    por_nov = (min(ineditas, key=lambda x: x["distancia_da_cadencia"])
               if ineditas else None)
    if not abertas:
        return {
            "canal": canal, "abertas": 0, "por_cadencia": None,
            "por_largura": None, "coincidem": None,
            "por_cadencia_geral": por_cad_geral,
            "por_novidade": por_nov,
            "ineditas": [x["cenas"] for x in ineditas],
            "motivo": ("NENHUMA contagem de cena de "
                       f"{MIN_CENAS} a {MAX_CENAS} abre janela nos dois mundos "
                       "nesta faixa — a pinca do 740/748. Aqui nao se escolhe "
                       "contagem pela janela, declara-se a EXPOSICAO; a CADENCIA "
                       "e a NOVIDADE do tamanho seguem ordenando."),
        }
    por_cad = min(abertas, key=lambda x: x["distancia_da_cadencia"])
    por_lar = max(abertas, key=lambda x: x["largura"])
    return {
        "canal": canal,
        "abertas": len(abertas),
        "por_cadencia": por_cad,
        "por_largura": por_lar,
        "coincidem": por_cad["cenas"] == por_lar["cenas"],
        "custo_em_caracteres": por_lar["largura"] - por_cad["largura"],
        "por_cadencia_geral": por_cad_geral,
        "por_novidade": por_nov,
        "ineditas": [x["cenas"] for x in ineditas],
        "motivo": "",
    }


def contagens_da_frota(exceto: str = "") -> dict:
    """`{contagem de cena: quantas pecas}` da frota, DELEGADO ao dono.

    O `exceto` existe pela mesma razao que no irmao: na hora de ESCOLHER, a
    spec da rodada pode ja estar no disco, e ai "inedita" nunca podia ser
    verdade. Nenhuma varredura se refaz aqui.
    """
    pecas = EC.varre()
    if exceto:
        pecas = [p for p in pecas if p["arquivo"] != exceto]
    return EC.quadro(pecas)["por_contagem_de_cena"]


def relato(canal: str = "labtreinamento", voz: str = None,
           exceto: str = "") -> str:
    voz = voz or ensaio.VOZ_DO_CANAL.get(canal) if hasattr(ensaio, "VOZ_DO_CANAL") else voz
    if not voz:
        voz = {"labtreinamento": "pt-BR-ThalitaMultilingualNeural",
               "epomeno-epipedo": "el-GR-NestorasNeural",
               "kolejny-poziom": "pl-PL-MarekNeural"}.get(canal)
    por_contagem = contagens_da_frota(exceto)
    e = escolha(canal, voz, por_contagem=por_contagem)
    L = [f"CONTAGEM DE CENAS de {canal} (voz {voz})"]
    if not e["abertas"]:
        L.append("  " + e["motivo"])
        L.append("")
        for x in sorted(quadro(canal, voz, por_contagem=por_contagem),
                        key=lambda x: x["distancia_da_cadencia"])[:6]:
            marca = "  << INEDITA na frota" if x["tamanho_inedito"] else \
                    f"  ({x['exemplares_na_frota']} na frota)"
            L.append(f"   {x['cenas']:2d} cenas  cadencia "
                     f"{x['cadencia_s']:.2f} s  "
                     f"|dif| {x['distancia_da_cadencia']:.2f}{marca}")
        L.append("")
        L.append(f"  cadencia MEDIDA (690/699): {CADENCIA_MEDIDA_S} s por plano "
                 "— nao e alvo, ela ORDENA")
        L.append(f"  melhor cadencia: {e['por_cadencia_geral']['cenas']} cenas")
        if e["por_novidade"]:
            L.append("  melhor cadencia entre as INEDITAS: "
                     f"{e['por_novidade']['cenas']} cenas "
                     f"(|dif| {e['por_novidade']['distancia_da_cadencia']:.2f})")
            L.append(f"  tamanhos que a frota NUNCA usou: {e['ineditas']}")
        else:
            L.append("  a frota JA usou todos os tamanhos de "
                     f"{MIN_CENAS} a {MAX_CENAS} — a novidade de tamanho "
                     "acabou, e a de FORMA fica com o `esqueleto_entre_canais`")
        L.append("")
        L.append("  a contagem da frota e do `esqueleto_entre_canais`, nao daqui.")
        return "\n".join(L)
    for x in quadro(canal, voz, por_contagem=por_contagem):
        if not x["janela"]:
            continue
        marca = ""
        if x["cenas"] == e["por_cadencia"]["cenas"]:
            marca += "  << cadencia"
        if x["cenas"] == e["por_largura"]["cenas"]:
            marca += "  << largura"
        L.append(f"   {x['cenas']:2d} cenas  janela {x['janela']}  "
                 f"largura {x['largura']:2d}  cadencia {x['cadencia_s']:.2f} s"
                 f"{marca}")
    L.append("")
    L.append(f"  cadencia MEDIDA (690/699): {CADENCIA_MEDIDA_S} s por plano — "
             "nao e alvo, ela ORDENA")
    L.append(f"  melhor cadencia: {e['por_cadencia']['cenas']} cenas "
             f"(janela de {e['por_cadencia']['largura']} caractere(s))")
    L.append(f"  janela mais larga: {e['por_largura']['cenas']} cenas "
             f"({e['por_largura']['largura']} caractere(s))")
    if e["por_novidade"]:
        L.append("  melhor cadencia entre as INEDITAS na frota: "
                 f"{e['por_novidade']['cenas']} cenas "
                 f"(|dif| {e['por_novidade']['distancia_da_cadencia']:.2f}); "
                 f"tamanhos nunca usados: {e['ineditas']}")
    if not e["coincidem"]:
        L.append(f"  >> os dois criterios NAO coincidem: escolher a cadencia "
                 f"custa {e['custo_em_caracteres']} caractere(s) de latitude")
    L.append("")
    L.append("  isto NAO reprova e nao escreve a peca: a cadencia que o")
    L.append("  espectador ve e da duracao REAL PREVISTA, nao da estimada —")
    L.append("  o `cadencia_longo` usa a estimada e as duas diferem 0,16 s")
    L.append("  por plano nesta mira, sem trocar a escolha (medido).")
    return "\n".join(L)


if __name__ == "__main__":
    canal = sys.argv[1] if len(sys.argv) > 1 else "labtreinamento"
    print(relato(canal))
    sys.exit(0)   # SEMPRE zero: isto informa, nao reprova.
