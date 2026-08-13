"""Saida do Gemini: quem escreve o roteiro agora e a Anthropic.

O motivo nao foi qualidade, foi cota. O free tier do Gemini da 20 requisicoes
por DIA e cada pacote gasta de 2 a 5 (ideacao, roteiro, ate duas extensoes,
short companheiro). Em 12/08/2026, as 22:14, next-level-money morreu com HTTP
429 — e a cadeia de providers escolhia o fornecedor UMA VEZ, na construcao,
entao nao havia para onde ir mesmo com a Anthropic ociosa.

Os testes aqui cobrem as tres coisas que aquele run provou faltar: cadeia que
troca de elo durante a chamada, corpo de request valido para a familia atual
(nada de budget_tokens), e teto de gasto que nao vira fallback silencioso.
"""

from __future__ import annotations

import json

import httpx
import pytest

from maquina.providers import LLMCadeia, obter_llm
from maquina.providers.base import ErroOrcamento, ErroProvider
from maquina.providers.reais import LLMAnthropic


# ---------- corpo do request ----------

def _sse(*eventos: dict) -> bytes:
    return b"".join(
        f"event: {e['type']}\ndata: {json.dumps(e)}\n\n".encode() for e in eventos
    )


def _resposta_ok(texto: str = "resposta", parou_por: str = "end_turn") -> bytes:
    return _sse(
        {"type": "message_start",
         "message": {"usage": {"input_tokens": 1000, "output_tokens": 0}}},
        {"type": "content_block_start", "index": 0,
         "content_block": {"type": "thinking", "thinking": ""}},
        {"type": "content_block_delta", "index": 0,
         "delta": {"type": "thinking_delta", "thinking": "raciocinio interno"}},
        {"type": "content_block_start", "index": 1,
         "content_block": {"type": "text", "text": ""}},
        {"type": "content_block_delta", "index": 1,
         "delta": {"type": "text_delta", "text": texto}},
        {"type": "message_delta", "delta": {"stop_reason": parou_por},
         "usage": {"output_tokens": 2000}},
        {"type": "message_stop"},
    )


def _anthropic(monkeypatch, responder, **kwargs) -> tuple[LLMAnthropic, list[dict]]:
    """LLMAnthropic real, com o transporte HTTP trocado por um espiao."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-de-teste")
    llm = LLMAnthropic(**kwargs)
    corpos: list[dict] = []

    def _handler(req: httpx.Request) -> httpx.Response:
        corpos.append(json.loads(req.content))
        return responder(len(corpos))

    llm._cli = httpx.Client(
        transport=httpx.MockTransport(_handler), base_url="https://api.anthropic.com"
    )
    return llm, corpos


def test_pede_pensamento_adaptativo_e_esforco(monkeypatch):
    llm, corpos = _anthropic(monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()))

    assert llm.completar("oi", esforco="high") == "resposta"

    corpo = corpos[0]
    assert corpo["thinking"] == {"type": "adaptive"}
    assert corpo["output_config"] == {"effort": "high"}
    assert corpo["stream"] is True
    assert corpo["model"] == "claude-opus-5"


@pytest.mark.parametrize("proibido", ["budget_tokens", "temperature", "top_p", "top_k"])
def test_nao_manda_parametro_que_a_familia_atual_recusa(monkeypatch, proibido):
    """Opus 5 devolve 400 para qualquer um destes — o run morre na primeira cena."""
    llm, corpos = _anthropic(monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()))

    llm.completar("oi")

    assert proibido not in json.dumps(corpos[0])


def test_reserva_espaco_para_o_pensamento_alem_do_pedido(monkeypatch):
    """Pensamento sai do mesmo orcamento da resposta.

    Sem a folga, um roteiro de 16k gastaria parte do teto pensando e sairia
    cortado no meio do JSON — erro que aparece como "JSON invalido" tres
    camadas acima, sem dizer que a causa foi truncamento.
    """
    llm, corpos = _anthropic(monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()))

    llm.completar("oi", max_tokens=16384)

    assert corpos[0]["max_tokens"] > 16384


def test_pensamento_nao_entra_no_texto(monkeypatch):
    """O JSON do roteiro e parseado direto: raciocinio junto quebraria o parse."""
    llm, _ = _anthropic(monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()))

    assert llm.completar("oi") == "resposta"


def test_resposta_truncada_diz_que_foi_truncada(monkeypatch):
    llm, _ = _anthropic(
        monkeypatch,
        lambda _: httpx.Response(200, content=_resposta_ok('{"cenas": [{"nar', "max_tokens")),
    )

    with pytest.raises(ErroProvider, match="truncada"):
        llm.completar("oi")


def test_campo_recusado_com_400_nao_mata_o_run(monkeypatch):
    """Rede contra corpo de request que envelhece.

    `thinking` e `output_config` dao qualidade ao roteiro, mas nao SAO o
    roteiro. Um 400 neles sem esta rede viraria queda para o Gemini (que esta
    sem cota) e run perdido — o problema que a migracao veio resolver.
    """
    respostas = {
        1: httpx.Response(400, json={"error": {"message": "output_config: unsupported"}}),
        2: httpx.Response(200, content=_resposta_ok()),
    }
    llm, corpos = _anthropic(monkeypatch, lambda n: respostas[n])

    assert llm.completar("oi") == "resposta"
    assert "output_config" in corpos[0]
    assert "output_config" not in corpos[1]
    assert corpos[1]["thinking"] == {"type": "adaptive"}, "so o campo recusado sai"


def test_400_que_nao_e_de_campo_opcional_falha_na_hora(monkeypatch):
    """Modelo inexistente ou prompt invalido nao se resolve tirando campo."""
    llm, corpos = _anthropic(
        monkeypatch, lambda _: httpx.Response(400, json={"error": "model not found"})
    )

    with pytest.raises(ErroProvider, match="400"):
        llm.completar("oi")
    assert len(corpos) == 1, "nao insiste no que nao vai mudar"


def test_modelo_de_outro_provider_falha_na_construcao(monkeypatch):
    """`llm_model: gemini-flash-latest` servia aos tres providers.

    Nesse caminho a classe pedia um modelo do Google a api.anthropic.com e
    tomava 404 no meio da producao. Agora a reclamacao vem antes da primeira
    chamada, e diz qual campo usar.
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-de-teste")

    with pytest.raises(ErroProvider, match="llm_model_gemini"):
        LLMAnthropic("gemini-flash-latest")


def test_conta_o_gasto_pelo_preco_do_modelo(monkeypatch):
    llm, _ = _anthropic(monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()))

    llm.completar("oi")

    # 1k entrada a US$5/1M + 2k saida a US$25/1M
    assert llm.custo_usd == pytest.approx(0.001 * 5 + 0.002 * 25, rel=1e-6)


def test_429_e_repetido_antes_de_desistir(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _: None)
    respostas = {
        1: httpx.Response(429, json={"error": "rate limit"}),
        2: httpx.Response(200, content=_resposta_ok()),
    }
    llm, corpos = _anthropic(monkeypatch, lambda n: respostas[n])

    assert llm.completar("oi") == "resposta"
    assert len(corpos) == 2


def test_teto_de_gasto_para_o_run(monkeypatch):
    llm, _ = _anthropic(
        monkeypatch, lambda _: httpx.Response(200, content=_resposta_ok()), teto_usd=0.01
    )

    llm.completar("oi")  # gasta US$ 0,055, acima do teto
    with pytest.raises(ErroOrcamento, match="teto"):
        llm.completar("de novo")


# ---------- cadeia com fallback na chamada ----------

class LLMFake:
    def __init__(self, resposta: str = "", erro: Exception | None = None):
        self.resposta = resposta
        self.erro = erro
        self.chamadas = 0
        self.custo_usd = 1.0

    def completar(self, prompt, *, sistema="", max_tokens=4096, esforco=""):
        self.chamadas += 1
        if self.erro:
            raise self.erro
        return self.resposta


def test_provider_que_cai_no_meio_do_run_passa_a_vez(monkeypatch):
    """O caso de 12/08/2026: 429 na cota diaria com outro provider disponivel."""
    morto = LLMFake(erro=ErroProvider("Gemini 429: cota diaria"))
    vivo = LLMFake(resposta="roteiro")
    cadeia = LLMCadeia([("gemini", lambda: morto), ("anthropic", lambda: vivo)])

    assert cadeia.completar("escreva") == "roteiro"
    assert vivo.chamadas == 1


def test_elo_morto_nao_e_tentado_de_novo():
    """Cota do dia nao volta na quinta chamada — insistir so gasta tempo."""
    morto = LLMFake(erro=ErroProvider("429"))
    vivo = LLMFake(resposta="ok")
    cadeia = LLMCadeia([("gemini", lambda: morto), ("anthropic", lambda: vivo)])

    for _ in range(3):
        cadeia.completar("x")

    assert morto.chamadas == 1
    assert vivo.chamadas == 3


def test_cadeia_toda_morta_levanta_erro_em_vez_de_inventar_texto():
    """Roteiro de stub publicado no YouTube e pior que run que falhou."""
    cadeia = LLMCadeia([
        ("a", lambda: LLMFake(erro=ErroProvider("caiu"))),
        ("b", lambda: LLMFake(erro=ErroProvider("caiu tambem"))),
    ])

    with pytest.raises(ErroProvider, match="nenhum LLM"):
        cadeia.completar("x")


def test_teto_de_gasto_nao_vira_fallback_para_o_proximo_elo():
    """Trocar de fornecedor por orcamento so mudaria o gasto de bolso."""
    caro = LLMFake(erro=ErroOrcamento("teto"))
    outro = LLMFake(resposta="ok")
    cadeia = LLMCadeia([("anthropic", lambda: caro), ("openai", lambda: outro)])

    with pytest.raises(ErroOrcamento):
        cadeia.completar("x")
    assert outro.chamadas == 0


def test_custo_soma_os_elos_usados():
    cadeia = LLMCadeia([
        ("a", lambda: LLMFake(erro=ErroProvider("caiu"))),
        ("b", lambda: LLMFake(resposta="ok")),
    ])
    cadeia.completar("x")

    assert cadeia.custo_usd == 2.0  # os dois foram construidos


# ---------- selecao de provider ----------

@pytest.fixture
def cfg():
    from maquina.config import Config

    return Config()


def _sem_chaves(monkeypatch):
    for env in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(env, raising=False)


def test_auto_poe_a_anthropic_na_frente_do_gemini(cfg, monkeypatch):
    _sem_chaves(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    cfg.llm_provider = "auto"

    cadeia = obter_llm(cfg)

    assert [nome for nome, _ in cadeia._elos] == ["anthropic", "gemini"]


def test_a_cadeia_empilha_os_free_tiers_na_ordem_do_yaml(cfg, monkeypatch):
    """Nenhum plano gratuito sozinho aguenta seis pacotes/dia; somados, sobram."""
    _sem_chaves(monkeypatch)
    for env in ("CEREBRAS_API_KEY", "GROQ_API_KEY", "MISTRAL_API_KEY"):
        monkeypatch.setenv(env, "x")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    cfg.llm_provider = "auto"

    cadeia = obter_llm(cfg)

    assert [n for n, _ in cadeia._elos] == ["cerebras", "groq", "mistral", "gemini"]


def test_provedor_da_cadeia_sem_chave_e_pulado_em_silencio(cfg, monkeypatch):
    """A lista e desejo; a chave e que decide. Citar quem nao assinei nao quebra."""
    _sem_chaves(monkeypatch)
    monkeypatch.setenv("GROQ_API_KEY", "x")
    cfg.llm_provider = "auto"

    assert [n for n, _ in obter_llm(cfg)._elos] == ["groq"]


def test_o_gemini_continua_como_rede_de_seguranca(cfg, monkeypatch):
    """Sair do Gemini como padrao nao e o mesmo que jogar fora a chave gratis."""
    _sem_chaves(monkeypatch)
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    cfg.llm_provider = "auto"

    cadeia = obter_llm(cfg)

    assert cadeia.completar.__self__._elos[0][0] == "gemini"


def test_sem_nenhuma_chave_cai_no_stub(cfg, monkeypatch):
    """E o que mantem o CI verde sem gastar credito."""
    _sem_chaves(monkeypatch)
    cfg.llm_provider = "auto"

    assert type(obter_llm(cfg)).__name__ == "LLMStub"


def test_provider_explicito_nao_ganha_cadeia_atras(cfg, monkeypatch):
    """Escolher gemini no YAML e escolha; nao pode virar chamada paga sem aviso."""
    _sem_chaves(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    cfg.llm_provider = "gemini"

    cadeia = obter_llm(cfg)

    assert [nome for nome, _ in cadeia._elos] == ["gemini"]


def test_cada_provider_recebe_o_seu_modelo(cfg, monkeypatch):
    """O bug latente: LLMAnthropic("gemini-flash-latest") era 404 garantido."""
    _sem_chaves(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    cfg.llm_provider = "auto"
    cadeia = obter_llm(cfg)

    construidos = {nome: fabrica() for nome, fabrica in cadeia._elos}

    assert construidos["anthropic"].modelo.startswith("claude-")
    assert construidos["gemini"].modelo == cfg.llm_modelos["gemini"]
