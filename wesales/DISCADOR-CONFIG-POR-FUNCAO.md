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
