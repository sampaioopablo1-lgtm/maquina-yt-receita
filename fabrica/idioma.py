#!/usr/bin/env python3
"""Confere que a narracao inteira esta na lingua que a spec declara.

Motivo de existir, com nome e data: escrevi o `blocos_006` comecando em
indonesio e derrapando para portugues a partir do capitulo 2. A docstring do
proprio arquivo registra o diagnostico — "o linter de narracao nao pega troca de
idioma, so o autor pega". Ele passou limpo nos seis portoes.

Por que nenhum dos outros pega: o `narracao.py` mede ritmo, quantidade de
numero, hype e gancho, e nada disso depende da lingua; o `glifos` so pergunta se
existe fonte com o desenho do caractere, e portugues e indonesio usam o mesmo
alfabeto; o `duracao` conta caracteres. Um roteiro meio indonesio e meio
portugues satisfaz os seis e produz um video inutilizavel — o TTS le portugues
com fonemas indonesios, e o espectador desiste na primeira frase virada.

Custo de descobrir tarde: o pacote inteiro. Nao ha conserto parcial; o roteiro
se reescreve.

COMO DECIDE. Duas evidencias, nesta ordem:

1. ESCRITA. Grego e devanagari se separam do alfabeto latino por codepoint, e
   isso e certeza, nao estimativa. Uma cena em grego dentro de uma spec latina
   (ou o contrario) e erro imediato.

2. PALAVRA FUNCIONAL. Dentro do alfabeto latino a decisao sai das palavras de
   funcao — artigo, preposicao, conjuncao, pronome. Elas sao as mais frequentes
   de qualquer lingua e nao mudam com o assunto, entao servem para as seis
   linguas latinas do portfolio sem depender do tema da spec.

   As listas trazem so o que DISCRIMINA dentro deste portfolio. "que" e "para"
   estao em portugues e espanhol e por isso ficam de fora das duas; "uma/una",
   "isso/eso", "os/los" ficam, porque separam. Palavra que aparece em duas
   listas nao ajuda a decidir e so gera empate.

O portao e deliberadamente surdo para cena curta: abaixo de MIN_TOKENS nao ha
evidencia suficiente e acusar ali seria ruido. Cena de kicker curto passa.

Uso:  python3 idioma.py <spec.json>
Sai 1 se houver erro.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata

# Quantas palavras de funcao da lingua ERRADA bastam para acusar. Duas sao
# coincidencia plausivel ("no" e "de" existem em varias); tres em UMA cena, com
# a lingua declarada perdendo, e frase virada.
MIN_ACHADOS = 3

# E por quanto ela precisa VENCER a lingua declarada. Vencer por um so nao
# separa drift de ruido — uma frase portuguesa com um espanholismo empata em
# torno de zero. Drift de verdade nao empata: uma frase inteira em portugues
# dentro de um roteiro indonesio marca cinco a oito contra zero.
MARGEM = 2

# A janela: quantas cenas seguidas somar, e com que folga acusar o trecho.
# Calibrado no corpus de 14/08/2026 — ver _janelas.
JANELA = 5
JANELA_MIN = 6
JANELA_MARGEM = 4

# Abaixo disto a cena nao tem evidencia. Medido no corpus de 14/08/2026: a cena
# mediana tem 25 tokens, e as que ficam abaixo de 8 sao kicker e CTA curto.
MIN_TOKENS = 8

# Palavras de funcao DISCRIMINANTES. Ver docstring: o que aparece em duas
# linguas do portfolio foi removido das duas, porque empata em vez de decidir.
FUNCIONAIS = {
    "pt": {"nao", "uma", "voce", "muito", "tambem", "entao", "ainda", "isso",
           "isto", "mas", "dos", "das", "essa", "esse", "assim", "sao",
           "seu", "sua", "quando", "pelo", "pela", "ate", "ja", "onde",
           "quem", "tem", "nos", "nas", "eles", "elas", "foi", "fica",
           "com", "sem", "um", "os", "vai", "sempre", "depois", "outro",
           "outra", "apenas", "tudo", "esses", "essas", "dele", "dela",
           "qualquer", "pouco", "coisa", "gente", "cabe", "faz", "poe"},
    "es": {"una", "usted", "muy", "tambien", "entonces", "todavia", "eso",
           "esto", "pero", "los", "las", "esa", "ese", "asi", "son",
           "cuando", "hasta", "ya", "donde", "quien", "tiene", "hay", "del",
           "sus", "ellos", "ellas", "fue", "queda", "mismo", "otro",
           "con", "sin", "siempre", "despues", "otra", "solo", "todo",
           "algo", "cualquier", "poco", "ahora", "cosa", "hace", "pone"},
    "en": {"the", "and", "of", "to", "is", "that", "you", "for", "with", "this",
           "it", "not", "are", "but", "have", "was", "they", "from", "your",
           "what", "when", "which", "there", "their", "than", "then", "about",
           "will", "would", "can", "because", "should", "could", "only",
           "also", "more", "other", "some", "any", "into", "over", "after",
           "before", "these", "those", "being", "does", "did", "how", "why"},
    "id": {"yang", "dan", "di", "ke", "untuk", "tidak", "ini", "itu", "dengan",
           "dari", "adalah", "akan", "bisa", "kamu", "saya", "sudah", "juga",
           "karena", "atau", "pada", "kalau", "orang", "lebih", "harus",
           "setiap", "bukan", "saja", "kalo", "banyak", "sama",
           "dalam", "oleh", "seperti", "hanya", "masih", "tetapi", "namun",
           "semua", "kita", "mereka", "sendiri", "sangat", "belum", "agar",
           "supaya", "ketika", "sehingga", "tapi", "bahwa", "ada"},
    "pl": {"sie", "nie", "jest", "tego", "ktory", "ale", "tylko", "jak", "tym",
           "przez", "dla", "oraz", "zeby", "wiec", "juz", "jako", "moze",
           "kiedy", "gdy", "bardzo", "wszystko", "ten", "czy", "swoje",
           "jesli", "nawet", "ktore", "tych", "byla", "bylo", "beda",
           "przy", "pod", "nad", "ktora", "wszyscy", "jednak", "dlatego",
           "poniewaz", "zawsze", "nigdy", "teraz", "wtedy", "kazdy", "swoim"},
    "tr": {"bir", "ve", "bu", "icin", "ile", "daha", "ama", "cok", "sonra",
           "kadar", "olarak", "var", "yok", "gibi", "ne", "diye",
           "ancak", "ise", "yani", "hem", "eger", "kendi", "sey",
           "zaman", "iki", "gore", "olan", "degil", "sadece", "hicbir",
           "veya", "ayrica", "boyle", "soyle", "simdi", "artik", "bile",
           "birlikte", "uzere", "dolayi", "nasil", "neden", "hangi", "biraz"},
}

# As listas passam por um teste que prova que nenhuma palavra esta em duas
# delas: `test_idioma.py::test_nenhuma_palavra_funcional_serve_a_duas_linguas`.
# Isso nao e zelo — foi assim que a primeira versao deste portao acusou a cena
# 45 da sx-educacao-001, que e portugues corrente, de parecer espanhol: `ser`,
# `cada` e `por` estavam nas duas listas e o empate virou acusacao.

# Escritas que se separam por codepoint. Certeza, nao estimativa.
ESCRITAS = {
    "el": lambda c: "Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿",
    "hi": lambda c: "ऀ" <= c <= "ॿ",
}

IDIOMA_BASE = {"pt-br": "pt", "pt-pt": "pt", "es-mx": "es", "es-es": "es",
               "en-us": "en", "en-gb": "en", "id-id": "id", "el-gr": "el",
               "tr-tr": "tr", "pl-pl": "pl", "hi-in": "hi"}


def _base(tag: str) -> str:
    t = (tag or "").lower()
    return IDIOMA_BASE.get(t, IDIOMA_BASE.get("-".join(t.split("-")[:2]), t[:2]))


def idioma_da_spec(sp: dict) -> str:
    """A lingua vem da VOZ, nao do campo `idioma`.

    A voz e o que o TTS realmente usa: uma spec marcada `pt-BR` que renderiza
    com id-ID-GadisNeural sai em indonesio, e e a voz que manda. O campo
    `idioma` serve ao YouTube, e o portao de identidade ja o confere contra o
    config do canal.
    """
    voz = sp.get("voz") or ""
    return _base("-".join(voz.split("-")[:2])) if voz else _base(sp.get("idioma", ""))


def _sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _tokens(nar: str) -> list[str]:
    return re.findall(r"[^\W\d_]+", _sem_acento(nar.lower()), re.UNICODE)


def escrita_de(nar: str) -> str | None:
    """Devolve 'el' ou 'hi' quando a cena e predominantemente daquela escrita.

    Predominante, e nao "tem um caractere": um nome proprio grego citado num
    roteiro em ingles nao pode reprovar a cena.
    """
    letras = [c for c in nar if c.isalpha()]
    if len(letras) < MIN_TOKENS:
        return None
    for cod, dentro in ESCRITAS.items():
        if sum(1 for c in letras if dentro(c)) > 0.5 * len(letras):
            return cod
    return None


def pontua(nar: str) -> dict[str, int]:
    """Quantas palavras de funcao de cada lingua latina esta cena contem."""
    toks = set(_tokens(nar))
    return {cod: len(toks & palavras) for cod, palavras in FUNCIONAIS.items()}


def analisa_cena(nar: str, declarado: str) -> str | None:
    """Devolve o motivo se esta cena nao esta na lingua declarada."""
    esc = escrita_de(nar)
    if declarado in ESCRITAS:
        # Declarada grega ou hindi: a cena TEM que estar naquela escrita.
        if esc != declarado:
            return f"declarada {declarado} mas a cena nao esta na escrita de {declarado}"
        return None
    if esc:
        return f"declarada {declarado} mas a cena esta em {esc}"

    toks = _tokens(nar)
    if len(toks) < MIN_TOKENS:
        return None
    p = pontua(nar)
    meu = p.get(declarado, 0)
    outro, quanto = max(p.items(), key=lambda kv: kv[1])
    if quanto >= MIN_ACHADOS and quanto >= meu + MARGEM and outro != declarado:
        return (f"declarada {declarado} mas parece {outro} "
                f"({quanto} palavras de funcao de {outro} contra {meu} de {declarado})")
    return None


def _janelas(cenas, declarado: str) -> list[str]:
    """A derrapagem real nao e uma cena, e um TRECHO.

    A regra por cena e estrita de proposito — ela nao pode acusar portugues
    corrente de espanhol — e o preco disso e deixar passar a cena pobre em
    palavra de funcao. Medido no corpus em 14/08/2026: com um roteiro
    portugues inteiro declarado como indonesio, a regra por cena marca 28% das
    cenas. Suficiente para derrubar o build, mas nao para achar um trecho curto.

    A janela recupera isso sem afrouxar nada: soma as contagens de JANELA cenas
    seguidas. Uma cena com uma palavra portuguesa e ruido; cinco cenas seguidas
    somando oito palavras portuguesas contra uma indonesia e um capitulo virado.
    """
    contagens = []
    for c in cenas:
        nar = c.get("nar", "")
        if len(_tokens(nar)) < MIN_TOKENS or escrita_de(nar):
            contagens.append(None)          # sem evidencia, nao entra na soma
        else:
            contagens.append(pontua(nar))

    faltas = []
    for i in range(len(contagens) - JANELA + 1):
        bloco = [p for p in contagens[i:i + JANELA] if p]
        if len(bloco) < JANELA - 1:         # janela quase toda sem evidencia
            continue
        soma = {cod: sum(p[cod] for p in bloco) for cod in FUNCIONAIS}
        meu = soma.get(declarado, 0)
        outro, quanto = max(soma.items(), key=lambda kv: kv[1])
        if outro != declarado and quanto >= JANELA_MIN and quanto >= meu + JANELA_MARGEM:
            faltas.append(
                f"cenas {i:02d}-{i + JANELA - 1:02d}: o trecho parece {outro}, nao "
                f"{declarado} ({quanto} palavras de funcao de {outro} contra {meu})")
    return faltas


def _funde(faltas: list[str]) -> list[str]:
    """Trecho longo virado gera uma janela por cena; reportar todas e ruido."""
    return faltas[:6] + ([f"... e mais {len(faltas) - 6} trecho(s)"]
                         if len(faltas) > 6 else [])


def analisa(sp: dict) -> list[str]:
    declarado = idioma_da_spec(sp)
    if declarado not in FUNCIONAIS and declarado not in ESCRITAS:
        return [f"idioma {declarado!r} sem perfil — some ao perfil antes de usar a voz"]

    faltas = []
    for bloco in ("longo", "short"):
        cenas = sp.get(bloco) or []
        for i, c in enumerate(cenas):
            motivo = analisa_cena(c.get("nar", ""), declarado)
            if motivo:
                faltas.append(f"{bloco} cena {i:02d}: {motivo}")
        if declarado in FUNCIONAIS and len(cenas) >= JANELA:
            faltas += [f"{bloco} {j}" for j in _funde(_janelas(cenas, declarado))]
    return faltas


def main() -> int:
    sp = json.load(open(sys.argv[1], encoding="utf-8"))
    faltas = analisa(sp)
    print(f"{sys.argv[1]}  idioma={idioma_da_spec(sp)}  "
          f"cenas={len(sp.get('longo') or [])}+{len(sp.get('short') or [])}")
    for f in faltas:
        print(f"  ERRO   {f}")
    print(f"  -> {len(faltas)} erro(s)")
    return 1 if faltas else 0


if __name__ == "__main__":
    raise SystemExit(main())
