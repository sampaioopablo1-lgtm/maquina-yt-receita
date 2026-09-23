#!/usr/bin/env python3
"""Roda as cinco auditorias e separa achado NOVO de achado JA REPORTADO.

Duas dores concretas que este script resolve.

**A primeira: rodar 3 de 5.** Sao cinco auditorias somente-leitura, cada uma
com seu comando, e nenhuma delas sabe das outras. Rodada que esquece uma nao
percebe que esqueceu.

**A segunda, que ja me pegou:** em 23/09/2026 eu reportei 5 achados de tag ao
dono como se fossem trabalho novo, e 3 deles estavam resolvidos na conta havia
uma hora. A correcao foi o aviso de frescor (`_frescor.py`). Mas sobra o caso
oposto e igualmente ruim: achado REAL, ja reportado, ja na fila do dono, sendo
reapresentado a cada rodada como se fosse novidade. Isso treina o dono a ignorar
o relatorio tao bem quanto o alarme falso treina.

Entao aqui existe uma LINHA DE BASE: `auditoria-base.json`, que diz quantos
achados cada auditoria tem hoje e por que. O relatorio compara:

  - contagem == base  -> "conhecido", nao e novidade, o dono ja tem na fila
  - contagem  > base  -> **NOVO**, e o unico caso que pede atencao
  - contagem  < base  -> **CONSERTADO**, e noticia boa que vale dizer

A base e commitada de proposito: quando o dono decide e alguem conserta, a
base muda no mesmo commit do conserto, e quem ler o diff ve as duas coisas
juntas. Base que ninguem atualiza vira mentira — se a contagem cair, este
script manda atualizar.

Uso:  python3 wesales/tools/auditoria_tudo.py
      python3 wesales/tools/auditoria_tudo.py --gravar-base   # depois de conserto

Codigo de saida:  0 = nada novo   1 = achado novo   2 = base desatualizada
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "auditoria-base.json")
HORAS = re.compile(r"\(\d+ h atras\)")

# nome -> (script, como contar os achados na saida)
# A contagem vem da propria saida, nao do codigo de saida: auditoria que sai 0
# de proposito (`campos`) tambem tem achado que vale acompanhar.
AUDITORIAS = [
    ("refs", "auditoria_refs.py", "referencia para workflow arquivado"),
    ("tags", "auditoria_tags.py", "tag com limpeza pulada sem segunda rede"),
    ("campos", "auditoria_campos.py", "campo nem escrito nem lido"),
    ("condicoes", "auditoria_condicoes.py", "condicao de oportunidade sem gatilho que a carregue"),
    ("portoes", "auditoria_portoes.py", "cadencia que consome capacidade sem ler os portoes"),
]

# Como extrair a contagem de cada saida. Cada auditoria imprime um cabecalho
# proprio; contar linha por padrao e mais estavel que parsear tudo.
CONTA = {
    "refs": lambda s: 0 if "nenhuma referencia para workflow arquivado" in s
            else s.count("-> "),
    "tags": lambda s: 0 if "nenhuma tag com limpeza pulada sem segunda rede" in s
            else s.count("arrancado por:"),
    "campos": lambda s: _depois(s, "NEM ESCRITO NEM LIDO por workflow"),
    "condicoes": lambda s: 0 if "nenhum (no que os dumps mostram)" in s
            else s.count("conserto: `patch_condicoes_etapa.py`"),
    "portoes": lambda s: 0 if "nenhuma (no que os dumps mostram)" in s
            else s.count("a promessa do GUIA-SDR.md"),
}


def _depois(saida, marca):
    """O numero no fim da linha que contem `marca` (ex.: '... — 4:')."""
    for linha in saida.splitlines():
        if marca in linha:
            digitos = "".join(c for c in linha.split("—")[-1] if c.isdigit())
            return int(digitos) if digitos else 0
    return 0


def roda(script):
    r = subprocess.run([sys.executable, os.path.join(AQUI, script)],
                       capture_output=True, text=True)
    return r.stdout + r.stderr, r.returncode


def le_base():
    try:
        with open(BASE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def main():
    gravar = "--gravar-base" in sys.argv
    base = le_base()
    if not base and not gravar:
        print("SEM LINHA DE BASE (%s nao existe ou nao le)." % os.path.basename(BASE))
        print("Rode com --gravar-base para congelar o estado de hoje como base.\n")

    resultado, novos, consertados = {}, [], []
    velhos = atrasados = 0
    for nome, script, rotulo in AUDITORIAS:
        saida, codigo = roda(script)
        n = CONTA[nome](saida)
        resultado[nome] = {"achados": n, "rotulo": rotulo, "saida": codigo}
        if not velhos and not atrasados:
            # o aviso do `_frescor` e igual nas cinco; basta ler de uma
            velhos = len(HORAS.findall(saida))
            atrasados = saida.count("dump ") if "AVISO DE FRESCOR" in saida else 0

    print("=" * 72)
    print("AUDITORIA COMPLETA — %d auditorias somente-leitura" % len(AUDITORIAS))
    print("=" * 72)
    if velhos or atrasados:
        print("frescor: %d dump(s) possivelmente defasado(s), %d com backup irmao mais"
              % (velhos, atrasados))
        print("novo. Achado que os envolva e CANDIDATO, nunca item.")
        print("-" * 72)
    print("%-11s %8s %8s  %s" % ("auditoria", "achados", "base", "situacao"))
    for nome, _, rotulo in AUDITORIAS:
        n = resultado[nome]["achados"]
        b = (base.get(nome) or {}).get("achados")
        if b is None:
            sit = "sem base"
        elif n > b:
            sit = "*** NOVO: %d a mais que a base ***" % (n - b)
            novos.append((nome, b, n, rotulo))
        elif n < b:
            sit = "CONSERTADO: %d a menos que a base" % (b - n)
            consertados.append((nome, b, n))
        else:
            sit = "conhecido, ja na fila do dono" if n else "limpo"
        print("%-11s %8d %8s  %s" % (nome, n, "-" if b is None else b, sit))
    print()

    for nome, _, rotulo in AUDITORIAS:
        n = resultado[nome]["achados"]
        porque = (base.get(nome) or {}).get("porque")
        if n and porque:
            print("  %s (%d): %s" % (nome, n, porque))
    if any(resultado[n]["achados"] for n, _, _ in AUDITORIAS):
        print()

    if novos:
        print("!" * 72)
        print("ACHADO NOVO — isto sim e para olhar agora")
        for nome, b, n, rotulo in novos:
            print("   %s: %d -> %d  (%s)" % (nome, b, n, rotulo))
        print("   Rode a auditoria sozinha para ver qual. Achado de dump e")
        print("   CANDIDATO: confirmar ao vivo antes de virar item.")
        print("!" * 72)
    if consertados:
        print("Consertado desde a base: %s" %
              ", ".join("%s (%d->%d)" % x for x in consertados))
        print("Atualize a base no MESMO commit do conserto: --gravar-base")

    if gravar:
        novo = {nome: {"achados": resultado[nome]["achados"],
                       "porque": (base.get(nome) or {}).get("porque", "")}
                for nome, _, _ in AUDITORIAS}
        with open(BASE, "w", encoding="utf-8") as fh:
            json.dump(novo, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print("\nbase gravada em %s — revise o campo `porque` de cada uma."
              % os.path.basename(BASE))
        return 0

    if novos:
        return 1
    if consertados:
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
