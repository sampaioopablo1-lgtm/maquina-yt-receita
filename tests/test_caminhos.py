"""O workdir e UM so para quem renderiza e para quem publica.

O defeito que estes testes prendem (15/08/2026): `publicar.py` resolvia o
diretorio com a string `/tmp/f/<pacote>` escrita a mao, sem ler
FABRICA_WORKDIR, enquanto `fabrica.py` e `vozes.py` liam a variavel. Render em
disco real terminava em /home/user/f/<pacote> e a publicacao ia procurar em
/tmp/f/<pacote>.

O teste que importa e o de CONCORDANCIA, nao o de valor: um default certo em
tres copias separadas volta a divergir na proxima vez que alguem mexer numa so.
"""

import ast
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from caminhos import RAIZ_PADRAO, dir_trabalho, raiz  # noqa: E402


@pytest.fixture
def sem_var(monkeypatch):
    monkeypatch.delenv("FABRICA_WORKDIR", raising=False)


def test_default_e_tmp_f(sem_var):
    """O Actions renderiza no default, e la /tmp e disco de verdade."""
    assert raiz() == RAIZ_PADRAO == "/tmp/f"
    assert dir_trabalho({"slug": "resep-naik-level"}) == "/tmp/f/resep-naik-level"


def test_variavel_vence(monkeypatch):
    """Sem isto o render de 86 cenas nao cabe: no sandbox /tmp e tmpfs (RAM)."""
    monkeypatch.setenv("FABRICA_WORKDIR", "/home/user/f")
    assert dir_trabalho({"slug": "x", "pacote": "resep-naik-level-003"}) \
        == "/home/user/f/resep-naik-level-003"


def test_pacote_vence_o_slug(sem_var):
    """Dois pacotes do mesmo canal na mesma pasta fazem o RETOMA costurar
    clipes de roteiros diferentes, sem erro nenhum."""
    sp = {"slug": "kolejny-poziom", "pacote": "kolejny-poziom-008"}
    assert dir_trabalho(sp).endswith("/kolejny-poziom-008")


def test_slug_quando_nao_ha_pacote(sem_var):
    """As specs antigas nao declaram `pacote` e continuam funcionando."""
    assert dir_trabalho({"slug": "sx-educacao"}).endswith("/sx-educacao")


def test_publicar_e_vozes_usam_a_MESMA_funcao():
    """A trava real: nenhum dos dois pode ter a sua propria copia do caminho.

    Ambos sao rodados como script (`python3 fabrica/publicar.py`), entao
    `fabrica/` entra no sys.path sozinho e o import direto de `caminhos` e o
    mesmo objeto — comparar por identidade prova que nao ha copia paralela.
    """
    import caminhos
    import publicar

    assert publicar.dir_trabalho is caminhos.dir_trabalho

    # O vozes.py importa edge_tts no topo, que nem sempre esta instalado onde
    # os testes rodam. Le o texto: o que se prende aqui e a AUSENCIA de uma
    # segunda resolucao, e isso o codigo-fonte mostra.
    fonte = open(os.path.join(RAIZ, "fabrica", "vozes.py"), encoding="utf-8").read()
    assert "from caminhos import dir_trabalho" in fonte


def _modulos():
    fab = os.path.join(RAIZ, "fabrica")
    for nome in sorted(os.listdir(fab)):
        if nome.endswith(".py") and nome != "caminhos.py":
            caminho = os.path.join(fab, nome)
            yield nome, ast.parse(open(caminho, encoding="utf-8").read())


def test_so_caminhos_le_a_variavel():
    """Ler FABRICA_WORKDIR e o que duplica o default; SETAR e legitimo.

    O `ensaio.py` seta a variavel para redirecionar o render do ensaio — e o
    uso certo. Quem faz `os.environ.get("FABRICA_WORKDIR", ...)` esta, por
    definicao, escrevendo uma segunda copia do default.
    """
    culpados = []
    for nome, arvore in _modulos():
        for no in ast.walk(arvore):
            if not (isinstance(no, ast.Call)
                    and isinstance(no.func, ast.Attribute)
                    and no.func.attr == "get"):
                continue
            if any(isinstance(a, ast.Constant) and a.value == "FABRICA_WORKDIR"
                   for a in no.args):
                culpados.append(f"{nome}:{no.lineno}")
    assert not culpados, (
        "leram FABRICA_WORKDIR direto em vez de chamar caminhos.raiz(): "
        + ", ".join(culpados)
    )


def test_ninguem_mais_escreve_tmp_f_a_mao():
    """`/tmp/f` so pode virar VALOR dentro de caminhos.py.

    Foi assim que o defeito entrou: um literal copiado pela metade. Docstring e
    texto de `help=` nomeiam o caminho sem resolver nada — nao sao o defeito, e
    proibi-los so faria alguem apagar a documentacao para o teste passar.
    """
    culpados = []
    for nome, arvore in _modulos():
        docs = {ast.get_docstring(n, clean=False) for n in ast.walk(arvore)
                if isinstance(n, (ast.Module, ast.ClassDef,
                                  ast.FunctionDef, ast.AsyncFunctionDef))}
        ajuda = {kw.value.value for no in ast.walk(arvore)
                 if isinstance(no, ast.Call)
                 for kw in no.keywords
                 if kw.arg == "help" and isinstance(kw.value, ast.Constant)}
        for no in ast.walk(arvore):
            if (isinstance(no, ast.Constant) and isinstance(no.value, str)
                    and "/tmp/f" in no.value
                    and no.value not in docs and no.value not in ajuda):
                culpados.append(f"{nome}:{no.lineno}: {no.value!r}")
    assert not culpados, (
        "resolveram o workdir a mao em vez de usar caminhos.dir_trabalho:\n"
        + "\n".join(culpados)
    )
