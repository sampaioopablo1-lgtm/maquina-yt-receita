#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-004.

PAUTA, medida em 18/08/2026 e gravada em pautas_banco. O assunto vivo do
nicho pt-BR e o preco do EA FC 27, e o formato que performa e PERGUNTA DE
DECISAO DE COMPRA:

    video (90 dias)                                              v/d
    EA FC 27 O MAIS CARO DE TODOS OS TEMPOS! (short)         56.704,9
    FC 27 Mais Caro Que GTA 6?                                7.566,0
    EA FC 27 | QUAL VERSAO COMPRAR? STANDARD, ULTIMATE
      OU ULTIMATE+? (Oniixes FC, 23/07)                         177,2
    Preco dos Jogos VALE A PENA COMPRAR FIFA TODO ANO            99,2
    EA FC 26 EM PROMOCAO HISTORICA — ARMADILHA? (20/06)          11,1

Mediana do canal: 17,35. O "QUAL VERSAO COMPRAR" roda a 10x a mediana com
canal pequeno — e a pergunta esta aberta AGORA: pre-venda aberta desde
23/07, lancamento 25/09, acesso antecipado 18/09.

EIXO NAO USADO: os videos de decisao comparam LISTAS de beneficios; nenhum
faz a CONTA — o que cada real a mais compra de verdade. A casa do -004:
a diferenca em reais entre edicoes dividida pelo que ela contem, a pergunta
"qual modo voce joga" como filtro que zera ou valida cada beneficio, e o
ciclo anual de depreciacao (o proprio nicho registrou o FC 26 em "promocao
historica" nove meses depois do lancamento).

NUMEROS VERIFICADOS (18/08/2026, duas fontes que batem — Critical Hits
23/07 com a tabela completa; TechTudo e Diario de Pernambuco com o teto de
R$ 749,50 e o piso de R$ 299):
  * Standard: R$ 299 (PC) / R$ 349 (consoles)
  * Ultimate: R$ 429 (PC) / R$ 499 (consoles) — ate 7 dias de acesso
    antecipado, 6.000 FC Points em tres meses, Passe Premium da Temporada 1
  * Ultimate Plus: R$ 699 (PC) / R$ 749,50 (consoles) — 7 dias antecipado,
    10.000 FC Points em cinco distribuicoes, Passes Premium T1 a T5
  * Lancamento 25/09/2026; acesso antecipado 18/09; EA Play da 10% na
    pre-venda de PS/Xbox.
As contas derivadas (150 de diferenca; ~21 por dia de antecipacao; 400,50
ate a Plus) sao aritmetica direta desses precos.

SIMILARIDADE vs publicados do canal:
  -002 "Lei Felca nos Games: R$ 333 Milhoes e o Fim da Caixinha" -> regulacao
  -003 "Preco dos Jogos em 2026: Quantas Horas de Trabalho Custa GTA 6"
Este NAO e regulacao nem horas de trabalho: e decisao de compra por edicao.
A caixinha aparece UMA vez (FC Points viram packs), como ponte para o -002.

TITULO modela a estrutura do outlier local ([JOGO] + [pergunta de decisao
entre edicoes]) com keyword nos 5 primeiros termos.

DIMENSIONAMENTO pelo agregado de producao (fabrica/ensaio.py, n=132):
pt-BR-AntonioNeural = 16,11 chars/s + 0,939 s/frase. Alvo no MEIO da janela
(aprendizado 302): ~9.900 chars em ~78 cenas = ~13,2 min.
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


# ---------------------------------------------------------------- cap 1
T("A pré-venda abriu", "e o teto assusta",
  "A pré-venda do novo FC abriu com o preço mais alto da história da "
  "franquia no Brasil: setecentos e quarenta e nove reais e cinquenta "
  "centavos no topo.",
  cap="O número errado da discussão")
I("A discussão que se vê", "caro ou não",
  "A internet inteira está discutindo se isso é caro. Essa discussão não "
  "ajuda ninguém a decidir nada.")
I("O reflexo nos títulos", "o mais caro de todos os tempos",
  "Os títulos do nicho gritam a mesma frase: o mais caro de todos os "
  "tempos. O grito olha para o teto da tabela, e o teto é opcional.")
I("O número que decide", "a diferença",
  "Porque ninguém é obrigado a comprar o topo. O número que decide a sua "
  "compra é a diferença entre as edições, e o que essa diferença contém.")
I("Três edições", "três contas",
  "São três edições, e entre a mais barata e a mais cara existe uma escada "
  "de valores. Cada degrau tem um preço e um conteúdo. Dá para calcular os "
  "dois.")
I("O que ninguém faz", "dividir a diferença",
  "Os vídeos de comparação listam os benefícios de cada versão. Quase "
  "nenhum divide o preço do degrau pelo que o degrau entrega. É essa conta "
  "que vamos fazer.")
L("O caminho", ["As três edições em números", "O preço de cada degrau",
                "O filtro do seu modo", "O ciclo anual", "Armadilhas"],
  "Cinco partes. As três edições em números. O preço real de cada degrau. "
  "O filtro que zera ou valida cada benefício. O ciclo anual da franquia. "
  "E as armadilhas.")
I("Regra da casa", "número com fonte",
  "Como sempre neste canal: os preços são os oficiais da pré-venda "
  "brasileira, e toda conta derivada você refaz de cabeça no caminho da "
  "loja.")
T("Começando", "pela tabela",
  "Começando pelo que está à venda, exatamente como está à venda:")

# ---------------------------------------------------------------- cap 2
T("Edição Standard", "o jogo, e só",
  "A Standard é o jogo completo. Trezentos e quarenta e nove reais nos "
  "consoles, duzentos e noventa e nove no computador.",
  cap="As três edições em números")
I("O que ela tem", "tudo que é jogo",
  "Nela está tudo o que é futebol: os mesmos modos, o mesmo gameplay, os "
  "mesmos times. Nenhuma partida a menos.")
I("O que ela não tem", "nada de jogo a menos",
  "E vale repetir de outro jeito, porque a loja sugere o contrário: não "
  "existe conteúdo de futebol trancado fora da Standard. O que muda é "
  "acessório.")
I("Bônus de pré-venda", "iguais para todos",
  "Os bônus de pré-encomenda, como ídolos para o time e reforços de "
  "Carreira, valem para as três edições. Eles não separam os degraus.")
I("Edição Ultimate", "o degrau do meio",
  "A Ultimate sobe para quatrocentos e noventa e nove nos consoles, "
  "quatrocentos e vinte e nove no computador.")
I("O que o degrau traz", "antecipação e moeda",
  "O degrau traz até sete dias de acesso antecipado, seis mil FC Points "
  "parcelados em três meses, e o Passe Premium da primeira temporada.")
I("Edição Ultimate Plus", "o topo",
  "A Ultimate Plus é o topo: setecentos e quarenta e nove reais e "
  "cinquenta centavos nos consoles, seiscentos e noventa e nove no "
  "computador.")
I("O que o topo traz", "passes e mais moeda",
  "O topo mantém os sete dias de antecipação, sobe os pontos para dez mil "
  "em cinco entregas, e estica os Passes Premium da primeira à quinta "
  "temporada.")
I("PC contra console", "a mesma escada, mais baixa",
  "Repare que o computador paga menos em todos os degraus. A escada é a "
  "mesma; ela só começa cinquenta reais mais embaixo.")
I("As datas", "duas, e importam",
  "As datas importam para a conta: lançamento em vinte e cinco de "
  "setembro, acesso antecipado a partir de dezoito.")
I("Um desconto real", "assinante da EA",
  "E um desconto verdadeiro no meio do caminho: assinante do serviço da EA "
  "tem dez por cento na pré-venda das lojas de console.")
T("Tabela na mesa", "agora a conta",
  "Essa é a tabela. Agora o que interessa: quanto custa cada degrau, e o "
  "que ele vale.")

# ---------------------------------------------------------------- cap 3
T("O degrau do meio", "cento e cinquenta reais",
  "Da Standard para a Ultimate, nos consoles, o degrau custa cento e "
  "cinquenta reais. É esse número que você está decidindo pagar.",
  cap="O preço de cada degrau")
I("O que ele compra", "três coisas",
  "Ele compra três coisas. A semana de antecipação. A moeda que só existe "
  "dentro do jogo. E o passe da temporada de estreia.")
I("Se você tirar a moeda", "sobra a semana",
  "Se os pontos e o passe não valem nada para você, e daqui a pouco vamos "
  "ver quando não valem, sobra a semana de antecipação.")
I("A semana em reais", "vinte e um por dia",
  "Cento e cinquenta reais divididos por sete dias dão pouco mais de vinte "
  "e um reais por dia de antecipação. Um ingresso de cinema por dia, para "
  "jogar antes.")
I("O degrau do topo", "quatrocentos e um",
  "Da Standard direto para a Ultimate Plus, o degrau custa quatrocentos "
  "reais e cinquenta centavos. Mais que o preço de uma segunda Standard.")
I("O que ele compra", "temporadas",
  "A diferença da Plus para a Ultimate está quase toda nos passes: cinco "
  "temporadas em vez de uma, e quatro mil pontos a mais.")
I("O detalhe do parcelamento", "moeda em conta-gotas",
  "Repare no desenho: os pontos não vêm de uma vez, vêm parcelados ao "
  "longo de meses. Isso não é generosidade, é calendário de retenção. A "
  "moeda pinga para você voltar.")
I("O passe premium", "valor condicionado",
  "E o passe de temporada só vira valor se a temporada for jogada. Passe "
  "de quem parou em dezembro é papel picado digital.")
B("A escada", ["Standard", "Ultimate", "Ultimate Plus"], [47, 67, 100],
  "Vista como escada, a pergunta muda de tamanho: o segundo degrau custa "
  "cento e cinquenta, e o terceiro, mais duzentos e cinquenta em cima.")
I("Moeda não é desconto", "pontos não são reais",
  "E uma regra antes de seguir: FC Points não são dinheiro. Só compram "
  "coisas dentro do jogo, no preço que o jogo definir, e boa parte vira "
  "pacote de sorteio.")
I("A ponte", "a caixinha já foi aberta",
  "Sobre o que há dentro desses pacotes e por que a lei brasileira entrou "
  "nesse assunto, este canal já fez um vídeo inteiro. Fica o aviso de uma "
  "linha: pacote é sorteio.")
T("Degraus precificados", "falta o filtro",
  "Degraus precificados. Falta o filtro que decide, para VOCÊ, se cada "
  "degrau vale alguma coisa:")

# ---------------------------------------------------------------- cap 4
T("O filtro", "qual modo você joga?",
  "O filtro é uma pergunta só: qual modo você realmente joga? A resposta "
  "zera ou valida cada benefício da tabela.",
  cap="O filtro do seu modo")
I("Carreira e Pro Clubs", "pontos valem zero",
  "Se a sua vida é Modo Carreira ou Pro Clubs, os FC Points e os passes "
  "valem zero para você. Não é opinião: eles são moeda do Ultimate Team.")
I("A consequência", "Ultimate vira antecipação",
  "Para esse jogador, a Ultimate vira só a semana antecipada por cento e "
  "cinquenta reais. E a Plus perde o sentido por inteiro.")
I("Ultimate Team casual", "a conta dos pontos",
  "Se você joga Ultimate Team de vez em quando, a conta é comparar: quanto "
  "custariam seis mil pontos comprados avulsos na loja no dia? Compare com "
  "o degrau e decida.")
I("Por que não cravamos", "preço de loja muda",
  "Não vamos cravar o preço avulso aqui de propósito: ele muda por "
  "plataforma e por promoção. A conta é sua, o método fica.")
I("Ultimate Team diário", "a Plus se paga?",
  "Se você vive no Ultimate Team e compraria os passes de temporada de "
  "qualquer jeito, a Plus deixa de ser luxo e vira pacote com desconto. "
  "Essa é a única pessoa para quem ela existe.")
I("Quem joga os dois", "some as metades",
  "Se você divide o tempo entre Carreira e Ultimate Team, some as duas "
  "leituras: a parte dos pontos vale pela metade do seu tempo, e a conta "
  "encolhe na mesma proporção.")
I("Quem compra de presente", "Standard mais vale-presente",
  "E quem compra para presentear alguém: Standard mais um vale-presente da "
  "loja costuma servir melhor que a Plus, porque devolve a escolha a quem "
  "vai jogar.")
I("A pergunta do tempo", "horas por semana",
  "Uma régua auxiliar honesta: quantas horas por semana você joga? Quem "
  "joga três horas semanais raramente extrai valor de qualquer degrau "
  "acima da Standard.")
I("A antecipação", "vale para quem corre",
  "E os sete dias valem mais para quem entra cedo no mercado do Ultimate "
  "Team, quando os preços dos jogadores ainda estão se formando. Para "
  "quem joga Carreira, é só ansiedade.")
T("Filtro aplicado", "falta o calendário",
  "Com o filtro aplicado, a maioria já sabe sua edição. Falta a última "
  "camada, que é a que mais economiza: o calendário.")

# ---------------------------------------------------------------- cap 5
T("O ciclo anual", "todo ano, a mesma curva",
  "Esta franquia relança todo ano, e todo ano desenha a mesma curva de "
  "preço: topo na pré-venda, queda contínua depois.",
  cap="O ciclo anual")
I("Por que a curva cai", "o sucessor já tem data",
  "A queda não é acidente: no dia do lançamento, o sucessor do ano "
  "seguinte já está no calendário da empresa. A depreciação vem embutida "
  "no modelo de negócio.")
I("A prova no nicho", "promoção histórica",
  "A prova estava nos títulos deste ano: o jogo atual apareceu em promoção "
  "chamada de histórica nove meses depois do lançamento.")
I("A conta da posse", "preço por mês",
  "A conta honesta de um jogo anual é preço dividido por meses de posse "
  "útil. Quem compra na pré-venda paga o topo e leva doze meses de vida do "
  "jogo.")
I("A conta com números", "trinta por mês no topo",
  "Nos consoles, a Standard na pré-venda dá pouco menos de trinta reais "
  "por mês, se você jogar o ano inteiro. Esse é o melhor cenário do "
  "comprador de lançamento.")
I("Quem espera", "paga menos por mês",
  "Quem espera três meses paga visivelmente menos e ainda leva nove meses "
  "de jogo vivo. Em preço por mês, esperar quase sempre vence.")
I("O que a espera custa", "o começo da temporada",
  "O que a espera custa é o começo: as primeiras semanas de mercado, os "
  "amigos jogando antes, a novidade. Isso tem valor real, só não aparece "
  "em real na etiqueta.")
I("As duas estratégias", "explícitas",
  "Ficam então duas estratégias honestas. Pagar o topo para viver o "
  "lançamento, sabendo o que o topo custa. Ou esperar a curva cair, "
  "sabendo o que se perde.")
I("O que não é estratégia", "pagar o topo sem usar",
  "O que não é estratégia é pagar preço de lançamento e jogar pela "
  "primeira vez em novembro. Essa combinação paga o pior dos dois mundos.")
T("Calendário fechado", "faltam as armadilhas",
  "Com preço, filtro e calendário, o sistema está completo. Faltam os "
  "quatro erros que mais custam nessa compra:")

# ---------------------------------------------------------------- cap 6
T("Armadilha um", "comprar a Plus por status",
  "A primeira: comprar a Ultimate Plus para aproveitar, sem jogar Ultimate "
  "Team. É pagar quatrocentos reais de conteúdo que nunca será aberto.",
  cap="Quatro armadilhas caras")
I("Armadilha dois", "contar pontos como desconto",
  "A segunda: somar os FC Points como se fossem reais de volta. Moeda de "
  "jogo não paga boleto, não volta ao bolso, e expira junto com o seu "
  "interesse.")
I("Armadilha três", "antecipação sem agenda",
  "A terceira: pagar pela semana antecipada e não ter agenda para jogar "
  "naquela semana. Vinte e um reais por dia só valem se os dias forem "
  "usados.")
I("Armadilha quatro", "assinar pelo desconto",
  "A quarta: assinar o serviço da EA só para ganhar dez por cento na "
  "pré-venda. Assinatura que não seria feita de qualquer jeito é custo, "
  "não desconto.")
I("O custo somado", "mais que o jogo",
  "Somadas, essas armadilhas custam mais que uma Standard inteira. É o "
  "jogo que você pagou e não levou.")
I("Edição não é skill", "o campo é o mesmo",
  "E o lembrete que ninguém imprime na loja: edição não muda habilidade. "
  "Dentro da partida, a Plus e a Standard jogam exatamente o mesmo "
  "futebol.")
I("O fio das quatro", "benefício sem uso",
  "O fio comum: pagar por benefício que o seu jeito de jogar não usa. A "
  "tabela é igual para todo mundo; o valor dela, não.")
I("O antídoto", "modo antes da loja",
  "O antídoto cabe numa frase: decida qual modo você joga antes de abrir a "
  "página da loja, e não depois.")
T("Última parte", "o resumo que decide",
  "Resta juntar tudo numa folha que decide em um minuto:")

# ---------------------------------------------------------------- cap 7
T("A folha de decisão", "três perguntas",
  "Três perguntas, em ordem. Qual modo você joga? Você vai jogar na semana "
  "de dezoito de setembro? E você compraria os passes de qualquer jeito?",
  cap="A folha de decisão")
I("Carreira ou Clubs", "Standard, e pronto",
  "Modo Carreira ou Pro Clubs: Standard, sem culpa. Todo o futebol está "
  "lá, e cada real acima disso compra coisa que você não usa.")
I("Ultimate Team casual", "Standard ou Ultimate",
  "Ultimate Team casual: Standard, ou Ultimate se a conta dos pontos "
  "avulsos fechar a seu favor no dia.")
I("Ultimate Team diário", "a Plus com a conta feita",
  "Ultimate Team diário, com passes que seriam comprados de qualquer "
  "jeito: a Plus é a única edição em que o topo se justifica.")
I("Sem pressa", "a curva trabalha para você",
  "E se nenhuma resposta pediu urgência: espere. A curva de preço desta "
  "franquia trabalha para quem tem paciência, todo ano, sem exceção.")
I("O desconto que sobrou", "EA Play, com uso",
  "O desconto de dez por cento do serviço da EA entra na folha só para "
  "quem já assina ou assinaria pelo catálogo. Nesse caso, ele é real e "
  "vale nas três edições.")
I("Um exemplo aplicado", "o jogador de Carreira",
  "Exemplo aplicado: jogador de Carreira, dez horas por semana, sem pressa "
  "de lançamento. Resposta da folha: Standard, comprada quando a curva "
  "ceder. Sem drama.")
L("O resumo", ["Diferença, não teto", "Pontos não são reais",
               "Modo decide edição", "Preço por mês", "Agenda antes da loja"],
  "O resumo em cinco linhas. Olhe a diferença, não o teto. Pontos não são "
  "reais. O seu modo decide a edição. Pense em preço por mês. E agenda "
  "antes da loja.")
I("Se fizer uma coisa só", "escreva seu modo",
  "Se você fizer uma coisa só antes da pré-venda, faça esta: escreva num "
  "papel qual modo você jogou de verdade no último ano. A edição certa sai "
  "daí sozinha.")
C("Nível do Jogo", "a economia dos games",
  "Agora me conta nos comentários: qual edição você vai levar, e qual modo "
  "você joga? Quero ver se a escolha bate com a conta.")
C("Nível do Jogo", "a economia dos games",
  "E se quiser a mesma conta para outro lançamento ou outra franquia "
  "anual, escreve o nome. O mais pedido vira o próximo vídeo.")

SHORT = [
    {"layout": "titulo", "kicker": "FC 27 até R$ 749",
     "sub": "o número errado",
     "nar": "O novo FC custa até setecentos e quarenta e nove reais, e esse "
            "é o número errado para a sua decisão.", "sem_cap": True},
    {"layout": "item", "kicker": "O número certo", "preco": "a diferença",
     "nar": "O certo é a diferença entre edições: cento e cinquenta reais "
            "separam a Standard da Ultimate nos consoles.", "sem_cap": True},
    {"layout": "item", "kicker": "O que ele compra", "preco": "R$ 21 por dia",
     "nar": "Se você não joga Ultimate Team, isso compra uma semana "
            "antecipada: pouco mais de vinte e um reais por dia.",
     "sem_cap": True},
    {"layout": "item", "kicker": "O filtro", "preco": "seu modo decide",
     "nar": "Carreira ou Pro Clubs: Standard resolve, todo o futebol está "
            "lá. A Plus só existe para quem vive no Ultimate Team.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Nível do Jogo", "sub": "a conta completa",
     "nar": "Essa é a decisão inteira: modo primeiro, edição depois. Qual "
            "você vai levar? Comenta aí.", "sem_cap": True},
]

COPY = """# A conta que decide a edição do FC 27 antes da pré-venda

## TÍTULO
EA FC 27: Standard, Ultimate ou Plus? A Conta em Reais Antes da Pré-Venda

## DESCRIÇÃO
A pré-venda do EA Sports FC 27 abriu com o preço mais alto da história da franquia no Brasil: até R$ 749,50 na Ultimate Plus de console. A internet inteira discute se isso é caro — e essa discussão não decide nada, porque ninguém é obrigado a comprar o topo. Este vídeo faz a conta que decide: a diferença entre as edições, dividida pelo que cada degrau realmente contém.

AS TRÊS EDIÇÕES EM NÚMEROS (pré-venda oficial no Brasil): Standard por R$ 349 nos consoles e R$ 299 no PC — o jogo completo, todos os modos. Ultimate por R$ 499 / R$ 429 — até 7 dias de acesso antecipado, 6.000 FC Points parcelados em três meses e o Passe Premium da Temporada 1. Ultimate Plus por R$ 749,50 / R$ 699 — os mesmos 7 dias, 10.000 FC Points em cinco entregas e os Passes Premium das Temporadas 1 a 5. Lançamento em 25 de setembro; acesso antecipado a partir de 18; assinantes EA Play têm 10% na pré-venda das lojas de console.

O PREÇO DE CADA DEGRAU. Da Standard à Ultimate: R$ 150. Se você não joga Ultimate Team, sobra a semana antecipada — R$ 150 ÷ 7 ≈ R$ 21 por dia. Da Standard à Plus: R$ 400,50, quase uma segunda Standard, com o valor concentrado nos passes de cinco temporadas. E uma regra antes de qualquer conta: FC Points não são dinheiro — só compram conteúdo dentro do jogo, e boa parte vira pacote de sorteio (a caixinha que este canal já dissecou no vídeo da Lei Felca).

O FILTRO QUE DECIDE: qual modo você joga? Carreira e Pro Clubs zeram pontos e passes — Standard sem culpa. Ultimate Team casual compara o degrau com o preço avulso dos pontos no dia. Ultimate Team diário, que compraria os passes de qualquer jeito, é a única pessoa para quem a Plus se justifica.

O CICLO ANUAL. A franquia relança todo ano e desenha a mesma curva: topo na pré-venda, queda depois — o FC 26 apareceu em "promoção histórica" nove meses após o lançamento. A conta honesta de jogo anual é preço por mês de posse. Pagar o topo para viver o lançamento é uma estratégia; esperar a curva cair é outra. Pagar o topo e só jogar em novembro não é estratégia.

E as quatro armadilhas: a Plus comprada "para aproveitar" sem jogar FUT; pontos contados como desconto; antecipação paga sem agenda para usá-la; e assinatura feita só pelo desconto de 10%.

Se fizer uma coisa só antes da pré-venda: escreva qual modo você jogou de verdade no último ano. A edição certa sai daí sozinha.

## CAPÍTULOS
{CAPITULOS}

## COMENTÁRIO
Duas perguntas, porque a graça é ver se a escolha bate com a conta: qual edição você vai levar — Standard, Ultimate ou Plus — e qual modo você realmente joga? E se quiser a mesma conta para outro lançamento ou outra franquia anual, escreve o nome: o mais pedido vira o próximo vídeo.

## HASHTAGS
#EAFC27 #FC27 #NivelDoJogo

## TAGS
ea fc 27, fc 27 preço, ea fc 27 pré venda, fc 27 qual versão comprar, fc 27 ultimate edition, fc 27 standard, ea fc 27 brasil, fc points, ultimate team, fc 27 acesso antecipado, preço dos jogos, economia dos games, ea sports fc, vale a pena fc 27, nivel do jogo

## CONFIGURAÇÕES DO STUDIO
- Idioma: Português (Brasil) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Localização: Brasil | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ativados (duração acima de 8 minutos)

## MÚSICA / LICENÇA
{TRILHA}

## FONTES
Preços e conteúdos das edições do EA Sports FC 27 no Brasil conforme a pré-venda oficial aberta em julho de 2026, reportados de forma coincidente por Critical Hits (tabela completa: Standard R$ 299 PC / R$ 349 consoles; Ultimate R$ 429 / R$ 499 com até 7 dias de acesso antecipado, 6.000 FC Points em três meses e Passe Premium da Temporada 1; Ultimate Plus R$ 699 / R$ 749,50 com 10.000 FC Points em cinco distribuições e Passes Premium das Temporadas 1 a 5), TechTudo e Diario de Pernambuco (teto de R$ 749,50 e piso de R$ 299). Lançamento mundial em 25 de setembro de 2026 e acesso antecipado a partir de 18 de setembro, conforme a própria EA. As contas derivadas (R$ 150 de diferença entre Standard e Ultimate nos consoles; ~R$ 21 por dia de antecipação; R$ 400,50 até a Ultimate Plus) são aritmética direta desses preços. Preços de FC Points avulsos e promoções variam por plataforma e por data — por isso o vídeo ensina a comparação e não crava esses valores. A menção à "promoção histórica" do EA FC 26 refere-se à cobertura do próprio nicho em junho de 2026. Este vídeo é análise educativa de decisão de compra; não é aconselhamento financeiro e não tem afiliação com a Electronic Arts.
"""

SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-004",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#F2F2F7", "c1": "#FF4D6D", "c2": "#4CC9F0", "bg": "#0F1020"},
    "thumb": {"l1": "STANDARD OU PLUS?", "l2": "a conta em reais"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/nivel-do-jogo-004.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")

    from ensaio import MODELO_VOZ, duracao_estimada  # noqa: E402
    R, P = MODELO_VOZ[SPEC["voz"]]
    dl = duracao_estimada(CENAS, SPEC["voz"])
    ds = duracao_estimada(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"voz {SPEC['voz']}: {R} chars/s + {P} s/frase")
    print(f"longo: {sum(len(c['nar']) for c in CENAS)} chars -> {dl/60:.1f} min")
    print(f"short: {sum(len(c['nar']) for c in SHORT)} chars -> {ds:.0f} s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
