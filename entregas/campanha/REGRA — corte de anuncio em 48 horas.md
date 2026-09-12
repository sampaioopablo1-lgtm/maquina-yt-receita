# Regra de corte e religamento — janela de 48 horas

*Criada em 09/09/2026. Vale para qualquer campanha da conta 1695865631502778.*
*Coluna "onde a conta está" atualizada em 12/09/2026 — os números de 09/09 ficaram obsoletos.*

## Por que 48 horas e não 24, nem 7 dias

O Meta leva de 24 a 48 horas para sair da fase de aprendizado inicial. Antes disso o número é
ruído: o leilão ainda está calibrando quem vê o anúncio. Depois de 7 dias, já foi dinheiro
demais em anúncio morto.

**48 horas é o ponto onde o dado já é dado e o prejuízo ainda é pequeno.**

Mas tempo sozinho não basta. Um anúncio de 48 horas com 80 impressões não tem o que ser julgado.
Por isso toda regra abaixo exige **tempo E volume**.

## Referência de mercado (geração de lead, Brasil, 2026)

| Métrica | Mercado | Piso aceitável | Onde a conta está hoje |
|---|---|---|---|
| CTR (link) | 0,90% a 1,60% | **0,50%** | **2,95% e 3,64%** — acima do mercado (medido 12/09) |
| CPM | R$ 15 a R$ 35 | **R$ 60** | **R$ 29,32 e R$ 29,62** — dentro da faixa (medido 12/09) |
| Custo por lead B2B | R$ 25 a R$ 80 | **R$ 150** | **R$ 4,39 e R$ 4,82** — muito abaixo do mercado (medido 12/09) |

## As regras de corte

Rodam uma vez por dia. Um anúncio ou conjunto só é pausado se bater **tempo, volume e defeito**
ao mesmo tempo.

### Nível anúncio

| # | Condição | Ação |
|---|---|---|
| A1 | ≥ 48h no ar **e** ≥ 1.000 impressões **e** 0 lead **e** CTR < 0,50% | pausar |
| A2 | ≥ 48h no ar **e** ≥ 500 impressões **e** CTR < 0,30% | pausar — está morto, não precisa esperar mais |
| A3 | ≥ 48h no ar **e** ≥ 500 impressões **e** 0 clique | pausar |
| A4 | já existe lead no conjunto **e** o custo por lead deste anúncio é > 3× o do melhor anúncio (o melhor com no mínimo 3 leads) | pausar |

### Nível conjunto

| # | Condição | Ação |
|---|---|---|
| C1 | ≥ 48h no ar **e** ≥ 2.000 impressões **e** 0 lead **e** CPM > R$ 60 | pausar o conjunto |
| C2 | ≥ 72h no ar **e** alcance total < 500 pessoas | pausar — público pequeno demais para leiloar |
| C3 | todos os anúncios do conjunto foram pausados pelas regras acima | pausar o conjunto |

## As travas — o que a regra NUNCA faz

1. **Nunca mexe em orçamento.** Nem sobe, nem desce, nem tira teto. Isso é decisão do Pablo.
2. **Nunca pausa nada que gerou lead nas últimas 48 horas**, por pior que esteja o CTR.
3. **Nunca deixa um conjunto com menos de 2 anúncios ativos.** Se o corte esvaziaria o conjunto,
   pausa só os piores e mantém os 2 melhores rodando até haver substituto.
4. **Nunca pausa o último conjunto ativo de uma campanha.** Campanha zerada não volta do zero de
   graça — perde o aprendizado inteiro.
5. **Nunca apaga.** Só pausa e renomeia com prefixo `ZZ`. O que está pausado guarda histórico e
   pode voltar.
6. **Nunca corta antes das 48h**, mesmo que o número esteja horrível. Único caso de corte
   imediato: erro de entrega que impede o anúncio de rodar (aí é conserto, não corte).

## Religar

Um anúncio pausado volta quando:
- o motivo do corte foi corrigido (criativo novo, público novo, erro de entrega resolvido) — aí
  não é religar, é **anúncio novo**; ou
- ele foi cortado por CPM alto num conjunto que depois foi corrigido, e há orçamento sobrando
  no conjunto (o CBO decide sozinho para onde vai).

**Religar o mesmo anúncio com o mesmo público raramente funciona.** O padrão é substituir.

## Como o corte é registrado

Toda pausa vira uma linha aqui embaixo, com data, o que foi pausado, o número que motivou e o
que entrou no lugar. Sem isso a regra vira faxina cega.

## Histórico de cortes

### 12/09/2026, 12h — primeira rodada. **Zero cortes.**

Medidos os 30 anúncios ativos e os 7 conjuntos ativos, `last_7d`.

**Nível anúncio — nenhum entrou na análise.** Os 30 foram criados em 11/09 entre 17h31 e
20h58; na hora da rodada tinham entre **12 e 15 horas de vida**. O PASSO 1 manda descartar
tudo abaixo de 48h, e a trava 6 proíbe cortar antes disso "mesmo que o número esteja
horrível". Vários estão com zero impressão, o que sem o corte de tempo pareceria caso de
A3 — e seria erro, porque anúncio de 12 horas ainda não teve chance.

**Nível conjunto — dois elegíveis, nenhum bateu.**

| Conjunto | Idade | Impressões | Alcance | Lead | Veredito |
|---|---|---|---|---|---|
| LEADS I INTERESSE I FASE 3 | ~64h | 1.151 | 953 | 7 | **C1 não bate** (exige ≥2.000 impressões e 0 lead) · **C2 não bate** (exige ≥72h e alcance <500) |
| LEADS I SEMELHANTE CNAE RJ I FASE 3 | ~64h | 741 | 624 | 5 | idem |

Os 5 conjuntos de nicho têm ~14 horas — fora da janela.

**Nenhuma trava impediu corte algum.** As regras simplesmente não dispararam: a conta é nova
demais para ter anúncio maduro e ruim.

### O que a medição revelou, e é a notícia da rodada

Os números da tabela de referência lá em cima, medidos em 09/09, ficaram **obsoletos**:

| | 09/09 | 12/09 |
|---|---|---|
| CTR | 0,41% a 0,74% (abaixo do mercado) | **2,95% e 3,64%** (acima do mercado) |
| CPM | R$ 90 no fundo (muito acima) | **R$ 29,32 e R$ 29,62** (dentro da faixa) |
| Custo por lead | sem lead | **R$ 4,39 e R$ 4,82** (mercado é R$ 25 a R$ 80) |

O CTR multiplicou por cerca de cinco e o CPM caiu pela metade. O custo por lead está
**cinco vezes abaixo do piso de mercado**. A tabela foi atualizada no topo do arquivo para
que a próxima rodada não compare com número velho.

**Ressalva honesta:** isso é de 09 a 11/09, ou seja, **antes** das mudanças da madrugada de
12/09 (segmentação dos nichos corrigida, copy de mentoria removida, 18 vídeos pausados, 6
peças novas). O efeito dessas mudanças só aparece no fechamento de 12/09.
