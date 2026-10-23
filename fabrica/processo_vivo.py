#!/usr/bin/env python3
"""O `pgrep -f` casa a PROPRIA linha de comando — e eu reportei "VIVO" tres vezes.

Medido em 20/10 as 01:5x, e e o espelho exato do defeito de 19/10 as 16:2x,
cometido DENTRO do conserto dele.

ONTEM eu declarei morta uma suite que estava viva, porque li o arquivo que ela
ainda nao tinha terminado de escrever. A regra que eu escrevi no `CLAUDE.md`
foi: "antes de dizer que uma execucao morreu, pergunte ao SISTEMA se o
processo existe", e o discriminador que eu nomeei foi `pgrep -fa pytest`.

HOJE eu perguntei ao sistema exactamente assim — `pgrep -f "pytest tests"` —
e ele respondeu com a MINHA PROPRIA PERGUNTA. O `-f` casa a linha de comando
INTEIRA, e o laco de espera que eu montei era

    until ! pgrep -f "pytest tests" > /dev/null; do sleep 20; done

cuja propria linha de comando contem o texto `pytest tests`. Logo o laco casa
a si mesmo e NUNCA sai, e cada consulta minha devolvia os PIDs dos lacos de
espera. Medido: quatro PIDs, nenhum deles python, a suite havia terminado
havia minutos com 25 falhas e conjunto identico a base.

**E o par das duas rodadas e a licao, nao cada uma delas:**

    17/10  instrumento que devolve VAZIO nao prova ausencia  (o grep dos inscritos)
    19/10  arquivo que devolve VAZIO nao prova morte          (o .norm a meio de escrever)
    20/10  instrumento que devolve CHEIO nao prova presenca   (o pgrep se vendo)

A terceira e a mais barata de evitar e a mais cara de nao ver, porque VAZIO me
deixa desconfiado e CHEIO me deixa tranquilo. Eu relatei "VIVO, 54%" e "VIVO,
100%" ao dono com a suite ja encerrada.

O DISCRIMINADOR, e ele e de uma linha: um processo de pytest e um processo
cujo EXECUTAVEL e python. Laco de espera, `pgrep`, `grep` e shell nao sao. Por
isso aqui a pergunta nao e "existe linha de comando com este texto" e sim
"existe processo cujo `comm` e python E cujos argumentos tem este texto" — e o
PID desta propria chamada sai fora por construcao.

NAO E PORTAO e nao tem o que reprovar: isto responde uma pergunta sobre o
SISTEMA, nao sobre uma peca. Codigo de saida: 0 se o padrao tem processo vivo,
1 se nao tem — porque este modulo existe para ser usado dentro de `until`:

    until ! python3 fabrica/processo_vivo.py "pytest tests"; do sleep 20; done

A NEGACAO E OBRIGATORIA e vai escrita aqui porque faltou na linha que o
`CLAUDE.md` publicava: `until CMD` para quando o comando ACERTA, e 0 e VIVO,
logo `until` sem `!` espera o processo COMECAR. Em 21/10 as 22:3x eu copiei a
forma sem a negacao, o laco voltou em um minuto e eu relatei "a execucao saiu"
com doze pontos no log — o mesmo tipo de erro do `2>&1` de 19/10, em que o
modulo estava certo e a INVOCACAO desfazia o conserto.
"""
import os
import subprocess
import sys

# O que NAO conta como o processo que eu procuro, por mais que a linha de
# comando casse. A lista e de SHELLS e de FERRAMENTAS DE BUSCA, e nao de
# nomes do que eu espero: nomear o esperado seria identidade onde ha
# propriedade (743/753/761) — a propriedade e "nao e o interpretador".
NAO_SAO_O_PROCESSO = (
    "bash", "sh", "dash", "zsh", "fish",
    "pgrep", "pkill", "grep", "ps", "timeout", "nohup", "env", "xargs",
)


# POR QUE A FONTE E O `/proc` E NAO O `ps` — e o SEGUNDO defeito desta rodada,
# e e da mesma familia do primeiro.
#
# A primeira versao daqui lia `ps -eo pid=,comm=,args=`, e o teste reprovou com
# o processo VIVO na frente dele. Medido: o `ps` TRUNCA a coluna `args` na
# largura do terminal, e sob pytest nao ha tty — ele cortou em 58 caracteres e
# a marca que eu procurava morava DEPOIS do corte:
#
#     "/usr/local/bin/python3 -c import time; _ = 'MARCA_DBG_SOB_"
#
# Logo "o padrao nao casou" nao significava "o processo nao existe": significava
# "a leitura foi cortada". E o 17/10 outra vez — instrumento que devolve vazio
# nao prova ausencia — dentro do conserto de um instrumento que devolvia CHEIO
# sem prova. O `ps -ww` resolveria o corte; o `/proc/<pid>/cmdline` nao TEM
# largura, e e a fonte de onde o proprio `ps` le.
def _tabela() -> list[tuple[int, str, str]]:
    """(pid, comm, args) de todo processo, lido do `/proc`.

    Levanta se nao achar processo nenhum: tabela vazia e ausencia de LEITURA,
    nao sistema sem processo — e devolver lista vazia aqui faria o chamador
    concluir "morreu", que e o erro de 19/10 numa camada abaixo.
    """
    linhas = []
    try:
        pids = [d for d in os.listdir("/proc") if d.isdigit()]
    except OSError as e:
        raise RuntimeError(
            f"AUSENCIA DE LEITURA: nao consegui listar o /proc ({e}). Isto "
            "nao e 'nada rodando' — e instrumento sem dado."
        )
    for d in pids:
        try:
            with open(f"/proc/{d}/comm", encoding="utf-8", errors="replace") as f:
                comm = f.read().strip()
            with open(f"/proc/{d}/cmdline", "rb") as f:
                # O cmdline e NUL-separado e NAO tem limite de largura. Era a
                # largura do `ps` que escondia a marca.
                args = f.read().replace(b"\x00", b" ").decode(
                    "utf-8", errors="replace").strip()
        except OSError:
            continue   # processo morreu entre o listdir e a leitura
        if not comm:
            continue
        linhas.append((int(d), comm, args))
    if not linhas:
        raise RuntimeError(
            "AUSENCIA DE LEITURA: o /proc nao devolveu processo nenhum. Isto "
            "nao e 'nada rodando' — e instrumento sem dado, e concluir "
            "'morreu' daqui e o erro de 19/10 as 16:2x."
        )
    return linhas


EU = os.path.basename(os.path.abspath(__file__))


def sou_eu(args: str) -> bool:
    """Este modulo, rodando em OUTRO processo — e ele NAO e o processo.

    MEDIDO em 23/10 as 00:0x, e e o defeito que este arquivo foi escrito
    para consertar, uma camada acima. O `candidatos` tirava de fora o PID
    da propria chamada e o do pai dela; uma SEGUNDA copia concorrente do
    modulo tem outro PID, o executavel dela e python e os argumentos dela
    contem o padrao procurado — logo ela passava todos os filtros e era
    contada como o PROCESSO.

    Medido no proprio relato: as 00:00, com a suite rodando, ele disse
    `VIVO: 2 processo(s)` — o pytest (pid 3548) e o observador do laco de
    espera (pid 4364), que era este modulo. O numero estava errado por um.
    E a falha e PERMISSIVA no sentido pior: dois observadores concorrentes
    veem um ao outro e os dois dizem VIVO para sempre, que e exatamente o
    laco infinito do `pgrep` de 20/10 as 01:4x.

    O `NAO_SAO_O_PROCESSO` nao podia pegar isto: ele casa o EXECUTAVEL
    (`comm`), e o `comm` de uma copia deste modulo e `python3`. O
    discriminador tem de ser o ARGUMENTO que nomeia este arquivo.
    """
    return EU in (args or "")


def candidatos(padrao: str, executavel: str = "python") -> list[dict]:
    """Processos cujo EXECUTAVEL casa e cujos argumentos contem `padrao`.

    O PID desta propria chamada e o do pai dela saem fora por construcao: e
    por aqui que o `pgrep` se via no espelho.
    """
    meus = {os.getpid(), os.getppid()}
    saida = []
    for pid, comm, args in _tabela():
        if pid in meus:
            continue
        if executavel not in comm:
            continue
        if any(comm.startswith(n) for n in NAO_SAO_O_PROCESSO):
            continue
        if sou_eu(args):
            continue
        if padrao not in args:
            continue
        saida.append({"pid": pid, "comm": comm, "args": args})
    return saida


def espelhos(padrao: str) -> list[dict]:
    """O que o `pgrep -f` devolveria e que NAO e o processo — os espelhos.

    Existe para o relato poder NOMEAR o engano em vez de so o evitar: foi
    vendo quatro PIDs de shell que eu descobri o defeito.
    """
    reais = {c["pid"] for c in candidatos(padrao)}
    saida = []
    for pid, comm, args in _tabela():
        if pid in reais or pid in {os.getpid(), os.getppid()}:
            continue
        if padrao in args:
            d = {"pid": pid, "comm": comm, "args": args[:120]}
            if sou_eu(args):
                d["comm"] = "%s (OUTRA copia deste modulo)" % comm
            saida.append(d)
    return saida


def vivo(padrao: str, executavel: str = "python") -> bool:
    return bool(candidatos(padrao, executavel))


def relato(padrao: str = "pytest tests") -> str:
    c = candidatos(padrao)
    e = espelhos(padrao)
    L = [f"PROCESSO VIVO? padrao {padrao!r}, executavel python"]
    if c:
        L.append(f"  VIVO: {len(c)} processo(s)")
        for x in c[:4]:
            L.append(f"   pid {x['pid']:7d}  {x['comm']}")
    else:
        L.append("  NAO — nenhum processo python com esse padrao nos argumentos")
    if e:
        L.append(f"  e o `pgrep -f` devolveria {len(e)} ESPELHO(S), que nao sao"
                 f" o processo:")
        for x in e[:4]:
            L.append(f"   pid {x['pid']:7d}  {x['comm']}  (shell/busca)")
        L.append("  foi assim que eu reportei VIVO tres vezes em 20/10 as"
                 " 01:4x com a suite ja encerrada.")
    return "\n".join(L)


if __name__ == "__main__":
    pad = sys.argv[1] if len(sys.argv) > 1 else "pytest tests"
    print(relato(pad))
    sys.exit(0 if vivo(pad) else 1)
