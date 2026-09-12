# Máquina de prospecção ativa no WhatsApp — 10 conexões, rotação e IA

Prospecção **personalizada** em volume. Cada mensagem é única porque cada empresa
errou uma coisa diferente. Não é disparo em massa: é a mesma esteira rodando muitas vezes.

## As sete camadas

### 1. Descoberta — já rodando
Varredura da Biblioteca de Anúncios da Meta de hora em hora, combinando nicho e bairro
sem repetir combinação. Saída por empresa: nome, página, **defeito do anúncio**, há quanto
tempo no ar, link público.

**Capacidade real: 3 a 5 empresas aproveitáveis por varredura, 50 a 80 por dia.**

### 2. Enriquecimento — o número
Por ordem de confiabilidade:
1. **URL de destino do próprio anúncio** — muitos apontam para `api.whatsapp.com/send?phone=`, com o número dentro. É a fonte mais limpa: o número está no anúncio que a empresa pagou para veicular.
2. **Bio do Instagram comercial** — botão de WhatsApp com o número.
3. **Site da empresa** — link `wa.me` ou botão flutuante.

Validação antes de entrar na fila: formato, DDD do Rio, duplicidade contra o histórico.

### 3. Redação — uma mensagem por empresa
Escrita caso a caso a partir do defeito. Não é template com variável: o defeito, a data e
o nome mudam o texto inteiro.

**Regra fixa:** a prova na primeira linha, a apresentação na segunda. A prévia da
notificação é a única linha garantida.

### 4. Rotação — 10 conexões, estado independente
Cada conexão é uma sessão D-API com `sessionId` próprio, IP dedicado e **estado próprio**:

| Campo | Para quê |
|---|---|
| `idade_dias` | define o teto da rampa |
| `enviados_hoje` | trava o teto diário |
| `bloqueios_janela` | numerador da taxa de bloqueio |
| `status` | ativa / aquecendo / pausada / caída |

**A rampa é por sessão, nunca global.** Chip novo não herda o volume de um chip maduro —
esse é o erro que derruba operações inteiras.

| Idade da sessão | Teto/dia |
|---|---|
| 0 a 7 dias | 20 |
| 8 a 14 dias | 50 |
| 15 a 21 dias | 100 |
| 22 dias+ | 150 |

Distribuição em rodízio ponderado pela maturidade, com sorteio: a mesma empresa nunca
recebe dois toques de números diferentes.

### 5. Envio
- Intervalo aleatório de **40 a 120 segundos**, nunca ritmo constante
- Somente 9h às 18h, dias úteis
- **Nenhum link na primeira mensagem**
- Perfil de cada conexão completo antes do primeiro envio: foto, nome, descrição

### 6. Resposta — o webhook acorda a IA
A D-API dispara `messages.received`. Esse webhook aponta para uma URL de escuta que me
acorda com o conteúdo da resposta.

A partir daí:
1. Classifico: interessado / pergunta / não é o decisor / não quero
2. Escrevo a resposta no contexto daquela empresa e daquele defeito
3. Ofereço **17h30 ou 18h30**, mesmo dia, limite 21h30
4. Aceitou → crio o evento na agenda com Meet e aviso o Pablo
5. Não é o decisor → peço o contato de quem é, e o caso volta para a fila com o novo alvo

Quem responde **sai da cadência na hora**. Nunca recebe o toque seguinte.

### 7. Monitoramento — o que realmente protege
A Meta bloqueia automaticamente acima de **2% de taxa de bloqueio**. Esse é o número que
decide se a operação vive, e ele é medido no número, não na ferramenta.

Por sessão, a cada rodada:
- taxa de bloqueio na janela de 50 últimos envios
- taxa de resposta (resposta alta protege o número: sinaliza mensagem desejada)
- status da conexão

**Paradas automáticas:**
| Gatilho | Ação |
|---|---|
| 2 bloqueios em 50 envios numa sessão | pausa **essa** sessão por 48h |
| taxa de bloqueio geral acima de 1,5% | pausa **tudo**, avisa o Pablo |
| conexão caída | tira do rodízio, não redistribui a cota |

## A cadência

| Toque | Quando | Conteúdo |
|---|---|---|
| 1 | dia 0 | O defeito, com data. Pergunta quem cuida das campanhas. |
| 2 | dia 3 | Quanto isso custa por mês, na verba dele. |
| 3 | dia 7 | O anúncio de um concorrente feito certo. Encerramento. |

Três toques, não cinco. WhatsApp é mais invasivo que e-mail: o quarto toque não traz
resposta, traz bloqueio.

## O dimensionamento honesto

10 conexões maduras suportam **1.500 mensagens/dia**. A descoberta entrega **50 a 80**.

**A camada de rotação está superdimensionada para a de descoberta.** Começar com 10
conexões é pagar por capacidade que não tem o que enviar — e pior, obriga a diluir a
personalização para preencher, que é exatamente o que sobe o bloqueio.

**Começar com 3 conexões.** Elas cobrem 150 a 450/dia quando maduras, o dobro do que a
descoberta produz. Subir para 10 quando a descoberta escalar — o que exige outras fontes
além da Biblioteca de Anúncios.

## Regra inegociável

**Nenhuma das conexões é o número pessoal do Pablo.** Dez chips dedicados. O pior caso
tem que ser perder um chip, nunca o telefone do negócio.

## O que falta confirmar

- **Preço da D-API** — a página de planos é renderizada por JavaScript e o sandbox não
  executa. Precisa ser conferido no site.
- Se o plano cobre 10 sessões simultâneas e qual o custo por sessão.
