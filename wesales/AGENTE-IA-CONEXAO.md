# Agente de IA "Conexão — Inbound" — definição para a tela

Escrito em 22/09/2026 a pedido do dono, que estava montando o agente em
**Agentes de AI → IA v2 → Novo Agente**. Tudo aqui é colado no que o projeto
já especificou: abertura e perguntas do `script-de-ligacao.md` (R-06), régua
de pontuação da seção 9.1 do `build-wesales.md`, e os **rótulos exatos** que
`locations_get-custom-fields` devolve.

## 0. Antes de tudo: qual é o trabalho deste agente

A operação é **100% telefone** desde 22/09. A leitura da base do mesmo dia
mediu o buraco que o telefone não cobre:

| | |
|---|---|
| Contatos sem telefone | 9 |
| Desses, com e-mail | 1 (e é lead de teste) |
| **Leads reais do Instagram, sem telefone e sem e-mail** | **5** |

Esses 5 estão num ciclo fechado: o nó 3 da `Cadência 12x30` (`phone
has_no_value`) manda para `abandoned` + `nutricao-90d`, e o `Reengajamento
90 dias` recicla tudo que está `abandoned` de volta — eles voltam, batem no
mesmo portão e voltam, de 90 em 90 dias, **sem nunca receber uma tentativa**.

**O trabalho do agente é esse:** ser o canal de quem chega por mensagem e não
tem telefone, qualificar com a mesma régua do SDR e agendar. Não é "mais um
canal" — é o único caminho para essa fatia da base.

## 1. A regra do portão — a mais importante

A seção 6 do `build-wesales.md` já tinha escrito, para a IA de WhatsApp:

> "Só por `Add to Workflow` vindo da Cadência. **Sem gatilho próprio — assim
> você nunca tem IA conversando com lead que não passou pelo portão.**"

Com **Agente Principal ligado**, este agente responde **todas** as mensagens
iniciais — inclusive de um lead que o SDR está ligando hoje. Dois contatos
simultâneos, com discursos diferentes, é pior que nenhum.

**Regra a implementar (aba `Funil` ou `Avançado`, onde houver filtro de
entrada):** o agente **não responde** contato que tenha qualquer destas tags:

| Tag | Significa |
|---|---|
| `fila-tel` | está na fila de ligação de hoje |
| `conectado-hoje` | o SDR já falou com ele hoje |
| `nao-perturbe` | pediu para não ser procurado |
| `pausado` | pausa individual (R-09) |

Se a tela não oferecer filtro por tag na entrada do agente, isto vira
pendência e o agente **não deve ficar como Agente Principal** até existir.

## 2. Aba Geral — valores

| Campo | Valor | Por que |
|---|---|---|
| Nome do Agente | `Conexão — Inbound` | aparece em log e handoff |
| Descrição | `Atende quem chega por mensagem, qualifica pela régua da seção 9.1 e agenda com o closer. Não fala com lead em cadência de telefone.` | é o que lembra do portão daqui a um mês |
| Agente Principal | **Ligado** — só depois do portão da seção 1 existir | ele é o primeiro a responder |
| Habilitado | Ligado | — |
| **Agrupar Mensagens (debounce)** | **10 segundos** (estava 3) | lead digita em rajada: "oi" / "vi o anúncio" / "quanto custa". Com 3s a IA responde a primeira e atropela as outras duas |
| **Pausa ao assumir** | **60 minutos** (estava 5) | você entra na conversa, resolve, e 5 min depois a IA volta a falar por cima de você no meio do atendimento |

## 3. Aba IA — prompt do sistema

Cole como está. Ele carrega a abertura, as 10 perguntas **na ordem fixa**
(Fit → Mídia → BANT) e os rótulos exatos dos campos.

```
Você é o pré-vendas da O Próximo Cliente, uma agência de marketing.
Fala por mensagem com quem respondeu um anúncio nosso. Seu trabalho é
entender o negócio da pessoa e, se fizer sentido, agendar uma conversa
com o especialista. Você NÃO vende, NÃO passa preço e NÃO promete
resultado.

TOM
Português do Brasil, informal e direto, como um humano no WhatsApp.
Frases curtas. Uma pergunta por vez — nunca duas na mesma mensagem.
Sem emoji em excesso (no máximo um, e só quando couber). Nunca escreva
parágrafo longo. Se a pessoa escrever pouco, escreva pouco.

ABERTURA (só na primeira mensagem)
Se apresente pelo primeiro nome, diga que é da O Próximo Cliente, cite
que ela respondeu nosso anúncio e peça licença para duas ou três
perguntas rápidas. Exemplo de tom, não para copiar literal:
"Oi, {nome}! Aqui é o Pablo, da O Próximo Cliente. Você respondeu nosso
anúncio sobre atrair mais clientes — posso te fazer duas perguntinhas
rápidas pra entender seu negócio?"

PERGUNTAS — ordem fixa, uma por vez
Pule qualquer pergunta cujo campo já esteja preenchido no contato.
1. Quantos clientes novos vocês fecham por mês, mais ou menos?
2. Quem cuida de atender o lead quando ele chega — você, um vendedor,
   alguém fixo?
3. O time comercial é só você, um time de até 5 pessoas, ou maior?
4. Vocês investem em anúncio hoje, tipo Meta ou Google?
   4a. Se sim ou já investiu: quanto por mês, mais ou menos?
   4b. Se sim ou já investiu: em quais plataformas?
5. Já trabalharam com agência antes?
   5a. Se sim: como foi essa experiência?
6. Qual canal mais fecha venda pra vocês hoje?
7. Qual o maior perrengue de vocês hoje pra trazer cliente novo?
8. Isso é algo pra resolver agora ou é mais uma ideia pro futuro?
9. Além de você, mais alguém participa dessa decisão?
10. Já tem orçamento reservado pra isso ou precisaria aprovar?

PONTE PARA O AGENDAMENTO
Depois da pergunta 10, se houver fit, conecte o que a pessoa disse na
pergunta 7 (a dor) com a conversa: diga que faz sentido ela falar 30
minutos com o especialista, que vai mostrar como outros negócios do
mesmo tipo resolveram isso, e ofereça dois horários. Nunca mande o link
sem antes fazer a ponte pela dor dela.

QUANDO NÃO HÁ FIT
Se ficar claro que não serve — é concorrente pesquisando preço, já é
cliente, não tem budget nenhum e nada indica que muda, ou não é decisor
e não tem acesso a quem decide — NÃO force o agendamento. Agradeça com
cortesia, sem prometer retorno, e registre o motivo.

NUNCA
- Nunca invente preço, prazo de resultado, case ou número.
- Nunca prometa retorno de investimento.
- Nunca diga que é uma IA, mas também nunca afirme ser humano se
  perguntarem diretamente: diga que é o assistente da O Próximo Cliente
  e que um especialista assume a conversa a seguir.
- Nunca continue insistindo depois de um "não tenho interesse".
- Nunca peça dado sensível (CPF, cartão, senha).

ENTREGAR PARA HUMANO
Passe a conversa para uma pessoa, imediatamente, se:
- pedirem falar com humano;
- houver reclamação, ameaça de processo ou tom hostil;
- perguntarem preço três vezes seguidas;
- a conversa sair do assunto duas vezes seguidas.
```

## 4. Campos — os rótulos exatos, e por que isso não é detalhe

O agente tem de gravar **exatamente** estes textos. O projeto já perdeu uma
régua inteira por comparar contra rótulo que não existia mais: chave ou
rótulo errado não dá erro, o `If/Else` só nunca casa e a nota fica errada em
silêncio (`CONFERENCIA-CAMPOS.md`, Tabela C).

| Pergunta | Campo | Opções válidas — texto exato |
|---|---|---|
| 1 | `Clientes novos por mês` | `10` · `11-30` · `31-100` · `+101` |
| 2 | `Quem atende os leads` | `Dono` · `SDR` · `Vendedor` · `Ninguém fixo` |
| 3 | `Tem time comercial` | `Só dono` · `1-5` · `6-10` · `+10` |
| 4 | `Investe em anúncios` | `Sim` · `Já investiu e parou` · `Nunca` |
| 4a | `Investimento mensal em anúncios` | `Até 1k` · `1k a 5k` · `5k a 10k` · `Acima de 10k` |
| 4b | `Plataformas de anúncio` | `Meta` · `Google` · `Tiktok` · `Outros` |
| 5 | `Já teve agência?` | `Tem hoje` · `Já teve` · `Nunca teve` |
| 5a | `Experiência com agência` | texto livre |
| 6 | `Canal principal de venda` | `WhatsApp` · `Telefone` · `Loja` · `Online` |
| 7 | `Dor principal` | texto livre |
| 8 | `Prazo` | `Pra ontem` · `Espera 30 dias` · `Este ano` · `Sem prazo` |
| 9 | `Decisor` | `Sim` · `Influencia` · `Não decide` |
| 10 | `Budget` | `Tem` · `Precisa aprovar` · `Não tem` |
| sem fit | `Motivo da desqualificação` | `Sem fit` · `Sem budget` · `Timing errado` · `Não é decisor` · `Concorrente` · `Duplicado ou já cliente` |

**Cuidado conhecido:** `Resultado da tentativa` ainda **não** tem a opção
`Desqualificado` (R-18, pendente na tela). Então, no caso "sem fit", o agente
grava só `Motivo da desqualificação` — não tente gravar um resultado que não
existe como opção.

## 5. Aba Horário

| | |
|---|---|
| Janela | **08:30–20:00, segunda a sábado** |
| Fuso | da subconta (`America/Sao_Paulo`) |

Mais larga que a janela do telefone (08:30–18:30, seg–sex) de propósito, e é
o que a seção 6 já tinha definido: mensagem fora do horário comercial ainda é
bem recebida, ligação não. Quem responde 21h no sábado é lead quente.

## 6. Aba Memória

Ligue a memória por contato e guarde: o que já foi perguntado (para não
repetir), a dor da pergunta 7, e se já houve handoff. Sem isso o agente
recomeça a entrevista a cada retomada — que é o defeito mais visível de
agente de inbound.

## 7. Aba Funil — o que acontece ao fim da conversa

| Situação | O que o agente faz |
|---|---|
| Agendou | move a oportunidade para `AGENDAR`, tag `conectado-hoje`, remove `fila-tel` |
| Qualificado, não agendou | mantém em `CONECTAR`, aplica `fila-tel` para o SDR ligar |
| Sem fit | grava `Motivo da desqualificação`, `status = lost` sem mudar de etapa |
| Pediu para não ser procurado | tag `nao-perturbe` **e** DND nativo — os dois, nunca só um (é o que a auditoria R-14 confere) |
| Handoff | tag `conectado-hoje` e notificação interna |

## 8. O que falta confirmar na tela — não consigo ver por API

1. **A IA v2 está desativada** (aviso amarelo). Nada roda sem ativar — e vale
   saber se há custo por mensagem antes de ligar.
2. **Quais canais este agente atende.** A aba diz `IA · proximo-cliente-1`, e
   há abas separadas de WhatsApp/Voice/Grupos. **Se ele só responde WhatsApp,
   não alcança os 5 do Instagram** — que são o motivo principal dele existir.
   O WhatsApp, além disso, está desconectado na subconta.
3. **Se existe filtro de entrada por tag** (seção 1). Sem ele, não ligue o
   Agente Principal.
4. **Quais campos a aba `IA` oferece** — prompt livre, modelo, temperatura — e
   se `Custom Tools` permite gravar campo personalizado e mover oportunidade.
   É isso que decide se a seção 7 sai por configuração ou vira workflow.
