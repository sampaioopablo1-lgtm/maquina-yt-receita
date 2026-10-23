# -*- coding: utf-8 -*-
"""Monta a spec do `labtreinamento-015` — o PRIMEIRO longo deste canal em quatro
dias, e o segundo longo da frota em 23/10.

Canal escolhido pelo contador (`passo_zero`): janela de 24 h em 8 / 9 / 8, empate
entre kolejny e labtreinamento, desempatado pelo que esta ha mais tempo sem
publicar. E medido no parque: das 18 pecas de 23/10, UMA e longo (o
`epomeno-epipedo-069`), logo DOIS dos tres canais estao sem longo no dia contra
o pedido do dono de um longo e um curto por canal por dia.

Classe de conteudo: PROCEDIMENTO. Nenhum numero do mundo entra — nem numero de
norma, nem periodicidade de reciclagem, nem prazo, nem percentual. Os numerais
falados sao a contagem das PROPRIAS tabelas e colunas do procedimento.

A ORIGEM NASCE AQUI: o longo E a origem, logo nao ha irmao a comparar. O que foi
conferido e o contrario — que o eixo NAO repete nenhum dos treze longos do canal
(o `-011` conta vencimento, o `-012` o custo por pessoa, o `-014` o denominador
do percentual) nem a familia de peca publicada hoje em outro canal.
"""
import json
import os
import sys

RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

L = []


def cena(**k):
    L.append(k)


# ---------------------------------------------------------------- CAPITULO 1
cena(layout="titulo", kicker="A linha em branco", sub="o contratado de ontem",
     cap="A linha em branco",
     nar="Entrou alguém novo na equipe ontem. Você abre a matriz de treinamento, e a linha dessa pessoa está em branco.")
cena(layout="item", kicker="E a pergunta aparece", preco="o que ele precisa?",
     nar="A pergunta que vem em seguida é simples de fazer e difícil de responder: o que essa pessoa precisa ter feito?", sem_cap=True)
cena(layout="item", kicker="Você olha a matriz", preco="e ela não responde",
     nar="Você procura na própria matriz, e ela não diz. Ela guarda o que cada pessoa fez, e não o que cada pessoa deveria fazer.", sem_cap=True)
cena(layout="item", kicker="Então você pergunta", preco="para alguém",
     nar="Aí você pergunta para o encarregado, ou copia a linha de um colega parecido. As duas saídas funcionam e nenhuma fica escrita.", sem_cap=True)
cena(layout="erro", codigo="#N/D", causa="Pessoa sem exigência cadastrada",
     saida="A exigência não é da pessoa",
     nar="Se você tenta procurar a exigência pelo nome de quem chegou, não encontra nada. E o erro não é da fórmula.", sem_cap=True)
cena(layout="item", kicker="Porque a matriz", preco="tem a unidade errada",
     nar="A matriz foi montada tendo a pessoa como unidade. Quem chega depois não tem passado, então não tem linha.", sem_cap=True)
cena(layout="item", kicker="E isso não aparece", preco="enquanto ninguém entra",
     nar="Numa equipe que não muda, essa escolha nunca incomoda. Ela aparece no dia da contratação, da transferência e da saída.", sem_cap=True)
cena(layout="numero", valor="?", legenda="o que ele precisa ter feito",
     nota="a resposta existe antes da pessoa chegar", escala=1.0,
     nar="O vídeo é sobre essa pergunta. E a parte importante é que ela tem resposta antes de a pessoa existir na empresa.", sem_cap=True)
cena(layout="item", kicker="Os dados são seus", preco="e já estão aí",
     nar="Você não vai precisar de nada que não tenha. A descrição das funções de um lado e os registros de quem fez o quê do outro.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 2
cena(layout="titulo", kicker="A unidade", sub="cargo, não pessoa",
     cap="A unidade da matriz",
     nar="A exigência não nasce da pessoa. Ela nasce do que a pessoa faz, e isso é anterior a quem está fazendo.")
cena(layout="divisor", parte="1", titulo="Trocar a unidade",
     nar="Primeira parte: trocar a unidade da matriz. É ela que decide tudo o que vem depois.", sem_cap=True)
cena(layout="item", kicker="Duas pessoas no mesmo posto", preco="mesma exigência",
     nar="Duas pessoas que fazem a mesma coisa, no mesmo lugar, precisam das mesmas coisas. A exigência não distingue uma da outra.", sem_cap=True)
cena(layout="item", kicker="A mesma pessoa em dois postos", preco="duas exigências",
     nar="E a mesma pessoa, se muda de posto, passa a precisar de outra lista. O que mudou não foi ela: foi a atividade.", sem_cap=True)
cena(layout="comparar",
     esq={"titulo": "Matriz pela pessoa", "itens": ["Quem chega não tem linha", "Transferência não se expressa", "Quem sai leva a regra", "Cada caso é um caso"]},
     dir={"titulo": "Matriz pelo cargo", "itens": ["A linha já existe", "Trocar de cargo troca a lista", "A regra fica", "O caso novo já tem resposta"]},
     nar="Os dois lados guardam a mesma informação. Só um dos dois responde o que você precisa no dia em que alguém entra.", sem_cap=True)
cena(layout="item", kicker="E não é sobre o nome", preco="é sobre a atividade",
     nar="Cargo aqui não quer dizer o nome no contrato. Quer dizer o conjunto de atividades, que é o que gera a exigência.", sem_cap=True)
cena(layout="item", kicker="Dois nomes, um posto", preco="junte",
     nar="Se dois nomes de cargo fazem exatamente a mesma coisa, eles são um posto só na matriz. Separar vira trabalho dobrado.", sem_cap=True)
cena(layout="item", kicker="Um nome, dois postos", preco="separe",
     nar="E se o mesmo nome de cargo faz coisas diferentes em áreas diferentes, são dois postos. O nome engana nos dois sentidos.", sem_cap=True)
cena(layout="item", kicker="Quem decide isso", preco="é a atividade descrita",
     nar="O que separa um posto do outro é a descrição da atividade, não a hierarquia e não o departamento.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 3
cena(layout="titulo", kicker="As duas tabelas", sub="e a ponte entre elas",
     cap="As duas tabelas",
     nar="Com a unidade trocada, a matriz deixa de ser uma tabela e passa a ser duas, ligadas por uma coluna.")
cena(layout="lista", kicker="Duas tabelas, um vínculo",
     itens=["Posto e exigência", "Pessoa e posto", "A conta sai do cruzamento"],
     nar="Uma tabela diz o que cada posto exige. A outra diz em que posto cada pessoa está. A conta sai do cruzamento das duas.", sem_cap=True)
cena(layout="item", kicker="A primeira é curta", preco="e quase não muda",
     nar="A tabela de postos tem poucas linhas e muda raramente. Ela é a parte que você pensa uma vez e revisa de vez em quando.", sem_cap=True)
cena(layout="item", kicker="A segunda muda sempre", preco="e é só isso",
     nar="A tabela de pessoas muda toda semana, e cada mudança é uma célula: o posto de alguém. Nada mais.", sem_cap=True)
cena(layout="formula", formula="exigência da pessoa = exigência do posto dela",
     notas=["a pessoa não tem exigência própria",
            "ela herda a do posto em que está",
            "trocar o posto troca a lista inteira"],
     nar="A exigência de uma pessoa deixa de ser digitada e passa a ser herdada. Você escreve o posto, e a lista vem com ele.", sem_cap=True)
cena(layout="item", kicker="E o registro do que foi feito", preco="continua por pessoa",
     nar="O que foi feito continua sendo da pessoa, com data. Isso é histórico e pertence a ela, não ao posto.", sem_cap=True)
cena(layout="item", kicker="São coisas diferentes", preco="e ficam separadas",
     nar="A exigência é do posto. A realização é da pessoa. Misturar as duas na mesma tabela é como a matriz estava antes.", sem_cap=True)
cena(layout="item", kicker="A terceira coluna", preco="a data",
     nar="No registro do que foi feito, a data não é enfeite. Sem ela você sabe que houve, e não sabe se ainda vale.", sem_cap=True)
cena(layout="item", kicker="Sem nome de pessoa", preco="na tabela de postos",
     nar="E a tabela de postos não leva nome de ninguém. No dia em que ela levar, você voltou para o começo do vídeo.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 4
cena(layout="titulo", kicker="Mudou de função", sub="o caso que não se expressa",
     cap="Quem mudou de função",
     nar="Agora o caso que a matriz antiga não conseguia escrever de jeito nenhum: alguém que troca de posto.")
cena(layout="item", kicker="Na matriz pela pessoa", preco="você edita a linha",
     nar="Na matriz antiga você abria a linha da pessoa e trocava as exigências uma por uma, de cabeça.", sem_cap=True)
cena(layout="item", kicker="E perdia duas coisas", preco="de uma vez",
     nar="Nessa edição duas informações desaparecem: o que ela deixou de precisar, e o que ela passou a precisar.", sem_cap=True)
cena(layout="lista", kicker="Na troca de posto",
     itens=["O que já tem e continua valendo", "O que já tem e não serve mais", "O que falta e é novo"],
     nar="Toda troca de posto gera três grupos. O primeiro não dá trabalho, o segundo não dá trabalho, e o terceiro é a sua lista.", sem_cap=True)
cena(layout="item", kicker="O grupo do meio", preco="não se apaga",
     nar="O que ela fez e não serve mais no posto novo continua registrado. Ninguém desfez aquilo, e se ela voltar, serve outra vez.", sem_cap=True)
cena(layout="item", kicker="Com as duas tabelas", preco="é uma célula",
     nar="Com as duas tabelas, a transferência é editar uma célula: o posto. Os três grupos aparecem sozinhos no cruzamento.", sem_cap=True)
cena(layout="erro", codigo="#REF!", causa="A linha antiga foi apagada",
     saida="Troque o posto, não apague a linha",
     nar="O erro mais caro dessa hora é apagar a linha e criar outra. Quem faz isso perde o histórico de uma pessoa que continua na empresa.", sem_cap=True)
cena(layout="item", kicker="Promoção é o mesmo caso", preco="com outro nome",
     nar="Promoção, remanejamento e mudança de turno são o mesmo caso: a atividade mudou, então a lista mudou.", sem_cap=True)
cena(layout="item", kicker="E a cobertura temporária", preco="também",
     nar="Quem cobre um posto por um período está fazendo aquela atividade. A exigência vem junto, mesmo que o contrato não mude.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 5
cena(layout="titulo", kicker="Quem saiu", sub="e a regra que fica",
     cap="Quem saiu",
     nar="O terceiro caso é a saída. E aqui a diferença entre as duas matrizes é a mais fácil de ver.")
cena(layout="item", kicker="Na matriz pela pessoa", preco="a regra sai com ela",
     nar="Quando a matriz é pela pessoa, a exigência daquele posto morava na linha de quem ocupava. A pessoa sai, e a regra sai com ela.", sem_cap=True)
cena(layout="item", kicker="E quem entrar no lugar", preco="começa do zero",
     nar="Quem entrar naquele posto depois recomeça a descoberta inteira. A empresa já sabia, e esqueceu junto com a saída.", sem_cap=True)
cena(layout="item", kicker="Com o posto como unidade", preco="a regra não sai",
     nar="Com o posto como unidade, a linha de exigência fica. O que sai é o vínculo de uma pessoa com aquele posto.", sem_cap=True)
cena(layout="divisor", parte="2", titulo="O que a matriz passa a responder",
     nar="Segunda parte: o que você consegue perguntar depois que a unidade está certa.", sem_cap=True)
cena(layout="item", kicker="E o registro de quem saiu", preco="não se apaga",
     nar="O registro de quem saiu continua guardado. Ele não entra mais na conta de hoje, e continua sendo prova do que aconteceu.", sem_cap=True)
cena(layout="item", kicker="Uma coluna resolve", preco="ativo ou não",
     nar="Uma coluna de situação na tabela de pessoas resolve isso. Quem não está ativo sai da conta sem sair do arquivo.", sem_cap=True)
cena(layout="item", kicker="Apagar parece limpeza", preco="e é perda",
     nar="Apagar a linha de quem saiu parece organização. É a única das operações do vídeo que não tem como desfazer.", sem_cap=True)
cena(layout="item", kicker="Posto vazio", preco="continua na tabela",
     nar="E posto sem ninguém continua na tabela de postos. Ele volta a ser ocupado, e a exigência dele estava esperando.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 6
cena(layout="titulo", kicker="Quem está sem", sub="a pergunta que vale",
     cap="Quem está sem o quê",
     nar="Com as duas tabelas no lugar, aparece uma pergunta que a matriz antiga não conseguia responder.")
cena(layout="item", kicker="Antes", preco="quem fez o quê",
     nar="A matriz antiga respondia uma coisa: quem fez o quê. É uma lista de presença organizada, e ela não aponta trabalho nenhum.", sem_cap=True)
cena(layout="item", kicker="Agora", preco="quem está sem o quê",
     nar="A matriz pelo posto responde outra: quem está em um posto que exige algo que essa pessoa não tem registrado.", sem_cap=True)
cena(layout="formula", formula="falta = exigido pelo posto − registrado pela pessoa",
     notas=["o exigido vem da tabela curta",
            "o registrado vem do histórico",
            "o que sobra é a sua lista de trabalho"],
     nar="A conta é uma subtração entre as duas tabelas. O que sobra não é um indicador: é uma lista de nomes com o que falta em cada um.", sem_cap=True)
cena(layout="item", kicker="E ela nasce ordenada", preco="pelo posto",
     nar="Essa lista já vem agrupada por posto, que é como o trabalho é feito. Você não convoca uma pessoa: convoca um posto.", sem_cap=True)
cena(layout="item", kicker="O contratado de ontem", preco="aparece no primeiro dia",
     nar="E a pessoa que entrou ontem aparece nessa lista no mesmo dia, sem ninguém se lembrar dela. O posto dela já tinha a resposta.", sem_cap=True)
cena(layout="barras", kicker="O que cada matriz responde",
     barras=[{"rotulo": "Quem fez", "valor": 9}, {"rotulo": "Quem está sem", "valor": 9}],
     nar="As duas perguntas valem o mesmo e não são a mesma. A primeira você já tinha. A segunda é a que gera convocação.", sem_cap=True)
cena(layout="item", kicker="Sem meta nenhuma", preco="e sem percentual",
     nar="Repare que até aqui não apareceu percentual nem meta. A lista de quem está sem algo não precisa de nota para virar tarefa.", sem_cap=True)
cena(layout="item", kicker="E o percentual", preco="sai depois, se você quiser",
     nar="Se você quiser o percentual, ele sai disso. Mas ele é resumo, e quem trabalha trabalha com a lista.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 7
cena(layout="titulo", kicker="O registro", sub="o que fica escrito",
     cap="O que fica escrito",
     nar="Falta a última parte, que é a mais chata e a que faz a matriz sobreviver a você.")
cena(layout="item", kicker="A tabela de postos", preco="precisa de dono e data",
     nar="A tabela que diz o que cada posto exige é uma decisão. Toda decisão precisa de quem decidiu e de quando.", sem_cap=True)
cena(layout="item", kicker="Sem isso", preco="ela vira folclore",
     nar="Sem quem e quando, a lista de exigências de um posto se torna uma coisa que todo mundo repete e ninguém sabe de onde veio.", sem_cap=True)
cena(layout="lista", kicker="Três colunas na decisão",
     itens=["O que o posto exige", "Quem definiu", "Desde quando"],
     nar="São três colunas, uma vez por posto. É o trecho mais curto da matriz, e é o único que responde por ela.", sem_cap=True)
cena(layout="item", kicker="Quando a exigência muda", preco="não sobrescreva",
     nar="E quando a exigência de um posto mudar, não apague a antiga. A pessoa que cumpriu a regra de antes cumpriu a regra que valia.", sem_cap=True)
cena(layout="item", kicker="Uma linha nova", preco="com a data nova",
     nar="A mudança é uma linha nova com a data nova. Assim você consegue olhar para trás e entender por que a conta de então dava aquilo.", sem_cap=True)
cena(layout="item", kicker="E o resto é manutenção", preco="uma célula por vez",
     nar="Depois disso a manutenção é pequena: quando alguém entra, sai ou muda, você edita uma célula. A matriz se recalcula.", sem_cap=True)
cena(layout="item", kicker="Comece pelo posto", preco="que mais troca de gente",
     nar="Se você for montar hoje, comece pelo posto onde entra e sai mais gente. É ali que a unidade errada custa mais.", sem_cap=True)
cena(layout="cta", kicker="Qual é a unidade da sua matriz", sub="escreva aí embaixo",
     nar="Abra a sua matriz e veja uma coisa só: a primeira coluna é nome de pessoa ou nome de posto? Escreve aqui embaixo.", sem_cap=True)

# ------------------------------------------------------------------- O SHORT
SHORT = [
    dict(layout="titulo", kicker="Entrou alguém ontem", sub="a linha está em branco",
         nar="A linha do novato está vazia."),
    dict(layout="item", kicker="E a matriz não diz", preco="o que ele precisa",
         nar="A matriz não diz o que falta."),
    dict(layout="barras", kicker="Onde mora a exigência",
         barras=[{"rotulo": "Pessoa", "valor": 2}, {"rotulo": "Posto", "valor": 9}],
         nar="A exigência é do posto, não dela."),
    dict(layout="item", kicker="Quem chega", preco="herda a lista",
         nar="Quem chega herda a lista dele."),
    dict(layout="lista", kicker="Duas tabelas",
         itens=["Posto e exigência", "Pessoa e posto"],
         nar="São duas tabelas e uma coluna."),
    dict(layout="item", kicker="Trocar de função", preco="é uma célula",
         nar="Trocar de função vira célula."),
    dict(layout="titulo", kicker="E a pergunta muda", sub="de quem fez para quem está sem",
         nar="A pergunta não é mais quem fez."),
    dict(layout="item", kicker="Vira quem está sem", preco="com nome e posto",
         nar="É quem está sem, com o posto."),
    dict(layout="cta", kicker="Pessoa ou posto?", sub="veja a primeira coluna",
         nar="Olhe a primeira coluna da sua."),
]

COPY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy-labtreinamento-015.md"), encoding="utf-8").read()

sp = {
    "slug": "labtreinamento",          # em PACOTE o slug e o CANAL
    "pacote": "labtreinamento-015",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "thumb": {"l1": "Pessoa", "l2": "ou posto?"},
    "longo": L,
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD
sp["paleta"] = TD.paleta_do_canal("labtreinamento")

import trilho
n = trilho.aplica_no_longo(sp["longo"])

destino = os.path.join(RAIZ, "fabrica", "specs", "labtreinamento-015.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("gravado %s" % destino)
print("longo %d cenas | short %d | trilho %d capitulos" % (len(L), len(SHORT), n))
