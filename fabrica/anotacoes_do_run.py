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


def terminou(jobs: list | dict, status_do_run: str | None = None) -> dict:
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

    E O `todos_terminaram` TAMBEM PRECISA DO STATUS DO RUN — medido em 23/10
    as 00:1x, e custou uma espera que saiu na hora errada. O laco de espera
    perguntou pelo run `39876950273` antes de a matriz existir: havia UM job
    (`preparar`, concluido), logo `pendentes` era zero e `todos_terminaram`
    saiu **True** com o `produzir` ainda por criar. O que me salvou foi a
    guarda de 22/10 as 05:3x, que RECUSOU estabelecer o provedor por
    vacuidade — nao este campo.

    **A lista de jobs de um run em andamento ainda esta sendo POVOADA**, logo
    zero pendente sobre ela e o vazio de instrumento outra vez. Com
    `status_do_run` diferente de `completed` o campo vira **None**, nao False:
    nao se sabe se terminou, e isso e diferente de saber que nao terminou. Sem
    o argumento ele se comporta como antes, porque o payload dos jobs nao traz
    o status do run — e inventar um padrao faria a recusa depender de quem
    chamou lembrar de passa-lo.

    **Os dois campos continuam nao sendo autoridade sozinhos:** o run pode
    dizer `completed` com job em andamento (19:4x) e pode dizer `in_progress`
    com todos os jobs ja criados e feitos. O veredito pede os DOIS.
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
    todos = bool(saida) and pend == 0
    run_aberto = (status_do_run is not None
                  and str(status_do_run) != "completed")
    if todos and run_aberto:
        todos = None
    return {
        "jobs": saida,
        "n": len(saida),
        "pendentes": pend,
        "todos_terminaram": todos,
        "status_do_run": status_do_run,
        "run_aberto": run_aberto,
        "divergem": div,
        "motivo": None if not div else (
            "%d job(s) com TODOS os passos concluidos e `conclusion` ainda "
            "nulo: o campo de status esta atrasado e os PASSOS sao a medida. "
            "Medido em 22/10 as 19:4x, quando esperar o campo custou 25 "
            "minutos com a peca ja publicada." % div),
    }


def relato_do_termino(jobs: list | dict,
                      status_do_run: str | None = None) -> str:
    """UM dono da frase, e ela sai nos DOIS ramos — com e sem divergencia.

    E A PRIMEIRA LINHA CARREGA O VEREDITO, nao a contagem de pendentes:
    medido em 23/10 as 00:1x, o laco de espera grepava `0 pendente` e com a
    matriz ainda por criar essa contagem E zero. Quem le a contagem le a
    coisa errada; o campo que decide e o `todos_terminaram`, e agora ele sai
    em letra. **Grepe `TERMINOU: SIM`.**
    """
    q = terminou(jobs, status_do_run)
    rotulo = {True: "SIM", False: "NAO", None: "INDETERMINADO"}[
        q["todos_terminaram"]]
    L = ["TERMINO DO RUN: %d job(s), %d pendente(s). TERMINOU: %s"
         % (q["n"], q["pendentes"], rotulo)]
    for j in q["jobs"]:
        L.append("  %s %s — conclusion=%r, passos %d/%d, terminado=%r"
                 % (j["id"], (j["nome"] or "?")[:46], j["conclusao"],
                    j["passos_concluidos"], j["passos"], j["terminado"]))
    if q["run_aberto"] and q["pendentes"] == 0:
        L.append("  >> o RUN ainda esta %r: a lista de jobs de um run em "
                 "andamento ainda esta sendo POVOADA, logo zero pendente "
                 "sobre ela e vazio de instrumento. Medido em 23/10 as 00:1x, "
                 "quando havia so o `preparar` e o `produzir` nem existia."
                 % str(q["status_do_run"]))
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


def fatia_de_job(lida: dict, pacote: str | None = None) -> dict:
    """O que `jobs[0]` e, e se ele e o job de onde a PROCEDENCIA sai.

    **POR QUE ISTO EXISTE, e a medicao e de 23/10 as 08:4x, nesta rodada.** Eu
    fui ler o `::notice:: PUBLICADO` a mao, com
    `gh api .../jobs --jq '.jobs[0].id'` e depois
    `check-runs/<job>/annotations` — quando este modulo ja responde isso. E o
    `[0]` e uma FATIA: a ponta de uma lista lida como se fosse a lista, que e a
    familia do `[:3]` da lista do proxy (19/10 as 19:2x), do `tail -10` das
    formas (21/10 as 23:2x) e do `sed -n '45,90p'` dos capitulos livres (22/10
    as 10:3x).

    **Medido nos dois runs desta rodada:** no run do RENDER (`39923653381`)
    `jobs[0]` e o **`preparar`** (`120314658279`) e quem narrou e o
    **`produzir`** (`120314685498`); no run do `retomar` (`39924132717`) ha UM
    job, logo a fatia acerta. Isto e, **a rota a mao esta errada em todo run de
    render e acertou aqui por ACIDENTE** — a mesma forma do acordo acidental
    dos dois caminhos de saida (22/10 as 00:3x) e do casamento de host (01:1x).

    E o custo nao e cosmetico: contar o aviso do 733 no `preparar` devolve zero
    por **VACUIDADE**, que e o defeito que pos job inventado na procedencia de
    quatro pecas. O `provedor` RECUSA ali; a fatia nao recusa nada.

    **Isto NOMEIA e nao decide:** o veredito do provedor continua saindo do
    `provedor`, pelo discriminador MEDIDO (job que emitiu `SOM` narrou), nunca
    do indice nem do NOME do job.
    """
    jobs = lida["jobs"]
    primeiro = jobs[0]["id"] if jobs else None
    try:
        dono = provedor(lida, pacote)["job"]
    except SemProcedencia:
        dono = None
    return {"primeiro": primeiro, "n_jobs": len(jobs),
            "job_do_provedor": dono,
            "fatia_acerta": None if dono is None else primeiro == dono}


def divergencia_de_titulo(lida: dict) -> dict:
    """O titulo tem DOIS donos, e eles nao medem a mesma coisa.

    **MEDIDO em 23/10 as 08:4x, e isto RETRATA o que o `registro_da_rodada`
    afirma de si.** O docstring dele diz que passar o titulo *"serve para a
    rodada conferir que o titulo que a rodada escreveu e o que subiu"*.
    **Falso.** A linha de `videos` do `registro_videos` monta, para short,
    `titulo = titulo_short(spec) or titulo_do_notice` — isto e, **a SPEC vence e
    o notice e ignorado**. Logo a conferencia compara a minha digitacao contra a
    NOSSA propria spec: os dois lados sao nossos, e o que o YouTube de fato
    recebeu nao entra na conta.

    Reproduzido: um notice dizendo `titulo=UM TITULO QUE A SPEC NAO TEM` devolve
    a linha com o titulo da spec, sem ninguem dizer nada.

    **E o custo nao e teorico.** Em 19/10 as 14:4x TRES pacotes subiram o short
    com o titulo do LONGO, porque a copy nao trazia `## TITULO SHORT` — isto e,
    o que subiu diverge do que a gente quis, e o **notice e a unica testemunha
    disso**. E o corpus, que a trava de titulo duplicado do `prontidao` le
    (773), e alimentado com o titulo da LINHA: titulo nosso no corpus poe no
    anti-duplicata um titulo que o YouTube nunca recebeu, e a trava fica cega
    naquela peca — em silencio e no sentido PERMISSIVO.

    **Medido no disco:** das 445 specs com short, **338 trazem** a secao (ali a
    spec vence e o notice e ignorado) e **107 nao** (ali a linha CAI no titulo
    do notice). Os dois lados existem, logo o cruzamento nao passa por
    vacuidade.

    **Isto NOMEIA; quem RECUSA e o `registro_da_rodada`**, porque e ele que
    grava no corpus. E as duas leituras sao DELEGADAS aos donos — reparsear o
    notice aqui criaria o terceiro dono da forma dele.
    """
    import corpus_atrasado as CA
    texto = "\n".join(m for j in lida["jobs"] for m in j["mensagens"])
    # A chave e o `youtube_id` e NAO o `pacote`, e isto e o conserto de um FALSO
    # POSITIVO MEDIDO em 23/10 as 13:5x, no PRIMEIRO pacote desde que esta
    # funcao nasceu (08:4x do mesmo dia, vista so em short solto): um pacote
    # emite DOIS notices com o MESMO `pacote` — o longo e o short —, logo um
    # dicionario chaveado por pacote guarda so o ULTIMO e compara a linha do
    # SHORT contra o titulo do LONGO. Ele acusou o `epomeno-epipedo-069` de ter
    # subido o short com o titulo do longo quando os notices crus dizem o
    # contrario:
    #   PUBLICADO ... shorts youtube_id=D07pVhb6Qrc titulo=Ena charti...
    #   PUBLICADO ... longo  youtube_id=e_irNzHj1jc titulo=O Fakelos...
    # **Detector que inventa achado e pior que nao ter detector (725)** — e aqui
    # ele fez o `registro_da_rodada` LEVANTAR, os quatro parques ficaram sem
    # escrever e a rodada quase relatou ao dono um defeito que a maquina nao
    # cometeu. O `youtube_id` e unico por peca, e e por ele que as duas leituras
    # falam da MESMA peca.
    #
    # E o lado do LONGO e VACUO, e isso vai dito: a linha dele COPIA o titulo do
    # proprio notice (`registro_videos`), logo os dois lados sao o mesmo valor e
    # o cruzamento so tem dentes no SHORT — que e onde o incidente de 19/10 as
    # 14:4x ocorreu.
    do_notice = {y: tit for _p, y, tit in CA.titulos_dos_notices(texto)}
    pares, div = [], []
    for ln in publicado(lida):
        yid = ln.get("youtube_id")
        if yid not in do_notice:
            continue
        nosso, testemunha = ln.get("titulo"), do_notice[yid]
        pares.append(yid)
        if (nosso or "").strip() != (testemunha or "").strip():
            div.append({"pacote": ln.get("pacote"), "youtube_id": yid,
                        "da_linha": nosso, "do_notice": testemunha})
    return {"pares": len(pares), "divergentes": div,
            "do_notice": do_notice}


_PRE_PUB = "  PUBLICADO: "


def _linha_do_publicado(lida: dict) -> list:
    """UM dono das linhas do PUBLICADO, e elas saem nos DOIS ramos.

    **O TITULO ia junto e era jogado fora — medido em 23/10 as 08:4x.** A linha
    de `videos` que o `publicado` devolve carrega `titulo`, `publicado_em`,
    `canal` e `origem_id`, e o relato imprimia so o par pacote -> id. Logo a
    unica forma de ver o titulo que de fato subiu era eu reler o notice a mao —
    e o titulo e exatamente o valor que o `registro_da_rodada` CONFERE e que o
    faz LEVANTAR quando divergir, porque o corpus guarda o titulo CURTO e a
    trava de titulo duplicado do `prontidao` compara contra ele (773). Titulo
    meu no corpus poe no anti-duplicata um titulo que o YouTube nao recebeu, e
    a trava fica cega naquela peca, em silencio e no sentido PERMISSIVO.

    E a forma do defeito e a desta casa: dado que existe um nivel acima e nao
    desce — o `quadro` que o `contagem_de_cenas` calculava e descartava (20/10,
    03:2x), a prosa que o `irmaos_da_origem` prometia e nao imprimia (15:3x), a
    nota da rota no ramo que calava (13:2x) e o `run` que o `_som_do_job` nao
    recebia (22/10, 06:2x).
    """
    linhas = []
    d = divergencia_de_titulo(lida)
    for ln in publicado(lida):
        pac = ln.get("pacote")
        test = d["do_notice"].get(pac)
        linhas.append(_PRE_PUB + "%s -> %s  em=%s\n    titulo que SUBIU (do "
                      "notice, a testemunha): %r\n    titulo da LINHA (da "
                      "nossa spec, o que vai ao corpus): %r%s"
                      % (pac, ln.get("youtube_id"), ln.get("publicado_em"),
                         test, ln.get("titulo"),
                         "" if test is None or
                         (test or "").strip() == (ln.get("titulo") or "").strip()
                         else "  << DIVERGEM: o corpus receberia um titulo que o"
                              " YouTube nao recebeu, e a trava do 773 ficaria"
                              " cega nesta peca"))
    if not linhas:
        linhas.append(_PRE_PUB + "nenhum `::notice:: PUBLICADO` neste run — o "
                      "que e o normal no run do RENDER, que publica nada. "
                      "Ausencia de notice NAO e peca sem publicar: quem diz "
                      "isso e o run do `retomar`.")
    return linhas


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
    linhas.extend(_linha_do_publicado(lida))
    f = fatia_de_job(lida, pacote)
    if f["n_jobs"] > 1 and f["fatia_acerta"] is False:
        linhas.append("  FATIA: `jobs[0]` deste run e o %s e NAO e o job de "
                      "onde a procedencia sai (%s) — contar o aviso do 733 ali "
                      "devolve zero por VACUIDADE. Medido em 23/10 as 08:4x."
                      % (f["primeiro"], f["job_do_provedor"]))
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
        # o status do RUN vem de uma SEGUNDA chamada de proposito: o payload
        # dos jobs nao o traz, e sem ele o `todos_terminaram` sai True sobre
        # uma lista que ainda esta sendo povoada (23/10 as 00:1x).
        cab = _api("repos/%s/actions/runs/%s" % (REPO, run)) or {}
        print(relato_do_termino(bruto, (cab or {}).get("status")))
        return 0
    run = argv[0] if argv else None
    pacote = argv[1] if len(argv) > 1 else None
    print(relato(run, pacote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
