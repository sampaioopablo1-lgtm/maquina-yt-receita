# Auditoria de ponta a ponta — 09/09/2026, 13h

*Primeira auditoria feita com acesso de escrita real (token do usuário do sistema Funcionário,
via servidor MCP oficial da Meta). Todos os números são da vida inteira das campanhas.*

## O quadro geral

| Campanha | Impressões | Alcance | Freq. | Gasto | CPM | CTR | Resultado |
|---|---|---|---|---|---|---|---|
| **REC I FS1** (topo) | 2.702 | 2.603 | 1,04 | R$ 27,43 | R$ 10,15 | 0,70% | 1.777 video views |
| **LEADS I FORM I FS1** (fundo) | 403 | 313 | 1,29 | R$ 32,17 | **R$ 79,83** | 0,50% | **0 leads** |

O topo está barato e saudável. O fundo gastou **mais** que o topo para entregar **sete vezes menos
impressões**, e não trouxe nenhum lead.

## Achado 1 — o erro que eu quase cometi: Stories não é vilão em toda parte

Na leitura agregada da conta, Stories parecia desperdício puro: R$ 15,56 gastos, zero cliques.
Quebrando **por campanha**, a conclusão se inverte para o topo:

### Topo (REC) — custo por ThruPlay

| Posicionamento | Impressões | Gasto | CPM | ThruPlays | Custo/ThruPlay |
|---|---|---|---|---|---|
| Facebook Reels | 1.744 | R$ 14,43 | R$ 8,27 | 306 | **R$ 0,047** |
| Instagram Stories | 163 | R$ 5,89 | R$ 36,16 | 104 | R$ 0,057 |
| Facebook Stories | 170 | R$ 2,48 | R$ 14,60 | 56 | **R$ 0,044** |
| Facebook Feed | 289 | R$ 2,00 | R$ 6,93 | 37 | R$ 0,054 |
| Instagram Reels | 199 | R$ 1,65 | R$ 8,30 | 28 | R$ 0,059 |
| Instagram Feed | 136 | R$ 0,99 | R$ 7,28 | 14 | R$ 0,071 |

**Facebook Stories é o segundo posicionamento mais barato do topo.** O CPM alto do Instagram
Stories é compensado por uma taxa de visualização altíssima — 104 ThruPlays em 163 impressões.
Julgar posicionamento de campanha de vídeo por *clique* é o erro; a moeda ali é atenção.

**Decisão: não mexer no topo.** Ele está entregando atenção a R$ 0,05.

### Fundo (LEADS) — custo por clique

| Posicionamento | Impressões | Gasto | CPM | CTR | Cliques |
|---|---|---|---|---|---|
| Instagram Reels | 136 | R$ 9,63 | R$ 70,81 | 0,74% | 1 |
| Instagram Feed | 136 | R$ 9,21 | R$ 67,72 | 0,00% | 0 |
| **Instagram Stories** | 46 | R$ 5,97 | **R$ 129,78** | 0,00% | 0 |
| Facebook Feed | 44 | R$ 3,59 | R$ 81,59 | 0,00% | 0 |
| Facebook Reels | 33 | R$ 2,55 | R$ 77,27 | **3,03%** | 1 |
| **Facebook Stories** | 8 | R$ 1,22 | **R$ 152,50** | 0,00% | 0 |

Aqui Stories custa o dobro do resto e não devolve nada. **Corte aplicado** no conjunto
`LEADS I LISTA CNPJ + QUENTE I FASE 1`: fora Stories, fora feed de perfil, fora desktop.
Ficaram Facebook Feed, Facebook Reels, Instagram Feed e Instagram Reels, só celular.
As 12 listas personalizadas foram preservadas, uma a uma.

## Achado 2 — o problema do fundo não é posicionamento, é tamanho de público

CPM entre R$ 68 e R$ 152 em **todos** os posicionamentos não é sinal de criativo ruim nem de
lugar errado: é sinal de leilão apertado. O conjunto soma 12 públicos, mas cruzados com Rio de
Janeiro, 25 a 65 anos, e a maioria das listas é **nacional** — sobra pouca gente do Rio dentro
delas. O Meta paga caro para achar as poucas pessoas elegíveis.

É exatamente a hipótese que o conjunto `LEADS I SEMELHANTE CNAE RJ I FASE 1` (criado hoje) existe
para testar: o semelhante amplia a base mantendo o sinal. Se o CPM dele cair para a faixa de
R$ 20-30, a resposta está dada.

## Achado 3 — idade e gênero: o público real não é o público imaginado

| Faixa | Impressões | Gasto | CPM | CTR |
|---|---|---|---|---|
| **65+ feminino** | 792 | R$ 9,84 | R$ 12,42 | **1,26%** |
| 55-64 masculino | 263 | R$ 6,89 | R$ 26,20 | 1,14% |
| 55-64 feminino | 425 | R$ 4,86 | R$ 11,44 | 0,94% |
| 35-44 masculino | 290 | R$ 9,70 | R$ 33,45 | **0,00%** |
| 25-34 masculino | 149 | R$ 4,51 | R$ 30,27 | **0,00%** |
| 25-34 feminino | 109 | R$ 2,12 | R$ 19,45 | 0,00% |

Quem clica é **55+**, principalmente mulheres. Quem não clica, e custa mais caro, é **25-44
masculino** — justamente o perfil que o conjunto de topo tenta comprar com interesses de
"empresário" e "pequeno negócio".

**Não é decisão de ajustar agora**, e explico por quê: 2 cliques no fundo e 19 no topo são
amostra pequena demais para cortar faixa etária. Mas é o número a observar na próxima leitura.
Se 65+ continuar liderando, o interesse de "Small business owners" está trazendo aposentado que
gosta do assunto, não dono de empresa.

## Achado 4 — o anúncio novo está com erro de entrega, e a causa é o app

O anúncio `VR1 — INTERESSE` (`120247352877730766`), criado hoje no conjunto que estava vazio,
está **WITH_ISSUES**. O log do Meta:

> *"Ads creative post was created by an app that is in development mode. It must be in public to
> create this ad."*

O app **OPC Automação** está em modo de desenvolvimento. Enquanto estiver, nenhum criativo novo
criado por ele entrega — nem o criativo dinâmico do conjunto semelhante.

**Ação do Pablo, um clique:** developers.facebook.com → app OPC Automação → chave
**"Em desenvolvimento" → "Modo ativo"**.

## O que foi feito nesta auditoria

| Ação | Resultado |
|---|---|
| Anúncio no conjunto vazio | criado — `120247352877730766` |
| Conjunto semelhante CNAE RJ | criado — `120247353022060766`, pausado, sem anúncio ainda |
| Corte de Stories no fundo | aplicado |
| Só celular no fundo | aplicado |
| Reativação do conjunto de fundo | feita (a edição forçou pausa; foi religado) |
| Criativo dinâmico do semelhante | **bloqueado** pelo modo de desenvolvimento do app |
| Topo (INT I DONOS) | **não tocado, de propósito** — está a R$ 0,05 por ThruPlay |

## O que observar na próxima leitura

1. **CPM do fundo depois do corte.** Se cair de R$ 80 para R$ 40-50, o posicionamento era parte
   do problema. Se ficar igual, é tamanho de público, e o semelhante é a resposta.
2. **65+ continua liderando cliques?** Se sim, revisar os interesses do topo.
3. **Frequência do fundo (1,29).** Já é a mais alta da conta com apenas 313 pessoas alcançadas —
   confirma público pequeno demais.
