"""Dez citacoes apontavam para dentro de um pacote que nao esta no repo.

MEDIDO em 19/10 as 06:1x. Varridos os caminhos citados entre crases no codigo e
nos documentos da rotina, DOIS nao existem — nem no repo, nem no `git log --all`,
nem neste conteiner, nem no sandbox do Composio:

  * `motor/config.py`, citado em CINCO lugares, que e a procedencia declarada
    dos quatro temas e portanto da PALETA DOS TRES CANAIS;
  * `motor/scenes.html`, citado em CINCO lugares, que e a procedencia declarada
    das coordenadas dos layouts `comparar` e `numero`.

**E o aprendizado 743 pela SEGUNDA vez** — la foi o `references/shorts-playbook.md`
citado em quatro documentos por tres dias — e agora na procedencia da identidade
visual da frota inteira.

**E o teste que eu escrevi para guardar aquilo NAO podia pegar estes:** o
`test_referencia_citada_existe.py` abre UM caminho cravado a mao. Identidade onde
havia propriedade, a classe do 743/753/761, e por isso ele passava verde.

Este arquivo varre TODOS os caminhos citados e reprova listando os que faltam.
As duas excecoes conhecidas sao DECLARADAS e apontam para
`docs/pacote-do-dono-NAO-esta-no-repo.md`, que diz de onde os valores vieram e
qual dos dois tem segunda fonte independente (as cores tem; as coordenadas nao).
"""
import glob
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho citado que NAO existe e cuja ausencia esta EXPLICADA. Entrada nova aqui
# exige paragrafo no documento — senao isto vira o silencio que o arquivo
# combate.
AUSENTES_DECLARADOS = {
    "motor/config.py": "docs/pacote-do-dono-NAO-esta-no-repo.md",
    "motor/scenes.html": "docs/pacote-do-dono-NAO-esta-no-repo.md",
}

# Extensoes de arquivo NOSSO. `.html` entra porque e justamente a de um dos dois
# ausentes; sem ela o teste nao mediria o caso que o fez existir.
EXT = r"(?:py|md|json|jsonl|html|yml|yaml|sql|txt)"
CITACAO = re.compile(rf"`([A-Za-z0-9_./-]+/[A-Za-z0-9_.-]+\.{EXT})`")

# Prefixo que NAO e caminho do repo: exemplo de URL, caminho de outro sistema.
IGNORA = ("http", "/etc/", "/proc/", "/usr/", "/tmp/", "~/")


def _fontes():
    alvos = []
    for padrao in ("fabrica/*.py", "tests/*.py", "consultas/*.sql"):
        alvos += glob.glob(os.path.join(RAIZ, padrao))
    for doc in ("CLAUDE.md", "docs/ROTINA.md", "docs/ROTINA-NUCLEO.md"):
        p = os.path.join(RAIZ, doc)
        if os.path.exists(p):
            alvos.append(p)
    return sorted(alvos)


def _citados():
    """{caminho citado: [arquivos que o citam]}, do disco."""
    fora: dict[str, list[str]] = {}
    for f in _fontes():
        with open(f, encoding="utf-8", errors="replace") as fh:
            texto = fh.read()
        for achado in set(CITACAO.findall(texto)):
            if achado.startswith(IGNORA):
                continue
            fora.setdefault(achado, []).append(os.path.relpath(f, RAIZ))
    return fora


def test_a_varredura_nao_fica_VAZIA():
    """Regex que deixa de casar faria todo o arquivo passar calado."""
    cit = _citados()
    assert len(cit) >= 20, (
        f"a varredura achou so {len(cit)} caminhos citados — perdeu a ancora")
    assert len(_fontes()) >= 50, "as fontes encolheram; releia este arquivo"


def test_todo_caminho_citado_EXISTE_ou_esta_declarado():
    cit = _citados()
    faltam = {k: v for k, v in cit.items()
              if not os.path.exists(os.path.join(RAIZ, k))}
    nao_declarados = {k: v for k, v in faltam.items()
                      if k not in AUSENTES_DECLARADOS}
    assert not nao_declarados, (
        "citar caminho e afirmar que o caminho existe (743). Estes nao existem "
        "e nao estao declarados: " + "; ".join(
            f"{k} (citado em {', '.join(v[:3])})"
            for k, v in sorted(nao_declarados.items())))


def test_os_DOIS_ausentes_conhecidos_continuam_ausentes():
    """Se o pacote do dono voltar, a excecao sai e a citacao volta a conferir.

    Reprova no outro sentido de proposito: manter uma excecao para arquivo que
    JA existe e deixar uma mentira travada por teste."""
    presentes = [k for k in AUSENTES_DECLARADOS
                 if os.path.exists(os.path.join(RAIZ, k))]
    assert not presentes, (
        f"{presentes} voltou ao repo — tire da lista de excecoes e corrija "
        "as citacoes, porque agora elas conferem")


def test_cada_excecao_tem_documento_que_a_EXPLICA():
    for caminho, doc in AUSENTES_DECLARADOS.items():
        p = os.path.join(RAIZ, doc)
        assert os.path.exists(p), f"o documento da excecao {caminho} nao existe"
        with open(p, encoding="utf-8") as f:
            texto = f.read()
        assert caminho in texto, (
            f"{doc} nao explica {caminho} — excecao sem motivo escrito e o "
            "silencio que este arquivo combate")


def test_os_DOIS_ausentes_sao_de_fato_citados_no_codigo():
    """Sem citacao viva, as excecoes nao medem nada e devem sair da lista."""
    cit = _citados()
    for caminho in AUSENTES_DECLARADOS:
        assert caminho in cit, (
            f"{caminho} nao e mais citado em lugar nenhum — tire da lista")
        assert len(cit[caminho]) >= 2, (
            f"{caminho} ficou com uma citacao so: {cit[caminho]}")


def test_o_documento_distingue_o_que_TEM_segunda_fonte():
    """As cores foram MEDIDAS no video publicado; as coordenadas, nao.

    Essa distincao e o conteudo do achado: sem ela o documento viraria 'nada
    disto se sustenta', que e falso e pior que a citacao quebrada."""
    with open(os.path.join(RAIZ, "docs",
                           "pacote-do-dono-NAO-esta-no-repo.md"),
              encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    for frase in ("segundo apoio", "SATAVG", "apoio ÚNICO", "743"):
        assert frase in texto, f"o documento perdeu {frase!r}"


def test_o_teste_ANTIGO_de_procedencia_continua_existindo():
    """Ele guarda o caso do 743 e NAO e substituido por este.

    Este varre; aquele abre o arquivo e confere o CONTEUDO da referencia. Os
    dois medem coisas diferentes, e apagar o antigo perderia a lição original."""
    p = os.path.join(RAIZ, "tests", "test_referencia_citada_existe.py")
    assert os.path.exists(p), "o teste do 743 saiu do disco"
