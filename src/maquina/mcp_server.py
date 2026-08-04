#!/usr/bin/env python3
"""Servidor MCP da maquina de video.

Expoe o motor que ja existe (pesquisa, diagnostico, producao, publicacao) como
ferramentas conversacionais. O objetivo e o operador perguntar em linguagem
natural — "qual video teve pior retencao?" — em vez de decorar comandos.

Transporte stdio: e uma ferramenta local, de um usuario so, rodando na maquina
do operador com as credenciais dele. Nao ha terceiro no meio e nada e exposto
na rede.

Nota sobre async: o motor por baixo e sincrono (googleapiclient, ffmpeg). Todo
trabalho bloqueante vai para uma thread via asyncio.to_thread, senao o event
loop trava durante um render de varios minutos.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from enum import Enum
from typing import Any, Callable

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import Config
from .models import Formato, Ideia, Status
from .pipeline import Pipeline

# stdio: log em stderr. Escrever em stdout corromperia o protocolo.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log = logging.getLogger("maquina.mcp")

mcp = MCPServer("maquina_mcp")

MAX_ITENS = 50


class FormatoResposta(str, Enum):
    """Formato de saida das ferramentas."""

    MARKDOWN = "markdown"
    JSON = "json"


def _anotacoes(
    titulo: str,
    *,
    leitura: bool = True,
    destrutivo: bool = False,
    idempotente: bool = True,
    mundo_aberto: bool = True,
) -> ToolAnnotations:
    """Anotacoes da ferramenta, com os defaults seguros deste projeto."""
    return ToolAnnotations(
        title=titulo,
        read_only_hint=leitura,
        destructive_hint=destrutivo,
        idempotent_hint=idempotente,
        open_world_hint=mundo_aberto,
    )


# --------------------------------------------------------------------------
# Utilitarios compartilhados
# --------------------------------------------------------------------------


def _pipeline() -> Pipeline:
    return Pipeline(Config.load())


async def _em_thread(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Roda trabalho bloqueante fora do event loop."""
    return await asyncio.to_thread(fn, *args, **kwargs)


def _erro(e: Exception) -> str:
    """Mensagem de erro acionavel: diz o que fazer, nao so o que falhou."""
    texto = str(e)

    if "credencial" in texto.lower() or "youtube_token" in texto:
        return (
            "Erro: sem credencial do YouTube. Rode `maquina auth-youtube` uma vez "
            "na sua maquina para autorizar a conta. Confirme que esta selecionando "
            "o canal correto (@SetiapLevelID) na tela do Google."
        )
    if "ANTHROPIC_API_KEY" in texto or "OPENAI_API_KEY" in texto:
        return (
            f"Erro: chave de API ausente ({texto}). Preencha o .env a partir do "
            ".env.example, ou use MAQ_LLM_PROVIDER=stub para rodar offline."
        )
    if any(k in texto for k in ("FISH_AUDIO_API_KEY", "ELEVENLABS_API_KEY")) or "voice_id" in texto.lower():
        return (
            "Erro: narracao nao configurada. Para o Fish Audio (onde a voz do "
            "operador ja esta clonada), preencha FISH_AUDIO_API_KEY — gere uma "
            "chave NOVA, a anterior vazou e deve ser revogada. O MAQ_TTS_VOICE_ID "
            "e o id do modelo em fish.audio/m/<id>."
        )
    if "quota" in texto.lower() or "quotaExceeded" in texto:
        return (
            "Erro: cota da YouTube API esgotada (10.000 unidades/dia; uma busca "
            "custa 100 e um upload ~1.600). Aguarde a renovacao ou peca aumento "
            "no Google Cloud Console."
        )
    if "nao encontrado" in texto.lower():
        return f"Erro: {texto}. Use maquina_listar_videos para ver os slugs disponiveis."

    log.exception("falha na ferramenta MCP")
    return f"Erro: {type(e).__name__}: {texto}"


def _nao_encontrado(slug: str, detalhe: str = "") -> str:
    """Erro padrao de slug invalido — sempre aponta como descobrir os validos."""
    extra = f" {detalhe}" if detalhe else ""
    return (
        f"Erro: video '{slug}' nao encontrado.{extra} "
        "Use maquina_listar_videos para ver os slugs disponiveis."
    )


def _formatar(dados: dict, formato: FormatoResposta, titulo: str, linhas: list[str]) -> str:
    """Serializa em JSON ou monta o markdown ja preparado pelo chamador."""
    if formato is FormatoResposta.JSON:
        return json.dumps(dados, indent=2, ensure_ascii=False, default=str)
    return "\n".join([f"# {titulo}", "", *linhas])


# --------------------------------------------------------------------------
# Modelos de entrada
# --------------------------------------------------------------------------


class PesquisaInput(BaseModel):
    """Entrada da pesquisa de subnicho."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    termo: str = Field(
        ...,
        description="Termo de busca no idioma do canal (ex.: 'cara mengatur keuangan')",
        min_length=2,
        max_length=200,
    )
    limite: int = Field(
        default=25, description="Quantos videos analisar (1-50)", ge=1, le=50
    )
    formato_resposta: FormatoResposta = FormatoResposta.MARKDOWN

    @field_validator("termo")
    @classmethod
    def termo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("termo nao pode ser vazio")
        return v.strip()


class ListarInput(BaseModel):
    """Entrada da listagem de videos."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    status: str | None = Field(
        default=None,
        description=(
            "Filtra por status: ideia, roteirizado, narrado, ilustrado, "
            "renderizado, aguardando_revisao, publicado, rejeitado, erro"
        ),
    )
    limite: int = Field(default=20, description="Maximo de itens (1-50)", ge=1, le=MAX_ITENS)
    offset: int = Field(default=0, description="Quantos pular (paginacao)", ge=0)
    formato_resposta: FormatoResposta = FormatoResposta.MARKDOWN


class SlugInput(BaseModel):
    """Entrada para operacoes sobre um video ja existente."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    slug: str = Field(
        ..., description="Identificador do video (veja em maquina_listar_videos)",
        min_length=1, max_length=200,
    )
    formato_resposta: FormatoResposta = FormatoResposta.MARKDOWN


class ComentariosInput(SlugInput):
    """Entrada da leitura de comentarios."""

    limite: int = Field(default=50, description="Comentarios a analisar", ge=1, le=100)


class IdeiasInput(BaseModel):
    """Entrada da geracao de pautas."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    formato: Formato = Field(
        default=Formato.LONGO, description="'longo' (16:9) ou 'shorts' (9:16)"
    )
    quantidade: int = Field(default=5, description="Quantas pautas gerar", ge=1, le=10)
    formato_resposta: FormatoResposta = FormatoResposta.MARKDOWN


class ProduzirInput(BaseModel):
    """Entrada da producao de video."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    titulo: str = Field(..., description="Titulo da pauta", min_length=3, max_length=300)
    angulo: str = Field(default="", description="Angulo editorial (opcional)", max_length=500)
    formato: Formato = Field(default=Formato.LONGO, description="'longo' ou 'shorts'")


class PublicarInput(BaseModel):
    """Entrada da publicacao. Exige confirmacao explicita."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    slug: str = Field(..., description="Identificador do video renderizado", min_length=1)
    confirmar: bool = Field(
        default=False,
        description=(
            "OBRIGATORIO true para publicar de fato. Existe para impedir que uma "
            "mencao casual na conversa suba video no canal."
        ),
    )
    em_horas: int = Field(
        default=3, description="Agendar para daqui a N horas (0 = imediato)", ge=0, le=720
    )
    privacidade: str = Field(
        default="public", description="'public', 'unlisted' ou 'private'"
    )

    @field_validator("privacidade")
    @classmethod
    def privacidade_valida(cls, v: str) -> str:
        if v not in {"public", "unlisted", "private"}:
            raise ValueError("privacidade deve ser public, unlisted ou private")
        return v


# --------------------------------------------------------------------------
# Ferramentas — leitura e analise
# --------------------------------------------------------------------------


@mcp.tool(
    name="maquina_status",
    annotations=_anotacoes("Status da maquina", mundo_aberto=False),
)
async def maquina_status() -> str:
    """Mostra a configuracao do canal, providers ativos e o que falta configurar.

    Use como primeiro diagnostico quando algo falhar, ou para confirmar se as
    credenciais estao ligadas antes de produzir. Providers marcados como "stub"
    rodam offline e produzem conteudo de teste, nao publicavel.

    Returns:
        str: JSON com o schema:
        {
          "canal": {"nome": str, "handle": str, "idioma": str},
          "providers": {"llm": str, "tts": str, "imagem": str},
          "providers_reais": bool,   # false = rodando em modo offline/teste
          "youtube_autenticado": bool,
          "limites": {"max_por_dia": int, "exigir_revisao": bool},
          "pendencias": [str]        # o que falta para produzir de verdade
        }
    """
    try:
        cfg = Config.load()
        p = await _em_thread(_pipeline)

        nomes = {
            "llm": type(p.llm).__name__,
            "tts": type(p.tts).__name__,
            "imagem": type(p.imagem).__name__,
        }
        reais = not any("Stub" in n for n in nomes.values())
        yt_ok = cfg.yt_token.exists()

        pendencias: list[str] = []
        if "Stub" in nomes["llm"]:
            pendencias.append("ANTHROPIC_API_KEY ausente — roteiros serao de teste")
        if "Stub" in nomes["tts"]:
            pendencias.append(
                "TTS sem credencial (FISH_AUDIO_API_KEY) — narracao sera silencio. "
                "Revogue a chave vazada do Fish e gere outra antes de preencher."
            )
        if "Stub" in nomes["imagem"]:
            pendencias.append("OPENAI_API_KEY ausente — imagens serao placeholders")
        if not yt_ok:
            pendencias.append("YouTube nao autorizado — rode `maquina auth-youtube`")
        if not cfg.canal.referencias_titulo:
            pendencias.append(
                "referencias_titulo vazio — rode maquina_pesquisar_subnicho para "
                "alimentar o pilar 1 (titulo)"
            )

        return json.dumps(
            {
                "canal": {
                    "nome": cfg.canal.nome,
                    "handle": cfg.canal.handle,
                    "idioma": cfg.canal.idioma,
                },
                "providers": nomes,
                "providers_reais": reais,
                "youtube_autenticado": yt_ok,
                "limites": {
                    "max_por_dia": cfg.publicacao.max_por_dia,
                    "exigir_revisao": cfg.publicacao.exigir_revisao,
                },
                "pendencias": pendencias,
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_listar_videos",
    annotations=_anotacoes("Listar videos", mundo_aberto=False),
)
async def maquina_listar_videos(params: ListarInput) -> str:
    """Lista os videos da maquina e em que etapa cada um esta.

    Use para descobrir o `slug` de um video antes de chamar as ferramentas que
    operam sobre um video especifico (diagnosticar, publicar, ler comentarios).

    Args:
        params (ListarInput):
            - status (str | None): filtro por etapa
            - limite (int): maximo de itens, 1-50 (padrao 20)
            - offset (int): quantos pular, para paginacao
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON com o schema:
        {
          "count": int, "offset": int, "has_more": bool, "next_offset": int | null,
          "videos": [{"slug": str, "status": str, "formato": str,
                      "titulo": str, "youtube_id": str | null,
                      "duracao_s": float | null, "custo_usd": float}]
        }
        Ou markdown equivalente.

    Examples:
        - "quais videos estao prontos?" -> status='renderizado'
        - "o que ja foi publicado?" -> status='publicado'
        - "deu erro em algum?" -> status='erro'
    """
    try:
        filtro = Status(params.status) if params.status else None
    except ValueError:
        validos = ", ".join(s.value for s in Status)
        return f"Erro: status '{params.status}' invalido. Use um de: {validos}"

    try:
        p = await _em_thread(_pipeline)
        # Busca offset+limite+1 para saber se ha proxima pagina.
        todos = await _em_thread(
            p.store.listar, filtro, params.offset + params.limite + 1
        )
        janela = todos[params.offset : params.offset + params.limite]
        tem_mais = len(todos) > params.offset + params.limite

        itens = [
            {
                "slug": v.slug,
                "status": v.status.value,
                "formato": v.formato.value,
                "titulo": (v.roteiro.titulo if v.roteiro else v.ideia.titulo if v.ideia else ""),
                "youtube_id": v.youtube_id,
                "duracao_s": v.duracao_s,
                "custo_usd": round(v.custo_usd, 4),
            }
            for v in janela
        ]

        dados = {
            "count": len(itens),
            "offset": params.offset,
            "has_more": tem_mais,
            "next_offset": params.offset + len(itens) if tem_mais else None,
            "videos": itens,
        }

        if not itens:
            return "Nenhum video encontrado. Use maquina_produzir_video para criar o primeiro."

        linhas = [
            f"- **{i['titulo'] or i['slug']}** (`{i['slug']}`) — {i['status']}"
            + (f", {i['duracao_s']:.0f}s" if i["duracao_s"] else "")
            + (f", https://youtu.be/{i['youtube_id']}" if i["youtube_id"] else "")
            for i in itens
        ]
        if tem_mais:
            linhas.append(f"\n_Mais resultados: offset={dados['next_offset']}_")

        return _formatar(dados, params.formato_resposta, "Videos", linhas)
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_pesquisar_subnicho",
    annotations=_anotacoes("Pesquisar subnicho no YouTube"),
)
async def maquina_pesquisar_subnicho(params: PesquisaInput) -> str:
    """Descobre quais titulos ja performam no subnicho, para alimentar o pilar 1.

    Busca pela API oficial do YouTube e ordena por **views/dia**, nao por views
    absolutas: video antigo acumula views e parece vencedor mesmo tendo parado
    de performar. Para canal novo, o sinal util e o que entrega agora.

    Custo de cota: ~100 unidades por chamada (teto diario de 10.000). Nao chame
    em loop.

    Args:
        params (PesquisaInput):
            - termo (str): busca no idioma do canal
            - limite (int): videos a analisar, 1-50 (padrao 25)
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON com o schema:
        {
          "termo": str, "count": int,
          "videos": [{"titulo": str, "canal": str, "views": int,
                      "views_por_dia": float, "video_id": str}],
          "palavras_chave": [[str, int]],        # palavra, peso por performance
          "padroes": [str],                      # estruturas recorrentes
          "diferencial_alta_performance": str,
          "titulos_propostos": [str]             # 10 titulos novos sugeridos
        }

    Examples:
        - "pesquisa o que funciona sobre financas pessoais" -> termo no idioma do canal
        - Don't use when: voce quer as metricas do SEU canal (use maquina_diagnosticar_video)
    """
    try:
        from .providers import obter_llm
        from .stages.pesquisa import buscar, extrair_padroes, palavras_frequentes

        cfg = Config.load()
        videos = await _em_thread(buscar, cfg, params.termo, params.limite)
        if not videos:
            return (
                f"Nenhum video encontrado para '{params.termo}'. Tente um termo mais "
                f"amplo, no idioma do canal ({cfg.canal.idioma})."
            )

        frequentes = palavras_frequentes(videos)
        analise = await _em_thread(extrair_padroes, obter_llm(cfg), cfg, videos)

        dados = {
            "termo": params.termo,
            "count": len(videos),
            "videos": [
                {
                    "titulo": v.titulo,
                    "canal": v.canal,
                    "views": v.views,
                    "views_por_dia": round(v.views_por_dia, 1),
                    "video_id": v.video_id,
                }
                for v in videos
            ],
            "palavras_chave": frequentes,
            "padroes": analise.get("padroes", []),
            "diferencial_alta_performance": analise.get("diferencial_alta_performance", ""),
            "titulos_propostos": analise.get("titulos_propostos", []),
        }

        linhas = [f"**{len(videos)} videos analisados**, ordenados por views/dia.", ""]
        linhas += [
            f"- [{v.views:,} views | {v.views_por_dia:,.0f}/dia] {v.titulo} — _{v.canal}_"
            for v in videos[:10]
        ]
        linhas += ["", "## Palavras-chave (ponderadas por performance)",
                   ", ".join(p for p, _ in frequentes)]
        if padroes := analise.get("padroes"):
            linhas += ["", "## Padroes estruturais"] + [f"- {x}" for x in padroes]
        if dif := analise.get("diferencial_alta_performance"):
            linhas += ["", "## O que separa os que performam", dif]
        if propostos := analise.get("titulos_propostos"):
            linhas += ["", "## Titulos propostos"] + [f"- {x}" for x in propostos]

        return _formatar(dados, params.formato_resposta, f"Subnicho: {params.termo}", linhas)
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_diagnosticar_video",
    annotations=_anotacoes("Diagnosticar os 3 pilares"),
)
async def maquina_diagnosticar_video(params: SlugInput) -> str:
    """Aponta qual dos 3 pilares (titulo, thumbnail, roteiro) e o gargalo do video.

    Cruza CTR e retencao para nomear a causa, em vez de deixar voce interpretar
    grafico: CTR alto com retencao baixa significa problema de ROTEIRO — a capa
    entregou o clique e o video nao segurou. Refazer a thumbnail nesse caso e
    consertar a coisa errada.

    Abaixo de 500 impressoes devolve 'sem_dados' de proposito: amostra pequena
    leva a conclusao errada.

    Args:
        params (SlugInput):
            - slug (str): identificador do video (precisa estar publicado)
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON com o schema:
        {
          "slug": str, "titulo": str, "youtube_id": str,
          "gargalo": "titulo"|"thumbnail"|"roteiro"|"nenhum"|"sem_dados",
          "ctr": float, "retencao_media_pct": float,
          "resumo": str, "acoes": [str]
        }

    Examples:
        - "por que esse video nao foi pra frente?" -> slug do video
        - "qual o gargalo do ultimo video?" -> liste primeiro, depois diagnostique
    """
    try:
        p = await _em_thread(_pipeline)
        video = await _em_thread(p.store.obter, params.slug)
        if not video:
            return _nao_encontrado(params.slug)
        if not video.youtube_id:
            return (
                f"Erro: '{params.slug}' ainda nao foi publicado — nao ha metricas. "
                "Publique primeiro com maquina_publicar_video."
            )

        d = await _em_thread(p.diagnosticar, video)
        if not d:
            return "Erro: nao foi possivel coletar metricas."

        dados = {
            "slug": video.slug,
            "titulo": video.roteiro.titulo if video.roteiro else "",
            "youtube_id": video.youtube_id,
            "gargalo": d.gargalo.value,
            "ctr": round(d.ctr, 4),
            "retencao_media_pct": round(d.retencao, 2),
            "resumo": d.resumo,
            "acoes": d.acoes,
        }
        linhas = [
            f"**Gargalo: {d.gargalo.value.upper()}**", "",
            f"CTR {d.ctr:.1%} | Retencao {d.retencao:.1f}%", "",
            d.resumo, "",
        ]
        if d.acoes:
            linhas += ["## Acoes"] + [f"- {a}" for a in d.acoes]

        return _formatar(dados, params.formato_resposta, dados["titulo"] or video.slug, linhas)
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_ler_comentarios",
    annotations=_anotacoes("Ler comentarios traduzidos"),
)
async def maquina_ler_comentarios(params: ComentariosInput) -> str:
    """Le os comentarios do video, traduz e extrai sinais tecnicos acionaveis.

    Essencial em canal cujo idioma o operador nao le. Problemas como musica alta
    demais, voz artificial ou ritmo ruim aparecem nos comentarios ANTES de
    aparecerem na curva de retencao — e sem traducao esse canal de feedback
    simplesmente nao existe.

    Args:
        params (ComentariosInput):
            - slug (str): identificador do video publicado
            - limite (int): comentarios a analisar, 1-100 (padrao 50)
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON com o schema:
        {
          "slug": str, "total_comentarios": int,
          "sentimento": "positivo"|"misto"|"negativo",
          "resumo": str,
          "sinais_tecnicos": [str],
          "comentarios_relevantes": [{"original": str, "traducao": str}]
        }
    """
    try:
        from .providers import obter_llm
        from .stages.revisao import analisar_comentarios, buscar_comentarios

        cfg = Config.load()
        p = await _em_thread(_pipeline)
        video = await _em_thread(p.store.obter, params.slug)
        if not video:
            return _nao_encontrado(params.slug)
        if not video.youtube_id:
            return f"Erro: '{params.slug}' ainda nao foi publicado."

        brutos = await _em_thread(
            buscar_comentarios, cfg, video.youtube_id, params.limite
        )
        if not brutos:
            return "Ainda nao ha comentarios neste video."

        analise = await _em_thread(analisar_comentarios, obter_llm(cfg), cfg, brutos)
        if not analise:
            return "Nao foi possivel analisar os comentarios."

        dados = {"slug": video.slug, "total_comentarios": len(brutos), **analise}

        linhas = [
            f"**Sentimento:** {analise.get('sentimento', '?')} "
            f"({len(brutos)} comentarios)", "",
            analise.get("resumo", ""), "",
        ]
        if sinais := analise.get("sinais_tecnicos"):
            linhas += ["## Sinais tecnicos acionaveis"] + [f"- {s}" for s in sinais]
        if relevantes := analise.get("comentarios_relevantes"):
            linhas += ["", "## Comentarios"] + [
                f"- {c.get('traducao', '')}" for c in relevantes[:10]
            ]

        return _formatar(dados, params.formato_resposta, "Comentarios", linhas)
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_revisar_roteiro",
    annotations=_anotacoes("Revisar roteiro traduzido"),
)
async def maquina_revisar_roteiro(params: SlugInput) -> str:
    """Traduz o roteiro para o idioma do operador e avalia se soa natural.

    Sem isto, aprovar um roteiro em idioma que voce nao le e um carimbo. A
    avaliacao de naturalidade indica se um falante nativo diria aquilo — texto
    'artificial' costuma anteceder retencao ruim.

    Args:
        params (SlugInput):
            - slug (str): identificador do video
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON com o schema:
        {
          "slug": str, "titulo": str,
          "naturalidade": "natural"|"aceitavel"|"artificial",
          "observacao": str, "traducao": str
        }
    """
    try:
        from .providers import obter_llm
        from .stages.revisao import revisar_roteiro

        cfg = Config.load()
        p = await _em_thread(_pipeline)
        video = await _em_thread(p.store.obter, params.slug)
        if not video or not video.roteiro:
            return _nao_encontrado(params.slug, "Ou ele ainda nao tem roteiro.")

        r = await _em_thread(revisar_roteiro, obter_llm(cfg), cfg, video.roteiro)
        dados = {
            "slug": video.slug,
            "titulo": video.roteiro.titulo,
            "naturalidade": r.get("naturalidade", ""),
            "observacao": r.get("observacao", ""),
            "traducao": r.get("traducao", ""),
        }
        linhas = [
            f"**Naturalidade:** {dados['naturalidade']}",
            f"**Observacao:** {dados['observacao']}", "",
            "## Traducao", dados["traducao"],
        ]
        return _formatar(dados, params.formato_resposta, dados["titulo"], linhas)
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_gerar_ideias",
    annotations=_anotacoes("Gerar pautas", idempotente=False),
)
async def maquina_gerar_ideias(params: IdeiasInput) -> str:
    """Gera pautas candidatas, sem produzir nada.

    Aplica o eixo tematico da rodada (rotacao automatica) para forcar variacao
    estrutural entre videos publicados em sequencia, e evita repetir temas ja
    publicados no canal.

    Args:
        params (IdeiasInput):
            - formato (Formato): 'longo' ou 'shorts'
            - quantidade (int): pautas a gerar, 1-10 (padrao 5)
            - formato_resposta: 'markdown' ou 'json'

    Returns:
        str: JSON: {"formato": str, "eixo": str,
                    "ideias": [{"titulo": str, "angulo": str,
                                "palavras_chave": [str]}]}
    """
    try:
        from .stages.roteiro import proximo_eixo

        cfg = Config.load()
        p = await _em_thread(_pipeline)
        publicados = await _em_thread(p.store.titulos_publicados)
        ideias = await _em_thread(p.ideias, params.formato, params.quantidade)

        dados = {
            "formato": params.formato.value,
            "eixo": proximo_eixo(cfg, len(publicados)),
            "ideias": [
                {"titulo": i.titulo, "angulo": i.angulo, "palavras_chave": i.palavras_chave}
                for i in ideias
            ],
        }
        linhas = [f"_Eixo desta rodada: {dados['eixo']}_", ""] + [
            f"{n}. **{i.titulo}**\n   {i.angulo}" for n, i in enumerate(ideias, 1)
        ]
        return _formatar(dados, params.formato_resposta, "Pautas", linhas)
    except Exception as e:
        return _erro(e)


# --------------------------------------------------------------------------
# Ferramentas — escrita
# --------------------------------------------------------------------------


@mcp.tool(
    name="maquina_produzir_video",
    annotations=_anotacoes("Produzir video (nao publica)", leitura=False, idempotente=False),
)
async def maquina_produzir_video(params: ProduzirInput) -> str:
    """Produz um video completo, da pauta ao MP4. NAO publica.

    Executa roteiro, narracao, imagens, legendas, render e thumbnail. Demora
    varios minutos e consome credito de API (~US$ 2,70 num video longo).

    O arquivo fica local para revisao. Publicar e um passo separado e explicito
    (maquina_publicar_video) — a revisao humana e o que separa este projeto de
    uma fabrica de conteudo em massa.

    Args:
        params (ProduzirInput):
            - titulo (str): titulo da pauta
            - angulo (str): angulo editorial, opcional
            - formato (Formato): 'longo' (16:9) ou 'shorts' (9:16)

    Returns:
        str: JSON: {"slug": str, "status": str, "video_path": str,
                    "thumbnail_path": str, "duracao_s": float,
                    "custo_usd": float, "proximo_passo": str}
    """
    try:
        p = await _em_thread(_pipeline)
        ideia = Ideia(titulo=params.titulo, angulo=params.angulo, formato=params.formato)
        video = await _em_thread(p.produzir, ideia)

        return json.dumps(
            {
                "slug": video.slug,
                "status": video.status.value,
                "video_path": video.video_path,
                "thumbnail_path": video.thumbnail_path,
                "duracao_s": round(video.duracao_s or 0, 1),
                "custo_usd": round(video.custo_usd, 4),
                "proximo_passo": (
                    "Assista o video e rode maquina_revisar_roteiro antes de publicar."
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return _erro(e)


@mcp.tool(
    name="maquina_publicar_video",
    annotations=_anotacoes("Publicar no YouTube", leitura=False, destrutivo=True, idempotente=False),
)
async def maquina_publicar_video(params: PublicarInput) -> str:
    """Publica um video ja renderizado no canal. Acao publica e dificil de desfazer.

    Roda antes as checagens de compliance: teto diario, similaridade de roteiro
    contra os ultimos publicados, titulo duplicado, e divulgacao de conteudo
    sintetico. Se qualquer uma bloquear, nada e publicado.

    Exige `confirmar=true`. Sem isso apenas simula e mostra o que aconteceria —
    protecao para que uma mencao casual na conversa nao suba video no canal.

    Args:
        params (PublicarInput):
            - slug (str): identificador do video renderizado
            - confirmar (bool): OBRIGATORIO true para publicar de fato
            - em_horas (int): agendar para daqui a N horas, 0 = imediato (padrao 3)
            - privacidade (str): 'public', 'unlisted' ou 'private'

    Returns:
        str: JSON. Sem confirmacao:
        {"simulacao": true, "aprovado": bool, "bloqueios": [str],
         "alertas": [str], "titulo": str, "para_publicar": str}
        Com confirmacao:
        {"publicado": true, "youtube_id": str, "url": str, "agendado_para": str|null}
    """
    try:
        from datetime import datetime, timedelta
        from pathlib import Path

        p = await _em_thread(_pipeline)
        video = await _em_thread(p.store.obter, params.slug)
        if not video:
            return _nao_encontrado(params.slug)
        if not video.video_path or not Path(video.video_path).exists():
            return f"Erro: '{params.slug}' ainda nao foi renderizado."

        res = await _em_thread(p.verificar, video)

        if not params.confirmar:
            return json.dumps(
                {
                    "simulacao": True,
                    "aprovado": res.aprovado,
                    "bloqueios": res.bloqueios,
                    "alertas": res.alertas,
                    "titulo": video.roteiro.titulo if video.roteiro else "",
                    "duracao_s": round(video.duracao_s or 0, 1),
                    "para_publicar": (
                        "Chame de novo com confirmar=true. Assista o video antes."
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )

        if not res.aprovado:
            return json.dumps(
                {
                    "publicado": False,
                    "bloqueios": res.bloqueios,
                    "motivo": (
                        "Checagens de compliance bloquearam a publicacao. "
                        "Ver docs/03-compliance-monetizacao.md"
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )

        quando = (
            datetime.now().astimezone() + timedelta(hours=params.em_horas)
            if params.em_horas
            else None
        )
        video = await _em_thread(
            p.publicar, video, agendar_para=quando, privacidade=params.privacidade
        )

        return json.dumps(
            {
                "publicado": True,
                "youtube_id": video.youtube_id,
                "url": f"https://youtu.be/{video.youtube_id}",
                "agendado_para": quando.isoformat() if quando else None,
                "alertas": res.alertas,
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return _erro(e)


def main() -> None:
    """Entry point do servidor MCP (transporte stdio)."""
    mcp.run()


if __name__ == "__main__":
    main()
