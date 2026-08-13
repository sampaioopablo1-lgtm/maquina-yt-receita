# LLM sem cartão de crédito: empilhar free tiers

**Decisão (13/08/2026):** a máquina sai do Gemini como provedor único, mas não
troca por plano pago. Passa a usar uma **cadeia de planos gratuitos** que troca
de elo sozinha quando um bate no limite.

## O problema não era qualidade, era cota

O free tier do Gemini dá **20 requisições por dia**. Cada pacote consome de 2 a
5 (ideação, roteiro, até duas extensões, short companheiro). Com seis disparos
diários a conta é ~30 requisições — a cota estoura antes do meio-dia. Foi o que
derrubou `next-level-money` em 12/08/2026 às 22:14 com HTTP 429.

Trocar Gemini por outro provedor único só move a parede de lugar. A saída é
somar, porque nenhum plano gratuito sozinho aguenta o ritmo e quatro somados
sobram com folga de ordem de grandeza.

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
llm_cadeia: ["anthropic", "cerebras", "groq", "mistral", "gemini"]
llm_modelos:
  cerebras: "gpt-oss-120b"
  groq: "openai/gpt-oss-120b"
  mistral: "mistral-large-latest"
  gemini: "gemini-flash-latest"
```

`anthropic` fica na frente da lista mesmo sem assinatura: **a lista é desejo, a
chave é que decide**. Sem `ANTHROPIC_API_KEY` no ambiente o elo é pulado em
silêncio, e no dia em que a chave existir a máquina passa a usá-la sozinha.

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

## Chaves a criar (todas gratuitas, sem cartão)

| Secret | Onde | Minutos |
|---|---|---|
| `CEREBRAS_API_KEY` | cloud.cerebras.ai | ~2 |
| `GROQ_API_KEY` | console.groq.com/keys | ~2 |
| `MISTRAL_API_KEY` | console.mistral.ai | ~3 (verifica telefone) |

Adicionar em **Settings → Secrets and variables → Actions** do repositório. Os
workflows já passam as três. Enquanto nenhuma existir, a máquina continua no
Gemini exatamente como hoje — nada quebra, só continua limitada a 20/dia.
