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
| D11 | Rotina do SDR: prioridade resposta quente (5 min) → retorno → inbound novo (15 min) → fila da 12x30 → fechar horário → no-show; blocos 09:00–11:30 e 14:00–16:30. Meta do W18 passa a "toques/dia". |

## Execução (marcar ao concluir, com data e commit)

- [ ] E1 Inventário: todo workflow publicado × etapa/campo/tag/tarefa que toca
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
