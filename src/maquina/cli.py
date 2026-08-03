"""CLI da maquina."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config import Config
from .models import Formato, Ideia, Status
from .pipeline import Pipeline
from .storage import Store

app = typer.Typer(add_completion=False, help="Maquina de video para YouTube")
console = Console()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
)


def _cfg() -> Config:
    return Config.load()


@app.command()
def ideias(
    formato: Formato = typer.Option(Formato.LONGO, help="shorts ou longo"),
    n: int = typer.Option(5, help="quantas ideias gerar"),
):
    """Gera pautas candidatas para o canal."""
    p = Pipeline(_cfg())
    tabela = Table("#", "Titulo", "Angulo")
    for i, ideia in enumerate(p.ideias(formato, n), 1):
        tabela.add_row(str(i), ideia.titulo, ideia.angulo[:60])
    console.print(tabela)


@app.command()
def produzir(
    titulo: str = typer.Argument(..., help="Titulo da pauta"),
    angulo: str = typer.Option("", help="Angulo editorial"),
    formato: Formato = typer.Option(Formato.LONGO),
):
    """Produz um video da ideia ate o MP4 (nao publica)."""
    p = Pipeline(_cfg())
    video = p.produzir(Ideia(titulo=titulo, angulo=angulo, formato=formato))
    console.print(f"[green]OK[/] {video.video_path}")
    console.print(f"Duracao: {video.duracao_s:.1f}s | Custo: US$ {video.custo_usd:.4f}")
    console.print(f"Revise e publique: [bold]maquina publicar {video.slug}[/]")


@app.command()
def auto(
    formato: Formato = typer.Option(Formato.LONGO),
    publicar_apos: bool = typer.Option(False, "--publicar", help="publica se passar nas checagens"),
):
    """Ciclo completo: escolhe uma pauta nova, produz e (opcional) publica."""
    cfg = _cfg()
    p = Pipeline(cfg)

    lista = p.ideias(formato, 5)
    if not lista:
        console.print("[red]nenhuma ideia gerada[/]")
        raise typer.Exit(1)

    escolhida = lista[0]
    console.print(f"Pauta: [bold]{escolhida.titulo}[/]")
    video = p.produzir(escolhida)

    res = p.verificar(video)
    for a in res.alertas:
        console.print(f"[yellow]alerta:[/] {a}")
    if not res.aprovado:
        for b in res.bloqueios:
            console.print(f"[red]bloqueio:[/] {b}")
        raise typer.Exit(2)

    console.print(f"[green]Produzido:[/] {video.video_path}")

    if publicar_apos and not cfg.publicacao.exigir_revisao:
        quando = datetime.now().astimezone() + timedelta(hours=3)
        p.publicar(video, agendar_para=quando)
        console.print(f"[green]Agendado[/] para {quando:%d/%m %H:%M}")
    else:
        console.print("Aguardando revisao humana: [bold]maquina publicar "
                      f"{video.slug}[/]")


@app.command()
def publicar(
    slug: str,
    em_horas: int = typer.Option(3, help="agendar para daqui a N horas (0 = ja)"),
    privacidade: str = typer.Option("public", help="public, unlisted ou private"),
    sim: bool = typer.Option(False, "--yes", "-y", help="pula a confirmacao"),
):
    """Publica um video ja renderizado (com checagens de compliance)."""
    cfg = _cfg()
    p = Pipeline(cfg)
    video = p.store.obter(slug)
    if not video:
        console.print(f"[red]nao encontrei '{slug}'[/]")
        raise typer.Exit(1)
    if not video.video_path or not Path(video.video_path).exists():
        console.print("[red]video ainda nao renderizado[/]")
        raise typer.Exit(1)

    res = p.verificar(video)
    for a in res.alertas:
        console.print(f"[yellow]alerta:[/] {a}")
    if not res.aprovado:
        for b in res.bloqueios:
            console.print(f"[red]bloqueio:[/] {b}")
        raise typer.Exit(2)

    assert video.roteiro
    console.print(f"\n[bold]{video.roteiro.titulo}[/]")
    console.print(f"{video.duracao_s:.0f}s | {video.formato.value} | {video.video_path}")
    console.print(f"Thumbnail: {video.thumbnail_path}\n")

    if not sim and not typer.confirm("Publicar?"):
        raise typer.Exit(0)

    quando = datetime.now().astimezone() + timedelta(hours=em_horas) if em_horas else None
    p.publicar(video, agendar_para=quando, privacidade=privacidade)
    console.print(f"[green]https://youtu.be/{video.youtube_id}[/]")


@app.command()
def retomar(slug: str):
    """Continua um video interrompido, sem refazer o que ja existe."""
    p = Pipeline(_cfg())
    video = p.retomar(slug)
    console.print(f"[green]{video.status.value}[/] {video.video_path or ''}")


@app.command()
def listar(status: str = typer.Option("", help="filtra por status")):
    """Lista os videos e seus estados."""
    store = Store(_cfg().data_dir / "maquina.db")
    filtro = Status(status) if status else None
    tabela = Table("Slug", "Status", "Formato", "Titulo", "YouTube")
    for v in store.listar(filtro):
        titulo = v.roteiro.titulo if v.roteiro else (v.ideia.titulo if v.ideia else "-")
        tabela.add_row(v.slug, v.status.value, v.formato.value, titulo[:45], v.youtube_id or "-")
    console.print(tabela)


@app.command()
def diagnosticar(slug: str = typer.Argument("", help="vazio = todos os publicados")):
    """Aponta qual dos 3 pilares e o gargalo de cada video."""
    cfg = _cfg()
    p = Pipeline(cfg)
    videos = [p.store.obter(slug)] if slug else p.store.listar(Status.PUBLICADO)

    for v in filter(None, videos):
        if not v.youtube_id:
            continue
        console.rule(v.roteiro.titulo[:70] if v.roteiro else v.slug)
        try:
            if d := p.diagnosticar(v):
                console.print(str(d))
        except Exception as e:
            console.print(f"[red]erro ao coletar metricas: {e}[/]")


@app.command("auth-youtube")
def auth_youtube():
    """Autoriza a conta do YouTube (rodar uma vez, localmente)."""
    from .stages.youtube import autenticar

    cfg = _cfg()
    caminho = autenticar(cfg)
    console.print(f"[green]Token salvo em {caminho}[/]")
    console.print(
        "\nPara o GitHub Actions: copie o conteudo deste arquivo para o secret "
        "[bold]YT_TOKEN_JSON[/]."
    )


@app.command("voice-clone")
def voice_clone(
    amostras: list[Path] = typer.Argument(..., help="arquivos de audio da sua voz"),
    nome: str = typer.Option("", help="nome da voz (padrao: nome do canal)"),
):
    """Registra sua voz no ElevenLabs e devolve o voice_id."""
    from .providers.reais import TTSElevenLabs

    cfg = _cfg()
    faltando = [p for p in amostras if not p.exists()]
    if faltando:
        console.print(f"[red]nao encontrei: {', '.join(map(str, faltando))}[/]")
        raise typer.Exit(1)

    tts = TTSElevenLabs(cfg.tts_model, cfg.tts_voice_id)
    voice_id = tts.clonar_voz(nome or cfg.canal.nome, amostras)
    console.print(f"[green]voice_id:[/] {voice_id}")
    console.print(f"Adicione ao .env: [bold]MAQ_TTS_VOICE_ID={voice_id}[/]")


@app.command()
def pesquisar(
    termo: str = typer.Argument(..., help="termo do subnicho, no idioma do canal"),
    limite: int = typer.Option(25, help="quantos videos analisar"),
    aplicar: bool = typer.Option(
        False, "--aplicar", help="grava as palavras-chave em config/default.yaml"
    ),
):
    """Descobre o que ja performa no subnicho — alimenta o pilar 1 (titulo).

    Usa a API oficial: devolve views e data de forma estruturada, e ordena por
    views/dia para mostrar o que performa AGORA, nao o que acumulou com o tempo.
    """
    import yaml

    from .providers import obter_llm
    from .stages.pesquisa import buscar, extrair_padroes, palavras_frequentes

    cfg = _cfg()
    console.print(f"Buscando [bold]{termo}[/] em {cfg.canal.idioma}...")

    videos = buscar(cfg, termo, limite)
    if not videos:
        console.print("[yellow]nenhum video encontrado[/]")
        raise typer.Exit(0)

    tabela = Table("Views", "Views/dia", "Titulo", "Canal")
    for v in videos[:15]:
        tabela.add_row(f"{v.views:,}", f"{v.views_por_dia:,.0f}", v.titulo[:55], v.canal[:20])
    console.print(tabela)

    frequentes = palavras_frequentes(videos)
    console.print("\n[bold]Palavras-chave ponderadas por performance:[/]")
    console.print(", ".join(p for p, _ in frequentes))

    analise = extrair_padroes(obter_llm(cfg), cfg, videos)

    if padroes := analise.get("padroes"):
        console.print("\n[bold]Padroes estruturais:[/]")
        for p in padroes:
            console.print(f"  - {p}")
    if dif := analise.get("diferencial_alta_performance"):
        console.print(f"\n[bold]O que separa os que performam:[/]\n{dif}")
    if propostos := analise.get("titulos_propostos"):
        console.print("\n[bold]Titulos propostos:[/]")
        for t in propostos:
            console.print(f"  - {t}")

    if not aplicar:
        console.print(
            "\n[dim]Revise antes de adotar. Para gravar as palavras-chave na "
            "config: --aplicar[/]"
        )
        raise typer.Exit(0)

    caminho = Path("config/default.yaml")
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}
    chaves = analise.get("palavras_chave") or [p for p, _ in frequentes[:15]]
    atuais = dados.setdefault("canal", {}).get("referencias_titulo") or []
    dados["canal"]["referencias_titulo"] = sorted({*atuais, *chaves})
    caminho.write_text(
        yaml.safe_dump(dados, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    console.print(
        f"\n[green]{len(dados['canal']['referencias_titulo'])} palavras-chave "
        f"gravadas em {caminho}[/]"
    )


@app.command("voice-test")
def voice_test(
    voice_id: str = typer.Option("", help="voice_id a testar (padrao: o do .env)"),
):
    """Gera uma amostra curta no idioma do canal para avaliacao nativa.

    Rode ANTES de produzir o primeiro video: o sotaque do clone bate direto no
    pilar 3 (retencao), e 15 minutos de teste evitam semanas de video ruim.
    """
    from .providers import obter_llm, obter_tts
    from .stages.revisao import gerar_amostra_voz

    cfg = _cfg()
    destino = cfg.out_dir / "_teste_voz"
    amostra = gerar_amostra_voz(
        obter_llm(cfg), obter_tts(cfg), cfg, destino, voice_id or cfg.tts_voice_id
    )

    console.print(f"\n[bold]Texto ({cfg.canal.idioma}):[/]\n{amostra.texto}\n")
    console.print(f"[green]Audio:[/] {amostra.audio}")
    console.print(
        "\n[yellow]Envie este audio para um falante nativo avaliar.[/] Pergunte:\n"
        "  1. A pronuncia soa nativa ou estrangeira?\n"
        "  2. O ritmo soa natural para narracao?\n"
        "  3. Voce assistiria 8 minutos desta voz?\n\n"
        "Se a resposta 1 for 'estrangeira', troque para voz nativa de catalogo "
        "(MAQ_TTS_VOICE_ID) antes de escalar."
    )


@app.command()
def comentarios(
    slug: str = typer.Argument(..., help="slug do video publicado"),
    limite: int = typer.Option(50, help="quantos comentarios analisar"),
):
    """Le e traduz os comentarios, destacando sinais tecnicos acionaveis."""
    from .providers import obter_llm
    from .stages.revisao import analisar_comentarios, buscar_comentarios

    cfg = _cfg()
    p = Pipeline(cfg)
    video = p.store.obter(slug)
    if not video or not video.youtube_id:
        console.print(f"[red]video '{slug}' nao encontrado ou nao publicado[/]")
        raise typer.Exit(1)

    brutos = buscar_comentarios(cfg, video.youtube_id, limite)
    if not brutos:
        console.print("[yellow]sem comentarios ainda[/]")
        raise typer.Exit(0)

    analise = analisar_comentarios(obter_llm(cfg), cfg, brutos)
    if not analise:
        raise typer.Exit(0)

    console.print(f"\n[bold]Sentimento:[/] {analise.get('sentimento', '?')}")
    console.print(f"\n{analise.get('resumo', '')}\n")

    if sinais := analise.get("sinais_tecnicos"):
        console.print("[bold yellow]Sinais tecnicos acionaveis:[/]")
        for s in sinais:
            console.print(f"  - {s}")

    if relevantes := analise.get("comentarios_relevantes"):
        tabela = Table("Original", "Traducao")
        for c in relevantes[:10]:
            tabela.add_row(c.get("original", "")[:60], c.get("traducao", "")[:60])
        console.print(tabela)


@app.command()
def revisar(slug: str):
    """Traduz o roteiro para o seu idioma e avalia se soa natural."""
    from .providers import obter_llm
    from .stages.revisao import revisar_roteiro

    cfg = _cfg()
    p = Pipeline(cfg)
    video = p.store.obter(slug)
    if not video or not video.roteiro:
        console.print(f"[red]video '{slug}' sem roteiro[/]")
        raise typer.Exit(1)

    r = revisar_roteiro(obter_llm(cfg), cfg, video.roteiro)
    naturalidade = r.get("naturalidade", "?")
    cor = {"natural": "green", "aceitavel": "yellow"}.get(naturalidade, "red")

    console.print(f"\n[bold]{video.roteiro.titulo}[/]")
    console.print(f"Naturalidade: [{cor}]{naturalidade}[/]")
    if obs := r.get("observacao"):
        console.print(f"Observacao: {obs}")
    console.print(f"\n[bold]Traducao ({cfg.canal.idioma_revisao}):[/]\n{r.get('traducao', '')}")


@app.command()
def custo():
    """Custo de producao acumulado por video."""
    store = Store(_cfg().data_dir / "maquina.db")
    videos = store.listar(limite=200)
    total = sum(v.custo_usd for v in videos)

    tabela = Table("Slug", "Formato", "Custo (US$)")
    for v in videos:
        if v.custo_usd:
            tabela.add_row(v.slug, v.formato.value, f"{v.custo_usd:.4f}")
    console.print(tabela)

    com_custo = [v for v in videos if v.custo_usd]
    console.print(f"\nTotal: US$ {total:.2f} em {len(com_custo)} videos")
    if com_custo:
        console.print(f"Media por video: US$ {total / len(com_custo):.4f}")


@app.command()
def doctor():
    """Verifica ambiente, credenciais e providers ativos."""
    from . import media
    from .providers import obter_imagem, obter_llm, obter_tts

    cfg = _cfg()
    tabela = Table("Item", "Status", "Detalhe")

    try:
        tabela.add_row("ffmpeg", "[green]ok[/]", media.ffmpeg_bin())
    except Exception as e:
        tabela.add_row("ffmpeg", "[red]falta[/]", str(e))

    for nome, obj in [
        ("LLM", obter_llm(cfg)),
        ("TTS", obter_tts(cfg)),
        ("Imagem", obter_imagem(cfg)),
    ]:
        real = "Stub" not in type(obj).__name__
        tabela.add_row(
            nome,
            "[green]real[/]" if real else "[yellow]stub[/]",
            type(obj).__name__,
        )

    tabela.add_row(
        "YouTube",
        "[green]ok[/]" if cfg.yt_token.exists() else "[yellow]sem token[/]",
        str(cfg.yt_token),
    )
    tabela.add_row("Canal", cfg.canal.nome, f"idioma={cfg.canal.idioma}")
    tabela.add_row("Revisao humana", "on" if cfg.publicacao.exigir_revisao else "off",
                   f"max {cfg.publicacao.max_por_dia}/dia")
    console.print(tabela)


if __name__ == "__main__":
    app()
