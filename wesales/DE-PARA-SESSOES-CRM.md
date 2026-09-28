# De-para: o que as sessões disseram × o que está no CRM (27/09 20:50)

Fonte do lado "disseram": histórico de commits de 26/09 18:00 a 27/09 20:41 nos quatro
branches que mexeram no WeSales. Fonte do lado "CRM": leituras feitas hoje pela API
pública (Action `recon`/`verificar`, conector GHL_CRM) e pela sessão logada do navegador.

## As sessões

| Sessão (branch) | Período | Escreveu no CRM? |
|---|---|---|
| **A** — `abertura-operacao-dnd-n7dnjv` (esta) | 27/09 01:27–20:41 | **sim**, e conferido — tabela abaixo |
| **B** — `amazing-johnson-mclksg` | 26/09 23:52–27/09 20:12 | **não**: os próprios commits dizem "zero escrita no CRM", "modo relatório". Auditorias, ROADMAP reconstruído, achados F-19 a F-23 e G-25 a G-30 |
| **C** — `laughing-bohr-ki6ah8` (PC do dono, rodando agora) | 27/09 20:40– | **ainda não**: último commit é uma sonda de leitura dos nós das mensagens e da pontuação |
| **D** — `abertura-operacao-dnd-ib6xaz` | 27/09 17:47–17:58 | **não**: registrou as funções (Andreyna SDR, Pablo closer) e consertou um arquivo da Action |

## Sessão A — o que está no CRM

| Hora | O que foi escrito | Situação hoje no CRM |
|---|---|---|
| 01:27 | `dnd = true` em 30 contatos (rampa) | **revertido às 20:23** — `dnd = false` em 31 |
| 03:54 | `Prioridade` em 39 leads | vigente: 5 com 4, **34 com 0** (os 31 liberados continuam 0 até a cadência regravar) |
| 12:05 | 31 tags `nao-perturbe`, 9 DND, nome de oportunidade, descarte do teste de calendário | `nao-perturbe` **retirado às 20:23**; ficou só em 3 contatos que não são leads |
| 14:23–14:35 | dono em 64/64 contatos e 43/43 oportunidades | ✓ recon 19:37: 0 sem dono |
| 14:51 | `Prazo` e `Investe em anúncios` derivados em 37 contatos | ✓ visto nos contatos em 20:20 |
| 14:57–15:29 | filas do discador `fila-sdr` / `fila-closer` | ✓ 5 com `fila-sdr` em CONECTAR |
| 17:07 | ficha BANT: 30 campos em ordem na pasta da ficha | ✓ verificar verde 19:26 |
| 18:25 | carteira → Andreyna; `SDR responsável` só com a SDR | ✓ |
| 18:32 | campo `B · Quanto pode investir` | ✓ posição 405 |
| tarde (tela, sessão do navegador) | Gatilhos do Call Center + fila | ✓ relido na tela |
| 19:12 | `Reunião Cancelada` publicado | ✓ já estava publicado (API) |
| 19:37 | e-mail da SDR (feito pelo dono) | ✓ API |
| 20:06 | itens 4 e 6: Pós-agendamento v2 v17, Cadência 12x30 v36, Fechar Horário v10, Pós-ligação v3 v6 | ✓ relido pela sessão logada |
| 20:23 | 31 leads liberados | ✓ resposta do CRM contato a contato |

## Ficou só em documento (NÃO está no CRM)

| Item | Onde está escrito | Quem destrava |
|---|---|---|
| 42 textos de WhatsApp e lembretes | `COPY-WHATSAPP.md` | sessão C, rodando agora |
| Pontuação G-04 | `ESTADO-27-09.md` §12 | sessão C, rodando agora |
| Prioridade dos 31 liberados (hoje 0) | `recalcula_prioridade.py` | qualquer sessão, pela API pública |
| 5 pastas de campo + arrastos (só a pasta da ficha foi feita) | `USABILIDADE.md` §4 | tela |
| Achados do pente fino: Prioridade 6→5, laço de 1 h do Fechar Horário, inbound sem cadência ao voltar | `ESTADO-27-09.md` §10 | sessão com acesso ao construtor |
| Atuador de `sdr-lotado` e `fila-wa` | `FALTA-PARA-SER-MAQUINA.md` | sessão com acesso ao construtor |
| Achados F-19 a F-23 e G-25 a G-30 da sessão B | `ROADMAP-SALES-ENGAGEMENT.md` no branch dela | revisar antes: a própria sessão B marca vários como "decisão do dono" |
| Mapeamento dos 9 formulários do Meta | `FALTA-PARA-SER-MAQUINA.md` §4-BIS | dono, na tela do GHL |
| Conta de anúncio `UNSETTLED`, termos de Lead Ads | `ESTADO-27-09.md` §4.1 | dono, no Meta |
| Painel SDR externo | — | abandonado por decisão do dono (tudo dentro do CRM) |

## Divergência entre sessões que precisa de atenção

- A sessão B (G-30) e a sessão A (§11) acharam o mesmo campo novo, `Voice AI Reason for
  Call`. Leitura da sessão A às 20:15: **0 agentes de Voice AI** na conta. O campo fica;
  não há recurso cobrando.
- A sessão B trabalha num ROADMAP reconstruído que a sessão A não tem. Antes de aplicar
  qualquer F/G novo, juntar os dois documentos para não aplicar item que já foi
  resolvido ou retratado.

## Gravado pela sessão do PC em 27-28/09

Caminho: `renovar_bearer.js` com o `storage-state.json` local + `ghl_interno.py` (API interna)
para workflows; API pública para contatos. Script: `tools/gravar_copy_whatsapp.py` (lê os
textos do `COPY-WHATSAPP.md`, confere o texto antigo contra o backup lido antes, grava
preservando `status`, relê e compara nó a nó). Backup de cada workflow antes da gravação em
`.local/bkp-copy-27-09/` (fora do git). Nenhum nó, contato, campo ou tag criado ou apagado.

| Item | Workflow ou registro | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|
| MI-0 + MIF | Cadência Inbound | v21 → v22 | sim | gravado primeiro; MI-0 sai seg 28/09 08:30 com o texto novo |
| MT1, MT4 | Cadência 12x30 | v36 → v37 | sim | releitura do script caiu em 503; relida em seguida, nó a nó igual |
| MT8, MT11, MT12 | Cadência 12x30 — parte 2 | v11 → v12 | sim | |
| MFH1, MFH2 | Fechar Horário | v10 → v11 | sim | |
| TRI-1, resposta 1, resposta 2 | Triagem da Nutrição | v21 → v22 | sim | opções 1/2/3 mantidas |
| N1–N6 | Nutrição — WhatsApp a cada 15 dias | v32 → v33 | sim | |
| NS-1 | Recuperação de No-show | v23 → v24 | sim | |
| CANC-1 | Reunião Cancelada | v4 → v5 | sim | |
| 22 envios (17 WA + 5 e-mails) | Lembretes da Reunião v3 | v4 → v5 | sim | assunto dos e-mails e os 8 envios de 10 min intactos |
| G-04: 5 portões, igualdade exata, pontos iguais | Pós-agendamento v2 | v17 → v18 | sim | 1k a 5k +`Abaixo de 5k` (6) · Até 1k +`Até R$ 1.000` (2) · Urgência Sem prazo +`Posso esperar e ver oque acontece` (2) · Investe Sim +3 valores pagos do Meta (13) · Investe Nunca +`Não invisto nada ainda` (4) |
| Pente fino 4: Prioridade 6 antes da 5 | Pós-agendamento v2 | v18 → v19 | sim | tirado só o campo Prioridade=6 do nó 6a5f65bb (Data agendado fica); vale o nó dedicado "Prioridade = 5" (§9.2 vai de 1 a 5). Nenhum nó apagado |
| Prioridade dos 31 liberados | 31 contatos em CONECTAR | 0 → 4 | sim | `recalcula_prioridade.py --aplicar`, regra 5 da §9.2; novo `--dump`: 0 de 39 a mudar. Os 3 não-leads ficam 0 |
| Texto antigo conferido | os 42 nós + 5 portões | — | — | nenhuma divergência: todo texto antigo era o descrito no documento |

Consertos de ferramenta no caminho: `ghl_interno.py` e `recalcula_prioridade.py` passam a
mandar User-Agent de navegador (sem ele o Cloudflare responde 1010).

### Para o dono decidir (recomendação em uma linha)

| Item | Recomendação |
|---|---|
| Laço de 1 h do Fechar Horário com `Pediu retorno` (FH2, FH3, Fim: Wait 1 h → volta ao mesmo portão, sem contador; e não reconfere se o lead ainda está em CONECTAR) | limitar a 72 h (contador + saída para tarefa `[RETORNO]` ao SDR) e apontar o Go To para o portão "Ainda em CONECTAR?"; precisa de nós novos, então é decisão sua |
| F-19 / F-20: auto-resposta de ausência tratada como interesse | aprovar T-23 e C-33 no `APROVADO.md` e montar o workflow "Resposta Automática — Ausência" (WA e e-mail) depois de terça; antes disso, só o filtro "Doesn't Contain" na Interceptação de Sinal — Resposta v2 |
| F-21 + F-23: Interceptação de Sinal por e-mail | adiar: só importa quando houver lead sem telefone respondendo e-mail; montar já com o teto semanal do F-23 |
| F-22: reputação do e-mail | conferir em Email Services se o domínio é dedicado; se for, ligar o Warmup antes do primeiro EM-1 |
| G-27/G-29: `SDR responsável` e `B · Quanto pode investir` sem nenhum workflow lendo | definir que a SDR preenche os dois na ligação e que a nota de qualificação lê `Quanto pode investir`; hoje nada lê |
| Pente fino 6: inbound que volta para CONECTAR não ganha cadência | manter como está até ter caso real; o Retorno Vencido cobre |
| G-25, G-26, G-28, G-30 | nada a fazer: resolvidos pela sua decisão das 20:10–20:23 ou só registro (Voice AI com 0 agentes) |

## Itens 1–4 (28/09) — sessão do PC, 27/09 18:00–18:50

| Item | O que foi gravado | Workflow ou registro | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| 1A trava | **nada gravado nos 17 envios** | — | — | — | o pedido exige o nó nativo "esperar condição com tempo limite", e nenhum dos 70 workflows da conta o tem (varridos: só esperas de tempo, agendamento e resposta). O Chrome segue desconectado, e o construtor não desenha no navegador sem tela. **36 contatos** (CONECTAR aberto, `cad-inbound`, sem `nao-perturbe`) receberiam a MI-0 juntos seg 08:30 |
| 1A alternativa testada | laço com nós já usados na conta (tag → "tem wa-liberado?" → senão, espera 15 min e volta), `tools/gravar_portao_wa.py` | ZZ TESTE MENSAGEM (era rascunho) | v6 → v11, agora **publicado** | sim | teste no contato de teste: parou em `wa-aguardando`, o governador (`--so`) liberou, e seguiu o fluxo. Aprendido: o GHL valida ao publicar que o `parentKey` de cada nó é o id do nó anterior. Não aplicado em workflow real, porque não é o desenho pedido |
| 1B agendamento | PR com os 3 arquivos para o branch padrão | PR #104 | — | — | aguarda merge do dono. A tarefa local do Agendador do Windows foi criada e depois **desativada** para não rodar em dobro |
| 1B governador | modo de teste `--so <contactId>` | `tools/wa_governador.py` | — | ensaio ok | contrato original mantido |
| 4 calendário | consent em português; antecedência de 2 h (`allowBookingAfter` 2 `hours`); aviso por e-mail ao closer para remarcada e cancelada | Reunião com closer | — | sim | **o PUT público reiniciou a duração para 30 min**; restaurada na hora para 1 h (igual ao backup, relido). O aviso de marcada ao closer já existia. **O aviso ao contato está LIGADO** (e-mail de marcada), diferente do que o pedido supunha; não mexi |
| pedido anterior | campo `Canal da tentativa` (Telefone/WhatsApp), id `AsZMGmsKVu1xEp36hyLb`, posição 595, pasta da ficha | campo de contato | criado | sim | pedido explícito do dono antes da regra "não criar campo" |
| pedido anterior | 3 portões `fila-wa` → `Canal da tentativa == WhatsApp`; limpeza do canal no fim de 10 ramos (não no "Resultado vazio?") | Pós-ligação v3 | v6 → v7 | sim | teste no contato de teste: Tentativas WhatsApp vazio → 1, Tentativas telefone ficou em 4, canal limpo no fim |
| pedido anterior | listas inteligentes "Ligar pelo WhatsApp" (`a1CX9wVdSIbTHngFK4L9`) e "Fila do dia — SDR" (`3w5btTbp8ccrZ1tLa5BV`) | Contatos | criadas | filtros relidos | a conta tinha **0** listas. Falta: colunas, compartilhar com a Andreyna e fixar |

### Itens 1–4 — segunda rodada (27/09 19:00–20:30, modo automático desligado pelo dono)

| Item | O que foi gravado | Workflow ou registro | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| 1A trava | portão antes dos 17 WhatsApp de prospecção: tag `wa-aguardando` → "tem wa-liberado?" → remove tags e envia; senão "tem wa-manual?" → tarefa `[WHATSAPP MANUAL] <código> — {{contact.first_name}}` (texto + snippet) e segue; senão espera 15 min e volta | Reunião Cancelada / Inbound / 12x30 / 12x30 p2 / Fechar Horário / Nutrição / No-show | v5→v6 / v22→v23 / v37→v38 / v12→v13 / v11→v12 / v33→v34 / v24→v25 | sim, nó a nó + arquivo de execução (17/17 atrás da trava) | laço em vez do nó nativo "esperar condição com timeout": não há esse nó na conta para copiar e o Chrome segue desconectado. Mesmo desenho testado ao vivo no ZZ TESTE MENSAGEM (parou, foi liberado, seguiu). A janela seg–sex 08:30–18:30 dos 7 workflows faz o papel do passo 1 |
| 1A governador | reserva as vagas do dia (11–15) para os primeiros da fila; o excedente vira `wa-manual` na hora; às 18:30 o que sobrar vira manual; modo `--so <id>` para teste | `tools/wa_governador.py` | — | simulado | segunda simulada: 36 às 08:30 + 3 às 14:00 → 13 automáticos espalhados entre 09:00 e 17:30, 26 manuais, ninguém preso |
| 1B agendamento | só no GitHub (PR #104, atualizado); nada local | PR #104 | — | — | tarefa do Windows e .cmd removidos por ordem do dono. **Sem o merge, ninguém é liberado nem vira manual** (nada sai em lote; os leads ficam esperando) |
| 2 snippets | 17 trechos de texto (SMS), um por envio, texto idêntico ao nó; pasta "WhatsApp manual — prospecção" | Conversas → Trechos | 0 → 17 | sim, 17/17 texto | "WA MI-0 abertura inbound" ficou fora da pasta (o PUT de pasta devolve 200 e não move). Teste "/WA MI-0" na conversa: não confirmado pela tela sem janela; nada foi enviado |
| 4 calendário | aviso nativo ao contato (e-mail de marcada) **desligado**; avisos ao closer seguem | Reunião com closer | — | sim | evita e-mail em dobro com o Lembretes v3 |
| teste | ZZ TESTE MENSAGEM devolvido a rascunho, idêntico ao original | workflow de teste | v11 → v12 draft | sim | |
| listas SDR | "Fila do dia — SDR" (`w1trBx1OSrGoh6bs8klb`, 36 contatos) e "Ligar pelo WhatsApp" (`a1CX9wVdSIbTHngFK4L9`): filtros no formato da tela, ordenadas por Prioridade, colunas Nome/Telefone/Tentativas telefone/Última atividade/Prioridade, **compartilhadas com a Andreyna**, abas fixadas | Contatos | — | sim, na tela e pela API | aprendido: a tela usa outro formato de filtro (`custom_fields.<id>`, etapa sem `status`, sem `range`); compartilhar é `POST api.leadconnectorhq.com/smartlist/share_with_select`. Uma lista que eu criei quebrou a tela (compartilhamento gravado como texto) e foi **excluída**; tela conferida depois |
| Canal da tentativa | teste no contato de teste | Pós-ligação v3 v7 | — | sim | Tentativas WhatsApp 0→1, telefone ficou 4, canal limpo no fim |

### Terceira rodada (27/09 20:30–21:30)

| Item | O que foi gravado | Onde | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| governador | PR #104 mergeado pela sessão (autorizado pelo dono); Action manual `aplicar=false` rodou verde ("fim de semana: nada a liberar") | branch padrão / GitHub Actions | — | sim | o agendamento vale a partir de seg 08:30, a cada 30 min, sem depender do PC |
| telefone | número toca para Pablo **e** Andreyna (`linkedRingAllUsers`); caixa postal após 20 s; gravação de ligações mantida | +55 11 5026-6034 | — | sim (API pública) | rota do app: `POST backend/phone-system/twilio-accounts` (`assignedUsers`, `voicemail`). "Número dedicado" do usuário deixado vazio de propósito |
| dono do lead novo | "Assign user" das cadências passa de Pablo para a Andreyna (só atua em lead sem dono); tarefa `[WHATSAPP MANUAL] MI-0` vai direto para a Andreyna (na MI-0 o lead novo ainda não tem dono) | Cadência Inbound / Cadência 12x30 | v23→v24 / v38→v39 | sim, nó a nó | antes, todo lead novo ia para o Pablo e as tarefas da SDR iriam para ele |
| permissões SDR | ligados só contatos, conversas, oportunidades, agenda, ligações, tags, painel/relatórios, mídias; configurações, pagamentos, workflows, marketing e IA desligados | usuário Andreyna | — | sim | feito pelo dono na tela (a API pública devolveu 200 sem gravar). "Só dados atribuídos" desligado **por decisão do dono (27/09 21:40): a SDR vê todos os contatos por enquanto** |

### Quarta rodada — o que tinha ficado para trás (27/09 21:40–22:30)

| Item | O que foi gravado | Onde | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| formulário SDR | "Qualificação e agendamento — SDR" (`ww2ruVG5CdJ7rWJ83Gbf`), duplicado do "Qualificação SDR" (original intacto, conferido contra o backup). Blocos: Contato · **Já respondido no anúncio — só confirme** (Necessidade, Urgência, Investimento, Investe, Prazo) · N · B (Budget + **Quanto pode investir**) · A · SDR responsável. Só o telefone é obrigatório | Formulários | novo | sim, página pública | o conteúdo real fica no arquivo da versão mais recente (`versionHistory[0]`); o `formData` do GET vem desatualizado |
| agenda SDR | calendário "Agendamento pela SDR" (`oOfR9ADPJM0WyVyHRgKE`, slug `agendamento-sdr-proximo-cliente`): mesmo closer, 1 h, antecedência 2 h, **com o formulário acima na mesma página**; avisos só ao closer (sem e-mail ao lead) | Calendários | novo | sim, página pública (horário → "Selecionar" → formulário → "Agendar reunião") | o calendário público do lead ("Reunião com closer") não mudou |
| gatilhos | os 6 workflows de reunião ganharam um 2º gatilho, cópia do original com o calendário da SDR e o mesmo primeiro passo | Pós-agendamento v2, Lembretes v3, Reunião Cancelada, No-show, Comparecimento, SLA do Closer | só gatilhos | sim | ensaio antes no ZZ TESTE TAREFA: reunião de teste no calendário da SDR disparou a tarefa com marcador; reuniões de teste canceladas, gatilho de teste desativado, ZZ de volta a rascunho |
| link preenchido | tarefa [FECHAR HORÁRIO] e FH2/FH3 com "Abrir agendamento com a ficha preenchida" (nome, telefone, e-mail, empresa, necessidade, urgência, investimento, prazo, SDR) | Pós-ligação v3 / Fechar Horário | v7→v8 / v13→v14 | sim | FH2/FH3 deixam de dizer que o WhatsApp "já saiu sozinho" |
| ficha | campos do anúncio no topo da ficha (posições 50–58): Necessidade, Urgência, Investimento, Investe, Prazo | campos de contato | posições | sim | `campos_bant.py` atualizado para manter |
| Fechar Horário | laços de "Pediu retorno" voltam a checar "Ainda em CONECTAR?" (lead que sai da etapa deixa o laço) | Fechar Horário | v12→v13 | sim | limite de horas não aplicado: exigiria campo novo |
| roteiro | trecho "ROTEIRO da ligação" (digitar /ROTEIRO) | Conversas → Trechos | 17→18 | sim | |
| listas | Fila quente, Fechar horário, Retornos vencidos (SDR, compartilhadas com a Andreyna); Reuniões marcadas, Negociar (closer) | Contatos | novas | sim, na tela | |
| teste | tag `wa-lib-2026-09-27` retirada do contato de teste | contato de teste | — | sim | |
| F-19 (parte que não exige campo nem tag nova) | as 19 frases de ausência/resposta automática entram como condições OU no portão de opt-out, cujo ramo "sim" encerra sem ação | Interceptação de Sinal — Resposta v2 | v10→v11 | sim, nó a nó + arquivo de execução | auto-resposta deixa de virar prioridade 5 / `fila-quente` / "ligar agora". O `Stop on Response` nativo das cadências continua parando a cadência (limite da plataforma) |

### Ficou para o dono (27/09 22:40)

| Item | Recomendação |
|---|---|
| Valor da oportunidade nasce 5000 fixo | **decidido pelo dono em 27/09: fica fixo em R$ 5.000.** Nada a gravar |
| Passagem para FORMALIZAR / entrega | definir quem assume depois do fechamento e o checklist; depois disso vira uma tarefa automática |
| Relatórios e dashboard | montar na tela depois da 1ª semana de operação, com dado real (ligações/dia, conexão por tentativa, agendamentos, comparecimento) |
| Tags `sdr-lotado` e `fila-wa` (lidas, nunca aplicadas) | `fila-wa` ficou obsoleta com o Canal da tentativa; `sdr-lotado` só faz sentido com mais de uma SDR — manter sem uso por ora |
| Limite de horas no "Pediu retorno" do Fechar Horário | exigiria campo contador novo; hoje o lead sai do laço ao deixar CONECTAR e o Retorno Vencido avisa |
| Resposta automática também parar a cadência | limite do GHL (`Stop on Response` não filtra texto); reativar à mão quando acontecer |

### Quinta rodada (27/09 22:40–23:30)

| Item | O que foi gravado | Onde | Versão antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| Pediu retorno: prazo 3 dias | workflow novo "Retorno — prazo de 3 dias" (`892d424e`): Resultado = Pediu retorno → espera 3 dias → ainda Pediu retorno e em CONECTAR → oportunidade **Abandonada** + `nutricao-90d` + nota | workflow novo | v2, publicado | sim | "perdido e nutrido" = Abandonado: a Nutrição só envia com `status-nutricao`, que o Espelho aplica em Abandonado; "Perdido" pararia a nutrição |
| FORMALIZAR: prazo 7 dias | workflow novo "Formalização Parada" (`14a76a7d`): entra em FORMALIZAR → espera 7 dias → ainda aberta → aviso + tarefa "[CLOSER] Marcar a oportunidade como ganha ou perdida" | workflow novo | v2 → v3 (3 → 7 dias) | sim | decisão do dono: depois de FORMALIZAR o closer marca ganha ou perdida |
| fila do discador | atuador das filas no branch padrão (PR #106 e #107), cron a cada 30 min seg–sex 08:00–18:59; aplicado agora: `fila-sdr` 5 → 36 | GitHub Actions + tag `fila-sdr` | — | sim, 36/36 | antes o cron nunca tinha rodado (arquivo fora do branch padrão): lead novo não entrava na fila do Power Dialer |
| painel "Decisão — Operação SDR/Closer" | painel criado (`6ab9b477ea8a8a09aee49d8b`), **ainda sem widgets** | Relatórios | — | — | gravar widget pela API esbarra em "versão desatualizada do painel"; falta o formato que a tela usa |

### Sexta rodada — relatórios e Pixel (27/09 23:30–28/09 00:45)

| Item | O que foi gravado | Onde | Relido | Observação |
|---|---|---|---|---|
| painel de decisão | "Decisão — Operação SDR/Closer" (`6ab9b477ea8a8a09aee49d8b`) com **21 widgets** (leads e origem/campanha/meio/usuário; oportunidades abertas/ganhas/perdidas/valor/eficiência; reuniões agendadas/confirmadas/canceladas/não comparecidas; tarefas; ações manuais) | Painel de controle | sim, API | montado pela tela sem janela (objetivos: vendas, agendamento, equipe, leads) + **4 widgets acrescentados um a um: chamadas por status, chamadas por usuário, duração média das chamadas, distribuição por etapas — total 25** |
| Pixel no calendário público | `pixelId` 1600846091439175 no "Reunião com closer" (evento sai do navegador do lead) | Calendário | sim | duração, consentimento e antecedência conferidos intactos |
| Pixel nos itens internos | calendário da SDR sem Pixel de propósito; formulários internos disparam `SubmitApplication` já ao abrir a página (ruído da SDR) — remoção pelo formulário novo não pegou (rota própria `/forms/update-…`); original protegido | Formulários | — | os 2 `SubmitApplication` de 27/09 vieram daí |
| Conversions API | 3 workflows novos: "Meta CAPI — Contato (atendeu)" → `Contact`; "— Reunião marcada" (2 calendários) → `Schedule`; "— Venda ganha" → `Purchase`; integração Facebook conectada, pixel 1600846091439175, BRL | workflows novos | sim, publicados | **o GHL exige token**: lido do valor personalizado `{{custom_values.meta_capi_token}}` (criado com o texto COLE_O_TOKEN_AQUI). Até o dono colar o token, os eventos não saem. `Lead` fora de propósito: o formulário do Meta já conta |

### Análises pedidas (28/09) — aprovadas e entregues
Tentativas até agendar e até qualificar ainda sem dado real (4 agendados e 3 qualificados, quase todos teste); e a conta não congela o nº de tentativas no momento do agendamento/qualificação. Proposta: script semanal (GitHub, segunda cedo) que calcula pelo histórico das conversas (ligações/WhatsApp antes da data da reunião e antes do envio do formulário da SDR) + 3 análises: velocidade de resposta × agendamento, conexão por tentativa/horário/canal, resultado por formulário/campanha do Meta. Resultado como nota fixa no painel "Decisão".

| Item | O que foi gravado | Onde | Relido | Observação |
|---|---|---|---|---|
| análises semanais | `tools/analises_semanais.py`: tentativas até agendar e até qualificar, velocidade da 1ª ligação × agendamento, conexão por tentativa/horário/canal, resultado por origem | nota fixa no painel "Decisão" | sim (1 nota, atualizada no lugar) | ligação por WhatsApp não aparece na conversa, só nos contadores; conexão = chamada completada ≥ 20 s |
| agendamento | Action `wesales-analises.yml` no branch padrão (PR #108), toda segunda 07:00; rodada manual verde | GitHub | sim | sem `GHL_STORAGE_STATE` ela só imprime no log; a nota do painel exige sessão (a chave pública dá 401) |
| sessão na nuvem | segredo `GHL_STORAGE_STATE` (sessão sem os caches `statsig`, 10 KB; a completa tinha 111 KB e o limite é 48 KB), autorizado pelo dono | GitHub | sim: Action atualizou a nota do painel sem o PC | o token de renovação **não desliza com o uso** (mesma validade antes e depois): vence em **25/10/2026** |
| aviso de vencimento | `tools/vigia_sessao.py` na Action semanal (PR #109): com ≤ 10 dias abre issue no GitHub (chega por e-mail) com o passo a passo | GitHub | sim ("vence em 27 dias") | só a nota do painel depende da sessão; governador, filas e análises usam `GHL_PIT` |

### Sem ação manual (28/09) — a sessão saiu do GitHub

| Item | O que foi feito | Onde | Relido | Observação |
|---|---|---|---|---|
| funil real | o relatório abre com funil **por marco do lead**, cumulativo (entrou → tentado → conectou → qualificou → agendou → compareceu → ganhou), taxa sobre a etapa anterior e sobre o total | `tools/analises_semanais.py` | sim | o "Funil de oportunidades" por etapa dá NOVO LEAD → CONECTAR = 100% (passagem automática); o funil real corrige o conceito |
| entrega sem sessão | relatório semanal vira **tarefa "📊 Análise da semana"** para o Pablo (API pública); Action só com `GHL_PIT` (PR #110) | GitHub + Tarefas | sim, Action na nuvem criou a tarefa | nenhuma credencial que vença |
| sessão removida | segredo `GHL_STORAGE_STATE` **apagado** do GitHub; aviso de vencimento retirado da Action; nota do painel virou aviso de onde o relatório chega | GitHub / painel | sim | nada nas automações depende de login do dono |

### Conversions API ativa (28/09 00:10)

| Item | O que foi feito | Onde | Relido | Observação |
|---|---|---|---|---|
| token | dono colou o token real do Meta em "Meta CAPI token"; a sessão copiou para o campo de token dos 3 nós, sem exibir | Meta CAPI — Contato / Reunião marcada / Venda ganha | sim, v3 → v4, confere com o valor guardado | se o token for trocado, recopiar para os 3 nós |
| janela | os 3 workflows herdaram a janela seg–sex 08:30–18:30 do modelo; **retirada** para o evento sair na hora | os 3 workflows | sim | |
| teste | Resultado = Atendeu no contato de teste (2×) → Meta registrou **2 eventos `Contact` de servidor** (23:00–00:00) | Pixel 1600846091439175 | sim, `ads_get_dataset_stats` SERVER_ONLY | `server_last_fired_time` do Meta demora a atualizar; a contagem é o sinal confiável. `Purchase` não testado de propósito (não mandar venda falsa) |
| Pixel no formulário da SDR | "Qualificação e agendamento — SDR": `fbPixelId`, `pageViewEvent` e `formSubmissionEvent` vazios (a remoção de antes tinha gravado; a leitura que dizia o contrário pegou uma cópia antiga do arquivo). Página pública aberta sem tela: nenhum evento disparado | formulário novo | sim (arquivo da versão atual + página ao vivo) | o formulário original "Qualificação SDR" segue com Pixel (protegido e fora do fluxo da SDR). Contato de teste limpo: 3 tarefas [FECHAR HORÁRIO] concluídas e tag `fechar-horario` retirada |

### Playbook SDR/Closer (28/09)

| O que | Onde | Estado |
|---|---|---|
| Playbook de ponta a ponta: operação, links, rotina hora a hora, registrar tentativa, scripts inbound + objeções, qualificar e agendar, rotina do closer, regras da máquina, metas, referências | Claude Docs — https://claude.ai/code/artifact/8454238e-c51c-4bbc-90ff-cc407f4b6458 | pronto (rev 23) |
| Fotos das telas | ficha do contato de teste (sem dado de lead real), formulário SDR em branco, painel Decisão | no doc |
| Pesquisa de mercado | HBR 2011, MIT/InsideSales LRM, Gong Labs (aberturas e objeções), Meetime (metas e benchmark BR) — tabela "O que a pesquisa de mercado diz" nos scripts | no doc |
| Correção | "Ligação por WhatsApp não existe no sistema" → ligação pelo app + lista "Ligar pelo WhatsApp" + Canal da tentativa = WhatsApp | no doc |

### Trava de canal, formulário antes da agenda e horários do closer (28/09, madrugada)

| Item | O que foi gravado | Onde | Antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| trava de canal | workflow "Trava de canal — falou hoje" (`c4a3aab7-5fb2-4d05-80cf-0364a0a90bc5`): tag `falou-hoje` → espera 12 h → tira. Gatilhos: **Call Status = completed, saída** (ligação do discador atendida), Resultado = Atendeu, Resultado = Pediu retorno. Sem janela de horário | Automações | novo, publicado v3 | sim (3 gatilhos ativos, apontando para o 1º nó) | pedido do dono: lead que atendeu o Power Dialer continuava na lista "Ligar pelo WhatsApp" até a SDR marcar o Resultado. O gatilho de ligação não pôde ser testado sem ligação real |
| listas | "Ligar pelo WhatsApp" (`1b41aFUhh6DYi8SAX0tC`) e "Fila do dia — SDR" (`pcawrltPew1bn3WIi37q`) excluem `falou-hoje`; cópias da Andreyna (`s2toTEDB1ATwN141VV8M`, `MFZ0A8m1ZsCpxnHb4LN8`) atualizadas por `POST api.leadconnectorhq.com/smartlist/update_shares` de dentro da sessão | Contatos | filtro novo | sim, nas 4 | PUT sem `sharedWith` (a API exige texto e texto já quebrou a tela). Cópia compartilhada não aceita PUT (403): só `update_shares` |
| atuador | `fila-sdr` exclui `falou-hoje`; rede de segurança: candidato da lista do WhatsApp que atendeu o discador (≥ 20 s, últimas 12 h) sem a tag entra no workflow da trava (`POST /contacts/{id}/workflow/{id}`) | PR #111 (mergeado) | — | Action rodou verde (0 casos) | o discador puxa `fila-tel` (decisão de 27/09); o `Pós-ligação v3` já tira `fila-tel` e as cadências em Atendeu/Pediu retorno |
| formulário primeiro | "Qualificação e agendamento — SDR" redireciona ao enviar para o calendário "Agendamento pela SDR"; o calendário passou a usar o formulário padrão (nome/telefone/e-mail) com contato fixo (`stickyContact`) | Formulários / Calendários | ação "mensagem" → "abrir URL"; formId do calendário → padrão | sim | pedido do dono: perguntas primeiro, dia e hora no final. **Envio não testado** (o formulário tem verificação Cloudflare; não se contorna) |
| link da SDR | "Abrir agendamento com a ficha preenchida" abre o **formulário** com 24 campos do CRM (contato, anúncio, N, B, A); corrigidas as chaves `investimento_mensal_em_anncios`/`investe_em_anncios` (estavam com "ú" e nunca preenchiam) | Fechar Horário v14→v15, Pós-ligação v3 v8→v9 | — | sim (3 links trocados, 0 velhos; prefill conferido na página) | `tools/gravar_link_form_primeiro.py` |
| horários | agenda do Pablo (schedule `xn2Wz3s2eBWulv7j4JXM`): seg–sex 18:00–22:00, sáb 09:00–12:00, dom fechado; os 2 calendários ligados a ela; intervalo 90 min | Calendários | 17:30–20:30 todo dia, a cada 30 min | sim: seg–sex 18:00/19:30/21:00, sáb 09:00/10:30 | `openHours` no calendário não gera sábado quando há schedule do usuário; a disponibilidade vale pela schedule |
| playbook | links, Passo 3 (lista se atualiza sozinha), Passo 5 (formulário → agenda), Qualificar e agendar, horários do closer | Claude Docs | rev 36 | sim | |
| roteiro do discador | "Roteiro SDR + ficha do lead" (`6ab9f0e9c4094d71a47295bd`): botão "Abrir ficha de {{contact.first_name}} e agendar" com o link do formulário preenchido (24 campos) + resumo do anúncio + roteiro em 5 blocos | Configurações → Telefone → Roteiros (rota `POST backend/phone-system/locations/{loc}/call-scripts`, `scriptContent: {contentType: "html", contentBody}`) | novo | sim: com `replaceVariables=true&contactId=<teste>` o link sai com os dados do lead | o painel Roteiro do Power Dialer busca com `replaceVariables=true&contactId` do lead na linha (lido no código do discador). É o caminho da SDR dentro do discador. `tools/criar_roteiro_discador.py` |

### Turnos flexíveis, grupo automático, metas e comissão (28/09)

| Item | O que foi gravado | Onde | Antes → depois | Relido | Observação |
|---|---|---|---|---|---|
| janela das automações | 16 workflows publicados: seg–sex 08:30–**21:00** (Pós-ligação v2, rascunho, intocado) | Automações | 08:30–18:30 | sim, 16/16 (backup em `.local/bkp-janela-28-09/`) | turnos das SDRs: 09–18 e 13–21 (dono) |
| turnos | `wesales/equipe.json` (SDRs, turnos, `tag_fila`, closer) + `tools/turnos.py`; governador: janela do WhatsApp automático = do 1º turno a 30 min antes do fim do último (hoje 09:00–20:30); atuador: lead novo (24 h, nunca tentado) de SDR fora do turno passa para SDR em turno, com as tarefas; com 2+ SDRs, tag `fila-tel-<nome>` por SDR | PR #112 e #113 (mergeados) | crons até 20:59 | simulado com SDR fictícia (1ª versão pegava os 38 antigos com contador vazio → limitado a 24 h) | só existe **uma** SDR com usuário (Andreyna). A SDR da manhã entra no `equipe.json` quando o usuário for criado |
| grupo com o closer | workflow "Grupo com o closer — tarefa da SDR" (`8ed2fc63-e542-4b9d-867e-6a2cd6b1799f`): reunião confirmada nos 2 calendários → tarefa `[GRUPO] Criar grupo com o closer — {{contact.first_name}}` para a SDR, prazo no dia | Automações | novo, publicado v3, sem janela | sim (2 gatilhos ativos) | concluir a tarefa = grupo criado (sem tag manual). Tarefa vai para a Andreyna; com 2 SDRs, rever |
| playbook | turnos + rotina da manhã; máquina acompanha os turnos; tag por SDR; tarefa [GRUPO]; motivos de desqualificação; comissão sobre a 1ª mensalidade paga (R$ 500 / R$ 1.000 por venda); planejamento out–dez (R$ 30k / 50k / 100k) e ganho da SDR com e sem 100 ligações/dia; listas "o que não está pronto" retiradas (pendências do dono, abaixo) | Claude Docs | rev 54 | sim | |

**Pendências do dono (fora do playbook da SDR):**
- Conta de anúncios do Meta com pagamento pendente e termos de lead da Página.
- Formulários do Meta: 5 de 9 sem mapeamento para o CRM (conferir só os de campanhas ativas).
- Criar o usuário da SDR da manhã no CRM e pôr o `userId` em `wesales/equipe.json`.
- Passagem depois de FORMALIZAR (quem assume, checklist) e modelos de proposta/contrato.
- Critério da premiação anual.
- Volume de leads para a meta (460 em out, 770 em nov, 1.540 em dez) e 2º closer ou mais horários a partir de novembro (agenda atual ≈ 74 reuniões/mês).

### Uma tag, uma lista, um botão (28/09, manhã)

| Item | O que foi gravado | Onde | Relido | Observação |
|---|---|---|---|---|
| uma tag no discador | a SDR puxa só `fila-tel`. Os 36 leads de 19–21/09 (entraram antes da Cadência Inbound, nunca receberam `fila-tel`) ganharam a tag `sem-cadencia`; o atuador põe `fila-tel` neles 1×/dia (sem ligação nas últimas 24 h), até 12 tentativas, **sem WhatsApp automático** (decisão do dono). Rede de órfãos: lead novo fora da cadência (2 h a 3 dias, Tentativa nº 0) entra na Cadência Inbound. `fila-sdr` aposentada (tirada dos 36) | PR #114 + Action aplicada | sim: 36 em `fila-tel`, `fila-sdr` 0, CONVERGIU | a Cadência Inbound não aceita reentrada (`allowMultiple: false`) |
| lista única da SDR | "Minha fila — SDR" (`lC5kjBoCH1J3Ze0VKsYe`): CONECTAR, sem perdido/não perturbe/`falou-hoje`, e (fila-quente OU fila-tel OU fechar-horario OU retorno-vencido OU 2+ tentativas tel sem conexão); ordem Prioridade ↓. Compartilhada com a Andreyna; as 5 antigas (Fila quente, Fila do dia, Ligar pelo WhatsApp, Fechar horário, Retornos vencidos) **descompartilhadas** dela (continuam do dono) | Contatos | sim: 36 na tela, ordenada | não apagadas |
| lista única do closer | "Minha agenda — Closer" (`GNlBCDC1iukze8m1bqOt`): REUNIÃO/NEGOCIAR/FORMALIZAR, sem perdido; ordem Data agendado ↑ | Contatos | filtros relidos | as 2 antigas do closer seguem existindo |
| botão WhatsApp | Roteiro do Power Dialer recriado (`6ab9fa95d6f0a71d7f123034`): botões "Abrir ficha e agendar" e "📱 Ligar pelo WhatsApp" (`api.whatsapp.com/send?phone={{contact.phone_raw}}`) | Roteiros | sim, com o contato de teste | o roteiro antigo (6ab9f0e9…) foi sobrescrito num teste e apagado; a SDR escolhe o roteiro de novo no painel |
| coluna com botão na lista | **não feito**: exige campo personalizado novo (regra do dono) e a lista não mostra link como botão | — | — | alternativa: botão no Roteiro + clique no nome abre a ficha |
| playbook | links, rotina, Passo 1 (uma tag + botão verde), Passo 3, regras | Claude Docs rev 64 | sim | |

### Vigia das rotinas (28/09)

| Item | O que foi gravado | Observação |
|---|---|---|
| rotina na nuvem | `trig_01RFBXPswYVRBvMvst3RqhZj` reaproveitada (antes: "rotina ativa", one-shot 28/09 08:30 com o estado superado de 27/09). Agora "WeSales — vigia das rotinas (avaliar e propor, sem publicar)", seg–sex 12:17 e 21:17 (São Paulo), sessão nova a cada rodada | lê Actions + CRM (só leitura), escreve em `wesales/SAUDE-ROTINAS.md` e, se houver decisão, cria **uma** tarefa "🩺 Rotinas — decisão dd/mm" para o Pablo. Proibido publicar/editar qualquer coisa no CRM |

### Playbook auto-explicativo e rotina "construção contínua" (28/09, madrugada)

| Item | O que foi feito | Observação |
|---|---|---|
| playbook | nova seção "Guia das telas" (Minha fila, Ficha, Call Center, Tarefas, Conversas — 4 capturas novas com nomes/telefones de leads borrados), glossário de tags (quem põe, o que significa, o que a SDR faz), passo a passo do grupo no celular (salvar lead e closer, criar, admin, convite por link) e sequência de mensagens no grupo da marcação ao pós-reunião | rev 65 |
| rotina "construção contínua" | lida, não alterada (pedido do dono: só entender). Nuvem, ~1 sessão/hora, branch `claude/amazing-johnson-mclksg`, escreve especificação (build-wesales.md, ROADMAP F-/G-/T-, APRENDIZADOS, APROVADO.md como freio), não escreve no CRM | diverge do que está publicado (ex.: F-27 especifica "chamada perdida" com Call Status; a Trava de canal já usa esse gatilho) |
| label GitHub | `para-claude` criada para pedidos do dono ao ciclo de melhoria | o agendamento local de hora em hora foi **negado** pelo controle de permissões (agente autônomo com escrita no CRM); fica para o dono liberar |

### Lista do closer corrigida e F-27 publicado (28/09, manhã)

| Item | O que foi gravado | Relido | Observação |
|---|---|---|---|
| lista do closer | "Minha agenda — Closer" mostrava 54 (a tela descartou o OU de etapas; "qualquer uma das tags" deu 0). Agora filtra só pela tag `closer-ativo`, mantida pelo atuador (oportunidade aberta em REUNIÃO/NEGOCIAR/FORMALIZAR) | sim, 2 na tela | PR #115 (atuador) mergeado |
| F-27 | workflow "Retorno de chamada perdida (F-27)" (`21206cc9-c01e-4845-9b62-ebbd06d14fc9`): Call Status entrada não atendida (no-answer/busy/canceled/voicemail) → se oportunidade aberta e sem `nao-perturbe`: Prioridade 5, `fila-quente`, tarefa `[LIGAR AGORA] Retornar ligação perdida` para o dono do lead. Sem janela, reentrada ligada | publicado v3, gatilho ativo | versão enxuta do F-27 da rotina "construção contínua" (PR #102): sem a mensagem MRC-1 (template Meta) e sem opção nova em Sinal recebido. **Não testado com chamada real** |
| F-24, F-25, F-26 | não publicados | — | e-mail não é canal da operação hoje (F-24/F-25); F-26 a própria rotina marcou travado no F-09 |

### PENDENTES-CRM (nuvem → local), 28/09 manhã

| Item | O que foi feito | Observação |
|---|---|---|
| 2 `fila-wa` | nenhum workflow publicado punha a tag; o atuador passou a manter (PR #116): CONECTAR, 1+ tentativa tel sem conexão, sem `falou-hoje`/`wa-feito-hoje`/`nao-perturbe` | 0 elegíveis hoje (contadores começam agora) |
| workflow novo | "WhatsApp tentado hoje" (`1c247efc-7f6f-4028-b328-6ab51103c3da`): Canal da tentativa = WhatsApp → `wa-feito-hoje` 12 h + tira `fila-wa` | 1 ligação de WhatsApp por lead por dia |
| 3 | Pós-ligação v3 já tira `fila-wa` (6 nós) | conferido |
| 1 visão em Conversas | **manual do dono** (admin cria e compartilha); passos no playbook | API não cria visão |
| playbook | Passo 3 da sessão da nuvem mantido; corrigidas 3 frases que diziam que a cadência põe `fila-wa` | rev 76 |
| ciclo /loop 1h | cancelado (job 74f7640a) por decisão do dono: melhorias discutidas na nuvem, aplicadas aqui 1–3×/dia | |

### Painel de ligação pelo WhatsApp (28/09)

| Item | Resultado | Observação |
|---|---|---|
| campos | "Canal da tentativa" 595→**10** e "Resultado da tentativa" 600→**20** (pasta da ficha): aparecem logo abaixo do Nome na coluna direita de Conversas | só posição (PUT sem parentId); `campos_bant.py` atualizado para não voltar |
| botão | o botão verde **"Ligar"** do cabeçalho da conversa é **"Ligar via WhatsApp"** (aria-label), da integração do WhatsApp (Stevo) | conferido na tela, sem ligar |
| visão | os leads têm conversa (amostra de 12 dos `sem-cadencia`: todos com conversa TYPE_PHONE) → aparecem na visão por tag | a visão ainda precisa ser criada/compartilhada pelo dono |
| registro | a ligação por WhatsApp **não deixa registro** no CRM (mensagens Stevo chegam como TYPE_CUSTOM_SMS; nenhuma chamada WhatsApp) | a medição de 40% depende da SDR marcar Canal = WhatsApp |

### Robôs nunca rodaram por agendamento (28/09 09:20)

| Achado | Correção |
|---|---|
| filas do discador, governador do WhatsApp e análises semanais **nunca rodaram por cron** (só manual); outros workflows do repo, em minutos quebrados, rodam | PR #117: filas `7,37 11-23 * * 1-5`, governador `13,43 11-23 * * 1-5`, análises `19 10 * * 1` (GitHub atrasa e descarta crons em :00/:30). Rodados à mão às 09:16: filas (CONVERGIU; `fila-wa` 0 — nenhuma ligação feita hoje ainda), governador e análises |
| visão "Ligar pelo WhatsApp" criada pelo dono em Conversas | fica vazia até a SDR ligar pelo discador e o lead não atender (regra: 1+ tentativa tel sem conexão) |

### Canais por toque — 50% ligação, 40% ligação de WhatsApp, 10% mensagem (28/09 09:30)

| Item | O que foi feito | Observação |
|---|---|---|
| regra | ligação de WhatsApp é **toque da cadência** (não "quem não atendeu"). Atuador: toque k = tentativas registradas (tel+WA)+1; WhatsApp nos toques 2,4,6,8,10 (tira `fila-tel`, põe `fila-wa`); telefone nos 1,3,5,7,9,11,12 | PR #118 |
| leads atuais | aplicado às 09:26: **14 dos 36 antigos na `fila-wa`** (paridade do id: metade começa pelo WhatsApp), 22 na `fila-tel`; CONVERGIU | alternam nos próximos toques |
| entrada na cadência | leads antigos entram na Cadência Inbound (fluxo completo, com mensagens) **1 por rodada**, seg–sex 09–18, só com toque de telefone no dia e só quando < 2 mensagens esperam o governador; perdem `sem-cadencia` | 1º: Ceuomar Delphino (09:26) |
| mensagens | governador: **1 por rodada** (era 2) e ~1/3 das rodadas puladas ao acaso quando não está atrasado → intervalo irregular (30/60/90 min + espera de 15 min do portão); limite 11–15/dia mantido | pedido do dono: não parecer robô |
| mistura atual | 12 ligações (7 tel / 5 WA) + 5 mensagens = 41% / 29% / 29%. **Próximo passo:** trocar 3 das 5 mensagens (MT4, MT8, MT11) por ligação de WhatsApp → 8/7/2 = 47% / 41% / 12% | exige editar portões das cadências; com ensaio antes |
| playbook | Passo 3: tabela de toques × canal, regra "toque de WhatsApp", 1 ligação de WhatsApp por lead por dia | rev 78 |
