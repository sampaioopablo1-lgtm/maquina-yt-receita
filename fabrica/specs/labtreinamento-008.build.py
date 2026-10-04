#!/usr/bin/env python3
"""Monta a spec labtreinamento-008.

ALAVANCA ATACADA: **A — conversao, pela FORMA que este canal ja provou**, e o
numero de partida e o mais desproporcional da frota.

NUMERO DE PARTIDA, lido em 04/10/2026 com o lifetime relido por videos.list
(o aprendizado 554 explica por que o dado anterior nao servia):

    labtreinamento .... 65 inscritos, 14 videos, 2.463 views
                        short: mediana 0,55 views/dia, topo 34,16
                        longo: mediana 0,31 views/dia
                        veredito: `suspenso` (piso de 8 min)
                        razao longo/short: 5% — a segunda pior da frota

O QUE DEU CERTO, e sao DOIS videos que respondem por 96% das views de short:

    "Por Hora ou por Projeto? A Conta no Seu Ultimo Orcamento" .. 1.132 views
    "INSS do Autonomo: 11% ou 20%? A Escolha na Sua Guia" ....... 1.111 views

Os dois sao a MESMA forma: uma ESCOLHA BINARIA que o espectador decide com um
papel que ele JA TEM na mao — o orcamento dele, a guia dele. Nao e assunto, e
forma: os dois sao sobre dinheiro de prestador de servico, e os dois terminam
numa decisao que e dele.

O QUE NAO DEU: norma e planilha, que era a identidade antiga do canal. NR-10
fez 21 no short e 18 no longo; ISO 9001, 28 e 14; a planilha de riscos
psicossociais, 26 e 9 numa versao e 4 e 11 na outra; o FAP, 20 e 31. Nenhum
passou de 31 views. Sete videos de norma somam menos que um dia do short do
orcamento.

E O NUMERO QUE DOI, que e o motivo deste pacote existir: o short "Por Hora ou
por Projeto" fez 1.132 views e **o longo do mesmo pacote fez TRES**. Trezentos
e setenta e sete para um. O canal acha mil pessoas com o short e tres com o
longo, no mesmo dia, com o mesmo assunto.

O QUE MUDO POR CAUSA DISSO:

1. **A PAUTA COPIA A FORMA DOS DOIS CAMPEOES** e abandona norma e planilha:
   escolha binaria de prestador de servico, decidida com o papel dele.

2. **O EIXO E NOVO.** Nenhum dos catorze videos fala de PRAZO DE RECEBIMENTO.
   Precificacao ja foi (por hora ou por projeto); carga tributaria ja foi (INSS
   11% ou 20%). O que nunca foi: o que custa receber mais cedo.

3. **NENHUM NUMERO EXTERNO CARREGA O VIDEO**, e isso foi decisao desta rodada,
   nao preferencia. A pauta primeira era o Fator R do Simples Nacional, que
   depende dos 28% da LC 123/2006; o planalto.gov.br cortou a conexao em tres
   tentativas (`OpenSSL SSL_read: unexpected eof`). A regra do canal diz que
   numero sem fonte oficial nao entra, e a doutrina diz para redesenhar a pauta
   de modo que o numero que decide seja o DO ESPECTADOR. Foi o que fiz: aqui os
   tres numeros que decidem sao o desconto que ele da, o prazo que ele antecipa
   e a taxa que o banco DELE oferece no app dele. Nenhum precisa de terceiro.

A CONTA, entregue no capitulo 2 (~135 s estimados):
    desconto dividido pelo que sobra = o juro do periodo
    10 dividido por 90 = onze virgula um por cento
    se o periodo e de trinta dias, esse e o juro AO MES que ele esta pagando

DIMENSIONAMENTO: veredito `suspenso` = piso de 8 min. Alvo ~545 s (9min05s), 8
capitulos. Nao da para encostar nos 480 s com oito capitulos e a margem do
`MARGEM_CAP`: oito vezes 68 s ja passa de 540. Entao o piso real de um longo de
oito capitulos neste canal e ~9 min, e eu prefiro dizer isso a cortar capitulo
— a alavanca B pede MAIS capitulos, nao menos.

A VOZ DESTE CANAL ERRA PARA MENOS: a pt-BR-ThalitaMultilingualNeural mediu
-1,9% no desvio do modelo, o unico caso da frota em que o real sai mais CURTO
que a estimativa. Por isso os capitulos foram desenhados em ~68 s e nao nos
64,2 s do portao: 68 x 0,981 = 66,7 s, que ainda sobra sobre os 60 s do
`copy_md`.
"""

C1 = [
    {"layout": "titulo", "kicker": "O cliente pede desconto",
     "sub": "para pagar à vista",
     "cap": "O desconto que parece de graça",
     "nar": "O cliente aprova o orçamento e faz um pedido só: um desconto para "
            "pagar à vista. Você aceita, porque dinheiro na mão hoje parece "
            "sempre melhor do que dinheiro daqui a um mês."},
    {"layout": "item", "kicker": "E parece custar nada", "preco": "só um desconto",
     "sem_cap": True,
     "nar": "E parece não custar nada. Você não assinou contrato de empréstimo, "
            "não pagou tarifa, não falou com banco nenhum."},
    {"layout": "item", "kicker": "Mas você emprestou", "preco": "ao contrário",
     "sem_cap": True,
     "nar": "Só que aconteceu um empréstimo ali, e ele foi ao contrário do que "
            "você imagina: quem pagou juros foi você, e quem recebeu foi o "
            "cliente."},
    {"layout": "item", "kicker": "Ele ficou com o dinheiro", "preco": "um mês a mais",
     "sem_cap": True,
     "nar": "Pense no que o cliente ganhou. Ele ficou com o dinheiro dele um "
            "mês a mais do que ficaria, e pagou menos por isso."},
    {"layout": "item", "kicker": "Isso tem nome", "preco": "e tem taxa",
     "sem_cap": True,
     "nar": "Isso tem nome no mercado financeiro e tem taxa. A diferença é que "
            "na sua proposta a taxa não está escrita em lugar nenhum."},
    {"layout": "item", "kicker": "Ela está escondida", "preco": "dentro do desconto",
     "sem_cap": True,
     "nar": "Ela está escondida dentro do desconto, e dá para tirar de lá com "
            "uma divisão."},
    {"layout": "item", "kicker": "Dois números", "preco": "da sua própria proposta",
     "sem_cap": True,
     "nar": "Você precisa de dois números, e os dois estão na última proposta "
            "que você enviou. Vou pegar eles agora."},
    {"layout": "item", "kicker": "No fim", "preco": "você sabe quanto cobrou de juros",
     "sem_cap": True,
     "nar": "No fim deste vídeo você vai saber, em por cento ao mês, quanto de "
            "juros você cobrou de si mesmo no seu último desconto."},
]

C2 = [
    {"layout": "titulo", "kicker": "A divisão", "sub": "dois números seus",
     "cap": "A conta: o desconto dividido pelo que sobra",
     "nar": "Abra a última proposta em que você deu desconto para pagamento à "
            "vista. Precisamos de duas informações dela."},
    {"layout": "item", "kicker": "Número 1", "preco": "o desconto, em por cento",
     "sem_cap": True,
     "nar": "O primeiro é o desconto que você deu, em por cento. Se foi em "
            "reais, divida pelo valor cheio e multiplique por cem."},
    {"layout": "item", "kicker": "Número 2", "preco": "quantos dias você antecipou",
     "sem_cap": True,
     "nar": "O segundo é quantos dias você antecipou. É a diferença entre o "
            "prazo normal da sua proposta e o dia em que o dinheiro entrou."},
    {"layout": "item", "kicker": "Agora a divisão", "preco": "desconto ÷ o que sobra",
     "sem_cap": True,
     "nar": "Agora a divisão. Pegue o desconto e divida pelo que sobra dos cem "
            "por cento, não pelos cem."},
    {"layout": "item", "kicker": "Dez por cento", "preco": "10 ÷ 90 = 11,1%",
     "sem_cap": True,
     "nar": "Se o desconto foi de dez por cento, a conta é dez dividido por "
            "noventa. Dá onze vírgula um por cento."},
    {"layout": "item", "kicker": "Esse é o juro", "preco": "do período antecipado",
     "sem_cap": True,
     "nar": "Esse é o juro que você pagou pelo período que antecipou. Se o "
            "período foi de trinta dias, ele já é o juro ao mês."},
    {"layout": "item", "kicker": "Pronto", "preco": "onze por cento ao mês",
     "sem_cap": True,
     "nar": "Onze vírgula um por cento ao mês. A conta acabou aqui, e o resto "
            "do vídeo é o que esse número significa."},
    {"layout": "item", "kicker": "Por que 90 e não 100", "preco": "é o que você levou",
     "sem_cap": True,
     "nar": "E por que dividir por noventa, e não por cem? Porque noventa é o "
            "que você realmente levou. O juro se mede sobre o que entrou no "
            "seu bolso, não sobre o preço de tabela."},
]

C3 = [
    {"layout": "titulo", "kicker": "Onze por cento ao mês",
     "sub": "isso é muito ou pouco?", "cap": "Onze por cento ao mês é muito?",
     "nar": "Onze vírgula um por cento ao mês parece um número pequeno porque "
            "vem de um desconto pequeno. Então vamos dar escala a ele."},
    {"layout": "item", "kicker": "Compare com o que você paga",
     "preco": "no seu próprio app", "sem_cap": True,
     "nar": "Não vou citar taxa de banco nenhuma aqui, porque taxa muda e varia "
            "por cliente. Abra o aplicativo do SEU banco e procure antecipação "
            "de recebíveis, ou crédito para capital de giro."},
    {"layout": "item", "kicker": "A taxa que aparece lá", "preco": "é a sua referência",
     "sem_cap": True,
     "nar": "A taxa que aparecer ali é a sua referência real, porque é o preço "
            "que o mercado cobra de você, com o seu nome e o seu histórico."},
    {"layout": "item", "kicker": "Se a sua conta deu mais", "preco": "o desconto é o caro",
     "sem_cap": True,
     "nar": "Se o número que você calculou no capítulo anterior é maior que a "
            "taxa do seu banco, então o desconto à vista é a forma mais cara de "
            "antecipar dinheiro que você tem à disposição."},
    {"layout": "item", "kicker": "E se deu menos", "preco": "o desconto é o barato",
     "sem_cap": True,
     "nar": "E se deu menos, o desconto é o caminho mais barato e você deve "
            "continuar dando. Os dois resultados são úteis; o que não serve é "
            "não saber."},
    {"layout": "item", "kicker": "O erro comum", "preco": "comparar com nada",
     "sem_cap": True,
     "nar": "O erro mais comum não é dar desconto demais. É dar desconto sem "
            "ter nada do outro lado da comparação."},
    {"layout": "item", "kicker": "E é fácil cair nele", "preco": "porque não tem fatura",
     "sem_cap": True,
     "nar": "E é fácil cair nesse erro, porque o desconto não gera fatura, não "
            "gera extrato e não aparece em nenhuma linha da sua contabilidade "
            "como despesa financeira."},
]

C4 = [
    {"layout": "titulo", "kicker": "Prazos diferentes", "sub": "mudam tudo",
     "cap": "Quando o prazo não é de trinta dias",
     "nar": "Até aqui o exemplo antecipou trinta dias, e isso tornou a conta "
            "direta. Mas o seu caso pode ser outro prazo."},
    {"layout": "item", "kicker": "A regra", "preco": "proporção pelos dias",
     "sem_cap": True,
     "nar": "A regra é proporção. Você tem o juro do período; para passar para "
            "o mês, multiplique por trinta e divida pelos dias que antecipou."},
    {"layout": "item", "kicker": "Antecipou 60 dias", "preco": "11,1 × 30 ÷ 60 = 5,6%",
     "sem_cap": True,
     "nar": "Suponha dez por cento de desconto, mas para antecipar sessenta "
            "dias. O juro do período continua onze vírgula um. Agora divida "
            "pela metade, porque o prazo dobrou. Dá cinco vírgula seis por "
            "cento ao mês."},
    {"layout": "item", "kicker": "Antecipou 15 dias", "preco": "5,3 × 30 ÷ 15 = 10,6%",
     "sem_cap": True,
     "nar": "Agora o contrário. Desconto de cinco por cento, mas antecipando "
            "só quinze dias. O juro do período é cinco vírgula três. Multiplique "
            "por dois, porque o prazo é metade de um mês. Dez vírgula seis por "
            "cento."},
    {"layout": "item", "kicker": "Repare", "preco": "desconto menor, juro maior",
     "sem_cap": True,
     "nar": "Repare no que acabou de acontecer. O desconto de cinco por cento "
            "custou quase o mesmo que o de dez, porque o prazo era metade."},
    {"layout": "item", "kicker": "O que pesa", "preco": "não é o desconto, é o prazo",
     "sem_cap": True,
     "nar": "É isso que a conta revela: o que decide o custo não é o tamanho do "
            "desconto, é a relação entre ele e o prazo que você antecipou."},
    {"layout": "item", "kicker": "Uma ressalva honesta", "preco": "isso é aproximação",
     "sem_cap": True,
     "nar": "E uma ressalva: essa proporção é uma aproximação. A conta exata usa "
            "juro composto e dá um número um pouco maior; para decidir se vale "
            "ou não, a proporção já resolve."},
]

C5 = [
    {"layout": "titulo", "kicker": "Quando dar desconto", "sub": "é certo",
     "cap": "Quando o desconto é a decisão certa",
     "nar": "Este vídeo não é contra dar desconto à vista. Existem três "
            "situações em que ele é a melhor decisão disponível."},
    {"layout": "item", "kicker": "Primeira", "preco": "o cliente não pagaria",
     "sem_cap": True,
     "nar": "A primeira é risco. Se há chance real de o cliente atrasar ou não "
            "pagar, o desconto não está comprando prazo: está comprando "
            "certeza, e certeza vale caro."},
    {"layout": "item", "kicker": "Segunda", "preco": "você precisa do caixa hoje",
     "sem_cap": True,
     "nar": "A segunda é caixa. Se você precisa do dinheiro nesta semana para "
            "pagar algo que não espera, onze por cento ao mês pode ser mais "
            "barato que a multa do que você deixaria de pagar."},
    {"layout": "item", "kicker": "Terceira", "preco": "o desconto compra volume",
     "sem_cap": True,
     "nar": "A terceira é volume. Se o desconto fecha um contrato maior ou "
            "garante os próximos três meses de trabalho, ele deixou de ser "
            "custo financeiro e virou investimento comercial."},
    {"layout": "item", "kicker": "Em todas as três", "preco": "você decide SABENDO",
     "sem_cap": True,
     "nar": "Nas três você continua dando o desconto. A diferença é que agora "
            "você sabe quanto ele custa, e pode dizer o número em voz alta na "
            "negociação."},
    {"layout": "item", "kicker": "E isso muda a conversa", "preco": "de favor para troca",
     "sem_cap": True,
     "nar": "Isso muda a conversa com o cliente. Deixa de ser um favor que você "
            "faz e passa a ser uma troca com preço, que é o que ela sempre foi."},
    {"layout": "item", "kicker": "Um exemplo de frase", "preco": "para usar",
     "sem_cap": True,
     "nar": "Uma frase que funciona na negociação. Esse desconto equivale a "
            "onze por cento ao mês para mim. Consigo fazer metade dele se o "
            "pagamento sair em até uma semana."},
]

C6 = [
    {"layout": "titulo", "kicker": "O lado do cliente", "sub": "por que ele pede",
     "cap": "Por que o cliente pede, e o que ele sabe",
     "nar": "Vale entender por que esse pedido chega tão certeiro, tantas vezes, "
            "de clientes diferentes."},
    {"layout": "item", "kicker": "Para a empresa", "preco": "é crédito sem banco",
     "sem_cap": True,
     "nar": "Para uma empresa organizada, pedir desconto à vista é captar "
            "crédito sem banco, sem garantia e sem análise de risco. E o "
            "credor dessa operação é você, que nem foi consultado sobre a "
            "taxa."},
    {"layout": "item", "kicker": "E o departamento financeiro", "preco": "calcula isso",
     "sem_cap": True,
     "nar": "E do outro lado da mesa esse número costuma estar calculado. "
            "Departamento financeiro tem taxa interna e compara as duas antes "
            "de fazer o pedido."},
    {"layout": "item", "kicker": "Então a assimetria", "preco": "é de informação",
     "sem_cap": True,
     "nar": "A assimetria da negociação não é de tamanho nem de poder. É de "
            "informação: um lado sabe a taxa e o outro não."},
    {"layout": "item", "kicker": "A conta do capítulo 2", "preco": "fecha essa diferença",
     "sem_cap": True,
     "nar": "A divisão que você fez no segundo capítulo fecha essa diferença em "
            "dez segundos, e ela é a mesma conta que o financeiro da empresa "
            "faz do lado dele."},
    {"layout": "item", "kicker": "Não é jogo sujo", "preco": "é prática normal",
     "sem_cap": True,
     "nar": "E não estou dizendo que é jogo sujo. É prática normal de gestão de "
            "caixa, e funciona porque o prestador raramente faz a conta."},
    {"layout": "item", "kicker": "O que muda", "preco": "é você ter o número",
     "sem_cap": True,
     "nar": "O que muda quando você tem o número é simples: você para de "
            "responder por intuição e passa a responder por comparação. E "
            "quem responde por comparação negocia melhor, mesmo quando "
            "termina aceitando o pedido."},
]

C7 = [
    {"layout": "titulo", "kicker": "O desconto na tabela", "sub": "é pior ainda",
     "cap": "O desconto que mora na sua tabela de preços",
     "nar": "Falta o caso mais caro de todos, e ele não acontece numa "
            "negociação. Ele mora na sua tabela de preços."},
    {"layout": "item", "kicker": "Desconto padrão", "preco": "para todo mundo",
     "sem_cap": True,
     "nar": "É o desconto fixo à vista que você oferece para todo cliente, "
            "sempre, escrito na proposta antes de qualquer conversa."},
    {"layout": "item", "kicker": "Por que é pior", "preco": "você paga sem precisar",
     "sem_cap": True,
     "nar": "Ele é pior porque você paga a taxa inclusive para o cliente que "
            "pagaria à vista de qualquer jeito, e para aquele que nunca teria "
            "pedido desconto nenhum. Você financia quem não precisava."},
    {"layout": "item", "kicker": "Faça esta conta", "preco": "em quantos orçamentos?",
     "sem_cap": True,
     "nar": "Olhe os seus últimos dez orçamentos fechados e conte em quantos "
            "deles o desconto à vista foi usado. Esse é o único número que diz "
            "se ele serve."},
    {"layout": "item", "kicker": "Se quase todos usaram", "preco": "o preço é o descontado",
     "sem_cap": True,
     "nar": "Se quase todos usaram, o seu preço real é o preço com desconto, e "
            "o preço cheio da sua tabela é ficção."},
    {"layout": "item", "kicker": "Se quase ninguém usou", "preco": "ele não compra nada",
     "sem_cap": True,
     "nar": "E se quase ninguém usou, ele não está comprando antecipação "
            "nenhuma: está só reduzindo a sua margem nos poucos casos em que "
            "alguém reparou."},
    {"layout": "item", "kicker": "Em todo caso", "preco": "a tabela precisa decidir",
     "sem_cap": True,
     "nar": "Nos dois casos a tabela precisa de uma decisão sua, e não de um "
            "número que ficou lá porque alguém copiou de outra proposta "
            "antiga. Revisar esse campo é a coisa mais barata que você faz "
            "nesta semana."},
]

C8 = [
    {"layout": "titulo", "kicker": "Agora, na sua proposta", "sub": "três passos",
     "cap": "Três passos na sua última proposta",
     "nar": "Antes de fechar o vídeo, faça os três passos na sua última "
            "proposta. Leva menos de um minuto."},
    {"layout": "item", "kicker": "Passo 1", "preco": "o desconto em por cento",
     "sem_cap": True,
     "nar": "Primeiro: pegue o desconto à vista que você deu, em por cento. "
            "Se na proposta ele está em reais, divida pelo valor cheio e "
            "multiplique por cem."},
    {"layout": "item", "kicker": "Passo 2", "preco": "desconto ÷ o que sobra",
     "sem_cap": True,
     "nar": "Segundo: divida esse desconto pelo que sobra dos cem. Dez por "
            "noventa, cinco por noventa e cinco."},
    {"layout": "lista", "kicker": "Passo 3 — o ajuste do prazo", "sem_cap": True,
     "itens": ["× 30 ÷ dias antecipados = % ao mês",
               "compare com a taxa do seu banco, no app",
               "maior que ela? o desconto é o caro"],
     "nar": "Terceiro: multiplique por trinta, divida pelos dias que você "
            "antecipou, e compare com a taxa do seu próprio banco."},
    {"layout": "item", "kicker": "Guarde o número", "preco": "para a próxima negociação",
     "sem_cap": True,
     "nar": "Guarde o resultado em algum lugar que você vê rápido, de "
            "preferência no mesmo arquivo da sua tabela de preços. Ele serve "
            "na próxima vez que alguém pedir, e pedir vai pedir."},
    {"layout": "item", "kicker": "Nenhum número daqui", "preco": "é de terceiro",
     "sem_cap": True,
     "nar": "E repare: nenhum número deste vídeo veio de lei, de pesquisa ou de "
            "banco. Os três são seus, e eu expliquei na descrição por que fiz "
            "questão disso."},
    {"layout": "cta", "kicker": "Quanto deu o seu?",
     "sub": "escreve nos comentários", "sem_cap": True,
     "nar": "Escreve nos comentários quanto deu o seu, em por cento ao mês. "
            "Neste canal todo vídeo termina numa conta que você faz no seu "
            "próprio dinheiro; se serviu, se inscreve."},
]

CENAS = C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8

# SHORT: os dois campeoes deste canal tem 41 s e 32 s. Alvo ~35 s.
SHORT = [
    {"layout": "titulo", "kicker": "Desconto para pagar à vista",
     "sub": "você emprestou dinheiro", "sem_cap": True,
     "nar": "Quando você dá desconto para o cliente pagar à vista, quem pagou "
            "juros foi você."},
    {"layout": "titulo", "kicker": "A conta", "sub": "desconto ÷ o que sobra",
     "sem_cap": True,
     "nar": "Divida o desconto pelo que sobra dos cem. Dez por cento viram dez "
            "dividido por noventa: onze vírgula um por cento."},
    {"layout": "titulo", "kicker": "Antecipou 30 dias?",
     "sub": "11,1% AO MÊS", "sem_cap": True,
     "nar": "Se você antecipou trinta dias, esse é o juro ao mês que você "
            "cobrou de si mesmo."},
    {"layout": "titulo", "kicker": "Compare no app do seu banco",
     "sub": "antecipação de recebíveis", "sem_cap": True,
     "nar": "Compare com a antecipação de recebíveis do seu banco. Deu mais? O "
            "desconto é o jeito mais caro que você tem."},
    {"layout": "cta", "kicker": "A conta inteira está no canal",
     "sub": "com prazos diferentes", "sem_cap": True,
     "nar": "No canal tem a conta com outros prazos e os três casos em que vale "
            "dar o desconto mesmo assim."},
]

THUMB = {"l1": "Desconto", "l2": "é juro"}

COPY = """# Desconto a vista: o juro que voce cobra de si mesmo

## TITULO
Desconto para Pagar à Vista: Divida por 90 e Veja o Juro que Você Está Pagando

## TITULO SHORT
Desconto à vista é juro. Quanto?

## DESCRICAO
O cliente aprova o orçamento e pede um desconto para pagar à vista. Você aceita, porque dinheiro na mão hoje parece sempre melhor do que dinheiro daqui a um mês. E parece não custar nada: não houve contrato de empréstimo, nem tarifa, nem banco.

Só que houve um empréstimo ali, e ele foi ao contrário do que a maioria imagina. Quem pagou juros foi você; quem recebeu foi o cliente, que ficou com o dinheiro dele mais tempo e pagou menos por isso. A taxa existe — ela só não está escrita em lugar nenhum da sua proposta.

A conta tem dois números, e os dois estão na última proposta que você enviou: o desconto que você deu, em porcentagem, e quantos dias você antecipou.

A divisão é esta: **pegue o desconto e divida pelo que sobra dos cem, não pelos cem.** Dez por cento de desconto é dez dividido por noventa — 11,1%. Se você antecipou trinta dias, esse é o juro ao mês que você pagou. Por que noventa e não cem? Porque noventa é o que realmente entrou no seu bolso, e juro se mede sobre o que entrou, não sobre o preço de tabela.

Para outros prazos, a regra é proporção: multiplique por trinta e divida pelos dias antecipados. Dez por cento para antecipar sessenta dias dá 5,6% ao mês. Cinco por cento para antecipar quinze dias dá 10,6% — quase o mesmo que o desconto de dez. É isso que a conta revela: o que decide o custo não é o tamanho do desconto, é a relação entre ele e o prazo.

No vídeo tem também: por que não cito taxa de banco nenhuma e mando você olhar o app do seu próprio banco; os três casos em que dar o desconto é a decisão certa mesmo custando 11% ao mês (risco de inadimplência, necessidade de caixa e desconto que compra volume); por que o pedido chega tão certeiro de clientes diferentes; e o caso mais caro de todos, que é o desconto fixo que mora na sua tabela de preços e você paga até para quem pagaria à vista de qualquer jeito.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Os três passos, para fazer agora na sua última proposta: (1) o desconto à vista que você deu, em %. (2) divida pelo que sobra dos cem — 10 ÷ 90 = 11,1%. (3) multiplique por 30, divida pelos dias que você antecipou, e compare com a taxa de antecipação do SEU banco, no app. Deu mais que ela? O desconto é a forma mais cara de antecipar que você tem. Quanto deu o seu?

## HASHTAGS
#Precificacao #PrestadorDeServico #LabTreinamento

## TAGS
desconto a vista, antecipacao de recebiveis, juros implicitos, precificacao servico, prestador de servico autonomo, fluxo de caixa, negociacao com cliente, tabela de precos, margem de lucro, capital de giro, orcamento servico, como calcular juros, desconto no orcamento, financas para autonomo, gestao financeira

## CONFIGURACOES DO STUDIO
Categoria: Educação. Idioma: Português do Brasil. Não é para crianças. Contém mídia sintética.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este vídeo não cita nenhum número de terceiro — nem taxa de banco, nem lei, nem pesquisa. Os três números que decidem são seus: o desconto que você deu, os dias que você antecipou, e a taxa que o seu próprio banco oferece no app dele.

E isso foi uma DECISÃO, não uma preferência. A pauta original era o Fator R do Simples Nacional, que depende do limite de 28% da Lei Complementar 123/2006. Tentei abrir o texto da lei no planalto.gov.br três vezes e a conexão foi cortada nas três (erro de leitura SSL). A regra deste canal é que número sem confirmação em fonte oficial não entra no vídeo — então ele não entrou, e eu redesenhei a pauta para que o número que decide fosse o seu. Preferi trocar de assunto a citar de memória.

As contas do vídeo são aritmética simples e você pode conferir todas: 10 ÷ 90 = 11,11%; 5 ÷ 95 = 5,26%; 11,11 × 30 ÷ 60 = 5,56%; 5,26 × 30 ÷ 15 = 10,53%.

UMA RESSALVA QUE O VÍDEO DIZ EM VOZ ALTA: a regra de proporção por dias é uma aproximação. A conta exata usa juro composto e dá um número um pouco maior — 10% por 30 dias antecipados equivale a cerca de 260% ao ano no composto, não a 133%. Para decidir se vale ou não, a aproximação resolve; para contrato, use a fórmula composta.

O QUE O VÍDEO NÃO AFIRMA: que dar desconto à vista seja errado. Um capítulo inteiro trata dos três casos em que ele é a decisão certa. O vídeo afirma só que o custo existe, que ele é calculável em dez segundos, e que decidir sem ele é decidir sem metade da informação.
"""


def _copy_existente():
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "labtreinamento-008.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8")).get("copy")
        if c:
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-008",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
