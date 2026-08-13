#!/usr/bin/env python3
"""A chave de estilo do canal: tudo que um roteiro precisa respeitar, num bloco.

Noventa e oito dos cento e sete longos que faltam para a meta ainda nao existem
como texto. Escrever cada um a mao custa cerca de uma hora; o gargalo da maquina
deixou de ser render e passou a ser AUTORIA.

Para um modelo rascunhar spec sem que cada uma saia com outra voz, ele precisa
receber, junto da pauta, tudo que faz um roteiro pertencer AQUELE canal. Esta e
a peca que faltava — e e a unica coisa que aproveitei do metodo que o Pablo
mandou em 13/08 (Claude + Google Flow): la a consistencia entre cenas vem de
carregar um bloco fixo em cada prompt. O nosso equivalente estava espalhado por
config/canais, pelos portoes e pelos aprendizados, e nunca reunido.

PRINCIPIO DE CONSTRUCAO, que e o que separa isto de um prompt colado a mao:
nada aqui e digitado duas vezes. Os limites vem IMPORTADOS dos portoes que os
aplicam, e o config do canal entra VERBATIM. Se alguem mudar MAX_VIRGULAS ou
reescrever o comentario de um canal, a chave muda junto. Um prompt com numero
copiado envelhece calado — e envelhecer calado e o defeito que mais custou
tempo neste repositorio.

Uso:
    python3 fabrica/estilo.py <canal> [--titulos <arquivo.json>]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

# Importados, nunca redigitados. Cada um destes numeros e aplicado por um portao;
# repeti-los aqui a mao criaria duas verdades.
from narracao import MAX_NUM_FRASE, MAX_PALAVRAS, MAX_VIRGULAS, SLOP, VAGO  # noqa: E402
from copy_md import MAX_CAP, MIN_CAP  # noqa: E402
from ensaio import MODELO_VOZ  # noqa: E402
from prontidao import (  # noqa: E402
    MIN_PALAVRAS_DESCRICAO, PISO_LONGO_S, SHORT_MAX_S, SHORT_MIN_S, TETO_LONGO_S,
)

# Alvo de duracao no meio da faixa: 13 min e o centro dos 12-15 da rotina.
# Mediana do corpus: 3.562 frases em 1.669 cenas nas 25 specs de 14/08/2026.
# Vai de 1,53 (agla-level-003) a 3,20 (nivel-do-jogo-002) — por isso e premissa
# de planejamento, e o portao conta as frases de verdade.
FRASES_POR_CENA = 2.13

ALVO_LONGO_S = 780
ALVO_SHORT_S = 37
CENAS_MIN, CENAS_MAX = 70, 90
CAPS_MIN, CAPS_MAX = 6, 8

# O unico pedaco desta chave que NAO e uma regra medida — e por isso e o mais
# importante. Os seis portoes conferem se o roteiro esta CERTO: densidade de
# numero, duracao, borda, glifo, estrutura da copy. Nenhum deles pergunta se
# alguem se importa. Um roteiro pode passar nos seis e nao mexer com ninguem.
#
# O que esta abaixo saiu de LER as dezessete specs do repositorio e comparar as
# aberturas. Metade abre com um numero; metade abre com uma pessoa numa
# situacao. As segundas sao melhores, no mesmo canal e com a mesma voz — e o
# movimento que se repete nelas nunca tinha sido escrito em lugar nenhum.
ARCO_EMOCIONAL = """7. O ARCO — a parte que nenhum portao mede.

   Os portoes conferem se o roteiro esta certo. Nenhum pergunta se alguem se
   importa. Isto aqui e o que separa os dois.

   A ABERTURA nao anuncia o assunto: poe alguem dentro de um momento.

       fraco  "Cinquenta e nove virgula tres por cento dos trabalhadores
               brasileiros estao no setor informal."
       forte  "Dia vinte e cinco, saldo zero."

       fraco  "O salario minimo subiu treze por cento."
       forte  "Teu salario subiu. E por alguns dias voce sentiu alivio."

   O numero nao some — ele entra na SEGUNDA cena, para explicar o que a
   primeira fez sentir. Abrir com estatistica gasta o unico momento em que
   o espectador ainda nao decidiu ficar.

   O MOVIMENTO CENTRAL, que e o melhor que esta maquina faz: o espectador
   chega achando que a culpa e dele, e o video mostra que e estrutural.

       "Nao e porque voce e gastador. E porque seu dinheiro nao tem ordem."
       "Essa explicacao e comoda porque fecha o assunto rapido e poe todo o
        peso numa pessoa so. Mas nao explica por que milhoes passam pelo
        mesmo, no mesmo mes, com o mesmo padrao."

   Faca esse giro cedo, no primeiro capitulo. Ele e o que compra os treze
   minutos seguintes: a pessoa para de se defender e comeca a querer entender.

   FALE COM ALGUEM. Segunda pessoa, sempre. "Quanto sobra pra voce depois de
   pagar" prende; "o rendimento medio das familias" nao.

   NOMEIE O CUSTO NA VIDA, nao na planilha. O numero sozinho e inerte; o que
   ele impede e que doi.

       inerte  "A diferenca e de trezentos euros."
       vivo    "Nao e uma diferenca de trezentos euros. E a diferenca entre
                construir alguma coisa e sobreviver."

   O RITMO carrega emocao. Frase longa para explicar, frase curta para
   assentar. Tres frases do mesmo tamanho seguidas achatam qualquer verdade.

   FECHE DEVOLVENDO CONTROLE. Depois de treze minutos mostrando um sistema
   maior que a pessoa, entregue uma coisa que ela faz sozinha esta semana, com
   o custo em tempo dito na cara: "leva cinco minutos", "cabe num cafe".
   Sem isso o video informa e desanima, e desanimado ninguem volta.

   O QUE NAO FAZER: pena, alarme, culpa e promessa. O tom e de alguem que
   respeita quem ouve — mostra a conta, nao vende susto nem salvacao."""

LAYOUTS = {
    "titulo": "kicker, sub. Abre secao. Com `cap` vira capitulo; sem, leva sem_cap.",
    "item":   "kicker, preco. Uma afirmacao com um destaque curto ao lado.",
    "lista":  "kicker, itens[]. Ate cinco itens, cada um um SINTAGMA curto.",
    "barras": "kicker, itens[], alturas[]. itens sao ROTULOS DE EIXO, nunca frases.",
    "cta":    "kicker, sub. So no fim.",
}


def _config_do_canal(canal: str) -> str:
    caminho = os.path.join(RAIZ, "config", "canais", f"{canal}.yaml")
    if not os.path.exists(caminho):
        raise SystemExit(f"canal desconhecido: {canal} (sem config/canais/{canal}.yaml)")
    return open(caminho, encoding="utf-8").read().rstrip()


def _voz_do_config(texto: str) -> str:
    for linha in texto.splitlines():
        if "voz_edge:" in linha:
            return linha.split(":", 1)[1].strip().strip('"')
    return ""


def orcamento(voz: str) -> dict:
    """Quantos caracteres cabem, pelos DOIS termos medidos da voz.

    O orcamento nao sai de uma taxa: sai de chars/R + frases*P. Escrever pelo
    numero de cenas fazia a duracao sair a esmo, mas escrever por taxa unica
    fazia pior, porque a taxa aparente da MESMA voz varia 85% conforme o
    roteiro seja de frase longa ou curta (id-ID-Gadis, 14/08/2026).

    FRASES_POR_CENA e a mediana do corpus (3.562 frases em 1.669 cenas nas 25
    specs de 14/08/2026). E premissa de planejamento, nao medicao da spec: o
    portao conta as frases de verdade. Quem escreve frase mais curta que a
    mediana gasta mais segundo por caractere e cabe menos texto — e o portao
    dira isso antes do render.
    """
    if voz not in MODELO_VOZ:
        return {"modelo": None}
    R, P = MODELO_VOZ[voz]
    cenas = 80
    frases_longo = cenas * FRASES_POR_CENA
    frases_short = 5 * FRASES_POR_CENA
    chars_longo = int((ALVO_LONGO_S - frases_longo * P) * R)
    return {
        "modelo": (R, P),
        "cenas_alvo": cenas,
        "chars_longo": chars_longo,
        "chars_por_cena": int(chars_longo / cenas),
        "chars_short": int((ALVO_SHORT_S - frases_short * P) * R),
    }


def chave(canal: str, titulos_anteriores: list[str] | None = None) -> str:
    cfg = _config_do_canal(canal)
    voz = _voz_do_config(cfg)
    orc = orcamento(voz)
    idi = "pt"  # os termos proibidos abaixo saem por idioma; pt cobre os 4 canais pt-BR
    for linha in cfg.splitlines():
        if "idioma:" in linha and "revisao" not in linha:
            idi = linha.split(":", 1)[1].strip().strip('"').split("-")[0]
            break

    L = []
    L.append(f"CHAVE DE ESTILO — {canal}")
    L.append("=" * 60)
    L.append("")
    L.append("1. O CANAL, como esta registrado. Isto vale mais que qualquer")
    L.append("   instrucao generica: sao medicoes deste canal, nao boas praticas.")
    L.append("")
    L.append(cfg)
    L.append("")
    L.append("2. TAMANHO — pelos DOIS termos medidos desta voz.")
    if orc["modelo"]:
        R, P = orc["modelo"]
        L.append(f"   voz {voz}: {R} chars/s de fala + {P} s por frase")
        L.append(f"   longo: ~{orc['chars_longo']} chars de narracao em "
                 f"{CENAS_MIN}-{CENAS_MAX} cenas (~{orc['chars_por_cena']} por cena)")
        L.append(f"   short: ~{orc['chars_short']} chars em 5 cenas")
        L.append(f"   Isto supoe {FRASES_POR_CENA} frases por cena (mediana do corpus).")
        L.append(f"   Cada ponto final a mais custa {P} s: frase curta e ritmo, e")
        L.append("   tambem e orcamento. Escreva mais seco e caberao menos caracteres.")
    else:
        L.append(f"   voz {voz} SEM MODELO MEDIDO — meca antes de dimensionar.")
    L.append(f"   O portao reprova longo abaixo de {PISO_LONGO_S//60} min ou acima "
             f"de {TETO_LONGO_S//60}, e short fora de {SHORT_MIN_S}-{SHORT_MAX_S} s.")
    L.append("")
    L.append(f"3. ESTRUTURA — {CAPS_MIN} a {CAPS_MAX} capitulos.")
    L.append(f"   O capitulo so aparece no YouTube se estiver a {MIN_CAP} s do")
    L.append(f"   anterior; acima de {MAX_CAP} s um novo entra sozinho.")
    L.append("   A cena que FECHA capitulo termina em ? ou : apontando para o")
    L.append("   proximo. Nunca em ponto final: a virada de capitulo e onde o")
    L.append("   espectador sai, e watch hours e a metrica do YPP.")
    L.append("")
    L.append("4. NARRACAO — o que o portao reprova:")
    L.append("   - numeros por extenso, nunca digito cru (o TTS soletra errado)")
    L.append(f"   - no maximo {MAX_NUM_FRASE - 1} quantidades por frase; acima disso")
    L.append("     e planilha falada. Quebre em progressao, um numero por frase.")
    L.append(f"   - no maximo {MAX_PALAVRAS} palavras por frase (um folego)")
    L.append(f"   - no maximo {MAX_VIRGULAS - 1} virgulas por frase")
    L.append(f"   - proibido abrir com: {', '.join(SLOP.get(idi, [])) or '—'}")
    L.append(f"   - proibido citar sem dono: {', '.join(VAGO.get(idi, [])) or '—'}")
    L.append("     (use NOME + ANO + NUMERO, ou nao use)")
    L.append("")
    L.append("5. LAYOUTS disponiveis:")
    for nome, desc in LAYOUTS.items():
        L.append(f"   {nome:8} {desc}")
    L.append("   O rotulo de barra e o de eixo: 'harian', nao 'harian Rp100rb:")
    L.append("   Rp2,6 jt'. Frase inteira em rotulo estoura a borda e reprova.")
    L.append("")
    L.append("6. COPY — descricao com no minimo "
             f"{MIN_PALAVRAS_DESCRICAO} palavras, 3 hashtags, 15 tags")
    L.append("   (o orcamento conta tag com espaco como len+2, teto 480),")
    L.append("   comentario fixado com pergunta real, e aviso de fontes.")
    L.append("   Todo numero da copy tem que estar no roteiro. Nao invente, e")
    L.append("   nao nomeie instituicao que nao de para verificar.")
    L.append("")
    L.append(ARCO_EMOCIONAL)
    L.append("")
    L.append("8. NAO REPETIR — similaridade maxima de 0,65 contra estes titulos")
    L.append("   ja publicados neste canal:")
    for t in (titulos_anteriores or []):
        L.append(f"   - {t}")
    if not titulos_anteriores:
        L.append("   (nenhum informado — passe --titulos para respeitar a regra)")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("canal")
    p.add_argument("--titulos", default=None,
                   help="JSON com a lista de titulos ja publicados no canal")
    args = p.parse_args()
    titulos = json.load(open(args.titulos, encoding="utf-8")) if args.titulos else None
    print(chave(args.canal, titulos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
