#!/usr/bin/env python3
"""Monta a spec agla-level-006.

PASSO 0A — O QUE O CANAL JA DISSE

Esta e a PRIMEIRA vez que o PASSO 0A roda neste canal com dado de verdade, e
so foi possivel porque a rodada anterior parou para consertar a coleta: ate as
21h de hoje o agla-level tinha SEIS videos publicados e ZERO metricas. Dois
deles estavam no ar havia quatro dias sem uma unica leitura. A causa eram dois
defeitos empilhados no coletor (aprendizados 462 e 463); depois do conserto, a
frota saiu de 19 para 158 videos medidos.

`v_maquina_licoes` continua sem devolver linha para este canal — tres titulos
distintos e amostra pequena demais. Veredito, portanto: `sem dado`, tratado
como canal frio.

Mas o (b) agora existe, e traz uma comparacao limpa. Dois pares publicados no
MESMO dia, 20/08, mesmo canal, mesma voz:

    8th Pay Commission: fitment factor, a verdade dos 400%   777,1 s   5,00 v/d
    ITR 2026: o prazo passou — quanta multa e quanto juro     840,8 s   0,00 v/d

  DEU CERTO: confrontar um NUMERO PROMETIDO publicamente com a conta real. O
  vencedor pega os "400% de aumento" que circulam sobre a oitava comissao e vai
  conferir. Ele tem adversario: a promessa. E o short dele tambem lidera, com
  7,00 contra 5,50.

  NAO DEU: a conta do estrago ja feito. O ITR fala do prazo que JA passou e da
  multa que voce JA deve — quem perdeu, perdeu, e nao ha o que fazer com a
  informacao. Zero views por dia num video de catorze minutos. O terceiro,
  "EPF: o que mudou, o que nao", e explicacao neutra sem adversario: 0,27.

  MUDEI: peguei um numero prometido em praca publica — "agora voce saca o PF no
  caixa eletronico" — e fui ver quanto sai de verdade. Cinquenta por cento pelo
  ATM, setenta e cinco pelo UPI, e vinte e cinco que nao sai nunca. E promessa
  contra conta, nao estrago consumado.

RESSALVA HONESTA SOBRE A FORCA DISSO

Sao TRES titulos. A comparacao de 20/08 e limpa porque a data e a mesma, mas
n=2 nao sustenta lei. O que da alguma confianca e que a mesma forma — promessa
publica contra conta real — ja tinha aparecido como vencedora no
epomeno-epipedo hoje, em outra lingua e outro nicho, sob outro nome (divisao
entre dois grupos). Sao primos: os dois opoem duas coisas que o espectador
acredita serem uma so.

O EIXO, E POR QUE NAO E O OBVIO

`pautas_banco` tem o eixo `8cpc-fitment` esmagando tudo:

  [556] 8th Pay Commission BIG Update Fitment Factor ...... 46.276,7 v/d
  [557] 8th Pay Commission se kya badhegi salary? ......... 46.163,6
  [558] 8th Pay Commission Salary Chart Level 1-18 ........ 27.069,2
  [563] 8th Pay Commission: 400% Salary Hike ..............  9.024,5

E eu NAO peguei nenhum deles, apesar de serem os maiores numeros do banco
inteiro. Motivo: o canal publicou exatamente esse assunto em 20/08 — o video de
5,00 v/d E o fitment factor dos 400%. Repetir o eixo quatro dias depois nao e
seguir o dado, e republicar.

Peguei o segundo eixo, `epfo-30`, que nunca foi usado e e o segundo mais forte:

  [564] EPFO ne PF Withdrawal ka sistema badal dala ........ 8.125,9
  [565] EPFO 3.0 New Rules UPI PF Withdrawal ATM 75% ....... 6.116,4
  [566] PF Withdrawal Process Online EPFO 3.0 ............... 6.057,5

Cuidado com similaridade: o canal tem "EPF Scheme 2026: o que mudou, o que nao
— e a regra dos 36 meses". Aquele e sobre o ESQUEMA e o prazo de 36 meses;
este e sobre COMO e QUANTO se saca. Adjacente, pergunta diferente.

OS NUMEROS, confirmados em duas fontes que batem

  em vigor desde ......... 29 de junho de 2026
  saque pelo UPI ......... ate 75% do saldo
  saque pelo cartao ATM .. ate 50% do saldo
  retencao obrigatoria ... 25%, sempre
  auto-liquidacao ........ pedidos ate 5 lakh, sem intervencao manual
  cartoes ATM ............ distribuidos por fases

VERIFIQUEI DUAS VEZES, E A SEGUNDA MUDOU O VIDEO. A primeira busca dizia que
ate junho o saque por UPI e ATM AINDA NAO estava disponivel, apesar do anuncio
— e isso teria virado o gancho: "prometeram e nao entregaram". So que estamos
em agosto. Fui conferir o estado ATUAL e o quadro e outro: o esquema entrou em
vigor em 29 de junho e a plataforma foi lancada. Publicar "ainda nao existe"
sobre algo que ja funciona seria o erro mais caro possivel neste nicho.

O gancho mudou junto: nao e "nao entregaram", e "entregaram com um limite que
ninguem repetiu". Que e mais verdadeiro e continua sendo promessa contra conta.

O QUE ESTE VIDEO NAO FAZ

  - nao diz que o EPFO 3.0 e ruim: auto-liquidacao ate cinco lakh sem
    intervencao humana e uma melhora real, e o video diz isso;
  - nao promete prazo de cartao ATM para ninguem: a distribuicao e por fases e
    o video afirma que nao da para prever a sua;
  - nao trata dos casos especiais de saque (doenca, casamento, moradia), que
    tem regras proprias e nao cabem aqui;
  - nao da conselho previdenciario.

TAXA DA VOZ. hi-IN-MadhurNeural: R = 11,92 chars/s — a MAIS LENTA da frota,
quase metade do grego — e P = 1,194 s/frase. n = 140.

Consequencia pratica no dimensionamento: com R tao baixo, o mesmo minuto de
video pede quase a METADE dos caracteres que um roteiro grego pede. A spec 005
deste canal mediu 98 chars por cena em 77 cenas para 823,7 s; usei isso como
ponto de partida em vez de recalcular do zero, que e o que o aprendizado 436
manda — densidade historica do CANAL, medida, nao chute.

ORCAMENTO: medido no arquivo pronto (436), e com `duracao_estimada` CRUA, sem
vies por voz — aprendizado 454, confirmado quatro vezes hoje.

  74 cenas, 6 capitulos, 6 no short.
  longo previsto (cru) ... 751,0 s = 12:31
  short previsto ......... 39,8 s   (teto seguro 43,1)

  capitulos, em segundos previstos, todos dentro de [60, 150]:

    131,2  जो वादा हुआ, और जो सच है ............. 13 cenas
    111,3  असल में क्या बदला .................... 12
    122,1  पचास, पचहत्तर, पच्चीस ................ 12
    127,3  वो पच्चीस प्रतिशत क्यों .............. 12
    124,7  वो पच्चीस प्रतिशत कमाता कितना है ..... 12
    132,8  निकालने से पहले क्या देखें ........... 13

  A PRIMEIRA MEDICAO DEU 621,0 s — 10:21, abaixo dos 12 min. QUARTA vez em
  quatro pacotes que a primeira versao sai curta, sempre pelo mesmo motivo de
  fundo: escrevo menos do que planejo. Aqui foram 61 cenas onde eu tinha
  planejado 73, e 92 chars por cena onde a densidade medida do canal e 98.

  Ja que o padrao se repetiu quatro vezes seguidas, ele deixou de ser acidente:
  a primeira versao de uma spec minha sai entre 15% e 30% abaixo do alvo. O
  conserto certo nao e escrever mais na primeira tentativa — e ORCAR a medicao
  como parte do trabalho, sempre com fato reservado para preencher.

  Consertei com o fato que faltava, e ele era importante o bastante para virar
  capitulo: os vinte e cinco por cento retidos RENDEM. A taxa do EPF para
  2025-26 e 8,25% ao ano, terceira vez seguida no mesmo nivel, calculada sobre
  o saldo mensal e creditada uma vez por ano. Sobre o um lakh retido do exemplo
  isso da cerca de 8.250 por ano.

  Isso mudou o video para melhor, e nao so o tamanho. Sem esse capitulo o
  roteiro so acusava a retencao; com ele, o video mostra os dois lados e deixa
  a decisao com quem assiste — que e o que a pauta original prometia.

  TRES PORTOES ME PEGARAM:

  1. COPY — escrevi cabecalhos que este canal nao usa. O 005 usa
     `## HASHTAGS` em secao propria, `## CONFIGURACOES DO STUDIO`,
     `## MUSICA / LICENCA` e `## AVISO SOBRE OS NUMEROS`. Segunda vez hoje que
     erro o formato de copy de um canal, depois do grego. Nao e coincidencia:
     eu escrevo a copy de memoria em vez de copiar o cabecalho do pacote
     anterior DO MESMO canal.
  2. NARRACAO, planilha falada — duas vezes. A pior era a taxa de juros: "ano
     fiscal dois mil vinte e cinco vinte e seis, oito virgula dois cinco por
     cento" sao quatro numeros numa frase, e em hindi por extenso isso e uma
     frase inteira sozinha.
  3. NARRACAO, slop — "इस वीडियो में" ("neste video"). O portao diz para
     comecar o video em vez de anuncia-lo, e ele esta certo.

  E UM ERRO DE HELPER: usei `cap=` num `L()`, que nao aceita. Foi sorte, porque
  capitulo TEM de abrir em layout `titulo` — o helper me impediu de escrever
  algo que o portao reprovaria depois.

CAPITULOS abrem em layout `titulo` (388) e precisam passar de MIN_CAP 60 s.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


# ------------------------------------------- 1. जो वादा हुआ, और जो सच है
T("वादा", "एटीएम से पीएफ़",
  "पिछले कुछ महीनों में एक बात हर जगह सुनाई दी। अब आप अपना पीएफ़ एटीएम से "
  "निकाल सकेंगे, जैसे बैंक का पैसा निकालते हैं।",
  cap="जो वादा हुआ, और जो सच है")
T("और यह सच है", "अफ़वाह नहीं",
  "और यह अफ़वाह नहीं थी। यह सच में हुआ, और आज चालू है। इसलिए यह वीडियो यह "
  "नहीं कहेगा कि आपसे झूठ बोला गया।")
I("लागू", "उनतीस जून से",
  "नई ईपीएफ़ योजना और ईपीएफ़ओ के नए नियम उनतीस जून दो हज़ार छब्बीस से लागू "
  "हो चुके हैं।")
T("तो फिर सवाल क्या है", "रक़म का",
  "तो फिर इस वीडियो का सवाल क्या है। सवाल यह नहीं कि निकाल सकते हैं या नहीं। "
  "सवाल यह है कि कितना निकलता है।")
T("क्योंकि वादे में", "एक शब्द नहीं था",
  "क्योंकि जिस वाक्य ने सबका ध्यान खींचा, उसमें एक शब्द कभी नहीं आया। वह शब्द "
  "है सीमा।")
I("पहला नंबर", "पचहत्तर प्रतिशत",
  "यूपीआई से आप अपने पीएफ़ बैलेंस का अधिकतम पचहत्तर प्रतिशत निकाल सकते हैं।")
I("दूसरा नंबर", "पचास प्रतिशत",
  "और ईपीएफ़ओ के एटीएम कार्ड से यह सीमा और नीचे है। वहाँ अधिकतम पचास प्रतिशत "
  "मिलता है।")
B("दो रास्ते", ["एटीएम", "यूपीआई"], [38, 58],
  "यानी एक ही खाते पर दो अलग सीमाएँ, सिर्फ़ रास्ते के हिसाब से।")
T("इसका मतलब", "रास्ता ही फ़ैसला है",
  "इसका मतलब यह हुआ कि रास्ता चुनना अपने आप में एक फ़ैसला बन गया है। पहले "
  "ऐसा नहीं था।")
I("तीसरा नंबर", "पच्चीस प्रतिशत",
  "और सबसे ज़रूरी नंबर तीसरा है। पच्चीस प्रतिशत रक़म खाते में रुकी रहेगी, "
  "किसी भी रास्ते से।")
T("यह कोई देरी नहीं है", "यह नियम है",
  "ध्यान दीजिए, यह कोई प्रक्रिया की देरी नहीं है जो कल ठीक हो जाएगी। यह "
  "योजना का हिस्सा है।")
T("इसलिए वादा अधूरा नहीं", "अधूरा सुनाया गया",
  "इसलिए कहना यह चाहिए कि वादा अधूरा नहीं था। वह अधूरा सुनाया गया, और सीमा "
  "वाला हिस्सा रास्ते में गिर गया।")
T("अब क्रम से", "पहले क्या बदला",
  "अब इसे क्रम से देखते हैं। पहले यह कि असल में बदला क्या है, क्योंकि बदलाव "
  "सिर्फ़ निकासी का नहीं है।")

# ------------------------------------------- 2. ईपीएफ़ओ में असल में क्या बदला
T("पहला बदलाव", "मंज़ूरी का इंतज़ार",
  "सबसे बड़ा बदलाव वह नहीं है जिसकी चर्चा हुई। सबसे बड़ा बदलाव इंतज़ार का है।",
  cap="असल में क्या बदला")
T("पहले क्या होता था", "दफ़्तर से दफ़्तर",
  "पहले दावा लगाने के बाद वह किसी मेज़ पर जाता था, फिर किसी और मेज़ पर। हर "
  "मेज़ पर दिन जुड़ते थे।")
I("अब", "पाँच लाख तक अपने आप",
  "अब पाँच लाख रुपये तक के दावे अपने आप निपट सकते हैं, बिना किसी मैनुअल "
  "हस्तक्षेप के।")
T("इसका मतलब समझिए", "इंसान बीच से हटा",
  "इसका मतलब यह है कि तय सीमा तक आपके दावे और आपके पैसे के बीच से इंसानी "
  "मंज़ूरी हट गई है।")
T("यह छोटी बात नहीं", "देरी यहीं बनती थी",
  "यह छोटी बात नहीं है, और मैं इसे कमतर नहीं दिखाऊँगा। पीएफ़ की ज़्यादातर "
  "शिकायतें इसी इंतज़ार से बनती थीं।")
I("दूसरा बदलाव", "यूपीआई से सीधे खाते में",
  "दूसरा बदलाव यह कि निकाली गई रक़म यूपीआई के ज़रिए सीधे आपके जुड़े बैंक "
  "खाते में आ सकती है।")
I("तीसरा बदलाव", "पीएफ़ से जुड़ा कार्ड",
  "और तीसरा यह कि ईपीएफ़ओ अपने सदस्यों को पीएफ़ से जुड़ा एटीएम कार्ड देने जा "
  "रहा है।")
T("कार्ड पर एक चेतावनी", "चरणों में मिलेगा",
  "यहाँ एक ईमानदार चेतावनी ज़रूरी है। ये कार्ड सबको एक साथ नहीं मिल रहे, "
  "बल्कि चरणों में बँट रहे हैं।")
T("तो तारीख़ मत पूछिए", "मैं नहीं बता सकता",
  "इसलिए अगर आप पूछें कि आपका कार्ड कब आएगा, तो ईमानदार जवाब है कि मुझे नहीं "
  "पता, और किसी को नहीं पता।")
T("इन तीनों को जोड़िए", "तस्वीर बनती है",
  "इन तीनों बदलावों को जोड़ दीजिए तो तस्वीर बनती है। दावा तेज़, रास्ता आसान, "
  "और रक़म पर एक ढक्कन।")
T("ढक्कन ही असली ख़बर है", "पर वही छूट गया",
  "और वह ढक्कन ही असली ख़बर है, क्योंकि वही तय करता है कि ज़रूरत के दिन "
  "आपके हाथ में कितना आएगा।")
T("तो अब गिनते हैं", "अपने ही पैसे पर",
  "तो अब सीधे गिनती करते हैं, अपने ही खाते के पैसे पर।")

# ------------------------------------------- 3. पचास, पचहत्तर, पच्चीस
T("मान लीजिए", "एक सीधा उदाहरण",
  "मान लीजिए आपके पीएफ़ खाते में चार लाख रुपये जमा हैं। कोई ख़ास स्थिति नहीं, "
  "सामान्य नौकरी और सामान्य जमा।",
  cap="पचास, पचहत्तर, पच्चीस")
T("अब ज़रूरत आ पड़ी", "पूरा चाहिए",
  "अब मान लीजिए कोई ज़रूरत आ पड़ी और आपको लगा कि पूरा पैसा निकाल लूँ। यह सोच "
  "स्वाभाविक है, क्योंकि पैसा आपका है।")
I("यूपीआई से", "तीन लाख",
  "यूपीआई के रास्ते से आपको तीन लाख रुपये मिलेंगे। यह चार लाख का पचहत्तर "
  "प्रतिशत है।")
I("एटीएम से", "दो लाख",
  "एटीएम कार्ड के रास्ते से दो लाख मिलेंगे, क्योंकि वहाँ सीमा पचास प्रतिशत "
  "है।")
B("एक ही खाता", ["एटीएम", "यूपीआई"], [40, 60],
  "एक ही खाता, एक ही ज़रूरत, और एक लाख रुपये का फ़र्क़ सिर्फ़ इस बात से कि "
  "आपने कौन सा बटन दबाया।")
I("और बचा", "एक लाख",
  "और दोनों ही हालत में एक लाख रुपये खाते में रुके रहेंगे। वह पच्चीस प्रतिशत "
  "है।")
T("यह पैसा गया नहीं है", "यह रुका है",
  "साफ़ कर दूँ कि यह पैसा कहीं गया नहीं है। वह आपका है, बढ़ता भी रहेगा, बस "
  "आज आपके हाथ में नहीं आएगा।")
T("पर ज़रूरत के दिन", "फ़र्क़ यही है",
  "लेकिन जिस दिन ज़रूरत होती है, उस दिन खाते में दिखने वाला पैसा और हाथ में "
  "आने वाला पैसा दो अलग चीज़ें बन जाती हैं।")
T("और यही चूक होती है", "लोग पूरा मान लेते हैं",
  "और यहीं सबसे आम चूक होती है। लोग खाते का पूरा बैलेंस देखकर योजना बना लेते "
  "हैं, और ऐन वक़्त पर हिसाब छोटा निकलता है।")
T("अगर रक़म बड़ी हो", "फ़र्क़ भी बड़ा",
  "और ध्यान रहे, जितनी बड़ी जमा रक़म होगी, यह फ़र्क़ भी उतना ही बड़ा होगा। "
  "प्रतिशत वही रहता है, रुपया नहीं।")
T("तो पहला काम", "पचहत्तर प्रतिशत गिनिए",
  "इसलिए पहला काम यही है। अपने बैलेंस का पचहत्तर प्रतिशत निकालिए, और उसी "
  "संख्या से योजना बनाइए।")
T("अब अगला सवाल", "यह सीमा क्यों",
  "अब अगला सवाल, जो जायज़ है। यह सीमा लगाई ही क्यों गई है।")

# ------------------------------------------- 4. वो पच्चीस प्रतिशत क्यों रुका है
T("वजह बताई गई है", "और छिपाई नहीं गई",
  "इसकी वजह छिपाई नहीं गई है, और मैं उसे वैसे ही रखूँगा जैसे वह है। पच्चीस "
  "प्रतिशत की रोक रिटायरमेंट की बचत बचाने के लिए है।",
  cap="वो पच्चीस प्रतिशत क्यों")
T("तर्क सीधा है", "खाता ख़ाली न हो",
  "तर्क सीधा है। अगर निकालना बहुत आसान हो जाए, तो खाता बार बार ख़ाली होगा, "
  "और साठ की उम्र में कुछ नहीं बचेगा।")
T("और यह डर काल्पनिक नहीं", "पर आपका मामला अलग हो सकता है",
  "यह डर काल्पनिक नहीं है। लेकिन इसका मतलब यह भी नहीं कि हर व्यक्ति का मामला "
  "एक जैसा है।")
T("दो लोग", "एक ही नियम",
  "जिसकी नौकरी स्थिर है और जिसकी नहीं, दोनों पर यही एक नियम लगता है। नियम "
  "आपकी स्थिति नहीं पूछता।")
T("इसलिए मैं यह नहीं कहूँगा", "कि नियम ग़लत है",
  "इसलिए मैं यह नहीं कहूँगा कि नियम ग़लत है। मैं यह कहूँगा कि उसे जानकर योजना "
  "बनाना आपकी ज़िम्मेदारी बन गई है।")
T("और आसानी की क़ीमत", "यहीं दिखती है",
  "और आसानी की एक क़ीमत होती है, जो यहीं दिखती है। रास्ता जितना तेज़ हुआ, "
  "ढक्कन उतना ही ज़रूरी माना गया।")
T("यह अदला बदली", "पहले नहीं थी",
  "यह अदला बदली पहले नहीं थी। पहले निकालना मुश्किल था, पर सीमा इस तरह सामने "
  "नहीं खड़ी थी।")
T("अब सोचिए", "आपके लिए कौन सा बेहतर",
  "अब यह सोचना आपके ऊपर है कि आपके लिए क्या बेहतर है। धीमा और पूरा, या तेज़ "
  "और सीमित।")
T("मेरा काम", "सवाल साफ़ रखना",
  "मेरा काम यहाँ जवाब देना नहीं है, बल्कि सवाल साफ़ रखना है। जवाब हर किसी का "
  "अलग होगा, और होना भी चाहिए।")
T("पर एक बात तय है", "पहले से जानना बेहतर है",
  "पर एक बात तय है। यह सीमा ज़रूरत के दिन पता चलना, और आज पता चलना, दो बिलकुल "
  "अलग अनुभव हैं।")
T("आज पता चलने पर", "समय बचता है",
  "आज पता चलने पर आपके पास समय है कि दूसरा इंतज़ाम सोच लें। ज़रूरत के दिन "
  "समय ही वह चीज़ है जो नहीं होती।")
T("तो अब आख़िरी हिस्सा", "करना क्या है",
  "तो अब आख़िरी हिस्सा, जो सबसे काम का है। आज आप कर क्या सकते हैं।")

# ------------------------------------------- 5. निकालने से पहले क्या देखें
T("अब एक ज़रूरी बात", "रुका पैसा मरा नहीं है",
  "अब एक बात जो इस पूरी बहस का पलड़ा बदल देती है, और जिसे मैं छिपाऊँगा नहीं। "
  "वह रुका हुआ पच्चीस प्रतिशत बेकार नहीं पड़ा रहता।",
  cap="वो पच्चीस प्रतिशत कमाता कितना है")
T("ब्याज मिलता है", "और दर अधिसूचित है",
  "उस पर ब्याज मिलता है, और दर सरकार की ओर से अधिसूचित होती है। चालू वित्त "
  "वर्ष की दर तय हो चुकी है।")
I("ब्याज दर", "सवा आठ प्रतिशत",
  "वह दर है आठ दशमलव दो पाँच प्रतिशत सालाना।")
T("और यह लगातार तीसरा साल है", "दर वही रही",
  "और यह लगातार तीसरा साल है जब यह दर वही रखी गई है। सात करोड़ से ज़्यादा "
  "सदस्यों पर यही दर लागू होती है।")
T("अब उसी उदाहरण पर लौटिए", "एक लाख रुका था",
  "अब उसी चार लाख वाले उदाहरण पर लौटिए। वहाँ एक लाख रुपये खाते में रुके थे।")
I("वह एक लाख", "साल में कमाता है",
  "उस एक लाख पर साल भर में लगभग आठ हज़ार दो सौ पचास रुपये ब्याज बनता है।")
T("यानी रुकना", "मुफ़्त नहीं है",
  "यानी वह पैसा रुका हुआ ज़रूर है, पर बैठा हुआ नहीं है। वह काम कर रहा है, और "
  "उसकी दर बुरी नहीं है।")
T("ब्याज कैसे बनता है", "हर महीने, पर मिलता साल में",
  "एक तकनीकी बात जो काम की है। ब्याज हर महीने के चलते बैलेंस पर बनता है, "
  "लेकिन खाते में साल में एक बार जुड़ता है।")
T("इसका असर", "निकासी के समय पर",
  "इसका असर यह है कि आप किस महीने निकालते हैं, यह भी थोड़ा फ़र्क़ डालता है। "
  "साल के बीच में निकाला पैसा उस साल का पूरा ब्याज नहीं कमाता।")
T("तो नियम को दो तरह से देखिए", "रोक और सुरक्षा",
  "इसलिए पच्चीस प्रतिशत की रोक को दो तरह से देखा जा सकता है। एक रोक की तरह, "
  "और एक ऐसी बचत की तरह जो अपने आप बढ़ती है।")
T("मैं दोनों बता रहा हूँ", "फ़ैसला आपका",
  "मैं दोनों पक्ष जानबूझकर रख रहा हूँ, क्योंकि आपकी ज़रूरत तात्कालिक है या "
  "नहीं, यह सिर्फ़ आप जानते हैं।")
T("पर योजना बनाते समय", "दोनों नंबर चाहिए",
  "पर योजना बनाते समय दोनों नंबर चाहिए। कितना हाथ में आएगा, और जो नहीं आएगा "
  "वह किस दर पर बढ़ेगा।")

T("तीन चीज़ें", "और तीनों मुफ़्त",
  "निकालने की सोचने से पहले तीन चीज़ें देख लीजिए। तीनों मुफ़्त हैं और तीनों "
  "आज ही हो सकती हैं।",
  cap="निकालने से पहले क्या देखें")
I("पहला", "असली बैलेंस देखिए",
  "पहला, अपना मौजूदा बैलेंस देखिए, और उसका पचहत्तर प्रतिशत अलग लिख लीजिए। वही "
  "आपकी असली उपलब्ध रक़म है।")
I("दूसरा", "केवाईसी और बैंक",
  "दूसरा, अपनी केवाईसी और जुड़ा हुआ बैंक खाता जाँच लीजिए। यूपीआई का रास्ता "
  "इसी जोड़ पर टिका है।")
I("तीसरा", "रास्ता तय कीजिए",
  "तीसरा, तय कीजिए कि रास्ता कौन सा है। यूपीआई से ज़्यादा मिलता है, यह अब आप "
  "जानते हैं।")
T("और अगर ज़रूरत बड़ी है", "पहले गिनिए",
  "और अगर ज़रूरत बड़ी है, तो निकालने से पहले गिनिए कि पचहत्तर प्रतिशत उसे "
  "पूरा करता भी है या नहीं।")
T("अगर नहीं करता", "तो अभी पता चलना ज़रूरी है",
  "अगर नहीं करता, तो यह जानना आज ज़रूरी है, न कि उस दिन जब पैसे की ज़रूरत "
  "सामने खड़ी हो।")
T("एक बात दोहराऊँगा", "यह सलाह नहीं है",
  "एक बात दोहरा दूँ। यह जानकारी है, वित्तीय सलाह नहीं। आपकी स्थिति के हिसाब "
  "से सही रास्ता बदल सकता है।")
T("और ख़ास मामलों में", "नियम अलग हैं",
  "बीमारी, शादी या घर जैसे ख़ास मामलों में निकासी के अपने अलग नियम हैं, और "
  "वे यहाँ शामिल नहीं हैं।")
T("अब शुरुआत पर लौटते हैं", "वादा और गिनती",
  "अब शुरुआत पर लौटते हैं। वादा था कि पीएफ़ एटीएम से निकलेगा, और वह सच निकला।")
T("पर गिनती अलग निकली", "पचास और पचहत्तर",
  "पर गिनती वैसी नहीं निकली जैसी सुनाई गई थी। एटीएम से पचास, यूपीआई से "
  "पचहत्तर, और पच्चीस वहीं का वहीं।")
T("यह धोखा नहीं है", "यह अधूरी ख़बर है",
  "यह धोखा नहीं है। यह अधूरी ख़बर है, और अधूरी ख़बर का नुक़सान ज़रूरत के दिन "
  "ही दिखता है।")
T("अगले वीडियो में", "पैंतीस साल का हिसाब",
  "अगले वीडियो में मैं इसी खाते का दूसरा हिस्सा लूँगा। पैंतीस साल में यह "
  "पच्चीस प्रतिशत बनता कितना है।")
C("अगर काम आया", "अपना सवाल लिखिए",
  "अगर यह गिनती काम आई हो तो सब्सक्राइब कर लीजिए, और कमेंट में लिखिए कि आपको "
  "एटीएम वाला रास्ता चाहिए या यूपीआई वाला।")

SHORT = [
    {"layout": "titulo", "kicker": "वादा", "sub": "एटीएम से पीएफ़",
     "nar": "कहा गया कि अब पीएफ़ एटीएम से निकलेगा। सच है — पर एक शब्द कभी "
            "नहीं आया। सीमा।",
     "sem_cap": True},
    {"layout": "item", "kicker": "यूपीआई से", "preco": "75%",
     "nar": "यूपीआई से आपके बैलेंस का अधिकतम पचहत्तर प्रतिशत निकलता है।",
     "sem_cap": True},
    {"layout": "item", "kicker": "एटीएम से", "preco": "50%",
     "nar": "और एटीएम कार्ड से सिर्फ़ पचास प्रतिशत।",
     "sem_cap": True},
    {"layout": "barras", "kicker": "एक ही खाता", "itens": ["एटीएम", "यूपीआई"],
     "alturas": [40, 60],
     "nar": "एक ही खाते पर, सिर्फ़ रास्ता बदलने से रक़म बदल जाती है।",
     "sem_cap": True},
    {"layout": "item", "kicker": "और रुकेगा", "preco": "25%",
     "nar": "और पच्चीस प्रतिशत हर हाल में खाते में रुका रहेगा।",
     "sem_cap": True},
    {"layout": "cta", "kicker": "पूरी गिनती", "sub": "चैनल पर",
     "nar": "चार लाख पर यह कितना बनता है, पूरे वीडियो में।",
     "sem_cap": True},
]

COPY = """# ईपीएफ़ओ 3.0: निकलता कितना है

## TITULO
EPFO 3.0: ATM से 50%, UPI से 75% — और 25% कभी नहीं निकलेगा

## DESCRICAO
पिछले कुछ महीनों में एक बात हर जगह सुनाई दी: अब आप अपना पीएफ़ एटीएम से निकाल सकेंगे, जैसे बैंक का पैसा निकालते हैं। यह अफ़वाह नहीं थी — नई ईपीएफ़ योजना और ईपीएफ़ओ के नए नियम 29 जून 2026 से लागू हो चुके हैं, और सुविधा चालू है।

तो फिर सवाल क्या है? सवाल यह नहीं कि निकाल सकते हैं या नहीं। सवाल यह है कि कितना निकलता है — क्योंकि जिस वाक्य ने सबका ध्यान खींचा, उसमें एक शब्द कभी नहीं आया: सीमा।

यूपीआई से आप अपने पीएफ़ बैलेंस का अधिकतम 75% निकाल सकते हैं। ईपीएफ़ओ के एटीएम कार्ड से यह सीमा और नीचे है — अधिकतम 50%। और सबसे ज़रूरी नंबर तीसरा है: 25% रक़म खाते में रुकी रहेगी, किसी भी रास्ते से। यह प्रक्रिया की देरी नहीं है जो कल ठीक हो जाएगी — यह योजना का हिस्सा है, और वजह भी बताई गई है: रिटायरमेंट की बचत बचाना।

वीडियो में 4 लाख रुपये के सीधे उदाहरण पर पूरी गिनती है: यूपीआई से 3 लाख, एटीएम से 2 लाख, और दोनों हालत में 1 लाख खाते में रुका हुआ। एक ही खाता, एक ही ज़रूरत, और एक लाख रुपये का फ़र्क़ सिर्फ़ इस बात से कि आपने कौन सा बटन दबाया।

साथ में वह बदलाव भी, जिसकी चर्चा कम हुई पर जो शायद सबसे बड़ा है: 5 लाख रुपये तक के दावे अब अपने आप निपट सकते हैं, बिना मैनुअल हस्तक्षेप के। यानी तय सीमा तक आपके दावे और आपके पैसे के बीच से इंसानी मंज़ूरी हट गई है। पीएफ़ की ज़्यादातर शिकायतें इसी इंतज़ार से बनती थीं।

अंत में तीन काम जो आज मुफ़्त में किए जा सकते हैं, और एक ईमानदार चेतावनी: एटीएम कार्ड चरणों में बँट रहे हैं, और आपका कब आएगा यह कोई नहीं बता सकता।

{CAPITULOS}

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
एक सवाल जो मुझे सच में जानना है: आपने अपना पीएफ़ बैलेंस पिछली बार कब देखा था, और क्या आपको पता था कि उसका सिर्फ़ 75% ही हाथ में आ सकता है? कमेंट में लिखिए — मुझे लगता है ज़्यादातर लोगों को यह नंबर नहीं पता।

## HASHTAGS
#EPFO #PFWithdrawal #AglaLevel

## TAGS
epfo 3.0, pf withdrawal, epf 2026, upi se pf nikale, atm se pf, pf balance check, epfo new rules, provident fund, 75 percent rule, auto settlement, pf claim, epfo card, salary employee, personal finance hindi, Agla Level

## CONFIGURACOES DO STUDIO
- Idioma: Hindi (hi) | Categoria: Educacao (27)
- Publico: nao e conteudo para criancas
- Conteudo sintetico: SIM, declarado
- Legendas: legendas.srt em hi

## MUSICA / LICENCA
संगीत: {TRILHA}

शैक्षिक सामग्री, वित्तीय सलाह नहीं। कथन AI की मदद से बनाया गया है, शोध और संपादन मानव द्वारा। बीमारी, शादी या घर जैसे ख़ास मामलों की निकासी के अपने अलग नियम हैं, जो इसमें शामिल नहीं हैं।

## AVISO SOBRE OS NUMEROS
24 अगस्त 2026 की स्थिति। नई ईपीएफ़ योजना और ईपीएफ़ओ के नए नियम 29 जून 2026 से प्रभावी — दो स्वतंत्र स्रोतों में एक जैसी जानकारी। निकासी सीमाएँ: यूपीआई से अधिकतम 75%, ईपीएफ़ओ एटीएम कार्ड से अधिकतम 50%, और 25% अनिवार्य रूप से खाते में बनाए रखना — यह रिटायरमेंट बचत की सुरक्षा के लिए बताया गया है। 5 लाख रुपये तक के दावों का स्वतः निपटान बिना मैनुअल हस्तक्षेप के। एटीएम कार्ड चरणबद्ध तरीक़े से वितरित हो रहे हैं, इसलिए किसी व्यक्ति विशेष के लिए तारीख़ का दावा नहीं किया गया है। 4 लाख के उदाहरण की सभी संख्याएँ इन्हीं प्रतिशतों की सीधी गणना हैं और वीडियो में क़दम दर क़दम दिखाई गई हैं। यह सामग्री वित्तीय सलाह नहीं है।
"""

SPEC = {
    "slug": "agla-level",
    "pacote": "agla-level-006",
    "idioma": "hi",
    "voz": "hi-IN-MadhurNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1A2233", "c1": "#0E7C86", "c2": "#E4933B",
               "bg": "#F4F7F5"},
    "thumb": {"l1": "ATM से 50%", "l2": "UPI से 75%"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short
    p = grava(SPEC)
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"gravado em {p}")
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)} "
          f"({sum(len(c['nar']) for c in CENAS)/len(CENAS):.0f}/cena)")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get("cap")]))
