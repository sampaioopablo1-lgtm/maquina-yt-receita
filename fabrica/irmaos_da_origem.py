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

**E EM 20/10 AS 15:3x ELE QUASE ME DEIXOU REPETIR UMA FAMILIA, pelo que ele
mostrava e NAO pelo que faltava.** Escrevendo o `labtreinamento-s093` eu ia usar
COMPARAR TRES ORCAMENTOS PELO PRECO QUANDO O ESCOPO DIFERE (capitulos 37 a 41 da
origem `yrWVyqQtw00`). O relato trouxe os cinco irmaos, acusou que tres nao tem o
campo, e imprimiu **tres frases de outros irmaos citando o `s010`** — as tres
dizendo que ele e *"ORDEM DE CONTRATACAO"*, *"a ORDEM do orcamento"*, *"pedir o
estudo antes do levantamento"*. Lido assim, o meu eixo parecia outro: ordem
contra comparacao de propostas.

**A narracao do PROPRIO `s010` diz o contrario, em letra:** *"Quem pede orcamento
sem levantamento recebe o escopo da instalacao inteira"* e *"O preco cai porque o
escopo encolheu, nao porque alguem negociou"*. Isto e exatamente o eixo
escopo-contra-preco. **A familia dele estava escrita na peca e ausente de tudo o
que o modulo me mostrou.**

**A causa e de PROCEDENCIA e nao de ausencia: resumo de TERCEIRO perde o eixo.**
As frases que o modulo imprimia eram de segunda mao — o irmao B descrevendo o
irmao A — e compressao feita por outro guarda o que interessava a ELE. O ramo
*"nenhum irmao CITA outro pelo nome"*, que manda ler a copy inteira, **nao
disparou justamente porque havia citacoes**: quanto mais os irmaos se citam,
menos o modulo manda ler a fonte.

**E O RELATO PROMETIA A PROSA E NUNCA A IMPRIMIA — `irmaos()` a calculava e
`relato()` a jogava fora.** A linha de ATENCAO dizia, em letra, *"leia a PROSA
abaixo, que e onde a geracao antiga a registrava"*, e abaixo nao havia prosa
nenhuma: so as citacoes de segunda mao. Medido nas specs de **SHORT SOLTO** com
copy, que sao a populacao que este modulo serve:

| | |
|---|---|
| specs de short solto com copy | **240** |
| COM o campo da familia | **69** |
| **SEM** o campo | **171** |
| dessas, com bloco de prosa | **171 de 171** |
| para quantas o `relato` imprimia esse bloco | **ZERO** |

E no caso desta rodada o bloco carregava a familia em letra: o
`AVISO SOBRE OS NUMEROS` do `s010` diz *"a ORDEM de contratacao nao envelhece, e
e ela que este short carrega"*. A frase prometida existia e nao chegava a saida —
a mesma forma da nota da rota de 13:2x (calculada e descartada) e do `quadro` que
o `contagem_de_cenas` jogava fora as 03:2x.

**E A NARRACAO E A FONTE DE PRIMEIRA MAO, e ela acrescenta o que a prosa NAO
tem:** o `AVISO` do `s010` fala de *ordem*, e a narracao dele fala de
*"o preco cai porque o escopo encolheu"* — que e o eixo que eu ia repetir. Logo a
prosa sozinha nao bastava: ela e o resumo que o autor fez da PROPRIA peca, e
resumo tambem comprime.

**E O NUMERO QUE EU IA RELATAR ESTAVA ERRADO, e quem me pegou foi o teste que eu
escrevi nesta mesma rodada.** Eu havia medido *"66 de 379 specs em que so o
titulo sobra"* e ia escrever isso aqui: **as 66 eram PACOTES**, que este modulo
nem considera irmao (`irmaos()` exige `longo` vazio). Na populacao certa esse
numero e **ZERO** — nenhum short solto fica so com o titulo, porque todos tem
bloco de prosa. Era o §3.8 no meu proprio numero: contei outra populacao e ia
apresenta-la como a do defeito.

**Consertado:** o irmao SEM o campo entrega a `narracao` dele, cena por cena e
**sem truncar** (truncar por tamanho foi o que quase cortou a frase que salvou o
`s035`), marcada como PRIMEIRA mao; as citacoes continuam saindo, agora marcadas
como SEGUNDA. Irmao COM o campo **nao** recebe esse bloco: o campo e o dono
quando existe, e imprimir as duas coisas criaria o segundo dono da familia.

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


def _narracao(spec: dict) -> list:
    """A narracao do short do irmao, cena por cena — a fonte de PRIMEIRA mao.

    Ela e o que foi AO AR, e por isso nao depende de o autor ter escrito campo
    nem bloco de prosa. Medido em 20/10: 66 das 379 specs de short com copy nao
    tem campo nem prosa, e as 66 tem narracao.
    """
    saida = []
    for c in (spec.get("short") or []):
        nar = (c.get("nar") or "").strip()
        if nar:
            saida.append(nar)
    return saida


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
            # PRIMEIRA mao: o que a peca do irmao de fato fala. Sem isto o
            # irmao de geracao antiga entregava so o titulo (20/10, 15:3x).
            "narracao": _narracao(d),
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
            " leia a PROSA abaixo, que e onde a geracao antiga a registrava."
            " **E leia a NARRACAO deles, que vai logo abaixo: ela e de PRIMEIRA"
            " mao.** Frase de irmao citando irmao e resumo de TERCEIRO, e"
            " compressao feita por outro guarda o eixo que interessava a ELE —"
            " foi assim que o `s010` apareceu tres vezes como *ordem de"
            " contratacao* enquanto a propria narracao dele dizia *o preco cai"
            " porque o escopo encolheu* (20/10, 15:3x).")
        for i in todos:
            if i["tem_campo_familia"]:
                # o campo e o DONO quando existe; imprimir a narracao ao lado
                # dele criaria o segundo dono da familia.
                continue
            if not i["narracao"]:
                linhas.append(
                    f"    [{i['pacote']} | PRIMEIRA mao] sem narracao na spec —"
                    " aqui so o titulo sobra mesmo, e a copy inteira e o"
                    " caminho.")
                continue
            for nome_bloco, texto in sorted(i["prosa"].items()):
                linhas.append(
                    f"    [{i['pacote']} | PROSA '{nome_bloco}'] o bloco"
                    " INTEIRO, que a linha acima promete e que o relato nao"
                    " imprimia ate 20/10:")
                for par in texto.split("\n\n"):
                    par = " ".join(par.split())
                    if par:
                        linhas.append(f"      > {par}")
            linhas.append(
                f"    [{i['pacote']} | NARRACAO, primeira mao] o que a peca dele"
                " FALA, cena por cena, sem truncar:")
            for n in i["narracao"]:
                linhas.append(f"      . {n}")
        nomes = [i["pacote"] for i in todos]
        achou_mencao = False
        for i in todos:
            copy_i = i.get("_copy", "")
            outros = [n for n in nomes if n != i["pacote"]]
            for frase in frases_que_citam_irmao(copy_i, outros):
                achou_mencao = True
                linhas.append(
                    f"    [{i['pacote']} CITA outro irmao | SEGUNDA mao]"
                    f" {frase}")
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
