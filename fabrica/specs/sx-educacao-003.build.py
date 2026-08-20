#!/usr/bin/env python3
"""Monta a spec sx-educacao-003.

EIXO. O canal tem veredito `canal frio` — 7 shorts a 1,08 v/d de mediana e 6
longos a 0,00. A acao escrita para esse veredito e explicita: o problema nao e
o formato, e o gancho ou o eixo; arrisque um eixo novo.

O `pautas_banco` do nicho tem um agrupamento que domina os outliers e que o
canal NUNCA tocou: `ia-operando-a-planilha`. Seis outliers, de seis canais
DIFERENTES, entre 778,7 e 3.859,3 views/dia:

    Curso de Excel Online .... 3.859,3   ChatGPT na planilha
    Francysco Alcylandyo ..... 2.005,4   criar planilha com IA de graca
    Leticia Smirelli ......... 1.296,3   Claude no Power BI via MCP
    Guia do Excel ............ 1.115,7   Excel virar dashboard web com IA
    Joao Ernani ...............  803,9   controlador financeiro com IA
    Hashtag Treinamentos ......  778,7   dashboards automaticos no Gemini

Seis canais independentes batendo no mesmo eixo vale mais que um pico isolado.
Os dois eixos que o canal ja usou (licenca ociosa de Power BI, concurso contra
CLT) rendem 0,00 e 1,08 v/d.

A ESTRUTURA copiada e a dos seis, nao o assunto: PROMESSA DE ARTEFATO +
"de graca" + "sem precisar de X". O que muda e o gatilho — aqui existe uma DATA,
e ela e daqui a menos de um mes.

NUMEROS. Duas fontes que batem em cada um, uma institucional:

  A funcao =COPILOT do Excel sai do ar em 14 de setembro de 2026
    institucional .. Microsoft 365 Message Center MC1454373 e a pagina
                     "COPILOT Function" do Microsoft Support
    independente ... The Register (17/08/2026), TechRadar, Windows Central,
                     Neowin, XDA Developers — todos citando a mesma data

  Lancada em agosto de 2025, nunca chegou a versao geral; a GA estava
  prevista para janeiro de 2027
    TechRadar, Windows Central e The Register concordam

  Substituto: o painel lateral do Copilot no Excel, que exige licenca
    Microsoft Support e Microsoft Learn (pagina de licenciamento)

  Precos, lidos direto de microsoft.com/pt-br em 20/08/2026
    Microsoft 365 Copilot para Empresas .. R$ 120,20 usuario/mes (lista)
                                           R$ 103,03 anual, ate 300 usuarios
    Microsoft 365 Premium ................ R$ 109,00 por mes
    Microsoft 365 Personal ............... R$  51,00 por mes
    Microsoft 365 Family ................. R$  60,00 por mes
    segunda fonte dos R$ 109,00: MacMagazine e Gazz Conecta
    todos os precos de empresa sao SEM impostos, o proprio site diz

ACENTUACAO. As duas specs anteriores deste canal tem 0,00% de letras
acentuadas — portugues escrito em ASCII, que o TTS le errado ("e" no lugar de
"e" com acento, "esta" no lugar de "esta" com acento). O portao de ortografia
nao pegou porque ele compara a spec com as OUTRAS DO MESMO CANAL, e as duas
estao igualmente erradas: a referencia do canal e zero. Esta spec escreve
portugues de verdade, e o portao ganhou um piso por IDIOMA junto com ela.
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


# ------------------------------------------------------------------ cap 1
T("Catorze de setembro", "a fórmula sai do ar",
  "Catorze de setembro de dois mil e vinte e seis. Nessa data uma fórmula do "
  "Excel simplesmente deixa de existir, e se ela está numa planilha sua, é "
  "melhor você saber agora.",
  cap="A data que quase ninguém viu")
I("Qual fórmula", "igual COPILOT abre parênteses",
  "A fórmula é a COPILOT. Você digitava igual, COPILOT, e escrevia um pedido "
  "em português dentro da célula. A inteligência artificial respondia ali "
  "mesmo, como se fosse um cálculo.")
I("Quem avisou", "Message Center da Microsoft",
  "O aviso saiu no Message Center da própria Microsoft, com o código MC um "
  "quatro cinco quatro três sete três. Não é boato de fórum: é comunicado "
  "oficial para administradores.")
I("Quando saiu", "dezessete de agosto",
  "A imprensa técnica pegou no dia dezessete de agosto. The Register, "
  "TechRadar, Windows Central e Neowin publicaram a mesma data de "
  "desligamento, cada um por conta própria.")
I("O que acontece na data", "fórmula nova deixa de ser aceita",
  "A partir do dia catorze você não consegue mais criar uma fórmula nova com "
  "ela. E as que já existem param de devolver resposta.")
B("O tempo que sobra", ["Hoje", "Prazo"], [100, 22],
  "Daqui até lá são menos de quatro semanas.")
T("E tem uma segunda parte", "que ninguém está contando",
  "E existe uma segunda parte dessa história, que os avisos mencionam de "
  "passagem e que muda o custo da coisa toda.")
I("O substituto existe", "mas não é de graça",
  "A Microsoft diz que dá para continuar pelo painel lateral do Copilot no "
  "Excel. É verdade. O que o comunicado não destaca é que o painel exige "
  "licença paga.")
I("Quanto custa", "cento e vinte reais e vinte centavos",
  "O complemento Copilot para empresas está anunciado a cento e vinte reais "
  "e vinte centavos por usuário por mês, no site brasileiro da própria "
  "Microsoft.")
L("O que este vídeo faz", ["O que a fórmula fazia de verdade",
                           "Por que ela morreu antes de nascer",
                           "Quanto custa o substituto oficial",
                           "Três rotas que não cobram nada",
                           "A conta que decide o seu caso"],
  "Então vamos por partes: o que ela fazia, por que morreu antes de nascer, "
  "quanto custa o substituto, três rotas de graça e a conta do seu caso.")
I("Um aviso", "não vou vender ferramenta",
  "Um aviso que vale o vídeo inteiro. Não vendo ferramenta nenhuma nem digo "
  "que a paga é desperdício. Ponho os números lado a lado, porque a maioria "
  "decide com metade deles. Começando pelo que a fórmula fazia:")

# ------------------------------------------------------------------ cap 2
T("Dentro da célula", "não ao lado dela",
  "O detalhe que fazia a COPILOT ser diferente de tudo não era a "
  "inteligência artificial. Era o lugar onde ela morava: dentro da célula.",
  cap="O que a fórmula fazia dentro da célula")
I("A diferença", "a resposta era um valor",
  "Quando a resposta da inteligência artificial cai numa célula, ela vira um "
  "valor de planilha. Dá para arrastar, referenciar, somar, filtrar e usar "
  "numa tabela dinâmica.")
I("O caso mais comum", "classificar texto solto",
  "O uso mais comum era classificar texto. Trezentas respostas de pesquisa "
  "numa coluna, separadas em elogio, reclamação e dúvida. Uma fórmula "
  "arrastada para baixo.")
I("O segundo caso", "resumir em uma linha",
  "O segundo era resumir. Um campo de observação com cinco linhas de texto "
  "vira uma frase curta na coluna do lado, para caber no relatório sem "
  "ninguém ler tudo.")
I("O terceiro", "padronizar o que veio torto",
  "O terceiro era padronizar. Cidade digitada de dez jeitos, cargo em "
  "maiúscula e minúscula, telefone com e sem traço. O trabalho sujo de toda "
  "base real.")
I("Por que isso importava", "recalcula sozinho",
  "E como era fórmula, recalculava sozinho. Chegou linha nova na base, a "
  "classificação da linha nova aparece. Ninguém precisa lembrar de rodar "
  "nada.")
B("Onde estava o ganho", ["Copiar e colar", "Fórmula"], [100, 18],
  "Esse era o ganho de verdade. Não era a inteligência artificial responder "
  "melhor: era ela responder no lugar onde o dado já mora, sem ida e volta "
  "de copiar e colar.")
T("Só que", "ela nunca foi liberada para todo mundo",
  "Só que tem um ponto que muda a leitura de tudo isso. Ela nunca foi "
  "liberada para todo mundo.")
I("Quem tinha acesso", "Insider e Frontier",
  "Ela só funcionava para quem estava nos programas de teste da Microsoft, "
  "chamados Insider e Frontier. Quem usa o Excel normal do trabalho nunca "
  "viu essa fórmula funcionando.")
I("O que isso significa", "quase ninguém perde algo",
  "Isso tem um lado bom e um lado ruim. O lado bom é que quase ninguém tem "
  "planilha em produção dependendo dela. O lado ruim vem no próximo "
  "capítulo.")
I("A pergunta que fica", "por que testar e desistir",
  "Porque se ela nunca saiu do teste e já vai ser desligada, a pergunta não "
  "é o que fazer sem ela. É por que a Microsoft testou por um ano e "
  "desistiu:")

# ------------------------------------------------------------------ cap 3
T("Agosto de dois mil e vinte e cinco", "o começo",
  "A fórmula apareceu em agosto de dois mil e vinte e cinco, no canal de "
  "testes do Excel. Fazia doze meses que ela estava em avaliação.",
  cap="Por que ela morreu antes de nascer")
I("O plano original", "janeiro de dois mil e vinte e sete",
  "O plano anunciado era liberar para todo mundo em janeiro de dois mil e "
  "vinte e sete. Ou seja: ela é desligada quatro meses antes da data em que "
  "deveria estrear.")
B("A linha do tempo", ["Teste", "Estreia prevista"], [100, 0],
  "Um ano inteiro de teste, e a estreia foi cancelada no meio do caminho. "
  "É raro ver isso escrito com data, e é por isso que vale prestar atenção "
  "no motivo.")
I("O motivo declarado", "o painel faz o mesmo",
  "O motivo oficial é que o painel lateral do Copilot já faz as mesmas "
  "tarefas: resumir texto, classificar dados, gerar conteúdo e buscar "
  "informação na internet.")
I("O que isso diz", "uma porta só",
  "Lido de outro jeito: a Microsoft escolheu ter uma porta de entrada só "
  "para a inteligência artificial no Excel. E essa porta é o painel, não a "
  "barra de fórmulas.")
T("E a porta escolhida", "é a que tem licença",
  "E aqui as duas metades da história se encontram, porque a porta que "
  "sobrou é justamente a que cobra.")
I("O painel hoje", "licença Copilot obrigatória",
  "O painel, esse já tem regra publicada: precisa de licença Microsoft "
  "trezentos e sessenta e cinco Copilot. Está escrito na página de "
  "licenciamento da própria Microsoft.")
I("Não é acusação", "é sequência de fatos",
  "Não digo que uma coisa causou a outra. Digo o resultado: o caminho de "
  "teste fecha, e o que continua tem preço de tabela.")
I("Então vamos ao preço", "número por número",
  "E preço de tabela dá para conferir. É o que vem agora, número por número, "
  "direto do site brasileiro da Microsoft:")

# ------------------------------------------------------------------ cap 4
T("O preço oficial", "lido no site brasileiro",
  "Estes números foram lidos na página de preços da Microsoft do Brasil, em "
  "vinte de agosto de dois mil e vinte e seis. Eles mudam, e por isso a data "
  "importa mais que o valor.",
  cap="Quanto custa o substituto oficial")
I("Empresa", "cento e vinte reais e vinte centavos",
  "O complemento Copilot para empresas: cento e vinte reais e vinte centavos "
  "por usuário por mês, preço de lista.")
I("Com o desconto atual", "cento e três reais e três centavos",
  "Existe uma promoção que baixa para cento e três reais e três centavos por "
  "usuário por mês, na assinatura anual com renovação automática.")
I("Duas letras miúdas", "impostos e teto de usuários",
  "Duas observações que estão na mesma página. Os valores são sem impostos. "
  "E o complemento é limitado a trezentos usuários.")
I("Pessoa física", "os planos individuais",
  "Para quem paga sozinho a tabela é outra. O Premium sai por cento e nove "
  "reais por mês, e é o plano com os recursos de inteligência artificial "
  "completos.")
I("Os dois mais baratos", "cinquenta e um e sessenta",
  "Abaixo dele ficam o Personal, a cinquenta e um reais por mês, e o Family, "
  "a sessenta reais por mês para até seis pessoas.")
B("A escada", ["Personal", "Family", "Premium", "Empresa"],
  [42, 50, 91, 100],
  "Em ordem, os degraus são cinquenta e um, sessenta e cento e nove reais. "
  "O de empresa fica acima dos três.")
T("Agora a conta que interessa", "por ano e por equipe",
  "Um valor por mês parece pequeno. A conta que decide é sempre a de doze "
  "meses, e ela muda de tamanho quando tem equipe.")
I("Uma pessoa", "no ano",
  "Uma pessoa no plano de empresa, com o preço promocional, doze meses. "
  "Dá mil duzentos e trinta e seis reais por ano.")
I("Cinco pessoas", "no ano",
  "Agora uma equipe de cinco. Ainda com o desconto, seis mil cento e "
  "oitenta e um reais por ano.")
I("E sem o desconto", "sete mil duzentos e doze reais",
  "Sem o desconto, a mesma equipe de cinco custa sete mil duzentos e doze "
  "reais por ano. E sem impostos, lembrando.")
I("A pergunta certa", "vale para o seu uso",
  "Isso não é caro nem barato no vácuo. Fica caro ou barato quando você "
  "compara com o que a ferramenta faz por você. E é aí que a diferença entre "
  "fórmula e painel volta:")

# ------------------------------------------------------------------ cap 5
T("Não são a mesma coisa", "e a diferença é operacional",
  "Dizer que o painel faz o mesmo é verdade na lista de tarefas e mentira "
  "na rotina. A diferença não está no que a inteligência artificial "
  "responde, e sim em onde a resposta cai.",
  cap="Fórmula e painel não são a mesma coisa")
I("A fórmula", "resposta que é dado",
  "Na fórmula, a resposta nasce dentro da célula. Ela é um dado da planilha "
  "desde o primeiro instante, e todo o resto do Excel enxerga ela.")
I("O painel", "resposta que é texto",
  "No painel, a resposta nasce numa conversa ao lado. Você lê, decide, e leva "
  "para a planilha. Em muitos casos isso é ótimo. Em um caso específico, é "
  "ruim.")
I("O caso ruim", "a base que cresce",
  "O caso ruim é a base que recebe linha nova toda semana. Com fórmula, a "
  "linha nova já vem classificada. Com painel, alguém precisa lembrar de "
  "pedir de novo.")
B("Cem linhas novas por semana", ["Fórmula", "Painel"], [8, 100],
  "Numa base que ganha cem linhas por semana, a fórmula custa zero minuto de "
  "trabalho humano por semana. O painel custa alguns minutos, toda semana, "
  "para sempre.")
I("O que isso vira no ano", "quatro horas",
  "Cinco minutos por semana são quatro horas por ano. Não é catástrofe, mas "
  "é trabalho que não aparece em planilha de custo nenhuma.")
T("O outro lado", "onde o painel ganha",
  "E o painel ganha em coisa que a fórmula nunca fez bem, o que é justo "
  "registrar.")
I("Onde o painel é melhor", "tarefa que muda toda vez",
  "Tarefa que muda toda vez. Montar gráfico, reorganizar aba, escrever "
  "fórmula de uso único. Nada disso melhora sendo repetido sozinho.")
I("A regra prática", "repete ou não repete",
  "A regra prática cabe numa pergunta. A tarefa se repete sozinha quando "
  "chega dado novo? Se sim, você quer fórmula. Se não, o painel resolve "
  "igual ou melhor.")
I("Guarde essa pergunta", "ela decide o gasto",
  "Guarde essa pergunta, porque ela é quem decide se você precisa pagar "
  "alguma coisa. Agora as três rotas que não cobram nada:")

# ------------------------------------------------------------------ cap 6
T("Três rotas", "nenhuma delas cobra",
  "São três, e elas resolvem faixas diferentes do problema. Nenhuma é "
  "perfeita, e vou dizer o defeito de cada uma junto com o que ela faz bem.",
  cap="Três rotas que não cobram nada")
I("Rota um", "tabela de correspondência",
  "A primeira é a mais antiga e a mais subestimada: uma aba de "
  "correspondência com PROCX. Você lista os termos que aparecem e o que cada "
  "um vira, e a fórmula procura.")
I("Quando ela basta", "vocabulário fechado",
  "Ela basta quando o vocabulário é fechado: cidade, cargo, código. Nesses "
  "casos a inteligência artificial não é melhor, é mais cara e menos "
  "previsível.")
I("O defeito dela", "texto livre derruba",
  "O defeito aparece em texto livre de verdade. Uma resposta de pesquisa "
  "escrita por uma pessoa não cabe em tabela de correspondência, e aí você "
  "precisa da rota dois.")
I("Rota dois", "a inteligência artificial fora da célula",
  "A segunda é usar inteligência artificial gratuita fora do Excel. Você "
  "cola a coluna, pede a classificação e traz de volta. É o que a fórmula "
  "fazia, com um copiar e colar no meio.")
I("Por que isso serve", "o volume decide",
  "Se a base é atualizada uma vez por mês, esse copiar e colar custa dois "
  "minutos por mês. Ninguém assina licença anual por isso.")
I("O cuidado obrigatório", "dado de pessoa não sai da empresa",
  "E um cuidado que não é opcional. Dado de cliente, de paciente ou de "
  "funcionário não sai da empresa para ferramenta pessoal. Aí é a rota um, "
  "ou é a licença corporativa.")
I("Rota três", "peça a fórmula, não a resposta",
  "A terceira é a que mais gente esquece. Em vez de pedir a resposta para a "
  "inteligência artificial, peça a FÓRMULA. Descreva o que você quer e peça "
  "o cálculo pronto para colar.")
I("Por que essa é a melhor", "roda sozinha depois",
  "É a melhor das três para base que cresce, porque o que fica na planilha é "
  "fórmula comum. Recalcula sozinha, sem internet e sem licença.")
I("O defeito da rota três", "você precisa conferir",
  "O defeito é que fórmula gerada por inteligência artificial erra, e erra "
  "calada. Testar em dez linhas conhecidas antes de aplicar em dez mil é o "
  "mínimo.")
B("As três, lado a lado", ["PROCX", "IA fora", "IA escreve fórmula"],
  [30, 55, 100],
  "Compare pelo que sobra na planilha depois. O PROCX deixa tabela. A "
  "inteligência artificial por fora deixa valor colado. A que escreve "
  "fórmula deixa cálculo que continua trabalhando.")
I("E se você já paga", "não jogue fora",
  "E se a sua empresa já tem a licença, nada disso é motivo para largar. O "
  "painel é bom. O ponto é que ele não deveria ser a única resposta possível "
  "para quem não tem.")
T("Falta uma coisa", "decidir com número",
  "Falta a parte que este canal nunca pula: transformar isso numa conta que "
  "você faz com os seus próprios números.")

# ------------------------------------------------------------------ cap 7
T("Seis linhas", "e a decisão sai sozinha",
  "A planilha de decisão tem seis linhas. Cada uma é um número que você já "
  "tem ou consegue estimar em cinco minutos.",
  cap="A conta que decide o seu caso")
I("Linha um", "quantas pessoas usariam",
  "Linha um: quantas pessoas na sua equipe realmente usariam a inteligência "
  "artificial no Excel toda semana. Não quantas têm Excel aberto: quantas "
  "usariam.")
I("Linha dois", "o custo anual por pessoa",
  "Linha dois: o custo anual por pessoa. Com o preço promocional de hoje, "
  "mil duzentos e trinta e seis reais e trinta e seis centavos, ainda sem "
  "impostos.")
I("Linha três", "quantas tarefas se repetem",
  "Linha três: quantas das tarefas se repetem sozinhas quando chega dado "
  "novo. É a pergunta do capítulo cinco, agora virando número.")
I("Linha quatro", "minutos por semana sem a licença",
  "Linha quatro: quantos minutos por semana custaria fazer essas mesmas "
  "tarefas pela rota gratuita. Meça uma vez, com relógio, em vez de chutar.")
I("Linha cinco", "o seu custo por hora",
  "Linha cinco: o seu custo por hora. Salário mensal dividido por cento e "
  "setenta e seis horas é uma aproximação boa o bastante para esta conta.")
I("Linha seis", "há dado sensível",
  "Linha seis é sim ou não, e ela tem poder de veto. Existe dado pessoal na "
  "base? Se existir, a rota gratuita externa sai da mesa e a conta muda de "
  "figura.")
B("O cruzamento", ["Custo da licença", "Custo do tempo"], [100, 38],
  "O resultado é uma comparação só: o custo anual da licença contra o custo "
  "anual do tempo. E na maioria das equipes pequenas o tempo perde por "
  "margem larga.")
I("Onde ela vira", "equipe grande e tarefa repetitiva",
  "Ela vira quando as duas coisas acontecem juntas: muita gente e muita "
  "tarefa que se repete. Aí o tempo passa a licença e pagar é o certo.")
I("O erro comum", "decidir pela manchete",
  "O erro que este vídeo evita é decidir pela manchete. Nem assinar porque "
  "saiu recurso novo, nem recusar por princípio. A conta acima leva menos de "
  "dez minutos.")
I("Se você fizer só uma coisa", "meça os minutos",
  "Se fizer só uma coisa depois deste vídeo, faça a linha quatro. Meça com "
  "relógio o tempo da rota gratuita por semana. Esse número sozinho responde "
  "metade da pergunta.")
C("SX Educação", "toda semana, com a conta na tela",
  "E antes do dia catorze, procure COPILOT na barra de fórmulas das suas "
  "planilhas. Leva um minuto. Se este vídeo te poupou uma assinatura, "
  "inscreve no canal.")

# ------------------------------------------------------------------ short
#
# Ele resolve sozinho: data, o que morre, o que custa o substituto e a rota
# gratuita que serve para base que cresce. O longo entra como continuacao
# opcional, nunca como condicao para a coisa fazer sentido (regra critica:
# "short que so aponta para o longo e trailer, nao short").
SHORT = [
    {"layout": "titulo", "kicker": "14 de setembro", "sub": "a fórmula morre",
     "nar": "Catorze de setembro: a fórmula COPILOT do Excel sai do ar.",
     "sem_cap": True},
    {"layout": "item", "kicker": "O que ela fazia",
     "preco": "IA dentro da célula",
     "nar": "Ela punha inteligência artificial dentro da célula, e "
            "recalculava sozinha.", "sem_cap": True},
    {"layout": "item", "kicker": "O substituto", "preco": "R$ 120,20 por mês",
     "nar": "O substituto é o painel lateral, e exige licença: cento e vinte "
            "reais por usuário por mês.", "sem_cap": True},
    {"layout": "item", "kicker": "A rota grátis",
     "preco": "peça a fórmula, não a resposta",
     "nar": "A saída de graça é pedir a FÓRMULA para a inteligência "
            "artificial, e não a resposta.", "sem_cap": True},
    {"layout": "item", "kicker": "Por que funciona", "preco": "roda sozinha",
     "nar": "Fórmula colada recalcula sozinha quando chega linha nova. Sem "
            "licença. Confira em dez linhas antes.", "sem_cap": True},
    {"layout": "cta", "kicker": "SX Educação", "sub": "confira hoje",
     "nar": "Procure COPILOT nas suas planilhas antes do dia catorze.",
     "sem_cap": True},
]


COPY = """# =COPILOT sai do ar em 14 de setembro: o que colocar no lugar

## TITULO
Excel: a Funcao COPILOT Sai do Ar em 14 de Setembro. O Que Colocar no Lugar

## DESCRICAO
Em 14 de setembro de 2026 a funcao =COPILOT do Excel deixa de existir. O aviso saiu no Message Center da propria Microsoft, sob o codigo MC1454373, e foi repercutido no dia 17 de agosto por The Register, TechRadar, Windows Central e Neowin — todos citando a mesma data.

Se voce nunca viu essa formula funcionando, ha um motivo: ela nunca saiu do teste. Apareceu em agosto de 2025 nos programas Insider e Frontier, tinha estreia geral marcada para janeiro de 2027, e vai ser desligada quatro meses ANTES de estrear. Isso tem um lado bom — quase ninguem tem planilha em producao dependendo dela — e um lado que quase nenhum aviso destaca.

O lado que ninguem destaca e o preco do substituto. A Microsoft diz que voce pode continuar usando IA no Excel pelo painel lateral do Copilot, e isso e verdade. O que ela nao poe no mesmo paragrafo e que o painel exige licenca. Lido na pagina brasileira da Microsoft em 20/08/2026: o complemento Microsoft 365 Copilot para Empresas custa R$ 120,20 por usuario/mes de preco de lista, ou R$ 103,03 na assinatura anual — sem impostos, limitado a 300 usuarios. Do lado individual, o Microsoft 365 Premium sai por R$ 109,00/mes, contra R$ 51,00 do Personal e R$ 60,00 do Family.

O QUE TEM DENTRO:

O que a formula fazia de verdade, e por que o lugar dela importava mais que a IA. Resposta que nasce dentro da celula vira DADO de planilha: da para arrastar, referenciar, somar e usar em tabela dinamica. Resposta que nasce no painel vira texto numa conversa ao lado, que alguem precisa levar para a planilha na mao.

A diferenca operacional entre os dois, que a lista de tarefas esconde. Numa base que recebe 100 linhas novas por semana, a formula custa zero minuto de trabalho humano por semana; o painel custa alguns minutos, toda semana, para sempre. Cinco minutos por semana sao quatro horas por ano que nao aparecem em planilha de custo nenhuma.

Tres rotas que nao cobram nada, com o defeito de cada uma dito junto com o que ela faz bem. (1) Tabela de correspondencia com PROCX, para vocabulario fechado — nesses casos a IA e mais cara e menos previsivel, nao melhor. (2) IA gratuita fora do Excel, para base atualizada uma vez por mes — com o cuidado obrigatorio: dado de cliente, paciente ou funcionario nao sai da empresa para ferramenta pessoal. (3) Pedir a FORMULA em vez da resposta — a melhor das tres para base que cresce, porque o que fica na planilha e um calculo comum que recalcula sozinho, sem internet e sem licenca.

A planilha de decisao de seis linhas: quantas pessoas usariam de fato, custo anual por pessoa, quantas tarefas se repetem sozinhas, minutos por semana pela rota gratuita, seu custo por hora, e se ha dado sensivel na base. A ultima linha tem poder de veto.

SE VOCE SO FIZER UMA COISA: antes do dia 14, procure COPILOT na barra de formulas das suas planilhas. Leva um minuto e evita a surpresa de achar erro no meio de um relatorio.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Duas perguntas para quem chegou ate aqui: voce chegou a usar a =COPILOT em alguma planilha de verdade, ou so viu falar dela? E qual das tres rotas gratuitas resolve o SEU caso — PROCX, IA por fora, ou pedir a formula pronta? Estou juntando as respostas para um video so sobre a rota tres, que e a que mais gente subestima.

## HASHTAGS
#Excel #Copilot #SXEducacao

## TAGS
excel, copilot excel, funcao copilot, microsoft 365 copilot, excel com ia, ia no excel, planilha com ia, formula excel, procx, power bi, analise de dados, produtividade excel, excel 2026, copilot preco, automatizar planilha

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao > 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
A data de 14 de setembro de 2026 para o desligamento da funcao =COPILOT vem do Microsoft 365 Message Center, aviso MC1454373, e da pagina "COPILOT function" do Microsoft Support; foi conferida contra a cobertura independente de The Register, TechRadar, Windows Central, Neowin e XDA Developers publicada em 17/08/2026, todas com a mesma data. O historico da funcao (lancada em agosto de 2025 nos programas Insider e Frontier, disponibilidade geral prevista para janeiro de 2027 e nunca alcancada) vem das mesmas fontes. Os precos foram lidos em 20/08/2026 nas paginas brasileiras da Microsoft: R$ 120,20 e R$ 103,03 por usuario/mes para o complemento Microsoft 365 Copilot para Empresas (sem impostos, ate 300 usuarios, assinatura anual com renovacao automatica), e R$ 51,00, R$ 60,00 e R$ 109,00 por mes para Microsoft 365 Personal, Family e Premium. Preco de software muda sem aviso e varia por regiao, revendedor e regime tributario — confira o valor vigente antes de decidir, e por isso a planilha deste video nunca traz esses numeros dentro de formula: eles vao em celula, para voce atualizar. As contas de 12 meses e de equipe de cinco servem para mostrar a mecanica da comparacao, nao para prever o custo de ninguem. Este conteudo e educativo sobre Excel e decisao de ferramenta; nao e recomendacao de compra nem orientacao juridica sobre licenciamento.
"""


def _copy_existente():
    """Le a copy do .json ao lado, se ele ja existir. A copy real nasce depois
    do render, com os tempos de capitulo medidos; reconstruir daqui a apagaria.
    """
    import os
    alvo = "fabrica/specs/sx-educacao-003.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "sx-educacao",
    "pacote": "sx-educacao-003",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#10261C", "c1": "#217346", "c2": "#F2B134",
               "bg": "#F1F7F4"},
    "thumb": {"l1": "=COPILOT morre", "l2": "14 de setembro"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/sx-educacao-003.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ensaio import duracao_estimada, duracao_estimada_short
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
