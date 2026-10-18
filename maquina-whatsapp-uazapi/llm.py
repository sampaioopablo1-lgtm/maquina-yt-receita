"""Gemini (SDK novo google-genai). tools=None hoje; o parâmetro já existe pra function calling depois."""
import os
from google import genai
from google.genai import types

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def generate_reply(history: list[dict], system: str, tools: list | None = None) -> str:
    config = types.GenerateContentConfig(system_instruction=system, max_output_tokens=1024, tools=tools)
    response = _client.models.generate_content(model=MODEL, contents=history, config=config)
    # TODO: tratar part.function_call quando tools for usado
    text = (response.text or "").strip()
    print(f"[llm] reply len={len(text)}")
    return text
