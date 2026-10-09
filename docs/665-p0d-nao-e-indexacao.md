# P0D depois de duas horas é falha de processamento, não indexação

08/10/2026, rodada das 21:09. Aprendizado 665, severidade `critico`.

## O que foi medido

Duas peças do epomeno estavam com ZERO view havia horas:

| peça | id | idade | views | `uploadStatus` | `duration` |
|---|---|---|---|---|---|
| epomeno-s007 | `Ta_KN8yXLaI` | 10,9 h | **0** | `uploaded` | **P0D** |
| epomeno-s008 | `oHwlhhneIos` | 8,9 h | **0** | `uploaded` | **P0D** |

E todas as peças que receberam distribuição hoje estão `processed` com duração
real — **inclusive as publicadas horas DEPOIS dessas duas**:

| peça | id | idade | views | `duration` |
|---|---|---|---|---|
| epomeno-s009 | `pquXg25s5Ps` | 3,9 h | **273** | PT34S |
| kolejny-s009 | `g9lHoS6boHA` | 2,9 h | **258** | PT38S |
| labtreinamento-s006 | `UE0fcjIdURQ` | 1,9 h | 0 (jovem) | PT34S |
| labtreinamento-s007 | `RuQM42HS8CM` | 0,9 h | 0 (jovem) | PT35S |

## A conclusão, e o que ela derruba

**Vídeo que não terminou de processar não é distribuído.** O zero não era forma,
não era posição no dia e não era tag — era upload que nunca ficou pronto.

Caem, como explicação deste caso:
- o efeito de **posição no dia** (já derrubado pelo 663: a sétima peça do canal
  fez 273 em 3,9 h);
- a hipótese de **forma repetida** (663) — não foi refutada, ficou
  **desnecessária**, e não deve ser usada como se tivesse evidência;
- a hipótese de **tags** como causa do zero (ela segue aberta como causa de
  *alcance*, no experimento 36, mas não explica zero).

## E derruba uma regra da própria rotina

A rotina diz, nas travas:

> `uploadStatus` sai `uploaded` com `duration: P0D` e pode levar MAIS de uma
> consulta — reconsulte, não "conserte"

Isso é verdade em **minutos**. Em **horas** é defeito. A nota, como estava
escrita, me ensinou a descartar justamente o sinal que explicava tudo — e eu a
obedeci por oito rodadas, reportando "três em uploaded, benigno" em cada
relatório de vigilância do teto.

**Regra nova:** `P0D` depois de **2 h** é falha de processamento. A peça deve ser
tratada como NÃO PUBLICADA — não conta no ritmo do dia, não entra no denominador
de alcance, e vai dita no relatório.

## O que fazer com as duas

Decisão do dono, porque é irreversível: apagar as duas e republicar as specs
(`epomeno-epipedo-s007` e `s008`), ou esperar. Não apaguei por conta própria.
Se amanhã continuarem em `P0D`, são upload morto.

## Vigilância do teto, corrigida

A contagem "N/N vivos, N públicos, M processados" vinha sendo reportada com os
não-processados como ruído de indexação. Passa a valer: **qualquer peça com mais
de 2 h fora de `processed` é incidente e vai nomeada**, com id e idade.

## Nota de método: o 401 intermitente

Esta medição quase não aconteceu. A chamada de vigilância em três lotes devolveu
agregado de 89 itens para 134 ids, e o motivo era um HTTP **401** em um dos
lotes — com token recém-emitido. Reemitir o token não resolveu; dividir o lote
reproduziu o 401 no mesmo ramo três vezes, o que me fez suspeitar de um id
específico. Repetindo exatamente a mesma chamada de seis ids, veio **200**.

Ou seja: **o 401 é INTERMITENTE, não depende do conjunto** — e é o mesmo modo de
falha que quebrou o `apontar_para_longo` às 18:16 (662). Regra: ler
`status_code` de CADA requisição antes de somar itens; agregado esconde lote que
falhou.

---

## Adendo de 09/10/2026 — TAG zero tem a MESMA armadilha que o P0D

Aprendizado 672. Este documento existe porque eu tratava `P0D` como indexacao
quando ja era defeito. O erro simetrico aconteceu com as TAGS, e no mesmo dia.

A rotina mandava: *"se vier nulo ou 8, o passo falhou — refaca por `pg_net`"*.
Apliquei ao `cBBYHdP5JYA` (`labtreinamento-s008`), lido com ~1 minuto de vida:

| leitura | req | idade | tags |
|---|---|---|---|
| 1 | 716 | ~1 min | **0** |
| 2 | 717 | ~2,5 min | **15** |

Era a corrida de indexacao do 659. Se eu tivesse obedecido a rotina, teria
reescrito o snippet de um video que estava **correto** — cometendo o 659 dentro
da correcao do 662.

**A regra passa a ser, e ela e simetrica a do P0D:**

- **tag nula ANTES de 2 min nao decide nada.** Espere e releia. Nao escreva.
- **tag nula DEPOIS de 2 min e falha** do passo: refaca por `pg_net` um PUT de
  `part=snippet` com o snippet INTEIRO e as quinze tags.
- **OITO tags em qualquer momento** e o defeito antigo do `[:8]` do
  `publicar.py`, removido em 08/10. Se reaparecer, o codigo regrediu — conserte o
  codigo, nao o video.

A forma geral das duas regras e a mesma, e vale para qualquer campo que o
`videos.list` sirva: **uma leitura jovem nao distingue "ainda nao indexou" de
"nao existe". O que distingue e o RELOGIO, e so ele.** Sem um limiar de idade
escrito, a leitura unica fabrica as duas conclusoes opostas com igual confianca.
