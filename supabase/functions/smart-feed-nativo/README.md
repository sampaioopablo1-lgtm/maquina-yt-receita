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

**Imóvel com data de venda sai do ar.** Desde a v10, `vendido_em`
preenchido no espelho conta como indisponível: o sync desliga e a
reativação ignora, mesmo com `ativo_vista = true` (decisão do usuário em
11/08 — melhor segurar um disponível do que anunciar um vendido). Nota:
os 311 carimbos existentes datam todos de 07/06/2026 (varredura em lote);
se um deles voltar ao mercado, limpe o `vendido_em` no espelho.

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
`All` (decisão do usuário em 11/08, para a categoria Endereço do portal
pontuar completa): o endereço é exibido inteiro, incluindo o número
aleatório. Imóveis sem logradouro no cadastro caem para `Neighborhood`.
Coordenadas ausentes são preenchidas por propagação de CEP idêntico
(média dos vizinhos com GPS, marcadas com `gps_origem: cep_vizinho`).

Ressalva conhecida: o número aleatório trafega junto com CEP e coordenada
GPS reais, o que é internamente incoerente e pode motivar recusa do portal.
Se anúncios voltarem a ser desativados, o próximo passo é baixar o
`displayAddress` para `Neighborhood`.

## Filtros de emissão

Um anúncio ativo só entra no XML se tiver oferta válida (venda e/ou locação),
preço coerente com a transação, preço de venda entre R$ 15 mil e R$ 150
milhões, e book completo pela régua do portal: 20 fotos para residencial,
10 para terreno e comercial (jpg/png/webp). A régua de fotos segue a nota
máxima da categoria Imagens do Grupo Zap — anúncio abaixo dela fica fora
até o book ser completado no Vista.

**Tour virtual** só é emitido quando a ficha tem tour 360 real. O link
padrão apontando para página própria foi removido na v7: o portal pontuou
0% na categoria com ele. Replicar o tour de um imóvel nos demais foi
descartado por ser enganoso ao comprador (mostra o interior de outro
imóvel) e por risco de derrubada em massa por duplicação.

## Variáveis de ambiente

| Variável | Uso |
|---|---|
| `JAZZ_PUBLIC_BASE_URL` | base do link de tour virtual próprio |
| `JAZZ_VIDEO_PADRAO` | vídeo de fallback quando o imóvel não tem um |
| `JAZZ_IPTU_PADRAO` | IPTU de fallback |
| `JAZZ_ANO_CONSTRUCAO_PADRAO` | ano de construção de fallback |
| `JAZZ_TELEFONE_CONTATO` | telefone no cabeçalho do feed |
| `JAZZ_FEED_MIN_LISTINGS` | piso do guard de estoque (padrão 50) |
