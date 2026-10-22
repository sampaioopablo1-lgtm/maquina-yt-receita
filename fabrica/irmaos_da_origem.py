"""Os irmaos de uma origem, e o que deles SERVE de comparador de familia.

**Aprendizado 776, `alto`, medido em 15/10 as 12:2x, escrevendo o
`epomeno-epipedo-s035`.** Eu escolhi os capitulos 59 a 62 da origem `eimuyGaCor8`
— o limiar ser RELATIVO e nao linha absoluta — que e o achado mais forte daquele
trecho. **Ja era a familia do `epomeno-epipedo-s023`**, da MESMA origem: o titulo
curto dele e, literalmente, *"To orio den metraei an zeis"*.

**E o que me pegou foi ler o TITULO, nao um portao nem um campo.** Os dois irmaos
(`s001` e `s023`) sao de geracao ANTERIOR e **nenhum dos dois tem
`## FAMILIA DE ENTRADA ERRADA`** — o campo que eu usaria para comparar nao existe
neles. A regra (f) manda nao repetir familia, e a forma como eu a cumpro
(comparar o campo) **falha em silencio** quando o irmao nao o tem: ausencia de
campo lida como ausencia de familia.

**E o `segundo_angulo.nao_mencionados` NAO pega isto**, e e importante dizer por
que: ele compara CAPITULOS, e capitulo livre nao significa familia livre. Aqui o
68 estava livre e a familia dos 59 a 62 nao estava — sao perguntas diferentes.

**Pior: a geracao antiga registrou a familia em PROSA, em outro lugar.** O `s023`
tem um bloco *"O QUE EU NAO LEVEI"* que nomeia a familia do `s001` ("essa familia
JA foi usada pelo `s001`") e declara de quais capitulos ele mesmo saiu. Ou seja, a
informacao existia — em texto corrido, num cabecalho que nenhum codigo meu lia.

**O que este modulo faz:** para cada irmao devolve o titulo curto, a familia
QUANDO o campo existe, as notas de prosa que costumam carrega-la, e os capitulos
que ele declara ter usado. E quando o campo falta, `relato` **DIZ que falta** e
manda comparar pelo titulo e pela prosa, em vez de devolver vazio — porque vazio
se le como "nao ha familia", que foi exatamente o erro.

**E EM 20/10 AS 15:3x ELE QUASE ME DEIXOU REPETIR UMA FAMILIA, pelo que ele
mostrava e NAO pelo que faltava.** Escrevendo o `labtreinamento-s093` eu ia usar
COMPARAR TRES ORCAMENTOS PELO PRECO QUANDO O ESCOPO DIFERE (capitulos 37 a 41 da
origem `yrWVyqQtw00`). O relato trouxe os cinco irmaos, acusou que tres nao tem o
campo, e imprimiu **tres frases de outros irmaos citando o `s010`** — as tres
dizendo que ele e *"ORDEM DE CONTRATACAO"*, *"a ORDEM do orcamento"*, *"pedir o
estudo antes do levantamento"*. Lido assim, o meu eixo parecia outro: ordem
contra comparacao de propostas.

**A narracao do PROPRIO `s010` diz o contrario, em letra:** *"Quem pede orcamento
sem levantamento recebe o escopo da instalacao inteira"* e *"O preco cai porque o
escopo encolheu, nao porque alguem negociou"*. Isto e exatamente o eixo
escopo-contra-preco. **A familia dele estava escrita na peca e ausente de tudo o
que o modulo me mostrou.**

**A causa e de PROCEDENCIA e nao de ausencia: resumo de TERCEIRO perde o eixo.**
As frases que o modulo imprimia eram de segunda mao — o irmao B descrevendo o
irmao A — e compressao feita por outro guarda o que interessava a ELE. O ramo
*"nenhum irmao CITA outro pelo nome"*, que manda ler a copy inteira, **nao
disparou justamente porque havia citacoes**: quanto mais os irmaos se citam,
menos o modulo manda ler a fonte.

**E O RELATO PROMETIA A PROSA E NUNCA A IMPRIMIA — `irmaos()` a calculava e
`relato()` a jogava fora.** A linha de ATENCAO dizia, em letra, *"leia a PROSA
abaixo, que e onde a geracao antiga a registrava"*, e abaixo nao havia prosa
nenhuma: so as citacoes de segunda mao. Medido nas specs de **SHORT SOLTO** com
copy, que sao a populacao que este modulo serve:

| | |
|---|---|
| specs de short solto com copy | **240** |
| COM o campo da familia | **69** |
| **SEM** o campo | **171** |
| dessas, com bloco de prosa | **171 de 171** |
| para quantas o `relato` imprimia esse bloco | **ZERO** |

E no caso desta rodada o bloco carregava a familia em letra: o
`AVISO SOBRE OS NUMEROS` do `s010` diz *"a ORDEM de contratacao nao envelhece, e
e ela que este short carrega"*. A frase prometida existia e nao chegava a saida —
a mesma forma da nota da rota de 13:2x (calculada e descartada) e do `quadro` que
o `contagem_de_cenas` jogava fora as 03:2x.

**E A NARRACAO E A FONTE DE PRIMEIRA MAO, e ela acrescenta o que a prosa NAO
tem:** o `AVISO` do `s010` fala de *ordem*, e a narracao dele fala de
*"o preco cai porque o escopo encolheu"* — que e o eixo que eu ia repetir. Logo a
prosa sozinha nao bastava: ela e o resumo que o autor fez da PROPRIA peca, e
resumo tambem comprime.

**E O NUMERO QUE EU IA RELATAR ESTAVA ERRADO, e quem me pegou foi o teste que eu
escrevi nesta mesma rodada.** Eu havia medido *"66 de 379 specs em que so o
titulo sobra"* e ia escrever isso aqui: **as 66 eram PACOTES**, que este modulo
nem considera irmao (`irmaos()` exige `longo` vazio). Na populacao certa esse
numero e **ZERO** — nenhum short solto fica so com o titulo, porque todos tem
bloco de prosa. Era o §3.8 no meu proprio numero: contei outra populacao e ia
apresenta-la como a do defeito.

**Consertado:** o irmao SEM o campo entrega a `narracao` dele, cena por cena e
**sem truncar** (truncar por tamanho foi o que quase cortou a frase que salvou o
`s035`), marcada como PRIMEIRA mao; as citacoes continuam saindo, agora marcadas
como SEGUNDA. Irmao COM o campo **nao** recebe esse bloco: o campo e o dono
quando existe, e imprimir as duas coisas criaria o segundo dono da familia.

**E EM 20/10 AS 17:4x ELE REPORTAVA COMO DECLARADO O CAPITULO QUE O IRMAO DIZ
NAO TER LEVADO.** O `_capitulos_declarados` casava `capitulos N a M` em QUALQUER
lugar da copy, e a geracao antiga escreve, em prosa, um bloco
*"O QUE EU NAO LEVEI, de proposito, e vai escrito para a proxima rodada achar:
as quatro dzwignie que FUNCIONAM (capitulos 52 a 61)"*. O relato saia dizendo
*"capitulos que ele declara: 52 a 61"* — **o oposto do que a frase diz**, e no
`kolejny-poziom-s022` esse bloco e a UNICA citacao de capitulo da copy, logo
**10 de 10** dos "declarados" dele eram negados.

**E o custo e de PAUTA, nao de relato: capitulo que o irmao deixou de proposito
aparecia como consumido**, e e justamente a reserva que ele escreveu para a
rodada seguinte achar. Medido nas specs de SHORT SOLTO com copy, que e a
populacao que este modulo serve: **15 de 242** tinham capitulo negado contado
como declarado, e em duas delas (`kolejny-poziom-s022` e
`epomeno-epipedo-s022`) era a lista INTEIRA.

**Os 242 sao o RETRATO de 20/10, nao o estado de hoje:** a populacao cresce de
uma peca por rodada, e o que nao envelhece e a RAZAO — ~6% das specs. O teste
reconfere a razao contra o disco em vez do denominador, porque a primeira versao
dele cobrava uma janela ABSOLUTA sobre a populacao e expirou por PRODUCAO em
21/10 as 19:4x, reprovando com o acervo simplesmente maior (17 de 268 = 6,3%).

**TRES DETECTORES MEUS ERRARAM ANTES DO QUE MEDE, e os tres vao escritos porque
cada um erra de um jeito diferente:** por LINHA achei **1** caso (a negacao mora
uma linha acima da citacao); por PARAGRAFO, aceitando co-ocorrencia, achei
**37** (a maioria era bloco de numero `DESCARTADO` e contagem de reserva das
`## FONTES` — co-ocorrencia nao e negacao); e exigindo o marcador em **negrito**
achei **ZERO**, porque no acervo ele e prosa nua. O terceiro e o 17/10 outra vez:
instrumento que devolve vazio nao prova ausencia, e eu quase relatei que o
defeito nao existia depois de o ter visto na peca.

**O MARCADOR E UM SO E E MEDIDO, e os outros TRES ficaram de fora com o motivo:**
`DESCARTADO` (73 blocos), `ficaram FORA` (41) e `ficou FORA` (17) tambem citam
capitulo, e ali o capitulo e em boa parte a **PROCEDENCIA da recusa** — o
`kolejny-poziom-s074` cita os capitulos 9 e 12 para dizer por que o numero deles
nao entrou, isto e, ele LEU os dois. Excluir esses faria o contrario do conserto:
capitulo consumido voltaria a parecer livre, e a trava da regra (f) ficaria cega.
Seria detector que inventa achado (725), e por isso o conjunto e `MARCAS_DE_NEGACAO`
com UMA entrada e a medida ao lado.

**PONTO CEGO DECLARADO:** a negacao e PROSA, logo irmao que a escreva com outras
palavras nao e pego — e eu nao sei quantos sao, porque sabe-lo exigiria ler as
242 copies. O que esta medido e o marcador que o acervo repete.

**E NOMEAR EM VEZ DE FILTRAR:** o negado nao desaparece, sai em linha PROPRIA do
relato como RESERVA que o irmao deixou escrita — e irmao cujo declarado fica
VAZIO depois da exclusao **diz isso**, em vez de a linha sumir, porque linha que
desaparece se le como "ele nao declarou capitulo nenhum".

**O que ele NAO faz:** decidir se duas familias sao a mesma. Isso e leitura, e
nenhum limiar de similaridade de string distingue "o limiar e relativo" de "o
indicador mede renda e nao patrimonio" — as duas frases falam do mesmo limiar.
Ele poe o material na mesa; quem compara sou eu.
"""
import glob
import math
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# O DONO da contagem de capitulo do longo. Recontar aqui criaria o segundo dono
# do mesmo fato, que e a assinatura que congelou a legenda e parou a mira.
import segundo_angulo as SA   # noqa: E402

# Cabecalhos onde a familia pode estar escrita, em ordem de forca.
CAMPO_FAMILIA = "FAMILIA DE ENTRADA ERRADA"
# A geracao antiga nao tinha o campo e registrava em prosa nestes blocos.
BLOCOS_DE_PROSA = ("O QUE EU NAO LEVEI", "AVISO SOBRE OS NUMEROS", "AVISO")
# Marcador MEDIDO do bloco em que o irmao declara o que NAO levou: 19 ocorrencias
# nas 242 specs de short solto com copy. `DESCARTADO` (73 blocos), `ficaram FORA`
# (41) e `ficou FORA` (17) ficam de FORA de proposito — ali o capitulo citado e em
# boa parte a PROCEDENCIA da recusa de um NUMERO, isto e, capitulo que a peca LEU.
MARCAS_DE_NEGACAO = ("O QUE EU NAO LEVEI",)


def _secao(copy: str, nome: str) -> str:
    m = re.search(r"^##\s*" + re.escape(nome) + r"\s*$\n(.*?)(?=^##\s|\Z)",
                  copy, re.M | re.S)
    return (m.group(1).strip() if m else "")


def _titulo_curto(copy: str) -> str:
    m = re.search(r"^##\s*TITULO SHORT\s*$\n+(.+)$", copy, re.M)
    return m.group(1).strip() if m else ""


def _narracao(spec: dict) -> list:
    """A narracao do short do irmao, cena por cena — a fonte de PRIMEIRA mao.

    Ela e o que foi AO AR, e por isso nao depende de o autor ter escrito campo
    nem bloco de prosa.

    **O numero que morava aqui — "66 das 379 specs" — e o que o docstring do
    modulo RETRATA: as 66 eram PACOTES, que `irmaos()` nem considera irmao.**
    Ele ficou nesta funcao depois de retratado la em cima, o que e o 753 em
    forma de docstring: duas contas da mesma coisa, uma corrigida. Na populacao
    certa sao **242** specs de short solto com copy e **ZERO** ficam so com o
    titulo. Quem recontra isso e o teste, nao esta frase.
    """
    saida = []
    for c in (spec.get("short") or []):
        nar = (c.get("nar") or "").strip()
        if nar:
            saida.append(nar)
    return saida


# A PALAVRA "CAPITULO" EM CADA LINGUA DA FROTA, e ela entrou medida.
#
# Medido em 22/10 as 21:4x: das 293 copies de short solto, **181 citam
# capitulo** em alguma lingua e o padrao antigo pegava **136**. Dos 45
# perdidos, **UM** era de LINGUA (o `kolejny-poziom-s096`, cuja FONTES diz
# `rozdzialy 30, 31 i 32`) e **QUARENTA E QUATRO** eram de FORMA — a
# ENUMERACAO `capitulos 30, 31 e 32`, que nao e faixa nem capitulo unico.
#
# **Eu fui procurar o 725 (vocabulario de uma lingua lido como cobertura da
# frota) e encontrei outro defeito, maior.** O de lingua e a minoria; o de
# forma e 44 de 45, e vai dito nessa ordem.
PALAVRA_CAPITULO = r"(?:cap[ií]tulos?|rozdzia[lł](?:y|ow|ów|u)?|κεφ[αά]λαι[οα])"

# Quantos numeros uma enumeracao pode encadear. O limite existe contra o 725:
# sem ele, "capitulos 30, 31 e 32" seguido de uma frase cheia de numeros
# engoliria a frase inteira. Oito e o maior encadeamento OBSERVADO no acervo.
MAX_ENCADEADOS = 8


def _citados(trecho: str) -> set:
    """Todo capitulo que um trecho de prosa cita — sem julgar o sinal.

    TRES formas, e as tres medidas no acervo: a FAIXA (`N a M`), o capitulo
    UNICO (`capitulo N`) e a ENUMERACAO (`capitulos N, M e K`). A terceira
    entrou em 22/10 as 21:4x e e a que mais faltava — 44 dos 45 casos
    perdidos.

    **A enumeracao PARA no primeiro token que nao liga, e o `MAX_ENCADEADOS`
    existe contra o 725:** sem a parada, uma frase cheia de numeros depois da
    lista seria engolida inteira, e detector que inventa achado e pior que nao
    ter detector. Numero NU, sem a palavra antes, nao entra de jeito nenhum.
    """
    achados = set()
    for m in re.finditer(PALAVRA_CAPITULO + r"\s+(\d{1,3})\s*a\s*(\d{1,3})",
                         trecho, re.I):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b and b - a < 60:
            achados.update(range(a, b + 1))
    for m in re.finditer(PALAVRA_CAPITULO + r"\s+(\d{1,3})\b", trecho, re.I):
        achados.add(int(m.group(1)))
        # A ENUMERACAO continua do numero casado: so digitos ligados por
        # virgula ou pela conjuncao da lingua entram, e ela PARA no primeiro
        # token que nao e nenhum dos dois. Encadear sem parar seria o 725.
        resto = trecho[m.end():]
        for _ in range(MAX_ENCADEADOS):
            liga = re.match(r"\s*(?:,|;|\be\b|\bi\b|\band\b|\bκαι\b)"
                            r"\s*(\d{1,3})\b", resto, re.I)
            if not liga:
                break
            achados.add(int(liga.group(1)))
            resto = resto[liga.end():]
    return achados


def _blocos_de_negacao(copy: str) -> list:
    """Os intervalos de texto em que o irmao declara o que NAO levou.

    O marcador e PROSA NUA no acervo (exigir negrito devolveu ZERO), e o bloco
    vai dele ate o fim do PARAGRAFO — por linha a negacao fica de fora, porque
    ela mora uma linha acima da citacao.
    """
    saida = []
    for marca in MARCAS_DE_NEGACAO:
        for m in re.finditer(r"\*{0,2}" + re.escape(marca), copy, re.I):
            resto = copy[m.end():]
            fim = re.search(r"\n\s*\n|\n##\s", resto)
            saida.append((m.start(),
                          m.end() + (fim.start() if fim else len(resto))))
    return saida


def capitulos_negados(copy: str) -> list:
    """Os capitulos que a copy diz, em letra, NAO ter levado.

    Eles sao a RESERVA que o irmao deixou escrita para a rodada seguinte achar,
    e e por isso que saem NOMEADOS em vez de apenas descontados.
    """
    negados = set()
    for a, b in _blocos_de_negacao(copy):
        negados |= _citados(copy[a:b])
    return sorted(negados)


def _sem_reserva(copy: str) -> str:
    """A copy sem a secao `## RESERVA`, porque ali capitulo citado e o AVESSO.

    **Medido em 22/10 as 21:4x, e e um falso positivo que ja existia:** das 26
    copies com secao `## RESERVA`, **DEZESSEIS** tinham capitulos dela contados
    como DECLARADOS — e a reserva diz, em letra, `LIVRES os capitulos N e M`,
    isto e o oposto de usado. Contar aquilo faria a rodada seguinte PULAR
    justamente o que o irmao deixou livre.

    A secao INTEIRA sai, em vez de se subtrair o conjunto dela: capitulo pode
    aparecer legitimamente nas FONTES **e** na reserva (como *"NAO LEVAR, e
    territorio do sNNN"*), e subtrair o conjunto apagaria o uso legitimo.

    E o conteudo da reserva NAO e reparseado aqui: o dono dele e o
    `reservas_escritas`, e refazer a leitura criaria o segundo dono.
    """
    m = re.search(r"^##\s*RESERVA\s*$.*?(?=^##\s|\Z)", copy, re.M | re.S)
    return (copy[:m.start()] + copy[m.end():]) if m else copy


def _capitulos_declarados(copy: str) -> list:
    """Numeros que a copy diz ter USADO — a geracao antiga os escreve em prosa.

    Capitulo citado dentro de um bloco de negacao **nao entra**: ate 20/10 as
    17:4x entrava, e o relato dizia *"capitulos que ele declara: 52 a 61"* de um
    bloco cuja frase e *"o que eu NAO levei"*. E desde 22/10 as 21:4x a secao
    `## RESERVA` inteira tambem fica fora, pelo `_sem_reserva`.
    """
    corpo = _sem_reserva(copy)
    return sorted(_citados(corpo) - set(capitulos_negados(corpo)))


def frases_que_citam_irmao(copy: str, pacotes: list) -> list:
    """As frases da copy que NOMEIAM outro pacote de short.

    E o sinal mais direto que a geracao antiga deixou: o `s023` escreve
    *"essa familia JA foi usada pelo `s001`"* no meio de um bloco de prosa, e foi
    isso que salvou o `s035`. Truncar o bloco por tamanho cortava exatamente esta
    frase, entao o modulo procura a MENCAO em vez de imprimir o bloco inteiro.
    """
    alvos = [re.escape(p.split("-")[-1]) for p in pacotes]
    if not alvos:
        return []
    padrao = re.compile(r"(?<![\w-])`?(?:" + "|".join(alvos) + r")`?(?![\w-])")
    saida = []
    for frase in re.split(r"(?<=[.;!?])\s+", " ".join(copy.split())):
        if padrao.search(frase) and len(frase) > 20:
            saida.append(frase.strip())
    return saida


def irmaos(origem: str, raiz=None, dir_specs=None) -> list:
    """Um dict por spec de short que declara `longo_existente == origem`.

    **A guarda de vacuidade e DELEGADA ao `segundo_angulo._dir_valido`**, que e
    o dono dela desde 20/10 as 12:3x: sem ela, diretorio errado devolve lista
    VAZIA e bem formada. Medido em 22/10 as 12:4x, quando eu passei `dir_specs`
    na posicao de `raiz` e a resposta vazia (`n = 0`) passou por "origem sem
    irmaos" — e e por isso que ela LEVANTA em vez de responder zero.

    **E `dir_specs` entrou como argomento PROPRIO na mesma rodada, e o motivo e
    uma regressao minha:** a primeira versao do conserto derivava a raiz do
    `dir_specs` por convencao, e o `segundo_angulo` passa diretorio ARBITRARIO
    (parque proprio de teste, `tmp_path`). Exigir a convencao `fabrica/specs`
    quebrou o `texto_dos_livres` para todo chamador que nao a cumpre — pego pela
    suite, 26 falhas contra 25. Quando ele vem, ele VENCE a raiz; a derivacao
    pela raiz fica para quem chama sem ele.
    """
    specs = dir_specs or os.path.join(raiz or RAIZ, "fabrica", "specs")
    SA._dir_valido(specs)
    saida = []
    for f in sorted(glob.glob(os.path.join(specs, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo_existente") != origem or d.get("longo"):
            continue
        copy = d.get("copy", "") or ""
        familia = _secao(copy, CAMPO_FAMILIA)
        saida.append({
            "pacote": d.get("pacote", os.path.basename(f)[:-5]),
            "titulo_curto": _titulo_curto(copy),
            "familia": familia,
            "tem_campo_familia": bool(familia),
            "prosa": {b: _secao(copy, b) for b in BLOCOS_DE_PROSA
                      if _secao(copy, b)},
            "capitulos_declarados": _capitulos_declarados(copy),
            # A reserva que ele deixou ESCRITA. Ate 20/10 as 17:4x ela entrava
            # em `capitulos_declarados`, isto e, aparecia como consumida.
            "capitulos_negados": capitulos_negados(copy),
            # PRIMEIRA mao: o que a peca do irmao de fato fala. Sem isto o
            # irmao de geracao antiga entregava so o titulo (20/10, 15:3x).
            "narracao": _narracao(d),
            "_copy": copy,
        })
    return saida


# Quantos capitulos uma familia costuma carregar. OBSERVADO nas copies que
# declaram capitulo, nao escolhido — e so isso que ele e: o tamanho tipico da
# aposta, usado para dizer a ORDEM DE GRANDEZA da forca da evidencia.
FAMILIA_TIPICA = 5


def forca_da_ausencia(declarados: int, n_capitulos: int,
                      familia: int = FAMILIA_TIPICA) -> float | None:
    """Se os capitulos fossem SORTEADOS, qual a chance de colidir com o irmao?

    **POR QUE EXISTE (21/10 as 01:3x).** O `cobertura_dos_capitulos` nasceu uma
    rodada antes e diz *"nenhuma sobreposicao entre os declarados e os seus"* —
    **sem o denominador.** Medido nos 103 irmaos que declaram capitulo em
    origem de 20+ capitulos, a fracao do longo que um irmao reivindica vai de
    **1% a 62%** (mediana 9,7%). Logo *"nenhuma sobreposicao"* nao quer dizer a
    mesma coisa em dois irmaos:

    * irmao que declara **1 de 100**: sob sorteio, a chance de colidir com uma
      familia de cinco capitulos e **0,05** — "nao colidiu" era quase certo por
      construcao, e prova quase nada;
    * irmao que declara **40 de 64**: a chance e **0,99** — ai "nao colidiu" e
      sinal forte.

    A mediana dos 103 e **0,41**, isto e, a metade dos irmaos esta numa faixa em
    que o resultado binario nao se interpreta sozinho. **E a primeira linha da
    disciplina da rotina aplicada ao meu proprio instrumento de um dia:** antes
    de chamar um achado de achado, pergunte se o instrumento pode produzi-lo.

    **O MODELO VAI DECLARADO COMO MODELO, e ele e FALSO de proposito:** capitulo
    de familia NAO e sorteado — ele vem em bloco contiguo, como os 50 a 57 desta
    rodada mostram. Logo este numero e **ordem de grandeza sob uma nula
    explicita**, nunca probabilidade de coisa nenhuma no mundo. Tratar como
    probabilidade medida seria o erro inverso do que ele conserta.
    """
    if n_capitulos <= 0 or declarados <= 0:
        return None
    if n_capitulos - declarados < familia:
        return 1.0
    return 1.0 - (math.comb(n_capitulos - declarados, familia)
                  / float(math.comb(n_capitulos, familia)))


def _dir_specs(raiz=None) -> str:
    """O diretorio das specs, derivado da raiz — UM dono.

    Existe porque `segundo_angulo.nao_mencionados` recebe `dir_specs` e nao
    `raiz`, e passar um no lugar do outro e exatamente o que a guarda
    `_dir_valido` de 20/10 as 12:3x pega. Derivar aqui, num lugar so, e o que
    impede a proxima chamada de errar a posicao outra vez.
    """
    return os.path.join(raiz or RAIZ, "fabrica", "specs")


def cobertura_dos_capitulos(origem: str, meus=(), raiz=None, excluir=()) -> dict:
    """Em quantos irmaos a conferencia por CAPITULO e mecanica, e em quantos nao.

    **POR QUE EXISTE (20/10 as 23:4x).** Eu escrevo em TODA copy uma frase da
    forma *"nenhum dos tres toca os capitulos 38 a 45 — conferido short por
    short"*. Ela soa como verificacao uniforme, e nao e: o capitulo declarado
    sai da PROSA da copy do irmao, e **146 das 248 specs de short solto do disco
    nao declaram capitulo nenhum**. Para essas a unica rota e LER a narracao e
    julgar — o que e legitimo e e outro ato.

    **Medido nas cinco origens que esta sessao usou:** dos irmaos delas, so
    **1 de 4**, 2 de 4, 4 de 6, 2 de 4 e 1 de 4 tem capitulo declarado. Isto e,
    na maioria dos casos a frase que eu escrevo cobre uma MINORIA dos irmaos
    pela rota mecanica, e o resto pela leitura.

    **O que ele NAO faz, e a trava e a do 776:** sobreposicao de capitulo NAO e
    familia repetida — *capitulo livre nao e familia livre*, e a reciproca
    tambem nao vale. Ele devolve a sobreposicao como MOTIVO PARA LER, nunca como
    veredito, e quem decide familia sou eu lendo. Ele tambem nao conta como
    "sem sobreposicao" o irmao cujos capitulos sao DESCONHECIDOS: ausencia de
    dado nao e ausencia de colisao, que e o erro que custou o 761.
    """
    meus = set(int(x) for x in (meus or ()))
    # O tamanho do longo sai do DONO da contagem de capitulo
    # (`segundo_angulo.nao_mencionados`), nao de uma leitura propria: recontar
    # aqui criaria o segundo dono, a assinatura que congelou a legenda.
    #
    # E O ARGUMENTO DELE E `dir_specs`, NAO `raiz` — eu passei a raiz na
    # primeira versao disto e envolvi a chamada num `except Exception`, que
    # ENGOLIU a guarda `_dir_valido` de 20/10 as 12:3x. Aquela guarda nasceu
    # para LEVANTAR em vez de devolver zero bem formado, e o meu try/except a
    # transformou de volta em silencio: `n_capitulos` saia 0 e a forca saia
    # `None` para todo irmao, calada. Guarda engolida por chamador e guarda que
    # nao existe.
    n_caps = (SA.nao_mencionados(origem, _dir_specs(raiz)) or {}).get(
        "n_capitulos") or 0
    saida = {"conhecidos": [], "desconhecidos": [], "colidem": [], "forca": {}}
    # `excluir` NAO e conveniencia: a spec desta rodada ja esta no disco quando
    # eu pergunto, logo sem ele a peca aparece como irma de si mesma e colide
    # com os PROPRIOS capitulos. E a QUINTA vez desta assinatura — o
    # `variedade._especs_do_canal`, o `concentracao.contagem`, o
    # `esqueleto_entre_canais.novidade` e o `segundo_angulo` carregam o mesmo
    # parametro pelo mesmo motivo, e o `relato` daqui o chama de `excluir`.
    for i in irmaos(origem, raiz):
        if i["pacote"] in excluir:
            continue
        caps = set(i["capitulos_declarados"])
        if not caps:
            saida["desconhecidos"].append(i["pacote"])
            continue
        saida["conhecidos"].append(i["pacote"])
        # A FORCA da ausencia, por irmao: "nao colidiu" nao quer dizer a mesma
        # coisa quando o irmao declara 1 de 100 e quando declara 40 de 64.
        # Ver `forca_da_ausencia` — 21/10 as 01:3x.
        saida["forca"][i["pacote"]] = {
            "declarados": len(caps),
            "n_capitulos": n_caps,
            "p_colidiria": forca_da_ausencia(len(caps), n_caps),
        }
        inter = sorted(caps & meus)
        if inter:
            saida["colidem"].append({"pacote": i["pacote"], "capitulos": inter})
    n = len(saida["conhecidos"]) + len(saida["desconhecidos"])
    saida["irmaos"] = n
    saida["fracao_mecanica"] = (len(saida["conhecidos"]) / float(n)) if n else 0.0
    return saida


def _linha_da_cobertura(origem: str, meus=(), raiz=None, excluir=()) -> list:
    """A frase da cobertura, com UM dono, e ela sai nos DOIS ramos.

    Sair so quando ha irmao desconhecido faria a linha CALAR na origem em que a
    conferencia E mecanica — e e ali que a frase da copy pode ser escrita sem
    ressalva. E o ramo que cala quando importa (13:2x).
    """
    c = cobertura_dos_capitulos(origem, meus, raiz, excluir)
    if not c["irmaos"]:
        return []
    L = [f"  COBERTURA POR CAPITULO: {len(c['conhecidos'])} de {c['irmaos']}"
         f" irmao(s) declaram capitulo, logo a conferencia mecanica alcanca"
         f" {100 * c['fracao_mecanica']:.0f}% deles."]
    if c["desconhecidos"]:
        L.append("    sem capitulo declarado (so por LEITURA da narracao): "
                 + ", ".join(c["desconhecidos"])
                 + ". Nao conte estes como 'sem sobreposicao': ausencia de dado"
                   " nao e ausencia de colisao (761).")
    else:
        L.append("    TODOS declaram, logo aqui a frase da copy pode dizer"
                 " 'conferido por capitulo' sem ressalva.")
    if c["colidem"]:
        for x in c["colidem"]:
            L.append(f"    SOBREPOSICAO com {x['pacote']}: capitulos"
                     f" {x['capitulos'][0]} a {x['capitulos'][-1]}. Isto e"
                     " MOTIVO PARA LER, nao veredito — capitulo livre nao e"
                     " familia livre, e a reciproca tambem nao (776).")
    elif not meus:
        # Sem `meus` nao existe sobreposicao a declarar, e dizer "nenhuma"
        # aqui seria afirmar sobre um conjunto vazio — o verde fabricado do
        # §3.8 na forma mais barata.
        L.append("    sobreposicao NAO conferida: a pauta ainda nao escolheu"
                 " capitulo, e com `meus` vazio dizer 'nenhuma' seria afirmar"
                 " sobre conjunto vazio.")
    elif c["conhecidos"]:
        L.append("    nenhuma sobreposicao entre os declarados e os seus.")
        L.extend(_linha_da_forca(c))
    return L


def _linha_da_forca(c: dict) -> list:
    """Quanto vale o "nenhuma sobreposicao" — UM dono da frase.

    Sem isto o relato devolve um BINARIO cuja forca varia por um fator 20 entre
    irmaos (P de 0,05 a 0,99, medido nos 103 que declaram capitulo). Ele NAO
    filtra e NAO decide: nomeia a forca, como o `origens_sem_uso` nomeia origem
    inutilizavel em vez de a esconder.
    """
    fr = c.get("forca") or {}
    ps = [v["p_colidiria"] for v in fr.values()
          if v.get("p_colidiria") is not None]
    if not ps:
        return ["      (forca da ausencia NAO calculada: o tamanho do longo nao"
                " foi lido. Ausencia de denominador nao e denominador grande.)"]
    L = []
    for pac in sorted(fr):
        v = fr[pac]
        pc = v["p_colidiria"]
        if pc is None:
            continue
        L.append("      %s declara %d de %d capitulos, logo sob SORTEIO a"
                 " colisao com uma familia de %d teria P=%.2f."
                 % (pac, v["declarados"], v["n_capitulos"],
                    FAMILIA_TIPICA, pc))
    pior = max(ps)
    if pior < 0.25:
        L.append("      >> ATENCAO: a maior P e %.2f, logo 'nenhuma"
                 " sobreposicao' era QUASE CERTO por construcao e prova"
                 " pouco. A conferencia que vale aqui e a LEITURA." % pior)
    elif pior >= 0.75:
        L.append("      >> a maior P e %.2f, logo 'nenhuma sobreposicao' e"
                 " sinal FORTE: sob sorteio ela quase certamente teria"
                 " ocorrido." % pior)
    L.append("      (o SORTEIO e nula DECLARADA e FALSA de proposito: capitulo"
             " de familia vem em bloco contiguo. Isto e ordem de grandeza da"
             " forca, nunca probabilidade do mundo.)")
    return L


def sem_campo(origem: str, raiz=None) -> list:
    return [i["pacote"] for i in irmaos(origem, raiz)
            if not i["tem_campo_familia"]]


def _linha_dos_capitulos(i: dict) -> str:
    """A linha dos capitulos declarados, com UM dono.

    O ramo vazio existe porque ele e o caso MEDIDO: no `kolejny-poziom-s022` a
    unica citacao de capitulo da copy mora dentro do bloco de negacao, logo
    depois do conserto o declarado dele e VAZIO. Deixar a linha desaparecer ali
    se leria como "ele nao declarou capitulo nenhum", que e o sentido
    PERMISSIVO: quem lesse concluiria que a origem esta livre.
    """
    cs = i["capitulos_declarados"]
    if cs:
        return (f"    capitulos que ele declara: {cs[0]} a {cs[-1]}"
                f" ({len(cs)} citados)")
    if i["capitulos_negados"]:
        return ("    capitulos que ele declara: NENHUM — toda citacao de"
                " capitulo da copy dele esta dentro do bloco do que ele NAO"
                " levou, logo a familia dele sai do TITULO, da PROSA e da"
                " NARRACAO, nao dos capitulos.")
    return ("    capitulos que ele declara: nenhum citado na copy — compare"
            " pelo TITULO e pela NARRACAO.")


def relato(origem: str, raiz=None, excluir=(), meus=()) -> str:
    todos = [i for i in irmaos(origem, raiz) if i["pacote"] not in excluir]
    if not todos:
        return (f"IRMAOS de {origem}: NENHUM. Origem virgem — a regra (f) nao tem"
                " contra o que comparar nesta origem, mas o CANAL tem: confira as"
                " familias das outras pecas do canal do mesmo dia.")
    linhas = [f"IRMAOS de {origem}: {len(todos)}."]
    faltam = []
    for i in todos:
        linhas.append(f"  {i['pacote']} — titulo curto: {i['titulo_curto']!r}")
        if i["tem_campo_familia"]:
            linhas.append("    familia (campo): "
                          + " ".join(i["familia"].split())[:220])
        else:
            faltam.append(i["pacote"])
            linhas.append("    familia (campo): **AUSENTE** — geracao anterior")
        linhas.append(_linha_dos_capitulos(i))
        if i["capitulos_negados"]:
            ns = i["capitulos_negados"]
            linhas.append(
                f"    capitulos que ele diz NAO ter levado: {ns[0]} a {ns[-1]}"
                f" ({len(ns)} citados) — RESERVA que ele deixou escrita para a"
                " rodada seguinte achar, e que ate 20/10 as 17:4x este relato"
                " contava como DECLARADA.")
    if faltam:
        linhas.append(
            "  ATENCAO: " + ", ".join(faltam) + " NAO tem o campo"
            f" `## {CAMPO_FAMILIA}`. **Ausencia de campo NAO e ausencia de"
            " familia** — foi exatamente assim que eu quase repeti a familia do"
            " `epomeno-epipedo-s023` em 15/10 (776). Compare pelo TITULO CURTO e"
            " leia a PROSA abaixo, que e onde a geracao antiga a registrava."
            " **E leia a NARRACAO deles, que vai logo abaixo: ela e de PRIMEIRA"
            " mao.** Frase de irmao citando irmao e resumo de TERCEIRO, e"
            " compressao feita por outro guarda o eixo que interessava a ELE —"
            " foi assim que o `s010` apareceu tres vezes como *ordem de"
            " contratacao* enquanto a propria narracao dele dizia *o preco cai"
            " porque o escopo encolheu* (20/10, 15:3x).")
        for i in todos:
            if i["tem_campo_familia"]:
                # o campo e o DONO quando existe; imprimir a narracao ao lado
                # dele criaria o segundo dono da familia.
                continue
            if not i["narracao"]:
                linhas.append(
                    f"    [{i['pacote']} | PRIMEIRA mao] sem narracao na spec —"
                    " aqui so o titulo sobra mesmo, e a copy inteira e o"
                    " caminho.")
                continue
            for nome_bloco, texto in sorted(i["prosa"].items()):
                linhas.append(
                    f"    [{i['pacote']} | PROSA '{nome_bloco}'] o bloco"
                    " INTEIRO, que a linha acima promete e que o relato nao"
                    " imprimia ate 20/10:")
                for par in texto.split("\n\n"):
                    par = " ".join(par.split())
                    if par:
                        linhas.append(f"      > {par}")
            linhas.append(
                f"    [{i['pacote']} | NARRACAO, primeira mao] o que a peca dele"
                " FALA, cena por cena, sem truncar:")
            for n in i["narracao"]:
                linhas.append(f"      . {n}")
        nomes = [i["pacote"] for i in todos]
        achou_mencao = False
        for i in todos:
            copy_i = i.get("_copy", "")
            outros = [n for n in nomes if n != i["pacote"]]
            for frase in frases_que_citam_irmao(copy_i, outros):
                achou_mencao = True
                linhas.append(
                    f"    [{i['pacote']} CITA outro irmao | SEGUNDA mao]"
                    f" {frase}")
        if not achou_mencao:
            linhas.append(
                "    nenhum irmao CITA outro pelo nome — entao o titulo curto e"
                " o unico comparador que sobra, e leia a copy do irmao inteira"
                " antes de escrever.")
    linhas.extend(_linha_da_cobertura(origem, meus, raiz, excluir))
    linhas.append(
        "  (isto NAO decide se duas familias sao a mesma: nenhum limiar de"
        " string distingue duas frases sobre o MESMO limiar. Poe o material na"
        " mesa; a comparacao e leitura.)")
    linhas.append(
        "  (e capitulo livre NAO e familia livre: o `segundo_angulo` compara"
        " CAPITULOS, e sao perguntas diferentes.)")
    return "\n".join(linhas)


if __name__ == "__main__":
    import sys
    print(relato(sys.argv[1] if len(sys.argv) > 1 else "eimuyGaCor8"))
