#!/usr/bin/env python3
"""Quanto a pauta de um canal está CONCENTRADA numa origem só.

POR QUE ISTO EXISTE, e é um hábito meu que eu só vi ao contar. Em 13/10/2026,
às 04:0x, o `labtreinamento` tinha **dez** shorts tirados do MESMO longo
(`ntrMxq89I4o`) enquanto **nove** das suas treze origens tinham sido usadas
**uma vez só** — e há doze specs de longo no canal, com 55 a 87 capítulos cada.
Eu vinha minerando um longo por rodada porque era o que estava aberto na minha
cabeça, e chamei isso de "a unidade de pauta é (LONGO x FAMÍLIA)" — que é
verdade, e não é licença para ficar num longo só.

**O risco não é estético.** O portão `similaridade` (<= 0,65 contra o mesmo
canal) existe por causa do conteúdo INAUTÊNTICO do YPP: *"the substance of each
video should be materially varied"*. Logo concentração de origem ataca
exatamente o portão que estamos tentando passar, e ela cresce devagar — por isso
precisa de contador, não de memória.

**E ELE RECOMENDAVA PAUTA QUE NÃO SE PODE ESCREVER — medido em 14/10 às 03:1x.**
Na rodada das 03:06 ele apontou `KRUERlNPzDw` e `StQNFMdpGdk` como "e e daqui que
a proxima peca deveria sair". As duas são do `labtreinamento`, as duas têm **sete
capítulos de TÍTULO** e nenhuma das duas tem spec local.

**RETRATAÇÃO DE 14/10 ÀS 15:2x, e é da frase que estava AQUI — aprendizado 761.**
Eu escrevia neste docstring que as duas têm *"nenhuma faixa de legenda da
máquina (medido pelo `capitulos.yml`, runs 38504585378 e 38504726301)"*. **Não
foi medido.** As anotações dos dois runs trazem só os **sete títulos** e a linha
`7 capitulos:` — eles rodaram **sem `legenda=true`**, logo mediram a DESCRIÇÃO e
eu concluí sobre a LEGENDA. É o §3.8 na forma mais crua: eu perguntei uma coisa
ao instrumento e li a resposta como se fosse de outra.

**E o oposto é que está medido.** Em 14/10 às 14:1x e 15:1x, pelo `pg_net`:

    captions?part=snippet&videoId=StQNFMdpGdk -> 200, faixa `standard`,
      download com tfmt=srt -> 200, 15.044 caracteres  (virou o -s049)
    captions?part=snippet&videoId=KRUERlNPzDw -> 200, faixa `standard`,
      download com tfmt=srt -> 200, 13.941 caracteres  (virou o -s050)

**As duas eram escrevíveis todo esse tempo**, e a frase falsa daqui é o que me
fez pulá-las por dias enquanto eu pegava sempre a banda de três usos. O
comportamento do módulo já estava certo — ele diz *"sem fonte LOCAL; confira a
legenda antes de descartar"* — e foi a minha nota que contradizia o próprio
código.
 Pela regra (h) o texto de um capítulo sai da **legenda**, nunca do título —
*"escrever a partir de título seria inventar conteúdo"*. Logo as duas origens que
ele recomendava eram **impossíveis de escrever**, e eu só descobri isso depois de
gastar dois runs.

**E A PRIMEIRA VERSÃO DESTE CONSERTO DEU FALSO NEGATIVO NA FROTA INTEIRA, dez
minutos depois de eu escrevê-la.** Ela procurava `longo_existente` nas specs de
LONGO — e spec de longo não declara isso, porque **ela é o longo**. Resultado:
`escrevivel` devolveu False para as treze origens, inclusive para as duas que eu
acabara de usar nas rodadas de 01:07 e 02:07. Eu quase relatei ao dono que o
canal não tinha pauta escrevível nenhuma. O vínculo origem→pacote mora na COPY do
short, e quem o resolve é o `segundo_angulo.pacote_do_id` — que já existia.

**A causa é a mesma classe do 743:** o módulo contava, e **não conferia se a
origem é ESCREVÍVEL**. Recomendador que aponta para pauta inviável é tão ruim
quanto detector que inventa achado. Agora `escrevivel()` confere se existe spec
local com capítulos, `analise` separa `usadas_uma_vez` em **`recomendadas`** e
**`sem_fonte_local`**, e o relato nomeia as duas listas com motivos diferentes.
**O que ele NÃO pode afirmar:** que origem sem spec local é inviável em definitivo
— ela pode ter legenda, e aí a rota é o `capitulos.yml` com `legenda=true`. Ele
diz "sem fonte LOCAL; confira a legenda antes de descartar".

**O que este módulo NÃO faz:** não reprova nada e não escolhe pauta. Ele conta e
diz onde a concentração está, com a lista das origens pouco usadas ao lado — que
é a informação que a rodada precisa para trocar. Limiar de ALERTA é observado e
declarado: o dobro da segunda origem mais usada, porque é a forma mais simples
de dizer "uma origem está carregando o canal" sem inventar número.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import sys

RAIZ = os.path.dirname(__file__)


def contagem(canal: str, raiz: str = None) -> dict[str, int]:
    """{origem: quantos shorts} para um canal, lendo `longo_existente`."""
    base = raiz or os.path.join(RAIZ, "specs")
    c: collections.Counter = collections.Counter()
    for f in glob.glob(os.path.join(base, f"{canal}-s*.json")):
        with open(f, encoding="utf-8") as fh:
            o = json.load(fh).get("longo_existente")
        if o:
            c[o] += 1
    return dict(c)


def escrevivel(origem: str, canal: str, raiz: str = None) -> bool:
    """A origem tem spec LOCAL com capítulos, isto é: dá para escrever hoje.

    Falso NÃO quer dizer inviável — quer dizer que o texto teria de vir da faixa
    de legenda pelo `capitulos.yml` (regra h). Foi a confusão de 14/10: duas
    origens recomendadas não tinham spec NEM legenda, e a descrição só dá título.
    """
    base = raiz or os.path.join(RAIZ, "specs")
    for f in glob.glob(os.path.join(base, f"{canal}-[0-9]*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if d.get("longo_existente") == origem and d.get("longo"):
            return True
    # A spec de LONGO nao declara `longo_existente` — ela E o longo. O vinculo
    # origem -> pacote mora na COPY do short, e quem o resolve e o
    # `segundo_angulo.pacote_do_id`. A primeira versao desta funcao procurava
    # `longo_existente` nas specs de longo e por isso devolveu False para a
    # frota INTEIRA, inclusive para as duas origens que eu acabara de usar nas
    # rodadas de 01:07 e 02:07. Falso negativo meu, achado por conferir.
    if raiz:                      # teste sintetico: nao ha copy para resolver
        return False
    try:
        import segundo_angulo
    except ImportError:            # pragma: no cover
        return False
    pacote = segundo_angulo.pacote_do_id(origem)
    if not pacote:
        return False
    return bool(segundo_angulo.capitulos_do_pacote(pacote))


def analise(contagens: dict[str, int], canal: str = None,
            raiz: str = None) -> dict:
    """Quem domina, por quanto, e quais origens estão pouco usadas.

    `dominante` é a origem mais usada. `alerta` é True quando ela tem mais que o
    DOBRO da segunda — limiar observado, não importado: com uma origem no dobro
    da seguinte, a variedade do canal passa a depender de um texto só.
    """
    if not contagens:
        return {"total_shorts": 0, "origens": 0, "dominante": None,
                "alerta": False, "motivo": "nenhum short com origem declarada"}
    ordem = sorted(contagens.items(), key=lambda kv: (-kv[1], kv[0]))
    top, n_top = ordem[0]
    n_seg = ordem[1][1] if len(ordem) > 1 else 0
    total = sum(contagens.values())
    uma_vez = sorted(o for o, n in contagens.items() if n == 1)
    # 14/10: separar o que da para escrever HOJE do que precisaria de legenda.
    if canal:
        recomendadas = [o for o in uma_vez if escrevivel(o, canal, raiz)]
        sem_fonte = [o for o in uma_vez if o not in recomendadas]
    else:
        recomendadas, sem_fonte = uma_vez, []
    return {
        "total_shorts": total,
        "origens": len(contagens),
        "dominante": top,
        "n_dominante": n_top,
        "n_segunda": n_seg,
        "fracao_dominante": round(n_top / total, 3),
        "usadas_uma_vez": uma_vez,
        "recomendadas": recomendadas,
        "sem_fonte_local": sem_fonte,
        "alerta": n_top > 2 * n_seg,
        "motivo": (f"{top} carrega {n_top} de {total} shorts, mais que o dobro "
                   f"da segunda ({n_seg}). O portao `similaridade` e de "
                   f"MONETIZACAO, e concentracao de origem ataca ele."
                   if n_top > 2 * n_seg else
                   f"{top} lidera com {n_top}, contra {n_seg} da segunda — "
                   "dentro do dobro."),
    }


def relato(canal: str, raiz: str = None) -> str:
    c = contagem(canal, raiz)
    a = analise(c, canal, raiz)
    if not a["total_shorts"]:
        return f"PAUTA de {canal}: {a['motivo']}"
    linhas = [f"PAUTA de {canal}: {a['total_shorts']} shorts sobre "
              f"{a['origens']} origens.",
              f"  dominante {a['dominante']} com {a['n_dominante']} "
              f"({a['fracao_dominante']*100:.0f}%), segunda com {a['n_segunda']}."]
    if a["alerta"]:
        linhas.append("  >> ALERTA: " + a["motivo"])
    if a["recomendadas"]:
        linhas.append(f"  origens usadas UMA vez e ESCREVIVEIS hoje "
                      f"({len(a['recomendadas'])}), e e daqui que a proxima "
                      "peca deveria sair: " + ", ".join(a["recomendadas"]))
    if a["sem_fonte_local"]:
        linhas.append(f"  usadas UMA vez mas SEM SPEC LOCAL "
                      f"({len(a['sem_fonte_local'])}): "
                      + ", ".join(a["sem_fonte_local"])
                      + " — a descricao da so o TITULO do capitulo (regra h); "
                      "confira a LEGENDA pelo capitulos.yml antes de descartar, "
                      "e nao escreva a partir de titulo.")
    if not a["recomendadas"] and not a["sem_fonte_local"]:
        linhas.append("  nenhuma origem usada UMA vez: a unidade de pauta e "
                      "(LONGO x FAMILIA), entao pegue a origem de MENOR "
                      "contagem com capitulos intocados.")
    linhas.append("  (isto CONTA, nao reprova: a escolha de origem segue a "
                  "regra (a) da rotina e a consulta de estoque.)")
    return "\n".join(linhas)


def main() -> int:
    canais = sys.argv[1:] or ["labtreinamento", "epomeno-epipedo",
                              "kolejny-poziom"]
    for c in canais:
        print(relato(c))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
