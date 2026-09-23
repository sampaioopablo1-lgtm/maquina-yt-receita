#!/usr/bin/env python3
"""Toque que consome capacidade tem de passar pelos portoes de capacidade.

O `GUIA-SDR.md` (linhas 74-76) promete ao SDR, sem ressalva: "se voce passar de
100 toques no dia ou tiver 50 ou mais tarefas vencidas, o sistema segura os
toques novos". E o `pausado` e o botao de pausa do proprio SDR, aplicado a mao.
Quem cumpre essas duas promessas sao portoes dentro de cada cadencia — e
cadencia montada depois pode simplesmente nao te-los. Foi assim que a
`Cadência Inbound` ficou sem os dois portoes de capacidade (F-05 / 9e), achado
a mao em 23/09/2026. Esta auditoria existe para o proximo caso nao precisar de
sorte.

A INVARIANTE, e nao "comparar a cadencia A com a B": **se um toque coloca o
lead na fila (`fila-tel` / `fila-wa`) ou conta `toque`, ele consome capacidade
do SDR — logo a cadencia tem de ler os tres portoes.** Comparar cadencia com
cadencia daria alarme falso a cada diferenca legitima de desenho; a invariante
nao.

Os tres portoes, e o que cada um le:

| portao                      | le                              |
|-----------------------------|---------------------------------|
| `Lead pausado?`             | tag `pausado`                   |
| `SDR lotado?`               | tag `sdr-lotado`                |
| `Teto de toques da semana?` | campo `c1xuCuLyJheHOQoJ3grH`    |

A deteccao e por CONTEUDO, nao por nome de no: procura a tag/campo em qualquer
lugar do workflow. Cadencia que leia `sdr-lotado` num no chamado de outra
coisa passa — e correto que passe, o que importa e ler.

Cobertura por toque entra como informacao: portao presente em 5 de 6 toques e
buraco parcial, e o numero mostra onde olhar. Portao em 0 de N e o que falha.

Achado em cadencia `published` e falha (codigo 1). `draft` e `ZZ TESTE*` sao
aviso.

Limite honesto, o de sempre: le os dumps de `wesales/workflows-json/`, que sao
fotografia — o aviso de frescor do `_frescor.py` diz quais estao velhos.
Achado tirado de dump e CANDIDATO; confirma-se lendo o workflow ao vivo, ou
medindo o efeito (contato com `pausado` numa cadencia que recebe `fila-tel`).

Uso:  python3 wesales/tools/auditoria_portoes.py
Sai com codigo 1 se cadencia publicada consumir capacidade sem ler os portoes.
"""
import collections
import glob
import json
import os
import re
import sys

from _frescor import aviso

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")

# `T7 · Lead pausado?`, `TI1 · Ainda vale ligar?`, `TR3 · Atendeu?` ...
TOQUE = re.compile(r"^([A-Z]{1,3})(\d+)\s*·\s*(.+)$")

# O que marca "este toque consome capacidade do SDR".
CONSOME = {"fila-tel", "fila-wa", "toque"}

# portao -> (o que ele le, como aparece no JSON)
PORTOES = {
    "Lead pausado?": "pausado",
    "SDR lotado?": "sdr-lotado",
    "Teto de toques da semana?": "c1xuCuLyJheHOQoJ3grH",
}


def le(bruto, chave):
    """A cadencia le esta tag/campo em algum lugar?

    Tag entra no JSON como elemento de lista (`["sdr-lotado"]`), e campo
    personalizado como `conditionSubType`. `"chave"` com as aspas evita casar
    `pausado` dentro de `despausado` ou de um texto de mensagem.
    """
    return ('"%s"' % chave) in bruto


def cadencias():
    """[(nome, status, {toque: {portao}}, bruto, consome?)] de todo dump com toques."""
    saida = []
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        wf = dado.get("workflow") or {}
        if not wf.get("id"):
            continue
        tpl = (wf.get("workflowData") or {}).get("templates") or []
        toques = collections.defaultdict(set)
        for t in tpl:
            m = TOQUE.match(t.get("name") or "")
            if m:
                toques[m.group(1) + m.group(2)].add(m.group(3))
        if not toques:
            continue
        bruto = json.dumps(tpl, ensure_ascii=False)
        consome = sorted(c for c in CONSOME if le(bruto, c))
        saida.append((wf.get("name") or os.path.basename(caminho)[:-5],
                      wf.get("status"), dict(toques), bruto, consome))
    return saida


def main():
    aviso(DUMPS)
    todas = cadencias()
    if not todas:
        print("nenhuma cadencia com toques nomeados em %s" % DUMPS)
        return 0

    print("%d cadencia(s) com toques nomeados\n" % len(todas))
    graves, avisos = [], []

    for nome, status, toques, bruto, consome in todas:
        n = len(toques)
        faltam, parciais = [], []
        for portao, chave in PORTOES.items():
            if not le(bruto, chave):
                faltam.append((portao, chave))
                continue
            k = sum(1 for g in toques.values() if portao in g)
            if 0 < k < n:      # k == 0 e so rotulo diferente, nao buraco
                parciais.append((portao, k, n))

        print("%-38s [%-9s] %d toque(s)  consome: %s"
              % (nome[:38], status, n, ", ".join(consome) or "nao aparenta consumir"))
        for portao, chave in PORTOES.items():
            if not le(bruto, chave):
                print("     NAO le %-22s  (portao %r ausente)" % (chave, portao))
                continue
            k = sum(1 for g in toques.values() if portao in g)
            if k == n:
                print("     le %-26s  portao %r nos %d toques" % (chave, portao, n))
            elif k == 0:
                # `Recuperação de No-show` le `pausado` dentro do
                # `NS{n} · Ainda vale recuperar?`. Ler e o que importa; o nome
                # do no e so o rotulo. Isto NAO e achado.
                print("     le %-26s  sob outro nome de no (nenhum %r) — ok"
                      % (chave, portao))
            else:
                print("     le %-26s  portao %r em %d de %d toques" % (chave, portao, k, n))
        if faltam and consome:
            alvo = graves if (status == "published"
                              and not nome.startswith("ZZ TESTE")) else avisos
            alvo.append((nome, status, n, consome, faltam))
        for portao, k, total in parciais:
            print("     PARCIAL: %r em %d de %d toques" % (portao, k, total))
        print()

    print("=" * 72)
    print("CADENCIA PUBLICADA QUE CONSOME CAPACIDADE SEM LER OS PORTOES")
    if not graves:
        print("  nenhuma (no que os dumps mostram)")
    for nome, status, n, consome, faltam in graves:
        print("  %s  [%s]  %d toques" % (nome, status, n))
        print("      cada toque marca: %s" % ", ".join(consome))
        for portao, chave in faltam:
            print("      nao le %-24s -> portao %r nunca roda" % (chave, portao))
        print("      a promessa do GUIA-SDR.md linhas 74-76 e falsa para esta cadencia")
    print("=" * 72)

    if avisos:
        print("\nMESMO PADRAO, MAS NAO E FALHA — rascunho ou copia de teste")
        for nome, status, n, consome, faltam in avisos:
            print("  %-38s [%s]  falta: %s"
                  % (nome[:38], status, ", ".join(p for p, _ in faltam)))

    if graves:
        print("\nAchado de dump e CANDIDATO. Confirmar lendo o workflow ao vivo, ou")
        print("medindo: contato com `pausado` que ainda recebe `fila-tel`.")
    return 1 if graves else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
