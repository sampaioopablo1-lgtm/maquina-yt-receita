# -*- coding: utf-8 -*-
"""Estrutura do OPC05, em um lugar so. Tudo em segundos da FONTE (IMG_2007.MOV)."""

SRC = "IMG_2007.MOV"
FPS = 30
W, H = 1080, 1920

# trechos de fala, na ordem final. (inicio, fim, texto revisado)
FALA = [
    (38.70, 39.82, "a agência vai te cobrar"),
    (46.12, 49.70, "cinco mil, dez mil, e vamos muito mais para cima"),
    (50.16, 53.50, "mas existe uma forma de você mesmo, empresário, fazer isso"),
    (53.60, 56.50, "se dedicando talvez trinta minutos, uma hora por semana"),
    (19.58, 23.90, "imagine todo dia, pela manhã antes de chegar no seu negócio, seu whatsapp está bombando"),
    (13.90, 17.66, "é importante ter uma geração de demanda de aquisição previsível"),
    (24.48, 26.84, "para isso, existem anúncios na internet"),
    (62.06, 63.18, "siga aqui no instagram"),
    (64.10, 70.25, "estou para te orientar a como construir essa máquina previsível de geração de clientes"),
]

# planos visuais: (tipo, fonte, entrada, indices de FALA que ele cobre, dissolvencia_na_entrada)
PLANOS = [
    ("rosto", SRC,                  None, [0, 1], False),
    ("broll", "bx/px_12894347.mp4", 1.0,  [2],    True),   # maos digitando: voce mesmo fazendo
    ("broll", "bx/px_17512949.mp4", 0.5,  [3],    False),  # dedo no celular: pouco tempo por semana
    ("broll", "bx/px_10374888.mp4", 0.5,  [4],    False),  # rolando o celular: whatsapp bombando
    ("broll", "bx/px_8322398.mp4",  3.0,  [5],    True),   # pes na calcada: fluxo de demanda
    ("broll", "bx/px_8971235.mp4",  0.5,  [6],    False),  # gente circulando: alcance dos anuncios
    ("rosto", SRC,                  None, [7, 8], True),
]

DISSOLVE = 0.5   # 15 quadros a 30 fps, nas viradas de assunto
WHOOSH_ANTES = 0.10
TETO_PCM = 0.86


def durs():
    return [round(b - a, 3) for a, b, _ in FALA]


def blocos():
    """Devolve, por plano: (i0, t_inicio, t_fim, duracao)."""
    d = durs()
    ini = [round(sum(d[:i]), 3) for i in range(len(d) + 1)]
    out = []
    for p in PLANOS:
        idx = p[3]
        out.append((idx[0], ini[idx[0]], ini[idx[-1] + 1],
                    round(ini[idx[-1] + 1] - ini[idx[0]], 3)))
    return out, ini


if __name__ == "__main__":
    bl, ini = blocos()
    print("total %.2f s" % ini[-1])
    for p, (i0, a, b, d) in zip(PLANOS, bl):
        print("  %-5s %-22s %6.2f -> %6.2f  (%.2f s)%s" %
              (p[0], p[1].split("/")[-1], a, b, d, "  dissolvencia" if p[4] else ""))
