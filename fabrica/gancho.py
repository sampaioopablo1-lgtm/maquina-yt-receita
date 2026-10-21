# -*- coding: utf-8 -*-
"""O gancho tem DOIS limites na mesma cena, e eu os conciliava a mao.

MEDIDO em 19/10 as 21:1x, escrevendo o `epomeno-epipedo-s070`. O
`mira.orcamento` me deu **59 caracteres por cena** para nove cenas no
`ALVO_SHORT` da frota, eu escrevi a cena 0 nesse orcamento, e o portao
`variedade` REPROVOU: *"a primeira frase da cena 1 tem 13 palavras e o limite e
12"*. Encurtei o gancho, a previsao caiu de 41,6 para **41,0** — abaixo do piso
da faixa —, e eu recuperei o comprimento em duas cenas do meio **somando de
cabeca quantos caracteres faltavam**, em QUATRO iteracoes:

    57,9 -> 41,0   62,3 -> 43,0   58,8 -> 41,4   59,3 -> 41,6

**Sao dois limites sobre a MESMA cena e nenhum instrumento os mostrava
juntos:** o orcamento fala em CARACTERES e o portao fala em PALAVRAS. E o item
3 da §10 — todo numero que eu calculo a mao vira um erro meu —, e aqui ele
custou quatro passadas e um portao vermelho.

**O LIMITE E LIDO DO PORTAO, nao copiado.** `variedade.GANCHO_MAX_PALAVRAS` e
`variedade.primeira_frase` sao os donos, e este modulo os CHAMA — a mesma
disciplina do `area_segura.py`, que passou a ler a margem do portao em vez de
repetir o numero. Copiar o 12 aqui seria o quinto caso de dois donos da semana.

**E A MEDIDA DO CUSTO SAI DO `ensaio`, nao de uma regra de tres minha:** a
previsao depois do corte vem de `ensaio.duracao_real_prevista` com a spec
ALTERADA, que e a mesma funcao que a mira e o portao cobram. Refazer
`R` e `P` aqui criaria o segundo dono da sobrecarga por voz, que e o defeito
que congelou a legenda.

**O teto em CARACTERES e por IDIOMA e vai como ORIENTACAO, nao como limite.**
Medido no disco, a mediana de caracteres por palavra da primeira frase:

| idioma | n | chars/palavra | 12 palavras cabem em |
|---|---|---|---|
| `el` | 726 | 5,78 | ~69 |
| `pl` | 678 | 6,22 | ~75 |
| `pt-BR` | 989 | 5,25 | ~63 |
| `id` | 121 | 6,33 | ~76 |
| `tr` | 49 | 6,25 | ~75 |

**E a mediana NAO teria me avisado**, e isso vai dito: a minha frase tinha 68
caracteres, ABAIXO dos 69 do grego, e ainda assim 13 palavras — porque ela usou
palavras curtas. Logo o teto estatistico orienta a redacao e **a conferencia
que decide e a contagem exata**, que e o que `confere` faz.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(RAIZ, "fabrica") not in sys.path:
    sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

# Medido no disco em 19/10 as 21:2x: mediana de caracteres por palavra da
# PRIMEIRA FRASE das cenas de short, por idioma. Orientacao de redacao, nao
# limite — ver o docstring.
CHARS_POR_PALAVRA = {
    "el": 5.78, "pl": 6.22, "pt-BR": 5.25, "id": 6.33, "tr": 6.25,
    "en": 5.50, "es-MX": 5.04, "hi": 4.79,
}


def limite() -> int:
    """O limite de palavras do gancho, LIDO do portao que o cobra."""
    import variedade

    return variedade.GANCHO_MAX_PALAVRAS


def palavras_do_gancho(spec: dict) -> int:
    """Palavras da primeira frase da cena 0, pela MESMA funcao do portao."""
    import variedade

    cenas = spec.get("short") or []
    if not cenas:
        return 0
    return len(variedade.primeira_frase(cenas[0].get("nar") or "").split())


def teto_de_caracteres(idioma: str):
    """Quantos caracteres costumam caber no limite de palavras, por idioma.

    Devolve None para idioma sem medida — inventar um numero aqui seria limiar
    sem procedencia (§10).
    """
    cpp = CHARS_POR_PALAVRA.get(idioma)
    return None if cpp is None else round(limite() * cpp)


def _previsao(spec: dict, provedor: str = "edge"):
    """A previsao que a MIRA e o PORTAO cobram, pela funcao deles."""
    import ensaio

    return ensaio.duracao_real_prevista(
        spec.get("short") or [], spec.get("voz", ""), provedor)


def custo_do_encurtamento(spec: dict, provedor: str = "edge") -> dict:
    """Se o gancho passa do limite, quanto custa cortar — e onde recuperar.

    Esta e a conta que eu fiz de cabeca em quatro iteracoes. Ela corta a frase
    nas primeiras `limite()` palavras, mede a previsao da spec ASSIM, e diz
    quantos caracteres precisam voltar para as OUTRAS cenas para a previsao
    retornar ao ponto de hoje.
    """
    import copy

    import variedade

    cenas = spec.get("short") or []
    n = palavras_do_gancho(spec)
    lim = limite()
    fora = {
        "palavras": n, "limite": lim, "passa": n > lim,
        "idioma": spec.get("idioma"),
        "teto_de_caracteres": teto_de_caracteres(spec.get("idioma")),
        "chars_do_gancho": len(
            variedade.primeira_frase((cenas[0].get("nar") or "")) if cenas else ""
        ),
    }
    if not cenas:
        fora["motivo"] = "spec sem cenas de short"
        return fora
    fora["previsao_hoje"] = _previsao(spec, provedor)
    if n <= lim:
        fora["motivo"] = "o gancho cabe; nada a cortar"
        return fora

    frase = variedade.primeira_frase(cenas[0].get("nar") or "")
    curta = " ".join(frase.split()[:lim])
    sp2 = copy.deepcopy(spec)
    sp2["short"][0]["nar"] = (
        (cenas[0].get("nar") or "").replace(frase, curta, 1)
    )
    fora["chars_perdidos"] = len(frase) - len(curta)
    fora["previsao_depois"] = _previsao(sp2, provedor)
    fora["queda_s"] = round(fora["previsao_hoje"] - fora["previsao_depois"], 2)
    # quantos caracteres recolocar nas OUTRAS cenas para voltar ao ponto
    recolocar = 0
    outras = len(cenas) - 1
    if outras > 0:
        sp3 = copy.deepcopy(sp2)
        while recolocar < 400:
            if _previsao(sp3, provedor) >= fora["previsao_hoje"]:
                break
            recolocar += outras
            for c in sp3["short"][1:]:
                c["nar"] = (c.get("nar") or "") + "x"
    fora["recolocar_chars"] = recolocar
    fora["recolocar_por_cena"] = (
        round(recolocar / outras, 1) if outras else None
    )
    fora["motivo"] = (
        f"o gancho passa em {n - lim} palavra(s); cortar tira "
        f"{fora['chars_perdidos']} caracteres e derruba a previsao em "
        f"{fora['queda_s']} s, que se recupera com ~"
        f"{fora['recolocar_por_cena']} caracteres por cena nas outras "
        f"{outras}"
    )
    return fora


def relato(caminho: str, spec: dict | None = None) -> str:
    import rascunho
    sp = rascunho.spec_de(caminho, spec)
    d = custo_do_encurtamento(sp)
    linhas = ["GANCHO de %s:" % sp.get("slug", caminho)]
    linhas.append(
        "  primeira frase da cena 1: %s palavra(s), limite %s (lido do portao)"
        % (d["palavras"], d["limite"])
    )
    teto = d.get("teto_de_caracteres")
    linhas.append(
        "  ela tem %s caracteres; no idioma %s, %s palavras costumam caber em "
        "~%s — ORIENTACAO, nao limite (palavra curta fura o teto)"
        % (d.get("chars_do_gancho"), d.get("idioma"), d["limite"],
           teto if teto is not None else "sem medida")
    )
    if d["passa"]:
        linhas.append("  >> PASSA DO LIMITE: " + d["motivo"])
        linhas.append(
            "     previsao hoje %.2f s, depois do corte %.2f s"
            % (d["previsao_hoje"], d["previsao_depois"])
        )
    else:
        linhas.append("  cabe. previsao edge %.2f s" % d["previsao_hoje"])
    linhas.append(
        "  isto INFORMA antes do render; quem reprova e o portao `variedade`."
    )
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/gancho.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
