"""Listas inteligentes pela rota que o app usa (services.leadconnectorhq.com/contacts/smartlist),
com o bearer da sessão (ghl_interno). Descoberta em 27/09 criando uma lista pela tela."""
import json, urllib.request, urllib.error
import ghl_interno as g

SVC = "https://services.leadconnectorhq.com"


def sl(metodo, caminho, corpo=None):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(SVC + caminho, data=dados, method=metodo)
    for k, v in {"authorization": "Bearer " + g.bearer(), "accept": "application/json",
                 "channel": "APP", "source": "WEB_USER", "version": "2021-07-28",
                 "origin": "https://app.wesalescrm.com",
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"}.items():
        req.add_header(k, v)
    if dados:
        req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")[:600]
