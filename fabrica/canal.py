"""De que CANAL e uma spec. Um dono so, e ele existe porque eram TRES.

MEDIDO em 19/10 as 05:2x e as 05:3x, na mesma rodada:

  * `mira.confere` lia `spec["slug"]` como se fosse o canal — e desde a `s077`
    o slug e o PACOTE, logo ele nunca mais achou o canal no `ALVO_POR_CANAL` e
    passou a dizer `tem_mira: False`, isto e, **parou de conferir a mira e
    declarou que nao havia mira a conferir**. Seis pecas publicadas assim;
  * `mira.tally_fora_da_mira`, escrito depois, derivava CERTO com
    `pacote.rsplit("-s", 1)[0]`;
  * `registro_videos.linhas_dos_notices` lia `spec["slug"]` para a coluna
    `canal` de `videos` — e as SETE linhas parqueadas da `s077` a `s083`
    sairam com `canal = 'labtreinamento-s0NN'`. Nao chegaram ao banco porque o
    `execute_sql` esta negado, o que e sorte e nao metodo: com elas dentro, a
    coluna que o `concentracao_frota` e a `estoque.sql` agrupam ficaria cega.

**A assinatura e a mesma do `assert 20 <= ds <= 60` do `etapas.py` e a da
legenda congelada do short solto: donos demais para a mesma regra, um
atualizado.** O remedio nao e consertar os dois lugares — e haver UM.
"""


import re

# A QUARTA forma apareceu em 19/10 as 12:5x, e o modo de falha foi o MESMO.
# Escrevendo o `epomeno-epipedo-068` — o primeiro PACOTE em muitas rodadas —, o
# `mira.relato` saiu com `canal 'epomeno-epipedo-068' nao tem ALVO_POR_CANAL
# medido`. A regra antiga cortava so o sufixo de SHORT SOLTO (`-sNNN`) e o
# pacote usa `-NNN`, logo o canal de todo longo voltava inteiro e o instrumento
# parava de conferir sem reprovar nada — a falha PERMISSIVA de 05:2x, na forma
# que ela toma no formato que o dono mandou construir.
#
# Aqui o canal `epomeno-epipedo` nao tem mira propria, logo o efeito foi so a
# mensagem errada; num pacote de `labtreinamento`, que TEM mira desde 09/10, o
# instrumento ficaria cego exatamente como nas seis pecas da `s077` a `s082`.
#
# A FORMA DO SUFIXO E MEDIDA, nao suposta: varridos os 347 nomes de spec do
# disco, 215 sao `<canal>-sNNN`, 131 sao `<canal>-NNN` e 8 sao o canal nu. Os
# **catorze** prefixos distintos terminam todos em letra, logo cortar um grupo
# final de digitos nunca encosta no nome de um canal.
#
# O LIMITE VAI DECLARADO: um nome de canal que terminasse em digito seria
# cortado errado (`kp-plan-9233` -> `kp-plan`). Nenhum dos catorze e assim, e
# `kp-plan-9233-20260811` — que e PACOTE e aparece no docstring do
# `kolejny-poziom-s017` — resolve certo. Ha teste cobrando os dois casos.
_SUFIXO = re.compile(r"-s?\d+$")

# E A QUINTA FORMA SAI DO PARQUE, nao do disco — medida em 23/10 as 17:0x, pelo
# `familia_entre_canais`. Quando a peca e de PACOTE, o `registro_videos` grava
# `slug = pacote + "-short"` e o parque de duracao grava `<pacote>-longo`, logo
# existem nomes que o disco NAO tem: as TRES linhas de longo de 19/10 (3 de 163)
# resolviam para si mesmas e viravam canal FANTASMA. Medido antes de mexer:
# **zero** dos 454 nomes de spec do disco termina nestes dois sufixos e nenhum
# dos catorze prefixos de canal termina assim, logo cortar e seguro. O corte e
# ANTES do grupo de digitos, e o grupo de digitos segue sendo cortado UMA vez:
# iterar os dois mudaria `kp-plan-9233-20260811` de `kp-plan-9233` para
# `kp-plan`, que e comportamento que ja tem teste desde 19/10.
_PAPEL = re.compile(r"-(?:longo|short)$")


def do_pacote(pacote: str) -> str:
    """`labtreinamento-s083`, `epomeno-epipedo-068` e `...-068-longo` -> o canal."""
    return _SUFIXO.sub("", _PAPEL.sub("", str(pacote or "")))


def da_spec(spec: dict) -> str:
    """O canal de uma spec, nas TRES convencoes de `slug`.

    O `pacote` vem primeiro porque ele sempre foi o pacote; o `slug` entra como
    reserva, e era o canal nas specs antigas.
    """
    return do_pacote(spec.get("pacote") or spec.get("slug") or "")
