"""F-16 / G-11 (A7): a tag `conectado-hoje` (posta pelo Pos-ligacao v2 no
Atendeu) nunca era removida -> quem atendia uma vez sumia da "Fila Telefone
Hoje" para sempre. Saida A da secao 2.31, num workflow a parte (sem mexer no
Pos-ligacao v2): tag adicionada -> espera 1 dia -> remove a tag.
Sem janela (nao cria tarefa nem mensagem; tirar a tag de madrugada e inofensivo).
Uso: python build_limpa_conectado.py [--so-montar]
     TESTE=1 -> copia "ZZ TESTE Limpa conectado-hoje" com espera de 2 min"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

TESTE = os.environ.get("TESTE") == "1"
TAG = "conectado-hoje"
NOME = ("ZZ TESTE " if TESTE else "") + "Limpa conectado-hoje (24 h)"
passos = [g.wait_step(2, "minutes") if TESTE else g.wait_step(1, "days"),
          g.tag_step([TAG], remove=True)]
if "--so-montar" in sys.argv:
    print(len(g.montar(passos)), "nós"); sys.exit(0)
c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.preencher(c, wf, NOME, passos, [g.tag_trigger("Conectado hoje", TAG)],
            allow_reentry=True, stop_on_response=False)
g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json", NOME + ".json"))
print("publicar:", g.publicar(c, wf), wf, NOME)
