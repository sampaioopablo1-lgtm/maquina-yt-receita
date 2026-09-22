"""W20 - Qualidade da Conexao (IMPLEMENTACAO-WORKFLOWS.md, W20; F-06).

Nos pela API interna, RASCUNHO. O gatilho `Transcript Generated` e de
marketplace (`transcript_generated`) e entra pela tela (add_trigger_w20.js):
Tipo = Ligacoes, Direcao = Saida. Por isso o no 1 da spec (If/Else de
direcao) sai - a spec preve isso ("se o gatilho oferecer o filtro").

Variavel de duracao lida do catalogo do builder:
customVarPrefix `transcript_generated`, reference `call_duration` (numerical).
"""
import ghl_api as g

DURACAO = "PLjkuvnoDk7Hvt4qv0a8"     # C-29 Duracao da ligacao
CONEXAO_REAL = "7wtFfDDxOpYCfHzBsZXP"  # C-30 Conexao real (Sim/Nao)
REAIS_TEL = "2BSLMqty4LEwdoyNTdU8"     # C-31 Conexoes reais telefone
COM_TRANSC = "JejovPl6Vf0SBtAiVIpw"    # C-32 Ligacoes com transcricao

NOME = "Qualidade da Conexão"

passos = [
    g.field_step(DURACAO, "Duração da ligação",
                 "{{transcript_generated.call_duration}}", "numerical"),
    g.math_step(COM_TRANSC, "+", 1),
    g.Branch("Duração ≥ 60s?",
             [g.cond("contact_detail", DURACAO, ">=", "60")],
             sim=[g.field_step(CONEXAO_REAL, "Conexão real", "Sim", "select"),
                  g.math_step(REAIS_TEL, "+", 1)],
             nao=[g.field_step(CONEXAO_REAL, "Conexão real", "Não", "select")]),
]

if __name__ == "__main__":
    c = g.client()
    ja = [w for w in c.request("GET", "/workflow/" + g.LOC) if w.get("name") == NOME]
    if ja:
        raise SystemExit("ja existe '%s' (%s) - nao duplico" % (NOME, ja[0]["id"]))
    wf = g.build(c, NOME, passos, [], allow_reentry=True, stop_on_response=False)
    doc = g.export(c, wf, "../workflows-json/" + NOME + ".json")
    tpl = doc["workflow"]["workflowData"]["templates"]
    print("criado", wf, "status", doc["workflow"].get("status"), "nos", len(tpl))
    for t in tpl:
        print("  ", t.get("type"), "|", t.get("name"))
