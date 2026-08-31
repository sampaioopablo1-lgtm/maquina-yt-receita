#!/usr/bin/env python3
"""Monta a spec nivel-do-jogo-008.

Esta rodada nao ataca uma alavanca: ela troca o EIXO do canal, porque o numero
diz que o problema nao esta na alavanca.

NUMERO DE PARTIDA, medido em 31/08/2026:

    nivel-do-jogo ..... 3 inscritos, 21 videos publicos, 396 views totais
                        longo: mediana de 0,06 views/dia
                        veredito: `canal frio`
    game-money-lab .... 0 inscritos, 12 videos publicos, 188 views totais
                        longo: mediana de 0,04 views/dia
                        veredito: `canal frio`

Os dois canais tem o MESMO nicho — economia dos games — em linguas diferentes,
e os dois estao frios. Quando o mesmo nicho falha em duas linguas, a hipotese
"o canal precisa de outro assunto" fica fraca e a hipotese "o nicho nao admite
a forma que converte" fica forte.

O QUE DEU CERTO: dos oito titulos publicados, os dois unicos que sao ESCOLHA do
espectador sao "EA FC 27: Standard, Ultimate ou Plus?" e "Loja em Reais, Cartao
em Dolar ou Gift Card?". Os outros seis sao fato sobre a industria — demissoes
na Square Enix, Lei Felca, inflacao nos games, por que a skin custa duzentos
reais, preco dos jogos, precificacao da Steam.

O QUE NAO DEU: seis de oito eixos nao passam a condicao 2 do aprendizado 504.
Quanto custou fazer um jogo e quanto lucra um estudio sao numeros que o
espectador RECEBE. Ele nao decide nada e nao ha conta que ele faca em si mesmo.

O QUE MUDO POR CAUSA DISSO — e nao e o assunto, e o EIXO: o canal para de
falar da economia da INDUSTRIA e passa a falar do dinheiro DELE com jogos. E o
unico lugar deste nicho onde as tres condicoes do 504 cabem juntas, e e onde os
dois titulos que ja eram escolha ja estavam. (Aprendizado 534.)

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `canal frio`. A rotina manda EIXO NOVO e nao fixa faixa para frio;
alavanca B manda o PISO, e o piso mais conservador da rotina e o do `suspenso`:
**oito minutos**. Com mediana de longo em 0,06 views/dia, dimensionar para doze
ou quinze minutos seria gastar render em algo que ninguem assiste.

Oito capitulos, e nao nove, porque `copy_md` so abre capitulo sessenta segundos
depois do anterior: em 480 segundos, nove capitulos nao cabem sem que um seja
engolido. A RESPOSTA fecha no capitulo 3, dentro dos primeiros duzentos
segundos.

E a regra do `suspenso` — o melhor material vai para o short — vale aqui: o
short entrega a conta inteira, nao a manchete.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **assinatura contra compra, com os jogos que ele mesmo jogou**.
Nunca usado neste canal.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele pagou de assinatura e o que ele gastaria
   comprando;
2. e ESCOLHA COM PRAZO — a assinatura renova, e ele decide renovar ou nao;
3. o SHORT entrega a conta — a soma dos precos dos jogos que ele jogou, menos o
   que pagou no ano.

ESTRUTURA copiada do outlier que a coleta de hoje mediu em 29,3x a mediana da
amostra turca — "Ev Almak Yerine Kirada Kalsan Ne Olurdu? Hesapladim":
contrafactual binario em segunda pessoa. E a mesma forma que hoje moveu o longo
em dois canais (aprendizado 532). Assunto NAO copiado, e nem poderia: aquele e
imovel, este e jogo.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita preco de assinatura, nao cita preco de jogo, nao cita
catalogo, nao cita nome de servico. Todos os numeros da conta sao do proprio
espectador — o extrato dele mostra o que pagou, e a loja mostra o preco de hoje
dos jogos que ELE jogou. Nao ha numero meu para certificar, e por isso nao ha
numero meu que possa envelhecer nem que dependa de qual servico ele assina.

O QUE O VIDEO NAO FAZ: nao diz que assinatura e boa ou ruim, nao recomenda
servico, nao compara catalogos, nao promete economia e nao e aconselhamento
financeiro.
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
T("Você paga todo mês", "e nunca conferiu",
  "Tem uma cobrança que entra na sua fatura todo mês, ou uma vez por ano, e "
  "que você renova sem pensar. A assinatura de jogos.",
  cap="Você renova sem conferir")
I("Não é imposto", "é escolha",
  "Isso não é uma conta de luz. Ninguém te obriga. Você escolhe renovar, e "
  "escolhe de novo na renovação seguinte.")
I("A promessa", "sai mais barato",
  "A promessa é sempre a mesma: sai mais barato do que comprar. E na maioria "
  "das vezes ela até é verdadeira.")
I("Mas na maioria não é você", "é a média",
  "Só que essa frase vale para quem joga muita coisa do catálogo. A pergunta "
  "que interessa é se ela vale para você, com o que você jogou de verdade.")
I("E isso ninguém calcula", "nem o serviço",
  "Ninguém faz essa conta por você. O serviço não tem interesse em fazer, e "
  "você não tem os dois números do lado do outro.")
I("Os números existem", "e são seus",
  "Mas os dois números existem, e os dois são seus. Um está no seu extrato. O "
  "outro está no seu histórico de jogos.")
I("O que vem agora", "uma soma e uma subtração",
  "Em alguns minutos você faz essa conta sozinho: uma soma e uma subtração, "
  "com o que já está gravado na sua conta.")

# -------------------------------------------------------------------- cap 2
T("Os dois lados", "o que saiu e o que valeu",
  "A conta tem dois lados, e o erro mais comum é olhar só para um deles.",
  cap="Os dois lados da conta")
I("Lado um", "o que saiu do bolso",
  "O primeiro lado é simples: quanto saiu do seu bolso em assinatura nos "
  "últimos doze meses.")
I("Cuidado aqui", "some tudo",
  "Some tudo, inclusive os meses em que você quase não abriu o console. Você "
  "pagou por eles do mesmo jeito.")
I("Lado dois", "o que você jogou",
  "O segundo lado é o que você realmente jogou. Não o que estava no catálogo, "
  "não o que você adicionou na lista.")
I("A diferença importa", "jogado, não disponível",
  "Catálogo enorme não é valor recebido. O que entra na conta é só o que você "
  "abriu e jogou de fato.")
I("E vale por preço", "não por quantidade",
  "E cada um desses jogos entra pelo preço dele, não pela contagem. Dez jogos "
  "baratos não valem o mesmo que dois caros.")
I("Qual preço", "o que você pagaria",
  "O preço que conta é o que você pagaria por ele hoje, na loja, se tivesse "
  "que comprar.")
I("Agora dá pra comparar", "os dois em reais",
  "Com os dois lados em reais, a comparação deixa de ser opinião e vira "
  "aritmética. E aritmética não depende de quem está falando.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("A conta", "uma soma e uma subtração",
  "Então a conta. Uma soma, uma subtração, e você precisa de duas listas.",
  cap="A conta: soma e subtração")
I("Primeira lista", "os jogos que você jogou",
  "Primeira lista: os jogos do catálogo que você abriu nos últimos doze meses. "
  "Seu histórico de jogos mostra isso.")
I("Anote o preço", "de cada um",
  "Ao lado de cada um, anote o preço dele hoje na loja. É o que você teria "
  "gasto comprando.")
I("Some", "esse é o valor recebido",
  "Some essa coluna. O resultado é quanto de jogo você efetivamente consumiu, "
  "em reais.")
I("Segunda conta", "o que você pagou",
  "Agora o outro lado: some tudo o que você pagou de assinatura nos mesmos "
  "doze meses.")
I("Subtraia", "e o sinal responde",
  "Subtraia o que você pagou do valor que você somou. O sinal do resultado "
  "responde a pergunta.")
I("Positivo", "a assinatura te devolveu",
  "Se sobrou positivo, a assinatura te devolveu mais do que custou, e essa é a "
  "diferença em reais.")
I("Negativo", "você pagou a mais",
  "Se ficou negativo, você pagou mais do que consumiu, e o número é exatamente "
  "quanto.")
I("Por que funciona", "os dois lados são seus",
  "Funciona porque os dois lados são seus, e do mesmo período. Não entra "
  "média, não entra catálogo, não entra promessa.")
I("Pronto", "o resto é onde achar",
  "Essa é a conta inteira. O que vem agora é onde achar cada número e o que "
  "essa conta não pega.")

# ===================== DEPOIS DOS 200 SEGUNDOS ==============================

# -------------------------------------------------------------------- cap 4
T("Onde achar", "tudo já está gravado",
  "Os dois números já existem gravados. Nenhum deles você precisa estimar.",
  cap="Onde achar os números")
I("O que você pagou", "no histórico de compras",
  "O que você pagou está no histórico de compras da sua conta, ou na fatura do "
  "cartão, mês a mês.")
I("Cuidado com a renovação", "o preço pode ter mudado",
  "Olhe o valor de cada cobrança, não o preço anunciado hoje. Renovação e "
  "promoção de entrada costumam ser valores diferentes.")
I("O que você jogou", "no histórico de jogos",
  "O que você jogou está no seu histórico de atividade. A maioria das "
  "plataformas guarda isso e ainda mostra o tempo de cada jogo.")
I("Se tiver o tempo", "use como filtro",
  "Se aparecer o tempo jogado, use como filtro: um jogo que você abriu por "
  "vinte minutos e largou não é valor recebido.")
I("O preço de cada um", "na própria loja",
  "O preço de cada jogo você pega na própria loja, hoje. Não precisa lembrar "
  "quanto custava no lançamento.")
I("Se estiver em promoção", "use o preço cheio",
  "Se estiver em promoção, use o preço cheio. Promoção é sorte de data, e não "
  "é isso que você está medindo.")
I("Tudo no mesmo dia", "os dois lados",
  "Levante os dois lados no mesmo dia. Preço de hoje contra fatura de hoje.")

# -------------------------------------------------------------------- cap 5
T("O que a conta não pega", "e é importante",
  "Agora o que essa conta não cobre, porque sem isso ela fica torta.",
  cap="O que a conta não pega")
I("Multijogador", "às vezes vem junto",
  "Primeiro: em alguns serviços o online faz parte do mesmo pacote. Se você "
  "só joga online, isso é valor recebido mesmo sem catálogo.")
I("Como resolver", "some à parte",
  "Se for o seu caso, some esse valor à parte, do lado do que você recebeu. "
  "Ele não é catálogo, mas é uso.")
I("Jogos que somem", "o acesso é temporário",
  "Segundo: jogo de catálogo pode sair. Você jogou, mas não é seu. Comprar dá "
  "posse, assinar dá acesso.")
I("Isso não muda a conta", "muda o que ela significa",
  "Isso não muda o cálculo, muda a leitura dele. Se para você importa manter, "
  "o mesmo número pesa diferente.")
I("Descontos e pacotes", "verifique",
  "Terceiro: se você pagou anual ou pegou pacote com desconto, use o valor "
  "real cobrado, não a soma dos meses cheios.")
I("O ano que vem", "não é este",
  "Quarto: essa é a conta do ano que passou. O próximo depende do que você vai "
  "jogar, e isso ninguém sabe hoje.")
I("Então serve pra quê", "pra decidir a renovação",
  "E é justamente por isso que ela serve: o ano que passou é a melhor "
  "estimativa que existe do seu próprio comportamento.")

# -------------------------------------------------------------------- cap 6
T("O caso que engana", "o catálogo grande",
  "Tem um caso que engana quase todo mundo, e vale um capítulo.",
  cap="O caso que engana")
I("A sensação", "tenho centenas de jogos",
  "A sensação de ter centenas de jogos disponíveis é real, e ela é o produto "
  "principal do serviço.")
I("Mas o número", "conta só o que abriu",
  "Só que a conta não paga sensação. Ela conta o que você abriu.")
I("O teste", "quantos você jogou de verdade",
  "Faça o teste: olhe sua lista e conte quantos você realmente jogou no ano. "
  "Costuma ser um número menor do que a lembrança. E vale contar só os que "
  "você passou mais de uma noite jogando, porque abrir um jogo por vinte "
  "minutos e desistir não é o mesmo que ter jogado.")
I("Se der poucos", "não é derrota",
  "Se der poucos, isso não significa que você errou. Significa que o valor "
  "que você recebe é de outro tipo, e o número mostra o tamanho dele.")
I("E aí a decisão fica clara", "renovar ou comprar",
  "Com o número na mão a decisão fica simples: renovar, ou pegar essa mesma "
  "quantia e comprar os poucos jogos que você joga.")
I("As duas respostas valem", "depende do seu número",
  "As duas respostas são legítimas, e nenhuma delas é a certa em geral. A "
  "resposta certa é a que o seu número apontar. O que não vale é renovar por "
  "inércia e nunca ter olhado.")

# -------------------------------------------------------------------- cap 7
T("De um ano para vários", "aqui a escala aparece",
  "E agora o passo que muda a percepção do tamanho.",
  cap="De um ano para vários")
I("Um ano", "parece pouco",
  "A diferença de um ano costuma parecer pequena, seja ela positiva ou "
  "negativa.")
I("Multiplique", "pelos anos que você já assina",
  "Multiplique pelos anos que você já assina. É o mesmo comportamento, "
  "acumulado.")
I("E olhe pra frente", "renovação é decisão anual",
  "Depois olhe para frente: a renovação é uma decisão que se repete, e o "
  "resultado se repete com ela.")
I("E cuidado com um detalhe", "o preço sobe",
  "E tem um detalhe que passa batido: o valor da renovação costuma subir de um "
  "ano para o outro. Se você multiplicar usando o preço antigo, subestima.")
I("Compare com algo", "que você conhece",
  "Para sentir o tamanho, compare com algo que você conhece. Com o preço de um "
  "jogo novo, por exemplo. Se o acumulado de vários anos equivale a três ou "
  "quatro jogos que você teria comprado e guardado, isso diz uma coisa. Se "
  "equivale a vinte jogos que você nunca teria comprado, diz outra bem "
  "diferente.")
I("O bom da conta anual", "dá pra mudar",
  "O lado bom é que essa decisão volta todo ano, e volta inteira. Uma conta "
  "ruim de um ano não obriga o ano seguinte, e uma conta boa também não "
  "garante que o próximo será igual.")

# -------------------------------------------------------------------- cap 8
T("O que fazer hoje", "três passos",
  "Fechamos com o que dá pra fazer hoje, em três passos.",
  cap="O que fazer hoje")
L("Três passos",
  ["Liste o que jogou", "Some os preços", "Subtraia o que pagou"],
  "Primeiro: liste os jogos do catálogo que você jogou no ano. Segundo: some "
  "os preços deles. Terceiro: subtraia o que você pagou.")
I("O primeiro passo", "é o mais revelador",
  "O primeiro passo já é o mais revelador, porque quase sempre a lista é "
  "menor do que a memória.")
I("O terceiro", "leva dois minutos",
  "O terceiro é uma subtração no celular. A conta inteira leva menos tempo do "
  "que uma partida.")
I("Anote com a data", "você vai querer depois",
  "Anote o resultado com a data. Na próxima renovação você vai querer comparar "
  "com o ano anterior.")
I("E refaça no ano que vem", "mesma conta",
  "E refaça no ano que vem. Os números mudam, a operação não.")
I("Uma coisa importante", "isso não é conselho",
  "Deixando claro: nada aqui é recomendação de serviço nem conselho "
  "financeiro. É um jeito de calcular.")
C("Nível do Jogo", "faça a conta hoje",
  "Se você chegou até aqui, faça essa conta hoje com a sua própria conta. E "
  "escreve nos comentários só a diferença que deu.")


# =============================== O SHORT ====================================
# Veredito `canal frio` com regra de `suspenso`: o melhor material vai no
# short. Ele entrega a conta inteira, nao a manchete.
SHORT = [
    {"layout": "titulo", "kicker": "Sua assinatura de jogos", "sub": "vale pra você?",
     "nar": "A assinatura de jogos sai mais barata na média. A pergunta é se "
            "sai pra você.", "sem_cap": True},
    {"layout": "item", "kicker": "Liste", "preco": "o que você jogou no ano",
     "nar": "Abra seu histórico e liste os jogos do catálogo que você "
            "realmente jogou nos últimos doze meses.", "sem_cap": True},
    {"layout": "item", "kicker": "Some", "preco": "o preço de cada um",
     "nar": "Ao lado de cada um, o preço dele hoje na loja. Some a coluna: "
            "isso é o que você recebeu.", "sem_cap": True},
    {"layout": "item", "kicker": "Subtraia", "preco": "o que você pagou",
     "nar": "Subtraia o que você pagou de assinatura no mesmo período. O sinal "
            "do resultado responde tudo.", "sem_cap": True},
    {"layout": "cta", "kicker": "Nível do Jogo", "sub": "onde achar os números",
     "nar": "Onde achar cada número e o que essa conta não pega, no vídeo "
            "completo aqui embaixo.", "sem_cap": True},
]

THUMB = {"l1": "Assinar", "l2": "ou comprar"}

COPY = """# Assinatura de jogos: a conta com os SEUS jogos

## TITULO
Se Você Tivesse Comprado em Vez de Assinar, Quanto Teria Gastado no Ano?

## DESCRICAO
Tem uma cobrança que entra na sua fatura todo mês, ou uma vez por ano, e que você renova sem pensar. A promessa é sempre a mesma: sai mais barato do que comprar — e na maioria das vezes ela até é verdadeira. Só que essa frase vale para quem joga muita coisa do catálogo. A pergunta que interessa é se ela vale para VOCÊ, com o que você jogou de verdade. Ninguém faz essa conta por você: o serviço não tem interesse, e você nunca teve os dois números lado a lado. Mas os dois existem, e os dois são seus.

A CONTA (uma soma e uma subtração)

Liste os jogos do catálogo que você abriu nos últimos doze meses — seu histórico de atividade mostra isso. Ao lado de cada um, anote o preço dele HOJE na loja: é o que você teria gasto comprando. Some essa coluna; o resultado é quanto de jogo você efetivamente consumiu, em reais. Agora some tudo o que você pagou de assinatura nos MESMOS doze meses, inclusive os meses em que quase não abriu o console — você pagou por eles do mesmo jeito. Subtraia o que pagou do valor que somou. Positivo: a assinatura te devolveu mais do que custou. Negativo: você pagou a mais, e o número é exatamente quanto. Funciona porque os dois lados são seus e do mesmo período — não entra média, não entra catálogo, não entra promessa.

ONDE ACHAR: o que você pagou está no histórico de compras da conta ou na fatura do cartão (use o valor de cada cobrança, não o preço anunciado hoje — renovação e promoção de entrada são valores diferentes). O que você jogou está no histórico de atividade, e se aparecer o tempo jogado, use como filtro: vinte minutos e largou não é valor recebido. O preço de cada jogo, na própria loja; se estiver em promoção, use o preço cheio, porque promoção é sorte de data.

O QUE A CONTA NÃO PEGA: o online multijogador, quando vem no mesmo pacote (some à parte, do lado do que você recebeu); o fato de que jogo de catálogo pode sair — comprar dá posse, assinar dá acesso, e isso não muda o cálculo mas muda a leitura dele; pacotes anuais com desconto (use o valor real cobrado); e o ano que vem, que depende do que você vai jogar. É a conta do ano que passou — e é justamente por isso que serve, porque o ano que passou é a melhor estimativa que existe do seu próprio comportamento.

Nada aqui é recomendação de serviço nem conselho financeiro. É um jeito de calcular.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Faz essa conta com a tua própria assinatura e escreve aqui só um número: a diferença em reais, com o sinal. Sem nome de serviço, sem lista de jogos, só a diferença. Quero ver o quanto esses números se espalham entre quem assina a mesma coisa.

## HASHTAGS
#Games #FinançasPessoais #NívelDoJogo

## TAGS
assinatura de jogos, vale a pena assinar, catalogo de jogos, historico de jogos, quanto gasto com games, comprar ou assinar, renovacao de assinatura, orcamento gamer, preco de jogos, biblioteca de jogos, custo por jogo, financas pessoais, gastos com games, assinatura anual, decisao de renovacao

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de assinatura, nao cita preco de jogo, nao cita catalogo, nao cita nome de servico e nao compara servicos entre si. Todos os numeros da conta sao do proprio espectador: o que ele pagou sai do historico de compras ou da fatura do cartao dele, e o preco dos jogos sai da loja no dia em que ele abrir — e sao os jogos que ELE jogou, tirados do historico de atividade dele. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa de qual servico ele assina. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer preco de mensalidade ou de jogo. Esses valores mudam por regiao, por promocao e por data de renovacao, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao diz que assinatura e boa ou ruim — as duas respostas sao legitimas e dependem do numero de cada um —, nao recomenda servico, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/nivel-do-jogo-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "nivel-do-jogo",
    "pacote": "nivel-do-jogo-008",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1B4332", "c1": "#D64570", "c2": "#F2B134", "bg": "#F4F1EA"},
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
    grava(SPEC, "fabrica/specs/nivel-do-jogo-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
