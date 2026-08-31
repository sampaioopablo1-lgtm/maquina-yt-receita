#!/usr/bin/env python3
"""Monta a spec labtreinamento-007.

ALAVANCA ATACADA: **A — conversao short -> inscrito, pela FORMA.** E desta vez
o canal isolou a variavel sozinho.

NUMERO DE PARTIDA, medido em 31/08/2026 (`v_maquina_licoes` + `metricas`):

    labtreinamento .... 6 shorts medidos, 6 longos medidos
                        short: mediana 1,13 views/dia, TOPO 249,31
                        longo: mediana 0,41 views/dia
                        veredito: `suspenso`
                        1.210 views totais no canal

O QUE DEU CERTO — e por muito: o pacote `labtreinamento-006`, "INSS do
Autonomo: 11% ou 20%?". O short dele tem MIL E NOVENTA E SETE views, contra
uma mediana de canal de vinte e uma. O longo dele tem TRINTA E DUAS views,
cinco vezes o segundo colocado do canal (NR-10, quinze views). E o unico
pacote do canal que e ESCOLHA do espectador, com o numero na guia DELE.

O QUE NAO DEU — e aqui esta a licao cara: **esse short converteu ZERO
inscritos com mil e noventa e sete views**. E da para dizer por que, porque o
roteiro dele esta gravado. Ele entrega a escolha e a consequencia, e depois
diz: "quanto isso da com a sua guia esta no video completo aqui embaixo". Ou
seja, ele SEGUROU a conta. A rotina ja mandava o contrario — "o SHORT tambem
entrega a conta, nao so a manchete" — e o pacote 006 nao obedeceu.

Isso e o experimento que faltava para o aprendizado 482. Ate hoje a evidencia
era "pacote menos visto converteu mais". Agora ha um caso com a MESMA forma
(escolha binaria, segunda pessoa, dinheiro do espectador), com o MAIOR alcance
do canal, e conversao zero. A unica coisa que ele nao fez foi entregar a conta.
Alcance nao converte; a conta fechada e que converte. (Aprendizado 539.)

E o resto do canal confirma o negativo pelo outro lado: os tres pacotes
"[EXCEL] Planilha..." somam quinze views de longo e quarenta e uma de short, e
os de norma — NR-1, NR-10, FAP — sao fato sobre o mundo com prazo
institucional. Nenhum deles e conta que o espectador faca em si mesmo.

O QUE MUDO POR CAUSA DISSO, e e uma coisa so: **o short entrega a subtracao
inteira e fecha**. O que fica para o longo nao e o numero — e onde achar as
horas, o que a conta nao pega, e quando ela engana. O canal para de publicar
planilha e norma.

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `suspenso` => PISO de oito minutos. Oito capitulos, porque `copy_md`
so abre capitulo sessenta segundos depois do anterior.

A RESPOSTA fecha no capitulo 3, e desta vez com MARGEM: o aprendizado 537,
medido hoje nos dois pacotes anteriores, mostra que a estimativa chega curta
justamente no ponto dos duzentos segundos — errou 5,3% e 7,1%, sempre para
menos, e os dois pacotes passaram no portao e fecharam a resposta FORA dos
duzentos segundos no video publicado. Aqui a resposta e dimensionada para
fechar ate ~185s NA ESTIMATIVA, e o tempo real vai ser conferido no copy.md
renderizado antes de publicar.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **por hora ou por projeto — o que o ultimo orcamento pagou de
verdade pela sua hora**. Os eixos ja publicados no canal sao INSS do autonomo,
FAP, NR-10, NR-1, ISO 9001 e planilhas. Precificacao do proprio trabalho nunca
foi ao ar aqui.

A FORMA e a do unico pacote que funcionou no proprio canal: "X ou Y? A escolha
em <lugar concreto> que decide <consequencia>". Assunto NAO copiado — aquele e
previdencia, este e preco do proprio trabalho.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele recebeu no ultimo projeto e as horas que ele
   mesmo gastou;
2. e ESCOLHA COM PRAZO — o proximo orcamento, que ele vai mandar;
3. o SHORT entrega a conta — divisao fechada, com o numero, sem empurrar para
   o longo. Esta e a correcao da rodada.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita valor de hora, nao cita piso de categoria, nao cita
tabela de honorarios e nao cita nenhuma profissao especifica como referencia de
preco. Os dois numeros da conta sao do proprio espectador: o valor que ele
recebeu no ultimo projeto e as horas que ele gastou nele. Nao ha numero meu
para certificar em duas fontes, e por isso nao ha numero meu que possa
envelhecer nem que dependa da area dele.

O QUE O VIDEO NAO FAZ: nao diz quanto ninguem deve cobrar, nao recomenda
cobrar por hora nem por projeto, nao promete aumento e nao e aconselhamento
financeiro nem juridico.
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
T("Você mandou um preço", "e nunca conferiu depois",
  "Você mandou um preço para o último trabalho que fez. Fechou, entregou, "
  "recebeu. E provavelmente nunca voltou para conferir o que aquele preço "
  "pagou de verdade pela sua hora.",
  cap="O preço que você mandou")
I("Não é sobre cobrar caro", "é sobre saber",
  "Isso não é uma conversa sobre cobrar caro. É sobre saber quanto você "
  "recebeu por hora, o que é uma pergunta diferente e bem mais útil. Dá para "
  "responder ela sem decidir nada, e é melhor assim.")
I("E é escolha sua", "com prazo",
  "E é uma escolha que volta com prazo: o próximo orçamento que você vai "
  "mandar. Não é semana que vem em tese, é o próximo.")
I("Os dois números", "já existem",
  "Os dois números de que você precisa já existem, e os dois são seus. Um "
  "está no que você recebeu. O outro está no tempo que você gastou.")
I("Um deles é fácil", "o outro incomoda",
  "O primeiro é fácil de achar. O segundo é o que quase ninguém junta, e é "
  "justamente ele que muda a resposta.")
I("O que vem agora", "uma divisão",
  "Em alguns minutos você faz essa conta sozinho. É uma divisão, com números "
  "que você já tem, sem planilha nova e sem esperar o mês fechar. E ela "
  "responde uma pergunta só, mas responde de verdade.")

# -------------------------------------------------------------------- cap 2
T("Os dois lados", "o que entrou e o que saiu de você",
  "A conta tem dois lados, e o erro mais comum é olhar só para o primeiro.",
  cap="Os dois lados da conta")
I("Lado um", "o valor recebido",
  "O primeiro lado é o valor que entrou pelo trabalho. Líquido, depois do que "
  "você paga de imposto e de taxa da plataforma, se houver. Use o que sobrou "
  "na sua conta, não o que estava escrito no orçamento.")
I("Lado dois", "as horas de verdade",
  "O segundo lado são as horas. E aqui a palavra que importa é: todas.")
I("Não só a execução", "tudo que o trabalho puxou",
  "Não só o tempo sentado fazendo a entrega. Todo o tempo que aquele trabalho "
  "puxou, do primeiro contato até o último ajuste.")
I("As reuniões", "contam",
  "As reuniões contam. As trocas de mensagem que interromperam outra coisa "
  "contam, e contam com o tempo que você levou para voltar ao que estava "
  "fazendo. O deslocamento conta.")
I("As revisões", "principalmente elas",
  "As revisões contam, principalmente as que vieram depois de você achar que "
  "tinha acabado.")
I("E a proposta", "mesmo não paga",
  "E o tempo que você gastou montando a proposta conta também, porque ele só "
  "existiu por causa desse trabalho.")
I("Agora dá pra dividir", "os dois seus",
  "Com esses dois lados na mão, a conta deixa de ser opinião sobre preço e "
  "vira aritmética sobre o seu tempo.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — com margem, por causa do aprendizado 537.
T("A conta", "uma divisão",
  "Então a conta. Uma divisão, e uma comparação.",
  cap="A conta: uma divisão")
I("Divida", "recebido pelas horas",
  "Divida o valor líquido que você recebeu pelo total de horas que o trabalho "
  "consumiu. O resultado é a sua hora real naquele projeto. Não é a hora que "
  "você planejou, não é a que está na sua proposta: é a que aconteceu.")
I("Agora compare", "com a que você diz",
  "Agora compare com o valor de hora que você diz que cobra, ou que você "
  "imaginava estar recebendo. Se nunca pensou nisso, use o que acharia justo "
  "receber por uma hora sua.")
I("Se a real for maior", "o preço estava bom",
  "Se a hora real for maior, aquele preço estava bom para você, e vale saber "
  "por quê antes de mudar qualquer coisa.")
I("Se for menor", "essa é a diferença",
  "Se for menor, a diferença entre as duas é exatamente o que aquele projeto "
  "te custou sem aparecer no preço. E multiplicada pelas horas, ela vira o "
  "valor que ficou de fora do orçamento.")
I("E isso responde", "a pergunta do título",
  "E é isso que decide se, para você, cobrar por projeto está funcionando ou "
  "está escondendo horas.")
I("A conta acabou aqui", "o resto é o porquê",
  "A conta acabou aqui, e você já pode fazer a sua. O resto do vídeo é onde "
  "achar as horas, o que a conta não pega e quando ela engana.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Onde achar as horas", "sem ter anotado",
  "O problema prático é que quase ninguém anotou as horas. Dá para "
  "reconstruir, e com boa precisão.",
  cap="Onde achar as horas")
I("A agenda", "as reuniões estão lá",
  "Comece pela agenda: as reuniões daquele período estão marcadas, com "
  "duração. E some também os quinze minutos antes de cada uma, que você gastou "
  "se preparando, e os quinze depois, que você levou para voltar ao que "
  "estava fazendo.")
I("O histórico de mensagens", "tem hora",
  "Depois o histórico de mensagens ou de e-mail. As trocas têm data e hora, e "
  "elas desenham o período em que o trabalho ocupou espaço na sua cabeça.")
I("Os arquivos", "guardam a data",
  "Os arquivos que você entregou guardam a data de criação e a de modificação. "
  "Cada versão nova é uma revisão que aconteceu.")
I("Some por dia", "não por tarefa",
  "Some por dia, e não por tarefa: é mais fácil lembrar que uma terça inteira "
  "foi embora naquilo do que reconstruir cada bloco.")
I("Erre para menos", "e ainda assim",
  "E na dúvida, erre para menos. Se a conta já incomoda com uma estimativa "
  "conservadora, ela incomoda de verdade.")
I("Do próximo em diante", "anote",
  "Do próximo trabalho em diante, anote enquanto acontece. Uma linha por dia "
  "basta, e ela transforma essa conta em coisa de dois minutos.")

# -------------------------------------------------------------------- cap 5
T("O que a conta não pega", "e é justo dizer",
  "Tem coisas que essa conta não captura, e é mais honesto dizer do que fingir "
  "que ela decide tudo.",
  cap="O que a conta não pega")
I("O aprendizado", "vale, e não entra",
  "A primeira: o que você aprendeu ali. Um trabalho que pagou mal e te deixou "
  "sabendo fazer uma coisa nova não foi só prejuízo.")
I("Mas cuidado", "isso não se repete",
  "Cuidado com essa, porém: aprendizado acontece uma vez. Se o mesmo tipo de "
  "trabalho já se repetiu três vezes, o argumento acabou.")
I("O portfólio", "e o cliente que apresenta",
  "A segunda: portfólio e apresentação. Um trabalho que abre porta tem valor "
  "que não está no preço dele, e às vezes vale mais do que o projeto inteiro.")
I("Também tem prazo", "portas fecham",
  "Mas essa também vence. Se a porta não abriu em alguns meses, ela não vai "
  "abrir por causa daquele projeto.")
I("O terceiro", "a paz",
  "A terceira não tem número: um cliente que não gera retrabalho vale mais por "
  "hora do que a conta mostra, e um que gera vale menos. E essa é a única das "
  "três que não vence com o tempo — ela se repete em todo projeto que você "
  "fizer com a mesma pessoa.")
I("Junte isso", "depois da divisão",
  "Junte tudo isso DEPOIS de fazer a divisão, nunca antes. Se vier antes, "
  "vira desculpa para não olhar o número.")

# -------------------------------------------------------------------- cap 6
T("O caso que engana", "o projeto grande",
  "Agora o caso que engana quase todo mundo, e ele merece um capítulo.",
  cap="O caso que engana")
I("O projeto grande", "parece o melhor",
  "O trabalho de maior valor costuma parecer o melhor do ano, porque o número "
  "que entrou foi o maior, e porque é dele que você lembra quando alguém "
  "pergunta como foi o ano.")
I("Mas ele também", "consumiu mais",
  "Só que ele também foi o que mais consumiu tempo, e muitas vezes o que mais "
  "gerou revisão e reunião.")
I("Faça a divisão nele", "e no menor",
  "Faça a divisão nos dois: no maior trabalho do ano e no menor. Não é raro a "
  "ordem se inverter.")
I("Se inverteu", "não é sobre tamanho",
  "Se inverteu, o que você descobriu não é que projeto grande é ruim. É que o "
  "preço dele foi feito olhando o tamanho, e não as horas.")
I("E o contrário existe", "o pequeno que sangra",
  "O contrário também aparece: o trabalho pequeno, de preço simbólico, que "
  "consumiu um mês em pedaços. Esse é o que costuma doer mais, porque ele "
  "nunca ocupou um dia inteiro e por isso nunca pareceu grande o bastante "
  "para você reclamar dele.")
I("As duas formas servem", "depende do seu número",
  "Cobrar por hora e cobrar por projeto são as duas legítimas, e nenhuma é a "
  "certa em geral. A certa é a que o seu número apontar. O que não vale é "
  "mandar preço por hábito e nunca ter conferido.")

# -------------------------------------------------------------------- cap 7
T("De um projeto", "para o ano",
  "Agora o passo que muda a percepção do tamanho.",
  cap="De um projeto para o ano")
I("Um projeto", "parece pouco",
  "A diferença em um projeto costuma parecer pequena, seja ela a favor ou "
  "contra. É pequena mesmo, e é por isso que ela passa batida todas as vezes.")
I("Faça em três", "os últimos três",
  "Faça a mesma divisão nos três últimos trabalhos que você entregou. Três já "
  "mostram se é padrão ou se foi um caso.")
I("Se os três apontam igual", "é o seu preço",
  "Se os três apontam para o mesmo lado, isso não é azar: é o jeito como você "
  "monta preço, e ele se repete no próximo.")
I("Multiplique", "pelos trabalhos do ano",
  "Multiplique a diferença média pelo número de trabalhos que você entrega num "
  "ano. É o mesmo comportamento, acumulado.")
I("Compare com algo", "que você conhece",
  "Para sentir o tamanho, compare com algo que você conhece. Com o valor de um "
  "projeto inteiro, por exemplo. Se a diferença acumulada no ano equivale a um "
  "projeto que você entregou de graça, isso diz uma coisa. Se equivale a uma "
  "tarde de trabalho, diz outra bem diferente, e você pode parar de se "
  "preocupar com isso.")
I("O bom disso", "o próximo orçamento",
  "O lado bom é que a decisão volta no próximo orçamento, e volta inteira. Um "
  "projeto mal precificado não obriga o seguinte.")

# -------------------------------------------------------------------- cap 8
T("O que fazer hoje", "três passos",
  "Fechamos com o que dá pra fazer hoje, em três passos.",
  cap="O que fazer hoje")
L("Três passos",
  ["Pegue o último projeto", "Some todas as horas", "Divida o líquido"],
  "Primeiro: pegue o último trabalho que você entregou e recebeu. Segundo: "
  "some todas as horas que ele consumiu, inclusive proposta, reunião e "
  "revisão. Terceiro: divida o valor líquido pelas horas.")
I("Compare", "com o que você diz cobrar",
  "Compare o resultado com o valor de hora que você diz cobrar. A diferença "
  "entre os dois é a conta inteira, e ela cabe numa linha do seu caderno.")
I("Se doer", "não mude o preço ainda",
  "Se o número doer, resista a mudar o preço na hora. Faça nos três últimos "
  "primeiro, para saber se é padrão ou se foi um projeto específico. Um "
  "número ruim sozinho não é padrão, é um caso.")
I("E depois", "mude uma coisa só",
  "E quando mudar, mude uma coisa só: ou o preço, ou o que está incluído. "
  "Mudar as duas ao mesmo tempo tira de você a chance de saber qual funcionou.")
C("Escreva o seu número", "nos comentários",
  "Se você fizer a conta, escreve aqui embaixo só uma coisa: se a sua hora "
  "real ficou acima ou abaixo da que você diz cobrar, e por quanto. Sem nome "
  "de cliente e sem valor de projeto. Quero ver o quanto isso se espalha.")

# =============================== O SHORT =====================================
# A CORRECAO DA RODADA: o short entrega a divisao FECHADA, com o resultado.
# O pacote 006 segurou a conta ("esta no video completo") e converteu zero com
# 1.097 views. O que fica para o longo aqui e o porque, nao o numero.

SHORT = [
    {"layout": "titulo", "kicker": "Seu último projeto",
     "sub": "quanto pagou por hora?",
     "nar": "O último trabalho que você entregou: quanto ele pagou pela sua "
            "hora de verdade?", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pegue o líquido", "sub": "o que sobrou",
     "nar": "Pegue o valor que sobrou depois de imposto e taxa.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Some as horas", "sub": "todas elas",
     "nar": "Some todas as horas: execução, reuniões, deslocamento, revisões "
            "e o tempo que você gastou montando a proposta.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Divida", "sub": "essa é sua hora real",
     "nar": "Divida um pelo outro. Esse é o valor real da sua hora naquele "
            "projeto.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Compare", "sub": "com a que você diz",
     "nar": "Compare com a hora que você diz que cobra. A diferença entre as "
            "duas é o que aquele projeto te custou sem aparecer no preço. A "
            "conta é essa, e ela já está pronta.", "sem_cap": True},
    {"layout": "cta", "kicker": "Quando ela engana",
     "sub": "está no vídeo completo",
     "nar": "Quando essa conta engana, e onde achar as horas que você não "
            "anotou, está no vídeo completo aqui embaixo.", "sem_cap": True},
]

THUMB = {"l1": "Por hora", "l2": "ou projeto"}

COPY = """# A hora real do seu último projeto, calculada com os seus dois números

## TITULO
Por Hora ou por Projeto? A Conta no Seu Último Orçamento Que Decide o Próximo

## DESCRICAO
Você mandou um preço para o último trabalho que fez. Fechou, entregou, recebeu — e provavelmente nunca voltou para conferir o que aquele preço pagou de verdade pela sua hora. Este vídeo não é sobre cobrar caro. É sobre saber quanto você recebeu por hora, que é uma pergunta diferente e bem mais útil, e é uma escolha que volta com prazo: o próximo orçamento que você vai mandar.

Nenhum número deste vídeo é meu. Não há valor de hora, não há piso de categoria, não há tabela de honorários e não há nenhuma profissão usada como referência de preço. Os dois números da conta são seus, e os dois já existem: o valor líquido que entrou pelo trabalho e as horas que ele consumiu.

A conta é uma divisão. Pegue o valor que sobrou depois de imposto e de taxa de plataforma, some TODAS as horas que o trabalho puxou — execução, reuniões, trocas de mensagem que interromperam outra coisa, deslocamento, revisões, e o tempo que você gastou montando a proposta — e divida um pelo outro. O resultado é a sua hora real naquele projeto. Compare com o valor de hora que você diz que cobra: a diferença entre os dois é exatamente o que aquele projeto te custou sem aparecer no preço.

Há um capítulo sobre onde achar as horas que você não anotou: a agenda guarda as reuniões com duração, o histórico de mensagens guarda data e hora das trocas, e os arquivos entregues guardam a data de cada versão — cada versão nova é uma revisão que aconteceu. Some por dia, não por tarefa, e na dúvida erre para menos.

Há um capítulo sobre o que a conta NÃO pega, porque é mais honesto dizer: o que você aprendeu ali, o portfólio e a porta que o trabalho abre, e a paz de um cliente que não gera retrabalho. Os dois primeiros vencem — aprendizado acontece uma vez, e porta que não abriu em alguns meses não vai abrir. E todos eles entram DEPOIS da divisão, nunca antes.

E há o caso que engana: o projeto de maior valor costuma parecer o melhor do ano porque o número que entrou foi o maior, mas foi também o que mais consumiu tempo e gerou revisão. Faça a divisão no maior e no menor trabalho do ano — não é raro a ordem se inverter.

O fechamento são três passos para hoje, com o número que já está no seu histórico.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz essa conta com o teu último projeto e escreve aqui só uma coisa: se a tua hora real ficou acima ou abaixo da que tu diz cobrar, e por quanto. Sem nome de cliente e sem valor de projeto, só a diferença. Quero ver o quanto isso se espalha entre quem trabalha na mesma área.

## HASHTAGS
#Autônomo #Freelancer #LabTreinamento

## TAGS
valor da hora, cobrar por hora ou por projeto, precificacao freelancer, quanto cobrar, orcamento de projeto, hora tecnica, autonomo, freelancer, precificar servico, calcular valor hora, controle de horas, retrabalho, revisao de projeto, carreira tecnica, gestao do tempo

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita valor de hora, nao cita piso de categoria, nao cita tabela de honorarios, nao cita nenhuma profissao como referencia de preco e nao compara areas entre si. Os dois numeros da conta sao do proprio espectador: o valor liquido que ele recebeu esta no extrato ou na nota dele, e as horas saem da agenda, do historico de mensagens e da data dos arquivos que ele mesmo entregou. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da area dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer valor de referencia de hora ou de projeto. Esses valores mudam por area, por regiao, por senioridade e por data, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao diz que cobrar por hora e melhor que cobrar por projeto — as duas respostas sao legitimas e dependem do numero de cada um —, nao promete aumento de preco e nao e aconselhamento financeiro nem juridico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/labtreinamento-007.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-007",
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
    grava(SPEC, "fabrica/specs/labtreinamento-007.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
