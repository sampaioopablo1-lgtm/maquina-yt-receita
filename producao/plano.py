# -*- coding: utf-8 -*-
"""OPC06 -- previsibilidade de crescimento. Take IMG_2010."""

SRC = "IMG_2010.MOV"
FPS = 30
W, H = 1080, 1920

FALA = [
    (19.52, 25.32, "muitas empresas realmente só existem, elas somente seguem o baile, mas isso é muito perigoso"),
    (0.92, 6.40, "se você sabe me responder quanto o seu negócio vai crescer no próximo mês, você tem previsibilidade"),
    (13.86, 19.14, "é importante ter um processo de crescimento previsível, um processo calculado"),
    (25.22, 30.78, "é importante ter uma estratégia de crescimento, de aquisição de clientes todos os dias no whatsapp"),
    (31.44, 34.60, "aqui em nosso instagram do próximo cliente, vou te passar dicas"),
    (41.82, 45.10, "siga o próximo cliente e nos vemos nos próximos conteúdos"),
]

PLANOS = [
    ("rosto", SRC,                  None, [0],    False),
    ("broll", "bx/q_13675325.mp4",  0.5,  [1],    True),   # maos no volante: quem dirige, controla
    ("broll", "bx/q_6266437.mp4",   4.5,  [2],    False),  # teclado: o processo calculado
    ("broll", "bx/q_7821861.mp4",   1.2,  [3],    True),   # celular acendendo: cliente chegando
    ("rosto", SRC,                  None, [4, 5], True),
]

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


if __name__ == "__main__":
    bl, ini = blocos()
    print("total %.2f s" % ini[-1])
    for p, (i0, a, b, d) in zip(PLANOS, bl):
        print("  %-5s %-22s %6.2f -> %6.2f  (%.2f s)%s" %
              (p[0], p[1].split("/")[-1], a, b, d, "  dissolvencia" if p[4] else ""))
