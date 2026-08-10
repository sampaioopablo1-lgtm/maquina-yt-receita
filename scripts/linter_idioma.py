#!/usr/bin/env python3
"""
Linter de idioma para roteiros indonésios.

Detecta palavras fora do indonésio (PT-BR, ES, etc.) que podem ter
escapado para o roteiro via LLM. Sai com código 0 se limpo, 1 se há
violações. Aceita arquivo ou stdin.

Uso:
    python scripts/linter_idioma.py out/<slug>/roteiro.txt
    python scripts/linter_idioma.py out/<slug>/narracao.json
    cat out/<slug>/legendas.srt | python scripts/linter_idioma.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Palavras portuguesas de alta frequência que NUNCA aparecem em indonésio.
# Não incluir palavras que existem nos dois idiomas (ex: "ada" = "ada" em ID).
# ──────────────────────────────────────────────────────────────────────────────
_PALAVRAS_PT = {
    # pronomes e determinantes
    "não", "nao", "mas", "para", "como", "você", "voce", "seu", "sua",
    "seus", "suas", "esse", "essa", "esses", "essas", "isso", "este",
    "esta", "estes", "estas", "aqui", "ali", "lá", "la",
    # conjunções / advérbios
    "então", "entao", "ainda", "também", "tambem", "porque", "porquê",
    "quando", "onde", "quem", "qual", "quanto", "quão",
    "muito", "pouco", "sempre", "nunca", "já", "ja", "só", "so",
    "mesmo", "outro", "outra", "outros", "outras", "toda", "todo",
    "todos", "todas", "mais", "menos", "bem", "mal",
    # verbos comuns (formas que não existem em indonésio)
    "fazer", "poder", "querer", "dever", "ter", "ser", "estar",
    "foi", "era", "eram", "são", "tem", "vem", "diz", "vai", "faz",
    "pode", "deve", "quer", "faz", "fez", "veio", "disse",
    "vamos", "veja", "veja", "vejamos", "temos", "estamos", "somos",
    # preposições / artigos compostos
    "pelo", "pela", "pelos", "pelas", "num", "numa", "nuns", "numas",
    "del",  # espanhol — nunca indonésio
    # substantivos específicos
    "dinheiro", "pessoa", "pessoas", "trabalho", "vida", "tempo",
    "coisa", "coisas", "forma", "modo", "parte", "vez", "vezes",
    # espanhol de alta frequência (também não aparece em indonésio)
    "pero", "sino", "aunque", "porque", "cuando", "donde", "quien",
    "mucho", "poco", "siempre", "nunca", "ahora", "también", "tambian",
    "puedo", "puede", "quiero", "quiere", "vamos", "tengo", "tiene",
}

# Caracteres com diacríticos impossíveis em indonésio
# (PT/FR/ES: ã õ ç é ê â ô à ñ û î ù ë ï ü etc.)
_DIACRITICO_RE = re.compile(
    r"[àáâãäåæçèéêëìíîïðñòóôõöùúûüýþÿ"
    r"ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝÞŸ]",
    re.UNICODE,
)

# Marcadores de tempo do SRT — ignorar
_SRT_TEMPO_RE = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> ")
_SRT_NUMERO_RE = re.compile(r"^\d+$")


def _extrair_linhas_srt(texto: str) -> list[tuple[int, str]]:
    """Devolve (numero_linha_original, texto) apenas das linhas de narração."""
    resultado = []
    for i, linha in enumerate(texto.splitlines(), 1):
        linha = linha.strip()
        if not linha or _SRT_NUMERO_RE.match(linha) or _SRT_TEMPO_RE.match(linha):
            continue
        resultado.append((i, linha))
    return resultado


def _extrair_linhas_json(texto: str) -> list[tuple[int, str]]:
    """Extrai texto de narracao.json (formato exportar-narracao)."""
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        return []
    resultado = []
    for cena in dados.get("cenas", []):
        idx = cena.get("indice", "?")
        t = cena.get("texto", "")
        resultado.append((idx, t))
    return resultado


def _extrair_linhas_txt(texto: str) -> list[tuple[int, str]]:
    return [(i, l.strip()) for i, l in enumerate(texto.splitlines(), 1) if l.strip()]


def verificar_linha(numero: int | str, texto: str) -> list[str]:
    """Devolve lista de avisos para uma linha. Vazio = sem problemas."""
    avisos: list[str] = []

    # 1. Caracteres com diacríticos impossíveis em indonésio
    matches_diac = _DIACRITICO_RE.findall(texto)
    if matches_diac:
        chars = ", ".join(sorted(set(matches_diac)))
        avisos.append(
            f"  linha {numero}: caractere fora do alfabeto indonésio: {chars!r}\n"
            f"    → {texto[:120]}"
        )

    # 2. Palavras PT/ES de alta frequência
    palavras = re.findall(r"\b[a-zA-Z]{3,}\b", texto.lower())
    encontradas = [p for p in palavras if p in _PALAVRAS_PT]
    if encontradas:
        avisos.append(
            f"  linha {numero}: palavra(s) PT/ES: {', '.join(sorted(set(encontradas)))}\n"
            f"    → {texto[:120]}"
        )

    return avisos


def lint(caminho: Path | None = None) -> int:
    if caminho:
        texto = caminho.read_text(encoding="utf-8")
        sufixo = caminho.suffix.lower()
    else:
        texto = sys.stdin.read()
        sufixo = ".txt"

    if sufixo == ".srt":
        linhas = _extrair_linhas_srt(texto)
    elif sufixo == ".json":
        linhas = _extrair_linhas_json(texto)
    else:
        linhas = _extrair_linhas_txt(texto)

    todos_avisos: list[str] = []
    for numero, linha in linhas:
        todos_avisos.extend(verificar_linha(numero, linha))

    if todos_avisos:
        print(f"LINTER DE IDIOMA — {len(todos_avisos)} problema(s) encontrado(s):\n")
        for a in todos_avisos:
            print(a)
        print(
            "\nCorriga o roteiro antes de narrar. "
            "Um único 'não' ou 'você' no meio do indonésio "
            "quebra a credibilidade do canal."
        )
        return 1

    n = len(linhas)
    print(f"OK — {n} linha(s) verificada(s), nenhuma violação de idioma.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.exists():
            print(f"arquivo não encontrado: {p}", file=sys.stderr)
            sys.exit(2)
        sys.exit(lint(p))
    else:
        sys.exit(lint())
