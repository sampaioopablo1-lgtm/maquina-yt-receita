#!/usr/bin/env python3
"""Monta a spec labtreinamento-005.

ALAVANCA ATACADA: **A — conversao short -> inscrito**. Numero de partida
brutal e sem ambiguidade: **ZERO**. Oito videos publicados, 75 views somadas,
nenhum inscrito.

O QUE DEU CERTO, e e o unico sinal que este canal produziu ate agora. Medido
em 25/08/2026, longo a longo:

    labtreinamento-004  NR-10, "o prazo termina em junho de 2027"   3,22 v/d
    labtreinamento-003  "[EXCEL] ISO 9001:2026 — Planilha ..."      0,94 v/d
    labtreinamento-001  "[EXCEL] Planilha de Riscos ... NR-1"       0,46 v/d
    labtreinamento-002  "[EXCEL] Planilha de Riscos ... NR-1"       0,27 v/d

O unico longo SEM o formato "[EXCEL] Planilha" fez 3,22 views/dia; os tres de
planilha somam mediana 0,46. Cinco virgula oito vezes. E ele e o unico que
anuncia um PRAZO.

Uma ressalva honesta: n=1 no vencedor, e eu nao consigo separar "eixo NR-10" de
"forma de prazo" com um caso so. Por isso esta rodada muda o EIXO e mantem a
FORMA — se o proximo prazo tambem subir, a forma fica provada; se cair, o
credito era do eixo. E isso e desenho de experimento, nao palpite.

O QUE NAO DEU: tudo o mais. Zero inscritos em oito videos. Retencao dos dois
mais recentes em 12,0% e 12,6%, contra 3,1% e 4,0% dos dois primeiros — o canal
melhorou e mesmo assim ninguem assina.

O QUE VOU MUDAR POR CAUSA DISSO, e sao tres coisas:

  1. EIXO NOVO, que e o que o veredito manda. `v_maquina_licoes` diz
     `canal frio`, e a regra do canal frio e eixo novo, nao mais um video igual.
     Os oito publicados cobrem NR-1 (duas vezes), ISO 9001 e NR-10. FAP e RAT,
     nunca — e e o numero que transforma seguranca do trabalho em dinheiro na
     folha, que e exatamente a ponte que falta neste canal.

  2. A FORMA QUE MEDIU MELHOR: prazo datado no titulo. Aqui ele nao e retorico,
     e o calendario oficial: consulta em 30/09/2026, contestacao de 1 a 30/11.

  3. A CONTA NA SEGUNDA PESSOA (aprendizado 487, medido hoje no setiap-level).
     Nao basta ser metodo: o numero tem de sair de um documento que o
     espectador TEM. Aqui saem tres — o FAP do proprio estabelecimento no
     FAPWeb, o RAT do proprio CNAE, e a propria folha mensal. O short entrega
     a multiplicacao inteira, nao a manchete.

DURACAO. `canal frio` nao tem faixa no veredito, entao vale o piso duro de 8
min. E a alavanca B empurra para o piso: neste canal os segundos vistos ficam
em 86 e 103 (nao nos ~200 do kolejny-poziom), entao alongar so derruba a
retencao. Alvo: pouco acima de 8:30.

--------------------------------------------------------------------- A PAUTA

FONTES INSTITUCIONAIS, duas independentes que se confirmam:

  1. MINISTERIO DA PREVIDENCIA SOCIAL (gov.br/previdencia, com espelho no
     gov.br/inss):
       FAP e multiplicador de 0,5000 a 2,0000 sobre a aliquota RAT.
       FAP com vigencia para 2027 .... disponivel para consulta em
                                       30 de setembro de 2026.
       Contestacao ................... de 1 a 30 de novembro, eletronica,
                                       por formulario no FAPWeb.
       Quem analisa .................. o Conselho de Recursos da Previdencia
                                       Social (CRPS), conforme a Lei 13.846,
                                       de 18 de junho de 2019.
       Efeito suspensivo ............. NAO TEM. O FAP divulgado se aplica
                                       enquanto a contestacao e analisada.
       Acesso ........................ restrito ao estabelecimento, por senha
                                       gov.br.

  2. RECEITA FEDERAL (pagina do FAP em receita.economia.gov.br), que publica a
     legislacao, as perguntas frequentes e os dados da empresa:
       RAT e de 1% para risco minimo, 2% para medio e 3% para grave, sobre a
       remuneracao total paga aos segurados empregados e trabalhadores avulsos
       no mes.

A CONTA, e ela e o coracao do video e do short. Aliquota efetiva = RAT x FAP.
Numa folha mensal de 100.000 reais, com RAT de 2%:

    FAP 0,5 ...... aliquota 1,0% ...... 1.000 reais por mes
    FAP 1,0 ...... aliquota 2,0% ...... 2.000 reais por mes
    FAP 2,0 ...... aliquota 4,0% ...... 4.000 reais por mes

Mesma folha, mesmo CNAE, mesma atividade: 3.000 reais de diferenca por mes,
36.000 por ano, decididos so pelo historico de acidentes. E o teto e quatro
vezes o piso.

O QUE O VIDEO NAO FAZ: nao diz qual e o FAP de ninguem (o acesso e restrito ao
estabelecimento), nao promete resultado de contestacao, e nao substitui
contador nem assessoria juridica.

ACENTOS. Portugues com toda a acentuacao; numeros por extenso, porque o TTS
soletra digito cru errado.
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


# ============================ OS PRIMEIROS 200 SEGUNDOS ======================
# Onde achar o proprio FAP e como transformar em reais sai nos capitulos 1 a 3.

# ------------------------------------------------------------------- cap 1
T("Um multiplicador", "na folha da sua empresa",
  "Existe um multiplicador aplicado sobre uma contribuição da folha da sua "
  "empresa, e ele muda todo ano sem que ninguém avise.",
  cap="O multiplicador que ninguém mostra")
I("O nome dele", "Fator Acidentário de Prevenção",
  "O nome completo é Fator Acidentário de Prevenção, e quase todo mundo do "
  "setor conhece pela sigla FAP. Se você trabalha com segurança do trabalho, "
  "provavelmente já ouviu falar sem nunca ter aberto o número.")
I("A faixa", "de zero vírgula cinco a dois",
  "Ele vai de zero vírgula cinco a dois vírgula zero. É um número por "
  "estabelecimento, calculado pela Previdência.")
I("O que ele faz", "multiplica o seu RAT",
  "Esse número multiplica a alíquota do seguro de acidente do trabalho que a "
  "sua empresa já paga.")
I("Ou seja", "a mesma folha, contas diferentes",
  "Duas empresas com a mesma folha e a mesma atividade podem recolher valores "
  "bem diferentes. A diferença é o histórico de acidentes.")
I("É por estabelecimento", "não por empresa",
  "Um detalhe que muda a conta de quem tem mais de uma unidade: o índice é "
  "atribuído por estabelecimento, e não à empresa como um todo.")
I("Ou seja", "cada unidade tem o seu",
  "Duas filiais da mesma empresa podem receber índices diferentes, porque "
  "cada uma carrega o próprio histórico.")
I("E ele já está pronto", "calculado sobre o seu passado",
  "O cálculo do próximo ano já está sendo feito, sobre o que aconteceu na sua "
  "empresa. Ele não espera você olhar.")

# ------------------------------------------------------------------- cap 2
T("Onde ver o seu", "e a partir de quando",
  "Primeira coisa prática: onde você vê o número da sua própria empresa.",
  cap="Onde consultar o seu FAP")
I("O sistema", "FAPWeb",
  "A consulta é feita no sistema da Previdência chamado FAPWeb, e o mesmo "
  "índice também aparece pela Receita Federal. Não é serviço pago e não "
  "precisa de intermediário.")
I("O acesso", "senha gov ponto br",
  "O acesso é por senha do portal do governo, e é restrito ao próprio "
  "estabelecimento. Ninguém consulta o FAP de terceiros.")
I("A data", "trinta de setembro",
  "O FAP com vigência para dois mil e vinte e sete fica disponível para "
  "consulta em trinta de setembro de dois mil e vinte e seis.")
I("O que aparece lá", "o índice e a memória de cálculo",
  "Na consulta aparece o índice atribuído ao estabelecimento e os dados "
  "usados no cálculo. É essa memória que sustenta qualquer questionamento.")
I("A memória de cálculo", "é o que sustenta contestação",
  "Vale insistir nessa parte. Sem olhar a memória de cálculo, uma contestação "
  "vira opinião, e opinião não muda índice.")
I("Quem não consulta", "descobre no recolhimento",
  "Quem não consulta acaba descobrindo o índice pelo valor recolhido em "
  "janeiro, quando o prazo de contestação já fechou.")
I("Anote dois números", "o FAP e a data",
  "Anote o índice e o dia em que você consultou. Os dois vão importar em "
  "novembro, e eu explico por quê mais adiante.")

# ------------------------------------------------------------------- cap 3
T("Transforme em reais", "duas multiplicações",
  "Segunda coisa prática, e é aqui que o número vira dinheiro.",
  cap="Como transformar o FAP em reais")
I("Ache o seu RAT", "pelo CNAE",
  "Antes do FAP, ache a sua alíquota RAT. Ela vem da atividade da empresa, "
  "pelo CNAE.")
I("São três valores", "um, dois ou três por cento",
  "São três possibilidades, e elas seguem o grau de risco da atividade. "
  "Risco mínimo paga um por cento. Risco médio paga dois por cento. E risco "
  "grave paga três por cento.")
I("Sobre o quê", "a remuneração total do mês",
  "Essa alíquota incide sobre a remuneração total paga no mês aos empregados "
  "e aos trabalhadores avulsos.")
I("Primeira multiplicação", "RAT vezes FAP",
  "Agora multiplique: RAT vezes FAP. O resultado é a sua alíquota efetiva, "
  "que é a que realmente sai da folha.")
I("Segunda multiplicação", "pela sua folha",
  "Multiplique a alíquota efetiva pela sua folha mensal. Esse é o valor que o "
  "histórico de acidentes custa por mês.")
I("O nome do resultado", "RAT ajustado",
  "Muita gente chama esse resultado de RAT ajustado. É o mesmo número: a "
  "alíquota depois do multiplicador.")
I("Cuidado com a ordem", "primeiro multiplica, depois aplica",
  "A ordem importa na hora de conferir: primeiro se multiplica a alíquota "
  "pelo fator, e só então se aplica sobre a folha.")
I("Pronto", "o método acabou",
  "Esse é o método inteiro. O resto do vídeo é o exemplo em reais, o "
  "calendário, e o que a contestação alcança.")

# ============ ate aqui, ~200 segundos. O que segue aprofunda. ===============

# ------------------------------------------------------------------- cap 4
T("Em reais", "uma folha de cem mil",
  "Vamos pôr números redondos, porque em porcentagem ninguém sente.",
  cap="O exemplo em reais")
I("A empresa do exemplo", "risco médio",
  "Uma empresa com folha mensal de cem mil reais e atividade de risco médio, "
  "ou seja, RAT de dois por cento.")
I("Com FAP um", "dois mil por mês",
  "Se o FAP dela for um vírgula zero, a alíquota efetiva continua em dois por "
  "cento, e o recolhimento fica em dois mil reais por mês.")
I("Com FAP mínimo", "mil por mês",
  "Se o FAP for zero vírgula cinco, a alíquota cai para um por cento, e o "
  "valor cai para mil reais por mês.")
I("Com FAP máximo", "quatro mil por mês",
  "E se o FAP for dois vírgula zero, a alíquota sobe para quatro por cento, e "
  "o valor vai a quatro mil reais por mês.")
B("Mesma folha, mesmo CNAE", ["FAP 0,5", "FAP 1,0", "FAP 2,0"], [25, 50, 100],
  "Mesma folha, mesma atividade, mesmo mês. A diferença entre o piso e o teto "
  "é de três mil reais.")
I("No ano", "trinta e seis mil",
  "Ao longo de um ano isso são trinta e seis mil reais de diferença, "
  "decididos pelo histórico de acidentes e por mais nada.")
I("Se o risco for grave", "a diferença abre mais",
  "Numa empresa de risco grave, com RAT de três por cento, a mesma folha vai "
  "de mil e quinhentos reais no piso a seis mil no teto.")
I("Nesse caso", "quatro mil e quinhentos por mês",
  "A diferença mensal passa de quatro mil e quinhentos reais, e o ano fecha "
  "acima de cinquenta mil.")
I("Por isso importa", "segurança vira linha de custo",
  "É por isso que este número interessa a quem cuida de segurança: ele é a "
  "linha que liga prevenção a custo de folha.")

# ------------------------------------------------------------------- cap 5
T("O calendário", "duas datas",
  "Agora as duas datas, e elas são diferentes uma da outra.",
  cap="As duas datas do calendário")
I("Primeira data", "trinta de setembro",
  "Em trinta de setembro abre a consulta. É quando você descobre o índice que "
  "vai valer no ano seguinte.")
I("Segunda data", "primeiro a trinta de novembro",
  "De primeiro a trinta de novembro corre o prazo de contestação. São trinta "
  "dias, e só nesse período.")
I("Entre uma e outra", "um mês para conferir",
  "Entre as duas datas você tem cerca de um mês para conferir a memória de "
  "cálculo antes de decidir se contesta. Esse intervalo existe de propósito, "
  "e é o único momento confortável do calendário inteiro.")
I("O que fazer em outubro", "conferir, não esperar",
  "Outubro é o mês de trabalho: conferir os dados do cálculo, comparar com os "
  "próprios registros de acidente e afastamento, e decidir.")
I("O prazo não reabre", "trinta dias e acabou",
  "E é bom saber que esse prazo não reabre. Passou trinta de novembro, o "
  "índice segue valendo pelo ano inteiro.")
I("Como se contesta", "só por meio eletrônico",
  "A contestação é feita exclusivamente por meio eletrônico, em formulário "
  "disponível no próprio FAPWeb.")
I("Quem julga", "o CRPS",
  "Quem analisa é o Conselho de Recursos da Previdência Social, conforme a "
  "lei de dois mil e dezenove que definiu esse rito.")

# ------------------------------------------------------------------- cap 6
T("O detalhe caro", "contestar não suspende",
  "E agora o detalhe que costuma pegar as empresas de surpresa.",
  cap="Contestar não suspende a cobrança")
I("Sem efeito suspensivo", "o índice vale enquanto isso",
  "A contestação não tem efeito suspensivo. O FAP divulgado continua sendo "
  "aplicado enquanto o pedido é analisado.")
I("Ou seja", "você paga e discute",
  "Na prática, você recolhe pelo índice divulgado e discute em paralelo. "
  "Contestar não é uma pausa no pagamento, e essa é a parte que costuma "
  "aparecer tarde demais nas reuniões de orçamento.")
I("O que isso muda", "planeje o caixa",
  "Isso muda o planejamento: se o seu índice subiu, o custo maior começa "
  "junto com o ano, independente da contestação.")
I("E se der certo", "o acerto vem depois",
  "Se a contestação for acolhida, o ajuste acontece depois. Mas o fluxo de "
  "caixa do começo do ano já terá acontecido.")
I("No caixa", "provisione pelo índice divulgado",
  "Para o financeiro isso tem nome: a provisão do ano se faz pelo índice "
  "divulgado, não pelo índice que você espera conseguir.")
I("Contestar continua valendo", "só não é pausa",
  "Nada disso quer dizer que não vale contestar. Quer dizer que contestar e "
  "planejar o caixa são duas coisas separadas.")
I("Por isso a conta", "vem antes da discussão",
  "Por isso a conta que fizemos importa: ela te diz o tamanho do impacto "
  "antes de você decidir se vale contestar.")

# ------------------------------------------------------------------- cap 7
T("De onde vêm", "duas fontes oficiais",
  "De onde saíram estes números, porque essa pergunta cabe sempre.",
  cap="De onde vêm os números")
I("Primeira fonte", "Ministério da Previdência Social",
  "A faixa do multiplicador, as datas de consulta e de contestação, o rito no "
  "conselho e a ausência de efeito suspensivo vêm do Ministério da "
  "Previdência Social.")
I("Segunda fonte", "Receita Federal",
  "As alíquotas RAT de um, dois e três por cento e a base de incidência sobre "
  "a remuneração do mês vêm da página do FAP na Receita Federal.")
I("São dois órgãos", "e isso não é detalhe",
  "Repare que são dois órgãos diferentes: o multiplicador e o calendário "
  "estão na Previdência, e a alíquota base está na Receita.")
I("Por isso cito os dois", "cada um no que é dele",
  "Por isso eu cito os dois, cada um na parte que é dele. Misturar as fontes "
  "é como um número acaba atribuído a quem nunca o publicou.")
I("Como conferir sozinho", "duas buscas",
  "Você confere sem intermediário com duas buscas: fator acidentário de "
  "prevenção no site da Previdência, e FAP no site da Receita Federal.")
I("O que eu não uso", "portal de dicas",
  "Não usei calculadora de internet nem portal de dicas. Número que não está "
  "em fonte oficial não entra aqui.")
I("Por que insisto", "aqui o erro é caro",
  "Em matéria de recolhimento, errar não é curiosidade: quem paga a conta é "
  "quem seguiu a informação. Prefiro dizer menos e ter conferido.")

# ------------------------------------------------------------------- cap 8
T("Esta semana", "três coisas",
  "Três coisas que dá para fazer esta semana, antes mesmo de a consulta abrir.",
  cap="O que fazer esta semana")
I("Primeira", "confirme o seu RAT",
  "Confirme a alíquota RAT da sua empresa pelo CNAE. Um, dois ou três por "
  "cento, e anote qual é.")
I("Segunda", "pegue a folha do mês",
  "Pegue a remuneração total do último mês. Esse é o número que você vai "
  "multiplicar quando o índice sair.")
L("Terceira", ["Meu RAT é",
               "Minha folha do mês é",
               "Se o FAP vier em dois, eu pago"],
  "E deixe três linhas escritas: meu RAT, minha folha do mês, e quanto eu "
  "pagaria se o índice viesse no teto.")
I("A terceira linha", "é o pior caso",
  "A terceira linha é o pior caso calculado com antecedência. Em trinta de "
  "setembro você só compara com o número real.")
I("Guarde junto", "o print da memória de cálculo",
  "Quando a consulta abrir, guarde também a memória de cálculo em arquivo. "
  "Ela é o ponto de partida de qualquer discussão em novembro.")
I("Resumindo", "duas multiplicações e duas datas",
  "Resumindo: alíquota efetiva é RAT vezes FAP, o custo do mês é isso vezes a "
  "folha, a consulta abre em trinta de setembro e a contestação fecha em "
  "trinta de novembro.")
C("LabTreinamento", "faça a sua conta",
  "Faça hoje uma coisa só: calcule quanto a sua empresa pagaria com o índice "
  "no teto, e guarde o número. Aqui a gente pega um número da sua rotina "
  "técnica e transforma em uma conta que você mesmo faz. Se é isso que você "
  "procura, se inscreve.")


# -------------------------------------------------------------------- short
#
# ENTREGA A MULTIPLICACAO INTEIRA, na segunda pessoa, com os tres numeros que
# o espectador TEM: o RAT do CNAE dele, a folha dele, e o FAP do
# estabelecimento dele. Aprendizado 487.
SHORT = [
    {"layout": "titulo", "kicker": "Um multiplicador", "sub": "de 0,5 a 2,0",
     "nar": "A sua empresa tem um multiplicador entre zero vírgula cinco e "
            "dois vírgula zero que ninguém te mostrou.", "sem_cap": True},
    {"layout": "item", "kicker": "Pegue o seu RAT", "preco": "1, 2 ou 3 por cento",
     "nar": "Pegue a sua alíquota RAT pelo CNAE: um, dois ou três por cento.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Multiplique pelo FAP", "preco": "sua alíquota real",
     "nar": "Multiplique pelo FAP do seu estabelecimento. O resultado é a "
            "alíquota que realmente sai da sua folha.", "sem_cap": True},
    {"layout": "item", "kicker": "Numa folha de cem mil", "preco": "três mil de diferença",
     "nar": "Com RAT de dois por cento, a diferença entre o piso e o teto é de "
            "três mil reais por mês na mesma folha.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "consulta em 30/09",
     "nar": "A consulta abre em trinta de setembro. Calcule o seu pior caso "
            "antes disso e guarde o número.", "sem_cap": True},
]

COPY = """# FAP 2027: consulta em 30 de setembro e o multiplicador de 0,5 a 2,0

## TITULO
FAP 2027: Consulta Abre em 30 de Setembro e o Multiplicador Vai de 0,5 a 2,0

## DESCRICAO
Existe um multiplicador aplicado sobre uma contribuição da folha da sua empresa que muda todo ano e quase nunca é olhado a tempo: o FAP, Fator Acidentário de Prevenção. Ele vai de 0,5000 a 2,0000, é calculado por estabelecimento e multiplica a alíquota do seguro de acidente do trabalho. Duas empresas com a mesma folha e a mesma atividade podem recolher valores muito diferentes — a diferença é o histórico de acidentes. Este vídeo mostra onde consultar o índice da sua própria empresa, como transformá-lo em reais com duas multiplicações, e quais são as duas datas do calendário.

ONDE CONSULTAR (fonte: Ministério da Previdência Social)

A consulta é feita no sistema FAPWeb e também está disponível pela Receita Federal. O acesso é por senha gov.br e é restrito ao próprio estabelecimento. O FAP com vigência para 2027 fica disponível para consulta em 30 de setembro de 2026. Na consulta aparecem o índice atribuído e os dados usados no cálculo — é essa memória de cálculo que sustenta qualquer questionamento.

AS DUAS MULTIPLICAÇÕES

1) Ache a sua alíquota RAT pelo CNAE: 1% para risco mínimo, 2% para risco médio, 3% para risco grave, incidindo sobre a remuneração total paga no mês aos empregados e trabalhadores avulsos (fonte: Receita Federal). 2) Alíquota efetiva = RAT × FAP. 3) Custo do mês = alíquota efetiva × folha mensal.

O EXEMPLO EM REAIS

Empresa com folha mensal de R$100.000 e RAT de 2%. Com FAP 1,0 a alíquota efetiva é 2% e o recolhimento é R$2.000/mês. Com FAP 0,5 a alíquota cai para 1% e o valor cai para R$1.000/mês. Com FAP 2,0 a alíquota sobe para 4% e o valor vai a R$4.000/mês. Mesma folha, mesma atividade, mesmo mês: R$3.000 de diferença mensal, R$36.000 por ano, decididos pelo histórico de acidentes.

O CALENDÁRIO E O DETALHE QUE PEGA AS EMPRESAS

A consulta abre em 30 de setembro de 2026. A contestação corre de 1º a 30 de novembro, exclusivamente por meio eletrônico, em formulário disponível no FAPWeb, e é analisada pelo Conselho de Recursos da Previdência Social (CRPS), conforme a Lei nº 13.846, de 18 de junho de 2019. E o ponto que costuma surpreender: a contestação NÃO tem efeito suspensivo. O FAP divulgado continua sendo aplicado enquanto o pedido é analisado — na prática, a empresa recolhe pelo índice divulgado e discute em paralelo. Se o índice subiu, o custo maior começa junto com o ano.

O QUE ESTE VÍDEO NÃO FAZ: não informa o FAP de nenhuma empresa (o acesso é restrito ao estabelecimento), não promete resultado de contestação, e não substitui contador nem assessoria jurídica.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faça a conta do pior caso antes de 30 de setembro e escreva um número aqui: quanto a sua empresa pagaria por mês se o FAP viesse em 2,0. Não precisa dizer a folha nem o nome da empresa — só o valor. Quero ver quantos aqui têm um impacto de cinco dígitos por ano escondido num índice que ninguém abriu ainda.

## HASHTAGS
#FAP #SegurancaDoTrabalho #LabTreinamento

## TAGS
fap 2027, fator acidentario de prevencao, fapweb, rat, seguro acidente do trabalho, aliquota rat, contestacao fap, crps, folha de pagamento, cnae, seguranca do trabalho, sesmt, custo de acidente, previdencia social, gestao de sst

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Os numeros vem de DUAS fontes institucionais independentes que se confirmam. (1) MINISTERIO DA PREVIDENCIA SOCIAL (gov.br/previdencia, com espelho no gov.br/inss): o FAP e um multiplicador de 0,5000 a 2,0000 sobre a aliquota RAT, calculado por estabelecimento; o FAP com vigencia para 2027 fica disponivel para consulta em 30 de setembro de 2026; a contestacao corre de 1 a 30 de novembro, exclusivamente por meio eletronico em formulario do FAPWeb, e e analisada pelo Conselho de Recursos da Previdencia Social (CRPS) conforme a Lei 13.846, de 18 de junho de 2019; a contestacao NAO tem efeito suspensivo, de modo que o indice divulgado se aplica durante a analise; o acesso e restrito ao estabelecimento, por senha gov.br. (2) RECEITA FEDERAL (pagina do FAP em receita.economia.gov.br, com legislacao, perguntas frequentes e dados da empresa): a aliquota RAT e de 1% para risco minimo, 2% para risco medio e 3% para risco grave, incidente sobre a remuneracao total paga no mes aos segurados empregados e trabalhadores avulsos. O EXEMPLO EM REAIS FOI DERIVADO dessas duas fontes, nao copiado: folha de 100.000 reais com RAT de 2% da 2.000 reais/mes com FAP 1,0; 1.000 reais/mes com FAP 0,5; e 4.000 reais/mes com FAP 2,0 — 3.000 reais de diferenca mensal e 36.000 por ano entre o piso e o teto, na mesma folha e no mesmo CNAE. NAO foi usada nenhuma calculadora de internet nem portal de dicas. O video diz em voz alta que nao informa o FAP de nenhuma empresa, que nao promete resultado de contestacao e que nao substitui contador nem assessoria juridica.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/labtreinamento-005.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-005",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#16222F", "c1": "#0F6E8C", "c2": "#E0A02E",
               "bg": "#F1F5F7"},
    "thumb": {"l1": "FAP 2027", "l2": "0,5 a 2,0"},
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
    grava(SPEC, "fabrica/specs/labtreinamento-005.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
