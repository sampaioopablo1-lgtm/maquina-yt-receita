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


def arquivo_valido(caminho, minimo):
    """Um clipe parcial de um ffmpeg morto por SIGKILL passa no teste de
    tamanho com conteudo corrompido — o F.dur() seguinte estoura e derruba o
    RETOMA inteiro (lclip38 e lclip46 do setiap-006). Validar e barato;
    apagar o invalido aqui faz o loop refazer so aquele clipe."""
    if not (os.path.exists(caminho) and os.path.getsize(caminho) > minimo):
        return False
    try:
        F.dur(caminho)
        return True
    except Exception:
        os.remove(caminho)
        return False

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


# ---- trava contra relancamento concorrente (2 processos no mesmo workdir
# dobram o consumo de RAM e um refaz o montar apagando o que o outro usa) ----
os.makedirs(d, exist_ok=True)
_lock = f"{d}/.etapas.lock"
if os.path.exists(_lock):
    _pid_antigo = open(_lock).read().strip()
    _vivo = False
    if _pid_antigo.isdigit():
        try:
            os.kill(int(_pid_antigo), 0)
            _vivo = True
        except (OSError, ProcessLookupError):
            _vivo = False
    if _vivo:
        sys.exit(
            f"etapas.py ja esta rodando neste workdir (pid {_pid_antigo}, {d}). "
            f"pkill -f etapas.py, confirme com ps aux | grep python3, e relance UM."
        )
    log(f"lock orfao de pid {_pid_antigo} (processo morto) — assumindo o workdir")
with open(_lock, "w") as f:
    f.write(str(os.getpid()))


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


# A etapa 7 e a que mais reprova — e ela roda DEPOIS de a etapa 5 apagar os
# clipes e de a 6 mixar a trilha. Sem esta marca, rodar de novo apos uma
# reprovacao refazia os 76 clipes (35 min) e, pior, chamava aplicar_trilha
# sobre um video que JA tinha trilha, somando a musica duas vezes num arquivo
# que passa em todos os asserts de duracao e tamanho.
# Aconteceu em seja-mais-magra-001: o teste reprovou por falso positivo e a
# retomada comecou a reconstruir tudo do zero.
PRONTO = f"{d}/longo.ok"
LONGO_PRONTO = arquivo_valido(f"{d}/video.mp4", 1_000_000) and os.path.exists(PRONTO)
if LONGO_PRONTO:
    log("etapas 1-6: longo ja montado e com trilha, retomando do teste visual")

# ---------------------------------------------------------------- 1. assets
# A guarda conta mp3 E thumbnail porque `montar` produz os dois, e a thumbnail
# sai por ultimo (fabrica.py, no fim de montar). Em labtreinamento-001 o
# primeiro run morreu num KeyError do campo `thumb` DEPOIS de gerar os 80 mp3;
# na retomada a contagem de mp3 estava completa, `montar` foi pulado inteiro, e
# o pacote chegou ao fim sem thumbnail — sem nenhum assert reclamar, porque
# nenhuma etapa seguinte olha para esse arquivo.
_mp3_ok = len(glob.glob(f"{d}/l*.mp3")) >= len(sp["longo"])
_thumb = f"{d}/thumbnail.png"
if not LONGO_PRONTO:
    if not (_mp3_ok and os.path.exists(_thumb)):
        log("etapa 1: montar")
        F.montar(spec)
    log(f"etapa 1 ok: {len(glob.glob(f'{d}/l*.mp3'))} mp3 + thumbnail")

# A thumbnail e entregavel: sem ela o pacote sobe sem capa e o CTR morre. Vale
# tanto para o caminho normal quanto para a retomada com LONGO_PRONTO, que pula
# a etapa 1 e nunca passaria pela verificacao acima.
assert os.path.exists(_thumb) and os.path.getsize(_thumb) > 2000, (
    f"thumbnail ausente ou vazia em {_thumb} — `montar` nao chegou ao fim; "
    f"apague os l*.mp3 do pacote e rode de novo, ou gere a thumb antes de seguir")

# --------------------------- 1.5. broll das cenas que pedem (experimento 10)
# Roda ANTES da etapa 2 porque o clipe_cena decide o ramo pela existencia do
# arquivo _broll.mp4. Falha aqui nunca para o render: a cena cai no fallback
# (lower-third sobre preto), que le e nao trava — broll e enfeite.
cenas = sp["longo"]
W, H = 1280, 720
RW, RH = F.render_wh(W, H)
_pedem_broll = [(i, c) for i, c in enumerate(cenas)
                if c.get("layout") == "broll"]
if _pedem_broll and not LONGO_PRONTO:
    import broll as BR                                            # noqa: E402
    _k = BR.chave()
    # A origem da chave vai para o log ANTES de qualquer cena: no
    # agla-level-004 as 7 cenas cairam no fallback e o log nao dizia se
    # faltou chave, candidato ou rede — 20 min de render para a mesma
    # duvida (aprendizado 304).
    log(f"etapa 1.5: chave do Pexels — {BR.ORIGEM_DA_CHAVE}")
    _ok = 0
    for _i, _c in _pedem_broll:
        _dd = F.dur(f"{d}/l{_i:02d}.mp3") + 0.5
        if BR.garantir(d, "l", _i, _c, _dd, RW, RH, api_key=_k):
            _ok += 1
        else:
            log(f"  broll cena {_i} ({_dd:.1f}s) SEM FOOTAGE: {BR.ULTIMO_MOTIVO}")
    log(f"etapa 1.5 ok: broll em {_ok}/{len(_pedem_broll)} cenas")

# ------------------------------------------- 2. clipes, liberando um a um
log("etapa 2: clipes do longo")
tempos = []
# Com o longo pronto os clipes ja foram apagados pela etapa 5, e refaze-los so
# para recalcular `tempos` custa 35 min. Os mesmos numeros estao em tempos.json,
# gravados na etapa 3 a partir dos clipes RENDERIZADOS.
pendentes = [] if LONGO_PRONTO else list(enumerate(cenas))
if LONGO_PRONTO:
    tempos = json.load(open(f"{d}/tempos.json"))
    log(f"etapa 2 pulada: {len(tempos)} tempos lidos de tempos.json")
for i, c in pendentes:
    saida = f"{d}/lclip{i:02d}.mp4"
    if not arquivo_valido(saida, 10000):
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

# O copy.md sai daqui e nao do `render()` da fabrica, que esta esteira nunca
# chama — era por isso que TODO pacote feito por etapas.py ficava sem ele, e o
# publicar.py caia no texto da spec com "{CAPITULOS}" ainda por preencher.
# Medido em 13/08/2026 no seviye-seviye-002, ja publicado com o placeholder.
# Fica junto da legenda de proposito: os dois dependem de `tempos`, que so
# existe aqui e some quando os clipes sao apagados.
F.escrever_copy(sp, tempos, d)
log("etapa 3 ok: legendas.srt + tempos.json + copy.md")

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
partes = [] if LONGO_PRONTO else list(enumerate(((0, meio), (meio, len(cenas))), start=1))
for parte, (ini, fim) in partes:
    saida = f"{d}/p{parte}.mp4"
    if arquivo_valido(saida, 100000):
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

if not LONGO_PRONTO:
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

    # --------------------- 5. so agora, com o concat conferido, libera restos
    for f in glob.glob(f"{d}/p[12].mp4") + glob.glob(f"{d}/lclip*.mp4"):
        os.remove(f)
    log("etapa 5 ok: partes e clipes liberados")

    # ------------------------------------------------------------ 6. trilha
    # A marca so e escrita DEPOIS da trilha entrar. Ela e o que impede a
    # proxima retomada de mixar musica sobre musica.
    log("etapa 6: trilha")
    F.aplicar_trilha(d, "video.mp4", sp["slug"], sp.get("trilha"))
    open(PRONTO, "w").write(f"longo montado, trilha {sp['trilha']}\n")
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

# ---------------------------------------------------------------- 8. short
# O short era renderizado por script avulso e NUNCA passava no teste visual —
# foi assim que todos os shorts 9:16 sairam com o layout 16:9 estourando as
# bordas sem ninguem notar (kp-plan-9233 pegou 6/6 quadros com tinta na borda).
# Agora ele e parte do pacote: mesma fabrica, mesmo teste, mesmo assert.
log("etapa 8: short")
if not (os.path.exists(f"{d}/short.mp4") and os.path.getsize(f"{d}/short.mp4") > 100000):
    SW, SH = 720, 1280
    SRW, SRH = F.render_wh(SW, SH)
    for i, c in enumerate(sp["short"]):
        saida = f"{d}/sclip{i:02d}.mp4"
        if arquivo_valido(saida, 10000):
            continue
        dd = F.dur(f"{d}/s{i:02d}.mp3") + 0.5
        with open(f"{d}/s{i:02d}.srt", "w") as srt:
            srt.write(f"1\n{F.st(0.2)} --> {F.st(dd - 0.15)}\n{c['nar']}\n")
        nf = max(int(dd * 30), 1)
        F.clipe_cena(d, "s", i, c, dd, nf, SRW, SRH)
    with open(f"{d}/slista.txt", "w") as f:
        for i in range(len(sp["short"])):
            f.write(f"file 'sclip{i:02d}.mp4'\n")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
        "-i", f"{d}/slista.txt", "-vf", f"scale={SW}:{SH}:flags=lanczos",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        f"{d}/short.mp4"], check=True, capture_output=True, cwd=d)
    F.aplicar_trilha(d, "short.mp4", sp["slug"], sp.get("trilha"))
ds = F.dur(f"{d}/short.mp4")
assert 20 <= ds <= 60, f"short com {ds:.1f}s — fora da faixa 30-45s (tolerancia 20-60)"
_erros, _avisos = VIS.conferir(f"{d}/short.mp4",
                               VIS.hexcor(sp["paleta"].get("bg", "#FFFFFF")))
assert not _erros, "short reprovado no teste visual — nao entregue assim"
log(f"etapa 8 ok: short.mp4 {ds:.1f}s, conferido quadro a quadro")
log("PACOTE OK")

try:
    os.remove(_lock)
except OSError:
    pass
