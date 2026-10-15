"""776, `alto`, medido em 15/10 as 12:2x, escrevendo o `epomeno-epipedo-s035`.

Eu escolhi os capitulos 59 a 62 da origem `eimuyGaCor8` — o limiar ser RELATIVO e
nao linha absoluta de sobrevivencia — e **ja era a familia do
`epomeno-epipedo-s023`**, da MESMA origem, cujo titulo curto e literalmente
*"To orio den metraei an zeis"*.

**Tres coisas falharam juntas, e as tres vao travadas aqui:**

1. **O campo de familia NAO EXISTE na geracao antiga.** Nem o `s001` nem o `s023`
   tem `## FAMILIA DE ENTRADA ERRADA`. A forma como eu cumpro a regra (f) —
   comparar o campo — **falha em silencio** nesse caso: ausencia de campo lida
   como ausencia de familia. Mesma assinatura do corpus atrasado (726) e da trava
   de titulo (773): permissiva.

2. **Capitulo livre NAO e familia livre.** O `segundo_angulo.nao_mencionados`
   compara CAPITULOS, e disse 73 livres de 87 — verdade, e irrelevante para a
   pergunta. O capitulo 68 estava livre e a familia dos 59 a 62 nao estava.

3. **A geracao antiga registrou a familia em PROSA**, dentro de um bloco que
   nenhum codigo meu lia: o `s023` escreve *"Essa familia JA foi usada pelo
   `s001` deste canal"* no meio do `## AVISO SOBRE OS NUMEROS`. **Truncar o bloco
   por tamanho cortava exatamente essa frase** — a primeira versao deste modulo
   imprimia 400 caracteres e a perdia. Por isso ele procura a MENCAO a outro
   pacote em vez de imprimir o bloco.

**E um erro MEU dentro da propria peca, corrigido ANTES de publicar:** eu escrevi
no descarte que a familia dos capitulos 63 a 65 ("o limiar nao e criterio de
beneficio") estava *livre*. **Nao esta** — o `s023` cobre 59 a **67** e carrega
esse ponto explicitamente. Conferi lendo a copy do irmao, nao contando capitulos.

**O que o modulo NAO faz, e vai dito no proprio relato:** decidir se duas
familias sao a mesma. Nenhum limiar de similaridade de string distingue "o limiar
e relativo" de "o indicador mede renda e nao patrimonio" — as duas frases falam
do MESMO limiar, com palavras parecidas, e sao perguntas diferentes.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import irmaos_da_origem as io  # noqa: E402
import segundo_angulo as sa  # noqa: E402

ORIGEM = "eimuyGaCor8"
SEM_CAMPO = ["epomeno-epipedo-s001", "epomeno-epipedo-s023"]
TITULO_QUE_SALVOU = "Το όριο δεν μετράει αν ζεις"


def test_os_dois_irmaos_antigos_NAO_tem_o_campo_de_familia():
    """Sem este fato o aprendizado nao existe — e com ele a trava e permissiva."""
    faltam = io.sem_campo(ORIGEM)
    for p in SEM_CAMPO:
        assert p in faltam, (
            f"{p} ganhou o campo `## FAMILIA DE ENTRADA ERRADA`. Isso e bom, e"
            " esta nota tem de ser RELIDA em vez de reaproveitada: o modulo"
            " nasceu para o caso em que ele falta.")


def test_o_titulo_curto_do_s023_E_a_familia_que_eu_ia_repetir():
    irs = {i["pacote"]: i for i in io.irmaos(ORIGEM)}
    assert irs["epomeno-epipedo-s023"]["titulo_curto"] == TITULO_QUE_SALVOU
    assert not irs["epomeno-epipedo-s023"]["tem_campo_familia"]


def test_CAPITULO_livre_nao_e_FAMILIA_livre__a_contraprova_do_776():
    """O 68 estava livre pelo `segundo_angulo` E a familia dos 59 a 62 nao."""
    nm = sa.nao_mencionados(ORIGEM)
    livres = nm["nao_mencionados"]
    assert len(livres) > 60, (
        "o instrumento de CAPITULO dizia muita coisa livre — e e verdade, e"
        " responde outra pergunta")
    # e o irmao que ja usava aquela familia esta ali, de pe
    assert "epomeno-epipedo-s023" in nm["shorts"]


def test_o_relato_AVISA_que_ausencia_de_campo_nao_e_ausencia_de_familia():
    t = io.relato(ORIGEM)
    assert "AUSENTE" in t
    assert "Ausencia de campo NAO e ausencia de familia" in t
    assert "776" in t, "a procedencia vai no relato"
    assert "capitulo livre NAO e familia livre" in t.replace("**", "")


def test_o_relato_SURFACE_a_frase_de_PROSA_que_cita_o_irmao():
    """Era a frase que a primeira versao truncava, e e o sinal mais direto."""
    t = io.relato(ORIGEM)
    assert "s023 CITA outro irmao" in t
    assert "JA foi usada pelo" in t, (
        "a mencao em prosa voltou a ser cortada — foi exatamente isso que o"
        " truncamento de 400 caracteres fazia")


def test_frases_que_citam_irmao_nao_casa_pedaco_de_palavra():
    """Contraprova: `s0011` e `xs001` nao sao `s001`."""
    assert io.frases_que_citam_irmao(
        "A familia veio do pacote s0011 e nao importa aqui de verdade.",
        ["canal-s001"]) == []
    achou = io.frases_que_citam_irmao(
        "Esta familia JA foi usada pelo `s001` deste canal, e por isso saiu.",
        ["canal-s001"])
    assert len(achou) == 1


def test_o_modulo_DIZ_que_nao_compara_familia_por_string():
    """E confere CODIGO, nao prosa.

    **SEGUNDA vez em duas rodadas que um teste meu casa PROSA:** na rodada das
    11:1x o `test_o_modulo_NAO_importa_nada_de_banco` pegou a palavra
    `execute_sql` no DOCSTRING do `janela_sem_banco`, que a nomeia justamente
    para explicar o bloqueio; aqui a primeira versao pegou "similaridade" no
    docstring, que a nomeia para RECUSA-LA. **Nomear uma coisa e o contrario de
    depender dela**, e a forma certa e varrer a arvore com os docstrings
    removidos.
    """
    import ast
    t = io.relato(ORIGEM)
    assert "NAO decide se duas familias sao a mesma" in t
    arvore = ast.parse((RAIZ / "fabrica" / "irmaos_da_origem.py").read_text())
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            no.body = [x for x in no.body
                       if not (isinstance(x, ast.Expr)
                               and isinstance(x.value, ast.Constant)
                               and isinstance(x.value.value, str))]
    codigo = ast.unparse(arvore)
    for proibido in ("SequenceMatcher", "difflib", "ratio", "fuzz"):
        assert proibido not in codigo, (
            f"{proibido}: comparar familia por string e o criterio inventado que"
            " o docstring recusa")
    # e a prosa TEM de nomear a recusa, senao ela nao esta declarada
    assert "similaridade" in (RAIZ / "fabrica"
                              / "irmaos_da_origem.py").read_text()


def test_origem_virgem_DIZ_para_onde_ir_em_vez_de_calar():
    t = io.relato("nao-existe-este-id")
    assert "NENHUM" in t and "CANAL" in t


def test_a_spec_nova_CORRIGIU_o_descarte_que_eu_escrevi_errado():
    """Eu chamei de "livre" a familia dos capitulos 63 a 65, que o `s023` usa."""
    import json
    d = json.loads((RAIZ / "fabrica" / "specs"
                    / "epomeno-epipedo-s035.json").read_text(encoding="utf-8"))
    copy = d["copy"]
    assert "escrevi \"livre\" aqui e estava ERRADO" in copy
    assert "capitulos 59 a 67" in copy
