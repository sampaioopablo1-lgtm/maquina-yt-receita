#!/usr/bin/env python3
"""Ha quanto tempo cada canal nao publica LONGO — a pergunta do DONO.

**Palavras dele em 16/10:** *"pelo menos 2 videos por dia por canal, 1 video
longo e outro curto"*. Essa frase tem DUAS metades e so uma tinha dono: o
`concentracao_frota.escolha_do_momento` conta PEÇA na janela de 24 h e **nao
distingue longo de short**, logo ele responde "qual canal produziu menos" e
nunca "qual canal esta sem LONGO".

**MEDIDO em 23/10 as 18:4x, e e por isso que este modulo existe:** naquela
rodada eu escolhi o canal do pacote pelo VAO sem longo, e a classificacao saiu
de um laco Python escrito na linha de comando — o item 3 da §10, que diz que
todo numero que eu calculo a mao vira um erro meu. A causa era uma camada
abaixo: **o parque de duracao nao carregava o formato.** O `do_registro`
copiava `pacote`, `canal`, `youtube_id`, `em` e `cenas`, e **jogava fora o
`formato` e o `slug`**, que sao os dois unicos campos do registro do dono que
distinguem o LONGO do SHORT de um pacote.

E O PACOTE NAO SERVE DE CHAVE, medido no proprio arquivo: os tres pacotes de
19/10 estao como `<pacote>-longo` (eu montei o dicionario a mao, antes de o
`do_registro` existir) e os de 22/10 em diante tem o **MESMO** `pacote` duas
vezes, distinguidos so pela previsao. Nove linhas ficaram indeterminadas, e
foram reparadas com o formato LIDO do dono — o
`docs/pendente/videos-a-inserir.sql`, que o `registro_videos.sql_insert`
escreve com a coluna `formato` em letra.

**E A MEDICAO QUE EU IA RELATAR ERA FALSA, e fica registrada porque era minha:**
procurando a origem do defeito eu contei o SQL pendente com
`grep -c 'insert into videos'` e com um regex que lia a PRIMEIRA tupla de cada
linha, e os dois disseram *"205 shorts, ZERO longos"* — eu ia relatar ao dono que
o registro de `videos` perde a linha do LONGO. **Falso:** o `sql_insert` escreve
UM `insert` com uma tupla por peça, logo a contagem por LINHA e por primeira
tupla erra pelo mesmo motivo, e os dois instrumentos meus se confirmavam um ao
outro. Contadas as TUPLAS: **211, com 205 `shorts` e 6 `longo`** — os seis
pacotes publicados, nenhum perdido. E a assinatura de 23/10 as 13:5x, quando o
meu detector de divergencia de titulo acusou a maquina de um defeito que ela nao
cometeu: **antes de chamar um achado de achado, pergunte se o instrumento pode
produzi-lo.**

ELE NOMEIA E NAO DECIDE. A escolha do canal e do `passo_zero`, pelo
`concentracao_frota`; isto poe o vao do longo ao lado para que a segunda metade
do pedido do dono deixe de depender da minha memoria. Nao e portao e o codigo de
saida e sempre zero.
"""
from __future__ import annotations

import datetime
import sys

import canal as CA
import duracao_a_medir as DM

FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def _instante(s: str):
    if not s:
        return None
    try:
        return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


def pecas(caminho: str = None) -> list[dict]:
    """As linhas do parque com `canal` e `formato` DERIVADOS pelos donos.

    O canal sai de `canal.do_pacote` e NAO do campo `canal` da linha: 57 das
    169 linhas nao o tem, logo ler o campo perderia essas peças em silencio
    (a mesma razao do `familia_entre_canais`). O formato sai de
    `duracao_a_medir.formato`, que RECUSA em vez de palpitar.
    """
    out = []
    for r in DM.carrega(caminho):
        pac = r.get("pacote") or ""
        try:
            cn = CA.do_pacote(pac)
        except Exception:
            cn = None
        out.append({
            "pacote": pac,
            "youtube_id": r.get("youtube_id"),
            "em": r.get("em"),
            "canal": cn,
            "formato": DM.formato(r),
        })
    return out


def sem_formato(caminho: str = None) -> list[dict]:
    """As peças cujo formato o parque NAO sabe. Vao NOMEADAS, nunca contadas
    como short: supor o formato aqui e o 733 em forma de contagem."""
    return [p for p in pecas(caminho) if p["formato"] is None]


def quadro(agora: str = None, caminho: str = None) -> dict:
    """Por canal: o ULTIMO longo, o vao em horas, e o ultimo short.

    `vao_h` e `None` quando o canal **nunca** publicou longo no parque — e isso
    e diferente de "nao sei", que e o `sem_formato`. O canal de MAIOR vao sai
    em `mais_antigo`, e canal sem longo nenhum vence qualquer vao finito,
    porque zero longos e o caso extremo e nao a ausencia de dado.
    """
    ag = _instante(agora) or datetime.datetime.utcnow()
    todas = pecas(caminho)
    por_canal = {}
    for cn in FROTA:
        suas = [p for p in todas if p["canal"] == cn]
        longos = [p for p in suas if p["formato"] == "longo" and _instante(p["em"])]
        shorts = [p for p in suas if p["formato"] == "shorts" and _instante(p["em"])]
        ul = max(longos, key=lambda p: p["em"]) if longos else None
        us = max(shorts, key=lambda p: p["em"]) if shorts else None
        vao = None
        if ul:
            vao = round((ag - _instante(ul["em"])).total_seconds() / 3600.0, 2)
        por_canal[cn] = {
            "n_longos": len(longos),
            "n_shorts": len(shorts),
            "ultimo_longo": ul,
            "ultimo_short": us,
            "vao_h": vao,
        }
    nunca = [c for c in FROTA if por_canal[c]["n_longos"] == 0]
    if nunca:
        mais_antigo = sorted(nunca)[0]
    else:
        mais_antigo = max(FROTA, key=lambda c: por_canal[c]["vao_h"])
    return {
        "agora": ag.strftime("%Y-%m-%dT%H:%M:%S"),
        "canais": por_canal,
        "mais_antigo": mais_antigo,
        "nunca": nunca,
        "sem_formato": sem_formato(caminho),
    }


def na_janela(janela_h: float = 24.0, agora: str = None,
              caminho: str = None) -> dict:
    """Longos e shorts de cada canal DENTRO da janela, com limite de CIMA.

    O limite de cima e deliberado: sem ele, parque com instante no futuro conta
    (o defeito medido em 20/10 as 13:2x no irmao `concentracao_frota`).
    """
    ag = _instante(agora) or datetime.datetime.utcnow()
    desde = ag - datetime.timedelta(hours=janela_h)
    out = {}
    for cn in FROTA:
        out[cn] = {"longo": 0, "shorts": 0}
    for p in pecas(caminho):
        i = _instante(p["em"])
        if not i or i < desde or i > ag or p["canal"] not in out:
            continue
        if p["formato"] in ("longo", "shorts"):
            out[p["canal"]][p["formato"]] += 1
    return out


def _linha_do_vao(q: dict, cn: str) -> str:
    """UM dono da frase, nos TRES ramos (nunca publicou / vao / mais antigo)."""
    d = q["canais"][cn]
    if d["n_longos"] == 0:
        return ("  %-16s NUNCA publicou longo no parque — e isto nao e "
                "'nao sei': o que o parque nao sabe sai em `sem_formato`." % cn)
    ul = d["ultimo_longo"]
    marca = "  << MAIOR VAO" if cn == q["mais_antigo"] else ""
    return ("  %-16s ultimo longo %s (%s), vao de **%.1f h** | %d longo(s), "
            "%d short(s) no parque%s"
            % (cn, ul["em"], ul["youtube_id"], d["vao_h"],
               d["n_longos"], d["n_shorts"], marca))


def relato(agora: str = None, caminho: str = None, janela_h: float = 24.0) -> str:
    q = quadro(agora, caminho)
    j = na_janela(janela_h, agora, caminho)
    ls = ["LONGO POR CANAL (do parque de duracao, com o formato LIDO do dono):"]
    for cn in FROTA:
        ls.append(_linha_do_vao(q, cn))
    ls.append("  na janela de %.0f h: %s"
              % (janela_h, " | ".join("%s %dL/%dS" % (c, j[c]["longo"],
                                                      j[c]["shorts"])
                                      for c in FROTA)))
    sf = q["sem_formato"]
    if sf:
        ls.append("  SEM FORMATO (%d peca(s)), NOMEADAS e nao contadas como "
                  "short: %s" % (len(sf), ", ".join(
                      "%s/%s" % (p["pacote"], p["youtube_id"]) for p in sf[:6])))
    else:
        ls.append("  SEM FORMATO: nenhuma — as 169 linhas do parque sabem o "
                  "proprio formato, e as nove indeterminadas foram reparadas "
                  "com o valor LIDO do dono em 23/10 as 21:3x.")
    ls.append("  o DONO pediu ao menos UM longo e UM curto por canal por dia "
              "(16/10). Isto NOMEIA e NAO decide: a escolha do canal e do "
              "`passo_zero`, pelo `concentracao_frota`, que conta PEÇA e nao "
              "distingue formato.")
    return "\n".join(ls)


def main(argv: list[str]) -> int:
    janela = float(argv[1]) if len(argv) > 1 else 24.0
    print(relato(janela_h=janela))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
