"""Nenhum dado de lead no log público do GitHub Actions (30/09, auditoria).

O repositório é público e os logs das rodadas também: calendly_para_crm, atuador_filas, link_formulario e
outros imprimiam nome, e-mail, telefone e até o link do formulário preenchido. Em vez de caçar cada print,
este módulo mascara a SAÍDA inteira quando roda no Actions (GITHUB_ACTIONS=true):

  - todo nome/e-mail/telefone que passar por `registrar()` (a `pedir()` dos robôs registra cada resposta
    da API) vira "•••" em qualquer linha impressa depois;
  - e-mail, telefone e query string de URL são mascarados por padrão, mesmo sem registro.

Localmente (no PC do dono) nada muda: a saída continua legível.
"""
from __future__ import annotations

import os
import re
import sys

# só campos de PESSOA ("name" genérico também vem de workflow, campo e agenda e mascarava "ligar", "lead")
CHAVES = {"firstName", "lastName", "contactName", "fullName", "firstNameLowerCase",
          "lastNameLowerCase", "email", "phone", "nome", "telefone"}
COMUNS = {"sem", "nome", "lead", "teste", "ligar", "para", "com", "delivery", "empresa", "contato", "cliente"}
_termos: set[str] = set()
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
FONE = re.compile(r"\+?\d[\d\s().-]{8,}\d")
QUERY = re.compile(r"(https?://\S+?)\?\S+")


def registrar(obj, _prof=0) -> None:
    if _prof > 6:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in CHAVES and isinstance(v, str):
                for parte in [v] + v.split():
                    if len(parte) >= 4 and parte.lower() not in COMUNS:
                        _termos.add(parte.lower())
            elif isinstance(v, (dict, list)):
                registrar(v, _prof + 1)
    elif isinstance(obj, list):
        for x in obj:
            registrar(x, _prof + 1)


def mascarar(texto: str) -> str:
    texto = QUERY.sub(r"\1?•••", texto)
    texto = EMAIL.sub("•••", texto)
    texto = FONE.sub("•••", texto)
    if _termos:
        for t in sorted(_termos, key=len, reverse=True):
            texto = re.sub(r"(?<!\w)%s(?!\w)" % re.escape(t), "•••", texto, flags=re.I)
    return texto


class _Saida:
    def __init__(self, orig):
        self._orig = orig

    def write(self, s):
        return self._orig.write(mascarar(s))

    def __getattr__(self, n):
        return getattr(self._orig, n)


def ativar() -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true" and not isinstance(sys.stdout, _Saida):
        sys.stdout, sys.stderr = _Saida(sys.stdout), _Saida(sys.stderr)


ativar()
