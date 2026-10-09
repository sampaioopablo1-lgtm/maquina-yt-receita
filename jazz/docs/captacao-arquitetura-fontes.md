# Máquina de captação: estudo de mecanismo e fontes

Pergunta: como montar, com o menor custo possível, um fluxo que entregue
anúncio de **pessoa física** com telefone, para competir de verdade.

Resposta curta: **a maior alavanca disponível hoje não é fonte nova — é a
dimensão tempo do que já se coleta, que está sendo descartada.** Depois dela,
por ordem de retorno sobre custo: inverter o funil (o dono vem até você),
expandir portais onde o dono publica o telefone, e por último sinais públicos
oficiais, que dão o imóvel e o nome mas nunca o telefone.

---

## Camada 0 — O que está sendo jogado fora agora (custo: R$ 0)

`captacao-prospectar/index.ts:166`:

```ts
.upsert(linhas, { onConflict: "fonte,anuncio_id", ignoreDuplicates: true });
```

A varredura roda 3× por dia e reencontra os mesmos anúncios. `ignoreDuplicates`
manda tudo isso para o lixo. O que se perde:

| sinal | por que importa | custo de obter |
|---|---|---|
| **dias no portal** | particular parado há 90 dias já tentou sozinho e não conseguiu. É o lead mais maduro que existe — e o mais fácil de abordar, porque a dor é dele, não sua. | zero |
| **queda de preço** | dono que baixa preço está sinalizando urgência antes de qualquer conversa. | zero |
| **anúncio que sumiu** | sumiu em 3 semanas: vendeu — e vendeu sem você, o que é informação de mercado. Sumiu depois de 120 dias: desistiu, e desistiu atende telefone. | zero |
| **reincidência** | mesmo imóvel anunciado, retirado, reanunciado meses depois: dono que quer vender e não consegue, ciclo após ciclo. | zero |

Nenhum vendedor de lista tem isso, porque lista é foto. Quem varre todo dia
tem filme. **É a única vantagem competitiva desta operação que não pode ser
comprada por um concorrente com mais orçamento.**

Implementado em `20260910_captacao_dimensao_tempo.sql`. O score inverte a
régua antiga de propósito: **anúncio velho vale mais que anúncio novo.** Dono
no dia 3 ainda acha que vende sozinho; dono no dia 90 já sabe que não vende.

### Armadilha de deploy que os testes pegaram

`fn_captacao_marcar_sumidos()` na primeira execução marcaria como sumida a base
inteira — medido, 37 de 37 linhas — porque `visto_em` foi retro-preenchido a
partir de `coletado_em` e a Edge Function ainda não o escreve. Sumido vale
score −1000: **a fila do captador zerava no dia um.**

A guarda: só é candidato a sumido quem a coleta nova já reviu ao menos uma vez
(`visto_em > coletado_em + 1 hora`). Quem nunca foi revisto não é sumido, é
desconhecido — e desconhecido continua na fila.

---

## Camada 1 — Inverter o funil: o dono entrega o telefone (custo: ~R$ 0)

O maior retorno por real gasto, e o de menor risco jurídico, porque o titular
entrega o dado voluntariamente, com finalidade declarada.

**"Quanto vale meu imóvel?"** — avaliação instantânea e gratuita. O dono digita
endereço, tipo, área e quartos; recebe uma faixa de valor na hora; deixa o
telefone para receber o laudo completo.

A Jazz já tem o único insumo que isso exige e que a concorrência local não tem:
**3.894 fichas reais com preço, área e bairro**. A mediana do m² por bairro já
está calculada em `fn_captacao_score`. A barra de busca em linguagem natural já
resolve o endereço.

Por que funciona melhor que lista comprada:
- quem pede avaliação está pensando em vender **agora**;
- o telefone vem com consentimento e finalidade — base legal limpa;
- custo marginal por lead tende a zero depois da página no ar;
- e o laudo é a desculpa perfeita para a segunda ligação.

Custo: uma página no Lovable + a RPC de avaliação. Zero dado novo.

---

## Camada 2 — Mais portais onde o proprietário publica o telefone

Hoje: Zap, VivaReal, ChavesNaMão (via GeckoAPI, 1 crédito por 30 anúncios).

| fonte | volume de particular | como | custo |
|---|---|---|---|
| **OLX** | o maior do Brasil em venda direta por dono | confirmar se a GeckoAPI já cobre; é o primeiro pedido a fazer a eles | igual ao atual |
| **Mercado Livre Imóveis** | relevante e subexplorado | **API pública e gratuita** (`developers.mercadolivre.com.br`), OAuth, categoria imóveis | R$ 0 + dev |
| **Placa "vende-se" na rua** | altíssimo em bairro consolidado | o dono publicou o telefone na calçada exatamente para ser ligado. App simples: o time fotografa, OCR extrai o telefone | ~R$ 0 |

A placa merece atenção: é hiperlocal, o que favorece quem está em São José dos
Campos e não favorece plataforma nacional nenhuma. É a fonte mais barata e a
menos disputada.

---

## Camada 3 — Sinais públicos oficiais (dão o alvo, nunca o telefone)

Estes identificam **qual imóvel vai à venda** antes de o anúncio existir. Não
entregam telefone; entregam nome e endereço, e a abordagem vira carta, visita
ou busca do contato por meio próprio.

| fonte | sinal | custo | ressalva |
|---|---|---|---|
| **Inventário aberto** (ESAJ/TJSP, público) | herdeiro quase sempre vende | consulta pública | finalidade comercial sobre dado judicial exige parecer jurídico |
| **Partilha em divórcio** | venda para dividir | consulta pública | idem |
| **Editais de leilão / execução** | venda forçada | público | concorrência alta |
| **Alvará e habite-se** (prefeitura) | estoque novo entrando | público | sinal de construtora, não de PF |
| **Matrícula** (ARISP/ONR) | nome do proprietário | ~R$ 50–100 por certidão | caro para varredura; serve sob demanda, depois de o lead existir |

Ordem correta: usar Camadas 0–2 para gerar volume, e a Camada 3 só para
qualificar um lead que já vale a certidão.

---

## O que fica de fora, e por quê

**Enriquecimento CPF → telefone: não.** Não existe fonte pública no Brasil que
faça essa ligação. O que o mercado vende com esse nome vem de vazamento. Além
do risco jurídico, há o risco de produto: uma base contaminada não se
descontamina depois, e a Jazz passaria a ter um passivo em vez de um ativo.

**Raspagem direta dos portais: não.** Os termos de uso proíbem, e o telefone
publicado ali foi publicado para o comprador ligar. A GeckoAPI existe
justamente para colocar essa responsabilidade num fornecedor com contrato.

Vale registrar o que isso não impede: as Camadas 0, 1 e 2 juntas entregam mais
volume qualificado do que qualquer lista comprada, porque entregam **intenção
datada** — e é intenção, não telefone, que fecha captação.

---

## Ordem de execução sugerida

1. **Camada 0** — dimensão tempo. Já implementada, custo zero, usa a coleta que já roda.
2. **Camada 1** — página de avaliação. Maior retorno, base legal limpa, insumo já existe.
3. **Camada 2** — pedir OLX à GeckoAPI; depois Mercado Livre; depois placa.
4. **Camada 3** — só sob demanda, com parecer jurídico antes.
