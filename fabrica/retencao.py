"""As DUAS rotas de retencao, e a diferenca entre elas — medido em 16/10 as 16:xx.

Pedido do dono: *"Quero bater recordes. Destravar a maquina. Estude o github,
videos do YouTube, blogs de fora do pais, artigos mais lidos sobre este assunto.
Aprenda de forma profunda"*.

O gargalo desta maquina esta nomeado desde o 693: views/peca e cego para efeito
menor que o DOBRO (CV 0,66 -> 109 pecas por braco), logo os experimentos 37, 38
e 40 sao indecidiveis. A pergunta que vale — *o que faz uma peca romper* — pede
retencao. Este modulo e o resultado de procurar retencao por fora da pendencia 1.

=============================================================================
ROTA A — O HEATMAP PUBLICO (`yt-dlp`), GRATIS E SEM OAUTH. **NAO E RETENCAO.**
=============================================================================
`yt-dlp --dump-json <url>` traz o campo `heatmap`: **100 baldes** com
`start_time`, `end_time` e `value` normalizado de 0 a 1. Sai do proprio
`watch?v=`, onde o campo cru e `intensityScoreNormalized` (cem ocorrencias).
Funciona no sandbox do Composio, sem token, sem banco e sem escopo.

**E A RESSALVA E MAIOR QUE O ACHADO: isto e a curva de REPLAY ("most replayed"),
nao a de retencao.** Um pico marca onde as pessoas VOLTAM, nao onde ficam. Lidas
quatro pecas vencedoras do nosso nicho com heatmap, o pico cai no MEIO
(t = 11,6 a 36,3 s) e a media dos tres primeiros segundos e MENOR que a do resto
em 4 de 4. Ler isso como "abandono nos tres segundos" seria o efeito (C) da
rotina: comparador escolhido sem medir o que ele mede.

**E O LIMIAR FOI MEDIDO, e corrige o unico numero que a web deu.** Um blog
(ubos.tech) dizia "~10 mil views, observado". Sondadas doze pecas do nicho
`excel/planilha` numa separacao monotona limpa:

    5.490 / 12.662 / 22.935 / 45.332 views  -> SEM heatmap (4 de 4)
    63.492 ... 839.127 views                -> COM heatmap (8 de 8)

Logo o limiar esta entre **45 mil e 63 mil**, nao em 10 mil. `n=12`, um nicho,
um dia — declarado.

**E ELE NAO E FUNCAO SO DE VIEWS:** um short de 29 s com **2,1 MILHOES** de
views veio SEM heatmap, e outro de 29 s com 183 mil veio COM. Logo a presenca
nao se preve pela contagem de views sozinha, e eu nao sei a regra.

**O que isto nos da, honestamente:** nada sobre as NOSSAS pecas — a melhor da
frota tem ~1.600 views, um fator ~30 abaixo do limiar. O que da e a forma dos
VENCEDORES do nicho, que e a unica leitura de atencao disponivel hoje.

=============================================================================
ROTA B — A API DE ANALYTICS. **E RETENCAO DE VERDADE, e depende de UM clique.**
=============================================================================
Lido na fonte PRIMARIA (`developers.google.com/youtube/analytics/metrics`,
contando o campo e nao o codigo HTTP):

* **`audienceWatchRatio`** — *"The absolute ratio of viewers watching the video
  at the given point in the video"*, com o ponto dado pela dimensao
  `elapsedVideoTimeRatio`. **E a curva de retencao por peca.**
* **`relativeRetentionPerformance`** — *"how well a video retains viewers ...
  in comparison to all YouTube videos of similar length"*, 0 a 1, ponto a ponto.

**O SEGUNDO E O ACHADO QUE MAIS IMPORTA DE TODA A PESQUISA**, e a razao e o 693:
ele e um comparador **ja normalizado contra a populacao do YouTube de duracao
semelhante**. Isso dispensa construir linha de base com 109 pecas por braco —
o problema que torna 37, 38 e 40 indecidiveis hoje.

A chamada e UMA por peca, e a forma exata e:

    ids=channel==MINE  startDate=..  endDate=..
    metrics=audienceWatchRatio,relativeRetentionPerformance
    dimensions=elapsedVideoTimeRatio
    filters=video==<ID>            # obrigatorio: UM video por chamada

Escopo: `yt-analytics.readonly`, que **ja esta em `fabrica/tokens.py`** desde
09/10. Falta so o clique de consentimento (pendencia 1).

**E O QUE O CLIQUE NAO COMPRA, para eu nao prometer:** a metrica de swipe. Na
pagina oficial de metricas, `swiped` aparece **ZERO** vezes e "chose to view"
**ZERO** — o *"Viewed vs swiped away"* e **so do Studio**, nao da API. A
afirmacao de terceira mao de que 70 a 90% seria o bom e abaixo de 60% colapsaria
a distribuicao (atribuida a uma analise de 3,3 bilhoes de Shorts) **nao foi
verificada em fonte primaria** e nao entra como numero nosso.

**E o que eu NAO sei, e vai dito em vez de suposto:** se o relatorio de retencao
cobre SHORTS. A pagina de dimensoes menciona Shorts oito vezes, mas eu nao
consigo testar sem o escopo. Prometer a curva do short antes do clique seria
afirmar sem medir.

=============================================================================
O QUE A LITERATURA DEU, E A REGUA DA §5 APLICADA
=============================================================================
A rotina avisa que busca na web devolve blog de fornecedor, e devolveu: para
"retencao nos tres primeiros segundos" os numeros vieram 10-30%, 15-25%, 30-50%
e ">80%", de quatro fontes diferentes, **nenhuma oficial e todas se
contradizendo**. Nada disso entra. O unico item aproveitavel foi o NOME de uma
metrica, que me levou a fonte primaria — e la o nome provou que ela nao existe
na API.
"""

# Medido em 16/10, doze pecas do nicho excel/planilha, separacao monotona.
LIMIAR_HEATMAP_OBSERVADO = (45332, 63492)  # (maior SEM, menor COM)
BALDES_DO_HEATMAP = 100

# A excecao que proibe tratar o limiar como funcao de views (medida no mesmo dia).
SEM_HEATMAP_APESAR_DE_VIEWS = {"duracao_s": 29, "views": 2127417}

QUERY_RETENCAO = {
    "ids": "channel==MINE",
    "metrics": "audienceWatchRatio,relativeRetentionPerformance",
    "dimensions": "elapsedVideoTimeRatio",
}
ESCOPO_NECESSARIO = "https://www.googleapis.com/auth/yt-analytics.readonly"

# Na pagina oficial de metricas: zero ocorrencias de "swiped" e "chose to view".
METRICA_DE_SWIPE_EXISTE_NA_API = False


def query_de_retencao(video_id: str, inicio: str, fim: str) -> dict:
    """A chamada do relatorio de retencao, UM video por vez.

    O filtro de UM video e exigencia da API (`audienceWatchRatio` requer
    `elapsedVideoTimeRatio` e filtro de video unico); combinacao invalida devolve
    400 nomeando o campo. Levanta aqui em vez de montar chamada que o servidor
    vai recusar — e porque montar payload a mao contra uma forma documentada e a
    assinatura que matou tres runs (718/729/738).
    """
    if not video_id or "," in video_id:
        raise ValueError(
            f"UM video por chamada; recebi {video_id!r}. A API exige "
            f"filters=video==<ID> unico com elapsedVideoTimeRatio"
        )
    fora = dict(QUERY_RETENCAO)
    fora.update({"startDate": inicio, "endDate": fim,
                 "filters": f"video=={video_id}"})
    return fora


def heatmap_tem_resolucao(duracao_s: float) -> float:
    """Segundos por balde. Em short de 30 s cada balde mede 0,3 s."""
    if duracao_s <= 0:
        raise ValueError("duracao tem de ser positiva")
    return duracao_s / BALDES_DO_HEATMAP


def baldes_ate(duracao_s: float, segundos: float) -> int:
    """Quantos baldes cobrem os primeiros `segundos` de uma peca."""
    n = round(BALDES_DO_HEATMAP * segundos / duracao_s)
    return max(1, min(BALDES_DO_HEATMAP, n))


def forma_do_replay(heatmap: list[dict], duracao_s: float,
                    segundos: float = 3.0) -> dict:
    """Le a curva de REPLAY — e o nome da funcao diz isso de proposito.

    NAO devolve "retencao" em chave nenhuma. Quem quiser retencao usa a rota B.
    """
    if not heatmap:
        raise ValueError(
            "heatmap vazio: isto e AUSENCIA DE LEITURA (peca abaixo do limiar "
            f"observado de {LIMIAR_HEATMAP_OBSERVADO[1]} views, ou a regra que "
            "eu nao conheco), NAO replay zero"
        )
    v = [b["value"] for b in heatmap]
    n = baldes_ate(duracao_s, segundos)
    resto = v[n:] or v
    pico = v.index(max(v))
    return {
        "baldes": len(v),
        "media_inicio": sum(v[:n]) / n,
        "media_resto": sum(resto) / len(resto),
        "balde_do_pico": pico,
        "t_do_pico_s": round(pico * duracao_s / BALDES_DO_HEATMAP, 1),
        "inicio_e_o_pico": pico < n,
    }


def relato() -> str:
    lo, hi = LIMIAR_HEATMAP_OBSERVADO
    return "\n".join([
        "RETENCAO — duas rotas, e elas medem coisas DIFERENTES:",
        f"  A) heatmap publico (yt-dlp): GRATIS, sem OAuth, {BALDES_DO_HEATMAP} "
        f"baldes — mas e REPLAY, nao retencao,",
        f"     e so existe acima de algo entre {lo} e {hi} views (medido, n=12).",
        "     A melhor peca da frota tem ~1.600 views: nao serve para NOS.",
        "  B) API de Analytics: audienceWatchRatio + relativeRetentionPerformance",
        "     por elapsedVideoTimeRatio, UM video por chamada. E retencao de",
        "     verdade, e o relative JA e normalizado contra videos de duracao",
        "     semelhante — o que dispensa as 109 pecas por braco do 693.",
        f"     Escopo {ESCOPO_NECESSARIO.split('/')[-1]} JA esta no codigo;",
        "     falta UM clique de consentimento (pendencia 1).",
        "  O que o clique NAO compra: a metrica de swipe nao existe na API.",
    ])


if __name__ == "__main__":
    print(relato())
