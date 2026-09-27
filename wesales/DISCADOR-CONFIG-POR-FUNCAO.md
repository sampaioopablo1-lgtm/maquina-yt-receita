# Discador (Call Center do WeSales) — a configuração de cada função

Pergunta do dono em 27/09/2026: *"Considerando as telas enviadas do Power Dialer, qual a
configuração que cada função precisa fazer dar start na lista e ser seguida
automaticamente?"*

**De onde vem esta resposta, para não haver dúvida:** eu **não** estou olhando as telas
nesta sessão. Estou usando a leitura que foi feita delas e registrada na §3 do
`USABILIDADE.md` — e **reconferi todos os números na conta hoje**, porque eles mudaram
desde que aquela seção foi escrita. Onde a tela e o número divergem, o número está aqui.

---

## A resposta curta, antes dos detalhes

**O discador não tem start automático.** `Iniciar discagem` é botão, e não existe rota de
API nem gatilho de workflow que o aperte. Então "ser seguida automaticamente" não pode
significar o discador começando sozinho.

O que **pode** ser automático — e é o que importa — é **a composição da lista** e **o que
acontece depois de cada ligação**. O humano fica com três cliques e uma classificação:

```
  a máquina mantém a tag  →  3 cliques do SDR  →  disca  →
  SDR marca "Resultado da tentativa"  →  a máquina retoma
```

---

## Por que a lista tem de ser por TAG, e não por pipeline

A tela `Fila de ligações` tem o bloco **PUXAR DO CRM** com exatamente dois modos:

| modo | o que faz |
|---|---|
| **Pipeline** | pipeline + estágio → `Puxar leads deste pipeline` |
| **Tag** | uma tag → `Puxar contatos desta tag` |

E o resultado é uma **lista plana**: `Prioridade` não chega ao discador. Toda a
reconciliação de `Prioridade` ordena a *lista inteligente*, que é outra tela.

**Medido hoje, e é mais grave do que o documento dizia:**

| | |
|---|---|
| discáveis com segurança (`Prioridade` ≥ 3, sem DND, sem `nao-perturbe`, com telefone) | **8** |
| **protegidos que TÊM telefone** — o que o modo Pipeline arrastaria | **42** |

O documento anterior estimava 34. São **42**. Puxar por `Pipeline → FUNIL DE VENDAS →
CONECTAR` liga para gente que está travada de propósito, e `Prioridade = 0` **não protege**
porque o discador não lê esse campo.

> **Regra, sem exceção: ninguém puxa por Pipeline.** O modo Tag é o único seguro.

---

## SDR

**Tag: `fila-sdr`** — criada e populada na conta em 27/09 14:52. Hoje tem **5 contatos**:
Gerson, Ana Ruth, Ricardo, Andreia, Andre (o lote 1 da rampa, `Prioridade` 4).

### O que o SDR faz na tela — três cliques, sem escolher nada

```
1. Call center → Fila de ligações
2. PUXAR DO CRM → aba Tag → fila-sdr → Puxar contatos desta tag
3. Iniciar discagem
```

### Os parâmetros da tela, e por que ficam como estão

| campo | valor | por quê |
|---|---|---|
| `NÚMERO ATIVO` | `O Próximo Cliente · 5512982381407` | único número da conta; nada a escolher |
| `TOQUE MÁX. (S)` | **30** | 30 s é o que faz a chamada perdida aparecer no celular do lead. Abaixo de ~20 s muita gente nem vê |
| `PAUSA ENTRE LIGAÇÕES (S)` | **3** | dá ao SDR tempo de marcar o resultado antes da próxima. Zero transforma a fila em atropelo |

### O que o SDR faz **depois** de cada ligação — e este é o elo fraco

Marcar **`Resultado da tentativa`**. Não é burocracia: é o que faz a máquina continuar.
O `Pós-ligação v3` (publicado) lê esse campo e decide a mensagem, o contador e o próximo
toque.

**O discador não escreve esse campo.** Medido: `Resultado da tentativa` preenchido em
**4 de 64** contatos. Se o SDR não marcar, a cadência para — e para em silêncio, sem erro
em lugar nenhum.

---

## Closer

**Tag: `fila-closer`** — criada e populada em 27/09 14:52. Hoje tem **2 contatos**, e os
dois são o item mais valioso da operação:

| | |
|---|---|
| `Daniel` `+5521968390582` | R$ 5.000 · nota **93** · `Budget` = Tem · `Prazo` = Pra ontem · `Decisor` = Sim |
| `genilson \| Bombeiro` `+5521972023213` | idem |

Os dois em `NEGOCIAR` desde **19/09**, `updatedAt` = 19/09. **Oito dias, nenhum toque.**

```
1. Call center → Fila de ligações
2. PUXAR DO CRM → aba Tag → fila-closer → Puxar contatos desta tag
3. Iniciar discagem
```

Mesmos 30 s e 3 s. Depois da ligação o closer marca **`Reunião foi qualificada`** e, se
desqualificar, **`Motivo da desqualificação`** — é o par que o `Loop do closer v2` lê.

**Por que fila separada e não uma só:** o discador entrega lista plana, sem ordem. Se SDR e
closer puxassem a mesma tag, o closer discaria lead de primeira tentativa e o SDR discaria
negociação em andamento. Duas tags é mais barato que um mal-entendido.

---

## Gestor

**Não configura discador — não disca.** A função dele são duas telas:

- `Call center → Dashboard` (nunca foi examinada; ver abaixo)
- a contagem de tarefa vencida, que é o freio de capacidade

E o freio **não existe hoje**: quatro workflows consultam a tag `sdr-lotado` e **ninguém a
aplica**, então a resposta é sempre "não está lotado". Com 5 leads não dói; no cenário de
10 leads/dia, dói.

---

## Como a lista se mantém sozinha

A tag é o que automatiza. A regra:

```
entra  em fila-sdr    : Prioridade >= 3, etapa CONECTAR, sem DND, sem nao-perturbe, com telefone
sai    de fila-sdr    : caiu abaixo de 3, ganhou DND/nao-perturbe, mudou de etapa, ou foi conectado hoje
entra  em fila-closer : etapa REUNIÃO DE DIAGNÓSTICO ou NEGOCIAR, sem DND, com telefone
sai    de fila-closer : saiu dessas etapas, ou virou won/lost/abandoned
```

**Remover importa tanto quanto pôr.** Tag que fica é lead discado sem motivo — e aqui o
discador **liga de verdade**, não é lista para olhar.

**O atuador existe e rodou.** `wesales/tools/atuador_filas.py`, na Action
`wesales-finalizar.yml` (modo `filas-aplicar`) e no `wesales-filas.yml` com cron às
**11:10 UTC de segunda a sexta** — 08:10 em São Paulo, antes do expediente, para o SDR
abrir o discador com a fila do dia pronta.

Como foi validado, em duas camadas:

1. **Offline, antes de tocar no CRM:** rodei a regra contra o snapshot real da conta e ela
   **reproduziu exatamente** a decisão que eu havia tomado à mão — `fila-sdr` 5,
   `fila-closer` 2, nada a pôr, nada a tirar.
2. **Ao vivo, na Action:** rodou contra a conta, releu depois de escrever e **convergiu**.
   O script sai diferente de zero se não convergir, então "passou" é a prova, não o print.

Detalhe de desenho que vale dizer: o `pablo sampaio`, que tem `Prioridade` 5, ficou fora da
fila **pelo mecanismo, não pela heurística de nome** — a oportunidade dele está `lost`,
então não tem etapa aberta. Regra que depende de estado real erra menos que regra que
depende de lista de exceções.

O cron só vale depois do merge, porque agendamento roda a versão do branch padrão e o
script vive no branch de trabalho. Até lá, o modo `filas-aplicar` faz o mesmo.

### Se a ordem passar a importar

Ela se perde na lista plana. Aí o caminho é tag por faixa (`fila-5`, `fila-4`…) e o SDR
puxa a de cima primeiro. Mais tags, mais manutenção — só fazer quando o volume justificar.
Com 5 leads, não justifica.

---

## Duas coisas que podem mudar esta resposta, e eu não tenho como ver

**1. `Gatilhos`** — uma das quatro telas do Call Center que ninguém abriu (`Disparo`,
`Gatilhos`, `Mensagens rápidas`, `Dashboard`). Se `Gatilhos` permitir "ao terminar a
ligação, faça X", parte do que aqui depende do SDR marcar à mão passa a ser automático — e
o elo fraco desta resposta desaparece. **Vale abrir antes de treinar ninguém.**

**2. `Receber` está `Desativado`** — o interruptor ao lado do número ativo. A operação vai
discar dezenas de vezes com toque de 30 s; lead que vê chamada perdida **liga de volta**, e
é o retorno mais barato do funil. Com `Receber` desligado essa ligação não é atendida aqui.

Não vou afirmar o que `Desativado` significa — se rejeita, cai em caixa postal, ou só não
toca **nesta aba** (o padrão em softphone). As três consequências são diferentes. Conferir
custa uma ligação do celular para `5512982381407`.


---

## Adendo de 27/09 15:52 — tela real recebida, três fatos novos

O dono mandou a tela do Call Center com `fila-sdr` puxada. Três coisas que a leitura
anterior não tinha:

**1. `fila-sdr` funciona na ferramenta.** `Puxar contatos desta tag` devolveu
**"5 contato(s) com telefone · 5 novo(s) adicionado(s)"** — Ana Ruth, Ricardo, Andreia,
Andre e Gerson na caixa. A tag mantida pelo atuador é lida pelo discador exatamente como
desenhado. Verificado na tela, não só na API.

**2. `Receber` está LIGADO** ("Recebendo"). O dono ativou. A pergunta aberta sobre chamada
de retorno está fechada: o número `5512982381407` atende retorno nesta aba.

**3. A tela é a aba `Disparo`, não `Fila de ligações` — e são ferramentas diferentes.**
`Disparo` tem `Escolher áudio`, `INTERVALO (s)` = 5, `TOQUE MÁX. (s)` = 5 e
**`SIMULTÂNEAS` = 5**. Isso é **disparo de áudio em massa, 5 linhas em paralelo**, com toque
de 5 segundos — um robô, não uma fila para o SDR conversar. Duas consequências:

- **Para a rotina do SDR, a aba é `Fila de ligações`** (sequencial, o SDR fala). Puxar a
  `fila-sdr` em `Disparo` e apertar o botão laranja ligaria para os 5 ao mesmo tempo com
  toque de 5 s — sem áudio selecionado, o comportamento é incerto; com áudio, é robocall
  para lead pago. **Não apertar em `Disparo`** sem saber o que ele faz sem áudio.
- **Corrijo o que escrevi sobre o teto da ferramenta:** eu disse "sequencial, uma linha".
  `Fila de ligações` é; `Disparo` tem `SIMULTÂNEAS`, então a ferramenta **tem** paralelismo
  — só que para áudio, não para conversa. O teto de ~150/dia do SDR humano continua; o
  de disparo de áudio é outro assunto e outra decisão.

A aba **`Gatilhos`** está a um clique dessa tela. É a que pode automatizar o pós-ligação e
tirar do SDR o dever de marcar `Resultado da tentativa` à mão. Vale mandar essa tela.

---

## Adendo de 27/09 16:40 — `Gatilhos` recebida, e dois ajustes na `Fila de ligações`

O dono mandou a aba `Gatilhos` e a `Fila de ligações` com a `fila-sdr` puxada.

### O que `Gatilhos` faz — e o que NÃO faz

Três eventos, cada um com `Ativar workflow` + `Aplicar tag(s)`:

| evento | quando dispara |
|---|---|
| `Ligação feita` | **você liga e o lead atende** |
| `Ligação recebida` | o lead liga e você atende |
| `Ligação perdida` | o lead liga e ninguém atende |

**Não existe evento para "liguei e não atendeu"** — que é ~80% das discagens. Então o
gatilho não substitui `Resultado da tentativa` para o caso mais comum. O elo fraco
desta resposta (o SDR marcar o resultado à mão) foi fechado por outro caminho: o
**Painel SDR** tem os botões `Não atendeu / Caixa Postal / Pediu retorno / Número errado /
Não ligar / Desqualificado`, um clique cada, e ao salvar a qualificação marca `Atendeu`
sozinho. Ver `ASSOCIACOES-DE-CAMPO.md` §4.

**O que vale configurar em `Gatilhos` (2 minutos, tela do WeSales — a API não chega aqui):**

| evento | `Aplicar tag(s)` | por quê |
|---|---|---|
| `Ligação feita` | `conectado-hoje` | é a tag que as cadências leem para **não** mandar mais toque no mesmo dia; o `Limpa conectado-hoje (24 h)` tira depois. Se o SDR esquecer de marcar `Atendeu`, a cadência ao menos não atropela o lead que acabou de atender |
| `Ligação recebida` | `conectado-hoje` | mesmo motivo: retorno do lead é conexão |
| `Ligação perdida` | *(nada)* | nenhum workflow publicado lê uma tag de "perdida"; tag sem leitor é ruído |

`Ativar workflow`: **deixar vazio nos três.** O `Pós-ligação v3` não serve aqui — ele é
disparado por **mudança do campo** `Resultado da tentativa`, e entrar por gatilho com o
campo vazio cai no ramo `Resultado vazio? → SIM`, que não faz nada. Isto foi lido no
roteiro publicado, não suposto.

### Dois ajustes na tela `Fila de ligações` (a que o SDR usa)

1. **`TOQUE MÁX. (s)` está em 5.** A recomendação continua **30**: com 5 s a maioria dos
   leads nem vê o celular tocar, e a chamada perdida — o retorno mais barato do funil —
   não acontece. Os 5 s são o padrão da aba `Disparo` (robô), não da fila humana.
2. **O campo de tag mostra `fila-tel`** (0 contatos com telefone, 1 sem). `fila-tel` é uma
   tag que os workflows publicados **removem** (`Pós-ligação v3`, nó `-TAG fila-tel,
   fila-wa, fila-quente`), não uma que alguém aplica — por isso está vazia. A fila do SDR é
   **`fila-sdr`**, mantida pelo atuador. A caixa de contatos já está com os 5 certos
   (Gerson, Ana Ruth, Ricardo, Andreia…), então o `Puxar` da `fila-sdr` funcionou; só não
   digitar `fila-tel` de novo amanhã.

---

## Retificação de 27/09 19:30 — `fila-tel` É a fila desenhada; `fila-sdr` é o reservatório

Pente fino nos 33 roteiros publicados (dumps em `auditoria-roteiros`, cruzando quem
põe e quem lê cada tag) mostrou o que eu não tinha visto ao criar a `fila-sdr`:

- **As cadências põem `fila-tel` a cada toque** (Cadência 12x30 em 6 nós, parte 2 em 6,
  Inbound também), junto com a tarefa "[CADENCIA] Tn · Ligar…".
- **O `Pós-ligação v3` tira `fila-tel` em todo ramo** (Atendeu, Não atendeu, Caixa
  Postal, Pediu retorno, Número errado, Não ligar, Desqualificado — 6 nós `-TAG`).
- **O `Fila Travada` vigia `fila-tel`**: se a tag ficar 8 h sem resultado, avisa o
  gestor e põe `fila-travada`.

Ou seja: **`fila-tel` = "leads com toque de ligação pendente agora"**, mantida pelos
próprios workflows, no ritmo da cadência 12x30. É exatamente o que o discador deve
puxar — e é o que o dono digitou na tela (estava com 0 porque a T1 do lote 1 ainda
não disparou; dispara quando o lead entra em CONECTAR ou ganha `cad-outbound`, e as
cadências põem `Prioridade = 3` sozinhas).

**Corrijo a instrução da rotina:** o SDR puxa **`fila-tel`**. Se vier vazia (nenhum
toque vencido naquela hora), aí puxa **`fila-sdr`**, que é o reservatório de discáveis
(CONECTAR, Prioridade ≥ 3, sem DND) mantido pelo atuador — útil no primeiro dia e em
dia de fila curta, mas fora do ritmo da cadência. O adendo das 16:40 dizia "tag
`fila-sdr`, não `fila-tel`"; estava errado, e a razão é a lição 2.16: eu não tinha lido
o roteiro que executa. `fila-closer` continua valendo (nenhum workflow a toca).

### Outros achados do cruzamento (nenhum é defeito, todos ficam registrados)

| tag/campo | situação | leitura |
|---|---|---|
| `pausado` | lida por 4 workflows, nunca posta por workflow | tag **manual** de pausa do gestor; `Mestre de saída` a tira. Por desenho |
| `reengajamento-ativo` | lida como guarda em Cadência 12x30, nunca posta | guarda sobressalente; `cad-inbound` cobre o caso real |
| `fila-wa` | lida e removida, nunca posta | fila de ligação por WhatsApp, indisponível nesta conta (CANAIS.md) |
| `fila-quente` | posta por Inbound e pelas Interceptações de Sinal, tirada pelo Pós-ligação | funciona |
| `limpar-tarefas` | posta pelas cadências, lida por ninguém | higiene manual (`rotina-limpar-tarefas.md`); não bloqueia nada |
| `Toques na semana` | escrita só pelo `Contador de Toques` (gatilho: tag `toque`) | teto de 6/semana funciona |
| valores de `Investimento mensal` nas condições | `Até 1k / 1k a 5k / 5k a 10k / Acima de 10k` | o Meta grava `Abaixo de 5k`, `Até R$ 1.000`, `Não invisto nada ainda` → nota 0 nesse bloco para lead do anúncio (G-04, decisão do dono pendente) |

## Decisão do dono, 27/09 21:30 — só `fila-tel`, puxada em horários fixos

A SDR **não usa `fila-sdr`**. No Power (`Fila de ligações`, nunca `Disparo`) ela puxa
sempre `fila-tel`, que as cadências põem quando o toque vence e o `Pós-ligação v3` tira
quando o resultado é marcado — por isso ela junta atrasados e atuais e respeita a 12x30.
Puxadas: **08:40, 11:00, 14:00, 16:30**. Lead novo não espera puxada: o Speed-to-lead
avisa e a SDR liga pela ficha. `fila-sdr` continua existindo (nada apagado), fora da rotina.

**Só na terça 29/09:** a `fila-tel` vem vazia até ~10:05, porque o primeiro toque da
Cadência Inbound vence 1 dia + ~1 h35 depois da MI-0 de segunda 08:30.
