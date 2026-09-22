"""Prova que a regua de qualificacao soma certo, sem depender de agendamento.

O `Pós-agendamento v2` so dispara com mudanca de status de agendamento, que
a API nao cria. Entao a regua e montada sozinha num workflow de teste com
gatilho de tag, disparada num contato de valores conhecidos, e o resultado
e comparado com a conta feita na mao.

Uso:
  python teste_regua.py montar    -> cria e publica o workflow de teste
  python teste_regua.py esperar   -> mostra a nota que DEVERIA sair
  python teste_regua.py conferir  -> le a nota que saiu e compara
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
import regua_qualificacao as rq

NOME = "ZZ TESTE REGUA"
TAG = "teste-regua"
CONTATO = "Lj96CIFYaGKPiC0opzbc"          # Teste Atendeu
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
NOTA = C["Nota de qualificação"]["id"]

acao = sys.argv[1] if len(sys.argv) > 1 else "montar"
c = g.client()

if acao == "montar":
    c.create_location_tag(TAG)
    fim = g.note_step("Régua rodou",
                      "Nota calculada: " + g.token("contact.nota_de_qualificao"))
    passos = rq.montar_regua(C, NOTA, fim["id"], fim_node=fim)
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
           if w.get("type") == "workflow"}
    wf = ids.get(NOME) or g.create_workflow(c, NOME)
    g.preencher(c, wf, NOME, passos, [g.tag_trigger("Teste Regua", TAG)],
                allow_reentry=True)
    print("nos=%d" % len(g.montar(passos)))
    print("publicado" if g.publicar(c, wf) else "NAO PUBLICOU")
    print("agora aplique a tag '%s' no contato de teste" % TAG)

elif acao in ("esperar", "conferir"):
    from urllib.request import urlopen  # noqa: F401  (so para deixar claro)
    print("leia o contato pelo conector e rode a conta:")
    print("  contato:", CONTATO)
    print("  campo da nota:", NOTA)
    print()
    print("tabela da régua (campo -> valor: pontos):")
    for rotulo, opcoes in rq.REGUA:
        print("  %-34s %s" % (rotulo,
                              "  ".join("%s=%d" % (v, p) for v, p in opcoes)))
