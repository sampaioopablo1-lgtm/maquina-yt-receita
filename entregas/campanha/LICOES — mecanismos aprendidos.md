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
