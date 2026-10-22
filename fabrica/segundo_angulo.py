#!/usr/bin/env python3
"""Capitulos AINDA NAO USADOS de um longo que ja rendeu short. Tudo local.

POR QUE ISTO EXISTE (12/10/2026, e nasce do passo que eu fiz A MAO na rodada das
11:07). O achado da rodada anterior foi que **a unidade de pauta e (longo,
familia de capitulo), nao o longo**: 48 das 49 origens tinham sido usadas UMA vez
e eu tratava cada longo como uso unico por habito.

Para escrever o primeiro segundo angulo eu precisei de tres passos, e dois deles
eram frageis:

  1. listar origens usadas uma vez — `pauta_viva.por_uso` ja faz, mas ele roda no
     RUNNER porque le a playlist de uploads;
  2. **achar qual spec LOCAL carrega os capitulos daquele longo** — eu descobri
     lendo a PROSA do AVISO do short ("...do longo labtreinamento-010
     (6BeNHqT2okA)"). Isso e adivinhacao de texto, e quebra na primeira spec que
     escrever o aviso de outro jeito;
  3. ver quais capitulos o short existente ja consumiu.

**E A MINHA PRIMEIRA TENTATIVA DE CONSERTO ESTAVA ERRADA, medido no ato:** eu
escrevi este modulo resolvendo `youtube_id -> pacote` pelo retrato
`fabrica/ponte/videos.json`, e fui testar no caso real. O retrato **nao tem** o
`6BeNHqT2okA` nem o pacote `labtreinamento-010` — nenhum dos dois, em nenhuma
linha. O longo e anterior ao retrato ou nunca foi registrado nele. Logo **nao
existe mapeamento estruturado local de id de origem para spec de pacote**: o par
existe so na PROSA que eu mesmo escrevi no aviso do short.

**O que o modulo faz no lugar:** procura, dentro da copy do short, o nome de uma
spec que EXISTE em `fabrica/specs/`. Isso nao e adivinhacao de prosa — e casar
contra um vocabulario FECHADO, o conjunto dos nomes de spec do repositorio, e
qualquer acerto e verificavel abrindo o arquivo.

**A limitacao que fica declarada:** isso depende da convencao de o aviso do short
nomear o pacote de origem. E convencao, nao garantia. Quando falha, o modulo diz
que falhou e manda usar o `capitulos.yml` com `legenda=true`, que nao depende de
convencao nenhuma.

**E ELE DEU FALSO POSITIVO NA PRIMEIRA VEZ QUE EU O USEI PARA ESCOLHER — medido
as 12:1x de 12/10, uma rodada depois de eu o escrever.** Tres origens do kolejny
(`MjI4ZGJAhIo`, `SP7Vz8qHdRY`, `Xgt32iH8Ft8`) resolveram para a spec
`kolejny-poziom`, que e o SLUG DO CANAL e tem dez cenas de longo. E verdade
conhecida que isso esta errado em pelo menos um caso: o docstring do
`kolejny-poziom-s017` diz, escrito por mim em 11/10, que o `Xgt32iH8Ft8` e do
pacote `kp-plan-9233-20260811` e que **nao tem spec em `fabrica/specs/`**. A
resposta certa ali e None, e o modulo devolvia um pacote.

Duas causas, e as duas tem conserto:
  1. **o nome casava sem FRONTEIRA**, entao `kolejny-poziom` casava dentro de
     `kolejny-poziom-s017`. Agora a busca exige que o nome nao seja seguido nem
     precedido de `-` ou de caractere de palavra;
  2. **o slug do canal nao e nome de pacote.** A spec homonima do canal e
     generica ou legada, e por isso ela sai da lista de candidatos.

**E o que sobra de duvida sai MARCADO, nao escondido:** pacote resolvido com
menos de VINTE cenas de longo vira `suspeito=True`, porque os longos de verdade
da frota medem **56 a 90 capitulos** e os unicos casos de dez eram esse falso
positivo. O limiar e observado, nao inventado, e a procedencia esta nesta linha.

**O QUE ELE NAO FAZ, e nao e timidez:** ele nao escolhe capitulo e nao nomeia familia —
familia. Capitulo e conteudo que vai ao ar, e a familia de entrada errada e
julgamento — a regra (e) pede ARITMETICA, a (f) pede familia nao repetida no dia,
e o `similaridade` tem a palavra final. O modulo entrega a lista; a escolha e de
quem escreve.

**E ele nao garante que o capitulo esta livre.** Ele marca os que a copy do short
existente MENCIONA pelo kicker, o que e indicio e nao prova: um short pode usar o
conteudo de um capitulo sem citar o kicker dele. Por isso a saida separa
"mencionado" de "nao mencionado" em vez de dizer "usado" e "livre".
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(RAIZ, "fabrica", "specs")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nome_da_spec   # noqa: E402  — UM dono do nome da spec (as duas convencoes)


# Cenas de longo abaixo disto: nao e longo, e a resolucao vai MARCADA.
# OBSERVADO na frota — os longos de verdade medem 56 a 90 capitulos, e os unicos
# casos de dez eram o falso positivo do slug do canal (12/10 12:1x).
MIN_CAPITULOS_PLAUSIVEL = 20



def _dir_valido(dir_specs: str) -> str:
    """O UM dono da conferencia do diretorio — e ele LEVANTA em vez de calar.

    MEDIDO em 20/10 as 12:3x, escrevendo o `epomeno-epipedo-s075`. Eu chamei
    `nao_mencionados('9Hg5A3H1Qe4', 'epomeno-epipedo')` passando o CANAL na
    posicao do `dir_specs`, e a funcao devolveu uma resposta bem formada e
    VAZIA:

        {'pacote': None, 'n_capitulos': 0, 'shorts': [], 'nao_mencionados': []}

    As cinco funcoes deste modulo varrem com
    `glob.glob(os.path.join(dir_specs, '*.json'))`, e `glob` de caminho que nao
    existe devolve `[]` sem levantar nada.

    **E o que torna isto pior que o 000 do `curl`: o vazio aqui e CAMUFLADO por
    um estado LEGITIMO que o proprio modulo reporta.** `pacote: None` significa,
    pelo docstring do `pacote_do_id`, *"a convencao nao foi seguida"* — isto e,
    origem sem spec local, que e a regra (h) e acontece de verdade. Logo
    "diretorio errado" e "origem sem spec" sao INDISTINGUIVEIS pela saida, e eu
    passei varias chamadas atras do motivo de o `pauta_do_momento` ver 63
    capitulos onde eu via zero.

    E a familia e a de sempre, agora com o SEXTO membro: instrumento que
    devolve VAZIO nao prova ausencia (17/10, o grep dos inscritos); arquivo
    vazio nao prova morte (19/10, o `.norm` a meio de escrever); instrumento
    CHEIO nao prova presenca (20/10 as 01:4x, o `pgrep` se vendo); 000 nao diz
    de QUEM e o zero (09:3x); 000 em todo host nao separa rede de POLITICA
    (11:4x); e aqui, vazio CAMUFLADO por um estado legitimo do proprio
    instrumento. O conserto e o do `porta1` — recusar com o motivo em vez de
    responder zero.
    """
    if not os.path.isdir(dir_specs):
        raise ValueError(
            "dir_specs nao e um diretorio: %r. Varredura em caminho inexistente "
            "devolveria resposta VAZIA e bem formada, indistinguivel de origem "
            "sem spec local (regra h) — medido em 20/10 as 12:3x." % (dir_specs,))
    return dir_specs


def slugs_de_canal(dir_specs: str = SPECS) -> set:
    """Os `slug` que as specs declaram. Slug de canal NAO e nome de pacote."""
    _dir_valido(dir_specs)
    fora = set()
    for p in glob.glob(os.path.join(dir_specs, "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("slug"):
            fora.add(str(sp["slug"]))
    return fora


def nomes_de_spec(dir_specs: str = SPECS) -> list:
    """O vocabulario FECHADO: os nomes de spec que existem no repositorio.

    SEM os nomes que sao slug de canal: a spec homonima do canal e generica ou
    legada, e foi ela que produziu o falso positivo de 12/10 em tres origens.
    Ordenado do mais longo para o mais curto, para que `labtreinamento-010` case
    antes de um hipotetico `labtreinamento-01`.
    """
    slugs = slugs_de_canal(dir_specs)
    nomes = [os.path.basename(p)[:-5]
             for p in glob.glob(os.path.join(dir_specs, "*.json"))]
    return sorted((n for n in nomes if n not in slugs), key=len, reverse=True)


def _casa_inteiro(nome: str, texto: str) -> bool:
    """O nome aparece como identificador INTEIRO, nao como prefixo de outro.

    Sem isto `kolejny-poziom` casa dentro de `kolejny-poziom-s017`.
    """
    return re.search(r"(?<![\w-])" + re.escape(nome) + r"(?![\w-])",
                     texto, re.IGNORECASE) is not None


def pacote_do_id(yid: str, dir_specs: str = SPECS) -> str | None:
    """`youtube_id` -> spec de pacote que carrega os capitulos daquele longo.

    Resolvido pela copy do SHORT que declara esta origem: procura nela o nome de
    uma spec que EXISTE, e exige que essa spec tenha cenas de longo. Casar contra
    vocabulario fechado, e nao contra um padrao de texto.

    Devolve None quando a convencao nao foi seguida — e aí a rota e o
    `capitulos.yml` com `legenda=true`, que nao depende de convencao.
    """
    vocab = nomes_de_spec(dir_specs)
    for nome, copy in shorts_da_origem(yid, dir_specs):
        for cand in vocab:
            if cand == nome or not _casa_inteiro(cand, copy):
                continue
            if capitulos_do_pacote(cand, dir_specs):
                return cand
    return None


def _cenas_do_longo(pacote: str, dir_specs: str = SPECS) -> list:
    """As cenas do LONGO daquele pacote, como estao no disco. UM dono da leitura.

    Ele existe porque o `capitulos_do_pacote` devolve KICKER e o
    `texto_dos_livres` precisa da NARRACAO da mesma cena: duas leituras do mesmo
    arquivo seriam dois donos da forma da spec, que e a assinatura que congelou a
    legenda.
    """
    p = os.path.join(dir_specs, f"{pacote}.json")
    if not os.path.exists(p):
        return []
    try:
        sp = json.load(open(p, encoding="utf-8"))
    except Exception:                                       # noqa: BLE001
        return []
    return [c for c in (sp.get("longo") or []) if isinstance(c, dict)]


def capitulos_do_pacote(pacote: str, dir_specs: str = SPECS) -> list:
    """Os kickers das cenas do LONGO daquele pacote. Lista vazia se nao houver."""
    return [(c.get("kicker") or "").strip()
            for c in _cenas_do_longo(pacote, dir_specs)]


def shorts_da_origem(yid: str, dir_specs: str = SPECS, exceto: str = None) -> list:
    """As specs de short que declaram `longo_existente == yid`.

    `exceto` tira UMA spec da varredura — a peca da PROPRIA rodada, que ja esta
    no disco quando eu pergunto. **Medido em 20/10 as 14:3x:** sem ele, escrever
    a spec antes de consultar derruba a RESERVA da origem dela (de 76 para 71
    capitulos nesta rodada), e a reserva e o DESEMPATE da pauta — logo a origem
    pode perder um empate que deveria ganhar. O nome e normalizado pelo
    `nome_da_spec`, porque as cinco funcoes que aceitam `exceto` se dividiam em
    duas convencoes (11:3x).
    """
    fora = []
    for p in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        nome = os.path.basename(p)
        if exceto and nome_da_spec.casa(nome, exceto):
            continue
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("longo_existente") == yid:
            fora.append((nome[:-5], sp.get("copy") or ""))
    return fora


def _sem_reserva(copy: str) -> str:
    """A copy do irmao SEM os blocos de reserva que ele deixou escritos.

    **O DEFEITO, medido em 20/10 as 12:4x, escolhendo a pauta desta rodada.** O
    `labtreinamento-s016` deixou uma reserva nomeando quatro capitulos do
    `labtreinamento-010` para a rodada seguinte achar — e o `nao_mencionados`
    devolvia TRES deles como MENCIONADOS. Quem os mencionou foi o proprio bloco
    de reserva: a comparacao varria a copy INTEIRA, e o bloco existe justamente
    para dizer que aqueles capitulos NAO foram usados.

    **A promessa virava uso, e a direcao e perversa:** quanto melhor a rodada
    anterior documentou o que deixou, mais invisivel o capitulo fica como livre.
    Medido no disco: **2 das 49** origens com short e 20+ capitulos tem capitulo
    assim, **QUATRO** capitulos em total — pequeno, e e o lado da pauta que a
    reserva nasceu para abrir.

    **A remissao era CIRCULAR:** o `reservas_escritas` diz, desde que nasceu,
    que quem decide se a reserva segue livre e esta funcao — e esta funcao era
    cegada pela propria reserva.

    **E a secao `## FONTES` FICA**, de proposito: ali o irmao nomeia os
    capitulos que ele de fato usou, e aquilo e mencao legitima. So o bloco de
    negacao sai.

    A extracao e DELEGADA ao dono (`reservas_escritas.blocos_de_reserva`), e o
    import e TARDIO porque o grafo tem ciclo: o `irmaos_da_origem` importa este
    modulo e o `reservas_escritas` importa aquele. Reimplementar a leitura aqui
    criaria o segundo dono do bloco, que e a assinatura que congelou a legenda.
    """
    if not copy:
        return ""
    import reservas_escritas as RE   # tardio: ciclo IO -> SA, RE -> IO
    for bloco in RE.blocos_de_reserva(copy):
        copy = copy.replace(bloco, " ")
    return copy


def nao_mencionados(yid: str, dir_specs: str = SPECS,
                    exceto: str = None) -> dict:
    """Capitulos cujo kicker NAO aparece na copy de nenhum short desta origem.

    "Nao mencionado" e INDICIO de capitulo livre, nao prova: um short pode usar o
    conteudo sem citar o kicker. A saida devolve as duas listas para que quem
    escreve decida olhando, em vez de confiar num rotulo.

    **`exceto` MEDIDO em 20/10 as 14:3x, e e a metade que faltava do conserto de
    08:2x.** Naquela rodada o `pauta_do_momento` ganhou `exceto` e o passou ao
    dono da CONTAGEM (`concentracao.contagem`) — e nunca aqui. Como o desempate
    da pauta e a RESERVA, que sai desta funcao, escrever a spec da rodada antes
    de consultar derrubava a reserva da origem dela e **trocava a escolha**: com
    a `kolejny-poziom-s076` no disco a reserva do `-5aMrDsxlZE` caiu de 76 para
    71 e a escolha virou para o `42hpD7eaptE` (73), mesmo COM o `exceto` ligado.
    Conserto aplicado a UM de dois donos nao e conserto.

    **PONTO CEGO DECLARADO, e ele NAO foi consertado:** a comparacao e por TEXTO
    do kicker, logo kicker REPETIDO no mesmo longo e uma entrada so — capitulo
    cujo GEMEO foi citado desaparece da lista de livres. Medido no disco:
    **71 das 134** specs de longo com 20+ cenas tem kicker repetido, cobrindo
    **585** cenas. Consertar isso trocaria a base da comparacao (texto por
    indice) em todas as leituras historicas, e isso e desenho e nao conserto de
    rodada.
    """
    _dir_valido(dir_specs)
    pacote = pacote_do_id(yid, dir_specs)
    caps = capitulos_do_pacote(pacote, dir_specs) if pacote else []
    usados = shorts_da_origem(yid, dir_specs, exceto)
    copys = " ".join(c for _, c in usados).lower()
    limpos = " ".join(_sem_reserva(c) for _, c in usados).lower()
    men, nao, so_na_reserva = [], [], []
    for k in caps:
        if not k:
            continue
        kl = k.lower()
        if kl in limpos:
            men.append(k)
        else:
            nao.append(k)
            if kl in copys:
                so_na_reserva.append(k)
    return {"pacote": pacote, "n_capitulos": len(caps),
            "suspeito": bool(pacote) and 0 < len(caps) < MIN_CAPITULOS_PLAUSIVEL,
            "shorts": [n for n, _ in usados],
            "mencionados": men, "nao_mencionados": nao,
            "mencionados_so_na_reserva": so_na_reserva}


def declarados_pelos_irmaos(yid: str, dir_specs: str = SPECS,
                            exceto: str = None) -> dict:
    """Capitulos que a copy de um IRMAO declara ter usado, por INDICE da cena.

    **MEDIDO em 22/10 as 12:3x, escrevendo o `kolejny-poziom-s093`, e custou
    duas cenas daquela peca.** O `nao_mencionados` casa o TEXTO do kicker contra
    a copy do irmao — e a copy declara FAIXA em digitos (*"Capitulos 66 a 74 do
    longo"*). Logo capitulo DECLARADO continua saindo como livre, e a lista de
    livres o oferece como pauta.

    Na origem daquela rodada (`-5aMrDsxlZE`) eram **15 capitulos** declarados
    dentro dos 70 livres, e um deles era o 74: o `kolejny-poziom-s076` declara
    66 a 74 **e a narracao dele diz, em letra, "Sprawdz ponownie po trzech
    miesiacach"** — a mesma frase que a minha cena 11. **Nenhum portao pegaria
    isso:** o `similaridade` compara TITULO, nao cena.

    Eram DOIS donos do mesmo fato, e eles discordavam: a faixa e lida pelo
    `irmaos_da_origem._capitulos_declarados`, e e DELE que esta funcao a pede.
    **O import e tardio de proposito** — o `irmaos_da_origem` importa este modulo
    no topo, logo importa-lo aqui no topo seria circular. Delegar continua sendo
    um dono so.

    **Ele NOMEIA e NAO FILTRA**, pela disciplina do `origens_sem_uso`: o
    `nao_mencionados` segue devolvendo a mesma lista de `nao_mencionados` que
    sempre devolveu, e esta funcao diz quais daqueles indices um irmao declara.
    Tirar o capitulo da lista escondia o conflito em vez de o mostrar, e mudava
    a base de comparacao de toda leitura historica.

    **O que ele NAO prova, nos dois sentidos:** declaracao em prosa nao e
    verdade sobre a peca (a faixa `66 a 74` pode cobrir capitulo que o irmao nao
    tocou), e ausencia de declaracao nao e ausencia de uso — **146 das specs de
    short solto do disco nao declaram capitulo nenhum** (medida do
    `cobertura_dos_capitulos`). Ele devolve MOTIVO PARA LER a peca do irmao,
    nunca veredito: capitulo livre nao e familia livre (776).
    """
    import irmaos_da_origem as IO   # tardio: IO importa este modulo no topo
    d = nao_mencionados(yid, dir_specs, exceto)
    if not d["pacote"]:
        return {"pacote": None, "por_indice": {}, "n": 0}
    livres = set(d["nao_mencionados"])
    cenas = _cenas_do_longo(d["pacote"], dir_specs)
    por_indice = {}
    for ir in IO.irmaos(yid, IO.raiz_do_dir_specs(dir_specs)):
        if exceto and nome_da_spec.casa(ir.get("arquivo") or
                                        nome_da_spec.arquivo(ir["pacote"]),
                                        exceto):
            continue
        for i in (ir.get("capitulos_declarados") or []):
            if 0 <= i < len(cenas):
                k = (cenas[i].get("kicker") or "").strip()
                if k and k in livres:
                    por_indice.setdefault(i, []).append(ir["pacote"])
    return {"pacote": d["pacote"],
            "por_indice": {i: sorted(set(v)) for i, v in por_indice.items()},
            "n": len(por_indice)}

def texto_dos_livres(yid: str, dir_specs: str = SPECS,
                     exceto: str = None) -> dict:
    """Os capitulos LIVRES daquela origem **com a narracao de cada um**, inteira.

    **Medido em 22/10 as 10:3x, escolhendo a familia do `epomeno-epipedo-s093`.**
    O `nao_mencionados` devolve KICKER, e kicker e TITULO — escrever a partir de
    titulo e inventar conteudo, que e literalmente o que a regra (h) proibe. Logo
    a rodada tem de ler o TEXTO, e nao havia instrumento: eu escrevia um laco
    `python3 -c` na hora e **cortava a saida com `sed -n '45,90p'`**.

    O corte e o defeito. Das **59** origens livres daquela leitura, o texto de
    **28 (47%)** caiu FORA da fatia e eu nunca o li — e escolhi a familia das 31
    que sobraram. E a mesma assinatura da fatia do proxy (19/10 as 19:2x, que
    lia a ponta VELHA da lista) e do `tail -10` das formas de treze cenas (21/10
    as 23:2x, que me fez escolher um esqueleto que ja existia): **ler uma ponta
    de uma lista como se fosse a lista.**

    Por isso ele devolve TUDO e nunca fatia, e o `relato` imprime a contagem na
    PRIMEIRA linha: assim um corte na leitura fica visivel em vez de silencioso.

    **E o conjunto livre e DELEGADO** ao `nao_mencionados` — recomputa-lo aqui
    criaria o segundo dono do indicio de capitulo livre, com o ponto cego do
    kicker repetido divergindo entre os dois.

    **E O PONTO CEGO DO KICKER REPETIDO REAPARECE UMA CAMADA ABAIXO, e vai
    NOMEADO:** o livre e UM texto de kicker, e o longo pode ter DUAS cenas com
    ele. As duas voltam, cada uma com o proprio indice, e `cenas_do_kicker` diz
    quantas sao — filtrar para uma esconderia metade do texto justamente onde o
    `nao_mencionados` ja e cego.

    **Cena com narracao VAZIA sai NOMEADA** (`nar` em branco e `sem_narracao`
    True) em vez de desaparecer: instrumento que devolve vazio nao prova
    ausencia (17/10). E origem sem spec local devolve lista vazia com
    `pacote: None`, que e a regra (h) e nao e defeito — o ramo legitimo fica.
    """
    d = nao_mencionados(yid, dir_specs, exceto)
    livres = set(d["nao_mencionados"])
    cenas = _cenas_do_longo(d["pacote"], dir_specs) if d["pacote"] else []
    quantas = {}
    for c in cenas:
        k = (c.get("kicker") or "").strip()
        if k:
            quantas[k] = quantas.get(k, 0) + 1
    decl = declarados_pelos_irmaos(yid, dir_specs, exceto)["por_indice"]
    fora = []
    for i, c in enumerate(cenas):
        k = (c.get("kicker") or "").strip()
        if k not in livres:
            continue
        nar = (c.get("nar") or "").strip()
        fora.append({"indice": i, "kicker": k, "nar": nar,
                     "sem_narracao": not nar,
                     "declarado_por": decl.get(i, []),
                     "cenas_do_kicker": quantas.get(k, 1)})
    return {"pacote": d["pacote"], "n_capitulos": d["n_capitulos"],
            "n_livres": len(livres), "shorts": d["shorts"], "livres": fora,
            "sem_narracao": [x["indice"] for x in fora if x["sem_narracao"]],
            "declarados_por_irmao": sorted(decl),
            "kickers_repetidos": sorted(k for k in livres
                                        if quantas.get(k, 0) > 1)}


def _linha_dos_declarados(d: dict) -> str:
    """UM dono da frase do conflito, e ela sai nos DOIS ramos.

    Sem conflito ela DIZ isso em vez de calar: ausencia de linha e
    indistinguivel de linha que nao foi escrita, e foi a ausencia dela que me
    levou ao capitulo 74 em 22/10 as 12:3x.
    """
    ns = d.get("declarados_por_irmao") or []
    if not ns:
        return ("  nenhum dos livres e DECLARADO por irmao — e isto e dito em "
                "vez de omitido. Declaracao ausente tambem nao prova ausencia "
                "de uso: a maioria das specs de short solto nao declara "
                "capitulo nenhum.")
    return ("  %d livre(s) sao DECLARADOS por irmao e vao MARCADOS abaixo, nao "
            "filtrados: %s. O `nao_mencionados` casa o TEXTO do kicker e a copy "
            "declara FAIXA em digitos, logo eles saiam como livres — medido em "
            "22/10 as 12:3x, quando isso me custou duas cenas do "
            "`kolejny-poziom-s093`. LEIA a peca do irmao antes de tomar um "
            "deles: declaracao em prosa NAO e veredito nos dois sentidos."
            % (len(ns), ns))

def relato_dos_livres(yid: str, dir_specs: str = SPECS,
                      exceto: str = None) -> str:
    """O texto dos livres, INTEIRO e sem fatia. Codigo de saida sempre zero."""
    d = texto_dos_livres(yid, dir_specs, exceto)
    L = []
    if not d["pacote"]:
        L.append("TEXTO DOS LIVRES de %s: sem spec local (regra h) — os "
                 "capitulos saem da descricao publicada e o texto da faixa de "
                 "legenda. Isto NAO e defeito." % yid)
        return "\n".join(L)
    L.append("TEXTO DOS LIVRES de %s (%s): %d cena(s) de %d capitulo(s), "
             "%d livre(s) por kicker." % (yid, d["pacote"], len(d["livres"]),
                                          d["n_capitulos"], d["n_livres"]))
    L.append("  a contagem vem PRIMEIRO de proposito: foi cortar esta saida com "
             "uma fatia que me fez escolher a familia de 31 de 59 livres em "
             "22/10 as 10:3x. Leia TODAS; o conjunto livre e do "
             "`nao_mencionados`, nao daqui.")
    if d["kickers_repetidos"]:
        L.append("  kicker(s) REPETIDO(S) no longo, logo mais de uma cena por "
                 "entrada livre: %s — o `nao_mencionados` conta uma, aqui vem "
                 "as duas." % ", ".join(d["kickers_repetidos"]))
    if d["sem_narracao"]:
        L.append("  cena(s) LIVRE(S) sem narracao, NOMEADAS em vez de omitidas: "
                 "%s" % d["sem_narracao"])
    L.append(_linha_dos_declarados(d))
    for x in d["livres"]:
        L.append("  %3d | %s | %s%s" % (
            x["indice"], x["kicker"], x["nar"] or "(sem narracao)",
            ("   << DECLARADO por %s" % ", ".join(x["declarado_por"]))
            if x["declarado_por"] else ""))
    L.append("  isto NAO escolhe familia: poe o texto na mesa. Capitulo livre "
             "NAO e familia livre (776), e a comparacao com os irmaos e do "
             "`irmaos_da_origem`.")
    return "\n".join(L)


def main() -> int:
    if len(sys.argv) > 1:
        alvos = sys.argv[1:]
    else:
        # Sem argumento: toda origem que JA rendeu short, uma vez ou mais.
        vistos = {}
        for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
            try:
                sp = json.load(open(p, encoding="utf-8"))
            except Exception:                               # noqa: BLE001
                continue
            le = sp.get("longo_existente")
            if le:
                vistos.setdefault(le, 0)
                vistos[le] += 1
        alvos = sorted(vistos)
    for yid in alvos:
        d = nao_mencionados(yid)
        if not d["pacote"]:
            # O ramo SEM spec local — e ele calava sobre os usos ANTERIORES, que
            # e a informacao que mais importa para nao repetir FAMILIA. Medido em
            # 16/10 as 19:2x: eu escrevi um short inteiro sobre uma familia que o
            # `labtreinamento-s059` ja tinha usado, da MESMA origem, e descobri
            # pelo portao `similaridade` depois de trocar o titulo duas vezes. O
            # modulo TINHA a lista (`shorts_da_origem`) e o `continue` a jogava
            # fora junto com o resto.
            anteriores = [nome for nome, _ in shorts_da_origem(yid)]
            print(f"{yid}: a copy do short nao nomeia nenhuma spec de pacote com "
                  f"cenas de longo. Use capitulos.yml com legenda=true (regra h).")
            if anteriores:
                print(f"   ATENCAO: esta origem JA rendeu {len(anteriores)} "
                      f"short(s) — {', '.join(anteriores)}. Leia a copy de cada "
                      f"um ANTES de escolher a familia de entrada errada: aqui o "
                      f"modulo nao sabe quais capitulos foram usados, so quais "
                      f"PECAS saem daqui.")
            else:
                print("   e esta origem ainda nao rendeu short nenhum — primeiro "
                      "angulo, logo nao ha familia anterior a evitar.")
            continue
        if not d["n_capitulos"]:
            print(f"{yid}: pacote {d['pacote']} sem cenas de longo na spec — "
                  f"use capitulos.yml com legenda=true.")
            continue
        marca = "  *** SUSPEITO: poucas cenas para um longo — confira com " \
                "capitulos.yml antes de usar" if d["suspeito"] else ""
        print(f"{yid} | pacote {d['pacote']} | {d['n_capitulos']} capitulos | "
              f"shorts: {', '.join(d['shorts']) or 'nenhum'}{marca}")
        print(f"   mencionados pela copy ({len(d['mencionados'])}): "
              f"{', '.join(d['mencionados'][:6])}")
        print(f"   NAO mencionados ({len(d['nao_mencionados'])}) — indicio, nao "
              f"prova: {', '.join(d['nao_mencionados'][:10])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
