# Saúde das rotinas — histórico do vigia

Escrito pela rotina na nuvem "WeSales — vigia das rotinas (avaliar e propor, sem publicar)"
(`trig_01RFBXPswYVRBvMvst3RqhZj`), seg–sex ~12:17 e ~21:17 (São Paulo). Ela **lê e propõe**;
quem publica no CRM é o dono. Cada entrada traz só o que mudou desde a anterior.

## Linha de base — 28/09 02:40 (sessão local)

- Filas do discador (Action): última rodada aplicada 05:25 UTC, CONVERGIU. `fila-tel` 37
  (36 `sem-cadencia` + 1 da cadência), `fila-sdr` 0 (aposentada), `fila-closer` 2, `falou-hoje` 0.
- Governador do WhatsApp: janela do dia 09:00–20:30 (turnos em `wesales/equipe.json`).
- Listas: "Minha fila — SDR" 36 contatos; "Minha agenda — Closer" gravada (tela não conferida).
- Workflows novos em observação: Trava de canal — falou hoje; Grupo com o closer — tarefa da SDR;
  Retorno — prazo de 3 dias; Formalização Parada.
- Ainda não testado com dado real: gatilho de ligação atendida (Trava), tarefa [GRUPO],
  envio do formulário → agenda, botões do Roteiro no discador.

## 01/10 09:45 (SP) — vigia

**Rotinas**
- ⚠️ **Mudança de arquitetura não registrada**: "filas do discador" e "governador" **não têm mais rodadas desde 28/09** (última 17:00 UTC, manuais). Quem roda agora é `WeSales - relogio (filas + governador a cada 30 min)`: laço de ~5,5 h que se relança sozinho (22 rodadas; as `schedule` aparecem "cancelled" por design, as `dispatch` do bot fecham em success). Cobertura contínua: 30/09 17:07 → 01/10 07:21 UTC sem buraco, ciclos de 30 min, sem falha. Rodada 22 em andamento desde 07:21 UTC. ✅
- ✅ Veredito das filas: CONVERGIU em todos os ciclos lidos. Fora do horário (21:14→) o ciclo só faz Calendly/formulário. "Análises semanais" (seg 07:00): não houve segunda desde a última entrada; conferir 05/10.
- ⚠️ Branch padrão: "Ciclo — informe e disparo da frota" falhou 27/60 e "Diagnóstico dos 3 pilares" 5/60 — são da máquina de YouTube, não do WeSales; só registro.

**Números (relógio 30/09 17:07 → 22:16; CRM 01/10 09:45)**
- Trava: "rede da trava de canal" 0 contatos; "sem cadência: 0 lead(s) com toque hoje". Mas no CRM a tag `sem-cadencia` ainda está em **36** contatos e `fila-tel` em 11 (19 `fila-quente`, 18 `fila-wa`, 38 `fila-travada`, 8 `fila-closer`). `falou-hoje`: 0.
- CONECTAR: 57 contatos `etapa-conectar`, **todos os 57 com `atraso-1a-tentativa`**. 84 em `cad-inbound`.
- **Rede de órfãos: os mesmos 4 leads (g1GRGO4h…, rDdjNJj8…, FHQa3ti8…, dQ8vtdPH…) "entram na Cadência" em TODO ciclo por 5 h** — não saem da lista.
- "entrada gradual: PAUSADA (Cadência em diagnóstico)".
- Reuniões: Calendly 1 futura ativa; no-show 3/6 em 02/10 (2 contatos `noshow-6x15`). `etapa-reuniao` 6.
- Não medido nesta rodada (limite de leitura do conector): tarefas vencidas [GRUPO]/[WHATSAPP MANUAL]/[LIGAR AGORA]; leads novos >1 h sem tentativa.

**PROPOSTAS PARA O DONO**
1. Órfãos repetidos: a rede reaplica a mesma ação sem efeito (a Cadência está "em diagnóstico"/pausada, então a entrada não "pega"). Decidir: retomar a Cadência ou fazer a rede só registrar 1x e parar de repetir (ruído de log + risco de reentrada duplicada quando reativar).
2. `atraso-1a-tentativa` em 57/57 e `sem-cadencia` em 36 com "0 toque hoje": a tag de atraso parece não ser limpa ao haver tentativa, ou ninguém ligou. Conferir com a SDR se há ligações; se sim, o atuador deveria tirar a tag.
3. Documentar no DE-PARA que o relógio substituiu as Actions agendadas de filas/governador (hoje o vigia e o dono podem achar que "não rodam").
4. Não criei a tarefa 🩺 no CRM: o conector desta sessão só tem leitura de tarefas (sem criar). Esta entrada é o canal.
