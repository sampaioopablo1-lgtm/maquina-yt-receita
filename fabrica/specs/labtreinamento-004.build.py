#!/usr/bin/env python3
"""Monta a spec labtreinamento-004.

CANAL. Veredito `sem dado`: 2 shorts e 2 longos medidos, 23 views no acervo. A
regra do veredito manda seguir a memoria do NICHO, e nao a propria — que aqui
nao tem o que dizer. O nicho autoriza a faixa inteira: longos de concorrente
medem 78,0 v/d de mediana com topo em 695,2.

EIXO. Os quatro titulos publicados sao TRES planilhas de Excel (NR-1 duas
vezes, ISO 9001 uma) e um short de NR-1. O eixo `nr-tecnica` nunca foi usado, e
ele e o mais consistente do banco deste canal: tres videos do mesmo concorrente
sobre atualizacao de norma, medindo 79,3, 68,8 e 66,1 v/d — nao um pico, uma
FAIXA. Faixa estreita com n=3 vale mais que um topo solitario.

  (O banco marca `nr1-psicossociais` com zero usados. Esta errado: duas das
  planilhas publicadas sao exatamente disso. E o mesmo buraco do aprendizado
  409 visto do outro lado — la eu marquei demais, aqui ninguem marcou nada.
  Nao usei o rotulo como prova; li os titulos publicados.)

FORMATO. A estrutura dos tres outliers e a mesma: "NR-X ATUALIZADA:
<consequencia concreta>". Palavra-chave primeiro, consequencia no lugar do
assunto. "NR-10 Atualizada: Os Erros Que Estao Gerando Multas nas Empresas"
mede 68,8; "NR 35 ATUALIZADA: O Que Muda no Treinamento em Altura", 79,3. E a
estrutura copiada aqui. O assunto e outro.

A PAUTA, datada e com fonte institucional.

  Portaria MTE no 737, de 29 de maio de 2026, publicada no DOU em 1o de junho
  de 2026, aprova o novo texto da NR-10 — Seguranca em Instalacoes Eletricas.
  O PDF da portaria esta hospedado no proprio gov.br.

    transicao ......... 12 meses
    vigencia .......... 1o de junho de 2027
    substitui ......... integralmente as Portarias MTE 598/2004 e MTPS 508/2016
    muda o que ........ prioriza DESENERGIZACAO sobre EPI
                        reconhece ARCO ELETRICO como exigencia, com EPI por
                        categoria e, em alguns casos, estudo de energia incidente
                        integra o risco eletrico ao GRO/PGR

  Conferido em duas passagens de busca com veiculos independentes que batem, e
  uma delas aponta para o arquivo no gov.br. Data de hoje: 20 de agosto de
  2026 — restam pouco mais de nove meses de transicao.

A DOR: nove meses parece muito e nao e, porque o que a norma nova exige nao se
resolve com treinamento — exige levantamento, projeto e, em parte dos casos,
estudo de engenharia. Quem comecar em maio de 2027 nao termina.

O QUE O VIDEO NAO FAZ: nao lista artigo por artigo da norma, nao diz quanto
custa um estudo de energia incidente (varia demais para um numero honesto) e
nao promete que a fiscalizacao vai apertar em tal mes.
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


# ------------------------------------------------------------------- cap 1
T("Nove meses", "e não é muito",
  "A NR dez inteira foi reescrita, e a sua empresa tem pouco mais de nove "
  "meses para se adequar. Parece bastante. Não é.",
  cap="Nove meses, e por que não é muito")
I("Qual norma", "instalações elétricas",
  "Estamos falando da norma que rege segurança em instalações e serviços com "
  "eletricidade. A que trata de quem trabalha energizado, de quem projeta e de "
  "quem autoriza.")
I("O que aprovou", "Portaria setecentos e trinta e sete",
  "O texto novo veio pela Portaria do Ministério do Trabalho e Emprego número "
  "setecentos e trinta e sete, assinada em vinte e nove de maio deste ano.")
I("Quando foi publicada", "primeiro de junho",
  "Ela saiu no Diário Oficial da União em primeiro de junho, e o arquivo está "
  "no site do próprio Ministério. Não é interpretação de ninguém.")
I("Quando passa a valer", "junho de dois mil e vinte e sete",
  "A transição é de doze meses. O texto novo passa a valer em primeiro de "
  "junho do ano que vem.")
I("O que ela substitui", "duas portarias antigas",
  "E ela não emenda o texto anterior: substitui por inteiro o que valia desde "
  "dois mil e quatro, com a revisão de dois mil e dezesseis.")
I("Por que isso importa", "não dá para comparar linha a linha",
  "Substituição integral muda a forma de estudar. Não adianta procurar o que "
  "mudou comparando parágrafo com parágrafo, porque o texto foi reescrito, não "
  "remendado. O caminho é ler o novo inteiro.")
I("Quanto tempo isso leva", "uma tarde",
  "Ler a norma inteira leva uma tarde. Descobrir o que ela exige da sua "
  "instalação leva meses, e é essa segunda parte que o prazo cobra.")
T("Por que nove meses é pouco", "não é treinamento",
  "Agora a parte que decide se você vai chegar no prazo ou não.")
I("O engano comum", "achar que é curso",
  "Muita gente lê atualização de norma e pensa em reciclagem de treinamento. "
  "Marca o curso, tira a lista de presença e considera resolvido.")
I("Aqui não resolve", "levantamento e projeto",
  "Nesta aqui não resolve. Parte do que mudou exige levantamento em campo, "
  "revisão de projeto e, em alguns casos, estudo de engenharia.")
I("A conta do calendário", "quem começa tarde não termina",
  "Levantamento, projeto e estudo não são coisas de duas semanas. Quem começar "
  "em maio do ano que vem não termina em junho.")
I("E tem fila", "todo mundo no mesmo prazo",
  "Some a isso uma coisa que quase ninguém considera: o prazo é o mesmo para "
  "todo mundo. Quem fornece estudo de engenharia vai ter fila nos últimos "
  "meses, e fila não se resolve com urgência.")
B("Quando a demanda aparece", ["Agosto de 2026", "Abril de 2027"], [18, 100],
  "A procura por quem faz esse trabalho não é constante ao longo do prazo. Ela "
  "se concentra no fim, e é justamente quando você vai precisar.")
L("O que vem agora", ["As três mudanças que pesam",
                      "O que fazer nos próximos noventa dias",
                      "Quem a norma alcança",
                      "O que eu não vou te dizer"],
  "Então vamos ver as três mudanças que realmente pesam, o que dá para fazer "
  "nos próximos noventa dias, quem exatamente a norma alcança, e o que eu não "
  "vou te dizer aqui.")
I("Começando pela primeira", "a que inverte a lógica",
  "Começando pela mudança que inverte a lógica de decisão no campo:")

# ------------------------------------------------------------------- cap 2
T("Desenergizar primeiro", "o EPI vem depois",
  "A primeira mudança: o texto novo prioriza a desenergização sobre o "
  "equipamento de proteção individual.",
  cap="Mudança um: desenergizar vem primeiro")
I("O que isso quer dizer", "ordem de preferência",
  "Na prática, isso estabelece uma ordem. A pergunta deixa de ser qual EPI "
  "usar, e passa a ser se dava para desligar.")
I("E se não dava", "precisa justificar",
  "Se não dava para desligar, isso precisa estar justificado — não é uma "
  "escolha de conveniência do time em campo.")
I("Por que isso é grande", "muda o registro",
  "É grande porque muda o que fica registrado. O documento deixa de provar "
  "que havia EPI e passa a precisar provar que a energização era necessária.")
B("A ordem que a norma quer", ["Desenergizar", "Se não der: proteger"],
  [100, 55],
  "Desenergizar primeiro. Só depois, e com justificativa, trabalhar protegido.")
I("Quem sente primeiro", "manutenção",
  "Quem sente isso primeiro é a manutenção, porque desligar quase sempre "
  "significa parar produção. E aí a conversa sai da segurança e entra no "
  "planejamento.")
I("O conflito real", "produção contra parada",
  "É um conflito real e não adianta fingir que não existe. Parar uma linha "
  "custa dinheiro medido em hora, e a justificativa de trabalhar energizado "
  "costuma nascer dessa conta.")
I("O que muda na conversa", "a conta vai para o papel",
  "O que muda é que essa conta passa a precisar estar escrita. Não é proibido "
  "trabalhar energizado; é obrigatório registrar por que não deu para desligar.")
I("Quem assina", "e é aí que aperta",
  "E alguém assina esse registro. Quando a justificativa sai do subentendido e "
  "vira documento assinado, a decisão muda de qualidade — em geral para melhor.")
I("O que fazer com isso", "olhar as ordens de serviço",
  "O trabalho prático aqui é olhar as ordens de serviço que hoje autorizam "
  "trabalho energizado e perguntar, uma por uma, se a justificativa está "
  "escrita ou está subentendida.")
I("Subentendida não serve", "é o ponto",
  "Subentendida não serve, e esse é exatamente o ponto da mudança.")
I("Um teste rápido", "pergunte ao eletricista",
  "Um teste que você pode fazer amanhã: pergunte a quem executa por que aquele "
  "serviço é feito energizado. Se a resposta for sempre foi assim, você "
  "encontrou uma das linhas do seu plano.")
I("Próxima mudança", "a que exige cálculo",
  "A segunda mudança é a que traz cálculo para dentro da norma:")

# ------------------------------------------------------------------- cap 3
T("Arco elétrico", "virou exigência",
  "Segunda mudança: o arco elétrico passa a ser tratado como exigência, e não "
  "como assunto de curso avançado.",
  cap="Mudança dois: arco elétrico com categoria")
I("O que é o arco", "não é choque",
  "E vale separar, porque muita gente mistura. Arco elétrico não é choque. É a "
  "liberação de energia em forma de calor e pressão quando a corrente encontra "
  "caminho pelo ar.")
I("Por que separar importa", "o EPI é outro",
  "Importa porque a proteção é outra. O que protege de choque não protege de "
  "queimadura por arco.")
I("O que o arco faz", "calor e pressão",
  "O arco libera calor suficiente para queimar através de roupa comum, e "
  "pressão suficiente para arremessar quem está perto. São dois danos "
  "diferentes acontecendo no mesmo instante.")
I("Por isso categoria", "não é sim ou não",
  "Por isso a proteção não é sim ou não: é por nível. Uma vestimenta adequada "
  "para um ponto da instalação pode ser insuficiente em outro, na mesma "
  "empresa e no mesmo dia.")
I("O que a norma pede", "EPI por categoria",
  "O texto novo trabalha com EPI por categoria — ou seja, o equipamento "
  "precisa corresponder ao nível de energia daquele ponto da instalação.")
I("E como se sabe o nível", "estudo de energia incidente",
  "E para saber o nível, em parte dos casos é preciso estudo de energia "
  "incidente. Isso é cálculo de engenharia sobre a instalação real.")
I("Aqui está o prazo", "estudo não é rápido",
  "É aqui que os nove meses apertam. Estudo de energia incidente depende de "
  "levantar a instalação como ela está, não como está no projeto antigo.")
I("Por que a diferença importa", "projeto e realidade divergem",
  "E em instalação com anos de operação essas duas coisas quase nunca "
  "coincidem. Cada ampliação, cada troca de equipamento e cada reforma "
  "afastaram um pouco a planta do papel.")
I("O trabalho invisível", "atualizar o unifilar",
  "Então boa parte do esforço não é o cálculo em si: é atualizar o diagrama "
  "unifilar até ele descrever a instalação que existe. Isso é campo, não "
  "escritório.")
T("Um aviso honesto", "não vou dar preço",
  "E aqui eu vou te dever uma informação, de propósito.")
I("Por que não digo o preço", "varia demais",
  "Não vou dizer quanto custa esse estudo. O valor varia com o tamanho da "
  "instalação e com o estado da documentação, e um número médio aqui "
  "enganaria mais do que ajudaria.")
I("O que dá para dizer", "peça três orçamentos",
  "O que dá para dizer com segurança: peça pelo menos três orçamentos, e "
  "compare o escopo antes do preço.")
I("Terceira mudança", "a que junta tudo",
  "A terceira mudança é a que costura as outras duas ao que você já faz:")

# ------------------------------------------------------------------- cap 4
T("Risco elétrico no GRO", "deixa de ser ilha",
  "Terceira mudança: o risco elétrico passa a estar integrado ao gerenciamento "
  "de riscos ocupacionais.",
  cap="Mudança três: o elétrico entra no GRO")
I("O que isso muda", "sai do documento separado",
  "Até aqui, o elétrico vivia num documento próprio, com vida própria, muitas "
  "vezes atualizado por gente diferente de quem cuida do resto.")
I("Agora", "mesmo inventário",
  "Agora ele entra no mesmo inventário de riscos que o resto da empresa, com o "
  "mesmo plano de ação.")
I("Por que isso é bom", "para de contradizer",
  "Isso é bom por um motivo prático: para de existir a situação em que dois "
  "documentos da mesma empresa dizem coisas diferentes sobre o mesmo risco.")
I("Isso acontece mais do que parece", "auditoria encontra",
  "E acontece bastante. Em auditoria é comum aparecer um risco elétrico "
  "classificado de um jeito no documento da área e de outro no inventário "
  "geral, sem que ninguém tivesse notado.")
I("Qual dos dois vale", "a pergunta que ninguém quer",
  "Quando isso aparece, a pergunta seguinte é qual dos dois vale — e não existe "
  "resposta boa. Integrar os dois é o que faz essa pergunta deixar de existir.")
I("E por que dá trabalho", "os dois precisam conversar",
  "E dá trabalho pelo mesmo motivo. Se o inventário e o documento elétrico "
  "nunca conversaram, alguém vai ter que sentar e conciliar os dois.")
B("Antes e depois", ["Documentos separados", "Um inventário só"], [100, 100],
  "Não é mais documento, é o mesmo documento. O volume não muda; o que muda é "
  "que agora existe uma versão só da verdade.")
I("Quem faz isso", "quem já faz o PGR",
  "Na maioria das empresas isso cai para quem já cuida do PGR, e é comum essa "
  "pessoa não ser a mesma que assina a parte elétrica.")
I("O primeiro passo", "descobrir quem são os dois",
  "Então o primeiro passo é banal e quase sempre pulado: descobrir quem são "
  "essas duas pessoas e colocar as duas na mesma sala.")
I("Agora o prático", "noventa dias",
  "Com as três mudanças na mesa, o que dá para fazer nos próximos noventa "
  "dias:")

# ------------------------------------------------------------------- cap 5
T("Quatro passos", "nos próximos noventa dias",
  "Quatro passos para os próximos noventa dias. Nenhum deles depende de "
  "orçamento aprovado.",
  cap="O que fazer nos próximos noventa dias")
I("Passo um", "baixar a portaria",
  "Primeiro: baixe a portaria no site do Ministério do Trabalho. O texto "
  "oficial é gratuito, e ler a fonte evita depender de resumo de terceiro — "
  "inclusive deste aqui.")
I("Passo dois", "listar trabalhos energizados",
  "Segundo: liste todos os trabalhos energizados que a empresa faz hoje, com a "
  "justificativa de cada um. Se a justificativa não existe por escrito, "
  "anote isso também.")
I("Por que essa lista", "ela vira o plano",
  "Essa lista é o que vira seu plano. Cada linha sem justificativa escrita é "
  "uma tarefa, e você já sabe quantas são.")
I("Passo três", "mapear onde falta estudo",
  "Terceiro: identifique em quais pontos da instalação você não sabe o nível "
  "de energia incidente. Não precisa calcular agora — precisa saber onde falta.")
I("Passo quatro", "juntar as duas pessoas",
  "Quarto: marque uma reunião entre quem mantém o inventário de riscos e quem "
  "responde pela parte elétrica. Uma hora, com as duas listas na mesa.")
I("O que sai dessa reunião", "a lista de divergências",
  "O produto dessa hora não é um plano. É uma lista de divergências entre os "
  "dois documentos — e essa lista é mais útil que qualquer cronograma feito "
  "antes de conhecê-la.")
T("Um erro de sequência", "comum e caro",
  "E aqui cabe um aviso sobre a ordem em que as empresas costumam fazer isso.")
I("O erro", "contratar antes de saber",
  "O erro comum é contratar o estudo de engenharia primeiro, antes de saber "
  "quais pontos realmente precisam dele.")
I("Por que sai caro", "escopo inflado",
  "Sai caro porque o escopo vira a instalação inteira, quando talvez metade "
  "dela não exigisse. E o fornecedor não tem como saber isso por você.")
I("A ordem certa", "levantar, depois contratar",
  "A ordem que funciona é a inversa: levantar primeiro, descobrir onde falta, e "
  "só então pedir orçamento com escopo definido. Os passos dois e três deste "
  "vídeo existem exatamente para isso.")
T("O que eu não vou te dizer", "três coisas",
  "E encerro com três coisas que eu não vou te dizer, porque não sei.")
I("Primeira", "artigo por artigo",
  "Não vou percorrer a norma artigo por artigo. Ela substitui um texto de duas "
  "décadas, e um resumo falado não substitui a leitura.")
I("Segunda", "quanto custa",
  "Não vou dizer quanto custa a adequação. Depende do estado da sua "
  "instalação, e quem te der um número sem olhar está chutando.")
I("Terceira", "quando a fiscalização aperta",
  "E não vou dizer quando a fiscalização vai apertar. O que eu sei é a data em "
  "que o texto passa a valer, e essa data é primeiro de junho do ano que vem.")
I("Por que não estimo isso", "seria chute com voz firme",
  "Poderia dar um palpite e ele soaria bem, porque palpite dito com voz firme "
  "soa igual a informação. Mas você tomaria decisão de orçamento com base "
  "nele, e eu não tenho como sustentá-lo.")
I("O que fazer com a incerteza", "trate a data como o prazo",
  "O jeito prático de lidar com isso é simples: trate a data de vigência como "
  "se fosse a data da cobrança. Ela é a única que está escrita.")
T("Quem a norma alcança", "quatro palavras que confundem",
  "Antes de fechar, um trecho de vocabulário que confunde muita gente e "
  "atravessa tudo o que falamos.",
  cap="Quem a norma alcança")
I("A norma separa pessoas", "por autorização e formação",
  "A NR dez não trata todo mundo igual. Ela separa quem pode fazer o quê a "
  "partir de formação e de autorização formal da empresa.")
I("Habilitado", "registro no conselho",
  "Profissional habilitado é quem tem formação em engenharia elétrica com "
  "registro no conselho de classe. É quem pode projetar e assinar.")
I("Qualificado", "curso específico reconhecido",
  "Qualificado é quem comprova curso específico na área elétrica reconhecido "
  "pelo sistema oficial de ensino.")
I("Capacitado", "trabalha sob supervisão",
  "Capacitado é quem trabalha sob supervisão de habilitado ou qualificado, e "
  "com autorização da empresa.")
I("Autorizado", "a empresa designou por escrito",
  "E autorizado é a camada que muita empresa esquece: é o ato formal da "
  "empresa designando aquela pessoa para aquele serviço.")
B("Onde mora a falha comum", ["Tem treinamento", "Tem autorização escrita"],
  [100, 45],
  "A falha mais comum que eu vejo não é falta de treinamento — é ter "
  "treinamento e não ter a autorização registrada.")
I("Por que isso liga com o resto", "quem assina a justificativa",
  "E isso conecta com a primeira mudança: se trabalhar energizado passa a "
  "exigir justificativa registrada, alguém autorizado precisa estar do outro "
  "lado da assinatura.")
I("O que conferir hoje", "a lista de autorizados",
  "Então vale conferir se a sua lista de autorizados existe, está atualizada e "
  "corresponde a quem de fato executa. Em muitas empresas ela envelheceu.")
C("LabTreinamento", "norma com data, não com achismo",
  "Faça hoje só o passo dois: liste os trabalhos energizados e marque quais "
  "não têm justificativa escrita. Se este vídeo te poupou tempo, inscreva-se.")


# -------------------------------------------------------------------- short
#
# Entrega sozinho: a data, as tres mudancas em uma frase cada e a acao. O longo
# e continuacao opcional, nunca condicao.
SHORT = [
    {"layout": "titulo", "kicker": "NR-10 reescrita",
     "sub": "prazo: junho de 2027",
     "nar": "A NR dez foi reescrita inteira, e o prazo para se adequar termina "
            "em junho do ano que vem.", "sem_cap": True},
    {"layout": "item", "kicker": "O que aprovou", "preco": "Portaria 737/2026",
     "nar": "Portaria do Ministério do Trabalho número setecentos e trinta e "
            "sete, publicada em primeiro de junho.", "sem_cap": True},
    {"layout": "item", "kicker": "Muda 1", "preco": "desenergizar antes do EPI",
     "nar": "Primeira mudança: desenergizar vem antes do EPI, e trabalhar "
            "energizado precisa de justificativa escrita.", "sem_cap": True},
    {"layout": "item", "kicker": "Muda 2", "preco": "arco elétrico com categoria",
     "nar": "Segunda: arco elétrico vira exigência, com EPI por categoria e "
            "estudo de energia incidente em parte dos casos.", "sem_cap": True},
    {"layout": "item", "kicker": "Muda 3", "preco": "risco elétrico no GRO",
     "nar": "Terceira: o risco elétrico entra no mesmo inventário do resto da "
            "empresa.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "comece pela lista",
     "nar": "Liste hoje os trabalhos energizados sem justificativa escrita.",
     "sem_cap": True},
]

COPY = """# NR-10 atualizada: o prazo termina em junho de 2027

## TITULO
NR-10 Atualizada: o Prazo Termina em Junho de 2027 e Três Exigências São Novas

## DESCRICAO
A NR-10 inteira foi reescrita, e a sua empresa tem pouco mais de nove meses para se adequar. Parece bastante — não é, e este vídeo explica por quê.

O QUE ACONTECEU, COM FONTE

A Portaria MTE nº 737, de 29 de maio de 2026, publicada no Diário Oficial da União em 1º de junho de 2026, aprovou o novo texto da NR-10 (Segurança em Instalações Elétricas). O arquivo da portaria está hospedado no site do próprio Ministério do Trabalho e Emprego. A transição é de 12 meses: o texto novo passa a valer em 1º de junho de 2027. Ele não emenda a norma anterior — substitui integralmente os textos das Portarias MTE nº 598/2004 e MTPS nº 508/2016.

POR QUE NOVE MESES É POUCO

Porque parte do que mudou não se resolve com reciclagem de treinamento. Exige levantamento em campo, revisão de projeto e, em alguns casos, estudo de engenharia. Quem começar em maio de 2027 não termina em junho.

AS TRÊS MUDANÇAS QUE PESAM

1) DESENERGIZAR VEM PRIMEIRO. O texto prioriza a desenergização sobre o EPI. A pergunta deixa de ser qual equipamento usar e passa a ser se dava para desligar — e, se não dava, isso precisa estar justificado. Na prática muda o que fica registrado: o documento deixa de provar que havia EPI e passa a precisar provar que a energização era necessária.

2) ARCO ELÉTRICO COM CATEGORIA. Arco elétrico não é choque: é liberação de energia em forma de calor e pressão. O que protege de um não protege do outro. O texto novo trabalha com EPI por categoria, o que exige saber o nível de energia daquele ponto — e, em parte dos casos, estudo de energia incidente sobre a instalação real, não sobre o projeto antigo.

3) RISCO ELÉTRICO NO GRO. O elétrico deixa de viver num documento próprio e entra no mesmo inventário de riscos e plano de ação do resto da empresa. Acaba a situação em que dois documentos da mesma empresa dizem coisas diferentes sobre o mesmo risco — e começa o trabalho de conciliar os dois, normalmente feito por duas pessoas que nunca conversaram.

O QUE FAZER NOS PRÓXIMOS 90 DIAS (nada depende de orçamento aprovado)

Baixar a portaria no site do MTE e ler a fonte. Listar todos os trabalhos energizados que a empresa faz hoje, com a justificativa de cada um — cada linha sem justificativa escrita é uma tarefa, e você já sabe quantas são. Identificar em quais pontos você não sabe o nível de energia incidente (não precisa calcular agora, precisa saber onde falta). E marcar uma reunião de uma hora entre quem mantém o inventário de riscos e quem responde pela parte elétrica.

O QUE ESTE VÍDEO NÃO FAZ

Não percorre a norma artigo por artigo — ela substitui um texto de duas décadas e resumo falado não substitui leitura. Não diz quanto custa a adequação, porque depende do estado da instalação e quem der um número sem olhar está chutando. E não diz quando a fiscalização vai apertar: o que se sabe é a data em que o texto passa a valer, 1º de junho de 2027.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Duas perguntas para quem trabalha com isso, e as respostas variam muito mais do que parece: na sua empresa, quantos trabalhos energizados têm justificativa ESCRITA hoje, e vocês já sabem em quais pontos falta estudo de energia incidente? Estou juntando essas respostas para o próximo material — o que mais me interessa é saber se a conciliação entre o documento elétrico e o inventário de riscos já começou em algum lugar.

## HASHTAGS
#NR10 #SegurancaDoTrabalho #LabTreinamento

## TAGS
nr 10, nr10 atualizada, portaria 737 2026, seguranca do trabalho, arco eletrico, energia incidente, desenergizacao, gro, pgr, sst, instalacoes eletricas, tecnico de seguranca, engenharia de seguranca, nr 10 2027, ministerio do trabalho

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao > 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Portaria MTE nº 737, de 29/05/2026, publicada no DOU em 01/06/2026, aprovando o novo texto da NR-10; transição de 12 meses e vigência em 01/06/2027; substituição integral das Portarias MTE nº 598/2004 e MTPS nº 508/2016. Conferido em duas passagens de busca com veículos independentes que coincidem, e o PDF da portaria está hospedado em gov.br (Ministério do Trabalho e Emprego) — leia a fonte, ela é gratuita. Este vídeo NÃO percorre a norma artigo por artigo e não substitui a leitura do texto oficial nem a consulta a profissional habilitado. Não há neste vídeo estimativa de custo de adequação nem de estudo de energia incidente, porque o valor depende do porte e do estado da instalação. Não há previsão sobre intensidade ou calendário de fiscalização — a única data afirmada é a de vigência. Material educativo para profissionais de SST, não é consultoria nem parecer técnico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/labtreinamento-004.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-004",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#16222F", "c1": "#0F6E8C", "c2": "#E0A02E",
               "bg": "#F1F5F7"},
    "thumb": {"l1": "NR-10 nova", "l2": "prazo jun/2027"},
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
    grava(SPEC, "fabrica/specs/labtreinamento-004.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
