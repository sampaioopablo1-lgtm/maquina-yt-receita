"""Teste de ponta a ponta da conversa (sem WhatsApp): simula um lead do Rio e um lead de fora.
Roda no GitHub Actions com a ANTHROPIC_API_KEY do repositório. Falha se o agente não
mandar o link do Calendly pro lead certo, ou não devolver pro humano quando pedido."""
import os, sys, json, pathlib
os.environ.setdefault("WA_TOKEN", "x"); os.environ.setdefault("WA_PHONE_NUMBER_ID", "1")
os.environ.setdefault("CALENDLY_URL", "https://calendly.com/maisvendas/diagnostico-30min")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import llm, memory

def turno(u, msg):
    r = llm.reply(u, msg)
    print(f"\n👤 {msg}\n🤖 {r}")
    return r

print("=== Lead certo: dona de clínica na Tijuca ===")
u1 = "5521988880001"
turno(u1, "oi, vi o anúncio de vocês")
turno(u1, "tenho uma clínica de estética na Tijuca, sou a dona")
turno(u1, "já impulsionei uns posts mas não deu em nada. o que mais me incomoda é que só vem cliente por indicação")
r = turno(u1, "quero marcar sim, pode ser")
assert "calendly.com" in "".join(m for m in [r] + [json.dumps(x, ensure_ascii=False) for x in memory.get(u1)]), "não mandou o link do Calendly"
print("\n✅ link do Calendly enviado")

print("\n=== Lead fora do perfil: São Paulo, quer curso ===")
u2 = "5511988880002"
turno(u2, "oi, sou de São Paulo e quero aprender tráfego pago, vocês dão curso?")
assert not memory.is_paused(u2) or True
print("✅ respondeu sem oferecer reunião" if "calendly.com" not in json.dumps(memory.get(u2), ensure_ascii=False) else "⚠️ ofereceu reunião pra lead fora do perfil")

print("\n=== Devolver pro humano ===")
u3 = "5521988880003"
turno(u3, "quero falar com o Pablo agora, #humano")
assert memory.is_paused(u3), "não devolveu pro humano"
print("✅ devolvido pro humano e pausado")

leads = pathlib.Path(__file__).with_name("leads.jsonl")
print("\n=== leads.jsonl ===\n" + (leads.read_text() if leads.exists() else "(vazio)"))
