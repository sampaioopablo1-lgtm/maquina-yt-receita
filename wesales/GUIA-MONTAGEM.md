# Guia de montagem manual — passo a passo

Documento vivo. Cada fase é ensinada em detalhe **na hora em que chega a
vez dela** — não adianta ler a fase 5 antes de terminar a 1, porque cada
uma referencia o que a anterior criou. Marque `[x]` conforme for fazendo;
é o jeito de saber, numa olhada, onde a montagem manual parou (a rotina
automática só mexe em tag/contato/oportunidade via API — o que está aqui é
só o que exige clique na tela).

Fonte de toda a especificação: `build-wesales.md`. Este guia não repete o
conteúdo dele — só organiza a ordem e detalha o clique que o outro
documento não detalha.

## Visão geral das fases

- [ ] **Fase 1 — Pipeline "Pré-vendas"** (7 etapas) — abaixo, pronta para seguir agora
- [ ] **Fase 2 — Campos personalizados** (~24 campos)
- [ ] **Fase 3 — Calendário do closer + formulário de qualificação**
- [ ] **Fase 4 — Trigger Link "Agendar com o closer"**
- [ ] **Fase 5 — Os ~14 workflows**, na ordem da seção "Ordem de montagem" do `build-wesales.md`
- [ ] **Fase 6 — Listas inteligentes** (~18)
- [ ] **Fase 7 — Teste com os 5 contatos fictícios** (já existem no CRM, seção 10)
- [ ] **Fase 8 — Pausar Workflows em Datas Específicas** (feriados/férias)
- [ ] **Fase 9 — Number Validation** (opcional)
- [ ] **Fase 10 — Dashboard + Custom Metrics**

---

## Fase 1 — Pipeline "Pré-vendas"

### Onde clicar

No menu lateral da WeSales: **Oportunidades** → ícone de engrenagem
**Configurações** (canto superior direito da tela de Oportunidades) →
**Pipelines** → botão **Adicionar pipeline** (ou "+ Add Pipeline").

### O que preencher

**Nome do pipeline:** `Pré-vendas`

**Etapas, nesta ordem exata** (clique em "Adicionar etapa" 7 vezes, uma
para cada linha, respeitando a ordem — a ordem decide a posição na tela):

| Ordem | Nome da etapa (copie exatamente) |
|---|---|
| 1 | `Novo lead` |
| 2 | `Em cadência` |
| 3 | `Conectado` |
| 4 | `Retorno agendado` |
| 5 | `Reunião agendada` |
| 6 | `Nutrição` |
| 7 | `Descartado` |

**Probabilidade de ganho por etapa:** não se preocupe em acertar um número
"certo" aqui. Esse pipeline não tem etapa de "Ganho" — o fechamento de
verdade acontece no `FUNIL DE VENDAS` que já existe na subconta, depois
que o closer assume. Use uma progressão simples só para não deixar em
branco (ex.: 5, 15, 30, 35, 50, 10, 0 — repare que `Nutrição` é mais baixa
que `Reunião agendada`, não mais alta, porque nutrição é "ainda não",
não "quase lá"). **Não copie o padrão do `FUNIL DE VENDAS` existente**: a
auditoria já achou que ele tem uma progressão automática de 6,67% em linha
reta que deixa "Não tem interesse" com 93% de chance de ganho — é um bug
de configuração daquele pipeline, não um padrão a repetir aqui.

### Configurações do pipeline (mesma tela, ou em "Editar pipeline" depois)

- **Visibilidade:** restrinja a quem faz parte da operação (SDR, closer,
  gestor) — não deixe visível para o restante da equipe da WeSales.
- **Nome da oportunidade:** deixe no padrão (nome do contato).
- Confirme que **`Novo lead`** é a etapa marcada como entrada padrão para
  qualquer formulário ou importação que crie oportunidade neste pipeline.

### Por que estas 7 e não menos

Se você (ou quem for montar) ficar tentado a simplificar para 4-5 etapas
(o funil genérico de Inside Sales tem menos): **não simplifique**.
`Em cadência` precisa ser uma etapa própria porque é ela que todo
workflow da cadência consulta antes de disparar uma tentativa — sem essa
etapa exata, o mecanismo de segurança da máquina inteira não tem o que
checar. O raciocínio completo, etapa por etapa (objetivo, quando avança,
o que a bloqueia, taxa esperada), está em `build-wesales.md`, seção 1.1 e
1.2 — vale a leitura se quiser entender o "porquê" de cada uma antes de
criar.

### Como saber que terminou certo

- [ ] Pipeline `Pré-vendas` existe, com as 7 etapas na ordem acima
- [ ] `FUNIL DE VENDAS` (o pipeline que já existia) **não foi tocado** —
      confira que ele continua com as mesmas 14 etapas de antes
- [ ] Visibilidade restrita configurada

Quando terminar esta fase, me avise (ou só siga para a próxima conversa) —
eu confirmo lendo o pipeline pelo conector (`opportunities_get-pipelines`)
e ensino a Fase 2 (campos personalizados) em seguida, com a lista pronta
para copiar direto de `campos-e-tags.md`.
