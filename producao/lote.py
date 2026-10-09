# -*- coding: utf-8 -*-
"""Os planos dos Reels restantes, num arquivo so. Escreve plano.py e roda a esteira."""
import json, os, shutil, subprocess, sys

PLANOS = {
"OPC07_whatsapp": dict(
  src="IMG_2011.MOV", tr="tr_IMG_2011.json",
  fala=[
    (1.10, 5.90,  "você já perdeu clientes por demorar a responder no whatsapp"),
    (10.24,16.70, "e infelizmente isso acontece, às vezes por falta de dar aquela devida atenção, o cliente vai para a concorrência"),
    (17.30,19.10, "e como é que você resolve isso"),
    (19.38,24.06, "muitos empresários, muitas empresas botam uma pessoa para atender, mas mesmo"),
    (27.28,33.02, "e hoje temos a ia, certamente é uma inovação que tem ajudado bastante"),
    (33.62,37.90, "aqui em nosso canal no instagram, dicas como essa"),
    (63.30,66.30, "siga o próximo cliente que eu te ajudo a encontrar o seu"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/r_10397453.mp4",  1.0,  [1],    True),
    ("broll", "bx/s_5846713.mp4",   1.0,  [2,3],  False),
    ("broll", "bx/r_6755168.mp4",   1.0,  [4],    True),
    ("rosto", None,                 None, [5,6],  True),
  ]),

"OPC08_independencia": dict(
  src="IMG_2315.MOV", tr="tr_IMG_2315.json",
  fala=[
    (0.30, 5.90,  "empresário, você está disposto a sair desse lugar de não crescimento para um lugar"),
    (5.90, 9.30,  "de escala através de investimento em anúncios, é isso mesmo"),
    (9.54, 13.78, "você já investiu em agência, até mesmo se frustrou no passado, eu quero te ensinar"),
    (21.30,25.48, "existe uma maneira prática, existe uma maneira bem didática para você desenvolver"),
    (25.60,29.34, "eu não quero transformar você em um próximo gestor de tráfego, eu quero te ensinar"),
    (29.34,35.72, "a ter uma independência de crescimento do seu negócio, para você destravá-lo aí e ter uma escala e fazer acontecer"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/s_7981954.mp4",   0.5,  [1],    True),
    ("broll", "bx/s_8053942.mp4",   1.0,  [2],    False),
    ("broll", "bx/s_6391707.mp4",   0.5,  [3],    True),
    ("broll", "bx/r_8348130.mp4",   0.5,  [4],    False),
    ("rosto", None,                 None, [5],    True),
  ]),

"OPC09_prospeccao": dict(
  src="IMG_2015.MOV", tr="tr_IMG_2015.json",
  fala=[
    (29.22,35.06, "como eu crio um processo onde eu posso ter todos os dias próximos clientes caindo no meu instagram"),
    (35.48,40.52, "onde que eu posso estar ligando para essas pessoas ou para essas empresas, se você for um"),
    (40.52,47.92, "caso de b2b, de uma maneira, para que você consiga ir de forma ativa procurar novas parcerias"),
    (19.00,23.80, "é importante você ter estratégias de forma previsíveis e organizadas para você ter o"),
    (65.10,69.20, "siga aqui no nosso instagram que você vai ter dicas e informações"),
    (69.96,73.20, "para que a gente possa te ajudar a ter o seu próximo cliente"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/r_6406024.mp4",   0.5,  [1],    True),
    ("broll", "bx/s_6391707.mp4",   0.5,  [2],    False),
    ("broll", "bx/r_13601612.mp4",  0.5,  [3],    True),
    ("rosto", None,                 None, [4,5],  True),
  ]),

"OPC10_grandes_marcas": dict(
  src="IMG_2319.MOV", tr="tr_IMG_2319.json",
  fala=[
    (5.50, 9.40,  "sai desse lugar onde você não tem controle sobre novos clientes do seu negócio"),
    (28.04,33.40, "empresas grandes hoje, como coca-cola, pepsi, até mesmo em outros segmentos como"),
    (33.40,37.72, "amazon, spotify, enfim, eles têm um processo de divulgação e investimento"),
    (37.72,43.74, "absurdo e o padrão é o mesmo, independente"),
    (43.74,47.74, "do meu tamanho, continuar investindo para que não só cresça o meu negócio, mas"),
    (47.74,51.66, "para que eu sobreviva, o mercado cada vez mais está competitivo"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/r_7812348.mp4",   1.5,  [1],    True),
    ("broll", "bx/s_5846713.mp4",   1.0,  [2],    False),
    ("broll", "bx/s_13736548.mp4",  0.5,  [3],    False),
    ("broll", "bx/r_6339911.mp4",   0.5,  [4],    True),
    ("rosto", None,                 None, [5],    True),
  ]),

"OPC11_nao_sou_agencia": dict(
  src="IMG_2294.MOV", tr="tr_IMG_2294.json",
  fala=[
    (24.80,30.70, "e eu não sou agência, e até mesmo não sou uma agência que gostaria de ser mais uma no mercado"),
    (14.42,18.76, "uma maneira para a gente corrigir isso é ter um método claro, um processo simples e"),
    (18.76,24.20, "objetivo através de anúncios online para que você possa ter clientes todos os dias no seu whatsapp"),
    (31.76,36.70, "na verdade eu quero te ensinar a como fazer, em vez de você pagar dez, quinze, vinte mil ou até"),
    (36.70,41.90, "mais por ano em uma agência, eu vou te ensinar como fazer uma campanha"),
    (43.38,45.58, "para que você traga clientes todos os dias para o seu whatsapp"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/r_10397453.mp4",  1.0,  [1],    True),
    ("broll", "bx/r_8348130.mp4",   0.5,  [2],    False),
    ("broll", "bx/s_6391707.mp4",   0.5,  [3],    True),
    ("rosto", None,                 None, [4,5],  True),
  ]),
"OPC12_imagine_acordar": dict(
  src="IMG_2302.MOV", tr="tr_IMG_2302.json",
  fala=[
    (0.00, 5.30,  "agora imagine você acordar amanhã, o seu whatsapp está bombando, caindo novos clientes para o seu negócio"),
    (5.86, 13.38, "e isso não é uma fórmula mágica, isso não é uma missão impossível, inclusive você deve estar pagando caro por uma agência se está fazendo isso pra você"),
    (13.88,19.54, "agora imagine o dinheiro que você está investindo em uma agência, você mesmo possa investir no seu negócio"),
    (30.14,34.90, "e é muito simples e muito objetivo, em uma hora ou até menos você consegue fazer esse anúncio"),
    (35.20,37.50, "e para isso tem método, tem processo"),
    (61.06,63.66, "venha para o programa o próximo cliente"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/r_6755168.mp4",   1.0,  [1],    True),
    ("broll", "bx/s_7981954.mp4",   0.5,  [2],    False),
    ("broll", "bx/px_12894347.mp4", 1.0,  [3],    True),
    ("rosto", None,                 None, [4,5],  True),
  ]),

"OPC13_escolheu_o_concorrente": dict(
  src="IMG_2304.MOV", tr="tr_IMG_2304.json",
  fala=[
    (0.52, 6.90,  "seja sincero comigo, você já ficou frustrado por descobrir que aquela pessoa que você encontrou"),
    (6.90, 13.88, "não entrou no seu negócio, e certamente ela escolheu o concorrente para poder comprar"),
    (14.58,21.70, "eu sei como é que é, isso é difícil, mas talvez essa pessoa só encontrou o seu concorrente porque ela foi impactada por algum vídeo, como isso aqui"),
    (31.06,35.80, "queremos que o seu negócio prospere, mas para isso você precisa aprender a divulgar"),
    (65.90,71.76, "é isso, forte abraço, clique que eu te vejo do outro lado da mentoria, e vamos para cima que vendas não dá para esperar"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/px_8971235.mp4",  0.5,  [1],    True),
    ("broll", "bx/s_8053942.mp4",   1.0,  [2],    False),
    ("broll", "bx/r_6406024.mp4",   0.5,  [3],    True),
    ("rosto", None,                 None, [4],    True),
  ]),

"OPC14_em_vez_da_agencia": dict(
  src="IMG_2308.MOV", tr="tr_IMG_2308.json",
  fala=[
    (0.00, 8.68,  "você gostaria de aprender a divulgar o seu próprio negócio de forma objetiva e clara, sem enrolação? participa da mentoria o próximo cliente"),
    (9.08, 17.88, "em vez de você investir cinco, trinta mil em uma divulgação através de uma agência de marketing digital, você empresário, você empreendedora, eu vou te ensinar a fazer isso"),
    (17.88,23.22, "para que você possa ter previsibilidade e controle sobre o seu processo de crescimento"),
    (30.22,37.58, "imagine você mesmo poder gerar pessoas interessadas para o seu whatsapp, abrir o seu celular e todos os dias ali ter cliente para responder"),
    (39.04,44.92, "clique agora, preenche a aplicação para que a gente possa marcar uma conversa, e eu te vejo na próxima turma"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/s_6391707.mp4",   0.5,  [1],    True),
    ("broll", "bx/q_13675325.mp4",  0.5,  [2],    False),
    ("broll", "bx/px_17512949.mp4", 0.5,  [3],    True),
    ("rosto", None,                 None, [4],    True),
  ]),

"OPC15_aluguel_sim_anuncio_nao": dict(
  src="IMG_2314.MOV", tr="tr_IMG_2314.json",
  fala=[
    (0.00, 6.04,  "quando falam para você que é preciso investir no seu negócio para ele atrair novos clientes todos os dias, o que você pensa"),
    (7.04, 13.18, "mas quando falam para você que é preciso pagar cinco, dez, quinze mil de aluguel"),
    (22.64,27.28, "pois é, tem empresários dispostos a investir cinco, dez, quinze, trinta mil em aluguel"),
    (33.68,39.42, "mas tem dificuldade em ouvir investir cinco, dez, quinze, vinte mil em anunciar a sua própria marca, a sua própria empresa"),
    (53.76,59.12, "então não tenha medo e invista no crescimento do seu negócio, porque se o negócio não crescer ele morre"),
    (66.16,70.66, "clica nesse vídeo para poder preencher a nossa aplicação"),
  ],
  planos=[
    ("rosto", None,                 None, [0],    False),
    ("broll", "bx/s_13736548.mp4",  0.5,  [1],    True),
    ("broll", "bx/r_7812348.mp4",   1.5,  [2],    False),
    ("broll", "bx/r_8348130.mp4",   0.5,  [3],    True),
    ("rosto", None,                 None, [4,5],  True),
  ]),

"OPC16_o_que_e_a_mentoria": dict(
  src="IMG_2309.MOV", tr="tr_IMG_2309.json",
  fala=[
    (0.96, 8.04,  "eu estou aqui com o pessoal para poder entrar na próxima turma do próximo cliente, você pode falar sobre o programa aqui para eles"),
    (9.26, 15.06, "opa, claro, bora lá, o programa o próximo cliente é uma mentoria prática"),
    (15.06,21.14, "focada em ensinar empresários e profissionais como criar anúncios online que trazem"),
    (21.14,26.96, "clientes todos os dias direto para o whatsapp, sem depender de agência ou terceiros"),
    (37.46,43.62, "é prático, direto e feito para você ter previsibilidade de clientes toda semana"),
    (50.00,54.26, "você vai ver o passo a passo para poder ter clientes todos os dias, só clicar nesse vídeo aqui para se inscrever"),
  ],
  planos=[
    ("rosto", None,                 None, [0,1],  False),
    ("broll", "bx/r_13601612.mp4",  0.5,  [2],    True),
    ("rosto", None,                 None, [3],    False),
    ("broll", "bx/r_10397453.mp4",  1.0,  [4],    True),
    ("rosto", None,                 None, [5],    True),
  ]),
}

CABECA = '''# -*- coding: utf-8 -*-
SRC = %r
FPS = 30
W, H = 1080, 1920
FALA = %r
PLANOS = %r
DISSOLVE = 0.5
WHOOSH_ANTES = 0.10
TETO_PCM = 0.86
def durs():
    return [round(b - a, 3) for a, b, _ in FALA]
def blocos():
    d = durs()
    ini = [round(sum(d[:i]), 3) for i in range(len(d) + 1)]
    out = []
    for p in PLANOS:
        idx = p[3]
        out.append((idx[0], ini[idx[0]], ini[idx[-1] + 1],
                    round(ini[idx[-1] + 1] - ini[idx[0]], 3)))
    return out, ini
'''


def escrever(nome):
    p = PLANOS[nome]
    planos = [(t, f or p["src"], e, i, d) for t, f, e, i, d in p["planos"]]
    open("plano.py", "w").write(CABECA % (p["src"], p["fala"], planos))
    # ARMADILHA CARA: se tr.json for um symlink (renderizando em pasta
    # paralela), shutil.copy SEGUE o link e escreve no arquivo de origem,
    # compartilhado. Quatro videos gravaram no mesmo tr.json e tres sairam com
    # a legenda de outro take. Apague o link antes de copiar.
    if os.path.islink("tr.json") or os.path.exists("tr.json"):
        os.remove("tr.json")
    shutil.copy(p["tr"], "tr.json")


def rodar(nome):
    escrever(nome)
    shutil.rmtree("planos", ignore_errors=True)
    shutil.rmtree("leg", ignore_errors=True)
    for etapa in ("monta_video.py", "monta_audio.py", "legendas.py"):
        r = subprocess.run(["python3", etapa], capture_output=True, text=True)
        if r.returncode:
            print(nome, etapa, "FALHOU\n", r.stderr[-800:]); return False
    # render com o nome certo
    src = open("render.py").read()
    import re
    src = re.sub(r'"OPC\w+\.mp4"', '"%s.mp4"' % nome, src)
    open("render_tmp.py", "w").write(src)
    r = subprocess.run(["python3", "render_tmp.py"], capture_output=True, text=True)
    if r.returncode or not os.path.exists(nome + ".mp4"):
        print(nome, "RENDER FALHOU\n", r.stderr[-800:]); return False
    subprocess.run(["/usr/local/bin/ffmpeg", "-v", "error", "-y", "-i", nome + ".mp4",
                    "-c:v", "libx264", "-profile:v", "high", "-crf", "21", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "copy",
                    "entrega_%s.mp4" % nome], check=True)
    bl, ini = __import__("importlib").import_module("plano").blocos() if False else (None, None)
    print("%-24s pronto  %s" % (nome, os.path.getsize("entrega_%s.mp4" % nome)))
    return True


if __name__ == "__main__":
    for nome in sys.argv[1:] or list(PLANOS):
        rodar(nome)
