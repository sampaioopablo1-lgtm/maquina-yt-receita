---
name: economia-de-token
description: Onde cada trabalho deve rodar para gastar o mínimo de crédito do Claude — a escada Python/Jev/OpenCode/Claude, e a regra de Action empurra, Claude puxa. Leia antes de criar rotina, cron, trigger ou automação de qualquer tipo.
---

# Onde este trabalho deve rodar

Antes de automatizar qualquer coisa, desça a escada e pare no primeiro nível que resolve. Subir um nível sem precisar é desperdício medido, não teórico.

| nível | ferramenta | custo Claude | o que pertence aqui |
|---|---|---|---|
| **1** | Python em GitHub Action | **zero** | auditoria, relatório, contagem, exportar dump, mover etapa, qualquer coisa determinística |
| **2** | **Jev** (TypeSafe System One) | centavos | classificar, pontuar, decidir sim/não sobre texto curto |
| **3** | **OpenCode** | grátis / barato | edição de código rotineira, refactor mecânico |
| **4** | Claude | caro | diagnóstico, arquitetura, decidir o que fazer com um achado novo |

## A regra que mais economiza: Action empurra, Claude puxa

**Polling com LLM é o erro caro.** Até 23/09/2026 havia uma rotina de hora em hora que criava uma **sessão nova do Claude a cada disparo — 24 por dia** — para *ver se* algo mudou. Nas duas últimas noites ela produziu principalmente auditoria de documentação sobre si mesma, enquanto 42 leads envelheciam intocados.

E havia uma rotina diária que abria uma sessão do Claude para executar `python3 wesales/tools/auditoria_tudo.py` — um modelo de raciocínio para rodar um script que lê arquivos locais.

O certo é o inverso:

```
Action roda de graça no cron
  ├─ exit 0  nada mudou   -> ninguém é acordado
  └─ exit != 0            -> aí sim vale uma sessão
```

O código de saída é a campainha. Ver `.github/workflows/wesales-auditoria.yml`.

## Regras práticas

- **Nunca** ponha um agente num cron para "verificar" algo. Ponha um script, e deixe o agente ser chamado pelo resultado.
- Um alarme que dispara todo dia é um alarme ignorado. Achado real que espera decisão vai para a **linha de base** (`auditoria-base.json`) com o `porque` explicando que não está resolvido — e continua impresso no resumo. Vermelho só quando **muda**.
- Prompt de rotina é contexto pago a cada disparo. Se a rotina precisa de 60 linhas de contexto, o lugar disso é um `CLAUDE.md` ou uma skill, não o prompt.
- `wesales/CLAUDE.md` existe para uma sessão nova não reler 20.437 linhas. Mantenha-o curto; um CLAUDE.md longo derrota o próprio propósito.
- Modelo: Haiku/Sonnet para varredura e trabalho mecânico. Opus quando a decisão é difícil.

## O que o Jev NÃO faz

Não reduz o consumo do Claude por substituí-lo dentro de uma sessão. Ele **absorve decisão repetitiva que hoje acorda o Claude** — é assim que economiza. Confundir as duas coisas leva a esperar economia que não vem.

Custo hoje: `jev-1.13-free` pelo OpenCode Zen é **gratuito por tempo limitado**. Quando sair do ar, responde 404/410 — os scripts avisam explicitamente (`avisa_free_acabou`), e `JEV_MODEL=jev-1.13` opta pelo pago.
