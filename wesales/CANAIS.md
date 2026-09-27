# CANAIS.md — ligação e mensagem: o que a conta tem, o que a plataforma permite

Medido na subconta `1D53YTI9C7oIMBavcQxV` em 27/09/2026, pela API oficial, e
cruzado com as regras atuais da plataforma. Escrito porque a operação abre na
terça e o desenho da cadência depende de qual canal pode fazer o quê — e a
resposta não é a que o pedido supõe.

## 1. O que está ligado na conta (medido, não suposto)

`locations_get-location` devolve:

| sinal | valor | o que significa |
|---|---|---|
| `phoneCallEnabled` | `true` | ligação pelo sistema está liberada |
| `settings.saasSettings.twilioRebilling` | `enabled`, markup 20% | LC Phone (Twilio white-label) em uso, com rebilling |
| `conversationsEnabled` | `true` | caixa única de conversa ativa |
| `botServiceEnabled` | **`false`** | **Conversation AI desligada** |
| `facebookMessengerEnabled` | `true` | Messenger ligado |
| `locale` / `timezone` | `pt_BR` / `America/Sao_Paulo` | confere com o que o `build-wesales.md` manda conferir |
| `contactUniqueIdentifiers` | `[email, phone]` | dedupe por e-mail **e** telefone |

**Ligação pelo número funciona, e já rodou:** a conversa do contato
`AhFGDtHPwrrcPyPVJc0H` carrega `lastCallStatus: "completed"` com
`lastCallTimestamp`. Não é teoria — já houve ligação completada pelo sistema.

**`botServiceEnabled: false` é um defeito aberto:** a seção 6 do
`build-wesales.md` ("Qualificação por IA no WhatsApp") depende da Conversation
AI. Com ela desligada, aquele workflow não tem como qualificar. Conferir antes
de contar com ele na abertura.

## 2. O WhatsApp desta conta NÃO é a API oficial do Meta

Três evidências independentes, todas na mesma leitura de `conversations`:

1. **`lastMessageType: TYPE_CUSTOM_SMS`** nas conversas de WhatsApp. A
   integração oficial entrega mensagem como tipo WhatsApp; `TYPE_CUSTOM_SMS` é
   *Custom Conversation Provider* — um provedor de terceiros plugado no lugar do
   SMS.
2. **`createdBy.sourceId: 682cd9287059b4173d8b17bd-mawx7is9`** nos contatos que
   entram por esse canal — app de marketplace, não a integração nativa.
3. **IDs de grupo entrando como contato.** Dois "leads" têm `phone`
   `+120363226349138496` e `+120363294985523330`. E.164 tem no máximo 15
   dígitos; esses têm 18, e `120363…` é o prefixo de JID de **grupo** do
   WhatsApp. O conteúdo confirma: um é broadcast de "Data Analyst Roadmap", o
   outro um post de hóquei do San Lorenzo em espanhol. Só uma ponte não oficial
   (QR/ multi-device) enxerga grupo; a API oficial não entrega grupo.

**Consequência dura:** a **WhatsApp Business Calling API exige a Cloud API
oficial**. Numa ponte não oficial ela não existe. Então "ligar por WhatsApp
direto do sistema" **não** está disponível nesta conta como ela está hoje —
ligação por WhatsApp segue sendo o SDR abrindo o app no celular, que é o que a
cadência sempre assumiu ao mandar tarefa em vez de discar.

## 3. Se um dia migrar para a Cloud API oficial, estas são as regras

Não são regras do GHL, são do Meta, e mudam o desenho da régua:

| regra | valor |
|---|---|
| janela para ligar depois do aceite | **72 horas** |
| pedido de permissão | **1 por 24h**, máximo **2 em 7 dias** |
| pedido sem resposta | expira em **7 dias** |
| permissão temporária | vale **7 dias** |
| permissão permanente | não expira |
| teto de ligações conectadas | **100 por 24h** |
| indisponível em | EUA, Canadá, Egito, Vietnã, Nigéria (Brasil não está na lista) |

Ou seja: **não se liga por WhatsApp sem pedido de permissão aceito antes.** Uma
régua de 12 tentativas em 30 dias cabe no máximo ~8 pedidos de permissão, e
cada aceite abre só 72h. WhatsApp call é escalada, nunca o canal padrão.

## 4. O campo que já existe para isso, e está vazio

`Permissão WhatsApp` (`kdKnJecyZtssILfPPigl`, `SINGLE_OPTIONS`:
`Sim` / `Não` / `Não solicitado`) é exatamente o portão que a regra acima pede —
e o nó de entrada da cadência já escreve `Não solicitado` nele (medido no teste
de ponta a ponta de 27/09). Hoje **os 38 leads de `CONECTAR` estão todos em
`Não solicitado`**, isto é: nenhum pode receber ligação de WhatsApp, nem hoje
nem depois de migrar, até que alguém peça e o lead aceite.

`Canal que conectou` (`TxJmoWdkA8rTqC1uEsMW`: `Ligação WhatsApp` /
`Ligação normal` / `Mensagem`) também já está pronto para medir qual canal
converte.

## 5. O desenho que decorre disso

| tentativa | canal | automático? |
|---|---|---|
| discagem padrão | **número LC Phone comprado** | pode ser tarefa com discador no sistema; não precisa de permissão nenhuma |
| mensagem | WhatsApp pelo provedor atual | automática, é o que a cadência já faz |
| ligação por WhatsApp | só depois de `Permissão WhatsApp = Sim` | **hoje indisponível** (ponte não oficial) |

Regra de ouro para a abertura: **o número comprado é o canal de ligação; o
WhatsApp é o canal de mensagem.** Misturar os dois na mesma tentativa é o que
produz tarefa mandando o SDR fazer algo que o sistema não consegue.

## 6. Higiene que este documento obriga

**Grupo de WhatsApp não é lead.** Os dois JIDs da seção 2 estavam em
`NOVO LEAD` com `cad-inbound` — a corrida do G-03 na terça os promoveria para
`CONECTAR` e a cadência mandaria mensagem de venda **dentro de grupos**, com o
número da operação. Tratados em 27/09/2026 pelo mesmo caminho do A9 (nada
excluído): `dnd` ligado, tags `nao-perturbe` + `grupo-whatsapp-nao-e-lead`,
oportunidade em `abandoned`.

**Isso vai repetir.** Enquanto a ponte não oficial estiver no ar, todo grupo que
receber mensagem pode virar contato, ganhar oportunidade pela Porta de Entrada e
entrar na régua. O portão de higiene de telefone da cadência (nó 0.0, seção 2.3)
não pega isso, porque 18 dígitos passam por "tem telefone". **Conserto certo:**
portão na entrada que rejeite `phone` com mais de 15 dígitos ou começando em
`120363`, aplicando `grupo-whatsapp-nao-e-lead` e `abandoned` sozinho.

**Sem dono.** O teste de ponta a ponta mostrou a oportunidade nascendo com
`assignedTo: null`, enquanto os 38 leads reais têm dono posto na mão. Toda
`Internal Notification → Contact Owner` da máquina — inclusive a do opt-out por
palavra-chave (§2.9.5) — não tem para quem ir num lead novo. A distribuição
(R-10, nó 0.7/0.7b) precisa estar no ar antes de a entrada valer.

## Fontes das regras da seção 3

- <https://respond.io/help/whatsapp/whatsapp-business-calling-api>
- <https://www.infobip.com/docs/whatsapp/whatsapp-business-calling/business-initiated-calling>
- <https://developer.8x8.com/connect/docs/voice/whatsapp-business-calling/business-initiated/>
- <https://support.wati.io/en/articles/12546668-understanding-whatsapp-calling-restrictions-and-guidelines>
- <https://developers.facebook.com/documentation/business-messaging/whatsapp/calling>
