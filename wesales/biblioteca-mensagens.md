# Biblioteca de mensagens versionada — R-04

Fonte da verdade dos textos das 3 mensagens automáticas da Cadência 12x30
(`build-wesales.md`, seção 2.6). Em Reev/Meetime o template é objeto de
primeira classe, com desempenho próprio — aqui virava texto solto dentro do
nó do workflow, sem código e sem histórico. Este documento é o que fecha essa
diferença: cada texto tem um código, cada edição gera uma versão nova, e o
campo `Template usado` (C-23, `campos-e-tags.md`) grava qual saiu para cada
contato.

## Regra de versionamento

**Nunca edite um texto em vigor.** Editar o texto de `M1-v1` sem trocar o
código quebra a régua: toda resposta anterior à edição fica atribuída a um
texto que não existe mais, e a comparação de desempenho perde o chão. O
fluxo correto:

1. Escreva a nova versão numa linha nova, com código seguinte (`M1-v1` →
   `M1-v2`; variante de teste A/B do R-05 usa sufixo de letra, `M1-a`/`M1-b`,
   não número — os dois formatos convivem porque significam coisas
   diferentes: `-v2` substitui, `-a`/`-b` compete).
2. Marque a linha antiga como `Substituído em <data>` na coluna Status.
   Nunca apague a linha: é o histórico que permite comparar depois.
3. Troque o texto no nó de envio do workflow (`build-wesales.md`, seção 2.6)
   para o novo código.
4. Campo `Template usado` é `TEXT` (não `SINGLE_OPTIONS`) exatamente para
   este passo não exigir editar a lista de opções do campo na tela — o
   workflow escreve o código novo direto.

## Templates ativos

| Código | Canal | Nó de envio | Desde | Status |
|---|---|---|---|---|
| `M1-v1` | WhatsApp | Cadência 12x30 — T1, D1 08:45 | 18/09/2026 | Ativo |
| `M2-v1` | WhatsApp | Cadência 12x30 — após T8, D10 13:30 | 18/09/2026 | Ativo |
| `M3-v1` | WhatsApp | Cadência 12x30 — após T12, D30 17:45 | 18/09/2026 | Ativo |

## M1-v1 — abertura, pede permissão de ligar

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}.
> Vi que vocês trabalham com {{contact.segmento}} e queria te fazer 2 perguntas
> rápidas sobre captação de clientes. Posso te ligar hoje ou prefere por aqui?

Sem `[Agendar com o closer]` de propósito: é a mensagem que pergunta permissão
de ligar, e um link ali compete com a pergunta em vez de reforçá-la.

## M2-v1 — reforço

> {{contact.first_name}}, tentei falar com você algumas vezes e não quero ser
> chato. Uma linha só: hoje vocês trazem cliente novo mais por indicação ou por
> anúncio? Se for indicação, tenho um caso que talvez te interesse. Se preferir
> já reservar 30 min direto, sem esperar minha ligação: [Agendar com o closer]

## M3-v1 — encerramento

> {{contact.first_name}}, vou parar de te procurar por aqui. Se um dia quiser
> falar sobre captação, me responde esta mensagem que eu retomo de onde paramos.
> Ou, se quiser adiantar, o link continua de pé: [Agendar com o closer]
> Sucesso!

`[Agendar com o closer]` é o Trigger Link da seção 2.9 do `build-wesales.md`,
não texto literal — insira pelo ícone `{}` da caixa de mensagem, em Custom
Values → Trigger Links.

## Como isso responde o "Pronto quando" do R-04

"Dá para dizer qual abertura teve mais resposta" sem abrir mensagem por
mensagem: a interceptação de sinal do F-01 (`build-wesales.md`, seção 2.9.3)
já grava `Sinal recebido` = `Resposta de mensagem` toda vez que o lead
responde fora do fluxo normal, via gatilho nativo `Customer Replied`. A lista
inteligente `Resposta por Template` (`build-wesales.md`, seção 8.13) cruza
esse sinal com `Template usado` — contar linhas agrupadas por código responde
a pergunta, sem campo de contagem novo e sem planilha.

**Limite conhecido:** `Sinal recebido` é um campo único, não um log — se o
mesmo contato responder a M1 e mais tarde clicar num link (sinal de M2/M3), o
valor mais recente sobrescreve o mais antigo e a resposta a M1 some do filtro
`Resposta por Template`. É o mesmo limite já registrado no F-01
(`build-wesales.md`, seção 2.9.4) para `Sinal recebido` em geral; não é
específico deste item e não compensa criar um campo por sinal só para cobrir
o caso raro de dois sinais do mesmo contato antes de qualquer classificação.

## Quando a próxima versão nascer

Edite só a tabela "Templates ativos" e adicione a seção do texto novo abaixo
das existentes — nunca troque o texto de uma seção já publicada. Atualize o
nó de envio correspondente em `build-wesales.md`, seção 2.6, para o novo
código.
