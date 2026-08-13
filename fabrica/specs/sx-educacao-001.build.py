#!/usr/bin/env python3
"""Monta a spec sx-canal-001. Escrita como codigo para os capitulos e os
`sem_cap` sairem certos por construcao, e nao a mao em 80 objetos JSON."""
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


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ---------------------------------------------------------------- cap 1
T("A conta que cresce sozinha", "e ninguem confere",
  "A licenca do Power BI e cobrada por pessoa, todo mes, e ninguem na empresa "
  "recebe um aviso quando ela cresce. Ela so aparece na fatura.",
  cap="A conta que ninguem confere")
I("O padrao", "todo mundo ganha licenca",
  "O que acontece na maioria das empresas e simples. Alguem pede acesso ao "
  "painel, o time de tecnologia compra mais uma licenca, e ninguem volta para "
  "conferir se ela ainda e usada.")
I("Seis meses depois", "a lista so cresceu",
  "Seis meses depois a lista tem nomes de gente que mudou de area, de gente "
  "que saiu, e de gente que abre o painel duas vezes por ano.")
I("E o reajuste", "primeiro em quase dez anos",
  "E em dois mil e vinte e cinco a Microsoft reajustou essas licencas pela "
  "primeira vez em quase dez anos. Quem nao mexeu na lista sentiu o aumento "
  "em cima de um numero que ja estava inflado.")
I("Quanto pesa", "some por doze meses",
  "E reajuste em licenca mensal nao se sente no mes. Se sente no ano, "
  "porque ele multiplica por doze antes de aparecer no orcamento.")
T("Este video", "a planilha, coluna por coluna",
  "Entao a pergunta deste video nao e quanto custa a licenca. E quanto custa "
  "a SUA, com os seus nomes, e quantos deles nao precisavam existir.")
L("O que a gente monta", ["As tres licencas", "As colunas da planilha",
                          "A formula que decide", "O erro mais caro",
                          "Quando a capacidade compensa"],
  "A gente monta uma planilha do zero. Cinco partes: as tres licencas, as "
  "colunas, a formula que decide quem precisa de qual, o erro mais caro, e "
  "quando vale trocar o modelo inteiro.")
I("Sem instalar nada", "Excel que voce ja tem",
  "Nao precisa instalar nada. Tudo isso e Excel comum, com funcoes que "
  "existem ha anos. Nenhuma delas e avancada.")
I("E antes de comecar", "os precos sao entrada, nao verdade",
  "Um aviso que vale o video inteiro. Os precos mudam e variam por contrato, "
  "entao a planilha nunca traz preco escrito dentro da formula. O preco e "
  "sempre uma celula que voce preenche:")

# ---------------------------------------------------------------- cap 2
T("As tres licencas", "e o que cada uma permite",
  "Comeca entendendo o que voce esta comprando. Sao tres formas de pagar, e "
  "elas nao servem para a mesma coisa.",
  cap="As tres licencas, sem jargao")
I("Gratuita", "voce cria, ninguem ve",
  "A primeira e a gratuita. Voce cria relatorio, conecta dados e monta o "
  "painel. O que voce nao faz e compartilhar com outra pessoa.")
I("Por usuario", "criar e compartilhar",
  "A segunda e a licenca por usuario. Ela libera o compartilhamento. E aqui "
  "mora a confusao mais cara do Power BI.")
I("A confusao", "quem LE tambem paga",
  "Nesse modelo, quem le o painel tambem precisa de licenca. Nao basta o "
  "analista ter. O gerente que so abre e olha tambem consome uma.")
I("Como saber a sua", "portal de administracao",
  "Para descobrir qual dessas voce paga hoje, olhe o portal de administracao "
  "do Microsoft trezentos e sessenta e cinco. Nao pergunte, confira.")
I("A terceira", "capacidade, nao pessoa",
  "A terceira e diferente. Voce nao paga por pessoa, paga por uma capacidade "
  "de processamento reservada, e quem so le passa a ler sem licenca propria.")
I("Uma pergunta antes", "voce compartilha com quantos?",
  "E antes de escolher, responda uma coisa. Com quantas pessoas voce "
  "compartilha painel hoje? Se voce nao sabe de cabeca, ja e sinal.")
B("Como o custo cresce", ["Por usuario", "Capacidade"], [100, 45],
  "A diferenca de formato importa mais que o preco. Por usuario, o custo "
  "cresce junto com o numero de pessoas. Por capacidade, ele e fixo e nao "
  "olha quantas pessoas leem.")
I("Entao existe um ponto", "onde os dois se cruzam",
  "O que significa que existe um ponto de cruzamento. Abaixo dele, pagar por "
  "pessoa sai mais barato. Acima, sai mais caro, e a diferenca so aumenta.")
I("Achar esse ponto", "e o objetivo da planilha",
  "Achar esse ponto para a sua empresa e exatamente o que a planilha faz. E "
  "ela precisa de menos dados do que voce imagina.")
T("Ponte", "so quatro informacoes",
  "Na verdade a planilha inteira roda com quatro informacoes. Quais sao elas?")

# ---------------------------------------------------------------- cap 3
T("As colunas", "quatro, e mais nada",
  "Abra uma aba nova e chame de Pessoas. Vamos precisar de quatro colunas, e "
  "nenhuma delas e dificil de conseguir.",
  cap="A planilha: as colunas")
L("Aba Pessoas", ["Nome", "Area", "Papel", "Ultimo acesso"],
  "Nome, area, papel, e ultimo acesso. Nome e area voce ja tem. Papel e "
  "ultimo acesso sao os dois que fazem o trabalho.")
I("Papel", "so tres valores",
  "A coluna papel aceita so tres valores. Cria, edita, ou apenas le. Sem "
  "meio-termo e sem texto livre, senao a formula nao consegue contar.")
I("Como travar", "validacao de dados",
  "Para garantir isso, use validacao de dados na coluna. Uma lista com os "
  "tres valores, e o Excel passa a recusar qualquer outra coisa digitada "
  "ali.")
I("Ultimo acesso", "a data, nao a impressao",
  "A coluna ultimo acesso e uma data. Ela vem do relatorio de uso do proprio "
  "Power BI, e nao da sua lembranca de quem usa o painel.")
I("De onde vem", "exporte, nao estime",
  "Esse relatorio sai do proprio Power BI, na area de administracao. Exporte "
  "para Excel e cole na aba. Nunca preencha de cabeca.")
I("Se nao tiver acesso", "peca uma vez so",
  "Se voce nao tem acesso a essa area, peca ao administrador. E um pedido "
  "unico, e ele destrava a planilha inteira.")
I("Por que ela decide", "aqui mora a economia",
  "Essa coluna e a que mais economiza dinheiro. Ela transforma uma discussao "
  "de opiniao numa contagem, e contagem ninguem discute.")
T("Segunda aba", "os precos, isolados",
  "Agora uma segunda aba, chamada Precos. Ela existe por um motivo de "
  "manutencao, nao de organizacao.")
L("Aba Precos", ["Licenca por usuario", "Licenca premium por usuario",
                 "Capacidade mensal", "Cambio"],
  "Quatro celulas. O valor da licenca por usuario, o da premium por usuario, "
  "o da capacidade mensal, e a taxa de cambio se a sua cobranca vier em "
  "dolar.")
I("A regra de ouro", "nenhum preco na formula",
  "A regra de ouro e essa: nenhum preco escrito dentro de formula. Se o "
  "valor muda, voce troca uma celula e a planilha inteira se atualiza "
  "sozinha.")
I("Se voce ignorar", "vira arqueologia",
  "Quem ignora isso descobre o custo seis meses depois, quando precisa "
  "cacar precos escondidos dentro de vinte formulas diferentes.")
I("O bloqueio", "proteja a aba",
  "Vale proteger essa aba com senha e liberar so as quatro celulas. Nao e "
  "desconfianca. E que planilha compartilhada acumula edicao acidental.")
T("Ponte", "agora a conta",
  "Com as duas abas prontas, falta a parte que de fato decide alguma coisa:")

# ---------------------------------------------------------------- cap 4
T("A formula", "quem precisa e quem nao",
  "A primeira conta responde uma pergunta so. Quantas licencas voce esta "
  "pagando sem necessidade?",
  cap="A formula que decide")
I("A funcao", "CONT.SES, nada alem",
  "A funcao e CONT.SES. Ela conta linhas que atendem varias condicoes ao "
  "mesmo tempo, e e a unica funcao nova que este video pede.")
I("Primeira condicao", "papel igual a apenas le",
  "A primeira condicao e o papel igual a apenas le. Isso separa quem consome "
  "de quem produz.")
I("Segunda condicao", "sem acesso ha noventa dias",
  "A segunda e o ultimo acesso anterior a noventa dias atras. Para isso use "
  "HOJE menos noventa, dentro da propria formula, para o corte andar sozinho "
  "todo dia.")
I("O resultado", "licencas dormindo",
  "O resultado e o numero de licencas que estao sendo pagas por gente que so "
  "leria, e que nem isso fez no ultimo trimestre.")
I("Multiplique", "e voce tem o desperdicio",
  "Multiplique esse numero pelo valor da licenca, la da aba Precos. Esse e o "
  "seu desperdicio mensal, e ele costuma surpreender.")
I("Cuidado com a data vazia", "celula em branco engana",
  "Um detalhe que estraga a conta: quem nunca acessou costuma vir com a "
  "celula vazia, e celula vazia nao entra na comparacao de data.")
I("O conserto", "trate vazio como nunca",
  "O conserto e tratar vazio como nunca acessou, e contar essas linhas "
  "separadamente. Elas sao as licencas mais desperdicadas de todas.")
I("Por que noventa", "e nao trinta",
  "Noventa dias e proposital. Trinta dias pega ferias e afastamento, e voce "
  "acaba cortando acesso de gente que vai voltar a usar na semana seguinte.")
L("Tres numeros que saem", ["Licencas ativas", "Licencas dormindo",
                            "Custo por area"],
  "Da mesma aba saem mais dois numeros. Licencas ativas, licencas dormindo, "
  "e o custo por area quando voce usa SOMASES em vez de CONT.SES.")
I("A diferenca das duas", "contar contra somar",
  "A diferenca entre elas e simples. CONT.SES conta linhas; SOMASES soma "
  "valores dessas linhas. Uma da quantidade, a outra da dinheiro.")
I("Custo por area", "aqui a conversa muda",
  "O custo por area e o que muda a conversa dentro da empresa. Ele para de "
  "ser um problema de tecnologia e vira um numero de cada diretoria.")
T("Ponte", "mas tem um erro maior",
  "So que existe um erro que custa mais caro que todas as licencas dormindo "
  "somadas. Qual?")

# ---------------------------------------------------------------- cap 5
T("O erro mais caro", "licenca para quem so le",
  "O erro mais caro nao e licenca esquecida. E dar licenca paga para muita "
  "gente que so precisa olhar.",
  cap="O erro que dobra a conta")
I("O caminho natural", "cada pedido, uma licenca",
  "Ele acontece naturalmente. Cada pedido de acesso vira uma licenca, e "
  "ninguem para para perguntar quantos pedidos ja foram atendidos assim.")
I("Cinquenta leitores", "cinquenta licencas",
  "Pense numa area com cinquenta pessoas que so abrem o painel e olham. "
  "Isso vira cinquenta licencas pagas. Todo mes, para gente que nunca "
  "criou nada.")
I("E cresce sem pedir", "cada contratacao entra na conta",
  "Pior: essa conta cresce sozinha. Cada pessoa nova que entra na area vira "
  "mais uma licenca, sem ninguem decidir nada.")
I("A alternativa", "a mesma leitura, sem licenca",
  "No modelo de capacidade, essas mesmas cinquenta pessoas leem sem licenca "
  "propria. Voce paga a capacidade, e a leitura deixa de ser cobrada por "
  "cabeca.")
I("Entao a pergunta muda", "quantos LEEM, nao quantos usam",
  "Entao a pergunta certa nao e quantas pessoas usam o Power BI. E quantas "
  "delas apenas leem.")
I("Na planilha", "voce ja tem esse numero",
  "E esse numero voce ja tem. E a contagem de papel igual a apenas le, sem "
  "nenhum filtro de data.")
I("Cuidado com o atalho", "capacidade nao e so preco",
  "Um cuidado antes de correr para a capacidade. Ela tambem muda como o dado "
  "e processado e como a area de tecnologia administra o ambiente.")
I("Ou seja", "a decisao nao e so da planilha",
  "Ou seja, a planilha diz quando vale a pena olhar. A decisao final passa "
  "por quem cuida da infraestrutura.")
T("Ponte", "entao quando vale?",
  "O que deixa uma pergunta em aberto, e ela tem resposta numerica:")

# ---------------------------------------------------------------- cap 6
T("O ponto de virada", "uma divisao, so isso",
  "O calculo do ponto de virada e uma divisao. Custo mensal da capacidade "
  "dividido pelo custo de uma licenca por usuario.",
  cap="Quando a capacidade compensa")
I("O que sai", "um numero de pessoas",
  "O que sai e um numero de pessoas. Acima dele, a capacidade tende a sair "
  "mais barata. Abaixo, a licenca por pessoa ganha.")
I("Um exemplo do formato", "sem numero de contrato",
  "Um exemplo do formato, com valores inventados so para mostrar a conta. "
  "Se a capacidade custa mil e a licenca custa vinte, o ponto fica em "
  "cinquenta pessoas.")
I("Compare com o seu", "leitores, nao usuarios",
  "Compare esse numero com a sua contagem de leitores. Se a sua contagem for "
  "maior, voce esta pagando a mais todo mes desde que passou desse ponto.")
I("E ele se move", "para os dois lados",
  "E o ponto se move. Reajuste de licenca empurra ele para baixo, o que faz "
  "a capacidade compensar com menos gente do que compensava antes.")
I("Se a cobranca vier em dolar", "o cambio entra na conta",
  "E se a sua cobranca vier em dolar, o cambio mexe no ponto de virada sem "
  "que nenhum preco tenha mudado. Por isso ele e uma celula tambem.")
I("Por isso a data", "carimbe a planilha",
  "Por isso carimbe a data em que voce preencheu os precos. Sem a data, "
  "daqui a um ano ninguem sabe se aquele numero ainda vale.")
L("Tres numeros para revisar", ["Precos", "Ultimo acesso", "Papel de cada um"],
  "Tres coisas envelhecem nessa planilha. Os precos, a coluna de ultimo "
  "acesso, e o papel de cada pessoa quando ela muda de area.")
I("Com que frequencia", "trimestral basta",
  "Uma revisao por trimestre basta. Mensal vira burocracia e ninguem "
  "mantem; anual deixa passar tres meses de licenca dormindo.")
I("O ganho real", "nao e so o dinheiro",
  "E o ganho maior nem e o dinheiro. E parar de discutir acesso por opiniao "
  "e passar a discutir por contagem.")
T("Ponte", "para nao morrer na gaveta",
  "Falta so a parte que decide se essa planilha vai durar ou virar mais um "
  "arquivo esquecido:")

# ---------------------------------------------------------------- cap 7
T("Manter viva", "tres habitos",
  "Uma planilha dessas morre por falta de rotina, nunca por falta de "
  "formula. Tres habitos resolvem.",
  cap="Como manter a planilha viva")
I("Primeiro", "a fonte, sempre a mesma",
  "Primeiro: o ultimo acesso vem sempre do relatorio de uso, sempre exportado "
  "do mesmo lugar. Fonte que muda de mes para mes destroi a comparacao.")
I("Segundo", "uma aba de historico",
  "Segundo: guarde uma aba de historico com o total de cada mes. Uma linha "
  "por mes, e em um ano voce enxerga a tendencia em vez de um retrato.")
I("Terceiro", "um dono, com nome",
  "Terceiro: a planilha precisa de um dono com nome. Planilha de todo mundo "
  "e planilha de ninguem, e essa some em dois trimestres.")
L("Recapitulando", ["Quatro colunas", "Precos isolados",
                    "CONT.SES com HOJE menos noventa", "Leitores contra o ponto"],
  "Recapitulando o que voce monta. Quatro colunas na aba Pessoas, os precos "
  "isolados numa aba propria, CONT.SES com HOJE menos noventa, e a contagem "
  "de leitores comparada ao ponto de virada.")
I("A parte que quase ninguem faz", "a coluna de papel",
  "A parte que quase ninguem faz e a coluna papel. Sem ela a planilha vira "
  "uma lista de nomes, e lista de nomes nao decide nada.")
I("O que nao fazer", "cortar acesso sem avisar",
  "Uma coisa a nao fazer: cortar acesso de ninguem so porque a formula "
  "apontou. Avise a area primeiro, e deixe a pessoa dizer se ainda precisa.")
I("Senao", "a planilha vira inimiga",
  "Senao a planilha deixa de ser ferramenta e vira motivo de briga. E ai "
  "ninguem mais atualiza a coluna de papel.")
I("Se voce so fizer uma coisa", "conte os leitores",
  "Se voce so fizer uma coisa depois deste video, conte quantas pessoas "
  "apenas leem os seus paineis. Esse numero sozinho ja muda a conversa.")
I("E leva minutos", "nao um projeto",
  "E leva minutos, nao um projeto. A planilha inteira cabe numa manha, e a "
  "primeira contagem cabe num cafe.")
I("E documente a decisao", "uma linha basta",
  "Quando decidir mudar ou ficar, escreva uma linha na propria planilha "
  "dizendo por que. Daqui a um ano, ninguem vai lembrar do motivo.")
C("SX Educacao", "Excel, dados e decisao",
  "Se voce montou a planilha, escreve nos comentarios quantos leitores voce "
  "achou. Estou juntando esses numeros para o proximo video.")
C("SX Educacao", "Excel, dados e decisao",
  "E se voce quer a proxima planilha sobre outro custo escondido, diz qual. "
  "A mais pedida sai primeiro.")

SHORT = [
    {"layout": "titulo", "kicker": "Sua conta do Power BI", "sub": "esta inflada",
     "nar": "A sua conta do Power BI provavelmente esta inflada. E da para "
            "provar com uma planilha de quatro colunas.", "sem_cap": True},
    {"layout": "item", "kicker": "O erro", "preco": "quem so LE tambem paga",
     "nar": "No modelo por usuario, quem so le o painel tambem consome "
            "licenca. Cinquenta leitores viram cinquenta licencas.", "sem_cap": True},
    {"layout": "item", "kicker": "A formula", "preco": "CONT.SES + HOJE menos noventa",
     "nar": "Uma funcao resolve. CONT.SES com papel igual a apenas le, e "
            "ultimo acesso anterior a noventa dias atras.", "sem_cap": True},
    {"layout": "item", "kicker": "O que sai", "preco": "licencas dormindo",
     "nar": "O que sai e o numero de licencas pagas por gente que nem "
            "abriu o painel no ultimo trimestre.", "sem_cap": True},
    {"layout": "cta", "kicker": "SX Educacao", "sub": "a planilha completa",
     "nar": "A planilha inteira, coluna por coluna, esta no video longo. "
            "Assiste agora.", "sem_cap": True},
]

def _copy_existente():
    """Le a copy do .json ao lado, se ele ja existir."""
    import os
    alvo = "fabrica/specs/sx-educacao-001.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500:
            return c
    return "gerado a partir dos capitulos reais apos o render"


SPEC = {
    "slug": "sx-educacao",
    "pacote": "sx-educacao-001",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Deliberate_Thought",   # canais.trilha
    "paleta": {"ink": "#10261C", "c1": "#217346", "c2": "#F2B134", "bg": "#F1F7F4"},
    "thumb": {"l1": "LICENCAS DORMINDO", "l2": "a planilha que acha"},
    "longo": CENAS,
    "short": SHORT,
    # A copy REAL vive no .json e nao aqui: ela foi escrita depois deste
    # script. Reconstruir a partir do bilhete apaga 4.288 chars de copy pronta
    # e derruba a spec no portao — foi o que aconteceu em 14/08/2026, quando
    # rodei este build so para acrescentar o campo `trilha`.
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/sx-educacao-001.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    chars = sum(len(c["nar"]) for c in CENAS)
    TAXA = 14.30
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {chars} | estimativa: {(chars/TAXA + 0.5*len(CENAS))/60:.1f} min")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
