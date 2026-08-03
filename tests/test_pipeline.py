"""Testes da pipeline com providers offline — nao consomem credito nem rede."""

from __future__ import annotations

import pytest

from maquina.config import Config
from maquina.models import Cena, Formato, Ideia, Roteiro, Status, Video
from maquina.pipeline import Pipeline
from maquina.stages import compliance
from maquina.stages.diagnostico import Gargalo, diagnosticar
from maquina.models import Metricas
from maquina.storage import Store


@pytest.fixture
def cfg(tmp_path) -> Config:
    c = Config(data_dir=tmp_path / "data", out_dir=tmp_path / "out")
    c.llm_provider = c.tts_provider = c.image_provider = "stub"
    c.data_dir.mkdir(parents=True, exist_ok=True)
    c.out_dir.mkdir(parents=True, exist_ok=True)
    return c


# ---------- modelos ----------

def test_formato_define_resolucao():
    assert Formato.SHORTS.resolucao == (1080, 1920)
    assert Formato.LONGO.resolucao == (1920, 1080)
    assert Formato.LONGO.duracao_alvo_s >= 8 * 60  # blocos de anuncio


def test_slug_estavel_e_unico():
    a, b = Ideia(titulo="Como decidir melhor"), Ideia(titulo="Como decidir melhor")
    assert a.slug == b.slug
    assert a.slug != Ideia(titulo="Outro titulo").slug


# ---------- persistencia ----------

def test_store_roundtrip(cfg):
    store = Store(cfg.data_dir / "t.db")
    v = Video(slug="x", formato=Formato.LONGO, ideia=Ideia(titulo="T"))
    store.salvar(v)

    lido = store.obter("x")
    assert lido is not None and lido.slug == "x"

    v.status = Status.RENDERIZADO
    store.salvar(v)
    assert store.obter("x").status is Status.RENDERIZADO
    assert len(store.listar(Status.RENDERIZADO)) == 1


# ---------- compliance ----------

def _video_com_roteiro(texto: str, titulo: str = "Titulo") -> Video:
    return Video(
        slug=titulo.lower(),
        formato=Formato.LONGO,
        duracao_s=9 * 60,
        thumbnail_path="/tmp/t.jpg",
        roteiro=Roteiro(
            titulo=titulo,
            gancho="g",
            descricao="d",
            cenas=[Cena(indice=0, narracao=texto, prompt_visual="p")],
        ),
    )


def test_compliance_bloqueia_roteiro_duplicado(cfg):
    store = Store(cfg.data_dir / "t.db")
    texto = "Conteudo identico repetido para acionar a checagem de similaridade."

    primeiro = _video_com_roteiro(texto, "Primeiro")
    store.salvar(primeiro)

    res = compliance.verificar(_video_com_roteiro(texto, "Segundo"), cfg, store)
    assert not res.aprovado
    assert any("similar" in b for b in res.bloqueios)


def test_compliance_bloqueia_teto_diario(cfg):
    from datetime import datetime

    store = Store(cfg.data_dir / "t.db")
    for i in range(cfg.publicacao.max_por_dia):
        v = _video_com_roteiro(f"Texto exclusivo numero {i} " * 5, f"Titulo {i}")
        v.publicado_em = datetime.now()
        store.salvar(v)

    novo = _video_com_roteiro("Assunto completamente diferente dos demais " * 5, "Novo")
    res = compliance.verificar(novo, cfg, store)
    assert not res.aprovado
    assert any("teto diario" in b for b in res.bloqueios)


def test_compliance_alerta_video_longo_curto_demais(cfg):
    store = Store(cfg.data_dir / "t.db")
    v = _video_com_roteiro("Roteiro unico para este teste " * 5, "Curto")
    v.duracao_s = 5 * 60
    res = compliance.verificar(v, cfg, store)
    assert res.aprovado
    assert any("8 min" in a for a in res.alertas)


# ---------- diagnostico dos 3 pilares ----------

@pytest.mark.parametrize(
    "ctr,retencao,esperado",
    [
        (0.09, 12.0, Gargalo.ROTEIRO),     # atrai clique, nao segura
        (0.02, 35.0, Gargalo.THUMBNAIL),   # segura quem entra, poucos entram
        (0.02, 10.0, Gargalo.TITULO),      # os dois ruins -> tema/pauta
        (0.08, 34.0, Gargalo.NENHUM),      # alinhado
    ],
)
def test_diagnostico_identifica_gargalo(cfg, ctr, retencao, esperado):
    m = Metricas(youtube_id="v", impressoes=5000, ctr=ctr, retencao_media_pct=retencao)
    assert diagnosticar(m, cfg).gargalo is esperado


def test_diagnostico_nao_conclui_com_amostra_pequena(cfg):
    m = Metricas(youtube_id="v", impressoes=50, ctr=0.01, retencao_media_pct=5.0)
    assert diagnosticar(m, cfg).gargalo is Gargalo.SEM_DADOS


# ---------- legendas ----------

def test_legendas_respeitam_duracao_das_cenas(cfg, tmp_path):
    from maquina.stages.producao import gerar_legendas

    roteiro = Roteiro(
        titulo="t",
        gancho="g",
        cenas=[
            Cena(indice=0, narracao="Primeira cena com algum texto.", prompt_visual="p", duracao_s=4.0),
            Cena(indice=1, narracao="Segunda cena com outro texto.", prompt_visual="p", duracao_s=3.0),
        ],
    )
    srt = gerar_legendas(roteiro, tmp_path / "l.srt")
    conteudo = srt.read_text(encoding="utf-8")

    assert "-->" in conteudo
    assert conteudo.startswith("1\n")
    # Ultimo timestamp nao pode ultrapassar a soma das duracoes (4 + 3 = 7s).
    ultimo = conteudo.strip().splitlines()[-2].split(" --> ")[1]
    h, m, resto = ultimo.split(":")
    s = float(resto.replace(",", "."))
    assert int(h) * 3600 + int(m) * 60 + s <= 7.05


# ---------- rotacao de eixos (defesa da cadencia diaria) ----------

def test_eixos_rotacionam_sem_repetir(cfg):
    from maquina.stages.roteiro import proximo_eixo

    cfg.canal.eixos_tematicos = ["a", "b", "c"]
    percorridos = [proximo_eixo(cfg, i) for i in range(3)]
    assert percorridos == ["a", "b", "c"]          # N videos -> N eixos distintos
    assert proximo_eixo(cfg, 3) == "a"             # so entao reinicia


def test_eixo_tolera_lista_vazia(cfg):
    from maquina.stages.roteiro import proximo_eixo

    cfg.canal.eixos_tematicos = []
    assert proximo_eixo(cfg, 0) == "(livre)"


def test_ideacao_injeta_eixo_no_prompt(cfg, monkeypatch):
    """O eixo tem que chegar ao LLM — sem isso a defesa e decorativa."""
    from maquina.stages import roteiro as r

    capturado = {}
    original = r._json_do_llm

    class LLMEspiao:
        def completar(self, prompt, *, sistema="", max_tokens=4096):
            capturado["prompt"] = prompt
            from maquina.providers.stubs import LLMStub

            return LLMStub().completar(prompt, sistema=sistema)

    cfg.canal.eixos_tematicos = ["eixo-sentinela"]
    r.gerar_ideias(LLMEspiao(), cfg, Formato.LONGO, n=2, publicados=[])
    assert "eixo-sentinela" in capturado["prompt"]


# ---------- revisao em idioma estrangeiro ----------

def test_amostra_de_voz_produz_audio_real(cfg, tmp_path):
    from maquina.providers.stubs import LLMStub, TTSStub
    from maquina.stages.revisao import gerar_amostra_voz

    amostra = gerar_amostra_voz(LLMStub(), TTSStub(), cfg, tmp_path / "voz")
    assert amostra.texto.strip()
    assert amostra.audio.exists() and amostra.audio.stat().st_size > 0


def test_analise_de_comentarios_extrai_sinais(cfg):
    from maquina.providers.stubs import LLMStub
    from maquina.stages.revisao import analisar_comentarios

    r = analisar_comentarios(LLMStub(), cfg, ["komentar satu", "komentar dua"])
    assert r is not None and "sinais_tecnicos" in r


def test_analise_sem_comentarios_retorna_none(cfg):
    from maquina.providers.stubs import LLMStub
    from maquina.stages.revisao import analisar_comentarios

    assert analisar_comentarios(LLMStub(), cfg, []) is None


# ---------- ponta a ponta ----------

@pytest.mark.slow
def test_produzir_gera_mp4_real(cfg):
    """Roda a pipeline inteira offline e valida que sai um MP4 tocavel."""
    from maquina import media

    p = Pipeline(cfg)
    video = p.produzir(Ideia(titulo="Teste ponta a ponta", formato=Formato.SHORTS))

    assert video.status is Status.RENDERIZADO
    caminho = cfg.out_dir / video.slug / "final.mp4"
    assert caminho.exists() and caminho.stat().st_size > 10_000
    assert media.duracao(caminho) > 1.0
    assert (cfg.out_dir / video.slug / "thumbnail.jpg").exists()
