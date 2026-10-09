"""labtreinamento-s010 — a ordem errada: estudo antes do levantamento.

ALAVANCA desta rodada, uma coisa so: FECHAR n=3 do tratamento novo NESTE canal.
O aprendizado 682 registrou o gatilho antes de olhar o resultado, e esta peca e
o terceiro ponto que ele pediu. Nao mudo mais nada aqui de proposito — mesma
mira de duracao (topo do ALVO), mesmo pedido de inscricao no kicker do CTA,
mesma forma de titulo BR (endereco direto, nao pergunta pura). Se as 12 h as
tres pecas novas do labtreinamento continuarem baixas, o 682 manda DESFAZER o
tratamento NESTE canal e voltar a mira antiga, mudando uma coisa so.

POR QUE n=3 e necessario: com tres leituras e mediana, o tratamento novo esta
fazendo 400 e 296 no epomeno e no kolejny, e 13 e 3 no labtreinamento. Eu primeiro
atribui isso ao PERFIL da origem (conformidade corporativa, que o 651 mediu ~30x
pior) — e o proprio canal refutou: `labtreinamento-s007`, tratamento ANTIGO,
origem "CAT em Doenca Ocupacional", o MESMO perfil, fez 147 as 11,9 h. Com o
perfil preso dentro do canal, o perfil nao explica; o tratamento explica. Isso
invalidou o 681 e escreveu o 682: e uma interacao CANAL x TRATAMENTO, e eu NAO
consigo separar qual dos tres componentes (mira de duracao, CTA de inscricao,
forma do titulo) responde — por isso o passo seguinte e desfazer o pacote inteiro
neste canal e voltar a mudar UMA COISA SO.

MEDIDO nesta rodada, mediana de tres com a faixa ao lado:
  epomeno-s011   7,7 h  400 (303-406) | kolejny-s011  6,8 h  296 (256-299)
  kolejny-s010   8,9 h  234 (234-239) | epomeno-s010  9,9 h  210 (176-212)
  labtreinamento-s007 (ANTIGO) 11,9 h  147 (144-149)
  labtreinamento-s008 (NOVO)    7,5 h   13 (9-14)
  labtreinamento-s009 (NOVO)    2,9 h    3 (3)

NUMERO DE PARTIDA desta peca: 3 e 13, as duas irmas de tratamento novo; 147 e o
alvo a bater, que e o que o tratamento antigo faz no mesmo perfil.

DE ONDE SAI: longo `yrWVyqQtw00` (labtreinamento-004, a norma eletrica nova),
capitulo "Um erro de sequencia | comum e caro". O short ORIGINAL do pacote cobre
a reescrita, a data de vigencia e as tres mudancas (desenergizar antes do EPI,
arco eletrico vira exigencia, risco eletrico entra no mesmo inventario) — e PARA
ali. Nao toca na ordem de contratacao, que e uma entrada errada de dinheiro e nao
de norma: contrata-se o estudo de engenharia primeiro, o escopo vira a instalacao
inteira, e metade dela talvez nao exigisse.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F4F1EA}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a data de
# vigencia, nao cita o numero da portaria, nao cita preco de adequacao e NAO
# NOMEIA a norma (o nome dela carrega um numeral). Conferido A MAO campo por
# campo, porque o portao `narracao` conta QUANTIDADES por frase e NAO pega
# digito cru.
#
# A REGRA (g) MANDA: a data de vigencia e o numero do ato normativo envelhecem —
# um short com a data do ano passado fica errado e continua no ar. O preco nem
# existe: o proprio longo diz "quem te der um numero sem olhar esta chutando".
# A ORDEM de contratacao nao envelhece, e e ela que este short carrega.
#
# UNICO NUMERAL NA NARRACAO: "a ordem inversa" / "metade" — descrevem o
# raciocinio, nao o mundo. Uma quantidade por frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que contratar o estudo de engenharia ANTES do
# levantamento faz o escopo virar a instalacao inteira, e que a ordem que
# funciona e a inversa — levantar, descobrir onde falta, e so entao pedir
# orcamento com escopo definido. Esta no longo labtreinamento-004
# (`yrWVyqQtw00`), capitulo "Um erro de sequencia — comum e caro".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a data de vigencia — de calendario, envelhece;
#   (2) o numero do ato normativo e o nome numerado da norma;
#   (3) quanto custa a adequacao, que depende da instalacao DELE.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Você pediu o estudo", "sub": "antes de levantar",
     "nar": "Chegou a norma elétrica nova e você pediu o estudo no mesmo dia. A "
            "conta veio alta, e a ordem é o motivo.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Sem levantamento", "sub": "o escopo é tudo",
     "nar": "Quem pede orçamento sem levantamento recebe o escopo da instalação "
            "inteira. É o único escopo que o fornecedor cota sem te conhecer.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "E talvez metade", "sub": "não exigisse",
     "nar": "E talvez metade da instalação não exigisse o estudo. O fornecedor não "
            "tem como saber isso por você.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A ordem inversa", "sub": "levante primeiro",
     "nar": "A ordem que funciona é a inversa: levante, descubra onde falta, e só "
            "então peça orçamento com escopo definido.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Se inscreva", "sub": "para as próximas",
     "nar": "O preço cai porque o escopo encolheu, não porque alguém negociou. Se "
            "inscreva para as próximas, e o roteiro está no vídeo.",
     "sem_cap": True},
]

THUMB = {"l1": "Levante", "l2": "antes de cotar"}

COPY = """# labtreinamento-s010

## TITULO
Por Que Pedir o Estudo de Engenharia Antes do Levantamento Encarece a Adequação Elétrica

## TITULO SHORT
Você pediu o estudo antes de levantar

## DESCRICAO
A reação mais comum quando chega uma norma elétrica nova é também a mais cara: pedir orçamento do estudo de engenharia no mesmo dia. O gasto não aparece inflado por má-fé do fornecedor — aparece porque a sequência está trocada, e a sequência trocada só tem um escopo possível.

Funciona assim: quem pede orçamento sem levantamento recebe o escopo da instalação inteira. Não existe alternativa do outro lado. O fornecedor não conhece a sua planta, não sabe quais pontos realmente precisam de estudo, e a única cotação que ele consegue montar sem chutar é a que cobre tudo. Você recebe um número grande e correto para o escopo errado.

E talvez metade da instalação não exigisse. Essa é a parte que só o levantamento responde, e ele não é função do fornecedor: descobrir onde falta é trabalho de dentro, feito com a lista do que existe na mão.

A ordem que funciona é a inversa — levantar primeiro, descobrir onde falta, e só então pedir orçamento com escopo definido. O preço cai não porque alguém negociou melhor, mas porque o escopo encolheu para aquilo que de fato precisa. É a diferença entre comprar um estudo e comprar a tranquilidade de ter pedido orçamento.

Aqui não há data de vigência, número de portaria nem preço, e isso é deliberado: data e número são definidos por ato normativo e envelhecem, e preço de adequação depende do estado da instalação — quem te der um número sem olhar está chutando. A ordem de contratação não envelhece. O roteiro do levantamento, os prazos com fonte e o que a norma separa entre habilitado, qualificado, capacitado e autorizado estão no vídeo completo.

## COMENTARIO FIXADO
O erro aqui não é de preço, é de sequência: pedir o estudo ANTES do levantamento só tem um escopo possível, a instalação inteira — porque é o único que o fornecedor consegue cotar sem te conhecer. E talvez metade dela não exigisse. A ordem que funciona é a inversa: levante, descubra onde falta, e só então peça orçamento com escopo definido. O preço cai porque o escopo encolheu, não porque alguém negociou. E para ficar claro, porque o vídeo não é contra o estudo: onde a norma exige, o estudo é obrigatório e não há desconto nisso. O que não vale é comprá-lo antes de saber onde. Quem já cotou nas duas ordens, escreva nos comentários apenas se o escopo mudou — sem valores.

## HASHTAGS
#SegurancaDoTrabalho #RiscoEletrico #LabTreinamento

## TAGS
levantamento eletrico, estudo de engenharia, escopo definido, adequacao eletrica, orcamento de adequacao, ordem de contratacao, seguranca do trabalho, risco eletrico, norma eletrica, trabalhos energizados, lista de autorizados, labtreinamento, gestao de riscos, planejamento orcamentario, inventario de riscos

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita data de
vigencia, numero de portaria nem preco, e NAO NOMEIA a norma (o nome dela carrega
um numeral). Conferido a mao campo por campo.

A REGRA (g) MANDA: data de vigencia e numero de ato normativo envelhecem; preco
de adequacao depende da instalacao de quem assiste. A ORDEM de contratacao nao
envelhece, e e ela que este short carrega.

UNICO NUMERAL NA NARRACAO: "a ordem inversa" e "metade", que descrevem o
raciocinio.

O QUE O VIDEO AFIRMA: que pedir o estudo ANTES do levantamento faz o escopo virar
a instalacao inteira, e que a ordem que funciona e a inversa — levantar,
descobrir onde falta, e so entao pedir orcamento com escopo definido. Esta no
longo labtreinamento-004 (yrWVyqQtw00), capitulo "Um erro de sequencia — comum e
caro".

DESCARTADO, e vai escrito:
  (1) a data de vigencia, de calendario;
  (2) o numero do ato normativo e o nome numerado da norma;
  (3) quanto custa a adequacao, que depende da instalacao DELE.

## FONTES
O longo de onde este short foi extraido (labtreinamento-004, yrWVyqQtw00) traz as
fontes oficiais. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s010",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "yrWVyqQtw00",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/labtreinamento-s010.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (topo: centro pt-BR ~ -4,5%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*0.923:.1f} a {s*0.977:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
