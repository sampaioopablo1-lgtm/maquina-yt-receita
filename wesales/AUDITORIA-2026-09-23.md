# Auditoria geral do CRM — 23/09/2026 (noite)

Pedido do dono: "auditar, verificar, revisar, etapa por etapa… encontrou erro ou
otimização, já faça, você tem todas as aprovações… pensando em usabilidade,
produtividade e facilidade".

**Método.** `tools/ler_workflow.py` transforma cada workflow publicado em um
roteiro legível (`auditoria-roteiros/*.txt`: condições com nome de campo/etapa,
textos exatos, tarefas, esperas, janelas, gatilhos). Cinco revisões paralelas
por etapa do funil (entrada+Inbound · 12x30+monitores · pós-ligação+sinais ·
reunião+closer · nutrição+triagem+varredura transversal), ~80 achados. Correções
aplicadas com `tools/corrigir.py` (lista JSON → backup em
`workflows-json/_antes-auditoria/` → conferência de next/parentKey/goto → PUT →
releitura). Listas aplicadas: `auditoria-roteiros/lote1.json`, `lote2.json`,
`lote3-*.json`. Auditorias no fim: `auditoria_final` 0 problemas, 5 de
`auditoria_tudo` limpas.

## Corrigido e publicado

**Entrada / Inbound**
- MI-0: "Recebi seu contato **agora**" (falso fora da janela) + primeiro nome → texto novo sem nome e sem promessa de minutos.
- MIF saía sem trava (inclusive para REUNIÃO / Não ligar) → trava "Ainda vale mandar?" + texto novo.
- Laço "Pediu retorno?" sem saída (lead preso para sempre) → trava de etapa nos 5 laços.
- "Não atendeu" automático gravado para quem já saiu de CONECTAR → trava nos 5 pontos.
- Aviso "aguardando retorno" repetido 5× → só o do TI1, com nome + telefone + "ligue em até 15 min".
- Nomes de nó invertidos ("WhatsApp ainda vem primeiro?" = SIM quer dizer rebaixado) → renomeados.
- Trava de etapa antes da MI-0 (caso Carlos Andrade).
- Speed-to-lead quase nunca disparava (lia campo gravado na criação da tarefa) → lê "Resultado da tentativa"; aviso com telefone e ação; nota-ruído removida.
- Lead Esquecido: aviso acionável; tag `novo-lead-estagnado` agora sai pelo Espelho.
- Mestre de saída: nota técnica em toda troca de etapa do closer removida.

**Cadência 12x30**
- MT1/MT4/MT8/MT11/MT12 sem primeiro nome; MT1 sem "sobre o seu cadastro"; MT12 coerente com a nutrição.
- **T12 não tinha ligação** (a régua era 11 ligações + despedida) → tarefa T12 + `toque` + 2 h, despedida só se não atendeu.

**Pós-ligação → reconstruído como `Pós-ligação v3`** (146 → 80 nós; v2 em rascunho)
- Caixa Postal era tratada como Atendeu (lead recebia "foi bom falar com você") → vira Não atendeu.
- Desqualificado não existia → sai das cadências, perdido, nota com motivo, aviso se motivo vazio.
- Não ligar agora tira de **todas** as réguas (antes Fechar Horário/Inbound seguiam).
- Pediu retorno: tarefa no horário combinado, ou tarefa para preencher data/hora; sem fila-quente.
- Número errado: sai das cadências; abandonado + aviso "ache outro contato" se houver e-mail/Instagram.
- Contadores no ramo certo; Canal que conectou; ~40 nós mortos eliminados.
- Sem janela de propósito (reage ao clique do SDR) — exceção registrada na `auditoria_final`.
- Testado no contato `ZZ Teste Pós-ligação v3`: Caixa Postal, Atendeu, Pediu retorno, Desqualificado.

**Reunião / closer**
- Nota de qualificação somava até **115** (Prazo e Urgência contavam juntos) → máximo 100.
- Lead que agenda **sem oportunidade** ficava fora de tudo → cria a oportunidade em REUNIÃO e segue.
- Nota "CHECKLIST DE AUTOAUDITORIA" gravada em todo contato → removida.
- `{{user.name}}` vazio na nota → "Qualificado por"; horário em formato legível.
- Esperas 24h/"3h" (3 horas corridas; atrasava o aviso em reunião marcada em cima da hora) → só 30 min antes.
- **Aviso ao closer virou briefing**: nome, empresa, hora, link, telefone, nota, anúncios, quem atende, BANT, dor, trilha, próximo passo.
- **Reunião Cancelada** (novo): sai dos lembretes, WhatsApp oferecendo remarcar, tarefa [NO-SHOW] remarcar.
- No-show: NS-1 sem primeiro nome e com trava `nao-perturbe`; "para ao responder" desligado (lead ficava preso em REUNIÃO).
- Registro de Comparecimento tira da recuperação de no-show e do SLA (no-show marcado por engano).
- Fechar Horário: "(30 minutos)" → "(1 hora)".
- Lembretes v3 com link do Google Meet (calendário trocado para Google Meet).

**Nutrição / Triagem / Opt-out**
- Lead reengajado nunca mais recebia nutrição (tag `reengajado` não saía) → corrigido.
- 6 mensagens reescritas: sem nome, com valor, posicionamento (atender o lead / aproveitar o que já investe), saída "responde PARAR".
- TRI-1 novo; confirmação ao lead nos ramos 1/2/3 (no 3, antes do DND).
- "agora não quero" desligava o lead para sempre → não mais.
- Menu repetia a cada resposta de quem disse "agora não" → não repete.
- **1ª resposta agora é lida**: "não tenho interesse"/"agora não"/"quero conversar" vão direto ao ramo; só o ambíguo recebe o menu.
- Opt-out reconhece PARAR / SAIR / STOP sozinhos.

**Transversal**
- 41 tarefas com vencimento "0" (nasciam vencidas) → vencem hoje 18:00 (closer: proposta 2 dias úteis, negociação 1). Compatível com a Faxina (vencida = dia anterior).
- Fila Travada: janela seg–sex + texto que diz o que fazer.
- Avisos de sinal: nome + telefone + "em até 5 min".
- GUIA-SDR: Pediu retorno / Número errado / Desqualificado conforme o v3; Dor principal nas palavras do lead; tarefas vencem 18:00.

## Deliberadamente NÃO feito (e por quê)
- **Apagar o gatilho `customer_reply` "vazio"** (sugerido 2×): é o único que dispara com a Stevo (tipo 20). Apagar desligaria Triagem/Opt-out/Interceptação.
- **Mestre tirar das cadências**: o fim da 12x30 move a oportunidade e seria cortado; as cadências têm portões.
- **Testar Reunião Cancelada no 9940 hoje**: "tirar dos Lembretes" mataria o teste de H-3/M-10 de 24/09. Testar depois das 18:30 de 24/09.

## Backlog (próxima rodada / decisões)
1. **Porta de Entrada** põe `cad-inbound` em todo contato criado (import/manual também) e o lead inbound espera o SDR mover (o 1º alerta vem em 24 h). Decidir na abertura de 28/09: mover inbound de anúncio direto para CONECTAR e filtrar a origem.
2. Pós-agendamento/Lembretes podem rodar em dobro se a reunião for reconfirmada (A CONFIRMAR em teste).
3. Loop do closer: veredito "Não" antes do motivo vira perdido mesmo com "Timing errado".
4. Interceptação de Resposta só vale em CONECTAR (resposta a lembrete/no-show não vira [SINAL]); 1 tarefa por mensagem.
5. 12x30: opção "Não trabalhada" no lugar do "Não atendeu" automático; contador de WA; espera de `sdr-lotado` 1 dia; Faxina sem paginação acima de 100 leads.
6. Retorno Vencido mede da edição do campo, não da data prometida; tag nunca sai.
7. Nutrição: reentrada em paralelo; encerramento após N6.
8. Atribuição/avisos de gestor usam usuário fixo — rever quando houver mais de um usuário.
9. Calendário: horário oferecido 17:30–19:30 inclusive fim de semana (dono corrige na tela).
10. Domínio de e-mail próprio (hoje sai pelo LC Email compartilhado).
