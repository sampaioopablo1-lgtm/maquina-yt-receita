# Chegar perto de B2B na Meta sem segmentação de renda
Estudo feito em 10/09/2026 consultando a própria API da Meta
(METAADS_LIST_TARGETING_SEARCH via Composio), não de memória.

## 1. Renda não existe no Brasil. Ponto.

Busquei a classe `income` inteira. Existem exatamente quatro opções, e todas
as quatro são dos Estados Unidos:

| opção | tamanho |
|---|---|
| Renda familiar: 5% mais relevantes dos códigos postais (EUA) | 15,1 M |
| Renda familiar: 10% mais relevantes dos códigos postais (EUA) | 31,4 M |
| (mais duas faixas, também EUA) | — |

A Meta calcula isso a partir de renda média por CEP americano, com dado
público do censo. No Brasil não há equivalente e não existe nenhuma opção de
renda. Quem promete "segmentar por renda no Facebook Brasil" está vendendo
fumaça ou usando um proxy sem dizer.

## 2. O que existe no lugar: três proxies reais

### a) Classificação de consumidor — Brasil
A coisa mais perto de renda que a Meta oferece por aqui. É classificação de
**preferência de consumo**, não de renda declarada:

- `6046096201583` — Pessoas que preferem produtos de valor **alto** no Brasil — 18,1 M
- `6110813675983` — Pessoas no Brasil que preferem produtos de valor **intermediário e alto** — 46,2 M

Não é renda. É poder de compra inferido do comportamento. Serve como piso.

### b) Sinais de que a pessoa É dona de negócio
- `6002714898572` — Proprietários de pequenas empresas — 48,5 M
- `6377178995383` — **Administradores de lojas** — 1,1 M ← o mais apertado de todos
- `6297846662583` — Administradores do perfil comercial do Instagram — 89,3 M
- `6020530281783` — Administradores de página comercial — 63,3 M

E por setor, que é segmentação B2B de verdade:
- `6020530269183` — Admin de Página sobre Comida e Restaurante — 3,5 M
- `6020530250383` — Admin de Página sobre Varejo — 17,5 M
- `6020568271383` — Admin de Página sobre Saúde e Beleza — 30,4 M

### c) Idade do negócio — o filtro anti-iniciante
- `6273108079183` — Nova empresa ativa (< 6 meses) — 14,9 M
- `6273196847983` — Nova empresa ativa (< 12 meses) — 23,8 M
- `6273108107383` — Novo negócio ativo (< 24 meses) — 45,2 M
- `6041891177783` — Novos administradores de página — 736 M

Interesses brasileiros que só quem tem CNPJ costuma seguir:
- `6003099842040` — **Sebrae** — 4,1 M
- `6003210642133` — **Cielo** — 1,5 M (maquininha; consumidor não segue adquirente)
- `6005579149997` — PagSeguro — 13,8 M (mais fraco: também é carteira de consumidor)

Testei e **não existem** como interesse: Stone, SumUp, Mercado Pago, MEI,
CNPJ, nota fiscal.

## 3. O desenho que eu recomendo

Não é "achar renda". É empilhar três condições com E, e usar exclusão:

    (é dono: Proprietários de pequenas empresas OU Administradores de lojas
             OU admin de perfil comercial do Instagram OU cargos Dono/Sócio)
  E (tem poder de compra: preferem produtos de valor alto no Brasil)
  E (não é iniciante: EXCLUIR Nova empresa ativa < 6 meses
                      E EXCLUIR Novos administradores de página)

A terceira linha é a que faltava. No dia 10/09 a Jessica chegou pela campanha
de WhatsApp: afiliada de Mercado Livre, zero clientes, querendo encher um
grupo de WhatsApp. Ela passou por "admin de página" porque tinha acabado de
criar uma. **"Novos administradores de página" e "nova empresa < 6 meses" são
o carimbo de quem está começando** — e a mentoria não é para quem está
começando, é para quem já fatura e quer previsibilidade.

Incluir sinal de dono acha muita gente. Excluir sinal de iniciante é o que
tira a Jessica sem tirar o Julio.

## 4. Onde o dado do próprio Pablo vence tudo isso

Nenhum proxy da Meta chega perto de uma lista de CNPJ real. A conta já tem
lista de construção civil RJ (41/42/43), contabilidade RJ e BR, consultoria,
SaaS e instituição de ensino. Semelhante de lista de CNPJ é B2B de verdade;
interesse é aproximação.

O caminho mais forte para faturamento alto não é a Meta: é montar a lista.
Receita Federal abre CNPJ com CNAE, porte, capital social e município. Filtrar
por capital social e porte, subir como público personalizado e fazer semelhante
disso é mais preciso que qualquer combinação de interesse.

## 5. O que não fiz e por quê

Não apliquei nada. Isto é estudo — mexer em segmentação pausa conjunto e
reinicia aprendizado, e a conta já reiniciou três vezes hoje. Vale aplicar de
uma vez só, com o Pablo decidindo, e não em fatias.

Ressalva honesta: os tamanhos acima são globais, não do Rio. Dentro de RJ,
30-50 anos, cada um encolhe muito. Empilhar as três condições pode deixar o
público pequeno demais para R$30/dia entregar — o risco real dessa mudança
não é errar o alvo, é não ter volume.

---

# Parte 2 — A Meta TEM públicos B2B. E eles não servem para o Pablo.

Estudo em 10/09/2026, varrendo a classe `industries` da API (40 opções) e
comparando com o que o mercado escreve.

## O que encontrei: firmografia de verdade

A Meta tem segmentos B2B explícitos que quase ninguém usa. **Faturamento da
empresa** — não renda pessoal, faturamento do negócio:

| segmento | id | tamanho GLOBAL |
|---|---|---|
| Receita da empresa: abaixo de US$ 1 mi | 6377169088983 | 3,3 M |
| Receita da empresa: US$ 1 mi a 10 mi | 6377168992983 | 1,8 M |
| Receita da empresa: acima de US$ 10 mi | 6377408081983 | 1,19 M |
| Tamanho: 1 a 10 funcionários | 6377169550583 | 2,8 M |
| Tamanho: 11 a 100 funcionários | 6377134779583 | 1,5 M |
| Tamanho: 101 a 500 | 6377169297783 | 776 k |
| Tamanho: mais de 500 | 6377408290383 | 612 k |
| Empresas criadas antes de 2000 | 6377134922183 | 1,3 M |
| Empresas criadas 2000–2009 | 6377408028783 | 1,3 M |
| Empresas criadas 2010–hoje | 6377168689383 | 2,5 M |
| **Tomadores de decisões empresariais** | 6262428231783 | **41.974** |
| Interesses e cargos dos tomadores de decisões | 6262428209783 | 41.975 |
| Tomadores de decisões de TI | 6262428248783 | 13.754 |

E funcionários por porte de empresa B2B:
- Grandes (500+): 6075565069783 — 220 M
- Pequenas (10 a 200): 6080792282783 — 99,4 M
- Médias (200 a 500): 6080792228383 — 37,7 M

Mais 25 funções profissionais (Gestão 17,6 M, Vendas 14,2 M, Negócios e
finanças 7,9 M, Serviços jurídicos 1,0 M, Serviços de saúde 10,6 M...).

## Por que isso não resolve o problema do Pablo

**Os números da tabela são MUNDIAIS.** "Tomadores de decisões empresariais"
tem 42 mil pessoas no planeta inteiro. Filtrado para Rio de Janeiro, 30 a 50
anos, sobra um punhado — não entrega nem com orçamento grande, quanto mais
com R$30/dia.

Faturamento de US$ 1 a 10 milhões: 1,8 milhão no mundo. O Rio é uma fração
minúscula disso. Empilhar esse segmento com localização e idade produz um
público que a Meta não consegue entregar.

**O segmento existe, está documentado, e é inútil nesta escala.** Isso
contradiz muito conteúdo de guru que vende "segmentação B2B secreta do
Facebook" — a segmentação existe mesmo, o problema é o tamanho.

## O que o mercado diz (e onde concordo)

O consenso de 2026 entre quem opera:

1. **Público amplo tende a bater empilhamento de interesse.** Com Advantage+
   como padrão, o que você adiciona vira sugestão, não cerca. A exceção que
   os próprios artigos citam é justamente nicho B2B apertado — onde sair do
   interesse queima verba.
2. **Criativo filtra melhor que segmentação.** A mensagem decide quem para o
   dedo. "É para quem já fatura e quer previsibilidade" filtra mais do que
   qualquer combinação de interesse.
3. **Formulário instantâneo com pergunta de qualificação** custa bem menos
   por lead que landing page, e a pergunta é onde o filtro real acontece.

Onde eu discordo do consenso: "amplo + criativo" pressupõe volume de conversão
para o algoritmo aprender. Com 6 leads em um dia, não há aprendizado nenhum. Na
escala do Pablo, a segmentação ainda importa — só não do jeito que se vende.

## Veredito

**Não existe hack de renda. Existem quatro alavancas reais, em ordem de força:**

1. **Lista própria de CNPJ** — a única firmografia confiável. Receita Federal
   abre CNAE, porte e capital social por município. Semelhante disso vence
   qualquer interesse.
2. **Exclusão de iniciante** — "Novos administradores de página" e "Nova
   empresa ativa < 6 meses". Tira a Jessica sem tirar o Julio.
3. **A pergunta do formulário / da IA** — filtro que acontece depois do clique,
   e o único que enxerga faturamento de verdade.
4. **Criativo que desqualifica** — dizer no anúncio para quem NÃO é.

Os segmentos firmográficos da Meta ficam de fora não por serem ruins, mas por
serem pequenos demais para o Rio com R$30/dia. Se um dia a verba subir e a
operação for nacional, eles voltam para a mesa.
