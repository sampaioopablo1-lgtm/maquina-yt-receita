# chavesnamao-feed

Edge Function que gera o XML do acervo da Jazz no **padrão do portal Chaves na
Mão** e sobe para `feeds-portais/chavesnamao.xml`.

URL entregue ao portal:

```
https://cscczluzpblzhvojxanp.supabase.co/storage/v1/object/public/feeds-portais/chavesnamao.xml
```

Diferente do `smart-feed-nativo`, aqui há **fonte legível** versionada, não
bundle: `gerador.ts` (puro, sem Deno/Supabase — só dado → texto) e `index.ts`
(leitura da tabela, filtros, upload).

## Ações

POST com `{"acao": "..."}`:

- `precomputar` — gera o XML e sobe para o Storage.
- `prever` — gera, **não sobe**, e devolve contagem, bytes e o primeiro
  `<imovel>` como amostra. É o modo de conferir mudança de regra antes de
  publicar.

Agendamento: cron `feed-precomputar-chavesnamao`, `40 6,18 * * *` (03:40 e
15:40 de Brasília). O portal lê o arquivo uma vez por dia — duas gerações
diárias bastam, e a cadência baixa é resposta direta ao incidente de 19/08,
quando precompute de 10 em 10 minutos derrubou o feed inteiro por CPU.

## O que vem do padrão do portal (e não de preferência nossa)

**Estrutura fixa.** Raiz `<Document>` → `<imoveis>` → `<imovel>`, 53 tags por
imóvel, **todas presentes mesmo vazias**, nomes case sensitive. A saída foi
conferida tag a tag contra o XML de exemplo publicado pelo portal: mesma lista,
mesma ordem.

**PNG não entra.** O portal processa JPG, JPEG e WEBP. PNG é descartado aqui
mesmo, em vez de virar foto quebrada no anúncio — e o contador
`fotos_descartadas` na resposta mostra quanto foi. (O VRSync aceita PNG, então
este feed é mais estreito que o outro de propósito. O conversor
`feed-trocar-fotos-convertidas` é quem reduz esse número.)

**Teto de 30 fotos por imóvel.** O que passa disso o portal ignora; o corte é
feito antes, na ordem em que as fotos chegam do Vista.

**Descritivo até 3.000 caracteres**, título até 100 — mesma régua de higiene do
feed do Zap (sem telefone, sem link, sem emoji, sem CAIXA ALTA, sem jargão de
anúncio).

**Vídeo só do YouTube e só link de navegador.** Sem `/embed/`, sem Shorts, sem
Vimeo: a documentação pede link que abra normalmente no navegador. Tour 360 só
quando é tour de verdade — link de vídeo em `tour_virtual` não vira `tour_360`.

**Tipo e finalidade andam juntos.** As listas de tipos do portal são separadas
por finalidade, e a string tem que bater exatamente ("Casa / Sobrado em
Condomínio", "Conj. Comercial / Sala"). `Sítio / Chácara` só existe na lista
residencial e `Fazenda` só na comercial — por isso um sítio sai como `RE` e uma
fazenda como `CO`. `RU` (rural) não é usado: o portal não publica lista de
tipos para essa finalidade.

**`data_atualizacao` em vez de truque de preço.** O feed do Zap desloca
centavos toda semana para forçar reindexação. Aqui não: o padrão tem campo
próprio de atualização, que sai de `feed_properties.updated_at`, e o preço vai
inteiro.

## Decisões nossas, que valem revisão

**Contagem de cômodos derivada de característica.** O portal tem campos
numéricos (`closet`, `varanda`, `lareira`, `escritorio`, `despensa`, `bar`,
`area_servico`, `quarto_empregada`) que o Vista não numera. Quando a
característica diz que existe, o feed publica **1** — nunca um número
inventado. Subnotifica (duas varandas viram "1") e isso é deliberado:
superestimar seria anúncio falso.

**Áreas comum e privativa.** As características chegam em dois vocabulários
misturados — os termos nativos do VRSync que o Vista emite em inglês (`Pool`,
`BBQ`, `Elevator`) e texto livre em português — e são traduzidas para itens em
português. O portal **ignora silenciosamente** item fora da lista dele, então a
tradução erra para o lado de mandar mais: item desconhecido não custa nada,
item faltando custa filtro de busca. A lista canônica do portal vive em
`chavesnamao.com.br/imoveis/integracao/areas_comuns` (e `.../areas_privativas`)
e **ainda não foi conferida contra o mapa daqui** — quando for, o ajuste é só
nas tabelas `AREA_COMUM`/`AREA_PRIVATIVA` do `gerador.ts`.

**Número da rua é sorteado, estável por imóvel, nunca o real** — mesma decisão
do feed VRSync (11/08), e com a mesma ressalva: o número sorteado viaja junto
com CEP e GPS reais, o que é internamente incoerente e pode motivar recusa. Se
o portal reclamar, `JAZZ_CNM_ESCONDER_ENDERECO=1` publica tudo com
`esconder_endereco_imovel = 1` sem republicar o bundle. Imóvel sem logradouro
já sai assim.

**Cidade e bairro são obrigatórios no padrão**, então anúncio sem eles não é
emitido: ocuparia vaga e seria recusado na importação.

## Bloqueios: o que este feed respeita

`feed_property_portal_publicacao` é por portal. Este gerador lê:

- `portal = 'chavesnamao'` — bloqueio deste portal;
- `portal = 'vrsync_rede'` — **menos** `motivo = 'fotos_abaixo_da_meta'`.

A exceção tem razão: aquela régua (12 fotos) é a nota de Imagens do Grupo OLX
dentro de um contrato de 3.000 vagas. O Chaves na Mão não publica exigência
assim, e derrubar anúncio por régua de outro portal seria jogar estoque fora.
Já `ausente_xml_vista` (sumiu do XML do Vista) e `duplicado_no_portal` falam do
imóvel, não do portal, e valem aqui também — imóvel desativado no Vista não
pode ser anunciado em lugar nenhum.

## Filtros de emissão

Entram no XML os anúncios `ativo = true` que tenham: oferta válida (venda e/ou
locação), preço coerente com a transação, preço de venda entre R$ 15 mil e
R$ 150 milhões, cidade e bairro preenchidos, e pelo menos **7 fotos** em
formato aceito pelo portal (jpg/jpeg/webp — o PNG já saiu da conta).

A ordem da fila é a mesma do outro feed: book completo e ficha completa
primeiro; o teto corta por baixo.

**Guard de estoque.** Menos de 50 imóveis emitíveis derruba a execução com
erro em vez de subir arquivo curto — o portal substitui a carga inteira pelo
que baixa, então um XML pela metade apagaria o acervo. Falhar mantém no ar o
arquivo do dia anterior.

## Variáveis de ambiente

| Variável | Uso | Padrão |
|---|---|---|
| `JAZZ_CNM_BUCKET` | bucket do arquivo | `feeds-portais` |
| `JAZZ_CNM_OBJETO` | nome do objeto | `chavesnamao.xml` |
| `JAZZ_CNM_MAX_LISTINGS` | teto de anúncios (0 = sem teto) | `3000` |
| `JAZZ_CNM_MIN_LISTINGS` | piso do guard de estoque | `50` |
| `JAZZ_CNM_MIN_FOTOS` | régua de fotos para entrar | `JAZZ_FEED_MIN_FOTOS` ou 7 |
| `JAZZ_CNM_DESTAQUES` | quantos do topo da fila vão como `destaque=1` | `0` |
| `JAZZ_CNM_ESCONDER_ENDERECO` | `1` esconde o endereço de todos | desligado |
| `JAZZ_CNM_LINK_TEMPLATE` | link do imóvel no site; `{codigo}` é substituído | vazio |

## Como vai ao ar

Dois passos no projeto da Jazz: a migração `20260918_feed_chavesnamao.sql` e o
deploy desta função. Existem dois caminhos, descritos com os segredos exatos em
`jazz/docs/PORTAL-CHAVES-NA-MAO.md` — o conector Supabase da conta (que hoje
está em `needs_reconnect`) ou o workflow `jazz-publicar-feed-chavesnamao.yml`,
que roda os dois passos no runner do Actions e não depende do conector.

O contêiner das sessões do Claude não alcança `*.supabase.co` (egresso
bloqueado pela política do ambiente), então publicar daqui por HTTP direto não
é opção nem com chave em mãos.

## Pendências conhecidas

1. Conferir o mapa de áreas comum/privativa contra as listas oficiais do
   portal (as páginas exigem acesso ao site do Chaves na Mão).
2. `fn_vigia_feed_auditar()` lê a idade do XML por bucket, sem filtrar o nome
   do objeto. Enquanto isso não for corrigido, este feed mora em bucket
   separado para não contaminar a auditoria do feed do Zap.
3. Não existe vigia próprio deste arquivo. O mínimo seria alertar quando o
   objeto passar de 26 h sem atualização — o portal lê uma vez por dia e uma
   falha silenciosa some por uma semana.
4. Duplicação de código com o `smart-feed-nativo` (higiene de texto,
   prioridade, endereço público). Só existe porque o que está versionado
   daquela função é bundle publicado, não fonte; quando a fonte voltar ao
   repositório, as duas viram um módulo comum.
