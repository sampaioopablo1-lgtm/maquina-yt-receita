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
11/08 — melhor segurar um disponível do que anunciar um vendido). A v11
fechou a janela do meio de ciclo: o upsert já grava indisponível como
`ativo=false` (flag `indisponivel_espelho`), em vez de deixar a limpeza
só para o fechamento do ciclo — antes disso, um `precomputar` no meio do
ciclo podia fotografar vendidos como ativos. Nota:
os 311 carimbos existentes datam todos de 07/06/2026 (varredura em lote);
se um deles voltar ao mercado, limpe o `vendido_em` no espelho.

**Estado do anúncio segue o Vista.** Ao fechar cada ciclo de sync, a função
reconcilia `feed_properties.ativo` contra `vista_imoveis_log.ativo_vista`:
ativo no Vista volta a ligar, inativo no Vista desliga. Antes existia só o
caminho de desligar, e anúncios derrubados pela regra de "fantasma" (ausentes
do XML por mais de 7 dias) ficavam presos em inativo para sempre.

**O XML do Vista é quem manda sobre publicar.** O espelho `vista_imoveis_log`
é cego pra desativação: a sincronização lê a carteira ativa via API e um
imóvel desativado some da resposta em vez de vir marcado como inativo — foi
assim que 42426 e 44666 seguiram no ar com `ativo_vista = true` e geraram
lead errado (12/08). A trava está no banco, em
`fn_gate_feed_xml_vista()` (cron `feed-gate-xml-vista`, de 5 em 5 minutos):
o que não aparece no XML de portais do Vista entra em
`feed_property_portal_publicacao` como desabilitado, e o gerador de XML já
respeita essa tabela. Ficar no banco é proposital — o sync não passa por ali,
então um ciclo de sincronização não desfaz o bloqueio. `motivo =
'ausente_xml_vista'` separa o bloqueio automático do bloqueio feito por
pessoa: a regra só religa o que ela mesma desligou. `fn_vigia_gate_xml_vista()`
(cron `vigia-gate-xml-vista`, de hora em hora) alerta se algum ativo ausente
do XML escapar sem trava. Na aplicação, 282 anúncios ativos estavam ausentes
do XML do Vista e 183 deles estavam no ar: o feed caiu de 2.714 para 2.531.

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
(média dos vizinhos com GPS, marcadas com `gps_origem: cep_vizinho`) e, desde
13/08, por geocodificação do logradouro real via Nominatim/OpenStreetMap
(`gps_origem: nominatim`, Edge Function `geocode-enderecos`).

O resultado da varredura completa: **90,4% dos anúncios ativos com coordenada**
(3.329 de 3.681), contra 56% antes. Origem: 1.693 do próprio Vista, 1.510
geocodificadas, 126 ainda aproximadas por CEP vizinho. No XML publicado são
2.697 dos 3.000 anúncios.

Duas conferências foram necessárias, e ambas nasceram de erro observado:
`viaConfere` compara o nome da via devolvida com o logradouro pedido — passar
o CEP faz o Nominatim casar pelo CEP e devolver outra rua quando o logradouro
não existe na base ("Atlantica, Caraguatatuba" voltou como "Avenida Geraldo
Nogueira da Silva"). `cidadeConfere` exige o município no endereço devolvido —
a regra da via sozinha deixou passar um caso em 1.517, "Saldanha Marinho,
Campinas" casando com a rua homônima em Hortolândia. Coordenada errada é pior
que coordenada ausente, porque o comprador filtra por mapa.

Os 352 sem coordenada são logradouros que o OpenStreetMap não tem mapeados —
alameda interna de condomínio fechado, principalmente. Concentram-se em
Campinas (83), Atibaia (56), Bertioga (38), Caraguatatuba (29) e Bragança
Paulista (27). Não são preenchidos por média de bairro: centroide a
quilômetros do imóvel seria número inventado com cara de precisão.

Ressalva conhecida: o número aleatório trafega junto com CEP e coordenada
GPS reais, o que é internamente incoerente e pode motivar recusa do portal.
Se anúncios voltarem a ser desativados, o próximo passo é baixar o
`displayAddress` para `Neighborhood`.

## Filtros de emissão

Um anúncio ativo só entra no XML se tiver oferta válida (venda e/ou locação),
preço coerente com a transação, preço de venda entre R$ 15 mil e R$ 150
milhões, e pelo menos **7 fotos** (jpg/png/webp).

A régua de emissão (7) não é a mesma coisa que a régua de nota (20
residencial / 10 terreno-comercial, em `metaFotosPortal`). Até 12/08 as duas
eram a mesma, e isso custava estoque: mirando a nota máxima da categoria
Imagens, o feed publicava 2.531 anúncios quando 3.442 atendiam o piso do
portal. As duas passaram a viver separadas — `minFotosEmissao()` decide quem
entra, `metaFotosPortal()` segue alimentando o score, as sugestões de
melhoria e a ordem de prioridade. Quem tem book completo e ficha completa
continua no topo da fila; com o teto de 3.000 anúncios do contrato, o corte
por prioridade é o que decide quem fica de fora.

**Tour virtual** só é emitido quando a ficha tem tour 360 real. O link
padrão apontando para página própria foi removido na v7: o portal pontuou
0% na categoria com ele. Replicar o tour de um imóvel nos demais foi
descartado por ser enganoso ao comprador (mostra o interior de outro
imóvel) e por risco de derrubada em massa por duplicação.

Auditoria de 12/08 no XML nativo do Vista: o acervo tem **zero** tours 360.
As 6 tags `<VirtualTourLink>` preenchidas carregam vídeo do YouTube — quatro
Shorts, dois `watch`, e uma delas contém só `&quot;`. O classificador já
trata link de YouTube/Vimeo como vídeo e não como tour, então a categoria
sair zerada está correto e não é falha do pipeline. Enquanto não houver
captação de tour 360 de verdade, essa categoria não pontua.

**Características.** O Vista já entrega `<Feature>` no vocabulário do VRSync,
em inglês — `Pool`, `BBQ`, `Elevator`, `Maids Quarters`, 32 termos ao todo,
17.813 ocorrências no XML nativo. O mapeador original só conhecia o caminho
português→inglês (`/piscina/i` → `Pool`), então quase tudo caía fora: só 772
dos 3.000 anúncios publicados levavam características, contra 80% de
cobertura na origem. Desde a v16 o termo que já chega no vocabulário oficial
passa direto, e `BarbecueBalcony` — que o Vista emite colado — vira `BBQ` +
`Balcony`. Resultado medido: 2.612 anúncios com características (87%) e
15.053 tags emitidas.

## Variáveis de ambiente

| Variável | Uso |
|---|---|
| `JAZZ_PUBLIC_BASE_URL` | base do link de tour virtual próprio |
| `JAZZ_VIDEO_PADRAO` | vídeo de fallback quando o imóvel não tem um |
| `JAZZ_IPTU_PADRAO` | IPTU de fallback |
| `JAZZ_ANO_CONSTRUCAO_PADRAO` | ano de construção de fallback |
| `JAZZ_TELEFONE_CONTATO` | telefone no cabeçalho do feed |
| `JAZZ_FEED_MIN_LISTINGS` | piso do guard de estoque (padrão 50) |
| `JAZZ_FEED_MIN_FOTOS` | régua de fotos pra entrar no XML (padrão 7) |
| `JAZZ_FEED_MAX_LISTINGS` | teto de anúncios no XML (padrão 3000) |
