# PLAYBOOK — o documento central da máquina

> **Este arquivo é lido no início de todo disparo da rotina, antes de qualquer produção.**
> Ele descreve como a máquina opera *hoje*. Quando o processo mudar, muda aqui — junto
> com a regra correspondente em `aprendizados` no Supabase. Documento e banco andam juntos.

Projeto Supabase: **`vevocauwtarctfwngrch`** (`maquina-yt-dark`, us-east-1) · Bucket: `videos-maquina` · Repositório: este.

> O projeto antigo (`cscczluzpblzhvojxanp`) é de um CRM imobiliário e **continua vivo** —
> as tabelas da máquina eram seis ilhas em ~150 tabelas de outro produto. Nada de vídeo
> volta a ser gravado lá. A base fica em `/tmp/.sburl`, nunca digitada: o `l` do ref é
> homóglifo de `1` em fonte de terminal, e o erro que isso produz (`Video URL is not
> allowed`, DNS sem resolução) não aponta para erro de digitação.

---

## 0. As quatro consultas de abertura

Rode antes de escolher o canal. Substituem meia dúzia de `select` espalhados.

```sql
select * from v_maquina_regras where severidade in ('critico','alto');  -- o que não repetir
select * from v_maquina_fila limit 3;                                   -- quem é o próximo
select * from v_maquina_estoque;                                        -- onde estamos
select * from v_maquina_formatos where canal = '<slug>';                -- o que performa NO NICHO
select * from v_maquina_licoes  where canal = '<slug>';                 -- o que performou NESTE CANAL
```

**A quarta e a quinta consulta não são a mesma pergunta**, e confundi-las foi o
buraco da máquina até 20/08/2026. `v_maquina_formatos` mede os *concorrentes* —
é a memória da pesquisa. `v_maquina_licoes` mede o *próprio acervo*. Onde as
duas discordam, **vale a própria**: o nicho descreve um público, o canal
descreve o seu.

`v_maquina_fila` ordena por *canal com YouTube configurado primeiro*, depois **token
vivo**, depois `ultimo_pacote_em` mais antigo. `v_maquina_formatos` é a memória da
pesquisa: mostra a mediana de views/dia por família de formato, acumulada ao longo das
semanas.

O critério de token entrou em 20/08/2026 e custou um roteiro para aparecer. A fila
entregou o `sx-educacao` como próximo da vez; escrevi 78 cenas, sete capítulos e a copy
inteira, e só então o portão do render descobriu o `refresh_token` morto. **O portão
funcionou** — abortou em 90 s em vez de gastar 20 min renderizando um pacote sem rota de
publicação. O que faltava era antes: a fila lê `canais` e `videos`, e saúde de token não
mora em nenhum dos dois.

A auditoria (`scripts/auditar_escopos.py`) já existia e já sabia responder. Faltava ela
rodar sozinha e **gravar**: agora escreve `token_vivo` e `token_testado_em` em
`config.yt_token_<slug>`, junto da coleta diária das 05:00 UTC, e a fila lê dali.

Duas coisas que a fila deliberadamente **não** faz, e que é fácil inverter por engano:

- **token morto não zera `pode_produzir`.** O pacote ainda pode ser renderizado e
  entregue no Drive esperando a reautorização — foi o que fizemos com o
  `sx-educacao-003`. Zerar transformaria *"espere o Pablo"* em *"nunca mais produza"*.
- **ausência de medida não é morte.** Canal nunca auditado entra como vivo; tratar
  desconhecido como morto pararia a frota no dia em que a auditoria falhasse, e o
  `confere_token.py` continua sendo a rede de baixo.

### `v_maquina_licoes` — o laço que faltava

Durante duas semanas a máquina publicou 152 vídeos e **nunca leu o próprio
resultado**. Havia 1.932 linhas em `metricas` e nenhuma linha do caminho de
decisão as consultava. A pergunta era barata e ninguém a fazia.

A view devolve um **veredito por canal**, e ele decide produção — não descreve:

| veredito | o que significa | o que muda no roteiro |
|---|---|---|
| `suspenso` | o short entrega, o longo não paga o render | longo no **piso** de 8 min; o melhor material vai no short |
| `canal frio` | **nenhum** dos dois pegou, e nunca houve pico | o problema é gancho/nicho, não formato — arrisque eixo novo |
| `liberado` | o longo se paga | faixa inteira de 12 a 15 min |
| `sem dado` | menos de 3 vídeos com 48h+ no formato | siga a memória do nicho |

O corte de `suspenso` sai da razão de custo: um longo custa ~20× o render de um
short (80 cenas contra 6), então ele precisa entregar ao menos 1/20 do short
para empatar em **views por minuto de runner**. E `liberado` exige piso
absoluto de 1 v/d — sem isso a razão aprovava o longo de um canal onde o short
também estava morto.

**`views` decide; `retenção` entra quando existe, e quase nunca existe.**

Esta seção afirmou o contrário e a afirmação era falsa — fica registrada porque
ela mudou decisões. Eu escrevia aqui que nenhum `refresh_token` carregava
`yt-analytics.readonly` e que retenção/CTR só voltariam com um novo
consentimento nos doze canais. A prova era `config.yt_token_*.scopes`, que
registra o que foi **pedido**, não o que foi concedido. O banco desmente: a
coleta diária escreve 629 linhas e a query de Analytics **responde** — sem
escopo ela daria 403 e o vídeo não teria linha nenhuma. Doze vídeos têm
retenção real, e ela **muda** entre coletas.

Retenção aparece em 12 de 629 porque 617 quase não são assistidos. Não há
decisão do dono pendente: há audiência faltando.

O que isso muda na prática — retenção separa dois problemas que views sozinho
confunde:

| leitura | diagnóstico |
|---|---|
| views baixo, retenção **alta** | distribuição: título e thumb não fazem clicar, o roteiro está bom |
| views baixo, retenção **baixa** | roteiro: quem entrou, saiu |
| retenção **acima de 100%** | o vídeo foi reassistido — o sinal mais forte que existe em short |

Já dá para ler algo: o `setiap-level` mede 0,11 v/d no longo **com 28,3% de
retenção** — problema de distribuição, não de roteiro. O `nivel-do-jogo` mede
0,15 v/d com **2,2%** — problema de roteiro. Os dois pareciam idênticos por
views.

Retenção viaja sempre com `ret_n`, quantos vídeos a sustentam: mediana sobre um
vídeo não pode se ler igual a mediana sobre trinta. Continuam fora `ctr` e
`impressões` (as linhas existem mas vêm zeradas), `inscritos_ganhos` e
`receita` (canal nenhum está no YPP).

`fabrica/aprendizado.py` é quem lê isso e monta o bloco que entra no prompt do
`autor.py`. O `diario.yml` imprime o painel a cada ciclo.

### A hora de publicar deixou de ser sobra de escalonamento

Até 20/08/2026 **nada** decidia a hora: o pacote subia quando o render
terminava, e o render começava quando o ciclo de 30 min calhava de pegar a spec.
O custo foi medido, em hora UTC de publicação dos shorts:

| canal | UTC | hora local |
|---|---|---|
| `seviye-seviye` (Istambul) | 00, 01, 06 | **03h, 04h**, 09h |
| `kolejny-poziom` (Varsóvia) | 00, 01 | **02h, 03h** |
| `epomeno-epipedo` (Atenas) | 03, 04, 05 | 06h, 07h, 08h |

O `seviye-seviye` é o dono do **melhor short da frota** — mediana de 81,5 v/d — e
dois terços das publicações dele caíram na madrugada de Istambul.

`fabrica/janela.py` corrige, e afirma só o que não precisa de medição: **entre
01h e 08h local o canal cai para o fim da fila**. É *preferência, nunca portão* —
se não houver mais nada pronto ele dispara igual, porque frota parada não rende.
A fila anda de meia em meia hora, então todo canal alcança a própria janela
dentro do mesmo dia.

Qual é a *melhor* hora dentro do dia continua sem resposta, e está registrado
como experimento aberto — a amostra atual mistura hora, tema e formato, então
ranquear horas agora seria inventar.

---

## 1. O gargalo, declarado

**O gargalo é 1 CPU renderizando a 22x o tempo real.** Medido em 2026-08-11, lado a
lado, com a mesma fábrica:

| máquina | CPU / RAM | s por cena | pacote de 75 cenas | × tempo real |
|---|---|---|---|---|
| sandbox Composio | 1 / 985 MB | 208 s | **4 h 20 min** | 22,7× |
| runner 4 vCPU | 4 / 16 GB | 10,3 s | **~13 min** | 1,14× |

São **20× de diferença**, e ela explica o teto de ~5 pacotes/dia melhor do que qualquer
conta de cota. A cota do YouTube é de 100 uploads/dia por projeto e usamos 10. O
`ESCALA_RENDER = 0.75` da fábrica existe só porque o `zoompan` não cabia em 1 GB — num
runner ele não é necessário. O caminho para escalar está em `.github/workflows/frota.yml`:
um job por canal, `max-parallel: 10`, spec vinda do Storage.

> **O gargalo NÃO é a cota — corrigido em 2026-08-12.** Durante sete ciclos esta
> seção afirmou que `publicacao.max_por_dia` valia 6 e travava a frota. O número
> estava errado, e a informação certa estava quatro linhas acima, no parágrafo
> anterior: a cota é de **100 uploads/dia por projeto**. O 6 vinha de dividir as
> 10.000 unidades diárias da API por 1.600, supondo que `videos.insert` saísse
> desse balde — não sai, são 100 chamadas num balde separado (aprendizados #57
> e #174).
>
> O que era verdade: o teto é **da CONTA, não do canal**. `maquina sincronizar`
> puxa a frota inteira para o SQLite do canal, e o modelo `Video` nem tem campo
> `canal`, então `publicados_hoje()` soma os treze. Prova de 12/08: o job do
> `setiap-level`, com ZERO publicados no dia, foi bloqueado porque outros quatro
> canais somavam 6.
>
> Com 100/dia a conta fica: **50 pacotes/dia de teto contra ~9 longos/dia de
> render**. A cota tem folga de 5×; o gargalo volta a ser CPU, como o
> aprendizado #139 já dizia.
>
> **Falta a guarda por canal.** O limite de 3 pacotes/dia/canal que a rotina pede
> não existe em código, e não dá para escrevê-lo sem um campo `canal` no `Video`
> e no SQLite. A trava anti-spam continua sendo necessária — automação em escala
> com variação mínima é lida como spam — mas hoje ela só existe no teto agregado.
>
> **E a vaga não vale o mesmo nos dois formatos.** Com 154 a 194 horas de vida,
> os 5 shorts do setiap-level medem mediana de **19,32 views/dia** e os 4 longos
> **0,15** — 129×. A vaga gasta com longo em canal frio rende quase nada.

O que **não** resolve: o container do Claude Code tem o hardware (4 CPU/16 GB, medido)
mas o proxy de egresso nega `speech.platform.bing.com` (edge-tts) e `supabase.co` com
403 de política — depois de anexar o CA ao certifi o erro deixou de ser de certificado e
passou a ser de política, que não se contorna. Ele só computa dado que chega por git.

**Os 12 canais publicam direto** (2026-08-11): cada um tem OAuth próprio em
`config.yt_token_<slug>`, e 7 deles já passaram pela verificação por telefone — sem ela
o `thumbnails/set` responde 403 e só a capa fica pendente, o vídeo sobe igual.

A publicação em si **deixou de ser gargalo em 2026-08-05.** Sete vídeos (4 pacotes) subiram
pela Upload-Post e sobreviveram ao nascimento, contra 6/6 apagados pela Composio.

| pacote | formato | duração | id |
|---|---|---|---|
| teste de sobrevivência | short | 0:26 | `GKQXVoA1zS0` |
| setiap-level-003 | longo | 25:44 | `G8ocnpQIiyg` |
| setiap-level-003 | short | 0:33 | `I6no74M2NDU` |
| setiap-level-004 | longo | 28:36 | `v-5v7R13BBc` |
| setiap-level-004 | short | 0:41 | `ZYh3bpLP5JE` |
| resep-naik-level-002 | longo | 14:15 | `le6IBDH7u6M` |
| resep-naik-level-002 | short | 0:42 | `IdcluUKbwJ4` |

A regra "nunca por app de terceiro" nunca disse "nenhum terceiro" — disse "nenhum
terceiro **não auditado**". A Upload-Post opera a YouTube Data API com auditoria
própria, e é essa a diferença. **A regra da Composio continua valendo.**

Duas coisas que o Playbook afirmava e o dado derrubou:

- ~~Canal não verificado não sobe vídeo acima de 15 min~~ — `G8ocnpQIiyg` tem 25:44 no
  mesmo canal não verificado. Regra 43 está `invalidado`.
- ~~Thumbnail e SRT ficam manuais no Studio~~ — `thumbnail_url` e `youtube_subtitle_file`
  são parâmetros da API.

O que continua aberto: `metricas` está vazia, então **toda decisão de pauta é cega** —
só grupo de pares, nunca retenção própria. Com os 3 vídeos no ar, `/analytics/setiaplevel`
passa a devolver dado em alguns dias e os experimentos abertos fecham.

**Limites do plano grátis da Upload-Post: 10 uploads/mês, 1 perfil.** O portfólio
inteiro não cabe nele — mas o gargalo real não é cota, é ter um canal só.

### A cota grátis é maior do que este repositório assumia

Eu vinha calculando `10.000 unidades ÷ 1.600 por upload = 6 uploads/dia`.
**Errado.** `videos.insert` tem balde próprio: **100 uploads/dia**, de graça, em
projeto próprio do Google Cloud — separado das 10.000 unidades dos outros
endpoints.

O que trava não é a cota, é a auditoria: projeto não verificado tem **todo upload
travado em privado**, e a diretriz aqui é sempre público. A auditoria é
**gratuita**, leva semanas e não é garantida. Ela pede três coisas: descrição do caso
de uso, **vídeo demonstrando o fluxo de OAuth**, e aceite dos Termos — e o vídeo é o
item que trava quem tenta. Os dois primeiros já estão escritos e prontos para colar em
`docs/18-submissao-auditoria.md`. O projeto a usar **já existe**: `Youtube RECEITA`, o
mesmo onde o Gemini roda.

Nenhum serviço grátis dá 100 uploads/dia porque o teto é do YouTube, não do
intermediário: quem vende plano está vendendo **a auditoria dele**. Postiz
auto-hospedado é grátis no software mas publica com as suas credenciais — mesma
cota, mesma exigência. Detalhes e a tabela comparativa em `docs/16-cota-de-upload.md`.

---

## 2. Pauta — a parte que decide o resultado

A ordem importa. Quem inverte produz vídeo bonito que ninguém assiste.

1. **Consulte o acervo antes de pesquisar.** `v_maquina_formatos` já pode responder.
2. **Meça o grupo de pares**: `YOUTUBE_SEARCH_YOU_TUBE` (90 dias, duração compatível) →
   `YOUTUBE_GET_VIDEO_DETAILS_BATCH` → views/dia → mediana → outlier ≥ 3× mediana.
3. **Grave tudo em `pautas_banco`**, inclusive o que mediu mal. O acervo só serve se
   registrar os mortos — é assim que se enxerga um formato morrendo.
4. **Identifique o formato morto.** Em 6 de 6 canais medidos, era o que o próprio canal
   tinha acabado de publicar. Inclusive uma vez em que a máquina só descobriu depois
   (`setiap-level-003`, template a 1,0 v/d).
5. **Pauta = (formato que performa) × (dor real datada) × (eixo ainda não usado).**
6. **Similaridade ≤ 0,65** contra os vídeos anteriores *do mesmo canal*.

### Dois limites das ferramentas de pesquisa

- **Transcrição do YouTube está bloqueada.** `youtube-transcript-api` devolve
  `RequestBlocked` do sandbox — IP de nuvem. Testado em dois sandboxes e quatro vídeos.
  Não insista: use `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, os documentos que a descrição
  linkar, e a medição do grupo de pares.
- **O filtro `channelId` do `YOUTUBE_SEARCH_YOU_TUBE` é ignorado.** Ele exige `q` e
  devolve o YouTube inteiro. Não serve para medir um canal específico — e devolve
  resultado plausível, então dá para concluir errado sem perceber.

O título modela a **estrutura** do outlier, nunca o assunto. Palavra-chave nos 5 primeiros termos.

**Número exato vence número redondo, e os centavos são a prova.** A precisão sinaliza
captura de painel real, não alegação: `R$24.540,04 em 60 DIAS` (265 mil views, 7,1% de
curtidas) e `R$18.503,07 em 10 dias` usam a mesma assinatura, e nenhum arredonda. O mesmo
padrão apareceu, sem relação nenhuma, no nicho indonésio de dívida — `58 pinjol, 120 juta,
4 bulan` a 892 v/d contra `Panduan Lengkap` genérico a **0,3 v/d**. Dois idiomas, dois
nichos, uma assinatura.

> Para nós a regra é estreita: **quando a fonte institucional der precisão, não arredonde**
> — nem na narração nem no título. E nunca invente precisão que a fonte não tem. O BPS diz
> 3,34%; é isso que se fala, não "mais de três por cento".

---

## 2d. A escrita deixou de ser humana — e o portão que isso obrigou a construir

**Ligado em 2026-08-20.** Até aqui o ciclo tinha três pernas e a primeira era manual:

```
escrever pauta  ->  renderizar (frota.yml)  ->  publicar (frota.yml)
   ^ a mão                        disparado pelo diario.yml a cada 30 min
```

Uma spec por disparo da rotina horária dá, no melhor dia, **24 pacotes para treze
canais**. A meta é 5 por canal por dia — **65**. E o teto nunca foi o que segurava a
frota: em 20/08, com `MAX_POR_DIA_POR_CANAL` já em 5, **oito dos treze canais tinham ZERO
spec pendente**. O gargalo era a escrita.

`fabrica/autor.py` escreve. `.github/workflows/autoria.yml` roda de duas em duas horas,
commita a spec em `fabrica/specs/`, e o `diario.yml` a pega no ciclo seguinte — sem
ligação direta entre os dois. **A spec no repositório continua sendo a interface**, como
já era para as escritas à mão.

### O portão de fatos é a condição, não um extra

Enquanto cada roteiro saía escrito a mão, a regra das **duas fontes que batem** era
cumprida na *pesquisa*, antes de a spec existir, e ficava registrada no cabeçalho do
`.build.py`. Um gerador quebra exatamente esse acordo: ele escreve *"quarenta e dois por
cento"* com a mesma fluência sendo verdade ou não, e **nenhum dos sete portões olha para
o mundo** — eles medem ritmo, língua, borda e duração.

E o custo do erro não é simétrico entre os canais. `labtreinamento` fala de norma
regulatória com prazo, `sx-educacao` e `next-level-money` de dinheiro, `seja-mais-magra`
de saúde. Número errado ali **não é vídeo ruim, é dano**.

Então `fabrica/fatos.py`, e a divisão de trabalho que ele faz:

| etapa | quando | custo | o que faz |
|---|---|---|---|
| `verificar` | uma vez, quando a spec nasce | modelo + busca na web, minutos, dólares | classifica cada afirmação em `confirmado` / `refutado` / `sem_fonte` / `retorica` |
| `conferir` | a cada ciclo de 30 min, em toda spec | microssegundos, offline | veredito existe? aprovou? a narração ainda é a mesma? |

A terceira pergunta é a que dá força às outras duas: o veredito guarda o **sha256 da
narração inteira**. Trocar uma palavra muda a impressão e **anula a aprovação**. Não há
como aprovar um roteiro e renderizar outro.

Regras que saem disso:

- Spec com `autoria: "maquina"` **não renderiza** sem veredito aprovado. O portão está em
  `prontidao.PORTOES` e em `orquestra._falhas_baratas`, que é o que monta a matriz da frota.
- Spec escrita à mão **não precisa** de veredito. O corte por `autoria` é a fronteira
  exata do problema: quem responde por ela é a pesquisa que já foi feita.
- Reprovada vira `.json.reprovado` e **não é apagada**. Apagar em silêncio esconderia
  quanto o gerador erra — que é o número que decide se isto continua ligado.
- `sem_fonte` reprova igual a `refutado`. Dúvida não vira aprovação.

### O tamanho se pede em caracteres, não em cenas

A duração não está no número de cenas: `duração = chars/R + frases×P`. Duas consequências
que custaram vídeo antes de virarem código:

1. **Corrigir em caracteres.** Pedir *"acrescente cinco cenas"* devolve cinco cenas de
   tamanho arbitrário e a medida seguinte erra de novo.
2. **A densidade é do canal.** O termo `P` é por frase, e cada canal escreve com uma
   densidade própria e estável — `setiap-level` 1,98 frases/cena, `seviye-seviye` 2,71.
   Prever com a mediana do corpus erra 3,9%; com a mediana do próprio canal, **1,4%**.
   Como a tolerância do laço é 7,4%, isso é a diferença entre o primeiro rascunho já
   nascer dentro e gastar mais uma chamada de modelo.

E **o laço mede o short junto com o longo**. Em 20/08 o `labtreinamento-003` foi ao ar com
short de 47,6 s, fora do teto de 45, porque o dimensionamento só olhava o longo. Em canal
frio é o short que entrega — 19,32 v/d contra 0,15 dos longos no `setiap-level`. O alvo do
short passa a ser o **meio** da faixa útil (37 s), nunca o teto.

#### Em short, o modelo de voz tem viés — e viés não se trata com margem

O `(R, P)` de cada voz é ajustado **só em cena de longo**: a calibração lê os `legendas.srt`
do bucket, e short queima a legenda em vez de exportar `.srt`. Aplicado a short, o modelo
erra — e erra sempre no mesmo sentido.

Eu compensei isso à mão por duas semanas: a cada short publicado, media *um* erro e subia
`MARGEM_SHORT` para cobrir o pior caso até ali — 3%, 5%, 7%, 7,5%, quatro valores em dois
dias. Isso nunca converge, porque o máximo de uma amostra cresce com `n`.

O que encerrou a questão não foi estatística melhor, foi **olhar onde o dado já estava**: a
esteira grava `videos.duracao_s` com o ffprobe do arquivo montado, ou seja, a duração real
de todo short publicado está no banco desde o primeiro dia. Trinta medidas de uma vez, em
vez de nove ao longo de duas semanas.

Com a amostra inteira o diagnóstico muda: **28 das 30 erram para cima, mediana +4,7%**. É
viés, não dispersão. Margem de segurança não conserta viés — ela esconde, e cobra o preço
de reprovar roteiro bom. Quem conserta é a previsão:

| constante | valor | o que é |
|---|---|---|
| `ensaio.VIES_SHORT` | 1,047 | mediana do erro; multiplica a previsão de short |
| `prontidao.MARGEM_SHORT` | 0,043 | percentil 95 do **resíduo**, depois do viés |

Regras que ficam:

1. **Toda previsão de short passa por `duracao_estimada_short`.** A crua é para longo.
2. **O teto é sobre a previsão**: `45 / (1 + margem)` = 43,1 s, nunca `45 × (1 − margem)`.
   As duas dão "um número menor que 45" e respondem a perguntas diferentes.
3. **Medida só calibra quando o texto de hoje é o texto que foi lido.** Se
   `git log -1 --format=%cs` do `.json` for posterior a `publicado_em`, a medida entra em
   `medidas_short.tsv` mas fica fora da conta. Foi assim que três shorts que eu **estiquei**
   depois do render apareciam como erro de −20%.
4. **Percentil 95, não máximo.** Com `n ≥ 20` o percentil é estimável; o máximo continua
   sendo ruído. Quem reescrever a constante roda `python3 fabrica/calibra_short.py` — o
   `test_calibra_short` cobra que os três (TSV, viés, margem) concordem.

### O gargalo mudou de lugar: agora é a PESQUISA

Primeiro disparo real, run 32349960529: **31 segundos, verde, zero spec escrita.**
Duas causas empilhadas, e ambas só apareceram porque fui ler o log de um job verde:

1. `ANTHROPIC_API_KEY` não existia nos segredos do repositório.
2. O canal escolhido não tinha pauta em banco.

Daí três regras que agora estão em código: a chave morre no início do job com `::error::`
e não dentro do laço; **carência existindo e nada escrito vira `::warning::`** com o motivo
por canal; e `carencia` devolve **código 3** quando há carência e nenhum canal com pauta,
para o workflow não ler lista vazia como "fila cheia".

E o achado maior. Com a escrita automatizada, **o que segura a frota passou a ser o banco
de pautas.** Medido em 20/08:

| canais com pauta em banco | canais em zero |
|---|---|
| resep-naik-level 12 · sx-educacao 12 · agla-level 4 · labtreinamento 4 · seja-mais-magra 4 | cocina-por-niveles · epomeno-epipedo · game-money-lab · kolejny-poziom · next-level-money · nivel-do-jogo · setiap-level · seviye-seviye |

São ~24 pacotes de estoque de pauta antes de secar — e a fila por carência entrega
justamente os canais em zero, porque **o mais carente costuma ser o que a pesquisa não
visita há mais tempo**. Por isso `carencia` filtra canal sem pauta e avisa quais são.

Quem enche o banco é o **PASSO 0 da rotina horária**, que continua manual. Automatizar a
pesquisa é o próximo degrau e depende de acesso à YouTube Data API a partir do runner.

### O custo é novo nesta máquina

Até aqui um pacote custava CPU de runner. Agora custa dólar de API, e a conta escala com a
meta. Por isso o `autoria.yml` nasce com `pacotes: 1` por disparo e **toda geração imprime
o gasto** (`fabrica/modelo.py` conta tokens e dólares por chamada). Os primeiros dias
servem para **medir o custo por pacote**; o ritmo se decide depois. Subir o número antes
de ter a medida é escolher no escuro.

---

## 2b. A camada falada — o defeito que a máquina não enxergava

`python3 fabrica/narracao.py <spec.json>` roda **antes do TTS** (é a etapa 0 do
`etapas.py`) e derruba o build em erro. Existe porque todas as outras etapas medem se o
vídeo *saiu*, e nenhuma media se ele *prende*.

Rodado nos 7 pacotes que existiam, achou um defeito sistêmico:

**Toda virada de capítulo fechava com ponto final morto — 116 ocorrências, nos 7.**
É o segundo exato em que o espectador decide sair, e não havia um gancho sequer. A última
cena antes de um capítulo novo termina em pergunta, dois-pontos ou reticências.

As outras três travas:

| Trava | Limite | Por quê |
|---|---|---|
| Frase-planilha | ≤ 3 quantidades por frase | O ouvinte perde a conta. *(A justificativa de duração que eu tinha escrito aqui era o oposto do medido — ver abaixo.)* |
| Ritmo | 6% a 45% de frases ≤ 5 palavras | Longa que monta → média → **soco**. `agla-level-003` saiu com 1,3%: monótono do início ao fim |
| Understatement | zero hype, zero slop | "inacreditável", "neste vídeo vamos", "estudos mostram" sem nome |

> Conta-se **quantidade**, não palavra de número. `dua ribu dua puluh enam` são quatro
> palavras e **um** número — o ano. A primeira versão contava palavra e acusava 8 numa
> frase que fala de duas; um linter que grita à toa é um linter que ninguém lê.

Origem: skill `roteiro-deep-time`, publicada no vídeo `bIIACr4z7F4`. O resto do que
aquele material ensina (pesquisa de pauta, fonte dupla, controle de duração) a máquina
já fazia — e melhor.

### As cenas do longo entram em camadas

Cada cena vira **base + uma camada por elemento**, e os elementos entram no ritmo da
fala — fade de 0,40 s e deslize de 26 px, espalhados pelos primeiros 62% da cena. A
camada é do tamanho do quadro, então o `overlay` vai em `x=0` e não há coordenada para
acertar duas vezes.

Isso substitui a cena que chegava pronta: quatro itens apareciam juntos e ficavam
parados os dez segundos em que o narrador os percorre um a um.

> **`-framerate 30` em CADA imagem do caminho de camadas.** Sem isso o `-loop 1` entra
> a 25 fps e as cenas com camada saem a 25 enquanto as sem camada saem a 30 — o concat
> junta as duas **sem reclamar** e o resultado é fps variável. Medido: 225 quadros em
> 9 s virando 270.

O **short fica de fora**: são 30 s com legenda queimada, e ali a entrada escalonada
rouba tempo de leitura em vez de dar ritmo.

### Dimensione pela fórmula, nunca pela tabela de chars/s

```
duração = chars / 20,58  +  frases × 0,96  +  cenas × 1,08
```

A voz lê a 20,58 chars/s; cada ponto final custa **0,96 s de pausa**; cada cena custa
mais **1,08 s** (é um mp3 separado, com silêncio de borda, e o `etapas.py` soma 0,5 s de
folga por clipe). Medido para `id-ID-ArdiNeural`.

Duas consequências que contrariam o que este arquivo dizia antes:

- **Número não deixa a narração lenta — deixa rápida.** Amostra densa em número por
  extenso: **20,58** chars/s. Amostra de frases curtas: **12,01**. O que custa tempo é a
  pausa, não o número. A regra das ≤3 quantidades continua valendo por *retenção*.
- **O ritmo que o linter exige alonga o vídeo.** Mais frases curtas = mais pausas. 14% de
  frases curtas dá 17,0 chars/s efetivos; 50% dá 12,01.

Validação: previu 853 s, o render deu 853,9 s. O termo por cena vem de **um** pacote —
confirmar no próximo antes de tratar como medido.

---

## 2c. Sincronizar o sandbox — confira antes de renderizar

`fabrica.py` importa de `src/maquina` (`ffmpeg_bin`, `duracao`). Transferir o arquivo
sozinho **quebra** o sandbox: leve o fecho de dependências.

```
fab/fabrica.py + src/maquina/{__init__,models,media}.py
```

Confira os quatro md5 contra o repositório **antes** de renderizar. Divergiu duas vezes
no mesmo dia — uma delas com `ken_burns` e `dir_trabalho` diferentes, que é exatamente o
par que produz vídeo costurando dois roteiros sem levantar erro.

> **O último bloco do tar.gz vai em hex, não em base64.** O padding do gzip é uma corrida
> longa de caracteres repetidos; em base64 um erro dentro dela mantém o tamanho e não
> aparece. Aconteceu: 284 bytes certos, md5 errado.

### O sandbox recicla — guarde a fábrica no Storage

O sandbox some sem aviso e leva junto a fábrica, as dependências, `/tmp/.upk` e
`/tmp/.sburl`. Aconteceu no meio de um disparo e custou cinco blocos de base64 para
refazer. **Depois de sincronizar, suba o tar.gz para o bucket:**

```
curl -s -X POST "$SB/fabrica.tgz" -H "Authorization: Bearer $ANON" -H "apikey: $ANON" \
     -H "Content-Type: application/gzip" --data-binary @fabrica.tgz
```

Aí a recuperação vira um `curl` do público + `tar -xzf` + `pip install edge-tts cairosvg`.
Confira o md5 contra o repositório mesmo assim — o Storage é INSERT-only, então um
`fabrica.tgz` velho lá dentro **não é sobrescrito** e você baixaria a versão errada
sem nenhum erro. Se o md5 divergir, suba com nome novo (`fabrica-AAAAMMDD.tgz`).

> **Aconteceu em 2026-08-11 e custou a publicação de um pacote.** O sandbox
> reciclou, o bucket **não tinha** o tar prometido acima, e `/tmp/.upk` (chave
> da Upload-Post) sumiu junto — a chave não existia em nenhum outro lugar. A
> fábrica foi restaurada arquivo a arquivo com md5 conferido (8/8), e o backup
> atual é `fabrica-20260811.tgz`. A chave só o Pablo pode repor; enquanto ela
> não tiver casa persistente (GitHub secret `UPLOAD_POST_KEY`), todo recycle
> do sandbox bloqueia a publicação de novo.

> **`/mnt/files` NÃO é disco durável — medido em 2026-08-12.** Era tratado como
> a cópia segura do sandbox. Numa reciclagem o diretório veio **vazio**, com um
> `/tmp/s3fs_mount.err` no lugar: é um s3fs e o mount pode simplesmente falhar.
> Quem salvou foi o Storage — 6/6 recursos responderam HTTP 206 e a fábrica
> inteira, as três trilhas e a referência de voz voltaram em ~1 minuto.
> **A única cópia durável é o Storage.** `/mnt/files` serve como cache; nada
> pode depender dele para sobreviver a um recycle.

**Restaurar um sandbox novo** (o caminho testado, `videos-maquina/fabrica/`):

```bash
B=https://vevocauwtarctfwngrch.supabase.co/storage/v1/object/public/videos-maquina
mkdir -p /tmp/spec /tmp/trilhas
for f in etapas.py fabrica.py visual.py narracao.py tagbudget.py publicar.py; do
  curl -sfL -o /tmp/spec/$f "$B/fabrica/$f"; done
for t in Wholesome Inspired Deliberate_Thought; do
  curl -sfL -o /tmp/trilhas/$t.mp3 "$B/trilhas/$t.mp3"; done
curl -sfL -o /tmp/referencia-corte.wav "$B/voz/referencia-corte.wav"
pip install -q edge-tts cairosvg
md5sum /tmp/spec/*.py     # tem que bater com fabrica/*.py do repositório
```

Para **atualizar** um arquivo no Storage, use `.github/workflows/ponte-arquivo.yml`
com `destino_storage`. Ele existe porque o container da rotina leva 403 de política
em `supabase.co`, e porque o Storage separa criar de atualizar: `POST` recusa objeto
existente e `PUT` recusa objeto inexistente — a ponte tenta os dois. Sem isso, o
reenvio falha e a cópia durável envelhece uma versão atrás sem ninguém notar
(aconteceu com `fabrica/etapas.py` em 2026-08-12).

### O short passou a ser conferido — e o layout 16:9 não serve para ele

Todos os shorts publicados até 2026-08-11 saíram com a geometria 16:9 esticada
no quadro 9:16: o círculo do layout `item` começava fora da borda esquerda e a
legenda queimada encostava nas duas laterais (visual.py: 6/6 quadros com tinta
na borda, 3–6,3%). Ninguém viu porque o `etapas.py` só conferia o longo.

Correções, todas no repositório: `svg_cena` desvia para `svg_cena_retrato`
quando H > W (geometria dimensionada pela largura — margem medida: 0,00%);
`EST` ganhou `MarginL/R=18`; e o `etapas.py` ganhou a **etapa 8**, que
renderiza o short pela mesma fábrica e o reprova no mesmo teste visual do
longo. Short de script avulso acabou.

---

## 3. Produção — o que quebra em silêncio

Estes três já entregaram vídeo defeituoso sem levantar erro nenhum:

| Armadilha | Sintoma | Guarda hoje |
|---|---|---|
| Fonte sem o script do idioma | legenda queimada **vazia**, texto sem shaping | `usar_fonte()` confere no `fc-list` e quebra alto |
| Capítulo medido no mp3 | deriva de ~23s no vídeo inteiro | tempos vêm de `dur(lclipNN.mp4)` |
| Download que falhou | HTML salvo como `.mp3` passa em tamanho e extensão | `trilha_ok()` mede duração > 30s |

**Meça a taxa da voz antes de dimensionar o roteiro.** Elas variam 53%:

| Voz | chars/s | pausa s/frase |
|---|---|---|
| `hi-IN-MadhurNeural` | 9,85 | — |
| `id-ID-GadisNeural` | 11,8 | — |
| `pt-BR-AntonioNeural` | 13,42 | — |
| `en-*` | 14,5 | — |
| `id-ID-ArdiNeural` | 15,1 (20,58 pura) | 0,96 |
| `pl-PL-MarekNeural` | 23,05 pura | **1,40** |

> A coluna de pausa importa mais que a de taxa: no `pl-PL-MarekNeural` a pausa
> por frase é a maior já medida e as pausas custaram 284s dos 773s do
> `kp-plan-9233` — o modelo de três termos previu 757s e o render deu 772,6s
> (erro +2%). Em polonês, menos frases e mais longas rendem mais minuto por
> caractere.

Limites do sandbox: tmpfs **493 MB**, RAM ~985 MB, bash **180s por comando**. Renderize em
lotes de 10 cenas apagando png/mp3 consumidos. Acima de ~18 min: áudio 128k e CRF 29, senão
estoura o teto de 50 MB do Storage.

---

### Número de pacote se consulta, não se supõe

`python3 fabrica/grava_spec.py <slug>` diz quais números estão ocupados e qual é o próximo
livre. Todo build script novo grava por `grava_spec.grava(SPEC)`, que **recusa** escrever por
cima de um `.json` cujo título é outro.

Isto existe porque em 20/08/2026 escolhi `epomeno-epipedo-005` por suposição. O -005 existia,
estava commitado e **o vídeo já estava no ar**. O build script reescreveu o `.json` inteiro e
nenhum portão reclamou — os portões conferem se a spec está *certa*, não se ela é a spec
*certa*. O que pegou o erro foi acidente: a extração das tags falhou e a copy que apareceu era
de outro vídeo.

## 4. Entrega

```
sandbox curl → Supabase Storage → GOOGLEDRIVE_UPLOAD_FROM_URL → GOOGLEDRIVE_MOVE_FILE
```

- **Para saber se um passo emitiu aviso ou erro, leia as ANOTAÇÕES do job**, não o log:
  `GET /repos/<owner>/<repo>/check-runs/<job_id>/annotations`. Elas trazem exatamente os
  `::error::` e `::warning::` que a fábrica emite, sem o ruído de instalação e cleanup.
  Em 21/08/2026 gastei três chamadas paginando um log sem achar as linhas de thumbnail e
  legenda, e terminei dizendo ao Pablo que não consegui verificar; **uma** chamada nas
  anotações respondeu na hora. O log serve para NÚMERO (duração medida cena a cena); a
  anotação serve para VEREDITO.

- **`frota.yml` recebe ARRAY JSON no input `pacotes`**, não o nome do pacote:
  `[{"canal":"next-level-money","pacote":"next-level-money-006","idioma":"en"}]`.
  Mandar a string solta faz o `jq -c '{include:.}'` produzir um escalar, a matriz sai
  vazia e o run falha em segundos — **com o job `preparar` marcado como `success`**.
  Esse par é a assinatura a reconhecer: *um único job, verde, run vermelho, zero
  anotações*. Isso é matriz vazia, não erro de render, e não adianta procurar no log
  do render porque render nenhum chegou a existir. Aconteceu em 24/08/2026 (run
  32745494822); o redisparo no formato certo é o 32745698913.

- **`GOOGLEDRIVE_UPLOAD_FROM_URL` ignora o parent.** Tudo cai na raiz `0AL8gANwo3v7jUk9PVA`.
  O `MOVE_FILE` não é opcional — sem ele o pacote fica órfão.
- **Os dois campos dele são `source_url` e `name`.** Não `file_url`, não `file_name`. A nota
  antiga só corrigia metade (`name` em vez de `file_name`) e por isso o erro voltou em
  20/08/2026: `Following fields are missing: {'source_url'}`. Uma ida e volta perdida por
  uma nota incompleta — quando corrigir um nome de campo, confira os outros da mesma chamada.
- A URL do Storage precisa do segmento **`/object/public/`**; sem ele o Drive recebe 400 porque
  a leitura vai autenticada e o Composio não manda header.
- Caminho no Storage: `AAAA-MM-DD-<slug>-<seq>-<artefato>`. Sem o `<seq>` dá **409** quando o
  mesmo canal entrega dois pacotes no mesmo dia.
- **Não mande `x-upsert: true`** — a policy anon é INSERT-only e upsert responde 403.
- Não use `upload_local_file` do workbench: morre quando o kernel reinicia.

### Publicação (Upload-Post)

`POST https://api.upload-post.com/api/upload`, header `Authorization: Apikey <chave>`,
`async_upload=true`, e depois `/uploadposts/status?request_id=`.

**`privacyStatus=public`, sempre.** Não listado não entra em recomendação e não acumula
sinal de algoritmo — é vídeo produzido para não ser visto. *(Conferido na API: os cinco
vídeos do canal estão `public`. O parâmetro sempre funcionou.)*

**`youtube_subtitle_file` + `youtube_subtitle_language` são obrigatórios no longo.**
A API devolve `contentDetails.caption = false` nos cinco vídeos publicados — inclusive
nos dois longos que têm `legendas.srt` pronto e guardado no Storage. Eu tirei o parâmetro
durante a bisseção do erro de tags e nunca recoloquei. Em canal de idioma não-inglês a
legenda alimenta a busca, permite tradução automática e sustenta retenção no mudo.
A Upload-Post só aceita legenda **no momento do upload** — não dá para anexar depois.

**Rode `python3 fabrica/tagbudget.py tags.txt` antes de enviar.** O limite de 500
caracteres do YouTube vale para o conjunto, e toda tag com espaço entra entre aspas:
custa `len+2`. Somar só os caracteres aprova lista que o YouTube rejeita — foi o que
derrubou o `setiap-level-004` duas vezes, com 477 de soma e **542 de custo real**.

Quando a API devolver mensagem específica (`One or more tags are invalid`), **esgote
essa causa antes de inventar hipótese estrutural.** O `error_code` e o `failure_stage`
da Upload-Post são genéricos (`media_invalid_format` / `media_validation`) e não
contradizem a mensagem. Ignorar isso custou dois envios e uma regra falsa.

Leia as tags com `mapfile -t` e grave o arquivo **com quebra de linha final** — o
`while read` descarta a última linha, e o sintoma é uma tag a menos, silenciosa.

### Rota própria: `fabrica/publicar.py`

O que publicou os pacotes de 2026-08-11 era código solto dentro de uma sessão, reescrito
a cada disparo. Agora mora em `fabrica/publicar.py`, e a **ordem dos passos é medida**:

1. **Short primeiro.** Em canal frio o feed de Shorts entrega e o de longos não — 4
   shorts entre 1,7 e 17,9 views/hora contra 4 longos entre 0 e 0,2. O short leva o
   link do longo, nunca o contrário.
2. **Longo**, com a descrição já apontando para o short que acabou de subir.
3. `thumbnails/set` — **403 aqui não é defeito do código**, é canal sem verificação por
   telefone. O vídeo continua público; só a capa fica pendente.
4. `captions.insert` (multipart) — **409 é sucesso**: o vídeo já tem faixa naquele
   idioma. Foi esse 409 lido como falha que manteve viva a regra "nenhum vídeo tem
   legenda" depois de ela já estar resolvida.
5. `playlistItems.insert` — playlist por canal levanta sessão, e é uma chamada.

Os passos 3 a 5 **não precisam de Studio manual**: num único passe em 2026-08-11 saíram
9 thumbnails, 3 faixas de legenda e 4 playlists sobre vídeos **já publicados**.

---

## 4c. A frota — 12 canais e a divisão do dia

`config.plano_diario_canais` guarda a conta; ela parte da capacidade medida, não do teto
da cota:

| cenário | pacotes/dia | uploads/dia | % da cota (100) |
|---|---|---|---|
| hoje, sandbox de 1 CPU | 5 | 10 | 10% |
| frota no Actions | 24 (2/canal) | 48 | 48% |
| teto da cota | 50 | 100 | 100% |

O teto de 100 **não é alcançável hoje** e nem é o alvo certo: 4 pacotes/dia/canal passa
do limite anti-spam de 2 longos/dia/canal. O alvo é 2 pacotes/dia/canal.

O que separa a linha 1 da linha 2 é orçamento de minutos do Actions, não código. O repo é
**privado**: 2.000 min/mês grátis, e um pacote custa ~25 min num runner de 2 vCPU. Para
24 pacotes/dia são ~18.000 min/mês (~US$ 128/mês). **Repo público zera isso** — minutos
ilimitados e runner de 4 vCPU, que é justamente o porte medido em 13 min/pacote. É uma
decisão do dono, não da máquina; o que a máquina pode dizer é o número.

Divisão do dia: `v_maquina_fila` já ordena por canal com YouTube primeiro e
`ultimo_pacote_em` mais antigo — a rotação sai dela, sem lista fixa. Um canal por disparo,
completo, continua valendo dentro de cada job.

---

## 5. Registro

Uma linha em `videos` por pacote, com **colunas reais** — não jsonb.
`canal`, `fonte_pauta`, `fonte_pauta_vd`, `similaridade`, `duracao_s`, `duracao_short_s`,
`drive_*`, `supabase_url`, `lufs`, `tamanho_mb`, `cenas`, `capitulos`.
O `roteiro` jsonb guarda só o que é narrativo.

> Regra que nasceu de um defeito: **o que vai ser comparado entre pacotes mora em coluna.**
> Enquanto tudo estava no jsonb, `videos` nem sequer tinha coluna de canal, e nenhum
> aprendizado era computável por SQL.

Depois: `update canais set ultimo_pacote_em = now(), pacotes = pacotes + 1`.

---

### Reaproveitar pacote de canal irmão

Quando o canal que existe não tem mais nada próprio na fila, um pacote parado em
canal ainda não criado **pode** ir para ele — mas o critério é **idioma + tema**,
nunca a mera existência do arquivo.

Feito em 05/08: `resep-naik-level-002` ("Belanja Mingguan Rp100.000", custo de vida
com preços médios nacionais) subiu no Setiap Level. Indonésio, mesmo país, tema de
dinheiro — cabe na descrição do canal, que fala de como o dinheiro molda a vida.

O que **não** fazer: publicar grego, turco ou espanhol no canal indonésio. O
algoritmo aprende o público de um canal pelo histórico; misturar idiomas ensina que
ele não tem público definido, e aí ele para de recomendar também o que estava certo.

Pacote anterior à exportação de `legendas.srt` sobe **sem legenda** — não dá para
reconstruir, porque o SRT precisa da duração real de cada clipe, que só existe
durante o render.

---

## 5b. Como ler desempenho sem se enganar

**Janela mínima de 48h.** Em 05/08 comparei cinco vídeos publicados e quatro deles tinham
**uma hora de vida**. Nessa janela qualquer leitura mede relógio, não conteúdo. Registre
o número, não o veredito.

O que os dados mostraram, com essa ressalva:

| vídeo | duração | idade | views | v/d |
|---|---|---|---|---|
| `GKQXVoA1zS0` | 0:27 | 37h | **572** | ~371 |
| `ZYh3bpLP5JE` | 0:42 | 1h | 0 | — |
| `I6no74M2NDU` | 0:34 | 1h | 0 | — |
| `G8ocnpQIiyg` | 25:45 | 1h | 1 | — |
| `v-5v7R13BBc` | 28:36 | 1h | 1 | — |

A diferença gritante é idade, não formato. Mas há um sinal estrutural que sobrevive à
ressalva: **o único vídeo com alcance é um short.** O feed de Shorts entrega a canal sem
histórico; o feed de longos não.

### Views acumuladas não são taxa

Eu li "572 views em 37h" como **371 views/dia**, como se fosse ritmo. Na remedição 1h30
depois o contador estava **congelado em 572**, com as mesmas 2 curtidas.

Não era taxa. Foi **uma rajada única que já terminou** — o vídeo pegou um empurrão do
feed de Shorts e parou. Antes de citar views/dia, **meça duas vezes com intervalo** e
confirme que o número anda. Um denominador não transforma um evento em tendência.

### As três diferenças entre o que pegou e o que não pegou

O vídeo que recebeu distribuição foi feito por outro processo, e é diferente em três
coisas concretas. Nenhuma está provada como causa — o que segue é hipótese com base
material, para virar experimento.

**1. O short dele resolve; os meus são trailer.** Em 27 segundos ele entrega três
hábitos completos, cada um explicado, e fecha com uma pergunta. Os meus fecham mandando
o espectador embora: *"sistem lengkapnya ada di video panjang"*. Short que não resolve
nada pede clique em vez de dar valor — e o feed mede retenção até o fim. **O short tem
que se sustentar sozinho.** O longo é continuação opcional, nunca condição para a coisa
fazer sentido.

**2. As tags estão invertidas.** Ele usa 11 tags largas: `uang`, `gaji`,
`ekonomi Indonesia`, `gaya hidup`. Eu uso 15 a 19 de cauda longa: `sbn ritel pemula`,
`harga kedelai 2026`, `iuran bpjs berapa persen`. Cauda longa é a estratégia de quem já
tem autoridade e disputa termo específico; em canal sem histórico ela **isola** o vídeo
de qualquer cluster grande. A mistura certa é âncora larga primeiro, cauda longa depois.

**3. Ele fala COM o espectador; os meus descrevem um objeto.** *"Três hábitos pequenos
que estão secretamente drenando o SEU salário"* contra *"Lista exata para sete dias"*.
Não é qualidade de escrita — é a quem a frase é dirigida. Pelo menos o gancho e o título
do short precisam voltar para a segunda pessoa e para uma dor que o espectador reconhece
em si.

### O que não dá para medir hoje

`/analytics/<perfil>?platforms=youtube` da Upload-Post volta **tudo zerado** — o escopo
OAuth *dela* não inclui YouTube Analytics.

Isso vale para a Upload-Post e **não** para os tokens próprios: em 20/08/2026 medi que a
coleta própria (`diagnostico.yml` → `coletar_metricas`) recebe retenção de verdade. O que
falta ali é audiência, não permissão — ver a seção do laço de aprendizado. Impressões e
CTR continuam zeradas nos dois caminhos.

---

## 6. O laço de aprendizado

Este é o ponto do documento. A máquina não deve reaprender a mesma coisa duas vezes.

```
incidente ou medição
      ↓
aprendizados  (regra + evidência numérica + onde é aplicada)
      ↓
guarda no código  (usar_fonte, trilha_ok, auditar.py)  ou  passo da rotina
      ↓
próximo disparo lê v_maquina_regras antes de produzir
```

**Ao fim de todo disparo, pergunte três coisas e grave a resposta:**

1. Alguma coisa quebrou ou saiu diferente do esperado? → `aprendizados`, com a evidência.
2. Alguma escolha foi um palpite? → `experimentos`, com hipótese e métrica-alvo.
3. Alguma medição nova? → `pautas_banco`, inclusive os resultados ruins.

Regra só vale com **evidência numérica** e com **`aplicado_em` preenchido**. Regra sem lugar
de aplicação é anotação, não aprendizado. Quando a evidência for contrariada, marque
`status = 'invalidado'` com o motivo — não apague; o histórico do erro é parte do acervo.

Regenere `APRENDIZADOS.md` a partir da tabela quando ela mudar. A tabela é a fonte da verdade.

---

## 7. Nunca

- Publicar pela **Composio** `YOUTUBE_UPLOAD_VIDEO` (6/6 apagados). A Upload-Post é
  outra coisa: auditada, e com 3/3 sobrevivendo.
- Publicar como `unlisted` ou `private`.
- Enviar tags sem passar pelo `tagbudget.py`.
- Gravar dado de vídeo no projeto `cscczluzpblzhvojxanp` (é o CRM).
- Criar triggers novos.
- Longo abaixo de 8 minutos.
- Escalonar duração sem correlação medida no grupo de pares.
- Fechar um pacote com arquivo parado na raiz do Drive.
- Digitar a URL do Storage à mão — vem de `/tmp/.sburl`.
- Arredondar número que a fonte institucional deu com precisão — nem na narração,
  nem no título.
- Renderizar o longo sem `-framerate 30` em cada imagem do caminho de camadas.
- Fazer o short ser recorte do longo: ele fecha sozinho e **depois** aponta.
- Procurar contorno para a publicação em onde o código roda (Colab, Supabase,
  auto-hospedado). A trava é do **projeto** da API. Três perguntas equivalentes já
  gastaram tempo com a mesma resposta.
