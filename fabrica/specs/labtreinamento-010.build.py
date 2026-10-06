"""labtreinamento-010 — tres datas candidatas e um dia util.

ALAVANCA ATACADA: A (forma: metodo sobre o documento do espectador).

NUMERO DE PARTIDA, lido AO VIVO na `videos.list` em 06/10/2026 23:16, casado
por `item->>'id'`, ordenado por VIEWS DE LONGO (aprendizado 598):

    pacote  short  longo  trav.   dur     titulo
    006      1111     35    3,2%  515,7   INSS do Autonomo: 11% ou 20%? A escolha na SUA guia
    005        22     32  145,5%  554,0   FAP 2027: consulta abre em 30 de setembro
    004        21     18   85,7%  717,2   NR-10 atualizada: o prazo termina em junho de 2027
    008       215     15    7,0%  539,4   Desconto a vista: divida por 90
    003        28     14   50,0%  822,3   [EXCEL] ISO 9001:2026
    001         4     11  275,0%  785,0   [EXCEL] Riscos psicossociais NR-1
    002        26      9   34,6%  871,6   [EXCEL] Riscos psicossociais NR-1 (mesmo assunto)
    007      1132      3    0,3%  520,6   Por hora ou por projeto? a conta no seu orcamento
    009         9      3   33,3%  614,0   FGTS: os 8% do mes passado e o dia 20

ESTE CANAL TEM O CASO MAIS LIMPO DO 598 DA FROTA, e vale dizer com numero: os
DOIS shorts de mais de mil views (1.132 e 1.111) deram as DUAS piores
travessias, 0,3% e 3,2%. Os tres melhores longos vieram de shorts de 1.111, 22
e 21 views. Alcance de short nao compra longo — aqui com uma razao de 50x entre
os shorts e nenhuma vantagem no longo.

O QUE DEU CERTO: os tres primeiros sao (a) uma ESCOLHA no documento do proprio
espectador e (b) dois PRAZOS DATADOS, com a data no titulo. Este canal tem 65
inscritos, o maior da frota, e publico profissional de SST e qualidade — gente
que age por prazo.
O QUE NAO DEU: o 007 e metodo sobre documento proprio e fez 3 views de longo.
Mas o short dele tem 1.132 views, entao a leitura consistente e a do 598, nao
"metodo nao funciona". E o 002 repete o assunto do 001 e ficou abaixo dele.
O QUE VOU MUDAR: juntar as DUAS coisas que funcionaram em um unico pacote —
prazo datado E conta no documento do espectador — em vez de escolher uma.

VEREDITO `suspenso` -> piso de 8 min e o melhor material no short. Sobre o
piso, aprendizado 602. Saiu em ~560 s.

TRAVA DO 549 com o segundo teste do 605: 323 linhas de vida inteira, 7 quedas,
pior delta -4 — isso e jitter, nao a troca posicional. E na ultima coleta
nenhum dos 14 ids esta abaixo do proprio passado (pior desvio +2). A tabela
SERVE neste canal; li ao vivo so para incluir o pacote 009, de hoje.

EIXO NOVO. Os nove anteriores falam de INSS do autonomo, FAP, NR-10, desconto a
vista, ISO 9001, riscos psicossociais (duas vezes), precificacao por hora e
FGTS. NENHUM fala de CAT. Este fala, e pelo detalhe que decide tudo: QUAL data
inicia o prazo.

FECHADO NO TEXTO DA LEI, com a ressalva de fonte declarada no AVISO:
  * planalto.gov.br, Lei 8.213/1991 consolidada (310.324 chars de texto legivel)
    — art. 22 caput (comunicar ate o primeiro dia util seguinte ao da
    ocorrencia, e em caso de morte de imediato, sob pena de multa); art. 22 § 1
    (copia fiel para o acidentado ou dependentes E para o sindicato da
    categoria); § 2 (na falta de comunicacao da empresa podem formaliza-la o
    acidentado, dependentes, entidade sindical, o medico que o assistiu ou
    qualquer autoridade publica, NAO prevalecendo nestes casos o prazo); § 3 (a
    comunicacao do § 2 nao exime a empresa); § 4 (sindicatos podem acompanhar a
    cobranca das multas); § 5 (a multa nao se aplica na hipotese do caput do
    art. 21-A); art. 21-A (a pericia do INSS caracteriza a natureza acidentaria
    quando constatar nexo tecnico epidemiologico, pela relacao entre a
    atividade da empresa e a entidade morbida elencada na CID); art. 23 (dia do
    acidente, em doenca profissional ou do trabalho: data do inicio da
    incapacidade laborativa, OU o dia da segregacao compulsoria, OU o dia do
    diagnostico, valendo o que ocorrer PRIMEIRO); art. 19 e paragrafos (o que e
    acidente do trabalho; a empresa responde pelas medidas de protecao;
    constitui contravencao penal deixar de cumprir as normas; e dever da
    empresa informar os riscos).
  * gov.br/inss (37.406 chars) — confirma a VIA: o servico "Registrar
    Comunicacao de Acidente de Trabalho - CAT" existe na pagina de Empresas do
    orgao que recebe a comunicacao.

A RESSALVA, e ela esta no AVISO tambem: o prazo em si tem UMA fonte, o texto
consolidado da lei no planalto. Para prazo LEGAL isso e a fonte definitiva —
nao e medicao, e a norma. O gov.br/inss corrobora quem recebe e por onde, nao o
prazo. E o numero que decide continua sendo do espectador: as tres datas
candidatas do registro de ocorrencia dele.

ALAVANCA B: resposta na cena 11. Residuo da `pt-BR-ThalitaMultilingualNeural`
no ensaio.py; a conta corrigida esta no rodape e vai ser conferida no
legendas.srt (aprendizado 604, que ja tem tres pontos: 0,1 s, 4,6 s e 8,2 s, os
tres errando para MAIS).

HASHTAGS com a do canal, como 002 a 008 — sete pacotes. O 009, meu, de hoje de
manha, saiu sem ela. QUINTO canal seguido em que o pacote anterior e meu e esta
fora do padrao do proprio canal: aprendizado 601.

TITULO PROPRIO DO SHORT: tem (aprendizado 548). So o 008 e o 009 tinham.
"""

import json

CENAS = []

BROLL = {
    5055607: ("https://videos.pexels.com/video-files/5055607/5055607-hd_1280_720_25fps.mp4",
              "ArtHouse Studio",
              "https://www.pexels.com/video/three-workers-in-industrial-suit-5055607/"),
    8060739: ("https://videos.pexels.com/video-files/8060739/8060739-hd_1280_720_50fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/close-up-footage-of-a-person-filling-up-the-form-8060739/"),
    8375617: ("https://videos.pexels.com/video-files/8375617/8375617-hd_1366_720_25fps.mp4",
              "Tima Miroshnichenko",
              "https://www.pexels.com/video/a-doctor-writing-on-a-paper-8375617/"),
    4378032: ("https://videos.pexels.com/video-files/4378032/4378032-hd_1280_720_25fps.mp4",
              "Ketut Subiyanto",
              "https://www.pexels.com/video/calendar-hanged-on-a-wall-4378032/"),
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


# ================= OS PRIMEIROS DUZENTOS SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
B("Um dia útil", "e o prazo já começou",
  "O prazo para comunicar um acidente do trabalho é de um dia útil. Curto, "
  "conhecido, e quase sempre contado a partir da data errada.",
  "three workers in industrial safety suits", 5055607,
  cap="Um dia útil, contado a partir de qual data")
T("Onde está escrito", "artigo vinte e dois",
  "Está no artigo vinte e dois da lei que organiza os benefícios da Previdência "
  "Social, com a redação dada por uma lei complementar de dois mil e quinze.")
T("O texto", "até o primeiro dia útil",
  "A empresa, ou o empregador doméstico, deverá comunicar o acidente do "
  "trabalho à Previdência Social até o primeiro dia útil seguinte ao da "
  "ocorrência.")
T("E tem pena", "multa que cresce",
  "E não é recomendação: o próprio artigo prevê multa, variável entre o limite "
  "mínimo e o limite máximo do salário de contribuição, aumentada nas "
  "reincidências.")
T("O problema real", "não é o tamanho do prazo",
  "Mas o problema que aparece na prática não é o tamanho do prazo. É saber "
  "qual é a data da ocorrência quando não houve um acidente com hora marcada.")
T("Porque doença", "não tem hora",
  "Num acidente típico a data é óbvia. Numa doença ocupacional não existe um "
  "instante único, e aí a lei precisou escolher uma data — e escolheu.")
T("O que vem agora", "três datas",
  "Este vídeo não cita nenhuma alíquota, nenhum valor de multa e nenhum piso. "
  "Cita três datas candidatas, e a regra que diz qual delas vale.")
T("Dia útil é dia útil", "não é vinte e quatro horas",
  "E antes de contar, uma precisão do texto: ele diz primeiro dia útil "
  "seguinte, não vinte e quatro horas. Fim de semana e feriado não são dia "
  "útil, e isso muda a conta num acidente de sábado.")

# -------------------------------------------------------------------- cap 2
B("A resposta", "está no artigo vinte e três",
  "A resposta está no artigo vinte e três, e ela vale para doença profissional "
  "ou do trabalho. Ele define o que se considera como dia do acidente.",
  "close up of a person filling out a form", 8060739,
  cap="Qual data começa o prazo: as três candidatas")
T("Primeira candidata", "início da incapacidade",
  "A primeira candidata é a data do início da incapacidade laborativa para o "
  "exercício da atividade habitual. Não é o dia do desconforto; é o da "
  "incapacidade.")
T("Segunda candidata", "segregação compulsória",
  "A segunda é o dia da segregação compulsória, que é o afastamento imposto, "
  "por exemplo por determinação sanitária.")
T("Terceira candidata", "o diagnóstico",
  "A terceira é o dia em que for realizado o diagnóstico. Aqui conta o "
  "documento: a data que o laudo ou o atestado carrega.")
T("E a regra", "o que ocorrer primeiro",
  "E a regra que decide está na última frase do artigo: vale para este efeito "
  "o que ocorrer primeiro. A mais antiga das três, não a mais conveniente.")
T("A conta", "três datas e um dia útil",
  "Então a conta é esta: escreva as três datas, circule a mais antiga, e conte "
  "um dia útil a partir dela. Pronto, você tem o seu prazo.")
T("Nenhum número meu", "tudo do seu registro",
  "Nenhuma dessas datas vem de mim. Todas estão no registro de ocorrência, no "
  "atestado e no prontuário que a sua empresa já tem.")
T("E no acidente comum", "a data é a do fato",
  "Vale dizer o limite disto: o artigo vinte e três fala de doença "
  "profissional ou do trabalho. No acidente típico a data da ocorrência é a do "
  "próprio fato, e não há três candidatas para escolher.")

# ======================== DEPOIS DA RESPOSTA ================================

# -------------------------------------------------------------------- cap 3
T("Uma exceção", "e ela é dura",
  "O mesmo artigo vinte e dois traz uma exceção ao prazo de um dia útil, e ela "
  "é a mais dura do dispositivo.",
  cap="Em caso de morte não é um dia útil")
T("Em caso de morte", "de imediato",
  "Em caso de morte, a comunicação é de imediato, e à autoridade competente. "
  "Não há dia útil seguinte, não há expediente, não há segunda-feira.")
T("Por que isso importa", "o plantão",
  "Isso importa porque muda o desenho do procedimento interno: quem está de "
  "plantão num sábado precisa saber que esse caso não espera o escritório abrir.")
T("Duas vias diferentes", "não é a mesma coisa",
  "E note que são duas obrigações com destinos diferentes no texto: a "
  "comunicação à Previdência Social, e a comunicação imediata à autoridade "
  "competente.")
T("Confundir custa", "e custa caro",
  "Quem trata os dois casos com o mesmo fluxo tende a cumprir o prazo do mais "
  "frequente e perder o do mais grave, que é exatamente o inverso do que a lei "
  "pede.")
T("Um teste simples", "no seu procedimento",
  "Abra o seu procedimento de resposta a acidentes e procure a palavra morte. "
  "Se ela não aparecer com um fluxo próprio, o procedimento está incompleto.")
T("E o prazo do resto", "continua",
  "Para todos os outros casos o prazo segue sendo até o primeiro dia útil "
  "seguinte ao da ocorrência, com a data definida como vimos no capítulo dois.")
T("Quem é a autoridade competente", "o texto não diz",
  "E repare que o texto diz autoridade competente sem nomeá-la. Quem define "
  "isso é a norma de cada situação, então esse é um ponto para o seu "
  "procedimento resolver antes do acidente, não durante.")

# -------------------------------------------------------------------- cap 4
T("E se a empresa não comunicar", "parágrafo segundo",
  "Agora a parte que muita gente não sabe que existe, e está no parágrafo "
  "segundo do artigo vinte e dois.",
  cap="Quem mais pode emitir, e para eles o prazo não vale")
T("Cinco podem formalizar", "na falta da empresa",
  "Na falta de comunicação por parte da empresa, podem formalizá-la o próprio "
  "acidentado, seus dependentes, a entidade sindical competente, o médico que "
  "o assistiu, ou qualquer autoridade pública.")
T("E aqui está o detalhe", "o prazo não prevalece",
  "E o texto termina com uma frase que muda o jogo: não prevalecendo nestes "
  "casos o prazo previsto neste artigo.")
T("O que isso significa", "não há decadência para eles",
  "Ou seja, quando quem comunica é o trabalhador, o sindicato ou o médico, "
  "aquele prazo de um dia útil simplesmente não se aplica a eles.")
T("Mas atenção", "parágrafo terceiro",
  "O parágrafo terceiro fecha a porta do outro lado: essa comunicação não exime "
  "a empresa da responsabilidade pela falta de cumprimento do artigo.")
T("Traduzindo", "não é substituto",
  "Traduzindo: o trabalhador emitir a comunicação não conserta o "
  "descumprimento da empresa. Resolve o registro, não a infração.")
T("E tem fiscalização", "parágrafo quarto",
  "E o parágrafo quarto diz que sindicatos e entidades representativas de "
  "classe poderão acompanhar a cobrança das multas pela Previdência Social.")
T("Por que isso é útil", "para os dois lados",
  "Esse parágrafo é útil para os dois lados: para o trabalhador, porque abre "
  "um caminho quando a empresa não emite; e para a empresa, porque mostra que "
  "o registro aparecer por outra via não encerra o assunto dela.")

# -------------------------------------------------------------------- cap 5
T("A cópia fiel", "parágrafo primeiro",
  "Falta uma obrigação que quase nunca é cumprida, e ela está no parágrafo "
  "primeiro do mesmo artigo.",
  cap="A cópia fiel que vai para você e para o sindicato")
T("Quem recebe", "duas partes",
  "Da comunicação receberão cópia fiel o acidentado, ou seus dependentes, e "
  "também o sindicato a que corresponda a sua categoria.")
T("Cópia fiel", "não é resumo",
  "A expressão do texto é cópia fiel. Não é aviso, não é resumo e não é "
  "confirmação de protocolo: é a mesma comunicação, inteira.")
T("Por que o sindicato", "e por que importa",
  "O sindicato entra no texto junto com o trabalhador, e isso se conecta com o "
  "parágrafo quarto: ele pode acompanhar a cobrança das multas.")
T("O teste do arquivo", "procure a segunda via",
  "Então um teste rápido no seu arquivo: para a última comunicação emitida, "
  "existe registro de entrega da cópia ao trabalhador e ao sindicato?")
T("Se não existe", "é obrigação aberta",
  "Se não existe, não é uma formalidade esquecida: é uma obrigação do próprio "
  "artigo que ficou aberta, e ela é fácil de fechar.")
T("E para o trabalhador", "é o seu direito",
  "E se você é o trabalhador: essa cópia é sua por previsão do parágrafo "
  "primeiro. Pedi-la não é favor.")
T("Está no mesmo artigo", "do prazo",
  "Vale notar onde essa obrigação mora: no mesmo artigo vinte e dois que fixa "
  "o prazo. Não é norma de outro lugar, é o parágrafo imediatamente seguinte "
  "ao caput que todo mundo cita.")
T("Um detalhe de arquivo", "comprove a entrega",
  "E como é obrigação de entregar, o que fecha o item no seu arquivo não é a "
  "cópia guardada: é o comprovante de que ela foi entregue a quem o parágrafo "
  "nomeia.")

# -------------------------------------------------------------------- cap 6
B("Sem comunicação", "e ainda assim acidentário",
  "Existe um caminho em que a natureza acidentária é reconhecida mesmo sem "
  "comunicação nenhuma, e ele está no artigo vinte e um A.",
  "a doctor writing on a medical report", 8375617,
  cap="Quando o INSS caracteriza sem comunicação")
T("Quem caracteriza", "a perícia do INSS",
  "A perícia médica do Instituto Nacional do Seguro Social considerará "
  "caracterizada a natureza acidentária da incapacidade em uma hipótese "
  "específica.")
T("A hipótese", "nexo técnico epidemiológico",
  "Quando constatar a ocorrência de nexo técnico epidemiológico entre o "
  "trabalho e o agravo. É o nome técnico de uma ligação estatística reconhecida.")
T("De onde sai o nexo", "duas listas cruzadas",
  "Esse nexo decorre da relação entre a atividade da empresa e a entidade "
  "mórbida motivadora da incapacidade, elencada na Classificação Internacional "
  "de Doenças.")
T("Pode ser afastado", "parágrafo primeiro",
  "E o parágrafo primeiro prevê o contrário: a perícia deixará de aplicar o "
  "artigo quando demonstrada a inexistência do nexo. Não é automático nos dois "
  "sentidos.")
T("A ligação com a multa", "parágrafo quinto",
  "Aqui entra o parágrafo quinto do artigo vinte e dois: a multa não se aplica "
  "na hipótese do caput do artigo vinte e um A.")
T("O que isso ensina", "duas coisas distintas",
  "Ou seja, reconhecimento do caráter acidentário e multa por não comunicar são "
  "coisas distintas, e uma pode existir sem a outra.")
T("De quando é esse artigo", "não é antigo",
  "Esse dispositivo não vem da redação original da lei: ele foi incluído "
  "depois, por uma lei posterior, justamente para dar à perícia esse caminho.")
T("E foi ajustado", "quando mudou o doméstico",
  "Mais tarde a redação foi ajustada de novo, e foi nessa revisão que o "
  "empregador doméstico passou a aparecer no texto, ao lado da empresa.")

# -------------------------------------------------------------------- cap 7
T("E o que é acidente", "artigo dezenove",
  "Para fechar, vale ler o que a lei chama de acidente do trabalho, porque a "
  "definição é mais larga do que a imagem que vem à cabeça.",
  cap="O que a lei chama de acidente do trabalho")
T("A definição", "duas consequências",
  "É o que ocorre pelo exercício do trabalho a serviço de empresa ou de "
  "empregador doméstico, provocando lesão corporal ou perturbação funcional.")
T("E o efeito exigido", "três possibilidades",
  "Com um efeito: que cause a morte, ou a perda, ou a redução — permanente ou "
  "temporária — da capacidade para o trabalho.")
T("Perturbação funcional", "não precisa de sangue",
  "Note perturbação funcional e redução temporária. Não é preciso lesão "
  "visível nem incapacidade definitiva para caber na definição.")
T("Parágrafo primeiro", "a responsabilidade",
  "O parágrafo primeiro diz que a empresa é responsável pela adoção e uso das "
  "medidas coletivas e individuais de proteção e segurança da saúde do "
  "trabalhador.")
T("Parágrafo segundo", "contravenção penal",
  "O parágrafo segundo vai além da multa: constitui contravenção penal, "
  "punível com multa, deixar a empresa de cumprir as normas de segurança e "
  "higiene do trabalho.")
T("Parágrafo terceiro", "informar os riscos",
  "E o terceiro cria um dever de informação: é dever da empresa prestar "
  "informações pormenorizadas sobre os riscos da operação a executar.")
T("E não é só empregado", "o texto é mais largo",
  "O artigo também alcança o exercício do trabalho dos segurados de uma "
  "categoria específica que ele cita por remissão, além do trabalho a serviço "
  "de empresa ou de empregador doméstico.")

# -------------------------------------------------------------------- cap 8
B("Hoje", "quinze minutos",
  "Fechando com a coisa a fazer, que leva quinze minutos e usa só papel que "
  "você já tem.",
  "a calendar hanging on a wall", 4378032,
  cap="Hoje: três datas e um dia útil")
T("Primeiro", "pegue o último caso",
  "Pegue o último caso de doença ocupacional registrado na sua empresa, ou o "
  "seu próprio, se você é o trabalhador.")
T("Segundo", "escreva as três datas",
  "Escreva as três datas: início da incapacidade, segregação compulsória se "
  "houve, e a data do diagnóstico no laudo.")
T("Terceiro", "circule a mais antiga",
  "Circule a mais antiga das três. Essa é a data da ocorrência para efeito "
  "deste prazo, porque a lei manda valer o que ocorrer primeiro.")
T("Quarto", "conte um dia útil",
  "Conte um dia útil a partir dela e compare com a data em que a comunicação "
  "foi efetivamente emitida. Agora você sabe se o prazo foi cumprido.")
T("E o que não concluir", "a ressalva",
  "O que não concluir: isto não é consultoria jurídica, não avalia o seu caso "
  "e não decide se houve nexo. Caso concreto é trabalho de profissional.")
T("E se o prazo passou", "não é motivo para não emitir",
  "E se a conta mostrar que o prazo passou, isso não é motivo para não emitir. "
  "O parágrafo terceiro trata do descumprimento como coisa própria, separada "
  "de existir ou não o registro.")
C("Nos comentários", "só um número",
  "Nos comentários escreva só quantos dias de diferença deu na sua conta. Sem "
  "nome de empresa, sem CID e sem dado de ninguém.")

# ================================== SHORT ====================================

SHORT = [
    {"layout": "titulo", "kicker": "Um dia útil", "sub": "mas a partir de quando",
     "nar": "O prazo para comunicar acidente do trabalho é de um dia útil. O "
            "problema é a data em que ele começa.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Em doença ocupacional", "sub": "são três datas",
     "nar": "Em doença do trabalho a lei dá três datas: início da "
            "incapacidade, segregação compulsória e diagnóstico.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A regra", "sub": "o que ocorrer primeiro",
     "nar": "E manda valer o que ocorrer primeiro. A mais antiga das três, não "
            "a mais conveniente.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A conta", "sub": "do seu próprio registro",
     "nar": "Escreva as três, circule a mais antiga e conte um dia útil. Todas "
            "saem do seu registro.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "E em caso de morte", "sub": "não é um dia útil",
     "nar": "Em caso de morte não é um dia útil: é de imediato. Essa e outras "
            "quatro regras estão no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Três datas", "l2": "um dia útil"}

COPY = """# CAT: o prazo é de um dia útil, mas a data que o inicia são três — e vale a mais antiga

## TITULO
CAT em Doença Ocupacional: São Três Datas Candidatas e Vale a Mais Antiga — Conte o Seu Prazo

## TITULO SHORT
CAT: três datas, qual inicia o prazo?

## DESCRICAO
O prazo para comunicar um acidente do trabalho à Previdência Social é de um dia útil. Isso quase todo mundo sabe. O que derruba a contagem na prática não é o tamanho do prazo: é saber qual é a data da ocorrência quando não houve um acidente com hora marcada, e sim uma doença ocupacional.

O artigo 23 da Lei 8.213/1991 resolve isso e é pouco lido. Ele diz que se considera como dia do acidente, no caso de doença profissional ou do trabalho, a data do início da incapacidade laborativa para o exercício da atividade habitual, ou o dia da segregação compulsória, ou o dia em que for realizado o diagnóstico — e encerra com a frase que decide tudo: valendo para este efeito o que ocorrer primeiro. São três datas candidatas e vale a mais antiga, não a mais conveniente. A conta deste vídeo é essa: escreva as três, circule a mais antiga, conte um dia útil a partir dela e compare com a data em que a comunicação foi emitida. As três datas saem do registro de ocorrência, do atestado e do laudo que você já tem.

Depois da resposta o vídeo percorre cinco regras do artigo 22 e dos artigos vizinhos. O caput: a empresa ou o empregador doméstico deverão comunicar até o primeiro dia útil seguinte ao da ocorrência e, em caso de morte, de imediato à autoridade competente, sob pena de multa variável entre o limite mínimo e o máximo do salário de contribuição, aumentada nas reincidências. O § 2º: na falta de comunicação da empresa podem formalizá-la o próprio acidentado, seus dependentes, a entidade sindical competente, o médico que o assistiu ou qualquer autoridade pública — não prevalecendo nestes casos o prazo do artigo; e o § 3º avisa que isso não exime a empresa. O § 1º: da comunicação receberão cópia fiel o acidentado ou seus dependentes e também o sindicato da categoria. O artigo 21-A: a perícia médica do INSS considerará caracterizada a natureza acidentária quando constatar nexo técnico epidemiológico entre o trabalho e o agravo, pela relação entre a atividade da empresa e a entidade mórbida elencada na CID — e o § 5º do artigo 22 diz que a multa não se aplica nessa hipótese. E o artigo 19, que define acidente do trabalho de forma mais larga do que a imagem comum: basta perturbação funcional que cause redução temporária da capacidade para o trabalho.

Uma ressalva que pesa mais que a conta: este vídeo é informativo, não é consultoria jurídica, não avalia caso concreto e não decide se há nexo entre a doença e o trabalho. Ele não cita alíquota, valor de multa nem piso de nada. Se houver divergência sobre a data, sobre o nexo ou sobre a emissão, isso é trabalho de profissional habilitado e, no caso do trabalhador, também do sindicato da categoria.

CAPITULOS
{CAPITULOS}

Nos comentários escreva só quantos dias de diferença deu na sua conta. Sem nome de empresa, sem CID e sem dado de pessoa nenhuma.

## DISCLOSURE
A narração e os gráficos deste vídeo são gerados por computador. O texto é original e o conteúdo é informativo, não constitui consultoria jurídica, médica ou de segurança do trabalho.

## HASHTAGS
#CAT #SegurancaDoTrabalho #LabTreinamento

## TAGS
CAT, comunicacao de acidente de trabalho, prazo da CAT, primeiro dia util, artigo 22 Lei 8213, artigo 23 Lei 8213, doenca ocupacional, doenca profissional, inicio da incapacidade, nexo tecnico epidemiologico, artigo 21-A, copia fiel sindicato, acidente do trabalho, seguranca do trabalho, SST

## COMENTARIO FIXADO
A conta inteira: em doença ocupacional o artigo 23 da Lei 8.213/1991 dá três datas candidatas para o dia do acidente — início da incapacidade laborativa, segregação compulsória e data do diagnóstico — e manda valer o que ocorrer primeiro. Escreva as três, circule a mais antiga, conte um dia útil a partir dela e compare com a data em que a comunicação foi emitida. E atenção ao caso de morte: ali não é um dia útil, é de imediato.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhuma aliquota, nenhum valor de multa, nenhum piso, nenhum teto e nenhuma estatistica de acidente. Os unicos numeros citados sao PRAZOS e ARTIGOS: o prazo de um dia util e o "de imediato" em caso de morte (art. 22, caput), os artigos 19, 21-A, 22 e 23 da Lei 8.213/1991, e os paragrafos 1 a 5 do art. 22. Prazo legal e numero de artigo nao sao medicoes.

O NUMERO QUE DECIDE E DO ESPECTADOR: as tres datas candidatas do art. 23 saem do registro de ocorrencia, do atestado e do laudo que ele ja tem, e a operacao e escolher a mais antiga e somar um dia util.

A RESSALVA DE FONTE, declarada: o prazo tem UMA fonte, o texto consolidado da Lei 8.213/1991 no planalto.gov.br. Para prazo LEGAL essa e a fonte definitiva — nao e medicao que precise de cruzamento, e a norma, publicada pela Presidencia da Republica. O gov.br/inss corrobora a VIA (o servico "Registrar Comunicacao de Acidente de Trabalho - CAT" existe na area de Empresas do orgao que recebe a comunicacao), nao o prazo. Nao inventei uma segunda fonte para o prazo e nao finjo que o gov.br/inss e uma.

O QUE FOI DESCARTADO, e por que: (1) o valor da multa, porque o texto a define por referencia ao limite minimo e maximo do salario de contribuicao, que muda por ano e que eu nao fecharia em duas fontes nesta rodada — o video diz que existe multa e como ela e definida, sem numero; (2) o prazo de entrega de eSocial e de qualquer evento correlato, porque muda por ato normativo e nao e o assunto; (3) qualquer afirmacao sobre SE uma doenca especifica tem nexo com uma atividade especifica, porque isso depende da CID, do regulamento e da pericia — o video explica o MECANISMO do art. 21-A e diz explicitamente que o parag. 1 permite afasta-lo; (4) orientacao de como contestar indeferimento, que e trabalho de profissional habilitado.

## FONTES
Lei nº 8.213, de 24 de julho de 1991 (Planos de Benefícios da Previdência Social), texto consolidado — Presidência da República, planalto.gov.br: art. 19 e §§ 1º a 3º; art. 21-A e § 1º; art. 22 caput e §§ 1º a 5º (redação do caput dada pela Lei Complementar nº 150, de 2015; § 5º incluído pela Lei nº 11.430, de 2006); art. 23.
Instituto Nacional do Seguro Social — gov.br/inss, área de Empresas: serviço "Registrar Comunicação de Acidente de Trabalho - CAT" (confirma o órgão que recebe a comunicação e a via de registro).
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/labtreinamento-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-010",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
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
    grava(SPEC, "fabrica/specs/labtreinamento-010.json")
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
        if "circule a mais antiga, e conte um dia útil" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
