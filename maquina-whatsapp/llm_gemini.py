"""Cérebro alternativo, grátis: Gemini 2.5 Flash (google-genai). Mesma interface de llm.reply.
Sem function calling: o link do Calendly vai no prompt e '#HUMANO' no texto devolve pro Pablo."""
import os, json, pathlib, datetime, urllib.parse
from google import genai
from google.genai import types
import memory

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
CALENDLY = os.environ["CALENDLY_URL"]
SYSTEM = pathlib.Path(__file__).with_name("prompt.md").read_text(encoding="utf-8") + f"""

# Ferramentas (versão sem function calling)
- Para marcar a reunião, mande este link exatamente como está, numa mensagem só: {CALENDLY}
- Para devolver a conversa pro Pablo, termine sua resposta com a palavra exata #HUMANO.
"""
LOG = pathlib.Path(__file__).with_name("leads.jsonl")


def _to_gemini(hist: list) -> list:
    out = []
    for m in hist:
        text = m["content"] if isinstance(m["content"], str) else " ".join(
            b.get("text", "") for b in m["content"] if isinstance(b, dict) and b.get("type") == "text")
        if text.strip():
            out.append({"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": text}]})
    return out


def reply(user: str, text: str) -> str:
    memory.append(user, "user", text)
    cfg = types.GenerateContentConfig(system_instruction=SYSTEM, max_output_tokens=1024)
    resp = _client.models.generate_content(model=MODEL, contents=_to_gemini(memory.get(user)), config=cfg)
    out = (resp.text or "").strip()
    memory.append(user, "assistant", out)
    if "#HUMANO" in out:
        memory.pause(user)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "tipo": "handoff", "whatsapp": user}, ensure_ascii=False) + "\n")
        out = out.replace("#HUMANO", "").strip()
    if CALENDLY in out:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "tipo": "reuniao_oferecida", "whatsapp": user}, ensure_ascii=False) + "\n")
    return out
