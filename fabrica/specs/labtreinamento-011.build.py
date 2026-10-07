"""labtreinamento-011 — quantos da sua equipe estao com treinamento vencendo.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

NUMERO DE PARTIDA, do proprio canal. A trava do 549 passou nas duas partes:
catorze linhas com metrica, todos os deltas da ultima coleta contra o max
anterior POSITIVOS ou zero. O retrato SERVE.

    pacote                                      short   longo   travessia
    Por Hora ou por Projeto?                    1.132       3       0,27%
    INSS do Autonomo: 11% ou 20%?               1.111      35       3,2%
    FAP 2027: consulta abre em 30 de setembro      20      31        155%
    NR-10: o prazo termina em junho                21      18         86%
    [EXCEL] ISO 9001: planilha de transicao        28      14         50%
    [EXCEL] Riscos Psicossociais NR-1              26       9         35%

O QUE DEU CERTO, e e contraintuitivo o bastante para escrever: os dois shorts
GIGANTES deram as duas PIORES travessias, e os longos mais vistos do canal (31 e
35) vieram de shorts de VINTE views. O que esses dois tem no titulo e PRAZO
DATADO — "consulta abre em 30 de setembro", "o prazo termina em junho" — e o
terceiro melhor e uma ESCOLHA BINARIA no documento da pessoa ("11% ou 20%?").

O QUE NAO DEU: isca de planilha. Os tres pacotes "[EXCEL]" deram 14, 11 e 9
views de longo, os piores do canal. Quem vem pelo arquivo nao fica pelo metodo.

O QUE VOU MUDAR: juntar prazo datado com a conta no documento da pessoa, e tirar
qualquer isca de download do titulo.

PESQUISA DE TENDENCIA (obrigatoria). YouTube
`chart=mostPopular&regionCode=BR&videoCategoryId=26`, quinze itens, status 200 e
`error` ausente. **A 26 e PROXY e eu digo isso:** a categoria real de todos os
videos da frota e a 27 (Education), que nao tem chart em regiao nenhuma
(aprendizado 610).
O feed brasileiro estava com humor, Disney, squishy, crianca e cachorro. Zero
trabalho, zero seguranca.
GRAFEI A FORMA, DESCARTEI O ASSUNTO: "Como saber se tem alguem MEXENDO NO SEU
CELULAR" — COMO SABER SE ALGO QUE TE AFETA E VOCE NAO VE. Virou o titulo e a
promessa inteira: como saber quais treinamentos da sua equipe vencem antes do
fim do ano. Nao grafei celular, Disney nem squishy.

EIXO, e por que ele e novo. Os dez pacotes falam de NR-1, ISO 9001, NR-10, FAP,
INSS do autonomo, hora contra projeto, desconto como juro, FGTS e CAT. NENHUM
trata de CONTROLE DE VALIDADE — de saber, numa lista de pessoas, quem vence
quando. E o 010 usou "tres datas" para a CAT, entao este NAO repete esse
enquadramento: aqui o assunto e a lista da equipe, nao os campos de um documento.

VEREDITO DO CANAL: `suspenso` (v_maquina_licoes, sete shorts e sete longos
medidos). Piso de oito minutos e o melhor material NO SHORT. Pela colisao do
aprendizado 602, SETE capitulos de ~70 s, nao oito.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO AFIRMA NENHUMA PERIODICIDADE DE NORMA, e isso e a decisao de
# desenho, nao um descuido.
#
# POR QUE, e esta medido nesta rodada: a fonte brasileira NAO ABRIU. O
# `planalto.gov.br` esta inacessivel pelas TRES rotas que a maquina tem:
#   * `pg_net` do Supabase -> "Failure when receiving data from the peer", nas
#     quatro tentativas, inclusive com timeout de 55 s e em http simples;
#   * proxy deste container -> 403 no CONNECT;
#   * sandbox do Composio -> timeout de 20 s com zero bytes.
# E os sites do Ministerio do Trabalho sao renderizados por JavaScript: 200 com
# 201 KB e texto limpo vazio. A pagina de normas vigentes devolve 404.
#
# A rotina diz que pauta cujo numero nao fecha deve ser REDESENHADA para que o
# numero que decide seja o DO ESPECTADOR. Foi o que fiz, e e por isso que o
# video pede a periodicidade em vez de afirma-la:
#
#   "pegue a periodicidade que consta no SEU certificado ou no procedimento da
#    SUA empresa" — nao "a NR tal e bienal".
#
# Assim a unica coisa que o video afirma e ARITMETICA: data de realizacao mais
# periodicidade da uma data de vencimento, e vencimento menos hoje da os dias
# que faltam. Isso nao precisa de fonte porque nao e afirmacao sobre o mundo.
#
# O QUE EU NAO FIZ: nao citei de memoria que a NR-10 e bienal, nem qualquer
# outra periodicidade. Sei que varias sao, mas memoria nao e fonte, e a regra da
# casa e que numero sem duas fontes nao entra.
#
# =============================================================================
"""

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


BROLL = {
    4284181: ("https://videos.pexels.com/video-files/4284181/4284181-hd_1280_720_50fps.mp4",
              "Tiger Lily", "https://www.pexels.com/video/people-talking-in-the-warehouse-4284181/"),
    9057678: ("https://videos.pexels.com/video-files/9057678/9057678-hd_1920_1080_25fps.mp4",
              "SHVETS production", "https://www.pexels.com/video/a-person-encircling-the-date-on-the-calendar-9057678/"),
    8293501: ("https://videos.pexels.com/video-files/8293501/8293501-hd_1280_720_30fps.mp4",
              "RDNE Stock project", "https://www.pexels.com/video/a-man-writing-on-a-paper-in-a-clipboard-8293501/"),
    8479064: ("https://videos.pexels.com/video-files/8479064/8479064-hd_1920_1080_25fps.mp4",
              "ArtHouse Studio", "https://www.pexels.com/video/person-working-on-a-laptop-8479064/"),
    1793371: ("https://videos.pexels.com/video-files/1793371/1793371-hd_1920_1080_30fps.mp4",
              "Miguel A. Padrinan", "https://www.pexels.com/video/person-saving-a-date-on-his-planner-1793371/"),
    5100043: ("https://videos.pexels.com/video-files/5100043/5100043-hd_1920_1080_30fps.mp4",
              "Gustavo Fring", "https://www.pexels.com/video/man-working-on-the-construction-site-5100043/"),
    7816376: ("https://videos.pexels.com/video-files/7816376/7816376-hd_1920_1080_25fps.mp4",
              "Pavel Danilyuk", "https://www.pexels.com/video/a-realtor-doing-her-checklist-7816376/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor, "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — as duas contas inteiras, com as entradas nomeadas — abre o
# capitulo 2, que a estimativa poe perto dos 70 s. Vou medir a FRASE no
# legendas.srt depois do render.

# ---------------------------- 1 -------------------------------------- ~70 s
B("Quem vence primeiro", "e você não sabe dizer",
  "Se eu perguntar agora quantas pessoas da sua equipe estão com treinamento vencendo nos próximos noventa dias, você consegue responder sem abrir nada?",
  "people talking in a warehouse", 4284181, cap="Quem vence primeiro")
T("Quase ninguém consegue", "e não é desorganização",
  "Quase ninguém consegue, e não é desorganização. É que o certificado guarda a data de quando o treinamento aconteceu, não a data em que ele deixa de valer.")
T("A data que falta", "ninguém a escreve",
  "A data que interessa, a do vencimento, não está escrita em lugar nenhum. Ela precisa ser calculada, uma pessoa de cada vez.")
T("E some quando muda", "quem entra e quem sai",
  "E some de vista toda vez que alguém entra na equipe, muda de função ou volta de afastamento com um treinamento diferente do resto do time.")
T("O custo de descobrir tarde", "é sempre o mesmo",
  "Descobrir tarde custa sempre a mesma coisa: alguém parado esperando turma, ou um treinamento comprado com pressa pelo preço da urgência.")
T("O que este vídeo faz", "duas contas e uma lista",
  "Este vídeo resolve isso com duas contas curtas e uma lista que você monta agora e depois só revisa por mês.")
T("Não precisa de sistema", "nem de consultoria",
  "Não precisa de sistema, não precisa de consultoria e não precisa comprar nada. Papel e caneta resolvem para uma equipe pequena.")
T("E o aviso do começo", "sobre periodicidade",
  "Um aviso desde já: eu não vou dizer de quanto em quanto tempo cada treinamento se repete. Esse número vem do seu certificado, e explico o porquê no fim.")

# ---------------------------- 2 -------------------------------------- ~70 s
B("As duas contas", "e só isso",
  "Aqui estão as duas contas. A primeira: data em que o treinamento foi realizado, mais a periodicidade dele, dá a data de vencimento.",
  "a person encircling a date on the calendar", 9057678, cap="As duas contas")
T("A segunda", "vencimento menos hoje",
  "A segunda: data de vencimento menos a data de hoje dá quantos dias faltam. É esse número que você vai ordenar.")
T("Repare no que entra", "só coisa que você tem",
  "Repare no que entra nas duas: a data de realização, que está no certificado, e a periodicidade, que está no certificado ou no procedimento da empresa.")
T("Nenhuma entrada é minha", "todas são suas",
  "Nenhuma dessas entradas vem de mim. Todas vêm de um papel que você já tem guardado, e é isso que torna a conta confiável.")
T("Um exemplo", "com data redonda",
  "Um exemplo. Treinamento realizado em março do ano passado, periodicidade de dois anos. O vencimento cai em março do ano que vem.")
T("E os dias que faltam", "a conta que ordena",
  "Se hoje é outubro, faltam cerca de cinco meses. Esse é o número que coloca a pessoa em cima ou embaixo da sua lista.")
T("O erro mais comum", "usar a data de emissão",
  "O erro mais comum é usar a data de emissão do certificado em vez da data de realização. Elas podem estar separadas por semanas.")
T("Use sempre a realização", "e anote qual usou",
  "Use sempre a data da realização, e anote em algum lugar que foi ela que você usou. Isso evita refazer a conta daqui a seis meses.")

# ---------------------------- 3 -------------------------------------- ~70 s
B("O que ler no certificado", "três campos, não mais",
  "Agora o certificado. Você precisa de três campos dele, e só três, mesmo que o documento tenha vinte linhas de texto.",
  "a man writing on a paper in a clipboard", 8293501, cap="O que ler no certificado")
T("Campo um", "o nome da pessoa",
  "O primeiro é o nome de quem fez, escrito igual ao que está no seu cadastro, para você não acabar com a mesma pessoa em duas linhas.")
T("Campo dois", "a data de realização",
  "O segundo é a data em que o treinamento foi realizado, que às vezes aparece como período com início e fim. Nesse caso, use o fim.")
T("Campo três", "a periodicidade",
  "O terceiro é a periodicidade, ou seja, de quanto em quanto tempo ele precisa ser refeito. Costuma estar no rodapé ou no procedimento interno.")
T("Se não achar", "pergunte a quem ministrou",
  "Se a periodicidade não estiver no certificado, pergunte a quem ministrou ou veja no procedimento da sua empresa. Não chute esse número.")
T("Por que não chutar", "ele comanda tudo",
  "Não chute porque ele comanda as duas contas. Errar a periodicidade move a data de vencimento de uma pessoa em meses.")
T("A carga horária", "não entra aqui",
  "A carga horária não entra nesta conta. Ela importa para outras coisas, mas não muda quando o treinamento vence.")
T("Com três campos", "a linha está pronta",
  "Com esses três campos você já consegue escrever uma linha da lista. Repita para cada pessoa e a lista nasce sozinha.")

# ---------------------------- 4 -------------------------------------- ~70 s
B("A lista", "cinco colunas bastam",
  "A lista tem cinco colunas e cabe em qualquer planilha ou caderno. Nome, treinamento, data de realização, periodicidade e vencimento.",
  "person working on a laptop", 8479064, cap="A lista de cinco colunas")
T("A quinta é calculada", "as outras são copiadas",
  "As quatro primeiras você copia do certificado. A quinta é a única calculada, e sai da primeira conta que eu dei.")
T("Uma linha por pessoa", "e por treinamento",
  "Uma linha por pessoa e por treinamento. Quem fez três treinamentos ocupa três linhas, e isso é proposital.")
T("Por que separado", "porque vencem em datas diferentes",
  "É proposital porque cada treinamento vence na sua própria data. Juntar tudo numa linha por pessoa esconde exatamente o que você quer ver.")
T("Depois ordene", "pelo vencimento, crescente",
  "Terminada a lista, ordene pelo vencimento, do mais próximo para o mais distante. O topo da lista é a sua fila de trabalho.")
T("O que aparece no topo", "costuma surpreender",
  "O que aparece no topo costuma surpreender, porque raramente é quem você imaginava. Memória não ordena datas bem.")
T("Guarde num lugar só", "e combinado com alguém",
  "Guarde essa lista num lugar só, e combine com outra pessoa onde ela fica. Lista que mora na cabeça de uma pessoa some quando ela sai de férias.")
T("Revise por mês", "quinze minutos bastam",
  "Revise uma vez por mês. Com a lista pronta, a revisão é olhar o topo e conferir quem entrou na equipe desde a última vez.")

# ---------------------------- 5 -------------------------------------- ~70 s
B("A antecedência", "o número que você escolhe",
  "Falta um número, e esse é escolha sua: com quantos dias de antecedência você quer ser avisado antes de um treinamento vencer.",
  "person saving a date on a planner", 1793371, cap="A antecedência")
T("Por que precisa existir", "o dia do vencimento é tarde",
  "Esse número precisa existir porque descobrir no dia do vencimento não serve para nada. Você precisa de tempo para agir.")
T("De quanto tempo", "depende de duas coisas",
  "De quanto tempo depende de duas coisas suas: quanto demora para formar turma e quanto demora para a pessoa conseguir sair da operação.")
T("Meça, não estime", "olhe a última vez",
  "Em vez de estimar, olhe a última turma que você montou e conte os dias entre a decisão e a realização. Esse é o seu número real.")
T("Some uma folga", "porque algo sempre atrasa",
  "Some uma folga em cima dele, porque alguma coisa sempre atrasa. Se a última turma levou quarenta dias, trabalhar com sessenta é razoável.")
T("E aí a regra fica", "simples de aplicar",
  "A regra fica assim: tudo que vence dentro desse prazo entra na sua lista de ação agora, não no mês que vem.")
T("O resto só observa", "sem ansiedade",
  "O que vence depois você apenas observa. Essa separação é o que tira a ansiedade de olhar a lista inteira toda semana.")
T("Um número por treinamento", "se fizer sentido",
  "Se um treinamento específico for muito mais difícil de agendar, dê a ele uma antecedência maior. A regra não precisa ser igual para todos.")

# ---------------------------- 6 -------------------------------------- ~70 s
B("Quem entra na lista", "mais gente do que parece",
  "Falta decidir quem entra na lista, e aqui costuma faltar gente. Não é só quem está na operação hoje.",
  "man working on a construction site", 5100043, cap="Quem entra na lista")
T("Quem mudou de função", "pode precisar de outro",
  "Quem mudou de função pode precisar de um treinamento que não precisava antes, e o certificado antigo continua válido para a função antiga.")
T("Quem voltou de afastamento", "o tempo correu igual",
  "Quem voltou de afastamento longo entra também: o tempo correu para o certificado dele igual, mesmo sem ele estar trabalhando.")
T("Terceirizados e temporários", "se trabalham na sua área",
  "Terceirizados e temporários que trabalham na sua área entram na lista de controle, mesmo que o treinamento seja responsabilidade de outra empresa.")
T("Por que entram", "você precisa saber, não fazer",
  "Entram porque você precisa SABER a situação deles para liberar ou não uma atividade, mesmo quando não é você quem agenda o treinamento.")
T("Quem está de licença", "marque, não exclua",
  "Quem está de licença longa não some da lista. Marque a situação numa coluna de observação e deixe a linha lá.")
T("O risco de excluir", "é voltar sem ninguém notar",
  "O risco de excluir é a pessoa voltar e ninguém notar que o treinamento dela venceu no meio do afastamento.")
T("Regra simples", "quem pode executar, entra",
  "A regra simples é esta: se a pessoa pode ser escalada para a atividade, ela entra na lista. Decida pela possibilidade, não pela escala de hoje.")

# ---------------------------- 7 -------------------------------------- ~70 s
B("Quatro passos", "para esta semana",
  "Quatro passos, e todos cabem nesta semana. Comece pelo que der e vá completando, porque lista incompleta já é melhor que nenhuma.",
  "a person doing her checklist", 7816376, cap="Quatro passos")
T("Um", "junte os certificados",
  "Primeiro: junte os certificados da equipe num lugar só, digital ou físico, sem organizar nada ainda. Só juntar.")
T("Dois", "monte as cinco colunas",
  "Segundo: monte a lista de cinco colunas, uma linha por pessoa e por treinamento, copiando os três campos de cada certificado.")
T("Três", "calcule e ordene",
  "Terceiro: calcule o vencimento de cada linha e ordene do mais próximo para o mais distante. Só agora você tem a resposta da primeira pergunta.")
T("Quatro", "defina a antecedência",
  "Quarto: defina a sua antecedência olhando quanto tempo levou a última turma, some uma folga, e marque quem já entrou nesse prazo.")
T("Quem estiver faltando", "pergunte, não presuma",
  "Se faltar certificado de alguém, escreva o nome mesmo assim com um campo em branco. Linha em branco é visível; pessoa esquecida não é.")
T("Por que não dei prazos", "e isto é importante",
  "E agora o porquê do aviso do começo: eu não disse de quanto em quanto tempo cada treinamento se repete porque não consegui confirmar isso em fonte oficial hoje.")
T("Memória não é fonte", "então peguei o seu número",
  "Eu sei de cabeça várias dessas periodicidades, mas memória não é fonte. Por isso a conta usa o número que está no SEU papel.")
C("Conte quantos", "sem nomes, só o número",
  "Se você montar a lista, escreva nos comentários quantas pessoas apareceram dentro da sua antecedência. Sem nomes, só o número.")


# =============================== O SHORT =====================================
# `suspenso` manda o MELHOR MATERIAL para o short, e aqui o melhor material e a
# conta inteira — ela cabe em duas frases. O short entrega as duas contas e
# guarda para o longo a LISTA (as cinco colunas, a antecedencia e quem entra).
#
# A FORMA vem do que o proprio canal mediu, e esta no cabecalho: os dois shorts
# gigantes deram as piores travessias; os dois melhores tinham PRAZO DATADO no
# titulo. Entao o short abre com prazo datado ("antes do fim do ano") e fecha com
# o erro que invalida a conta — nao com "veja o video".
SHORT = [
    {"layout": "titulo", "kicker": "Antes do fim do ano",
     "sub": "quantos da sua equipe",
     "nar": "Quantas pessoas da sua equipe estão com treinamento vencendo "
            "antes do fim do ano? Quase ninguém sabe responder.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "E não é desorganização",
     "sub": "é a data que falta",
     "nar": "O certificado guarda a data em que o treinamento aconteceu, não a "
            "data em que ele deixa de valer.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A primeira conta",
     "sub": "uma linha, duas entradas",
     "nar": "Data de realização mais a periodicidade que consta no seu "
            "certificado dá a data de vencimento.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A segunda", "sub": "e é ela que ordena",
     "nar": "Vencimento menos hoje dá os dias que faltam. Ordene do menor para "
            "o maior e a resposta aparece.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "O erro que derruba tudo",
     "sub": "e quase todo mundo comete",
     "nar": "Quem usa a data de emissão em vez da data de realização erra por "
            "semanas. A lista inteira está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Quem vence", "l2": "antes de dezembro"}

COPY = """# labtreinamento-011

## TITULO
Quantos da Sua Equipe Estão com Treinamento Vencendo Antes do Fim do Ano? Duas Contas e Uma Lista

## TITULO SHORT
Quem da sua equipe vence antes de dezembro?

## DESCRICAO
Se alguém perguntar agora quantas pessoas da sua equipe estão com treinamento vencendo nos próximos noventa dias, você consegue responder sem abrir nada? Quase ninguém consegue, e não é desorganização. É que o certificado guarda a data em que o treinamento FOI REALIZADO, não a data em que ele deixa de valer. A data que interessa não está escrita em lugar nenhum: ela precisa ser calculada, uma pessoa de cada vez.

Este vídeo resolve isso com duas contas de uma linha cada e uma lista que você monta uma vez e revisa por mês. A primeira conta: data de realização mais a periodicidade dá a data de vencimento. A segunda: data de vencimento menos a data de hoje dá os dias que faltam — e é esse número que ordena a lista. Repare no que entra nas duas contas: a data de realização, que está no certificado, e a periodicidade, que está no certificado ou no procedimento da sua empresa. Nenhuma das duas entradas vem daqui.

E é aqui que vai o aviso mais importante desta descrição, dito antes de qualquer outra coisa: ESTE VÍDEO NÃO AFIRMA DE QUANTO EM QUANTO TEMPO NENHUM TREINAMENTO SE REPETE. Não porque o assunto seja delicado, mas porque hoje eu não consegui confirmar nenhuma periodicidade em fonte oficial — o texto das normas não abriu por nenhuma das vias que eu tenho, e o detalhe técnico disso está escrito no bloco AVISO SOBRE OS NÚMEROS, mais abaixo. Eu sei de cabeça várias dessas periodicidades, e isso não basta: memória não é fonte. Então a conta deste vídeo usa o número que está no SEU papel, e a única coisa que o vídeo afirma é aritmética — somar e subtrair datas.

O que o vídeo cobre, nos sete capítulos: as duas contas com as entradas nomeadas e um exemplo de data redonda; os três campos que você precisa ler no certificado, e só três, mesmo que o documento tenha vinte linhas; a lista de cinco colunas — pessoa, treinamento, data de realização, periodicidade e vencimento calculado — uma linha por pessoa E por treinamento, nunca uma linha por pessoa; como definir a sua antecedência olhando quanto tempo levou a última turma e somando uma folga, em vez de copiar um prazo de alguém; quem entra na lista, que é mais gente do que parece (quem mudou de função, quem voltou de afastamento longo, terceirizados e temporários que trabalham na sua área); e quatro passos que cabem nesta semana.

Uma ressalva: este conteúdo é informativo e não é consultoria de segurança do trabalho, não avalia a situação da sua empresa e não diz se a sua equipe está ou não em conformidade com qualquer norma. Decidir isso é trabalho de profissional habilitado, com o texto da norma na mão.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
As duas contas estão no primeiro minuto e meio, então não é preciso ver o vídeo inteiro para pegá-las: data de REALIZAÇÃO do treinamento mais a periodicidade que consta no seu certificado dá a data de vencimento; vencimento menos hoje dá os dias que faltam, e é por esse número que a lista se ordena. O erro mais comum é usar a data de EMISSÃO do certificado no lugar da data de realização — as duas podem estar separadas por semanas. E o aviso que eu repito dentro do vídeo: eu não digo aqui de quanto em quanto tempo cada treinamento se repete, porque hoje não consegui confirmar isso em fonte oficial, e memória não é fonte. Esse número é o único que vem do seu papel. Se você montar a lista, escreva nos comentários quantas pessoas apareceram dentro da sua antecedência — sem nomes, só o número.

## HASHTAGS
#SegurancaDoTrabalho #ControleDeTreinamentos #LabTreinamento

## TAGS
controle de treinamentos, vencimento de treinamento, validade de certificado, data de realizacao, reciclagem de treinamento, planilha de controle de treinamento, gestao de equipe, seguranca do trabalho, SST, matriz de treinamento, antecedencia de agendamento, terceirizados treinamento, controle de validade, lab treinamento, organizacao de equipe

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pt-BR
defaultAudioLanguage: pt-BR
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}
B-roll: Pexels, creditos por clipe em broll_creditos.json e abaixo.
Tiger Lily; SHVETS production; RDNE Stock project; ArtHouse Studio;
Miguel A. Padrinan; Gustavo Fring; Pavel Danilyuk.

## AVISO SOBRE OS NUMEROS
ZERO AFIRMACAO SOBRE O MUNDO. Este video nao cita periodicidade de norma, nao
cita numero de NR, nao cita prazo legal, nao cita multa, nao cita estatistica de
acidente e nao cita preco de treinamento. O que ele afirma e SO ARITMETICA: data
mais periodicidade da uma data; data menos data da um numero de dias. Isso nao
precisa de fonte porque nao e afirmacao sobre o mundo — e a operacao que o
espectador faz com os numeros DELE.

POR QUE DESENHEI ASSIM, e esta medido nesta rodada: a fonte nao abriu. O
`planalto.gov.br` esta inacessivel pelas TRES rotas que a maquina tem:
  * `pg_net` do Supabase -> "Failure when receiving data from the peer", nas
    quatro tentativas, inclusive com timeout de 55 s e em http simples;
  * proxy deste container -> 403 no CONNECT;
  * sandbox do Composio -> timeout de 20 s com zero bytes.
E os sites do Ministerio do Trabalho sao renderizados por JavaScript: 200 com
201 KB e texto limpo vazio; a pagina de normas vigentes devolve 404.

O QUE FOI DESCARTADO, e vai escrito porque a regra da casa e que o descarte
tambem se declara: (1) a periodicidade de qualquer treinamento — eu sei de
cabeca que varias sao bienais, e memoria nao e fonte, entao nao entrou nenhuma;
(2) o numero e o nome de qualquer NR, porque citar a norma sem poder ler o texto
dela hoje seria afirmar de memoria; (3) o prazo em que o treinamento vencido
impede a atividade, que depende do texto da norma e do procedimento da empresa;
(4) qualquer juizo sobre conformidade, que e trabalho de profissional habilitado.

O NUMERO QUE DECIDE E DO ESPECTADOR, e aqui ele e o unico numero do video: a
periodicidade sai do certificado ou do procedimento da empresa dele, a data de
realizacao sai do mesmo papel, e a antecedencia sai de quanto tempo levou a
ultima turma que ele mesmo agendou.

## FONTES
NENHUMA FONTE NORMATIVA E CITADA, e isso e deliberado — ver o bloco acima. As
unicas "fontes" deste video sao os documentos do proprio espectador: o
certificado de treinamento (data de realizacao e periodicidade) e o procedimento
interno da empresa dele. Os hosts oficiais testados e que NAO abriram nesta
rodada estao nomeados no AVISO SOBRE OS NUMEROS.
B-roll: Pexels, licenca Pexels, creditos por clipe em broll_creditos.json.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-011",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/labtreinamento-011.json")
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
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "coloca a pessoa em cima ou embaixo" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
