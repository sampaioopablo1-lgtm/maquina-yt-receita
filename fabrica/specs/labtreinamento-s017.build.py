"""labtreinamento-s017 — A PRIMEIRA PECA DO FORMATO NOVO. Curta, e de dinheiro.

ESTA PECA EXECUTA AS DECISOES DE 12/10, e elas estao em `docs/decisoes-12-10.md`.
O dono deu o controle com estas palavras: *"tome decisoes importantes pra
revertermos, mudando ate o formato, estilo do canal, tipo de conteudo, etc.
Assuma o controle"*. Entao mudam TRES coisas de uma vez, de proposito, e isso vai
declarado como confundidor em vez de escondido:

  1. DURACAO: 20 a 26 s REAIS, contra os 29 a 42 de todas as 161 pecas
     anteriores. Tres fontes apontam para baixo (o nosso `mostPopular` com
     mediana de 26 s no BR, o playbook externo com picos em 13 e 60, e o fato de
     que 30-42 s ja foi testado em 161 pecas sem romper nenhuma vez — 713);
  2. CONTEUDO: dinheiro do PROPRIO espectador, nao conformidade corporativa.
     Medido no proprio canal (651): os dois unicos quase-rompimentos da historia
     da frota (1.111 e 1.133 views) sao dinheiro proprio; conformidade mede 4 a
     70. FURO DECLARADO: aqueles dois sao pacotes ADJACENTES (006/007), o que
     parece evento de distribuicao; na janela casada posterior o fator cai para
     ~2. Eu uso o fator 2, nao o 30;
  3. OS NUMEROS VOLTAM A NARRACAO. Nas pecas de conformidade eu vinha aplicando
     "zero numeral", que e MAIS ESTRITO que a regra: a 640 permite ate TRES
     quantidades por frase, por extenso. Em conteudo de dinheiro o numero E a
     entrega — tirar o numero tiraria o short.

ORIGEM: longo `bQoujWaY7Hw` (pacote `labtreinamento-008`), 58 capitulos,
"Desconto para Pagar a Vista: Divida por 90". O short ORIGINAL dele usou a
divisao por noventa e o prazo de trinta dias, e **fechou dizendo "no canal tem a
conta com outros prazos"** — ou seja, este angulo esta pre-declarado como nao
usado, pelo proprio autor, antes de qualquer resultado.

FAMILIA, a decima primeira: **PROPORCAO COM O PRAZO**. A entrada errada e
comparar dois descontos pelo TAMANHO quando o que decide e a razao entre o
desconto e os dias antecipados. Capitulos usados: "Prazos diferentes", "A regra",
"Antecipou 60 dias", "Antecipou 15 dias", "Repare" e "O que pesa".
E a entrega e contraintuitiva e verificavel na hora: **cinco por cento custou o
dobro de dez por cento**, porque o prazo era um quarto.

MIRA: `alvo_short('labtreinamento')` = **20,0 a 26,0 de duracao REAL** — a faixa
NOVA. Com o fator do Piper no pt-BR (0,821) isso pede estimativa de 24,4 a 31,7;
`estimativa_para_real(24,0)` da 29,2 e os chars por cena vieram de
`chars_por_cena`, nao da minha cabeca.

A LEITURA QUE DECIDE, declarada ANTES: **romper e UMA peca acima de 5.000 views**,
3x a melhor da historia. Dez pecas assim sem rompimento e duracao+conteudo caem
como alavanca, e o proximo suspeito e a abertura.

IDENTIDADE: faixa ATUAL do canal, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# AQUI OS NUMEROS ENTRAM, e isso e mudanca de politica declarada. Eles entram
# POR EXTENSO e no maximo tres quantidades por frase (640). Conferido frase a
# frase.
#
# E ELES NAO ENVELHECEM, que e o que a regra (g) protege: nao ha taxa, indice,
# aliquota, limite anual nem data de vigencia. Sao os numeros de um EXEMPLO
# aritmetico — dez por cento, cinco por cento, sessenta dias, quinze dias — e a
# conta que eles ilustram e a mesma em qualquer ano.
#
# O QUE EU NAO LEVEI: a taxa de antecipacao de recebiveis do banco, que o longo
# usa como comparador. ESSA muda, e e exatamente o tipo de numero que a regra (g)
# manda deixar fora. A peca manda o espectador olhar a dele.
#
# E O QUE SOBRA PARA A PROXIMA RODADA: "Quando dar desconto" com as tres
# situacoes em que vale mesmo assim, e o capitulo do "desconto padrao na tabela",
# que e a familia O PADRAO QUE NINGUEM ESCOLHEU. Quinto angulo deste longo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Cinco por cento", "sub": "custa mais que dez", "nar": "Cinco por cento pode custar mais que dez.", "sem_cap": True},
    {"layout": "item", "kicker": "Porque", "nar": "Desconto à vista é empréstimo seu.", "sem_cap": True},
    {"layout": "item", "kicker": "E o juro", "nar": "E o juro não depende do tamanho dele.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Depende", "sub": "dos dias que você antecipou", "nar": "Depende dos dias que você antecipou.", "sem_cap": True},
    {"layout": "item", "kicker": "Dez por cento", "nar": "Dez por cento por sessenta dias: cinco ao mês.", "sem_cap": True},
    {"layout": "item", "kicker": "Cinco por cento", "nar": "Cinco por cento por quinze dias: dez ao mês.", "sem_cap": True},
    {"layout": "titulo", "kicker": "O menor", "sub": "custou o dobro", "nar": "O desconto menor custou o dobro.", "sem_cap": True},
    {"layout": "item", "kicker": "Então divida", "nar": "Divida sempre o desconto pelo prazo.", "sem_cap": True},
    {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se", "nar": "Faça a conta no seu orçamento. Inscreva-se.", "sem_cap": True}
]

THUMB = {"l1": "5% custa", "l2": "o dobro"}

COPY = """# labtreinamento-s017

## TITULO
Cinco Por Cento Pode Custar O Dobro De Dez — Quem Decide É O Prazo Que Você Antecipou

## TITULO SHORT
5% custa mais que 10%

## DESCRICAO
Quando o cliente pede desconto para pagar à vista, você faz um empréstimo sem perceber — e quem paga juros é você. Isso quase todo mundo já ouviu. O que quase ninguém faz é a parte que decide o custo.

Porque o custo **não está no tamanho do desconto**. Está na relação entre ele e o número de dias que você antecipou.

Veja os dois casos, e eles são reais no dia a dia de quem vende a prazo:

- **dez por cento** de desconto para antecipar **sessenta dias** sai por cerca de **cinco por cento ao mês**;
- **cinco por cento** de desconto para antecipar **quinze dias** sai por cerca de **dez por cento ao mês**.

O desconto que parece metade do outro custou **o dobro**. E ele não aparece em lugar nenhum: desconto não gera fatura, não gera extrato e não entra na sua contabilidade como despesa financeira. Ele só aparece se você fizer a conta.

A conta é proporção, e cabe de cabeça: pegue o juro do período e passe para o mês — multiplique por trinta e divida pelos dias que você antecipou. Se antecipou trinta dias, o número já está pronto. Se antecipou sessenta, divida por dois. Se antecipou quinze, multiplique por dois.

O teste que fecha isso vale cinco minutos e é no seu próprio papel: abra o último orçamento em que você deu desconto para pagamento à vista, veja quantos dias aquilo antecipou de verdade, e faça a proporção. O número que sair é o juro que você cobrou de si mesmo.

Este short não cita a taxa de antecipação de recebíveis de nenhum banco: essa muda, e é exatamente o número que não deve morar num short. Compare com a sua, no seu aplicativo.

No vídeo completo: a conta passo a passo, por que se divide por noventa e não por cem, os três casos em que vale dar o desconto mesmo assim, e por que desconto padrão na tabela é pior que desconto negociado.

## COMENTARIO FIXADO
O detalhe que faz esse erro sobreviver é que o desconto não deixa rastro: não há fatura, não há extrato, não há linha de despesa financeira. Então o custo existe e ninguém o vê. E a parte contraintuitiva é a proporção — dois descontos de tamanhos bem diferentes podem custar a mesma coisa, ou se inverter, só pelo prazo. De propósito não coloquei aqui a taxa de antecipação de nenhum banco: essa muda, e a comparação que importa é com a sua. Conta nos comentários: no seu último orçamento com desconto à vista, quantos dias você antecipou, e quanto deu a proporção?

## HASHTAGS
#FinancasDaEmpresa #FluxoDeCaixa #LabTreinamento

## TAGS
desconto a vista, antecipacao de recebiveis, custo do desconto, juro implicito, fluxo de caixa, precificacao, orcamento, prazo de pagamento, capital de giro, financas para autonomo, financas da pequena empresa, negociacao com cliente, matematica financeira, taxa ao mes, labtreinamento

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
AQUI OS NUMEROS ENTRAM, e isso e MUDANCA DE POLITICA DECLARADA. Nas pecas de
conformidade eu vinha aplicando "zero numeral", que e mais estrito que a regra:
a 640 permite ate TRES quantidades por frase, por extenso. Em conteudo de
dinheiro o numero E a entrega — tirar o numero tiraria o short. Conferido frase a
frase, por extenso, no maximo tres por frase.

E ELES NAO ENVELHECEM, que e o que a regra (g) de fato protege: nao ha taxa,
indice, aliquota, limite anual nem data de vigencia. Sao os numeros de um EXEMPLO
aritmetico (dez por cento, cinco por cento, sessenta dias, quinze dias), e a
conta que eles ilustram e a mesma em qualquer ano.

O QUE EU NAO LEVEI: a taxa de antecipacao de recebiveis do banco, que o longo usa
como comparador. ESSA muda, e e exatamente o tipo de numero que a regra (g) manda
deixar fora de um short. A peca manda o espectador olhar a dele.

ANGULO PRE-DECLARADO PELO PROPRIO ORIGINAL: o short original do
`labtreinamento-008` usou a divisao por noventa e o prazo de trinta dias, e
fechou dizendo "no canal tem a conta com OUTROS PRAZOS". Este e esse angulo.
Capitulos usados: "Prazos diferentes", "A regra", "Antecipou 60 dias",
"Antecipou 15 dias", "Repare" e "O que pesa" do longo `bQoujWaY7Hw`.

FAMILIA: PROPORCAO COM O PRAZO — a entrada errada e comparar dois descontos pelo
TAMANHO quando o que decide e a razao entre o desconto e os dias antecipados.

ESTA PECA MUDA TRES COISAS DE UMA VEZ, e o confundidor vai declarado: duracao
(20 a 26 s REAIS contra 29 a 42 das 161 anteriores), conteudo (dinheiro proprio
contra conformidade) e politica de numero. Se ela romper, eu NAO saberei qual das
tres pesou — e isso e aceito de proposito, porque o que esta em jogo nao e medir
um efeito de 25%, e descobrir se existe rompimento. Ver
`docs/decisoes-12-10.md`.

A LEITURA DECLARADA ANTES: romper e UMA peca acima de 5.000 views, 3x a melhor
da historia da frota (1.614).

## FONTES
O longo de onde este short foi extraido (`labtreinamento-008`, `bQoujWaY7Hw`)
carrega a conta inteira. Este short NAO introduz numero novo sobre o mundo — os
numeros dele sao de um exemplo aritmetico, nao medidas do mundo — entao nao exige
fonte institucional nova.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s017",
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
    from ensaio import (duracao_estimada_short, alvo_short,
                        duracao_real_prevista, estimativa_para_real)
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/labtreinamento-s017.json")
    est = duracao_estimada_short(SHORT, SPEC["voz"])
    real = duracao_real_prevista(SHORT, SPEC["voz"], "piper")
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"FORMATO NOVO | {len(SHORT)} cenas | dinheiro proprio | bQoujWaY7Hw")
    print(f"estimado: {est:.1f}s | REAL previsto: {real:.1f}s")
    print(f"mira REAL do canal (NOVA): {lo}-{hi} | "
          f"estimativa que ela pede: {estimativa_para_real(lo, SPEC['voz']):.1f}"
          f"-{estimativa_para_real(hi, SPEC['voz']):.1f}")
    print(f"real na mira? {'SIM' if lo <= real <= hi else 'NAO'}")
    print(f"por plano: {real/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
