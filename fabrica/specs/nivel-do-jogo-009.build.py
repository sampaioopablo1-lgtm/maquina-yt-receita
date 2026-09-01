#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-009.

ALAVANCA ATACADA: **A — conversao short -> inscrito**, por EIXO NOVO. O
veredito do canal e `canal frio`, e a rotina manda eixo novo, nao mais um
video igual.

NUMERO DE PARTIDA, lido em 01/09/2026 20:15Z ja com o dado corrigido do
aprendizado 549 (as leituras anteriores deste canal estavam embaralhadas):

    nivel-do-jogo ..... 3 inscritos, 22 videos, 445 views
                        short: mediana 0,61 views/dia, topo 16,81
                        longo: mediana 0,16 views/dia, topo 1,06
                        veredito: `canal frio`
                        DEZ DUPLICATAS da "Lei Felca" somando 29 views

O QUE DEU CERTO — e e uma coisa so, e e um short:

    "Quantas Horas de Trabalho Custa GTA 6" .... short 250 views (16,81/dia)
    "EA FC 27: Standard, Ultimate ou Plus?" .... short  96 views ( 6,81/dia)

Os dois sao a MESMA forma: uma conta em reais sobre uma compra que o
espectador esta prestes a fazer. Sao tambem os dois unicos numeros do canal
que saem do chao.

O QUE NAO DEU: os longos, todos. O longo do GTA 6 fez DUAS views contra 250 do
short do mesmo pacote — cento e vinte e cinco para um. O do EA FC 27 fez
quinze contra noventa e seis. E o que fala da INDUSTRIA em vez do bolso do
jogador nao existe: "Demissoes na Square Enix" fez ZERO no longo, e as dez
copias da "Lei Felca" somam vinte e nove views entre todas.

Duracao nao explica: os dois maiores shorts sao justamente os pacotes de longo
MAIS LONGO do canal (768 s e 775 s), e os longos curtos (521 a 575 s) nao
foram melhores. O problema nao e o tamanho do longo, e que ninguem chega nele.

O EIXO NOVO, E POR QUE ELE E NOVO: os vinte e dois videos deste canal falam de
GASTAR — preco, edicao, cambio, assinatura, caixinha. Nenhum fala de
RECUPERAR. Este fala: o dinheiro que ja saiu e pode voltar, e o prazo que esta
correndo agora.

E ele cabe na frase da alavanca A sem forcar: no fim voce vai saber, olhando
DOIS numeros que ja estao na sua conta Steam, se a porta ainda esta aberta pra
voce — e qual das duas.

A CONTA, entregue no capitulo 2 (~133 s estimados):
    numero 1: a data da compra    -> quantos dias fazem
    numero 2: as horas jogadas
    porta A (politica da Steam): 14 dias E menos de 2 horas, as duas juntas
    porta B (CDC art. 49): 7 dias, e as horas NAO entram na conta

DIMENSIONAMENTO: `canal frio` nao define faixa. Apliquei por analogia a regra
do `suspenso` — piso de oito minutos e o melhor material no short — porque o
unico alcance medido do canal esta no short e porque a alavanca B manda ir ao
piso quando ha duvida. Alvo ~535 s (8min55s), 8 capitulos. Digo que e analogia,
nao regra: se o veredito ganhar faixa propria para `canal frio`, este numero
muda.

AS FONTES, e o que ficou de fora:
  * Prazo de 7 dias e a devolucao "de imediato, monetariamente atualizada":
    Lei 8.078/1990 (CDC), art. 49 e paragrafo unico, lido direto no
    planalto.gov.br nesta rodada.
  * O que o fornecedor tem de fazer no cartao: Decreto 7.962/2013, art. 5o,
    paragrafo 3o, tambem lido no planalto.gov.br. Sao DOIS atos normativos
    distintos, mas o publicador oficial e o mesmo (Planalto) — a pagina
    explicativa do gov.br/mj devolveu 404. Isso vai escrito no aviso.
  * 14 dias e duas horas: pagina oficial de reembolsos da Steam em portugues
    (store.steampowered.com/steam_refunds). E POLITICA DA EMPRESA, nao lei, e
    o roteiro diz isso com todas as letras — inclusive porque a propria pagina
    admite que "consumidores em certas jurisdicoes podem ter direitos
    adicionais".
  * O QUE O VIDEO NAO AFIRMA: que a Steam e obrigada a devolver no dia dez com
    dez horas jogadas. Isso e interpretacao judicial e eu nao tenho fonte para
    ela. O video diz o que cada porta EXIGE e para onde reclamar quando as
    duas divergem.
"""

C1 = [
    {"layout": "titulo", "kicker": "Você comprou", "sub": "e se arrependeu",
     "cap": "O prazo já está correndo",
     "nar": "Você comprou um jogo. Abriu, jogou um pouco, e não era aquilo. "
            "A pergunta agora não é se dá pra devolver. É quanto tempo "
            "ainda te resta."},
    {"layout": "item", "kicker": "O prazo não começa quando você decide",
     "preco": "começa na compra", "sem_cap": True,
     "nar": "E ele não começa a contar quando você desiste. Começa no dia da "
            "compra, e já está correndo enquanto você assiste isso."},
    {"layout": "item", "kicker": "Não existe UM prazo", "preco": "existem dois",
     "sem_cap": True,
     "nar": "A parte que quase ninguém sabe é que não existe um prazo. "
            "Existem dois, e eles não são iguais."},
    {"layout": "item", "kicker": "Um é política", "preco": "o outro é lei",
     "sem_cap": True,
     "nar": "Um é a política da loja, que ela escreve e pode mudar. O outro é "
            "lei brasileira, que a loja não escreve."},
    {"layout": "item", "kicker": "Os dois têm condições diferentes",
     "preco": "e prazos diferentes", "sem_cap": True,
     "nar": "Os dois têm prazos diferentes e exigem coisas diferentes de "
            "você. Um deles conta suas horas jogadas. O outro não."},
    {"layout": "item", "kicker": "Você não escolhe um", "preco": "você descobre qual te alcança",
     "sem_cap": True,
     "nar": "Então a pergunta certa não é qual é melhor. É qual dos dois "
            "ainda alcança a sua compra hoje."},
    {"layout": "item", "kicker": "Dois números", "preco": "você já tem os dois",
     "sem_cap": True,
     "nar": "Pra responder isso você precisa de dois números, e os dois já "
            "estão na sua conta. Vou pegar eles agora."},
]

C2 = [
    {"layout": "titulo", "kicker": "Abra sua conta", "sub": "os dois números",
     "cap": "Os dois números que decidem",
     "nar": "Abra a Steam, vá em ajuda e depois em compras recentes. Tudo o "
            "que você precisa está nessa tela."},
    {"layout": "item", "kicker": "Número 1", "preco": "a data da compra",
     "sem_cap": True,
     "nar": "O primeiro número é a data da compra. Conte quantos dias fazem "
            "desde ela até hoje."},
    {"layout": "item", "kicker": "Número 2", "preco": "as horas jogadas",
     "sem_cap": True,
     "nar": "O segundo é o tempo jogado, que aparece na sua biblioteca, "
            "embaixo do nome do jogo."},
    {"layout": "item", "kicker": "Porta A — política da Steam",
     "preco": "14 dias E menos de 2 horas", "sem_cap": True,
     "nar": "Primeira porta, a política da loja: quatorze dias desde a "
            "compra e menos de duas horas jogadas. As duas condições ao "
            "mesmo tempo."},
    {"layout": "item", "kicker": "Porta B — a lei", "preco": "7 dias, sem contar horas",
     "sem_cap": True,
     "nar": "Segunda porta, a lei: sete dias. E aqui as horas jogadas não "
            "entram na conta."},
    {"layout": "item", "kicker": "Faça agora", "preco": "duas comparações",
     "sem_cap": True,
     "nar": "Então são duas comparações. Seus dias são menos de quatorze e "
            "suas horas menos de duas? Porta A aberta. Seus dias são menos de "
            "sete? Porta B aberta."},
    {"layout": "item", "kicker": "Pronto", "preco": "a conta acabou",
     "sem_cap": True,
     "nar": "Essa é a conta inteira, e ela já acabou. O resto do vídeo é o "
            "que cada porta significa e o que fazer quando as duas discordam."},
]

C3 = [
    {"layout": "titulo", "kicker": "A porta A", "sub": "o que a Steam escreve",
     "cap": "A porta da loja: as duas condições juntas",
     "nar": "Vamos à primeira porta. A página oficial de reembolsos da Steam, "
            "em português, é bem direta sobre ela."},
    {"layout": "item", "kicker": "O texto oficial", "preco": "duas semanas, duas horas",
     "sem_cap": True,
     "nar": "Ela diz, com essas palavras, que a oferta de reembolso se "
            "aplica a jogos e softwares comprados na loja nas primeiras duas "
            "semanas após a data da compra e com menos de duas horas de uso."},
    {"layout": "item", "kicker": "E é E, não OU", "preco": "as duas ao mesmo tempo",
     "sem_cap": True,
     "nar": "Repare que são as duas juntas, e não uma ou outra. Cinco dias "
            "com três horas jogadas já fecha essa porta, mesmo você estando "
            "bem dentro do prazo de duas semanas."},
    {"layout": "item", "kicker": "Por qualquer motivo", "preco": "isso é generoso",
     "sem_cap": True,
     "nar": "Dentro dessas duas condições a política é generosa: a própria "
            "página diz que serve por qualquer motivo, inclusive não ter "
            "gostado."},
    {"layout": "item", "kicker": "E fora delas", "preco": "ainda é analisado",
     "sem_cap": True,
     "nar": "E ela acrescenta que, mesmo fora das regras, o pedido é "
            "analisado. Ou seja, pedir custa nada."},
    {"layout": "item", "kicker": "Onde se pede", "preco": "help.steampowered.com",
     "sem_cap": True,
     "nar": "O pedido é feito no help ponto steampowered ponto com, achando "
            "a compra na lista e escolhendo o motivo. Não precisa falar com "
            "ninguém e não tem telefone no meio."},
    {"layout": "item", "kicker": "Quanto demora", "preco": "até uma semana após aprovado",
     "sem_cap": True,
     "nar": "A página também diz o prazo do dinheiro: até uma semana depois "
            "da data em que o reembolso foi aprovado."},
]

C4 = [
    {"layout": "titulo", "kicker": "A porta B", "sub": "o que a lei diz",
     "cap": "A porta da lei: sete dias, sem condição de uso",
     "nar": "Agora a segunda porta, e ela não é da Steam. É do Código de "
            "Defesa do Consumidor."},
    {"layout": "item", "kicker": "Artigo 49", "preco": "prazo de 7 dias",
     "sem_cap": True,
     "nar": "O artigo quarenta e nove diz que o consumidor pode desistir do "
            "contrato no prazo de sete dias, contado da assinatura ou do "
            "recebimento do produto."},
    {"layout": "item", "kicker": "A condição", "preco": "fora do estabelecimento",
     "sem_cap": True,
     "nar": "A condição é que a contratação tenha acontecido fora do "
            "estabelecimento comercial. Compra pela internet é exatamente "
            "esse caso."},
    {"layout": "item", "kicker": "O que NÃO está lá", "preco": "nenhuma hora jogada",
     "sem_cap": True,
     "nar": "E agora o ponto: leia o artigo inteiro e não existe uma palavra "
            "sobre tempo de uso. A lei não conta suas horas."},
    {"layout": "item", "kicker": "O parágrafo único", "preco": "devolução de imediato",
     "sem_cap": True,
     "nar": "O parágrafo único vai além: os valores pagos serão devolvidos de "
            "imediato, monetariamente atualizados."},
    {"layout": "item", "kicker": "Prazo mais curto", "preco": "condição mais frouxa",
     "sem_cap": True,
     "nar": "Então repare na troca. A lei te dá menos tempo, sete contra "
            "quatorze, mas não te cobra as horas."},
    {"layout": "item", "kicker": "É por isso que são duas portas",
     "preco": "e não uma melhor", "sem_cap": True,
     "nar": "É por isso que eu chamei de duas portas e não de uma regra "
            "melhor que a outra. Elas pegam situações diferentes."},
]

C5 = [
    {"layout": "titulo", "kicker": "E o que a Steam diz", "sub": "sobre a lei",
     "cap": "A própria Steam reconhece a segunda porta",
     "nar": "Aqui vem a parte que costuma surpreender. Essa segunda porta não "
            "é uma interpretação minha."},
    {"layout": "item", "kicker": "Na mesma página", "preco": "uma frase curta",
     "sem_cap": True,
     "nar": "Na mesma página de reembolsos, uma frase curta diz que "
            "consumidores em certas jurisdições podem ter direitos "
            "adicionais a um reembolso."},
    {"layout": "item", "kicker": "Jurisdição", "preco": "é o país onde você compra",
     "sem_cap": True,
     "nar": "Jurisdição, aqui, é o país onde você está. E o Brasil é um "
            "desses países, por causa do artigo quarenta e nove."},
    {"layout": "item", "kicker": "Ou seja", "preco": "a política não substitui a lei",
     "sem_cap": True,
     "nar": "Ou seja, a política da loja não substitui a lei do seu país. "
            "Ela convive com ela."},
    {"layout": "item", "kicker": "O que eu NÃO estou dizendo",
     "preco": "que você ganha sempre", "sem_cap": True,
     "nar": "O que eu não estou dizendo é que você ganha sempre. Não estou "
            "afirmando que a Steam é obrigada a devolver no dia dez com dez "
            "horas jogadas."},
    {"layout": "item", "kicker": "Isso é caso a caso", "preco": "e eu não tenho fonte",
     "sem_cap": True,
     "nar": "Isso depende de decisão caso a caso e eu não tenho fonte "
            "oficial pra afirmar. Prefiro dizer o que cada porta exige."},
    {"layout": "item", "kicker": "O que dá pra afirmar", "preco": "os dois prazos",
     "sem_cap": True,
     "nar": "O que dá pra afirmar é o texto dos dois: quatorze dias e duas "
            "horas na política, sete dias sem contar horas na lei."},
]

C6 = [
    {"layout": "titulo", "kicker": "O dinheiro volta", "sub": "mas para onde?",
     "cap": "Para onde o dinheiro volta",
     "nar": "Aprovado o reembolso, falta a pergunta que quase ninguém faz "
            "antes: para onde esse dinheiro volta?"},
    {"layout": "item", "kicker": "Steam", "preco": "carteira ou pagamento original",
     "sem_cap": True,
     "nar": "A página da Steam diz que você recebe na sua Carteira Steam ou "
            "diretamente na forma de pagamento original."},
    {"layout": "item", "kicker": "A diferença é enorme", "preco": "carteira não sai da Steam",
     "sem_cap": True,
     "nar": "E a diferença entre as duas é enorme. Dinheiro na Carteira só "
            "serve pra comprar na Steam de novo. Ele não volta pro seu banco."},
    {"layout": "item", "kicker": "Peça o original", "preco": "quando puder escolher",
     "sem_cap": True,
     "nar": "Então, quando o formulário te deixar escolher, peça na forma de "
            "pagamento original. Só aceite a Carteira se for a única opção."},
    {"layout": "item", "kicker": "E a lei", "preco": "diz o que fazer no cartão",
     "sem_cap": True,
     "nar": "Do lado da lei existe uma regra específica pro cartão, e ela "
            "está no decreto que regula o comércio eletrônico."},
    {"layout": "item", "kicker": "Decreto de 2013", "preco": "artigo 5º, parágrafo 3º",
     "sem_cap": True,
     "nar": "O artigo quinto diz que o fornecedor comunica imediatamente a "
            "administradora do cartão para que a transação não seja lançada "
            "na fatura, ou seja estornada se já tiver sido."},
    {"layout": "item", "kicker": "Confira na fatura", "preco": "é lá que se prova",
     "sem_cap": True,
     "nar": "Então a conferência final não é no e-mail de confirmação. É na "
            "sua fatura, no mês seguinte."},
]

C7 = [
    {"layout": "titulo", "kicker": "Quando nenhuma porta abre",
     "sub": "e o que ainda dá", "cap": "Quando as duas portas estão fechadas",
     "nar": "Falta o caso ruim: você passou dos quatorze dias, ou passou das "
            "duas horas e também dos sete dias."},
    {"layout": "item", "kicker": "Peça mesmo assim", "preco": "custa zero",
     "sem_cap": True,
     "nar": "Primeiro, peça mesmo assim. A própria página diz que o pedido "
            "fora da regra ainda é analisado, e um pedido negado não te tira "
            "nada."},
    {"layout": "item", "kicker": "Jogo com defeito", "preco": "é outro caminho",
     "sem_cap": True,
     "nar": "Segundo, se o problema é o jogo não funcionar, isso não é "
            "arrependimento. É produto com defeito, e o caminho é outro."},
    {"layout": "item", "kicker": "Se a loja negar", "preco": "consumidor.gov.br e Procon",
     "sem_cap": True,
     "nar": "Terceiro, se você acha que estava dentro da lei e foi negado, "
            "existe o consumidor ponto gov ponto br e existe o Procon do seu "
            "estado."},
    {"layout": "item", "kicker": "Guarde os dois números", "preco": "data e horas",
     "sem_cap": True,
     "nar": "E pra qualquer um desses caminhos, guarde os mesmos dois "
            "números do começo: a data da compra e as horas jogadas. É com "
            "eles que você prova."},
    {"layout": "item", "kicker": "Print da tela", "preco": "vale mais que memória",
     "sem_cap": True,
     "nar": "Tire um print da tela de compras recentes hoje. Daqui a um mês "
            "essa tela pode estar diferente e a sua memória não vale como "
            "prova."},
    {"layout": "item", "kicker": "E o mais importante", "preco": "não deixe o prazo passar",
     "sem_cap": True,
     "nar": "Mas nada disso substitui a coisa mais simples: não deixar o "
            "prazo passar enquanto você decide."},
]

C8 = [
    {"layout": "titulo", "kicker": "Agora, na sua conta", "sub": "três passos",
     "cap": "Três passos na sua conta",
     "nar": "Antes de sair, faça os três passos na sua própria conta. Leva "
            "menos tempo do que o resto deste vídeo."},
    {"layout": "item", "kicker": "Passo 1", "preco": "quantos dias desde a compra",
     "sem_cap": True,
     "nar": "Passo um: em compras recentes, veja a data e conte os dias até "
            "hoje."},
    {"layout": "item", "kicker": "Passo 2", "preco": "quantas horas jogadas",
     "sem_cap": True,
     "nar": "Passo dois: na biblioteca, embaixo do nome do jogo, veja o "
            "tempo jogado. É o mesmo número que a loja usa pra decidir."},
    {"layout": "lista", "kicker": "Passo 3 — as duas comparações", "sem_cap": True,
     "itens": ["menos de 14 dias E menos de 2 horas → porta da loja",
               "menos de 7 dias, qualquer hora → porta da lei",
               "nenhuma das duas → peça assim mesmo"],
     "nar": "Passo três: as duas comparações, e a resposta sai sozinha."},
    {"layout": "item", "kicker": "Se alguma abriu", "preco": "peça hoje, não amanhã",
     "sem_cap": True,
     "nar": "Se alguma das duas abriu, peça hoje. Os dois prazos são curtos e "
            "os dois contam desde a compra, não desde a sua decisão."},
    {"layout": "item", "kicker": "As fontes", "preco": "estão na descrição",
     "sem_cap": True,
     "nar": "Os dois textos que eu li, o do código de defesa do consumidor "
            "e o do decreto do comércio eletrônico, estão na descrição, junto "
            "com a página oficial de reembolsos da Steam. Escrevi lá também o "
            "que este vídeo não afirma."},
    {"layout": "cta", "kicker": "Qual porta abriu pra você?",
     "sub": "escreve nos comentários", "sem_cap": True,
     "nar": "Escreve nos comentários qual das duas portas abriu pra você. "
            "Neste canal todo vídeo termina numa conta que você faz no seu "
            "próprio dinheiro; se serviu, se inscreve."},
]

CENAS = C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8

SHORT = [
    {"layout": "titulo", "kicker": "Comprou e se arrependeu?",
     "sub": "não existe um prazo, existem dois", "sem_cap": True,
     "nar": "Comprou o jogo e se arrependeu? Não existe um prazo pra "
            "devolver. Existem dois."},
    {"layout": "titulo", "kicker": "Porta 1 — a loja",
     "sub": "14 dias E menos de 2h", "sem_cap": True,
     "nar": "A política da Steam: quatorze dias e menos de duas horas "
            "jogadas. As duas juntas."},
    {"layout": "titulo", "kicker": "Porta 2 — a lei",
     "sub": "7 dias, sem contar horas", "sem_cap": True,
     "nar": "O código de defesa do consumidor: sete dias. E aqui as horas "
            "jogadas não entram na conta."},
    {"layout": "titulo", "kicker": "Abra compras recentes",
     "sub": "data e horas jogadas", "sem_cap": True,
     "nar": "Pegue a data da compra e o tempo jogado. Compare com os dois "
            "prazos e você já sabe."},
    {"layout": "cta", "kicker": "Toda semana uma conta dessas",
     "sub": "se inscreve", "sem_cap": True,
     "nar": "Aqui todo vídeo termina numa conta que você faz no seu próprio "
            "dinheiro. Se serviu, se inscreve."},
]

THUMB = {"l1": "Dois prazos", "l2": "não um"}

COPY = """# Reembolso de jogo: os dois prazos que correm ao mesmo tempo

## TITULO
Reembolso de Jogo: São Dois Prazos, Não Um — Descubra Qual Ainda Vale pra Você

## TITULO SHORT
Reembolso de jogo: são dois prazos

## DESCRICAO
Você comprou um jogo, abriu, e não era aquilo. A pergunta não é se dá pra devolver — é quanto tempo ainda te resta. E a parte que quase ninguém sabe é que não existe UM prazo. Existem dois, eles correm ao mesmo tempo, e exigem coisas diferentes de você.

A primeira porta é a política da loja. A página oficial de reembolsos da Steam, em português, diz que o reembolso se aplica a jogos comprados nas primeiras duas semanas e com menos de duas horas de uso. São as duas condições juntas: cinco dias com três horas jogadas já fecha essa porta, mesmo dentro do prazo.

A segunda porta é lei brasileira. O artigo 49 do Código de Defesa do Consumidor dá sete dias para desistir do contrato quando a contratação acontece fora do estabelecimento comercial — que é o caso de qualquer compra pela internet. E o texto do artigo não menciona tempo de uso em lugar nenhum: a lei não conta suas horas jogadas. O parágrafo único ainda diz que os valores pagos serão devolvidos de imediato, monetariamente atualizados.

A troca entre as duas é essa: a lei te dá menos tempo, sete contra quatorze, mas não te cobra as horas. Por isso a pergunta certa não é qual é melhor, é qual das duas ainda alcança a sua compra hoje.

No vídeo você faz a conta com dois números que já estão na sua conta: a data da compra, em compras recentes, e o tempo jogado, na biblioteca. Duas comparações e a resposta sai.

Também está lá: por que a própria página da Steam reconhece que consumidores de certas jurisdições têm direitos adicionais; a diferença entre receber na Carteira Steam e na forma de pagamento original, que é a diferença entre o dinheiro voltar pro seu banco ou ficar preso na loja; o que o Decreto 7.962/2013 manda o fornecedor fazer no seu cartão; e o que ainda dá pra fazer quando as duas portas já fecharam.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
As duas comparações, pra fazer agora: (1) menos de 14 dias E menos de 2 horas jogadas → porta da loja aberta. (2) menos de 7 dias, não importa quantas horas → porta da lei aberta. (3) nenhuma das duas → peça assim mesmo, a própria Steam diz que analisa fora da regra. Qual abriu pra você?

## HASHTAGS
#Reembolso #Steam #NivelDoJogo

## TAGS
reembolso steam, como pedir reembolso steam, prazo reembolso jogo, direito de arrependimento, artigo 49 cdc, codigo de defesa do consumidor, devolver jogo steam, 2 horas steam, carteira steam, estorno cartao compra online, decreto 7962, consumidor jogos, comprei e me arrependi, reembolso jogo digital, direitos do gamer

## CONFIGURACOES DO STUDIO
Categoria: Educação. Idioma: Português do Brasil. Não é para crianças. Contém mídia sintética.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Prazo de 7 dias, a condição de "fora do estabelecimento comercial" e a devolução "de imediato, monetariamente atualizados": Lei 8.078/1990 (Código de Defesa do Consumidor), artigo 49 e parágrafo único, lido direto em planalto.gov.br.

O que o fornecedor deve fazer no cartão: Decreto 7.962/2013, artigo 5º, parágrafo 3º, também lido em planalto.gov.br.

RESSALVA DE FONTE, e ela é minha: são dois atos normativos diferentes, mas o publicador oficial é o mesmo (Planalto). A página explicativa do gov.br/mj sobre direito de arrependimento devolveu 404 quando tentei abrir. Então o texto da lei está conferido na fonte primária, mas não em duas instituições distintas.

Os 14 dias e as 2 horas: página oficial de reembolsos da Steam em português (store.steampowered.com/steam_refunds). Isso é POLÍTICA DA EMPRESA, não lei — ela escreve e pode mudar. A mesma página diz que "consumidores em certas jurisdições podem ter direitos adicionais a um reembolso", e é essa a frase que reconhece a segunda porta.

O QUE ESTE VÍDEO NÃO AFIRMA: que a Steam é obrigada a devolver seu dinheiro no décimo dia com dez horas jogadas. Isso depende de decisão caso a caso e eu não tenho fonte oficial para afirmar. O vídeo diz o que cada porta EXIGE, e para onde reclamar quando as duas divergem — consumidor.gov.br e o Procon do seu estado.
"""


def _copy_existente():
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "nivel-do-jogo-009.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8")).get("copy")
        if c:
            return c
    return COPY


SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-009",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1B4332", "c1": "#D64570", "c2": "#7FB069", "bg": "#EFF6F1"},
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
    grava(SPEC, "fabrica/specs/nivel-do-jogo-009.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
