# A divergencia MEDIDA entre o prompt armazenado e docs/ROTINA.md

Gerado em 12/10/2026, lendo o prompt vivo com `get_trigger` do trigger
`trig_01Y6ZvwsrbxteyS933sgzqK4` e comparando com o corpo de `docs/ROTINA.md`
depois da linha `---`.

POR QUE ESTE ARQUIVO EXISTE. A rotina manda, no seu §3.6, sincronizar o prompt
armazenado sempre que o arquivo andar na frente, e da o caminho barato: editar
`docs/ROTINA.md`, extrair o corpo e passar ESSE texto como `prompt`. Eu venho
relatando a divergencia por varias rodadas sem executa-la, e relatar sem numero
nao e relato. Entao aqui esta o numero: as duas versoes diferem em
**95 linhas de diff**, concentradas em **cinco blocos**, e nenhuma delas e
contradicao -- sao adicoes do arquivo que o prompt ainda nao tem.

OS CINCO BLOCOS:
 1. pauta (a) -> (a-2): com o banco em 402 a fonte e `pauta-viva.yml`, nao o
    retrato de 06/10; o filtro do `corpus_publicados.json`; contar por TITULO
    DISTINTO;
 2. regra (h) mecanizada: `capitulos.yml`, e a metade que faltava -- a descricao
    da so o TITULO do capitulo, e o texto sai da faixa de legenda;
 3. a linha de base da suite, agora medida nesta sessao;
 4. a narracao JA TEM plano B em producao (`voz_piper.py`), com o custo do R/P;
 5. o `mcp__github__*` SE recupera -- retratacao da retratacao.

O QUE EU **NAO** FIZ, e vai dito em vez de ficar implicito: eu nao chamei
`update_trigger`. O motivo nao e permissao -- e que passar 60 mil caracteres por
parametro de ferramenta significa eu os reemitir a mao, e reemitir a mao e
exatamente o mecanismo que produziu os erros que este arquivo documenta. Os
cinco blocos ja estao no `CLAUDE.md`, que e relido a cada rodada, entao o custo
de a divergencia continuar e baixo. **Quando a sincronia acontecer, ela e uma
colagem mecanica deste corpo, e depois se confere com `get_trigger`.**

```diff
--- prompt ARMAZENADO no trigger (lido com get_trigger em 12/10 13:1x)
+++ docs/ROTINA.md (corpo depois da linha ---)
@@ -358,2 +358,14 @@
      **e nunca o número que estiver escrito aqui**: ele envelhece a cada publicação;
+  a-2) **com o banco em 402 a consulta não roda, e a fonte é `pauta-viva.yml`**
+     (`fabrica/pauta_viva.py`), que lê a PLAYLIST DE UPLOADS pela API — viva, sem
+     banco e sem retrato. **RETRATAÇÃO de 12/10:** eu reconstruía pelo retrato
+     `fabrica/ponte/videos.json`, de 06/10, escrevi a ressalva certa e tratei o
+     número como estoque por três rodadas, anunciando "a pauta acabou". O vivo
+     achou TRÊS onde o retrato dizia uma. O `pauta_local.py` fica como PISO.
+     **O vivo só conta longo cujo título está no `corpus_publicados.json`:** sem
+     esse filtro ele devolveu 65 "origens" no labtreinamento que eram as AULAS DE
+     CURSO DO DONO (668 na forma de pauta).
+     **Conte por TÍTULO DISTINTO, nunca por id** — em 12/10 eu errei a mesma
+     conta três vezes (cinco → três → dois) porque dez ids eram dez cópias de um
+     título, e uma delas era cópia de origem já consumida;
   b) PRIMEIRO ÂNGULO de longo virgem;
@@ -376,2 +388,9 @@
      pela `videos.list`** — isso não é motivo para trocar de origem.
+     **MECANIZADO EM 12/10, e com a metade que faltava:** `capitulos.yml` →
+     `fabrica/capitulos_do_longo.py`. E o que faltava é decisivo — **a descrição
+     dá só o TÍTULO do capítulo, nunca o que ele afirma**. Escrever a partir de
+     título de capítulo é INVENTAR conteúdo. O texto sai da faixa de **legenda**
+     que a própria máquina subiu (`legenda=true`), preferindo a faixa NÃO
+     automática. Foi assim que o `eZ697VNYCPU` virou pauta: 75 falas, 9.249
+     caracteres, e nenhuma frase do short inferida de título.
 **AO PUBLICAR, GRAVE `videos.origem_id`** com o `longo_existente` da spec (670).
@@ -492,3 +511,6 @@
   `FAILED` para comparar depois — o número escrito aqui envelhece, o CONJUNTO
-  não. Em 11/10: **25 falham, 2.103 passam** (passa/skip sobem com teste novo).
+  não. Em 12/10, medido nesta sessão às 12:5x: **25 falham, 2.234 passam,
+  475 skip** — e o CONJUNTO das 25 é o que importa, porque passam/skip sobem com
+  teste novo. A frase anterior desta linha trazia o parêntese DUAS vezes e um
+  `~2.205` estimado; os dois eram descuido meu de edição.
   **E a composição NÃO é "título duplicado e Devanagari" — eu escrevi isso e
@@ -513,5 +535,18 @@
   outra rodada em 09/10. Recuperado com `git stash pop`, mas foi erro meu.
-- **A NARRAÇÃO TEM FORNECEDOR ÚNICO** e isso é um buraco conhecido:
-  `edge_tts.Communicate` em `fabrica.py:598`. Não instale costura de plano B sem
-  um segundo provedor de verdade — costura vazia só adiciona risco.
+- **A NARRAÇÃO JÁ TEM PLANO B, E ELE ESTÁ EM PRODUÇÃO — 12/10.** A frase antiga
+  aqui dizia "fornecedor único ... não instale costura de plano B sem um segundo
+  provedor de verdade". A condição foi cumprida: o `edge_tts` passou a dar **403
+  no handshake DO RUNNER** (runs 38198672898 e 38202568056, versão 7.2.8, duas
+  vozes) e a máquina parou de produzir em qualquer lugar. `fabrica/voz_piper.py`
+  é provedor de verdade — neural, offline, sem chave — e entra **só depois das
+  três tentativas do edge-tts**, para a frota voltar sozinha à voz original
+  quando ele voltar.
+  **O QUE ISSO CUSTA, e vai no relato de toda peça:** o `R` e o `P` de
+  `MODELO_VOZ` são do edge-tts e **não valem** para as vozes do Piper — usá-los
+  é o erro do 679/698. Cada peça narrada por lá sai com `::warning::`, e o
+  instrumento para remedir é `calibra-piper.yml`, que **não escreve** em
+  `ensaio.py`: colar é decisão. **A voz grega do Piper só existe em qualidade
+  `low`**, e isso é diferença real entre canais.
+  Todas as peças de 12/10 saíram pelo Piper: `byriXB1gSg8`, `DQKMvUi2FF4`,
+  `rusVeiFco9Q`.
 
@@ -574,4 +609,12 @@
     pior e desnecessário; foi o dono quem viu o link na tela.
-    **O que continua valendo:** o `mcp__github__*` NÃO se recupera — segue
-    `invalid session` depois da troca. Para ler um job sem ele, use as ANOTAÇÕES:
+    **E CAIU EM 12/10, pelo MESMO raciocínio que esta entrada condena:** eu
+    escrevi "o `mcp__github__*` NÃO se recupera — segue `invalid session`". Na
+    rodada das 08:07 ele reconectou sozinho e devolveu log completo. **Ausência
+    de mudança não é impossibilidade de mudança — e eu apliquei o erro proibido
+    à ferramenta seguinte, dentro da correção dele.** Sonde antes de declarar
+    que não há rota.
+    **A rota das ANOTAÇÕES continua sendo a certa ENQUANTO o MCP estiver fora**,
+    com um limite medido: ela só carrega o que foi emitido como
+    `::warning::`/`::notice::`. Em 12/10 o motivo de uma falha e o `youtube_id`
+    de uma publicação bem-sucedida ficaram invisíveis por isso:
     `gh api repos/<owner>/<repo>/check-runs/<job_id>/annotations` devolve os
@@ -808,6 +851,18 @@
    MCP, Vercel (OAuth). O Supabase JÁ está ligado como MCP.
-13. **Liberar `speech.platform.bing.com` na política de rede do ambiente** (Network
-   access → Allowed domains, deixando "Allow package managers" marcado). Hoje o
-   CONNECT leva 403 e por isso este container não sintetiza voz nem renderiza. É o
-   que tornaria a rodada local, e é também o plano B da narração que a §6 pede.
+13. **Liberar hosts na política de rede do ambiente** (Network access → Allowed
+   domains, deixando "Allow package managers" marcado). São DOIS grupos, e o
+   segundo é novo e mais consequente:
+   (a) `speech.platform.bing.com` — hoje o CONNECT leva 403 e por isso este
+       container não sintetiza voz nem renderiza localmente;
+   (b) **as FONTES INSTITUCIONAIS**, medido às 10:15 de 12/10 com `curl -v`:
+       `ec.europa.eu`, `www.statistics.gr`, `api.sejm.gov.pl` e `www.gov.br` —
+       os quatro devolvem **403 ao CONNECT**, confirmado no
+       `__agentproxy/status` como `policy denial`.
+   **E (b) é o que trava o refil da pauta.** Longo carrega número sobre o mundo,
+   número exige duas fontes institucionais (600), e a rota documentada para isso
+   é o `pg_net` — que depende do banco, que está em 402. Logo o 402 não bloqueia
+   só a medição: ele bloqueia **escrever longo novo**, e portanto o refil da
+   pauta. Com ele fechado eu só consigo short de longo JÁ publicado, que não
+   introduz número novo. **Prometer longo novo nesta condição é mentir com
+   número.**
 DÍVIDA TÉCNICA: **25 testes falham, e a composição está na §6** — 15 de
```
