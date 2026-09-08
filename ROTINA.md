# ROTINA — o prompt do disparo horário

Cópia versionada do prompt em `trig_01Y6ZvwsrbxteyS933sgzqK4`
(*"Máquina YT — construir e otimizar até monetizar"*, cron `8 * * * *`).

O trigger é a fonte que executa; este arquivo existe para que a rotina tenha
histórico em git. **Quando um mudar, mude o outro no mesmo commit.**

---

## Mudança de 08/09/2026 — ritmo de 1 a 3 pacotes/dia/canal, e o Storage vira ponte

Quatro fatos medidos em 08/09/2026 motivaram esta versão:

| fato | número | consequência |
|---|---|---|
| a rotina estava **desligada** | `enabled=false`, último pacote 01/09 | a frota parou 7 dias; religar é parte da mudança |
| Supabase Storage quase cheio | **622 MB de 1 GB**, e 620 MB são 46 MP4 | o MP4 é apagado do bucket assim que o Drive confirma, no mesmo pacote |
| Pexels construído e não usado | **2 de 83 specs** têm `broll_q` | b-roll deixa de ser experimento e vira obrigatório |
| duplicatas no ar | 11 no `kolejny-poziom`, 10 no `nivel-do-jogo` | a guarda anti-duplicata passa a **bloquear**, não avisar |
| `expurgo-storage.yml` sem cron | só `workflow_call`/`dispatch` | passa a ser chamado ao fim de todo disparo |

**Sobre o ritmo.** Em 24/08 o teto foi baixado de 5 para 1 pacote/dia/canal, e o
motivo registrado no PLAYBOOK não era cadência: era duplicata — ~3.100 das ~4.029
views do `kolejny-poziom` vinham de **cinco cópias do mesmo short**. O teto de 1 foi
o remédio disponível na época porque a guarda anti-duplicata não bloqueava.

O alvo agora é **1 a 3 pacotes/dia/canal**, e ele só é legítimo com o remédio certo
no lugar: a duplicata é barrada na origem (§ FILA), não pela escassez de vagas.
Se a guarda de similaridade estiver desligada ou falhando, **o teto volta a 1** —
essa é a condição, não uma recomendação.

Diferenças em relação à versão de 05/08/2026:

| antes | agora |
|---|---|
| MP4 ficava no bucket depois da cópia | **apagado do bucket no mesmo pacote**, assim que o `drive_id` volta |
| b-roll do Pexels = experimento 10, opcional | **obrigatório**: ≥40% das cenas do longo, ≥2 no short |
| 1 pacote/dia/canal (teto de 24/08) | **1 a 3/dia/canal**, condicionado à guarda anti-duplicata |
| um canal por disparo | **lote por disparo**, até acabar a quota de LLM do dia |
| short 30-45 s | **short 26-38 s** — os dois maiores da frota têm 26 s e 30 s |
| similaridade ≤0,65 avisava | similaridade ≤0,65 **bloqueia**, e título quase-igual também |

---

Rotina horária da máquina de vídeos.

Supabase: projeto **vevocauwtarctfwngrch** (maquina-yt-dark). O projeto antigo
`cscczluzpblzhvojxanp` é de um CRM imobiliário — NÃO gravar nada de vídeo lá.

ANTES DE TUDO: leia PLAYBOOK.md no repositório e rode
`select * from v_maquina_regras where severidade in ('critico','alto')`. Ele descreve
como a máquina opera hoje; a tabela `aprendizados` é a fonte da verdade. Confira também
`md5sum` de fabrica/*.py no sandbox contra o repositório — a cópia em /tmp/fab já ficou
desatualizada e produziu o pacote errado sem levantar erro.

REGRA MESTRA: um pacote por vez, do início ao fim, com entrega incremental. Só comece o
próximo pacote se o anterior estiver 100% entregue E PUBLICADO. O disparo pode fechar
mais de um pacote — o que muda é quantos, não a disciplina de fechar um antes de abrir
outro.

## Teto do disparo

Feche pacotes enquanto **todas** estas condições valerem. Ao primeiro "não", pare,
registre o motivo em `videos.erro` e responda com o que entregou:

1. `config.pacotes_por_disparo` não esgotado (padrão 3);
2. cota de LLM do dia com folga — cheque o contador que `maquina auto` imprime por
   provedor antes de abrir o próximo pacote;
3. o canal da vez tem menos de 3 pacotes nas últimas 24 h;
4. Supabase Storage abaixo de 800 MB (§ PASSO 2);
5. cota de publicação do mês com folga (§ PASSO 2B).

Nenhum desses tetos é ocioso: cada um já derrubou um job. Prefira **entregar menos e
registrar por que** a estourar um deles.

DURAÇÃO DO LONGO — 12 a 15 minutos (70-90 cenas), 6-8 capítulos de 10-14 cenas,
micro-gancho na abertura e ponte no fim. NUNCA abaixo de 8 min. Em canal com veredito
`suspenso` ou `canal frio`, escreva no PISO da faixa e ponha o melhor material no short.

MEÇA A TAXA DA VOZ antes de dimensionar o roteiro — elas variam de 9,85 a 20,02 chars/s.
Gere um mp3 de teste com números por extenso e divida chars por duração. Assumir o padrão
errado já produziu 9:25 onde eu queria 13:00.

ESCALONAMENTO: canal com retenção acima de 40% ou views/vídeo acima da mediana do nicho
sobe para 25-30 min; registre em config.

## FILA

1. `select * from v_maquina_pendencias limit 1` — só mostra erro com artefato
   recuperável; retome pelo manifesto e entregue o que existe.
2. Senão `select * from v_maquina_fila order by ultimo_pacote_em asc nulls first`
   — pegue o primeiro canal com menos de 3 pacotes nas últimas 24 h.

**GUARDA ANTI-DUPLICATA — bloqueia, não avisa.** Antes de gerar qualquer spec, com o
título candidato em mãos:

- similaridade do roteiro ≤ 0,65 contra os últimos 30 do MESMO canal → acima disso,
  descarte a pauta e sorteie outra;
- título com trigrama em comum com qualquer título já no ar do canal → descarte;
- eixo temático diferente do último pacote do canal → o `canal frio` exige eixo novo,
  e repetir eixo medido que não pegou é o erro que a própria regra proíbe.

Se qualquer uma das três não puder ser verificada (view fora do ar, banco inacessível),
**produza apenas 1 pacote no canal neste dia** e registre a degradação em
`aprendizados`. Cadência sem guarda foi o que gerou as 21 duplicatas hoje no ar.

## PASSO 0 — DEMANDA

Consulte `v_maquina_formatos` e `pautas_banco` ANTES de pesquisar. Depois, via Composio
YOUTUBE_SEARCH_YOU_TUBE + YOUTUBE_GET_VIDEO_DETAILS_BATCH, colete vídeos de 90 dias do
nicho/idioma, calcule VIEWS/DIA, mediana, e isole outliers (≥3x). Grave TUDO em
`pautas_banco`, inclusive os mortos. Confirme números com WebSearch no idioma e em fonte
institucional — duas fontes que batam.

Pauta = (formato que performa) × (dor real datada) × (eixo não usado). O título modela a
ESTRUTURA do outlier, nunca o assunto; keyword nos 5 primeiros termos.

**O que a frota já provou sobre a pauta do short** — use como prior, não como regra:
os três maiores shorts do `setiap-level` falam de COMPORTAMENTO (um hábito que o
espectador tem sem perceber), e os dois maiores são também os mais curtos do canal.
Pauta de comportamento com número fechado bate pauta de informação genérica.

## PASSO 1 — PRODUÇÃO

Sandbox Composio; fábrica em `fabrica/`; `pip install edge-tts cairosvg` se reciclou.

- `python3 etapas.py <spec.json>` — etapas sequenciais, cada uma confere a própria
  saída. Nunca apague clipes em segundo plano.
- Números por extenso, sem dígitos crus (o TTS soletra errado).
- **B-ROLL DO PEXELS — OBRIGATÓRIO.** Toda cena de dado, valor, comparação ou ação
  declara `layout: "broll"` com `broll_q` em inglês. Mínimo **40% das cenas do longo**
  e **2 cenas do short**. O `broll.py` já tem fallback íntegro: se a chave faltar ou a
  busca falhar, o clipe cai no fundo escuro e o render não para. Antes de renderizar,
  rode `python3 fabrica/confere_broll.py` — se ele disser CHAVE AUSENTE, exporte
  `PEXELS_API_KEY` ou grave em `config.pexels_api_key`; descobrir isso depois de 20 min
  de render é o aprendizado 304. Pexels: 200 requisições/hora, sem custo, licença
  comercial livre. Crédito sai em `broll_creditos.json` e entra no copy.
- SHORT 9:16: **26-38 s**, gancho nos 2 primeiros segundos, CTA falado.
- TRILHA: `trilha_do_canal()`, -28 dB, crédito no copy.md.
- Áudio loudnorm I=-14 TP=-1.5, estéreo 48 kHz, +faststart. Legenda queimada só no
  short; o longo exporta `legendas.srt`.
- Thumbnail 1280x720 (máx 3 palavras) + copy.md no idioma do canal: título ≤100 c,
  descrição 200+ palavras com capítulos cronometrados REAIS, CTA, disclosure de
  conteúdo sintético, 3 hashtags, 15 tags, comentário fixado, configurações do Studio.

## PASSO 2 — ENTREGA

**O STORAGE É PONTE, NÃO ARQUIVO — e a ponte se desmonta no mesmo disparo.**

O MP4 continua subindo para o bucket, porque `GOOGLEDRIVE_UPLOAD_FROM_URL` precisa de
uma URL pública e é o bucket que a fornece. O que muda é que ele **não fica lá**.

Em 08/09/2026 o bucket estava com 622 MB de 1 GB, e 620 MB eram 46 MP4 (~13,5 MB cada);
os outros 137 arquivos somavam 2,7 MB. O `expurgo-storage.yml` existe desde 25/08 para
varrer exatamente isso, mas ele só tem `workflow_call` e `workflow_dispatch` — **sem
cron**. Ninguém o chamava, e por isso o peso voltou.

E o custo não é só o teto de 1 GB: o Fair Use do Supabase cobra em **GB-Hrs**, e apagar
não devolve o que já queimou no ciclo. Cada hora que o MP4 fica no bucket é cota gasta.
Segurar 0,65 GB em vez de 3,7 GB é o que separa ~480 GB-Hrs/mês (dentro do teto) de
~2.750 (3,7× acima). Por isso o expurgo não é faxina periódica: é parte do pacote.

Ordem obrigatória, por artefato de vídeo:

1. sobe o MP4 para o bucket (a ponte);
2. `GOOGLEDRIVE_UPLOAD_FROM_URL` a partir da URL pública;
3. confirma o `drive_id` na resposta;
4. **apaga o MP4 do bucket pela Storage API**, no mesmo pacote — nunca por SQL: o
   gatilho `protect_objects_delete` barra, e o escape faria a linha sumir com o arquivo
   continuando a ocupar S3 para sempre.

Só apague depois do passo 3 confirmado. Sem `drive_id`, o MP4 fica e vira pendência.

| artefato | destino final | por quê |
|---|---|---|
| MP4 (longo e short) | **Google Drive** | 15 GB free ≈ 1.100 vídeos |
| legendas.srt | Supabase Storage, **permanente** | 1,5 MB no total, e é a matéria-prima do `calibrar-vozes.yml`, que lê o tempo real de cena |
| thumbnail, copy.md | Supabase Storage | ~1 MB, cabe folgado |
| linhas (`videos`, `metricas`, …) | Supabase Postgres | 21 MB de 500 MB, sem pressão |

`videos.supabase_url` continua valendo como ÍNDICE mesmo depois do MP4 apagado — é dele
que o `calibrar-vozes` deriva o nome do `.srt` trocando o sufixo. Não anule a coluna.

Para os artefatos leves, do sandbox:

    ANON="<chave anon de vevocauwtarctfwngrch>"
    curl -s -X POST "https://vevocauwtarctfwngrch.supabase.co/storage/v1/object/videos-maquina/<AAAA-MM-DD>-<pacote>-<arquivo>" \
      -H "Authorization: Bearer $ANON" -H "apikey: $ANON" \
      -H "Content-Type: <mime>" --data-binary @<arquivo> --max-time 240

Não mande `x-upsert`. Não use `upload_local_file` do workbench.

Para o MP4: GOOGLEDRIVE_UPLOAD_FROM_URL (campo obrigatório é `name`, não `file_name`)
+ GOOGLEDRIVE_MOVE_FILE — o `parent_id` é ignorado no upload e tudo cai na raiz
`0AL8gANwo3v7jUk9PVA`. Grave o id do Drive em `videos.drive_*` e só então apague o MP4
do bucket, como manda a ordem acima.

**Antes de subir qualquer coisa**, cheque o consumo:

    select pg_size_pretty(sum((metadata->>'size')::bigint)) from storage.objects;

Acima de **800 MB**, não abra pacote novo: rode primeiro o `expurgo-storage.yml` com
`executar=true` e `dias=0` e confirme a queda. Ele já sabe o que preservar (`.srt`) e o
que varrer (MP4 com `youtube_id` ou `drive_id`, e órfão sem linha em `videos`).

**AO FIM DE TODO DISPARO**, chame o `expurgo-storage.yml` com `dias=0`, `executar=true`.
Foi a ausência dessa chamada — o workflow não tem cron — que deixou 620 MB voltarem ao
bucket depois da varredura de 25/08.

## PASSO 2B — PUBLIQUE

A rota está validada: 5 vídeos publicados pela Upload-Post contra 6/6 apagados pela
Composio. A proibição da Composio continua valendo.

- `POST https://api.upload-post.com/api/upload`, header `Authorization: Apikey <chave em
  /tmp/.upk>`, `async_upload=true`, depois `/uploadposts/status?request_id=`.
- OBRIGATÓRIOS em todo envio: `privacyStatus=public` (nunca unlisted/private),
  `youtube_subtitle_file` + `youtube_subtitle_language` no longo, `thumbnail_url`,
  `containsSyntheticMedia=true`, `selfDeclaredMadeForKids=false`, `defaultLanguage`,
  `defaultAudioLanguage`, `categoryId=27`.
- ANTES de enviar rode `python3 fabrica/tagbudget.py tags.txt`. O limite de 500 chars do
  YouTube conta tag com espaço entre aspas (len+2); somar só os caracteres aprova lista
  que o YouTube rejeita.
- Leia tags com `mapfile -t` e grave o arquivo com quebra de linha final.
- PUBLIQUE O SHORT PRIMEIRO, apontando para o longo: em canal frio o feed de Shorts
  entrega e o de longos não.
- Se a API devolver mensagem específica, esgote essa causa antes de inventar hipótese
  estrutural — `error_code` e `failure_stage` da Upload-Post são genéricos e não
  contradizem a mensagem.
- Se o canal não existir no YouTube, entregue no Drive e diga ao Pablo qual canal falta
  criar.
- NUNCA publique pela Composio `YOUTUBE_UPLOAD_VIDEO`.

**TETO DE PUBLICAÇÃO — confira antes de gastar.** O plano grátis da Upload-Post dá
**10 uploads/mês em 1 perfil**. Rode `/uploadposts/history` no primeiro disparo do dia,
guarde o consumido em `config.uploads_mes` e pare de publicar quando faltarem 2 do teto.
Pacote produzido e não publicado **não se perde**: entregue no Drive, registre em
`videos` com `erro='cota de publicacao do mes esgotada'` e ele entra na fila do mês
seguinte. Produzir sem publicar é desperdício de CPU; publicar sem cota é job que morre
no fim, depois do render — que é o pior lugar para falhar.

> O teto de 10/mês é o que hoje separa a rotina do alvo de 1 a 3 pacotes/dia/canal.
> Com 13 canais, o alvo pede ~390 a ~1.170 publicações/mês. Enquanto a cota não subir,
> a rotina produz no ritmo novo e publica no ritmo da cota, priorizando o canal com
> melhor mediana de views/dia no short. Isso é degradação declarada, não falha.

## PASSO 3 — REGISTRO

`insert` em `videos` (fonte_pauta, duração real, youtube_id, drive_*, supabase_url,
cenas, capítulos) + `update canais set ultimo_pacote_em=now(), pacotes=pacotes+1`. Uma
linha por formato (longo e short separados). Falha → `videos.erro` com CAUSA e AÇÃO,
preservando clipes prontos. Registre views em `metricas`.

Grave também, por pacote: quantas cenas usaram b-roll do Pexels e quantas caíram no
fallback. Sem esse par de números não dá para dizer se o b-roll mudou retenção.

## PASSO 4 — APRENDA

Ao fim de todo disparo grave: o que quebrou → `aprendizados` com evidência numérica e
`aplicado_em`; o que foi palpite → `experimentos`; o que mediu → `pautas_banco`. Regra
contrariada vira `status='invalidado'` com motivo, nunca apagada.

NÃO conclua desempenho com menos de 48 h de vida. Compare views/dia entre vídeos de
idade parecida.

## PASSO 5 — ANALISE E TENDÊNCIAS

Uma vez por dia, no primeiro disparo após 06:00 UTC.

- RESULTADOS: colete views/likes/comments de TODOS os vídeos publicados via `videos.list`
  (part=statistics, lotes de 50) e grave snapshot em `metricas`. **Mapeie a resposta por
  `item->>'id'`, nunca por posição na lista** — casar por posição embaralhou views de
  short com as de longo e invalidou uma rodada inteira de leitura (aprendizado 549).
  Compare views/dia entre vídeos de idade parecida do MESMO canal; ganhador/perdedor vira
  linha em `pautas_banco` (veredito) e, com 48 h+ de dados, `aprendizados`.
- OTIMIZE O PRÓXIMO: o que o ganhador fez (estrutura de título, gancho, duração, eixo)
  entra na spec seguinte do canal; o que o perdedor fez não se repete sem mudança.
  Registre a decisão em `experimentos` quando for aposta.
- MERCADO/TENDÊNCIAS (rotativo, 1 canal por dia): WebSearch de tendências do nicho no
  idioma (dores novas datadas, mudanças de lei, datas sazonais próximas) + 1 busca
  YouTube de outliers da SEMANA (não 90 dias) para capturar ondas cedo. Grave em
  `pautas_banco` com `observacao='tendencia-semanal'`.
- **CONVERSÃO — a métrica que a frota ainda não venceu.** Dois shorts com 1.097 e 986
  views converteram ZERO inscritos. Toda rodada registra, por canal, `views_do_short` e
  `inscritos_ganhos` no período; enquanto a razão for zero, o experimento aberto continua
  sendo o PEDIDO do short (experimento 26), não o alcance. Alcance a frota já tem.
- PADRÕES DE EXCELÊNCIA (validados 2026-08-11): pattern interrupt nos primeiros 5 s
  (+23% retenção vs abertura estática); loop de retenção a cada 15-30 s (pergunta
  aberta/promessa); estrutura problema→conflito→resolução; CTR e watch time mandam —
  rosto não. Marcação de IA NÃO reduz alcance nem monetização (política oficial); o risco
  real é a política de "conteúdo inautêntico" (jul/2025): produção em massa templated sem
  voz editorial. Antídoto: pesquisa própria com números datados, voz editorial consistente
  por canal, variedade de formatos — e é exatamente por isso que a guarda anti-duplicata
  bloqueia em vez de avisar.

NUNCA criar novos triggers.

Resposta final: canal → título → duração real → fonte da pauta (views/dia) → cenas com
b-roll / cenas em fallback → link do YouTube → links do Drive → "storage: X MB/1 GB" →
"uploads do mês: X/10" → "estoque: X/50".
