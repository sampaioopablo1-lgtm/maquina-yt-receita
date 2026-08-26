#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-007.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA: 55 views no canal inteiro, ZERO inscritos, mediana de
0,37 view por dia por short e topo de 3,64. E a menor distribuicao da frota.

O QUE DEU CERTO: o eixo de CHECAR, e nao o de recomendar. Foi medido no proprio
nicho em 11/08 e bate o de recomendar em quinze vezes. Os tres pacotes
anteriores seguem esse eixo e e por isso que o canal existe.

O QUE NAO DEU: converter, e da para dizer por que com precisao. Os tres eixos
anteriores sao todos o MESMO gesto — ler um rotulo ou um registro:

    004  as 189 alegacoes permitidas em shake e termogenico
    005  o registro da semaglutida generica na Anvisa
    006  a coluna certa da tabela nutricional

Nos tres o espectador confere um PRODUTO. Ele nao decide nada, nao ha conta
que sobreviva a saida do supermercado, e o que ele leva embora e desconfianca,
nao um metodo. Pelo aprendizado 504 falta a condicao dois: nao ha escolha
dele, e sem escolha nao ha conversao.

O QUE MUDEI: a coisa medida deixa de ser um rotulo e passa a ser a SEMANA DELE.
A conta e feita nos proprios minutos, a escolha e dele todo dia, e o resultado
nao depende de comprar nada.

E ha uma aritmetica dentro dela que quase ninguem faz: os minutos intensos
valem o DOBRO. As duas faixas oficiais sao equivalentes — 150 a 300 moderados
OU 75 a 150 intensos — entao um minuto intenso conta como dois moderados. Quem
mistura os dois tipos na mesma semana, que e a maioria, esta somando errado.

OS NUMEROS, e as duas rotas institucionais

  - Adultos: 150 a 300 minutos semanais de atividade fisica moderada, OU 75 a
    150 minutos de atividade intensa, ou uma combinacao equivalente.
  - Fortalecimento muscular em pelo menos DOIS dias por semana, e isso e um
    requisito separado, nao parte dos minutos.

    rota 1  OMS — "WHO guidelines on physical activity and sedentary
            behaviour" (2020), e a pagina "Every move counts towards better
            health"
    rota 2  Ministerio da Saude do Brasil — "Guia de Atividade Fisica para a
            Populacao Brasileira" (2021), feito com a UFPel e a OPAS, com as
            mesmas duas faixas e os mesmos dois dias

O QUE FICOU DE FORA, e o video diz em voz alta

  - O BLOCO MINIMO de dez minutos. Esta e a descoberta desta rodada e ela e um
    descarte: as proprias paginas da OMS divergem entre si. Paginas regionais
    antigas ainda trazem "bouts of at least 10 minutes", que e a recomendacao
    de 2010, enquanto a diretriz de 2020 e comunicada como "cada movimento
    conta". Duas rotas nao batem, entao o numero NAO entra no video. O video
    conta o desacordo em vez de escolher um lado.
  - Qualquer promessa de perda de peso, em quilos ou em prazo.
  - Qualquer dose, prescricao ou indicacao. E nicho YMYL e a regra do canal e
    mais dura que a da rede.
  - Qualquer numero de calorias gastas por minuto. Depende da pessoa.
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


# ---------------------------------------- 1. Duas faixas, nao uma
T("São duas faixas", "e quase ninguém sabe da segunda",
  "A recomendação oficial de atividade física para adultos não é um número. "
  "São duas faixas, e a maioria das pessoas só ouviu falar de uma.",
  cap="São duas faixas, não uma")
I("A que todo mundo conhece", "cento e cinquenta a trezentos",
  "A conhecida é a moderada: de cento e cinquenta a trezentos minutos por "
  "semana.")
I("A que quase ninguém cita", "setenta e cinco a cento e cinquenta",
  "A outra é a intensa: de setenta e cinco a cento e cinquenta minutos por "
  "semana. Metade do tempo.")
T("E as duas são equivalentes", "e aí mora a conta",
  "As duas faixas são apresentadas como equivalentes. E é exatamente aí que "
  "mora a conta que este vídeo ensina.")
T("Porque se são equivalentes", "um minuto intenso vale dois",
  "Porque se metade do tempo entrega o mesmo, então um minuto intenso vale "
  "dois minutos moderados. Simples assim, e quase ninguém soma desse jeito.")
T("O que você vai saber fazer", "somar a sua própria semana",
  "Ao fim você vai conseguir somar a sua semana em uma unidade só e comparar "
  "com a faixa. A sua semana, não a média de ninguém.")
T("E antes de tudo", "isto não substitui consulta",
  "Antes de tudo, o de sempre: isto não substitui consulta médica, e quem tem "
  "qualquer condição de saúde decide isso com quem acompanha o caso.")
T("Não há promessa de peso", "há uma conta para fazer",
  "E não há aqui promessa de perda de peso nenhuma. O que existe é o que as "
  "instituições recomendam, e a conta que sai disso.")

# ---------------------------------------- 2. De onde vem
T("De onde vem o número", "duas instituições, o mesmo número",
  "Antes da conta, de onde vem o número. Duas instituições independentes, e "
  "elas dizem a mesma coisa.",
  cap="De onde vem o número")
I("A primeira", "a Organização Mundial da Saúde",
  "A primeira é a Organização Mundial da Saúde, nas diretrizes de atividade "
  "física e comportamento sedentário publicadas em dois mil e vinte.")
I("A segunda", "o Ministério da Saúde",
  "A segunda é o Ministério da Saúde, no Guia de Atividade Física para a "
  "População Brasileira, de dois mil e vinte e um.")
T("O guia brasileiro", "não é tradução",
  "O guia brasileiro não é tradução. Foi feito com a Universidade Federal de "
  "Pelotas e com a Organização Pan-Americana da Saúde, com dezenas de "
  "pesquisadores.")
T("E ainda assim", "as faixas são as mesmas",
  "E mesmo assim as duas faixas são as mesmas, e os dois dias de "
  "fortalecimento também. Quando duas rotas independentes batem, o número "
  "entra.")
T("Quando não batem", "ele não entra",
  "E quando elas não batem, o número não entra. Tem um caso desses neste "
  "vídeo, e ele vai ter um capítulo só para ele.")
I("Por que isso importa aqui", "é assunto de saúde",
  "Isso importa mais aqui do que em qualquer outro assunto, porque em saúde "
  "um número errado não é só um número errado.")
T("Então a regra é simples", "duas rotas ou nada",
  "A regra deste canal é simples: duas rotas oficiais que batam, ou o número "
  "fica de fora e eu digo que ficou.")

# ---------------------------------------- 3. A conta
T("Agora a conta", "três passos e uma unidade só",
  "Agora a conta. São três passos, e o truque é converter tudo para uma "
  "unidade só antes de somar.",
  cap="A conta da sua semana")
I("Passo um", "anote a semana em duas colunas",
  "Passo um: escreva a semana passada em duas colunas. Minutos de atividade "
  "moderada de um lado, minutos de atividade intensa do outro.")
T("Vale tudo que é movimento", "trabalho, deslocamento, casa",
  "E vale tudo que é movimento, não só academia. Trabalho, deslocamento a pé "
  "ou de bicicleta, tarefas de casa, lazer.")
I("Passo dois", "multiplique a coluna intensa por dois",
  "Passo dois: multiplique a coluna intensa por dois. Agora ela está na mesma "
  "unidade da outra.")
I("Passo três", "some as duas colunas",
  "Passo três: some as duas colunas. O resultado é a sua semana inteira "
  "escrita em minutos moderados.")
T("E aí compare", "com a faixa conhecida",
  "E aí é só comparar esse total com a faixa de cento e cinquenta a "
  "trezentos.")
T("Um exemplo redondo", "só para ver a mecânica",
  "Um exemplo com números redondos, só para ver a mecânica funcionando.")
T("Noventa moderados", "e trinta intensos",
  "Digamos noventa minutos moderados na semana, mais trinta minutos intensos. "
  "Somando cru dá cento e vinte, e parece que faltou pouco.")
T("Mas a conta certa", "dá cento e cinquenta",
  "A conta certa dobra os trinta: noventa mais sessenta dá cento e cinquenta. "
  "A mesma semana, e agora ela está dentro da faixa.")

# ---------------------------------------- 4. Os dois dias
T("E há uma segunda exigência", "que não é feita de minutos",
  "E há uma segunda exigência, que não é feita de minutos e por isso escapa "
  "de quase toda conversa sobre o assunto.",
  cap="Os dois dias que não são minutos")
I("Fortalecimento muscular", "em pelo menos dois dias",
  "As duas rotas pedem atividades de fortalecimento muscular em pelo menos "
  "dois dias por semana.")
T("Dias, não minutos", "a unidade aqui é outra",
  "Repare na unidade: o texto fala em dias, não em minutos. São duas contas "
  "diferentes, e elas não se substituem.")
T("Então não troque uma pela outra", "é o erro mais comum",
  "E o erro mais comum é trocar uma pela outra. Somar minutos de caminhada e "
  "achar que a parte de fortalecimento está resolvida.")
T("E o contrário também", "só força não fecha a outra",
  "O contrário vale igual. Dois dias de força não preenchem a faixa de "
  "minutos, porque são coisas diferentes sendo pedidas.")
I("Então a folha tem três campos", "duas colunas e um contador",
  "Então a sua folha tem três campos: as duas colunas de minutos, e um "
  "contador de dias de fortalecimento.")
T("Três campos", "e a semana fica descrita",
  "Três campos e a semana inteira fica descrita. E aí dá para ver qual dos "
  "três está mais longe, que é a única informação acionável disso tudo.")
T("Porque a pergunta útil", "não é se você faz o suficiente",
  "Porque a pergunta útil nunca foi se você faz o suficiente. É qual dos três "
  "campos está mais vazio nesta semana.")

# ---------------------------------------- 5. O numero descartado
T("Agora o número que ficou fora", "e por que ficou",
  "Agora o capítulo prometido: o número que eu tinha para dar e não dei.",
  cap="O número que ficou de fora")
I("A regra dos dez minutos", "você já ouviu falar dela",
  "Você provavelmente já ouviu que só contam blocos de pelo menos dez "
  "minutos. Que caminhar cinco minutos não serviria de nada.")
T("Eu fui conferir", "e as fontes divergem",
  "Fui conferir para poder dizer isso com segurança, e as próprias páginas da "
  "Organização Mundial da Saúde divergem entre si.")
T("Páginas antigas dizem uma coisa", "a diretriz nova comunica outra",
  "Páginas mais antigas ainda trazem o bloco mínimo de dez minutos, que vem "
  "da recomendação de dois mil e dez. A diretriz de dois mil e vinte é "
  "comunicada de outro jeito: cada movimento conta.")
T("Duas rotas que não batem", "então não entra",
  "Duas rotas que não batem no mesmo número. Pela regra deste canal, então, "
  "ele não entra no vídeo.")
I("E o que fazer com isso", "anote os dois totais",
  "O que dá para fazer sem escolher um lado: anote a semana com e sem os "
  "blocos curtos. Se os dois totais caem na faixa, a dúvida não muda a sua "
  "decisão.")
T("E se só um cai", "a diferença é sua para investigar",
  "E se só um deles cai, você sabe exatamente onde a dúvida mora, o que já é "
  "melhor do que repetir uma regra que talvez não valha mais.")
T("Isto é o oposto de opinião", "é uma divergência declarada",
  "Isto não é opinião contra opinião. É uma divergência entre documentos "
  "declarada em voz alta, que é o que se faz quando as fontes discordam.")

# ---------------------------------------- 6. Onde a conta para
T("Onde a conta para", "e ela para em vários lugares",
  "Onde esta conta para, porque ela para em vários lugares e prefiro dizer "
  "quais.",
  cap="Onde a conta para")
T("Ela não mede intensidade", "isso é sensação, não cronômetro",
  "Ela não resolve o que é moderado e o que é intenso para você. Isso depende "
  "do seu condicionamento, e nenhum cronômetro decide sozinho.")
I("Não há calorias aqui", "de propósito",
  "Não há nenhum número de calorias gastas neste material, de propósito. Isso "
  "varia demais entre pessoas para virar uma conta genérica.")
T("E não há promessa de peso", "nem em quilos nem em prazo",
  "E não há promessa de peso nenhuma, nem em quilos nem em prazo. As "
  "recomendações são de saúde, e não uma tabela de emagrecimento.")
I("Nem dose, nem prescrição", "esse nunca foi o assunto",
  "Não há dose, prescrição nem indicação aqui. Este canal aponta o que a "
  "instituição publicou e ensina você a conferir.")
T("E se há qualquer condição", "a conversa é com quem acompanha",
  "E se existe qualquer condição de saúde, gravidez, lesão ou tratamento em "
  "curso, a conversa é com quem acompanha o seu caso, antes de mudar qualquer "
  "coisa.")
T("Também não vale de um dia", "a unidade é a semana",
  "E repare que a unidade de tudo isto é a semana, não o dia. Um dia parado "
  "não estraga nada, e um dia heroico também não resolve.")
T("O que isto entrega", "é a sua semana em um número",
  "O que isto entrega é a sua própria semana convertida em um número "
  "comparável. Nada além disso, e já é bastante.")

# ---------------------------------------- 7. Sete dias
T("Sete dias", "e uma folha de papel",
  "Então o combinado desta semana é pequeno de propósito.",
  cap="Sete dias e uma folha")
L("Os três campos", ["minutos moderados",
                     "minutos intensos, que você vai dobrar",
                     "dias de fortalecimento"],
  "Uma folha com três campos: minutos moderados, minutos intensos, e dias de "
  "fortalecimento.")
T("Anote no dia", "não no domingo de memória",
  "Anote no próprio dia, e não no domingo tentando lembrar. Memória de semana "
  "inteira erra sempre para o mesmo lado.")
I("No sétimo dia", "dobre, some, compare",
  "No sétimo dia dobre a coluna intensa, some as duas, e compare com a "
  "faixa.")
T("E guarde a folha", "ela é o seu ponto de partida",
  "Guarde essa folha. Ela vira o ponto de partida da próxima, e comparar duas "
  "semanas suas vale mais que comparar a sua com a de qualquer outra pessoa.")
T("Uma semana não decide nada", "quatro já dizem alguma coisa",
  "Uma semana sozinha não decide nada. Quatro já mostram um padrão, e padrão "
  "é o que dá para mudar.")
T("E se o número vier baixo", "isso é informação, não veredito",
  "E se o número vier baixo, isso é informação e não um veredito sobre você. "
  "Até porque as duas rotas dizem a mesma coisa sobre começar: qualquer "
  "quantidade é melhor que nenhuma.")
C("Faça a folha hoje", "e conte quanto deu",
  "Comece a folha hoje e escreva nos comentários quanto deu a sua semana "
  "depois de dobrar a coluna intensa. Se conta feita com fonte oficial é o "
  "que você procura, se inscreva — aqui o número sempre vem de duas rotas, e "
  "quando elas discordam eu digo.")

SHORT = [
    {"layout": "titulo", "kicker": "A recomendação não é um número",
     "sub": "sao duas faixas",
     "nar": "A recomendação oficial de atividade física não é um número. São "
            "duas faixas, e a segunda quase ninguém cita.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Cento e cinquenta a trezentos",
     "sub": "ou setenta e cinco a cento e cinquenta",
     "nar": "Cento e cinquenta a trezentos minutos moderados por semana, ou "
            "setenta e cinco a cento e cinquenta intensos.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Se são equivalentes",
     "sub": "um minuto intenso vale dois",
     "nar": "Como as duas são equivalentes, um minuto intenso vale dois "
            "moderados. E aí está a conta.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Duas colunas",
     "sub": "dobre a intensa e some",
     "nar": "Escreva a sua semana em duas colunas, dobre a coluna intensa, "
            "some, e compare com a faixa.", "sem_cap": True},
    {"layout": "cta", "kicker": "E tem um terceiro campo",
     "sub": "que não é feito de minutos",
     "nar": "Tem ainda um terceiro campo, que não é feito de minutos, e ele "
            "está no vídeo completo aqui embaixo.", "sem_cap": True},
]

THUMB = {"l1": "Um minuto intenso", "l2": "vale dois"}

COPY = """# São duas faixas equivalentes, e a equivalência é uma conta que quase ninguém faz

## TITULO
Atividade Física: as Duas Faixas Oficiais, e Por Que um Minuto Intenso Vale Dois

## DESCRICAO
A recomendação oficial de atividade física para adultos não é um número — são duas faixas, e a maioria das pessoas só ouviu falar de uma delas. A conhecida é a moderada: de 150 a 300 minutos por semana. A outra é a intensa: de 75 a 150 minutos por semana, metade do tempo. E as duas são apresentadas como equivalentes.

É exatamente aí que mora a conta deste vídeo. Se metade do tempo entrega o mesmo, então um minuto de atividade intensa vale dois minutos de atividade moderada — e quem mistura os dois tipos na mesma semana, que é a maioria das pessoas, está somando errado. Um exemplo com números redondos: 90 minutos moderados mais 30 intensos somam 120 na conta crua, e parece que faltou. Dobrando os 30, a soma é 150, e a mesma semana passa a estar dentro da faixa.

O método são três passos, todos na sua própria semana e sem comprar nada: escreva os dias em duas colunas, minutos moderados de um lado e minutos intensos do outro, contando tudo que é movimento — trabalho, deslocamento a pé ou de bicicleta, tarefas de casa, lazer, não só academia. Multiplique a coluna intensa por dois. Some e compare com a faixa.

Há uma segunda exigência que escapa de quase toda conversa sobre o assunto, porque ela não é feita de minutos: atividades de fortalecimento muscular em pelo menos dois dias por semana. Repare na unidade — dias, não minutos. São duas contas diferentes e elas não se substituem: somar caminhada não resolve a parte de fortalecimento, e dois dias de força não preenchem a faixa de minutos.

Um capítulo inteiro é sobre um número que eu tinha para dar e não dei: a regra do bloco mínimo de dez minutos. Fui conferir e as próprias páginas da OMS divergem entre si — páginas mais antigas ainda trazem o bloco mínimo, que vem da recomendação de 2010, enquanto a diretriz de 2020 é comunicada como "cada movimento conta". Duas rotas que não batem, então o número não entra, e o vídeo conta o desacordo em vez de escolher um lado.

Este vídeo não substitui consulta médica, não promete perda de peso em quilos nem em prazo, e não traz dose, prescrição ou indicação.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz a folha de sete dias e escreve aqui quanto deu a tua semana depois de dobrar a coluna intensa — e, principalmente, qual dos três campos ficou mais vazio: os minutos moderados, os intensos, ou os dois dias de fortalecimento. Meu palpite é que o terceiro campo é o que mais falta e o que menos aparece nas conversas sobre o assunto, mas isso é palpite meu e eu queria ver o que sai de gente que fez a conta de verdade.

## HASHTAGS
#AtividadeFisica #SaudeComEvidencia #SejaMaisMagra

## TAGS
atividade fisica recomendacao, 150 minutos por semana, guia de atividade fisica, ministerio da saude atividade fisica, oms atividade fisica, atividade moderada e intensa, fortalecimento muscular dois dias, quanto exercicio por semana, saude com evidencia, guia atividade fisica brasil, como calcular minutos de exercicio, sedentarismo, saude publica brasil, exercicio e saude, checar fonte oficial

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 26 de agosto de 2026. As duas faixas e os dois dias foram conferidos em DUAS rotas institucionais independentes que se confirmam. (1) ORGANIZAÇÃO MUNDIAL DA SAÚDE (who.int): as "WHO guidelines on physical activity and sedentary behaviour", de 2020, e o comunicado "Every move counts towards better health". (2) MINISTÉRIO DA SAÚDE (gov.br/saude): o "Guia de Atividade Física para a População Brasileira", de 2021, produzido com a Universidade Federal de Pelotas e a Organização Pan-Americana da Saúde. As duas dizem o mesmo: para adultos, de 150 a 300 minutos semanais de atividade física moderada, ou de 75 a 150 minutos de atividade intensa, ou combinação equivalente; e atividades de fortalecimento muscular em pelo menos dois dias por semana.

AVISO SOBRE OS NÚMEROS — o que foi descartado e por quê. (a) O BLOCO MÍNIMO DE DEZ MINUTOS não entra, e este é o descarte principal desta edição: as próprias páginas da OMS divergem entre si. Páginas regionais mais antigas ainda trazem "bouts of at least 10 minutes", herança da recomendação de 2010, enquanto a diretriz de 2020 é comunicada sob a mensagem de que cada movimento conta. Como as duas rotas não batem no mesmo número, ele fica de fora, e o vídeo dedica um capítulo a explicar a divergência em vez de escolher um lado. (b) Não há nenhum número de CALORIAS gastas: varia demais entre pessoas para virar conta genérica. (c) Não há promessa de perda de peso, em quilos ou em prazo: as recomendações citadas são de saúde, não uma tabela de emagrecimento. (d) Não há dose, prescrição nem indicação de qualquer natureza. Este é conteúdo educativo e não substitui consulta médica; quem tem condição de saúde, gravidez, lesão ou tratamento em curso decide qualquer mudança com o profissional que acompanha o caso.
"""

SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-007",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#22303C", "c1": "#2E8B7A", "c2": "#D98324", "bg": "#F6F3EE"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "seja-mais-magra-007.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
