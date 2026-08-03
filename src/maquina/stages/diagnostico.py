"""Diagnostico dos 3 pilares.

Converte o raciocinio manual de "olhar o grafico do Studio" em uma regra. A
combinacao de CTR e retencao identifica qual dos tres pilares e o gargalo — que
e a diferenca entre ajustar a coisa certa e refazer thumbnail quando o problema
era o roteiro.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..config import Config
from ..models import Metricas


class Gargalo(str, Enum):
    TITULO = "titulo"
    THUMBNAIL = "thumbnail"
    ROTEIRO = "roteiro"
    NENHUM = "nenhum"
    SEM_DADOS = "sem_dados"


@dataclass
class Diagnostico:
    gargalo: Gargalo
    resumo: str
    acoes: list[str]
    ctr: float
    retencao: float

    def __str__(self) -> str:
        linhas = [
            f"Gargalo: {self.gargalo.value.upper()}",
            f"CTR {self.ctr:.1%} | Retencao {self.retencao:.1f}%",
            "",
            self.resumo,
        ]
        if self.acoes:
            linhas += ["", "Acoes:"] + [f"  - {a}" for a in self.acoes]
        return "\n".join(linhas)


# Volume minimo de impressoes para o CTR significar algo.
MIN_IMPRESSOES = 500


def diagnosticar(m: Metricas, cfg: Config) -> Diagnostico:
    ctr_ok = m.ctr >= cfg.metas.ctr_min
    ret_ok = m.retencao_media_pct >= cfg.metas.retencao_min_pct

    if m.impressoes < MIN_IMPRESSOES:
        return Diagnostico(
            gargalo=Gargalo.SEM_DADOS,
            resumo=(
                f"Apenas {m.impressoes} impressoes — amostra insuficiente. "
                "Aguarde antes de concluir qualquer coisa; nao refaca nada ainda."
            ),
            acoes=["Reavaliar em 7 dias ou ao passar de 500 impressoes"],
            ctr=m.ctr,
            retencao=m.retencao_media_pct,
        )

    if ctr_ok and ret_ok:
        return Diagnostico(
            gargalo=Gargalo.NENHUM,
            resumo="Os tres pilares alinhados. Este e o padrao a repetir.",
            acoes=[
                "Registrar o padrao de titulo e thumbnail como referencia do canal",
                "Produzir variacoes do mesmo tema — o publico ja respondeu",
            ],
            ctr=m.ctr,
            retencao=m.retencao_media_pct,
        )

    if ctr_ok and not ret_ok:
        return Diagnostico(
            gargalo=Gargalo.ROTEIRO,
            resumo=(
                f"CTR bom ({m.ctr:.1%}) e retencao baixa "
                f"({m.retencao_media_pct:.1f}% vs meta {cfg.metas.retencao_min_pct:.0f}%). "
                "A thumbnail entregou o clique e o video nao segurou. "
                "O problema esta no conteudo, nao na capa — nao refaca a thumbnail."
            ),
            acoes=[
                "Revisar os primeiros 30s: o gancho precisa entregar o que o titulo promete",
                "Conferir o volume da trilha — musica alta e causa recorrente de abandono",
                "Verificar consistencia da voz ao longo do video",
                "Ler os comentarios: o diagnostico costuma estar escrito la",
                "Cortar blocos de baixa densidade de informacao",
            ],
            ctr=m.ctr,
            retencao=m.retencao_media_pct,
        )

    if not ctr_ok and ret_ok:
        return Diagnostico(
            gargalo=Gargalo.THUMBNAIL,
            resumo=(
                f"Retencao boa ({m.retencao_media_pct:.1f}%) e CTR baixo ({m.ctr:.1%}). "
                "Quem entra, fica — mas pouca gente entra. O conteudo esta certo; "
                "a capa nao esta convertendo a impressao em clique."
            ),
            acoes=[
                "Refazer a thumbnail com os 3 elementos: texto curto no topo (max 3 palavras), "
                "figura de autoridade centralizada, imagem que representa o titulo",
                "Aumentar contraste e tamanho da fonte — a maioria assiste no celular",
                "Testar uma segunda versao e comparar o CTR",
            ],
            ctr=m.ctr,
            retencao=m.retencao_media_pct,
        )

    return Diagnostico(
        gargalo=Gargalo.TITULO,
        resumo=(
            f"CTR ({m.ctr:.1%}) e retencao ({m.retencao_media_pct:.1f}%) abaixo da meta. "
            "Quando os dois falham juntos, normalmente o tema nao casa com a demanda "
            "do subnicho — a raiz esta na escolha de titulo/pauta."
        ),
        acoes=[
            "Rever as palavras-chave: partir de titulos ja validados no subnicho",
            "Confirmar que o tema tem demanda real antes de reeditar o video",
            "Nao insistir neste video — aplicar o aprendizado no proximo",
        ],
        ctr=m.ctr,
        retencao=m.retencao_media_pct,
    )
