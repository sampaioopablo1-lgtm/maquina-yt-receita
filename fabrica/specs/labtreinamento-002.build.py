#!/usr/bin/env python3
"""Monta a spec labtreinamento-002.

Escrita como codigo pelo mesmo motivo da sx-educacao-001: os capitulos e os
`sem_cap` saem certos por construcao, e nao a mao em oitenta objetos JSON.

Por que ESTE tema, e nao outro: o config do canal registra a medicao de
2026-08-12 sobre dezesseis videos. A mediana dos longos e 1,8 views/dia e o
topo e 40,0 — e o que separa nao e tema nem duracao, e ARTEFATO. O cluster de
ISO conceitual ficou todo entre 0,7 e 1,8; o topo entrega uma PLANILHA que
resolve uma obrigacao regulatoria com data.

A obrigacao aqui e a NR-1 psicossocial: a Portaria MTE 1.419/2024 poe o risco
psicossocial no GRO e no PGR, o periodo educativo terminou em 26/05/2026, e
desde entao a mesma falha que rendia orientacao rende autuacao. Confirmado em
busca de 13/08/2026 (contabeis.com.br, rsdata.com.br, barbieriadvogados.com).

O giro do roteiro — a parte que nenhum portao mede — e que a leitura mais cara
dessa norma e a errada: "vamos ter que contratar psicologo e testar todo
mundo". A norma avalia o TRABALHO, nao o trabalhador. Isso e ao mesmo tempo
verdadeiro, barato e libertador, e e o que compra os treze minutos.

Taxa MEDIDA de pt-BR-ThalitaMultilingualNeural: 16,52 chars/s.
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
T("Sexta, dez da manha", "o e-mail do juridico",
  "Sexta-feira, dez da manha. Chega um e-mail do juridico com uma pergunta de "
  "uma linha so. Onde esta o nosso inventario de riscos psicossociais?",
  cap="O e-mail que muda a semana")
I("Voce abre o PGR", "e ele nao fala disso",
  "Voce abre o programa de gerenciamento de riscos da empresa. Ele existe ha "
  "anos e esta bem feito. E nao tem uma linha sobre o assunto.")
I("A data", "vinte e seis de maio",
  "A data que fez o juridico escrever e vinte e seis de maio de dois mil e "
  "vinte e seis. Foi o dia em que terminou o prazo de adaptacao.")
I("O que terminou ali", "a fase orientativa",
  "Antes dessa data a fiscalizacao era orientativa. O auditor via a falha e "
  "orientava. Depois dela, a mesma falha vira autuacao.")
I("De onde vem a regra", "Portaria MTE 1.419/2024",
  "A regra vem da Portaria do Ministerio do Trabalho numero mil quatrocentos e "
  "dezenove, publicada em dois mil e vinte e quatro. Ela alterou a Norma "
  "Regulamentadora numero um.")
I("O que ela manda fazer", "tratar como risco, e nao como tema",
  "E o que ela manda e direto. O risco psicossocial passa a ser gerenciado "
  "como qualquer outro risco ocupacional, dentro do mesmo programa.")
I("Sem excecao por porte", "onde ha CLT, ha obrigacao",
  "A portaria nao abriu excecao por tamanho de empresa nem por numero de "
  "empregados. Onde existe empregado com carteira assinada, existe a "
  "obrigacao de gerenciar.")
I("A reacao mais comum", "vamos contratar psicologo",
  "A reacao dentro das empresas foi quase sempre a mesma. Vamos ter que "
  "contratar psicologo e aplicar teste em todo mundo.")
I("Essa leitura e cara", "e nao e a que a norma pede",
  "Essa leitura e cara e lenta. E nao e a que a norma pede. Ela ja custou a "
  "muita empresa um orcamento que nao precisava existir.")
I("O que a norma pede", "cabe numa planilha",
  "O que a norma pede de verdade cabe numa pasta de trabalho com quatro abas. "
  "E ela que a gente monta aqui, coluna por coluna.")
L("O caminho", ["Os seis grupos de fator", "A aba Inventario",
                "A formula do nivel", "O plano de acao", "Os erros mais caros"],
  "Sao cinco partes. Os seis grupos de fator que o auditor procura. As colunas "
  "do inventario e a formula que classifica. O plano de acao. E os erros que "
  "saem mais caros.")
T("Ponte", "e sem teste nenhum",
  "E nada disso exige aplicar teste psicologico em ninguem. O que exige e "
  "olhar para outro lugar. Para onde?")

# ---------------------------------------------------------------- cap 2
T("O objeto da avaliacao", "o trabalho, nao o trabalhador",
  "A norma nao pede o estado mental de ninguem. Ela pede a avaliacao de como o "
  "trabalho esta organizado. O objeto e o trabalho.",
  cap="Nao se avalia a pessoa")
I("A diferenca e pratica", "ela decide as colunas",
  "Essa diferenca nao e filosofica. Ela decide o que entra na sua planilha e o "
  "que nunca pode entrar nela.")
I("O que nunca entra", "nome, diagnostico, atestado",
  "Nome de pessoa nao entra. Diagnostico nao entra. Atestado nao entra. Dado "
  "de saude tem regra propria e nao mora no inventario de riscos.")
I("O que entra", "a situacao de trabalho",
  "O que entra e a situacao. Prazo definido por quem nao executa. Turno que "
  "muda sem aviso. Meta revisada no meio do mes.")
I("A pergunta muda", "de quem para o que",
  "Entao a pergunta deixa de ser quem esta adoecendo. Passa a ser o que na "
  "rotina de trabalho produz o desgaste, e com que frequencia isso acontece.")
I("A norma nao da lista fechada", "os guias agrupam em seis",
  "A norma nao entrega uma lista pronta de fatores. Os guias de referencia "
  "costumam agrupar em seis familias, e e assim que a planilha organiza.")
L("Os tres primeiros", ["Carga e jornada", "Autonomia", "Clareza de papeis"],
  "Os tres primeiros vem do desenho do trabalho. Quanto se pede e em quanto "
  "tempo. Quanto a pessoa decide do proprio ritmo. E o quanto esta claro o que "
  "cabe a cada um.")
I("Carga e jornada", "o exemplo tipico",
  "Carga aparece assim: escala aberta com dois dias de antecedencia, ou hora "
  "extra virando regra num setor especifico. Isso e situacao, e da para "
  "registrar.")
I("Autonomia", "quem decide o ritmo",
  "Autonomia aparece quando o sistema mede cada minuto e a pessoa nao pode "
  "parar sem justificar. Quanto menor o controle sobre o proprio ritmo, maior "
  "o desgaste.")
I("Clareza de papeis", "duas chefias, uma pessoa",
  "Clareza de papeis aparece na pessoa que responde a duas chefias com "
  "prioridades diferentes. Ela erra decidindo, e erra tambem sem decidir.")
L("Os outros tres", ["Apoio da chefia", "Reconhecimento", "Assedio e violencia"],
  "Os outros tres vem da relacao. O apoio que existe quando algo da errado. O "
  "reconhecimento do que foi feito. E a violencia, que inclui assedio e "
  "agressao de cliente.")
I("Apoio da chefia", "o teste do erro",
  "Apoio se mede por um teste simples. Quando alguem erra, o time resolve "
  "junto ou a pessoa fica sozinha com o problema?")
I("Assedio e violencia", "tem regra propria",
  "Assedio e violencia tem tratamento proprio e canal proprio. Eles entram no "
  "inventario como risco, mas a apuracao de caso nunca vira linha de planilha.")
T("Ponte", "e agora vira coluna",
  "Seis familias, e todas descrevem organizacao de trabalho. Falta transformar "
  "isso em algo que o auditor consiga ler:")

# ---------------------------------------------------------------- cap 3
T("Quatro abas", "e a primeira e o trabalho",
  "Abra uma pasta nova. Sao quatro abas. Inventario, Matriz, Plano e "
  "Historico. Comece pela primeira, que e onde mora o trabalho de verdade.",
  cap="A aba Inventario, coluna por coluna")
L("Aba Inventario", ["Codigo", "Setor ou grupo", "Fator", "Situacao observada",
                     "Fonte da evidencia"],
  "As cinco primeiras colunas descrevem o achado. Codigo, setor ou grupo, "
  "fator, situacao observada e fonte da evidencia.")
I("Codigo", "para o plano poder apontar",
  "O codigo existe para o plano de acao apontar para a linha certa. Sem ele, "
  "duas situacoes parecidas viram a mesma e uma some.")
I("Setor ou grupo", "nunca uma pessoa",
  "O setor identifica um grupo de gente que trabalha nas mesmas condicoes. "
  "Nunca uma pessoa. Se a linha so descreve alguem, ela esta na aba errada.")
I("Fator", "lista fechada, nao texto livre",
  "O fator vem de uma lista fechada com as seis familias. Use validacao de "
  "dados na coluna. Texto livre aqui destroi qualquer contagem depois.")
I("Situacao observada", "verbo, prazo, frequencia",
  "A situacao e a coluna que o auditor le primeiro. Ela precisa de verbo e de "
  "frequencia. Escala publicada com dois dias de antecedencia, toda semana.")
I("O contraexemplo", "estresse na equipe",
  "O contraexemplo e escrever estresse na equipe. Isso nao e situacao, e "
  "conclusao. Nao da para agir sobre ela nem verificar se melhorou.")
I("A coluna que decide tudo", "Fonte da evidencia",
  "E se existe uma coluna que separa um inventario defensavel de um inventario "
  "inventado, e a quinta. Ela responde uma pergunta: como voce soube disso?")
L("Fontes que valem", ["Pesquisa anonima", "Escuta por grupo", "Absenteismo",
                       "Horas extras", "Canal de denuncia"],
  "Pesquisa anonima. Escuta por grupo. Absenteismo. Registro de horas extras. "
  "Canal de denuncia e atas da comissao interna.")
I("O que elas tem em comum", "todas descrevem grupo",
  "Repare no que todas tem em comum. Nenhuma delas e individual. Todas "
  "descrevem grupo, e e por isso que o inventario fica util sem virar "
  "prontuario.")
I("A pesquisa anonima", "so funciona se for anonima",
  "E a pesquisa so produz dado verdadeiro enquanto for anonima de verdade. "
  "Basta uma vez identificar alguem para ela nunca mais servir.")
I("Um numero por linha", "a data da coleta",
  "Guarde tambem a data da coleta junto da fonte. Daqui a um ano ninguem "
  "lembra se aquele numero veio de marco ou de novembro.")
T("Ponte", "e quanto pesa cada uma?",
  "Com isso a planilha ja descreve o que acontece. Falta o que ela ainda nao "
  "sabe dizer: qual dessas linhas e a mais grave?")

# ---------------------------------------------------------------- cap 4
T("Duas notas", "e uma multiplicacao",
  "A classificacao sai de duas notas e uma multiplicacao. Probabilidade e "
  "severidade, cada uma de um a cinco, e o produto das duas.",
  cap="A formula que classifica o risco")
I("Probabilidade", "frequencia, nao chute",
  "Probabilidade e frequencia da exposicao. Nota um e situacao rara. Nota "
  "cinco e situacao presente na rotina, toda semana, para todo o grupo.")
I("Severidade", "consequencia se acontecer",
  "Severidade e o tamanho da consequencia. Nota um e desconforto pontual. Nota "
  "cinco e afastamento, acidente ou saida de gente boa.")
I("Trave as duas colunas", "validacao de dados",
  "Ponha validacao de dados nas duas colunas, aceitando so numero inteiro "
  "entre um e cinco. Sem isso alguem digita quatro virgula cinco e a faixa "
  "para de fechar.")
I("A formula do nivel", "igual a probabilidade vezes severidade",
  "O nivel e a multiplicacao. Na coluna nivel voce escreve igual. Depois a "
  "celula da probabilidade. Depois asterisco. Depois a celula da severidade.")
I("A faixa", "e escolha sua, nao da norma",
  "Agora a parte que quase ninguem escreve. A faixa que separa alto de medio e "
  "escolha da empresa. A norma nao dita esses cortes.")
I("Entao deixe visivel", "a aba Matriz existe para isso",
  "Por isso a aba Matriz existe. Ela guarda os cortes escritos, com a data em "
  "que foram definidos e por quem. Criterio que so mora na cabeca vira "
  "discussao no dia da auditoria.")
L("Um corte possivel", ["Ate tres: baixo", "Quatro a oito: medio",
                        "Nove a quatorze: alto", "Quinze ou mais: critico"],
  "Um corte possivel. Ate tres e baixo. De quatro a oito e medio. De nove a "
  "quatorze e alto. Quinze ou mais e critico.")
I("A formula da classificacao", "SE aninhado",
  "A classificacao sai de um SE aninhado sobre o nivel. Ele testa do maior "
  "para o menor: critico primeiro, depois alto, depois medio, e o resto cai em "
  "baixo.")
I("Se preferir sem aninhar", "PROCV na aba Matriz",
  "Quem nao gosta de SE aninhado usa PROCV na aba Matriz com correspondencia "
  "aproximada. Mesma resposta, e o criterio passa a viver numa tabela em vez "
  "de dentro da formula.")
I("Envolva com SEERRO", "linha em branco nao acusa",
  "Envolva com SEERRO para a linha ainda em branco nao mostrar erro. Planilha "
  "cheia de aviso vermelho e planilha que ninguem preenche.")
B("Onde as linhas caem", ["Baixo", "Medio", "Alto", "Critico"],
  [55, 100, 62, 18],
  "E quando voce termina, aparece o desenho. A maioria das linhas cai no meio, "
  "poucas no topo, e sao essas poucas que decidem o que voce faz na segunda "
  "de manha.")
I("Formatacao condicional", "so nas duas faixas de cima",
  "Pinte so alto e critico. Se tudo tem cor, nada tem destaque, e a planilha "
  "volta a ser uma lista onde a urgencia nao aparece.")
T("Ponte", "e o que se faz com elas?",
  "Entao voce ja sabe quais linhas pesam mais. O auditor nao para ai, e a "
  "proxima pergunta dele e sempre a mesma:")

# ---------------------------------------------------------------- cap 5
T("O plano", "cinco colunas e nenhuma frouxa",
  "O que voce fez a respeito. Essa e a pergunta. E ela se responde em cinco "
  "colunas, sem nenhuma delas ficar frouxa.",
  cap="O plano de acao que o auditor le")
L("Aba Plano", ["Codigo do risco", "Medida", "Responsavel", "Prazo",
                "Verificacao"],
  "Codigo do risco, medida de controle, responsavel, prazo e verificacao da "
  "eficacia. Cinco colunas, e a ultima e a que quase todo mundo deixa vazia.")
I("Puxe so o que pesa", "alto e critico",
  "O plano nao repete o inventario inteiro. Ele puxa so as linhas classificadas "
  "como alto e critico, que sao as que exigem acao.")
I("Como puxar", "FILTRO, ou PROCV pelo codigo",
  "Se o seu Excel tem a funcao FILTRO, uma formula resolve. Se nao tem, use "
  "PROCV pelo codigo do risco, que funciona em qualquer versao.")
I("A medida", "e aqui mora o erro caro",
  "A medida de controle e a coluna onde mora o erro mais caro deste tema "
  "inteiro. E ele quase sempre tem a mesma cara.")
I("A medida individual", "palestra, aplicativo, ginastica",
  "Palestra sobre saude mental. Aplicativo de meditacao. Ginastica laboral. "
  "Nenhuma delas e ruim, e nenhuma delas responde a um risco que nasce da "
  "organizacao do trabalho.")
I("A ordem importa", "primeiro na fonte",
  "A norma trabalha com ordem de prioridade. Primeiro elimina ou reduz na "
  "fonte. Depois medida coletiva e organizacional. So por ultimo a medida "
  "voltada ao individuo.")
I("Traduzindo", "a medida certa muda a rotina",
  "Traduzindo para a planilha: se a situacao e escala publicada com dois dias "
  "de antecedencia, a medida e publicar com quinze. Nao e ensinar o grupo a "
  "lidar com a incerteza.")
I("Responsavel", "um nome, nunca uma area",
  "O responsavel e um nome. Nunca uma area. Medida de responsabilidade do "
  "Recursos Humanos e medida de ninguem, e essa nao acontece.")
I("Prazo", "uma data, nunca continuo",
  "O prazo e uma data no calendario. Continuo nao e prazo. Imediato tambem "
  "nao. Data que passou vale mais que prazo que nunca chega.")
I("A coluna do atrasado", "uma formula com HOJE",
  "Ponha uma coluna que compara o prazo com a funcao HOJE e marca atrasado "
  "quando a data passou e o status ainda nao esta concluido. Ela faz o "
  "trabalho de cobrar sozinha.")
I("Verificacao da eficacia", "a que mais falta",
  "E a ultima coluna e a que mais falta nos planos que eu vejo. Ela responde "
  "se a medida funcionou, com que evidencia, e em que data isso foi "
  "conferido.")
I("Como verificar", "a mesma fonte, de novo",
  "Verificar e simples: use a mesma fonte que gerou o achado. Se veio de "
  "pesquisa anonima, a proxima rodada compara. Se veio de hora extra, o "
  "relatorio compara.")
T("Ponte", "e o que mais derruba?",
  "Com essas cinco colunas o plano para de ser lista de boa intencao. Falta so "
  "conhecer os tres jeitos de perder tudo isso:")

# ---------------------------------------------------------------- cap 6
T("Erro um", "risco generico sem fonte",
  "O primeiro erro e a linha generica. Estresse elevado no setor, sem situacao "
  "e sem fonte. Isso nao e inventario, e opiniao com aparencia de documento.",
  cap="Os tres erros mais caros")
I("Por que ele custa", "nao da para verificar",
  "Ele custa porque impede as duas pontas. Nao da para escolher uma medida "
  "para ele, e nao da para verificar depois se melhorou.")
I("O conserto", "quebre em situacoes",
  "O conserto e quebrar em situacoes concretas. Uma linha generica costuma "
  "virar tres linhas especificas, e cada uma com uma medida diferente.")
I("Erro dois", "so medida individual",
  "O segundo erro e responder tudo com medida voltada ao individuo. O plano "
  "fica bonito, o custo aparece, e a causa continua exatamente onde estava.")
I("Como o auditor ve", "a fonte segue apontando",
  "E ele aparece sozinho na verificacao. A rodada seguinte da pesquisa mostra "
  "o mesmo numero, e o registro de hora extra tambem.")
I("Erro tres", "sem verificacao e sem data",
  "O terceiro erro e o plano sem verificacao e sem data. A empresa fez, gastou "
  "e nao registrou se funcionou. Na pratica, e como se nao tivesse feito.")
I("E um quarto", "que nao e da norma",
  "Tem um quarto erro que nao vem da norma, e ele e o mais silencioso. E "
  "colocar nome de pessoa ou dado de saude na planilha.")
I("O custo real", "a pesquisa morre",
  "O custo dele nao e a multa. E que a noticia corre, a proxima pesquisa vem "
  "respondida com o que a pessoa acha que deve responder, e voce fica cego.")
I("Cego e pior que sem planilha", "porque parece que voce sabe",
  "E ficar cego com uma planilha cheia e pior que nao ter planilha nenhuma. "
  "Porque agora existe um documento dizendo que esta tudo bem.")
I("A regra simples", "linha descreve trabalho",
  "A regra que resolve os quatro cabe numa frase. Cada linha descreve uma "
  "situacao de trabalho, com uma fonte e uma data.")
T("Ponte", "e como isso nao morre?",
  "Essa planilha resolve o dia da auditoria. Sobra a parte que decide se ela "
  "vai durar ou virar mais um arquivo esquecido:")

# ---------------------------------------------------------------- cap 7
T("Manter viva", "tres habitos",
  "Uma planilha dessas morre por falta de rotina, nunca por falta de formula. "
  "Tres habitos resolvem.",
  cap="Como manter a planilha viva")
I("Primeiro", "a mesma fonte, sempre",
  "Primeiro: a fonte de cada coluna nunca muda no meio do caminho. Fonte que "
  "troca de origem destroi a comparacao, e comparacao e a unica prova de que a "
  "medida funcionou.")
I("Segundo", "a aba Historico",
  "Segundo: a aba Historico guarda uma linha por mes, com a contagem de "
  "quantas linhas estao em cada faixa. Em um ano voce enxerga tendencia em vez "
  "de retrato.")
I("A formula do historico", "CONT.SES",
  "Essa contagem e uma funcao so. CONT.SES sobre a coluna de classificacao, "
  "cruzando com o status. Uma coluna para alto em aberto, outra para critico "
  "em aberto.")
I("Terceiro", "um dono com nome",
  "Terceiro: a planilha precisa de um dono com nome, do mesmo jeito que cada "
  "medida precisa. Planilha de todo mundo e planilha de ninguem.")
I("Quando revisar", "a norma diz, e voce confere la",
  "Sobre a frequencia de revisao, o intervalo esta escrito na propria norma e e "
  "la que voce confere. O que ninguem discute e revisar quando a organizacao "
  "do trabalho muda.")
I("O que conta como mudanca", "e mais comum do que parece",
  "E isso e mais comum do que parece. Troca de sistema. Mudanca de escala. "
  "Fusao de setores ou corte de time. Cada uma delas muda a exposicao do grupo.")
L("Recapitulando", ["Situacao com verbo", "Fonte da evidencia",
                    "Nota vezes nota", "Responsavel e prazo", "Verificacao"],
  "Recapitulando o que voce monta. Situacao com verbo e frequencia. Fonte da "
  "evidencia. Nota vezes nota para o nivel. Responsavel com nome e prazo com "
  "data. E a verificacao da eficacia.")
I("A parte que quase ninguem faz", "a coluna da fonte",
  "A parte que quase ninguem faz e a coluna da fonte. Sem ela a planilha vira "
  "uma lista de impressoes, e lista de impressoes nao sustenta nada.")
I("O que nao fazer", "montar sozinho no RH",
  "Uma coisa a nao fazer: montar isso sozinho dentro de uma sala. A comissao "
  "interna e o time de saude e seguranca precisam ver antes, porque metade das "
  "situacoes eles ja conhecem.")
I("Se voce so fizer uma coisa", "tres linhas com fonte",
  "Se voce so fizer uma coisa depois deste video, escreva tres linhas com "
  "situacao e fonte. So tres. Elas ja mostram se voce tem material ou nao.")
I("E leva uma tarde", "nao um projeto",
  "E leva uma tarde, nao um projeto. A estrutura inteira cabe numa manha, e as "
  "tres primeiras linhas cabem num cafe.")
C("LabTreinamento", "processos, planilha e prova",
  "Se voce montou o inventario, escreve nos comentarios quantas linhas "
  "ficaram em alto. Estou juntando esses numeros para o proximo video.")
C("LabTreinamento", "processos, planilha e prova",
  "E se voce quer a proxima planilha sobre outra obrigacao, diz qual. A mais "
  "pedida sai primeiro.")

SHORT = [
    {"layout": "titulo", "kicker": "NR-1 psicossocial", "sub": "leram errado",
     "nar": "A maior parte das empresas leu a NR-1 psicossocial errado. E a "
            "leitura errada e justamente a mais cara de todas.", "sem_cap": True},
    {"layout": "item", "kicker": "O erro", "preco": "avaliar a pessoa",
     "nar": "Acharam que precisavam contratar psicologo e aplicar teste em "
            "todo mundo. Nao e isso. A norma nao avalia o trabalhador.",
     "sem_cap": True},
    {"layout": "item", "kicker": "O objeto", "preco": "o trabalho, nao quem trabalha",
     "nar": "Ela avalia como o trabalho esta organizado. Jornada, autonomia, "
            "clareza de papeis, apoio da chefia quando algo da errado.",
     "sem_cap": True},
    {"layout": "item", "kicker": "A coluna que salva", "preco": "fonte da evidencia",
     "nar": "E no inventario existe uma coluna que decide tudo. Fonte da "
            "evidencia. Ela responde uma pergunta so: como voce soube disso?",
     "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "a planilha completa",
     "nar": "A planilha inteira, coluna por coluna e formula por formula, esta "
            "no video longo. Assiste agora.", "sem_cap": True},
]

COPY = """# Planilha de riscos psicossociais da NR-1

## TITULO
[EXCEL] Planilha de Riscos Psicossociais NR-1: Inventario e Plano de Acao

## DESCRICAO
Desde 26 de maio de 2026 acabou o periodo de adaptacao: a falha que antes rendia orientacao do auditor passou a render autuacao. A regra vem da Portaria MTE n. 1.419, de 2024, que incluiu os riscos psicossociais no Gerenciamento de Riscos Ocupacionais e no PGR, sem abrir excecao por porte de empresa ou numero de empregados.

A leitura mais cara dessa norma e a errada, e ela se espalhou: "vamos ter que contratar psicologo e aplicar teste em todo mundo". Nao e isso. O objeto da avaliacao e o trabalho, nao o trabalhador. O que entra no inventario e a situacao de trabalho — escala publicada com dois dias de antecedencia, meta revisada no meio do mes, pessoa respondendo a duas chefias com prioridades diferentes. Nome, diagnostico e atestado nao entram: dado de saude tem regra propria e nao mora no inventario de riscos.

Neste video a planilha e montada do zero, com quatro abas: Inventario, Matriz, Plano e Historico.

Inventario: as cinco colunas que descrevem o achado, por que o fator precisa de validacao de dados em vez de texto livre, e a coluna que separa um inventario defensavel de um inventado — Fonte da evidencia. Pesquisa anonima, escuta por grupo, absenteismo, registro de horas extras, canal de denuncia e atas da CIPA. Nenhuma delas individual, todas descrevendo grupo.

Matriz: probabilidade e severidade de um a cinco, o nivel como produto das duas, SE aninhado ou PROCV com correspondencia aproximada para classificar, e SEERRO para a linha em branco nao acusar erro. A faixa que separa alto de medio e escolha da empresa, e a norma nao dita esses cortes — por isso eles ficam escritos na aba Matriz, com data e responsavel.

Plano: codigo do risco, medida, responsavel com nome, prazo com data e verificacao da eficacia. A ordem de prioridade das medidas importa — primeiro eliminar ou reduzir na fonte, depois medida coletiva e organizacional, e so por ultimo a medida voltada ao individuo. Palestra, aplicativo de meditacao e ginastica laboral nao respondem a um risco que nasce da organizacao do trabalho.

E os quatro erros que saem mais caros, incluindo o mais silencioso: colocar nome de pessoa na planilha. O custo dele nao e a multa, e sim a pesquisa anonima deixar de produzir dado verdadeiro.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Uma pergunta, porque a resposta varia muito: quantas linhas do seu inventario ficaram classificadas como alto? E, se voce ja passou por auditoria depois de maio, o que o auditor pediu primeiro? Estou juntando esses relatos para o proximo video.

## HASHTAGS
#NR1 #RiscosPsicossociais #LabTreinamento

## TAGS
nr1, riscos psicossociais, pgr, gro, portaria 1419, saude mental no trabalho, inventario de riscos, plano de acao, excel, planilha, sst, seguranca do trabalho, matriz de risco, cipa, rh

## CONFIGURACAO DE STUDIO
- Idioma: Portugues (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo alterado ou sintetico: SIM (voz gerada por IA)
- Local: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios no meio: ligados (duracao acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
A base normativa citada e a Portaria MTE n. 1.419, de 27 de agosto de 2024, que alterou a NR-1, e o encerramento do periodo de adaptacao em 26 de maio de 2026. Os cortes da matriz de risco usados aqui (ate 3 baixo, 4 a 8 medio, 9 a 14 alto, 15 ou mais critico) NAO vem da norma: sao um criterio de exemplo, e cada empresa define o seu e registra onde definiu. O agrupamento em seis familias de fator segue os guias de referencia usados na pratica, e nao uma lista fechada da norma. O intervalo de revisao do inventario esta na propria NR-1 e deve ser conferido no texto vigente. Este video e material educativo sobre construcao de planilha e organizacao de processo; nao e consultoria juridica nem parecer tecnico de saude e seguranca do trabalho.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-002",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "paleta": {"ink": "#101B2B", "c1": "#1D3557", "c2": "#E07A5F", "bg": "#F7F6F3"},
    "thumb": {"l1": "NR-1 PSICOSSOCIAL", "l2": "o inventario que falta"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    p = "fabrica/specs/labtreinamento-002.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    TAXA = 16.52          # pt-BR-ThalitaMultilingualNeural, medida
    chars = sum(len(c["nar"]) for c in CENAS)
    cs = sum(len(c["nar"]) for c in SHORT)
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {chars} | estimativa: {(chars/TAXA + 0.5*len(CENAS))/60:.1f} min")
    print(f"chars short: {cs} | estimativa: {cs/TAXA + 0.5*len(SHORT):.0f} s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
