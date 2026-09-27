"""Vigia horário: roda as auditorias, compara com a linha de base, e só grita
quando MUDA. Custo de Claude por rodada: zero.

POR QUE ASSIM, E NÃO UM AGENTE NO CRON
--------------------------------------
Pedido do dono em 27/09/2026: uma rotina que rode a cada hora, 24h, sem prompt
novo, revisando, testando e implementando. A parte de revisar e testar é isto.
A parte de "agente no cron" o projeto já mediu e pausou — `economia-de-token`
(skill) registra: *"Até 23/09/2026 havia uma rotina de hora em hora que criava
uma sessão nova do Claude a cada disparo — 24 por dia — para ver se algo mudou.
Nas duas últimas noites ela produziu principalmente auditoria de documentação
sobre si mesma, enquanto 42 leads envelheciam intocados."* Pausar isso foi a
maior economia do projeto.

A regra que sobrou, e que este arquivo implementa: **Action empurra, Claude
puxa.** O código de saída é a campainha.

    exit 0   nada mudou desde a linha de base  -> ninguém é acordado
    exit 1   mudou                             -> aí vale uma sessão
    exit 2   a própria varredura falhou        -> vale uma sessão, é defeito meu

E a segunda regra, que é o que faz a campainha ser confiável: **um alarme que
dispara toda hora é um alarme ignorado.** Achado real que espera decisão do dono
(o G-04, por exemplo) mora na linha de base com o `porque` dizendo que não está
resolvido, e continua impresso no resumo — mas não deixa a rodada vermelha.
Vermelho significa *apareceu algo que ninguém viu ainda*.

O QUE ELE NÃO FAZ, E NÃO PODE FAZER
-----------------------------------
- **Não edita workflow.** Isso exige a API interna com bearer de sessão logada;
  não sai de Action nem de contêiner. Nenhuma rotina desatendida implementa
  workflow, e prometer isso seria mentira.
- **Não escreve no CRM.** O `APROVADO.md` é o freio de mão e proíbe por escrito
  a rotina se autorizar ("um `[x]` que a própria rotina escreveu não é
  autorização"). Escrita continua saindo por acionamento manual com a caixa
  marcada por uma pessoa.

Então o escopo honesto de uma rotina 24h desatendida é: **revisar, testar,
medir e avisar.** Implementar continua sendo decisão com gente no circuito.

A LINHA DE BASE
---------------
`wesales/vigia-base.json`, versionada no repositório de propósito: o marcador
em `.local/` não sobrevive ao checkout efêmero do Action (defeito já documentado
no `promote_g03_scheduled.py`). Atualizar a base é ato deliberado de gente — a
rotina nunca a reescreve sozinha, senão ela silencia os próprios achados.

USO
---
    python3 wesales/tools/vigia.py            # varre e compara
    python3 wesales/tools/vigia.py --gravar   # regrava a base (ato humano)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "vigia-base.json"
TOOLS = ROOT / "tools"

# Cada varredura: (nome, comando, precisa_de_rede).
# Tudo aqui é leitura. Nenhum comando desta lista escreve em lugar nenhum.
VARREDURAS = [
    ("valores", [sys.executable, str(TOOLS / "auditoria_valores.py"), "--json"], True),
    ("prioridade", [sys.executable, str(TOOLS / "recalcula_prioridade.py"), "--dump"], True),
]


def roda(comando):
    """Devolve (codigo, saida). Nunca levanta: a varredura não pode derrubar o vigia."""
    try:
        p = subprocess.run(comando, capture_output=True, text=True, timeout=600)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, "comando não encontrado: %s" % comando[1]
    except subprocess.TimeoutExpired:
        return 124, "estourou o tempo (600s)"


def impressoes(nome, codigo, saida):
    """Reduz a saída de uma varredura a um conjunto de linhas comparáveis.

    Para a auditoria de valor, que sai em JSON, usa (tipo, campo, detalhe) — de
    propósito **sem o nome do contato**: lead novo com o mesmo defeito não é
    achado novo, é o mesmo defeito. Sem isso a base viraria vermelha todo dia
    que a campanha trouxesse lead, e um alarme diário é um alarme ignorado.
    """
    if nome == "valores":
        try:
            dados = json.loads(saida[saida.index("["):saida.rindex("]") + 1])
        except (ValueError, json.JSONDecodeError):
            return {"valores: saída ilegível (exit %d)" % codigo}
        return {"valores: [%s] %s — %s" % (a.get("tipo"), a.get("campo"), a.get("detalhe"))
                for a in dados}
    # As outras varreduras entram pelas linhas que interessam.
    marcas = ("[9.2-", "prioridade ", "a mudar:", "parou", "CONECTAR:")
    return {"%s: %s" % (nome, linha.strip()) for linha in saida.splitlines()
            if any(m in linha for m in marcas)}


def carrega_base():
    if not BASE.exists():
        return {"conhecidos": {}, "porque": {}}
    try:
        return json.loads(BASE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"conhecidos": {}, "porque": {}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gravar", action="store_true",
                       help="regrava a linha de base com o que a varredura achou agora")
    args = parser.parse_args()

    base = carrega_base()
    conhecidos = set(base.get("conhecidos") or [])
    porque = base.get("porque") or {}

    agora, falhas = set(), []
    for nome, comando, _rede in VARREDURAS:
        codigo, saida = roda(comando)
        # exit 1 da auditoria de valor significa "tem achado", não falha.
        if codigo not in (0, 1):
            falhas.append("%s: exit %d — %s" % (nome, codigo, saida.strip()[:300]))
            continue
        agora |= impressoes(nome, codigo, saida)

    novos = sorted(agora - conhecidos)
    sumiram = sorted(conhecidos - agora)
    print("varreduras: %d · achados agora: %d · na base: %d"
          % (len(VARREDURAS), len(agora), len(conhecidos)))

    if porque:
        print("\nconhecidos que esperam decisão (não deixam vermelho):")
        for chave, motivo in sorted(porque.items()):
            print("  %s\n      %s" % (chave, motivo))

    if args.gravar:
        BASE.write_text(json.dumps(
            {"conhecidos": sorted(agora), "porque": porque},
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("\nbase regravada com %d achados" % len(agora))
        return 0

    if falhas:
        print("\nVARREDURA FALHOU — isto é defeito da ferramenta, não da conta:")
        for f in falhas:
            print("  " + f)
        return 2

    if novos:
        print("\nNOVO (%d) — nada disso estava na base:" % len(novos))
        for n in novos:
            print("  + " + n)
    if sumiram:
        print("\nSUMIU (%d) — conferir se foi consertado ou se a leitura quebrou:" % len(sumiram))
        for s in sumiram:
            print("  - " + s)

    if not novos and not sumiram:
        print("\nsem mudança desde a linha de base")
        return 0
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as erro:
        print("vigia parou: " + str(erro))
        raise SystemExit(2)
