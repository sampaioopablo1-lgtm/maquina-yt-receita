#!/usr/bin/env python3
"""As ANOTACOES de um run lidas UMA vez, e o job do provedor DERIVADO delas.

POR QUE ISTO EXISTE, e e defeito MEDIDO do parque, nao conveniencia minha.

O 733 estabeleceu que o provedor de cada cena e OBSERVAVEL: um
`::warning:: NARRACAO PELO PIPER` por cena do Piper, zero se o edge venceu —
*"antes de inferir qual provedor narrou, CONTE OS AVISOS"*. Desde entao eu
contei esse aviso com um `--jq` escrito na hora, li o `::notice:: SOM` com os
olhos e REDIGITEI o JSON dele como literal Python, e digitei o `job` a mao
dentro do `duracao_a_medir.do_registro`. Tres transcricoes por rodada, e e o
item 3 da §10 na OITAVA dimensao: canal (19/10 as 11:2x), cota (23:3x), cenas
(20/10 as 02:2x), pauta (08:2x), dono da origem (10:1x), som (21/10 as 22:3x),
contrato do render (22/10 as 02:5x) e agora as ANOTACOES.

**E o `job` tinha DOIS DONOS, cada um preenchido por uma transcricao minha
diferente — e eles DIVERGIAM em silencio.** Medido em 22/10 as 05:3x cruzando
`duracoes-a-medir.jsonl` com `som-medido.jsonl`: de **65** pacotes com job nos
dois parques, **QUATRO** divergem — `epomeno-epipedo-s072`,
`kolejny-poziom-s073`, `kolejny-poziom-s074` e `labtreinamento-s091`.

**E nos quatro o job do parque de DURACAO e o do `retomar`, nao o do render.**
Conferido na API, aqueles quatro jobs tem tres anotacoes cada — a do Node, a do
`ubuntu-latest` e o `PUBLICADO` — e **zero** aviso do Piper e **zero** SOM.
Logo o *"provedor edge MEDIDO (zero avisos no job X)"* que eu escrevi para as
quatro contou o aviso do 733 **num job que nunca narra**: o zero era VACUO, a
mesma forma do `or True` de 16/10 e do `except Exception: continue` de 12/10.

**A conclusao SOBREVIVEU, e isso e SORTE e nao metodo:** contados nos jobs
`produzir` de verdade (`118434208097`, `118449827173`, `118505061977`,
`118524197854`), os quatro dao **zero** aviso, logo as quatro pecas foram
mesmo narradas pelo edge. O que estava errado era a PROCEDENCIA, e procedencia
inventada e pior que procedencia ausente (19/10 as 07:2x), porque convida a
conferir no lugar errado.

**O DISCRIMINADOR NAO E O NOME DO JOB, e e por isso que ele e barato:** job que
emitiu `SOM` **mediu audio**, logo narrou; job que emitiu `PUBLICADO` subiu a
peca. Contar o aviso do Piper so vale no primeiro, e isso e PROPRIEDADE da
anotacao e nao da string `produzir` na coluna do nome — que e convencao do
workflow e pode mudar sem ninguem avisar.

E as duas leituras sao **DELEGADAS**: o `::notice:: SOM` vira registro pelo
`som_parqueado.do_notice` e o `PUBLICADO` pelo
`registro_videos.linhas_dos_notices`. Reparsear aqui criaria o segundo dono de
cada forma — a assinatura que congelou a legenda.

NAO E PORTAO e nao tem o que reprovar: isto responde uma pergunta sobre um RUN.
Codigo de saida sempre zero.

    python3 fabrica/anotacoes_do_run.py <run_id> [pacote]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REPO = "sampaioopablo1-lgtm/maquina-yt-receita"

# A marca do 733. Ela vive no `voz_piper.aviso_de_calibracao`, e ha teste desde
# aquele dia que reprova se alguem a trocar por `print` — sem ela o provedor
# volta a ser inferido no olho.
MARCA_PIPER = "NARRACAO PELO PIPER"


class SemProcedencia(Exception):
    """A pergunta nao pode ser respondida DESTE run sem inventar nada."""


def _api(caminho: str) -> object:
    """A chamada crua, isolada para o teste poder injetar outra no lugar."""
    out = subprocess.run(["gh", "api", caminho], capture_output=True, text=True)
    if out.returncode != 0:
        raise SemProcedencia("`gh api %s` falhou: %s"
                             % (caminho, (out.stderr or "").strip()[:200]))
    return json.loads(out.stdout or "null")


def leitura(run: str | int, api=None) -> dict:
    """Os jobs do run e as anotacoes de cada um, numa leitura so.

    Devolve `{run, jobs: [{id, nome, conclusao, mensagens: [...]}]}`. Run sem
    job nenhum LEVANTA, do jeito que o `porta1` recusa janela curta: zero job e
    indistinguivel de run que nao existe, e seguir daria contagem vacua.
    """
    chamada = api or _api
    run = str(run)
    jobs = (chamada("repos/%s/actions/runs/%s/jobs" % (REPO, run)) or {})
    jobs = jobs.get("jobs") if isinstance(jobs, dict) else jobs
    if not jobs:
        raise SemProcedencia(
            "o run %s nao devolveu job nenhum: zero job e indistinguivel de run"
            " inexistente, e contar aviso numa lista vazia e o zero VACUO que"
            " esta nota descreve" % run)
    saida = []
    for j in jobs:
        anot = chamada("repos/%s/check-runs/%s/annotations"
                       % (REPO, j.get("id"))) or []
        saida.append({
            "id": str(j.get("id")),
            "nome": j.get("name"),
            "conclusao": j.get("conclusion"),
            "mensagens": [a.get("message") or "" for a in anot],
        })
    return {"run": run, "jobs": saida}


def terminou(jobs: list | dict) -> dict:
    """Aquele job acabou? E a resposta NAO sai do campo `conclusion`.

    **Medido em 22/10 as 19:4x, e custou 25 minutos de espera.** Em 13:4x eu
    media o contrario — o RUN dizia `completed/success` com o job `produzir`
    ainda `in_progress` — e a regra que eu escrevi foi *"espere pelos JOBS, nao
    pelo RUN"*. **Nesta rodada foi o endpoint dos JOBS que mentiu:** o
    `retomar` publicou as 19:20:07 (`::notice:: PUBLICADO ... youtube_id=...`),
    o run voltou `completed/success`, o artefato do registro existia — e
    `/actions/runs/<id>/jobs` seguiu devolvendo `status: in_progress,
    conclusion: null` por vinte e cinco minutos, com as anotacoes vazias
    porque o check-run tambem estava preso.

    **Logo os dois endpoints DISCORDAM nos DOIS sentidos, e nenhum dos dois
    campos de status e autoridade.** A regra de 13:4x fica RETRATADA na parte
    que elegia um deles; o que sobrevive dela e o aviso de que o campo de
    status do RUN nao prova que o trabalho acabou.

    **E o discriminador estava DENTRO do mesmo payload que eu ja lia:** o
    `/jobs` traz `steps` por job, e nesta medicao os **quinze** passos estavam
    `completed/success` enquanto o job dizia `in_progress`. Eu lia o campo
    errado do dicionario certo — a familia do `.get(chave, default)` sobre a
    resposta errada (08:3x), agora com a chave certa e o campo errado.

    A regra: **job cujos PASSOS acabaram todos esta terminado**, mesmo com
    `conclusion` nulo, e a divergencia sai NOMEADA em vez de escondida — quem
    a esconder faz a rodada seguinte esperar o campo que nao vem.

    **Passo NENHUM visivel nao decide**, e devolve `terminado: None`: um job
    que ainda nao comecou tambem nao tem passo concluido, e chamar isso de
    terminado seria o vazio de instrumento lido como ausencia (17/10).
    """
    if isinstance(jobs, dict):
        jobs = jobs.get("jobs") if "jobs" in jobs else [jobs]
    saida, pend, div = [], 0, 0
    for j in jobs or []:
        passos = list(j.get("steps") or [])
        feitos = [s for s in passos if s.get("conclusion") is not None]
        por_passo = bool(passos) and len(feitos) == len(passos)
        por_campo = j.get("conclusion") is not None
        if not passos:
            terminado = None
        else:
            terminado = por_campo or por_passo
        if terminado is not True:
            pend += 1
        if por_passo and not por_campo:
            div += 1
        saida.append({
            "id": str(j.get("id")),
            "nome": j.get("name"),
            "conclusao": j.get("conclusion"),
            "status": j.get("status"),
            "passos": len(passos),
            "passos_concluidos": len(feitos),
            "por_campo": por_campo,
            "por_passo": por_passo,
            "terminado": terminado,
        })
    return {
        "jobs": saida,
        "n": len(saida),
        "pendentes": pend,
        "todos_terminaram": bool(saida) and pend == 0,
        "divergem": div,
        "motivo": None if not div else (
            "%d job(s) com TODOS os passos concluidos e `conclusion` ainda "
            "nulo: o campo de status esta atrasado e os PASSOS sao a medida. "
            "Medido em 22/10 as 19:4x, quando esperar o campo custou 25 "
            "minutos com a peca ja publicada." % div),
    }


def relato_do_termino(jobs: list | dict) -> str:
    """UM dono da frase, e ela sai nos DOIS ramos — com e sem divergencia."""
    q = terminou(jobs)
    L = ["TERMINO DO RUN: %d job(s), %d pendente(s)." % (q["n"], q["pendentes"])]
    for j in q["jobs"]:
        L.append("  %s %s — conclusion=%r, passos %d/%d, terminado=%r"
                 % (j["id"], (j["nome"] or "?")[:46], j["conclusao"],
                    j["passos_concluidos"], j["passos"], j["terminado"]))
    if q["divergem"]:
        L.append("  >> %s" % q["motivo"])
    else:
        L.append("  >> os PASSOS e o campo `conclusion` concordam nesta "
                 "leitura — e eles discordam nos DOIS sentidos (13:4x o RUN "
                 "adiantou, 19:4x o JOB atrasou), logo nenhum campo de status "
                 "e autoridade sozinho.")
    return "\n".join(L)


def _som_do_job(job: dict, run: str | None = None) -> list:
    """Os `::notice:: SOM` daquele job, virados em registro pelo DONO deles.

    **O `run` ENTRA, e ele nao entrava.** Medido em 22/10 as 06:2x, na PRIMEIRA
    peca parqueada por este modulo: das 69 linhas do `som-medido.jsonl` a dela
    foi a UNICA sem o campo `run`, porque a `leitura` tem o run na mao e o
    `_som_do_job` nao o recebia. Ele e OPCIONAL no parque, logo a falha e
    SILENCIOSA — nada levantou —, e a procedencia da leitura ficou pela metade
    num modulo escrito para que ela deixasse de ser digitada. E a mesma forma do
    `quadro` que o `contagem_de_cenas` calculava e jogava fora (20/10, 03:2x): o
    dado existia um nivel acima e nao descia.
    """
    import som_parqueado as SP
    fora = []
    for m in job["mensagens"]:
        linha = (m or "").strip()
        if not linha.startswith("SOM ") and "::notice::SOM" not in linha:
            continue
        try:
            fora.append(SP.do_notice(linha, job=job["id"], run=run))
        except Exception:
            # Forma que o DONO nao reconhece nao vira registro: inventar um aqui
            # seria o segundo dono da forma da anotacao.
            continue
    return fora


def jobs_que_narraram(lida: dict, pacote: str | None = None) -> list:
    """Os jobs em que contar o aviso do 733 NAO e vacuo.

    O discriminador e PROPRIEDADE da anotacao e nao o nome do job: job que
    emitiu `SOM` mediu audio, logo narrou. Era o nome que eu usava sem dizer, e
    foi contar num job de `retomar` que produziu as quatro procedencias erradas
    de 22/10 as 05:3x.
    """
    fora = []
    for j in lida["jobs"]:
        sons = _som_do_job(j, run=lida.get("run"))
        if not sons:
            continue
        if pacote and not any(s["pacote"] == pacote for s in sons):
            continue
        fora.append({"id": j["id"], "nome": j["nome"],
                     "som": sons,
                     "avisos_piper": sum(1 for m in j["mensagens"]
                                         if MARCA_PIPER in (m or ""))})
    return fora


def som_do_run(lida: dict, pacote: str | None = None) -> list:
    """A lista FLAT dos registros de SOM do run — com UM dono e com RECUSA.

    **POR QUE ELA EXISTE (22/10, 08:3x): ela morava DENTRO do `provedor` e eu a
    procurei no `leitura`.** A `leitura` devolve exatamente DUAS chaves — `run`
    e `jobs` — e `som` nunca foi uma delas; eu escrevi
    `for s in leitura(run).get("som", []):` e o laco **nao rodou nenhuma vez**.
    Nada levantou, nada foi parqueado, e a chamada imprimiu o `run` como se
    tivesse funcionado: o unico discriminador foi RELER o parque, que respondeu
    `s107 presente: False` (a disciplina de 20/10 as 13:2x).

    **E a FAMILIA ganha o oitavo membro, na forma mais confortavel dela:**

    | | |
    |---|---|
    | 17/10 | instrumento que devolve VAZIO nao prova ausencia |
    | 19/10 | arquivo VAZIO nao prova morte |
    | 20/10 01:4x | instrumento CHEIO nao prova presenca (o `pgrep` se vendo) |
    | 20/10 09:3x | 000 nao diz de QUEM e o zero |
    | 20/10 11:4x | 000 em TODO host nao separa REDE de POLITICA |
    | 20/10 12:3x | vazio CAMUFLADO por um estado legitimo do instrumento |
    | 21/10 21:0x | arquivo que EXISTE nao prova que e DESTA execucao |
    | **22/10 08:3x** | **`.get(chave, default)` sobre a resposta ERRADA e vazio BEM FORMADO** |

    O `.get` com default e pior que o `glob` de 20/10 as 12:3x porque ele nao
    depende de erro de caminho nenhum: a chave simplesmente **nunca existiu**
    naquela resposta, e o default a faz parecer uma lista legitimamente vazia.

    **E o dado estava VISIVEL:** o `relato` imprime a linha do SOM, logo a
    rodada ve o som e nao tem funcao nenhuma que o entregue com esse nome — a
    lista flat so existia como `provedor(...)["som"]`, dentro de uma funcao cujo
    NOME e sobre o provedor. E a forma do `quadro` que o `contagem_de_cenas`
    calculava e jogava fora (20/10, 03:2x), um nivel acima.

    RECUSA quando nenhum job do run narrou, do jeito que o `porta1` recusa
    janela curta — e devolver `[]` ali seria refazer o defeito que esta funcao
    conserta. A leitura e DELEGADA ao `jobs_que_narraram`: reparsear a anotacao
    aqui criaria o segundo dono da forma dela.
    """
    narraram = jobs_que_narraram(lida, pacote)
    if not narraram:
        raise SemProcedencia(
            "nenhum job do run %s emitiu `SOM`%s: devolver lista vazia aqui"
            " seria o vazio BEM FORMADO que esta funcao conserta (22/10 as"
            " 08:3x), e e indistinguivel de run cujo som ninguem leu"
            % (lida["run"], " para %s" % pacote if pacote else ""))
    return [s for j in narraram for s in j["som"]]


def provedor(lida: dict, pacote: str | None = None) -> dict:
    """`edge` ou `piper` pela CONTAGEM (733), com o job de onde ela saiu.

    RECUSA quando nenhum job do run narrou: zero aviso num job que nao narra
    nao mede provedor nenhum, e foi exatamente esse zero que eu reportei como
    medicao em quatro pecas.
    """
    narraram = jobs_que_narraram(lida, pacote)
    if not narraram:
        raise SemProcedencia(
            "nenhum job do run %s emitiu `SOM`%s, logo nenhum deles narrou: "
            "contar o aviso do 733 aqui devolveria zero por VACUIDADE, que e o "
            "defeito medido em 22/10 as 05:3x (quatro pecas com o job do "
            "`retomar` como procedencia do provedor)"
            % (lida["run"], " para %s" % pacote if pacote else ""))
    total = sum(j["avisos_piper"] for j in narraram)
    return {
        "provedor": "piper" if total else "edge",
        "avisos_piper": total,
        "job": narraram[0]["id"],
        "jobs": [j["id"] for j in narraram],
        # A lista flat tem UM dono, e e o `som_do_run` — remonta-la aqui era o
        # que a escondia atras de um nome sobre o provedor (22/10, 08:3x).
        "som": som_do_run(lida, pacote),
    }


def publicado(lida: dict) -> list:
    """As linhas de `videos` dos `::notice:: PUBLICADO`, pelo DONO delas."""
    import registro_videos as RV
    texto = "\n".join(m for j in lida["jobs"] for m in j["mensagens"])
    return RV.linhas_dos_notices(texto)


def divergencias_de_job(duracao: list | None = None,
                        som: list | None = None) -> dict:
    """O `job` tem DOIS donos; isto cruza os dois e nomeia quem discorda.

    As duas listas sao DELEGADAS ao `carrega` de cada parque: reler os arquivos
    aqui criaria o terceiro leitor deles.
    """
    import duracao_a_medir as DM
    import som_parqueado as SP
    d = DM.carrega() if duracao is None else duracao
    s = SP.carrega() if som is None else som
    por_som = {}
    for x in s:
        if x.get("job"):
            por_som.setdefault(x.get("pacote"), set()).add(str(x["job"]))
    comuns, div = [], []
    for x in d:
        p, j = x.get("pacote"), x.get("job")
        if not j or p not in por_som:
            continue
        comuns.append(p)
        if str(j) not in por_som[p]:
            div.append({"pacote": p, "duracao": str(j),
                        "som": sorted(por_som[p])})
    return {"comuns": len(comuns), "divergentes": div}


def relato(run: str | int | None = None, pacote: str | None = None,
           api=None) -> str:
    linhas = []
    cruz = divergencias_de_job()
    linhas.append("JOB nos DOIS parques: %d pacote(s) em comum, %d divergente(s)"
                  % (cruz["comuns"], len(cruz["divergentes"])))
    for x in cruz["divergentes"]:
        linhas.append("  DIVERGE %s: duracao=%s som=%s"
                      % (x["pacote"], x["duracao"], ", ".join(x["som"])))
    if not cruz["divergentes"]:
        linhas.append("  os dois donos concordam — e foi a divergencia em QUATRO"
                      " de 65 que mostrou que o job vinha da minha digitacao")
    if run is None:
        return "\n".join(linhas)
    lida = leitura(run, api=api)
    linhas.append("RUN %s: %d job(s)" % (lida["run"], len(lida["jobs"])))
    try:
        p = provedor(lida, pacote)
        linhas.append("  PROVEDOR %s — %d aviso(s) `%s`, no job %s"
                      % (p["provedor"].upper(), p["avisos_piper"], MARCA_PIPER,
                         p["job"]))
        for s in p["som"]:
            linhas.append("  SOM %s %s: %s LUFS, pico %s dBTP, %d silencio(s)"
                          % (s["arquivo"], s["pacote"], s["lufs"],
                             s["pico_dbtp"], len(s["silencios"] or [])))
    except SemProcedencia as e:
        linhas.append("  PROVEDOR nao estabelecido: %s" % e)
    for ln in publicado(lida):
        linhas.append("  PUBLICADO %s -> %s" % (ln.get("pacote"),
                                                ln.get("youtube_id")))
    return "\n".join(linhas)


def main(argv: list | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    # `--termino <run>`: a pergunta do laco de espera, e ela NAO passa pelo
    # `leitura` porque o que ela precisa sao os `steps`, que o endpoint dos
    # jobs traz e o `leitura` nao guarda. Sem este chamador o `terminou` seria
    # a classe dos layouts mortos: codigo escrito que ninguem chama.
    if argv and argv[0] == "--termino":
        run = argv[1] if len(argv) > 1 else None
        bruto = _api("repos/%s/actions/runs/%s/jobs" % (REPO, run)) or {}
        print(relato_do_termino(bruto))
        return 0
    run = argv[0] if argv else None
    pacote = argv[1] if len(argv) > 1 else None
    print(relato(run, pacote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
