# 211 contra 0 na mesma idade: a medida que parou a maquina de publicar

Escrito em 08/10/2026 11:15, na rodada que entregou ZERO video de proposito.

## O numero

Onze videos publicados em 08/10 nos tres canais, com a hora de publicacao, a
idade e as views da ultima coleta:

| canal | # no dia | publicado | idade | views |
|---|---|---|---|---|
| epomeno | 1 | 00:19 | 10,9 h | 121 |
| epomeno | 2 | 01:47 | 9,4 h | 208 |
| epomeno | 3 | 02:17 | 8,9 h | 259 |
| epomeno | 4 | 07:19 | 3,9 h | **0** |
| epomeno | 5 | 10:18 | 0,9 h | **0** |
| kolejny | 1 | 03:15 | 7,9 h | 33 |
| kolejny | 2 | 04:15 | 6,9 h | 17 |
| kolejny | 3 | 05:20 | 5,9 h | 7 |
| kolejny | 4 | 06:23 | 4,8 h | 4 |
| labtreinamento | 1 | 08:18 | 2,9 h | 0 |
| labtreinamento | 2 | 09:18 | 1,9 h | 0 |

## A unica comparacao que sobrevive aos confundidores

Quase tudo nessa tabela esta confundido: as pecas mais recentes sao mais jovens,
e os canais tem alcance muito diferente entre si. Uma comparacao escapa, e e
dentro do MESMO canal e na MESMA idade:

    epomeno-s005  publicado 02:17   com 3,9 h de vida:  211 views
    epomeno-s006  publicado 07:19   com 3,9 h de vida:    0 views

Mesmo canal, mesmo formato, mesma duracao de ~34 s, cinco cenas `titulo` nos
dois, b-roll zero nos dois. A serie inicial do s005 foi 8, 8, 130, 211 — ele deu
o degrau de liberacao do aprendizado 653 as 2,9 h. O s006 nao deu.

## O que NAO explica

- **Idade:** a comparacao e na mesma idade.
- **Canal:** e o mesmo canal.
- **Angulo:** o s006 e terceiro angulo, mas o kolejny-s004, s005 e s006 sao
  PRIMEIROS angulos de longos diferentes e tambem estao em um digito.
- **Oscilacao do contador (650):** ela move dezenas, nao a diferenca entre 0 e
  211.

## As duas causas candidatas, e nao sei qual e

1. **Hora de publicacao.** Tudo que saiu entre 00:19 e 02:17 recebeu rajada;
   nada que saiu das 03:15 em diante recebeu. 03:15 UTC e madrugada no Brasil e
   manha cedo na Grecia e na Polonia.
2. **Ordem no dia / saturacao por canal.** O s006 foi a QUARTA peca do epomeno
   no dia. O aprendizado 606 ja dizia que o teto de producao e por canal; isto
   seria a primeira medida de um custo marginal real.

As duas estao CORRELACIONADAS no desenho atual, porque a rotina e horaria e
publica em sequencia. Foi o meu proprio desenho que criou a ambiguidade.

## Por que isso parou a rodada

A projecao da Porta 1 supoe que TODA peca recebe a rajada mediana (~420), o que
dava ~794 mil views em 90 dias contra os 3 milhoes exigidos. Se apenas as duas ou
tres primeiras pecas do dia por canal recebem rajada, a 21 videos/dia o numero
cai para a ordem de 200 mil. A pergunta "quantos videos por dia" deixa de ter
resposta obvia.

Publicar a sexta peca do epomeno nesta rodada seria exatamente o que esta sob
suspeita, e sujaria a medida. Entao a rodada das 11:09 entregou ZERO video, de
proposito, e o motivo esta aqui. Enquanto o experimento `hora-x-ordem-no-dia`
estiver aberto, o limite pratico passa a ser **tres pecas por canal por dia,
espacadas** — nao por falta de pauta (ha 42 longos de origem virgens, ver 652 e
655), mas para que a leitura seja possivel.

## O desenho do experimento

Num dia, publicar a PRIMEIRA peca do canal DEPOIS das 03:00 UTC.

- Se ela receber rajada, a causa nao e a hora e passa a ser a ordem no dia.
- Se nao receber, a hora fica como candidata principal, e o teste seguinte e
  publicar a QUARTA peca do dia em horario de madrugada.

Mede-se pelo DEGRAU do 653 as ~4 h de vida — a peca saltou de um digito para
dezenas, sim ou nao — dentro do mesmo canal e na mesma faixa de idade, nunca por
views absolutas entre canais. Precisa de dois dias intacto, uma peca por celula
por dia.

## O que resolveria isso em uma tarde

`yt-analytics.readonly`. Com retencao e impressoes por peca, a diferenca entre
"nao foi empurrada" e "foi empurrada e ninguem ficou" aparece direto, e nao
preciso de dois dias de A/B as cegas. E a pendencia numero um do dono, e esta e
a terceira vez que ela aparece como pre-condicao e nao como melhoria.
