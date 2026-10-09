import json,pathlib
p=pathlib.Path("prompt.md").read_text(encoding="utf-8")
pathlib.Path("src/prompt.ts").write_text("// Gerado a partir de prompt.md — edite o .md e rode: python3 gerar_prompt.py\nexport const SYSTEM = "+json.dumps(p, ensure_ascii=False)+";\n", encoding="utf-8")
print("ok")
