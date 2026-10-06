# As 46 duplicatas, com o custo de apagar cada uma medido

Medido em 06/10/2026 sobre `videos` x `metricas`, com a ULTIMA leitura lifetime
por video (aprendizado 592 — nunca `max(views)`).

## O que existe

Onze grupos de `(canal, formato, titulo)` tem mais de uma copia publicada. São
57 linhas no total: **11 ficam** (a copia de cada grupo com MAIS views) e
**46 saem**. Uma das 46 nem tem video no YouTube (`nivel-do-jogo-002`, com
`youtube_id` nulo) — essa e linha de banco, nao upload.

| grupo | canal | formato | copias |
|---|---|---|---|
| 1 | kolejny-poziom | longo | 6 |
| 2 | kolejny-poziom | shorts | 5 |
| 3 | next-level-money | longo | 6 |
| 4 | next-level-money | shorts | 5 |
| 5 | nivel-do-jogo | longo | 6 (uma sem video) |
| 6 | nivel-do-jogo | shorts | 5 |
| 7 | resep-naik-level | longo | 5 |
| 8 | seviye-seviye | longo | 5 |
| 9 | seviye-seviye | shorts | 4 |
| 10 | sx-educacao | longo | 5 |
| 11 | sx-educacao | shorts | 5 |

Todas sao de 13 a 17 de agosto de 2026 — a janela em que o cron republicava o
mesmo pacote todo dia. O `sx-educacao` e o caso extremo: as cinco copias de
cada formato tem o MESMO `pacote` (`sx-educacao-001`).

## O custo de apagar, que eu precisava medir antes de recomendar

Apagar video no YouTube apaga a hora de exibicao dele. Como a meta e o YPP, era
preciso saber quanto isso custa antes de chamar a limpeza de "lixo de catalogo".
Medido:

| o que sai | videos | views somadas | duracao media |
|---|---|---|---|
| longos | 27 | **211** | 829 s |
| shorts | 19 | **2.573** | 42 s |

**O custo e desprezivel, e por isso a limpeza pode ir.** Os 27 longos somam 211
views; mesmo supondo retencao generosa de 40%, sao cerca de **19 horas** de
exibicao contra as **4.000** que o YPP pede — menos de meio por cento. E as
2.573 views de short contam para o portao de 10 milhoes em 90 dias: sao
**0,026%** dele, e sao views de agosto, que ja estao saindo de qualquer janela
de 90 dias.

## Por que apagar, entao

Nao e pela hora de exibicao — e pela MEDICAO. O aprendizado 586 mostrou que as
quatro melhores posicoes do ranking de cruzamento eram o MESMO video do
seviye-seviye publicado quatro vezes, e o 594 mostrou que elas mexem o ranking
dos canais em sentidos opostos: o kolejny-poziom salta de 15,6% para 46,5%
quando as copias saem do denominador. Duplicata nao e so ruido: ela mente para
cima exatamente no topo do ranking, que e onde eu vou buscar o exemplo a copiar.

Enquanto elas nao saem, a contramedida esta na consulta e continua obrigatoria:
**deduplicar por `(canal, titulo)` antes de ranquear qualquer coisa.**

## A consulta que lista as 46, uma a uma

```sql
with ult as (
  select distinct on (youtube_id) youtube_id, views from metricas
  where duracao_media_s = 0 and retencao_media_pct = 0
  order by youtube_id, coletado_em desc
),
g as (select canal, formato, titulo from videos
      where youtube_id is not null and titulo is not null
      group by canal, formato, titulo having count(*) > 1),
d as (select v.canal, v.formato, v.titulo, v.pacote, v.youtube_id,
             v.publicado_em, coalesce(u.views, 0) views
      from videos v join g using (canal, formato, titulo)
      left join ult u on u.youtube_id = v.youtube_id),
r as (select *, row_number() over (partition by canal, formato, titulo
                                   order by views desc, publicado_em asc nulls last) rk
      from d)
select canal, formato, youtube_id, publicado_em::date, views,
       case when rk = 1 then 'FICA' else 'APAGAR' end acao
from r order by canal, formato, rk;
```

O criterio de quem FICA e **a copia com mais views**, nao a mais antiga. O 586
tinha usado a mais antiga, que serve para medir mas nao para decidir o que
apagar: entre duas copias iguais, a que acumulou mais exibicao e a que vale
manter.

## O que eu NAO faco aqui

Apagar video e irreversivel e e no canal do dono. A lista existe para ele
apagar; eu nao apago. E a `sx-educacao` esta com token morto de qualquer forma.
