"""labtreinamento-s004 — o mesmo desconto nao tem o mesmo preco: divide pelo PRAZO.

ALAVANCA: A (alcance por short). Quarto short solto do labtreinamento.

O QUE DEU CERTO: a regra do 654 pegou TRES falsos negativos seguidos — o
`conduz.py` reportou "0 publicados, 1 falharam" com HTTP 410 no PUT do binario e
o video estava no ar nas tres vezes. Perguntar ao canal antes de retentar evitou
tres duplicatas. E a disciplina de nao abrir os tres testes travados pelo
experimento 33 continua de pe: nenhum foi aberto hoje.

O QUE NAO DEU, e e a correcao desta rodada: as 13:13 eu escrevi na propria rotina
"ordene os longos livres pelo alcance do short ORIGINAL de cada pacote". Duas
horas depois (658) descobri que as cinco "melhores origens livres do kolejny" que
esse criterio elegeu — `_M8t8SPC_f0` (1.152), `jDa9SM8A7os` (634), `qcY5XC1KtlQ`
(594), `SZV9Vk5YFwI` (414), `5gHnniPl0f8` (323) — sao SEIS COPIAS DO MESMO VIDEO,
exatamente as de `docs/duplicatas-a-apagar.md`. O criterio PREMIAVA DUPLICACAO:
video copiado seis vezes aparece seis vezes no topo. Se eu tivesse construido a
partir dele, o CTA deste short apontaria para um video marcado para EXCLUSAO.
Contagem honesta, por TITULO DISTINTO e excluindo o grupo duplicado INTEIRO (nao
`row_number()=1`, porque a primeira copia tambem sera apagada): epomeno 18/18
titulos, labtreinamento 13/13, kolejny 24 longos mas 19 titulos — livres 36, nao
41. E o duodecimo erro meu com a mesma assinatura: o instrumento fabricou o
achado, e desta vez o instrumento era uma regra que eu mesmo acabara de escrever.

O QUE VOU MUDAR, e e uma coisa so: o inventario volatil SAIU da rotina e foi para
`docs/estoque.md`, versionado, com a consulta que o produz. A rotina agora aponta
para o arquivo em vez de carregar lista. Foi assim que o 652/655 e o 658
nasceram: lista escrita dentro do prompt envelhece ali e eu nao percebo.
NUMERO DE PARTIDA: 214 do short do pacote de origem, e 196 do solto maduro do
canal.

DE ONDE SAI: capitulo "Quando o prazo nao e de trinta dias" do longo
labtreinamento-008 (`bQoujWaY7Hw`), que o short original daquele pacote so
ENCOSTA — ele fecha o prazo em um mes e manda o resto para o canal. Perfil 651:
dinheiro da PROPRIA pessoa, com papel que ela ja tem na mao (a ultima proposta).
O recorte e ARITMETICO: a entrada errada e tratar o desconto como preco, quando o
preco e o desconto DIVIDIDO PELO PRAZO que ele antecipou. Mesmo desconto, prazo
curto, custo muito maior.

IDENTIDADE: faixa atual do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}` com trilha `Inspired` — nove pacotes seguidos. A pauta vem do 008,
mas uso a FAIXA ATUAL e nao a paleta daquele pacote (601, e o erro que repeti tres
vezes em 08/10).

TENDENCIA: o feed BR/26 NAO foi lido nesta rodada, e digo em vez de inventar. Do
PL/26 lido as 06:22 ficou a FORMA: pergunta ou imperativo em segunda pessoa, onze
de quinze. Cena 1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita percentual
# de desconto, nao cita prazo em dias, nao cita taxa de antecipacao, nao cita
# valor e nao nomeia banco nem orgao. Conferido A MAO campo por campo, porque o
# portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru (640).
#
# O QUE O VIDEO AFIRMA: que o custo de um desconto a vista depende do PRAZO que
# ele antecipou, logo o mesmo desconto sai mais caro quando o prazo antecipado e
# curto. Esta no longo labtreinamento-008 (`bQoujWaY7Hw`), capitulos "A conta: o
# desconto dividido pelo que sobra" e "Quando o prazo nao e de trinta dias", com
# as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qualquer percentual de desconto e o resultado da divisao — estao no longo
#       com fonte; o short nao precisa deles para dizer que prazo curto encarece;
#   (2) qualquer taxa de antecipacao de recebiveis — e preco de mercado, muda, e
#       nao foi reconferido hoje em duas fontes; o short MANDA comparar, nao diz
#       o numero;
#   (3) se vale ou nao dar o desconto, que depende do caixa e esta no longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Mesmo desconto?", "sub": "prazos diferentes",
     "nar": "Você deu o mesmo desconto à vista para quem pagaria logo e para "
            "quem pagaria muito depois?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "O desconto não é o preço", "sub": "o prazo é",
     "nar": "Então você cobrou de si mesmo dois juros bem diferentes, porque o "
            "preço do dinheiro não é o desconto que você deu.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Divida", "sub": "pelos dias antecipados",
     "nar": "Divida o desconto pelo que sobra, e divida de novo pelos dias que "
            "você antecipou de verdade.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Prazo curto", "sub": "custa muito mais",
     "nar": "Prazo curto com desconto igual sai muito mais caro, e é exatamente "
            "ali que o cliente esperto compra.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Pegue a proposta", "sub": "e conte os dias",
     "nar": "Pegue a última proposta e conte os dias que o desconto antecipou. A "
            "conta está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Divida pelos", "l2": "dias"}

COPY = """# labtreinamento-s004

## TITULO
Desconto à Vista: o Mesmo Desconto Não Tem o Mesmo Preço — Divida pelo Prazo

## TITULO SHORT
Mesmo desconto, prazo curto: muito mais caro

## DESCRICAO
Quem dá desconto para o cliente pagar à vista costuma ter uma política só: um percentual, igual para todo mundo. É o jeito mais simples de administrar e também o mais caro, porque o desconto não é o preço do dinheiro — o preço é o desconto dividido pelo prazo que ele antecipou.

Pense em dois clientes com a mesma proposta e o mesmo desconto. Um deles pagaria em poucos dias; o outro só pagaria bem mais adiante. Para o primeiro, você entregou o mesmo abatimento para trazer o dinheiro quase nada para a frente: o juro implícito é altíssimo. Para o segundo, o mesmo abatimento comprou um pedaço grande de tempo, e o juro implícito é muito menor. Mesma linha na tabela, dois negócios completamente diferentes — e o único que percebeu isso, até agora, foi o cliente que escolheu o lado bom.

A conta tem dois passos e nenhum número de fora. Primeiro, o desconto sobre o que efetivamente sobra: você não abate do que recebeu, você abate do que ia receber. Segundo, e é esse que quase ninguém dá: divida o resultado pelos dias que o pagamento foi realmente antecipado, contados da data em que o cliente ia pagar até a data em que ele pagou. Só depois desse segundo passo os dois negócios ficam comparáveis entre si, e comparáveis com a antecipação que o seu banco vende.

O que sai disso não é "pare de dar desconto". É que um desconto único, igual para qualquer prazo, está sempre caro demais em algum pedaço da sua carteira — e esse pedaço é exatamente o que mais gente vai escolher. Quem quer continuar dando desconto à vista precisa de uma política que olhe o prazo, não só o valor.

Não há aqui nenhum percentual, nenhum prazo em dias e nenhuma taxa: os números que decidem estão na sua última proposta e no extrato da sua conta. A conta completa, com outros prazos, a comparação com a antecipação de recebíveis e os casos em que o desconto é a decisão certa mesmo assim — estão no vídeo.

## COMENTARIO FIXADO
O passo que quase ninguém dá é o segundo. Todo mundo divide o desconto pelo que sobra; poucos dividem de novo pelos DIAS que o pagamento foi antecipado — da data em que o cliente ia pagar até a data em que pagou. Sem esse segundo passo, dois negócios com o mesmo desconto e prazos muito diferentes parecem iguais, e eles não são: o de prazo curto é o caro. Se você for olhar a sua última proposta, comente só se o prazo antecipado foi curto ou longo — sem valores e sem percentual.

## HASHTAGS
#Financas #Precificacao #LabTreinamento

## TAGS
desconto a vista, precificacao, juro implicito, antecipacao de recebiveis, fluxo de caixa, prazo de pagamento, proposta comercial, pequeno negocio, financas da empresa, margem, tabela de precos, politica de desconto, brasil, calculo, lab treinamento

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

## AVISO SOBRE OS NUMEROS
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita percentual de
desconto, nao cita prazo em dias, nao cita taxa de antecipacao, nao cita valor e
nao nomeia banco nem orgao. Conferido a mao campo por campo, porque o portao
`narracao` conta quantidades por frase e nao pega digito cru (640).

O QUE O VIDEO AFIRMA: que o custo de um desconto a vista depende do PRAZO que ele
antecipou, logo o mesmo desconto sai mais caro quando o prazo antecipado e curto.
Esta no longo labtreinamento-008 (bQoujWaY7Hw), capitulos "A conta: o desconto
dividido pelo que sobra" e "Quando o prazo nao e de trinta dias", com as fontes.

DESCARTADO, e vai escrito:
  (1) qualquer percentual de desconto e o resultado da divisao — estao no longo
      com fonte; o short nao precisa deles para dizer que prazo curto encarece;
  (2) qualquer taxa de antecipacao de recebiveis — e preco de mercado, muda, e
      nao foi reconferido hoje em duas fontes; o short MANDA comparar;
  (3) se vale ou nao dar o desconto, que depende do caixa e esta no longo.

## FONTES
O longo de onde este short foi extraido (labtreinamento-008, bQoujWaY7Hw) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s004",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "bQoujWaY7Hw",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s004.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
