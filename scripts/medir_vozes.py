"""Mede caracteres por segundo de cada voz edge-tts usada pela frota.

Por que existe: `roteiro.escrever_roteiro` dimensiona o texto em CARACTERES,
porque e caractere que o TTS converte em tempo. A conta e

    chars_alvo = duracao_alvo_s * taxa

e a duracao que sai e `chars_alvo / taxa_real`. Ou seja, o video so alcanca o
alvo se a taxa ASSUMIDA for maior ou igual a real. Assumir menos que a real
encurta o video na mesma proporcao.

Isso torna o padrao de 12,0 perigoso, nao conservador. As vozes vao de 9,85 a
20,02 chars/s. Numa voz de 20, assumir 12 entrega 60% da duracao pedida: 780 s
viram 468 s, sete minutos e meio — ABAIXO do piso de 8 min, e o video e barrado
depois de ja ter custado o render inteiro.

Em 12/08/2026, nove dos treze canais usavam voz sem taxa medida. Este script
tira a duvida: sintetiza um texto NA LINGUA DA VOZ e divide caracteres pela
duracao real do mp3. A lingua importa porque quantos caracteres cabem num
segundo depende do sistema de escrita — devanagari e alfabeto grego carregam
muito mais som por caractere que o latino.

Roda no runner do Actions (.github/workflows/medir-vozes.yml) — o container do
agente nao alcanca speech.platform.bing.com.

Uso:
    pip install edge-tts
    python scripts/medir_vozes.py                    # todas as vozes da frota
    python scripts/medir_vozes.py pl-PL-MarekNeural  # so estas
"""

from __future__ import annotations

import asyncio
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# Texto de calibracao POR IDIOMA. Isto nao e capricho.
#
# A primeira medicao usou um unico texto em portugues para as doze vozes e
# produziu numeros que parecem certos e nao sao. A taxa e caracteres por
# segundo, e quantos caracteres cabem num segundo depende do SISTEMA DE ESCRITA
# e da lingua, nao so da voz: hi-IN em devanagari e el-GR em alfabeto grego
# carregam muito mais som por caractere que o alfabeto latino. Medir uma voz
# grega lendo portugues responde a pergunta errada — o roteiro dela vai ser
# escrito em grego.
#
# Numeros POR EXTENSO em todos, como a fabrica escreve: digito cru muda a
# duracao porque o TTS soletra "2026" de forma diferente em cada idioma.
TEXTOS = {
    "pt": (
        "Este e um texto de calibracao com duracao suficiente para medir a taxa "
        "de fala desta voz com precisao razoavel. Ele contem numeros por "
        "extenso, como mil novecentos e noventa e nove, duzentos e cinquenta, e "
        "tres virgula sete por cento. Tambem contem frases de comprimento "
        "variado. Algumas curtas. Outras mais longas, com virgulas e "
        "subordinadas, do jeito que uma narracao real se comporta quando o "
        "roteirista escreve para o ouvido e nao para o olho."
    ),
    "en": (
        "This is a calibration text long enough to measure this voice's speaking "
        "rate with reasonable precision. It contains numbers written out, such as "
        "nineteen ninety nine, two hundred and fifty, and three point seven "
        "percent. It also contains sentences of varying length. Some short. "
        "Others longer, with commas and subordinate clauses, the way real "
        "narration behaves when the writer writes for the ear and not the eye."
    ),
    "id": (
        "Ini adalah teks kalibrasi yang cukup panjang untuk mengukur kecepatan "
        "bicara suara ini dengan presisi yang wajar. Teks ini berisi angka yang "
        "ditulis dengan huruf, seperti seribu sembilan ratus sembilan puluh "
        "sembilan, dua ratus lima puluh, dan tiga koma tujuh persen. Ada juga "
        "kalimat dengan panjang berbeda. Beberapa pendek. Yang lain lebih "
        "panjang, dengan koma dan anak kalimat, seperti narasi sungguhan ketika "
        "penulis menulis untuk telinga dan bukan untuk mata."
    ),
    "es": (
        "Este es un texto de calibracion con duracion suficiente para medir la "
        "velocidad de habla de esta voz con precision razonable. Contiene "
        "numeros escritos con letras, como mil novecientos noventa y nueve, "
        "doscientos cincuenta, y tres coma siete por ciento. Tambien contiene "
        "frases de longitud variada. Algunas cortas. Otras mas largas, con comas "
        "y subordinadas, como se comporta una narracion real cuando el guionista "
        "escribe para el oido y no para el ojo."
    ),
    "pl": (
        "To jest tekst kalibracyjny o dlugosci wystarczajacej do zmierzenia "
        "tempa mowy tego glosu z rozsadna precyzja. Zawiera liczby zapisane "
        "slowami, takie jak tysiac dziewiecset dziewiecdziesiat dziewiec, "
        "dwiescie piecdziesiat, oraz trzy przecinek siedem procent. Zawiera "
        "takze zdania o roznej dlugosci. Niektore krotkie. Inne dluzsze, z "
        "przecinkami i zdaniami podrzednymi, tak jak zachowuje sie prawdziwa "
        "narracja, gdy autor pisze dla ucha, a nie dla oka."
    ),
    "tr": (
        "Bu, bu sesin konusma hizini makul bir hassasiyetle olcmeye yetecek "
        "uzunlukta bir kalibrasyon metnidir. Yazi ile yazilmis sayilar icerir, "
        "ornegin bin dokuz yuz doksan dokuz, iki yuz elli ve yuzde uc virgul "
        "yedi. Ayrica farkli uzunlukta cumleler icerir. Bazilari kisa. "
        "Digerleri daha uzun, virgullerle ve yan cumlelerle, yazar goz icin "
        "degil kulak icin yazdiginda gercek anlatimin davrandigi gibi."
    ),
    # Alfabeto grego: a taxa em caracteres muda muito em relacao ao latino.
    "el": (
        "Αυτό είναι ένα κείμενο βαθμονόμησης με αρκετή διάρκεια ώστε να μετρηθεί "
        "ο ρυθμός ομιλίας αυτής της φωνής με λογική ακρίβεια. Περιέχει αριθμούς "
        "γραμμένους ολογράφως, όπως χίλια εννιακόσια ενενήντα εννέα, διακόσια "
        "πενήντα, και τρία κόμμα επτά τοις εκατό. Περιέχει επίσης προτάσεις "
        "διαφορετικού μήκους. Κάποιες σύντομες. Άλλες μεγαλύτερες, με κόμματα "
        "και δευτερεύουσες προτάσεις, όπως συμπεριφέρεται μια πραγματική αφήγηση."
    ),
    # Devanagari: cada caractere carrega muito mais som que no alfabeto latino.
    "hi": (
        "यह एक अंशांकन पाठ है जो इस आवाज़ की बोलने की गति को उचित सटीकता से मापने "
        "के लिए पर्याप्त लंबा है। इसमें शब्दों में लिखी संख्याएँ हैं, जैसे उन्नीस सौ "
        "निन्यानबे, दो सौ पचास, और तीन दशमलव सात प्रतिशत। इसमें अलग अलग लंबाई के "
        "वाक्य भी हैं। कुछ छोटे। कुछ लंबे, अल्पविराम और उपवाक्यों के साथ, जैसे "
        "असली कथन तब व्यवहार करता है जब लेखक आँख के लिए नहीं, कान के लिए लिखता है।"
    ),
}


def texto_da_voz(voz: str) -> tuple[str, str]:
    """(idioma, texto) — o texto tem que estar na lingua que a voz vai narrar."""
    idioma = voz.split("-")[0].lower()
    return idioma, TEXTOS.get(idioma, TEXTOS["en"])


# Mesmo rate que a producao usa. Medir com outro rate invalida a medida.
RATE = "-4%"


def vozes_da_frota() -> list[str]:
    achadas = []
    for arquivo in sorted((ROOT / "config" / "canais").glob("*.yaml")):
        dados = yaml.safe_load(arquivo.read_text(encoding="utf-8")) or {}
        voz = (dados.get("canal") or {}).get("voz_edge", "")
        if voz and voz not in achadas:
            achadas.append(voz)
    padrao = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    voz = (padrao.get("canal") or {}).get("voz_edge", "")
    if voz and voz not in achadas:
        achadas.append(voz)
    return achadas


def duracao_s(caminho: Path) -> float:
    """Duracao do mp3, com ffprobe se houver e ffmpeg se nao houver.

    O runner do Actions tem ffmpeg e NAO tem ffprobe — descoberto na primeira
    execucao deste script, que sintetizou as doze vozes e perdeu todas na hora
    de medir. Sao dois binarios distintos e so um vem na imagem.
    """
    if probe := shutil.which("ffprobe"):
        saida = subprocess.run(
            [probe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(caminho)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return float(saida)

    # Sem ffprobe: decodifica para o vazio e le o `time=` final do stderr, que e
    # a duracao real processada.
    proc = subprocess.run(
        [_ffmpeg(), "-i", str(caminho), "-f", "null", "-"],
        capture_output=True, text=True,
    )
    marcas = re.findall(r"time=(\d+):(\d\d):(\d\d\.\d+)", proc.stderr)
    if not marcas:
        raise RuntimeError(f"nao consegui medir {caminho.name}:\n{proc.stderr[-400:]}")
    h, m, s = marcas[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def _ffmpeg() -> str:
    if achado := shutil.which("ffmpeg"):
        return achado
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


async def medir(voz: str, destino: Path) -> tuple[float, str, int]:
    import edge_tts

    idioma, texto = texto_da_voz(voz)
    mp3 = destino / f"{voz}.mp3"
    # Retentativa: o edge-tts recusa IP de datacenter de forma intermitente, e
    # uma recusa nao e motivo para deixar a voz sem taxa.
    for tentativa in range(4):
        try:
            await edge_tts.Communicate(texto, voz, rate=RATE).save(str(mp3))
            if mp3.exists() and mp3.stat().st_size > 0:
                break
        except Exception as e:
            if tentativa == 3:
                raise
            print(f"    tentativa {tentativa + 1} falhou ({e}) — repetindo", flush=True)
        await asyncio.sleep(3 * (tentativa + 1))
    return len(texto) / duracao_s(mp3), idioma, len(texto)


async def principal(vozes: list[str]) -> int:
    resultados: dict[str, tuple[float, str, int]] = {}
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        for voz in vozes:
            print(f"  medindo {voz}...", flush=True)
            try:
                resultados[voz] = await medir(voz, destino)
            except Exception as e:
                print(f"    FALHOU: {e}", flush=True)

    if not resultados:
        print("Nenhuma voz medida.", file=sys.stderr)
        return 1

    faltando = sorted({
        voz.split("-")[0].lower() for voz in resultados
    } - set(TEXTOS))
    print(f"\nrate={RATE}, texto na lingua de cada voz\n")
    print("Cole em src/maquina/stages/roteiro.py:\n")
    print("CHARS_POR_S = {")
    for voz, (taxa, idioma, n) in sorted(resultados.items()):
        print(f'    "{voz}": {taxa:.2f},  # {idioma}, {n} chars')
    print("}")

    maior = max(taxa for taxa, _, _ in resultados.values())
    print(
        f"\nMaior taxa medida: {maior:.2f} chars/s. O padrao de quem nao esta na "
        f"tabela precisa ser >= isso — assumir menos que a taxa real encurta o "
        f"video na mesma proporcao."
    )
    if faltando:
        print(
            f"\nATENCAO: sem texto proprio para {', '.join(faltando)} — medidas "
            f"em ingles, e a taxa em caracteres muda com o sistema de escrita. "
            f"Acrescente o idioma em TEXTOS antes de confiar nesses numeros."
        )
    return 0


if __name__ == "__main__":
    alvos = sys.argv[1:] or vozes_da_frota()
    print(f"{len(alvos)} voz(es) para medir.")
    sys.exit(asyncio.run(principal(alvos)))
