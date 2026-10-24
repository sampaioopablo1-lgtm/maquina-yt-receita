"""Conversa com as caixas Gmail/Google Workspace: SMTP para enviar, IMAP para ler e guardar rascunho.

Autenticação por SENHA DE APP (Conta Google > Segurança > Verificação em duas etapas > Senhas de app).
Não precisa de projeto no Google Cloud nem de OAuth, e serve igual para @gmail.com e Workspace.

Leitura sempre em modo somente-leitura (BODY.PEEK): a máquina não marca nada como lido na caixa.
"""
from __future__ import annotations

import datetime as dt
import email
import email.policy
import imaplib
import re
import smtplib
import time
from dataclasses import dataclass, field
from email.message import EmailMessage
from email.utils import formataddr, formatdate, getaddresses, make_msgid, parseaddr

from rotacao import Conta

SMTP_HOST, SMTP_PORTA = "smtp.gmail.com", 465
IMAP_HOST = "imap.gmail.com"
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def montar(conta: Conta, para: str, assunto: str, corpo: str,
           in_reply_to: str | None = None, references: str | None = None) -> EmailMessage:
    """Texto puro (entrega melhor que HTML em cold mail), Message-ID do domínio da conta e,
    em follow-up/resposta, In-Reply-To + References para cair na mesma conversa do lead."""
    msg = EmailMessage()
    msg["From"] = formataddr((conta.nome, conta.email)) if conta.nome else conta.email
    msg["To"] = para
    msg["Subject"] = assunto
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=conta.email.split("@", 1)[1])
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        refs = (references or "").split()
        if in_reply_to not in refs:
            refs.append(in_reply_to)
        msg["References"] = " ".join(refs)
    # Descadastro em um clique pelo próprio e-mail: quem responde "sair" cai na lista de bloqueio
    msg["List-Unsubscribe"] = "<mailto:%s?subject=sair>" % conta.email
    msg.set_content(corpo)
    return msg


def enviar(conta: Conta, msg: EmailMessage) -> None:
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORTA, timeout=60) as s:
        s.login(conta.email, conta.senha)
        s.send_message(msg)


def testar_login(conta: Conta) -> tuple[bool, str]:
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORTA, timeout=30) as s:
            s.login(conta.email, conta.senha)
        with imaplib.IMAP4_SSL(IMAP_HOST) as im:
            im.login(conta.email, conta.senha)
        return True, "SMTP e IMAP ok"
    except (smtplib.SMTPException, imaplib.IMAP4.error, OSError) as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:160])


@dataclass
class Recebida:
    message_id: str
    de: str
    assunto: str
    data: dt.datetime | None
    in_reply_to: str = ""
    references: str = ""
    texto: str = ""
    automatica: bool = False          # fora do escritório / resposta automática
    falhou_para: list[str] = field(default_factory=list)   # preenchido só em bounce


CORTE = re.compile(
    r"^\s*(>|Em .{0,200}escreveu:|On .{0,200}wrote:|-{2,}\s*Original Message|-{2,}\s*Mensagem original|"
    r"De:\s|From:\s|Enviado do meu|Sent from my)", re.I)


def limpar_resposta(texto: str, limite: int = 4000) -> str:
    """Fica só com o que o lead escreveu: corta a citação do nosso e-mail e a assinatura de celular."""
    linhas = []
    for linha in (texto or "").replace("\r\n", "\n").split("\n"):
        if CORTE.match(linha):
            break
        linhas.append(linha)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()[:limite]


def _texto(msg) -> str:
    try:
        parte = msg.get_body(preferencelist=("plain", "html"))
    except Exception:
        parte = None
    if parte is None:
        return ""
    try:
        conteudo = parte.get_content()
    except Exception:
        conteudo = (parte.get_payload(decode=True) or b"").decode("utf-8", "replace")
    if parte.get_content_type() == "text/html":
        conteudo = re.sub(r"(?is)<(script|style).*?</\1>", " ", conteudo)
        conteudo = re.sub(r"(?i)<br\s*/?>|</p>|</div>", "\n", conteudo)
        conteudo = re.sub(r"<[^>]+>", " ", conteudo)
    return conteudo


def _automatica(msg) -> bool:
    auto = (msg.get("Auto-Submitted") or "no").lower()
    if auto != "no" or msg.get("X-Autoreply") or msg.get("X-Autorespond"):
        return True
    return bool(re.search(r"(fora do escrit|out of office|aus[eê]ncia|automatic reply|resposta autom)",
                          msg.get("Subject") or "", re.I))


def _bounce(msg, bruto: bytes, de: str) -> list[str]:
    if not re.search(r"(mailer-daemon|postmaster)", de, re.I):
        return []
    falhou = [a for _, a in getaddresses([msg.get("X-Failed-Recipients") or ""]) if a]
    if not falhou:
        falhou = re.findall(rb"Final-Recipient:\s*rfc822;\s*<?([^\s>]+)", bruto, re.I)
        falhou = [f.decode("utf-8", "replace") for f in falhou]
    return sorted({f.strip().lower() for f in falhou})


def analisar(bruto: bytes) -> Recebida:
    msg = email.message_from_bytes(bruto, policy=email.policy.default)
    de = parseaddr(str(msg.get("From") or ""))[1].lower()
    try:
        data = email.utils.parsedate_to_datetime(str(msg.get("Date")))
    except Exception:
        data = None
    falhou = _bounce(msg, bruto, de)
    return Recebida(
        message_id=str(msg.get("Message-ID") or "").strip(),
        de=de,
        assunto=str(msg.get("Subject") or ""),
        data=data,
        in_reply_to=str(msg.get("In-Reply-To") or "").strip(),
        references=str(msg.get("References") or "").strip(),
        texto="" if falhou else limpar_resposta(_texto(msg)),
        automatica=_automatica(msg),
        falhou_para=falhou,
    )


def ler_caixa(conta: Conta, desde: dt.date, maximo: int = 300) -> list[Recebida]:
    """Mensagens da Caixa de entrada desde `desde` (somente leitura)."""
    criterio = "%02d-%s-%d" % (desde.day, MESES[desde.month - 1], desde.year)
    saida = []
    with imaplib.IMAP4_SSL(IMAP_HOST) as im:
        im.login(conta.email, conta.senha)
        im.select("INBOX", readonly=True)
        typ, dados = im.search(None, "SINCE", criterio)
        ids = (dados[0] or b"").split()[-maximo:]
        for num in ids:
            typ, partes = im.fetch(num, "(BODY.PEEK[])")
            for p in partes:
                if isinstance(p, tuple):
                    r = analisar(p[1])
                    if r.message_id:
                        saida.append(r)
    return saida


LISTA = re.compile(r'\((?P<flags>[^)]*)\) "(?P<sep>[^"]*)" (?P<nome>.+)$')


def pasta_rascunhos(im) -> str:
    """O nome muda com o idioma da conta ([Gmail]/Rascunhos, [Gmail]/Drafts): acha pela marca \\Drafts."""
    typ, linhas = im.list()
    for linha in linhas or []:
        m = LISTA.match(linha.decode("utf-8", "replace") if isinstance(linha, bytes) else str(linha))
        if m and "\\Drafts" in m.group("flags"):
            return m.group("nome")
    return '"[Gmail]/Drafts"'


def salvar_rascunho(conta: Conta, msg: EmailMessage) -> None:
    """Deixa a resposta pronta nos Rascunhos da própria conta, já na conversa do lead: abrir, revisar, enviar."""
    with imaplib.IMAP4_SSL(IMAP_HOST) as im:
        im.login(conta.email, conta.senha)
        im.append(pasta_rascunhos(im), r"(\Draft)", imaplib.Time2Internaldate(time.time()),
                  msg.as_bytes())
