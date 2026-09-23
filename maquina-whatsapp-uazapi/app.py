"""uazapi -> buffer -> Gemini -> respostas fatiadas com 'digitando'. Tudo síncrono, threading."""
import os, time, pathlib
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
import uazapi, memory
from buffer import MessageBuffer
import llm

app = Flask(__name__)
CALENDLY = os.environ.get("CALENDLY_URL", "")
OWNER = os.environ.get("OWNER_NUMBER", "")
SYSTEM = pathlib.Path(__file__).with_name("prompt.md").read_text(encoding="utf-8").replace("{{CALENDLY_URL}}", CALENDLY)


def split_reply(text: str) -> list[str]:
    out = []
    for p in text.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        if len(p) <= 800:
            out.append(p)
            continue
        buf = ""
        for s in p.split(". "):
            s = s if s.endswith(".") else s + "."
            if len(buf) + len(s) > 800 and buf:
                out.append(buf.strip()); buf = ""
            buf += s + " "
        if buf.strip():
            out.append(buf.strip())
    return out


def handle_flush(user: str, texts: list[str]) -> None:
    try:
        uazapi.send_presence(user, "composing")
        memory.append(user, "user", "\n".join(texts))
        reply = llm.generate_reply(memory.get(user), SYSTEM)
        memory.append(user, "model", reply)
        handoff = "#HUMANO" in reply
        reply = reply.replace("#HUMANO", "").strip()
        for chunk in split_reply(reply):
            uazapi.send_presence(user, "composing")
            time.sleep(1 + len(chunk) / 200)
            uazapi.send_text(user, chunk)
        uazapi.send_presence(user, "paused")
        if handoff:
            memory.pause(user)
            if OWNER:
                uazapi.send_text(OWNER, f"Conversa devolvida pra você: wa.me/{user}\nÚltima mensagem: {' | '.join(texts)[:200]}")
    except Exception as e:
        print(f"[flush] erro user={user} {type(e).__name__}")


buffer = MessageBuffer(float(os.environ.get("BUFFER_SECONDS", "8")), handle_flush)


@app.get("/")
def health():
    return "ok"


@app.post("/webhook")
def webhook():
    payload = request.get_json(silent=True) or {}
    if payload.get("event") != "message":
        return jsonify(ok=True)
    d = payload.get("data") or {}
    if d.get("fromMe") or d.get("isGroup") or d.get("type") != "text" or not d.get("body"):
        return jsonify(ok=True)
    number = str(d.get("from", "")).split("@")[0]
    if not number or memory.is_paused(number):
        return jsonify(ok=True)
    uazapi.mark_read(number, d.get("id", ""))
    buffer.add(number, d["body"])
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
