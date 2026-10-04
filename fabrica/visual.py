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

CENA COM FOOTAGE E OUTRA COISA, e isto custou um pacote em 04/10/2026. As
quatro medidas acima assumem CARTAO: fundo plano, texto por cima. Numa cena
`layout: "broll"` o quadro e uma FOTOGRAFIA escurecida, e `analisa` toma a cor
dominante dela como "fundo" e chama toda a variacao fotografica de "tinta" —
inclusive na borda. O seviye-seviye-010 foi reprovado em `t=333,9s` com 3,6% de
tinta na borda, e a tinta estava no TOPO (5,35%), na base (4,04%) e na direita
(4,61%), espalhada: era a estacao de trem do clipe, nao texto cortado. Nos
quadros de cartao do mesmo video a margem le 0,00% nos quatro lados.

E PIOR: antes disso o portao nao estava aprovando footage, estava sem ve-lo. A
amostragem e uniforme e as cenas de broll sao curtas (8 a 11 s em 556 a 728 s).
Medido nos tres pacotes com footage de 04/10: agla-level-009 teve ZERO dos 12
quadros sondados dentro de cena broll, resep-naik-level-010 tambem zero, e o
seviye-seviye-010 pegou um — e reprovou. Os dois primeiros passaram por sorte
de amostragem, nao por conferencia.

Por isso o portao agora faz duas coisas diferentes, e as duas APERTAM:

  * recebe `janelas_broll` e sonda UM quadro dentro de cada cena de footage,
    alem dos n uniformes. Cena com footage deixa de depender de sorte.
  * no quadro de footage, nao mede tinta/margem/fundo — mede o que de fato
    pode dar errado ali: se o lower-third e LEGIVEL sobre o clipe. O fundo de
    referencia e a cor dominante da propria faixa do lower-third, nao do quadro
    inteiro.

O fallback documentado do broll (lower-third sobre preto, quando o clipe nao
vem) continua passando, porque la o texto e perfeitamente legivel — e e isso
que a medida nova pergunta.

E A FRAQUEZA DESTA MEDIDA FICA DITA, porque ela e mais fraca que a do cartao e
isso nao deve ser descoberto depois. Na faixa do lower-third sobre footage, a
propria variacao do clipe conta como tinta: medido no seviye-seviye-010, as
quatro cenas deram 11,66%, 45,33%, 2,96% e 52,75% de tinta na faixa. Ou seja
`MIN_TINTA_LT` so pega o caso extremo — a faixa chapada, em que o texto nao
renderizou. Quem realmente julga aqui e o CONTRASTE (os quatro deram 265, 292,
379 e 238, contra um piso de 55). Este portao pega "o texto nao entrou" e "o
texto lavou"; ele NAO pega "o texto esta um pouco dificil de ler sobre um
clipe movimentado". Para isso ainda e preciso olhar o quadro.

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
RECONFERIR_S = 0.8        # quanto adiante reamostrar um quadro que mediu vazio
MIN_CONTRASTE = 70        # distancia RGB media entre tinta e fundo
MAX_DESVIO_FUNDO = 60     # distancia da cor dominante ate o fundo declarado

# Faixa do lower-third, medida a partir da base do quadro. E a unica regiao que
# importa num quadro de footage: e onde a fabrica desenha kicker e sub.
FAIXA_LT = 0.34
MIN_TINTA_LT = 0.004      # texto no lower-third. Mais baixo que MIN_TINTA do
                          # cartao porque a faixa e um terco do quadro e o texto
                          # ocupa parte dela; 0,00% continua reprovando.
MIN_CONTRASTE_LT = 55     # texto sobre clipe nunca tem o contraste de texto
                          # sobre fundo plano, mas abaixo disto nao se le.


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


def quadro_em(v, t):
    """Um quadro avulso no instante t. Custa uma decodificacao, entao so e
    usado para reconferir um quadro que ja acusou problema."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1",
         "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True)
    px = W * H * 3
    return r.stdout[:px] if len(r.stdout) >= px else None


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


def analisa_lt(q):
    """Mede SO a faixa do lower-third, contra o fundo dela mesma.

    Num quadro de footage nao existe "o fundo do quadro": existe o clipe. Mas
    existe uma pergunta que decide se a cena presta — o texto sobre o clipe da
    para ler? Essa pergunta se responde na faixa onde o texto esta, e com a cor
    dominante DESSA faixa como referencia.
    """
    y0 = int(H * (1 - FAIXA_LT))
    conta = Counter()
    for y in range(y0, H, 3):
        for x in range(0, W, 5):
            o = (y * W + x) * 3
            conta[(q[o] // 12, q[o + 1] // 12, q[o + 2] // 12)] += 1
    bal = conta.most_common(1)[0][0]
    fundo = (bal[0] * 12 + 6, bal[1] * 12 + 6, bal[2] * 12 + 6)

    tinta = total = 0
    soma_d = 0
    for y in range(y0, H, 2):
        for x in range(0, W, 2):
            o = (y * W + x) * 3
            d = dist((q[o], q[o + 1], q[o + 2]), fundo)
            total += 1
            if d > 90:
                tinta += 1
                soma_d += d
    return {
        "fundo": fundo,
        "tinta": tinta / max(total, 1),
        "contraste": (soma_d / tinta) if tinta else 0,
    }


def _em_janela(t, janelas):
    for a, b in janelas or ():
        if a <= t <= b:
            return True
    return False


def conferir(video, fundo_esperado=None, n=QUADROS, janelas_broll=None):
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
        onde = f"t={t:.1f}s"
        # QUADRO DE FOOTAGE: as quatro medidas de cartao nao se aplicam, e
        # aplica-las reprova video bom (ver o docstring). Mede-se o
        # lower-third.
        if _em_janela(t, janelas_broll):
            tintas.pop()
            lt = analisa_lt(q)
            fl = lt["fundo"]
            print(f"{t:>7.1f} {'broll':>6}  {lt['tinta']*100:>6.2f}% "
                  f"{lt['contraste']:>6.0f}  #{fl[0]:02X}{fl[1]:02X}{fl[2]:02X}"
                  f"  (lower-third)")
            if lt["tinta"] < MIN_TINTA_LT:
                erros.append(f"{onde}: cena de footage sem texto legivel no "
                             f"lower-third ({lt['tinta']*100:.2f}% de tinta na "
                             f"faixa) — o clipe entrou e o texto nao")
            elif lt["contraste"] < MIN_CONTRASTE_LT:
                erros.append(f"{onde}: lower-third com contraste "
                             f"{lt['contraste']:.0f} sobre o clipe — o texto "
                             f"existe e nao se le em cima do footage")
            continue
        print(f"{t:>7.1f} {m['tinta']*100:>6.2f}% {m['margem']*100:>6.2f}% "
              f"{m['contraste']:>6.0f}  #{f[0]:02X}{f[1]:02X}{f[2]:02X}")
        # A amostragem e uniforme e nao sabe onde as cenas comecam, entao um
        # quadro pode cair na janela de entrada da animacao — nos primeiros
        # ~0,45s de uma cena em camadas ainda nao ha elemento nenhum na tela, e
        # medir zero ali e o comportamento correto da fabrica, nao defeito.
        # Aconteceu duas vezes seguidas em seja-mais-magra-001, no mesmo
        # t=732,4s: a cena 72 comeca em 732,1s e mede 0,00% a 0,3s dela, 4,94%
        # a 1,0s e 5,22% a 2,9s. Sem esta reconferencia o teste reprova um video
        # perfeito, e reprovar bom video ensina a ignorar o teste.
        if m["tinta"] < MIN_TINTA:
            q2 = quadro_em(video, min(t + RECONFERIR_S, d - 0.1))
            if q2:
                m2 = analisa(q2)
                if m2["tinta"] >= MIN_TINTA:
                    print(f"{'':>7} {m2['tinta']*100:>6.2f}%  (reconferido a "
                          f"+{RECONFERIR_S}s: a cena renderiza, o quadro caiu na "
                          f"entrada da animacao)")
                    tintas[-1] = m2["tinta"]
                    m = m2
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
    # CADA CENA DE FOOTAGE RECEBE UMA SONDA PROPRIA, e isto APERTA o portao.
    # A amostragem uniforme nao cobre cena curta: medido em 04/10/2026, o
    # agla-level-009 e o resep-naik-level-010 tiveram ZERO dos 12 quadros dentro
    # de cena broll, com tres cenas de footage cada. Passaram sem serem
    # conferidos. Um quadro por janela custa uma decodificacao e tira a sorte
    # da conta.
    for a_, b_ in (janelas_broll or ()):
        meio = (a_ + b_) / 2
        if any(abs(meio - d * (i + 0.5) / len(qs)) < (b_ - a_) / 2
               for i in range(len(qs))):
            continue                      # a amostra uniforme ja caiu aqui
        q = quadro_em(video, min(meio, d - 0.1))
        if not q:
            avisos.append(f"t={meio:.1f}s: nao consegui sondar a cena de footage")
            continue
        lt = analisa_lt(q)
        fl = lt["fundo"]
        print(f"{meio:>7.1f} {'broll':>6}  {lt['tinta']*100:>6.2f}% "
              f"{lt['contraste']:>6.0f}  #{fl[0]:02X}{fl[1]:02X}{fl[2]:02X}"
              f"  (sonda da cena)")
        if lt["tinta"] < MIN_TINTA_LT:
            erros.append(f"t={meio:.1f}s: cena de footage sem texto legivel no "
                         f"lower-third ({lt['tinta']*100:.2f}% de tinta na faixa) "
                         f"— o clipe entrou e o texto nao")
        elif lt["contraste"] < MIN_CONTRASTE_LT:
            erros.append(f"t={meio:.1f}s: lower-third com contraste "
                         f"{lt['contraste']:.0f} sobre o clipe — o texto existe e "
                         f"nao se le em cima do footage")

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
