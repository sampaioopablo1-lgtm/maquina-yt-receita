"""W18 - Monitor de Capacidade (IMPLEMENTACAO-WORKFLOWS.md, W18).

Um aviso ao gestor, seg-sex 11h e 15h: conferir se a fila do dia passou de
100 tarefas. O gatilho e `scheduler_trigger` (existe nesta conta, conferido
na tela em 22/09/2026) e entra depois, pela tela, porque o formato do
agendamento so se aprende gravando uma vez.

Usabilidade: o texto do aviso diz o que fazer e onde, sem exigir que o
gestor lembre de numero de lista ou de id.
"""
import ghl_api as g

NOME = "Monitor de Capacidade"

CORPO = ("Confira a fila de hoje: a meta é no máximo 100 tarefas por dia. "
         "Abra Contatos → Smart Lists → \"Fila do Dia — Total\". "
         "Se passou de 100, tire leads da cadência ou redistribua antes do "
         "fim do expediente.")

passos = [
    dict(g.notify_user_step("Fila do dia — conferir capacidade", CORPO),
         name="Avisar o gestor para conferir a fila do dia"),
]

if __name__ == "__main__":
    c = g.client()
    ja = [w for w in c.request("GET", "/workflow/" + g.LOC) if w.get("name") == NOME]
    if ja:
        raise SystemExit("ja existe '%s' (%s) - nao duplico" % (NOME, ja[0]["id"]))
    wf = g.build(c, NOME, passos, [], allow_reentry=True, stop_on_response=False)
    doc = g.export(c, wf, "../workflows-json/" + NOME + ".json")
    print("criado", wf, "status", doc["workflow"].get("status"),
          "nos", len(doc["workflow"]["workflowData"]["templates"]))
