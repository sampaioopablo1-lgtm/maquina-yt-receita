#!/usr/bin/env python3
"""Monta a spec agla-level-008.

ALAVANCA ATACADA: **A — conversao short -> inscrito, pela FORMA.**

NUMERO DE PARTIDA, medido em 31/08/2026:

    agla-level ....... 11 pacotes publicados, 114 views TOTAIS
                       short: mediana 1,62 views/dia, topo 2,38
                       longo: mediana 0,16 views/dia
                       inscritos ganhos: ZERO, em tudo
                       veredito: `canal frio`

O QUE DEU CERTO — e e um sinal que os outros canais frios NAO tem: a
RETENCAO do short. "ITR 2026" segurou oitenta e nove virgula dois por cento
(trinta e cinco segundos de trinta e nove) e "EPF 2026: 36 महीने का नियम"
segurou oitenta virgula seis por cento (trinta de trinta e oito). Quem chega
assiste ate o fim. O problema deste canal nao e o espectador desistir.

O QUE NAO DEU: duas coisas, e nenhuma delas e retencao de short.
Primeira, o LONGO. Os quatro mais antigos tem entre setecentos e vinte e seis
e oitocentos e quarenta segundos, e o de vinte e seis views segurou tres
virgula cinco por cento — vinte e sete segundos de setecentos e setenta e
sete. Segunda, e a que decide: ZERO inscritos em onze pacotes.

E da para dizer por que, olhando os titulos: ITR, EPF, EPFO tres ponto zero,
oitava comissao de pagamento, regime tributario. Os cinco sao REGRA
INSTITUCIONAL. Sao fato sobre o mundo com prazo do governo, e nao conta que o
espectador faca em si mesmo com numero dele. E o aprendizado 482 diz
exatamente isso: fato nao converte, metodo converte. Este canal e a versao
mais pura desse erro na frota — onze de onze.

O QUE MUDO POR CAUSA DISSO: **EIXO NOVO** (regra do `canal frio`), e o eixo
sai da regra do governo e passa para o holerite DELE. Zero numero
institucional: nao ha aliquota, nao ha teto, nao ha percentual de contribuicao.
Os dois numeros da conta estao nas duas linhas do papel que ele recebe todo
mes. E — aprendizado 539, medido hoje no labtreinamento — **o short entrega a
subtracao FECHADA**, com o resultado, e nao empurra o numero para o longo.

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: a rotina manda eixo novo e nao fixa faixa. Alavanca B manda o
PISO, e o piso mais conservador e o do `suspenso`: **oito minutos**. Com o
longo em zero virgula dezesseis views/dia, dimensionar para treze minutos
seria gastar render em algo que ninguem termina.

Oito capitulos. E cada capitulo desenhado com ~64s NA ESTIMATIVA, nunca 60,
por causa do aprendizado 537 medido hoje: o desvio da estimativa nao tem sinal
fixo, e no labtreinamento-007 um capitulo estimado em 60,4s rodou abaixo de
60s e `copy_md` engoliu a abertura do seguinte — oito desenhados, sete no
video. A resposta fecha ate ~192s na estimativa, e o tempo REAL vai ser
conferido no copy.md renderizado antes de publicar.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **CTC contra o que cai na conta — a diferenca calculada no proprio
holerite**. Os eixos ja publicados neste canal sao ITR, EPF, EPFO, oitava
comissao e regime tributario. Salario liquido contra salario anunciado nunca
foi ao ar aqui, e e a dor mais universal do assalariado indiano.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o numero da carta de oferta e o que o banco creditou;
2. e ESCOLHA COM PRAZO — a proxima oferta, ou a proxima conversa de aumento;
3. o SHORT entrega a conta — a subtracao fechada, com o resultado.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita aliquota de imposto, nao cita percentual de contribuicao,
nao cita teto, nao cita faixa e nao cita nome de empresa nem de banco. Os dois
numeros da conta estao no holerite do proprio espectador. Nao ha numero meu
para certificar em duas fontes, e por isso nao ha numero meu que possa
envelhecer nem que dependa do estado ou da empresa dele.

O QUE O VIDEO NAO FAZ: nao diz que CTC alto e bom ou ruim, nao recomenda
aceitar nem recusar oferta, nao promete aumento e nao e aconselhamento
financeiro nem tributario.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("एक नंबर आपको बताया गया", "दूसरा बैंक में आता है",
  "आपको नौकरी मिलते समय एक नंबर बताया गया था। हर महीने बैंक में एक दूसरा नंबर "
  "आता है। और आपने शायद कभी दोनों को साथ रखकर नहीं देखा।",
  cap="दो नंबर, एक ही नौकरी")
I("यह छिपाना नहीं है", "यह बनावट है",
  "इसमें कोई धोखा ज़रूरी नहीं है। दोनों अलग होते ही हैं, क्योंकि वे दो अलग "
  "चीज़ें नाप रहे हैं।")
I("पर फ़र्क़ का आकार", "आपको पता होना चाहिए",
  "लेकिन उस फ़र्क़ का आकार आपको पता होना चाहिए। वही तय करता है कि अगली बार "
  "कोई नंबर सुनकर आप क्या समझेंगे।")
I("और यह चुनाव है", "समय सीमा के साथ",
  "और इसकी समय सीमा साफ़ है: अगली ऑफ़र, या अगली बढ़ोतरी की बातचीत।")
I("दोनों नंबर मौजूद हैं", "और दोनों आपके हैं",
  "अच्छी बात यह है कि दोनों नंबर पहले से मौजूद हैं, और दोनों आपके हैं। एक "
  "काग़ज़ पर है, दूसरा बैंक के विवरण में।")
I("आगे क्या", "एक घटाव",
  "कुछ ही मिनटों में आप यह हिसाब ख़ुद कर लेंगे। एक घटाव है, उन्हीं नंबरों से "
  "जो आपके पास पहले से हैं।")

# -------------------------------------------------------------------- cap 2
T("दो पलड़े", "जो कहा गया, जो आया",
  "इस हिसाब के दो पलड़े हैं, और सबसे आम ग़लती सिर्फ़ पहले को देखना है।",
  cap="दो पलड़े: कहा गया और आया")
I("पहला पलड़ा", "सालाना नंबर",
  "पहला पलड़ा वह सालाना नंबर है जो आपको बताया गया। उसे बारह से भाग दीजिए, "
  "ताकि वह महीने की भाषा में आ जाए।")
I("यह महीने का नहीं है", "यह सिर्फ़ भाग है",
  "ध्यान रहे, यह आपकी महीने की कमाई नहीं है। यह सिर्फ़ वही सालाना नंबर है, "
  "बारह हिस्सों में बाँटा हुआ।")
I("दूसरा पलड़ा", "जो सच में आया",
  "दूसरा पलड़ा वह है जो सच में आपके खाते में आया। पिछले महीने का, बैंक के "
  "विवरण से — याददाश्त से नहीं।")
I("एक महीना काफ़ी नहीं", "तीन लीजिए",
  "एक महीना काफ़ी नहीं है। पिछले तीन का औसत लीजिए, क्योंकि किसी महीने में "
  "कुछ अलग जुड़ता या कटता है।")
I("अब दोनों", "एक ही इकाई में",
  "अब दोनों नंबर एक ही इकाई में हैं: रुपये, महीने के। दोनों तुलना के लायक़ "
  "हो गए।")
I("अब यह राय नहीं है", "अब यह गणित है",
  "और जैसे ही इकाई एक हुई, यह राय नहीं रहा। यह गणित हो गया।")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — com a margem do aprendizado 537.
T("हिसाब", "एक घटाव",
  "तो हिसाब यह रहा। एक घटाव, और चाहें तो एक भाग।",
  cap="हिसाब: एक घटाव")
I("पहला क़दम", "सालाना बटा बारह",
  "पहला क़दम: बताया गया सालाना नंबर, बारह से भाग। इसे लिख लीजिए।")
I("दूसरा क़दम", "तीन महीने का औसत",
  "दूसरा क़दम: पिछले तीन महीनों में खाते में आई रक़म का औसत। इसे भी लिख "
  "लीजिए।")
I("तीसरा क़दम", "घटाइए",
  "तीसरा क़दम: पहले में से दूसरा घटाइए। जो बचा, वही हर महीने का फ़र्क़ है।")
I("यही जवाब है", "रुपयों में",
  "यही आपका जवाब है, और वह रुपयों में है। न प्रतिशत, न कोई भारी शब्द, और "
  "किसी की राय पर निर्भर नहीं।")
I("चाहें तो", "बारह से गुणा",
  "चाहें तो उसे बारह से गुणा कर दीजिए। तब आपको साल का फ़र्क़ दिख जाएगा।")
I("हिसाब यहीं पूरा", "बाक़ी कारण है",
  "हिसाब यहीं पूरा हो गया, और आप अभी अपना निकाल सकते हैं। बाक़ी वीडियो यह है "
  "कि वह फ़र्क़ कहाँ जाता है, और कब यह हिसाब धोखा देता है।")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("फ़र्क़ कहाँ जाता है", "काग़ज़ पर लिखा है",
  "अब वह हिस्सा जो ज़्यादातर लोग नहीं पढ़ते: वह फ़र्क़ जाता कहाँ है।",
  cap="फ़र्क़ कहाँ जाता है")
I("कुछ कटता है", "और आपका ही रहता है",
  "कुछ हिस्सा कटता है लेकिन आपका ही रहता है — वह किसी खाते में जमा होता है "
  "जिस तक आपकी पहुँच बाद में होती है।")
I("कुछ कटता है", "और वापस नहीं आता",
  "कुछ हिस्सा कटता है और वापस नहीं आता, क्योंकि वह किसी और को जाता है।")
I("कुछ जुड़ा ही नहीं था", "पर नंबर में था",
  "और कुछ हिस्सा कभी आपके हाथ आने वाला था ही नहीं — वह उस बड़े नंबर में "
  "जोड़ा गया था, बस।")
I("तीनों अलग हैं", "और यही असली बात है",
  "ये तीनों अलग चीज़ें हैं, और अपने काग़ज़ पर इन्हें अलग-अलग पहचानना ही इस "
  "वीडियो का असली काम है।")
I("अपनी पर्ची लीजिए", "और तीन ढेर बनाइए",
  "अपनी वेतन पर्ची लीजिए और हर कटौती को तीन में से किसी एक ढेर में डालिए: "
  "मेरा है, मेरा नहीं है, कभी था ही नहीं।")
I("जो न समझ आए", "पूछिए",
  "जो लाइन समझ न आए, उसे अपनी कंपनी के मानव संसाधन विभाग से पूछ लीजिए। यह "
  "सवाल पूछना सामान्य है।")

# -------------------------------------------------------------------- cap 5
T("जो हिसाब में नहीं आता", "और कहना ज़रूरी है",
  "कुछ चीज़ें इस हिसाब में नहीं आतीं, और उन्हें छिपाने से बेहतर है कह देना।",
  cap="जो हिसाब में नहीं आता")
I("पहली", "जो जमा हो रहा है",
  "पहली: जो कटकर आपके ही खाते में जमा हो रहा है, वह ग़ायब नहीं हुआ। वह "
  "आज नहीं मिला, इतना ही।")
I("इसलिए फ़र्क़", "पूरा नुक़सान नहीं",
  "इसलिए यह फ़र्क़ पूरा का पूरा नुक़सान नहीं है। यह वह रक़म है जो इस महीने "
  "आपके हाथ में नहीं आई।")
I("दूसरी", "बीमा और सुविधाएँ",
  "दूसरी: बीमा और वैसी सुविधाएँ जिनका मूल्य होता है पर वह पर्ची में रुपये "
  "बनकर नहीं दिखता।")
I("पर सावधानी", "मूल्य तभी जब काम आए",
  "पर यहाँ सावधानी: सुविधा का मूल्य तभी है जब वह आपके काम की हो। जिस चीज़ "
  "का आप कभी उपयोग नहीं करते, उसका मूल्य आपके लिए शून्य है।")
I("तीसरी", "जो हर महीने नहीं आता",
  "तीसरी: साल में एक बार मिलने वाली रक़म। वह बड़े नंबर में है, पर हर महीने "
  "के हिसाब में नहीं।")
I("इसीलिए तीन महीने", "और इसीलिए औसत",
  "इसीलिए तीन महीने का औसत लीजिए, और जिस महीने कुछ असामान्य हुआ हो उसे अलग "
  "से पहचान लीजिए।")

# -------------------------------------------------------------------- cap 6
T("जब हिसाब धोखा देता है", "दो ऑफ़र",
  "अब वह स्थिति जो लगभग सबको धोखा देती है, और वह एक अलग अध्याय की हक़दार है.",
  cap="जब हिसाब धोखा देता है")
I("दो ऑफ़र", "एक ही बड़ा नंबर",
  "मान लीजिए दो ऑफ़र हैं और दोनों का सालाना नंबर एक जैसा है। लोग यहीं मान "
  "लेते हैं कि दोनों बराबर हैं।")
I("पर बनावट अलग", "तो हाथ अलग",
  "पर दोनों की बनावट अलग हो सकती है, और तब हर महीने हाथ में आने वाली रक़म "
  "अलग होगी।")
I("इसलिए तुलना", "बड़े नंबर की नहीं",
  "इसलिए दो ऑफ़र की तुलना बड़े नंबर से मत कीजिए। जो हर महीने खाते में आएगा, "
  "उससे कीजिए।")
I("वह पूछा जा सकता है", "और पूछना चाहिए",
  "और वह पूछा जा सकता है। ऑफ़र मिलने पर महीने की अनुमानित रक़म पूछना पूरी "
  "तरह सामान्य सवाल है।")
I("उलटा भी होता है", "बड़ा नंबर, कम हाथ",
  "उलटा भी होता है: बड़ा सालाना नंबर, पर हाथ में कम। और छोटा नंबर, पर हाथ "
  "में ज़्यादा।")
I("दोनों सही हो सकते हैं", "आपका नंबर तय करेगा",
  "दोनों ही ऑफ़र सही हो सकते हैं, और कोई एक आम तौर पर बेहतर नहीं है। सही वही "
  "है जिसे आपका नंबर बताए। ग़लत सिर्फ़ यह है कि बिना देखे मान लेना।")

# -------------------------------------------------------------------- cap 7
T("एक महीने से", "पूरे साल तक",
  "अब वह क़दम जो इस फ़र्क़ का आकार महसूस कराता है।",
  cap="एक महीने से पूरे साल तक")
I("एक महीना", "छोटा लगता है",
  "एक महीने का फ़र्क़ अक्सर छोटा लगता है। छोटा होता भी है, और इसीलिए वह हर "
  "बार बिना ध्यान खींचे निकल जाता है।")
I("बारह से गुणा", "अब वह दिखता है",
  "उसे बारह से गुणा कीजिए। वही व्यवहार, जुड़कर।")
I("फिर सालों से", "जितने साल आप यहाँ हैं",
  "फिर उन सालों से गुणा कीजिए जितने साल आप इसी ढाँचे में काम कर रहे हैं।")
I("किसी जानी चीज़ से तुलना", "ताकि आकार समझ आए",
  "आकार समझने के लिए उसे किसी जानी-पहचानी चीज़ से जोड़िए। जैसे कितने महीने "
  "का किराया, या कितने महीने का घर का ख़र्च।")
I("और शून्य भी जवाब है", "पूरी तरह",
  "यह भी हो सकता है कि फ़र्क़ छोटा निकले और आपको कुछ बदलने की ज़रूरत न हो। "
  "वह भी पूरा जवाब है, और अब वह अनुमान नहीं, हिसाब है।")
I("अच्छी बात", "यह फिर आता है",
  "अच्छी बात यह है कि यह फ़ैसला हर ऑफ़र और हर बढ़ोतरी पर लौटकर आता है। एक "
  "बार का हिसाब अगली बार को नहीं बाँधता।")

# -------------------------------------------------------------------- cap 8
T("आज क्या कीजिए", "तीन क़दम",
  "अंत में वह जो आज किया जा सकता है, तीन क़दमों में।",
  cap="आज क्या कीजिए")
L("तीन क़दम",
  ["सालाना बटा बारह", "तीन महीने का औसत", "घटाइए"],
  "पहला: बताया गया सालाना नंबर, बारह से भाग। दूसरा: पिछले तीन महीनों में खाते "
  "में आई रक़म का औसत। तीसरा: पहले में से दूसरा घटाइए।")
I("फिर पर्ची खोलिए", "और तीन ढेर",
  "फिर वेतन पर्ची खोलिए और कटौतियों को तीन ढेरों में बाँटिए: मेरा है, मेरा "
  "नहीं है, कभी था ही नहीं।")
I("यह संख्या रखिए", "अगली बातचीत के लिए",
  "यह संख्या संभालकर रखिए। अगली ऑफ़र या अगली बढ़ोतरी की बातचीत में आप बड़े "
  "नंबर पर नहीं, इसी पर बात कर पाएँगे।")
I("आज कुछ बदलिए मत", "पहले जान लीजिए",
  "और आज कुछ बदलने की ज़रूरत नहीं है। पहले जान लेना ही पूरा क़दम है।")
C("अपना नंबर लिखिए", "टिप्पणी में",
  "अगर आप यह हिसाब करें तो नीचे सिर्फ़ एक चीज़ लिखिए: महीने का फ़र्क़, "
  "रुपयों में। न कंपनी का नाम, न अपना वेतन। मैं देखना चाहता हूँ कि यह संख्या "
  "कितनी अलग-अलग निकलती है।")

# =============================== O SHORT =====================================
# APRENDIZADO 539: o short entrega a subtracao FECHADA, com o resultado.
# O que fica para o longo e para onde o dinheiro foi, nao o numero.

SHORT = [
    {"layout": "titulo", "kicker": "जो नंबर बताया गया",
     "sub": "वो खाते में नहीं आता",
     "nar": "जो सालाना नंबर आपको बताया गया था, वह खाते में नहीं आता। फ़र्क़ "
            "अभी निकालिए।", "sem_cap": True},
    {"layout": "titulo", "kicker": "पहला", "sub": "सालाना बटा बारह",
     "nar": "पहला: बताया गया सालाना नंबर, बारह से भाग।", "sem_cap": True},
    {"layout": "titulo", "kicker": "दूसरा", "sub": "तीन महीने का औसत",
     "nar": "दूसरा: पिछले तीन महीनों में खाते में आई रक़म का औसत।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "घटाइए", "sub": "यही आपका फ़र्क़ है",
     "nar": "पहले में से दूसरा घटाइए। जो बचा, वही महीने का फ़र्क़ है। बारह से "
            "गुणा कीजिए, साल का भी मिल जाएगा।", "sem_cap": True},
    {"layout": "cta", "kicker": "वो पैसा जाता कहाँ है",
     "sub": "पूरा वीडियो नीचे",
     "nar": "वह पैसा जाता कहाँ है, पूरा वीडियो नीचे लिंक में।",
     "sem_cap": True},
]

THUMB = {"l1": "CTC या", "l2": "हाथ में"}

COPY = """# बताया गया नंबर और खाते में आया नंबर: फ़र्क़ अपनी ही पर्ची से निकालिए

## TITULO
CTC या हाथ में आने वाली सैलरी? अपनी पर्ची से फ़र्क़ ख़ुद निकालिए

## DESCRICAO
नौकरी मिलते समय आपको एक सालाना नंबर बताया गया था। हर महीने बैंक में एक दूसरा नंबर आता है। दोनों का अलग होना कोई धोखा नहीं है — वे दो अलग चीज़ें नाप रहे हैं — लेकिन उस फ़र्क़ का आकार आपको पता होना चाहिए, क्योंकि वही तय करता है कि अगली ऑफ़र या अगली बढ़ोतरी की बातचीत में आप किस नंबर पर बात करेंगे।

इस वीडियो में मेरा एक भी नंबर नहीं है। कोई कर की दर नहीं, कोई अंशदान का प्रतिशत नहीं, कोई सीमा नहीं, किसी कंपनी या बैंक का नाम नहीं। हिसाब के दोनों नंबर आपके अपने हैं और दोनों पहले से मौजूद हैं: एक आपकी वेतन पर्ची पर, दूसरा बैंक के विवरण में।

हिसाब एक घटाव है। बताया गया सालाना नंबर बारह से भाग दीजिए — यह आपकी महीने की कमाई नहीं, बस वही नंबर बारह हिस्सों में बँटा हुआ है। फिर पिछले तीन महीनों में खाते में सच में आई रक़म का औसत निकालिए, याददाश्त से नहीं बल्कि बैंक के विवरण से, क्योंकि किसी महीने में कुछ अलग जुड़ता या कटता है। अब पहले में से दूसरा घटाइए: जो बचा वही हर महीने का फ़र्क़ है, रुपयों में। बारह से गुणा कीजिए तो साल का फ़र्क़ सामने आ जाएगा।

एक अध्याय इस पर है कि वह फ़र्क़ जाता कहाँ है, और वहाँ तीन अलग चीज़ें हैं जिन्हें अपने काग़ज़ पर अलग-अलग पहचानना ही असली काम है: कुछ कटता है पर आपका ही रहता है, कुछ कटता है और वापस नहीं आता, और कुछ कभी आपके हाथ आने वाला था ही नहीं। अपनी पर्ची लीजिए और हर कटौती को तीन ढेरों में डालिए — मेरा है, मेरा नहीं है, कभी था ही नहीं।

एक अध्याय उस पर है जो हिसाब में नहीं आता, क्योंकि छिपाने से बेहतर है कह देना: जो कटकर आपके ही खाते में जमा हो रहा है वह ग़ायब नहीं हुआ; बीमा और वैसी सुविधाएँ जिनका मूल्य तभी है जब वे आपके काम की हों; और साल में एक बार मिलने वाली रक़म, जो बड़े नंबर में है पर हर महीने के हिसाब में नहीं।

और एक अध्याय उस स्थिति पर है जो लगभग सबको धोखा देती है: दो ऑफ़र, एक जैसा सालाना नंबर, अलग बनावट — और इसलिए हर महीने हाथ में अलग रक़म। दो ऑफ़र की तुलना बड़े नंबर से नहीं, महीने की अनुमानित रक़म से कीजिए; वह पूछना पूरी तरह सामान्य सवाल है।

अंत में तीन क़दम, उन्हीं नंबरों से जो आपके पास आज मौजूद हैं।

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
यह हिसाब करके नीचे सिर्फ़ एक चीज़ लिखिए: महीने का फ़र्क़, रुपयों में। न कंपनी का नाम, न अपना वेतन, सिर्फ़ फ़र्क़। मैं देखना चाहता हूँ कि एक जैसी नौकरियों में भी यह संख्या कितनी अलग-अलग निकलती है।

## HASHTAGS
#सैलरी #करियर #AglaLevel

## TAGS
ctc kya hai, in hand salary, salary slip kaise padhein, ctc vs in hand, take home salary, vetan parchi, salary structure, offer letter, job offer comparison, monthly salary calculation, kitni salary milegi, deductions in salary, personal finance hindi, career hindi, salary negotiation

## CONFIGURACOES DO STUDIO
- Idioma: Hindi (hi) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: India | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita aliquota de imposto, nao cita percentual de contribuicao, nao cita teto nem faixa, nao cita nome de empresa nem de banco e nao compara empregadores entre si. Os dois numeros da conta sao do proprio espectador: o numero anual esta na carta de oferta ou na vetan parchi dele, e o valor creditado esta no extrato bancario dele. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa do estado, do setor ou da empresa dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer aliquota, percentual de dedução ou limite legal. Esses valores mudam por regime, por faixa e por ano, e citar um so deles tornaria a conta errada para a maioria de quem assiste — e o video precisa exatamente do contrario, porque a conta e feita com o papel de cada um. O video tambem nao diz que um numero anual alto e bom ou ruim, nao recomenda aceitar nem recusar oferta, nao promete aumento e nao e aconselhamento financeiro nem tributario.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/agla-level-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "agla-level",
    "pacote": "agla-level-008",
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/agla-level-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
