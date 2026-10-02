#!/usr/bin/env python3
"""Planilha de leads (CSV exportado do Google Sheets) -> fila qualificada e validada para o disparo.

    python coldmail/tools/qualificar.py planilha.csv fila.csv [--sem-mx]

O que faz com cada linha (nenhum dado de lead fica no repositório: entrada e saída são arquivos locais):
  - acha o e-mail mesmo em linha com colunas deslocadas (formulário antigo: data e IP no lugar do nome);
  - descarta: sem e-mail, teste, domínio digitado errado, duplicado, domínio sem servidor de e-mail (MX);
  - normaliza empresa ("DMP SISTEMA LTDA" -> "Dmp Sistema"), com a preposição certa (na/no/nos);
  - campos do e-mail: primeiro_nome, vendedores, gancho (frase pelo porte: vendedores + faturamento,
    sem citar valores) e convite_extra (gerente: "traga quem decide");
  - prioridade A (e-mail de empresa + decisor), B (decisor ou e-mail de empresa), C (resto).
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys

EMAIL = re.compile(r"[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PESSOAIS = {"gmail.com", "hotmail.com", "outlook.com", "live.com", "yahoo.com", "yahoo.com.br", "icloud.com",
            "bol.com.br", "uol.com.br", "terra.com.br", "hotmail.com.br", "outlook.com.br", "msn.com", "ig.com.br",
            "globo.com", "me.com"}
ERROS_DOMINIO = {"gmail.con", "gmial.com", "gmai.com", "gmail.co", "hotmial.com", "hotmail.con", "gamil.com",
                 "gmail.com.br", "outlook.con", "hotmal.com"}
DECISOR = re.compile(r"(c-level|s[oó]ci|diretor|dono|ceo|propriet|fundador|presidente|gerente|gestor|head|"
                     r"coordenador|empres[aá]ri)", re.I)
DONO = re.compile(r"(s[oó]ci|dono|diretor|ceo|c-level|propriet|fundador|presidente)", re.I)
MEIO = re.compile(r"(gerente|coordenador|gestor|head|supervisor)", re.I)
TESTE = re.compile(r"(teste|test@|dummy|v4company\.com|@fb\.com|exemplo|example)", re.I)
EMPRESA_RUIM = re.compile(r"^\s*(nenhuma|nenhum|confidencial|teste|testre|n/?a|-|\.|x|sem empresa|aut[oô]nom[oa])\s*$",
                          re.I)
MASC = (r"(grupo|supermercado|shopping|restaurante|instituto|escrit[oó]rio|col[eé]gio|hospital|hotel|atacad[aã]o|"
        r"posto|studio|est[uú]dio|sal[aã]o|centro|consult[oó]rio|laborat[oó]rio|banco|bar|mercado|armaz[eé]m|"
        r"ateli[eê]|atelier|sistema|condom[ií]nio|buffet|bistr[oô]|emp[oó]rio|dep[oó]sito|frigor[ií]fico|haras|"
        r"s[ií]tio|clube|club)")
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
MINUSC = {"de", "da", "do", "das", "dos", "e", "em"}


GRANDES = ("gmail", "hotmail", "outlook", "yahoo", "icloud", "live")
NAO_NOME = {"portal", "grupo", "loja", "contato", "comercial", "vendas", "empresa", "atendimento", "financeiro",
            "adm", "administrativo", "rh", "marketing", "sac", "suporte", "diretoria", "gerencia", "gerência", "dr",
            "dra", "sr", "sra", "eu", "nenhum", "teste"}


def dominio_parecido(d: str) -> bool:
    """gmail.cm, hotmail.co, outlok.com...: provedor grande com final errado (o domínio pode até existir)."""
    if d in PESSOAIS:
        return False
    base = d.split(".")[0]
    return any(base == g or (len(base) >= 5 and _distancia(base, g) == 1) for g in GRANDES)


def _distancia(a: str, b: str) -> int:
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atual = [i]
        for j, cb in enumerate(b, 1):
            atual.append(min(ant[j] + 1, atual[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = atual
    return ant[-1]


def primeiro_nome(nome: str, empresa: str) -> str:
    """'TÚLIO silva' -> 'Túlio'. Vazio quando o campo traz a empresa ('Portal Dovale', 'Grothe&Lima')."""
    if not nome or nome.startswith("<") or "@" in nome:
        return ""
    p = re.split(r"[\s&/.,-]+", nome.strip())[0]
    if len(p) < 2 or p.lower() in NAO_NOME or not re.match(r"^[^\W\d_]+$", p):
        return ""
    if empresa and p.lower() in re.split(r"[\s&/.,-]+", empresa.lower()):
        return ""
    return p[:1].upper() + p[1:].lower()


def empresa_curta(e: str) -> str:
    e = re.sub(r"\b(ltda|me|eireli|epp|s/?a|mei)\.?\s*$", "", (e or "").strip(), flags=re.I).strip(" -.,")
    if EMPRESA_RUIM.match(e or "x"):
        return ""
    if e.isupper() or e.islower():
        e = " ".join(w.lower() if (w.lower() in MINUSC and i) else w.capitalize()
                     for i, w in enumerate(e.lower().split()))
    return e


def preposicao(e: str) -> tuple[str, str, str]:
    """('na X', 'da X', 'a X'), com o gênero certo: no Grupo, nos Supermercados, na Artes Gráficas."""
    if not e:
        return "", "", ""
    w = e.split()[0].lower()
    if re.match(MASC + r"s$", w):
        return "nos " + e, "dos " + e, "os " + e
    if re.match(MASC + r"$", w):
        return "no " + e, "do " + e, "o " + e
    return "na " + e, "da " + e, "a " + e


def vendedores(t: str) -> str:
    t = (t or "").replace("_", " ").strip().lower()
    if not t or "#" in t or "<" in t or "@" in t:
        return ""
    if re.match(r"^\d+ a \d+$", t) or re.match(r"^(acima|mais) de \d+$", t):
        t += " vendedores"
    return t


def gancho(v: str, faturamento: str) -> str:
    n = [int(x) for x in re.findall(r"\d+", v)]
    porte = "" if not n else "grande" if ("mais de" in v or "acima" in v or max(n) > 10) else \
        "medio" if max(n) >= 6 else "pequeno"
    f = (faturamento or "").lower().replace("_", " ")
    fat = "alto" if ("300" in f or "100 a 300" in f) else "medio" if "70 a 100" in f else \
        "baixo" if ("abaixo" in f or "20 mil" in f) else ""
    abre = ("Com %s, " % v) if v else ""
    if porte == "grande" or (fat == "alto" and porte != "pequeno"):
        corpo = "o que costuma travar não é falta de lead: é cada vendedor atendendo de um jeito e ninguém " \
                "enxergando o funil inteiro."
        return (abre + corpo) if abre else "Na maioria das empresas do seu porte, " + corpo
    if porte == "medio" or fat == "medio":
        corpo = "cada lead que esfria sem resposta faz falta na meta do mês."
        return (abre + corpo) if abre else "No seu porte, " + corpo
    if porte == "pequeno" or fat == "baixo":
        corpo = "o primeiro passo costuma ser não perder quem já chega: responder rápido e insistir do jeito certo."
        return (abre + corpo) if abre else "Nessa fase, " + corpo
    return ""


def mes_ano(d: str) -> str:
    m = re.search(r"(\d{4})-(\d{2})-\d{2}", d or "")
    if m:
        return "%s de %s" % (MESES[int(m.group(2)) - 1], m.group(1))
    m = re.search(r"\d{1,2}/(\d{1,2})/(\d{4})", d or "")
    if m and 1 <= int(m.group(1)) <= 12:
        return "%s de %s" % (MESES[int(m.group(1)) - 1], m.group(2))
    return ""


def _resolve(host: str) -> bool:
    import dns.resolver
    for tipo in ("A", "AAAA"):
        try:
            dns.resolver.resolve(host, tipo, lifetime=8)
            return True
        except Exception:
            pass
    return False


def tem_mx(dominio: str, cache: dict) -> bool | None:
    """True/False; None se não deu para consultar (sem dnspython ou DNS fora): não descarta por isso."""
    if dominio in cache:
        return cache[dominio]
    try:
        import dns.resolver
        mx = [str(r.exchange).rstrip(".") for r in dns.resolver.resolve(dominio, "MX", lifetime=8)]
        # "null MX" (RFC 7505): o domínio declara que não recebe e-mail
        mx = [h for h in mx if h]
        cache[dominio] = bool(mx) and any(_resolve(h) for h in mx[:3])
    except ImportError:
        cache[dominio] = None
    except Exception as e:
        nome = type(e).__name__
        cache[dominio] = False if nome in ("NXDOMAIN", "NoAnswer", "NoNameservers") else None
    return cache[dominio]


def qualificar(linhas: list[list[str]], checar_mx: bool = True) -> tuple[list[dict], collections.Counter]:
    saida, motivos, vistos, cache = [], collections.Counter(), set(), {}
    for r in linhas:
        r = list(r) + [""] * (17 - len(r))
        deslocada = bool(re.match(r"\d{1,2}-\w+\.?-\d{4}", r[5])) and bool(re.match(r"\d+\.\d+\.\d+\.\d+", r[6]))
        if deslocada:
            nome, email, empresa, cargo, tam, fat, data = r[7], r[8], r[10], r[11], r[12], r[13], r[5]
        else:
            nome, email, cargo, data, empresa, tam, fat = r[1], r[2], r[4], r[6], r[7], r[8], r[13]
        m = EMAIL.search(email or "") or EMAIL.search(" ".join(r))
        email = (m.group(0) if m else "").strip().lower().rstrip(".")
        nome = (nome or "").strip()
        motivo = ""
        if not email:
            motivo = "sem e-mail"
        elif TESTE.search(email) or TESTE.search(nome) or "<test lead" in nome:
            motivo = "teste"
        elif email.split("@")[1] in ERROS_DOMINIO or dominio_parecido(email.split("@")[1]):
            motivo = "domínio digitado errado"
        elif email in vistos:
            motivo = "duplicado"
        elif checar_mx and tem_mx(email.split("@")[1], cache) is False:
            motivo = "domínio sem servidor de e-mail"
        if motivo:
            motivos[motivo] += 1
            continue
        vistos.add(email)
        emp = empresa_curta(empresa)
        na, da, artigo = preposicao(emp)
        v = vendedores(tam)
        corporativo = email.split("@")[1] not in PESSOAIS
        decisor = bool(DECISOR.search(cargo or ""))
        pontos = (2 if corporativo else 0) + (2 if decisor else 0) + (1 if emp else 0)
        saida.append({
            "prioridade": "A" if pontos >= 4 else "B" if pontos >= 3 else "C",
            "email": email,
            "primeiro_nome": primeiro_nome(nome, empresa),
            "empresa_curta": emp, "na_empresa": na, "da_empresa": da, "a_empresa": artigo,
            "cargo": (cargo or "").strip(), "vendedores": v,
            "gancho": gancho(v, fat),
            "convite_extra": "Se quiser, traga quem decide aí também." if (MEIO.search(cargo or "")
                                                                          and not DONO.search(cargo or "")) else "",
            "mes_ano": mes_ano(data),
        })
    ordem = {"A": 0, "B": 1, "C": 2}
    saida.sort(key=lambda x: ordem[x["prioridade"]])
    return saida, motivos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("planilha")
    ap.add_argument("fila")
    ap.add_argument("--sem-mx", action="store_true")
    a = ap.parse_args(argv)
    linhas = list(csv.reader(open(a.planilha, encoding="utf-8-sig")))[1:]
    fila, motivos = qualificar(linhas, checar_mx=not a.sem_mx)
    with open(a.fila, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fila[0].keys()) if fila else ["email"])
        w.writeheader()
        w.writerows(fila)
    print("%d linhas · %d na fila · descartes: %s · prioridade: %s" % (
        len(linhas), len(fila), dict(motivos), dict(collections.Counter(x["prioridade"] for x in fila))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
