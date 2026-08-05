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

Última sincronização: **2026-08-05** · 22 regras ativas, 4 críticas.

---

## Crítico

### Upload por app de terceiro é destruição garantida
**Nunca** publicar via `YOUTUBE_UPLOAD_VIDEO` do Composio ou qualquer app de terceiro. Só a
API própria, com projeto auditado e OAuth do dono.

> 6 uploads, 6 apagados. No Setiap Level, 4 de 5 vídeos aparecem como *"Deleted video"* — o
> único sobrevivente entrou por outro caminho. Regra do YouTube: projeto de API não auditado
> criado após 28/07/2020 fica restrito a privado, e em canal novo é removido.

`aplicado_em:` rotina PASSO 2

### A auditoria da API é o único gargalo real do portfólio
Enquanto `config.api_auditada = 'false'`, a máquina só acumula estoque.

> 20 pacotes prontos, 0 publicados, 0 métricas coletadas. Consequência: toda decisão de pauta
> é cega — usa grupo de pares, nunca retenção própria.

`aplicado_em:` `docs/10-auditoria-api.md` · depende de ação humana

### O que vive só no sandbox está perdido
Todo script operacional mora no repositório e é reinstalado por bootstrap.

> Em risco hoje: `lote.py`, `final.py`, a Noto Sans Devanagari em `~/.fonts`, as trilhas em
> `/tmp/trilhas`. Gatilho: reciclagem do sandbox ou OOM.

`aplicado_em:` `fabrica/bootstrap.sh`

---

## Pauta

### O formato campeão é o sistema completo, não a dica isolada
Estruturar o longo como sistema de 4 pilares num vídeo só (reserva + dívida + investimento +
aposentadoria). Dica única rende uma ordem de grandeza menos.

> Setiap Level, n=41, mediana do nicho **27 v/d**. Família *sistema completo*: **4.757 v/d**.
> Topo: Rory Asyari × Ligwina Hananto, *"Dana Darurat, Investasi, Cicilan & Pensiun"* —
> **9.467 v/d**, 350× a mediana.

`aplicado_em:` rotina PASSO 0

### O formato morto costuma ser o que o próprio canal já publicou
Medir o formato do vídeo anterior **do próprio canal** contra o grupo de pares antes de
escolher a pauta. Em 6 de 6 canais medidos, ele era o formato morto.

> `game-money-lab` "The Economics of Owning a X": 0–14 v/d · `nivel-do-jogo` "A Economia de X":
> 1–46 · `resep-naik-level` listas com preço por porção: 1–8 · `setiap-level`
> "Gaji X juta bisa nabung": 1,3 · `agla-level` ensaios motivacionais: 1,4 contra 62,8 do
> regulatório.

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

> `setiap-level` escalonado: ≥20 min mediana 18,5 v/d (n=5) contra <20 min 0,6 (n=14) — 31×.
> `agla-level` **não** escalonado: outliers vivem entre 3 e 12 min, e os dois vídeos de 28 e
> 31 min mediram 61 e 45 v/d contra 2.041 do outlier de 8 min.

`aplicado_em:` rotina ESCALONAMENTO

---

## Produção e render

### Medir a taxa de narração da voz antes de dimensionar o roteiro
Rodar `montar()` e medir chars/s antes de fechar a contagem de cenas.

> 9,85 (`hi-IN-MadhurNeural`) · 11,8 (`id-ID-GadisNeural`) · 13,42 (`pt-BR`) · 14,5 (`en`) ·
> 15,1 (`id-ID-ArdiNeural`). Amplitude de **53%** no mesmo número de cenas.

`aplicado_em:` rotina PASSO 1

### Script sem fonte instalada falha em silêncio
Toda spec em script não-latino declara `"fonte"`, e `usar_fonte()` confere no `fc-list`.

> Sem a checagem o SVG cai num fallback e a legenda queimada sai **vazia**, sem erro. Em
> devanágari o cairosvg desenhava glifos soltos (halant visível, matra do lado errado) e o
> libass não renderizava nada — 0 pixels. Depois da correção: `क्ष` caiu de 187px (3 glifos)
> para 161px (ligadura correta) e a legenda passou de 0 para 2.390 pixels escuros.
> **Risco residual:** a fonte vive em `~/.fonts` do sandbox e morre com ele.

`aplicado_em:` `fabrica.py usar_fonte()`

### Capítulo tem que ser medido no clipe, nunca no mp3
Os tempos vêm de `dur(lclipNN.mp4)`.

> Deriva de ~23s. Os tempos vinham de `mp3 + 0,5` mas o `-shortest` cortava o clipe no tamanho
> cru do mp3. Remover o `-shortest` devolveu a folga entre cenas e a duração subiu de 11:52
> para 12:16. Afetou **todos** os pacotes anteriores à correção.

`aplicado_em:` `fabrica.py render()`

### Download que falha vira arquivo que passa em toda checagem
Validar duração (> 30s) de todo asset baixado, não só existência e tamanho.

> `Cipher.mp3` com 3,2 KB de HTML de um 404. Quebrou no passo da trilha, **depois** de 74
> clipes renderizados.

`aplicado_em:` `fabrica.py trilha_ok()`

### O teto de 50 MB do Storage manda no encode do vídeo longo
Acima de ~18 min: áudio 128k e CRF 29.

> 57 MB em 25:44 (recusado) → 49,95 MB só com CRF 29 (perto demais) → **42,7 MB** com áudio
> 128k. A 192k o áudio sozinho passava de 37 MB.

`aplicado_em:` `fabrica.py` concat

### A checagem do RETOMA vem antes de medir o mp3
Os lotes apagam png/mp3 consumidos para caber no tmpfs de 493 MB.

> `render()` quebrava em `dur(l00.mp3)` num clipe que já estava pronto.

`aplicado_em:` `fabrica.py render()`

---

## Entrega

### `GOOGLEDRIVE_UPLOAD_FROM_URL` ignora o parent
Todo upload cai na raiz `0AL8gANwo3v7jUk9PVA`. O `GOOGLEDRIVE_MOVE_FILE`
(`add_parents` + `remove_parents` + `supports_all_drives`) faz parte da mesma sequência.

> Aconteceu em todos os pacotes. Se a sequência é interrompida, o pacote fica órfão na raiz.

`aplicado_em:` rotina PASSO 2

### O caminho no Storage precisa do número do pacote
`AAAA-MM-DD-<slug>-<seq>-<artefato>`.

> **409 Duplicate** em `2026-08-05-agla-level-video.mp4` porque o mesmo canal já tinha entregue
> naquele dia. E: omitir `x-upsert: true` — a policy anon é INSERT-only e upsert dá 403.

`aplicado_em:` rotina PASSO 2

### Heredoc corrompe acima de ~1.400 bytes
Arquivo grande vai para o sandbox em gzip+base64 fatiado, com md5 por pedaço.

> Falhou a 2.300 bytes (chunk `m004`, md5 divergente); resolvido em pedaços de 700 bytes.
> Conferir com `tr -d '\n' | md5sum` para descontar a quebra de linha do heredoc.

`aplicado_em:` rotina PASSO 1

---

## Processo

### O jsonb vira lixeira e mata a agregação
Todo dado que vai ser comparado entre pacotes mora em **coluna**. O jsonb guarda só o narrativo.

> `videos` não tinha coluna de canal — era impossível juntar com `canais`. As chaves divergiam
> entre pacotes: `drive_video` vs `entrega.video`, `similaridade_vs_video1` vs
> `similaridade_vs_anteriores` vs `fonte_pauta.similaridade_vs_anterior`. Nenhum aprendizado
> era computável por SQL.

`aplicado_em:` schema `videos`

### A pesquisa do PASSO 0 tem que virar acervo
Gravar cada medição de par em `pautas_banco`, inclusive as ruins.

> Sem isso cada disparo remede o mesmo grupo do zero, e nunca se vê um formato morrer ao
> longo do tempo.

`aplicado_em:` rotina PASSO 0

### Trilha por hash faz canais soarem iguais
Fixar a trilha em `canais.trilha`.

> O sorteio por hash do slug pôs 4 canais em *Inspired* (`epomeno-epipedo`, `cocina-por-niveles`,
> `nivel-do-jogo`, `agla-level`) e 4 em *Wholesome* (`kolejny-poziom`, `seviye-seviye`,
> `game-money-lab`, `setiap-level`). Biblioteca de 4 faixas para 10 canais.

`aplicado_em:` `canais.trilha`
