#!/usr/bin/env python3
"""Auditoria do ciclo de vida das tags de estado (somente leitura).

Duas perguntas que acharam defeito real em 23/09/2026, viradas em checagem
fixa. Ambas sao mecanicas, ambas silenciosas quando falham.

PERGUNTA 1 — quem limpa a tag e alcancado?
  `remove_from_workflow` CANCELA os passos pendentes do contato no workflow
  alvo: os nos de saida do alvo NAO rodam. Logo toda tag cuja limpeza mora
  DENTRO de um workflow e permanente para quem sai por remocao externa.
  Foi assim que `fechar-horario` sobreviveu a quem agenda (secao 2.31.2 do
  build-wesales.md): o `Pos-agendamento v2` arranca o contato do
  `Fechar Horario` no no 4, e os 4 `Remove Tag` dele nunca rodam.
  Agravante que o relatorio mostra: tag limpa por UM unico workflow nao tem
  segunda rede. Tag que o `Mestre de saida` tambem limpa tem.

PERGUNTA 2 — quem aplica a tag esta no ar antes de quem a testa?
  Workflow publicado que testa uma tag que so um rascunho aplica le a tag
  como ausente e desce pelo ramo errado, sem erro nenhum.

  CUIDADO, e esta e a licao mais caduca deste arquivo: `status: draft` num
  dump e a afirmacao mais fragil que existe aqui. `draft` e o estado natural
  de um workflow nos segundos entre montar e publicar — exatamente a janela em
  que os scripts de wesales/tools/ exportam. Em 23/09 eu registrei um defeito
  inteiro (F-17) lendo um dump exportado 4 SEGUNDOS antes da publicacao. Por
  isso a pergunta 2 sai como PERGUNTA, nunca como falha, e nunca muda o codigo
  de saida: conferir na tela ou medindo o efeito ao vivo (contar contatos com a
  tag) antes de registrar qualquer coisa.

Limite honesto, igual ao do auditoria_refs.py: le os dumps de
`wesales/workflows-json/`, que podem estar defasados em relacao a conta — um
patch aplicado ao vivo sem re-export deixa o arquivo descrevendo o estado
anterior. Compare com o backup irmao em `_antes-*/` antes de concluir; se
forem identicos em `updatedAt`, o dump nao responde nada.

Uso:  python3 wesales/tools/auditoria_tags.py
Sai com codigo 1 so na pergunta 1, e so quando a tag nao tem segunda rede.
"""
import glob
import json
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
# Tags que NAO nascem de workflow por decisao de projeto — nao acusar como
# "ninguem aplica". Fonte: IMPLEMENTACAO-WORKFLOWS.md, tabela das tres familias
# ("exceto `pausado` (SDR, a mao) e `cad-inbound` (integracao/formulario)").
FORA_DO_WORKFLOW = {"pausado", "cad-inbound"}


def ids_alvo(atributos):
    """Ids de workflow citados por um no de remove/add_to_workflow.

    O payload do GHL usa `workflow_id` (lista). Os outros nomes ficam por
    tolerancia — se a chave mudar, o no aparece em vez de desaparecer calado.
    """
    for chave in ("workflow_id", "workflows", "workflow", "workflowIds", "selectedWorkflows"):
        valor = atributos.get(chave)
        if valor:
            itens = valor if isinstance(valor, list) else [valor]
            return [x if isinstance(x, str) else (x.get("id") or x.get("value")) for x in itens]
    return []


def carrega():
    """Um registro por dump vivo: nome, status, id e os nos."""
    vivos = {}
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        wf = dado.get("workflow") or dado
        wid = wf.get("id")
        if not wid:
            continue
        vivos[wid] = {
            "nome": wf.get("name") or os.path.basename(caminho)[:-5],
            "status": wf.get("status"),
            "atualizado": wf.get("updatedAt"),
            "nos": (wf.get("workflowData") or {}).get("templates") or [],
        }
    return vivos


def mapeia(vivos):
    aplica = defaultdict(set)     # tag -> {wid que aplica}
    limpa = defaultdict(set)      # tag -> {wid que remove}
    testa = defaultdict(set)      # tag -> {wid que le em condicao}
    arranca = defaultdict(set)    # wid alvo -> {wid que arranca o contato}
    for wid, w in vivos.items():
        for no in w["nos"]:
            atributos = no.get("attributes") or {}
            tipo = no.get("type")
            if tipo == "add_contact_tag":
                for tag in atributos.get("tags") or []:
                    aplica[tag].add(wid)
            elif tipo == "remove_contact_tag":
                for tag in atributos.get("tags") or []:
                    limpa[tag].add(wid)
            elif tipo == "remove_from_workflow":
                for alvo in ids_alvo(atributos):
                    if alvo and alvo != wid:      # auto-remocao nao conta: roda depois da limpeza
                        arranca[alvo].add(wid)
            else:
                blob = json.dumps(atributos, ensure_ascii=False)
                for tag in set(list(aplica) + list(limpa)):
                    if '"%s"' % tag in blob:
                        testa[tag].add(wid)
    # segunda passada: condicoes que citam tag que nenhum no aplica/remove
    conhecidas = set(aplica) | set(limpa)
    for wid, w in vivos.items():
        for no in w["nos"]:
            if no.get("type") in ("add_contact_tag", "remove_contact_tag", "remove_from_workflow"):
                continue
            blob = json.dumps(no.get("attributes") or {}, ensure_ascii=False)
            for tag in conhecidas:
                if '"%s"' % tag in blob:
                    testa[tag].add(wid)
    return aplica, limpa, testa, arranca


def main():
    vivos = carrega()
    if not vivos:
        print("nenhum dump encontrado em %s" % DUMPS)
        return 0
    aplica, limpa, testa, arranca = mapeia(vivos)
    nome = lambda wid: vivos[wid]["nome"]
    status = lambda wid: vivos[wid]["status"]

    print("%d workflows com dump (%d publicados)\n" % (
        len(vivos), sum(1 for w in vivos.values() if w["status"] == "published")))

    # ---- PERGUNTA 1 ----
    print("PERGUNTA 1 — limpeza de tag pulada por `remove_from_workflow`")
    print("(nos de saida do alvo nao rodam quando um terceiro arranca o contato)\n")
    graves = []
    for tag in sorted(limpa):
        if tag in FORA_DO_WORKFLOW:
            # Marcador de origem que persiste nao e defeito: `cad-inbound` diz de
            # onde o lead veio, e isso nao expira. `pausado` e do SDR. Limpeza
            # pulada nessas duas nao vira alarme.
            continue
        donos = limpa[tag]
        expostos = sorted(w for w in donos if arranca.get(w))
        if not expostos:
            continue
        # Segunda rede = existe algum removedor que NINGUEM arranca. A limpeza
        # dele sempre roda, entao a tag tem por onde sair. Nao basta procurar o
        # "Mestre de saida" pelo nome: o `toque`, por exemplo, e limpo pelo
        # Contador de Toques, que e rede legitima.
        tem_rede = any(not arranca.get(w) for w in donos)
        for w in expostos:
            quem = sorted(arranca[w], key=nome)
            marca = "" if tem_rede else "   <<< SEM SEGUNDA REDE"
            print("  %-22s limpa em %-26s [%s]%s" % (tag, nome(w), status(w), marca))
            for outro in quem:
                print("      arrancado por: %s [%s]" % (nome(outro), status(outro)))
            if not tem_rede:
                graves.append((tag, nome(w)))
    if not any(arranca.get(w) for donos in limpa.values() for w in donos):
        print("  nenhuma tag nesta situacao")

    # ---- PERGUNTA 2 ----
    print("\nPERGUNTA 2 — aplicador atras do consumidor (PERGUNTA, nunca falha)")
    print("`draft` num dump vale 'no momento do export'. Confirmar na tela ou")
    print("contando contatos com a tag antes de registrar qualquer coisa.\n")
    perguntas = 0
    for tag in sorted(testa):
        if tag in FORA_DO_WORKFLOW:
            continue
        consumidores = [w for w in testa[tag] if status(w) == "published"]
        produtores = aplica.get(tag) or set()
        if not consumidores or not produtores:
            continue
        if not any(status(w) == "published" for w in produtores):
            perguntas += 1
            print("  %-22s aplicada so por %s" % (
                tag, ", ".join("%s [%s]" % (nome(w), status(w)) for w in sorted(produtores, key=nome))))
            print("      testada por %d publicado(s): %s" % (
                len(consumidores), ", ".join(sorted(nome(w) for w in consumidores))))
    if not perguntas:
        print("  nenhuma pergunta aberta")

    # ---- PERGUNTA 3 ----
    print("\nPERGUNTA 3 — tag so removida, nunca aplicada (no-op e lista que nao enche)")
    print("Nao e bug de workflow: e peca de desenho antigo que sobrou. Cada linha")
    print("aqui e uma decisao — tirar os nos, ou voltar a aplicar a tag.\n")
    orfas = 0
    for tag in sorted(limpa):
        if tag in FORA_DO_WORKFLOW or aplica.get(tag):
            continue
        onde = sorted(limpa[tag], key=nome)
        nos = sum(1 for w in onde for no in vivos[w]["nos"]
                  if no.get("type") == "remove_contact_tag"
                  and tag in ((no.get("attributes") or {}).get("tags") or []))
        orfas += 1
        print("  %-22s removida em %d no(s), %d workflow(s); aplicada em NENHUM" % (tag, nos, len(onde)))
        print("      %s" % ", ".join("%s [%s]" % (nome(w), status(w)) for w in onde))
    if not orfas:
        print("  nenhuma tag nesta situacao")

    print()
    if graves:
        print("%d tag(s) com limpeza pulada E sem segunda rede — conferir na tela:" % len(graves))
        for tag, onde in graves:
            print("   %s (limpa em %s)" % (tag, onde))
        return 1
    print("nenhuma tag com limpeza pulada sem segunda rede")
    return 0


if __name__ == "__main__":
    sys.exit(main())
