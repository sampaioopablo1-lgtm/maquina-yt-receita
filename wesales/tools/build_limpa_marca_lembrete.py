"""Tira a tag `lr-conf-agora` 2 h depois de posta pelo `Lembretes da Reunião v3`.
Enquanto ela existe, D-3/D-1 não saem: evita empilhar com a confirmação quando a
reunião foi marcada em cima da hora. Sem janela (só mexe em tag).
Uso: python build_limpa_marca_lembrete.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
TAG = "lr-conf-agora"
NOME = "Lembretes · limpa marca de confirmação (2 h)"
passos = [g.wait_step(2, "hours"), g.tag_step([TAG], remove=True)]
c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.preencher(c, wf, NOME, passos, [g.tag_trigger("Marca de confirmação", TAG)],
            allow_reentry=True, stop_on_response=False)
g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json", NOME + ".json"))
print("publicar:", g.publicar(c, wf), wf, NOME)
