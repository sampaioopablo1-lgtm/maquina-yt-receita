#!/usr/bin/env python3
"""O esqueleto repete ENTRE canais, e o portao compara DENTRO de um.

Por que este modulo existe, e sao duas razoes, nao uma.

A PRIMEIRA e o item 3 da §10: toda conta que eu faco a mao vira um erro meu.
Eu venho escrevendo, no relato de cada rodada e no `CLAUDE.md`, frases como
"esqueleto inedito nas 116 formas da frota" e "a frota nao tinha nenhuma peca
de doze cenas" — e cada uma dessas frases saiu de um laco Python descartavel
escrito na hora, sobre o `glob` das specs. Conferido depois, os numeros que eu
escrevi estavam CERTOS (113 em 20:1x de 19/10 mais tres pecas da e 116 em
23:1x, mais tres = 119 hoje), logo o defeito nao e numero errado. O defeito e
que a pergunta era escrita a mao junto com o laco, e por isso eu so respondia
a pergunta que me ocorria digitar.

A SEGUNDA e a que apareceu na PRIMEIRA execucao deste modulo, e e dela que
sai o valor: a pergunta que nunca me ocorreu digitar e a do DONO. Palavras
dele em 19/10: "os videos publicados me parecem todos a mesma dinamica,
imagens, formas, estilo. EM TODOS OS CANAIS." O "em todos os canais" e uma
dimensao que o portao `variedade` NAO PODE ver: o `_especs_do_canal` dele
filtra `slug == slug`, logo ele conta esqueleto repetido DENTRO do canal e e
cego para forma que atravessa canal. Medido no disco:

    | | |
    |---|---|
    | specs com short | 366 |
    | formas DISTINTAS | 119 |
    | formas presentes em MAIS DE UM canal | 34 |
    | pecas nessas formas | 271 = 74% |
    | a mais repetida, `titulo-titulo-titulo-titulo-cta` | 82 pecas, ONZE canais |

Nos tres canais VIVOS o quadro nao se dissolve: 276 pecas, 106 formas, 26
atravessando canal e 186 pecas (67%) nelas, com a mesma forma no topo (58
pecas, os tres canais). Isto e o 762 numa dimensao nova — la eu concentrei
producao num canal sem ver; aqui a FORMA atravessa os canais sem ninguem
contar.

O que isto NAO afirma: que forma compartilhada seja defeito por si. Peca de
cinco cenas tem poucas sequencias possiveis, e `titulo-...-cta` e a moldura de
todas elas. O que esta medido e a NEGACAO da leitura confortavel: nao se pode
dizer "o esqueleto esta variado" olhando o aviso do portao, porque ele mede
outra coisa.

NAO E PORTAO, pelo argumento do `mira.py`: ele reprovaria 271 specs, que sao
acervo e nao producao. Aviso que reprova 271 vezes deixa de avisar. O codigo
de saida e SEMPRE zero.

E a ASSINATURA sai de `variedade.esqueleto`, que e o dono dela desde que o
portao existe. Reescrever o `"-".join(...)` aqui criaria o segundo dono da
mesma regra — a assinatura que congelou a legenda, parou a mira de conferir
por seis pecas e pos job inventado na serie. Ha teste por AST cobrando isso.
"""
import collections
import glob
import math
import random
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cenas_da_spec as _CS
import nome_da_spec as NS   # noqa: E402  — UM dono do nome da spec
import variedade as V  # noqa: E402  — DONO da assinatura do esqueleto

DIR_SPECS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs")

# Os tres canais da frota. Lista DECLARADA e nao derivada, porque "vivo" e
# estado do negocio e nao propriedade do disco: canal parado continua tendo
# spec. Ela existe para separar ACERVO de PRODUCAO, que e a licao do 762 —
# acervo dilui rodada.
CANAIS_VIVOS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def _canal_da_spec(d: dict) -> str:
    """O canal de uma spec, delegado ao dono UNICO (`canal.da_spec`)."""
    import canal
    return canal.da_spec(d)


def varre(dir_specs: str = None) -> list[dict]:
    """Toda spec do disco que tem short, com canal, contagem e esqueleto.

    Levanta se nao achar nenhuma: varredura vazia que devolve lista vazia faz
    todo teste passar por vacuidade, que e o defeito do 743 em forma de glob.
    """
    dir_specs = dir_specs or DIR_SPECS
    saida = []
    for f in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        short = d.get("short") or []
        if not short:
            continue
        saida.append({
            "arquivo": os.path.basename(f),
            "canal": _canal_da_spec(d),
            "cenas": len(short),
            "esqueleto": V.esqueleto(short),
        })
    if not saida:
        raise RuntimeError(
            f"AUSENCIA DE LEITURA: nenhuma spec com short em {dir_specs}. "
            "Varredura vazia nao e 'frota sem esqueleto' — e instrumento sem "
            "dado, e devolver zero aqui faria todo teste passar por vacuidade."
        )
    return saida


def quadro(pecas: list[dict] = None, so_vivos: bool = False) -> dict:
    """As contagens que eu vinha escrevendo a mao, todas de uma vez."""
    pecas = pecas if pecas is not None else varre()
    if so_vivos:
        pecas = [p for p in pecas if p["canal"] in CANAIS_VIVOS]
    canais = collections.defaultdict(set)
    formas = collections.Counter()
    por_n = collections.Counter()
    formas_por_n = collections.defaultdict(set)
    for p in pecas:
        formas[p["esqueleto"]] += 1
        canais[p["esqueleto"]].add(p["canal"])
        por_n[p["cenas"]] += 1
        formas_por_n[p["cenas"]].add(p["esqueleto"])
    atravessam = {e for e, s in canais.items() if len(s) > 1}
    n_atravessadas = sum(formas[e] for e in atravessam)
    return {
        "pecas": len(pecas),
        "formas": len(formas),
        "formas_que_atravessam": len(atravessam),
        "pecas_em_forma_que_atravessa": n_atravessadas,
        "fracao_atravessada": (n_atravessadas / len(pecas)) if pecas else 0.0,
        "por_contagem_de_cena": dict(sorted(por_n.items())),
        # Quantas FORMAS distintas existem em cada tamanho — nao quantas pecas.
        # As duas ocupam o MESMO lugar na minha frase e divergem por um fator
        # de ate 5,5 (34 pecas contra 7 formas em seis cenas, 149 contra 65 em
        # dez): e o 753 em forma de UNIDADE.
        "formas_por_contagem_de_cena": {
            n: sorted(s) for n, s in sorted(formas_por_n.items())},
        "canais_da_forma": {e: sorted(s) for e, s in canais.items()},
        "contagem_da_forma": dict(formas),
    }


def cegas_para_o_portao(pecas: list[dict] = None) -> dict:
    """As formas que atravessam canal e que o portao `variedade` NAO PODE ver.

    E este o numero que importa, e ele e mais agudo que a fracao: o portao
    avisa a partir de `variedade.ESQUELETO_AVISA_EM` pecas iguais DENTRO de um
    canal, logo forma que aparece uma vez em cada de oito canais nunca o faz
    disparar. Medido no disco: das 34 formas que atravessam canal, **33 sao
    invisiveis** ao portao, e elas levam 189 pecas.

    O limiar e LIDO de `variedade.ESQUELETO_AVISA_EM` e nao copiado — seria o
    segundo dono do mesmo numero, que e a assinatura da semana. Se alguem
    baixar o limiar do portao, este instrumento acompanha sozinho.
    """
    pecas = pecas if pecas is not None else varre()
    q = quadro(pecas)
    cegas, vistas = [], []
    for esq, canais in q["canais_da_forma"].items():
        if len(canais) < 2:
            continue
        por = collections.Counter(
            p["canal"] for p in pecas if p["esqueleto"] == esq)
        (cegas if max(por.values()) < V.ESQUELETO_AVISA_EM
         else vistas).append(esq)
    return {
        "limiar_do_portao": V.ESQUELETO_AVISA_EM,
        "atravessam": len(cegas) + len(vistas),
        "cegas": sorted(cegas),
        "vistas_por_acidente": sorted(vistas),
        "pecas_cegas": sum(q["contagem_da_forma"][e] for e in cegas),
    }


def sem(pecas: list[dict], exceto: str) -> list[dict]:
    """A populacao SEM a peca que esta sendo perguntada. UM dono do filtro.

    **Medido em 22/10 as 11:4x, no relato desta rodada: a linha do ACERVO e a
    da NOVIDADE, no MESMO relato, discordavam sobre quantas formas a frota
    tem.** Com a spec no disco, o relato imprimia `acervo: 424 pecas, 177
    formas` e, duas linhas abaixo, `esqueleto INEDITO nas 176 formas de short
    da frota` — porque so a frase da novidade filtrava a propria peca, e as
    outras tres contas leiam `varre()` cru. E o **753 dentro de um relato**, a
    mesma forma da banda cravada no texto do `mira` e da linha do piso que nao
    dizia de quantos mundos ela era.

    **E a divergencia aparece justamente quando a rodada ACERTA:** as duas
    linhas so discordam na contagem de FORMAS quando a peca e o UNICO exemplar
    da propria forma, que e o alvo de toda rodada. Medido no disco, **137 de
    424 pecas (32,3%)** estao nesse caso — e a linha de PECAS discorda
    SEMPRE, em 424 de 424, porque a peca perguntada esta sempre dentro do
    `varre()`.

    O `exceto` e o nome do arquivo e o casamento e DELEGADO ao
    `nome_da_spec.casa`, que e o dono das duas convencoes de nome (20/10 as
    11:3x). Sem `exceto` a lista volta como veio: ausencia de nome nao e
    ausencia de peca.
    """
    if not exceto:
        return pecas
    return [p for p in pecas if not NS.casa(p["arquivo"], exceto)]


def novidade(esq: str, cenas: int, pecas: list[dict] = None,
             exceto: str = "") -> dict:
    """Esta forma e nova? E este TAMANHO? — a frase do relato, derivada.

    Responde as duas perguntas que eu escrevia a mao em cada rodada, e a
    TERCEIRA que eu nunca escrevia: em quantos CANAIS esta forma ja vive.

    **E EM 20/10 AS 18:4x ENTROU A QUARTA, que eu escrevia a mao em TODA
    rodada: quantas FORMAS distintas existem neste TAMANHO de cena.** Eu venho
    escrevendo na copy *"inedito nas SETE formas de onze cenas"*, *"as DUAS
    formas de sete cenas"*, *"a TERCEIRA forma de oito cenas"* — e o modulo
    devolvia `exemplares_do_tamanho`, que e o numero de PECAS. As duas
    grandezas ocupam o MESMO lugar na frase e divergem por um fator de ate
    **5,5**: em seis cenas sao **34 pecas** e **7 formas**; em dez, **149** e
    **65**. E o 753 em forma de UNIDADE, como `cadencia` estimada contra real
    (02:2x) e como `alvo` no orcamento (19/10, 15:2x).

    **E AS CINCO AFIRMACOES DO ACERVO FORAM RECONFERIDAS CONTRA O DISCO, e as
    CINCO estao CERTAS** — `epomeno-epipedo-s070` (catorze formas de nove),
    `kolejny-poziom-s071` (sete de onze), `labtreinamento-s089` (duas de sete),
    `-s091` (cinco de seis) e `-s092` (tres de sete). **Logo isto nao e um
    numero errado publicado, e vai dito assim em vez de inflado:** e uma conta
    que eu acertei cinco vezes a mao, com o numero ERRADO para a mesma frase
    disponivel no campo vizinho. O item 3 da §10 nao fala do acerto, fala da
    sexta vez.

    **E EM 21/10 AS 00:4x ELE ACEITOU OS DOIS ARGUMENTOS TROCADOS e devolveu
    resposta BEM FORMADA sobre OUTRA pergunta.** Eu chamei
    `novidade("labtreinamento", "titulo-lista-item-barras-item-titulo-item-cta")`
    — canal no lugar do esqueleto e esqueleto no lugar da contagem — e ele
    respondeu `forma_inedita=True`, `tamanho_inedito=True`,
    `exemplares_do_tamanho=0`. **As duas metades sairam "NOVO", que e a direcao
    PERMISSIVA**, e eu ia escrever isso na copy: a resposta era sobre um
    esqueleto chamado *labtreinamento* e um tamanho de cena que e uma string.

    **A CAUSA e que as duas contas comparam por IGUALDADE, e igualdade nunca
    levanta.** `contagem_da_forma.get(esq, 0)` e a contagem por cenas com tipo
    errado simplesmente NAO CASAM, e "nao casou" e exatamente a resposta
    *inedito*. Medido nos oito pares (texto, numero) adjacentes da fabrica que
    eu consigo chamar sem banco: **SETE LEVANTAM** com os argumentos trocados —
    `TypeError` na aritmetica do `ensaio` e do `mira`, `KeyError` na tabela de
    vozes, `AttributeError` no `legenda`, `ValueError` no `contagem_de_cenas` —
    **e so este CALAVA.** Logo isto nao e defeito de familia e vai dito assim
    em vez de inflado: aritmetica e busca em tabela se defendem sozinhas,
    comparacao por IGUALDADE nao.

    **A REGRA QUE FICA: funcao que so compara por IGUALDADE nao se defende
    sozinha, e precisa conferir o TIPO na porta.** E a guarda e de TIPO e nao de
    coerencia: os dois argumentos NAO sao redundantes — a frota tem forma
    inedita com tamanho repetido e o contrario, e ha teste que chama esqueleto
    inventado com contagem real de proposito.

    `exceto` e o nome do arquivo da propria peca, e ele NAO e conveniencia: a
    spec desta rodada ja esta no disco quando eu pergunto, logo sem ele
    "inedito" nunca pode ser verdade e o relato diz "JA EXISTE: 1 exemplar"
    de uma peca que e o proprio unico exemplar. O `variedade._especs_do_canal`
    carrega o mesmo parametro pela mesma razao, e foi dele que eu copiei a
    forma depois de a primeira execucao daqui mostrar o defeito.
    """
    # A guarda e de TIPO porque as duas contas comparam por IGUALDADE, e
    # igualdade com tipo errado nao levanta: ela devolve "nao casou", que e a
    # resposta `inedito`. E ela vem ANTES da varredura, para chamada errada nao
    # pagar a leitura do disco. Ver o docstring — 21/10 as 00:4x.
    if not isinstance(esq, str):
        raise TypeError(
            "`esq` tem de ser o ESQUELETO (texto), e veio %r (%s). Os dois"
            " primeiros argumentos sao (esqueleto, contagem de cenas) nesta"
            " ORDEM; trocados, as duas metades saem 'NOVO' sem medir nada."
            % (esq, type(esq).__name__))
    if isinstance(cenas, bool) or not isinstance(cenas, int):
        raise TypeError(
            "`cenas` tem de ser a CONTAGEM de cenas (inteiro), e veio %r (%s)."
            " Os dois primeiros argumentos sao (esqueleto, contagem de cenas)"
            " nesta ORDEM; trocados, as duas metades saem 'NOVO' sem medir"
            " nada." % (cenas, type(cenas).__name__))
    pecas = pecas if pecas is not None else varre()
    pecas = sem(pecas, exceto)
    q = quadro(pecas)
    iguais = q["contagem_da_forma"].get(esq, 0)
    canais = q["canais_da_forma"].get(esq, [])
    return {
        "esqueleto": esq,
        "cenas": cenas,
        "formas_na_frota": q["formas"],
        "forma_inedita": iguais == 0,
        "exemplares_da_forma": iguais,
        "canais_da_forma": canais,
        "exemplares_do_tamanho": q["por_contagem_de_cena"].get(cenas, 0),
        # PECAS e FORMAS sao duas perguntas, e e a segunda que a copy escreve.
        "formas_do_tamanho": len(
            q["formas_por_contagem_de_cena"].get(cenas, [])),
        "formas_do_tamanho_lista": q["formas_por_contagem_de_cena"].get(
            cenas, []),
        "tamanho_inedito": q["por_contagem_de_cena"].get(cenas, 0) == 0,
        "contagens_existentes": sorted(q["por_contagem_de_cena"]),
        # O `exceto` VIAJA no resultado porque a frase das ordens livres
        # precisa dele: sem isso ela contaria a propria peca entre as tomadas,
        # que e o mesmo defeito que o `exceto` existe para corrigir.
        "exceto": exceto or "",
    }


# A convencao das PONTAS e MEDIDA e nao suposta: das 169 formas do disco, 156
# (92,3%) comecam em `titulo` e terminam em `cta`, e por PECA sao 385 de 416
# (92,5%). Ela NAO e universal — treze formas fogem dela —, logo entra como
# PARAMETRO declarado e o relato diz o que supos. Cravar a convencao sem a
# medida seria limiar sem procedencia (§10).
PONTAS_MEDIDAS = ("titulo", "cta")

# Acima disto o modulo NAO enumera: a contagem exata sai do multinomial e os
# exemplos saem de sorteio com semente fixa. Doze cenas ja dao 7.560
# ordenacoes e quarenta dariam um numero sem uso nenhum na tela.
MAX_ENUMERADAS = 5000


def _separador() -> str:
    """O separador da assinatura, PERGUNTADO ao dono em vez de cravado.

    `variedade.esqueleto` e o dono da assinatura do esqueleto. Em vez de
    repetir o literal dele aqui — o que faria o segundo dono —, pergunta-se a
    ele como ele une DUAS cenas conhecidas e tira-se o separador do meio. Se o
    dono trocar de separador, isto acompanha sem ninguem editar nada.
    """
    a, z = PONTAS_MEDIDAS
    s = V.esqueleto([{"layout": a}, {"layout": z}])
    assert s.startswith(a) and s.endswith(z), (
        "o dono da assinatura mudou de forma: %r nao e %r + separador + %r"
        % (s, a, z))
    return s[len(a):len(s) - len(z)]


def _mult(itens) -> tuple:
    return tuple(sorted(collections.Counter(itens).items()))


def _multinomial(itens) -> int:
    n = math.factorial(len(itens))
    for k in collections.Counter(itens).values():
        n //= math.factorial(k)
    return n


def formas_livres(cenas: int, layouts, pecas: list[dict] = None,
                  exceto: str = "", pontas: bool = True,
                  limite: int = 6, semente: int = 0) -> dict:
    """Quais ORDENS destes mesmos layouts a frota nunca usou.

    MEDIDO em 22/10 as 03:3x, escrevendo o `labtreinamento-s105`. O `novidade`
    respondia *"esta forma e nova?"* e nunca *"qual forma usar"* — e quando ele
    disse `forma_inedita: False` eu fui buscar as formas do tamanho numa
    SEGUNDA chamada e escolhi uma nova A MAO, no olho. E a mesma falta do
    `mira.orcamento` antes de 19/10 as 14:2x (*"esta na mira?"* sem *"quanto
    escrever para entrar?"*) e do `contagem_de_cenas` antes de 20/10 as 03:2x,
    que recusava sem ordenar.

    **E a colisao e recorrente, nao acidente:** a primeira forma que eu escrevi
    ja existia TAMBEM no `kolejny-poziom-s090` (21/10, 23:2x), e nas duas vezes
    quem pegou foi a segunda chamada. Duas em poucas rodadas e o item 3 da §10.

    **A contagem e EXATA e nao amostrada:** `possiveis` sai do multinomial do
    multiconjunto e `livres` subtrai as que a frota ja usou COM a mesma mistura
    (e, com `pontas`, com as mesmas extremidades). Os `exemplos` e que saem de
    sorteio com semente fixa, para o instrumento ser reproduzivel.

    **E LIVRES ZERO nao devolve lista vazia: ele RECUSA dizendo que o
    multiconjunto esta ESGOTADO**, do jeito que o `porta1` recusa janela curta.
    Medido no disco, SEIS multiconjuntos estao nesse estado — entre eles
    `titulo x3 + cta` e `titulo + item x4 + cta` —, e neles a novidade de FORMA
    e impossivel: ela tem de vir de trocar a MISTURA de layouts, nao a ordem.
    Devolver lista vazia faria a rodada seguinte procurar o que nao existe.
    """
    cenas = _CS.exige(cenas, "esqueleto_entre_canais.formas_livres")
    if isinstance(layouts, str):
        layouts = [x for x in layouts.split("-") if x]
    layouts = list(layouts or [])
    if len(layouts) != int(cenas):
        raise ValueError(
            "formas_livres: %d layout(s) para %r cenas — os dois argumentos "
            "descrevem a MESMA peca, e aceitar a divergencia seria responder "
            "bem formado sobre outra pergunta (a licao de 21/10 as 00:4x)"
            % (len(layouts), cenas))
    mult = _mult(layouts)
    pecas = varre() if pecas is None else pecas
    alvo = NS.arquivo(exceto) if exceto else ""
    usadas = {p["esqueleto"] for p in pecas
              if p.get("esqueleto") and p.get("cenas") == cenas
              and p.get("arquivo") != alvo}

    meio = list(layouts)
    if pontas:
        a, z = PONTAS_MEDIDAS
        if a not in meio or z not in meio:
            return {"cenas": cenas, "mult": mult, "pontas": pontas,
                    "possiveis": 0, "tomadas": 0, "livres": 0, "exemplos": [],
                    "esgotado": True,
                    "motivo": ("a convencao das pontas pede %r na frente e %r "
                               "no fim, e esta mistura nao tem os dois — chame "
                               "com `pontas=False` para contar sem ela"
                               % (a, z))}
        meio.remove(a)
        meio.remove(z)

    sep = _separador()

    def monta(perm):
        # O SEPARADOR e PERGUNTADO ao dono (`_separador`), nunca cravado aqui:
        # remontar a assinatura com um literal criaria o SEGUNDO dono da regra,
        # e o teste irmao de 20/10 as 01:3x reprova por AST exatamente isso —
        # foi ele que me pegou na primeira versao desta funcao.
        #
        # E a pergunta e feita UMA vez, nao por permutacao: chamar o dono
        # dentro do laco custou 47 s -> 228 s nos dois arquivos de teste
        # (medido), porque sao ate 5.000 permutacoes por chamada. Um dono e
        # uma pergunta, nao uma chamada por item.
        nomes = list(perm) if not pontas else (
            [PONTAS_MEDIDAS[0]] + list(perm) + [PONTAS_MEDIDAS[1]])
        return sep.join(nomes)

    possiveis = _multinomial(meio)
    tomadas = {e for e in usadas if _mult(e.split("-")) == mult
               and (not pontas or (e.split("-")[0] == PONTAS_MEDIDAS[0]
                                   and e.split("-")[-1] == PONTAS_MEDIDAS[1]))}
    livres = possiveis - len(tomadas)

    exemplos = []
    if livres > 0:
        if possiveis <= MAX_ENUMERADAS:
            import itertools
            todas = sorted({monta(p) for p in itertools.permutations(meio)})
            exemplos = [e for e in todas if e not in tomadas][:limite]
        else:
            r = random.Random(semente)
            tentativas = 0
            vistos = set()
            while len(exemplos) < limite and tentativas < 20000:
                tentativas += 1
                p = list(meio)
                r.shuffle(p)
                e = monta(p)
                if e in tomadas or e in vistos:
                    continue
                vistos.add(e)
                exemplos.append(e)
    motivo = ""
    if livres == 0:
        motivo = (
            "multiconjunto ESGOTADO: a frota ja usou as %d ordenacao(oes) que "
            "existem para esta mistura de layouts. A novidade de FORMA e "
            "impossivel aqui, e ela tem de vir de trocar a MISTURA, nao a "
            "ordem." % possiveis)
    return {"cenas": cenas, "mult": mult, "pontas": pontas,
            "possiveis": possiveis, "tomadas": len(tomadas), "livres": livres,
            "exemplos": exemplos, "esgotado": livres == 0, "motivo": motivo}


def _linha_das_livres(cenas: int, esq: str, pecas=None, exceto: str = "") -> str:
    """UM dono da frase. Ela sai nos DOIS ramos da novidade: com a forma nova
    ela diz quanto AINDA resta, e com a forma repetida ela diz o que usar."""
    try:
        f = formas_livres(cenas, esq, pecas=pecas, exceto=exceto)
    except ValueError as e:
        return "  ORDENS LIVRES: %s" % e
    if f["esgotado"]:
        return "  >> ORDENS LIVRES: NENHUMA — %s" % f["motivo"]
    linha = ("  ORDENS LIVRES destes mesmos layouts: %d de %d possiveis "
             "(%d usada(s) pela frota)" % (f["livres"], f["possiveis"],
                                           f["tomadas"]))
    if f["exemplos"]:
        linha += "\n  exemplos: " + ", ".join(f["exemplos"][:3])
    linha += ("\n  supondo %r na frente e %r no fim, que e a convencao MEDIDA "
              "em 92,3%% das formas do disco e NAO e universal."
              % PONTAS_MEDIDAS)
    return linha


def _frase_da_novidade(n: dict) -> str:
    if n["forma_inedita"]:
        p = (f"esqueleto INEDITO nas {n['formas_na_frota']} formas de short "
             f"da frota")
    else:
        p = (f"esqueleto JA EXISTE: {n['exemplares_da_forma']} exemplar(es), "
             f"em {len(n['canais_da_forma'])} canal(is) "
             f"({', '.join(n['canais_da_forma'])})")
    if n["tamanho_inedito"]:
        t = (f"e o TAMANHO de {n['cenas']} cenas e inedito — as contagens "
             f"existentes sao {n['contagens_existentes']}")
    else:
        t = (f"e o tamanho de {n['cenas']} cenas tem "
             f"{n['exemplares_do_tamanho']} PECA(S) em "
             f"{n['formas_do_tamanho']} FORMA(S) distinta(s) — e e a segunda"
             " que a copy escreve")
    livres = _linha_das_livres(n["cenas"], n["esqueleto"],
                               exceto=n.get("exceto") or "")
    return f"  {p},\n  {t}.\n{livres}"


def formas_usadas_do_tamanho(cenas: int, pecas: list[dict] = None,
                             exceto: str = "") -> dict:
    """As formas que a frota JA USOU num tamanho de cena, com os ARQUIVOS.

    **Medido em 22/10 as 16:3x, escrevendo o `epomeno-epipedo-s095`.** O
    `novidade` devolve um VEREDITO sobre uma forma e uma CONTAGEM do tamanho
    (`formas_do_tamanho`), e o `formas_livres` devolve ordens que ninguem usou
    — e nenhum dos dois devolve a LISTA das usadas. Logo, para escolher
    esqueleto, eu venho escrevendo um laco sobre `varre()` na linha de comando,
    a cada rodada em que a primeira forma colide. Terceira vez nesta sessao, e
    e o item 3 da §10.

    **E a falta JA PRODUZIU um defeito medido, com custo:** em 21/10 as 23:2x
    eu precisei exatamente desta lista, escrevi o laco e cortei a saida com
    `tail -10` sobre um tamanho que tinha DEZ formas — li as sete ultimas como
    se fossem o conjunto e escolhi um esqueleto que JA EXISTIA. E a familia da
    fatia do proxy (19/10 as 19:2x) e da fatia dos capitulos livres (22/10 as
    10:3x): ler uma ponta de lista como se fosse a lista.

    **O tamanho do risco vai MEDIDO, e a fatia nao e caso de borda:** dos
    **13** tamanhos de cena que a frota usa, **DEZ tem oito formas ou mais**,
    isto e, um `tail -10` corta a lista em dez de treze. E o pior deles e o
    mais usado: **dez cenas tem 65 formas em 149 pecas**, onde a fatia
    descarta 55 de 65.

    Por isso a CONTAGEM vem primeiro na frase e a lista sai INTEIRA, que e a
    disciplina do `segundo_angulo.relato_dos_livres` — com a contagem na
    frente, um corte na leitura fica visivel em vez de silencioso.

    A varredura e DELEGADA ao `varre` e o filtro da propria peca ao `sem`, que
    e o dono das duas convencoes de nome. **Tamanho que a frota nunca usou
    devolve lista VAZIA e nao levanta**, porque ali o vazio e o valor CERTO e
    e justamente a resposta que a rodada quer — e o campo `usado` o diz em
    letra, para nao se confundir com varredura que falhou (17/10).
    """
    cenas = _CS.exige(cenas, "esqueleto_entre_canais.formas_usadas_do_tamanho")
    pecas = sem(varre() if pecas is None else pecas, exceto)
    por, canais = {}, {}
    for x in pecas:
        if x.get("cenas") != cenas or not x.get("esqueleto"):
            continue
        por.setdefault(x["esqueleto"], []).append(x["arquivo"])
        canais.setdefault(x["esqueleto"], set()).add(x.get("canal"))
    formas = [{"esqueleto": e, "arquivos": sorted(a), "n": len(a),
               "canais": sorted(c for c in canais[e] if c)}
              for e, a in por.items()]
    formas.sort(key=lambda f: (-f["n"], f["esqueleto"]))
    return {
        "cenas": cenas,
        "usado": bool(formas),
        "n_formas": len(formas),
        "n_pecas": sum(f["n"] for f in formas),
        "formas": formas,
        "canais": sorted({c for f in formas for c in f["canais"]}),
    }


def _linha_das_formas_usadas(cenas: int, pecas=None, exceto: str = "") -> str:
    """UM dono da frase, e ela sai nos DOIS ramos: com o tamanho usado ela
    lista tudo, e com o tamanho inedito ela DIZ isso em vez de calar."""
    u = formas_usadas_do_tamanho(cenas, pecas=pecas, exceto=exceto)
    if not u["usado"]:
        return ("  FORMAS USADAS em %d cenas: NENHUMA — a frota nunca usou "
                "este tamanho, logo toda ordem e nova." % cenas)
    L = ["  FORMAS USADAS em %d cenas: %d forma(s) em %d peca(s) — a contagem "
         "vem PRIMEIRO de proposito, para um corte na leitura ficar visivel "
         "(21/10 as 23:2x, quando um `tail -10` sobre dez formas me fez "
         "escolher uma que ja existia). A lista sai INTEIRA:"
         % (cenas, u["n_formas"], u["n_pecas"])]
    for f in u["formas"]:
        L.append("   %2dx  %s" % (f["n"], f["esqueleto"]))
    return "\n".join(L)


def misturas_do_tamanho(cenas: int, pecas: list[dict] = None,
                        exceto: str = "", pontas: bool = True) -> dict:
    """Quais MISTURAS de layout a frota usa num tamanho, e quanta ordem sobra.

    **Medido em 22/10 as 19:3x, escrevendo o `epomeno-epipedo-s096`.** O
    `formas_livres` responde *"quantas ordens DESTES layouts sobram"* — e
    **recebe a mistura como argumento**. Logo a pergunta anterior, *"qual
    mistura escolher"*, continuava sem dono: eu listava as formas usadas do
    tamanho (`formas_usadas_do_tamanho`, de 22/10 as 16:3x) e compunha uma
    mistura **no olho**, contando layouts com os dedos.

    **E o passo no olho ja errou DUAS vezes, com custo medido:** em 21/10 as
    23:2x e em 22/10 as 14:4x a primeira forma que eu compus **JA EXISTIA**, e
    nas duas quem pegou foi uma segunda chamada ao `novidade`. **Nesta rodada
    ele acertou por sorte** — a forma saiu inedita —, e isso vai dito em vez de
    inflado: aqui o defeito era LATENTE.

    **O TAMANHO VAI MEDIDO:** a frota usa **54** misturas distintas em treze
    tamanhos de cena, e **NOVE delas estao ESGOTADAS** (toda ordem com aquelas
    pontas ja foi usada). Nelas a novidade de FORMA e impossivel e tem de vir
    de trocar a MISTURA — que e exatamente a pergunta que nao tinha dono.

    **E a escolha no olho NAO converge com a medida.** Em treze cenas a frota
    usa quatro misturas, com **41.579 / 13.859 / 13.848 / 3.959** ordens
    livres; a que eu escolhi a mao nesta rodada foi a de **13.848**, isto e a
    terceira. Acertar *"inedita"* nao e o mesmo que escolher onde ha espaco.

    **A contagem e DELEGADA ao `formas_livres`** — recontar o multinomial aqui
    criaria o segundo dono da conta, a assinatura que congelou a legenda —, e a
    varredura ao `varre` com o filtro do `sem`.

    **E tamanho que a frota nunca usou RECUSA em vez de inventar mistura**, do
    jeito que o `porta1` recusa janela curta: sem peca naquele tamanho nao ha
    de onde DERIVAR a mistura, e escolher uma seria limiar sem procedencia
    (§10). O campo `usado` o diz em letra.
    """
    cenas = _CS.exige(cenas, "esqueleto_entre_canais.misturas_do_tamanho")
    pecas = sem(varre() if pecas is None else pecas, exceto)
    u = formas_usadas_do_tamanho(cenas, pecas=pecas)
    vistas, ordem = {}, []
    for f in u["formas"]:
        lay = [x for x in f["esqueleto"].split(_separador()) if x]
        chave = _mult(lay)
        if chave not in vistas:
            vistas[chave] = {"mult": chave, "layouts": lay,
                             "n_pecas": 0, "formas": 0}
            ordem.append(chave)
        vistas[chave]["n_pecas"] += f["n"]
        vistas[chave]["formas"] += 1
    saida = []
    for chave in ordem:
        m = vistas[chave]
        # A CONTA E DO `formas_livres`, dono dela desde 22/10 as 03:3x.
        r = formas_livres(cenas, m["layouts"], pecas=pecas,
                          pontas=pontas)
        m = dict(m)
        m["possiveis"] = r.get("possiveis", 0)
        m["livres"] = r.get("livres", 0)
        m["esgotado"] = bool(r.get("esgotado")) or not r.get("livres")
        m["motivo"] = r.get("motivo")
        saida.append(m)
    saida.sort(key=lambda m: (-m["livres"], -m["n_pecas"], m["mult"]))
    esg = [m for m in saida if m["esgotado"]]
    return {
        "cenas": cenas,
        "usado": bool(saida),
        "n_misturas": len(saida),
        "misturas": saida,
        "n_esgotadas": len(esg),
        "esgotadas": esg,
        "motivo": None if saida else (
            "a frota nunca usou %d cenas, logo nao existe mistura de onde "
            "DERIVAR a resposta — inventar uma seria limiar sem procedencia "
            "(§10). Escolha a mistura a partir de um tamanho vizinho e conte "
            "com o `formas_livres`." % cenas),
    }


def sugere_forma(cenas: int, pecas: list[dict] = None, exceto: str = "",
                 pontas: bool = True, semente: int = 0) -> dict:
    """Uma forma LIVRE no tamanho pedido, da mistura onde mais ordem sobra.

    Fecha o passo que faltava: o `formas_livres` conta ordens de uma mistura
    DADA, e esta escolhe a mistura — a maior de `livres` — e devolve um exemplo
    que a frota nao usou. **Os exemplos sao do `formas_livres`** (sorteio com
    semente fixa, para ser reproduzivel); aqui nao se monta assinatura nenhuma,
    porque o dono dela e o `variedade.esqueleto`.

    **E as ESGOTADAS saem NOMEADAS e nao filtradas**, pela disciplina do
    `origens_sem_uso`: esconde-las faria a rodada seguinte perguntar por que a
    lista encurtou, quando a resposta e que naquela mistura a novidade de forma
    e impossivel.
    """
    q = misturas_do_tamanho(cenas, pecas=pecas, exceto=exceto, pontas=pontas)
    vivas = [m for m in q["misturas"] if not m["esgotado"]]
    if not vivas:
        q["sugerida"] = None
        q["mistura"] = None
        q["motivo"] = q.get("motivo") or (
            "as %d mistura(s) que a frota usa em %d cenas estao TODAS "
            "ESGOTADAS: a novidade de forma ali e impossivel e tem de vir de "
            "trocar a MISTURA de layouts, nao a ordem."
            % (q["n_misturas"], cenas))
        return q
    m = vivas[0]
    r = formas_livres(cenas, m["layouts"], pecas=sem(
        varre() if pecas is None else pecas, exceto),
        pontas=pontas, semente=semente)
    ex = list(r.get("exemplos") or [])
    q["mistura"] = m
    q["sugerida"] = ex[0] if ex else None
    q["alternativas"] = ex[1:]
    return q


def _linha_das_misturas(cenas: int, pecas=None, exceto: str = "") -> str:
    """UM dono da frase, e ela sai nos DOIS ramos — tamanho usado e inedito."""
    s = sugere_forma(cenas, pecas=pecas, exceto=exceto)
    if not s["usado"]:
        return ("  MISTURA em %d cenas: a frota nunca usou este tamanho, logo "
                "nao ha de onde DERIVAR a mistura — %s" % (cenas, s["motivo"]))
    L = ["  MISTURA em %d cenas: %d que a frota usa, %d ESGOTADA(S) — a "
         "escolha da mistura deixou de ser no olho (22/10 as 19:3x, depois de "
         "a forma composta a mao JA EXISTIR duas vezes)."
         % (cenas, s["n_misturas"], s["n_esgotadas"])]
    for m in s["misturas"]:
        rot = " ESGOTADA" if m["esgotado"] else ""
        L.append("   %6d livres de %6d  %s%s"
                 % (m["livres"], m["possiveis"],
                    " + ".join("%s x%d" % (k, v) for k, v in m["mult"]), rot))
    if s.get("sugerida"):
        L.append("   >> onde mais sobra ordem: %s"
                 % " + ".join("%s x%d" % (k, v) for k, v in
                              s["mistura"]["mult"]))
        L.append("   >> forma LIVRE sugerida: %s" % s["sugerida"])
    else:
        L.append("   >> %s" % s["motivo"])
    return "\n".join(L)


def relato(caminho=None, spec=None) -> str:
    """A MESMA convencao dos outros relatos: `(caminho, spec=None)`.

    Ela nascera como `relato(spec_ou_caminho)` — UM parametro cujo NOME dizia
    que aceitava os dois. **E o despachante do `antes_do_render` decide pela
    ARIDADE, nao pelo nome** (a licao de 20/10 as 11:3x, e por isso que o
    `paleta_da_spec` foi normalizado em 21/10 as 20:3x). Logo a passada de
    pre-render declarava *"NAO aceita rascunho"* sobre um modulo que ACEITAVA,
    e isso e silencio permissivo: ela dizia que nao conferiu podendo conferir.

    **Custou uma escolha, em 21/10 as 23:2x:** sem a resposta na passada eu fui
    conferir a novidade do esqueleto a mao, li uma listagem que o meu proprio
    `tail -10` havia CORTADO (as 7 ultimas de 10 formas de treze cenas) e
    escolhi uma forma que JA EXISTIA no `epomeno-epipedo`. E a familia da fatia
    do proxy de 19/10 as 19:2x, agora com o `tail`.
    """
    if isinstance(caminho, dict):     # compatibilidade: a spec na 1a posicao
        caminho, spec = None, caminho
    # A PECA PERGUNTADA SAI DA POPULACAO UMA VEZ, aqui, e as QUATRO contas do
    # relato leem a MESMA lista. Ate 22/10 as 11:4x so a frase da novidade era
    # filtrada, e o MESMO relato imprimia "acervo: 424 pecas, 177 formas" com
    # "INEDITO nas 176 formas da frota" duas linhas abaixo. Ver o `sem`.
    #
    # E o `exceto` sai do NOME do arquivo mesmo no rascunho: a peca pode nao
    # estar no disco agora e estar na proxima chamada, e sem ele "inedita"
    # nunca poderia ser verdade (01:3x de 20/10). SEM CAMINHO ele caia para
    # vazio e a peca se contava a si mesma (22/10 as 03:4x) — o nome sai do
    # `pacote` da propria spec, pelo dono unico do `nome_da_spec`.
    d = None
    if caminho is not None or spec is not None:
        d = spec if spec is not None else json.load(
            open(caminho, encoding="utf-8"))
    short = (d.get("short") or []) if d else []
    exceto = ""
    if short:
        exceto = (os.path.basename(caminho) if caminho
                  else NS.arquivo(d.get("pacote") or ""))
    pecas = sem(varre(), exceto)
    q = quadro(pecas)
    qv = quadro(pecas, so_vivos=True)
    L = ["ESQUELETO ENTRE CANAIS — o que o portao `variedade` nao ve"]
    for rot, x in (("acervo", q), ("canais VIVOS", qv)):
        L.append(
            f"  {rot}: {x['pecas']} pecas, {x['formas']} formas; "
            f"{x['formas_que_atravessam']} atravessam canal e levam "
            f"{x['pecas_em_forma_que_atravessa']} pecas "
            f"({100 * x['fracao_atravessada']:.0f}%)"
        )
    topo = sorted(q["contagem_da_forma"].items(),
                  key=lambda kv: -kv[1])[:3]
    for e, n in topo:
        c = q["canais_da_forma"][e]
        L.append(f"   {n:3d}x em {len(c):2d} canal(is)  {e}")
    if short:
        L.append("")
        L.append(f"desta peca ({d.get('pacote', '?')}):")
        L.append(_frase_da_novidade(
            novidade(V.esqueleto(short), len(short), pecas, exceto)))
        L.append(_linha_das_formas_usadas(len(short), pecas, exceto))
        L.append(_linha_das_misturas(len(short), pecas, exceto))
    c = cegas_para_o_portao(pecas)
    L.append("")
    L.append(
        f"  das {c['atravessam']} formas que atravessam canal, "
        f"{len(c['cegas'])} sao INVISIVEIS ao portao (ele avisa a partir de "
        f"{c['limiar_do_portao']} iguais DENTRO de um canal) e levam "
        f"{c['pecas_cegas']} pecas"
    )
    L.append("")
    L.append("  o portao `variedade` compara contra o MESMO canal (o")
    L.append("  `_especs_do_canal` filtra pelo slug), logo forma que")
    L.append("  atravessa canal e invisivel para ele. Isto NOMEIA e NAO")
    L.append("  reprova: portao aqui reprovaria o acervo inteiro.")
    return "\n".join(L)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    print(relato(arg))
    sys.exit(0)   # SEMPRE zero: isto informa, nao reprova.
