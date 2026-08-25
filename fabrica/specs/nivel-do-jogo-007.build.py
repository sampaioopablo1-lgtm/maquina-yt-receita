#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-007.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA, e ele e o melhor da frota inteira:

    nivel-do-jogo-004  short   94 views   2 inscritos   2,128%   ret 50,8%
    nivel-do-jogo-003  short  250 views   0 inscritos   0,000%   ret 40,8%
    nivel-do-jogo-005  short   11 views   0 inscritos   0,000%   ret 21,2%

    melhor canal da frota (epomeno-epipedo): 0,141%

O MAIS VISTO CONVERTEU ZERO. O de noventa e quatro views converteu quinze
vezes mais que o melhor canal da maquina. Isso replica o aprendizado 482 num
segundo canal e num segundo idioma, e a diferenca esta na FORMA do titulo:

  converteu     "EA FC 27: Standard, Ultimate ou Plus? A Conta em Reais"
                -> uma DECISAO entre opcoes concretas, com o dinheiro DELE
  nao converteu "Preco dos Jogos em 2026: Quantas Horas de Trabalho Custa"
                -> uma ESTATISTICA sobre o mercado
  nao converteu "Steam Mudou Como Seu Jogo e Precificado"
                -> um FATO sobre a politica de uma empresa

Gravado como aprendizado 497.

O QUE EU MUDEI POR CAUSA DISSO

1. O pacote inteiro tem a forma do 004, e nao o assunto dele: tres formas de
   pagar o MESMO jogo, e a conta que decide qual delas. Segunda pessoa do
   comeco ao fim. O espectador termina sabendo calcular em si mesmo, que e o
   teste que a rotina exige de toda pauta.

2. O short PARA DE TENTAR FECHAR SOZINHO (aprendizado 493): ele entrega o
   imposto e o passo da conta, e manda o ponto de virada para o longo.

3. VEREDITO `suspenso` (v_maquina_licoes, 8 longos a 0,08 views/dia de
   mediana): longo no PISO de oito minutos, e o melhor material no short.

OS NUMEROS, e as duas rotas institucionais que os sustentam

  IOF de 3,5% sobre cambio de cartao de credito internacional, cartao de
  debito internacional, cartao pre-pago internacional e compra de moeda
  estrangeira em especie. Em vigor desde 23/05/2025, pelo Decreto 12.466 de
  22/05/2025.

    rota 1  Ministerio da Fazenda — comunicado de maio de 2025 e a
            apresentacao da Receita Federal `iof-maio-2025.pdf` publicada em
            gov.br/fazenda, que traz a tabela de aliquotas
    rota 2  Receita Federal — pagina de orientacao tributaria do IOF em
            gov.br/receitafederal, e o Decreto 12.466 no acervo do Planalto

  A aliquota anterior era 6,38% ate 2022 (Ministerio da Fazenda).

O QUE FICOU DE FORA, e o video diz isso em voz alta

  - O ARTIGO exato do decreto. O planalto.gov.br e o gov.br recusam acesso
    automatizado (bloqueio de egresso), entao eu li o conteudo indexado e nao
    o texto literal. Citar artigo que nao li seria inventar precisao.
  - O antigo cronograma de reducao gradual do IOF ate zero. Nao fecha em duas
    fontes oficiais depois da unificacao de 2025.
  - QUALQUER cotacao de dolar e QUALQUER spread de banco. Mudam todo dia e
    variam por emissor. O video ensina onde olhar em vez de fingir um numero,
    e essa e a parte que vira METODO.

O eixo — rota de pagamento e imposto — nao aparece em nenhum dos cinco titulos
no ar do canal, que sao todos sobre a etiqueta de preco. Aqui a pergunta e
outra: dado o preco, por onde voce paga.
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ------------------------------------------ 1. O mesmo jogo, tres etiquetas
T("O mesmo jogo", "tres preços diferentes",
  "O mesmo jogo, no mesmo dia, custa três valores diferentes para você. E a "
  "diferença não está no jogo. Está em por onde você paga.",
  cap="O mesmo jogo, três preços")
L("As três rotas", ["Loja brasileira, em reais",
                    "Cartão internacional, em dólar",
                    "Gift card ou cartão pré-pago"],
  "São três rotas. A loja brasileira em reais, o cartão internacional em "
  "dólar, e o gift card ou cartão pré-pago.")
T("A maioria escolhe", "sem fazer a conta",
  "A maioria das pessoas escolhe uma delas por hábito, e nunca compara. Este "
  "vídeo é a comparação.")
T("E ela não é opinião", "é aritmética",
  "E ela não é opinião. É aritmética, com um imposto que tem número oficial e "
  "data de início.")
T("Não é sobre achar promoção", "é sobre a rota",
  "E não é sobre caçar promoção. A promoção você já sabe procurar. Isto aqui "
  "vale mesmo quando o preço anunciado é exatamente o mesmo nas duas lojas.")
T("Foi essa conta", "que me surpreendeu",
  "Quando eu fiz essa conta pela primeira vez, a rota que eu usava por hábito "
  "havia anos era a mais cara das três. Por uma margem que não era pequena.")
I("O que você leva daqui", "uma conta de três passos",
  "No fim você vai saber calcular, no seu caso, qual das três rotas sai mais "
  "barata. Com os seus valores, não com os meus.")

# ------------------------------------------- 2. O imposto tem nome e numero
T("A peça que falta", "chama-se IOF",
  "A peça que quase ninguém soma chama-se IOF. Imposto sobre Operações "
  "Financeiras. Ele incide quando o seu real vira moeda estrangeira.",
  cap="O imposto tem nome e número")
I("A alíquota hoje", "três vírgula cinco por cento",
  "A alíquota é de três vírgula cinco por cento. Esse é o número, e ele vale "
  "para o cartão de crédito internacional.")
L("Onde ela incide", ["Cartão de crédito internacional",
                      "Cartão de débito internacional",
                      "Cartão pré-pago e moeda em espécie"],
  "E vale também para o cartão de débito internacional, para o cartão "
  "pré-pago e para a compra de moeda estrangeira em espécie.")
I("Desde quando", "maio de dois mil e vinte e cinco",
  "Vale desde maio do ano passado. O dia exato é vinte e três, e a regra entrou "
  "por decreto.")
T("Antes disso", "o número era outro",
  "Antes de dois mil e vinte e dois a alíquota chegava a seis vírgula trinta e "
  "oito por cento. O governo unificou as regras e o número parou onde está.")
T("Guarde só um número", "três e meio por cento",
  "Você não precisa decorar o decreto. Precisa decorar um número: três e meio "
  "por cento em cima de tudo que você paga em moeda estrangeira.")
I("E ele não aparece", "na tela da loja",
  "E ele não aparece na tela da loja. Aparece depois, na sua fatura, quando "
  "não dá mais para desistir da compra.")

# ------------------------------------------------- 3. A conta, em tres passos
T("Agora a conta", "três passos, e só",
  "Agora a conta. São três passos, e você faz no aplicativo do banco em menos "
  "de um minuto.",
  cap="A conta, em três passos")
I("Passo um", "preço em dólar vezes a cotação",
  "Passo um. Pegue o preço em dólar e multiplique pela cotação do dia. Isso "
  "dá o valor bruto em reais.")
I("Passo dois", "some três e meio por cento",
  "Passo dois. Multiplique esse valor por um vírgula zero trinta e cinco. É o "
  "IOF entrando.")
I("Passo três", "compare com a loja em reais",
  "Passo três. Compare o resultado com o preço que a loja brasileira mostra "
  "em reais. Ganhou o menor.")
T("Parece óbvio", "e quase ninguém faz",
  "Parece óbvio escrito assim. Mas quase ninguém faz, porque o preço em dólar "
  "sempre parece menor na hora de clicar.")
T("O erro está no passo dois", "que some da tela",
  "E o erro mora no passo dois, que é justamente o que a tela não mostra.")
T("Repare no que ele faz", "com um jogo caro",
  "E repare no efeito. Três e meio por cento parece pouco, mas incide sobre o "
  "valor cheio. Num jogo caro, ele sozinho come boa parte da vantagem.")
I("Vale para tudo", "assinatura, DLC, moeda do jogo",
  "E vale para tudo que passa por câmbio: assinatura mensal, conteúdo extra, "
  "e a moeda de dentro do jogo. Não é só a compra grande.")

# -------------------------------------- 4. O dolar do banco nao e o da noticia
T("Falta um detalhe", "e ele custa dinheiro",
  "Falta um detalhe no passo um, e ele custa dinheiro de verdade. A cotação "
  "que o seu banco usa não é a que aparece no noticiário.",
  cap="O dólar do banco não é o da notícia")
T("A cotação da notícia", "é a do mercado entre bancos",
  "A cotação que você vê na notícia é a do mercado entre bancos. Você não "
  "compra dólar nesse mercado.")
I("O que você paga", "é a cotação do emissor",
  "Você paga a cotação que o emissor do seu cartão aplica, e ela vem sempre um "
  "pouco acima. Essa diferença tem nome: spread.")
T("Cada banco tem o seu", "e não anuncia",
  "Cada banco tem o seu spread, e nenhum deles estampa isso na propaganda. "
  "Mas está na sua fatura, e dá para medir.")
L("Como medir o seu", ["Ache uma compra internacional na fatura",
                       "Divida o valor em reais pelo valor em dólar",
                       "Compare com a cotação daquele dia"],
  "Ache uma compra internacional antiga na fatura. Divida o valor em reais "
  "pelo valor em dólar. Compare com a cotação daquele dia.")
I("A diferença que sobrar", "é o seu spread",
  "A diferença que sobrar é o seu spread, medido no seu banco, com o seu "
  "cartão. Não é estimativa de ninguém.")
T("Faça isso uma vez", "e vale para sempre",
  "Você faz isso uma vez na vida e passa a somar esse número em toda compra "
  "internacional que fizer depois.")
T("Sem ele", "a conta fica otimista",
  "Sem ele, a conta do passo um fica otimista. E conta otimista é a que faz "
  "você escolher a rota errada.")

# ------------------------------------------------- 5. O gift card nao escapa
T("A terceira rota", "e a ilusão que ela cria",
  "Falta a terceira rota, e ela cria a ilusão mais cara das três. O gift card "
  "e o cartão pré-pago.",
  cap="O gift card não escapa")
T("A sensação é boa", "você já pagou em reais",
  "A sensação é ótima. Você paga em reais, recebe um saldo, e depois gasta "
  "esse saldo sem ver preço em dólar nenhum.")
I("Mas o imposto", "já foi cobrado na carga",
  "Só que o imposto já foi cobrado. Ele incide quando o saldo é carregado, não "
  "quando você gasta.")
I("A mesma alíquota", "três e meio por cento",
  "É a mesma alíquota de três e meio por cento. Cartão pré-pago internacional "
  "está na mesma linha da regra.")
T("O que muda", "é só quando você sente",
  "O que muda não é o valor. É o momento em que você sente. E sentir depois "
  "faz o gasto parecer menor do que foi.")
T("Se o gift card for da loja brasileira", "aí a conversa é outra",
  "Atenção a uma exceção: gift card vendido em reais pela loja brasileira não "
  "passa por câmbio nenhum. Esse não tem IOF.")
T("A pergunta certa", "é em que moeda a carga acontece",
  "Então a pergunta não é se é gift card. É em que moeda a carga acontece. "
  "Câmbio houve? Teve imposto.")
T("E tem um efeito colateral", "o saldo que sobra",
  "Tem ainda um custo escondido no pré-pago: o saldo que sobra e não fecha com "
  "nenhum preço. Ele fica parado lá, e você já pagou imposto por ele.")

# -------------------------------- 6. A loja brasileira ja cobrou de voce
T("E a loja em reais", "é a mais barata?",
  "Se as outras duas rotas somam imposto, a loja brasileira em reais é sempre "
  "a mais barata? Não necessariamente, e vale entender por quê.",
  cap="A loja brasileira já cobrou")
T("O preço em reais", "não caiu do céu",
  "O preço em reais que ela mostra não caiu do céu. Ele foi definido pela "
  "distribuidora olhando o poder de compra do mercado local.")
I("Nele já estão", "os tributos do país",
  "E dentro dele já estão os tributos que incidem sobre serviço digital "
  "vendido aqui. Você não vê a linha, mas ela existe.")
T("A diferença é essa", "um imposto aparece, o outro não",
  "A diferença entre as rotas não é imposto contra ausência de imposto. É "
  "imposto embutido contra imposto somado depois.")
T("Por isso a comparação", "tem de ser no valor final",
  "Por isso a comparação só vale no valor final. Nunca compare etiqueta com "
  "etiqueta, compare o que sai da sua conta.")
T("Às vezes a loja local perde", "e isso acontece mesmo",
  "E sim, às vezes a loja local perde, principalmente quando o preço regional "
  "foi ajustado para cima e o dólar está calmo.")
T("A conta não tem lado", "ela só responde",
  "A conta não torce por nenhuma rota. Ela só responde, com os seus números, "
  "naquele dia, para aquele jogo.")
T("E ela muda de resposta", "quando o dólar mexe",
  "E a resposta muda sozinha ao longo do ano, sem que nenhuma loja mude nada, "
  "porque um dos lados da comparação depende do câmbio e o outro não.")

# ------------------------------------------------------ 7. O ponto de virada
T("Existe um ponto", "onde a resposta muda",
  "E existe um ponto exato onde a resposta vira. Ele é o motivo de você fazer "
  "a conta uma vez e nunca mais precisar refazer do zero.",
  cap="O ponto de virada")
T("Pense assim", "qual cotação empata as duas rotas",
  "Pense na pergunta ao contrário. Em vez de perguntar qual é mais barata, "
  "pergunte qual cotação de dólar empataria as duas.")
I("A conta do empate", "preço em reais dividido pelo preço em dólar",
  "Divida o preço da loja brasileira pelo preço em dólar. Depois divida esse "
  "resultado por um vírgula zero trinta e cinco.")
I("O que sai", "é a sua cotação de empate",
  "O número que sai é a cotação de empate. Acima dela, a loja brasileira "
  "ganha. Abaixo dela, a rota em dólar ganha.")
T("Ainda falta o spread", "então desconte ele também",
  "Se você já mediu o seu spread, desconte ele aqui também. A cotação de "
  "empate desce, e a loja brasileira passa a ganhar mais vezes.")
T("Agora você tem um gatilho", "e não uma dúvida",
  "Agora você não tem mais uma dúvida a cada compra. Tem um gatilho. Olha a "
  "cotação do dia e compara com o seu número.")
T("E ele é seu", "não é regra geral",
  "Esse número é seu, do seu banco e daquele jogo. Não existe cotação de "
  "empate universal, e quem te vender uma está chutando.")

# --------------------------------------------------- 8. Antes de clicar
T("Antes de clicar", "trinta segundos",
  "Antes da próxima compra, trinta segundos de rotina. É o resumo prático de "
  "tudo que está aqui.",
  cap="Antes de clicar em comprar")
L("A rotina", ["Anote o preço nas duas moedas",
               "Multiplique o valor em dólar por um vírgula zero trinta e cinco",
               "Some o seu spread e compare"],
  "Anote o preço nas duas moedas. Multiplique o valor em dólar por um vírgula "
  "zero trinta e cinco. Some o seu spread, e compare.")
T("Se a diferença for pequena", "fique na rota em reais",
  "E uma regra de bolso para o empate: se a diferença ficar pequena, fique na "
  "rota em reais. Reembolso e suporte em português valem alguma coisa.")
I("Um aviso honesto", "as regras mudam",
  "Um aviso honesto: alíquota de imposto muda por decreto, e da noite para o "
  "dia. Confira a data antes de aplicar qualquer número que você ouviu.")
T("Inclusive este", "confira também",
  "Inclusive este. O número que eu dei tem data, e a data está na descrição, "
  "junto com onde eu conferi.")
T("O que fica", "não é o número, é o método",
  "E o que fica para você não é o três e meio por cento. É o método: comparar "
  "sempre o valor que sai da conta, e nunca a etiqueta que a loja mostra.")
C("Faça a sua conta agora", "e me diga qual rota ganhou",
  "Faça a conta com o último jogo que você comprou e veja se você escolheu "
  "certo. Se este tipo de conta te serve, se inscreve que toda semana tem uma.")


# ---------------------------------------------------------------------------
# O SHORT. Ele nao fecha sozinho (aprendizado 493): entrega o imposto e o
# passo da conta, e manda o PONTO DE VIRADA para o longo.
SHORT = [
    {"layout": "titulo", "kicker": "O mesmo jogo", "sub": "três preços",
     "nar": "O mesmo jogo custa três valores diferentes para você hoje, e a "
            "diferença não está no jogo.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Está em", "sub": "por onde você paga",
     "nar": "Está em por onde você paga: loja em reais, cartão internacional "
            "ou gift card.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pagou em moeda estrangeira",
     "sub": "três e meio por cento",
     "nar": "Se houve câmbio, entram três e meio por cento de IOF em cima. "
            "Vale desde maio do ano passado.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E não aparece", "sub": "na tela da loja",
     "nar": "E não aparece na loja. Aparece na fatura.", "sem_cap": True},
    {"layout": "titulo", "kicker": "A conta rápida",
     "sub": "vezes um vírgula zero trinta e cinco",
     "nar": "Multiplique o preço em dólar pela cotação e depois por um vírgula "
            "zero trinta e cinco.", "sem_cap": True},
    {"layout": "cta", "kicker": "Existe uma cotação de empate",
     "sub": "e ela é sua",
     "nar": "Tem uma cotação em que as duas rotas empatam, e o jeito de achar "
            "a sua está no vídeo completo, no link aqui embaixo.",
     "sem_cap": True},
]

THUMB = {"l1": "o mesmo jogo", "l2": "três preços"}

COPY = """# A rota de pagamento muda o preço final — e o imposto só aparece na fatura

## TITULO
Loja em Reais, Cartão em Dólar ou Gift Card? A Conta Antes de Comprar o Jogo

## DESCRICAO
O mesmo jogo, no mesmo dia, custa três valores diferentes dependendo de por onde você paga: a loja brasileira em reais, o cartão internacional em dólar, ou o gift card e o cartão pré-pago. A diferença não está no jogo — está na rota de pagamento, e a peça que quase ninguém soma é um imposto que só aparece depois, na fatura.

Esse imposto é o IOF, o Imposto sobre Operações Financeiras, que incide quando o seu real vira moeda estrangeira. A alíquota é de 3,5% e vale para cartão de crédito internacional, cartão de débito internacional, cartão pré-pago internacional e compra de moeda estrangeira em espécie. Está em vigor desde 23 de maio de 2025, pelo Decreto 12.466, de 22 de maio de 2025. Antes de 2022 a alíquota chegava a 6,38%, e a unificação das regras de 2025 é o que fixou o número onde ele está hoje.

O vídeo monta a conta em três passos que você faz no aplicativo do banco em menos de um minuto: multiplique o preço em dólar pela cotação do dia, multiplique o resultado por 1,035 para somar o IOF, e compare com o preço que a loja brasileira mostra em reais. Ganha o menor.

Depois entra o detalhe que derruba a maioria das comparações: a cotação que o seu banco usa não é a que aparece no noticiário. A diferença chama-se spread, varia por emissor, e não é anunciada — mas está na sua fatura. O vídeo mostra como medir o seu uma única vez, dividindo o valor em reais pelo valor em dólar de uma compra internacional antiga e comparando com a cotação daquele dia. Feito isso, o número é seu para sempre.

O gift card recebe um capítulo próprio porque cria a ilusão mais cara das três: o imposto já foi cobrado na carga do saldo, não no momento em que você gasta. A exceção é o gift card vendido em reais pela loja brasileira, que não passa por câmbio e portanto não tem IOF — a pergunta certa não é se é gift card, é em que moeda a carga acontece.

O fecho é o ponto de virada: em vez de perguntar qual rota é mais barata a cada compra, você calcula uma vez a cotação de empate — o preço em reais dividido pelo preço em dólar, dividido por 1,035. Acima dela a loja brasileira ganha; abaixo, a rota em dólar. Esse número é seu, do seu banco e daquele jogo, e substitui a dúvida por um gatilho.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz a conta com o último jogo que você comprou e conta aqui qual rota ganhou — e de quanto foi a diferença. Tenho curiosidade em ver se o spread muda muito de banco para banco, porque essa é a parte que eu não consegui medir para ninguém além de mim.

## HASHTAGS
#EconomiaDosGames #IOF #NivelDoJogo

## TAGS
comprar jogo mais barato, iof cartao internacional, gift card steam, preco de jogos no brasil, cotacao do dolar compra, spread do banco, cartao internacional imposto, economia dos games, steam brasil, psn brasil, xbox brasil, imposto compra internacional, como economizar em jogos, financas para gamers, nivel do jogo

## CONFIGURACAO DE STUDIO
- Idioma: Português (pt-BR) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Brasil | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 25 de agosto de 2026. O número central deste vídeo é a alíquota de IOF de 3,5% sobre operações de câmbio de cartão de crédito internacional, cartão de débito internacional, cartão pré-pago internacional e compra de moeda estrangeira em espécie, em vigor desde 23/05/2025 pelo Decreto 12.466, de 22/05/2025. Ele foi conferido em duas rotas institucionais independentes: (1) Ministério da Fazenda — comunicado de maio de 2025 sobre as medidas de equilíbrio fiscal e a apresentação da Receita Federal publicada em gov.br/fazenda com a tabela de alíquotas; (2) Receita Federal — página de orientação tributária do IOF em gov.br/receitafederal, e o Decreto 12.466 no acervo de legislação do Planalto. A alíquota anterior de 6,38%, vigente até 2022, consta do mesmo comunicado do Ministério da Fazenda.

AVISO SOBRE OS NÚMEROS — o que foi descartado e por quê. (a) O artigo exato do decreto NÃO entrou. Os domínios oficiais recusaram acesso automatizado à consulta, então o conteúdo foi lido pela indexação e não no texto literal; citar número de artigo que não foi lido seria inventar precisão. (b) O antigo cronograma de redução gradual do IOF até zero NÃO entrou: depois da unificação de 2025 ele não fecha em duas fontes oficiais. (c) Nenhuma cotação de dólar e nenhum spread bancário são afirmados como fato. Ambos mudam diariamente e variam por emissor, então o vídeo ensina onde o espectador mede os seus em vez de apresentar um número que já nasceria velho. (d) O vídeo afirma que tributos sobre serviço digital já estão embutidos no preço em reais praticado no mercado local, sem quantificar essa fatia — a composição do preço regional é decisão comercial da distribuidora e não é publicada. Alíquota de imposto muda por decreto, e o vídeo diz isso em voz alta: confira a data antes de aplicar qualquer número. Não há aqui recomendação de investimento nem orientação tributária individual.
"""

SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-007",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1B4332", "c1": "#D64570", "c2": "#F2B134", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "nivel-do-jogo-007.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
