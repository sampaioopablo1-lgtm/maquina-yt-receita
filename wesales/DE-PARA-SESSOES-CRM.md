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
