"""Barreiras aplicadas ANTES do upload.

Estas checagens existem porque o modo de falha mais caro deste projeto nao e um
video ruim — e o canal perder monetizacao por conteudo repetitivo ou por spam de
automacao em escala. Ver docs/03-compliance-monetizacao.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

from ..config import Config
from ..models import Formato, Video
from ..storage import Store


@dataclass
class Resultado:
    aprovado: bool = True
    bloqueios: list[str] = field(default_factory=list)
    alertas: list[str] = field(default_factory=list)

    def bloquear(self, motivo: str) -> None:
        self.aprovado = False
        self.bloqueios.append(motivo)

    def alertar(self, motivo: str) -> None:
        self.alertas.append(motivo)


def _normalizar(texto: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", texto.lower())


def similaridade(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalizar(a), _normalizar(b)).ratio()


def verificar(video: Video, cfg: Config, store: Store) -> Resultado:
    r = Resultado()

    if not video.roteiro:
        r.bloquear("video sem roteiro")
        return r

    # 1. Teto diario DA CONTA. Apesar do SQLite morar em data/<slug>/, o
    # `maquina sincronizar` enche esse banco com a frota inteira, entao esta
    # contagem e dos treze canais somados — e o teto e a cota real de
    # videos.insert, 100/dia por projeto do Google Cloud.
    #
    publicados = store.publicados_hoje()
    if publicados >= cfg.publicacao.max_por_dia:
        r.bloquear(
            f"cota diaria da conta atingida ({publicados}/{cfg.publicacao.max_por_dia} "
            "uploads somando todos os canais). videos.insert reabre as 00:00 UTC. "
            "Ver docs/03-compliance-monetizacao.md"
        )

    # 1b. Teto POR CANAL — a guarda anti-spam de verdade. A cota da conta e de
    # 100/dia e nao protege canal nenhum: treze canais cabem nela publicando
    # sete vezes cada, que e exatamente o padrao que o YouTube le como spam.
    # So passou a ser possivel quando o Video ganhou campo `canal` (2026-08-12);
    # antes disso nao havia como separar um canal dos outros doze neste banco.
    canal = video.canal or cfg.canal_slug
    if canal:
        do_canal = store.publicados_hoje_canal(canal)
        if do_canal >= cfg.publicacao.max_por_canal_dia:
            r.bloquear(
                f"teto diario do canal {canal} atingido "
                f"({do_canal}/{cfg.publicacao.max_por_canal_dia} videos = "
                f"{cfg.publicacao.max_por_canal_dia // 2} pacotes). "
                "Automacao em escala com variacao minima e lida como spam."
            )

    # 2. Similaridade de roteiro contra o historico recente.
    limite = cfg.publicacao.similaridade_max
    for titulo, texto in store.roteiros_recentes(cfg.publicacao.janela_similaridade):
        if titulo == video.roteiro.titulo:
            continue
        s = similaridade(video.roteiro.texto_completo, texto)
        if s > limite:
            r.bloquear(f"roteiro {s:.0%} similar a '{titulo}' (limite {limite:.0%})")
            break

    # 3. Titulo duplicado ou quase identico.
    for titulo in store.titulos_publicados():
        if titulo == video.roteiro.titulo:
            continue
        if titulo and similaridade(video.roteiro.titulo, titulo) > 0.90:
            r.bloquear(f"titulo quase identico a '{titulo}'")
            break

    # 4. Duracao: abaixo de 8 min o formato longo perde blocos de anuncio.
    #
    # BLOQUEIA, nao alerta. Era alerta ate 2026-08-12, e alerta nao impede nada:
    # o cron de 4 em 4 horas do producao.yml roda `maquina auto --publicar` sem
    # ninguem olhando, e nesse dia publicou EtVxgh1x-Q4 com 226 s — tres minutos
    # e quarenta e seis — como formato longo, publico. A regra da rotina e
    # "NUNCA abaixo de 8 min"; um aviso que ninguem le nao e nunca.
    if video.formato is Formato.LONGO and video.duracao_s and video.duracao_s < 8 * 60:
        r.bloquear(
            f"duracao {video.duracao_s / 60:.1f} min < 8 min — longo abaixo do piso "
            "perde os blocos de anuncio do meio. Republique como shorts ou "
            "estenda o roteiro."
        )

    # 4b. Short fora da faixa de 30 a 45 s que a rotina pede.
    #
    # Acima de 60 s BLOQUEIA: o feed de Shorts e o unico que entrega em canal
    # frio — medido, 23,0 views/dia contra 0,1 do longo — e passar do minuto
    # arrisca sair dele. Entre 45 e 60 apenas alerta, porque ja esta publicado
    # e o estrago e de ritmo, nao de distribuicao.
    #
    # Abaixo de 20 s tambem bloqueia: nao cabe gancho, desenvolvimento e CTA
    # falado, e sem CTA o short nao converte em inscrito — que e a unica razao
    # de ele existir na estrategia.
    if video.formato is Formato.SHORTS and video.duracao_s:
        if video.duracao_s > 60:
            r.bloquear(
                f"short com {video.duracao_s:.0f} s — acima de 60 arrisca sair "
                "do feed de Shorts, que e o unico que entrega em canal frio. "
                "A rotina pede 30 a 45."
            )
        elif video.duracao_s < 20:
            r.bloquear(
                f"short com {video.duracao_s:.0f} s — curto demais para gancho, "
                "desenvolvimento e CTA falado. Sem CTA nao vira inscrito."
            )
        elif video.duracao_s > 45:
            r.alertar(
                f"short com {video.duracao_s:.0f} s, acima dos 45 que a rotina "
                "pede — ainda no feed, mas o ritmo afrouxa"
            )

    # 5. Metadados minimos.
    if len(video.roteiro.titulo) > 100:
        r.bloquear("titulo acima de 100 caracteres (limite do YouTube)")
    if not video.roteiro.descricao.strip():
        r.alertar("descricao vazia")
    if not video.thumbnail_path:
        r.alertar("sem thumbnail — CTR e o segundo pilar, nao publique sem ela")

    # 5b. Legenda: caption=false prejudica acessibilidade e ranking de pesquisa.
    if not video.legenda_path or not Path(video.legenda_path).exists():
        r.alertar(
            "sem legenda (.srt) — o video sera publicado com caption=false; "
            "gere legendas antes de publicar"
        )

    # 6. Divulgacao de conteudo sintetico: informativo, nao bloqueia.
    if video.conteudo_sintetico:
        r.alertar(
            "marcado como conteudo sintetico — flag de divulgacao sera enviada no upload"
        )

    return r
