"""Cliente uazapi: os 3 endpoints do MVP. Em erro HTTP, print curto e segue."""
import os, requests

BASE = os.environ["UAZAPI_BASE_URL"].rstrip("/")
H = {"token": os.environ["UAZAPI_INSTANCE_TOKEN"], "Content-Type": "application/json"}


def _call(method: str, path: str, body: dict) -> None:
    try:
        r = requests.request(method, f"{BASE}{path}", json=body, headers=H, timeout=20)
        if r.status_code >= 400:
            print(f"[uazapi] {method} {path} -> {r.status_code}")
    except requests.RequestException as e:
        print(f"[uazapi] {method} {path} falhou: {type(e).__name__}")


def send_text(number: str, text: str) -> None:
    _call("POST", "/send/text", {"number": number, "text": text, "linkPreview": True})


def send_presence(number: str, presence: str) -> None:
    _call("POST", "/send/presence", {"number": number, "presence": presence})


def mark_read(number: str, message_id: str) -> None:
    _call("PUT", "/send/read", {"number": number, "messageId": message_id})
