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
