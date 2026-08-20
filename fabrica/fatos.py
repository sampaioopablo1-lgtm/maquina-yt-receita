#!/usr/bin/env python3
"""O portao que confere NUMERO contra fonte, antes de o render comecar.

Existe porque a rotina passou a escrever spec sozinha. Enquanto cada roteiro
saia daqui escrito a mao, a regra das "duas fontes que batem" era cumprida por
mim, na pesquisa, e nada no repositorio precisava verificar nada. Um gerador
automatico quebra exatamente esse acordo: ele escreve `quarenta e dois por
cento` com a mesma fluencia com que escreve a verdade, e nenhum dos sete
portoes de `prontidao.py` sabe a diferenca — eles medem ritmo, lingua, borda e
duracao, nunca o mundo.

E o custo do erro nao e simetrico entre os canais. `labtreinamento` fala de
norma regulatoria com prazo, `sx-educacao` e `next-level-money` de dinheiro,
`seja-mais-magra` de saude. Numero errado ali nao e video ruim, e dano.

## A divisao de trabalho, que e o ponto do arquivo

Verificar e CARO: uma chamada de modelo com busca na web, minutos, dolares.
Fazer isso a cada 30 minutos, em toda spec do diretorio, seria insustentavel —
e `prontidao.py` roda exatamente assim.

Entao a verificacao acontece UMA VEZ, quando a spec nasce, e o veredito fica
gravado dentro da propria spec, em `spec["fatos"]`. O portao barato de todo
ciclo (`conferir`) so pergunta tres coisas: existe veredito, ele aprovou, e a
narracao ainda e a mesma que ele leu.

Essa terceira pergunta e a que da forca as outras duas. O veredito guarda o
sha256 da narracao inteira — longo mais short, na ordem. Trocar uma palavra
muda a impressao e ANULA a aprovacao. Nao ha como aprovar um roteiro e
publicar outro, nem por descuido nem de proposito.

## Por que a extracao e generosa e a classificacao nao e

`afirmacoes()` devolve toda frase com quantidade dentro. Isso inclui muita
coisa que nao e afirmacao sobre o mundo: "sao tres colunas", "o primeiro
ponto". Reprovar uma spec por causa de "tres colunas" seria repetir o
aprendizado 230 — um alarme que dispara sempre vira um alarme que ninguem le.

Mas separar retorica de fato com regex nao da: a mesma forma de frase serve as
duas. Entao a extracao fica burra e generosa, e QUEM classifica e o modelo,
frase a frase, junto com a verificacao — e a classificacao fica escrita no
veredito, auditavel. So `factual` precisa das duas fontes.

Uso:
    python3 fabrica/fatos.py extrair   <spec.json>   # o que sera verificado
    python3 fabrica/fatos.py verificar <spec.json>   # chama o modelo e grava
    python3 fabrica/fatos.py conferir  [spec.json]   # portao barato, offline
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

MODELO = os.getenv("FATOS_MODELO", "claude-opus-5")

# A busca na web e um tool do lado do servidor: uma requisicao so, o modelo
# pesquisa por dentro dela. `web_search_20260209` e a variante com filtragem
# dinamica, disponivel no Opus 5.
FERRAMENTA_BUSCA = "web_search_20260209"
MAX_BUSCAS = 12

SITUACOES = ("confirmado", "refutado", "sem_fonte", "retorica")
APROVADAS = ("confirmado", "retorica")


def narracao_toda(spec: dict) -> list[tuple[str, int, str]]:
    """(bloco, indice da cena, narracao) de longo e short, nessa ordem."""
    saida = []
    for bloco in ("longo", "short"):
        for i, cena in enumerate(spec.get(bloco) or []):
            nar = (cena or {}).get("nar") or ""
            if nar.strip():
                saida.append((bloco, i, nar))
    return saida


def impressao(spec: dict) -> str:
    """sha256 da narracao inteira. E a isto que o veredito se prende.

    So a narracao entra. Kicker, sub e paleta mudam o video, nao mudam o que
    ele AFIRMA — e reverificar por causa de uma troca de cor gastaria dolares
    para reler o mesmo texto.
    """
    corpo = "\n".join(f"{b}#{i}\t{nar}" for b, i, nar in narracao_toda(spec))
    return "sha256:" + hashlib.sha256(corpo.encode("utf-8")).hexdigest()


# O artigo indefinido e homografo do numero UM em metade das linguas da frota,
# e `narracao.conta_numeros` conta os dois igual. La isso e inofensivo: ele
# soma contra um teto de quatro por frase, e um artigo perdido nao derruba
# ninguem. Aqui seria fatal — medido em 20/08/2026 na labtreinamento-003, o
# extrator devolvia 85 afirmacoes, e "E uma coisa fica dita ja." era uma
# delas. Mandar isso para verificacao gasta dolar para o modelo responder
# "retorica" oitenta vezes, e afoga as afirmacoes que importam.
#
# So o token SOZINHO some. "um milhao" sobrevive por "milhao", "um por cento"
# por "cento", "uma em cada tres" por "tres" — o grupo continua existindo
# quando ha qualquer outro sinal numerico. O que o filtro remove e exatamente
# o caso em que o artigo era o unico.
ARTIGO = {
    "pt": r"\b(um|uma|uns|umas)\b",
    "es": r"\b(un|uno|una|unos|unas)\b",
    "tr": r"\b(bir)\b",
    "el": r"\b(ενα|ενας|μια)\b",
    "hi": r"(एक)",
}


def afirmacoes(spec: dict) -> list[dict]:
    """Toda frase com quantidade de verdade dentro, de qualquer bloco.

    Generosa de proposito: ver o cabecalho. O corte entre fato e retorica e do
    modelo, nao daqui. O que ela NAO faz e confundir artigo com numero.
    """
    import narracao as N

    idi = N.idioma_de(spec, None)
    artigo = ARTIGO.get(idi)
    saida = []
    for bloco, i, nar in narracao_toda(spec):
        for frase in N.frases(nar, idi):
            corpo = frase if idi == "hi" else N.normaliza(frase)
            if artigo:
                corpo = re.sub(artigo, " ", corpo)
            tem_numero = N.conta_numeros(corpo, idi) > 0
            tem_ano = bool(re.search(r"\b(19|20)\d{2}\b", frase))
            if tem_numero or tem_ano:
                saida.append({"bloco": bloco, "cena": i, "texto": frase})
    return saida


SISTEMA = """Voce confere fatos de roteiro de video antes de ele ser gravado.

Cada afirmacao que voce recebe saiu da narracao de um video que vai ao ar num
canal do YouTube sobre dinheiro, carreira, saude ou norma regulatoria. Errar um
numero nesses assuntos causa dano a quem assiste, entao o padrao e alto.

Para cada afirmacao, classifique em uma destas situacoes:

  retorica    o numero nao afirma nada sobre o mundo: e estrutura do roteiro
              ("sao tres pontos", "a primeira coluna", "vamos ao segundo
              exemplo"), contagem interna do proprio video, ou exemplo
              declarado como hipotetico dentro da propria frase.
  confirmado  afirma algo sobre o mundo E voce encontrou DUAS fontes
              independentes que concordam com o valor. Fonte institucional
              (orgao publico, agencia reguladora, comite de norma, instituto
              de estatistica, publicacao revisada) vale mais que imprensa, e
              pelo menos UMA das duas precisa ser institucional.
  refutado    voce encontrou fonte confiavel que contradiz a afirmacao.
  sem_fonte   afirma algo sobre o mundo e voce NAO conseguiu as duas fontes.

`sem_fonte` nao e vergonha nem falha sua: e a resposta certa quando o dado nao
esta publicado, esta atras de paywall, ou as fontes divergem entre si. Nao
converta duvida em `confirmado`. Na duvida entre `confirmado` e `sem_fonte`,
responda `sem_fonte`.

Nao classifique como `retorica` uma afirmacao sobre o mundo so porque ela e
vaga ou arredondada. "A maioria das empresas gasta milhares" e afirmacao sobre
o mundo, e sem fonte ela e `sem_fonte`.

Responda SO com JSON, sem cerca de codigo, no formato:

{"afirmacoes": [{"i": 0, "situacao": "confirmado", "fontes": ["url", "url"],
                 "nota": "uma frase dizendo o que a fonte diz"}]}

`fontes` fica vazia em `retorica`. `nota` e sempre obrigatoria e sempre curta.
Devolva um item para CADA afirmacao recebida, na mesma numeracao."""


def _pergunta(spec: dict, itens: list[dict]) -> str:
    ctx = (f"Canal: {spec.get('slug')}. Idioma da narracao: "
           f"{spec.get('idioma')}. Pacote: {spec.get('pacote')}.\n"
           f"Hoje e {os.getenv('FATOS_HOJE') or 'a data corrente'}.\n\n"
           f"Afirmacoes ({len(itens)}):\n")
    linhas = [f"{i}. {it['texto']}" for i, it in enumerate(itens)]
    return ctx + "\n".join(linhas)


def verificar(spec: dict, *, modelo: str = "") -> dict:
    """Chama o modelo com busca na web e devolve o veredito, ja com impressao."""
    import datetime as dt

    itens = afirmacoes(spec)
    agora = dt.datetime.now(dt.timezone.utc).isoformat()
    if not itens:
        # Roteiro sem numero nenhum e raro mas legitimo. Aprovar com a lista
        # vazia e honesto: nao ha o que conferir, e o registro diz isso.
        return {"verificado_em": agora, "modelo": modelo or MODELO,
                "hash_narracao": impressao(spec), "veredito": "aprovado",
                "afirmacoes": []}

    import modelo as M

    bruto = M.so_o_json(M.chamar(
        SISTEMA, [{"role": "user", "content": _pergunta(spec, itens)}],
        modelo=modelo or MODELO, max_tokens=16000,
        ferramentas=[{"type": FERRAMENTA_BUSCA, "name": "web_search",
                      "max_uses": MAX_BUSCAS}]))
    vereditos = {int(v["i"]): v for v in bruto.get("afirmacoes", []) if "i" in v}

    saida = []
    for i, it in enumerate(itens):
        v = vereditos.get(i) or {}
        sit = v.get("situacao")
        if sit not in SITUACOES:
            # Item que o modelo esqueceu ou classificou fora da lista NAO passa
            # por omissao. Silencio nao e aprovacao.
            sit = "sem_fonte"
            v = dict(v, nota=v.get("nota") or "o modelo nao classificou esta afirmacao")
        saida.append({**it, "situacao": sit,
                      "fontes": v.get("fontes") or [],
                      "nota": v.get("nota") or ""})

    reprovadas = [a for a in saida if a["situacao"] not in APROVADAS]
    return {"verificado_em": agora, "modelo": modelo or MODELO,
            "hash_narracao": impressao(spec),
            "veredito": "reprovado" if reprovadas else "aprovado",
            "afirmacoes": saida}


def conferir(spec: dict) -> list[str]:
    """O portao barato, offline. Roda em todo ciclo, custa microssegundos."""
    fatos = spec.get("fatos")
    if not fatos:
        return ["sem veredito de fatos — rode `fabrica/fatos.py verificar` "
                "nesta spec antes de renderizar"]
    if fatos.get("hash_narracao") != impressao(spec):
        return ["a narracao mudou depois da verificacao — o veredito e de outro "
                "texto e nao vale; verifique de novo"]
    if fatos.get("veredito") != "aprovado":
        ruins = [a for a in fatos.get("afirmacoes", [])
                 if a.get("situacao") not in APROVADAS]
        amostra = "; ".join(f"[{a['situacao']}] {a['texto'][:70]}" for a in ruins[:3])
        return [f"{len(ruins)} afirmacao(oes) sem fonte ou refutada(s): {amostra}"]
    return []


def _carrega(caminho: str) -> dict:
    return json.load(open(caminho, encoding="utf-8"))


def main() -> int:
    import glob

    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]

    if cmd == "extrair":
        sp = _carrega(sys.argv[2])
        itens = afirmacoes(sp)
        for i, it in enumerate(itens):
            print(f"{i:3d} {it['bloco']}#{it['cena']:<3d} {it['texto']}")
        print(f"\n{len(itens)} afirmacao(oes) iriam para verificacao.")
        return 0

    if cmd == "verificar":
        caminho = sys.argv[2]
        sp = _carrega(caminho)
        v = verificar(sp)
        sp["fatos"] = v
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(sp, f, ensure_ascii=False, indent=2)
            f.write("\n")
        for a in v["afirmacoes"]:
            marca = " " if a["situacao"] in APROVADAS else "!"
            print(f"{marca} {a['situacao']:<11} {a['texto'][:88]}")
            if a["fontes"]:
                print(f"      {' | '.join(a['fontes'][:2])}")
        print(f"\nveredito: {v['veredito'].upper()} "
              f"({len(v['afirmacoes'])} afirmacoes)")
        return 0 if v["veredito"] == "aprovado" else 1

    if cmd == "conferir":
        alvos = sys.argv[2:] or sorted(
            glob.glob(os.path.join(RAIZ, "fabrica/specs/*.json")))
        ruins = 0
        for c in alvos:
            sp = _carrega(c)
            if not sp.get("longo"):
                continue
            faltas = conferir(sp)
            if faltas:
                ruins += 1
                print(f"{os.path.basename(c)[:-5]}: {faltas[0]}")
        print(f"\n{ruins} spec(s) sem fatos conferidos.")
        return 1 if ruins else 0

    print(f"comando desconhecido: {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
