# -*- coding: utf-8 -*-
"""O mapa de dono MEDIDO das origens — a medicao que vivia so em PROSA.

**Medido em 20/10 as 10:1x, na TERCEIRA vez que eu tirei a mesma origem da
escolha a mao.** O `concentracao.origem_de_outro_canal` existe desde 18/10 e
exige um `dono_medido` — *"{youtube_id: canal}, e tem de vir de MEDICAO"* —, e o
`pauta_do_momento` nasceu em 20/10 as 08:2x chamando-o. Nas duas rodadas em que
ele teve o que dizer o relato saiu com **"mapa de dono MEDIDO ausente"**, porque
ninguem passava o mapa: ele nao existia como DADO em lugar nenhum.

**E a medicao existia, escrita em PROSA:** em 18/10 as 01:2x o `QiaGg03WSR0` foi
medido como longo do **LabTreinamento** (campo `author` da propria pagina,
509 s), enquanto dois shorts do `kolejny-poziom` o declaram como origem. Essa
frase esta no `CLAUDE.md`, no docstring do `concentracao.py` e no do
`pauta_do_momento.py` — **em nenhum lugar que um instrumento possa LER.**

**O custo e de ESCOLHA DE PAUTA e esta medido:** nesta rodada o
`pauta_do_momento` deu `QiaGg03WSR0` como ESCOLHIDA no `kolejny-poziom` (2 usos,
52 de 56 capitulos intocados, a maior reserva do empate). Com o mapa, ela sai da
escolha NOMEADA e a vez passa ao `SZV9Vk5YFwI`. Nas rodadas de 01:3x e 07:4x eu
a tirei **a mao**, escrevendo na copy que *"este arquivo registra que ele e longo
do LabTreinamento"* — isto e o item 3 da §10 na quinta dimensao, e a classe dos
layouts mortos numa forma nova: **o dado estava escrito e ninguem podia
chama-lo.**

**O QUE ENTRA AQUI, e o criterio e estreito de proposito:** somente id cujo dono
foi **MEDIDO** na pagina do proprio video, com a procedencia ao lado. Palpite,
ausencia da playlist e "parece de outro canal" **nao entram** — a primeira versao
do `origem_de_outro_canal` acusava origem ausente da playlist e deu DOIS falsos
positivos (725), e um mapa frouxo reintroduz exatamente isso, agora como dado
compartilhado.

**E O MAPA NAO E EXAUSTIVO, e isso tem de continuar dito:** ausencia de medicao
nao e ausencia de problema. O relato de quem o usa diz quantas entradas ele tem
E que origem fora dele e DESCONHECIDA, nunca "do proprio canal".
"""

# {youtube_id: (canal_dono, procedencia MEDIDA)}
#
# A procedencia e obrigatoria por construcao: entrada sem ela nao passa no
# `_valida`, porque mapa de dono sem medicao ao lado e palpite com cara de dado.
MEDIDOS = {
    "QiaGg03WSR0": (
        "labtreinamento",
        "18/10 as 01:2x — `author` LabTreinamento na pagina do proprio video, "
        "509 s, `isUnlisted` falso. Declarado como origem por "
        "`kolejny-poziom-s004` e `-s035`, cujas FONTES dizem "
        "`kolejny-poziom-018`: o ID esta errado, nao o conteudo.",
    ),
}


def _valida(mapa: dict) -> dict:
    """Levanta se uma entrada nao trouxer procedencia, em vez de aceitar
    palpite — a mesma disciplina do `provedor` obrigatorio no parque (733)."""
    for oid, v in mapa.items():
        if not isinstance(v, tuple) or len(v) != 2:
            raise ValueError(
                "entrada %r sem (canal, procedencia): mapa de dono sem medicao "
                "ao lado e palpite com cara de dado" % oid)
        canal, proc = v
        if not canal or not proc or len(proc) < 40:
            raise ValueError(
                "entrada %r com procedencia vazia ou curta demais para dizer "
                "ONDE foi medida: %r" % (oid, proc))
    return mapa


def mapa() -> dict:
    """{youtube_id: canal}, na forma que o `origem_de_outro_canal` cobra."""
    return {oid: v[0] for oid, v in _valida(MEDIDOS).items()}


def procedencia(oid: str) -> str | None:
    """ONDE o dono daquele id foi medido. `None` para id fora do mapa — e id
    fora do mapa e DESCONHECIDO, nunca do proprio canal."""
    v = _valida(MEDIDOS).get(oid)
    return v[1] if v else None


def relato() -> str:
    L = ["DONO MEDIDO: %d origem(ns) com dono medido na pagina." % len(MEDIDOS)]
    for oid, (canal, proc) in sorted(_valida(MEDIDOS).items()):
        L.append("  %-12s -> %s" % (oid, canal))
        L.append("      %s" % proc)
    L.append("  o mapa NAO e exaustivo: origem fora dele e DESCONHECIDA, nunca "
             "do proprio canal. Ausencia de medicao nao e ausencia de problema.")
    return "\n".join(L)


def main() -> int:
    print(relato())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
