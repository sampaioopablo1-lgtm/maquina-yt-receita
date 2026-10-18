"""Lista as reuniões marcadas no AgendouAI nos próximos 7 dias.

Uso (no seu computador, não aqui):
  1. pip install requests
  2. Defina a chave no terminal (nunca coloque a chave dentro do arquivo):
       Windows (PowerShell):  $env:AGENDOU_API_KEY="lk_..."
       Mac/Linux:             export AGENDOU_API_KEY="lk_..."
  3. python ferramentas/agendou_reunioes.py
"""
import os, sys, datetime as dt
import requests

KEY = os.environ.get("AGENDOU_API_KEY")
if not KEY:
    sys.exit("Defina AGENDOU_API_KEY antes de rodar (veja o topo do arquivo).")

BASE = "https://api.agendou.io/api/public/v1"
H = {"X-API-Key": KEY, "Content-Type": "application/json"}
hoje = dt.date.today()
r = requests.get(f"{BASE}/agendamentos", headers=H, timeout=30,
                 params={"data_inicio": hoje.isoformat(),
                         "data_fim": (hoje + dt.timedelta(days=7)).isoformat(),
                         "limit": 100})
r.raise_for_status()
itens = r.json().get("data", [])
if not itens:
    print("Nenhuma reunião nos próximos 7 dias.")
for a in itens:
    quando = a["data_hora"].replace("T", " ")[:16]
    print(f'{quando} | {a.get("cliente_nome","?")} | {a.get("cliente_telefone","")} | {a.get("status","")}')
print(f"\nTotal: {len(itens)}")
