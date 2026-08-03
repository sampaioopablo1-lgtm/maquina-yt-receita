# Playbook operacional do canal

Regras extraídas das fontes estudadas e convertidas em critérios que a máquina aplica.
As transcrições integrais dos vídeos de terceiros não são versionadas aqui — o que
importa operacionalmente são as regras abaixo, com a fonte registrada.

## Fontes estudadas

| Tema | Link |
|---|---|
| Análise de canal novo com 7 vídeos (CTR, retenção, diagnóstico) | https://www.youtube.com/watch?v=5d51ucUJH5E |
| Como subir vídeos corretamente (título, thumbnail, roteiro) | https://www.youtube.com/watch?v=a0O2edDkMlc |
| Vídeo longo vs. curto em canal dark | https://www.youtube.com/watch?v=GXTo_88pg7o |

## Os 3 pilares (critério central)

A máquina otimiza para três métricas nesta ordem. Um vídeo só é considerado saudável
quando **os três** estão alinhados — acertar dois e errar um derruba o vídeo.

| Pilar | Métrica | Meta | O que controla |
|---|---|---|---|
| 1. Título | Impressões | crescendo | Palavras-chave validadas do nicho |
| 2. Thumbnail | **CTR** | **≥ 5%**, bom a partir de 7-8% | Clique sobre a impressão |
| 3. Roteiro | **Retenção média** | **≥ 30%** | Se o vídeo é entregue ou morre |

**Diagnóstico que a máquina automatiza** (é exatamente o raciocínio da fonte 1):

- CTR alto + retenção baixa → **o problema é o roteiro/áudio**, não a thumbnail.
  Sintomas recorrentes: música alta demais, voz trocada no meio, gancho fraco nos
  primeiros 30s.
- CTR baixo + retenção boa → **o problema é a thumbnail**. Refazer no padrão validado.
- Impressões baixas → **o problema é o título**, não está "traqueando" palavra-chave.

Isto está implementado em `src/maquina/stages/diagnose.py`: a máquina puxa as métricas
do YouTube Analytics e devolve o gargalo nomeado, em vez de você olhar gráfico na mão.

## Anatomia da thumbnail (padrão validado)

Três elementos obrigatórios — a fonte 2 mostra que faltar um derruba o CTR:

1. **Texto curto no topo** — máximo 3 palavras (a maioria assiste no celular; texto longo
   vira fonte ilegível).
2. **Autoridade** — rosto/figura central, expressão séria, olhando para frente.
3. **Imagem que representa o título** — o objeto concreto do roteiro.

Mais: manter coerência de cenário com o padrão que funciona no subnicho (nas referências
analisadas: ambiente de casa + vegetação ao fundo).

⚠️ **Limite importante:** "seguir o padrão do nicho" é diferente de "copiar a thumbnail do
concorrente". Replicar composição, cores e enquadramento de um canal específico gera
conteúdo derivativo, enfraquece a marca e pode gerar reclamação. A máquina usa o padrão
como *briefing de estilo*, com arte própria.

## Título

Não inventar do zero em canal novo. O processo é:

1. Coletar títulos dos vídeos que performaram no subnicho.
2. Extrair as palavras-chave recorrentes.
3. Escrever **semelhante e melhorado** — nunca copiar e colar.

Quando o canal tiver público próprio, aí sim criar do zero sobre as palavras-chave do
canal.

**Tags:** peso mínimo na descoberta, por documentação do próprio YouTube. Úteis apenas
para termos frequentemente escritos errado. A máquina preenche, mas não gasta esforço ali.

## Formato: longo vs. Shorts

A estratégia de referência (fonte 3) é **vídeo longo, 40-60 min, em canal subnichado**,
com o argumento de que empilha receita recorrente e é mais previsível que o modelo de
"história" que estoura um vídeo e mata o canal.

Decisão deste projeto: **os dois, com papéis distintos.**

- **Longo (16:9)** — ativo principal. Gera receita acumulada e autoridade. Múltiplos
  blocos de anúncio, RPM maior.
- **Shorts (9:16)** — aquisição. Alimenta o topo do funil e testa ganchos barato, mas
  RPM muito baixo. Não é o produto, é o anúncio do produto.

## Constância e subnicho

- Escolher **um nicho**, testar vários temas dentro dele, identificar o que performa e
  focar nisso. Isso é o que a tabela `metricas` do Supabase existe para responder.
- Empilhar vídeos: a receita vem do acervo, não de um vídeo isolado.
- **Não abandonar canal com 3-7 vídeos.** O ciclo de sinal do YouTube é mais longo que
  isso — a fonte 1 mostra um canal dando sinal exatamente nessa faixa.
- Engajar nos comentários: é a fonte mais barata de diagnóstico ("música alta" aparece
  no comentário antes de aparecer no gráfico de retenção).
