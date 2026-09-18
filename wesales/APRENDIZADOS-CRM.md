# O que as execuções da rotina horária já descobriram

Memória entre rodadas. Antes de investigar de novo, procure aqui.

## Conector `GHL CRM` — confirmado nesta rodada (18/09/2026)

As ferramentas `mcp__GHL-CRM__*` **estavam presentes** nesta sessão. Rodei
`locations_get-custom-fields`, `contacts_get-contacts` e
`opportunities_get-pipelines` na subconta `1D53YTI9C7oIMBavcQxV` para
reconferir o estado antes de mexer no roadmap: 0 campos personalizados, 0
contatos, 1 pipeline (`FUNIL DE VENDAS`, o que já existia, não o
`Pré-vendas` do projeto). Bate exatamente com `auditoria-resultado.md` —
nada mudou na subconta desde a auditoria.

Se numa execução futura o conector **não** estiver na sessão, o problema
provável é o mesmo já resolvido antes (ver `rotina-horaria.md`): a rotina
precisa nascer com `GHL-CRM` anexado. Não é falta de acesso à subconta — é
falta do conector na sessão. Registre e siga com o item de backlog que não
depende do CRM, como a instrução manda.

## O que o conector cria e o que não cria (reconfirmado)

Sem mudança desde `auditoria-resultado.md`: 36 ferramentas, cria tag (via
`contacts_add-tags`), contato, atualiza oportunidade, lê tarefas, manda
mensagem. **Não cria** campo personalizado, pipeline, workflow, calendário,
formulário, trigger link. Etapas 2/3 (parte de campo) e a montagem de
`build-wesales.md` inteira continuam manuais por natureza da API, não por
limitação do conector.

## Pesquisa externa que valeu a pena guardar

- **`Trigger Link Clicked`** é gatilho nativo de workflow no GHL (Marketing →
  Trigger Links → criar link → usar como gatilho ou inserir via `{}` →
  Custom Values → Trigger Links dentro de uma mensagem). Não precisa de
  landing page nova: qualquer URL, incluindo a de um calendário já existente,
  vira um link rastreável.
- **`Customer Replied`** é gatilho nativo de workflow (não só um tipo de nó
  `Wait`), com filtro por canal (SMS, WhatsApp, e-mail) e por frase. Serve
  para reagir a uma resposta **sem** depender do fluxo em que ela chegou —
  é o que fecha a lacuna F-01 do roadmap sem inventar nada fora do GHL.
- Não confirmei se um campo `DATE` do GHL grava hora além da data (o mesmo
  dado que falta desde a lacuna L-01/S-01, `Data do retorno`). Documentado
  como ponto de atenção em `campos-e-tags.md` (C-14) em vez de assumir —
  quem criar o campo na tela confirma e atualiza esta nota.
