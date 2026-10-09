"""A tag que volta ao short tem de ser a que ele tinha, nao uma parecida.

O reparo copia os OITO PRIMEIROS do longo do mesmo pacote. Isso nao e
aproximacao: o `publicar.py` monta o short como `(short_tags or tags)[:8]`, e o
`orcamento_tags` so corta acima de 480 caracteres — teto que oito tags nunca
alcancam. Estes testes prendem essa igualdade contra as duas funcoes reais, de
modo que mudar uma sem mudar a outra quebre aqui.

E prendem tambem a trava que importa mais: `videos.update` apaga todo campo de
snippet que nao chegar, entao gravar so `tags` repetiria — um degrau adiante —
exatamente o defeito que este arquivo existe para consertar.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402
import tags_do_short as T  # noqa: E402


QUINZE = ["fap 2027", "fator acidentario de prevencao", "fapweb", "rat",
          "seguro acidente do trabalho", "aliquota rat", "contestacao fap",
          "crps", "folha de pagamento", "cnae", "seguranca do trabalho",
          "sesmt", "custo de acidente", "previdencia social", "gestao de sst"]


def _snippet(**extra):
    base = {"title": "Titulo do short", "description": "Paragrafo um.",
            "categoryId": "27", "defaultLanguage": "pt-BR",
            "defaultAudioLanguage": "pt-BR"}
    base.update(extra)
    return base


class _Falso:
    def __init__(self):
        self.enviado = None

    def __call__(self, url, data=None, method=None, headers=None):
        if method == "PUT":
            self.enviado = json.loads(data.decode())
        return _Corpo("{}")


class _Corpo:
    def __init__(self, txt):
        self.txt = txt

    def read(self):
        return self.txt.encode()


# --------------------------------------------- a fonte reproduz o original

def test_os_oito_do_longo_sao_os_do_short():
    """A igualdade que autoriza copiar do irmao, contra as funcoes reais.

    ATENCAO — ESTE TESTE FOI VIRADO EM 09/10/2026, e o motivo importa.

    Ele exigia `TAGS_DO_SHORT == 8` e a igualdade `longo[:8] == short`. Isso
    congelava um DEFEITO: o `publicar.py` mandava `tags[:8]` no short, e as sete
    que sobravam das quinze eram justamente as de cauda longa (aprendizado 662).
    O corte em oito era meu, nao do YouTube — o `orcamento_tags` ja respeita o
    limite de 480 caracteres, e quinze tags custam 216 dos 480. Com o `[:8]`
    removido, o short sobe com a lista INTEIRA, igual ao longo, e foi medido
    ponta a ponta no `aiQdNIGaRb8`.

    Licao de instrumento: um teste que afirma um numero redondo defende o numero,
    nao o comportamento. O que este teste deve cobrar e que o short e o longo
    recebam A MESMA lista, qualquer que seja o tamanho dela, e que quem decide o
    que cabe seja o orcamento.
    """
    # o que o `publicar.py` manda no short (sem corte desde 08/10)
    do_short_no_upload, _ = P.orcamento_tags(QUINZE)
    # o que o `publicar.py` manda no longo
    do_longo_publicado, custo = P.orcamento_tags(QUINZE)

    assert do_longo_publicado == do_short_no_upload, \
        "short e longo tem de receber a MESMA lista de tags"
    assert len(do_short_no_upload) == 15, "o orcamento nao pode cortar as quinze"
    assert custo <= 480, "as quinze cabem inteiras; o corte nunca entra em jogo"


def test_o_reparo_nao_corta_mais_a_lista():
    """`TAGS_DO_SHORT = None` significa: quem corta e o orcamento, nao um numero.

    Se alguem reintroduzir um inteiro aqui, o short volta a subir com uma
    fatia da copy e as tags de cauda longa se perdem em silencio. Este teste
    existe para que essa volta seja barulhenta.
    """
    assert T.TAGS_DO_SHORT is None


# ------------------------------------------------------ a gravacao e inteira

def test_grava_o_snippet_inteiro_e_nao_so_as_tags(monkeypatch):
    falso = _Falso()
    monkeypatch.setattr(T, "_req", falso)
    r = T.repor("tok", "S1", _snippet(), QUINZE[:8])
    assert r.startswith("reposto")
    env = falso.enviado["snippet"]
    assert env["tags"] == QUINZE[:8]
    assert env["title"] == "Titulo do short"
    assert env["description"] == "Paragrafo um."
    assert env["categoryId"] == "27"
    assert env["defaultLanguage"] == "pt-BR"


def test_nao_mexe_em_quem_ja_tem_tags(monkeypatch):
    falso = _Falso()
    monkeypatch.setattr(T, "_req", falso)
    assert T.repor("tok", "S1", _snippet(tags=["ja", "tinha"]), QUINZE[:8]) \
        == "ja tinha tags"
    assert falso.enviado is None


def test_sem_fonte_nao_inventa(monkeypatch):
    """Longo tambem sem tags: melhor deixar vazio do que escrever palpite."""
    falso = _Falso()
    monkeypatch.setattr(T, "_req", falso)
    r = T.repor("tok", "S1", _snippet(), [])
    assert r.startswith("sem fonte")
    assert falso.enviado is None


def test_modo_seco_nao_grava(monkeypatch):
    falso = _Falso()
    monkeypatch.setattr(T, "_req", falso)
    assert "nada enviado" in T.repor("tok", "S1", _snippet(), QUINZE[:8], seco=True)
    assert falso.enviado is None
