import json,sys
CSS=open('cs.html').read().split('<style>')[1].split('</style>')[0]
MULT=('<div class="card"><div class="sec">MULTIPLICADOR DE CANCELAMENTO</div><table>'
 '<tr><th>Cancelamentos no mês</th><th style="text-align:right">Recebe da variável</th></tr>'
 +''.join(f'<tr><td>{a}</td><td class="v">{b}</td></tr>' for a,b in [("0","100%"),("1","90%"),("2","75%"),("3","50%"),("4 ou mais","0%")])+'</table></div>')
def fixo(v):
    return ('<div class="card"><div class="sec">1 · FIXO POR NÍVEL</div><table class="lv">'+
      ''.join(f'<tr><td>{n}</td><td class="v">{x}</td></tr>' for n,x in zip(["Júnior","Pleno","Sênior"],v))+'</table></div>')
def var(titulo,linhas,head=("Nível","Variável")):
    return (f'<div class="card"><div class="sec">2 · {titulo}</div><table><tr><th>{head[0]}</th><th style="text-align:right">{head[1]}</th></tr>'+
      ''.join(f'<tr><td>{a}</td><td class="v">{b}</td></tr>' for a,b in linhas)+'</table></div>')
def page(f):
    cards=''.join(f'<div class="card"><div class="n">{i+1}</div><div class="t">{t}</div><div class="d">{d}</div><div class="big">{b}</div></div>'+('<div class="plus">+</div>' if i<len(f["partes"])-1 else '') for i,(t,d,b) in enumerate(f["partes"]))
    ex=(f'<div class="ex"><div class="l">{f["ex"][0]}</div><div class="r">{f["ex"][1]}</div></div>') if f.get("ex") else ''
    extra=f.get("extra","")
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="k">TURBO7 · REMUNERAÇÃO</div><h1>{f["h1"]}</h1><div class="sub">{f["sub"]}</div>
<div class="row">{cards}</div><div class="row">{fixo(f.get("fixo",["R$ 2.000","R$ 3.000","R$ 5.000"]))}{f["var"]}</div>{extra}{ex}
<div class="foot">{f["foot"]}</div></body></html>'''
F=json.load(open('funcoes.json'))
for slug,f in F.items():
    open(f'{slug}.html','w').write(page(f).replace('VAR_MULT',MULT))
print(' '.join(F))
