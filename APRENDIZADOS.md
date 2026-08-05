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

Última sincronização: **2026-08-05** · 41 regras ativas (7 críticas, 25 altas, 9 médias).

---

## Crítico

### A auditoria da API é o único gargalo real do portfólio — RESOLVIDO 05/08/2026
Priorizar o formulário de auditoria (caminho A) acima de qualquer otimização de conteúdo
**deixou de ser necessário para publicar**: o caminho B (Upload-Post) foi confirmado abaixo.

> 20 pacotes prontos, 0 publicados, 0 métricas coletadas antes da resolução. `config.api_auditada`
> virou `true` em 05/08 12:04 UTC.

`aplicado_em:` `docs/10-auditoria-api.md` · `config.api_auditada`

### Rota Upload-Post sobreviveu ao teste de 24h: gargalo da auditoria resolvido para o caminho B
`config.api_auditada` pode virar `true` e a rotina pode retomar publicação pela Upload-Post
(`privacy_status: unlisted` no pedido). Continua manual no Studio: thumbnail e `legendas.srt`.

> `GKQXVoA1zS0` (`setiap-level`), publicado 04/08 02:41 UTC, checado 05/08 12:00 UTC — **33h**
> depois: `uploadStatus=processed`, `privacyStatus=public` (pedido como `unlisted`, o YouTube
> tornou `public` — o oposto do que um projeto não auditado faria), `embeddable=true`, 567
> views e 2 likes orgânicos, via `YOUTUBE_GET_VIDEO_DETAILS_BATCH` (nunca a documentação do
> serviço). `experimentos.id=4` concluído.

`aplicado_em:` `config.api_auditada` · PLAYBOOK seção 1

### A regra dos 6/6 é sobre auditoria, não sobre terceiro
Terceiro só entra se o projeto de API dele for auditado. O teste que decide é de sobrevivência:
um vídeo unlisted, 24h, conferido por `YOUTUBE_GET_VIDEO_DETAILS_BATCH` — nunca a promessa do site.

> Composio: projeto não auditado para este uso — 6 de 6 apagados. Upload-Post: opera a YouTube
> Data API com quota e auditoria próprias; a API expõe `privacy_status: public`, que projeto não
> auditado não conseguiria oferecer. Regra do YouTube: projeto criado após 28/07/2020 sem
> auditoria de compliance só sobe vídeo privado, e em canal novo ele é removido.

`aplicado_em:` PLAYBOOK seção 1

### Upload por app de terceiro NÃO AUDITADO é destruição garantida
**Nunca** publicar via `YOUTUBE_UPLOAD_VIDEO` do Composio ou qualquer app cujo projeto de API
não seja auditado. Antes de confiar em qualquer terceiro, rodar o teste de sobrevivência de 24h.

> 6 uploads, 6 apagados. No Setiap Level, 4 de 5 vídeos aparecem como *"Deleted video"* — o
> único sobrevivente entrou por outro caminho (Upload-Post, auditado). Regra do YouTube:
> projeto de API não auditado criado após 28/07/2020 fica restrito a privado, e em canal novo
> é removido.

`aplicado_em:` rotina PASSO 2

### Confirmado 4 de 5: o canal com YouTube configurado foi limpo
Nenhum longo entregue deve ser enviado por app não auditado antes da auditoria.

> Setiap Level (`UCf4-ZFoZQWKJotZNdi4Yl7w`) tem 4 vídeos marcados *"Deleted video"* e só o
> short de 26s sobreviveu — o único enviado por caminho auditado. Verificado em 05/08/2026.

`aplicado_em:` rotina PASSO 2

### O que vive só no sandbox está perdido
Todo script operacional (`lote.py`, `final.py`, fontes, trilhas) mora no repositório e é
reinstalado por bootstrap. O sandbox é descartável.

> Em risco: `lote.py`, `final.py`, a Noto Sans Devanagari em `~/.fonts`, as trilhas em
> `/tmp/trilhas`. Gatilho: reciclagem do sandbox ou OOM.

`aplicado_em:` `fabrica/bootstrap.sh`

### Toda etapa confere a própria saída
Depois de gerar arquivo, comparar a duração real com a esperada e abortar na divergência.
Medir a entrada e reportar como sucesso esconde truncamento.

> Caso 1: concat truncado em 1236,9s de 1715,6s e o log dizia "render ok 1716", porque a soma
> vinha dos tempos medidos antes da limpeza. Caso 2: parte 2 saiu com 279,6s de 825,5s por
> clipes ausentes — o assert pegou na hora. Regra derivada: limpeza usa padrão ancorado —
> `l*.srt` levou junto o `legendas.srt`, que era entregável.

`aplicado_em:` `fabrica/etapas.py`

---

## Pauta

### O formato campeão é o sistema completo, não a dica isolada
Estruturar o longo como sistema de 4 pilares num vídeo só (reserva + dívida + investimento +
aposentadoria). Dica única rende uma ordem de grandeza menos.

> Setiap Level, n=41, mediana do nicho **27 v/d**. Família *sistema completo*: **4.757,5 v/d**.
> Topo: Rory Asyari × Ligwina Hananto, *"Dana Darurat, Investasi, Cicilan & Pensiun"* —
> **9.467 v/d**, 350× a mediana. Segundo lugar: *4 SISTEM KEUANGAN* — 48 v/d.

`aplicado_em:` rotina PASSO 0

### O formato morto costuma ser o que o próprio canal já publicou
Medir o formato do vídeo anterior **do próprio canal** contra o grupo de pares antes de
escolher a pauta. Em 5 de 5 canais medidos, era o formato morto.

> `agla_level` ensaios motivacionais: 1,4 v/d contra 62,8 do regulatório · `setiap_level`
> "Gaji X juta bisa nabung": mediana 1,3 v/d · `nivel_do_jogo` "A Economia de X": 1–46 v/d ·
> `game_money_lab` "The Economics of Owning a X": 0–14 v/d · `resep_naik_level` listas com
> preço por porção: 1–8 v/d.

`aplicado_em:` rotina PASSO 0

### A máquina usou um formato que ela mesma agora mede como morto
Rodar a consulta de veredito em `pautas_banco` **antes** de fechar o título.

> `setiap-level-003` — *"Gaji Harian Rp100 Ribu: Matematika Nyata Menuju Rp100 Juta"*. A família
> *menabung 100 juta* mede **1,0 v/d**. As vizinhas *gaji UMR bisa nabung* (48) e *gaji UMR mau
> kaya* (46) também estão mortas. *Sistema completo* mede 4.757.

`aplicado_em:` rotina PASSO 0 · achado por auditoria retroativa

### Ensaio motivacional e catastrofista é o piso do nicho
Nunca abrir pauta com colapso / catástrofe / "erros que você comete" sem número datado.

> n=4, mediana **1,0 v/d**. *"Kiamat Finansial 2026"* 10 v/d · *"95% Gagal Kaya di Usia 30an"*
> 0 · *"Kesalahan Finansial di Usia 20-an"* 0. O mesmo padrão se repete em hindi no
> `agla-level`: 1,4 v/d.

`aplicado_em:` rotina PASSO 0

### Conteúdo regulatório datado bate ensaio motivacional em 45×
Priorizar mudança de regra com data de vigência (lei, alíquota, prazo) sobre conselho atemporal.

> `agla-level`: regulatório **62,8 v/d** (n=16) contra motivacional **1,4** (n=28). Outlier:
> StudyIQ IAS, *EPF Scheme 2026*, 2.041,9 v/d. Mediana limpa do nicho: 2,9 (n=44).

`aplicado_em:` rotina PASSO 0

### Duração só escala onde o nicho já premia duração
Escalonar para 25–30 min apenas com correlação duração × views/dia medida **no grupo de pares**.
Sem essa correlação, ficar em 12–15 min.

> `setiap_level` escalonado: ≥20 min mediana 18,5 v/d (n=5) contra <20 min 0,6 v/d (n=14) — 31×.
> `agla_level` **não** escalonado: outliers vivem entre 3 e 12 min, e os dois vídeos de 28 e
> 31 min mediram 61 e 45 v/d contra 2.041 do outlier de 8 min.

`aplicado_em:` rotina ESCALONAMENTO

---

## Produção e render

### Medir a taxa de narração da voz antes de dimensionar o roteiro
Rodar `montar()` e medir chars/s da voz do canal antes de fechar a contagem de cenas. As vozes
variam 53% entre si.

> 9,85 (`hi-IN-MadhurNeural`) · 11,8 (`id-ID-GadisNeural`) · 13,42 (`pt-BR`) · 14,5 (`en`) ·
> 15,1 (`id-ID-ArdiNeural`). Amplitude de **53%** no mesmo número de cenas.

`aplicado_em:` rotina PASSO 1

### A taxa da voz depende do texto, não só da voz
Medir chars/s com o mp3 do próprio roteiro depois do `montar`, nunca reaproveitar a taxa de
outro pacote. Número escrito por extenso arrasta a locução.

> Voz `id-ID-ArdiNeural`, roteiro denso em número por extenso (*dua ribu dua puluh enam, lima
> koma tujuh persen*): desvio de **-9,1%** — estimativa dizia 26,1 min, a real deu 28,6 min.
> Ainda dentro da faixa escalonada de 25-30, mas com 15% de erro na direção errada estouraria.

`aplicado_em:` rotina PASSO 1

### A taxa da voz cai em roteiro denso em número por extenso
Dimensionar a spec para a taxa MAIS LENTA plausível, não para a medida no pacote anterior.
Podar antes de renderizar custa minutos; refazer o render custa uma hora.

> `id-ID-ArdiNeural`: queda de -9,1% (13,72 medida vs 15,1 registrada) — com as 98 cenas
> originais o vídeo daria 15,5 min, fora da faixa de 12-15; podado para 91 saiu em 14:24.
> `es-MX-DaliaNeural`: queda de -5,9% (13,0 vs 13,82 do pacote anterior).

`aplicado_em:` rotina PASSO 1

### Script sem fonte instalada falha em silêncio
Toda spec em script não-latino declara `"fonte"`, e `usar_fonte()` confere no `fc-list`. Sem a
checagem, o SVG cai num fallback e a legenda queimada sai **vazia**, sem erro.

> Caso hindi/devanágari: libass não renderizava nada — 0 pixels de legenda; cairosvg desenhava
> glifos soltos (halant visível, matra do lado errado). Depois da correção: `क्ष` caiu de 187px
> (3 glifos soltos) para 161px (ligadura correta); legenda passou de 0 para 2.390 pixels
> escuros. **Risco residual:** a fonte vive em `~/.fonts` do sandbox e morre quando ele recicla.

`aplicado_em:` `fabrica.py usar_fonte()`

### "O arquivo parou de crescer" não é sinal de que o processo terminou
Liberar espaço só DEPOIS que o subprocess retorna. Nunca inferir conclusão observando tamanho
de arquivo: a escrita do ffmpeg é em rajadas e a pausa parece fim.

> Um faxineiro em background apagava `lclip*.mp4` quando `video.mp4` ficava a 8s do tamanho
> esperado — os 196 clipes sumiram no meio do concat e o vídeo saiu com 1236,9s em vez de
> 1716s (28% faltando, incluindo capítulo final e CTA), mas o log dizia "render ok 1716" porque
> a soma vinha dos tempos medidos ANTES da limpeza. Custo: ~25 min de refazer TTS + 196 clipes +
> concat. Correção: `etapas.py` só limpa depois do subprocess retornar, com assert de que a
> duração do concat bate com a soma dos clipes.

`aplicado_em:` `fabrica/etapas.py`

### Capítulo tem que ser medido no clipe, nunca no mp3
Os tempos de capítulo vêm de `dur(lclipNN.mp4)`. Medir pelo mp3 ignora a folga entre cenas e
desalinha o vídeo inteiro.

> Tempos vinham de `mp3 + 0,5` mas o `-shortest` cortava o clipe no tamanho cru do mp3 — deriva
> de ~23s, afetando todos os pacotes anteriores à correção. Remover o `-shortest` devolveu a
> folga de 0,5s e a duração subiu de 11:52 para 12:16.

`aplicado_em:` `fabrica.py render()`

### Dois pacotes do mesmo canal dividiam o diretório de trabalho
A spec declara `"pacote"` e o diretório de trabalho vem dele. O `"slug"` continua sendo o do
canal porque é ele que escolhe a trilha.

> Defeito: `d = /tmp/f/<slug>` usava o slug do CANAL, então `setiap-level-003` e `004`
> gravavam na mesma pasta — o RETOMA pula clipes que já existem, sobrando `lclip` do pacote
> anterior, e o concat costura dois roteiros diferentes num vídeo só, sem erro nenhum. Detectado
> em conferência manual antes do render do 004; não estourou antes por sorte (clipes do 003 já
> tinham sido apagados na entrega em lotes).

`aplicado_em:` `fabrica.py dir_trabalho()`

### Download que falha vira arquivo HTML que passa em toda checagem
Validar duração (>30s) de todo asset baixado, não só existência e tamanho. Um 404 salvo em
disco tem bytes e extensão certos.

> `Cipher.mp3` com 3,2 KB de HTML de um 404 — quebrou no passo da trilha, **depois** de 74
> clipes renderizados.

`aplicado_em:` `fabrica.py trilha_ok()`

### O Ken Burns não movia: era zoom puro, sem pan
`zoompan` precisa de x e y variando no tempo. Com x/y no centro sobra só o zoom, e 7% em 10s é
imperceptível — o vídeo lê como imagem parada e a retenção paga.

> Defeito: `x=iw/2-(iw/zoom/2)` e `y=ih/2-(ih/zoom/2)` são constantes. Antes: `AMP_ZOOM 0.07`
> sem pan. Depois: `AMP_ZOOM 0.12` + pan em 4 direções alternadas (limitado a 50% da margem
> aberta pelo zoom, para não cortar até 11% de um lado). PSNR entre quadro 0 e 85 na mesma cena
> caiu de 25,3 dB para 21,9 dB = ~2× mais mudança de pixel por segundo.

`aplicado_em:` `fabrica.py ken_burns()`

### O tmpfs mora na RAM e o concat inteiro não cabe
Concatenar pacote longo em duas metades, liberando os clipes da primeira antes de codificar a
segunda. A junção final é `-c copy`, quase de graça.

> tmpfs de 493 MB (contabilizado como shared na RAM) para 196 clipes = 390 MB, numa máquina de
> 985 MB — ffmpeg a 36% de CPU escrevendo 0,26 MB a cada 50s (horas de encode); o pan novo faz
> todo quadro mudar, então o x264 perdeu o desconto de quadros quase idênticos. Depois da
> divisão: 6 MB/min, ~23× mais rápido.

`aplicado_em:` `fabrica/etapas.py` + `metades.py`

### Legenda queimada só no short
No longo, entregar `legendas.srt` para subir no Studio em vez de queimar. Queimada rouba área
útil e bloqueia a legenda própria do YouTube, que traduz e é indexada.

> Fonte do srt: tempos dos clipes renderizados, casa ao milissegundo com o vídeo final — melhor
> que a legenda automática, que erra número e nome próprio, justamente onde este formato se
> apoia. Efeito colateral bom: o longo deixa de depender do libass para scripts não-latinos.

`aplicado_em:` `fabrica.py render()`

### A cena de CTA invertia a cor e lia como erro
Nenhum layout inverte fundo e texto. O CTA usa a identidade do canal com cor de destaque no
kicker.

> Defeito: `if lay == cta: bg = ink` — fundo escuro com texto branco nas 3 últimas cenas de todo
> vídeo, e `sub_fg` era `#FFFFFF` (sumiria no fundo claro depois da correção). A virada de cor
> no fim era percebida como defeito de render, não como cartão de encerramento. Depois: brilho
> médio do CTA 253, igual às demais cenas (254).

`aplicado_em:` `fabrica.py svg_cena()`

### A checagem do RETOMA vem antes de medir o mp3
Em `render()`, conferir se o clipe já existe ANTES de medir o mp3. Os lotes apagam png/mp3
consumidos para caber no tmpfs de 493 MB.

> `render()` quebrava em `dur(l00.mp3)` num clipe que já estava pronto (RAM ~985 MB).

`aplicado_em:` `fabrica.py render()`

### Glob de limpeza precisa ser ancorado no prefixo exato
Apagar por padrão explícito (`lclip*.mp4`, `l[0-9][0-9].png`) e nunca por `l*.<ext>`. O curinga
largo pegou `legendas.srt` junto com os srt de cena.

> Defeito: `rm -f $d/l*.srt` apagou `legendas.srt`, o entregável — porque `legendas.srt` também
> começa com `l`. Correção: a legenda agora é escrita numa etapa própria e nenhuma limpeza usa
> curinga de uma letra.

`aplicado_em:` `fabrica/etapas.py`

### O teto de 50 MB do Storage manda no encode do vídeo longo
Acima de ~18 min: áudio 128k e CRF 29.

> 57 MB em 25:44 (recusado pelo upload padrão, limite 50 MB) → 49,95 MB só com CRF 29 (perto
> demais) → **42,7 MB** com áudio 128k. A 192k o áudio sozinho passava de 37 MB.

`aplicado_em:` `fabrica.py` concat

---

## Entrega

### `GOOGLEDRIVE_UPLOAD_FROM_URL` ignora o parent
Todo upload cai na raiz do Drive (`0AL8gANwo3v7jUk9PVA`). O `GOOGLEDRIVE_MOVE_FILE`
(`add_parents` + `remove_parents` + `supports_all_drives`) faz parte da mesma sequência.

> Aconteceu em todos os uploads até agora. Se a sequência é interrompida, o pacote fica órfão
> na raiz.

`aplicado_em:` rotina PASSO 2

### O caminho no Storage precisa do número do pacote
Nomear como `AAAA-MM-DD-<slug>-<seq>-<artefato>`. Só a data colide quando o mesmo canal entrega
dois pacotes no mesmo dia.

> **409 Duplicate** em `2026-08-05-agla-level-video.mp4` porque o mesmo canal já tinha entregue
> naquele dia. E: omitir `x-upsert: true` — a policy anon é INSERT-only e upsert dá 403.

`aplicado_em:` rotina PASSO 2

### Transferência por heredoc corrompe acima de ~1.400 bytes
Mandar arquivo grande para o sandbox em gzip+base64 fatiado, com md5 por pedaço. Conferir com
`tr -d '\n' | md5sum` para descontar a quebra de linha do heredoc.

> Falhou a 2.300 bytes (chunk `m004`, md5 divergente); resolvido em pedaços de 700 bytes.

`aplicado_em:` rotina PASSO 1

---

## Processo

### As 4 views `v_maquina_*` rodavam SECURITY DEFINER e vazavam para anon
Toda view criada sobre tabela com RLS restrita a `service_role` precisa de
`with (security_invoker=true)` explícito na criação — sem isso a view roda com o privilégio de
quem criou e ignora a RLS, e o schema padrão do Supabase concede SELECT a anon/authenticated em
toda tabela/view nova por padrão.

> Achado pelo Supabase Advisor (nível ERROR: `security_definer_view`) em `v_maquina_fila`,
> `v_maquina_estoque`, `v_maquina_regras`, `v_maquina_formatos`. Confirmado: `select` como
> `anon` retornava linhas de canais/vídeos/aprendizados/pautas_banco antes do fix; 0 linhas
> depois. Corrigido em produção e **versionado em `supabase/schema.sql` pela primeira vez** —
> essas views (e `painel_pilares`/`progresso_ypp`, que tinham o mesmo problema) nunca tinham
> estado no arquivo. Gap relacionado: as tabelas-base `canais`/`aprendizados`/`pautas_banco`/
> `experimentos` foram criadas direto em produção por sessões anteriores e continuam fora do
> schema.sql — reaplicar o arquivo do zero não recria essas views porque as tabelas não existem
> nele; as definições servem para manter as views versionadas, não para reconstruir o banco.

`aplicado_em:` `supabase/schema.sql` (views)

### PRs de continuidade acumulam sem merge — reaproveitar por cherry-pick, nunca recriar do zero
Antes de refazer um fix "do zero", medir se ele já existe numa branch/PR aberta e não
mergeada. Se o commit for isolado e não tocar arquivos alterados depois na trunk, cherry-pick
direto — mais seguro que reescrever, e evita que a pilha de PRs redundantes cresça.

> Causa raiz: cada sessão de continuidade recriava os mesmos 3 fixes do zero (vazamento de RLS,
> `pendente()`, `ffmpeg_bin()`) porque a PR anterior não tinha sido mergeada, e branches antigas
> divergiam da trunk o suficiente para o diff parecer destrutivo. Ação: cherry-pick de 2
> commits isolados e já testados (`7e1f56e` do PR #20, `b7b41b4` do PR #21) direto para a trunk
> atual, sem conflito (`git diff` entre merge-base e HEAD nos arquivos tocados veio vazio).
> Resultado: 55/55 testes. PRs #18, #19, #20, #21 seguem abertas como draft e precisam ser
> fechadas manualmente pelo humano — o conteúdo útil delas já foi incorporado nesta sessão.

`aplicado_em:` rotina do disparador automático · PR desta sessão

### Existe disco de verdade fora do tmpfs
`/mnt/files` é s3fs (64P). Arquivo grande que não está em uso imediato vai para lá em vez de
disputar RAM com o ffmpeg.

> Descoberta: `df -h /mnt/files` → s3fs 64P. Cuidado: é preciso trazer de volta antes do passo
> que lê os arquivos — não fiz isso e a parte 2 saiu com 279s em vez de 825s. Depois: mover 66
> clipes liberou 113 MB de tmpfs e a RAM disponível subiu de 14 para 54 MB.

`aplicado_em:` rotina PASSO 1

### Log de sucesso pode mentir se a medição vem antes do efeito
Toda etapa que produz arquivo confere o próprio resultado antes de declarar ok. Medir a entrada
e reportar como se fosse a saída esconde exatamente as falhas que importam.

> "render ok 1716" impresso a partir da soma dos clipes, enquanto o vídeo concatenado tinha
> 1236,9s. Regra prática: `assert abs(duracao_da_saida - soma_das_entradas) < 5`.

`aplicado_em:` `fabrica/etapas.py`

### O jsonb vira lixeira e mata a agregação
Todo dado que vai ser comparado entre pacotes mora em **coluna**, não em `roteiro` jsonb. O
jsonb guarda só o narrativo.

> `videos` não tinha coluna de canal — impossível juntar com `canais`. Chaves divergentes entre
> pacotes: `drive_video` vs `entrega.video`, `similaridade_vs_video1` vs
> `similaridade_vs_anteriores` vs `fonte_pauta.similaridade_vs_anterior`. Nenhum aprendizado era
> computável por SQL.

`aplicado_em:` schema `videos`

### A pesquisa do PASSO 0 tem que virar acervo
Gravar cada medição de par em `pautas_banco`, inclusive as ruins.

> Sem isso cada disparo remede o mesmo grupo do zero, e nunca se vê um formato morrer ao longo
> do tempo — perda da série histórica de views/dia por formato.

`aplicado_em:` rotina PASSO 0

### Registro gravado antes da entrega cria pacote fantasma
PASSO 3 só roda depois de PASSO 2 confirmar os artefatos no Drive. Registro sem `drive_video` é
um pacote que não existe, e ele infla o estoque.

> `epomeno-1000e-odigos-20260805` + short registrados em 05/08 02:04 com duração 729s e 25s, mas
> sem diretório no sandbox, sem spec 002 no repo nem no sandbox, zero objetos no Storage com
> prefixo `epomeno` — estoque contava 22 pacotes, um deles nunca existiu. Passou despercebido
> porque o `status` era igual ao dos pacotes bons; só o `drive_video` nulo denunciava. Resolvido
> 05/08: substituído por `epomeno-epipedo-002` no mesmo canal.

`aplicado_em:` rotina PASSO 3

### Sem métrica própria o laço de aprendizado fica pela metade
Priorizar qualquer rota que devolva métrica do canal. Enquanto `metricas` estiver vazia, toda
decisão de pauta usa só grupo de pares e nenhum experimento fecha.

> Rota disponível: `upload-post /analytics/<perfil>` cobre YouTube. Com `metricas` vazia e 3
> experimentos abertos, não dá para responder: retenção por formato, CTR por estilo de
> thumbnail, se o zoom+pan segurou mais que o zoom parado, se o srt bate a legenda queimada.

`aplicado_em:` PLAYBOOK seção 6

### O proxy do ambiente bloqueia supabase.co na saída
O caminho é sandbox → Supabase, nunca o inverso — não tente subir do ambiente do agente para o
Storage.

> `curl` do agente para `cscczluzpblzhvojxanp.supabase.co:443` deu exit 56 / HTTP 000 (gateway
> respondeu 403 ao CONNECT, política de bloqueio). O Supabase MCP funciona porque usa outro
> canal. Do sandbox, a transferência funciona: 13 pedaços de 1.200 bytes, md5 final idêntico ao
> arquivo local.

`aplicado_em:` rotina PASSO 1

### Trilha por hash faz canais soarem iguais
Fixar a trilha em `canais.trilha`.

> O sorteio por hash do slug pôs 4 canais em *Inspired* (`epomeno-epipedo`, `cocina-por-niveles`,
> `nivel-do-jogo`, `agla-level`) e 4 em *Wholesome* (`kolejny-poziom`, `seviye-seviye`,
> `game-money-lab`, `setiap-level`). Biblioteca de 4 faixas para 10 canais.

`aplicado_em:` `canais.trilha`
