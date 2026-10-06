"""labtreinamento-009 — FGTS: os oito por cento, conferidos contra a propria folha.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal e com a ULTIMA leitura de `metricas`
(aprendizado 592 — nunca mais `max(views)`):

    pacote  short -> longo   titulo
    005        20 ->  31     FAP 2027: Consulta Abre em 30 de Setembro...
    006     1.111 ->  35     INSS do Autonomo: 11% ou 20%? ...
    004        21 ->  18     NR-10 Atualizada: o Prazo Termina em Junho de 2027...
    003        28 ->  14     [EXCEL] ISO 9001:2026 ...
    001         4 ->  11     [EXCEL] Planilha de Riscos Psicossociais NR-1 ...
    002        26 ->   9     [EXCEL] Planilha de Riscos Psicossociais NR-1 ...
    007     1.132 ->   3     Por Hora ou por Projeto? ...
    008         0 ->   0     Desconto para Pagar a Vista ... (publicado 04/10)

O QUE DEU CERTO: o 005. Um short de VINTE views entregou TRINTA E UMA views de
longo — o unico pacote do canal em que o longo passou o short. O titulo dele e
declarativo, nomeia uma coisa buscavel (FAP) e carrega numeros: exatamente a
forma que o aprendizado 589 mediu na frota inteira.

O QUE NAO DEU: o 007. MIL CENTO E TRINTA E DUAS views de short e TRES de longo
— o maior short do canal e o pior cruzamento dele. O titulo e pergunta pura
("Por Hora ou por Projeto?"), sem entidade nomeada e sem numero, que e o traco
do terco de BAIXO no 589. E o canal tem outra leitura no mesmo sentido: dos
oito pacotes, os quatro que nomeiam uma obrigacao com data (NR-1, ISO, NR-10,
FAP) somam 52 views de longo; os dois que entregam conselho generico de negocio
somam 3.

O QUE VOU MUDAR: titulo declarativo com a entidade nomeada e o numero na
frente, e pauta de volta ao eixo que mediu melhor — uma obrigacao com data que
a pessoa confere sozinha. O 007 nao foi um acidente: foi o canal saindo do que
ele e.

EIXO, e por que ele e novo. Os oito pacotes falam de NR-1 (001, 002), ISO 9001
(003), NR-10 (004), FAP (005), INSS do autonomo (006) e de precificacao e
desconto (007, 008). NENHUM fala do deposito mensal que a empresa faz no nome
do trabalhador. Este fala: existe uma data, existe uma base, existe um
percentual, e os tres cabem numa conferencia de dois minutos.

VEREDITO DO CANAL: `suspenso` (v_maquina_licoes, 7 shorts e 7 longos medidos,
2.463 views). Pela rotina isso manda PISO de 8 minutos e o melhor material no
SHORT. O longo fica perto do piso — alavanca B — e o short entrega a conta
inteira, nao so a manchete.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ENTRAM NO VIDEO, conferidos em DUAS fontes institucionais que batem — o texto
# consolidado da Lei 8.036/1990 no planalto.gov.br e o PDF da mesma lei no
# caixa.gov.br:
#
#   * oito por cento da remuneracao paga ou devida no mes anterior, por
#     trabalhador — artigo 15.
#   * deposito ate o dia vinte de cada mes — mesmo artigo 15.
#   * a remuneracao da base inclui as parcelas dos artigos 457 e 458 da CLT —
#     mesmo artigo 15.
#
# DESCARTADO, e por que: os percentuais dos REGIMES DIFERENTES nao entram. O
# aprendiz e o empregado domestico tem aliquotas proprias, e eu nao as fechei
# em duas fontes oficiais DENTRO desta rodada. O video diz que esses regimes
# existem e sao diferentes, e trata do empregado CLT comum — que e quem a
# conferencia atende. Tambem NAO entram as cifras de multa e juros do deposito
# em atraso, pela mesma razao: o video diz que atraso tem correcao, juros e
# multa, sem dizer quanto.
#
# TAMBEM FORA, de proposito: nao digo o que fazer se a conta nao bater alem de
# procurar o canal oficial, nao oriento sobre acao trabalhista, nao calculo
# saque nem rescisao, e nao afirmo que toda diferenca e irregularidade — o
# video lista as razoes legitimas de diferenca antes de qualquer outra coisa.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: a remuneracao da folha do mes passado e
# o valor do deposito no extrato dele. Os dois estao na mao dele, e nenhum dos
# dois e meu.
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


# O LINK FICA NA SPEC, nao na busca em tempo de render. Resolvido pela busca por
# `pg_net` DENTRO do banco, que e onde a chave do Pexels mora: o
# `prebusca_broll.py` rodado da sandbox para em "chave do Pexels: AUSENTE"
# porque o passo do workflow nao exporta os secrets, e do meu runner o proxy
# devolve 403 para api.pexels.com. Com o link gravado o pacote fica
# REPRODUZIVEL: sem ele, dois renders da mesma spec pegam clipes diferentes.
BROLL = {
    6538597: ("https://videos.pexels.com/video-files/6538597/6538597-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-woman-getting-a-file-6538597/"),
    7535087: ("https://videos.pexels.com/video-files/7535087/7535087-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/person-using-a-calculator-7535087/"),
    6413836: ("https://videos.pexels.com/video-files/6413836/6413836-hd_1280_720_24fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/a-woman-writing-on-the-notebook-6413836/"),
}

# CADA CLIPE ESCOLHIDO CONTRA O QUE A NARRACAO DIZ. O primeiro candidato da
# cena de abertura era "person writing TAX FRAUD on a notepad" — e a narracao
# ali e sobre uma conferencia de rotina, nao sobre fraude. Aquele clipe
# transformaria uma conta aritmetica numa acusacao ao empregador. Descartado.


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor,
                           "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — o numero do espectador — fecha dentro do capitulo 3. O que vem
# depois protege a conta de falso alarme.

# -------------------------------------------------------------------- cap 1
B("Todo mês tem uma data", "e quase ninguém olha para ela",
  "Todo mês, no seu nome, entra um depósito que não passa pela sua conta "
  "corrente e que você quase nunca confere. Ele tem data certa.",
  "payslip paperwork desk close up", 6538597,
  cap="Todo mês tem uma data")
T("A data", "até o dia vinte",
  "A lei marca o prazo: o depósito do mês tem que estar feito até o dia vinte "
  "do mês seguinte. Não é uma data que a empresa escolhe.")
T("Por que isso importa", "a conferência tem um calendário",
  "Isso importa porque muda o que você compara com o quê. O valor que aparece "
  "hoje no extrato se refere ao mês passado, não a este.")
T("O erro mais comum", "comparar mês com mês errado",
  "E esse é o erro mais comum de quem tenta conferir. A pessoa olha a folha "
  "deste mês e o depósito deste mês, e conclui que falta dinheiro.")
T("A regra simples", "o depósito olha para trás",
  "Guarde a regra assim: o depósito de um mês olha sempre para a remuneração "
  "do mês anterior. Um mês de distância, sempre.")
T("Primeiro passo", "separe a folha do mês passado",
  "Então o primeiro passo não é abrir o extrato. É separar a folha de "
  "pagamento do mês passado, que é a base de tudo o que vem a seguir.")
T("Quem recebe por recibo", "o eixo é outro",
  "Se você não tem folha porque trabalha por recibo, esta conferência não é a sua. Ela vale para quem é registrado pela CLT.")
T("Onde ela está", "no portal da empresa ou no papel",
  "Essa folha está no portal do empregador ou no papel que você recebe. "
  "Qualquer uma das duas serve, desde que seja a do mês certo.")

# -------------------------------------------------------------------- cap 2
T("A base da conta", "não é o salário na mão",
  "Agora a parte que mais gera engano. A base do cálculo não é o salário que "
  "cai na sua conta.",
  cap="A base não é o que cai na conta")
T("O que a lei diz", "remuneração paga ou devida",
  "A lei fala em remuneração paga ou devida no mês anterior. Remuneração é "
  "uma palavra mais larga do que salário líquido.")
T("O que entra", "as parcelas da CLT",
  "Dentro dela entram as parcelas previstas nos artigos quatrocentos e "
  "cinquenta e sete e quatrocentos e cinquenta e oito da CLT.")
T("Em linguagem de folha", "o bruto, antes das descontos",
  "Em linguagem de folha de pagamento, isso quer dizer o bruto. O valor antes "
  "de descontar previdência, imposto e o que mais for descontado.")
T("Então some", "salário mais o que é habitual",
  "Então some o salário base com o que vem todo mês junto dele: horas extras "
  "habituais, adicional noturno, insalubridade, comissões.")
T("Comissão conta", "mesmo variando todo mês",
  "Comissão entra na base mesmo quando varia muito de um mês para o outro. O que muda é o valor, não o fato de ela contar.")
T("Hora extra eventual", "também entra no mês em que houve",
  "Hora extra que aconteceu só naquele mês também entra na base daquele mês. Habitual ou não, se foi paga, compõe a remuneração.")
T("O que não é remuneração", "indenização não entra",
  "O que a folha chama de indenização ou de reembolso não é remuneração. Vale "
  "transporte devolvido e diária de viagem ficam de fora.")
T("Se a folha separa tudo", "melhor para você",
  "Folha que separa cada parcela em uma linha facilita a conferência. Some linha por linha e compare com o total bruto impresso.")
T("Anote esse número", "ele é metade da conta",
  "Anote o bruto do mês passado em algum lugar. Ele é metade da conta, e a "
  "outra metade é um único percentual.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
B("Os oito por cento", "o percentual é um só",
  "O percentual está no artigo quinze da lei e é um só para o empregado "
  "comum: oito por cento.",
  "typing numbers on calculator", 7535087,
  cap="Os oito por cento")
T("A conta", "bruto vezes zero vírgula zero oito",
  "A conta é direta. Pegue o bruto que você anotou e multiplique por zero "
  "vírgula zero oito. Em calculadora, é o bruto vezes oito dividido por cem.")
T("Esse é o seu número", "o que deveria ter sido depositado",
  "O resultado é o seu número: o valor que deveria ter entrado na sua conta "
  "vinculada referente ao mês passado.")
T("Agora compare", "abra o extrato do fundo",
  "Agora abra o extrato do fundo no aplicativo oficial e procure o depósito "
  "lançado para esse mês. Compare com o número que você acabou de achar.")
T("Dois resultados", "bate ou não bate",
  "Só existem dois resultados. Ou os dois valores batem, com centavos de "
  "diferença, ou existe uma distância que tem que ser explicada.")
T("Centavos não são erro", "o arredondamento é normal",
  "Diferença de centavos não é erro. Arredondamento de centavos acontece em "
  "qualquer folha e não significa nada.")
T("Se der diferença grande", "não conclua ainda",
  "Se a distância for de dezenas ou centenas de reais, segure a conclusão. Existem razões comuns para isso, e elas vêm no próximo bloco.")
T("Anote a data da conferência", "ela serve de marco",
  "Anote também a data em que você conferiu. Se precisar voltar ao assunto depois, essa data situa o que já tinha sido lançado e o que ainda não.")
T("Guarde os dois valores", "o seu e o do extrato",
  "Guarde os dois valores lado a lado. O resto do vídeo serve para você saber "
  "se uma diferença maior tem explicação legítima.")

# -------------------------------------------------------------------- cap 4
T("Quando a diferença é normal", "e são vários casos",
  "Antes de concluir qualquer coisa, veja as razões pelas quais a conta deixa "
  "de bater sem que exista nada de errado.",
  cap="Quando a diferença é normal")
T("Primeiro caso", "mês de admissão ou de saída",
  "O primeiro é o mês em que você entrou ou saiu da empresa. A remuneração é "
  "proporcional aos dias, e o depósito acompanha essa proporção.")
T("Segundo caso", "o décimo terceiro tem depósito próprio",
  "O segundo é o décimo terceiro salário. Ele gera depósito próprio, em cima "
  "do valor dele, e não se mistura com o do salário do mês.")
T("Terceiro caso", "afastamento sem remuneração",
  "O terceiro é o afastamento. Em alguns afastamentos não há remuneração no "
  "mês, e sem remuneração não há base para o depósito.")
T("Quarto caso", "a folha foi corrigida depois",
  "O quarto é a folha corrigida depois do fechamento. Se a empresa acertou um "
  "valor no mês seguinte, o depósito também se acerta no mês seguinte.")
T("Quinto caso", "o extrato demora a atualizar",
  "E o quinto é o extrato simplesmente ainda não ter atualizado. O depósito "
  "feito perto do prazo pode demorar alguns dias para aparecer.")
T("Sexto caso", "férias no meio do mês",
  "Há ainda o mês de férias, em que parte da remuneração entra como férias e parte como salário. A base muda de forma e o depósito acompanha.")
T("Como separar os casos", "olhe a folha, não o extrato",
  "Para saber em qual caso você está, a resposta quase sempre está na folha daquele mês, não no extrato. O extrato só mostra o resultado.")
T("Só depois disso", "a diferença vira pergunta",
  "Só depois de descartar esses cinco casos é que uma diferença vira uma "
  "pergunta de verdade para levar a alguém.")

# -------------------------------------------------------------------- cap 5
B("Faça a conta do ano", "doze conferências, não uma",
  "Uma conferência de um mês prova pouco. Doze conferências seguidas provam "
  "muito, e dão quase o mesmo trabalho.",
  "writing in notebook rows table", 6413836,
  cap="Faça a conta do ano")
T("Como fazer", "uma linha por mês",
  "Monte uma linha por mês: bruto da folha, o seu número calculado e o valor "
  "que o extrato mostra. Três colunas, doze linhas.")
T("O que você procura", "um padrão, não um mês",
  "O que interessa não é um mês solto. É se existe um padrão: uma diferença "
  "que se repete sempre no mesmo sentido.")
T("Diferença que se repete", "essa é a que fala",
  "Uma diferença que aparece num mês e some no outro costuma ser calendário. "
  "Uma que se repete todo mês costuma ser base de cálculo.")
T("Onde o padrão aparece", "em geral numa parcela",
  "Quando a base é o problema, o padrão quase sempre está numa parcela: "
  "alguma coisa que está na folha e que não entrou na conta do depósito.")
T("Comece pelos meses fáceis", "os de salário parado",
  "Comece pelos meses em que nada mudou: sem férias, sem décimo terceiro, sem afastamento. Se bate nesses, a sua conta está certa.")
T("Depois os meses estranhos", "um de cada vez",
  "Só então vá aos meses atípicos, um de cada vez. Comparar um mês de férias com um mês comum confunde mais do que esclarece.")
T("Doze linhas num papel", "não precisa de planilha",
  "Isso cabe num papel. Doze linhas, três colunas, e você já enxerga o que nenhuma leitura de mês solto mostra.")
T("E aí você já sabe qual", "porque fez a conta linha a linha",
  "E aí você já consegue apontar qual parcela é, porque refez a conta linha a "
  "linha e não dependeu de ninguém para isso.")

# -------------------------------------------------------------------- cap 6
T("O que este vídeo não diz", "e os limites importam",
  "Agora a parte que costuma ser omitida. Aqui estão as coisas sobre as quais "
  "este vídeo não fala.",
  cap="O que este vídeo não diz")
T("Outros regimes", "aprendiz e doméstico são diferentes",
  "Não trata do aprendiz nem do empregado doméstico. Esses regimes têm "
  "percentuais próprios e a conferência deles é outra.")
T("Por que não falo deles", "não conferi em duas fontes",
  "E não dou os percentuais deles porque não os conferi em duas fontes "
  "oficiais. Número sem duas fontes não entra, nem quando é fácil de achar.")
T("Atraso", "tem correção, juros e multa",
  "Depósito em atraso tem correção, juros e multa previstos na mesma lei. As "
  "cifras eu também não digo, pela mesma razão.")
T("Não é orientação jurídica", "é uma conferência",
  "Nada aqui é orientação jurídica. É uma conferência aritmética que termina "
  "num número seu, e a decisão sobre o que fazer é sua.")
T("Não trato de rescisão", "ali a conta é outra",
  "Também não trato de rescisão. Na saída existem outras parcelas e outra aritmética, e misturar as duas coisas gera erro.")
T("Não falo de saque", "nem de aniversário",
  "Nem falo de saque, de modalidade de saque ou de prazo para sacar. Isso é outro assunto e não muda em nada a conferência do depósito.")
T("Por que insisto no limite", "porque o excesso tira a confiança",
  "Insisto nesses limites porque vídeo que fala de tudo acaba acertando pouco. Aqui são três números e uma comparação.")
T("O que eu fiz", "li a lei e dividi em passos",
  "O que eu fiz foi ler o artigo quinze e separar em passos: a data, a base, "
  "o percentual, e as razões normais de diferença.")

# -------------------------------------------------------------------- cap 7
T("Onde conferir sozinho", "sem depender deste vídeo",
  "Se você quiser checar tudo o que eu disse, as duas fontes estão abertas e "
  "não custam nada.",
  cap="Onde conferir sozinho")
T("A lei", "no portal da legislação federal",
  "O texto consolidado da lei está no portal da legislação federal. Procure a "
  "lei oito mil e trinta e seis e vá direto ao artigo quinze.")
T("A mesma lei, outra fonte", "no banco que opera o fundo",
  "A mesma lei está publicada no site do banco que opera o fundo. Duas fontes "
  "oficiais, o mesmo texto, e foi assim que eu conferi.")
T("O extrato", "no aplicativo oficial",
  "O extrato vem do aplicativo oficial do fundo, com o seu login. Nenhum "
  "outro lugar precisa saber os seus números.")
T("Por que insisto nisso", "porque o número é seu",
  "Insisto porque o número é seu e a conferência também. Vídeo nenhum deve "
  "ser a última palavra sobre o seu dinheiro.")
T("Guarde o link da lei", "ele não muda de endereço",
  "Guarde o endereço do texto da lei em algum lugar seu. Ele não muda, e serve para qualquer conferência futura.")
T("Desconfie de número solto", "sem fonte, não serve",
  "E desconfie de qualquer número sobre o seu dinheiro que apareça sem fonte. Inclusive os que aparecem com confiança.")
T("A conferência é sua", "e leva dois minutos",
  "A conferência inteira leva dois minutos depois que você faz uma vez. O trabalho está em começar, não em repetir.")
T("Inclusive este", "confira e depois confie",
  "Inclusive este. Refaça a conta com a sua folha na mão, e só então decida "
  "se ela faz sentido.")

# -------------------------------------------------------------------- cap 8
T("A conferência em quatro passos", "do começo ao fim",
  "Agora a conferência inteira, em quatro passos, para você fazer depois de "
  "fechar o vídeo.",
  cap="A conferência em quatro passos")
T("Passo um", "a folha do mês passado",
  "Passo um: separe a folha de pagamento do mês passado, porque o depósito "
  "deste mês se refere a ela.")
T("Passo dois", "o bruto, com o que é habitual",
  "Passo dois: pegue o bruto, somando o que vem todo mês junto do salário "
  "base, e deixando de fora o que é indenização.")
T("Passo três", "multiplique por zero vírgula zero oito",
  "Passo três: multiplique esse bruto por zero vírgula zero oito. Esse é o "
  "valor que deveria ter sido depositado.")
T("Passo quatro", "compare com o extrato",
  "Passo quatro: compare com o extrato. Se a diferença passar de centavos, "
  "volte nos cinco casos normais antes de concluir qualquer coisa.")
T("Se bater", "feche o vídeo tranquilo",
  "Se os dois valores baterem, acabou. Você não precisa fazer mais nada, e agora sabe conferir sozinho todo mês.")
T("Se não bater", "volte aos seis casos",
  "Se não baterem, volte aos seis casos normais antes de qualquer outra coisa. A maioria das diferenças morre ali.")
T("E se sobrar dúvida", "leve o número, não a impressão",
  "E se ainda sobrar dúvida, leve o número calculado e a folha, não a impressão de que algo está errado. Número conversa melhor.")
C("Escreva a diferença aqui embaixo", "só a diferença, não o salário",
  "Nos comentários, escreva só a diferença que você encontrou, em reais, e "
  "nunca o seu salário. Quero ver quantos fecham em zero.")


# ================================== SHORT ====================================
# O veredito do canal e `suspenso`, e a rotina manda o MELHOR MATERIAL no
# short. Entao o short entrega a conta COMPLETA — data, base, percentual e
# comparacao — e nao so a manchete. O 007 provou o custo do contrario: mil
# cento e trinta e duas views de short e tres de longo.

SHORT = [
    {"layout": "titulo", "kicker": "FGTS do mês passado",
     "sub": "confira em dois minutos",
     "nar": "Dá para conferir o depósito do mês passado em dois minutos. São "
            "quatro passos.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Um", "sub": "a folha do mês anterior",
     "nar": "Um: pegue a folha do mês anterior. O depósito deste mês se "
            "refere a ela, não a este.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dois", "sub": "o bruto, não o líquido",
     "nar": "Dois: use o bruto, com horas extras e adicionais habituais. Não "
            "o valor que cai na conta.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Três", "sub": "vezes zero vírgula zero oito",
     "nar": "Três: multiplique por zero vírgula zero oito. Esse é o valor "
            "devido.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Quatro", "sub": "compare com o extrato",
     "nar": "Quatro: compare com o extrato do aplicativo oficial. Diferença "
            "de centavos é arredondamento.", "sem_cap": True},
]


THUMB = {"l1": "8% do bruto", "l2": "bate?"}


COPY = """# labtreinamento-009

## TITULO
FGTS: os 8% do Mês Passado e o Dia 20 — Confira o Depósito Contra a Sua Folha

## TITULO SHORT
FGTS: 8% do bruto, e o dia 20

## DESCRICAO
Todo mês entra um depósito no seu nome que não passa pela conta corrente, e
quase ninguém confere. Dá para conferir em dois minutos, com a folha de
pagamento na mão e uma calculadora, e este vídeo separa a conferência em quatro
passos.

O primeiro passo é de calendário, e é onde a maioria erra: o depósito de um mês
se refere à remuneração do mês ANTERIOR. Comparar a folha deste mês com o
depósito deste mês produz uma diferença que não existe.

O segundo passo é a base. A lei fala em remuneração paga ou devida, incluindo as
parcelas dos artigos 457 e 458 da CLT — ou seja, o bruto, com horas extras
habituais, adicional noturno, insalubridade e comissões. O que a folha chama de
indenização ou reembolso fica de fora.

O terceiro passo é o percentual, que está no artigo 15 da Lei 8.036 de 1990 e é
de 8% para o empregado comum. Bruto vezes zero vírgula zero oito.

O quarto passo é a comparação com o extrato do aplicativo oficial. E antes de
concluir que falta alguma coisa, o vídeo lista cinco razões pelas quais a conta
deixa de bater sem que haja irregularidade: mês de admissão ou saída, décimo
terceiro, afastamento sem remuneração, folha corrigida depois e extrato ainda
não atualizado.

Os percentuais do aprendiz e do empregado doméstico não são citados, e as cifras
de multa e juros do depósito em atraso também não — nenhum desses números foi
conferido em duas fontes oficiais nesta edição, e número sem duas fontes não
entra. O vídeo diz que esses regimes e essas penalidades existem, e manda
conferir na fonte.

Nada aqui é orientação jurídica. É uma conferência aritmética que termina num
número seu.

Capítulos:
00:00 Todo mês tem uma data
01:12 A base não é o que cai na conta
02:38 Os oito por cento
03:57 Quando a diferença é normal
05:18 Faça a conta do ano
06:34 O que este vídeo não diz
07:52 Onde conferir sozinho
09:04 A conferência em quatro passos

Escreva nos comentários só a diferença que você encontrou, em reais — nunca o
seu salário.

## DISCLOSURE
A narração e as imagens deste vídeo foram geradas com inteligência artificial.
Os números citados vêm de fontes oficiais, indicadas na descrição.

## HASHTAGS
#FGTS #FolhaDePagamento #DireitosTrabalhistas

## TAGS
fgts, extrato fgts, deposito fgts, lei 8036, artigo 15 fgts, base de calculo fgts, remuneracao bruta, conferir fgts, folha de pagamento, horas extras habituais, decimo terceiro fgts, conta vinculada, direitos trabalhistas, fgts nao depositado, calculo fgts

## COMENTARIO FIXADO
Quatro passos: folha do mês ANTERIOR → bruto (com habituais, sem indenização) →
vezes zero vírgula zero oito → compare com o extrato. Diferença de centavos é
arredondamento. Escreva aqui só a diferença, nunca o salário.

## MUSICA / LICENCA
Trilha: Inspired (biblioteca livre do pacote). B-roll: Pexels, crédito por clipe
em broll_creditos.json.

## AVISO SOBRE OS NUMEROS
Este vídeo cita três números e os três são do artigo 15 da Lei 8.036 de 1990,
conferidos em duas fontes institucionais que batem — o texto consolidado no
planalto.gov.br e o PDF da mesma lei no caixa.gov.br: oito por cento da
remuneração paga ou devida no mês anterior; depósito até o dia vinte de cada
mês; e base incluindo as parcelas dos artigos 457 e 458 da CLT. DESCARTADO: os
percentuais do aprendiz e do empregado doméstico, e as cifras de multa e juros
do depósito em atraso. Todos existem e estão na mesma lei, mas não os fechei em
duas fontes oficiais nesta rodada, então o vídeo afirma que existem e manda
conferir na fonte, sem dizer quanto. TAMBÉM FORA: não oriento sobre ação
trabalhista, não calculo saque nem rescisão, e não afirmo que toda diferença é
irregularidade — as cinco razões legítimas de diferença vêm antes de qualquer
conclusão. O número que decide é do espectador: o bruto da folha dele e o
depósito no extrato dele.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/labtreinamento-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-009",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C", "bg": "#F4F1EA"},
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
    grava(SPEC, "fabrica/specs/labtreinamento-009.json")
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
