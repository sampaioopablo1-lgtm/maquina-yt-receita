# Auditoria das campanhas — 09/09/2026

*Conta 1695865631502778. Período: desde 07/09 (início) até agora. Total gasto: R$48,88.*

## 1. Posicionamento: onde o dinheiro foi e o que voltou

### Conjunto de topo — INT I DONOS (R$26,36)

| Posicionamento | Impressões | Cliques | Gasto | CPM | CTR |
|---|---|---|---|---|---|
| **Facebook Reels** | 1.637 | **16** | R$13,59 | R$8,30 | **0,98%** |
| **Facebook Feed** | 285 | **2** | R$1,93 | **R$6,78** | 0,70% |
| Instagram Reels | 192 | 0 | R$1,59 | R$8,30 | 0% |
| Instagram Stories | 161 | 0 | **R$5,90** | **R$36,65** | 0% |
| Facebook Stories | 161 | 0 | R$2,38 | R$14,81 | 0% |
| Instagram Feed | 134 | 0 | R$0,97 | R$7,25 | 0% |
| Facebook perfil | 2 | 0 | R$0,00 | — | — |

### Conjunto de fundo — LEADS I LISTA CNPJ (R$22,52)

| Posicionamento | Impressões | Cliques | Gasto | CPM |
|---|---|---|---|---|
| Instagram Feed | 105 | 0 | R$6,78 | R$64,62 |
| Instagram Reels | 109 | 1 | R$6,27 | R$57,56 |
| **Instagram Stories** | 34 | 0 | R$5,24 | **R$154,16** |
| Facebook Reels | 25 | 1 | R$1,74 | R$69,75 | 
| Facebook Feed | 27 | 0 | R$1,47 | R$54,56 |
| **Facebook Stories** | 5 | 0 | R$1,02 | **R$204,45** |

## 2. Os cinco achados

### Achado 1 — Todos os cliques vieram do Facebook. Nenhum do Instagram.

No conjunto de topo: **18 cliques, os 18 no Facebook**. O Instagram consumiu R$8,46 em 487
impressões e devolveu **zero**.

Isso é contraintuitivo para quem trabalha o Instagram organicamente, mas o dado é claro. O
Facebook Reels sozinho entregou 1.637 impressões a R$8,30 de CPM com 0,98% de CTR — o melhor
número da conta inteira, e a única linha que se aproxima do que seria uma campanha saudável.

### Achado 2 — Stories queimou 30% do orçamento e trouxe zero cliques.

Somando os dois conjuntos, Stories (Facebook + Instagram) consumiu **R$14,54 de R$48,88** para
361 impressões e **nenhum clique**. O Instagram Stories no conjunto de fundo custou **R$154,16 de
CPM** — vinte e três vezes o Facebook Feed do topo. O Facebook Stories, R$204,45.

Stories é formato de tela cheia e passagem rápida: funciona para marca com criativo vertical
nativo, não para um vídeo de posicionamento reaproveitado. Nesta conta, é o buraco no balde.

### Achado 3 — ERRADO, corrigido às 12h. O público não é pequeno.

**O que eu escrevi primeiro está abaixo, e a correção vem logo depois.** Mantenho o texto original
à vista porque o erro é instrutivo: eu inferi o tamanho do público a partir do alcance, e alcance
é função do gasto, não do tamanho.

Consultando os públicos personalizados da conta diretamente:

| Lista | Tamanho no Meta |
|---|---|
| Cópia de Editado — CNAE 41 42 43 RJ 100K | **41.000 a 48.200** |
| Editado — CNAE 41 42 43 RJ 100K | **29.500 a 34.700** |
| Cópia de Leads empresaqui CONSULTORIA BR | 24.100 a 28.400 |
| Contabilidade BR 25K 2 | 8.700 a 10.200 |
| Leads empresaqui Instituição de ensino BR | 7.400 a 8.700 |
| Contabilidade RJ | 3.300 a 3.900 |

A maior lista **já é do Rio** e tem mais de 40 mil pessoas. As 231 do relato original eram o
alcance de R$21 gastos, não o tamanho do público.

**Isso derruba a explicação que eu dei para o CPM de R$73.** A causa é outra — otimização para
geração de lead com histórico quase nulo, ou o formato de publicação promovida, que engaja pouco
e por isso encarece o leilão. Fica em aberto, e é o que a próxima semana de entrega deve mostrar.

**E os públicos semelhantes já existem.** Onze deles, criados em 07/09 a partir destas mesmas
listas — todos `INACTIVE`, nunca usados. Não há o que construir: há o que ligar.

---

#### Texto original do achado 3, mantido para registro

*(Contém o erro corrigido acima.)*

O conjunto de fundo é pequeno demais, e por um motivo específico.

Ele carrega **doze públicos personalizados** — listas de CNPJ, contabilidade, SaaS, instituição de
ensino — que somam mais de 100 mil contatos no papel. Mas a segmentação geográfica exclui **todos
os estados do Brasil menos o Rio**, e a maioria dessas listas é **nacional** (`Contabilidade BR
25K`, `Leads empresaqui Saas BR`, `Instituição de ensino BR`).

O resultado é que 100 mil contatos viram um punhado de gente do Rio: **alcance real de 231
pessoas em dois dias**. Público minúsculo é exatamente o que faz o CPM subir para R$73 — o Meta
paga caro para achar as poucas pessoas que restam.

**E há uma pergunta de fundo:** contabilidade, SaaS e instituição de ensino são o seu cliente?
Se a mentoria é para dono de negócio local que precisa de lead no WhatsApp, essas listas estão
comprando o público errado a preço de público raro.

### Achado 4 — Não existe pixel na conta.

`promoted_object: {pixel_id: null}` nos dois conjuntos. Nenhum evento de site é rastreado, nenhum
público de remarketing por visita existe, e o Meta não tem sinal de conversão para aprender.

Os públicos de engajamento que você tem (`ENG INST`, `PG 365`, `VV 15s`) são bons e cobrem parte
disso — quem viu vídeo, quem interagiu com a página. Mas quem entra num site e não converte fica
invisível.

### Achado 5 — Duas configurações que estão brigando entre si.

**No topo:** `age_min: 25, age_max: 65` mas `age_range: [30, 50]`. Dois recortes de idade
diferentes no mesmo conjunto. O que vale é o 25-65; o 30-50 é resíduo de alguma edição.

**Nos dois:** `device_platforms: [mobile, desktop]`. Mas todos os posicionamentos que entregaram
são de celular (Reels, Stories, Feed mobile). Desktop está ligado e não entrega — não custa, mas
polui a leitura.

**No fundo:** `advantage_audience: 0` e `targeting_relaxation: {lookalike: 0, custom_audience: 0}`.
Toda expansão automática desligada, com um público que já é pequeno. É o oposto do que ele
precisa.

## 3. Os refinamentos, em ordem de impacto

| # | Mudança | Por quê | Ganho esperado |
|---|---|---|---|
| 1 | **Desligar Stories** nos dois conjuntos | 30% do gasto, zero clique, CPM de até R$204 | recupera ~R$9/dia de verba morta |
| 2 | **Concentrar no Facebook Reels + Feed** | 100% dos cliques vieram daí, ao menor CPM | mesma verba, ~3x mais cliques |
| 3 | **Ligar as melhorias padrão de criativo** | recomendação do próprio Meta, lift estimado 69 | o maior ganho isolado disponível |
| 4 | **Trocar o título `{{product.name}}`** | o Facebook não tem palavra para segmentar | destrava a entrega do conjunto de leads |
| 5 | **Tirar as listas nacionais fora do ICP** do conjunto de fundo | SaaS, ensino e contabilidade BR não são dono de negócio local do Rio | público volta a ter tamanho utilizável |
| 6 | **Ligar a expansão de público** no fundo | público pequeno + expansão desligada = CPM alto | CPM cai de R$73 para a faixa de R$10-20 |
| 7 | **Instalar o pixel** | nenhum evento de site rastreado hoje | habilita remarketing e aprendizado |
| 8 | Corrigir a faixa etária dupla no topo | 25-65 contra 30-50 no mesmo conjunto | higiene |

**Os cinco primeiros custam zero e são de hoje.** Os itens 7 e 8 são estrutura, para a semana.

## 4. A leitura honesta do conjunto

R$48,88 é pouco dinheiro para julgar campanha, e o Meta confirma isso: benchmark de indústria e
ranking de leilão voltam **sem dados**, porque 2.700 impressões não dão base estatística.

Mas duas coisas já são visíveis com esse volume, e não vão mudar com mais verba:

**Stories não converte aqui** — 361 impressões sem um único clique não é ruído, é padrão.

**E o Facebook Reels funciona** — 0,98% de CTR a R$8,30 de CPM é um número normal de campanha
saudável, no meio de uma conta que não tem nenhum outro.

O caminho não é gastar mais. É parar de dividir R$30/dia entre sete posicionamentos, sendo que
dois deles carregam tudo.
