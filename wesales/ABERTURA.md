# Abertura da operação — o que está armado e o que falta decidir

Escrito em 27/09/2026 01:15 UTC (sáb 26/09 22:15 São Paulo) para a próxima
sessão não redescobrir. **Leia só isto para a abertura**; o resto está no
`build-wesales.md` §2.42 a §2.46.

## O risco, em uma frase

**36 execuções da `Cadência Inbound` estão paradas no nó 24 (`WhatsApp · MI-0`)
e disparam JUNTAS quando a janela abrir** — próxima abertura **segunda 28/09
08:30**, porque a janela das duas cadências é `days [1,2,3,4,5]` 08:30-18:30.

Isso contraria a rampa de **6/dia** que o dono decidiu em 23/09
(`ESTADO-E-PLANO.md` linha 177, `PLANO-MULTICANAL.md` linha 93).

## Por que a janela é a única alavanca

| tentativa | por que não funciona |
|---|---|
| mover o lead para `NOVO LEAD` | a trava `MI-0 · Ainda vale mandar?` é o **nó 21** e já foi avaliada na entrada (24/09 00:53); a execução parou no **nó 24**, depois dela. Voltar de etapa **não desinscreve** |
| mover e devolver na terça | `Inbound` tem `allowMultiple: false` (não reinscreve) e `12x30` tem `true` (**reinscreve**) → duplica a 12x30 |
| tag `pausado` | os portões que a leem estão nos toques, **depois** do nó 24 |

**Resta a janela**, que alcança execução já parada sem tocar em contato:
`patch_janela_abertura.py --fechar --aplicar` deixa `days: [2]` (só terça).
Ou pela tela: `Automation → cadência → engrenagem → Execution window → só Ter`.

**Não roda por MCP nem por Action:** editar workflow usa a API interna, com
bearer de sessão logada (`.local/_ghl_bearer.txt`, navegador headless). Todos os
domínios do GHL estão bloqueados pelo proxy deste contêiner (testado: `000`).
O MCP funciona porque roda **fora** do contêiner — e não tem ferramenta de
workflow.

## Duas decisões do dono, pendentes

**1. A data.** O `PLANO-MULTICANAL.md` diz **segunda 28/09** com lote de 6. Em
27/09 o dono disse **terça** em chat. Não resolvido. `days: [2]` serve para
terça e é seguro para as duas leituras.

**2. DND nos 30**, para respeitar a rampa de 6/dia. Lista pronta, por ID exato.

### Lote 1 — fica LIVRE para disparar (os 6 que o plano nomeia)

```
7ECnj1bSeEIm5P58Ifd9  Carlos Andrade
WOf6FTgB36ZhjtQ6foM8  Gerson De Souza Pia
rXiVo6Y6eaxP8weJtETr  Ana Ruth
Kf4yk8YQQDGWaGXVsxrw  Ricardo
spaz4KnmixKJEMwYSzAv  Andreia
127LTEsNLqHby6k6LMHe  Andre
```

### Recebe DND — 30 contatos

```
["lqxkp4EdUdBRPr83JYhn", "9RLeKfPDe6yE49RLOO7u", "SxX69gKO2G5AWyVAPOjh", "YlPqam7AalWJqEpL6emi", "M55h4I5eclbmNIMgFSnv", "hkO0ENFbA375WhekeMWH", "sEaRRkZn5TV1Jw2IU3rv", "fb8vCRpBeAySCBAoMO4F", "yjqB57Ld0bsYLBa8E3jz", "1Gf0H1BRNrXIoXTe6t40", "ADlcS8hdZnBXTYhARKy9", "L70kMS9JSharFXQSijVL", "gtufwlEa5yNgrzgu4IKm", "RO26ZaQ3tiyrvDp1LAjr", "ofGSGKq3yASwxq2nsupn", "t2nDfQZzqv7OajSodU9B", "zZkWlOHbfmohz1JsmJzR", "tNDkZGkMtEDYcw8qxxQW", "wovEnOmNpccbCHHC1eED", "zN97QTlkYwSMllJYxkCQ", "JdohMHlLRig0s78t5cxt", "ossJg7kUN0rrKF59sx0m", "ziI1XTJh4UvIUGTUppXZ", "3ufCFsY8ASh3BbwRb5Ld", "GhMa7O5TZfIG3CORZNdE", "tcphhGxOgj7sF0P7cI92", "Gth7ccWeUcSPEu6QDUGi", "wZabWXgjVzW7AjRYnZ8L", "OfHQEWxgxjUC1cIurwzO", "0l6KtdWoSpOIMn1CeeAw"]
```

**Limite não medido, e é o motivo de pedir confirmação:** não se sabe se o DND
faz a execução parada **falhar e parar** ou **pular e seguir**. A segunda
possibilidade queima a MI-0 em silêncio. Sugestão registrada: deixar 1 livre na
abertura e medir, em vez de descobrir com 30.

## Já feito, não repetir

- `Rafaela de Paula - We Sales` (`d0ZJyFlxl1GZNDUiICnt`), a atendente da própria
  plataforma: `dnd: true`, `nao-perturbe` adicionada, `fila-quente` removida,
  em 27/09 01:08. O Jev a classificou `suporte_ou_fornecedor` 0.89.
- `Teste Não Atende`: já tinha proteção.
- Tarefas na etapa `CONECTAR`: **1**, do contato de teste. Duplicidade **não** é
  o risco aqui.
