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
