"""Citar caminho e afirmar que o caminho EXISTE — medido em 14/10 as 02:3x.

Por tres dias quatro documentos citaram `references/shorts-playbook.md` como a
procedencia de um parametro de PRODUCAO (a faixa `ALVO_POR_CANAL` do
labtreinamento) e **o arquivo nunca foi comitado**: `git log --all -- references`
nao devolvia commit nenhum.

E o teste que eu escrevi para guardar essa procedencia PASSAVA, porque ele
exigia que a *string* "shorts-playbook" estivesse no `ensaio.py` e nunca exigiu
que o CAMINHO citado existisse. Portao verde fabricando "a procedencia esta
escrita" (§3.8) — ele guardava a citacao, nao a fonte.

Estes testes falham se qualquer `references/<arquivo>` citado nos documentos que
governam producao deixar de existir.
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[1]

# Os arquivos que GOVERNAM producao e por isso nao podem citar fonte fantasma.
ONDE = [
    pathlib.Path("fabrica") / "ensaio.py",
    pathlib.Path("CLAUDE.md"),
    pathlib.Path("docs") / "ROTINA.md",
    pathlib.Path("docs") / "pipeline-canal-dark-estudado.md",
]

CITACAO = re.compile(r"references/([A-Za-z0-9_.-]+\.md)")


def _citacoes():
    achadas = {}
    for rel in ONDE:
        alvo = RAIZ / rel
        if not alvo.exists():
            continue
        for nome in CITACAO.findall(alvo.read_text(encoding="utf-8")):
            achadas.setdefault(nome, []).append(str(rel))
    return achadas


def test_toda_referencia_citada_existe_de_verdade():
    faltando = {
        nome: onde
        for nome, onde in _citacoes().items()
        if not (RAIZ / "references" / nome).exists()
    }
    assert not faltando, (
        "citacao aponta para arquivo que NAO existe — foi exatamente este o "
        f"defeito de 11/10 a 14/10: {faltando}"
    )


def test_a_citacao_que_falhou_esta_entre_as_conferidas():
    """Sem esta ancora o teste acima passaria por vacuidade se a citacao saisse."""
    assert "shorts-playbook.md" in _citacoes(), (
        "o `shorts-playbook.md` saiu das citacoes: se isso foi deliberado, "
        "tire-o tambem do comentario de procedencia do `ensaio.py`, porque la "
        "ele e a fonte numero 2 da faixa 20-26 do labtreinamento"
    )


def test_o_playbook_declara_que_foi_RECONSTRUIDO():
    """Ele nao pode ser lido como leitura fresca dos repositorios."""
    t = (RAIZ / "references" / "shorts-playbook.md").read_text(encoding="utf-8")
    assert "RECONSTRU" in t.upper(), "a reconstrucao de 14/10 tem de ir declarada"
    assert "nunca foi comitado" in t, "o defeito tem de ficar escrito onde ele morava"


def test_o_playbook_mantem_a_procedencia_FRACA_a_vista():
    t = (RAIZ / "references" / "shorts-playbook.md").read_text(encoding="utf-8")
    for marca in ("vidIQ", "35 bilh", "Tubefilter", "sem nome"):
        assert marca in t, (
            f"a procedencia {marca!r} saiu: sem ela o playbook parece fonte "
            "forte, e ele e explicitamente MISTO e fraco"
        )


def test_o_playbook_nao_virou_limiar():
    """Ele nao autoriza mexer em parametro de producao sozinho."""
    t = (RAIZ / "references" / "shorts-playbook.md").read_text(encoding="utf-8")
    assert "convergencia" in t.lower() or "convergência" in t.lower()
    assert "nao decide nada por si" in t.lower() or "não decide nada por si" in t.lower()


def test_os_quatro_recusados_continuam_com_motivo_escrito():
    t = (RAIZ / "references" / "shorts-playbook.md").read_text(encoding="utf-8")
    for repo in ("youtube-automation-agent", "ai-video-generator-claude",
                 "claude-youtube", "claude-code-youtube-mcp", "claude-real-video"):
        assert repo in t, f"{repo} saiu da lista do que NAO entrou"
