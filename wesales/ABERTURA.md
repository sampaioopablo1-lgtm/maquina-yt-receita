# ABERTURA.md — a abertura da operação e o que fazer com os 30 leads inbound

Decisão tomada em 27/09/2026 sobre duas perguntas que estavam abertas: **em
que dia a operação abre** (segunda 28/09 ou terça 29/09) e **o que aplicar
nos 30 leads de inbound do formulário do Meta Ads** — em particular, se
algum deles leva DND.

Este documento é o roteiro da abertura. Ele não substitui o
`build-wesales.md` (que é a especificação nó a nó) nem o
`ROADMAP-SALES-ENGAGEMENT.md` (que é o backlog): ele diz só a ordem das
ações da abertura, e por quê.

---

## 1. Decisão — abertura na terça 29/09/2026

A data não é preferência, está codificada em dois lugares:

- `wesales/tools/promote_g03_scheduled.py` — portão de tempo rígido,
  `WINDOW_START = 2026-09-29 08:00` e `WINDOW_END = 2026-09-30 08:00`
  (`America/Sao_Paulo`). Fora da janela o runner imprime `outside scheduled
  window; no CRM writes` e sai sem tocar no CRM.
- `.github/workflows/wesales-g03.yml` — `cron: "0 11 * * *"` (= 08:00 SP),
  diário desde já, mas inofensivo até a janela abrir.

**Por que não segunda 28/09:** o runner acorda às 08:00 e não faz nada.
Abrir na segunda significa ou promover o estoque de `NOVO LEAD` na mão, ou
editar `WINDOW_START` na manhã da abertura — mexer no portão de tempo no dia
D, no único componente que escreve no CRM. Ganha um dia e paga com uma
alteração não revisada.

**E há trabalho de verdade para a segunda** (seção 3): a tag de origem dos
30 leads tem que estar aplicada *antes* da promoção de terça, senão eles
caem na régua errada e não há volta. Segunda é o dia de preparar, terça é o
dia de abrir.

---

## 2. Decisão — nenhum DND nos 30 leads

Os 30 são inbound: preencheram formulário do Meta Ads. **Pediram contato.**
É o oposto do que aciona DND nesta operação, que liga DND em exatamente dois
lugares:

- ramo `Não ligar` do Pós-ligação (`build-wesales.md`, seção 4) — depois de
  o SDR classificar uma **ligação de telefone**;
- workflow "Opt-out por Palavra-chave" (seção 2.9.5) — quando o **texto** da
  resposta bate na lista canônica de frases.

Nenhum dos 30 passou por nenhum dos dois. E DND aqui não é um erro
recuperável: o próprio documento registra que o DND nativo é **permanente
por desenho** (seções 4 e "Pausa individual"), que nenhuma automação o
desfaz, que nenhuma lista mostra "DND aplicado hoje" e que, por isso, DND
errado não se descobre — só se descobre o lead que nunca mais respondeu.
Aplicar em massa em 30 leads pagos é o erro mais caro disponível na tela.

**O que aplicar em vez disso:** a tag **`cad-inbound`**, que é o registro de
origem do lead e o que o manda para a **Cadência Inbound** (seção 2.10) —
régua de 5 min / 30 min / 2h / 1 dia / 3 dias, em `Wait → Time Delay`
relativo à entrada, desenhada exatamente para formulário respondido.

Opt-out continua coberto, lead por lead, pelos dois nós acima, no dia em que
um deles de fato pedir para parar.

Para referência, o que **não** é DND (e já tem lugar próprio):

| Situação | Tratamento correto |
|---|---|
| Telefone ruim | tag `telefone-invalido` (portão de higiene, seção 2.3) |
| 12 tentativas esgotadas sem conexão | `status = abandoned` + tag `nutricao-90d`, **sem sair de `CONECTAR`** |
| "me procura mês que vem" | tag `pausado` (T-14) — `nao-perturbe` seria overkill e ligaria o DND |
| Pediu para parar, por ligação ou por texto | aí sim: `nao-perturbe` + DND + `status = lost` |

---

## 3. O problema de ordem — por que a tag vem antes da promoção

**Nada na máquina aplica `cad-inbound` hoje.** A Porta de Entrada (seção
1.3) é de nó único: cria a oportunidade em `NOVO LEAD` e nada mais, sem tag
de origem. O próprio documento registra por que `Tag Added` foi descartado
como gatilho: "dependeria de alguém aplicar a tag primeiro, o que nenhum
fluxo hoje faz na entrada".

As duas cadências disputam o **mesmo evento**, separadas só por essa tag:

| Workflow | Gatilho | Filtro | Régua |
|---|---|---|---|
| Cadência 12x30 (seção 2.1) | `Opportunity Stage Changed` → `CONECTAR` | `cad-inbound` **ausente** | dias |
| Cadência Inbound (seção 2.10) | `Opportunity Stage Changed` → `CONECTAR` | `cad-inbound` **presente** | minutos |

E o runner do G-03 promove para `CONECTAR` tudo que estiver `open` em `NOVO
LEAD`.

**Logo:** se os 30 chegarem em terça sem a tag, a promoção das 08:00 os joga
na régua **outbound, medida em dias**. E não dá para consertar depois — o
gatilho é mudança de etapa, eles já estarão em `CONECTAR`, e a Cadência
Inbound tem `Allow Re-entry` desligado. Marcar a tag depois não gera evento
novo. Os 5 minutos de SLA que a seção 2.10 existe para ganhar viram 1 hora,
para leads que o anúncio já pagou.

Ressalva, para não confundir dois limites diferentes: aplicar a tag por ação
em massa não dispara `Contact Created` (proteção nativa da HighLevel contra
automação em massa acidental), e isso aqui **não importa** — a Porta de
Entrada já criou a oportunidade desses leads, e o gatilho que decide o ramo
é a mudança de etapa de terça, não a tag.

---

## 4. Roteiro da abertura

### Segunda 28/09 — preparar, sem escrever no funil

- [ ] Aplicar `cad-inbound` nos 30 leads de inbound (ação nativa em massa em
      Contatos). **Nenhum DND, nenhum `nao-perturbe`.**
- [ ] Conferir que os 30 estão `open` em `NOVO LEAD` — quem estiver
      `abandoned` ou `lost` o runner ignora de propósito, e isso está certo.
- [ ] Conferir que a **Cadência Inbound** está publicada e testada. A regra
      do G-03 ("não promover estoque antes da cadência publicada e testada")
      vale para a Inbound aqui, não só para a 12x30 — é ela que vai receber
      esses 30.
- [ ] Conferir que o secret `GHL_PIT` está configurado no repositório.
- [ ] Não executar o runner na mão. Ele é inerte até 29/09 08:00; forçar
      antes disso exigiria mexer no portão de tempo.

### Terça 29/09, 08:00 (`America/Sao_Paulo`) — abrir

- [ ] O runner promove `NOVO LEAD` → `CONECTAR`.
- [ ] Os 30 caem na Cadência Inbound; a T1 sai em 5 minutos dentro da janela
      08:30–18:30.

### Terça, depois da T1 — conferir

- [ ] Quantos entraram na Cadência Inbound e quantos vazaram para a 12x30.
      Qualquer vazamento é tag que faltou na segunda.
- [ ] Log do runner: `queried`, `promoted`, `skipped_non_open`.
- [ ] Tarefas `[CADENCIA]` geradas, e o portão de higiene de telefone
      barrando quem não tem telefone válido.

---

## 5. Dois pontos do runner a saber antes de terça

Achados ao ler `promote_g03_scheduled.py` para escrever este documento.
Nenhum dos dois é motivo para adiar — os dois são motivo para não se
surpreender.

**O marcador de idempotência não sobrevive ao CI.** `MARKER_FILE` aponta
para `wesales/.local/g03-run.json`, escrito no checkout efêmero do GitHub
Actions. A proteção "já rodou" só funciona na execução local do PC; no CI,
cada corrida começa sem marcador.

**A borda de 30/09 é sorte, não desenho.** `WINDOW_END` é 30/09 às 08:00 e a
comparação é inclusiva, então a corrida de 30/09 cai exatamente na borda:
com o atraso normal do scheduler do GitHub ela provavelmente fica de fora,
mas isso não está garantido. O efeito de uma segunda execução é idempotente
(`PUT` para `CONECTAR` no que ainda estiver em `NOVO LEAD`), então não é
perda — é ruído fora do nosso controle. Se incomodar, fechar a janela em
29/09 23:59 resolve, mas é mudança de código e não deve ser feita na véspera.

**A limpeza de tarefas é só relatório** (`count_overdue_tasks`), porque a API
pública não oferece endpoint normal de atualização/conclusão de tarefas. A
higiene de tarefas segue manual na abertura — ver `rotina-limpar-tarefas.md`.
