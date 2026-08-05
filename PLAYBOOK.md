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
select * from v_maquina_formatos where canal = '<slug>';                -- o que performa nele
```

`v_maquina_fila` já ordena por *canal com YouTube configurado primeiro*, depois por
`ultimo_pacote_em` mais antigo. `v_maquina_formatos` é a memória da pesquisa: mostra a
mediana de views/dia por família de formato, acumulada ao longo das semanas.

---

## 1. O gargalo, declarado

**Faltam 9 canais no YouTube.** Só `setiap-level` (`@setiaplevelid`) existe. É a única
coisa nesta lista que a máquina não consegue fazer sozinha, e ela bloqueia 10 dos 12
pacotes prontos — em polonês, grego, turco, espanhol, hindi, português e inglês, todos
sem destino. Cada canal leva ~2 min no Studio.

A publicação em si **deixou de ser gargalo em 2026-08-05.** Três vídeos subiram pela
Upload-Post e sobreviveram ao nascimento, contra 6/6 apagados pela Composio.

| | duração | id |
|---|---|---|
| short do 004 | 0:26 | `ZYh3bpLP5JE` |
| setiap-level-003 | 25:44 | `G8ocnpQIiyg` |
| setiap-level-004 | 28:35 | `v-5v7R13BBc` |

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
**gratuita**, leva semanas e não é garantida.

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

O título modela a **estrutura** do outlier, nunca o assunto. Palavra-chave nos 5 primeiros termos.

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

---

## 3. Produção — o que quebra em silêncio

Estes três já entregaram vídeo defeituoso sem levantar erro nenhum:

| Armadilha | Sintoma | Guarda hoje |
|---|---|---|
| Fonte sem o script do idioma | legenda queimada **vazia**, texto sem shaping | `usar_fonte()` confere no `fc-list` e quebra alto |
| Capítulo medido no mp3 | deriva de ~23s no vídeo inteiro | tempos vêm de `dur(lclipNN.mp4)` |
| Download que falhou | HTML salvo como `.mp3` passa em tamanho e extensão | `trilha_ok()` mede duração > 30s |

**Meça a taxa da voz antes de dimensionar o roteiro.** Elas variam 53%:

| Voz | chars/s |
|---|---|
| `hi-IN-MadhurNeural` | 9,85 |
| `id-ID-GadisNeural` | 11,8 |
| `pt-BR-AntonioNeural` | 13,42 |
| `en-*` | 14,5 |
| `id-ID-ArdiNeural` | 15,1 |

Limites do sandbox: tmpfs **493 MB**, RAM ~985 MB, bash **180s por comando**. Renderize em
lotes de 10 cenas apagando png/mp3 consumidos. Acima de ~18 min: áudio 128k e CRF 29, senão
estoura o teto de 50 MB do Storage.

---

## 4. Entrega

```
sandbox curl → Supabase Storage → GOOGLEDRIVE_UPLOAD_FROM_URL → GOOGLEDRIVE_MOVE_FILE
```

- **`GOOGLEDRIVE_UPLOAD_FROM_URL` ignora o parent.** Tudo cai na raiz `0AL8gANwo3v7jUk9PVA`.
  O `MOVE_FILE` não é opcional — sem ele o pacote fica órfão.
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
OAuth concedido não inclui YouTube Analytics. Sem impressão, CTR e retenção, a view
`painel_pilares` não classifica gargalo nenhum, e todo diagnóstico se apoia só em views
públicas. Isso só se resolve com escopo próprio, o que depende da auditoria.

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
