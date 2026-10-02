"""Máquina de cold mail (coldmail/tools): rotação, aquecimento, texto, threading, leitura e decisão.

Nada aqui fala com rede: Gmail, CRM e IA são trocados por dublês e o banco é SQLite em memória.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import random
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

FERRAMENTAS = Path(__file__).resolve().parents[1] / "coldmail" / "tools"
sys.path.insert(0, str(FERRAMENTAS))
with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}):
    import agenda  # noqa: E402
    import banco  # noqa: E402
    import cold  # noqa: E402
    import gmail  # noqa: E402
    import ia  # noqa: E402
    from rotacao import (BR, Conta, capacidade, limite_hoje, na_janela, planejar,  # noqa: E402
                         renderizar, spintax)

HOJE = dt.date(2026, 10, 1)


def conta(email, limite=30, inicio=HOJE - dt.timedelta(days=30)):
    return Conta(email=email, senha="x", nome="Pablo Sampaio", limite_dia=limite, inicio=inicio)


# ------------------------------------------------------------------ aquecimento e janela
def test_aquecimento_sobe_ate_o_teto():
    c = conta("a@x.com", limite=30, inicio=HOJE)
    assert [limite_hoje(c, HOJE + dt.timedelta(days=d)) for d in (0, 1, 5, 20)] == [5, 8, 20, 30]
    assert limite_hoje(c, HOJE - dt.timedelta(days=1)) == 0


def test_janela_so_dia_util_em_horario_comercial():
    quinta_10h = dt.datetime(2026, 10, 1, 10, tzinfo=BR)
    assert na_janela(quinta_10h)
    assert not na_janela(quinta_10h.replace(hour=19))
    assert not na_janela(dt.datetime(2026, 10, 3, 10, tzinfo=BR))   # sábado


# ------------------------------------------------------------------ rotação
def test_followup_fica_na_conta_da_conversa_e_novo_vai_para_quem_tem_folga():
    contas = [conta("a@x.com"), conta("b@x.com"), conta("c@x.com")]
    cap = {"a@x.com": 1, "b@x.com": 3, "c@x.com": 2}
    devidos = [{"id": 1, "passo": 1, "conta": "c@x.com"},
               {"id": 2, "passo": 2, "conta": "a@x.com"},
               {"id": 3, "passo": 0}, {"id": 4, "passo": 0}, {"id": 5, "passo": 0}]
    fila = planejar(devidos, contas, cap)
    por_id = {l["id"]: c for l, c in fila}
    assert por_id[1] == "c@x.com" and por_id[2] == "a@x.com"
    assert por_id[3] == "b@x.com"            # b tinha mais folga
    assert len(fila) == 5
    # intercalado: nunca a mesma conta duas vezes seguidas enquanto há outra na fila
    contas_em_ordem = [c for _, c in fila]
    assert contas_em_ordem[:3] == ["a@x.com", "b@x.com", "c@x.com"]


def test_followup_espera_quando_a_conta_dele_esta_sem_folga():
    contas = [conta("a@x.com"), conta("b@x.com")]
    fila = planejar([{"id": 1, "passo": 1, "conta": "a@x.com"}], contas, {"a@x.com": 0, "b@x.com": 5})
    assert fila == []


def test_capacidade_respeita_enviados_e_teto_da_rodada():
    contas = [conta("a@x.com", limite=30), conta("b@x.com", limite=30)]
    cap = capacidade(contas, {"a@x.com": 29}, HOJE, por_rodada=3)
    assert cap == {"a@x.com": 1, "b@x.com": 3}


# ------------------------------------------------------------------ texto
def test_spintax_e_variaveis():
    rng = random.Random(1)
    texto = renderizar("{Oi|Olá} {primeiro_nome}, tudo bem na {empresa}?\n\n{abertura}\n\n\n{x}fim",
                       {"primeiro_nome": "Joana", "empresa": "Acme", "abertura": ""}, rng)
    assert texto.split(" ")[0] in ("Oi", "Olá")
    assert "Joana, tudo bem na Acme?" in texto
    assert "\n\n\n" not in texto and "{x}" not in texto


def test_variavel_dentro_de_spintax_e_nome_vazio_sem_virgula_solta():
    for semente in range(10):
        t = renderizar("{{primeiro_nome}, pergunta rápida|pergunta sobre a {empresa}}",
                       {"primeiro_nome": "Joana", "empresa": "Acme"}, random.Random(semente))
        assert t in ("Joana, pergunta rápida", "Pergunta sobre a Acme")
    assert renderizar("Oi {primeiro_nome}, tudo bem?", {"primeiro_nome": ""}, random.Random()) == "Oi, tudo bem?"


def test_spintax_aninhado():
    assert spintax("{a|{b|b}}", random.Random(0)) in ("a", "b")


def test_trecho_opcional_some_sem_o_dado_e_aninha():
    modelo = "[[Em {mes_ano} você pediu contato[[, com o time de {vendedores}]] na {empresa_curta}.]]\nPergunta"
    cheio = {"mes_ano": "junho de 2023", "vendedores": "3 a 6 vendedores", "empresa_curta": "Acme"}
    assert renderizar(modelo, cheio, random.Random()).startswith(
        "Em junho de 2023 você pediu contato, com o time de 3 a 6 vendedores na Acme.")
    sem_time = dict(cheio, vendedores="")
    assert renderizar(modelo, sem_time, random.Random()).startswith("Em junho de 2023 você pediu contato na Acme.")
    assert renderizar(modelo, {}, random.Random()) == "Pergunta"


@pytest.mark.parametrize("bruto, esperado", [
    ("(11) 98765-4321", "+5511987654321"), ("+55 21 98742-9940", "+5521987429940"),
    ("1133224455", "+551133224455"), ("98765-4321", ""), ("meu zap é 0800 123", ""), ("", ""),
])
def test_normalizar_whatsapp(bruto, esperado):
    assert ia.normalizar_whatsapp(bruto) == esperado


def test_variavel_com_padrao():
    modelo = "A {empresa:sua empresa}, precisa de +CLIENTES?"
    assert renderizar(modelo, {"empresa": "Acme"}, random.Random()) == "A Acme, precisa de +CLIENTES?"
    assert renderizar(modelo, {"empresa": ""}, random.Random()) == "A sua empresa, precisa de +CLIENTES?"
    assert renderizar("{primeiro_nome:Oi}, voltando", {}, random.Random()) == "Oi, voltando"


@pytest.mark.parametrize("arquivo", ["sequencia.json", "sequencia.exemplo.json"])
@pytest.mark.parametrize("lead", [
    {"email": "j@acme.com", "primeiro_nome": "joana", "empresa": "Acme", "abertura": ""},
    {"email": "x@y.com", "primeiro_nome": "", "empresa": "", "abertura": ""},
])
def test_sequencias_renderizam_todos_os_passos(arquivo, lead):
    passos = json.loads((FERRAMENTAS.parent / arquivo).read_text(encoding="utf-8"))["passos"]
    c = conta("a@x.com")
    c.assinatura = "Pablo"
    for p in passos:
        for campo in ("assunto", "corpo"):
            if p.get(campo):
                t = renderizar(p[campo], cold.variaveis(lead, c), random.Random())
                assert "{" not in t and "}" not in t and "|" not in t and "[[" not in t and "]]" not in t, t
                assert not t.startswith(",") and "A , " not in t and " ," not in t, t


# ------------------------------------------------------------------ Gmail
def test_followup_vai_na_mesma_conversa():
    c = conta("a@dominio.com")
    m = gmail.montar(c, "j@acme.com", "Re: oi", "corpo", in_reply_to="<2@d>", references="<1@d>")
    assert m["In-Reply-To"] == "<2@d>"
    assert m["References"] == "<1@d> <2@d>"
    assert m["Message-ID"].endswith("@dominio.com>")
    assert "mailto:a@dominio.com" in m["List-Unsubscribe"]


def test_limpar_resposta_corta_a_citacao():
    texto = "Pode ser quinta às 14h.\n\nAbs\n\nEm qua., 1 de out. de 2026 às 10:00, Pablo escreveu:\n> Oi Joana"
    assert gmail.limpar_resposta(texto) == "Pode ser quinta às 14h.\n\nAbs"


def test_bounce_e_resposta_automatica():
    dsn = (b"From: Mail Delivery Subsystem <mailer-daemon@googlemail.com>\r\nMessage-ID: <b@g>\r\n"
           b"Subject: Delivery Status Notification (Failure)\r\nX-Failed-Recipients: Nao.Existe@acme.com\r\n\r\nx")
    r = gmail.analisar(dsn)
    assert r.falhou_para == ["nao.existe@acme.com"]
    ooo = (b"From: Joana <j@acme.com>\r\nMessage-ID: <o@a>\r\nSubject: Fora do escritorio\r\n"
           b"Auto-Submitted: auto-replied\r\n\r\nVolto dia 10.")
    assert gmail.analisar(ooo).automatica


# ------------------------------------------------------------------ banco
def test_sqlite_ignora_duplicado_e_filtra():
    db = banco.Sqlite()
    assert db.inserir("cold_leads", [{"email": "a@x.com"}, {"email": "a@x.com"}, {"email": "b@x.com"}]) == 2
    db.atualizar("cold_leads", [("email", "eq", "b@x.com")], {"status": "bounce"})
    assert [l["email"] for l in db.buscar("cold_leads", [("status", "eq", "ativo")])] == ["a@x.com"]
    assert len(db.buscar("cold_leads", [("email", "in", ["a@x.com", "b@x.com"])])) == 2
    assert db.buscar("cold_leads", [("email", "in", [])]) == []


# ------------------------------------------------------------------ decisão e agenda
@pytest.mark.parametrize("r, modo, crm, esperado", [
    ({"categoria": "descadastro", "confianca": 0.4}, "auto", True, "bloquear"),
    ({"categoria": "sugeriu_horario", "confianca": 0.9, "resposta": "ok", "horario_pedido": "terça às 10h"}, "auto",
     True, "sdr"),
    ({"categoria": "sugeriu_horario", "confianca": 0.9, "resposta": "ok", "horario_pedido": "terça às 10h"},
     "rascunho", True, "rascunho"),
    ({"categoria": "enviou_whatsapp", "confianca": 0.9, "resposta": "ok", "whatsapp": "+5511987654321"}, "auto", True,
     "sdr"),
    ({"categoria": "enviou_whatsapp", "confianca": 0.9, "resposta": "ok", "whatsapp": "+5511987654321"}, "rascunho",
     True, "rascunho"),
    ({"categoria": "interessado", "confianca": 0.9, "resposta": "ok"}, "auto", True, "responder"),
    ({"categoria": "interessado", "confianca": 0.6, "resposta": "ok"}, "auto", True, "rascunho"),
    ({"categoria": "objecao", "confianca": 0.99, "resposta": "ok"}, "auto", True, "rascunho"),
    ({"categoria": "outro", "confianca": 0.0, "resposta": ""}, "auto", True, "humano"),
])
def test_decidir(r, modo, crm, esperado):
    assert cold.decidir(r, modo, 0.8, crm) == esperado


def test_ia_numero_invalido_vira_pedido_de_whatsapp(monkeypatch):
    monkeypatch.setattr(ia, "_chamar", lambda *a, **k: json.dumps({
        "categoria": "enviou_whatsapp", "confianca": 0.95, "horario_pedido": "terça, 6/10, às 10h",
        "whatsapp": "123", "resumo": "x", "resposta": "y"}))
    r = ia.analisar_resposta({}, "nosso", "meu zap 123, pode ser terça 10h", "hoje")
    assert r["categoria"] == "sugeriu_horario" and r["whatsapp"] == "" and r["confianca"] <= 0.5


def test_ia_fora_do_ar_vai_para_humano(monkeypatch):
    def falha(*a, **k):
        raise ConnectionError("sem rede")
    monkeypatch.setattr(ia, "_chamar", falha)
    r = ia.analisar_resposta({}, "nosso", "oi", "hoje")
    assert r["categoria"] == "outro" and cold.decidir(r, "auto", 0.8, True) == "humano"


# ------------------------------------------------------------------ ponta a ponta (dublês)
@pytest.fixture
def maquina(monkeypatch, tmp_path):
    db = banco.Sqlite()
    monkeypatch.setattr(banco, "abrir", lambda exigir_remoto=False: db)
    contas = [{"email": "a@d.com", "senha_app": "x", "nome": "Pablo", "inicio": "2026-01-01"},
              {"email": "b@d.com", "senha_app": "x", "nome": "Pablo", "inicio": "2026-01-01"}]
    seq = json.loads((FERRAMENTAS.parent / "sequencia.exemplo.json").read_text(encoding="utf-8"))
    monkeypatch.setenv("COLDMAIL_CONTAS", json.dumps(contas))
    monkeypatch.setenv("COLDMAIL_SEQUENCIA", json.dumps(seq))
    monkeypatch.delenv("GHL_PIT", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    enviados, rascunhos = [], []
    monkeypatch.setattr(gmail, "enviar", lambda c, m: enviados.append((c.email, m)))
    monkeypatch.setattr(gmail, "salvar_rascunho", lambda c, m: rascunhos.append((c.email, m)))
    monkeypatch.setattr(cold.time, "sleep", lambda s: None)
    csv = tmp_path / "leads.csv"
    csv.write_text("email;nome;empresa\nj@acme.com;Joana Silva;Acme\nm@beta.com;Marcos;Beta\n"
                   "invalido;X;Y\nk@gama.com;Kátia;Gama\n", encoding="utf-8")
    assert cold.main(["importar", str(csv), "--aplicar"]) == 0
    return SimpleNamespace(db=db, enviados=enviados, rascunhos=rascunhos)


def test_envio_rotaciona_e_leitura_para_a_sequencia(maquina, monkeypatch):
    assert cold.main(["enviar", "--aplicar", "--forcar"]) == 0
    assert len(maquina.enviados) == 3
    assert {c for c, _ in maquina.enviados} == {"a@d.com", "b@d.com"}
    joana = maquina.db.buscar("cold_leads", [("email", "eq", "j@acme.com")])[0]
    assert joana["passo"] == 1 and joana["status"] == "ativo" and joana["thread_msgid"]
    assert joana["primeiro_nome"] == "Joana"

    # Joana responde: a sequência dela para e a resposta da IA vira rascunho (modo padrão)
    bruto = ("From: Joana <j@acme.com>\r\nMessage-ID: <r1@acme.com>\r\nSubject: Re: %s\r\n"
             "In-Reply-To: %s\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nTenho interesse, como funciona?"
             % (joana["assunto"], joana["thread_msgid"])).encode("utf-8")
    monkeypatch.setattr(gmail, "ler_caixa", lambda c, desde: [gmail.analisar(bruto)] if c.email == joana["conta"] else [])
    monkeypatch.setattr(ia, "analisar_resposta", lambda *a, **k: {
        "categoria": "pediu_info", "confianca": 0.9, "horario_pedido": "", "resumo": "quer saber mais",
        "resposta": "Claro! Posso te mostrar em 20 min na quinta às 14h?"})
    assert cold.main(["ler", "--aplicar"]) == 0
    joana = maquina.db.buscar("cold_leads", [("email", "eq", "j@acme.com")])[0]
    assert joana["status"] == "respondeu" and joana["categoria"] == "pediu_info"
    assert len(maquina.rascunhos) == 1
    _, rasc = maquina.rascunhos[0]
    assert rasc["In-Reply-To"] == "<r1@acme.com>" and rasc["Subject"].startswith("Re:")

    # segunda leitura não reprocessa a mesma mensagem
    assert cold.main(["ler", "--aplicar"]) == 0
    assert len(maquina.rascunhos) == 1

    # Joana não recebe follow-up; os outros recebem o passo 2 na mesma conta e na mesma conversa
    maquina.db.atualizar("cold_leads", [("status", "in", ["ativo", "respondeu"])],
                         {"proximo_envio": "2000-01-01T00:00:00+00:00"})
    antes = {l["email"]: l for l in maquina.db.buscar("cold_leads")}
    maquina.enviados.clear()
    assert cold.main(["enviar", "--aplicar", "--forcar"]) == 0
    assert {m["To"] for _, m in maquina.enviados} == {"m@beta.com", "k@gama.com"}
    for c, m in maquina.enviados:
        assert c == antes[m["To"]]["conta"]
        assert m["In-Reply-To"] == antes[m["To"]]["ultimo_msgid"]


def test_descadastro_bloqueia_para_sempre(maquina, monkeypatch):
    cold.main(["enviar", "--aplicar", "--forcar"])
    bruto = b"From: m@beta.com\r\nMessage-ID: <s@beta>\r\nSubject: Re: x\r\n\r\nme tira da lista"
    monkeypatch.setattr(gmail, "ler_caixa", lambda c, desde: [gmail.analisar(bruto)])
    monkeypatch.setattr(ia, "analisar_resposta", lambda *a, **k: {
        "categoria": "descadastro", "confianca": 0.99, "horario_pedido": "", "resumo": "", "resposta": ""})
    cold.main(["ler", "--aplicar"])
    assert maquina.db.buscar("cold_leads", [("email", "eq", "m@beta.com")])[0]["status"] == "descadastro"
    assert maquina.db.buscar("cold_bloqueio", [("email", "eq", "m@beta.com")])
    assert maquina.rascunhos == []


def test_lead_que_sugere_horario_vira_tarefa_da_sdr_sem_marcar(maquina, monkeypatch):
    cold.main(["enviar", "--aplicar", "--forcar"])
    chamadas = []
    monkeypatch.setattr(agenda, "ativo", lambda: True)
    monkeypatch.setattr(agenda, "contato", lambda lead, tags, tel="": chamadas.append(("contato", tel)) or "C1")
    monkeypatch.setattr(agenda, "oportunidade", lambda cid, nome: chamadas.append(("oportunidade", cid)) or "O1")
    monkeypatch.setattr(agenda, "tarefa", lambda cid, titulo, corpo, resp=None: chamadas.append(("tarefa", titulo, corpo)))
    monkeypatch.setenv("COLDMAIL_MODO", "auto")
    bruto = b"From: k@gama.com\r\nMessage-ID: <q@gama>\r\nSubject: Re: x\r\n\r\nPode ser terca as 10h?"
    monkeypatch.setattr(gmail, "ler_caixa", lambda c, desde: [gmail.analisar(bruto)])
    monkeypatch.setattr(ia, "_chamar", lambda *a, **k: json.dumps({
        "categoria": "sugeriu_horario", "confianca": 0.95, "horario_pedido": "terça, 6/10, às 10h", "whatsapp": "",
        "resumo": "topou", "resposta": "Anotei terça às 10h. Me passa seu WhatsApp para a SDR confirmar?"}))
    maquina.enviados.clear()
    cold.main(["ler", "--aplicar"])
    assert ("oportunidade", "C1") in chamadas
    tarefa = [c for c in chamadas if c[0] == "tarefa"][0]
    assert "confirmar dia e horário" in tarefa[1] and "terça, 6/10, às 10h" in tarefa[2]
    assert "ainda não mandou número" in tarefa[2]
    assert [m["To"] for _, m in maquina.enviados] == ["k@gama.com"]
    assert not hasattr(agenda, "marcar")     # a máquina não marca reunião: quem marca é a SDR


def test_resposta_com_whatsapp_grava_telefone_e_cria_tarefa(maquina, monkeypatch):
    cold.main(["enviar", "--aplicar", "--forcar"])
    chamadas = []
    monkeypatch.setattr(agenda, "ativo", lambda: True)
    monkeypatch.setattr(agenda, "contato", lambda lead, tags, tel="": chamadas.append(("contato", tel)) or "C1")
    monkeypatch.setattr(agenda, "oportunidade", lambda cid, nome: "O1")
    monkeypatch.setattr(agenda, "tarefa", lambda cid, titulo, corpo, resp=None: chamadas.append(("tarefa", titulo, corpo)))
    monkeypatch.setenv("COLDMAIL_MODO", "auto")
    bruto = b"From: k@gama.com\r\nMessage-ID: <w@gama>\r\nSubject: Re: x\r\n\r\nMeu zap: (11) 98765-4321"
    monkeypatch.setattr(gmail, "ler_caixa", lambda c, desde: [gmail.analisar(bruto)])
    monkeypatch.setattr(ia, "_chamar", lambda *a, **k: json.dumps({
        "categoria": "enviou_whatsapp", "confianca": 0.95, "horario_pedido": "", "whatsapp": "(11) 98765-4321",
        "resumo": "mandou o zap", "resposta": "Obrigado! Te chamo ainda hoje no WhatsApp."}))
    maquina.enviados.clear()
    cold.main(["ler", "--aplicar"])
    assert ("contato", "+5511987654321") in chamadas
    tarefas = [c for c in chamadas if c[0] == "tarefa"]
    assert tarefas and "WhatsApp" in tarefas[0][1] and "confirmar dia e horário" in tarefas[0][1] and "+5511987654321" in tarefas[0][2]
    assert [m["To"] for _, m in maquina.enviados] == ["k@gama.com"]


def test_contato_existente_nao_perde_tags_nem_cadastro(monkeypatch):
    pedidos = []

    def falso(metodo, rota, corpo=None):
        pedidos.append((metodo, rota, corpo))
        if rota.startswith("/contacts/search/duplicate") and "number=" in rota:
            return {"contact": {"id": "EXISTE", "phone": "+5521987429940"}}
        if rota.startswith("/contacts/search/duplicate"):
            return {}
        return {}
    monkeypatch.setattr(agenda, "pedir", falso)
    cid = agenda.contato({"email": "novo@acme.com", "primeiro_nome": "Ana", "empresa": "Acme"},
                         ["cold-email"], "+5521987429940")
    assert cid == "EXISTE"
    metodos = [(m, r.split("?")[0]) for m, r, _ in pedidos]
    assert ("POST", "/contacts/EXISTE/tags") in metodos      # só acrescenta tag
    assert ("POST", "/contacts/upsert") not in metodos       # nada de sobrescrever nome/empresa/tags
    assert not any(m == "PUT" for m, _ in metodos)           # já tinha telefone


def test_segunda_resposta_vira_nota_e_resposta_de_outro_endereco_e_reconhecida(maquina, monkeypatch):
    cold.main(["enviar", "--aplicar", "--forcar"])
    k = maquina.db.buscar("cold_leads", [("email", "eq", "k@gama.com")])[0]
    chamadas = []
    monkeypatch.setattr(agenda, "ativo", lambda: True)
    monkeypatch.setattr(agenda, "contato", lambda lead, tags, tel="": "C1")
    monkeypatch.setattr(agenda, "oportunidade", lambda cid, nome: "O1")
    monkeypatch.setattr(agenda, "pedir", lambda metodo, rota, corpo=None: chamadas.append(("pedir", metodo, rota, corpo)))
    monkeypatch.setattr(agenda, "tarefa", lambda cid, titulo, corpo, resp=None: chamadas.append(("tarefa", titulo)))
    monkeypatch.setattr(agenda, "nota", lambda cid, corpo: chamadas.append(("nota", corpo)))
    monkeypatch.setenv("COLDMAIL_MODO", "auto")
    # 1ª resposta vem de OUTRO endereço (secretária), só achável pela conversa; 2ª corrige o número
    r1 = ("From: secretaria@gama.com\r\nMessage-ID: <r1@gama>\r\nIn-Reply-To: %s\r\nSubject: Re: x\r\n\r\n"
          "zap 2188887744" % k["thread_msgid"]).encode()
    r2 = ("From: k@gama.com\r\nMessage-ID: <r2@gama>\r\nIn-Reply-To: <r1@gama>\r\nReferences: %s <r1@gama>\r\n"
          "Subject: Re: x\r\n\r\ncorrigindo: 21988877729" % k["thread_msgid"]).encode()
    monkeypatch.setattr(gmail, "ler_caixa", lambda c, desde: [gmail.analisar(r1), gmail.analisar(r2)]
                        if c.email == k["conta"] else [])
    numeros = iter(["2188887744", "21988877729"])
    monkeypatch.setattr(ia, "_chamar", lambda *a, **kw: json.dumps({
        "categoria": "enviou_whatsapp", "confianca": 0.95, "horario_pedido": "", "whatsapp": next(numeros),
        "resumo": "mandou o zap", "resposta": "Obrigado! A SDR vai te chamar."}))
    cold.main(["ler", "--aplicar"])
    assert [c for c in chamadas if c[0] == "tarefa"] == [("tarefa", "[COLD] Ligar ou chamar no WhatsApp para confirmar dia e horário")]
    assert any(c[0] == "nota" for c in chamadas)
    assert ("pedir", "PUT", "/contacts/C1", {"phone": "+5521988877729"}) in chamadas
