# Script de ligação e playbook de objeções — R-06

Fonte da verdade do que o SDR **fala** numa ligação (telefone ou ligação por
WhatsApp — as duas são canal de voz na cadência, ver `briefing-sdr.md`). É o
par falado de `biblioteca-mensagens.md`, que é o texto escrito: lá é a
mensagem automática, aqui é o roteiro humano. Antes deste documento, a
ligação existia só como consequência no workflow (`build-wesales.md`, seção
4, ramo `Atendeu`) — o que acontece *dentro* da ligação nunca tinha sido
especificado.

## Por que não é só "um roteiro"

Pesquisado antes de escrever: em Reev, Meetime, Outreach e Salesloft o script
de ligação e a régua de qualificação (BANT/MEDDIC) são dois objetos
separados — o SDR segue um roteiro na conversa e, **depois de desligar**,
preenche o formulário de qualificação de memória. É o ponto onde a régua
perde precisão: o SDR reconstrói a nota, não a mede em tempo real, e quanto
mais ligações no dia, mais a reconstrução vira chute. Aqui o script segue a
**mesma ordem e o mesmo agrupamento** dos blocos de pontuação da seção 9.1 do
`build-wesales.md` (Fit → Maturidade de mídia → BANT) — cada pergunta falada
é o campo que ela grava, na ordem em que a régua soma pontos. O SDR não
preenche um formulário depois da ligação: ele já está preenchendo enquanto
fala, porque a pergunta 3 é literalmente o rótulo do campo `Q-04` lido em voz
alta. Um concorrente olhando a tela vê "o SDR segue um script"; não vê que a
ordem do script é a ordem da fórmula de pontuação, e que isso é o que faz a
nota nascer certa na primeira vez, não corrigida depois.

A ordem também não é arbitrária dentro da lógica de venda: pontuação sobe de
Fit (30) para Mídia (25) para BANT (45), e a conversa segue a mesma
progressão — pergunta fácil de responder primeiro, pergunta sensível
(orçamento, decisor) por último, quando já existe rapport. As duas
progressões coincidirem é o que faz o script soar natural e ainda assim
alimentar a régua sem esforço extra do SDR.

## 1. Antes de discar

- Confira `Segmento`, `Site` e `Instagram` do contato — normalmente já vêm
  preenchidos da origem do lead. Se estiverem vazios, pergunte só o que
  faltar durante a ligação; não interrompa a abertura para isso.
- Tenha a tela de `Resultado da tentativa` (`campos-e-tags.md`, C-02) aberta
  para classificar assim que a ligação terminar — é o campo que dispara o
  Pós-ligação (`build-wesales.md`, seção 4).

## 2. Abertura

Vale para toda tentativa de telefone ou ligação por WhatsApp que for
atendida (o gatilho do bloco abaixo é a ligação conectar, não importa a
tentativa `T{n}`).

> Oi, {{contact.first_name}}? Aqui é o {{user.first_name}} da
> {{location.name}}. Te liguei porque vi que vocês trabalham com
> {{contact.segmento}} e queria entender rapidinho como está a captação de
> cliente novo aí — tenho só 2 minutos, pode ser?

Se a resposta for "pode": segue para a seção 3. Se for "não tenho tempo
agora" ou qualquer variação de recusa: vai para a objeção 1 da seção 5.

**Detalhe de digitação que decide a ordem da fila:** quando o lead pedir para
ligar em outro horário, anote em `Hora do retorno` **sempre com dois dígitos**
— `09:30`, nunca `9:30`. O campo é `TEXT` (o GHL descarta a hora em campo
`DATE`, por isso o par), e `TEXT` ordena por letra: `9:30` cai **depois** de
`14:00` na lista `Retornos`, porque `'9'` vem depois de `'1'`. O placeholder da
tela já mostra `HH:MM`; esta linha existe porque o placeholder não impede.

### ⚠️ Aviso de gravação — pendência aberta em 22/09/2026, **decisão do dono**

**Se as ligações passarem a ser gravadas, esta abertura muda, e este é o
lugar da mudança.** O F-06 (`build-wesales.md`, seção 2.27) mede duração
real de chamada pelo gatilho `Transcript Generated`, que só existe para
chamada **gravada** — a transcrição depende da gravação estar habilitada no
número. Gravar ligação com lead no Brasil é tratamento de dado pessoal sob a
LGPD e pede, no mínimo, aviso ao interlocutor no início da chamada e uma
base legal declarada (legítimo interesse ou consentimento).

Consequência prática para este roteiro: o aviso entra exatamente aqui, nos
primeiros segundos — que são o ativo mais escasso de uma ligação fria. Não
é um acréscimo neutro ao texto acima; concorre com o gancho que o R-05 vai
otimizar.

**Não escrevo a frase.** Redação e base legal são do dono ou de quem o
assessora — não é dedução que uma rodada automática deva fazer sozinha. O
que fica registrado é onde ela entra e o que ela custa. Enquanto o F-06 não
for ligado (os campos C-29/C-30 nascem `[ ]` em `APROVADO.md`), a abertura
acima vale como está: **hoje nada é gravado.**

Quando o R-05 (`build-wesales.md`, seção 2.6.1) declarar um vencedor entre
`M1-a` e `M1-b`, revise esta abertura para usar o mesmo gancho da mensagem
vencedora — os dois canais (mensagem escrita e ligação) falando com ganchos
diferentes desperdiça o aprendizado que o teste A/B pagou para descobrir.

### Se cair na caixa postal

Deixe recado curto, não repita a ligação na mesma hora, deixe o próximo
canal da cadência (`build-wesales.md`, seção 2.5) seguir seu curso:

> Oi {{contact.first_name}}, aqui é o {{user.first_name}} da
> {{location.name}}. Te liguei rapidinho sobre captação de clientes pra
> {{contact.segmento}}. Vou te mandar uma mensagem por aqui também —
> qualquer coisa, me chama.

Classifique `Resultado da tentativa` = `Caixa Postal`.

## 3. Perguntas de diagnóstico

Ordem fixa: Fit → Maturidade de mídia → BANT, espelhando a seção 9.1. Pule
qualquer pergunta cujo campo já esteja preenchido no contato.

| Ordem | Pergunta falada | Grava no campo | Bloco (peso, seção 9.1) |
|---|---|---|---|
| 1 | "Hoje, mais ou menos quantos clientes novos vocês fecham por mês?" | `Clientes novos por mês` (Q-04) | Fit (30) |
| 2 | "E quem cuida de atender o lead quando ele chega — é você, é vendedor, tem alguém fixo nisso?" | `Quem atende os leads` (Q-11) | Fit (30) |
| 3 | "O time comercial de vocês é só você, um time de até 5 pessoas, ou maior que isso?" | `Tem time comercial` (Q-10) | Fit (30) |
| 4 | "Vocês chegam a investir em anúncio hoje, tipo Meta ou Google?" | `Investe em anúncios` (Q-05) | Mídia (25) |
| 4a | *Se `Sim` ou `Já investiu e parou`:* "E mais ou menos quanto por mês?" | `Investimento mensal em anúncios` (Q-06) | Mídia (25) |
| 4b | *Se `Sim` ou `Já investiu e parou`:* "Em quais plataformas — Meta, Google, TikTok?" | `Plataformas de anúncio` (Q-07) | — (apoio, sem peso) |
| 5 | "Já chegaram a trabalhar com agência antes?" | `Já teve agência?` (Q-08) | — (apoio) |
| 5a | *Se `Tem hoje` ou `Já teve`:* "Como foi essa experiência?" | `Experiência com agência` (Q-09) | — (apoio, alimenta a objeção 2) |
| 6 | "Hoje o principal canal que fecha venda pra vocês é WhatsApp, telefone, loja física?" | `Canal principal de venda` (Q-13) | — (apoio) |
| 7 | "Se eu te perguntasse qual é o maior perrengue de vocês hoje pra trazer cliente novo, qual seria?" | `Dor principal` (Q-16) | — (apoio, é o gancho da ponte) |
| 8 | "Isso é algo que vocês querem resolver agora, ou é mais uma ideia pro futuro?" | `Prazo` (Q-17) | BANT (45) |
| 9 | "Além de você, tem mais alguém que participa dessa decisão?" | `Decisor` (Q-15) | BANT (45) |
| 10 | "Vocês já têm orçamento reservado pra isso ou precisaria aprovar em algum momento?" | `Budget` (Q-14) | BANT (45) |

`Usa CRM` (Q-12) não tem pergunta própria: se surgir naturalmente na
conversa (ex.: "hoje anoto tudo numa planilha"), registre; não vale
interromper o roteiro para uma pergunta sem peso na régua.

## 3a. Quando não há fit — R-18

Se em qualquer ponto das perguntas de diagnóstico ficar claro que o lead não
serve (concorrente ligando para pesquisar preço, já é cliente, sem budget
nenhum e sem sinal de que muda, decisor ausente e sem acesso a ele), **não
force a ponte da seção 4**. Encerre a ligação com cortesia, sem prometer
retorno, e classifique `Resultado da tentativa` = `Desqualificado` +
`Motivo da desqualificação` (`campos-e-tags.md`, C-02/C-16 — mesmas opções
que o closer usa depois de uma reunião, aqui preenchidas por você antes dela
existir). O Pós-ligação fecha a oportunidade sozinho, sem abrir tarefa de
agendamento nem ocupar horário do closer.

Timing errado ("agora não, mas talvez em alguns meses") **não** é
`Desqualificado` — continue e classifique como `Pediu retorno` se o lead
topar conversar de novo depois, ou registre `Motivo da desqualificação` =
`Timing errado` só se ele mesmo encerrar o assunto (o Pós-ligação recicla
esse motivo para nutrição em vez de descarte, seção 4 do `build-wesales.md`).

## 4. Ponte para o agendamento

Só chegue aqui depois da pergunta 10, com o lead ainda qualificado (seção
3a não se aplicou). Pular a ponte antes do BANT completo tira pontos da
nota sem o SDR perceber.

> Baseado no que você me contou, faz sentido eu te apresentar como a gente
> resolve isso. Vou reservar uns 30 minutos com nosso especialista pra te
> mostrar certinho, sem compromisso. Você prefere [dia] de manhã ou de
> tarde?

Ao combinar o horário, abra o link do formulário de qualificação anexado ao
calendário do closer (`build-wesales.md`, seção 7.2) e agende na mesma tela
— o formulário já carrega as respostas das seções 2 e 3 se o SDR preencheu
durante a ligação; `Qualificação` sai com o valor padrão `SDR`. O envio
dispara o Pós-agendamento (`build-wesales.md`, seção 5), que
calcula `Nota de qualificação` a partir do que acabou de ser preenchido.

## 5. As 8 objeções mais comuns

| # | O lead diz | Causa real | Resposta do SDR |
|---|---|---|---|
| 1 | "Não tenho tempo agora" / "me liga depois" | Pegou de surpresa, não é recusa definitiva | "Sem problema, prometo que são só 2 minutos mesmo. Se não rolar, me diz um horário melhor que eu ligo de novo." Se insistir: registre `Pediu retorno` com o horário combinado (`build-wesales.md`, seção 4, ramo `Pediu retorno`) |
| 2 | "Já tenho agência" / "já tentei antes e não deu certo" | Má experiência anterior, ceticismo | "Entendo, é super comum — a maioria de quem eu falo já passou por agência que não entregou. Posso te perguntar o que especificamente não funcionou?" (grava em `Experiência com agência`, pergunta 5a) e usa a resposta como gancho do resto da conversa |
| 3 | "Não tenho orçamento pra isso agora" | Pressupõe investimento alto sem saber o valor real | "Faz sentido, mas vale entender o que dá pra fazer — muita gente que eu falo pensa que precisa de um investimento grande e descobre que não. Sem compromisso, só pra você ter a informação." |
| 4 | "Manda por WhatsApp/e-mail que eu vejo" | Deflection padrão pra desligar rápido | "Consigo mandar sim, mas é bem mais rápido eu te explicar agora do que você ficar lendo texto — são só mais 2 minutos e você já sai sabendo se faz sentido ou não." |
| 5 | "Preciso falar com meu sócio/decisor antes" | `Decisor` = `Influencia` ou `Não decide` | "Faz todo sentido. Podemos já marcar com ele/ela junto, assim eu explico pros dois ao mesmo tempo e vocês decidem sem eu repetir a conversa duas vezes?" |
| 6 | "Hoje já tenho cliente suficiente por indicação" | Acha que não precisa de canal pago, mas não mediu se estagnou | "Que ótimo, indicação é o canal mais barato que existe. A questão é: esse número tá crescendo mês a mês ou estagnado?" — volta para a pergunta 1 se ainda não respondida |
| 7 | "Quanto custa?" | Pede preço antes do diagnóstico | "Isso depende do que a gente desenhar pra sua realidade — é exatamente esse o motivo da reunião com o especialista, ele te mostra o investimento certo pro seu caso, sem chute." Nunca cite valor na ligação |
| 8 | "Não conheço vocês" / "como conseguiu meu contato" | Desconfiança do frio (cold call) | "Boa pergunta. A gente trabalha com empresas de {{contact.segmento}} e seu contato veio da nossa lista de prospecção do setor — te ligo porque vi que faz sentido pro que vocês fazem, não é ligação aleatória." |

Se a objeção 1 (ou qualquer outra) persistir depois de uma segunda tentativa
de resposta na mesma ligação, encerre educadamente e classifique
`Resultado da tentativa` conforme o desfecho real (`Não atendeu` só se a
ligação não emendou conversa nenhuma; `Pediu retorno` se topou falar depois;
`Não ligar` se pediu explicitamente para não ser mais contatado — aciona o
DND, `build-wesales.md`, seção 4, ramo `Não ligar`). Insistir além disso não
está no roteiro.

## 6. Regra de ouro

A mesma regra que já vale para a IA no WhatsApp (`build-wesales.md`, seção
6, prompt do bot) vale para o SDR humano — os dois canais precisam soar como
a mesma empresa, não como dois discursos diferentes:

**Nunca prometa preço, desconto, prazo de resultado ou garantia. Nunca
invente caso de cliente.** Se o lead insistir em número, a resposta é
sempre a da objeção 7.

Antes deste documento essa regra só existia escrita para o bot; o SDR humano
não tinha nada equivalente registrado, e é justamente a ligação — não a
mensagem automática — onde alguém sob pressão do "quanto custa?" é mais
tentado a improvisar um número.

## Como isso responde o "Pronto quando" do R-06

"Um SDR novo liga no segundo dia": este documento cobre abertura, caixa
postal, as 10 perguntas na ordem que a régua soma pontos, a ponte e as 8
objeções mais prováveis — nada aqui exige memorização, é ler e seguir a
ordem. Um SDR novo lê este documento e escuta 2-3 ligações reais no dia 1;
no dia 2 já tem roteiro completo para tocar a fila sozinho, inclusive para o
que sai do previsto (as objeções).

**Limite conhecido:** a ordem fixa das perguntas assume que a conversa flui
sem interrupção. Na prática o lead às vezes responde a pergunta 7 (dor
principal) espontaneamente lá na pergunta 2 — está certo o SDR aproveitar e
pular a pergunta correspondente, o roteiro é guia de conteúdo, não texto
decorado palavra por palavra (a única exceção é a seção 6, regra de ouro,
que não admite paráfrase que abra brecha para prometer preço ou garantia).
