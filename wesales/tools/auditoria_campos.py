#!/usr/bin/env python3
"""Mapa de quem escreve e quem le cada campo personalizado (somente leitura).

Nasceu do `d880870`, onde o dono achou a mao "4 campos de data que nunca
gravavam". Este script generaliza a pergunta: para cada campo personalizado de
contato, quais workflows PUBLICADOS escrevem nele e quais leem.

DE PROPOSITO NAO E ALARME: sai sempre com 0. A regra que este projeto aprendeu
em 23/09/2026 e que auditoria gritando sobre o que e intencional treina a gente
a ignorar auditoria — e aqui a maior parte do resultado e intencional:

  - "so lido, ninguem escreve" e o normal dos campos de QUALIFICACAO: quem
    preenche `Budget`, `Decisor`, `Dor principal`, `Segmento`, `Urgencia`,
    `Motivo da desqualificacao`, `Reuniao foi qualificada` e o SDR ou o closer
    na tela. Workflow le o que o humano classificou. Nao e defeito.
  - "so escrito, ninguem le" quase sempre significa "a LISTA que leria ainda
    nao existe". `Prioridade`, `Tentativas telefone`, `Conexoes telefone`
    existem para ordenar e mostrar nas listas inteligentes (secoes 8.x do
    `IMPLEMENTACAO-WORKFLOWS.md`), e lista inteligente NAO aparece em nenhum
    dump. Este script nao ve listas — logo nao pode chamar isso de orfao.

O que vale olhar de verdade e a terceira coluna: campo que **nem e escrito nem
e lido por workflow nenhum**. Ai ou a fiacao nunca foi montada, ou o campo
sobrou de um desenho antigo. Cruzar cada um com `campos-e-tags.md` antes de
concluir: alguns estao declarados como "especificado, falta montar na tela".

Limite, o mesmo das outras duas auditorias: le os dumps de
`wesales/workflows-json/`, que podem estar defasados da conta. Dump com backup
irmao identico em `updatedAt` e pre-patch e nao responde nada.

As duas guardas de frescor ficam no `_frescor.py`, compartilhado pelas tres
auditorias: elas imprimem o mesmo aviso porque leem os mesmos dumps.

Uso:  python3 wesales/tools/auditoria_campos.py
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

from _frescor import aviso

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
INVENTARIO = os.path.join(AQUI, "campos.json")
ESCRITA = {"update_contact_field", "math_operation"}
MERGE = re.compile(r"\{\{\s*(contact\.[a-z0-9_]+)")


def inventario():
    """id -> nome dos campos PERSONALIZADOS de contato (standard fica fora)."""
    with open(INVENTARIO, encoding="utf-8") as fh:
        dado = json.load(fh)
    saida = {}
    for nome, v in dado.items():
        if not isinstance(v, dict):
            continue
        chave = str(v.get("chave") or "")
        if v.get("id") and chave.startswith("contact.") and v.get("tipo") != "STANDARD_FIELD":
            saida[v["id"]] = (nome, chave)
    return saida


def varre(campos):
    chave2id = {chave: i for i, (_, chave) in campos.items()}
    escreve, le = defaultdict(set), defaultdict(set)
    publicados = 0
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        wf = dado.get("workflow") or dado
        if wf.get("status") != "published":
            continue
        publicados += 1
        nome = wf.get("name") or os.path.basename(caminho)[:-5]
        for no in (wf.get("workflowData") or {}).get("templates") or []:
            a = no.get("attributes") or {}
            blob = json.dumps(a, ensure_ascii=False)
            if no.get("type") in ESCRITA:
                for campo in a.get("fields") or []:
                    if campo.get("field") in campos:
                        escreve[campo["field"]].add(nome)
                # math_operation usa `updateField`/`selectField`, nao `fields`
                for chave in ("updateField", "selectField"):
                    if a.get(chave) in campos:
                        escreve[a[chave]].add(nome)
                # merge field DENTRO do valor escrito e leitura, nao escrita
                for m in MERGE.findall(blob):
                    if m in chave2id:
                        le[chave2id[m]].add(nome)
            else:
                for i in campos:
                    if i in blob:
                        le[i].add(nome)
                for m in MERGE.findall(blob):
                    if m in chave2id:
                        le[chave2id[m]].add(nome)
    return escreve, le, publicados


def main():
    aviso(DUMPS)
    campos = inventario()
    if not campos:
        print("nenhum campo personalizado de contato em %s" % INVENTARIO)
        return 0
    escreve, le, publicados = varre(campos)
    print("%d campos personalizados de contato, %d workflows publicados lidos\n" % (
        len(campos), publicados))

    grupos = (
        ("NEM ESCRITO NEM LIDO por workflow — o que vale olhar",
         lambda i: not escreve.get(i) and not le.get(i)),
        ("so ESCRITO (a lista que leria talvez nao exista ainda — nao e orfao)",
         lambda i: escreve.get(i) and not le.get(i)),
        ("so LIDO (normal de campo que o SDR/closer preenche na tela)",
         lambda i: le.get(i) and not escreve.get(i)),
    )
    for titulo, cond in grupos:
        alvo = sorted((campos[i][0], i) for i in campos if cond(i))
        print("%s — %d:" % (titulo, len(alvo)))
        for nome, i in alvo:
            quem = escreve.get(i) or le.get(i) or set()
            extra = ("  <- %s" % ", ".join(sorted(quem))) if quem else ""
            print("   %-34s%s" % (nome, extra[:110]))
        print()
    fiados = sum(1 for i in campos if escreve.get(i) and le.get(i))
    print("%d campos com escrita E leitura em workflow (fiados dos dois lados)" % fiados)
    print("\nEste script nao falha de proposito: a maior parte do que ele lista e")
    print("intencional. Ler o docstring antes de tratar qualquer linha como defeito.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `... | head` fecha o pipe no meio. Sem isto o script morre com traceback
        # e um `exit=1` que parece falha de auditoria — justamente a confusao que
        # ele existe para nao causar.
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
