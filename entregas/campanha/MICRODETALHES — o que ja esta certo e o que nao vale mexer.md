# Microdetalhes da conta — 09/09/2026, 14h

*Varredura de configuração fina: dispositivo, conexão, hora do dia, atribuição, frequência,
configuração da conta. Alguns itens que parecem otimização são mito; estão marcados como tal.*

## 1. Desktop — já desligado

| Dispositivo | Impressões | Gasto | CPM | CTR | Cliques |
|---|---|---|---|---|---|
| Android smartphone | 2.835 | R$ 49,54 | R$ 17,47 | 0,74% | **21** |
| iPhone | 214 | R$ 9,78 | R$ 45,71 | 0,00% | 0 |
| Desktop | 49 | R$ 0,24 | R$ 4,90 | 0,00% | 0 |
| Tablets | 15 | R$ 0,17 | — | 0,00% | 0 |

Desktop e tablet somam **R$ 0,41 na vida inteira** — o Meta já quase não entregava ali. Deixei só
celular nos quatro conjuntos, mas para registro: essa não era a fonte do desperdício.

## 2. iPhone custa 2,6× mais e não deu um clique — e mesmo assim não vou cortar

CPM de R$ 45,71 contra R$ 17,47 do Android, e zero clique em 214 impressões. Tentador cortar.

**Não vou, e o motivo é o que separa gestor de gestor:** 214 impressões não decidem nada. A
chance de zero cliques em 214 impressões com CTR real de 0,74% é de cerca de 20% — ou seja, um em
cada cinco recortes bons pareceria morto nesse tamanho de amostra. Cortar iOS agora seria decidir
no ruído, e iPhone no Brasil concentra renda mais alta, que é exatamente o dono de empresa que
queremos.

**Regra:** revisitar quando o iPhone passar de 1.000 impressões. Se continuar em zero, corta.

## 3. "Só Wi-Fi" — isso é mito neste caso

Existe a segmentação por conexão (`wireless_carrier: Wifi`), e ela **faz sentido em campanha de
instalação de app**: o app pesa dezenas de MB, quem está no 4G desiste no meio do download.

Aqui o destino é **formulário instantâneo dentro do Facebook** — abre em menos de 100 KB, no 3G
inclusive. Ligar "só Wi-Fi" cortaria de 30% a 40% do público para resolver um problema que não
existe, e ainda subiria o CPM, porque público menor é leilão mais caro.

**Decisão: não aplicar.** Se um dia houver campanha para site pesado ou app, aí sim.

## 4. Atribuição — eu achei um defeito, investiguei, e não era defeito

Os conjuntos de lead estão com janela de **1 dia de clique, 0 de visualização**. O padrão do Meta
para a maioria dos objetivos é 7 dias de clique, e janela curta significa menos conversões
atribuídas e aprendizado mais lento. Parecia um erro grave.

Tentei corrigir. O Meta respondeu duas coisas:

1. *"Attribution window update is no longer supported after adset creation."*
2. Ao criar um conjunto novo com 7 dias: *"Based on the objectives and optimization goals you
   have selected, supported combination of click-through and view-through attribution window
   values are: **(1, 0)**"*

Ou seja: **para formulário instantâneo, 1 dia de clique é a única janela que existe.** Não é
configuração errada, é regra da plataforma. O lead acontece dentro do próprio Facebook, na hora —
não há jornada de 7 dias para atribuir.

Registro isso porque quase criei um conjunto novo do zero para "corrigir" algo que estava certo.

## 5. Hora do dia — o dado existe, a ferramenta para usá-lo não

| Faixa | Gasto | Cliques | CTR |
|---|---|---|---|
| **21h** | R$ 2,93 | **6** | **2,28%** |
| 11h | R$ 4,70 | 2 | 1,56% |
| 9h | R$ 3,19 | 3 | 1,36% |
| 12h | R$ 6,45 | 2 | 1,19% |
| 18h | R$ 3,13 | 0 | 0,00% |
| 20h | R$ 3,18 | 0 | 0,00% |
| 22h | R$ 2,95 | 0 | 0,00% |

**21h é de longe a melhor hora** — 6 dos 19 cliques da conta, com CTR três vezes a média. E 12h é
a hora que mais gasta com desempenho mediano.

**Por que não vou aplicar programação horária agora:** o Meta só libera a grade de horários em
campanha com **orçamento vitalício**. As duas campanhas usam orçamento diário. Trocar para
vitalício muda o modo de gasto inteiro da conta e trava a data de fim — decisão sua, não minha,
e prematura com 19 cliques de histórico.

Fica anotado para quando houver volume: concentrar entre 9h e 12h, e 20h às 22h.

## 6. Limite de frequência

| Conjunto | Limite |
|---|---|
| INT I DONOS (topo) | 7 impressões a cada 7 dias — **correto** |
| Conjuntos de lead | nenhum |

Sem limite nos conjuntos de lead é aceitável **hoje**, porque a frequência está em 1,29. Vira
problema acima de 2,5. Fica na lista de vigilância.

## 7. Configuração geral da conta

| Item | Estado | Leitura |
|---|---|---|
| Fuso | America/Sao_Paulo | correto — os relatórios batem com o relógio do Rio |
| Moeda | BRL | correto |
| Status | ativo, sem restrição | limpo |
| **Limite de gastos da conta** | **nenhum** | ver abaixo |
| Categoria especial de anúncio | vazia | correto — mentoria não é emprego, crédito nem moradia |
| Orçamento mínimo diário | R$ 5,17 | referência |
| Filtro de inventário | RELAXED | adequado para B2B; MODERATE encareceria sem ganho |
| Pixel | existe (`1600846091439175`) | irrelevante para formulário instantâneo; útil quando houver site |
| Gasto acumulado | R$ 42,37 | — |

**O único item que eu recomendo e não posso decidir:** a conta está **sem limite de gastos**. Um
teto de conta é um freio de mão — se algo escapar (um conjunto duplicado, um orçamento digitado
errado), ele para antes de virar prejuízo. Sugiro **R$ 300/mês**, bem acima do que você gasta
hoje (R$ 30/dia = R$ 900/mês seria o teto natural das campanhas, mas o gasto real está em ~R$ 15).
Mexe em dinheiro, então é sua palavra.

## 8. O que eu não mexeria, e por quê

- **Otimização de orçamento por conjunto (ABO).** A campanha usa CBO e isso está certo com três
  conjuntos disputando o mesmo teste. ABO faria sentido para forçar gasto igual entre eles — mas
  aí o Meta para de proteger você de conjunto ruim.
- **Lance com limite (bid cap).** Só faz sentido quando existe custo por lead conhecido. Com zero
  leads, não há número para colocar no campo.
- **Público-alvo expandido.** Já desliguei hoje. Manter desligado até o teste do semelhante
  terminar — expansão contamina a comparação.

## 9. O que realmente importa, e não é micro

Nada nesta lista muda o jogo. O que muda é: **o conjunto de fundo tem 313 pessoas de alcance e
CPM de R$ 80.** Ajuste fino em público pequeno é enfeitar sala apertada. A resposta é o conjunto
semelhante que entrou hoje — se o CPM dele vier na faixa de R$ 20 a 30, a hipótese está provada e
o caminho é migrar o orçamento para lá.
