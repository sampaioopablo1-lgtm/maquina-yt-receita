#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-003.

PAUTA, medida em 18/08/2026 e gravada em pautas_banco (canal com 114 linhas).
Tres buscas novas (produtos com proteina, excesso de proteina, quanta proteina
por dia) revelaram o eixo mais quente que este canal ja viu, e ele NAO e das
canetas:

    video (pt-BR, 90 dias)                              canal            v/d
    O GRAVE PROBLEMA DOS PRODUTOS COM MUITA PROTEINA    Ola, Ciencia!  13.566
    A Triste Vida dos Viciados em PROTEINA (27 min)     M. Matheus     10.781
    O que a moda da proteina fez com a gente? (32 min)  NV1C           10.330
    A verdade sobre a necessidade de proteina (23 min)  Dr. Seraphim    5.448
    Seu Corpo Joga Proteina Fora Depois de 30g?         Lua Ferrari       883

Mediana geral do banco do canal: 184,6. O eixo proteina roda a DEZENAS de
milhares de v/d, em video LONGO de 13 a 32 minutos — o formato raro em que o
nicho premia exatamente o que a maquina produz. Os tres do topo se citam
entre si: o eixo esta em conversa aberta agora.

EIXO NAO USADO: os cinco discutem a CIENCIA (quanto precisa, mito dos 30g,
ortorexia). NENHUM faz a conta de CONSUMO no supermercado — o que cada grama
custa, como a coluna dos 100 g compara, quanto do preco e marketing. E a casa
deste canal e precisamente numeros aplicaveis: peso x fator, rotulo, preco
por grama, folha de seis linhas.

NUMEROS VERIFICADOS (duas fontes institucionais que batem, 18/08/2026):
  * OMS/FAO, "Protein and Amino Acid Requirements in Human Nutrition" (2007):
    0,8 g/kg/dia minimo para adulto saudavel; 70 kg -> 56 g/dia. Faixa para
    treino/emagrecimento/idade citada na literatura: 1,2 a 2,0 g/kg.
  * Anvisa, RDC 429/2020 + IN 75/2020, em vigor desde 09/10/2022: tabela
    nutricional por 100 g/100 ml OBRIGATORIA, criada para comparacao.
  * Estudo 25 g vs 100 g numa refeicao (2023, pubmed 38118410) — o mito dos
    30 g; e o proprio outlier do nicho cita e discute o mesmo estudo.
Nenhum preco de produto e afirmado: o metodo (gramas / real) e ensinado com
as celulas em branco, no estilo da casa.

SIMILARIDADE vs pacotes anteriores do MESMO canal:
  -001 "Ozempic Natural Existe? 3 Produtos que a Anvisa Proibiu" -> produtos
       falsos de farmacia
  -002 "Ozempic e Mounjaro: O Que Voce Reganha..."               -> reganho e
       massa magra pos-caneta
Este NAO e caneta e NAO e produto proibido: e rotulo de ALIMENTO e conta de
mercado. A ponte com a -002 existe (proteina protege massa magra no
emagrecimento) e e citada uma vez, como continuidade.

TITULO modela a ESTRUTURA do outlier ("O GRAVE PROBLEMA DOS PRODUTOS COM
MUITA PROTEINA QUE NINGUEM ESTA FALANDO" = [produtos com proteina] + [o que
ninguem mostra]), nunca o assunto do video dele; keyword nos 5 primeiros
termos.

DIMENSIONAMENTO pelo agregado de producao (fabrica/ensaio.py, n=76):
pt-BR-FranciscaNeural = 16,92 chars/s + 1,036 s/frase. ~10.100 chars em ~72
cenas fecham ~13,1 min.
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
T("A prateleira mudou", "proteína em tudo",
  "Pão com proteína. Iogurte com proteína. Até água com proteína. A "
  "prateleira inteira decidiu, de repente, que você precisa de mais.",
  cap="A prateleira encheu de proteína")
I("O preço acompanhou", "a versão proteica custa mais",
  "E cada versão proteica custa mais que a versão comum ao lado. Você paga a "
  "diferença acreditando que está comprando saúde.")
I("A pergunta errada", "isso é saudável?",
  "A pergunta que a embalagem quer que você faça é: isso é saudável? Essa "
  "pergunta não tem número, e por isso ela é tão fácil de vender.")
I("As perguntas certas", "duas contas",
  "As perguntas que decidem a compra são outras. De quantos gramas você "
  "precisa por dia? E quanto custa cada grama que está no seu carrinho?")
I("Quem responde", "não é a frente do pote",
  "Nenhuma das duas é respondida pela frente da embalagem. As duas são "
  "respondidas por uma multiplicação e uma divisão que cabem num guardanapo.")
L("O que este vídeo monta", ["A conta do seu corpo", "O truque da porção",
                             "Proteína por real", "Folha de seis linhas",
                             "Armadilhas caras"],
  "Cinco partes. A conta do seu corpo. O truque da porção no rótulo. A "
  "proteína por real. A folha de seis linhas. E as armadilhas mais caras da "
  "gôndola.")
I("Antes de tudo", "proteína não é vilã",
  "Uma coisa precisa ficar clara desde já. Proteína não é vilã, e comer "
  "pouca proteína é um problema real. O assunto aqui é o preço da embalagem, "
  "não o nutriente.")
I("A regra da casa", "fonte, número e conta",
  "E vale a regra de sempre deste canal: fonte com nome, número com data, e "
  "uma conta que você refaz em casa sem acreditar em ninguém.")
T("Então", "quanto você precisa?",
  "Começando pela pergunta que sustenta todas as outras: de quantos gramas o "
  "seu corpo realmente precisa por dia?")

# ---------------------------------------------------------------- cap 2
T("A conta do corpo", "peso vezes fator",
  "A resposta inteira cabe numa multiplicação: o seu peso vezes um fator. "
  "Todo o resto da discussão é detalhe em cima disso.",
  cap="A conta do seu corpo")
I("O fator mínimo", "zero vírgula oito",
  "A Organização Mundial da Saúde usa zero vírgula oito grama por quilo de "
  "peso por dia como referência mínima para adulto saudável.")
I("Na prática", "setenta quilos",
  "Para uma pessoa de setenta quilos, isso dá cinquenta e seis gramas por "
  "dia. Esse número é o piso de sobrevivência, não a meta de todo mundo.")
I("De onde vem", "OMS e FAO",
  "O valor vem do documento de necessidades de proteína da OMS com a FAO, "
  "publicado em dois mil e sete. É referência antiga, e continua sendo a "
  "referência.")
I("Quem precisa de mais", "treino, dieta, idade",
  "Quem treina força, quem está emagrecendo e quem está envelhecendo precisa "
  "de mais. A faixa citada na literatura vai de um vírgula dois a dois "
  "gramas por quilo.")
I("Por que na dieta", "proteger o músculo",
  "Durante o emagrecimento a proteína ganha um papel extra: segurar a massa "
  "magra enquanto o peso desce. Foi exatamente o assunto do vídeo anterior "
  "deste canal.")
I("Sua meta", "sai do seu peso",
  "A sua meta, portanto, não sai de vídeo nenhum, nem deste. Sai do seu "
  "peso, multiplicado pelo fator da sua situação.")
I("É faixa, não gatilho", "sem neurose de gatilho",
  "E é uma faixa, não um gatilho. Ficar um pouco abaixo num dia não desfaz "
  "nada, e estourar a faixa não constrói músculo extra.")
I("Sem cronômetro", "o dia inteiro conta",
  "Também não precisa de cronômetro nem de balança de bolso. O que conta é o "
  "total do dia, somado do jeito que a sua rotina permitir.")
I("O caso dos mais velhos", "o corpo responde menos",
  "Nos mais velhos há um agravante com nome: resistência anabólica. O corpo "
  "responde menos ao mesmo estímulo, e por isso a faixa deles fica na parte "
  "de cima.")
I("A exceção séria", "rim é caso de consulta",
  "Uma exceção importante: quem tem doença renal ou outra condição de saúde "
  "faz essa conta com um profissional, nunca com um vídeo.")
T("Meta na mão", "agora, o rótulo",
  "Com a sua meta na mão, a pergunta vira: onde esses gramas estão? E é aí "
  "que o rótulo começa a trabalhar contra você.")

# ---------------------------------------------------------------- cap 3
T("O rótulo", "duas colunas, duas histórias",
  "Todo rótulo brasileiro mostra a proteína em duas colunas: por porção e "
  "por cem gramas. As colunas contam histórias diferentes.",
  cap="O truque da porção")
I("Quem escolhe a porção", "a marca",
  "A porção é definida pela marca, produto a produto. Um pacote usa trinta "
  "gramas, outro usa duzentos mililitros. São números que não se comparam.")
I("O número da frente", "o que fica bem na foto",
  "E o número estampado na frente da embalagem é sempre o que fica melhor na "
  "foto. A frente é publicidade. A tabela é obrigação legal.")
I("A coluna que compara", "cem gramas",
  "A coluna que serve para comparar é a de cem gramas. Ela iguala a régua "
  "entre qualquer pote, pacote ou garrafa da loja.")
I("Desde quando", "regra da Anvisa",
  "Isso não é gentileza da marca: é regra da Anvisa em vigor desde outubro "
  "de dois mil e vinte e dois, criada exatamente para permitir comparação.")
I("A regra prática", "ignore a frente",
  "A regra prática tem uma linha só: ignore a frente, vire a embalagem, leia "
  "a coluna dos cem gramas. Sempre a mesma coluna, em todos os produtos.")
I("O que aparece", "surpresas na mesma régua",
  "Lida na mesma régua, a gôndola surpreende. Um iogurte proteico pode ter "
  "menos proteína por cem gramas que um iogurte natural comum ao lado.")
I("O pão proteico", "compare com o pão comum",
  "O pão proteico passa pelo mesmo teste: parte da diferença que você paga "
  "está na receita, e parte está só na palavra impressa na frente.")
I("A água com proteína", "o caso extremo",
  "O caso extremo da onda é a água com proteína. Poucos gramas por garrafa, "
  "preço de suplemento, e a mesma palavra grande na frente fazendo o "
  "trabalho todo.")
I("Selo não é medida", "efeito halo",
  "A palavra proteína escrita em letra grande não mede nada. É o efeito "
  "halo: um atributo bom iluminando o resto do produto na sua cabeça.")
I("O resto vem junto", "açúcar e sódio na carona",
  "Porque o resto vem junto. Açúcar, sódio e a lista de ingredientes "
  "continuam lá, embaixo da palavra que fez você pegar o pote.")
T("Coluna certa", "falta o preço",
  "Coluna certa escolhida. Agora falta cruzar o rótulo com o número que ele "
  "nunca mostra: o preço de cada grama.")

# ---------------------------------------------------------------- cap 4
T("Proteína por real", "a divisão da casa",
  "A conta é uma divisão: os gramas de proteína do pacote inteiro, divididos "
  "pelo preço do pacote. O resultado é proteína por real.",
  cap="Proteína por real")
I("Como montar", "tabela, peso, etiqueta",
  "Os ingredientes da conta já estão na loja. A tabela diz os gramas por cem "
  "gramas. A embalagem diz o peso total. A etiqueta da gôndola diz o preço.")
I("Por que sem preços aqui", "a conta é sua",
  "Este vídeo não vai te dar preço nenhum, de propósito. Preço muda por "
  "cidade, por semana e por marca. O método é o que fica valendo.")
I("O padrão", "a comida comum ganha",
  "Mas o padrão que a divisão revela é consistente: as fontes comuns quase "
  "sempre entregam o grama de proteína mais barato da loja.")
I("O exemplo clássico", "o ovo",
  "O exemplo clássico é o ovo: cerca de seis gramas de proteína por unidade, "
  "num dos custos por grama mais baixos que existem.")
I("O prato de casa", "arroz com feijão",
  "E o prato mais brasileiro de todos entra na lista: arroz com feijão forma "
  "proteína completa, por um custo que nenhum pote com nome em inglês "
  "alcança.")
I("O frango da semana", "quilo rende",
  "Frango, ovos, sardinha, leite: a lista de fontes baratas é curta, "
  "conhecida e resolve a maior parte da meta de quase todo mundo.")
B("O desenho da divisão", ["Ovo", "Feijão", "Frango", "Pote proteico"],
  [100, 90, 70, 25],
  "Feita a divisão, o desenho costuma ser esse: comida comum no topo da "
  "entrega por real, produto de marketing lá embaixo.")
I("O que o pote vende", "conveniência",
  "O que o produto proteico vende de verdade é conveniência: abrir e comer. "
  "Conveniência é um valor real. Só precisa ser cobrada pelo nome certo.")
I("Quando vale", "sabendo o multiplicador",
  "E há dias em que ela vale: rotina apertada, viagem, falta de opção. O "
  "problema nunca é comprar. É comprar sem saber quantas vezes mais caro o "
  "grama saiu.")
T("Meta e preço na mão", "falta o papel",
  "Meta calculada, preço por grama entendido. Falta organizar tudo num papel "
  "que dura a semana:")

# ---------------------------------------------------------------- cap 5
T("Folha de seis linhas", "sua meta num papel",
  "Seis linhas resolvem. Uma folha, preenchida uma vez, ajustada quando o "
  "peso mudar.",
  cap="A folha de seis linhas")
I("Linha um", "seu peso",
  "Linha um: o seu peso atual. É ele que dimensiona todo o resto da folha.")
I("Linha dois", "seu fator",
  "Linha dois: o fator da sua situação. O piso da OMS para quem é sedentário "
  "e saudável, a faixa de cima para quem treina ou está emagrecendo.")
I("Linha três", "a multiplicação",
  "Linha três: a meta diária. É a linha um vezes a linha dois, e é a única "
  "multiplicação da folha inteira.")
I("Linha quatro", "o que já entra",
  "Linha quatro: uma estimativa honesta do que você já come de proteína num "
  "dia comum. A maioria descobre que não está tão longe quanto pensava.")
I("Linha cinco", "a lacuna",
  "Linha cinco: a diferença entre a meta e o que já entra. É essa lacuna, e "
  "só ela, que precisa de solução. Não o dia inteiro.")
I("Linha seis", "como preencher",
  "Linha seis: com o que a lacuna será preenchida, começando pelas fontes "
  "comuns que a sua conta por real apontou. Ovo, feijão, frango.")
I("E o suplemento", "última linha, não primeira",
  "Suplemento entra na linha seis quando a rotina pede, com o preço por "
  "grama anotado do lado. Ele é atalho de conveniência, não requisito.")
I("Por que a folha funciona", "tira o marketing da decisão",
  "A folha funciona por um motivo simples: quando a lacuna tem tamanho "
  "escrito, a promessa da embalagem para de mandar na compra.")
T("Sistema no papel", "faltam as armadilhas",
  "Sistema no papel. Falta blindar contra os quatro erros que mais custam "
  "caro nessa prateleira:")

# ---------------------------------------------------------------- cap 6
T("Armadilha um", "saúde por associação",
  "A primeira: levar ultraprocessado para casa como se fosse saúde porque a "
  "frente diz proteína. A palavra não muda a lista de ingredientes.",
  cap="Quatro armadilhas caras")
I("O que vem na carona", "doses que você recusaria",
  "Em muitos desses produtos, a proteína chega acompanhada de açúcar e sódio "
  "em doses que você não aceitaria num produto sem a palavra mágica.")
I("Armadilha dois", "mais é sempre melhor",
  "A segunda: achar que estourar a faixa constrói músculo extra. Acima do "
  "teto da sua faixa, o corpo não guarda o excedente como músculo.")
I("Armadilha três", "o teto dos trinta gramas",
  "A terceira é o mito invertido: o suposto teto de trinta gramas por "
  "refeição, aquele medo de que o resto vira desperdício.")
I("O estudo que testou", "doses grandes numa refeição",
  "O estudo que testou isso é de dois mil e vinte e três. Ele comparou doses "
  "pequenas contra uma dose de cem gramas, numa refeição única, e acompanhou "
  "as horas seguintes.")
I("O que ele viu", "o corpo dá conta",
  "O corpo aproveitou a dose maior ao longo do tempo. Distribuir proteína "
  "pode ser estratégia útil; obrigação biológica não é.")
I("Armadilha quatro", "colágeno como proteína",
  "A quarta: pagar colágeno como se fosse proteína completa. Colágeno é "
  "proteína incompleta, sem o conjunto de aminoácidos que a conta da sua "
  "meta pressupõe.")
I("O detalhe do colágeno", "some da conta da meta",
  "Isso não faz do colágeno um produto inútil para outros fins. Faz dele um "
  "número que não entra na linha da sua meta de proteína, e o rótulo não "
  "avisa.")
I("O fio comum", "decidir sem número",
  "As quatro têm o mesmo fio: uma decisão de compra tomada pela frente da "
  "embalagem, sem nenhum número do seu lado da mesa.")
I("O antídoto", "duas contas",
  "O antídoto são as duas contas deste vídeo: peso vezes fator, e gramas por "
  "real. Com as duas na mão, o marketing perde a alavanca.")
T("Última parte", "fazer durar",
  "Falta o de sempre: fazer isso sobreviver à semana que vem.")

# ---------------------------------------------------------------- cap 7
T("Para durar", "três hábitos",
  "Isso se mantém com três hábitos pequenos. Nenhum exige força de vontade. "
  "Todos exigem lugar fixo.",
  cap="Para durar")
I("Primeiro", "a folha na cozinha",
  "Primeiro: a folha de seis linhas fica na cozinha, visível. Meta que mora "
  "numa gaveta não muda compra nenhuma.")
I("Segundo", "um rótulo por compra",
  "Segundo: um rótulo novo lido por compra, sempre na coluna dos cem gramas. "
  "Um por vez, sem transformar o mercado em auditoria.")
I("Terceiro", "refazer quando o peso mudar",
  "Terceiro: refazer a linha três quando o peso mudar. A meta acompanha o "
  "corpo, e não o contrário.")
L("O resumo", ["Peso vezes fator", "Coluna dos cem gramas",
               "Gramas por real", "Comida comum primeiro",
               "Folha na cozinha"],
  "O resumo cabe em cinco linhas. Multiplique peso por fator. Leia a coluna "
  "dos cem gramas. Divida gramas por real. Preencha com comida comum "
  "primeiro. Deixe a folha à vista.")
I("Se fizer uma coisa só", "uma conta e um rótulo",
  "Se for fazer só o essencial depois deste vídeo, faça isto. Multiplique "
  "seu peso por zero vírgula oito, e leia um rótulo na coluna dos cem "
  "gramas.")
I("O tempo que leva", "menos que a fila do caixa",
  "As duas coisas juntas levam menos tempo que a fila do caixa. E mudam a "
  "próxima compra inteira.")
C("Seja Mais Magra", "evidência, não promessa",
  "Agora me conta nos comentários: qual produto proteico da sua despensa "
  "perdeu para o ovo na conta por grama? Estou juntando os casos.")
C("Seja Mais Magra", "evidência, não promessa",
  "E se existe outro rótulo que você quer ver passar pela mesma conta, "
  "escreve o nome dele. O mais pedido vira o próximo vídeo do canal.")

SHORT = [
    {"layout": "titulo", "kicker": "Proteína em tudo",
     "sub": "a conta que falta",
     "nar": "A prateleira encheu de pão proteico e iogurte proteico. A conta "
            "que decide a compra ninguém imprime.", "sem_cap": True},
    {"layout": "item", "kicker": "Sua meta", "preco": "peso vezes o fator",
     "nar": "Multiplique seu peso por zero vírgula oito. Esse é o mínimo de "
            "gramas de proteína por dia segundo a OMS.", "sem_cap": True},
    {"layout": "item", "kicker": "O rótulo", "preco": "coluna dos cem gramas",
     "nar": "No rótulo, ignore a frente e leia a coluna dos cem gramas. Ela "
            "existe por regra da Anvisa exatamente para comparar.",
     "sem_cap": True},
    {"layout": "item", "kicker": "A divisão", "preco": "gramas por real",
     "nar": "Divida os gramas do pacote pelo preço. O ovo costuma vencer "
            "quase todo pote com proteína no nome.", "sem_cap": True},
    {"layout": "cta", "kicker": "Seja Mais Magra", "sub": "a conta completa",
     "nar": "Essa é a conta inteira: meta, coluna e divisão. Qual produto da "
            "sua despensa perde para o ovo? Comenta aí.", "sem_cap": True},
]

COPY = """# A conta por grama que a prateleira proteica não imprime

## TÍTULO
Produtos com Proteína: A Conta por Grama que Ninguém Faz no Supermercado

## DESCRIÇÃO
Pão proteico, iogurte proteico, água com proteína. A prateleira inteira decidiu que você precisa de mais — e cada versão proteica custa mais que a versão comum ao lado. Este vídeo não pergunta se isso é saudável. Ele faz as duas contas que a embalagem espera que você não faça.

A CONTA DO SEU CORPO. A Organização Mundial da Saúde usa 0,8 g de proteína por quilo de peso por dia como referência mínima para adulto saudável (documento OMS/FAO de necessidades de proteína, 2007) — para 70 kg, 56 g por dia. Quem treina força, está emagrecendo ou envelhecendo trabalha com a faixa maior citada na literatura, de 1,2 a 2,0 g/kg. Sua meta não sai de vídeo nenhum: sai do seu peso vezes o seu fator.

O TRUQUE DA PORÇÃO. A porção do rótulo é escolhida pela marca e não se compara entre produtos. A coluna que compara é a de 100 g — obrigatória por regra da Anvisa (RDC 429/2020 e IN 75/2020) em vigor desde outubro de 2022, criada exatamente para isso. Lida na mesma régua, a gôndola surpreende: um iogurte proteico pode ter menos proteína por 100 g que o iogurte natural ao lado.

PROTEÍNA POR REAL. A divisão da casa: gramas de proteína do pacote inteiro divididos pelo preço. Este vídeo não dá preço nenhum de propósito — preço muda por cidade e por semana; o método fica. O padrão que a conta revela é consistente: ovo (cerca de 6 g por unidade), feijão com arroz, frango e sardinha entregam o grama mais barato da loja, e o que o pote proteico vende de verdade é conveniência. Conveniência tem valor — só precisa ser cobrada pelo nome certo.

A FOLHA DE SEIS LINHAS. Peso, fator, meta (a única multiplicação), o que você já come, a lacuna, e como preenchê-la começando pela comida comum. Suplemento entra na última linha quando a rotina pede, com o custo por grama anotado do lado.

E AS QUATRO ARMADILHAS CARAS: o ultraprocessado comprado como saúde por causa de uma palavra na frente; o mito de que estourar a faixa vira músculo; o falso teto de 30 g por refeição — um estudo de 2023 que comparou doses de 25 g e 100 g numa única refeição mostrou o corpo aproveitando a dose maior ao longo das horas; e o colágeno pago como se fosse proteína completa.

Se você fizer uma única coisa depois deste vídeo: multiplique seu peso por 0,8 e leia um único rótulo na coluna dos 100 g. Leva menos tempo que a fila do caixa.

## CAPÍTULOS
{CAPITULOS}

## COMENTÁRIO
Uma pergunta, porque a resposta muda de despensa para despensa: qual produto proteico da sua casa perdeu para o ovo quando você fez a conta por grama? E qual rótulo você quer ver passar pela mesma conta no próximo vídeo? O mais pedido vai primeiro.

## HASHTAGS
#Proteina #RotuloNutricional #SejaMaisMagra

## TAGS
produtos com proteína, quanta proteína por dia, proteína por dia, rótulo nutricional, pão proteico, iogurte proteico, whey protein vale a pena, alimentos ricos em proteína, marketing nutricional, ultraprocessados, tabela nutricional, proteína para emagrecer, quanto custa proteína, nutrição baseada em evidências, efeito halo

## CONFIGURAÇÕES DO STUDIO
- Idioma: Português (Brasil) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Localização: Brasil | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ativados (duração acima de 8 minutos)

## MÚSICA / LICENÇA
{TRILHA}

## FONTES
A referência de 0,8 g de proteína por quilo por dia para adultos saudáveis vem do documento "Protein and Amino Acid Requirements in Human Nutrition" (OMS/FAO/UNU, 2007); o exemplo de 56 g/dia para 70 kg é aritmética direta desse fator. A faixa de 1,2 a 2,0 g/kg para pessoas ativas, em emagrecimento ou mais velhas reflete o intervalo citado na literatura esportiva e geriátrica recente. A obrigatoriedade da coluna por 100 g na tabela nutricional é da Anvisa (RDC 429/2020 e IN 75/2020, em vigor desde 09/10/2022), criada para permitir comparação entre produtos. O estudo sobre doses altas numa única refeição é o ensaio publicado em dezembro de 2023 que comparou 25 g e 100 g de proteína pós-treino (PubMed 38118410). O dado de ~6 g de proteína por ovo é o valor aproximado de tabelas de composição de alimentos para um ovo de tamanho médio. NENHUM preço de produto é afirmado neste vídeo, de propósito: preços variam por cidade, semana e marca, e o método ensinado usa os números que você mesmo coleta na loja. Este vídeo é conteúdo educativo sobre leitura de rótulos e matemática de consumo; não é aconselhamento médico nem nutricional, não substitui consulta com profissional de saúde, e quem tem doença renal ou outra condição clínica deve definir metas de proteína com seu médico ou nutricionista.
"""

SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-003",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    # canais.trilha do banco; o credito CC-BY sai do hash no copy.
    "trilha": "Wholesome",
    "paleta": {"ink": "#2B1B1F", "c1": "#C9184A", "c2": "#7FB069", "bg": "#FDF3F4"},
    "thumb": {"l1": "PROTEÍNA EM TUDO", "l2": "a conta que falta"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/seja-mais-magra-003.json"
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
