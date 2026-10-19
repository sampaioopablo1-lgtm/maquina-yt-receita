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


def do_pacote(pacote: str) -> str:
    """`labtreinamento-s083` -> `labtreinamento`; `labtreinamento` -> igual."""
    base = str(pacote or "")
    return base.rsplit("-s", 1)[0] if "-s" in base else base


def da_spec(spec: dict) -> str:
    """O canal de uma spec, nas DUAS convencoes de `slug`.

    O `pacote` vem primeiro porque ele sempre foi o pacote; o `slug` entra como
    reserva, e era o canal nas specs antigas.
    """
    return do_pacote(spec.get("pacote") or spec.get("slug") or "")
