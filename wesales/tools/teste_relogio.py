"""Mede qual variavel de data/hora o GHL preenche num campo TEXT.

A regua publicada grava a string 'sim' em `Entrada em` / `1a tentativa em`,
nao a hora (APRENDIZADOS 22/09). Antes de trocar por {{right_now...}},
medir. Grava candidatas no C-14 (`Data e hora do sinal`, nenhum workflow
ativo usa) do contato de teste, via tag `teste-relogio`.

Uso:
  python teste_relogio.py montar    -> cria e publica o workflow de teste
  depois aplique a tag `teste-relogio` no contato de teste e leia o C-14
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "ZZ TESTE RELOGIO"
TAG = "teste-relogio"
CONTATO = "Lj96CIFYaGKPiC0opzbc"          # Teste Atendeu
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
C14 = C["Data e hora do sinal"]["id"]
VALOR = ("A={{right_now}} | B={{right_now.date}} | "
         "C={{right_now.year}}-{{right_now.month}}-{{right_now.day}} "
         "{{right_now.hour}}:{{right_now.minute}} | "
         "D={{right_now.day_of_week}} | E={{right_now.time}}")

if __name__ == "__main__":
    c = g.client()
    c.create_location_tag(TAG)
    passos = [g.field_step(C14, "Data e hora do sinal", VALOR, "text")]
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    wf = ids.get(NOME) or g.create_workflow(c, NOME)
    g.preencher(c, wf, NOME, passos, [g.tag_trigger("Teste Relogio", TAG)],
                allow_reentry=True)
    print("wf", wf, "publicado" if g.publicar(c, wf) else "NAO PUBLICOU")
