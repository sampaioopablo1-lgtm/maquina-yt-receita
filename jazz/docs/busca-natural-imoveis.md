# Busca de imóveis em linguagem natural (barra única)

Migração: `jazz/supabase/migrations/20260903_busca_natural_imoveis.sql`

## O que muda pro visitante

Uma barra só, como no Google. Ele digita a frase inteira:

```
apartamento 3 quartos no Jardim Aquarius até 700 mil
```

e recebe a lista filtrada. Sem combo de tipo, sem combo de cidade, sem slider
de preço antes de ver o primeiro imóvel. O filtro estruturado continua
existindo — mas como refinamento **depois** dos resultados, não como pedágio
antes deles.

## Por que o parser mora no banco

Três razões, nesta ordem:

1. **O dicionário de bairro e cidade é o acervo.** `busca_lugares` é uma
   materialized view sobre `vista_imoveis_log`; bairro novo no XML do Vista
   entra na busca sozinho. Uma lista mantida à mão no frontend envelhece na
   primeira captação.
2. **A mesma interpretação serve mais de uma porta.** Site, WhatsApp e o CRM
   chamam `fn_interpretar_busca` e recebem o mesmo JSON. Parser no React
   significaria reescrevê-lo em cada canal.
3. **Filtro e índice no mesmo lugar.** O que o parser decide vira `where` na
   mesma transação, com o GIN do `tsvector` ao lado.

## Contrato

### `rpc_buscar_imoveis(q text, limite int, pagina int, ordenar text) -> jsonb`

`security definer`, exposta a `anon` e `authenticated`. `ordenar` aceita
`relevancia` (padrão), `preco_asc`, `preco_desc`, `recentes`. `limite` é
travado entre 1 e 60.

```json
{
  "ok": true,
  "total": 12,
  "pagina": 1,
  "limite": 24,
  "ordenar": "relevancia",
  "busca_ampliada": false,
  "interpretacao": {
    "categoria": "Apartamento",
    "dormitorios": 3,
    "bairro": "Jardim Aquarius",
    "preco_max": 700000,
    "texto_livre": null,
    "consulta": "apartamento 3 quartos no Jardim Aquarius até 700 mil"
  },
  "itens": [{ "codigo": "AP1001", "categoria": "Apartamento", "bairro": "...",
              "valor_venda": 690000, "foto_destaque": "...", "relevancia": 0 }]
}
```

Duas coisas que a resposta carrega de propósito:

- **`interpretacao`** é pra ser mostrada na tela como chips removíveis
  ("Apartamento ✕", "3+ quartos ✕", "até R$ 700 mil ✕"). É o que dá ao
  visitante o controle que o combo dava, sem cobrar o clique adiantado — e é
  o que evita a pergunta "por que esse imóvel apareceu?".
- **`busca_ampliada: true`** diz que a frase não casou com nada no corte
  textual e a busca foi repetida sem ele. A tela deve dizer isso ("não
  encontramos *heliponto*; veja o que temos perto"), nunca fingir que aquele
  era o resultado pedido.

A RPC só devolve ficha com `ativo_vista = true` e só coluna de vitrine.
`corretor_*`, `captador_id`, proprietário e `raw` **não** passam por ela: o
site é anônimo.

### `fn_interpretar_busca(q text) -> jsonb`

O parser isolado, pra depurar uma frase sem rodar a busca. Extrai, nesta
ordem: finalidade, área, preço, contagens, categoria, lugar, código.

A ordem não é decorativa — em *"acima de 250 m2"* o número é metragem, e o
regex de piso de preço casaria nele primeiro se viesse antes.

O que a frase não disser, ninguém filtra: campo ausente é campo livre. O que
ela disser e o parser não reconhecer (`piscina`, `mobiliado`, nome de
condomínio fora do dicionário) vira `texto_livre` e busca no `tsvector`, com
peso A pra empreendimento/bairro/cidade/categoria, B pra endereço e descrição,
C pra características.

## Convenções que a busca assume

- **Contagem é piso, não igualdade.** "3 quartos" traz 3 e 4 dormitórios —
  ninguém recusa um quarto extra dentro do orçamento.
- **Número sem escala abaixo de 10.000 é milhar.** "apartamento de 700"
  significa 700 mil, não R$ 700.
- **`entre 400 e 600 mil`**: a escala do segundo número vale pros dois.
- **Preço é `valor_venda`, com fallback pra `valor_locacao`.** Sem
  `finalidade` na frase, uma ordenação por preço mistura venda e locação na
  mesma régua. Quando a barra não disser a finalidade, a tela deve ordenar por
  relevância — que é o padrão.
- **Código digitado direto** (`AP1002`) é busca exata e ignora o resto.

## Manutenção

`busca_lugares` precisa de refresh depois de cada carga do feed:

```sql
select public.fn_busca_lugares_refresh();  -- refresh concurrently
```

Pendura no mesmo pg_cron que já roda o espelho do XML. Sem refresh, bairro
recém-captado cai no `texto_livre` em vez de virar filtro — degrada, não
quebra.

## Como isto foi verificado

Cluster PostgreSQL 16 local, tabela `vista_imoveis_log` recriada com as
colunas reais do espelho e 7 fichas (uma desativada). Conferido:

- as 6 frases de exemplo devolvem exatamente os códigos esperados;
- `ativo_vista = false` não aparece em nenhuma busca;
- barra vazia devolve a vitrine inteira, sem filtro;
- frase que não casa (`mansao com heliponto`) devolve `busca_ampliada: true`
  e o acervo, não tela vazia;
- paginação (`limite`/`pagina`), as quatro ordenações e `limite = 0` (trava
  em 1) se comportam;
- duas chamadas na mesma transação não colidem na tabela temporária.

O que **não** foi verificado: comportamento com os 3.894 registros reais —
plano de execução e escolha de índice mudam com a massa, e a materialized
view de lugares nunca rodou contra o acervo inteiro. Medir na primeira
aplicação.
