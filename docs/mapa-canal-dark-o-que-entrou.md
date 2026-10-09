# O "Mapa do Canal Dark com IA" — o que entrou, o que já tínhamos, o que está errado nele

Documento trazido pelo dono em 09/10/2026 (`ianofacil.com.br`, 6 páginas: as 8
etapas da fábrica + 30 prompts). Pedido: estudar e instalar as melhorias.

Este arquivo existe para que ninguém releia o PDF e reaplique o que já foi
aplicado — e para que ninguém repita as três afirmações erradas dele.

---

## 1. As 8 etapas: a máquina já faz as oito

| # | Etapa do mapa | Onde mora aqui | Veredito |
|---|---|---|---|
| 1 | Nicho e roteiro | `autor.py`, `esboco.py`, rotina horária | já existe, com portão de fontes |
| 2 | Narração | `fabrica.py` (`edge_tts`) | já existe — **mas é fornecedor único, ver §4** |
| 3 | Imagens | `layout.py` (SVG → PNG em camadas) | já existe, e não é imagem gerada |
| 4 | Animação | `motion.py` (experimento 33) | já existe |
| 5 | Montagem | `fabrica.py` + ffmpeg, `loudnorm=I=-14:TP=-1.5:LRA=11` | já existe |
| 6 | Shorts | `.srt` queimado só no short (`fabrica.py:838`) | já existe |
| 7 | Thumbnail | `layout.analisa_thumb` | já existe, **e mede mais que o mapa pede** |
| 8 | Postagem | `publicar.py` + ponte | já existe |

A checagem do mapa para a etapa 7 é "legível no celular". O nosso portão já
mede **sobreposição das duas linhas**, **largura em pixel rasterizado** (porque
`l2` é desenhado em `c1`, a cor da moldura: uma linha que transborda não sai
cortada, sai *invisível*) e **tinta fora da caixa branca**. Nada disso está no
mapa.

---

## 2. O que ENTROU — portão `variedade` (`fabrica/variedade.py`)

Três itens do mapa apontavam para coisas que a máquina não olhava.

### (a) Conteúdo inautêntico — **o item mais caro do documento**

Medido em 09/10/2026: **39 de 39** shorts soltos da frota têm a mesma sequência
de layouts, `titulo-titulo-titulo-titulo-cta`. Por canal: epomeno 15, kolejny
14, labtreinamento 10.

A substância *varia* de verdade — origem, aritmética e entrada errada diferentes
em cada peça — e o kicker do CTA tem **trinta** valores distintos nas 39. Metade
do que o mapa pede a máquina já fazia sem saber. O **esqueleto** é que nunca
variou.

O portão **avisa e não reprova**, e o motivo é de experimento, não de
conveniência: mudar o número de cenas mexe no gancho **visual**, que é o que o
experimento 33 (motion) está medindo com trava de intocado por 10 dias ou 15
shorts/canal. Reprovar hoje obrigaria a quebrar a trava do 33 na próxima peça.

Fica **pré-registrado** como experimento 39: variar o esqueleto é o **primeiro**
teste da fila quando o 33 fechar, passando na frente dos três que esperam (short
de 22–26 s, b-roll na cena 1, matar os fades). O argumento é assimetria — este
risco é de nível **canal** e irreversível; os três da fila são de nível **view**.

**Não está afirmado que o esqueleto aciona a política.** O YouTube não publicou
lista do que conta como feito em massa, e inventar causa aqui teria a assinatura
do item 8 da rotina. Aprendizado 687.

### (b) Gancho — primeira frase da cena 1, ≤ 12 palavras (mapa, prompt 25)

**Reprova.** Estado em 09/10: **26 de 86** specs da frota passariam de 12
palavras; nos 39 shorts soltos, 14 passam (mediana 9, máximo 21). O
`epomeno-epipedo-s015`, publicado às 10:17 de hoje, tem 13 — o portão o pegaria.

### (c) Thumbnail — ≤ 4 palavras somando as duas linhas (mapa, prompt 23)

**Reprova.** Estado em 09/10: **40 de 86** specs da frota passariam de 4
palavras.

Os portões rodam em spec **nova**: nada disso reprova peça publicada.

### Os limiares não são meus

`12` e `4` são do mapa, literalmente, e estão escritos com a procedência no
docstring do módulo — limiar sem procedência é critério inventado. O `6` do
aviso de esqueleto **é** meu, e é exatamente por isso que ele só avisa.

---

## 3. As três afirmações erradas do mapa

1. **"Política de conteúdo inautêntico, julho de 2025"** — não é proibição nova.
   Em 15/07/2025 o YouTube **renomeou** `repetitious content` para
   `inauthentic content`; conteúdo repetitivo e feito em massa já era inelegível
   antes. O próprio liaison do YouTube chamou de atualização menor, de rótulo.
2. **"O YouTube desmonetiza"** — é regra de **elegibilidade do YPP**, não de
   remoção. Para quem já monetiza é risco de desmonetizar; para nós, que estamos
   tentando *entrar* pela Porta 1, **é o portão em si**. Importa mais, não menos.
3. **"Vídeo longo acima de 8 minutos libera anúncio no meio"** — o número está
   certo, a data não: o piso caiu de 10 para 8 minutos em **julho de 2020**, não
   em 2025. E **não há nada a instalar**: medi os 47 longos da frota e **46
   passam de 8 minutos** (mediana ~13 min). O único abaixo é uma spec-tronco de
   10 cenas, não um pacote. Anúncio no meio só vale depois do YPP, de todo modo.

As fontes são secundárias em quase toda a cobertura, e o YouTube não define
"mass produced". A frase oficial que opera é: *"The substance of each video
should be materially varied and deliver creative, educational, or other value."*

---

## 4. O que o mapa aponta e NÃO foi instalado, com o motivo

- **Regra de ouro 1, "nunca dependa de um único fornecedor; toda etapa precisa
  de plano B".** A narração tem **fornecedor único**: `edge_tts.Communicate` em
  `fabrica.py:598`, uma chamada, três tentativas, nenhuma alternativa. E a falha
  já é real e medida — `speech.platform.bing.com` leva 403 no CONNECT pela
  política de rede deste ambiente (`vozes.py:13`), e é por isso que todo render
  depende do runner, da fila e da URL assinada de 10 minutos. **Não instalei a
  costura do plano B** porque uma costura sem segundo provedor adiciona risco ao
  único caminho de produção que existe, sem benefício hoje. Virou pendência
  nomeada: ou liberar o host (pendência 9) ou uma credencial de um segundo TTS.
- **Prompt 6 (revisão anti-molde) e prompt 30 (análise de retenção)** — pedem
  chamada de modelo (`ANTHROPIC_API_KEY`, pendência 7) e
  `yt-analytics.readonly` (pendência 1). O prompt 30 é, aliás, a quarta fonte
  independente a dizer que a pendência 1 é pré-condição.
- **Prompt 24, "janela de short de 30 a 55 s"** — a nossa é 30–45 e é portão
  (`SHORT_MIN_S`, `SHORT_MAX_S`). Os 45 s são auto-impostos: Shorts aceita até 3
  minutos. É território do experimento 38, que ainda **não tem veredito** —
  nenhuma peça de tratamento novo passou das 12 h. Não mexer.
- **Prompts 7–21 (bloco de estilo, texto exato na imagem, prompt negativo)** —
  não se aplicam: a máquina compõe PNG em camadas com paleta fixa por canal
  (`docs/estoque.md`), não gera imagem por difusão. A regra 22 do mapa ("nunca
  escreva no prompt positivo o que você não quer") não tem onde morder aqui.
- **Prompts 23/25/26/27/28 restantes** — descrição com capítulos, 15 tags de
  busca, comentário fixado: já existem em `copy_md.py` e em toda spec.
