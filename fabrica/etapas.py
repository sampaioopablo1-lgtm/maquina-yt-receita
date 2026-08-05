#!/usr/bin/env python3
"""Roda um pacote em etapas SEQUENCIAIS, cada uma comecando so quando a anterior
retorna.

Existe por causa de um estrago concreto. Num pacote de 196 cenas, os clipes
(335 MB) + o concat (45 MB) + a trilha (95 MB) nao cabem nos 493 MB de tmpfs do
sandbox, entao era preciso liberar espaco no meio. A primeira tentativa usou um
processo em segundo plano que apagava os clipes quando `video.mp4` ficava 8s do
mesmo tamanho — tratando "parou de crescer" como "terminou".

Nao e sinal nenhum: a escrita do ffmpeg e em rajadas. Os clipes sumiram no meio
do concat e o video saiu com 1236,9s em vez de 1716s — 28% faltando, incluindo o
capitulo final e o CTA. E o log dizia "render ok 1716", porque a soma vinha dos
tempos medidos ANTES da limpeza: a saida estava truncada e o log parecia certo.

Daqui saem tres regras, todas aplicadas abaixo:
  1. quem libera espaco e o proprio fluxo, depois do subprocess RETORNAR;
  2. toda etapa que produz arquivo confere o proprio resultado (o assert do
     concat), em vez de reportar a medicao da entrada;
  3. limpeza usa padrao ancorado (`lclip*.mp4`, `l{i:02d}.png`) e nunca curinga
     de uma letra — `l*.srt` levou junto o `legendas.srt`, que era entregavel.

Uso:  python3 etapas.py <spec.json>
"""
import sys, os, json, glob, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F

if len(sys.argv) < 2:
    sys.exit("uso: python3 etapas.py <spec.json>")
# Sem argumento obrigatorio isto ficava com um default fixo, e uma copia
# desatualizada no sandbox chegou a IGNORAR o argv: rodou 4 minutos gerando
# narracao do pacote anterior, no diretorio do canal errado, sem erro nenhum.
# Nao ha default seguro aqui — o pacote e sempre declarado por quem chama.
spec = sys.argv[1]
sp = json.load(open(spec))
d = F.dir_trabalho(sp)
# O diretorio de trabalho tem que ser o do pacote pedido. Se a copia da fabrica
# for antiga e resolver por slug de canal, o disparo para aqui em vez de
# costurar dois roteiros num video so.
assert d.endswith(sp.get("pacote") or sp["slug"]), f"dir {d} nao bate com {spec}"


def log(m):
    print(m, flush=True)


# ------------------------------------------------- 0. a narracao, antes do TTS
# Roda antes de gastar minutos de sintese e de render: defeito de narracao e o
# unico que a maquina nao conseguia enxergar sozinha. Um render impecavel de um
# roteiro que nao prende continua sendo um video que ninguem termina.
import narracao as N                                              # noqa: E402

_idi = N.idioma_de(sp)
_erros, _avisos, _frases = N.analisa(sp, _idi)
log(f"etapa 0: narracao idioma={_idi}, {len(_frases)} frases, "
    f"{len(_erros)} erro(s), {len(_avisos)} aviso(s)")
for _a in _avisos:
    log(f"  aviso  {_a}")
for _e in _erros:
    log(f"  ERRO   {_e}")
assert not _erros, "narracao reprovada — corrija a spec antes de renderizar"
log("etapa 0 ok")


# ---------------------------------------------------------------- 1. assets
if len(glob.glob(f"{d}/l*.mp3")) < len(sp["longo"]):
    log("etapa 1: montar")
    F.montar(spec)
log(f"etapa 1 ok: {len(glob.glob(f'{d}/l*.mp3'))} mp3")

# ------------------------------------------- 2. clipes, liberando um a um
log("etapa 2: clipes do longo")
cenas = sp["longo"]
W, H = 1280, 720
RW, RH = F.render_wh(W, H)
tempos = []
for i, c in enumerate(cenas):
    saida = f"{d}/lclip{i:02d}.mp4"
    if not (os.path.exists(saida) and os.path.getsize(saida) > 10000):
        dd = F.dur(f"{d}/l{i:02d}.mp3") + 0.5
        nf = max(int(dd * 30), 1)
        # Uma unica fonte para o clipe. Este loop ja teve copia propria da
        # logica e ficou para tras quando a composicao em camadas entrou na
        # fabrica: o pacote sairia SEM animacao e passaria em todos os asserts.
        F.clipe_cena(d, "l", i, c, dd, nf, RW, RH)
    tempos.append(F.dur(saida))
    # padrao ancorado: nunca `l*.png`
    for ext in ("png", "mp3"):
        try:
            os.remove(f"{d}/l{i:02d}.{ext}")
        except OSError:
            pass
    if i % 40 == 0:
        log(f"  clipe {i}/{len(cenas)}")
log(f"etapa 2 ok: {len(tempos)} clipes, {sum(tempos):.1f}s")

# ------------------------------- 3. legenda ANTES de qualquer limpeza futura
with open(f"{d}/legendas.srt", "w", encoding="utf-8") as srt:
    t = 0.0
    for i, c in enumerate(cenas):
        fim = t + tempos[i]
        srt.write(f"{i+1}\n{F.st(t + 0.15)} --> {F.st(fim - 0.15)}\n{c['nar']}\n\n")
        t = fim
json.dump(tempos, open(f"{d}/tempos.json", "w"))
log("etapa 3 ok: legendas.srt + tempos.json")

# -------------------------------------------- 4. concat, em DUAS METADES
# O tmpfs mora na RAM: 196 clipes sao 390 MB dos 985 MB da maquina. Concatenar
# tudo de uma vez deixava 2 MB livres, com kswapd0 ativo e o ffmpeg a 36% de
# CPU escrevendo 0,26 MB a cada 50s — horas de encode. Metade de cada vez libera
# a RAM da primeira antes de codificar a segunda, e a juncao final e -c copy.
# Medido: 0,26 MB/50s antes, 6 MB/min depois.
#
# O aperto piorou quando o Ken Burns passou a ter pan de verdade: com quadros
# quase identicos o x264 comprimia de graca, e agora nao comprime mais.
crf = "29" if sum(tempos) >= 1100 else "26"
meio = len(cenas) // 2
for parte, (ini, fim) in enumerate(((0, meio), (meio, len(cenas))), start=1):
    saida = f"{d}/p{parte}.mp4"
    if os.path.exists(saida) and os.path.getsize(saida) > 100000:
        log(f"etapa 4: parte {parte} ja existe")
        continue
    lista = f"{d}/lista_p{parte}.txt"
    with open(lista, "w") as f:
        for i in range(ini, fim):
            f.write(f"file 'lclip{i:02d}.mp4'\n")
    log(f"etapa 4: parte {parte}, clipes {ini}-{fim - 1}")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
        "-i", lista, "-vf", f"scale={W}:{H}:flags=lanczos", "-c:v", "libx264",
        "-preset", "veryfast", "-crf", crf, "-pix_fmt", "yuv420p",
        "-c:a", "copy", saida], check=True, capture_output=True, cwd=d)
    esperado, real = sum(tempos[ini:fim]), F.dur(saida)
    log(f"etapa 4: parte {parte} ok, {real:.1f}s (esperado {esperado:.1f}s)")
    assert abs(real - esperado) < 5, f"parte {parte} truncada"
    # libera a RAM desta metade antes de codificar a proxima
    for i in range(ini, fim):
        try:
            os.remove(f"{d}/lclip{i:02d}.mp4")
        except OSError:
            pass

with open(f"{d}/lista_final.txt", "w") as f:
    f.write("file 'p1.mp4'\nfile 'p2.mp4'\n")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
    "-i", f"{d}/lista_final.txt", "-c", "copy", "-movflags", "+faststart",
    f"{d}/video.mp4"], check=True, capture_output=True, cwd=d)
dv = F.dur(f"{d}/video.mp4")
log(f"etapa 4 ok: video.mp4 {dv:.1f}s")
# A etapa confere a PROPRIA saida. Sem isto, um concat truncado passa batido
# atras de um log de sucesso montado com a medicao da entrada.
assert abs(dv - sum(tempos)) < 5, f"concat truncado: {dv:.1f} vs {sum(tempos):.1f}"

# ------------------------- 5. so agora, com o concat conferido, libera restos
for f in glob.glob(f"{d}/p[12].mp4") + glob.glob(f"{d}/lclip*.mp4"):
    os.remove(f)
log("etapa 5 ok: partes e clipes liberados")

# ---------------------------------------------------------------- 6. trilha
log("etapa 6: trilha")
F.aplicar_trilha(d, "video.mp4", sp["slug"])
log(f"etapa 6 ok: {F.dur(f'{d}/video.mp4'):.1f}s, "
    f"{os.path.getsize(f'{d}/video.mp4') / 1e6:.1f} MB")

# ------------------------------- 7. alguem finalmente OLHA o video
# As seis etapas acima medem se o arquivo saiu: duracao, tamanho, soma dos
# clipes. Nenhuma media se ele esta visivel. As duas queixas visuais que
# chegaram ao dono — cor invertida no CTA e legenda em hindi saindo VAZIA —
# passaram por todos os asserts, porque o arquivo estava perfeito.
import visual as VIS                                              # noqa: E402

_erros, _avisos = VIS.conferir(f"{d}/video.mp4",
                               VIS.hexcor(sp["paleta"].get("bg", "#FFFFFF")))
assert not _erros, "video reprovado no teste visual — nao entregue assim"
log("etapa 7 ok: video conferido quadro a quadro")
log("PACOTE OK")
