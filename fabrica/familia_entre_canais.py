"""A FAMILIA atravessa canal, e nenhum instrumento olhava para fora do canal.

**Medido em 23/10 as 17:0x, escolhendo a familia do `epomeno-epipedo-s102`.** Eu
tinha QUATRO candidatas na mao e descartei uma delas — a ATRIBUICAO do movimento
de um agregado ao componente que empurrou para o outro lado (capitulo 19 daquele
longo) — **porque ela e o eixo do `kolejny-poziom-s099`, publicado HOJE as
06:21Z em OUTRO canal.** E eu sabia disso **de cabeca**: nenhum instrumento do
repo me diria.

**As tres comparacoes que existem param antes desta:**

| instrumento | o que compara |
|---|---|
| `irmaos_da_origem` | familia DENTRO da mesma origem |
| portao `similaridade` | titulo contra o MESMO canal (o `_especs_do_canal` filtra pelo slug) |
| `esqueleto_entre_canais` | **FORMA** atravessando canal |

**Logo a FORMA atravessando canal tem instrumento desde 20/10 as 01:3x e a
FAMILIA nao tinha nenhum** — e e a familia que carrega o conteudo. Eu venho
escrevendo em cada copy desta semana, em letra, que *"o `similaridade` nao
pegaria repeticao entre canais, porque compara contra o MESMO canal"*: a frase
estava certa e **a conferencia era a minha memoria**, que e o item 3 da §10 na
decima dimensao.

**E a pergunta e literalmente a do DONO.** Palavras dele em 19/10: *"os videos
publicados me parecem todos a mesma dinamica, imagens, formas, estilo. **Em
todos os canais.** Ajuste."* O `esqueleto_entre_canais` respondeu a metade da
FORMA; esta e a metade do CONTEUDO.

**A RECENCIA SAI DO PARQUE, e isso e forcado: a spec no disco NAO TEM DATA.** O
instante vem de `duracao_a_medir.carrega()` e o canal de `canal.do_pacote` —
medido, **57 das 163 linhas do parque nao tem o campo `canal`**, logo ler o campo
perderia essas pecas em silencio. E a mesma delegacao que o
`contagem_de_cenas.repete_recente` faz pela mesma razao.

**E A FAMILIA SAI DO DONO, NOS DOIS NIVEIS.** O campo `## FAMILIA DE ENTRADA
ERRADA` existe em **138 das 311** specs de short solto com copy (0,444) e falta
em 173 — logo os dois lados existem e nenhum dos dois ramos passa por vacuidade.
Para quem nao tem o campo vai o **bloco de PROSA e a NARRACAO inteira**, com a
procedencia ROTULADA, porque frase de irmao citando irmao e compressao de
TERCEIRO e guarda o eixo que interessava a ELE (20/10, 15:3x). A leitura e
sempre do `irmaos_da_origem`, que e o dono dela — reparsear aqui criaria o
segundo dono da forma da copy, a assinatura que congelou a legenda.

**ELE NAO DECIDE SE DUAS FAMILIAS SAO A MESMA (776):** poe o material na mesa.
Decidir por semelhanca de texto seria detector que inventa achado (725), e o
caso desta rodada mostra por que: *atribuicao de um agregado a um componente* e
*atribuicao de um resultado a uma variavel que nao variou* nao compartilham uma
palavra e sao o mesmo eixo para quem le.

**E o `RECENTES_K` vai DECLARADO como redacao e nao como medida:** ele sai de
quantas pecas por canal a frota publica numa janela em que a repeticao e
visivel ao espectador, nao de uma distribuicao. Por ser escolha, e parametro, e
quem precisar de outro passa o argumento.

**NAO E PORTAO** e o codigo de saida e **sempre zero**, pelo argumento do
`mira.py`: reprovar aqui exigiria decidir semelhanca, que e justamente o que
este modulo recusa fazer.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import canal as CA
import duracao_a_medir as DM
import irmaos_da_origem as IO
import nome_da_spec as NS
import rascunho as RA

# REDACAO declarada, nao medida: ver o docstring.
RECENTES_K = 3

# A frota, para o relato saber de quem ele NAO tem noticia. Ela e do
# `orquestra.CANAIS_FOCO`; aqui ela e so a lista de quem perguntar.
_FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def _spec(pacote: str, dir_specs: str = None):
    """A spec de um pacote, ou None quando ela nao esta no disco.

    A LEITURA e do `rascunho.spec_de`, que e o dono dela desde 21/10 as 20:3x —
    um `json.load` aqui seria o segundo dono. Arquivo ausente devolve None e vai
    NOMEADO no relato, porque ausencia de leitura nao e ausencia de familia.
    """
    d = dir_specs or IO._dir_specs()
    try:
        return RA.spec_de(os.path.join(d, NS.arquivo(pacote)))
    except (FileNotFoundError, NotADirectoryError, ValueError):
        return None


def familia_da_peca(pacote: str, dir_specs: str = None) -> dict:
    """O que a peca DIZ da familia dela, com a procedencia ROTULADA.

    `campo` e PRIMEIRA mao e e o dono quando existe. Sem ele vao a PROSA e a
    NARRACAO, as duas inteiras e as duas de primeira mao — truncar por tamanho
    foi o que quase cortou a frase que salvou o `labtreinamento-s035`.
    """
    sp = _spec(pacote, dir_specs)
    if sp is None:
        return {"pacote": pacote, "sem_spec": True, "tem_campo": None,
                "campo": "", "prosa": [], "narracao": [], "titulo": ""}
    cp = sp.get("copy") or ""
    campo = IO._secao(cp, IO.CAMPO_FAMILIA).strip()
    prosa = []
    narracao = []
    if not campo:
        for nome in IO.BLOCOS_DE_PROSA:
            t = IO._secao(cp, nome).strip()
            if t:
                prosa.append((nome, t))
        narracao = IO._narracao(sp)
    return {"pacote": pacote, "sem_spec": False, "tem_campo": bool(campo),
            "campo": campo, "prosa": prosa, "narracao": narracao,
            "titulo": IO._titulo_curto(cp)}


def recentes_de_outros(canal: str, k: int = RECENTES_K, parque=None,
                       dir_specs: str = None, exceto: str = "") -> dict:
    """As `k` ultimas pecas de CADA canal que nao e este, do PARQUE.

    O canal de cada linha sai do `canal.do_pacote` e nao do campo `canal`, que
    falta em 57 das 163 linhas — ler o campo perderia essas pecas calado.
    """
    regs = DM.carrega() if parque is None else list(parque)
    por_canal = {}
    for r in regs:
        pac = r.get("pacote") or ""
        if not pac:
            continue
        if exceto and NS.casa(pac, exceto):
            continue
        c = CA.do_pacote(pac)
        if c == canal:
            continue
        por_canal.setdefault(c, []).append(r)
    outros = {}
    for c, rs in por_canal.items():
        rs.sort(key=lambda r: r.get("em") or "")
        vistos = []
        for r in reversed(rs):
            pac = r["pacote"]
            if pac in [v["pacote"] for v in vistos]:
                continue
            f = familia_da_peca(pac, dir_specs)
            f["em"] = r.get("em")
            vistos.append(f)
            if len(vistos) >= k:
                break
        outros[c] = vistos
    sem_parque = [c for c in _FROTA if c != canal and not outros.get(c)]
    recusa = None
    if not any(outros.values()):
        recusa = ("nenhum outro canal da frota tem peca no parque — aqui nao se "
                  "compara familia entre canais, e isso e ESTADO e nao "
                  "propriedade. Do jeito que o `porta1` recusa janela curta.")
    return {"canal": canal, "k": k, "outros": outros,
            "sem_parque": sem_parque, "recusa": recusa}


def _linha_das_familias(d: dict) -> list:
    """UM dono da frase, nos DOIS ramos."""
    pre = "  FAMILIA ENTRE CANAIS"
    if d.get("recusa"):
        return ["%s: %s" % (pre, d["recusa"])]
    L = ["%s: as %d ultimas de cada OUTRO canal, do parque. O portao "
         "`similaridade` compara contra o MESMO canal, logo familia que "
         "atravessa canal e invisivel para ele — e esta era a conferencia que "
         "eu fazia de MEMORIA (23/10, 17:0x)." % (pre, d["k"])]
    for c in sorted(d["outros"]):
        for f in d["outros"][c]:
            L.append("    %s | %s | %s" % (c, f["pacote"], f.get("em") or "-"))
            if f["sem_spec"]:
                L.append("      >> spec NAO esta no disco: a familia dela nao "
                         "foi lida. Ausencia de leitura nao e ausencia de "
                         "familia (17/10).")
                continue
            if f["tem_campo"]:
                L.append("      familia (campo, PRIMEIRA mao): %s"
                         % " ".join(f["campo"].split())[:400])
                continue
            L.append("      campo AUSENTE — geracao anterior. Vai a PROSA e a "
                     "NARRACAO, as duas de PRIMEIRA mao, porque citacao de "
                     "irmao e compressao de TERCEIRO (20/10, 15:3x).")
            L.append("      titulo curto: %s" % (f["titulo"] or "-"))
            for nome, t in f["prosa"]:
                L.append("      [PROSA '%s'] %s" % (nome, " ".join(t.split())))
            for n in f["narracao"]:
                L.append("      . %s" % n)
    if d["sem_parque"]:
        L.append("    sem peca no parque: %s — e isso NAO quer dizer que o "
                 "canal nao publicou, quer dizer que o parque nao a tem."
                 % ", ".join(d["sem_parque"]))
    L.append("    isto NAO decide se duas familias sao a MESMA (776): poe o "
             "material na mesa. Decidir por semelhanca de texto seria detector "
             "que inventa achado (725) — o caso de 23/10 as 17:0x nao "
             "compartilha uma palavra com o irmao de outro canal e e o mesmo "
             "eixo.")
    return L


def relato(canal: str, k: int = RECENTES_K, parque=None, dir_specs: str = None,
           exceto: str = "") -> str:
    d = recentes_de_outros(canal, k=k, parque=parque, dir_specs=dir_specs,
                           exceto=exceto)
    return "\n".join(_linha_das_familias(d))


def main() -> int:
    c = sys.argv[1] if len(sys.argv) > 1 else "labtreinamento"
    exceto = sys.argv[2] if len(sys.argv) > 2 else ""
    print(relato(c, exceto=exceto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
