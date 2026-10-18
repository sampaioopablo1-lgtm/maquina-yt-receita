# Meta Ads pelo MCP — estado da conexão e da conta "O Próximo Cliente"

> Lido em 06/09/2026 direto pelo conector Meta Ads (MCP), sem print. Continua o
> mapa do funil em `docs/19-funil-mentoria-proximo-cliente.md` (PR #82), que
> foi escrito a partir de uma tela do Gerenciador antes de o conector existir.
> Os ids abaixo são os que as ferramentas do conector pedem.

## A conexão

O conector responde e enxerga **60 contas de anúncio** do usuário. Nem todas
estão liberadas: a Meta libera o MCP conta a conta ("gradually being rolled
out"), e algumas voltam bloqueadas, suspensas ou com pendência de pagamento.

O que o conector **faz** hoje nas contas liberadas: lê campanhas, conjuntos e
anúncios publicados com métricas; lê públicos, pixels, páginas, vídeos e
imagens; cria campanha, conjunto, criativo, anúncio e público; pausa e ativa.

O que ele **não faz** nestas contas: ler **rascunhos** do Gerenciador. A
campanha `REC | TOPO` montada em 04/09 era rascunho — o conector não a vê, e
ela não existe como campanha publicada em nenhuma das duas contas abaixo.

## As duas contas que importam

| | O Próximo Cliente | SX Educação 01 |
|---|---|---|
| id da conta | `1695865631502778` | `966354405737730` |
| negócio | sxeducacao (`1367006478234906`) | sxeducacao |
| status | ACTIVE, MCP liberado, consultável | ACTIVE, MCP liberado, consultável |
| **forma de pagamento** | **não tem** | tem |
| campanhas publicadas | nenhuma | 27, todas pausadas, R$ 0 em 30 dias |
| páginas promovíveis | nenhuma vinculada | O Próximo Cliente e SX Educação |
| Instagram vinculado | nenhum | nenhum |
| vídeos na biblioteca | nenhum | 10+ (material antigo da SX) |
| imagens | 1 ("untitled") | — |

A conta "O Próximo Cliente" é a certa para o funil: é nova, sem histórico
poluído, e já recebeu o pixel e os públicos. Mas **sem forma de pagamento nada
publica** — é a primeira coisa a resolver, e só o dono faz.

## O que já foi feito na conta (05/09, pelo Gerenciador)

- **Pixel / conjunto de dados** `O PRÓXIMO CLIENTE` (`1600846091439175`),
  criado 05/09 e atribuído à conta. Nunca disparou — esperado, não há site.
- **Nove públicos personalizados** por lista de clientes (CSV), todos ativos:

| Público | Tamanho aprox. |
|---|---|
| Cópia de Editado - CNAE 41 42 43 RJ 100K - Editado | 41–48 mil |
| Editado - CNAE 41 42 43 RJ 100K.csv | 29–35 mil |
| Cópia de Leads empresaqui CONSULTORIA BR.csv | 24–28 mil |
| Contabilidade BR 25K 2.csv | 8,7–10 mil |
| Leads empresaqui Instituição de ensino BR.csv (2 versões) | 6–9 mil cada |
| Leads empresaqui Saas BR.csv | 6–8 mil |
| Contabilidade RJ.csv | 3–4 mil |
| Contabilidade BR 25K 1.csv | 2–2,5 mil |

Isso muda o plano do topo em relação ao doc 19. Lá o público frio era por
comportamento e interesse (administradores de página, pequenos empresários).
Agora existem **listas de empresários por CNAE e segmento** — construção civil
(CNAE 41/42/43), contabilidade, consultoria, SaaS, ensino. Lista de cliente é
público mais preciso que interesse, e serve de **semente de semelhante** desde
o primeiro dia, sem esperar o público de vídeo encher.

Ajuste sugerido no `REC | TOPO`: um conjunto `LISTAS` (todas as listas
empilhadas, ~120 mil pessoas) ao lado do conjunto `INTERESSES`, mesma verba,
mesmos cinco vídeos, sete dias. O conjunto `ADM DE PÁGINAS` do print fica como
terceiro se a segmentação por comportamento ainda existir no Gerenciador.

## Páginas

- `O Próximo Cliente` — id `1117439194786453`. O usuário tem permissão de
  anunciar por ela. **Termos de Cadastro (lead ads) não aceitos** — bloqueia a
  camada 2 (formulário instantâneo). Aceitar em
  https://www.facebook.com/legal/leadgen/tos antes da semana 2.
- `SX Educação` — id `993057757216875`. Mesma pendência de termos.

## Checklist para ligar a camada 1 pelo conector

Do dono (o conector não faz):

- [ ] Forma de pagamento na conta `1695865631502778`
- [ ] Cinco vídeos 9:16 dos cinco ângulos (doc 19), virada antes do segundo 15
- [ ] Aceitar os termos de lead ads na Página (para a camada 2)
- [ ] Vincular o Instagram à Página (para o posicionamento em Reels e o
      público de engajamento)

Do conector, assim que os itens acima estiverem prontos:

- [ ] Subir os cinco vídeos na conta
- [ ] Criar `REC | TOPO` (reconhecimento, ThruPlay) com dois conjuntos,
      `LISTAS` e `INTERESSES`, R$ 25–30/dia cada, frequência 2 a cada 7 dias
- [ ] Um anúncio por ângulo em cada conjunto, nome `[ângulo]-[formato]-[data]`
- [ ] Públicos de vídeo `VV_THRUPLAY_30D`, `VV_50_60D`, `VV_75_90D` (doc 19)
- [ ] Semelhante 1% da lista `CNAE 41 42 43 RJ` como terceiro conjunto de teste

## Como ler isto de novo

Pelo conector, sempre com o id da conta:

- campanhas e métricas: `ads_get_ad_entities` (nível campaign, adset, ad)
- públicos: `ads_get_ad_account_custom_audiences`
- pixel: `ads_get_datasets`
- páginas e termos de lead ads: `ads_get_ad_account_pages`
- erros que travam entrega: `ads_get_errors`
