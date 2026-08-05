# A rotina horária — texto atual

> Este é o prompt que o Pablo cola a cada disparo. Vive aqui para não ser
> reconstruído de memória: quando o processo muda, muda **aqui e no PLAYBOOK
> junto**, e a regra correspondente entra em `aprendizados`.
>
> Última revisão: 2026-08-05.

---

Rotina horária da máquina de vídeos. UM PACOTE POR VEZ, do início ao fim.

Supabase: projeto **vevocauwtarctfwngrch** (maquina-yt-dark). O projeto antigo cscczluzpblzhvojxanp é de um CRM imobiliário — NÃO gravar nada de vídeo lá.

ANTES DE TUDO: leia PLAYBOOK.md e rode `select * from v_maquina_regras where severidade in ('critico','alto')`. O PLAYBOOK descreve como a máquina opera hoje; `aprendizados` é a fonte da verdade.

SANDBOX: ele recicla sem aviso e leva junto a fábrica, as dependências e as chaves. Recupere com `curl` do `fabrica.tgz` no bucket + `tar -xzf` + `pip install edge-tts cairosvg`, e **confira os md5 de fabrica/*.py contra o repositório** — o Storage é INSERT-only, então um tar velho lá dentro não é sobrescrito e você baixaria a versão errada sem erro nenhum. Cópia desatualizada já produziu vídeo costurando dois roteiros sem levantar erro.

REGRA MESTRA: um único canal por disparo, completo (longo + short + thumbnail + copy + legendas), com entrega incremental. Só comece outro canal se o primeiro estiver 100% entregue E PUBLICADO.

DURAÇÃO DO LONGO — 12 a 15 minutos (70-90 cenas), 6-8 capítulos de 10-14 cenas, micro-gancho na abertura e ponte no fim. NUNCA abaixo de 8 min.
DIMENSIONE PELA FÓRMULA, não pela tabela de chars/s: `duração = chars/20,58 + frases × 0,96 + cenas × 1,08` (id-ID-ArdiNeural). A pausa entre frases domina — o ritmo que o linter exige ALONGA o vídeo. A tabela de chars/s erra até 21%.
ESCALONAMENTO: canal com retenção acima de 40% ou views/vídeo acima da mediana do nicho sobe para 25-30 min; registre em config.

FILA: 1) `select * from v_maquina_pendencias limit 1` — só mostra erro com artefato recuperável. 2) senão `select * from v_maquina_fila limit 1` — ela já põe canal com YouTube primeiro e expõe `pode_produzir` com o teto de 3 pacotes/dia descontado. Produzir para canal que não existe engorda estoque que não embarca.

PASSO 0 — DEMANDA: consulte `v_maquina_formatos` e `pautas_banco` ANTES de pesquisar. Depois, via YOUTUBE_SEARCH_YOU_TUBE + YOUTUBE_GET_VIDEO_DETAILS_BATCH, colete vídeos de 90 dias do nicho/idioma, calcule VIEWS/DIA, mediana e outliers (≥3×). Grave TUDO em pautas_banco, inclusive os mortos.
- PESQUISE PELOS CANAIS DO NICHO, não por termos amplos. Medido em `07-pesquisa-subnicho.md`: busca por termo cai em cluster curto e repetitivo; partir de 5-10 canais concorrentes e varrer o catálogo deles dá sinal muito melhor. Guarde o CANAL (link, idioma, nicho, mediana de v/d, formato dominante), não só o vídeo — é o canal que se acompanha ao longo dos disparos. Confirme números com WebSearch no idioma e em fonte institucional — duas fontes que batam.
- Pauta = (formato que performa) × (dor real datada) × (eixo não usado). Similaridade ≤0,65 vs vídeos anteriores do MESMO canal.
- O título modela a ESTRUTURA do outlier, nunca o assunto; keyword nos 5 primeiros termos.
- NÚMERO EXATO VENCE NÚMERO REDONDO. Quando a fonte der precisão, não arredonde — nem na narração nem no título. E nunca invente precisão que a fonte não tem.
- A transcrição do YouTube está BLOQUEADA (IP de nuvem) e o filtro `channelId` do search é IGNORADO. Não insista em nenhum dos dois.

PASSO 1 — PRODUÇÃO (sandbox Composio; fábrica em fabrica/):
- `python3 etapas.py <spec.json>` — etapas sequenciais, cada uma confere a própria saída. A etapa 0 roda o linter de narração ANTES do TTS e derruba o build em erro.
- Nenhuma trava pega TROCA DE IDIOMA. Releia a narração inteira no idioma do canal antes de renderizar — o linter mede ritmo e número, não idioma, e o TTS leria português com voz indonésia sem nenhum erro.
- Números por extenso, sem dígitos crus.
- As cenas do longo entram em CAMADAS (base + uma por elemento). `-framerate 30` em CADA imagem, senão sai a 25 fps e o concat mistura sem reclamar.
- SHORT 9:16, 30-45s: ARCO COMPLETO, não recorte do longo. Estado A → mecanismo → estado B → só então o CTA. Ele fecha sozinho e depois aponta.
- TRILHA: trilha_do_canal(), -28 dB, crédito no copy.md.
- Áudio loudnorm I=-14 TP=-1.5, estéreo 48kHz, +faststart. Legenda queimada só no short; o longo exporta legendas.srt.
- thumbnail 1280x720 (máx 3 palavras) + copy.md no idioma do canal: título ≤100c, descrição 200+ palavras com capítulos cronometrados REAIS, CTA, disclosure de conteúdo sintético, 3 hashtags, 15 tags, comentário fixado.

PASSO 2 — ENTREGA. Do sandbox, para cada artefato:
  ANON="<chave anon do maquina-yt-dark>"
  curl -s -X POST "https://vevocauwtarctfwngrch.supabase.co/storage/v1/object/videos-maquina/<AAAA-MM-DD>-<pacote>-<arquivo>" -H "Authorization: Bearer $ANON" -H "apikey: $ANON" -H "Content-Type: <mime>" --data-binary @<arquivo> --max-time 240
Não mande x-upsert. A URL base vem de `/tmp/.sburl`, nunca digitada — o `l` do ref é homóglifo de `1`. Depois GOOGLEDRIVE_UPLOAD_FROM_URL (campo obrigatório é `name`) + GOOGLEDRIVE_MOVE_FILE.

PASSO 2B — PUBLIQUE. **Confira /uploadposts/history ANTES de renderizar**, não depois: o plano grátis dá 10 envios/mês e cada pacote custa dois. Sem cota, produza e entregue sem publicar.
  POST https://api.upload-post.com/api/upload, header `Authorization: Apikey <chave em /tmp/.upk>`, `async_upload=true`, depois `/uploadposts/status?request_id=`.
  OBRIGATÓRIOS: `privacyStatus=public`, `youtube_subtitle_file` + `youtube_subtitle_language` no longo, `thumbnail_url`, `containsSyntheticMedia=true`, `selfDeclaredMadeForKids=false`, `defaultLanguage`, `defaultAudioLanguage`, `categoryId=27`.
  ANTES de enviar rode `python3 fabrica/tagbudget.py tags.txt` — tag com espaço conta entre aspas (len+2). Leia com `mapfile -t` e grave com quebra de linha final.
  PUBLIQUE O SHORT PRIMEIRO, apontando para o longo: em canal frio o feed de Shorts entrega e o de longos não.
  Se a API devolver mensagem específica, esgote essa causa antes de inventar hipótese estrutural.
  NUNCA publique pela Composio YOUTUBE_UPLOAD_VIDEO.
  NÃO procure contorno em onde o código roda (Colab, Supabase, auto-hospedado): a trava é do PROJETO da API. A saída é a auditoria — texto pronto em docs/18-submissao-auditoria.md.

PASSO 3 — REGISTRO: insert em videos (fonte_pauta, duração real, youtube_id, drive_*, supabase_url, cenas, capítulos) + update canais. Uma linha por formato. Falha → videos.erro com CAUSA e AÇÃO, preservando clipes prontos. Registre views em `metricas`.

PASSO 4 — APRENDA. Ao fim de todo disparo grave: o que quebrou → `aprendizados` com evidência numérica e `aplicado_em`; o que foi palpite → `experimentos`; o que mediu → `pautas_banco`. Regra contrariada vira `status='invalidado'` com motivo, nunca apagada.
NÃO conclua desempenho com menos de 48h. Compare views/dia entre vídeos de idade parecida.

NUNCA criar novos triggers.

Resposta final: canal → título → duração real → fonte da pauta (views/dia) → link do YouTube → links do Drive → "estoque: X/50".
