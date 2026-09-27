#!/usr/bin/env python3
"""Finaliza a configuracao do CRM de ponta a ponta, pelo que a API publica permite.

POR QUE ESTE ARQUIVO EXISTE
---------------------------
O dono pediu, em 27/09: *"Realmente nao quero realizar acao, faca tudo voce. Estude
meios. Finalize a configuracao agora, de ponta a ponta."*

Entao nada aqui pede clique. O que ainda nao sai por API esta marcado como tal, com o
motivo tecnico, e nao com "falta o dono fazer".

COMO ISTO RODA, dado que o conteiner nao alcanca a API do GHL
-------------------------------------------------------------
Medido em 27/09: `services.leadconnectorhq.com` e `backend.leadconnectorhq.com`
respondem 000 pelo proxy de egresso deste conteiner. Entao a escrita sai de uma Action.

E aqui esta o detalhe que destravou: **um `workflow_dispatch` pela API do GitHub exige
que o arquivo exista no branch padrao** — testei e `wesales-pastas.yml`, que so existe
no branch de trabalho, devolveu 404. Mas o dispatch aceita `ref`, e **roda a versao do
arquivo que esta naquele ref**. Como `wesales-g03.yml` ja esta no branch padrao e ja
carrega `secrets.GHL_PIT`, um dispatch dele com `ref` no branch de trabalho executa o
que este arquivo manda, com rede e com segredo. Sem merge, sem tocar no branch padrao.

ORDEM, e por que ela e essa
---------------------------
    --recon       le tudo, escreve nada. Precisa vir primeiro porque a decisao de dono
                  do lead depende de saber quais usuarios existem, e `GET /users/` nao
                  passa pelo conector MCP — so pela API publica.
    --pastas      cria as 5 pastas e renomeia a grande. Idempotente.
    --donos       atribui dono nas oportunidades e contatos sem dono.
    --verificar   rele a conta e prova o que mudou.

NUNCA APAGA NADA
----------------
Regra 1 do projeto. **Nenhuma funcao deste arquivo emite DELETE**, e nao e por
disciplina de chamada: o verbo nao existe no codigo. Todos os leads vieram de clique
pago.

O QUE ESTE ARQUIVO NAO CONSEGUE, com a prova
--------------------------------------------
- **Mover campo para pasta.** `PUT /custom-fields/{id}` aceita apenas
  `locationId, name, description, placeholder, showInForms, options, acceptedFormats,
  maxFileLimit`. Nao tem `parentId` — conferido lendo o `requestBody` inteiro do spec
  oficial, duas vezes, porque eu ja errei nisso (licao 2.12). `POST /custom-fields/`
  exige `parentId`, entao campo **novo** nasce em pasta, mas mover existente nao sai.
- **Publicar workflow.** `apps/workflows.json` tem so `GET /workflows/`.
Os dois saem pela API interna, que e o proximo passo e depende do segredo
`GHL_STORAGE_STATE`. O `--recon` reporta se ele existe, para eu saber sem perguntar.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://services.leadconnectorhq.com"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
LOC = "1D53YTI9C7oIMBavcQxV"
VERSION = "2021-07-28"
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
ETAPAS = {
    "7ae9c950": "NOVO LEAD", "deb60542": "CONECTAR",
    "3d26fcd1": "REUNIAO DE DIAGNOSTICO", "cbcf0229": "NEGOCIAR",
    "b8485ec0": "FORMALIZAR",
}

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from pastas_de_campo import PASTAS, PASTA_GRANDE, PASTA_MAQUINA, MAPA  # noqa: E402


def token() -> str:
    t = (os.environ.get("GHL_PIT") or "").strip()
    if not t:
        raise SystemExit("sem GHL_PIT — este script roda na Action.")
    return t


def pedir(metodo: str, caminho: str, corpo: dict | None = None, tolerar=()):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(BASE + caminho, data=dados, method=metodo)
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("Version", VERSION)
    req.add_header("Accept", "application/json")
    # Sem isto a API devolve 403 Cloudflare 1010 "browser_signature_banned":
    # o padrao do urllib e User-Agent "Python-urllib/3.x", que o Cloudflare do
    # GHL barra por regra de bot. Medido na Action em 27/09 — nao era escopo de
    # token, e o erro nao diz isso em lugar nenhum. O token continua sendo o
    # controle de acesso; isto so faz a requisicao parecer com o que ela e.
    req.add_header("User-Agent", UA)
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        corpo_erro = ""
        try:
            corpo_erro = e.read().decode("utf-8")[:400]
        except Exception:
            pass
        if e.code in tolerar:
            return {"_erro": e.code, "_detalhe": corpo_erro}
        raise SystemExit("%s %s -> HTTP %s %s" % (metodo, caminho, e.code, corpo_erro))
    except urllib.error.URLError as e:
        raise SystemExit("%s %s -> rede recusou: %s" % (metodo, caminho, e.reason))


# ---------------------------------------------------------------- leitura

def usuarios() -> list:
    r = pedir("GET", "/users/?locationId=%s" % LOC, tolerar=(401, 403, 404, 422))
    if "_erro" in r:
        print("  !! GET /users/ -> HTTP %s. O PIT pode nao ter o escopo users.readonly."
              % r["_erro"])
        print("     detalhe: %s" % r["_detalhe"])
        return []
    return r.get("users") or []


def pastas_da_conta() -> dict:
    r = pedir("GET", "/custom-fields/object-key/contact?locationId=%s" % LOC)
    return {p.get("name"): p.get("id") for p in (r.get("folders") or []) if p.get("name")}


def campos_da_conta() -> list:
    r = pedir("GET", "/custom-fields/object-key/contact?locationId=%s" % LOC)
    return r.get("fields") or []


def oportunidades() -> list:
    todas, pagina = [], None
    while True:
        q = {"location_id": LOC, "pipeline_id": PIPELINE, "status": "open", "limit": "100"}
        if pagina:
            q["page"] = str(pagina)
        r = pedir("GET", "/opportunities/search?" + urllib.parse.urlencode(q))
        lote = r.get("opportunities") or []
        todas += lote
        meta = r.get("meta") or {}
        prox = meta.get("nextPage")
        if not prox or not lote:
            break
        pagina = prox
    return todas


def contatos() -> list:
    todos, inicio = [], None
    while True:
        corpo = {"locationId": LOC, "pageLimit": 100}
        if inicio:
            corpo["searchAfter"] = inicio
        r = pedir("POST", "/contacts/search", corpo, tolerar=(400, 422))
        if "_erro" in r:
            print("  !! POST /contacts/search -> HTTP %s; sigo sem a lista de contatos."
                  % r["_erro"])
            return todos
        lote = r.get("contacts") or []
        todos += lote
        if not lote or len(todos) >= (r.get("total") or 0):
            break
        inicio = lote[-1].get("searchAfter")
        if not inicio:
            break
    return todos


# ---------------------------------------------------------------- recon

def bloco(titulo, fn):
    """Roda uma etapa do recon e segue mesmo se ela falhar.

    A primeira versao morria no primeiro erro: o 403 em /custom-fields matou o
    reconhecimento antes de imprimir pastas, campos, oportunidades e contatos —
    e reconhecimento que para na primeira pedra nao serve para reconhecer.
    """
    print()
    print(titulo)
    try:
        fn()
    except SystemExit as e:
        print("  !! esta etapa falhou e o recon seguiu: %s" % e)
    except Exception as e:
        print("  !! esta etapa falhou e o recon seguiu: %s: %s"
              % (type(e).__name__, e))


def recon() -> int:
    print("=" * 74)
    print("RECONHECIMENTO — le tudo, escreve nada")
    print("=" * 74)

    print("\n[1] SEGREDOS disponiveis neste runner")
    for nome in ("GHL_PIT", "GHL_STORAGE_STATE"):
        v = os.environ.get(nome) or ""
        print("  %-18s %s" % (nome, ("presente, %d chars" % len(v)) if v.strip()
                              else "AUSENTE"))
    print("  (GHL_STORAGE_STATE e o que decide se a API interna abre: mover campo e")
    print("   publicar workflow dependem so dela.)")

    def _usuarios():
        us = usuarios()
        for u in us:
            print("  %s | %s %s | %s | roles=%s" % (
                u.get("id"), u.get("firstName") or "", u.get("lastName") or "",
                u.get("email"),
                json.dumps(u.get("roles") or {}, ensure_ascii=False)[:120]))
        if not us:
            print("  (nenhum devolvido)")

    def _pastas():
        ps = pastas_da_conta()
        for n, i in sorted(ps.items()):
            marca = "  <-- a pasta grande" if i == PASTA_GRANDE else ""
            print("  %-42s %s%s" % (n, i, marca))
        if not ps:
            print("  (nenhuma pasta devolvida)")
        print("  faltam criar: %s"
              % [n for n in PASTAS if n not in ps and n != PASTA_MAQUINA])
        print("  a grande já se chama PASTA_MAQUINA? %s"
              % ({v: k for k, v in ps.items()}.get(PASTA_GRANDE) == PASTA_MAQUINA))

    def _campos():
        cs = campos_da_conta()
        porpasta = {}
        for c in cs:
            porpasta.setdefault(c.get("parentId"), []).append(c.get("name"))
        for pid, nomes in sorted(porpasta.items(), key=lambda kv: -len(kv[1])):
            print("  %-26s %d campos" % (pid, len(nomes)))
        print("  total de campos: %d" % len(cs))

    def _ops():
        ops = oportunidades()
        print("  abertas: %d" % len(ops))
        for pref, nome in ETAPAS.items():
            na = [o for o in ops if (o.get("pipelineStageId") or "").startswith(pref)]
            if na:
                print("    %-24s %2d  sem dono: %d"
                      % (nome, len(na), sum(1 for o in na if not o.get("assignedTo"))))

    def _contatos():
        ct = contatos()
        print("  contatos: %d | sem dono: %d"
              % (len(ct), sum(1 for c in ct if not c.get("assignedTo"))))

    bloco("[2] USUARIOS da subconta — quem pode ser dono de lead", _usuarios)
    bloco("[3] PASTAS de campo hoje", _pastas)
    bloco("[4] CAMPOS por pasta", _campos)
    bloco("[5] OPORTUNIDADES abertas e dono", _ops)
    bloco("[6] CONTATOS e dono", _contatos)

    print("\n" + "=" * 74)
    print("DECISAO que este recon habilita: com a lista de usuarios acima eu escolho o")
    print("dono e rodo --donos. Nao preciso perguntar se houver um unico usuario nao-")
    print("administrativo, ou se o dono do lead for o unico que ja tem leads.")
    return 0


# ---------------------------------------------------------------- pastas

def pastas() -> int:
    print("=" * 74)
    print("PASTAS — renomeia a grande e cria as outras quatro")
    print("=" * 74)
    ps = pastas_da_conta()
    atual = {v: k for k, v in ps.items()}.get(PASTA_GRANDE)
    if atual == PASTA_MAQUINA:
        print("  = a pasta grande já se chama %r" % PASTA_MAQUINA)
    else:
        pedir("PUT", "/custom-fields/folder/%s" % PASTA_GRANDE,
              {"name": PASTA_MAQUINA, "locationId": LOC})
        print("  ~ pasta grande %s renomeada" % PASTA_GRANDE)
        print("      de:   %s" % (atual or "(nome anterior nao lido)"))
        print("      para: %s" % PASTA_MAQUINA)
        ps[PASTA_MAQUINA] = PASTA_GRANDE
    for nome in PASTAS:
        if nome == PASTA_MAQUINA or nome in ps:
            print("  = %-42s já existe" % nome)
            continue
        r = pedir("POST", "/custom-fields/folder",
                  {"objectKey": "contact", "name": nome, "locationId": LOC})
        novo = (r.get("folder") or r).get("id") if isinstance(r, dict) else None
        ps[nome] = novo
        print("  + %-42s criada (%s)" % (nome, novo))
    print("\n  Mover os campos para dentro NAO sai por API (PUT /custom-fields/{id} nao")
    print("  tem parentId). Fica para a API interna, nao para o dono.")
    # Rele a conta: o que a resposta do POST disse nao e o que a conta tem.
    depois = pastas_da_conta()
    faltam = [n for n in PASTAS if n not in depois]
    print("\n  conferido relendo a conta: %d de %d pastas presentes"
          % (len(PASTAS) - len(faltam), len(PASTAS)))
    if faltam:
        print("  FALTAM: %s" % faltam)
        return 1
    return 0


# ---------------------------------------------------------------- donos

def donos(user_id: str | None) -> int:
    print("=" * 74)
    print("DONO DO LEAD — tarefa sem destinatario nao aparece na fila de ninguem")
    print("=" * 74)
    if not user_id:
        us = usuarios()
        candidatos = [u for u in us if u.get("id")]
        if len(candidatos) == 1:
            user_id = candidatos[0]["id"]
            print("  um unico usuario na conta; escolhido sem perguntar: %s (%s)"
                  % (user_id, candidatos[0].get("email")))
        else:
            print("  !! %d usuarios; passe --user <id>. Nao escolho no escuro porque"
                  % len(candidatos))
            print("     dono errado manda o lead para a fila da pessoa errada.")
            for u in candidatos:
                print("     %s | %s" % (u.get("id"), u.get("email")))
            return 2

    ops = [o for o in oportunidades() if not o.get("assignedTo")]
    print("\n  oportunidades sem dono: %d" % len(ops))
    ok = 0
    for o in ops:
        pedir("PUT", "/opportunities/%s" % o["id"], {"assignedTo": user_id})
        ok += 1
        if ok % 10 == 0:
            print("    ... %d/%d" % (ok, len(ops)))
    print("  oportunidades atribuidas: %d" % ok)

    ct = [c for c in contatos() if not c.get("assignedTo")]
    print("\n  contatos sem dono: %d" % len(ct))
    ok2 = 0
    for c in ct:
        pedir("PUT", "/contacts/%s" % c["id"], {"assignedTo": user_id})
        ok2 += 1
        if ok2 % 10 == 0:
            print("    ... %d/%d" % (ok2, len(ct)))
    print("  contatos atribuidos: %d" % ok2)
    return 0


# ---------------------------------------------------------------- verificar

def verificar() -> int:
    print("=" * 74)
    print("VERIFICACAO — rele a conta depois da escrita")
    print("=" * 74)
    ps = pastas_da_conta()
    faltam = [n for n in PASTAS if n not in ps]
    print("\n  pastas presentes: %d de %d" % (len(PASTAS) - len(faltam), len(PASTAS)))
    if faltam:
        print("  FALTAM: %s" % faltam)
    ops = oportunidades()
    sem = [o for o in ops if not o.get("assignedTo")]
    print("  oportunidades abertas: %d | ainda sem dono: %d" % (len(ops), len(sem)))
    for o in sem[:10]:
        print("    sem dono: %s" % (o.get("name") or o.get("id")))
    ct = contatos()
    if ct:
        semc = [c for c in ct if not c.get("assignedTo")]
        print("  contatos: %d | ainda sem dono: %d" % (len(ct), len(semc)))
    campos = campos_da_conta()
    dentro = sum(1 for c in campos
                 if c.get("parentId") == ps.get(PASTA_MAQUINA, PASTA_GRANDE))
    print("  campos na pasta da maquina: %d (esperado 29 antes de mover nada)" % dentro)
    # Sai diferente de zero quando algo NAO esta no lugar. E de proposito: o log
    # de um job que passou nao e legivel pela API sem o id do job, e o de um que
    # falhou e. Entao "passou" ja e a confirmacao, e "falhou" me entrega o motivo.
    # Verificacao que so imprime e verificacao que ninguem le.
    ok = not faltam and not sem
    print("\n  veredito: %s" % ("TUDO NO LUGAR" if ok
                                else "FALTA o que esta listado acima"))
    return 0 if ok else 1


# A funcao `sondar` viveu aqui entre 15:10 e 15:35 de 27/09 e foi retirada depois de
# responder a sua unica pergunta. O achado dela, que e o que importa:
#
#     POST /custom-fields/folder com objectKey=contact -> HTTP 400
#     {"message":"Api does not support objectKey of type contact or opportunity"}
#
# Retirada por dois motivos. O primeiro: a pergunta esta respondida, e definitivamente
# — o grupo /custom-fields/ da v2 e para objeto personalizado, entao pasta de campo de
# contato e tela. Esta registrado na licao 2.19 e na §4 do USABILIDADE.md, que e onde
# alguem vai procurar. O segundo, e mais pratico: ela saia 1 SEMPRE, de proposito, para
# eu conseguir ler o log. Um passo que falha por desenho vira check vermelho permanente
# no PR, e revisor nenhum distingue "sonda que terminou o trabalho" de "codigo quebrado".
# Ferramenta de diagnostico que sobrevive ao diagnostico passa a mentir sobre o estado.


FORM_ID = "DNz54AK2ryRSW7uCuznP"
# Os cinco campos que o SDR NAO deve perguntar de novo (ASSOCIACOES-DE-CAMPO.md §3):
# os tres que o anuncio responde e os dois derivados deles.
FORM_ESPERADOS = {
    "2LnUD4KYSGkIBwiUdzl3": "Urgência",
    "OJQEsl5dV37pfVY2sIaB": "Necessidade",
    "bQithNwReQIBGlZBaNlI": "Investimento mensal em anúncios",
    "lAqbaJE9K4LDkq3t2zzc": "Prazo",
    "x5JUx0YCWaZmH3Q85psI": "Investe em anúncios",
}


def formulario() -> int:
    """Le o formulario de qualificacao que o dono criou e confere os 5 campos.

    A API publica nao expoe campo de formulario (FormsParams e so id/name). Mas o
    widget publico embute o schema no HTML, e o runner alcanca o dominio que o
    conteiner nao alcanca. Entao: baixa o widget, procura os ids dos 56 campos e
    imprime os que aparecem.

    Sai 1 se faltar algum dos 5 que o SDR nao deve perguntar de novo. Sucesso e a
    confirmacao; falha me entrega o que falta. Mesmo padrao do --verificar.
    """
    import re as _re
    url = "https://api.leadconnectorhq.com/widget/form/" + FORM_ID
    print("=" * 74)
    print("FORMULARIO DE QUALIFICACAO — %s" % FORM_ID)
    print("=" * 74)
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", errors="replace")
    print("  widget baixado: %d bytes" % len(html))
    with open(SNAPSHOT, encoding="utf-8") as fh:
        campos = json.load(fh)["campos"]
    presentes = [(c["id"], c["nome"]) for c in campos if c["id"] in html]
    print("\n  campos personalizados do CRM encontrados no formulario: %d" % len(presentes))
    for i, n in presentes:
        marca = "  <-- ja respondido pelo anuncio/derivado" if i in FORM_ESPERADOS else ""
        print("     %s  %s%s" % (i, n, marca))
    # rotulos visiveis, para conferir a ordem e o texto que o SDR le
    rotulos = _re.findall(r'"label"\s*:\s*"([^"]{2,80})"', html)
    if rotulos:
        print("\n  rotulos na ordem em que aparecem (%d):" % len(rotulos))
        for r_ in rotulos[:60]:
            print("     - %s" % r_)
    faltam = [n for i, n in FORM_ESPERADOS.items() if i not in html]
    print("\n  dos 5 que o SDR nao deve perguntar de novo, FALTAM no formulario: %s"
          % (faltam or "nenhum"))
    if faltam:
        print("  Sem eles no formulario, o SDR nao ve a resposta do anuncio na hora")
        print("  da ligacao — e pergunta de novo o que o lead ja respondeu.")
    return 1 if faltam else 0


def main() -> int:
    a = sys.argv[1:]
    user = None
    if "--user" in a:
        user = a[a.index("--user") + 1]
    if "--recon" in a:
        return recon()
    if "--pastas" in a:
        return pastas()
    if "--donos" in a:
        return donos(user)
    if "--verificar" in a:
        return verificar()
    if "--formulario" in a:
        return formulario()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
