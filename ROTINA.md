# ROTINA — o prompt do disparo horário

Cópia versionada do prompt em `trig_01Y6ZvwsrbxteyS933sgzqK4`
(*"Máquina YT — produção guiada por dados + publicação direta"*, cron `8 * * * *`).

O trigger é a fonte que executa; este arquivo existe para que a rotina tenha
histórico em git. **Quando um mudar, mude o outro no mesmo commit.**

## Mudança de 05/08/2026 — publicação deixou de ser condicional

A versão anterior publicava só `SE config.api_auditada = 'true'`, subia como
**privado**, esperava 15 minutos e verificava sobrevivência antes de tornar
público. Esse portão existia porque 6 de 6 uploads pela Composio tinham sido
apagados pelo YouTube.

O portão caiu porque o dado mudou: **5 vídeos publicados pela Upload-Post, 5
sobreviventes.** A regra nunca disse "nenhum terceiro" — disse "nenhum terceiro
não auditado", e a Upload-Post opera a YouTube Data API com auditoria própria.
A proibição da Composio continua valendo.

Outras diferenças em relação à versão antiga:

| antes | agora |
|---|---|
| projeto `cscczluzpblzhvojxanp` (CRM imobiliário) | `vevocauwtarctfwngrch` (maquina-yt-dark) |
| publicava privado e esperava 15 min | publica **público**, direto |
| sem legenda | `youtube_subtitle_file` obrigatório no longo |
| tags sem conferência | `tagbudget.py` antes de todo envio |
| longo primeiro | **short primeiro**, apontando para o longo |
| fila lia `videos` cru | lê `v_maquina_pendencias` (só erro recuperável) |
| taxa da voz assumida | **medida** antes de dimensionar o roteiro |
| — | md5 da fábrica conferido contra o repositório |
| — | proibido concluir desempenho com menos de 48h |

## Mudança de 20/08/2026 — piso de 10 publicados por canal, sorteio na fila

A fila ordenava por `ultimo_pacote_em` (rodízio por antiguidade). Isso distribui
parelho, mas **não fecha lacuna**: em 20/08 havia canal com 26 publicados e canal
com 4, e o rodízio tratava os dois igual.

Passa a valer um piso: **enquanto um canal tiver menos de 10 vídeos publicados,
ele tem prioridade**. Dentro do grupo prioritário o canal é **sorteado**, não
escolhido por antiguidade. Quando todos passarem de 10, o sorteio vale para
todos.

Estado medido em 20/08 (publicados / faltam para 10):

| canal | publicados | faltam |
|---|---:|---:|
| cocina-por-niveles | 0 | 10 — **sem canal no YouTube, bloqueado** |
| agla-level | 4 | 6 |
| game-money-lab | 4 | 6 |
| labtreinamento | 4 | 6 |
| seja-mais-magra | 6 | 4 |
| resep-naik-level | 8 | 2 |
| os outros 7 | 12 a 26 | 0 |

Déficit total 34, dos quais 24 alcançáveis. Os 10 de `cocina-por-niveles`
dependem de o Pablo criar o canal no YouTube.

Outras correções desta data:

- **A nota "plano grátis: 10 uploads/mês" estava desatualizada.** Agosto fechou
  146 publicações, com dias de 11 a 21. O limite não é o que estava escrito;
  confira o consumo real em `/uploadposts/history` antes de assumir teto.
- **CTR e retenção nunca foram coletados.** Em 1.723 linhas de `metricas`:
  `ctr` preenchido em 0, `impressoes` em 0, `retencao_media_pct` em 59 (3,4%).
  A causa é o próprio PASSO 5, que coleta por `videos.list part=statistics` — a
  Data API não devolve impressão, CTR nem retenção. Esses números só saem da
  **YouTube Analytics API** (`reports.query`, escopo `yt-analytics.readonly`).
  Sem eles o PASSO 4 aprende no escuro: não dá para dizer que gancho segurou
  audiência olhando só views.

---

Rotina horária da máquina de vídeos. UM PACOTE POR VEZ, do início ao fim.

Supabase: projeto **vevocauwtarctfwngrch** (maquina-yt-dark). O projeto antigo cscczluzpblzhvojxanp é de um CRM imobiliário — NÃO gravar nada de vídeo lá.

ANTES DE TUDO: leia PLAYBOOK.md no repositório e rode `select * from v_maquina_regras where severidade in ('critico','alto')`. Ele descreve como a máquina opera hoje; a tabela `aprendizados` é a fonte da verdade. Confira também `md5sum` de fabrica/*.py no sandbox contra o repositório — a cópia em /tmp/fab já ficou desatualizada e produziu o pacote errado sem levantar erro.

REGRA MESTRA: um único canal por disparo, completo (longo + short + thumbnail + copy + legendas), com entrega incremental. Só comece outro canal se o primeiro estiver 100% entregue E PUBLICADO.

DURAÇÃO DO LONGO — 12 a 15 minutos (70-90 cenas), 6-8 capítulos de 10-14 cenas, micro-gancho na abertura e ponte no fim. NUNCA abaixo de 8 min.
MEÇA A TAXA DA VOZ antes de dimensionar o roteiro — elas variam de 9,85 a 20,02 chars/s. Gere um mp3 de teste com números por extenso e divida chars por duração. Assumir o padrão errado já produziu 9:25 onde eu queria 13:00.
ESCALONAMENTO: canal com retenção acima de 40% ou views/vídeo acima da mediana do nicho sobe para 25-30 min; registre em config.

FILA: 1) `select * from v_maquina_pendencias limit 1` — só mostra erro com artefato recuperável; retome pelo manifesto e entregue o que existe. 2) senão sorteie o canal com PISO DE 10 PUBLICADOS: canal abaixo de 10 vem primeiro, e dentro do grupo o desempate é aleatório. Respeita `pode_produzir` (máx 3 pacotes/24h/canal e canal existente no YouTube).

    select f.slug, f.nome, f.idioma, f.nicho, f.voz, f.estilo, f.duracao_alvo_s,
           coalesce(p.publicados, 0)                   as publicados,
           greatest(0, 10 - coalesce(p.publicados, 0)) as falta_para_meta
      from v_maquina_fila f
      left join (select canal, count(*) as publicados
                   from videos
                  where status = 'publicado' and youtube_id is not null
                  group by canal) p on p.canal = f.slug
     where f.pode_produzir
     order by (coalesce(p.publicados, 0) < 10) desc, random()
     limit 1;

Canal sem `youtube_channel_id` nunca entra (o `pode_produzir` já barra): entregue no Drive e diga ao Pablo qual canal falta criar.

PASSO 0 — DEMANDA: consulte `v_maquina_formatos` e `pautas_banco` ANTES de pesquisar. Depois, via Composio YOUTUBE_SEARCH_YOU_TUBE + YOUTUBE_GET_VIDEO_DETAILS_BATCH, colete vídeos de 90 dias do nicho/idioma, calcule VIEWS/DIA, mediana, e isole outliers (≥3x). Grave TUDO em pautas_banco, inclusive os mortos. Confirme números com WebSearch no idioma e em fonte institucional — duas fontes que batam. Pauta = (formato que performa) × (dor real datada) × (eixo não usado). O título modela a ESTRUTURA do outlier, nunca o assunto; keyword nos 5 primeiros termos. Similaridade ≤0,65 vs vídeos anteriores do MESMO canal.

PASSO 1 — PRODUÇÃO (sandbox Composio; fábrica em fabrica/; pip install edge-tts cairosvg se reciclou):
- `python3 etapas.py <spec.json>` — etapas sequenciais, cada uma confere a própria saída. Nunca apague clipes em segundo plano.
- Números por extenso, sem dígitos crus (o TTS soletra errado).
- SHORT 9:16: 30-45s, gancho nos 2 primeiros segundos, CTA falado.
- TRILHA: trilha_do_canal(), -28 dB, crédito no copy.md.
- Áudio loudnorm I=-14 TP=-1.5, estéreo 48kHz, +faststart. Legenda queimada só no short; o longo exporta legendas.srt.
- thumbnail 1280x720 (máx 3 palavras) + copy.md no idioma do canal: título ≤100c, descrição 200+ palavras com capítulos cronometrados REAIS, CTA, disclosure de conteúdo sintético, 3 hashtags, 15 tags, comentário fixado, configurações do Studio.

PASSO 2 — ENTREGA. Do sandbox, para cada artefato:

    ANON="<chave anon de vevocauwtarctfwngrch>"
    curl -s -X POST "https://vevocauwtarctfwngrch.supabase.co/storage/v1/object/videos-maquina/<AAAA-MM-DD>-<pacote>-<arquivo>" \
      -H "Authorization: Bearer $ANON" -H "apikey: $ANON" \
      -H "Content-Type: <mime>" --data-binary @<arquivo> --max-time 240

Não mande x-upsert. Não use upload_local_file do workbench. Depois GOOGLEDRIVE_UPLOAD_FROM_URL (campo obrigatório é `name`, não file_name) + GOOGLEDRIVE_MOVE_FILE — o parent_id é ignorado no upload e tudo cai na raiz `0AL8gANwo3v7jUk9PVA`.

PASSO 2B — PUBLIQUE. Isto não é mais condicional: a rota está validada, com 5 vídeos publicados pela Upload-Post contra 6/6 apagados pela Composio.
- `POST https://api.upload-post.com/api/upload`, header `Authorization: Apikey <chave em /tmp/.upk>`, `async_upload=true`, depois `/uploadposts/status?request_id=`.
- OBRIGATÓRIOS em todo envio: `privacyStatus=public` (nunca unlisted/private), `youtube_subtitle_file` + `youtube_subtitle_language` no longo, `thumbnail_url`, `containsSyntheticMedia=true`, `selfDeclaredMadeForKids=false`, `defaultLanguage`, `defaultAudioLanguage`, `categoryId=27`.
- ANTES de enviar rode `python3 fabrica/tagbudget.py tags.txt`. O limite de 500 chars do YouTube conta tag com espaço entre aspas (len+2); somar só os caracteres aprova lista que o YouTube rejeita.
- Leia tags com `mapfile -t` e grave o arquivo com quebra de linha final.
- PUBLIQUE O SHORT PRIMEIRO, apontando para o longo: em canal frio o feed de Shorts entrega e o de longos não.
- Se a API devolver mensagem específica, esgote essa causa antes de inventar hipótese estrutural — `error_code` e `failure_stage` da Upload-Post são genéricos e não contradizem a mensagem.
- Se o canal não existir no YouTube, entregue no Drive e diga ao Pablo qual canal falta criar.
- NUNCA publique pela Composio `YOUTUBE_UPLOAD_VIDEO`.
- Confira o consumo real em `/uploadposts/history` antes de gastar. Não assuma teto pela documentação antiga: a nota de "10 uploads/mês" não bate com agosto, que fechou 146 publicações.

PASSO 3 — REGISTRO: insert em videos (fonte_pauta, duração real, youtube_id, drive_*, supabase_url, cenas, capítulos) + update canais set ultimo_pacote_em=now(), pacotes=pacotes+1. Uma linha por formato (longo e short separados). Falha → videos.erro com CAUSA e AÇÃO, preservando clipes prontos. Registre views em `metricas`.

PASSO 4 — APRENDA. Ao fim de todo disparo grave: o que quebrou → `aprendizados` com evidência numérica e `aplicado_em`; o que foi palpite → `experimentos`; o que mediu → `pautas_banco`. Regra contrariada vira `status='invalidado'` com motivo, nunca apagada.
NÃO conclua desempenho com menos de 48h de vida. Compare views/dia entre vídeos de idade parecida.

PASSO 5 — ANALISE E TENDÊNCIAS (1x por dia, no primeiro disparo após 06:00 UTC):
- RESULTADOS: colete de TODOS os vídeos publicados e grave snapshot em `metricas`. São DUAS fontes, não uma:
  a) `videos.list part=statistics` (lotes de 50) → views, likes, comments.
  b) **YouTube Analytics API `reports.query`** → `impressions`, `impressionClickThroughRate`, `averageViewPercentage`, `averageViewDuration`. Preencha `impressoes`, `ctr`, `retencao_media_pct` e `duracao_media_s`. Exige escopo `yt-analytics.readonly` na autorização do canal; se o escopo faltar, registre em `aprendizados` como bloqueio e avise o Pablo — não deixe a coluna zerada em silêncio.
  Coletar só (a) é o que zerou CTR e retenção em toda a base: sem esses dois não há como saber que gancho segurou audiência, e o PASSO 4 vira palpite. Compare views/dia entre vídeos de idade parecida do MESMO canal; ganhador/perdedor vira linha em `pautas_banco` (veredito) e, com 48h+ de dados, `aprendizados`.
- OTIMIZE O PRÓXIMO: o que o ganhador fez (estrutura de título, gancho, duração, eixo) entra na spec seguinte do canal; o que o perdedor fez não se repete sem mudança. Registre a decisão em `experimentos` quando for aposta.
- MERCADO/TENDÊNCIAS (rotativo, 1 canal por dia): WebSearch de tendências do nicho no idioma (dores novas datadas, mudanças de lei, datas sazonais próximas) + 1 busca YouTube de outliers da SEMANA (não 90 dias) para capturar ondas cedo. Grave em `pautas_banco` com observacao='tendencia-semanal'.
- PADRÕES DE EXCELÊNCIA (validados 2026-08-11): pattern interrupt nos primeiros 5s (+23% retenção vs abertura estática); loop de retenção a cada 15-30s (pergunta aberta/promessa); estrutura problema→conflito→resolução; CTR e watch time mandam — rosto não. Marcação de IA NÃO reduz alcance nem monetização (política oficial); o risco real é a política de "conteúdo inautêntico" (jul/2025): produção em massa templated sem voz editorial. Antídoto: pesquisa própria com números datados, voz editorial consistente por canal, variedade de formatos. Tração típica: 30-50 uploads; YPP ~12 meses em nicho de retenção alta.

NUNCA criar novos triggers.

Resposta final: canal → título → duração real → fonte da pauta (views/dia) → link do YouTube → links do Drive → "estoque: X/50".
