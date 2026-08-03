"""Pesquisa de subnicho: descobre o que ja performa antes de escrever titulo.

Alimenta o pilar 1. A regra do playbook e "pegar o que esta validado e
remodelar" — mas so da para remodelar o que foi medido primeiro. Este modulo
usa a API oficial (dados estruturados, com views e data) em vez de raspar tela.

Custo de cota: search.list = 100 unidades, videos.list = 1. Uma pesquisa
completa fica em ~100-300 unidades do teto diario de 10.000.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from ..config import Config
from ..providers.base import LLM

log = logging.getLogger("maquina.pesquisa")

# Palavras funcionais que poluem a contagem de frequencia sem informar nada.
# Cobre indonesio, ingles e portugues — os idiomas que aparecem no corpus.
VAZIAS = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "ini", "itu", "pada",
    "adalah", "tidak", "bisa", "akan", "sudah", "juga", "atau", "saya", "kamu",
    "the", "a", "an", "and", "or", "to", "of", "in", "for", "on", "with", "is",
    "how", "what", "why", "you", "your", "de", "da", "do", "que", "para", "com",
    "um", "uma", "os", "as", "no", "na", "por", "se", "mais",
}

EXTRAIR_PADROES_PROMPT = """Abaixo estao titulos de videos do YouTube que ja
performam no subnicho (com views e views/dia). Estao em {idioma}.

Analise e devolva, em {destino}:
1. Os padroes estruturais recorrentes dos titulos que mais performam.
2. As palavras-chave que se repetem e parecem carregar a busca.
3. O que os titulos de alta performance tem que os de baixa nao tem.

Depois proponha 10 titulos NOVOS em {idioma}: semelhantes ao padrao validado,
porem melhorados e originais. Nunca copie um titulo existente.

JSON:
{{"padroes":["..."],
  "palavras_chave":["..."],
  "diferencial_alta_performance":"...",
  "titulos_propostos":["..."]}}

Titulos analisados:
{titulos}"""


@dataclass
class VideoEncontrado:
    video_id: str
    titulo: str
    canal: str
    views: int
    publicado_em: datetime

    @property
    def dias(self) -> float:
        delta = datetime.now(timezone.utc) - self.publicado_em
        return max(delta.total_seconds() / 86400, 1.0)

    @property
    def views_por_dia(self) -> float:
        """Normaliza pela idade.

        Views absolutas premiam video antigo; views/dia mostra o que esta
        performando agora — que e o sinal util para canal novo.
        """
        return self.views / self.dias


def buscar(
    cfg: Config, termo: str, limite: int = 25, dias_max: int = 365
) -> list[VideoEncontrado]:
    """Busca videos do subnicho na regiao e idioma do canal."""
    from .youtube import _servico

    yt = _servico(cfg)
    regiao = cfg.canal.idioma.split("-")[0].upper()
    # Mapeia idioma -> regiao quando diferem (id = Indonesia).
    regiao = {"ID": "ID", "PT": "BR", "EN": "US"}.get(regiao, regiao)

    publicado_apos = (
        (datetime.now(timezone.utc) - timedelta(days=dias_max))
        .isoformat()
        .replace("+00:00", "Z")
    )

    resp = (
        yt.search()
        .list(
            part="snippet",
            q=termo,
            type="video",
            maxResults=min(limite, 50),
            order="viewCount",
            relevanceLanguage=cfg.canal.idioma,
            regionCode=regiao,
            publishedAfter=publicado_apos,
        )
        .execute()
    )

    ids = [item["id"]["videoId"] for item in resp.get("items", [])]
    if not ids:
        return []

    # search.list nao traz estatisticas; videos.list completa com 1 unidade.
    detalhes = (
        yt.videos().list(part="snippet,statistics", id=",".join(ids)).execute()
    )

    encontrados = []
    for item in detalhes.get("items", []):
        snip, stats = item["snippet"], item.get("statistics", {})
        encontrados.append(
            VideoEncontrado(
                video_id=item["id"],
                titulo=snip["title"],
                canal=snip["channelTitle"],
                views=int(stats.get("viewCount", 0)),
                publicado_em=datetime.fromisoformat(
                    snip["publishedAt"].replace("Z", "+00:00")
                ),
            )
        )

    encontrados.sort(key=lambda v: v.views_por_dia, reverse=True)
    return encontrados


def palavras_frequentes(videos: list[VideoEncontrado], top: int = 20) -> list[tuple[str, int]]:
    """Frequencia de palavras nos titulos, ponderada por performance.

    Titulos com mais views/dia contam mais: a palavra que aparece no video que
    esta performando vale mais que a que aparece no que nao performou.
    """
    if not videos:
        return []

    teto = max(v.views_por_dia for v in videos) or 1.0
    contador: Counter[str] = Counter()

    for v in videos:
        peso = max(int(v.views_por_dia / teto * 10), 1)
        for palavra in re.findall(r"\w+", v.titulo.lower()):
            if len(palavra) > 2 and palavra not in VAZIAS and not palavra.isdigit():
                contador[palavra] += peso

    return contador.most_common(top)


def extrair_padroes(llm: LLM, cfg: Config, videos: list[VideoEncontrado]) -> dict:
    """Pede ao LLM os padroes estruturais e propostas de titulo."""
    from .roteiro import _json_do_llm

    linhas = "\n".join(
        f"- [{v.views:,} views | {v.views_por_dia:,.0f}/dia] {v.titulo}"
        for v in videos[:30]
    )
    return _json_do_llm(
        llm.completar(
            EXTRAIR_PADROES_PROMPT.format(
                idioma=cfg.canal.idioma,
                destino=cfg.canal.idioma_revisao,
                titulos=linhas,
            ),
            max_tokens=4096,
        )
    )
