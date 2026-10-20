"""O nome de uma spec tem DUAS formas, e o parametro `exceto` as confundia.

MEDIDO em 20/10 as 11:3x, escrevendo o `labtreinamento-s092`. Cinco funcoes da
fabrica aceitam `exceto` — a peca da PROPRIA rodada, que ja esta no disco quando
eu pergunto — e elas se dividem em DUAS convencoes incompativeis:

| funcao | convencao |
|---|---|
| `concentracao.contagem` | **PACOTE** (`labtreinamento-s092`), porque ela monta `"%s.json" % exceto` |
| `pauta_do_momento.quadro/escolha/relato` | **PACOTE**, por delegar ao de cima |
| `esqueleto_entre_canais.novidade` | **ARQUIVO** (`labtreinamento-s092.json`) |
| `contagem_de_cenas.contagens_da_frota` | **ARQUIVO** |
| `variedade._especs_do_canal` | **ARQUIVO** |

**E errar a convencao falha em SILENCIO, nos DOIS sentidos.** Medido na peca
daquela rodada, com a MESMA string nas duas chamadas:

    EC.novidade(..., exceto='labtreinamento-s092')       -> forma_inedita=False, 1 exemplar
    EC.novidade(..., exceto='labtreinamento-s092.json')  -> forma_inedita=True,  0 exemplares
    CC.contagem(..., exceto='labtreinamento-s092')       -> KRUERlNPzDw = 5
    CC.contagem(..., exceto='labtreinamento-s092.json')  -> KRUERlNPzDw = 6

Isto e, a string CERTA para uma e a ERRADA para a outra — e as duas respondem as
duas perguntas da MESMA decisao da rodada (qual origem, qual esqueleto). Nenhuma
levanta: `exceto` que nao casa simplesmente nao filtra nada.

**O custo foi medido na rodada que produziu este modulo:** eu passei o PACOTE ao
`EC.novidade`, ele devolveu `forma_inedita: False` com `1 exemplar` para uma forma
que a frota NAO tem, e eu ia escrever isso na copy. So peguei porque fui conferir
a chave `arquivo` por outro motivo. **A falha e PERMISSIVA no sentido pior:** com
a spec no disco e o `exceto` errado, `forma_inedita` nao pode ser True nunca —
logo a unica pergunta que a funcao existe para responder no momento de escolher
fica respondida com NAO, sempre.

Este modulo e o UM dono da conversao e da comparacao. Ele NAO migra as
convencoes para uma so: as funcoes seguem documentando a sua, e o que muda e que
as duas formas passam a ser aceitas pelas cinco. Trocar a convencao de uma delas
mexeria em portao (`variedade`) por conveniencia de chamada, que e o avesso do
trabalho.
"""

import os

EXT = ".json"


def pacote(nome: str) -> str:
    """O nome SEM a extensao, dada qualquer das duas formas."""
    b = os.path.basename(nome or "")
    return b[: -len(EXT)] if b.endswith(EXT) else b


def arquivo(nome: str) -> str:
    """O nome COM a extensao, dada qualquer das duas formas."""
    p = pacote(nome)
    return p + EXT if p else ""


def casa(no_disco: str, exceto: str) -> bool:
    """A UNICA comparacao: o arquivo do disco e a peca que `exceto` nomeia?

    `exceto` vazio devolve False — nada e excluido —, porque e esse o valor
    padrao das cinco funcoes e trata-lo como casamento filtraria a frota
    inteira.
    """
    if not exceto or not no_disco:
        return False
    return arquivo(no_disco) == arquivo(exceto)


if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        print("%r -> pacote %r | arquivo %r" % (a, pacote(a), arquivo(a)))
