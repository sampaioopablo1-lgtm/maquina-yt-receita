# -*- coding: utf-8 -*-
"""Monta a spec do `labtreinamento-014` — o TERCEIRO longo com trilho, e com ele
os TRES canais da frota passam a ter um.

Canal escolhido pelo contador: minimo absoluto na janela de 24 h (8 / 9 / 9),
sem empate — e era o unico sem longo novo.

Classe de conteudo: PROCEDIMENTO. Nenhum numero do mundo entra: nem prazo de
NR, nem periodicidade de reciclagem, nem percentual de meta. Todos os numeros
da conta sao do PROPRIO espectador (a folha dele, a lista de presenca dele).
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
cena(layout="titulo", kicker="O denominador", sub="o número que ninguém discute",
     cap="O número embaixo da conta",
     nar="Você reporta um percentual de treinados. Todo mundo olha o número de cima, e o problema quase sempre está no de baixo.")
cena(layout="item", kicker="Não é quantos treinaram", preco="é sobre quantos",
     nar="A pergunta não é quantas pessoas passaram pelo treinamento. É sobre quantas esse número foi dividido, e isso ninguém confere.", sem_cap=True)
cena(layout="item", kicker="O mesmo numerador", preco="dois percentuais",
     nar="As mesmas pessoas treinadas podem virar oitenta por cento ou cinquenta, só trocando o número de baixo. Nenhuma delas mentiu.", sem_cap=True)
cena(layout="erro", codigo="#DIV/0!", causa="Divisão sem denominador",
     saida="Defina primeiro quem era elegível",
     nar="Se você põe os treinados em cima e deixa o de baixo em branco, a planilha nem calcula. Ela não mostra número errado: mostra nenhum.", sem_cap=True)
cena(layout="item", kicker="Ninguém pergunta", preco="nem a auditoria",
     nar="Na prática quase nunca alguém pede o denominador. Pedem o percentual, que é o resultado, e o resultado esconde a escolha.", sem_cap=True)
cena(layout="numero", valor="÷", legenda="onde mora a decisão",
     nota="o número de cima você conta; o de baixo você escolhe", escala=1.0,
     nar="Todo o vídeo é sobre esse sinal. O que está em cima se conta; o que está embaixo se decide.", sem_cap=True)
cena(layout="item", kicker="E a decisão é sua", preco="então escreva",
     nar="Como a escolha é sua, ela precisa estar escrita em algum lugar. Indicador sem regra de denominador não se compara com nada.", sem_cap=True)
cena(layout="item", kicker="Os dados existem", preco="e são seus",
     nar="Você não precisa de nada que não tenha. A lista de presença de um lado e a folha de pessoal do outro.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 2
cena(layout="titulo", kicker="Quem entrou", sub="e quem saiu no meio",
     cap="Quem entrou e quem saiu no meio",
     nar="O denominador parece fixo e não é. Pessoas entram e saem durante o período, e cada uma muda a conta de um jeito diferente.")
cena(layout="divisor", parte="1", titulo="O denominador",
     nar="Primeira parte: montar o número de baixo, porque é ele o difícil e não a divisão.", sem_cap=True)
cena(layout="lista", kicker="Quatro situações, quatro contas",
     itens=["Estava no começo e ficou", "Entrou no meio", "Saiu no meio", "Entrou e saiu dentro"],
     nar="Quatro situações aparecem em qualquer período. Tratar as quatro igual é o que produz indicador que ninguém consegue repetir.", sem_cap=True)
cena(layout="item", kicker="Quem entrou depois", preco="teve tempo de treinar?",
     nar="Quem entrou faltando duas semanas para o fim não teve chance real de treinar. Contar essa pessoa no de baixo derruba o seu número sem motivo.", sem_cap=True)
cena(layout="comparar",
     esq={"titulo": "Fora do denominador", "itens": ["Entrou no fim do período", "Afastado o período todo", "Função sem o requisito", "Já saiu antes do início"]},
     dir={"titulo": "Dentro do denominador", "itens": ["Estava e ficou", "Entrou com tempo de treinar", "Saiu, mas estava elegível", "Voltou de afastamento"]},
     nar="A linha que separa não é quem está hoje na folha. É quem teve a oportunidade de treinar dentro do período que você está medindo.", sem_cap=True)
cena(layout="item", kicker="Quem saiu também conta", preco="se era elegível",
     nar="E quem saiu no meio conta, se teve tempo de treinar e não treinou. Tirar essa pessoa é o jeito mais fácil de melhorar o indicador sem fazer nada.", sem_cap=True)
cena(layout="item", kicker="Afastado é caso próprio", preco="e vai declarado",
     nar="Quem passou o período inteiro afastado não tinha como treinar. Esse caso sai da conta, e a regra fica escrita em vez de combinada.", sem_cap=True)
cena(layout="item", kicker="Uma vez, para valer", preco="e não a cada mês",
     nar="Essa lista de regras se escreve uma vez. Ela muda quando muda a política, não quando o resultado do mês ficou abaixo do esperado.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 3
cena(layout="titulo", kicker="A janela", sub="de quando a quando",
     cap="A janela: de quando a quando",
     nar="Antes de dividir, falta decidir o período. E a escolha do período muda o indicador tanto quanto a do denominador.")
cena(layout="formula", formula="treinados na janela ÷ elegíveis na janela",
     notas=["treinados: concluíram DENTRO do período",
            "elegíveis: tiveram oportunidade DENTRO do período",
            "a mesma janela nos dois — é aí que o erro entra"],
     nar="Em cima, quem concluiu dentro do período. Embaixo, quem era elegível no mesmo período. As duas janelas têm de ser a mesma.", sem_cap=True)
cena(layout="item", kicker="O erro é misturar", preco="numerador de um, denominador de outro",
     nar="O erro mais comum é somar os treinados de todo o histórico e dividir pelas pessoas de hoje. Isso dá um percentual que não existe.", sem_cap=True)
cena(layout="item", kicker="Janela móvel ou ano", preco="as duas servem",
     nar="Doze meses corridos ou o ano fechado, as duas funcionam. O que não funciona é trocar de uma para a outra quando o número não agrada.", sem_cap=True)
cena(layout="numero", valor="=", legenda="a mesma janela nos dois lados",
     nota="trocar a janela de um lado só é o erro mais barato de evitar", escala=0.7,
     nar="Se você só guardar uma coisa deste capítulo, guarde isto: a mesma janela em cima e embaixo.", sem_cap=True)
cena(layout="item", kicker="Arredonde para baixo", preco="sempre para baixo",
     nar="Se der setenta e nove e meio por cento, escreva setenta e nove. Indicador não é lugar para otimismo na segunda casa.", sem_cap=True)
cena(layout="barras", kicker="Mesmos treinados, três janelas",
     barras=[{"rotulo": "Histórico todo", "valor": 9}, {"rotulo": "Doze meses", "valor": 6}, {"rotulo": "Trimestre", "valor": 3}],
     nar="Os mesmos treinados dão três percentuais bem diferentes em três janelas. Nenhuma das três está errada, e só uma responde à sua pergunta.", sem_cap=True)
cena(layout="item", kicker="Dois caminhos", preco="um resultado",
     nar="Daí sai uma coisa prática: o indicador melhora de dois jeitos. Treinando mais gente, ou acertando quem de fato era elegível.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 4
cena(layout="titulo", kicker="Quais papéis", sub="todos você já tem",
     cap="De quais papéis saem os dois números",
     nar="Nenhum dos dois números se estima. Os dois estão escritos em documentos que já existem na sua mesa.")
cena(layout="divisor", parte="2", titulo="Os papéis",
     nar="Segunda parte: onde exatamente olhar, linha por linha, para não pôr número de memória.", sem_cap=True)
cena(layout="lista", kicker="Três fontes e acabou",
     itens=["Lista de presença assinada", "Movimentação de pessoal do período", "Descrição das funções"],
     nar="Três fontes bastam. A presença dá o de cima, a movimentação dá o de baixo, e a descrição de função diz quem precisava do treinamento.", sem_cap=True)
cena(layout="item", kicker="Presença, não inscrição", preco="a diferença é grande",
     nar="Em cima entra quem concluiu, não quem se inscreveu. A lista de inscritos sempre é maior, e usar ela infla o seu número.", sem_cap=True)
cena(layout="item", kicker="A movimentação tem data", preco="e é ela que decide",
     nar="Cada admissão e cada desligamento tem uma data. É comparando essas datas com a sua janela que você resolve as quatro situações.", sem_cap=True)
cena(layout="item", kicker="A função diz quem precisa", preco="não o organograma",
     nar="Quem precisa do treinamento sai da descrição da função, e não do cargo no organograma. Dois cargos iguais podem ter requisitos diferentes.", sem_cap=True)
cena(layout="item", kicker="Guarde o denominador", preco="com a lista de nomes",
     nar="Guarde junto do percentual a lista de quem entrou no de baixo. Sem ela, em três meses você não consegue explicar o próprio número.", sem_cap=True)
cena(layout="item", kicker="Uma hora", preco="e a regra está pronta",
     nar="O trabalho inteiro é cerca de uma hora e se faz uma vez. Depois disso, cada período leva poucos minutos.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 5
cena(layout="titulo", kicker="Dois erros", sub="os dois dão número bonito",
     cap="Os dois erros que dão um número bonito",
     nar="Dois erros estragam essa conta, e os dois a deixam mais bonita. É por isso que eles duram tanto sem ninguém notar.")
cena(layout="erro", codigo="#REF!", causa="O denominador apontava para a lista antiga",
     saida="Refaça a lista do período, com as datas",
     nar="Primeiro erro: o de baixo veio de uma lista velha, de antes das admissões. A planilha calcula, mas está comparando dois tempos diferentes.", sem_cap=True)
cena(layout="item", kicker="O segundo é escolhido", preco="e por isso é pior",
     nar="Segundo erro: tirar do de baixo quem saiu da empresa. Isso sempre melhora o indicador, e é a tentação que não dá aviso nenhum.", sem_cap=True)
cena(layout="item", kicker="Os dois dão número", preco="nenhum dá erro",
     nar="Nos dois casos a conta fecha e o número sai redondo. Ninguém recebe aviso de que o de baixo estava errado.", sem_cap=True)
cena(layout="formula", formula="conferência = elegíveis × percentual ≟ treinados",
     notas=["se não fecha, o erro está no denominador",
            "faça a conta ao contrário, uma vez",
            "dois minutos, e pega os dois erros"],
     nar="A conferência é fazer a conta ao contrário. Multiplique os elegíveis pelo percentual e tem de dar exatamente os treinados que você contou.", sem_cap=True)
cena(layout="item", kicker="A segunda conferência", preco="é uma pergunta",
     nar="E uma segunda, mais simples: se eu entregasse a lista de nomes do denominador, alguém discordaria de algum deles?", sem_cap=True)
cena(layout="item", kicker="Compare com você mesmo", preco="não com o setor",
     nar="Compare o seu percentual com o seu do período anterior, pela mesma regra. Comparar com média de setor é trocar um denominador que você conhece por um que não.", sem_cap=True)
cena(layout="item", kicker="O erro não é a divisão", preco="é a lista",
     nar="Em tudo isso a divisão nunca falha. Falha sempre a lista, e é ela a única coisa que vale revisar de novo.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 6
cena(layout="titulo", kicker="Mesma turma", sub="e dois percentuais",
     cap="Mesma turma, dois percentuais",
     nar="Aqui fica claro por que o percentual sozinho não diz nada. Duas áreas com o mesmo treinamento podem reportar números bem diferentes.")
cena(layout="comparar",
     esq={"titulo": "Percentual sem regra", "itens": ["Compara com qualquer um", "Muda com a rotatividade", "Não diz quem faltou"]},
     dir={"titulo": "Percentual com regra", "itens": ["Compara com você mesmo", "Muda com o treinamento", "Diz exatamente quem faltou"]},
     nar="Percentual sem regra de denominador compara você com qualquer um. Com a regra escrita, ele compara você com o seu próprio período passado.", sem_cap=True)
cena(layout="item", kicker="Uma área com rotatividade", preco="e outra estável",
     nar="Uma área que trocou metade da equipe e outra que não trocou ninguém não têm o mesmo denominador, mesmo com a mesma turma treinada.", sem_cap=True)
cena(layout="numero", valor="×2", legenda="metade do denominador, o dobro do indicador",
     nota="mesma turma, nenhuma pessoa treinada a mais", escala=0.8,
     nar="Com metade do denominador, o mesmo treinamento vira o dobro do indicador. Ninguém treinou uma pessoa a mais.", sem_cap=True)
cena(layout="item", kicker="Por isso não se empresta", preco="nenhum número",
     nar="Por isso nenhum percentual que você ouve de fora serve para você. O número dele responde ao denominador dele.", sem_cap=True)
cena(layout="item", kicker="Nem a média do setor", preco="ela não tem regra",
     nar="O mesmo vale para qualquer média de mercado que circula. É percentual sem regra de denominador, ou seja, o erro do primeiro capítulo.", sem_cap=True)
cena(layout="barras", kicker="Mesma turma, três áreas",
     barras=[{"rotulo": "Equipe estável", "valor": 8}, {"rotulo": "Rotatividade média", "valor": 5}, {"rotulo": "Rotatividade alta", "valor": 3}],
     nar="Três áreas, a mesma turma treinada, três indicadores. A diferença não está no esforço de treinar.", sem_cap=True)
cena(layout="item", kicker="O número é seu", preco="e a regra também",
     nar="O resultado dessa conta não se compara e não se empresta. É seu, assim como é sua a regra que o produziu.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 7
cena(layout="titulo", kicker="Qual meta", sub="a resposta não é cem",
     cap="Qual meta faz sentido",
     nar="Resta a pergunta difícil: qual percentual é suficiente. E aqui não existe número que valha para todas as áreas.")
cena(layout="divisor", parte="3", titulo="A meta",
     nar="Terceira parte: como sair de um alvo redondo para um que você consegue defender.", sem_cap=True)
cena(layout="item", kicker="Cem por cento", preco="quase sempre é da regra",
     nar="Quando alguém bate cem por cento com folga, vale olhar o denominador antes de comemorar. Muitas vezes a conquista foi na lista.", sem_cap=True)
cena(layout="lista", kicker="O que torna a meta mais dura",
     itens=["Rotatividade alta", "Equipe em turnos", "Treinamento longo", "Função nova na área"],
     nar="Quatro coisas tornam a meta mais difícil, e nenhuma delas tem a ver com empenho. Têm a ver com quantas pessoas novas entram e quando.", sem_cap=True)
cena(layout="item", kicker="Turno complica", preco="porque a janela encurta",
     nar="Equipe em turnos tem menos horas coincidentes, logo menos chance de treinar dentro da janela. Isso entra na meta, não na cobrança.", sem_cap=True)
cena(layout="numero", valor="1", legenda="a primeira pessoa que falta",
     nota="saber o nome vale mais que saber o percentual", escala=1.0,
     nar="E se a meta parece longe, o que muda mais é saber o nome da primeira pessoa que falta. O percentual não diz isso.", sem_cap=True)
cena(layout="item", kicker="A lista de faltantes", preco="é o entregável",
     nar="O indicador serve para produzir uma lista de nomes. Se ele não produz essa lista, ele é relatório e não é ferramenta.", sem_cap=True)
cena(layout="item", kicker="Primeiro meça", preco="depois cobre",
     nar="Por isso a ordem é esta e não a inversa: primeiro você acerta a regra, e só depois define a meta e cobra alguém.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 8
cena(layout="titulo", kicker="Hoje", sub="uma conta e uma linha",
     cap="Uma conta para hoje",
     nar="Se for para guardar uma coisa deste vídeo, guarde a conta. Treinados na janela divididos pelos elegíveis na mesma janela.")
cena(layout="item", kicker="Escreva a regra", preco="antes do número",
     nar="Escreva a regra do denominador antes de calcular. Uma frase basta, e ela é o que vai sobreviver à troca de quem faz o relatório.", sem_cap=True)
cena(layout="item", kicker="Guarde os nomes", preco="junto do percentual",
     nar="Guarde a lista de nomes do denominador junto do resultado. É ela que responde quando alguém perguntar de onde veio o número.", sem_cap=True)
cena(layout="item", kicker="Refaça por período", preco="não por semana",
     nar="Refaça a conta a cada período fechado, não toda semana. Indicador que se recalcula demais perde a comparação com ele mesmo.", sem_cap=True)
cena(layout="item", kicker="Se a regra mudar", preco="o histórico muda com ela",
     nar="Uma exceção: se a regra do denominador mudar, recalcule o histórico pela nova. Série com duas regras no meio não compara nada.", sem_cap=True)
cena(layout="item", kicker="O número não julga", preco="só mostra",
     nar="E qualquer percentual que saia não é uma nota sobre o seu trabalho. É onde você está hoje, e serve para sair de lá.", sem_cap=True)
cena(layout="item", kicker="Número baixo", preco="é número útil",
     nar="Se vier baixo, não troque a regra. Um número baixo que você sabe defender vale mais que um alto que ninguém consegue explicar.", sem_cap=True)
cena(layout="cta", kicker="Qual era o seu denominador", sub="escreva aí embaixo",
     nar="Faça a conta e escreva aqui embaixo uma coisa só: qual regra você usou no denominador. Sem nomes e sem números.", sem_cap=True)

# ------------------------------------------------------------------- O SHORT
# Mira do canal: 20,0 a 26,0 de duracao REAL. UMA frase por cena.
SHORT = [
    dict(layout="titulo", kicker="Dividido pelo número errado", sub="o de baixo",
         nar="O erro não está em cima."),
    dict(layout="item", kicker="Não é quantos treinaram", preco="é sobre quantos",
         nar="O problema é o denominador."),
    dict(layout="barras", kicker="Mesma turma, três áreas",
         barras=[{"rotulo": "Estável", "valor": 8}, {"rotulo": "Média", "valor": 5}, {"rotulo": "Alta", "valor": 3}],
         nar="A mesma turma dá três números."),
    dict(layout="item", kicker="Quem entrou no fim", preco="não teve chance",
         nar="Entrou ontem, não dava para treinar."),
    dict(layout="titulo", kicker="Elegível na janela", sub="não quem está hoje",
         nar="Embaixo vai quem teve chance."),
    dict(layout="lista", kicker="Estes entram",
         itens=["Estava e ficou", "Entrou com tempo", "Saiu, era elegível"],
         nar="Quem saiu também conta."),
    dict(layout="item", kicker="O erro tentador", preco="tirar quem saiu",
         nar="Tirar quem saiu melhora sem treinar."),
    dict(layout="item", kicker="A mesma janela", preco="em cima e embaixo",
         nar="Trocar a janela de um lado inventa número."),
    dict(layout="cta", kicker="Qual foi a sua regra", sub="escreva embaixo",
         nar="Escreva embaixo a sua regra."),
]

COPY = """# O seu percentual de treinados está dividido pelo número errado

## TITULO
O seu Percentual de Treinados está Dividido pelo Número Errado

## DESCRICAO
Você reporta um percentual de treinados e todo mundo olha o número de cima. O problema quase sempre está no de baixo — e ele não é um fato que se conta: é uma escolha que alguém fez e raramente escreveu.

Neste vídeo a conta é uma: treinados na janela divididos pelos elegíveis na mesma janela. Parece óbvio e quase nunca é feito assim, porque o denominador parece fixo e não é. Pessoas entram e saem durante o período, e cada uma muda a conta de um jeito diferente.

Não há um único número meu neste vídeo. Nenhum prazo de norma, nenhuma periodicidade de reciclagem, nenhum percentual de meta e nenhuma média de mercado. Todos os números da conta são seus: a sua lista de presença, a sua movimentação de pessoal e a sua descrição de funções.

Um capítulo monta o denominador, que é a parte difícil. Quatro situações aparecem em qualquer período: quem estava no começo e ficou, quem entrou no meio, quem saiu no meio e quem entrou e saiu dentro da janela. Tratar as quatro igual é o que produz indicador que ninguém consegue repetir no período seguinte. A linha que separa não é quem está hoje na folha, é quem teve oportunidade real de treinar dentro do período medido — e quem saiu no meio conta, se teve essa oportunidade e não treinou.

Um capítulo trata da janela, que muda o resultado tanto quanto o denominador. O erro mais comum é somar os treinados de todo o histórico e dividir pelas pessoas de hoje: isso produz um percentual que não corresponde a período nenhum. Doze meses corridos ou o ano fechado, as duas regras funcionam; o que não funciona é trocar de uma para a outra quando o número não agrada.

Um capítulo mostra os dois erros que deixam o indicador mais bonito e por isso duram tanto: o denominador vindo de uma lista anterior às admissões, e a retirada de quem saiu da empresa. Nos dois casos a planilha calcula, o número sai redondo e nenhum aviso aparece. Por isso existe a conferência: multiplique os elegíveis pelo percentual e tem de dar exatamente os treinados que você contou.

E um capítulo sobre a meta, que não é cem por cento por decreto. Rotatividade alta, equipe em turnos, treinamento longo e função nova tornam a meta mais dura, e nenhuma dessas quatro coisas tem a ver com empenho.

Faça a conta e escreva nos comentários uma coisa só: qual regra você usou no denominador.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faça a conta e escreva aqui embaixo uma coisa só: qual foi a sua regra de denominador. Sem nomes de empresa e sem números. Quero ver quantas regras diferentes existem para um indicador que todo mundo reporta como se fosse o mesmo.

## HASHTAGS
#Treinamento #Indicadores #LabTreinamento

## TAGS
indicador de treinamento, percentual de treinados, denominador, lista de presenca, movimentacao de pessoal, rotatividade, treinamento obrigatorio, planilha de treinamento, calcule voce mesmo, gestao de treinamento, rh, seguranca do trabalho, meta de treinamento, elegiveis

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita prazo de norma regulamentadora, nao cita periodicidade de reciclagem, nao cita percentual de meta, nao cita media de mercado e nao cita valor de multa. Todos os numeros da conta saem da propria lista de presenca, da propria movimentacao de pessoal e da propria descricao de funcoes de quem assiste, e por isso nao ha numero meu que possa envelhecer nem que dependa do setor, da regiao ou do ano. Este video e da classe PROCEDIMENTO: a trava de duas fontes institucionais (600) se aplica a numero sobre o MUNDO que muda, e aqui nao existe nenhum. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer periodicidade de reciclagem e qualquer meta numerica. A primeira depende da norma aplicavel e muda; a segunda depende da rotatividade e do regime de turnos de cada area, e cita-la tornaria o video uma cobranca em vez de uma medida. O video tambem nao diz que treinar mais e sempre melhor, nao indica fornecedor de treinamento, nao trata rotatividade como culpa de ninguem e nao e consultoria juridica nem de seguranca do trabalho.
"""

sp = {
    "slug": "labtreinamento",          # em PACOTE o slug e o CANAL
    "pacote": "labtreinamento-014",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "thumb": {"l1": "Dividido errado", "l2": "o denominador"},
    "longo": L,
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD
sp["paleta"] = TD.paleta_do_canal("labtreinamento")

import trilho
n = trilho.aplica_no_longo(sp["longo"])

destino = os.path.join(RAIZ, "fabrica", "specs", "labtreinamento-014.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(f"gravado {destino}")
print(f"longo {len(L)} cenas | short {len(SHORT)} | trilho {n} capitulos")
