"""Os QUATRO temas do pipeline do dono — e por que cada canal recebe um.

POR QUE ESTE ARQUIVO EXISTE (19/10/2026). O dono olhou as pecas publicadas e
disse: *"os videos publicados, me parecem todos a mesma dinamica, imagens,
formas, estilo. Em todos os canais. Ajuste. Explore a documentacao."*

**Ele esta certo, e o numero e meu.** Varridas as 205 specs de short da frota:

    layouts existentes no short      4   (titulo, item, lista, cta)
    cenas em `item` + `titulo`       1.554 de 1.667 = 93%
    esqueleto mais repetido          titulo-titulo-titulo-titulo-cta
                                     -- o MESMO nos TRES canais
    paletas                          TODAS claras: bg #F3F7FA (epomeno),
                                     #F4F1EA (kolejny), #F5F3ED (labtreinamento)

Tres canais, tres fundos quase iguais, as mesmas quatro formas e o mesmo
esqueleto no topo dos tres. Nao e impressao dele: e a contagem.

DE ONDE VEM O CONSERTO — da DOCUMENTACAO DELE, nao do meu gosto. O pacote
`pipeline_canal_dark_v2.0.zip` que ele mandou em 12/10 traz `motor/config.py`
com **quatro** temas prontos, cada um com descricao escrita por ele dizendo
para que serve. Os quatro estao copiados abaixo SEM MUDANCA.

A ATRIBUICAO POR CANAL, com a procedencia de cada escolha:

  * `labtreinamento` -> **noite**. Nao e escolha: e MEDIDO. O longo de 8 min que
    ele aponta como referencia (`FtCtIJPsc_Q`) e peca dele, feita com este
    pipeline, e a paleta dela bate com este tema. Ver `paleta_referencia.py`.
  * `epomeno-epipedo` -> **papel**. A descricao DELE nomeia o caso: *"Para
    historia, educacao, biografias, financas pessoais."* O canal e financas
    pessoais em grego.
  * `kolejny-poziom` -> **misterio**, e esta e **escolha por ELIMINACAO, nao
    medicao** -- vai dita assim em vez de vendida como derivacao. `noite` e do
    labtreinamento e `neon` e descrito para *"games, tecnologia, internet,
    cultura pop"*, que nao e o canal. Sobra `misterio`, e ele tem dois apoios
    fracos: o par escuro+vermelho le como RISCO, que e o assunto do canal
    (custo do credito), e a fonte dele (Oswald) cobre os diacriticos poloneses,
    enquanto a do `neon` (Bebas Neue) nao tem minuscula.

**O QUE ESTE ARQUIVO NAO MUDA, e e deliberado: a FONTE.** Os temas trazem
`fonte_titulo` e `fonte_texto`, e trocar familia de fonte arrisca glifo ausente
em grego e em polones -- defeito que so aparece DEPOIS de publicar, e que a
regra do §3.8 manda nao arriscar sem medir. Aqui atravessa so a COR. A fonte
fica como passo medido: conferir no runner quais familias estao instaladas
antes de mexer.

**E A TRAVA 601 CONTINUA VALENDO AO CONTRARIO:** nunca copie paleta de um canal
para outro. Este modulo existe justamente para que cada canal tenha a SUA, e
`paleta_do_canal` levanta se alguem pedir canal fora do mapa em vez de devolver
um padrao -- padrao silencioso e como os tres fundos ficaram iguais.
"""
from __future__ import annotations

# Copiado de motor/config.py do pipeline do dono, tema por tema, sem mudanca.
# E ESSE ARQUIVO NAO ESTA NO REPO (medido em 19/10 as 06:1x): o ZIP foi lido numa
# sessao anterior e nao foi comitado, logo isto e TRANSCRICAO. O que salva estes
# hex de terem apoio unico e a medicao independente no video publicado dele —
# luminancia 37 do fundo e o SATAVG dos 530 quadros, em
# `fabrica/video_referencia.py`. Ver `docs/pacote-do-dono-NAO-esta-no-repo.md`.
TEMAS = {
    "noite": dict(
        descricao="Escuro azulado com destaque turquesa. Serve para quase tudo: "
                  "curiosidades, ciencia, tecnologia, historia.",
        cores=dict(bg="#0E1117", panel="#161B24", panel2="#1E2430", line="#2C3442",
                   txt="#EEF1F5", txt2="#C9D1DC", mut="#8B95A5",
                   acc="#3DDBD9", acc2="#F5A524", red="#FF5A5F", ok="#3CCB7F",
                   ink="#0B0E13", win="#0B0E13"),
        fonte_titulo="Anton", fonte_texto="Inter", maiusculas=True),
    "misterio": dict(
        descricao="Preto com vermelho e tom de osso. Para misterio, casos reais, "
                  "lendas, terror leve.",
        cores=dict(bg="#0B0B0C", panel="#151517", panel2="#1D1D20", line="#2E2E33",
                   txt="#F2EEE8", txt2="#D6CFC4", mut="#8F877C",
                   acc="#E23B3B", acc2="#D9C7A7", red="#FF4D4D", ok="#7FB77E",
                   ink="#0B0B0C", win="#08080A"),
        fonte_titulo="Oswald", fonte_texto="Source Sans 3", maiusculas=True),
    "papel": dict(
        descricao="Claro, cor de papel, com terracota. Para historia, educacao, "
                  "biografias, financas pessoais.",
        cores=dict(bg="#F4EFE6", panel="#FFFFFF", panel2="#EDE6D8", line="#D8CFBE",
                   txt="#1B1A17", txt2="#3A3833", mut="#7A7263",
                   acc="#C8502A", acc2="#2B6CB0", red="#B83227", ok="#2E8B57",
                   ink="#FFFFFF", win="#FBF8F2"),
        fonte_titulo="Playfair Display", fonte_texto="Inter", maiusculas=False),
    "neon": dict(
        descricao="Roxo escuro com verde-limao e magenta. Para games, tecnologia, "
                  "internet, cultura pop.",
        cores=dict(bg="#0C0A1A", panel="#16122B", panel2="#201A3D", line="#342A5E",
                   txt="#F3F0FF", txt2="#D5CEF2", mut="#9A90C2",
                   acc="#B6FF3B", acc2="#FF4FD8", red="#FF4F6D", ok="#3BFFB0",
                   ink="#0C0A1A", win="#0A0816"),
        fonte_titulo="Bebas Neue", fonte_texto="Space Grotesk", maiusculas=True),
}

# canal -> (tema, procedencia da escolha)
TEMA_DO_CANAL = {
    "labtreinamento":  ("noite",    "MEDIDO: a paleta do longo da referencia do proprio dono"),
    "epomeno-epipedo": ("papel",    "A descricao DELE nomeia 'financas pessoais'"),
    "kolejny-poziom":  ("misterio", "ELIMINACAO: noite e de outro canal e neon e de games"),
}


# AJUSTE por canal, e cada um carrega a MEDIDA que o justifica. Sem esta tabela
# a escolha viraria "o mapa mudou e ninguem sabe por que".
AJUSTES = {
    # O nosso `c2` PREENCHE forma (o circulo do `item`, as barras). No video da
    # referencia forma e PAINEL, nao acento: o `acc2` do tema (#F5A524, laranja
    # saturado) romperia o SATAVG de 3,4 a 5,6 medido nos 530 quadros dela.
    "labtreinamento": {"c2": "panel2"},
}

# Chaves que so os layouts de LONGO usam (`layouts_longo.py`): o par errado/certo
# e o painel. Chave a mais nao muda o short, que le `bg`, `ink`, `c1` e `c2`.
EXTRAS = ("red", "ok", "panel", "mut", "acc")


def paleta_do_tema(tema: str) -> dict:
    """As quatro chaves que o nosso render usa, tiradas das cores DELE.

    O mapa e fixo e explicito de proposito: `bg`->bg, `ink`->txt (a tinta do
    texto sobre o fundo), `c1`->acc, `c2`->acc2. Sem isto cada rodada
    escolheria uma chave diferente e os canais voltariam a convergir.
    """
    if tema not in TEMAS:
        raise KeyError(
            f"tema {tema!r} nao existe no pipeline do dono; os quatro sao "
            f"{sorted(TEMAS)} — inventar um quinto e paleta minha outra vez"
        )
    c = TEMAS[tema]["cores"]
    pal = {"bg": c["bg"], "ink": c["txt"], "c1": c["acc"], "c2": c["acc2"]}
    pal.update({k: c[k] for k in EXTRAS if k in c})
    return pal


def paleta_do_canal(canal: str) -> dict:
    """LEVANTA para canal desconhecido — padrao silencioso foi o defeito."""
    if canal not in TEMA_DO_CANAL:
        raise KeyError(
            f"canal {canal!r} nao tem tema atribuido. Devolver um padrao aqui e "
            "como os tres fundos ficaram quase iguais: escolha e escreva a "
            "procedencia em TEMA_DO_CANAL."
        )
    c = TEMAS[TEMA_DO_CANAL[canal][0]]["cores"]
    pal = paleta_do_tema(TEMA_DO_CANAL[canal][0])
    for chave, de in AJUSTES.get(canal, {}).items():
        pal[chave] = c[de]
    return pal


def fundo_escuro(canal: str) -> bool:
    """Fundo escuro pelo mesmo limiar de `paleta_referencia` (luma < 180)."""
    h = paleta_do_canal(canal)["bg"].lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b < 180


def relato() -> str:
    linhas = ["TEMAS do pipeline do dono aplicados por canal:"]
    for canal, (tema, por) in TEMA_DO_CANAL.items():
        p = paleta_do_canal(canal)
        linhas.append(f"  {canal:<16} -> {tema:<9} bg {p['bg']} ink {p['ink']} "
                      f"c1 {p['c1']} c2 {p['c2']}")
        linhas.append(f"  {'':<16}    porque: {por}")
    linhas.append("  a FONTE de cada tema NAO atravessa: glifo ausente em grego "
                  "ou polones so aparece depois de publicar.")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relato())
