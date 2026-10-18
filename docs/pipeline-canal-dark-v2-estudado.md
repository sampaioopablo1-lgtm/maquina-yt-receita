# O `pipeline_canal_dark_v2.0` — estudado em 18/10/2026, e o que entrou

O dono mandou o zip sem recado, como mandou o v1.2 em 12/10 e os cinco
repositórios em 11/10. A régua é a mesma da §5 da rotina: **entra o que converge
com medição nossa, e nada por autoridade da fonte.** O estudo do v1.2 está em
`docs/pipeline-canal-dark-estudado.md`; este arquivo só trata do que **mudou**
de lá para cá e do veredito de cada mudança. Quem reler o zip inteiro reaplica o
que já foi aplicado — não releia; leia os dois arquivos.

## O que ele é na 2.0

A mesma fábrica local para Windows (roteiro → narração → cenas no navegador →
montagem → shorts → thumbnail → agendamento), agora com o Claude Code **ou** o
Codex como operador, nove *skills* em vez de seis, um painel visual, uma esteira
por tarefa agendada e **três vozes em fila**: edge-tts (online) → Piper (local) →
voz do Windows. Continua honesto no que importa: o `guia/06_YOUTUBE.md` repete
que vídeo enviado por projeto de API não auditado **fica travado como privado**,
e manda subir pelo Studio enquanto a auditoria não vem — o que bate com o que
nós vivemos.

## O que mudou do 1.2 para o 2.0, item a item

| mudança | veredito | motivo |
|---|---|---|
| Piper como voz de reserva, Windows como terceira | **já temos** o Piper (`fabrica/voz_piper.py`, 12/10); a voz do Windows não existe em runner Linux | — |
| **"Uma voz só por vídeo"**: se a online cai no meio, os blocos já feitos são refeitos com a que ficou | **ENTROU** — `fabrica/voz_unica.py` | ver abaixo: a medição que a justifica é nossa |
| Volume final em **dois passos** (mede com `ebur128`, corrige por ganho + `alimiter`) em vez de `loudnorm` de uma passada | **não entrou** | medimos 10 peças reais com `som.py`: todas dentro de 1,0 LU do alvo, amplitude 1,1 LU, sem direção. Um segundo passo corrigiria o que não está errado |
| Verificador de pronúncia por `faster-whisper`, agora com detecção de *glitch* (similaridade < 0,72, silêncio > 1,6 s) e até 4 regravações | **não entrou**, mesmo veredito do 1.2 | 200–500 MB de modelo no runner com minuto contado; segue como sugestão ao dono |
| QA reprova `volume fora do alvo ± 1,0 LU` | **não entrou** | a nossa dispersão medida tem 1,1 LU de amplitude: esse portão reprovaria peça por variação normal |
| QA avisa `volume da voz varia > 6 dB entre blocos` | **não entrou** | nós já lemos o LRA (1,7 a 3,1) por peça; outro número para a mesma pergunta |
| Similaridade entre roteiros: erro acima de 0,30, aviso acima de 0,15 (5-gramas) | **não entrou**, igual ao 1.2 | o nosso limiar (0,65) vem do mapa do dono; o dele não traz procedência |
| Shorts automáticos: janelas de 15 a 58 s pontuadas por gancho (pergunta, número, cena de destaque), sem cruzar capítulo | **não se aplica** | short solto nosso nasce de spec, não de recorte do longo; e 15–58 é escolha de produto, não medição |
| Legenda do short em grupos de **3** palavras | **já temos** grupos de até 4 (`fabrica/legenda.py`, 690) | diferença de uma palavra sem medição de nenhum dos lados |
| Trilha a ~−31 LUFS que só sobe (+6 dB) em silêncio > 1,0 s | **não entrou** | parâmetro de produção sem medição; trava da §10 |
| "Nunca travessão" em tela, título, descrição e narração | **não entrou** | regra de estilo sem procedência; nenhuma medição nossa fala disso |
| Cor: `out_color_matrix=bt601:out_range=pc` ao extrair quadro para JPEG | **já registrado** no 1.2 | — |
| Esteira: 1 vídeo/dia por padrão "para não parecer produção em série", até 5 | **não entrou** | opinião do produto; o nosso teto está medido e é decisão do dono (pendência 4) |
| Tempo de palavra na voz local dividido proporcionalmente dentro da frase | **já fazemos** por caracteres (`legenda.py`) | — |

## O que ENTROU, e é UMA coisa — e a medição é NOSSA

**`fabrica/voz_unica.py`: uma voz só por peça.** O `fabrica.py` tenta o edge-tts
três vezes **por cena** e cai no Piper na terceira falha. Em 16/10 isso produziu
**três peças publicadas com voz mista**, contadas pelos avisos
`NARRACAO PELO PIPER` na anotação do job do render:

| peça | cenas pelo Piper | job |
|---|---|---|
| `labtreinamento-s060` | **2** de 10 | `116943785023` |
| `labtreinamento-s061` | **1** de 10 | `116989849294` |
| `labtreinamento-s062` | **2** de 10 | `117070798289` |

E o Piper do pt-BR é `pt_BR-faber-medium`, voz **masculina**, dentro de um short
narrado pela Thalita, **feminina**. Logo essas três peças trocam de voz e de
gênero no meio de quarenta segundos — e o portão `identidade` (601) não as
pegou, porque ele lê a spec e não o áudio. O
`tests/test_o_run_pode_ser_MISTO.py` havia registrado o regime misto como
problema da **banda** (ponto sem mundo de provedor). **Ele é também um defeito
audível, e foi ao ar três vezes** — eu o medi e não o li como defeito até a
regra do v2.0 nomear a saída.

**A saída, em duas etapas e nesta ordem:**

1. para cada cena que caiu no Piper, **uma** tentativa a mais do edge. A queda
   medida foi de 1 a 2 cenas em 10, logo o edge estava de pé no run — a chance
   de recuperar a voz do canal (identidade, 601) é alta e custa no máximo um
   timeout de 90 s por cena;
2. se ainda sobrar cena do Piper, **todas** as cenas do edge são refeitas pelo
   Piper. Para o Piper e não para o edge porque o edge acabou de falhar duas
   rodadas neste run e o Piper é offline: unificar para o lado que falha é
   promessa, unificar para o que acabou de funcionar é certeza. Se o Piper não
   conseguir refazer uma cena, o render **levanta** em vez de publicar misto.

**E a consequência para o instrumento do 733 vai dita:** a contagem de avisos
volta a ser **0 ou N (cenas)**, nunca entre os dois. O aviso sai uma vez por
cena no estado **final**, depois da unificação — imprimi-lo na hora da queda
deixaria a anotação contando um estado que a peça publicada não tem. E a marca
lateral `sNN.mp3.piper` existe porque a RETOMA reaproveita mp3 válido de run
anterior: sem ela não haveria como saber quem narrou aquele arquivo, e a peça
sairia mista outra vez pelo caminho do restart.

**O que isto NÃO conserta:** as três peças já publicadas. Apagar vídeo publicado
exige o dono. E não mexe em voz, mira, `rate` nem em nenhum parâmetro de
produção (§10) — a voz do canal segue a da spec, e o Piper segue sendo fallback,
nunca primeira voz (`test_voz_piper.py` continua cobrando isso).

**O que isto NÃO prova:** que o misto não volte por outro caminho. A unificação
cobre a queda do edge por cena e o restart; não cobre um Piper que falhe no meio
da unificação (aí o render levanta, de propósito). Doze testes em
`tests/test_uma_voz_so_por_peca.py`, um deles **falha se o aviso do 733 voltar a
sair antes da unificação** e um **falha se o motivo sair do módulo**.

## A chave da licença: nada mudou

Continua onde o 1.2 a deixou (`config.licenca_pipeline_canal_dark` no Supabase)
e continua fora do git, pelo motivo do 1.2: o repositório é **público**. O zip
2.0 não traz chave nova e a verificação segue chamando `app.ianofacil.com.br`,
que o proxy desta sessão nega.
