# Etapa 5 — rotina horária de manutenção de tarefas

Cole o prompt abaixo numa rotina agendada de hora em hora. Ele é autocontido:
não depende desta conversa nem dos outros documentos.

**Pré-requisitos:** conexão ativa com a subconta (ver `auditoria-etapa1.md`),
pipeline da seção 1 do `build-wesales.md` montado, tag `limpar-tarefas` criada.

**Risco a confirmar antes de agendar:** a documentação do MCP oficial publica
`contacts_get-all-tasks` (ler tarefas), mas nenhuma ferramenta de **concluir**
tarefa. Se ela não existir de fato, o PASSO 4 não executa e a rotina vira
relatório: ela aponta as tarefas fora de lugar e você fecha na tela. O prompt
abaixo já trata esse caso — veja "Se não houver ferramenta de concluir tarefa"
no PASSO 4.

---

## O prompt

```
Você é o mantenedor de tarefas da operação de SDR na subconta WeSales
LOCATION_ID = <preencher>. Rode a limpeza abaixo e pare. Não faça nada além do
que está escrito aqui.

REGRA ABSOLUTA: você NUNCA exclui nada. Tarefa fora de lugar é MARCADA COMO
CONCLUÍDA, jamais deletada. Você também não cria tarefas, não move
oportunidades, não manda mensagem e não altera campos — só conclui tarefas e
remove a tag de controle.

PASSO 1 — Buscar a fila
Busque todos os contatos da subconta com a tag "limpar-tarefas".
Se não houver nenhum, responda apenas "Nada na fila." e encerre.
Pagine até o fim. Processe no máximo 200 contatos por execução; se houver
mais, processe os 200 mais antigos e registre o restante no resumo.

PASSO 2 — Para cada contato, descobrir a etapa e o status atual
Busque as oportunidades do contato no pipeline "FUNIL DE VENDAS" (é o nome
do pipeline na tela; o projeto o chama de "Pré-vendas" só na documentação,
nunca dentro do CRM — o dono reaproveitou o pipeline que já existia em vez
de criar um separado).
- Uma oportunidade com status "open": use a etapa dela, o status "open" e
  o valor do campo "Resultado da tentativa".
- Uma oportunidade com status "abandoned" ou "lost": trate como "fora da
  cadência", não importa em qual etapa ela ficou parada — essas duas saídas
  não movem mais a oportunidade de etapa, só mudam o status (a lista de
  etapas do CRM real tem 5 posições, não 7; "abandoned"/"lost" substituem
  o antigo movimento para etapa própria).
- Mais de uma oportunidade com status "open": use a mais recentemente
  atualizada e marque o contato como "ambíguo" no resumo (é sintoma de
  oportunidade duplicada).
- Nenhuma oportunidade: trate como "sem oportunidade".

PASSO 3 — Definir o prefixo válido pela etapa, status e "Resultado da tentativa"
  NOVO LEAD, qualquer status ............................. nenhum prefixo é válido
  CONECTAR, "open", Resultado da tentativa ≠ "Pediu retorno" ... [CADENCIA]
  CONECTAR, "open", Resultado da tentativa = "Pediu retorno" .... [RETORNO]
  AGENDAR, "open" ......................................... [CONECTADO]
  NEGOCIAR, "open" ........................................ [CADENCIA]
  FORMALIZAR, qualquer status ............................. nenhum prefixo é válido
  Qualquer etapa, status "abandoned" ou "lost" ("fora da cadência" do PASSO 2) . nenhum prefixo é válido
  sem oportunidade ........................................ nenhum prefixo é válido

NEGOCIAR aceita [CADENCIA] porque a régua de recuperação de no-show cria
tarefas `[CADENCIA] NS1/NS2/NS3` sem tirar a oportunidade de `NEGOCIAR`.

PASSO 4 — Concluir as tarefas fora de lugar
Liste as tarefas ABERTAS (não concluídas) do contato. Para cada uma:
- Se o título começa exatamente com o prefixo válido da etapa atual: NÃO TOQUE.
- Caso contrário (prefixo de outra etapa, ou sem prefixo, ou a etapa não admite
  prefixo): marque a tarefa como CONCLUÍDA.
A comparação é no início do título, sensível ao texto entre colchetes e
insensível a maiúsculas. Tarefa já concluída é ignorada.

Se não houver ferramenta de concluir tarefa nas suas ferramentas disponíveis:
NÃO tente contornar por outro caminho e NÃO remova a tag. Liste no resumo, por
contato, quais tarefas deveriam ser concluídas, e diga na primeira linha:
"Modo relatório — sem ferramenta de conclusão; nenhuma tarefa foi alterada."

PASSO 5 — Remover a tag
Só depois de processar todas as tarefas do contato SEM ERRO, remova dele a tag
"limpar-tarefas". Se qualquer tarefa falhou, MANTENHA a tag: o contato volta na
próxima hora. Nunca remova a tag para "limpar o resumo".

PASSO 6 — Resumo
Devolva exatamente nesta forma:

  Contatos na fila: N
  Contatos processados: N
  Tarefas concluídas: N
  Tarefas preservadas: N
  Tags removidas: N
  Contatos mantidos na fila (erro): N
  Contatos ambíguos (oportunidade duplicada): N

  Detalhe por contato (só os que tiveram tarefa concluída ou erro):
  | Contato | Etapa | Prefixo válido | Concluídas | Preservadas | Erro |

  Erros (se houver): mensagem da API por contato.

Se um contato tiver mais de 20 tarefas abertas, conclua as fora de lugar
normalmente e sinalize no resumo: pode indicar cadência em loop.

Se o total de tarefas concluídas nesta execução passar de 300, PARE, não remova
mais nenhuma tag e responda com o alerta: "Volume anormal — parei por
segurança, revisar antes de rodar de novo." Volume assim quase sempre é
workflow em loop, e concluir tudo apagaria o rastro do problema.

Se você não conseguir se conectar à subconta, responda apenas "Sem conexão com
a subconta" e encerre. Não tente caminho alternativo.
```

---

## Por que a rotina é assim

**Por que concluir e não excluir.** Tarefa concluída fica no histórico do
contato e no relatório de produtividade do SDR. Tarefa excluída desaparece — e
com ela a evidência de que a cadência gerou trabalho que ninguém fez. O número
que interessa ao gestor (tentativas geradas x tentativas classificadas) morre
junto.

**Por que a tag só sai no fim.** Se a tag saísse antes, um erro de API no meio
deixaria tarefas órfãs sem nada apontando para elas. Mantendo a tag, o pior
caso é a rotina repetir o trabalho na hora seguinte — que é idempotente.

**Por que o teto de 300.** Uma cadência mal montada pode gerar centenas de
tarefas por hora. O teto transforma um incidente silencioso (a rotina
"limpando" para sempre) em um alarme.

**Por que a etapa manda, e não a tarefa.** O prefixo é derivado da etapa da
oportunidade porque a etapa é o estado verdadeiro do lead — é ela que os
portões da cadência consultam. A tarefa é só um lembrete; quando os dois
divergem, a etapa está certa.

**Por que o status entra na conta, não só a etapa.** No pipeline real (5
etapas, `FUNIL DE VENDAS`), sair da cadência quase nunca move a oportunidade
de etapa — "12 tentativas esgotadas", "número errado" e "não ligar" mudam só
o `status` (`abandoned`/`lost`), e a oportunidade continua parada em
`CONECTAR` (`build-wesales.md`, seção 1.0). Um lead assim tem etapa
`CONECTAR`, igual a quem ainda está na régua — só o `status` diferencia os
dois. Sem checar o `status`, a rotina trataria as tarefas `[CADENCIA]` de
quem já saiu como válidas para sempre, e elas nunca seriam concluídas.

## Como agendar

Rotina horária, dias úteis, das 08:00 às 19:00 (fora desse intervalo não há
tarefa nascendo e não há SDR trabalhando). Fuso da subconta.

Primeira semana: rode com a fila pequena e leia o resumo todo dia. O que você
está procurando é "Tarefas concluídas" alto de forma consistente — isso não é
sinal de rotina eficiente, é sinal de SDR não classificando as tentativas.

---

## O agendador existe, e eu tinha olhado no lugar errado — corrigido em 23/09/2026 03:20

**Retrato do que eu escrevi abaixo: estava errado, e o erro foi de método.** Eu
afirmei que "nenhum workflow do Actions usa `GHL_TOKEN`" apoiado em
`git grep -ln 'GHL_TOKEN' .github/`. O grep é verdadeiro e a conclusão é falsa: o
grep vê **só a branch em que eu estou**, e o workflow vive em outra. Ele existe:

| | |
|---|---|
| arquivo | `.github/workflows/faxina-tarefas.yml` |
| nome | `Faxina de Tarefas — CRM WeSales` |
| criado | 23/09/2026 00:12 BRT, `state: active` |
| execuções | 2, as duas `workflow_dispatch`, as duas `success` (03:12 UTC) |

**A regra que fica:** workflow agendado roda a partir da branch em que o arquivo
está, não da branch em que você está trabalhando — então `git grep` na branch
local **não responde** "existe workflow do Actions para isto?". A fonte é a API
do Actions (`list_workflows`). É o mesmo erro do F-17 com uma roupa nova: eu
confirmei fora do dump e não confirmei fora da **branch**.

### Mas o agendamento não é o que este documento especifica

O arquivo tem **dois** `cron`, e em GitHub Actions eles **somam**:

```
schedule:
  - cron: "*/10 11-22 * * 1-5"    # a cada 10 min, 11h-22h UTC, seg-sex
  - cron: "0 * * * *"             # de hora em hora, TODOS os dias
```

| | Documentado acima | No ar |
|---|---|---|
| dia útil, janela 08–19 BRT (11–22 UTC) | 12 execuções (horária) | **84** |
| sábado e domingo | **0** ("não há tarefa nascendo e não há SDR trabalhando") | **24 por dia** |
| madrugada | 0 | 1 por hora |

São **7× a cadência documentada** dentro da janela, mais 24 execuções por dia
fora dela, onde este documento diz explicitamente zero. Não é erro de código: é o
`cron` dizendo uma coisa e o documento outra, e alguém vai acreditar no documento.

**Por que a diferença importa, e não é só custo de minuto de Actions:** a proteção
contra corrida com o workflow do GHL é a **carência de 5 minutos** (tarefa criada
há menos de 5 min não é tocada). Com execução de hora em hora, 5 minutos de
carência é folga enorme. Com execução a cada 10 minutos, a carência cobre metade
do intervalo — a margem some. O teto de 200 por execução e a trava de "mais da
metade das tarefas abertas" continuam valendo, então o risco não é destruição; é a
margem de segurança ter encolhido sem ninguém decidir isso.

**Decisão, e é sua:** ou o `cron` passa a valer (`0 11-22 * * 1-5`, horária na
janela, e some o `0 * * * *`), ou este documento passa a descrever a cadência de 10
minutos e a carência de 5 minutos é revista para caber nela. As duas são válidas —
ter as duas escritas diferente não é.

**Um detalhe frágil no mesmo arquivo:** o `checkout` está pinado em
`ref: claude/amazing-johnson-mclksg`, a branch deste PR. Quando o PR for mesclado e
a branch apagada, o workflow quebra no primeiro `checkout` — e ele roda sozinho, de
madrugada, sem ninguém olhando. Trocar por `main` (ou pela branch padrão) no mesmo
movimento em que o PR entrar.

### O que eu havia escrito antes, e o que dele sobrevive

Depois do `0aebc38` (integração privada "Faxina de Tarefas" criada com 4 escopos,
token guardado no segredo `GHL_TOKEN`), a Faxina tem **duas** encarnações e
nenhuma das duas está agendada de fato:

| Caminho | O que é | Estado |
|---|---|---|
| o prompt acima | rotina horária de agente, dias úteis 08:00–19:00, fuso da subconta | é a forma descrita neste documento; depende de alguém colar o prompt numa rotina |
| `wesales/tools/faxina_tarefas.py` | script Python, lê `GHL_TOKEN` do ambiente, validado com token real no `0aebc38` | ~~nada o chama~~ — **errado, ver a seção acima**: o `faxina-tarefas.yml` existe e já rodou. O que falta é acertar a cadência |

~~Conferido com `git grep -ln 'GHL_TOKEN' .github/`~~ — **essa conferência não
serve**, e é o erro corrigido na seção acima: o grep vê só a branch local, e o
workflow vive em outra. O segredo tem consumidor e o script tem gatilho. O que
sobrevive desta seção é só a distinção entre os dois caminhos, abaixo — e a
escolha já foi feita por ação: é o Actions.

**Duas saídas, e elas não se misturam:**

1. **Actions**, se a Faxina é para rodar sozinha: um `.github/workflows/` com
   `schedule` (hora em hora nos dias úteis, convertendo para UTC) chamando
   `python wesales/tools/faxina_tarefas.py` com `GHL_TOKEN: ${{ secrets.GHL_TOKEN }}`.
   É o caminho que o segredo já pressupõe.
2. **Rotina de agente**, se é para continuar como está descrito acima: aí o
   `GHL_TOKEN` não serve, porque sessão na nuvem não tem a API interna nem o
   segredo — a rotina faz o trabalho pelo MCP, e o script fica como ferramenta
   de PC.

Escolher uma. Ter as duas meio-feitas é o formato em que ninguém percebe que a
faxina não rodou.

### Nota de segurança: o PIT antigo pode ser revogado sem quebrar nada aqui

Fica registrado junto porque saiu da mesma varredura. O Private Integration
Token que apareceu no histórico de chat de uma sessão anterior está com a
rotação **recomendada e nunca confirmada**. Varri o repositório:

- `wesales/tools/ghl_api.py` usa o **bearer da API interna**
  (`wesales/.local/_ghl_bearer.txt`, renovado por sessão de navegador), não PIT.
- `faxina_tarefas.py` usa o `GHL_TOKEN` **novo**, da integração do `0aebc38`.
- `conectar.md` descreve o caminho por PIT como receita manual, com
  `${WESALES_PIT}` — variável, não valor.
- `git grep` por `pit-[0-9a-f]{8}-` e por JWT em `wesales/` volta **vazio**:
  nenhum token versionado.

Ou seja: **nenhum consumidor automatizado do PIT antigo dentro deste
repositório** — revogar não quebra nada daqui. O limite honesto é esse "daqui":
se aquele PIT foi colado em algo fora do repositório (Zapier, Make, n8n, um
serviço próprio), revogar quebra aquilo, e isso eu não tenho como ver. Se não
foi, é um clique sem risco em Settings → Private Integrations.

Conferido também que o `criar_pit.js` não vaza o token novo: ele escreve só em
`stdout` (para ser canalizado ao `gh secret set`) e os prints vão para
`wesales/.local/`, que está no `.gitignore` (linha 18). Nenhum `pit-*.png`
rastreado no git.
