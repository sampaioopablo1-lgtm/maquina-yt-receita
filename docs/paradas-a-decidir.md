# As 15 specs que sairiam da matriz caladas — e por que NÃO são 15 julgamentos

**Levantado em 11/10/2026**, rodando `orquestra._falhas_baratas` em cada spec de
produção fora do inventário `PARADAS`. É o conjunto exato que o
`test_narracao_das_specs` acusa, com a mensagem literal do portão.

**RETRATAÇÃO MINHA, e é do enquadramento que eu dei ao dono em duas rodadas.**
Eu escrevi no `CLAUDE.md` que o inventário "são quinze julgamentos, um por spec,
e merece decisão, não varredura". **Medido, não são quinze.** São **três
famílias** de defeito, e **onze das quinze são a MESMA**, com o mesmo remédio
mecânico escrito pelo próprio portão. E o que mais encurta a decisão: **só
quatro das quinze são de canal da frota** — as outras onze são de canal PARADO,
onde consertar não produz nada hoje.

## O que decide de verdade: as QUATRO da frota

| spec | família | o que o portão diz |
|---|---|---|
| `epomeno-epipedo-008` | capítulo sem margem | `Η ημερομηνία: δύο Οκτωβρίου` dura **64,0 s** |
| `epomeno-epipedo-010` | capítulo sem margem | `Το τεκμήριο δεν ρωτάει τι έβγαλες` dura **63,9 s** |
| `labtreinamento-005` | capítulo sem margem | `As duas datas do calendário` dura **63,7 s** |
| `epomeno-epipedo-009` | números numa frase | short 04: **4 números** numa frase |

## As três famílias, e o remédio que o portão já prescreve

**(1) Capítulo sem margem — 11 das 15.** O piso do `copy_md` é 60 s e o modelo
de voz erra até **4,9% nos dois sentidos**, então capítulo estimado em 61–64 s
passa na estimativa e **some no render**. Já aconteceu de verdade:
`setiap-level-014`, 01/09/2026. Remédio escrito pelo portão: **esticar o texto
até 64 s estimados**. É mecânico, não é julgamento.

Da frota: `epomeno-epipedo-008` (64,0), `epomeno-epipedo-010` (63,9),
`labtreinamento-005` (63,7).
De canal parado: `agla-level-008`, `game-money-lab-008`, `nivel-do-jogo-008`,
`nivel-do-jogo-009` (**cinco** capítulos raspando), `resep-naik-level-009`,
`setiap-level-012`, `seviye-seviye-008`.

**(2) Quatro números numa frase — 4 das 15.** "Planilha falada": o `narracao`
recusa mais de três quantidades por frase. Remédio escrito: **quebrar em
progressão**. Também mecânico.

Da frota: `epomeno-epipedo-009`.
De canal parado: `agla-level-003`, `next-level-money-010`, `seja-mais-magra-007`.

**(3) Acentuação fora do padrão — 1 das 15.** `nivel-do-jogo-003`, canal
parado: 1,9% das letras acentuadas contra 4,2% nas outras specs pt do mesmo
canal. Em pt isso muda a pronúncia do TTS e **nenhum outro portão enxerga**.

## A decisão que sobra para o dono, em uma linha

Para cada uma das **quatro da frota**: **consertar o texto** (mecânico, o portão
diz exatamente o quê) **ou registrar no inventário `PARADAS` com o motivo**. As
onze de canal parado podem ficar como estão sem custo de produção — elas só
ocupam a contagem das 25 falhas conhecidas.

**Por que eu não conserto sozinho:** a trava da rodada de construção diz que ela
**não edita specs em massa**, e mexer no texto de capítulo é escrever conteúdo
que vai ao ar em três canais vivos. O levantamento é meu; a caneta é dele.

**Como remedir, sem depender de mim:**

    python3 -m pytest tests/test_narracao_das_specs.py -q

e cada falha trará a mensagem literal do portão para aquela spec.
