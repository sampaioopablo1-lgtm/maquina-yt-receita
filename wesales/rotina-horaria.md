# Rotina horária — construção contínua do CRM

Roda de hora em hora, em sessão nova, e continua a construção da operação de
SDR junto com o dono da conta.

## O que ela faz a cada execução

Escolhe **o item de maior valor**, não faz tudo:

| | Frente | O que envolve |
|---|---|---|
| A | **Verificar o CRM** | Auditoria de leitura, comparada com `auditoria-resultado.md`. Pipeline novo, campo novo, contato entrando, tag aplicada — tudo vira atualização do documento |
| B | **Executar o aprovado** | O que estiver com `[x]` em `APROVADO.md` e ainda não foi feito |
| C | **Melhorar a especificação** | Revisar `build-wesales.md` contra o que se sabe do CRM real, corrigindo nó, gatilho, nome de campo ou regra que não bate |
| D | **Fechar lacunas** | As lacunas L-01 a L-06 do briefing e os quatro itens que a auditoria não fechou: tags, workflows, calendários, formulários |

## O freio de mão

`APROVADO.md` é a única porta de escrita no CRM. Com ele vazio, a rotina lê o
CRM e trabalha na documentação — e mais nada. Foi feito assim de propósito:
uma rotina autônoma que cria coisa em CRM de produção sem autorização escrita é
como deixar a porta destrancada porque ninguém costuma passar ali.

## Quando dá erro

A rotina não desiste na primeira. A ordem é: ler a mensagem inteira, pesquisar
na internet — issues do GitHub, blogs, fóruns, documentação oficial do HighLevel
e do MCP —, testar a hipótese e corrigir. Só registra como bloqueio depois de
**três abordagens diferentes**.

O que aprender vai para `APRENDIZADOS-CRM.md`, para a execução seguinte não
refazer a mesma investigação. É o que evita a rotina descobrir a mesma coisa
vinte e quatro vezes por dia.

**Uma exceção com regra própria, medida em 22/09/2026:** `403` do conector
(`The token does not have access to this location.` ou `Forbidden resource`)
**não** é bloqueio de acesso até ser provado. Repita a chamada com
`locationId: 1D53YTI9C7oIMBavcQxV` explícito antes de qualquer outra coisa —
na medição, as mesmas chamadas que davam `403` sem o parâmetro voltaram `200`
com ele, e um endpoint de `opportunities` reportou a mesma falta como `422
locationId can't be undefined`. Só se o `403` sobreviver ao parâmetro
explícito é que se suspeita do token. Procedimento completo em
`conectar.md`, seção "Quando der 403".

## Conector: resolvido

A rotina nasceu sem o conector anexado — a API de criação desta organização não
aceitava anexar. **Resolvido:** ela agora carrega `GHL-CRM`
(`services.leadconnectorhq.com/mcp`), além de Cloudflare e Composio. As quatro
frentes funcionam.

## Um detalhe para conferir na primeira rodada

A configuração de sessão da rotina declara como destino os branches
`claude/keen-knuth` (neste repositório) e `claude/bold-cannon` (em
`proximo-cliente`), que não são o branch do projeto. O prompt manda commitar em
`claude/amazing-johnson-mclksg`, e é isso que deve prevalecer — mas se os
commits da primeira execução não aparecerem no PR #93, é aqui que eles foram
parar.

## Limites

- Só mexe em `wesales/`. O repositório também abriga a máquina de vídeo e a
  Jazz, e a fronteira vale para a rotina também
- Não encosta nas 12 falhas de `tests/test_narracao_das_specs.py` — são
  pré-existentes e de outro projeto
- Sem nada de valor a fazer, não commita e encerra em silêncio. Commit vazio
  não é sinal de trabalho

## Controlar

Pausar, mudar o intervalo ou desligar: é só pedir. Ela não se cancela sozinha.

## Número oficial de teste (23/09/2026)

Para qualquer teste que precise mandar ou receber WhatsApp de verdade:
**+55 21 98742-9940** — contato "Pablo Sampaio" (`rdaijzR0ZVCmXLAJ6jT2`), celular
do dono. **Nunca** usar +55 12 98238-1407 (é o número conectado à Stevo). Lead
real nunca é usado em teste.
