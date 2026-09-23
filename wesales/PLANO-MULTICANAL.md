# Plano — funil com REUNIÃO DE DIAGNÓSTICO + cadências multicanais

Decidido pelo dono em 22/09/2026 ("aplique todas as recomendações … ajuste de
ponta a ponta"). Este arquivo é o **estado da obra**: se a sessão cair, retome
pela lista de execução no fim.

## Decisões (todas do dono, 22/09/2026)

| # | Decisão |
|---|---|
| D1 | Etapa `AGENDAR` (id `3d26fcd1-220d-49ed-8325-705dfe9055b1`) é **renomeada para `REUNIÃO DE DIAGNÓSTICO`**. Mesmo id. |
| D2 | `CONECTAR` tem um objetivo único: **conectar + qualificar (formulário do closer) + agendar**. O lead só sai de `CONECTAR` com reunião marcada (ou por perda/nutrição). |
| D3 | `Atendeu` **não move mais de etapa**. O lead fica em `CONECTAR` na fase **"fechar horário"** (poucos toques, mais próximos) até agendar. |
| D4 | Reunião marcada → `REUNIÃO DE DIAGNÓSTICO`. O **closer** move para `NEGOCIAR` quando apresenta a proposta. |
| D5 | Canais da cadência: ligação pelo **WhatsApp dentro do GHL (Stevo Voice, botão "Ligar via WhatsApp")**, ligação normal pelo GHL, e **mensagem de WhatsApp automática** (Stevo = ação "SMS" do GHL). **Sem e-mail** por enquanto. |
| D6 | **WhatsApp primeiro** em todo toque, ligação normal como segunda tentativa. Com **3 ligações de WhatsApp seguidas não atendidas**, o lead passa a ter a ligação normal primeiro (protege o número). |
| D7 | **Cadência Inbound** curta e intensa (24–48 h), multicanal, e depois a 12x30. |
| D8 | Qualificar por texto é permitido quando o lead insiste; o SDR sempre tenta a ligação primeiro. |
| D9 | O resultado de cada toque decide a próxima tarefa: **mantida** (Não atendeu / Caixa Postal / vazio), **reagendada** (Pediu retorno → a cadência pausa até a data do retorno) ou **excluída** (Atendeu com reunião, Não ligar, Número errado, Desqualificado). |
| D10 | Campo novo **`Canal que conectou`** (Ligação WhatsApp / Ligação normal / Mensagem), marcado junto com o resultado. ⚠️ **O campo existe e ninguém escreve nele** — medido em 23/09 03:50, o id `TxJmoWdkA8rTqC1uEsMW` não aparece em nenhum dos 33 dumps. O "marcado junto com o resultado" não foi montado: o `Pós-ligação v2` grava `Resultado da tentativa` e não grava este. Sem isso a D6 (WhatsApp primeiro, ligação normal na segunda) fica sem dado para ser avaliada — dá para dizer que trocou de canal, não qual funcionou. Seção 2.34 do `build-wesales.md`. |
| D12 | **Faxina de Tarefas:** tarefa AUTOMÁTICA aberta que perdeu o contexto (etapa/status/resultado) é **excluída**, com nota no contato; concluída e manual nunca são tocadas. Roda de graça no GitHub Actions (repo público), a cada 10 min em horário comercial. Script: `tools/faxina_tarefas.py` (17 casos testados). |
| D13 | **Nenhuma tarefa nasce no fim de semana.** Todo workflow que cria tarefa tem janela seg–sex 08:30–18:30 (inclusive Interceptação de Sinal, Pós-ligação e No-show). |
| D14 | **Capacidade do SDR:** no máximo **100 ligações/dia** (WhatsApp ou normal) — ou seja, até 100 tarefas de toque criadas por dia por SDR. Se o SDR tiver **50 ou mais tarefas vencidas**, nenhuma tarefa nova de cadência é criada para ele até cair abaixo de 50. Mecanismo: a Faxina conta, por SDR, vencidas e criadas hoje; se estourar, põe a tag `sdr-lotado` nos leads em cadência daquele SDR; a cadência, antes de criar o toque, espera em laço de 1 h enquanto a tag existir (mesmo padrão do portão "Lead pausado?"). Retorno combinado e sinal quente (respondeu/clicou) **não** são represados. |
| D11 | Rotina do SDR: prioridade resposta quente (5 min) → retorno → inbound novo (15 min) → fila da 12x30 → fechar horário → no-show; blocos 09:00–11:30 e 14:00–16:30. Meta do W18 passa a "toques/dia". |

## Execução (marcar ao concluir, com data e commit)

- [x] E1 Inventário ao vivo — 24 publicados, `INVENTARIO-WORKFLOWS.md` (22/09). Achado: Interceptação Resposta v2 e Opt-out filtram canal 19 (WhatsApp oficial); a Stevo chega como 20 → hoje nenhuma resposta pela Stevo dispara os dois (E10).
- [x] E2 Etapa renomeada pelo dono na tela (23/09), mesmo id; `ghl_api.STAGES` ganhou `REUNIÃO DE DIAGNÓSTICO` (AGENDAR fica como apelido)
- [x] E3 Campo `Canal que conectou` criado (`TxJmoWdkA8rTqC1uEsMW`, `contact.canal_que_conectou`). Falta na tela: opção `Desqualificado` em `Resultado da tentativa` (dono)
- [x] E4 12x30 multicanal NO AR em 2 partes (`c64a808b` 380 nós + `17e6dc19` parte 2, 347 nós), T1 testada numa cópia (tarefa, campos, relógio); fila sai só depois da espera. Detalhe antigo: `tools/build_w11.py` reescrito e validado offline (`--so-montar`: 724 nós, 0 goto quebrado, 22 tarefas, 5 mensagens MT1/MT4/MT8/MT11/MT12, 0 'sim'). Falta: montar a cópia `ZZ TESTE 12X30` (W11_NOME/W11_TAG), testar, depois gravar na real e publicar. Fase "fechar horário" = workflow novo `tools/build_fechar_horario.py` (41 nós, validado offline), dispara pela tag `fechar-horario`
- [x] E5-E7 APLICADOS em 23/09 (`patch_funil_reuniao.py --aplicar`, backup `_antes-patch-funil/`): Pós-agendamento → REUNIÃO DE DIAGNÓSTICO e passa a tirar da Inbound, Reengajamento e Fechar Horário; Loop do closer, No-show e SLA em REUNIÃO; Pós-ligação: Atendeu fica em CONECTAR + tarefa [FECHAR HORÁRIO] + tag fechar-horario. Conferido: mesmos ids, publicados, gatilhos ativos.
- [x] E8 `Fechar Horário` PUBLICADO e W17d despublicado (23/09). Antes: criado em RASCUNHO (`82dd1fad-1bdd-44f7-8214-3a685521e2b4`, 41 nós) — falta publicar e despublicar o W17d. W17d (AGENDAR Estagnado) → "atendeu e não agendou" dentro de CONECTAR; W22 conta desde a proposta
- [x] E9 Inbound multicanal PUBLICADA (272 nós: WhatsApp primeiro, MI-0 automática na entrada, MIF-v2 na passagem, pausa no retorno, relógio certo). 12x30 parte 1 passou a portão por tag + grava etapa-conectar na entrada (a passagem da Inbound entra por tag `cad-outbound`). Reengajamento: só condições por tag (toques seguem telefone — decidir se vira multicanal)
- [~] E10 Gatilho canal 20 (Stevo) acrescentado na Interceptação Resposta v2 e no Opt-out, ativos (23/09, `tools/gatilho_stevo.py`). Falta o teste real com mensagem do número do dono
- [~] E11 W18 com texto novo (100 toques/dia, trava de 50 vencidas); W17b coerente (Pós-ligação tira a fila no resultado); W15 ok (1ª tentativa carimbada na T1). Falta na tela: listas inteligentes/painel (filtros por etapa → usar as tags etapa-*)
- [x] E12 Auditoria final ao vivo (23/09): 25 publicados, 0 condição de oportunidade fora de gatilho de oportunidade, 0 relógio errado, 0 prefixo desconhecido pela Faxina, 0 tarefa sem janela; 2 remoções apontam para a IA em rascunho (inofensivo). Testes: T1 da 12x30 (cópia), Espelho de Etapa, relógio, gatilho Stevo
- [~] E13 Faxina com capacidade por SDR (D14) escrita (`capacidade()`: vencidas + toques de hoje por SDR → tag `sdr-lotado` nos leads em CONECTAR). Falta: permissão `workflow` no gh (dono), token GHL (dono), 1ª execução em modo relatório
- [x] E14 Janela seg–sex aplicada em Interceptação (Clique e Resposta) e Pós-ligação; os demais já tinham. Opt-out fica sem janela de propósito (DND na hora)


Notas: nó `sms` aceito pela API (formato {type:sms, body, attachments}) — gravado no rascunho ZZ TESTE API; prova de entrega pela Stevo pendente. Pausa do retorno = laço de 1 h enquanto Resultado = Pediu retorno (sem espera por data). Pós-agendamento não tirava o lead da Inbound nem do Reengajamento — incluído no patch.

- [x] E15 `Espelho de Etapa` publicado + 26 condições de oportunidade trocadas por tag em 10 workflows + tags dos 55 leads (23/09). Ver APRENDIZADOS.

## 23/09/2026 madrugada — rodada final

- [x] **Só inbound (decisão do dono):** a Porta de Entrada não marcava `cad-inbound` em ninguém — a Cadência Inbound nunca rodava. Agora todo contato novo nasce com `cad-inbound` (testado com contato novo) e os 49 leads em NOVO LEAD foram marcados. ~~Promovido para CONECTAR → Inbound (MI-0 + 5 toques) → passa para a 12x30.~~ **Correção de 23/09/2026, sessão na nuvem, medida por API — esta última frase não aconteceu:** as 50 oportunidades marcadas continuam abertas em `NOVO LEAD` (nenhuma virou `CONECTAR`), 0 têm `Entrada em`/`Tentativa nº` e 0 têm tarefa. O gatilho da Cadência Inbound (`IMPLEMENTACAO-WORKFLOWS.md`, W12) é `Opportunity Stage Changed → CONECTAR`, filtrado por `cad-inbound` — a tag sozinha, sem a oportunidade mudar de etapa, não aciona nada. A marcação ficou pronta; a promoção (mesma decisão represada em `ROADMAP-SALES-ENGAGEMENT.md`, G-03) continua sem acontecer. Detalhe completo no G-03.
- [x] **Nutrição nova** (substitui o Reengajamento, mesmo id `37eb32e4`): 6 mensagens de WhatsApp, 1 a cada 15 dias, 100% automática; nunca manda para `telefone-invalido`. **Triagem da Nutrição** (`e7738b57`): o lead respondeu → espera 2 min (Opt-out primeiro) → mensagem TRI-1 (1 quero / 2 agora não / 3 sem interesse) → 1 volta para CONECTAR e para a 12x30 (tag `reengajado`, entra pela tag `cad-outbound`); 3 desliga (DND, nao-perturbe, perdido); 2 segue na nutrição; outra coisa → tarefa [SINAL] para o SDR. 12x30 parte 1 com reentrada ligada.
- [x] Opção **Desqualificado** criada em `Resultado da tentativa` (pela tela).
- [x] **Faxina:** integração privada "Faxina de Tarefas" (4 escopos) criada; token no segredo `GHL_TOKEN`; testada em modo relatório com dados reais (User-Agent obrigatório; id da tarefa = `_id`).
- [x] Agendador `.github/workflows/faxina-tarefas.yml` criado (pelo Claude Code no navegador) no branch padrão. 1ª execução em modo relatório OK (3 abertas, 1 a excluir, SDR 3 vencidas); variável `FAXINA_APLICAR=1` ligada em 23/09 e execução real: 1 excluída com nota. Roda a cada 10 min seg–sex 08–20h e de hora em hora fora disso. Desligar: apagar a variável `FAXINA_APLICAR`.
- [x] Mensagem automática PROVADA no número do dono (1407; conta Stevo = 9940): entregue como WhatsApp. Textos corrigidos (marca fixa).
- [ ] Triagem: armada no contato "Pablo Sampaio" (`rdaijzR0ZVCmXLAJ6jT2`, número 9940, tag `status-nutricao`). O 1407 é o número CONECTADO à Stevo (telefone da empresa) — responder dele aparece como mensagem da conta. Dispara quando o 9940 RESPONDER à N1 (mensagem vinda do lead, não enviada pela conta); a TRI-1 sai na janela (seg–sex 08:30–18:30). Depois de testar: tirar `status-nutricao` e desligar o `ZZ TESTE MENSAGEM` (`6bcaba47`).


## Fila autônoma (dono ausente, ciclo de 15 min, a partir de 23/09/2026 00:30)

Regras de cada rodada: 1) se houver script/navegador rodando, não interromper —
usar a rodada para ler documentação e revisar; 2) pegar o PRIMEIRO item `[ ]`
abaixo, fazer, TESTAR (com o número oficial de teste 9940 / contatos de teste,
nunca lead real), marcar `[x]` com data e evidência; 3) registrar o aprendizado
em `APRENDIZADOS-CRM.md`; 4) commit + push; 5) pensar no USUÁRIO (SDR, closer,
gestor): nomes claros, tarefas acionáveis, nada que dependa de decorar id.
Proibido sem o dono: excluir workflow/contato, mandar mensagem para lead real,
mudar preço/plano, mexer em outro projeto.

- [ ] A1 ATENÇÃO: a reconstrução da Triagem (00:30) descartou as execuções na fila — a TRI-1 NÃO vai sair sozinha às 08:30. Precisa de uma NOVA resposta do 9940 (em horário comercial sai na hora + 2 min). 08:30+: conferir que a TRI-1 saiu UMA vez para o 9940 (a marca antes da espera evita duplicata). Registrar. Depois de o dono responder 1/2/3, conferir o desfecho.
- [~] A2 (23/09 00:50) Investigado: nesta versão do GHL o calendário NÃO tem aba de lembretes (Calendários → Configurações só tem preferências) — lembrete de reunião é por WORKFLOW. Falta: (a) mapear o formato do nó "esperar até X h antes da reunião" (wait tipo `appointment`) pela tela num rascunho; (b) agendamento de teste para o 9940 (sem ferramenta de criar agendamento — pela tela). Depois: workflow "Lembretes da Reunião" (PA-CONF na hora, PA-R24, PA-R3H, PA-R30, sem `{{user.first_name}}`). Revisão do Pós-agendamento com olhos de usuário: confirmações e lembretes da reunião (PA-CONF, PA-R24, PA-R3H, PA-R30 da biblioteca) agora podem sair pela Stevo (nó `sms`) — sobe comparecimento. Montar, testar com o 9940, publicar.
- [ ] A3 Recuperação de No-show: mensagem NS-1 automática pela Stevo antes da NS1 (hoje só tarefa).
- [x] A4 (23/09 00:45) tarefa `[CLOSER] Apresentar proposta` no ramo Sim do Loop do closer — testada com o 9940 (nó executou). De quebra: 4 campos de DATA que nunca gravavam, corrigidos (ver APRENDIZADOS). Antes: Closer: ao "Reunião foi qualificada = Sim", criar tarefa `[CLOSER] Apresentar proposta` (a Faxina já reconhece o prefixo) — o closer hoje não tem tarefa nenhuma. Conferir o Loop do closer nó a nó.
- [ ] A5 Negociação Estagnada (W22, F-13): está especificado e não publicado — revisar, montar com portão por tag (`etapa-negociar`), testar, publicar.
- [x] A6 (23/09 01:00) `GUIA-SDR.md` e `GUIA-CLOSER.md` escritos (linguagem de quem usa; conferidos contra os workflows no ar — ex.: veredito Não + Timing errado → nutrição, lido do Loop do closer). O `briefing-sdr.md` fica como instrução do dono. Antes: reescrever `briefing-sdr.md` (rotina do SDR multicanal, prioridades, o que cada resultado faz, Faxina, limite 100/dia) e um guia curto do closer. Linguagem de quem usa, não de quem constrói.
- [ ] A7 Listas inteligentes (tela): Fila Telefone Hoje, Retornos, Fechar Horário, No-show, Nutrição — filtros por tag `etapa-*`/`status-*`; conferir colunas úteis ao SDR.
      > **Antes de montar a Fila Telefone Hoje, ler o F-16 (§2.31 do `build-wesales.md`).**
      > Trocar a cláusula de etapa por `etapa-conectar` resolve o lado da etapa, mas o
      > filtro especificado tem **duas** cláusulas: `não conectado-hoje` **E** etapa. E
      > `conectado-hoje` **nunca é removida** por ninguém (varredura nos 32 dumps). Com o
      > `Atendeu` ficando em `CONECTAR`, quem atende uma vez e não fecha horário sai da
      > fila **para sempre**. Montar a lista com o filtro como está escrito entrega um
      > vazamento pronto. A decisão é a pendência 2 do `ESTADO-E-PLANO.md` (recomendo a
      > saída A: `Wait 24h` → `Remove Tag` no `Pós-ligação v2`). **A7 depende dela.**
- [ ] A8 Auditoria completa de novo (`tools/auditoria_final.py`) + releitura de cada workflow publicado pensando no usuário (nomes dos nós, textos de tarefa, notificações).
      > Rodar **também** `python3 wesales/tools/auditoria_tags.py`. Ela faz duas perguntas
      > que a `auditoria_final.py` não faz (cruzamento completo na §2.33.1): limpeza de tag
      > pulada por `remove_from_workflow`, e tag só removida e nunca aplicada. Hoje devolve
      > **5 achados**, e **3 deles saem publicando a `Triagem da Nutrição`**.
- [ ] A9 Limpeza de testes: contato 9940 (tirar `status-nutricao`, `triagem-enviada` depois do A1), `ZZ TESTE MENSAGEM` e cópias ZZ em rascunho; `ZZ Teste Porta Inbound`.
      > **Faltam cinco, e são as que dão problema.** Medido em 23/09 02:35: a validação do
      > multicanal de 22:34 a 00:45 criou contato **e oportunidade `open` em `NOVO LEAD`**
      > para `Sem Nome`, `O Próximo Cliente`, `Pablo Sampaio`, `Francisca` e
      > `156766977421470` — **sem `source` e sem prefixo `ZZ`**. As que o A9 lista já estão
      > marcadas e por isso são fáceis; estas cinco são indistinguíveis de lead, e se a
      > esteira ligar assim a máquina liga para o dono e para a própria agência. Elas
      > também inflam a base: o `NOVO LEAD` tem 50 `open` e só **37** são lead pago.
