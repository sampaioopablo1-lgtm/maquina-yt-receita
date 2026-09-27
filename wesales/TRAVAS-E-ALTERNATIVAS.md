# Travas e alternativas — o que estudei e o que realmente destrava

Pedido do dono em 27/09/2026: *"Outras travas, estude no github, comunidades, sites,
artigos, soluções inteligentes pra encontrarmos as soluções. Sempre que encontrar um
problema, pesquise alternativas pra resolver."*

Este arquivo é o resultado, e ele **corrige uma afirmação minha**: eu disse que criar
pasta de campo era só tela. Não é.

## Como pesquisar daqui, dado que os domínios do GHL são bloqueados

Medido em 27/09: `curl` e `WebFetch` para `help.gohighlevel.com`,
`marketplace.gohighlevel.com`, `highlevel.stoplight.io`, `ideas.gohighlevel.com`,
`backend.` e `services.leadconnectorhq.com` → todos negados pelo proxy de egresso.

O que **funciona**, e vale como método permanente:

| caminho | serve para |
|---|---|
| **`WebSearch`** | roda fora do contêiner. Dá para pesquisar a documentação e ler o resumo, não a página inteira |
| **clonar `GoHighLevel/highlevel-api-docs` do GitHub** | é o **spec OpenAPI oficial**, versionado. `raw.githubusercontent.com` e o proxy de git respondem. Isto é fonte primária, não fórum |
| **os 36 dumps de workflow no próprio repositório** | condições exatas dos portões, offline |
| **o conector MCP `GHL CRM`** | roda fora do contêiner, então alcança a API pública mesmo com o proxy negando |
| **GitHub Actions** | runner com internet aberta. É onde mora o segredo `GHL_PIT` e onde 6 Actions deste projeto já falam com a API pública |

A lição que eu levo: **quando um host é negado, a pergunta não é "como furo o proxy",
é "onde mais esse dado vive"**. Duas vezes hoje a resposta foi "no GitHub".

## Trava 1 — editar workflow

Quatro rotas avaliadas, com o que cada uma respondeu.

### (a) API pública v2 — NÃO, e agora é fato, não suposição

Clonei o spec oficial e listei as rotas de workflow:

```
apps/workflows.json        → /workflows/   GET
apps/v3/workflows-v3.json  → /workflows/   GET
```

**Só `GET`.** Nenhum POST, PUT, PATCH ou DELETE. Não é limitação de escopo do token
nem de plano: o endpoint de escrita **não existe**. Isso está entre os pedidos mais
votados no portal de ideias do GHL ("REST API — Workflow POST/PUT Endpoint", "API to
create Workflows").

Então o uso da API interna neste projeto nunca foi preguiça: é o único caminho.

### (b) Snapshots — NÃO

Snapshot carrega workflow e pode ser empurrado para subconta, o que soaria como rota
oficial. Mas o spec só tem:

```
GET  /snapshots/
POST /snapshots/share/link
GET  /snapshots/snapshot-status/{snapshotId}
GET  /snapshots/snapshot-status/{snapshotId}/location/{locationId}
```

Criar, atualizar e **empurrar** snapshot não têm endpoint. Sobra consultar e gerar
link de compartilhamento. Não resolve.

### (c) API interna — SIM, com duas condições que não são minhas

Existe, é o que o projeto sempre usou, e agora tem cliente sem dependência externa
(`wesales/tools/ghl_interno.py`). Falta: o host `backend.leadconnectorhq.com`
liberado na política de rede **ou** a Action `wesales-interno.yml` com o segredo
`GHL_STORAGE_STATE`. As duas são configuração do dono, uma vez.

### (d) ATUADOR EXTERNO — SIM, e está disponível AGORA

Esta é a alternativa que a pesquisa rendeu, e ela dispensa tudo acima.

Os dois defeitos de workflow que eu achei não precisam de edição de workflow para
serem resolvidos, porque **os dois são tags** — e o conector já escreve tag:

| defeito | o que o workflow faz | alternativa sem editar workflow |
|---|---|---|
| `fila-wa` é lida mas nenhum workflow a aplica (§9) | 3 workflows leem num portão | **eu aplico a tag** em quem atende o critério da fila de WhatsApp (`Permissão WhatsApp` = `Sim`, em `CONECTAR`, sem DND). A lista 8.3 passa a encher |
| `sdr-lotado` é lida por 4 workflows e ninguém a aplica (§8) | 4 portões consultam; o freio nunca fecha | **eu aplico e removo a tag** contando tarefa vencida. O freio de capacidade passa a existir, do lado de fora |

O ponto que faz isso funcionar: **o workflow só precisa LER a tag. Nada diz que quem
escreve tem de ser um workflow.** Os portões foram desenhados para consultar estado
de contato, e estado de contato é exatamente o que a API pública escreve.

É a mesma doutrina que o `economia-de-token` (skill) já registrava para outra coisa —
*"Action empurra, Claude puxa"* — aplicada a atuador em vez de alarme.

**Limites honestos do atuador externo**, para não vender como equivalente:

- **Latência.** O workflow reagiria no instante; o atuador reage na frequência com que
  roda. Para o freio de capacidade (que compara com 50 tarefas vencidas) isso é
  irrelevante. Para algo que precise reagir em segundos, não serve.
- **Não substitui nó de mensagem.** Se o defeito fosse "falta mandar uma mensagem",
  atuador externo não resolveria sem virar disparo por fora, o que quebra o
  `Template usado` e o histórico. Aqui os dois defeitos são de **tag**, e é por isso
  que a alternativa serve.
- **Precisa de `[x]`.** Aplicar tag nova é escrita no CRM; entra na fila de módulos e
  na trilha de auditoria.

## Trava 2 — pastas de campo: eu estava errado, a API pública faz

Eu disse, mais de uma vez, que criar pasta de campo e reagrupar os 53 campos era
trabalho de tela. **O spec oficial mostra o contrário:**

```
POST   /custom-fields/           Create Custom Field
POST   /custom-fields/folder     Create Custom Field Folder
PUT    /custom-fields/folder/{id}  Update Custom Field Folder Name
PUT    /custom-fields/{id}       Update Custom Field By Id
GET    /custom-fields/{id}       Get Custom Field / Folder By Id
```

Ou seja: criar as quatro pastas da §4 do `USABILIDADE.md` (`1 · SDR PREENCHE`,
`2 · NÃO MEXER`, `3 · CLOSER PREENCHE`, `4 · VEIO DO ANÚNCIO`) e mover cada campo
(alterando o `parentId` por `PUT /custom-fields/{id}`) **é chamada de API pública**.

E a rota para executar já existe neste projeto: **seis Actions** já usam
`secrets.GHL_PIT` contra `https://services.leadconnectorhq.com`
(`wesales-vigia`, `wesales-valores`, `wesales-prioridade`, `wesales-g03`,
`wesales-picklist`, `wesales-overdue-report`), e o comentário do `wesales-picklist.yml`
registra o motivo: *"o GitHub tem rede e o secret GHL_PIT"*.

Então o maior item de usabilidade que eu havia parado — **53 de 56 campos numa pasta
só**, que é a origem do "meio completo e confuso" do dono — sai por Action com o
segredo que já existe. Sem tela, sem sessão logada, sem liberar host novo.

**Ressalvas antes de executar**, porque escrita em definição de campo é mais
arriscada que escrita em contato:

- `DELETE /custom-fields/{id}` existe no mesmo grupo. A regra 1 do projeto proíbe
  excluir campo, e o script não pode ter esse verbo no código — não é questão de
  "não chamar", é de não existir o caminho.
- Mover campo altera a **tela de todo mundo**. Faz-se em lote pequeno, conferindo
  depois de cada lote, e com o mapa campo→pasta versionado antes.
- O `PUT` de campo pode exigir o corpo completo do campo. Ler antes, mandar o objeto
  inteiro com o `parentId` novo, reler para confirmar — e não supor que `PUT` é merge.

Outras rotas úteis que apareceram na mesma leitura e que eu não sabia existirem:

| rota | para quê |
|---|---|
| `POST /locations/{id}/recurring-tasks` | tarefa recorrente por API — trabalho na frente do SDR sem workflow |
| `POST /locations/{id}/tasks/search` | busca de tarefa com filtro — é o que mede "tarefa vencida" para o freio da §8 |
| `POST /locations/{id}/tags` | criar tag por API |
| `PUT /locations/{id}` | configuração da subconta |

## Trava 3 — ler documentação oficial

Resolvida: `git clone --depth 1 https://github.com/GoHighLevel/highlevel-api-docs`.
Fica em `/home/user/gohighlevel/highlevel-api-docs`, é leitura anônima pelo proxy de
git, e contém `apps/*.json` com o spec de cada área. Conferido: commit
`0af86a4`, remote confirmado.

Isto vale mais que qualquer fórum: quando a pergunta é "a API faz X?", a resposta está
no spec, e é binária.

## A regra que fica

Quando aparecer trava, antes de declarar "é trabalho de tela", percorrer nesta ordem:

1. **O spec oficial no GitHub diz que existe endpoint?** Se sim, o resto é caminho de
   execução, não impossibilidade.
2. **Existe rota de execução que já funciona?** Neste projeto: conector MCP (fora do
   contêiner) e GitHub Actions (com `GHL_PIT`). Só depois pensar em host liberado ou
   sessão logada.
3. **O defeito precisa mesmo do componente que está travado?** O caso do `fila-wa`
   mostra que não: o portão lê estado de contato, e estado de contato é escrevível.
4. **Se nada disso servir**, então é tela — e aí a especificação fica escrita com o
   clique exato, como o `patch_janela_abertura.py` faz no docstring.
