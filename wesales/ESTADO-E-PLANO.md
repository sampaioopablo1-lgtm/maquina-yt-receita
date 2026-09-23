# Estado do sistema e plano de continuidade — leitura de 22/09/2026, 19:55 UTC

Leitura completa pedida pelo dono antes de implementar qualquer coisa:
documentos, API ao vivo e workflows. **Tudo abaixo foi medido nesta rodada**,
não herdado de rodada anterior. Onde não deu para medir, está dito.

> **Nota de 23/09/2026, corrigida na mesma data:** este documento é uma
> fotografia datada (números de pipeline/campos/etapa mudaram desde então —
> a fonte viva é a leitura por API que cada rodada do
> `ROADMAP-SALES-ENGAGEMENT.md` faz, não este arquivo). Esta nota dizia que
> "a única linha ainda ativa é a pendência 0" — estava errada, sem ter
> conferido as outras linhas antes de afirmar isso: 9e e 11a/11b também
> seguiam ativas na seção 8 na hora em que isto foi escrito. As três já
> viraram item de roadmap — pendência 0 → G-16, 9e → G-17, 11a/11b → G-19 —
> pela mesma razão de sempre: nenhuma rodada de coerência (G-10/G-13/G-14)
> tinha cruzado este arquivo linha por linha até essas promoções
> acontecerem. **O que esta correção não afirma:** que as demais linhas da
> seção 8 (1, 2, 4, 5, 6, 8, 9c, 10, 12) estão todas cobertas em outro
> lugar — isso não foi reconferido nesta rodada; cada uma continua valendo
> como está escrita ali até alguém confirmar o contrário.

## 1. A subconta

| | |
|---|---|
| Nome / id | Pablo Santos's Account · `1D53YTI9C7oIMBavcQxV` |
| País / locale / moeda | **`BR`** · `pt_BR` · `BRL` |
| Cidade / fuso | São José dos Campos–SP · `America/Sao_Paulo` |
| Telefone da conta | `+5512982381407` |
| Plano | `saasMode: activated`, assinatura **`trialing`** |
| Campos personalizados de contato | **55** |
| Pipeline | 1 — `FUNIL DE VENDAS`, 5 etapas (NOVO LEAD → CONECTAR → AGENDAR → NEGOCIAR → FORMALIZAR) |

## 2. A base, medida

| Medida | Número |
|---|---|
| Contatos | **50** |
| Oportunidades | **50** (1:1 com contato — a Porta de Entrada funciona) |
| Leads reais do Facebook | 39 |
| Contatos de teste/estrutura do projeto | 6 |
| Contatos sem `source` (chegaram por Instagram) | 5 |
| Com telefone | 41 (**9 sem**) |
| Com e-mail | 39 |
| **Sem dono (`assignedTo` vazio)** | **44 de 50** |
| **Sem nenhuma tag** | **33 de 50** |
| `country` = `US` e `timezone` = vazio | **50 de 50** |
| Telefone ou e-mail duplicado | nenhum |

### Oportunidades por etapa e status

| Etapa | Status | Quantas |
|---|---|---|
| NOVO LEAD | `open` | **45** |
| CONECTAR | `lost` | 2 |
| NEGOCIAR | `open` | 2 |
| NEGOCIAR | `lost` | 1 |

Idade na etapa: **37 oportunidades com 3 a 4 dias** paradas, 9 com 2 a 3 dias.
A mais antiga tem 3,7 dias. `monetaryValue` = 5000 em todas as 50 (valor
padrão do workflow de entrada, não estimativa real). `lostReasonId` = vazio
nas 50 — confirma o F-12.

### Entrada por dia

| Dia | Contatos novos |
|---|---|
| 18/09 | 6 |
| 19/09 | 37 (backfill da carga inicial) |
| 20/09 | 6 |
| 21/09 | 1 |
| 22/09 | **0** |

### Preenchimento de campos

As três respostas do formulário do Meta chegam: `Urgência` 40, `Necessidade`
34, `Investimento mensal em anúncios` 32. **Todo o resto da régua de
qualificação (`Decisor`, `Budget`, `Prazo`, `Tem time comercial`) aparece em
3 contatos — e os 3 são de teste.** Nenhum lead real foi qualificado ainda,
porque nenhum foi trabalhado ainda.

## 3. O diagnóstico, em uma frase

**A máquina está construída e a esteira não está ligada.** 20 workflows
publicados, 55 campos, 21 tags, pipeline montado — e 45 leads pagos parados
em `NOVO LEAD`, sem dono, sem tag de fila, há até 3,7 dias. O que falta não é
mais automação: é o passo que coloca o lead na esteira.

Isso é exatamente o **L-07 / G-03**, aberto desde o primeiro dia do projeto:
não existe gatilho que promova `NOVO LEAD` → `CONECTAR`. A `Cadência 12x30`
está publicada e correta, e não roda para ninguém porque ninguém entra nela.

## 4. Canais: o que a especificação não viu

Duas descobertas desta leitura, nenhuma das duas está em nenhum documento:

**Instagram está conectado e vivo.** Página `O Próximo Cliente`
(`pageId 17841480745368398`), 5 conversas com mensagem real de DM. Os 5
contatos correspondentes têm oportunidade aberta em `NOVO LEAD`, carregam só
`limpar-tarefas` e **nenhum tem telefone**. Numa cadência 100% telefone, são
inalcançáveis por construção.

Ressalva de leitura, para não repetir erro deste projeto: as mensagens vêm com
`direction: outbound` e `from` = a conta, e uma delas é claramente pessoal
("Felicidades em seu coração prima"). **Não afirmo que são leads pedindo
preço** — afirmo que o canal existe, tem tráfego real e não está governado por
nada.

**E-mail está livre e sem uso.** 39 contatos têm e-mail; nenhuma régua usa o
canal. É o único canal que eu consigo instrumentar por API (`emails_create-template`)
e o único que **não** disputa a rampa de aquecimento do telefone (F-14).

## 5. O que eu consigo fazer daqui, medido nesta rodada

| Ação | Por API? | Prova |
|---|---|---|
| Corrigir `country` e `timezone` do contato | **Sim** | testado em `ZZ TESTE ESTRUTURA`: virou `BR` / `America/Sao_Paulo`, e as 14 tags sobreviveram |
| Atribuir dono ao contato (`assignedTo`) | **Sim** | parâmetro existe no schema |
| Gravar valor em campo personalizado | **Sim** | `body_customFields` aceita id + valor |
| Adicionar / remover tag | **Sim** | já usado no projeto |
| Mover etapa, status, dono da oportunidade | **Sim** | `opportunities_update-opportunity` |
| Criar template de e-mail | **Sim** | `emails_create-template` |
| Criar workflow, pipeline, campo, calendário, lista inteligente, dashboard | **Não** | seção 11 do `build-wesales.md`; calendário e campo existem na API oficial mas não neste conector |

**Armadilha registrada:** `body_tags` no update **sobrescreve todas as tags**
do contato. Nunca passar esse parâmetro num update que não seja de tags.

**Limitação nova, medida hoje:** `calendars_get-calendar-events` devolve 422
"Either of userId, calendarId or groupId is required" **mesmo passando
`userId`** — o conector não repassa o parâmetro. Não consigo auditar o
calendário do closer por API.

## 6. O que os 24 dumps de workflow não dizem

> **Refinado em 23/09/2026, 01:30 UTC — metade disto venceu, e a metade que
> sobrou ficou mais precisa.**
>
> Os dumps foram refeitos ao vivo em `482de1f` ("inventário ao vivo dos 24
> workflows"). Depois do refresh:
>
> | | Antes (22/09) | Agora |
> |---|---|---|
> | `status` | `draft` em todos os 22 | **`published` em 24** de 26 |
> | `triggers` | `[]` em todos | **`[]` em todos os 26, ainda** |
>
> Então a conclusão se divide em duas, e só uma continua valendo:
>
> - **"O `draft` era artefato de fotografia pré-publicação" — confirmado.** Um
>   dump refeito depois de publicar mostra `published`. Hoje dá para responder
>   "isto está no ar?" olhando o arquivo.
> - **"O dump não diz o gatilho" — continua, e agora é mais forte.** O
>   `triggers: []` sobreviveu ao refresh ao vivo nos 26 arquivos. Não é
>   defasagem: **o gatilho não entra nesta forma de exportação, ponto.** E é
>   nele que mora a correção dos monitores do F-05.
>
> A frase que fica: **`workflows-json/` responde "está publicado?" e nunca
> responde "em qual gatilho?".** Para a segunda pergunta, só a tela.
Os 24 arquivos de `workflows-json/` — incluindo `Monitor de Capacidade` e
`Qualidade da Conexão`, criados hoje — trazem **todos** `status: draft` e
`triggers: []`. É artefato do dump (fotografia do payload antes de publicar),
não estado do CRM: o `GUIA-MONTAGEM.md` lista 20 publicados com rastro lido
por API. **Nenhum arquivo deste repositório responde "isto está ligado e em
qual gatilho?"** — só a tela responde.

## 7. Plano de continuidade, em etapas

Ordem por alavanca, não por facilidade. As etapas 1 a 3 são de escrita em
dados reais e **esperam confirmação do dono** (regra 2 do briefing).

### Etapa A — ligar a esteira (a que vale mais)
Promover os leads reais de `NOVO LEAD` → `CONECTAR` com dono atribuído, em
lotes. É o que faz os 20 workflows publicados começarem a rodar.
**Decisão necessária:** tamanho do lote. Ver a conta da rampa F-14 — 6/dia
devolve a curva segura, 10-13/dia estoura o teto da semana 1 no dia 2.

### Etapa B — consertar o país e o fuso dos 49 contatos restantes — **rebaixada**, era o item que eu tinha vendido como o mais fácil de aprovar

~~`country: US` + `timezone: vazio` em base 100% brasileira afeta janela de
horário de workflow, validação de número (W19) e qualquer nó que use fuso do
contato.~~

**Corrigido em 22/09/2026, 21:25 UTC — eu superestimei esta etapa, e a medição
que me refuta já estava no projeto.** A Tabela L do `CONFERENCIA-CAMPOS.md`
tinha fechado os dois lados antes de eu escrever isto:

| O que eu afirmei | O que a Tabela L já tinha medido |
|---|---|
| "afeta janela de horário de workflow" | **Não afeta.** A decisão D-02 e a seção 2.4 mandam usar fuso **da subconta**, com a justificativa explícita "não use fuso do contato: o SDR trabalha no fuso dele". Nenhum nó lê fuso do contato, então o `null` não quebra nada |
| "afeta validação de número (W19)" | A Tabela L registrou isso como **conferência acoplada ao R-13, não afirmação** — e o W19 saiu **por decisão do dono** (`c945077`), então não há o que destravar |

**O que sobra, honestamente:** higiene de dado. Uma base brasileira marcada
como americana está errada, e a própria Tabela L aponta o risco real — se
algum workflow futuro escolher "fuso do contato" num `Wait` ou numa janela de
envio, cai em fallback silencioso. Isso é **prevenção**, não conserto: barato,
reversível e **sem urgência nenhuma**. Não deve ser a primeira coisa a
aprovar, e eu a apresentei como se fosse.

O erro de método foi o ponto 12 do meu próprio checklist: a conclusão existia
num documento (Tabela L), eu citei essa mesma tabela para outra coisa na mesma
rodada, e não carreguei a conclusão dela para dentro da minha proposta.

### Etapa C — enriquecer `Empresa`
O campo está vazio em 100% da base (Tabela J). Muitos nomes de lead do Meta
carregam o nome do negócio (`Zenilson Fonseca, Serviços E Instalações`,
`Ana Ruth / Especialista em Cabelos`, `TINTIM | Rastreie suas conversas`).
Dá para extrair e gravar por API, com revisão do dono numa lista antes.

### Etapa D — rota para os 9 sem telefone — **agora com o número que faltava**
Numa operação 100% telefone eles são inalcançáveis. Medido em 22/09, 21:25:
dos 9 sem telefone, **1 tem e-mail** (e é lead de teste do Meta) e **8 não
têm**; os 5 leads reais do Instagram não têm telefone **nem** e-mail. Então
"campanha de e-mail" **não é rota para este público** — o único canal que os
alcança é o **DM do Instagram**. Isso derruba a premissa do F-15; correção
completa na seção 2.30 do `build-wesales.md`.

### Etapa E — canal de e-mail (não disputa a rampa do telefone)
Criar templates por API a partir da `biblioteca-mensagens.md`, com sequência
própria. É o único canal que consigo instrumentar daqui de ponta a ponta e o
único que não consome o teto de ligações/dia do F-14.

### Etapa F — governar o Instagram
Definir o que acontece com DM: quem responde, em quanto tempo, e como o lead
entra no funil. Hoje não há regra nenhuma.

## 8. Pendências do dono que travam outras coisas

| # | Pendência | O que destrava |
|---|---|---|
| 1 | **Aviso de gravação (LGPD)** antes de ligar gravação por número | a transcrição já está ligada na subconta; o clique da gravação não passa pelo W20 |
| 2 | Formato de `Entrada em` / `1ª tentativa em` — hora ou a string `sim`? | se for `sim`, o R-02 speed-to-lead não mede nada |
| 3 | Lote do G-03 contra a rampa do F-14 | Etapa A acima |
| 4 | Entrada de leads parada (Gerenciador de Anúncios) | a esteira sem alimentação |
| 5 | Marcar as 6 tags e os 4 campos no `APROVADO.md` | coerência do freio de mão |
| 6 | Pré-requisito 6 do W20 (`Conexão real = vazio` antes de cada tentativa) | sem ele, um `Sim` antigo sobrevive às tentativas seguintes |
| ~~6b~~ | ~~Conferir na tela se o gatilho do `Espelho de Etapa` etiqueta o acervo~~ — **FECHADA por medição em 23/09 02:35**, não precisou de tela | etiqueta o acervo inteiro: das **53 oportunidades `open`, 53 têm a tag de etapa certa**, 0 sem tag, 0 divergente — inclusive as criadas em 20 e 21/09, antes da publicação. As condições dos 11 workflows têm dado |
| ~~7~~ | ~~`conectado-hoje` sem removedor~~ — **RESOLVIDO pelo dono em 23/09, e melhor do que eu tinha recomendado.** Removedor em workflow à parte (`tag adicionada → espera 1 dia → remove`, `allowMultiple`) em vez de dentro do `Pós-ligação v2`; conferi por medição que a tag saiu no teste. E ele achou a saída que eu não tinha visto: **`Fila Telefone Hoje = fila-tel + etapa-conectar`, sem `conectado-hoje` na lista**, porque a 12x30 põe e tira `fila-tel` a cada toque. Falta só publicar a versão real (espera de 1 dia, não os 2 min da cópia ZZ) e tirar a ZZ antes |
| 8 | **Confirmar com um comando no seu PC:** `python patch_remove_parte2.py` **sem** `--aplicar` (não escreve nada, só lista) | o assunto do `23db864` diz "parte 2 nas remoções", então provavelmente já está feito — o que falta é confirmar quantos nós o script pegou, porque ele varre só os publicados. Se algum ficou para trás, o lead que agenda continua recebendo toque automático da segunda metade da régua. O dump não responde isso (seção 2.31.3) |
| ~~0~~ | ~~Uma pergunta, não uma limpeza: `Francisca` (+5512981913254) é você testando ou é gente?~~ — **respondida em 23/09/2026 por outra sessão, que promoveu a pergunta a item de roadmap (`ROADMAP-SALES-ENGAGEMENT.md`, G-16), e FECHADA por inteiro na mesma data.** `conversations_get-messages` no fio inteiro confirma: é pessoa real, conversa pessoal (PIX, carona, áudio), sem sinal comercial. O dono autorizou ao vivo em chat (~11:35 BRT, "sim"); duas sessões executaram em sequência (17:06 UTC tags `etapa-novo-lead`/`cad-inbound` removidas e `nao-perturbe` aplicada de proteção antes; 17:08 UTC oportunidade `gwDvzf9FeRDv2LfOVbH9` movida para `abandoned`) — detalhe completo no próprio G-16. | resolvido: o contato não é mais elegível a nenhum toque da Cadência Inbound |
| ~~11~~ | ~~Escolher como a Faxina roda~~ — **FECHADA por ação: é o Actions.** O `faxina-tarefas.yml` existe e já rodou 2× com sucesso. Eu havia dito que nenhum workflow o chamava; era `git grep` numa branch só, e o arquivo vive em outra — corrigido |
| 11a | ~~**Acertar a cadência da Faxina**~~ — **promovido a item de roadmap em 23/09/2026: `ROADMAP-SALES-ENGAGEMENT.md`, G-19.** o `cron` diz `*/10 11-22 * * 1-5` **mais** `0 * * * *`, e os dois somam: **84 execuções por dia útil** (documentado: 12) e **24 por dia no fim de semana** (documentado: 0) | a carência de 5 min contra corrida com o workflow do GHL foi desenhada para cadência horária; com 10 min ela cobre metade do intervalo. O teto de 200 e a trava da metade seguem valendo, então não é destruição — é margem que encolheu sem ninguém decidir. Ou o `cron` vira `0 11-22 * * 1-5`, ou o documento passa a descrever 10 min e a carência é revista |
| 11b | ~~**Despinar o `checkout` do `faxina-tarefas.yml`**~~ — **mesma promoção, G-19** — está em `ref: claude/amazing-johnson-mclksg` | quando este PR for mesclado e a branch apagada, o workflow quebra no primeiro `checkout`, rodando sozinho de madrugada sem ninguém olhando. Trocar pela branch padrão no mesmo movimento do merge |
| 12 | **Revogar o PIT antigo** (o que apareceu no histórico de chat) — Settings → Private Integrations | varri o repositório: nenhum consumidor automatizado dele aqui (o `ghl_api.py` usa o bearer interno, a Faxina usa o `GHL_TOKEN` novo, o `conectar.md` só documenta a receita). Revogar não quebra nada **deste repositório**. O limite é esse: se ele foi colado em algo fora (Zapier, Make, n8n), revogar quebra aquilo, e isso eu não vejo |
| ~~9a/9b~~ | ~~Publicar a `Triagem da Nutrição`~~ e ~~dois `Remove Tag`~~ — **FECHADAS pelo dono, e 3 das 5 já estavam fechadas quando eu as reportei.** A `Triagem da Nutrição` foi publicada às 03:24 e o `Mestre de saída v2` passou a limpar `fechar-horario` e `cadencia-12x30-p2`. Eu reportei os 5 achados às 04:35 e 04:55 lendo um dump de **22/09 16:27** — detalhe e conserto da ferramenta na §2.33.3 |
| ~~9d~~ | ~~Duas linhas no `patch_condicoes_etapa.py`~~ — **MEDIDA em 23/09/2026, e a pendência estava superestimada.** Os 10 alvos já estavam consertados (28 segmentos, 49 condições, 0 falhas, contra os backups pré-patch); o defeito real não era o passado, era a falta de guarda para workflow futuro. `auditoria_condicoes.py` (nova, somente leitura) cobre isso agora; `ALVOS` virou varredura ao vivo (`--incluir-teste`, `--alvo NOME`), tabela de tradução de 3 para 8 padrões | `build-wesales.md` §2.36 |
| 9c | **Decisão, não lacuna: `Canal que conectou` é manual ou automático?** O `GUIA-SDR.md` instrui o SDR a preencher na tela, junto com `Resultado da tentativa` — minha leitura anterior ("ninguém escreve, logo nunca terá resposta") lia a D10 errado e está corrigida na §2.33.7 | manual capta o que só o humano sabe; automático não depende de disciplina. Recomendo automático **onde o ramo já sabe** (o nó que trata "atendeu no WhatsApp" pode gravar sozinho) e manual onde não sabe |
| 9e | **Cresceu de "portar 6 nós na Inbound" para uma decisão sobre três cadências — promovido a item de roadmap próprio em 23/09/2026: `ROADMAP-SALES-ENGAGEMENT.md`, G-17.** A invariante (todo toque que enfileira ou marca `toque` deve ler `pausado`/`sdr-lotado`/teto semanal) achou que `Recuperação de No-show` e `Reengajamento 90 dias` também falham — o `Reengajamento` pior que a Inbound: gasta a cota semanal sem nunca respeitá-la. Patch da Inbound pronto e validado (`patch_portao_inbound.py --dump`, `build-wesales.md` §2.37); as outras duas esperam o dono escolher, por cadência, entre portar o portão ou tirar a tag `toque` (§2.38) | `auditoria_portoes.py` mede 3 cadências publicadas em falha hoje; G-17 é a fila de decisão a partir de agora, não esta linha |
| 10 | **Decidir o `fila-wa`**: apagar a lista 8.3 e tirar os 75 nós, ou devolver fila própria ao WhatsApp | a tag é removida em 75 nós e aplicada em nenhum — a `Fila WhatsApp Hoje` nunca pode encher. Não é bug: o `PLANO-MULTICANAL.md` fez o WhatsApp virar parte do toque. O desatualizado é a lista 8.3. Recomendo apagar (seção 2.33) |

**Medição de 23/09 02:35 — a composição do `NOVO LEAD` mudou e o número que eu
vinha carregando ("39 leads reais") está desatualizado.** São **50 oportunidades
`open` em `NOVO LEAD`** (eram 45), e elas não são todas lead:

| O que é | Quantas | Quem |
|---|---|---|
| **lead pago de verdade** | **37** | `source: Facebook` |
| lead de Instagram sem `source` | 5 | `TINTIM`, `Dkw.oficial`, `Nathalia.ggss` e mais 2 — os que não têm telefone nem e-mail, alvo do agente de IA |
| **teste de ontem à noite, sem marcação** | **5** | `Sem Nome`, `O Próximo Cliente`, `Pablo Sampaio`, `Francisca`, `156766977421470` — criadas 22/09 22:34 a 23/09 00:45, durante a validação do multicanal |
| teste já marcado | 3 | `ZZ Teste Porta Inbound`, `ZZ TESTE ESTRUTURA`, `Teste Não Ligar` |

Então o lote da Etapa A é sobre **42 candidatos** (37 + 5), não 39 — e só depois de
tirar os 5 da terceira linha, que é a pendência 0 acima.

**A entrada de anúncio continua parada.** O lead mais novo com `source: Facebook`
segue sendo `Carlos Andrade`, 21/09 09:17 — mais de **41 horas**. As 6
oportunidades novas desta noite são todas de teste seu, nenhuma veio do
Gerenciador.

**Sobre as pendências 7, 8 e 9 (novas em 23/09):** as três nasceram dos commits
`1d04af2` e `23db864`, que vieram do seu PC (mudança de etapa em 5 workflows,
12x30 multicanal no ar em duas partes, `Fechar Horário` publicado). As
mudanças estão certas; o que apareceu foi o encontro delas com coisas
antigas. Medi a conta antes de escrever: `conectado-hoje` está em 2 contatos
(os dois de teste do projeto) e `fechar-horario` em 0. **Nenhum lead real
afetado** — as três são armadilha, não incêndio, e é exatamente por isso que
precisam ser resolvidas *antes* da Etapa A, não depois: o primeiro lote que
entrar em cadência é quem começa a pagar. A 8 é a única que eu não consigo verificar
daqui — e, pelo assunto do commit, é provável que já esteja resolvida; é
confirmação, não conserto.

---

## 9. O modo de operação mudou em 22/09, e nenhum documento dizia isso

Em `f0a0474` o dono autorizou publicar de forma permanente ("publique tudo você
mesmo sempre") e o W18 e o W20 foram publicados no mesmo commit. Isso muda o
projeto mais do que qualquer item de roadmap, e muda em silêncio.

**Até hoje, publicar era um passo humano.** A rotina especificava, o dono
abria a tela, olhava e publicava. Esse intervalo não era burocracia: era o
único lugar onde um erro de especificação parava antes de virar
comportamento. Todos os defeitos achados hoje — o `Mestre de saída v2`
apontando para o Clique antigo, o F-09 mandando desviar para um canal
extinto, o F-15 resgatando por um canal que o público não tem — foram
achados **em especificação**, antes de rodarem.

**A partir de agora a distância entre especificar e produzir é zero.** O que
antes era "uma rodada escreveu isso, alguém vai olhar" passou a ser "uma
rodada escreveu isso e está no ar". A consequência prática:

| Antes | Agora |
|---|---|
| erro de spec custava uma correção de documento | erro de spec custa comportamento errado em lead real |
| o checklist de conferência era desejável | o checklist de conferência é a **única** barreira |
| "publicar ficou com o dono" era o freio | não há freio automático nenhum |

Não é argumento para voltar atrás — é decisão do dono e ela acelera muito.
É argumento para **duas coisas ficarem obrigatórias**, não opcionais:

1. **Conferir antes de publicar, na própria rodada que publica.** O checklist
   de 14 pontos (`APRENDIZADOS-CRM.md`) deixou de ser revisão posterior e
   passou a ser pré-condição.
2. **Publicar só o que tem gatilho que não pode disparar sozinho, ou que já
   passou por conferência.** O W20 é o exemplo bom por acidente: está no ar e
   **não dispara**, porque depende de gravação por número que continua
   desligada. Publicar um workflow ocioso é seguro; publicar um que já tem
   gatilho vivo não é a mesma coisa.

### O caso do W20, e o encadeamento de um clique

Estado medido agora: W20 publicado, gatilho `Transcript Generated` ativo,
transcrição ligada na subconta, **gravação por número desligada**. Então hoje
nada é gravado e o W20 nunca roda. Correto e seguro.

**Um único clique — ligar gravação num número — dispara três coisas ao mesmo
tempo:**

| O que acontece | Estado |
|---|---|
| Toda ligação de saída passa a ser gravada | **aviso de LGPD ainda não escrito** (`script-de-ligacao.md`, seção 2) |
| O W20 começa a gravar `Duração da ligação` e `Conexão real` | desenho conferido: escreve nos **dois** ramos (nós 5 e 7), então não há valor velho sobrevivendo entre chamadas **com** transcrição |
| Custo do add-on começa a contar | US$ 0,024 por minuto gravado |

O pré-requisito 6 continua aberto e continua correto, com escopo menor do que
está escrito: como o W20 escreve nos dois ramos, o valor só envelhece na
tentativa que **não gera transcrição nenhuma** (não atendida, caixa postal).
Para essa, um `Sim` antigo sobrevive — é o reset que falta nas seções 2.4/2.10.

