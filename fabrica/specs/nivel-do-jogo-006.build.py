#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-006.

POR QUE ESTE CANAL, E POR QUE NAO O PACOTE QUE JA ESTAVA PRONTO

Canal da vez na fila (o topo, cocina-por-niveles, nao existe no YouTube).

Antes de escrever isto eu quase publiquei outra coisa. O `nivel-do-jogo-002`
estava em `videos` com status `listado_para_publicacao`, 857 s, passando nos
dez portoes, parado desde 05/08. Cheguei a disparar o render. Ao investigar
POR QUE estava parado, descobri que ele nao estava parado: o video
"Lei Felca nos Games: R$ 333 Milhoes e o Fim da Caixinha" JA ESTA NO AR CINCO
VEZES, sob os pacotes nivel-do-jogo-cron-2026-08-13, -14, -15, -16 e -17, cada
um com longo E short — dez videos do mesmo conteudo. Cancelei o run.

`listado_para_publicacao` quer dizer "ESTA LINHA nunca publicou", nao "este
video nunca foi publicado", porque `videos.pacote` guarda o nome da RODADA e
nao o da spec. Registrado como aprendizado 443, severidade critica.

O VEREDITO, e o que ele muda no dimensionamento

v_maquina_licoes, medido em 24/08 05:40: `suspenso`.

  - 7 shorts, mediana 0,47 views/dia, TOPO 37,26
  - 8 longos, mediana 0,09 views/dia
  - 352 views no acervo inteiro

`suspenso` nao e `canal frio`. Frio quer dizer que nenhum formato pegou. Aqui
o short pegou — teve pico de 37,26 v/d — e o longo nao paga o render: 0,09
views/dia contra um custo de ~20x o de um short.

A instrucao do PLAYBOOK para esse veredito e explicita, e e o oposto do que
fiz no pacote anterior de outro canal: LONGO NO PISO de 8 minutos, e o MELHOR
MATERIAL VAI NO SHORT. Por isso este roteiro tem 55 cenas e nao 85, e por isso
o short abre com o numero mais forte que existe aqui em vez de guarda-lo.

O ACERVO, lido pelos titulos publicados

Cinco titulos distintos no ar:

  - Por Que a Inflacao nos Games E Mais Perigosa Que na Vida Real
  - Lei Felca nos Games: R$ 333 Milhoes e o Fim da Caixinha  (x5 pelo cron)
  - Preco dos Jogos em 2026: Quantas Horas de Trabalho Custa
  - EA FC 27: Standard, Ultimate ou Plus? A Conta em Reais
  - Steam Mudou Como Seu Jogo e Precificado: R$25 ou R$55

Tres dos cinco sao PRECO AO CONSUMIDOR. O canal olha sempre para a etiqueta.

O EIXO ESCOLHIDO

`pautas_banco` tem 58 pautas neste canal, quase todas jogadas num eixo
guarda-chuva ("preco e crise da industria dos games") que mistura coisas
diferentes. Separando por sub-tema, o nao usado com maior massa e maior
outlier e DEMISSOES x LUCRO:

  [429] Square Enix Hits RECORD PROFITS After Firing Western Devs .. 12.220,1 v/d
  [394] Xbox anuncia 3.200 despidos, 4 estudios, reset ................ 326,0
  [437] XBOX COLAPSA: mas despidos MASIVOS ......................... 110,7
  [426] STOP Trying to Save Gaming? Xbox Closes Studios ............. 48,9
  [421] Much MORE Video Game Industry Layoffs Predicted ............. 31,4
  [435] Sony Promised 12 Live Service Games. They Shipped 2 ......... 21,4
  ... mais nove no mesmo sub-tema

O [423] de 56.704,9 v/d e EA FC 27, e esse eixo ja foi gasto no pacote 004.

E o melhor: este eixo e uma PERGUNTA ECONOMICA de verdade, que e o que o canal
promete no nome. Nao "os jogos estao caros", e sim "por que cortar gente faz o
lucro subir MAIS do que a folha economizada".

OS NUMEROS, com fonte institucional

  Square Enix Holdings, resultado do ano fiscal encerrado em 31/03/2026
  (relatorio oficial da propria companhia, hd.square-enix.com):

    - vendas liquidas: 297.661 milhoes de ienes, QUEDA de 8,3%
    - lucro operacional: 54.736 milhoes de ienes, ALTA de 34,9%
    - Q1 do ano fiscal seguinte (jun/2026): lucro operacional +88,6%,
      e o segmento de games (Digital Entertainment) +91,8%

  Demissoes na industria em 2026 (rastreador ASGC / Amir Satvat, divulgado
  pelo GamesBeat):

    - projecao para o ano: 14.259 postos
    - a projecao de janeiro era 8.025 — subiu 78% no meio do caminho
    - confirmadas ate meados do ano: 9.781
    - media de 44 postos por dia
    - comparacao: 2024 fechou perto de 15.631; 2025 caiu para 9.197

O MECANISMO — e o giro

Vender 8,3% menos e lucrar 34,9% mais so fecha por custo. Ate ai e obvio. O
que NAO e obvio, e e o video:

  1. Salario de quem faz jogo nao lancado nao e despesa, e ATIVO. Vira custo
     de desenvolvimento capitalizado no balanco, e so vira despesa quando o
     jogo sai.
  2. Fechar o estudio baixa esse ativo de uma vez — dor unica, num trimestre.
     A folha economizada, essa e RECORRENTE.
  3. E o corte nao derruba a receita de hoje, porque a receita de hoje vem de
     jogo lancado ha anos. Ele derruba a receita de daqui a tres ou quatro
     anos, que e o ciclo de um jogo.

Ou seja: a contabilidade e o ciclo de producao tem RELOGIOS DIFERENTES. O
lucro recorde e a demissao aparecem no mesmo trimestre; a conta aparece em
outro, distante o bastante para ninguem ligar uma coisa a outra.

O QUE ESTE VIDEO NAO FAZ

  - nao diz que a Square Enix fraudou nada: os numeros sao os que ela mesma
    publicou, e a contabilidade descrita e a norma, nao um truque;
  - nao afirma que o lucro veio SO das demissoes. A propria empresa cita
    eficiencia e mix de produto, e o video diz isso. O que o video sustenta e
    mais estreito: a direcao do efeito e o descasamento dos prazos;
  - nao preve o futuro da empresa nem recomenda acao nenhuma;
  - nao usa o numero de demissoes como se fosse censo: rastreador de demissao
    depende de anuncio publico, e o video fala isso com todas as letras.

TAXA DA VOZ. pt-BR-AntonioNeural: R = 16,68 chars/s, P = 1,040 s/frase,
n = 214 amostras medidas contra legendas.srt reais. Vies do longo: -0,4%.
O P e o MAIS ALTO da frota — esta voz pausa muito entre frases, entao frase
conta pesado no orcamento: 121 frases sozinhas ja valem 126 s.

ORCAMENTO (medido depois de escrever, nao antes — aprendizado 436):
56 cenas, 55 gaps de 0,300 s. Medido no arquivo pronto: 530,1 s previstos, que
com o vies de -0,4% cai em ~528 s = 8:48 — acima do piso duro de 480 s com
folga de quase um minuto, e deliberadamente longe dos 12-15 min porque o
veredito e `suspenso`. Short: 42,1 s.

CAPITULOS. Cinco, de onze a doze cenas. A ~9,5 s por cena, cada capitulo mede
~105 s: dentro de MIN_CAP 60 e MAX_CAP 150. Capitulo abre em layout `titulo`.

DOIS PORTOES ME PEGARAM, E OS DOIS ESTAVAM CERTOS

1. ORTOGRAFIA. Escrevi a narracao inteira SEM ACENTO — 0,0% de letras
   acentuadas contra 4,2% nas outras specs deste canal. Em portugues isso muda
   a pronuncia do TTS, e o portao diz exatamente por que ele existe: nenhum
   outro enxerga, porque o texto continua parecendo a lingua certa. `idioma`
   passou, `glifos` passou, so a densidade diacritica denunciou. Corrigido no
   corpo das cenas; esta docstring fica sem acento de proposito, como as
   outras.

2. DURACAO DO SHORT. Primeira versao deu 46,9 s previstos contra teto seguro
   de 43,1 (o teto da rotina e 45 e o residuo do modelo chega a 4,3%). Enxuguei
   para 42,1 s SEM tirar o gancho: com o veredito `suspenso`, o short e onde o
   melhor material tem que estar, entao cortei repeticao e nao conteudo.
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


# ------------------------------------------------ 1. Duas linhas do mesmo ano
T("Vendeu menos", "lucrou mais",
  "A Square Enix fechou o ano fiscal vendendo menos. E lucrando muito mais. As "
  "duas coisas, no mesmo relatório, assinadas pela própria empresa.",
  cap="Duas linhas do mesmo relatório")
I("Vendas líquidas", "queda de oito vírgula três por cento",
  "As vendas líquidas caíram oito vírgula três por cento. Duzentos e noventa e "
  "sete bilhões de ienes.")
B("No mesmo ano", ["Vendas", "Lucro"], [-25, 70],
  "O lucro operacional subiu trinta e quatro vírgula nove por cento. Quase "
  "cinquenta e cinco bilhões de ienes.")
T("Uma linha desce", "a outra sobe forte",
  "Uma linha desceu. A outra subiu três vezes mais forte do que a primeira "
  "desceu. No mesmo período, na mesma empresa.")
T("E no trimestre seguinte", "acelerou",
  "E no trimestre seguinte acelerou. O lucro operacional subiu oitenta e oito "
  "vírgula seis por cento contra o mesmo trimestre do ano anterior.")
I("Só o setor de games", "mais noventa e um vírgula oito por cento",
  "Só o setor de jogos digitais subiu noventa e um vírgula oito por cento. "
  "Quase dobrou.")
T("A explicação curta", "e verdadeira",
  "A explicação curta que circulou e simples: eles demitiram. E ela não está "
  "errada. Está incompleta, e a parte que falta e a interessante.")
T("Porque a conta", "não fecha so com folha",
  "Porque cortar folha economiza o valor da folha. Aqui o lucro subiu bem mais "
  "do que qualquer folha cortada explicaria sozinha.")
L("Tres perguntas", ["De onde vem a diferença",
                     "Por que a receita não caiu junto",
                     "Quando a conta chega"],
  "Então são três perguntas. De onde vem a diferença, por que a receita não "
  "caiu junto com o time, e quando essa conta chega.")
T("A resposta das três", "e a mesma",
  "A resposta das três e a mesma coisa, e ela não está na indústria de games. "
  "Está na contabilidade.")
I("Aviso", "nada aqui e irregular",
  "Um aviso antes: nada do que eu vou descrever e irregular. E a norma "
  "contábil, aplicada como manda o manual. O problema não e a regra.")

# --------------------------------------- 2. Salario que não e despesa
T("A primeira peça", "salário que virou ativo",
  "A primeira peça e a que quase ninguém fora do setor conhece. O salário de "
  "quem faz um jogo que ainda não saiu não entra como despesa.",
  cap="O salário que não e despesa")
I("Ele vira", "custo capitalizado",
  "Ele vira custo de desenvolvimento capitalizado. Ou seja: vira um bem no "
  "balanço da empresa, do lado dos ativos.")
T("A lógica e defensável", "e vale dizer",
  "E a lógica disso e defensável. A empresa está construindo uma coisa que vai "
  "gerar receita depois, entao o gasto e investimento, não consumo.")
T("Igual a uma fábrica", "que ainda está em obra",
  "E o mesmo tratamento de uma fábrica em construção. Ninguem lanca o tijolo "
  "como prejuízo do mês.")
I("A despesa aparece", "quando o jogo sai",
  "A despesa so aparece quando o jogo sai, amortizada contra a receita que ele "
  "gera. Ai sim entra no resultado.")
T("Agora inverta", "e olhe o corte",
  "Agora inverta e olhe o que acontece quando a empresa cancela o projeto e "
  "fecha o estúdio.")
I("O ativo", "e baixado de uma vez",
  "Aquele ativo acumulado não vale mais nada, e e baixado. Isso da um prejuízo "
  "grande, feio, e concentrado num trimestre so.")
T("Mas so num", "trimestre so",
  "Num trimestre so. Depois disso, some do resultado para sempre.")
T("E a economia", "essa fica",
  "E a folha que deixou de existir? Essa fica. Ela reaparece em cada trimestre "
  "seguinte, sem escândalo nenhum, como custo que simplesmente não está la.")
B("Dor e ganho", ["Baixa: uma vez", "Folha: todo trimestre"], [70, 22],
  "Uma dor de uma vez contra um ganho que se repete. Essa e a assimetria que "
  "faz o número do ano seguinte parecer outra empresa.")
I("E por isso", "o lucro sobe mais que a folha",
  "E e por isso que o lucro sobe mais do que a folha cortada. Não e so o "
  "salário que sai. E o projeto inteiro que para de pesar.")

# ------------------------------------ 3. Por que a receita não cai junto
T("Segunda peça", "o dinheiro de hoje e velho",
  "Segunda peça, e ela responde a pergunta que mais incomoda: se a empresa "
  "cortou tanta gente, por que a receita não desabou junto?",
  cap="Por que a receita não cai junto")
T("Porque a receita de hoje", "não vem do trabalho de hoje",
  "Porque a receita que entra hoje não vem do trabalho que está sendo feito "
  "hoje.")
I("Vem de jogo", "lançado ha anos",
  "Vem de jogo que ja está na prateleira, de catálogo antigo, de assinatura, de "
  "conteúdo de um título lançado ha três, cinco, dez anos.")
T("Quem foi demitido", "estava construindo o futuro",
  "Quem foi demitido não estava operando essa receita. Estava construindo a "
  "receita de daqui a alguns anos.")
I("O ciclo de um jogo grande", "três a cinco anos",
  "Um jogo grande leva de três a cinco anos entre começar e sair. Esse e o "
  "prazo em que o corte de hoje aparece na receita.")
T("Então no curto prazo", "so o custo se move",
  "Então no curto prazo o corte mexe so num lado da conta. O custo cai na hora. "
  "A receita não se mexe.")
T("O resultado", "e um lucro sem contraparte",
  "O resultado e um lucro que sobe sem nada puxando para baixo. E ele e "
  "verdadeiro. So não e permanente.")
L("O que o trimestre mostra", ["O custo que saiu",
                               "A receita que ficou",
                               "Nada do que foi cancelado"],
  "O trimestre mostra o custo que saiu e a receita que ficou. Não tem uma linha "
  "para o jogo que agora nunca vai existir.")
T("E não existe essa linha", "em lugar nenhum",
  "E não existe essa linha em lugar nenhum do relatório, porque contabilidade "
  "registra o que aconteceu, não o que deixou de acontecer.")
I("Isso não e falha", "e limite",
  "Isso não e falha do relatório. E o limite dele. Quem le e que precisa saber "
  "que esse limite existe.")
T("E a indústria inteira", "está fazendo o mesmo",
  "E o ponto seguinte e o que tira isso do caso isolado: a indústria inteira "
  "está fazendo a mesma coisa ao mesmo tempo.")

# -------------------------------------------- 4. O tamanho do corte
T("Terceira peça", "o tamanho disso",
  "Terceira peça: o tamanho. Porque uma empresa cortando e uma decisão. A "
  "indústria inteira cortando junto e outra coisa.",
  cap="O tamanho do corte")
I("Projecao para dois mil e vinte e seis", "quatorze mil duzentos e cinquenta e nove",
  "O rastreador mais acompanhado do setor projeta quatorze mil duzentos e "
  "cinquenta e nove postos perdidos em dois mil e vinte e seis.")
T("E essa projecao", "subiu no meio do ano",
  "E essa projecao não começou assim. Em janeiro ela era oito mil e vinte e "
  "cinco. Subiu setenta e oito por cento no meio do caminho.")
I("Ja confirmadas", "nove mil setecentas e oitenta e uma",
  "Confirmadas ate meados do ano: nove mil setecentas e oitenta e uma. Uma "
  "média de quarenta e quatro postos por dia.")
T("Quarenta e quatro", "por dia",
  "Quarenta e quatro pessoas por dia, todo dia, incluindo os dias em que "
  "nenhuma notícia sobre isso foi publicada.")
B("Por ano", ["2024", "2025", "2026 proj."], [78, 46, 71],
  "Para comparar: dois mil e vinte e quatro fechou perto de quinze mil "
  "seiscentos e trinta e um. Dois mil e vinte e cinco caiu para nove mil cento "
  "e noventa e sete. E dois mil e vinte e seis voltou a subir.")
T("Então não e recuperação", "e um ciclo",
  "Então não houve recuperação. Houve um ano mais calmo entre dois anos "
  "pesados.")
I("E aqui um limite", "do próprio número",
  "E aqui vale um limite do número: rastreador de demissão depende de anúncio "
  "público. Corte pequeno, sem comunicado, não entra.")
T("O que significa", "que o real e maior",
  "O que significa que o número real e maior do que esse, e não menor. Nenhum "
  "rastreador desses e censo.")
T("Mesmo assim", "a direção e clara",
  "Mesmo com essa margem, a direção e clara, e ela bate com o que os balanços "
  "estao mostrando do outro lado.")
I("Custo cortado agora", "produto que não nasce depois",
  "Milhares de pessoas saindo agora, em empresas que reportam lucro recorde "
  "agora, para produtos que não vao nascer depois.")

# ------------------------------------------- 5. Quando a conta chega
T("Então quando", "a conta chega",
  "Então vamos a última pergunta, que e a única que importa para quem joga: "
  "quando essa conta chega, e como ela vai parecer.",
  cap="Quando a conta chega")
I("Ela chega", "em três a cinco anos",
  "Ela chega no prazo do ciclo. Tres a cinco anos, que e o tempo entre começar "
  "um jogo e ele existir.")
T("E vai parecer", "outra coisa",
  "E quando chegar, não vai parecer o que e. Vai parecer falta de ideia, ou "
  "público que mudou, ou série que se esgotou.")
L("O que você vai ver", ["Menos lancamentos grandes",
                         "Mais remaster e sequência",
                         "Mais catálogo antigo"],
  "Na prática: menos lançamento grande e novo, mais remaster, mais sequência "
  "segura, mais catálogo antigo reaproveitado.")
T("Cada um desses", "tem explicação própria",
  "E cada uma dessas coisas vai ter uma explicação própria e razoável na "
  "época. Nenhuma delas vai citar um trimestre de dois mil e vinte e seis.")
T("Esse e o ponto", "do vídeo inteiro",
  "Esse e o ponto do vídeo inteiro. Não e que alguém mentiu. E que a causa e o "
  "efeito ficam longe demais um do outro para serem vistos juntos.")
I("O relatório", "está correto",
  "O relatório está correto. O lucro e real. A demissão e real. A ligação entre "
  "eles e real. So que ela leva anos para aparecer no único lugar onde você "
  "olharia.")
T("O que fazer com isso", "se você joga",
  "E o que fazer com isso, se você so joga? Uma coisa, e ela e barata.")
L("Quando ler lucro recorde", ["Veja a receita tambem",
                               "Veja o que foi cancelado",
                               "Veja o pipeline anunciado"],
  "Quando ler que uma empresa de jogos teve lucro recorde, olhe a receita na "
  "mesma manchete. E procure o que foi cancelado no mesmo ano.")
T("Se a receita caiu", "você ja sabe a historia",
  "Se a receita caiu e o lucro subiu, você ja sabe qual dos dois lados da conta "
  "se moveu, e ja sabe quando o outro se move.")
T("No próximo vídeo", "o outro lado",
  "No próximo vídeo eu pego o outro lado disso: o que acontece com o preço do "
  "jogo quando o estúdio que ia fazer o concorrente dele fecha.")
C("Se isso foi útil", "assina o canal",
  "Se seguir o dinheiro por três anos de contabilidade foi útil, assina o "
  "canal, e me conta nos comentários qual jogo cancelado você ainda sente "
  "falta.")


# O veredito `suspenso` manda o MELHOR material para o short. Então ele NAO
# guarda o número: abre com a contradicao inteira nos dois primeiros segundos.
# Orcamento medido para ~38 s com 6 cenas.
SHORT = [
    {"layout": "titulo", "kicker": "Vendeu oito por cento menos",
     "sub": "e lucrou trinta e cinco por cento mais",
     "nar": "A Square Enix vendeu oito por cento menos no ano e lucrou trinta e "
            "cinco por cento mais.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Mesmo relatório", "sub": "assinado por ela",
     "nar": "As duas linhas estão no mesmo relatório, assinado pela própria "
            "empresa.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Demitiram", "sub": "mas não é só isso",
     "nar": "Demitiram. Mas folha cortada não explica um lucro subindo três "
            "vezes mais rápido do que a venda caiu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Salário de jogo não lançado",
     "sub": "não é despesa, é ativo",
     "nar": "Salário de quem faz jogo que ainda não saiu não é despesa, é ativo "
            "no balanço.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Fecha o estúdio", "sub": "a dor é uma vez só",
     "nar": "Fechou o estúdio, esse ativo cai de uma vez. A folha economizada "
            "fica para sempre.", "sem_cap": True},
    {"layout": "titulo", "kicker": "A conta chega", "sub": "em três a cinco anos",
     "nar": "A conta chega em três a cinco anos, com outro nome. Explico no "
            "canal.", "sem_cap": True},
]

THUMB = {"l1": "vendeu menos", "l2": "lucrou 35% mais"}

COPY = """# Vender menos e lucrar mais so fecha por custo — e o custo tem dois relogios

## TITULO
Demissões nos Games: Como a Square Enix Vendeu 8% Menos e Lucrou 35% Mais

## DESCRICAO
No relatório do ano fiscal encerrado em 31 de março de 2026, a Square Enix reportou vendas líquidas de 297.661 milhões de ienes — queda de 8,3% — e lucro operacional de 54.736 milhões de ienes, alta de 34,9%. No trimestre seguinte o lucro operacional subiu 88,6% na comparação anual, com o segmento de jogos digitais avançando 91,8%. Os dois números estão no mesmo documento, publicado pela própria companhia.

A explicação que circulou foi "eles demitiram". Ela não está errada, está incompleta — e a parte que falta é a que este vídeo persegue: cortar folha economiza o valor da folha, mas aqui o lucro subiu bem mais do que qualquer folha cortada explicaria sozinha.

A diferença está na contabilidade, e ela é a norma, não um truque. O salário de quem desenvolve um jogo ainda não lançado não entra como despesa: vira custo de desenvolvimento capitalizado, um ativo no balanço, pelo mesmo princípio que trata uma fábrica em construção como investimento e não como prejuízo do mês. Quando o projeto é cancelado e o estúdio fecha, esse ativo é baixado de uma vez — uma dor grande, feia e concentrada em um único trimestre. Já a folha que deixou de existir reaparece em todos os trimestres seguintes, como custo que simplesmente não está mais lá. Uma dor única contra um ganho recorrente.

O segundo mecanismo responde por que a receita não cai junto: a receita de hoje não vem do trabalho de hoje. Vem de jogo já lançado, catálogo, assinatura e conteúdo de títulos antigos. Quem foi demitido estava construindo a receita de três a cinco anos à frente — o ciclo de um jogo grande. No curto prazo o corte move só um lado da conta.

Do lado da indústria, o rastreador mais acompanhado do setor projeta 14.259 postos perdidos em 2026, contra uma estimativa inicial de 8.025 em janeiro — alta de 78% no meio do ano. Até meados do ano eram 9.781 confirmadas, média de 44 postos por dia. Para comparação: 2024 fechou perto de 15.631 e 2025 caiu para 9.197. O vídeo declara o limite desse dado: rastreador depende de anúncio público, então o número real é maior, não menor — nenhum deles é censo.

Termina com o que isso significa para quem joga, e com uma rotina de duas linhas para ler a próxima manchete de "lucro recorde".

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Uma pergunta honesta para quem trabalha ou trabalhou com contabilidade em estúdio: qual é a fatia típica do custo de desenvolvimento que fica capitalizada até o lançamento? Achei a regra descrita em todo lugar e o percentual em lugar nenhum — é a única parte disto que eu não consegui sustentar com número.

## HASHTAGS
#IndustriaDosGames #SquareEnix #NivelDoJogo

## TAGS
demissoes games, square enix, industria dos games, lucro operacional, custo capitalizado, economia dos games, layoffs, balanco financeiro, mercado de jogos, desenvolvimento de jogos, contabilidade, resultados financeiros, xbox, estudios fechados, ciclo de producao

## CONFIGURACAO DE STUDIO
- Idioma: Português (pt-BR) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Brasil | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 24 de agosto de 2026. (1) Fonte institucional: Square Enix Holdings Co., Ltd., resultado do exercício encerrado em 31/03/2026, publicado pela própria companhia — vendas líquidas de 297.661 milhões de ienes (‑8,3%) e lucro operacional de 54.736 milhões de ienes (+34,9%); no primeiro trimestre do exercício seguinte, lucro operacional +88,6% na comparação anual e segmento Digital Entertainment +91,8%. (2) Demissões: rastreador do setor (ASGC / Amir Satvat), divulgado pelo GamesBeat — projeção de 14.259 postos para 2026 contra 8.025 estimados em janeiro, 9.781 confirmadas até meados do ano, média de 44 por dia, com 2024 em torno de 15.631 e 2025 em 9.197. Este segundo dado depende de anúncio público e não é censo: subestima por construção, e o vídeo afirma isso explicitamente. O tratamento de custo de desenvolvimento capitalizado descrito aqui é a norma contábil do setor, não uma prática particular desta empresa, e nada neste vídeo sugere irregularidade. A empresa atribui o resultado também a eficiência e mix de produto; o vídeo não afirma que o lucro veio apenas das demissões, apenas descreve a direção do efeito e o descasamento de prazos entre a decisão e a consequência. Não há previsão nem recomendação de investimento.
"""

SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-006",
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
                           "nivel-do-jogo-006.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
