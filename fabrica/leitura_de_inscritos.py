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
"""

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, "docs", "pendente", "inscritos-lidos.jsonl")

# O ritmo que a frota media em 12/10 e que serve de alvo de resolucao. Ele e
# PREMISSA e nao medida de hoje: o 755 mostrou que ele proprio era UMA contagem.
# Fica aqui com esse nome para quem chamar saber que esta passando uma suposicao.
RITMO_SUPOSTO_DA_FROTA = 1.79


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


def veredito(agora: str, ritmo: float = None, caminho=None) -> dict:
    """O que uma leitura feita AGORA consegue responder.

    Devolve as tres portas separadas, porque juntar as duas primeiras foi o
    defeito. `ritmo` e o ritmo que se quer resolver; sem ele usa a premissa
    declarada em `RITMO_SUPOSTO_DA_FROTA`.
    """
    import porta1

    ritmo = RITMO_SUPOSTO_DA_FROTA if ritmo is None else ritmo
    h = janela_desde_a_ultima(agora, caminho)
    if h is None:
        return {"horas": None, "degrau": False, "resolve_ritmo": False,
                "resolve_duas_contagens": False,
                "motivo": "nenhuma leitura gravada: a primeira serve de ANCORA "
                          "e nao responde nada sozinha."}
    piso = porta1.piso_de_resolucao(h) if h > 0 else float("inf")
    precisa_uma = porta1.horas_para_resolver(ritmo)
    precisa_duas = porta1.horas_para_resolver(ritmo, 2)
    return {
        "horas": round(h, 2),
        "piso_da_janela": round(piso, 2),
        "degrau": h >= porta1.HORAS_MINIMAS,
        "resolve_ritmo": h >= precisa_uma,
        "resolve_duas_contagens": h >= precisa_duas,
        "horas_para_uma": round(precisa_uma, 1),
        "horas_para_duas": round(precisa_duas, 1),
        "faltam_para_duas": round(max(0.0, precisa_duas - h), 1),
    }


def relato(agora: str, ritmo: float = None, caminho=None) -> str:
    v = veredito(agora, ritmo, caminho)
    if v["horas"] is None:
        return "LEITURA: " + v["motivo"]
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
            "devolve `indeterminado` com mais horas, e gasta requisicao na rota "
            "que fechou por LIMITE em 19/10 as 06:1x."
        )
    return "\n".join(linhas)


if __name__ == "__main__":
    import datetime
    import sys

    agora = sys.argv[1] if len(sys.argv) > 1 else \
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(relato(agora))
