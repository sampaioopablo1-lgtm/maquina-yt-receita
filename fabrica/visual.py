#!/usr/bin/env python3
"""Teste de fumaca visual: alguem finalmente olha o quadro.

Todas as outras etapas medem se o video SAIU — duracao, tamanho, md5, soma dos
clipes. Nenhuma media se ele esta VISIVEL. As duas queixas visuais que chegaram
ao dono passaram por todos os asserts: cor invertida na cena de CTA, e legenda
queimada saindo VAZIA em hindi porque a fonte nao tinha o script devanagari. Nos
dois casos o arquivo estava perfeito e o video, nao.

Isto amostra quadros do mp4 pronto e mede quatro coisas por quadro:

  tinta      fracao de pixels que diferem do fundo. Perto de zero e cena que
             nao renderizou; muito alta sugere fundo errado.
  margem     tinta na faixa externa. Texto encostando na borda foi cortado ou
             vai ser, dependendo do player.
  contraste  distancia media da tinta ate o fundo. Texto que existe no arquivo
             e some na tela cai aqui.
  fundo      a cor dominante e a do canal? Pega inversao de paleta.

Uso:  python3 visual.py <video.mp4> [--fundo RRGGBB] [--quadros 12]
Sai 1 se houver ERRO.
"""
import re
import subprocess
import sys
from collections import Counter

W, H = 640, 360           # amostra reduzida: o que se mede aqui e area, nao nitidez
QUADROS = 12
MARGEM_PCT = 0.04         # faixa externa considerada "borda"

MIN_TINTA = 0.0015        # abaixo disto o quadro esta praticamente vazio. Baixo de
                          # proposito: uma cena legitima pode ter so o kicker, e nos
                          # primeiros 0,45s de uma cena em camadas nenhum elemento
                          # entrou ainda. Render que falhou de verdade da 0,00%.
MIN_TINTA_MEDIANA = 0.02  # o piso acima julga um quadro; este julga o video inteiro.
                          # Cena com kicker mede ~6% de tinta, cena sem texto ~0,9%.
MAX_TINTA = 0.62          # acima disto o fundo provavelmente nao e o fundo
MAX_MARGEM = 0.012        # tinta encostada na borda
MIN_CONTRASTE = 70        # distancia RGB media entre tinta e fundo
MAX_DESVIO_FUNDO = 60     # distancia da cor dominante ate o fundo declarado


def duracao(v):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", v], capture_output=True, text=True)
    return float(r.stdout.strip())


def quadros(v, n=QUADROS):
    """Um unico passe do ffmpeg devolve os n quadros ja reduzidos.

    Amostrar com -ss por quadro custaria n decodificacoes; aqui e uma so.
    """
    d = duracao(v)
    fps = n / d
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", v, "-vf", f"fps={fps},scale={W}:{H}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True)
    px = W * H * 3
    return [r.stdout[i:i + px] for i in range(0, len(r.stdout) - px + 1, px)], d


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def analisa(q):
    """Mede um quadro. O fundo e a cor dominante do proprio quadro — nao da
    para assumir a paleta, porque um quadro com fundo errado tambem precisa
    ser medido contra o que ele de fato tem."""
    conta = Counter()
    for i in range(0, len(q) - 2, 3 * 7):        # amostragem esparsa: cor dominante
        conta[(q[i] // 12, q[i + 1] // 12, q[i + 2] // 12)] += 1
    bal = conta.most_common(1)[0][0]
    fundo = (bal[0] * 12 + 6, bal[1] * 12 + 6, bal[2] * 12 + 6)

    tinta = borda = fraco = 0
    soma_d = 0
    total = borda_total = 0
    mx, my = int(W * MARGEM_PCT), int(H * MARGEM_PCT)
    for y in range(0, H, 2):
        na_borda = y < my or y >= H - my
        for x in range(0, W, 2):
            o = (y * W + x) * 3
            p = (q[o], q[o + 1], q[o + 2])
            d = dist(p, fundo)
            eh_tinta = d > 90
            total += 1
            if eh_tinta:
                tinta += 1
                soma_d += d
            elif d > 22:
                # Nem fundo nem tinta: ha ALGO desenhado ali, so que perto demais
                # do fundo para ser lido. Contar isto separado e o que distingue
                # "a cena nao renderizou" de "a cena renderizou e some na tela" —
                # dois defeitos com a mesma aparencia no total de tinta.
                fraco += 1
            if na_borda or x < mx or x >= W - mx:
                borda_total += 1
                if eh_tinta:
                    borda += 1
    return {
        "fundo": fundo,
        "tinta": tinta / total,
        "margem": borda / max(borda_total, 1),
        "contraste": (soma_d / tinta) if tinta else 0,
        "fraco": fraco / total,
    }


def conferir(video, fundo_esperado=None, n=QUADROS):
    qs, d = quadros(video, n)
    erros, avisos = [], []
    tintas = []
    print(f"{video}  {d:.1f}s  {len(qs)} quadros")
    print(f"{'t(s)':>7} {'tinta':>7} {'margem':>7} {'contr':>6}  fundo")
    for i, q in enumerate(qs):
        m = analisa(q)
        tintas.append(m["tinta"])
        t = d * (i + 0.5) / len(qs)
        f = m["fundo"]
        print(f"{t:>7.1f} {m['tinta']*100:>6.2f}% {m['margem']*100:>6.2f}% "
              f"{m['contraste']:>6.0f}  #{f[0]:02X}{f[1]:02X}{f[2]:02X}")
        onde = f"t={t:.1f}s"
        if m["tinta"] < MIN_TINTA:
            if m["fraco"] > MIN_TINTA * 2:
                erros.append(f"{onde}: ha desenho, mas nenhum contraste legivel "
                             f"({m['fraco']*100:.2f}% de pixels quase iguais ao fundo) "
                             f"— a cena renderizou e some na tela")
            else:
                erros.append(f"{onde}: quadro praticamente vazio ({m['tinta']*100:.2f}% de tinta) "
                             f"— cena nao renderizou ou legenda saiu vazia")
        elif m["tinta"] > MAX_TINTA:
            avisos.append(f"{onde}: {m['tinta']*100:.0f}% de tinta — fundo provavelmente errado")
        if m["margem"] > MAX_MARGEM:
            erros.append(f"{onde}: {m['margem']*100:.1f}% de tinta na borda — texto cortado ou encostando")
        if m["tinta"] >= MIN_TINTA and m["contraste"] < MIN_CONTRASTE:
            erros.append(f"{onde}: contraste {m['contraste']:.0f} — texto existe no arquivo mas some na tela")
        if fundo_esperado and dist(f, fundo_esperado) > MAX_DESVIO_FUNDO:
            avisos.append(f"{onde}: fundo #{f[0]:02X}{f[1]:02X}{f[2]:02X} nao e o do canal "
                          f"#{fundo_esperado[0]:02X}{fundo_esperado[1]:02X}{fundo_esperado[2]:02X}")
    # MIN_TINTA julga um quadro de cada vez, e por bom motivo e frouxo. Mas um
    # video pode estar vazio sem que nenhum quadro sozinho encoste no piso: em
    # seja-mais-magra-001, 59 das 76 cenas foram escritas sem `kicker`, entao a
    # fabrica desenhou so o fundo e a legenda queimada. Deu 0,88% de tinta
    # quadro apos quadro — seis vezes acima do piso individual, e ainda assim
    # doze minutos de tela cinza. Passou no teste; so nao passou porque UMA
    # cena deu 0,00% por acidente.
    #
    # A mediana denuncia o que o minimo nao ve. Cena legitima com kicker mede
    # ~6% de tinta; cena sem texto mede ~0,9%. O corte em 2% separa as duas sem
    # ambiguidade, e a mediana (nao a media) aguenta um ou outro quadro escuro
    # de transicao sem reprovar o video inteiro.
    if tintas:
        med = sorted(tintas)[len(tintas) // 2]
        if med < MIN_TINTA_MEDIANA:
            erros.append(
                f"mediana de tinta {med*100:.2f}% em {len(tintas)} quadros "
                f"(minimo aceitavel {MIN_TINTA_MEDIANA*100:.0f}%) — o video esta "
                f"quase vazio do inicio ao fim; provavelmente faltou `kicker` nas cenas")
    for a in avisos:
        print(f"  aviso  {a}")
    for e in erros:
        print(f"  ERRO   {e}")
    print(f"  -> {len(erros)} erro(s), {len(avisos)} aviso(s)")
    return erros, avisos


def hexcor(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fundo = None
    if "--fundo" in sys.argv:
        fundo = hexcor(sys.argv[sys.argv.index("--fundo") + 1])
    n = QUADROS
    if "--quadros" in sys.argv:
        n = int(sys.argv[sys.argv.index("--quadros") + 1])
    erros, _ = conferir(args[0], fundo, n)
    sys.exit(1 if erros else 0)
