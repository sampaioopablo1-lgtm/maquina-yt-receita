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
sinal de algoritmo — é vídeo produzido para não ser visto.

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
