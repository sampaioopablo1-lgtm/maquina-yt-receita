# Doze pacotes por dia: o que trava, o que não trava

Escrito em 26/08/2026, medido e não estimado.

## 1. Hoje são ONZE canais possíveis, não doze

| canal | pode publicar hoje? | o que falta |
|---|---|---|
| epomeno-epipedo, kolejny-poziom, seviye-seviye, setiap-level, nivel-do-jogo, next-level-money, game-money-lab, resep-naik-level, labtreinamento, agla-level, seja-mais-magra | **sim** (11) | — |
| sx-educacao | **não** | token morto (`invalid_grant`) — reautorizar |
| cocina-por-niveles | **não** | o canal não existe no YouTube — criar |

Doze por dia é aritmeticamente impossível até esses dois voltarem. O teto por
canal já está certo: `orquestra.MAX_POR_DIA_POR_CANAL = 1`, e 12 canais × 1 = 12.

## 2. A cota do YouTube CABE — e meu número anterior estava errado

O custo por pacote, contando só as chamadas que o `publicar.py` faz de verdade:

    longo    videos.insert 1600 + thumbnails.set 50 + captions.insert 400  = 2.050
    short    videos.insert 1600 + thumbnails.set 50                        = 1.650
    apontar  videos.list 1 + videos.update 50                              =    51
    ---------------------------------------------------------------------------
    PACOTE                                                                 = 3.751

`playlistItems.insert` **não custa nada hoje**: `--playlist` é `None` por padrão
e nenhum `config/canais/*.yaml` define uma, então `na_playlist` devolve "sem
playlist" sem chamar a API. Eu tinha somado 100 por pacote que não existem.

    12 pacotes/dia = 45.012 unidades

**Teto observado: ≥52.514.** Em 20/08 saíram 14 pacotes num dia só, todos com
sucesso. Então 12/dia cabe, com ~7.500 de folga.

**A folga é exatamente do tamanho do trabalho de reparo.** Em 25/08 os 9
pacotes (33.759) mais os reparos do dia — 35 tags repostas (1.750) e ~90
créditos CC-BY (4.500) — estouraram a cota às 20h25. Daí a regra:

> Em dia de 12 pacotes, **nenhum reparo em lote**. Backfill de CC-BY, reposição
> de tags e limpeza de duplicatas ficam para os dias de cadência menor.

Se um dia precisar de mais folga, o corte disponível é `captions.insert`:
400 × 12 = **4.800/dia**. Custo: o longo passa a depender da legenda automática
do YouTube em vez do `.srt` renderizado. É decisão de qualidade, não técnica.

## 3. O render NÃO trava

`frota.yml` recebe um ARRAY de pacotes e abre um job por canal, sem
`max-parallel`. Doze pacotes rendem em paralelo: ~13 min de relógio, não 12×13.
Um disparo só:

```
pacotes: [{"canal":"a","pacote":"a-013","idioma":"el"}, ... 12 itens ...]
publicar: true
```

## 4. O que trava de verdade: ESCREVER as doze specs

Essa é a única etapa sem automação, e não por acidente. O `autoria.yml` existe e
faz exatamente esse trabalho, mas o cron foi **desligado em 24/08 por decisão do
dono**: *"Eu não tenho ANTHROPIC_API_KEY, que não precise no processo."* Eram 54
falhas em 55 execuções, todas no mesmo passo.

Então quem escreve é a rotina horária, à mão. Medido na noite de 25→26/08:

    5 specs em 9 rodadas  =  1 spec a cada ~1,8 rodada

A 24 rodadas por dia isso dá ~13 specs/dia — **12/dia cabe**, mas consome
metade das rodadas e deixa a outra metade para tudo o mais.

O tempo por spec se reparte assim, medido:

| etapa | tempo | dá para acelerar? |
|---|---|---|
| pesquisa + duas fontes institucionais | ~15 min | **não** — é onde a qualidade mora |
| escrever a narração | ~15 min | não |
| **dimensionar (medir, acrescentar cena, remedir)** | **~10 min** | **sim, e foi feito** |
| commit + render + conferir | ~5 min | parcialmente (render em lote) |

O `fabrica/dimensiona.py` ataca a terceira linha: numa passada ele diz o déficit
em segundos **por capítulo** e no total, e quantas cenas isso significa naquela
voz. Três voltas viram uma.

## 5. E a publicação, hoje, é manual

Com o Supabase em 402 o `diario.yml` (Ciclo) não roda: ele lê o estado por
PostgREST. Publicar é o modo ponte, à mão, um pacote por vez — ver
`publicar-na-virada-da-cota.md`.

**Enquanto o 402 não cair, 12/dia significa 12 publicações manuais.** Isso não
escala e é o segundo item da lista do dono, junto com os dois canais.

## 6. Ordem de ataque, do que mais destrava para o que menos

1. **Reautorizar sx-educacao e criar cocina-por-niveles** — sem isso o número 12
   não existe.
2. **Supabase Pro (ou esperar a virada do ciclo)** — devolve o Ciclo automático
   e tira as 12 publicações manuais do caminho.
3. **`youtube.com/verify`** em agla-level, seviye-seviye, resep-naik-level e
   game-money-lab — hoje o `thumbnails.set` desses quatro devolve 403 e a
   unidade é gasta do mesmo jeito.
4. **Decidir sobre a `ANTHROPIC_API_KEY`** — é o que religa o `autoria.yml` e
   tira a escrita das minhas rodadas. Sem ela, 12/dia é possível mas ocupa
   metade da capacidade da rotina.

## 7. Uma ressalva que o dado obriga

O aprendizado 507 mede que as 4.000 horas do YPP **não fecham publicando mais**:
ao ritmo atual seriam 3.516 longos. Elas fecham quando o longo sai de 40 para
centenas de views, e isso vem de ter inscritos.

Doze por dia continua valendo — mais shorts é mais chance de converter — **desde
que a forma continue certa** (aprendizado 504: dinheiro do espectador, escolha
dele, e a conta). Doze pacotes na forma errada produzem doze vezes zero, e é
literalmente o que os cinco canais mediram: em cinco canais seguidos o short
mais visto converteu zero.
