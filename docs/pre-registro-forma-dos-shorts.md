# Pré-registro: a forma dos onze shorts, classificada ANTES de qualquer view

Escrito em 26/08/2026, 17h20 UTC. Os onze pacotes estão renderizados e nenhum
foi publicado — nenhum tem uma única view. É de propósito que a classificação
seja feita agora.

## Por que antes

O aprendizado 514 mediu o que a frota consegue e o que não consegue medir:

- por PACOTE não há poder nenhum. Sessenta e sete dos setenta e nove shorts
  publicados têm zero inscrito, e o esperado sob uma taxa única é 67,4.
- por GRUPO o efeito aparece. O aprendizado 482, re-testado agrupando por
  forma, dá 21,6× com p exato de 0,00023.

Ou seja: o teste que vale é o agrupado, e o agrupamento depende de um rótulo
que EU atribuo. Rotular depois de ver quem converteu é escolher o resultado.
Rotular agora, no escuro, é a única versão do teste que significa alguma coisa.

Quando os onze estiverem publicados e tiverem exposição — lembrando que um
inscrito esperado pede cerca de 916 views na taxa base — roda-se
`fabrica/conversao.py` com estes grupos, sem tocar nos rótulos.

## O critério

Do aprendizado 482, a divisão grossa: **método** que a pessoa aplica em si
mesma contra **fato** sobre o mundo.

Do aprendizado 504, as três condições finas, que têm de valer juntas:

1. o dinheiro (ou a coisa medida) é DO ESPECTADOR, em segunda pessoa
2. é uma ESCOLHA que ele faz, não um número imposto de fora
3. o short entrega a CONTA, não só o fato

## A classificação

| pacote | c1 dele | c2 escolha | c3 conta no short | grupo |
|---|:--:|:--:|:--:|---|
| `nivel-do-jogo-007` | sim | sim | sim | **método** |
| `seviye-seviye-007` | sim | sim | sim | **método** |
| `setiap-level-012` | sim | sim | sim | **método** |
| `agla-level-007` | sim | sim | procedimento | **método** |
| `game-money-lab-007` | sim | sim | procedimento | **método** |
| `kolejny-poziom-012` | sim | fraca | sim | **método fraco** |
| `seja-mais-magra-007` | sim | fraca | sim | **método fraco** |
| `resep-naik-level-008` | sim | fraca | sim | **método fraco** |
| `epomeno-epipedo-011` | sim | **não** | sim | **incompleto** |
| `labtreinamento-006` | sim | sim | **adiada** | **incompleto** |
| `next-level-money-007` | sim | fraca | **adiada** | **incompleto** |

Onde "fraca" quer dizer que o espectador decide um comportamento seu, mas não
elege uma opção com prazo e consequência — os minutos da semana, o consumo da
cozinha, a tarifa de luz que ele até pode trocar mas o short não pede. Onde
"adiada" quer dizer que o short anuncia a conta e a entrega no longo, que é
justamente o que a alavanca A manda não fazer.

## O caso que dói, e por que eu não vou consertar

`epomeno-epipedo-011` é o pacote do canal com MAIS sinal da frota — 8
inscritos, 43 horas — e é o primeiro da ordem de publicação. E é ele que falha
a condição dois: IVA é imposto, o espectador não escolhe nada. É a mesma forma
do `seviye-seviye-005`, que teve dinheiro do espectador, prazo, e zero
inscrito em 337 views.

A tentação é reescrever o short antes de publicar. Não vou, e o motivo é o
próprio 514: eu não consigo distinguir duas formas boas com a exposição que a
frota tem. Reescrever agora com base num julgamento que não dá para validar
destrói o único teste limpo que existe aqui — os rótulos deixam de ser cegos e
o resultado passa a medir a minha intuição, não a forma.

Se o grupo "incompleto" converter pior, o pré-registro vira evidência. Se
converter igual, a condição dois cai, e ela cai com número.

## O que este documento não é

Não é gate. `prontidao.py` não lê isto, e não deve: transformar julgamento em
portão é como o portão de ortografia quase aprovou um defeito — a régua tem de
sair de medição, não de opinião. Isto é uma aposta escrita com data, para ser
conferida contra o que acontecer.
