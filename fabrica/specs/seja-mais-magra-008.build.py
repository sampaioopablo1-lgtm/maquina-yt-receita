#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-008.

ALAVANCA ATACADA: **A — conversao short -> inscrito.** Terceiro pacote do
experimento 26: o PEDIDO do short vira a inscricao.

NUMERO DE PARTIDA, medido em 01/09/2026 (retrato por `channels.list`):

    seja-mais-magra ... 1 inscrito, 143 views, 14 videos no ar
                        7 pacotes publicados
                        short: mediana 1,41 views/dia, topo 8,84
                        longo: mediana 0,00 views/dia
                        veredito: `canal frio`

O QUE DEU CERTO — e e pouco, e vale dizer que e pouco: os dois shorts de maior
alcance sao "Atividade Fisica: as Duas Faixas Oficiais" com quarenta views e
"Ozempic e Mounjaro" com trinta e duas. Nenhum dos dois converteu.

O QUE NAO DEU: os longos, e nao e "quase nenhum". SETE de sete estao em zero ou
duas views. E os quatro mais antigos tem entre setecentos e dez e oitocentos e
setenta e dois segundos, dimensionados para o teto quando a alavanca B ja
mandava o piso.

E aqui esta a parte que muda a decisao desta rodada: **a forma ja foi corrigida
neste canal, duas vezes, e nao mudou nada.** "Produtos com Proteina: A Conta
por Grama" e "Tabela Nutricional: a Coluna Certa" sao os dois exatamente o que
o aprendizado 504 pede — conta que o espectador faz em si mesmo. Tiveram
dezenove e vinte e cinco views de short, e zero inscritos.

Pelo aprendizado 540 isso normalmente mandaria pular o canal. Nao pulei, por
dois motivos: e um dos dois unicos canais liberados pelo teto de um longo por
dia nesta hora, e — o que importa mais — **os dois pacotes com a forma certa
tinham o CTA apontando para o video completo**. A forma foi corrigida; o
PEDIDO nunca foi. Entao este canal nao e uma repeticao: e o terceiro braco do
experimento 26, aberto ontem.

O QUE MUDO POR CAUSA DISSO:

1. **EIXO NOVO** (regra do `canal frio`), e ele sai do produto e da regulacao —
   Anvisa, semaglutida, alegacoes, rotulo, faixas oficiais — e vai para o dado
   que o espectador ja tem no bolso.

2. **O PEDIDO** (experimento 26): o short entrega a conta fechada E pede a
   inscricao, amarrada ao metodo. Nao aponta para o longo. Terceiro canal,
   terceira lingua.

ADAPTACAO HONESTA DA CONDICAO 1 DO APRENDIZADO 504: ali a condicao e "o
dinheiro e DELE". Num canal de saude o analogo nao e dinheiro, e DADO — e o
principio e o mesmo: os numeros da conta tem de sair do aparelho dele, nao de
uma tabela minha. Estou anotando a adaptacao em vez de fingir que a regra
original cabe.

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: eixo novo e o piso de **oito minutos**. Com todos os longos do
canal em zero, dimensionar para treze minutos seria gastar render em algo que
ninguem abre.

Oito capitulos com ~64s NA ESTIMATIVA, e a resposta fechando ate **185s** — a
margem foi corrigida de 192 para 185 na rodada anterior, porque com 192
desenhado duas vozes seguidas fecharam aos 204s no video publicado (aprendizado
537). O tempo REAL vai ser conferido no copy.md renderizado antes de publicar.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **o vao entre a semana e o fim de semana, medido no proprio
celular**. Os eixos ja publicados aqui sao proibicoes da Anvisa, reganho com
canetas, proteina por grama, alegacoes de shake e termogenico, semaglutida
generica, coluna da tabela nutricional e faixas oficiais de atividade. Nenhum
deles usa o historico que o espectador ja carrega.

AS TRES CONDICOES DO APRENDIZADO 504 (com a adaptacao acima):
1. os numeros sao DELE — o historico de passos ou minutos ativos do celular;
2. e ESCOLHA COM PRAZO — o proximo fim de semana, que chega em dias;
3. o SHORT entrega a conta — a subtracao fechada, e depois pede a inscricao.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita meta de passos, nao cita minutos recomendados, nao cita
caloria, nao cita peso e nao cita nome de aplicativo nem de aparelho. Os dois
numeros da conta saem do historico do proprio espectador. Nao ha numero meu
para certificar em duas fontes, e por isso nao ha numero meu que possa
envelhecer nem que dependa da idade, do peso ou da condicao dele.

O QUE O VIDEO NAO FAZ: nao prescreve exercicio, nao diz quanto ninguem deve se
mexer, nao promete emagrecimento, nao fala de dieta e nao e aconselhamento
medico. E ha um aviso explicito no fim do roteiro para quem tem condicao de
saude ou orientacao medica em contrario.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("Seu celular já contou", "e você nunca olhou assim",
  "O seu celular vem contando quanto você se move há meses. E provavelmente "
  "você nunca olhou esses números do jeito que muda alguma coisa.",
  cap="O que o celular já contou")
I("Não é sobre meta", "é sobre o seu padrão",
  "Isso não é sobre bater meta nenhuma. É sobre enxergar o seu padrão, que é "
  "uma pergunta diferente e bem mais útil.")
I("E tem prazo", "o próximo fim de semana",
  "E tem prazo curto: o próximo fim de semana chega em poucos dias.")
I("Os dois números existem", "e são seus",
  "Os dois números de que você precisa já existem, e os dois são seus. Não "
  "vêm de tabela nenhuma, nem da minha nem de ninguém.")
I("Nada para instalar", "nada para começar",
  "Você não precisa instalar nada, comprar nada nem começar nada. O histórico "
  "já está gravado.")
I("Ninguém faz por você", "nem o aplicativo",
  "E ninguém faz essa conta por você. O aplicativo mostra o dia de hoje, "
  "porque é isso que prende. O padrão de quatro semanas ele não mostra.")
I("Não é planilha", "é uma vez só",
  "Isso também não vira rotina nova. É uma sentada, com o que já está "
  "gravado, e depois você segue a sua vida.")
I("E serve pra decidir", "não pra cobrar",
  "O resultado serve pra decidir onde mexer. Não serve pra te cobrar nada.")
I("O que vem agora", "uma subtração",
  "Em alguns minutos você faz essa conta sozinha. Duas médias e uma "
  "subtração.")

# -------------------------------------------------------------------- cap 2
T("Os dois lados", "os dias úteis e o resto",
  "A conta tem dois lados, e quase ninguém separa os dois.",
  cap="Os dois lados da semana")
I("Lado um", "segunda a sexta",
  "O primeiro lado é a média dos seus dias de semana. Segunda a sexta, e "
  "só eles.")
I("Lado dois", "sábado e domingo",
  "O segundo lado é a média do sábado e do domingo. Separados do resto, "
  "sempre.")
I("Use quatro semanas", "não uma",
  "Use as últimas quatro semanas. Uma semana isolada quase sempre teve "
  "alguma coisa fora do normal.")
I("Passos ou minutos", "escolha um",
  "Pode ser passos ou minutos ativos, desde que seja o mesmo nos dois lados.")
I("Não misture as unidades", "esse é o erro comum",
  "Misturar passos de um lado com minutos do outro inventa uma diferença que "
  "não existe.")
I("Por que separar", "os dois dias são outra vida",
  "Sábado e domingo costumam ter outra rotina e outro horário. Somar tudo "
  "junto apaga isso.")
I("São lados de tamanho diferente", "por isso média",
  "Os dois lados não têm o mesmo tamanho. Um tem os dias de trabalho, o "
  "outro tem só o fim de semana.")
I("Então não some", "tire média",
  "Por isso não some os dois lados. Tire a média de cada um. Média com média "
  "é a única comparação justa aqui.")
I("Feriado no meio", "conte como fim de semana",
  "Feriado no meio da semana vai para o lado do fim de semana.")
I("Agora dá pra comparar", "média com média",
  "Com os dois lados na mesma unidade, isso deixa de ser impressão e vira "
  "aritmética sobre a sua própria semana.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — margem de 185s (aprendizado 537).
T("A conta", "uma subtração",
  "Então a conta. Duas médias, uma subtração.",
  cap="A conta: uma subtração")
I("Passo um", "média de segunda a sexta",
  "Passo um: some os cinco dias úteis de cada semana e divida por cinco. Faça "
  "isso nas quatro semanas e tire a média.")
I("Passo dois", "média do fim de semana",
  "Passo dois: some sábado e domingo e divida por dois. Também nas quatro "
  "semanas.")
I("Passo três", "subtraia",
  "Passo três: subtraia a segunda média da primeira. O que sobrar é o seu "
  "vão de fim de semana.")
I("Se der positivo", "você cai no fim de semana",
  "Se der positivo, você se move menos no fim de semana do que nos dias "
  "úteis. E agora você sabe de quanto.")
I("Se der negativo", "é o contrário",
  "Se der negativo, é o contrário: o fim de semana é onde você se move mais, "
  "e a semana é que está parada.")
I("Escreva os dois", "lado a lado",
  "Escreva os dois números lado a lado num papel. Ver os dois juntos já muda "
  "o que você entende, antes mesmo da subtração.")
I("E anote o sinal", "ele é metade da resposta",
  "E anote o sinal junto com o número. O sinal é metade da resposta, e é a "
  "metade que as pessoas esquecem de olhar.")
I("A conta acabou aqui", "o resto é o porquê",
  "A conta acabou aqui e você já pode fazer a sua. O resto do vídeo é onde "
  "achar os números e o que essa conta não pega.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Onde achar", "no próprio aparelho",
  "Agora onde esses números estão, porque quase ninguém abre essa tela.",
  cap="Onde achar os números")
I("O histórico", "costuma ter meses",
  "O aplicativo de saúde do próprio celular guarda o histórico, e costuma "
  "guardar meses, não dias.")
I("Procure a visão semanal", "não a do dia",
  "Procure a visão por semana, e não a do dia. É ela que dá o número por dia "
  "sem você somar nada à mão.")
I("Anote sete números", "por semana",
  "Anote os sete números de cada semana. São vinte e oito ao todo, e cabem "
  "num papel.")
I("Se faltar um dia", "pule a semana",
  "Se em alguma semana faltar dado — celular no carregador, dia sem sair com "
  "ele —, pule a semana inteira em vez de inventar o dia.")
I("E se for relógio", "vale igual",
  "Se você usa relógio ou pulseira, vale igual. O que não vale é comparar uma "
  "semana medida pelo relógio com outra medida pelo celular.")
I("Quatro semanas seguidas", "sem escolher",
  "Use quatro semanas seguidas, e não as quatro que você gostou mais. "
  "Escolher semana é o jeito mais fácil de provar o que você já achava.")
I("Se você trocou de aparelho", "recomece a contagem",
  "E se você trocou de celular no meio, conte só as semanas do aparelho "
  "atual. Aparelhos diferentes contam diferente.")
I("Na dúvida", "erre para menos",
  "E na dúvida, erre para menos no lado do fim de semana. Se o vão aparecer "
  "mesmo com uma conta conservadora, ele existe mesmo.")

# -------------------------------------------------------------------- cap 5
T("O que a conta não pega", "e é justo dizer",
  "Tem coisas que essa conta não captura, e é mais honesto dizer do que "
  "fingir que ela decide tudo.",
  cap="O que a conta não pega")
I("A intensidade", "não aparece",
  "A primeira: intensidade. Um passeio lento e uma subida forte contam "
  "parecido em passos, e não são a mesma coisa.")
I("Por isso os minutos ativos", "ajudam",
  "Por isso, se o seu aparelho tiver minutos ativos além de passos, faça a "
  "conta com os dois. Onde eles discordam, tem informação.")
I("A segunda", "o que não é passo",
  "A segunda: o que não é passo. Bicicleta, natação e musculação quase não "
  "aparecem na contagem, e mesmo assim aconteceram.")
I("Se o seu treino é assim", "conte à parte",
  "Se o seu movimento principal é desse tipo, anote esses dias à parte, "
  "senão a conta vai dizer que você parou quando você não parou.")
I("A terceira", "o descanso é legítimo",
  "A terceira não é um erro de medida: descansar é legítimo. Um vão pequeno "
  "no fim de semana pode ser exatamente o que o seu corpo precisava.")
I("A quarta", "semana difícil acontece",
  "E tem a quarta: uma semana de doença, de viagem ou de trabalho pesado "
  "muda tudo, e ela não avisa no número.")
I("A conta não julga", "ela mostra o tamanho",
  "Essa conta não diz que você deveria estar fazendo mais. Ela mostra o "
  "tamanho de uma diferença que você não estava vendo.")

# -------------------------------------------------------------------- cap 6
T("O caso que engana", "a semana de trabalho",
  "Agora o caso que engana quase todo mundo, e ele merece um capítulo.",
  cap="O caso que engana")
I("Muita gente descobre", "que anda por obrigação",
  "Muita gente faz essa conta e descobre uma coisa incômoda: quase todo o "
  "movimento da semana vem do deslocamento, não de escolha.")
I("Se isso é você", "o vão é frágil",
  "Se isso é o seu caso, o seu número de dias úteis é frágil. Ele depende do "
  "trajeto, e não de um hábito.")
I("Teste fácil", "um feriado no meio",
  "Tem um teste simples: olhe um feriado que caiu no meio da semana. Se "
  "aquele dia se parece com sábado, a resposta apareceu.")
I("E quem trabalha de casa", "vê o contrário",
  "Quem trabalha de casa costuma ver o contrário: a semana é o lado parado, e "
  "o fim de semana é quando o corpo sai.")
I("Tem um terceiro caso", "o fim de semana cheio",
  "E tem um terceiro caso: quem tem o fim de semana ocupado com casa, "
  "criança e obrigação. Aí o número do sábado pode ser alto sem nada disso "
  "ter sido exercício.")
I("A contagem não distingue", "e você distingue",
  "A contagem não sabe a diferença entre andar por prazer e andar carregando "
  "sacola. Você sabe, e essa leitura é sua.")
I("Por isso o número não decide sozinho", "ele abre a pergunta",
  "Por isso o número não decide nada sozinho. Ele abre a pergunta certa, que "
  "é: esse movimento está vindo de onde?")
I("Nenhum dos dois é erro", "são padrões diferentes",
  "Nenhum dos dois é errado. São padrões diferentes, e cada um pede uma coisa "
  "diferente. O que não vale é achar que sabe qual é o seu sem ter olhado.")

# -------------------------------------------------------------------- cap 7
T("De um fim de semana", "para o ano",
  "Agora o passo que faz o tamanho aparecer.",
  cap="De um fim de semana para o ano")
I("Um sábado", "parece pouco",
  "A diferença de um sábado parece pequena. É pequena mesmo, e é por isso que "
  "ela passa despercebida toda semana.")
I("Multiplique", "por dois dias",
  "Multiplique o vão pelos dois dias do fim de semana. Depois pelas cinquenta "
  "e duas semanas do ano.")
I("Agora ele tem tamanho", "e sinal",
  "Agora aquele número pequeno tem tamanho, e tem sinal. E o sinal é o que "
  "diz onde está a alavanca da sua semana.")
I("Compare com algo", "que você conhece",
  "Para sentir o tamanho, compare com alguma coisa que você conhece: quantos "
  "dias inteiros de movimento aquilo dá no ano.")
I("E pode dar quase zero", "isso também é resposta",
  "Pode dar quase zero, e a sua semana ser parelha. Essa é uma resposta "
  "completa, e agora ela é medida em vez de suposta.")
I("E olhe o sinal antes do tamanho",  "ele diz onde mexer",
  "Antes do tamanho, olhe o sinal. Ele diz de que lado da semana está a "
  "alavanca, e é isso que muda o que você faria.")
I("Se o vão é positivo", "o sábado é o alvo",
  "Vão positivo quer dizer que o fim de semana é o lado parado. Então é lá "
  "que uma mudança pequena rende mais.")
I("Se é negativo", "a semana é o alvo",
  "Vão negativo quer dizer o contrário: os dias úteis é que estão parados, e "
  "aí o alvo é o meio da semana, não o sábado.")
I("O bom disso", "o fim de semana volta",
  "O lado bom é que o fim de semana volta em poucos dias, e volta inteiro. "
  "Um mês ruim não obriga o seguinte.")

# -------------------------------------------------------------------- cap 8
T("O que fazer hoje", "três passos",
  "Fechamos com o que dá pra fazer hoje, em três passos.",
  cap="O que fazer hoje")
L("Três passos",
  ["Abra o histórico", "Separe úteis e fim de semana", "Subtraia as médias"],
  "Primeiro: abra o histórico do seu celular nas últimas quatro semanas. "
  "Segundo: separe os dias úteis do fim de semana. Terceiro: subtraia uma "
  "média da outra.")
I("Faça uma vez", "não vire rotina",
  "Faça uma vez só. Isso não é para virar planilha semanal, é para você "
  "saber onde está o seu vão.")
I("Se o vão for grande", "mexa em um dia",
  "Se o vão for grande, mexa em um dia só, o que for mais fácil. Mudar o fim "
  "de semana inteiro de uma vez raramente dura.")
I("E refaça em um mês", "só uma vez",
  "Refaça a conta daqui a um mês, uma vez, para ver se o número andou. Não "
  "antes: quatro semanas é o mínimo para não ler ruído.")
I("Um aviso", "se houver orientação médica",
  "E um aviso que precisa estar aqui: se você tem alguma condição de saúde ou "
  "orientação médica sobre atividade física, ela vale mais do que qualquer "
  "conta deste vídeo.")
# EXPERIMENTO 26 — o pedido do longo tambem fecha em conta, nao em clique.
I("E guarde o número", "pra comparar depois",
  "Guarde o número num lugar que você reencontre. Sem ele, daqui a um mês "
  "você vai comparar com a lembrança, e a lembrança sempre perde.")
C("Escreva o seu número", "nos comentários",
  "Se você fizer a conta, escreve aqui embaixo só uma coisa: o vão, com o "
  "sinal. Sem peso, sem meta, sem nome de aplicativo. Quero ver o quanto isso "
  "varia entre quem tem rotina parecida.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26, terceiro pacote. O short entrega a subtracao FECHADA e gasta
# o pedido na INSCRICAO, amarrada ao metodo. Nao aponta para o longo.

SHORT = [
    {"layout": "titulo", "kicker": "Seu celular já contou",
     "sub": "faça essa conta agora",
     "nar": "O seu celular já contou quanto você se move há meses. Faz essa "
            "conta agora.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Número um", "sub": "média de segunda a sexta",
     "nar": "Número um: a média dos seus dias úteis nas últimas quatro "
            "semanas. Passos ou minutos ativos, escolha um.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Número dois", "sub": "média do fim de semana",
     "nar": "Número dois: a média de sábado e domingo, nas mesmas quatro "
            "semanas.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Subtraia", "sub": "esse é o seu vão",
     "nar": "Subtraia o segundo do primeiro. Positivo: você cai no fim de "
            "semana. Negativo: a semana é que está parada. A conta é essa.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Se serviu",
     "sub": "se inscreve — uma conta por semana",
     "nar": "Se essa conta serviu, se inscreve. Uma conta por semana, feita "
            "com os seus próprios números.", "sem_cap": True},
]

THUMB = {"l1": "Semana ou", "l2": "fim de semana"}

COPY = """# O vão entre a sua semana e o seu fim de semana, com o histórico que já está no seu celular

## TITULO
Semana ou Fim de Semana? A Conta que o Seu Celular Já Fez por Você

## DESCRICAO
O seu celular vem contando quanto você se move há meses, e provavelmente você nunca olhou esses números do jeito que muda alguma coisa. Este vídeo não é sobre bater meta nenhuma — é sobre enxergar o seu padrão, que é uma pergunta diferente e bem mais útil. E tem prazo curto: o próximo fim de semana chega em poucos dias.

Não há um único número meu neste vídeo. Não há meta de passos, não há minutos recomendados, não há caloria, não há peso, e não há nome de aplicativo ou de aparelho. Os dois números da conta saem do histórico que já está gravado no seu celular. Você não precisa instalar nada, comprar nada nem começar nada.

A conta são duas médias e uma subtração. Some os cinco dias úteis de cada semana e divida por cinco; some sábado e domingo e divida por dois. Faça isso nas últimas quatro semanas — não na última, porque uma semana isolada quase sempre teve alguma coisa fora do normal. Depois subtraia a segunda média da primeira. Se der positivo, você se move menos no fim de semana, e agora você sabe de quanto. Se der negativo, é o contrário: o fim de semana é onde você se move mais e a semana é que está parada.

Pode ser passos ou minutos ativos, desde que seja o mesmo nos dois lados. Misturar as duas unidades inventa uma diferença que não existe, e é o erro mais comum aqui.

Um capítulo mostra onde achar os números — a visão por semana do aplicativo de saúde, e o que fazer quando falta um dia (pular a semana inteira em vez de inventar o dia). Outro capítulo diz o que a conta NÃO pega, porque é mais honesto do que fingir: a intensidade não aparece na contagem de passos; bicicleta, natação e musculação quase não aparecem e mesmo assim aconteceram; e descansar é legítimo — um vão pequeno pode ser exatamente o que o seu corpo precisava. Esta conta não diz que você deveria estar fazendo mais. Ela mostra o tamanho de uma diferença que você não estava vendo.

E há o caso que engana: muita gente descobre que quase todo o movimento da semana vem do deslocamento, não de escolha — e nesse caso o número dos dias úteis é frágil, porque depende do trajeto e não de um hábito. O teste é olhar um feriado que caiu no meio da semana.

AVISO: este vídeo não prescreve exercício, não diz quanto ninguém deve se mexer, não promete emagrecimento e não é aconselhamento médico. Se você tem alguma condição de saúde ou orientação médica sobre atividade física, ela vale mais do que qualquer conta daqui.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz essa conta com o teu histórico e escreve aqui só uma coisa: o vão, com o sinal. Sem peso, sem meta, sem nome de aplicativo, só o número. Quero ver o quanto isso varia entre quem tem rotina parecida.

## HASHTAGS
#Saúde #AtividadeFísica #SejaMaisMagra

## TAGS
contagem de passos, minutos ativos, aplicativo de saude, historico do celular, media de passos, fim de semana sedentario, rotina de movimento, atividade fisica no dia a dia, quantos passos eu dou, monitorar movimento, habito de caminhar, saude e rotina, medir atividade, passos por dia, calcular sozinho

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita meta de passos, nao cita minutos recomendados, nao cita caloria, nao cita peso, nao cita indice e nao cita nome de aplicativo nem de aparelho. Os dois numeros da conta saem do historico do proprio espectador, no celular ou no relogio dele. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da idade, do peso ou da condicao dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer meta ou faixa recomendada. Elas variam por idade e por condicao de saude, e citar uma so delas transformaria uma conta descritiva numa prescricao — que e exatamente o que este video nao e. O video tambem nao prescreve exercicio, nao diz quanto ninguem deve se mexer, nao promete emagrecimento, nao fala de dieta e nao e aconselhamento medico; ha aviso explicito no roteiro de que orientacao medica individual vale mais do que qualquer conta daqui.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seja-mais-magra-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-008",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#22303C", "c1": "#3E7C8A", "c2": "#E0A458", "bg": "#F6F3EE"},
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
    grava(SPEC, "fabrica/specs/seja-mais-magra-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
