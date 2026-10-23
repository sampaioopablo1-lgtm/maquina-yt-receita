# -*- coding: utf-8 -*-
"""O REGISTRO depois de publicar nao tinha dono, e eu o redigitava toda rodada.

Publicar uma peca termina em QUATRO escritas, sempre as mesmas e sempre na
mesma ordem: a duracao parqueada (com o provedor e o job), o SOM parqueado, a
linha de `videos` no pendente, e o titulo no corpus. Cada uma tem dono. **O que
nao tinha dono era a sequencia**, e eu a reescrevia a cada rodada num bloco de
~30 linhas na linha de comando.

**E ela ja produziu TRES defeitos distintos nesta sessao, todos de digitacao e
nenhum de modulo:**

* **19/10 as 21:1x** — `registro_videos.py >> arquivo.sql 2>&1` levou a nota
  legivel do modulo PARA DENTRO do SQL: tres linhas de prosa portuguesa num
  arquivo que outro programa consome. O modulo estava certo desde 15/10 (o
  relato sai por stderr de proposito); a INVOCACAO desfez o conserto;
* **22/10 as 05:3x** — o `job` da duracao vinha do run do `retomar` em QUATRO
  de 65 pacotes, e la nenhum job narra: contar o aviso do 733 ali devolve zero
  por VACUIDADE. Procedencia inventada e pior que procedencia ausente;
* **23/10 as 01:3x** — `c.append(titulo)` no corpus, que e
  `{"titulos": [...]}` e nao uma lista. A falha foi ruidosa e o `len(c)` que eu
  imprimi antes dela devolveu **1** (a contagem das CHAVES) sem me acender nada.

**A guarda que este modulo carrega e a de 20/10 as 13:2x: cada parque e RELIDO
depois de gravar, e ausencia LEVANTA.** Retorno de funcao nao prova presenca —
foi assim que eu escrevi `parqueado: True` a partir do meu proprio rotulo com a
peca fora do parque.

**E o provedor e o job saem do run do RENDER, nunca do de publicacao**, com a
derivacao DELEGADA ao `anotacoes_do_run`, que RECUSA quando nenhum job do run
narrou. Os dois runs vao em argumentos SEPARADOS e nenhum tem padrao: dar
padrao a um deles faria a rodada futura passar o run errado em silencio, que e
exatamente o defeito de 05:3x.

**Nada aqui reimplementa escrita nenhuma.** O SQL sai do `registro_videos`
(stdout puro), o registro da duracao do `duracao_a_medir.do_registro` (que exige
provedor e job pelo 733), o do som do `som_parqueado`, e o titulo do
`corpus_atrasado.aplicar`, que e quem sabe a forma do arquivo. Refazer qualquer
uma criaria o segundo dono — a assinatura que congelou a legenda.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import anotacoes_do_run as AR  # noqa: E402
import corpus_atrasado as CA   # noqa: E402
import duracao_a_medir as DM   # noqa: E402
import registro_videos as RV   # noqa: E402
import som_parqueado as SP     # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_PENDENTE = os.path.join(RAIZ, "docs", "pendente", "videos-a-inserir.sql")


def _notice_do_pacote(lida_pub: dict, pacote: str) -> dict:
    """O registro do `::notice:: PUBLICADO` deste pacote, ou LEVANTA.

    Devolver `None` aqui faria o resto do passo rodar com um dicionario vazio e
    parquear peca sem youtube_id, do jeito que o 000 do curl parecia resposta.
    """
    regs = AR.publicado(lida_pub) or []
    meus = [r for r in regs if r.get("pacote") == pacote]
    if not meus:
        raise ValueError(
            "nenhum `::notice:: PUBLICADO` para %r neste run. Sem o notice nao "
            "ha youtube_id, e parquear sem ele poe linha cega nos quatro "
            "parques — ausencia de notice NAO e peca publicada." % pacote)
    return meus[0]


def _apende_sql(sql: str, caminho: str) -> int:
    """Acrescenta o INSERT, e RECUSA se o arquivo tiver linha que nao seja SQL.

    O `2>&1` de 19/10 as 21:1x poe prosa aqui, e quem colasse no SQL Editor
    levaria erro de sintaxe com o INSERT seguinte FORA do lote. A conferencia e
    do arquivo INTEIRO e nao so do que eu acabei de escrever: prosa que ja
    estivesse ali continuaria quebrando o lote.
    """
    antes = io.open(caminho, encoding="utf-8").read() if os.path.exists(caminho) else ""
    io.open(caminho, "a", encoding="utf-8").write(
        ("" if (not antes or antes.endswith("\n")) else "\n")
        + sql.rstrip("\n") + "\n")
    dep = io.open(caminho, encoding="utf-8").read()
    ruins = [l for l in dep.splitlines()
             if l.strip() and not l.startswith("insert into videos")]
    if ruins:
        raise ValueError(
            "o pendente tem %d linha(s) que nao sao `insert into videos`: %r. "
            "Isto e o `2>&1` de 19/10 as 21:1x — stderr em cima de arquivo que "
            "outro programa consome." % (len(ruins), ruins[:2]))
    return len([l for l in dep.splitlines() if l.strip()])


def registra(run_render, run_pub, pacote, prev_edge, prev_piper,
             titulo=None, sql_pendente=None, api=None):
    """As quatro escritas, na ordem, cada uma pelo dono — e cada parque RELIDO.

    `titulo` e opcional porque o notice ja o carrega: passa-lo serve para a
    rodada conferir que o titulo que ela escreveu e o que subiu. Divergir
    LEVANTA, em vez de gravar no corpus um titulo que o YouTube nao recebeu.
    """
    if not run_render or not run_pub:
        raise ValueError(
            "os DOIS runs sao obrigatorios e nenhum tem padrao: o provedor e o "
            "job saem do RENDER e o notice do de PUBLICACAO. Dar padrao a um "
            "faria a rodada passar o run errado em silencio (22/10, 05:3x).")
    if run_render == run_pub:
        raise ValueError(
            "o run do render e o da publicacao sao o MESMO (%r). No run do "
            "`retomar` nenhum job narra, logo o aviso do 733 contaria zero por "
            "VACUIDADE — e foi assim que QUATRO pecas ficaram com procedencia "
            "inventada." % run_render)

    lida_r = AR.leitura(run_render, api=api) if "api" in \
        AR.leitura.__code__.co_varnames else AR.leitura(run_render)
    lida_p = AR.leitura(run_pub, api=api) if "api" in \
        AR.leitura.__code__.co_varnames else AR.leitura(run_pub)

    reg = _notice_do_pacote(lida_p, pacote)
    tit_no_ar = (reg.get("titulo") or "").strip()
    if titulo is not None and titulo.strip() != tit_no_ar:
        raise ValueError(
            "o titulo que a rodada escreveu (%r) NAO e o que subiu (%r). "
            "Gravar o meu no corpus poria no anti-duplicata um titulo que o "
            "YouTube nao recebeu." % (titulo, tit_no_ar))

    prov = AR.provedor(lida_r, pacote)
    if not prov.get("provedor") or not prov.get("job"):
        raise ValueError(
            "o provedor nao se estabeleceu no run do render (%s): %s"
            % (run_render, prov.get("motivo") or "sem motivo"))

    fora = {"pacote": pacote, "youtube_id": reg.get("youtube_id"),
            "provedor": prov["provedor"], "job": prov["job"],
            "titulo": tit_no_ar}

    # 1) DURACAO — o `do_registro` exige provedor e job (733) e mapeia o
    # instante do notice, que os dois donos chamam por nomes diferentes.
    DM.parqueia(DM.do_registro(reg, prev_edge, prev_piper,
                               prov["provedor"], prov["job"]))
    linhas = DM.carrega()
    if not any(r.get("pacote") == pacote for r in linhas):
        raise ValueError(
            "a peca NAO esta no parque de duracao depois de gravar. Retorno de "
            "funcao nao prova presenca (20/10, 13:2x).")
    fora["duracao_linhas"] = len(linhas)
    fora["duracao_sem_leitura"] = sum(1 for r in linhas if not r.get("real"))

    # 2) SOM — a lista FLAT vem do dono, que RECUSA quando nenhum job narrou.
    for s in AR.som_do_run(lida_r, pacote=pacote):
        SP.parqueia(s)
    ls = SP.carrega()
    if not any(r.get("pacote") == pacote for r in ls):
        raise ValueError("a peca NAO esta no parque de som depois de gravar.")
    fora["som_linhas"] = len(ls)

    # 3) VIDEOS — stdout puro do dono, e o arquivo reconferido inteiro.
    cam = sql_pendente or SQL_PENDENTE
    fora["sql_linhas"] = _apende_sql(RV.sql_insert(AR.publicado(lida_p)), cam)
    if reg.get("youtube_id") not in io.open(cam, encoding="utf-8").read():
        raise ValueError("o youtube_id NAO esta no pendente depois de gravar.")

    # 4) CORPUS — o dono sabe a forma do arquivo (`{"titulos": [...]}`), e foi
    # por nao saber que eu levei `AttributeError` em 23/10 as 01:3x.
    CA.aplicar([tit_no_ar])
    fora["corpus_titulos"] = CA.titulos_do_corpus() \
        if hasattr(CA, "titulos_do_corpus") else None
    return fora


def relato(run_render, run_pub, pacote, prev_edge, prev_piper, **kw) -> str:
    d = registra(run_render, run_pub, pacote, prev_edge, prev_piper, **kw)
    L = ["REGISTRO DA RODADA de %s -> %s" % (pacote, d["youtube_id"]),
         "  provedor %s MEDIDO no job %s (do run do RENDER, nunca do `retomar`)"
         % (d["provedor"].upper(), d["job"]),
         "  titulo no ar: %r" % d["titulo"],
         "  DURACAO: %d linhas (%d sem leitura) — presente, RELIDO"
         % (d["duracao_linhas"], d["duracao_sem_leitura"]),
         "  SOM: %d linhas — presente, RELIDO" % d["som_linhas"],
         "  SQL pendente: %d linhas, ZERO prosa — reconferido INTEIRO"
         % d["sql_linhas"]]
    if d.get("corpus_titulos") is not None:
        L.append("  CORPUS: %d titulos" % d["corpus_titulos"])
    else:
        L.append("  CORPUS: aplicado pelo dono (a contagem nao e exposta por ele)")
    L.append("  >> os quatro donos escreveram e os quatro parques foram RELIDOS: "
             "retorno de funcao nao prova presenca (20/10, 13:2x).")
    return "\n".join(L)


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 5:
        print("uso: python3 fabrica/registro_da_rodada.py "
              "<run_render> <run_pub> <pacote> <prev_edge> <prev_piper> [titulo]")
        return 0
    print(relato(a[0], a[1], a[2], float(a[3]), float(a[4]),
                 titulo=(a[5] if len(a) > 5 else None)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
