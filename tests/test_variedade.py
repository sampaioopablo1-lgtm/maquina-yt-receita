"""O portao de conteudo inautentico. Ver `fabrica/variedade.py`.

Estes testes travam tres coisas que eu quero que doam se alguem as afrouxar:
que os limiares sao os do mapa e nao outros, que o `esqueleto` AVISA e nunca
reprova (a trava do experimento 33 e o motivo), e que o fim de frase grego
conta `;` como interrogacao — ja errei isso uma vez com um `endswith("?")`.
"""
import json

import pytest

import variedade


def _spec(nar: str, l1: str = "Um", l2: str = "dois", slug: str = "canal-x",
          cenas: int = 5) -> dict:
    short = [{"layout": "titulo", "kicker": "k", "sub": "s", "nar": nar}]
    short += [{"layout": "titulo", "kicker": "k", "sub": "s", "nar": "Outra."}
              for _ in range(max(0, cenas - 2))]
    short += [{"layout": "cta", "kicker": "k", "sub": "s", "nar": "Fim."}]
    return {"slug": slug, "pacote": f"{slug}-s001", "short": short, "longo": [],
            "thumb": {"l1": l1, "l2": l2}, "paleta": {}}


# ----------------------------- GANCHO ---------------------------------------

def test_gancho_de_treze_palavras_reprova():
    nar = "uma duas tres quatro cinco seis sete oito nove dez onze doze treze."
    erros, _ = variedade.analisa(_spec(nar))
    assert any(e.startswith("gancho") for e in erros)


def test_gancho_de_doze_palavras_passa():
    nar = "uma duas tres quatro cinco seis sete oito nove dez onze doze."
    erros, _ = variedade.analisa(_spec(nar))
    assert not any(e.startswith("gancho") for e in erros)


def test_o_gancho_mede_a_PRIMEIRA_frase_e_nao_a_cena():
    """Uma cena longa com gancho curto passa — e isso e o ponto do prompt 25.

    Se o portao medisse a cena inteira, ele cobraria brevidade de toda a
    narracao, que nao e o que o mapa pede nem o que prende em um segundo.
    """
    nar = ("Curto demais? Agora vem uma frase enorme com muitas palavras "
           "depois dela, que nao deveria contar para o gancho de jeito nenhum.")
    erros, _ = variedade.analisa(_spec(nar))
    assert not any(e.startswith("gancho") for e in erros)


def test_o_ponto_e_virgula_grego_fecha_frase():
    """`;` e o sinal de interrogacao em grego. Um checador ingenuo de `?` lia a
    pergunta grega como frase inacabada e somava as palavras da frase seguinte.
    """
    nar = "Ρωτάς πόσο κοστίζει; " + " ".join(["λέξη"] * 20) + "."
    erros, _ = variedade.analisa(_spec(nar))
    assert not any(e.startswith("gancho") for e in erros), (
        "a primeira frase grega tem tres palavras; o portao somou a segunda")


# ----------------------------- THUMBNAIL ------------------------------------

def test_thumb_de_cinco_palavras_reprova():
    erros, _ = variedade.analisa(_spec("Curto.", l1="Uma duas", l2="tres quatro cinco"))
    assert any(e.startswith("thumbnail") for e in erros)


def test_thumb_de_quatro_palavras_passa():
    erros, _ = variedade.analisa(_spec("Curto.", l1="Uma duas", l2="tres quatro"))
    assert not any(e.startswith("thumbnail") for e in erros)


# ----------------------------- ESQUELETO ------------------------------------

def test_o_esqueleto_e_a_sequencia_de_layouts():
    s = _spec("Curto.")
    assert variedade.esqueleto(s["short"]) == "titulo-titulo-titulo-titulo-cta"


def test_esqueleto_repetido_AVISA_e_nunca_reprova(tmp_path):
    """A trava do experimento 33 e o motivo, e esta no docstring do modulo.

    Se alguem transformar este aviso em erro sem fechar o 33 antes, este teste
    cai e diz por que.
    """
    d = tmp_path / "fabrica" / "specs"
    d.mkdir(parents=True)
    for i in range(6):
        s = _spec("Curto.", slug="canal-x")
        s["pacote"] = f"canal-x-s{i:03d}"
        (d / f"canal-x-s{i:03d}.json").write_text(json.dumps(s), encoding="utf-8")

    nova = _spec("Curto.", slug="canal-x")
    erros, avisos = variedade.analisa(nova, str(tmp_path), "canal-x-s999.json")
    assert any(a.startswith("esqueleto") for a in avisos)
    assert not any(e.startswith("esqueleto") for e in erros)


def test_esqueleto_diferente_nao_avisa(tmp_path):
    d = tmp_path / "fabrica" / "specs"
    d.mkdir(parents=True)
    for i in range(6):
        s = _spec("Curto.", slug="canal-x")
        s["pacote"] = f"canal-x-s{i:03d}"
        (d / f"canal-x-s{i:03d}.json").write_text(json.dumps(s), encoding="utf-8")

    nova = _spec("Curto.", slug="canal-x", cenas=4)
    variedade._CACHE.clear()
    _erros, avisos = variedade.analisa(nova, str(tmp_path), "canal-x-s999.json")
    assert not any(a.startswith("esqueleto") for a in avisos)


def test_canal_de_uma_peca_so_nao_avisa(tmp_path):
    """Sem irmas no canal nao ha mesmice para medir, e avisar ali seria ruido."""
    (tmp_path / "fabrica" / "specs").mkdir(parents=True)
    variedade._CACHE.clear()
    _erros, avisos = variedade.analisa(_spec("Curto."), str(tmp_path), "x.json")
    assert avisos == []


# ----------------------------- LIMIARES -------------------------------------

@pytest.mark.parametrize("nome,valor", [
    ("GANCHO_MAX_PALAVRAS", 12),
    ("THUMB_MAX_PALAVRAS", 4),
])
def test_os_limiares_sao_os_do_mapa(nome, valor):
    """12 e 4 vem do mapa (prompts 25 e 23), nao de mim.

    Mudar um deles e mudar a procedencia, e ai o docstring do modulo passa a
    mentir sobre de onde o numero veio. Se for para mudar, mude os dois lugares.
    """
    assert getattr(variedade, nome) == valor
