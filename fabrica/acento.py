# -*- coding: utf-8 -*-
"""O acento da NARRACAO era conferido no olho, e falhou DUAS rodadas seguidas.

POR QUE EXISTE (19/10, 18:2x). Em 15:3x a descricao grega do
`epomeno-epipedo-s068` subiu **sem tonos**; em 17:2x a primeira versao do
`labtreinamento-s086` trazia *"O mesmo treino da tres"*, *"todo o historico"*,
*"voce usou"*. Nas duas vezes quem pegou fui **eu relendo** — e nas duas o
`CLAUDE.md` registrou a mesma frase: *"nenhum portao cobra acento da NARRACAO"*,
*"o acento e passo de REDACAO e nao tem instrumento"*. Duas vezes com a mesma
assinatura deixa de ser acidente: e o item 3 da §10, a conferencia morando na
minha cabeca.

E O CUSTO NAO E ESTETICO: o TTS le o texto como ele esta escrito. Sem tonos a
voz grega muda a silaba tonica; sem acento o pt-BR troca a pronuncia da palavra.
A peca sai narrada errado e **nenhum portao reprova** — e o `copy` so conta
palavras.

**A REGRA SAI DA MEDICAO, NAO DE UMA LISTA DE IDIOMAS.** Varridas as specs do
disco, a proporcao de letras acentuadas na narracao do short:

| idioma | n | com ZERO acento |
|---|---|---|
| `el`    |  86 | **0** |
| `tr`    |  10 | **0** |
| `pl`    |  81 | 2 |
| `pt-BR` | 120 | 5 |
| `en` / `id` / `hi` | 16 / 23 / 8 | **todas** |

Logo o discriminador **nao e um limiar universal**: em `en`, `id` e `hi` o zero e
o valor CERTO, e um instrumento que alarmasse ali seria detector que inventa
achado (725). Quem decide e a distribuicao do PROPRIO idioma, lida do disco:
idioma cuja maioria das specs esta em zero **nao discrimina**, e isto sai como
RECUSA com o motivo, do jeito que o `porta1` recusa janela curta.

**E O QUE A VARREDURA ACHOU NO ACERVO, dito sem inflar:** sete specs de idioma
que normalmente carrega acento estao em zero — `labtreinamento-002`, `-003`,
`seja-mais-magra-004`, `sx-educacao-001`, `-002` (pt-BR) e `kolejny-poziom-003`,
`-004` (pl). Duas delas sao de canal VIVO da frota. **O que eu NAO afirmo:** que
foram publicadas assim, nem que o defeito e o mesmo das duas peças de hoje — a
narracao gravada vive no video e eu nao a reli. O que esta medido e que a spec no
disco nao tem acento.

**NAO E PORTAO**, e o motivo e o do `mira.py`: ele reprovaria essas sete, que sao
acervo e nao producao. O lugar dele e o relato da rodada e a suite.
"""
import glob
import json
import os
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Abaixo disto a narracao conta como ESCRITA SEM ACENTO. Nao e limiar de
# qualidade: e o piso do instrumento, porque uma letra acentuada solta num
# paragrafo inteiro nao distingue texto acentuado de texto sem acento.
PISO_DE_ZERO = 0.5


def proporcao(cenas) -> float | None:
    """Porcentagem de letras com marca diacritica na narracao das cenas.

    None quando nao ha letra nenhuma — ausencia nao e zero, que e a regra do
    `duracao_a_medir.residuos`.
    """
    texto = "".join(((c or {}).get("nar") or "") for c in (cenas or []))
    letras = [ch for ch in texto if ch.isalpha()]
    if not letras:
        return None
    marcadas = sum(1 for ch in letras
                   if unicodedata.normalize("NFD", ch)[1:])
    return 100.0 * marcadas / len(letras)


def sem_acento(texto: str) -> str:
    """O mesmo texto com as marcas diacriticas retiradas.

    Existe para a CONTRAPROVA: sem ela o teste nao tem o caso negativo e passa
    com qualquer tabela, que foi o defeito do `or True` de 16/10.
    """
    return "".join(ch for ch in unicodedata.normalize("NFD", texto)
                   if not unicodedata.combining(ch))


def distribuicao(idioma: str, raiz: str = None) -> dict:
    """A distribuicao MEDIDA do idioma, lida das specs do DISCO."""
    raiz = raiz or RAIZ
    valores = []
    zeros = []
    for caminho in sorted(glob.glob(os.path.join(raiz, "fabrica", "specs",
                                                 "*.json"))):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        if (sp.get("idioma") or "?") != idioma:
            continue
        p = proporcao(sp.get("short"))
        if p is None:
            continue
        valores.append(p)
        if p < PISO_DE_ZERO:
            zeros.append(os.path.basename(caminho))
    valores.sort()
    if not valores:
        return {"idioma": idioma, "n": 0, "zeros": [], "discrimina": False,
                "motivo": f"nenhuma spec de idioma {idioma!r} no disco"}
    # O idioma discrimina quando o acento e a REGRA nele: a maioria das specs
    # carrega acento. Derivado, nao listado — lista de idiomas envelhece e e
    # exatamente o tipo de numero que a §10 proibe cravar.
    discrimina = len(zeros) * 2 < len(valores)
    nao_zero = [v for v in valores if v >= PISO_DE_ZERO]
    return {
        "idioma": idioma,
        "n": len(valores),
        "minimo": valores[0],
        "mediana": valores[len(valores) // 2],
        "maximo": valores[-1],
        "piso_dos_acentuados": (min(nao_zero) if nao_zero else None),
        "zeros": zeros,
        "discrimina": discrimina,
        "motivo": None if discrimina else (
            f"{len(zeros)} de {len(valores)} specs de {idioma!r} estao em zero: "
            "neste idioma o zero e o valor CERTO e o instrumento NAO "
            "discrimina. Alarmar aqui seria detector que inventa achado (725)."),
    }


def veredito(spec: dict, raiz: str = None) -> dict:
    """A narracao desta spec parece escrita SEM acento?

    O veredito e contra a distribuicao do PROPRIO idioma. Quando o idioma nao
    discrimina, ele RECUSA com o motivo em vez de devolver um `False` que
    pareceria conferencia feita.
    """
    idi = spec.get("idioma") or "?"
    p = proporcao(spec.get("short"))
    d = distribuicao(idi, raiz)
    out = {"idioma": idi, "proporcao": p, "n": d.get("n"),
           "mediana": d.get("mediana"), "piso": d.get("piso_dos_acentuados"),
           "discrimina": d["discrimina"], "motivo": d.get("motivo")}
    if p is None:
        out["suspeita"] = None
        out["motivo"] = "spec sem narracao: ausencia nao e zero"
        return out
    if not d["discrimina"]:
        out["suspeita"] = None
        return out
    out["suspeita"] = p < PISO_DE_ZERO
    if out["suspeita"]:
        out["motivo"] = (
            f"narracao com {p:.2f}% de letras acentuadas num idioma em que "
            f"{d['n'] - len(d['zeros'])} de {d['n']} specs carregam acento "
            f"(mediana {d['mediana']:.2f}%). O TTS le o texto como esta "
            "escrito, logo isto muda a PRONUNCIA — e nenhum portao cobra.")
    return out


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    v = veredito(spec)
    nome = spec.get("pacote") or os.path.basename(caminho)
    if v["proporcao"] is None:
        return f"ACENTO de {nome}: {v['motivo']}"
    linhas = [f"ACENTO de {nome} ({v['idioma']}): "
              f"{v['proporcao']:.2f}% de letras acentuadas na narracao"]
    if not v["discrimina"]:
        linhas.append("  RECUSA: " + v["motivo"])
        return "\n".join(linhas)
    linhas.append(f"  distribuicao MEDIDA do idioma: n={v['n']}, mediana "
                  f"{v['mediana']:.2f}%, piso dos acentuados "
                  f"{v['piso']:.2f}%")
    if v["suspeita"]:
        linhas.append("  >> SUSPEITA: " + v["motivo"])
    else:
        linhas.append("  carrega acento, como as outras deste idioma. "
                      "NAO reprova — isto informa, pelo argumento do `mira.py`.")
    return "\n".join(linhas)


def main() -> int:
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        print("uso: acento.py fabrica/specs/<spec>.json [...]")
        return 2
    for a in sys.argv[1:]:
        print(relato(a))
    return 0  # INFORMA e nunca reprova, como o `mira.py`


if __name__ == "__main__":
    raise SystemExit(main())
