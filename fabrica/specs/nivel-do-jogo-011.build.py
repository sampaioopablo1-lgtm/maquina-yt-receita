"""nivel-do-jogo-011 — drift no analogico: o prazo nao e o da caixa.

ALAVANCA ATACADA: A (forma: metodo que a pessoa aplica em si mesma).

NUMERO DE PARTIDA, e a primeira coisa a dizer e que ele e PEQUENO. Lido AO VIVO
na `videos.list` em 06/10/2026 21:15, casado por `item->>'id'`, porque a tabela
`metricas` deste canal NAO serve (ver abaixo):

    pacote  short  longo   titulo
    004      100     21    EA FC 27: Standard, Ultimate ou Plus? A Conta em Reais
    007        4      9    Loja em Reais, Cartao em Dolar ou Gift Card? A Conta
    005       11      8    Steam Mudou Como Seu Jogo e Precificado
    cron      5/8/4   8/7/5 Lei Felca (tres duplicatas do mesmo titulo)
    003      250      4    Preco dos Jogos: Quantas Horas de Trabalho Custa
    009        6      3    Reembolso de Jogo: Sao Dois Prazos, Nao Um
    008       15      2    Se Voce Tivesse Comprado em Vez de Assinar
    010       49      0    Passe de Temporada: Quanto Voce Ja Gastou
    006        6      0    Demissoes nos Games: Square Enix

O QUE NAO DA PARA LER, e eu nao vou inventar: com teto de 21 views de longo, a
diferenca entre 21, 9 e 8 nao se distingue de ruido. Este canal nao adjudica
nada sozinho — inclusive nao adjudica o aprendizado 598: o short MAIOR (003,
250 views) deu a PIOR travessia do canal (1,6%), o que apoia o 598, mas o
segundo maior (004, 100 views) deu a MELHOR (21,0%), o que nao apoia. Com esses
numeros as duas leituras cabem, e dizer que uma delas esta confirmada aqui
seria fabricar sinal.

O QUE DA PARA DIZER: os tres longos no topo (21, 9 e 8) sao os tres pacotes de
CONTA — dois deles tem "A Conta" literalmente no titulo e o terceiro compara
dois precos. Os que ficaram em zero (010, 006) sao panorama e noticia de
industria. E isso e a mesma direcao que o kolejny-poziom mostrou nesta mesma
rodada com numeros dez vezes maiores. Nao e prova deste canal; e consistencia
entre canais.
O QUE VOU MUDAR: manter a forma de conta e trocar o objeto da conta — de preco
para PRAZO. Contar dias e uma conta, e o documento e do espectador.

POR QUE EU LI AO VIVO EM VEZ DE USAR A TABELA. A trava do aprendizado 549
acusou 26 quedas em 320 linhas de vida inteira neste canal, pior delta -250. E,
diferente do kolejny-poziom desta mesma rodada, o retrato de 04/10 TAMBEM esta
contaminado: 7 dos 24 ids estao abaixo do proprio passado, pior -246. Entao nao
servem nem `max(views)` nem a ultima linha. A unica leitura confiavel e a
`videos.list` agora, casada por id. Fica anotado que este canal precisa de uma
recoleta antes de qualquer conclusao estatistica.

VEREDITO `canal frio` -> eixo novo e piso de 8 min por analogia com `suspenso`.
Sobre o piso, ver o aprendizado 602: com oito capitulos de 64,2 s o piso de
480 s e inalcancavel, e o minimo com margem e ~552 s. Saiu em ~553 s.

EIXO NOVO. Os dezesseis anteriores falam de edicoes do EA FC, loja contra
cartao contra gift card (com IOF), preco regional da Steam, Lei Felca e
caixinhas, preco em horas de trabalho, reembolso, inflacao nos games, comprar
contra assinar, passe de temporada e demissoes. NENHUM fala de GARANTIA. Este
fala, e pelo caso mais comum do hardware: o drift do analogico, que aparece
MESES depois da compra — ou seja, o caso de livro do vicio oculto.

FECHADO EM DUAS INSTITUICOES, e a segunda acrescenta fato que a lei nao da:
  * planalto.gov.br — Lei 8.078/1990 compilada. Art. 26, I e II (trinta dias
    para nao duravel, noventa para duravel); art. 26 par. 1 (a contagem comeca
    da ENTREGA EFETIVA); art. 26 par. 2, I (a reclamacao comprovada OBSTA a
    decadencia ate a resposta negativa inequivoca); art. 26 par. 3 (no vicio
    oculto o prazo comeca quando o defeito fica evidenciado); art. 18 par. 1
    (nao sanado em trinta dias, o consumidor escolhe entre substituicao,
    restituicao imediata atualizada e abatimento); art. 18 par. 2 (as partes
    podem convencionar de sete a cento e oitenta dias, e em contrato de adesao
    a clausula exige manifestacao expressa EM SEPARADO); art. 49 (sete dias
    fora do estabelecimento); art. 50 (a garantia contratual e COMPLEMENTAR a
    legal).
  * procon.sp.gov.br — Fundacao Procon-SP, o orgao que APLICA. Cita o art. 26
    literalmente, define vicio aparente contra vicio oculto ("nao evidenciados
    de inicio, so aparecendo apos determinado tempo ou consumo"), confirma que
    no vicio oculto a contagem comeca na constatacao com os MESMOS prazos, e
    acrescenta duas coisas que a lei nao diz: que o direito de reclamar
    INDEPENDE do certificado de garantia, bastando documento que comprove a
    compra, e que em algumas situacoes sera preciso laudo tecnico.

Nenhum numero meu entra. Todos os numeros sao prazos legais, e o numero que
decide e a DATA da nota fiscal do espectador mais o dia em que o defeito
apareceu.

ALAVANCA B: resposta dentro dos primeiros 200 s, na cena 11. Residuo da
`pt-BR-AntonioNeural` e -0,4% com n=214; a conta corrigida esta no rodape e vai
ser conferida no legendas.srt depois do render (aprendizado 604).

TITULO PROPRIO DO SHORT: tem (aprendizado 548).

HASHTAGS em CamelCase com a do canal, como 002, 004, 005, 006, 007, 008 e 009 —
sete dos nove. Quebraram o padrao o 003 e o 010, e o 010 e meu, de hoje de
manha. Terceiro canal seguido em que o pacote anterior e meu e esta errado:
aprendizado 601.
"""

import json

CENAS = []

# Resolvidos por `pg_net` dentro do Postgres (aprendizado 574).
BROLL = {
    5901406: ("https://videos.pexels.com/video-files/5901406/5901406-hd_1366_720_30fps.mp4",
              "ROMAN ODINTSOV",
              "https://www.pexels.com/video/close-up-of-hands-using-video-game-controller-5901406/"),
    6143908: ("https://videos.pexels.com/video-files/6143908/6143908-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/person-touching-a-paper-6143908/"),
    1793371: ("https://videos.pexels.com/video-files/1793371/1793371-hd_1280_720_30fps.mp4",
              "Miguel Á. Padriñán",
              "https://www.pexels.com/video/person-saving-a-date-on-his-planner-1793371/"),
    6755160: ("https://videos.pexels.com/video-files/6755160/6755160-hd_1280_720_25fps.mp4",
              "Tima Miroshnichenko",
              "https://www.pexels.com/video/young-man-repairing-electronic-device-6755160/"),
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
B("Três relógios", "não um",
  "O analógico do seu controle começou a andar sozinho. Existem três prazos "
  "diferentes correndo sobre isso, e o da caixa é o menos importante dos três.",
  "close up of hands using a video game controller", 5901406,
  cap="Três prazos correndo, e o da caixa é o menor")
T("O primeiro", "é o da lei",
  "O primeiro prazo é o da garantia legal. Ele existe por lei, vale para "
  "qualquer produto durável e ninguém precisa te conceder nada.")
T("O segundo", "é do fornecedor",
  "O segundo é o prazo que o fornecedor tem para consertar depois que você "
  "reclama. Ele é curto, e quando estoura a escolha passa a ser sua.")
T("O terceiro", "é o da caixa",
  "O terceiro é a garantia que vem escrita na caixa ou no certificado. Esse é "
  "contratual, e a lei diz que ele é complementar, não substituto.")
T("Por que isso importa", "a ordem se inverte",
  "A maioria olha só para o terceiro. Quando ele vence, a pessoa acha que "
  "acabou. Não acabou, e em alguns casos nem tinha começado.")
T("O caso do drift", "aparece depois",
  "E o drift é o exemplo perfeito disso, porque ele quase nunca aparece na "
  "primeira semana. Aparece meses depois, com o uso.")
T("O que vem agora", "a conta de dias",
  "Então a conta deste vídeo não é de reais. É de dias, e os dois números "
  "saem de papéis que você tem: a nota fiscal e a data em que o defeito surgiu.")

# -------------------------------------------------------------------- cap 2
B("Pegue a nota", "e olhe a data",
  "A resposta começa num documento só seu. Pegue a nota fiscal ou o "
  "comprovante de compra e olhe a data da entrega, não a data do pedido.",
  "person touching a paper document on a table", 6143908,
  cap="Qual prazo é o seu, e como contar")
T("Primeira pergunta", "o defeito é visível?",
  "Agora uma pergunta só, e ela decide tudo: o defeito era visível na entrega, "
  "ou apareceu depois de um tempo de uso?")
T("Se era visível", "conta da entrega",
  "Se era visível na entrega, a contagem começa na entrega efetiva do produto. "
  "É o caso de um controle que já chegou torto ou riscado.")
T("Se apareceu depois", "conta de quando apareceu",
  "Se apareceu depois, isso é vício oculto, e a contagem começa no momento em "
  "que o defeito ficou evidenciado. Não na compra.")
T("A conta", "noventa dias a partir dali",
  "Então a sua conta é esta: produto durável tem noventa dias, e para vício "
  "oculto esses noventa dias correm a partir do dia em que o drift apareceu.")
T("É isso", "e não precisa de mim",
  "Essa é a resposta inteira. Dois dados seus, uma pergunta e uma soma de dias. "
  "Eu não entrei com nenhum número nessa conta.")
T("Anote hoje", "antes de esquecer",
  "E faça uma coisa agora: anote a data em que você notou o problema. Daqui a "
  "dois meses você não vai lembrar, e é essa data que inicia o seu prazo.")

# ======================== DEPOIS DA RESPOSTA ================================

# -------------------------------------------------------------------- cap 3
T("De onde vem", "artigo vinte e seis",
  "Esses prazos não são praxe de loja nem política de fabricante. Estão no "
  "artigo vinte e seis do Código de Defesa do Consumidor.",
  cap="Os noventa dias, e de onde começam")
T("São dois prazos", "e dependem do produto",
  "O artigo traz dois: trinta dias para serviço e produto não durável, e "
  "noventa dias para serviço e produto durável.")
T("Console é durável", "controle também",
  "Console, controle e headset são produtos duráveis. Então o prazo que te "
  "interessa aqui é o de noventa dias, não o de trinta.")
T("O parágrafo primeiro", "entrega efetiva",
  "E o parágrafo primeiro do mesmo artigo diz de onde a contagem parte: da "
  "entrega efetiva do produto. Entrega, não compra, não pagamento.")
T("Por que a diferença", "compra online",
  "Para quem compra na internet essa diferença é real. Você pode ter pagado "
  "numa segunda e recebido dez dias depois, e o prazo é do recebimento.")
T("O Procon confirma", "e cita o artigo",
  "A Fundação Procon de São Paulo, que é quem aplica o código no estado, cita "
  "esse artigo com as mesmas palavras na sua página de dúvidas.")
T("Um detalhe do Procon", "que a lei não diz",
  "E acrescenta um detalhe prático que a lei não traz: o direito de reclamar "
  "não depende do certificado de garantia. Basta comprovar a compra.")

# -------------------------------------------------------------------- cap 4
B("O vício oculto", "o seu caso",
  "Agora o parágrafo que muda tudo para quem tem drift, e é o parágrafo "
  "terceiro do mesmo artigo vinte e seis.",
  "person writing a date on a planner", 1793371,
  cap="Vício oculto: o relógio começa depois")
T("O que ele diz", "fica evidenciado",
  "Tratando-se de vício oculto, o prazo começa no momento em que ficar "
  "evidenciado o defeito. É a lei escolhendo a data do aparecimento.")
T("A definição", "pelo Procon",
  "O Procon define vício oculto como aquele não evidenciado de início, que só "
  "aparece após determinado tempo ou consumo do produto.")
T("Isso é drift", "quase por definição",
  "Leia essa frase pensando no drift. Um analógico que funcionou por oito "
  "meses e começou a derivar cabe nela quase por definição.")
T("E os prazos", "são os mesmos",
  "E o Procon é explícito: constatado o vício oculto, inicia-se a contagem dos "
  "prazos, e são os mesmos trinta e noventa dias do artigo.")
T("O que não muda", "a ressalva honesta",
  "Uma ressalva que eu preciso dizer: o Procon avisa que em algumas situações "
  "será preciso laudo técnico mostrando que a origem é de fabricação.")
T("Ou seja", "não é automático",
  "Ou seja, vício oculto não é senha automática. É o prazo que começa depois, "
  "e a origem do defeito pode precisar de prova. O que o parágrafo te dá é "
  "tempo para reclamar, não a garantia de que a reclamação será aceita.")

# -------------------------------------------------------------------- cap 5
B("O segundo relógio", "trinta dias",
  "Você reclamou dentro do prazo. Começa aí o segundo relógio, e esse é do "
  "fornecedor: ele tem trinta dias para sanar o vício.",
  "technician repairing an electronic device", 6755160,
  cap="Os trinta dias do fornecedor")
T("Está no artigo dezoito", "parágrafo primeiro",
  "Isso está no artigo dezoito, parágrafo primeiro. E o texto é claro sobre o "
  "que acontece quando esses trinta dias passam sem conserto.")
T("A escolha passa a ser sua", "três opções",
  "Não sendo o vício sanado no prazo, o consumidor pode exigir, à sua escolha, "
  "uma de três coisas. A escolha é sua, não da loja.")
T("Primeira", "outro produto",
  "A primeira é a substituição do produto por outro da mesma espécie, em "
  "perfeitas condições de uso.")
T("Segunda", "dinheiro de volta",
  "A segunda é a restituição imediata da quantia paga, monetariamente "
  "atualizada, sem prejuízo de eventuais perdas e danos.")
T("Terceira", "abatimento",
  "A terceira é o abatimento proporcional do preço, para quem prefere ficar "
  "com o produto como ele está e pagar menos por ele. Faz sentido quando o "
  "defeito incomoda mas não impede de jogar.")
T("Guarde o protocolo", "a data conta",
  "Por isso guarde o número do atendimento e a data em que entregou o produto. "
  "Os trinta dias contam dali, e quem precisa provar a data é você.")

# -------------------------------------------------------------------- cap 6
T("Esse prazo pode mudar", "e muita gente não sabe",
  "Os trinta dias não são imutáveis, e essa é a parte que quase ninguém sabe. "
  "O próprio artigo dezoito permite mudar o prazo.",
  cap="De sete a cento e oitenta dias")
T("O parágrafo segundo", "a faixa",
  "O parágrafo segundo diz que as partes podem convencionar a redução ou a "
  "ampliação do prazo, não podendo ser inferior a sete nem superior a cento e "
  "oitenta dias.")
T("Ou seja", "pode ser seis vezes maior",
  "Ou seja, aquele prazo de trinta dias pode legalmente virar cento e oitenta. "
  "Seis vezes mais tempo com o produto na assistência.")
T("Mas tem condição", "e ela protege você",
  "Só que o mesmo parágrafo coloca uma condição, e ela existe justamente para "
  "proteger quem assina sem ler.")
T("Em contrato de adesão", "em separado",
  "Nos contratos de adesão, a cláusula de prazo deverá ser convencionada em "
  "separado, por meio de manifestação expressa do consumidor.")
T("O que isso quer dizer", "não vale escondido",
  "Em outras palavras, esse prazo maior não pode estar escondido no meio das "
  "letras miúdas. Ele precisa de um sim seu, destacado.")
T("O que fazer com isso", "procure a cláusula",
  "Então se a assistência te falar de um prazo maior que trinta dias, peça "
  "para ver onde você concordou com isso em separado. Se não acharem, o prazo "
  "que vale é o de trinta dias do artigo.")

# -------------------------------------------------------------------- cap 7
T("Reclamar para o relógio", "literalmente",
  "Falta o movimento mais barato e mais ignorado de toda essa história: "
  "reclamar não é só pedir conserto. Reclamar PARA o relógio.",
  cap="Reclamar obsta a decadência")
T("Parágrafo segundo", "obstam a decadência",
  "O artigo vinte e seis, parágrafo segundo, lista o que obsta a decadência, "
  "ou seja, o que interrompe a contagem contra você.")
T("O inciso primeiro", "a reclamação",
  "O primeiro item é a reclamação comprovadamente formulada pelo consumidor "
  "perante o fornecedor, até a resposta negativa correspondente.")
T("E ela tem forma", "inequívoca",
  "E o texto exige que essa resposta negativa seja transmitida de forma "
  "inequívoca. Silêncio da loja não é resposta negativa.")
T("A consequência prática", "o prazo congela",
  "Na prática: enquanto a loja não te dá um não claro, o prazo não está "
  "correndo contra você. Mas isso só vale se a reclamação for comprovável.")
T("Por isso", "sempre por escrito",
  "Por isso reclame por escrito, por um canal que gere registro, e guarde o "
  "protocolo. Reclamação por telefone sem número de atendimento não prova nada.")
T("É o passo mais barato", "e o mais esquecido",
  "Esse é o passo mais barato da lista inteira e o mais esquecido. Custa cinco "
  "minutos e congela o prazo que está trabalhando contra você.")

# -------------------------------------------------------------------- cap 8
T("O terceiro relógio", "o da caixa",
  "Voltamos ao prazo da caixa, aquele que a maioria acha que é o único. O "
  "código fala dele no artigo cinquenta.",
  cap="A da caixa é complementar, e os sete dias")
T("O que ele diz", "complementar",
  "A garantia contratual é complementar à legal e será conferida mediante "
  "termo escrito. Complementar quer dizer que soma, não que substitui.")
T("A inversão", "que custa dinheiro",
  "Então a leitura certa é o contrário da que se faz. O prazo da caixa se soma "
  "ao da lei, e vencer o da caixa não encerra o da lei.")
T("E se comprou online", "artigo quarenta e nove",
  "Tem ainda um prazo separado, que não é de defeito nenhum: o artigo quarenta "
  "e nove dá sete dias para desistir da compra feita fora da loja física.")
T("Esse é por arrependimento", "não por vício",
  "Esse não exige problema no produto. É arrependimento, e os valores pagos "
  "devem ser devolvidos de imediato, monetariamente atualizados.")
T("Não confunda os dois", "são relógios diferentes",
  "Não confunda esse com os noventa dias. Um é para desistir sem motivo, o "
  "outro é para reclamar de defeito. Perder um não consome o outro.")
C("Nos comentários", "só uma data",
  "Escreva nos comentários só isto: quantos dias de uso o seu controle tinha "
  "quando o drift apareceu. Sem modelo, sem loja, sem valor.")

# ================================== SHORT ====================================

SHORT = [
    {"layout": "titulo", "kicker": "Drift no analógico", "sub": "o prazo não é o da caixa",
     "nar": "Seu controle anda sozinho e a garantia da caixa já venceu. Isso "
            "não encerra o seu prazo.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Produto durável", "sub": "noventa dias",
     "nar": "O código do consumidor dá noventa dias para reclamar de vício em "
            "produto durável, e controle é durável.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "E aqui está o pulo", "sub": "vício oculto",
     "nar": "Para vício oculto, o prazo começa quando o defeito fica "
            "evidenciado. Drift de oito meses é esse caso.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A conta", "sub": "duas datas suas",
     "nar": "Conte noventa dias do dia em que o drift apareceu, não da "
            "compra. Anote essa data hoje.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Tem mais dois prazos", "sub": "e um congela o relógio",
     "nar": "Há outros dois prazos, e um deles congela a contagem a seu "
            "favor. Os três estão no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Drift", "l2": "qual prazo vale"}

COPY = """# Drift no analógico: qual dos três prazos é o seu, e como contar com a sua nota fiscal

## TITULO
Drift no Controle: São Três Prazos, Não Um — e a Garantia da Caixa é o Menos Importante

## TITULO SHORT
Drift: qual dos três prazos é o seu?

## DESCRICAO
O analógico do seu controle começou a andar sozinho e a garantia escrita na caixa já venceu. Muita gente para aí, e para cedo: existem três prazos diferentes correndo sobre o mesmo defeito, e o da caixa é o menos importante dos três.

A conta deste vídeo não é de reais, é de dias, e os dois números saem de papéis que você já tem. Pegue a nota fiscal e responda uma pergunta: o defeito era visível na entrega, ou apareceu depois de um tempo de uso? Se era visível, a contagem começa na entrega efetiva do produto. Se apareceu depois, é vício oculto, e o artigo vinte e seis, parágrafo terceiro, do Código de Defesa do Consumidor manda contar do momento em que o defeito ficou evidenciado. Produto durável tem noventa dias — então para drift que apareceu em oito meses de uso, os noventa dias correm a partir do dia em que ele apareceu, não da compra. Anote essa data hoje, porque é ela que inicia o seu prazo.

Depois da resposta, o vídeo percorre os outros dois relógios. O artigo dezoito, parágrafo primeiro, dá ao fornecedor trinta dias para sanar o vício, e quando esse prazo estoura a escolha passa a ser do consumidor entre três opções: substituição por outro produto da mesma espécie, restituição imediata da quantia paga monetariamente atualizada, ou abatimento proporcional do preço. O parágrafo segundo do mesmo artigo permite que esse prazo seja convencionado entre sete e cento e oitenta dias, mas em contrato de adesão a cláusula tem de ser convencionada em separado, por manifestação expressa do consumidor — não vale escondida nas letras miúdas. E o artigo vinte e seis, parágrafo segundo, traz o movimento mais barato de toda a história: a reclamação comprovadamente formulada obsta a decadência até a resposta negativa, que precisa ser transmitida de forma inequívoca. Reclamar por escrito congela o prazo que está correndo contra você.

Por fim, o artigo cinquenta diz que a garantia contratual é complementar à legal — ela soma, não substitui. E o artigo quarenta e nove dá sete dias para desistir de compra feita fora do estabelecimento comercial, que é um prazo separado, de arrependimento, e não de defeito.

Uma ressalva que pesa mais que a conta: isto não é consultoria jurídica e não resolve o seu caso concreto. A própria Fundação Procon de São Paulo avisa que em algumas situações será preciso laudo técnico detalhando os indícios de que o problema teve origem em vício de fabricação. Vício oculto não é senha automática: é o prazo que começa depois, e a origem do defeito pode precisar de prova. Se houver recusa ou divergência, isso é assunto para o Procon do seu estado ou para um advogado.

CAPITULOS
{CAPITULOS}

Nos comentários escreva só isto: quantos dias de uso o seu controle tinha quando o drift apareceu. Sem modelo, sem loja, sem valor.

## DISCLOSURE
A narração e os gráficos deste vídeo são gerados por computador. O texto é original e o conteúdo é informativo, não constitui consultoria jurídica nem orientação sobre caso concreto.

## HASHTAGS
#GarantiaLegal #Controle #NivelDoJogo

## TAGS
drift no analogico, garantia legal, codigo de defesa do consumidor, vicio oculto, artigo 26 CDC, noventa dias garantia, trinta dias conserto, nota fiscal prazo, produto duravel, reclamar vicio, Procon, garantia contratual complementar, direito de arrependimento, artigo 18 CDC, controle de videogame

## COMENTARIO FIXADO
A conta inteira em duas linhas: pegue a nota fiscal e responda se o defeito era visível na entrega ou apareceu depois. Se apareceu depois, é vício oculto, e os noventa dias de produto durável contam do dia em que o drift apareceu, não da compra — artigo 26, parágrafo 3º, do CDC. Anote hoje a data em que você notou o problema, porque é ela que inicia o seu prazo, e reclame por escrito: reclamação comprovada obsta a decadência até a resposta negativa inequívoca.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu, nenhum preco, nenhum valor de conserto e nenhuma estatistica de defeito. TODOS os numeros que ele cita sao prazos e artigos de lei, e cada um esta na fonte abaixo: noventa dias e trinta dias (art. 26, I e II), entrega efetiva como inicio da contagem (art. 26 par. 1), a reclamacao que obsta a decadencia (art. 26 par. 2, I), o inicio da contagem no vicio oculto (art. 26 par. 3), os trinta dias para sanar e as tres escolhas do consumidor (art. 18 par. 1), a faixa de sete a cento e oitenta dias com manifestacao expressa em separado nos contratos de adesao (art. 18 par. 2), os sete dias de arrependimento fora do estabelecimento (art. 49) e a garantia contratual como complementar a legal (art. 50). O numero que decide e do espectador: a data de entrega na nota fiscal dele e o dia em que o defeito apareceu.

A SUSTENTACAO E DE DUAS INSTITUICOES, e a segunda acrescenta fato que a lei nao traz: o texto e a Lei 8.078/1990 compilada no planalto.gov.br, e quem aplica e a Fundacao Procon de Sao Paulo, que cita o art. 26 com as mesmas palavras, define vicio oculto como aquele "nao evidenciado de inicio, so aparecendo apos determinado tempo ou consumo do produto", confirma que constatado o vicio oculto inicia-se a contagem dos MESMOS prazos, e diz que o direito de reclamar INDEPENDE do certificado de garantia, bastando documento que comprove a compra.

O QUE FOI DESCARTADO, e por que: (1) a afirmacao de que um jogo DIGITAL e produto nao duravel ou duravel — a classificacao e contestada e eu nao vou decidi-la num video; por isso o pacote fala de CONTROLE e CONSOLE, que sao duraveis sem controversia, e nao estende a conclusao ao jogo baixado; (2) qualquer taxa de incidencia de drift por modelo ou fabricante, porque nao existe estatistica oficial disso e numero de fabricante nao e fonte institucional; (3) o prazo de garantia que cada fabricante oferece, porque muda por produto e por pais e o video diz justamente que esse e o menos importante dos tres; (4) a promessa de que vicio oculto garante o conserto — o proprio Procon avisa do laudo tecnico, e isso esta DENTRO do video, nao so aqui; (5) qualquer orientacao sobre como abrir processo, porque isso e trabalho de advogado e nao de roteiro.

ALCANCE DA FONTE, declarado: a Fundacao Procon-SP e orgao estadual de Sao Paulo. A lei que ela cita e FEDERAL e vale no pais inteiro, mas o canal de atendimento varia por estado, e o video diz "o Procon do seu estado" por isso.

## FONTES
Lei nº 8.078, de 11 de setembro de 1990 (Código de Defesa do Consumidor), texto compilado — Presidência da República, planalto.gov.br: art. 18, §§ 1º e 2º; art. 26, I, II, §§ 1º, 2º e 3º; art. 49; art. 50.
Fundação Procon-SP, Dúvidas mais frequentes — procon.sp.gov.br: garantia legal e prazos, definição de vício aparente e vício oculto, início da contagem no vício oculto, independência do certificado de garantia e necessidade eventual de laudo técnico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/nivel-do-jogo-011.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-011",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1B4332", "c1": "#D64570", "c2": "#7FB069",
               "bg": "#EFF6F1"},
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
    grava(SPEC, "fabrica/specs/nivel-do-jogo-011.json")
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
    RESIDUO = 0.996   # pt-BR-AntonioNeural, -0,4% no ensaio.py, n=214
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "a partir do dia em que o drift apareceu" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
