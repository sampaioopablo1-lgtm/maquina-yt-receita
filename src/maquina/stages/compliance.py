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

    # 1. Teto diario DO CANAL — automacao em escala com variacao minima e
    # tratada como spam. Conta so este canal, porque o SQLite e por canal.
    publicados = store.publicados_hoje()
    if publicados >= cfg.publicacao.max_por_dia:
        r.bloquear(
            f"teto diario do canal atingido ({publicados}/{cfg.publicacao.max_por_dia}). "
            "Ver docs/03-compliance-monetizacao.md"
        )

    # 1b. Teto diario DA CONTA — este e cota de verdade, e ate 2026-08-12 nao
    # era checado em lugar nenhum. Os 13 canais publicam pelo mesmo projeto do
    # Google Cloud, e videos.insert da 100 chamadas/dia POR PROJETO. Sem esta
    # soma, treze canais gastariam treze tetos e o estouro apareceria so como
    # quotaExceeded no meio de um upload, com o pacote ja renderizado.
    da_conta = store.publicados_hoje_conta()
    if da_conta >= cfg.publicacao.max_conta_por_dia:
        r.bloquear(
            f"cota diaria da conta atingida ({da_conta}/{cfg.publicacao.max_conta_por_dia} "
            "uploads em todos os canais). videos.insert reabre as 00:00 UTC."
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
    if video.formato is Formato.LONGO and video.duracao_s and video.duracao_s < 8 * 60:
        r.alertar(
            f"duracao {video.duracao_s / 60:.1f} min < 8 min — "
            "sem multiplos blocos de anuncio"
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
