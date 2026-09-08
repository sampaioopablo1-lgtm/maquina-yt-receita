# Captação: por que o rendimento era 6%, e o que mudou

Migração: `jazz/supabase/migrations/20260909_captacao_radar_particulares.sql`

## O pedido e o que ele virou

O pedido original foi enriquecer os prospects com fonte externa — cruzar CPF
para achar o telefone do proprietário. **Isso não foi feito e não deve ser.**

Não existe fonte pública no Brasil que ligue CPF a telefone. O que o mercado
vende como "enriquecimento cadastral" vem de vazamento, e cruzar isso aqui
contaminaria a base inteira da Jazz sem volta — além de o telefone do anúncio
ter sido publicado para o comprador ligar, não para a imobiliária prospectar.

O diagnóstico também estava errado. O gargalo não era falta de fonte: eram
três defeitos na régua, dois deles derrubando proprietário de verdade antes de
chegar ao captador.

## Os três defeitos

### 1. `s/?a$` comia sobrenome comum

A régua tem `s/?a\.?$` para pegar "S/A" no fim do nome. Sem fronteira de
palavra antes do `s`, ela casa com qualquer nome terminado em "sa":

| nome | régua atual | corrigida |
|---|---|---|
| Nelson Barbosa | **empresa** | particular |
| Ana Sousa | **empresa** | particular |
| Marta Rosa | **empresa** | particular |
| Jose Pedrosa | **empresa** | particular |
| Rita Feitosa | **empresa** | particular |
| Predial S.A. | **particular** | empresa |
| Imoveis S/A | empresa | empresa |

Barbosa e Sousa estão entre os sobrenomes mais comuns do país. Esses
proprietários nunca chegaram ao captador, todo dia, desde que a régua existe.
E o erro andava nos dois sentidos: `Predial S.A.` passava como particular
porque o ponto entre o S e o A quebrava o casamento.

Correção: `\ys[./]?a\.?$`.

### 2. Telefone repetido não era sinal

Proprietário tem um imóvel, às vezes dois. Corretor autônomo sem CRECI no
anúncio e com nome de duas palavras — "Marcos Silva" — passava como
`particular` e queimava uma ligação. O que o denuncia não é o nome: é o mesmo
telefone em catorze anúncios.

O dado já estava na tabela, e já havia índice por telefone. Ninguém contava.
Agora conta: a partir de 4 anúncios no mesmo número (parametrizável), é
carteira, não dono.

### 3. A fila era ordenada por data, e a data favorece o corretor

Corretor republica quase diariamente; dono anuncia uma vez e espera. Ordenar
por `coletado_em desc` põe sistematicamente a carteira na frente do
proprietário. Agora a ordem é por score.

## O que o acervo passou a fazer

O acervo real (`vista_imoveis_log`, 3.894 fichas) é a vantagem que nenhuma
lista comprada tem, e estava fora do circuito.

- **Imóvel que já é nosso** sai da fila. O captador ligava oferecendo captação
  de algo que a Jazz já anuncia, e perdia a credibilidade na primeira frase.
- **Imóvel que esteve no acervo, saiu, e reapareceu anunciado por particular**
  (`ex_carteira`) vai para o topo. O dono tirou da imobiliária e está tentando
  vender sozinho: já provou que quer vender, já provou que aceita
  intermediação, e agora está descobrindo o trabalho que dá.
- **Mediana do m² por bairro** vira régua de preço. Anúncio de particular 10%
  abaixo da mediana é dono com pressa ou preço errado — os dois querem
  corretor.

### O casamento fraco não pontua, de propósito

Casar por (cidade, bairro, tipo, quartos, área ±5%, preço ±10%) parecia bom.
Medido na fixture: **casou 174 anúncios contra uma única ficha**, porque imóvel
padrão de bairro padrão tem esses cinco campos iguais aos milhares. Como
`ex_carteira` vale +40, isso jogaria lixo para o topo da fila.

Então o casamento fraco só anota o código para a ligação conferir
(`acervo_confianca = 'fraca'`). Só o casamento por endereço com número define
`ex_carteira` e `ja_no_acervo`.

## Não perturbe

`captacao_nao_perturbe` é uma lista por telefone, para sempre, checada antes de
qualquer sugestão. Quem pediu para não ser procurado não volta à fila nem se
anunciar outro imóvel daqui a um ano.

```sql
select public.fn_captacao_nao_perturbe('12999998888', 'pediu no telefone', 'luana');
```

## Uso

```sql
select public.fn_captacao_preparar();      -- classifica + cruza acervo + pontua
select * from public.fn_captacao_sugerir(10);
select public.fn_captacao_estoque();
```

`fn_captacao_preparar()` substitui a chamada solta de `fn_captacao_classificar()`
no pg_cron. A função de um argumento **substitui** a de zero argumentos: manter
as duas torna `fn_captacao_classificar()` ambígua ("function is not unique") e
quebraria os chamadores atuais. A migração faz o `drop` explícito.

## Como isto foi verificado

PostgreSQL 16 local. Fixture de 234 anúncios reproduzindo a distribuição da
auditoria de 13/08 (156 empresas, 16 telefones genéricos, 10 ambíguos, 10
particulares) mais os modos de falha: um corretor com 14 anúncios, três com 9,
um imóvel já no acervo, um que saiu do acervo, um abaixo da mediana do bairro e
um que pediu para não ser procurado.

**27 asserções, todas passando.** Entre elas: as empresas nomeadas na auditoria
seguem fora da fila; os 10 proprietários seguem `particular`; carteira não
ocupa vaga; `Newcore` (empresa de uma palavra) não vira particular; imóvel já
nosso e não-perturbe são bloqueados; o dedupe por telefone continua valendo;
`fn_captacao_classificar()` sem argumento continua funcionando; `preparar()` é
idempotente; e o pipeline não quebra com nulos, área zero ou tabela vazia.

A/B na mesma fixture, com a dinâmica real de datas (carteira republica, dono
não): a régua de produção entrega **9 de 10** úteis, com Marcos Silva ocupando
uma vaga. A nova entrega **10 de 10**, com o `ex_carteira` no topo.

### O que NÃO foi verificado

- Comportamento contra os prospects reais. A fixture é construída, não coletada
  — as proporções vêm da auditoria de 13/08, mas os nomes e telefones são
  inventados. O ganho do `s/?a$` em particular depende de quantos sobrenomes
  terminados em "sa" existem na base real; medir com
  `select count(*) from captacao_prospects where anunciante ~ '(?i)\ys[./]?a\.?$'`
  antes e depois.
- O limite de 4 anúncios por telefone é palpite calibrado, não medido. Vale
  rodar `fn_captacao_classificar(3)` e `(5)` na base real e comparar.
- Custo de crédito da GeckoAPI não muda: nada aqui coleta mais.
