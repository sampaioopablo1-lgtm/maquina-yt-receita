#!/usr/bin/env python3
"""Quantos dias faltam para vencer a sessão guardada em GHL_STORAGE_STATE.

O token de renovação da sessão do WeSales NÃO renova com o uso (medido em 28/09: mesma
validade antes e depois do acesso), então a cada ~30 dias o dono precisa logar de novo.
Imprime os dias restantes e sai com código 3 quando faltam 10 dias ou menos — a Action usa
isso para abrir um aviso (issue) no GitHub, que chega por e-mail. Nunca imprime a sessão.
"""
import base64
import datetime as dt
import json
import os
import sys

s = json.loads(os.environ.get("GHL_STORAGE_STATE") or "{}")
itens = [i for o in s.get("origins", []) for i in o.get("localStorage", [])] + s.get("cookies", [])
exp = None
for i in itens:
    if i.get("name") == "refresh-token-v2" and str(i.get("value", "")).count(".") == 2:
        p = i["value"].split(".")[1]
        p += "=" * (-len(p) % 4)
        exp = json.loads(base64.urlsafe_b64decode(p)).get("exp")
        break
if not exp:
    print("sem sessão legível em GHL_STORAGE_STATE")
    sys.exit(3)
dias = (dt.datetime.fromtimestamp(exp, dt.timezone.utc) - dt.datetime.now(dt.timezone.utc)).days
print("sessão do WeSales vence em %d dias (%s UTC)" % (dias, dt.datetime.fromtimestamp(exp, dt.timezone.utc).strftime("%d/%m/%Y")))
sys.exit(3 if dias <= 10 else 0)
