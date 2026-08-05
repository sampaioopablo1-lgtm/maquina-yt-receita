# APRENDIZADOS

Registro do que a máquina aprendeu — cada regra com a evidência numérica que a sustenta e o
lugar onde ela é aplicada. **A fonte da verdade é a tabela `aprendizados` no Supabase**;
este arquivo é a visão legível, regenerada a partir dela.

```sql
select * from v_maquina_regras;                 -- só as ativas, por severidade
select * from aprendizados where status <> 'ativo';  -- o que já foi invalidado
```

Regra só entra com **evidência numérica** e **`aplicado_em`** preenchido. Regra sem lugar de
aplicação é anotação, não aprendizado. Regra contrariada vira `invalidado` com motivo — nunca
é apagada, porque o histórico do erro é parte do acervo.

Última sincronização: **2026-08-05** · 51 regras ativas, 11 críticas · projeto `vevocauwtarctfwngrch` (`maquina-yt-dark`).

---

## Crítico

### Confirmado 4 de 5: o canal com YouTube configurado foi limpo
Setiap Level (`UCf4-ZFoZQWKJotZNdi4Yl7w`) tem 4 vídeos marcados *Deleted video* e só o short de
26s sobreviveu. Nenhum longo entregue deve ser enviado antes da auditoria.

> 5 vídeos no total, 4 deletados. Sobrevivente: *"3 Kebiasaan Kecil yang Diam-Diam Menghabiskan
> Gajimu"* (26s). Verificado em 2026-08-05.

`aplicado_em:` rotina PASSO 2

### A auditoria da API é o único gargalo real do portfólio
Enquanto `config.api_auditada = false`, a máquina só acumula estoque. Priorizar o formulário de
auditoria acima de qualquer otimização de conteúdo.

> 0 publicados, 0 métricas coletadas, 20 pacotes prontos. Consequência: toda decisão de pauta é
> cega — usa grupo de pares, nunca retenção própria.

`aplicado_em:` `docs/10-auditoria-api.md`

### Visibilidade sempre pública
Todo upload sai com `privacyStatus=public`. Não usar `unlisted` nem `private` em nenhuma
hipótese — vídeo não listado não entra em recomendação, não acumula sinal de algoritmo e não
serve ao objetivo do portfólio. Decisão do dono do canal em 2026-08-05.

> Corrigir retroativamente: `ZYh3bpLP5JE`, `G8ocnpQIiyg`.

`aplicado_em:` `PLAYBOOK.md` + comando de upload

### Tag com espaço custa +2 no orçamento de 500 do YouTube
O limite de 500 caracteres vale para o **conjunto** de tags, e toda tag que contém espaço entra
entre aspas: custa `len(tag)+2`. Somar só os caracteres aprova listas que o YouTube rejeita.
Antes de qualquer envio, rodar `fabrica/tagbudget.py`, que usa limite 480 (500 menos 20 de
margem, porque o arredondamento não é documentado).

> `setiap-level-004`: 22 tags, soma de caracteres 477, custo real **542** — `"One or more tags
> are invalid"`. Depois da poda: 19 tags, custo 451, subiu.

`aplicado_em:` `fabrica/tagbudget.py` + `PLAYBOOK.md`

### A Upload-Post publica de verdade — o upload passou
O caminho existe e funciona. Ainda assim, só tratar como resolvido depois da checagem de 24h: os
6 anteriores também nasceram vivos.

> Canal Setiap Level, `ZYh3bpLP5JE`, `unlisted`, confirmado por `YOUTUBE_GET_VIDEO_DETAILS_BATCH`,
> metadados intactos (título, descrição, 3 tags, categoryId 27, defaultLanguage id). Contraste:
> 6/6 uploads pela Composio viraram *Deleted video*.

`aplicado_em:` rotina PASSO 2

### Rota Upload-Post sobreviveu ao teste de 24h: gargalo da auditoria resolvido para o caminho B
`config.api_auditada` pode virar `true` e a rotina pode retomar publicação pela Upload-Post
(`privacy_status unlisted` no pedido). Continua manual no Studio: thumbnail e o `legendas.srt`.

> `GKQXVoA1zS0`, publicado 04/08 02:41 UTC, checado 33h depois: `uploadStatus=processed`,
> `privacyStatus` pedido `unlisted` → observado `public`, `embeddable=true`, 567 views, 2 likes
> (engajamento orgânico, não placeholder). Fonte: `YOUTUBE_GET_VIDEO_DETAILS_BATCH`, não a
> documentação do serviço. `experimentos.id=4`.

`aplicado_em:` `config.api_auditada` · PLAYBOOK seção 1

### Upload por app de terceiro NÃO AUDITADO é destruição garantida
Nunca publicar por app cujo projeto de API não seja auditado. Antes de confiar em qualquer
terceiro, rodar o teste de sobrevivência de 24h. A auditoria própria segue sendo o caminho
definitivo.

> 6 uploads pela Composio, 6 apagados. Regra do YouTube: projeto de API não auditado criado após
> 28/07/2020 fica restrito a privado, e em canal novo é removido.

`aplicado_em:` rotina PASSO 2

### A regra dos 6/6 é sobre auditoria, não sobre terceiro
Terceiro só entra se o projeto de API dele for auditado. O teste que decide é de sobrevivência:
um vídeo `unlisted`, 24h, conferido por `YOUTUBE_GET_VIDEO_DETAILS_BATCH` — nunca a promessa do
site.

> Composio: projeto não auditado para este uso — 6/6 apagados. Upload-Post: opera a YouTube Data
> API com quota e auditoria próprias; a API expõe `privacy_status: public`, que projeto não
> auditado não conseguiria oferecer. Custo do teste: 1 vídeo dos 21 do estoque.

`aplicado_em:` PLAYBOOK seção 1

### A máquina tem projeto Supabase próprio
O projeto da máquina de vídeo é `vevocauwtarctfwngrch` (`maquina-yt-dark`), região `us-east-1`.
Toda leitura, escrita e entrega usa **este** ref. O projeto antigo `cscczluzpblzhvojxanp`
continua vivo, mas é de um CRM imobiliário — não gravar nada de vídeo lá. Bucket
`videos-maquina`, público para leitura e `anon` só com INSERT.

> Migrado em 2026-08-05: 10 canais, 29 vídeos, 50 aprendizados, 65 pautas, 4 experimentos, 57
> objetos de Storage, 499.338.755 bytes — md5 do manifesto nome:tamanho idêntico nos dois
> projetos. Motivo: as 6 tabelas da máquina eram ilhas em ~150 tabelas de CRM imobiliário.

`aplicado_em:` `PLAYBOOK.md` + `/tmp/.sburl`

### O que vive só no sandbox está perdido
Todo script operacional (`lote.py`, `final.py`, fontes, trilhas) mora no repositório e é
reinstalado por bootstrap. O sandbox é descartável.

> Em risco a cada reciclagem ou OOM: `lote.py`, `final.py`, Noto Sans Devanagari em `~/.fonts`,
> `/tmp/trilhas`.

`aplicado_em:` `fabrica/bootstrap.sh`

### Toda etapa confere a própria saída
Depois de gerar arquivo, comparar a duração real com a esperada e abortar na divergência. Medir a
entrada e reportar como sucesso esconde truncamento.

> Caso 1: concat truncado em 1236,9s de 1715,6s e o log dizia "render ok 1716", porque a soma
> vinha dos tempos medidos antes. Caso 2: parte 2 saiu com 279,6s de 825,5s por clipes ausentes —
> o assert pegou na hora.

`aplicado_em:` `fabrica/etapas.py`

---

## Pauta

### O formato campeão é o sistema completo, não a dica isolada
Estruturar o longo como sistema de 4 pilares num vídeo só (reserva + dívida + investimento +
aposentadoria). Dica única rende uma ordem de grandeza menos.

> `setiap-level`, n=41, mediana do nicho **27 v/d**. Família *sistema completo* (n=2): **4.757,5
> v/d**. Topo: Rory Asyari × Ligwina Hananto, *"Dana Darurat, Investasi, Cicilan & Pensiun"* —
> **9.467 v/d**, 350× a mediana. Segundo lugar: *"Pucuk Asa 4 SISTEM KEUANGAN"* — 48 v/d.

`aplicado_em:` rotina PASSO 0

### O formato morto costuma ser o que o próprio canal já publicou
Medir o formato do vídeo anterior **do próprio canal** contra o grupo de pares antes de escolher
a pauta. Em 5 de 5 canais medidos, ele era o formato morto.

> `agla-level` ensaios motivacionais: 1,4 v/d contra 62,8 do regulatório · `setiap-level` "Gaji X
> juta bisa nabung": mediana 1,3 · `nivel-do-jogo` "A Economia de X": 1–46 · `game-money-lab`
> "The Economics of Owning a X": 0–14 · `resep-naik-level` listas com preço por porção: 1–8.

`aplicado_em:` rotina PASSO 0

### A máquina usou um formato que ela mesma agora mede como morto
Rodar a consulta de veredito em `pautas_banco` **antes** de fechar o título.

> `setiap-level-003` — *"Gaji Harian Rp100 Ribu: Matematika Nyata Menuju Rp100 Juta"*. A família
> *menabung 100 juta* mede **1,0 v/d**. As vizinhas *gaji UMR bisa nabung* (48) e *gaji UMR mau
> kaya* (46) também estão mortas. *Sistema completo* mede 4.757,5.

`aplicado_em:` rotina PASSO 0

### Ensaio motivacional e catastrofista é o piso do nicho
Nunca abrir pauta com colapso/catástrofe/"erros que você comete" sem número datado. Mede o pior
resultado de todas as famílias.

> n=4, mediana **1,0 v/d**. *"Kiamat Finansial 2026"* 10 v/d · *"95% Gagal Kaya di Usia 30an"* 0 ·
> *"Kesalahan Finansial di Usia 20-an"* 0. Repete em hindi no `agla-level`: 1,4 v/d.

`aplicado_em:` rotina PASSO 0

### Conteúdo regulatório datado bate ensaio motivacional em 45×
Em nichos de finanças pessoais, priorizar mudança de regra com data de vigência (lei, alíquota,
prazo) sobre conselho atemporal.

> `agla-level`, n=44: regulatório **62,8 v/d** (n=16) contra motivacional **1,4** (n=28). Outlier:
> StudyIQ IAS, *EPF Scheme 2026*, 2.041,9 v/d. Mediana limpa do nicho: 2,9.

`aplicado_em:` rotina PASSO 0

### Duração só escala onde o nicho já premia duração
Escalonar para 25–30 min apenas com correlação duração × views/dia medida **no grupo de pares**.
Sem essa correlação, ficar em 12–15 min.

> `setiap-level` escalonado: ≥20 min mediana 18,5 v/d (n=5) contra <20 min 0,6 v/d (n=14) — 31×.
> `agla-level` **não** escalonado: outliers vivem entre 3 e 12 min; os dois vídeos de 28 e 31 min
> mediram 61 e 45 v/d contra 2.041,9 do outlier de 8 min.

`aplicado_em:` rotina ESCALONAMENTO

---

## Produção e render

### Medir a taxa de narração da voz antes de dimensionar o roteiro
Rodar `montar()` e medir chars/s da voz do canal antes de fechar a contagem de cenas. As vozes
variam 53% entre si.

> `hi-IN-MadhurNeural` 9,85 · `id-ID-GadisNeural` 11,8 · `pt-BR-AntonioNeural` 13,42 · `en-*` 14,5
> · `id-ID-ArdiNeural` 15,1 — 53% de amplitude no mesmo número de cenas.

`aplicado_em:` rotina PASSO 1

### A taxa da voz depende do texto, não só da voz
Medir chars/s com o mp3 do próprio roteiro depois do `montar()`, nunca reaproveitar a taxa de
outro pacote. Número escrito por extenso arrasta a locução.

> `id-ID-ArdiNeural`: taxa registrada 15,1, medida neste roteiro 13,72 (-9,1%, roteiro denso em
> número por extenso). Estimativa dizia 26,1 min; a real deu 28,6 min — ainda dentro da faixa
> 25–30, mas 15% de erro na direção errada estouraria.

`aplicado_em:` rotina PASSO 1

### A taxa da voz cai em roteiro denso em número por extenso
Dimensionar a spec para a taxa **mais lenta** plausível, não para a medida no pacote anterior.
Podar antes de renderizar custa minutos; refazer o render custa uma hora.

> `id-ID-ArdiNeural`: -9,1% (registrada 15,1, medida 13,72). `es-MX-DaliaNeural`: -5,9% (13,82 →
> 13,0). Com as 98 cenas originais o vídeo daria 15,5 min, fora da faixa 12–15; podado para 91
> cenas, saiu em 14:24.

`aplicado_em:` rotina PASSO 1

### Script sem fonte instalada falha em silêncio
Toda spec em script não-latino declara `"fonte"`, e `usar_fonte()` confere no `fc-list`. Sem a
checagem, o SVG cai num fallback e a legenda queimada sai **vazia**, sem erro nenhum.

> Devanágari: `cairosvg` desenhava glifos soltos (halant visível, matra do lado errado); `libass`
> não renderizava nada — 0 pixels. Depois da correção: `क्ष` caiu de 187px (3 glifos soltos) para
> 161px (ligadura correta); legenda passou de 0 para 2.390 pixels escuros. Risco residual: a
> fonte vive em `~/.fonts` do sandbox e morre quando ele recicla.

`aplicado_em:` `fabrica.py usar_fonte()`

### Legenda queimada só no short
No longo, entregar `legendas.srt` para subir no Studio em vez de queimar. Queimada rouba área
útil e bloqueia a legenda própria do YouTube, que traduz e é indexada.

> Vantagem sobre a automática: erra número e nome próprio, justamente onde este formato se apoia.
> Fonte do srt: tempos dos clipes renderizados, casa ao milissegundo com o vídeo final. Efeito
> colateral bom: o longo deixa de depender do `libass` para scripts não-latinos.

`aplicado_em:` `fabrica.py render()`

### Capítulo tem que ser medido no clipe, nunca no mp3
Os tempos de capítulo vêm de `dur(lclipNN.mp4)`. Medir pelo mp3 ignora a folga entre cenas e
desalinha o vídeo inteiro.

> Causa: tempos vinham de `mp3 + 0,5` mas `-shortest` cortava o clipe no tamanho cru do mp3.
> Deriva de ~23s, afetou todos os pacotes anteriores à correção. Remover o `-shortest` devolveu a
> folga e a duração subiu de 11:52 para 12:16.

`aplicado_em:` `fabrica.py render()`

### Download que falha vira arquivo HTML que passa em toda checagem
Validar duração (>30s) de todo asset baixado, não só existência e tamanho. Um 404 salvo em disco
tem bytes e extensão certos.

> `Cipher.mp3` com 3,2 KB de HTML de um 404. Quebrou no passo da trilha, depois de 74 clipes
> renderizados.

`aplicado_em:` `fabrica.py trilha_ok()`

### O tmpfs mora na RAM e o concat inteiro não cabe
Concatenar pacote longo em duas metades, liberando os clipes da primeira antes de codificar a
segunda. A junção final é `-c copy`, quase de graça.

> tmpfs 493 MB (shared na RAM), 196 clipes = 390 MB, máquina com 985 MB de RAM. O pan novo faz
> todo quadro mudar, então o x264 perdeu o desconto de quadros quase idênticos: ffmpeg a 36% de
> CPU escrevendo 0,26 MB a cada 50s. Depois da divisão: 6 MB/min, ~23× mais rápido.

`aplicado_em:` `fabrica/etapas.py` + `metades.py`

### O Ken Burns não movia: era zoom puro, sem pan
`zoompan` precisa de x e y variando no tempo. Com x/y no centro sobra só o zoom, e 7% em 10s é
imperceptível — o vídeo lê como imagem parada e a retenção paga.

> Antes: `AMP_ZOOM 0,07` sem pan (`x`/`y` constantes). Depois: `AMP_ZOOM 0,12` + pan em 4 direções
> alternadas, percorrendo só 50% da margem aberta pelo zoom (100% cortaria até 11% de um lado).
> PSNR entre quadro 0 e 85 da mesma cena caiu de 25,3 dB para 21,9 dB — ~2× mais mudança de pixel
> por segundo.

`aplicado_em:` `fabrica.py ken_burns()`

### "O arquivo parou de crescer" não é sinal de que o processo terminou
Liberar espaço só depois que o subprocess retorna. Nunca inferir conclusão observando tamanho de
arquivo: a escrita do ffmpeg é em rajadas e a pausa parece fim.

> Um faxineiro em background apagava `lclip*.mp4` quando `video.mp4` ficava a 8s do mesmo
> tamanho. Os 196 clipes sumiram no meio do concat; o vídeo saiu com 1236,9s em vez de 1716s —
> 28% faltando, incluindo o capítulo final e o CTA. O log dizia "render ok 1716" porque a soma
> vinha dos tempos medidos antes da limpeza. Custo: ~25 min de refazer TTS + 196 clipes + concat.

`aplicado_em:` `fabrica/etapas.py`

### Dois pacotes do mesmo canal dividiam o diretório de trabalho
A spec declara "pacote" e o diretório de trabalho vem dele. O "slug" continua sendo o do canal
porque é ele que escolhe a trilha.

> Defeito: `d = /tmp/f/<slug>` usava o slug do **canal**, então `setiap-level-003` e `004`
> gravavam na mesma pasta. Consequência: o RETOMA pula clipes que já existem — o concat costura
> dois roteiros diferentes num vídeo só, sem erro nenhum. Não estourou por sorte, não por guarda.

`aplicado_em:` `fabrica.py dir_trabalho()`

### A cena de CTA invertia a cor e lia como erro
Nenhum layout inverte fundo e texto. O CTA usa a identidade do canal com cor de destaque no
kicker.

> Defeito: `if lay == cta: bg = ink` — fundo escuro com texto branco nas 3 últimas cenas de todo
> vídeo, com `sub_fg` `#FFFFFF` sumindo no fundo claro. Depois da correção, brilho médio do CTA
> 253, igual às demais cenas (254).

`aplicado_em:` `fabrica.py svg_cena()`

### A checagem do RETOMA vem antes de medir o mp3
Em `render()`, conferir se o clipe já existe **antes** de medir o mp3. Os lotes apagam png/mp3
consumidos para caber no tmpfs de 493 MB.

> Sintoma: `render()` quebrava em `dur(l00.mp3)` num clipe que já estava pronto.

`aplicado_em:` `fabrica.py render()`

### Glob de limpeza precisa ser ancorado no prefixo exato
Apagar por padrão explícito (`lclip*.mp4`, `l[0-9][0-9].png`) e nunca por `l*.<ext>`. O curinga
largo pegou `legendas.srt` junto com os srt de cena.

> Defeito: `rm -f $d/l*.srt` apagou `legendas.srt`, o entregável — porque também começa com "l".
> Correção: a legenda agora é escrita numa etapa própria e nenhuma limpeza usa curinga de uma
> letra.

`aplicado_em:` `fabrica/etapas.py`

### O teto de 50 MB do Supabase manda no encode de vídeo longo
Acima de ~18 min: áudio 128k e CRF 29.

> 57 MB em 25:44 (recusado pelo upload padrão) → 49,95 MB só com CRF 29 (perto demais do teto de
> 50 MB) → **42,7 MB** com áudio 128k. A 192k o áudio sozinho passava de 37 MB.

`aplicado_em:` `fabrica.py` concat

---

## Entrega

### A API da Upload-Post cobre thumbnail e legenda
Enviar `thumbnail_url` e `youtube_subtitle_file` na mesma chamada. Também aceita
`containsSyntheticMedia`, `defaultLanguage`, `categoryId` e `playlist`.

> Correção de: registro anterior dizia que thumbnail e SRT ficariam manuais no Studio — errado.
> O pacote inteiro sobe numa chamada só, sem passo manual.

`aplicado_em:` PLAYBOOK seção 1

### `GOOGLEDRIVE_UPLOAD_FROM_URL` ignora o parent
Todo upload cai na raiz do Drive. Sempre seguir com `GOOGLEDRIVE_MOVE_FILE` (`add_parents` +
`remove_parents` + `supports_all_drives`) na mesma sequência.

> Raiz: `0AL8gANwo3v7jUk9PVA`. Risco: pacote fica órfão na raiz se a sequência for interrompida —
> aconteceu em todos os uploads até agora.

`aplicado_em:` rotina PASSO 2

### Base do Storage vem de arquivo, nunca digitada
O ref do projeto tem "L" minúsculo, homóglifo de "1" em fonte de terminal, e o bucket é
`videos-maquina`, não `videos`. A base fica em `/tmp/.sburl` e é sempre lida de lá.

> Sintomas de digitar errado: *"Video URL is not allowed"* do upload-post, DNS sem resolução,
> *"Bucket not found"* via HTTP 400 — nenhum aponta para erro de digitação.

`aplicado_em:` `/tmp/.sburl` + `PLAYBOOK.md`

### Caminho do Storage precisa do número do pacote
Nomear como `AAAA-MM-DD-<slug>-<seq>-<artefato>`. Só a data colide quando o mesmo canal entrega
dois pacotes no mesmo dia.

> Erro: **409 Duplicate** em `2026-08-05-agla-level-video.mp4`, mesmo canal, mesmo dia. Também:
> omitir `x-upsert: true` — a policy anon é INSERT-only e upsert dá 403.

`aplicado_em:` rotina PASSO 2

### Transferência por heredoc corrompe acima de ~1.400 bytes
Mandar arquivo grande pro sandbox em gzip+base64 fatiado, com md5 por pedaço. Conferir com
`tr -d '\n' | md5sum` para descontar a quebra de linha do heredoc.

> Falhou a 2.300 bytes (chunk `m004`, md5 divergente); resolvido em pedaços de 700 bytes. Limite
> observado: 1.400 a 2.300 bytes.

`aplicado_em:` rotina PASSO 1

---

## Processo

### As 4 views `v_maquina_*` rodavam SECURITY DEFINER e vazavam para `anon`
Toda view criada sobre tabela com RLS restrita a `service_role` precisa de
`with (security_invoker=true)` explícito na criação — sem isso a view roda com o privilégio de
quem criou e ignora a RLS, e o schema padrão do Supabase concede SELECT a `anon`/`authenticated`
em toda tabela/view nova por default.

> Views: `v_maquina_fila`, `v_maquina_estoque`, `v_maquina_regras`, `v_maquina_formatos`.
> Achado por: Supabase advisor security (nível ERROR: `security_definer_view`). Confirmado:
> `select as anon` retornava linhas de `canais`/`videos`/`aprendizados`/`pautas_banco` antes do
> fix, 0 linhas depois. Corrigido em produção 2026-08-05; versionado em `supabase/schema.sql`
> nesta rotina.

`aplicado_em:` `supabase/schema.sql` (views) + migration `v_maquina_views_security_invoker`

### PRs de continuidade acumulam sem merge — reaproveitar por cherry-pick, nunca recriar do zero
Antes de refazer um fix "do zero", medir se ele já existe numa branch/PR aberta e não mergeada.
Se o commit for isolado e não tocar arquivos alterados depois na trunk, cherry-pick direto — mais
seguro que reescrever, e evita a pilha de PRs redundantes crescer.

> Causa raiz: cada sessão de continuidade recriava os mesmos 3 fixes do zero (RLS leak,
> `pendente()`, `ffmpeg_bin`) porque a PR anterior não tinha sido mergeada, e branches antigas
> divergiam da trunk o suficiente para o diff parecer destrutivo. PRs #18–#23 propuseram o mesmo
> escopo sem nenhuma mergeada. Ação: cherry-pick de commit isolado e já testado direto para a
> trunk.

`aplicado_em:` rotina do disparador automático

### O jsonb vira lixeira e mata a agregação
Todo dado que vai ser comparado entre pacotes mora em coluna, não em `roteiro` jsonb. O jsonb
guarda só o que é narrativo.

> Achado: `videos` não tinha coluna de canal — impossível juntar com `canais`. Chaves divergentes:
> `drive_video` vs `entrega.video`, `similaridade_vs_video1` vs `similaridade_vs_anteriores` vs
> `fonte_pauta.similaridade_vs_anterior`. Nenhum aprendizado era computável por SQL.

`aplicado_em:` schema `videos`

### Registro gravado antes da entrega cria pacote fantasma
PASSO 3 só roda depois de PASSO 2 confirmar os artefatos no Drive. Registro sem `drive_video` é
um pacote que não existe, e ele infla o estoque.

> Caso: `epomeno-1000e-odigos-20260805` + short registrados em 05/08 02:04 com duração 729s e
> 25s. Verificação: sem diretório no sandbox, sem spec 002 no repo nem no sandbox, zero objetos
> no Storage com prefixo `epomeno`. Passou despercebido porque `status=listado_para_publicacao` é
> igual ao dos pacotes bons — só o `drive_video` nulo denunciava.

`aplicado_em:` rotina PASSO 3

### Mensagem de erro literal antes de hipótese estrutural
Quando a API devolve mensagem específica (*"One or more tags are invalid"*), esgotar essa causa
antes de inventar hipótese estrutural. O `error_code` e o `failure_stage` da Upload-Post são
genéricos (`media_invalid_format` / `media_validation`) e não contradizem a mensagem.

> Causa real: orçamento de tags. Regra falsa gerada e depois invalidada: nº 43 ("canal não
> verificado não aceita vídeo acima de 15 min"). Custo: 2 envios desperdiçados e uma regra falsa.

`aplicado_em:` `PLAYBOOK.md`

### Postgres do Supabase é alcançável direto por MCP
`mcp__Supabase__execute_sql` roda SQL no projeto sem passar pelo sandbox e sem a chave anon. Isso
contorna dois limites que vinham custando tempo: o proxy deste ambiente bloqueia `supabase.co`, e
a chave anon só permite INSERT (o endpoint list do Storage volta vazio).

> Ganho: leitura de `storage.objects` e UPDATE, ambos impossíveis pela anon. Substitui: curl com
> chave anon pelo sandbox Composio.

`aplicado_em:` `PLAYBOOK.md`

### Sem métrica própria o laço de aprendizado fica pela metade
Priorizar qualquer rota que devolva métrica do canal. Enquanto `métricas` estiver vazia, toda
decisão de pauta usa só grupo de pares e nenhum experimento fecha.

> Rota possível: `upload-post /analytics/<perfil>` cobre YouTube. 0 métricas coletadas, 3
> experimentos abertos. O que não dá pra responder: retenção por formato, CTR por estilo de
> thumbnail, se o zoom+pan segurou mais que o zoom parado, se o srt bate a legenda queimada.

`aplicado_em:` PLAYBOOK seção 6

### Log de sucesso pode mentir se a medição vem antes do efeito
Toda etapa que produz arquivo confere o próprio resultado antes de declarar ok. Medir a entrada e
reportar como se fosse a saída esconde exatamente as falhas que importam.

> Caso: "render ok 1716" impresso a partir da soma dos clipes, enquanto o vídeo concatenado tinha
> 1236,9s. Regra prática: `assert abs(duracao_da_saida - soma_das_entradas) < 5`.

`aplicado_em:` `fabrica/etapas.py`

### Existe disco de verdade fora do tmpfs
`/mnt/files` é s3fs (64P). Arquivo grande que não está em uso imediato vai para lá em vez de
disputar RAM com o ffmpeg.

> Descoberta: `df -h /mnt/files` → s3fs 64P. Cuidado: é preciso trazer de volta antes do passo que
> lê os arquivos — não fiz isso e a parte 2 saiu com 279s em vez de 825s. Efeito medido: mover 66
> clipes liberou 113 MB de tmpfs e a RAM disponível subiu de 14 para 54 MB.

`aplicado_em:` rotina PASSO 1

### Pesquisa do PASSO 0 tem que virar acervo
Gravar cada medição de par em `pautas_banco`, inclusive as ruins.

> Sem isso, cada disparo remede o mesmo grupo do zero e nunca se vê um formato morrer ao longo do
> tempo.

`aplicado_em:` rotina PASSO 0

### Migração entre projetos passa por `pg_net`, não pelo contexto
Para mover linhas entre dois projetos Supabase, a origem faz `net.http_post` para o PostgREST do
destino com `jsonb_agg(to_jsonb(t))`. Os dados nunca entram no contexto do agente. A extensão
`http` não está disponível (só `pg_net`, assíncrono): a resposta é conferida depois em
`net._http_response` por id. Objetos de Storage vão por script retomável no sandbox, um arquivo
por vez, porque o tmpfs de 493 MB mora na RAM.

> 476 MB, lotes de 14+15+14+4+10, 57 objetos, 6 tabelas, 42s para os vídeos longos, 90 KB
> evitados no contexto do agente.

`aplicado_em:` `PLAYBOOK.md`

### O proxy do ambiente bloqueia `supabase.co` na saída
A spec vai pro sandbox em gzip+base64 fatiado com md5 por pedaço. Não tentar subir do ambiente do
agente pro Storage: o caminho é sandbox → Supabase, nunca o inverso.

> Erro: `curl exit 56`, HTTP 000, host `cscczluzpblzhvojxanp.supabase.co:443`, proxy respondeu 403
> ao CONNECT (policy denial). O Supabase MCP funciona porque usa outro canal. Transferência OK:
> 13 pedaços de 1.200 bytes, md5 final idêntico ao arquivo local.

`aplicado_em:` rotina PASSO 1

### Trilha por hash faz canais soarem iguais
Fixar a trilha em `canais.trilha`. O sorteio por hash do slug colocou 4 canais na mesma faixa.

> 10 canais, biblioteca de 4 faixas. *Inspired*: `epomeno-epipedo`, `cocina-por-niveles`,
> `nivel-do-jogo`, `agla-level`. *Wholesome*: `kolejny-poziom`, `seviye-seviye`, `game-money-lab`,
> `setiap-level`.

`aplicado_em:` `canais.trilha`

### `while read` engole a última linha sem quebra final
Ao ler lista de arquivo em bash, garantir a quebra final ou usar `mapfile`. Foram 21 de 22 tags
sem ninguém notar.

> Causa: `read` retorna falso na última linha sem newline e o corpo do laço não roda. Sintoma:
> contagem 21 quando o arquivo tinha 22 tags. Correção: gravar o arquivo com newline final, ou
> usar `mapfile -t`.

`aplicado_em:` rotina PASSO 2

---

## Invalidado

### ~~Canal não verificado não aceita vídeo acima de 15 minutos~~ (regra 43)
Refutada por contraexemplo direto: `setiap-level-003` (1544,5s = 25min44) subiu como
`G8ocnpQIiyg` pelo mesmo canal não verificado. A causa real do erro em `setiap-level-004` era o
orçamento de tags, não a duração. O erro `media_invalid_format` / `media_validation` é genérico e
a mensagem `"One or more tags are invalid"` era literal — a mensagem certa foi descartada em
favor da hipótese errada.
