#!/usr/bin/env python3
"""
Manda para a Meta o evento "Schedule" (reuniao agendada) de cada lead que virou
reuniao, para a campanha aprender a perseguir quem agenda — nao quem so preenche.

Uso:
    META_ACCESS_TOKEN=... python3 enviar_reuniao.py '<json com a lista>'

Formato esperado no argumento:
    [{"email":"...","telefone":"21999999999","quando":1789012345,
      "nome":"Andre","valor":2000}]

`quando` e o horario em que a reuniao FOI AGENDADA (nao o horario da reuniao),
em segundos. A Meta so aceita evento com ate 7 dias de idade.
"""
import hashlib
import json
import os
import sys
import urllib.request

DATASET = "1600846091439175"
API = "https://graph.facebook.com/v21.0"


def digerir(texto):
    """A Meta so aceita dado pessoal criptografado. Normaliza e aplica SHA-256."""
    if not texto:
        return None
    return hashlib.sha256(texto.strip().lower().encode("utf-8")).hexdigest()


def telefone_e164(numero):
    """21980417915 -> 5521980417915. So digitos, com codigo do pais."""
    so_digitos = "".join(c for c in str(numero) if c.isdigit())
    if not so_digitos:
        return None
    if not so_digitos.startswith("55"):
        so_digitos = "55" + so_digitos
    return so_digitos


def montar(pessoa):
    dados = {}
    if pessoa.get("email"):
        dados["em"] = [digerir(pessoa["email"])]
    if pessoa.get("telefone"):
        dados["ph"] = [digerir(telefone_e164(pessoa["telefone"]))]
    if pessoa.get("nome"):
        dados["fn"] = [digerir(pessoa["nome"].split()[0])]
    dados["country"] = [digerir("br")]

    evento = {
        "event_name": "Schedule",
        "event_time": int(pessoa["quando"]),
        "action_source": "business_messaging",
        "event_id": f"reuniao-{digerir(pessoa.get('email') or pessoa['telefone'])[:16]}",
        "user_data": dados,
    }
    if pessoa.get("valor"):
        evento["custom_data"] = {"value": float(pessoa["valor"]), "currency": "BRL"}
    return evento


def main():
    token = os.environ.get("META_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta META_ACCESS_TOKEN no ambiente.")
    if len(sys.argv) < 2:
        sys.exit("Falta a lista de pessoas em JSON como argumento.")

    pessoas = json.loads(sys.argv[1])
    eventos = [montar(p) for p in pessoas]

    corpo = json.dumps({"data": eventos}).encode("utf-8")
    req = urllib.request.Request(
        f"{API}/{DATASET}/events?access_token={token}",
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        resposta = json.loads(r.read())

    print(json.dumps(resposta, indent=2, ensure_ascii=False))
    recebidos = resposta.get("events_received", 0)
    if recebidos != len(eventos):
        sys.exit(f"Enviei {len(eventos)} e a Meta recebeu {recebidos}. Conferir.")


if __name__ == "__main__":
    main()
