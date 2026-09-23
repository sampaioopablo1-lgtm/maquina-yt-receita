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
# Tags que NAO nascem de workflow por decisao de projeto — nao acusar na
# pergunta 2 como "ninguem aplica". Fonte: IMPLEMENTACAO-WORKFLOWS.md, tabela
# das tres familias ("exceto `pausado` (SDR, a mao) e `cad-inbound`
# (integracao/formulario)").
NASCEM_FORA = {"pausado", "cad-inbound"}

# Tags cuja limpeza pulada NAO e alarme na pergunta 1, porque persistir e o
# ponto delas. Lista curta de proposito.
#
# CUIDADO — `cad-inbound` SAIU desta lista em 23/09/2026. Eu a tinha posto aqui
# raciocinando "marcador de origem que persiste nao e defeito". O papel da tag
# mudou no `bff2514`: o no 0 da `Cadencia Inbound` e um `if_else` que TESTA
# `cad-inbound`, ou seja, ela virou a tag de PORTAO da cadencia, e o no 254 a
# remove na saida. Remocao de portao pulada nao e inofensiva. E o F-16 de novo:
# quando o papel de uma tag muda, todo julgamento antigo sobre ela vence.
PERSISTIR_E_O_PONTO = {"pausado"}


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


def frescor():
    """Para cada dump vivo, diz se existe backup `_antes-*` MAIS NOVO que ele.

    Se existe, o dump esta velho: alguem aplicou patch na conta e exportou o
    backup sem re-exportar o arquivo principal. Achado tirado de dump velho e
    achado de mentira — foi o que aconteceu em 23/09/2026, quando esta auditoria
    reportou 5 tags sem segunda rede e 3 delas ja estavam resolvidas na conta
    (a `Triagem da Nutricao` tinha sido publicada as 03:24 e o dump dela ainda
    dizia `draft`).
    """
    atraso = {}
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        nome = os.path.basename(caminho)
        try:
            with open(caminho, encoding="utf-8") as fh:
                meu = (json.load(fh).get("workflow") or {}).get("updatedAt") or ""
        except (ValueError, OSError):
            continue
        mais_novo = ""
        for backup in glob.glob(os.path.join(DUMPS, "_antes-*", nome)):
            try:
                with open(backup, encoding="utf-8") as fh:
                    u = (json.load(fh).get("workflow") or {}).get("updatedAt") or ""
            except (ValueError, OSError):
                continue
            if u > mais_novo:
                mais_novo = u
        if mais_novo and mais_novo > meu:
            atraso[nome[:-5]] = (meu, mais_novo)
    return atraso


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

    atraso = frescor()
    if atraso:
        print("=" * 72)
        print("AVISO DE FRESCOR — %d dump(s) com backup `_antes-*` MAIS NOVO que eles." % len(atraso))
        print("O arquivo principal nao foi re-exportado depois de um patch na conta.")
        print("QUALQUER achado abaixo que envolva estes workflows pode ja estar resolvido:")
        for nome, (meu, novo) in sorted(atraso.items()):
            print("   %-34s dump %s  <  backup %s" % (nome, meu[:19], novo[:19]))
        print("Conferir ao vivo antes de reportar. Em 23/09/2026 esta auditoria")
        print("reportou 5 tags sem segunda rede e 3 ja estavam resolvidas por isto.")
        print("=" * 72 + "\n")

    # ---- PERGUNTA 1 ----
    print("PERGUNTA 1 — limpeza de tag pulada por `remove_from_workflow`")
    print("(nos de saida do alvo nao rodam quando um terceiro arranca o contato)\n")
    graves = []
    for tag in sorted(limpa):
        if tag in PERSISTIR_E_O_PONTO:
            continue
        donos = limpa[tag]
        expostos = sorted(w for w in donos if arranca.get(w))
        if not expostos:
            continue
        # Segunda rede = existe removedor que ninguem arranca E QUE ESTA NO AR.
        # Duas correcoes que custaram alarme errado:
        #  - nao basta procurar o "Mestre de saida" pelo nome: o `toque` e limpo
        #    pelo Contador de Toques, que e rede legitima (alarme falso, 23/09);
        #  - removedor em `draft` NAO e rede: em 23/09 o script deixou de acusar
        #    `nutricao-90d` e `cad-inbound` porque quem as limpa e a `Triagem da
        #    Nutricao`, que esta em rascunho. Rede que nao esta publicada nao
        #    salva ninguem, e o resultado foi a auditoria ficar PERMISSIVA, que e
        #    o pior jeito de errar.
        # Nota sobre `draft`: aqui ele nao serve para ACUSAR (isso e a armadilha
        # do F-17), so para NAO CREDITAR uma rede. Direcao segura.
        livres = [w for w in donos if not arranca.get(w)]
        tem_rede = any(status(w) == "published" for w in livres)
        rede_em_rascunho = [w for w in livres if status(w) != "published"]
        for w in expostos:
            quem = sorted(arranca[w], key=nome)
            marca = "" if tem_rede else "   <<< SEM SEGUNDA REDE NO AR"
            print("  %-22s limpa em %-26s [%s]%s" % (tag, nome(w), status(w), marca))
            for outro in quem:
                print("      arrancado por: %s [%s]" % (nome(outro), status(outro)))
            if not tem_rede and rede_em_rascunho:
                print("      vira rede quando publicarem: %s" % ", ".join(
                    "%s [%s]" % (nome(r), status(r)) for r in rede_em_rascunho))
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
        if tag in NASCEM_FORA:
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
        if tag in NASCEM_FORA or aplica.get(tag):
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
        print("%d tag(s) com limpeza pulada E sem segunda rede NO AR — conferir na tela:" % len(graves))
        for tag, onde in graves:
            print("   %s (limpa em %s)" % (tag, onde))
        return 1
    print("nenhuma tag com limpeza pulada sem segunda rede no ar")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `... | head` fecha o pipe. Sem esta guarda o script morre com traceback
        # e exit=1, que parece falha de auditoria — a confusao que ele evita.
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
