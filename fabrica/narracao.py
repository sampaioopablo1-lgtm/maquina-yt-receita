#!/usr/bin/env python3
"""Confere a camada FALADA de uma spec, antes de gastar TTS e render.

Motivo de existir: a maquina ja garante que o video sai inteiro, no tempo certo,
com legenda e capitulo — e nada disso mede se a narracao PRENDE. Retencao e o
unico numero que ainda nao temos (`metricas` esta vazia), entao o que da pra
fazer hoje e travar mecanicamente os defeitos de narracao conhecidos.

Uma convergencia que justifica a checagem 6: ja tinhamos medido que roteiro
denso em numero por extenso derruba a taxa do TTS em 9,1% (id-ID-ArdiNeural:
15,1 registrado vs 13,72 medido). Frase-planilha e ao mesmo tempo o que faz o
espectador sair e o que faz a duracao derivar. Um check resolve os dois.

Uso:  python3 narracao.py <spec.json> [--idioma id] [--estrito]
Sai 1 se houver ERRO. Avisos nao derrubam o build.
"""
import sys
import json
import re
import unicodedata
from collections import Counter

# ---------------------------------------------------------------- vocabulario
# Intensificador de hype: o principio e o understatement. Quanto mais pesado o
# fato, mais seca a frase — quem precisa anunciar que e incrivel, nao e.
HYPE = {
    "pt": ["inacreditavel", "incrivel", "absurdo", "insano", "chocante",
           "voce nao vai acreditar", "impressionante", "surreal", "bizarro"],
    "en": ["unbelievable", "incredible", "insane", "mind blowing", "mind-blowing",
           "shocking", "you won't believe", "you wont believe", "crazy", "jaw dropping"],
    "es": ["increible", "inacreible", "alucinante", "impactante", "no vas a creer",
           "brutal", "flipante"],
    "id": ["luar biasa", "gila", "tidak masuk akal", "mengejutkan", "kamu tidak akan percaya",
           "dahsyat", "fantastis"],
    "el": ["απιστευτο", "τρελο", "συγκλονιστικο", "δεν θα το πιστεψεις", "απισteυτα"],
    "tr": ["inanilmaz", "cilginca", "sok edici", "inanamayacaksin", "muhtesem"],
    "pl": ["niewiarygodne", "szalone", "szokujace", "nie uwierzysz", "niesamowite"],
    "hi": ["अविश्वसनीय", "हैरान", "चौंकाने"],
}

# Abertura-slop: anuncia o video em vez de comecar o video.
SLOP = {
    "pt": ["voce sabia que", "neste video vamos", "prepare-se para", "sem mais delongas",
           "vamos falar sobre", "fique ate o final"],
    "en": ["did you know that", "in this video we", "in this video, we", "get ready to",
           "without further ado", "let's talk about", "stay until the end", "stick around"],
    "es": ["sabias que", "en este video vamos", "preparate para", "sin mas preambulos",
           "quedate hasta el final"],
    "id": ["tahukah kamu", "di video ini kita akan", "bersiaplah untuk", "tonton sampai habis",
           "simak sampai akhir"],
    "el": ["ηξερες οτι", "σε αυτο το βιντεο θα", "μεινε μεχρι το τελος"],
    "tr": ["biliyor muydunuz", "bu videoda", "sonuna kadar izleyin"],
    "pl": ["czy wiesz ze", "w tym filmie", "zostan do konca"],
    "hi": ["क्या आप जानते हैं", "इस वीडियो में"],
}

# Estatistica sem dono. O genero se sustenta em NOME + ANO + LUGAR + NUMERO;
# "estudos mostram" e o contrario disso.
VAGO = {
    "pt": ["estudos mostram", "cientistas dizem", "especialistas afirmam", "pesquisas indicam",
           "dados mostram", "sabe-se que"],
    "en": ["studies show", "scientists say", "experts agree", "research shows",
           "data shows", "it is known that"],
    "es": ["los estudios muestran", "los cientificos dicen", "los expertos afirman",
           "las investigaciones indican"],
    "id": ["penelitian menunjukkan", "para ahli mengatakan", "studi menunjukkan",
           "data menunjukkan"],
    "el": ["μελετες δειχνουν", "οι ειδικοι λενε", "ερευνες δειχνουν"],
    "tr": ["arastirmalar gosteriyor", "uzmanlar diyor", "veriler gosteriyor"],
    "pl": ["badania pokazuja", "eksperci mowia", "dane pokazuja"],
    "hi": ["अध्ययन बताते हैं", "विशेषज्ञ कहते हैं"],
}

# Palavras de numero. O roteiro escreve numero por extenso (o TTS soletra digito
# errado), entao contar digito nao acha frase-planilha — tem que contar palavra.
NUMEROS = {
    "pt": r"\b(um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|"
          r"quatorze|catorze|quinze|dezesseis|dezessete|dezoito|dezenove|vinte|trinta|quarenta|"
          r"cinquenta|sessenta|setenta|oitenta|noventa|cem|cento|duzentos|trezentos|quinhentos|"
          r"mil|milhao|milhoes|bilhao|bilhoes|por cento|virgula)\b",
    "en": r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
          r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|"
          r"sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion|percent|point)\b",
    "es": r"\b(uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|"
          r"catorce|quince|dieciseis|veinte|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|"
          r"noventa|cien|ciento|doscientos|quinientos|mil|millon|millones|por ciento|coma)\b",
    "id": r"\b(satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|belas|"
          r"puluh|seratus|ratus|seribu|ribu|juta|miliar|triliun|persen|koma)\b",
    "el": r"\b(ενα|δυο|τρια|τεσσερα|πεντε|εξι|επτα|οκτω|εννεα|δεκα|εικοσι|τριαντα|σαραντα|"
          r"πενηντα|εξηντα|εβδομηντα|ογδοντα|ενενηντα|εκατο|χιλια|χιλιαδες|εκατομμυρια|τοις εκατο)\b",
    "tr": r"\b(bir|iki|uc|dort|bes|alti|yedi|sekiz|dokuz|on|yirmi|otuz|kirk|elli|altmis|"
          r"yetmis|seksen|doksan|yuz|bin|milyon|milyar|yuzde|virgul)\b",
    "pl": r"\b(jeden|dwa|trzy|cztery|piec|szesc|siedem|osiem|dziewiec|dziesiec|dwadziescia|"
          r"trzydziesci|czterdziesci|piecdziesiat|sto|tysiac|tysiace|milion|miliard|procent)\b",
    "hi": r"(एक|दो|तीन|चार|पाँच|पांच|छह|सात|आठ|नौ|दस|बीस|तीस|सौ|हज़ार|हजार|लाख|करोड़|प्रतिशत)",
}

# Conectores que NAO encerram um grupo de numero: "quarenta e dois" e um numero.
CONECTOR = {
    "pt": r"\b(e|de|do|da|com|por)\b", "en": r"\b(and|point|of|to|a|per)\b",
    "es": r"\b(y|con|de|por)\b", "id": r"\b(dan|koma|per)\b",
    "el": r"\b(και|με)\b", "tr": r"\b(ve)\b", "pl": r"\b(i|z)\b", "hi": r"(और)",
}

MAX_NUM_FRASE = 4      # 4+ QUANTIDADES numa frase e planilha falada
MAX_PALAVRAS = 34      # nao cabe num folego so
MAX_VIRGULAS = 3       # 3+ virgulas viram frases separadas
MIN_SOCO_PCT = 6.0     # % minimo de frases curtas (<=5 palavras): o ritmo
MAX_SOCO_PCT = 45.0    # acima disso nao e ritmo, e telegrama

IDIOMA_BASE = {"pt-br": "pt", "pt-pt": "pt", "es-mx": "es", "es-es": "es",
               "en-us": "en", "en-gb": "en", "id-id": "id", "el-gr": "el",
               "tr-tr": "tr", "pl-pl": "pl", "hi-in": "hi"}


def normaliza(s):
    """Tira acento para casar as listas sem multiplicar variantes."""
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def idioma_de(spec, forcado=None):
    if forcado:
        return IDIOMA_BASE.get(forcado.lower(), forcado.lower()[:2])
    voz = spec.get("voz", "")
    tag = "-".join(voz.split("-")[:2]).lower()
    return IDIOMA_BASE.get(tag, tag[:2] or "en")


# Fim de frase em devanagari e o DANDA (।), nao o ponto. Sem ele, todo roteiro
# em hindi virava UMA frase so: o agla-level-003 foi acusado de "4 numeros numa
# frase" num trecho que tem dois em cada uma das duas frases, e a trava
# reprovaria qualquer roteiro em hindi para sempre. O canal tem 0 publicados.
# O danda duplo (॥) fecha verso/estrofe e tambem encerra.
FIM_DE_FRASE = ".!?…।॥"


# Como se fecha uma pergunta, por idioma. O grego NAO usa "?": o ponto de
# interrogacao grego e ";" (U+003B) e o codepoint dedicado U+037E, que o
# Unicode define como canonicamente equivalente a ele. Sem esta tabela o
# portao do gancho era IMPOSSIVEL de passar em grego — o roteiro certo
# levava aviso e o errado tambem, o que e o mesmo que nao ter portao.
# Medido em 19/08/2026: 5 avisos no epomeno-epipedo-004 e 5 no 005, todos
# em pontes que JA terminavam em pergunta.
#
# O ";" fica fora do padrao geral de proposito: em portugues, ingles ou
# polones ponto e virgula nao fecha pergunta nenhuma.
GANCHO = {
    None: ("?", ":", "\u2026", "..."),
    "el": ("?", ";", "\u037e", ":", "\u2026", "..."),
}


def frases(texto):
    return [
        f.strip()
        for f in re.split(rf"(?<=[{re.escape(FIM_DE_FRASE)}])\s+|\n+", texto)
        if f.strip()
    ]


def conta_numeros(frase, idi):
    """Conta QUANTIDADES, nao palavras de numero.

    "dua ribu dua puluh enam" sao quatro palavras e um unico numero: o ano 2026.
    Contar palavra acusava 8 numeros numa frase que fala de dois. A unidade certa
    e o GRUPO — uma corrida de palavras de numero, atravessada por conectores
    ("e", "and", "dan", "koma"), vale 1.
    """
    padrao = NUMEROS.get(idi)
    if not padrao:
        return len(re.findall(r"\d+", frase))
    txt = frase if idi == "hi" else normaliza(frase)
    conector = CONECTOR.get(idi, r"\b(e)\b")
    grupos, dentro = 0, False
    for tok in re.findall(r"\S+", txt):
        eh_num = bool(re.fullmatch(r"[\d.,]*\d[\d.,]*[^\w]*", tok)) or bool(re.search(padrao, tok))
        eh_lig = bool(re.search(conector, tok))
        if eh_num:
            if not dentro:
                grupos += 1
                dentro = True
        elif eh_lig and dentro:
            pass                  # conector nao encerra o grupo: "quarenta e dois"
        else:
            dentro = False
    return grupos


def analisa(spec, idi):
    erros, avisos = [], []
    todas = []
    cenas = spec.get("longo", [])

    for i, c in enumerate(cenas):
        nar = c.get("nar", "")
        n = normaliza(nar)
        onde = f"cena {i:02d}"

        for termo in HYPE.get(idi, []):
            if normaliza(termo) in n:
                erros.append(f"{onde}: hype '{termo}' — understatement, a calma e que faz bater")
        for termo in SLOP.get(idi, []):
            if normaliza(termo) in n:
                erros.append(f"{onde}: slop '{termo}' — comece o video em vez de anuncia-lo")
        for termo in VAGO.get(idi, []):
            if normaliza(termo) in n:
                avisos.append(f"{onde}: estatistica sem dono '{termo}' — use NOME + ANO + NUMERO")

        fs = frases(nar)
        todas.extend(fs)
        for f in fs:
            nn = conta_numeros(f, idi)
            if nn >= MAX_NUM_FRASE:
                erros.append(f"{onde}: {nn} numeros numa frase — planilha falada. "
                             f"Quebre em progressao: \"{f[:70]}...\"")
            pal = len(f.split())
            if pal > MAX_PALAVRAS:
                avisos.append(f"{onde}: frase de {pal} palavras, nao cabe num folego")
            if f.count(",") >= MAX_VIRGULAS:
                avisos.append(f"{onde}: {f.count(',')} virgulas numa frase — vire frases separadas")

        # Cliffhanger: so na cena que ANTECEDE uma troca de capitulo. `sem_cap`
        # marca quase toda cena — nao e sinal de ponte, e o contrario disso.
        proxima_abre_cap = i + 1 < len(cenas) and cenas[i + 1].get("cap")
        if proxima_abre_cap and fs:
            if not fs[-1].rstrip().endswith(GANCHO.get(idi, GANCHO[None])):
                avisos.append(f"{onde}: ultima cena do capitulo fecha com ponto final morto "
                              f"— vira '{cenas[i + 1]['cap']}' sem gancho")

    # Ritmo: sobe, sobe, derruba. Sem frase curta nao ha soco.
    if todas:
        curtas = sum(1 for f in todas if len(f.split()) <= 5)
        pct = 100.0 * curtas / len(todas)
        if pct < MIN_SOCO_PCT:
            avisos.append(f"ritmo: so {pct:.1f}% de frases curtas (<=5 palavras), "
                          f"minimo {MIN_SOCO_PCT}% — falta o soco depois do build")
        elif pct > MAX_SOCO_PCT:
            avisos.append(f"ritmo: {pct:.1f}% de frases curtas, acima de {MAX_SOCO_PCT}% — "
                          f"vira telegrama, sem frase que monte")
    return erros, avisos, todas


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    estrito = "--estrito" in sys.argv
    forcado = None
    if "--idioma" in sys.argv:
        forcado = sys.argv[sys.argv.index("--idioma") + 1]

    spec = json.load(open(args[0], encoding="utf-8"))
    idi = idioma_de(spec, forcado)
    erros, avisos, todas = analisa(spec, idi)

    print(f"{args[0]}  idioma={idi}  cenas={len(spec.get('longo', []))}  frases={len(todas)}")
    for e in erros:
        print(f"  ERRO   {e}")
    for a in avisos:
        print(f"  aviso  {a}")
    print(f"  -> {len(erros)} erro(s), {len(avisos)} aviso(s)")
    if erros or (estrito and avisos):
        sys.exit(1)


if __name__ == "__main__":
    main()
