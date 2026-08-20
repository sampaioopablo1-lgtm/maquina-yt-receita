"""O portao que confere numero contra fonte.

Ele nasce junto com a escrita automatica de roteiro e existe por causa dela.
Enquanto cada spec saia escrita a mao, a regra das duas fontes que batem era
cumprida na pesquisa; um gerador quebra esse acordo, porque texto de modelo
afirma com a mesma fluencia sendo verdade ou nao.

O que estes testes cercam e a parte que falha em SILENCIO:

  - o veredito preso ao texto que ele leu, e nao a spec;
  - o item que o modelo esqueceu de classificar valendo reprovacao, nunca
    aprovacao por omissao;
  - o artigo indefinido nao passando por numero, que era o defeito que
    inflava a lista de 61 para 85 na labtreinamento-003;
  - spec escrita a mao continuando a passar, para o portao novo nao travar a
    frota inteira no ciclo seguinte.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import fatos  # noqa: E402
import modelo  # noqa: E402
import prontidao  # noqa: E402


def _spec(**extra) -> dict:
    sp = {
        "slug": "labtreinamento", "pacote": "labtreinamento-999",
        "idioma": "pt-BR", "voz": "pt-BR-ThalitaMultilingualNeural",
        "longo": [{"layout": "titulo", "nar": "O salario minimo subiu para "
                                              "mil e quinhentos reais."}],
        "short": [{"layout": "titulo", "nar": "Uma coisa muda em setembro."}],
    }
    sp.update(extra)
    return sp


def _aprovado(sp: dict) -> dict:
    return {"verificado_em": "2026-08-20T00:00:00+00:00", "modelo": "claude-opus-5",
            "hash_narracao": fatos.impressao(sp), "veredito": "aprovado",
            "afirmacoes": []}


# ---------------------------------------------------------------- impressao

def test_impressao_muda_quando_a_narracao_muda():
    """Trocar UMA palavra da narracao tem de anular o veredito.

    E a propriedade que sustenta o portao inteiro: sem ela daria para aprovar
    um roteiro e renderizar outro, e o veredito viraria carimbo.
    """
    a = _spec()
    b = _spec()
    b["longo"][0]["nar"] = "O salario minimo subiu para mil e seiscentos reais."
    assert fatos.impressao(a) != fatos.impressao(b)


def test_impressao_ignora_o_que_nao_e_afirmacao():
    """Cor e kicker mudam o video, nao mudam o que ele AFIRMA.

    Reverificar por causa de uma troca de paleta gastaria dolar para reler o
    mesmo texto.
    """
    a = _spec()
    b = _spec(paleta={"ink": "#000000"})
    b["longo"][0]["kicker"] = "Mil e quinhentos"
    assert fatos.impressao(a) == fatos.impressao(b)


# ------------------------------------------------------------------ extracao

def test_artigo_indefinido_nao_e_afirmacao():
    """"Uma coisa muda em setembro" nao tem numero nenhum dentro.

    `narracao.conta_numeros` conta o artigo porque la ele soma contra um teto
    de quatro por frase e um artigo perdido nao derruba ninguem. Aqui seria
    fatal: medido na labtreinamento-003, o extrator devolvia 85 afirmacoes e
    "E uma coisa fica dita ja." era uma delas.
    """
    sp = _spec(longo=[{"nar": "Uma coisa fica dita ja. E uma outra tambem."}],
               short=[])
    assert fatos.afirmacoes(sp) == []


def test_o_artigo_some_mas_o_numero_ao_lado_fica():
    """So o token SOZINHO some. "um milhao" continua sendo afirmacao."""
    sp = _spec(longo=[{"nar": "Uma empresa gasta um milhao por ano."}], short=[])
    assert len(fatos.afirmacoes(sp)) == 1


def test_ano_em_digito_e_afirmacao_mesmo_sem_palavra_de_numero():
    sp = _spec(longo=[{"nar": "A norma foi publicada em 2015."}], short=[])
    assert len(fatos.afirmacoes(sp)) == 1


def test_extracao_cobre_longo_e_short():
    sp = _spec()
    blocos = {a["bloco"] for a in fatos.afirmacoes(sp)}
    assert blocos == {"longo"}          # o short do _spec so tem artigo
    sp["short"] = [{"nar": "Sao tres anos de prazo."}]
    assert {a["bloco"] for a in fatos.afirmacoes(sp)} == {"longo", "short"}


# ------------------------------------------------------------------ conferir

def test_sem_veredito_nao_passa():
    assert fatos.conferir(_spec())


def test_veredito_de_outro_texto_nao_vale():
    sp = _spec()
    sp["fatos"] = _aprovado(sp)
    sp["longo"][0]["nar"] = "O salario minimo subiu para dois mil reais."
    faltas = fatos.conferir(sp)
    assert faltas and "narracao mudou" in faltas[0]


def test_veredito_aprovado_e_intacto_passa():
    sp = _spec()
    sp["fatos"] = _aprovado(sp)
    assert fatos.conferir(sp) == []


def test_reprovado_diz_qual_frase_reprovou():
    """Reprovar sem apontar a frase obriga a reescrever o roteiro inteiro."""
    sp = _spec()
    sp["fatos"] = {**_aprovado(sp), "veredito": "reprovado",
                   "afirmacoes": [{"bloco": "longo", "cena": 0,
                                   "texto": "O salario minimo subiu para mil e quinhentos reais.",
                                   "situacao": "sem_fonte", "fontes": [], "nota": ""}]}
    faltas = fatos.conferir(sp)
    assert faltas and "salario minimo" in faltas[0] and "sem_fonte" in faltas[0]


def test_retorica_nao_reprova():
    """"Cinco colunas bastam" e estrutura do roteiro, nao afirmacao sobre o
    mundo. Se retorica reprovasse, o portao dispararia sempre — e alarme que
    dispara sempre e alarme que ninguem le (aprendizado 230)."""
    sp = _spec()
    sp["fatos"] = {**_aprovado(sp),
                   "afirmacoes": [{"bloco": "longo", "cena": 0, "texto": "Cinco colunas bastam.",
                                   "situacao": "retorica", "fontes": [], "nota": "estrutura"}]}
    assert fatos.conferir(sp) == []


# ------------------------------------------------------ omissao nao e aprovacao

def test_item_nao_classificado_vira_sem_fonte(monkeypatch):
    """O modelo devolve 3 vereditos para 4 afirmacoes. O que falta REPROVA.

    O caminho oposto — assumir que o silencio quer dizer "estava certo" — e o
    unico jeito de este portao aprovar um numero que ninguem olhou.
    """
    sp = _spec(longo=[{"nar": "Sao tres anos. O prazo vai ate 2029. "
                              "O custo medio e de cem reais."}], short=[])
    itens = fatos.afirmacoes(sp)
    assert len(itens) == 3

    resposta = {"afirmacoes": [
        {"i": 0, "situacao": "retorica", "nota": "estrutura"},
        {"i": 1, "situacao": "confirmado", "fontes": ["a", "b"], "nota": "bate"},
    ]}
    monkeypatch.setattr(modelo, "chamar", lambda *a, **k: json.dumps(resposta))

    v = fatos.verificar(sp)
    assert v["veredito"] == "reprovado"
    assert v["afirmacoes"][2]["situacao"] == "sem_fonte"
    assert "nao classificou" in v["afirmacoes"][2]["nota"]


def test_situacao_fora_da_lista_nao_aprova(monkeypatch):
    sp = _spec(longo=[{"nar": "O custo medio e de cem reais."}], short=[])
    monkeypatch.setattr(modelo, "chamar", lambda *a, **k: json.dumps(
        {"afirmacoes": [{"i": 0, "situacao": "provavelmente", "nota": "acho que sim"}]}))
    v = fatos.verificar(sp)
    assert v["veredito"] == "reprovado"
    assert v["afirmacoes"][0]["situacao"] == "sem_fonte"


def test_veredito_carimba_a_impressao_do_texto_que_leu(monkeypatch):
    sp = _spec(longo=[{"nar": "O custo medio e de cem reais."}], short=[])
    monkeypatch.setattr(modelo, "chamar", lambda *a, **k: json.dumps(
        {"afirmacoes": [{"i": 0, "situacao": "confirmado", "fontes": ["a", "b"], "nota": "x"}]}))
    v = fatos.verificar(sp)
    assert v["veredito"] == "aprovado"
    sp["fatos"] = v
    assert fatos.conferir(sp) == []


def test_roteiro_sem_numero_nenhum_aprova_sem_chamar_o_modelo(monkeypatch):
    """Raro, mas legitimo. Aprovar com a lista vazia e honesto: nao ha o que
    conferir, e o registro diz isso."""
    def explode(*a, **k):
        raise AssertionError("nao devia ter chamado a API")
    monkeypatch.setattr(modelo, "chamar", explode)
    sp = _spec(longo=[{"nar": "O trabalho fica melhor quando a equipe conversa."}],
               short=[])
    v = fatos.verificar(sp)
    assert v["veredito"] == "aprovado" and v["afirmacoes"] == []


# ------------------------------------------------------------------ o portao

def test_spec_escrita_a_mao_nao_precisa_de_veredito():
    """O portao novo nao pode travar as 50 specs que ja existem.

    Nenhuma delas tem `fatos`, e a pesquisa das duas fontes esta no cabecalho
    do `.build.py`. Quem responde por elas e a rotina que as escreveu.
    """
    assert prontidao._gate_fatos(_spec()) == []


def test_spec_de_maquina_sem_veredito_trava():
    assert prontidao._gate_fatos(_spec(autoria="maquina"))


def test_spec_de_maquina_com_veredito_valido_passa():
    sp = _spec(autoria="maquina")
    sp["fatos"] = _aprovado(sp)
    assert prontidao._gate_fatos(sp) == []


def test_fatos_esta_na_lista_de_portoes():
    """Escrever o portao e nao liga-lo e a forma silenciosa de nao ter portao."""
    assert "fatos" in dict(prontidao.PORTOES)
