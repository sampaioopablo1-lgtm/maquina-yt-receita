# -*- coding: utf-8 -*-
"""O portao da verde no comentario fixado, e eu NAO achei como fazer pegar.

O ACHADO, reproduzido: entreguei a copy do `labtreinamento-s087` sem a secao
`## COMENTARIO FIXADO` e o portao `copy` reprovou UM problema — "sem
hashtags" — e deu VERDE no comentario, que tambem faltava. O `comentario` do
`publicar.ler_copy` e um balde PEGA-TUDO, e quem subiria como comentario
fixado do video era o bloco `## CONFIGURACOES DO STUDIO`.

E AS TRES TENTATIVAS DE DISCRIMINADOR FALHARAM. Este arquivo guarda os tres
numeros para que a rodada seguinte nao as repita, e guarda a REPRODUCAO, que e
a unica coisa com procedencia aqui.

O que este arquivo NAO faz: cobrar portao. Nao ha portao — a conferencia por
cabecalho reprovou 47 testes da suite porque o cabecalho TRADUZ, e a minha
medicao que a autorizou tinha filtrado a amostra pelo cabecalho em portugues.
"""
import ast
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import copy_secoes as CS  # noqa: E402

PISO_DE_SPECS = 150
PISO_DE_IDIOMAS = 4


def _specs():
    """TODA spec com copy seccionada — SEM filtrar por cabecalho.

    Filtrar por `## DESCRICAO` foi o erro que produziu o "322 de 322": a
    amostra ficava restrita ao cabecalho em portugues, logo nao podia conter
    contraexemplo. E o 725, e o filtro e a causa.
    """
    fora = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            with open(p, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        t = sp.get("copy")
        if isinstance(t, str) and "##" in t:
            fora.append((os.path.basename(p), sp))
    return fora


def test_a_varredura_sai_do_DISCO_e_reprova_se_encolher():
    specs = _specs()
    assert len(specs) >= PISO_DE_SPECS, (
        f"so {len(specs)} specs com copy seccionada — abaixo do piso de "
        f"{PISO_DE_SPECS} este arquivo passa por VACUIDADE"
    )


def test_a_varredura_cobre_MAIS_DE_UM_IDIOMA__que_e_a_guarda_do_725():
    """Sem esta guarda eu media vocabulario de um idioma e chamava de frota."""
    specs = _specs()
    idiomas = {sp.get("idioma", "?") for _, sp in specs}
    assert len(idiomas) >= PISO_DE_IDIOMAS, (
        f"a varredura ve so {sorted(idiomas)} — com menos de "
        f"{PISO_DE_IDIOMAS} idiomas ela nao pode achar o contraexemplo que "
        "derrubou a conferencia por cabecalho"
    )


def test_o_cabecalho_do_comentario_TRADUZ__e_e_por_isso_que_nao_ha_portao():
    """A medicao que derrubou a tentativa (1), e ela reprova se for apagada."""
    specs = _specs()
    sem_portugues = [
        (n, CS.cabecalho_do_comentario(sp["copy"]))
        for n, sp in specs
        if not re.search(r"^##\s*COMENT", sp["copy"], re.M | re.I)
    ]
    assert len(sem_portugues) >= 10, (
        "menos de dez specs sem o cabecalho portugues — se o acervo foi "
        "uniformizado, releia a nota: a conferencia por cabecalho volta a ser "
        f"possivel. Hoje: {len(sem_portugues)}"
    )
    traduzidos = {c for _, c in sem_portugues if c}
    assert traduzidos, (
        "nenhum dos cabecalhos traduzidos foi reconhecido — a lista "
        "CABECALHOS_MEDIDOS perdeu os idiomas, e com ela a REPRODUCAO"
    )


def test_a_tentativa_das_CHAVES_do_studio_nao_e_universal():
    """Tentativa (2): as chaves da API nao traduzem, mas faltam por geracao."""
    specs = _specs()
    chaves = ("privacyStatus", "categoryId", "madeForKids", "defaultLanguage")
    sem = [n for n, sp in specs if not all(k in sp["copy"] for k in chaves)]
    assert len(sem) >= 50, (
        "as quatro chaves do Studio passaram a estar em quase toda spec — "
        f"hoje faltam em {len(sem)}; se isso mudar, a tentativa (2) volta a "
        "poder ser avaliada e esta nota tem de ser relida"
    )


def test_a_tentativa_da_FORMA_das_linhas_da_FALSO_POSITIVO():
    """Tentativa (3): prosa em polones e indonesio comeca com "Palavra:".

    Detector que inventa achado e pior que nao ter detector (725). Este teste
    guarda os falsos positivos para que ninguem readote a forma.
    """
    chave = re.compile(r"^\s*(?:#|[A-Za-z_][A-Za-z0-9_]*\s*:\s*\S)")
    falsos = []
    for n, sp in _specs():
        com = CS.comentario_de(sp)
        linhas = [x for x in com.split("\n") if x.strip()]
        if not linhas:
            continue
        frac = sum(1 for x in linhas if chave.match(x)) / len(linhas)
        if frac > 0.5 and "privacyStatus" not in com:
            falsos.append(n)
    assert falsos, (
        "a forma `palavra:` deixou de dar falso positivo no acervo — se isso "
        "for verdade, a tentativa (3) volta a mesa; confira antes de readotar"
    )


def test_a_REPRODUCAO_do_vazamento_funciona__e_e_a_unica_prova_daqui():
    """Retirada a secao, o balde pega-tudo enche com outra secao."""
    vazou = [
        n for n, sp in _specs()
        if CS.vazamento_simulado(sp).get("vazou")
    ]
    assert len(vazou) >= 50, (
        "a simulacao do vazamento parou de reproduzir em quase toda spec — "
        f"hoje {len(vazou)}. Sem ela este arquivo nao prova o defeito"
    )


def test_a_simulacao_mostra_o_BLOCO_DO_STUDIO_subindo_como_comentario():
    """O caso concreto que eu publiquei: nao basta "vazou", importa O QUE."""
    for n, sp in _specs():
        v = CS.vazamento_simulado(sp)
        if v.get("vazou") and "privacyStatus" in (v.get("depois") or ""):
            return
    raise AssertionError(
        "nenhuma spec do disco reproduz o caso em que o bloco de "
        "CONFIGURACOES DO STUDIO sobe como comentario fixado — e esse e o "
        "caso que eu de fato escrevi nesta hora"
    )


def test_NAO_virou_portao__cobrado_por_AST():
    """Sem discriminador com procedencia nao ha portao (§10).

    Por AST e nao por texto porque o `prontidao.py` CITA o nome do modulo na
    prosa do comentario que explica por que a conferencia nao entrou — casar
    prosa pegaria a explicacao em vez do codigo.
    """
    caminho = os.path.join(RAIZ, "fabrica", "prontidao.py")
    with open(caminho, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    importa = [
        a.name for n in ast.walk(arvore) if isinstance(n, ast.Import)
        for a in n.names
    ] + [
        n.module for n in ast.walk(arvore) if isinstance(n, ast.ImportFrom)
    ]
    assert "copy_secoes" not in importa, (
        "o `prontidao` voltou a importar o `copy_secoes`: a conferencia por "
        "cabecalho reprova 47 testes, e nenhuma das tres tentativas tem "
        "procedencia"
    )
    chamadas = [
        ast.unparse(n.func) for n in ast.walk(arvore) if isinstance(n, ast.Call)
    ]
    assert not any("copy_secoes" in c for c in chamadas)


def test_a_leitura_e_DELEGADA_ao_publicar__cobrado_por_AST():
    caminho = os.path.join(RAIZ, "fabrica", "copy_secoes.py")
    with open(caminho, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    chamadas = [
        ast.unparse(n.func) for n in ast.walk(arvore) if isinstance(n, ast.Call)
    ]
    assert any("ler_copy" in c for c in chamadas), (
        "o modulo nao CHAMA o publicar.ler_copy — reimplementar a "
        "classificacao criaria o segundo dono dela"
    )
    nomes = [
        t.id for n in ast.walk(arvore) if isinstance(n, ast.Assign)
        for t in n.targets if isinstance(t, ast.Name)
    ]
    assert "comentario" not in nomes, "ha um segundo dono do balde aqui"


def test_as_TRES_tentativas_e_a_medicao_VACUA_continuam_escritas():
    """Conserto sem o motivo escrito volta calado — e aqui nao houve conserto."""
    with open(os.path.join(RAIZ, "fabrica", "copy_secoes.py"),
              encoding="utf-8") as f:
        t = f.read()
    for marca, o_que in (
            ("CIRCULAR", "a medicao que autorizou a tentativa (1)"),
            ("183", "as specs sem as chaves do Studio, tentativa (2)"),
            ("SEIS falsos positivos", "os falsos positivos da tentativa (3)"),
            ("vacu", "a primeira medicao, que foi vacua"),
            ("47", "os testes que a suite reprovou"),
    ):
        assert re.search(marca, t, re.I), (
            f"saiu do modulo: {o_que} (marca {marca!r}) — e sao eles que "
            "impedem a rodada seguinte de repetir a tentativa"
        )
