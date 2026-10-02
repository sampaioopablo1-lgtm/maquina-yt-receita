"""Regras puras da máquina de cold mail: nada aqui fala com rede, por isso é o que os testes cobrem.

  - aquecimento: cada conta começa mandando pouco e sobe um degrau por dia até o teto dela;
  - janela: só envia em dia útil, no horário comercial de São Paulo;
  - rotação: follow-up sai SEMPRE da conta que abriu a conversa (mesma thread no Gmail do lead);
    lead novo vai para a conta com mais folga hoje, e a fila final intercala as contas
    (A, B, C, A, B, C...) para nenhuma caixa disparar várias seguidas;
  - texto: spintax {Oi|Olá} e variáveis {primeiro_nome}, {empresa}...
"""
from __future__ import annotations

import datetime as dt
import random
import re
from collections import defaultdict
from dataclasses import dataclass, field

BR = dt.timezone(dt.timedelta(hours=-3))


@dataclass
class Conta:
    email: str
    senha: str
    nome: str = ""
    limite_dia: int = 30
    inicio: dt.date = field(default_factory=lambda: dt.datetime.now(BR).date())
    assinatura: str = ""

    @classmethod
    def de_dict(cls, d: dict) -> "Conta":
        inicio = d.get("inicio")
        return cls(
            email=d["email"].strip().lower(),
            senha=(d.get("senha_app") or d.get("senha") or "").replace(" ", ""),
            nome=d.get("nome") or "",
            limite_dia=int(d.get("limite_dia") or 30),
            inicio=dt.date.fromisoformat(inicio) if inicio else dt.datetime.now(BR).date(),
            assinatura=d.get("assinatura") or "",
        )


def limite_hoje(conta: Conta, hoje: dt.date, rampa_inicial: int = 5, rampa_passo: int = 3) -> int:
    """Teto de envios da conta hoje. Dia 0: 5, depois +3 por dia até o `limite_dia` da conta."""
    dias = (hoje - conta.inicio).days
    if dias < 0:
        return 0
    return max(0, min(conta.limite_dia, rampa_inicial + rampa_passo * dias))


def na_janela(agora: dt.datetime, inicio_h: int = 8, fim_h: int = 18) -> bool:
    """Seg a sex, das `inicio_h` às `fim_h` (horário de São Paulo)."""
    local = agora.astimezone(BR)
    return local.isoweekday() <= 5 and inicio_h <= local.hour < fim_h


def capacidade(contas: list[Conta], enviados_hoje: dict[str, int], hoje: dt.date,
               por_rodada: int, **rampa) -> dict[str, int]:
    """Quantos envios cada conta ainda pode fazer NESTA rodada (folga do dia, limitada a `por_rodada`)."""
    cap = {}
    for c in contas:
        folga = limite_hoje(c, hoje, **rampa) - enviados_hoje.get(c.email, 0)
        cap[c.email] = max(0, min(folga, por_rodada))
    return cap


def planejar(devidos: list[dict], contas: list[Conta], cap: dict[str, int]) -> list[tuple[dict, str]]:
    """Distribui os leads devidos entre as contas e devolve a fila intercalada [(lead, conta)].

    Follow-up (passo > 0) vem primeiro e fica preso à conta que já conversa com o lead; se essa
    conta não tem folga (ou saiu da configuração), o lead espera a próxima rodada — trocar de conta
    no meio da sequência quebraria a thread. Lead novo vai para a conta com mais folga restante.
    """
    cap = dict(cap)
    ordem = [c.email for c in contas]
    por_conta: dict[str, list[dict]] = defaultdict(list)

    for lead in devidos:
        if int(lead.get("passo") or 0) > 0:
            c = lead.get("conta")
            if c in cap and cap[c] > 0:
                por_conta[c].append(lead)
                cap[c] -= 1

    for lead in devidos:
        if int(lead.get("passo") or 0) == 0:
            livres = [c for c in ordem if cap.get(c, 0) > 0]
            if not livres:
                break
            c = max(livres, key=lambda e: (cap[e], -ordem.index(e)))
            por_conta[c].append(lead)
            cap[c] -= 1

    fila: list[tuple[dict, str]] = []
    while any(por_conta.values()):
        for c in ordem:
            if por_conta.get(c):
                fila.append((por_conta[c].pop(0), c))
    return fila


SPIN = re.compile(r"\{([^{}]*\|[^{}]*)\}")
VAR = re.compile(r"\{(\w+)(?::([^{}|]*))?\}")      # {empresa} ou {empresa:sua empresa} (padrão se vazio)


def spintax(texto: str, rng: random.Random) -> str:
    """{Oi|Olá|E aí} vira uma das opções. Aninhado também funciona (resolve de dentro para fora)."""
    while True:
        novo = SPIN.sub(lambda m: rng.choice(m.group(1).split("|")), texto)
        if novo == texto:
            return novo
        texto = novo


def renderizar(modelo: str, variaveis: dict, rng: random.Random) -> str:
    """Variáveis primeiro (assim "{{primeiro_nome}, pergunta|...}" funciona), depois spintax.
    Variável vazia some sem deixar "Oi ," nem linha em branco dupla; {empresa:sua empresa} usa o padrão."""
    def valor(m):
        if m.group(1) not in variaveis and m.group(2) is None:
            return m.group(0)
        v = str(variaveis.get(m.group(1)) or "").strip() or (m.group(2) or "")
        return re.sub(r"[{}|]", " ", v)
    texto = VAR.sub("", spintax(VAR.sub(valor, modelo), rng))   # variável que o lead não tem: some
    texto = re.sub(r"[ \t]+([,.!?])", r"\1", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def variaveis(lead: dict, conta: Conta, extra: dict | None = None) -> dict:
    v = dict(extra or {})
    v.update({
        "primeiro_nome": (lead.get("primeiro_nome") or "").strip().title(),
        "empresa": lead.get("empresa") or "",
        "cargo": lead.get("cargo") or "",
        "site": lead.get("site") or "",
        "abertura": lead.get("abertura") or "",
        "remetente": conta.nome.split(" ")[0] if conta.nome else "",
        "assinatura": conta.assinatura or conta.nome,
    })
    return v


def proximo_envio(agora: dt.datetime, espera_dias: int, rng: random.Random) -> dt.datetime:
    """Data do próximo passo: `espera_dias` depois, com 0-120 min de folga para não cair sempre na mesma hora."""
    return agora + dt.timedelta(days=espera_dias, minutes=rng.randint(0, 120))


def assunto_resposta(assunto: str) -> str:
    return assunto if re.match(r"^\s*(re|res)\s*:", assunto or "", re.I) else "Re: %s" % (assunto or "").strip()


def espacamento(n_envios: int, janela_s: int = 1500, minimo: int = 20, maximo: int = 120) -> float:
    """Segundos entre um envio e o próximo para a rodada caber em ~25 min."""
    if n_envios <= 1:
        return 0.0
    return float(max(minimo, min(maximo, janela_s / n_envios)))
