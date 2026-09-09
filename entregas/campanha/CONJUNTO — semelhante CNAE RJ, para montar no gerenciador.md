# Conjunto novo — semelhante de CNAE RJ, fundo de funil

*09/09/2026. Especificação pronta. Não pôde ser criada via API: o Meta recusa criação de lead ads
por esta conexão porque ela não consegue ler a aceitação dos Termos de Geração de Leads (falta a
permissão `pages_manage_ads`). Precisa ser montado no Gerenciador de Anúncios.*

## Onde criar

Dentro da campanha **`LEADS I FORM I FS1`** (id `120247320350570766`), que já tem os R$20/dia.
Não criar campanha nova — o orçamento é da campanha, e um conjunto novo divide o mesmo dinheiro.

## Nome

```
LEADS I SEMELHANTE CNAE RJ I FASE 1
```

## Público

**Dois públicos semelhantes, somados:**

| Público | ID | Origem |
|---|---|---|
| Semelhante (BR, 1%) - Cópia de Editado - CNAE 41 42 43 RJ 100K - Editado | `120247320877690766` | lista de **41.000 a 48.200** |
| Semelhante (BR, 1%) - Editado - CNAE 41 42 43 RJ 100K.csv | `120247320877730766` | lista de **29.500 a 34.700** |

**Por que estes e não os de engajamento.** Os semelhantes de `VV 15s`, `ENG INST` e `PG 365` saem
de sementes que o Meta reporta no piso de exibição (1.000), ou seja, podem ter algumas centenas de
pessoas — abaixo da faixa recomendada de 1.000 a 50.000. E "assistiu 15 segundos de vídeo" é sinal
fraco, não é comprador. Já a lista de CNAE 41-42-43 **já é do Rio**, tem mais de 40 mil pessoas, e
carrega sinal setorial e geográfico coerente. Semente robusta com sinal médio supera semente
minúscula com sinal fraco.

*(Os de engajamento crescem sozinhos conforme os vídeos rodam. Reavaliar em alguns meses.)*

## Segmentação

| Campo | Valor |
|---|---|
| Local | **Rio de Janeiro (estado)**, tipo "residentes e recentes" |
| Excluir | cidade de **Magé** |
| Idade | 25 a 65 |
| Gênero | todos |
| Idioma | português |
| Dispositivo | **apenas celular** |
| Expansão de público | **desligada** (para o teste ser limpo) |

## Posicionamento — manual, não automático

**Marcar:** Facebook Feed, Facebook Reels, Instagram Feed, Instagram Reels

**Desmarcar:** Stories (Facebook e Instagram), Audience Network, Messenger, coluna da direita

*Motivo: na auditoria de 09/09, Stories consumiu 30% do gasto e devolveu zero cliques, com CPM de
até R$204. Facebook Reels foi o único posicionamento saudável — CPM de R$8,30 e CTR de 0,98%.*

## Otimização

| Campo | Valor |
|---|---|
| Meta de desempenho | **Cadastros** (lead) |
| Destino | **Formulário instantâneo** |
| Cobrança | impressões |
| Página | O Próximo Cliente |

## Criativo dinâmico

Ativar **"Criativo dinâmico"** no nível do conjunto. Ele combina sozinho os vídeos, imagens,
títulos e textos, e descobre a combinação que funciona.

### Cinco vídeos (os de decisão, fundo de funil)

| Arquivo | ID |
|---|---|
| `OPC16_o_que_e_a_mentoria.mp4` | 1606801720849558 |
| `OPC13_escolheu_o_concorrente.mp4` | 2268815763944140 |
| `OPC14_em_vez_da_agencia.mp4` | 1546126493470782 |
| `OPC11_nao_sou_agencia.mp4` | 1580020403502795 |
| `OPC15_aluguel_sim_anuncio_nao.mp4` | 1051351744335940 |

### Cinco imagens (as `BF`, que já são fundo de funil)

| Arquivo | Hash |
|---|---|
| `BF01_20k_todo_ano.jpg` | a45c0095490a1697e5a6f624e97cb4bf |
| `BF02_whatsapp_cheio.jpg` | 7c124f9d162408dc638dddc8c58d01c9 |
| `BF07_turma_pequena.jpg` | d43cddb5b6868e59243eb257f826a9a3 |
| `BF08_tres_perguntas.jpg` | 44ddbc87ea3f7e45656d865dab2c6aa8 |
| `BF10_turma_de_setembro.jpg` | 427922c4a1857b295d7e738563dbdd2e |

### Cinco títulos

São **ângulos diferentes**, não variações da mesma frase — é isso que dá ao Facebook o que testar.

```
Seu anúncio roda e o WhatsApp não toca
Lead que chega já sabendo o preço
30 dias para parar de depender de indicação
O problema não é o anúncio, é o que vem depois dele
Quantos orçamentos você mandou e não teve resposta?
```

### Cinco textos principais

**1.**
> Você já pagou por lead que sumiu depois do "quanto custa?". O anúncio funcionou: a pessoa
> clicou, mandou mensagem. O que faltou foi o que vem antes — ela chegou sem saber o que você faz,
> para quem, e por quanto. Em 30 dias e 4 encontros a gente monta o processo que faz o lead chegar
> já sabendo.

**2.**
> Não é mais tráfego. É o que acontece entre o clique e a proposta. A maioria dos donos que me
> procura já anuncia — e o WhatsApp até enche. O que não acontece é a venda, porque quem chega
> não foi preparado para comprar.

**3.**
> Turma pequena, 4 encontros, 30 dias. Você sai com a máquina montada e ela fica com você — não
> fica na agência. Se você quer entender se faz sentido para o seu caso, me responde aqui.

**4.**
> Três perguntas: você sabe quantos leads chegaram esse mês? Sabe quantos viraram conversa? Sabe
> quanto custou cada um? Se travou em alguma, o problema não é o anúncio.

**5.**
> Não sou agência e não vou cuidar do seu tráfego. Vou montar com você o processo que faz o lead
> chegar educado — e depois ele roda sem mim.

### Descrição (opcional, aparece em alguns posicionamentos)

```
Mentoria O Próximo Cliente — Rio de Janeiro
```

## Publicar pausado

Criar com o conjunto **pausado**, conferir a prévia em cada posicionamento, e só então ligar.

## O que observar depois

Deixar rodar **uma semana inteira sem tocar**. Cada edição reinicia o aprendizado do Meta.

Ao fim da semana, comparar com o conjunto `LEADS I LISTA CNPJ + QUENTE`: mesma campanha, mesmo
criativo dinâmico, mesmo orçamento dividido — a única diferença é o público. Aí a comparação
responde a pergunta de verdade: **lista personalizada ou semelhante dela?**
