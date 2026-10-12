#!/usr/bin/env python3
"""Escreve uma spec sem sobrescrever pacote alheio por engano.

POR QUE ISTO EXISTE, e a resposta e um erro meu de 20/08/2026.

Escolhi o numero `epomeno-epipedo-005` para um pacote novo sem olhar quais ja
existiam. O -005 existia, estava commitado e o video ja estava NO AR — "Επιτόκια
2026: 0,03% στην κατάθεση, 14,49% στην κάρτα", 83 cenas. O build script
sobrescreveu o `.json` inteiro e NADA reclamou:

  - os portoes baratos rodaram no conteudo NOVO e passaram, porque o conteudo
    novo estava correto; eles conferem a spec, nao a identidade dela;
  - o `pacote` dentro do arquivo batia com o nome do arquivo, entao um teste de
    coerencia nome-x-campo tambem teria passado;
  - o que me salvou foi acidente: a extracao das tags falhou, fui ver por que, e
    a copy que apareceu era de outro video.

Se as tags tivessem sido extraidas, eu teria publicado e o `.json` de um video
no ar estaria descrito por outro roteiro para sempre.

A REGRA: numero de pacote se CONSULTA, nao se supoe. `proximo_livre()` responde
olhando o diretorio, e `grava()` recusa apagar spec de outro pacote.
"""
import json
import os
import pathlib
import re
import sys

SPECS = pathlib.Path(__file__).resolve().parent / "specs"


def ocupados(slug: str) -> list[int]:
    """Numeros de pacote que ja existem em disco para o canal."""
    ns = []
    for p in SPECS.glob(f"{slug}-*.json"):
        m = re.search(r"-(\d{3})\.json$", p.name)
        if m:
            ns.append(int(m.group(1)))
    return sorted(ns)


def proximo_livre(slug: str) -> str:
    """O proximo numero de pacote do canal, como `slug-NNN`.

    Devolve max+1 e nao o primeiro buraco: buraco costuma ser pacote que
    alguem apagou de proposito, e reusar o numero mistura dois historicos.
    """
    ns = ocupados(slug)
    return f"{slug}-{(max(ns) + 1) if ns else 1:03d}"


def _titulo(copy: str) -> str:
    """Primeira linha do copy, que e o `# titulo` do markdown."""
    for linha in (copy or "").splitlines():
        if linha.startswith("#"):
            return linha.lstrip("# ").strip()
    return ""


def grava(spec: dict, caminho: str | None = None, *,
          forcar: bool = False) -> pathlib.Path:
    """Grava a spec em `specs/<pacote>.json`, recusando trocar de pacote.

    Recusa quando ja existe arquivo no destino cujo TITULO e outro — o sinal
    de que o numero pertence a outro video. Reescrever a propria spec (mesmo
    titulo, roteiro revisado) continua livre, que e o caso normal.

    `forcar` E KEYWORD-ONLY DESDE 12/10, E ISSO CONSERTA UM DEFEITO SILENCIOSO
    QUE DESLIGAVA ESTA TRAVA EM 114 DOS 166 BUILDERS.

    A assinatura antiga era `grava(spec, forcar=False)`, e a convencao dos
    builders era chamar `grava(SPEC, "fabrica/specs/<pacote>.json")` — passando
    um CAMINHO na posicao do `forcar`. String nao vazia e verdadeira, logo todos
    esses builders rodavam com `forcar=True` e **pulavam a conferencia inteira**.
    Medido em 12/10: 114 de 166. A trava existe por causa do defeito de 19/08,
    quando o `kolejny-poziom-007` renderizou 89 cenas e dezessete minutos de
    runner para descobrir que o nome ja pertencia a um video de 11/08 — e ela
    estava desligada justamente nos builders que a usariam.

    O `caminho` deixou de ser ignorado e passou a ser CONFERIDO contra o destino
    derivado do `pacote`. Medido antes de mudar: nos 114 builders que o passam, o
    caminho bate com o derivado em **114 de 114**, entao a conferencia nao
    quebra ninguem e transforma um argumento inerte em verificacao.
    """
    pacote = spec["pacote"]
    alvo = SPECS / f"{pacote}.json"
    if caminho is not None:
        esperado = os.path.join("fabrica", "specs", f"{pacote}.json")
        dado = os.path.normpath(str(caminho))
        if os.path.normpath(esperado) != dado and os.path.basename(dado) != alvo.name:
            raise SystemExit(
                f"RECUSADO: o caminho passado nao e o destino desta spec.\n"
                f"  passado:  {caminho}\n"
                f"  derivado: {esperado}\n"
                f"  o destino vem do campo `pacote`, nao do argumento.")
    if alvo.exists() and not forcar:
        velho = json.loads(alvo.read_text(encoding="utf-8"))
        tv, tn = _titulo(velho.get("copy", "")), _titulo(spec.get("copy", ""))
        if tv and tn and tv != tn:
            raise SystemExit(
                f"RECUSADO: {alvo.name} ja existe e e outro video.\n"
                f"  em disco: {tv}\n"
                f"  chegando: {tn}\n"
                f"  o proximo numero livre deste canal e "
                f"{proximo_livre(spec['slug'])}\n"
                f"  (se a intencao e mesmo substituir, passe forcar=True)")
    alvo.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    return alvo


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("uso: grava_spec.py <slug-do-canal>")
    slug = sys.argv[1]
    print(f"ocupados: {ocupados(slug)}")
    print(f"proximo livre: {proximo_livre(slug)}")
