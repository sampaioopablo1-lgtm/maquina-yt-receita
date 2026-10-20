"""O PARQUE das leituras de inscritos — e a pergunta "vale a pena ler AGORA?".

POR QUE EXISTE, e o defeito e desta rodada. As 10:0x de 19/10 eu li os tres
canais porque a leitura anterior tinha **4 h** — a regra H (686) — e o quadro
saiu com os tres em `indeterminado`, como tinha de sair: numa janela de 4 h o
piso de resolucao e **6,00 inscritos/dia**, e o ritmo da frota que eu media era
~1,8. **A leitura era previsivelmente inutil, e eu gastei tres requisicoes nela
na mesma madrugada em que a rota fechou por LIMITE.**

E o `porta1.py` ja sabia disso: o docstring do `piso_de_resolucao` diz em letra
que *"as >= 4 h da regra H bastam para pular o DEGRAU da replica, e eu tratei
isso como se bastasse para medir RITMO"*. **O numero estava no modulo e a
DECISAO continuava na minha cabeca** — item 3 da §10, que e o que esta rodada
tira daqui.

**E as leituras nao moravam em lugar nenhum.** Elas estavam no relato de cada
rodada e na minha memoria, logo "quando foi a ultima?" era pergunta para mim.
E a assinatura do 726: o passo que nao tem instrumento e o passo que eu solto.
Agora elas entram num arquivo, como as duracoes entram no parque do
`duracao_a_medir`.

**AS DUAS PORTAS SAO DIFERENTES, e confundi-las foi o erro de dias:**

    regra H (686)        >= 4 h   — pula o DEGRAU da replica do contador
    resolucao            24/ritmo — e o que permite FALAR de ritmo
    criterio do 723      o dobro  — porque ele exige |delta| >= 2, nao >= 1

Passar a primeira **nao** autoriza a segunda, e este modulo recusa dizer que
autoriza. O que ele faz e nomear qual pergunta a janela responde.

**E A JANELA NAO E A UNICA PORTA — medido em 20/10 as 13:2x, na PRIMEIRA rodada
em que o criterio do 723 passou por TEMPO.** Em vinte e duas rodadas seguidas
este modulo recusou a leitura, e nas vinte e duas a recusa saiu do ramo
`degrau and not resolve_duas_contagens`. **A nota sobre a ROTA morava DENTRO
desse ramo** — logo, no instante em que o tempo finalmente autorizou (27,05 h,
piso 0,89/dia), o relato imprimiu tres SIM e **calou sobre a unica coisa que
ainda impedia a leitura.** Falha PERMISSIVA, e no sentido pior: ela convida a
gastar requisicao.

E a nota era **PROSA CRAVADA** — *"a rota que fechou por LIMITE em 19/10 as
06:1x"* —, isto e, um modo MEDIDO naquele dia reescrito a mao numa string,
quando o modo medido nesta rodada e `negado_por_politica` e o remedio dele e
OUTRO: a tela de Network access, que e do dono, em vez de esperar volume. E o
753 em forma de PROCEDENCIA.

**Consertado com DELEGACAO:** o modo da rota entra por fora, MEDIDO pelo dono
da pergunta (`vivacidade_publica.modo_de_fechamento`), e o relato o nomeia nos
DOIS ramos. **Sem o modo ele DIZ que a rota nao foi sondada**, do jeito que o
`porta1` recusa janela curta — porque ausencia de sonda nao e rota aberta.
"""

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, "docs", "pendente", "inscritos-lidos.jsonl")

# O ritmo que a frota media em 12/10 e que serve de alvo de resolucao. Ele e
# PREMISSA e nao medida de hoje: o 755 mostrou que ele proprio era UMA contagem.
# Fica aqui com esse nome para quem chamar saber que esta passando uma suposicao.
RITMO_SUPOSTO_DA_FROTA = 1.79

# O que cada modo MEDIDO da rota significa para ESTA decisao. As chaves NAO sao
# lista minha: elas sao conferidas contra `vivacidade_publica.modos()`, que as
# DERIVA do `modo_de_fechamento`. Nomear modo aqui seria o segundo dono deles —
# a assinatura que congelou a legenda —, e o que importa e que **o remedio de
# cada modo e diferente**: um pede economia de requisicao, outro nao responde a
# volume nenhum, e `negado_por_politica` nao se conserta deste lado.
CONSEQUENCIA_DO_MODO = {
    "aberta": "a rota RESPONDEU na sonda, logo ler agora entrega leitura.",
    "limite": "recusa por VOLUME: leia inscritos e duracao na MESMA passagem e "
              "gaste menos requisicao por rodada.",
    "consentimento": "parede do CONSENT: ela NAO responde a volume — cookie, "
                     "User-Agent e `&hl=en` foram testados em 16/10 e nao "
                     "resolvem. Nao ha o que economizar.",
    "sem_egresso": "a sonda nao tem rede: nao ha leitura e nao se conserta "
                   "deste lado.",
    "negado_por_politica": "o proxy negou o CONNECT: o remedio e do DONO, na "
                           "tela de Network access, e NAO e esperar.",
    "indeterminado": "a sonda nao decidiu: faltou controle. Nao prometa leitura "
                     "sobre ela.",
}


def _linhas(caminho=None):
    caminho = caminho or ARQ
    if not os.path.exists(caminho):
        return []
    saida = []
    for linha in open(caminho, encoding="utf-8"):
        linha = linha.strip()
        if linha:
            saida.append(json.loads(linha))
    return saida


def leituras(caminho=None) -> list:
    """Todas as leituras, da mais ANTIGA para a mais nova."""
    return sorted(_linhas(caminho), key=lambda r: r["em"])


def grava(em: str, canais: dict, fonte: str, caminho=None) -> bool:
    """Acrescenta uma leitura. Devolve False quando ela ja estava igual.

    **Reescrever o MESMO instante com valor DIFERENTE levanta**, pela mesma
    razao do `duracao_a_medir`: contagem de um instante nao muda, e duas
    leituras discordantes do mesmo `em` sao defeito de quem gravou, nao dado.
    """
    caminho = caminho or ARQ
    if not canais:
        raise ValueError("leitura sem canal nenhum nao e leitura")
    for ja in _linhas(caminho):
        if ja["em"] == em:
            if ja["canais"] == canais:
                return False
            raise ValueError(
                f"o instante {em} ja esta gravado com {ja['canais']} e agora "
                f"veio {canais}. Contagem de um instante nao muda — confira a "
                "ROTA antes de regravar (17/10, peca de controle)."
            )
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps({"em": em, "canais": canais, "fonte": fonte},
                           ensure_ascii=False, sort_keys=True) + "\n")
    return True


def _horas(a: str, b: str) -> float:
    import datetime as _dt

    ta = _dt.datetime.fromisoformat(a.replace("Z", "+00:00"))
    tb = _dt.datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (tb - ta).total_seconds() / 3600.0


def janela_desde_a_ultima(agora: str, caminho=None) -> float | None:
    """Horas entre a ultima leitura gravada e `agora`. None se nao houver nenhuma."""
    todas = leituras(caminho)
    if not todas:
        return None
    return _horas(todas[-1]["em"], agora)


def _rota(modo_da_rota: str = None) -> dict:
    """O modo MEDIDO da rota, conferido contra o DONO dos modos.

    Modo que o `vivacidade_publica.modos()` nao conhece **LEVANTA** em vez de
    passar: foi inventar nome de modo que o teste de 19/10 as 23:4x passou a
    proibir por AST, e aceitar um aqui reintroduziria isso como dado.
    """
    import vivacidade_publica

    if modo_da_rota is None:
        return {"modo_da_rota": None, "rota_sondada": False}
    conhecidos = vivacidade_publica.modos()
    if modo_da_rota not in conhecidos:
        raise ValueError(
            "modo de rota %r nao e um dos que o `modo_de_fechamento` devolve "
            "(%s). Modo inventado como dado e pior que modo ausente."
            % (modo_da_rota, ", ".join(sorted(conhecidos))))
    return {"modo_da_rota": modo_da_rota, "rota_sondada": True}


def _linha_da_rota(v: dict) -> str:
    """A frase da rota, com UM dono — ela sai nos DOIS ramos do relato.

    Ter dois donos dela era o defeito: a nota vivia dentro do ramo da recusa,
    e por isso calou na rodada em que o tempo autorizou a leitura.
    """
    if not v.get("rota_sondada"):
        return ("  ROTA: **NAO SONDADA nesta chamada.** Sonde com os TRES "
                "controles (host NEUTRO, escrita e `__agentproxy/status`) antes "
                "de prometer leitura — ausencia de sonda nao e rota aberta.")
    modo = v["modo_da_rota"]
    return "  ROTA (modo MEDIDO): %s — %s" % (
        modo, CONSEQUENCIA_DO_MODO.get(
            modo, "modo sem consequencia escrita: escreva-a antes de decidir."))


def veredito(agora: str, ritmo: float = None, caminho=None,
             modo_da_rota: str = None) -> dict:
    """O que uma leitura feita AGORA consegue responder.

    Devolve as tres portas separadas, porque juntar as duas primeiras foi o
    defeito. `ritmo` e o ritmo que se quer resolver; sem ele usa a premissa
    declarada em `RITMO_SUPOSTO_DA_FROTA`.
    """
    import porta1

    ritmo = RITMO_SUPOSTO_DA_FROTA if ritmo is None else ritmo
    rota = _rota(modo_da_rota)
    h = janela_desde_a_ultima(agora, caminho)
    if h is None:
        saida = {"horas": None, "degrau": False, "resolve_ritmo": False,
                 "resolve_duas_contagens": False,
                 "motivo": "nenhuma leitura gravada: a primeira serve de ANCORA "
                           "e nao responde nada sozinha."}
        saida.update(rota)
        return saida
    piso = porta1.piso_de_resolucao(h) if h > 0 else float("inf")
    precisa_uma = porta1.horas_para_resolver(ritmo)
    precisa_duas = porta1.horas_para_resolver(ritmo, 2)
    saida = {
        "horas": round(h, 2),
        "piso_da_janela": round(piso, 2),
        "degrau": h >= porta1.HORAS_MINIMAS,
        "resolve_ritmo": h >= precisa_uma,
        "resolve_duas_contagens": h >= precisa_duas,
        "horas_para_uma": round(precisa_uma, 1),
        "horas_para_duas": round(precisa_duas, 1),
        "faltam_para_duas": round(max(0.0, precisa_duas - h), 1),
    }
    saida.update(rota)
    return saida


def relato(agora: str, ritmo: float = None, caminho=None,
           modo_da_rota: str = None) -> str:
    v = veredito(agora, ritmo, caminho, modo_da_rota)
    if v["horas"] is None:
        return "LEITURA: " + v["motivo"] + "\n" + _linha_da_rota(v)
    r = RITMO_SUPOSTO_DA_FROTA if ritmo is None else ritmo
    linhas = [
        f"LEITURA DE INSCRITOS: {v['horas']} h desde a ultima, piso de "
        f"resolucao {v['piso_da_janela']}/dia.",
        f"  degrau da replica (regra H, >= 4 h): "
        f"{'SIM' if v['degrau'] else 'NAO'}",
        f"  resolve ritmo de {r}/dia (precisa {v['horas_para_uma']} h): "
        f"{'SIM' if v['resolve_ritmo'] else 'NAO'}",
        f"  resolve pelo criterio do 723, |delta| >= 2 (precisa "
        f"{v['horas_para_duas']} h): "
        f"{'SIM' if v['resolve_duas_contagens'] else 'NAO'}",
    ]
    if v["degrau"] and not v["resolve_duas_contagens"]:
        linhas.append(
            f"  >> passar a regra H NAO e resolver ritmo: faltam "
            f"{v['faltam_para_duas']} h para o criterio do 723. Ler agora "
            "devolve `indeterminado` com mais horas, e gasta requisicao."
        )
    # A linha da ROTA sai nos DOIS ramos, e e por isso que ela tem um dono so:
    # ela morava DENTRO do ramo acima e calou na rodada em que o tempo passou.
    linhas.append(_linha_da_rota(v))
    if v["resolve_duas_contagens"] and v.get("modo_da_rota") not in (None, "aberta"):
        linhas.append(
            "  >> a JANELA autoriza e a ROTA nao: as duas portas sao "
            "independentes, e passar uma nao e passar a outra."
        )
    return "\n".join(linhas)


if __name__ == "__main__":
    import datetime
    import sys

    agora = sys.argv[1] if len(sys.argv) > 1 else \
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(relato(agora))
