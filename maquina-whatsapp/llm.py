"""Cérebro: Claude com duas ferramentas. Loop manual, curto, sem abstração."""
import os, json, pathlib, urllib.parse, datetime
import anthropic
import memory

client = anthropic.Anthropic()
MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5")
CALENDLY = os.environ["CALENDLY_URL"]
SYSTEM = pathlib.Path(__file__).with_name("prompt.md").read_text(encoding="utf-8")
LOG = pathlib.Path(__file__).with_name("leads.jsonl")

TOOLS = [
    {
        "name": "agendar_reuniao",
        "description": "Gera o link de agendamento do diagnóstico para este contato, já com nome preenchido. Chame só quando a pessoa for o cliente certo e tiver aceitado marcar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {"type": "string"},
                "empresa": {"type": "string"},
                "resumo": {"type": "string", "description": "Uma linha: negócio, bairro, se anuncia, dor principal."},
            },
            "required": ["nome", "empresa", "resumo"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "name": "passar_para_humano",
        "description": "Devolve a conversa para o Pablo e para de responder. Use nas situações do roteiro.",
        "input_schema": {
            "type": "object",
            "properties": {"motivo": {"type": "string"}},
            "required": ["motivo"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def _log(kind: str, user: str, data: dict) -> None:
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "tipo": kind, "whatsapp": user, **data}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _run_tool(user: str, name: str, inp: dict) -> tuple[str, bool]:
    """Devolve (resultado_para_o_modelo, encerrar_conversa)."""
    if name == "agendar_reuniao":
        q = urllib.parse.urlencode({"name": inp["nome"], "a1": user})
        link = f"{CALENDLY}?{q}"
        _log("reuniao_oferecida", user, {**inp, "link": link})
        return json.dumps({"link": link}), False
    if name == "passar_para_humano":
        memory.pause(user)
        _log("handoff", user, inp)
        return json.dumps({"ok": True}), True
    return json.dumps({"erro": "ferramenta desconhecida"}), False


def reply(user: str, text: str) -> str:
    """Um turno completo: adiciona a mensagem, roda o loop de ferramentas, devolve o texto final."""
    memory.append(user, "user", text)
    out_text = []
    for _ in range(4):  # no máximo 4 idas e voltas por turno
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            tools=TOOLS,
            messages=memory.get(user),
        )
        memory.append(user, "assistant", [b.model_dump() for b in resp.content])
        out_text += [b.text for b in resp.content if b.type == "text"]
        if resp.stop_reason != "tool_use":
            break
        results, stop = [], False
        for b in resp.content:
            if b.type == "tool_use":
                content, s = _run_tool(user, b.name, b.input)
                stop = stop or s
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": content})
        memory.append(user, "user", results)
        if stop:
            break
    return "\n\n".join(t.strip() for t in out_text if t.strip())
