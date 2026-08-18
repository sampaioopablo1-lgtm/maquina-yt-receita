import json, subprocess, sys, os, asyncio
import cairosvg, edge_tts

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from maquina.media import duracao as _duracao, ffmpeg_bin  # fallback pro binario estatico do imageio-ffmpeg

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def wrap(t, n):
    """Quebra por ESPACO. Palavra maior que `n` fica inteira numa linha so —
    e por isso `n` nunca garantiu largura; quem garante e `corpo_que_cabe`.

    O `if cur` na primeira palavra existe porque sem ele uma palavra sozinha
    maior que `n` devolvia ['', 'LabTreinamento']: a linha vazia virava um
    <tspan> que empurrava o bloco inteiro uma entrelinha para baixo, e para
    baixo e onde o Ken Burns corta. Achado pelo teste, nao em producao.
    """
    out, cur = [], ''
    for w in t.split():
        if cur and len(cur)+len(w)+1 > n: out.append(cur); cur = w
        else: cur = (cur+' '+w).strip()
    if cur: out.append(cur)
    return out

# Fonte do canal. O padrao cobre latino, grego e cirilico, mas nao tem
# devanagari: em hindi o cairosvg desenhava os glifos soltos (o halant ficava
# visivel e a matra caia do lado errado) e a legenda queimada saia VAZIA, porque
# nao havia nenhuma fonte com o script instalada. Specs em hindi declaram
# "fonte": "Noto Sans Devanagari", e ai os dois motores passam a shapear.
FONTE = "DejaVu Sans"

# Largura media de um glifo bold em fracao do corpo. MEDIDA, nao estimada:
# "LabTreinamento" com corpo 108 rasterizou 981 px de tinta em 14 caracteres,
# o que da 0,649. 0,62 fica abaixo do medido de proposito — errar para menos
# aqui encolhe um texto que caberia; errar para mais deixa tinta na borda.
LARGURA_GLIFO = 0.62

# A faixa que o Ken Burns corta MAIS a borda de 4% do visual.py: e a mesma
# conta do `layout.corte_do_ken_burns`, e o desenho tem de respeitar o que o
# portao mede. Repetida aqui como numero porque o layout.py importa este
# modulo, e nao o contrario.
MARGEM_SEGURA = 0.1204
LARGURA_SEGURA = 1 - 2 * MARGEM_SEGURA


def corpo_que_cabe(t, n, size, largura):
    """Maior corpo ate `size` em que a linha mais larga cabe em `largura`.

    `wrap` divide por ESPACO e nunca parte uma palavra: 'LabTreinamento' com
    n=11 sai numa linha de 14 caracteres, e o `n` que parecia limitar a largura
    nao limita nada. Medido em 17/08/2026 no labtreinamento-002 short cena 4 —
    tinta de x=49 a x=1030 num quadro de 1080, com a zona segura em 130..950.

    Por isso a largura passa a ser conferida DEPOIS da quebra, contra a linha
    que realmente saiu, do mesmo jeito que a `geometria_thumb` ja encolhia o
    titulo em vez de escolher entre dois degraus fixos.
    """
    maior = max((len(l) for l in wrap(t, n)), default=0)
    if not maior or largura <= 0:
        return size
    return min(size, largura / (maior * LARGURA_GLIFO))


def texto_na_caixa(t, cx, cy, largura, altura, fill, n=12, corpo_max=None, lh=1.25):
    """Texto centrado numa caixa, encolhido ate caber nos DOIS eixos.

    O campo `preco` foi desenhado para caber um preco, e chega frase: no
    setiap-level-005 cena 60 ele vale 'dari lima koma enam tiga ke tiga koma
    sembilan sembilan' — 54 caracteres que com n=12 viram cinco linhas. Elas
    desciam de 0,59H ate 0,957H, transbordando a propria tarja e entrando na
    borda que o Ken Burns corta.

    Encolher e melhor do que cortar: o numero continua legivel, e nenhuma spec
    precisa ser reescrita para o desenho parar de estourar.
    """
    corpo = corpo_max or altura * 0.5
    linhas = wrap(t, n) or ['']
    corpo = min(corpo, corpo_que_cabe(t, n, corpo, largura),
                altura / (1 + (len(linhas) - 1) * lh) * 0.82)
    # `y` da PRIMEIRA linha: sobe metade do bloco e desce a altura de uma maiuscula.
    alt = corpo * (1 + (len(linhas) - 1) * lh)
    return tsp(t, cx, cy - alt / 2 + corpo * 0.78, corpo, fill, n=n, lh=lh)


def tsp(t, x, y, size, fill, n=30, anchor='middle', lh=1.25, subindo=False,
        largura=None):
    """`subindo=True` ancora `y` na ULTIMA linha, e nao na primeira.

    O texto que quebra cresce para baixo, e embaixo e onde o Ken Burns corta.
    Medido em 17/08/2026: o rotulo de barra 'antes: caixa aleatoria' quebra em
    duas linhas a partir de y=0,865H e poe tinta ate 0,912H — dentro da zona de
    risco, que comeca em 0,88H. Com `subindo` a segunda linha fica onde a unica
    ficaria, e a primeira sobe: o bloco cresce para dentro do quadro.
    """
    linhas = wrap(t, n) or ['']
    if largura:
        size = corpo_que_cabe(t, n, size, largura)
    topo = y - int(size * lh) * (len(linhas) - 1) if subindo else y
    o = f'<text x="{x}" y="{topo}" font-family="{FONTE}" font-weight="bold" font-size="{int(size)}" fill="{fill}" text-anchor="{anchor}">'
    for i, l in enumerate(linhas):
        o += f'<tspan x="{x}" dy="{0 if i==0 else int(size*lh)}">{esc(l)}</tspan>'
    return o + '</text>'

W_THUMB = 1280          # a capa e sempre 16:9, mesmo em canal de retrato

_LARG_REF = 100.0       # corpo em que a largura e medida uma vez por string
_LARG_CACHE = {}


def largura_do_texto(t, size):
    """Largura em pixels da linha `t` no corpo `size` — MEDIDA, nao estimada.

    `LARGURA_GLIFO = 0,62` foi medido em 'LabTreinamento', que e caixa mista, e
    a constante virou a largura de TODO texto. Medido em 18/08/2026 na propria
    fonte de producao, a razao real varia por um fator de tres:

        iiiiiiiiii .............. 0,324
        10.685 ................... 0,614
        LabTreinamento ........... 0,649
        BERAPA LAMA? ............. 0,704      <- maiuscula
        MILHOES .................. 0,704
        WWWWWWWWWW ............... 1,094

    Com 0,62 para tudo, 'BERAPA LAMA?' foi calculado em 1.101 px e saiu com
    1.251: a capa do setiap-level-007 renderizou com as duas pontas cortadas
    pela moldura. Nenhum portao viu, porque `analisa_thumb` so conferia a faixa
    VERTICAL da tinta.

    A largura de uma fonte vetorial escala linear com o corpo, entao basta uma
    rasterizacao por string — no corpo de referencia — e uma regra de tres. O
    cache existe porque a busca de corpo em `geometria_thumb` reavalia as
    mesmas linhas dezenas de vezes.
    """
    if not t:
        return 0.0
    chave = (t, FONTE)
    if chave not in _LARG_CACHE:
        _LARG_CACHE[chave] = _mede_largura(t, _LARG_REF)
    return _LARG_CACHE[chave] * size / _LARG_REF


def _mede_largura(t, size):
    """Largura da tinta de `t`, rasterizando uma vez. Sem PIL cai na estimativa."""
    alt = int(size * 2)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="6000" height="{alt}">'
           f'<rect width="6000" height="{alt}" fill="#FFFFFF"/>'
           f'<text x="20" y="{int(size)}" font-family="{FONTE}" font-weight="bold" '
           f'font-size="{int(size)}" fill="#000000">{esc(t)}</text></svg>')
    try:
        import io

        from PIL import Image
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=6000,
                               output_height=alt)
        im = Image.open(io.BytesIO(png)).convert("L")
        caixa = im.point(lambda v: 255 if v < 128 else 0).getbbox()
        if caixa:
            return float(caixa[2] - caixa[0])
    except Exception:
        pass
    return len(t) * size * LARGURA_GLIFO


def quebra_por_largura(t, size, largura):
    """Quebra `t` em linhas que cabem em `largura` PIXELS no corpo `size`.

    `wrap` recebe um numero de CARACTERES, que nao e largura: 'IIIII' e 'WWWWW'
    tem cinco caracteres e larguras muito diferentes. Aqui a contagem sai da
    largura util dividida pela largura media de glifo — o mesmo 0,62 medido em
    'LabTreinamento' e ja usado pelo `corpo_que_cabe`.

    Uma palavra sozinha maior que o limite continua inteira numa linha, porque
    `wrap` nunca parte palavra. Quem garante a largura nesse caso e a busca de
    corpo em `geometria_thumb`, que desce ate a palavra caber.
    """
    if not t:
        return []
    out, cur = [], ''
    for w in t.split():
        cand = (cur + ' ' + w).strip()
        if cur and largura_do_texto(cand, size) > largura:
            out.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        out.append(cur)
    return _sem_orfao(out, size, largura)


def _sem_orfao(linhas, size, largura):
    """Nenhuma linha termina numa palavrinha de ate dois caracteres.

    "10.685 x 4.503" quebrava em "10.685 x" / "4.503": o `x` da comparacao —
    que E o video — ficava pendurado no fim da primeira linha, longe do segundo
    numero. "$32 = 5 COMIDAS" quebrava em "$32 = 5" / "COMIDAS" pelo mesmo
    motivo, com o `=` e o `5` separados do que eles igualam.

    A palavrinha desce para a linha seguinte, e so quando as tres condicoes
    valem: a linha tem mais de uma palavra (senao ela ficaria vazia), existe
    linha seguinte, e a linha seguinte continua cabendo depois de receber.
    Sem a terceira condicao o conserto do orfao vira um estouro de largura.
    """
    linhas = list(linhas)
    for i in range(len(linhas) - 1):
        for _ in range(3):                  # "$32 = 5" precisa de duas passadas
            palavras = linhas[i].split()
            if len(palavras) < 2 or len(palavras[-1]) > 2:
                break
            if largura_do_texto(f"{palavras[-1]} {linhas[i + 1]}", size) > largura:
                break
            linhas[i] = " ".join(palavras[:-1])
            linhas[i + 1] = f"{palavras[-1]} {linhas[i + 1]}"
    return linhas


def tsp_linhas(linhas, x, y, size, fill, lh=1.25):
    """Igual ao `tsp`, mas recebe as linhas PRONTAS em vez de quebrar de novo.

    Existe para a thumbnail: quem mede e quem desenha tem de olhar para as
    mesmas linhas, e o `tsp` so aceita texto solto mais um `n`.
    """
    if not linhas:
        return ''
    o = (f'<text x="{x}" y="{y}" font-family="{FONTE}" font-weight="bold" '
         f'font-size="{int(size)}" fill="{fill}" text-anchor="middle">')
    for i, l in enumerate(linhas):
        o += f'<tspan x="{x}" dy="{0 if i == 0 else int(size * lh)}">{esc(l)}</tspan>'
    return o + '</text>'


def geometria_thumb(th, H=720):
    """Onde cada linha da thumbnail comeca e termina, em pixel.

    Vive separado do desenho porque o PORTAO precisa da mesma conta. Medir a
    imagem pronta nao serve: renderizar uma linha de cada vez para comparar as
    faixas muda a geometria — ela depende das duas — e o portao reprovava as
    dezenove specs, inclusive as boas. Tentei desse jeito primeiro.

    Devolve tambem `topo` e `base` de cada bloco, que e o que o portao compara,
    e as LINHAS ja quebradas — quem desenha tem de usar exatamente estas, senao
    a conta e o desenho divergem e a colisao volta por outro caminho.
    """
    MARGEM, GAP, LH = 40, 54, 1.25
    disponivel = H - 2 * MARGEM

    # Antes: `wrap(l1, 12)` e `wrap(l2, 16)`, e uma escada que so ENCOLHIA a
    # partir de 150. Duas consequencias medidas em 18/08/2026 nas vinte e
    # quatro specs de producao:
    #
    #   1. as vinte e quatro paravam em s1=150, o teto. A escada nunca disparou
    #      uma vez sequer. "61 HORAS" — sete caracteres — saia no mesmo corpo
    #      de um titulo de duas linhas, com metade do quadro em branco. Numa
    #      capa, branco sobrando e legibilidade jogada fora: no feed ela aparece
    #      com 120 px de altura, e ali so o tamanho decide.
    #
    #   2. quebrar por CONTAGEM DE CARACTERE erra onde importa. "10.685 x 4.503"
    #      com n=12 vira "10.685 x" / "4.503": o `x` da comparacao fica orfao no
    #      fim da primeira linha, e a comparacao — que e o video inteiro — se
    #      parte no meio. "BERTAHAN BERAPA LAMA?" vira "BERTAHAN BERAPA" /
    #      "LAMA?" pelo mesmo motivo.
    #
    # Agora a busca vai do maior para o menor e a quebra e por LARGURA MEDIDA,
    # com o mesmo LARGURA_GLIFO de 0,62 que o `corpo_que_cabe` usa. O primeiro
    # corpo que cabe nos DOIS eixos vence, entao titulo curto cresce e titulo
    # longo encolhe — sem escada, sem degrau, e sem teto artificial em 150.
    #
    # TETO=300 nao e estetica, e o limite em que uma palavra de cinco letras
    # ainda cabe na largura util (1200 / (5 x 0,62) = 387, com folga).
    # RESPIRO: sem ele o texto cabe na conta e encosta na moldura. 'BERAPA
    # LAMA?' saia de ponta a ponta do branco, tecnicamente dentro e visualmente
    # espremido — e uma letra a mais de folga vira corte no player.
    TETO, PISO, PROPORCAO, RESPIRO = 300, 40, 0.60, 28
    largura = W_THUMB - 2 * MARGEM - 2 * RESPIRO

    s1 = PISO
    l1 = quebra_por_largura(th.get("l1", ""), PISO, largura)
    l2 = quebra_por_largura(th.get("l2", ""), int(PISO * PROPORCAO), largura)
    for corpo in range(TETO, PISO - 1, -2):
        s2c = max(1, int(corpo * PROPORCAO))
        c1 = quebra_por_largura(th.get("l1", ""), corpo, largura)
        c2 = quebra_por_largura(th.get("l2", ""), s2c, largura)
        a1 = corpo + max(0, len(c1) - 1) * int(corpo * LH) if c1 else 0
        a2 = s2c + max(0, len(c2) - 1) * int(s2c * LH) if c2 else 0
        # A ALTURA cabendo nao basta: `wrap` nunca parte palavra, entao uma
        # palavra sozinha maior que a largura util atravessa a moldura sem
        # alterar a contagem de linhas. E o que cortava 'BERAPA LAMA?'.
        cabe_largura = (max((largura_do_texto(l, corpo) for l in c1), default=0) <= largura
                        and max((largura_do_texto(l, s2c) for l in c2), default=0) <= largura)
        if cabe_largura and a1 + (GAP if c1 and c2 else 0) + a2 <= disponivel:
            s1, l1, l2 = corpo, c1, c2
            break

    s2 = max(1, int(s1 * PROPORCAO))
    alt1 = s1 + max(0, len(l1) - 1) * int(s1 * LH) if l1 else 0
    alt2 = s2 + max(0, len(l2) - 1) * int(s2 * LH) if l2 else 0
    total = alt1 + (GAP if l1 and l2 else 0) + alt2

    topo = MARGEM + (disponivel - total) / 2
    base1 = topo + alt1
    topo2 = base1 + (GAP if l1 and l2 else 0)
    return {
        "margem": MARGEM, "lh": LH, "gap": GAP,
        "s1": s1, "s2": s2,
        "y1": topo + s1 * 0.78, "y2": topo2 + s2 * 0.78,
        "topo1": topo, "base1": base1,
        "topo2": topo2, "base2": topo2 + alt2,
        "linhas1": len(l1), "linhas2": len(l2),
        "l1": l1, "l2": l2,
    }


def svg_thumb(th, pal, W=1280, H=720):
    """A thumbnail, com as duas linhas posicionadas por CALCULO.

    Antes as posicoes eram fixas: l1 em y=300 com corpo 150, l2 em y=480. Com
    entrelinha de 1,25 a segunda linha de l1 cai em 487 — sete pixels DEPOIS
    do topo de l2. Toda thumbnail cujo l1 quebrasse em duas linhas saia com os
    textos empilhados um sobre o outro, ilegivel.

    Estava assim em todo pacote e nenhum portao via: o layout.py mede as CENAS
    e o visual.py amostra o VIDEO. A thumbnail nao passava por nenhum dos dois
    — e ela e a unica imagem que decide se alguem clica.

    Aqui o bloco inteiro e medido antes de ser posicionado, e centrado na caixa
    branca. O corpo de l1 encolhe quando o texto e longo, para o bloco nao
    transbordar em vez de colidir.
    """
    g = geometria_thumb(th, H)
    s1, y1, s2, y2 = g["s1"], g["y1"], g["s2"], g["y2"]
    MARGEM, LH = g["margem"], g["lh"]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" fill="{pal["c1"]}"/>'
        f'<rect x="{MARGEM}" y="{MARGEM}" width="{W - 2 * MARGEM}" '
        f'height="{H - 2 * MARGEM}" fill="#FFFFFF"/>'
        # As LINHAS vem da geometria, nao de um `wrap` repetido aqui com outro
        # `n`. Era assim antes (n=12 e n=16) e funcionava por coincidencia: bastava
        # a conta e o desenho discordarem de uma linha para o portao aprovar uma
        # capa que sai colidindo.
        + tsp_linhas(g["l1"], W // 2, y1, s1, pal["ink"], lh=LH)
        + tsp_linhas(g["l2"], W // 2, y2, s2, pal["c1"], lh=LH)
        + '</svg>'
    )


def usar_fonte(nome):
    """Troca a fonte do canal e CONFERE que ela existe. Sem a conferencia, uma
    fonte ausente nao da erro: o SVG cai num fallback qualquer e a legenda
    queimada sai vazia — defeito que so aparece assistindo ao video pronto.
    A fonte vive em ~/.fonts do sandbox, entao some quando ele recicla."""
    global FONTE, EST
    if not nome:
        return
    fams = subprocess.run(["fc-list","--format=%{family}\n"], capture_output=True, text=True).stdout
    if nome not in fams:
        raise RuntimeError(
            f"fonte '{nome}' nao instalada no sandbox. Instale em ~/.fonts e rode fc-cache -f. "
            "Sem ela a legenda queimada sai VAZIA e o texto de tela sai sem shaping.")
    EST = EST.replace(f"FontName={FONTE}", f"FontName={nome}")
    FONTE = nome

def elementos(c):
    """Quantos elementos desta cena entram em cena separadamente.

    Zero significa cena de uma peca so — ela vai inteira no fundo. Acima de
    zero, `svg_cena(..., camada=k)` devolve o k-esimo elemento sozinho, sobre
    tela transparente, e quem monta o clipe faz cada um entrar no seu tempo.
    """
    lay = c.get('layout', 'titulo')
    if lay == 'broll':
        # Uma peca so: o movimento da cena vem do proprio footage, nao de
        # camadas entrando. Zero manda o clipe_cena para o ramo simples.
        return 0
    if lay in ('lista', 'barras'):
        return len(c.get('itens', []))
    if lay in ('titulo', 'cta'):
        return 2 if c.get('sub') else 1
    if lay == 'item':
        return 2 if c.get('preco') else 1
    return 0


def svg_cena_retrato(c, pal, W, H):
    """Cena 9:16 com geometria propria, dimensionada pela LARGURA.

    O svg_cena dimensiona fonte e formas por H, que em paisagem e o lado
    menor. Em retrato H e o lado MAIOR: o circulo do layout `item` saia com
    borda esquerda em x negativo e o kicker de `titulo` nao cabia na largura.
    O visual.py pegou 6/6 quadros do short com tinta na borda (3-6,3%) — e os
    shorts anteriores foram publicados assim, porque so o longo era conferido.
    Medido no kp-plan-9233: esta geometria devolve margem 0,00%.
    """
    ink, c1, c2 = pal['ink'], pal['c1'], pal['c2']
    bg = pal.get('bg', '#FFFFFF'); lay = c.get('layout', 'titulo')
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    s += f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    cx = W // 2
    if lay in ('titulo', 'cta'):
        fg = c1 if lay == 'titulo' else c2
        big = c.get('kicker', '')
        s += tsp(big, cx, H*0.40, W*(0.15 if len(big) <= 8 else 0.10), fg, n=11,
                 largura=W*LARGURA_SEGURA)
        s += f'<path d="M {cx-W*0.30} {H*0.50} Q {cx} {H*0.52}, {cx+W*0.30} {H*0.50}" stroke="{c2 if lay=="titulo" else c1}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        if c.get('sub'):
            s += tsp(c['sub'], cx, H*0.58, W*0.055, ink, n=22, largura=W*LARGURA_SEGURA)
    elif lay == 'item':
        s += f'<circle cx="{cx}" cy="{H*0.28}" r="{W*0.24}" fill="none" stroke="{ink}" stroke-width="8"/>'
        s += f'<circle cx="{cx}" cy="{H*0.28}" r="{W*0.15}" fill="{c2}" opacity="0.55"/>'
        s += tsp(c.get('kicker', ''), cx, H*0.50, W*0.085, ink, n=14,
                 largura=W*LARGURA_SEGURA)
        if c.get('preco'):
            s += f'<rect x="{cx-W*0.26}" y="{H*0.56}" width="{W*0.52}" height="{H*0.075}" fill="{c1}"/>'
            s += texto_na_caixa(c['preco'], cx, H*0.5975, W*0.50, H*0.075,
                                '#FFFFFF', n=12, corpo_max=W*0.075)
    elif lay == 'lista':
        s += tsp(c.get('kicker', ''), cx, H*0.16, W*0.08, ink, n=16, largura=W*LARGURA_SEGURA)
        y = H * 0.30
        for i, it in enumerate(c.get('itens', [])):
            col = [c1, c2, ink][i % 3]
            # O bullet em 0,12W com raio 0,022W comeca em 0,098W, e a zona
            # segura so comeca em 0,1204W: a bolinha encostava na borda mesmo
            # com o texto curto. Medido no setiap-level-004 short cena 1.
            s += f'<circle cx="{W*0.15}" cy="{y-H*0.012}" r="{W*0.022}" fill="{col}"/>'
            # n=26 a corpo 0,055W chegava a x=1038 num quadro de 1080, e o pan
            # horizontal poe a faixa direita a partir de 1013. Medido no
            # setiap-level-004 short cena 1: 1,03%. Aqui a conta e pela LARGURA,
            # que em retrato e o lado curto — cabem 22 caracteres, nao 26.
            s += tsp(it, W*0.18, y, W*0.05, ink, n=22, anchor='start',
                     largura=W*(1 - 0.18 - MARGEM_SEGURA))
            y += H * 0.10
    elif lay == 'barras':
        labs = c.get('itens', ['1', '2', '3', '4']); n = len(labs); bw = W*0.76/n
        alt = c.get('alturas')
        # 0,14H com corpo 0,08W punha o ascender em 0,106H, e a faixa de topo do
        # pan vertical so termina em 0,116H. Mesmo defeito do 16:9, outra conta.
        s += tsp(c.get('kicker', ''), cx, H*0.175, W*0.075, ink, n=18,
                 largura=W*LARGURA_SEGURA)
        s += f'<line x1="{W*0.10}" y1="{H*0.60}" x2="{W*0.90}" y2="{H*0.60}" stroke="{ink}" stroke-width="3" opacity="0.35"/>'
        for i, lb in enumerate(labs):
            bh = (H*0.06 + (alt[i]/max(alt))*H*0.28) if alt else (H*0.06 + i*H*0.28/max(n-1, 1))
            x = W*0.12 + i*bw
            s += f'<rect x="{x}" y="{H*0.60-bh}" width="{bw*0.72}" height="{bh}" fill="{[c1,c2,ink][i%3]}"/>'
            s += tsp(str(lb), x+bw*0.36, H*0.65, W*0.035, ink, n=12, largura=bw*0.9)
    return s + '</svg>'


def svg_cena(c, pal, W, H, camada=None):
    """camada=None: a cena inteira (comportamento historico, e o do short).
    camada='base': so o fundo e o que nao se move.
    camada=k (0-based): so o k-esimo elemento, sobre fundo transparente.

    Existe porque a cena estatica era o defeito de retencao mais visivel do
    formato: quatro itens de uma lista apareciam juntos e ficavam parados os
    dez segundos inteiros em que o narrador os percorre um a um. Com os
    elementos entrando no tempo da fala, o olho tem motivo para continuar.

    Retrato (short 9:16) desvia para svg_cena_retrato: a geometria daqui e
    16:9 e estoura as bordas laterais quando H > W.
    """
    if H > W and camada is None:
        return svg_cena_retrato(c, pal, W, H)
    ink, c1, c2 = pal['ink'], pal['c1'], pal['c2']
    bg = pal.get('bg', '#FFFFFF'); lay = c.get('layout','titulo')

    def quer(k):
        """Este elemento entra nesta camada?"""
        if camada is None:
            return True
        if camada == 'base':
            return k is None      # k=None marca o mobiliario fixo da cena
        return k == camada

    fundo = (camada is None or camada == 'base')
    # A cena de CTA invertia o fundo (escuro com texto claro). Como sao as tres
    # ultimas de cada video, a virada de cor no fim lia como defeito de render,
    # nao como cartao de encerramento. Agora o CTA segue a identidade do canal.
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    # A cena broll nao pinta fundo: o PNG sai com alpha e o clipe_cena poe o
    # footage por baixo. Se o footage faltar, o fallback compoe sobre preto —
    # texto branco sobre preto le, entao o degrade e o pior caso aceitavel.
    if fundo and lay != 'broll':
        s += f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    cx = W//2
    if lay == 'broll':
        # Cartao flutuante, NAO faixa ate a borda: o portao do prontidao.py
        # mede tinta nos 4% externos (MAX 1,2%) e a primeira versao — faixa
        # colada no rodape + descendentes do devanagari — reprovou 6/7 cenas
        # do agla-level-004 com 1,3 a 1,6%. O cartao termina em 0,86H e o
        # texto mais fundo fica em ~0,84H: folga de 10 pontos ate a zona.
        s += (f'<rect x="{W*0.07}" y="{H*0.62}" width="{W*0.86}" '
              f'height="{H*0.24}" rx="{H*0.02}" fill="#000000" '
              f'opacity="0.45"/>')
        s += tsp(c.get('kicker', ''), W*0.11, H*0.735, H*0.065, '#FFFFFF',
                 n=24, anchor='start', largura=W*0.78)
        if c.get('sub'):
            s += tsp(c['sub'], W*0.11, H*0.825, H*0.042, c2, n=42,
                     anchor='start', largura=W*0.78)
        return s + '</svg>'
    if lay in ('titulo','cta'):
        fg = c1 if lay=='titulo' else c2
        # sub_fg era branco no cta — o que so funcionava com o fundo invertido.
        # Sem a inversao, branco sobre fundo claro sumia por completo.
        sub_fg = ink
        big = c.get('kicker','')
        if quer(0):
            s += tsp(big, cx, H*0.40, H*(0.15 if len(big)<=10 else 0.09), fg, n=16,
                     largura=W*LARGURA_SEGURA)
            s += f'<path d="M {cx-W*0.26} {H*0.52} Q {cx} {H*0.55}, {cx+W*0.26} {H*0.52}" stroke="{c2 if lay=="titulo" else c1}" stroke-width="10" fill="none" stroke-linecap="round"/>'
        if c.get('sub') and quer(1):
            s += tsp(c['sub'], cx, H*0.65, H*0.055, sub_fg, n=30, largura=W*LARGURA_SEGURA)
    elif lay == 'lista':
        if quer(None):
            s += tsp(c.get('kicker',''), cx, H*0.18, H*0.08, ink, n=24, largura=W*LARGURA_SEGURA)
        # Passo FIXO de 0,17H punha o quarto item em 0,89H — dentro da zona que
        # o Ken Burns corta, que comeca em 0,88H. Nao era uma spec infeliz: TODA
        # lista de quatro itens reprovava, por construcao. Agora o passo divide a
        # faixa segura (0,38H a 0,80H) pelo numero de itens e so encolhe quando
        # precisa; com tres ou menos nada muda, que e como as boas ja estavam.
        itens = c.get('itens', [])
        passo = min(H*0.17, H*0.42/max(len(itens)-1, 1))
        y = H*0.38
        for i, it in enumerate(itens):
            if quer(i):
                col = [c1, c2, ink][i%3]
                s += f'<circle cx="{W*0.16}" cy="{y-H*0.02}" r="{H*0.025}" fill="{col}"/>'
                s += tsp(it, W*0.21, y, H*0.055, ink, n=36, anchor='start',
                         largura=W*(1 - 0.21 - MARGEM_SEGURA))
            y += passo
    elif lay == 'barras':
        labs = c.get('itens', ['1','2','3','4']); n = len(labs); bw = W*0.64/n
        alt = c.get('alturas')
        if quer(None):
            # Kicker em 0,16H com corpo 0,08H punha o ASCENDER em 0,102H, e o
            # pan vertical (i%4 em 2 e 3) sobe o enquadramento ate a faixa de
            # topo terminar em 0,115H. Medido no kolejny-poziom-002 cena 35:
            # 6,55% de tinta na borda de CIMA, nao na de baixo. Baseline em
            # 0,205H com corpo 0,07H poe o ascender em 0,154H, com folga.
            s += tsp(c.get('kicker',''), cx, H*0.205, H*0.07, ink, n=26,
                     largura=W*LARGURA_SEGURA)
            # A linha de base fica no fundo: e o chao contra o qual as barras
            # sobem, e sem ela as primeiras parecem flutuar no vazio.
            s += f'<line x1="{W*0.15}" y1="{H*0.82}" x2="{W*0.85}" y2="{H*0.82}" stroke="{ink}" stroke-width="3" opacity="0.35"/>'
        for i, lb in enumerate(labs):
            if not quer(i):
                continue
            # Amplitude 0,48H punha o topo da barra mais alta em 0,22H, onde o
            # kicker agora desce quando quebra em duas linhas. 0,42H deixa o
            # topo em 0,28H e a proporcao entre as barras nao muda — o que se
            # le num grafico de barras e a razao, nao o valor absoluto.
            bh = (H*0.12 + (alt[i]/max(alt))*H*0.42) if alt else (H*0.12 + i*H*0.42/max(n-1,1))
            x = W*0.18 + i*bw
            s += f'<rect x="{x}" y="{H*0.82-bh}" width="{bw*0.72}" height="{bh}" fill="{[c1,c2,ink][i%3]}"/>'
            # y=0,90H punha o rotulo dentro da faixa que o Ken Burns corta.
            # Medido em 17/08/2026: com AMP_ZOOM 0,12 e AMP_PAN 0,5 o zoom tira
            # ate 8,04% de um lado, e somando os 4% que o visual.py chama de
            # borda a zona de risco comeca em 0,88H. Baseline em 0,90H mais o
            # descender da fonte punha tinta ate 0,908H — 77 das 99 cenas
            # `barras` de TODAS as specs reprovavam. 0,865H sai da zona com
            # folga e mantem o rotulo abaixo da linha de base.
            #
            # `subindo` porque o rotulo de duas linhas crescia justamente para
            # dentro da zona: 'antes: caixa aleatoria' punha tinta ate 0,912H.
            # Ancorado na ultima linha, o bloco cresce para cima e a base fica
            # onde sempre esteve.
            s += tsp(str(lb), x+bw*0.36, H*0.865, H*0.038, ink, n=14, subindo=True,
                     largura=bw*0.9)
    elif lay == 'item':
        if quer(None):
            s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.22}" fill="none" stroke="{ink}" stroke-width="9"/>'
            s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.14}" fill="{c2}" opacity="0.55"/>'
        if quer(0):
            s += tsp(c.get('kicker',''), W*0.63, H*0.36, H*0.07, ink, n=20,
                     largura=W*(1 - 0.63 - MARGEM_SEGURA)*2)
        if c.get('preco') and quer(1):
            s += f'<rect x="{W*0.51}" y="{H*0.5}" width="{W*0.24}" height="{H*0.13}" fill="{c1}"/>'
            s += texto_na_caixa(c['preco'], W*0.63, H*0.565, W*0.22, H*0.13,
                                '#FFFFFF', n=12, corpo_max=H*0.06)
    return s + '</svg>'

def dur(f):
    return _duracao(f)

def st(x):
    return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{x%60:06.3f}".replace(".",",")

async def vozes(cenas, voz, pref, d):
    for i, c in enumerate(cenas):
        alvo = f"{d}/{pref}{i:02d}.mp3"
        # RETOMA: mp3 valido nao se refaz — cada restart pos-crash custava
        # ~10 min de TTS refeito do zero.
        if os.path.exists(alvo) and os.path.getsize(alvo) > 1000:
            continue
        # O websocket do edge-tts ja pendurou sem erro nem timeout (15 min
        # parado na cena 82 do setiap-006). wait_for + 3 tentativas.
        for tentativa in range(3):
            try:
                com = edge_tts.Communicate(c["nar"], voz, rate="-4%")
                await asyncio.wait_for(com.save(alvo), timeout=90)
                if os.path.getsize(alvo) > 1000:
                    break
                raise RuntimeError(f"mp3 vazio: {alvo}")
            except Exception:
                try:
                    os.remove(alvo)
                except OSError:
                    pass
                if tentativa == 2:
                    raise


from caminhos import dir_trabalho as _dir_trabalho  # noqa: E402

# Reexportado de `caminhos`, que e texto puro e nao arrasta cairosvg/edge_tts.
# O `publicar.py` e o `vozes.py` precisam do MESMO caminho e nao podem pagar
# esta stack — quando cada um resolvia o seu, o publicar.py ficou procurando
# em /tmp/f um pacote renderizado noutra raiz.
dir_trabalho = _dir_trabalho


def montar(spec_file):
    sp = json.load(open(spec_file))
    usar_fonte(sp.get("fonte"))
    slug, pal, voz = sp["slug"], sp["paleta"], sp["voz"]
    d = dir_trabalho(sp); os.makedirs(d, exist_ok=True)
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            # O longo entra em camadas (base + um png por elemento). O short
            # nao: sao 30s com legenda queimada, e ali a entrada escalonada
            # rouba tempo de leitura em vez de dar ritmo.
            FW, FH = W, H
            if pref == "l":
                cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H, camada='base').encode(),
                                 write_to=f"{d}/{pref}{i:02d}.png", output_width=FW, output_height=FH)
                for k in range(elementos(c)):
                    cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H, camada=k).encode(),
                                     write_to=f"{d}/{pref}{i:02d}_{k}.png",
                                     output_width=FW, output_height=FH)
            else:
                cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H).encode(),
                                 write_to=f"{d}/{pref}{i:02d}.png", output_width=FW, output_height=FH)
        asyncio.run(vozes(cenas, voz, pref, d))
    cairosvg.svg2png(bytestring=svg_thumb(sp["thumb"], pal).encode(),
                     write_to=f"{d}/thumbnail.png",
                     output_width=1280, output_height=720)
    print(slug, "assets ok")

# Capitulos e copy.md vivem em copy_md.py: sao texto puro e nao podem exigir
# cairosvg/edge_tts de quem so precisa deles (o job de reparo de descricao
# morria importando esta stack inteira para formatar markdown).
from copy_md import capitulos, credito_trilha, escrever_copy as _escrever_copy  # noqa: E402,F401
from copy_md import trilha_do_canal as _trilha_do_canal  # noqa: E402

TRILHA_DIR = "/tmp/trilhas"


def trilha_do_canal(slug, registrada=None):
    """Assinatura sonora do canal, validando o mp3 de verdade (ver trilha_ok).

    `registrada` vem de sp["trilha"] e PRECISA chegar aqui. Medido em
    14/08/2026 contra o bucket: com as tres faixas que existem de verdade, o
    hash acerta 3 dos 13 canais e erra 10 — e nao erra so o credito, erra o
    AUDIO, porque `aplicar_trilha` chama esta mesma funcao.
    """
    return _trilha_do_canal(slug, trilha_ok, registrada)


def escrever_copy(sp, tempos, d):
    return _escrever_copy(sp, tempos, d, trilha_ok)
# Sem `-shortest`: o corte era feito pelo audio (a narracao crua), o que comia
# a folga de 0,5s no fim de cada cena — a fala terminava e a cena virava no
# mesmo quadro. Quem limita a duracao e o `-t` do clipe, entao a folga volta.
AUDIO_ARGS = ["-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ac","2","-ar","48000","-c:a","aac","-b:a","192k"]

def trilha_ok(f):
    """Um download que falhou vira um .mp3 com HTML dentro. Ele passa no glob,
    passa no teste de tamanho, e so estoura no ffprobe — depois de a fabrica ja
    ter gasto o render inteiro. Entao valida decodificando de verdade."""
    try:
        return dur(f) > 30
    except Exception:
        return False


# Escala de render. Era 0,75 para caber no sandbox de ~1GB, e o concat fazia
# upscale de 960x540 para 1280x720 — texto fino ampliado, borrado de saida. O
# render vive no Actions desde 15/08 e la ha 7GB, entao nao ha mais motivo.
ESCALA_RENDER = 1.0

# Quantas vezes o quadro e AMPLIADO logo antes do zoompan.
#
# ISTO E O CONSERTO DO TREMOR. O `zoompan` avalia x e y por quadro e ARREDONDA
# PARA PIXEL INTEIRO. Com AMP_ZOOM 0,12 e AMP_PAN 0,5 o pan anda de 0,13 a 0,53
# px por quadro sobre um quadro de 1280 — menos de um pixel. A imagem fica
# parada de dois a oito quadros e entao salta 1px de uma vez. E isso que se ve
# como imagem tremendo. Ampliando antes, 1px de arredondamento vale meio pixel
# na saida, e o movimento passa a ser continuo.
#
# MEDIDO em 17/08/2026 sobre uma cena `lista` de quatro itens com camadas,
# quarenta quadros, contando os que ficam praticamente identicos ao anterior:
#
#     variante                              travados   desvio   custo/clipe
#     hoje: overlay 1x -> 960x540            8 de 39    0,476       9,3 s
#     ampliar 2x antes do zoompan            0 de 39    0,274      15,3 s
#     rasterizar tudo em 2x                  0 de 39    0,286      29,9 s
#
# Ampliar no filtro da o MESMO resultado que rasterizar em 2x pela metade do
# custo: o que importa para o arredondamento e a resolucao que o zoompan ve, e
# nao de onde ela veio. Rasterizar em 2x custa caro porque os overlays das
# camadas passam a rodar todos em 2560x1440.
SUAVIZA = 2
# Amplitude do Ken Burns por cena (7% = perceptivel sem cortar a arte).
AMP_ZOOM = 0.12
# Fracao da margem disponivel que o pan percorre. 1.0 encostaria na borda e
# cortaria ate 11% de um dos lados — o suficiente para comer o fim de um item
# de lista. 0.5 mantem o enquadramento centrado e ainda da deslocamento visivel.
AMP_PAN = 0.5


def ken_burns(i, nf):
    """Zoom + pan em 4 direcoes alternadas, em funcao de `on` (numero do frame).

    Retorna (expressao de zoom, fracao horizontal, fracao vertical). As fracoes
    valem 0 a 1 sobre a margem que o zoom abriu; 0.5 e o centro. Alternar em 4
    (nao em 2) evita que cenas vizinhas facam o mesmo movimento espelhado, que
    o olho le como repeticao.
    """
    p = f"on/{nf}"
    dentro = f"1+{AMP_ZOOM}*{p}"
    fora = f"{1 + AMP_ZOOM:.4g}-{AMP_ZOOM}*{p}"
    meio = 0.5
    ini = (1 - AMP_PAN) / 2                      # 0.25
    varre = f"{ini}+{AMP_PAN}*{p}"               # 0.25 -> 0.75
    volta = f"{ini + AMP_PAN}-{AMP_PAN}*{p}"     # 0.75 -> 0.25
    return [
        (dentro, varre, meio),   # aproxima varrendo para a direita
        (fora,   volta, meio),   # afasta varrendo para a esquerda
        (dentro, meio,  varre),  # aproxima descendo
        (fora,   meio,  volta),  # afasta subindo
    ][i % 4]
def render_wh(W, H):
    return (int(W * ESCALA_RENDER) // 2 * 2, int(H * ESCALA_RENDER) // 2 * 2)

# Em video explicador a trilha existe para tirar o silencio entre as frases,
# nao para ser ouvida: trilha alta e causa comum de abandono neste formato.
VOL_TRILHA = "-28dB"

def aplicar_trilha(d, out, slug, registrada=None):
    """Mixa a trilha CC-BY sob a narracao em UM passe, sobre o arquivo ja
    concatenado. Por clipe (ou com -stream_loop) estourava a RAM do sandbox;
    aqui o video sai em copy e so o audio e reencodado."""
    faixa = trilha_do_canal(slug, registrada)
    if not faixa:
        # NAO retorne calado. Este `return` existiu ate 14/08/2026 e e o
        # mecanismo por tras da inconsistencia medida naquele dia: dos quatro
        # videos entregues que eu analisei no bucket, um tinha trilha e nao
        # creditava, e outro creditava Inspired sem ter trilha nenhuma.
        #
        # Calado ele e invisivel duas vezes: o log escreve "etapa 6 ok" e a
        # marca de pronto dizia "longo montado e com trilha". O video sai sem a
        # assinatura sonora do canal e ninguem fica sabendo.
        #
        # QUANTO ISSO PEGOU, medido em 15/08/2026 nos artefatos ENTREGUES no
        # bucket (piso de ruido, percentil 5 em janelas de 0,5 s): dos SETE
        # pacotes medidos, SEIS sairam sem musica nenhuma. So o
        # labtreinamento-001 tem trilha. Nao e caso raro, e a regra.
        #
        # E os artefatos do bucket SAO os publicados: duracao e tamanho batem
        # na casa decimal contra videos.duracao_s e videos.tamanho_mb.
        raise RuntimeError(
            f"nenhuma trilha utilizavel em {TRILHA_DIR} para o canal {slug} "
            f"(registrada={registrada!r}). Renderizar sem musica e uma saida "
            f"ERRADA, nao uma saida menor: o canal perde a assinatura sonora e "
            f"o copy.md pode creditar uma faixa que nao toca. Baixe as trilhas "
            f"antes de renderizar."
        )
    alvo = f"{d}/{out}"
    dv = dur(alvo)
    # Loop barato: concat demuxer com stream copy ate cobrir o video.
    lista, bed = f"{d}/trilha_lista.txt", f"{d}/bed.mp3"
    with open(lista, "w") as f:
        f.write(f"file '{faixa}'\n" * (int(dv // dur(faixa)) + 2))
    subprocess.run([ffmpeg_bin(),"-nostdin","-y","-f","concat","-safe","0","-i",lista,"-c","copy",bed],check=True,capture_output=True)
    mix = f"{d}/mix_{out}"
    subprocess.run([ffmpeg_bin(),"-nostdin","-y","-i",alvo,"-i",bed,"-filter_complex",
        f"[1:a]volume={VOL_TRILHA}[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=11[a]",
        # Num pacote escalonado (25-30 min) o audio passa a dominar o arquivo:
        # 192k por 26 min ja da ~37 MB e o video inteiro nao cabe no limite de
        # 50 MB do upload padrao do Supabase. Para narracao com trilha a -28 dB,
        # 128k e indistinguivel e devolve ~7 MB.
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac",
        "-b:a", "192k" if dv < 1100 else "128k", "-ac","2","-ar","48000",
        "-t",f"{dv:.2f}","-movflags","+faststart",mix],check=True,capture_output=True)
    os.replace(mix, alvo)
    os.remove(bed)

# MarginL/R forcam a quebra de linha antes da caixa encostar nas laterais do
# 9:16 — sem eles a legenda queimada tocava as duas bordas em TODO quadro do
# short (medido pelo visual.py: 3-6,3% de tinta na borda; com margens, 0,00%).
EST = f"FontName={FONTE},Fontsize=13,Bold=1,PrimaryColour=&H00FFFFFF,BorderStyle=3,BackColour=&HB0000000,Outline=1,Shadow=0,MarginV=36,MarginL=18,MarginR=18"

def render(spec_file):
    sp = json.load(open(spec_file)); slug = sp["slug"]
    usar_fonte(sp.get("fonte"))
    d = dir_trabalho(sp)
    tempos = []
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            # A checagem do RETOMA vem ANTES de medir o mp3: quando os lotes ja
            # renderizaram tudo, o png/mp3 foi apagado para caber no tmpfs, e
            # medir aqui quebrava o render inteiro num clipe que ja existia.
            saida = f"{d}/{pref}clip{i:02d}.mp4"  # RETOMA
            if os.path.exists(saida) and os.path.getsize(saida) > 10000:
                continue
            dd = dur(f"{d}/{pref}{i:02d}.mp3") + 0.5
            open(f"{d}/{pref}{i:02d}.srt","w").write(f"1\n{st(0.2)} --> {st(dd-0.15)}\n{c['nar']}\n")
            RW, RH = render_wh(W, H)
            # Ken Burns em funcao de `on` (numero do frame), nao por incremento
            # acumulado: assim a amplitude e a mesma nas duas direcoes e ocupa a
            # cena inteira, seja ela de 8s ou de 15s. O incremento fixo anterior
            # fazia o zoom-in crescer sem teto (+23% numa cena de 13s, cortando
            # a borda do texto) e o zoom-out travar em 1.0 depois de 3,3s,
            # deixando metade das cenas imovel em ~75% da duracao.
            nf = max(int(dd * 30), 1)
            z, fx, fy = ken_burns(i, nf)
            # x/y ficavam presos no centro, entao o movimento era zoom puro de
            # 7% em ~10s — imperceptivel, o video lia como imagem parada. Agora
            # ha deslocamento de verdade, em 4 direcoes alternadas.
            vf = (f"scale=iw*{SUAVIZA}:ih*{SUAVIZA}:flags=bilinear,"
                  f"zoompan=z='{z}':d={nf}"
                  f":x='(iw-iw/zoom)*({fx})':y='(ih-ih/zoom)*({fy})'"
                  f":s={RW}x{RH}:fps=30")
            # Legenda queimada so no short. No longo ela rouba area util e
            # impede a legenda propria do YouTube (que traduz e e indexada);
            # o pacote entrega um .srt para subir junto, melhor que a automatica.
            if pref == "s":
                vf += f",subtitles={d}/{pref}{i:02d}.srt:force_style='{EST}'"
            clipe_cena(d, pref, i, c, dd, nf, RW, RH)
            # MANIFESTO: checkpoint por clipe — uma falha nunca custa o pacote
            with open(f"{d}/manifesto.txt","a") as mf:
                mf.write(f"{pref}clip{i:02d}.mp4\n")
        # Os tempos dos capitulos saem do clipe RENDERIZADO, nunca do mp3: o mp3
        # e a narracao crua, e a cena tem folga no fim. Estimar pelo mp3 dava um
        # erro que se acumulava cena a cena (+23s no fim de um video de 12 min),
        # jogando os capitulos do fim para depois do trecho que nomeiam.
        if pref == "l":
            tempos = [dur(f"{d}/lclip{i:02d}.mp4") for i in range(len(cenas))]
            # Legenda de verdade para subir no Studio. Sai dos clipes
            # renderizados, entao bate ao milissegundo com o video final —
            # e e melhor que a automatica do YouTube, que erra nomes proprios
            # e numeros justamente onde este formato se apoia.
            with open(f"{d}/legendas.srt", "w", encoding="utf-8") as srt:
                t = 0.0
                for i, c in enumerate(cenas):
                    fim = t + tempos[i]
                    srt.write(f"{i+1}\n{st(t + 0.15)} --> {st(fim - 0.15)}\n{c['nar']}\n\n")
                    t = fim
        with open(f"{d}/{pref}lista.txt","w") as f:
            for i in range(len(cenas)): f.write(f"file '{pref}clip{i:02d}.mp4'\n")
        out = "video.mp4" if pref=="l" else "short.mp4"
        RW, RH = render_wh(W, H)
        args = [ffmpeg_bin(),"-nostdin","-y","-f","concat","-safe","0","-i",f"{d}/{pref}lista.txt"]
        if (RW, RH) != (W, H):
            # Aqui nao ha zoompan, entao da para usar um preset eficiente sem
            # risco de OOM: `ultrafast` gerava 178 MB em 12 min (6x maior que
            # o necessario) e estourava o limite de upload de 50 MB.
            # E o CRF sobe nos pacotes escalonados pelo mesmo motivo: em arte
            # vetorial chapada com zoom lento, crf 29 e visualmente igual a 26.
            crf = "26" if pref != "l" or sum(dur(f"{d}/lclip{i:02d}.mp4") for i in range(len(cenas))) < 1100 else "29"
            args += ["-vf",f"scale={W}:{H}:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf",crf,"-pix_fmt","yuv420p","-c:a","copy"]
        else:
            args += ["-c","copy"]
        subprocess.run(args + ["-movflags","+faststart",f"{d}/{out}"],check=True,capture_output=True,cwd=d)
        aplicar_trilha(d, out, slug, sp.get("trilha"))
    escrever_copy(sp, tempos, d)
    print(slug, "render ok", round(sum(tempos)))
if __name__ == "__main__":
    fn = sys.argv[1]; spec = sys.argv[2]
    montar(spec) if fn == "montar" else render(spec)

# --------------------------------------------------------------- animacao
ENTRADA = 0.40      # segundos que cada elemento leva para entrar
DESLIZE = 26        # pixels que ele sobe enquanto entra
INICIO = 0.45       # atraso do primeiro elemento, para a cena assentar
OCUPA = 0.62        # fracao da cena em que todos ja entraram


def tempos_entrada(n, dd):
    """Quando cada um dos n elementos entra, numa cena de dd segundos.

    Espalha as entradas pelos primeiros 62% da cena. Nao ha alinhamento por
    palavra — nao temos timestamp do TTS — mas o narrador percorre a lista na
    mesma ordem e no mesmo ritmo, entao a coincidencia e boa o bastante para o
    olho e muito melhor do que tudo aparecer junto.
    """
    if n <= 0:
        return []
    fim = max(INICIO + ENTRADA, dd * OCUPA)
    if n == 1:
        return [INICIO]
    passo = (fim - INICIO) / (n - 1)
    return [INICIO + i * passo for i in range(n)]


def filtro_camadas(n, dd, i_cena, nf, RW, RH):
    """Monta o filter_complex: base + n camadas entrando, e o Ken Burns no fim.

    Cada camada e uma tela transparente do tamanho do quadro, entao o overlay
    vai em x=0 e so o y anima — nao ha coordenada para acertar aqui, o SVG ja
    colocou o elemento no lugar certo.
    """
    z, fx, fy = ken_burns(i_cena, nf)
    if n == 0:
        return (f"[0:v]scale=iw*{SUAVIZA}:ih*{SUAVIZA}:flags=bilinear,"
                f"zoompan=z='{z}':d={nf}:x='(iw-iw/zoom)*({fx})'"
                f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30[v]")
    partes, atual = [], "0:v"
    for k, t0 in enumerate(tempos_entrada(n, dd)):
        partes.append(f"[{k+1}:v]format=rgba,fade=in:st={t0:.2f}:d={ENTRADA}:alpha=1[a{k}]")
        y = f"{DESLIZE}*max(0\\,1-(t-{t0:.2f})/{ENTRADA})"
        partes.append(f"[{atual}][a{k}]overlay=x=0:y='{y}':format=auto[o{k}]")
        atual = f"o{k}"
    # A ampliacao vem DEPOIS dos overlays de proposito: ampliar antes faria
    # cada camada compor em 2560x1440 e dobraria o custo sem ganho — o que o
    # zoompan precisa e so da resolucao que ELE ve.
    partes.append(f"[{atual}]scale=iw*{SUAVIZA}:ih*{SUAVIZA}:flags=bilinear,"
                  f"zoompan=z='{z}':d=1:x='(iw-iw/zoom)*({fx})'"
                  f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30[v]")
    return ";".join(partes)


def clipe_cena(d, pref, i, c, dd, nf, RW, RH, est=None):
    """Renderiza UM clipe de cena. Fonte unica para fabrica.render e etapas.py.

    Existe porque o etapas.py mantinha a propria copia deste loop, e as duas
    saiam do lugar sem avisar: a composicao em camadas entrou aqui e o etapas.py
    continuou no caminho antigo de zoompan sobre imagem unica. O pacote sairia
    sem animacao nenhuma, e nada acusaria — o video tem a duracao certa, o
    tamanho certo e passa em todos os asserts.
    """
    saida = f"{d}/{pref}clip{i:02d}.mp4"
    broll_mp4 = f"{d}/{pref}{i:02d}_broll.mp4"
    if (c.get("layout") == "broll" and os.path.exists(broll_mp4)
            and os.path.getsize(broll_mp4) > 10000):
        # Footage por baixo, lower-third transparente por cima. O broll ja
        # vem preparado (dd segundos, RWxRH, 30fps, escurecido, sem audio)
        # pelo broll.py; o PNG e renderizado em WxH e sobe para RWxRH aqui.
        # stream_loop -1 cobre a diferenca de arredondamento entre o -t do
        # preparo e o -t deste corte: sem ele um broll 0,1s curto congela.
        args = [ffmpeg_bin(), "-nostdin", "-y",
                "-stream_loop", "-1", "-t", f"{dd:.2f}", "-i", broll_mp4,
                "-framerate", "30", "-loop", "1", "-t", f"{dd:.2f}",
                "-i", f"{d}/{pref}{i:02d}.png",
                "-i", f"{d}/{pref}{i:02d}.mp3",
                "-filter_complex",
                f"[1:v]scale={RW}:{RH}[t];[0:v][t]overlay=0:0:format=auto[v]",
                "-map", "[v]", "-map", "2:a"]
        subprocess.run(args + ["-t", f"{dd:.2f}", "-c:v", "libx264",
                               "-preset", "ultrafast", "-crf", "23",
                               "-pix_fmt", "yuv420p", *AUDIO_ARGS, saida],
                       check=True, capture_output=True)
        return saida
    n_cam = elementos(c) if pref == "l" else 0
    if n_cam:
        args = [ffmpeg_bin(), "-nostdin", "-y",
                "-framerate", "30", "-loop", "1", "-t", f"{dd:.2f}",
                "-i", f"{d}/{pref}{i:02d}.png"]
        for k in range(n_cam):
            args += ["-framerate", "30", "-loop", "1", "-t", f"{dd:.2f}",
                     "-i", f"{d}/{pref}{i:02d}_{k}.png"]
        args += ["-i", f"{d}/{pref}{i:02d}.mp3",
                 "-filter_complex", filtro_camadas(n_cam, dd, i, nf, RW, RH),
                 "-map", "[v]", "-map", f"{n_cam+1}:a"]
    else:
        z, fx, fy = ken_burns(i, nf)
        vf = (f"scale=iw*{SUAVIZA}:ih*{SUAVIZA}:flags=bilinear,"
              f"zoompan=z='{z}':d={nf}:x='(iw-iw/zoom)*({fx})'"
              f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30")
        if pref == "s":
            vf += f",subtitles={d}/{pref}{i:02d}.srt:force_style='{est or EST}'"
        args = [ffmpeg_bin(), "-nostdin", "-y", "-loop", "1",
                "-i", f"{d}/{pref}{i:02d}.png", "-i", f"{d}/{pref}{i:02d}.mp3",
                "-vf", vf]
    subprocess.run(args + ["-t", f"{dd:.2f}", "-c:v", "libx264",
                           "-preset", "ultrafast", "-crf", "23",
                           "-pix_fmt", "yuv420p", *AUDIO_ARGS, saida],
                   check=True, capture_output=True)
    return saida
