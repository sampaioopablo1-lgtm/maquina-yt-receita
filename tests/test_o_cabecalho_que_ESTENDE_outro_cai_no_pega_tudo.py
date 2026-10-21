"""Cabecalho que ESTENDE outro da mesma copy — 21/10 as 04:3x.

Escrevendo a `epomeno-epipedo-s082` eu deixei um `## COMENTARIO FIXADO FIM`
solto na copy. Para o `publicar.ler_copy` isso e uma SECAO, e o comentario
fixado e um balde PEGA-TUDO (medido em 20/10 as 20:3x): o bloco errado podia ir
ao ar como comentario do video. **Peguei relendo, nao por instrumento.**

E E O UNICO DISCRIMINADOR QUE SOBREVIVEU, de CINCO tentados — as tres de 20/10
(cabecalho `COMENT*`, que TRADUZ; chaves do Studio, ausentes por geracao; forma
das linhas, com seis falsos positivos) e as DUAS desta rodada: prefixo CRU
(325 acusacoes, todas pares legitimos) e frequencia (acusa traducao legitima).

O que faz este funcionar e comparar a copy COM ELA MESMA — o par (base,
extensao) e interno, logo nao depende de idioma — e ter o conjunto de sufixos
OBSERVADO no disco: ele acusa ZERO das copies do acervo.
"""
import ast
import collections
import glob
import inspect
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as ADR   # noqa: E402
import copy_secoes as CS        # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "copy_secoes.py")


def _copies():
    saida = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        c = d.get("copy") or ""
        if c:
            saida.append((d.get("pacote") or os.path.basename(p)[:-5], c))
    return saida


def test_a_varredura_nao_passa_por_VACUIDADE():
    assert len(_copies()) >= 200, (
        "so %d copies no disco; abaixo de 200 este arquivo passa por vacuidade"
        % len(_copies()))


def test_ele_acusa_ZERO_do_acervo():
    """Detector que inventa achado e pior que nao ter detector (725). O acervo
    e a prova: se ele acusar alguem, o conjunto de sufixos esta incompleto."""
    acusadas = [(pac, CS.prefixo_colidido(c)) for pac, c in _copies()]
    acusadas = [(p, r) for p, r in acusadas if r]
    assert not acusadas, (
        "ele acusou %d copies do acervo: %r. O conjunto `SUFIXOS_LEGITIMOS` e "
        "OBSERVADO; se uma copy legitima passou a colidir, o sufixo novo entra "
        "na constante COM a medida ao lado — nunca o teste e afrouxado"
        % (len(acusadas), acusadas[:3]))


def test_ele_ACUSA_o_meu_erro_desta_rodada():
    """Contraprova no outro sentido: sem ela, acusar nada passaria por este
    arquivo."""
    ruim = ("# x\n\n## COMENTARIO FIXADO\nabc\n\n"
            "## COMENTARIO FIXADO FIM\ndef\n")
    r = CS.prefixo_colidido(ruim)
    assert len(r) == 1, "o caso real desta rodada nao foi acusado: %r" % r
    assert r[0]["sufixo"] == "FIM"
    assert r[0]["base"] == "COMENTARIO FIXADO"
    assert r[0]["extensao"] == "COMENTARIO FIXADO FIM"


def test_os_pares_LEGITIMOS_nao_sao_acusados():
    bom = ("# x\n\n## TITULO\na\n\n## TITULO SHORT\nb\n\n"
           "## AVISO\nc\n\n## AVISO SOBRE OS NUMEROS\nd\n")
    assert CS.prefixo_colidido(bom) == [], (
        "os dois pares OBSERVADOS do acervo foram acusados")
    # e em outro idioma, porque a comparacao e interna e nao depende dele
    indo = "# x\n\n## JUDUL\na\n\n## JUDUL SHORT\nb\n"
    assert CS.prefixo_colidido(indo) == [], (
        "o par indonesio foi acusado: a comparacao deixou de ser interna")


def test_o_PREFIXO_CRU_de_fato_erra_e_isso_e_RECONFERIDO():
    """A medida que justifica a guarda dos sufixos: sem ela, 325 acusacoes.
    Numero medido que ninguem reconfere envelhece calado (753)."""
    pares = 0
    sufixos = collections.Counter()
    for _, c in _copies():
        hs = [h.strip() for h in re.findall(r"^##\s+(.+?)\s*$", c, re.M)]
        for a in hs:
            for b in hs:
                if a != b and b.startswith(a + " "):
                    pares += 1
                    sufixos[b[len(a) + 1:].strip().upper()] += 1
    assert pares >= 200, (
        "o prefixo cru passou a achar so %d pares; abaixo disso a guarda dos "
        "sufixos deixa de ser necessaria e esta nota se rele" % pares)
    assert set(sufixos) <= set(s.upper() for s in CS.SUFIXOS_LEGITIMOS), (
        "apareceu sufixo de prefixo-colisao que NAO esta na constante: %r. "
        "Ou e erro de digitacao numa copy, ou e secao legitima nova — e nos "
        "dois casos alguem tem de OLHAR, nao mover o numero"
        % (set(sufixos) - set(s.upper() for s in CS.SUFIXOS_LEGITIMOS)))


def test_a_FREQUENCIA_nao_servia_como_discriminador():
    """O segundo que eu tentei nesta rodada: cabecalho que aparece numa copy so.
    Ele acusa traducao legitima, e o teste guarda isso para ninguem o readotar."""
    freq = collections.Counter()
    for _, c in _copies():
        for h in set(h.strip() for h in re.findall(r"^##\s+(.+?)\s*$", c, re.M)):
            freq[h] += 1
    unicos = [h for h, n in freq.items() if n == 1]
    assert len(unicos) >= 5, (
        "so %d cabecalhos de ocorrencia unica; sem eles o arquivo nao mostra "
        "por que a frequencia nao serve" % len(unicos))
    # e entre eles tem de haver cabecalho LEGITIMO — traducao ou secao ad-hoc
    legitimo = [h for h in unicos
                if "KOMENTARZ" in h.upper() or "JUDUL" in h.upper()
                or h.upper().startswith("MIRA")]
    assert legitimo, (
        "nenhum dos cabecalhos de ocorrencia unica e reconhecivelmente "
        "legitimo (%r) — sem isso a frequencia pareceria um discriminador bom"
        % unicos[:8])


def test_o_RELATO_carrega_a_linha_e_o_instrumento_esta_na_PASSADA():
    """Calculado e descartado pelo chamador e a classe dos layouts mortos."""
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    fn = [n for n in ast.walk(arvore)
          if isinstance(n, ast.FunctionDef) and n.name == "relato"][0]
    chamadas = [c.func.id for c in ast.walk(fn)
                if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)]
    assert "prefixo_colidido" in chamadas, (
        "o `relato` nao chama `prefixo_colidido`")
    assert "copy_secoes" in ADR.INSTRUMENTOS, (
        "o `copy_secoes` nao esta na passada do `antes_do_render`: %r"
        % (ADR.INSTRUMENTOS,))
    # os DOIS ramos saem
    _, sp = _spec_real()
    bom = sp["copy"]
    # o defeito REAL: um cabecalho a mais no fim de uma copy completa
    cab = CS.cabecalhos(bom)
    base = next((h for h in cab if "COMENT" in h.upper()), cab[0])
    ruim = bom + "\n## %s FIM\nsobra\n" % base
    assert "CABECALHO COLIDIDO" in _relato_de(ruim), (
        "o ramo que ACUSA nao sai no relato")
    assert "nenhum cabecalho ESTENDE" in _relato_de(bom), (
        "o ramo que diz que esta limpo nao sai — calar nao e dizer que esta ok")


def _spec_real():
    """Uma spec de short solto DERIVADA do disco — o `relato` chama o
    `publicar.ler_copy`, que SAI com `SystemExit` numa copy mínima, logo a
    fixture tem de ser uma copy de VERDADE. E isso e mais fiel: foi assim que o
    defeito ocorreu, acrescentando um cabecalho a uma copy completa."""
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short") or not (d.get("copy") or ""):
            continue
        if CS.prefixo_colidido(d["copy"]):
            continue
        return p, d
    raise AssertionError("perdi a ancora: nenhuma spec de short solto limpa")


def _relato_de(copy_txt):
    """Grava numa COPIA, com a spec real por base, para nao tocar o disco."""
    import tempfile
    _, sp = _spec_real()
    sp = dict(sp)
    sp["copy"] = copy_txt
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        json.dump(sp, f, ensure_ascii=False)
        caminho = f.name
    try:
        return CS.relato(caminho)
    finally:
        os.unlink(caminho)


def test_o_LIMITE_e_as_QUATRO_falhas_continuam_escritos():
    doc = inspect.getdoc(CS.prefixo_colidido) or ""
    assert "FONTES E RESSALVAS" in doc, (
        "o LIMITE declarado saiu do docstring: uma copy com `FONTES` e "
        "`FONTES E RESSALVAS` juntas SERIA acusada, e e por isso que isto "
        "informa em vez de reprovar")
    assert "325" in doc, "a medida do prefixo cru saiu do docstring"
    for marca in ("frequencia", "725", "20:3x"):
        assert marca in doc, (
            "a marca %r saiu do docstring; sem ela a rodada seguinte readota um "
            "dos quatro discriminadores que falharam" % marca)
    fonte = open(FONTE, encoding="utf-8").read()
    assert "SUFIXOS_LEGITIMOS" in fonte and "MEDIDOS" in fonte, (
        "a procedencia do conjunto de sufixos saiu do modulo")
