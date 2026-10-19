#!/usr/bin/env python3
"""A linha em `videos` e o SEGUNDO passo manual do registro, e eu o perdi ao
automatizar o PRIMEIRO.

POR QUE ISTO EXISTE, medido em 13/10/2026 as 14:1x. Eu fui gravar metrica das
doze pecas de hoje e levei

    insert or update on table "metricas" violates foreign key constraint
    "metricas_youtube_id_fkey" -- Key (youtube_id)=(CdUiplaeP5g) is not present
    in table "videos"

As doze pecas publicadas hoje nao tinham linha em `videos`. O paragrafo 9 da
rotina pede exatamente isso -- "registro: linha em `videos` COM `origem_id`" --
e eu nao fiz nenhuma vez em doze publicacoes.

**A CAUSA E A PARTE QUE VALE GUARDAR, e e sobre automatizar pela metade.** O
registro manual tinha DOIS passos: o titulo no `corpus_publicados.json` e a
linha em `videos`. Medido no banco, as linhas de `videos` existem ate o
`labtreinamento-s025` (12/10 as 23:12) e param ali. As 00:2x de hoje eu escrevi
o `corpus_atrasado.py`, passei a fazer o passo do corpus com instrumento -- e
**soltei o passo que nao tinha instrumento**. Trocar memoria por ferramenta num
dos dois passos fez o outro desaparecer do habito.

**E a falha e RUIDOSA, nao permissiva** -- ao contrario da do corpus, que barrava
titulo duplicado e simplesmente parava de barrar. Esta levanta chave estrangeira.
So que ela levanta **apenas quando alguem tenta medir**, e eu nao tentei medir
por catorze horas. Barulho que ninguem ouve e silencio.

**E A MEDICAO DO TAMANHO QUASE SAIU INFLADA, pelo efeito (C) da rotina:** eu
montei a mao uma lista de pacotes "suspeitos" e ela trouxe
`kolejny-poziom-s020` e `-s021` como faltantes. **Esses pacotes NAO EXISTEM** --
nem spec, nem publicacao. O atraso real e exatamente as doze de hoje. Lista
escrita a mao mentindo, outra vez.

USO, depois de publicar:

    <notices do retomar.yml> | python3 fabrica/registro_videos.py

Ele imprime o INSERT pronto, para rodar por `execute_sql` -- a unica rota aberta
enquanto o REST esta em 402. Nao executa nada sozinho: SQL que escreve no banco
sai para revisao, nao sai disparado por um pipe.
"""
from __future__ import annotations

import json
import os
import re
import sys

import canal

SPECS = os.path.join(os.path.dirname(__file__), "specs")

# A mesma forma do notice que o `corpus_atrasado` le, e de proposito: uma fonte
# so para os dois passos do registro, senao eles divergem como divergiram.
_NOTICE = re.compile(
    r"PUBLICADO\s+(\S+)\s+(\S+)\s+youtube_id=(\S+)\s+titulo=(.*?)\s+em=(\S+)")


def _esc(s: str) -> str:
    return (s or "").replace("'", "''")


def titulo_short(spec: dict) -> str:
    """O `## TITULO SHORT` da copy -- o que o YouTube recebe.

    E a MESMA forma que o corpus guarda. Em 13/10 as 00:2x eu medi o corpus pelo
    `## TITULO` longo e errei por dezessete pecas; o titulo que vale e este.
    """
    copy = spec.get("copy") or ""
    if "## TITULO SHORT" not in copy:
        return ""
    return copy.split("## TITULO SHORT")[1].split("##")[0].strip()


def linhas_dos_notices(texto: str, raiz: str = None) -> list[dict]:
    """Uma linha de `videos` por notice, com os campos que o paragrafo 9 pede.

    `origem_id` vem do `longo_existente` da spec (670) -- e o campo cuja ausencia
    faz a `consultas/estoque.sql` nao saber que a origem foi consumida.
    """
    raiz = raiz or SPECS
    out = []
    for pacote, formato, yid, titulo, em in _NOTICE.findall(texto):
        if yid == "?":          # run abortado: o 718 ja mandou nao contar
            continue
        caminho = os.path.join(raiz, pacote + ".json")
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            spec = json.load(f)
        # O FORMATO decide o slug e a contagem de cenas, e a forma e a do
        # `publicar.py:524-534`, que e quem grava quando o banco esta aberto:
        #   longo  -> slug = pacote,            cenas = len(longo)
        #   shorts -> slug = pacote + "-short", cenas = len(short)
        #
        # MEDIDO EM 19/10 AS 13:0x, no PRIMEIRO pacote publicado desde que este
        # modulo nasceu (13/10). Ele cravava `-short` e `len(short)` para
        # QUALQUER notice, porque todas as peças de seis dias foram short solto.
        # Com o `execute_sql` aberto, as duas linhas do `epomeno-epipedo-068`
        # teriam o MESMO slug e o `on conflict (slug) do nothing` descartaria a
        # do LONGO em silencio — a falha permissiva outra vez, e no registro.
        e_longo = formato == "longo"
        out.append({
            "slug": pacote if e_longo else f"{pacote}-short",
            "status": "publicado",
            "formato": formato,
            "titulo": titulo if e_longo else (titulo_short(spec) or titulo),
            "youtube_id": yid,
            "canal": canal.da_spec({"pacote": pacote, **spec}),
            "pacote": pacote,
            # Longo NAO tem origem: ele E a origem. `None` aqui e o valor certo,
            # e o aviso do 670 vale so para short.
            "origem_id": None if e_longo else spec.get("longo_existente"),
            "cenas": len(spec.get("longo" if e_longo else "short") or []),
            "publicado_em": em,
            "trilha": spec.get("trilha"),
        })
    return out


COLUNAS = ("slug", "status", "formato", "titulo", "youtube_id", "canal",
           "pacote", "origem_id", "cenas", "publicado_em", "trilha")


def sql_insert(linhas: list[dict]) -> str:
    """O INSERT, com `on conflict (slug) do nothing` -- reexecutar e inofensivo."""
    if not linhas:
        return ""
    vals = []
    for l in linhas:
        campos = []
        for c in COLUNAS:
            v = l.get(c)
            campos.append("null" if v is None else
                          (str(v) if c == "cenas" else f"'{_esc(str(v))}'"))
        vals.append("(" + ",".join(campos) + ")")
    return ("insert into videos (" + ",".join(COLUNAS) + ") values "
            + ", ".join(vals) + " on conflict (slug) do nothing")


def relato(linhas: list[dict]) -> str:
    if not linhas:
        return ("REGISTRO: nenhum notice de publicacao reconhecido. Se houve "
                "publicacao, a linha de `videos` NAO existe e a metrica daquela "
                "peca vai levantar chave estrangeira quando alguem tentar medir.")
    # O aviso do 670 e so para SHORT: longo nao tem origem, ele E a origem.
    sem_origem = [l["slug"] for l in linhas
                  if not l["origem_id"] and l["formato"] != "longo"]
    fora = [f"{l['pacote']} -> {l['youtube_id']}" for l in linhas]
    linhas_txt = [f"REGISTRO: {len(linhas)} linha(s) de `videos` a inserir."]
    linhas_txt += [f"  {x}" for x in fora]
    if sem_origem:
        linhas_txt.append("  SEM origem_id (670 pede): " + ", ".join(sem_origem))
    linhas_txt.append("  rode o SQL por `execute_sql` -- o REST esta em 402 e "
                      "este modulo NAO executa nada sozinho.")
    return "\n".join(linhas_txt)


def main() -> int:
    """O relato vai para STDERR e o SQL para STDOUT, e isto e conserto MEDIDO.

    Em 15/10 as 15:2x eu rodei `registro_videos.py | tee -a
    docs/pendente/videos-a-inserir.sql` e o arquivo ficou com TRES linhas de
    prosa portuguesa dentro de um .sql -- "REGISTRO: 1 linha(s)...",
    "epomeno-epipedo-s036 -> R4Ldmvcu9k8" e o conselho de rodar por
    `execute_sql`. Quem abrisse o arquivo e colasse no SQL Editor levaria erro
    de sintaxe nas linhas 5 a 7, e o INSERT da linha 9 nao entraria.

    E a assinatura e EXATAMENTE a do 729, do outro lado: la a nota legivel do
    `estado_ponte.py` grudou no base64 porque EU redirecionei stderr para
    dentro do payload; aqui ela grudou no SQL porque o MODULO a imprimia em
    stdout. O conserto do 729 foi stdout puro, e eu nao o apliquei a este
    modulo quando o escrevi (726) -- o mesmo defeito com dois donos.
    """
    texto = sys.stdin.read()
    linhas = linhas_dos_notices(texto)
    print(relato(linhas), file=sys.stderr)
    sql = sql_insert(linhas)
    if sql:
        print(sql)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
