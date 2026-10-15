"""Os irmaos de uma origem, e o que deles SERVE de comparador de familia.

**Aprendizado 776, `alto`, medido em 15/10 as 12:2x, escrevendo o
`epomeno-epipedo-s035`.** Eu escolhi os capitulos 59 a 62 da origem `eimuyGaCor8`
— o limiar ser RELATIVO e nao linha absoluta — que e o achado mais forte daquele
trecho. **Ja era a familia do `epomeno-epipedo-s023`**, da MESMA origem: o titulo
curto dele e, literalmente, *"To orio den metraei an zeis"*.

**E o que me pegou foi ler o TITULO, nao um portao nem um campo.** Os dois irmaos
(`s001` e `s023`) sao de geracao ANTERIOR e **nenhum dos dois tem
`## FAMILIA DE ENTRADA ERRADA`** — o campo que eu usaria para comparar nao existe
neles. A regra (f) manda nao repetir familia, e a forma como eu a cumpro
(comparar o campo) **falha em silencio** quando o irmao nao o tem: ausencia de
campo lida como ausencia de familia.

**E o `segundo_angulo.nao_mencionados` NAO pega isto**, e e importante dizer por
que: ele compara CAPITULOS, e capitulo livre nao significa familia livre. Aqui o
68 estava livre e a familia dos 59 a 62 nao estava — sao perguntas diferentes.

**Pior: a geracao antiga registrou a familia em PROSA, em outro lugar.** O `s023`
tem um bloco *"O QUE EU NAO LEVEI"* que nomeia a familia do `s001` ("essa familia
JA foi usada pelo `s001`") e declara de quais capitulos ele mesmo saiu. Ou seja, a
informacao existia — em texto corrido, num cabecalho que nenhum codigo meu lia.

**O que este modulo faz:** para cada irmao devolve o titulo curto, a familia
QUANDO o campo existe, as notas de prosa que costumam carrega-la, e os capitulos
que ele declara ter usado. E quando o campo falta, `relato` **DIZ que falta** e
manda comparar pelo titulo e pela prosa, em vez de devolver vazio — porque vazio
se le como "nao ha familia", que foi exatamente o erro.

**O que ele NAO faz:** decidir se duas familias sao a mesma. Isso e leitura, e
nenhum limiar de similaridade de string distingue "o limiar e relativo" de "o
indicador mede renda e nao patrimonio" — as duas frases falam do mesmo limiar.
Ele poe o material na mesa; quem compara sou eu.
"""
import glob
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cabecalhos onde a familia pode estar escrita, em ordem de forca.
CAMPO_FAMILIA = "FAMILIA DE ENTRADA ERRADA"
# A geracao antiga nao tinha o campo e registrava em prosa nestes blocos.
BLOCOS_DE_PROSA = ("O QUE EU NAO LEVEI", "AVISO SOBRE OS NUMEROS", "AVISO")


def _secao(copy: str, nome: str) -> str:
    m = re.search(r"^##\s*" + re.escape(nome) + r"\s*$\n(.*?)(?=^##\s|\Z)",
                  copy, re.M | re.S)
    return (m.group(1).strip() if m else "")


def _titulo_curto(copy: str) -> str:
    m = re.search(r"^##\s*TITULO SHORT\s*$\n+(.+)$", copy, re.M)
    return m.group(1).strip() if m else ""


def _capitulos_declarados(copy: str) -> list:
    """Numeros que a copy diz ter usado — a geracao antiga os escreve em prosa."""
    achados = set()
    for m in re.finditer(r"capitulos?\s+(\d{1,3})\s*a\s*(\d{1,3})", copy, re.I):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b and b - a < 60:
            achados.update(range(a, b + 1))
    for m in re.finditer(r"[Cc]apitulo\s+(\d{1,3})\b", copy):
        achados.add(int(m.group(1)))
    return sorted(achados)


def frases_que_citam_irmao(copy: str, pacotes: list) -> list:
    """As frases da copy que NOMEIAM outro pacote de short.

    E o sinal mais direto que a geracao antiga deixou: o `s023` escreve
    *"essa familia JA foi usada pelo `s001`"* no meio de um bloco de prosa, e foi
    isso que salvou o `s035`. Truncar o bloco por tamanho cortava exatamente esta
    frase, entao o modulo procura a MENCAO em vez de imprimir o bloco inteiro.
    """
    alvos = [re.escape(p.split("-")[-1]) for p in pacotes]
    if not alvos:
        return []
    padrao = re.compile(r"(?<![\w-])`?(?:" + "|".join(alvos) + r")`?(?![\w-])")
    saida = []
    for frase in re.split(r"(?<=[.;!?])\s+", " ".join(copy.split())):
        if padrao.search(frase) and len(frase) > 20:
            saida.append(frase.strip())
    return saida


def irmaos(origem: str, raiz=None) -> list:
    """Um dict por spec de short que declara `longo_existente == origem`."""
    raiz = raiz or RAIZ
    saida = []
    for f in sorted(glob.glob(os.path.join(raiz, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo_existente") != origem or d.get("longo"):
            continue
        copy = d.get("copy", "") or ""
        familia = _secao(copy, CAMPO_FAMILIA)
        saida.append({
            "pacote": d.get("pacote", os.path.basename(f)[:-5]),
            "titulo_curto": _titulo_curto(copy),
            "familia": familia,
            "tem_campo_familia": bool(familia),
            "prosa": {b: _secao(copy, b) for b in BLOCOS_DE_PROSA
                      if _secao(copy, b)},
            "capitulos_declarados": _capitulos_declarados(copy),
            "_copy": copy,
        })
    return saida


def sem_campo(origem: str, raiz=None) -> list:
    return [i["pacote"] for i in irmaos(origem, raiz)
            if not i["tem_campo_familia"]]


def relato(origem: str, raiz=None, excluir=()) -> str:
    todos = [i for i in irmaos(origem, raiz) if i["pacote"] not in excluir]
    if not todos:
        return (f"IRMAOS de {origem}: NENHUM. Origem virgem — a regra (f) nao tem"
                " contra o que comparar nesta origem, mas o CANAL tem: confira as"
                " familias das outras pecas do canal do mesmo dia.")
    linhas = [f"IRMAOS de {origem}: {len(todos)}."]
    faltam = []
    for i in todos:
        linhas.append(f"  {i['pacote']} — titulo curto: {i['titulo_curto']!r}")
        if i["tem_campo_familia"]:
            linhas.append("    familia (campo): "
                          + " ".join(i["familia"].split())[:220])
        else:
            faltam.append(i["pacote"])
            linhas.append("    familia (campo): **AUSENTE** — geracao anterior")
        if i["capitulos_declarados"]:
            cs = i["capitulos_declarados"]
            linhas.append(f"    capitulos que ele declara: {cs[0]} a {cs[-1]}"
                          f" ({len(cs)} citados)")
    if faltam:
        linhas.append(
            "  ATENCAO: " + ", ".join(faltam) + " NAO tem o campo"
            f" `## {CAMPO_FAMILIA}`. **Ausencia de campo NAO e ausencia de"
            " familia** — foi exatamente assim que eu quase repeti a familia do"
            " `epomeno-epipedo-s023` em 15/10 (776). Compare pelo TITULO CURTO e"
            " leia a PROSA abaixo, que e onde a geracao antiga a registrava.")
        nomes = [i["pacote"] for i in todos]
        achou_mencao = False
        for i in todos:
            copy_i = i.get("_copy", "")
            outros = [n for n in nomes if n != i["pacote"]]
            for frase in frases_que_citam_irmao(copy_i, outros):
                achou_mencao = True
                linhas.append(f"    [{i['pacote']} CITA outro irmao] {frase}")
        if not achou_mencao:
            linhas.append(
                "    nenhum irmao CITA outro pelo nome — entao o titulo curto e"
                " o unico comparador que sobra, e leia a copy do irmao inteira"
                " antes de escrever.")
    linhas.append(
        "  (isto NAO decide se duas familias sao a mesma: nenhum limiar de"
        " string distingue duas frases sobre o MESMO limiar. Poe o material na"
        " mesa; a comparacao e leitura.)")
    linhas.append(
        "  (e capitulo livre NAO e familia livre: o `segundo_angulo` compara"
        " CAPITULOS, e sao perguntas diferentes.)")
    return "\n".join(linhas)


if __name__ == "__main__":
    import sys
    print(relato(sys.argv[1] if len(sys.argv) > 1 else "eimuyGaCor8"))
