# smart-feed-nativo

Edge Function que sincroniza o acervo do Vista CRM e gera o XML VRSync
consumido pelos portais (Grupo Zap / VivaReal / OLX).

`index.ts` é o bundle exatamente como está publicado no Supabase — é código
já empacotado, não a fonte original. Está versionado aqui para que exista
histórico e ponto de retorno: sem isso não há como voltar uma versão quando
um deploy quebra o feed.

## Ações

Invocada por POST com `{"acao": "..."}`:

- `sincronizar` — lê o XML do Vista (ou o espelho `vista_imoveis_log`),
  normaliza e grava em `feed_properties`. Processa até 1000 itens por
  execução, com cursor em `feed_sync_pendente`.
- `precomputar` — gera o XML VRSync completo e sobe para o bucket
  `feeds-precomputados/vrsync.xml`.

## Regras que valem a pena conhecer

**Estado do anúncio segue o Vista.** Ao fechar cada ciclo de sync, a função
reconcilia `feed_properties.ativo` contra `vista_imoveis_log.ativo_vista`:
ativo no Vista volta a ligar, inativo no Vista desliga. Antes existia só o
caminho de desligar, e anúncios derrubados pela regra de "fantasma" (ausentes
do XML por mais de 7 dias) ficavam presos em inativo para sempre.

**Desativação em massa é bloqueada.** Se os candidatos a desligar passarem de
20% do acervo ativo, nada é desligado e fica um erro no log — protege contra
um XML truncado do Vista zerar os portais.

**Estoque mínimo no XML.** `precomputar` falha com 500 se houver menos de 50
listings emitíveis, para preservar o cache do portal em vez de publicar um
feed vazio.

**Endereço.** O número de rua publicado é aleatório e estável por imóvel
(derivado do código, faixa 101–999), nunca o número real do cadastro; se o
sorteio coincidir com o real, é deslocado. O `displayAddress` vai como
`Street`, então o portal exibe rua e bairro mas não o número.

Ressalva conhecida: o número aleatório trafega junto com CEP e coordenada
GPS reais, o que é internamente incoerente e pode motivar recusa do portal.
Se anúncios voltarem a ser desativados, o próximo passo é baixar o
`displayAddress` para `Neighborhood`.

## Filtros de emissão

Um anúncio ativo só entra no XML se tiver oferta válida (venda e/ou locação),
preço coerente com a transação, preço de venda entre R$ 15 mil e R$ 150
milhões, e no mínimo 5 fotos em formato aceito (jpg/png/webp).

## Variáveis de ambiente

| Variável | Uso |
|---|---|
| `JAZZ_PUBLIC_BASE_URL` | base do link de tour virtual próprio |
| `JAZZ_VIDEO_PADRAO` | vídeo de fallback quando o imóvel não tem um |
| `JAZZ_IPTU_PADRAO` | IPTU de fallback |
| `JAZZ_ANO_CONSTRUCAO_PADRAO` | ano de construção de fallback |
| `JAZZ_TELEFONE_CONTATO` | telefone no cabeçalho do feed |
| `JAZZ_FEED_MIN_LISTINGS` | piso do guard de estoque (padrão 50) |
