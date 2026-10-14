"""As DUAS credenciais do `modelo.py`, e o que cada teste PODE afirmar.

Nasceu em 14/10 as 18:4x de uma correcao do DONO. Eu havia recomendado a ele a
chave de API do Console como "o caminho de menos trabalho", olhando so o nome da
variavel que o `modelo.py` lia. Ele perguntou se o Console tinha formato
gratuito, e a pergunta expoe o que eu nao tinha olhado: **credito de API e uma
carteira separada da assinatura**, logo a chave de API GASTA e o
`CLAUDE_CODE_OAUTH_TOKEN` (do `claude setup-token`) usa a assinatura que ele ja
paga. O caminho dele era o mais barato, e o meu conselho estava errado pelo
custo.

O QUE ESTES TESTES AFIRMAM: o mapeamento credencial -> CABECALHO, e que a
mensagem de falta nomeia os DOIS nomes.

O QUE ELES NAO AFIRMAM, de proposito: que o token de OAuth seja ACEITO por
`POST /v1/messages` deste script. Nao ha token nesta sessao para medir, e o token
nasceu para autenticar a CLI do Claude Code, que pode falar por outra rota. Um
teste que inventasse esse veredito seria portao verde fabricando "esta tudo
certo" (§3.8). Quando houver token, a leitura do 401/403 e que decide.
"""
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import modelo  # noqa: E402


def test_a_chave_de_API_vai_em_x_api_key():
    h = modelo.cabecalhos(modelo.credencial({"ANTHROPIC_API_KEY": "sk-ant-xxx"}))
    assert h["x-api-key"] == "sk-ant-xxx"
    assert "authorization" not in h


def test_o_token_de_oauth_vai_em_Authorization_Bearer_com_o_beta():
    h = modelo.cabecalhos(modelo.credencial({"CLAUDE_CODE_OAUTH_TOKEN": "tok"}))
    assert h["authorization"] == "Bearer tok"
    assert h["anthropic-beta"] == modelo.BETA_OAUTH
    assert "x-api-key" not in h, (
        "token de OAuth em x-api-key seria apresentar a credencial na forma "
        "errada e ler o 401 como se fosse token invalido")


def test_as_duas_formas_mandam_a_versao_e_o_content_type():
    for env in ({"ANTHROPIC_API_KEY": "k"}, {"CLAUDE_CODE_OAUTH_TOKEN": "t"}):
        h = modelo.cabecalhos(modelo.credencial(env))
        assert h["anthropic-version"] == "2023-06-01"
        assert h["content-type"] == "application/json"


def test_a_chave_de_API_tem_PRECEDENCIA__porque_e_a_rota_VERIFICADA():
    cred = modelo.credencial({"ANTHROPIC_API_KEY": "k",
                              "CLAUDE_CODE_OAUTH_TOKEN": "t"})
    assert cred.tipo == "api_key", (
        "com as duas no ambiente usa-se a que sabemos que funciona; trocar a "
        "ordem e decisao com procedencia, nao arrumacao")


def test_variavel_VAZIA_nao_conta_como_credencial():
    """Secret inexistente no GitHub chega como string vazia, nao como ausente."""
    cred = modelo.credencial({"ANTHROPIC_API_KEY": "   ",
                              "CLAUDE_CODE_OAUTH_TOKEN": "t"})
    assert cred.tipo == "oauth", (
        "chave vazia caindo em x-api-key daria 401 e eu leria 'chave invalida' "
        "onde o fato e 'secret nao colado'")


def test_sem_nenhuma_das_duas_a_mensagem_NOMEIA_as_duas():
    with pytest.raises(SystemExit) as e:
        modelo.credencial({})
    msg = str(e.value)
    assert "ANTHROPIC_API_KEY" in msg and "CLAUDE_CODE_OAUTH_TOKEN" in msg
    assert "setup-token" in msg, (
        "quem le a falha tem de saber COMO obter a segunda, nao so o nome dela")


def test_a_credencial_NUNCA_imprime_o_valor():
    cred = modelo.credencial({"CLAUDE_CODE_OAUTH_TOKEN": "segredo-que-nao-sai"})
    for texto in (str(cred), repr(cred), f"{cred}"):
        assert "segredo-que-nao-sai" not in texto
        assert "chars" in texto
    assert "segredo-que-nao-sai" not in str({"c": cred})


def test_o_modulo_DECLARA_que_a_rota_do_oauth_nao_foi_medida():
    """A ressalva e parte do achado: sem token nao ha veredito."""
    fonte = (RAIZ / "fabrica" / "modelo.py").read_text()
    assert "NAO AFIRMO" in fonte
    assert "setup-token" in fonte
    assert "carteira separada" in fonte, (
        "a razao de existir a segunda credencial e o CUSTO, e ela tem de ficar "
        "escrita onde o codigo a le")
