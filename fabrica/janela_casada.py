#!/usr/bin/env python3
"""Comparar braco com braco na MESMA FAIXA DE IDADE, e dizer quando NAO ha leitura.

POR QUE ISTO EXISTE. A rotina manda, em letra, "compare peca com peca na MESMA
FAIXA DE IDADE, lendo a janela do proprio `metricas`" — e nao havia modulo
nenhum para isso. Eu vinha fazendo no olho, e no olho eu errei tres vezes:

  684  usei a MELHOR peca do grupo como linha de base, e o gatilho mandou
       desfazer o que nao tinha feito nada;
  682  comparei piso atual de pecas de idades diferentes, que e o efeito (D);
  698  acertei a conta (duas pecas abaixo do minimo de oito, ~1%) mas a fiz de
       cabeca, e a mesma conta de cabeca em 701 saiu certa por sorte.

Entao a conta mora aqui. O modulo faz TRES coisas, e a terceira e a que mais
importa:

  1. escolhe, para cada peca, a leitura DENTRO de uma faixa de idade declarada;
  2. diz se as FAIXAS dos dois bracos se sobrepoem;
  3. **quando se sobrepoem, RECUSA chamar de leitura** — devolve
     `ha_leitura=False` com o motivo escrito, em vez de deixar quem le escolher
     uma mediana que lhe agrade.

A regra que isto implementa e do 693 e do proprio 684: *se a peca nova cai
DENTRO da faixa antiga, nao ha leitura, qualquer que seja a mediana.* Com
CV 0,66 views/peca e cego abaixo do dobro, e faixa que se sobrepoe nao chega
nem perto disso.

O p devolvido quando NAO ha sobreposicao e combinatorio e exato: sob a nula de
os dois bracos virem da mesma distribuicao, a chance de os `k` do braco novo
ocuparem exatamente as `k` posicoes do topo (ou da base) e `1/C(n, k)`. **Ele
NAO e um teste de magnitude** — nao diz que o efeito e grande, diz so que a
separacao completa seria improvavel por acaso. E ele e invalido se as pecas nao
forem de dias comparaveis: o confundidor temporal do 701 continua sendo do
RELATO, nao da conta.
"""
from __future__ import annotations

import json
import sys
from math import comb


class SemLeituraNaFaixa(Exception):
    """Nenhuma leitura da peca cai dentro da faixa de idade pedida."""


def leitura_na_faixa(leituras: list[tuple[float, int]],
                     de_h: float, ate_h: float) -> int:
    """A leitura da peca dentro da faixa. O MAXIMO, pelo estimador do 688.

    Varias leituras podem cair na faixa (a rodada coleta de hora em hora). O
    estimador e o maximo declarado como PISO — um contador de view so atrasa,
    nunca adianta — entao entre duas leituras da mesma faixa vale a maior, e
    nao a ultima.
    """
    dentro = [v for (h, v) in leituras if de_h <= h <= ate_h]
    if not dentro:
        raise SemLeituraNaFaixa(
            f"nenhuma das {len(leituras)} leituras cai em [{de_h}, {ate_h}] h. "
            "Isto nao e zero: e silencio. Colete na faixa ou alargue a faixa "
            "DECLARANDO que alargou."
        )
    return max(dentro)


def separacao(novo: list[int], antigo: list[int]) -> dict:
    """Os dois bracos se separam? E com que p sob a nula?

    `ha_leitura` e False quando as faixas se sobrepoem, e e esse campo que
    decide — nao a mediana, que existe no retorno so para o relato.
    """
    if not novo or not antigo:
        raise ValueError("braco vazio: sem n nao existe comparacao")

    acima = min(novo) > max(antigo)
    abaixo = max(novo) < min(antigo)
    n, k = len(novo) + len(antigo), len(novo)
    p = 1.0 / comb(n, k) if (acima or abaixo) else None

    return {
        "novo": sorted(novo, reverse=True),
        "antigo": sorted(antigo, reverse=True),
        "faixa_novo": (min(novo), max(novo)),
        "faixa_antigo": (min(antigo), max(antigo)),
        "mediana_novo": _mediana(novo),
        "mediana_antigo": _mediana(antigo),
        "sobrepoe": not (acima or abaixo),
        "ha_leitura": acima or abaixo,
        "direcao": "novo ACIMA" if acima else ("novo ABAIXO" if abaixo else None),
        "p_sob_a_nula": p,
        "n_total": n,
        "motivo": None if (acima or abaixo) else (
            f"as faixas se SOBREPOEM — novo [{min(novo)}, {max(novo)}] dentro ou "
            f"cruzando antigo [{min(antigo)}, {max(antigo)}]. Pelo 684/693, peca "
            "nova dentro da faixa antiga NAO e leitura, qualquer que seja a "
            "mediana."),
    }


def _mediana(xs: list[int]) -> float:
    s = sorted(xs)
    m = len(s) // 2
    return float(s[m]) if len(s) % 2 else (s[m - 1] + s[m]) / 2.0


def compara(pecas: dict, bracos: dict, de_h: float, ate_h: float) -> dict:
    """`pecas` = {nome: [(idade_h, views)]}; `bracos` = {braco: [nomes]}.

    Exige exatamente dois bracos, e o primeiro e o NOVO. Peca sem leitura na
    faixa sai em `sem_leitura` em vez de entrar como zero — ausencia e silencio.
    """
    if len(bracos) != 2:
        raise ValueError("a comparacao e entre DOIS bracos, nem mais nem menos")
    (nome_novo, lista_novo), (nome_antigo, lista_antigo) = bracos.items()

    vals, sem = {}, []
    for braco in (lista_novo, lista_antigo):
        for nome in braco:
            try:
                vals[nome] = leitura_na_faixa(pecas[nome], de_h, ate_h)
            except SemLeituraNaFaixa:
                sem.append(nome)

    novo = [vals[n] for n in lista_novo if n in vals]
    antigo = [vals[n] for n in lista_antigo if n in vals]
    if not novo or not antigo:
        return {"faixa_h": (de_h, ate_h), "sem_leitura": sem, "ha_leitura": False,
                "motivo": "um dos bracos ficou sem nenhuma peca na faixa de idade",
                "braco_novo": nome_novo, "braco_antigo": nome_antigo,
                "valores": vals}

    out = separacao(novo, antigo)
    out.update({"faixa_h": (de_h, ate_h), "sem_leitura": sem,
                "braco_novo": nome_novo, "braco_antigo": nome_antigo,
                "valores": vals})
    return out


def relato(r: dict) -> str:
    out = [f"JANELA CASADA de {r['faixa_h'][0]} a {r['faixa_h'][1]} h de vida.",
           f"  {r['braco_novo']:22} {r.get('novo')}",
           f"  {r['braco_antigo']:22} {r.get('antigo')}"]
    if r.get("sem_leitura"):
        out.append(f"  SEM leitura na faixa (silencio, nao zero): "
                   + ", ".join(r["sem_leitura"]))
    if r["ha_leitura"]:
        out.append(f"  SEPARADOS, {r['direcao']}, p = 1/{round(1/r['p_sob_a_nula'])}"
                   f" = {r['p_sob_a_nula']*100:.1f}% sob a nula (n={r['n_total']}).")
        out.append("  E o p NAO mede magnitude, so separacao. Confundidor "
                   "temporal vai no RELATO.")
    else:
        out.append("  NAO HA LEITURA. " + r["motivo"])
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print('uso: janela_casada.py \'{"de_h":2.5,"ate_h":4.5,'
              '"pecas":{"a":[[3.0,11]]},"bracos":{"novo":["a"],"antigo":["b"]}}\'')
        return 2
    d = json.loads(sys.argv[1])
    print(relato(compara(d["pecas"], d["bracos"], d["de_h"], d["ate_h"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
