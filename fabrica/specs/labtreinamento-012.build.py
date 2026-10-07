"""labtreinamento-012 — o custo por pessoa que o orcamento de turma nao mostra.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA, com uma LEITURA
NOVA do canal que apareceu nesta rodada.

NUMERO DE PARTIDA, lido AO VIVO em 07/10 06:12 pelo `videos.list`
(part=statistics,status) nos 22 ids. Vigilancia do teto 7 na mesma chamada:
101/101 vivos nos tres canais, zero fora de public, zero nao processado.

    pacote  assunto                          dias  short  longo  travessia
    008     Desconto a vista e juro: /90        3,2    215     15      7,0%
    006     INSS do autonomo: 11% ou 20%       40,7  1.111     35      3,2%
    005     FAP 2027: consulta abre em 30/09   42,6     22     32       145%
    004     NR-10: o prazo termina em junho    47,3     21     18        86%
    003     [EXCEL] ISO 9001: transicao        48,0     28     14        50%
    002     [EXCEL] Riscos Psicossociais NR-1  50,1     26      9        35%
    001     NR-1: a fiscalizacao ja comecou    55,8      4     11       275%
    007     Por hora ou por projeto?           36,3  1.133      3      0,26%

O QUE DEU CERTO, e e a LEITURA NOVA: o short do 008 tem 215 views em 3,2 dias e
e o terceiro maior do canal. Ate ontem o retrato dizia "short grande = travessia
ruim", porque os dois gigantes (1.111 e 1.133) deram 3,2% e 0,26%. O 008 mostra
que o problema NAO e tamanho: ele e medio-grande E carrega promessa de CONTA no
titulo do short ("Desconto a vista e juro. Quanto?"), e cruzou 7,0% — vinte e
sete vezes o 007, que tem short do mesmo porte dos gigantes.

O QUE NAO DEU, e e a parte que eu quase leria errado: a travessia em PORCENTO
favorece quem tem short minusculo. O 001 "ganha" com 275% e tem onze views de
longo. Pela regra do aprendizado 598, ordeno por VIEWS DE LONGO: 35, 32, 18, 15,
14, 11, 9, 3. Os dois melhores sao 006 e 005, e os dois sao UM NUMERO QUE JA FOI
APLICADO AO ESPECTADOR e que ele pode conferir no proprio papel — a aliquota da
guia e o multiplicador do FAP. O 007, o pior longo do canal, pede DECISAO ("por
hora ou por projeto?"), nao conferencia.

O QUE VOU MUDAR: mantenho a promessa de conta no titulo do short, que e o que o
008 acabou de confirmar, e troco "decisao sua" por "numero que o fornecedor ja
aplicou em voce e nao imprimiu".

TENTEI A FAMILIA QUE MEDE MELHOR E NAO DEU, e vai escrito: "numero que a NORMA
ja aplicou em voce" (aliquota, adicional, faixa progressiva) exige o texto da
norma, e o `planalto.gov.br` continua inacessivel. QUINTA tentativa, tres horas
depois da primeira, mesmo erro no `pg_net`: "Failure when receiving data from
the peer". Nao e intermitencia. Entao o "ja aplicado em voce" aqui vem do
FORNECEDOR, nao do Estado — e ai nao ha norma a citar.

PESQUISA DE TENDENCIA (obrigatoria). Feita nesta rodada para o canal da fila
anterior e NAO refeita para BR: o feed BR/26 foi lido as 03:08 desta madrugada
(humor, Disney, squishy, crianca, cachorro; zero trabalho) e a forma grafada
dali — "COMO SABER SE ALGO QUE TE AFETA E VOCE NAO VE" — ja foi usada no 011.
Para este pacote a forma vem do PROPRIO CANAL, que e evidencia mais forte que o
feed: o short do 008, medido ha trinta minutos. Declaro a troca em vez de
inventar uma grafagem nova.

EIXO, e por que ele e novo. Os onze pacotes falam de NR-1, ISO 9001, NR-10, FAP,
INSS do autonomo, hora contra projeto, desconto como juro, FGTS, CAT e controle
de validade. NENHUM trata de COMPRA de treinamento. O 011 e a lista de quem
vence quando; este e o custo por cabeca da turma que voce vai comprar para essa
lista — a continuacao natural, sem repetir o enquadramento. Similaridade medida
contra os dez titulos do canal no corpus: 0,49, teto 0,65.

IDENTIDADE: faixa do canal conferida em TRES pacotes (008, 009, 010), nao no
anterior — paleta `{ink #22333B, c1 #A4243B, c2 #D8973C, bg #F4F1EA}` e trilha
`Inspired`. Nas duas rodadas passadas eu descobri que EU mesmo havia trocado a
paleta do kolejny e do epomeno (aprendizado 617); aqui ela bate.

VEREDITO DO CANAL: `suspenso` — piso de oito minutos e o melhor material NO
SHORT. Pela colisao do aprendizado 602, SETE capitulos, nao oito.

PISO DE CARACTERES, calculado ANTES da primeira cena (aprendizado 616):
`piso_de_caracteres('pt-BR-ThalitaMultilingualNeural', n_cenas=56)` da 119
caracteres por narracao para o total fechar 480 s, e o custo fixo das 56 cenas e
99 s. Escrevi para ~127, mirando ~505 s.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO AFIRMACAO SOBRE O MUNDO. Nao ha fonte a citar porque nao ha afirmacao a
# sustentar: o video nao diz quanto custa treinamento, nao cita norma, nao cita
# periodicidade, nao cita preco de mercado e nao nomeia fornecedor.
#
# O QUE O VIDEO AFIRMA E ARITMETICA:
#   * custo por pessoa = preco da turma dividido pelo numero de pessoas que voce
#     VAI MANDAR — nunca pelo limite do "ate";
#   * quando faltam pessoas para o limite, o custo por pessoa SOBE, e sobe na
#     proporcao exata da divisao;
#   * comparar duas cotacoes e comparar esses dois custos por pessoa, para o
#     MESMO numero de pessoas — o seu.
#
# AS ENTRADAS SAO TODAS DO ESPECTADOR: o preco da turma e o limite estao na
# cotacao dele, e o numero de pessoas sai da lista dele. Nenhum numero meu
# entra no resultado.
#
# O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O
# ABRE: tres mil reais para turma de ate vinte, dois mil para turma de ate doze,
# e doze pessoas para mandar. Nao e preco de fornecedor nenhum.
#
# O QUE FOI DESCARTADO:
#   (1) quanto custa treinamento de verdade no mercado brasileiro — nao tenho
#       fonte e nao cito de memoria;
#   (2) qualquer periodicidade, carga horaria ou numero de NR, pelo mesmo motivo
#       do 011: o planalto nao abre (quinta tentativa nesta rodada);
#   (3) se contratar turma fechada ou mandar para turma aberta — depende de
#       logistica e de preco que eu nao tenho;
#   (4) qualquer juizo sobre fornecedor, qualidade de instrutor ou validade de
#       certificado.
#
# E O QUE A CONTA NAO DECIDE esta no capitulo sete: o custo por pessoa nao e o
# unico criterio. Turma fechada na sua empresa economiza horas de deslocamento
# que esta conta nao ve, e o video diz isso em vez de fingir que o menor numero
# ganha sempre.
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


# Links gravados pela busca via `pg_net`. NENHUM repete pacote anterior deste
# canal: os quatorze ja usados (1793371, 4284181, 4378032, 5055607, 5100043,
# 6413836, 6538597, 7535087, 7816376, 8060739, 8293501, 8375617, 8479064,
# 9057678) foram lidos de TODAS as specs do canal antes da escolha.
# Todos com quinze segundos ou mais: a cena fica em ~8,7 s e o preparo pede
# ~11,7 s.
BROLL = {
    8196812: ("https://videos.pexels.com/video-files/8196812/8196812-hd_1280_720_25fps.mp4",
              "Yan Krukau",
              "https://www.pexels.com/video/students-having-a-lecture-in-their-classroom-8196812/"),
    8716885: ("https://videos.pexels.com/video-files/8716885/8716885-hd_1280_720_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/woman-sitting-while-writing-in-notebook-8716885/"),
    7648407: ("https://videos.pexels.com/video-files/7648407/7648407-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/business-people-in-a-meeting-7648407/"),
    7100892: ("https://videos.pexels.com/video-files/7100892/7100892-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/video-of-a-man-teaching-in-front-7100892/"),
    3981779: ("https://videos.pexels.com/video-files/3981779/3981779-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/a-man-practicing-the-right-way-of-doing-cpr-3981779/"),
    32252415: ("https://videos.pexels.com/video-files/32252415/13755052_1366_720_24fps.mp4",
               "SHOX ART",
               "https://www.pexels.com/video/hands-on-cpr-training-with-mannequin-outdoors-32252415/"),
    8198505: ("https://videos.pexels.com/video-files/8198505/8198505-hd_1280_720_25fps.mp4",
              "Yan Krukau",
              "https://www.pexels.com/video/students-raising-hands-in-class-8198505/"),
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
# A resposta — a divisao inteira, com as duas entradas nomeadas — abre o
# capitulo 2, que a estimativa poe perto dos 72 s. Vou medir a FRASE no
# legendas.srt depois do render, nao a abertura de capitulo (aprendizado 537).

# ---------------------------- 1 -------------------------------------- ~72 s
B("Turma de até vinte", "e você tem doze",
  "O orçamento de treinamento quase sempre vem com preço por turma e um limite: turma de até tantas pessoas. E você raramente tem esse número exato.",
  "students having a lecture in a classroom", 8196812, cap="Turma de até vinte")
T("O preço é da turma", "não da pessoa",
  "O preço é da turma. Você paga o mesmo valor mandando vinte pessoas ou mandando doze, e isso está escrito ali, só não está somado.")
T("O número que falta", "ninguém o imprime",
  "O número que decide a compra é o custo por pessoa, e ele não está impresso em lugar nenhum do orçamento. Você precisa fazer a divisão.")
T("E ele muda", "conforme a sua lista",
  "E ele não é um número fixo do fornecedor: muda conforme a SUA lista. Dois clientes com a mesma cotação pagam valores diferentes por cabeça.")
T("O erro mais comum", "dividir pelo limite",
  "O erro mais comum é dividir pelo limite do orçamento. Isso dá o melhor caso possível, que só acontece se você lotar a turma.")
T("E o limite é teto", "não é contagem",
  "O limite é um teto, não uma contagem. A palavra até está ali justamente porque o fornecedor não sabe quantas pessoas você vai mandar.")
T("O que este vídeo faz", "uma divisão e uma comparação",
  "A solução é uma divisão seguida de uma comparação. Os números já estão na sua cotação e na sua lista de vencimentos, nenhum vem de fora.")
T("Sem preço de mercado", "e vou explicar por quê",
  "Não vou citar quanto custa treinamento. Esse número eu não tenho em fonte, e o vídeo funciona inteiro sem ele.")

# ---------------------------- 2 -------------------------------------- ~72 s
B("A divisão", "e é só uma",
  "A conta é uma divisão: preço da turma dividido pelo número de pessoas que você VAI mandar. Não pelo limite, e não pelo tamanho da equipe.",
  "woman writing in a notebook", 8716885, cap="A divisão")
T("Repare na entrada", "vai mandar, não poderia mandar",
  "Repare na entrada: quantas pessoas vão mandar de verdade. Quem está de licença, quem já tem certificado válido e quem saiu não entram.")
T("O resultado", "é o único número comparável",
  "O resultado é o custo por pessoa daquela cotação, para a sua situação. É o único número que se compara entre dois orçamentos diferentes.")
T("A comparação", "mesmo número de pessoas",
  "E a comparação tem uma regra: use o MESMO número de pessoas nas duas contas. É o seu número, e não muda de fornecedor para fornecedor.")
T("Por que isso importa", "o limite varia",
  "Isso importa porque o limite varia entre cotações. Comparar custo por pessoa calculado em limites diferentes é comparar duas situações que não existem.")
T("O que pode inverter", "e inverte com frequência",
  "E aqui está o que mais surpreende: a cotação que parece mais cara por pessoa no limite pode ser a mais barata para o seu número real.")
T("Dois números por cotação", "o preço e o limite",
  "Então de cada orçamento você tira dois números: o preço da turma e o limite de pessoas. O terceiro número é seu, e é o mesmo para todos.")
T("Agora onde ler", "e são quatro campos",
  "Com a conta na mão, falta saber onde cada número está no papel. São quatro campos, e dois deles costumam estar na letra miúda.")

# ---------------------------- 3 -------------------------------------- ~72 s
B("Quatro campos", "no orçamento ou na proposta",
  "O primeiro campo é o preço da turma. Procure o valor que não está multiplicado por nada: é o preço do evento, não o de uma vaga.",
  "business people in a meeting", 7648407, cap="Quatro campos para ler")
T("Cuidado aqui", "preço por vaga é outra coisa",
  "Se a cotação dá preço por vaga, você está em outro modelo e a divisão não é necessária. O custo por pessoa já está impresso ali.")
T("O segundo campo", "o limite de pessoas",
  "O segundo campo é o limite: turma de até tantos. Anote o número, não a faixa, e confira se ele vale por turma ou por dia de curso.")
T("O terceiro campo", "o que está incluído",
  "O terceiro é o que está incluído: material, certificado, deslocamento do instrutor, reposição de quem faltar. Só o que estiver escrito conta.")
T("Por que isso é um campo", "muda a comparação",
  "Isso é um campo e não um detalhe, porque duas cotações com preços parecidos podem incluir coisas diferentes. Aí a divisão compara maçã com laranja.")
T("O quarto campo", "a validade do orçamento",
  "O quarto é a validade da proposta. Ele não entra na divisão, mas decide se você ainda pode comparar as duas ou se uma já venceu.")
T("Se faltar um campo", "pergunte, não presuma",
  "Se algum desses campos não estiver no papel, pergunte antes de comparar. Presumir o que está incluído é o jeito mais rápido de errar a conta.")
T("E anote", "para a próxima compra",
  "Anote os quatro num lugar só. Na próxima compra você compara a cotação nova com a antiga em menos de um minuto.")

# ---------------------------- 4 -------------------------------------- ~72 s
B("Por que o até engana", "e engana sempre na mesma direção",
  "A palavra até cria uma expectativa de preço que só se realiza na turma cheia. E turma cheia é o caso menos comum em equipe pequena.",
  "a man teaching in front of a class", 7100892, cap="Por que o até engana")
T("A conta do fornecedor", "é legítima",
  "Do lado do fornecedor isso é legítimo: ele reserva instrutor, sala e material para o limite, e o custo dele não cai se você mandar menos.")
T("Mas o custo é seu", "e ele sobe",
  "Só que o custo por pessoa é seu, e ele sobe exatamente na proporção da divisão. Menos gente no mesmo preço significa mais por cabeça.")
T("Quanto sobe", "a conta é direta",
  "E sobe rápido: mandar metade da turma dobra o custo por pessoa. Mandar dois terços aumenta em cerca de cinquenta por cento.")
T("Por isso o teto importa", "mais que o preço",
  "Por isso o limite importa tanto quanto o preço. Uma turma de limite menor e preço menor pode ser melhor para quem tem pouca gente.")
T("E o oposto também", "se você tem muita gente",
  "E o contrário vale: se você tem gente suficiente para lotar, o limite alto passa a trabalhar a seu favor e o preço por cabeça desaba.")
T("O que não fazer", "inventar gente",
  "O que não fazer é inventar gente para lotar a turma. Treinar quem não precisa custa o mesmo que não treinar quem precisa, e some do controle.")
T("Vamos aos números", "e são inventados",
  "Fica mais claro com números. Eles são inventados por mim, e digo isso na cena que abre o exemplo.")

# ---------------------------- 5 -------------------------------------- ~72 s
B("Exemplo", "números inventados, e digo",
  "Os números deste exemplo são inventados para a conta ficar visível. Não são preço de fornecedor nenhum e não foram medidos em lugar nenhum.",
  "a man practicing CPR training", 3981779, cap="Exemplo com números redondos")
T("Cotação A", "turma grande, preço maior",
  "Cotação A: três mil reais, turma de até vinte pessoas. Dividindo pelo limite dá cento e cinquenta reais por pessoa.")
T("Cotação B", "turma menor, preço menor",
  "Cotação B: dois mil reais, turma de até doze pessoas. Dividindo pelo limite dá cerca de cento e sessenta e sete por pessoa.")
T("No limite", "a A parece melhor",
  "Olhando só assim, a A parece melhor: cento e cinquenta contra cento e sessenta e sete. É essa comparação que quase todo mundo faz.")
T("Mas quantas pessoas", "você tem de verdade",
  "Agora entre com o seu número. Digamos que a sua lista tem doze pessoas para mandar, nem uma mais.")
T("Refazendo a A", "com o seu número",
  "A cotação A fica em três mil divididos por doze, ou seja duzentos e cinquenta reais por pessoa. O limite de vinte não foi usado.")
T("Refazendo a B", "com o mesmo número",
  "A cotação B fica em dois mil divididos por doze, ou seja cento e sessenta e sete por pessoa. O limite dela coincide com a sua lista.")
T("A inversão", "e o tamanho dela",
  "A ordem inverteu. A diferença é de oitenta e três reais por pessoa, que na sua lista inteira dá mil reais no mesmo treinamento.")

# ---------------------------- 6 -------------------------------------- ~72 s
B("O que entra", "só o que está escrito",
  "Agora a parte que arruína comparação boa: o que está incluído. A regra é uma só, e vale nos dois lados: entra o que está escrito.",
  "hands-on CPR training with a mannequin", 32252415, cap="O que entra na comparação")
T("Material e certificado", "nem sempre vêm juntos",
  "Material didático e emissão de certificado nem sempre estão no preço. Quando um orçamento inclui e o outro não, a divisão sozinha engana.")
T("Como resolver", "some antes de dividir",
  "Resolve-se somando antes de dividir: ponha no preço da turma tudo o que você teria de pagar à parte, e só então divida pelo seu número.")
T("Deslocamento", "quando a turma é fechada",
  "Deslocamento e hospedagem do instrutor aparecem em turma fechada na sua empresa. Se estiverem por fora, entram na soma da mesma forma.")
T("Reposição", "a linha que quase ninguém lê",
  "Reposição de quem faltou é a linha que quase ninguém lê, e é a que mais custa depois. Confira se há reposição e em que prazo.")
T("O que não entra", "o seu tempo",
  "O que não entra na conta é o seu tempo e as horas de trabalho que a equipe deixa de produzir. Existem, mas não se comparam com nada no papel.")
T("Por que deixar fora", "para a conta continuar conferível",
  "Ficam fora para a conta continuar conferível: duas pessoas com os mesmos orçamentos têm de chegar no mesmo número por pessoa.")
T("Resumo da regra", "soma, depois divide",
  "A regra em cinco palavras: some o que está escrito, depois divida pelo seu número. Nessa ordem, e só com o que está no papel.")

# ---------------------------- 7 -------------------------------------- ~72 s
B("O que a conta não decide", "e é importante",
  "Esta conta não diz qual fornecedor contratar. Diz quanto cada um custa por pessoa para a sua lista, e isso é um critério entre vários.",
  "students raising hands in class", 8198505, cap="O que a conta não decide")
T("Turma fechada", "economiza o que a conta não vê",
  "Turma fechada na sua empresa pode economizar horas de deslocamento da equipe inteira, e essas horas não aparecem em nenhuma das divisões.")
T("Qualidade", "não está no preço",
  "E não digo nada sobre qualidade de instrutor nem sobre validade de certificado: isso depende de coisas que não estão no orçamento.")
T("Primeiro passo", "junte as cotações",
  "Quatro passos, e cabem nesta semana. Primeiro: junte as cotações que você tem em aberto, mesmo as vencidas, para ter base de comparação.")
T("Segundo passo", "conte a sua lista",
  "Segundo: conte quantas pessoas você VAI mandar, usando a lista de vencimentos. Esse é o número que entra em todas as divisões.")
T("Terceiro passo", "some o que está escrito",
  "Terceiro: para cada cotação, some ao preço da turma tudo o que não está incluído e que você teria de pagar à parte.")
T("Quarto passo", "divida e ordene",
  "Quarto: divida cada soma pelo seu número e ordene. O menor custo por pessoa é o ponto de partida da conversa, não o fim dela.")
C("Conte quantas cotações", "e se a ordem inverteu",
  "Se você fizer a conta, escreva nos comentários quantas cotações comparou e se a ordem inverteu. Sem nomes de fornecedor e sem valores.")


# =============================== O SHORT =====================================
# `suspenso` manda o MELHOR MATERIAL para o short — e o short do 008, medido
# nesta rodada com 215 views em 3,2 dias, confirmou que promessa de CONTA no
# titulo do short nao impede distribuicao. Entao este titula a conta.
SHORT = [
    {"layout": "titulo", "kicker": "Turma de até vinte", "sub": "e você tem doze",
     "nar": "O orçamento diz turma de até vinte. Você tem doze pessoas para "
            "mandar, e paga o mesmo preço.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "O preço é da turma", "sub": "não da pessoa",
     "nar": "O custo por pessoa não está impresso em lugar nenhum do "
            "orçamento. Você faz a divisão.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "O erro", "sub": "dividir pelo limite",
     "nar": "Dividir pelo limite dá o melhor caso, que só acontece com a turma "
            "cheia. Divida pelo seu número.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "E a ordem inverte", "sub": "com frequência",
     "nar": "A cotação que parece mais cara por pessoa no limite pode ser a "
            "mais barata para a sua lista.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Mesmo número", "sub": "nas duas contas",
     "nar": "Use o mesmo número de pessoas nas duas divisões: o seu. O exemplo "
            "inteiro está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Por turma", "l2": "ou por pessoa?"}

COPY = """# labtreinamento-012

## TITULO
Treinamento Cotado por Turma: o Custo por Pessoa Que o Orçamento Não Mostra

## TITULO SHORT
Turma de até 20? Divida pelo seu número

## DESCRICAO
O orçamento de treinamento quase sempre vem com preço por turma e um limite: turma de até tantas pessoas. E você raramente tem esse número exato. O preço é da turma — você paga o mesmo valor mandando vinte pessoas ou mandando doze, e isso está escrito ali, só não está somado. O número que decide a compra é o custo por pessoa, e ele não está impresso em lugar nenhum do orçamento: você precisa fazer a divisão. E ele não é um número fixo do fornecedor, muda conforme a SUA lista — dois clientes com a mesma cotação pagam valores diferentes por cabeça.

O erro mais comum é dividir pelo limite do orçamento, porque isso dá o melhor caso possível, que só acontece se você lotar a turma. O limite é um teto, não uma contagem: a palavra "até" está ali justamente porque o fornecedor não sabe quantas pessoas você vai mandar. A conta certa é uma divisão só — preço da turma dividido pelo número de pessoas que você VAI mandar, descontando quem está de licença, quem já tem certificado válido e quem saiu. E a comparação entre duas cotações tem uma regra: use o MESMO número de pessoas nas duas contas, porque esse número é seu e não muda de fornecedor para fornecedor.

O vídeo mostra onde ler cada campo (preço da turma, limite de pessoas, o que está incluído e a validade da proposta), por que a palavra "até" engana sempre na mesma direção, e um exemplo com números redondos — declarados inventados na própria cena que o abre — em que a ordem das duas cotações INVERTE quando você entra com o seu número real. Um capítulo inteiro vai para o que está incluído: material, certificado, deslocamento do instrutor e reposição de quem faltou, com a regra em cinco palavras — some o que está escrito, depois divida pelo seu número.

E o último capítulo é o que a conta NÃO decide. O menor custo por pessoa é o ponto de partida da conversa, não o fim dela: turma fechada na sua empresa pode economizar horas de deslocamento da equipe inteira, e essas horas não aparecem em nenhuma das divisões. O vídeo não diz quanto custa treinamento no mercado, não cita norma nem periodicidade, não nomeia fornecedor e não opina sobre qualidade de instrutor nem validade de certificado — nada disso está no orçamento, e nada disso é necessário para a conta.

Conteúdo informativo, não é consultoria de segurança do trabalho nem recomendação de compra.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
A conta está no primeiro minuto e meio, então não é preciso ver o vídeo inteiro para pegá-la: preço da turma dividido pelo número de pessoas que você VAI mandar. Nunca pelo limite do "até", que é teto e não contagem. Para comparar duas cotações, use o MESMO número de pessoas nas duas divisões — o seu — e antes de dividir some ao preço da turma tudo o que não está incluído e que você pagaria à parte (material, certificado, deslocamento do instrutor, reposição de quem faltou). Duas armadilhas: mandar metade da turma dobra o custo por pessoa, e a cotação que parece mais cara por pessoa no limite pode ser a mais barata para a sua lista real. Se fizer a conta, escreva nos comentários quantas cotações comparou e se a ordem inverteu — sem nome de fornecedor e sem valores.

## HASHTAGS
#Treinamento #CustoPorPessoa #LabTreinamento

## TAGS
custo por pessoa, orcamento de treinamento, turma fechada, turma aberta, comparar cotacoes, treinamento corporativo, compra de treinamento, limite de turma, material didatico incluido, reposicao de faltas, seguranca do trabalho, SST, gestao de equipe, planejamento de treinamento, lab treinamento

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
Yan Krukau; Pavel Danilyuk; RDNE Stock project; Gustavo Fring; SHOX ART.

## AVISO SOBRE OS NUMEROS
ZERO AFIRMACAO SOBRE O MUNDO, e por isso nao ha fonte a citar: o video nao diz
quanto custa treinamento, nao cita norma, nao cita periodicidade, nao cita preco
de mercado e nao nomeia fornecedor.

O QUE O VIDEO AFIRMA E ARITMETICA, e so ela:
  * custo por pessoa = preco da turma dividido pelo numero de pessoas que voce
    VAI MANDAR — nunca pelo limite do "ate";
  * faltando gente para o limite, o custo por pessoa sobe na proporcao exata da
    divisao: metade da turma dobra o valor por cabeca;
  * comparar duas cotacoes e comparar esses dois custos por pessoa para o MESMO
    numero de pessoas, o seu;
  * o que nao esta incluido soma ao preco da turma ANTES da divisao.

AS ENTRADAS SAO TODAS DO ESPECTADOR: preco da turma e limite saem da cotacao
dele, e o numero de pessoas sai da lista dele. Nenhum numero meu entra no
resultado.

O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O ABRE:
tres mil reais para turma de ate vinte, dois mil para turma de ate doze, doze
pessoas na lista. Nao e preco de fornecedor nenhum e nao foi medido em lugar
nenhum.

O QUE FOI DESCARTADO, e vai escrito:
  (1) quanto custa treinamento no mercado brasileiro — sem fonte, sem citacao;
  (2) qualquer periodicidade, carga horaria ou numero de NR, pelo mesmo motivo
      do labtreinamento-011: o `planalto.gov.br` nao abre. QUINTA tentativa
      nesta rodada, tres horas depois da primeira, mesmo erro pelo `pg_net`
      ("Failure when receiving data from the peer") — nao e intermitencia;
  (3) se contratar turma fechada ou mandar para turma aberta, que depende de
      logistica e de precos que eu nao tenho;
  (4) qualquer juizo sobre fornecedor, instrutor ou certificado.

E O QUE A CONTA NAO DECIDE esta no capitulo sete: o menor custo por pessoa e o
ponto de partida da conversa, nao o fim. Turma fechada economiza horas de
deslocamento da equipe que esta conta nao ve, e o video diz isso em vez de
fingir que o menor numero ganha sempre.

## FONTES
NENHUMA FONTE NORMATIVA OU DE MERCADO E CITADA, e isso e deliberado. As unicas
"fontes" sao os documentos do proprio espectador: as cotacoes que ele tem em
maos e a lista de vencimentos da equipe dele (que e o assunto do
labtreinamento-011).
B-roll: Pexels, licenca Pexels, creditos por clipe em broll_creditos.json.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-012",
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
    from ensaio import (duracao_estimada, duracao_estimada_short, duracao_cena,
                        piso_de_caracteres)
    grava(SPEC, "fabrica/specs/labtreinamento-012.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    piso = piso_de_caracteres(SPEC["voz"], n_cenas=len(CENAS), cenas_por_cap=8)
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"piso por cena: {piso['min_por_cena']} (manda o {piso['manda']}) | "
          f"media real: {sum(len(c.get('nar','')) for c in CENAS)/len(CENAS):.0f}")
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
        if "pelo número de pessoas que você VAI mandar" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
