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

---

## As duas portas de saída (correção de 10/09)

Existem **dois** caminhos que entregam prospect, e eles selecionam diferente:

| | `fn_captacao_sugerir` | `fn_captacao_processar_fila` |
|---|---|---|
| o que é | a fila do captador, sob demanda | as **10 sugestões por solicitação** |
| dispara | chamada manual / rotina | gatilho de solicitação nova + cron 6 min |
| seleciona por | score | perfil + proximidade da faixa de preço do cliente |

As melhorias de 09/09 e 10/09 foram todas para a primeira. A segunda monta a
própria consulta e só olhava `perfil` — herdou a régua de classificação, mas
**não herdou nenhum dos bloqueios**.

Na prática, no fluxo que de fato entrega as 10 ao corretor:

- quem pediu para **não ser procurado** continuava sendo sugerido;
- imóvel que a própria Jazz já anuncia continuava sendo sugerido;
- anúncio que já saiu do portal continuava sendo sugerido.

O primeiro é o que importa: uma lista de não perturbe que vale em uma porta e
não na outra não é uma lista de não perturbe.

Demonstrado no teste, e vale registrar como quase passou batido: com faixa de
preço larga (400–800k) os bloqueados caíam para 11º por proximidade de preço e
o vazamento não aparecia. Só com faixa estreita em torno do preço deles
(640–700k) o `Dario Fontes`, que está no não perturbe, apareceu em primeiro na
lista do corretor.

Correção em `20260910_captacao_fila_solicitacao_respeita_radar.sql`: um filtro
`coalesce(p.score, 1) > 0` e o score como desempate. O `coalesce` deixa passar
quem ainda não foi pontuado, então antes da primeira execução de
`fn_captacao_score` o comportamento é idêntico ao de hoje.

A ordenação por proximidade da faixa do cliente **continua dominante** depois
do perfil: aqui não é lista fria, é casamento com uma solicitação real, e
orçamento é o que faz a sugestão servir.

## PF/PJ e logo do anunciante (14/09/2026)

Diagnóstico com o print da busca real: as dez opções vieram marcadas
"Imobiliária" e **estavam certas** — "SANT ANA INVESTIMENTOS" casa em `invest`
no regex de nome. O classificador não errou. O que falta é **oferta de
particular**: sem dez donos na fila, a busca completa o número com carteira.

Então o ganho não está em apertar contra imobiliária, está em parar de perder
o dono de verdade.

### Sinal 1 — PF/PJ, que já chegava e ninguém lia

O extrator grava `dados.advertiser_type` do Chaves na Mão desde 13/08, com o
comentário "guardado pra um futuro ajuste do classificador". Ficou um mês
gravado e ignorado. É o sinal mais direto da coleta: o portal declarando
pessoa física ou jurídica, sem inferência por nome.

O lado que mais rende é o **PF**, porque a régua de nome exige duas palavras
para dizer "particular" — quem anuncia como "Marcelo" ficava `indefinido` e
não entrava na fila. Com PF declarado e telefone em um anúncio só, é dono.

O resgate fica **depois** da contagem de telefone de propósito: corretor
autônomo é pessoa física de verdade, e o que o denuncia é o mesmo número em
catorze anúncios, não o cadastro.

### Sinal 2 — logo do anunciante

Observação do usuário: "as imagens, com logo, normalmente são de
imobiliárias". Está certo, e não é preciso analisar pixel: quem tem logo tem
**cadastro de logo** no portal, e o objeto `advertiser` já é guardado inteiro.
Pessoa física não sobe logotipo.

A varredura é por *nome de chave* contendo "logo", não por chave fixa: o campo
aparece como `logoUrl`, `logo` e `logotipo` conforme o portal, e fixar um nome
faria o sinal sumir calado numa renomeação.

### A trava do sinal de logo

Se o portal passar a devolver logo (ou avatar padrão) para **todo** anunciante,
a regra deixa de separar nada e marca a base inteira como empresa — zerando a
oferta de particular, que é o problema que isto veio resolver. Falharia para o
lado pior, e calada.

Por isso o sinal só vale enquanto for minoria: acima de 60% da base ele se
desliga sozinho, e o retorno do classificador diz `logo_em_uso: false`. Medido
no teste: com 90% de logo, a trava desliga e os 10 particulares sobrevivem;
com o teto solto em 1.0, 9 viram empresa.

### Antes de confiar no sinal 2, meça

```sql
select * from public.fn_captacao_diagnostico_anunciante();
```

Devolve, por fonte, quantos prospects têm PF, PJ e logo, e **quais chaves de
logo** aparecem de fato. Se vier tudo zero, o campo não está sendo entregue e o
sinal é inerte — não quebra nada, mas também não ajuda, e é melhor saber por
medida do que por suposição.

### Armadilha de deploy

A migração dropa `fn_captacao_classificar()` **e** `fn_captacao_classificar(int)`.
A assinatura nova tem dois parâmetros com default; deixar a de um argumento viva
faz `fn_captacao_classificar(4)` — a chamada do pg_cron e de
`fn_captacao_preparar` — virar ambígua (`function ... is not unique`) e a
captação para. Foi o teste que pegou isso, não a leitura.

### Verificação

`jazz/scripts/teste_captacao_pf_pj_logo.sql` — 12 asserções em PostgreSQL 16:
o resgate do PF de uma palavra, PJ com nome inocente, logo pegando quem o nome
não pegava, grafia alternativa da chave, logo vazio não contando, PF com
carteira seguindo empresa, e os seis casos que já funcionavam sem mudar de
classe (Nelson Barbosa particular, SANT ANA empresa, Ltda empresa, CRECI
empresa, Newcore indefinido, telefone falso descartar).

`jazz/scripts/teste_captacao_trava_logo.sql` — a trava nos dois sentidos, e a
migração aplicada duas vezes para provar idempotência.
