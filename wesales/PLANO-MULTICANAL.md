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
| D10 | Campo novo **`Canal que conectou`** (Ligação WhatsApp / Ligação normal / Mensagem), marcado junto com o resultado. |
| D12 | **Faxina de Tarefas:** tarefa AUTOMÁTICA aberta que perdeu o contexto (etapa/status/resultado) é **excluída**, com nota no contato; concluída e manual nunca são tocadas. Roda de graça no GitHub Actions (repo público), a cada 10 min em horário comercial. Script: `tools/faxina_tarefas.py` (17 casos testados). |
| D13 | **Nenhuma tarefa nasce no fim de semana.** Todo workflow que cria tarefa tem janela seg–sex 08:30–18:30 (inclusive Interceptação de Sinal, Pós-ligação e No-show). |
| D14 | **Capacidade do SDR:** no máximo **100 ligações/dia** (WhatsApp ou normal) — ou seja, até 100 tarefas de toque criadas por dia por SDR. Se o SDR tiver **50 ou mais tarefas vencidas**, nenhuma tarefa nova de cadência é criada para ele até cair abaixo de 50. Mecanismo: a Faxina conta, por SDR, vencidas e criadas hoje; se estourar, põe a tag `sdr-lotado` nos leads em cadência daquele SDR; a cadência, antes de criar o toque, espera em laço de 1 h enquanto a tag existir (mesmo padrão do portão "Lead pausado?"). Retorno combinado e sinal quente (respondeu/clicou) **não** são represados. |
| D11 | Rotina do SDR: prioridade resposta quente (5 min) → retorno → inbound novo (15 min) → fila da 12x30 → fechar horário → no-show; blocos 09:00–11:30 e 14:00–16:30. Meta do W18 passa a "toques/dia". |

## Execução (marcar ao concluir, com data e commit)

- [x] E1 Inventário ao vivo — 24 publicados, `INVENTARIO-WORKFLOWS.md` (22/09). Achado: Interceptação Resposta v2 e Opt-out filtram canal 19 (WhatsApp oficial); a Stevo chega como 20 → hoje nenhuma resposta pela Stevo dispara os dois (E10).
- [ ] E2 Renomear a etapa (D1) e trocar `AGENDAR` no código (`ghl_api.STAGES`) e nos documentos
- [ ] E3 Campo `Canal que conectou` (D10)
- [ ] E4 Cadência 12x30 multicanal com fase "fechar horário" e pausa no retorno (D2, D3, D5, D6, D9)
- [ ] E5 Pós-ligação v2: Atendeu não move etapa; resultado → manter/excluir/reagendar (D3, D9)
- [ ] E6 Pós-agendamento v2: reunião marcada → REUNIÃO DE DIAGNÓSTICO (D4)
- [ ] E7 Loop do closer, Registro de Comparecimento, SLA/Recuperação de no-show → nova etapa (D4)
- [ ] E8 W17d (AGENDAR Estagnado) → "atendeu e não agendou" dentro de CONECTAR; W22 conta desde a proposta
- [ ] E9 Cadência Inbound multicanal (D7) e Reengajamento 90d coerente
- [ ] E10 Interceptação de Sinal / Opt-out: responder pela Stevo (canal SMS) dispara?
- [ ] E11 Mestre de saída, W15, W17b, W18 (meta em toques), listas e painel
- [ ] E12 Testes ponta a ponta com contato de teste + auditoria final
- [ ] E13 Faxina: capacidade por SDR (D14) + agendador no GitHub Actions + token do GHL (dono cria)
- [ ] E14 Janela seg-sex em todo workflow que cria tarefa (D13)
