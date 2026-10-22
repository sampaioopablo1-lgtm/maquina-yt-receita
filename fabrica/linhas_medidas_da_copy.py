"""As linhas MEDIDAS da copy, GERADAS em vez de escritas por mim.

**MEDIDO em 22/10 as 13:4x, e e a SEXTA vez na mesma sessao.** A copy de cada
peca carrega afirmacoes sobre a PROPRIA peca — quais numerais a narracao fala,
qual a previsao em cada mundo, quantos caracteres por cena, se o esqueleto e
inedito — e eu as escrevia a mao, ANTES de a narracao estar final. Quando o
corte de caracteres entra (e ele entra quase sempre, porque a previsao tem de
cair na faixa), a afirmacao fica atras e a copy passa a dizer coisa falsa sobre
a peca que ela acompanha.

Contado nesta sessao: o `numerais_falados` derrubou a declaracao da copy em
**seis** rodadas, e o valor da previsao no bloco de exposicao eu tive de
reconferir **duas vezes na mesma rodada**. E o item 3 da §10 — toda conta que eu
faco a mao vira um erro meu — aplicado ao texto que acompanha a peca.

**TODA linha e DELEGADA ao dono da medida** (`numerais_falados`, `mira`,
`acento`, `variedade`, `esqueleto_entre_canais`): recalcular qualquer uma aqui
criaria o segundo dono dela, que e a assinatura que congelou a legenda, parou a
mira de conferir por seis pecas e pos job inventado na serie.

**NAO E PORTAO e nao reprova**, pelo argumento do `mira.py`: ele GERA o texto
para eu colar, e o codigo de saida e sempre zero.

### E A CONFERENCIA NO OUTRO SENTIDO NAO E VIAVEL — medido, e vai escrito

O `numerais_falados.declaracao_incompleta` cobre UM ramo: numeral que a narracao
FALA e a copy nao cita. O ramo que falta e o meu defeito: numeral que a copy
declara como falado e a narracao NAO fala. Eu tentei fecha-lo pelo unico sinal
mecanico disponivel — numeral do idioma aparecendo **entre aspas** na copy — e
**medi antes de ligar**:

| | |
|---|---|
| specs de short solto varridas | **285** |
| acusadas pela regra crua | 12 |
| **das quais so o ACENTO diferia** (`tres` contra `tres`) | **8** |
| acusadas depois de dobrar o acento | **5** |
| **FALSOS POSITIVOS** | **4** |
| casos REAIS | **1** (`labtreinamento-s071`, que declara "dois" e fala so "tres") |

Os quatro falsos positivos tem todos a MESMA forma, e ela e inevitavel: a copy
cita o numeral **entre aspas para dizer que ele esta AUSENTE**, ou para falar da
peca de um IRMAO. Medidos: *"sem dizer 'tres', porque a contagem nao e a tese"*,
*"'cinco' seria numeral, e a lista pode mudar"*, *"nao e 'media', nao e 'tres'"*
e *"falava 'dwa' e 'jeden' pelo mesmo motivo"* — este ultimo sobre o irmao.

Logo **quatro de cinco achados seriam inventados**, e o 725 e explicito:
detector que inventa achado e pior que nao ter detector. **A conferencia fica
NAO FEITA, e dita como nao feita** — o que fecha o defeito e a geracao, nao a
acusacao: linha gerada nao pode discordar da peca, porque ela sai da peca.
"""
from __future__ import annotations

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import acento as AC           # noqa: E402
import esqueleto_entre_canais as EC   # noqa: E402
import mira                   # noqa: E402
import ensaio                 # noqa: E402
import nome_da_spec as NS     # noqa: E402
import numerais_falados as NF  # noqa: E402
import rascunho as RS         # noqa: E402
import variedade as V         # noqa: E402


def medidas(caminho: str = None, spec: dict = None) -> dict:
    """Os fatos medidos da peca, cada um pedido ao DONO dele.

    Aceita rascunho (`spec=`), porque a copy se escreve ANTES de a spec ir para
    o disco — e e justamente ai que a afirmacao a mao envelhece.
    """
    sp = RS.spec_de(caminho, spec)
    cenas = sp.get("short") or []
    if not cenas:
        return {"pacote": sp.get("pacote"), "cenas": 0, "tem_short": False}
    pacote = sp.get("pacote") or ""
    nf = NF.da_spec(sp)
    conf = mira.confere(sp)
    nov = EC.novidade(V.esqueleto(cenas), len(cenas), None,
                      NS.arquivo(pacote) if pacote else "")
    th = sp.get("thumb") or {}
    return {
        "pacote": pacote,
        "tem_short": True,
        "cenas": len(cenas),
        "idioma": nf["idioma"],
        "numerais": list(nf["total"] or []),
        "numerais_sabe_ler": nf["total"] is not None,
        # as previsoes moram em `confere()["previsoes"]`, e a faixa vem do
        # `ensaio.faixa_do_short` — perguntar a FORMA antes de ler e o que
        # impede o `.get` com default de devolver vazio bem formado
        # (22/10 as 08:3x).
        "prev_edge": (conf.get("previsoes") or {}).get("edge"),
        "prev_piper": (conf.get("previsoes") or {}).get("piper"),
        # DUAS faixas com o mesmo nome "faixa" no repo, e confundi-las e o
        # 753 em forma de UNIDADE: a do PORTAO (`faixa_do_short`, 18 a 45) e
        # a MIRA (`alvo_short`, 41,5 a 43,0 na frota). As duas vao NOMEADAS.
        "faixa_do_portao": ensaio.faixa_do_short(sp),
        "mira": ensaio.alvo_short(NS.pacote(sp.get("pacote") or "")
                                  and __import__("canal").da_spec(sp)),
        "media_chars": round(
            sum(len(c.get("nar") or "") for c in cenas) / float(len(cenas)), 2),
        "esqueleto": V.esqueleto(cenas),
        "forma_inedita": nov.get("forma_inedita"),
        "formas_da_frota": nov.get("formas_na_frota"),
        # o `acento.proporcao` recebe CENAS, nao texto: passar o texto junto
        # estoura `AttributeError` numa linha do OUTRO modulo, que e a
        # familia de 22/10 as 09:3x. Pego na primeira execucao.
        "acento": AC.proporcao(cenas),
        "thumb_palavras": len(
            ("%s %s" % (th.get("l1", ""), th.get("l2", ""))).split()),
        "gancho_palavras": len(
            V.primeira_frase((cenas[0].get("nar") or "")).split()),
    }


def _linha_dos_numerais(m: dict) -> str:
    """UM dono da frase dos numerais, e ela sai nos DOIS ramos.

    Idioma sem vocabulario **DIZ que o modulo nao sabe ler** em vez de afirmar
    que a narracao nao fala numeral: vazio de instrumento nao prova ausencia
    (17/10).
    """
    if not m.get("numerais_sabe_ler"):
        return ("NUMERAIS: o `numerais_falados` NAO sabe ler o idioma %r, logo "
                "esta linha nao afirma nada sobre a narracao — vazio de "
                "instrumento nao prova ausencia." % m.get("idioma"))
    ns = m.get("numerais") or []
    if not ns:
        return ("NUMERAIS: a narracao nao fala numeral nenhum, conferido pelo "
                "`numerais_falados` (com a ressalva dele: ausencia de "
                "vocabulario nao prova ausencia).")
    return ("NUMERAIS falados pela narracao, do `numerais_falados`: %s. Se eles "
            "sao estrutura do argumento ou fato sobre o mundo, decide a regra "
            "(g) — e ela e leitura." % ", ".join('"%s"' % n for n in ns))


def linhas(caminho: str = None, spec: dict = None) -> list:
    """As linhas prontas para colar na copy, todas DERIVADAS."""
    m = medidas(caminho, spec)
    if not m.get("tem_short"):
        return ["sem cenas de short: nada a medir."]
    L = [_linha_dos_numerais(m)]
    if m.get("prev_edge") is not None:
        L.append("PREVISAO, do `ensaio` pelo `mira.confere`: edge %.2f s / "
                 "piper %.2f s. MIRA do canal %s; faixa que o PORTAO cobra "
                 "%s — as duas se chamam faixa no repo e nao sao a mesma."
                 % (m["prev_edge"], m["prev_piper"], m.get("mira"),
                    m.get("faixa_do_portao")))
    L.append("FORMA: %d cenas, media de %.2f caracteres por cena, esqueleto "
             "`%s` — %s nas %s formas de short da frota (do "
             "`esqueleto_entre_canais`, com esta peca FORA da varredura)."
             % (m["cenas"], m["media_chars"], m["esqueleto"],
                "INEDITO" if m.get("forma_inedita") else "JA EXISTE",
                m.get("formas_da_frota")))
    # o `acento.proporcao` JA devolve percentual: multiplicar por 100 aqui
    # imprimiu 1361%% na primeira execucao — e o 753 em forma de UNIDADE,
    # duas grandezas com o mesmo nome dentro do mesmo relato.
    L.append("REDACAO: acento %.2f%% da narracao, thumbnail com %d palavra(s), "
             "gancho com %d palavra(s) — os limites sao do portao `variedade`."
             % (m["acento"], m["thumb_palavras"], m["gancho_palavras"]))
    return L


def relato(caminho: str = None, spec: dict = None) -> str:
    L = ["LINHAS MEDIDAS da copy — GERADAS, nao escritas a mao:"]
    for x in linhas(caminho, spec):
        L.append("  " + x)
    L.append("  cole-as na copy em vez de as redigitar: foi redigitar que fez a "
             "declaracao de numerais ficar atras da narracao em SEIS rodadas "
             "desta sessao, sempre depois do corte de caracteres.")
    L.append("  e a conferencia no OUTRO sentido (numeral que a copy declara e "
             "a narracao nao fala) NAO foi feita, e o motivo esta no docstring: "
             "4 de 5 achados seriam inventados (725).")
    return "\n".join(L)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: linhas_medidas_da_copy.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
