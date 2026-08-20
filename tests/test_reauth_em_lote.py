"""Reautorizar dez canais nao pode custar dez disparos.

Em 19-20/08/2026 o dono autorizou os treze canais no navegador, a maquina
continuou com dez tokens mortos, e ele teve de refazer tudo. A causa nao foi
ele: autorizar no navegador nao grava nada — o `code` precisa ser trocado por
`refresh_token` em ate ~10 minutos, e o unico caminho era um terminal com o
SUPABASE_SERVICE_ROLE_KEY exportado, ou um disparo do reauth.yml POR CANAL.

Agora o reauth.yml aceita as dez URLs de uma vez. Estes testes cercam a parte
que quebra em silencio: separar as URLs coladas numa caixa de texto de uma
linha so.
"""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FONTE = (RAIZ / ".github" / "workflows" / "reauth.yml").read_text(encoding="utf-8")

# O regex sai do proprio workflow: se ele mudar la, o teste passa a medir o
# novo, e nao uma copia que envelhece em silencio.
_m = re.search(r're\.findall\(\s*\n?\s*r"([^"]+)"', FONTE)
assert _m, "nao achei o regex de separacao no reauth.yml"
PADRAO = _m.group(1)


def separa(blob: str) -> list[str]:
    return [u.strip() for u in re.findall(PADRAO, blob, re.S) if "code=" in u]


def campos(url: str) -> tuple[str, str]:
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    return q.get("state", ["?"])[0], q.get("code", ["?"])[0]


# URL real devolvida pelo Google, com o `iss=` e o `scope=` que quebraram a
# primeira versao deste separador.
def _url(slug: str, code: str) -> str:
    return ("http://localhost/?state=" + slug +
            "&iss=https://accounts.google.com&code=" + code +
            "&scope=https://www.googleapis.com/auth/youtube.force-ssl"
            "%20https://www.googleapis.com/auth/youtube.upload"
            "%20https://www.googleapis.com/auth/youtube")


TRES = [_url("sx-educacao", "4/0Aaaa"), _url("agla-level", "4/0Bbbb"),
        _url("seviye-seviye", "4/0Cccc")]
ESPERADO = [("sx-educacao", "4/0Aaaa"), ("agla-level", "4/0Bbbb"),
            ("seviye-seviye", "4/0Cccc")]


def test_separa_por_quebra_de_linha():
    assert [campos(u) for u in separa("\n".join(TRES))] == ESPERADO


def test_separa_por_espaco():
    """A caixa do workflow_dispatch e de UMA linha: o navegador pode trocar as
    quebras por espaco ao colar."""
    assert [campos(u) for u in separa(" ".join(TRES))] == ESPERADO


def test_separa_coladas_sem_separador_nenhum():
    """E pode simplesmente engoli-las, deixando as URLs grudadas."""
    assert [campos(u) for u in separa("".join(TRES))] == ESPERADO


def test_o_iss_e_o_scope_nao_partem_a_url():
    """O defeito que este teste existe para impedir: cortar em `https?://`
    generico parte a URL no `iss=https://accounts.google.com` e no `scope=`.
    O numero de URLs saia CERTO e o conteudo saia vazio — a pior forma de
    errar, porque parece que funcionou."""
    achadas = separa(TRES[0])
    assert len(achadas) == 1
    slug, code = campos(achadas[0])
    assert slug == "sx-educacao" and code == "4/0Aaaa"
    assert "accounts.google.com" in achadas[0], "a URL foi truncada antes do fim"


def test_lixo_em_volta_nao_atrapalha():
    assert [campos(u) for u in separa(f"  {TRES[0]}\n\n   {TRES[1]}  \n")] == ESPERADO[:2]


def test_campo_vazio_ou_sem_code_devolve_nada():
    assert separa("") == []
    assert separa("http://localhost/?state=x") == []


def test_o_workflow_grava_a_data_de_emissao():
    """Sem isso o vigia nunca sabe a idade do token (aprendizado 345), e a
    coluna congela na criacao da linha."""
    assert '"atualizado_em"' in FONTE


def test_uma_url_ruim_nao_derruba_as_outras():
    """Cada codigo e de uso unico: se uma falha aborta o lote, as outras nove
    autorizacoes humanas vao junto."""
    corpo = FONTE[FONTE.index("ok, falhas = [], []"):]
    assert "except Exception" in corpo and "falhas.append" in corpo


def test_o_canal_e_confirmado_pela_api_antes_de_gravar():
    """O `state` e so o que o link declarou; quem escolhe o canal e a pessoa na
    tela do Google. Gravar sem conferir poe o token de um canal na linha de
    outro — erro que ja custou um pacote inteiro em 14/08."""
    assert "mine=true" in FONTE and "canal ERRADO" in FONTE
