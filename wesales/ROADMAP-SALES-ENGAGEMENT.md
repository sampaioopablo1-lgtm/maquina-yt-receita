# O que falta para virar Reev/Meetime de verdade

O alvo do projeto não é "ter uma cadência no GHL". É chegar o mais perto
possível de uma plataforma de sales engagement usando recursos nativos. Este
arquivo é a distância que falta, medida e priorizada.

**É o backlog que a rotina horária trabalha.** Um item por execução, de cima
para baixo, respeitando o `APROVADO.md`.

## O que já está desenhado

Cadência multicanal de 12 tentativas, filas por tag em listas inteligentes,
régua de qualificação com nota, roteamento por resultado, saída limpa, rotina
de higiene de tarefas. Isso é o **motor**.

O que falta abaixo é quase tudo **instrumentação e cadências vizinhas** — que
é justamente onde Reev e Meetime ganham de um CRM configurado na mão.

---

## Bloco 1 — Medição (a maior lacuna)

Hoje a máquina executa e não se mede. Um SDR sem medição é um SDR com opinião.

### R-01 · Métricas de cadência por tentativa e por canal
**Por quê:** a pergunta que paga a operação é "a T7 ainda vale a pena?". Sem
taxa de conexão por tentativa, a cadência de 12 é fé, não desenho.
**Como:** campos contadores por canal (`Tentativas telefone`,
`Tentativas WhatsApp`, `Conexões telefone`, `Conexões WhatsApp`) alimentados
pelo Pós-ligação, e listas inteligentes agrupando por `Tentativa nº`.
**Pronto quando:** dá para responder "qual tentativa conecta mais" sem planilha.

### R-02 · Speed-to-lead
**Por quê:** é a métrica nº 1 de inbound na literatura de vendas, e a que mais
move conversão. Ninguém mede porque ninguém guarda o par de horários.
**Como:** campo `Data de entrada` (preenchido na criação) e
`Data da 1ª tentativa`. A diferença é a métrica.
**Pronto quando:** existe lista "leads com mais de 1h sem primeira tentativa".

### R-03 · Funil do SDR por período
**Por quê:** entraram / conectaram / agendaram / compareceram é o funil que o
gestor olha. Hoje só existe o estado atual, não o fluxo.
**Como:** campos de data por marco (`Data conectado`, `Data agendado`,
`Data compareceu`) + listas filtradas por período.
**Pronto quando:** dá para dizer a taxa de conexão do mês sem contar na mão.

---

## Bloco 2 — Conteúdo que se mede

### R-04 · Biblioteca de mensagens versionada
**Por quê:** em Reev/Meetime o template é objeto de primeira classe, com
desempenho próprio. Aqui as mensagens estão soltas dentro do workflow.
**Como:** campo `Template usado` preenchido junto com cada envio, e os textos
num documento versionado com código (`M1-a`, `M1-b`, `M2-a`...).
**Pronto quando:** dá para dizer qual abertura teve mais resposta.

### R-05 · Teste A/B da abertura
**Por quê:** a M1 decide se existe cadência. É o único texto que merece teste.
**Como:** If/Else alternando duas versões da M1 e gravando qual em
`Template usado`.
**Pronto quando:** duas versões rodando e a comparação sai da lista inteligente.

### R-06 · Script de ligação e playbook de objeções
**Por quê:** o SDR liga 100 vezes por dia. Sem script, cada ligação é
improviso, e o que funciona não vira repertório do time.
**Como:** documento com abertura, pergunta de diagnóstico, ponte para o
agendamento e as 8 objeções mais comuns com respostas.
**Pronto quando:** um SDR novo liga no segundo dia.

---

## Bloco 3 — Cadências vizinhas

### R-07 · Cadência inbound (lacuna L-04)
**Por quê:** as tags `cad-inbound`/`cad-outbound` existem e só há cadência
outbound. Inbound com cadência de 30 dias é lead perdido: a régua é em minutos.
**Como:** cadência própria — tentativa em 5 min, 30 min, 2h, 1 dia, 3 dias.
**Pronto quando:** formulário preenchido dispara ligação em minutos.

### R-08 · Reengajamento dos 90 dias
**Por quê:** `nutricao-90d` marca a saída e nada traz de volta. Nutrição sem
retorno é arquivo morto.
**Como:** workflow que, aos 90 dias, devolve para `Novo lead` com tag
`cad-outbound` e uma abertura diferente da primeira rodada.
**Pronto quando:** o lead de hoje volta à fila em dezembro, sozinho.

### R-09 · Regras de pausa
**Por quê:** cadência que dispara em feriado ou com o SDR de férias queima
lead e credibilidade.
**Como:** tag `pausado` checada no portão, e calendário de feriados na janela
do workflow.
**Pronto quando:** o Natal não gera 120 tarefas.

---

## Bloco 4 — Operação com mais de um SDR

### R-10 · Distribuição de leads
**Por quê:** o desenho atual assume um SDR. No segundo, sem regra, os dois
ligam para o mesmo lead.
**Como:** round robin na atribuição da tarefa + campo `SDR responsável`, com
as listas inteligentes filtrando por usuário logado.
**Pronto quando:** dois SDRs trabalham sem colidir.

### R-11 · Alerta de capacidade (lacuna L-05)
**Por quê:** 10 leads/dia × 12 tentativas dá ~120 tarefas/dia em regime, acima
da meta de 100. A fila estoura silenciosamente.
**Como:** lista inteligente de tarefas abertas do dia + notificação ao gestor
acima do limite.
**Pronto quando:** o gestor sabe da fila cheia antes do SDR desistir dela.

### R-12 · Handoff e no-show
**Por quê:** reunião agendada que não acontece é o vazamento mais caro do
funil, e hoje o desenho termina no agendamento.
**Como:** gatilho de status `No-show` → volta para cadência com régua curta;
SLA do closer para dar retorno.
**Pronto quando:** no-show vira nova tentativa, não silêncio.

---

## Bloco 5 — Qualidade e confiança

### R-13 · Higiene de base
**Por quê:** base suja infla métrica e queima SDR. A subconta bloqueia
duplicata por e-mail e telefone, o que ajuda, mas não cobre número inválido
nem lead sem telefone.
**Como:** lista inteligente de contatos sem telefone válido; rotina de
marcação, nunca de exclusão.
**Pronto quando:** a fila do SDR não tem lead impossível de ligar.

### R-14 · Auditoria de compliance
**Por quê:** `nao-perturbe` e DND são a linha entre prospecção e perseguição.
Precisa ser verificável, não confiável.
**Como:** rotina que confere se algum contato com DND recebeu mensagem, e se
algum envio saiu fora da janela.
**Pronto quando:** existe relatório que prova que ninguém foi incomodado
indevidamente.

### R-15 · Dashboard do gestor
**Por quê:** todo o resto acima morre se depender de alguém abrir seis listas.
**Como:** dashboard nativo com ligações/dia, conexões/dia, agendamentos,
taxa por tentativa, fila em atraso.
**Pronto quando:** o gestor abre uma tela e sabe se o dia foi bom.

---

## Ordem sugerida

Medição primeiro (R-01, R-02, R-03), porque sem ela as decisões seguintes são
chute. Depois conteúdo (R-04, R-05, R-06), que é o que mais move resultado por
hora investida. Só então as cadências vizinhas e a operação com mais gente.

R-14 sobe para o topo no dia em que a operação começar a mandar mensagem de
verdade. Antes disso, não há a quem incomodar.
