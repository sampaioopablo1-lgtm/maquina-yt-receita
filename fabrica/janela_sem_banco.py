"""A janela de 24 h por canal SEM o banco — e os DOIS defeitos que ela mede.

**Aprendizado 775, `alto`, medido em 15/10 as 11:1x, na primeira rodada desta
sessao em que o `execute_sql` recusou.** O contador que escolhe o canal
(`concentracao_frota.relato(janela=...)`) le `videos.publicado_em`, logo morre com
o banco. Existe uma fonte substituta que e DATADA e vive no repo: o `git log` do
`fabrica/corpus_publicados.json`, que ganha uma linha por publicacao.

**E ela tem DOIS defeitos medidos, os dois descobertos ao conferir contra o
numero que o banco dera uma hora antes (24 pecas em 24 h):**

1. **CONTAR LINHAS `+` INFLA POR ~2x.** A primeira versao somou **46**. O corpus
   e regravado com `indent=2` e a lista se REORDENA, entao um titulo reaparece
   como linha adicionada em commits posteriores: **22 dos 24 titulos apareceram
   DUAS vezes**. A contagem certa e por titulo DISTINTO, atribuido ao commit MAIS
   VELHO que o adicionou.

2. **O COMMIT ATRASA CONTRA A PUBLICACAO, e o atraso cai no canal errado.**
   Mesmo corrigido o item 1, o modulo deu **6** no `labtreinamento` contra os
   **7** que o banco dera as 10:07 — porque eu publico e so depois comito. **Um
   contador que subestima justamente o canal que ACABOU de produzir mandaria
   produzir nele de novo**, que e o oposto do que o 762 construiu. Por isso
   `relato` DIZ que e um piso e **recusa ordenar** quando a diferenca entre os
   dois canais mais baixos e de uma peca so.

3. **E O TERCEIRO DEFEITO MATA A CONTAGEM, nao so a enfraquece: TITULO NAO E
   CHAVE DE PUBLICACAO.** Contar titulos DISTINTOS (o conserto do item 1) faz
   duas publicacoes com o MESMO titulo curto colapsarem em uma — e isso nao e
   hipotetico, e o **773**: o `labtreinamento-s051` foi ao ar com o mesmo
   `## TITULO SHORT` do `labtreinamento-s038` (*"Conclusao nao e situacao"*),
   porque a trava comparava o titulo LONGO contra um corpus de CURTOS. Varrida a
   frota, e a UNICA colisao — e ela basta: a janela perde **uma peca do
   labtreinamento**, exatamente o canal onde a colisao aconteceu. Os dois
   consertos se contradizem: contar linhas INFLA, contar distintos PERDE, e o
   corpus e **lista nua** — nao guarda de qual peca e o titulo, logo nao existe
   terceira forma de contar com esta fonte.

**A CONCLUSAO, e ela e uma RECUSA: este modulo NAO ORDENA CANAL.** Medido contra
o banco de uma hora antes (24 pecas em 24 h), ele devolve 22 a 23 e erra o
`labtreinamento` em DUAS — uma pela colisao de titulo (provada) e o resto pelo
atraso do commit. Erro de duas pecas e maior que a distancia que decide a
escolha, entao `ordena` devolve **sempre** `None` e o relato manda usar o outro
criterio.

**O que SOBREVIVE sem o banco, e e o que decidiu a rodada:** a **ULTIMA
publicacao por canal**, que sai dos `created_at` dos runs do `retomar.yml` pela
API do GitHub. E o mesmo desempate MEDIDO do 771 (vence quem tem a peca mais
ANTIGA), e ele nao depende de commit, nem de banco, nem de titulo.

**O que isto NAO e:** substituto do contador do banco. E um PISO declarado com
erro conhecido de ~2 pecas, para a rodada que nao consegue medir — e `relato` diz
isso em letra em vez de calar.
"""
import collections
import datetime
import json
import glob
import os
import re
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = "fabrica/corpus_publicados.json"
FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

# Medido em 15/10 as 11:1x: linhas `+` somadas contra titulos DISTINTOS na mesma
# janela de 24 h. O banco dizia 24, e foi assim que o defeito apareceu.
INFLACAO_MEDIDA = {"linhas": 46, "distintos": 24, "repetidos": 22}


def titulo_curto_por_canal(raiz=None) -> dict:
    """`## TITULO SHORT` -> slug do canal, lido das specs (nao usa banco)."""
    raiz = raiz or RAIZ
    saida = {}
    for f in sorted(glob.glob(os.path.join(raiz, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        m = re.search(r"^##\s*TITULO SHORT\s*$\n+(.+)$", d.get("copy", "") or "", re.M)
        if m:
            saida[m.group(1).strip()] = d.get("slug", "")
    return saida


def _git(args, raiz):
    return subprocess.run(["git"] + args, cwd=raiz, capture_output=True,
                          text=True).stdout


def primeiro_commit_por_titulo(raiz=None) -> dict:
    """titulo -> instante do commit MAIS VELHO que o adicionou ao corpus.

    O `git log` vem do mais novo para o mais velho, entao sobrescrever a chave
    deixa no fim o MAIS VELHO — que e o commit da publicacao de verdade. Contar
    cada ocorrencia seria o defeito 1 deste modulo.
    """
    raiz = raiz or RAIZ
    linhas = [l.split(maxsplit=1) for l in
              _git(["log", "--format=%H %cI", "--", CORPUS], raiz).strip().split("\n")
              if l.strip()]
    saida = {}
    for sha, quando in linhas:
        diff = _git(["show", sha, "--", CORPUS], raiz)
        for add in re.findall(r'^\+\s{4}"(.+?)",?\s*$', diff, re.M):
            saida[add] = quando.strip()
    return saida


def contagem(horas=24, agora=None, raiz=None, mapa=None, primeiro=None):
    """(contagem por canal, ultima por canal) na janela, por titulo DISTINTO."""
    mapa = mapa if mapa is not None else titulo_curto_por_canal(raiz)
    primeiro = primeiro if primeiro is not None else primeiro_commit_por_titulo(raiz)
    agora = agora or datetime.datetime.now(datetime.timezone.utc)
    corte = agora - datetime.timedelta(hours=horas)
    jan, ult = collections.Counter(), {}
    for titulo, quando in primeiro.items():
        canal = mapa.get(titulo)
        if not canal:
            continue
        dt = datetime.datetime.fromisoformat(quando)
        if dt < corte:
            continue
        jan[canal] += 1
        if canal not in ult or dt > ult[canal]:
            ult[canal] = dt
    return dict(jan), ult


ERRO_MEDIDO_EM_PECAS = 2   # labtreinamento 5 aqui contra 7 no banco, 15/10 10:07


def ordena(jan: dict):
    """SEMPRE (None, os dois mais baixos) — este modulo NAO ordena canal.

    E recusa por medicao, nao por zelo: o erro contra o banco e de
    `ERRO_MEDIDO_EM_PECAS`, e uma parte dele e ESTRUTURAL (defeito 3 — titulo nao
    e chave de publicacao, e o corpus e lista nua). Uma margem nao conserta isso,
    porque o erro nao esta limitado por nada que eu tenha medido. Devolver um
    vencedor aqui seria criterio inventado, que e o que a §10 proibe.
    """
    pares = sorted(((jan.get(c, 0), c) for c in FROTA))
    return None, sorted(c for _n, c in pares[:2])


def relato(horas=24, agora=None, raiz=None, mapa=None, primeiro=None) -> str:
    jan, ult = contagem(horas, agora, raiz, mapa, primeiro)
    linhas = [f"JANELA DE {horas} H SEM O BANCO (git log do corpus) — e isto e um"
              " PISO, nao o contador:",
              "  " + ", ".join(f"{c} {jan.get(c, 0)}" for c in FROTA)]
    _baixo, emp = ordena(jan)
    linhas.append(
        "  NAO ORDENA, e a recusa e MEDIDA: contra o banco de 15/10 10:07 este"
        f" modulo erra {ERRO_MEDIDO_EM_PECAS} pecas no labtreinamento (deu 5"
        " contra 7). Uma parte e ESTRUTURAL — titulo nao e chave de publicacao,"
        " e o 773 provou com o `s051`/`s038`, que compartilham o titulo curto e"
        " colapsam em UM. Os dois mais baixos aqui sao " + ", ".join(emp) +
        ", e QUEM DECIDE e a ULTIMA publicacao por canal (`created_at` dos runs"
        " do `retomar.yml`): e o criterio MEDIDO do 771, e ele nao depende de"
        " banco, nem de commit, nem de titulo.")
    if ult:
        linhas.append("  ultimo commit de corpus por canal: " + ", ".join(
            f"{c} {ult[c]:%H:%M}" for c in FROTA if c in ult))
    linhas.append(
        "  (contar linhas `+` INFLA: na janela de 15/10 deu"
        f" {INFLACAO_MEDIDA['linhas']} contra {INFLACAO_MEDIDA['distintos']}"
        f" titulos distintos, porque {INFLACAO_MEDIDA['repetidos']} reaparecem"
        " quando a lista se reordena. Conte DISTINTO.)")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relato())
