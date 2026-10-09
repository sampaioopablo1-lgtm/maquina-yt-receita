"""labtreinamento-s012 — a data que obriga nao e a do calendario.

ALAVANCA desta rodada: o ESQUELETO DE DEZ CENAS, que e a regra de forma vigente
para short solto (experimento 40), aplicada agora tambem no labtreinamento.
NUMERO DE PARTIDA: no labtreinamento o braco de dez cenas tem n=0; as quatro
pecas de tratamento novo do canal (s008 a s011) sao de CINCO cenas.
**E ESTA PECA NAO ENTRA NO BRACO DO 682, de proposito** — o 682 le as pecas de
cinco cenas do tratamento novo, e misturar dez cenas ali destruiria a leitura
que esta a horas de ficar pronta.

O QUE DEU CERTO: o `kolejny-poziom-s017` subiu com dez cenas e 41,83 s reais
(+1,0% sobre o estimado, no piso polones), e o braco de dez cenas chegou a n=3.

O QUE NAO DEU, e e o achado desta rodada, sobre o INSTRUMENTO: o piso lido de
`metricas` MENTE para id que nao entrou na coleta recente. Quatro pecas antigas
do labtreinamento liam 0, 23, 32 e 49 em `metricas` e liam **41, 171, 49 e 64**
ao vivo na mesma hora — o `s007`, que o docstring do `s010` citava com 147, lia
ZERO na tabela. Isso retira a base de varias comparacoes que eu fiz hoje neste
canal, inclusive a frase "o labtreinamento faz piso ~42 contra 218 a 462 dos
outros": com numero fresco a MEDIANA do tratamento antigo aqui e **62**, e a
faixa e 40 a 214. E a regra que falhou e uma que esta escrita na rotina:
COLETE ANTES DE LER.

O QUE VOU MUDAR: o esqueleto, e nada mais. Mesma voz, mesma forma de titulo do
BR, mesmo pedido de inscricao no CTA.

DE ONDE SAI: longo `KRUERlNPzDw` (a planilha de transicao da norma de
qualidade), capitulos "A data que ja esta marcada", "Aba Cronograma: contar de
tras para frente" e "Quatro erros que saem caros". **Origem SEM spec local** —
pacote anterior a convencao atual, e os capitulos sairam da DESCRICAO PUBLICADA
pela `videos.list`, como a regra (h) manda. Foi a segunda vez hoje.

FAMILIA DIFERENTE das duas pecas de hoje no canal, como a regra (f) exige: o
`s010` era ORDEM (estudo antes do levantamento) e o `s011` era LIMIAR (a faixa
que separa alto de medio). Esta e **ANCORA** — a entrada errada nao e a ordem
nem o corte, e o PONTO DE REFERENCIA: a pessoa ancora o plano no prazo publico
quando a data que a obriga e a da propria auditoria de transicao, e quem a
define e o organismo certificador. O short original do pacote faz as abas da
planilha e PARA ali.

TITULO EM ENDERECO DIRETO, a forma do BR/26 (pergunta pura e sinal polones).
FEED BR NAO RELIDO nesta rodada — lido as 00:4x, dezesseis horas, muito fora da
janela de quatro horas e meia do 623, e vai dito que nao foi relido.

IDENTIDADE: faixa ATUAL do canal `{ink #22333B, c1 #A4243B, c2 #D8973C,
bg #F2F2EF}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a data de
# publicacao da edicao nova, nao cita o fim do periodo de transicao, nao cita
# quantos anos ele dura, nao cita numero de abas, de colunas, de marcos nem de
# linhas, e nao cita faixa de nota. Conferido A MAO campo por campo, porque o
# portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA, e com forca aqui: a descricao do longo tem "16 de setembro
# de 2026" e "setembro de 2029" — datas de vigencia, exatamente a classe que a
# regra manda deixar fora. E tem mais: o proprio longo diz que **os cortes de
# faixa sao criterio da empresa**, e a regra (g) tem caso especial para isso —
# numero que o longo chama de ESCOLHA nao entra de jeito nenhum, porque repetir
# escolha como norma e transformar a nossa invencao em exigencia.
#
# O QUE NAO ENVELHECE, e e o que a peca carrega: a data que obriga a empresa e a
# da AUDITORIA DE TRANSICAO dela, quem a define e o organismo certificador, e o
# cronograma se conta de tras para frente a partir dela. Isso vale qualquer que
# seja o calendario.
#
# NUMERAIS NA NARRACAO: nenhum.
#
# O QUE O VIDEO AFIRMA: que o prazo publico nao e a data da empresa; que quem
# marca a auditoria de transicao e o certificador e nao ela; que perguntar antes
# e escolher a data em vez de receber; e que acao marcada como concluida sem
# eficacia verificada reaparece na auditoria externa. Esta nos capitulos "A data
# que ja esta marcada", "Aba Cronograma" e "Quatro erros que saem caros" do longo
# `KRUERlNPzDw`.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) as duas datas e a duracao da transicao — vigencia, muda;
#   (2) as faixas de prioridade e a escala de nota — o longo diz que sao criterio
#       da empresa, logo escolha e nao norma;
#   (3) a lista do que ganha peso na edicao nova — e redacao de norma e eu nao
#       tenho duas fontes institucionais para ela nesta rodada.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Você anotou o prazo", "sub": "e ficou tranquilo", "nar": "Você anotou o prazo da norma nova e ficou tranquilo.", "sem_cap": True},
    {"layout": "item", "kicker": "O prazo público", "preco": "não é seu", "nar": "Só que esse prazo público não é a sua data de verdade.", "sem_cap": True},
    {"layout": "item", "kicker": "A sua data", "preco": "é a auditoria", "nar": "A sua data é a da sua própria auditoria de transição.", "sem_cap": True},
    {"layout": "titulo", "kicker": "E essa data", "sub": "não é você que marca", "nar": "E quem marca essa auditoria no seu ciclo não é você.", "sem_cap": True},
    {"layout": "item", "kicker": "Quem define", "preco": "o certificador", "nar": "É o organismo certificador que define isso.", "sem_cap": True},
    {"layout": "item", "kicker": "Então", "preco": "pergunte antes", "nar": "Então quem pergunta antes escolhe, e quem espera recebe.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Por isso", "sub": "conte de trás para frente", "nar": "Por isso o cronograma inteiro conta de trás para frente.", "sem_cap": True},
    {"layout": "item", "kicker": "Parta dela", "preco": "não do calendário", "nar": "Parta da sua auditoria, e nunca do calendário público.", "sem_cap": True},
    {"layout": "item", "kicker": "E cada ação", "preco": "eficácia verificada", "nar": "E cada ação só fecha com a eficácia verificada.", "sem_cap": True},
    {"layout": "cta", "kicker": "Inscreva-se", "sub": "para a próxima", "nar": "Pergunte essa data ao certificador hoje. Inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "Sua data", "l2": "é outra"}

COPY = """# labtreinamento-s012

## TITULO
A Data Que Obriga Você Na Transição Da Norma Não É A Do Calendário — É A Da Sua Auditoria

## TITULO SHORT
A data que obriga você é outra

## DESCRICAO
Quase todo mundo anota o prazo público da transição e sai tranquilo. O problema é que esse prazo não é a data que obriga a sua empresa.

A data que obriga é a da **sua auditoria de transição** — e ela não é escolhida por você. Quem a define é o organismo certificador, dentro do ciclo de auditorias que a sua empresa já tem. Dois concorrentes com o mesmo certificado podem ser cobrados em momentos bem diferentes, e nenhum dos dois decidiu isso.

Daí sai a única pergunta que organiza o resto: **em qual auditoria do meu ciclo a versão nova vai ser cobrada?** Quem faz essa pergunta cedo escolhe a data; quem espera recebe a data — e descobre o prazo real quando já não dá para reorganizar nada.

Com a resposta na mão, o cronograma se conta de trás para frente, partindo dessa auditoria e não do fim do período de transição. É o mesmo plano, na ordem que cabe no tempo que existe de verdade.

E tem um erro silencioso que vale mais que todos os outros: marcar ação como concluída sem verificar eficácia. A planilha fica verde, a reunião fica curta, e a não conformidade aparece na auditoria externa. Verificar eficácia é perguntar se resolveu — não se foi feito.

Este short não traz nenhuma data, nenhuma duração de transição e nenhuma faixa de nota, e isso é deliberado: datas de vigência mudam, e o próprio vídeo completo diz que as faixas de prioridade são critério da empresa, não da norma. O que não envelhece é a regra: a sua data é a da sua auditoria, e a pergunta é com o certificador.

A planilha completa — diagnóstico, lacunas, plano e cronograma, montada do zero — está no vídeo completo no canal.

## COMENTARIO FIXADO
O erro aqui não é de prazo, é de âncora: as pessoas penduram o plano no prazo público e esquecem que quem as cobra é a auditoria do próprio ciclo, marcada pelo organismo certificador. Por isso a primeira tarefa da transição não é preencher planilha nenhuma — é mandar um e-mail ao certificador perguntando em qual auditoria do seu ciclo a versão nova será cobrada. Com essa data você conta o cronograma de trás para frente; sem ela você está planejando contra um calendário que não é o seu. Para ser justo com quem espera: esperar não é preguiça, é não saber que a data é negociável em termos de informação, não de prazo. E o erro mais silencioso de todos: ação marcada como concluída sem eficácia verificada — a planilha fica verde e a não conformidade aparece na auditoria externa. De propósito não citei nenhuma data nem faixa de nota aqui: datas de vigência mudam e as faixas são critério da sua empresa. Quem já perguntou ao certificador, conta nos comentários só se a resposta veio rápido.

## HASHTAGS
#ISO9001 #Qualidade #LabTreinamento

## TAGS
auditoria de transicao, organismo certificador, transicao da norma, cronograma de tras para frente, verificacao de eficacia, plano de acao qualidade, diagnostico de lacunas, sistema de gestao da qualidade, nao conformidade, auditoria externa, planilha de transicao, lab treinamento, gestao da qualidade, ciclo de auditoria, prazo de transicao

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
publicacao da edicao nova, fim do periodo de transicao, duracao em anos, numero
de abas, colunas ou marcos, nem faixa de nota. Conferido a mao campo por campo.

A REGRA (g) MANDA com forca aqui: a descricao do longo traz duas datas de
vigencia, que e a classe exata que fica fora. E o caso especial da regra tambem
se aplica: o proprio longo diz que os cortes de faixa sao CRITERIO DA EMPRESA,
logo sao escolha e nao norma, e repetir escolha como norma seria transformar a
nossa invencao em exigencia.

O QUE NAO ENVELHECE, e e o que a peca carrega: a data que obriga e a da auditoria
de transicao da propria empresa, quem a define e o organismo certificador, o
cronograma se conta de tras para frente a partir dela, e acao sem eficacia
verificada reaparece na auditoria externa.

NUMERAIS NA NARRACAO: nenhum.

DESCARTADO, e vai escrito:
  (1) as duas datas e a duracao da transicao — vigencia, muda;
  (2) faixas de prioridade e escala de nota — criterio da empresa;
  (3) a lista do que ganha peso na edicao nova — redacao de norma, sem duas
      fontes institucionais nesta rodada.

## FONTES
O longo de onde este short foi extraido (KRUERlNPzDw) traz as datas e as fontes.
Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s012",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F2F2EF"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "KRUERlNPzDw",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/labtreinamento-s012.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | TOPO no pt-BR")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*0.952:.1f} a {s*0.994:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
