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

**E O CONSERTO DAS 03:2x RECOMENDOU, NA PRIMEIRA RODADA SEGUINTE, UMA CONTAGEM
QUE NAO CABE — medido em 20/10 as 04:1x, no `kolejny-poziom`.** Posto a ordenar
na pinca, ele deu **15 cenas** como *"melhor cadencia entre as INEDITAS"*. **O
teto MEDIDO da voz polonesa e 14** (`mira.teto_de_cenas`), logo 15 nao cabe em
silencio nenhum. Medido nos tres canais, as contagens que ele oferecia acima do
teto da propria voz:

    | canal           | teto MEDIDO | ineditas RECOMENDADAS acima dele |
    |---|---|---|
    | labtreinamento  | **11** | 15, 16, 17, 18, 19, 20 |
    | epomeno-epipedo | **15** | 16, 17, 18, 19, 20 |
    | kolejny-poziom  | **14** | 15, 16, 17, 18, 19, 20 |

**E e a QUINTA vez da mesma assinatura na familia destes instrumentos: nao
chamar quem ja sabe.** O `mira.teto_de_cenas` existe desde 20/10 as 00:3x, com o
piso de caracteres por cena OBSERVADO (21, a media do `labtreinamento-s081`), e
este modulo nunca o chamou — o `MAX_CENAS = 20` daqui e um limite de VARREDURA,
nao o teto da voz, e eu os tratei como a mesma coisa.

**O teto e DELEGADO, e as contagens acima dele vao NOMEADAS e nao filtradas:** o
relato diz qual e o teto, de onde ele vem e que acima dele o orcamento cai
abaixo do piso observado de caracteres. Esconde-las faria a rodada seguinte
perguntar por que a lista encurtou — e nomear em vez de filtrar e a disciplina do
`origens_sem_uso`.

**E ELE NAO SABE O QUE O CANAL ACABOU DE PUBLICAR — medido em 20/10 as 05:2x,
escrevendo o `labtreinamento-s090`.** Ele deu **SETE** cenas como melhor
cadencia, e as DUAS pecas anteriores deste canal — a `s088` e a `s089` — tem
sete cada. Eu recusei o sete **a mao**, como tinha recusado o treze a mao uma
hora antes no `kolejny`, quando o `s072` daquele canal tinha treze. **Duas
recusas a mao em duas rodadas e o item 3 da §10 — e ele mora DENTRO do
instrumento que existe para tirar essa conta da minha cabeca.**

Medido nos tres canais vivos no instante da escolha:

    | canal           | melhor cadencia | ultimas duas do canal | repete? |
    |---|---|---|---|
    | labtreinamento  | **7**  | `s089` 7, `s088` 7   | **SIM** |
    | epomeno-epipedo | **14** | `s072` 14, `s071` 12 | **SIM** |
    | kolejny-poziom  | **14** | `s073` 12, `s072` 13 | nao     |

**Dois de tres.** E o custo nao e estetico: repetir tamanho no mesmo canal em
rodadas seguidas e literalmente a reclamacao do dono de 19/10 — *"os videos
publicados me parecem todos a mesma dinamica, imagens, formas, estilo"* — e o
portao `variedade` **nao pega**, porque ele conta ESQUELETO repetido e nao
TAMANHO, e so avisa a partir de seis iguais.

**A RECENCIA SAI DO PARQUE, e isso e forcado: a spec no disco nao tem data.**
`duracao_a_medir.carrega()` e o dono das pecas publicadas com instante (`em`), o
`canal.do_pacote` e o dono UNICO da derivacao do canal desde 19/10 as 05:2x — e
e preciso, porque **57 das 78 linhas do parque nao tem o campo `canal`** — e as
cenas saem do `esqueleto_entre_canais`. Nenhuma das tres contas se refaz aqui.

**O K E REDACAO DECLARADA, nao medicao, e vai dito:** `RECENTES_K = 2` sai das
duas recusas acima, nao de uma distribuicao. Por isso ele e **parametro** e o
instrumento **NOMEIA em vez de filtrar** — a melhor cadencia continua saindo no
relato, com a colisao ao lado e com a melhor que NAO repete logo embaixo. Filtrar
esconderia a contagem que a cadencia escolhe, e seria a cegueira que o
`origens_sem_uso` nasceu para desfazer.

**E O "MIRE O PISO" DO 772 NAO E APLICAVEL EM TODA CONTAGEM — medido em 20/10
as 06:3x, depois de eu recusar o TETO da voz a mao pela SEGUNDA vez.** As 04:1x
eu recusei catorze cenas no `kolejny` porque o orcamento ali dava 22 caracteres,
UM acima do piso OBSERVADO; as 06:2x recusei quinze no `epomeno` pela conta
identica. **Duas recusas a mao, com a mesma aritmetica, e o `cabe_na_voz` deste
modulo e um BOOLEANO: ele diz que cabe e nao diz com quanta folga.**

E ao medir a folga apareceu um fato que nenhum documento nosso tinha: **em tres
dos 37 pares (canal, contagem) abaixo do teto, o PISO da faixa nao e alcancavel
com texto legivel** — a conta pede MENOS caracteres por cena que o piso
observado:

    | canal           | cenas | chars para o PISO | folga |
    |---|---|---|---|
    | labtreinamento  | 8  | 24 | 3 |
    | labtreinamento  | **9**  | **19** | **-2** |
    | labtreinamento  | **10** | **15** | **-6** |
    | labtreinamento  | **11** | **12** | **-9** |
    | epomeno-epipedo | 15 (teto) | 22 | **1** |
    | kolejny-poziom  | 14 (teto) | 22 | **1** |

**E o caso do meio e o mais usado da frota: DEZ cenas, 149 pecas.** Naquele canal
e naquela contagem, *"mire o piso"* pede cena de quinze caracteres — logo a regra
de redacao do 772 **nao se aplica ali**, e o `teto_de_cenas` nao contradiz isso:
ele pergunta se ALGUM numero de caracteres cai DENTRO da faixa, nao se o piso
dela e alcancavel. **As duas perguntas sao diferentes e eu as tratei como uma.**

O `folga_no_piso` entra como COLUNA e o relato NOMEIA os dois casos — piso
inalcancavel e folga rente — em vez de filtrar contagem nenhuma. A conta e
DELEGADA ao `mira.chars_no_alvo` e o piso de caracteres ao
`mira.teto_de_cenas(...)["chars_minimos"]`: refazer qualquer uma aqui criaria o
segundo dono.

NAO E PORTAO, pelo argumento do `mira.py`: ele reprovaria quase toda spec do
acervo, que foi escrita antes de a janela dos dois mundos existir. Codigo de
saida SEMPRE zero.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ensaio   # noqa: E402  — DONO da duracao e do orcamento de caracteres
import mira     # noqa: E402  — DONO da janela dos dois mundos
import esqueleto_entre_canais as EC
import nome_da_spec as NS   # noqa: E402  — UM dono do nome da spec
import duracao_a_medir as DM         # noqa: E402  — DONO do parque de publicadas
import canal as CA                   # noqa: E402  — DONO da derivacao do canal

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

# Quantas pecas publicadas do PROPRIO canal contam como "recente" para efeito de
# repeticao de TAMANHO.
#
# Isto e REDACAO DECLARADA e nao medicao: o 2 sai das duas recusas que eu fiz a
# mao — o treze no `kolejny` em 20/10 as 04:1x e o sete no `labtreinamento` as
# 05:2x —, nao de uma distribuicao. Por ser escolha e nao medida, ele e
# parametro, o instrumento NOMEIA a colisao em vez de filtrar a contagem, e isto
# nao reprova nada: quem decide e quem escreve a peca.
RECENTES_K = 2

# Quando a folga de caracteres sobre o piso OBSERVADO conta como "rente".
#
# REDACAO DECLARADA, nao medida: o 2 e o menor valor que exclui as DUAS recusas
# que eu fiz a mao — o teto do `kolejny` as 04:1x e o do `epomeno` as 06:2x, as
# duas com folga de UM caractere. **E a faixa de 2 a 4 nunca foi observada**: as
# contagens que eu aceitei tem folga 5, 9, 10, 11 e 15, logo nenhum dado escolhe
# dentro dela, e por isso isto e parametro e o instrumento NOMEIA em vez de
# filtrar.
FOLGA_RENTE = 2


def _piso_executavel(voz: str, n: int, faixa) -> int:
    """Caracteres por cena que de fato ALCANCAM o piso da faixa — DELEGADO.

    O dono e `mira.janela_do_mundo`, que e quem o `mira.orcamento` ja chamava
    para imprimir o PISO EXECUTAVEL. Aqui so se traduz "sem janela" para zero,
    porque o `quadro` precisa de um inteiro para a coluna da folga — e zero ali
    le como "o piso nao e alcancavel", que e a leitura certa.

    NAO refaz a inversao: refazer criaria o quarto dono da mesma conta, depois
    do inversor cru, do epsilon escrito a mao e do relato do `mira`.
    """
    j = mira.janela_do_mundo(voz, n, faixa, "edge")
    if j:
        return j[0]
    # SEM JANELA TEM DUAS CAUSAS, e colapsar as duas em zero foi o defeito que
    # o meu PROPRIO conserto introduziu em 21/10 as 02:4x, na mesma rodada:
    # zero le como "o piso NAO e alcancavel", e para duas e tres cenas a janela
    # EXISTE — ela mora ACIMA do teto de varrimento do dono
    # (`mira.MAX_CHARS_VARRIDOS`, 240 por escolha documentada). Medido: com tres
    # cenas no grego a previsao entra em 242 caracteres, e com duas em 380.
    # Logo e a familia de 17/10 outra vez — instrumento que devolve VAZIO nao
    # prova ausencia — dentro do conserto de outra coisa.
    #
    # O discriminador e barato: se o inversor cru ja responde no teto ou acima
    # dele, a janela (se existe) esta fora do alcance do laco, e a resposta
    # honesta e None = NAO MEDIDO, nunca zero.
    cru = mira.chars_no_alvo(voz, n, faixa[0])
    if cru and cru >= mira.MAX_CHARS_VARRIDOS:
        return None
    return 0


def quadro(canal: str, voz: str, faixa=None, por_contagem=None,
           exceto: str = "", recentes=None) -> list[dict]:
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
    # O TETO DA VOZ e DELEGADO ao `mira.teto_de_cenas`, que o mede contra o piso
    # OBSERVADO de caracteres por cena. O `MAX_CENAS` daqui e limite de
    # VARREDURA, nao teto de voz — tratar os dois como a mesma coisa foi o
    # defeito de 20/10 as 04:1x.
    teto = teto_da_voz(voz, faixa)
    # A RECENCIA no PROPRIO canal, que o `variedade` nao ve: ele conta esqueleto
    # repetido, nao tamanho. Ela NAO filtra contagem nenhuma — entra como coluna.
    if recentes is None:
        recentes = recentes_do_canal(canal)
    rec_cenas = [r["cenas"] for r in recentes if r["cenas"]]
    # O PISO de caracteres por cena e do dono do teto — nunca o literal daqui.
    piso_chars = int(mira.teto_de_cenas(voz, faixa)["chars_minimos"])
    saida = []
    for n in range(MIN_CENAS, MAX_CENAS + 1):
        j = mira.janela_dos_dois_mundos(voz, n, faixa)
        cad = alvo_s / n   # pela duracao REAL, que e a que a mira cobra
        exemplares = int(por_contagem.get(n, 0) or 0)
        _pe = _piso_executavel(voz, n, faixa)
        saida.append({
            "cenas": n,
            "janela": j,
            "largura": (j[1] - j[0] + 1) if j else 0,
            "cadencia_s": cad,
            "distancia_da_cadencia": abs(cad - CADENCIA_MEDIDA_S),
            "exemplares_na_frota": exemplares,
            "tamanho_inedito": exemplares == 0,
            "cabe_na_voz": n <= teto,
            "repete_recente": n in rec_cenas,
            # Quantos caracteres por cena a peca precisa para encostar no PISO
            # da faixa, e quanto isso sobra do piso OBSERVADO de caracteres.
            # NEGATIVO significa que o piso da faixa NAO e alcancavel com texto
            # legivel — e ai a regra de redacao do 772 nao se aplica.
            #
            # E O NUMERO SAI DO `janela_do_mundo`, QUE E O DONO DO PISO
            # EXECUTAVEL (21/10, 02:3x). Ate aqui ele saia de
            # `chars_no_alvo(voz, n, faixa[0] + 0.05)` — o inversor CRU com um
            # epsilon escrito a mao. Medido nas tres vozes de 2 a 20 cenas: o
            # inversor cru devolve valor cuja previsao cai ABAIXO do piso em
            # **54 de 54** pares (deficit mediano 0,206 s, maximo 0,870 s), e o
            # `+ 0.05` conserta **5 desses 54** — isto e, ele PARECE correcao e
            # nao e. O `janela_do_mundo[0]` acerta 54 de 54, e difere do cru por
            # exatamente +1 caractere em 51 deles.
            "chars_no_piso": _pe,
            # None quer dizer NAO MEDIDO (a janela mora acima do teto de
            # varrimento), e nao "sem folga": os tres estados sao alcancavel
            # (inteiro >= 0), inalcancavel (negativo) e nao medido (None).
            "folga_no_piso": (None if _pe is None else _pe - piso_chars),
            "piso_nao_medido": _pe is None,
            "recentes_com_esse_tamanho": [r["pacote"] for r in recentes
                                          if r["cenas"] == n],
        })
    return saida


def escolha(canal: str, voz: str, faixa=None, por_contagem=None,
            exceto: str = "", recentes=None) -> dict:
    """As duas pontas do trade-off, e o que elas custam uma a outra.

    Devolve `None` em `por_cadencia` e `por_largura` quando NENHUMA contagem
    abre janela — que e o caso dos dois canais sem mira propria. Inventar uma
    escolha ali seria esconder a pinca do 740/748 em vez de a nomear, que e o
    que o `origens_sem_uso` ensina a nao fazer.
    """
    # A faixa e resolvida AQUI tambem porque o teto da voz depende dela, e
    # `faixa=None` chegava crua ao `mira.teto_de_cenas` (pego na 1a execucao).
    faixa = faixa if faixa is not None else ensaio.alvo_short(canal)
    if recentes is None:
        recentes = recentes_do_canal(canal)
    q = quadro(canal, voz, faixa, por_contagem=por_contagem, exceto=exceto,
               recentes=recentes)
    abertas = [x for x in q if x["janela"]]
    # A CADENCIA e a NOVIDADE nao dependem da janela, logo elas saem SEMPRE.
    # Era deixa-las de fora que fazia o relato calar nos dois canais da pinca.
    cabem = [x for x in q if x["cabe_na_voz"]] or q
    por_cad_geral = min(cabem, key=lambda x: x["distancia_da_cadencia"])
    # A NOVIDADE so vale entre as contagens que CABEM na voz: recomendar acima
    # do teto medido e entregar polones telegrafico (04:1x).
    ineditas = [x for x in q if x["tamanho_inedito"] and x["cabe_na_voz"]]
    acima_do_teto = [x["cenas"] for x in q if not x["cabe_na_voz"]]
    ined_acima = [x["cenas"] for x in q
                  if x["tamanho_inedito"] and not x["cabe_na_voz"]]
    por_nov = (min(ineditas, key=lambda x: x["distancia_da_cadencia"])
               if ineditas else None)
    # A melhor cadencia que NAO repete o tamanho das ultimas do canal. Ela entra
    # AO LADO da melhor cadencia, nunca no lugar dela: substituir seria filtrar,
    # e o K e redacao declarada, nao medida.
    sem_rep = [x for x in cabem if not x["repete_recente"]]
    por_cad_nova = (min(sem_rep, key=lambda x: x["distancia_da_cadencia"])
                    if sem_rep else None)
    # E a melhor cadencia que SERVE de fato: cabe na voz, nao repete tamanho
    # recente E alcanca o PISO da faixa com folga. Era isto que faltava — o
    # modulo CALCULAVA a `folga_no_piso` desde 06:3x e a chave de escolha
    # aplicava SO a recencia, logo ela devolvia, em dois canais de tres, uma
    # contagem que a propria coluna dele recusa: 14 no `kolejny` (folga +1, a
    # conta que eu recusei a mao em 04:1x, 06:2x e 07:1x) e 9 no
    # `labtreinamento` (folga -2, isto e PISO INALCANCAVEL). E a quinta vez
    # desta familia de instrumentos: nao aplicar o que o proprio modulo sabe.
    # `folga_no_piso` None quer dizer NAO MEDIDO, e nao-medido NAO serve —
    # mas por um motivo diferente de folga rente, e o relato o separa.
    serve = [x for x in sem_rep
             if x["folga_no_piso"] is not None
             and x["folga_no_piso"] > FOLGA_RENTE]
    por_cad_serve = (min(serve, key=lambda x: x["distancia_da_cadencia"])
                     if serve else None)
    # NOMEADOS e nao filtrados: o que caiu por folga sai no relato, como o
    # `origens_sem_uso` nomeia origem inutilizavel em vez de a esconder.
    desc_folga = [x["cenas"] for x in sem_rep
                  if x["folga_no_piso"] is not None
                  and x["folga_no_piso"] <= FOLGA_RENTE]
    if not abertas:
        return {
            "canal": canal, "abertas": 0, "por_cadencia": None,
            "por_largura": None, "coincidem": None,
            "por_cadencia_geral": por_cad_geral,
            "por_novidade": por_nov,
            "ineditas": [x["cenas"] for x in ineditas],
            "teto_da_voz": teto_da_voz(voz, faixa),
            "acima_do_teto": acima_do_teto,
            "ineditas_acima_do_teto": ined_acima,
            "recentes": recentes,
            "por_cadencia_sem_repetir": por_cad_nova,
            "por_cadencia_servivel": por_cad_serve,
            "descartados_pela_folga": desc_folga,
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
        "teto_da_voz": teto_da_voz(voz, faixa),
        "acima_do_teto": acima_do_teto,
        "ineditas_acima_do_teto": ined_acima,
        "recentes": recentes,
        "por_cadencia_sem_repetir": por_cad_nova,
        "por_cadencia_servivel": por_cad_serve,
        "descartados_pela_folga": desc_folga,
        "motivo": "",
    }


def teto_da_voz(voz: str, faixa) -> int:
    """O teto de cenas desta voz, DELEGADO ao `mira.teto_de_cenas`.

    Ele mede quantas cenas cabem antes de o orcamento por cena cair abaixo do
    piso OBSERVADO de caracteres (21, a media do `labtreinamento-s081`).
    Recalcular aqui criaria o segundo dono — e foi por NAO o chamar que este
    modulo recomendou 15 cenas numa voz cujo teto e 14.
    """
    t = mira.teto_de_cenas(voz, faixa)
    return int(t["teto"]) if t else MAX_CENAS


def recentes_do_canal(canal: str, k: int = RECENTES_K, registros=None,
                      cenas_por_pacote=None) -> list[dict]:
    """As `k` ultimas pecas PUBLICADAS deste canal, com a contagem de cenas.

    As tres contas sao DELEGADAS, e nenhuma delas podia ficar aqui:

    * o instante vem de `duracao_a_medir.carrega()`, o dono do parque — a spec
      no disco **nao tem data**, logo a recencia nao e derivavel da varredura;
    * o canal vem de `canal.do_pacote`, o dono UNICO desde 19/10 as 05:2x, e nao
      do campo `canal` do registro, que **falta na maioria das linhas antigas**;
    * as cenas vem de `esqueleto_entre_canais.varre()`.

    Peca cujo pacote nao esta mais no disco sai com `cenas: None` em vez de
    sumir — ausencia de spec nao e ausencia de publicacao, e descartar faria a
    janela de recencia andar para tras em silencio.
    """
    regs = DM.carrega() if registros is None else registros
    if cenas_por_pacote is None:
        cenas_por_pacote = {p["arquivo"][:-5]: p["cenas"] for p in EC.varre()}
    meus = [r for r in regs if CA.do_pacote(r.get("pacote", "")) == canal]
    meus.sort(key=lambda r: r.get("em", ""), reverse=True)
    saida = []
    for r in meus[:max(0, int(k))]:
        pac = r.get("pacote", "")
        saida.append({"pacote": pac, "em": r.get("em", ""),
                      "cenas": cenas_por_pacote.get(pac)})
    return saida


def contagens_da_frota(exceto: str = "") -> dict:
    """`{contagem de cena: quantas pecas}` da frota, DELEGADO ao dono.

    O `exceto` existe pela mesma razao que no irmao: na hora de ESCOLHER, a
    spec da rodada pode ja estar no disco, e ai "inedita" nunca podia ser
    verdade. Nenhuma varredura se refaz aqui.
    """
    pecas = EC.varre()
    # o filtro e DELEGADO ao `EC.sem`, que e o dono dele desde 22/10 as 11:4x
    # — recopiar a compreensao aqui era o segundo dono do mesmo fato.
    pecas = EC.sem(pecas, exceto)
    return EC.quadro(pecas)["por_contagem_de_cena"]


def _linha_do_teto(e: dict) -> str:
    """A linha que NOMEIA o teto e o que ficou acima dele.

    UM dono: ela nascia duplicada nos dois ramos do relato, que e o 753 em
    forma de frase (o `mira._linha_do_orcamento` tem a mesma razao).
    """
    acima = e.get("acima_do_teto") or []
    ined = e.get("ineditas_acima_do_teto") or []
    s = (f"  TETO MEDIDO desta voz: {e['teto_da_voz']} cenas "
         "(`mira.teto_de_cenas`, contra o piso OBSERVADO de caracteres)")
    if acima:
        s += (f"\n  acima dele, FORA da ordenacao: {acima}"
              + (f" — destas, nunca usadas pela frota: {ined}; recomenda-las "
                 "seria entregar orcamento abaixo do piso de caracteres (04:1x)"
                 if ined else ""))
    return s


def _linha_da_folga(q: list[dict], e: dict) -> str:
    """A linha que NOMEIA onde o PISO da faixa nao e alcancavel, ou e rente.

    UM dono, e ela sai nos DOIS ramos do relato — a frase do teto nasceu
    duplicada e foi isso que a fez divergir (753).
    """
    cabem = [x for x in q if x["cabe_na_voz"]]
    inalc = [x["cenas"] for x in cabem
             if x["folga_no_piso"] is not None and x["folga_no_piso"] < 0]
    nao_med = [x["cenas"] for x in cabem if x["folga_no_piso"] is None]
    rente = [x["cenas"] for x in cabem
             if x["folga_no_piso"] is not None
             and 0 <= x["folga_no_piso"] <= FOLGA_RENTE]
    L = ["  FOLGA DE CARACTERES no PISO da faixa (piso OBSERVADO do "
         "`mira.teto_de_cenas`):"]
    if inalc:
        L.append(f"  >> em {inalc} o PISO da faixa NAO e alcancavel com texto "
                 "legivel — a regra de redacao do 772 (`mire o PISO`) nao se "
                 "aplica nessas contagens, e o `teto_de_cenas` nao contradiz "
                 "isso: ele pergunta se ALGUM numero de caracteres cai DENTRO "
                 "da faixa.")
    if nao_med:
        L.append(f"  >> em {nao_med} o piso NAO FOI MEDIDO, e isto nao e o "
                 "mesmo que inalcancavel: a janela mora ACIMA do teto de "
                 f"varrimento do dono (`mira.MAX_CHARS_VARRIDOS` = "
                 f"{mira.MAX_CHARS_VARRIDOS}). Medido: com tres cenas no grego "
                 "a previsao entra em 242 caracteres e com duas em 380. Elas "
                 "NAO entram na escolha, e o motivo e falta de medida — nao "
                 "falta de folga. Vazio de instrumento nao prova ausencia "
                 "(17/10).")
    if rente:
        L.append(f"  >> em {rente} a folga e de ate {FOLGA_RENTE} caractere(s) "
                 "— foi por essa conta que o teto da voz foi recusado a mao em "
                 "04:1x e 06:2x. O numero e REDACAO declarada, nao medida.")
    if not inalc and not rente and not nao_med:
        L.append("  todas as contagens que cabem na voz alcancam o piso com "
                 "folga — nada a nomear aqui.")
    x = e.get("por_cadencia_geral")
    if x:
        L.append(f"  a escolha por cadencia ({x['cenas']} cenas) pede "
                 f"{x['chars_no_piso']} caractere(s) por cena no piso "
                 f"(folga {x['folga_no_piso']:+d}).")
    s = e.get("por_cadencia_servivel")
    fora = e.get("descartados_pela_folga") or []
    if s:
        L.append(f"  >> melhor cadencia que SERVE (cabe na voz, nao repete "
                 f"tamanho recente e alcanca o piso com folga): "
                 f"{s['cenas']} cenas, {s['chars_no_piso']} caractere(s) no "
                 f"piso (folga {s['folga_no_piso']:+d}).")
    else:
        L.append("  >> NENHUMA contagem serve aos tres filtros ao mesmo tempo "
                 "— aqui nao se escolhe contagem, declara-se a EXPOSICAO, do "
                 "jeito que o `porta1` recusa janela curta.")
    if fora:
        L.append(f"  descartadas pela folga, e NOMEADAS em vez de filtradas: "
                 f"{fora}.")
    return "\n".join(L)


def _linha_da_recencia(e: dict) -> str:
    """A linha que NOMEIA a repeticao de tamanho no proprio canal.

    UM dono, e ela sai nos DOIS ramos do relato — a frase do teto nasceu
    duplicada e foi isso que a fez divergir (753).
    """
    rec = e.get("recentes") or []
    if not rec:
        return ("  RECENCIA no canal: o parque nao tem peca publicada deste "
                "canal — logo isto NAO ordena nada, e nao e 'nao repete'")
    desc = ", ".join(f"{r['pacote']} "
                     + (f"{r['cenas']} cenas" if r["cenas"] else "cenas ?")
                     for r in rec)
    s = (f"  RECENCIA no canal (ultimas {len(rec)} publicadas, do parque): "
         f"{desc}")
    marcadas = [x for x in (e.get("por_cadencia_geral"),
                            e.get("por_cadencia"), e.get("por_novidade"))
                if x and x.get("repete_recente")]
    if marcadas:
        quais = sorted({x["cenas"] for x in marcadas})
        s += (f"\n  >> a escolha por cadencia REPETE o tamanho: {quais}. "
              "Repetir tamanho no mesmo canal em rodadas seguidas e a "
              "reclamacao do dono de 19/10, e o portao `variedade` NAO pega "
              "(ele conta esqueleto, nao tamanho).")
        nova = e.get("por_cadencia_sem_repetir")
        if nova:
            s += (f"\n  melhor cadencia que NAO repete: {nova['cenas']} cenas "
                  f"(|dif| {nova['distancia_da_cadencia']:.2f})")
        else:
            s += ("\n  e NENHUMA contagem que cabe na voz escapa da "
                  "repeticao — aqui a novidade tem de ser de FORMA.")
    else:
        s += "\n  a escolha por cadencia NAO repete tamanho recente."
    return s


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
        cabem = [x for x in quadro(canal, voz, por_contagem=por_contagem)
                 if x["cabe_na_voz"]]
        for x in sorted(cabem,
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
        L.append(_linha_do_teto(e))
        L.append(_linha_da_recencia(e))
        L.append(_linha_da_folga(
            quadro(canal, voz, por_contagem=por_contagem), e))
        L.append("  a contagem da frota e do `esqueleto_entre_canais`, e o teto")
        L.append("  da voz e do `mira.teto_de_cenas` — nenhum dos dois e daqui.")
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
    L.append(_linha_do_teto(e))
    L.append(_linha_da_recencia(e))
    L.append(_linha_da_folga(quadro(canal, voz, por_contagem=por_contagem), e))
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
