#!/usr/bin/env python3
"""Gera a spec do cocina-por-niveles-003 — el secreto del rendimiento del frijol.

Fonte da pauta (PASSO 0, 05/08/2026, n=47 videos mexicanos de 90 dias):
  mediana do nicho ............ 127 views/dia  (nicho grande, mediana alta)
  formato que performa ........ prato unico + segredo/tecnica, 434 a 690 v/d
    "El SECRETO para unos CHICHARRONES super CRUJIENTES" ......... 670 v/d
    "ENCHILADAS ECONOMICAS para toda la FAMILIA" ................. 448 v/d
  familia fraca ............... lista com preco ("N recetas con $100"), mediana 109
    e e exatamente o que o pacote anterior DESTE canal usou
    ("Despensa de $500 pesos: la lista exacta para 7 dias")

O canal e um explicador em doodle: nao compete em demonstracao de tecnica com
canais que filmam comida de verdade. O que ele faz melhor e a MATEMATICA. Entao
a pauta pega a estrutura do outlier (prato unico + segredo) e poe o segredo onde
o canal tem vantagem: o rendimento, em pesos por porcao.

Ancoras 2026 (Profeco, CONASAMI): salario minimo 315,04/dia geral e 440,87 na
ZLFN, alta de 13%; canasta basica entre 772,70 e 947,70; frijol 32/kg; tortilla
de milho 17/kg; ovo de 18 pecas caiu de 45,76 para 42,34.

Numeros por extenso, sem digitos — convencao do pacote anterior, que funcionou
com a es-MX-DaliaNeural (13,82 chars/s medidos).
"""
import json, os

VOZ = "es-MX-DaliaNeural"
PALETA = {"ink": "#1A1A1A", "c1": "#E36414", "c2": "#3A7D44", "bg": "#FDF6EC"}

CAPS = []


def cap(titulo, cenas):
    CAPS.append((titulo, cenas))


# ============================ 1 ============================
cap("El aumento que no se siente", [
 ("titulo", "13%", "subió el salario mínimo", "El salario mínimo subió trece por ciento en dos mil veintiséis. Trescientos quince pesos con cuatro centavos al día en la zona general."),
 ("titulo", "13%", "subió el salario mínimo", "En la Zona Libre de la Frontera Norte, cuatrocientos cuarenta pesos con ochenta y siete centavos. El aumento más grande en años."),
 ("item", "Y aun así", "no alcanza", "Y aun así, llegas al quince y ya no alcanza. No es que lo estés imaginando. Es que la despensa subió por otro lado."),
 ("barras", "Canasta básica 2026", ["Más barata", "PACIC", "Más cara"], [77, 91, 95], "La canasta básica de enero de dos mil veintiséis va de setecientos setenta y dos pesos hasta novecientos cuarenta y siete, según Profeco. El acuerdo contra la inflación apunta a novecientos diez."),
 ("item", "Al mes", "más de cuatro mil", "Para una familia de cuatro en zona urbana, la canasta alimentaria mensual pasa de cuatro mil pesos. Casi la mitad de un salario mínimo mensual."),
 ("titulo", "Hoy", "un solo ingrediente", "Hoy no vamos a ver una lista de veinte recetas. Vamos a ver un solo ingrediente, y el secreto que lo hace rendir cinco veces."),
 ("titulo", "El frijol", "treinta y dos pesos el kilo", "El frijol. Treinta y dos pesos el kilo, según los precios de este año. Y ese kilo, bien hecho, da cinco comidas para una familia."),
 ("item", "El secreto", "no es la receta", "El secreto no está en la receta. Está en cómo lo cueces y en cómo lo repartes. Y ahí es donde casi todos pierden dinero sin darse cuenta."),
 ("lista", "Lo que vamos a ver", ["Qué compra un kilo", "El secreto del rendimiento", "Cinco comidas del mismo pote", "El costo real por porción"], "Cuatro partes: qué compra de verdad un kilo, el secreto del rendimiento, las cinco comidas que salen del mismo pote, y cuánto cuesta cada porción."),
 ("item", "Si tienes prisa", "ve al minuto del secreto", "Si solo tienes tiempo para una parte, ve directo al secreto del rendimiento. Ahí está la diferencia entre tres comidas y cinco."),
 ("item", "Y una advertencia", "no es dieta", "Y una aclaración: esto no es una dieta ni un reto. Es aritmética de cocina, con los precios que hay ahorita."),
 ("titulo", "Empecemos", "por el kilo", "Empecemos por lo básico: qué te llevas realmente cuando pagas esos treinta y dos pesos."),
])

# ============================ 2 ============================
cap("Qué compra un kilo de frijol", [
 ("titulo", "1 kilo seco", "2,5 kilos cocido", "Un kilo de frijol seco no se queda en un kilo. Al cocerse absorbe agua y se convierte en unos dos kilos y medio de frijol listo."),
 ("item", "Eso significa", "el precio real baja", "Eso significa que el precio por kilo servido no es treinta y dos pesos. Es alrededor de trece, porque el agua hace parte del trabajo."),
 ("barras", "Costo por kilo servido", ["Frijol", "Huevo", "Pollo"], [22, 60, 100], "Comparado con otras fuentes de proteína, el frijol cocido queda muy por debajo. El huevo de dieciocho piezas anda en cuarenta y dos pesos con treinta y cuatro, y bajó siete punto cuatro por ciento este año."),
 ("item", "La tortilla", "diecisiete el kilo", "Y la tortilla de maíz, diecisiete pesos el kilo. Frijol con tortilla sigue siendo la comida más barata que existe en México, y por mucho."),
 ("titulo", "Pero", "no todo kilo rinde igual", "Pero aquí está el detalle que casi nadie dice: no todos los kilos rinden lo mismo. Dos personas compran el mismo kilo y una saca el doble."),
 ("item", "La diferencia", "está en tres decisiones", "La diferencia está en tres decisiones que se toman antes de que el frijol toque el fuego. Y ninguna cuesta dinero."),
 ("lista", "Antes de cocer", ["Revisar y limpiar", "Remojar o no", "Cuánto agua"], "Antes de cocer: revisar y limpiar, decidir si remojas, y cuánta agua pones. Esas tres deciden cuánto rinde el pote."),
 ("item", "Revisar", "piedras y frijol partido", "Revisar toma cinco minutos. Sacas piedras y frijol partido. El frijol partido se deshace y espesa el caldo, y ese caldo es parte del rendimiento."),
 ("item", "El caldo", "no se tira nunca", "Porque el caldo del frijol no es agua sucia. Es la base de tres de las cinco comidas que vamos a ver. Tirarlo es tirar una comida."),
 ("titulo", "El remojo", "aquí hay discusión", "El remojo es donde la gente discute. Hay quien jura que sí y quien jura que no. Los dos tienen parte de razón, y el motivo es práctico."),
 ("item", "Con remojo", "menos gas, más parejo", "Con remojo de una noche, el frijol cuece más rápido y más parejo. Ahorras gas, que también es dinero, y quedan menos granos duros."),
 ("item", "Sin remojo", "más sabor, más tiempo", "Sin remojo el caldo queda más espeso y con más sabor, pero tarda más y gasta más gas. Si tienes olla de presión, sin remojo funciona bien."),
 ("titulo", "Ahora sí", "el secreto", "Y ahora sí, el secreto del rendimiento, que no está en nada de lo anterior."),
])

# ============================ 3 ============================
cap("El secreto del rendimiento", [
 ("titulo", "La sal", "hasta el final", "El secreto es la sal. Se pone al final, cuando el frijol ya está suave. Nunca al principio."),
 ("item", "Por qué", "la cáscara se endurece", "Si salas desde el inicio, la cáscara se endurece y el frijol tarda mucho más en cocer. Gastas más gas y quedan granos duros que nadie come."),
 ("item", "Y los duros", "son pérdida directa", "Y cada grano duro que se queda en el plato es dinero que compraste y no comiste. Ahí se va el rendimiento sin que lo veas."),
 ("titulo", "Segundo", "el agua justa", "Segundo: el agua justa. Demasiada agua diluye el caldo y te obliga a hervir de más para espesarlo, otra vez gastando gas."),
 ("item", "La regla", "tres dedos arriba", "La regla vieja sirve: agua tres dedos arriba del frijol, y agregar agua caliente si hace falta. Agua fría a medio cocimiento endurece el grano."),
 ("titulo", "Tercero", "el pote grande", "Tercero, y es el que más rinde: cuece de más. El mismo gas, la misma hora de tu tiempo, y sale para varios días."),
 ("barras", "Costo por comida", ["Cocer 1 día", "Cocer 3 días", "Cocer 5 días"], [100, 45, 30], "Cocer para un día y cocer para cinco cuesta casi el mismo gas y el mismo tiempo. El costo por comida se desploma."),
 ("item", "Eso es el secreto", "no es una receta", "Ese es el verdadero secreto, y por eso no es una receta: es una decisión de cantidad. La olla llena rinde mucho más que la olla chica."),
 ("item", "El límite", "cuánto aguanta", "El límite es cuánto aguanta bien: en refrigerador, unos cuatro días. Congelado en porciones, meses. Y ahí el rendimiento se multiplica otra vez."),
 ("lista", "Guardar bien", ["Enfriar antes de tapar", "Porciones separadas", "Caldo aparte"], "Guardar bien es parte del secreto: enfriar antes de tapar, separar en porciones, y guardar algo de caldo aparte para las recetas que lo piden."),
 ("item", "Tapar caliente", "es el error clásico", "Tapar caliente genera vapor, y el vapor arruina el frijol antes de tiempo. Es el error que más comida tira a la basura."),
 ("titulo", "Con eso", "ya tienes la base", "Con esas tres decisiones ya tienes la base. Ahora veamos las cinco comidas distintas que salen del mismo pote."),
])

# ============================ 4 ============================
cap("Cinco comidas del mismo pote", [
 ("titulo", "Comida uno", "de la olla", "Comida uno: frijoles de la olla. El pote tal cual, con su caldo, cebolla y sal. Es la más simple y la más barata."),
 ("item", "Con tortilla", "ya es comida completa", "Con tortilla de maíz ya es una comida completa en proteína, porque el maíz y el frijol se complementan. Eso no es opinión, es composición."),
 ("titulo", "Comida dos", "refritos", "Comida dos: frijoles refritos. Machacas una parte con un poco de su caldo y grasa. Cambia por completo la textura y el sabor."),
 ("item", "El truco", "no dejarlos secos", "El truco es no dejarlos secos: se agrega caldo poco a poco. Refritos secos se sirven menos y sobran más, y lo que sobra sin gustar se tira."),
 ("titulo", "Comida tres", "enfrijoladas", "Comida tres: enfrijoladas. Licúas frijol con su caldo, bañas tortillas y listo. Aquí el caldo que ibas a tirar es el platillo entero."),
 ("item", "Rinden mucho", "y se ven distintas", "Es la que más rinde de las cinco, porque el frijol se convierte en salsa. Y en la mesa se ve como otra comida, que es lo que evita el cansancio."),
 ("titulo", "Comida cuatro", "sopa de frijol", "Comida cuatro: sopa de frijol. Más caldo, un poco de verdura, y se estira sin perder sustancia."),
 ("item", "Aquí entra", "lo que quedó", "Aquí entra lo que quedó de la semana: un pedazo de cebolla, medio jitomate, un chile. Es la comida que limpia el refrigerador."),
 ("titulo", "Comida cinco", "tacos o tostadas", "Comida cinco: tacos o tostadas de frijol. Los refritos que quedaron, sobre tortilla, con lo que haya encima."),
 ("item", "Es la más flexible", "acepta cualquier cosa", "Es la más flexible: acepta queso, salsa, lechuga, un huevo. Y cada agregado cambia el plato sin cambiar la base."),
 ("lista", "Las cinco", ["De la olla", "Refritos", "Enfrijoladas", "Sopa", "Tacos o tostadas"], "Cinco comidas, un solo pote: de la olla, refritos, enfrijoladas, sopa y tacos. Nadie en la mesa siente que comió lo mismo cinco veces."),
 ("item", "Eso importa", "más que el precio", "Y eso importa más que el precio, porque la comida barata que se repite igual termina en el bote de basura al tercer día."),
 ("titulo", "Ahora", "las cuentas", "Ahora hagamos las cuentas completas, con los precios de este año."),
])

# ============================ 5 ============================
cap("El costo real por porción", [
 ("titulo", "La base", "treinta y dos pesos", "La base: un kilo de frijol, treinta y dos pesos. Ese es todo el gasto principal de las cinco comidas."),
 ("item", "Agrega", "cebolla, ajo, sal, gas", "Agrega cebolla, ajo, sal y el gas de la cocción. Redondeando con holgura, unos cincuenta pesos por todo el pote."),
 ("item", "Tortillas", "para cinco comidas", "Súmale tortillas para acompañar las cinco comidas. Con dos kilos a diecisiete pesos, treinta y cuatro pesos más."),
 ("barras", "El pote completo", ["Frijol", "Extras y gas", "Tortillas"], [32, 18, 34], "El total del pote completo ronda ochenta y cuatro pesos, para cinco comidas de una familia."),
 ("titulo", "Divide", "y aparece el número", "Divide y aparece el número que importa: alrededor de diecisiete pesos por comida familiar. No por persona. Por comida."),
 ("item", "Compáralo", "con comer fuera", "Compáralo con una comida corrida fuera de casa, que en muchas ciudades ya no baja de cien pesos por persona."),
 ("barras", "Por comida familiar", ["El pote", "Fuera de casa"], [17, 100], "La diferencia no es de veinte por ciento. Es de varias veces, y se repite cinco veces en la semana."),
 ("item", "En un mes", "la cuenta cambia", "Si eso se repite dos veces por semana durante un mes, la diferencia se vuelve un pago completo de algo más importante."),
 ("titulo", "Pero ojo", "no es todos los días", "Pero seamos honestos: nadie come frijol cinco días seguidos y queda contento. Y ese es justo el punto de las cinco versiones."),
 ("item", "La meta", "que rinda sin cansar", "La meta no es comer frijol siempre. Es que cuando lo cocines, rinda de verdad y no canse. Eso es lo que baja el gasto del mes."),
 ("item", "Y el ahorro real", "está en no tirar", "Y el ahorro más grande no está en comprar más barato. Está en no tirar. La comida que se echa a perder es el gasto invisible."),
 ("titulo", "Hablemos", "de esos errores", "Hablemos entonces de los errores que tiran dinero, porque son pocos y siempre son los mismos."),
])

# ============================ 6 ============================
cap("Los errores que tiran dinero", [
 ("titulo", "Error uno", "cocer poquito", "Error uno: cocer poquito. Prendes el gas una hora para dos platos. El costo por plato se dispara y ni lo notas."),
 ("item", "El gas", "cuesta igual", "El gas cuesta casi lo mismo para media olla que para la olla llena. Es el gasto que más se desperdicia en la cocina mexicana."),
 ("titulo", "Error dos", "salar al principio", "Error dos, y ya lo vimos: salar al principio. Endurece la cáscara, alarga la cocción y deja granos que nadie se come."),
 ("titulo", "Error tres", "tirar el caldo", "Error tres: tirar el caldo. Ahí van las enfrijoladas y la sopa, que son dos de las cinco comidas."),
 ("item", "Tirar caldo", "es tirar dos comidas", "Dicho de otro modo: tirar el caldo del frijol es tirar dos de cada cinco comidas que ya pagaste."),
 ("titulo", "Error cuatro", "guardar caliente", "Error cuatro: guardar caliente y tapado. Se agria antes de tiempo y la mitad del pote termina en la basura."),
 ("item", "Enfriar", "no toma tiempo real", "Enfriar antes de tapar no te quita tiempo: sigues con tus cosas mientras el pote baja de temperatura. Solo hay que acordarse."),
 ("titulo", "Error cinco", "repetir igual", "Error cinco: servirlo idéntico tres días. Aunque esté bueno, la familia deja de comerlo, y lo que no se come se tira."),
 ("item", "Variar", "cuesta cero", "Variar no cuesta dinero: es machacar, licuar o poner sobre tortilla. Los mismos frijoles, tres platos distintos."),
 ("lista", "Los cinco errores", ["Cocer poquito", "Salar al inicio", "Tirar el caldo", "Guardar caliente", "Repetir igual"], "Los cinco errores: cocer poquito, salar al inicio, tirar el caldo, guardar caliente y repetir igual. Ninguno se arregla con dinero."),
 ("item", "Todos", "se arreglan con orden", "Todos se arreglan con orden, y el orden es gratis. Por eso el rendimiento no depende de cuánto ganas."),
 ("titulo", "Cerremos", "con el plan", "Cerremos con el plan concreto de la semana, para que esto no se quede en teoría."),
])

# ============================ 7 ============================
cap("El plan de la semana", [
 ("titulo", "Domingo", "el pote grande", "Domingo: el pote grande. Un kilo completo, sal al final, y dejas enfriar destapado antes de guardar."),
 ("item", "Separa", "desde el primer día", "Separa desde ese momento: una parte con caldo, una parte para machacar, y algo de caldo solo, aparte."),
 ("item", "Ese reparto", "es todo el trabajo", "Ese reparto de cinco minutos el domingo es prácticamente todo el trabajo de la semana. Lo demás es calentar y cambiar la forma."),
 ("titulo", "Lunes", "de la olla", "Lunes: de la olla, con tortilla. La versión más simple, cuando todavía está en su mejor punto."),
 ("titulo", "Martes", "refritos", "Martes: refritos, con caldo poco a poco para que no queden secos."),
 ("titulo", "Jueves", "enfrijoladas", "Jueves: enfrijoladas, con el caldo que guardaste aparte. Deja un día de por medio y nadie siente repetición."),
 ("item", "El día de por medio", "es parte del plan", "Ese día de por medio no es casualidad. Es lo que hace que la quinta comida siga siendo bienvenida."),
 ("titulo", "Viernes", "sopa o tacos", "Viernes: sopa con lo que quedó en el refrigerador, o tacos con los refritos que sobraron."),
 ("lista", "Resumen del plan", ["Domingo: cocer y repartir", "Lunes: de la olla", "Martes: refritos", "Jueves: enfrijoladas", "Viernes: sopa o tacos"], "Ese es el plan: domingo cueces y repartes, y de lunes a viernes solo cambias la forma. Un pote, cinco comidas."),
 ("item", "Y si sobra", "al congelador", "Y si sobra, al congelador en porciones. El frijol congelado aguanta meses y te salva un día de prisa sin gastar de más."),
 ("item", "Ese día", "es el que más ahorra", "Ese día de prisa es justo cuando la gente pide comida a domicilio. Tener una porción lista es lo que evita ese gasto."),
 ("titulo", "Y así", "el número final", "Y así el número final se sostiene: alrededor de diecisiete pesos por comida familiar, con precios de dos mil veintiséis."),
])

# ============================ 8 ============================
cap("Lo que te llevas", [
 ("titulo", "Tres cosas", "para recordar", "Si te llevas solo tres cosas de este video, que sean estas."),
 ("item", "Uno", "la sal hasta el final", "Uno: la sal hasta el final. Es gratis y es la diferencia entre frijol suave y granos duros que nadie come."),
 ("item", "Dos", "cuece de más", "Dos: cuece de más. El mismo gas y el mismo tiempo, repartido entre cinco comidas en vez de una."),
 ("item", "Tres", "el caldo no se tira", "Tres: el caldo no se tira nunca. Ahí viven dos de las cinco comidas."),
 ("titulo", "El resto", "es repartir", "Todo lo demás es repartir bien y cambiar la forma. Ninguna de esas cosas cuesta un peso adicional."),
 ("item", "Y por eso", "funciona con cualquier salario", "Y por eso este método funciona igual con salario mínimo que sin él. No depende de cuánto ganas, depende de cómo cueces."),
 ("titulo", "El contexto", "no va a mejorar solo", "El contexto no va a mejorar solo. La canasta básica seguirá moviéndose, y el aumento del salario se lo come el precio."),
 ("item", "Lo que sí controlas", "es el rendimiento", "Lo único que controlas de verdad es el rendimiento de lo que ya compraste. Y eso se decide en tu cocina, no en el mercado."),
 ("item", "Empieza", "este domingo", "Empieza este domingo con un kilo. Si funciona, la semana siguiente ya sabes exactamente qué hacer."),
 ("cta", "Cocina por Niveles", "un nivel a la vez", "Cuéntame en los comentarios a cuánto está el kilo de frijol en tu ciudad. Estoy juntando precios reales para el siguiente video."),
 ("cta", "Cocina por Niveles", "un nivel a la vez", "Y si quieres el mismo análisis con otro ingrediente básico, escribe cuál. El más pedido se hace primero."),
 ("cta", "Cocina por Niveles", "un nivel a la vez", "Gracias por llegar hasta el final. Nos vemos en el siguiente, aquí en Cocina por Niveles."),
])


# ===== poda para centralizar a duracao =====
# Com 98 cenas o video ia de 14,0 a 15,5 min conforme a taxa da voz. A es-MX
# mediu 13,82 chars/s no pacote anterior, mas o indonesio desacelerou 9% num
# roteiro denso em numero por extenso — e este tambem e. Podando as cenas que
# repetem algo ja dito, a faixa fica 13,0 a 14,4: dentro dos 12-15 em qualquer
# taxa plausivel, em vez de depender de a voz nao desacelerar.
REDUNDANTES = (
    "Y una aclaración: esto no es una dieta",     # o tom ja esta dado
    "Porque el caldo del frijol no es agua",      # repetido no capitulo de erros
    "Tapar caliente genera vapor",                # idem
    "Es la más flexible: acepta queso",           # detalhe menor
    "Si eso se repite dos veces por semana",      # a comparacao ja foi feita
    "Enfriar antes de tapar no te quita tiempo",  # idem
    "Ese día de por medio no es casualidad",      # ja esta implicito no plano
)
for _, _cenas in CAPS:
    _cenas[:] = [c for c in _cenas if not c[-1].startswith(REDUNDANTES)]


# ===================== montagem =====================
def cena(t, primeira, titulo_cap):
    lay, kicker = t[0], t[1]
    c = {"layout": lay, "kicker": kicker}
    if lay == "barras":
        c["itens"], c["alturas"], nar = t[2], t[3], t[4]
    elif lay == "lista":
        c["itens"], nar = t[2], t[3]
    elif lay == "item":
        c["preco"], nar = t[2], t[3]
    else:
        c["sub"], nar = t[2], t[3]
    c["nar"] = nar
    if primeira:
        c["cap"] = titulo_cap
    else:
        c["sem_cap"] = True
    return c


longo = []
for titulo_cap, cenas in CAPS:
    for i, t in enumerate(cenas):
        longo.append(cena(t, i == 0, titulo_cap))

short = [
 cena(("titulo", "$32", "un kilo de frijol", "Un kilo de frijol cuesta treinta y dos pesos. Bien hecho, da cinco comidas para toda la familia."), False, ""),
 cena(("item", "El secreto", "la sal al final", "El secreto no es la receta: es la sal hasta el final. Salar al inicio endurece la cáscara y deja granos que nadie come."), False, ""),
 cena(("titulo", "No tires", "el caldo", "Y el caldo no se tira nunca. Ahí viven las enfrijoladas y la sopa: dos de las cinco comidas."), False, ""),
 cena(("item", "Resultado", "diecisiete por comida", "El pote completo con tortillas sale en unos ochenta y cuatro pesos. Diecisiete por comida familiar."), False, ""),
 cena(("cta", "Cocina por Niveles", "el plan completo", "El plan de los cinco días y los errores que tiran dinero están en el video largo."), False, ""),
]
for c in short:
    c.pop("sem_cap", None)

spec = {
    "slug": "cocina-por-niveles",
    "pacote": "cocina-por-niveles-003",
    "voz": VOZ,
    "paleta": PALETA,
    "thumb": {"l1": "$32 = 5 COMIDAS", "l2": "el secreto"},
    "longo": longo,
    "short": short,
    "copy": "gerado a partir dos capitulos reais apos o render",
}

if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "cocina-por-niveles-003.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    nl = sum(len(c["nar"]) for c in longo)
    ns = sum(len(c["nar"]) for c in short)
    print(f"cenas longo ....... {len(longo)}")
    print(f"capitulos ......... {len(CAPS)}")
    print(f"chars narracao .... {nl}")
    for taxa in (13.0, 13.82, 14.5):
        s = nl / taxa + len(longo) * 0.5
        print(f"  a {taxa} chars/s .. {s:.0f}s = {s/60:.1f} min")
    print(f"short ............. {len(short)} cenas, {ns} chars, "
          f"~{ns/13.82 + len(short)*0.5:.0f}s")
    print(f"bytes ............. {os.path.getsize(destino)}")
