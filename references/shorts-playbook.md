# O que entrou dos cinco repositórios externos — e com que procedência

**ESTE ARQUIVO FOI RECONSTRUÍDO EM 14/10/2026 ÀS 02:3x, E A RECONSTRUÇÃO VAI
DECLARADA PORQUE ELA É O ACHADO.** Em 11/10 eu escrevi, no `CLAUDE.md`, no
`docs/ROTINA.md`, no `docs/pipeline-canal-dark-estudado.md` e num comentário do
`fabrica/ensaio.py`, que o que entrou dos cinco repositórios estava "em
`references/shorts-playbook.md`". **O arquivo nunca foi comitado** — `git log
--all -- references` não devolve commit nenhum, e o diretório não existia.

Então por três dias **quatro documentos apontaram para uma fonte inexistente**, e
um deles é a procedência da faixa `ALVO_POR_CANAL` do `labtreinamento`, que é
parâmetro de PRODUÇÃO. Quem fosse conferir de onde vem o `20,0 a 26,0` chegaria a
um `No such file or directory`.

**E o teste que eu escrevi para guardar exatamente isso PASSAVA.** O
`tests/test_decisoes_12_10.py::test_a_PROCEDENCIA_das_decisoes_continua_escrita_no_codigo`
exigia que a *string* `"shorts-playbook"` aparecesse no `ensaio.py` — e nunca
exigiu que o CAMINHO CITADO EXISTISSE. Portão verde fabricando "a procedência
está escrita" (§3.8), na forma mais literal: ele guardava a citação, não a fonte.

## O que o conteúdo abaixo É, e o que ele NÃO é

É a transcrição dos três itens que **já governam o código** e que sobreviveram na
nota do `CLAUDE.md` ("O que entrou dos cinco projetos externos"). **Não é leitura
nova dos repositórios**, não traz número que não estivesse já escrito, e **não
vale como fonte fresca**: a leitura original é de 11/10 e o que dela restou é
esta lista. Se alguém precisar de mais que isto, o caminho é reler os
repositórios, que continuam em `/home/user/<autor>/<repo>`.

## ENTROU, e nada por autoridade da fonte

Entrou só o que **converge com medição nossa**, que é a régua da §5 da rotina.

1. **Cadência de mudança visual a cada ~3 s.** Converge com a física que nós
   medimos sozinhos (690/699: a alavanca é a DURAÇÃO DA CENA, não a amplitude).
2. **Faixa boa de 15 a 60 s, com picos em 13 s e 60 s.** É a **segunda** fonte
   independente contra o experimento 38 — a primeira é o nosso próprio
   `chart=mostPopular` (10 a 35 s, mediana 26 s no BR). **Não mudou `ALVO_SHORT`**
   quando entrou: o 38 seguia sem leitura de 12 h, e views/peça é cego sob
   CV 0,66 (693).
3. **Conversão de "vídeo relacionado" abaixo de 1%.** Apoia o experimento 37 — o
   CTA pedindo inscrição em vez de apontar para o longo.

**PROCEDÊNCIA, declarada e MISTA, e é fraca de propósito dizer isso:**
- "estudo de 35 bilhões de views" — **sem nome**, logo não verificável;
- `vidIQ` — **fornecedor de ferramenta**, isto é, parte interessada;
- Tubefilter / Digital i — com **nome e data**, e é a única das três que eu
  citaria sozinha.

**Logo este arquivo não decide nada por si.** Ele é a segunda fonte de uma
convergência; a primeira é sempre a nossa medição.

## NÃO ENTROU, com motivo escrito

- `youtube-automation-agent` — pipeline Node paralelo ao nosso, sem portão, sem
  corpus anti-duplicata e sem disciplina de medição. Trocar seria **regressão**.
- `ai-video-generator-claude` — prompts para Higgsfield. Os shorts soltos têm
  b-roll ZERO por decisão, e Higgsfield consome crédito: só se o dono pedir.
- `claude-youtube` (as *skills*) — andaime para criador humano e orientado a
  LONGO: o `hook.md` pede gancho de 30 s com ~75 palavras, e o nosso short
  inteiro tem ~41 s. **Os scripts dele usam a YouTube Analytics API com OAuth** —
  isto é, o escopo que nós perdemos (689): confirmação independente de que o
  clique de consentimento é o único caminho, não um atalho.
- `claude-code-youtube-mcp` — exige Node, chave de API e instalação pelo dono. O
  que tem de interessante é o mapa de **"most replayed"**, proxy de retenção em
  canal alheio por dado público. Fica como sugestão ao dono, não como dependência.
- `claude-real-video` — frames + transcrição sincronizada. Nós já fazemos análise
  de quadro com `ffmpeg`/`signalstats`, e o gargalo não é ler vídeo dos outros.

## A regra de método que sai disto

**Citar caminho é afirmar que o caminho existe.** Quando um documento ou um
comentário de código aponta para um arquivo como procedência, o teste que guarda
essa procedência tem de **abrir o arquivo**, não procurar o nome dele numa
string. `tests/test_referencia_citada_existe.py` faz isso agora, para toda
citação de `references/` no `ensaio.py`, no `CLAUDE.md` e no `docs/ROTINA.md`.
