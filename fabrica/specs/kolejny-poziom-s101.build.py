import sys, json, os, pathlib
sys.path.insert(0, '/home/user/maquina-yt-receita/fabrica')
import temas_do_dono as TD, layouts_do_short as LS, guardas_do_construtor as GC

PAC = 'kolejny-poziom-s101'
CANAL = 'kolejny-poziom'
SOND = set(LS.desenham())

def cena(layout, **kw):
    assert layout in SOND, 'layout %r fora do conjunto SONDADO %s' % (layout, sorted(SOND))
    return dict(layout=layout, **kw)

short = [
 cena('titulo', kicker='Wykres z umowy', sub='niczego nie odejmuje',
      nar='Wykres z umowy niczego nie odejmuje.'),
 cena('item', kicker='Co on pokazuje', sub='same wpłaty i sam wzrost',
      nar='Pokazuje tylko twoje wpłaty i sam ich wzrost.'),
 cena('barras', kicker='Część planu nie jest narysowana',
      barras=[{'rot':'W wykresie','v':100},{'rot':'Poza wykresem','v':100}],
      nar='Część tego planu nie jest narysowana.'),
 cena('item', kicker='Co zostało poza nim', sub='dwie stałe pozycje umowy',
      nar='Poza nim zostały dwie stałe pozycje.'),
 cena('lista', kicker='Obie są w twojej umowie',
      itens=['Roczna opłata','Podatek od zysku'],
      nar='To roczna opłata i podatek od zysku.'),
 cena('titulo', kicker='Pobierane', sub='automatycznie, bez twojego ruchu',
      nar='Obie pobierane są automatycznie.'),
 cena('item', kicker='Bez faktury', sub='i bez pytania o zgodę',
      nar='Nie przyjdzie faktura ani pytanie o zgodę.'),
 cena('barras', kicker='Dwa różne pytania',
      barras=[{'rot':'Pytanie wykresu','v':100},{'rot':'Twoje pytanie','v':100}],
      nar='Pytanie wykresu to nie twoje pytanie.'),
 cena('item', kicker='Dlatego się mylisz', sub='brutto czytasz jak netto',
      nar='I dlatego czytasz brutto jak własne netto.'),
 cena('lista', kicker='Poproś o dwie wersje',
      itens=['Wersja brutto','Wersja po kosztach'],
      nar='Poproś o drugą wersję tego samego wykresu.'),
 cena('cta', kicker='Sprawdź swoją umowę', sub='i zasubskrybuj kanał',
      nar='Sprawdź swoją umowę i zasubskrybuj kanał.'),
]

COPY = pathlib.Path("/tmp/claude-0/-home-user-maquina-yt-receita/d350e067-96dd-57b8-872e-549292f29a73/scratchpad/copy_s101.md").read_text()

sp = {
 'pacote': PAC,
 'slug': PAC,
 'idioma': 'pl',
 'voz': 'pl-PL-MarekNeural',
 'trilha': 'Wholesome',
 'paleta': TD.paleta_do_canal(CANAL),
 'longo': [],
 'longo_existente': 'ef_oZmfmdz4',
 'thumb': {'l1': 'Wykres brutto', 'l2': 'kieszeń netto'},
 'short': short,
 'copy': COPY,
}

GC.exige(sp)
print(json.dumps(sp, ensure_ascii=False, indent=1))
