#!/usr/bin/env python3
"""Monta a spec agla-level-009.

ALAVANCA ATACADA: **A — conversao short -> inscrito, pela FORMA**, somada ao
primeiro teste real de FOOTAGE neste canal.

NUMERO DE PARTIDA, medido em 04/10/2026, em dado de vida inteira (coluna
`views` das linhas de `videos.list`, nao das linhas de Analytics — aprendizado
554):

    agla-level ....... 12 videos publicados, 135 views de canal
                       teto de um video: 28 views
                       inscritos: UM, em doze pacotes
                       veredito: `canal frio` — o mais frio da frota

O QUE DEU CERTO, e e um numero que nenhum outro canal da frota tem: a RAZAO
longo/short. O par "8th Pay Commission" fechou short 28 e longo 26 — noventa e
tres por cento de quem viu o short atravessou para o longo. Na frota inteira
essa razao fica entre dois e vinte e quatro por cento. Aqui ela e a melhor que
existe.

O QUE ISSO DIZ, e muda o diagnostico deste canal: o gargalo NAO e a travessia
do short para o longo. Quem chega atravessa. O gargalo e que ninguem chega —
vinte e oito views e o teto de doze videos. Isso e distribuicao, nao formato.

E o par "8th Pay Commission" e o agla-level-004, que e exatamente a spec que
pediu footage e **nao recebeu**: sete cenas com `layout: "broll"`, sete caidas
no fallback (lower-third sobre preto), porque `api.pexels.com` deu
`TimeoutError` a partir do runner. O melhor video deste canal e o unico que foi
DESENHADO com footage, e ele rodou sem footage nenhum. Nao da para afirmar que
o footage e a causa — a amostra e um — mas da para dizer que o desenho que
produziu o melhor numero do canal nunca foi testado como foi desenhado.

Entao este pacote testa isso: footage de verdade, pela pre-busca.

O QUE MUDO POR CAUSA DISSO: duas coisas, e so duas.
1. **EIXO NOVO** (regra do `canal frio`), descrito abaixo.
2. **TRES CENAS DE ABERTURA DE CAPITULO COM FOOTAGE REAL**, com `broll_url` ja
   resolvido na spec pelo `prebusca_broll.py` rodado de onde a API responde.
   Nao sete: tres. Se o CDN tambem estiver bloqueado no runner, perco tres
   cenas para o fallback, nao oito — e o log dira qual dos dois hosts caiu.

O QUE NAO MUDO, de proposito: a voz, a paleta, a trilha e o idioma ficam. Com
amostra de um nao se mexe em duas variaveis ao mesmo tempo.

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: a rotina manda eixo novo e nao fixa faixa. O piso mais
conservador e o do `suspenso`: **oito minutos**. Com o teto do canal em 28
views, dimensionar para treze minutos seria gastar render em algo que ninguem
termina.

Oito capitulos. Cada capitulo desenhado com ~68s NA ESTIMATIVA — nunca 60, e
nunca entre 60 e 64,2 — por causa do aprendizado 553, medido em 02/10/2026 no
labtreinamento-008: um capitulo estimado em 60,8s (1,3% de folga sobre o
MIN_CAP) rodou curto e `copy_md` engoliu a abertura do seguinte. Oito
desenhados, sete no video, e o portao passou LIMPO. O desvio da voz chega a
4,9% e nao tem sinal fixo, entao 1,3% nao e folga. O `MARGEM_CAP` agora cobra
7%, e este pacote e desenhado com 13%.

A SUBTRACAO FECHA EM 196,6s na estimativa — dentro dos primeiros 200 s, que e a
regra. A cena seguinte e so a ponte, e o capitulo 4 abre em 215,9s. O longo
fica em 558,4s = 9,31 min, entre o piso de 480 e o teto de 900. O tempo REAL
sai do `legendas.srt` renderizado e e conferido antes de publicar.

Os oito capitulos ficam em 73,0 / 67,1 / 71,3 / 72,5 / 69,7 / 72,9 / 71,4 e
48,5s de NARRACAO. Somados os 0,3s de intervalo por cena, o menor dos sete que
o portao confere e 68,6s contra os 64,2s exigidos — 7% de margem sobre a
exigencia, que ja e 7% sobre o piso. O oitavo nao e conferido por nao ter
capitulo depois dele.

As cenas de footage levam narracao CURTA (~8s) de proposito: o `escolher` do
`broll.py` recusa clipe mais curto que a fala, e `FOLGA_S` cobra 3s acima da
estimativa. Cena de 8s pede clipe de 11s, que o Pexels tem de sobra; cena de
15s pede 18s, que afunila a escolha e empurra para o fallback.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **a rubrica que esta na propria vetan parchi dele e so chega se
for pedida — quanto voltou sem ser reclamado no ano passado.**

Os eixos ja publicados neste canal sao ITR, EPF, EPFO 3.0, oitava comissao,
regime tributario e CTC contra liquido (o 008). Este nao e o 008 de novo: o 008
compara o numero ANUNCIADO com o CREDITADO, e a conta e uma subtracao entre
dois numeros que chegam sozinhos. Aqui os dois numeros sao outros — o que
estava RESERVADO no nome dele contra o que ele EFETIVAMENTE pediu — e o
resultado nao e uma diferenca de contabilidade, e dinheiro que ninguem pagou a
ninguem porque nao foi reclamado.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — a rubrica esta no nome dele, na pr√≥pria parchi dele;
2. e ESCOLHA COM PRAZO — a data limite de dar entrada na empresa DELE, que chegou
   no e-mail dele;
3. o SHORT entrega a conta — a subtracao fechada, com o resultado.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita limite de isencao, nao cita aliquota, nao cita percentual,
nao cita nome de rubrica obrigatoria, nao cita nome de empresa e nao afirma o
que acontece com o dinheiro nao reclamado — porque isso varia por empresa e eu
nao tenho fonte para nenhuma delas. O video diz apenas o que e verificavel no
papel do proprio espectador: a rubrica esta la ou nao esta; ele pediu ou nao
pediu.

O QUE O VIDEO NAO FAZ: nao diz qual estrutura salarial e melhor, nao recomenda
aceitar nem recusar oferta, nao afirma que a empresa fica com o nao reclamado,
nao promete economia de imposto e nao e aconselhamento financeiro nem
tributario.
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


def B(kicker, sub, nar, q, cap=None):
    """Cena de abertura de capitulo COM FOOTAGE.

    O `copy_md` aceita `broll` ao lado de `titulo` como cena que abre secao,
    porque no epomeno-epipedo-004 as sete aberturas eram broll e ele desenhou
    7 capitulos para publicar 4. Narracao curta de proposito: ver o
    DIMENSIONAMENTO.
    """
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 197 SEGUNDOS ==========================
# A resposta fecha no fim do capitulo 3. Nada essencial depois disso.

# -------------------------------------------------------------------- cap 1
B("कुछ रक़म माँगने पर मिलती है", "अपने आप नहीं आती",
  "आपकी वेतन पर्ची पर कुछ लाइनें ऐसी हैं जो अपने आप नहीं आतीं। वे आती हैं तभी, "
  "जब आप माँगते हैं।",
  "person reading paper documents at a desk",
  cap="माँगने पर मिलने वाला पैसा")
I("और जो नहीं माँगा गया", "वो हाथ नहीं आया",
  "और जो नहीं माँगा गया, वो आपके हाथ नहीं आया। कोई सूचना नहीं आती, कोई शिकायत "
  "दर्ज नहीं होती। साल ख़त्म होता है और वो रक़म आपके खाते में कभी नहीं दिखती।")
I("मेरा एक भी नंबर नहीं", "दोनों नंबर आपके हैं",
  "हिसाब में मेरा एक भी नंबर नहीं है। कोई सीमा नहीं, कोई प्रतिशत नहीं, किसी "
  "कंपनी का नाम नहीं। हिसाब के दोनों नंबर आपके अपने काग़ज़ पर हैं। और मैं यह भी "
  "नहीं कहूँगा कि उस रक़म का आगे क्या होता है, क्योंकि वो हर जगह अलग है और मेरे "
  "पास उसका कोई भरोसेमंद स्रोत नहीं है।")
I("समय सीमा भी आपकी है", "आपके मेल में आई थी",
  "और इसकी समय सीमा भी आपकी ही है: आपकी कंपनी में दावा करने की आख़िरी तारीख़, "
  "जो आपको मेल में मिली थी।")
I("दो अध्याय में हिसाब", "पूरा हो जाएगा",
  "अगले दो अध्यायों में हिसाब पूरा हो जाएगा। एक घटाव, दो नंबर, और दोनों आज आपके "
  "पास मौजूद हैं।")

# -------------------------------------------------------------------- cap 2
T("पर्ची उठाइए", "और लाइनें छाँटिए",
  "अब पर्ची उठाइए, पूरी, नीचे तक। आपको तीन तरह की लाइनें दिखेंगी, और पहला नंबर "
  "सिर्फ़ एक तरह से बनता है।",
  cap="पहला नंबर: पर्ची की वो लाइनें")
I("पहली तरह", "बिना शर्त हर महीने",
  "पहली तरह: वो रक़म जो हर महीने अपने आप आती है, चाहे आप कुछ करें या न करें। यह "
  "पहले नंबर में नहीं आती, क्योंकि यह छूटती ही नहीं।")
I("दूसरी तरह", "कटकर आपके नाम जमा",
  "दूसरी तरह: वो जो काटकर आपके ही नाम जमा होती है। यह भी पहले नंबर में नहीं "
  "आती, क्योंकि यह ग़ायब नहीं हुई — इसने जगह बदली है।")
I("तीसरी तरह", "यही हमारा नंबर है",
  "तीसरी तरह, और यही हमारा नंबर है: वो लाइनें जिनके सामने रक़म लिखी है, पर वो "
  "रक़म बिल जमा करने पर आती है। नाम कुछ भी हो, पहचान एक ही है — शर्त के साथ "
  "रखी गई रक़म।")
I("जोड़िए, बारह से गुणा", "यह पहला नंबर है",
  "इन तीसरी तरह की सारी लाइनें जोड़ लीजिए। महीने का जोड़ बारह से गुणा कीजिए। यह "
  "साल भर में आपके नाम रखी गई रक़म है, और यही पहला नंबर है।")

# -------------------------------------------------------------------- cap 3
B("दूसरा नंबर", "याददाश्त से नहीं निकलेगा",
  "दूसरा नंबर याददाश्त से नहीं निकलेगा। वो पिछले साल के आपके अपने दावों से "
  "निकलेगा।",
  "hands using a calculator on a desk with documents",
  cap="दूसरा नंबर, और घटाव")
I("पिछले बारह महीने", "सच में कितना लिया",
  "पिछले बारह महीनों में आपने इन लाइनों के बदले सच में कितना लिया? बिल जमा किए "
  "और पैसा मिला — उसका जोड़। मेल में, या पर्ची में उसी लाइन के सामने, यह दिखा "
  "होगा।")
I("याद ही नहीं आ रहा", "तो जवाब शून्य है",
  "अगर यह याद ही नहीं आ रहा, तो यही आपका जवाब है: शून्य। और शून्य भी एक नंबर "
  "है, जिसे जानना सबसे ज़्यादा ज़रूरी है।")
I("अब घटाइए", "पहला, उसमें से दूसरा",
  "अब घटाइए। पहला नंबर, उसमें से दूसरा नंबर। जो बचा, वही रक़म आपके नाम रखी थी "
  "और आपके हाथ नहीं आई। रुपयों में, पूरे साल की।")
I("हिसाब पूरा", "आगे है क्यों और कैसे",
  "हिसाब पूरा हो गया। आगे के अध्याय इस पर हैं कि यह नंबर बड़ा क्यों निकलता है, "
  "और अगली बार इसे शून्य के पास कैसे लाया जाए। और एक अध्याय उस पर भी है जो इस "
  "घटाव में जान‑बूझकर नहीं रखा गया।")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("यह नंबर बड़ा क्यों", "जब पैसा आपका ही था",
  "अब सवाल यह है कि यह नंबर इतना बड़ा क्यों निकलता है, जब वो रक़म आपके ही नाम "
  "रखी थी।",
  cap="यह नंबर बड़ा क्यों निकलता है")
I("पहली वजह", "बिल",
  "पहली वजह: बिल। जो रक़म बिल देने पर आती है, वो बिल के बिना नहीं आती। और बिल "
  "साल के अंत में इकट्ठे नहीं होते — वे महीने भर में बनते और खो जाते हैं।")
I("दूसरी वजह", "तारीख़",
  "दूसरी वजह: तारीख़। दावा करने की खिड़की हर जगह साल भर खुली नहीं रहती। जिस दिन "
  "वो बंद हुई, उस साल की उस रक़म का सवाल ख़त्म।")
I("तीसरी वजह", "और सबसे चुपचाप",
  "तीसरी वजह, और सबसे चुपचाप: आपको पता ही नहीं था कि वो लाइन आपकी पर्ची पर है। "
  "जो लाइन पढ़ी नहीं गई, उसका दावा भी नहीं होता।")
I("तीनों आपके हाथ में", "कोई नियम नहीं बदलना",
  "और ध्यान दीजिए: तीनों वजहें आपके हाथ में हैं। कोई नियम बदलने की ज़रूरत नहीं "
  "है — तीनों आपके अपने काग़ज़ और अपनी तारीख़ों का मामला हैं। और यही इस हिसाब "
  "की पूरी बात है: जो आपके हाथ में नहीं है, उस पर मैं आपका समय नहीं लगाऊँगा।")

# -------------------------------------------------------------------- cap 5
B("तीन वजहें", "तीन क़दम",
  "तो तीनों वजहों के सामने एक-एक क़दम रखिए। तीनों आज शुरू हो सकते हैं।",
  "person organizing receipts and paperwork on a table",
  cap="तीनों के लिए एक-एक क़दम")
I("बिल के लिए", "एक जगह",
  "बिल के लिए: एक जगह। फ़ोन में एक फ़ोल्डर, या मेज़ पर एक लिफ़ाफ़ा। बिल बनते ही "
  "वहाँ जाए, महीने के अंत का इंतज़ार नहीं।")
I("तारीख़ के लिए", "एक अलार्म",
  "तारीख़ के लिए: एक अलार्म। अपनी कंपनी की आख़िरी तारीख़ पता कीजिए, और उससे तीन "
  "हफ़्ते पहले का रिमाइंडर आज लगा दीजिए।")
I("लाइन के लिए", "एक बार पूरी पर्ची",
  "लाइन के लिए: एक बार पूरी पर्ची पढ़िए, हर लाइन, नीचे तक। जो लाइन समझ न आए, "
  "उसका नाम लिखकर पूछ लीजिए — यह पूछना पूरी तरह सामान्य सवाल है।")
I("अगर एक ही कर सकें", "तो अलार्म वाला कीजिए",
  "और अगर तीन में से एक ही कर सकते हैं, तो अलार्म वाला कीजिए। बिल खो जाने पर भी "
  "ज़्यादातर जगह दोबारा निकल आते हैं, पर तारीख़ निकल जाने पर कुछ नहीं बचता।")
I("तीन क़दम, तीन वजहें", "अगले साल का घटाव",
  "तीन क़दम, तीन वजहें। और अगले साल का यही घटाव इसी से छोटा निकलेगा।")

# -------------------------------------------------------------------- cap 6
T("वो बात जो कहनी चाहिए", "यह घटाव सब नहीं नापता",
  "अब वो बात, जिसे छिपाने से बेहतर है कह देना: यह घटाव सब कुछ नहीं नापता, और "
  "तीन चीज़ें इसमें जान‑बूझकर नहीं हैं।",
  cap="जो इस हिसाब में नहीं आता")
I("जो कटकर जमा हुई", "वो ग़ायब नहीं हुई",
  "जो रक़म काटकर आपके ही नाम जमा हो रही है, वो इस नंबर में नहीं है और होनी भी "
  "नहीं चाहिए। वो ग़ायब नहीं हुई — उसकी जगह बदली है।")
I("जो बिना शर्त आती है", "छूटने का सवाल नहीं",
  "जो रक़म बिना शर्त हर महीने आती है, वो भी इसमें नहीं है। उसे माँगना नहीं "
  "पड़ता, तो छूटने का सवाल भी नहीं उठता। उसे जोड़ देने से नंबर बड़ा दिखेगा और "
  "वजह ग़लत होगी।")
I("साल में एक बार", "इसमें मत जोड़िए",
  "साल में एक बार मिलने वाली रक़म अलग मामला है। वो बड़े नंबर में दिखती है पर "
  "महीने के इस हिसाब में नहीं आती — उसे इसमें मत जोड़िए। वो अपनी जगह एक अलग "
  "सवाल है, और अलग ही पूछा जाना चाहिए।")
I("और अगर लाइन ही नहीं है", "तो जवाब शून्य है",
  "और एक ईमानदार बात: अगर आपकी पर्ची पर तीसरी तरह की लाइन एक भी नहीं है, तो "
  "आपका जवाब शून्य है। वो भी नतीजा है, और अगली बातचीत का विषय है।")

# -------------------------------------------------------------------- cap 7
T("इस नंबर का एक काम", "अगली बातचीत में",
  "यह नंबर निकल चुका है। अब इसका एक काम बाक़ी है, और वो अगली बातचीत में होता "
  "है।",
  cap="अगली बातचीत में कौन सा नंबर")
I("बड़ा सालाना नंबर", "अकेले कुछ नहीं बताता",
  "अगली ऑफ़र में बड़ा सालाना नंबर अकेले कुछ नहीं बताता। दो ऑफ़र का सालाना नंबर "
  "एक जैसा हो सकता है और बनावट अलग — और इसलिए हाथ में आने वाली रक़म अलग।")
I("तो यह पूछिए", "कौन सी शर्त पर है",
  "तो यह पूछिए: कौन सी लाइनें बिना शर्त हैं और कौन सी बिल पर। यह सवाल पूरी तरह "
  "सामान्य है, और इसका जवाब लिखित में माँगा जा सकता है। पूछने का सही समय ऑफ़र "
  "मानने से पहले है, बाद में नहीं।")
I("मौजूदा जगह पर", "एक शांत तर्क",
  "और अपनी मौजूदा जगह पर यही नंबर एक शांत तर्क है: इतनी रक़म मेरे नाम रखी थी, "
  "और इन तीन वजहों से मेरे हाथ नहीं आई। यह शिकायत नहीं है, यह एक नंबर है — और "
  "नंबर पर बातचीत आसान होती है।")
I("यह वीडियो नहीं कहता", "कौन सी बनावट अच्छी है",
  "और यह वीडियो नहीं कहता कि कौन सी बनावट अच्छी है। वो आपके ख़र्चों पर निर्भर "
  "करता है, और वो आप जानते हैं, मैं नहीं।")

# -------------------------------------------------------------------- cap 8
T("आज, इसी काग़ज़ से", "तीन क़दम",
  "तो आज, इसी काग़ज़ से, तीन क़दम — और तीनों में कोई नया नंबर नहीं चाहिए।",
  cap="तीन क़दम, आज के काग़ज़ से")
I("पहला क़दम", "जोड़िए और बारह से गुणा",
  "पहला: पर्ची उठाकर तीसरी तरह की लाइनें जोड़िए और बारह से गुणा कीजिए। यह पहला "
  "नंबर है, और यह आज बन जाएगा।")
I("दूसरा क़दम", "घटाइए — शून्य भी जवाब है",
  "दूसरा: पिछले साल जो सच में लिया, उसका जोड़ निकालिए — और याद न हो तो शून्य भी "
  "जवाब है। अब घटाइए।")
I("तीसरा क़दम", "एक फ़ोल्डर, एक अलार्म",
  "तीसरा: आज एक फ़ोल्डर बनाइए और एक अलार्म लगाइए। यही दो चीज़ें अगले साल का "
  "नंबर बदलेंगी।")
C("नीचे सिर्फ़ फ़र्क़ लिखिए", "न कंपनी, न सैलरी",
  "और नीचे कमेंट में सिर्फ़ एक चीज़ लिखिए: साल का फ़र्क़, रुपयों में। न कंपनी "
  "का नाम, न अपनी सैलरी।")


# =============================== O SHORT =====================================
# APRENDIZADO 539: o short entrega a subtracao FECHADA, com o resultado.
# O que fica para o longo e POR QUE o numero sai grande, nao o numero.

SHORT = [
    {"layout": "titulo", "kicker": "पर्ची पर रखा पैसा",
     "sub": "माँगे बिना नहीं मिलता",
     "nar": "पर्ची पर कुछ रक़म आपके नाम रखी है, जो माँगे बिना हाथ नहीं "
            "आती। कितनी, निकालिए।", "sem_cap": True},
    {"layout": "titulo", "kicker": "पहला", "sub": "बिल वाली लाइनें, बारह से गुणा",
     "nar": "पहला: वो लाइनें जोड़िए जिनकी रक़म बिल देने पर आती है। बारह "
            "से गुणा।", "sem_cap": True},
    {"layout": "titulo", "kicker": "दूसरा", "sub": "पिछले साल सच में लिया",
     "nar": "दूसरा: पिछले साल आपने इनके बदले सच में कितना लिया। याद न हो तो "
            "शून्य।", "sem_cap": True},
    {"layout": "titulo", "kicker": "घटाइए", "sub": "यही रक़म हाथ नहीं आई",
     "nar": "पहले में से दूसरा घटाइए। जो बचा, वही रक़म आपके नाम रखी थी और "
            "हाथ नहीं आई।", "sem_cap": True},
    {"layout": "cta", "kicker": "बड़ा क्यों निकलता है",
     "sub": "पूरा वीडियो नीचे",
     "nar": "यह नंबर बड़ा क्यों निकलता है, पूरा वीडियो नीचे।",
     "sem_cap": True},
]

THUMB = {"l1": "पर्ची पर", "l2": "रखा पैसा"}

COPY = """# पर्ची पर रखी वो रक़म जो माँगे बिना हाथ नहीं आती

## TITULO
वेतन पर्ची पर रखा पैसा: पिछले साल कितना आपके हाथ नहीं आया?

## TITULO SHORT
पर्ची पर रखा पैसा: कितना छूट गया?

## DESCRICAO
आपकी वेतन पर्ची पर कुछ लाइनें ऐसी हैं जिनके सामने रक़म लिखी होती है, पर वो रक़म अपने आप नहीं आती — वो बिल जमा करने पर आती है। और जो नहीं माँगा गया, वो आपके हाथ नहीं आया। इसकी कोई सूचना नहीं आती, कोई शिकायत दर्ज नहीं होती: साल ख़त्म होता है और वो रक़म आपके खाते में कभी नहीं दिखती।

इस वीडियो में मेरा एक भी नंबर नहीं है। कोई सीमा नहीं, कोई प्रतिशत नहीं, कोई दर नहीं, किसी कंपनी का नाम नहीं। मैं यह भी नहीं कहता कि उस रक़म का क्या होता है, क्योंकि वो हर जगह अलग है और मेरे पास उसका कोई स्रोत नहीं। हिसाब के दोनों नंबर आपके अपने काग़ज़ पर हैं, और दोनों आज मौजूद हैं।

हिसाब एक घटाव है। पहले पर्ची उठाइए, पूरी, नीचे तक, और लाइनों को तीन ढेरों में छाँटिए: जो बिना शर्त हर महीने आती हैं; जो काटकर आपके ही नाम जमा होती हैं; और जिनकी रक़म बिल देने पर आती है। पहले दो ढेर इस हिसाब में नहीं हैं — पहला छूटता ही नहीं, और दूसरा ग़ायब नहीं हुआ, उसकी जगह बदली है। तीसरा ढेर ही हमारा नंबर है: उसे जोड़िए और बारह से गुणा कीजिए। यह साल भर में आपके नाम रखी गई रक़म है।

दूसरा नंबर याददाश्त से नहीं निकलेगा। पिछले बारह महीनों में आपने इन्हीं लाइनों के बदले सच में कितना लिया — बिल जमा किए और पैसा मिला — उसका जोड़। यह मेल में मिलेगा, या पर्ची में उसी लाइन के सामने। और अगर याद ही नहीं आ रहा, तो यही आपका जवाब है: शून्य। अब पहले में से दूसरा घटाइए। जो बचा, वही रक़म आपके नाम रखी थी और आपके हाथ नहीं आई, पूरे साल की, रुपयों में।

एक अध्याय इस पर है कि यह नंबर बड़ा क्यों निकलता है, और वहाँ तीन वजहें हैं जो तीनों आपके हाथ में हैं: बिल, जो महीने भर में बनते और खो जाते हैं; तारीख़, क्योंकि दावे की खिड़की साल भर खुली नहीं रहती; और वो लाइन जो आपने कभी पढ़ी ही नहीं। अगले अध्याय में तीनों के सामने एक-एक क़दम है — एक फ़ोल्डर, एक अलार्म, और एक बार पूरी पर्ची पढ़ना।

एक अध्याय उस पर है जो इस हिसाब में जान‑बूझकर नहीं आता, क्योंकि छिपाने से बेहतर है कह देना: कटकर जमा होने वाली रक़म, बिना शर्त आने वाली रक़म, और साल में एक बार मिलने वाली रक़म। और अगर आपकी पर्ची पर तीसरी तरह की लाइन एक भी नहीं है, तो आपका जवाब शून्य है — वो भी नतीजा है।

और एक अध्याय इस पर है कि यही नंबर अगली बातचीत में कैसे काम आता है: दो ऑफ़र का सालाना नंबर एक जैसा हो सकता है और बनावट अलग, इसलिए हाथ में आने वाली रक़म अलग। पूछना यह है कि कौन सी लाइनें बिना शर्त हैं और कौन सी बिल पर।

अंत में तीन क़दम, उन्हीं नंबरों से जो आपके पास आज मौजूद हैं।

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
यह हिसाब करके नीचे सिर्फ़ एक चीज़ लिखिए: साल का फ़र्क़, रुपयों में। न कंपनी का नाम, न अपनी सैलरी, सिर्फ़ फ़र्क़। और अगर आपकी पर्ची पर ऐसी एक भी लाइन नहीं है, तो शून्य लिखिए — मैं यही देखना चाहता हूँ कि यह कितनी जगह शून्य निकलता है।

## HASHTAGS
#सैलरी #करियर #AglaLevel

## TAGS
salary slip kaise padhein, vetan parchi, reimbursement claim, salary slip reimbursement, flexible benefit plan, bill submit karke paisa, take home salary, salary structure, ctc vs in hand, salary components explained, personal finance hindi, career hindi, salary negotiation, hr se kya puchein, paisa kahan jata hai

## CONFIGURACOES DO STUDIO
- Idioma: Hindi (hi) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: India | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita limite de isencao, nao cita aliquota, nao cita percentual de contribuicao, nao cita teto nem faixa, nao cita nome de empresa e nao nomeia nenhuma rubrica especifica como obrigatoria ou garantida. Os dois numeros da conta sao do proprio espectador: o primeiro sai das linhas condicionais da vetan parchi dele multiplicadas por doze, e o segundo sai dos reembolsos que ele mesmo pediu e recebeu nos ultimos doze meses. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa do estado, do setor ou da empresa dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer limite de isencao ou aliquota, porque muda por regime, por faixa e por ano, e citar um so tornaria a conta errada para a maioria de quem assiste; (2) o nome de qualquer rubrica, porque a nomenclatura varia por empresa e nomear uma faria o espectador procurar a palavra em vez de procurar a CONDICAO, que e o que o video ensina a reconhecer; (3) **o que acontece com o dinheiro nao reclamado** — o video afirma apenas que ele nao chegou ao espectador, que e o unico fato verificavel no papel dele. Dizer que a empresa fica com ele seria afirmacao sobre pratica empresarial, que varia por contrato e para a qual eu nao tenho duas fontes oficiais. O video tambem nao diz qual estrutura salarial e melhor, nao recomenda aceitar nem recusar oferta, nao promete economia de imposto e nao e aconselhamento financeiro nem tributario.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/agla-level-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "agla-level",
    "pacote": "agla-level-009",
    "idioma": "hi",
    "voz": "hi-IN-MadhurNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1D2D44", "c1": "#B23A48", "c2": "#E9A03B", "bg": "#F5F2EA"},
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
    grava(SPEC, "fabrica/specs/agla-level-009.json")
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
    for c in CENAS:
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
