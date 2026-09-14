# Regra de corte e religamento — janela de 48 horas

*Criada em 09/09/2026. Vale para qualquer campanha da conta 1695865631502778.*
*Coluna "onde a conta está" atualizada em 14/09/2026 — medida nos 2 conjuntos ativos.*

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
| CTR (link) | 0,90% a 1,60% | **0,50%** | **2,30% e 2,88%** — acima do mercado (medido 14/09) |
| CPM | R$ 15 a R$ 35 | **R$ 60** | **R$ 27,96 e R$ 28,77** — dentro da faixa (medido 14/09) |
| Custo por lead B2B | R$ 25 a R$ 80 | **R$ 150** | **R$ 7,19 e R$ 5,49** — muito abaixo do mercado, mas subindo (medido 14/09) |

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

### 14/09/2026, 12h11 — segunda rodada. **Zero cortes.**

Esta era a rodada que ia julgar os 5 conjuntos de nicho pelo dado, porque eles passaram
das 48 horas. Não julgou, e o motivo não é a regra: **os 5 já estavam pausados** quando a
rodada rodou. A conta foi enxugada antes, na noite de 12/09, e o log de atividade mostra
quem fez: **o próprio Pablo**, pelo Power Editor, às 21h16 e 21h17 de 12/09 — pausou
`INT I DONOS`, `WPP I INTERESSE DONOS DE EMPRESA`, `WPP I PERSONALIZADO LISTAS + ENGAJAMENTO`
e `WPP I SEMELHANTE CNAE RJ`.

Sobraram **2 conjuntos ativos**, os dois na campanha de lead, e é neles que está o dinheiro.

**Nível conjunto — os 2 elegíveis, nenhum bateu.**

| Conjunto | Idade | Impressões | Alcance | Lead | CPL | CTR | CPM | Veredito |
|---|---|---|---|---|---|---|---|---|
| LEADS I INTERESSE I FASE 3 | ~115h | 3.341 | 2.375 | **13** | **R$ 7,19** | 2,30% | R$ 27,96 | **C1 não bate** (tem lead) · **C2 não bate** (alcance 2.375) · C3 não bate |
| LEADS I PERSONALIZADO CNAE RJ I FASE 3 | ~115h | 1.145 | 876 | **6** | **R$ 5,49** | 2,88% | R$ 28,77 | idem |

**Nível anúncio — nenhum entrou na análise, de novo.** Os 10 anúncios ativos (V11 a V15,
cinco em cada conjunto) foram criados em 12/09 entre 20h21 e 21h14. Na hora da rodada tinham
**39 a 40 horas**. Falta pouco, mas falta: a trava 6 proíbe cortar antes das 48h. Eles ficam
julgáveis a partir da noite de **14/09**.

**19 leads no total, a R$ 7,19 e R$ 5,49.** O piso de mercado é R$ 25. O conjunto que aponta
para as listas personalizadas é o mais barato dos dois — foi a mudança certa.

**Alerta de vigilância:** o CPL do `INTERESSE` está em **R$ 7,19**, contra R$ 4,39 medido em
12/09. Subiu, e o teto combinado com o Pablo é **R$ 8,00**. Ainda está abaixo, mas encostou.
Se fechar um dia acima de R$ 8,00, avisar; dois dias seguidos acima, reverter as mudanças
da madrugada de 12/09.

**Fora das regras de corte, mas achado da rodada:** a conta entrou em **"In grace period"**
às 6h20 de 13/09 por falta de saldo e só voltou a **"Active"** às 12h54, depois de um PIX de
R$ 200. Foram cerca de **6 horas e meia** de conta em pendência de pagamento. Já está
resolvido e nenhuma ação é necessária — fica registrado porque explica qualquer buraco de
entrega na manhã de 13/09.

**Erros de entrega: `[]`.** A limpeza de 12/09 segurou — a conta continua sem erro crônico,
então o próximo erro de verdade vai aparecer sozinho.
