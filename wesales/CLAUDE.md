# WeSales — leia isto antes de abrir qualquer outro arquivo

Operação de SDR no WeSales (GoHighLevel white-label). Subconta
**`1D53YTI9C7oIMBavcQxV`** — toda chamada MCP exige esse `locationId`.

Existem **20.000+ linhas** de documentação aqui e o gatilho horário cria uma
**sessão nova a cada disparo**. Este arquivo existe para você não reler tudo:
vá direto no que a pergunta pede.

## Regras que não se negociam

1. **Nunca exclua** contato, campo, tag ou workflow existente.
2. **Nada entra no CRM que não esteja `[x]` no `APROVADO.md`.** Linha que você
   mesma acrescentar nasce `[ ]`; só o dono troca para `[x]`.
3. Antes de **criar ou alterar em massa**, liste o que fará e peça confirmação.
4. Campo ou tag com nome parecido já existindo: **pergunte** se reaproveita.
5. Só mexa em `wesales/`. Nunca force-push, commit vazio ou teste desabilitado.
6. Operação não suportada pelo MCP: diga claramente e escreva o passo a passo
   manual no documento.
7. Responda em **português do Brasil**, com tabelas quando ajudar.

## Comece sempre por aqui (1 comando)

```bash
python3 wesales/tools/auditoria_tudo.py
```

| saída | significa |
|---|---|
| 0 | nada novo — o esperado |
| 1 | **achado NOVO** — o único caso que merece interromper alguém |
| 2 | algo foi consertado — atualize `auditoria-base.json` no mesmo commit |
| 3 | **alguma auditoria QUEBROU** — conserte antes de ler o resto |

Ele roda as cinco auditorias somente-leitura e compara com
`tools/auditoria-base.json`. Achado que já está na base **não é novidade** — o
dono já tem na fila. Não reporte de novo.

## Qual arquivo para qual pergunta

| pergunta | arquivo |
|---|---|
| o que estou autorizada a escrever no CRM? | `APROVADO.md` |
| o que está na fila do dono? | `ROADMAP-SALES-ENGAGEMENT.md` |
| por que isso foi feito assim? | `build-wesales.md` (seções `## 2.x`) |
| que erro já cometemos aqui? | `APRENDIZADOS-CRM.md` |
| que campos e tags existem? | `campos-e-tags.md` |
| que workflows existem e o que cada nó faz? | `INVENTARIO-WORKFLOWS.md` |
| o que o SDR vê na tela? | `GUIA-SDR.md` |
| textos das mensagens | `biblioteca-mensagens.md` |

## Armadilhas já medidas — não redescubra

- **Achado tirado de dump é CANDIDATO, não item.** `workflows-json/` é
  fotografia. Confirme ao vivo antes de reportar. O descolamento corre nos dois
  sentidos: já tratei dump de workflow morto como defeito vivo, e já existiu
  workflow publicado que nenhum documento catalogava.
- **`workflows-json/` não tem só workflow.** O `_campos.json` é uma *lista*.
  Varredura sem `isinstance(dado, dict)` quebra com `AttributeError` — foi
  assim que as cinco auditorias morreram em silêncio por 2 dias.
- **Conferência que você escreve só pega o defeito que você imaginou.** A única
  resposta que não se engana é a da conta: `put()` (em
  `tools/patch_funil_reuniao.py`) **levanta `RuntimeError`** se o PUT for
  recusado. Não engula a resposta.
- **Condição de oportunidade só funciona se o gatilho a carregar**
  (`pipeline_stage_updated`, `opportunity_status_changed`). Em qualquer outro
  gatilho, "Pipeline stage is X" lê vazio e dá **sempre falso**, sem erro. Use
  as tags do `Espelho de Etapa`.
- **Voltar a oportunidade de etapa NÃO desinscreve** do workflow.
- **`remove_from_workflow` cancela os passos pendentes** do alvo: os nós de
  saída dele não rodam, e a tag que ele limparia fica permanente.
- **O MCP não cria nem edita** workflow, lista inteligente, campo, pipeline ou
  calendário. Isso é tela, ou script `tools/patch_*.py` com `--aplicar`.

## IDs fixos

```
subconta   1D53YTI9C7oIMBavcQxV
pipeline   0Fo2xbeayE4EP6yuSUtq   (FUNIL DE VENDAS)
NOVO LEAD  7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d
CONECTAR   deb60542-a5cd-43ae-b875-b467b120a72c
REUNIÃO    3d26fcd1-220d-49ed-8325-705dfe9055b1
NEGOCIAR   cbcf0229-5e19-4fdb-8c50-6c641b78b3bb
FORMALIZAR b8485ec0-98e8-459f-b990-f40a5e3bd25b
```

## Convenção de escrita

`build-wesales.md`: **só acrescente no fim**, em seção `## 2.x` nova. Sessões
paralelas editam parágrafos no meio — assim ninguém colide.
