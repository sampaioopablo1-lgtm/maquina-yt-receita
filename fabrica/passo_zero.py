"""O passo zero da rodada numa chamada — com os tres donos DELEGADOS.

POR QUE ESTE MODULO EXISTE (19/10/2026, 23:3x). Nesta rodada eu chamei dois
instrumentos de tres e escrevi o terceiro a mao: a contagem da janela de cota
saiu de um laco Python descartavel sobre o `duracoes-a-medir.jsonl`, com o
corte `'2026-10-19T07:00:00Z'` **digitado**. E o `fabrica/janela_de_cota.py`
existe desde a manha de hoje, e o teste dele se chama
`test_contar_a_janela_de_cota_deixou_de_ser_de_cabeca`.

**E o defeito das 11:2x na SEGUNDA dimensao:** la foi a contagem de CANAL, cujo
instrumento (`concentracao_frota.escolha_do_momento`) eu reescrevi a mao cinco
rodadas seguidas; aqui foi a contagem de COTA. Nos dois casos o instrumento
existia e quem nao o chamou fui eu, o autor. A diferenca e que o custo deste
esta MEDIDO, e e grande:

| as 23:1x de 19/10 | as 00:07 de 20/10 |
|---|---|
| a mao: 19 envios, 30.400 unidades | a mao: **ZERO envios, 0 unidades** |
| instrumento: 19 envios, 30.400 | instrumento: **19 envios, 30.400** |

Entre 00:00 e 07:00 UTC a janela corrente abriu no dia ANTERIOR, logo o corte
com a data de hoje digitada conta um intervalo VAZIO e eu relataria *"a janela
esta livre"* com 30.400 unidades dentro dela. **E o 771 outra vez** — janela
errada, no sentido que apaga as ultimas horas — e a rodada seguinte a esta cai
exactamente nessa banda.

**ELE NAO REFAZ CONTA NENHUMA.** As tres respostas vem dos donos:

  * inscritos -> `leitura_de_inscritos.relato` (que delega o piso ao `porta1`);
  * canal     -> `concentracao_frota.escolha_do_momento`;
  * cota      -> `janela_de_cota.relato` (que deriva a abertura das 07:00 UTC).

Refazer qualquer uma delas aqui criaria o SEGUNDO dono — a assinatura que
congelou a legenda do short, parou a mira de conferir por seis pecas e pos job
inventado na serie. Ha teste por AST que reprova se este arquivo passar a
derivar corte de janela, ler o parque ou calcular piso de resolucao sozinho.

**ELE NAO REPROVA NADA** e o codigo de saida e sempre zero: ele informa o que
a rodada precisa saber antes de escolher pauta. Quem reprova peca e o
`prontidao`.
"""
import datetime
import sys


def _secoes(agora: datetime.datetime | None = None, janela_h: float = 24.0,
            modo_da_rota: str = None):
    """As tres secoes do passo zero, cada uma pedida ao seu dono.

    `modo_da_rota` e o modo MEDIDO da rota nesta rodada, do
    `vivacidade_publica.modo_de_fechamento`, e vai REPASSADO ao
    `leitura_de_inscritos` em vez de conferido aqui. Sem ele o relato DIZ que a
    rota nao foi sondada — e essa frase existe porque em 20/10 as 13:2x, na
    primeira rodada em que o criterio do 723 passou por TEMPO, este relato
    imprimiu tres SIM e calou sobre a rota, que estava `negado_por_politica`.
    """
    agora = agora or datetime.datetime.now(datetime.timezone.utc)
    import concentracao_frota
    import janela_de_cota
    import leitura_de_inscritos

    escolha = concentracao_frota.escolha_do_momento(janela_h)
    return [
        ("INSCRITOS", leitura_de_inscritos.relato(
            agora.isoformat(), modo_da_rota=modo_da_rota)),
        ("CANAL", _linha_do_canal(escolha)),
        ("COTA", janela_de_cota.relato(agora)),
    ]


def _linha_do_canal(escolha: dict) -> str:
    """A escolha do canal em letra — o dicionario e do `concentracao_frota`."""
    c = escolha["contagem"]
    partes = ", ".join(f"{k} {v}" for k, v in c.items())
    linhas = [f"CANAL na janela de {escolha['janela_h']:.0f} h: {partes}.",
              f"  escolhido: **{escolha['escolhido']}**"]
    if escolha.get("houve_empate"):
        linhas.append("  houve EMPATE em %s — desempatado pelo que esta ha mais "
                      "tempo sem publicar." % ", ".join(escolha["empatados"]))
    linhas.append("  (isto CONTA e nao reprova: a pauta dentro do canal sai do "
                  "`concentracao.py`, pela regra (a).)")
    return "\n".join(linhas)


def relato(agora: datetime.datetime | None = None, janela_h: float = 24.0,
           modo_da_rota: str = None) -> str:
    blocos = [texto for _, texto in _secoes(agora, janela_h, modo_da_rota)]
    blocos.append(">> ISTO NAO REPROVA e nao escolhe pauta: ele responde as tres "
                  "perguntas do passo zero com os donos de cada uma. A peca "
                  "ainda passa pelo `antes_do_render.py` e pelo `prontidao`.")
    return "\n\n".join(blocos)


if __name__ == "__main__":
    # O primeiro argumento, quando vem, e o modo MEDIDO da rota nesta rodada.
    print(relato(modo_da_rota=(sys.argv[1] if len(sys.argv) > 1 else None)))
    sys.exit(0)
