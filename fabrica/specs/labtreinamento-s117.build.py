# -*- coding: utf-8 -*-
import json, os, sys
sys.path.insert(0, 'fabrica')
import temas_do_dono as TD
import guardas_do_construtor as GC
import layouts_do_short as LS

PAC = "labtreinamento-s117"
CANAL = "labtreinamento"
SOND = set(LS.desenham())

short = [
 {"layout": "titulo", "kicker": "Três coisas da guia", "sub": "e só duas são números",
  "nar": "A sua conta começa com três coisas."},
 {"layout": "barras", "kicker": "Duas você já tem de cor",
  "barras": [{"rot": "Valor e meses", "v": 100}, {"rot": "O código", "v": 100}],
  "nar": "Duas dessas três você sabe de cor."},
 {"layout": "item", "kicker": "Valor e meses", "sub": "saem da memória",
  "nar": "O valor e os meses saem da memória."},
 {"layout": "item", "kicker": "O código, não", "sub": "ele só está no papel",
  "nar": "Já o código só existe no documento."},
 {"layout": "lista", "kicker": "E ele não é quantidade",
  "itens": ["Alíquota cheia", "Alíquota reduzida", "O código diz qual"],
  "nar": "E essa terceira não é quantidade."},
 {"layout": "item", "kicker": "Ela é uma classe", "sub": "e a classe decide",
  "nar": "É a classe que diz se a conta é sua."},
 {"layout": "titulo", "kicker": "Supor sai redondo", "sub": "e sai de outra pessoa",
  "nar": "Supondo, ela sai redonda e alheia."},
 {"layout": "cta", "kicker": "LabTreinamento", "sub": "inscreva-se",
  "nar": "Abra a guia e leia o código antes."},
]

for i, c in enumerate(short):
    assert c["layout"] in SOND, (i, c["layout"], "FORA do conjunto SONDADO")

sp = {
 "slug": PAC, "pacote": PAC, "idioma": "pt-BR",
 "voz": "pt-BR-ThalitaMultilingualNeural",
 "trilha": "Inspired", "longo_existente": "4OYBkCHFTV8", "longo": [],
 "thumb": {"l1": "Código não é", "l2": "número"},
 "paleta": TD.paleta_do_canal(CANAL),
 "short": short,
}
AQUI = os.path.dirname(os.path.abspath(__file__))
cp = os.path.join(AQUI, "copy_s117.md")
if os.path.exists(cp):
    sp["copy"] = open(cp, encoding="utf-8").read()
GC.exige(sp)
dest = sys.argv[1] if len(sys.argv) > 1 else "fabrica/specs/%s.json" % PAC
json.dump(sp, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", dest, "cenas", len(short), "media chars",
      round(sum(len(c["nar"]) for c in short) / float(len(short)), 2))
for c in short: print("  %2d %s" % (len(c["nar"]), c["nar"]))
