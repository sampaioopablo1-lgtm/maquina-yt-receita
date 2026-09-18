# Regra de corte e religamento — janela de 48 horas

*Criada em 09/09/2026. Vale para qualquer campanha da conta 1695865631502778.*
*Coluna "onde a conta está" atualizada em 14/09/2026 — medida nos 2 conjuntos ativos.*
*Em 14/09/2026 o Pablo trocou o corte direto por uma escada de 4 tentativas. **Em 15/09/2026 ele
trocou de novo: a escada saiu, entrou a REGRA V3 — anúncio que não performa em 48h ganha criativo
novo (imagem/copy) com base nos dados. Ver a seção "REGRA V3".** A escada fica só como histórico.*

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
| A1 | ≥ 48h no ar **e** ≥ 1.000 impressões **e** 0 lead **e** CTR < 0,50% | **entra na escada** |
| A2 | ≥ 48h no ar **e** ≥ 500 impressões **e** CTR < 0,30% | **entra na escada** |
| A3 | ≥ 48h no ar **e** ≥ 500 impressões **e** 0 clique | **entra na escada** |
| A4 | já existe lead no conjunto **e** o custo por lead deste anúncio é > 3× o do melhor anúncio (o melhor com no mínimo 3 leads) | **entra na escada** |

**Bater uma regra A não pausa mais nada.** Desde 14/09/2026, por decisão do Pablo, bater A1–A4
apenas **abre a escada de tentativas** descrita na seção seguinte. O anúncio só é pausado no fim
dela, e só se nenhuma tentativa tiver melhorado.

### Nível conjunto

| # | Condição | Ação |
|---|---|---|
| **C0** | **≥ 48h desde o created_time do conjunto e 0 lead** | **pausar o conjunto** |
| C1 | ≥ 48h no ar **e** ≥ 2.000 impressões **e** 0 lead **e** CPM > R$ 60 | pausar o conjunto |
| C2 | ≥ 72h no ar **e** alcance total < 500 pessoas | pausar — público pequeno demais para leiloar |
| C3 | todos os anúncios do conjunto foram pausados pelas regras acima | pausar o conjunto |

### C0 — a regra dura de conjunto (decisão do Pablo, 17/09/2026)

*Palavra do Pablo: "a regra de desativar por falta de performance, crítica, também se aplica ao
conjunto de anúncios. Se em 48 horas, o conjunto não gerou leads, precisa ser desativado."*

**C0 vale acima de C1.** C1 exigia três coisas ao mesmo tempo (volume, zero lead e CPM alto) e por
isso quase nunca disparava — um conjunto podia queimar dias sem lead e nunca bater a condição.
C0 tira as muletas: **passou de 48 horas e não gerou lead, sai do ar.** C1, C2 e C3 continuam
existindo para os casos que C0 não pega (conjunto que gerou lead mas está caro, público pequeno
demais, conjunto esvaziado).

**Como medir, sem margem para interpretação:**
- O relógio é o `created_time` do CONJUNTO lido da Meta, nunca data escrita em prompt.
- "Lead" é o mesmo `results` que já usamos no nível anúncio (`actions:leadgen.other`), somado em
  todos os anúncios do conjunto, no período desde o created_time.
- Conjunto com menos de 48h não é julgado. Conjunto com exatamente 48h ou mais e zero lead é
  pausado na mesma rodada, sem pedir confirmação.
- Pausar = `ads_update_entity`, entity_type `ad_set`, status PAUSED, e renomear com o prefixo
  **"ZZ CORTADO 48H — "**. Não apagar nada. Os anúncios de dentro ficam como estão.
- Registrar na tabela "Trocas feitas" e no DIARIO, com o created_time que serviu de relógio e a
  contagem de leads que motivou o corte.

**ENTREGA ZERO conta como zero lead.** Um conjunto que não recebeu verba da CBO e ficou com 0
impressão em 48h é pausado igual. O raciocínio: numa campanha CBO a Meta distribui o orçamento
sozinha, e conjunto que ela escolheu não alimentar durante dois dias inteiros não vai alimentar
depois — ele só divide a atenção do algoritmo. Se o Pablo quiser testar aquele público de novo, o
caminho é conjunto novo com criativo novo, não esperar mais.

**O que C0 NÃO autoriza:** mexer em orçamento (segue proibido), pausar o último conjunto ativo de
uma campanha (segue proibido), e pausar conjunto que gerou lead nas últimas 48h (segue proibido).
Se C0 e uma trava se chocarem, **a trava vence** e a rodada avisa o Pablo em vez de pausar.

**Primeiro caso previsto:** LEADS I NICHO HARMONIZACAO BR I FASE 3 (120247470141000766), created
16/09 17h59, completa 48h em **18/09 por volta das 18h**. Até 17/09 14h tinha 5 impressões no total
e nenhum lead.

### TRAVA 7 — "não testado" não é o mesmo que "reprovado" (acrescentada 17/09/2026 21h33)

**C0 não corta conjunto que teve menos de 500 impressões nas 48 horas.** Abaixo disso o veredito é
**NÃO TESTADO**: a rodada não pausa, registra no DIARIO e avisa o Pablo em duas linhas.

Por quê. Na noite de 17/09 o Pablo baixou a verba da campanha de R$ 30 para R$ 20 por dia (log da
conta, 8h52, Power Editor), e no mesmo dia a conta passou de 3 para 6 conjuntos ativos. A verba por
conjunto caiu de R$ 10 para R$ 3,33 — e a CBO não reparte igual: no dia 17 o INTERESSE levou R$ 16,67
dos R$ 18,17 gastos, **92% de tudo**. Sobrou centavo para os outros cinco. O HARMONIZAÇÃO ficou 27
horas no ar e recebeu **5 impressões**.

Sem esta trava, a C0 mataria HARMONIZAÇÃO na sexta e IMOBILIÁRIA, ADVOCACIA e CONTABILIDADE no
sábado — quatro conjuntos em dois dias, nenhum deles reprovado por performance. Teriam sido
reprovados por não terem recebido verba para existir. Uma regra de corte que pune quem não recebeu
entrega não mede desempenho, mede a repartição da CBO.

O texto acima sobre "conjunto que a Meta escolheu não alimentar durante dois dias não vai alimentar
depois" continua verdadeiro **quando a campanha tem verba folgada**. Ele deixa de valer quando a
própria verba é o gargalo, e é exatamente esse o caso desde 17/09. Enquanto seis conjuntos
dividirem R$ 20 por dia, entrega baixa é sintoma da conta, não do público.

**500 impressões** é o mesmo piso que a C1 já usava para nível de anúncio (2.000) dividido pela
realidade desta conta: com CPM de R$ 30, 500 impressões custam R$ 15 — mais de meio dia de verba da
campanha inteira. Abaixo disso não há amostra para julgar nada.

## A escada de tentativas — o que vem antes de pausar

*Decidida pelo Pablo em 14/09/2026. Substitui o corte direto no nível anúncio.*

Anúncio ruim não é necessariamente anúncio morto: quase sempre é **uma peça errada** num conjunto
que funciona. Pausar direto joga fora o criativo inteiro sem saber qual peça era o problema. A
escada troca **uma variável por vez** e mede cada uma antes de condenar o anúncio.

### As rodadas

Quatro rodadas, **uma variável por rodada, nunca duas**. Trocar duas de uma vez e ver melhora não
ensina qual delas melhorou — e aí a próxima peça herda o erro.

| Rodada | O que muda | O que NÃO muda |
|---|---|---|
| 1 | **Título** (a chamada) | imagem, texto, botão, público |
| 2 | **Descrição** (o texto principal) | imagem, título vencedor da R1, botão, público |
| 3 | **Botão** (a chamada para ação) | imagem, título e texto vencedores, público |
| 4 | **Imagem / criativo** | título, texto e botão vencedores, público |

Cada rodada **parte do vencedor da anterior**, não do original. Se a R1 melhorou, a R2 roda em
cima do título novo. Se a R1 não melhorou, a R2 roda em cima do título original — o perdedor é
descartado, não acumulado.

### Quanto tempo e quanto volume

**Mínimo de 2 dias por rodada** — é a decisão do Pablo, e bate com a janela de aprendizado do Meta.

Mas tempo sozinho não basta, pela mesma razão que a regra de 48h já exige volume: **uma rodada só
recebe veredito com no mínimo 300 impressões.** Abaixo disso a diferença entre duas variações é
ruído, não resultado.

Com a conta de hoje — R$ 30/dia divididos entre 2 conjuntos e ~10 anúncios — cada anúncio recebe
cerca de **R$ 1 por dia**, ou perto de 40 impressões diárias. Nesse ritmo, 2 dias entregam ~80
impressões: **bem abaixo do piso.** Então, na prática:

- a rodada **estica** além dos 2 dias até juntar as 300 impressões;
- se passar de **7 dias** sem chegar lá, a rodada é declarada **inconclusiva por falta de entrega**
  e isso vira aviso ao Pablo — o problema não é o criativo, é que o anúncio não está recebendo
  verba suficiente para ser testado. Escada travada por fome de entrega não é escada.

### O que conta como "melhorou"

Compara-se **a mesma métrica que abriu a escada**, contra a rodada anterior:

| Entrou por | Métrica que decide | Melhorou se |
|---|---|---|
| A1, A2 | CTR | CTR sobe **pelo menos 20%** em relação à rodada anterior |
| A3 | cliques | passa a existir clique |
| A4 | custo por lead | CPL cai **pelo menos 20%** |

Os 20% existem para não comemorar oscilação. Melhora de 3% com 300 impressões é empate.

### O fim da escada

- **Alguma rodada melhorou** → o anúncio sai da escada e volta a ser anúncio normal, com a versão
  vencedora no ar. Se voltar a bater regra A no futuro, entra numa escada nova.
- **As quatro rodadas terminaram e nenhuma melhorou** → **aí sim pausar**, com o prefixo
  `ZZ CORTADO 48H — `, e registrar no histórico as quatro tentativas e o número de cada uma.
- **A escada é registrada mesmo quando dá certo.** Saber qual variável destravou o anúncio vale
  para todos os próximos — é a única forma de a escada ensinar alguma coisa em vez de só adiar
  decisão.

### Travas próprias da escada

1. **Uma variável por rodada.** Sem exceção. Duas mudanças juntas invalidam a rodada.
2. **Nunca mexer em orçamento para "dar chance" ao teste.** Se falta entrega, avisar o Pablo —
   a decisão de verba é dele.
3. **Nunca trocar o público no meio da escada.** Público é outra variável, e mudá-lo joga fora
   toda a comparação anterior.
4. **Editar criativo de anúncio ativo reinicia o aprendizado dele.** Isso é do Meta, não da regra.
   Por isso cada rodada **duplica o anúncio com a mudança** e pausa a versão anterior, em vez de
   editar por cima: assim a versão antiga fica guardada com o número dela, e dá para comparar.
   O nome ganha sufixo `— R1 titulo`, `— R2 descricao`, `— R3 botao`, `— R4 imagem`.
5. **A trava dos 2 anúncios ativos por conjunto continua valendo.** Duplicar-e-pausar mantém a
   contagem, mas se o conjunto estiver no limite, a rodada espera.
6. **Gasto acumulado da escada vira aviso.** Se o anúncio passar de **R$ 30 gastos** dentro da
   escada sem nenhum lead, avisar o Pablo — oito dias de teste num anúncio sem retorno é uma
   escolha que ele precisa poder revisar.

### O custo honesto desta regra

Quatro rodadas de 2 dias são **8 dias no mínimo** antes de qualquer pausa — e, com a entrega atual,
provavelmente bem mais, porque as rodadas vão esticar para alcançar o piso de impressões. Durante
esse tempo um anúncio ruim continua gastando.

É uma troca deliberada: **gasta-se mais tempo para não jogar fora criativo que só precisava de
um título melhor.** Vale a pena quando o criativo é caro de produzir, que é o caso aqui. Fica
registrado para que a escolha seja lembrada como escolha, não sofrida como lentidão.


## REGRA V3 — troca de criativo em 48h (decisão do Pablo em 15/09/2026, 20h)

*Substitui a escada de 4 rodadas de 14/09 no nível anúncio. Pablo: "no prazo de 48 horas o
anúncio não performar, mudar o criativo, imagem, copy, com base nos dados, contexto, objetivo da
agência".* As travas continuam iguais. **No nível conjunto, a partir de 17/09/2026 vale a C0 —
48h sem lead, o conjunto é pausado — e ela tem prioridade sobre C1. Ver "C0 — a regra dura de
conjunto".**

### Quando um anúncio "não performou" (tempo E volume, como sempre)

| # | Condição (≥ 48h no ar) | Leitura |
|---|---|---|
| T1 | ≥ 300 impressões **e** 0 lead | entrega sem converter |
| T2 | gasto ≥ 2× o CPL do melhor anúncio do conjunto (melhor com ≥ 3 leads) **e** 0 lead | já custou dois leads e não trouxe nenhum |
| T3 | ≥ 2 leads **e** CPL > 2× o do melhor anúncio | converte caro |
| T4 | ≥ 300 impressões **e** CTR < 0,80% | ninguém clica |
| T5 | ≥ 300 impressões **e** CPM > 2× o CPM médio do conjunto (ou > R$ 60) | leilão rejeita a peça: imagem/copy com baixa qualidade percebida |
| T6 | frequência > 3 **e** 0 lead | mesma pessoa vendo 3+ vezes sem agir: peça cansou |
| T7 | ≥ 20 cliques no link **e** 0 lead | clica e não preenche: promessa da peça não bate com o formulário |
| T8 | CPC > 2× o CPC do vencedor **e** 0 lead | cada clique custa o dobro do melhor: peça fraca |

**Métricas que a rodada lê sempre, por anúncio e por conjunto (últimos 7 dias e desde a última
mudança de público):** impressões, alcance, frequência, cliques no link, CTR, CPC, CPM, gasto,
leads, custo por lead, taxa clique→lead (leads ÷ cliques). Sem essas 11 colunas a rodada não julga.
Diagnóstico pela combinação: CTR baixo + CPM alto = imagem; CTR ok + T7 = copy/promessa ou
formulário; frequência alta = público saturado (aviso ao Pablo, não troca de criativo).

Menos de 300 impressões em 48h **não é veredito** — é falta de entrega. Anúncio assim não é
trocado nem pausado; fica, e se passar de 7 dias sem 300 impressões vira aviso ao Pablo.

### O que fazer (uma troca por anúncio, sem escada)

1. **Ler o vencedor do conjunto** (mais leads, menor CPL): a imagem dele e a copy dele são a base.
2. **Criar anúncio NOVO** no mesmo conjunto (nunca editar o antigo por cima):
   - se o anúncio ruim tinha a **mesma copy** do vencedor → o problema é a imagem → novo = imagem
     do vencedor + **copy nova** (ângulo diferente do BRIEFING: objeção "já impulsionei",
     indicação, agenda vazia, "quem faz seus anúncios hoje");
   - se tinha **imagem igual** e copy diferente → novo = copy do vencedor + **imagem nova**
     (das 5 imagens já hospedadas no Meta, a que ainda não rodou nesse conjunto; se todas rodaram,
     gerar imagem nova e avisar o Pablo);
   - se era **tudo diferente** do vencedor → novo = imagem do vencedor + copy nova.
3. **Como criar:** Windsor `create_ad` com `{"creative":{"creative_id":"<criativo do vencedor>"}}`
   (carrega o formulário), depois Windsor `update_ad_creative` (headline, message,
   `degrees_of_freedom_spec: {}`, e `image_url` quando for imagem). Se o criativo do vencedor for
   SHARE sem `link_data` (erro "no editable media sub-spec"), apontar o anúncio pro criativo já
   editado de outro conjunto com Windsor `update_ad` `{"creative":{"creative_id":...}}`. Ativar
   pelo MCP `ads_activate_entity`. Nome: `V<n> — <o que mudou>`.
4. **Pausar o antigo** só se ele bateu T1/T2/T4 (0 lead) e o conjunto continua com ≥ 2 ativos.
   Renomear `ZZ TROCADO 48H — <nome>`. Anúncio T3 (converte caro) **fica no ar** até o novo ter
   48h e 300 impressões; aí compara e pausa o pior.
5. **Registrar** na tabela "Trocas feitas" abaixo: data, anúncio antigo, número que motivou,
   anúncio novo, o que mudou. O anúncio novo só pode ser julgado depois de 48h + 300 impressões.
6. **NUNCA usar a foto do Pablo em criativo** (regra obrigatória, Pablo 15/09). Imagem nova = ilustração,
   cena de negócio ou texto sobre fundo; rosto do Pablo, nunca.
7. **Copy sempre no BRIEFING:** agência que escreve, publica e acompanha; dono só atende; para quem
   já fatura; sem "90 dias", sem preço, sem promessa em reais; formulário de 3 perguntas.

### Trocas feitas

| Data | Antigo (ID) | Conjunto | Motivo | Novo (ID) | O que mudou |
|---|---|---|---|---|---|
| 15/09 20h | V11 `120247409468960766` | INTERESSE | T1: 523 imp, 0 lead, R$13,54 em 72h (V15: 6 leads a R$8,41) | V16 `120247453147450766` | imagem do V15 + copy "Impulsionou e não deu em nada?" |
| 15/09 20h | — (adicionado) | INTERESSE | teste de 2ª copy junto | V17 `120247453147890766` | imagem do V15 + copy "Pare de depender de indicação" |
| 15/09 20h | — (adicionado) | CNAE RJ | conjunto com 0 lead em 7d, só copy antiga no ar | V16 `120247453176830766` | mesmo criativo do V16 INTERESSE |

## As travas — o que a regra NUNCA faz

1. **Nunca mexe em orçamento.** Nem sobe, nem desce, nem tira teto. Isso é decisão do Pablo.
2. **Nunca pausa nada que gerou lead nas últimas 48 horas**, por pior que esteja o CTR.
3. **Nunca deixa um conjunto com menos de 5 anúncios ativos** (Pablo, 15/09 22h: "ao menos 5 por conjunto, mesmo que ainda não tenha performado" — público mudou, tudo recomeça). Se o corte esvaziaria o conjunto,
   pausa só os piores e mantém os 2 melhores rodando até haver substituto.
4. **Nunca pausa o último conjunto ativo de uma campanha.** Campanha zerada não volta do zero de
   graça — perde o aprendizado inteiro.
5. **Nunca apaga.** Só pausa e renomeia com prefixo `ZZ`. O que está pausado guarda histórico e
   pode voltar.
6. **Nunca corta antes das 48h**, mesmo que o número esteja horrível. Único caso de corte
   imediato: erro de entrega que impede o anúncio de rodar (aí é conserto, não corte).
7. **Nunca pausa anúncio que ainda não terminou a escada.** Desde 14/09/2026, pausar anúncio é o
   último degrau, nunca o primeiro. Conjunto continua podendo ser pausado direto pelas regras C.

## Escadas em andamento

**Esta tabela é a memória da escada.** Cada rodada de corte roda numa sessão nova, sem lembrar da
anterior — então o estado de cada anúncio em teste tem que estar escrito aqui, ou a escada
recomeça do zero toda vez e nunca chega ao quarto degrau.

**Toda rodada de corte começa lendo esta tabela** e continua de onde parou, antes de procurar
anúncio novo para abrir escada.

| Anúncio (ID) | Conjunto | Entrou por | Rodada atual | Variável desta rodada | Começou em | Impressões da rodada | Métrica base | Métrica atual | Situação |
|---|---|---|---|---|---|---|---|---|---|
| *(nenhuma escada aberta — última medição 15/09 09h13: nenhum anúncio bateu A1–A4, nenhum conjunto bateu C1–C3)* | | | | | | | | | |

**Como preencher:**
- **Métrica base** = o valor que o anúncio tinha quando entrou na escada (ou o da rodada anterior,
  se já avançou). É contra ele que a rodada é julgada.
- **Situação** = `rodando` (ainda juntando impressões), `melhorou` (bateu os 20%, sai da escada),
  `sem melhora` (fechou a rodada abaixo do piso de melhora, vai para a próxima), ou
  `inconclusiva — sem entrega` (passou de 7 dias sem 300 impressões; virou aviso ao Pablo).
- Quando a escada fecha — por melhora ou por pausa no quarto degrau — a linha **sai desta tabela**
  e vira parágrafo no "Histórico de cortes", com as quatro tentativas e os números de cada uma.

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


### Medição de 15/09, 09h13 (últimos 7 dias, anúncios ativos com 48h+)
- **V15** (120247409549130766): 1.979 impressões, CTR 1,52%, **6 leads a R$ 8,40** — melhor anúncio da conta, referência da regra A4.
- **V11** (120247409468960766): 522 impressões, CTR 1,53%, 0 lead, R$ 13,52 — não bate A1 (menos de 1.000 impressões) nem A2/A3. Vigiar: se chegar a 1.000 sem lead e CTR cair abaixo de 0,50%, abre escada.
- **V13** (120247409490290766): 99 impressões, 1 lead a R$ 3,20.
- Demais V11–V15 duplicados: menos de 300 impressões cada, sem volume para julgar.
- **AGENDA (5 anúncios, criados 14/09 22h)**: menos de 48h de vida, fora da análise. Observação: o conjunto mostra R$ 1,41 gastos hoje mas os anúncios ainda reportam 0 impressões — atraso de atribuição, conferir amanhã.
- Nenhuma regra A ou C bateu. Nada aberto, nada pausado.
