#!/usr/bin/env python3
"""Máquina de cold mail com várias contas Gmail em rotação: prospecta, envia, lê a resposta e agenda.

    python coldmail/tools/cold.py contas [--testar]          # contas, limite de hoje (aquecimento), login
    python coldmail/tools/cold.py importar leads.csv          # DRY: valida e conta
    python coldmail/tools/cold.py importar leads.csv --aplicar
    python coldmail/tools/cold.py personalizar --limite 50 --aplicar   # 1ª linha por IA a partir do site
    python coldmail/tools/cold.py enviar [--aplicar]          # uma rodada de envios, intercalando as contas
    python coldmail/tools/cold.py ler [--aplicar]             # lê respostas, classifica, responde/agenda
    python coldmail/tools/cold.py status

Sem --aplicar nada é enviado, gravado nem marcado: só mostra o que faria (padrão dos robôs do wesales).

Modo das respostas (COLDMAIL_MODO):
  rascunho (padrão)  a resposta escrita pela IA fica nos Rascunhos da conta, na conversa do lead, e a SDR
                     ganha tarefa no CRM. Ninguém recebe nada sem uma pessoa clicar em Enviar.
  auto               "aceitou horário" livre na agenda -> marca a reunião e confirma por e-mail;
                     "enviou WhatsApp" -> grava o número no CRM, tarefa da SDR (ligar ou chamar no
                     WhatsApp para confirmar dia e horário) e responde avisando que a SDR vai entrar em contato;
                     "interessado" -> pede o WhatsApp (e oferece horários). Só com confiança >=
                     COLDMAIL_CONFIANCA_MIN (0.8). Objeção, pedido de informação etc. continuam em rascunho.
Descadastro e bounce são sempre automáticos: o lead sai da sequência e entra na lista de bloqueio.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import random
import re
import smtplib
import sys
import time
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import agenda  # noqa: E402  (importa o privacidade do wesales: log do Actions sem dado de lead)
import banco  # noqa: E402
import gmail  # noqa: E402
import ia  # noqa: E402
from rotacao import (BR, Conta, assunto_resposta, capacidade, espacamento, limite_hoje,  # noqa: E402
                     na_janela, planejar, proximo_envio, renderizar, variaveis)

RAIZ = AQUI.parent
LOCAL = RAIZ / ".local"
EMAIL = re.compile(r"^[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
CRM_CATEGORIAS = {"aceitou_horario", "enviou_whatsapp", "interessado", "pediu_info", "objecao"}


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def no_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true"


def _json_de(env: str, arquivo: Path):
    bruto = (os.environ.get(env) or "").strip()
    if bruto:
        return json.loads(bruto)
    if arquivo.exists():
        return json.loads(arquivo.read_text(encoding="utf-8"))
    return None


def carregar_contas() -> list[Conta]:
    dados = _json_de("COLDMAIL_CONTAS", LOCAL / "contas.json")
    if not dados:
        raise SystemExit("nenhuma conta: preencha o segredo COLDMAIL_CONTAS (ou coldmail/.local/contas.json) "
                         "no formato de coldmail/contas.exemplo.json")
    contas = [Conta.de_dict(d) for d in dados if d.get("ativa", True)]
    sem_senha = [c.email for c in contas if not c.senha]
    if sem_senha:
        raise SystemExit("conta sem senha_app: %s" % ", ".join(sem_senha))
    return contas


def carregar_sequencia(aplicar: bool) -> list[dict]:
    dados = _json_de("COLDMAIL_SEQUENCIA", LOCAL / "sequencia.json")
    if dados is None and (RAIZ / "sequencia.json").exists():
        dados = json.loads((RAIZ / "sequencia.json").read_text(encoding="utf-8"))
    if dados is None:
        if aplicar:
            raise SystemExit("sem sequência: crie coldmail/sequencia.json (ou o segredo COLDMAIL_SEQUENCIA). "
                             "O sequencia.exemplo.json não é enviado de verdade.")
        print("(DRY com coldmail/sequencia.exemplo.json)")
        dados = json.loads((RAIZ / "sequencia.exemplo.json").read_text(encoding="utf-8"))
    passos = dados["passos"] if isinstance(dados, dict) else dados
    if not passos or not passos[0].get("assunto"):
        raise SystemExit("sequência inválida: o 1º passo precisa de assunto e corpo")
    return passos


def configuracao() -> dict:
    janela = (os.environ.get("COLDMAIL_JANELA") or "8-18").split("-")
    return {
        "modo": (os.environ.get("COLDMAIL_MODO") or "rascunho").strip().lower(),
        "confianca_min": float(os.environ.get("COLDMAIL_CONFIANCA_MIN") or 0.8),
        "por_rodada": int(os.environ.get("COLDMAIL_POR_RODADA") or 3),
        "janela": (int(janela[0]), int(janela[1])),
        "link_agenda": os.environ.get("COLDMAIL_LINK_AGENDA") or "",
        "rampa": {"rampa_inicial": int(os.environ.get("COLDMAIL_RAMPA_INICIAL") or 5),
                  "rampa_passo": int(os.environ.get("COLDMAIL_RAMPA_PASSO") or 3)},
    }


def _em_lotes(db, tabela: str, coluna: str, valores, colunas: str = "*", lote: int = 80) -> list[dict]:
    valores = sorted(set(valores))
    saida = []
    for i in range(0, len(valores), lote):
        saida += db.buscar(tabela, [(coluna, "in", valores[i:i + lote])], colunas=colunas)
    return saida


def enviados_hoje(db, agora: dt.datetime) -> Counter:
    inicio = agora.astimezone(BR).replace(hour=0, minute=0, second=0, microsecond=0)
    return Counter(e["conta"] for e in db.buscar("cold_envios", [("enviado_em", "gte", iso(inicio))],
                                                 colunas="conta"))


# ---------------------------------------------------------------- contas
def cmd_contas(args) -> int:
    contas = carregar_contas()
    cfg = configuracao()
    hoje = dt.datetime.now(BR).date()
    db = banco.abrir()
    feitos = enviados_hoje(db, dt.datetime.now(dt.timezone.utc))
    total = 0
    for c in contas:
        lim = limite_hoje(c, hoje, **cfg["rampa"])
        total += lim
        linha = "  %-38s limite hoje %3d (teto %d, desde %s) · enviados hoje %d" % (
            c.email, lim, c.limite_dia, c.inicio.isoformat(), feitos.get(c.email, 0))
        if args.testar:
            ok, det = gmail.testar_login(c)
            linha += " · %s %s" % ("OK" if ok else "FALHOU", det)
        print(linha)
    print("%d contas · capacidade hoje: %d e-mails" % (len(contas), total))
    return 0


# ---------------------------------------------------------------- importar
def ler_csv(caminho: str) -> tuple[list[dict], list[str]]:
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t") if amostra else csv.excel
        linhas = list(csv.DictReader(f, dialect=dialeto))
    leads, problemas = [], []
    vistos = set()
    for n, bruta in enumerate(linhas, start=2):
        linha = {(k or "").strip().lower(): (v or "").strip() for k, v in bruta.items()}
        email = linha.pop("email", "").lower()
        if not EMAIL.match(email):
            problemas.append("linha %d: e-mail inválido" % n)
            continue
        if email in vistos:
            continue
        vistos.add(email)
        nome = linha.pop("primeiro_nome", "") or linha.pop("nome", "").split(" ")[0]
        linha.pop("nome", None)
        site = linha.pop("site", "")
        if site and not site.startswith("http"):
            site = "https://" + site
        lead = {"email": email, "primeiro_nome": nome, "empresa": linha.pop("empresa", ""),
                "cargo": linha.pop("cargo", ""), "site": site, "abertura": linha.pop("abertura", "")}
        extra = {k: v for k, v in linha.items() if k and v}
        lead["extra"] = json.dumps(extra, ensure_ascii=False) if extra else None
        leads.append(lead)
    return leads, problemas


def cmd_importar(args) -> int:
    leads, problemas = ler_csv(args.csv)
    for p in problemas[:20]:
        print("  ! " + p)
    db = banco.abrir()
    bloqueados = {b["email"] for b in _em_lotes(db, "cold_bloqueio", "email", [l["email"] for l in leads],
                                                colunas="email")}
    ja = {l["email"] for l in _em_lotes(db, "cold_leads", "email", [l["email"] for l in leads], colunas="email")}
    novos = [l for l in leads if l["email"] not in bloqueados and l["email"] not in ja]
    print("%d linhas válidas · %d na lista de bloqueio · %d já importados · %d novos" % (
        len(leads), len(bloqueados), len(ja), len(novos)))
    if not args.aplicar:
        print("(DRY: nada gravado; use --aplicar)")
        return 0
    agora = iso(dt.datetime.now(dt.timezone.utc))
    for l in novos:
        l.update({"status": "ativo", "passo": 0, "proximo_envio": agora})
    print("gravados: %d" % db.inserir("cold_leads", novos))
    return 0


# ---------------------------------------------------------------- personalizar
def cmd_personalizar(args) -> int:
    db = banco.abrir(exigir_remoto=no_actions())
    candidatos = db.buscar("cold_leads", [("status", "eq", "ativo"), ("passo", "eq", 0)],
                           ordem="id.asc", limite=args.limite * 5)
    alvo = [l for l in candidatos if not l.get("abertura") and l.get("site")][:args.limite]
    print("%d leads sem primeira linha e com site" % len(alvo))
    for l in alvo:
        frase = ia.abertura(l)
        print("  %s: %s" % (l["email"], frase or "(nada específico)"))
        if args.aplicar and frase:
            db.atualizar("cold_leads", [("id", "eq", l["id"])], {"abertura": frase})
    return 0


# ---------------------------------------------------------------- enviar
def montar_envio(lead: dict, conta: Conta, passos: list[dict], rng: random.Random):
    passo = int(lead.get("passo") or 0)
    p = passos[passo]
    try:
        extra = json.loads(lead.get("extra") or "{}")
    except ValueError:
        extra = {}
    v = variaveis(lead, conta, extra)
    corpo = renderizar(p["corpo"], v, rng)
    if passo == 0 or not lead.get("ultimo_msgid"):
        return gmail.montar(conta, lead["email"], renderizar(p["assunto"], v, rng), corpo), passo
    assunto = renderizar(p["assunto"], v, rng) if p.get("assunto") and p.get("nova_conversa") \
        else assunto_resposta(lead.get("assunto") or "")
    return gmail.montar(conta, lead["email"], assunto, corpo, in_reply_to=lead["ultimo_msgid"],
                        references=lead.get("thread_msgid")), passo


def cmd_enviar(args) -> int:
    cfg = configuracao()
    agora = dt.datetime.now(dt.timezone.utc)
    if not na_janela(agora, *cfg["janela"]) and not args.forcar:
        print("fora da janela de envio (%dh-%dh, seg-sex): nada a enviar" % cfg["janela"])
        return 0
    contas = carregar_contas()
    por_email = {c.email: c for c in contas}
    passos = carregar_sequencia(args.aplicar)
    db = banco.abrir(exigir_remoto=no_actions() and args.aplicar)

    devidos = db.buscar("cold_leads", [("status", "eq", "ativo"), ("proximo_envio", "lte", iso(agora))],
                        ordem="proximo_envio.asc", limite=1000)
    cap = capacidade(contas, enviados_hoje(db, agora), agora.astimezone(BR).date(), cfg["por_rodada"],
                     **cfg["rampa"])
    plano = planejar(devidos, contas, cap)
    bloqueados = {b["email"] for b in _em_lotes(db, "cold_bloqueio", "email", [l["email"] for l, _ in plano],
                                                colunas="email")}
    print("%d leads devidos · %d envios nesta rodada · folga por conta: %s" % (
        len(devidos), len(plano), ", ".join("%s=%d" % (c, n) for c, n in cap.items())))

    espaco = espacamento(len(plano))
    falhas: set[str] = set()
    feitos = 0
    for i, (lead, email_conta) in enumerate(plano):
        if email_conta in falhas:
            continue
        conta = por_email[email_conta]
        if lead["email"] in bloqueados:
            if args.aplicar:
                db.atualizar("cold_leads", [("id", "eq", lead["id"])], {"status": "descadastro"})
            continue
        if int(lead.get("passo") or 0) >= len(passos):
            if args.aplicar:
                db.atualizar("cold_leads", [("id", "eq", lead["id"])], {"status": "concluido"})
            continue
        rng = random.Random()
        msg, passo = montar_envio(lead, conta, passos, rng)
        print("  %s · passo %d/%d · via %s%s" % (lead["email"], passo + 1, len(passos), email_conta,
                                                "" if args.aplicar else " (DRY)"))
        if not args.aplicar:
            if args.mostrar:
                print("    Assunto: %s\n    %s" % (msg["Subject"], msg.get_content().strip().replace("\n", "\n    ")))
            continue
        try:
            gmail.enviar(conta, msg)
        except smtplib.SMTPAuthenticationError as e:
            falhas.add(email_conta)
            print("  !! %s recusou o login (senha de app?): %s — conta parada nesta rodada" % (email_conta, e))
            continue
        except smtplib.SMTPRecipientsRefused:
            db.atualizar("cold_leads", [("id", "eq", lead["id"])], {"status": "bounce"})
            db.inserir("cold_bloqueio", [{"email": lead["email"], "motivo": "recusado no envio"}])
            continue
        except smtplib.SMTPDataError as e:
            if e.smtp_code in (421, 450, 451, 550, 552, 554):
                falhas.add(email_conta)
                print("  !! %s bloqueada pelo Gmail (%s): conta parada nesta rodada — confira a caixa" % (
                    email_conta, e.smtp_code))
            continue
        except (smtplib.SMTPException, OSError) as e:
            print("  !! falha de envio (%s): o lead fica para a próxima rodada" % type(e).__name__)
            continue

        mid = msg["Message-ID"]
        db.inserir("cold_envios", [{"lead_id": lead["id"], "conta": email_conta, "passo": passo,
                                    "message_id": mid, "enviado_em": iso(dt.datetime.now(dt.timezone.utc))}])
        campos = {"passo": passo + 1, "conta": email_conta, "ultimo_msgid": mid,
                  "atualizado_em": iso(dt.datetime.now(dt.timezone.utc))}
        if passo == 0:
            campos.update({"assunto": str(msg["Subject"]), "thread_msgid": mid})
        if passo + 1 < len(passos):
            campos["proximo_envio"] = iso(proximo_envio(agora, int(passos[passo + 1].get("espera_dias") or 3), rng))
        else:
            campos.update({"status": "concluido", "proximo_envio": None})
        db.atualizar("cold_leads", [("id", "eq", lead["id"])], campos)
        feitos += 1
        if i < len(plano) - 1 and espaco:
            time.sleep(espaco * rng.uniform(0.7, 1.3))
    print("enviados: %d%s" % (feitos, (" · contas com problema: %s" % ", ".join(sorted(falhas))) if falhas else ""))
    return 0


# ---------------------------------------------------------------- ler
def decidir(r: dict, modo: str, confianca_min: float, crm: bool) -> str:
    """O que fazer com a resposta já classificada. Regra pura (testada)."""
    cat, conf = r.get("categoria"), float(r.get("confianca") or 0)
    if cat == "descadastro":
        return "bloquear"
    if cat == "fora_do_escritorio":
        return "ignorar"
    seguro = modo == "auto" and conf >= confianca_min and bool(r.get("resposta"))
    if cat == "aceitou_horario" and seguro and crm and r.get("horario_escolhido"):
        return "marcar_e_responder"
    if cat == "enviou_whatsapp" and seguro and r.get("whatsapp"):
        return "whatsapp"
    if cat in ("aceitou_horario", "interessado") and seguro:
        return "responder"
    return "rascunho" if r.get("resposta") else "humano"


def _ultimo_email(lead: dict, conta: Conta, passos: list[dict]) -> str:
    """Reconstrói (aproximado: o spintax pode ter sorteado outra variação) o último e-mail que mandamos."""
    passo = max(0, min(int(lead.get("passo") or 1) - 1, len(passos) - 1))
    try:
        extra = json.loads(lead.get("extra") or "{}")
    except ValueError:
        extra = {}
    return "Assunto: %s\n\n%s" % (lead.get("assunto") or "", renderizar(
        passos[passo]["corpo"], variaveis(lead, conta, extra), random.Random(0)))


def cmd_ler(args) -> int:
    cfg = configuracao()
    contas = carregar_contas()
    passos = carregar_sequencia(False)
    db = banco.abrir(exigir_remoto=no_actions() and args.aplicar)
    agora = dt.datetime.now(dt.timezone.utc)
    desde = agora.astimezone(BR).date() - dt.timedelta(days=args.dias)
    crm = agenda.ativo()
    cache_horarios: dict[str, str] | None = None

    def horarios() -> dict[str, str]:
        nonlocal cache_horarios
        if cache_horarios is None:
            cache_horarios = {}
            if crm:
                try:
                    cache_horarios = {h: agenda.por_extenso(h) for h in agenda.horarios_livres(agora)}
                except RuntimeError as e:
                    print("  agenda indisponível: %s" % e)
        return cache_horarios

    def registrar(m, conta, tipo, lead=None, r=None, acao=None):
        if args.aplicar:
            db.inserir("cold_mensagens", [{
                "message_id": m.message_id, "lead_id": (lead or {}).get("id"), "conta": conta.email,
                "recebido_em": iso(m.data or agora), "tipo": tipo, "categoria": (r or {}).get("categoria"),
                "confianca": (r or {}).get("confianca"), "acao": acao}])

    def atualizar_lead(lead, campos):
        if args.aplicar:
            db.atualizar("cold_leads", [("id", "eq", lead["id"])],
                         {**campos, "atualizado_em": iso(dt.datetime.now(dt.timezone.utc))})

    resumo = Counter()
    for conta in contas:
        try:
            msgs = gmail.ler_caixa(conta, desde)
        except Exception as e:
            print("  !! %s: não consegui ler a caixa (%s: %s)" % (conta.email, type(e).__name__, str(e)[:120]))
            continue
        vistos = {x["message_id"] for x in _em_lotes(db, "cold_mensagens", "message_id",
                                                     [m.message_id for m in msgs], colunas="message_id")}
        novos = [m for m in msgs if m.message_id not in vistos]
        enderecos = {m.de for m in novos} | {a for m in novos for a in m.falhou_para}
        leads = {l["email"]: l for l in _em_lotes(db, "cold_leads", "email", enderecos)}

        for m in novos:
            if m.falhou_para:
                for addr in m.falhou_para:
                    if addr in leads and args.aplicar:
                        atualizar_lead(leads[addr], {"status": "bounce", "proximo_envio": None})
                        db.inserir("cold_bloqueio", [{"email": addr, "motivo": "bounce"}])
                print("  bounce: %s" % ", ".join(m.falhou_para))
                resumo["bounce"] += 1
                registrar(m, conta, "bounce")
                continue
            lead = leads.get(m.de)
            if not lead:
                registrar(m, conta, "outra")
                continue
            if lead["status"] in ("descadastro", "bounce"):
                registrar(m, conta, "ignorada", lead)
                continue
            if m.automatica:
                print("  %s: resposta automática (segue a sequência)" % lead["email"])
                resumo["automatica"] += 1
                registrar(m, conta, "resposta", lead, {"categoria": "fora_do_escritorio"}, "ignorar")
                continue

            # resposta de verdade: a sequência para já, antes de qualquer outra coisa
            atualizar_lead(lead, {"status": "respondeu", "proximo_envio": None})
            r = ia.analisar_resposta(lead, _ultimo_email(lead, conta, passos), m.texto, horarios(),
                                     cfg["link_agenda"], agenda.por_extenso(iso(agora)))
            acao = decidir(r, cfg["modo"], cfg["confianca_min"], crm)
            resumo[r["categoria"]] += 1
            print("  %s → %s (%.2f) → %s%s" % (lead["email"], r["categoria"], float(r.get("confianca") or 0),
                                              acao, "" if args.aplicar else " (DRY)"))
            if r.get("resumo"):
                print("    %s" % r["resumo"])
            if not args.aplicar:
                if args.mostrar and r.get("resposta"):
                    print("    ---\n    %s" % r["resposta"].replace("\n", "\n    "))
                continue

            try:
                acao = executar(acao, r, lead, conta, m, crm, atualizar_lead, db)
            except Exception as e:   # CRM/Gmail fora: registra e deixa para humano, sem reprocessar e duplicar
                print("  !! não consegui executar %s (%s: %s)" % (acao, type(e).__name__, str(e)[:160]))
                acao = "erro:" + acao
            registrar(m, conta, "resposta", lead, r, acao)

    print("respostas: %s" % (", ".join("%s=%d" % kv for kv in resumo.most_common()) or "nenhuma nova"))
    return 0


def executar(acao: str, r: dict, lead: dict, conta: Conta, m, crm: bool, atualizar_lead, db) -> str:
    cat = r["categoria"]
    campos = {"categoria": cat}
    if acao == "bloquear":
        atualizar_lead(lead, {**campos, "status": "descadastro"})
        db.inserir("cold_bloqueio", [{"email": lead["email"], "motivo": "pediu para sair"}])
        return acao
    if acao == "ignorar":   # a IA viu ausência que o cabeçalho não acusou: a sequência volta a andar
        atualizar_lead(lead, {**campos, "status": "ativo",
                              "proximo_envio": iso(dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=3))})
        return acao

    cid = ""
    if crm and cat in CRM_CATEGORIAS:
        cid = agenda.contato(lead, ["cold-email", "cold-" + cat.replace("_", "-")], r.get("whatsapp") or "")
        campos["ghl_contato"] = cid
        agenda.oportunidade(cid, "%s · Cold e-mail" % (lead.get("empresa") or lead.get("primeiro_nome") or lead["email"]))
    corpo = (r.get("resposta") or "").strip()
    assinatura = conta.assinatura or (conta.nome.split(" ")[0] if conta.nome else "")
    resposta = gmail.montar(conta, lead["email"], assunto_resposta(m.assunto),
                            corpo + ("\n\n" + assinatura if assinatura else ""),
                            in_reply_to=m.message_id, references=m.references) if corpo else None

    if acao == "marcar_e_responder":
        quando = r["horario_escolhido"]
        agenda.marcar(cid, quando, "%s · Cold e-mail" % (lead.get("empresa") or lead.get("primeiro_nome") or "Reunião"))
        gmail.enviar(conta, resposta)
        agenda.nota(cid, "Cold e-mail: marcou sozinho para %s respondendo ao e-mail de %s.\nResumo: %s" % (
            agenda.por_extenso(quando), conta.email, r.get("resumo") or "-"))
        atualizar_lead(lead, {**campos, "status": "reuniao"})
    elif acao == "whatsapp":
        gmail.enviar(conta, resposta)
        if cid:
            agenda.tarefa(cid, "[COLD] Ligar ou chamar no WhatsApp para confirmar dia e horário", (
                "O lead respondeu ao cold e-mail (%s) com o WhatsApp %s. Já respondemos que a SDR vai ligar ou "
                "mandar mensagem para confirmar o melhor dia e horário: faça isso hoje e marque a reunião na agenda "
                "'Reunião com closer'.\nResumo: %s"
                % (conta.email, r["whatsapp"], r.get("resumo") or "-")))
        atualizar_lead(lead, campos)
    elif acao == "responder":
        gmail.enviar(conta, resposta)
        if cid:
            agenda.nota(cid, "Cold e-mail (%s): respondemos automaticamente oferecendo horários.\nResumo: %s"
                        % (cat, r.get("resumo") or "-"))
        atualizar_lead(lead, campos)
    else:
        if resposta:
            gmail.salvar_rascunho(conta, resposta)
        if cid:
            agenda.tarefa(cid, "[COLD] Responder e-mail (%s)" % cat.replace("_", " "), (
                "O lead respondeu ao cold e-mail enviado por %s.\nResumo: %s\n%s%s\n"
                "%s" % (conta.email, r.get("resumo") or "-",
                        ("WhatsApp que ele mandou: %s\n" % r["whatsapp"]) if r.get("whatsapp") else "",
                        ("Horário que ele pediu: %s" % agenda.por_extenso(r["horario_escolhido"]))
                        if r.get("horario_escolhido") else "",
                        "Resposta pronta nos Rascunhos dessa conta, na conversa do lead: revise e envie."
                        if resposta else "Responda direto pela caixa dessa conta.")))
        atualizar_lead(lead, {**campos, "status": "nao_agora" if cat == "nao_agora" else "respondeu"})
    return acao


# ---------------------------------------------------------------- status
def cmd_status(args) -> int:
    db = banco.abrir()
    leads = db.buscar("cold_leads", colunas="status,passo")
    print("leads: %d" % len(leads))
    for st, n in Counter(l["status"] for l in leads).most_common():
        print("  %-12s %d" % (st, n))
    agora = dt.datetime.now(dt.timezone.utc)
    sete = iso(agora - dt.timedelta(days=7))
    envios = db.buscar("cold_envios", [("enviado_em", "gte", sete)], colunas="conta")
    msgs = db.buscar("cold_mensagens", [("recebido_em", "gte", sete), ("tipo", "in", ["resposta", "bounce"])],
                     colunas="tipo,categoria")
    print("últimos 7 dias: %d envios · %d respostas · %d bounces" % (
        len(envios), sum(1 for x in msgs if x["tipo"] == "resposta"), sum(1 for x in msgs if x["tipo"] == "bounce")))
    for cat, n in Counter(x["categoria"] for x in msgs if x["tipo"] == "resposta").most_common():
        print("  %-20s %d" % (cat, n))
    for c, n in enviados_hoje(db, agora).most_common():
        print("  hoje via %s: %d" % (c, n))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("contas")
    s.add_argument("--testar", action="store_true", help="faz login SMTP e IMAP em cada conta")
    s = sub.add_parser("importar")
    s.add_argument("csv")
    s.add_argument("--aplicar", action="store_true")
    s = sub.add_parser("personalizar")
    s.add_argument("--limite", type=int, default=50)
    s.add_argument("--aplicar", action="store_true")
    s = sub.add_parser("enviar")
    s.add_argument("--aplicar", action="store_true")
    s.add_argument("--forcar", action="store_true", help="ignora a janela de horário")
    s.add_argument("--mostrar", action="store_true", help="no DRY, mostra o texto de cada e-mail")
    s = sub.add_parser("ler")
    s.add_argument("--aplicar", action="store_true")
    s.add_argument("--dias", type=int, default=3)
    s.add_argument("--mostrar", action="store_true", help="no DRY, mostra a resposta que a IA escreveu")
    sub.add_parser("status")
    args = ap.parse_args(argv)
    return {"contas": cmd_contas, "importar": cmd_importar, "personalizar": cmd_personalizar,
            "enviar": cmd_enviar, "ler": cmd_ler, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
