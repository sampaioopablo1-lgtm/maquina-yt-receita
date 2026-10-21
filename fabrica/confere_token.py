#!/usr/bin/env python3
"""Testa o token OAuth do canal ANTES de gastar render.

Existe por causa de 19/08/2026: o agla-level-004 renderizou 20 minutos, foi
entregue no Storage e so entao a publicacao descobriu que o refresh token
tinha morrido — 45 minutos DEPOIS de eu mesmo o ter testado vivo. Naquela
madrugada 9 dos 12 tokens morreram em cascata (aprendizado 303/304): os
emitidos enquanto o app OAuth ainda estava em modo Testing expiram no seu
proprio marco de 7 dias, um a um, sem aviso.

Falhar aqui custa 30 segundos e deixa a mensagem certa no log; falhar no
passo de publicacao custa o render inteiro e um pacote parado.

Desde 20/08/2026 ele confere mais que "o token vive". O epomeno-epipedo-008 foi
publicado e a legenda do longo levou 403 "permissions not sufficient", porque a
concessao real do Google nao tinha `youtube.force-ssl` — enquanto
`config.yt_token_epomeno-epipedo.scopes` a LISTAVA. Esse campo guarda o que foi
PEDIDO no fluxo de autorizacao, nao o que foi CONCEDIDO, e eu o li como prova de
permissao numa auditoria dos treze canais. Nao e prova.

A prova existe e e de graca: a resposta do refresh traz o campo `scope`, que e a
lista EFETIVA. Este arquivo le esse campo e exige force-ssl — sem ela o longo
sobe sem legenda, que nao e cosmetico em canal de idioma nao-ingles
(aprendizado 93).

O campo `scopes` do banco continua como esta, DE PROPOSITO. Eu cheguei a
escrever aqui um passo que o corrigia com a resposta do Google, e o desfiz antes
de rodar: `config.valor` e uma coluna jsonb unica, um PATCH nela substitui o
objeto INTEIRO, e dentro desse objeto mora o `refresh_token`. Consertar um campo
descritivo nao vale o risco de apagar a credencial dos treze canais. A saida
certa e nao confiar no campo — e e o que este arquivo faz agora, perguntando ao
Google toda vez em vez de ler o registro.

E EXISTEM DOIS SEGREDOS DE CREDENCIAL COM CONCESSOES DIFERENTES — medido em
21/10/2026, com os dois instrumentos na mesma hora, e isto nao estava escrito em
lugar nenhum:

  * este arquivo le pelo `publicar.token_do_canal`, que tenta
    `YT_TOKEN_<CANAL>` (AUSENTE, 0 chars nos tres) e cai no **`YT_TOKEN_JSON`**.
    A concessao que voltou para o `labtreinamento` (job 119070898648) foi
    `youtube` + `youtube.upload` + **`yt-analytics.readonly`**, SEM force-ssl;
  * o `sonda_oauth.py` le o **`YT_OAUTH_JSON`** (1116 chars, 3 canais), que e o
    que o `retomar.yml` usa para PUBLICAR, e nos tres canais ele responde
    `upload=sim, force-ssl=sim, analytics=NAO` (job 119073920894).

Logo os dois blobs divergem nos DOIS escopos que importam, em sentidos opostos.
Duas respostas para a mesma pergunta, cada uma de um dono — e a leitura errada
disso seria concluir "o dono reautorizou e perdeu o force-ssl", que e o que eu ia
escrever com um instrumento so.

**E A CONSEQUENCIA MAIOR E A OUTRA METADE: o `yt-analytics.readonly` existe em
`YT_TOKEN_JSON`.** Este repo reporta esse escopo como PERDIDO desde o
aprendizado 689, e a retencao e a unica alavanca do tamanho do problema. Escopo
concedido NAO e prova de que o dado vem — quem prova e uma chamada a Analytics
API com essa credencial, e ela nao foi feita ainda. Fica NOMEADO aqui em vez de
celebrado.

Uso: python3 fabrica/confere_token.py <canal> [spec.json]
Ambiente: SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (ou SB/KEY).
"""
import json
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import formato_da_peca as FP  # noqa: E402  — UM dono de "esta peca tem longo?"
from medir import CANAIS  # noqa: E402  — DONO do mapa slug -> id de canal

CANAIS_API = "https://www.googleapis.com/youtube/v3/channels"


def _env(*nomes):
    for n in nomes:
        v = os.environ.get(n)
        if v:
            return v.rstrip("/") if n.endswith("URL") or n == "SB" else v
    return None


def token_do_canal(canal, sb, sk):
    """Delega ao `publicar.token_do_canal` — ENV primeiro, REST depois.

    Tinha uma copia propria que so sabia ler o REST, e isso fazia este portao
    ser MAIS SEVERO que o passo que ele guarda: com o secret no lugar e a porta
    do Supabase fechada, aqui reprovava e o `publicar.py` teria publicado. Duas
    implementacoes da mesma pergunta divergem, e a divergencia aparece no pior
    momento — depois de dezessete minutos de render.
    """
    import publicar

    return publicar.token_do_canal(canal, sb, sk)


ESCOPO_LEGENDA = "https://www.googleapis.com/auth/youtube.force-ssl"
ESCOPO_ENVIO = "https://www.googleapis.com/auth/youtube.upload"

ESCOPOS_NECESSARIOS = {
    # captions.insert do longo. Sem ela o video sobe, e sobe MUDO para a busca.
    ESCOPO_LEGENDA: "enviar a faixa de legenda do longo",
    # videos.insert.
    ESCOPO_ENVIO: "publicar o video",
}


def escopos_necessarios(sp=None):
    """O que ESTA peca precisa, nao o que o formato mais exigente precisa.

    Medido em 21/10/2026, e e o defeito que este arquivo ja nomeia uma vez no
    `token_do_canal`: **portao mais severo que o passo que ele guarda e portao
    que mente.** Ali a severidade extra era ler o REST quando o `publicar.py`
    le o ENV; aqui e exigir o escopo da LEGENDA de uma peca que nao tem legenda
    para enviar.

    A prova esta no `publicar.py`: a chamada de `captions.insert` mora DENTRO
    do `if os.path.exists(longo)` (linha 1128 dentro do bloco da 1100), logo
    short solto nunca a alcanca. Todo o resto do caminho do short —
    `videos.insert`, `thumbnails.set`, `playlistItems.insert`, `videos.update`
    — se satisfaz com `youtube.upload` e `youtube`. O comentario fixado e
    PARSEADO da copy e nunca postado, logo `commentThreads.insert`, que
    exigiria force-ssl, nao acontece.

    E O TAMANHO VAI MEDIDO EM VEZ DE VENDIDO: este buraco e **LATENTE** para a
    producao desta frota, e eu o escrevi primeiro como "ATIVO". Medido depois: o
    passo que chama este portao no `frota.yml` tem `if: inputs.publicar`, e as
    rodadas renderizam com `publicar=false` e publicam pelo `retomar.yml` — logo
    o portao nao roda nelas. Quem o fez disparar foi um disparo MEU sem o
    `publicar=false`, que e o DEFAULT do workflow (true). Entao o que isto fecha
    e a invocacao PADRAO do `frota.yml`, nao a linha de producao; dizer o
    contrario seria vender conserto de defeito ativo, o que a nota do
    `test_duracao_dos_dois_provedores` (13/10) proibe em letra.

    O que o revelou: em 21/10 as 06:1x (run
    39554457072, job 119070898648) a concessao do
    `labtreinamento` perdeu o force-ssl (e ganhou `yt-analytics.readonly`), e
    este portao abortou o render do `labtreinamento-s098` — um short solto — por
    um escopo que a publicacao dele nao usa. Com **256** das 396 specs do disco
    sendo short solto, isso aborta o render de QUALQUER uma delas na invocacao
    padrao.

    `sp=None` devolve o conjunto ESTRITO de proposito: nao saber que peca e nao
    e licenca para ser permissivo, e e assim que o `diagnostico.yml` chama este
    arquivo. Quem afrouxa aqui tem de provar, no `publicar.py`, que a chamada
    nao acontece — afrouxar portao para a peca passar e o avesso do trabalho.
    """
    if sp is None or FP.tem_longo(sp):
        return dict(ESCOPOS_NECESSARIOS)
    return {ESCOPO_ENVIO: ESCOPOS_NECESSARIOS[ESCOPO_ENVIO]}


def canal_do_access_token(acc):
    """De QUEM e este token, perguntado a API. `None` se nao deu para ler.

    POR QUE ISTO EXISTE (21/10/2026, run 39560816227). O `publicar.py` carrega,
    na linha 150, a frase *"o `publicar.py` ainda pergunta a API de quem e o
    token antes de subir"* — e **essa frase e uma PROMESSA, nao codigo**: o
    unico confronto que existia era com o campo `canal`/`slug` DECLARADO dentro
    do segredo, e o `YT_TOKEN_JSON` nao declara nenhum.

    E a consequencia foi medida, nao suposta: o `chama_retencao` perguntou a API
    de quem e esse blob e a resposta foi **`UCf4-ZFoZQWKJotZNdi4Yl7w`**, que e o
    canal **Setiap Level** — um dos dez PARADOS, fora da frota. Logo, com
    `publicar=true` no `frota.yml`, uma peca da frota seria enviada para OUTRO
    canal, em silencio. O proprio `publicar.py` diz que isso "ja aconteceu uma
    vez (14/08)".

    Nas rodadas isso nao ocorreu porque elas publicam pelo `retomar.yml`, que le
    o `YT_OAUTH_JSON` (mapa POR CANAL). E o que separou um short da frota de uma
    subida no canal errado, no meu disparo das 06:1x, foram duas falhas sem
    relacao — o escopo da legenda e o 402 do nome. **Isso e sorte, nao metodo.**

    NUNCA imprime o token: devolve so o id do canal, que e publico.
    """
    req = urllib.request.Request(
        CANAIS_API + "?part=id&mine=true",
        headers={"Authorization": "Bearer " + acc})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            itens = json.load(r).get("items") or []
    except Exception:                                      # noqa: BLE001
        return None
    return (itens[0].get("id") if itens else None)


def _spec(caminho):
    """Le a spec quando o chamador a passa; `None` quando nao passa.

    Spec ilegivel NAO vira short solto: ela vira `None`, que e o conjunto
    estrito. Ler um arquivo torto como "peca sem longo" seria transformar um
    defeito de leitura em permissao, que e o sentido permissivo.
    """
    if not caminho:
        return None
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 fabrica/confere_token.py <canal> [spec.json]")
    canal = sys.argv[1]
    sp = _spec(sys.argv[2] if len(sys.argv) > 2 else None)
    preciso = escopos_necessarios(sp)
    sb = _env("SUPABASE_URL", "SB")
    sk = _env("SUPABASE_SERVICE_ROLE_KEY", "KEY")
    if not (sb and sk):
        sys.exit("AMBIENTE: sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY")
    tok = token_do_canal(canal, sb, sk)
    dados = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
    }).encode()
    req = urllib.request.Request(tok["token_uri"], data=dados, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resposta = json.load(r)
        resposta["access_token"]
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:300]
        sys.exit(
            f"TOKEN MORTO ({canal}): {e.code} {corpo}\n"
            f"O refresh token expirou ou foi revogado. Nada aqui se conserta "
            f"sozinho: o Pablo precisa reautorizar ESTE canal pelo link de "
            f"autorizacao e colar a URL do localhost. O render foi abortado de "
            f"proposito — renderizar sem rota de publicacao gasta 20 minutos "
            f"para produzir um pacote parado (aprendizado 304)."
        )
    # `scope` vem da resposta do proprio Google: e o que foi CONCEDIDO. Se o
    # campo faltar (algumas respostas de refresh o omitem), nao da para concluir
    # nada — e dizer "nao deu para conferir" e melhor que inventar aprovacao.
    bruto = resposta.get("scope")
    if not bruto:
        print(f"token de {canal}: vivo (a resposta do refresh nao trouxe "
              f"`scope`; os escopos efetivos ficam por conferir)")
        return 0

    concedidos = set(bruto.split())
    faltando = [d for e, d in preciso.items() if e not in concedidos]
    if faltando:
        sys.exit(
            f"ESCOPO FALTANDO ({canal}): a concessao do Google nao permite "
            f"{', '.join(faltando)}.\n"
            f"Concedidos: {' '.join(sorted(concedidos)) or '(nenhum)'}\n"
            f"O token VIVE — o que falta e permissao, e reautorizar e a unica "
            f"saida. O Pablo precisa refazer a autorizacao DESTE canal marcando "
            f"todas as caixas do consentimento.\n"
            f"O render foi abortado de proposito: publicar um longo que nao "
            f"pode levar legenda e publicar mudo para a busca (aprendizado 93), "
            f"e publicacao nao se desfaz."
        )
    # DE QUEM E O TOKEN — e aqui a severidade e maxima de proposito: publicar
    # no canal errado nao se desfaz, e a autorizacao de 09/10 nao cobre mover
    # nem apagar video publicado.
    esperado = CANAIS.get(canal)
    real = canal_do_access_token(resposta["access_token"])
    if esperado and real and real != esperado:
        sys.exit(
            f"CANAL ERRADO ({canal}): a credencial que o render usaria pertence "
            f"ao canal {real}, e {canal} e {esperado}.\n"
            f"Publicar daqui subiria a peca em OUTRO canal, e publicacao nao se "
            f"desfaz — o render foi abortado de proposito.\n"
            f"Os secrets `YT_TOKEN_<CANAL>` estao ausentes, logo o "
            f"`publicar.token_do_canal` cai no `YT_TOKEN_JSON`, que e um token "
            f"UNICO e generico. As rodadas publicam pelo `retomar.yml`, que le o "
            f"`YT_OAUTH_JSON` (mapa POR CANAL) e NAO tem este problema."
        )
    if esperado and real is None:
        print(f"::warning title=Dono do token nao lido::nao deu para perguntar a "
              f"API de quem e a credencial de {canal} — ausencia de leitura NAO "
              f"e prova de que o canal esta certo")
    elif esperado and real == esperado:
        print(f"canal conferido na API: {real}")

    print(f"token de {canal}: vivo, com os {len(preciso)} escopo(s) que ESTA "
          f"peca precisa concedido(s)")
    # NOMEIA em vez de filtrar: o escopo que esta peca nao usa pode ser
    # exatamente o que a proxima usa, e descobrir isso por render abortado custa
    # a rodada. Fica ::warning:: porque o short ESTA certo e o conserto e do
    # lado do dono.
    if ESCOPO_LEGENDA not in concedidos:
        print(f"::warning title=Sem escopo de legenda::a concessao de {canal} "
              f"NAO tem youtube.force-ssl, logo PACOTE COM LONGO segue "
              f"abortado neste canal (captions.insert; aprendizado 93). Esta "
              f"peca passou porque e short solto e nao envia legenda. Concedidos:"
              f" {' '.join(sorted(concedidos))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
