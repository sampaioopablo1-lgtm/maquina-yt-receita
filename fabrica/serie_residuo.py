"""A serie do residuo tinha DOIS donos: a lista no teste e o RESIDUO_N no mira.

POR QUE ESTE MODULO EXISTE (19/10/2026). Acrescentar um ponto era passo MEU, a
mao, em dois arquivos:

  1. uma linha `("<pacote>", <prev>, <real>, "<provedor>"),  # job <id>` na
     lista `SERIE` de `tests/test_residuo_quebra_o_limite_de_dois_segundos.py`;
  2. `RESIDUO_N` em `fabrica/mira.py`, incrementado de um.

**Isso ja corrompeu os dados DUAS vezes, e as duas estao medidas.** Em 18/10 as
11:2x eu descobri que `RESIDUO_N` dizia 93 e a lista tinha 94: o
`epomeno-epipedo-s058` estava la DUAS vezes. A causa era a forma do meu
`t.replace(ancora, ancora + "\\n" + linha)`: a ancora que eu escrevia era a linha
SEM o comentario `# job`, e a linha no arquivo TEM — logo o replace casava um
PREFIXO, a linha nova entrava no MEIO da antiga e o comentario ficava pendurado
no fim dela. Seis rodadas assim acumularam seis jobs numa linha so.

**E o `assert t.count(ancora) == 1` que eu usava para me proteger NAO pegava
isso**, porque o prefixo e unico mesmo quando a linha inteira nao e — a guarda
media o que eu pedi, e o que eu pedi era insuficiente.

**O QUE ESTE MODULO NAO FAZ, de proposito: nao MIGRA a serie.** Os dados ficam
onde estao, no teste que os ancora, e a leitura e por **AST** — mover a lista
para um `.json` seria criar um terceiro dono e perder os comentarios de
procedencia, que sao o que distingue um ponto medido de um numero escrito.

O que ele faz e tirar o passo da minha mao: `acrescenta` insere por **LINHA
INTEIRA**, recusa pacote repetido e job repetido, e **sincroniza o `RESIDUO_N`
no mesmo passo** — logo as duas coisas nao podem mais divergir.
"""
import ast
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_SERIE = os.path.join(
    RAIZ, "tests", "test_residuo_quebra_o_limite_de_dois_segundos.py")
ARQ_N = os.path.join(RAIZ, "fabrica", "mira.py")

PROVEDORES = ("edge", "piper")


def _texto(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def pontos(texto: str | None = None) -> list[tuple]:
    """A SERIE lida por AST do arquivo que a ancora. Fonte UNICA."""
    arvore = ast.parse(texto if texto is not None else _texto(ARQ_SERIE))
    for no in ast.walk(arvore):
        if (isinstance(no, ast.Assign) and len(no.targets) == 1
                and isinstance(no.targets[0], ast.Name)
                and no.targets[0].id == "SERIE"):
            return [tuple(ast.literal_eval(e) for e in t.elts)
                    for t in no.value.elts]
    raise RuntimeError("AUSENCIA DE LEITURA: nao achei a SERIE em "
                       f"{ARQ_SERIE} — leitura vazia nao e serie vazia")


def n_declarado(texto: str | None = None) -> int:
    t = texto if texto is not None else _texto(ARQ_N)
    m = re.search(r"^RESIDUO_N = (\d+)", t, re.M)
    if not m:
        raise RuntimeError("AUSENCIA DE LEITURA: nao achei RESIDUO_N")
    return int(m.group(1))


def divergencia() -> dict:
    """O defeito de 18/10 as 11:2x, como PROPRIEDADE e nao como aquele caso."""
    ps = pontos()
    nomes = [p[0] for p in ps]
    repetidos = sorted({x for x in nomes if nomes.count(x) > 1})
    jobs = re.findall(r"#\s*job\s*(\d+)", _texto(ARQ_SERIE))
    jobs_repetidos = sorted({j for j in jobs if jobs.count(j) > 1})
    duas_marcas = [l.strip() for l in _texto(ARQ_SERIE).splitlines()
                   if len(re.findall(r"#\s*job", l)) > 1]
    return {"n_serie": len(ps), "n_declarado": n_declarado(),
            "bate": len(ps) == n_declarado(), "pacotes_repetidos": repetidos,
            "jobs_repetidos": jobs_repetidos,
            "linhas_com_duas_marcas_de_job": duas_marcas}


def limites(ps: list[tuple] | None = None) -> tuple[float, float]:
    """A banda OBSERVADA: o menor e o maior residuo da serie.

    Nao arredonda nem alarga de proposito — ela e o extremo observado, e e por
    isso que as sete correcoes dela ALARGARAM. Quem quiser a banda do `mira.py`
    compara com isto em vez de reescrever o par a mao."""
    ps = ps if ps is not None else pontos()
    rs = [round(real - prev, 1) for _p, prev, real, _prov in ps]
    return min(rs), max(rs)


def acrescenta(pacote: str, prev: float, real: int, provedor: str,
               job: str, nota: str | None = None, aplicar: bool = False):
    """Insere UM ponto por LINHA INTEIRA e sincroniza o `RESIDUO_N`.

    Levanta em vez de aceitar quando:
      * o provedor nao foi MEDIDO (733) — `edge` ou `piper`, nunca inferido;
      * o pacote ja esta na serie (o ponto fantasma de 18/10);
      * o job ja esta no arquivo (duas pecas nao saem do mesmo job).

    Com `aplicar=False` devolve o que faria e nao grava — porque gravar sem
    conferir e como o passo antigo errava.
    """
    if provedor not in PROVEDORES:
        raise ValueError(
            f"provedor {provedor!r} nao e MEDIDO: conte os avisos "
            "`NARRACAO PELO PIPER` nas anotacoes do job (733), nao infira "
            "pela distancia entre previsao e real")
    t_serie, t_n = _texto(ARQ_SERIE), _texto(ARQ_N)
    ps = pontos(t_serie)
    if any(p[0] == pacote for p in ps):
        raise ValueError(f"{pacote} JA esta na serie — era assim que o ponto "
                         "fantasma de 18/10 as 11:2x nascia")
    if re.search(rf"#\s*job\s*{re.escape(str(job))}\b", t_serie):
        raise ValueError(f"o job {job} ja aparece na serie")

    linha = (f'    ("{pacote}", {prev}, {real}, "{provedor}"),'
             f'  # job {job}\n')
    comentario = ""
    if nota:
        comentario = "".join(f"    # {l}\n" for l in _quebra(nota))

    # Insere ANTES do `]` que fecha a SERIE, achado pela LINHA inteira — nunca
    # por prefixo de outra linha, que foi o defeito.
    linhas = t_serie.splitlines(keepends=True)
    inicio = next(i for i, l in enumerate(linhas) if l.startswith("SERIE = ["))
    fecha = next(i for i, l in enumerate(linhas[inicio:], inicio)
                 if l.rstrip("\n") == "]")
    novo_serie = "".join(linhas[:fecha]) + comentario + linha + \
        "".join(linhas[fecha:])

    alvo = len(ps) + 1
    novo_n, trocas = re.subn(r"^RESIDUO_N = \d+", f"RESIDUO_N = {alvo}",
                             t_n, count=1, flags=re.M)
    if trocas != 1:
        raise RuntimeError("nao consegui sincronizar o RESIDUO_N")

    if aplicar:
        with open(ARQ_SERIE, "w", encoding="utf-8") as f:
            f.write(novo_serie)
        with open(ARQ_N, "w", encoding="utf-8") as f:
            f.write(novo_n)
        d = divergencia()
        if not d["bate"] or d["pacotes_repetidos"] or d["jobs_repetidos"]:
            raise RuntimeError(f"gravei e o arquivo nao esta sao: {d}")
    return {"linha": linha, "residuo": round(real - prev, 1),
            "n": alvo, "limites_depois": limites(ps + [
                (pacote, prev, real, provedor)]), "aplicado": aplicar}


def _quebra(texto: str, largura: int = 72):
    palavras, linha, fora = texto.split(), "", []
    for p in palavras:
        if linha and len(linha) + 1 + len(p) > largura:
            fora.append(linha); linha = p
        else:
            linha = f"{linha} {p}".strip()
    if linha:
        fora.append(linha)
    return fora


def relato() -> str:
    d = divergencia()
    lo, hi = limites()
    fora = [f"SERIE do residuo: {d['n_serie']} pontos, RESIDUO_N {d['n_declarado']}"
            f" — {'BATE' if d['bate'] else '>> DIVERGEM'}",
            f"  banda OBSERVADA: ({lo}; {hi}) s"]
    for chave, titulo in (("pacotes_repetidos", "pacote repetido"),
                          ("jobs_repetidos", "job repetido"),
                          ("linhas_com_duas_marcas_de_job",
                           "linha com DUAS marcas de job")):
        if d[chave]:
            fora.append(f"  >> {titulo}: {d[chave]}")
    if d["bate"] and not any(d[k] for k in
                             ("pacotes_repetidos", "jobs_repetidos",
                              "linhas_com_duas_marcas_de_job")):
        fora.append("  sem ponto duplicado e sem comentario de job pendurado.")
    return "\n".join(fora)


if __name__ == "__main__":
    print(relato())
