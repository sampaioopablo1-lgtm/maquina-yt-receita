# Prompt para o Claude da extensão do Chrome — itens de tela da abertura

Cole o bloco abaixo no Claude da extensão, com o Chrome já logado no WeSales CRM.
Ele cobre os itens **2, 4, 5, 6 e 8**. O item 7 (G-04 opção B) **não está aqui de
propósito** — a razão está no fim deste arquivo.

---

Você está no WeSales CRM (app.wesalescrm.com), subconta `1D53YTI9C7oIMBavcQxV`.
Vou te pedir cinco ajustes de tela. A abertura da operação é terça 29/09, então
precisão importa mais que velocidade.

## Regras que valem para tudo, sem exceção

1. **Nunca excluir nada.** Contato, lead, oportunidade, campo, tag, workflow,
   pipeline: nunca. Todos os leads vieram de campanha paga no Meta Ads — cada
   contato é dinheiro já gasto. Descartar é `status = lost`, e a etapa fica onde
   está. Se algum passo parecer exigir exclusão, pare e me pergunte.
2. **Nunca ligar recurso de IA do GHL** (Conversation AI, Voice AI, Reviews AI,
   Funnel AI). Custa por uso e não foi aprovado.
3. **Não crie nem renomeie campo personalizado.** A estrutura de campos é gerida
   por script, contra um snapshot versionado de 57 campos; campo criado na tela
   quebra a automação no próximo run.
4. **Depois de cada salvamento, releia a tela e me diga o que ela mostra** — não
   o que você clicou. Se divergir do que eu pedi, pare e me avise antes de seguir.
5. **Não toque no formulário nativo `Qualificação SDR`.** Ele não é usado e não
   deve ser apagado. A ficha do contato é o formulário.

## Item 2 — Call Center: gatilhos e fila

Ícone do Call Center no menu lateral → **Gatilhos**:

| Gatilho | Estado | Aplicar tag(s) | Ativar workflow |
|---|---|---|---|
| Ligação feita | **ligado** | `conectado-hoje` | vazio |
| Ligação recebida | **ligado** | `conectado-hoje` | vazio |
| Ligação perdida | **desligado** | — | — |

Salvar os gatilhos. Depois → **Fila de ligações**:

- `TOQUE MÁX. (s)` = **30**
- `PAUSA ENTRE LIGAÇÕES (s)` = **3**

Releia e confirme os cinco valores.

## Item 5 — publicar o workflow `Reunião Cancelada`

Automações → `Reunião Cancelada`. Ele está em **rascunho**, com 10 nós, e está
completo. Revise se os 10 nós estão lá e **publique**. Não altere nenhum nó.
Me diga quantos nós você contou e se o estado virou publicado.

## Item 4 — campos BANT no `Pós-agendamento v2`

Automações → `Pós-agendamento v2`. Dois nós recebem o mesmo bloco de texto:

1. o nó de **NOTA** `REUNIÃO AGENDADA`
2. o nó de **AVISO INTERNO** de 30 min antes

Acrescente ao texto existente (não substitua) estas 13 linhas. **Copie, não
digite**: as chaves internas do GHL perdem acento de forma irregular, e um merge
field errado renderiza **vazio, sem dar erro nenhum**.

```
Necessidade: {{contact.necessidade}}
Dor principal: {{contact.dor_principal}}
Clientes novos por mes: {{contact.clientes_novos_por_ms}}
Quem atende os leads: {{contact.quem_atende_os_leads}}
Tem time comercial: {{contact.tem_time_comercial}}
Urgencia: {{contact.urgncia}}
Prazo: {{contact.prazo}}
Investimento mensal em anuncios: {{contact.investimento_mensal_em_anncios}}
Investe em anuncios: {{contact.investe_em_anncios}}
Budget: {{contact.budget}}
Decisor: {{contact.decisor}}
SDR responsavel: {{contact.sdr_responsvel}}
Empresa: {{contact.empresa}}
```

**Não altere** condições, contadores, nem a fórmula da nota. Salve e publique.

Confirme relendo: as 13 linhas estão nos DOIS nós, e nenhuma delas está com
acento nas chaves (`urgncia`, `anncios`, `sdr_responsvel`, `clientes_novos_por_ms`
estão certos assim, sem acento — é o GHL que corta).

## Item 6 — o texto da tarefa T1 manda clicar num botão que não existe

Procure o nó de **tarefa T1** (no workflow de cadência de primeira tentativa). O
texto dela manda clicar em **"Ligar via WhatsApp"**. Esse botão **não existe nesta
conta**: o WhatsApp aqui não é a Cloud API oficial, e a WhatsApp Business Calling
API exige a oficial.

Corrija para que **telefone seja o passo 1** do texto. Mantenha o resto da
instrução como está — é só a troca do canal do primeiro passo. Salve e publique.

Me mostre o texto antes e depois.

## Item 8 — conferir a ficha de um lead

Contatos → abra `Gerson De Souza Pia`. Confirme que a ficha mostra a pasta com os
campos na ordem N / T / B / A, e me diga:

1. `N · Necessidade (anúncio)` está preenchido ou vazio?
2. O que está em `B · Investimento mensal em anúncios (anúncio)`?
3. Existe um campo `B · Quanto pode investir`, e em que posição ele aparece
   (deve estar logo depois do `B · Investimento mensal`)?

Não preencha nada. É só leitura.

---

# Por que o item 7 (G-04 opção B) NÃO está no prompt

O item 7 muda a régua da `Nota de qualificação` (§9.1 do `build-wesales.md`), e
essa régua tem **consequência automática**: a faixa 0–24 grava `status = lost` e a
25–44 grava `abandoned` com tag `nutricao-90d`. Uma régua errada não dá erro —
ela descarta lead pago em silêncio.

A opção B diz "a §9.1 passa a ler `Urgência`/`Necessidade` por `Contains`", mas
**não diz quantos pontos cada texto do anúncio vale**. Os valores que o Meta grava
em `Investimento mensal` são `Acima de 10k`, `Abaixo de 5k`, `Até R$ 1.000` e
`Não invisto nada ainda`; a tabela do Bloco B pontua os degraus da picklist
(`Acima de 10k`=12, `5k a 10k`=10, `1k a 5k`=6, `Até 1k`=2). O mapeamento entre os
dois conjuntos é decisão de negócio, não de configuração, e um `Contains` mal
ordenado erra sozinho: `5k a 10k` contém tanto `10k` quanto `5k`, então a ordem
dos portões decide o resultado.

Passar isso para um agente de tela sem os números fechados é pedir para ele
inventar a régua. Fica para depois da decisão do dono.
