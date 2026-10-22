# -*- coding: utf-8 -*-
"""Os numerais que a NARRACAO fala, listados — porque eu os declarava de OLHO.

POR QUE ISTO EXISTE (21/10/2026). Toda copy desta geracao traz, no
`## AVISO SOBRE OS NUMEROS`, uma frase do tipo *"o unico numeral falado e X"* —
e essa frase eu escrevia relendo a narracao. **Na PRIMEIRA vez que a conferi
mecanicamente ela estava INCOMPLETA**, e era da peca de duas horas antes: o
`epomeno-epipedo-s083` (`Xp4jcAkYaPM`, publicado as 07:30:12Z) declara
*"τρεις"* e *"δύο"* e a narracao dele fala tambem **τρία** (*"Τρία πράγματα
μένουν πάντα έξω"*).

**O CONTEUDO estava certo e a DECLARACAO errada**, e a distincao importa: "τρία
πράγματα" conta a lista da propria peca, exatamente como os dois declarados —
nao e numero sobre o mundo e nao viola a regra (g). O que estava falso era a
palavra *"unicos"*. Declaracao que lista dois de tres e pior que declaracao
ausente, porque convida a rodada seguinte a confiar nela.

**ISTO LISTA E NAO JULGA.** Decidir se um numeral e estrutura do argumento (a
contagem dos dois caminhos) ou fato sobre o mundo (uma aliquota) e LEITURA, e
nenhum vocabulario a faz. O modulo poe os numerais na mesa; a regra (g)
continua sendo decisao de quem escreve.

**E NAO ALARMA, e o numero vem antes da decisao:** medido no disco, **56% das
specs de short solto** falam algum numeral por extenso, e os mais comuns sao
`δύο`, `duas`, `dwie`, `dois` e `três` — quase sempre a contagem de uma lista da
propria peca. Alarme que dispara na maioria das specs deixa de avisar, que e o
argumento pelo qual o `mira.py` tambem nao e portao.

**A MEDIDA E A PROPORCAO, e nao a contagem — retratado em 22/10 as 14:4x.** O
snapshot original era **144 das 259** (0,556) e o teste cobrava a contagem com
tolerancia de 15. **O acervo cresce uma spec por rodada**, logo a contagem sai
da tolerancia a cada ~16 rodadas por crescimento e nao por mudanca: em 22/10 as
14:4x ela deu **160 de 285**, e o teste reprovou mandando reler. Relido: a
proporcao foi de **0,556 para 0,561** — a propriedade que sustenta *"e comum"*
nao se mexeu. Era identidade onde havia propriedade (743/753/761), e o par
`144/259` fica como HISTORIA.

**O QUE ELE NAO VE, e por isso relato limpo NAO prova ausencia (17/10):**
numeral fora do vocabulario (ordinal, fracao escrita de outro jeito, numero em
digito — este ultimo o portao `narracao` ja conta), e numeral dentro de palavra
composta. O vocabulario e por IDIOMA e idioma sem entrada devolve lista vazia
**dizendo que nao sabe**, em vez de "nenhum numeral".

**AS FORMAS DE ARTIGO FICAM DE FORA, de proposito:** `um`/`uma` em pt,
`ένα`/`μία` em el e `jeden` em pl sao artigo na maior parte das ocorrencias, e
inclui-las acusaria quase toda frase — detector que inventa achado e pior que
nao ter detector (725). Logo "uma vez" nao e visto, e isso vai DITO.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# MEDIDO no disco: estes sao os numerais que de fato aparecem nas narracoes da
# frota, por idioma. Nao e tabela de gramatica — e o que o parque usa.
VOCABULARIO = {
    "pt": ("zero", "dois", "duas", "tres", "três", "quatro", "cinco", "seis",
           "sete", "oito", "nove", "dez", "onze", "doze", "treze", "catorze",
           "quatorze", "quinze", "vinte", "trinta", "quarenta", "cinquenta",
           "cem", "mil", "metade", "dobro", "triplo"),
    "el": ("δύο", "τρία", "τρεις", "τέσσερα", "τέσσερις", "πέντε", "έξι",
           "επτά", "εφτά", "οκτώ", "οχτώ", "εννιά", "εννέα", "δέκα", "είκοσι",
           "τριάντα", "σαράντα", "πενήντα", "εκατό", "χιλιάδες", "χιλιάδα",
           "μισό", "διπλό"),
    "pl": ("dwa", "dwie", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem",
           "dziewięć", "dziesięć", "dwadzieścia", "trzydzieści", "sto",
           "tysiąc", "połowa", "podwójnie"),
}

# Artigo na maior parte das ocorrencias — ver o docstring.
FORA_POR_SER_ARTIGO = {"pt": ("um", "uma"), "el": ("ένα", "μία", "μια"),
                       "pl": ("jeden", "jedna")}

_LETRA = r"\wά-ώα-ωΑ-ΩϊΐόύΊΌΎ"


def idiomas() -> tuple:
    """Os idiomas que o modulo SABE ler. Fora deles ele diz que nao sabe."""
    return tuple(sorted(VOCABULARIO))


def encontra(texto, idioma) -> list:
    """Os numerais do vocabulario presentes no texto, em ordem alfabetica.

    Idioma desconhecido devolve `None` — e NAO lista vazia, que leria como
    "nenhum numeral". Vazio de instrumento nao prova ausencia (17/10).
    """
    chave = (idioma or "")[:2]
    voc = VOCABULARIO.get(chave)
    if voc is None:
        return None
    alvo = (texto or "").lower()
    achados = []
    for p in voc:
        if re.search(r"(?<![%s])%s(?![%s])" % (_LETRA, re.escape(p), _LETRA),
                     alvo):
            achados.append(p)
    return sorted(set(achados))


def da_spec(sp) -> dict:
    """{total, por_cena, idioma} para a spec que esta sendo escrita."""
    idioma = ((sp or {}).get("idioma") or "")[:2]
    cenas = (sp or {}).get("short") or []
    por_cena = [(i, encontra(c.get("nar") or "", idioma))
                for i, c in enumerate(cenas)]
    total = encontra(" ".join(c.get("nar") or "" for c in cenas), idioma)
    return {"idioma": idioma, "total": total, "por_cena": por_cena}


def declaracao_incompleta(sp) -> list:
    """Numerais que a NARRACAO fala e que a COPY nao cita em lugar nenhum.

    E a conferencia que pegou a `s083`. Ela compara contra a copy INTEIRA de
    proposito: citar o numeral em qualquer secao ja mostra que quem escreveu o
    viu, e exigir que esteja na secao certa seria cobrar formatacao.
    """
    d = da_spec(sp)
    if d["total"] is None:
        return []
    copy = ((sp or {}).get("copy") or "").lower()
    return [n for n in d["total"] if n not in copy]


def relato(caminho=None, spec=None) -> str:
    """A MESMA convencao dos outros relatos: `(caminho, spec=None)`.

    Ela nascera com UM parametro cujo nome dizia aceitar os dois, e o
    despachante decide pela ARIDADE — logo a passada declarava "NAO aceita
    rascunho" sobre um modulo que aceitava (21/10, 23:2x).
    """
    if isinstance(caminho, dict):     # compatibilidade: a spec na 1a posicao
        caminho, spec = None, caminho
    caminho_ou_spec = spec if spec is not None else caminho
    sp = caminho_ou_spec
    if isinstance(sp, str):
        import json
        with open(sp, encoding="utf-8") as f:
            sp = json.load(f)
    d = da_spec(sp)
    linhas = ["NUMERAIS FALADOS de %s (%s):"
              % (sp.get("pacote") or sp.get("slug") or "?", d["idioma"] or "?")]
    if d["total"] is None:
        linhas.append("  idioma FORA do vocabulario (%s) — o modulo NAO SABE "
                      "ler este, e isso nao e 'nenhum numeral'."
                      % ", ".join(idiomas()))
        return "\n".join(linhas)
    if not d["total"]:
        linhas.append("  nenhum numeral do vocabulario. **Isto nao prova "
                      "ausencia**: ordinal, fracao escrita de outro jeito e "
                      "numeral dentro de palavra composta nao sao vistos, e "
                      "artigo (`um`/`uma` e equivalentes) fica de fora de "
                      "proposito.")
    else:
        linhas.append("  falados: %s" % ", ".join(d["total"]))
        for i, achados in d["por_cena"]:
            if achados:
                linhas.append("    cena %d: %s" % (i, ", ".join(achados)))
    faltam = declaracao_incompleta(sp)
    if faltam:
        linhas.append("  >> A COPY NAO CITA: %s — se ela diz 'o unico numeral "
                      "falado e ...', a frase esta INCOMPLETA. Foi assim que a "
                      "`epomeno-epipedo-s083` foi publicada com uma declaracao "
                      "que listava dois de tres." % ", ".join(faltam))
    else:
        linhas.append("  a copy cita todos os numerais que a narracao fala.")
    linhas.append("  isto LISTA e NAO julga: se o numeral e estrutura do "
                  "argumento ou fato sobre o mundo, decide a regra (g) — e ela "
                  "e leitura. Codigo de saida sempre zero.")
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/numerais_falados.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
