#!/usr/bin/env python3
"""Quantos pacotes a frota dispara AGORA, e o que falta em cada um dos outros.

Existe porque a pergunta "quantos pacotes estao prontos?" vinha sendo respondida
de cabeca, e a resposta mudava. Cada spec passa por sete portoes, cada um com
um custo de descoberta diferente:

  identidade   `pacote` e `idioma` presentes e coerentes com config/canais/.
               Custo de descobrir tarde: o render escreve num diretorio e a
               entrega procura noutro; ou o video sobe marcado na lingua errada.
  copy         >= 2 secoes reconheciveis, tags dentro do orcamento de 480, e a
               descricao acima das 200 palavras que a rotina pede. Custo tarde:
               o publicar.py aborta DEPOIS do render.
  idioma       a narracao inteira na lingua da VOZ. Custo tarde: o pacote —
               um roteiro meio virado passa nos outros seis e nao tem conserto
               parcial, o roteiro se reescreve.
  narracao     0 erros duros (planilha falada, slop). Custo tarde: o video sai
               com uma cena que ninguem consegue ouvir.
  layout       0 cenas com texto na borda. Custo tarde: 17 min de render e uma
               vaga de publicacao, medido no nivel-do-jogo-002.

O portao `copy` roda contra o `copy` da spec, nao contra o copy.md do render —
entao ele valida a ESTRUTURA e as tags, e nao os capitulos cronometrados, que so
existem depois dos clipes. E o suficiente para separar spec publicavel de spec
que vai abortar.

Uso:
    python3 fabrica/prontidao.py            # todas as specs
    python3 fabrica/prontidao.py <spec.json>
"""
from __future__ import annotations

import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

MIN_PALAVRAS_DESCRICAO = 200


def _gate_identidade(caminho, sp):
    from publicar import idioma_do_canal, trilha_do_canal_config

    faltas = []
    nome = os.path.basename(caminho)[:-5]
    if sp.get("pacote") != nome:
        faltas.append(f"pacote={sp.get('pacote')!r} != {nome!r}")
    do_canal = idioma_do_canal(sp["slug"])
    if sp.get("idioma"):
        if do_canal and sp["idioma"] != do_canal:
            faltas.append(f"idioma={sp['idioma']!r} mas canal e {do_canal!r}")
    elif not do_canal:
        faltas.append("sem idioma na spec e sem config/canais/")

    # A trilha e do CANAL, nunca do pacote: e a assinatura sonora que o
    # espectador reconhece antes de ler qualquer coisa. Trocar de faixa entre
    # videos do mesmo canal e o equivalente sonoro de trocar de logo.
    #
    # Este portao existe porque em 19/08/2026 o kolejny-poziom-005 foi ao ar
    # com Deliberate_Thought num canal registrado em Wholesome. Os sete
    # portoes passaram — nenhum lia a trilha do canal, que so existia no
    # banco. O unico que pegou foi um teste de repositorio, e ele so podia
    # pegar DEPOIS de uma segunda spec divergir da primeira.
    do_canal_trilha = trilha_do_canal_config(sp["slug"])
    if do_canal_trilha and sp.get("trilha") and sp["trilha"] != do_canal_trilha:
        faltas.append(f"trilha={sp['trilha']!r} mas a identidade do canal e "
                      f"{do_canal_trilha!r} (config/canais/{sp['slug']}.yaml)")
    return faltas


def _gate_copy(sp):
    """Le a copy da spec como o publicar.py leria, sem exigir o render."""
    import publicar as P

    bruto = sp.get("copy")
    if not isinstance(bruto, str) or len(bruto) < 200:
        return ["copy e bilhete, nao markdown — publicar.py aborta"]

    # ler_copy prefere o copy.md do workdir; aqui forcamos a spec passando um
    # diretorio que nao tem copy.md, e trocamos os placeholders por conteudo
    # plausivel para o _sem_placeholder nao reprovar o que o render preencheria.
    falso = dict(sp)
    falso["copy"] = bruto.replace("{CAPITULOS}", "0:00 abertura").replace(
        "{TRILHA}", "Music: Cipher2 by Kevin MacLeod"
    )
    try:
        cp = P.ler_copy(falso, os.path.join(RAIZ, "nao-existe"))
    except SystemExit as e:
        return [str(e)]

    faltas = []
    if not cp["titulo"] or len(cp["titulo"]) > 100:
        faltas.append(f"titulo com {len(cp['titulo'])} chars (limite 100)")
    palavras = len(cp["descricao"].split())
    if palavras < MIN_PALAVRAS_DESCRICAO:
        faltas.append(f"descricao com {palavras} palavras (minimo {MIN_PALAVRAS_DESCRICAO})")
    if not cp["tags"]:
        faltas.append("sem tags")
    else:
        mantidas, total = P.orcamento_tags(cp["tags"])
        if len(mantidas) < len(cp["tags"]):
            faltas.append(
                f"orcamento de tags corta {len(cp['tags']) - len(mantidas)} de "
                f"{len(cp['tags'])} ({total} chars)"
            )
    if not cp.get("hashtags"):
        faltas.append("sem hashtags")
    if not cp.get("comentario"):
        faltas.append("sem comentario fixado")
    return faltas


def _gate_narracao(caminho):
    import narracao

    sp = json.load(open(caminho, encoding="utf-8"))
    erros, _avisos, _todas = narracao.analisa(sp, narracao.idioma_de(sp, None))
    return erros


def _gate_layout(sp):
    import layout

    try:
        return layout.analisa(sp)
    except RuntimeError as e:
        # `usar_fonte` aborta quando a fonte do canal nao esta na maquina — o
        # agla-level pede Noto Sans Devanagari. Isso e defeito do AMBIENTE, nao
        # da spec, e reprovar a spec por isso esconderia o que ela tem de bom.
        # (O frota.yml instala fonts-noto-core, que traz Devanagari; medido em
        # 13/08/2026 — quatro familias apos o apt-get.)
        return [f"AMBIENTE, nao a spec: {e}"]


_COBERTURA: dict[int, int] = {}


def _fontes_que_cobrem(cp: int) -> int:
    """Quantas fontes instaladas tem glifo para este codepoint."""
    import subprocess

    if cp not in _COBERTURA:
        r = subprocess.run(["fc-list", f":charset={cp:#x}"],
                           capture_output=True, text=True)
        _COBERTURA[cp] = len([l for l in r.stdout.splitlines() if l.strip()])
    return _COBERTURA[cp]


def _gate_glifos(sp):
    """Nenhum caractere de TELA pode cair em tofu.

    `usar_fonte` ja protege a spec que DECLARA fonte — ele aborta se a familia
    nao estiver instalada. O que ele nao cobre e a spec que NAO declara: ela usa
    o DejaVu Sans e o fontconfig escolhe um fallback sozinho. Se nenhuma fonte
    da maquina tiver o glifo, o resultado nao e vazio, e TOFU: o retangulo
    branco. Tofu tem tinta, entao passa no visual.py e no layout.py, e so
    aparece assistindo ao video.

    ATENCAO, e o que mais importa aqui: a resposta deste portao so vale na
    MAQUINA QUE VAI RENDERIZAR. O container desta sessao tem cobertura Noto
    muito mais larga que o runner do frota.yml, que instala apenas
    fonts-noto-core e fonts-noto-cjk — medido em 13/08/2026, aqui nao existe
    um so codepoint alfabetico com zero fontes, entao rodar isto aqui aprova
    coisa que o runner transformaria em tofu. Por isso o frota.yml chama este
    modulo ANTES do render, junto com o layout.py: la o resultado e verdadeiro.

    O corpus de hoje tem duas escritas nao latinas — grego (64 fontes aqui) e
    devanagari (13, e a agla-level-003 ainda declara a familia certa). Nenhuma
    corre risco agora; este portao existe para a proxima spec, nao para as de
    hoje.

    So o texto de TELA entra: kicker, sub, preco, itens, thumb, e o `nar` do
    short (que vira legenda queimada). O `nar` do longo vai para o .srt, que o
    YouTube renderiza com as fontes do espectador.
    """
    alvos = []
    for c in sp.get("longo") or []:
        for k in ("kicker", "sub", "preco"):
            if c.get(k):
                alvos.append(c[k])
        alvos.extend(c.get("itens") or [])
    for c in sp.get("short") or []:
        for k in ("kicker", "sub", "preco", "nar"):
            if c.get(k):
                alvos.append(c[k])
        alvos.extend(c.get("itens") or [])
    for k in ("l1", "l2"):
        if (sp.get("thumb") or {}).get(k):
            alvos.append(sp["thumb"][k])

    sem_glifo = sorted({
        ch for ch in "".join(alvos)
        if ch.isalpha() and _fontes_que_cobrem(ord(ch)) == 0
    })
    if not sem_glifo:
        return []
    amostra = " ".join(f"{ch!r} (U+{ord(ch):04X})" for ch in sem_glifo[:8])
    return [f"{len(sem_glifo)} caractere(s) sem fonte nesta maquina — sairiam "
            f"como tofu: {amostra}"]


# Caracteres que a lingua EXIGE e que o ASCII nao tem. Grego, hindi e as demais
# escritas nao latinas ficam de fora porque o portao de idioma ja as pega: la a
# falta de acento nao existe, o alfabeto inteiro seria outro.
DIACRITICOS = {
    "tr": "çğıöşüÇĞİÖŞÜâî",
    "pl": "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ",
    "pt": "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÇ",
    "es": "áéíóúñüÁÉÍÓÚÑ",
}

# Abaixo disso o canal nao usa acento o bastante para servir de referencia.
PISO_REFERENCIA = 0.02


def _densidade_diacritica(cenas, tabela: str) -> float | None:
    txt = "".join((c or {}).get("nar") or "" for c in cenas)
    letras = sum(1 for ch in txt if ch.isalpha())
    if not letras:
        return None
    return sum(1 for ch in txt if ch in tabela) / letras


# Quantas specs precisam acentuar para que a mediana delas vire referencia. Com
# duas, uma convencao pessoal de um canal so viraria lei para a lingua inteira.
MINIMO_REFERENCIA_IDIOMA = 3


def _referencia_do_idioma(base: str, tabela: str, caminho: str) -> float:
    """Quanto acentua quem escreve esta lingua DIREITO, nos outros canais.

    So entram as specs acima do piso: a pergunta e "qual e a densidade de quem
    acentua", e uma spec em ASCII nao responde essa pergunta — ela e o caso que
    o portao existe para pegar. Deixar as zeradas na conta seria permitir que o
    defeito rebaixasse a barra que deveria acusa-lo.
    """
    import glob
    import statistics

    eu = os.path.basename(caminho)
    boas = []
    for outro in sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs", "*.json"))):
        if os.path.basename(outro) == eu:
            continue
        try:
            o = json.load(open(outro, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        idi = (o.get("idioma") or "").lower()
        outro_base = ("pt" if idi.startswith("pt") else
                      "es" if idi.startswith("es") else idi)
        if outro_base != base:
            continue
        d = _densidade_diacritica(o.get("longo") or [], tabela)
        if d is not None and d >= PISO_REFERENCIA:
            boas.append(d)
    if len(boas) < MINIMO_REFERENCIA_IDIOMA:
        return 0.0
    return statistics.median(boas)


def _gate_ortografia(caminho, sp):
    """A narracao usa os acentos que as OUTRAS specs deste canal usam?

    Nenhum dos sete portoes olhava para isto, e o defeito e mudo: turco sem
    acento continua parecendo turco, passa no portao de idioma, passa no de
    glifos (ASCII sempre tem fonte), e chega ao TTS — que pronuncia outra coisa.
    "acacagim" nao e "acacagim", e "sozlesme" nao e "sozlesme".

    Medido em 20/08/2026 sobre o corpus, densidade de acento por letra:

        tr  seviye-seviye-002/003    0,1270 e 0,1271     consistente
        pl  kolejny-poziom-006       0,0677
        pl  kolejny-poziom-003/004   0,0000              <- foram ao ar assim
        pt  varias                   0,0000              <- convencao mista

    Por isso o portao NAO afirma que toda lingua precisa de acento: ele afirma
    que uma spec nao pode divergir do PROPRIO CANAL. Onde as specs anteriores
    acentuam, a nova tem de acentuar; onde o canal nunca acentuou, nao ha
    referencia e o portao se cala. Assim ele pega a divergencia real sem
    inventar uma regra de ortografia que o corpus nao sustenta.

    Descoberto escrevendo a seviye-seviye-004: eu escrevi as 72 cenas em ASCII
    num canal cujas outras duas specs acentuam 12,7% das letras, e nada acusou.
    """
    import glob
    import statistics

    idi = (sp.get("idioma") or "").lower()
    base = ("pt" if idi.startswith("pt") else
            "es" if idi.startswith("es") else idi)
    tabela = DIACRITICOS.get(base)
    if not tabela:
        return []

    minha = _densidade_diacritica(sp.get("longo") or [], tabela)
    if minha is None:
        return []

    slug = sp.get("slug") or ""
    eu = os.path.basename(caminho)
    vizinhas = []
    for outro in sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs", f"{slug}-*.json"))):
        if os.path.basename(outro) == eu:
            continue
        try:
            o = json.load(open(outro, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        d = _densidade_diacritica(o.get("longo") or [], tabela)
        if d is not None:
            vizinhas.append(d)

    referencia = statistics.median(vizinhas) if vizinhas else 0.0
    if referencia < PISO_REFERENCIA:
        # O canal nao serve de referencia. Ate 20/08/2026 o portao parava aqui,
        # e esse era o buraco: um canal ERRADO POR INTEIRO tem referencia zero
        # e nunca acusa nada. O sx-educacao tem duas specs, as duas com 0,00%
        # de acento em portugues, e as duas ja no ar — o portao ficou calado
        # justamente onde havia mais o que dizer.
        #
        # A saida e trocar de populacao, nao de regra: pergunta-se quanto
        # acentua quem escreve ESTA LINGUA direito, olhando as specs dos OUTROS
        # canais do mesmo idioma. E so as que acentuam entram na conta — incluir
        # as zeradas seria deixar o defeito rebaixar a propria referencia. Em
        # pt a mediana das nove specs sai 1,85% (abaixo do piso, portao mudo de
        # novo); a mediana das que acentuam sai 4,10%, que e a resposta certa.
        referencia = _referencia_do_idioma(base, tabela, caminho)
    if referencia < PISO_REFERENCIA:
        return []          # nem o canal nem o idioma dao referencia

    # Metade da referencia e folga larga de proposito: texto varia, e o que
    # este portao procura e o caso de ASCII puro, nao a flutuacao normal.
    if minha < referencia / 2:
        de_onde = (f"nas outras specs de {slug}" if vizinhas
                   and statistics.median(vizinhas) >= PISO_REFERENCIA
                   else f"nas specs de {base} que acentuam")
        return [f"acentuacao fora do padrao: {minha:.1%} das letras contra "
                f"{referencia:.1%} {de_onde}. Em {base} isso muda a pronuncia "
                f"do TTS, e nenhum outro portao enxerga — o texto continua "
                f"parecendo a lingua certa"]
    return []


def _gate_capitulos(sp):
    """Capitulo que a spec desenha e o render nao produz some calado.

    `copy_md.capitulos` so trata como abertura de secao uma cena de layout
    `titulo` ou `broll` — a heuristica existe porque `cap` e usado SOLTO no
    acervo antigo (a cocina-por-niveles-002 tem 69 cenas com `cap`) e honrar
    todos viraria capitulo a cada minuto. Isso ja custou um pacote antes, com
    `broll`, e virou o aprendizado 311.

    O caso novo e o oposto: nas specs escritas com os ajudantes T/I/L/B/C o
    `cap` aparece UMA VEZ por capitulo, e e marcador de autor. Quando um deles
    abre com layout `item`, o render descarta e ninguem ve — a seviye-seviye-004
    desenhou 7 capitulos e publicou 6.

    Por isso o portao so opina quando o `cap` esta sendo usado como marcador:
    entre 6 e 8 ocorrencias, que e a faixa que a rotina pede. Fora dela ele se
    cala, porque ali quem manda e a heuristica de layout e mexer nisso quebraria
    o acervo.

    Os tempos sao estimados pelo modelo de voz, e nao pelos clipes: o portao
    roda ANTES do render. A estimativa erra ~2% no longo, e o que se compara e
    a CONTAGEM de capitulos, que nao muda por dois por cento.
    """
    import copy_md
    from ensaio import GAP_CENA_S, MODELO_VOZ, duracao_cena

    longo = sp.get("longo") or []
    voz = sp.get("voz", "")
    desenhados = sum(1 for c in longo if (c or {}).get("cap"))
    if not (6 <= desenhados <= 8) or voz not in MODELO_VOZ:
        return []

    tempos = [duracao_cena((c or {}).get("nar") or "", voz) + GAP_CENA_S
              for c in longo]
    try:
        produzidos = len(copy_md.capitulos(sp, tempos))
    except (KeyError, IndexError) as e:
        return [f"nao consegui simular os capitulos: {e}"]

    if produzidos == desenhados:
        return []
    perdidos = [c.get("cap") for c in longo
                if c.get("cap") and c.get("layout") not in ("titulo", "broll")]
    detalhe = f" — abre(m) em layout que o render ignora: {perdidos}" if perdidos else ""
    return [f"{desenhados} capitulos desenhados e {produzidos} produzidos{detalhe}. "
            f"Abertura de capitulo tem de ser layout `titulo` ou `broll`"]


PISO_LONGO_S = 480     # 8 min: piso duro da rotina
TETO_LONGO_S = 900     # 15 min, salvo canal escalonado
SHORT_MIN_S, SHORT_MAX_S = 30, 45
# Residuo do modelo de voz em SHORT, DEPOIS de corrigido o vies.
#
# Esta constante tem uma historia que vale mais que o numero. Ela mudou quatro
# vezes em dois dias — 3%, 5%, 7%, 7,5% — e as quatro pelo mesmo motivo: um
# short novo ia ao ar, eu media UM erro, ele estourava a margem, eu subia a
# margem para cobrir o pior caso ate ali. Isso nunca converge, porque o MAXIMO
# de uma amostra cresce com n. Era perseguicao, nao regra.
#
# O que encerrou a perseguicao nao foi estatistica melhor: foi descobrir que o
# dado ja estava no banco. A esteira grava `videos.duracao_s` com ffprobe do
# arquivo montado — a duracao REAL de todo short publicado esta la desde o
# primeiro dia. Eu media de um em um o que dava para medir de uma vez (a mesma
# classe do aprendizado 378: contar arquivo em vez de contar trabalho).
#
# Com as 30 medidas validas de uma vez, o diagnostico muda: 28 das 30 erram
# para CIMA, mediana +4,7%. Nao e dispersao em torno do certo, e VIES — e eu
# tinha declarado o contrario de manha, com nove medidas e tres delas mal
# pareadas. Margem de seguranca nao conserta vies: ela esconde, e cobra o preco
# de reprovar roteiro bom. Quem conserta e `ensaio.VIES_SHORT`, aplicado a
# PREVISAO. A margem fica so com o que sobra depois dele.
#
# Percentil 95 do residuo, nao o maximo: com n=30 o percentil e estimavel e o
# maximo continua sendo ruido. Os dois numeros saem de `calibra_short.py` e
# `test_calibra_short` cobra que eles batam com `medidas_short.tsv`.
MARGEM_SHORT = 0.043


def _gate_duracao(sp):
    """Duracao pelos DOIS termos medidos da voz: chars/R + frases*P.

    A versao anterior dividia por uma taxa unica e somava 0,5 s por CENA de
    respiracao. Os dois pedacos estavam errados, e no mesmo sentido.

    A taxa unica nao existe: medido em 14/08/2026, a id-ID-Gadis le a 15,19
    chars/s num texto de duas frases longas e a 8,19 no mesmo idioma com doze
    frases curtas. Mesma voz, 85% de diferenca. O que muda nao e a voz, e a
    quantidade de pontos finais — e cada ponto final custa silencio.

    E a respiracao nao e por cena: e por FRASE. O corpus tem 2,13 frases por
    cena na mediana, mas vai de 1,53 (agla-level-003) a 3,20 (nivel-do-jogo-002)
    — um fator de dois que o termo por cena nao enxergava.

    O short e o que mais importa aqui: em canal frio e ele que entrega, e a
    rotina exige 30 a 45 s. Abaixo de 30 nao e "curtinho", e fora do formato.
    """
    from ensaio import MODELO_VOZ, duracao_estimada, duracao_estimada_short

    voz = sp.get("voz", "")
    if voz not in MODELO_VOZ:
        return [f"voz {voz!r} sem modelo medido — meca antes de dimensionar"]

    faltas = []
    longo = sp.get("longo") or []
    if longo:
        d = duracao_estimada(longo, voz)
        if d < PISO_LONGO_S:
            faltas.append(f"longo com {d/60:.1f} min — abaixo do piso de 8 min")
        elif d > TETO_LONGO_S:
            faltas.append(f"longo com {d/60:.1f} min — acima de 15 min; so vale "
                          f"em canal escalonado, e o escalonamento vai no config")
    short = sp.get("short") or []
    if short:
        ds = duracao_estimada_short(short, voz)
        # `duracao_estimada_short` ja aplica `ensaio.VIES_SHORT`, o vies
        # medido do modelo em short. `ds` aqui e previsao CORRIGIDA — o que
        # sobra e o residuo, e e so ele que MARGEM_SHORT precisa cobrir.
        #
        # A conta e sobre a PREVISAO, nao sobre o teto: o erro vale
        # `ds x (1 + margem)`, entao o limite e `SHORT_MAX_S / (1 + margem)`.
        # A versao anterior escrevia `SHORT_MAX_S x (1 - margem)`, que e outra
        # coisa — mais apertada, e apertada por acidente e nao por decisao.
        #
        # A margem vale so no TETO. No piso o vies ja foi corrigido, e o que
        # sobra e simetrico: nao ha lado seguro para escolher.
        teto = SHORT_MAX_S / (1 + MARGEM_SHORT)
        if ds < SHORT_MIN_S:
            faltas.append(f"short com {ds:.0f} s — abaixo dos {SHORT_MIN_S} s "
                          f"que a rotina pede")
        elif ds > teto:
            faltas.append(f"short com {ds:.1f} s previstos (ja corrigidos do "
                          f"vies) — acima de {teto:.1f} s. O teto da rotina e "
                          f"{SHORT_MAX_S} s e o residuo do modelo chega a "
                          f"{MARGEM_SHORT:.1%}, entao {teto:.1f} previstos ja e "
                          f"o limite seguro")
    return faltas


def _gate_idioma(sp):
    """A narracao INTEIRA na lingua da voz. Nenhum outro portao olha para isso.

    Custo de descobrir tarde: o pacote. Um roteiro meio indonesio e meio
    portugues passa nos outros seis — o ritmo e medido igual, o alfabeto e o
    mesmo, os caracteres contam igual — e produz um video que ninguem assiste,
    porque o TTS le portugues com fonemas indonesios.
    """
    import idioma

    return idioma.analisa(sp)


def _gate_fatos(sp):
    """Numero conferido contra fonte — mas so em spec escrita pela MAQUINA.

    O corte por `autoria` nao e concessao, e a fronteira exata do problema.
    Enquanto todo roteiro saia escrito a mao pela rotina horaria, as "duas
    fontes que batem" eram cumpridas na PESQUISA, antes de a spec existir, e
    ficavam registradas no cabecalho do `.build.py` — o labtreinamento-003 cita
    committee.iso.org e quatro certificadoras em doze linhas de docstring. Um
    portao que exigisse veredito dessas specs estaria pedindo que a maquina
    reconferisse trabalho ja conferido, e o preco seria alto: nenhuma das 50
    specs do diretorio tem `fatos`, entao ligar isto para todas travaria a
    frota inteira no proximo ciclo de trinta minutos.

    O que muda com o gerador e QUEM garante. Texto escrito por modelo afirma
    com a mesma fluencia sendo verdade ou nao, e nenhum dos outros sete portoes
    olha para o mundo. Entao a regra e: quem se declara `autoria: maquina`
    passa pelo `fatos.py`; quem nao se declara continua respondendo pela
    pesquisa que ja fez.

    Spec de maquina sem o campo nao existe: o `autor.py` grava os dois juntos.
    """
    if sp.get("autoria") != "maquina":
        return []
    import fatos

    return fatos.conferir(sp)


PORTOES = (
    ("identidade", lambda c, s: _gate_identidade(c, s)),
    ("fatos", lambda c, s: _gate_fatos(s)),
    ("copy", lambda c, s: _gate_copy(s)),
    ("narracao", lambda c, s: _gate_narracao(c)),
    ("idioma", lambda c, s: _gate_idioma(s)),
    ("glifos", lambda c, s: _gate_glifos(s)),
    ("ortografia", lambda c, s: _gate_ortografia(c, s)),
    ("capitulos", lambda c, s: _gate_capitulos(s)),
    ("duracao", lambda c, s: _gate_duracao(s)),
    ("layout", lambda c, s: _gate_layout(s)),
)


def avalia(caminho):
    sp = json.load(open(caminho, encoding="utf-8"))
    if not sp.get("longo"):
        return None
    return {nome: fn(caminho, sp) for nome, fn in PORTOES}


def main() -> int:
    alvos = sys.argv[1:] or sorted(glob.glob(os.path.join(RAIZ, "fabrica/specs/*.json")))
    prontas, travadas = [], []

    for caminho in alvos:
        r = avalia(caminho)
        if r is None:
            continue
        nome = os.path.basename(caminho)[:-5]
        falhas = {g: f for g, f in r.items() if f}
        if falhas:
            travadas.append((nome, falhas))
        else:
            prontas.append(nome)

    print(f"PRONTAS ({len(prontas)}):")
    for n in prontas:
        print("   ", n)
    print(f"\nTRAVADAS ({len(travadas)}):")
    for n, falhas in travadas:
        print(f"    {n}")
        for portao, itens in falhas.items():
            print(f"        {portao}: {len(itens)} problema(s)")
            for i in itens[:3]:
                print(f"          - {i[:150]}")
            if len(itens) > 3:
                print(f"          ... e mais {len(itens) - 3}")

    total = len(prontas) + len(travadas)
    print(f"\n-> {len(prontas)}/{total} specs disparam a frota hoje")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
