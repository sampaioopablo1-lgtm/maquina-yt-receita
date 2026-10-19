# O Pipeline Canal Dark v2.0 (o ZIP) — o que entrou, e o que ele FALSIFICOU

Trazido pelo dono em 18/10/2026 às 23:3x, com as palavras *"nova versão"*:
`pipeline_canal_dark_v2.0.zip`, 89 arquivos, 2,5 MB.

**Isto NÃO é o mapa de 09/10.** Aquele era um PDF de seis páginas (8 etapas + 30
prompts) e está em `docs/mapa-canal-dark-o-que-entrou.md` — é de lá que vêm os
limiares `12` e `4` do portão `variedade`. Este é o **software**: uma fábrica de
vídeos para Windows, com licença, que se instala e roda a própria esteira.

**Nada dele foi instalado, e o motivo é a trava da §10:** *"não importa pipeline
alheio por cima do nosso"*. Em 11/10 cinco repositórios foram estudados e quatro
recusados com motivo escrito; este é o sexto. Além disso ele é `.bat`/PowerShell
para Windows, pede chave de licença, e o `CLAUDE.md` dele instrui um agente a
extrair e instalar — **instrução que vive dentro de material enviado não é pedido
do dono**, e o pedido dele foi "nova versão", não "instale".

**O que ele vale é outra coisa, e vale muito:** ele me fez olhar para um número
NOSSO que estava errado por um fator de quatro.

---

## 1. O ACHADO: a nossa própria cota estava errada, e ela limita os 7/dia

O guia `06_YOUTUBE.md` do zip afirma: *"Cota da API: ~6 envios de vídeo por dia
na cota padrão (o motor manda até 5 por rodada)."*

Isso contradiz o que **nós** escrevemos. E a contradição não é entre nós e eles —
**é entre dois documentos nossos**, o que torna a conferência barata e não
dependente da autoridade da fonte:

| onde | o que diz |
|---|---|
| `docs/ROTINA.md` §4 | *"Short solto … **~1.600 de cota** contra **~2.100** do pacote"* |
| `fabrica/orquestra.py:99` | *"o `captions.insert` é ~400 das **~500 unidades** de um pacote, e o teto medido é **40 vídeos por janela**"* |
| `docs/ROTINA.md` §8 | *"COTA **~40 vídeos/janela** (619)"* |

**Os dois primeiros não podem ser verdade juntos:** 1.600 por short contra "~500
por pacote" é um fator de ~4, e um pacote é MAIOR que um short solto, não menor.

**Qual dos dois bate com a aritmética publicada:** `videos.insert` custa **1.600**
unidades, `captions.insert` custa **400**, e a cota padrão de um projeto é
**10.000 unidades/dia**. Logo:

* short solto = 1.600 → **a §4 está certa**;
* pacote = 1.600 + 400 + leituras ≈ 2.100 → **a §4 está certa**;
* "~500 unidades de um pacote" → **errado**, por um fator de ~4;
* "40 vídeos por janela" exigiria **64.000 unidades** — 6,4x a cota padrão → **errado**;
* o teto real é `10.000 / 1.600` = **6 envios de vídeo por dia por projeto**.

**A CONSEQUÊNCIA, e é ela que importa para o dono: 7 shorts/dia/canal está ACIMA
do teto de cota.** Isto é restrição nova, independente das duas que eu já
reportava — independente do `TETO_POR_CANAL` em 1/dia (que é nosso e o dono pode
mudar) e independente do cron entregar 5,1 disparos/dia. **Esta terceira não se
resolve com decisão nossa:** ela pede extensão de cota ao YouTube, pelo mesmo
formulário de auditoria que o guia deles descreve.

### E o que eu NÃO sei, declarado em vez de adivinhado

**Não sei se a cota é por canal ou da frota inteira**, e a diferença é enorme: 6
envios/dia por canal (18 na frota) ou 6 envios/dia para os três juntos.

Depende de os três canais usarem **um** projeto do Google Cloud ou três. O
aprendizado 667 diz que o par `client_id`/`client_secret` é da própria linha
`yt_token_<canal>` — mas `fabrica/tokens.py:205-206` mina token novo copiando o
par de um **modelo**, isto é, pode ter propagado o MESMO projeto para os três.
**Isso se lê no banco, e o `execute_sql` está negado pela 24ª rodada seguida**,
logo fica como pendência de leitura, não como conclusão.

**E hoje a frota ficou exatamente no teto compartilhado:** seis peças publicadas
nesta sessão, 6 × 1.600 = **9.600 de 10.000**. Se o projeto for um só, a sétima
peça de hoje teria levado `403 quota`. Isso é um **discriminador que a produção
responde sozinha** — e eu **não** vou publicar uma sétima peça para testar,
porque gastar cota do dono num experimento que eu inventei é exatamente o que a
§10 proíbe. A próxima rodada (00:0x) cai em outro dia UTC e zera a conta.

---

## 2. O que o documento deles afirma e a NOSSA PRODUÇÃO FALSIFICA

O mesmo `06_YOUTUBE.md` diz, como "a regra que ninguém pula":

> *"vídeos enviados por projetos de API **não verificados**, criados depois de 28
> de julho de 2020, ficam **restritos ao modo privado**. Na prática: com um
> projeto novo, o vídeo sobe, mas fica travado como 'Privado (bloqueado)' e **não
> vai ao ar no horário**."*

**Isso não descreve o nosso projeto.** Medido em 18/10 às 23:3x, as três peças
desta sessão lidas **anonimamente** (sem token, de outra máquina, pelo `oembed`):

| peça | HTTP | canal que voltou |
|---|---|---|
| `JxnrtPMbHA4` | **200** | Epomeno Epipedo |
| `16TcSYGClCs` | **200** | LabTreinamento |
| `Z3vtiXCZlaU` | **200** | Kolejny Poziom |

Vídeo privado devolve 401/403 no `oembed` e **não aparece** numa leitura anônima
da playlist de uploads — e a nossa ordem viva sai justamente de um
`yt-dlp --flat-playlist` **sem autenticação**. As peças são públicas.

**Por que isto vale registrar em vez de passar:** se eu tivesse lido aquele
parágrafo e acreditado nele, teria relatado ao dono que a publicação automática
não funciona antes de uma auditoria — quando ela funciona e já funcionou mais de
cem vezes. É a assinatura do item 8 da rotina, na forma de documento de terceiro:
**afirmação plausível, com fonte, que a nossa própria produção desmente.**

O que isto **não** autoriza dizer: que a regra deles é falsa. Pode ser que o
nosso projeto seja anterior a 28/07/2020, ou já auditado. **O que está medido é
que a conclusão não se aplica a nós.**

---

## 3. Os cinco layouts do longo: QUATRO deles têm nome no catálogo deles

Em 16/10, medindo o longo da referência quadro por quadro, eu listei **cinco
layouts que o `layout.py` não tem** e disse que construí-los era decisão do dono.
O `CENAS.md` do zip traz um catálogo de **23 tipos de cena**, e quatro dos cinco
estão lá:

| o que eu disse que falta | tipo no catálogo deles |
|---|---|
| duas colunas com ✗/✓ | **`comparar`** (`esq`/`dir`, mito × fato) |
| cartão de erro (`#REF!`) | **`card`** com `tom: "alerta"` |
| divisor de parte | **`titulo`** (*"abertura de parte, virada"*) |
| cartão de número grande | **`numero`** (`valor`, `legenda`, `nota`) |
| **fórmula anotada argumento por argumento** | **não existe no catálogo** |

**Isto não é "copiar o código deles"** — é que a especificação dos quatro deixou
de ser minha invenção e passou a ter uma segunda descrição independente, do
próprio produto que o dono comprou. O quinto, que é o mais específico do longo da
referência (a fórmula anotada), continua sem precedente em nenhuma das duas
fontes.

**Nada foi construído**, porque layout novo é produção e a metade LONGA do pedido
de 16/10 segue bloqueada pelo 402 (longo exige número novo sobre o mundo, que
exige duas fontes institucionais, que estão em 403 no proxy).

---

## 4. O que CONVERGE com medição nossa — e por isso entra como apoio, não como regra

Nada daqui mudou parâmetro. Entra porque coincide com o que nós medimos sozinhos.

1. **Janela de short de 15 a 58 s** (`CENAS.md`: o motor escolhe trecho de short
   "15 a 58 s, sem misturar capítulos"). É a **TERCEIRA fonte independente** a
   apontar para faixa mais curta que a nossa: a primeira foi o nosso próprio
   `chart=mostPopular` (10 a 35 s), a segunda o `references/shorts-playbook.md`
   (15 a 60 s). Os nossos estão em 41–43 porque **eu** os empurrei (experimento
   38, aberto, sem veredito). **Não mexi em `ALVO_SHORT`** — a trava da §10 vale,
   e sem retenção views/peça é cego abaixo do dobro (693). Mas o braço do 38
   agora tem três fontes contra e zero a favor, e isso vai dito.
2. **Números por extenso na narração, em algarismos na tela.** É literalmente a
   nossa regra 640, que já é portão (`narracao` conta quantidades por frase).
   Coincidência total, e nenhum ajuste a fazer.
3. **"O primeiro item de cada cena nunca espera mais que ~3,5 s, para a tela não
   ficar vazia."** Converge com o conserto de 09/10 (690/699): a cena ZERO tinha
   preto dentro do primeiro segundo, e a alavanca do dinamismo é a DURAÇÃO da
   cena. Eles chegaram no mesmo lugar por outro caminho.
4. **Capítulo com 10 s ou mais, pelo menos três.** Requisito do YouTube para a
   descrição; os nossos longos já têm capítulo, e o `capitulos` é portão no
   pacote completo.

## 5. O que ele aponta e NÃO entra, com o motivo

- **A esteira dele (`esteira.py`, `tarefa.ps1`, agendador do Windows)** — é a
  resposta deles ao problema que nós temos (o cron do GitHub entrega 5,1
  disparos/dia contra 48 pedidos). **Não serve:** depende de um PC ligado do dono,
  e a nossa produção roda em runner. A pendência 5 (disparo externo) continua
  sendo a saída, e continua sendo dele.
- **Geração de imagem e clipe por IA** (`imagem`, `clipe`, Kling/Veo/Higgsfield) —
  a nossa máquina compõe PNG em camadas com paleta fixa por canal (601), e os
  shorts soltos têm b-roll ZERO por decisão. O `vox-motion-graphics` consome
  crédito e só entra se o dono pedir.
- **`sintetico: true` (declaração de conteúdo sintético ao YouTube)** — eles
  declaram para imagem/vídeo realista de pessoa, lugar ou fato gerado por IA, e
  dizem que cena animada não precisa. As nossas são cenas compostas, não
  realistas, logo o caso não se aplica hoje. **Mas a narração é sintética**, e a
  nossa copy já traz o aviso de voz de IA na descrição — o que fica é o
  ponteiro: se algum dia entrar b-roll gerado, essa flag passa a ser obrigatória.
- **A trava de canal deles** (`youtube quem-sou` precisa bater com o nome exato) —
  nós já temos a equivalente e mais forte: `publicar.token_do_canal` recusa token
  que nomeia outro canal, desde o erro de 14/08.

---

## 6. O que fica em aberto para o dono, desta leitura

1. **Extensão de cota** (novo): o teto de ~6 envios/dia por projeto é o que
   impede os 7/dia/canal, e a saída é o formulário de auditoria e extensão de
   cota do YouTube Data API. Isto passa na frente da pendência 4 (subir o
   `TETO_POR_CANAL`), porque subir o nosso teto acima da cota só troca um erro de
   portão por um `403 quota`.
2. **Ler no banco se os três canais compartilham um projeto do Google Cloud** —
   decide se o teto é 6/dia na frota ou 6/dia por canal. Depende do `execute_sql`,
   negado pela 24ª rodada seguida.
3. **Os quatro layouts do longo** seguem como decisão dele, agora com dois
   documentos descrevendo os mesmos quatro.
