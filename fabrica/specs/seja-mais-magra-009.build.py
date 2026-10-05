"""seja-mais-magra-009 — a faixa de ruido da propria balanca.

ALAVANCA ATACADA: A (conversao short -> inscrito), e o numero de partida sai
do PROPRIO canal, nao da media da frota.

O NUMERO DE PARTIDA. Oito pacotes publicados, 164 views de canal, zero
inscritos. Mas os shorts nao sao todos iguais, e a diferenca dentro do canal
reproduz o aprendizado 482 linha por linha:

    006  tabela nutricional, qual coluna comparar .......... 45 views
    007  atividade fisica, as duas faixas oficiais ......... 40 views
    002  Ozempic e Mounjaro, o que voce reganha ............ 32 views
    003  proteina, a conta por grama ....................... 19 views
    008  semana ou fim de semana ...........................  4 views
    005  semaglutida generica aprovada .....................  2 views
    001  Anvisa proibiu tres produtos ......................  1 view
    004  cento e oitenta e nove alegacoes permitidas .......  1 view

Os quatro de cima entregam um METODO que a pessoa aplica nos numeros DELA:
qual coluna olhar, em qual das duas faixas ela esta, o que ela reganha, quanto
custa por grama. Os quatro de baixo entregam FATO sobre o mundo: o que a Anvisa
proibiu, o que foi registrado, quantas alegacoes existem. Quarenta e cinco
contra um, e o assunto dos dois e rotulo. Nao e o tema que separa: e a forma.

O QUE DEU CERTO: metodo aplicavel ao extrato/rotulo do espectador — 006 e 007
somam 85 das 164 views do canal, em dois dos oito pacotes.
O QUE NAO DEU: abrir com numero institucional. 001, 004 e 005 abrem com um
numero da Anvisa e somam 4 views em tres pacotes.
O QUE VOU MUDAR: zero numero institucional neste pacote, por desenho, e o
unico numero que decide e medido pelo espectador na balanca da casa dele.

EIXO, e por que ele e novo. Os oito pacotes anteriores falam de PRODUTO
(Ozempic, shake, proteina, generico), de ROTULO (tabela, alegacoes) e de
ATIVIDADE (faixas, semana). Nenhum fala do INSTRUMENTO. Este fala: a balanca
varia sozinha, essa variacao tem um tamanho, o tamanho e diferente em cada
pessoa, e qualquer leitura menor que ele nao e noticia. A decisao com prazo que
o longo responde: no fim desta semana, mudo algo ou nao mudo?

TITULO, modelando a ESTRUTURA do outlier e nao o assunto. O 007 — segundo
melhor short do canal — tem a forma "<coisa>: <o metodo>, e Por Que <a
consequencia contraintuitiva>". A forma fica; o assunto muda. Similaridade
maxima medida contra o corpus de cento e quarenta titulos: zero virgula
quatrocentos e trinta e tres, contra o proprio 007. Dentro do teto de zero
virgula sessenta e cinco, e a semelhanca que sobrou e a estrutura, de proposito
— tirei a palavra "faixa" do titulo justamente para que a estrutura se repita
sem que o video pareca o mesmo.

VEREDITO: `canal frio` (v_maquina_licoes, 04/10/2026). Logo, eixo novo e piso
de oito minutos por analogia com `suspenso`. Alavanca B manda ir ao PISO da
faixa, e o piso real aqui nao e 480 s: com oito capitulos e o
`prontidao.MARGEM_CAP`, o minimo aritmetico ja e 8 x 64,2 = 514 s. Entao o
alvo e logo acima disso, e a resposta fecha DENTRO dos primeiros duzentos
segundos — nao na abertura do capitulo 4, que o aprendizado 537 mediu errando
em mais de quarenta segundos.

TITULO PROPRIO DO SHORT: tem. Sete dos oito pacotes deste canal mandaram o
short herdar o titulo do longo (001 foi o unico com titulo proprio), e e o
defeito do aprendizado 548 com nome e sobrenome. Trinta e dois caracteres.
"""

import json

CENAS = []

# Links resolvidos em 05/10/2026, e a busca rodou DENTRO do Postgres por
# `pg_net`: `net.http_get` para api.pexels.com com a chave lida do `config` na
# mesma consulta. Assim a chave nao atravessa nem a sandbox nem o chat, do
# mesmo jeito que o access_token do YouTube. No runner a busca nao roda —
# `api.pexels.com` da TimeoutError em 7 de 7 cenas pela faixa de IP dele.
# Com o link gravado o pacote fica reproduzivel: sem ele, dois renders da mesma
# spec pegam clipes diferentes, porque a busca reordena.
BROLL = {
    7801722: ("https://videos.pexels.com/video-files/7801722/7801722-hd_1366_576_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/a-person-weighing-using-a-weighing-scale-7801722/"),
    8554345: ("https://videos.pexels.com/video-files/8554345/8554345-hd_1280_720_25fps.mp4",
              "TP Motion",
              "https://www.pexels.com/video/filling-up-a-glass-with-water-8554345/"),
    5466772: ("https://videos.pexels.com/video-files/5466772/5466772-hd_1280_720_25fps.mp4",
              "olia danilevich",
              "https://www.pexels.com/video/using-a-calculator-and-writing-5466772/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================= OS PRIMEIROS DUZENTOS SEGUNDOS ======================

# -------------------------------------------------------------------- cap 1
T("Dois números diferentes", "no mesmo mostrador",
  "Existe o número que a balança mostra e existe o quanto o seu corpo "
  "mudou. Não são a mesma coisa, e a diferença tem tamanho.",
  cap="O número e a mudança não são a mesma coisa")
T("Ninguém está errado", "a balança está certa",
  "A balança não está quebrada e você não está se enganando. Ela pesa, com "
  "precisão, tudo que está em cima dela naquele segundo.")
T("E o que está em cima", "muda o dia inteiro",
  "Mas o que está em cima dela às sete da manhã e diferente do que está às "
  "sete da noite, sem uma célula de gordura ter entrado ou saido.")
B("Mesma pessoa", "duas horas de diferença",
  "A mesma pessoa, no mesmo dia, pode marcar valores que diferem em quase um "
  "quilo. Nenhum dos dois está errado.",
  "person stepping on a bathroom scale at home", 7801722)
T("O que isso custa", "em decisão, não em quilo",
  "Isso custa decisão. A pessoa pesa num dia ruim e muda o plano inteiro por "
  "causa de um número que ia voltar sozinho.")
T("Não e força de vontade", "e leitura de instrumento",
  "Isso não é falta de disciplina. É ler um instrumento sem saber a margem "
  "dele, que é um erro técnico e tem conserto técnico.")
T("Nenhum número meu", "nenhuma média nacional",
  "Não tem um número meu nesta conta. Nenhuma média, nenhum percentual "
  "recomendado. O número que decide sai da sua casa.")
T("O prazo é seu também", "a próxima pesagem",
  "O prazo também e seu: a próxima vez que você subir na balança. Ela vai "
  "mostrar um número, e você vai ter de decidir se aquilo significa algo.")

# -------------------------------------------------------------------- cap 2
T("O que mexe sozinho", "quatro coisas, nenhuma e gordura",
  "Quatro coisas mexem no mostrador sem mexer no corpo. Vale conhecer as "
  "quatro, porque são elas que formam o tamanho que vamos medir.",
  cap="O que faz o número andar sem nada mudar")
B("A primeira", "água",
  "A primeira é água. O corpo carrega litros dela e troca essa quantidade "
  "durante o dia, conforme você bebe, transpira e dorme.",
  "pouring water into a glass", 8554345)
T("A segunda", "o que ainda está passando",
  "A segunda é a comida que ainda está no caminho: o que você comeu ontem "
  "pesa hoje, e vai deixar de pesar sem ter virado nada.")
T("A terceira", "sal e carboidrato",
  "A terceira é sal e carboidrato, que fazem o corpo segurar mais água por "
  "um ou dois dias. Uma refeição mais salgada aparece no mostrador depois.")
T("A quarta", "a hora do relógio",
  "A quarta é a hora. Pesar de manhã em jejum e um ponto do dia; pesar à "
  "noite, depois de três refeições, e outro ponto.")
T("Juntas", "elas formam um intervalo",
  "Juntas, essas quatro fazem o seu número passear dentro de um intervalo "
  "que se repete e tem tamanho medível.")
T("E o tamanho é seu", "não é geral",
  "E esse tamanho é seu: depende de quanta água você carrega, do que come, "
  "de como treina. Por isso não existe número geral aqui.")
T("O que vem agora", "a conta, em dois passos",
  "O que vem agora é a conta. Dois passos, sete dias, e nada além da balança "
  "que você já tem em casa.")

# -------------------------------------------------------------------- cap 3
T("Passo um", "o mesmo momento, sete vezes",
  "Passo um: durante sete dias, pese uma vez por dia, sempre no mesmo "
  "momento. De manhã, em jejum, depois do banheiro, antes de beber água.",
  cap="A conta: sete dias e duas subtrações")
T("Mesmo momento", "e também mesma balança",
  "Mesmo momento é também mesma balança, no mesmo lugar do chao. Trocar de "
  "piso ou de aparelho no meio mistura dois instrumentos numa série só.")
T("Anote os sete", "todos, inclusive os ruins",
  "Anote os sete números. Todos. Inclusive o do dia que você quer esquecer, "
  "porque e justamente ele que define o tamanho que estamos medindo.")
T("Sete dias inteiros", "não cinco",
  "Sete dias inteiros, não cinco. Uma semana incompleta corta o fim de "
  "semana, e o fim de semana costuma ser o dia mais alto da série.")
T("Passo dois", "o maior e o menor",
  "Passo dois: olhe os sete e ache o maior e o menor. Esses dois valores são "
  "os únicos de que você precisa agora.")
T("A subtração", "esse e o seu número",
  "Subtraia o menor do maior. O resultado é a sua faixa de variação: o "
  "quanto a sua balança anda sozinha numa semana em que nada mudou.")
T("O que ele significa", "um limiar, não uma meta",
  "Esse número é um limiar: diferença menor que ele, entre duas pesagens, "
  "não é informação sobre o corpo. É o instrumento passeando.")
T("Guarde os dois", "a faixa e a média",
  "Guarde dois valores: a faixa, que é a subtração, e a média dos sete. A "
  "média sozinha não serve, porque sem a faixa você não sabe quanto ela "
  "pode errar.")

# ============================ DEPOIS DA RESPOSTA =============================

# -------------------------------------------------------------------- cap 4
T("Por que a média", "e não a pesagem de hoje",
  "A média dos sete é melhor que qualquer pesagem isolada, por aritmética: "
  "os dias altos e baixos se cancelam, e sobra o que não oscila.",
  cap="Por que a média de sete vence a pesagem de hoje")
T("Uma pesagem", "carrega a faixa inteira",
  "Uma pesagem sozinha carrega toda a faixa de variação em cima dela. A "
  "média de sete carrega uma fracao dessa faixa, porque o acaso aparece nos "
  "dois sentidos.")
T("Exemplo da sua própria série", "sem número meu",
  "Da para ver na sua série: compare o maior desvio de um dia com o tamanho "
  "da faixa. O dia erra muito mais que a média.")
T("E a média de amanhã", "muda pouco",
  "E tem outra vantagem. Trocando um dia por outro, a média de sete anda "
  "pouco. Isso é o que você quer de uma referência: que ela não pule.")
T("Não e desculpa", "e resolução",
  "Isso não é desculpa para ignorar a balança. É saber a resolução dela, do "
  "mesmo jeito que uma régua tem milímetros.")
T("Régua e balança", "a mesma ideia",
  "Ninguém tenta medir meio milímetro com uma régua de escola. Medir "
  "trezentos gramas de mudança com uma balança que varia um quilo é o mesmo "
  "gesto.")
T("O que você ganha", "para de reagir a ruído",
  "O que você ganha com a faixa é simples: você para de mudar o plano por "
  "causa de ruído, e passa a mudar só quando a leitura sai da faixa.")
T("O próximo passo", "como ler uma mudança",
  "Falta a parte que usa o número. Como saber, olhando a série, se algo "
  "realmente mudou.")

# -------------------------------------------------------------------- cap 5
T("A regra de leitura", "duas condições",
  "A regra tem duas condições, e as duas precisam valer ao mesmo tempo para "
  "uma mudança contar.",
  cap="Como saber se mudou de verdade")
T("Condição um", "maior que a faixa",
  "Condição um: a diferença entre a média desta semana e a da semana passada "
  "tem de ser maior que a sua faixa. Menor que ela, não conta.")
T("Condição dois", "repetiu",
  "Condição dois: a diferença apareceu no mesmo sentido em duas semanas "
  "seguidas. Uma semana sozinha ainda pode ser acaso dentro da faixa.")
T("Juntas", "elas filtram quase todo ruído",
  "Juntas, as duas condições derrubam quase todo o ruído. O que passa por "
  "elas é mudança de verdade, e merece que você mude algo.")
B("Media contra média", "nunca dia contra dia",
  "É sempre média contra média. Hoje contra o mesmo dia da semana passada "
  "compara dois sorteios dentro da faixa, e não prova nada.",
  "writing numbers in a notebook", 5466772)
T("Quando a faixa é grande", "espere mais",
  "Se a sua faixa saiu grande, você precisa de mais semanas para concluir "
  "algo. Não e azar: é a sua resolução.")
T("Quando ela é pequena", "você decide mais rápido",
  "Se saiu pequena, você enxerga mudanças menores e decide mais rápido. Dois "
  "corpos com a mesma rotina podem ter faixas bem diferentes.")
T("O que não fazer", "mudar a conta no meio",
  "O que não fazer: trocar o momento da pesagem, a balança ou o criterio no "
  "meio da série. Isso inventa uma mudança que não aconteceu no corpo.")

# -------------------------------------------------------------------- cap 6
T("Três erros", "que a faixa deixa visivel",
  "Com a faixa na mao, três erros comuns ficam óbvios. Todos eles são a mesma "
  "confusao: tratar leitura como mudança.",
  cap="Três erros que a faixa torna visíveis")
T("Erro um", "pesar todo dia e reagir todo dia",
  "Erro um: pesar todo dia e reagir todo dia. Pesar todo dia é útil, porque "
  "alimenta a média; reagir a cada leitura é ler ruído como notícia.")
T("Erro dois", "pesar quando parece bom",
  "Erro dois: pesar só quando parece que vai dar número bom. Isso corta os "
  "dias altos, encolhe a faixa e estraga as duas contas.")
T("Erro três", "comparar com outra pessoa",
  "Erro três: comparar a sua faixa com a de outra pessoa. Ela não mede "
  "esforço nem resultado, mede quanta água e comida o corpo movimenta.")
T("Nenhum dos três", "e falta de disciplina",
  "Nenhum dos três é falta de disciplina. Os três são erro de medição, e e "
  "por isso que tem conserto sem precisar de força nenhuma.")
T("O caso mais caro", "abandonar na primeira semana",
  "O caso mais caro é desistir na primeira semana por um número que estava "
  "dentro da faixa: interromper o que funcionava por ler mal o instrumento.")
T("E o caso inverso", "insistir em algo que não anda",
  "O inverso também acontece: insistir meses numa rotina que não move a média "
  "fora da faixa, porque uma leitura boa de vez em quando parece progresso.")
T("A faixa resolve os dois", "com o mesmo número",
  "A faixa resolve os dois casos com o mesmo número, e é esse o motivo de ela "
  "valer a semana que custa medir.")

# -------------------------------------------------------------------- cap 7
T("O que anotar", "e em que formato",
  "Vale falar do registro, porque a forma de anotar decide se a conta vai "
  "servir em um mês ou não.",
  cap="O que anotar, e por que dois números e não um")
T("Anote os sete", "não só a média",
  "Anote os sete números do dia, não apenas a média da semana. Sem os sete "
  "você não pode recalcular a faixa, e a faixa muda com o tempo.")
T("Dois números por semana", "faixa e média",
  "No fim de cada semana, feche dois números: a média dos sete e a faixa "
  "daquela semana. Uma linha por semana, dois valores.")
T("Por que dois", "um não distingue nada",
  "Por que dois: se a média cair e você tiver só ela, não dá para saber se "
  "caiu de verdade ou se a semana foi de faixa larga.")
T("Papel serve", "e aplicativo também",
  "Papel serve, caderno serve, aplicativo serve — desde que mostre os "
  "números do dia e não só um gráfico suavizado, que esconde o que interessa.")
T("Em quatro semanas", "você tem uma série",
  "Em quatro semanas você tem quatro médias e quatro faixas. E com isso você "
  "responde a pergunta que uma pesagem nunca respondeu: mudou, ou não mudou?")
T("E se a faixa mudar", "isso também é informação",
  "Se a faixa mudar muito de uma semana para outra, isso também e "
  "informação: algo na comida, no sal ou no treino mudou.")
T("Nada disso exige", "comprar coisa nenhuma",
  "E nada disso exige comprar nada, assinar nada nem trocar de balança. Exige "
  "sete leituras e duas subtrações.")

# -------------------------------------------------------------------- cap 8
T("Uma ressalva", "sobre o que a faixa não é",
  "Antes de terminar, uma ressalva, porque ela importa mais que a conta.",
  cap="O que esta conta NÃO diz")
T("Ela não diz", "se o seu peso está bom",
  "Esta conta não diz se o seu peso está bom, não diz qual deveria ser, e não "
  "diz se você precisa mudar algo. Ela diz apenas quando a balança está "
  "falando e quando está só variando.")
T("Ela não substitui", "quem acompanha você",
  "Ela também não substitui quem acompanha a sua saúde. Faixa de variação é "
  "leitura de instrumento, não diagnóstico, e não distingue perda de gordura "
  "de perda de músculo.")
T("Variação grande e rápida", "não é assunto de planilha",
  "E uma variação grande e rápida, de muitos quilos em pouco tempo, não é "
  "assunto de conta nenhuma: é assunto de consulta.")
T("O que sobra para você", "um limiar, e só",
  "O que sobra para você é um limiar, em quilos, calculado na sua casa, com a "
  "sua balança, nos seus sete dias. Abaixo dele, a leitura não é notícia.")
T("Comece hoje", "a série precisa de um dia um",
  "A série precisa de um dia um. Se você pesar amanhã de manhã e anotar, no "
  "próximo domingo você tem a sua faixa.")
C("Escreva a sua faixa aqui embaixo", "só o número da subtração",
  "Nos comentários, escreva só o número da subtração: maior menos menor, em "
  "quilos. Não o seu peso. Quero ver o quanto esse limiar muda entre pessoas "
  "que fazem a mesma rotina.")

# ================================== SHORT ====================================

# O short fecha UMA pergunta — quanto a balanca varia sozinha, com a conta
# inteira — e o longo abre OUTRA: como ler uma mudança contra esse numero
# (aprendizado 563). Trinta e poucos segundos, porque os dois shorts que
# mediram melhor neste canal tem trinta e cinco e trinta e sete segundos.

SHORT = [
    {"layout": "titulo", "kicker": "A balança varia", "sub": "sozinha",
     "nar": "A sua balança muda de número sem o seu corpo mudar nada. Essa "
            "variação tem tamanho, e dá para medir em uma semana.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Sete dias", "sub": "mesmo momento",
     "nar": "Pese uma vez por dia, sete dias, sempre no mesmo momento: de "
            "manhã, em jejum, depois do banheiro. Anote os sete.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ache dois", "sub": "o maior e o menor",
     "nar": "No fim da semana, ache o maior e o menor dos sete.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Subtraia", "sub": "esse e o seu limiar",
     "nar": "Subtraia o menor do maior. Esse é o seu limiar: qualquer "
            "diferença menor que ele não é mudança, e a balança passeando.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Como usar o limiar", "sub": "no vídeo",
     "nar": "Como saber se mudou de verdade são duas condições, e as duas "
            "estão no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Quanto ela", "l2": "varia sozinha"}

COPY = """# A faixa de variacao da propria balanca, medida em sete dias

## TITULO
Balança: Quanto Ela Varia Sozinha em Sete Dias, e Por Que Abaixo Disso Nada Mudou

## TITULO SHORT
Quanto sua balança varia sozinha

## DESCRICAO
Existe o número que a balança mostra e existe o quanto o seu corpo mudou. Os dois não são a mesma coisa, e a diferença entre eles tem um tamanho que você pode medir em casa, numa semana, sem comprar nada.

Quatro coisas movem o mostrador sem mover um grama de gordura: a água que o corpo troca ao longo do dia, a comida que ainda está em trânsito, o sal e o carboidrato que fazem o corpo segurar água por um ou dois dias, e a hora do relógio em que você sobe na balança. Juntas, elas fazem o seu número passear dentro de um intervalo que se repete toda semana.

A conta tem dois passos e nenhum número meu. Passo um: durante sete dias, pese uma vez por dia, sempre no mesmo momento — de manhã, em jejum, depois do banheiro, antes de beber água — e anote os sete valores, inclusive o do dia que você queria esquecer. Passo dois: ache o maior e o menor da série e subtraia. O resultado é a sua faixa de variação, e ela funciona como limiar: qualquer diferença menor que ela, entre duas pesagens, não é informação sobre o seu corpo.

O vídeo fecha essa conta nos primeiros três minutos e depois mostra o que fazer com o número: por que a média de sete dias vence qualquer pesagem isolada, as duas condições que uma mudança precisa cumprir para contar (ser maior que a faixa E repetir o sentido em duas semanas seguidas), três erros de medição que a faixa torna visíveis, e o que anotar por semana para que a série ainda sirva dentro de um mês.

Uma ressalva que importa mais que a conta: isso não diz se o seu peso está bom, não diz qual deveria ser e não substitui quem acompanha a sua saúde. Faixa de variação é leitura de instrumento, não diagnóstico, e não distingue perda de gordura de perda de músculo. Variação grande e rápida é assunto de consulta, não de planilha.

CAPITULOS
{CAPITULOS}

Escreva nos comentários só o número da subtração — maior menos menor, em quilos. Não o seu peso. Quero ver o quanto esse limiar muda entre pessoas com a mesma rotina.

## DISCLOSURE
Vídeo com narração e imagens geradas por computador. O roteiro é original e o conteúdo é informativo, não é orientação médica nem nutricional.

## HASHTAGS
#balanca #medicao #peso

## TAGS
balanca, faixa de variacao, como pesar, peso que oscila, media de sete dias, variacao de peso diaria, retencao de agua, pesar em jejum, erro de medicao, limiar de mudanca, acompanhar peso, peso oscila sem motivo, balanca de banheiro, serie semanal de peso, quando mudar a rotina

## COMENTARIO FIXADO
A conta inteira em duas linhas: pese sete dias no mesmo momento, anote os sete; pegue o maior, tire o menor. O resultado é o seu limiar — abaixo dele, a leitura não é notícia. Escreve aqui só esse número, em quilos, não o seu peso.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita peso ideal, nao cita indice de massa corporal, nao cita media nacional, nao cita quantos litros de agua o corpo carrega, nao cita percentual de variacao esperado, nao cita marca de balanca nem de aplicativo. O unico numero que decide e medido pelo espectador, na balanca da casa dele, em sete leituras: o maior menos o menor. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer faixa de referencia do tipo "o normal e variar X quilos", porque ela depende de massa, de rotina de comida e de treino, e um numero medio tornaria a conta errada para a maioria de quem assiste exatamente quando o numero certo esta na balanca dele; (2) qualquer afirmacao sobre quantos litros de agua o corpo troca por dia, porque nao conferi isso em duas fontes institucionais e o video nao precisa desse numero para a conta fechar — basta que a variacao exista, e a propria serie do espectador prova que existe; (3) qualquer juizo sobre peso, meta ou necessidade de mudar, porque a conta mede a RESOLUCAO do instrumento e nao o estado de quem sobe nele. ESTE EIXO SUBSTITUI O NUMERO INSTITUCIONAL DE PROPOSITO, e a decisao vem do proprio canal: os tres pacotes que abriram com numero da Anvisa (tres produtos proibidos, cento e oitenta e nove alegacoes permitidas, semaglutida generica registrada) somaram QUATRO views de short em tres pacotes, enquanto os dois que entregaram metodo aplicavel aos numeros do espectador (qual coluna da tabela comparar, em qual das duas faixas de atividade voce esta) somaram OITENTA E CINCO. O video tambem nao recomenda pesar todo dia nem deixar de pesar, nao vende nada, e diz explicitamente que variacao grande e rapida e assunto de consulta.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seja-mais-magra-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-009",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#22303C", "c1": "#3E7C8A", "c2": "#E0A458",
               "bg": "#F6F3EE"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/seja-mais-magra-009.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
    # Onde a conta fecha, que e o numero da alavanca B.
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "Subtraia o menor do maior" in (c.get("nar") or ""):
            print(f"  a subtracao fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
