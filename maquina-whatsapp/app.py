"""Webhook da WhatsApp Cloud API → buffer → Claude → resposta. Fluxo inteiro em ~80 linhas."""
import os, hmac, hashlib, threading
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, abort, send_from_directory
import whatsapp, buffer, memory
# Cérebro: Gemini (grátis) se houver GEMINI_API_KEY; senão Claude.
if os.environ.get("GEMINI_API_KEY"):
    import llm_gemini as llm
else:
    import llm

app = Flask(__name__)
VERIFY = os.environ["WA_VERIFY_TOKEN"]
APP_SECRET = os.environ.get("WA_APP_SECRET", "")
OWNER = os.environ.get("OWNER_WHATSAPP", "")


@app.get("/conectar")
def conectar():
    return send_from_directory("static", "conectar.html")


@app.get("/webhook")
def verify():
    if request.args.get("hub.verify_token") == VERIFY:
        return request.args.get("hub.challenge", ""), 200
    abort(403)


def _signed_ok() -> bool:
    if not APP_SECRET:
        return True
    sig = request.headers.get("X-Hub-Signature-256", "").removeprefix("sha256=")
    mac = hmac.new(APP_SECRET.encode(), request.get_data(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, mac)


def _on_flush(user: str, text: str) -> None:
    try:
        answer = llm.reply(user, text)
        if answer:
            whatsapp.send_split(user, answer)
        if memory.is_paused(user) and OWNER:
            whatsapp.send_text(OWNER, f"Conversa devolvida pra você: wa.me/{user}\nÚltima mensagem: {text[:200]}")
    except Exception as e:  # nunca deixar o webhook morrer
        print("erro no flush", user, repr(e))


@app.post("/webhook")
def receive():
    if not _signed_ok():
        abort(403)
    body = request.get_json(silent=True) or {}
    for entry in body.get("entry", []):
        for ch in entry.get("changes", []):
            v = ch.get("value", {})
            for m in v.get("messages", []):
                # só texto, só conversa individual, só o que não é eco do próprio número
                if m.get("type") != "text" or "group" in m.get("from", ""):
                    continue
                user, mid, text = m["from"], m["id"], m["text"]["body"]
                if memory.is_paused(user):
                    continue  # devolvido pro Pablo: a IA não responde mais
                threading.Thread(target=whatsapp.mark_read_and_typing, args=(mid,), daemon=True).start()
                buffer.push(user, text, _on_flush)
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
