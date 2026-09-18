# O que falta para virar Reev/Meetime de verdade

O alvo do projeto não é "ter uma cadência no GHL". Os blocos 1 a 5 são a
distância até a **paridade** com Reev e Meetime — e paridade é o **piso**, não
a chegada. O bloco 6 é o que faz a operação ficar fora da curva: coisas que a
maioria das operações de SDR não faz, e que nem as plataformas de prateleira
entregam bem.

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

### R-01 · Métricas de cadência por tentativa e por canal — **FEITO em 18/09/2026**
**Por quê:** a pergunta que paga a operação é "a T7 ainda vale a pena?". Sem
taxa de conexão por tentativa, a cadência de 12 é fé, não desenho.
**Como:** campos contadores por canal (`Tentativas telefone`,
`Tentativas WhatsApp`, `Conexões telefone`, `Conexões WhatsApp`) alimentados
pelo Pós-ligação, e listas inteligentes agrupando por `Tentativa nº`.
**Pronto quando:** dá para responder "qual tentativa conecta mais" sem planilha.

**Resumo:** campos C-09 a C-12 especificados em `campos-e-tags.md`, nós do
Pós-ligação atualizados em `build-wesales.md` (seção 4) e lista inteligente
`Conexão por Tentativa` criada (seção 8.6) — falta só a criação manual dos 4
campos na tela (a subconta segue com 0 campos e 0 contatos, confirmado por
`locations_get-custom-fields`/`contacts_get-contacts` nesta execução).

### R-02 · Speed-to-lead — **FEITO em 18/09/2026**
**Por quê:** é a métrica nº 1 de inbound na literatura de vendas, e a que mais
move conversão. Ninguém mede porque ninguém guarda o par de horários.
**Como:** carimbos `Entrada em` e `1ª tentativa em`, ambos **`TEXT` no formato
`AAAA-MM-DD HH:MM`** — e não `DATE`. Medido em 18/09/2026: campo `DATE` do GHL
descarta a hora, e speed-to-lead medido em minutos entre duas datas sem hora dá
zero no mesmo dia. A diferença entre os dois carimbos é a métrica.
**Pronto quando:** existe lista "leads com mais de 1h sem primeira tentativa".

**Resumo:** campos C-18/C-19 especificados em `campos-e-tags.md`; nó 0.6 e o
par 5c/5d (só na T1) especificados em `build-wesales.md` (seção 2.4); como
campo `TEXT` não aceita filtro relativo de data em lista inteligente, o "mais
de 1h" saiu de um workflow-relógio, não de um filtro — `Alerta de
Speed-to-lead` (seção 2.11) espera 1h e marca a tag `atraso-1a-tentativa`, que
a lista `Atraso na 1ª Tentativa` (8.8) só lê. **Falta a criação
manual dos 2 campos (campo personalizado não sai por API) e a aprovação da
tag nova em `APROVADO.md`** — ela é a 12ª, fora do lote das 11 já autorizadas
por nome; ficou com linha própria, ainda `[ ]`. Subconta reconfirmada nesta
execução via `locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: segue em 0 campos, 0 contatos, só o
`FUNIL DE VENDAS` pré-existente — nada mudou desde a auditoria.

### R-03 · Funil do SDR por período — **FEITO em 18/09/2026**
**Por quê:** entraram / conectaram / agendaram / compareceram é o funil que o
gestor olha. Hoje só existe o estado atual, não o fluxo.
**Como:** campos de data por marco (`Data conectado`, `Data agendado`,
`Data compareceu`) + listas filtradas por período.
**Pronto quando:** dá para dizer a taxa de conexão do mês sem contar na mão.

**Resumo:** campos C-20 a C-22 especificados em `campos-e-tags.md`; nó novo
no ramo `Atendeu` do Pós-ligação (seção 4) e no Pós-agendamento (seção 5)
grava `Data conectado`/`Data agendado`; workflow novo `Registro de
Comparecimento` (seção 5.2) grava `Data compareceu` a partir do status
`Showed` do calendário. Pesquisado antes de desenhar: o filtro nativo do GHL
`Last Stage Change Date` só reflete a etapa atual e subcontaria quem já
avançou — carimbo próprio por marco não tem esse defeito. O quarto marco,
"entraram" (lista 8.9), não ganhou campo novo: usa o `Data de criação`
nativo da oportunidade, que também não muda com o avanço de etapa. As
quatro listas (8.9 a 8.12) ficam em `build-wesales.md`, seção 8. Falta só a
criação manual dos 3 campos na tela — campo personalizado não sai por API;
subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente.

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

## Bloco 6 — fora da curva

Aqui não é paridade. É o que separa uma operação boa de uma operação que os
concorrentes não conseguem copiar olhando de fora.

### F-01 · Cadência que reage a sinal, não só a calendário — **FEITO em 18/09/2026**
**Por quê:** uma régua por dia trata igual quem abriu a mensagem três vezes e
quem nunca viu. O lead **dá sinal** — clica, responde, volta ao site — e a
cadência segue no D7 como se nada tivesse acontecido. É o desperdício mais caro
de qualquer operação de prospecção.
**Como:** link de gatilho nas mensagens; `Trigger Link Clicked` e
`Customer Replied` como gatilhos de um workflow de interceptação que põe
`Prioridade` = 5, aplica `fila-quente` e cria tarefa para agora, furando a fila
do dia.
**Pronto quando:** lead que clicou às 14h é ligado às 14h10, não no D7.

**Resumo:** seção 2.9 do `build-wesales.md` especifica o Trigger Link
`Agendar com o closer` embutido em M2/M3 e os dois workflows curtos
("— Clique" e "— Resposta") que fazem a interceptação; campos C-13/C-14
especificados em `campos-e-tags.md` — falta só a criação manual (Trigger Link
e campos não saem por API; a subconta segue com 0 campos e 0 contatos,
reconfirmado nesta execução via `locations_get-custom-fields`/
`contacts_get-contacts`).

### F-02 · Melhor horário aprendido, por segmento
**Por quê:** a tabela de horários das 12 tentativas é a mesma para todo mundo.
Mas dentista atende às 14h e obra atende às 7h. A operação descobre isso depois
de trezentas ligações — e não usa.
**Como:** gravar `Hora da conexão` sempre que o resultado for `Atendeu`;
comparar por `Segmento`; ajustar os horários das tentativas por faixa.
**Pronto quando:** o horário da T3 de um segmento é diferente do de outro, e a
diferença veio de evidência, não de palpite.

### F-03 · Loop do closer de volta para o SDR — **FEITO em 18/09/2026**
**Por quê:** este é o defeito mais comum e mais caro em pré-vendas. O SDR
agenda e **nunca descobre se agendou bem**. Sem isso, a nota de qualificação
nunca se calibra: ela é uma opinião que ninguém conferiu.
**Como:** campos `Reunião foi qualificada` (Sim / Não / Parcial) e
`Motivo da desqualificação`, preenchidos pelo closer no pós-reunião; relatório
cruzando a nota que o SDR deu com o veredito do closer.
**Pronto quando:** dá para dizer "nota ≥ 70 acerta X%" — e corrigir a régua da
seção 9 com dado, não com achismo.

**Resumo:** campos C-15 a C-17 especificados em `campos-e-tags.md`; workflow
`Loop do closer` especificado em `build-wesales.md` (seção 5.1), roteando por
veredito e motivo para `Nutrição`/`Descartado` sem tocar em `FUNIL DE VENDAS`;
lista inteligente `Calibração da Régua` criada (seção 8.7). Diferencial sobre
Reev/Meetime/Outreach/Salesloft, que fecham este loop só em relatório
agregado: dois nós de alerta em tempo real (nota ≥ 70 com veredito `Não`, ou
nota < 45 com veredito `Sim`) avisam o gestor no dia da reunião, não no
relatório do mês. Falta só a criação manual dos 3 campos na tela — campo
personalizado não sai por API; subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente.

### F-04 · Teto de toques por semana
**Por quê:** lead em duas cadências recebe o dobro de toques, e ninguém percebe
até o opt-out chegar. Frequência é o que transforma prospecção em perseguição.
**Como:** campo `Toques na semana`, incrementado a cada envio e cada ligação,
zerado semanalmente, checado no portão de toda tentativa.
**Pronto quando:** nenhum lead recebe mais que N toques por semana, venha de
onde vier.

### F-05 · Monitor de saúde da operação
**Por quê:** automação falha **em silêncio**. Tag que não saiu, lead parado numa
etapa, workflow que parou de disparar — descobre-se pelo número caindo, semanas
depois, quando o estrago já aconteceu.
**Como:** rotina que confere invariantes e denuncia violação: contato com
`fila-tel` há mais de 24h, lead em `Em cadência` sem tentativa há 7 dias, tarefa
vencida sem resultado, contato com `nao-perturbe` ainda dentro de workflow ativo.
**Pronto quando:** a operação avisa que quebrou antes de o gestor perguntar.

### F-06 · Qualidade da conexão, não a contagem
**Por quê:** `Atendeu` empacota na mesma célula a ligação de 8 segundos e a de 8
minutos. A métrica que importa não é alô, é conversa.
**Como:** duração da ligação vinda do call tracking; campo `Conexão real` = 
atendeu **e** durou mais de 60s. A taxa de conexão do relatório passa a usar
esse campo.
**Pronto quando:** "taxa de conexão" no relatório significa conversa, e o SDR
não consegue inflar o número desligando rápido.

---

## Ordem sugerida

Medição primeiro (R-01, R-02, R-03), porque sem ela as decisões seguintes são
chute. Depois conteúdo (R-04, R-05, R-06), que é o que mais move resultado por
hora investida. Só então as cadências vizinhas e a operação com mais gente.

R-14 sobe para o topo no dia em que a operação começar a mandar mensagem de
verdade. Antes disso, não há a quem incomodar.

F-01 e F-03 já saíram do bloco 6 fora da ordem normal, cada um na rodada em
que foi feito: sinal ignorado e nota não calibrada são dívidas que não se
pagam retroativamente — os dados que faltaram não voltam, calendário nenhum
devolve. Nenhum item do bloco 6 pede prioridade fora da ordem agora: os quatro
que restam pedem volume para fazer sentido. F-02 precisa de conexões
suficientes para ter padrão; F-06 precisa de call tracking ligado; F-04 e F-05
só mordem quando há mais de uma cadência no ar.

A ordem normal retoma: R-03 fecha o bloco 1 de medição, e só então o bloco 2
(conteúdo) entra na fila.
