#!/usr/bin/env python3
"""Escreve a spec de um pacote inteiro — longo, short, thumbnail e copy.

## Por que existe

O teto de producao subiu para 5 pacotes por canal por dia. O teto nunca foi o
que segurava a frota: em 20/08/2026, com o teto ainda em 3, OITO dos treze
canais tinham ZERO spec pendente e a fila girava vazia. O gargalo e que cada
roteiro nascia de um disparo da rotina horaria, escrito a mao, um por hora —
no melhor dia, 24 pacotes para treze canais. A meta de 5 por canal pede 65.

Nenhuma conta fecha por esse caminho. Ou a escrita passa a ser da maquina, ou
o teto de 5 e um numero no arquivo.

## O que este arquivo NAO decide sozinho

Ele nao inventa pauta do nada. A pauta sai de onde ja saia: `pautas_banco` e as
linhas `status='ideia'` de `videos`, que a rotina horaria produz pesquisando
com YOUTUBE_SEARCH e confirmando em fonte institucional. O que muda e a etapa
seguinte — transformar a pauta escolhida em 80 cenas — que era a parte cara e
mecanica.

E ele nao libera nada para render sem passar pelo `fatos.py`. Essa e a
condicao inteira sob a qual a escrita automatica e aceitavel nestes canais:
`labtreinamento` fala de norma com prazo, `sx-educacao` e `next-level-money` de
dinheiro, `seja-mais-magra` de saude. Numero errado ali nao e video ruim, e
dano. O gerador escreve; o portao confere cada quantidade contra duas fontes
que batem; so o que passa vira `.json` com `autoria: maquina`.

## O laco, e por que ele existe

Um unico disparo do modelo nao acerta 12 a 15 minutos. A duracao nao esta no
numero de cenas, esta no numero de CARACTERES por voz — e cada voz tem o seu
par (R chars/s, P s/frase) medido em `ensaio.MODELO_VOZ`. A conta de quanto
texto cabe e feita AQUI, antes de pedir, e conferida DEPOIS de receber:

    escrever -> medir -> corrigir por diferenca de caracteres -> medir

Corrigir por caractere e nao por cena e o ponto. Pedir "acrescente cinco cenas"
devolve cinco cenas de tamanho arbitrario e a medida seguinte erra de novo; a
correcao em caracteres converge, porque e a unidade em que o modelo de voz
mede.

Uso:
    python3 fabrica/autor.py escrever <slug> [--pauta "..."] [--seco]
    python3 fabrica/autor.py contexto <slug>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from difflib import SequenceMatcher

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

MODELO = os.getenv("AUTOR_MODELO", "claude-opus-5")

ALVO_S = 810                 # 13:30, o meio da faixa de 12 a 15 min
TOLERANCIA_S = 60            # +-1 min: dentro disso nao vale outra chamada
RODADAS_DURACAO = 3
SIMILARIDADE_MAX = 0.65      # a mesma que publicacao.similaridade_max


# `_normalizar` e uma copia de tres linhas de src/maquina/stages/compliance.py,
# e a copia e deliberada: aquele modulo importa Config, models e storage, que
# trazem pydantic junto. `fabrica/` roda com stdlib pura em runner sem instalar
# nada, e um import desses derrubaria a geracao por dependencia. Tres linhas
# duplicadas com o motivo escrito custam menos que essa amarra.
def _normalizar(texto: str) -> str:
    return re.sub(r"[^\w\s]", "", texto.lower())


def similaridade(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalizar(a), _normalizar(b)).ratio()


# --------------------------------------------------------------- o contexto

def _campo(texto: str, chave: str) -> str:
    m = re.search(rf'^\s*{chave}:\s*"?([^"\n#]+?)"?\s*(?:#.*)?$', texto, re.M)
    return m.group(1).strip() if m else ""


def contexto(slug: str, sb_url: str = "", sb_key: str = "") -> dict:
    """Tudo que o modelo precisa saber sobre o canal antes de escrever.

    Le o `config/canais/<slug>.yaml` com regex pelo mesmo motivo que
    `publicar.idioma_do_canal`: este arquivo tem de rodar em runner que nao
    instalou PyYAML.
    """
    import publicar as P

    caminho = os.path.join(RAIZ, "config", "canais", f"{slug}.yaml")
    if not os.path.exists(caminho):
        raise SystemExit(f"canal desconhecido: {slug} (sem config/canais/{slug}.yaml)")
    bruto = open(caminho, encoding="utf-8").read()

    ctx = {
        "slug": slug,
        "nome": _campo(bruto, "nome"),
        "idioma": P.idioma_do_canal(slug),
        "voz": _campo(bruto, "voz_edge"),
        "trilha": P.trilha_do_canal_config(slug),
        "estilo": _campo(bruto, "estilo_visual"),
        "categoria_id": _campo(bruto, "categoria_id") or "22",
        "tema": _campo(bruto, "tema"),
        # Os comentarios do yaml sao a memoria do nicho — a medicao de views/dia
        # por formato, a regra do canal, o que ja morreu. Vale mais para escrever
        # o roteiro do que qualquer campo estruturado, e por isso vai inteiro.
        "memoria": bruto,
    }
    ctx.update(_da_ultima_spec(slug))
    if sb_url and sb_key:
        ctx["titulos_publicados"] = titulos_publicados(slug, sb_url, sb_key)
        # A memoria do PROPRIO canal. Ate 20/08/2026 o gerador so via a memoria
        # do NICHO — o que os concorrentes fazem — e nunca o que os videos
        # deste canal ja tinham provado. Duas semanas publicando sem consultar
        # o proprio resultado.
        import aprendizado as A

        try:
            ctx["memoria_propria"] = A.memoria(sb_url, sb_key, slug)
        except Exception as e:
            # Nao derruba a geracao, mas TAMBEM nao segue calado. O gerador
            # precisa saber que esta escrevendo sem a memoria propria, senao
            # ele decide como se ela dissesse "nada a relatar" — e a diferenca
            # entre "nao ha licao" e "nao consegui ler a licao" e enorme.
            ctx["memoria_propria"] = (
                f"MEMORIA DO PROPRIO CANAL: INDISPONIVEL ({e}). Voce esta "
                f"escrevendo sem saber o que este canal ja provou. Seja "
                f"conservador: siga a memoria do nicho e nao invente eixo novo.")
            print(f"aviso: memoria propria indisponivel para {slug}: {e}",
                  file=sys.stderr)
    return ctx


def _da_ultima_spec(slug: str) -> dict:
    """Paleta e fonte vem da spec mais recente do proprio canal.

    Paleta nao esta no yaml: ela varia por pacote e vive dentro do `.json`.
    Herdar a ultima e a escolha conservadora — identidade visual e decisao de
    marca, e sortear cor a cada pacote faria o canal parecer treze canais.
    """
    import glob

    achados = sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", f"{slug}-*.json")))
    for caminho in reversed(achados):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if sp.get("paleta"):
            saida = {"paleta": sp["paleta"], "modelo_de": os.path.basename(caminho)}
            if sp.get("fonte"):
                saida["fonte"] = sp["fonte"]
            return saida
    raise SystemExit(f"{slug} nao tem nenhuma spec anterior — a primeira spec "
                     f"de um canal define paleta e se escreve a mao")


def proximo_numero(slug: str) -> int:
    import glob

    usados = []
    for c in glob.glob(os.path.join(RAIZ, "fabrica", "specs", f"{slug}-*.json")):
        m = re.search(rf"{re.escape(slug)}-(\d+)\.json$", c)
        if m:
            usados.append(int(m.group(1)))
    return (max(usados) + 1) if usados else 2


def _sb(url: str, sb_url: str, sb_key: str):
    import publicar as P

    r = P._req(f"{sb_url}/rest/v1/{url}",
               headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    return json.load(r)


def titulos_publicados(slug: str, sb_url: str, sb_key: str) -> list[str]:
    """Titulo de tudo que ja foi ao ar no canal — a base da similaridade."""
    q = urllib.parse.urlencode({
        "canal": f"eq.{slug}", "youtube_id": "not.is.null",
        "select": "titulo,formato,publicado_em",
        "order": "publicado_em.desc", "limit": "60"})
    return [l["titulo"] for l in _sb(f"videos?{q}", sb_url, sb_key) if l.get("titulo")]


def pautas_disponiveis(slug: str, sb_url: str, sb_key: str) -> list[dict]:
    """As pautas que a rotina ja pesquisou e ainda nao viraram pacote."""
    q = urllib.parse.urlencode({
        "canal": f"eq.{slug}", "status": "eq.ideia",
        "select": "slug,titulo,fonte_pauta,fonte_pauta_vd,criado_em",
        "order": "fonte_pauta_vd.desc.nullslast", "limit": "40"})
    return _sb(f"videos?{q}", sb_url, sb_key)


def inedita(titulo: str, publicados: list[str]) -> tuple[bool, float, str]:
    """A pauta e nova para ESTE canal? Devolve (passa, pior valor, contra quem)."""
    pior, contra = 0.0, ""
    for t in publicados:
        s = similaridade(titulo, t)
        if s > pior:
            pior, contra = s, t
    return pior <= SIMILARIDADE_MAX, pior, contra


# --------------------------------------------------------------- o dimensionamento

# Mediana MEDIDA do corpus em 20/08/2026, sobre as 49 specs com longo: 2,26
# frases por cena (media 2,28, de 1,53 a 3,20). O valor importa porque o termo
# P do modelo de voz e por FRASE: numa voz como a el-GR-Nestoras, com P=1,273,
# seis cenas de short gastam 16 s so em pausa se forem 2,1 frases cada. Chutar
# aqui e errar o dobro la.
FRASES_POR_CENA = 2.26


def densidade(slug: str, bloco: str = "longo") -> float:
    """Frases por cena do PROPRIO canal, medida nas specs que ele ja tem.

    A mediana do corpus serve de piso, mas cada canal escreve com uma densidade
    propria e estavel: o `setiap-level` fica em 1,98 e o `seviye-seviye` em
    2,71 — 37% de diferenca, e o termo P do modelo de voz cobra por frase.

    O ganho e medido, nao suposto. Sobre as 43 specs com mais de 2.000
    caracteres, prever o orcamento com a mediana do corpus erra 3,9% na
    mediana; com a mediana do canal, 1,4%. Como a tolerancia do laco e de 1 min
    em 13,5 (7,4%), a diferenca e entre o primeiro rascunho ja cair dentro e
    gastar mais uma chamada de modelo para chegar la.

    O pior caso nao melhora (17,2%, epomeno-epipedo-002, que tem 1,61 frases
    por cena contra 2,31 do canal). Isso e esperado e nao e problema: o laco
    existe justamente para os casos que o orcamento nao acerta de saida.
    """
    import glob
    import statistics

    import narracao as N

    vistos = []
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                                 f"{slug}-*.json"))):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        cenas = sp.get(bloco) or []
        if len(cenas) < 4:
            continue
        idi = N.idioma_de(sp, None)
        frases = sum(len(N.frases((c or {}).get("nar") or "", idi)) for c in cenas)
        vistos.append(frases / len(cenas))
    return statistics.median(vistos) if vistos else FRASES_POR_CENA


def orcamento_de_texto(voz: str, alvo_s: float, cenas: int,
                       frases_por_cena: float = FRASES_POR_CENA) -> int:
    """Quantos caracteres de narracao cabem em `alvo_s` segundos.

    Inverte a mesma conta de `ensaio.duracao_cena`: duracao = chars/R +
    frases*P, mais o silencio de 0,300 s entre cenas. Sem inverter isso o
    pedido ao modelo sairia em "cenas" ou "palavras", e nenhuma das duas
    unidades tem relacao estavel com o tempo — a id-ID-Gadis le a 15,19
    chars/s num texto de duas frases longas e a 8,19 com doze frases curtas.
    """
    from ensaio import GAP_CENA_S, MODELO_VOZ

    if voz not in MODELO_VOZ:
        raise SystemExit(f"voz {voz!r} sem modelo medido — rode calibrar-vozes "
                         f"antes de dimensionar roteiro para ela")
    R, P = MODELO_VOZ[voz]
    util = alvo_s - GAP_CENA_S * max(0, cenas - 1) - cenas * frases_por_cena * P
    return max(0, int(util * R))


def medir(cenas: list[dict], voz: str) -> float:
    from ensaio import duracao_estimada

    return duracao_estimada(cenas, voz)


def medir_short(cenas: list[dict], voz: str) -> float:
    """A previsao corrigida do vies que o modelo tem em short.

    Dimensionar short com a previsao crua produz roteiro curto demais de forma
    sistematica: 28 dos 30 shorts publicados sairam mais longos que o previsto.
    """
    from ensaio import duracao_estimada_short

    return duracao_estimada_short(cenas, voz)


def chars(cenas: list[dict]) -> int:
    return sum(len((c or {}).get("nar") or "") for c in cenas)


# --------------------------------------------------------------- a escrita

SISTEMA = """Voce escreve o roteiro completo de um video de YouTube, em JSON.

O canal e real, tem publico e tem historico. Voce recebe a memoria do nicho —
o que ja foi medido nele, em views/dia, por formato. Ela nao e decoracao: o
que esta escrito ali como morto esta morto, e repetir isso queima uma vaga.

## O formato de saida

Responda SO com JSON, sem cerca de codigo:

{"titulo": "...", "longo": [cena, ...], "short": [cena, ...],
 "thumb": {"l1": "...", "l2": "..."}, "copy": "markdown"}

Cada cena e um objeto com `layout`, `nar` e os campos do seu layout:

  {"layout": "titulo",  "kicker": "3 palavras", "sub": "5 palavras", "nar": "..."}
  {"layout": "item",    "kicker": "3 palavras", "preco": "um valor curto", "nar": "..."}
  {"layout": "lista",   "kicker": "3 palavras", "itens": ["...", "...", "..."], "nar": "..."}
  {"layout": "barras",  "kicker": "3 palavras", "itens": ["a","b","c"], "alturas": [0.3,0.6,1.0], "nar": "..."}
  {"layout": "cta",     "kicker": "3 palavras", "sub": "5 palavras", "nar": "..."}

A cena que ABRE um capitulo leva `"cap": "titulo do capitulo"`. Todas as
outras levam `"sem_cap": true`. Nunca os dois.

`kicker`, `sub`, `itens` e `preco` sao TEXTO NA TELA: curtos, sem frase
inteira, sem ponto final. `nar` e o que a voz fala.

## O que decide se o video presta

1. RITMO. Frases curtas. No maximo 34 palavras e 3 virgulas por frase. No
   maximo 4 quantidades numa frase — cinco numeros seguidos e planilha falada,
   ninguem ouve. Entre 6% e 45% das frases devem ter 5 palavras ou menos: e o
   soco que quebra a monotonia.
2. ABERTURA. As duas primeiras cenas sao um micro-gancho: uma tensao concreta
   e datada, nao uma promessa. A ultima cena e ponte para o proximo video.
3. CAPITULOS. Entre 6 e 8, cada um com 10 a 14 cenas.
4. LINGUA. TODA a narracao na lingua pedida. Nem uma frase noutra.
5. SEM SLOP. Nada de "neste video vamos explorar", "prepare-se", "isso vai
   mudar tudo", "a verdade que ninguem conta". Comece pelo fato.
6. NUMERO E COMPROMISSO. Todo numero que voce escrever sobre o mundo vai ser
   conferido contra duas fontes independentes, uma delas institucional, ANTES
   de o video ser gravado. Numero que voce nao tem certeza de onde veio: nao
   escreva. Prefira a afirmacao que voce consegue defender a uma mais forte que
   voce nao consegue. Se o dado exato nao existe publicado, diga a ordem de
   grandeza e diga que e ordem de grandeza.

## O short

De 5 a 7 cenas, e um video inteiro por si — nao um trecho do longo. Ele abre
com o resultado, nao com o contexto. Termina mandando ao longo.

## A copy

Markdown com estas secoes, nesta ordem, com estes nomes exatos:

# <titulo interno>
## TITULO        uma linha, ate 100 caracteres
## DESCRICAO     no MINIMO 200 palavras, em paragrafos
## CAPITULOS     escreva exatamente: {CAPITULOS}
## COMENTARIO FIXADO
## HASHTAGS      3 a 5, comecando com #
## TAGS          10 a 18 tags separadas por virgula
## CONFIGURACAO DE STUDIO
## MUSICA / LICENCA   escreva exatamente: {TRILHA}
## NOTA SOBRE FONTES  de onde veio cada numero, e o que o video NAO afirma

O titulo modela a ESTRUTURA do que performa no nicho, nunca o assunto de outro
video. A descricao e para quem vai ler, nao para o algoritmo.

## A pauta e o assunto; a estrutura vem do outlier

A PAUTA que voce recebe diz sobre O QUE falar. Ela NAO diz como o titulo deve
ser montado — e quase nunca vem na forma certa, porque foi pesquisada por
assunto.

Medido em 20/08/2026 no resep-naik-level: todo outlier do nicho tinha CIFRA
mais PERIODO no titulo (de 278 a 6.057 views/dia), e as doze pautas que o canal
tinha em banco eram todas do tipo "por que X esta errado", sem cifra e sem
periodo. Escrever o titulo na forma da pauta seria escrever exatamente na forma
que o nicho mede como morta.

Entao, sempre: leia a memoria do nicho, identifique a ASSINATURA dos titulos
que performam, e reescreva a pauta nessa assinatura. Se a memoria nao deixar
clara qual e a assinatura, diga isso na resposta em vez de inventar uma.

## Quando as duas memorias discordam, a PROPRIA vence

Voce recebe duas memorias. A do NICHO diz o que funciona no assunto, medido nos
concorrentes. A do PROPRIO CANAL diz o que funcionou NESTE canal, medido nos
videos que ele publicou.

Onde as duas concordam, siga sem pensar. Onde discordam, siga a propria: o
nicho descreve um publico, o proprio canal descreve O SEU publico, e e para ele
que o video vai.

O bloco da memoria propria traz um VEREDITO. Ele nao e sugestao — ele diz onde
por o seu melhor material, e em que tamanho escrever o longo. Cumpra-o.

## Numero que vem DENTRO da pauta nao e fonte

A pauta foi escrita por geracao de ideias, nao por medicao. Se ela traz uma
cifra fechada no titulo, trate essa cifra como NAO VERIFICADA ate encontrar
fonte. Medido em 20/08/2026: duas pautas do canal de saude traziam "R$ 27.000
em 5 Anos" e "R$ 18.000 em Shakes e Termogenicos", e nao existe pesquisa
medindo nenhum dos dois.

O caminho certo quando o total nao tem fonte e trocar a AFIRMACAO por um
METODO: em vez de dizer quanto custa, ensinar a conta e deixar o espectador
pôr o proprio numero. Isso e mais util, e verdadeiro.

## Em canal de saude, procure o fato REGULATORIO primeiro

Antes de qualquer afirmacao sobre o que funciona ou nao funciona no corpo,
procure o que a agencia reguladora PERMITE alegar, o que ela proibiu e o que
ela fiscaliza. Isso e conferivel, e datado, e nao depende de voce arbitrar
evidencia clinica em doze minutos.

Exemplo do que isso muda: "suplementos inuteis" e alegacao de eficacia,
insustentavel. "A Anvisa tem 189 alegacoes permitidas em rotulagem e emagrecer
nao e uma delas" e o texto da norma. O segundo e um gancho mais forte E expoe
menos."""


def _pedido(ctx: dict, pauta: str, cenas: int, orcamento: int) -> str:
    pub = ctx.get("titulos_publicados") or []
    return f"""Canal: {ctx['nome']} ({ctx['slug']}).
Lingua da narracao: {ctx['idioma']}. Voz: {ctx['voz']}.

PAUTA: {pauta}

TAMANHO. Escreva {cenas} cenas no longo. A soma dos campos `nar` do longo deve
ficar em {orcamento} caracteres, com folga de 3% para mais ou para menos. Este
numero sai da taxa medida desta voz e e o que decide a duracao do video —
trate-o como restricao, nao como sugestao. O short soma entre
{orcamento_curto(ctx['voz'], ctx['slug'])[0]} e {orcamento_curto(ctx['voz'], ctx['slug'])[1]} caracteres.

JA PUBLICADO NESTE CANAL (nao repita o angulo, e nao chegue perto do titulo):
{chr(10).join('  - ' + t for t in pub[:25]) or '  (nenhum)'}

MEMORIA DO NICHO — o arquivo de configuracao do canal, com o que ja foi medido
nele. Leia os comentarios: eles dizem qual formato entrega e qual morreu.

{ctx['memoria']}
{ctx.get('memoria_propria') or ''}"""


def orcamento_curto(voz: str, slug: str = "") -> tuple[int, int]:
    """Faixa de caracteres do short, dos 30 aos 45 s da rotina.

    Os alvos em SEGUNDOS sao divididos por `VIES_SHORT` antes de virar
    caracteres. `orcamento_de_texto` fala a lingua do modelo cru, e o modelo cru
    mede short 4,7% curto: pedir a ele texto para 43 s entrega 45. Corrigir aqui
    e o mesmo que corrigir na conferencia — os dois lados falam do mesmo video.

    O teto ja desconta o residuo de `prontidao.MARGEM_SHORT`, e mais 2 s de
    folga de escrita, porque o modelo de linguagem nao acerta o alvo na mosca.
    """
    from ensaio import VIES_SHORT
    from prontidao import MARGEM_SHORT, SHORT_MAX_S, SHORT_MIN_S

    fc = densidade(slug, "short") if slug else FRASES_POR_CENA
    piso = orcamento_de_texto(voz, (SHORT_MIN_S + 3) / VIES_SHORT, 6, fc)
    teto = orcamento_de_texto(
        voz, (SHORT_MAX_S / (1 + MARGEM_SHORT) - 2) / VIES_SHORT, 6, fc)
    return piso, teto


def _chamar(sistema: str, mensagens: list[dict], *, modelo: str = "") -> str:
    import modelo as M

    return M.chamar(sistema, mensagens, modelo=modelo or MODELO)


def _so_o_json(texto: str) -> dict:
    import modelo as M

    return M.so_o_json(texto)


def _monta(ctx: dict, bruto: dict, numero: int) -> dict:
    """O JSON do modelo mais o que e do CANAL e nao dele.

    Voz, trilha, idioma, paleta e fonte nao entram no pedido de proposito: sao
    identidade, ja estao decididas, e deixar o modelo repeti-las e criar uma
    segunda copia que uma hora diverge calada — foi assim que o
    kolejny-poziom-005 foi ao ar com a trilha de outro canal.
    """
    sp = {
        "slug": ctx["slug"],
        "pacote": f"{ctx['slug']}-{numero:03d}",
        "idioma": ctx["idioma"],
        "voz": ctx["voz"],
        "trilha": ctx["trilha"],
        "paleta": ctx["paleta"],
        "autoria": "maquina",
        "thumb": bruto.get("thumb") or {},
        "longo": bruto.get("longo") or [],
        "short": bruto.get("short") or [],
        "copy": bruto.get("copy") or "",
    }
    if ctx.get("fonte"):
        sp["fonte"] = ctx["fonte"]
    return sp


def escrever(ctx: dict, pauta: str, *, numero: int = 0, cenas: int = 80,
             modelo: str = "") -> dict:
    """Escreve, mede, e corrige por diferenca de CARACTERES ate caber."""
    numero = numero or proximo_numero(ctx["slug"])
    orcamento = orcamento_de_texto(ctx["voz"], ALVO_S, cenas,
                                   densidade(ctx["slug"], "longo"))
    historico = [{"role": "user", "content": _pedido(ctx, pauta, cenas, orcamento)}]

    sp = None
    for rodada in range(RODADAS_DURACAO + 1):
        resposta = _chamar(SISTEMA, historico, modelo=modelo)
        sp = _monta(ctx, _so_o_json(resposta), numero)
        correcoes = _fora_da_faixa(sp, ctx["voz"])
        dl = medir(sp["longo"], ctx["voz"])
        ds = medir(sp["short"], ctx["voz"]) if sp["short"] else 0.0
        print(f"  rodada {rodada}: {len(sp['longo'])} cenas, {dl/60:.1f} min "
              f"longo, {ds:.0f} s short", file=sys.stderr)
        if not correcoes or rodada == RODADAS_DURACAO:
            break
        historico += [{"role": "assistant", "content": resposta},
                      {"role": "user", "content": "\n\n".join(correcoes) +
                       "\n\nDevolva o JSON inteiro de novo."}]
    return sp


def _fora_da_faixa(sp: dict, voz: str) -> list[str]:
    """O que precisa mudar de tamanho, em CARACTERES, no longo e no short.

    O short entra aqui com o mesmo peso que o longo, e nao como sobra. Em canal
    frio e ele que entrega — os shorts do setiap-level mediram 19,32 views/dia
    contra 0,15 dos longos — e e ele que tem janela dura: 30 a 45 s. Em
    20/08/2026 um short foi ao ar com 47,6 s porque o dimensionamento so olhava
    o longo, e a correcao por cena nao chegava nele.

    A correcao vai em caracteres porque essa e a unidade do modelo de voz.
    Pedir "mais cinco cenas" devolve cinco cenas de tamanho arbitrario, e a
    medida seguinte erra de novo.
    """
    from ensaio import MODELO_VOZ
    from prontidao import MARGEM_SHORT, SHORT_MAX_S, SHORT_MIN_S

    R = MODELO_VOZ[voz][0]
    pedidos = []

    dl = medir(sp["longo"], voz)
    if abs(dl - ALVO_S) > TOLERANCIA_S:
        delta = int((ALVO_S - dl) * R)
        pedidos.append(_como_corrigir("longo", f"{dl/60:.1f} min",
                                      f"{ALVO_S/60:.1f} min", delta))

    if sp.get("short"):
        teto = SHORT_MAX_S / (1 + MARGEM_SHORT)
        alvo = (SHORT_MIN_S + teto) / 2
        ds = medir_short(sp["short"], voz)
        # `ds` ja vem corrigido do vies, entao a faixa util aqui e a faixa
        # REAL, e nao uma faixa encolhida para compensar erro do modelo. O que
        # sobra e mirar no meio dela: o modelo de linguagem nao acerta o alvo
        # na mosca, e o meio e o unico ponto que tolera errar para os dois
        # lados.
        #
        # O delta em caracteres divide por VIES_SHORT porque R e a taxa do
        # modelo CRU: sem isso o pedido de correcao vem 4,7% grande.
        if not (SHORT_MIN_S + 2 <= ds <= teto - 2):
            from ensaio import VIES_SHORT
            delta = int((alvo - ds) / VIES_SHORT * R)
            pedidos.append(_como_corrigir("short", f"{ds:.0f} s",
                                          f"{alvo:.0f} s", delta))
    return pedidos


def _como_corrigir(bloco: str, medido: str, alvo: str, delta: int) -> str:
    verbo = "ALONGUE" if delta > 0 else "ENCURTE"
    como = ("desenvolva os exemplos que ja estao la" if delta > 0
            else "funda frases redundantes e corte adjetivo")
    return (f"A narracao do {bloco} mede {medido} e o alvo e {alvo}. {verbo} a "
            f"narracao do {bloco} em cerca de {abs(delta)} caracteres, "
            f"distribuidos, sem mudar a pauta nem o numero de cenas. Nao encha "
            f"linguica e nao corte fato: {como}.")


def reparar(ctx: dict, sp: dict, faltas: dict, *, modelo: str = "") -> dict:
    """Uma rodada de conserto a partir do que os portoes reprovaram.

    Os portoes falam a lingua do defeito ("3 caractere(s) sem fonte", "cena 12
    com texto na borda"), e essa mensagem e melhor instrucao do que qualquer
    parafrase minha: ela e a mesma que eu leria.
    """
    lista = "\n".join(f"- [{g}] {f}" for g, fs in faltas.items() for f in fs)
    pedido = (f"Os portoes da fabrica reprovaram esta spec. Conserte SO o que "
              f"esta listado, sem reescrever o resto e sem mudar a pauta:\n\n"
              f"{lista}\n\nDevolva o JSON inteiro no mesmo formato.")
    resposta = _chamar(
        SISTEMA,
        [{"role": "user", "content": _pedido(ctx, sp["copy"][:400], len(sp["longo"]),
                                             chars(sp["longo"]))},
         {"role": "assistant", "content": json.dumps(
             {"longo": sp["longo"], "short": sp["short"],
              "thumb": sp["thumb"], "copy": sp["copy"]}, ensure_ascii=False)},
         {"role": "user", "content": pedido}],
        modelo=modelo)
    novo = _monta(ctx, _so_o_json(resposta), int(sp["pacote"].rsplit("-", 1)[1]))
    return novo


def carencia(sb_url: str, sb_key: str, alvo: int = 0) -> list[tuple[str, int]]:
    """Quantas specs faltam a cada canal, do mais carente para o menos.

    A conta e sobre specs PENDENTES — as que existem no repositorio e ainda nao
    foram ao ar. Nao adianta olhar publicados: um canal com 26 videos no ar e
    zero spec pendente e exatamente o canal que a frota nao tem o que renderizar
    amanha, e era o estado de oito dos treze em 20/08/2026.

    Devolve (slug, quantas faltam, quantas pautas ha em banco). O terceiro
    campo existe porque carencia sem pauta nao e trabalho disponivel — e um
    canal esperando pesquisa.

    O alvo padrao e o teto diario do orquestrador, porque e o que a frota
    consegue consumir num dia. Encher a fila acima disso nao produz um video a
    mais: produz spec envelhecendo no repositorio com uma pauta que era atual
    quando foi escrita.

    Canal sem destino no YouTube ou com token morto fica de fora: escrever para
    ele gasta dolar num roteiro que nao tem como publicar.
    """
    import orquestra as O

    if not (sb_url and sb_key):
        raise SystemExit("carencia le o banco: exporte SUPABASE_URL e "
                         "SUPABASE_SERVICE_ROLE_KEY")
    alvo = alvo or O.MAX_POR_DIA_POR_CANAL
    videos = O.busca_videos(sb_url, sb_key)
    est = O.estado(videos)
    com_destino = O.busca_canais_com_destino(sb_url, sb_key)
    com_token = O.canais_sem_token_morto(sb_url, sb_key)

    saida = []
    for slug, d in est["canais"].items():
        if slug not in com_destino or slug not in com_token:
            continue
        faltam = alvo - len(d["specs_pendentes"])
        if faltam <= 0:
            continue
        # Canal sem pauta em banco NAO entra na fila. Nao e detalhe: no
        # primeiro disparo real (run 32349960529, 20/08/2026) a fila devolveu
        # `seviye-seviye`, que tem carencia de spec e ZERO linha
        # `status='ideia'`, e o disparo terminou sem escrever nada. Ordenar so
        # por carencia entrega, com frequencia, exatamente o canal que nao tem
        # como produzir — porque o canal mais carente costuma ser justamente o
        # que a pesquisa nao visita ha mais tempo.
        #
        # Quem enche o banco de pautas e a pesquisa da rotina horaria (PASSO
        # 0), nao este arquivo. Filtrar aqui nao esconde o problema: o canal
        # sem pauta sai listado como tal em `carencia --mostrar-tudo`, e o
        # workflow avisa quando a fila inteira fica vazia por esse motivo.
        pautas = len(pautas_disponiveis(slug, sb_url, sb_key))
        saida.append((slug, faltam, len(d["specs_pendentes"]), pautas))
    # Mais carente primeiro; empate desfeito por quem tem menos spec pendente.
    saida.sort(key=lambda x: (-x[1], x[2], x[0]))
    return [(s, f, p) for s, f, _, p in saida]


# --------------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=("escrever", "contexto", "carencia"))
    ap.add_argument("slug", nargs="?", default="")
    ap.add_argument("--pauta", default="")
    ap.add_argument("--cenas", type=int, default=80)
    ap.add_argument("--modelo", default="")
    ap.add_argument("--alvo", type=int, default=0,
                    help="specs pendentes desejadas por canal (padrao: o teto "
                         "diario do orquestra)")
    ap.add_argument("--mostrar-tudo", dest="mostrar_tudo", action="store_true",
                    help="listar tambem os canais sem pauta em banco")
    ap.add_argument("--seco", action="store_true",
                    help="escreve e mede, mas nao chama o portao de fatos nem grava")
    a = ap.parse_args()

    sb_url = os.getenv("SUPABASE_URL", "")
    sb_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    if a.comando == "carencia":
        fila = carencia(sb_url, sb_key, alvo=a.alvo)
        sem_pauta = [(s, f) for s, f, p in fila if p == 0]
        if sem_pauta and not a.mostrar_tudo:
            print(f"::warning::{len(sem_pauta)} canal(is) com carencia de spec e "
                  f"ZERO pauta em banco — a pesquisa da rotina (PASSO 0) precisa "
                  f"visita-los: {', '.join(s for s, _ in sem_pauta)}", file=sys.stderr)
        produtiveis = 0
        for slug, faltam, pautas in fila:
            if pautas or a.mostrar_tudo:
                print(f"{slug} {faltam}")
                produtiveis += 1
        # Codigo 3 = ha carencia, mas nenhum canal tem pauta para escrever.
        # Isso NAO e "fila cheia", e o estado oposto: a frota vai secar e quem
        # precisa agir e a pesquisa, nao o gerador. Sem um codigo proprio o
        # workflow leria lista vazia como "nada a fazer" e terminaria verde.
        if fila and not produtiveis:
            return 3
        return 0

    if not a.slug:
        ap.error("escrever e contexto pedem um slug")
    ctx = contexto(a.slug, sb_url, sb_key)

    if a.comando == "contexto":
        print(json.dumps({k: v for k, v in ctx.items() if k != "memoria"},
                         ensure_ascii=False, indent=2))
        pautas = pautas_disponiveis(a.slug, sb_url, sb_key) if sb_url else []
        print(f"\n{len(pautas)} pauta(s) em banco:")
        for p in pautas[:10]:
            print(f"  {p.get('fonte_pauta_vd') or '?':>7} v/d  {p.get('titulo') or p['slug']}")
        return 0

    pauta = a.pauta
    if not pauta:
        pautas = pautas_disponiveis(a.slug, sb_url, sb_key)
        pub = ctx.get("titulos_publicados") or []
        for p in pautas:
            t = p.get("titulo") or p["slug"].rsplit("-", 1)[0].replace("-", " ")
            passa, pior, contra = inedita(t, pub)
            if passa:
                pauta = t
                print(f"pauta: {t}\n  (similaridade {pior:.2f} contra {contra!r})",
                      file=sys.stderr)
                break
            print(f"descartada por similaridade {pior:.2f}: {t}", file=sys.stderr)
    if not pauta:
        print(f"{a.slug}: nenhuma pauta disponivel abaixo de "
              f"{SIMILARIDADE_MAX} de similaridade — a rotina precisa pesquisar")
        return 1

    sp = escrever(ctx, pauta, cenas=a.cenas, modelo=a.modelo)

    import prontidao

    destino = os.path.join(RAIZ, "fabrica", "specs", f"{sp['pacote']}.json")
    tmp = destino + ".tmp"
    for tentativa in range(2):
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(sp, f, ensure_ascii=False, indent=2)
        r = prontidao.avalia(tmp)
        # `fatos` reprova por definicao antes da verificacao — ele so entra
        # depois que os portoes baratos aprovarem, para nao gastar dolar
        # conferindo numero de um roteiro que vai ser reescrito de qualquer jeito.
        falhas = {g: f for g, f in (r or {}).items() if f and g != "fatos"}
        if not falhas:
            break
        print(f"portoes reprovaram (tentativa {tentativa + 1}):", file=sys.stderr)
        for g, fs in falhas.items():
            for f in fs:
                print(f"  [{g}] {f}", file=sys.stderr)
        if tentativa == 1:
            os.unlink(tmp)
            print(f"{sp['pacote']}: nao passou nos portoes em duas tentativas")
            return 1
        sp = reparar(ctx, sp, falhas, modelo=a.modelo)

    if a.seco:
        os.unlink(tmp)
        print(json.dumps({"pacote": sp["pacote"], "pauta": pauta,
                          "cenas": len(sp["longo"]),
                          "longo_s": round(medir(sp["longo"], ctx["voz"]), 1),
                          "short_s": round(medir_short(sp["short"], ctx["voz"]), 1)},
                         ensure_ascii=False, indent=2))
        return 0

    import fatos

    print("conferindo fatos...", file=sys.stderr)
    sp["fatos"] = fatos.verificar(sp, modelo=a.modelo)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sp, f, ensure_ascii=False, indent=2)
        f.write("\n")

    for x in sp["fatos"]["afirmacoes"]:
        if x["situacao"] not in fatos.APROVADAS:
            print(f"  ! {x['situacao']:<11} {x['texto'][:88]}", file=sys.stderr)

    if sp["fatos"]["veredito"] != "aprovado":
        # A spec reprovada NAO e apagada: ela vira `.reprovado` ao lado, porque
        # o que o portao rejeitou e a materia-prima do proximo conserto — e
        # porque apagar em silencio esconde quanto o gerador erra.
        os.rename(tmp, destino + ".reprovado")
        import modelo as M

        print(f"{sp['pacote']}: REPROVADO no portao de fatos — "
              f"guardado em {os.path.basename(destino)}.reprovado")
        print(f"custo: {M.GASTO}")
        return 1

    os.rename(tmp, destino)
    import modelo as M

    print(f"{sp['pacote']}: {len(sp['longo'])} cenas, "
          f"{medir(sp['longo'], ctx['voz'])/60:.1f} min longo, "
          f"{medir_short(sp['short'], ctx['voz']):.0f} s short — pronto em "
          f"fabrica/specs/{os.path.basename(destino)}")
    # O custo sai impresso em TODA geracao, e nao num relatorio a parte. Esta e
    # a primeira coisa da maquina que gasta dinheiro por pacote, e a meta de 65
    # pacotes por dia so e sustentavel ou nao dependendo deste numero.
    print(f"custo: {M.GASTO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
