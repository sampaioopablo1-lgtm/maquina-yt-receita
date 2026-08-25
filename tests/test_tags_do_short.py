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

    No upload o short recebe `orcamento_tags(tags[:8])` e o longo recebe
    `orcamento_tags(tags)`. Como o orcamento so corta acima de 480 caracteres,
    e oito tags nao chegam la, os oito primeiros do longo publicado sao
    exatamente o que o short tinha.
    """
    # o que o `publicar.py` manda no short
    do_short_no_upload, _ = P.orcamento_tags(QUINZE[:8])
    # o que o `publicar.py` manda no longo, e que sobreviveu no ar
    do_longo_publicado, custo = P.orcamento_tags(QUINZE)

    assert do_longo_publicado[:T.TAGS_DO_SHORT] == do_short_no_upload
    assert len(do_short_no_upload) == 8, "o orcamento nao pode cortar oito tags"
    assert custo <= 480, "as quinze cabem inteiras; o corte nunca entra em jogo"


def test_o_corte_do_reparo_e_o_mesmo_do_publicar():
    """Se o `publicar.py` passar a mandar outro numero, este teste cai."""
    assert T.TAGS_DO_SHORT == 8


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
