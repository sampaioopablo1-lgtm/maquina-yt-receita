import pathlib
p = pathlib.Path(__file__).parent
html = (p / "painel.html").read_text(encoding="utf-8")
# String.raw: as barras invertidas do JS da pagina ('\\n', regex) chegam intactas ao navegador.
assert "`" not in html and "${" not in html, "painel.html nao pode ter crase nem ${"
(p / "painel.ts").write_text("// Gerado de painel.html: edite o .html e rode `python3 gerar.py` nesta pasta.\nexport const PAGINA = String.raw`" + html + "`;\n", encoding="utf-8")
print("painel.ts gerado")
