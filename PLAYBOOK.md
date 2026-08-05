# PLAYBOOK — o documento central da máquina

> **Este arquivo é lido no início de todo disparo da rotina, antes de qualquer produção.**
> Ele descreve como a máquina opera *hoje*. Quando o processo mudar, muda aqui — junto
> com a regra correspondente em `aprendizados` no Supabase. Documento e banco andam juntos.

Projeto Supabase: `cscczluzpblzhvojxanp` · Bucket: `videos-maquina` · Repositório: este.

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

**`config.api_auditada = 'false'`.** Enquanto isso não virar `true`, nada é publicado e
a máquina só acumula estoque. Todas as decisões de pauta são cegas — usam grupo de pares,
nunca retenção própria, porque `metricas` está vazia.

Evidência de que não há atalho: o único canal configurado no YouTube
(`setiap-level`, `UCf4-ZFoZQWKJotZNdi4Yl7w`) tem **4 de 5 vídeos marcados "Deleted video"**.
Os 4 subiram por app de terceiro. O sobrevivente não.

Há dois caminhos para sair disso, e eles não competem:

**A — auditoria própria** (`docs/10-auditoria-api.md`). Depende de ação humana:
formulário + criação dos canais no Studio. É o caminho definitivo — projeto próprio,
sem intermediário, sem mensalidade, sem depender da política de ninguém.

**B — Upload-Post** (skill em `.claude/skills/upload-post/`). Serviço que opera a
YouTube Data API com **quota e auditoria próprias**, então dispensa projeto no Google
Cloud. A API expõe `privacy_status: public` — e um projeto **não** auditado não
consegue publicar público, o YouTube força privado. É evidência forte, não prova.

> **A regra dos 6/6 continua valendo até ser refutada com dado.** Ela não diz
> "nenhum terceiro"; diz "nenhum terceiro **não auditado**". A Composio derrubou
> 6 de 6 porque o projeto dela não era auditado para este uso. Se o da Upload-Post
> é, o resultado muda — mas isso se decide medindo, não lendo o site deles.

**Teste de sobrevivência, obrigatório antes de confiar em B:** subir UM vídeo como
`unlisted`, esperar 24h, conferir com `YOUTUBE_GET_VIDEO_DETAILS_BATCH`. Sobreviveu →
`config.api_auditada='true'` e o caminho abre. Sumiu → registra o resultado em
`aprendizados`, volta ao Drive, e A vira a única rota. Custa um vídeo do estoque de 21.

O que o B ainda **não** cobre e continua manual no Studio: thumbnail (não há parâmetro
de thumbnail para YouTube na API) e o `legendas.srt`.

O que o B destrava de imediato, e é o motivo real de valer o teste: o endpoint
`/analytics/<perfil>` devolve métrica do YouTube. Hoje a tabela `metricas` está vazia
e **toda decisão de pauta é cega** — sem retenção própria, o laço de aprendizado só
tem grupo de pares. Com métrica entrando, os 3 experimentos abertos fecham.

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

- Publicar por app de terceiro (6/6 apagados).
- Criar triggers novos.
- Longo abaixo de 8 minutos.
- Escalonar duração sem correlação medida no grupo de pares.
- Fechar um pacote com arquivo parado na raiz do Drive.
