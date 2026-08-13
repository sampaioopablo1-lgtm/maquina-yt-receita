# A cadeia de LLM: Gemini no Tier 1, free tiers como rede

**Decisão (13/08/2026): não fazer nada.** O free tier do Gemini cabe a máquina
como ela está hoje. Atrás dele existe uma cadeia de planos gratuitos, inerte
enquanto não houver chave — ela só precisa existir para que um 429 de pico não
mate o job.

Contagem de chamadas por pacote, no código de hoje:

| | chamadas |
|---|---|
| short (o que a máquina produz agora) | **1** + 0,2 de ideação amortizada |
| longo (só 2 canais passam no portão de 300 views) | até 5 |

Seis disparos por dia dão **~11 a 13 chamadas** contra o teto de 20. O 429 que
derrubou `next-level-money` em 12/08 aconteceu **antes** do banco de pautas
(`ideia_guardada`, que amortiza a ideação em 5 pacotes) e da virada para
shorts — os dois consertos que reduziram a conta. Tratar a cota como problema
aberto depois deles foi resolver duas vezes o mesmo sintoma.

`maquina auto` agora imprime quantas chamadas o disparo gastou, por provedor.
Seis disparos dizem a verdade; até lá a conta acima é leitura de código.

**Ative faturamento só se o contador cruzar 20/dia** — aí o caminho está
descrito abaixo e leva 2 minutos.

> **O plano de consumidor não resolve.** Google AI Plus / Pro / Ultra (app do
> Gemini, Flow, NotebookLM) e a **API** do Gemini são medidores separados.
> Assinar o Plus não levanta o teto de 20 req/dia da API — o que levanta é
> vincular uma conta de faturamento ao projeto do Cloud, o que move a chave do
> Free Tier para o **Tier 1**.

**Custo medido no volume atual** (~30 chamadas/dia, ~60k tokens de entrada e
~22k de saída):

| Caminho | US$/mês |
|---|---|
| Gemini Flash (Tier 1) | ~8 |
| Gemini Flash-Lite | ~2 |
| Anthropic Opus 5 | ~26 |

> **Cuidado com o alias.** `gemini-flash-latest` segue o Flash mais novo, e o
> preço do Flash já subiu 5x entre versões (de 0,30/2,50 para 1,50/7,50 por 1M).
> O alias é conveniência que pode multiplicar a fatura sem aviso. Para cravar um
> id fixo: `maquina llm-modelos --provedor gemini`.

`llm_teto_usd` (padrão US$ 2,00 por run) agora vale para o Gemini também — não é
fallback para o próximo elo, é parada: trocar de fornecedor por orçamento só
mudaria de bolso.

---

## Por que a cadeia continua existindo, mesmo com o teto removido

O free tier do Gemini dá **20 requisições por dia**. Cada pacote consome de 2 a
5 (ideação, roteiro, até duas extensões, short companheiro). Com seis disparos
diários a conta é ~30 requisições — a cota estoura antes do meio-dia. Foi o que
derrubou `next-level-money` em 12/08/2026 às 22:14 com HTTP 429.

O faturamento resolve o teto **diário**, não a indisponibilidade: um 503, um
429 de pico ou um 400 de campo continuam derrubando o job se não houver para
onde ir. Foi isso que aquele run provou — a Anthropic estava configurada e
ociosa e o job morreu mesmo assim, porque o provedor era escolhido uma vez, na
construção. Os free tiers atrás do Gemini custam zero e removem essa classe
inteira de falha.

## As cotas (agosto/2026)

| Provedor | Cota gratuita | Limite que morde | Cartão? |
|---|---|---|---|
| **Cerebras** | 1M tokens/dia | 30 RPM · contexto 8K no free | não |
| **Groq** | 14.400 req/dia | **6.000 tokens/min** | não |
| **Mistral** | 1B tokens/mês | 2 RPM | não (pede telefone) |
| **GitHub Models** | 50 req/dia (alto) · 150 (mini) | 8K entrada / **4K saída** | não |
| **OpenRouter** (`:free`) | 50 req/dia | sobe para 1.000 com US$10 gastos uma vez | não |
| **Gemini** | 20 req/dia | — | não |

A máquina precisa de ~30 chamadas/dia, **sequenciais** (um pacote por vez). Por
isso os limites de requisições por minuto — 2 RPM da Mistral, 5 da Cerebras —
não incomodam. O que morde é o **teto por request**:

* **Groq, 6.000 TPM**: o roteiro de um longo pede 16k tokens de saída. Não cabe.
  Groq serve bem os shorts (~3-4k reais por chamada) e falha nos longos — a
  cadeia cobre isso passando para o próximo elo.
* **GitHub Models, 4K de saída**: mesma história, e por isso ele não está na
  cadeia padrão. Fica no catálogo porque não exige secret nova em Actions.
* **Cerebras, contexto 8K no free**: cabe o short com folga; o longo aperta.

Ou seja: a ordem da cadeia não é ranking de qualidade, é **ordem de quem
aguenta o request que estamos mandando**.

## Como está configurado

```yaml
llm_provider: "auto"
llm_cadeia: ["gemini", "cerebras", "groq", "mistral", "anthropic"]
llm_modelos:
  cerebras: "gpt-oss-120b"
  groq: "openai/gpt-oss-120b"
  mistral: "mistral-large-latest"
  gemini: "gemini-flash-latest"
```

**A lista é desejo; a chave é que decide.** Provedor sem chave no ambiente é
pulado em silêncio, então a cadeia pode citar quem você ainda não assinou.

`anthropic` fica em **último** de propósito, apesar de ser a melhor: é 13x mais
cara que o Gemini no Tier 1, e um elo caro na frente da fila transformaria
"adicionei a chave para testar" em fatura sem ninguém escolher isso. Para usá-la
é preciso dizer: `llm_provider: "anthropic"`.

## Os ids de modelo mudam — não chumbe em código

O `qwen/qwen3-32b` da Groq foi descontinuado em junho/2026. Em 13/08/2026 duas
fontes públicas discordavam do id correto do Qwen3-235B na Cerebras no mesmo
dia. Por isso o id vive no YAML e existe:

```bash
maquina llm-modelos              # todos os provedores com chave
maquina llm-modelos --provedor groq --filtro qwen
```

Ele marca com `*` o que está na config e avisa em vermelho se o id configurado
não aparecer mais na lista do provedor.

## Qualidade: o que ainda não sabemos

Os canais falam **oito idiomas** (pt-BR, es-MX, en, id-ID, tr-TR, el-GR, hi-IN,
pl-PL). Isso é a parte incerta da troca:

* **Llama 3.3 70B** cobre oficialmente 8 idiomas, e indonésio, turco e grego
  **não estão entre eles**.
* **Mistral Large** é forte nos europeus e mais fraco em hindi e indonésio.
* **Qwen3** e **gpt-oss-120b** são os candidatos mais plausíveis para cobertura
  ampla, por isso `gpt-oss-120b` é o padrão nos dois primeiros elos.

Nada disso está **medido** nos nossos idiomas — é leitura de documentação, não
evidência. O jeito de resolver é rodar o mesmo short em indonésio, turco e
grego por provedor e comparar com a revisão de tradução que a máquina já tem
(`stages/revisao.py` já pede naturalidade e devolve `aceitavel`/não). Até lá,
tratar a escolha de modelo como hipótese.

## Chaves opcionais da rede (todas gratuitas, sem cartão)

| Secret | Onde | Minutos |
|---|---|---|
| `CEREBRAS_API_KEY` | cloud.cerebras.ai | ~2 |
| `GROQ_API_KEY` | console.groq.com/keys | ~2 |
| `MISTRAL_API_KEY` | console.mistral.ai | ~3 (verifica telefone) |

Adicionar em **Settings → Secrets and variables → Actions** do repositório. Os
workflows já passam as três. Enquanto nenhuma existir a máquina roda só no
Gemini — funciona, mas volta a ter um ponto único de falha.
