# -*- coding: utf-8 -*-
"""O portao dizia "sem comentario fixado" e NUNCA podia dizer.

MEDIDO em 19/10 as 20:3x, na copy que eu mesmo escrevi nesta hora. Entreguei a
copy do `labtreinamento-s087` sem a secao `## COMENTARIO FIXADO` e sem a
`## HASHTAGS`, e o portao `copy` reprovou com UM problema — "sem hashtags" — e
deu VERDE no comentario, que tambem faltava. O `comentario` do
`publicar.ler_copy` e um balde PEGA-TUDO: a primeira secao que nao casa com
licenca, capitulos, hashtags nem tags cai nele. Sem a secao propria, quem foi
para la foi o bloco `## CONFIGURACOES DO STUDIO`, isto e, `privacyStatus:
public` e companhia iriam ao ar como COMENTARIO FIXADO do video.

Falha PERMISSIVA, a mesma classe da mira que parou de conferir por seis pecas.

E A MINHA PRIMEIRA MEDICAO DISTO FOI VACUA: eu varri 326 specs chamando
`ler_copy(texto)` — assinatura errada — dentro de um `except Exception:
continue`, as 326 levantaram, e o contador ficou em zero. Depois de corrigir a
assinatura ela ainda levantava, no placeholder `{TRILHA}`. "Zero vazamentos"
nao mediu nada, e e por isso que este arquivo tem piso de specs e cobra os dois
lados.
"""
import ast
import glob
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import copy_secoes as CS  # noqa: E402

PISO_DE_SPECS = 150


def _specs_com_copy():
    fora = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            with open(p, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        t = sp.get("copy")
        if isinstance(t, str) and "## DESCRICAO" in t.upper():
            fora.append((os.path.basename(p), sp))
    return fora


def test_a_varredura_sai_do_DISCO_e_reprova_se_encolher():
    """Vacuidade e o defeito do 743 em forma de glob."""
    specs = _specs_com_copy()
    assert len(specs) >= PISO_DE_SPECS, (
        f"so {len(specs)} specs com copy no disco — abaixo do piso de "
        f"{PISO_DE_SPECS} este arquivo passa por VACUIDADE e nao mede nada"
    )


def test_o_titulo_da_secao_do_COMENTARIO_nao_varia_no_disco():
    """E a procedencia de detectar por CABECALHO em vez de por conteudo.

    Para a LICENCA isso seria errado — a medicao de 25/08 que esta no
    `ler_copy` diz que o titulo dela muda de spec e de idioma. Para esta, 322
    de 322 usam um cabecalho que comeca por COMENT, e e esse numero que
    autoriza a conferencia. Se ele cair, a conferencia perde a procedencia.
    """
    specs = _specs_com_copy()
    declaram = [n for n, sp in specs if CS.declaradas(sp["copy"])["COMENT"]]
    assert len(declaram) == len(specs), (
        "specs que NAO declaram a secao do comentario: "
        + ", ".join(n for n, _ in specs if n not in set(declaram))
        + " — se isso passar a existir no acervo, releia a nota em vez de "
          "afrouxar a conferencia"
    )


def test_o_acervo_NAO_vaza_hoje__e_falha_se_passar_a_vazar():
    """O buraco e LATENTE, e e isso que justifica o portao em vez da suite."""
    specs = _specs_com_copy()
    vazam = [n for n, sp in specs if CS.comentario_vazado(sp)["vazado"]]
    assert not vazam, (
        "o acervo passou a VAZAR comentario fixado em: " + ", ".join(vazam)
        + " — aqui o certo e reler a nota: com o acervo vazando, a conferencia "
          "deixa de reprovar so a peca quebrada e passa a reprovar o parque, "
          "que e o argumento pelo qual o `mira.py` nao e portao"
    )


def _quebra(sp):
    """Devolve a mesma spec sem a secao do comentario. Os DOIS lados."""
    t = sp["copy"]
    i = t.index("## COMENTARIO FIXADO")
    j = t.index("## TAGS", i)
    q = dict(sp)
    q["copy"] = t[:i] + t[j:]
    return q


def _uma_spec_com_as_duas_secoes():
    for n, sp in _specs_com_copy():
        t = sp["copy"]
        if "## COMENTARIO FIXADO" in t and "## TAGS" in t and (
                t.index("## TAGS") > t.index("## COMENTARIO FIXADO")):
            return n, sp
    raise AssertionError(
        "nenhuma spec do disco tem a secao do comentario ANTES da de tags — "
        "sem ela a contraprova nao se monta e este arquivo nao mede nada"
    )


def test_CONTRAPROVA_sem_a_secao_o_instrumento_ACUSA():
    _, sp = _uma_spec_com_as_duas_secoes()
    v = CS.comentario_vazado(_quebra(sp))
    assert v["vazado"], "retirada a secao, o instrumento tinha de acusar"
    assert v["comentario"], (
        "e o que ele acusa e o balde CHEIO: comentario vazio nao prova o "
        "pega-tudo, prova so a ausencia"
    )
    assert not v["tem_secao"]


def test_CONTRAPROVA_no_outro_sentido_com_a_secao_ele_CALA():
    """Sem este, um instrumento que acusa sempre passaria."""
    _, sp = _uma_spec_com_as_duas_secoes()
    v = CS.comentario_vazado(sp)
    assert v["tem_secao"] and not v["vazado"]
    assert v["comentario"], "a secao declarada tem de chegar ao comentario"


def test_a_leitura_e_DELEGADA_ao_publicar__cobrado_por_AST():
    """Refazer a classificacao de secoes aqui criaria o SEGUNDO dono dela.

    Por AST e nao por texto porque o docstring do modulo CITA o ramo
    `elif not comentario` para se explicar, e casar prosa pegaria a
    explicacao em vez do codigo.
    """
    caminho = os.path.join(RAIZ, "fabrica", "copy_secoes.py")
    with open(caminho, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    chamadas = [
        ast.unparse(n.func) for n in ast.walk(arvore)
        if isinstance(n, ast.Call)
    ]
    assert any("ler_copy" in c for c in chamadas), (
        "o modulo nao CHAMA o publicar.ler_copy — se ele reimplementa a "
        "classificacao de secoes, os dois donos divergem em silencio"
    )
    # e nao pode ter um segundo classificador: nenhuma atribuicao a uma
    # variavel chamada `comentario` dentro deste modulo.
    nomes = [
        t.id for n in ast.walk(arvore) if isinstance(n, ast.Assign)
        for t in n.targets if isinstance(t, ast.Name)
    ]
    assert "comentario" not in nomes, (
        "ha um `comentario = ...` aqui: isto e o segundo dono do balde"
    )


def test_o_PORTAO_esta_fiado__por_PROPRIEDADE_sobre_o_disco():
    """Nomear a `s087` seria identidade onde ha propriedade (743/753/761)."""
    _, sp = _uma_spec_com_as_duas_secoes()
    quebrada = _quebra(sp)
    quebrada["slug"] = "zz-teste-balde-pega-tudo"
    quebrada["pacote"] = "zz-teste-balde-pega-tudo"
    destino = os.path.join(
        RAIZ, "fabrica", "specs", "zz-teste-balde-pega-tudo.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(quebrada, f, ensure_ascii=False)
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "fabrica", "prontidao.py"),
             destino],
            capture_output=True, text=True, cwd=RAIZ, timeout=1800,
        )
        saida = r.stdout + r.stderr
    finally:
        os.remove(destino)
    assert "COMENTARIO FIXADO" in saida, (
        "o portao `copy` nao cobra a ausencia da secao — ele pergunta se o "
        "balde esta cheio, e o pega-tudo sempre o enche:\n" + saida[-1500:]
    )


def test_a_licao_da_medicao_VACUA_continua_escrita():
    """Conserto sem o motivo escrito volta calado."""
    caminho = os.path.join(RAIZ, "fabrica", "copy_secoes.py")
    with open(caminho, encoding="utf-8") as f:
        t = f.read()
    assert re.search(r"VAC[UÚ]A|vacu", t, re.I), (
        "a nota de que a PRIMEIRA medicao disto foi vacua saiu do modulo — "
        "e ela e a licao, nao o conserto"
    )
    assert "{TRILHA}" in t, (
        "o motivo de haver substituicao de placeholder saiu do modulo: foi "
        "ele que fez a varredura levantar em silencio"
    )
