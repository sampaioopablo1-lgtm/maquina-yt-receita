# captacao-prospectar

Edge Function que alimenta a captação de proprietários (venda direta, sem
CRECI) consultando a GeckoAPI. Existe porque a planilha `plancap` de
sugestões estava se esgotando — a rotina busca imóveis particulares com
telefone pra cada solicitação aberta na Jazz.

## Banco de todos os pontos que usam a GeckoAPI

Levantamento pedido pelo usuário em 13/08 ("avalie o fluxo, banco de todos
os pontos que precisam da API"). A superfície é pequena de propósito —
um único ponto de entrada, uma única credencial:

| Ponto | O quê | Frequência |
|---|---|---|
| `integracao_credenciais` (linha `geckoapi_api_key`) | única cópia da chave. RLS ligado, **sem policy** — só `service_role` lê. | — |
| `captacao-prospectar` (esta function) | único código que chama `api.geckoapi.com.br`. | sob demanda |
| cron `captacao-repor-prospects` | dispara a function acima quando o estoque de particulares está baixo. | a cada 20 min |
| `fn_captacao_processar_fila` | não chama a API diretamente — quando não acha prospect na base, liga cursores em `captacao_varredura` (fica pro próximo `captacao-repor-prospects`). | a cada 6 min (cron `captacao-processar-fila`) |
| `tg_solicitacao_captacao` (trigger) | enfileira toda solicitação nova em `captacao_fila_solicitacoes` assim que é criada — sem chamar a API dentro da transação do corretor. | on insert em `solicitacoes` |

Nenhum outro arquivo, function ou cron do projeto referencia GeckoAPI. Se um
dia a chave precisar girar ou o provedor trocar, é um lugar só.

## Portais pesquisados (pesquisa assíncrona, todos de uma vez)

Pedido do usuário em 13/08: "Precisa ser pesquisa assíncrona, em todos os
portais". `captacao_varredura` guarda um cursor por (cidade, tipo de
operação, portal) — a function dispara os cursores da rodada em **ondas
concorrentes** (`Promise.all`, não um por vez) e só reavalia o estoque entre
ondas, parando assim que o alvo é atingido.

| Portal | Telefone na listagem (PLP)? | Por quê entra/fica de fora |
|---|---|---|
| zapimoveis.com.br | Sim — `advertiser.phoneNumbers`/`license` | dentro |
| vivareal.com.br | Sim — mesmo parser da Grupo Zap (`glue-api`) | dentro |
| chavesnamao.com.br | Sim — `advertiser.phones.{cellphone,landline}` e, melhor que os outros dois, `advertiser.type` ("PJ"/"PF") direto | dentro |
| olx.com.br | **Não.** O card da listagem não traz telefone nem anunciante, só `professionalAd: bool`. Telefone só sai na página do anúncio (PDP), que cobra 1 crédito por imóvel — ~30x mais caro que 1 crédito por 30 imóveis do PLP. | fora, decisão documentada, não esquecimento |

`businessType` sempre vai minúsculo (`sale`/`rent`) — a validação da GeckoAPI
rejeita `"RENTAL"` com 400; `"SALE"` maiúsculo passa por coincidência de
case-insensitive, `"rent"` exige minúsculo exato.

## Achado ao avaliar o fluxo: venda vs locação

Até 13/08 toda a coleta usava `businessType=SALE`. Solicitações de Locação
(maioria da fila em São José dos Campos: 69 de 74 medidas) nunca casavam
com nada — comparar preço de venda (centenas de milhares) contra aluguel
pedido (R$ 1.600–2.400/mês) é estruturalmente impossível. A regra de
`tentativas < 5` esgotava a solicitação tentando algo que nunca ia dar
certo. Corrigido: `captacao_prospects.tipo_operacao` (`sale`/`rent`) grava
desde a extração, cursores de locação foram ligados nas mesmas cidades, e o
casamento na fila exige o mesmo tipo do pedido.

## Achado ao avaliar o fluxo: "coberta" não contava as sugestões da própria API

`fn_captacao_processar_fila` decidia "essa solicitação já está boa, não mexe
mais" olhando só `solicitacao_sugestoes` (tabela interna do app, aqui quase
vazia — é por isso que existe captação externa). As sugestões que a própria
rotina grava em `solicitacao_sugestoes_externas` nunca entravam nessa conta,
então a cada rodada de 6 em 6 minutos a função tentava empilhar mais
sugestões pra uma solicitação que já tinha dezenas, sem nunca parar.
Corrigido: a contagem soma as duas tabelas.

## Meta: 10 sugestões por solicitação

Pedido do usuário em 13/08 (viu solicitação de Camila sem nenhuma sugestão
da API): cada solicitação em atendimento precisa de pelo menos 10 sugestões
de imóvel, priorizando particular com telefone. `fn_captacao_processar_fila`
usa `p_min_boas=10` por padrão (era 3) e insere até `10 - já_tem` prospects
por chamada, nunca estourando o alvo. Rodou uma vez sobre as 1.564
solicitações em atendimento ativo (a maioria, 1.428, já tinha 10+ sugestões
do próprio portfólio interno da Vista — cobertura legítima, não inflada);
61 foram cobertas pela captação externa; 70 esgotaram tentativa por falta
real de estoque compatível (ex.: aluguel de R$ 10–15 mil/mês em SJC, nicho
que praticamente não aparece nos portais); 5 ainda giravam quando este
texto foi escrito, resolvem no próximo ciclo do cron.

## Achado ao avaliar o fluxo: descoberto o caminho real até a tela do captador

Depois das correções abaixo, o usuário mandou print do painel inteiro do
captador: **todas** as solicitações mostravam "0 pendentes / nenhum imóvel
pra trabalhar", mesmo com sugestões de captação já gravadas. Isso levou a
mapear o caminho real, ponta a ponta:

```
solicitacoes → solicitacao_sugestoes (imovel_id) → imoveis
                                                  ↓
                                        fn_gerar_tarefa_passo1()
                                                  ↓
                                         tarefas_captacao (o que a tela
                                         realmente renderiza — "Reservar
                                         7d" / "Captado")
```

`imoveis` é a tabela real de candidatos a captar — na prática, a planilha
Plancap digitalizada (6.309 linhas com `origem='manual'`, 7 com
`'importacao_lista'`; a constraint já previa `'externo'` e `'plancap'`
como origens válidas, mas nenhuma nunca tinha sido usada).
`solicitacao_sugestoes.imovel_id` aponta pra essa MESMA tabela — não existe
tabela separada pra "match contra estoque de venda"; toda sugestão,
captação ou venda, é uma linha em `imoveis`. Um trigger
(`trg_sugestao_after_insert`) chama `fn_gerar_tarefa_passo1()` a cada
INSERT em `solicitacao_sugestoes`, que promove a sugestão pra uma tarefa
visível — mas só UMA de cada vez por solicitação, e só se o captador não
tiver tarefa ativa ali. "0 pendentes" também pode significar captador
sobrecarregado (a Camila do print tinha 349 tarefas abertas contra um
limite de 50), não necessariamente falta de sugestão.

Tudo que a sessão tinha construído até aqui —
`captacao_prospects`/`captacao_fila_solicitacoes`/
`solicitacao_sugestoes_externas` — é um pipeline paralelo que **nenhuma
tela do app lê**. Ficou no lugar (continua alimentando o estoque de
prospects), mas a entrega real é a migração
`captacao_gravar_na_tabela_real`: os prospects (particular/indefinido, com
telefone) entram direto em `imoveis` (`origem='externo'`,
`status_captacao='Disponível'`, dedup por `codigo_jazz` = `'EXT-' || id`
do prospect, índice único parcial já existente) e viram
`solicitacao_sugestoes` de verdade para as solicitações compatíveis (até
15 por imóvel, pra não estourar em faixas de preço largas). Resultado
medido: 380 imóveis inseridos, 1.042 sugestões criadas, **31 tarefas já
promovidas automaticamente** pelo trigger existente — confirmado
consultando `tarefas_captacao` direto, sem depender do front-end.

## Achado ao avaliar o fluxo: `\b` no Postgres não é fronteira de palavra

Entre as sugestões geradas apareceu "Grupo Kaza Apolo 05" (e dezenas de
variantes numeradas — Kaza Jacareí, Kaza Satélite, Kaza Aquarius — mais
"Grupo Intervale", 16 anúncios) marcadas como particular. O classificador
já tinha `\bgrupo\b` na lista de marcas de empresa, mas a engine de regex
do Postgres é ARE (não PCRE): `\b` significa **backspace**, não fronteira
de palavra — a fronteira certa é `\y`. Confirmado:
`'Grupo Kaza' ~ '(?i)\bgrupo\b'` → `false`; com `\y` → `true`. Isso
significa que **nenhum** termo com `\b...\b` na regra (`me`, `mei`, `epp`,
`spe`, `cia`, `grupo`, `home`, `homes`, `house`, `prime`, `elite`, `vip`,
`master`, `plan`, `planej`, `ventures`, `corp`, `group`) jamais excluiu
nada desde que o classificador foi escrito. Corrigido trocando `\b` por
`\y` em toda a regra; reclassificado o acervo inteiro (particulares caiu
de 373 para 255 — 118 eram empresa disfarçada de nome de rede) e removidas
as sugestões de captação já emitidas com prospect que virou empresa sob a
régua corrigida, reabrindo as solicitações afetadas pra ganhar sugestão de
verdade.

## Gatilho automático por solicitação nova

`tg_solicitacao_captacao` (AFTER INSERT em `solicitacoes`, só nos status
"em aberto": Trabalhando na busca do imóvel / Em Atendimento / Pendente /
Aguardando Aprovação Pablo) enfileira a solicitação em
`captacao_fila_solicitacoes` — sem HTTP dentro da trigger, de propósito,
pra nunca travar a transação do corretor esperando a GeckoAPI. O cron
`captacao-processar-fila` (6 em 6 min) processa a fila e, quando falta
material, liga os cursores de `captacao_varredura`; o cron
`captacao-repor-prospects` (20 em 20 min) é quem de fato consulta a API.

**Cuidado ao editar o gatilho de backfill**: ele só dispara em INSERT. Uma
auditoria em 13/08 achou 1.470 solicitações antigas — ativas, várias sem
nenhuma sugestão — que nunca tinham entrado na fila porque foram criadas
antes do gatilho existir. Backfill único aplicado
(`captacao_backfill_fila_completo`); se o gatilho for recriado ou uma nova
categoria de status "em aberto" for adicionada no app, rodar de novo:

```sql
insert into public.captacao_fila_solicitacoes (solicitacao_id)
select s.id from public.solicitacoes s
where s.status in ('Trabalhando na busca do imóvel','Em Atendimento','Pendente','Aguardando Aprovação Pablo')
on conflict (solicitacao_id) do nothing;
```

## Classificação (por que "sem CRECI" sozinho não bastava)

`fn_captacao_classificar()` usa três sinais, não só CRECI vazio — o campo
vazio sozinho dava 43% de "particular" e incluía imobiliárias reais (nome
com "imóveis", "corretor" etc.). Ordem: descartar (telefone claramente
falso) → empresa (CRECI presente) → empresa (nome de empresa) → particular
(nome com 2+ palavras, sem sinal de empresa) → indefinido. Yield real:
~6-8% de particular por página, não os 43% que o CRECI vazio sugeria.

## Onde a tela do captador lê os dados (confirmado, não mais suposição)

A tela "Minhas Captações" (worker `jazz-lead-conecta`, código fora deste
repositório) renderiza `tarefas_captacao` — confirmado batendo os FKs e o
trigger `trg_sugestao_after_insert` no banco, e verificando com uma
consulta direta que os cards "score / Reservar 7d / Captado por código"
correspondem a linhas de `tarefas_captacao` cujo `imovel_id` aponta pra
`imoveis`. `solicitacao_sugestoes_externas` (a tabela que a sessão criou
antes de mapear esse caminho) nunca teve relação com o que a tela mostra.
Ver "Achado ao avaliar o fluxo: descoberto o caminho real" acima pro
diagrama completo e o que foi corrigido.

Uma tarefa (`tarefas_captacao`) só é criada quando um trigger de INSERT em
`solicitacao_sugestoes` roda `fn_gerar_tarefa_passo1()`, e essa função
promove no máximo UMA sugestão por vez por solicitação, respeitando o
limite diário de contatos do captador (50 ligações / 20 WhatsApp) e um
teto de tarefas simultaneamente abertas. Uma solicitação pode ter dezenas
de sugestões `sugerido` em fila e mesmo assim mostrar "0 pendentes" na
tela se o captador responsável estiver com a cota de tarefas abertas
estourada — isso é limite operacional do captador, não falta de dado.

## Economia

1. Se o estoque de particulares já cobre o alvo pedido, devolve sem gastar
   crédito nenhum.
2. Cada cidade+tipo+portal tem cursor próprio — nunca relê a mesma página.
3. Ondas concorrentes reavaliam o estoque entre si — param assim que o alvo
   é atingido, em vez de gastar as ondas restantes.
4. Tudo que chega é gravado — uma chamada alimenta várias rodadas de
   `fn_captacao_processar_fila` depois.

## Variáveis / parâmetros do body

| Campo | Padrão | Uso |
|---|---|---|
| `alvo` | 30 | quantos particulares manter em estoque antes de parar de gastar crédito (teto 5000) |
| `maxPaginas` | 8 | cursores lidos nesta chamada (teto 40) |
| `concorrencia` | 4 | cursores disparados em paralelo por onda (teto 8) |
