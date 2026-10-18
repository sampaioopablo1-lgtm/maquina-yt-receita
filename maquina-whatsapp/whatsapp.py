"""Cliente mínimo da WhatsApp Cloud API (oficial). Só o que o agente usa."""
import os, time, requests

GRAPH = "https://graph.facebook.com/v22.0"
TOKEN = os.environ["WA_TOKEN"]
PHONE_ID = os.environ["WA_PHONE_NUMBER_ID"]
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def _post(payload: dict) -> dict:
    r = requests.post(f"{GRAPH}/{PHONE_ID}/messages", json=payload, headers=H, timeout=30)
    if r.status_code >= 400:
        print("WA erro", r.status_code, r.text)
    return r.json() if r.content else {}


def send_text(to: str, text: str) -> dict:
    return _post({"messaging_product": "whatsapp", "to": to, "type": "text",
                  "text": {"preview_url": True, "body": text}})


def mark_read_and_typing(message_id: str) -> None:
    """Marca como lida e mostra 'digitando…' (a Cloud API aceita os dois no mesmo pedido)."""
    _post({"messaging_product": "whatsapp", "status": "read", "message_id": message_id,
           "typing_indicator": {"type": "text"}})


def send_split(to: str, reply: str) -> None:
    """Quebra por parágrafo e envia como mensagens separadas, com pausa proporcional."""
    parts = [p.strip() for p in reply.split("\n\n") if p.strip()]
    for p in parts:
        send_text(to, p)
        time.sleep(min(4, 1 + len(p) / 200))
