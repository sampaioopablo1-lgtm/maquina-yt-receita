# "Services restricted" — o que eu posso fazer e o que so o dono pode

O dono colou o aviso do painel em 12/10 e pediu: *"ajuste para remover a
restricao"*.

    Services restricted
    Your projects are unable to serve requests as your organization has used
    up its quota. Resolve billing issues

## Eu NAO consigo remover isso, e o motivo nao e falta de tentativa

A restricao e **de cobranca, na organizacao**. Nao existe SQL, codigo, workflow
nem configuracao que a levante — e eu nao vou fingir o contrario depois de ter
passado semanas dizendo "e so esperar a virada do ciclo", que ficou falsificado
por 47 dias de 402 continuo.

E tem um limite de acesso em cima disso, medido agora:

| | |
|---|---|
| `list_organizations` | devolve **so `imobjazz-eng's Org`** |
| a org que tem o projeto de video | **`sampaioopablo1-lgtm`** — invisivel para este conector |

Logo eu nao leio o plano dela, nao leio a pagina de Usage dela e nao emito
pagamento. **O botao "Resolve billing issues" do proprio aviso e o caminho, e e
do dono.**

## MAS a maquina nao esta parada por causa disso — medido na mesma hora

Isto e o que muda a urgencia, e eu so soube hoje:

| rota | resultado as 13:4x |
|---|---|
| `execute_sql` no `vevocauwtarctfwngrch` | **funciona** |
| `pg_net` -> `ec.europa.eu` (Eurostat) | **200** |
| `pg_net` -> `www.googleapis.com` | **200** |
| REST / PostgREST | **402** |
| Storage | **402** |

**O 402 e do GATEWAY REST, nao do Postgres.** Entao medir, registrar e buscar
fonte institucional estao abertos, e publicar ja nao passa pelo Supabase desde
que o `retomar.yml` entrou. O que fica fechado e o REST, o Storage, e o pedaco do
runner que fala com o REST.

Ou seja: **resolver a cobranca e desejavel, nao bloqueante.** Se ele resolver,
voltam o Storage e o caminho automatico do `diario.yml`; se nao resolver, a
maquina continua produzindo pelo caminho que ela usou hoje — nove pecas.

## QUAL cota estourou: eu nao sei, e isso se ve em uma tela

Medido, o projeto nao esta grande: **banco 30 MB**, **Storage 114 objetos
somando 1.679 kB**. Portanto **nao foi tamanho de dado** — e por isso o pedido
anterior, de "apagar para liberar espaco", era um caminho vazio.

No plano Free, com dado deste tamanho, o que estoura e quase sempre **egress
(banda)** ou **invocacao de Edge Function**. Quem diz qual e a tela
**Organization -> Usage** da org `sampaioopablo1-lgtm`, e eu nao a alcanco.
**Olhe qual barra esta cheia antes de pagar por Pro**, porque se for egress,
subir de plano aumenta o teto mas nao conserta o que o consome.

## O QUE EU AJUSTEI, que e a parte que me cabe

**Nao gerar consumo.** Uma regra nova, e ela nasceu de um erro meu desta mesma
rodada: para sondar se um host responde pelo `pg_net`, eu pedi um dataflow do
Eurostat e trouxe **20.048.657 bytes para dentro do banco**. Isso e trafego, e
gravou 20 MB em `net._http_response` num banco de 26 MB.

**REGRA: sonda de disponibilidade pede endpoint PEQUENO.** Nunca um dump. E
apague a resposta grande no mesmo statement em que a leu — o `DELETE` dela
estourou o timeout de 60 s do MCP duas vezes (aprendizado 621, intermitente), e
o que salvou foi o TTL do proprio `pg_net`.

O resto do consumo do REST vem dos workflows que ainda o chamam e levam 402 a
cada ciclo (`diario.yml` em ~5 disparos/dia, mais `publicacao`, `autoria`,
`expurgo-storage`, `diagnostico`, `ponte-arquivo`, `reauth`, `kaggle-voz`).
**Nao os desliguei**: eles sao o caminho que volta quando a cobranca for
resolvida, e uma chamada que leva 402 transfere pouco. Se a tela de Usage
apontar egress, aqui e onde se mexe — e aí vale medir antes, nao cortar no
escuro.
