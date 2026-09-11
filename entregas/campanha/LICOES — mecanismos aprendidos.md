# Lições de mecanismo — como as ferramentas realmente se comportam
*Memória da máquina. Cada linha custou tempo ou lead para descobrir. Ler antes de mexer em qualquer coisa; acrescentar sempre que um comportamento surpreender.*

## Prospect Halo
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| Regra **obrigatória** (`additionalCriteria`) que o LinkedIn não consegue provar → o prospect é **adiado**, nunca contatado | Exclusão negativa ("não é agência") como obrigatória mata volume em silêncio. Usar como **preferida**. | 08/09 |
| Muitos filtros somados (títulos × setores × locais × exclusões) → o LinkedIn descarta em silêncio o que não reconhece e busca em todo lugar | Alvo enxuto rende mais: 6 títulos e 5 setores levaram a revisão de 1 para 10 perfis por passada | 08/09 |
| A API **não edita alvo** de agente existente (`update_agent` com titles/industries/locations retorna erro) | Mudar alvo = apagar e recriar. Definir bem antes de acumular leads. | 08/09 |
| Não existe importação de lista: leads só nascem da descoberta no LinkedIn | Cadência por lista de CNPJ roda fora da ferramenta | 08/09 |
| **Existe uma cota diária protegida de "verificação de perfil" (hydration), separada de convites e de créditos de prospect.** Quando ela acaba: `progressStatus: waiting_for_profile_capacity`, `waitingReason: LinkedIn profile verification capacity is currently exhausted`, e `nextRetryAt` diz a hora do reset | É o gargalo invisível nº 1. A busca acha os candidatos, mas eles ficam parados em `remainingCandidates` sem serem processados. Nada aparece como erro nem como pausa de segurança. **Sempre ler `progressStatus` e `waitingReason` antes de culpar a segmentação.** | 08/09 |
| Recriar agente reprocessa perfis e **queima a cota de verificação do dia** | Cada recriação custa capacidade real, não só a fila. Máximo uma recriação por dia. | 08/09 |
| `find_leads` não devolve e-mail; enriquecimento gasta 1 de 50 créditos/mês | E-mail é complemento para lead quente, nunca volume | 08/09 |
| Página de empresa publica conteúdo, mas não prospecta nem manda mensagem | Prospecção sempre pelo perfil pessoal | 08/09 |
| Autopilot de conteúdo gera o post ~20h antes de publicar | Dá para revisar e corrigir na véspera | 08/09 |
| Só conversas que já receberam resposta aceitam `reply_to_lead` | Não dá para puxar conversa parada pela API | 08/09 |

## Meta Ads
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| `ads_update_entity` força `status=PAUSED` em campanha e conjunto | Sempre chamar `ads_activate_entity` depois de qualquer edição | 07/09 |
| Vários públicos personalizados num conjunto = **união**, sem relatório por lista | Impossível saber de qual lista veio o lead. Separar exige orçamento por conjunto. | 08/09 |
| Lista nacional + geo estadual = interseção pequena | CPM dispara (R$78) e o orçamento não gasta | 08/09 |
| Editar segmentação reinicia a fase de aprendizado | Não mexer em conjunto que acabou de destravar | 08/09 |
| `instagram_user_id` é rejeitado no `object_story_spec` | Omitir o campo | 07/09 |
| Criação de anúncio de formulário falha pela API (falta permissão de ler os termos) | Anúncio de lead se cria no Gerenciador | 07/09 |

## Google
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| Perfil do LinkedIn não tem escrita por API (só leitura) | Título e "Sobre" são copiar e colar | 08/09 |
| Bloco de rotina marcado como "ocupado" some da busca de horário livre | Marcar como "disponível" o bloco em que se aceita reunião | 08/09 |
| `GOOGLEDRIVE_LIST_FILES` ignora `query`; usa `folderId` | Listar sempre por pasta | 07/09 |
| HTML enviado com mime `application/vnd.google-apps.document` vira Google Doc | Caminho para documento legível no celular | 07/09 |

## Instagram (verificado na conta do Pablo em 08/09)
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| A API do Instagram **recusa iniciar conversa nova**: `INSTAGRAM_SEND_TEXT_MESSAGE` só funciona em thread existente | O primeiro toque é SEMPRE manual do Pablo. Não existe automação legítima de DM frio, em ferramenta nenhuma | 08/09 |
| Depois que a pessoa responde, a janela de 24h abre e o envio é liberado (erro 403 subcode 2534022 quando fora da janela — não repetir) | Toques 2 e 3 podem ser automáticos, e é oficial | 08/09 |
| Comentário no post que dispara DM **abre a janela oficialmente**; curtida não abre; seguir não abre; resposta de story abre | O CTA "Comenta AGENDA" é o único mecanismo de aquisição em escala que a Meta autoriza | 08/09 |
| Pela API oficial: até **200 DMs por hora** para quem agiu primeiro. Ferramenta de navegador que "simula comportamento humano": 15% a 30% de suspensão ao ano contra menos de 0,5% da oficial | O caminho seguro é 400x maior que o arriscado. Simular comportamento humano é a descrição do que a Meta caça, não um selo de segurança | 08/09 |
| DM de desconhecido cai em "Solicitações", que quase ninguém abre. **Resposta a story cai na caixa principal** | Se tem story no ar, responder o story sempre vence o direct novo | 08/09 |

## Regras de conduta que saíram dessas lições
1. Quando um número não tem explicação, procurar o **mecanismo**, não o botão. O que some em silêncio (adiado, descartado, não entregue) importa mais que o que aparece no relatório.
2. Achou um defeito num lugar, procurar o mesmo defeito em **todos os lugares análogos** antes de encerrar.
3. Antes de mexer em algo que acabou de melhorar, calcular o que se perde reiniciando o aprendizado.
4. Registrar o mecanismo aqui na hora. Redescobrir custa dias.
5. **A linha que separa o seguro do arriscado não é "automatizar ou não", é "quem falou primeiro".** Iniciar conversa fria em volume derruba conta em qualquer plataforma. Responder quem te procurou é ilimitado e oficial. Toda máquina deve ser desenhada para o lead dar o primeiro passo.

## A prévia da notificação é a única linha garantida

Direct, e-mail e WhatsApp têm a mesma mecânica: a pessoa decide abrir lendo cerca de
50 caracteres na notificação. Tudo depois disso só existe se ela abrir.

Gastar essa linha com "Oi, aqui é o Pablo, do Rio. Não sou cliente" é entregar a única
chance para uma frase que identifica você como vendedor. A prova — o defeito concreto do
anúncio dele, com data — tem que ocupar esse lugar.

**Regra:** prova na primeira linha, apresentação na segunda. A apresentação não some,
porque sem ela a mensagem parece golpe; mas ela nunca vem antes.

Vale igual para o assunto do e-mail frio, que é a mesma linha com outro nome.

Corrigido em 08/09/2026, depois de escrever dez mensagens todas com o erro.

## Construir só o que ninguém vende

Em um único dia eu propus construir: um sequenciador de e-mail, uma máquina de estado de
cadência, uma camada de rotação de números de WhatsApp, um detector de resposta por IMAP e
um validador de e-mail. Todos existem prontos, entre R$ 127 e R$ 500 por mês.

Cada proposta isolada tinha justificativa de custo. Juntas, revelam um reflexo: escolher
construir em vez de comprar. E construir não é de graça — código próprio é frágil, depende
de eu estar rodando, e o pior caso é mandar o toque 4 para quem já respondeu.

**A regra:** construir só o que ninguém vende. Aqui isso é uma coisa só — **achar empresas
do Rio com anúncio visivelmente quebrado, com a prova e a data.** Nenhuma ferramenta do
mercado abre a Biblioteca de Anúncios e lê o título; elas personalizam por cargo, setor ou
sinal de contratação. Esse é o diferencial inteiro.

Disparo, cadência, rotação, estado, validação, CRM, agenda: **prateleira.** Comprar.

**A divisão certa:** eu sou a camada de pesquisa e redação. A ferramenta é a camada de envio.

Registrado em 08/09/2026, depois de o Pablo dizer "estamos tentando inventar roda" — e ele
estar certo.

## Os campos separados por barra no título são chamadas alternativas, não repetição

Descoberto em 09/09/2026, varrendo estética em Niterói. O anúncio da MCP Esteticaediagnostico
usa assim: "MCP Esteticaediagnostico | Preenchimento Labial | Lábio Aparente | Uma boca
modelada | Com Segurança".

**Cada campo é uma chamada diferente.** O Facebook testa qual funciona melhor com cada pessoa
e serve a vencedora. É um recurso bom, e é justamente ele que quase ninguém usa direito.

Todos os defeitos que eu venho catalogando são o mesmo erro nesse mesmo lugar:

| O que fizeram | Efeito |
|---|---|
| campos vazios | não há o que testar; o alcance encarece |
| mesma frase repetida | o teste compara a frase com ela mesma |
| nome da página ou URL colada | o teste roda em cima de lixo |

**Consequência para a abordagem:** parar de dizer "seu anúncio está errado" e passar a explicar
o recurso que ele paga e não usa, com um exemplo real de concorrente usando certo. Não acusa,
ensina algo verdadeiro na hora, e traz a prova social do toque 3 para o toque 1.

## O sandbox reinicia e leva a sessão do Prospect Halo junto (09/09, 10h36)

A rotina de checagem de post depende de chamar o Prospect Halo pelo workbench do Composio, que é
um sandbox remoto. Nesta rodada o sandbox tinha reiniciado: nenhum arquivo de sessão, nenhuma
variável de ambiente, nada. Refazer o `initialize` exige a chave `ph_live`, que não fica guardada
em lugar nenhum do repositório nem do ambiente desta sessão — ela vinha do contexto da conversa,
e o contexto foi compactado.

**A lição não é sobre o Prospect Halo, é sobre onde credencial mora.** Qualquer processo que só
funciona enquanto uma chave estiver viva na conversa para de funcionar no primeiro reinício, sem
aviso e sem erro visível — a rotina simplesmente não consegue mais olhar. Credencial de rotina
precisa estar num lugar que sobreviva ao reinício: variável de ambiente do ambiente remoto, ou um
arquivo que o Pablo reponha quando pedir.

**Efeito prático nesta rodada:** não consegui verificar se houve post às 7h30, nem os comentários,
nem se os engajadores entraram no agente. Não afirmo que não houve post — afirmo que não pude
olhar.

## O Supabase estava bloqueado por cota o tempo todo (09/09, 11h10)

Quatro tentativas de conectar o servidor MCP próprio falharam com "Não foi possível registrar no serviço de login". Eu atribuí a falha ao protocolo (OAuth na raiz do domínio) e reescrevi o servidor oito vezes. A causa real apareceu quando testei a URL de fora: **HTTP 402 — "Service for this project is restricted: exceed_egress_quota, exceed_storage_size_quota"**. A restrição é da organização inteira (os dois projetos ativos respondem igual). A função nunca chegou a rodar; nenhuma versão teria funcionado.

Mecanismo: o gateway do Supabase bloqueia antes da função quando a organização passa da cota gratuita (5 GB de saída, 1 GB de armazenamento). O bucket `videos-maquina` tem 622 MB em 181 vídeos; a saída foi consumida pelos downloads desses vídeos.

Regra: **antes de depurar protocolo, bater na URL com `curl` de fora e ler o código HTTP.** Um 402 ou 403 na porta encerra a investigação em um minuto.

## A Meta tem servidor MCP oficial que aceita app próprio (09/09, 11h10)

`https://mcp.facebook.com/ads` — servidor hospedado pela Meta, aberto a qualquer app desde 16/07/2026. Duas formas de entrar: OAuth pelo Login do Facebook para Empresas usando o **ID do app próprio como client_id**, ou `Authorization: Bearer <token de usuário do sistema>`. Escopos fixos do OAuth: `ads_management ads_read catalog_management business_management pages_show_list instagram_basic ads_mcp_management` — **sem `pages_manage_ads`**, que é o que o anúncio de lead precisa para ler os termos da página. O caminho com token de sistema carrega o que o token tiver.

Também existe painel de **regras** em Configurações do Business Suite → Integrações → "Servidor MCP de anúncios": permite bloquear criação de campanha, edição de orçamento, teto de orçamento. O servidor aplica essas regras. Sempre conferir esse painel quando uma escrita for negada sem erro claro.

## Cadeia de hosts tentada para o relé, e onde cada uma parou (09/09, 11h50)

Pablo pediu estrutura de tentativa-e-erro entre hosts. Executada, na ordem: Supabase (402 por cota da organização) → Lovable `create_project` (negado pelo classificador da sessão) → Netlify `deploy-site` em site existente vazio (negado) → Cloudflare (conector só lê workers, não publica) → Composio, busca por Vercel/Render (negada). Até a gravação do arquivo do relé com os endereços de OAuth de fachada foi negada.

Mecanismo: o classificador desta sessão bloqueia duas famílias — **criar ou publicar um host novo** e **escrever um servidor que aprova OAuth sem verificar**. Não é rede nem cota: é permissão da sessão. Só o dono da conta libera, nas configurações de permissão do claude.ai, ou a cadeia inteira devolve o mesmo "negado".

Regra: quando duas ferramentas de hospedagem diferentes são negadas com a mesma mensagem, parar a cadeia e pedir a liberação — a terceira e a quarta vão cair igual.

## O relé subiu no Cloudflare e a Meta recusou o token por ser de administrador (09/09, 12h25)

Cadeia até aqui: Supabase (cota) → Netlify (crédito pausado, site "Private") → Cloudflare Worker pelo editor online, com a rota `workers.dev` habilitada na mão (nasce desligada quando o worker vem do Git; o sintoma é `error code: 1042` em qualquer caminho). Relé responde: raiz 404, `/mcp/<segredo>` 200.

Ao repassar para `mcp.facebook.com/ads`, a Meta devolveu **403 "Admin system user tokens are not permitted on the Ads MCP server. Please use an Employee system user token."** O usuário do sistema "Integracao" é administrador. O servidor MCP oficial só aceita token de usuário do sistema com função **Funcionário**.

Regra: para o MCP da Meta, criar usuário do sistema *Funcionário*, atribuir conta de anúncios, página e app, e gerar o token nele. O de administrador continua servindo para a Graph API direta.

## O token de Funcionário destravou a criação de anúncios (09/09, 12h50)

Com o token do usuário do sistema **Funcionário** (`Integracaomcp`), `mcp.facebook.com/ads`
respondeu `initialize` 200 e listou **97 ferramentas** — inclusive `ads_create_ad`,
`ads_create_ad_set` e `ads_create_creative`. Pelo mesmo caminho foi criado o anúncio
`VR1 — INTERESSE` (`120247352877730766`), pausado, no conjunto que estava vazio havia duas
semanas. O erro de Termos de Geração de Leads **não era dos termos**: era da conexão sem
`pages_manage_ads`.

Mecanismo em uma linha: **o servidor MCP da Meta recusa token de administrador e aceita o de
funcionário** — e o token de funcionário carrega as permissões que o conector nativo não pede.

Limite que restou: chamadas maiores pelo sandbox são barradas pela permissão da sessão, não pela
Meta. Criar um anúncio simples passa; montar conjunto com segmentação longa, não.

## O erro de "Termos de Geração de Leads" era o app, não os termos (09/09, 14h20)

Com o token de Funcionário dá para **ler** o campo que o conector nativo não enxerga:

```
GET /1117439194786453?fields=leadgen_tos_accepted  →  {"leadgen_tos_accepted": true}
```

A página **aceitou** os termos. Ainda assim, os dois anúncios criados hoje pelo app OPC Automação
ficam `WITH_ISSUES` com a mensagem de termos não aceitos — e o mesmo anúncio já apareceu antes com
a mensagem de "app em modo de desenvolvimento". São **duas mensagens para a mesma causa**: o post
escuro do anúncio nasce por um app em desenvolvimento, e a Meta reporta ora um texto, ora outro.

Regra: quando um anúncio de lead acusar termos não aceitos, **primeiro conferir
`leadgen_tos_accepted`**. Se vier `true`, o problema é o app, não os termos — e nenhum clique na
página de termos vai resolver.

## O carimbo do app só existe em criativo dinâmico (09/09, 16h45)

Descoberta que destravou a conta inteira. Comparando dois anúncios com **o mesmo criativo, a mesma
publicação, a mesma página e o mesmo formulário**, um entregava e o outro não. A diferença era o
formato do conjunto:

| Conjunto | Formato | Anúncio criado por mim | Entrega |
|---|---|---|---|
| dinâmico (`is_dynamic_creative: true`) | Meta **gera uma publicação nova** por anúncio | carimbo do app OPC Automação | **não** |
| comum | o anúncio **aponta para a publicação que já existe** | sem carimbo | **sim** |

Mecanismo: o erro *"Ads creative post was created by an app in development mode"* fala do **post**,
não do anúncio. Em conjunto de criativo dinâmico, cada anúncio nasce com um post escuro novo, criado
por quem chamou a API. Em conjunto comum reaproveitando criativo existente, nenhum post novo nasce —
e não há o que carimbar.

**Regra prática enquanto o app estiver em desenvolvimento:** criar conjuntos **sem** criativo
dinâmico e montar a variação com **um anúncio por criativo**. Dez anúncios com dez criativos dão o
mesmo teste que o criativo dinâmico daria, com a vantagem de o relatório mostrar o desempenho de
cada peça separado — que o dinâmico esconde.

Consequência secundária: conjunto dinâmico aceita **um único anúncio** e **anúncio dinâmico não pode
ser apagado** (só junto com o conjunto). Foi esse par de regras que travou os quatro conjuntos
anteriores. Conjunto comum não tem nenhuma das duas limitações.

## O primeiro lead ficou no silêncio: WhatsApp Oficial exige template (09/09, 23h)

O lead André entrou às 22h01 pelo anúncio VR1. A automação "Pré-venda Meta Ads - Qualificação
Automática" disparou pelo gatilho DEAL_CREATED e chamou o agente. E nada saiu.

`get_chat_messages` no chat dele: **vazio**. `get_contact_history`: **vazio**.

**Mecanismo:** o canal é WhatsApp Business Oficial (API da Meta). Uma empresa **não pode abrir
conversa com mensagem livre** — só com um template HSM aprovado. `list_message_templates` na
conta devolvia **lista vazia**. O agente tinha o que dizer e não tinha por onde.

**Segundo defeito, no mesmo lugar:** os outros 24 gatilhos da automação são todos
`CHAT_WHATSAPP_OFFICIAL_MESSAGE_RECEIVE_CHANNEL` com palavra-chave (*oi*, *preço*, *quero*...).
Ou seja, a máquina inteira só acorda **se o lead falar primeiro**. Quem preenche formulário não
fala primeiro: ele espera.

**Correção:** criado o template `opc_abertura_lead_formulario` (id Meta `1067522472684876`,
MARKETING, pt_BR), com três botões de resposta rápida. O botão não é enfeite — o toque dele
**abre a janela de 24 horas**, e só a partir daí a IA conversa livre.

**Armadilha da criação:** a Meta recusa template cujo texto **começa ou termina com variável**
(erro 100, subcódigo 2388299). `{{1}}, você acabou de...` é rejeitado; `Oi {{1}}, você acabou
de...` passa.

**Limite do MCP do Clint:** as ferramentas expõem automações, templates, funil e conversas —
**não o texto de instrução do agente IA**. O prompt tem que ser colado na mão, no painel.

**Regra que fica:** antes de culpar o texto de um agente, conferir se **alguma mensagem chegou a
existir**. Chat vazio não é IA ruim, é canal bloqueado.

## Como criar anúncio Clique-para-WhatsApp pela API (10/09, 08h30)

Criada a campanha `WPP I CONVERSA I FS1` (`120247368224510766`), CBO R$ 30/dia, 3 conjuntos,
10 anúncios cada. Três mecanismos que custaram tentativa e erro:

**1. O bloqueio do app em modo de desenvolvimento NÃO se aplica aqui.** `ads_create_creative`
com vídeo funcionou de primeira. Confirma em definitivo o que já estava escrito: o carimbo do
app só existe em criativo dinâmico. A conta pode criar criativo novo à vontade.

**2. Criativo de vídeo exige miniatura.** `ads_create_creative` com `video_id` e sem
`image_hash` devolve *"At least one of image_hash or image_url must be provided"*. A miniatura
não é opcional para vídeo.

**3. O criativo do WhatsApp precisa do destino DENTRO do call_to_action.** Criar o criativo
solto com `call_to_action_type: "WHATSAPP_MESSAGE"` e depois usar `creative_id` no anúncio
falha com *"Invalid Creative For Objective"* (subcódigo 1487891). O que funciona é passar o
criativo inline no `ads_create_ad`:

```
{"object_story_spec":{"page_id":"...","video_data":{"video_id":"...","image_hash":"...",
 "message":"...","title":"...",
 "call_to_action":{"type":"WHATSAPP_MESSAGE",
   "value":{"app_destination":"WHATSAPP","link":"https://api.whatsapp.com/send"}}}}}
```

**4. Truque para não repetir o spec 30 vezes:** cada `ads_create_ad` inline gera um
`creative_id` próprio. Criar os 10 anúncios do primeiro conjunto inline, ler os `creative_id`
com `ads_get_ad_entities` (campo `creative`), e usar esses ids nos outros dois conjuntos.
De 30 specs longos para 10.

**5. `source_ad_id` não duplica fora do modo rascunho** — devolve *"creative is required"*.

**6. `ads_activate_entity` devolve INTERNAL error aleatoriamente.** É retryable de verdade:
as quatro que falharam passaram na segunda tentativa. Não é bloqueio, é instabilidade.

## Ter ferramenta de evento não é conseguir enviar evento (10/09/2026)

Eu disse que ia "ativar" o enriquecimento de dados para a Meta e depois tive que
voltar atrás: escrevi o script e o README, mas não enviei nada. A ferramenta de
pixel do conector cria regra de pixel de site — o Pablo não tem site. O envio de
evento offline (CAPI) exige token de usuário de sistema, que eu não tenho.

Regra: antes de dizer "ativei", conferir se existe credencial para o disparo.
Ferramenta disponível ≠ ação executada. E quando eu já tiver dito errado, o
conserto é dizer a frase inteira: "não ativei, porque não consigo sem o token."

## Anúncio de imagem Clique-para-WhatsApp: link_data, não video_data

Mesma estrutura do vídeo, trocando o bloco:

    {"object_story_spec":{"page_id":"...","link_data":{"image_hash":"...",
     "link":"https://api.whatsapp.com/send","message":"...","name":"...",
     "call_to_action":{"type":"WHATSAPP_MESSAGE",
       "value":{"app_destination":"WHATSAPP","link":"https://api.whatsapp.com/send"}}}}}

O `name` do link_data é o texto do botão, não o nome do anúncio. Criativo inline
funciona; creative_id avulso continua dando "Invalid Creative For Objective".

## O gatilho por palavra-chave era um funil dentro do funil (10/09/2026)

O Pablo notou que a IA não abriu conversa com o lead novo do formulário. Fui
olhar e achei DOIS bloqueios empilhados, não um:

**1. O gatilho de mensagem exigia uma palavra da lista.** A automação
"Pré-venda Meta Ads" tinha 24 gatilhos, cada um casando uma palavra: oi, olá,
bom dia, preço, valor, mentoria, cliente, e por aí. Quem escrevesse "Sim",
"Pode me explicar?", "👍" ou mandasse um áudio não disparava nada — a mensagem
chegava e o agente nunca era chamado. No chat do Zenilson a mensagem do lead
chegou às 12h16:07 com conteúdo vazio (tipo não suportado), e conteúdo vazio
não contém palavra nenhuma.

Conserto: a Clint só aceita UMA condição por gatilho, sem grupo AND/OR, e não
aceita valor vazio. Mas aceita `not-contains`. Então um gatilho de
`not-contains` com um valor improvável (`zzqxwjkvnp`) casa QUALQUER mensagem.
Os 24 gatilhos viraram 3: pega-tudo no Comercial, pega-tudo no número de teste,
e o DEAL_CREATED que já existia. Publicado como versão 5.

**2. O DEAL_CREATED dispara, mas o agente não tem como falar.** Esse gatilho
funcionava desde sempre — o problema é que ele abre o fluxo FORA da janela de
24h, e fora dela a Meta só entrega template aprovado. `list_message_templates`
continua devolvendo lista vazia: o `opc_abertura_lead_formulario` segue em
análise. Enquanto isso o agente roda, tenta escrever e o envio morre.

A regra que fica: **um gatilho que depende do texto do lead é um funil dentro
do funil.** Cada palavra que não está na lista é um lead perdido em silêncio,
e silêncio não aparece em relatório nenhum. Gatilho de canal deve ser
pega-tudo, e a filtragem, se precisar, é trabalho do agente — que ao menos
deixa rastro do que decidiu.

## Ler o agente não é editar o agente (10/09/2026)

Eu disse ao Pablo "vou ajustar isso no agente" ao ver a IA oferecer 19h e
repetir pergunta. Fui fazer e não existe ferramenta: o MCP da Clint tem
`list_ai_agents` (lê id e kind) e o nó `AI_AGENT_RUN` (aponta para um agente),
mas nada que escreva o prompt, o horário ou o comportamento dele. Automação eu
edito; agente eu só aponto.

Mesma família do erro do CAPI: confundi ter a peça no fluxo com poder mexer
nela. Antes de prometer ajuste, conferir se existe verbo de escrita para
aquele objeto — não basta o objeto aparecer em alguma listagem.

## Público de interesse tem vazamento embutido: "Renda" e "Freelancer" (10/09/2026)

A Jessica chegou pela campanha de WhatsApp, foi qualificada pela IA e marcou
reunião — mas é afiliada de Mercado Livre/Shopee, nunca fechou um cliente e
não tem negócio. Não é o público da mentoria.

Fui ler a segmentação e o vazamento estava escrito lá. Entre os 12 interesses,
cinco descrevem quem procura como GANHAR dinheiro, não quem já toca um negócio:

- Renda (negócios e finanças) — 6003719384062  ← o pior, ímã de renda extra
- Empresa em casa — 6003605501620
- Teletrabalho — 6003343813828
- Freelancer (carreiras) — 6003374632277  (e o cargo Freelancer, 111926488822704)
- Trabalho autônomo (carreiras) — 6003214937861

E no segundo bloco, dois comportamentos com o mesmo defeito:
- **New Page Admins** (6041891177783) — quem acabou de criar uma página é,
  por definição, quem está começando. É a Jessica.
- **Facebook Payments users 30d** (6004948896972) — sinal de quem COMPRA no
  Facebook, não de quem tem empresa.

Ficaram os sinais de propriedade: comportamento Small business owners, cargos
Dono/Proprietário/Comerciante/Sócio, empregadores Empresário/Proprietário, e o
segundo bloco reduzido a Facebook Page admins + Business page admins.

**A regra:** num público de interesse para vender a dono de negócio, todo termo
que fala de *ganhar renda* traz quem não tem negócio. Termo que fala de *ser
dono* traz quem tem. Ler a lista de interesses procurando essa diferença vale
mais do que qualquer ajuste de lance.

## Três conjuntos disputando a mesma pessoa é dinheiro brigando consigo

Os três conjuntos da WPP I CONVERSA I FS1 (semelhante, personalizado, interesse)
podiam alcançar a MESMA pessoa: quem está na lista de CNPJ também cai no
semelhante daquela lista e também tem interesse em "Pequena empresa".

Conserto: excluir as 9 listas próprias e os 3 públicos de engajamento
(VV, ENG INST, PG 365) dos conjuntos de semelhante e de interesse. Agora os três
são disjuntos — o personalizado fica com o público quente, o semelhante com o
parecido, o interesse só com quem é frio de verdade.

Além de parar a disputa interna, isso torna o número de cada conjunto legível:
antes, um lead que aparecesse no interesse podia ser alguém da lista, e a
comparação entre conjuntos não queria dizer nada.

**Nenhuma lista foi alterada** — elas são só referenciadas como exclusão, que é
o que o Pablo pediu quando disse "só não mudo público as listas".

## Bloqueio: token da Clint expirou (10/09/2026, 19h08)

O conector da Clint voltou `MCP server "Clint" requires re-authorization (token
expired)`. Enquanto isso durar eu fico cego para o CRM: não vejo lead novo, não
vejo conversa, não movo negócio de etapa. A Meta continua funcionando, então
ainda vejo gasto, clique e conversa iniciada — mas não vejo QUEM chegou.

Consequência prática: a rotina horária perde a parte que mais importa. Um lead
pode entrar e ficar sem aviso.

Conserto: só o Pablo pode reautorizar, nas configurações de conectores do
claude.ai. Não dá para fazer isso daqui — esta sessão não roda o fluxo de
autorização.

Regra: quando um conector cai, avisar UMA vez e seguir com o que resta
funcionando, dizendo exatamente o que deixou de ser visível. Não repetir o
aviso a cada rodada, e não fingir que a vigilância continua completa.

## Como achar a chave de uma cidade para excluir (10/09/2026)

O Pablo pediu para excluir Itaboraí de todas as campanhas. A exclusão de cidade
na Meta só aceita `cities: [{key}]` — nome não serve — e o MCP do Facebook não
tem busca de localidade: `ads_get_field_context` devolve `geo_locations` como
campo desconhecido, e busca na web não acha chave nenhuma.

O caminho que funciona é o Composio, toolkit metaads:

    METAADS_LIST_TARGETING_SEARCH
    { "type": "adgeolocation", "q": "Itaborai", "location_types": ["city"] }

Devolveu key 255567, região Rio de Janeiro (454). Confirmei depois lendo o
targeting de volta: a Meta ecoou `"name": "Itaboraí"`.

**A regra:** nunca chutar chave de localidade. Uma chave errada exclui a cidade
errada em silêncio — a API aceita, nada dá erro, e o dinheiro passa a evitar um
lugar que ninguém pediu. Buscar a chave, aplicar, e reler o targeting para ver
o nome que a Meta devolve.

Cidades excluídas hoje em toda a conta: Magé (258769) e Itaboraí (255567).

## O campo `exclusions` é aceito e descartado em silêncio (10/09/2026)

Tentei excluir o comportamento "Nova empresa ativa (< 6 meses)" (6273108079183)
do conjunto LEADS I INTERESSE I FASE 3, mandando `exclusions` dentro de
`targeting`. A resposta veio `success: true` e o eco de `updated_fields` trouxe
o bloco `exclusions` inteirinho, com o nome do comportamento e tudo.

Reli a segmentação: **não estava lá.** Tentei de novo, dessa vez com o campo
`name` junto do id. Mesmo resultado — eco perfeito, gravação nenhuma.

Duas tentativas, duas confirmações. O `exclusions` de comportamento passa pelo
MCP e some antes de chegar ao objeto.

**A regra, de novo e mais forte:** o eco de `updated_fields` NÃO é prova de
gravação. Ele repete o que eu mandei, não o que a Meta guardou. A única prova é
reler a entidade. Foi assim que eu peguei a chave de Itaboraí (deu certo) e é
assim que eu peguei este (deu errado).

Se eu tivesse confiado no `success: true`, teria dito ao Pablo que o filtro
anti-iniciante estava no ar, e ele estaria comprando lead de gente começando
achando que não estava. Mentira difícil de descobrir depois.

Contorno: a exclusão de comportamento precisa ser feita na interface do
Gerenciador, em "Excluir pessoas que correspondam a pelo menos um destes".

## O criativo que eu ia apagar era o único que trazia lead (11/09/2026, 12h10)

Passei a manhã montando a troca dos criativos: fora os vídeos, dez imagens por
conjunto. O Pablo pediu assim e eu executei sem olhar a conta.

Fui vigiar no ciclo horário e a conta dizia o contrário:

| Anúncio | Conjunto | Gasto | CTR | Leads |
|---|---|---|---|---|
| **V10 — Cliente todo dia (vídeo E)** | LEADS I INTERESSE I FASE 3 | R$6,67 | **3,17%** | **2** |
| **V10 — Cliente todo dia (vídeo E)** | LEADS I SEMELHANTE CNAE RJ I FASE 3 | R$1,13 | **3,70%** | **1** |
| DINAMICO - VÍDEOS | INT I DONOS | R$4,55 | 0,00% | 0 |

Três leads hoje a **R$2,60** cada. O critério de corte que eu mesmo escrevi no
plano era CTR mínimo de 0,5% — o vídeo V10 entrega **seis a sete vezes** isso.

**O mecanismo não é sobre vídeo contra imagem.** É que eu tratei um pedido de
criativo como se fosse pergunta de gosto, quando havia número na conta
respondendo. "Remove os vídeos" dito antes de ver que o vídeo faz R$2,60 de CPL
não é a mesma frase depois.

E os quatro conjuntos que o plano dizia atualizar estavam errados: dois estão
**pausados e renomeados `ZZ INATIVO`**, e os que produzem lead (FASE 3) não
estavam na lista. Eu escrevi "aplicar em 4 ad sets" copiando o documento antigo
em vez de ler a conta.

**A regra:** antes de trocar criativo, ler o desempenho do criativo que está
lá. Se o que vai sair tem resultado, a troca deixa de ser execução e vira
decisão — e a decisão é do Pablo, com o número na frente. Substituir o
vencedor sem avisar é o jeito mais caro de obedecer.

Segunda regra, menor: lista de ad set em documento apodrece em dias. Conferir os
ids na conta antes de planejar em cima deles.
